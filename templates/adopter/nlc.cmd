@echo off & python -x "%~f0" %* & exit /b %ERRORLEVEL%
# Adopter ./nlc.cmd — ADR 0060: honor store=project, then NLC_HUB, then user store.
import json
import os
import sys
from pathlib import Path

root = Path(sys.argv[0]).resolve().parent
args = sys.argv[1:]
hub = None
lock_path = root / ".nlc" / "lock.json"
if lock_path.is_file():
    try:
        data = json.loads(lock_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        data = {}
    if str(data.get("store", "")) == "project":
        raw = str(data.get("store_path") or ".nlc")
        store = Path(raw).expanduser()
        if not store.is_absolute():
            store = root / store
        py = store / "hub" / "tools" / "nlc.py"
        if py.is_file():
            hub = store / "hub"
if hub is None and os.environ.get("NLC_HUB"):
    hub = Path(os.environ["NLC_HUB"])
if hub is None:
    hub = Path.home() / ".local" / "share" / "nlc" / "hub"
script = hub / "tools" / "nlc.py"
if not script.is_file():
    sys.stderr.write("NLC:NOT_MET install hub first or set NLC_HUB\n")
    raise SystemExit(1)
os.execv(sys.executable, [sys.executable, str(script), "--project", str(root), *args])
