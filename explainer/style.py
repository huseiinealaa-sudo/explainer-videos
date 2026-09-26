"""Shared whiteboard style: paths, colours, fonts, text sizes and render settings.

Every video imports it (through `from explainer import *`). Importing it also sets
Manim's defaults: white background, black strokes, the shared font.
"""
import os
from pathlib import Path

from manim import *

# Repository root: override with EXPLAINER_ROOT, else the folder that holds this package.
ROOT = Path(os.environ.get("EXPLAINER_ROOT", Path(__file__).resolve().parents[1]))
OUTPUT_DIR = ROOT / "output"
BUILD_DIR = ROOT / "tmp"            # git-ignored: audio, media cache, previews

# ---------------- Colours ----------------
BG = WHITE
INK = BLACK
GREY_INK = "#555555"                # secondary strokes, notes, ray traces
LIGHT_INK = "#9e9e9e"               # faint guides, inactive items
PANEL_FILL = "#f3f3f3"              # light fill behind panels and table rows

# Generic palette: four accents that stay readable on white (used by the prover
# series as prover/fluid, meter/drive, measurement/OK, alarm).
ACCENT_1 = "#1f5fa8"                # blue
ACCENT_2 = "#c25a12"                # orange
ACCENT_3 = "#2e7d32"                # green
ACCENT_4 = "#c62828"                # red
PALETTE = [ACCENT_1, ACCENT_2, ACCENT_3, ACCENT_4]
OK_C = ACCENT_3                     # accepted / correct / done
ALERT_C = ACCENT_4                  # alarm / error / out of limit

# ---------------- Fonts & text sizes ----------------
FONT = "DejaVu Sans"
MONO = "DejaVu Sans Mono"           # tables, reports, code, function names
FS_TITLE = 64                       # opening title
FS_HEADING = 44                     # summary heading
FS_EQUATION = 40
FS_SUBTITLE = 38
FS_BODY = 36                        # bullets, corner title, panel titles
FS_SUMMARY = 34                     # summary lines
FS_SYMBOL = 30                      # single italic symbols (t, d)
FS_LABEL = 28                       # diagram labels
FS_NOTE = 26                        # material names, secondary labels
FS_AXIS = 24                        # axis labels, side notes
FS_TAG = 22                         # peak tags, small annotations

# ---------------- Frame ----------------
SAFE_WIDTH = 13.2                   # widest group that keeps a side margin in 16:9
CAPTION_Y = -3.3                    # caption line (SyncedScene.say)

# ---------------- Render settings ----------------
FINAL_RESOLUTION = (1920, 1080)
FINAL_FPS = 30

config.background_color = BG
Text.set_default(color=INK, font=FONT)
VMobject.set_default(color=INK)


def label(text, size=FS_LABEL, color=INK, **kw):
    return Text(text, font_size=size, color=color, **kw)


def mono(text, size=FS_TAG, color=INK, **kw):
    return Text(text, font_size=size, color=color, font=MONO, **kw)


def fit(mob, width=SAFE_WIDTH):
    """Shrink a group so it stays inside the 16:9 frame with a side margin."""
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob
