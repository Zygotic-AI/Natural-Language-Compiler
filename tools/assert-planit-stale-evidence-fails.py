#!/usr/bin/env python3
"""Landmine: stale planit-change-evidence must fail --check-evidence."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.planit_identity import landmine_stale_evidence_fails_main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(landmine_stale_evidence_fails_main())