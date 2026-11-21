"""Landmine: untracked digest-eligible file must fail hub last-pass-fresh."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROBE_REL = "docs/rca/_porcelain-refuse-probe.txt"


def _run(argv: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, check=False)


def main() -> int:
    leftover = ROOT / PROBE_REL
    leftover.unlink(missing_ok=True)

    tmp = Path(tempfile.mkdtemp(prefix="nlc-porcelain-"))
    shutil.rmtree(tmp)
    added = _run(["git", "worktree", "add", "--detach", str(tmp), "HEAD"], ROOT)
    if added.returncode != 0:
        print("ASSERT:FAIL cannot add disposable worktree")
        print((added.stderr or added.stdout or "")[-600:])
        return 1
    try:
        probe = tmp / PROBE_REL
        probe.parent.mkdir(parents=True, exist_ok=True)
        probe.write_text("untracked porcelain refuse probe\n", encoding="utf-8")
        proc = _run(
            [sys.executable, str(tmp / "tools" / "fitness-findings-last-pass-fresh.py")],
            tmp,
        )
    finally:
        _run(["git", "worktree", "remove", "--force", str(tmp)], ROOT)
        shutil.rmtree(tmp, ignore_errors=True)

    combined = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0:
        print("ASSERT:FAIL last-pass-fresh must NOT_MET on an untracked file")
        print(combined[-600:])
        return 1
    if "git status --porcelain is not empty" not in combined:
        print("ASSERT:FAIL dirty-tree fail must name git status --porcelain")
        print(combined[-600:])
        return 1
    if "Reproduce:" not in combined:
        print("ASSERT:FAIL dirty-tree fail must print Reproduce:")
        print(combined[-600:])
        return 1
    print("ASSERT:PASS untracked file fails last-pass-fresh porcelain refuse")
    return 0


if __name__ == "__main__":
    sys.exit(main())
