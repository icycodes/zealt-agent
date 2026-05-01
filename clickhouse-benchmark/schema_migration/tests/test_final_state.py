import os
import subprocess
import json
import pytest

def test_table_exists_and_altered():
    host = os.environ.get("CLICKHOUSE_HOST")
    password = os.environ.get("CLICKHOUSE_PASSWORD")
    user = os.environ.get("CLICKHOUSE_USERNAME", "default")
    
    assert host and password, "CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD must be set."
    
    url = f"https://{host}:8443/"
    query = "DESCRIBE TABLE test_migration FORMAT JSON"
    result = subprocess.run(
        ["curl", "-s", "-u", f"{user}:{password}", "-d", query, url],
        capture_output=True, text=True
    )
    
    assert result.returncode == 0, f"Curl command failed: {result.stderr}"
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse JSON response: {result.stdout}")
        
    assert "data" in data, f"Unexpected response format: {result.stdout}"
    
    columns = {row["name"]: row["type"] for row in data["data"]}
    
    assert "id" in columns, "Column 'id' not found in test_migration."
    assert columns["id"] == "UInt64", f"Expected 'id' to be UInt64, got {columns['id']}"
    
    assert "name" in columns, "Column 'name' not found in test_migration. Migration likely failed."
    assert columns["name"] == "Nullable(String)" or columns["name"] == "String", f"Expected 'name' to be String or Nullable(String), got {columns['name']}"

def test_script_execution_log():
    log_path = "/home/user/myproject/output.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did the script redirect output?"
