const { createClient } = require('@clickhouse/client');
const fs = require('fs');
const path = require('path');

// Get connection details from environment variables
const host = process.env.CLICKHOUSE_HOST;
const port = process.env.CLICKHOUSE_PORT || '8443';
const password = process.env.CLICKHOUSE_PASSWORD;

// Validate required environment variables
if (!host) {
  console.error('Error: CLICKHOUSE_HOST environment variable is required');
  process.exit(1);
}

if (!password) {
  console.error('Error: CLICKHOUSE_PASSWORD environment variable is required');
  process.exit(1);
}

// Construct proper URL format
const url = `https://${host}:${port}`;

// Create ClickHouse client
const client = createClient({
  url: url,
  username: 'default',
  password: password,
});

async function extractDictionary() {
  try {
    console.log('Connecting to ClickHouse...');
    await client.ping();
    console.log('Connected successfully');

    console.log('Querying system.columns for system database...');
    
    // Query system.columns table for system database
    const resultSet = await client.query({
      query: `
        SELECT 
          database,
          table,
          name AS column_name,
          type AS column_type
        FROM system.columns
        WHERE database = 'system'
        ORDER BY database, table, name
      `,
      format: 'JSONEachRow',
    });

    // Fetch all rows
    const data = await resultSet.json();
    
    console.log(`Extracted ${data.length} columns from system database`);

    // Format output as JSON array
    const output = data.map(row => ({
      database: row.database,
      table: row.table,
      name: row.column_name,
      type: row.column_type
    }));

    // Write to dictionary.json
    const outputPath = path.join(__dirname, 'dictionary.json');
    fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), 'utf8');
    
    console.log(`Dictionary saved to ${outputPath}`);
    console.log(`Total entries: ${output.length}`);
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  } finally {
    await client.close();
  }
}

// Run the extraction
extractDictionary();