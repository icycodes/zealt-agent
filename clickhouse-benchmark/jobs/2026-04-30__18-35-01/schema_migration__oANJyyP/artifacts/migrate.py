import os
import sys
import clickhouse_connect

def migrate():
    host = os.getenv('CLICKHOUSE_HOST')
    port = int(os.getenv('CLICKHOUSE_PORT', 8443))
    username = os.getenv('CLICKHOUSE_USERNAME', 'default')
    password = os.getenv('CLICKHOUSE_PASSWORD')

    if not host or not password:
        print("Error: CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD environment variables are required.")
        sys.exit(1)

    try:
        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=username,
            password=password,
            secure=True
        )
        print(f"Connected to ClickHouse at {host}:{port}")

        migration_file = '/home/user/myproject/migrations.sql'
        if not os.path.exists(migration_file):
            print(f"Error: {migration_file} not found.")
            sys.exit(1)

        with open(migration_file, 'r') as f:
            sql_content = f.read()

        # Split statements by semicolon and filter out empty strings
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]

        for statement in statements:
            print(f"Executing: {statement}")
            client.command(statement)
            print("Successfully executed.")

        print("All migrations completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()
