"""Landmine UC1 / ADR 0021: packet required; uncompiled bind-ready must pass."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import io
import json
import sys
import tempfile
from contextlib import redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "examples" / "interview-packet-missing"
BIND_READY = ROOT / "examples" / "bind-ready-uncompiled"


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_compliance import verify_fast_blockers
    from nlc_verify import emit_verify_fail, verify_deep, verify_fast

    blockers = verify_fast_blockers(FIXTURE.resolve())
    if not blockers or not any("interview-packet" in b for b in blockers):
        print("ASSERT:FAIL expected UC1 interview-packet blocker")
        for b in blockers:
            print(f"  {b}")
        return 1

    buf = io.StringIO()
    with redirect_stderr(buf):
        emit_verify_fail(blockers, root=FIXTURE)
    text = buf.getvalue()
    if "What's wrong:" not in text or "Option:" not in text or "Example:" not in text:
        print("ASSERT:FAIL emit_verify_fail must use ADR 0018 shape")
        print(text)
        return 1
    if text.lstrip().startswith("Reproduce:"):
        print("ASSERT:FAIL emit_verify_fail must not lead with Reproduce:")
        return 1

    if not BIND_READY.is_dir():
        print(f"ASSERT:FAIL missing {BIND_READY.relative_to(ROOT)}")
        return 1
    ok, reasons = verify_fast(BIND_READY.resolve())
    if not ok:
        print(f"ASSERT:FAIL bind-ready uncompiled verify_fast should pass: {reasons}")
        return 1
    if any("fingerprint" in r.lower() for r in reasons):
        print(f"ASSERT:FAIL uncompiled tree must not demand fingerprints: {reasons}")
        return 1

    deep = verify_deep(BIND_READY.resolve(), ROOT, "0.8.0")
    if deep != 0:
        print(f"ASSERT:FAIL bind-ready uncompiled verify_deep should pass, got {deep}")
        return 1
    if (BIND_READY / ".nlc" / "verified.json").is_file():
        print("ASSERT:FAIL uncompiled verify-deep must not write fingerprints")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        tree = Path(tmp)
        (tree / ".nlc").mkdir()
        (tree / ".nlc" / "lock.json").write_text(
            json.dumps({"schema": 1, "hub": "0.8.0", "store": "user"}) + "\n",
            encoding="utf-8",
        )
        missing = verify_fast_blockers(tree)
        if not missing or not any("interview-packet" in b for b in missing):
            print("ASSERT:FAIL uncompiled tree without packet must fail UC1")
            for b in missing:
                print(f"  {b}")
            return 1
        ok_missing, _ = verify_fast(tree)
        if ok_missing:
            print("ASSERT:FAIL uncompiled tree without packet must fail verify_fast")
            return 1

    print("ASSERT:PASS verify blocks missing interview-packet (UC1)")
    return 0
