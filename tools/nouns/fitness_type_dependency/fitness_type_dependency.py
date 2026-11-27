"""ADR 0065: type-dependency file and walker exist."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    errors: list[str] = []
    path = ROOT / "integrity" / "type-dependency.json"
    if not path.is_file():
        errors.append("missing integrity/type-dependency.json")
    else:
        payload = json.loads(path.read_text(encoding="utf-8"))
        types = payload.get("types")
        if not isinstance(types, dict) or "adr" not in types:
            errors.append("type-dependency.json must declare types including adr")
    walker = ROOT / "tools" / "nlc-state-walk.py"
    if not walker.is_file():
        errors.append("missing tools/nlc-state-walk.py")
    for item in errors:
        print(f"VIOLATION {item}")
    if errors:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
