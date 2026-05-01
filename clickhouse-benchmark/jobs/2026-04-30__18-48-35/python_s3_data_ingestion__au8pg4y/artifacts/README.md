# S3 Data Ingestion with ClickHouse Python SDK

## Overview
This script demonstrates how to ingest data from a public S3 CSV file into ClickHouse Cloud using the official `clickhouse-connect` Python SDK.

## Files Created
- `/home/user/ingest.py` - Main ingestion script
- `/logs/artifacts/code/ingest.py` - Preserved copy of the script

## Requirements
- Python 3.x
- `clickhouse-connect` package
- Environment variables:
  - `CLICKHOUSE_HOST` - ClickHouse Cloud host
  - `CLICKHOUSE_PORT` - ClickHouse Cloud port
  - `CLICKHOUSE_USER` - Username
  - `CLICKHOUSE_PASSWORD` - Password

## Table Schema
The script creates a table named `aapl_stock` with the following schema:

| Column | Type | Description |
|--------|------|-------------|
| Date | Date | Stock date |
| Open | Float64 | Opening price |
| High | Float64 | Highest price |
| Low | Float64 | Lowest price |
| Close | Float64 | Closing price |
| Volume | UInt64 | Trading volume |
| OpenInt | UInt64 | Open interest |

**Engine:** MergeTree
**Order Key:** Date

## Data Source
- URL: `https://datasets-documentation.s3.eu-west-3.amazonaws.com/aapl_stock.csv`
- Format: CSVWithNames (CSV with header row)

## Usage

### Install Dependencies
```bash
pip install clickhouse-connect
```

### Set Environment Variables
```bash
export CLICKHOUSE_HOST="your-host.clickhouse.cloud"
export CLICKHOUSE_PORT="8443"
export CLICKHOUSE_USER="your-username"
export CLICKHOUSE_PASSWORD="your-password"
```

### Run the Script
```bash
python3 /home/user/ingest.py
```

## Implementation Details

1. **Connection**: Establishes a secure HTTPS connection to ClickHouse Cloud
2. **Table Creation**: Uses `CREATE TABLE IF NOT EXISTS` to avoid errors on re-runs
3. **Data Ingestion**: Uses ClickHouse's `s3()` table function to directly read from S3 without downloading
4. **Insert**: Performs an `INSERT INTO ... SELECT * FROM s3(...)` to load data efficiently

## Key Features
- Secure connection (`secure=True`)
- Idempotent table creation
- Direct S3-to-ClickHouse data transfer (no intermediate files)
- Error handling for missing environment variables
- Progress feedback via print statements