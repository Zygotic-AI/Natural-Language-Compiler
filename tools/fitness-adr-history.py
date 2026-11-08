#!/usr/bin/env python3
"""Current ADRs live in adrs/; previous bytes live in adrs/history/."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.adr_history import *  # noqa: F403


if __name__ == "__main__":
    raise SystemExit(main())
