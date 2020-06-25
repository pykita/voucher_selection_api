import pandas as pd
from datetime import datetime, timedelta

def main():
    df = pd.read_parquet('pipeline/data.parquet.gzip')
    
    is_peru = df['country_code'] == 'Peru'
    df = df[is_peru]

    is_oreders_not_empty = df['total_orders'] != ''
    df = df[is_oreders_not_empty]
    
    #how can it appear in the dataset and have last_order_ts and first_order_ts?
    is_no_orders = df['total_orders'].astype(float) >= 1.0
    df = df[is_no_orders]
    # print(df.last_order_ts.max())
    # return    

    now_var = datetime(2018, 8, 5) 
    from_last_seen = 0
    to_last_seen = 30
    
    from_dt = now_var - timedelta(days=to_last_seen)
    to_dt = now_var - timedelta(days=from_last_seen)

    df_rc = df[(pd.to_datetime(df['last_order_ts']) >= from_dt) \
        & (pd.to_datetime(df['last_order_ts']) <= to_dt)]

    print(df_rc.head())

if __name__ == '__main__':
    main()
    