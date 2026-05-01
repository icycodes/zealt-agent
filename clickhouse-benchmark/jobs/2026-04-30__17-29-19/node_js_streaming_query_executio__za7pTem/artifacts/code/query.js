const { createClient } = require('@clickhouse/client');

async function run() {
  let host = process.env.CLICKHOUSE_HOST || 'https://localhost:8443';
  if (!host.startsWith('http')) {
    host = `https://${host}`;
  }
  if (!host.includes(':') || host.split(':').length < 3) {
    // If port is not specified, add 8443 as per requirements
    host = host.replace(/\/$/, '');
    if (!host.match(/:\d+$/)) {
      host = `${host}:8443`;
    }
  }

  const client = createClient({
    url: host,
    username: process.env.CLICKHOUSE_USER || 'default',
    password: process.env.CLICKHOUSE_PASSWORD || '',
    database: 'system',
  });

  try {
    const resultSet = await client.query({
      query: 'SELECT * FROM system.tables LIMIT 10',
      format: 'JSONEachRow',
    });

    const stream = resultSet.stream();
    const result = [];

    for await (const rows of stream) {
      rows.forEach((row) => {
        result.push(row.json());
      });
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('Error executing query:', error);
    process.exit(1);
  } finally {
    await client.close();
  }
}

run();
