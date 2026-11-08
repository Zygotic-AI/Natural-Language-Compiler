"""Current ADRs live in adrs/; previous bytes live in adrs/history/ (ADR 0059)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import re
import sys
from pathlib import Path

_CURRENT = re.compile(r"^(\d{4})-.+\.md$")
_HISTORY = re.compile(r"^(\d{4})-.+-(\d+)\.md$")
_STATUS = re.compile(
    r"^-?\s*(?:\*\*)?Status(?:\*\*)?:\s*(?:\*\*)?\s*(.+)$",
    re.I | re.M,
)
_MOVED = frozenset(
    {"rejected", "superseded", "revoked", "removed", "deprecated"}
)


def current_adr_paths(adrs_dir: Path) -> list[Path]:
    if not adrs_dir.is_dir():
        return []
    return sorted(
        path
        for path in adrs_dir.glob("*.md")
        if _CURRENT.match(path.name)
    )


def history_adr_paths(history_dir: Path) -> list[Path]:
    if not history_dir.is_dir():
        return []
    return sorted(path for path in history_dir.glob("*.md") if path.name != "README.md")


def read_status(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = _STATUS.search(text)
    if not match:
        return ""
    return match.group(1).split()[0].strip("*").strip()


def adr_history_errors(root: Path) -> list[str]:
    adrs = root / "adrs"
    if not adrs.is_dir():
        return []
    errors: list[str] = []
    for path in current_adr_paths(adrs):
        status = read_status(path).lower()
        if status in _MOVED:
            errors.append(
                f"{path.relative_to(root).as_posix()}: status {read_status(path)} must live in adrs/history/"
            )
    history = adrs / "history"
    for path in history_adr_paths(history):
        if not _HISTORY.match(path.name):
            errors.append(
                f"{path.relative_to(root).as_posix()}: history filename must be NNNN-slug-REVISION.md"
            )
    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
    if (root / "adrs").is_dir():
        scan_root = root
    elif root.name == "adrs":
        scan_root = root.parent
    else:
        print("RESULT:MET")
        return 0
    errors = adr_history_errors(scan_root)
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
