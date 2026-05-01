import os
import clickhouse_connect

def main():
    # Read connection details from environment variables
    host = os.getenv('CLICKHOUSE_HOST')
    port = int(os.getenv('CLICKHOUSE_PORT', 8443))
    username = os.getenv('CLICKHOUSE_USERNAME', 'default')
    password = os.getenv('CLICKHOUSE_PASSWORD')

    if not all([host, password]):
        print("Error: CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD environment variables must be set.")
        return

    # Connect to ClickHouse
    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=username,
        password=password,
        secure=True
    )

    # Create table
    # Note: JSON type might require 'allow_experimental_object_type' setting in some versions
    # but we will follow the requirements strictly.
    create_table_query = """
    CREATE TABLE IF NOT EXISTS github_events (
        id String,
        type String,
        actor JSON,
        repo JSON,
        payload JSON,
        public UInt8,
        created_at DateTime
    ) ENGINE = MergeTree()
    ORDER BY id
    """
    
    client.command(create_table_query)

    # Ingest data using url() function
    # The GH Archive data is JSONL. url() can handle .gz automatically.
    # We specify the schema in the url() function to match the table.
    # We use actor, repo, payload as String in url() and let ClickHouse cast to JSON.
    ingest_query = """
    INSERT INTO github_events
    SELECT 
        id, 
        type, 
        actor, 
        repo, 
        payload, 
        public, 
        parseDateTimeBestEffort(created_at)
    FROM url(
        'https://data.gharchive.org/2015-01-01-15.json.gz', 
        'JSONEachRow', 
        'id String, type String, actor String, repo String, payload String, public UInt8, created_at String'
    )
    """
    print("Starting ingestion...")
    client.command(ingest_query)
    print("Ingestion completed.")

    # Get row count
    result = client.query("SELECT count() FROM github_events")
    row_count = result.first_row[0]
    
    # Write row count to output.log
    output_log_path = '/home/user/ch-task/output.log'
    with open(output_log_path, 'w') as f:
        f.write(str(row_count))
    
    print(f"Total row count: {row_count}")
    print(f"Row count written to {output_log_path}")

if __name__ == "__main__":
    main()
