import os

import clickhouse_connect


def get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    host = get_env("CLICKHOUSE_HOST")
    port = int(get_env("CLICKHOUSE_PORT"))
    user = get_env("CLICKHOUSE_USER")
    password = get_env("CLICKHOUSE_PASSWORD")

    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password,
        secure=True,
    )

    client.command(
        """
        CREATE TABLE IF NOT EXISTS test_events (
            id UInt64,
            event_type String
        )
        ENGINE = MergeTree
        ORDER BY id
        """
    )

    rows = [(1, "push"), (2, "pull_request"), (3, "issue")]
    client.insert("test_events", rows, column_names=["id", "event_type"])

    result = client.query("SELECT count() AS row_count FROM test_events")
    row_count = result.result_rows[0][0]
    print(f"Row count: {row_count}")


if __name__ == "__main__":
    main()
