"""Landmine ADR 0064: work-queue.json is not lifecycle SSOT."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "requirements-sync-pending"


def main() -> int:
    dash = (ROOT / "tools/nouns/dashboard/dashboard.py").read_text(encoding="utf-8")
    if "work-queue.json" in dash:
        print("ASSERT:FAIL dashboard still names work-queue.json")
        return 1
    trap = FIXTURE / ".nlc" / "work-queue.json"
    if not trap.is_file():
        print("ASSERT:FAIL missing work-queue.json trap fixture")
        return 1
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_compliance import verify_fast_blockers

    blockers = verify_fast_blockers(FIXTURE.resolve())
    if not blockers or not any("requirements-sync" in b for b in blockers):
        print("ASSERT:FAIL trap json must not hide session Sync-Pending")
        for item in blockers:
            print(f"  {item}")
        return 1
    print("ASSERT:PASS work-queue.json is not SSOT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
