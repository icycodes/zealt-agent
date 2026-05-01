import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/ch-migration"

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_clickhouse_connect_installed():
    try:
        import clickhouse_connect
    except ImportError:
        pytest.fail("clickhouse-connect is not installed.")

def test_python3_installed():
    result = subprocess.run(["python3", "--version"], capture_output=True, text=True)
    assert result.returncode == 0, "python3 is not installed or not in PATH."