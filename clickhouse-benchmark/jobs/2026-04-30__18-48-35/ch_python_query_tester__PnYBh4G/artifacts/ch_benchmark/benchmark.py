#!/usr/bin/env python3
"""
ClickHouse Python Query Benchmark Script
"""
import os
import json
import time
import sys
from datetime import datetime

try:
    import clickhouse_connect
except ImportError:
    print("Error: clickhouse-connect is not installed. Run: pip install clickhouse-connect", file=sys.stderr)
    sys.exit(1)

def get_env_var(name, default=None):
    """Get environment variable with optional default"""
    value = os.environ.get(name, default)
    if value is None:
        print(f"Error: Environment variable {name} is not set", file=sys.stderr)
        sys.exit(1)
    return value

def parse_bool(value):
    """Parse string to boolean"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'on')
    return bool(value)

def main():
    # Get connection parameters from environment variables
    host = get_env_var('CH_HOST', 'localhost')
    port = int(get_env_var('CH_PORT', '8123'))
    user = get_env_var('CH_USER', 'default')
    password = get_env_var('CH_PASSWORD', '')
    secure = parse_bool(get_env_var('CH_SECURE', 'False'))

    # Log file path
    log_file = '/home/user/ch_benchmark/output.log'
    output_file = '/home/user/ch_benchmark/output.json'

    # Redirect stdout and stderr to log file
    sys.stdout = open(log_file, 'w')
    sys.stderr = sys.stdout

    try:
        # Connect to ClickHouse
        print(f"Connecting to ClickHouse at {host}:{port} (secure={secure})")
        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=user,
            password=password,
            secure=secure
        )
        print("Connected successfully")

        # Step 1: Create the events table
        print("Creating table 'events'...")
        create_table_query = """
        CREATE TABLE IF NOT EXISTS events (
            id UInt64,
            event_type String,
            timestamp DateTime
        ) ENGINE = MergeTree ORDER BY id
        """
        client.command(create_table_query)
        print("Table created successfully")

        # Step 2: Insert exactly 1000 rows
        print("Inserting 1000 rows into 'events' table...")
        current_time = datetime.now()
        
        # Prepare data for 1000 rows
        data = []
        event_types = ['click', 'view', 'purchase']
        
        for i in range(1, 1001):
            id_val = i
            event_type = event_types[i % 3]  # Distribute evenly among the three types
            timestamp = current_time
            data.append((id_val, event_type, timestamp))
        
        # Insert data
        client.insert('events', data, column_names=['id', 'event_type', 'timestamp'])
        print(f"Inserted {len(data)} rows successfully")

        # Step 3: Execute the GROUP BY query and measure time
        print("Executing query: SELECT event_type, count() FROM events GROUP BY event_type")
        query = "SELECT event_type, count() FROM events GROUP BY event_type"
        
        start_time = time.time()
        result = client.query(query)
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"Query executed in {execution_time:.4f} seconds")

        # Step 4: Format results
        results = []
        for row in result.result_rows:
            results.append([row[0], row[1]])
        
        print(f"Results: {results}")

        # Step 5: Write output to JSON file
        output_data = {
            "time_seconds": round(execution_time, 2),
            "results": results
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"Output written to {output_file}")
        print(f"Final output: {json.dumps(output_data, indent=2)}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        sys.stdout.close()

if __name__ == '__main__':
    main()