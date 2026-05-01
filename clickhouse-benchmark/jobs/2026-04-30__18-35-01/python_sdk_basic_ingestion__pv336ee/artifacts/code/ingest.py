import os
import clickhouse_connect

def main():
    # Fetch connection details from environment variables
    host = os.getenv('CLICKHOUSE_HOST')
    port = int(os.getenv('CLICKHOUSE_PORT', 8443))
    user = os.getenv('CLICKHOUSE_USER', 'default')
    password = os.getenv('CLICKHOUSE_PASSWORD', '')

    print(f"Connecting to {host}:{port} as {user}...")

    # Initialize the client
    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password,
        secure=True
    )

    # Create the table
    print("Creating table 'test_events'...")
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

    # Query the count
    print("Querying row count...")
    result = client.query('SELECT count() FROM test_events')
    row_count = result.result_set[0][0]
    print(f"Total rows in 'test_events': {row_count}")

if __name__ == "__main__":
    main()
