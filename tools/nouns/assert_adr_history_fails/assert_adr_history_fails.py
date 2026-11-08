"""Landmine: a rejected ADR left in adrs/ must fail fitness-adr-history."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PY = sys.executable
FITNESS = ROOT / "tools" / "fitness-adr-history.py"


def _run(tree: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [PY, str(FITNESS), str(tree)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tree = Path(td)
        adrs = tree / "adrs"
        adrs.mkdir()
        (adrs / "0001-sample.md").write_text(
            "# ADR 0001\n\n- Status: Rejected\n\n## Decision\n\nx\n",
            encoding="utf-8",
        )
        code, out = _run(tree)
        if code == 0 or "RESULT:NOT_MET" not in out:
            print("ASSERT:FAIL current rejected ADR must NOT_MET")
            print(out)
            return 1
        (adrs / "0001-sample.md").unlink()
        history = adrs / "history"
        history.mkdir()
        (history / "0001-sample-1.md").write_text(
            "# ADR 0001\n\n- Status: Rejected\n\n## Decision\n\nx\n",
            encoding="utf-8",
        )
        (adrs / "0002-live.md").write_text(
            "# ADR 0002\n\n- Status: Accepted\n- Revision: 1\n\n## Decision\n\ny\n",
            encoding="utf-8",
        )
        code, out = _run(tree)
        if code != 0 or "RESULT:MET" not in out:
            print("ASSERT:FAIL history copy plus current accepted must MET")
            print(out)
            return 1
    print("ASSERT:PASS rejected current ADR is refused")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
