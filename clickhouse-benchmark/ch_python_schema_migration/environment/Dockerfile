FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages clickhouse-connect==0.7.3

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="ClickHouse Cloud Schema Migration task environment with python3 and clickhouse-connect."

RUN mkdir -p /home/user/ch-migration

# Container contents:
#   - clickhouse-connect installed via pip.
#   - /home/user/ch-migration - empty project directory for the migration script.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]