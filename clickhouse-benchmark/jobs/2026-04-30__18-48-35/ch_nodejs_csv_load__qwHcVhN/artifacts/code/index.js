const { createClient } = require('@clickhouse/client');
const fs = require('fs');
const path = require('path');

async function main() {
  // Create ClickHouse client
  const client = createClient({
    host: `https://${process.env.CLICKHOUSE_HOST}:8443`,
    username: 'default',
    password: process.env.CLICKHOUSE_PASSWORD,
  });

  try {
    // Create the employees table if it doesn't exist
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
      format: 'JSON',
    });
    console.log('Table created (or already exists)');

    // Read CSV file as a stream and insert into ClickHouse
    const csvPath = path.join(__dirname, 'employees.csv');
    const csvStream = fs.createReadStream(csvPath);

    await client.insert({
      table: 'employees',
      format: 'CSVWithNames',
      values: csvStream,
    });
    console.log('Data inserted successfully');

    // Write "Success" to output.log
    fs.writeFileSync(path.join(__dirname, 'output.log'), 'Success');
    console.log('Output log written successfully');

  } catch (error) {
    console.error('Error:', error);
    throw error;
  } finally {
    await client.close();
  }
}

main().catch(console.error);
