#!/usr/bin/env bash

set -euo pipefail

: "${CH_API_KEY_ID:?CH_API_KEY_ID is required}"
: "${CH_API_KEY_SECRET:?CH_API_KEY_SECRET is required}"
: "${CH_ORG_ID:?CH_ORG_ID is required}"
: "${CH_SERVICE_ID:?CH_SERVICE_ID is required}"

api_url="https://api.clickhouse.cloud/v1/organizations/${CH_ORG_ID}/services/${CH_SERVICE_ID}/backupConfiguration"

payload='{"startTime":"00:00","retention":7}'

curl --fail --silent --show-error \
  --request PATCH \
  --url "${api_url}" \
  --header "Content-Type: application/json" \
  --user "${CH_API_KEY_ID}:${CH_API_KEY_SECRET}" \
  --data "${payload}"
