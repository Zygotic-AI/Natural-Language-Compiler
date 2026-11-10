"""Known-good: --local writes a project hub in the current git repo, not the user store."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXECUTE = ROOT / "goals" / "hub_install" / "execute.sh"


def main() -> int:
    if not EXECUTE.is_file():
        print("ASSERT:FAIL missing goals/hub_install/execute.sh")
        return 1
    with tempfile.TemporaryDirectory(prefix="nlc-local-pin-") as tmp:
        home = Path(tmp) / "home"
        repo = Path(tmp) / "app"
        home.mkdir()
        repo.mkdir()
        subprocess.run(["git", "init"], cwd=str(repo), check=True, capture_output=True)
        env = os.environ.copy()
        env["HOME"] = str(home)
        env["USERPROFILE"] = str(home)
        env["CI"] = "1"
        env["NLC_INSTALL_SCOPE"] = "local"
        env["NLC_SKIP_VERIFY"] = "1"
        env.pop("NLC_INSTALL_ROOT", None)
        proc = subprocess.run(
            ["bash", str(EXECUTE), "--local"],
            cwd=str(repo),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        if proc.returncode != 0:
            print("ASSERT:FAIL local install exit", proc.returncode, out[-1600:])
            return 1
        lock_path = repo / ".nlc" / "lock.json"
        if not lock_path.is_file():
            print("ASSERT:FAIL missing project lock")
            return 1
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        if lock.get("store") != "project" or lock.get("store_path") != ".nlc":
            print("ASSERT:FAIL lock not project", lock)
            return 1
        if not (repo / ".nlc" / "hub" / "tools" / "nlc.py").is_file():
            print("ASSERT:FAIL missing repo .nlc/hub")
            return 1
        if not (repo / ".agents" / "skills" / "planit" / "SKILL.md").is_file():
            print("ASSERT:FAIL hub skills not overlaid into the repo")
            return 1
        if (home / ".agents" / "skills" / "planit" / "SKILL.md").is_file():
            print("ASSERT:FAIL local install wrote ~/.agents/skills")
            return 1
        if (home / ".local" / "share" / "nlc" / "hub" / "tools" / "nlc.py").is_file():
            print("ASSERT:FAIL local install wrote the user-store hub")
            return 1
        if not (home / ".local" / "bin" / "nlc").is_file():
            print("ASSERT:FAIL PATH shim missing after local install")
            return 1
        if "SKILL_AUTHOR:MET" not in out:
            print("ASSERT:FAIL missing SKILL_AUTHOR:MET", out[-800:])
            return 1
    print("ASSERT:PASS local install pins the current repo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
