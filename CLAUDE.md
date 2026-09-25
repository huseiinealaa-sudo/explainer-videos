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

## Fast workflow (every project)
1. **Source first.** Each project has a cleaned source file `projects/<name>/sources/<name>_source.md`. It is the primary reference for the content and holds no real (site, personal or confidential) data.
2. **Research only verifies.** Use web research only to check the claims in the source. Add nothing except to correct an error or to fill a gap the explanation cannot do without; mark every such addition or correction with [+] and its source.
3. **One approval message.** Write the narration of ALL episodes (or all segments of a single video) in one go, and present it in ONE message together with any source conflicts and any new values.
4. **Then produce without stopping.** Once the narration is approved, continue the whole production (preview, final render, commit, push) without pausing, up to ONE pull request. Stop early only for an error that blocks completion.
5. Reply to the owner in Arabic.

## Narration
- Default voice: `ar-SA-HamedNeural` (chosen by the owner), normal speed. A project may set another voice or language in its own `CLAUDE.md`.
- Default language: Modern Standard Arabic.
- Arabic narration MUST be fully diacritized (تشكيل كامل) before sending to edge-tts — this noticeably improves pronunciation.
- Foreign terms in the narration are written in the letters of the narration language so the voice pronounces them correctly (each project keeps its own list).
- Split narration into segments; each scene duration must match its audio segment.

## Video defaults
- Resolution: 1080p, aspect 16:9.
- Style: whiteboard — white background, black strokes drawn progressively.
- On-screen text: English or equations only (Arabic RTL rendering in Manim is unreliable).
- Merge audio + video with ffmpeg.
- Series: each episode 3–4 minutes unless the project says otherwise. After all episodes are approved, they may be concatenated with ffmpeg into one file with a short title card between episodes (no re-render of episodes).

## Templates
- Every new video script goes in `projects/<name>/<name>_<video>.py`. The script name is also the output name (`output/<name>_<video>.mp4`) and the build folder name (`tmp/<name>_<video>/`).
- Scripts import the shared settings from `scripts/style.py` with this header (until the shared package replaces it):
  ```python
  import sys
  from pathlib import Path

  sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
  from style import *  # noqa: E402
  ```
- Use `projects/ut_intro/ut_intro.py` as the reference for visual style, pacing, and scene structure.
- Before rendering, show the owner the narration text for approval (see Fast workflow).
- Render a low-quality preview first to check layout, then render the final 1080p:
  `python projects/<name>/<name>_<video>.py --preview` → `tmp/<name>_<video>/preview.mp4`, then
  `python projects/<name>/<name>_<video>.py` → `output/<name>_<video>.mp4`.

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
