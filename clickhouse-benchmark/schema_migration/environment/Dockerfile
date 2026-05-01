FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages clickhouse-connect

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="ClickHouse Schema Migration task environment with initial migrations.sql."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat > migrations.sql <<'EOF'
CREATE TABLE IF NOT EXISTS test_migration (id UInt64) ENGINE = MergeTree ORDER BY id;
ALTER TABLE test_migration ADD COLUMN IF NOT EXISTS name String;
EOF

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - /home/user/myproject: base directory for the project
#   - /home/user/myproject/migrations.sql: initial SQL migration script

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
