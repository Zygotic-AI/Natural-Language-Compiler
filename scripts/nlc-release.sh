#!/usr/bin/env bash
# Thin entrypoint (ADR 0048): parse input, call the release goal, report.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "${ROOT}/tools/hub_release.py" "$@"
