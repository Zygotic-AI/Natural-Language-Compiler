"""Known-bad: --local outside a git worktree is INSTALL:NOT_MET."""

from __future__ import annotations

BOUNDARY = "bba-emit"

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
    with tempfile.TemporaryDirectory(prefix="nlc-nolocal-") as tmp:
        cwd = Path(tmp) / "not-a-repo"
        cwd.mkdir()
        env = os.environ.copy()
        env["HOME"] = str(Path(tmp) / "home")
        env["USERPROFILE"] = env["HOME"]
        env["NLC_INSTALL_SCOPE"] = "local"
        env["CI"] = "1"
        proc = subprocess.run(
            ["bash", str(EXECUTE), "--local"],
            cwd=str(cwd),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        if proc.returncode == 0:
            print("ASSERT:FAIL local install succeeded outside a repo\n", out[-800:])
            return 1
        if "What's wrong:" not in out:
            print("ASSERT:FAIL missing interview gap copy\n", out[-800:])
            return 1
        if "INSTALL:NOT_MET local install without a repo" not in out:
            print("ASSERT:FAIL missing NOT_MET token\n", out[-800:])
            return 1
    print("ASSERT:PASS local install without a repo is NOT_MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
