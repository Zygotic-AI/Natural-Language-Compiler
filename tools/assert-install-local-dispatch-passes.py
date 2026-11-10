#!/usr/bin/env python3
"""Adapter: PATH nlc execs the repo copy."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_install_local_dispatch_passes.assert_install_local_dispatch_passes import *  # noqa: F403

if __name__ == "__main__":
    raise SystemExit(main())
