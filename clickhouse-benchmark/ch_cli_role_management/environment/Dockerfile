FROM ubuntu:22.04

RUN apt-get update && apt-get install -y curl bash && rm -rf /var/lib/apt/lists/*

# Install clickhousectl
RUN ARCH=$(uname -m) && \
    curl -sL "https://github.com/ClickHouse/clickhousectl/releases/download/v0.1.18/clickhousectl-${ARCH}-unknown-linux-musl" -o /usr/local/bin/clickhousectl && \
    chmod +x /usr/local/bin/clickhousectl && \
    ln -s /usr/local/bin/clickhousectl /usr/local/bin/chctl

RUN useradd -m -s /bin/bash user
USER user
WORKDIR /home/user

RUN mkdir -p /home/user/ch-task
