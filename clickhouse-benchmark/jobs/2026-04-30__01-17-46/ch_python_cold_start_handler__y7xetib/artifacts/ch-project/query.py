import os

import clickhouse_connect


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


host = require_env("CH_HOST")
port = int(require_env("CH_PORT"))
user = require_env("CH_USER")
password = require_env("CH_PASSWORD")

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
