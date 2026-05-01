#!/usr/bin/env python3
"""
Ingest GitHub Archive data into ClickHouse Cloud
"""

import os
import clickhouse_connect
from datetime import datetime


def main():
    # Read connection details from environment variables
    host = os.environ.get('CLICKHOUSE_HOST')
    port = os.environ.get('CLICKHOUSE_PORT')
    username = os.environ.get('CLICKHOUSE_USERNAME')
    password = os.environ.get('CLICKHOUSE_PASSWORD')
    
    # Validate required environment variables
    if not all([host, port, username, password]):
        raise ValueError("Missing required environment variables. Please set: CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD")
    
    print(f"Connecting to ClickHouse at {host}:{port}...")
    
    # Connect to ClickHouse
    client = clickhouse_connect.get_client(
        host=host,
        port=int(port),
        username=username,
        password=password
    )
    
    # Test connection
    print("Testing connection...")
    result = client.query('SELECT 1')
    print("Connection successful!")
    
    # Create the github_events table with MergeTree engine
    print("Creating table 'github_events'...")
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS github_events
    (
        id String,
        type String,
        actor JSON,
        repo JSON,
        payload JSON,
        public UInt8,
        created_at DateTime
    )
    ENGINE = MergeTree()
    ORDER BY id
    '''
    
    client.command(create_table_query)
    print("Table created successfully!")
    
    # Ingest data from GitHub Archive using the url() table function
    print("Ingesting data from GitHub Archive...")
    # The GitHub Archive data is in JSON format with fields matching our schema
    ingest_query = '''
    INSERT INTO github_events (id, type, actor, repo, payload, public, created_at)
    SELECT
        id::String,
        type::String,
        actor::JSON,
        repo::JSON,
        payload::JSON,
        public::UInt8,
        toDateTime(created_at) as created_at
    FROM url(
        'https://data.gharchive.org/2015-01-01-15.json.gz',
        'JSONEachRow'
    )
    '''
    
    result = client.command(ingest_query)
    print(f"Data ingestion completed!")
    
    # Get the row count
    print("Getting row count...")
    row_count_result = client.query('SELECT count() FROM github_events')
    row_count = row_count_result.first_row[0]
    print(f"Total rows in github_events: {row_count}")
    
    # Write row count to output.log
    output_log_path = '/home/user/ch-task/output.log'
    with open(output_log_path, 'w') as f:
        f.write(f"Total rows in github_events: {row_count}\n")
        f.write(f"Ingestion completed at: {datetime.now().isoformat()}\n")
    
    print(f"Row count written to {output_log_path}")
    print("Ingestion completed successfully!")


if __name__ == '__main__':
    main()