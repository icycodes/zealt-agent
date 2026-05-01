import os
import clickhouse_connect

def main():
    host = os.environ.get('CLICKHOUSE_HOST', 'localhost')
    port = int(os.environ.get('CLICKHOUSE_PORT', 8443))
    user = os.environ.get('CLICKHOUSE_USER', 'default')
    password = os.environ.get('CLICKHOUSE_PASSWORD', '')

    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password,
        secure=True
    )

    create_table_query = """
    CREATE TABLE IF NOT EXISTS aapl_stock (
        Date Date,
        Open Float64,
        High Float64,
        Low Float64,
        Close Float64,
        Volume UInt64,
        OpenInt UInt64
    ) ENGINE = MergeTree()
    ORDER BY Date
    """
    client.command(create_table_query)
    print("Table aapl_stock created or already exists.")

    insert_query = """
    INSERT INTO aapl_stock
    SELECT * FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/aapl_stock.csv', 'CSVWithNames')
    """
    client.command(insert_query)
    print("Data ingested successfully from S3 into aapl_stock.")

    # Optional: verify count
    count = client.command("SELECT count() FROM aapl_stock")
    print(f"Total rows in aapl_stock: {count}")

if __name__ == '__main__':
    main()
