import os
import shutil
import pytest

PROJECT_DIR = "/home/user/ch-task"

def test_node_binary_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_csv_file_exists():
    csv_path = os.path.join(PROJECT_DIR, "employees.csv")
    assert os.path.isfile(csv_path), f"CSV file {csv_path} does not exist."
    with open(csv_path) as f:
        content = f.read()
    assert "id,name,department,salary" in content, "Expected header in employees.csv."
    assert len(content.strip().split("\n")) == 6, "Expected 1 header row and 5 data rows in employees.csv."
