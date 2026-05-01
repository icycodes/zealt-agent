import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/ch_benchmark"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_clickhouse_client_available():
    assert shutil.which("clickhouse-client") is not None, "clickhouse-client binary not found in PATH."
