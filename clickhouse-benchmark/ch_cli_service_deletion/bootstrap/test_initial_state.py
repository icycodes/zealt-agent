import os
import shutil

def test_project_dir_exists():
    assert os.path.isdir("/home/user"), "/home/user directory does not exist."

def test_clickhousectl_binary_available():
    assert shutil.which("clickhousectl") is not None, "clickhousectl binary not found in PATH."