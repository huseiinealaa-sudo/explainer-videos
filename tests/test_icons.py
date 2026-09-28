"""Tabler icons (explainer.icons): `python -m unittest discover tests`."""
import re
import unittest

import numpy as np
from manim import ManimColor, VectorizedPoint

from explainer.icons import ICON_DIR, TABLER_VERSION, icon, icon_names
from explainer.style import ACCENT_1, ALERT_C, INK

COMMON = ["alert-triangle", "settings", "gauge", "flame", "droplet", "bolt", "clock", "check",
          "x", "file", "search", "tool", "temperature", "bell", "lock", "eye", "user",
          "chart-line", "calculator", "bulb", "database", "calendar", "wind", "plug"]


def strokes(mob):
    """The icon's drawn parts (without the invisible 24×24 frame)."""
    return [m for m in mob.submobjects[1:] if m.has_points()]


class TablerIcons(unittest.TestCase):
    def test_vendored_set(self):
        names = icon_names()
        self.assertGreaterEqual(len(names), 20)
        self.assertTrue(set(COMMON) <= set(names), set(COMMON) - set(names))
        self.assertTrue((ICON_DIR.parent / "LICENSE").exists())
        self.assertIn("MIT License", (ICON_DIR.parent / "LICENSE").read_text())
        self.assertRegex(TABLER_VERSION, r"^\d+\.\d+\.\d+$")

    def test_common_icons_load_at_size(self):
        self.assertGreaterEqual(len(COMMON), 20)
        for size in (0.6, 1.0, 1.7):
            for name in COMMON:
                with self.subTest(name=name, size=size):
                    m = icon(name, size=size)
                    parts = strokes(m)
                    self.assertTrue(parts, f"{name}: no strokes")
                    self.assertTrue(all(p.get_num_points() > 0 for p in parts))
                    # the 24×24 box sets the size: exactly size × size, centred
                    self.assertAlmostEqual(m.width, size, places=3)
                    self.assertAlmostEqual(m.height, size, places=3)
                    np.testing.assert_allclose(m.get_center(), 0, atol=1e-6)
                    # the drawing itself is visible and inside the box
                    ink = [p for p in parts if p.get_stroke_opacity() > 0]
                    self.assertTrue(ink)
                    lo = np.min([p.get_corner([-1, -1, 0]) for p in ink], axis=0)
                    hi = np.max([p.get_corner([1, 1, 0]) for p in ink], axis=0)
                    self.assertGreater((hi - lo)[:2].max(), 0.3 * size)
                    self.assertTrue(np.all(lo[:2] >= -size / 2 - 1e-6))
                    self.assertTrue(np.all(hi[:2] <= size / 2 + 1e-6))

    def test_colour_and_stroke(self):
        for color in (INK, ACCENT_1, ALERT_C):
            m = icon("gauge", color=color, stroke_width=5)
            for p in strokes(m):
                self.assertEqual(ManimColor(p.get_stroke_color()).to_hex().lower(),
                                 ManimColor(color).to_hex().lower())
                self.assertEqual(p.get_stroke_width(), 5)
            frame = m.submobjects[0]
            self.assertEqual(frame.get_stroke_opacity(), 0)   # the 24×24 frame stays invisible

    def test_current_color_replaced(self):
        # the vendored files use currentColor; nothing of it reaches Manim
        svg = (ICON_DIR / "gauge.svg").read_text()
        self.assertIn("currentColor", svg)
        from explainer.icons import _prepared_svg
        out = _prepared_svg("gauge", "#1f5fa8").read_text()
        self.assertNotIn("currentColor", out)
        self.assertEqual(len(re.findall(r'stroke="none"', out)), 1)

    def test_unknown_icon(self):
        with self.assertRaises(FileNotFoundError):
            icon("no-such-icon-name")


if __name__ == "__main__":
    unittest.main()
