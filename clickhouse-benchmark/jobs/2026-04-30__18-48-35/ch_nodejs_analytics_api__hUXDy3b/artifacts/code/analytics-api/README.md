# ClickHouse Cloud Analytics API

A real-time analytics backend built with Node.js, Express, and ClickHouse Cloud.

## Setup

### Environment Variables

The following environment variables must be set:

- `CLICKHOUSE_URL`: ClickHouse Cloud URL (e.g., `https://your-host.clickhouse.cloud:8443` or `http://localhost:8123`)
- `CLICKHOUSE_USER`: ClickHouse username
- `CLICKHOUSE_PASSWORD`: ClickHouse password

### Installation

```bash
npm install
```

### Running the Server

```bash
node index.js
```

The server will start on port 3000.

## API Endpoints

### GET /metrics

Queries ClickHouse for the total number of parts in the system.

**Query:**
```sql
SELECT count() AS total_parts FROM system.parts
```

**Response:**
```json
{
  "total_parts": 12345
}
```

**Error Response (500):**
```json
{
  "error": "Failed to query database"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## Dependencies

- `express`: Web framework
- `@clickhouse/client`: Official ClickHouse client for Node.js

## Notes

- ClickHouse Cloud requires TLS/HTTPS for connections
- The URL provided in `CLICKHOUSE_URL` must include the correct protocol
- Error handling returns 500 status code on database query failures