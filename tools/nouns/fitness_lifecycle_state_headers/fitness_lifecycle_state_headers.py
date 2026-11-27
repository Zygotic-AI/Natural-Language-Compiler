"""ADR 0064: those four .nlc JSON names are not lifecycle SSOT."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    errors: list[str] = []
    dash = (ROOT / "tools/nouns/dashboard/dashboard.py").read_text(encoding="utf-8")
    if "work-queue.json" in dash:
        errors.append("dashboard still names work-queue.json")
    if "compile_guide_session" not in dash:
        errors.append("dashboard must import compile_guide_session")
    adr = (ROOT / "adrs/0019-guided-orchestration.md").read_text(encoding="utf-8")
    if "does not authorize" not in adr:
        errors.append("0019 must not authorize the four json files")
    session = ROOT / "tools/nouns/compile_guide_session/compile_guide_session.py"
    if not session.is_file():
        errors.append("missing compile_guide_session")
    for item in errors:
        print(f"VIOLATION {item}")
    if errors:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
