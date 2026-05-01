import os
import clickhouse_connect

def main():
    host = os.environ.get('CH_HOST', 'localhost')
    port = int(os.environ.get('CH_PORT', 8123))
    user = os.environ.get('CH_USER', 'default')
    password = os.environ.get('CH_PASSWORD', '')

    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password,
        connect_timeout=30,
        send_receive_timeout=120
    )

    result = client.query('SELECT 1')
    print(result.result_rows)

if __name__ == '__main__':
    main()
