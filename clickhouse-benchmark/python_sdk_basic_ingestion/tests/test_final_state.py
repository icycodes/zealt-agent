import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/ch_project"

def test_script_exists():
    script_path = os.path.join(PROJECT_DIR, "ingest.py")
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_log_exists_and_contains_3():
    log_path = os.path.join(PROJECT_DIR, "output.log")
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
    assert "3" in content, "Log file does not contain the expected row count '3'."

def test_database_state():
    # Install clickhouse-connect if not already installed by the user
    # (The user was supposed to install it, but we can verify it's available)
    try:
        import clickhouse_connect
    except ImportError:
        pytest.fail("clickhouse-connect is not installed in the environment.")

    host = os.environ.get("CLICKHOUSE_HOST")
    port = os.environ.get("CLICKHOUSE_PORT", "8443")
    user = os.environ.get("CLICKHOUSE_USER", "default")
    password = os.environ.get("CLICKHOUSE_PASSWORD")

    if not host or not password:
        pytest.skip("CLICKHOUSE_HOST or CLICKHOUSE_PASSWORD environment variables not set. Skipping database verification.")

    client = clickhouse_connect.get_client(
        host=host,
        port=int(port),
        username=user,
        password=password,
        secure=True
    )

    try:
        result = client.query("SELECT count() FROM test_events")
        count = result.result_rows[0][0]
        assert count >= 3, f"Expected at least 3 rows in test_events, found {count}."
        
        # Verify specific data
        data_result = client.query("SELECT id, event_type FROM test_events ORDER BY id LIMIT 3")
        rows = data_result.result_rows
        assert len(rows) == 3, "Expected 3 rows in the query result."
        assert rows[0] == (1, 'push'), f"Unexpected row 1: {rows[0]}"
        assert rows[1] == (2, 'pull_request'), f"Unexpected row 2: {rows[1]}"
        assert rows[2] == (3, 'issue'), f"Unexpected row 3: {rows[2]}"
    except Exception as e:
        pytest.fail(f"Failed to query database: {e}")
