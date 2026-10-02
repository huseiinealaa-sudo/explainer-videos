"""explainer: whiteboard explainer videos (Manim + edge-tts + ffmpeg).

    from explainer import *     # manim, style, timing, pipeline and the scene library

Modules: theme (the three themes, contrast), style (colours, fonts, sizes),
backgrounds (colour, gradient, image, slow motion), motion (zoom, stagger, path, pulse, parallax), timing (SyncedScene, word timings),
pipeline (project.toml, narration, render, merge, build), series (concat_series),
scenes (the scene library), icons (Tabler icons), symbols (ISA-5.1 P&ID symbols).
"""
from manim import *  # noqa: F401,F403

from .style import *  # noqa: F401,F403
from .backgrounds import *  # noqa: F401,F403
from .timing import *  # noqa: F401,F403
from .pipeline import *  # noqa: F401,F403
from .series import concat_series  # noqa: F401
from .scenes import *  # noqa: F401,F403
from .motion import *  # noqa: F401,F403
from .icons import *  # noqa: F401,F403
from .symbols import *  # noqa: F401,F403
