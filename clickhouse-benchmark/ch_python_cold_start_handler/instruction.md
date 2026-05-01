# ClickHouse Cloud Python Cold Start Handler

## Background
ClickHouse Cloud services may "pause" when idle. The first request after a pause may experience higher latency (a cold start). To handle this gracefully, applications must configure their database clients with increased timeouts.

## Requirements
- Create a Python script `/home/user/ch-project/query.py` that connects to a ClickHouse server and executes a simple query: `SELECT 1`.
- You must use the official `clickhouse-connect` library.
- The client must be configured to handle potential cold starts by setting `connect_timeout` to 30 seconds and `send_receive_timeout` to 120 seconds.
- The script should print the result of the query to the standard output.

## Implementation Guide
1. Ensure `clickhouse-connect` is installed or install it if necessary.
2. Create the script at `/home/user/ch-project/query.py`.
3. In the script, read the connection details from the environment variables: `CH_HOST`, `CH_PORT`, `CH_USER`, and `CH_PASSWORD`.
4. Initialize the `clickhouse_connect` client with these credentials and the required timeout settings (`connect_timeout=30`, `send_receive_timeout=120`).
5. Execute the query `SELECT 1` and print the result.

## Constraints
- Project path: /home/user/ch-project
- The script must use `clickhouse-connect`.
- The script must read credentials from environment variables.
- The script must configure `connect_timeout` and `send_receive_timeout` exactly as specified.