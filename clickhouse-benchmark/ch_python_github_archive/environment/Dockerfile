FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash dirmngr apt-transport-https gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL 'https://packages.clickhouse.com/rpm/lts/repodata/repomd.xml.key' | gpg --dearmor -o /usr/share/keyrings/clickhouse-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/clickhouse-keyring.gpg] https://packages.clickhouse.com/deb stable main" | tee /etc/apt/sources.list.d/clickhouse.list && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends clickhouse-server clickhouse-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/ch-task && chmod 0755 /home/user/ch-task

ENV CLICKHOUSE_HOST=localhost
ENV CLICKHOUSE_PORT=8123
ENV CLICKHOUSE_USERNAME=default
ENV CLICKHOUSE_PASSWORD=

LABEL Author="any-task-builder"
LABEL Description="ClickHouse task environment with a local clickhouse-server simulating ClickHouse Cloud."

# Container contents:
#   - clickhouse-server and clickhouse-client installed.
#   - /home/user/ch-task — project directory for the task
#   - Environment variables for CLICKHOUSE_HOST, CLICKHOUSE_PORT, etc.

CMD ["/bin/bash", "-c", "sudo -u clickhouse clickhouse-server --daemon --config-file=/etc/clickhouse-server/config.xml || su -s /bin/bash clickhouse -c 'clickhouse-server --daemon --config-file=/etc/clickhouse-server/config.xml' && trap : TERM INT; sleep infinity & wait"]
