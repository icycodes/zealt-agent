import os
import subprocess
import pytest
import clickhouse_connect

PROJECT_DIR = "/home/user/ch-migration"
MIGRATE_SCRIPT = os.path.join(PROJECT_DIR, "migrate.py")
LOG_FILE = os.path.join(PROJECT_DIR, "migration.log")

def test_migrate_script_exists():
    assert os.path.isfile(MIGRATE_SCRIPT), f"migrate.py not found at {MIGRATE_SCRIPT}"

def test_migrate_script_runs_successfully():
    result = subprocess.run(
        ["python3", "migrate.py"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"migrate.py failed with error: {result.stderr}"

def test_migration_log_exists():
    assert os.path.isfile(LOG_FILE), f"migration.log not found at {LOG_FILE}"

def test_users_table_schema_updated():
    host = os.environ.get("CLICKHOUSE_HOST")
    password = os.environ.get("CLICKHOUSE_PASSWORD")
    user = os.environ.get("CLICKHOUSE_USER", "default")
    port = int(os.environ.get("CLICKHOUSE_PORT", "8443"))

    assert host is not None, "CLICKHOUSE_HOST environment variable is not set."
    assert password is not None, "CLICKHOUSE_PASSWORD environment variable is not set."

    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password,
        secure=True
    )

    result = client.query("DESCRIBE TABLE users")
    columns = [row[0] for row in result.result_rows]
    types = {row[0]: row[1] for row in result.result_rows}

    assert "id" in columns, "Column 'id' missing from users table."
    assert "username" in columns, "Column 'username' missing from users table."
    assert "last_login" in columns, "Column 'last_login' missing from users table."

    assert types["id"] == "UInt64", f"Expected 'id' to be UInt64, got {types['id']}"
    assert types["username"] == "String", f"Expected 'username' to be String, got {types['username']}"
    assert types["last_login"] == "DateTime", f"Expected 'last_login' to be DateTime, got {types['last_login']}"