'use strict';

const { createClient } = require('@clickhouse/client');
const fs = require('fs');
const path = require('path');

async function main() {
  // 1. Connect to ClickHouse Cloud
  const client = createClient({
    url: `https://${process.env.CLICKHOUSE_HOST}:8443`,
    username: 'default',
    password: process.env.CLICKHOUSE_PASSWORD,
  });

  try {
    // 2. Create the employees table if it doesn't exist
    await client.command({
      query: `
        CREATE TABLE IF NOT EXISTS employees (
          id         UInt32,
          name       String,
          department String,
          salary     Float64
        )
        ENGINE = MergeTree()
        ORDER BY id
      `,
    });
    console.log('Table created (or already exists).');

    // 3. Read CSV as a stream and insert using CSVWithNames format
    const csvPath = path.join(__dirname, 'employees.csv');
    const csvStream = fs.createReadStream(csvPath);

    await client.insert({
      table: 'employees',
      values: csvStream,
      format: 'CSVWithNames',
    });
    console.log('Data inserted successfully.');

    // 4. Write "Success" to output.log
    const logPath = path.join(__dirname, 'output.log');
    fs.writeFileSync(logPath, 'Success\n');
    console.log('output.log written.');
  } finally {
    await client.close();
  }
}

main().catch((err) => {
  console.error('Error:', err);
  process.exit(1);
});
