#!/usr/bin/env python3
"""ADR 0063 overlap check."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.adr_decision_points.adr_decision_points import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
