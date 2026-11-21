#!/usr/bin/env python3
"""Landmine: stale planit-change-evidence must fail --check-evidence."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / ".nlc" / "planit-change-evidence.json"


def main() -> int:
    if not EVIDENCE.is_file():
        print("ASSERT:FAIL missing planit-change-evidence.json")
        return 1
    original = EVIDENCE.read_text(encoding="utf-8")
    proc: subprocess.CompletedProcess[str]
    try:
        record = json.loads(original)
        record["source_tree_sha256"] = "0" * 64
        EVIDENCE.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "fitness-planit-identity.py"),
                "--skill-only",
                "--loaded",
                ".agents/skills/planit/SKILL.md",
                "--check-evidence",
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
    finally:
        EVIDENCE.write_text(original, encoding="utf-8")
    combined = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0:
        print("ASSERT:FAIL stale planit change evidence must fail --check-evidence")
        print(combined[-800:])
        return 1
    if "Planit change evidence does not match the current tree" not in combined:
        print("ASSERT:FAIL expected stale evidence violation")
        print(combined[-800:])
        return 1
    print("ASSERT:PASS stale planit change evidence is refused")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())