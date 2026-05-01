"""
ClickHouse Cloud ingestion script.

Reads connection details from environment variables:
  CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD

Workflow:
  1. Connect to ClickHouse Cloud.
  2. Create table `test_events` (MergeTree, ordered by id).
  3. Insert 3 sample rows.
  4. Query and print the row count.
"""

import os
import clickhouse_connect


def get_client() -> clickhouse_connect.driver.Client:
    host = os.environ["CLICKHOUSE_HOST"]
    port = int(os.environ.get("CLICKHOUSE_PORT", 8443))
    user = os.environ.get("CLICKHOUSE_USER", "default")
    password = os.environ["CLICKHOUSE_PASSWORD"]

    print(f"Connecting to ClickHouse at {host}:{port} as '{user}' ...")
    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password,
        secure=True,
    )
    print("Connection established.")
    return client


def create_table(client: clickhouse_connect.driver.Client) -> None:
    ddl = """
    CREATE TABLE IF NOT EXISTS test_events (
        id         UInt64,
        event_type String
    )
    ENGINE = MergeTree()
    ORDER BY id
    """
    client.command(ddl)
    print("Table 'test_events' ready (created or already exists).")


def insert_rows(client: clickhouse_connect.driver.Client) -> None:
    rows = [
        [1, "push"],
        [2, "pull_request"],
        [3, "issue"],
    ]
    client.insert("test_events", rows, column_names=["id", "event_type"])
    print(f"Inserted {len(rows)} rows into 'test_events'.")


def query_count(client: clickhouse_connect.driver.Client) -> None:
    result = client.query("SELECT count() FROM test_events")
    count = result.first_row[0]
    print(f"Row count in 'test_events': {count}")


def main() -> None:
    client = get_client()
    try:
        create_table(client)
        insert_rows(client)
        query_count(client)
    finally:
        client.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()
