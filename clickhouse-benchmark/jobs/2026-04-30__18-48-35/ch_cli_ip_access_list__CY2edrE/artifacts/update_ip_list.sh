#!/bin/bash

# Read arguments
IP_CIDR="$1"
DESCRIPTION="$2"

# Validate arguments
if [ -z "$IP_CIDR" ] || [ -z "$DESCRIPTION" ]; then
    echo "Error: Missing arguments"
    echo "Usage: $0 <IP_CIDR> <DESCRIPTION>"
    echo "Example: $0 10.0.0.0/8 \"Office network\""
    exit 1
fi

# Read environment variables
CLICKHOUSE_ORG_ID="${CLICKHOUSE_ORG_ID}"
CLICKHOUSE_SERVICE_ID="${CLICKHOUSE_SERVICE_ID}"
CLICKHOUSE_KEY_ID="${CLICKHOUSE_KEY_ID}"
CLICKHOUSE_KEY_SECRET="${CLICKHOUSE_KEY_SECRET}"
CLICKHOUSE_API_URL="${CLICKHOUSE_API_URL:-https://api.clickhouse.cloud/v1}"

# Validate required environment variables
if [ -z "$CLICKHOUSE_ORG_ID" ] || [ -z "$CLICKHOUSE_SERVICE_ID" ] || [ -z "$CLICKHOUSE_KEY_ID" ] || [ -z "$CLICKHOUSE_KEY_SECRET" ]; then
    echo "Error: Missing required environment variables"
    echo "Required: CLICKHOUSE_ORG_ID, CLICKHOUSE_SERVICE_ID, CLICKHOUSE_KEY_ID, CLICKHOUSE_KEY_SECRET"
    exit 1
fi

# Construct API endpoint
API_ENDPOINT="${CLICKHOUSE_API_URL}/organizations/${CLICKHOUSE_ORG_ID}/services/${CLICKHOUSE_SERVICE_ID}"

# Construct JSON payload
JSON_PAYLOAD=$(cat <<EOF
{
    "ipAccessList": {
        "add": [
            {
                "source": "${IP_CIDR}",
                "description": "${DESCRIPTION}"
            }
        ]
    }
}
EOF
)

# Send PATCH request to ClickHouse Cloud API
curl -s -X PATCH \
    --user "${CLICKHOUSE_KEY_ID}:${CLICKHOUSE_KEY_SECRET}" \
    -H "Content-Type: application/json" \
    -d "${JSON_PAYLOAD}" \
    "${API_ENDPOINT}" > /home/user/ch-cli/output.log

# Check curl exit code
if [ $? -eq 0 ]; then
    echo "IP access list update request sent successfully"
    echo "Response saved to /home/user/ch-cli/output.log"
else
    echo "Error: Failed to send API request"
    exit 1
fi