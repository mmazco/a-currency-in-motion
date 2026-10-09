#!/bin/bash
# One frame. $1 = frame index.
# ?t= rather than the wall clock: headless Chrome fast-forwards JS timers but
# leaves CSS animations at zero, so advancing the clock captures every marker
# parked at its start. The page seeks each animation to the exact millisecond
# instead, which is both truthful and reproducible.
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# SRC/BG/OUT default to the light build, so the original pipeline is unchanged
SRC="${SRC:-usdt0-square.html}"
BG="${BG:-FFFFFFFF}"
OUT="${OUT:-frames}"
DIR="$(cd "$(dirname "$0")" && pwd)"
t=$(( $1 * 1000 / FPS ))
"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1080,1080 \
  --default-background-color=$BG --virtual-time-budget=900 \
  --screenshot="$DIR/$OUT/$(printf %04d $1).png" \
  "file://$DIR/$SRC?t=$t" >/dev/null 2>&1
