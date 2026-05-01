const express = require('express');
const { createClient } = require('@clickhouse/client');

const app = express();
const port = 3000;

const clickhouseHost = process.env.CLICKHOUSE_HOST;
const clickhousePassword = process.env.CLICKHOUSE_PASSWORD;
const clickhouseUser = process.env.CLICKHOUSE_USER || 'default';

if (!clickhouseHost || !clickhousePassword) {
  console.warn('Missing CLICKHOUSE_HOST or CLICKHOUSE_PASSWORD environment variables.');
}

const client = createClient({
  host: clickhouseHost,
  username: clickhouseUser,
  password: clickhousePassword,
});

app.get('/tables', async (req, res) => {
  try {
    const resultSet = await client.query({
      query: 'SELECT name FROM system.tables LIMIT 5',
      format: 'JSONEachRow',
    });

    const rows = await resultSet.json();
    const names = rows.map((row) => row.name);
    res.json(names);
  } catch (error) {
    console.error('Failed to query ClickHouse:', error);
    res.status(500).json({ error: 'Failed to query ClickHouse' });
  }
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
