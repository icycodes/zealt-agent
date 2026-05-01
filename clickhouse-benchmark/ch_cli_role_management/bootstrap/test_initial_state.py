import os

def test_initial_state():
    # The script should not exist yet
    assert not os.path.exists("/home/user/ch-task/manage.sh"), "manage.sh should not exist initially"
    # The directory should exist
    assert os.path.isdir("/home/user/ch-task"), "/home/user/ch-task directory should exist"
