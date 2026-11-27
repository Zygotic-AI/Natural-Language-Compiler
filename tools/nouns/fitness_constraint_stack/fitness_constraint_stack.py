"""ADR 0062: 0028 no longer owns policy compilation; 0062 names the stack."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    errors: list[str] = []
    stack = (ROOT / "adrs" / "0062-constraint-stack.md").read_text(encoding="utf-8")
    if "Only **codified** constraints bind" not in stack and "only **codified** constraints bind" not in stack.lower():
        if "Only **codified** constraints bind" not in stack:
            errors.append("0062 must say only codified constraints bind")
    verb = (ROOT / "adrs" / "0028-closed-atomic-verb-set-and-policy-adr-lineage.md").read_text(
        encoding="utf-8"
    )
    if "Policies become ADRs" in verb:
        errors.append("0028 still owns policy compilation")
    if "create" not in verb or "`bind`" not in verb:
        errors.append("0028 must keep the closed verb set")
    for item in errors:
        print(f"VIOLATION {item}")
    if errors:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
