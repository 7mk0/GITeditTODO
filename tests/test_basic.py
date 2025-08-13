import json, subprocess, sys, pathlib

PY = sys.executable
DB = pathlib.Path("tasks.json")

def run(*args):
    return subprocess.run([PY, "todo.py", *args], capture_output=True, text=True, check=True)

def setup_function(_f):
    if DB.exists():
        DB.unlink()

def test_add_and_list():
    run("add", "comprare latte")
    out = run("list").stdout
    assert "comprare latte" in out

def test_done_changes_status():
    run("add", "tagliare PCD")
    run("done", "1")
    data = json.loads(DB.read_text(encoding="utf-8"))
    assert data[0]["done"] is True
