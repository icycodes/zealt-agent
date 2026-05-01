#!/bin/bash

EMAIL=$1
ROLE_ID=$2
KEY_NAME=$3

# Execute clickhousectl cloud --json invitation create --email "$EMAIL" --role-id "$ROLE_ID"
clickhousectl cloud --json invitation create --email "$EMAIL" --role-id "$ROLE_ID"

# Execute clickhousectl cloud --json key create --name "$KEY_NAME" --role-id "$ROLE_ID"
clickhousectl cloud --json key create --name "$KEY_NAME" --role-id "$ROLE_ID"
