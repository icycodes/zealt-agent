# ClickHouse Cloud Schema Migration

This script manages schema changes for a ClickHouse Cloud database, ensuring the `users` table exists with the correct schema.

## Requirements

- Python 3.7+
- `clickhouse-connect` package

Install dependencies:
```bash
pip install clickhouse-connect
```

## Environment Variables

The following environment variables must be set:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CLICKHOUSE_HOST` | Yes | - | ClickHouse Cloud host |
| `CLICKHOUSE_PORT` | No | 8443 | ClickHouse Cloud port |
| `CLICKHOUSE_USER` | No | default | ClickHouse username |
| `CLICKHOUSE_PASSWORD` | Yes | - | ClickHouse password |

## Usage

```bash
export CLICKHOUSE_HOST=your-host.clickhouse.cloud
export CLICKHOUSE_PASSWORD=your-password
python migrate.py
```

## Schema

The script ensures the `users` table has the following schema:

```sql
CREATE TABLE users (
    id UInt64,
    username String,
    last_login DateTime
) ENGINE = MergeTree ORDER BY id
```

## Idempotency

The script is idempotent and safe to run multiple times:

- `CREATE TABLE IF NOT EXISTS` ensures the table is only created once
- `ALTER TABLE ADD COLUMN IF NOT EXISTS` ensures the column is only added once
- Existing data is preserved

## Logging

All actions are logged to `migration.log`:
- Connection status
- Table creation events
- Column addition events
- Success/failure messages

## Exit Codes

- `0`: Migration completed successfully
- `1`: Migration failed (check logs for details)