#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <youtube_url> [lang]" >&2
  exit 1
fi

URL="$1"
LANG="${2:-en}"

# Prefer manual subtitles; fall back to auto-generated subtitles.
if ! yt-dlp --skip-download --write-sub --sub-lang "$LANG" --sub-format vtt -o "%(title)s.%(ext)s" "$URL"; then
  yt-dlp --skip-download --write-auto-sub --sub-lang "$LANG" --sub-format vtt -o "%(title)s.%(ext)s" "$URL"
fi
