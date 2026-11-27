"""Release goal (ADR 0048 goal shape). Checks ADR 0061, then the thin step verbs."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REPO = "Zygotic-AI/Natural-Language-Compiler"
USAGE = "usage: ./release validate|sign [--armor FILE]|main|tag|gates"
VERSION_REL = "integrity/nlc-version.json"
ARMOR_REL = "integrity/checker-digest.sha256.approval.asc"
RELEASE_REF = re.compile(r"^release/v(\d+)\.(\d+)\.(\d+)$")


def version_file_of(root: Path) -> str:
    """Read integrity/nlc-version.json. Not used to pick the GitHub milestone."""
    return json.loads((root / VERSION_REL).read_text(encoding="utf-8"))["version"]


def release_ref_name(
    *,
    head: str | None = None,
    github_ref_name: str | None = None,
    root: Path | None = None,
) -> str:
    """Branch this process is on. Detached HEAD uses GITHUB_REF_NAME."""
    cwd = str(root or ROOT)
    if head is None:
        proc = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
        )
        head = (proc.stdout or "").strip() or "HEAD"
    if head != "HEAD":
        return head
    if github_ref_name is None:
        github_ref_name = os.environ.get("GITHUB_REF_NAME") or ""
    return github_ref_name or "HEAD"


def parse_release_version(ref: str) -> tuple[str | None, str | None]:
    """Return (X.Y.Z, None) when ref is exactly release/vX.Y.Z."""
    match = RELEASE_REF.match(ref)
    if not match:
        return None, (
            f"0061.1 saw branch {ref}; a release runs only on release/vX.Y.Z"
        )
    return f"{match.group(1)}.{match.group(2)}.{match.group(3)}", None


def _gh_json(args: list[str]) -> tuple[int, object, str]:
    attempts = [os.environ.copy()]
    stripped = {
        key: value
        for key, value in attempts[0].items()
        if key not in {"GH_TOKEN", "GITHUB_TOKEN"}
    }
    if stripped != attempts[0]:
        attempts.append(stripped)
    last_err = ""
    for env in attempts:
        proc = subprocess.run(
            ["gh", *args],
            capture_output=True,
            text=True,
            env=env,
        )
        out = (proc.stdout or "").strip()
        err = (proc.stderr or "").strip()
        if proc.returncode == 0:
            try:
                return 0, json.loads(out) if out else None, ""
            except json.JSONDecodeError:
                return 1, None, "gh output was not JSON"
        last_err = err or out
        if "403" not in last_err and "forbids access" not in last_err:
            break
    return 1, None, last_err


def milestone_open_issues(
    version: str,
    *,
    issues: list[dict] | None = None,
    gh_error: str | None = None,
) -> list[str]:
    """Return error lines naming each open milestone issue. Empty means the gate passes."""
    if gh_error:
        return [f"0061.1 milestone issues: cannot list issues ({gh_error})"]
    named = []
    for row in issues or []:
        number = row.get("number")
        title = row.get("title") or ""
        named.append(f"#{number} {title}".strip())
    if named:
        return [
            "0061.1 milestone issues: open issues remain for this milestone: "
            + "; ".join(named)
        ]
    return []


def select_milestones(rows: list, version: str) -> tuple[list[dict], str]:
    """Exactly one GitHub milestone whose title ends with ' - vX.Y.Z'."""
    suffix = f" - v{version}"
    found = [
        row
        for row in rows
        if isinstance(row, dict) and str(row.get("title") or "").endswith(suffix)
    ]
    if len(found) == 1:
        return found, ""
    titles = [str(row.get("title") or "") for row in found]
    if not found:
        seen = [str(row.get("title") or "") for row in rows if isinstance(row, dict)]
        listed = ", ".join(seen) if seen else "(none)"
        return [], (
            f"0061.1 milestone: zero GitHub milestones end with {suffix!r}; found: {listed}"
        )
    return [], (
        "0061.1 milestone: more than one GitHub milestone ends with "
        f"{suffix!r}: " + ", ".join(titles)
    )


def list_open_milestone_issues(
    version: str,
    *,
    milestones: list | None = None,
    gh_error: str | None = None,
) -> tuple[list[dict], str]:
    """Open issues on the one milestone whose title ends with ' - vX.Y.Z'."""
    if gh_error:
        return [], gh_error
    if milestones is None:
        code, payload, err = _gh_json(
            [
                "api",
                f"repos/{REPO}/milestones?state=all&per_page=100",
            ]
        )
        if code != 0 or not isinstance(payload, list):
            return [], err or "milestones list failed"
        milestones = payload
    found, err = select_milestones(milestones, version)
    if err:
        return [], err
    match = found[0]
    code, issues, err = _gh_json(
        [
            "issue",
            "list",
            "--repo",
            REPO,
            "--milestone",
            str(match.get("title") or match.get("number")),
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


def proposed_adrs(root: Path) -> list[str]:
    sys.path.insert(0, str(root / "tools"))
    from nouns.document_header.document_header import header_fields

    found: list[str] = []
    for path in sorted((root / "adrs").glob("[0-9][0-9][0-9][0-9]-*.md")):
        status = header_fields(path.read_text(encoding="utf-8")).get("Status", "")
        if status == "Proposed":
            found.append(path.relative_to(root).as_posix())
    return found


def _check_goals(root: Path) -> list[str]:
    missing: list[str] = []
    goals = root / "goals"
    if not goals.is_dir():
        return ["0061.3 goals: missing goals/"]
    for path in sorted(goals.iterdir()):
        if not path.is_dir() or path.name.startswith("."):
            continue
        if not (path / "execute.sh").is_file() and not (path / "execute.ps1").is_file():
            missing.append(path.name)
    errors: list[str] = []
    if missing:
        errors.append("0061.3 goals: missing execute.sh: " + ", ".join(missing))
    sys.path.insert(0, str(root / "tools"))
    from nouns.executable_shape.executable_shape import inventory

    _classified, unclassified = inventory(root)
    if unclassified:
        errors.append(
            "0061.3 goals: executable shape unclassified: "
            + ", ".join(unclassified[:12])
        )
    return errors


def _check_manifests(root: Path) -> list[str]:
    sys.path.insert(0, str(root / "tools"))
    from nouns.produce_package.produce_package import load_and_validate

    errors: list[str] = []
    pkg = root / ".nlc" / "produce-package.json"
    ok, _kind, reason = load_and_validate(pkg)
    if not ok:
        errors.append(f"0061.4 manifests: produce package {reason}")
    nlc = root / ".nlc"
    if nlc.is_dir():
        for path in sorted(nlc.rglob("emit-manifest.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                errors.append(f"0061.4 manifests: invalid {path.relative_to(root).as_posix()}")
                continue
            audit = data.get("audit") if isinstance(data, dict) else None
            status = audit.get("status") if isinstance(audit, dict) else ""
            if status != "pass":
                errors.append(
                    f"0061.4 manifests: {path.relative_to(root).as_posix()} audit={status or 'missing'}"
                )
    return errors


def _check_derived(root: Path) -> list[str]:
    sys.path.insert(0, str(root / "tools"))
    from nouns.fitness_derived_release_state.fitness_derived_release_state import (
        derived_release_state_errors,
    )

    drift = derived_release_state_errors(root)
    if drift:
        return ["0061.6 generated files: " + drift[0]]
    return []


def _check_r20(root: Path) -> list[str]:
    sys.path.insert(0, str(root / "tools"))
    from nouns.fitness_r20.fitness_r20 import scan_one

    hits = [
        item
        for item in scan_one(root)
        if not str(item[0]).replace("\\", "/").startswith("examples/")
    ]
    if hits:
        return [f"0061.8 charter agreement (R20): {len(hits)} disagreement(s)"]
    return []


def _check_release_profile(root: Path) -> list[str]:
    proc = subprocess.run(
        [sys.executable, str(root / "tools" / "nlc.py"), "--project", ".", "gate", "--profile", "release"],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    combined = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0 and "CI:MET" in combined:
        return []
    fail_lines = [
        line
        for line in combined.splitlines()
        if line.startswith("CI:FAIL") or line.startswith("FAILED ")
    ]
    detail = fail_lines[0] if fail_lines else f"exit {proc.returncode}"
    return [f"0061.7 gates: release profile FAIL ({detail})"]


def _check_version(root: Path, version: str | None, cmd: str) -> tuple[list[str], list[str]]:
    """Item 9. Tag and notes from later steps are pending, not MET."""
    if not version:
        return ["0061.9 version: no release version from branch"], []
    pending: list[str] = []
    fails: list[str] = []
    try:
        file_ver = version_file_of(root)
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        fails.append(f"0061.9 version file: unreadable ({exc})")
        file_ver = ""
    else:
        if file_ver != version:
            pending.append(
                f"0061.9 version file: integrity/nlc-version.json is {file_ver}, "
                f"branch is {version}; pending until validate"
            )
    notes = root / "docs" / "adoption" / f"RELEASE-v{version}.md"
    if not notes.is_file():
        pending.append(
            f"0061.9 release notes: missing docs/adoption/RELEASE-v{version}.md; pending until validate"
        )
    proc = subprocess.run(
        ["git", "tag", "--list", f"v{version}"],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    tag = (proc.stdout or "").strip()
    if tag:
        if cmd != "tag":
            pass
    else:
        pending.append(f"0061.9 tag: v{version} does not exist; pending until tag")
    return fails, pending


def _check_release_signature(root: Path) -> tuple[list[str], list[str]]:
    armor = root / ARMOR_REL
    if not armor.is_file():
        return [], ["0061.10 release signature: pending until sign"]
    return [], []


def check_item_1(
    version: str | None,
    branch_err: str | None,
    *,
    issues: list[dict] | None = None,
    gh_error: str | None = None,
) -> list[str]:
    errors: list[str] = []
    if branch_err:
        errors.append(branch_err)
        return errors
    if version is None:
        errors.append("0061.1 saw branch unknown; a release runs only on release/vX.Y.Z")
        return errors
    if issues is None and gh_error is None:
        issues, gh_error = list_open_milestone_issues(version)
    if gh_error:
        if gh_error.startswith("0061.1 "):
            errors.append(gh_error)
        else:
            errors.extend(milestone_open_issues(version, gh_error=gh_error))
    else:
        errors.extend(milestone_open_issues(version, issues=issues))
    return errors


def readiness_report(
    root: Path,
    *,
    cmd: str = "gates",
    head: str | None = None,
    github_ref_name: str | None = None,
    issues: list[dict] | None = None,
    gh_error: str | None = None,
    milestones: list | None = None,
    skip_profile: bool = False,
) -> tuple[list[str], list[str], list[str]]:
    """Evaluate every 0061 item. Returns (fails, pending, met)."""
    fails: list[str] = []
    pending: list[str] = []
    met: list[str] = []
    ref = release_ref_name(head=head, github_ref_name=github_ref_name, root=root)
    version, branch_err = parse_release_version(ref)
    if milestones is not None and gh_error is None and issues is None and version:
        issues, gh_error = list_open_milestone_issues(
            version, milestones=milestones, gh_error=None
        )

    item1 = check_item_1(
        version, branch_err, issues=issues, gh_error=gh_error
    )
    if item1:
        fails.extend(item1)
    else:
        met.append("0061.1 milestone issues")

    proposed = proposed_adrs(root)
    unsigned = unsigned_accepted_adrs(root)
    if proposed:
        fails.append(
            "0061.2 constraints: ADR not Accepted: " + ", ".join(proposed)
        )
    if unsigned:
        fails.extend(unsigned)
    if not proposed and not unsigned:
        met.append("0061.2 constraints")

    goals_err = _check_goals(root)
    if goals_err:
        fails.extend(goals_err)
    else:
        met.append("0061.3 goals")

    man_err = _check_manifests(root)
    if man_err:
        fails.extend(man_err)
    else:
        met.append("0061.4 manifests and audits")

    if proposed:
        fails.append(
            "0061.5 open questions: Proposed ADRs remain: " + ", ".join(proposed)
        )
    else:
        met.append("0061.5 open questions")

    der_err = _check_derived(root)
    if der_err:
        fails.extend(der_err)
    else:
        met.append("0061.6 generated files")

    if skip_profile:
        pending.append("0061.7 gates: NOT RUN (test skip)")
    else:
        gate_err = _check_release_profile(root)
        if gate_err:
            fails.extend(gate_err)
        else:
            met.append("0061.7 gates")

    r20_err = _check_r20(root)
    if r20_err:
        fails.extend(r20_err)
    else:
        met.append("0061.8 charter agreement")

    v_fail, v_pend = _check_version(root, version, cmd)
    fails.extend(v_fail)
    pending.extend(v_pend)
    if not v_fail and not v_pend:
        met.append("0061.9 version")

    sig_fail, sig_pend = _check_release_signature(root)
    fails.extend(sig_fail)
    pending.extend(sig_pend)
    if unsigned:
        pass
    elif not sig_fail and not sig_pend:
        met.append("0061.10 signatures")

    return fails, pending, met


def print_report(fails: list[str], pending: list[str], met: list[str]) -> int:
    if fails:
        print("RELEASE:REFUSED")
        for item in fails:
            print(item)
        for line in pending:
            print(f"PENDING {line}")
        for line in met:
            print(f"MET {line}")
        return 1
    for line in pending:
        print(f"PENDING {line}")
    for line in met:
        print(f"MET {line}")
    if pending:
        print("RELEASE_GATES:PENDING")
        return 0
    print("RELEASE_GATES:MET")
    return 0


def readiness_errors(root: Path, **kwargs) -> list[str]:
    """Fail lines only (tests)."""
    fails, _pending, _met = readiness_report(root, skip_profile=True, **kwargs)
    return fails


def run_step(root: Path, argv: list[str]) -> int:
    sys.path.insert(0, str(root / "tools"))
    from nouns.nlc_release_tag_gate.nlc_release_tag_gate import main as tag_main

    return tag_main(argv)


def main(argv: list[str] | None = None) -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_requirements import hub_tool

    hub_tool()
    args = sys.argv[1:] if argv is None else list(argv)
    if not args:
        print(USAGE)
        return 1
    cmd = args[0]
    if cmd == "gates":
        fails, pending, met = readiness_report(ROOT, cmd=cmd)
        return print_report(fails, pending, met)
    if cmd in {"validate", "sign", "main", "tag"}:
        fails, pending, met = readiness_report(ROOT, cmd=cmd)
        if fails:
            return print_report(fails, pending, met)
        print_report(fails, pending, met)
        return run_step(ROOT, args)
    print(USAGE)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
