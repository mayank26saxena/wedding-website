#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST="127.0.0.1"
PORT="${PORT:-5050}"
OUT_DIR="${OUT_DIR:-$ROOT_DIR/out}"
RAW_DIR="$OUT_DIR/$HOST:$PORT"
SITE_DIR="$OUT_DIR/site"
BASE_HREF="${BASE_HREF:-/wedding-website/}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
SERVER_SCRIPT="$ROOT_DIR/scripts/run_static_server.py"
SERVER_LOG="$OUT_DIR/server.log"

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

STATIC_HOST="$HOST" STATIC_PORT="$PORT" "$PYTHON_BIN" "$SERVER_SCRIPT" > "$SERVER_LOG" 2>&1 &
FLASK_PID=$!

cleanup() {
  if ps -p "$FLASK_PID" > /dev/null 2>&1; then
    kill "$FLASK_PID" >/dev/null 2>&1 || true
    wait "$FLASK_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

READY=0
for _ in {1..30}; do
  if curl -fs "http://$HOST:$PORT" >/dev/null 2>&1; then
    READY=1
    break
  fi
  if ! ps -p "$FLASK_PID" >/dev/null 2>&1; then
    cat "$SERVER_LOG" >&2 || true
    echo "Flask app terminated unexpectedly." >&2
    exit 1
  fi
  sleep 1
done

if [ "$READY" -ne 1 ]; then
  cat "$SERVER_LOG" >&2 || true
  echo "Timed out waiting for Flask to start on http://$HOST:$PORT" >&2
  exit 1
fi

wget --mirror --page-requisites --adjust-extension --convert-links --no-parent \
  --directory-prefix "$OUT_DIR" "http://$HOST:$PORT/"

if [ ! -d "$RAW_DIR" ]; then
  echo "Expected mirrored directory $RAW_DIR not found" >&2
  exit 1
fi

rm -rf "$SITE_DIR"
mv "$RAW_DIR" "$SITE_DIR"

find "$SITE_DIR" -name '*.html' -print0 | while IFS= read -r -d '' file; do
  "$PYTHON_BIN" - "$file" "$BASE_HREF" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
base_href = sys.argv[2]
text = path.read_text()
if '<base ' in text.lower():
    sys.exit(0)

lower = text.lower()
head_index = lower.find('<head>')
if head_index != -1:
    insert_at = head_index + len('<head>')
    updated = text[:insert_at] + f'\n    <base href="{base_href}">' + text[insert_at:]
else:
    updated = f'<head><base href="{base_href}"></head>' + text

path.write_text(updated)
PY
done

if [ -f "$SITE_DIR/index.html" ] && [ ! -f "$SITE_DIR/404.html" ]; then
  cp "$SITE_DIR/index.html" "$SITE_DIR/404.html"
fi

echo "Static site generated at $SITE_DIR"
