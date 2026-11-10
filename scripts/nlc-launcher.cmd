@echo off & python -x "%~f0" %* & exit /b %ERRORLEVEL%
# ADR 0060 PATH dispatch (Windows). python -x skips the @echo line.
import json
import os
import sys
from pathlib import Path

me = Path(sys.argv[0]).resolve()
args = sys.argv[1:]
home_bin = Path.home() / ".local" / "bin"
shims = set()
for name in ("nlc", "nlc.cmd"):
    path = home_bin / name
    try:
        if path.exists():
            shims.add(path.resolve())
    except OSError:
        pass


def run_py(script: str, extra: list[str]) -> None:
    os.execv(sys.executable, [sys.executable, script, *extra, *args])


if me in shims:
    cwd = Path.cwd().resolve()
    for directory in [cwd, *cwd.parents]:
        for name in ("nlc", "nlc.cmd"):
            candidate = directory / name
            if not candidate.is_file():
                continue
            try:
                same = candidate.resolve() == me
            except OSError:
                same = False
            if same:
                continue
            if name == "nlc.cmd":
                comspec = os.environ.get("COMSPEC", "cmd.exe")
                raise SystemExit(
                    os.spawnl(os.P_WAIT, comspec, "cmd", "/c", str(candidate), *args)
                )
            os.execv(str(candidate), [str(candidate), *args])
        lock_path = directory / ".nlc" / "lock.json"
        if not lock_path.is_file():
            continue
        try:
            data = json.loads(lock_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if str(data.get("store", "")) != "project":
            continue
        raw = str(data.get("store_path") or ".nlc")
        store = Path(raw).expanduser()
        if not store.is_absolute():
            store = directory / store
        py = store / "hub" / "tools" / "nlc.py"
        if py.is_file():
            run_py(str(py.resolve()), ["--project", str(directory)])

root = os.environ.get("NLC_INSTALL_ROOT") or str(Path.home() / ".local" / "share" / "nlc")
hub = os.environ.get("NLC_HUB") or str(Path(root) / "hub")
run_py(str(Path(hub) / "tools" / "nlc.py"), [])
