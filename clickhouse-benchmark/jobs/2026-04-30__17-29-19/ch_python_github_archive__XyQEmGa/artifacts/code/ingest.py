import os
import clickhouse_connect

def main():
    host = os.getenv('CLICKHOUSE_HOST')
    port = int(os.getenv('CLICKHOUSE_PORT', 8443))
    username = os.getenv('CLICKHOUSE_USERNAME')
    password = os.getenv('CLICKHOUSE_PASSWORD')

    print(f"Connecting to {host}:{port}...")
    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=username,
        password=password,
        secure=True if port in [443, 8443] else False
    )

    # Enable experimental JSON type
    try:
        client.command('SET allow_experimental_object_type = 1')
    except Exception as e:
        print(f"Warning: Could not set allow_experimental_object_type: {e}")

    try:
        client.command('SET allow_experimental_json_type = 1')
    except Exception as e:
        print(f"Warning: Could not set allow_experimental_json_type: {e}")

    # Create table
    # Note: Using JSON type as requested. 
    # In some versions it might be Object('json') or JSON.
    print("Creating table github_events...")
    client.command("""
        CREATE TABLE IF NOT EXISTS github_events (
            id String,
            type String,
            actor JSON,
            repo JSON,
            payload JSON,
            public UInt8,
            created_at DateTime
        ) ENGINE = MergeTree
        ORDER BY id
    """)

    # Ingest data using url() function
    # The format is JSONEachRow
    print("Ingesting data from GitHub Archive...")
    ingest_query = """
        INSERT INTO github_events
        SELECT
            id,
            type,
            actor,
            repo,
            payload,
            public,
            created_at
        FROM url('https://data.gharchive.org/2015-01-01-15.json.gz', 'JSONEachRow')
    """
    client.command(ingest_query)

    # Get row count
    row_count = client.command('SELECT count() FROM github_events')
    print(f"Total row count: {row_count}")

    # Write to log file
    log_path = '/home/user/ch-task/output.log'
    with open(log_path, 'w') as f:
        f.write(str(row_count))
    
    print(f"Row count written to {log_path}")

if __name__ == '__main__':
    main()
