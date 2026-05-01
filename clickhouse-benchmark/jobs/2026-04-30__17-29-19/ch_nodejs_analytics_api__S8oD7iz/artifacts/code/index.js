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
    
    if (dataset.length > 0) {
      // ClickHouse might return count() as a string for large values
      const totalParts = Number(dataset[0].total_parts);
      res.json({ total_parts: totalParts });
    } else {
      res.json({ total_parts: 0 });
    }
  } catch (error) {
    console.error('ClickHouse query error:', error);
    res.status(500).json({ error: 'Database query failed' });
  }
});

app.listen(port, () => {
  console.log(`Analytics API listening at http://localhost:${port}`);
});
