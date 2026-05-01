FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash gnupg dirmngr apt-transport-https && \
    curl -fsSL 'https://packages.clickhouse.com/rpm/lts/repodata/repomd.xml.key' | gpg --dearmor -o /usr/share/keyrings/clickhouse-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/clickhouse-keyring.gpg] https://packages.clickhouse.com/deb stable main" | tee /etc/apt/sources.list.d/clickhouse.list && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends clickhouse-server clickhouse-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/ch_benchmark && chmod 0755 /home/user && chmod 0755 /home/user/ch_benchmark

LABEL Author="any-task-builder"
LABEL Description="ClickHouse Cloud Python SDK task environment with a local ClickHouse server running."

# Container contents:
#   - Python 3 and pip installed.
#   - ClickHouse server and client installed.
#   - /home/user/ch_benchmark directory created.

CMD ["/bin/bash", "-c", "su -s /bin/bash clickhouse -c '/usr/bin/clickhouse-server --config-file=/etc/clickhouse-server/config.xml --daemon' && trap : TERM INT; sleep infinity & wait"]
