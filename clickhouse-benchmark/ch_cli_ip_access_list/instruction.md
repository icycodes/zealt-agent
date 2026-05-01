# Update ClickHouse Cloud IP Access List

## Background
You need to automate adding new IP addresses to a ClickHouse Cloud service's IP Access List using the Cloud Management API.

## Requirements
- Create a bash script `update_ip_list.sh` that takes two arguments: an IP CIDR (e.g., `10.0.0.0/8`) and a description.
- The script must use `curl` to send a `PATCH` request to the ClickHouse Cloud Management API to add the given IP to the access list.
- The script must read `CLICKHOUSE_ORG_ID`, `CLICKHOUSE_SERVICE_ID`, `CLICKHOUSE_KEY_ID`, and `CLICKHOUSE_KEY_SECRET` from environment variables.
- The script must use the base URL from the `CLICKHOUSE_API_URL` environment variable, defaulting to `https://api.clickhouse.cloud/v1` if not set.
- The script must use Basic Authentication with `KEY_ID:KEY_SECRET`.
- The API endpoint is `${CLICKHOUSE_API_URL}/organizations/${CLICKHOUSE_ORG_ID}/services/${CLICKHOUSE_SERVICE_ID}`.
- The JSON payload must follow the format: `{"ipAccessList": {"add": [{"source": "<IP>", "description": "<DESC>"}]}}`.
- The script must be executable.

## Implementation Guide
1. Read the IP CIDR and description from arguments (`$1` and `$2`).
2. Set up the `CLICKHOUSE_API_URL` variable (default to `https://api.clickhouse.cloud/v1`).
3. Use `curl -s -X PATCH` with `--user "${CLICKHOUSE_KEY_ID}:${CLICKHOUSE_KEY_SECRET}"` and `-H "Content-Type: application/json"`.
4. Send the correct JSON payload with `-d`.
5. Output the curl response to `/home/user/ch-cli/output.log`.

## Constraints
- Project path: /home/user/ch-cli
- Log file: /home/user/ch-cli/output.log
- Do not hardcode any credentials or IDs in the script.