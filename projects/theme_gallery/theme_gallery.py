"""Theme gallery: a silent catalogue of the themes, the backgrounds and the motion tools.

    1. a sample of library scenes (equation, worked calculation, table, flow, symbol drawing,
       bar chart) in each of the three themes: dark, blueprint, light
    2. the backgrounds: a colour, a gradient and an image, then the three slow motions
       (gradient, grid, particles)
    3. the five motion tools: zoom_on, stagger_in, move_along_path, pulse, parallax
No narration: NARRATION holds the length of each silent segment (seconds, from
theme_gallery_data.py). Rendered at 720p (project.toml, [render]).

Build (from the repo root):
    python projects/theme_gallery/theme_gallery.py --preview --qa   # -> tmp/theme_gallery/
    python projects/theme_gallery/theme_gallery.py                  # -> output/theme_gallery.mp4
"""
from pathlib import Path

from explainer import *
from explainer.symbols import isa
import theme_gallery_data as D

NARRATION = list(D.DURATIONS.values())          # silent segments (seconds)
SEG = {name: k + 1 for k, name in enumerate(D.DURATIONS)}
AUDIO_DIR = audio_dir_for(__file__)
HERE = Path(__file__).resolve().parent
CALL_SIZE = FS_LABEL                            # the call shown at the bottom of a demo


class ThemeGallery(SyncedScene):
    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)

        # ---------------- title ----------------
        s = SEG["title"]
        title_card(self, "Theme Gallery", "themes  ·  backgrounds  ·  motion tools",
                   series="explainer-videos  ·  catalogue")
        self.sync(self.end(s) - 0.7)
        self.clear()

        # ---------------- the three themes ----------------
        for name in D.THEMES:
            self.set_theme(name)
            self.structure_a(SEG[f"{name}_a"], name)
            self.structure_b(SEG[f"{name}_b"], name)

        # ---------------- backgrounds ----------------
        self.set_theme("dark")
        self.backgrounds_base(SEG["bg_base"])
        self.motion_background(SEG["bg_gradient"], "gradient", "dark")
        self.motion_background(SEG["bg_grid"], "grid", "blueprint")
        self.motion_background(SEG["bg_particles"], "particles", "dark")

        # ---------------- motion tools ----------------
        self.set_theme("dark")
        self.demo_zoom(SEG["zoom"])
        self.demo_stagger(SEG["stagger"])
        self.demo_path(SEG["path"])
        self.demo_pulse(SEG["pulse"])
        self.demo_parallax(SEG["parallax"])

        # ---------------- end ----------------
        s = SEG["end"]
        box = summary_box(self, "Theme gallery", [
            "3 themes: dark (default) · blueprint · light",
            "Backgrounds: colour · gradient · image, with slow motion",
            "5 motion tools: zoom · stagger · path · pulse · parallax"])
        self.sync(self.end(s) - 0.4)

    # ---------- helpers ----------
    def heading(self, text):
        return section_title(self, text)

    def call(self, text, color=GREY_INK):
        """The call that makes the demo, as the bottom caption."""
        self.say(text, color, size=CALL_SIZE)

    # ---------- the themes ----------
    def structure_a(self, s, name):
        """Equation, worked calculation, table."""
        self.heading(f"theme: {name}  ·  equation, calculation, table")
        eq = equation(self, D.EQUATION, colors={0: ACCENT_1, 2: ACCENT_3, 4: ACCENT_4},
                      pos=UP * 2.1, run_time=1.2)
        emphasize(self, eq[0], buff=0.07)
        worked_calculation(self, D.CALC_FORMULA, D.CALC_VALUES, D.CALC_RESULT, pos=DOWN * 0.5)
        self.sync(self.at(s, 0.5))
        self.clear()
        self.heading(f"theme: {name}  ·  equation, calculation, table")
        table = data_table(self, D.TABLE_HEADER, D.TABLE_ROWS, pos=UP * 0.3)
        highlight_row(self, table, D.TABLE_HIGHLIGHT)
        self.call("data_table(...)  ·  highlight_row(...)")
        self.sync(self.end(s) - 0.7)
        self.clear()

    def structure_b(self, s, name):
        """Process flow, a loop drawing with symbols and callouts, bar chart."""
        self.heading(f"theme: {name}  ·  flow, symbols, chart")
        flow = process_flow(self, D.FLOW_STEPS, pos=UP * 0.2)
        highlight_step(self, flow, D.FLOW_ACTIVE)
        self.sync(self.at(s, 0.22))
        self.clear()
        self.heading(f"theme: {name}  ·  flow, symbols, chart")
        k, y = 1.25, -0.9
        pump = centrifugal_pump(size=k)
        pump.shift(np.array([-4.4, y, 0]) - pump.port("in"))
        y2 = pump.port("out")[1]
        fe = orifice_plate(size=k)
        fe.shift(np.array([-1.5, y2, 0]) - fe.port("in"))
        fv = control_valve(size=k)
        fv.shift(np.array([1.7, y2, 0]) - fv.port("in"))
        ft = instrument(*D.LOOP_TAG, "field", size=1.0)
        ft.move_to([fe.port("tap")[0], y2 + 1.9, 0])
        lines = VGroup(
            signal_line([pump.port("in") + LEFT * 0.9, pump.port("in")], "process"),
            connect(pump, "out", fe, "in", kind="process"),
            connect(fe, "out", fv, "in", kind="process"),
            signal_line([fv.port("out"), fv.port("out") + RIGHT * 1.4], "process", arrow=True),
            connect(fe, "tap", ft, "bottom", kind="connection"))
        diagram = VGroup(pump, fe, fv, ft, lines)
        labeled_diagram(self, diagram, [("Pump", pump, DOWN), ("Orifice", fe, DOWN),
                                        ("Valve", fv, DOWN), ("FT", ft, RIGHT)],
                        draw_time=2.5)
        self.sync(self.at(s, 0.62))
        self.clear()
        bar_chart(self, D.BARS["labels"], D.BARS["values"], unit=D.BARS["unit"],
                  limit=D.BARS["limit"], pos=UP * 0.3)
        self.call("bar_chart(...)  ·  limit line, bars above it in ALERT_C")
        self.sync(self.end(s) - 0.7)
        self.clear()

    # ---------- the backgrounds ----------
    def backgrounds_base(self, s):
        """A colour, a gradient and a picture, each behind the same sample text."""
        sample = VGroup(label("Text stays readable", FS_HEADING, weight=BOLD),
                        label("on any surface: the QA contrast rule measures it (4.5:1)",
                              FS_LABEL, GREY_INK)).arrange(DOWN, buff=0.3)
        self.heading("backgrounds: colour · gradient · image")
        steps = [
            ("background(color=...)", dict(color=D.BG_SOLID)),
            ("background(gradient=[...], angle=-35)", dict(gradient=list(D.BG_GRADIENT),
                                                          angle=-35)),
            ("background(image=..., dim=0.55)", dict(image=HERE / D.BG_IMAGE,
                                                    dim=D.BG_IMAGE_DIM)),
        ]
        for k, (call, spec) in enumerate(steps):
            self.background(run_time=1.0, **spec)
            if k == 0:
                self.play(FadeIn(sample), run_time=0.6)
            self.call(call)
            self.sync(self.at(s, (k + 1) / 3) - 0.3)
        self.clear()
        self.background(run_time=0.8)              # the theme's own again

    def motion_background(self, s, motion, theme):
        """One slow background motion behind a short text."""
        if theme != current_theme():
            self.set_theme(theme)
        self.background(run_time=1.0, motion=motion)
        self.heading(f"background motion: {motion}")
        bullet_list(self, ["Slow: a full cycle takes 30 to 80 seconds",
                           "Never above the opacity the theme allows",
                           "Text keeps 4.5:1 contrast on top"], pos=UP * 0.2)
        self.call(f"background(motion=\"{motion}\")")
        self.sync(self.end(s) - 0.6)
        self.clear()
        self.background(run_time=0.0)              # the theme's own, without motion

    # ---------- the motion tools ----------
    def demo_zoom(self, s):
        self.heading("zoom_on: magnify an element, then return")
        k, y = 1.6, -0.6
        fv = control_valve(size=k)
        fv.shift(np.array([0, y, 0]) - fv.port("in") - RIGHT * 0.45 * k)
        pipe = VGroup(signal_line([fv.port("in") + LEFT * 3.6, fv.port("in")], "process"),
                      signal_line([fv.port("out"), fv.port("out") + RIGHT * 3.6], "process",
                                  arrow=True))
        fy = instrument("FY", "101", "field", size=1.0)
        fy.move_to([fv.port("actuator")[0] + 2.4, fv.port("actuator")[1] + 1.2, 0])
        air = connect(fy, "left", fv, "actuator", kind="pneumatic", route="hv", spacing=0.55,
                      end_gap=0.25)
        note = label("positioner", FS_TAG, GREY_INK).next_to(fy, DOWN, 0.2)
        self.play(Create(VGroup(pipe, fv)), run_time=1.2)
        self.play(Create(fy), Create(air), FadeIn(note), run_time=1.2)
        self.sync(self.at(s, 0.3))
        self.call("zoom_on(self, target, factor=2.4, hold=2)")
        zoom_on(self, fv.port("actuator") + RIGHT * 0.8, factor=D.ZOOM_FACTOR, hold=2.0)
        self.sync(self.end(s) - 0.6)
        self.clear()

    def demo_stagger(self, s):
        self.heading("stagger_in: items enter one after another")
        cards = VGroup()
        for text, icon_name in D.STAGGER_STEPS:
            body = VGroup(icon(icon_name, INK, 0.9), label(text, FS_LABEL)).arrange(DOWN, buff=0.3)
            cards.add(VGroup(SurroundingRectangle(body, color=LINE_C, buff=0.35,
                                                  corner_radius=0.15, stroke_width=3), body))
        cards.arrange(RIGHT, buff=0.6).move_to(UP * 0.2)
        self.call("stagger_in(self, items, shift=UP * 0.5, lag=0.3)")
        self.sync(self.at(s, 0.15))
        stagger_in(self, cards, shift=UP * 0.5, lag=0.3, run_time=0.7)
        self.sync(self.end(s) - 0.6)
        self.clear()

    def demo_path(self, s):
        self.heading("move_along_path: an element travels a path")
        pts = [np.array([x, y, 0.0]) for x, y in D.PATH_POINTS]
        path = VMobject(stroke_width=3, color=GREY_INK).set_points_smoothly(pts)
        a = label("A", FS_LABEL, ACCENT_1, weight=BOLD).next_to(pts[0], LEFT, 0.25)
        b = label("B", FS_LABEL, ACCENT_3, weight=BOLD).next_to(pts[-1], RIGHT, 0.25)
        self.play(Create(path), FadeIn(a), FadeIn(b), run_time=1.2)
        dot = Dot(radius=0.16, color=ACCENT_2)
        self.call("move_along_path(self, dot, path, trail=True)")
        trace = move_along_path(self, dot, path, run_time=3.0, trail=True, color=ACCENT_2)
        self.sync(self.at(s, 0.55))
        self.play(FadeOut(dot), FadeOut(trace), run_time=0.4)
        arrow = Triangle(fill_opacity=1, color=ACCENT_1).scale(0.22).rotate(-PI / 2)
        self.call("move_along_path(self, mark, path, rotate=True)")
        move_along_path(self, arrow, path, run_time=3.0, rotate=True)
        self.sync(self.end(s) - 0.6)
        self.clear()

    def demo_pulse(self, s):
        self.heading("pulse: a highlight on the element being explained")
        cards = VGroup()
        for text, icon_name in (("Pressure", "gauge"), ("Temperature", "temperature"),
                                ("Flow", "droplet")):
            body = VGroup(icon(icon_name, INK, 1.0), label(text, FS_LABEL)).arrange(DOWN, buff=0.3)
            cards.add(VGroup(SurroundingRectangle(body, color=LINE_C, buff=0.4,
                                                  corner_radius=0.15, stroke_width=3), body))
        cards.arrange(RIGHT, buff=1.0).move_to(UP * 0.2)
        self.play(FadeIn(cards), run_time=0.8)
        self.call("pulse(self, element, color, times=2)")
        self.sync(self.at(s, 0.2))
        pulse(self, cards[0], ACCENT_1, times=2)
        pulse(self, cards[1], ACCENT_2, times=2)
        pulse(self, cards[2], ACCENT_3, times=2)
        self.sync(self.end(s) - 0.6)
        self.clear()

    def demo_parallax(self, s):
        self.heading("parallax: depth layers travel at different speeds")
        far = VGroup(*[Rectangle(width=0.7, height=h, stroke_width=2, color=GRID_C)
                       for h in (0.8, 1.4, 1.0, 1.8, 1.2, 0.9, 1.6, 1.1)])
        far.arrange(RIGHT, buff=0.55, aligned_edge=DOWN).move_to([0, 1.35, 0])
        mid = VGroup(*[tank(size=1.0, color=GREY_INK) for _ in range(4)])
        mid.arrange(RIGHT, buff=1.8).move_to([0, 0.05, 0])
        near_line = Line(LEFT * 5.0, RIGHT * 5.0, stroke_width=isa.PROCESS_STROKE, color=LINE_C)
        near = VGroup(near_line, *[gate_valve(size=0.8) .move_to([x, 0, 0])
                                   for x in (-3.2, 0.0, 3.2)])
        near.move_to([0, -1.55, 0])
        layers = [(far, D.PARALLAX_DEPTHS[0]), (mid, D.PARALLAX_DEPTHS[1]),
                  (near, D.PARALLAX_DEPTHS[2])]
        names = VGroup(*[label(f"depth {d}", FS_TAG, GREY_INK) for d in D.PARALLAX_DEPTHS])
        names.arrange(RIGHT, buff=1.4).move_to([0, -2.5, 0])
        self.play(Create(VGroup(far, mid, near)), FadeIn(names), run_time=1.6)
        self.call("parallax(self, [(layer, depth), ...], shift=LEFT * 1.5)", GREY_INK)
        self.sync(self.at(s, 0.25))
        parallax(self, layers, LEFT * D.PARALLAX_SHIFT, run_time=2.5)
        parallax(self, layers, RIGHT * D.PARALLAX_SHIFT, run_time=2.5)
        self.sync(self.end(s) - 0.6)
        self.clear()


if __name__ == "__main__":
    main(__file__, "ThemeGallery", NARRATION)
