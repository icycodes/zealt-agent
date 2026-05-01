#!/usr/bin/env python3
import os
import sys

import clickhouse_connect


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        print(f"Missing required environment variable: {name}", file=sys.stderr)
        sys.exit(1)
    return value


def main() -> None:
    host = require_env("CLICKHOUSE_HOST")
    port = int(require_env("CLICKHOUSE_PORT"))
    user = require_env("CLICKHOUSE_USER")
    password = require_env("CLICKHOUSE_PASSWORD")

    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password,
        secure=True,
    )

    client.command(
        """
        CREATE TABLE IF NOT EXISTS aapl_stock (
            Date Date,
            Open Float64,
            High Float64,
            Low Float64,
            Close Float64,
            Volume UInt64,
            OpenInt UInt64
        )
        ENGINE MergeTree
        ORDER BY Date
        """
    )

    s3_url = "https://datasets-documentation.s3.eu-west-3.amazonaws.com/aapl_stock.csv"
    expected_rows = client.query(
        f"SELECT count() FROM s3('{s3_url}', 'CSVWithNames')"
    ).result_rows[0][0]

    client.command(
        f"INSERT INTO aapl_stock SELECT * FROM s3('{s3_url}', 'CSVWithNames')"
    )

    print(f"Inserted {expected_rows} rows into aapl_stock.")


if __name__ == "__main__":
    main()
