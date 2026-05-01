FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Node.js task environment for ClickHouse Cloud CSV bulk load."

RUN mkdir -p /home/user/ch-task && \
    cd /home/user/ch-task && \
    cat >employees.csv <<'EOF'
id,name,department,salary
1,Alice,Engineering,120000.50
2,Bob,Marketing,85000.00
3,Charlie,Sales,90000.00
4,Diana,Engineering,135000.00
5,Eve,HR,75000.00
EOF

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24 for the task environment
#   - /home/user/ch-task: base directory for the project
#   - /home/user/ch-task/employees.csv: CSV file with 5 records and 1 header row

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
