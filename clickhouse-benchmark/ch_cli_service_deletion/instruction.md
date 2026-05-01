# ClickHouse Cloud Service Deletion Script

## Background
You need to automate the deletion of a specific ClickHouse Cloud service using the official `clickhousectl` CLI tool.

## Requirements
- Write a bash script named `delete_service.sh` that accepts a service name as its first argument.
- The script must use `clickhousectl cloud service list` to find the service ID associated with the provided service name.
- The script must then delete the service using `clickhousectl cloud service delete <service-id>`.
- If the service name is not found, the script should exit with an error message and code 1.
- Make the script executable.

## Constraints
- **Project path**: /home/user
- **Script path**: /home/user/delete_service.sh
- Use `clickhousectl` for all interactions.
- Do not hardcode the service ID.

## Integrations
- None