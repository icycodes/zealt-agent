# Configure ClickHouse for Grafana using Node.js

## Background
You need to prepare a ClickHouse database for Grafana to use as a data source. You will write a Node.js script that uses the `@clickhouse/client` SDK to set up the schema and a dedicated read-only user.

## Requirements
- Write a script named `setup_grafana.js` in `/home/user/project`.
- The script must connect to ClickHouse at `http://localhost:8123` using the default user (no password).
- It must create a database named `grafana_db`.
- It must create a table `grafana_db.metrics` with columns: `timestamp` (DateTime), `metric_name` (String), and `value` (Float64). The engine must be `MergeTree` ordered by `(metric_name, timestamp)`.
- It must create a user `grafana_user` with password `grafana_pass`.
- It must grant `SELECT` privilege on `grafana_db.metrics` to `grafana_user`.
- The script should execute these commands sequentially and exit successfully.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/project` and install `@clickhouse/client`.
2. Write `setup_grafana.js`.
3. Use `client.command()` to execute the DDL statements.
4. Ensure you await all operations.

## Constraints
- Project path: `/home/user/project`
- The ClickHouse server is already running locally on port 8123.

## Integrations
- None