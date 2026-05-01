import os
import time
import json
import clickhouse_connect
from datetime import datetime

def run_benchmark():
    host = os.getenv('CH_HOST', 'localhost')
    port = int(os.getenv('CH_PORT', 8123))
    user = os.getenv('CH_USER', 'default')
    password = os.getenv('CH_PASSWORD', '')
    secure_str = os.getenv('CH_SECURE', 'False')
    secure = secure_str.lower() in ('true', '1', 't', 'y', 'yes')

    log_file = '/home/user/ch_benchmark/output.log'
    output_file = '/home/user/ch_benchmark/output.json'

    with open(log_file, 'a') as log:
        log.write(f"{datetime.now()}: Connecting to {host}:{port} as {user} (secure={secure})\n")
        
        try:
            client = clickhouse_connect.get_client(
                host=host,
                port=port,
                username=user,
                password=password,
                secure=secure
            )
            log.write(f"{datetime.now()}: Connected successfully\n")

            # 1. Create table
            client.command("DROP TABLE IF EXISTS events")
            client.command("""
                CREATE TABLE events (
                    id UInt64,
                    event_type String,
                    timestamp DateTime
                ) ENGINE = MergeTree ORDER BY id
            """)
            log.write(f"{datetime.now()}: Table 'events' created\n")

            # 2. Insert 1000 rows
            data = []
            event_types = ['click', 'view', 'purchase']
            now = datetime.now().replace(microsecond=0) # ClickHouse DateTime doesn't store microseconds by default
            for i in range(1, 1001):
                # Using i % 3 to distribute event types
                # 1 % 3 = 1 -> view
                # 2 % 3 = 2 -> purchase
                # 3 % 3 = 0 -> click
                data.append([i, event_types[i % 3], now])
            
            client.insert('events', data, column_names=['id', 'event_type', 'timestamp'])
            log.write(f"{datetime.now()}: Inserted 1000 rows\n")

            # 3. Execute query and measure time
            start_time = time.time()
            result = client.query('SELECT event_type, count() FROM events GROUP BY event_type')
            end_time = time.time()
            
            execution_time = end_time - start_time
            log.write(f"{datetime.now()}: Query executed in {execution_time:.4f} seconds\n")

            # 4. Format results
            # result.result_rows is a list of tuples
            results_list = [list(row) for row in result.result_rows]
            
            output_data = {
                "time_seconds": round(execution_time, 4),
                "results": results_list
            }

            with open(output_file, 'w') as f:
                json.dump(output_data, f)
            log.write(f"{datetime.now()}: Output written to {output_file}\n")

        except Exception as e:
            log.write(f"{datetime.now()}: Error: {str(e)}\n")
            raise e

if __name__ == "__main__":
    run_benchmark()
