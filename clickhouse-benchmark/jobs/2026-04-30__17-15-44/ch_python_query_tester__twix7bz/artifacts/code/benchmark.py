import os
import time
import json
import clickhouse_connect
from datetime import datetime

# Parse environment variables
ch_host = os.environ.get('CH_HOST', 'localhost')
ch_port = int(os.environ.get('CH_PORT', '8123'))
ch_user = os.environ.get('CH_USER', 'default')
ch_password = os.environ.get('CH_PASSWORD', '')
ch_secure_str = os.environ.get('CH_SECURE', 'False')
ch_secure = ch_secure_str.lower() in ('true', '1', 'yes')

client = clickhouse_connect.get_client(
    host=ch_host,
    port=ch_port,
    username=ch_user,
    password=ch_password,
    secure=ch_secure
)

# 1. Create table
client.command("DROP TABLE IF EXISTS events")
client.command("""
    CREATE TABLE events (
        id UInt64,
        event_type String,
        timestamp DateTime
    ) ENGINE = MergeTree ORDER BY id
""")

# 2. Insert 1000 rows
event_types = ['click', 'view', 'purchase']
rows = []
now = datetime.now()
for i in range(1, 1001):
    event_type = event_types[i % 3]
    rows.append([i, event_type, now])

client.insert('events', rows, column_names=['id', 'event_type', 'timestamp'])

# 3. Execute query and record time
query = "SELECT event_type, count() FROM events GROUP BY event_type"
start_time = time.time()
result = client.query(query)
end_time = time.time()

execution_time = end_time - start_time

# 4. Format output
results = [[row[0], row[1]] for row in result.result_rows]

output = {
    "time_seconds": execution_time,
    "results": results
}

# 5. Write to output.json
with open('/home/user/ch_benchmark/output.json', 'w') as f:
    json.dump(output, f)

# Make sure artifact directory exists
os.makedirs('/logs/artifacts/code', exist_ok=True)
with open('/logs/artifacts/output.json', 'w') as f:
    json.dump(output, f)

import shutil
shutil.copy2('/home/user/ch_benchmark/benchmark.py', '/logs/artifacts/code/benchmark.py')
