#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <service-name>" >&2
  exit 1
fi

service_name="$1"

service_id=$(clickhousectl cloud service list | awk -v name="$service_name" 'NR==1{next} $0 ~ name {print $1; exit}')

if [[ -z "$service_id" ]]; then
  echo "Error: service '$service_name' not found." >&2
  exit 1
fi

clickhousectl cloud service delete "$service_id"
