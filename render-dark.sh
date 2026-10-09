#!/bin/bash
# Dark-mode square render. Same mechanism as render.sh: seek each frame with
# ?t= rather than trusting the wall clock, retry drops, then encode.
set -e
cleanup(){ pkill -9 -f 'shot.sh' 2>/dev/null; for p in $(pgrep -f -- '--headless'); do kill -9 $p 2>/dev/null; done; }
trap cleanup EXIT
cd "$(dirname "$0")"
FPS=${FPS:-24}; FRAMES=${FRAMES:-442}
LAST=$((FRAMES-1))
rm -rf frames-dark && mkdir -p frames-dark export
export SRC=usdt0-square-dark.html BG=0F0F0FFF OUT=frames-dark
seq 0 $LAST | FPS=$FPS xargs -P 3 -I{} ./shot.sh {}
for i in $(seq 0 $LAST); do
  f=$(printf "frames-dark/%04d.png" $i)
  [ -s "$f" ] || { echo "  retry $i"; FPS=$FPS ./shot.sh $i; }
done
n=$(ls frames-dark/*.png | wc -l | tr -d ' ')
echo "  $n / $FRAMES frames"
[ "$n" = "$FRAMES" ] || exit 1
./pngs2mp4 export/usdt0-square-dark.mp4 $FPS 12 $(ls frames-dark/*.png | sort)
