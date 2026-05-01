import os
import clickhouse_connect

def main():
    host = os.environ.get('CLICKHOUSE_HOST')
    port = int(os.environ.get('CLICKHOUSE_PORT', 8443))
    username = os.environ.get('CLICKHOUSE_USERNAME')
    password = os.environ.get('CLICKHOUSE_PASSWORD')

    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=username,
        password=password
    )

    client.command("SET allow_experimental_json_type = 1")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS github_events (
        id String,
        type String,
        actor JSON,
        repo JSON,
        payload JSON,
        public UInt8,
        created_at DateTime
    ) ENGINE = MergeTree()
    ORDER BY id
    """
    client.command(create_table_query)

    insert_query = """
    INSERT INTO github_events
    SELECT id, type, actor, repo, payload, public, created_at
    FROM url('https://data.gharchive.org/2015-01-01-15.json.gz', 'JSONEachRow', 'id String, type String, actor JSON, repo JSON, payload JSON, public UInt8, created_at DateTime')
    """
    client.command(insert_query)

    result = client.query("SELECT count() FROM github_events")
    row_count = result.result_rows[0][0]

    with open('/home/user/ch-task/output.log', 'w') as f:
        f.write(str(row_count))

if __name__ == '__main__':
    main()
