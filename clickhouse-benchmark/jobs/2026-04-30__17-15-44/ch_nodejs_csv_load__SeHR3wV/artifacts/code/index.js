const { createClient } = require('@clickhouse/client');
const fs = require('fs');
const path = require('path');

async function main() {
    const host = process.env.CLICKHOUSE_HOST;
    const password = process.env.CLICKHOUSE_PASSWORD;

    const client = createClient({
        url: `https://${host}:8443`,
        username: 'default',
        password: password,
        database: 'default',
    });

    try {
        await client.command({
            query: `
                CREATE TABLE IF NOT EXISTS employees (
                    id UInt32,
                    name String,
                    department String,
                    salary Float64
                ) ENGINE = MergeTree()
                ORDER BY id
            `,
        });

        const readStream = fs.createReadStream(path.join(__dirname, 'employees.csv'));

        await client.insert({
            table: 'employees',
            values: readStream,
            format: 'CSVWithNames',
        });

        fs.writeFileSync(path.join(__dirname, 'output.log'), 'Success');
        console.log('Data loaded successfully.');
    } catch (error) {
        console.error('Error:', error);
        process.exit(1);
    } finally {
        await client.close();
    }
}

main();
