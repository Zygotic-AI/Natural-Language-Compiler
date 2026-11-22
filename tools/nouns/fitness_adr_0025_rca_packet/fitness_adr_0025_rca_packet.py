#!/usr/bin/env python3
"""ADR 0025 expansion: RCA packet schema + validator wired; fix-net rules run on every new RCA packet."""

from __future__ import annotations



import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = ROOT / "integrity" / "schemas" / "rca-packet.schema.json"
VALIDATOR = ROOT / "tools" / "validate-rca-packet.py"
RULES = ROOT / "rules" / "nlc-0025.json"
OK = ROOT / "examples" / "rca-packet-ok" / "rca-packet.json"
BAD = ROOT / "examples" / "rca-packet-blame-agent" / "rca-packet.json"
NET = ROOT / "examples" / "rca-packet-net-additive"
# Known-bad specimens for the fix-net rules (ADR 0025 d2-d3 as amended by ADR 0061), each with the refusal it must print.
KNOWN_BAD = (
    (NET / "kb1-c1-rev8.json", ("failed_level must be one of", "domain_definition must pin", "fix must be an object")),
    (NET / "kb2-s07.json", ("fix adds 1 and retires 0",)),
)
# RCA packets recorded on or after the #126 RCA are graded by the fix-net rules; older packets are history.
EFFECTIVE = "2026-11-21"


def _run(path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path, label in (
        (SCHEMA, "rca-packet.schema.json"),
        (VALIDATOR, "validate-rca-packet.py"),
        (RULES, "nlc-0025.json"),
        (OK, "rca-packet-ok specimen"),
    ):
        if not path.is_file():
            violations.append(f"missing {label}")
    if RULES.is_file():
        text = RULES.read_text(encoding="utf-8")
        if "expansion: rca-packet-schema" in text:
            violations.append("nlc-0025.json still lists expansion gate")
        if "validate-rca-packet.py" not in text:
            violations.append("nlc-0025.json must cite validate-rca-packet.py")
    if OK.is_file() and VALIDATOR.is_file():
        if _run(OK).returncode != 0:
            violations.append("ok specimen must MET validate-rca-packet")
    if BAD.is_file() and VALIDATOR.is_file():
        if _run(BAD).returncode == 0:
            violations.append("blame-agent specimen must NOT_MET")
    if VALIDATOR.is_file():
        for path, needles in KNOWN_BAD:
            rel = path.relative_to(ROOT).as_posix()
            if not path.is_file():
                violations.append(f"missing known-bad specimen {rel}")
                continue
            proc = _run(path)
            if proc.returncode == 0:
                violations.append(f"known-bad specimen {rel} must NOT_MET")
            for needle in needles:
                if needle not in proc.stderr:
                    violations.append(f"known-bad specimen {rel} must be refused with {needle!r}")
        for path in sorted((ROOT / "docs" / "rca").glob("*.packet.json")):
            try:
                recorded = str(json.loads(path.read_text(encoding="utf-8")).get("recorded_at", ""))
            except json.JSONDecodeError:
                recorded = EFFECTIVE
            if recorded and recorded < EFFECTIVE:
                continue
            proc = _run(path)
            if proc.returncode != 0:
                rel = path.relative_to(ROOT).as_posix()
                reasons = "; ".join(l.strip(" -") for l in proc.stderr.splitlines()[1:]) or proc.stderr.strip()
                violations.append(f"{rel} must MET validate-rca-packet: {reasons}")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

