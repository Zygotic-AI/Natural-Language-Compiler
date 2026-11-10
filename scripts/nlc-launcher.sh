#!/usr/bin/env bash
# Installed to ~/.local/bin/nlc — runs hub CLI with NLC_HUB set.
# ADR 0060: if this process is the global PATH shim, exec ./nlc or .nlc/lock.json store=project.
set -euo pipefail
INSTALL_ROOT="${NLC_INSTALL_ROOT:-${HOME}/.local/share/nlc}"
_dispatch="$(python3 -c '
import json, os, stat, sys
from pathlib import Path
me = Path(sys.argv[1]).resolve()
home_bin = Path.home() / ".local" / "bin"
shims = []
for name in ("nlc", "nlc.cmd"):
    p = home_bin / name
    try:
        shims.append(p.resolve())
    except OSError:
        pass
if me not in shims:
    sys.exit(0)
cwd = Path.cwd().resolve()
for directory in [cwd, *cwd.parents]:
    for name in ("nlc", "nlc.cmd"):
        cand = directory / name
        if not cand.is_file():
            continue
        if name == "nlc" and not (cand.stat().st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)):
            continue
        try:
            if cand.resolve() == me:
                continue
        except OSError:
            pass
        sys.stdout.write("exec\t" + str(cand))
        sys.exit(0)
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
        sys.stdout.write("py\t" + str(py.resolve()) + "\t" + str(directory))
        sys.exit(0)
' "$0" || true)"
if [[ -n "${_dispatch}" ]]; then
  if [[ "${_dispatch}" == exec$'\t'* ]]; then
    exec "${_dispatch#exec	}" "$@"
  fi
  if [[ "${_dispatch}" == py$'\t'* ]]; then
    _rest="${_dispatch#py	}"
    _py="${_rest%%	*}"
    _proj="${_rest#*	}"
    exec python3 "${_py}" --project "${_proj}" "$@"
  fi
  echo "NLC:NOT_MET PATH nlc could not exec the repo copy" >&2
  echo "  What's wrong: dispatch target was unusable: ${_dispatch}" >&2
  echo "  Fix: run ./nlc from the repo, or reinstall the PATH command." >&2
  exit 1
fi
export NLC_HUB="${NLC_HUB:-${INSTALL_ROOT}/hub}"
exec python3 "${NLC_HUB}/tools/nlc.py" "$@"
