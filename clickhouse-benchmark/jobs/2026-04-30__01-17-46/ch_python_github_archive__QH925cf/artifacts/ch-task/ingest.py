import os
from pathlib import Path

import clickhouse_connect


def main() -> None:
    host = os.environ.get("CLICKHOUSE_HOST")
    port = os.environ.get("CLICKHOUSE_PORT")
    username = os.environ.get("CLICKHOUSE_USERNAME")
    password = os.environ.get("CLICKHOUSE_PASSWORD")

    if not host or not port or not username or password is None:
        raise RuntimeError(
            "Missing ClickHouse connection details in environment variables."
        )

    client = clickhouse_connect.get_client(
        host=host,
        port=int(port),
        username=username,
        password=password,
    )

    client.command(
        """
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
        """
    )

    client.command(
        """
        INSERT INTO github_events
        SELECT
            id,
            type,
            actor,
            repo,
            payload,
            toUInt8(public) AS public,
            parseDateTimeBestEffort(created_at) AS created_at
        FROM url(
            'https://data.gharchive.org/2015-01-01-15.json.gz',
            'JSONEachRow',
            'id String, type String, actor JSON, repo JSON, payload JSON, public UInt8, created_at String'
        )
        """
    )

    row_count = client.query("SELECT count() FROM github_events").result_rows[0][0]

    output_path = Path("/home/user/ch-task/output.log")
    output_path.write_text(f"{row_count}\n")


if __name__ == "__main__":
    main()
