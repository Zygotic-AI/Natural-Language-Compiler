#!/usr/bin/env python3
"""ADR 0018: interview skill documents five-part blocking shape for humans.

UC1 (#144): interview skill packet contract must match integrity/schemas/interview-packet.schema.json.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INTERVIEW = ROOT / ".agents" / "skills" / "interview" / "SKILL.md"
PROPOSER = ROOT / ".agents" / "skills" / "bbp-proposer" / "SKILL.md"
PACKET_SCHEMA = ROOT / "integrity" / "schemas" / "interview-packet.schema.json"
PACKET_SCHEMA_REF = "integrity/schemas/interview-packet.schema.json"
VALIDATOR_REF = "validate-interview-packet"
OPTIONAL_PACKET_FIELDS = frozenset({"recorded_at"})
HAND_PACKET_LIST_RE = re.compile(
    r"interview-packet\.json`?\s*\(\s*`[a-z_]+`",
    re.MULTILINE,
)


def load_schema_required(schema_path: Path = PACKET_SCHEMA) -> list[str]:
    """Return required property names from the interview packet JSON schema."""
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    required = data.get("required")
    if not isinstance(required, list) or not required:
        raise ValueError("interview-packet.schema.json missing non-empty required array")
    return [str(k) for k in required]


def interview_packet_contract_violations(text: str, required: list[str]) -> list[str]:
    """
    Fail when the skill uses a hand-written packet field list or omits schema SSOT cues.
    """
    violations: list[str] = []
    if PACKET_SCHEMA_REF not in text:
        violations.append(f"interview SKILL must cite packet schema SSOT: {PACKET_SCHEMA_REF}")
    if VALIDATOR_REF not in text:
        violations.append("interview SKILL must cite validate-interview-packet.py")
    if ".nlc/interview-packet.json" not in text:
        violations.append("interview SKILL must cite .nlc/interview-packet.json")

    if HAND_PACKET_LIST_RE.search(text):
        violations.append(
            "interview SKILL must not hand-list packet fields; cite "
            f"{PACKET_SCHEMA_REF} and validate with {VALIDATOR_REF}"
        )

    for line in text.splitlines():
        if "interview-packet.json" not in line:
            continue
        if "required" not in line and "schema.json" not in line:
            violations.append(
                "interview packet step must point at schema required keys, not a bare file path"
            )
        break

    required_set = set(required)
    if "schema" not in required_set:
        violations.append("internal: packet schema must require schema key")
    elif not re.search(r"\bschema\b", text):
        violations.append("interview SKILL must mention packet `schema` (schema: 1)")

    for key in sorted(required_set):
        if key == "bind_ready":
            continue
        if key not in text:
            violations.append(f"interview SKILL must mention required packet field: {key}")

    if re.search(r"packet (field|includes) `([a-z_]+)`", text, re.IGNORECASE):
        allowed = required_set | OPTIONAL_PACKET_FIELDS
        for tok in re.findall(r"packet (?:field|includes) `([a-z_]+)`", text, re.IGNORECASE):
            if tok not in allowed:
                violations.append(
                    f"interview SKILL documents packet field `{tok}` not in schema required or optional"
                )

    return violations


def known_bad_packet_contract_probes(required: list[str]) -> list[str]:
    """Producer emits fields the gate must reject (drifted hand list without schema: 1)."""
    drifted = (
        "When bind-ready, write `.nlc/interview-packet.json` "
        "(`outcome`, `goals`, `requirements`, `knowledge_domains`, `bind_ready: true`)"
    )
    if not interview_packet_contract_violations(drifted, required):
        return ["known-bad drifted interview skill must fail packet contract check"]
    spurious_field = (
        f"{PACKET_SCHEMA_REF}\n"
        "validate-interview-packet.py\n"
        ".nlc/interview-packet.json\n"
        "schema outcome goals requirements knowledge_domains bind_ready\n"
        "Optional packet field: `recorded_at`. Packet includes `phantom_packet_field`.\n"
    )
    if not interview_packet_contract_violations(spurious_field, required):
        return ["known-bad skill documenting non-schema packet field must fail"]
    return []


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    try:
        required = load_schema_required()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"VIOLATION cannot load packet schema: {exc}")
        print("RESULT:NOT_MET")
        return 1

    violations.extend(known_bad_packet_contract_probes(required))

    if not INTERVIEW.is_file():
        violations.append("missing .agents/skills/interview/SKILL.md")
    else:
        text = INTERVIEW.read_text(encoding="utf-8", errors="replace")
        violations.extend(interview_packet_contract_violations(text, required))
        for needle in (
            "ADR 0018",
            "plain language",
            "/interview",
            "/planit",
            "When you block",
        ):
            if needle not in text:
                violations.append(f"interview SKILL must mention: {needle}")
        for needle in ("Problem", "Ask", "Example"):
            if needle not in text:
                violations.append(f"interview SKILL must document blocking part: {needle}")

    if not PROPOSER.is_file():
        violations.append("missing bbp-proposer SKILL.md")
    elif "rule-marker" not in PROPOSER.read_text(encoding="utf-8", errors="replace"):
        violations.append("bbp-proposer must prescribe rule-marker CLI (ADR 0023)")

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