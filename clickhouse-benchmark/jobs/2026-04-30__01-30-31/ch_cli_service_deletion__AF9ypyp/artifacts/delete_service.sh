#!/usr/bin/env bash

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <service-name>" >&2
  exit 1
fi

SERVICE_NAME="$1"

echo "Looking up service ID for '${SERVICE_NAME}'..."

SERVICE_ID=$(clickhousectl cloud service list \
  --output json \
  | jq -r --arg name "${SERVICE_NAME}" '.[] | select(.name == $name) | .id' \
  2>/dev/null || true)

if [[ -z "${SERVICE_ID}" ]]; then
  echo "Error: service '${SERVICE_NAME}' not found." >&2
  exit 1
fi

echo "Found service ID: ${SERVICE_ID}"
echo "Deleting service '${SERVICE_NAME}' (${SERVICE_ID})..."

clickhousectl cloud service delete "${SERVICE_ID}"

echo "Service '${SERVICE_NAME}' deleted successfully."
