import os
import json
import pytest

PROJECT_DIR = "/home/user/myproject"
QUERY_JS = os.path.join(PROJECT_DIR, "query.js")
PACKAGE_JSON = os.path.join(PROJECT_DIR, "package.json")
OUTPUT_LOG = os.path.join(PROJECT_DIR, "output.log")

def test_query_js_exists():
    assert os.path.isfile(QUERY_JS), f"{QUERY_JS} does not exist."

def test_package_json_has_clickhouse_client():
    assert os.path.isfile(PACKAGE_JSON), f"{PACKAGE_JSON} does not exist."
    with open(PACKAGE_JSON, "r") as f:
        pkg = json.load(f)
    
    deps = pkg.get("dependencies", {})
    assert "@clickhouse/client" in deps, "@clickhouse/client is not in package.json dependencies."

def test_output_log_exists():
    assert os.path.isfile(OUTPUT_LOG), f"{OUTPUT_LOG} does not exist."

def test_output_log_is_valid_json_array():
    with open(OUTPUT_LOG, "r") as f:
        content = f.read().strip()
    
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse {OUTPUT_LOG} as JSON: {e}")
    
    assert isinstance(data, list), f"Expected the parsed JSON to be a list, got {type(data).__name__}."
    
    if len(data) > 0:
        first_row = data[0]
        assert isinstance(first_row, dict), "Expected elements of the JSON array to be objects."
        assert "database" in first_row or "name" in first_row, "Expected row objects to contain 'database' or 'name' fields."
