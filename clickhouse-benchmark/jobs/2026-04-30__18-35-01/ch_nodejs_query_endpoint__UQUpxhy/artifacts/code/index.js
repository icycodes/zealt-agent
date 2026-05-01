const express = require('express');
const { createClient } = require('@clickhouse/client');

const app = express();
const port = 3000;

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
    // Returning the results as a JSON array of objects (e.g., [{name: "table1"}, ...])
    res.json(dataset);
  } catch (error) {
    console.error('ClickHouse query error:', error);
    res.status(500).json({ error: 'Failed to query ClickHouse' });
  }
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
