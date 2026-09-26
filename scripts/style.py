"""Bridge to the explainer package for scripts written before it existed.

The prover series and ut_intro keep their header (`sys.path.insert(... "scripts")`
then `from style import *`) and get exactly the names they used before; new scripts
use `from explainer import *` instead (see templates/new_project/).
"""
import asyncio  # noqa: F401  (exported as before)
import ssl  # noqa: F401
import subprocess  # noqa: F401
import sys
from pathlib import Path

# Works with or without `pip install -e .`: the package sits at the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from explainer.style import *  # noqa: E402,F401,F403
from explainer.timing import (SyncedScene, media_duration, segment_paths,  # noqa: E402,F401
                              segment_starts)
from explainer.pipeline import (PROXY_CA_BUNDLE, VOICE, build, merge_audio_video,  # noqa: E402,F401
                                render, synthesize)
