import os
import sys
import clickhouse_connect

def migrate():
    host = os.getenv('CLICKHOUSE_HOST')
    port = int(os.getenv('CLICKHOUSE_PORT', '8443'))
    username = os.getenv('CLICKHOUSE_USERNAME', 'default')
    password = os.getenv('CLICKHOUSE_PASSWORD')

    if not host or not password:
        print("Error: CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD environment variables must be set.")
        sys.exit(1)

    try:
        print(f"Connecting to ClickHouse at {host}:{port}...")
        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=username,
            password=password,
            secure=True
        )
        print("Connected successfully.")

        migrations_path = '/home/user/myproject/migrations.sql'
        if not os.path.exists(migrations_path):
            print(f"Error: {migrations_path} not found.")
            sys.exit(1)

        with open(migrations_path, 'r') as f:
            sql_content = f.read()

        # Split by semicolon and filter out empty statements
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]

        print(f"Found {len(statements)} statements to execute.")

        for i, statement in enumerate(statements, 1):
            print(f"Executing statement {i}/{len(statements)}...")
            print(f"SQL: {statement}")
            client.command(statement)
            print("Statement executed successfully.")

        print("Migration completed successfully.")

    except Exception as e:
        print(f"Error during migration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()
