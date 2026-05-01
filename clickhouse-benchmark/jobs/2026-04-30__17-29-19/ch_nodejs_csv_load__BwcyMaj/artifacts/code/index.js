const { createClient } = require('@clickhouse/client');
const fs = require('fs');
const path = require('path');

async function main() {
  const client = createClient({
    url: `https://${process.env.CLICKHOUSE_HOST}:8443`,
    username: 'default',
    password: process.env.CLICKHOUSE_PASSWORD,
    database: 'default',
  });

  try {
    // Create table if it doesn't exist
    await client.command({
      query: `
        CREATE TABLE IF NOT EXISTS employees (
          id UInt32,
          name String,
          department String,
          salary Float64
        ) ENGINE = MergeTree()
        ORDER BY id
      `,
    });

    // Insert data from CSV stream
    const csvFilePath = '/home/user/ch-task/employees.csv';
    const stream = fs.createReadStream(csvFilePath);

    await client.insert({
      table: 'employees',
      values: stream,
      format: 'CSVWithNames',
    });

    // Write Success to output.log
    fs.writeFileSync('/home/user/ch-task/output.log', 'Success');
    console.log('Bulk load completed successfully.');
  } catch (err) {
    console.error('Error during bulk load:', err);
    process.exit(1);
  } finally {
    await client.close();
  }
}

main();
