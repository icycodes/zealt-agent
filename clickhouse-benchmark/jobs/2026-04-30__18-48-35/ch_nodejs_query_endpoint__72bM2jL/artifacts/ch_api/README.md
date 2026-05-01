# ClickHouse Cloud Node.js REST API

## Overview
A REST API built with Express.js and `@clickhouse/client` that connects to ClickHouse Cloud and exposes endpoints to query system tables.

## Project Structure
- `index.js` - Main server file with Express app and ClickHouse client
- `package.json` - Project dependencies and configuration
- `node_modules/` - Installed dependencies

## Setup

### Environment Variables
The following environment variables are required:

- `CLICKHOUSE_HOST` - Full URL to ClickHouse Cloud instance (e.g., `https://<hostname>:8443`)
- `CLICKHOUSE_PASSWORD` - Password for ClickHouse Cloud authentication

### Installation
```bash
cd /home/user/ch_api
npm install
```

### Running the Server
```bash
node index.js
```

The server will start on port 3000.

## Endpoints

### GET /tables
Queries the ClickHouse system.tables and returns the first 5 table names.

**Response:**
```json
["table1", "table2", "table3", "table4", "table5"]
```

**Query:**
```sql
SELECT name FROM system.tables LIMIT 5
```

### GET /health
Health check endpoint.

**Response:**
```json
{ "status": "ok" }
```

## Error Handling
- Validates required environment variables on startup
- Handles ClickHouse connection errors gracefully
- Returns 500 status with error details on query failures
- Implements graceful shutdown on SIGTERM/SIGINT

## Dependencies
- `express` - Web framework
- `@clickhouse/client` - ClickHouse client library

## Configuration
- Port: 3000
- Username: `default` (hardcoded)
- Host and Password: Configured via environment variables