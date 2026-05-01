#!/bin/bash

EMAIL=$1
ROLE_ID=$2
KEY_NAME=$3

clickhousectl cloud --json invitation create --email "$EMAIL" --role-id "$ROLE_ID"
clickhousectl cloud --json key create --name "$KEY_NAME" --role-id "$ROLE_ID"
