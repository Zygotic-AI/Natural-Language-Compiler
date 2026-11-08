"""Which repo paths are in-force for public hub gates (O6).

In-force = every tracked-style path under the repo root except explicit
exclusions documented in ``integrity/HUB-IN-FORCE-EXCLUSIONS.md``.
"""

from __future__ import annotations

from pathlib import Path

# Path prefixes (posix, relative to repo root) excluded from in-force scans.
# SSOT prose: integrity/HUB-IN-FORCE-EXCLUSIONS.md
EXCLUDED_PREFIXES: tuple[str, ...] = (
    "docs/history/",
    "adrs/history/",
    "docs/rca/",
    "theory/history/",
    "examples/",
    "node_modules/",
    ".git/",
    ".venv/",
    "venv/",
    "__pycache__/",
)

# Single-segment roots excluded entirely (session / review sandboxes).
EXCLUDED_TOP_LEVEL: frozenset[str] = frozenset({"uploads"})

# Tracked paths skipped by the CG-R4 person-name scan only (not in-force exclusions).
# SSOT prose: integrity/HUB-IN-FORCE-EXCLUSIONS.md § Person-name scan exclusions
PERSON_NAME_EXCLUDED_RELS: frozenset[str] = frozenset({"CONTRIBUTORS.md"})


def is_excluded(rel_posix: str) -> bool:
    if not rel_posix or rel_posix == ".":
        return False
    top = rel_posix.split("/", 1)[0]
    if top in EXCLUDED_TOP_LEVEL:
        return True
    for prefix in EXCLUDED_PREFIXES:
        if rel_posix == prefix.rstrip("/") or rel_posix.startswith(prefix):
            return True
    return False


def is_person_name_excluded(rel_posix: str) -> bool:
    """True when CG-R4 person-name patterns must not scan this relative path."""
    return rel_posix in PERSON_NAME_EXCLUDED_RELS


def iter_in_force_files(root: Path, *, suffixes: tuple[str, ...]) -> list[Path]:
    found: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in suffixes:
            continue
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            continue
        if is_excluded(rel):
            continue
        found.append(path)
    return sorted(found)
