# takeoff_lift: Production Progress

## Build Log

| Segment | Built by | Calls | Automatic loop | Critic |
|---------|----------|-------|----------------|--------|
| seg 1 (3D) | scene-builder | 1 | it1 44 → it2 12 → it3 11 (all 11 judged 3D artefacts: world x-y of 3D shapes; checked on sheets) | — |
| seg 2 | scene-builder | 1 | it1 (1-2 run) 4 own critical → it2 0 | — |
| seg 3 | scene-builder | 1 | it1 12 → it2 1 → it3 0 | — |
| seg 4 | scene-builder | 2 (call 1 stopped by the auto-mode classifier before any preview; code kept) | it1 0 → it2 1 → it3 0 | — |
| seg 5 (3D) | scene-builder | 1 | it1 79 → it2 144 → it3 144 → it4 144 (all 3D artefacts: world x-y of runway, shadow and lift-arrow polygons; checked on sheets) | — |
| seg 6 | scene-builder | 1 | it1 (5-6 run) 1 → it2 0 → it3 0 | — |
| seg 7 | scene-builder | 1 | it1 0 → it2 0 → it3 0 (one 0.60 s sync warning: summary_box heading and frame before the first cue) | — |

## Manager notes
- Seg 2: cue `c("الدَّفْعُ")` finds the first occurrence (inside «وَالدَّفْعُ»), so the caption "Thrust > Drag" is 7.88 s early relative to «يَكُونُ الدَّفْعُ»; found by the "late" warning, fixed by the manager with nth=2 (commit 0303486); the 42.45 s warning is gone in the segment 4 run.
