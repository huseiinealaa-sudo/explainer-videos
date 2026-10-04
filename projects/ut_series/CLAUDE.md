# Project: ut_series — Ultrasonic testing (UT) (4 episodes)

Project-specific rules. The general rules in the root `CLAUDE.md` also apply; where they differ, this file wins for this project.
(`projects/ut_intro` is an older, separate project: do not touch it.)

## Series
Four episodes, 3–5 minutes each without the review segment, about 17 minutes in total. Every episode ends with a review segment (question, 3-second countdown, answer).
| # | Episode | Source sections (IAEA-TCS-67) | Status |
|---|---|---|---|
| 1 | The principle | §1.1.2.6 (p. 9), ch. 2 (pp. 99–132), §3.1 (pp. 133–136) | narration for approval |
| 2 | The probe and the beam | §2.6 (pp. 118–122), §3.2 (pp. 137–149), §3.3.4 (p. 153), §2.5 (pp. 124–131), §2.8 (pp. 128–131) | produced; waits for the owner's review |
| 3 | Calibration and angle-beam testing | §2.4.2 (pp. 112–115), §5.1–5.8 (pp. 178–202), §6 (p. 215), §8.4.1 (pp. 278–279) | produced; waits for the owner's review |
| 4 | Flaw evaluation and the report, with a glance at PAUT and TOFD | — | not started |
Episode 1 was produced first and approved; episodes 2 and 3 were produced after the owner's approval of the narration; episode 4 waits.

## Theme
- `project.toml` → `[style] theme`: chosen here **light** (the white board), 1080p (`[render] resolution`). Colours in scripts are the theme names (`INK`, `ACCENT_1` …), never literals.

## Source
- Official reference (priority 1): IAEA-TCS-67, *Training Guidelines in Non-destructive Testing Techniques: Manual for Ultrasonic Testing at Level 2*, IAEA 2017, free at https://www-pub.iaea.org/MTCD/Publications/PDF/TCS-67web.pdf (printed page = PDF page − 13). Supporting source: IAEA-TCS-10 (1999), not reachable from the container.
- Primary reference for the content: `projects/ut_series/sources/ut_series_source.md`: the owner's cleaned text with the verification corrections merged in, each marked [+] with its TCS-67 section and page. It is the approved reference for episodes 2–4. Items moved to a later episode are under «مرحّل إلى الحلقة 3».
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
| 1 | `ut_series_ep01_principle` | The principle of ultrasonic testing | approved model (merged) |
| 2 | `ut_series_ep02_probe_beam` | The probe and the beam | produced, 6:24 (content 4:31 + review 1:52) |
| 3 | `ut_series_ep03_calibration` | Calibration and angle-beam testing | produced, 6:41 (content 4:50 + review 1:52) |

## Terminology and on-screen conventions
- probe = المجس; couplant = الوسيط; pulse-echo = النبضة والصدى; through-transmission = النفاذ; resonance = الرنين; attenuation = التوهين; acoustic impedance = المعاوقة الصوتية.
- Colours: ACCENT_1 = sound wave / probe / incident wave, ACCENT_2 = reflected wave / echo, ACCENT_3 = transmitted wave / OK, ACCENT_4 = flaw / alarm.
- Illustrative values only; no site, personal or confidential data.

## Data
- All numbers come from `projects/ut_series/ut_series_data.py`, which runs `self_test()` on import (python projects/ut_series/ut_series_data.py prints the table).
- Inputs: all from IAEA-TCS-67 Table 2.1 (p. 104), owner decision 2026-10-02:
  | Item | Value |
  |---|---|
  | longitudinal velocity, steel | 5920 m/s (row "steel (calibration block)") |
  | shear velocity, steel | 3250 m/s |
  | velocity, water / air / aluminium (L) | 1480 / 330 / 6320 m/s |
  | density steel / water / air | 7850 / 1000 / 1.3 kg/m³ |
  | probe frequency, plate thickness, flaw depth | 5 MHz, 25 mm, 12 mm |
  Derived (computed in the module): Z air 429 Rayl, R steel–air 0.999963 (99.996 %), shear ratio 0.549 (about 0.55).

## Owner decisions
- 2026-10-02: new project `ut_series`, 4 episodes; this session produces episode 1 only; theme light, 1080p.
- 2026-10-02: tool fix allowed in this session: the light theme's `faint` and `accent2` raised to 4.5:1 contrast (may change old projects when they are re-rendered).
- 2026-10-02: the two known failing tests (`test_seg3_tag_touching_the_rays_is_found`, the `small round badge '10'` case) are not fixed here.
- 2026-10-02: approved the episode-1 narration with changes: TCS-67 values for the shear and air figures; the R formula spoken as the square of the quotient and drawn with its brackets; the full calibration sentence in segment 5; all advantages and limits spoken in segment 1 (no grey chips) with the material-properties sentence; 4:53 accepted; multiple echoes and t = v ÷ 2f moved to episode 3; review questions in English on screen and Arabic in the voice; the corrections merged into the source file; `CLAUDE.md` line 161 corrected.
