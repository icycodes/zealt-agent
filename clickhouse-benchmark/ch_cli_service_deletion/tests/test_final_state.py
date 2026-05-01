import os
import pytest

SCRIPT_PATH = "/home/user/delete_service.sh"

def test_script_exists_and_executable():
    """Priority 3 fallback: basic file existence and permission check."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_contains_list_command():
    """Priority 3 fallback: check script content for list command."""
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
    assert "clickhousectl cloud service list" in content, \
        "Expected 'clickhousectl cloud service list' in the script."

def test_script_contains_delete_command():
    """Priority 3 fallback: check script content for delete command."""
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
    assert "clickhousectl cloud service delete" in content, \
        "Expected 'clickhousectl cloud service delete' in the script."