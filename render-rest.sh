#!/bin/bash
# Finish the three remaining videos. Unlike render-all.sh this does NOT wipe the
# frame dir first, so an interrupted pass resumes instead of starting over.
set -e
cleanup(){ for p in $(pgrep -f -- '--headless'); do kill -9 $p 2>/dev/null; done; }
trap cleanup EXIT
cd "$(dirname "$0")"; mkdir -p export
run(){ # src bg outdir mp4 frames shooter
  echo "== $1 -> $4"
  mkdir -p "$3"
  export SRC=$1 BG=$2 OUT=$3
  missing=()
  for i in $(seq 0 $(($5-1))); do
    f=$(printf "$3/%04d.png" $i); [ -s "$f" ] || missing+=($i)
  done
  echo "   ${#missing[@]} frames to render"
  [ ${#missing[@]} -gt 0 ] && printf '%s\n' "${missing[@]}" | FPS=24 xargs -P 4 -I{} ./$6 {}
  for i in $(seq 0 $(($5-1))); do
    f=$(printf "$3/%04d.png" $i); [ -s "$f" ] || { FPS=24 ./$6 $i; }
  done
  n=$(ls $3/*.png | wc -l | tr -d ' '); echo "   $n / $5"
  [ "$n" = "$5" ] || exit 1
  ./pngs2mp4 "export/$4" 24 14 $(ls $3/*.png | sort); rm -rf "$3"
}
run usdt0-square-dark.html  0F0F0FFF fr2 usdt0-square-dark.mp4  442 shot.sh
run usdt0-arrival.html      FFFFFFFF fr3 usdt0-arrival.mp4      300 shot-wide.sh
run usdt0-arrival-dark.html 161616FF fr4 usdt0-arrival-dark.mp4 300 shot-wide.sh
echo "ALL DONE"
