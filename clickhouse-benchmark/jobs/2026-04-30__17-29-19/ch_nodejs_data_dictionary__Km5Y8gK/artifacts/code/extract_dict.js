const { createClient } = require('@clickhouse/client');
const fs = require('fs');
const path = require('path');

async function main() {
  let host = process.env.CLICKHOUSE_HOST;
  const password = process.env.CLICKHOUSE_PASSWORD;

  if (!host || !password) {
    console.error('CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD environment variables are required');
    process.exit(1);
  }

  // Ensure host has protocol
  if (!host.startsWith('http')) {
    const port = process.env.CLICKHOUSE_PORT || '8443';
    host = `https://${host}:${port}`;
  }

  const client = createClient({
    url: host,
    password: password,
    database: 'default',
  });

  try {
    const resultSet = await client.query({
      query: `
        SELECT database, table, name, type
        FROM system.columns
        WHERE database = 'system'
      `,
      format: 'JSONEachRow',
    });

    const dataset = await resultSet.json();

    const outputPath = path.join(__dirname, 'dictionary.json');
    fs.writeFileSync(outputPath, JSON.stringify(dataset, null, 2));

    console.log(`Dictionary saved to ${outputPath}`);
  } catch (error) {
    console.error('Error extracting dictionary:', error);
    process.exit(1);
  } finally {
    await client.close();
  }
}

main();
