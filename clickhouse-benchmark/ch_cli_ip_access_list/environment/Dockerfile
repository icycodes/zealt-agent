FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/ch-cli && chmod 0755 /home/user/ch-cli

LABEL Author="any-task-builder"
LABEL Description="ClickHouse Cloud API CLI task environment."

# Container contents:
#   - curl installed for API requests.
#   - /home/user/ch-cli — base directory for the script.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
