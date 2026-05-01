const express = require('express');
const { createClient } = require('@clickhouse/client');

const app = express();
const port = 3000;

// Initialize ClickHouse client
// CLICKHOUSE_HOST is expected to be a full URL like https://<hostname>:8443
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
    
    // resultSet.json() returns an array of objects for JSONEachRow
    const dataset = await resultSet.json();
    res.json(dataset);
  } catch (error) {
    console.error('Error querying ClickHouse:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
