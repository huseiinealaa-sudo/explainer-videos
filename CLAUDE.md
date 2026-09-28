# explainer-videos — Project Instructions

## Purpose
A general template that turns any file or topic into a professional whiteboard-style explainer video (or a series of episodes): Manim animation + narration (edge-tts), merged with ffmpeg.
Each topic is a project in `projects/<name>/`. Project-specific rules live in `projects/<name>/CLAUDE.md`; they add to these general rules and win where they differ.

## Reply language
- Always reply to the owner in Arabic (Modern Standard Arabic).

## Session setup (run at the start of EVERY session)
The cloud container is temporary. Before any work:
```bash
SETUPTOOLS_USE_DISTUTILS=stdlib pip install manim
SETUPTOOLS_USE_DISTUTILS=stdlib pip install -e .   # the explainer package (repo root)
```
Then verify: `ffmpeg -version`, `manim --version`, `edge-tts --version`, `python -c "import explainer"`.

## Known environment issues
1. **manim install fails** on building `srt` (AttributeError: install_layout) → always install with `SETUPTOOLS_USE_DISTUTILS=stdlib`.
2. **edge-tts fails with CERTIFICATE_VERIFY_FAILED** because traffic goes through a proxy and edge-tts hardcodes certifi. Do NOT use the edge-tts CLI. Use Python and patch the SSL context at runtime (`synthesize()` in `scripts/style.py` already does this):
```python
import ssl, edge_tts.communicate as c
c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
```
3. **No LaTeX in the container**: build equations from `Text` pieces, not `MathTex`/`Tex`.

## Quality standard
- The quality reference is the prover series (`projects/prover`). Quality comes before time; time is measured, not targeted.
- The material sets the length: each main section of the source gets 2–4 minutes, and each segment carries one main idea. The default format is a series of 3–5-minute episodes.
- Every concept: what it is, why, and a worked example when it involves numbers.
- Every mechanism, motion or sequence is shown as an animated drawing, drawn from scratch when the library does not have it. Text and table scenes take no more than about a third of an episode's duration.
- Privacy transforms, it does not delete: site cases, real numbers and screenshots become illustrative examples or simplified drawings.
- Every video stands on its own: a concept is not shortened because an earlier video explained it.
- Nothing is dropped for lack of verification or of time without showing it to the owner with a proposal.
- The narration is presented with a quality gate: the number of worked examples, the number of custom drawings, the share of text-scene time in each episode, and everything left out with its reason.
- In a series, the first episode is produced in full and pushed; the others are completed only after the owner approves its level.

## Fast workflow (every project)
The Fast workflow is subject to the Quality standard above; the step-by-step procedure is the `explainer-video` skill (`.claude/skills/explainer-video/SKILL.md`).
1. **Source first.** Each project has a cleaned source file `projects/<name>/sources/<name>_source.md`. It is the primary reference for the content and holds no real (site, personal or confidential) data.
2. **Research only verifies.** Use web research only to check the claims in the source. Add nothing except to correct an error or to fill a gap the explanation cannot do without; mark every such addition or correction with [+] and its source.
3. **One approval message.** Write the narration of ALL episodes (or all segments of a single video) in one go, and present it in ONE message together with the storyboard, the quality gate, any source conflicts and any new values.
4. **Then produce without stopping.** Once the narration is approved, continue the whole production (preview, final render, commit, push) up to ONE pull request. The only stops allowed after the narration is approved are presenting the first episode for the owner's approval of its level, and an error that blocks completion; no other confirmation to continue is requested, and fixing layout and sync is part of production.
5. **Every preview is checked before the final render, in two loops counted separately** (see Preview QA):
   - **Automatic loop first:** preview → `--qa` → fix the critical overlap findings → again, until the overlap reports show zero critical findings, at most 5 iterations per video. It costs no critic round.
   - **Then the critic loop:** the `video-critic` agent reviews the preview and its findings are fixed, at most 3 rounds per video. If critical overlap findings are still open after 5 automatic iterations, the critic is called anyway and told which ones (time, elements, why they stayed). Before each later critic round the automatic loop runs again on the changed segments.
   - Whatever is still open after critic round 3 (critic or overlap report) is listed in the pull request, never hidden.
6. Reply to the owner in Arabic.

## Narration
- Default voice: `ar-SA-HamedNeural` (chosen by the owner), normal speed. Default language: Modern Standard Arabic.
- Each project sets its language, voice and speed in `projects/<name>/project.toml` (`language`, `voice`, `rate` under `[narration]`); a missing file or key falls back to the defaults above, and a language without a voice gets that language's default voice (`explainer.pipeline.DEFAULT_VOICES`).
- Arabic narration MUST be fully diacritized (تشكيل كامل) before sending to edge-tts — this noticeably improves pronunciation.
- Foreign terms in the narration are written in the letters of the narration language so the voice pronounces them correctly (each project keeps its own list).
- Split narration into segments; each scene duration must match its audio segment.
- Word timing: `synthesize()` saves the edge-tts WordBoundary timings of each segment next to its audio (`tmp/<script>/audio/seg{i}.json`). `SyncedScene.cue(seg, phrase)` uses them to show an item exactly when its word is spoken (Arabic and English); without them it falls back to the phrase's relative position in the text. Cue phrases are copied from the narration exactly as written (same diacritics).

## Video defaults
- Resolution: 1080p, aspect 16:9.
- Style: whiteboard — white background, black strokes drawn progressively.
- On-screen text: English or equations only (Arabic RTL rendering in Manim is unreliable).
- Merge audio + video with ffmpeg.
- Series: each episode 3–5 minutes unless the project says otherwise (see Quality standard). After all episodes are approved, they may be concatenated with ffmpeg into one file with a short title card between episodes (no re-render of episodes).

## Templates
- Every new video script goes in `projects/<name>/<name>_<video>.py`. The script name is also the output name (`output/<name>_<video>.mp4`) and the build folder name (`tmp/<name>_<video>/`).
- New projects start from `templates/new_project/` (project `CLAUDE.md`, `project.toml`, `sources/<name>_source.md`, optional `<name>_data.py`, sample episode script); the copy steps are at the top of its `CLAUDE.md`.
- New scripts use the installed `explainer` package: `from explainer import *` (Manim, style, `SyncedScene` with `timeline/sync/at/cue/say/clear`, the pipeline, and the scene library in `explainer/scenes.py`); they end with `main(__file__, "SceneName", NARRATION)`.
- The scene library is for the general structure (titles, equations, tables); mechanisms and motions are drawn custom (see Scene library).
- Palette: `ACCENT_1`…`ACCENT_4` (blue, orange, green, red), `OK_C`, `ALERT_C`, `GREY_INK`, `LIGHT_INK`, `PANEL_FILL`; each project assigns the accents a meaning in its `CLAUDE.md`.
- Series: join finished episodes with `explainer.series.concat_series(...)` (title cards, stream copy, no re-encode of episodes).
- Older scripts (prover series, ut_intro) keep their header `sys.path.insert(0, .../"scripts")` + `from style import *`; `scripts/style.py` is a bridge to the package. Do not port them to the library.
- The prover series (`projects/prover/`) is the reference for quality, pacing and scene structure (see Quality standard); `projects/ut_intro/ut_intro.py` is a short example of the visual style.
- Before rendering, show the owner the narration text for approval (see Fast workflow).
- Render a low-quality preview first to check layout, then render the final 1080p:
  `python projects/<name>/<name>_<video>.py --preview` → `tmp/<name>_<video>/preview.mp4`, then
  `python projects/<name>/<name>_<video>.py` → `output/<name>_<video>.mp4`.
  `--segments 2` (or `2-3`) renders only those narration segments as a preview (`tmp/<name>_<video>/preview_seg02.mp4`); `--qa` adds the preview QA below.

## Scene library
`explainer/scenes.py`, imported by `from explainer import *`. Every function takes the scene first, animates its block and returns the group; staged blocks take `cues=[...]` (times from `self.cue(seg, phrase)`). Catalogue: `output/template_scene_gallery.mp4` (clip number = row number; each clip shows `NN / 18  name()` in the corner).

| # | Function | Use it when | Main inputs |
|---|---|---|---|
| 1 | `title_card` | opening a video or episode | `title, subtitle, series` |
| 2 | `section_title` | naming the current part in the corner | `text, prev` (transforms the previous heading) |
| 3 | `bullet_list` | a few points, each shown as it is spoken | `items, heading, cues, numbered` |
| 4 | `equation` | a formula whose parts are coloured or framed | `parts` (Text pieces), `colors={index: colour}` |
| 5 | `worked_calculation` | formula → substituted values → result | `formula, values, result, cues` |
| 6 | `labeled_diagram` | naming the parts of any drawing | `diagram, callouts=[(text, target, direction)], cues, start` (first badge number, for callouts revealed in batches) |
| 7 | `process_flow` (+ `highlight_step`) | a sequence of steps, lighting the current one | `steps, cues, vertical` |
| 8 | `stage_bar` (+ `set_stage`) | showing which stage of a cycle we are in | `stages, active, y` |
| 9 | `data_table` (+ `highlight_row`) | tabular values, marking one row | `header, rows, cues` |
| 10 | `comparison` | two options or cases side by side | `left, right` (title, lines…), `verdict` |
| 11 | `line_chart` | a trend against an acceptance band | `xs, ys, x_label, y_label, band` |
| 12 | `bar_chart` | magnitudes against a limit | `labels, values, unit, limit` |
| 13 | `checklist` | pass/fail items or procedure checks | `items, cues, failed` |
| 14 | `summary_box` | key takeaways at the end | `heading, lines, cues` |
| 15 | `concept_map` | how ideas relate (topics without numbers) | `center, nodes, links, cues` |
| 16 | `timeline` | events or steps in order (topics without numbers) | `events=[(when, text)], cues` |
| 17 | `image_panel` | a picture or SVG sketch the project may publish | `path, caption, credit, height` |
| 18 | `document_panel` (+ `highlight`) | a report, form or log, framing the line under review | `lines` (text or (text, BOLD)), `height`; `highlight(scene, doc, idx)` |

Helpers: `emphasize(scene, mob)` frames any part; `badge(n)` is a numbered circle. In `SyncedScene`: `self.say(text)` is the bottom caption line and `self.clear(*keep)` fades the screen.

**Icons and engineering symbols** (also from `from explainer import *`; catalogue: `output/symbol_gallery.mp4`, project `projects/symbol_gallery/`). They return mobjects without animating them, so the scene draws them (`Create`, `FadeIn`) and places them with `next_to` / `arrange` like any drawing.

| Function | Use it when | Main inputs |
|---|---|---|
| `icon` (`explainer/icons.py`) | a small pictogram next to a label, point or step (alarm, time, file, tool ...) | `name, color, size` (units, the icon's 24×24 box), `stroke_width`; returns an `SVGMobject` exactly `size` × `size`, centred |
| `icon_grid` | several icons with their names | `names, cols, size, cell` |
| `gate_valve` `globe_valve` `ball_valve` `butterfly_valve` `check_valve` `control_valve` `relief_valve` | valves on a P&ID or process drawing | `size, color`; ports `in`, `out` (+ `actuator` on `control_valve`) |
| `centrifugal_pump` `pd_pump` `compressor` `tank` `heat_exchanger` | pumps, machines, vessels | ports `in`/`out`; tank `top`/`inlet`/`outlet`/`bottom`; exchanger `tube_in`/`tube_out`/`shell_in`/`shell_out` |
| `orifice_plate` `turbine_meter` `magnetic_flowmeter` `coriolis_meter` `vortex_meter` | in-line flow elements (flow left → right) | ports `in`, `out`, `tap` (to the transmitter) |
| `instrument` | an ISA instrument bubble with tag | `function` ("FT"), `loop` ("101"), `location` = `field` / `panel` / `behind_panel` / `dcs` / `plc`; ports `top`/`bottom`/`left`/`right` |
| `connect` (+ `signal_line`) | a line between two ports | `connect(a, "out", b, "in", kind, route)`; `kind` = `process` / `connection` / `pneumatic` / `electrical` / `capillary` / `data`; `route` = `straight` / `hv` / `vh` / `hvh` / `vhv` or `via=[points]`; `arrow=True` |

- Icons: Tabler outline icons (MIT), version `TABLER_VERSION`, vendored in `explainer/assets/tabler/outline/` with its `LICENSE`. Only the icons in that folder load (list: `python -m explainer.icons list`); add more of the same version with `python -m explainer.icons add <name> ...` and commit them.
- ISA symbols (`explainer/symbols/isa.py`) are drawn in code: every symbol is a `Symbol` (a `VGroup`) with the same stroke and unit size, and `sym.port(name)` gives a point that moves with it. The free references behind each drawing are in `explainer/symbols/SOURCES.md`; `ISA_GROUPS` lists them for catalogues. Tags and loop numbers in videos stay illustrative.
- A video without narration passes segment lengths (seconds) as `NARRATION`: the pipeline writes silent audio, and the scene places items with `self.at(seg, frac)`.

**Rule:** the library is for the general structure (titles, equations, tables); mechanisms and motions are drawn custom. The storyboard names, for each segment, what comes from the library and what is drawn custom. A custom block that proves reusable goes into the library (with a clip in the catalogue) rather than staying in one project.

**Layout rule:** place texts and labels relative to each other and to what they name (`next_to`, `arrange`, `align_to`), not at fixed coordinates, and keep them at least `SAFE_MARGIN` (0.25 units) inside the frame; `fit()` keeps a group within `SAFE_WIDTH`. Text stays at `MIN_FONT_SIZE` (14) or larger after any scaling. Both limits are set so that the prover series passes them.

## Preview QA
Every preview passes these checks before the final render (procedure: the `explainer-video` skill):
- **Overlap check** (`explainer/qa/overlap.py`): `python projects/<name>/<script>.py --segments 2 --qa`, or for any script, old ones included, `python -m explainer.qa projects/<name>/<script>.py [--segments 2]`. After every animation it records texts and labels overlapping each other or shapes, texts closer than `CLEARANCE` (0.06 units, stroke width included) to a line, arrow or shape outside their frame (touching included), anything leaving the frame, text inside the safe margin, and text below `MIN_FONT_SIZE`; a text inside its own frame and a label's own leader arrow are not errors. It is run in the automatic loop (Fast workflow step 5) until it reports zero critical findings (at most 5 iterations) before the critic is called. `python -m explainer.qa.selftest` and `python -m unittest discover tests` check its rules. Output: one JSON report per segment in `tmp/<script>/qa/<run>/overlap/segNN.json` (time, the two elements, overlap amount, grid cell, fix suggestion).
- **Contact sheets** (`explainer/qa/contact_sheet.py`, made by the same `--qa` run): a frame every 3 s plus the start and end of each segment, with a 6×6 grid (A1 top-left … F6 bottom-right) and the time, 3×3 frames per sheet in `tmp/<script>/qa/<run>/sheets/`.
- **Critic** (`.claude/agents/video-critic.md`): a read-only agent that reads the sheets, the overlap reports, the storyboard, the approved narration and the data module, scores each segment and returns PASS or FIX. It keeps its recurring findings in `.claude/agent-memory/video-critic/MEMORY.md` and updates that file itself: it has Write/Edit, and a PreToolUse hook in its definition (`.claude/hooks/critic_memory_guard.py`) blocks any write outside `.claude/agent-memory/video-critic/`. Commit the memory file with the video.

## Accuracy and privacy (the repository is PUBLIC)
- Never put real site, personal or confidential data in the repository or the videos (serial numbers, IDs, real measured values, names, dates, locations). Use illustrative values.
- If a project shows numbers, all of them come from one data module in the project (e.g. `projects/<name>/<name>_data.py`); never type derived values by hand. Projects without numbers need no data module.
- On a technical or regulated topic, the first video (episode 1 of a series) opens with one sentence: this is educational material; the binding reference is the official documentation and approved procedures.
- If sources conflict with each other or with the owner's outline or source file, DO NOT decide silently: list the conflict in the narration approval message and ask the owner.
- If a fact cannot be verified, leave it out of the narration; never guess.
- Never try to complete site-specific data (nameplate values, certificates, open notes, or any real identifiers). It stays out of the repository and the videos.
- In the narration approval message, mark every sentence that was added or corrected from research with [+] and its source.

## Research and verification
- Verify every technical claim before it goes into the narration (within the limits of the Fast workflow).
- Source priority: 1) manufacturer, author or official documents, 2) standards and their official summaries, 3) technical papers, 4) reputable training material. Never use forums or unsourced blogs as the only source.
- Save sources for each video or episode in `projects/<name>/sources/<name>_<video>.md`: claim → source URL → short note.
- Conflicts, unverifiable facts, site-specific data and [+] marking: see Accuracy and privacy.

## Repository rules
- Commit ONLY final videos to `output/` (never commit `media/` or temp audio). `output/` stays flat.
- Commit each video's script (with its data module and sources) to `projects/<name>/`; build files stay in the git-ignored `tmp/`.
- Never move, rename or re-render a published video in `output/` unless the owner asks.
- Keep each video under 100 MB (GitHub limit).
- File names: lowercase_with_underscores.
