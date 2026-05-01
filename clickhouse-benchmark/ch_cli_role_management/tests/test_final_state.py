import os
import stat

def test_script_exists_and_executable():
    script_path = "/home/user/ch-task/manage.sh"
    assert os.path.exists(script_path), "manage.sh does not exist"
    
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), "manage.sh is not executable"

def test_script_content():
    script_path = "/home/user/ch-task/manage.sh"
    with open(script_path, "r") as f:
        content = f.read()
    
    assert "clickhousectl cloud" in content, "Script does not contain clickhousectl cloud commands"
    assert "--json" in content, "Script does not use --json flag"
    assert "invitation create" in content, "Script does not create invitation"
    assert "key create" in content, "Script does not create key"
    assert "$1" in content or "${1}" in content, "Script does not use first argument"
    assert "$2" in content or "${2}" in content, "Script does not use second argument"
    assert "$3" in content or "${3}" in content, "Script does not use third argument"
