import os
import clickhouse_connect

def main():
    host = os.environ.get('CLICKHOUSE_HOST')
    port = int(os.environ.get('CLICKHOUSE_PORT', 8443))
    username = os.environ.get('CLICKHOUSE_USERNAME', 'default')
    password = os.environ.get('CLICKHOUSE_PASSWORD')

    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=username,
        password=password,
        secure=True
    )

    with open('migrations.sql', 'r') as f:
        sql = f.read()

    statements = sql.split(';')
    for statement in statements:
        statement = statement.strip()
        if statement:
            print(f"Executing: {statement}")
            client.command(statement)
            print("Done.")

if __name__ == '__main__':
    main()
