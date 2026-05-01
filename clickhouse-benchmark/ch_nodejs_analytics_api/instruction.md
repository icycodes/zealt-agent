# ClickHouse Cloud Analytics API

## Background
You need to build a real-time analytics backend for a dashboard using Node.js, Express, and ClickHouse Cloud.

## Requirements
- Initialize a Node.js project in `/home/user/analytics-api`.
- Install `express` and the official `@clickhouse/client` SDK.
- Create an `index.js` file that starts an Express server on port 3000.
- Connect to ClickHouse Cloud using the following environment variables:
  - `CLICKHOUSE_URL` (e.g. `https://your-host.clickhouse.cloud:8443` or `http://localhost:8123`)
  - `CLICKHOUSE_USER`
  - `CLICKHOUSE_PASSWORD`
- Note: ClickHouse Cloud strictly requires TLS/HTTPS for connections, so your code should use the URL provided in `CLICKHOUSE_URL` which will include the correct protocol.
- Implement a GET `/metrics` endpoint that queries ClickHouse for `SELECT count() AS total_parts FROM system.parts` and returns the result as JSON in the format `{"total_parts": <number>}`.
- Ensure proper error handling and return a 500 status code if the database query fails.

## Constraints
- Project path: `/home/user/analytics-api`
- Start command: `node index.js`
- Port: 3000
