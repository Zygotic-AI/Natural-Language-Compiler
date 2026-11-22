#!/usr/bin/env bash
# ./release validate|sign [--armor FILE]|main|tag (ADR 0061). Thin entrypoint: the steps live in tools/nouns/nlc_release_tag_gate/.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
case "${1:-}" in
  validate|main|tag) exec python3 "${ROOT}/tools/nlc_release_tag_gate.py" "$1" ;;
  sign) exec python3 "${ROOT}/tools/nlc_release_tag_gate.py" "$@" ;;
  *) echo "usage: ./release validate|sign [--armor FILE]|main|tag"; exit 1 ;;
esac
