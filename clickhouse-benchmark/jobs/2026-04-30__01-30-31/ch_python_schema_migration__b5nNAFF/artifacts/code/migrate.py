#!/usr/bin/env python3
"""
ClickHouse Cloud Schema Migration Script
Ensures the `users` table exists with the correct schema,
adding the `last_login` column if it is missing.
"""

import logging
import os
import sys

import clickhouse_connect

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------
LOG_FILE = "/home/user/ch-migration/migration.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Connection helpers
# ---------------------------------------------------------------------------

def get_connection_params() -> dict:
    """Read connection details from environment variables."""
    host = os.environ.get("CLICKHOUSE_HOST")
    if not host:
        raise EnvironmentError("CLICKHOUSE_HOST environment variable is not set.")

    return {
        "host": host,
        "port": int(os.environ.get("CLICKHOUSE_PORT", 8443)),
        "username": os.environ.get("CLICKHOUSE_USER", "default"),
        "password": os.environ.get("CLICKHOUSE_PASSWORD", ""),
        "secure": True,
    }


# ---------------------------------------------------------------------------
# Migration steps
# ---------------------------------------------------------------------------

def ensure_table_exists(client: clickhouse_connect.driver.Client) -> None:
    """Create the `users` table if it does not already exist."""
    ddl = """
    CREATE TABLE IF NOT EXISTS users (
        id       UInt64,
        username String
    )
    ENGINE = MergeTree
    ORDER BY id
    """
    client.command(ddl)
    logger.info("Table 'users' ensured (CREATE TABLE IF NOT EXISTS executed).")


def ensure_last_login_column(client: clickhouse_connect.driver.Client) -> None:
    """Add the `last_login DateTime` column to `users` if it does not exist."""
    alter = "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login DateTime"
    client.command(alter)
    logger.info("Column 'last_login' ensured (ALTER TABLE ADD COLUMN IF NOT EXISTS executed).")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    logger.info("Starting ClickHouse Cloud schema migration.")

    try:
        params = get_connection_params()
    except EnvironmentError as exc:
        logger.error("Configuration error: %s", exc)
        sys.exit(1)

    try:
        client = clickhouse_connect.get_client(**params)
        logger.info("Connected to ClickHouse Cloud at %s:%s.", params["host"], params["port"])
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to connect to ClickHouse Cloud: %s", exc)
        sys.exit(1)

    try:
        ensure_table_exists(client)
        ensure_last_login_column(client)
    except Exception as exc:  # noqa: BLE001
        logger.error("Migration failed: %s", exc)
        sys.exit(1)
    finally:
        client.close()

    logger.info("Migration completed successfully.")


if __name__ == "__main__":
    main()
