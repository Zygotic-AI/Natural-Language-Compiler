"""Landmine: untracked digest-eligible file must fail hub last-pass-fresh."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROBE_REL = "docs/rca/_porcelain-refuse-probe.txt"
PROBE = ROOT / PROBE_REL
FITNESS = ROOT / "tools" / "fitness-findings-last-pass-fresh.py"


def main() -> int:
    try:
        PROBE.write_text("untracked porcelain refuse probe\n", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(FITNESS)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
    finally:
        PROBE.unlink(missing_ok=True)
    combined = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0:
        print("ASSERT:FAIL last-pass-fresh must NOT_MET on an untracked file")
        print(combined[-600:])
        return 1
    if "git status --porcelain is not empty" not in combined:
        print("ASSERT:FAIL dirty-tree fail must name git status --porcelain")
        print(combined[-600:])
        return 1
    if "Reproduce:" not in combined:
        print("ASSERT:FAIL dirty-tree fail must print Reproduce:")
        print(combined[-600:])
        return 1
    print("ASSERT:PASS untracked file fails last-pass-fresh porcelain refuse")
    return 0


if __name__ == "__main__":
    sys.exit(main())
