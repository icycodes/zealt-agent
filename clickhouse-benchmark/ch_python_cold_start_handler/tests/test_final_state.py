import os
import pytest

SCRIPT_FILE = "/home/user/ch-project/query.py"

def test_script_exists():
    """Priority 3: File existence check."""
    assert os.path.isfile(SCRIPT_FILE), f"query.py not found at {SCRIPT_FILE}"

def test_script_imports_clickhouse_connect():
    """Priority 3: Verify the script imports clickhouse_connect."""
    with open(SCRIPT_FILE) as f:
        content = f.read()
    assert "clickhouse_connect" in content, "The script must import or use clickhouse_connect."

def test_script_configures_timeouts():
    """Priority 3: Verify the script configures connect_timeout and send_receive_timeout."""
    with open(SCRIPT_FILE) as f:
        content = f.read()
    assert "connect_timeout=30" in content.replace(" ", ""), "The script must configure connect_timeout=30."
    assert "send_receive_timeout=120" in content.replace(" ", ""), "The script must configure send_receive_timeout=120."

def test_script_reads_env_vars():
    """Priority 3: Verify the script reads credentials from environment variables."""
    with open(SCRIPT_FILE) as f:
        content = f.read()
    assert "CH_HOST" in content, "The script must read CH_HOST from environment variables."
    assert "CH_PORT" in content, "The script must read CH_PORT from environment variables."
    assert "CH_USER" in content, "The script must read CH_USER from environment variables."
    assert "CH_PASSWORD" in content, "The script must read CH_PASSWORD from environment variables."
