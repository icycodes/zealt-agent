const { createClient } = require('@clickhouse/client');

async function setup() {
  const client = createClient({
    url: 'http://localhost:8123',
    username: 'default',
    password: '',
  });

  try {
    await client.command({
      query: 'CREATE DATABASE IF NOT EXISTS grafana_db',
    });

    await client.command({
      query: `
        CREATE TABLE IF NOT EXISTS grafana_db.metrics (
          timestamp DateTime,
          metric_name String,
          value Float64
        ) ENGINE = MergeTree()
        ORDER BY (metric_name, timestamp)
      `,
    });

    await client.command({
      query: "CREATE USER IF NOT EXISTS grafana_user IDENTIFIED WITH plaintext_password BY 'grafana_pass'",
    });

    await client.command({
      query: 'GRANT SELECT ON grafana_db.metrics TO grafana_user',
    });

    console.log('Setup completed successfully');
  } catch (error) {
    console.error('Error during setup:', error);
    process.exit(1);
  } finally {
    await client.close();
  }
}

setup();
