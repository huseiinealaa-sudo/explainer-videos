# Project: theme_gallery — catalogue of the themes, backgrounds and motion tools (1 silent video)

Project-specific rules. The general rules in the root `CLAUDE.md` also apply; where they differ, this file wins for this project.

- Video: `projects/theme_gallery/theme_gallery.py` → `output/theme_gallery.mp4` (**720p**, silent; `[render] resolution = "720p"` in `project.toml`).
- **No narration** (owner's request): `NARRATION` holds the length of each silent segment in seconds (`theme_gallery_data.DURATIONS`). The narration approval step does not apply.
- Content: a sample of library scenes in each theme (dark, blueprint, light), the backgrounds (colour, gradient, image; then the gradient, grid and particle motions) and the five motion tools (`zoom_on`, `stagger_in`, `move_along_path`, `pulse`, `parallax`).
- Theme: `dark` (the project's), switched on screen with `self.set_theme(...)`.
- All values are illustrative and live in `theme_gallery_data.py`. `assets/plate.png` is a procedurally generated picture (own work, no licence issue).
- When a theme, a background or a motion tool is added: add it here, re-run the QA loop, and re-render only if the owner asks (a published video is not re-rendered without the owner).
