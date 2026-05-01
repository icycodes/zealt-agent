# ClickHouse Python SDK Ingestion

## Background
Write a Python script to interact with ClickHouse Cloud using the official `clickhouse-connect` SDK.

## Requirements
- Connect to ClickHouse Cloud using the following environment variables: `CLICKHOUSE_HOST`, `CLICKHOUSE_PORT`, `CLICKHOUSE_USER`, `CLICKHOUSE_PASSWORD`.
- Create a table named `test_events` with columns `id UInt64` and `event_type String`. Use `MergeTree` engine ordered by `id`.
- Insert 3 rows of data: `[1, 'push']`, `[2, 'pull_request']`, `[3, 'issue']`.
- Query the table to count the number of rows and print the result.

## Implementation
1. Initialize a Python project in `/home/user/ch_project`.
2. Install `clickhouse-connect`.
3. Create a script `ingest.py` that connects to the database, creates the table, inserts data, and queries the count.
4. Run the script and redirect output to `/home/user/ch_project/output.log`.

## Constraints
- Project path: `/home/user/ch_project`
- Log file: `/home/user/ch_project/output.log`