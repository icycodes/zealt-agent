import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/ch-project"

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_clickhouse_connect_installed():
    try:
        import clickhouse_connect
    except ImportError:
        pytest.fail("clickhouse-connect is not installed.")
