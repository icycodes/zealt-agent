const express = require('express');
const { createClient } = require('@clickhouse/client');

// Initialize Express app
const app = express();

// Get environment variables
const clickhouseUrl = process.env.CLICKHOUSE_URL;
const clickhouseUser = process.env.CLICKHOUSE_USER;
const clickhousePassword = process.env.CLICKHOUSE_PASSWORD;

// Validate required environment variables
if (!clickhouseUrl || !clickhouseUser || !clickhousePassword) {
  console.error('Error: Missing required environment variables');
  console.error('Required: CLICKHOUSE_URL, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD');
  process.exit(1);
}

// Create ClickHouse client
const client = createClient({
  url: clickhouseUrl,
  username: clickhouseUser,
  password: clickhousePassword,
});

// Test connection on startup
(async () => {
  try {
    await client.ping();
    console.log('Successfully connected to ClickHouse');
  } catch (error) {
    console.error('Failed to connect to ClickHouse:', error.message);
  }
})();

// GET /metrics endpoint
app.get('/metrics', async (req, res) => {
  try {
    // Query ClickHouse for total parts count
    const result = await client.query({
      query: 'SELECT count() AS total_parts FROM system.parts',
      format: 'JSONEachRow',
    });

    // Parse the result
    const rows = await result.json();
    const totalParts = rows[0]?.total_parts || 0;

    // Return the result as JSON
    res.json({ total_parts: totalParts });
  } catch (error) {
    console.error('Error querying ClickHouse:', error);
    res.status(500).json({ error: 'Failed to query database' });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Start server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Analytics API server running on port ${PORT}`);
});