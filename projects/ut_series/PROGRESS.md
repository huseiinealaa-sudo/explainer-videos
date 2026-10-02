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

- **Duration:** 7:03.20 (content 5:18.8 + review 1:44.4), final 1080p
- **Size:** 21.98 MiB (23,045,927 bytes)
- **Git hash of the video:** 6bce50ccd561 (checked by the manager with `git hash-object`; before: cab18b933bd1)

## Owner review of the first render (2026-10-02)

The owner replaced the zig-zag pulse with wave-front arcs (`projects/ut_series/ut_visuals.py`, function `wavefront`, shared by episodes 2-4): three arcs, convex in the direction of travel, the front one the widest and strongest. It is used for every pulse and echo in segments 1, 2 (the two horizontal pulses), 4, 5, 6 and the review; the sine wave with the lambda bracket, the particle chains, the longitudinal/transverse panels and the A-scan are unchanged. The segment 4 board "Three consequences" was re-centred (left and right margins 0.62 units). Re-render: affected segments 1, 2, 4, 5, 6 and 7-31 re-checked by the automatic loop (0 critical), then the whole video (0 critical, 0 improvements). No third critic round (the change is in the drawing, not in the content). A scan of 1693 frames of the video found no ink touching the frame edges.
Stills sent for approval before the re-render: `projects/ut_series/frames/`.
