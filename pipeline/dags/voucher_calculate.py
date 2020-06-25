from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models.connection import Connection
from airflow.utils.dates import days_ago
from datetime import timedelta, datetime
from airflow import settings
from airflow import DAG
from sys import maxsize
from os import getenv
import pandas as pd

default_args = {
    'owner': 'Nikita',
    'start_date': datetime.now(),
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
    'depends_on_past': False
}

voucher_connection_id = 'voucher_connection'
max_value = 10000

# there might me a way to organize this data structure only once 
# and then share it between the services
segments = [
    {
        'type': 'recency_segment',
        'name': '0-30',
        'lower': 0,
        'upper': 30
    },
    {
        'type': 'recency_segment',
        'name': '31-60',
        'lower': 31,
        'upper': 60
    },
    {
        'type': 'recency_segment',
        'name': '61-90',
        'lower': 61,
        'upper': 90
    },
    {
        'type': 'recency_segment',
        'name': '91-120',
        'lower': 91,
        'upper': 120
    },
    {
        'type': 'recency_segment',
        'name': '121-180',
        'lower': 121,
        'upper': 180
    },
    {
        'type': 'recency_segment',
        'name': '180+',
        'lower': 180,
        'upper': max_value
    },
    {
        'type': 'frequency_segment',
        'name': '0-4',
        'lower': 0,
        'upper': 4
    },
    {
        'type': 'frequency_segment',
        'name': '5-13',
        'lower': 5,
        'upper': 13
    },
    {
        'type': 'frequency_segment',
        'name': '14-37',
        'lower': 14,
        'upper': 37
    },
    {
        'type': 'frequency_segment',
        'name': '38+',
        'lower': 38,
        'upper': max_value
    }
]

dag = DAG(
    'voucher_calculation',
    default_args=default_args,
    catchup=False,
    description='A DAG which setup values for all ranges',
    max_active_runs=1,
    concurrency=1,
    schedule_interval=timedelta(days=1) # the job should be run daily to get updated segments values
)

def create_connection():
    pg_conn = Connection(
        conn_id=voucher_connection_id,
        conn_type='postgres',
        host=getenv('POSTGRES_HOST'),
        schema=getenv('POSTGRES_DB'),
        login=getenv('POSTGRES_USER'),
        password=getenv('POSTGRES_PASSWORD'),
        port=5432
    )

    session = settings.Session()
    session.query(Connection).filter(Connection.conn_id == voucher_connection_id).delete()
    session.add(pg_conn)
    session.commit()

create_connection = PythonOperator(
    task_id='create_connection',
    python_callable=create_connection,
    dag=dag)


def validate_dataset():
    df = pd.read_parquet('/usr/local/airflow/data.parquet.gzip')
    
    is_peru = df['country_code'] == 'Peru'
    df = df[is_peru]

    is_oreders_not_empty = df['total_orders'] != ''
    df = df[is_oreders_not_empty]
    
    #how can it appear in the dataset and have last_order_ts and first_order_ts?
    is_no_orders = df['total_orders'].astype(float) >= 1.0
    df = df[is_no_orders]

    df.to_parquet('/usr/local/airflow/validated.data.parquet.gzip',
              compression='gzip')

validation_operator = PythonOperator(
    task_id='validate_dataset',
    python_callable=validate_dataset,
    dag=dag)

def get_frequency_voucher_amount(df, from_orders, to_orders):
    df_segment = df[(df['total_orders'].astype(float) >= from_orders) \
        & (df['total_orders'].astype(float) <= to_orders)]

    amount = df_segment.groupby(['voucher_amount']).count().total_orders.idxmax()

    return amount

def get_recency_voucher_amount(df, from_last_seen, to_last_seen):
    # in order to have more representative results 
    # we need to replace current execution date with a static value
    now_var = datetime(2018, 8, 5) 
    
    from_dt = now_var - timedelta(days=to_last_seen)
    to_dt = now_var - timedelta(days=from_last_seen)

    df_rc = df[(pd.to_datetime(df['last_order_ts']) >= from_dt) \
        & (pd.to_datetime(df['last_order_ts']) <= to_dt)]

    amount = df_rc.groupby(['voucher_amount']).count().total_orders.idxmax()

    return amount

def store_segment_info(amount, segment_type, segment_name):
    query = f'''
        update voucher_segments
        set voucher_amount = {int(amount)}
        where {segment_type} = '{segment_name}'
    '''

    hook = PostgresHook(postgres_conn_id=voucher_connection_id)

    with hook.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()

def populate_segments():
    df = pd.read_parquet('/usr/local/airflow/validated.data.parquet.gzip')

    for segment in segments:
        try:
            if segment['type'] == 'recency_segment':
                amount = get_recency_voucher_amount(df, segment['lower'], segment['upper'])
            elif segment['type'] == 'frequency_segment':
                amount = get_frequency_voucher_amount(df, segment['lower'], segment['upper'])

            store_segment_info(amount, segment['type'], segment['name'])
        except Exception as e:
            print(e)
            print(f'Error on populating {segment["type"]} with name {segment["name"]}')

populate_segments = PythonOperator(
    task_id='populate_segments',
    python_callable=populate_segments,
    dag=dag)



create_connection >> validation_operator >> populate_segments