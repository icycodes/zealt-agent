const express = require('express');
const { createClient } = require('@clickhouse/client');

const app = express();
const port = 3000;

const client = createClient({
  url: process.env.CLICKHOUSE_URL,
  username: process.env.CLICKHOUSE_USER,
  password: process.env.CLICKHOUSE_PASSWORD,
});

app.get('/metrics', async (req, res) => {
  try {
    const resultSet = await client.query({
      query: 'SELECT count() AS total_parts FROM system.parts',
      format: 'JSONEachRow',
    });
    
    const dataset = await resultSet.json();
    
    if (dataset && dataset.length > 0) {
      res.json({ total_parts: Number(dataset[0].total_parts) });
    } else {
      res.json({ total_parts: 0 });
    }
  } catch (error) {
    console.error('Error querying ClickHouse:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.listen(port, () => {
  console.log(`Analytics API listening on port ${port}`);
});
