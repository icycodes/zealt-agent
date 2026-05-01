#!/bin/bash

# ClickHouse Cloud Backup Configuration Script
# This script configures backup schedule and retention policy for a ClickHouse Cloud service

# Check for required environment variables
if [ -z "$CH_API_KEY_ID" ] || [ -z "$CH_API_KEY_SECRET" ] || [ -z "$CH_ORG_ID" ] || [ -z "$CH_SERVICE_ID" ]; then
    echo "Error: Missing required environment variables" >> /home/user/ch-backup/output.log
    echo "Required: CH_API_KEY_ID, CH_API_KEY_SECRET, CH_ORG_ID, CH_SERVICE_ID" >> /home/user/ch-backup/output.log
    exit 1
fi

# Log file
LOG_FILE="/home/user/ch-backup/output.log"

# API endpoint
API_URL="https://api.clickhouse.cloud/v1/organizations/${CH_ORG_ID}/services/${CH_SERVICE_ID}/backupConfiguration"

# JSON payload
PAYLOAD='{"startTime":"00:00","retention":7}'

# Send PATCH request with Basic Authentication
echo "Configuring backup for service ${CH_SERVICE_ID} in organization ${CH_ORG_ID}" >> "$LOG_FILE"
echo "Backup schedule: 00:00, Retention: 7 days" >> "$LOG_FILE"

RESPONSE=$(curl -s -w "\n%{http_code}" -X PATCH "$API_URL" \
    -H "Content-Type: application/json" \
    -u "${CH_API_KEY_ID}:${CH_API_KEY_SECRET}" \
    -d "$PAYLOAD" 2>&1)

# Extract HTTP status code from the last line
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
# Extract response body (everything except the last line)
RESPONSE_BODY=$(echo "$RESPONSE" | head -n -1)

# Check if request was successful
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "202" ]; then
    echo "Backup configuration updated successfully" >> "$LOG_FILE"
    echo "Response: $RESPONSE_BODY" >> "$LOG_FILE"
    exit 0
else
    echo "Error: Failed to update backup configuration" >> "$LOG_FILE"
    echo "HTTP Status: $HTTP_CODE" >> "$LOG_FILE"
    echo "Response: $RESPONSE_BODY" >> "$LOG_FILE"
    exit 1
fi