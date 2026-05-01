#!/bin/bash

# This script configures a custom backup schedule and retention policy for a ClickHouse Cloud service.
# It requires the following environment variables:
# - CH_API_KEY_ID: Your ClickHouse Cloud API Key ID
# - CH_API_KEY_SECRET: Your ClickHouse Cloud API Key Secret
# - CH_ORG_ID: Your ClickHouse Cloud Organization ID
# - CH_SERVICE_ID: Your ClickHouse Cloud Service ID

# Exit on error
set -e

# Validate environment variables
if [[ -z "$CH_API_KEY_ID" || -z "$CH_API_KEY_SECRET" || -z "$CH_ORG_ID" || -z "$CH_SERVICE_ID" ]]; then
    echo "Error: Required environment variables CH_API_KEY_ID, CH_API_KEY_SECRET, CH_ORG_ID, or CH_SERVICE_ID are not set."
    exit 1
fi

LOG_FILE="/home/user/ch-backup/output.log"
URL="https://api.clickhouse.cloud/v1/organizations/${CH_ORG_ID}/services/${CH_SERVICE_ID}/backupConfiguration"

# Prepare the JSON payload
# startTime: "00:00"
# retention: 7
PAYLOAD='{"startTime": "00:00", "retention": 7}'

# Perform the PATCH request using Basic Authentication
# The output is directed to the specified log file
echo "Executing backup configuration update at $(date)" >> "$LOG_FILE"
curl -s -X PATCH \
     -u "${CH_API_KEY_ID}:${CH_API_KEY_SECRET}" \
     -H "Content-Type: application/json" \
     -d "$PAYLOAD" \
     "$URL" >> "$LOG_FILE" 2>&1

echo "Configuration request completed. Results logged to $LOG_FILE"
