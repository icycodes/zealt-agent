#!/bin/bash

curl -X PATCH "https://api.clickhouse.cloud/v1/organizations/${CH_ORG_ID}/services/${CH_SERVICE_ID}/backupConfiguration" \
  -u "${CH_API_KEY_ID}:${CH_API_KEY_SECRET}" \
  -H "Content-Type: application/json" \
  -d '{
  "startTime": "00:00",
  "retention": 7
}' >> /home/user/ch-backup/output.log 2>&1
