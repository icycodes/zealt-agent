import os
import clickhouse_connect

host = os.environ["CH_HOST"]
port = int(os.environ["CH_PORT"])
user = os.environ["CH_USER"]
password = os.environ["CH_PASSWORD"]

client = clickhouse_connect.get_client(
    host=host,
    port=port,
    username=user,
    password=password,
    connect_timeout=30,
    send_receive_timeout=120,
)

result = client.query("SELECT 1")
print(result.result_rows)
