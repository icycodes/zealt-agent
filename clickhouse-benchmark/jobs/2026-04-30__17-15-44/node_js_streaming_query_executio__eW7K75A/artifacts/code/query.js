const { createClient } = require('@clickhouse/client');

async function main() {
  let host = process.env.CLICKHOUSE_HOST || '';
  if (!host.startsWith('http')) {
    host = 'https://' + host;
  }
  const url = new URL(host);
  url.protocol = 'https:';
  url.port = '8443';

  const client = createClient({
    url: url.toString(),
    username: process.env.CLICKHOUSE_USER,
    password: process.env.CLICKHOUSE_PASSWORD,
  });

  const resultSet = await client.query({
    query: 'SELECT * FROM system.tables',
    format: 'JSONEachRow',
  });

  const stream = resultSet.stream();
  const results = [];

  return new Promise((resolve, reject) => {
    stream.on('data', (rows) => {
      rows.forEach((row) => {
        results.push(row.json());
      });
    });

    stream.on('end', async () => {
      console.log(JSON.stringify(results, null, 2));
      await client.close();
      resolve();
    });

    stream.on('error', async (err) => {
      console.error(err);
      await client.close();
      reject(err);
    });
  });
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
