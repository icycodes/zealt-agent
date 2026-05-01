import os
import clickhouse_connect

def main():
    # Connect to ClickHouse Cloud using environment variables
    host = os.getenv('CLICKHOUSE_HOST')
    port_str = os.getenv('CLICKHOUSE_PORT', '8443')
    port = int(port_str)
    user = os.getenv('CLICKHOUSE_USER', 'default')
    password = os.getenv('CLICKHOUSE_PASSWORD', '')

    try:
        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=user,
            password=password,
            secure=True
        )
        print(f"Connected to ClickHouse at {host}:{port}")
    except Exception as e:
        print(f"Failed to connect to ClickHouse: {e}")
        return

    # Create table
    print("Creating table test_events...")
    client.command("""
        CREATE TABLE IF NOT EXISTS test_events (
            id UInt64,
            event_type String
        ) ENGINE = MergeTree
        ORDER BY id
    """)

    # Insert data
    print("Inserting data...")
    data = [
        [1, 'push'],
        [2, 'pull_request'],
        [3, 'issue']
    ]
    client.insert('test_events', data, column_names=['id', 'event_type'])

    # Query the table to count rows
    print("Querying row count...")
    result = client.query('SELECT count() FROM test_events')
    row_count = result.result_set[0][0]
    print(f"Total rows in test_events: {row_count}")

if __name__ == "__main__":
    main()
