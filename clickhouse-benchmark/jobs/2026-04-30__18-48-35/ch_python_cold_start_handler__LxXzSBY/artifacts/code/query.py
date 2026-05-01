import os
import clickhouse_connect


def main():
    # Read connection details from environment variables
    host = os.environ.get('CH_HOST')
    port = os.environ.get('CH_PORT')
    user = os.environ.get('CH_USER')
    password = os.environ.get('CH_PASSWORD')
    
    # Initialize ClickHouse client with cold start timeout settings
    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password,
        connect_timeout=30,
        send_receive_timeout=120
    )
    
    # Execute simple query
    result = client.command('SELECT 1')
    
    # Print the result
    print(result)


if __name__ == '__main__':
    main()