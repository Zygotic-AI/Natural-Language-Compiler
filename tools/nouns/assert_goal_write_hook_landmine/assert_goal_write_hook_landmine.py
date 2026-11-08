"""Landmine ADR 0058: registering a harness hook as NLC enforcement must NOT_MET."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
import tempfile
from pathlib import Path

from nouns.fitness_goal_write_hook.fitness_goal_write_hook import nlc_harness_hook_errors

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tree = Path(td)
        cursor = tree / ".cursor" / "hooks"
        cursor.mkdir(parents=True)
        (cursor / "nlc-goal-write-gate.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (tree / ".cursor" / "hooks.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "hooks": {
                        "preToolUse": [
                            {
                                "command": ".cursor/hooks/nlc-goal-write-gate.sh",
                                "matcher": "Write|Delete",
                                "failClosed": True,
                            }
                        ]
                    },
                }
            ),
            encoding="utf-8",
        )
        found = nlc_harness_hook_errors(tree)
        blob = " ".join(found)
        if not found or "preToolUse" not in blob:
            print("ASSERT:FAIL registered preToolUse must NOT_MET")
            print(found)
            return 1
        empty = Path(td) / "clean"
        empty.mkdir()
        if nlc_harness_hook_errors(empty):
            print("ASSERT:FAIL tree with no hooks must MET")
            return 1
    print("ASSERT:PASS registered harness hook is refused")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
