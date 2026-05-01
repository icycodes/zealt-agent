'use strict';

const express = require('express');
const { createClient } = require('@clickhouse/client');

const app = express();
const PORT = 3000;

// Validate required environment variables
const CLICKHOUSE_HOST = process.env.CLICKHOUSE_HOST;
const CLICKHOUSE_PASSWORD = process.env.CLICKHOUSE_PASSWORD;

if (!CLICKHOUSE_HOST) {
  console.error('ERROR: CLICKHOUSE_HOST environment variable is required (e.g. https://<hostname>:8443)');
  process.exit(1);
}

if (!CLICKHOUSE_PASSWORD) {
  console.error('ERROR: CLICKHOUSE_PASSWORD environment variable is required');
  process.exit(1);
}

// Initialize ClickHouse client
const client = createClient({
  host: CLICKHOUSE_HOST,
  username: 'default',
  password: CLICKHOUSE_PASSWORD,
});

// GET /tables — query system.tables and return results as JSON array
app.get('/tables', async (req, res) => {
  try {
    const resultSet = await client.query({
      query: 'SELECT name FROM system.tables LIMIT 5',
      format: 'JSONEachRow',
    });

    const rows = await resultSet.json();

    res.json(rows);
  } catch (err) {
    console.error('ClickHouse query error:', err.message);
    res.status(500).json({
      error: 'Failed to query ClickHouse',
      details: err.message,
    });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
  console.log(`ClickHouse host: ${CLICKHOUSE_HOST}`);
});
