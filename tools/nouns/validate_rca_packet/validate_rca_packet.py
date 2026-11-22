#!/usr/bin/env python3
"""ADR 0025: validate RCA packet JSON (schema + no-blame climb rules + fix-net rules)."""

from __future__ import annotations

BOUNDARY = "bba-emit"


import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = ROOT / "integrity" / "schemas" / "rca-packet.schema.json"

BLAME_ONLY = [
    re.compile(r"^\s*(the\s+)?agent\s+(caused|failed|is\s+at\s+fault)", re.I),
    re.compile(r"^\s*human\s+error\s*$", re.I),
    re.compile(r"^\s*operator\s+fault\s*$", re.I),
    re.compile(r"^\s*developer\s+mistake\s*$", re.I),
]

# ADR 0025 decisions 2-3 (as amended by ADR 0061): highest level first.
LEVELS = ("Principle", "Policy", "Standard", "Rule", "Codified constraint")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _schema_check(data: dict) -> list[str]:
    bad: list[str] = []
    if data.get("schema") != 1:
        bad.append("schema must be 1")
    for key in ("defect_summary", "unsuitable_process", "climb_steps", "repo_touch"):
        if key not in data:
            bad.append(f"missing {key}")
    climb = data.get("climb_steps")
    if not isinstance(climb, list) or not climb:
        bad.append("climb_steps must be non-empty array")
    touch = data.get("repo_touch")
    if not isinstance(touch, dict):
        bad.append("repo_touch must be object")
        return bad
    for key in ("adr_ids", "rule_ids", "gate_ids"):
        if not isinstance(touch.get(key), list):
            bad.append(f"repo_touch.{key} must be an array (schema)")
    if not isinstance(touch.get("belief"), str):
        bad.append("repo_touch.belief must be a string (schema)")
    belief = str(touch.get("belief", "")).strip()
    adr_ids = touch.get("adr_ids") or []
    rule_ids = touch.get("rule_ids") or []
    gate_ids = touch.get("gate_ids") or []
    if not belief and not adr_ids and not rule_ids and not gate_ids:
        bad.append("repo_touch must cite belief and/or adr_ids/rule_ids/gate_ids")
    return bad


def _policy_check(data: dict) -> list[str]:
    bad: list[str] = []
    process = str(data.get("unsuitable_process", "")).strip()
    if not process:
        bad.append("unsuitable_process required")
        return bad
    for rx in BLAME_ONLY:
        if rx.search(process):
            bad.append("unsuitable_process must name a process, not agent/human blame only")
            break
    if re.search(r"\b(agent|human|operator|developer)\s+(caused|at fault)\b", process, re.I):
        if "process" not in process.lower() and "procedure" not in process.lower():
            bad.append("root cause must climb to process language (ADR 0025)")
    climb = data.get("climb_steps") or []
    if len(climb) < 1:
        bad.append("at least one climb step required")
    return bad


def _exception_errors(exc: object, packet_path: Path | None) -> list[str]:
    """fix.exception: an owner .approval.asc that verifies with integrity/owner-keys/ and approves this RCA record."""
    if not isinstance(exc, str) or not exc.strip():
        return ["fix.exception must be the repo path of an owner-signed .approval.asc"]
    asc = ROOT / exc
    if not asc.is_file():
        return [f"fix.exception {exc} does not exist"]
    sys.path.insert(0, str(ROOT / "tools"))
    from nouns.owner_sidecar import owner_sidecar as _owner

    _signer, fields, errors = _owner.gpg_verify_clearsigned_in_repo(ROOT, asc)
    if errors:
        return [f"fix.exception {exc} does not verify with integrity/owner-keys/: {errors[0]}"]
    bad: list[str] = []
    if fields.get("Decision") != "Accepted":
        bad.append(f"fix.exception {exc}: Decision must be Accepted")
    doc = fields.get("Document", "")
    if packet_path is not None and packet_path.name.endswith(".packet.json"):
        record = packet_path.with_name(packet_path.name[: -len(".packet.json")] + ".md")
        try:
            want = record.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            want = record.as_posix()
        if doc != want:
            bad.append(f"fix.exception {exc}: Document must be this RCA record {want}")
    target = ROOT / doc if doc else None
    if target is None or not target.is_file():
        bad.append(f"fix.exception {exc}: Document {doc!r} does not exist")
    elif hashlib.sha256(target.read_bytes()).hexdigest() != fields.get("Content-SHA256", "").lower():
        bad.append(f"fix.exception {exc}: Content-SHA256 does not match {doc}")
    return bad


def _fix_net_check(data: dict, packet_path: Path | None = None) -> list[str]:
    """ADR 0025 d2-d3: name the failed level, pin the area's written target, fix at or above the failed level,
    and retire at least what the fix adds unless the owner signed an exception."""
    bad: list[str] = []
    failed = data.get("failed_level")
    if failed not in LEVELS:
        bad.append(f"failed_level must be one of {', '.join(LEVELS)}: name the level that failed")
    dd = data.get("domain_definition")
    if not isinstance(dd, dict) or not str(dd.get("path", "")).strip() or not _SHA256.match(str(dd.get("sha256", ""))):
        bad.append("domain_definition must pin the area's written target: {path, sha256}")
    else:
        target = ROOT / str(dd["path"])
        if not target.is_file():
            bad.append(f"domain_definition.path {dd['path']} does not exist")
        elif hashlib.sha256(target.read_bytes()).hexdigest() != dd["sha256"]:
            bad.append(f"domain_definition.sha256 does not match {dd['path']}: judge the fix against the current text")
    fix = data.get("fix")
    if not isinstance(fix, dict):
        bad.append("fix must be an object: {level, adds, retires} (plus exception when it adds more than it retires)")
        return bad
    level = fix.get("level")
    if level not in LEVELS:
        bad.append(f"fix.level must be one of {', '.join(LEVELS)}")
    elif failed in LEVELS and LEVELS.index(level) > LEVELS.index(failed):
        bad.append(f"fix.level {level} is below failed_level {failed}: fix the level that failed")
    adds, retires = fix.get("adds"), fix.get("retires")
    if not isinstance(adds, list) or not isinstance(retires, list):
        bad.append("fix.adds and fix.retires must be arrays of the rules, checks and state holders added and retired")
        return bad
    if len(adds) > len(retires):
        if "exception" in fix:
            bad.extend(_exception_errors(fix.get("exception"), packet_path))
        else:
            bad.append(
                f"fix adds {len(adds)} and retires {len(retires)}: list what it retires, "
                "or attach the owner's signed exception (fix.exception)"
            )
    return bad


def validate_data(data: dict, packet_path: Path | None = None) -> list[str]:
    return _schema_check(data) + _policy_check(data) + _fix_net_check(data, packet_path)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate-rca-packet.py <path-to-rca-packet.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1]).resolve()
    if not path.is_file():
        print(f"RCA_PACKET:NOT_MET missing {path}", file=sys.stderr)
        return 1
    if not SCHEMA.is_file():
        print("RCA_PACKET:NOT_MET missing integrity/schemas/rca-packet.schema.json", file=sys.stderr)
        return 1
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"RCA_PACKET:NOT_MET invalid JSON: {exc}", file=sys.stderr)
        return 1
    bad = validate_data(data, path)
    if bad:
        print("RCA_PACKET:NOT_MET", file=sys.stderr)
        for item in bad:
            print(f"  - {item}", file=sys.stderr)
        return 1
    print("RCA_PACKET:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
