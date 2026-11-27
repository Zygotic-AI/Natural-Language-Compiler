"""Compile-guide session document (ADR 0019 / 0064). Replaces the four .nlc JSON state files."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
from pathlib import Path

from nouns.document_header.document_header import header_fields, set_header_field

SESSION_REL = ".nlc/compile-guide-session.md"
TEMPLATE = """# Compile-guide session

- Status: idle
- Nlc-Type: compile-guide-session
- Sync-Pending: no
- Last-Requirement-Change:
- Pipeline-Stage:
- Fingerprint:

Session resume for interview / regen / ratify. Lifecycle state lives in this header (ADR 0064).

## Items

```json
[]
```
"""
_JSON_FENCE = "```json"
_FENCE_END = "```"


def session_path(root: Path) -> Path:
    return root / SESSION_REL


def ensure_session(root: Path) -> Path:
    path = session_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file():
        path.write_text(TEMPLATE, encoding="utf-8")
    return path


def _read(root: Path) -> str:
    path = session_path(root)
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def _write(root: Path, text: str) -> None:
    path = ensure_session(root)
    path.write_text(text, encoding="utf-8")


def fields(root: Path) -> dict[str, str]:
    return header_fields(_read(root))


def sync_pending(root: Path) -> bool:
    value = fields(root).get("Sync-Pending", "no").strip().lower()
    return value in {"yes", "true", "1"}


def set_sync_pending(root: Path, pending: bool, change: str = "") -> None:
    text = _read(root) or TEMPLATE
    text = set_header_field(text, "Sync-Pending", "yes" if pending else "no")
    if change:
        text = set_header_field(text, "Last-Requirement-Change", change)
        text = set_header_field(text, "Status", "in-progress")
    elif not pending:
        text = set_header_field(text, "Status", "idle")
    _write(root, text)


def last_requirement_change(root: Path) -> str:
    return fields(root).get("Last-Requirement-Change", "").strip()


def load_items(root: Path) -> list[dict]:
    text = _read(root)
    start = text.find(_JSON_FENCE)
    if start < 0:
        return []
    start = text.find("\n", start)
    end = text.find(_FENCE_END, start + 1)
    if start < 0 or end < 0:
        return []
    raw = text[start:end].strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return [row for row in data if isinstance(row, dict) and row.get("id") and row.get("stage")]


def save_items(root: Path, items: list[dict]) -> None:
    text = _read(root) or TEMPLATE
    blob = json.dumps(items, indent=2)
    start = text.find(_JSON_FENCE)
    if start < 0:
        text = text.rstrip() + f"\n\n## Items\n\n{_JSON_FENCE}\n{blob}\n{_FENCE_END}\n"
        _write(root, text)
        return
    line_end = text.find("\n", start)
    end = text.find(_FENCE_END, line_end + 1)
    if line_end < 0 or end < 0:
        _write(root, text.rstrip() + f"\n\n{_JSON_FENCE}\n{blob}\n{_FENCE_END}\n")
        return
    new = text[: line_end + 1] + blob + "\n" + text[end:]
    _write(root, new)
