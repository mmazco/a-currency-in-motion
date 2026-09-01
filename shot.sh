#!/bin/bash
# One frame. $1 = frame index. Deterministic: virtual-time-budget sets the
# page clock exactly, so this frame is always identical.
# No --user-data-dir on purpose — a fresh profile makes headless hang forever.
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DIR="$(cd "$(dirname "$0")" && pwd)"
t=$(( $1 * 1000 / FPS + 1 ))
"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1080,1080 \
  --default-background-color=FFFFFFFF --virtual-time-budget=$t \
  --screenshot="$DIR/frames/$(printf %04d $1).png" \
  "file://$DIR/usdt0-square.html?hold=$HOLD" >/dev/null 2>&1
