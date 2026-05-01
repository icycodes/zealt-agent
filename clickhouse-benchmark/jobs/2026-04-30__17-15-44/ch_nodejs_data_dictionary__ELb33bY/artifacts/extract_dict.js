const { createClient } = require('@clickhouse/client');
const fs = require('fs');

async function extractDictionary() {
  let host = process.env.CLICKHOUSE_HOST;
  if (host && !host.startsWith('http')) {
    host = 'https://' + host;
  }

  const client = createClient({
    url: host,
    username: 'default',
    password: process.env.CLICKHOUSE_PASSWORD,
  });

  try {
    const resultSet = await client.query({
      query: 'SELECT database, table, name, type FROM system.columns WHERE database = \'system\'',
      format: 'JSONEachRow',
    });

    const dataset = await resultSet.json();
    
    fs.writeFileSync('/home/user/ch_project/dictionary.json', JSON.stringify(dataset, null, 2));
    console.log('Dictionary extracted successfully.');
  } catch (error) {
    console.error('Error extracting dictionary:', error);
  } finally {
    await client.close();
  }
}

extractDictionary();
