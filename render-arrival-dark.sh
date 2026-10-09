#!/bin/bash
set -e
cleanup(){ pkill -9 -f 'shot-wide.sh' 2>/dev/null; for p in $(pgrep -f -- '--headless'); do kill -9 $p 2>/dev/null; done; }
trap cleanup EXIT
cd "$(dirname "$0")"
FPS=${FPS:-24}; FRAMES=${FRAMES:-300}; LAST=$((FRAMES-1))
mkdir -p export; rm -rf fr-dark && mkdir -p fr-dark
export SRC=usdt0-arrival-dark.html BG=0F0F0FFF OUT=fr-dark
seq 0 $LAST | FPS=$FPS xargs -P 4 -I{} ./shot-wide.sh {}
for i in $(seq 0 $LAST); do
  f=$(printf "fr-dark/%04d.png" $i)
  [ -s "$f" ] || { echo "  retry $i"; FPS=$FPS ./shot-wide.sh $i; }
done
n=$(ls fr-dark/*.png | wc -l | tr -d ' '); echo "  $n / $FRAMES frames"
[ "$n" = "$FRAMES" ] || exit 1
./pngs2mp4 export/usdt0-arrival-dark.mp4 $FPS 14 $(ls fr-dark/*.png | sort)
rm -rf fr-dark
