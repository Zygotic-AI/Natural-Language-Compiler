"""Read and write markdown document headers (ADR 0064)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import re
from pathlib import Path

_HEADER = re.compile(r"^-+\s*([^:]+):\s*(.*)$")
_STATUS = re.compile(
    r"^-?\s*(?:\*\*)?Status(?:\*\*)?:\s*(?:\*\*)?\s*(.+)$",
    re.I | re.M,
)


def header_fields(text: str) -> dict[str, str]:
    """Map header keys to values from leading `- Key: value` lines and Status."""
    fields: dict[str, str] = {}
    match = _STATUS.search(text)
    if match:
        fields["Status"] = match.group(1).split()[0].strip("*").strip()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        row = _HEADER.match(stripped)
        if not row:
            if stripped == "" or stripped.startswith("#"):
                continue
            if stripped.startswith("##"):
                break
            if not stripped.startswith("-"):
                if fields and stripped:
                    break
            continue
        key = row.group(1).strip().strip("*")
        fields[key] = row.group(2).strip()
    return fields


def fingerprint_bytes(body: bytes) -> str:
    """SHA-256 of document bytes (ADR 0050)."""
    return hashlib.sha256(body).hexdigest()


def set_header_field(text: str, key: str, value: str) -> str:
    """Replace or insert `- Key: value` after the title line."""
    pattern = re.compile(rf"^-\s*{re.escape(key)}:.*$", re.M)
    line = f"- {key}: {value}"
    if pattern.search(text):
        return pattern.sub(line, text, count=1)
    lines = text.splitlines(keepends=True)
    insert_at = 0
    if lines and lines[0].startswith("#"):
        insert_at = 1
        if insert_at < len(lines) and lines[insert_at].strip() == "":
            insert_at += 1
    extra = line + "\n"
    return "".join(lines[:insert_at]) + extra + "".join(lines[insert_at:])


def write_header_field(path: Path, key: str, value: str) -> None:
    """Update one header field on disk."""
    text = path.read_text(encoding="utf-8")
    path.write_text(set_header_field(text, key, value), encoding="utf-8")
