# Project: scene_gallery — catalogue of the scene library (1 video)

Project-specific rules. The general rules in the root `CLAUDE.md` also apply; where they differ, this file wins for this project.

- Video: `projects/scene_gallery/template_scene_gallery.py` → `output/template_scene_gallery.mp4` (the owner chose the `template_` output name; the script carries the same name so the build rules hold).
- Purpose: one clip per function of `explainer/scenes.py`, in `LIBRARY` order; the corner shows `NN / 18  function_name()`, the bottom line a one-line English description, the narration names the scene in Arabic.
- Source: the library itself (`explainer/scenes.py`); no research needed. See `sources/scene_gallery_source.md`.
- Numbers: all from `projects/scene_gallery/scene_gallery_data.py` (illustrative).
- Image: `assets/sketch.svg` is our own line drawing.
- When a function is added to the library: add it to `LIBRARY`, `DESCRIPTIONS`, a `demo_<name>` method and a narration segment, get the narration approved, then re-render (the owner must ask before a published video is re-rendered).
- Narration: Arabic, ar-SA-HamedNeural, normal speed (`project.toml`).
