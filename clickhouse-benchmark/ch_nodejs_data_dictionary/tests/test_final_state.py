import os
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user/ch_project"
EXTRACT_SCRIPT = os.path.join(PROJECT_DIR, "extract_dict.js")
DICTIONARY_FILE = os.path.join(PROJECT_DIR, "dictionary.json")

def test_nodejs_project_initialized():
    """Verify that package.json exists."""
    pkg_json = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg_json), f"package.json not found at {pkg_json}"

def test_clickhouse_client_installed():
    """Verify that @clickhouse/client is in dependencies."""
    pkg_json = os.path.join(PROJECT_DIR, "package.json")
    with open(pkg_json) as f:
        data = json.load(f)
    deps = data.get("dependencies", {})
    assert "@clickhouse/client" in deps, "@clickhouse/client not found in package.json dependencies"

def test_extract_script_exists():
    """Verify that extract_dict.js exists."""
    assert os.path.isfile(EXTRACT_SCRIPT), f"extract_dict.js not found at {EXTRACT_SCRIPT}"

def test_dictionary_file_exists():
    """Verify that dictionary.json exists."""
    assert os.path.isfile(DICTIONARY_FILE), f"dictionary.json not found at {DICTIONARY_FILE}"

def test_dictionary_content():
    """Verify the structure of dictionary.json."""
    with open(DICTIONARY_FILE) as f:
        data = json.load(f)
    
    assert isinstance(data, list), "Expected dictionary.json to contain a JSON array"
    assert len(data) > 0, "dictionary.json array is empty"
    
    # Check fields in the first item
    first_item = data[0]
    assert "database" in first_item, "Missing 'database' field in dictionary item"
    assert "table" in first_item, "Missing 'table' field in dictionary item"
    assert "name" in first_item, "Missing 'name' (column name) field in dictionary item"
    assert "type" in first_item, "Missing 'type' (column type) field in dictionary item"
    
    # Verify at least one entry matches system.columns
    found_system_columns = False
    for item in data:
        if item.get("database") == "system" and item.get("table") == "columns":
            found_system_columns = True
            break
            
    assert found_system_columns, "Could not find any entry with database='system' and table='columns' in dictionary.json"
