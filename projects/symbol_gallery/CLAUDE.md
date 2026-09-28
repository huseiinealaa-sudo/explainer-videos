# Project: symbol_gallery — catalogue of the icons and ISA symbols (1 silent video)

Project-specific rules. The general rules in the root `CLAUDE.md` also apply; where they differ, this file wins for this project.

- Video: `projects/symbol_gallery/symbol_gallery.py` → `output/symbol_gallery.mp4` (1080p, silent).
- **No narration** (owner's request): `NARRATION` holds the length of each silent segment in
  seconds (`symbol_gallery_data.DURATIONS`); the pipeline writes silent audio for them, so the
  QA tools and `at()` work as usual (`cue()` needs words and is not used). The narration
  approval step does not apply; the critic judges drawing–name fit and ISA conformity instead
  of drawing–speech fit.
- Content: every vendored Tabler icon (`explainer/icons.py`), then the ISA groups of
  `explainer.symbols.ISA_GROUPS`, the bubbles, the line types and an example loop.
- Sources: `explainer/symbols/SOURCES.md` (per symbol); `sources/symbol_gallery.md`.
- Tags and loop numbers: illustrative only, all in `symbol_gallery_data.py`.
- When icons or symbols are added to the library: add them to the data module (icons come in
  by themselves through `icon_names()`), re-run the QA loops, and re-render only if the owner
  asks (a published video is not re-rendered without the owner).
