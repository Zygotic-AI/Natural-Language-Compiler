"""Known-good: PATH nlc that is the global shim execs ./nlc in the current repo."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LAUNCHER = ROOT / "scripts" / "nlc-launcher.sh"


def main() -> int:
    if not LAUNCHER.is_file():
        print("ASSERT:FAIL missing scripts/nlc-launcher.sh")
        return 1
    with tempfile.TemporaryDirectory(prefix="nlc-dispatch-") as tmp:
        home = Path(tmp) / "home"
        repo = Path(tmp) / "app"
        bin_dir = home / ".local" / "bin"
        bin_dir.mkdir(parents=True)
        repo.mkdir()
        shim = bin_dir / "nlc"
        shim.write_bytes(LAUNCHER.read_bytes())
        shim.chmod(shim.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        local = repo / "nlc"
        local.write_text(
            "#!/usr/bin/env bash\n"
            "echo DISPATCHED\n"
            "printf '%s\\n' \"$@\"\n"
            "exit 0\n",
            encoding="utf-8",
        )
        local.chmod(local.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        env = os.environ.copy()
        env["HOME"] = str(home)
        env["USERPROFILE"] = str(home)
        env["NLC_HUB"] = str(Path(tmp) / "should-not-use")
        nested = repo / "sub"
        nested.mkdir()
        proc = subprocess.run(
            [str(shim), "verify", "--deep", "--", "keep"],
            cwd=str(nested),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        if proc.returncode != 0:
            print("ASSERT:FAIL dispatch exit", proc.returncode, out[-800:])
            return 1
        if "DISPATCHED" not in (proc.stdout or ""):
            print("ASSERT:FAIL PATH nlc did not exec repo ./nlc\n", out[-800:])
            return 1
        lines = [line for line in (proc.stdout or "").splitlines() if line != "DISPATCHED"]
        if lines != ["verify", "--deep", "--", "keep"]:
            print("ASSERT:FAIL argv not preserved", lines)
            return 1
    print("ASSERT:PASS PATH nlc execs repo copy with the same args")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
