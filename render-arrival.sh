#!/bin/bash
# Render the 12.5s arrival loop in both themes and encode each to MP4.
set -e
cleanup(){ pkill -9 -f 'shot-wide.sh' 2>/dev/null; for p in $(pgrep -f -- '--headless'); do kill -9 $p 2>/dev/null; done; }
trap cleanup EXIT
cd "$(dirname "$0")"
FPS=${FPS:-24}; FRAMES=${FRAMES:-300}; LAST=$((FRAMES-1))
mkdir -p export
for variant in "usdt0-arrival.html FFFFFFFF fr-light usdt0-arrival.mp4" \
               "usdt0-arrival-dark.html 0F0F0FFF fr-dark usdt0-arrival-dark.mp4"; do
  set -- $variant
  export SRC=$1 BG=$2 OUT=$3; MP4=$4
  echo "== $SRC -> $MP4"
  rm -rf "$OUT" && mkdir -p "$OUT"
  seq 0 $LAST | FPS=$FPS xargs -P 3 -I{} ./shot-wide.sh {}
  for i in $(seq 0 $LAST); do
    f=$(printf "$OUT/%04d.png" $i)
    [ -s "$f" ] || { echo "   retry $i"; FPS=$FPS ./shot-wide.sh $i; }
  done
  n=$(ls $OUT/*.png | wc -l | tr -d ' ')
  echo "   $n / $FRAMES frames"
  [ "$n" = "$FRAMES" ] || exit 1
  ./pngs2mp4 "export/$MP4" $FPS 14 $(ls $OUT/*.png | sort)
  rm -rf "$OUT"
done
