"""Landmine ADR 0065: parent Status goes stale when a child leaves Accepted."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nouns.document_header.document_header import header_fields
    from nouns.nlc_state_walk.nlc_state_walk import walk

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "integrity").mkdir()
        (root / "integrity" / "type-dependency.json").write_text(
            json.dumps({"schema": 1, "types": {"adr": {"depends_on": []}}}) + "\n",
            encoding="utf-8",
        )
        adrs = root / "adrs"
        adrs.mkdir()
        parent = adrs / "0001-parent.md"
        child = adrs / "0002-child.md"
        parent.write_text(
            "# Parent\n\n- Status: Accepted\n- Nlc-Type: adr\n"
            "- Depends-On: adrs/0002-child.md\n",
            encoding="utf-8",
        )
        child.write_text(
            "# Child\n\n- Status: Proposed\n- Nlc-Type: adr\n",
            encoding="utf-8",
        )
        walk(root)
        status = header_fields(parent.read_text(encoding="utf-8")).get("Status", "")
        if status != "stale":
            print(f"ASSERT:FAIL parent Status={status!r}, expected stale")
            return 1
    print("ASSERT:PASS child drop marks parent stale")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
