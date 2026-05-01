import json
import os
import time
from datetime import datetime

import clickhouse_connect


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "t"}


def main() -> None:
    log_path = "/home/user/ch_benchmark/output.log"
    output_path = "/home/user/ch_benchmark/output.json"

    ch_host = os.environ.get("CH_HOST")
    ch_port = os.environ.get("CH_PORT")
    ch_user = os.environ.get("CH_USER")
    ch_password = os.environ.get("CH_PASSWORD", "")
    ch_secure = os.environ.get("CH_SECURE", "False")

    if not ch_host or not ch_port or not ch_user:
        raise RuntimeError("CH_HOST, CH_PORT, and CH_USER environment variables are required")

    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write("Starting ClickHouse benchmark\n")

        client = clickhouse_connect.get_client(
            host=ch_host,
            port=int(ch_port),
            username=ch_user,
            password=ch_password,
            secure=parse_bool(ch_secure),
        )

        client.command("DROP TABLE IF EXISTS events")
        client.command(
            "CREATE TABLE events (id UInt64, event_type String, timestamp DateTime) "
            "ENGINE = MergeTree ORDER BY id"
        )
        log_file.write("Created table events\n")

        now = datetime.utcnow()
        event_types = ["click", "view", "purchase"]
        rows = [
            (idx, event_types[(idx - 1) % len(event_types)], now)
            for idx in range(1, 1001)
        ]
        client.insert("events", rows, column_names=["id", "event_type", "timestamp"])
        log_file.write("Inserted 1000 rows\n")

        start = time.perf_counter()
        result = client.query("SELECT event_type, count() FROM events GROUP BY event_type")
        elapsed = time.perf_counter() - start

        data = {
            "time_seconds": round(elapsed, 6),
            "results": result.result_rows,
        }
        with open(output_path, "w", encoding="utf-8") as output_file:
            json.dump(data, output_file)

        log_file.write(f"Query completed in {elapsed:.6f} seconds\n")
        log_file.write(f"Results written to {output_path}\n")


if __name__ == "__main__":
    main()
