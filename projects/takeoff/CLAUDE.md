# Project: takeoff — How does an airplane take off? Lift and takeoff speeds (single video)

Project-specific rules. The general rules in the root `CLAUDE.md` also apply; where they differ, this file wins for this project.
First episode outside the industrial field: it is also a test of what the template lacks (the PR carries a gap report).

## Video
- One episode, target 4:30–4:50, hard maximum 5:00; seven segments; storyboard in `storyboard/takeoff_lift.md`.
- Script `projects/takeoff/takeoff_lift.py` → `output/takeoff_lift.mp4` (build folder `tmp/takeoff_lift/`).
- Segments 1 and 5 are 3D in Manim (`ThreeDScene`): a simple, elegant airliner built from basic shapes, a runway, slow camera moves. The other segments are 2D. No Blender or other external 3D tool.
- The scene class is `TakeoffLift(SyncedScene, ThreeDScene)`; 2D segments use the default top-down camera, 3D segments restore it when they end. Texts in 3D segments are fixed in frame.
- If the overlap checker cannot judge a 3D segment, its contact sheets and the critic are the check (reported in the PR gap report).

## Source and verification
- Primary reference: `sources/takeoff_source.md` (the owner's cleaned source, kept verbatim).
- Official sources (priority 1): FAA PHAK FAA-H-8083-25C (aerodynamics chapters), 14 CFR 1.2 (V1, VR, V2), FAA AFH FAA-H-8083-3C; the equal-transit myth: NASA Glenn Research Center. Notes in `sources/takeoff_lift.md`.
- Where the cleaned source differs from an official source, the narration follows the official source and the correction is listed (claim, correction, source with page).
- Research only verifies: nothing is added except to correct an error or fill a gap the explanation needs.

## Narration
- Arabic, ar-SA-HamedNeural, normal speed (`project.toml`); fully diacritized. Decimals are read with «فَاصِلَة».
- Foreign terms written in Arabic letters:
  | Term | Narration spelling |
  |---|---|
  | V1 | فِي وَنْ |
  | VR | فِي آرْ |
  | V2 | فِي تُو |
  | stall | السْتُول |
  | Newton | نْيُوتِن |
  | Bernoulli | بِرْنُولِّي |
  | N (newton) | نْيُوتِن |
- Terminology: الرَّفْع = lift; الوَزْن = weight; الدَّفْع = thrust; السَّحْب = drag; زَاوِيَةُ الهُجُوم = angle of attack; الوَتَر = chord; الهَوَاءُ النِّسْبِيّ = relative wind; القَلَّابَات = flaps; الانْهِيَار = stall; سُرْعَةُ القَرَار = V1; سُرْعَةُ الدَّوَرَان = VR; سُرْعَةُ الأَمَانِ فِي الإِقْلَاع = V2; مَسَافَةُ التَّسَارُعِ وَالتَّوَقُّف = accelerate-stop distance.

## Terminology and on-screen conventions
- On screen: English labels and equations only. The aircraft is generic: no type, airline, logo or registration.
- Colours: ACCENT_1 blue = lift and airflow; ACCENT_2 orange = thrust / engines / the pilot's action; ACCENT_3 green = continue / OK; ACCENT_4 red = weight, drag, reject, stall, the myth. GREY_INK = runway, ground, chord line.
- Speeds relative to the air are "airspeed"; relative to the ground "ground speed".

## Data
- All numbers come from `projects/takeoff/takeoff_data.py`, which runs `self_test()` on import.
- Illustrative inputs:
  | Item | Value |
  |---|---|
  | Mass | 70 000 kg |
  | g | 9.81 m/s² |
  | Wing area S | 120 m² |
  | C_L with takeoff flaps | 1.6 |
  | ρ at 15 °C | 1.225 kg/m³ |
  | p0, R_air, T_hot | 101 325 Pa, 287.05 J/(kg·K), 318.15 K (45 °C) |
  | Headwind | 10 m/s |
  | Weight increase | 10 % |

## Owner decisions
- 2026-09-30: project created; single episode (target 4:30–4:50, max 5:00); segments 1 and 5 in 3D; left out for later episodes: landing, jet engines, flight controls, engine failure in detail.
