const express = require('express');
const { createClient } = require('@clickhouse/client');

const app = express();
const PORT = 3000;

// Get environment variables
const CLICKHOUSE_HOST = process.env.CLICKHOUSE_HOST;
const CLICKHOUSE_PASSWORD = process.env.CLICKHOUSE_PASSWORD;

// Validate required environment variables
if (!CLICKHOUSE_HOST) {
  console.error('Error: CLICKHOUSE_HOST environment variable is required');
  process.exit(1);
}

if (!CLICKHOUSE_PASSWORD) {
  console.error('Error: CLICKHOUSE_PASSWORD environment variable is required');
  process.exit(1);
}

// Create ClickHouse client
const clickhouseClient = createClient({
  host: CLICKHOUSE_HOST,
  username: 'default',
  password: CLICKHOUSE_PASSWORD,
});

// GET /tables endpoint
app.get('/tables', async (req, res) => {
  try {
    const resultSet = await clickhouseClient.query({
      query: 'SELECT name FROM system.tables LIMIT 5',
      format: 'JSON',
    });

    const result = await resultSet.json();
    
    // Extract the table names from the result
    const tableNames = result.data.map(row => row.name);
    
    res.json(tableNames);
  } catch (error) {
    console.error('Error querying ClickHouse:', error.message);
    res.status(500).json({ 
      error: 'Failed to query ClickHouse',
      message: error.message 
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`ClickHouse Host: ${CLICKHOUSE_HOST}`);
});

// Handle graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, closing server...');
  await clickhouseClient.close();
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('SIGINT received, closing server...');
  await clickhouseClient.close();
  process.exit(0);
});