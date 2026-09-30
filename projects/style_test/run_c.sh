#!/usr/bin/env bash
# Style C - ONE attempt, hard limit 15 minutes for install + render + encode. No retry.
# Usage: bash projects/style_test/run_c.sh   (result: $C_WORK/result.txt, $C_WORK/style_c.mp4)
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
export C_WORK=${C_WORK:-/tmp/style_test_c}
mkdir -p "$C_WORK"
export C_START_EPOCH=$(date +%s)
export HERE
echo "$C_START_EPOCH" > "$C_WORK/start_epoch"
timeout -k 10 900 bash -c '
  set -e
  pip install --no-input bpy
  echo "INSTALL_DONE $(( $(date +%s) - C_START_EPOCH ))"
  python "$HERE/style_c_blender.py"
  FPS=$(python -c "import json,sys;print(json.load(open(\"$C_WORK/render.json\"))[\"fps\"])")
  ffmpeg -y -loglevel error -framerate "$FPS" -i "$C_WORK/frames/f%04d.png" -vf "fps=24,format=yuv420p" \
    -c:v libx264 -crf 18 -preset fast "$C_WORK/style_c.mp4"
  echo "ENCODE_DONE $(( $(date +%s) - C_START_EPOCH ))"
' > "$C_WORK/run.log" 2>&1
CODE=$?
echo "exit=$CODE elapsed=$(( $(date +%s) - C_START_EPOCH ))s" > "$C_WORK/result.txt"
