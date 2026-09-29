# Project: pt_cal — Calibrating pressure transmitters with the Beamex MC6 (7 episodes)

Part 1 of the refinery transmitter-calibration series. Project-specific rules; the general rules in
the root `CLAUDE.md` also apply, and where they differ this file wins for this project.

## Source and verification
- Primary reference: `sources/pt_cal_source.md` — the owner's cleaned text kept verbatim, plus the
  section completed from the official manuals (hydraulic hand pump, pneumatic pumps; every line [+]
  with manual and page).
- Research notes per episode: `sources/pt_cal_ep0N_<name>.md` (claim → source → page → result).
- Official sources first (priority 1), by part:
  - Calibrator, pressure modules, pumps: Beamex Oy Ab (Finland) — MC6 User Manual, MC6 brochure,
    PG pump manuals (PGL, PGV, PGM, PGC, PGPH, PGHH, PGXH, PGHS), ePG manual/brochure, POC8 brochure
    (beamex.com/manuals-and-brochures and the product pages). Manuals are NOT stored in the repo.
  - Transmitter and manifold (no specific maker): terms (zero trim, sensor trim, D/A trim, rerange)
    and the manifold sequence from the Rosemount 3051 Reference Manual 00809-0100-4001 (Emerson);
    the transmitter is always drawn generic, without a brand.
  - Uncertainty: JCGM 100:2008 (GUM); certificate elements per ISO/IEC 17025 principles.
  - H₂S: OSHA official pages.
  - Priority 2: Beamex blog (adiabatic process, square-root transmitter, hysteresis).
- Where the owner's text differs from an official source, the narration follows the official source
  and the correction is listed (claim, correction, source, page) in the episode's research notes.

## Narration
- Arabic, ar-SA-HamedNeural, normal speed (`project.toml`); fully diacritized.
- Decimals are spoken with «فَاصِلَة» (never «أَعْشَار» or «عُشْرَيْن», which can be heard as whole numbers).
- Every episode opens with the one-sentence educational-material notice (each episode stands alone).
- Foreign terms written in Arabic letters:
  | Term | Narration spelling |
  |---|---|
  | Beamex | بِيمِكْس |
  | MC6 / MC5 | إِمْ سِي سِكْس / إِمْ سِي فَايْف |
  | MC6-Ex / -WS / -T | إِمْ سِي سِكْس إِكْس / دَبْلْيُو إِس / تِي |
  | HART, Fieldbus, Profibus | هَارْت، فِيلْدْبَاس، بْرُوفِيبَاس |
  | PGL PGV PGM PGC PGPH | بِي جِي إِلْ، بِي جِي فِي، بِي جِي إِمْ، بِي جِي سِي، بِي جِي بِي إِتْش |
  | PGHH PGXH PGHS | بِي جِي إِتْش إِتْش، بِي جِي إِكْس إِتْش، بِي جِي إِتْش إِس |
  | ePG, POC8, CENTRiCAL | إِي بِي جِي، بِي أُو سِي ثَمَانِيَة، سِنْتْرِيكَال |
  | CMX, LOGiCAL | سِي إِمْ إِكْس، لُوجِيكَال |
  | As-Found / As-Left | آزْ فَاوْنْد / آزْ لِفْت |
  | TUR, GUM | تِي يُو آر، جِي يُو إِمْ |
  | PT-101 | بِي تِي مِئَةٌ وَوَاحِد |
  | Excel | إِكْسِل |
  | mA, V, Ω, bar | مِلِّي أَمْبِير، فُولْت، أُوم، بَار |
- Terminology: مُرْسِل = transmitter; مُعَايِر = calibrator; وَحْدَةُ الضَّغْطِ = pressure module;
  مُعَدِّلُ الحَجْمِ = fine adjust (volume adjuster); صِمَامُ التَّنْفِيسِ = vent valve;
  مُحَدِّدُ الشَّوْطِ = stroke selector; صِمَامُ المُعَادَلَةِ = equalize valve; التَّفَاوُتُ = tolerance;
  عَدَمُ التَّأَكُّدِ = uncertainty; الضَّبْطُ = trim; تَغْيِيرُ المَدَى = re-ranging.

## Videos
| # | Script / output | Topic | Status |
|---|---|---|---|
| 1 | `pt_cal_ep01_device` | the MC6, electrical side, pressure modules, modes | rendered 1080p (4:21, 9.0 MB), critic PASS round 2 |
| 2 | `pt_cal_ep02_pressure` | generating pressure; hydraulic hand pump (model episode) | rendered 1080p (5:30), critic PASS round 3; level approved by the owner |
| 3 | `pt_cal_ep03_setup` | transmitter types, connections, 3-valve manifold, safety | narration approved |
| 4 | `pt_cal_ep04_procedure` | ten steps, approach rule, pressure decay | narration approved |
| 5 | `pt_cal_ep05_verdict` | calculation, verdict, certificate, interval | rendered 1080p (3:45, 9.0 MB), critic PASS round 2 |
| 6 | `pt_cal_ep06_trim` | four operations, trims and their order, when to trim, error patterns | rendered 1080p (3:01, 7.8 MB), critic PASS round 2 |
| 7 | `pt_cal_ep07_uncertainty` | error vs uncertainty, budget, TUR, guard band | narration approved |
| — | `pt_cal_full_series` | the seven episodes joined with title cards | after approval |

Storyboards: `storyboard/pt_cal_ep0N_<name>.md` (with the narration).

## Terminology and on-screen conventions
- On screen: English labels, model names as text, equations from `Text` pieces. No product photos,
  no logos, no screenshots: the calibrator, pumps and manifold are simplified custom drawings; the
  transmitter is generic (ISA bubble PT-101 where a tag is needed); ISA 5.1 symbols and Tabler icons
  from the library where they fit.
- The only tag used in examples is PT-101.
- Units: kg/cm² for the transmitter (owner's convention), bar for pumps and modules.
- Colours: ACCENT_1 blue = pressure / input / fluid; ACCENT_2 orange = generated signal, output,
  moving parts, heat; ACCENT_3 green = correct / PASS; ACCENT_4 red = danger, error, leak, FAIL.

## Data
- All numbers come from `pt_cal_data.py`, which runs `self_test()` on import; derived values are
  computed at full precision and rounded only for display.
- Illustrative inputs:
  | Item | Value |
  |---|---|
  | Transmitter | PT-101, 0–42 kg/cm², 4–20 mA, tolerance ±0.50 % of span |
  | Point example | nominal 42.000, actual 41.928 kg/cm², measured 20.0320 mA |
  | Budget (kg/cm²) | ref a 0.0153, current a 0.0130, resolution d 0.0010, repeatability s 0.0080, temperature a 0.0050, stability a 0.0100, k = 2 |
  | Error pattern | +0.37, +0.22, +0.03, −0.14, −0.30 % at 0/25/50/75/100 % |
  | Decay curves | from 42 kg/cm², 180 s at 1 s: thermal 0.30 (τ 30 s), leak 0.10 /min, mixed 0.20 (τ 25 s) + 0.05 /min |
- Published values (pump ranges, hose ratings, MC6 limits, module specs) are typed once in the data
  module with their source in the research notes.

## Owner decisions
- 2026-09-28: project created; 6 episodes, ~25 min; episode 2 is the model episode; out of this part:
  temperature (unit 4, ET terminals, cold-junction compensation, thermal mass, MC6-T).
- 2026-09-28 (narration approval): episode 5 split in two → 7 episodes (ep05 verdict, ep06 trim,
  ep07 uncertainty); module example EXT60 vs EXT600 approved; MC5 described only as the older
  generation (no "monochrome/keypad"); manifold sequence per the Rosemount 3051 Reference Manual;
  decimals spoken with «فاصلة», never «أعشار / عُشْرَين» (e.g. 7.2 = سَبْعَةٌ فَاصِلَةُ اثْنَيْنِ).
