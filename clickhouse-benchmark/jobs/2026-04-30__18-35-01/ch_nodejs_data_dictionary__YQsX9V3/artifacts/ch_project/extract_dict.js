const { createClient } = require('@clickhouse/client');
const fs = require('fs');
const path = require('path');

async function main() {
  const host = process.env.CLICKHOUSE_HOST;
  const password = process.env.CLICKHOUSE_PASSWORD;
  const port = process.env.CLICKHOUSE_PORT || '8443';

  if (!host || !password) {
    console.error('Error: CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD environment variables are required.');
    process.exit(1);
  }

  // Ensure host has protocol and port
  let url = host;
  if (!url.startsWith('http')) {
    url = `https://${host}:${port}`;
  }

  const client = createClient({
    url: url,
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
    
    console.log(`Successfully extracted ${dataset.length} columns to ${outputPath}`);
  } catch (error) {
    console.error('Error extracting data dictionary:', error);
    process.exit(1);
  } finally {
    await client.close();
  }
}

main();
