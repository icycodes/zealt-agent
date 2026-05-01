const fs = require('fs/promises');
const path = require('path');
const { createClient } = require('@clickhouse/client');

const { CLICKHOUSE_HOST, CLICKHOUSE_PASSWORD } = process.env;

if (!CLICKHOUSE_HOST || !CLICKHOUSE_PASSWORD) {
  console.error('Missing CLICKHOUSE_HOST or CLICKHOUSE_PASSWORD environment variables.');
  process.exit(1);
}

const outputPath = path.join(__dirname, 'dictionary.json');

const normalizeClickHouseUrl = (rawHost) => {
  const withScheme = rawHost.startsWith('http://') || rawHost.startsWith('https://')
    ? rawHost
    : `https://${rawHost}`;
  const url = new URL(withScheme);
  if (!url.port) {
    url.port = '8443';
  }
  return url.toString();
};

const client = createClient({
  url: normalizeClickHouseUrl(CLICKHOUSE_HOST),
  username: 'default',
  password: CLICKHOUSE_PASSWORD,
});

async function extractDictionary() {
  const query = `
    SELECT database, table, name, type
    FROM system.columns
    WHERE database = 'system'
    ORDER BY table, name
  `;

  const resultSet = await client.query({
    query,
    format: 'JSONEachRow',
  });

  const rows = await resultSet.json();
  await fs.writeFile(outputPath, JSON.stringify(rows, null, 2));
  console.log(`Wrote ${rows.length} rows to ${outputPath}`);
}

extractDictionary()
  .catch((error) => {
    console.error('Failed to extract dictionary:', error);
    process.exitCode = 1;
  })
  .finally(async () => {
    await client.close();
  });
