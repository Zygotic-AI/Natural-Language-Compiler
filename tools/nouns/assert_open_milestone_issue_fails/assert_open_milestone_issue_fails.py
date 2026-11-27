"""Landmine ADR 0061: open milestone issues are named."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nouns.hub_release.hub_release import milestone_open_issues

    errors = milestone_open_issues(
        "0.10.0",
        issues=[{"number": 42, "title": "Open work"}],
    )
    joined = " ".join(errors)
    if not errors or "#42" not in joined or "Open work" not in joined:
        print("ASSERT:FAIL expected named open milestone issue")
        print(joined)
        return 1
    print("ASSERT:PASS open milestone issues are named")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
