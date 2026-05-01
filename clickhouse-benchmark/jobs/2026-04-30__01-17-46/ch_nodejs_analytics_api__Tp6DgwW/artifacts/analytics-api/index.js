const express = require('express');
const { createClient } = require('@clickhouse/client');

const app = express();
const port = 3000;

const clickhouseClient = createClient({
  url: process.env.CLICKHOUSE_URL,
  username: process.env.CLICKHOUSE_USER,
  password: process.env.CLICKHOUSE_PASSWORD,
});

app.get('/metrics', async (req, res) => {
  try {
    const result = await clickhouseClient.query({
      query: 'SELECT count() AS total_parts FROM system.parts',
      format: 'JSONEachRow',
    });

    const rows = await result.json();
    const totalParts = rows[0]?.total_parts ?? 0;

    res.json({ total_parts: Number(totalParts) });
  } catch (error) {
    console.error('Failed to fetch metrics:', error);
    res.status(500).json({ error: 'Failed to fetch metrics' });
  }
});

app.listen(port, () => {
  console.log(`Analytics API listening on port ${port}`);
});
