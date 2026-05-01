import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/ch-task"
LOG_FILE = os.path.join(PROJECT_DIR, "output.log")

def test_github_events_table_exists():
    result = subprocess.run(
        ["clickhouse-client", "--query", "EXISTS TABLE github_events"],
        capture_output=True,
        text=True,
        check=False
    )
    assert result.returncode == 0, "Failed to query clickhouse server."
    assert result.stdout.strip() == "1", "The github_events table does not exist."

def test_github_events_has_data():
    result = subprocess.run(
        ["clickhouse-client", "--query", "SELECT count() FROM github_events"],
        capture_output=True,
        text=True,
        check=False
    )
    assert result.returncode == 0, "Failed to query github_events count."
    count = int(result.stdout.strip())
    assert count > 0, "The github_events table is empty."

def test_output_log_exists_and_matches():
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} does not exist."
    with open(LOG_FILE, "r") as f:
        log_content = f.read().strip()
    
    result = subprocess.run(
        ["clickhouse-client", "--query", "SELECT count() FROM github_events"],
        capture_output=True,
        text=True,
        check=False
    )
    db_count = result.stdout.strip()
    assert log_content == db_count, f"Log file content ({log_content}) does not match db count ({db_count})."
