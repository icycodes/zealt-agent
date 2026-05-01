import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/ch_benchmark"
OUTPUT_FILE = os.path.join(PROJECT_DIR, "output.json")

def test_events_table_row_count_via_cli():
    """Priority 1: Use ClickHouse CLI to verify the table exists and has 1000 rows."""
    result = subprocess.run(
        ["clickhouse-client", "-q", "SELECT count() FROM events"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"'clickhouse-client' query failed: {result.stderr}"
    count = result.stdout.strip()
    assert count == "1000", f"Expected 1000 rows in 'events' table, got: {count}"

def test_output_json_exists_and_valid():
    """Priority 3 fallback: Verify the output.json file content."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"
    
    with open(OUTPUT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {OUTPUT_FILE} as JSON: {e}")
            
    assert "time_seconds" in data, "Expected 'time_seconds' key in output.json"
    assert isinstance(data["time_seconds"], (int, float)), "'time_seconds' should be a number"
    
    assert "results" in data, "Expected 'results' key in output.json"
    assert isinstance(data["results"], list), "'results' should be a list"
    assert len(data["results"]) > 0, "'results' list should not be empty"
