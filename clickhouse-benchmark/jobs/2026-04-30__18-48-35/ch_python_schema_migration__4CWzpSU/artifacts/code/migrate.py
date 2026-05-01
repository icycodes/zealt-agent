#!/usr/bin/env python3
"""
ClickHouse Cloud Schema Migration Script

This script ensures the 'users' table exists with the correct schema
and adds the 'last_login' column if missing.
"""

import os
import logging
import clickhouse_connect
from datetime import datetime

# Configure logging
log_file = '/home/user/ch-migration/migration.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def get_connection_details():
    """Read connection details from environment variables."""
    host = os.getenv('CLICKHOUSE_HOST')
    port = int(os.getenv('CLICKHOUSE_PORT', '8443'))
    username = os.getenv('CLICKHOUSE_USER', 'default')
    password = os.getenv('CLICKHOUSE_PASSWORD')

    if not host:
        raise ValueError("CLICKHOUSE_HOST environment variable is required")
    if not password:
        raise ValueError("CLICKHOUSE_PASSWORD environment variable is required")

    return {
        'host': host,
        'port': port,
        'username': username,
        'password': password
    }


def connect_to_clickhouse():
    """Connect to ClickHouse Cloud and return the client."""
    details = get_connection_details()
    logger.info(f"Connecting to ClickHouse at {details['host']}:{details['port']}")
    
    client = clickhouse_connect.get_client(
        host=details['host'],
        port=details['port'],
        username=details['username'],
        password=details['password'],
        secure=True
    )
    
    logger.info("Successfully connected to ClickHouse Cloud")
    return client


def ensure_users_table(client):
    """Ensure the users table exists with the correct schema."""
    logger.info("Checking if 'users' table exists...")
    
    # Check if table exists
    result = client.query(
        "EXISTS TABLE users"
    )
    table_exists = result.result_rows[0][0] if result.result_rows else False
    
    if not table_exists:
        logger.info("Table 'users' does not exist, creating...")
        client.command(
            "CREATE TABLE users (id UInt64, username String) ENGINE = MergeTree ORDER BY id"
        )
        logger.info("Table created")
        return "Table created"
    else:
        logger.info("Table 'users' already exists")
        return "Table already exists"


def ensure_last_login_column(client):
    """Ensure the last_login column exists in the users table."""
    logger.info("Checking if 'last_login' column exists...")
    
    # Check if column exists
    result = client.query(
        "SELECT name FROM system.columns WHERE table = 'users' AND database = currentDatabase()"
    )
    existing_columns = [row[0] for row in result.result_rows]
    column_exists = 'last_login' in existing_columns
    
    if not column_exists:
        logger.info("Column 'last_login' does not exist, adding...")
        client.command(
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login DateTime"
        )
        logger.info("Column added")
        return "Column added"
    else:
        logger.info("Column 'last_login' already exists")
        return "Column already exists"


def main():
    """Main migration function."""
    logger.info("Starting ClickHouse schema migration...")
    
    try:
        # Connect to ClickHouse
        client = connect_to_clickhouse()
        
        # Ensure table exists
        ensure_users_table(client)
        
        # Ensure column exists
        ensure_last_login_column(client)
        
        # Write success message
        success_message = f"Migration completed successfully at {datetime.utcnow().isoformat()}"
        logger.info(success_message)
        
        # Also write to migration.log directly
        with open(log_file, 'a') as f:
            f.write(f"{success_message}\n")
        
        logger.info("Migration finished successfully")
        return 0
        
    except Exception as e:
        error_message = f"Migration failed: {str(e)}"
        logger.error(error_message)
        
        # Write error to migration.log directly
        with open(log_file, 'a') as f:
            f.write(f"{error_message}\n")
        
        return 1


if __name__ == "__main__":
    exit(main())