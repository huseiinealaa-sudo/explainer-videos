"""Style A: Manim ThreeDScene - dark gradient sky, baked warm/cool lighting, detailed airliner, calm sweeping camera.

Render (720p, 24 fps):
  python -m manim render -r 1280,720 --fps 24 projects/style_test/style_a_3d.py StyleA3D
Plane geometry comes from airliner_geom.py (shared with style C). Lighting is baked per face (Lambert + warm sun +
cool sky/fill + rim + spec); Manim's own white-highlight shading is switched off. Runway items are recycled around
the camera so nothing ever falls behind it.
"""
import math
import os
import sys
from functools import partial

import numpy as np
from manim import *
from manim.camera.three_d_camera import ThreeDCamera
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import airliner_geom as G  # noqa: E402

S = 0.16  # scene units per metre
PHI = 94.5 * DEGREES  # camera slightly below the look-at point: horizon stays fixed on screen
DUR = 10.0
TMP = os.path.join(os.path.dirname(os.path.dirname(HERE)), "tmp", "style_test")


def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])


def make_background(path, w=1280, h=720):
    """Dark sunset gradient with sun glow, stars and a low ridge. Horizon row matches PHI."""
    y_h = h / 2 + math.tan(PHI - math.pi / 2) / (4 / 20) * h / 2
    stops = [(0.0, "#ffb45e"), (0.05, "#ff7a45"), (0.16, "#d1467f"), (0.35, "#6b2f8f"), (0.65, "#2a1b66"), (1.0, "#0a0e2c")]
    ys = np.arange(h)[:, None]
    xs = np.arange(w)[None, :]
    s = np.clip((y_h - ys) / y_h, 0, 1)
    img = np.zeros((h, w, 3))
    pos = [p for p, _ in stops]
    cols = np.array([hexrgb(c) for _, c in stops])
    for ch in range(3):
        img[:, :, ch] = np.interp(s[:, 0], pos, cols[:, ch])[:, None]
    # below the horizon: hazy ground colour fading to dark
    below = ys > y_h
    t = np.clip((ys - y_h) / (h - y_h), 0, 1)
    ground = hexrgb("#3b2438")[None, None, :] * (1 - t[:, :, None]) + hexrgb("#100a1a")[None, None, :] * t[:, :, None]
    img = np.where(below[:, :, None], ground, img)
    # sun glow + disc
    sx, sy = 0.72 * w, y_h - 6
    d2 = ((xs - sx) / (0.42 * w)) ** 2 + ((ys - sy) / (0.30 * h)) ** 2
    img += np.exp(-d2)[:, :, None] * hexrgb("#ff8a3c") * 0.55 * (ys < y_h + 20)[:, :, None]
    disc = np.clip(1.8 - np.sqrt((xs - sx) ** 2 + (ys - sy) ** 2) / 26.0, 0, 1) * (ys < y_h)
    img = img * (1 - disc[:, :, None]) + disc[:, :, None] * hexrgb("#fff1c8")
    # stars
    rng = np.random.default_rng(3)
    for _ in range(160):
        x, y = rng.integers(0, w), rng.integers(0, int(y_h * 0.55))
        img[y, x] = np.maximum(img[y, x], 0.5 + 0.5 * rng.random()) * (1 - y / (y_h * 0.6))
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    pts = [(0, h)]
    for x in range(0, w + 1, 8):
        pts.append((x, y_h - 8 - 14 * (1 + math.sin(x * 0.011)) - 9 * (1 + math.sin(x * 0.043 + 1)) - 4 * (1 + math.sin(x * 0.1))))
    pts.append((w, h))
    d.polygon(pts, fill=(58, 30, 84))
    arr = np.asarray(im).astype(float) + np.random.default_rng(1).normal(0, 0.7, (h, w, 3))
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(path)
    return path


BASE = {
    "white": (0.95, 0.93, 0.93), "blue": (0.16, 0.47, 0.85), "belly": (0.78, 0.76, 0.82), "engine": (0.85, 0.84, 0.87),
    "glass": (0.05, 0.07, 0.12), "dark": (0.04, 0.04, 0.06), "gear": (0.55, 0.55, 0.60),
}
EMISSIVE = {"nav_red": (1.0, 0.15, 0.15), "nav_green": (0.15, 1.0, 0.4), "nav_white": (1.0, 1.0, 1.0)}
GLOSSY = {"white": 0.5, "blue": 0.5, "engine": 0.7, "glass": 1.0, "belly": 0.3, "gear": 0.4, "dark": 0.1}
SUN = np.array([1.0, 0.45, 0.12]); SUN /= np.linalg.norm(SUN)
FILL = np.array([-0.25, -1.0, 0.35]); FILL /= np.linalg.norm(FILL)
VIEW = np.array([-0.45, -0.85, 0.05]); VIEW /= np.linalg.norm(VIEW)


def bake_color(mat, n):
    if mat in EMISSIVE:
        return np.array(EMISSIVE[mat])
    base = np.array(BASE[mat])
    sky, gnd = np.array([0.30, 0.22, 0.48]), np.array([0.22, 0.13, 0.14])
    lam = base * (sky * (0.5 + 0.5 * n[2]) + gnd * (0.5 - 0.5 * n[2]))
    lam += base * np.array([1.0, 0.62, 0.30]) * 1.05 * max(0.0, n @ SUN)
    lam += base * np.array([0.55, 0.30, 0.50]) * 0.35 * max(0.0, n @ FILL)
    rim = (1 - max(0.0, n @ VIEW)) ** 3 * np.array([1.0, 0.55, 0.25]) * (0.15 + 0.85 * min(1.0, max(0.0, 0.8 * (n @ SUN) + 0.4)))
    hv = SUN + VIEW
    hv /= np.linalg.norm(hv)
    spec = max(0.0, n @ hv) ** 24 * 0.5 * GLOSSY.get(mat, 0.3) * np.array([1.0, 0.7, 0.45])
    return np.clip(lam + 0.55 * rim + spec, 0, 1)


def smooth(a, b, t):
    u = min(1.0, max(0.0, (t - a) / (b - a)))
    return u * u * (3 - 2 * u)


class StyleA3D(ThreeDScene):
    def __init__(self, **kwargs):
        os.makedirs(TMP, exist_ok=True)
        bg = make_background(os.path.join(TMP, "a_bg.png"))
        super().__init__(camera_class=partial(ThreeDCamera, background_image=bg, should_apply_shading=False), **kwargs)

    # far-layer helper: items that must always be painted under the plane, in a fixed order
    def _far(self, poly, layer):
        poly.shade_in_3d = True
        cam = self.camera
        poly.get_z_index_reference_point = lambda: -(1e6 - layer) * cam.get_rotation_matrix()[2]
        return poly

    def _flat(self, color, opacity=1.0, layer=0, n=4, stroke=0.0):
        p = Polygon(*[[i, 0, 0] for i in range(n)], fill_color=color, fill_opacity=opacity, stroke_width=stroke, stroke_color=color)
        return self._far(p, layer)

    def construct(self):
        tab = G.flight_table(DUR, 0.002)
        self.set_camera_orientation(phi=PHI, theta=-150 * DEGREES, focal_distance=20, zoom=1, frame_center=[0, 0, 2.6])

        # ---- plane: one polygon per face, colours baked once
        parts = G.build("low")
        verts, group_of_vert, faces = [], [], []
        for part in parts:
            off = len(verts)
            verts.extend(part["verts"])
            group_of_vert.extend([part["group"] == "gear"] * len(part["verts"]))
            cen = np.mean(part["verts"], axis=0)
            for f, mat in zip(part["faces"], part["mats"]):
                idx = np.array(f) + off
                pts = np.array(part["verts"])[np.array(f)]
                nrm = np.cross(pts[2] - pts[0], pts[3 % len(pts)] - pts[1]) if len(pts) >= 4 else np.cross(pts[1] - pts[0], pts[2] - pts[0])
                ln = np.linalg.norm(nrm)
                nrm = nrm / ln if ln > 1e-9 else np.array([0, 0, 1.0])
                if nrm @ (pts.mean(axis=0) - cen) < 0:
                    nrm = -nrm
                col = bake_color(mat, nrm)
                poly = Polygon(*[[0, 0, 0]] * len(f), fill_color=ManimColor.from_rgb(tuple(col)), fill_opacity=1,
                               stroke_color=ManimColor.from_rgb(tuple(col)), stroke_width=0.6)
                poly.shade_in_3d = True
                faces.append((poly, idx))
        V0 = np.array(verts)
        is_gear = np.array(group_of_vert)
        gear0 = np.array([0, 0, -1.0])
        plane = VGroup(*[p for p, _ in faces])
        self.add(plane)

        # ---- ground, haze, runway, scenery (all recycled / re-centred each frame)
        ground = self._flat("#191120", layer=0)
        haze_y = self._flat("#35213a", layer=1)
        haze_x = self._flat("#35213a", layer=1)
        runway = self._flat("#2d2740", layer=2)
        sheen = self._flat("#5a3a52", 0.55, layer=2.5)  # sunset reflection on the asphalt, far end
        edge_l = self._flat("#d8d2cc", layer=3)
        edge_r = self._flat("#d8d2cc", layer=3)
        dashes = [self._flat("#d8d2cc", layer=4) for _ in range(26)]
        glows = [self._flat("#ffb45e", 0.22, layer=5, n=10) for _ in range(56)]
        cores = [self._flat("#ffe2a8", 1.0, layer=6, n=8) for _ in range(56)]
        shadow = self._flat("#05030a", 0.5, layer=4.5, n=14)
        scenery = []
        for x0, x1, h, col in ((40, 105, 2.6, "#1b1530"), (122, 150, 3.4, "#1b1530"), (-30, 6, 3.0, "#1b1530")):
            scenery.append((self._flat(col, layer=1.5), x0, x1, h))
        windows = self._flat("#ffbf60", layer=1.6)
        tower = self._flat("#1b1530", layer=1.5)
        tower_cab = self._flat("#ffbf60", layer=1.6)
        self.add(ground, haze_y, haze_x, runway, sheen, edge_l, edge_r, shadow, *dashes, *glows, *cores, windows, tower, tower_cab,
                 *[s for s, *_ in scenery])

        def set_corners(poly, pts):
            pts = np.array(pts, dtype=float)
            poly.set_points_as_corners(np.vstack([pts, pts[:1]]))

        def rect(x0, x1, y0, y1, z=0.0):
            return [[x0, y0, z], [x1, y0, z], [x1, y1, z], [x0, y1, z]]

        def ngon(cx, cy, r, n, z=0.02, sy=1.0):
            return [[cx + r * math.cos(2 * math.pi * k / n), cy + r * sy * math.sin(2 * math.pi * k / n), z] for k in range(n)]

        def frame(t):
            px, pz, pitch, g = tab[min(int(round(t / 0.002)), len(tab) - 1)]
            # plane vertices: gear retract about gear0, pitch about the main-gear contact, then to world (units)
            V = V0.copy()
            V[is_gear] = gear0 + g * (V[is_gear] - gear0)
            ca, sa = math.cos(-pitch), math.sin(-pitch)
            R = np.array([[ca, 0, sa], [0, 1, 0], [-sa, 0, ca]])
            piv = np.array(G.PIVOT)
            W_ = (V - piv) @ R.T
            W_ += np.array([px, 0.0, pz])
            W_ *= S
            for poly, idx in faces:
                p = W_[idx]
                poly.set_points_as_corners(np.vstack([p, p[:1]]))
            centre = (np.array([px, 0.0, pz]) + R @ (-piv)) * S
            cx = centre[0]

            # camera: tracking + slow sweep from the rear quarter towards the side, plane low in frame, rises after lift-off
            u = smooth(0, DUR, t)
            self.set_camera_orientation(theta=(-150 + 52 * u) * DEGREES,
                                        frame_center=[cx + 2.0, 0.0, 2.6 + 0.65 * (centre[2] - S * 4.2)])

            x_lo = cx - 12
            set_corners(ground, rect(x_lo, cx + 250, -12, 140))
            set_corners(haze_y, rect(x_lo, cx + 250, 105, 140))
            set_corners(haze_x, rect(cx + 215, cx + 250, -12, 140))
            set_corners(runway, rect(x_lo, cx + 250, -3.6, 3.6, 0.005))
            set_corners(sheen, rect(cx + 60, cx + 250, -3.6, 3.6, 0.008))
            set_corners(edge_l, rect(x_lo, cx + 250, -3.42, -3.3, 0.01))
            set_corners(edge_r, rect(x_lo, cx + 250, 3.3, 3.42, 0.01))
            pitch_d = 8.0  # 50 m
            k0 = math.floor((cx - 10) / pitch_d)
            for k, d in enumerate(dashes):
                x = (k0 + k) * pitch_d
                set_corners(d, rect(x, x + 4.8, -0.07, 0.07, 0.012))
            lp = 6.4  # 40 m
            j0 = math.floor((cx - 12) / lp)
            for k in range(28):
                for side, sgn in enumerate((-1, 1)):
                    i = k * 2 + side
                    x = (j0 + k) * lp
                    set_corners(glows[i], ngon(x, sgn * 3.92, 0.26, 10, 0.03))
                    set_corners(cores[i], ngon(x, sgn * 3.92, 0.07, 8, 0.04))
            # plane shadow on the runway, fades with altitude
            alt = max(0.0, centre[2] - S * 4.2)
            shadow.set_fill(opacity=max(0.0, 0.5 - 0.12 * alt))
            set_corners(shadow, ngon(cx - 0.6 + 0.6 * alt, -0.3, 3.4 * (1 + 0.1 * alt), 14, 0.02, sy=0.45))
            # far-side buildings (static in the world)
            for poly, x0, x1, h in scenery:
                set_corners(poly, [[x0, 26, 0], [x1, 26, 0], [x1, 26, h], [x0, 26, h]])
            set_corners(windows, [[42, 25.9, 1.2], [103, 25.9, 1.2], [103, 25.9, 1.55], [42, 25.9, 1.55]])
            set_corners(tower, [[160, 30, 0], [162.2, 30, 0], [162.2, 30, 8], [160, 30, 8]])
            set_corners(tower_cab, [[158.6, 29.9, 8], [163.6, 29.9, 8], [163.6, 29.9, 9.2], [158.6, 29.9, 9.2]])

        frame(0.0)
        tracker = ValueTracker(0.0)
        ticker = Mobject()
        ticker.add_updater(lambda m: frame(tracker.get_value()))
        self.add(ticker)
        self.play(tracker.animate.set_value(DUR), run_time=DUR, rate_func=linear)
