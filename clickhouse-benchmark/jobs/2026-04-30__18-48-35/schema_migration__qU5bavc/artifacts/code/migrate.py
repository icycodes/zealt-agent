#!/usr/bin/env python3
"""
ClickHouse Schema Migration Script

This script reads SQL migration statements from migrations.sql and executes them
sequentially on a ClickHouse Cloud instance.
"""

import os
import sys
import clickhouse_connect


def get_env_var(name, default=None):
    """Get environment variable with optional default."""
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"Environment variable {name} is required and not set")
    return value


def main():
    """Main migration function."""
    # Get connection parameters from environment variables
    host = get_env_var('CLICKHOUSE_HOST')
    port = int(get_env_var('CLICKHOUSE_PORT', '8443'))
    username = get_env_var('CLICKHOUSE_USERNAME', 'default')
    password = get_env_var('CLICKHOUSE_PASSWORD')

    print(f"Connecting to ClickHouse Cloud at {host}:{port} as {username}...")

    # Connect to ClickHouse Cloud
    try:
        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=username,
            password=password,
            secure=True
        )
        print("Successfully connected to ClickHouse Cloud")
    except Exception as e:
        print(f"Failed to connect to ClickHouse Cloud: {e}")
        sys.exit(1)

    # Read migrations.sql file
    migrations_file = os.path.join(os.path.dirname(__file__), 'migrations.sql')
    try:
        with open(migrations_file, 'r') as f:
            sql_content = f.read()
        print(f"Successfully read {migrations_file}")
    except Exception as e:
        print(f"Failed to read {migrations_file}: {e}")
        sys.exit(1)

    # Split SQL statements by semicolon and filter empty statements
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]

    if not statements:
        print("No SQL statements found in migrations.sql")
        sys.exit(0)

    print(f"Found {len(statements)} SQL statement(s) to execute")

    # Execute each statement sequentially
    for i, statement in enumerate(statements, 1):
        print(f"\n[{i}/{len(statements)}] Executing: {statement[:100]}...")
        try:
            result = client.command(statement)
            print(f"  ✓ Statement executed successfully")
        except Exception as e:
            print(f"  ✗ Statement failed: {e}")
            sys.exit(1)

    print("\n✓ All migrations executed successfully")


if __name__ == '__main__':
    main()