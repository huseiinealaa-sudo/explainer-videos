"""explainer: whiteboard explainer videos (Manim + edge-tts + ffmpeg).

    from explainer import *     # manim, style, timing, pipeline and the scene library

Modules: style (colours, fonts, sizes), timing (SyncedScene, word timings),
pipeline (project.toml, narration, render, merge, build), series (concat_series),
scenes (the scene library).
"""
from manim import *  # noqa: F401,F403

from .style import *  # noqa: F401,F403
from .timing import *  # noqa: F401,F403
from .pipeline import *  # noqa: F401,F403
from .series import concat_series  # noqa: F401
from .scenes import *  # noqa: F401,F403
