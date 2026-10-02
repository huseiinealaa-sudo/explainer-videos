# Project: ut_series — Ultrasonic testing (UT) (4 episodes)

Project-specific rules. The general rules in the root `CLAUDE.md` also apply; where they differ, this file wins for this project.
(`projects/ut_intro` is an older, separate project: do not touch it.)

## Series
Four episodes, 3–5 minutes each without the review segment, about 17 minutes in total. Every episode ends with a review segment (question, 3-second countdown, answer).
| # | Episode | Source sections (IAEA-TCS-67) | Status |
|---|---|---|---|
| 1 | The principle | §1.1.2.6 (p. 9), ch. 2 (pp. 99–132), §3.1 (pp. 133–136) | narration for approval |
| 2 | The probe and the beam | — | not started |
| 3 | Calibration and angle-beam testing | — | not started |
| 4 | Flaw evaluation and the report, with a glance at PAUT and TOFD | — | not started |
Only episode 1 is produced in the first session; the others wait for the owner's approval of its level.

## Theme
- `project.toml` → `[style] theme`: chosen here **light** (the white board), 1080p (`[render] resolution`). Colours in scripts are the theme names (`INK`, `ACCENT_1` …), never literals.

## Source
- Official reference (priority 1): IAEA-TCS-67, *Training Guidelines in Non-destructive Testing Techniques: Manual for Ultrasonic Testing at Level 2*, IAEA 2017, free at https://www-pub.iaea.org/MTCD/Publications/PDF/TCS-67web.pdf (printed page = PDF page − 13). Supporting source: IAEA-TCS-10 (1999), not reachable from the container.
- Primary reference for the content: `projects/ut_series/sources/ut_series_source.md` (cleaned; verbatim as the owner supplied it; the corrections found by verification are in the research notes below and are applied in the narration).
- Research notes per video: `projects/ut_series/sources/ut_series_<video>.md` (claim → source → note).

## Narration
- Language / voice / speed: see `project.toml` (Arabic, ar-SA-HamedNeural, normal speed).
- Decimals are spoken digit by digit after «فَاصِلَةٌ» (1.184 → «وَاحِدٌ فَاصِلَةٌ وَاحِدٌ ثَمَانِيَةٌ أَرْبَعَةٌ»).
- On-screen text is English (the question text in the review too); the narration is Arabic.
- Foreign terms written in the narration's letters:
  | Term | Narration spelling |
  |---|---|
  | Hz / kHz / MHz | هِرْتْز / كِيلُوهِرْتْز / مِيغَاهِرْتْز |
  | Rayl / MRayl | رَايْل / مِيغَارَايْل |
  | A-scan | إِيهْ سْكَانْ |
  | Lamb (wave) | لَامْبْ |
  | µs | مِيكْرُوثَانِيَةٍ |
  | mm | مِلِّيمِتْرٍ |
  | aluminium | الأَلُمْنْيُومِ |

## Videos
| # | Script / output | Topic | Status |
|---|---|---|---|
| 1 | `ut_series_ep01_principle` | The principle of ultrasonic testing | narration for approval |

## Terminology and on-screen conventions
- probe = المجس; couplant = الوسيط; pulse-echo = النبضة والصدى; through-transmission = النفاذ; resonance = الرنين; attenuation = التوهين; acoustic impedance = المعاوقة الصوتية.
- Colours: ACCENT_1 = sound wave / probe / incident wave, ACCENT_2 = reflected wave / echo, ACCENT_3 = transmitted wave / OK, ACCENT_4 = flaw / alarm.
- Illustrative values only; no site, personal or confidential data.

## Data
- All numbers come from `projects/ut_series/ut_series_data.py`, which runs `self_test()` on import (python projects/ut_series/ut_series_data.py prints the table).
- Inputs (the owner's values; TCS-67 Table 2.1, p. 104, differs slightly on three of them, see `TCS67_ALTERNATIVES` and the episode-1 research notes):
  | Item | Value |
  |---|---|
  | longitudinal velocity, steel | 5920 m/s (TCS-67: "steel, calibration block") |
  | shear velocity, steel | 3240 m/s (TCS-67: 3250) |
  | velocity, water / air / aluminium (L) | 1480 / 343 / 6320 m/s (air in TCS-67: 330) |
  | density steel / water / air | 7850 / 1000 / 1.2 kg/m³ (air in TCS-67: 1.3) |
  | probe frequency, plate thickness, flaw depth | 5 MHz, 25 mm, 12 mm |

## Owner decisions
- 2026-10-02: new project `ut_series`, 4 episodes; this session produces episode 1 only; theme light, 1080p.
- 2026-10-02: tool fix allowed in this session: the light theme's `faint` and `accent2` raised to 4.5:1 contrast (may change old projects when they are re-rendered).
- 2026-10-02: the two known failing tests (`test_seg3_tag_touching_the_rays_is_found`, the `small round badge '10'` case) are not fixed here.
