import os
import shutil
import pytest

PROJECT_DIR = "/home/user/ch-task"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_python_installed():
    assert shutil.which("python3") is not None, "python3 is not installed."
