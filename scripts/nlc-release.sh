#!/usr/bin/env bash
# ./release validate|sign|main|tag (ADR 0061). Thin entrypoint: the steps live in tools/nouns/nlc_release_tag_gate/.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
case "${1:-}" in
  validate|sign|main|tag) exec python3 "${ROOT}/tools/nlc_release_tag_gate.py" "$1" ;;
  *) echo "usage: ./release validate|sign|main|tag"; exit 1 ;;
esac
