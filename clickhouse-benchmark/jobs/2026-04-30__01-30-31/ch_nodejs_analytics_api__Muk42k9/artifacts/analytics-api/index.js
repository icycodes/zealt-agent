const express = require('express');
const { createClient } = require('@clickhouse/client');

const app = express();
const PORT = 3000;

// Create ClickHouse client using environment variables.
// CLICKHOUSE_URL should include the full protocol and port,
// e.g. https://your-host.clickhouse.cloud:8443 (Cloud/TLS)
// or   http://localhost:8123 (local)
const client = createClient({
  url: process.env.CLICKHOUSE_URL,
  username: process.env.CLICKHOUSE_USER,
  password: process.env.CLICKHOUSE_PASSWORD,
});

// GET /metrics
// Queries ClickHouse for the total number of active data parts and returns
// the result as JSON: { "total_parts": <number> }
app.get('/metrics', async (req, res) => {
  try {
    const resultSet = await client.query({
      query: 'SELECT count() AS total_parts FROM system.parts',
      format: 'JSONEachRow',
    });

    const rows = await resultSet.json();

    // rows is an array; the single row contains the aggregated count.
    const totalParts = Number(rows[0].total_parts);

    return res.json({ total_parts: totalParts });
  } catch (err) {
    console.error('ClickHouse query failed:', err);
    return res.status(500).json({ error: 'Database query failed' });
  }
});

app.listen(PORT, () => {
  console.log(`Analytics API listening on port ${PORT}`);
});
