const fs = require('fs');
const path = require('path');
const { createClient } = require('@clickhouse/client');

const CSV_PATH = '/home/user/ch-task/employees.csv';
const OUTPUT_LOG = '/home/user/ch-task/output.log';

const host = process.env.CLICKHOUSE_HOST;
const password = process.env.CLICKHOUSE_PASSWORD;

if (!host || !password) {
  console.error('CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD must be set.');
  process.exit(1);
}

const client = createClient({
  url: `https://${host}:8443`,
  username: 'default',
  password,
});

async function main() {
  await client.exec({
    query: `
      CREATE TABLE IF NOT EXISTS employees (
        id UInt32,
        name String,
        department String,
        salary Float64
      )
      ENGINE = MergeTree()
      ORDER BY id
    `,
  });

  const csvStream = fs.createReadStream(CSV_PATH);

  await client.insert({
    table: 'employees',
    values: csvStream,
    format: 'CSVWithNames',
  });

  await fs.promises.writeFile(OUTPUT_LOG, 'Success');
}

main()
  .then(() => client.close())
  .catch(async (error) => {
    console.error(error);
    try {
      await client.close();
    } catch (closeError) {
      console.error(closeError);
    }
    process.exit(1);
  });
