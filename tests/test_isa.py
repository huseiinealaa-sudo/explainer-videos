"""ISA-5.1 symbols (explainer.symbols.isa): `python -m unittest discover tests`."""
import unittest

import numpy as np
from manim import RIGHT, UP, VGroup

import explainer.symbols.isa as isa
from explainer.symbols import (ISA_GROUPS, LOCATIONS, SIGNAL_KINDS, connect, control_valve,
                               instrument, signal_line, tank)
from explainer.style import ACCENT_1, MIN_FONT_SIZE


def all_symbols():
    for group in ISA_GROUPS.values():
        for fn, name in group:
            yield fn, getattr(isa, fn)


class Symbols(unittest.TestCase):
    def test_groups_cover_the_request(self):
        fns = {fn for fn, _ in all_symbols()}
        for fn in ["gate_valve", "globe_valve", "ball_valve", "butterfly_valve", "check_valve",
                   "control_valve", "relief_valve", "centrifugal_pump", "pd_pump", "compressor",
                   "tank", "heat_exchanger", "orifice_plate", "turbine_meter",
                   "magnetic_flowmeter", "coriolis_meter", "vortex_meter"]:
            self.assertIn(fn, fns)
        self.assertEqual(set(LOCATIONS), {"field", "panel", "behind_panel", "dcs", "plc"})
        self.assertEqual(set(SIGNAL_KINDS),
                         {"process", "connection", "pneumatic", "electrical", "capillary",
                          "data"})

    def test_uniform_size_colour_and_ports(self):
        for fn, make in all_symbols():
            with self.subTest(symbol=fn):
                s1, s2 = make(), make(size=2.0, color=ACCENT_1)
                self.assertTrue(0.4 <= max(s1.width, s1.height) <= 1.6, (fn, s1.width, s1.height))
                self.assertAlmostEqual(s2.width, 2 * s1.width, places=4)
                self.assertGreaterEqual(len(s1.port_names()), 2)
                for p in s1.port_names():             # ports sit on the drawing's box
                    pt = s1.port(p)
                    self.assertTrue(np.all(pt[:2] >= s1.get_corner([-1, -1, 0])[:2] - 1e-6))
                    self.assertTrue(np.all(pt[:2] <= s1.get_corner([1, 1, 0])[:2] + 1e-6))
                    np.testing.assert_allclose(s2.port(p), 2 * pt, atol=1e-6)
                inks = [m for m in s2.family_members_with_points()
                        if m.get_stroke_width() > 0 and m.get_stroke_opacity() > 0]
                self.assertTrue(inks)
                self.assertTrue(all(m.get_stroke_color().to_hex().lower() == ACCENT_1.lower()
                                    for m in inks), fn)

    def test_ports_move_with_the_symbol(self):
        v = control_valve()
        before = v.port("actuator")
        v.shift(RIGHT * 2 + UP).scale(1.5)
        after = v.port("actuator")
        self.assertFalse(np.allclose(before, after))
        self.assertTrue(np.allclose(v.copy().port("in"), v.port("in")))

    def test_bubbles(self):
        for loc in LOCATIONS:
            with self.subTest(location=loc):
                b = instrument("FIC", "101", loc)
                self.assertEqual(b.tag, "FIC-101")
                self.assertAlmostEqual(b.width, 1.0, places=3)
                texts = b.texts
                self.assertEqual([t.text for t in texts], ["FIC", "101"])
                # the text stays inside the outline, the function letters above the loop number
                self.assertGreater(texts[0].get_bottom()[1], texts[1].get_top()[1])
                for t in texts:
                    self.assertLess(np.linalg.norm(t.get_corner([1, 1, 0])[:2]), 0.5)
                    self.assertGreaterEqual(t.font_size, MIN_FONT_SIZE - 1e-6)
        with self.assertRaises(ValueError):
            instrument("FT", "101", "roof")

    def test_lines(self):
        for kind in SIGNAL_KINDS:
            with self.subTest(kind=kind):
                ln = signal_line([[-2, 0, 0], [2, 0, 0]], kind)
                self.assertEqual(ln.kind, kind)
                self.assertAlmostEqual(ln.width, 4.0, delta=0.3)
        n_marks = {k: len(signal_line([[-2, 0, 0], [2, 0, 0]], k)) - 1 for k in SIGNAL_KINDS}
        self.assertEqual(n_marks["process"], 0)
        self.assertEqual(n_marks["connection"], 0)
        self.assertGreater(n_marks["pneumatic"], 0)
        self.assertGreater(n_marks["capillary"], 0)
        self.assertGreater(n_marks["data"], 0)
        with self.assertRaises(ValueError):
            signal_line([[0, 0, 0], [1, 0, 0]], "laser")

    def test_connect_joins_ports(self):
        t = tank().shift(3 * RIGHT)
        b = instrument("LT", "101").shift(UP * 2)
        for route in ("straight", "hv", "vh", "hvh", "vhv"):
            ln = connect(t, "top", b, "bottom", kind="electrical", route=route)
            pts = ln[0].get_all_points() if len(ln[0].submobjects) == 0 else \
                np.vstack([d.get_all_points() for d in ln[0].submobjects])
            start, end = t.port("top"), b.port("bottom")
            self.assertLess(np.min(np.linalg.norm(pts - start, axis=1)), 1e-6)
            self.assertLess(np.min(np.linalg.norm(pts - end, axis=1)), 0.2)
        ln = connect(t, "top", b, "bottom", kind="process", via=[[3, 2, 0]])
        np.testing.assert_allclose(ln[0].get_start(), t.port("top"))
        np.testing.assert_allclose(ln[0].get_end(), b.port("bottom"))


if __name__ == "__main__":
    unittest.main()
