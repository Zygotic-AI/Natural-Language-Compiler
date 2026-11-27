"""ADR 0063: unique Decision-point names on current ADRs."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import re
import sys
from pathlib import Path

from nouns.document_header.document_header import header_fields

ROOT = Path(__file__).resolve().parents[3]
REGISTER = "integrity/adr-decision-points.json"
_POINT = re.compile(r"^-\s*Decision-point:\s*(.+)$", re.M)


def current_points(root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted((root / "adrs").glob("[0-9][0-9][0-9][0-9]-*.md")):
        text = path.read_text(encoding="utf-8")
        fields = header_fields(text)
        name = fields.get("Decision-point", "").strip()
        if not name:
            match = _POINT.search(text)
            name = match.group(1).strip() if match else f"ADR-{path.name[:4]}"
        rows.append(
            {
                "adr": path.name[:4],
                "decision_point": name,
                "path": path.relative_to(root).as_posix(),
            }
        )
    return rows


def overlap_errors(rows: list[dict[str, str]]) -> list[str]:
    seen: dict[str, str] = {}
    errors: list[str] = []
    for row in rows:
        name = row["decision_point"]
        if name.startswith("ADR-"):
            continue
        other = seen.get(name)
        if other:
            errors.append(f"decision-point {name!r} claimed by {other} and {row['adr']}")
        else:
            seen[name] = row["adr"]
    return errors


def write_register(root: Path, rows: list[dict[str, str]]) -> None:
    payload = {"schema": 1, "adr": "0063", "points": rows}
    (root / REGISTER).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--write"]
    root = Path(args[0]).resolve() if args else ROOT
    if "--write" in sys.argv:
        rows = current_points(root)
        write_register(root, rows)
        errors = overlap_errors(rows)
        for item in errors:
            print(f"VIOLATION {item}")
        if errors:
            print("RESULT:NOT_MET")
            return 1
        print("RESULT:MET")
        return 0
    rows = current_points(root)
    errors = overlap_errors(rows)
    register = root / REGISTER
    if register.is_file():
        payload = json.loads(register.read_text(encoding="utf-8"))
        listed = payload.get("points") if isinstance(payload, dict) else None
        if not isinstance(listed, list) or len(listed) != len(rows):
            errors.append("integrity/adr-decision-points.json drift; run with --write")
    else:
        errors.append("missing integrity/adr-decision-points.json")
    for item in errors:
        print(f"VIOLATION {item}")
    if errors:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
