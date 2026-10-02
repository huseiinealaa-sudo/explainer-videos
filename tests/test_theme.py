"""Tests of the themes, the backgrounds, the contrast rule and the motion tools.

`python -m unittest discover tests`. The contrast and theme tests need no rendering; the
motion tools run a scene without writing a video; one test renders a short preview to prove
that the animated background moves in a SyncedScene.
"""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import numpy as np
from manim import LEFT, RIGHT, UP, Dot, Rectangle, Square, VMobject, config, tempconfig

from explainer import theme
from explainer.backgrounds import make_background, theme_background
from explainer.motion import move_along_path, parallax, pulse, stagger_in, zoom_on
from explainer.qa.overlap import analyse, collect
from explainer.style import (ACCENT_1, BG, BG_ALT, GREY_INK, INK, LIGHT_INK, PANEL_FILL, label)
from explainer.timing import SyncedScene, find_phrase

ROOT = Path(__file__).resolve().parents[1]


class WithTheme(unittest.TestCase):
    """Runs a test under one theme and puts the previous one back."""

    def setUp(self):
        self._before = theme.current_theme()

    def tearDown(self):
        theme.set_theme(self._before)


class Themes(WithTheme):
    def test_three_themes_dark_is_the_default(self):
        self.assertEqual(sorted(theme.THEMES), ["blueprint", "dark", "light"])
        self.assertEqual(theme.DEFAULT_THEME, "dark")
        with tempfile.TemporaryDirectory() as d:        # a project that says nothing
            self.assertEqual(theme.project_theme(Path(d) / "x.py"), "dark")

    def test_every_theme_defines_every_token(self):
        for name, t in theme.THEMES.items():
            self.assertEqual(set(t["colors"]), set(theme.TOKENS), name)

    def test_dark_and_blueprint_pass_the_contrast_check_everywhere(self):
        for name in ("dark", "blueprint"):
            self.assertEqual(theme.check_theme(name), [], name)

    def test_light_is_the_original_board(self):
        c = theme.THEMES["light"]["colors"]
        self.assertEqual((c["bg"], c["ink"], c["muted"], c["faint"], c["panel"]),
                         ("#ffffff", "#000000", "#555555", "#9e9e9e", "#f3f3f3"))
        self.assertEqual((c["accent1"], c["accent2"], c["accent3"], c["accent4"]),
                         ("#1f5fa8", "#c25a12", "#2e7d32", "#c62828"))

    def test_colours_follow_the_theme_and_new_text_uses_them(self):
        theme.set_theme("blueprint")
        self.assertEqual(INK.to_hex().lower(), theme.THEMES["blueprint"]["colors"]["ink"])
        self.assertEqual(config.background_color.to_hex().lower(),
                         theme.THEMES["blueprint"]["colors"]["bg"])
        glyph = lambda m: m.family_members_with_points()[0].get_fill_color().to_hex()
        t = label("hello")
        self.assertEqual(glyph(t), "#F5F9FF")
        theme.set_theme("light")
        self.assertEqual(glyph(label("hello")), "#000000")
        self.assertEqual(glyph(t), "#F5F9FF")            # made before: keeps its colour
        self.assertEqual(ACCENT_1.to_hex().lower(), "#1f5fa8")

    def test_unknown_theme_is_refused(self):
        with self.assertRaises(ValueError):
            theme.set_theme("neon")

    def test_project_toml_chooses_the_theme(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "project.toml").write_text('[style]\ntheme = "blueprint"\n'
                                                  'background = ["grid", "particles"]\n')
            self.assertEqual(theme.project_theme(Path(d) / "x.py"), "blueprint")
            self.assertEqual(theme.project_motion(Path(d) / "x.py"), ("grid", "particles"))

    def test_projects_made_before_themes_stay_on_light(self):
        for name in ("prover", "rt_intro", "pt_cal", "svp_winsfc", "ut_intro", "scene_gallery",
                     "symbol_gallery"):
            self.assertEqual(theme.project_theme(ROOT / "projects" / name / "x.py"), "light", name)

    def test_contrast_ratio(self):
        self.assertAlmostEqual(theme.contrast_ratio("#000000", "#ffffff"), 21.0, places=1)
        self.assertAlmostEqual(theme.contrast_ratio("#777777", "#ffffff"), 4.48, places=1)


class Contrast(WithTheme):
    def found(self, mobs, **kw):
        return sorted(f.kind for f in analyse(collect(mobs), **kw))

    def test_text_close_to_its_background_is_critical(self):
        theme.set_theme("dark")
        fs = analyse(collect([label("Faint", color=BG_ALT)]))
        self.assertEqual([f.kind for f in fs], ["low_contrast"])
        self.assertEqual(fs[0].severity, "critical")
        self.assertLess(fs[0].extra["ratio"], 4.5)

    def test_every_text_token_passes_on_the_theme_background(self):
        for name in ("dark", "blueprint"):
            theme.set_theme(name)
            for color in (INK, GREY_INK, ACCENT_1):
                self.assertEqual(self.found([label("Readable", color=color)]), [], name)

    def test_filled_panels_under_a_text_count(self):
        theme.set_theme("dark")
        panel = Rectangle(width=4, height=1, stroke_width=0).set_fill(INK, 1)
        self.assertEqual(self.found([panel, label("Lost")]), ["low_contrast"])
        ok = Rectangle(width=4, height=1, stroke_width=0).set_fill(PANEL_FILL, 1)
        self.assertEqual(self.found([ok, label("Fine")]), [])

    def test_the_limit_is_4_5(self):
        theme.set_theme("light")
        # #777777 on white is 4.48:1 (just under), #707070 is 4.95:1
        self.assertEqual(self.found([label("x", color="#777777")]), ["low_contrast"])
        self.assertEqual(self.found([label("x", color="#707070")]), [])

    def test_inactive_text_is_exempt(self):
        theme.set_theme("light")                  # LIGHT_INK is 2.7:1 on white, by design
        self.assertEqual(self.found([label("inactive", color=LIGHT_INK)]), [])
        t = label("marked", color="#cccccc")
        t.contrast_exempt = True
        self.assertEqual(self.found([t]), [])

    def test_the_scene_background_is_what_is_behind_the_text(self):
        theme.set_theme("light")
        t = label("Dark on dark", color="#202020")
        black = lambda x, y: (0.05, 0.05, 0.05)
        self.assertEqual([f.kind for f in analyse(collect([t]), backdrop=black)],
                         ["low_contrast"])
        self.assertEqual(self.found([t]), [])     # on the theme's white it reads well

    def test_background_layers_are_not_checked_as_shapes(self):
        theme.set_theme("dark")
        bg = make_background(gradient=[BG, BG_ALT], motion=("grid", "particles"))
        self.assertEqual(collect([bg]), [])

    def test_gradient_surface_colour_is_read_from_the_plate(self):
        bg = make_background(gradient=["#000000", "#ffffff"], angle=0)
        left, right = bg.color_at(-7, 0), bg.color_at(7, 0)
        self.assertLess(left[0], 0.15)
        self.assertGreater(right[0], 0.85)

    def test_dimmed_image_surface(self):
        with tempfile.TemporaryDirectory() as d:
            from PIL import Image
            Image.new("RGB", (64, 36), (255, 255, 255)).save(Path(d) / "w.png")
            theme.set_theme("dark")
            bg = make_background(image=Path(d) / "w.png", dim=0.5)
            r, g, b = bg.color_at(0, 0)
            self.assertTrue(0.4 < r < 0.7)        # white half-way to the dark theme's BG


class Cue(unittest.TestCase):
    TEXT = "وَالدَّفْعُ يَبْدَأُ ثُمَّ الدَّفْعُ يَنْتَهِي"

    def test_whole_word_before_partial(self):
        i = find_phrase(self.TEXT, "الدَّفْعُ")
        self.assertEqual(i, self.TEXT.index("ثُمَّ") + len("ثُمَّ "))     # the lone one
        self.assertEqual(find_phrase(self.TEXT, "الدَّفْعُ", 1), i)

    def test_partial_when_no_whole_word(self):
        self.assertEqual(find_phrase("وَالدَّفْعُ فَقَطْ", "الدَّفْعُ"), 2)

    def test_latin_words(self):
        self.assertEqual(find_phrase("a cat concatenates cat", "cat"), 2)
        self.assertEqual(find_phrase("a cat concatenates cat", "cat", 2), 19)
        self.assertEqual(find_phrase("concatenates", "cat"), 3)
        self.assertEqual(find_phrase("nothing", "cat"), -1)

    def test_nth_counts_whole_words_first(self):
        self.assertEqual(find_phrase("xab ab ab", "ab", 2), 7)
        self.assertEqual(find_phrase("xab ab", "ab", 2), 4)       # one whole word only: nth of all

    def test_cue_uses_it(self):
        class S(SyncedScene):
            pass
        s = S.__new__(S)
        s.narration = [self.TEXT]
        s.words = [None]
        s.START = [0.0, 10.0]
        late = s.cue(1, "الدَّفْعُ")
        self.assertGreater(late, 5.0)             # the lone word, not the one inside «وَالدَّفْعُ»


def run_scene(scene_cls):
    """Play a scene at low quality without writing a video; returns the scene."""
    with tempfile.TemporaryDirectory() as d:
        with tempconfig({"quality": "low_quality", "write_to_movie": False,
                         "disable_caching": True, "media_dir": d, "verbosity": "ERROR",
                         "progress_bar": "none"}):
            scene = scene_cls()
            scene.render()
    return scene


class MotionTools(WithTheme):
    def test_zoom_returns_everything_to_where_it_was(self):
        out = {}

        class S(SyncedScene):
            def construct(self):
                a = Square(1.0, color=ACCENT_1).shift(LEFT * 3)
                b = label("text").shift(RIGHT * 2 + UP)
                self.add(a, b)
                before = [m.get_center().copy() for m in (a, b)]
                width = a.get_stroke_width()
                zoom_on(self, a, factor=2.0, hold=0.2, run_time=0.4)
                out["moved"] = [np.allclose(m.get_center(), c, atol=1e-6)
                                for m, c in zip((a, b), before)]
                out["size"] = (a.width, b.height, a.get_stroke_width(), width)
                out["zoomed"] = self.zoomed

        run_scene(S)
        self.assertEqual(out["moved"], [True, True])
        self.assertAlmostEqual(out["size"][0], 1.0, places=5)
        self.assertAlmostEqual(out["size"][2], out["size"][3], places=5)
        self.assertFalse(out["zoomed"])

    def test_zoom_magnifies_about_the_target(self):
        seen = {}

        class S(SyncedScene):
            def construct(self):
                a = Square(1.0).shift(LEFT * 3)
                far = Dot().shift(RIGHT * 3)
                self.add(a, far)

                def during(sc):
                    seen["a"] = (a.width, a.get_center().copy())
                    seen["zoomed"] = sc.zoomed
                zoom_on(self, a, factor=2.0, run_time=0.4, during=during)

        run_scene(S)
        self.assertAlmostEqual(seen["a"][0], 2.0, places=5)
        self.assertTrue(np.allclose(seen["a"][1], 0, atol=1e-6))    # the target is at the centre
        self.assertTrue(seen["zoomed"])

    def test_stagger_pulse_path_parallax(self):
        out = {}

        class S(SyncedScene):
            def construct(self):
                items = [Square(0.5).shift(RIGHT * k) for k in range(3)]
                stagger_in(self, items, lag=0.1, run_time=0.3)
                out["staggered"] = all(m in self.mobjects for m in items)
                n = len(self.mobjects)
                pulse(self, items[0], times=2, run_time=0.3)
                out["pulse_clean"] = len(self.mobjects) == n
                dot = Dot()
                path = VMobject().set_points_smoothly([np.array(p, float) for p in
                                                       [(-3, 0, 0), (0, 2, 0), (3, 0, 0)]])
                move_along_path(self, dot, path, run_time=0.5)
                out["dot_end"] = np.allclose(dot.get_center(), [3, 0, 0], atol=1e-3)
                far, near = Square(1).shift(UP), Square(1).shift(UP * 2)
                self.add(far, near)
                parallax(self, [(far, 0.25), (near, 1.0)], shift=LEFT * 2, run_time=0.3)
                out["parallax"] = (far.get_x(), near.get_x())

        run_scene(S)
        self.assertTrue(out["staggered"])
        self.assertTrue(out["pulse_clean"])
        self.assertTrue(out["dot_end"])
        self.assertAlmostEqual(out["parallax"][0], -0.5, places=5)
        self.assertAlmostEqual(out["parallax"][1], -2.0, places=5)


class SceneBackground(WithTheme):
    def test_clear_keeps_the_background_and_set_theme_switches(self):
        out = {}

        class S(SyncedScene):
            def construct(self):
                out["start"] = (self.bg is not None, theme.current_theme())
                label_ = label("x")
                self.add(label_)
                self.clear(run_time=0.2)
                out["after_clear"] = (self.bg in self.mobjects, label_ in self.mobjects)
                self.set_theme("blueprint", run_time=0.4)
                out["theme"] = theme.current_theme()
                out["bg_first"] = self.mobjects[0] is self.bg
                self.reset_theme(run_time=0.4)
                out["back"] = theme.current_theme()

        theme.set_theme("dark")
        run_scene(S)
        self.assertEqual(out["start"], (True, "dark"))          # dark has a gradient plate
        self.assertEqual(out["after_clear"], (True, False))
        self.assertEqual(out["theme"], "blueprint")
        self.assertTrue(out["bg_first"])
        self.assertEqual(out["back"], "dark")

    def test_a_plain_theme_adds_no_layer(self):
        self.assertIsNone(theme_background("light"))
        self.assertIsNotNone(theme_background("blueprint"))
        self.assertEqual(theme_background("dark").kind, "gradient")


class AnimatedBackground(unittest.TestCase):
    def test_the_background_moves_in_a_synced_scene(self):
        """Manim draws what comes before the first animated mobject once and a pause with
        nothing to update as one frozen frame. The moving layers have updaters and sit
        first, so a pause on an otherwise still screen must still change from frame to frame."""
        script = '''
from explainer import *

class Moves(SyncedScene):
    def construct(self):
        self.background(motion=("gradient", "grid", "particles"))
        self.add(label("still text", 40))
        self.wait(2)
'''
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "moves.py").write_text(script)
            (d / "project.toml").write_text('[style]\ntheme = "dark"\n')
            subprocess.run(["manim", "-ql", "--disable_caching", "--media_dir", str(d / "m"),
                            "--fps", "10", str(d / "moves.py"), "Moves"], check=True,
                           capture_output=True, cwd=d, env={**os.environ,
                                                             "EXPLAINER_SCRIPT": str(d / "moves.py")})
            video = next((d / "m").rglob("Moves.mp4"))
            frames = []
            for n in (2, 8, 14, 19):
                png = d / f"f{n}.png"
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vf",
                                f"select='eq(n,{n})'", "-frames:v", "1", str(png)], check=True)
                frames.append(np.asarray(__import__("PIL.Image", fromlist=["Image"])
                                         .open(png).convert("L"), dtype=float))
            diffs = [np.abs(frames[i] - frames[i + 1]).mean() for i in range(3)]
            self.assertTrue(all(x > 0.3 for x in diffs), diffs)     # a still screen gives ~0.003


if __name__ == "__main__":
    unittest.main()
