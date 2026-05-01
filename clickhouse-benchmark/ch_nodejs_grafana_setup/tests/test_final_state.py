import subprocess
import pytest

def test_database_exists():
    """Priority 1: Use clickhouse-client to verify database exists."""
    result = subprocess.run(
        ["clickhouse-client", "-q", "EXISTS DATABASE grafana_db"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"clickhouse-client failed: {result.stderr}"
    assert result.stdout.strip() == "1", "Database 'grafana_db' does not exist."

def test_table_exists():
    """Priority 1: Use clickhouse-client to verify table exists."""
    result = subprocess.run(
        ["clickhouse-client", "-q", "EXISTS TABLE grafana_db.metrics"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"clickhouse-client failed: {result.stderr}"
    assert result.stdout.strip() == "1", "Table 'grafana_db.metrics' does not exist."

def test_user_can_query():
    """Priority 1: Use clickhouse-client to verify the new user can query the table."""
    result = subprocess.run(
        ["clickhouse-client", "--user", "grafana_user", "--password", "grafana_pass", "-q", "SELECT count() FROM grafana_db.metrics"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to query table as grafana_user: {result.stderr}"
    assert result.stdout.strip() == "0", f"Expected count 0, got: {result.stdout.strip()}"
