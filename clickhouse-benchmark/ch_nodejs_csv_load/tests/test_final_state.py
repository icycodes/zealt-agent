import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/ch-task"

def test_output_log_success():
    """Priority 3 fallback: basic file existence and content check."""
    log_path = os.path.join(PROJECT_DIR, "output.log")
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    with open(log_path) as f:
        content = f.read()
    assert "Success" in content, f"Expected 'Success' in output.log, got: {content}"

def test_clickhouse_table_row_count():
    """Priority 1: Use HTTP API to verify the state in ClickHouse Cloud."""
    host = os.environ.get("CLICKHOUSE_HOST")
    password = os.environ.get("CLICKHOUSE_PASSWORD")
    
    assert host is not None, "CLICKHOUSE_HOST environment variable not set."
    assert password is not None, "CLICKHOUSE_PASSWORD environment variable not set."
    
    url = f"https://{host}:8443/?query=SELECT+count()+FROM+employees+FORMAT+CSV"
    
    result = subprocess.run(
        ["curl", "-s", "-S", "-u", f"default:{password}", url],
        capture_output=True, text=True
    )
    
    assert result.returncode == 0, f"curl request failed: {result.stderr}"
    assert result.stdout.strip() == "5", f"Expected count of 5 in employees table, got: {result.stdout}"
