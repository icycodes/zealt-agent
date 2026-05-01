#!/bin/bash

# Required environment variables:
# CH_API_KEY_ID
# CH_API_KEY_SECRET
# CH_ORG_ID
# CH_SERVICE_ID

LOG_FILE="/home/user/ch-backup/output.log"

# Check if environment variables are set
if [ -z "$CH_API_KEY_ID" ] || [ -z "$CH_API_KEY_SECRET" ] || [ -z "$CH_ORG_ID" ] || [ -z "$CH_SERVICE_ID" ]; then
    echo "Error: Missing required environment variables." | tee -a "$LOG_FILE"
    exit 1
fi

URL="https://api.clickhouse.cloud/v1/organizations/${CH_ORG_ID}/services/${CH_SERVICE_ID}/backupConfiguration"

# Send PATCH request to ClickHouse Cloud Management API
curl -s -X PATCH "$URL" \
    -u "${CH_API_KEY_ID}:${CH_API_KEY_SECRET}" \
    -H "Content-Type: application/json" \
    -d '{
        "startTime": "00:00",
        "retention": 7
    }' >> "$LOG_FILE" 2>&1

exit $?
