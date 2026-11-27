"""Agent/CI requirements sync (ADR 0019–0020). Humans use /interview."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from nouns.adr_scan import list_pending_adrs

BOUNDARY = "bba-emit"


def _pending_adr_names(root: Path) -> list[str]:
    return list_pending_adrs(root / "adrs")


def _run_check_rules(root: Path, hub: Path) -> int:
    adopted = root / "rules" / "adopted.json"
    check = hub / "tools" / "check-rule-adoption.py"
    return subprocess.run(
        [sys.executable, str(check), str(adopted)],
        cwd=str(root),
    ).returncode


def _maybe_regen_after_sync(root: Path, hub: Path) -> None:
    from nouns.compile_guide_session.compile_guide_session import last_requirement_change

    change = last_requirement_change(root)
    if not change:
        return
    script = hub / "tools" / "nlc-delta-regen.py"
    subprocess.run(
        [
            sys.executable,
            str(script),
            str(root),
            "--change",
            str(change),
            "--orchestrate",
            "--write-queue",
        ],
        cwd=str(root),
    )


def run_requirements(root: Path, hub: Path) -> int:
    pending = _pending_adr_names(root)
    if pending:
        print("Requirements unfinished — ratify in /interview first.", file=sys.stderr)
        print(f"  Waiting on: {', '.join(pending[:5])}{'…' if len(pending) > 5 else ''}", file=sys.stderr)
        return 1

    adopted = root / "rules" / "adopted.json"
    if not adopted.is_file():
        print("No adopted rules file yet — /interview drafts requirements.", file=sys.stderr)
        return 1

    code = _run_check_rules(root, hub)
    if code != 0:
        print("Rule check failed — fix in /interview.", file=sys.stderr)
        return code

    from nouns.compile_guide_session.compile_guide_session import set_sync_pending, sync_pending

    if sync_pending(root):
        _maybe_regen_after_sync(root, hub)
        set_sync_pending(root, False)

    regen = root / ".nlc" / "delta-regen-queue.json"
    if regen.is_file():
        try:
            data = json.loads(regen.read_text(encoding="utf-8"))
            steps = data.get("steps") or []
            if steps:
                print(f"Requirements synced. {len(steps)} rebuild(s) queued — /planit in agent.")
                return 0
        except json.JSONDecodeError:
            pass

    print("Requirements OK.")
    return 0
