#!/usr/bin/env python3
"""
S3 Data Ingestion with ClickHouse Python SDK

This script connects to ClickHouse Cloud and ingests a public CSV dataset
from S3 into a native ClickHouse MergeTree table.
"""

import os
import clickhouse_connect


def main():
    # Get connection credentials from environment variables
    host = os.environ.get('CLICKHOUSE_HOST')
    port = os.environ.get('CLICKHOUSE_PORT')
    user = os.environ.get('CLICKHOUSE_USER')
    password = os.environ.get('CLICKHOUSE_PASSWORD')

    # Validate required environment variables
    if not all([host, port, user, password]):
        raise ValueError(
            "Missing required environment variables. Please set: "
            "CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD"
        )

    # Establish secure connection to ClickHouse Cloud
    client = clickhouse_connect.get_client(
        host=host,
        port=int(port),
        username=user,
        password=password,
        secure=True
    )

    print("Connected to ClickHouse Cloud successfully.")

    # Create table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS aapl_stock (
        Date Date,
        Open Float64,
        High Float64,
        Low Float64,
        Close Float64,
        Volume UInt64,
        OpenInt UInt64
    ) ENGINE = MergeTree()
    ORDER BY Date
    """

    client.command(create_table_query)
    print("Table 'aapl_stock' created or already exists.")

    # Insert data from S3 using the s3() table function
    s3_url = 'https://datasets-documentation.s3.eu-west-3.amazonaws.com/aapl_stock.csv'

    insert_query = f"""
    INSERT INTO aapl_stock
    SELECT * FROM s3('{s3_url}', 'CSVWithNames')
    """

    result = client.command(insert_query)
    print(f"Data ingestion completed. Rows inserted: {result}")


if __name__ == '__main__':
    main()