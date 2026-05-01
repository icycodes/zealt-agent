const express = require('express');
const { createClient } = require('@clickhouse/client');

const app = express();
const port = 3000;

// ClickHouse client configuration
const client = createClient({
  host: process.env.CLICKHOUSE_HOST,
  username: 'default',
  password: process.env.CLICKHOUSE_PASSWORD,
});

app.get('/tables', async (req, res) => {
  try {
    const resultSet = await client.query({
      query: 'SELECT name FROM system.tables LIMIT 5',
      format: 'JSONEachRow',
    });
    const dataset = await resultSet.json();
    
    // Extract names and return as JSON array
    const tableNames = dataset.map(row => row.name);
    res.json(tableNames);
  } catch (error) {
    console.error('Error querying ClickHouse:', error);
    res.status(500).json({ error: 'Failed to query system tables' });
  }
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
