import shutil

def test_python3_available():
    assert shutil.which("python3") is not None, "python3 binary not found in PATH."

def test_pip3_available():
    assert shutil.which("pip3") is not None, "pip3 binary not found in PATH."
