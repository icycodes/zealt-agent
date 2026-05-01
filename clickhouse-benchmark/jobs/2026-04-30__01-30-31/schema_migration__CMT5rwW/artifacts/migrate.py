import os
import sys
import clickhouse_connect

def main():
    host = os.environ.get("CLICKHOUSE_HOST")
    port = int(os.environ.get("CLICKHOUSE_PORT", 8443))
    username = os.environ.get("CLICKHOUSE_USERNAME", "default")
    password = os.environ.get("CLICKHOUSE_PASSWORD")

    if not host:
        print("ERROR: CLICKHOUSE_HOST environment variable is not set.", flush=True)
        sys.exit(1)

    if not password:
        print("ERROR: CLICKHOUSE_PASSWORD environment variable is not set.", flush=True)
        sys.exit(1)

    migrations_file = os.path.join(os.path.dirname(__file__), "migrations.sql")

    print(f"Connecting to ClickHouse at {host}:{port} as '{username}'...", flush=True)

    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=username,
        password=password,
        secure=True,
    )

    print("Connection established.", flush=True)

    with open(migrations_file, "r") as f:
        sql_content = f.read()

    statements = [s.strip() for s in sql_content.split(";") if s.strip()]

    print(f"Found {len(statements)} migration statement(s) to execute.", flush=True)

    for i, statement in enumerate(statements, start=1):
        print(f"[{i}/{len(statements)}] Executing: {statement[:80]}{'...' if len(statement) > 80 else ''}", flush=True)
        client.command(statement)
        print(f"[{i}/{len(statements)}] OK", flush=True)

    print("All migrations executed successfully.", flush=True)

if __name__ == "__main__":
    main()
