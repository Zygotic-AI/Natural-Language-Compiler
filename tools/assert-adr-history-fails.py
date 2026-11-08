#!/usr/bin/env python3
"""Landmine: a rejected ADR left in adrs/ must fail fitness-adr-history."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_adr_history_fails import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
