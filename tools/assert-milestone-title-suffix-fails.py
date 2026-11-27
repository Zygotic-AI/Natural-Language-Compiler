#!/usr/bin/env python3
"""Landmine ADR 0061: milestone title suffix; zero or many refuse."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_milestone_title_suffix_fails import *  # noqa: F403

if __name__ == "__main__":
    raise SystemExit(main())
