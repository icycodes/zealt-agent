import logging
import os

import clickhouse_connect

LOG_PATH = "/home/user/ch-migration/migration.log"


def get_env_value(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value


def main() -> None:
    host = get_env_value("CLICKHOUSE_HOST")
    if not host:
        raise ValueError("CLICKHOUSE_HOST environment variable is required")

    port = int(get_env_value("CLICKHOUSE_PORT", "8443"))
    username = get_env_value("CLICKHOUSE_USER", "default")
    password = get_env_value("CLICKHOUSE_PASSWORD", "")

    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=username,
        password=password,
        secure=True,
    )

    table_exists = client.query(
        "SELECT count() FROM system.tables WHERE database = currentDatabase() AND name = 'users'"
    ).result_rows[0][0]

    if table_exists == 0:
        client.command(
            "CREATE TABLE IF NOT EXISTS users (id UInt64, username String) ENGINE = MergeTree ORDER BY id"
        )
        logging.info("Table created")
    else:
        logging.info("Table already exists")

    column_exists = client.query(
        "SELECT count() FROM system.columns WHERE database = currentDatabase() AND table = 'users' AND name = 'last_login'"
    ).result_rows[0][0]

    if column_exists == 0:
        client.command("ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login DateTime")
        logging.info("Column added")
    else:
        logging.info("Column already exists")

    logging.info("Migration completed successfully")


if __name__ == "__main__":
    main()
