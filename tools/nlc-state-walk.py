#!/usr/bin/env python3
"""ADR 0065 upward lifecycle walk."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.nlc_state_walk.nlc_state_walk import main  # noqa: E402

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())
