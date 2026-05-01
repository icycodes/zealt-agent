const { createClient } = require('@clickhouse/client');

const client = createClient({
  host: 'http://localhost:8123',
});

async function main() {
  await client.command({
    query: 'CREATE DATABASE IF NOT EXISTS grafana_db',
  });

  await client.command({
    query: `
      CREATE TABLE IF NOT EXISTS grafana_db.metrics (
        timestamp DateTime,
        metric_name String,
        value Float64
      )
      ENGINE = MergeTree
      ORDER BY (metric_name, timestamp)
    `,
  });

  await client.command({
    query: "CREATE USER IF NOT EXISTS grafana_user IDENTIFIED WITH plaintext_password BY 'grafana_pass'",
  });

  await client.command({
    query: 'GRANT SELECT ON grafana_db.metrics TO grafana_user',
  });
}

main()
  .then(() => {
    process.exitCode = 0;
  })
  .catch((error) => {
    console.error('Failed to configure ClickHouse for Grafana:', error);
    process.exitCode = 1;
  })
  .finally(async () => {
    await client.close();
  });
