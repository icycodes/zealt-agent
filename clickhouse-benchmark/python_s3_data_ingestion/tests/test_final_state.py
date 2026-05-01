import os
import subprocess
import pytest
import clickhouse_connect

def test_script_exists():
    script_path = "/home/user/ingest.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_script_execution():
    result = subprocess.run(["python3", "/home/user/ingest.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed: {result.stderr}"

def test_table_exists_and_populated():
    host = os.environ.get('CLICKHOUSE_HOST')
    port = int(os.environ.get('CLICKHOUSE_PORT', '8443'))
    user = os.environ.get('CLICKHOUSE_USER', 'default')
    password = os.environ.get('CLICKHOUSE_PASSWORD')
    
    assert host and password, "CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD must be set in the environment."
    
    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password,
        secure=True
    )
    
    # Check if table exists
    tables = client.command("EXISTS TABLE aapl_stock")
    assert tables == 1, "Table 'aapl_stock' does not exist."
    
    # Check row count
    count = client.command("SELECT count() FROM aapl_stock")
    assert count > 0, "Table 'aapl_stock' is empty. Expected data to be inserted from S3."
    
    # Check schema
    schema = client.query("DESCRIBE TABLE aapl_stock").result_rows
    columns = {row[0]: row[1] for row in schema}
    
    expected_columns = {
        'Date': 'Date',
        'Open': 'Float64',
        'High': 'Float64',
        'Low': 'Float64',
        'Close': 'Float64',
        'Volume': 'UInt64',
        'OpenInt': 'UInt64'
    }
    
    for col, data_type in expected_columns.items():
        assert col in columns, f"Column {col} is missing from the table."
        assert columns[col] == data_type, f"Column {col} has wrong type. Expected {data_type}, got {columns[col]}."
