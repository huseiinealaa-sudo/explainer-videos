# ut_series_ep01_principle: Production Progress

## Build Log

| Segment | Built by | Calls | Automatic loop | Critic |
|---------|----------|-------|----------------|--------|
| seg 1 (§1) | scene-builder | 1 | it1 0 → it2 2 → it3 0 | round 1 improvements only; round 2 PASS |
| seg 2 (§2) | scene-builder | 4 (one cut off by an API limit and repeated) | it1 2 → it2 crash fixed → it3 0; later fixes 1 → 0 | round 1 FIX (improvements #5, #9, #10) → round 2 improvement #1 (baseline) fixed |
| seg 3 (§3) | scene-builder (2), manager (1 edit) | 3 | it1 1 → it2 0 | round 1 improvement #2 fixed; the 6b improvement (transverse panel starts at its cue) done by the manager |
| seg 4 (§4) | scene-builder | 2 | it1 3 → it2 1 → it3 0 | round 1 improvements #3, #4 fixed |
| seg 5 (§5) | scene-builder | 3 | it1 6 → it2 1 → it3 0 | round 1 critical #1 (gauge reading touching its display) fixed; round 2 improvements #2, #3, #4 fixed |
| seg 6 (§6) | scene-builder | 3 | it1 1 → it2 0 | round 1 improvement #7 fixed; round 2 improvements #5, #6a fixed |
| seg 7–31 (review) | scene-builder | 2 | it1 3 → it2 0 | round 1 improvement #6 fixed |

Whole-video automatic runs (manager): 3, each 0 critical in all 31 narration entries (the last one also 0 improvements).
Critic: round 1 FIX (1 critical, 0 important, 10 improvements); round 2 PASS (0 critical, 0 important, 6 improvements, 5.5 of them applied: 1, 2, 3, 4, 5, 6a, and 6b by the manager). No third round (owner decision: round 2 passed, what came after was layout and timing only).

## Episode

- **Duration:** 6:33.10 (content 4:46.3 + review 1:46.8), final 1080p
- **Size:** 21.18 MiB (22,204,131 bytes)
- **Git hash of the video:** cd08dc9be34a (checked by the manager with `git hash-object`; before this render: 6bce50ccd561; first render: cab18b933bd1)

## Owner reviews (2026-10-02)

1. **Pulse shape.** The zig-zag pulse was replaced by wave-front arcs (`projects/ut_series/ut_visuals.py`, function `wavefront`, shared by episodes 2-4): three arcs, convex in the direction of travel, the front one the widest and strongest. Used for every pulse and echo in segments 1, 2 (the two horizontal pulses), 4, 5, 6 and the review; the sine wave with the lambda bracket, the particle chains, the longitudinal/transverse panels and the A-scan are unchanged. The segment 4 board "Three consequences" was re-centred. A scan of every frame found no ink touching the frame edges (no clipping).
2. **Concepts instead of equations** (new permanent rule in the Quality standard: an equation only if the technician uses it; one step-by-step worked example per episode; other numbers as visual results). Segments 2, 3, 4, 5 and the review were rewritten: no lambda equation or values (segment 2), no speed numbers (segment 3), no Z or R formula and no impedance values (segment 4, bars 88 % and about 100 %), only d = v t / 2 with the 12 mm flaw as a worked example (segment 5; the back-wall time and the aluminium steps removed, the gauge shows 26.7 mm), review Q2/Q3/Q6 changed. Narration of those segments re-synthesised; content 5:19 -> 4:46. Everything done by the manager (no sub-agents except the critic), per the owner's instruction.
3. **Critic round 3** (changed segments only): FIX with 1 critical, 2 important, 6 improvements; fixed by the manager (the back-wall echo arc touching the "Couplant" tag, the "about half" and steel/air results held longer, one-baseline example rows, Q3 lane updaters, the storyboard cue map rewritten). No fourth round; the automatic loop was re-run on the whole video: 0 critical, 0 improvements. Open after round 3: one improvement noted by the critic and left (the attenuation pulse at 0:21 squeezed to 0.25 width shows narrow U shapes; it still reads as weakening).

---

# ut_series_ep02_probe_beam and ut_series_ep03_calibration: Production Progress

Started 2026-10-04 09:32:56 UTC (PR opened at the time stated in the pull request). Built entirely by the manager (the main session): no `scene-builder` and no `render-runner` call. Haiku agents (`general-purpose`, 21 calls in total for both episodes) ran only mechanical work: previews with `--qa`, digests of the overlap reports, contact sheets. The critic (`video-critic`, opus) was called 6 times: 3 rounds per episode. The final renders were run by the manager with `python -m explainer.final_render`.

## Build Log

| Segment | Built by | Calls | Automatic loop | Critic |
|---------|----------|-------|----------------|--------|
| ep2 seg 1–6 (content) | manager | 0 agents | about 8 segment-level runs and 6 whole-video runs; last whole-video run 0 critical, 0 improvements | round 1 FIX; round 2 FIX (2 important, fixed); round 3 FIX (1 critical: angle probe fired backwards; fixed after the round, not re-reviewed) |
| ep2 seg 7–31 (review) | manager | 0 agents | same runs | not in the critic's scope after round 1 |
| ep3 seg 1–6 (content) | manager | 0 agents | about 6 segment-level runs and 5 whole-video runs; last whole-video run 0 critical, 0 improvements | round 1 FIX; round 2 FIX (2 critical, 1 important, fixed); round 3 PASS (5 improvements left) |
| ep3 seg 7–31 (review) | manager | 0 agents | same runs | cards 1 and 5 re-checked in rounds 2 and 3 |

## Episodes

| Episode | Duration | Content / review | Size | Git hash |
|---|---|---|---|---|
| ep2 `ut_series_ep02_probe_beam` | 6:24.00 | 4:31.5 / 1:52.5 | 14.15 MiB (14,837,293 bytes) | c5461bb3e973 (no file before; checked by the manager with `git hash-object`) |
| ep3 `ut_series_ep03_calibration` | 6:41.30 | 4:49.7 / 1:51.6 | 14.17 MiB (14,858,141 bytes) | ae0a9110d285 (no file before; checked by the manager) |

Final renders: 1 per episode, 1920x1080, RENDER_OK.

---

# ut_series_ep04_weld_evaluation: Production Progress

Started 2026-10-10 21:26:08 UTC (PR opened at the time stated in the pull request). Built entirely by the manager (the main session): no `scene-builder` and no `render-runner` call. Haiku agents (`general-purpose`, model haiku) ran only mechanical work: previews with `--qa`, digests of the overlap reports, contact sheets; the critic (`video-critic`) was called by the manager. Environment: Python 3.13, manim 0.22.0 in the virtual environment of the root `CLAUDE.md`.

## Build Log

| Segment | Built by | Calls | Automatic loop | Critic |
|---------|----------|-------|----------------|--------|
| (filled in at the end of production) | | | | |

