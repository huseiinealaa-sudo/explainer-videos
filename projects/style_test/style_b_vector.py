"""Style B: Manim 2D, flat vector look - layered parallax (sky, sun, clouds, ridges, hills, city, airport, runway,
foreground) and a flat side-view airliner. No text, no audio.

Render (720p, 24 fps):
  python -m manim render -r 1280,720 --fps 24 projects/style_test/style_b_vector.py StyleBVector
The flight numbers come from airliner_geom.flight_table (same kinematics as A and C).
"""
import math
import os
import random
import sys

import numpy as np
from manim import *
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import airliner_geom as G  # noqa: E402

DUR = 10.0
M_PER_U = 7.1  # metres per scene unit (plane 40 m -> 5.6 units)
TMP = os.path.join(os.path.dirname(os.path.dirname(HERE)), "tmp", "style_test")
FW, FH = 14.222, 8.0
HORIZON = -1.45
GROUND_TOP = -2.0  # far edge of the runway band
WHEEL_Y = -2.42  # where the wheels touch on screen at the start
PIVOT = np.array([-0.35, -0.79, 0.0])  # main-gear contact, plane-local

PAL = dict(
    sun="#fff1c8", halo="#ff9a52", cloud="#f0769a", far="#6b3a8f", mid="#4a2a78", hills="#33205e", city="#281a52",
    airport="#1f1445", ground="#1b1038", runway="#2a1c4d", near="#140a2a", lit="#ffbf60",
    body="#f6f2f4", belly="#cfc3e2", stripe="#2f9fe0", fin="#ff7043", fin_dark="#e0512a", wing="#ece7f0", wing_dark="#b9adcc",
    engine="#d7d0e2", engine_dark="#a79bbd", glass="#2a1f4a", rim="#ffb36b",
)


def smooth(a, b, t):
    u = min(1.0, max(0.0, (t - a) / (b - a)))
    return u * u * (3 - 2 * u)


def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])


def make_sky(path, w=1280, h=720):
    y_h = h / 2 - HORIZON * h / FH  # horizon row
    stops = [(0.0, "#ffc069"), (0.06, "#ff8a4a"), (0.18, "#e04f7a"), (0.38, "#8a3a8f"), (0.68, "#3a2377"), (1.0, "#150f45")]
    ys = np.arange(h)[:, None]
    s = np.clip((y_h - ys) / y_h, 0, 1)
    img = np.zeros((h, w, 3))
    pos = [p for p, _ in stops]
    cols = np.array([hexrgb(c) for _, c in stops])
    for ch in range(3):
        img[:, :, ch] = np.interp(s[:, 0], pos, cols[:, ch])[:, None]
    img = np.where((ys > y_h)[:, :, None], hexrgb("#8a3a8f")[None, None, :], img)
    rng = np.random.default_rng(5)
    for _ in range(90):
        x, y = rng.integers(0, w), rng.integers(0, int(y_h * 0.5))
        img[y, x] = np.maximum(img[y, x], 0.6 * (1 - y / (y_h * 0.55)))
    arr = img * 255 + np.random.default_rng(2).normal(0, 0.7, img.shape)
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(path)
    return path


def make_vignette(path, w=1280, h=720):
    ys, xs = np.mgrid[0:h, 0:w]
    r2 = ((xs - w / 2) / (w / 2)) ** 2 * 0.7 + ((ys - h / 2) / (h / 2)) ** 2 * 0.9
    a = np.clip((r2 - 0.45) * 0.55, 0, 0.6)
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[:, :, :3] = (8, 4, 24)
    rgba[:, :, 3] = (a * 255).astype(np.uint8)
    Image.fromarray(rgba).save(path)
    return path


def poly(pts, color, opacity=1.0):
    return Polygon(*[[x, y, 0] for x, y in pts], fill_color=color, fill_opacity=opacity, stroke_width=0)


def ridge(W, base, amp, seed, bottom=-9.0, n=220):
    rng = random.Random(seed)
    ks = [2, 3, 5, 8, 13]
    ph = [rng.random() * math.tau for _ in ks]
    am = [1.0, 0.6, 0.42, 0.25, 0.14]
    norm = sum(am)
    pts = [(0, bottom)]
    for i in range(n + 1):
        x = W * i / n
        v = sum(a * (1 - abs(math.sin(math.tau * k * x / W + p))) ** 1.4 for k, a, p in zip(ks, am, ph)) / norm
        pts.append((x, base + amp * v))
    pts.append((W, bottom))
    return pts


class Layer:
    def __init__(self, mob, W, fx, ky):
        self.mob, self.W, self.fx, self.ky = mob, W, fx, ky
        self.left = 0.0
        self.y = 0.0
        self.mob.shift(LEFT * 7.2)
        self.left = -7.2

    def update(self, dist, cam_y):
        new_left = -7.2 - ((self.fx * dist) % self.W)
        new_y = -self.ky * cam_y
        self.mob.shift(RIGHT * (new_left - self.left) + UP * (new_y - self.y))
        self.left, self.y = new_left, new_y


def tiled(make_tile, W, copies=2):
    tile = make_tile()
    return VGroup(*[tile.copy().shift(RIGHT * W * k) for k in range(copies)])


class StyleBVector(Scene):
    def construct(self):
        os.makedirs(TMP, exist_ok=True)
        rng = random.Random(11)
        sky = ImageMobject(make_sky(os.path.join(TMP, "b_sky.png"))).set_height(FH)
        sky.move_to(ORIGIN)
        self.add(sky)

        layers = []

        # sun with flat halo rings (nearly static)
        sun_c = np.array([3.9, -0.55, 0])
        sun = VGroup(*[Circle(radius=r, fill_color=PAL["halo"], fill_opacity=o, stroke_width=0).move_to(sun_c)
                       for r, o in ((3.0, 0.07), (2.1, 0.10), (1.5, 0.16))],
                     Circle(radius=1.0, fill_color=PAL["sun"], fill_opacity=1, stroke_width=0).move_to(sun_c))
        self.add(sun)
        sun_off = [0.0]

        def cloud_tile(W=20):
            g = VGroup()
            x = 0.5
            while x < W - 4:
                w = rng.uniform(2.6, 5.0)
                h = rng.uniform(0.16, 0.3)
                y = rng.uniform(0.3, 2.6)
                g.add(Ellipse(width=w, height=h, fill_color=PAL["cloud"], fill_opacity=0.42, stroke_width=0).move_to([x + w / 2, y, 0]))
                g.add(Ellipse(width=w * 0.55, height=h * 0.7, fill_color=PAL["halo"], fill_opacity=0.28, stroke_width=0).move_to([x + w * 0.55, y - h * 0.55, 0]))
                x += w + rng.uniform(0.6, 2.4)
            return g

        def add_layer(mob, W, fx, ky):
            self.add(mob)
            layers.append(Layer(mob, W, fx, ky))

        add_layer(tiled(cloud_tile, 20), 20, 0.02, 0.05)
        add_layer(tiled(lambda: poly(ridge(20, HORIZON - 0.05, 1.55, 3), PAL["far"]), 20), 20, 0.04, 0.22)
        add_layer(tiled(lambda: poly(ridge(20, HORIZON - 0.35, 1.05, 8), PAL["mid"]), 20), 20, 0.09, 0.35)
        add_layer(tiled(lambda: poly(ridge(18, HORIZON - 0.7, 0.55, 21, n=260), PAL["hills"]), 18), 18, 0.17, 0.5)

        def city_tile(W=22):
            g = VGroup()
            x = 0.2
            base = GROUND_TOP
            while x < W - 1.0:
                bw, bh = rng.uniform(0.35, 0.85), rng.uniform(0.45, 1.9)
                g.add(Rectangle(width=bw, height=bh, fill_color=PAL["city"], fill_opacity=1, stroke_width=0).move_to([x + bw / 2, base + bh / 2, 0]))
                if bh > 1.3 and rng.random() < 0.6:
                    g.add(Line([x + bw / 2, base + bh, 0], [x + bw / 2, base + bh + 0.25, 0], stroke_color=PAL["city"], stroke_width=2))
                for _ in range(int(bh * bw * 7)):
                    wx, wy = x + rng.uniform(0.06, bw - 0.1), base + rng.uniform(0.1, bh - 0.1)
                    g.add(Square(0.045, fill_color=PAL["lit"], fill_opacity=rng.uniform(0.5, 0.95), stroke_width=0).move_to([wx, wy, 0]))
                x += bw + rng.uniform(0.02, 0.22)
            return g

        add_layer(tiled(city_tile, 22), 22, 0.28, 0.65)

        def airport_tile(W=24):
            g = VGroup()
            base = GROUND_TOP
            for hx in (2.0, 21.2):  # arched hangars
                g.add(Rectangle(width=3.0, height=0.7, fill_color=PAL["airport"], fill_opacity=1, stroke_width=0).move_to([hx + 1.5, base + 0.35, 0]))
                g.add(Ellipse(width=3.0, height=0.8, fill_color=PAL["airport"], fill_opacity=1, stroke_width=0).move_to([hx + 1.5, base + 0.7, 0]))
            g.add(Rectangle(width=9.2, height=0.62, fill_color=PAL["airport"], fill_opacity=1, stroke_width=0).move_to([10.8, base + 0.31, 0]))
            g.add(Rectangle(width=8.6, height=0.12, fill_color=PAL["lit"], fill_opacity=0.9, stroke_width=0).move_to([10.8, base + 0.3, 0]))
            g.add(Rectangle(width=0.34, height=1.9, fill_color=PAL["airport"], fill_opacity=1, stroke_width=0).move_to([16.6, base + 0.95, 0]))
            g.add(poly([(15.85, base + 1.9), (17.35, base + 1.9), (17.6, base + 2.25), (15.6, base + 2.25)], PAL["airport"]))
            g.add(Rectangle(width=1.5, height=0.2, fill_color=PAL["lit"], fill_opacity=0.95, stroke_width=0).move_to([16.6, base + 2.0, 0]))
            g.add(Circle(radius=0.07, fill_color="#ff4b4b", fill_opacity=1, stroke_width=0).move_to([16.6, base + 2.4, 0]))
            for mx in (6.3, 18.6, 23.0):
                g.add(Line([mx, base, 0], [mx, base + 0.85, 0], stroke_color=PAL["airport"], stroke_width=3))
                g.add(Circle(radius=0.06, fill_color=PAL["lit"], fill_opacity=1, stroke_width=0).move_to([mx, base + 0.87, 0]))
            return g

        add_layer(tiled(airport_tile, 24), 24, 0.45, 0.85)

        # ground, runway band (static in x, follows the camera down) with scrolling markings
        ground = VGroup(
            Rectangle(width=FW + 2, height=8, fill_color=PAL["ground"], fill_opacity=1, stroke_width=0).move_to([0, GROUND_TOP - 4, 0]),
            Rectangle(width=FW + 2, height=1.0, fill_color=PAL["runway"], fill_opacity=1, stroke_width=0).move_to([0, GROUND_TOP - 0.5, 0]),
            Rectangle(width=FW + 2, height=0.05, fill_color=PAL["halo"], fill_opacity=0.6, stroke_width=0).move_to([0, GROUND_TOP - 0.025, 0]),
            Ellipse(width=6.5, height=0.3, fill_color=PAL["halo"], fill_opacity=0.25, stroke_width=0).move_to([sun_c[0] - 0.3, GROUND_TOP - 0.2, 0]),
            Rectangle(width=FW + 2, height=3.4, fill_color=PAL["near"], fill_opacity=1, stroke_width=0).move_to([0, GROUND_TOP - 1.0 - 1.7, 0]),
        )
        self.add(ground)
        ground_y = [0.0]

        def dash_tile(W=15.6):
            return VGroup(*[Rectangle(width=1.3, height=0.07, fill_color="#e8dff0", fill_opacity=0.9, stroke_width=0).move_to([0.65 + 2.6 * k, GROUND_TOP - 0.5, 0]) for k in range(6)])

        def lights_tile(W=15.6):
            g = VGroup()
            for k in range(6):
                x = 1.0 + 2.6 * k
                g.add(Circle(radius=0.2, fill_color=PAL["halo"], fill_opacity=0.25, stroke_width=0).move_to([x, GROUND_TOP + 0.02, 0]))
                g.add(Circle(radius=0.05, fill_color="#ffe2a8", fill_opacity=1, stroke_width=0).move_to([x, GROUND_TOP + 0.02, 0]))
            return g

        add_layer(tiled(lights_tile, 15.6), 15.6, 0.95, 1.0)
        add_layer(tiled(dash_tile, 15.6), 15.6, 1.0, 1.0)

        # ---- plane (plane-local coordinates, nose to +x, fuselage centre at the origin)
        def prof(x):
            xm = x / 2.8 * 20
            r, zo = G._fuselage_profile(xm)
            k = 0.39 / G.R_BODY
            return r * k, zo * k * 0.7

        xs_ = np.linspace(-2.8, 2.85, 140)
        top = [(x, prof(x)[1] + prof(x)[0]) for x in xs_]
        bot = [(x, prof(x)[1] - prof(x)[0]) for x in xs_]
        t_at = lambda x: prof(x)[1] + prof(x)[0]
        zo_at = lambda x: prof(x)[1]
        r_at = lambda x: prof(x)[0]

        def band(x0, x1, f0, f1, color):
            xs2 = [x for x, _ in top if x0 <= x <= x1]
            upper = [(x, zo_at(x) + f0 * r_at(x)) for x in xs2]
            lower = [(x, zo_at(x) + f1 * r_at(x)) for x in xs2]
            return poly(upper + lower[::-1], color)

        fin = VGroup(poly([(-1.45, 0.30), (-2.6, 0.38), (-2.95, 1.55), (-2.25, 1.55)], PAL["fin"]),
                     poly([(-1.55, 0.3), (-2.62, 0.38), (-2.72, 0.75), (-1.78, 0.68)], PAL["fin_dark"]))
        stab = poly([(-2.05, 0.22), (-2.75, 0.30), (-3.12, 0.56), (-2.62, 0.56)], PAL["wing_dark"])
        fus = poly(top + bot[::-1], PAL["body"])
        belly = band(-2.7, 2.6, -0.45, -1.0, PAL["belly"])
        stripe = band(-2.0, 2.15, -0.2, -0.42, PAL["stripe"])
        cockpit = poly([(2.0, t_at(2.0) - 0.03), (2.45, t_at(2.45) - 0.03), (2.36, t_at(2.36) - 0.17), (2.0, t_at(2.0) - 0.17)], PAL["glass"])
        windows = VGroup(*[RoundedRectangle(width=0.08, height=0.11, corner_radius=0.03, fill_color=PAL["glass"], fill_opacity=1, stroke_width=0)
                           .move_to([-1.95 + 0.175 * k, zo_at(-1.95 + 0.175 * k) + 0.09, 0]) for k in range(22)])
        rim = VMobject(stroke_color=PAL["rim"], stroke_width=2.4, stroke_opacity=0.85)
        rim.set_points_as_corners([[x, y + 0.005, 0] for x, y in top if -2.5 < x < 2.35])
        wing = VGroup(poly([(0.75, -0.10), (-0.45, -0.12), (-1.75, -0.52), (-1.30, -0.52)], PAL["wing"]),
                      poly([(-0.42, -0.125), (-1.75, -0.52), (-1.52, -0.52), (-0.35, -0.2)], PAL["wing_dark"]))
        engine = VGroup(
            poly([(0.15, -0.28), (0.75, -0.28), (0.75, -0.36), (0.15, -0.36)], PAL["wing_dark"]),
            Ellipse(width=0.95, height=0.42, fill_color=PAL["engine"], fill_opacity=1, stroke_width=0).move_to([0.45, -0.52, 0]),
            Ellipse(width=0.72, height=0.2, fill_color=PAL["engine_dark"], fill_opacity=1, stroke_width=0).move_to([0.43, -0.61, 0]),
            Ellipse(width=0.15, height=0.36, fill_color="#f1eef5", fill_opacity=1, stroke_width=0).move_to([0.9, -0.52, 0]),
            Ellipse(width=0.09, height=0.27, fill_color=PAL["glass"], fill_opacity=1, stroke_width=0).move_to([0.92, -0.52, 0]),
        )
        gear = VGroup(
            Line([-0.35, -0.22, 0], [-0.35, -0.65, 0], stroke_color="#6d6783", stroke_width=4),
            Circle(radius=0.14, fill_color="#221a38", fill_opacity=1, stroke_width=0).move_to([-0.35, -0.65, 0]),
            Circle(radius=0.06, fill_color="#7d7596", fill_opacity=1, stroke_width=0).move_to([-0.35, -0.65, 0]),
            Line([1.95, -0.32, 0], [1.95, -0.65, 0], stroke_color="#6d6783", stroke_width=3),
            Circle(radius=0.14, fill_color="#221a38", fill_opacity=1, stroke_width=0).move_to([1.95, -0.65, 0]),
            Circle(radius=0.06, fill_color="#7d7596", fill_opacity=1, stroke_width=0).move_to([1.95, -0.65, 0]),
        )
        beam = VGroup(poly([(2.85, -0.03), (9.5, -0.95), (9.5, -0.25)], "#ffe2a8", 0.10),
                      poly([(2.85, -0.03), (6.2, -0.5), (6.2, -0.12)], "#ffe2a8", 0.12))
        nav = Circle(radius=0.055, fill_color="#ff3b3b", fill_opacity=1, stroke_width=0).move_to([-2.9, 1.52, 0])
        plane = VGroup(beam, stab, fin, nav, gear, wing, fus, belly, stripe, windows, cockpit, rim, engine)
        plane.save_state()
        shadow = Ellipse(width=5.4, height=0.2, fill_color="#07030f", fill_opacity=0.45, stroke_width=0)
        self.add(shadow, plane)

        # foreground: lamp posts and grass blades, faster than the ground
        def posts_tile(W=15.4):
            g = VGroup()
            for k in range(4):
                x = 1.5 + 3.85 * k
                g.add(Rectangle(width=0.07, height=1.6, fill_color="#0d0620", fill_opacity=1, stroke_width=0).move_to([x, GROUND_TOP - 1.0 - 1.4 - 0.2, 0]))
                g.add(Circle(radius=0.3, fill_color=PAL["halo"], fill_opacity=0.25, stroke_width=0).move_to([x, GROUND_TOP - 1.0 - 0.6 - 0.2, 0]))
                g.add(Circle(radius=0.08, fill_color="#ffe2a8", fill_opacity=1, stroke_width=0).move_to([x, GROUND_TOP - 1.0 - 0.6 - 0.2, 0]))
            return g

        def grass_tile(W=16.0):
            pts = [(0, -9.0), (0, GROUND_TOP - 2.3)]
            x = 0.0
            while x < W:
                pts += [(x + 0.08, GROUND_TOP - 2.3 + rng.uniform(0.25, 0.6)), (x + 0.17, GROUND_TOP - 2.3)]
                x += 0.17
            pts += [(W, GROUND_TOP - 2.3), (W, -9.0)]
            return poly(pts, "#080416")

        add_layer(tiled(posts_tile, 15.4), 15.4, 1.6, 1.0)
        add_layer(tiled(grass_tile, 16.0), 16.0, 2.2, 1.0)
        self.add(ImageMobject(make_vignette(os.path.join(TMP, "b_vignette.png"))).set_height(FH))

        tab = G.flight_table(DUR, 0.002)

        def frame(t):
            px, pz, pitch, g = tab[min(int(round(t / 0.002)), len(tab) - 1)]
            dist = px / M_PER_U
            alt = pz / M_PER_U
            cam_y = 0.6 * alt
            for ly in layers:
                ly.update(dist, cam_y)
            ground.shift(UP * (-cam_y - ground_y[0]))
            ground_y[0] = -cam_y
            sun.shift(UP * (-0.06 * cam_y - sun_off[0]))
            sun_off[0] = -0.06 * cam_y
            # plane: restore base pose, retract gear, pitch about the main-gear contact, place on screen
            plane.restore()
            gear.scale(g, about_point=np.array([-0.35, -0.3, 0]))
            plane.rotate(pitch, about_point=PIVOT)
            xs = -3.6 + 2.0 * smooth(0, 7.5, t)
            target = np.array([xs, WHEEL_Y + alt - cam_y, 0])
            plane.shift(target - PIVOT)
            if g < 0.5:
                beam.set_fill(opacity=0.0)
            nav.set_fill(opacity=0.45 + 0.55 * (math.sin(t * 9) > 0.3))
            shadow.move_to([xs - 0.45, WHEEL_Y - 0.03 - cam_y, 0])
            shadow.set_fill(opacity=max(0.0, 0.45 - 0.12 * alt))

        frame(0.0)
        tracker = ValueTracker(0.0)
        ticker = Mobject()
        ticker.add_updater(lambda m: frame(tracker.get_value()))
        self.add(ticker)
        self.play(tracker.animate.set_value(DUR), run_time=DUR, rate_func=linear)
