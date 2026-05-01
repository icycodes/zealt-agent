#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# configure_backup.sh
# Configures a custom backup schedule and retention policy for a ClickHouse
# Cloud service via the Management API.
#
# Required environment variables:
#   CH_API_KEY_ID      – ClickHouse Cloud API key ID
#   CH_API_KEY_SECRET  – ClickHouse Cloud API key secret
#   CH_ORG_ID          – ClickHouse Cloud organisation ID
#   CH_SERVICE_ID      – ClickHouse Cloud service ID
# ---------------------------------------------------------------------------

LOG_FILE="/home/user/ch-backup/output.log"

log() {
  echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] $*" | tee -a "${LOG_FILE}"
}

# --- Validate required environment variables --------------------------------
for var in CH_API_KEY_ID CH_API_KEY_SECRET CH_ORG_ID CH_SERVICE_ID; do
  if [[ -z "${!var:-}" ]]; then
    echo "ERROR: Required environment variable '${var}' is not set." >&2
    exit 1
  fi
done

API_BASE_URL="https://api.clickhouse.cloud/v1"
ENDPOINT="${API_BASE_URL}/organizations/${CH_ORG_ID}/services/${CH_SERVICE_ID}/backupConfiguration"

PAYLOAD=$(cat <<'EOF'
{
  "startTime": "00:00",
  "retention": 7
}
EOF
)

log "Configuring backup for service '${CH_SERVICE_ID}' in organisation '${CH_ORG_ID}'..."
log "Endpoint : ${ENDPOINT}"
log "Payload  : ${PAYLOAD}"

HTTP_RESPONSE=$(curl --silent --show-error --write-out "\n%{http_code}" \
  --request PATCH \
  --url "${ENDPOINT}" \
  --user "${CH_API_KEY_ID}:${CH_API_KEY_SECRET}" \
  --header "Content-Type: application/json" \
  --data "${PAYLOAD}")

HTTP_BODY=$(echo "${HTTP_RESPONSE}" | sed '$d')
HTTP_STATUS=$(echo "${HTTP_RESPONSE}" | tail -n1)

log "HTTP status : ${HTTP_STATUS}"
log "Response    : ${HTTP_BODY}"

if [[ "${HTTP_STATUS}" -ge 200 && "${HTTP_STATUS}" -lt 300 ]]; then
  log "Backup configuration updated successfully."
else
  log "ERROR: API request failed with HTTP status ${HTTP_STATUS}."
  exit 1
fi
