"""Scene library: ready-made whiteboard building blocks for explainer videos.

Every function takes the running scene first, draws its block with animations and
returns the group so the caller can move, highlight or clear it later. Staged blocks
take `cues`: one absolute time per item (usually from scene.cue(seg, phrase)); each item
appears when its time comes. Without cues the items follow each other directly.

    title_card        opening title, subtitle, series line
    section_title     small heading in the top-left corner (transforms the previous one)
    bullet_list       points revealed one by one
    equation          equation built from Text pieces (no LaTeX), indexable by part
    worked_calculation   formula -> substituted values -> boxed result
    labeled_diagram   any drawing + numbered callouts with arrows
    process_flow      boxes joined by arrows; highlight_step() lights one
    stage_bar         row of stages with a marker; set_stage() moves it
    data_table        grid with header and shaded rows; highlight_row() marks one
    comparison        two cards side by side, optional verdict tick
    line_chart        trend on axes with an acceptance band; out-of-band points in red
    bar_chart         bars with values and an optional limit line
    checklist         items ticked (or crossed) one by one
    summary_box       framed key takeaways
    concept_map       central idea linked to surrounding ideas (topics without numbers)
    timeline          dated events along an arrow (topics without numbers)
    image_panel       framed picture (PNG/JPG/SVG) with caption (topics without numbers)
    document_panel    monospaced sheet (report, form, log); highlight() frames lines
Helpers: emphasize() draws a box around any part; badge() is a numbered circle.
"""
from pathlib import Path

import numpy as np
from manim import *

from .style import (ACCENT_1, ACCENT_3, ALERT_C, BG, FS_AXIS, FS_BODY, FS_EQUATION,
                    FS_HEADING, FS_LABEL, FS_NOTE, FS_SUBTITLE, FS_SUMMARY, FS_TAG,
                    FS_TITLE, GREY_INK, INK, LIGHT_INK, MONO, OK_C, PANEL_FILL, SAFE_WIDTH,
                    fit, label)

__all__ = ["title_card", "section_title", "bullet_list", "equation", "worked_calculation",
           "labeled_diagram", "process_flow", "highlight_step", "stage_bar", "set_stage",
           "data_table", "highlight_row", "comparison", "line_chart", "bar_chart",
           "checklist", "summary_box", "concept_map", "timeline", "image_panel",
           "document_panel", "highlight", "emphasize", "badge", "LIBRARY"]


# ---------------- internals ----------------
def _reveal(scene, items, cues, make_anim, run_time=0.6):
    """Play make_anim(item) for each item, waiting for its cue time if given."""
    for k, item in enumerate(items):
        if cues is not None and k < len(cues) and cues[k] is not None:
            scene.sync(cues[k])
        scene.play(make_anim(item), run_time=run_time)


def _box(text_mob, color=INK, pad=0.25, fill=None, corner=0.12, width=3):
    r = RoundedRectangle(width=text_mob.width + 2 * pad, height=text_mob.height + 2 * pad,
                         corner_radius=corner, stroke_width=width, color=color)
    if fill:
        r.set_fill(fill, 1)
    r.move_to(text_mob)
    return VGroup(r, text_mob)


def _exit_point(mob, target):
    """Where the line from mob's centre to `target` leaves mob's bounding box."""
    c = mob.get_center()
    v = np.array(target) - c
    half = np.array([mob.width / 2, mob.height / 2])
    t = min(half[i] / abs(v[i]) for i in range(2) if abs(v[i]) > 1e-9)
    return c + v * min(t, 1.0)


def badge(n, color=INK, radius=0.24):
    """Numbered circle."""
    c = Circle(radius=radius, stroke_width=3, color=color).set_fill(BG, 1)
    t = label(str(n), FS_TAG, color, weight=BOLD).move_to(c)
    return VGroup(c, t)


def emphasize(scene, mob, color=ACCENT_1, buff=0.12, run_time=0.6):
    """Draw a rounded box around `mob`; returns the box."""
    box = SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.1,
                               stroke_width=4)
    scene.play(Create(box), run_time=run_time)
    return box


# ---------------- 1 title_card ----------------
def title_card(scene, title, subtitle=None, series=None, y=1.2, run_time=2.0):
    """Opening title with a rule; optional series line above and subtitle below."""
    head = fit(Text(title, font_size=FS_TITLE, weight=BOLD))
    rule = Line(LEFT, RIGHT).set_width(head.width)
    parts = [head, rule]
    if series:
        parts.insert(0, label(series, FS_SUBTITLE, GREY_INK))
    if subtitle:
        parts.append(fit(label(subtitle, FS_SUBTITLE)))
    group = VGroup(*parts).arrange(DOWN, buff=0.35).move_to(UP * y)
    anims = [Write(head), Create(rule)]
    anims += [FadeIn(p, shift=UP * 0.15) for p in parts if p not in (head, rule)]
    scene.play(*anims, run_time=run_time)
    return group


# ---------------- 2 section_title ----------------
def section_title(scene, text, prev=None, run_time=0.6):
    """Heading in the top-left corner. Pass the previous heading to transform it."""
    new = label(text, FS_BODY - 6, weight=BOLD).to_corner(UL, buff=0.4)
    if prev is not None:
        scene.play(Transform(prev, new), run_time=run_time)
        return prev
    scene.play(Write(new), run_time=run_time)
    return new


# ---------------- 3 bullet_list ----------------
def bullet_list(scene, items, heading=None, cues=None, numbered=False, pos=ORIGIN,
                size=FS_BODY, width=SAFE_WIDTH):
    """Points revealed one by one (at `cues` if given)."""
    marks = [f"{k + 1}." if numbered else "•" for k in range(len(items))]
    rows = VGroup(*[label(f"{m}  {t}", size) for m, t in zip(marks, items)])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    group = VGroup(rows)
    if heading:
        head = label(heading, FS_HEADING, weight=BOLD)
        group = VGroup(head, rows).arrange(DOWN, buff=0.5)
        rows.align_to(head, LEFT).shift(RIGHT * 0.3)
    fit(group, width).move_to(pos)
    if heading:
        scene.play(Write(group[0]), run_time=0.8)
    _reveal(scene, rows, cues, lambda m: FadeIn(m, shift=RIGHT * 0.2))
    return group


# ---------------- 4 equation ----------------
def equation(scene, parts, colors=None, size=FS_EQUATION, pos=ORIGIN, run_time=1.5,
             buff=0.18):
    """Equation from Text pieces, e.g. ["MF", "=", "Vp", "÷", "Vm"]; group[k] is part k."""
    colors = colors or {}
    eq = VGroup(*[Text(p, font_size=size, color=colors.get(k, INK))
                  for k, p in enumerate(parts)]).arrange(RIGHT, buff=buff)
    fit(eq).move_to(pos)
    scene.play(Write(eq), run_time=run_time)
    return eq


# ---------------- 5 worked_calculation ----------------
def worked_calculation(scene, formula, values, result, cues=None, pos=ORIGIN,
                       color=ACCENT_1, size=FS_EQUATION):
    """Three lines: formula, the same with values substituted, then the boxed result.

    formula / values are lists of Text pieces; result is a string like "= 0.99900".
    """
    f = VGroup(*[Text(p, font_size=size) for p in formula]).arrange(RIGHT, buff=0.18)
    v = VGroup(*[Text(p, font_size=size - 4, color=GREY_INK) for p in values])
    v.arrange(RIGHT, buff=0.18)
    r = Text(result, font_size=size + 4, color=color, weight=BOLD)
    group = fit(VGroup(f, v, r).arrange(DOWN, buff=0.55)).move_to(pos)
    frame = SurroundingRectangle(r, color=color, buff=0.18, corner_radius=0.1,
                                 stroke_width=4)
    steps = [Write(f), FadeIn(v, shift=DOWN * 0.15),
             AnimationGroup(Write(r), Create(frame))]
    _reveal(scene, steps, cues, lambda a: a, run_time=1.0)
    group.add(frame)
    return group


# ---------------- 6 labeled_diagram ----------------
def labeled_diagram(scene, diagram, callouts, cues=None, numbered=True, color=INK,
                    draw_time=2.0, start=1):
    """Draw `diagram`, then callouts [(text, target, direction), ...] one by one.

    start is the first badge number: to reveal callouts in batches with other
    animations between them, call it again with an invisible diagram and start=n.

    target is a point or a mobject; direction (UP, DR, ...) places the label.
    """
    scene.play(Create(diagram), run_time=draw_time)
    notes = VGroup()
    for k, (text, target, direction) in enumerate(callouts):
        d = normalize(direction)
        if isinstance(target, Mobject):          # tip on the edge facing the label
            point = target.get_critical_point(np.sign(np.round(d, 6)))
            tip = point + d * 0.08
        else:
            point = np.array(target, dtype=float)
            tip = point + d * 0.15
        txt = label(text, FS_LABEL, color)
        item = VGroup(badge(start + k, color), txt).arrange(RIGHT, buff=0.15) if numbered \
            else VGroup(txt)
        # centre the label 0.8 beyond the tip, measured from its edge facing the target
        reach = abs(d[0]) * item.width / 2 + abs(d[1]) * item.height / 2
        item.move_to(point + d * (0.8 + reach))
        arrow = Arrow(_exit_point(item, tip), tip, buff=0.08, stroke_width=3, color=color,
                      max_tip_length_to_length_ratio=0.2)
        notes.add(VGroup(item, arrow))
    _reveal(scene, notes, cues, lambda m: AnimationGroup(FadeIn(m[0]), GrowArrow(m[1])))
    return VGroup(diagram, notes)


# ---------------- 7 process_flow ----------------
def process_flow(scene, steps, cues=None, color=INK, vertical=False, pos=ORIGIN,
                 size=FS_LABEL, width=SAFE_WIDTH):
    """Boxes joined by arrows; group[0] are the boxes, group[1] the arrows."""
    boxes = VGroup(*[_box(label(s, size, color), color) for s in steps])
    boxes.arrange(DOWN if vertical else RIGHT, buff=0.55 if vertical else 0.7)
    fit(boxes, width).move_to(pos)
    arrows = VGroup(*[Arrow(boxes[i].get_bottom() if vertical else boxes[i].get_right(),
                            boxes[i + 1].get_top() if vertical else boxes[i + 1].get_left(),
                            buff=0.08, stroke_width=3, color=color,
                            max_tip_length_to_length_ratio=0.3)
                      for i in range(len(boxes) - 1)])
    items = [(boxes[0], None)] + [(boxes[i + 1], arrows[i]) for i in range(len(arrows))]
    _reveal(scene, items, cues,
            lambda it: AnimationGroup(*([GrowArrow(it[1])] if it[1] else []),
                                      FadeIn(it[0], shift=RIGHT * 0.15), lag_ratio=0.4))
    return VGroup(boxes, arrows)


def highlight_step(scene, flow, k, color=ACCENT_1, run_time=0.5):
    """Light step k of a process_flow (others return to their normal look)."""
    anims = []
    for i, b in enumerate(flow[0]):
        on = i == k
        anims.append(b[0].animate.set_stroke(color if on else INK, 5 if on else 3)
                     .set_fill(color, 0.12 if on else 0))
    scene.play(*anims, run_time=run_time)


# ---------------- 8 stage_bar ----------------
def stage_bar(scene, stages, active=0, y=-2.6, color=ACCENT_1, width=SAFE_WIDTH):
    """Row of stage names with a marker under the active one; returns the bar."""
    cells = VGroup(*[label(f"{k + 1}  {s}", FS_TAG + 2) for k, s in enumerate(stages)])
    cells.arrange(RIGHT, buff=0.6)
    fit(cells, width - 0.4)
    frame = RoundedRectangle(width=cells.width + 0.5, height=cells.height + 0.45,
                             corner_radius=0.15, stroke_width=3, color=GREY_INK)
    bar = VGroup(frame, cells).move_to([0, y, 0])
    cells.move_to(frame)
    marker = Line(LEFT, RIGHT, stroke_width=7, color=color)
    bar.add(marker)
    _place_marker(bar, active, color)
    scene.play(Create(frame), FadeIn(cells), run_time=0.8)
    scene.play(Create(marker), run_time=0.4)
    return bar


def _place_marker(bar, k, color):
    frame, cells, marker = bar
    marker.set_width(cells[k].width).next_to(cells[k], DOWN, 0.08)
    for i, c in enumerate(cells):
        c.set_color(color if i == k else LIGHT_INK)
        c.set_opacity(1)


def set_stage(scene, bar, k, color=ACCENT_1, run_time=0.5):
    """Move the stage_bar marker to stage k."""
    target = bar.copy()
    _place_marker(target, k, color)
    scene.play(Transform(bar, target), run_time=run_time)


# ---------------- 9 data_table ----------------
def data_table(scene, header, rows, cues=None, pos=ORIGIN, size=FS_TAG + 2,
               col_buff=0.6, width=SAFE_WIDTH):
    """Grid with a bold header, a rule, shaded alternate rows; rows appear in turn.

    Returns VGroup(header_row, rule, body) where body[r] is VGroup(shade, cells).
    """
    table = [header] + [[str(c) for c in r] for r in rows]
    cells = [[Text(str(c), font_size=size, font=MONO,
                   weight=BOLD if r == 0 else NORMAL) for c in row]
             for r, row in enumerate(table)]
    col_w = [max(cells[r][c].width for r in range(len(cells))) for c in range(len(header))]
    row_h = max(m.height for row in cells for m in row) + 0.28
    xs = np.cumsum([0] + [w + col_buff for w in col_w[:-1]])
    total_w = xs[-1] + col_w[-1]
    lines = []
    for r, row in enumerate(cells):
        y = -r * row_h
        for c, m in enumerate(row):
            # first column left-aligned, the others right-aligned (numbers)
            if c == 0:
                m.move_to([xs[c], y, 0], aligned_edge=LEFT)
            else:
                m.move_to([xs[c] + col_w[c], y, 0], aligned_edge=RIGHT)
        lines.append(VGroup(*row))
    head = lines[0]
    rule = Line([-0.15, -row_h / 2, 0], [total_w + 0.15, -row_h / 2, 0], stroke_width=3)
    body = VGroup()
    for r, line in enumerate(lines[1:], start=1):
        shade = Rectangle(width=total_w + 0.3, height=row_h, stroke_width=0)
        shade.set_fill(PANEL_FILL if r % 2 else BG, 1)
        shade.move_to([total_w / 2, -r * row_h, 0])
        body.add(VGroup(shade, line))
    group = VGroup(head, rule, body)
    fit(group, width).move_to(pos)
    scene.play(FadeIn(head), Create(rule), run_time=0.7)
    _reveal(scene, body, cues, lambda m: FadeIn(m, shift=DOWN * 0.1), run_time=0.4)
    return group


def highlight_row(scene, table, r, color=ACCENT_1, run_time=0.5):
    """Mark body row r (0-based) of a data_table; returns the frame."""
    row = table[2][r]
    box = SurroundingRectangle(row, color=color, buff=0.03, stroke_width=4)
    scene.play(Create(box), row[1].animate.set_color(color), run_time=run_time)
    return box


# ---------------- 10 comparison ----------------
def comparison(scene, left, right, colors=(GREY_INK, ACCENT_1), verdict=None, cues=None,
               card_w=5.6, pos=ORIGIN):
    """Two cards (title, lines...) side by side; verdict "left"/"right" adds a tick."""
    cards = VGroup()
    for (title, *lines), color in zip((left, right), colors):
        txt = VGroup(label(title, FS_BODY, color, weight=BOLD),
                     *[label(t, FS_LABEL, color) for t in lines]).arrange(DOWN, buff=0.2)
        fit(txt, card_w - 0.5)
        frame = Rectangle(width=card_w, height=max(txt.height + 0.8, 3.0), stroke_width=4,
                          color=color)
        txt.move_to(frame)
        cards.add(VGroup(frame, txt))
    cards.arrange(RIGHT, buff=1.0)
    fit(cards).move_to(pos)
    vs = label("vs", FS_BODY, GREY_INK).move_to(cards)
    steps = [FadeIn(cards[0], shift=RIGHT * 0.2),
             AnimationGroup(FadeIn(vs), FadeIn(cards[1], shift=LEFT * 0.2))]
    group = VGroup(cards, vs)
    if verdict:
        k = 0 if verdict == "left" else 1
        tick = label("✓", FS_HEADING, OK_C, weight=BOLD)
        tick.next_to(cards[k][0], UP, 0.1).align_to(cards[k][0], RIGHT)
        steps.append(AnimationGroup(FadeIn(tick, scale=1.5),
                                    cards[k][0].animate.set_stroke(OK_C, 6)))
        group.add(tick)
    _reveal(scene, steps, cues, lambda a: a, run_time=0.8)
    return group


# ---------------- 11 line_chart ----------------
def line_chart(scene, xs, ys, x_label="", y_label="", band=None, x_range=None,
               y_range=None, size=(8.0, 4.2), pos=ORIGIN, color=ACCENT_1, run_time=2.5,
               decimals=2):
    """Trend drawn point by point; optional acceptance band (lo, hi), outliers in red."""
    xs, ys = list(xs), list(ys)
    x_range = x_range or [min(xs), max(xs), max((max(xs) - min(xs)) / 5, 1e-9)]
    if y_range is None:
        lo = min(ys + ([band[0]] if band else []))
        hi = max(ys + ([band[1]] if band else []))
        pad = (hi - lo) * 0.25 or 1
        y_range = [lo - pad, hi + pad, (hi - lo + 2 * pad) / 4]
    ax = Axes(x_range=x_range, y_range=y_range, x_length=size[0], y_length=size[1],
              tips=False, axis_config={"color": INK, "stroke_width": 3,
                                       "include_ticks": True, "tick_size": 0.05})
    # tick numbers as Text (DecimalNumber needs LaTeX, absent in the container)
    nums = VGroup(*[label(f"{v:.0f}", FS_TAG - 2).next_to(ax.c2p(v, y_range[0]), DOWN, 0.12)
                    for v in np.arange(x_range[0], x_range[1] + 1e-9, x_range[2])])
    nums.add(*[label(f"{v:.{decimals}f}", FS_TAG - 2).next_to(ax.c2p(x_range[0], v), LEFT, 0.12)
               for v in np.arange(y_range[0], y_range[1] + 1e-9, y_range[2])])
    xl = label(x_label, FS_AXIS).next_to(nums, DOWN, 0.2).set_x(ax.get_center()[0])
    yl = label(y_label, FS_AXIS).rotate(PI / 2).next_to(nums, LEFT, 0.2)
    yl.set_y(ax.get_center()[1])
    group = VGroup(ax, nums, xl, yl)
    parts = [Create(ax), FadeIn(nums), FadeIn(xl), FadeIn(yl)]
    if band:
        x0, x1 = ax.c2p(x_range[0], 0)[0], ax.c2p(x_range[1], 0)[0]
        y0, y1 = ax.c2p(0, band[0])[1], ax.c2p(0, band[1])[1]
        zone = Rectangle(width=x1 - x0, height=y1 - y0, stroke_width=0)
        zone.set_fill(OK_C, 0.10).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
        edges = VGroup(*[DashedLine([x0, y, 0], [x1, y, 0], stroke_width=2, color=OK_C)
                         for y in (y0, y1)])
        ax_band = VGroup(zone, edges)
        group.add(ax_band)
        parts.append(FadeIn(ax_band))
    group.move_to(pos)
    scene.play(*parts, run_time=1.2)
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys)]
    path = VMobject(color=color, stroke_width=4).set_points_as_corners(pts)
    dots = VGroup(*[Dot(p, radius=0.07, color=ALERT_C if band and not band[0] <= y <= band[1]
                        else color) for p, y in zip(pts, ys)])
    scene.play(Create(path), LaggedStart(*[FadeIn(d, scale=1.6) for d in dots],
                                         lag_ratio=0.3), run_time=run_time)
    group.add(path, dots)
    return group


# ---------------- 12 bar_chart ----------------
def bar_chart(scene, labels, values, unit="", limit=None, limit_label="limit",
              colors=None, height=3.6, bar_w=0.9, pos=ORIGIN, decimals=1, cues=None):
    """Vertical bars with their values; optional dashed limit line (bars above it in red)."""
    top = max(list(values) + ([limit] if limit is not None else [])) * 1.15
    scale = height / top
    colors = colors or [ACCENT_1] * len(values)
    base = Line(LEFT * (len(values) * (bar_w + 0.6) / 2 + 0.3),
                RIGHT * (len(values) * (bar_w + 0.6) / 2 + 0.3), stroke_width=3)
    bars, texts = VGroup(), VGroup()
    for k, (name, v) in enumerate(zip(labels, values)):
        x = (k - (len(values) - 1) / 2) * (bar_w + 0.6)
        c = ALERT_C if limit is not None and v > limit else colors[k]
        b = Rectangle(width=bar_w, height=max(v * scale, 0.02), stroke_width=3, color=c)
        b.set_fill(c, 0.35).move_to([x, 0, 0], aligned_edge=DOWN)
        val = label(f"{v:.{decimals}f}{unit}", FS_TAG, c, weight=BOLD).next_to(b, UP, 0.1)
        nm = label(name, FS_TAG).next_to([x, 0, 0], DOWN, 0.2)
        bars.add(b)
        texts.add(VGroup(val, nm))
    group = VGroup(base, bars, texts)
    if limit is not None:
        lim = DashedLine(base.get_left() + UP * limit * scale,
                         base.get_right() + UP * limit * scale, stroke_width=3, color=ALERT_C)
        lim_t = label(f"{limit_label} {limit:.{decimals}f}{unit}", FS_TAG, ALERT_C)
        lim_t.next_to(lim, RIGHT, 0.15)
        group.add(VGroup(lim, lim_t))
    fit(group).move_to(pos)
    scene.play(Create(base), FadeIn(VGroup(*[t[1] for t in texts])), run_time=0.6)
    _reveal(scene, list(zip(bars, texts)), cues,
            lambda it: AnimationGroup(GrowFromEdge(it[0], DOWN), FadeIn(it[1][0])),
            run_time=0.6)
    if limit is not None:
        scene.play(Create(group[3][0]), FadeIn(group[3][1]), run_time=0.6)
    return group


# ---------------- 13 checklist ----------------
def checklist(scene, items, cues=None, failed=(), pos=ORIGIN, size=FS_BODY - 2):
    """Empty boxes first, then each item ticked (or crossed if its index is in failed)."""
    rows = VGroup()
    for t in items:
        sq = Square(side_length=0.42, stroke_width=3, color=INK)
        rows.add(VGroup(sq, label(t, size)).arrange(RIGHT, buff=0.3))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    fit(rows).move_to(pos)
    scene.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=1.0)
    marks = VGroup()
    for k, r in enumerate(rows):
        bad = k in failed
        m = label("✗" if bad else "✓", size + 6, ALERT_C if bad else OK_C, weight=BOLD)
        marks.add(m.move_to(r[0]))

    def tick(k_mark):
        k, m = k_mark
        c = ALERT_C if k in failed else OK_C
        return AnimationGroup(FadeIn(m, scale=1.8), rows[k][1].animate.set_color(c))

    _reveal(scene, list(enumerate(marks)), cues, tick, run_time=0.5)
    return VGroup(rows, marks)


# ---------------- 14 summary_box ----------------
def summary_box(scene, heading, lines, cues=None, color=INK, pos=ORIGIN):
    """Framed key takeaways: heading, rule, then lines one by one."""
    head = label(heading, FS_HEADING, color, weight=BOLD)
    body = VGroup(*[label(f"•  {t}", FS_SUMMARY) for t in lines])
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    inner = VGroup(head, body).arrange(DOWN, buff=0.55)
    fit(inner, SAFE_WIDTH - 0.8)
    rule = Line(LEFT, RIGHT, stroke_width=3, color=color).set_width(inner.width)
    rule.move_to((head.get_bottom() + body.get_top()) / 2)
    frame = RoundedRectangle(width=inner.width + 0.9, height=inner.height + 0.8,
                             corner_radius=0.2, stroke_width=4, color=color)
    group = VGroup(frame, inner, rule).move_to(pos)
    frame.move_to(inner)
    scene.play(Create(frame), Write(head), run_time=1.0)
    scene.play(Create(rule), run_time=0.4)
    _reveal(scene, body, cues, lambda m: FadeIn(m, shift=RIGHT * 0.2))
    return group


# ---------------- 15 concept_map ----------------
def concept_map(scene, center, nodes, cues=None, links=None, radius=(4.2, 2.4),
                colors=None, pos=ORIGIN, run_time=0.6):
    """Central idea with surrounding ideas on an ellipse; optional link words."""
    colors = colors or [INK] * len(nodes)
    hub = _box(label(center, FS_BODY, weight=BOLD), INK, pad=0.3, fill=PANEL_FILL,
               width=4).move_to(pos)
    scene.play(GrowFromCenter(hub), run_time=0.8)
    items = []
    n = len(nodes)
    for k, (text, c) in enumerate(zip(nodes, colors)):
        a = PI / 2 - k * TAU / n
        p = np.array(pos) + np.array([radius[0] * np.cos(a), radius[1] * np.sin(a), 0])
        node = _box(label(text, FS_LABEL, c), c, pad=0.22).move_to(p)
        start, end = _exit_point(hub, p), _exit_point(node, hub.get_center())
        line = Line(start, end, stroke_width=3, color=c)
        extra = VGroup()
        if links and links[k]:
            extra.add(label(links[k], FS_TAG, GREY_INK).move_to(line).shift(
                rotate_vector(normalize(end - start), PI / 2) * 0.22))
        items.append(VGroup(line, node, extra))
    _reveal(scene, items, cues,
            lambda m: AnimationGroup(Create(m[0]), FadeIn(m[1], scale=0.8), FadeIn(m[2]),
                                     lag_ratio=0.3), run_time=run_time)
    return VGroup(hub, *items)


# ---------------- 16 timeline ----------------
def timeline(scene, events, cues=None, y=0.0, color=ACCENT_1, width=12.0, run_time=0.6):
    """Arrow with dated events [(when, text), ...], labels alternating above/below."""
    axis = Arrow(LEFT * width / 2, RIGHT * width / 2, buff=0, stroke_width=4,
                 max_tip_length_to_length_ratio=0.03).shift(UP * y)
    scene.play(GrowArrow(axis), run_time=1.0)
    n = len(events)
    items = []
    for k, (when, text) in enumerate(events):
        x = -width / 2 + width * (k + 0.5) / n
        dot = Dot([x, y, 0], radius=0.1, color=color)
        up = k % 2 == 0
        tick = Line([x, y, 0], [x, y + (0.55 if up else -0.55), 0], stroke_width=2,
                    color=GREY_INK)
        date = label(when, FS_LABEL, color, weight=BOLD)
        desc = label(text, FS_TAG)
        fit(desc, width / n * 1.8)
        tag = VGroup(date, desc).arrange(DOWN, buff=0.1)
        tag.next_to(tick, UP if up else DOWN, 0.1)
        items.append(VGroup(dot, tick, tag))
    _reveal(scene, items, cues,
            lambda m: AnimationGroup(FadeIn(m[0], scale=1.8), Create(m[1]),
                                     FadeIn(m[2], shift=(UP if m[1].get_end()[1] > y
                                                         else DOWN) * 0.1)),
            run_time=run_time)
    return VGroup(axis, *items)


# ---------------- 17 image_panel ----------------
def image_panel(scene, path, caption=None, credit=None, height=4.6, max_width=10.0,
                pos=ORIGIN, run_time=1.2):
    """Framed picture (PNG/JPG, or SVG drawn as strokes) with caption and credit line.

    Use only images the project may publish (own drawings, public-domain or licensed).
    """
    path = Path(path)
    if path.suffix.lower() == ".svg":
        img = SVGMobject(str(path)).set_height(height)
        show = Create(img)
    else:
        img = ImageMobject(str(path)).set_height(height)
        show = FadeIn(img)
    if img.width > max_width:
        img.scale_to_fit_width(max_width)
    frame = SurroundingRectangle(img, buff=0.12, stroke_width=4, color=INK)
    group = Group(frame, img)
    texts = VGroup()
    if caption:
        texts.add(label(caption, FS_LABEL))
    if credit:
        texts.add(label(credit, FS_TAG - 2, GREY_INK))
    if len(texts):
        texts.arrange(DOWN, buff=0.1).next_to(frame, DOWN, 0.2)
        group.add(texts)
    group.move_to(pos)
    scene.play(Create(frame), show, run_time=run_time)
    if len(texts):
        scene.play(FadeIn(texts, shift=UP * 0.1), run_time=0.5)
    return group


# ---------------- 18 document_panel ----------------
def document_panel(scene, lines, height=5.4, max_width=7.0, pos=ORIGIN, note=None,
                   size=FS_TAG - 4, run_time=2.0):
    """A sheet of monospaced lines (report, form, log), as the proving report of the
    prover series. lines: strings, or (text, BOLD) pairs. Returns
    VGroup(paper, rows[, note]); rows[k] is line k (for highlight()).
    """
    rows = VGroup(*[Text(t, font=MONO, font_size=size, weight=w)
                    for t, w in ((x, NORMAL) if isinstance(x, str) else x for x in lines)])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    paper = Rectangle(width=rows.width + 0.5, height=rows.height + 0.4, stroke_width=3,
                      color=INK).set_fill(BG, 1)
    doc = VGroup(paper, rows.move_to(paper))
    doc.scale_to_fit_height(height)
    if doc.width > max_width:
        doc.scale_to_fit_width(max_width)
    doc.move_to(pos)
    scene.play(Create(paper), run_time=0.6)
    scene.play(Write(rows), run_time=run_time)
    if note:
        n = label(note, FS_TAG - 4, GREY_INK).next_to(paper, DOWN, 0.08)
        scene.play(FadeIn(n), run_time=0.4)
        doc.add(n)
    return doc


def highlight(scene, doc, idx, color=ACCENT_3, run_time=0.5):
    """Frame line idx (or a list of lines) of a document_panel; the previous frame goes."""
    idx = [idx] if isinstance(idx, int) else list(idx)
    box = SurroundingRectangle(VGroup(*[doc[1][i] for i in idx]), buff=0.06, color=color,
                               stroke_width=4, corner_radius=0.05)
    old = getattr(doc, "_highlight", None)
    anims = [FadeOut(old)] if old is not None else []
    scene.play(*anims, Create(box), run_time=run_time)
    doc._highlight = box
    return box


# Catalogue order (used by projects/scene_gallery).
LIBRARY = ["title_card", "section_title", "bullet_list", "equation", "worked_calculation",
           "labeled_diagram", "process_flow", "stage_bar", "data_table", "comparison",
           "line_chart", "bar_chart", "checklist", "summary_box", "concept_map", "timeline",
           "image_panel", "document_panel"]
