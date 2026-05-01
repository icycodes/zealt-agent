#!/bin/bash

# Exit on error
set -e

SERVICE_NAME=$1

if [ -z "$SERVICE_NAME" ]; then
    echo "Usage: $0 <service-name>"
    exit 1
fi

# Get the list of services in JSON format
# We capture the output and handle failure
SERVICES_JSON=$(clickhousectl cloud service list --json) || {
    echo "Error: Failed to retrieve service list from clickhousectl."
    exit 1
}

# Extract the service ID using Python
# We use a python script to parse the JSON and find the service by name
SERVICE_ID=$(echo "$SERVICES_JSON" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    target_name = sys.argv[1]
    
    services = []
    if isinstance(data, list):
        services = data
    elif isinstance(data, dict):
        # Handle cases where services might be under a key
        for key in ['services', 'items', 'data']:
            if key in data and isinstance(data[key], list):
                services = data[key]
                break
    
    for service in services:
        if service.get('name') == target_name:
            print(service.get('id', ''))
            sys.exit(0)
except Exception as e:
    # Optional: print(f'Debug error: {e}', file=sys.stderr)
    pass
sys.exit(1)
" "$SERVICE_NAME" 2>/dev/null)

if [ -z "$SERVICE_ID" ]; then
    echo "Error: Service '$SERVICE_NAME' not found."
    exit 1
fi

# Delete the service
echo "Deleting service '$SERVICE_NAME' (ID: $SERVICE_ID)..."
clickhousectl cloud service delete "$SERVICE_ID"
