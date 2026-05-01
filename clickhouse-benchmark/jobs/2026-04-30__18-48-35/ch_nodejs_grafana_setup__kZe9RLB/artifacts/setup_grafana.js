const { createClient } = require('@clickhouse/client');

async function setupGrafanaDB() {
  // Create ClickHouse client
  const client = createClient({
    url: 'http://localhost:8123',
    username: 'default',
    password: '',
  });

  try {
    console.log('Connecting to ClickHouse...');

    // Create database grafana_db
    console.log('Creating database grafana_db...');
    await client.command({
      query: 'CREATE DATABASE IF NOT EXISTS grafana_db',
    });
    console.log('Database grafana_db created successfully.');

    // Create table metrics
    console.log('Creating table grafana_db.metrics...');
    await client.command({
      query: `
        CREATE TABLE IF NOT EXISTS grafana_db.metrics (
          timestamp DateTime,
          metric_name String,
          value Float64
        )
        ENGINE = MergeTree()
        ORDER BY (metric_name, timestamp)
      `,
    });
    console.log('Table grafana_db.metrics created successfully.');

    // Create user grafana_user with password
    console.log('Creating user grafana_user...');
    await client.command({
      query: `CREATE USER IF NOT EXISTS grafana_user IDENTIFIED BY 'grafana_pass'`,
    });
    console.log('User grafana_user created successfully.');

    // Grant SELECT privilege on grafana_db.metrics to grafana_user
    console.log('Granting SELECT privilege on grafana_db.metrics to grafana_user...');
    await client.command({
      query: 'GRANT SELECT ON grafana_db.metrics TO grafana_user',
    });
    console.log('SELECT privilege granted successfully.');

    console.log('Setup completed successfully!');
  } catch (error) {
    console.error('Error during setup:', error);
    process.exit(1);
  } finally {
    await client.close();
  }
}

// Run the setup
setupGrafanaDB();