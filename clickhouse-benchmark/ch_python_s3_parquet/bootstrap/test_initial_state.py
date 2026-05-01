import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_clickhouse_connect_installed():
    result = subprocess.run(
        ["python3", "-c", "import clickhouse_connect"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"clickhouse_connect package is not installed: {result.stderr}"
