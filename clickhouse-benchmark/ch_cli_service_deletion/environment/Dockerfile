FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN ARCH="$(uname -m)" && \
    case "$ARCH" in \
      x86_64|amd64) ARCH_TARGET="x86_64" ;; \
      aarch64|arm64) ARCH_TARGET="aarch64" ;; \
    esac && \
    curl -fsSL "https://github.com/ClickHouse/clickhousectl/releases/download/v0.1.18/clickhousectl-${ARCH_TARGET}-unknown-linux-musl" -o /usr/local/bin/clickhousectl && \
    chmod +x /usr/local/bin/clickhousectl

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="ClickHouse Cloud task environment with clickhousectl installed."

# Container contents:
#   - clickhousectl installed in /usr/local/bin/
#   - /home/user as the base directory for the script

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]