"""Self-test of the overlap check on small layouts (no rendering): `python -m explainer.qa.selftest`.

Each case lists the findings it must give; the intended overlaps (a text inside its frame,
a badge number, a ✓ on its box, a label on a panel, a text crossed out, a label's leader
arrow, a tick joining two labels) must give none. The two touches missed in the RT pilot
are rebuilt exactly in tests/test_overlap.py.
"""
from manim import (BOLD, DL, DOWN, DR, LEFT, ORIGIN, PI, RIGHT, UL, UP, UR, Arrow, Circle,
                   DashedLine, Dot, Line, Rectangle, Square, SurroundingRectangle, VGroup)

from ..scenes import badge
from ..style import BG, FS_AXIS, FS_BODY, FS_TAG, PANEL_FILL, label
from .overlap import analyse, collect


def cases():
    t = label("Framed label")
    yield "text inside its frame", [t, SurroundingRectangle(t, buff=0.15)], []
    yield "arrow through a text", [label("Crossed"), Arrow(DOWN * 1.5, UP * 1.5, buff=0)], \
        ["text_over_shape"]
    w = label("Guide block")
    gap = (w[4].get_right() + w[5].get_left()) / 2
    yield "line through the gap between two words", [w, Line(gap + DOWN, gap + UP)], \
        ["text_over_shape"]
    yield "two texts overlap", [label("First text"),
                                label("Second text").shift(RIGHT * 0.8 + UP * 0.1)], ["text_overlap"]
    yield "text off the frame", [label("Off the edge").move_to(RIGHT * 7.0)], ["out_of_frame"]
    yield "text in the safe margin", [label("Near the edge").to_edge(RIGHT, buff=0.1)], \
        ["in_safe_margin"]
    yield "text too small", [label("tiny", FS_TAG - 10)], ["text_too_small"]
    sq = Square(0.42)
    yield "tick mark on its box", [sq, label("✓", FS_BODY + 6).move_to(sq)], []
    yield "library badge", [badge(4)], []
    c = Circle(radius=0.2, stroke_width=3, fill_color=BG, fill_opacity=1)
    yield "small round badge '10'", [VGroup(c, label("10", FS_TAG, weight=BOLD).move_to(c))], []
    o = label("Overflowing")
    yield "text wider than its box", [o, Rectangle(width=o.width - 0.2, height=1.0)], \
        ["text_over_shape"]
    k = label("Touching")
    yield "text touches its frame", [k, Rectangle(width=k.width + 0.02, height=1.0)], \
        ["text_touches_frame"]
    yield "rotated axis label", [label("rotated axis label", FS_AXIS).rotate(PI / 2)], []
    yield "label on a filled panel", [Rectangle(width=4, height=1, stroke_width=0)
                                      .set_fill(PANEL_FILL, 1), label("On a panel")], []
    yield "invisible anchor", [Dot(radius=0.001).set_opacity(0), label("x")], []
    x = label("reading corrected twice")
    yield "text crossed out on purpose", [x, Line(x.get_corner(UL), x.get_corner(DR)),
                                          Line(x.get_corner(DL), x.get_corner(UR))], []
    yield "dashed line through a text", [DashedLine(LEFT * 2, RIGHT * 2), label("dashed")], \
        ["text_over_shape"]
    # clearance (text_near_shape): contacts with no overlap area, lines included
    r = label("Near a ray")
    yield "ray ending at a text", [r, Line(r.get_right() + RIGHT * 0.8, r.get_right() + RIGHT * 0.02,
                                           stroke_width=3)], ["text_near_shape"]
    plate = Rectangle(width=3, height=0.6)
    yield "label touching a plate edge", [plate, label("d", weight=BOLD).next_to(plate, LEFT, 0.03)], \
        ["text_near_shape"]
    yield "label beside a plate", [plate, label("d", weight=BOLD).next_to(plate, LEFT, 0.15)], []
    c1 = label("Callout").move_to(UP + RIGHT * 2)
    yield "callout with its leader arrow", [c1, Arrow(c1.get_left(), ORIGIN, buff=0.08)], []
    n1, n2 = label("note").move_to(UP), label("term").move_to(DOWN * 0.2)
    yield "tick joining two labels", [n1, n2, Line(n1.get_bottom() + DOWN * 0.05,
                                                   n2.get_top() + UP * 0.02)], []


def main():
    failed = 0
    for name, mobs, expect in cases():
        got = sorted(f.kind for f in analyse(collect(mobs)))
        ok = got == sorted(expect)
        failed += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name}: {got or 'no finding'}")
    print("all passed" if not failed else f"{failed} failed")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
