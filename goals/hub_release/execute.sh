#!/usr/bin/env bash
# Hub release goal (ADR 0048). Gates first (ADR 0061), then step verbs.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
exec python3 "${ROOT}/tools/hub_release.py" "$@"
