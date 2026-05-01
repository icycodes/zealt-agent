# Bulk Load CSV to ClickHouse Cloud via Node.js

## Background
You need to build a Node.js script that connects to a ClickHouse Cloud instance, creates a table, and bulk loads data from a CSV file using the official `@clickhouse/client` SDK.

## Requirements
- Initialize a Node.js project in `/home/user/ch-task`.
- Install the `@clickhouse/client` package.
- Write a script `index.js` that:
  1. Connects to ClickHouse Cloud using the `CLICKHOUSE_HOST` and `CLICKHOUSE_PASSWORD` environment variables. The host URL must use HTTPS and port 8443 (e.g., `https://${process.env.CLICKHOUSE_HOST}:8443`). Use `default` as the username.
  2. Creates a table named `employees` (if it doesn't exist) with the following schema: `id UInt32`, `name String`, `department String`, `salary Float64`. Use the `MergeTree` engine ordered by `id`.
  3. Reads the file `/home/user/ch-task/employees.csv` as a stream and inserts it into the `employees` table using the `CSVWithNames` format.
  4. Writes the text `Success` to `/home/user/ch-task/output.log` upon completion.
- Execute your script so the data is loaded.

## Constraints
- Project path: `/home/user/ch-task`
- Log file: `/home/user/ch-task/output.log`
- The script must handle the CSV header properly (using `CSVWithNames`).