import os
import clickhouse_connect

def main():
    host = os.environ.get('CLICKHOUSE_HOST')
    port = int(os.environ.get('CLICKHOUSE_PORT', '8443'))
    username = os.environ.get('CLICKHOUSE_USER', 'default')
    password = os.environ.get('CLICKHOUSE_PASSWORD')

    log_path = '/home/user/ch-migration/migration.log'

    try:
        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=username,
            password=password,
            secure=True
        )

        with open(log_path, 'a') as f:
            # Create table
            client.command('CREATE TABLE IF NOT EXISTS users (id UInt64, username String) ENGINE = MergeTree ORDER BY id')
            f.write('Table created\n')

            # Add column
            client.command('ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login DateTime')
            f.write('Column added\n')
            
            f.write('Migration successful\n')

    except Exception as e:
        with open(log_path, 'a') as f:
            f.write(f'Error: {e}\n')

if __name__ == '__main__':
    main()
