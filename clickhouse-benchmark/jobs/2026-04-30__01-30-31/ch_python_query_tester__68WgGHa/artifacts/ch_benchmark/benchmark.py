#!/usr/bin/env python3
"""
ClickHouse Query Benchmark Script
Connects to ClickHouse, creates a table, inserts 1000 rows,
benchmarks a GROUP BY query, and writes results to output.json.
"""

import os
import json
import time
import datetime
import logging

import clickhouse_connect

# ---------------------------------------------------------------------------
# Logging setup – mirrors output to output.log
# ---------------------------------------------------------------------------
LOG_FILE = os.path.join(os.path.dirname(__file__), "output.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Connection config from environment variables
# ---------------------------------------------------------------------------
CH_HOST     = os.environ.get("CH_HOST", "localhost")
CH_PORT     = int(os.environ.get("CH_PORT", "8123"))
CH_USER     = os.environ.get("CH_USER", "default")
CH_PASSWORD = os.environ.get("CH_PASSWORD", "")
CH_SECURE   = os.environ.get("CH_SECURE", "False").strip().lower() in ("true", "1", "yes")

OUTPUT_JSON = os.path.join(os.path.dirname(__file__), "output.json")


def main() -> None:
    log.info("Connecting to ClickHouse at %s:%d (secure=%s, user=%s)", CH_HOST, CH_PORT, CH_SECURE, CH_USER)

    client = clickhouse_connect.get_client(
        host=CH_HOST,
        port=CH_PORT,
        username=CH_USER,
        password=CH_PASSWORD,
        secure=CH_SECURE,
    )

    # ------------------------------------------------------------------
    # 1. Create the events table (drop first so the script is idempotent)
    # ------------------------------------------------------------------
    log.info("Dropping table 'events' if it exists …")
    client.command("DROP TABLE IF EXISTS events")

    log.info("Creating table 'events' …")
    client.command(
        """
        CREATE TABLE events (
            id         UInt64,
            event_type String,
            timestamp  DateTime
        ) ENGINE = MergeTree
          ORDER BY id
        """
    )
    log.info("Table 'events' created.")

    # ------------------------------------------------------------------
    # 2. Insert exactly 1000 rows
    # ------------------------------------------------------------------
    event_types = ["click", "view", "purchase"]
    now = datetime.datetime.now()

    rows = [
        (i, event_types[(i - 1) % 3], now)
        for i in range(1, 1001)
    ]

    log.info("Inserting %d rows …", len(rows))
    client.insert(
        "events",
        rows,
        column_names=["id", "event_type", "timestamp"],
    )
    log.info("Insert complete.")

    # ------------------------------------------------------------------
    # 3 & 4. Execute benchmark query and record execution time
    # ------------------------------------------------------------------
    query = "SELECT event_type, count() FROM events GROUP BY event_type"
    log.info("Running benchmark query: %s", query)

    t_start = time.perf_counter()
    result = client.query(query)
    t_end = time.perf_counter()

    elapsed = round(t_end - t_start, 6)
    log.info("Query finished in %.6f seconds.", elapsed)

    # ------------------------------------------------------------------
    # 5. Write output.json
    # ------------------------------------------------------------------
    # result.result_rows is a list of tuples; convert to list of lists
    results = [list(row) for row in result.result_rows]
    log.info("Query results: %s", results)

    output = {
        "time_seconds": elapsed,
        "results": results,
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(output, fh, indent=2)

    log.info("Output written to %s", OUTPUT_JSON)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
