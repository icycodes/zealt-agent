#!/bin/bash

# Check if service name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <service-name>"
    exit 1
fi

SERVICE_NAME="$1"

# Fetch the list of services in JSON format
SERVICES_JSON=$(clickhousectl cloud service list --json 2>/dev/null)

if [ $? -ne 0 ]; then
    echo "Error: Failed to fetch service list from clickhousectl."
    exit 1
fi

# Extract the service ID for the given service name using Python
SERVICE_ID=$(echo "$SERVICES_JSON" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    name_to_find = sys.argv[1]
    
    # Handle different possible JSON structures
    services = []
    if isinstance(data, list):
        services = data
    elif isinstance(data, dict):
        # Check common keys like 'services', 'items', 'result'
        services = data.get('services', data.get('items', data.get('result', [])))
        if not services and 'id' in data and 'name' in data:
            # Maybe it's a single object (though unlikely for a list command)
            services = [data]
    
    for s in services:
        if s.get('name') == name_to_find:
            # Try 'id' first, then 'service_id'
            sid = s.get('id') or s.get('service_id')
            if sid:
                print(sid)
                sys.exit(0)
    sys.exit(1)
except Exception:
    sys.exit(1)
" "$SERVICE_NAME")

if [ -z "$SERVICE_ID" ]; then
    echo "Error: Service '$SERVICE_NAME' not found."
    exit 1
fi

# Delete the service using the found ID
clickhousectl cloud service delete "$SERVICE_ID"

if [ $? -eq 0 ]; then
    echo "Successfully deleted service '$SERVICE_NAME' (ID: $SERVICE_ID)."
else
    echo "Error: Failed to delete service '$SERVICE_NAME' (ID: $SERVICE_ID)."
    exit 1
fi
