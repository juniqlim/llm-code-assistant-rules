#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPT="$SCRIPT_DIR/scripts/get_yt_subs.sh"

if [[ ! -f "$SCRIPT" ]]; then
  echo "missing script: $SCRIPT" >&2
  exit 1
fi

output="$($SCRIPT 2>&1 || true)"
if ! echo "$output" | rg -q "^Usage:"; then
  echo "expected usage message, got:" >&2
  echo "$output" >&2
  exit 1
fi

# Ensure script prefers manual subs and falls back to auto subs.
if ! rg -q -- "--write-sub" "$SCRIPT"; then
  echo "expected --write-sub for manual subtitles" >&2
  exit 1
fi
if ! rg -q -- "--write-auto-sub" "$SCRIPT"; then
  echo "expected --write-auto-sub for fallback" >&2
  exit 1
fi
