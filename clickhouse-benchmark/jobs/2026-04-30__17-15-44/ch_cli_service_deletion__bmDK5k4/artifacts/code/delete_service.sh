#!/bin/bash

if [ -z "$1" ]; then
    echo "Error: Service name not provided."
    exit 1
fi

SERVICE_NAME="$1"

# Fetch the JSON output
JSON_OUT=$(clickhousectl cloud service list --json 2>/dev/null)

if [ -n "$JSON_OUT" ]; then
    # Parse with Python if JSON output is available
    SERVICE_ID=$(echo "$JSON_OUT" | python3 -c '
import sys, json

try:
    data = json.loads(sys.stdin.read())
except Exception:
    sys.exit(0)

target_name = sys.argv[1]

def find_id(obj):
    if isinstance(obj, list):
        for item in obj:
            res = find_id(item)
            if res: return res
    elif isinstance(obj, dict):
        if obj.get("name") == target_name and "id" in obj:
            return obj["id"]
        for key, value in obj.items():
            res = find_id(value)
            if res: return res
    return None

res = find_id(data)
if res:
    print(res)
' "$SERVICE_NAME")
else
    # Fallback if --json is not supported or returned empty
    SERVICE_ID=$(clickhousectl cloud service list 2>/dev/null | grep -w "$SERVICE_NAME" | awk '{print $1}' | head -n 1)
fi

if [ -z "$SERVICE_ID" ]; then
    echo "Error: Service name '$SERVICE_NAME' not found."
    exit 1
fi

clickhousectl cloud service delete "$SERVICE_ID"
