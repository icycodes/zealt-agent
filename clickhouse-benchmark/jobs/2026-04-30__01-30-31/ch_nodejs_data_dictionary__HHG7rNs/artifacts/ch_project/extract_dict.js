'use strict';

const { createClient } = require('@clickhouse/client');
const fs = require('fs');
const path = require('path');

async function main() {
  // Read connection details from environment variables
  const host = process.env.CLICKHOUSE_HOST;
  const password = process.env.CLICKHOUSE_PASSWORD;

  if (!host) {
    console.error('ERROR: CLICKHOUSE_HOST environment variable is not set.');
    process.exit(1);
  }
  if (!password) {
    console.error('ERROR: CLICKHOUSE_PASSWORD environment variable is not set.');
    process.exit(1);
  }

  // Normalize host: ensure it has a protocol and port
  let normalizedHost = host.trim();
  if (!/^https?:\/\//i.test(normalizedHost)) {
    normalizedHost = `https://${normalizedHost}`;
  }
  if (!/:\d+$/.test(normalizedHost.replace(/^https?:\/\//, ''))) {
    normalizedHost = `${normalizedHost}:8443`;
  }

  console.log(`Connecting to ClickHouse at: ${normalizedHost}`);

  const client = createClient({
    url: normalizedHost,
    username: 'default',
    password: password,
  });

  try {
    console.log("Querying system.columns for database = 'system'...");

    const resultSet = await client.query({
      query: `
        SELECT
          database,
          table,
          name,
          type
        FROM system.columns
        WHERE database = 'system'
        ORDER BY table, name
      `,
      format: 'JSONEachRow',
    });

    const rows = await resultSet.json();

    console.log(`Retrieved ${rows.length} column records.`);

    const outputPath = path.join(__dirname, 'dictionary.json');
    fs.writeFileSync(outputPath, JSON.stringify(rows, null, 2), 'utf-8');

    console.log(`Data dictionary saved to: ${outputPath}`);
  } catch (err) {
    console.error('Error querying ClickHouse:', err.message || err);
    process.exit(1);
  } finally {
    await client.close();
  }
}

main();
