# ClickHouse Cloud Node.js REST API

## Background
Create a REST API using Express and `@clickhouse/client` that connects to ClickHouse Cloud and exposes an endpoint to query system tables.

## Requirements
- Initialize a Node.js project in `/home/user/ch_api`.
- Install `express` and `@clickhouse/client`.
- Create a server that listens on port 3000.
- Connect to ClickHouse Cloud using environment variables: `CLICKHOUSE_HOST` (a full URL of the form `https://<hostname>:8443`) and `CLICKHOUSE_PASSWORD`. The username should default to `default`.
- Implement a `GET /tables` endpoint that queries `SELECT name FROM system.tables LIMIT 5` and returns the results as a JSON array.

## Implementation Guide
1. Create the project directory `/home/user/ch_api` and initialize it with `npm init -y`.
2. Install the required packages.
3. Create an `index.js` file with the Express server and ClickHouse client configuration.
4. Pass the value of `CLICKHOUSE_HOST` directly to the `@clickhouse/client` `host` option (it is already a full URL).
5. Start the server on port 3000.

## Constraints
- Project path: `/home/user/ch_api`
- Start command: `node index.js`
- Port: 3000
- MUST use environment variables `CLICKHOUSE_HOST` and `CLICKHOUSE_PASSWORD` for connection.
- The server should handle potential connection errors gracefully.