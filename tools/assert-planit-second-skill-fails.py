#!/usr/bin/env python3
"""Landmine: a second planit/SKILL.md in the tree must fail one-owned fitness."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRA = Path("staging/_landmine_second_planit/planit/SKILL.md")


def main() -> int:
    dest = ROOT / EXTRA
    dest.parent.mkdir(parents=True, exist_ok=True)
    proc: subprocess.CompletedProcess[str]
    try:
        dest.write_text("# landmine second planit\n", encoding="utf-8")
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
        for directory in (
            ROOT / "staging" / "_landmine_second_planit" / "planit",
            ROOT / "staging" / "_landmine_second_planit",
        ):
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()
    combined = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0:
        print("ASSERT:FAIL second planit SKILL.md must fail one-owned fitness")
        print(combined[-800:])
        return 1
    if "multiple planit SKILL.md" not in combined:
        print("ASSERT:FAIL expected duplicate planit violation")
        print(combined[-800:])
        return 1
    print("ASSERT:PASS second planit SKILL.md is refused")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())