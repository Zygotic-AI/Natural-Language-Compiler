"""The identity check hashes the loaded skill against the hub registry.

A product repo is not the registry location and is not a skip.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / ".agents" / "skills" / "planit" / "SKILL.md"
OLD_COMMAND = "python3 tools/fitness-planit-identity.py"


def _run(project: Path, loaded: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "nlc.py"),
            "--project",
            str(project),
            "planit-identity",
            "--loaded",
            str(loaded),
        ],
        cwd=str(project),
        capture_output=True,
        text=True,
        check=False,
    )


def _hub(install: Path, body: bytes) -> None:
    hub = install / "hub"
    (hub / "tools").mkdir(parents=True)
    (hub / "tools" / "nlc.py").write_text("# fixture\n", encoding="utf-8")
    registry = hub / "integrity"
    registry.mkdir(parents=True)
    digest = hashlib.sha256(body).hexdigest()
    (registry / "planit-skill-registry.json").write_text(
        json.dumps(
            {
                "schema": 1,
                "canonical_path": ".agents/skills/planit/SKILL.md",
                "content_sha256": digest,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def _adopter(root: Path, install: Path, body: bytes) -> Path:
    skill = root / ".agents" / "skills" / "planit" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_bytes(body)
    nlc = root / ".nlc"
    nlc.mkdir()
    (nlc / "lock.json").write_text(
        json.dumps(
            {"schema": 1, "hub": "0.8.0", "store": "project", "store_path": str(install)},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return skill


def main() -> int:
    text = SKILL.read_text(encoding="utf-8")
    if OLD_COMMAND in text:
        print("ASSERT:FAIL skill still names the hub-cwd identity script")
        return 1
    if "./nlc planit-identity" not in text:
        print("ASSERT:FAIL skill does not name ./nlc planit-identity")
        return 1
    good = b"loaded planit skill\n"
    bad = b"other planit skill\n"
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        install = base / "install"
        project = base / "app"
        _hub(install, good)
        loaded = _adopter(project, install, good)
        if (project / "integrity" / "planit-skill-registry.json").exists():
            print("ASSERT:FAIL product repo must not hold the registry")
            return 1
        met = _run(project, loaded)
        out = (met.stdout or "") + (met.stderr or "")
        if met.returncode != 0 or "PLANIT_IDENTITY:MET" not in out:
            print(f"ASSERT:FAIL matching loaded skill must pass\n{out}")
            return 1
        loaded.write_bytes(bad)
        missed = _run(project, loaded)
        miss_out = (missed.stdout or "") + (missed.stderr or "")
        hub_registry = install / "hub" / "integrity" / "planit-skill-registry.json"
        if missed.returncode == 0 or "PLANIT_IDENTITY:NOT_MET" not in miss_out:
            print(f"ASSERT:FAIL mismatched loaded skill must fail\n{miss_out}")
            return 1
        if str(hub_registry) not in miss_out:
            print(f"ASSERT:FAIL mismatch must name the hub registry\n{miss_out}")
            return 1
        if str(project / "integrity") in miss_out:
            print(f"ASSERT:FAIL mismatch must not name a product-repo registry\n{miss_out}")
            return 1
        hub_registry.unlink()
        absent = _run(project, loaded)
        absent_out = (absent.stdout or "") + (absent.stderr or "")
        if absent.returncode == 0 or "missing hub registry" not in absent_out:
            print(f"ASSERT:FAIL missing hub registry must fail closed\n{absent_out}")
            return 1
    print("ASSERT:PASS loaded skill is checked against the hub registry")
    return 0
