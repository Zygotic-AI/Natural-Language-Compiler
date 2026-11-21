#!/usr/bin/env python3
"""Landmine: a ~/.agents/skills/planit route must fail one-owned fitness."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBE = Path(".agents/skills/_landmine_external_planit_route.md")


def main() -> int:
    dest = ROOT / PROBE
    dest.parent.mkdir(parents=True, exist_ok=True)
    proc: subprocess.CompletedProcess[str]
    try:
        dest.write_text("route to `~/.agents/skills/planit`\n", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "fitness-planit-one-owned.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
    finally:
        if dest.is_file():
            dest.unlink()
    combined = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0:
        print("ASSERT:FAIL external Planit route must fail one-owned fitness")
        print(combined[-800:])
        return 1
    if "~/.agents/skills/planit" not in combined and "external Planit" not in combined:
        print("ASSERT:FAIL expected external Planit violation")
        print(combined[-800:])
        return 1
    print("ASSERT:PASS external Planit route is refused")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())