const { createClient } = require('@clickhouse/client');
const fs = require('fs');
const path = require('path');

async function run() {
  const host = process.env.CLICKHOUSE_HOST;
  const password = process.env.CLICKHOUSE_PASSWORD;

  if (!host || !password) {
    console.error('CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD environment variables are required');
    process.exit(1);
  }

  const client = createClient({
    url: `https://${host}:8443`,
    username: 'default',
    password: password,
  });

  try {
    // Create table
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

    // Bulk insert from CSV
    const csvPath = '/home/user/ch-task/employees.csv';
    await client.insert({
      table: 'employees',
      values: fs.createReadStream(csvPath),
      format: 'CSVWithNames',
    });

    // Write success log
    fs.writeFileSync('/home/user/ch-task/output.log', 'Success');
    console.log('Success');
  } catch (err) {
    console.error('Error:', err);
    process.exit(1);
  } finally {
    await client.close();
  }
}

run();
