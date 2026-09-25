# explainer-videos — Project Instructions

## Purpose
Produce whiteboard-style explainer videos with Manim + Arabic narration (edge-tts), merged with ffmpeg.

## Session setup (run at the start of EVERY session)
The cloud container is temporary. Before any work:
```bash
SETUPTOOLS_USE_DISTUTILS=stdlib pip install manim
```
Then verify: `ffmpeg -version`, `manim --version`, `edge-tts --version`.

## Known environment issues
1. **manim install fails** on building `srt` (AttributeError: install_layout) → always install with `SETUPTOOLS_USE_DISTUTILS=stdlib`.
2. **edge-tts fails with CERTIFICATE_VERIFY_FAILED** because traffic goes through a proxy and edge-tts hardcodes certifi. Do NOT use the edge-tts CLI. Use Python and patch the SSL context at runtime:
```python
import ssl, edge_tts.communicate as c
c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
```

## Narration
- Voice: `ar-SA-HamedNeural` (default, chosen by the owner). Normal speed.
- Language: Modern Standard Arabic.
- The narration text MUST be fully diacritized (تشكيل كامل) before sending to edge-tts — this noticeably improves pronunciation.
- Split narration into segments; each scene duration must match its audio segment.

## Video defaults
- Resolution: 1080p, aspect 16:9.
- Style: whiteboard — white background, black strokes drawn progressively.
- On-screen text: English or equations only (Arabic RTL rendering in Manim is unreliable).
- Merge audio + video with ffmpeg.

## Templates
- Every new video script goes in `scripts/<video_name>.py` and must import shared settings from `scripts/style.py`.
- Use `scripts/ut_intro.py` as the reference for visual style, pacing, and scene structure.
- Before rendering, show the owner the fully diacritized narration text for approval.
- Render a low-quality preview first to check layout, then render the final 1080p:
  `python scripts/<video_name>.py --preview` → `tmp/<video_name>/preview.mp4`, then
  `python scripts/<video_name>.py` → `output/<video_name>.mp4`.

## Repository rules
- Commit ONLY final videos to `output/` (never commit `media/` or temp audio).
- Commit each video's script to `scripts/` alongside its video; build files stay in the git-ignored `tmp/`.
- Keep each video under 100 MB (GitHub limit).
- File names: lowercase_with_underscores.mp4
