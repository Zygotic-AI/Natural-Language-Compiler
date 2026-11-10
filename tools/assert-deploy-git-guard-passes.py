#!/usr/bin/env python3
"""Thin adapter: deploy_git_guard temp-repo tests."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.assert_deploy_git_guard_passes.assert_deploy_git_guard_passes import (  # noqa: E402
    main,
)

if __name__ == "__main__":
    raise SystemExit(main())
