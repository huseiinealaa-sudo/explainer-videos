"""Backgrounds: a colour, a gradient or a picture behind the scene, with optional slow motion.

    scene.background()                                  # the theme's own (SyncedScene)
    scene.background(color="#102030")
    scene.background(gradient=[BG, BG_ALT], angle=-35)
    scene.background(image="projects/x/assets/plate.jpg", dim=0.55)
    scene.background(gradient=[BG, BG_ALT], motion="gradient")      # a gradient that slides
    scene.background(color=BG, motion=("grid", "particles"))        # drifting grid + particles
`motion` is one name or a tuple of "gradient" (the gradient plate drifts and turns slowly),
"grid" (a faint grid drifts), "particles" (calm dots float up). A project can ask for one
in project.toml: [style] background = "particles".

Backgrounds are decoration, so they stay out of the way: they sit behind everything (index 0 of
scene.mobjects), SyncedScene.clear() keeps them, the QA overlap check does not see them and
measures the contrast of every text against the surface they paint (Background.color_at).
Motion is slow (a full turn takes 30-60 s), and grid lines and particles never go above
GRID_ALPHA, the opacity at which every theme still gives its text 4.5:1 (theme.check_theme).

Manim renders every mobject before the first one that is animated as one cached image, and a
pause with nothing to update as a frozen frame. The moving layers therefore carry time-based
updaters (a `dt` argument) and sit at the start of scene.mobjects: the scene sees an updater
at index 0, so the background and everything above it is redrawn every frame, in waits too.
The updaters add up dt (the scene clock), so a segment preview that skips animations before its
window still lands on the same moment of the motion as the full video.
"""
from pathlib import Path

import numpy as np
from manim import ORIGIN, Circle, Group, ImageMobject, Line, Rectangle, VGroup, config

from .style import BG, GRID_C
from .theme import MOTIONS, THEMES, TOKENS, _rgb, blend, current_theme, token

__all__ = ["Background", "make_background", "theme_background"]

GRID_STEP = 0.8             # units between grid lines
GRID_MAJOR = 4              # every 4th line is stronger (the blueprint look)
GRID_DRIFT = (0.10, 0.06)   # units per second
PARTICLES = 30
GRADIENT_PERIOD = (47.0, 61.0, 83.0)    # seconds of the slide in x, in y and of the turn


def _fw():
    return config.frame_width


def _fh():
    return config.frame_height


class Background(Group):
    """The layers of one background; color_at(x, y) is the surface colour there."""

    is_background = True

    def __init__(self, base=None, layers=(), kind="solid"):
        super().__init__()
        self.base, self.kind = base, kind
        self.dim_layer = None
        self.motion = ()
        if base is not None:
            self.add(base)
        self.add(*layers)

    def color_at(self, x, y):
        """RGB (0..1) of the surface behind a point, as painted now (motion layers of at most
        GRID_ALPHA opacity are not included: the theme check covers them)."""
        base = self.base
        if base is None:
            return _rgb(BG)
        if isinstance(base, ImageMobject):
            rgb = _image_color(base, x, y)
        else:
            rgb = _gradient_color(base, x, y)
        if self.dim_layer is not None:
            alpha = float(self.dim_layer.get_fill_opacity())
            rgb = blend(self.dim_layer.get_fill_rgbas()[0][:3], rgb, alpha)
        return tuple(rgb)


def _gradient_color(plate, x, y):
    """The colour of a gradient (or solid) plate at a point, as Cairo paints it: a linear
    gradient between the two points of get_gradient_start_and_end_points, stops evenly spaced."""
    rgbas = plate.get_fill_rgbas()
    if len(rgbas) == 1:
        return rgbas[0][:3]
    p0, p1 = (p[:2] for p in plate.get_gradient_start_and_end_points())
    d = p1 - p0
    s = float(np.clip(np.dot(np.array([x, y]) - p0, d) / max(np.dot(d, d), 1e-9), 0, 1))
    stops = np.linspace(0, 1, len(rgbas))
    return np.array([np.interp(s, stops, rgbas[:, k]) for k in range(3)])


def _image_color(img, x, y):
    px = img.pixel_array
    h, w = px.shape[:2]
    u = (x - img.get_left()[0]) / max(img.width, 1e-9)
    v = (img.get_top()[1] - y) / max(img.height, 1e-9)
    i, j = int(np.clip(v * h, 0, h - 1)), int(np.clip(u * w, 0, w - 1))
    return px[i, j][:3] / 255.0


# ---------------- base surfaces ----------------
def _plate(colors, angle, oversize=1.04):
    """A plate that covers the frame, filled with one colour or a linear gradient."""
    plate = Rectangle(width=_fw() * oversize, height=_fh() * oversize, stroke_width=0)
    colors = [token_color(c) for c in colors]
    plate.set_fill(colors if len(colors) > 1 else colors[0], opacity=1)
    if len(colors) > 1:
        plate.set_sheen_direction(_direction(angle))
    return plate


def _direction(angle_deg):
    """Sheen direction for a gradient at angle_deg (0 = left to right, -35 = towards the
    lower right). The vector is scaled by the plate's half sizes by Manim, so the gradient
    always runs corner-region to corner-region."""
    a = np.radians(angle_deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def token_color(c):
    """A colour given as a theme token name ('bg'), a ThemeColor or any Manim colour."""
    return token(c) if isinstance(c, str) and c in TOKENS else c


# ---------------- motion layers ----------------
def _grid(drift):
    """Faint grid lines; with drift, they move and wrap (the pattern repeats every
    GRID_STEP × GRID_MAJOR, so the wrap is invisible)."""
    s = GRID_STEP
    cols, rows = int(_fw() / s) + 2 * GRID_MAJOR + 2, int(_fh() / s) + 2 * GRID_MAJOR + 2
    cols += cols % 2
    rows += rows % 2
    lines = VGroup()
    for k in range(-cols // 2, cols // 2 + 1):
        major = k % GRID_MAJOR == 0
        lines.add(Line([k * s, -rows / 2 * s, 0], [k * s, rows / 2 * s, 0],
                       stroke_width=2.2 if major else 1.0, stroke_color=GRID_C,
                       stroke_opacity=0.34 if major else 0.2))
    for k in range(-rows // 2, rows // 2 + 1):
        major = k % GRID_MAJOR == 0
        lines.add(Line([-cols / 2 * s, k * s, 0], [cols / 2 * s, k * s, 0],
                       stroke_width=2.2 if major else 1.0, stroke_color=GRID_C,
                       stroke_opacity=0.34 if major else 0.2))
    if drift:
        period, clock = s * GRID_MAJOR, [0.0]

        def move(m, dt):
            clock[0] += dt
            m.move_to([(GRID_DRIFT[0] * clock[0]) % period, (GRID_DRIFT[1] * clock[0]) % period,
                       0])
        lines.add_updater(move)
    return lines


def _particles(seed):
    """Calm dots drifting upward with a slight sway; positions are a function of the clock."""
    rng = np.random.default_rng(seed)
    dots = VGroup()
    params = []
    for _ in range(PARTICLES):
        r = rng.uniform(0.025, 0.07)
        d = Circle(radius=r, stroke_width=0).set_fill(GRID_C, opacity=rng.uniform(0.18, 0.4))
        params.append((rng.uniform(-_fw() / 2, _fw() / 2), rng.uniform(0, 1),
                       rng.uniform(0.12, 0.3), rng.uniform(0.15, 0.5), rng.uniform(0, 6.28),
                       rng.uniform(0.15, 0.4)))
        dots.add(d)
    clock, h = [0.0], _fh() + 0.6

    def float_up(m, dt):
        clock[0] += dt
        t = clock[0]
        for d, (x0, y0, speed, sway, phase, rate) in zip(m, params):
            y = (y0 * h + speed * t) % h - h / 2
            d.move_to([x0 + sway * np.sin(rate * t * 2 + phase), y, 0])
    dots.add_updater(float_up)
    float_up(dots, 0)
    return dots


def _slide(plate):
    """The gradient plate drifts and turns slowly: one colour region wanders across the frame."""
    clock, base = [0.0], plate.get_center().copy()
    px, py, pa = GRADIENT_PERIOD
    ax, ay = _fw() * 0.55, _fh() * 0.5

    def move(m, dt):
        clock[0] += dt
        t = clock[0]
        m.move_to(base + [ax * np.sin(2 * np.pi * t / px), ay * np.sin(2 * np.pi * t / py + 1.0),
                          0])
        m.set_sheen_direction(_direction(-35 + 28 * np.sin(2 * np.pi * t / pa)))
    plate.add_updater(move)
    move(plate, 0)


# ---------------- the factory ----------------
def make_background(color=None, gradient=None, angle=-35, image=None, dim=0.55, grid=False,
                    motion=(), seed=7):
    """A Background. One base surface: `color`, `gradient` (2-3 colours) or `image` (a path,
    covered over the frame and dimmed by `dim` with the theme's background colour so text
    stays readable); `grid=True` adds a static grid; `motion` is a name or tuple of
    "gradient", "grid", "particles" (see the module docstring)."""
    motion = (motion,) if isinstance(motion, str) else tuple(motion or ())
    bad = [m for m in motion if m not in MOTIONS]
    if bad:
        raise ValueError(f"unknown motion {bad}; use {', '.join(MOTIONS)}")
    dim_rect = None
    if image is not None:
        if not Path(image).exists():
            raise FileNotFoundError(f"background image {image}")
        base, kind = ImageMobject(str(image)), "image"
        scale = max(_fw() / base.width, _fh() / base.height)
        base.scale(scale).move_to(ORIGIN)
        dim_rect = Rectangle(width=_fw() * 1.04, height=_fh() * 1.04, stroke_width=0)
        dim_rect.set_fill(BG, opacity=dim)
    else:
        colors = list(gradient) if gradient else [color if color is not None else BG]
        if "gradient" in motion:
            if len(colors) == 1:        # a sliding gradient needs a second colour
                colors = [colors[0], token("bg_alt")]
            colors = colors + colors[:1] if len(colors) == 2 else colors
        base = _plate(colors, angle, oversize=3.2 if "gradient" in motion else 1.04)
        kind = "gradient" if len(colors) > 1 else "solid"
        if "gradient" in motion:
            _slide(base)
    layers = [dim_rect] if dim_rect is not None else []
    if grid or "grid" in motion:
        layers.append(_grid(drift="grid" in motion))
    if "particles" in motion:
        layers.append(_particles(seed))
    bg = Background(base, layers, kind)
    bg.dim_layer, bg.motion = dim_rect, motion
    return bg


def theme_background(name=None, motion=()):
    """The theme's own background (see THEMES[...]["background"]) with extra motion layers;
    None when it is a plain colour with no motion: the camera colour alone paints it."""
    spec = dict(THEMES[name or current_theme()]["background"])
    if "gradient" in spec:
        spec["gradient"] = [token(c) for c in spec["gradient"]]
    if "color" in spec:
        spec["color"] = token(spec["color"])
    if motion:
        spec["motion"] = (motion,) if isinstance(motion, str) else tuple(motion)
    if set(spec) == {"color"}:
        return None
    return make_background(**spec)
