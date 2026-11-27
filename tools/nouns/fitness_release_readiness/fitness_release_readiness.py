"""ADR 0061: checklist first item is milestone issues; goal exists; no command table."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    errors: list[str] = []
    text = (ROOT / "adrs" / "0061-release-in-seven-steps.md").read_text(encoding="utf-8")
    quote = "Do we have all the issues for this milestone competed?"
    if quote not in text:
        errors.append("0061 must quote the milestone-issues item")
    if "git rev-parse --abbrev-ref HEAD" not in text:
        errors.append("0061 item 1 must say how the goal reads the branch")
    if "GITHUB_REF_NAME" not in text:
        errors.append("0061 item 1 must name GITHUB_REF_NAME for detached HEAD")
    if "nlc-version.json is not used to pick the milestone" not in text:
        errors.append("0061 item 1 must not pick the milestone from nlc-version.json")
    if "### Checklist" not in text and "Checklist" not in text:
        errors.append("0061 must be a checklist")
    if "`gh workflow run start-release.yml" in text:
        errors.append("0061 must not keep the seven-step command table")
    goal = ROOT / "goals" / "hub_release" / "execute.sh"
    if not goal.is_file():
        errors.append("missing goals/hub_release/execute.sh")
    readme = (ROOT / "goals" / "hub_release" / "README.md").read_text(encoding="utf-8")
    if quote not in readme:
        errors.append("release goal doc must quote the milestone-issues item")
    if "git rev-parse --abbrev-ref HEAD" not in readme:
        errors.append("release goal doc must define how it reads the branch")
    if "nlc-version.json is not used to pick the milestone" not in readme:
        errors.append("release goal doc must not pick the milestone from nlc-version.json")
    skill = (ROOT / ".agents" / "skills" / "release" / "SKILL.md").read_text(encoding="utf-8")
    if "hub_release" not in skill:
        errors.append("release skill must run the release goal")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    if agents.count(".agents/skills/release/SKILL.md") < 1:
        errors.append("AGENTS.md must point at the release skill")
    for item in errors:
        print(f"VIOLATION {item}")
    if errors:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
