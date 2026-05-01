import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_migrations_sql_exists():
    sql_path = os.path.join(PROJECT_DIR, "migrations.sql")
    assert os.path.isfile(sql_path), f"Migrations file {sql_path} does not exist."

def test_migrations_sql_content():
    sql_path = os.path.join(PROJECT_DIR, "migrations.sql")
    with open(sql_path) as f:
        content = f.read()
    assert "CREATE TABLE" in content, "Expected CREATE TABLE in migrations.sql."
    assert "ALTER TABLE" in content, "Expected ALTER TABLE in migrations.sql."
