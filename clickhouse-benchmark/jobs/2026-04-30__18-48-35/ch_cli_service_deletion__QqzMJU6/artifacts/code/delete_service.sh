#!/bin/bash

# ClickHouse Cloud Service Deletion Script
# Usage: ./delete_service.sh <service-name>

# Check if service name argument is provided
if [ -z "$1" ]; then
    echo "Error: Service name is required."
    echo "Usage: $0 <service-name>"
    exit 1
fi

SERVICE_NAME="$1"

echo "Looking for service: $SERVICE_NAME"

# Get the list of services and find the matching service ID
SERVICE_ID=$(clickhousectl cloud service list | grep "$SERVICE_NAME" | awk '{print $1}')

# Check if service was found
if [ -z "$SERVICE_ID" ]; then
    echo "Error: Service '$SERVICE_NAME' not found."
    echo "Available services:"
    clickhousectl cloud service list
    exit 1
fi

echo "Found service ID: $SERVICE_ID"
echo "Deleting service..."

# Delete the service
clickhousectl cloud service delete "$SERVICE_ID"

# Check if deletion was successful
if [ $? -eq 0 ]; then
    echo "Service '$SERVICE_NAME' (ID: $SERVICE_ID) has been successfully deleted."
else
    echo "Error: Failed to delete service."
    exit 1
fi