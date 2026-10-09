#!/bin/bash
# One 1920x1080 frame of the arrival diagram. $1 = frame index.
# ?t= seeks the CSS animations; the wall clock would leave them all at zero.
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DIR="$(cd "$(dirname "$0")" && pwd)"
t=$(( $1 * 1000 / FPS ))
"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1920,1080 \
  --default-background-color=$BG --virtual-time-budget=1100 \
  --screenshot="$DIR/$OUT/$(printf %04d $1).png" \
  "file://$DIR/$SRC?t=$t" >/dev/null 2>&1
