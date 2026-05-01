#!/usr/bin/env bash
set -euo pipefail

IP_CIDR="${1:-}"
DESCRIPTION="${2:-}"

if [[ -z "${IP_CIDR}" || -z "${DESCRIPTION}" ]]; then
  echo "Usage: $0 <ip_cidr> <description>" >&2
  exit 1
fi

: "${CLICKHOUSE_ORG_ID:?Environment variable CLICKHOUSE_ORG_ID is required}"
: "${CLICKHOUSE_SERVICE_ID:?Environment variable CLICKHOUSE_SERVICE_ID is required}"
: "${CLICKHOUSE_KEY_ID:?Environment variable CLICKHOUSE_KEY_ID is required}"
: "${CLICKHOUSE_KEY_SECRET:?Environment variable CLICKHOUSE_KEY_SECRET is required}"

CLICKHOUSE_API_URL="${CLICKHOUSE_API_URL:-https://api.clickhouse.cloud/v1}"
ENDPOINT="${CLICKHOUSE_API_URL}/organizations/${CLICKHOUSE_ORG_ID}/services/${CLICKHOUSE_SERVICE_ID}"

JSON_PAYLOAD=$(printf '{"ipAccessList": {"add": [{"source": "%s", "description": "%s"}]}}' "${IP_CIDR}" "${DESCRIPTION}")

curl -s -X PATCH \
  --user "${CLICKHOUSE_KEY_ID}:${CLICKHOUSE_KEY_SECRET}" \
  -H "Content-Type: application/json" \
  -d "${JSON_PAYLOAD}" \
  "${ENDPOINT}" \
  > /home/user/ch-cli/output.log
