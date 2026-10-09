#!/bin/bash
# Re-render every social video in SDS lilac, light and dark.
set -e
cleanup(){ pkill -9 -f 'shot.sh|shot-wide.sh' 2>/dev/null; for p in $(pgrep -f -- '--headless'); do kill -9 $p 2>/dev/null; done; }
trap cleanup EXIT
cd "$(dirname "$0")"; mkdir -p export
run(){ # $1 src  $2 bg  $3 outdir  $4 mp4  $5 frames  $6 shooter
  echo "== $1 -> $4"
  rm -rf "$3" && mkdir -p "$3"
  export SRC=$1 BG=$2 OUT=$3
  seq 0 $(($5-1)) | FPS=24 xargs -P 5 -I{} ./$6 {}
  for i in $(seq 0 $(($5-1))); do f=$(printf "$3/%04d.png" $i); [ -s "$f" ] || { FPS=24 ./$6 $i; }; done
  n=$(ls $3/*.png | wc -l | tr -d ' '); echo "   $n / $5"
  [ "$n" = "$5" ] || exit 1
  ./pngs2mp4 "export/$4" 24 14 $(ls $3/*.png | sort); rm -rf "$3"
}
run usdt0-square.html      FFFFFFFF fr1 usdt0-square.mp4       442 shot.sh
run usdt0-square-dark.html 0F0F0FFF fr2 usdt0-square-dark.mp4  442 shot.sh
run usdt0-arrival.html     FFFFFFFF fr3 usdt0-arrival.mp4      300 shot-wide.sh
run usdt0-arrival-dark.html 161616FF fr4 usdt0-arrival-dark.mp4 300 shot-wide.sh
