"""Landmine ADR 0062 / 0052: unsigned Accepted ADR is named and does not bind."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nouns.hub_release.hub_release import unsigned_accepted_adrs

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        adr = root / "adrs"
        adr.mkdir()
        (adr / "9999-unsigned.md").write_text(
            "# Unsigned\n\n- Status: Accepted\n",
            encoding="utf-8",
        )
        errors = unsigned_accepted_adrs(root)
        joined = " ".join(errors)
        if not errors or "9999-unsigned.md" not in joined:
            print("ASSERT:FAIL expected unsigned Accepted named")
            print(joined)
            return 1
    print("ASSERT:PASS unsigned Accepted ADR does not bind")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
