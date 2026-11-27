"""Release goal (ADR 0048 goal shape). Checks ADR 0061, then the thin step verbs."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REPO = "Zygotic-AI/Natural-Language-Compiler"
USAGE = "usage: ./release validate|sign [--armor FILE]|main|tag|gates"
VERSION_REL = "integrity/nlc-version.json"


def version_of(root: Path) -> str:
    return json.loads((root / VERSION_REL).read_text(encoding="utf-8"))["version"]


def _gh_json(args: list[str]) -> tuple[int, object, str]:
    proc = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    if proc.returncode != 0:
        return proc.returncode, None, err or out
    try:
        return 0, json.loads(out) if out else None, ""
    except json.JSONDecodeError:
        return 1, None, "gh output was not JSON"


def milestone_open_issues(
    version: str,
    *,
    issues: list[dict] | None = None,
    gh_error: str | None = None,
) -> list[str]:
    """Return error lines naming each open milestone issue. Empty means the gate passes."""
    if gh_error:
        return [f"0061.1 milestone issues: cannot list issues ({gh_error})"]
    rows = issues or []
    named = []
    for row in rows:
        number = row.get("number")
        title = row.get("title") or ""
        named.append(f"#{number} {title}".strip())
    if named:
        return [
            "0061.1 milestone issues: open issues remain for this milestone: "
            + "; ".join(named)
        ]
    return []


def list_open_milestone_issues(root: Path) -> tuple[list[dict], str]:
    """GitHub issues on the milestone whose title contains this release version."""
    ver = version_of(root)
    code, payload, err = _gh_json(
        ["api", f"repos/{REPO}/milestones", "--jq", "."]
    )
    if code != 0 or not isinstance(payload, list):
        return [], err or "milestones list failed"
    match = None
    for row in payload:
        if not isinstance(row, dict):
            continue
        title = str(row.get("title") or "")
        if ver in title or f"v{ver}" in title:
            match = row
            break
    if match is None:
        return [], f"no GitHub milestone title contains {ver}"
    number = match.get("number")
    code, issues, err = _gh_json(
        [
            "issue",
            "list",
            "--repo",
            REPO,
            "--milestone",
            str(match.get("title") or number),
            "--state",
            "open",
            "--json",
            "number,title",
            "--limit",
            "100",
        ]
    )
    if code != 0 or not isinstance(issues, list):
        return [], err or "issue list failed"
    return [row for row in issues if isinstance(row, dict)], ""


def unsigned_accepted_adrs(root: Path) -> list[str]:
    """Accepted numbered ADRs with no verifying sidecar (ADR 0052 / 0061 items 2 and 10)."""
    sys.path.insert(0, str(root / "tools"))
    from nouns.document_header.document_header import header_fields

    errors: list[str] = []
    adrs = root / "adrs"
    for path in sorted(adrs.glob("[0-9][0-9][0-9][0-9]-*.md")):
        status = header_fields(path.read_text(encoding="utf-8")).get("Status", "")
        if status != "Accepted":
            continue
        sidecar = Path(str(path) + ".approval.asc")
        alt = path.with_suffix(path.suffix + ".approval.asc")
        if sidecar.is_file() or alt.is_file():
            continue
        errors.append(path.relative_to(root).as_posix())
    if errors:
        return [
            "0061.2/10 unsigned Accepted ADR: " + ", ".join(errors)
        ]
    return []


def readiness_errors(root: Path, *, issues: list[dict] | None = None, gh_error: str | None = None) -> list[str]:
    """ADR 0061 checklist. First gate is milestone issues."""
    errors: list[str] = []
    if issues is None and gh_error is None:
        issues, gh_error = list_open_milestone_issues(root)
        if gh_error:
            errors.extend(milestone_open_issues(version_of(root), gh_error=gh_error))
        else:
            errors.extend(milestone_open_issues(version_of(root), issues=issues))
    else:
        errors.extend(milestone_open_issues(version_of(root), issues=issues, gh_error=gh_error))
    errors.extend(unsigned_accepted_adrs(root))
    return errors


def print_errors(errors: list[str]) -> int:
    if not errors:
        print("RELEASE_GATES:MET")
        return 0
    print("RELEASE:REFUSED")
    for item in errors:
        print(item)
    return 1


def run_step(root: Path, argv: list[str]) -> int:
    sys.path.insert(0, str(root / "tools"))
    from nouns.nlc_release_tag_gate.nlc_release_tag_gate import main as tag_main

    return tag_main(argv)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else list(argv)
    if not args:
        print(USAGE)
        return 1
    cmd = args[0]
    if cmd == "gates":
        return print_errors(readiness_errors(ROOT))
    if cmd in {"validate", "sign", "main", "tag"}:
        # Always re-check. First gate names open milestone issues.
        errors = readiness_errors(ROOT)
        if errors:
            return print_errors(errors)
        return run_step(ROOT, args)
    print(USAGE)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
