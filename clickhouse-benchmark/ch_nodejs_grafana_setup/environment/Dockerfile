FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash \
        apt-transport-https dirmngr gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    GNUPGHOME=$(mktemp -d) && \
    GNUPGHOME="$GNUPGHOME" gpg --no-default-keyring --keyring /usr/share/keyrings/clickhouse-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 8919F6BD2B48D754 && \
    rm -rf "$GNUPGHOME" && \
    chmod +r /usr/share/keyrings/clickhouse-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/clickhouse-keyring.gpg] https://packages.clickhouse.com/deb stable main" | tee /etc/apt/sources.list.d/clickhouse.list && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends clickhouse-server clickhouse-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/project && chmod 0755 /home/user/project

LABEL Author="any-task-builder"
LABEL Description="Node.js environment with ClickHouse server installed for testing ClickHouse SDK."

# Container contents:
#   - Node.js v24 installed
#   - ClickHouse server and client installed
#   - /home/user/project directory created

# Start ClickHouse server in the background and keep the container running
CMD ["/bin/bash", "-c", "su - clickhouse -s /bin/bash -c \"/usr/bin/clickhouse-server --config-file=/etc/clickhouse-server/config.xml --daemon\" && trap : TERM INT; sleep infinity & wait"]
