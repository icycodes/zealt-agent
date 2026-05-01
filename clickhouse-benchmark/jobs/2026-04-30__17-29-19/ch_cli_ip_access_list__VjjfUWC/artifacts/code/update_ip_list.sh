#!/bin/bash

# Read the IP CIDR and description from arguments
IP_CIDR=$1
DESCRIPTION=$2

# Check if arguments are provided
if [ -z "$IP_CIDR" ] || [ -z "$DESCRIPTION" ]; then
    echo "Usage: $0 <IP_CIDR> <DESCRIPTION>"
    exit 1
fi

# Set up the CLICKHOUSE_API_URL variable (default to https://api.clickhouse.cloud/v1)
API_URL=${CLICKHOUSE_API_URL:-https://api.clickhouse.cloud/v1}

# Read environment variables
ORG_ID=$CLICKHOUSE_ORG_ID
SERVICE_ID=$CLICKHOUSE_SERVICE_ID
KEY_ID=$CLICKHOUSE_KEY_ID
KEY_SECRET=$CLICKHOUSE_KEY_SECRET

# Check if required environment variables are set
if [ -z "$ORG_ID" ] || [ -z "$SERVICE_ID" ] || [ -z "$KEY_ID" ] || [ -z "$KEY_SECRET" ]; then
    echo "Error: Required environment variables (CLICKHOUSE_ORG_ID, CLICKHOUSE_SERVICE_ID, CLICKHOUSE_KEY_ID, CLICKHOUSE_KEY_SECRET) must be set."
    exit 1
fi

# The API endpoint is ${CLICKHOUSE_API_URL}/organizations/${CLICKHOUSE_ORG_ID}/services/${CLICKHOUSE_SERVICE_ID}
ENDPOINT="${API_URL}/organizations/${ORG_ID}/services/${SERVICE_ID}"

# The JSON payload must follow the format: {"ipAccessList": {"add": [{"source": "<IP>", "description": "<DESC>"}]}}
PAYLOAD=$(cat <<EOF
{
  "ipAccessList": {
    "add": [
      {
        "source": "$IP_CIDR",
        "description": "$DESCRIPTION"
      }
    ]
  }
}
EOF
)

# Use curl -s -X PATCH with --user "${CLICKHOUSE_KEY_ID}:${CLICKHOUSE_KEY_SECRET}" and -H "Content-Type: application/json"
# Output the curl response to /home/user/ch-cli/output.log
curl -s -X PATCH \
     --user "${KEY_ID}:${KEY_SECRET}" \
     -H "Content-Type: application/json" \
     -d "$PAYLOAD" \
     "$ENDPOINT" > /home/user/ch-cli/output.log
