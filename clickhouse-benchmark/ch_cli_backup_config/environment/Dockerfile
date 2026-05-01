FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="ClickHouse Cloud backup configuration script task environment."

RUN mkdir -p /home/user/ch-backup

# Container contents:
#   - curl installed for API requests.
#   - /home/user/ch-backup — project directory for the bash script.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
