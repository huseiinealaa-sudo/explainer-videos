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

## Series: Daniel Compact Prover (7 episodes)

### Privacy (the repository is PUBLIC)
- NEVER use real site data: serial numbers, meter tags/IDs, real MF values, configuration name, CSUM, real dates or locations.
- Public manufacturer values are allowed: nominal BPV 0.2463 m³ (24-inch model), nominal K-factor 60000 pls/m³, all standard equations and API tables.
- All numbers shown in any episode MUST come from scripts/prover_demo_data.py. Never type derived values by hand.

### Illustrative base data (inputs only)
| Item | Value |
|---|---|
| Prover serial | PRV-DEMO-001 |
| Meter tag | FT-DEMO-01 |
| Meter serial | MM-DEMO-0001 |
| Meter type | Coriolis (Micro Motion, generic) |
| Configuration name / CSUM | DEMO_PRV_CFG / a1b2 |
| Proving date | 15/03/2026 |
| BPV | 0.2463 m³ |
| Nominal K-factor | 60000 pls/m³ |
| Flow rate | 250.0 m³/h |
| Standard density (15 °C) | 840.0 kg/m³ |
| Prover temperature | 30.0 °C |
| Meter temperature | 29.9 °C |
| CPSp / CPLp / CPLm | 1.000000 / 1.000150 / 1.000160 |
| Passes per run | 3 |
| Runs | 5 |

### scripts/prover_demo_data.py must compute
- CTSp = 1 + 0.0000216 × (Tp − 15)
- CTLp and CTLm from API Table 54B (1980) using the density group constants; show which group applies.
- Choose 5 run pulse counts so the average MF ≈ 0.9990 and repeatability on K ≈ 0.03% (within the 0.05% limit).
- For each run: PRV VOL, MTR VOL, M-FACTOR, K-FACTOR; then average MF, final K, repeatability.
- Pass time = BPV ÷ Q × 3600 and expected frequency = Q × K ÷ 3600.
- Plenum example: line pressure 40 psig, R = 5 → 68 psig.
- Print everything as a table; other scripts import values from this module.

### Episodes
1. Proving principle and the MF equation
2. Pass, run, repeatability, Coriolis specifics
3. Compact prover construction (10 components)
4. Operating cycle (5 stages) and why flow never stops
5. Double chronometry, plenum pressure, upstream/downstream volumes, CTSP
6. FloBoss S600+, field case, web interface, typical proving session
7. Auditing the report: recompute one run step by step
Excluded from videos: maintenance tables, specifications, B54 constant tables, site data, open notes, references.

### Series rules
- Episode 1 opens with one sentence: this is educational material; the binding reference is the manufacturer's manual and approved site procedures.
- Each episode 3–4 minutes. Files: scripts/prover_epNN_<topic>.py and output/prover_epNN_<topic>.mp4.
- Terminology (whole series): الشَّوْط = pass (one piston stroke D1 → D2), الجَوْلَة = run (the average of consecutive passes). Never use المرور for pass or الشوط for run.
- English terms in narration are written in Arabic letters for correct pronunciation: بْلِينَم (Plenum)، بُوبِت (Poppet)، كْرُونُومِتْرِي (Chronometry)، كُورْيُولِيس (Coriolis)، وُوتَر دْرُو (Waterdraw)، فْلُو بُوس (FloBoss)، إِنْفَار (Invar)، رُولُون (Rulon).
- After all 7 episodes are approved: concatenate them with ffmpeg into output/prover_full_series.mp4 with a short title card between episodes (no re-render of episodes).

### Research and verification (every episode)
- Before writing an episode's narration, research its topic on the web and verify every technical claim.
- Where the owner's outline is incomplete or says "likely/probably" (e.g. meaning of S600+ screen fields, STAB STATUS, CERTIFICATION DATE, report export options), complete it from reliable sources.
- Source priority: 1) manufacturer documents (Emerson/Daniel, Brodie, Micro Motion manuals and data sheets), 2) API MPMS chapters and official summaries, 3) technical papers (e.g. North Sea Flow Measurement Workshop), 4) reputable industry training material. Never use forums or unsourced blogs as the only source.
- Save sources for each episode in sources/prover_epNN.md: claim → source URL → short note.
- If sources conflict with each other or with the owner's outline, DO NOT decide silently: list the conflict in the approval message and ask the owner.
- If a fact cannot be verified, leave it out of the narration rather than guess.
- Never try to complete site-specific data (nameplate values, certificates, the open notes). These stay out of the videos.
- In the narration approval message, mark each sentence that was added or corrected from research with [+] and its source.
