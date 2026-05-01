import os
import subprocess
import json
import threading
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
import pytest

PROJECT_DIR = "/home/user/ch-cli"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "update_ip_list.sh")
LOG_FILE = os.path.join(PROJECT_DIR, "output.log")

class MockServerRequestHandler(BaseHTTPRequestHandler):
    captured_requests = []

    def do_PATCH(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        auth_header = self.headers.get('Authorization')
        
        MockServerRequestHandler.captured_requests.append({
            "path": self.path,
            "method": self.command,
            "body": body,
            "auth": auth_header,
            "content_type": self.headers.get('Content-Type')
        })

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "success", "message": "IP added"}')

def start_mock_server(port=8080):
    MockServerRequestHandler.captured_requests = []
    server = HTTPServer(('127.0.0.1', port), MockServerRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution_and_api_request():
    server = start_mock_server(8080)
    
    env = os.environ.copy()
    env["CLICKHOUSE_API_URL"] = "http://127.0.0.1:8080/v1"
    env["CLICKHOUSE_ORG_ID"] = "test-org"
    env["CLICKHOUSE_SERVICE_ID"] = "test-service"
    env["CLICKHOUSE_KEY_ID"] = "test-key"
    env["CLICKHOUSE_KEY_SECRET"] = "test-secret"

    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    result = subprocess.run(
        [SCRIPT_PATH, "192.168.1.0/24", "VPN Access"],
        env=env,
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )

    server.shutdown()
    server.server_close()

    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    requests = MockServerRequestHandler.captured_requests
    assert len(requests) > 0, "No HTTP requests were made by the script."
    
    req = requests[0]
    
    assert req["path"] == "/v1/organizations/test-org/services/test-service", \
        f"Incorrect API path requested: {req['path']}"
    
    assert req["method"] == "PATCH", \
        f"Incorrect HTTP method: {req['method']}"
        
    assert "application/json" in req["content_type"], \
        f"Incorrect Content-Type: {req['content_type']}"
        
    expected_auth = "Basic " + base64.b64encode(b"test-key:test-secret").decode('utf-8')
    assert req["auth"] == expected_auth, \
        f"Incorrect or missing Authorization header: {req['auth']}"
        
    try:
        body_json = json.loads(req["body"])
    except json.JSONDecodeError:
        pytest.fail(f"Invalid JSON payload sent: {req['body']}")
        
    expected_body = {
        "ipAccessList": {
            "add": [
                {
                    "source": "192.168.1.0/24",
                    "description": "VPN Access"
                }
            ]
        }
    }
    assert body_json == expected_body, f"Incorrect JSON payload: {body_json}"

def test_log_file_contains_response():
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} does not exist."
    with open(LOG_FILE, 'r') as f:
        content = f.read()
    assert "success" in content and "IP added" in content, \
        f"Log file does not contain expected mock server response: {content}"
