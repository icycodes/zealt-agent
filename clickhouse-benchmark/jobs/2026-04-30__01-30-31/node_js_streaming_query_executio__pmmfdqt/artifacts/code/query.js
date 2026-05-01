const { createClient } = require('@clickhouse/client');

async function main() {
  const host = process.env.CLICKHOUSE_HOST;
  const username = process.env.CLICKHOUSE_USER;
  const password = process.env.CLICKHOUSE_PASSWORD;

  if (!host || !username || !password) {
    console.error(
      'Missing required environment variables: CLICKHOUSE_HOST, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD'
    );
    process.exit(1);
  }

  // Ensure we connect over HTTPS on port 8443
  const url = host.startsWith('http') ? host : `https://${host}`;
  const clientUrl = new URL(url);
  clientUrl.port = '8443';
  clientUrl.protocol = 'https:';

  const client = createClient({
    url: clientUrl.toString(),
    username,
    password,
  });

  try {
    const resultSet = await client.query({
      query: 'SELECT * FROM system.tables',
      format: 'JSONEachRow',
    });

    // Stream and collect all rows from the response
    const rows = await resultSet.json();

    console.log(JSON.stringify(rows, null, 2));
  } finally {
    await client.close();
  }
}

main().catch((err) => {
  console.error('Error:', err.message || err);
  process.exit(1);
});
