#!/usr/bin/env python3
"""Landmine ADR 0064: work-queue.json is not lifecycle SSOT."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_work_queue_json_not_ssot_fails import *  # noqa: F403

if __name__ == "__main__":
    raise SystemExit(main())
