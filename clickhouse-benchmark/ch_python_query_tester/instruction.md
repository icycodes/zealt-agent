# ClickHouse Python Query Benchmark

## Background
You need to benchmark query performance on a ClickHouse database using the official Python SDK `clickhouse-connect`.

## Requirements
- Initialize a Python project in `/home/user/ch_benchmark`.
- Install the `clickhouse-connect` library.
- Write a Python script `benchmark.py` that connects to a ClickHouse database using the following environment variables:
  - `CH_HOST` (e.g., localhost)
  - `CH_PORT` (e.g., 8123)
  - `CH_USER` (e.g., default)
  - `CH_PASSWORD` (e.g., empty string)
  - `CH_SECURE` (e.g., 'True' or 'False', parse to boolean)
- The script must perform the following operations sequentially:
  1. Create a table `events` (`id UInt64`, `event_type String`, `timestamp DateTime`) `ENGINE = MergeTree ORDER BY id`.
  2. Insert exactly 1000 rows into the `events` table (e.g., `id` from 1 to 1000, `event_type` as 'click', 'view', or 'purchase', and `timestamp` as the current time).
  3. Execute the query `SELECT event_type, count() FROM events GROUP BY event_type`.
  4. Record the query execution time (in seconds).
  5. Write the output to `/home/user/ch_benchmark/output.json` in exactly this JSON format: `{"time_seconds": 0.05, "results": [["click", 330], ["view", 340], ["purchase", 330]]}`.
- Run the script and ensure `output.json` is generated.

## Constraints
- Project path: `/home/user/ch_benchmark`
- Log file: `/home/user/ch_benchmark/output.log`
- The database connection must use the environment variables as specified. Do not hardcode credentials.
