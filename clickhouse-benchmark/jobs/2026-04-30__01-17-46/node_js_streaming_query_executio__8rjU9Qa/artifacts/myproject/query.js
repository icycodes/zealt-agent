const { createClient } = require('@clickhouse/client');

function buildClickHouseUrl(rawHost) {
  if (!rawHost) {
    throw new Error('CLICKHOUSE_HOST is required');
  }

  if (/^https?:\/\//i.test(rawHost)) {
    const parsed = new URL(rawHost);
    parsed.protocol = 'https:';
    parsed.port = '8443';
    return parsed.toString();
  }

  return `https://${rawHost}:8443`;
}

async function run() {
  const url = buildClickHouseUrl(process.env.CLICKHOUSE_HOST);
  const username = process.env.CLICKHOUSE_USER;
  const password = process.env.CLICKHOUSE_PASSWORD;

  if (!username) {
    throw new Error('CLICKHOUSE_USER is required');
  }

  if (!password) {
    throw new Error('CLICKHOUSE_PASSWORD is required');
  }

  const client = createClient({
    url,
    username,
    password,
  });

  const result = await client.query({
    query: 'SELECT * FROM system.tables',
    format: 'JSONEachRow',
  });

  const rows = [];
  try {
    const stream = result.stream();
    for await (const chunk of stream) {
      for (const row of chunk) {
        rows.push(row.json());
      }
    }
  } finally {
    result.close();
  }

  process.stdout.write(`${JSON.stringify(rows, null, 2)}\n`);
}

run().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
