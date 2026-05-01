#!/usr/bin/env python3
"""
ClickHouse Cloud Ingestion Script
Connects to ClickHouse Cloud, creates a table, inserts data, and queries the count.
"""

import os
import clickhouse_connect


def main():
    # Get connection details from environment variables
    host = os.environ.get('CLICKHOUSE_HOST')
    port = os.environ.get('CLICKHOUSE_PORT')
    user = os.environ.get('CLICKHOUSE_USER')
    password = os.environ.get('CLICKHOUSE_PASSWORD')
    
    # Validate required environment variables
    if not all([host, port, user, password]):
        print("Error: Missing required environment variables")
        print("Required: CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD")
        return
    
    print(f"Connecting to ClickHouse at {host}:{port}...")
    
    # Connect to ClickHouse Cloud
    client = clickhouse_connect.get_client(
        host=host,
        port=int(port),
        username=user,
        password=password
    )
    
    print("Connected successfully!")
    
    # Drop table if it exists (for clean testing)
    print("Dropping existing table (if any)...")
    client.command('DROP TABLE IF EXISTS test_events')
    
    # Create the test_events table
    print("Creating table 'test_events'...")
    create_table_query = '''
    CREATE TABLE test_events (
        id UInt64,
        event_type String
    ) ENGINE = MergeTree()
    ORDER BY id
    '''
    client.command(create_table_query)
    print("Table created successfully!")
    
    # Insert data
    print("Inserting data...")
    data = [
        [1, 'push'],
        [2, 'pull_request'],
        [3, 'issue']
    ]
    client.insert('test_events', data)
    print(f"Inserted {len(data)} rows successfully!")
    
    # Query the count
    print("Querying row count...")
    result = client.query('SELECT COUNT(*) as count FROM test_events')
    
    # Get the count value
    count = result.first_row[0]
    print(f"Total rows in test_events: {count}")
    
    # Also query all data for verification
    print("\nAll data in table:")
    all_data = client.query('SELECT * FROM test_events ORDER BY id')
    for row in all_data.named_results():
        print(f"  id={row['id']}, event_type={row['event_type']}")


if __name__ == '__main__':
    main()