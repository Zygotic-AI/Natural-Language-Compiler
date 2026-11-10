"""ADR 0060: install scope prompt and PATH dispatch are present in launchers."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

from fitness_hub_source import read_tool

ROOT = Path(__file__).resolve().parents[3]
LANDMINES = (
    "assert-install-local-dispatch-passes.py",
    "assert-install-local-pin-passes.py",
    "assert-install-local-outside-repo-fails.py",
    "assert-install-foreign-skills-passes.py",
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    ci = read_tool("tools/ci_fitness.py")
    for name in LANDMINES:
        if name not in ci:
            violations.append(f"ci_fitness must run {name}")
    sh = read_tool("goals/hub_install/execute.sh")
    ps1 = read_tool("goals/hub_install/execute.ps1")
    launcher = read_tool("scripts/nlc-launcher.sh")
    cmd = read_tool("scripts/nlc-launcher.cmd")
    lock = read_tool("tools/nouns/lock_validate/lock_validate.py")
    for rel, text, needles in (
        (
            "goals/hub_install/execute.sh",
            sh,
            ("--local", "--global", "NLC_INSTALL_SCOPE", "/dev/tty", "rev-parse --show-toplevel", "skills_staging"),
        ),
        (
            "goals/hub_install/execute.ps1",
            ps1,
            ("NLC_INSTALL_SCOPE", "local", "SkillsStaging", "nlc-launcher.cmd"),
        ),
        (
            "scripts/nlc-launcher.sh",
            launcher,
            ("global", "exec", ".nlc/lock.json"),
        ),
        (
            "scripts/nlc-launcher.cmd",
            cmd,
            ("store", "project", "nlc.py"),
        ),
        (
            "tools/nouns/lock_validate/lock_validate.py",
            lock,
            ("project", "workspace", "user"),
        ),
    ):
        for needle in needles:
            if needle not in text:
                violations.append(f"{rel} missing {needle!r}")
    if "bash \"${skill_check_goal}\" --root \"${AGENTS_SKILLS}\"" in sh:
        violations.append("execute.sh still grades mixed AGENTS_SKILLS")
    if "--root $AgentsSkills" in ps1 and "SkillsStaging" not in ps1:
        violations.append("execute.ps1 still grades mixed AgentsSkills")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
