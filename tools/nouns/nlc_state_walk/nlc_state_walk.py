"""Upward lifecycle walk (ADR 0065): compare fingerprints, write parent headers."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
from pathlib import Path

from nouns.document_header.document_header import (
    fingerprint_bytes,
    header_fields,
    write_header_field,
)

ROOT = Path(__file__).resolve().parents[3]
TYPE_DEP = "integrity/type-dependency.json"


def load_type_rules(root: Path) -> dict[str, list[str]]:
    payload = json.loads((root / TYPE_DEP).read_text(encoding="utf-8"))
    types = payload.get("types") or {}
    out: dict[str, list[str]] = {}
    for name, row in types.items():
        if isinstance(row, dict):
            deps = row.get("depends_on") or []
            out[str(name)] = [str(item) for item in deps if item]
    return out


def iter_governed(root: Path) -> list[Path]:
    paths: list[Path] = []
    adrs = root / "adrs"
    if adrs.is_dir():
        paths.extend(sorted(adrs.glob("[0-9][0-9][0-9][0-9]-*.md")))
    session = root / ".nlc" / "compile-guide-session.md"
    if session.is_file():
        paths.append(session)
    goals = root / "goals"
    if goals.is_dir():
        for path in sorted(goals.glob("**/execute.sh")):
            sibling = path.parent / "README.md"
            if sibling.is_file():
                paths.append(sibling)
    return paths


def child_paths(root: Path, parent: Path, rules: dict[str, list[str]]) -> list[Path]:
    text = parent.read_text(encoding="utf-8")
    fields = header_fields(text)
    raw = fields.get("Depends-On", "")
    found: list[Path] = []
    for part in [p.strip() for p in raw.split(",") if p.strip()]:
        path = (root / part).resolve()
        if path.is_file():
            found.append(path)
    parent_type = fields.get("Nlc-Type", "adr" if parent.parent.name == "adrs" else "")
    wanted = set(rules.get(parent_type, []))
    if wanted:
        for other in iter_governed(root):
            if other.resolve() == parent.resolve():
                continue
            other_type = header_fields(other.read_text(encoding="utf-8")).get("Nlc-Type", "")
            if other_type in wanted:
                found.append(other)
    return found


def walk(root: Path) -> list[str]:
    """Write Fingerprint headers. If a child status left Accepted, mark parent Status stale."""
    rules = load_type_rules(root)
    notes: list[str] = []
    for parent in iter_governed(root):
        body = parent.read_bytes()
        digest = fingerprint_bytes(body)
        write_header_field(parent, "Fingerprint", digest)
        dropped = []
        for child in child_paths(root, parent, rules):
            status = header_fields(child.read_text(encoding="utf-8")).get("Status", "")
            if status.lower() not in {"accepted", ""}:
                dropped.append(child.relative_to(root).as_posix())
        if dropped:
            write_header_field(parent, "Status", "stale")
            notes.append(f"{parent.relative_to(root).as_posix()}: child left Accepted: {', '.join(dropped)}")
    return notes


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    if not (root / TYPE_DEP).is_file():
        print("RESULT:NOT_MET missing integrity/type-dependency.json")
        return 1
    notes = walk(root)
    for line in notes:
        print(f"WALK {line}")
    print("STATE_WALK:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
