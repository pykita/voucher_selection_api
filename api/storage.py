import psycopg2


def get_voucher_amount(segment_name, segment_value):
    try:
        conn = psycopg2.connect("dbname='voucher' user='voucher' host='localhost' password='voucher' port=5433")
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
