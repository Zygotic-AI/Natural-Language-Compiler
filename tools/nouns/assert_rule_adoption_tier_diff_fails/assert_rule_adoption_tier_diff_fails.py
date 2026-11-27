"""Landmine ADR 0012 rev 2: different tiers still halt without an override."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "rule-adoption-tier-diff" / "rules" / "adopted.json"
TOOL = ROOT / "tools" / "check-rule-adoption.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(FIXTURE)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0 or "ADOPTION:NOT_MET" not in out:
        print("ASSERT:FAIL tier-diff conflict should ADOPTION:NOT_MET")
        print(out)
        return 1
    print("ASSERT:PASS rule-adoption-tier-diff fails adopt-time check")
    return 0
