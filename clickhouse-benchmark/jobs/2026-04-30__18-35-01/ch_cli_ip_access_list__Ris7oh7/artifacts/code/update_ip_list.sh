#!/bin/bash

# Read the IP CIDR and description from arguments
IP_CIDR=$1
DESCRIPTION=$2

# Validate arguments
if [[ -z "$IP_CIDR" || -z "$DESCRIPTION" ]]; then
    echo "Usage: $0 <IP_CIDR> <DESCRIPTION>"
    exit 1
fi

# Set up the CLICKHOUSE_API_URL variable (default to https://api.clickhouse.cloud/v1)
API_URL=${CLICKHOUSE_API_URL:-https://api.clickhouse.cloud/v1}

# Read environment variables
ORG_ID=${CLICKHOUSE_ORG_ID}
SERVICE_ID=${CLICKHOUSE_SERVICE_ID}
KEY_ID=${CLICKHOUSE_KEY_ID}
KEY_SECRET=${CLICKHOUSE_KEY_SECRET}

# Validate environment variables
if [[ -z "$ORG_ID" || -z "$SERVICE_ID" || -z "$KEY_ID" || -z "$KEY_SECRET" ]]; then
    echo "Error: Required environment variables are not set."
    echo "Please set CLICKHOUSE_ORG_ID, CLICKHOUSE_SERVICE_ID, CLICKHOUSE_KEY_ID, and CLICKHOUSE_KEY_SECRET."
    exit 1
fi

# API endpoint
ENDPOINT="${API_URL}/organizations/${ORG_ID}/services/${SERVICE_ID}"

# Prepare JSON payload
# Using printf to safely handle potential special characters in description if needed, 
# but for simplicity and following instructions:
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

# Output log path
LOG_FILE="/home/user/ch-cli/output.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Send PATCH request using curl
curl -s -X PATCH \
    --user "${KEY_ID}:${KEY_SECRET}" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" \
    "$ENDPOINT" > "$LOG_FILE"

# Optional: Output the response to stdout as well if desired, 
# but requirement says "Output the curl response to /home/user/ch-cli/output.log"
