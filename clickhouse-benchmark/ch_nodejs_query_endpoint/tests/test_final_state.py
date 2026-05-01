import os
import subprocess
import time
import socket
import urllib.request
import json
import pytest

PROJECT_DIR = "/home/user/ch_api"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Start the app
    env = os.environ.copy()
    # Note: Harbor evaluation runner should provide CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD
    process = subprocess.Popen(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Wait for the app to be ready
    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_tables_endpoint_returns_json_array(start_app):
    url = "http://localhost:3000/tables"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert isinstance(data, list), "Expected response to be a JSON array"
            # It should return up to 5 tables
            assert len(data) <= 5, f"Expected up to 5 tables, got {len(data)}"
            if len(data) > 0:
                # Depending on implementation, it might be strings or objects with 'name'
                item = data[0]
                assert isinstance(item, (str, dict)), "Expected items to be strings or objects"
                if isinstance(item, dict):
                    assert 'name' in item, "Expected object to have 'name' property"
    except Exception as e:
        pytest.fail(f"Failed to request {url}: {e}")
