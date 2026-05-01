import os
import clickhouse_connect

def main():
    # Read connection details from environment variables
    host = os.environ.get('CH_HOST')
    port = os.environ.get('CH_PORT')
    user = os.environ.get('CH_USER')
    password = os.environ.get('CH_PASSWORD')

    # Initialize the clickhouse_connect client with cold start handling configuration
    # connect_timeout=30, send_receive_timeout=120 as required
    try:
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
        
        # Print the result
        print(result.result_rows[0][0])

    except Exception as e:
        print(f"Error connecting to ClickHouse or executing query: {e}")

if __name__ == '__main__':
    main()
