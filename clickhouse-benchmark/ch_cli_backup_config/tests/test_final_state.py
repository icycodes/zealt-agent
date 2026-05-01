import os
import pytest

SCRIPT_FILE = "/home/user/ch-backup/configure_backup.sh"

def test_script_exists_and_executable():
    """Priority 3 fallback: basic file existence and permissions check."""
    assert os.path.isfile(SCRIPT_FILE), f"Script not found at {SCRIPT_FILE}"
    assert os.access(SCRIPT_FILE, os.X_OK), f"Script {SCRIPT_FILE} is not executable."

def test_script_contains_correct_api_endpoint():
    """Priority 3 fallback: verify curl command targets correct endpoint."""
    with open(SCRIPT_FILE, "r") as f:
        content = f.read()
    
    endpoint1 = "https://api.clickhouse.cloud/v1/organizations/${CH_ORG_ID}/services/${CH_SERVICE_ID}/backupConfiguration"
    endpoint2 = "https://api.clickhouse.cloud/v1/organizations/$CH_ORG_ID/services/$CH_SERVICE_ID/backupConfiguration"
    assert endpoint1 in content or endpoint2 in content, \
        f"Expected curl to target {endpoint1} or {endpoint2}, but it was not found in the script."

def test_script_uses_basic_auth():
    """Priority 3 fallback: verify Basic Auth is used."""
    with open(SCRIPT_FILE, "r") as f:
        content = f.read()
    
    has_auth = "-u" in content or "--user" in content
    has_creds = "${CH_API_KEY_ID}:${CH_API_KEY_SECRET}" in content or "$CH_API_KEY_ID:$CH_API_KEY_SECRET" in content
    
    assert has_auth and has_creds, \
        "Expected script to use Basic Auth (-u or --user) with $CH_API_KEY_ID:$CH_API_KEY_SECRET."

def test_script_sends_patch_request():
    """Priority 3 fallback: verify HTTP method."""
    with open(SCRIPT_FILE, "r") as f:
        content = f.read()
    
    assert "-X PATCH" in content or "--request PATCH" in content, \
        "Expected script to send a PATCH request."

def test_script_payload_contains_schedule_and_retention():
    """Priority 3 fallback: verify JSON payload."""
    with open(SCRIPT_FILE, "r") as f:
        content = f.read()
    
    # Simple substring checks to ensure the JSON payload is constructed
    assert "startTime" in content, "Expected 'startTime' field in the JSON payload."
    assert "00:00" in content, "Expected '00:00' value for 'startTime' in the JSON payload."
    assert "retention" in content, "Expected 'retention' field in the JSON payload."
    assert "7" in content, "Expected '7' value for 'retention' in the JSON payload."
