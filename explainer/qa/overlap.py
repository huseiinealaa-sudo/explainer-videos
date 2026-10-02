"""Overlap check (QA mode): the layout faults a viewer would notice, after every animation.

SyncedScene creates an OverlapChecker when the pipeline runs in QA mode (EXPLAINER_QA)
and calls check() after every animation. It records:
    text_overlap        two texts or labels overlap
    text_over_shape     a line, arrow or drawing runs through a text
    text_near_shape     a text closer than CLEARANCE to a line, arrow or drawing outside
                        its frame (touching included: contacts too small for text_over_shape)
    text_touches_frame  a text inside its frame touches or crosses the frame's outline
    out_of_frame        a text or a shape leaves the 16:9 frame
    in_safe_margin      a text inside the frame but closer than SAFE_MARGIN to its edge
    text_too_small      a text whose size after fit()/scale is below MIN_FONT_SIZE
    low_contrast        a text whose colour against what is behind it (the background of the
                        scene, with every fill under the text blended in) is below 4.5:1
                        (WCAG AA, theme.MIN_CONTRAST). Text in LIGHT_INK is inactive by
                        convention and exempt, as is any text marked `contrast_exempt = True`
Intended overlaps are not errors: a text inside a closed shape (its box, badge, table
row, panel or emphasis frame) that keeps clear of the outline, single-symbol marks
(✓ ✗ • ...) placed on a drawing on purpose, lines that cross out a whole text, and a
text's own leader (a path that starts at the text, an arrow whose tip points at it, or a
line joining it to another text). CLEARANCE was calibrated on the RT pilot and the prover
series (PR notes): real touches measured 0.00-0.056, intended placements 0.06 and more.

Each finding is an interval on the narration clock: first seen (time) -> gone (until).
write() saves them raw; report_by_segment() (run by the pipeline) writes one JSON report
per narration segment: the time, the two elements, the overlap amount, the grid cell
(6×6, A1 top-left ... F6 bottom-right, as on the contact sheets) and a fix suggestion.
"""
import json
import re
from pathlib import Path

import numpy as np
from manim import (DL, UR, Group, ImageMobject, MarkupText, Mobject, Paragraph, Text,
                   VGroup, VMobject, config)
from shapely import STRtree
from shapely.affinity import translate
from shapely.geometry import LinearRing, LineString, MultiPoint, Point, Polygon, box
from shapely.ops import nearest_points, unary_union

from ..style import BG, LIGHT_INK, MIN_FONT_SIZE, SAFE_MARGIN, SAFE_WIDTH
from ..theme import MIN_CONTRAST, _rgb, blend, contrast_ratio

MIN_AREA = 0.002            # scene units² (about 36 px² at 1080p): smaller contacts are noise
ATTACHED = 0.35             # parts of the same on-screen group this close move with a text
CLEARANCE = 0.06            # scene units (about 8 px at 1080p) between a text's glyphs and the
                            # ink (stroke width included) of any shape outside its frame
LEADER_REACH = 0.3          # a path starting this close to a text is that text's leader
ARROWS = ("Arrow", "DoubleArrow", "Vector", "CurvedArrow", "CurvedDoubleArrow")
TEXT_TYPES = (Text, MarkupText, Paragraph)
MARKS = set("✓✗✔✘×•·○●◦▪■□▲▼►◄★")
# Same classes as the critic: overlap, off-frame and unreadable text are critical; a text
# inside the safe margin is an improvement (it never blocks PASS).
SEVERITY = {"text_overlap": "critical", "text_over_shape": "critical", "out_of_frame": "critical",
            "text_near_shape": "critical",
            "text_touches_frame": "critical", "text_too_small": "critical",
            "low_contrast": "critical",
            "in_safe_margin": "improvement"}
DIRECTIONS = {"RIGHT": (1, 0), "LEFT": (-1, 0), "UP": (0, 1), "DOWN": (0, -1)}
OPPOSITE = {"RIGHT": "LEFT", "LEFT": "RIGHT", "UP": "DOWN", "DOWN": "UP"}
COLS, GRID = "ABCDEF", 6


# ---------------- grid (same cells as the contact sheets) ----------------
def cell(x, y):
    """Grid cell of a scene point: A1 (top-left) ... F6 (bottom-right)."""
    fw, fh = config.frame_width, config.frame_height
    c = min(GRID - 1, max(0, int((x + fw / 2) / fw * GRID)))
    r = min(GRID - 1, max(0, int((fh / 2 - y) / fh * GRID)))
    return f"{COLS[c]}{r + 1}"


def cells(bounds):
    """Cells covered by bounds (x0, y0, x1, y1), e.g. 'A4-B5'."""
    a, b = cell(bounds[0], bounds[3]), cell(bounds[2], bounds[1])
    return a if a == b else f"{a}-{b}"


# ---------------- what is on screen ----------------
class Item:
    """A visible element: a text (its box) or a shape (its ink, closed region and outline)."""

    def __init__(self, kind, mob, ink, region=None, outline=None, text="", font=None, core=None,
                 glyphs=None):
        self.kind, self.mob, self.ink = kind, mob, ink
        self.core = ink if core is None else core      # text: hull of its glyphs; shape: its ink
        self.glyphs = self.core if glyphs is None else glyphs   # text: each glyph's hull
        self.region, self.outline = region, outline
        self.fills = []                 # shape: [(polygon, rgb, opacity)] painted under later texts
        self.text, self.font = text, font
        self.cls = type(mob).__name__
        self.root = None                # the on-screen mobject (scene.mobjects entry) it is part of

    @property
    def open_path(self):
        return self.region is None or self.cls in ("Line", "Arrow", "DoubleArrow", "DashedLine",
                                                   "Vector")


_T = np.linspace(0, 1, 9)[:, None]
_BERNSTEIN = [(1 - _T) ** 3, 3 * (1 - _T) ** 2 * _T, 3 * (1 - _T) * _T ** 2, _T ** 3]


def _subpaths(vm):
    """[(xy samples, closed), ...] along each cubic Bézier subpath of a VMobject."""
    out = []
    for sp in vm.get_subpaths():
        n = len(sp) // 4 * 4
        if n < 4:
            continue
        curves = np.asarray(sp[:n], dtype=float).reshape(-1, 4, 3)
        pts = sum(b[None] * curves[:, i:i + 1] for i, b in enumerate(_BERNSTEIN))
        xy = pts[:, :, :2].reshape(-1, 2)
        if np.ptp(xy, axis=0).max() < 1e-6:
            continue
        out.append((xy, bool(np.allclose(sp[0], sp[n - 1], atol=1e-4))))
    return out


def _shape_item(m, skip):
    """One primitive shape (Line, Arrow with its tip, DashedLine with its dashes, ...)."""
    strokes, rings, fills, regions, layers = [], [], [], [], []
    for f in m.get_family():
        if id(f) in skip or not isinstance(f, VMobject) or not f.has_points():
            continue
        width = f.get_stroke_width() if f.get_stroke_opacity() > 0.05 else 0
        filled = f.get_fill_opacity() > 0.05
        if width <= 0 and not filled:
            continue
        half = max(width * 0.01 / 2, 0.01)          # Cairo draws stroke_width × 0.01 units
        for xy, closed in _subpaths(f):
            closed = closed and len(xy) >= 4
            if closed:
                poly = Polygon(xy).buffer(0)
                if not poly.is_empty:
                    regions.append(poly)
                    if filled:
                        fills.append(poly)
                        layers.append((poly, f.get_fill_rgbas()[:, :3].mean(axis=0),
                                       float(f.get_fill_opacity())))
            if width > 0:
                line = LinearRing(xy) if closed else LineString(xy)
                (rings if closed else strokes).append(line.buffer(half, cap_style="flat"))
    ink = unary_union(strokes + rings + fills)
    if ink.is_empty:
        return None
    item = Item("shape", m, ink, region=unary_union(regions) if regions else None,
                outline=unary_union(rings) if rings else None)
    item.fills = layers
    return item


def _text_of(m):
    t = getattr(m, "original_text", None) or getattr(m, "text", None)   # .text drops spaces
    if t is None and hasattr(m, "lines_text"):          # Paragraph
        t = getattr(m.lines_text, "original_text", "")
    return " ".join(re.sub(r"<[^>]+>", "", str(t or "")).split())


def _font_size(m):
    """Font size after scaling (Text.font_size breaks on rotated text, e.g. a y-axis label)."""
    fs0, h0 = getattr(m, "_font_size", None), getattr(m, "initial_height", None)
    if not fs0 or not h0:
        return None
    raw = str(getattr(m, "original_text", "") or getattr(m, "text", ""))
    turned = m.height > 1.5 * m.width and "\n" not in raw and len(raw.strip()) > 2
    return fs0 * (m.width if turned else m.height) / h0


def _text_item(m):
    glyphs = m.family_members_with_points()
    if not glyphs or max(g.get_fill_opacity() for g in glyphs) <= 0.05:
        return None
    text = _text_of(m)
    if text.replace(" ", "") in MARKS:                   # a mark placed on purpose, not a label
        return None
    (x0, y0), (x1, y1) = m.get_corner(DL)[:2], m.get_corner(UR)[:2]
    if x1 - x0 < 1e-6 or y1 - y0 < 1e-6:
        return None
    # the box catches a line through a label, even through the gap between two words;
    # the hull of the glyphs decides whether the text sits inside a (round) frame
    hull = MultiPoint(np.vstack([g.points[:, :2] for g in glyphs])).convex_hull
    # the clearance is measured to the letters themselves, not to the box or the hull
    ink = unary_union([MultiPoint(g.points[:, :2]).convex_hull for g in glyphs])
    return Item("text", m, box(x0, y0, x1, y1), text=text, font=_font_size(m), core=hull,
                glyphs=ink)


def collect(mobjects):
    """Visible items: whole texts, primitive shapes (with their tips or dashes) and images.
    VGroups (and point-less VMobjects) are only containers."""
    items, seen = [], set()

    def visit(m):
        if id(m) in seen:
            return
        seen.add(id(m))
        if isinstance(m, TEXT_TYPES):
            it = _text_item(m)
            if it:
                items.append(it)
            return
        if isinstance(m, ImageMobject):
            (x0, y0), (x1, y1) = m.get_corner(DL)[:2], m.get_corner(UR)[:2]
            r = box(x0, y0, x1, y1)
            items.append(Item("image", m, r, region=r))
            return
        if (isinstance(m, (VGroup, Group)) or not isinstance(m, VMobject)
                or (type(m) in (VMobject, Mobject) and not m.has_points())):
            for s in m.submobjects:
                visit(s)
            return
        texts = [d for d in m.get_family()[1:] if isinstance(d, TEXT_TYPES)]
        skip = {id(g) for t in texts for g in t.get_family()}
        it = _shape_item(m, skip)
        if it:
            items.append(it)
        seen.update(id(f) for f in m.get_family() if id(f) not in skip)
        for t in texts:
            visit(t)

    for m in mobjects:
        if getattr(m, "is_background", False):      # decoration: the contrast rule measures it
            continue
        first = len(items)
        visit(m)
        for it in items[first:]:
            it.root = id(m)
    return items


def inside(it, region, min_area=MIN_AREA):
    """Is item `it` (a text: the hull of its glyphs) inside a closed region? A sliver
    sticking out (into the frame's own stroke) still counts as inside."""
    if region is None or not region.intersects(it.core):
        return False
    return it.core.difference(region).area < max(min_area, 0.02 * it.core.area)


def struck_through(text, shape, tol=0.15):
    """A cross-out or strike-through drawn on purpose: a line spanning the text's width
    and lying within its height (e.g. a wrong statement crossed out)."""
    if not shape.open_path:
        return False
    tx0, ty0, tx1, ty1 = text.ink.bounds
    sx0, sy0, sx1, sy1 = shape.ink.bounds
    return (abs(sx0 - tx0) <= tol and abs(sx1 - tx1) <= tol
            and sy0 >= ty0 - tol and sy1 <= ty1 + tol)


def leader_of(text, shape, texts=(), reach=LEADER_REACH):
    """The text's own leader: a path that starts at the text (a callout arrow drawn from
    its label), an arrow whose tip points at it, or a line joining it to another text (a
    tick from a note to a term of a formula). A plain line that only ends near a text,
    its other end on a drawing (a ray of a burst, a guide, a link to an inset), is not."""
    if not shape.open_path:
        return False
    try:
        p0, p1 = (Point(p[:2]) for p in (shape.mob.get_start(), shape.mob.get_end()))
    except Exception:
        return False
    if text.ink.distance(p0) < reach:
        return True
    if text.ink.distance(p1) >= reach:
        return False
    return shape.cls in ARROWS or any(t is not text and t.ink.distance(p0) < reach
                                      for t in texts)



# ---------------- contrast ----------------
def _image_rgb(img, x, y):
    px = img.pixel_array
    h, w = px.shape[:2]
    u = (x - img.get_left()[0]) / max(img.width, 1e-9)
    v = (img.get_top()[1] - y) / max(img.height, 1e-9)
    return px[int(np.clip(v * h, 0, h - 1)), int(np.clip(u * w, 0, w - 1))][:3] / 255.0


def _glyph_colors(text):
    """[(rgb, opacity)] of the distinct fills of a text's glyphs."""
    seen = {}
    for g in text.mob.family_members_with_points():
        op = float(g.get_fill_opacity())
        if op > 0.05:
            rgb = g.get_fill_rgbas()[0][:3]
            seen[(tuple(np.round(rgb, 3)), round(op, 2))] = (rgb, op)
    return list(seen.values())


def _samples(text, n=(5, 3)):
    """Points over a text where the surface is read: a grid over its box, kept if close to a
    glyph (the middle of the box if none is)."""
    x0, y0, x1, y1 = text.ink.bounds
    pts = [(x0 + (x1 - x0) * (i + 0.5) / n[0], y0 + (y1 - y0) * (j + 0.5) / n[1])
           for i in range(n[0]) for j in range(n[1])]
    near = text.core.buffer(0.04)
    pts = [p for p in pts if near.contains(Point(p))]
    return pts or [((x0 + x1) / 2, (y0 + y1) / 2)]


def surface_at(point, index, items, backdrop):
    """RGB of what is behind a text at `point`: the scene's background, then every filled
    shape and image listed before the text (below it) that covers the point, blended in
    order."""
    rgb = np.asarray(backdrop(*point), dtype=float)
    p = Point(point)
    for it in items[:index]:
        if it.kind == "image" and it.region is not None and it.region.contains(p):
            rgb = _image_rgb(it.mob, *point)
        for poly, fill, alpha in it.fills:
            if alpha > 0.05 and poly.contains(p):
                rgb = np.asarray(blend(fill, rgb, alpha))
    return rgb


def low_contrast(text, index, items, backdrop, minimum=MIN_CONTRAST):
    """(worst ratio, text rgb, surface rgb, point) if the text's contrast with what is behind
    it falls below `minimum`; None if it is readable or exempt."""
    if getattr(text.mob, "contrast_exempt", False):
        return None
    worst = None
    for rgb, op in _glyph_colors(text):
        if np.allclose(rgb, _rgb(LIGHT_INK), atol=2e-3):     # inactive text (LIGHT_INK)
            continue
        for pt in _samples(text):
            bg = surface_at(pt, index, items, backdrop)
            shown = blend(rgb, bg, op)
            r = contrast_ratio(shown, bg)
            if worst is None or r < worst[0]:
                worst = (r, shown, bg, pt)
    if worst is not None and worst[0] < minimum - 1e-6:
        return worst
    return None


def _hex(rgb):
    r, g, b = (int(round(float(v) * 255)) for v in rgb[:3])
    return f"#{r:02x}{g:02x}{b:02x}"


# ---------------- naming (for the report) ----------------
def _short(text, n=48):
    return text if len(text) <= n else text[:n - 1] + "…"


def _nearest_label(point, items, texts, reach=0.6):
    """The label nearest to a point: a text, or the text inside a closed shape (a box,
    named by its content, wins over a loose text at the same distance; a bare one- or
    two-character text, such as a badge number, loses to the label beside it)."""
    p, best = Point(point[:2]), None
    for it in items:
        if it.kind == "text":
            d, t = it.ink.distance(p), it
        elif not it.open_path:
            inner = [x for x in texts if inside(x, it.region)]
            if not inner:
                continue
            d, t = it.region.distance(p) - 0.25, max(inner, key=lambda x: len(x.text))
        else:
            continue
        if it.kind == "text" and len(t.text) <= 2:
            d += 0.25
        if d <= reach and (best is None or d < best[0]):
            best = (d, t)
    return best[1] if best else None


def describe(it, texts, items=()):
    """A readable name: Text 'Guide block', Arrow from 'Motor' to 'M', Rectangle around 'M'."""
    if it.kind == "text":
        return f"Text '{_short(it.text)}'"
    if it.kind == "image":
        return f"Image at {cells(it.ink.bounds)}"
    if it.open_path:
        try:
            p0, p1 = it.mob.get_start(), it.mob.get_end()
        except Exception:
            p0 = p1 = None
        v = np.asarray(p1) - np.asarray(p0) if p0 is not None else np.zeros(3)
        if np.linalg.norm(v) > 1e-3:
            v = v / np.linalg.norm(v) * 0.12          # look just behind the start, past the tip
            others = [o for o in (items or texts) if o is not it and not (
                o.kind == "text" and o.ink.intersection(it.ink).area >= MIN_AREA)]
            a = _nearest_label(np.asarray(p0) - v, others, texts)
            b = _nearest_label(np.asarray(p1) + v, others, texts)
            start = f"'{_short(a.text, 30)}'" if a else cell(*p0[:2])
            end = f"'{_short(b.text, 30)}'" if b else cell(*p1[:2])
            return f"{it.cls} from {start} to {end}"
    if it.region is not None:
        inner = [t for t in texts if inside(t, it.region)]
        if inner:
            return f"{it.cls} around '{_short(max(inner, key=lambda t: len(t.text)).text, 30)}'"
    return f"{it.cls} at {cells(it.ink.bounds)}"


def _element(it, texts, items=()):
    x0, y0, x1, y1 = it.ink.bounds
    e = {"name": describe(it, texts, items), "kind": it.kind, "class": it.cls,
         "bbox": [round(v, 3) for v in (x0, y0, x1, y1)], "cells": cells((x0, y0, x1, y1))}
    if it.kind == "text":
        e["text"] = it.text
        if it.font is not None:
            e["font_size"] = round(it.font, 1)
    return e


# ---------------- analysis ----------------
class Finding:
    def __init__(self, kind, a, b=None, geom=None, **extra):
        self.kind, self.a, self.b, self.geom, self.extra = kind, a, b, geom, extra
        self.severity = SEVERITY[kind]
        self.key = (kind, id(a.mob), a.text or a.cls,
                    id(b.mob) if b else 0, (b.text or b.cls) if b else "")

    def amount(self):
        return self.geom.area if self.geom is not None else self.extra.get("amount", 0)


def analyse(items, margin=SAFE_MARGIN, min_font=MIN_FONT_SIZE, min_area=MIN_AREA,
            clearance=CLEARANCE, backdrop=None, min_contrast=MIN_CONTRAST, frame=True):
    """Every fault on screen now, as Findings. backdrop(x, y) -> RGB is the scene's
    background (the theme's BG when omitted); frame=False skips the frame and safe-margin
    rules (the content is magnified on purpose: motion.zoom_on)."""
    backdrop = backdrop or (lambda x, y: _rgb(BG))
    texts = [i for i in items if i.kind == "text"]
    shapes = [i for i in items if i.kind != "text"]
    found = []
    if texts:
        tree = STRtree([t.ink for t in texts])
        for i, a in enumerate(texts):
            for j in tree.query(a.ink, predicate="intersects"):
                if j > i:
                    ov = a.ink.intersection(texts[j].ink)
                    if ov.area >= min_area:
                        found.append(Finding("text_overlap", a, texts[j], ov))
    if texts and shapes:
        tree = STRtree([s.ink for s in shapes])
        for a in texts:
            for j in tree.query(a.ink, predicate="dwithin", distance=max(clearance, 1e-9)):
                s = shapes[j]
                if inside(a, s.region, min_area):
                    if s.outline is not None:           # inside its frame: fine unless it touches
                        ov = a.core.intersection(s.outline)
                        if ov.area >= min_area:
                            found.append(Finding("text_touches_frame", a, s, ov))
                    continue
                if struck_through(a, s):
                    continue
                ov = a.ink.intersection(s.ink)
                if ov.area >= min_area:
                    found.append(Finding("text_over_shape", a, s, ov))
                    continue
                # touching or too close: no overlap area, so measured as a distance between
                # the letters and the shape's ink (which already includes its stroke width)
                gap = a.glyphs.distance(s.ink)
                if gap < clearance and not leader_of(a, s, texts):
                    p = nearest_points(a.glyphs, s.ink)[0]
                    found.append(Finding("text_near_shape", a, s, amount=clearance - gap,
                                         gap=gap, clearance=clearance, at=(p.x, p.y)))
    for k, it in enumerate(items):
        if it.kind == "text":
            worst = low_contrast(it, k, items, backdrop, min_contrast)
            if worst:
                ratio, shown, bg, (x, y) = worst
                found.append(Finding("low_contrast", it, amount=min_contrast - ratio,
                                     ratio=ratio, minimum=min_contrast,
                                     text=_hex(shown), surface=_hex(bg), at=(x, y)))
    fw, fh = config.frame_width / 2, config.frame_height / 2
    for it in items:
        if frame:
            x0, y0, x1, y1 = it.ink.bounds
            side, over = max({"RIGHT": x1 - fw, "LEFT": -fw - x0, "UP": y1 - fh,
                              "DOWN": -fh - y0}.items(), key=lambda kv: kv[1])
            if over > 0.01:
                found.append(Finding("out_of_frame", it, amount=over, side=side))
            elif it.kind == "text" and over + margin > 0.01:
                found.append(Finding("in_safe_margin", it, amount=over + margin, side=side))
        if it.kind == "text" and it.font is not None and it.font < min_font - 0.05:
            found.append(Finding("text_too_small", it, amount=it.font))
    return found


# ---------------- fix suggestions ----------------
def _free_moves(it, items, offenders, margin, step=0.05, reach=2.5, pad=0.0):
    """Shortest moves [(distance, direction), ...] that clear `it` of every obstacle and
    keep it in the safe area. A text moves together with its small label group (e.g. the
    badge of a callout); its own leader arrow and a frame that contains it move with it,
    so they are not obstacles; the offenders always are."""
    fw, fh = config.frame_width / 2 - margin, config.frame_height / 2 - margin
    group = [o for o in items if o.root == it.root and o.ink.distance(it.ink) < ATTACHED]
    if any(o.ink.intersects(off.ink) for o in group if o is not it for off in offenders):
        group = [it]
    body = unary_union([o.ink for o in group])
    obstacles = [o.ink.buffer(pad) if pad else o.ink for o in offenders]
    for o in items:
        if o in group or o in offenders:
            continue
        if inside(it, o.region):
            continue                                    # its frame or panel
        if o.open_path and not o.ink.intersects(body):
            try:
                if Point(o.mob.get_start()[:2]).distance(body) < 0.2:
                    continue                            # its own leader arrow
            except Exception:
                pass
        obstacles.append(o.ink)
    tree = STRtree(obstacles) if obstacles else None
    moves = []
    for name, (dx, dy) in DIRECTIONS.items():
        for k in range(1, int(reach / step) + 1):
            g = translate(body, dx * k * step, dy * k * step)
            x0, y0, x1, y1 = g.bounds
            if x0 < -fw or x1 > fw or y0 < -fh or y1 > fh:
                break
            if tree is None or not len(tree.query(g, predicate="intersects")):
                moves.append((round(k * step, 2), name))
                break
    return sorted(moves)


def _move_text(name, moves):
    if not moves:
        return f"No free spot within 2.5 units: rearrange the group around {name}"
    d, where = moves[0]
    alt = f" (or {moves[1][1]} by {moves[1][0]:.2f})" if len(moves) > 1 else ""
    return f"Move {name} {where} by {d:.2f}{alt} — e.g. .shift({where} * {d:.2f})"


def suggest(f, items, texts, margin):
    a, b = f.a, f.b
    name_a = describe(a, texts, items)
    if f.kind == "text_overlap":
        ma = _free_moves(a, items, [b], margin)
        mb = _free_moves(b, items, [a], margin)
        if mb and (not ma or mb[0][0] < ma[0][0]):
            a, ma, name_a = b, mb, describe(b, texts, items)
        return (_move_text(name_a, ma) + "; lay texts out with next_to()/arrange() "
                "(buff ≥ 0.15) instead of fixed coordinates")
    if f.kind == "text_over_shape":
        s = _move_text(name_a, _free_moves(a, items, [b], margin))
        if b.open_path:
            return s + f"; or re-route {describe(b, texts, items)} (another callout direction or " \
                       "end point) so it does not cross the text"
        return s + " — keep labels off the drawing, placed with next_to()"
    if f.kind == "text_near_shape":
        pad = f.extra["clearance"] + 0.05
        s = _move_text(name_a, _free_moves(a, items, [b], margin, pad=pad))
        return s + (f" to keep ≥ {pad:.2f} from {describe(b, texts, items)} "
                    f"(gap now {f.extra['gap']:.3f}) — place it with next_to(..., buff ≥ 0.15)")
    if f.kind == "text_touches_frame":
        return (f"Keep {name_a} clear of the outline of {describe(b, texts, items)}: shrink the text "
                "(scale_to_fit_width(frame width − 0.3)) or enlarge the frame")
    if f.kind in ("out_of_frame", "in_safe_margin"):
        amount, side = f.extra["amount"], f.extra["side"]
        move = amount + (margin if f.kind == "out_of_frame" and a.kind == "text" else 0)
        width = a.ink.bounds[2] - a.ink.bounds[0]
        tip = f"Shift {name_a} {OPPOSITE[side]} by {move:.2f}"
        if side in ("LEFT", "RIGHT") and width > config.frame_width - 2 * margin:
            tip = f"{name_a} is {width:.2f} wide: shrink it with fit() (SAFE_WIDTH {SAFE_WIDTH})"
        return tip + f" to keep {margin} clear of the frame edge"
    if f.kind == "low_contrast":
        e = f.extra
        return (f"{name_a} is {e['text']} on {e['surface']}: {f.extra['ratio']:.1f}:1, below "
                f"{e['minimum']}:1. Use INK or GREY_INK (or an accent) for text, not LIGHT_INK "
                "or a colour near the background; on a filled panel pick the token that suits "
                "the panel; over an image raise `dim` in scene.background()")
    if f.kind == "text_too_small":
        return (f"{name_a} is font size {f.extra['amount']:.1f} (< {MIN_FONT_SIZE}): use a "
                "larger font_size, shorten the text, or let fit()/scale shrink it less")
    return ""


# ---------------- the checker ----------------
class OverlapChecker:
    """Called by SyncedScene after every animation in QA mode; findings become intervals."""

    def __init__(self, safe_margin=SAFE_MARGIN, min_font_size=MIN_FONT_SIZE, min_area=MIN_AREA,
                 clearance=CLEARANCE, min_contrast=MIN_CONTRAST):
        self.margin, self.min_font, self.min_area = safe_margin, min_font_size, min_area
        self.min_contrast = min_contrast
        self.clearance = clearance
        self.open, self.done = {}, []
        self.checks, self.last_time = 0, 0.0

    def check(self, scene, t):
        self.checks += 1
        self.last_time = t
        items = collect(scene.mobjects)
        texts = [i for i in items if i.kind == "text"]
        now = {}
        backdrop = getattr(scene, "background_color_at", None)
        frame = not getattr(scene, "zoomed", False)
        for f in analyse(items, self.margin, self.min_font, self.min_area, self.clearance,
                         backdrop=backdrop, min_contrast=self.min_contrast, frame=frame):
            now.setdefault(f.key, f)
        for key, f in now.items():
            rec = self.open.get(key)
            if rec is None:
                self.open[key] = self._record(f, t, items, texts)
            else:
                rec["until"] = round(t, 2)
                if f.amount() > rec["_peak"]:
                    rec["_peak"] = f.amount()
                    rec["overlap"] = self._amount(f)
        for key in [k for k in self.open if k not in now]:
            rec = self.open.pop(key)
            rec["until"] = round(t, 2)         # gone by the end of this animation
            self.done.append(rec)

    def _amount(self, f):
        if f.geom is not None:
            c = f.geom.centroid
            out = {"area": round(f.geom.area, 4),
                   "share_of_text": round(f.geom.area / max(f.a.ink.area, 1e-9), 3),
                   "at": [round(c.x, 3), round(c.y, 3)], "cell": cell(c.x, c.y)}
            if f.kind == "text_overlap":
                out["share_of_text"] = round(
                    f.geom.area / max(min(f.a.ink.area, f.b.ink.area), 1e-9), 3)
            return out
        if f.kind == "text_too_small":
            return {"font_size": round(f.extra["amount"], 1), "minimum": self.min_font}
        if f.kind == "low_contrast":
            x, y = f.extra["at"]
            return {"ratio": round(f.extra["ratio"], 2), "minimum": f.extra["minimum"],
                    "text_color": f.extra["text"], "background": f.extra["surface"],
                    "at": [round(x, 3), round(y, 3)], "cell": cell(x, y)}
        if f.kind == "text_near_shape":
            x, y = f.extra["at"]
            return {"gap": round(f.extra["gap"], 3), "clearance": f.extra["clearance"],
                    "at": [round(x, 3), round(y, 3)], "cell": cell(x, y)}
        return {"distance": round(f.extra["amount"], 3), "side": f.extra["side"],
                "limit": "frame edge" if f.kind == "out_of_frame"
                else f"safe margin {self.margin}"}

    def _record(self, f, t, items, texts):
        return {"type": f.kind, "severity": f.severity,
                "time": round(t, 2), "until": round(t, 2),
                "a": _element(f.a, texts, items), "b": _element(f.b, texts, items) if f.b else None,
                "overlap": self._amount(f),
                "suggestion": suggest(f, items, texts, self.margin), "_peak": f.amount()}

    def findings(self):
        out = self.done + list(self.open.values())
        for r in self.open.values():
            r["until"] = round(self.last_time, 2)
        return sorted(({k: v for k, v in r.items() if not k.startswith("_")} for r in out),
                      key=lambda r: (r["time"], r["type"]))

    def write(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(
            {"settings": self.settings(), "checks": self.checks,
             "last_time": round(self.last_time, 2), "findings": self.findings()},
            ensure_ascii=False, indent=1))

    def settings(self):
        return {"safe_margin": self.margin, "min_font_size": self.min_font,
                "min_area": self.min_area, "clearance": self.clearance,
                "min_contrast": self.min_contrast,
                "frame": [round(config.frame_width, 3), round(config.frame_height, 3)],
                "grid": "6x6: columns A-F left to right, rows 1-6 top to bottom"}


# ---------------- per-segment reports ----------------
def group_findings(findings):
    """Single-element findings of one kind that appear together (a menu bar of small
    texts, a list inside the margin) become one record that lists its elements."""
    out, groups = [], {}
    for f in findings:
        if f["b"] is None:
            groups.setdefault((f["type"], f["time"], f["overlap"].get("side")), []).append(f)
        else:
            out.append(f)
    for fs in groups.values():
        if len(fs) == 1:
            out.append(fs[0])
            continue
        f0, n = fs[0], len(fs)
        names = [x["a"].get("text") or x["a"]["name"] for x in fs]
        boxes = np.array([x["a"]["bbox"] for x in fs])
        bounds = (boxes[:, 0].min(), boxes[:, 1].min(), boxes[:, 2].max(), boxes[:, 3].max())
        members = f"{n} texts: " + ", ".join(f"'{_short(t, 24)}'" for t in names[:6]) \
            + (" …" if n > 6 else "")
        rec = {**f0, "until": max(x["until"] for x in fs),
               "a": {"name": members, "kind": "group", "cells": cells(bounds),
                     "bbox": [round(float(v), 3) for v in bounds],
                     "members": [x["a"] for x in fs]}}
        if f0["type"] == "low_contrast":
            worst = min(x["overlap"]["ratio"] for x in fs)
            rec["overlap"] = {**f0["overlap"], "ratio": worst}
            rec["suggestion"] = (f"{n} texts below {f0['overlap']['minimum']}:1 (worst "
                                 f"{worst}:1): use INK, GREY_INK or an accent for them; "
                                 "details in each member")
        elif f0["type"] == "text_too_small":
            sizes = [x["overlap"]["font_size"] for x in fs]
            rec["overlap"] = {**f0["overlap"], "font_size": [min(sizes), max(sizes)]}
            size = f"{min(sizes)}" if min(sizes) == max(sizes) else f"{min(sizes)}–{max(sizes)}"
            rec["suggestion"] = (f"{n} texts at font size {size} "
                                 f"(< {f0['overlap']['minimum']}): enlarge them, show fewer, or "
                                 "draw that part larger")
        else:
            far = max(x["overlap"]["distance"] for x in fs)
            rec["overlap"] = {**f0["overlap"], "distance": far}
            rec["suggestion"] = (f"Shift the {n} texts (as one group) "
                                 f"{OPPOSITE[f0['overlap']['side']]} by {far:.2f}, "
                                 f"or shrink the group with fit()")
        out.append(rec)
    return sorted(out, key=lambda r: (r["time"], r["type"]))


def report_by_segment(raw_path, starts, out_dir, segments, offset=0.0, meta=None):
    """Split the raw findings into overlap/segNN.json, one per narration segment.

    A finding is listed in every segment during which it is on screen; findings of one
    kind that appear together are grouped (group_findings). starts: segment start times
    plus the total length (segment_starts); segments: 1-based numbers.
    """
    raw = json.loads(Path(raw_path).read_text())
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {}
    findings = group_findings(raw["findings"])
    for k in segments:
        s, e = starts[k - 1], starts[k]
        rows = []
        for f in findings:
            if f["time"] < e - 1e-3 and (f["until"] > s + 1e-3 or f["time"] >= s - 1e-3):
                rows.append({**f, "video_time": round(f["time"] - offset, 2)})
        counts = {sev: sum(r["severity"] == sev for r in rows)
                  for sev in ("critical", "improvement")}
        (out_dir / f"seg{k:02d}.json").write_text(json.dumps(
            {**(meta or {}), "segment": k, "start": round(s, 2), "end": round(e, 2),
             "clock_offset": round(offset, 3), "settings": raw["settings"],
             "counts": counts, "findings": rows}, ensure_ascii=False, indent=1))
        summary[k] = counts
    return summary
