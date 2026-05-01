# ClickHouse Cloud Schema Migration

## Background
You need to manage schema changes for a ClickHouse Cloud database using the official Python SDK (`clickhouse-connect`). Your task is to write a Python script that ensures the `users` table exists and has the correct schema, applying an `ALTER TABLE` to add a missing column if necessary.

## Requirements
- Write a Python script `migrate.py` in the project directory.
- The script must connect to ClickHouse Cloud using the following environment variables: `CLICKHOUSE_HOST`, `CLICKHOUSE_PORT` (default 8443), `CLICKHOUSE_USER` (default 'default'), and `CLICKHOUSE_PASSWORD`.
- Ensure a table named `users` exists. If it doesn't, create it with the following schema: `id UInt64, username String`, using the `MergeTree` engine ordered by `id`.
- Ensure the `users` table has a `last_login` column of type `DateTime`. If it doesn't exist, use `ALTER TABLE` to add it.
- Log the actions taken (e.g., 'Table created', 'Column added') to `migration.log`.

## Implementation Guide
1. Read the connection details from environment variables.
2. Connect using `clickhouse_connect.get_client(host=..., port=..., username=..., password=..., secure=True)`.
3. Execute `CREATE TABLE IF NOT EXISTS users (id UInt64, username String) ENGINE = MergeTree ORDER BY id`.
4. Execute `ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login DateTime`.
5. Write a success message to `/home/user/ch-migration/migration.log`.

## Constraints
- Project path: `/home/user/ch-migration`
- Log file: `/home/user/ch-migration/migration.log`
- The script must be idempotent (safe to run multiple times).

## Integrations
- None