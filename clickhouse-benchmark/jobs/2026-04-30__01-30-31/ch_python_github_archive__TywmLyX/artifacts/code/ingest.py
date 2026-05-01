#!/usr/bin/env python3
"""
Ingest GitHub Archive events into ClickHouse Cloud.

Reads connection details from environment variables:
  CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD

Downloads one hour of GitHub Archive data (2015-01-01-15.json.gz) and inserts
it into the `github_events` table using ClickHouse's url() table function.
"""

import os
import logging

import clickhouse_connect

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration from environment
# ---------------------------------------------------------------------------
CLICKHOUSE_HOST = os.environ["CLICKHOUSE_HOST"]
CLICKHOUSE_PORT = int(os.environ.get("CLICKHOUSE_PORT", 8443))
CLICKHOUSE_USERNAME = os.environ.get("CLICKHOUSE_USERNAME", "default")
CLICKHOUSE_PASSWORD = os.environ.get("CLICKHOUSE_PASSWORD", "")

GHARCHIVE_URL = "https://data.gharchive.org/2015-01-01-15.json.gz"
TABLE_NAME = "github_events"
OUTPUT_LOG = "/home/user/ch-task/output.log"


def get_client() -> clickhouse_connect.driver.Client:
    """Return an authenticated ClickHouse client."""
    log.info("Connecting to ClickHouse at %s:%s", CLICKHOUSE_HOST, CLICKHOUSE_PORT)
    client = clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        username=CLICKHOUSE_USERNAME,
        password=CLICKHOUSE_PASSWORD,
        secure=True,
        # Increase timeout for large inserts via url()
        connect_timeout=30,
        send_receive_timeout=600,
    )
    return client


def create_table(client: clickhouse_connect.driver.Client) -> None:
    """Drop (if exists) and re-create the github_events table."""
    log.info("Creating table '%s' (dropping if it already exists)...", TABLE_NAME)
    client.command(f"DROP TABLE IF EXISTS {TABLE_NAME}")
    ddl = f"""
    CREATE TABLE {TABLE_NAME}
    (
        id         String,
        type       String,
        actor      JSON,
        repo       JSON,
        payload    JSON,
        public     UInt8,
        created_at DateTime
    )
    ENGINE = MergeTree()
    ORDER BY id
    SETTINGS allow_experimental_json_type = 1
    """
    client.command(ddl)
    log.info("Table '%s' created successfully.", TABLE_NAME)


def ingest_data(client: clickhouse_connect.driver.Client) -> None:
    """Insert GitHub Archive data using ClickHouse's url() table function."""
    log.info("Starting ingestion from %s ...", GHARCHIVE_URL)
    insert_sql = f"""
    INSERT INTO {TABLE_NAME}
        (id, type, actor, repo, payload, public, created_at)
    SELECT
        JSONExtractString(line, 'id')                              AS id,
        JSONExtractString(line, 'type')                            AS type,
        JSONExtractRaw(line, 'actor')                              AS actor,
        JSONExtractRaw(line, 'repo')                               AS repo,
        JSONExtractRaw(line, 'payload')                            AS payload,
        toUInt8(JSONExtractBool(line, 'public'))                   AS public,
        parseDateTimeBestEffortOrNull(
            JSONExtractString(line, 'created_at'))                 AS created_at
    FROM url('{GHARCHIVE_URL}', 'LineAsString', 'line String')
    SETTINGS
        max_http_get_redirects    = 3,
        input_format_parallel_parsing = 0
    """
    client.command(insert_sql)
    log.info("Ingestion complete.")


def get_row_count(client: clickhouse_connect.driver.Client) -> int:
    """Return the total row count of the github_events table."""
    result = client.query(f"SELECT count() FROM {TABLE_NAME}")
    return result.result_rows[0][0]


def write_output_log(row_count: int) -> None:
    """Write the row count to the output log file."""
    os.makedirs(os.path.dirname(OUTPUT_LOG), exist_ok=True)
    with open(OUTPUT_LOG, "w") as fh:
        fh.write(f"Total rows in {TABLE_NAME}: {row_count}\n")
    log.info("Row count written to %s  →  %d rows", OUTPUT_LOG, row_count)


def main() -> None:
    client = get_client()

    create_table(client)
    ingest_data(client)

    row_count = get_row_count(client)
    log.info("Total rows in '%s': %d", TABLE_NAME, row_count)

    write_output_log(row_count)

    client.close()
    log.info("Done.")


if __name__ == "__main__":
    main()
