# Node.js Streaming Query Execution

## Background
The Node.js `@clickhouse/client` SDK is commonly used to build backend APIs that stream analytical data efficiently using formats like `JSONEachRow`.

## Requirements
You need to create a Node.js script (`query.js`) that connects to ClickHouse Cloud, queries the `system.tables` table, and streams the results to standard output in JSON format.

## Implementation
1. Initialize a Node.js project in `/home/user/myproject`.
2. Install `@clickhouse/client`.
3. Create `query.js`.
4. Connect to ClickHouse Cloud using the provided credentials from environment variables (`CLICKHOUSE_HOST`, `CLICKHOUSE_USER`, `CLICKHOUSE_PASSWORD`).
5. Query `system.tables` using `format: 'JSONEachRow'`.
6. Process the streaming response properly and log the fully parsed JSON array to the console.
7. Run the script and redirect the output to `/home/user/myproject/output.log`.

## Constraints
- Project path: `/home/user/myproject`
- Log file: `/home/user/myproject/output.log`
- You must establish the connection over HTTPS using port `8443`.
- The query execution method must specify `format: 'JSONEachRow'`.