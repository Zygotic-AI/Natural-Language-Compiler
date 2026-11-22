#!/usr/bin/env python3
"""Fail closed when a second Planit skill or an external Planit route exists."""
from __future__ import annotations

import sys
from pathlib import Path

_CANONICAL_PLANIT_SKILL = ".agents/skills/planit/SKILL.md"
_PLANIT_IDENTITY_MODULE = "tools/nouns/planit_identity/planit_identity.py"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.planit_identity import one_owned_main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(one_owned_main())