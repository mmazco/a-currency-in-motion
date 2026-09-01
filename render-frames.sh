#!/bin/bash
# Render a deterministic frame sequence. --virtual-time-budget advances the
# page clock to an exact millisecond before the shot, so frame N is always the
# same picture — no wall-clock racing, no dropped frames.
set -e
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SRC="file://$PWD/usdt0-square.html?hold=$HOLD"
mkdir -p frames && rm -f frames/*.png
render(){
  n=$1; t=$(( n * 1000 / FPS ))
  "$CHROME" --headless --disable-gpu --hide-scrollbars --no-first-run \
    --user-data-dir="/tmp/cr-$n" --force-device-scale-factor=1 \
    --window-size=1080,1080 --default-background-color=FFFFFFFF \
    --virtual-time-budget=$((t+1)) \
    --screenshot="$PWD/frames/$(printf %04d $n).png" "$SRC" >/dev/null 2>&1
  rm -rf "/tmp/cr-$n"
}
export -f render; export CHROME SRC FPS
seq 0 $((TOTAL-1)) | xargs -P 8 -I{} bash -c 'render {}'
echo "rendered $(ls frames/*.png | wc -l | tr -d ' ') frames"
