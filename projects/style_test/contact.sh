#!/usr/bin/env bash
# One contact sheet (3x2 frames, one every 1.7 s) for a clip: bash contact.sh clip.mp4 sheet.png
ffmpeg -y -loglevel error -i "$1" -vf "fps=0.6,scale=640:-1,tile=3x2" -frames:v 1 "$2"
