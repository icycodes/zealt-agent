#!/usr/bin/env python3
"""
S3 Data Ingestion with ClickHouse Python SDK
Reads a public CSV dataset from S3 into a native ClickHouse MergeTree table.
"""

import os
import sys
import clickhouse_connect


def get_env(var: str) -> str:
    """Retrieve a required environment variable or exit with an error."""
    value = os.environ.get(var)
    if not value:
        print(f"ERROR: Required environment variable '{var}' is not set.", file=sys.stderr)
        sys.exit(1)
    return value


def main():
    # ------------------------------------------------------------------ #
    # 1. Read connection credentials from environment variables           #
    # ------------------------------------------------------------------ #
    host = get_env("CLICKHOUSE_HOST")
    port = int(os.environ.get("CLICKHOUSE_PORT", 8443))
    user = get_env("CLICKHOUSE_USER")
    password = get_env("CLICKHOUSE_PASSWORD")

    print(f"Connecting to ClickHouse at {host}:{port} as '{user}' (secure=True) …")

    # ------------------------------------------------------------------ #
    # 2. Establish a secure connection                                    #
    # ------------------------------------------------------------------ #
    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password,
        secure=True,
    )

    print("Connection established successfully.")

    # ------------------------------------------------------------------ #
    # 3. Create the target table (if it does not already exist)           #
    # ------------------------------------------------------------------ #
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS aapl_stock
    (
        Date    Date,
        Open    Float64,
        High    Float64,
        Low     Float64,
        Close   Float64,
        Volume  UInt64,
        OpenInt UInt64
    )
    ENGINE = MergeTree()
    ORDER BY Date
    """

    client.command(create_table_sql)
    print("Table 'aapl_stock' is ready (created or already exists).")

    # ------------------------------------------------------------------ #
    # 4. Insert data via the s3() table function                          #
    # ------------------------------------------------------------------ #
    s3_url = "https://datasets-documentation.s3.eu-west-3.amazonaws.com/aapl_stock.csv"

    insert_sql = f"""
    INSERT INTO aapl_stock
    SELECT *
    FROM s3(
        '{s3_url}',
        'CSVWithNames'
    )
    """

    print(f"Loading data from S3:\n  {s3_url}")
    client.command(insert_sql)
    print("Data ingestion complete.")

    # ------------------------------------------------------------------ #
    # 5. Report the number of rows inserted                               #
    # ------------------------------------------------------------------ #
    result = client.query("SELECT count() FROM aapl_stock")
    row_count = result.first_row[0]
    print(f"Total rows in 'aapl_stock': {row_count:,}")


if __name__ == "__main__":
    main()
