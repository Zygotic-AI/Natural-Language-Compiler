#!/usr/bin/env python3
"""Landmine: a second planit/SKILL.md in the tree must fail one-owned fitness."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.planit_identity import landmine_second_skill_fails_main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(landmine_second_skill_fails_main())