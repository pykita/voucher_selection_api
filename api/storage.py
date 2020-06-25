import psycopg2
from os import getenv

params = {
    'database': getenv('POSTGRES_DB'),
    'user': getenv('POSTGRES_USER'),
    'host': getenv('POSTGRES_HOST'),
    'password': getenv('POSTGRES_PASSWORD'),
    'port': getenv('POSTGRES_PORT')
}

def get_voucher_amount(segment_name, segment_value):
    try:
        conn = psycopg2.connect(**params)
    except:
        print("I am unable to connect to the database")

    cursor = conn.cursor()

    query = f'''
        select
            voucher_amount
        from voucher_segments
        where {segment_name} = '{segment_value}'
    '''

    cursor.execute(query)

    amount = cursor.fetchone()

    cursor.close()
    conn.close()

    return amount[0] if amount else None
