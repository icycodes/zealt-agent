# ClickHouse Cloud Role and Key Management

## Background
You need to write a bash script to automate managing API keys and invitations in ClickHouse Cloud using `clickhousectl`.

## Requirements
- Create a bash script at `/home/user/ch-task/manage.sh`.
- The script should take three arguments: an email address, a role ID, and an API key name.
- It must use `clickhousectl` to:
  1. Create an invitation for the provided email address with the provided role ID.
  2. Create an API key with the provided API key name and the provided role ID.
- The script should output the results in JSON format by passing the `--json` flag to `clickhousectl`.
- Ensure the script is executable.

## Implementation Guide
1. Create the script `/home/user/ch-task/manage.sh`.
2. Add `#!/bin/bash` at the top.
3. Read the arguments: `EMAIL=$1`, `ROLE_ID=$2`, `KEY_NAME=$3`.
4. Execute `clickhousectl cloud --json invitation create --email "$EMAIL" --role-id "$ROLE_ID"`.
5. Execute `clickhousectl cloud --json key create --name "$KEY_NAME" --role-id "$ROLE_ID"`.
6. Make the script executable (`chmod +x`).

## Constraints
- Project path: /home/user/ch-task
- The script must exactly match the argument order: email, role ID, key name.
- Do not hardcode the arguments.

## Integrations
- ClickHouse Cloud