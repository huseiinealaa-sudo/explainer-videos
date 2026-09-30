#!/usr/bin/env bash
# Join the three 10 s clips (A, B, C) into output/style_test.mp4, silent, 720p, with a small corner letter per style.
# Usage: bash projects/style_test/build_video.sh A.mp4 B.mp4 C.mp4
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
TMP="$ROOT/tmp/style_test"; mkdir -p "$TMP" "$ROOT/output"
FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
clips=("$1" "$2" "$3")
i=0
: > "$TMP/list.txt"
for letter in A B C; do
  src="${clips[$i]}"; i=$((i+1))
  ffmpeg -y -loglevel error -i "$src" -t 10 -an \
    -vf "scale=1280:720,fps=24,drawtext=fontfile=$FONT:text='$letter':fontsize=30:fontcolor=white@0.92:x=w-tw-26:y=20:box=1:boxcolor=black@0.40:boxborderw=9,format=yuv420p" \
    -c:v libx264 -crf 20 -preset medium "$TMP/lab_$letter.mp4"
  echo "file '$TMP/lab_$letter.mp4'" >> "$TMP/list.txt"
done
ffmpeg -y -loglevel error -f concat -safe 0 -i "$TMP/list.txt" -c copy -movflags +faststart "$ROOT/output/style_test.mp4"
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$ROOT/output/style_test.mp4"
