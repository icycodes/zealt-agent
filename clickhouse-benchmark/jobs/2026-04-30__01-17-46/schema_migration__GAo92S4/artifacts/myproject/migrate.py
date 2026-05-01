import os
import sys

import clickhouse_connect


def main() -> int:
    host = os.environ.get("CLICKHOUSE_HOST")
    if not host:
        print("Missing CLICKHOUSE_HOST environment variable", file=sys.stderr)
        return 1

    port = int(os.environ.get("CLICKHOUSE_PORT", "8443"))
    username = os.environ.get("CLICKHOUSE_USERNAME", "default")
    password = os.environ.get("CLICKHOUSE_PASSWORD")

    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=username,
        password=password,
        secure=True,
    )

    migrations_path = os.path.join(os.path.dirname(__file__), "migrations.sql")
    with open(migrations_path, "r", encoding="utf-8") as migrations_file:
        raw_sql = migrations_file.read()

    statements = [statement.strip() for statement in raw_sql.split(";") if statement.strip()]

    if not statements:
        print("No migrations found in migrations.sql")
        return 0

    for index, statement in enumerate(statements, start=1):
        print(f"Executing migration {index}/{len(statements)}...")
        client.command(statement)

    print("Migrations completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
