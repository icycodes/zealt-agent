# ClickHouse Cloud Backup Configuration Script

## Background
ClickHouse Cloud provides a Management API to manage service lifecycles and backups. You need to write a bash script that interacts with the ClickHouse Cloud Management API to configure a custom backup schedule and retention policy for a specific service.

## Requirements
- Write a bash script named `configure_backup.sh` in the project directory.
- The script must accept four environment variables: `CH_API_KEY_ID`, `CH_API_KEY_SECRET`, `CH_ORG_ID`, and `CH_SERVICE_ID`.
- It must use `curl` to send a `PATCH` request to the ClickHouse Cloud Management API (`https://api.clickhouse.cloud/v1/organizations/${CH_ORG_ID}/services/${CH_SERVICE_ID}/backupConfiguration`).
- The JSON payload should set the `startTime` field to `"00:00"` and the `retention` field to `7`.
- The script must use Basic Authentication with the provided API key ID and secret.
- The script must be executable.

## Constraints
- Project path: `/home/user/ch-backup`
- Log file: `/home/user/ch-backup/output.log`
- Do not execute the script; just create it and ensure it is correct and executable.

## Integrations
- None