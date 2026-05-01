# ClickHouse Schema Migration

## Background
Implement a simple Python script to perform schema migrations on ClickHouse Cloud using the official `clickhouse-connect` SDK.

## Requirements
- Write a Python script `migrate.py` that reads a `migrations.sql` file.
- The script must connect to ClickHouse Cloud using the following environment variables: `CLICKHOUSE_HOST`, `CLICKHOUSE_PORT` (default 8443), `CLICKHOUSE_USERNAME` (default 'default'), and `CLICKHOUSE_PASSWORD`.
- It should execute the SQL statements in the `migrations.sql` file sequentially.

## Implementation Guide
1. The project directory is `/home/user/myproject`.
2. The file `/home/user/myproject/migrations.sql` is already provided.
3. Install `clickhouse-connect`.
4. Create `migrate.py` that uses `clickhouse_connect.get_client(host=..., port=..., username=..., password=..., secure=True)`.
5. Read `migrations.sql`, split by `;`, and use `client.command()` to execute the DDL statements.
6. Run the script and redirect output to `output.log`.

## Constraints
- Project path: `/home/user/myproject`
- Log file: `/home/user/myproject/output.log`