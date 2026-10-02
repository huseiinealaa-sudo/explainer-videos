"""Shared whiteboard style: paths, colours, fonts, text sizes and render settings.

Every video imports it (through `from explainer import *`). Importing it also sets
Manim's defaults: the project's theme (explainer/theme.py: background, ink strokes) and the
shared font.
"""
import os
from pathlib import Path

from manim import *

from .theme import (DEFAULT_THEME, THEMES, ThemeColor, check_theme, contrast_ratio,  # noqa: F401
                    current_theme, project_motion, project_style, project_theme, set_theme,
                    theme_colors, theme_names)
from .theme import token as _token

# Repository root: override with EXPLAINER_ROOT, else the folder that holds this package.
ROOT = Path(os.environ.get("EXPLAINER_ROOT", Path(__file__).resolve().parents[1]))
OUTPUT_DIR = ROOT / "output"
BUILD_DIR = ROOT / "tmp"            # git-ignored: audio, media cache, previews

# ---------------- Colours ----------------
# Every colour is a ThemeColor (explainer/theme.py): it holds the value of the project's
# theme (dark by default, chosen by the `[style] theme` line of project.toml) and changes
# with SyncedScene.set_theme. `color=INK` in any script or default argument follows the theme.
BG = _token("bg")                    # background
BG_ALT = _token("bg_alt")            # second colour of gradients
INK = _token("ink")                  # text and primary strokes
GREY_INK = _token("muted")           # secondary text, strokes, notes, ray traces
LIGHT_INK = _token("faint")          # inactive items, faint guides
PANEL_FILL = _token("panel")         # fill behind panels and table rows
LINE_C = _token("line")              # lines, arrows, axes, symbols
GRID_C = _token("grid")              # background grid and particles

# Generic palette: four accents that stay readable on the theme's background (used by
# the prover series as prover/fluid, meter/drive, measurement/OK, alarm).
ACCENT_1 = _token("accent1")         # blue (yellow on blueprint)
ACCENT_2 = _token("accent2")         # orange
ACCENT_3 = _token("accent3")         # green
ACCENT_4 = _token("accent4")         # red
PALETTE = [ACCENT_1, ACCENT_2, ACCENT_3, ACCENT_4]
OK_C = _token("ok")                  # accepted / correct / done
ALERT_C = _token("alert")            # alarm / error / out of limit

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
SAFE_MARGIN = 0.25                  # keep text this far inside the frame (QA check)
MIN_FONT_SIZE = 14                  # smallest readable text at 1080p (x-height ≈ 14 px; QA check)
CAPTION_Y = -3.3                    # caption line (SyncedScene.say)

# ---------------- Render settings ----------------
FINAL_RESOLUTION = (1920, 1080)
FINAL_FPS = 30

Text.set_default(color=INK, font=FONT)
VMobject.set_default(color=LINE_C)


def label(text, size=FS_LABEL, color=INK, **kw):
    return Text(text, font_size=size, color=color, **kw)


def mono(text, size=FS_TAG, color=INK, **kw):
    return Text(text, font_size=size, color=color, font=MONO, **kw)


def fit(mob, width=SAFE_WIDTH):
    """Shrink a group so it stays inside the 16:9 frame with a side margin."""
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob
