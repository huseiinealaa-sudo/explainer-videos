"""Tabler icons (MIT, https://tabler.io/icons) as whiteboard strokes.

    icon("gauge")                                   # 1 unit square, INK strokes
    icon("flame", color=ALERT_C, size=0.8)
    icon_grid(["bolt", "clock"], cols=6)           # icons with their names below

The outline icons the repository uses are vendored in explainer/assets/tabler/outline/
(version in TABLER_VERSION, licence in explainer/assets/tabler/LICENSE): renders stay
offline and reproducible, and the repository keeps ~50 small files instead of the 5000+
of the full set (21 MB). `python -m explainer.icons add <name> ...` copies more icons of
the same version from the npm package (@tabler/icons on cdn.jsdelivr.net) into that folder;
`python -m explainer.icons list` prints the vendored names.

Tabler SVGs are 24×24, stroke="currentColor", fill="none", stroke-linecap/-linejoin round,
and start with an invisible 24×24 frame path (stroke="none"). icon() replaces currentColor
with the colour, keeps the frame as an invisible square so every icon has the same size and
centre whatever its drawing, and sets the stroke width, round caps and joins itself (Manim
does not read the linecap/linejoin attributes, and it would take stroke-width="2" as its
own, much thinner, stroke width).
"""
import re
import ssl
import sys
import tempfile
import urllib.request
from pathlib import Path

from manim import DOWN, UP, SVGMobject, VGroup
from manim.constants import CapStyleType, LineJointType

from .style import FS_TAG, GREY_INK, INK, label

__all__ = ["icon", "icon_grid", "icon_names", "ICON_DIR", "TABLER_VERSION"]

TABLER_VERSION = "3.48.0"
ICON_DIR = Path(__file__).resolve().parent / "assets" / "tabler" / "outline"
CDN = "https://cdn.jsdelivr.net/npm/@tabler/icons@{version}/icons/outline/{name}.svg"
PROXY_CA_BUNDLE = "/root/.ccr/ca-bundle.crt"

_FRAME = re.compile(r'<path[^>]*stroke="none"[^>]*/>')
_CACHE = Path(tempfile.gettempdir()) / "explainer_icons"


def icon_names():
    """Names of the vendored icons (file names without .svg), sorted."""
    return sorted(p.stem for p in ICON_DIR.glob("*.svg"))


def _prepared_svg(name, color):
    """The icon's SVG with the colour written in and the frame path made a plain box."""
    path = ICON_DIR / f"{name}.svg"
    if not path.exists():
        raise FileNotFoundError(
            f"Tabler icon {name!r} is not vendored; add it with "
            f"`python -m explainer.icons add {name}` (known: {', '.join(icon_names())})")
    svg = path.read_text()
    svg = svg.replace("currentColor", color)
    # The frame (M0 0h24v24H0z, stroke="none") fixes the size: keep it as a marked element.
    svg = _FRAME.sub('<path id="frame" d="M0 0h24v24H0z" fill="none" stroke="none"/>', svg, 1)
    svg = re.sub(r'\sclass="[^"]*"', "", svg)          # not used by Manim
    _CACHE.mkdir(exist_ok=True)
    out = _CACHE / f"{name}_{color.lstrip('#')}.svg"
    if not out.exists() or out.read_text() != svg:
        out.write_text(svg)
    return out


def icon(name, color=INK, size=1.0, stroke_width=4):
    """Tabler outline icon `name` as an SVGMobject: size × size units, strokes in `color`.

    submobjects[0] is the invisible 24×24 frame (it keeps size and centre the same for every
    icon); the rest are the icon's strokes, drawn in the whiteboard stroke width.
    """
    color = str(color)
    if not color.startswith("#"):
        from manim import ManimColor
        color = ManimColor(color).to_hex()
    mob = SVGMobject(str(_prepared_svg(name, color)), height=None, width=None,
                     should_center=True, stroke_color=color, fill_opacity=0)
    frame, strokes = mob.submobjects[0], mob.submobjects[1:]
    mob.scale(size / max(frame.width, frame.height))
    frame.set_stroke(opacity=0).set_fill(opacity=0)
    for m in strokes:
        filled = m.get_fill_opacity() > 0
        m.set_stroke(color, width=stroke_width, opacity=1)
        m.set_fill(color, opacity=1 if filled else 0)
        for f in m.get_family():
            f.cap_style = CapStyleType.ROUND
            f.joint_type = LineJointType.ROUND
    mob.shift(-frame.get_center())                  # centre of the 24×24 box at ORIGIN
    mob.icon_name = name
    return mob


def icon_grid(names, cols=6, size=0.9, color=INK, cell=(2.1, 1.7), name_size=FS_TAG - 4,
              name_color=GREY_INK):
    """Icons in a grid, each with its name below; returns VGroup of VGroup(icon, name).

    cell = (width, height) of one grid cell: icon + name + the gap to the next cell."""
    cells = VGroup(*[VGroup(icon(n, color, size), label(n, name_size, name_color))
                     for n in names])
    for c in cells:
        c[1].next_to(c[0], DOWN, 0.15)
    cells.arrange_in_grid(cols=cols, col_widths=[cell[0]] * cols,
                          row_heights=[cell[1]] * -(-len(cells) // cols), buff=0,
                          cell_alignment=UP)
    return cells


# ---------------- vendoring more icons ----------------
def add_icons(names, version=TABLER_VERSION):
    """Copy outline icons of `version` from the npm package (jsDelivr) into ICON_DIR."""
    ctx = ssl.create_default_context(cafile=PROXY_CA_BUNDLE) \
        if Path(PROXY_CA_BUNDLE).exists() else ssl.create_default_context()
    for name in names:
        with urllib.request.urlopen(CDN.format(version=version, name=name), context=ctx) as r:
            svg = r.read().decode()
        if 'stroke="currentColor"' not in svg:
            raise ValueError(f"{name}: not a Tabler outline icon")
        (ICON_DIR / f"{name}.svg").write_text(svg)
        print(f"added {name}")


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:] or ["list"]
    if cmd == "add" and rest:
        add_icons(rest)
    elif cmd == "list":
        print(" ".join(icon_names()))
    else:
        sys.exit("usage: python -m explainer.icons list | add <name> ...")
