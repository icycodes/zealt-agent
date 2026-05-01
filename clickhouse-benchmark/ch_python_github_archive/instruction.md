# Ingest GitHub Archive into ClickHouse Cloud

## Background
You need to write a Python script to ingest GitHub Archive events into ClickHouse Cloud using the official `clickhouse-connect` Python SDK. The GitHub Archive dataset contains public events from GitHub, and you'll be fetching a single hour of data.

## Requirements
- Create a Python script `/home/user/ch-task/ingest.py`.
- The script must read connection details from the following environment variables: `CLICKHOUSE_HOST`, `CLICKHOUSE_PORT`, `CLICKHOUSE_USERNAME`, `CLICKHOUSE_PASSWORD`.
- Connect to ClickHouse using `clickhouse-connect`.
- Create a table named `github_events` with the `MergeTree` engine ordered by `id`. The table schema must include at least: `id String`, `type String`, `actor JSON`, `repo JSON`, `payload JSON`, `public UInt8`, `created_at DateTime`.
- Ingest the data from `https://data.gharchive.org/2015-01-01-15.json.gz` into the `github_events` table. You can use ClickHouse's `url()` table function to do this efficiently.
- After ingestion, write the total row count of the `github_events` table to a log file.

## Implementation Guide
1. Install `clickhouse-connect`.
2. Write `/home/user/ch-task/ingest.py`.
3. Execute the script.
4. Write the row count to `/home/user/ch-task/output.log`.

## Constraints
- Project path: /home/user/ch-task
- Log file: /home/user/ch-task/output.log
- Use `clickhouse-connect` for all database interactions.
- The table must be named `github_events`.

## Integrations
- None