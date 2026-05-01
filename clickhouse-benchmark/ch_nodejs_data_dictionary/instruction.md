# ClickHouse Data Dictionary Extractor

## Background
You need to write a Node.js script that connects to ClickHouse Cloud using the official `@clickhouse/client` SDK and extracts a data dictionary (schema information) from the system tables.

## Requirements
- Initialize a Node.js project in `/home/user/ch_project`.
- Install `@clickhouse/client`.
- Create a script named `extract_dict.js` that connects to the ClickHouse Cloud instance.
- The script must read connection details from the following environment variables:
  - `CLICKHOUSE_HOST` (e.g., `https://your-host.clickhouse.cloud:8443`)
  - `CLICKHOUSE_PASSWORD`
- The user is implicitly `default`.
- Query the `system.columns` table to extract the `database`, `table`, `name` (column name), and `type` (column type) for all tables in the `system` database.
- Save the extracted data as a JSON array to `/home/user/ch_project/dictionary.json`.
- Run the script to generate the file.

## Implementation Guide
1. `cd /home/user/ch_project`
2. `npm init -y` and `npm install @clickhouse/client`
3. Write `extract_dict.js` to connect to ClickHouse and query `system.columns` where `database = 'system'`.
4. Format the output as a JSON array of objects and write to `dictionary.json`.
5. Run `node extract_dict.js`.

## Constraints
- Project path: /home/user/ch_project
- Output file: /home/user/ch_project/dictionary.json
- Use `@clickhouse/client` for Node.js.