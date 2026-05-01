import os
import clickhouse_connect

def main():
    host = os.environ.get('CLICKHOUSE_HOST', 'localhost')
    port = int(os.environ.get('CLICKHOUSE_PORT', '8123'))
    user = os.environ.get('CLICKHOUSE_USER', 'default')
    password = os.environ.get('CLICKHOUSE_PASSWORD', '')

    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password
    )

    client.command('''
        CREATE TABLE IF NOT EXISTS test_events (
            id UInt64,
            event_type String
        ) ENGINE = MergeTree()
        ORDER BY id
    ''')

    data = [
        [1, 'push'],
        [2, 'pull_request'],
        [3, 'issue']
    ]
    
    client.insert('test_events', data, column_names=['id', 'event_type'])

    count = client.command('SELECT count() FROM test_events')
    print(count)

if __name__ == '__main__':
    main()
