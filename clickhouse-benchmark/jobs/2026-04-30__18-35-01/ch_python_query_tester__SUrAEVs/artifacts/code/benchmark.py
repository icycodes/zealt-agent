import os
import json
import time
import datetime
import clickhouse_connect

def main():
    # Load environment variables
    host = os.environ.get('CH_HOST', 'localhost')
    port = int(os.environ.get('CH_PORT', 8123))
    user = os.environ.get('CH_USER', 'default')
    password = os.environ.get('CH_PASSWORD', '')
    secure_str = os.environ.get('CH_SECURE', 'False').lower()
    secure = secure_str == 'true'

    print(f"Connecting to ClickHouse at {host}:{port} (user: {user}, secure: {secure})")

    try:
        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=user,
            password=password,
            secure=secure
        )
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    # 1. Create table
    print("Creating table 'events'...")
    client.command("DROP TABLE IF EXISTS events")
    client.command("""
        CREATE TABLE events (
            id UInt64,
            event_type String,
            timestamp DateTime
        ) ENGINE = MergeTree ORDER BY id
    """)

    # 2. Insert 1000 rows
    print("Inserting 1000 rows...")
    event_types = ['click', 'view', 'purchase']
    data = []
    now = datetime.datetime.now()
    for i in range(1, 1001):
        data.append([i, event_types[i % 3], now])
    
    client.insert('events', data, column_names=['id', 'event_type', 'timestamp'])

    # 3. Execute query and 4. Record time
    print("Executing query...")
    start_time = time.time()
    result = client.query("SELECT event_type, count() FROM events GROUP BY event_type")
    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"Query executed in {execution_time:.4f} seconds")

    # 5. Write output.json
    output = {
        "time_seconds": execution_time,
        "results": result.result_rows
    }
    
    output_path = '/home/user/ch_benchmark/output.json'
    with open(output_path, 'w') as f:
        json.dump(output, f)
    
    print(f"Results written to {output_path}")

if __name__ == "__main__":
    main()
