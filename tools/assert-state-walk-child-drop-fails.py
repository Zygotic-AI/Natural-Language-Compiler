#!/usr/bin/env python3
"""Landmine ADR 0065: parent Status goes stale when a child leaves Accepted."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_state_walk_child_drop_fails import *  # noqa: F403

if __name__ == "__main__":
    raise SystemExit(main())
