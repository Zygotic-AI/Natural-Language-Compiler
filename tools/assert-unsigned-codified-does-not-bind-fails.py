#!/usr/bin/env python3
"""Landmine ADR 0062 / 0052: unsigned Accepted ADR is named and does not bind."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_unsigned_codified_does_not_bind_fails import *  # noqa: F403

if __name__ == "__main__":
    raise SystemExit(main())
