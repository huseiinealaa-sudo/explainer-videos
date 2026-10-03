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
