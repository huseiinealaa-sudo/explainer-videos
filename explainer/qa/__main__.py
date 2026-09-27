"""Run any video script in QA mode, old scripts included (they keep their own command line).

    python -m explainer.qa projects/prover/prover_ep03_components.py --segments 4
    python -m explainer.qa projects/<name>/<script>.py            # the whole video

Loads the script without running its __main__ block to read NARRATION and its scene
class, then calls pipeline.build(..., preview=True, qa=True).
"""
import argparse
import runpy
import sys
from pathlib import Path

from ..pipeline import build
from ..timing import SyncedScene


def scene_of(namespace, run_name):
    scenes = [v for v in namespace.values()
              if isinstance(v, type) and issubclass(v, SyncedScene) and v.__module__ == run_name]
    if len(scenes) != 1:
        sys.exit(f"expected one SyncedScene in the script, found {[s.__name__ for s in scenes]}")
    return scenes[0].__name__


def main():
    parser = argparse.ArgumentParser(prog="python -m explainer.qa")
    parser.add_argument("script", help="projects/<name>/<script>.py")
    parser.add_argument("--segments", help="only these narration segments, e.g. 2 or 2-3")
    args = parser.parse_args()
    script = Path(args.script).resolve()
    sys.path.insert(0, str(script.parent))           # the script's data module
    run_name = "explainer_qa_target"
    ns = runpy.run_path(str(script), run_name=run_name)
    print(build(script, scene_of(ns, run_name), ns["NARRATION"], preview=True,
                segments=args.segments, qa=True))


if __name__ == "__main__":
    main()
