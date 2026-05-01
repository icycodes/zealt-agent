import os
import subprocess
import time
import socket
import json
import urllib.request
import urllib.error
import pytest
import signal

PROJECT_DIR = "/home/user/analytics-api"

def wait_for_port(port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def clickhouse_server():
    # Start ClickHouse server
    process = subprocess.Popen(
        ["su", "-s", "/bin/bash", "clickhouse", "-c",
         "/usr/bin/clickhouse-server --config-file=/etc/clickhouse-server/config.xml"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    if not wait_for_port(8123, timeout=60):
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("ClickHouse server failed to start on port 8123.")
    
    yield process
    
    # Shut down ClickHouse server
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait(timeout=10)
    except Exception:
        pass

@pytest.fixture(scope="module")
def start_app(clickhouse_server):
    env = os.environ.copy()
    env["CLICKHOUSE_URL"] = "http://localhost:8123"
    env["CLICKHOUSE_USER"] = "default"
    env["CLICKHOUSE_PASSWORD"] = ""
    
    process = subprocess.Popen(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    if not wait_for_port(3000, timeout=30):
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Node app failed to start on port 3000.")
    
    yield
    
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait(timeout=10)
    except Exception:
        pass

def test_metrics_endpoints(start_app, clickhouse_server):
    """Priority 3: Verify the GET /metrics endpoint returns 200, and 500 when DB fails."""
    # 1. Success case
    try:
        req = urllib.request.Request("http://localhost:3000/metrics")
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            data = json.loads(response.read().decode())
            assert "total_parts" in data, "Response JSON missing 'total_parts' property."
            assert isinstance(data["total_parts"], (int, float)), "'total_parts' should be numeric."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to request /metrics: {e}")

    # 2. Failure case
    try:
        os.killpg(os.getpgid(clickhouse_server.pid), signal.SIGTERM)
        clickhouse_server.wait(timeout=10)
    except Exception:
        pass
    
    time.sleep(2)
    
    try:
        req = urllib.request.Request("http://localhost:3000/metrics")
        urllib.request.urlopen(req)
        pytest.fail("Expected HTTPError 500, but request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 500, f"Expected status 500 on database failure, got {e.code}"
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")
