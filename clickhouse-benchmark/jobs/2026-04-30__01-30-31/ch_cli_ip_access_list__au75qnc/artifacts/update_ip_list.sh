#!/usr/bin/env bash

# Usage: ./update_ip_list.sh <IP_CIDR> <DESCRIPTION>
# Example: ./update_ip_list.sh 10.0.0.0/8 "Office network"
#
# Required environment variables:
#   CLICKHOUSE_ORG_ID      - ClickHouse Cloud organisation ID
#   CLICKHOUSE_SERVICE_ID  - ClickHouse Cloud service ID
#   CLICKHOUSE_KEY_ID      - API key ID (used for Basic Auth username)
#   CLICKHOUSE_KEY_SECRET  - API key secret (used for Basic Auth password)
#
# Optional environment variables:
#   CLICKHOUSE_API_URL     - Base API URL (default: https://api.clickhouse.cloud/v1)

set -euo pipefail

# ── Arguments ────────────────────────────────────────────────────────────────
IP_CIDR="${1:?Usage: $0 <IP_CIDR> <DESCRIPTION>}"
DESCRIPTION="${2:?Usage: $0 <IP_CIDR> <DESCRIPTION>}"

# ── Environment variables ─────────────────────────────────────────────────────
: "${CLICKHOUSE_ORG_ID:?Environment variable CLICKHOUSE_ORG_ID is required}"
: "${CLICKHOUSE_SERVICE_ID:?Environment variable CLICKHOUSE_SERVICE_ID is required}"
: "${CLICKHOUSE_KEY_ID:?Environment variable CLICKHOUSE_KEY_ID is required}"
: "${CLICKHOUSE_KEY_SECRET:?Environment variable CLICKHOUSE_KEY_SECRET is required}"

CLICKHOUSE_API_URL="${CLICKHOUSE_API_URL:-https://api.clickhouse.cloud/v1}"

# ── Derived values ────────────────────────────────────────────────────────────
ENDPOINT="${CLICKHOUSE_API_URL}/organizations/${CLICKHOUSE_ORG_ID}/services/${CLICKHOUSE_SERVICE_ID}"
LOG_FILE="/home/user/ch-cli/output.log"

# ── JSON payload ──────────────────────────────────────────────────────────────
PAYLOAD=$(printf '{"ipAccessList": {"add": [{"source": "%s", "description": "%s"}]}}' \
    "${IP_CIDR}" "${DESCRIPTION}")

# ── Send request ──────────────────────────────────────────────────────────────
curl -s -X PATCH \
    --user "${CLICKHOUSE_KEY_ID}:${CLICKHOUSE_KEY_SECRET}" \
    -H "Content-Type: application/json" \
    -d "${PAYLOAD}" \
    "${ENDPOINT}" \
    | tee "${LOG_FILE}"
