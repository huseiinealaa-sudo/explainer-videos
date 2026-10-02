"""Themes: the colours of a video as one named set, chosen per project and switchable per scene.

A theme is a set of colour tokens:
    bg, bg_alt      the background and its second colour (gradients, the page behind panels)
    panel           fill behind panels, table rows and cards
    ink             text and primary strokes          muted   secondary text and strokes
    faint           inactive items and guides         line    lines, arrows, axes, symbols
    grid            the background grid and particles
    accent1..4      blue / orange / green / red roles (each project gives them a meaning)
    ok, alert       accepted / out-of-limit states
Three themes ship: "dark" (the default), "blueprint" and "light" (the original white board,
which the projects made before themes were pinned to, so they render exactly as they did).

The names in explainer.style (INK, BG, ACCENT_1, OK_C ...) are ThemeColor objects: ordinary
Manim colours whose value is rewritten in place when the theme changes. Code written as
`color=INK` therefore follows the theme, also in defaults evaluated at import time, and no
colour literal is needed outside this file. A mobject keeps the colour it was created with,
so switching the theme on a scene (SyncedScene.set_theme) starts from a cleared screen.

Choosing the theme, in order: the EXPLAINER_THEME variable, then the `theme` line of the
`[style]` table of the project's project.toml (the project is found from EXPLAINER_SCRIPT,
which the pipeline sets, or from the script on the command line), then "dark":
    [style]
    theme = "blueprint"          # dark | blueprint | light
    background = "particles"     # optional motion: gradient | grid | particles (or a list)
Contrast helpers (contrast_ratio, check_theme) are used by the QA overlap check and the tests.
"""
import os
import sys
import tomllib
from pathlib import Path

import numpy as np
from manim import ManimColor, config

THEME_ENV, SCRIPT_ENV = "EXPLAINER_THEME", "EXPLAINER_SCRIPT"
DEFAULT_THEME = "dark"
MIN_CONTRAST = 4.5                  # WCAG AA for normal text: the QA contrast rule
MOTIONS = ("gradient", "grid", "particles")
GRID_ALPHA = 0.4                    # strongest opacity of a background grid line or particle

TOKENS = ("bg", "bg_alt", "panel", "ink", "muted", "faint", "line", "grid",
          "accent1", "accent2", "accent3", "accent4", "ok", "alert")
# text tokens that must reach MIN_CONTRAST on every surface (bg, bg_alt, panel)
TEXT_TOKENS = ("ink", "muted", "faint", "line", "accent1", "accent2", "accent3", "accent4",
               "ok", "alert")
SURFACES = ("bg", "bg_alt", "panel")


def _theme(**c):
    c.setdefault("ok", c["accent3"])
    c.setdefault("alert", c["accent4"])
    return c


THEMES = {
    # The original whiteboard: every value is what the library used before themes existed.
    "light": {
        "colors": _theme(bg="#ffffff", bg_alt="#f3f3f3", panel="#f3f3f3", ink="#000000",
                         muted="#555555", faint="#9e9e9e", line="#000000", grid="#e3e3e3",
                         accent1="#1f5fa8", accent2="#c25a12", accent3="#2e7d32",
                         accent4="#c62828"),
        "background": {"color": "bg"},
    },
    # Deep slate-navy with a soft diagonal gradient and bright, saturated accents.
    "dark": {
        "colors": _theme(bg="#0e1424", bg_alt="#1c2748", panel="#1a2340", ink="#f3f6fc",
                         muted="#b4bfd6", faint="#8d9bb8", line="#dfe6f3", grid="#3b4a73",
                         accent1="#5cadff", accent2="#ffa94d", accent3="#4fd68f",
                         accent4="#ff7676"),
        "background": {"gradient": ("bg", "bg_alt")},
    },
    # Engineering drawing: white linework on blueprint blue, with a drafting grid.
    "blueprint": {
        "colors": _theme(bg="#0b3a7e", bg_alt="#134c96", panel="#10488e", ink="#f5f9ff",
                         muted="#d6e4f8", faint="#bcd2f2", line="#eaf2ff", grid="#4f84cc",
                         accent1="#ffe27a", accent2="#ffc293", accent3="#9af0b0",
                         accent4="#ffc6cc"),
        "background": {"color": "bg", "grid": True},
    },
}


# ---------------- colours that follow the theme ----------------
class ThemeColor(ManimColor):
    """A Manim colour whose value is the current theme's token (see set_theme)."""

    def __init__(self, token):
        super().__init__("#000000")
        self.token = token

    @classmethod
    def _from_internal(cls, value):
        return ManimColor(value)        # derived colours (darker(), interpolate()) are plain

    def __getattr__(self, name):
        # the palette used to be plain "#rrggbb" strings: .lower(), .lstrip() ... still work
        if name.startswith("__"):
            raise AttributeError(name)
        return getattr(self.to_hex(), name)

    def retarget(self, hex_value):
        # a new array, not an in-place write: colours already copied from this one keep theirs
        self._internal_value = ManimColor(hex_value)._internal_value.copy()


_COLORS = {t: ThemeColor(t) for t in TOKENS}
_state = {"name": None}


def token(name):
    """The ThemeColor of a token (INK is token('ink'))."""
    return _COLORS[name]


def theme_names():
    return list(THEMES)


def current_theme():
    return _state["name"]


def theme_colors(name=None):
    """{token: '#rrggbb'} of a theme (the current one by default)."""
    return dict(THEMES[name or _state["name"]]["colors"])


def set_theme(name):
    """Make `name` the current theme: every ThemeColor takes its value; Manim's default
    background colour follows. Returns the name."""
    if name not in THEMES:
        raise ValueError(f"unknown theme {name!r}; available: {', '.join(THEMES)}")
    for tok, color in THEMES[name]["colors"].items():
        _COLORS[tok].retarget(color)
    _state["name"] = name
    config.background_color = _COLORS["bg"].to_hex()
    return name


# ---------------- the project's choice ----------------
def _toml_for(script):
    path = Path(script).resolve().parent / "project.toml"
    return path if path.exists() else None


def _script_candidates():
    if os.environ.get(SCRIPT_ENV):
        yield os.environ[SCRIPT_ENV]
    for arg in sys.argv:
        if arg.endswith(".py") and Path(arg).exists():
            yield arg


def project_style(script=None):
    """The [style] table of the script's project.toml ({} if none), found from `script`,
    EXPLAINER_SCRIPT or a .py argument of the command line."""
    for cand in ([script] if script else []) + list(_script_candidates()):
        toml = _toml_for(cand)
        if toml:
            data = tomllib.loads(toml.read_text())
            style = dict(data.get("style", {}))
            if "theme" in data:                  # a top-level `theme = ...` line also works
                style.setdefault("theme", data["theme"])
            return style
    return {}


def project_theme(script=None):
    """The theme a project asks for (see the module docstring); DEFAULT_THEME if none."""
    return os.environ.get(THEME_ENV) or project_style(script).get("theme", DEFAULT_THEME)


def project_motion(script=None):
    """The background motion layers a project asks for, e.g. ('particles',)."""
    m = project_style(script).get("background", ())
    m = (m,) if isinstance(m, str) else tuple(m)
    bad = [x for x in m if x not in MOTIONS]
    if bad:
        raise ValueError(f"unknown background motion {bad}; use {', '.join(MOTIONS)}")
    return m


# ---------------- contrast (WCAG 2.x) ----------------
def _rgb(c):
    """(r, g, b) in 0..1 of a '#rrggbb' string, a Manim colour or an RGB triple."""
    if isinstance(c, (tuple, list, np.ndarray)):
        return tuple(float(v) for v in c[:3])
    return tuple(float(v) for v in ManimColor(c).to_rgb())


def luminance(c):
    """Relative luminance (0 black ... 1 white) of a colour."""
    lin = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in _rgb(c)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast_ratio(a, b):
    """WCAG contrast ratio (1:1 ... 21:1) between two colours."""
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def blend(top, bottom, alpha):
    """`top` over `bottom` at opacity alpha, as an RGB triple."""
    t, b = np.array(_rgb(top)), np.array(_rgb(bottom))
    return tuple(alpha * t + (1 - alpha) * b)


def check_theme(name, minimum=MIN_CONTRAST):
    """Pairs of a theme that fall short of `minimum`: [(token, surface, ratio), ...].
    Every text token is measured on every surface, and on the background under the
    strongest decoration (the grid lines at GRID_ALPHA)."""
    c = THEMES[name]["colors"]
    surfaces = {s: c[s] for s in SURFACES}
    surfaces["bg+grid"] = blend(c["grid"], c["bg"], GRID_ALPHA)
    bad = []
    for tok in TEXT_TOKENS:
        for s, color in surfaces.items():
            r = contrast_ratio(c[tok], color)
            if r < minimum:
                bad.append((tok, s, round(r, 2)))
    return bad


# the project's theme is active from the moment the package is imported
set_theme(project_theme())
