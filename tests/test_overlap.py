"""Tests of the overlap check (no rendering): `python -m unittest discover tests`.

The two touches that the check missed in the RT pilot (rt_intro_principle, round 1) are
rebuilt here from the script as it was before the fix (commit f13db36), with the same
shapes, sizes and coordinates, and must be found by text_near_shape; the fixed layouts of
the published version must not be.
"""
import unittest

import numpy as np
from manim import (BOLD, DOWN, LEFT, RIGHT, TAU, UP, Arrow, DoubleArrow, Line, Rectangle,
                   Square, VGroup, rotate_vector)

from explainer.qa.overlap import CLEARANCE, analyse, collect
from explainer.qa.selftest import cases
from explainer.style import ACCENT_1, FS_LABEL, FS_NOTE, INK, label

PLATE = "#e3e3e3"


def kinds(mobs, **kw):
    return sorted(f.kind for f in analyse(collect(mobs), **kw))


def near(mobs, **kw):
    return [f for f in analyse(collect(mobs), **kw) if f.kind == "text_near_shape"]


# ---------- rt_intro_principle, segment 3: the Ir-192 exposure head and its tags ----------
def rt_seg3(tag_x):
    """Exposure head with its 12 radial rays, and the four tags stacked from tag_pos
    (2.2 before the fix, 1.85 after it)."""
    head = Square(side_length=0.36, color=INK, stroke_width=3).set_fill(PLATE, 1)
    head.move_to([5.45, -1.13, 0])
    burst = VGroup(*[Line(head.get_center() + 0.3 * rotate_vector(RIGHT, a),
                          head.get_center() + 0.7 * rotate_vector(RIGHT, a),
                          stroke_width=3, color=ACCENT_1)
                     for a in np.linspace(0, TAU, 12, endpoint=False)])
    tags, prev = VGroup(), None
    for text in ("No power needed", "Portable: field work", "Cannot be switched off",
                 "Half-life ≈ 74 days"):
        t = label(text, FS_NOTE)
        if prev is None:
            t.move_to([tag_x, 0.05, 0])
        else:
            t.next_to(prev, DOWN, 0.2).align_to(prev, LEFT)
        tags.add(t)
        prev = t
    return [head, burst, tags]


# ---------- rt_intro_principle, segment 4: the dimension line d beside the plate ----------
def dim_line(x, y0, y1, text, side):
    """Same as dim_line() in rt_intro_principle.py."""
    arr = DoubleArrow([x, y0, 0], [x, y1, 0], buff=0, stroke_width=3, color=INK,
                      tip_length=0.16, max_tip_length_to_length_ratio=0.45)
    return VGroup(arr, label(text, FS_LABEL, INK, weight=BOLD).next_to(arr, side, 0.12))


def rt_seg4(dx, side):
    """Rig plate (px0 = -5.4, top -1.0, thickness 0.6, film gap 0.4) and the d dimension
    line: dx = -5.9 with the label on the RIGHT before the fix, -5.75 LEFT after it."""
    y_top, thick, gap = -1.0, 0.6, 0.4
    plate = Rectangle(width=0.9 + 5.4, height=thick, color=INK, stroke_width=3)
    plate.set_fill(PLATE, 1).move_to([(-5.4 + 0.9) / 2, y_top - thick / 2, 0])
    return [plate, dim_line(dx, y_top, y_top - thick - gap, "d", side)]


class KnownDefects(unittest.TestCase):
    def test_seg3_tag_touching_the_rays_is_found(self):
        found = near(rt_seg3(2.2))
        self.assertTrue(found, "the tag touching the rays was not found")
        self.assertEqual({f.a.text for f in found}, {"Cannot be switched off"})
        self.assertTrue(all(f.b.cls == "Line" for f in found))
        self.assertLess(min(f.extra["gap"] for f in found), 0.02)

    def test_seg4_d_label_touching_the_plate_is_found(self):
        found = near(rt_seg4(-5.9, RIGHT))
        self.assertEqual([(f.a.text, f.b.cls) for f in found], [("d", "Rectangle")])
        self.assertLess(found[0].extra["gap"], CLEARANCE)

    def test_both_known_defects_are_missed_by_the_area_rule_alone(self):
        # the reason for the clearance rule: no overlap area, so text_over_shape is silent
        for mobs in (rt_seg3(2.2), rt_seg4(-5.9, RIGHT)):
            self.assertNotIn("text_over_shape", kinds(mobs))

    def test_fixed_layouts_are_clean(self):
        self.assertEqual(kinds(rt_seg3(1.85)), [])
        self.assertEqual(kinds(rt_seg4(-5.75, LEFT)), [])

    def test_report_names_the_gap_and_a_move(self):
        from explainer.qa.overlap import OverlapChecker, suggest
        mobs = rt_seg4(-5.9, RIGHT)
        items = collect(mobs)
        f = [f for f in analyse(items) if f.kind == "text_near_shape"][0]
        amount = OverlapChecker()._amount(f)
        self.assertEqual(set(amount), {"gap", "clearance", "at", "cell"})
        self.assertIn("Move Text 'd'", suggest(f, items, [i for i in items if i.kind == "text"],
                                               0.25))


class ClearanceRule(unittest.TestCase):
    def test_line_and_arrow_without_area_are_checked(self):
        t = label("Label")
        line = Line(t.get_corner(DOWN + LEFT) + DOWN * 0.02 + LEFT,
                    t.get_corner(DOWN + RIGHT) + DOWN * 0.02 + RIGHT, stroke_width=2)
        self.assertEqual(kinds([t, line]), ["text_near_shape"])

    def test_stroke_width_counts(self):
        t = label("Label")
        y = t.get_bottom()[1] - CLEARANCE - 0.01               # centre line just clear
        thin = Line([-2, y, 0], [2, y, 0], stroke_width=1)      # ink edge CLEARANCE + 0.005
        thick = Line([-2, y, 0], [2, y, 0], stroke_width=8)     # ink edge CLEARANCE - 0.03
        self.assertEqual(kinds([t, thin]), [])
        self.assertEqual(kinds([t, thick]), ["text_near_shape"])

    def test_clear_placement_is_not_flagged(self):
        box = Rectangle(width=2, height=1, color=INK)
        for d in (UP, DOWN, LEFT, RIGHT):
            self.assertEqual(kinds([box, label("Beside").next_to(box, d, 0.15)]), [])

    def test_own_leader_arrow_is_not_flagged(self):
        t = label("Callout").move_to([2, 1, 0])
        target = [0, 0, 0]
        arrow = Arrow(t.get_left(), target, buff=0.08, stroke_width=3)
        self.assertEqual(kinds([t, arrow]), [])

    def test_arrow_tip_pointing_at_a_text_is_not_flagged(self):
        t = label("Result").move_to([2, 0, 0])
        self.assertEqual(kinds([t, Arrow([-1, 0, 0], t.get_left(), buff=0.06)]), [])

    def test_plain_line_ending_at_a_text_is_flagged(self):
        t = label("Result").move_to([2, 0, 0])
        ray = Line([-1, 0, 0], t.get_left() + LEFT * 0.02, stroke_width=3)
        self.assertEqual(kinds([t, ray]), ["text_near_shape"])


class SelfTest(unittest.TestCase):
    def test_selftest_cases(self):
        for name, mobs, expect in cases():
            with self.subTest(name):
                self.assertEqual(kinds(mobs), sorted(expect))


class CriticMemoryGuard(unittest.TestCase):
    """The PreToolUse hook of the video-critic agent (.claude/hooks/critic_memory_guard.py)."""

    def run_hook(self, path):
        import json
        import subprocess
        import sys
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        data = {"tool_name": "Edit", "tool_input": {"file_path": path}, "cwd": str(root)}
        r = subprocess.run([sys.executable, str(root / ".claude/hooks/critic_memory_guard.py")],
                           input=json.dumps(data), capture_output=True, text=True,
                           env={"CLAUDE_PROJECT_DIR": str(root)})
        return r.returncode

    def test_memory_file_allowed(self):
        self.assertEqual(self.run_hook(".claude/agent-memory/video-critic/MEMORY.md"), 0)

    def test_other_files_blocked(self):
        for p in ("CLAUDE.md", "explainer/qa/overlap.py", "/tmp/elsewhere.md",
                  ".claude/agent-memory/video-critic/../../agents/video-critic.md"):
            with self.subTest(p):
                self.assertEqual(self.run_hook(p), 2)


if __name__ == "__main__":
    unittest.main()
