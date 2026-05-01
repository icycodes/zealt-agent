FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages clickhouse-connect==0.7.6

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Python environment with clickhouse-connect installed for S3 data ingestion task."

# Container contents:
#   - python3, pip3 installed
#   - clickhouse-connect library installed
#   - /home/user: base directory for the python script

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]