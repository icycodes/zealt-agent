import os
import clickhouse_connect

def main():
    # Connection parameters from environment variables
    host = os.getenv('CLICKHOUSE_HOST')
    port = int(os.getenv('CLICKHOUSE_PORT', 8443))
    user = os.getenv('CLICKHOUSE_USER')
    password = os.getenv('CLICKHOUSE_PASSWORD')

    if not all([host, user, password]):
        print("Error: CLICKHOUSE_HOST, CLICKHOUSE_USER, and CLICKHOUSE_PASSWORD must be set.")
        return

    # Establish connection
    try:
        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=user,
            password=password,
            secure=True
        )
        print(f"Connected to ClickHouse at {host}")
    except Exception as e:
        print(f"Failed to connect to ClickHouse: {e}")
        return

    # Create table schema
    create_table_query = """
    CREATE TABLE IF NOT EXISTS aapl_stock (
        Date Date,
        Open Float64,
        High Float64,
        Low Float64,
        Close Float64,
        Volume UInt64,
        OpenInt UInt64
    ) ENGINE = MergeTree
    ORDER BY Date
    """
    
    try:
        client.command(create_table_query)
        print("Table 'aapl_stock' checked/created.")
    except Exception as e:
        print(f"Failed to create table: {e}")
        return

    # Ingest data from S3
    s3_url = 'https://datasets-documentation.s3.eu-west-3.amazonaws.com/aapl_stock.csv'
    insert_query = f"""
    INSERT INTO aapl_stock
    SELECT * FROM s3('{s3_url}', 'CSVWithNames')
    """

    try:
        print(f"Ingesting data from {s3_url}...")
        client.command(insert_query)
        
        # Verify insertion
        result = client.command("SELECT count() FROM aapl_stock")
        print(f"Success: Ingested data into 'aapl_stock'. Total rows: {result}")
    except Exception as e:
        print(f"Failed to ingest data: {e}")

if __name__ == "__main__":
    main()
