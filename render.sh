#!/bin/bash
# Render the cycle, retry any frame that dropped, then encode.
set -e
cleanup(){ pkill -9 -f 'shot.sh' 2>/dev/null; for p in $(pgrep -f -- '--headless'); do kill -9 $p 2>/dev/null; done; }
trap cleanup EXIT
cd "$(dirname "$0")"
LAST=$((FRAMES-1))
rm -rf frames && mkdir -p frames
seq 0 $LAST | FPS=$FPS xargs -P 3 -I{} ./shot.sh {}
# a worker occasionally wedges and drops its frame; fill the gaps serially
for i in $(seq 0 $LAST); do
  f=$(printf "frames/%04d.png" $i)
  [ -s "$f" ] || { echo "  retrying frame $i"; FPS=$FPS ./shot.sh $i; }
done
n=$(ls frames/*.png | wc -l | tr -d ' ')
echo "  $n / $FRAMES frames"
[ "$n" = "$FRAMES" ] || exit 1
./pngs2mp4 export/usdt0-square.mp4 24 12 $(ls frames/*.png | sort)
rm -rf frames
