"""Known-good: hub install MET when ~/.agents/skills already has failing foreign skills.

GitHub issue 67: post-install author check must grade the hub copied tree
(goals/hub_install/execute.sh staging copy), not every skill under the
shared ~/.agents/skills directory (including a symlink into another project).
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXECUTE = ROOT / "goals" / "hub_install" / "execute.sh"
FOREIGN_SKILL_BODY = """---
name: abbie-command
description: Use when invoking /abbie-command or working with get_template, run_model,
  run_report, or related Abbie tools.
---

# abbie-command

See [prompts](../prompts/README.md).
"""


def _write_foreign_skill(skill_dir: Path) -> Path:
    skill_dir.mkdir(parents=True, exist_ok=True)
    path = skill_dir / "SKILL.md"
    path.write_text(FOREIGN_SKILL_BODY, encoding="utf-8")
    return path


def _install_env(home: Path, store: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["USERPROFILE"] = str(home)
    env["NLC_INSTALL_ROOT"] = str(store)
    env.pop("NLC_SKIP_VERIFY", None)
    env.pop("NLC_REF", None)
    env.pop("NLC_VERSION", None)
    return env


def _run_install(home: Path, store: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(EXECUTE)],
        cwd=str(ROOT),
        env=_install_env(home, store),
        capture_output=True,
        text=True,
        check=False,
    )


def _assert_install_ok(label: str, home: Path, proc: subprocess.CompletedProcess[str]) -> str | None:
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        return f"{label}: install exit {proc.returncode}\n{out[-1600:]}"
    if "INSTALL:NOT_MET" in out:
        return f"{label}: INSTALL:NOT_MET in output\n{out[-1600:]}"
    if "SKILL_AUTHOR:MET" not in out:
        return f"{label}: missing SKILL_AUTHOR:MET\n{out[-1600:]}"
    if "VIOLATION frontmatter-yaml" in out or "VIOLATION in-skill-links" in out:
        return f"{label}: author check still graded foreign skills\n{out[-1600:]}"
    planit = home / ".agents" / "skills" / "planit" / "SKILL.md"
    foreign = home / ".agents" / "skills" / "abbie-command" / "SKILL.md"
    if not planit.is_file():
        return f"{label}: hub planit skill missing after overlay ({planit})"
    if not foreign.is_file():
        return f"{label}: foreign skill missing after overlay ({foreign})"
    return None


def _test_symlink_dest(base: Path) -> str | None:
    home = base / "symlink-home"
    store = base / "symlink-store"
    foreign_root = base / "fiquants" / "ai" / "skills"
    _write_foreign_skill(foreign_root / "abbie-command")
    agents = home / ".agents"
    agents.mkdir(parents=True)
    (home / ".agents" / "skills").symlink_to(foreign_root)
    proc = _run_install(home, store)
    return _assert_install_ok("symlink-dest", home, proc)


def _test_sibling_dir(base: Path) -> str | None:
    home = base / "sibling-home"
    store = base / "sibling-store"
    skills = home / ".agents" / "skills"
    _write_foreign_skill(skills / "abbie-command")
    proc = _run_install(home, store)
    return _assert_install_ok("sibling-dir", home, proc)


def main() -> int:
    if not EXECUTE.is_file():
        print("ASSERT:FAIL missing goals/hub_install/execute.sh")
        return 1
    with tempfile.TemporaryDirectory(prefix="nlc-install-foreign-skills-") as raw:
        base = Path(raw)
        for err in (_test_symlink_dest(base), _test_sibling_dir(base)):
            if err:
                print(f"ASSERT:FAIL {err}")
                return 1
    print("ASSERT:PASS install MET with foreign skills in ~/.agents/skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
