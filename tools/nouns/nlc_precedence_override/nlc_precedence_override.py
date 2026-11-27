"""Write integrity/precedence-overrides.json (ADR 0012)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REL = "integrity/precedence-overrides.json"


def load_overrides(path: Path) -> dict:
    if not path.is_file():
        return {"schema": 1, "adr": "0012", "overrides": []}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return {"schema": 1, "adr": "0012", "overrides": []}
    payload.setdefault("schema", 1)
    payload.setdefault("adr", "0012")
    payload.setdefault("overrides", [])
    return payload


def upsert(
    payload: dict,
    *,
    a: str,
    b: str,
    winner: str,
    key: str,
) -> dict:
    rows = list(payload.get("overrides") or [])
    kept = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        pair = {row.get("a"), row.get("b")}
        if pair == {a, b} or (key and row.get("conflict_key") == key):
            continue
        kept.append(row)
    kept.append({"a": a, "b": b, "winner": winner, "conflict_key": key})
    payload["overrides"] = kept
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", required=True)
    parser.add_argument("--b", required=True)
    parser.add_argument("--winner", required=True)
    parser.add_argument("--key", default="")
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args(argv)
    if args.winner not in {args.a, args.b}:
        print("OVERRIDE:NOT_MET winner must be --a or --b")
        return 1
    root = Path(args.root).resolve()
    path = root / REL
    payload = load_overrides(path)
    payload = upsert(
        payload, a=args.a, b=args.b, winner=args.winner, key=args.key
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"OVERRIDE:MET wrote {REL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
