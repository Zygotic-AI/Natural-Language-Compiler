#!/usr/bin/env python3
"""Landmines: one-owned Planit gate must refuse every external-route spelling class."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.planit_identity import landmine_one_owned_probes_main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(landmine_one_owned_probes_main())