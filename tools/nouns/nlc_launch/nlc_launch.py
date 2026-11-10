"""PATH nlc dispatch: global shim execs a repo-local copy (ADR 0060)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import stat
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from nlc_requirements import hub_tool  # noqa: E402


def global_shim_path() -> Path:
    return (Path.home() / ".local" / "bin" / "nlc").resolve()


def global_shim_cmd_path() -> Path:
    return (Path.home() / ".local" / "bin" / "nlc.cmd").resolve()


def is_global_shim(self_path: Path) -> bool:
    try:
        me = self_path.resolve()
    except OSError:
        return False
    for candidate in (global_shim_path(), global_shim_cmd_path()):
        try:
            if me == candidate:
                return True
        except OSError:
            continue
    return False


def _is_runnable_nlc(path: Path) -> bool:
    if not path.is_file():
        return False
    mode = path.stat().st_mode
    if path.suffix.lower() == ".cmd":
        return True
    return bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))


def find_local_target(cwd: Path, self_path: Path) -> tuple[str, ...] | None:
    """Return ('exec', path) or ('py', nlc_py, project) or None."""
    try:
        me = self_path.resolve()
    except OSError:
        me = self_path
    start = cwd.resolve()
    for directory in [start, *start.parents]:
        for name in ("nlc", "nlc.cmd"):
            candidate = directory / name
            if not _is_runnable_nlc(candidate):
                continue
            try:
                if candidate.resolve() == me:
                    continue
            except OSError:
                pass
            return ("exec", str(candidate))
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
            store = (directory / store)
        py = store / "hub" / "tools" / "nlc.py"
        if py.is_file():
            return ("py", str(py.resolve()), str(directory))
    return None


def main(argv: list[str] | None = None) -> int:
    hub_tool()
    args = list(sys.argv[1:] if argv is None else argv)
    cwd = Path.cwd()
    self_path = Path(args[1]).resolve() if len(args) >= 2 else Path(sys.argv[0])
    if args and args[0] == "--find-local":
        if len(args) >= 2:
            self_path = Path(args[1])
        found = find_local_target(cwd, self_path)
        if not found:
            return 1
        sys.stdout.write("\t".join(found) + "\n")
        return 0
    if args and args[0] == "--is-global":
        if len(args) >= 2:
            self_path = Path(args[1])
        return 0 if is_global_shim(self_path) else 1
    sys.stderr.write("nlc-launch: use --find-local <self> or --is-global <self>\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
