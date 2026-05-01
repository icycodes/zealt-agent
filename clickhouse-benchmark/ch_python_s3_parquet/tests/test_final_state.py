import os
import subprocess
import pytest

def test_amazon_reviews_table_and_data():
    host = os.environ.get("CH_HOST")
    port = os.environ.get("CH_PORT", "8443")
    user = os.environ.get("CH_USER", "default")
    password = os.environ.get("CH_PASSWORD", "")
    
    assert host, "CH_HOST environment variable is missing"
    
    python_script = f"""
import clickhouse_connect
import sys

client = clickhouse_connect.get_client(
    host='{host}',
    port={port},
    username='{user}',
    password='{password}',
    secure=True
)

res = client.query("EXISTS TABLE amazon_reviews")
if res.result_rows[0][0] != 1:
    print("Table 'amazon_reviews' does not exist")
    sys.exit(1)

schema = client.query("DESCRIBE TABLE amazon_reviews")
columns = {{row[0]: row[1] for row in schema.result_rows}}

if "review_id" not in columns or "String" not in columns["review_id"]:
    print("review_id column missing or invalid: " + str(columns.get('review_id')))
    sys.exit(1)

if "product_id" not in columns or "String" not in columns["product_id"]:
    print("product_id column missing or invalid: " + str(columns.get('product_id')))
    sys.exit(1)

if "star_rating" not in columns or "UInt8" not in columns["star_rating"]:
    print("star_rating column missing or invalid: " + str(columns.get('star_rating')))
    sys.exit(1)

count_res = client.query("SELECT count() FROM amazon_reviews")
count = count_res.result_rows[0][0]
if count != 10:
    print("Expected 10 rows, got " + str(count))
    sys.exit(1)

print("SUCCESS")
"""
    result = subprocess.run(
        ["python3", "-c", python_script],
        capture_output=True, text=True
    )
    
    assert result.returncode == 0, f"Verification script failed: {result.stdout} {result.stderr}"
    assert "SUCCESS" in result.stdout, "Verification script did not output SUCCESS."

def test_script_exists():
    assert os.path.isfile("/home/user/app/load_s3.py"), "The script /home/user/app/load_s3.py was not created."
