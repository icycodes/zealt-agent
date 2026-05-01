# S3 Data Ingestion with ClickHouse Python SDK

## Background
ClickHouse Cloud excels at querying external data lakes. The `s3()` table function allows seamless reading from S3-compatible object storage. In this task, you will write a Python script using the official HTTP client (`clickhouse-connect`) to ingest a public CSV dataset from S3 into a native ClickHouse MergeTree table.

## Requirements
- Write a Python script at `/home/user/ingest.py`.
- Connect to ClickHouse Cloud using credentials from environment variables: `CLICKHOUSE_HOST`, `CLICKHOUSE_PORT`, `CLICKHOUSE_USER`, and `CLICKHOUSE_PASSWORD`. Connection must be secure (`secure=True`).
- Create a table named `aapl_stock` (if it does not exist) with the following schema:
  - `Date` Date
  - `Open` Float64
  - `High` Float64
  - `Low` Float64
  - `Close` Float64
  - `Volume` UInt64
  - `OpenInt` UInt64
- The table should use the `MergeTree` engine, ordered by `Date`.
- Insert data into the `aapl_stock` table by reading directly from this public S3 URL: `https://datasets-documentation.s3.eu-west-3.amazonaws.com/aapl_stock.csv`. Use the `s3()` table function with the `CSVWithNames` format.

## Implementation Guide
1. Ensure `clickhouse-connect` is installed.
2. In `/home/user/ingest.py`, use `clickhouse_connect.get_client` to establish a connection.
3. Execute a `CREATE TABLE` command for the `aapl_stock` table.
4. Execute an `INSERT INTO ... SELECT * FROM s3(...)` command to load the data.
5. Print the number of rows inserted or a success message.

## Constraints
- Project path: `/home/user`
- The script must be executable by running `python3 /home/user/ingest.py`.