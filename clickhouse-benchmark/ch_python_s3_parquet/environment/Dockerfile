FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages clickhouse-connect

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="ClickHouse Cloud Python SDK (clickhouse-connect) environment."

RUN mkdir -p /home/user/app

# Container contents:
#   - clickhouse-connect installed via pip3.
#   - /home/user/app directory created for the project.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]