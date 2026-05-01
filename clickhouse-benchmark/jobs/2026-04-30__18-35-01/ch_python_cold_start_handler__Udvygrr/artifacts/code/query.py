import os
import clickhouse_connect

def main():
    # Read connection details from environment variables
    host = os.environ.get('CH_HOST')
    port = os.environ.get('CH_PORT')
    user = os.environ.get('CH_USER')
    password = os.environ.get('CH_PASSWORD')

    # Initialize the clickhouse-connect client with specified timeouts for cold starts
    # connect_timeout: 30 seconds
    # send_receive_timeout: 120 seconds
    client = clickhouse_connect.get_client(
        host=host,
        port=int(port) if port else None,
        username=user,
        password=password,
        connect_timeout=30,
        send_receive_timeout=120
    )

    # Execute a simple query
    result = client.query('SELECT 1')

    # Print the result of the query
    if result.result_rows:
        print(result.result_rows[0][0])

if __name__ == '__main__':
    main()
