const { createClient } = require('@clickhouse/client');

// Get credentials from environment variables
const host = process.env.CLICKHOUSE_HOST;
const user = process.env.CLICKHOUSE_USER;
const password = process.env.CLICKHOUSE_PASSWORD;

// Create ClickHouse client with HTTPS connection on port 8443
const client = createClient({
  host: `https://${host}:8443`,
  username: user,
  password: password,
});

async function queryTables() {
  try {
    // Query system.tables with JSONEachRow format
    const resultSet = await client.query({
      query: 'SELECT * FROM system.tables',
      format: 'JSONEachRow',
    });

    // Stream the results and collect them
    const results = [];
    
    for await (const row of resultSet.stream()) {
      results.push(row);
    }

    // Log the fully parsed JSON array to the console
    console.log(JSON.stringify(results, null, 2));
    
  } catch (error) {
    console.error('Error executing query:', error);
    process.exit(1);
  } finally {
    await client.close();
  }
}

// Execute the query
queryTables();