#!/bin/bash

IP_CIDR="$1"
DESCRIPTION="$2"

if [ -z "$IP_CIDR" ] || [ -z "$DESCRIPTION" ]; then
    echo "Usage: $0 <IP_CIDR> <DESCRIPTION>"
    exit 1
fi

API_URL="${CLICKHOUSE_API_URL:-https://api.clickhouse.cloud/v1}"

ENDPOINT="${API_URL}/organizations/${CLICKHOUSE_ORG_ID}/services/${CLICKHOUSE_SERVICE_ID}"

curl -s -X PATCH "$ENDPOINT" \
    --user "${CLICKHOUSE_KEY_ID}:${CLICKHOUSE_KEY_SECRET}" \
    -H "Content-Type: application/json" \
    -d "{\"ipAccessList\": {\"add\": [{\"source\": \"$IP_CIDR\", \"description\": \"$DESCRIPTION\"}]}}" > /home/user/ch-cli/output.log
