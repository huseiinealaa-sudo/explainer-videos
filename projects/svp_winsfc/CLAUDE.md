# Project: svp_winsfc — Calibron Small Volume Prover and WinSFC for the SFC332P (single video)

Project-specific rules. The general rules in the root `CLAUDE.md` also apply; where they differ, this file wins for this project.

## Video
- One video, about 14:30: first half the prover (Honeywell Enraf Calibron SVP and its SVP Controller), second half WinSFC with the Dynamic Flow Computers SFC332P, then a short wrap-up.
- Script `projects/svp_winsfc/svp_winsfc_full.py` → `output/svp_winsfc_full.mp4` (build folder `tmp/svp_winsfc_full/`).
- A `section_title` names each half and the wrap-up before their first segment.

| # | Segment | Scenes | Target |
|---|---|---|---|
| 1 | What an SVP is, why "small volume", the system | title_card + concept_map | 55 s |
| 2 | Mechanical layout | labeled_diagram | 65 s |
| 3 | The six stages of a pass | stage_bar + line_chart | 60 s |
| 4 | Three devices, two signals, terminals 12–17 | concept_map + data_table | 55 s |
| 5 | Controller modes and the four error messages | comparison + data_table | 55 s |
| 6 | Double chronometry and the F, L, MF chain | equation + worked_calculation | 70 s |
| 7 | Maintenance, static leak test, water draw | timeline + checklist | 55 s |
| 8 | Where WinSFC sits, Online / Offline | concept_map + data_table | 50 s |
| 9 | Direction rule: Upload / Download, three steps | comparison + checklist | 55 s |
| 10 | Main window, safe and dangerous menus | labeled_diagram + comparison | 65 s |
| 11 | Prove Data screen | data_table | 65 s |
| 12 | Diagnostic screen, three mental checks | labeled_diagram + worked_calculation | 60 s |
| 13 | Status Input / Switch Output window | concept_map | 50 s |
| 14 | Proving sequence and the checklist before Prove Request | process_flow + checklist | 65 s |
| 15 | Troubleshooting along the sequence, golden rules | summary_box | 45 s |

## Source and verification
- Primary reference: `sources/svp_winsfc_source.md` (the owner's cleaned source, kept verbatim).
- Official sources first (priority 1): Honeywell Enraf *Small Volume Prover Installation, Operation & Service Manual* (models 35–120, part 44200001 Rev 3, and 05–25, part 44200002), Honeywell Enraf *SVP Controller Operation Manual* (44200004 Rev 2), Dynamic Flow Computers *SFC332PM Metric Operators Manual* (12/4/2025).
- Where the cleaned source differs from an official source, the narration follows the official source and the conflict is listed (claim, correction, source with page) in `sources/svp_winsfc_full.md`.
- Research only verifies: nothing is added except to correct an error or fill a gap the explanation needs.

## Privacy and screens (the repository is PUBLIC)
- No real site data, no screenshots. WinSFC windows are drawn simplified inside `labeled_diagram`.
- No Status Input / Switch Output assignment numbers are shown.
- All numbers come from `svp_winsfc_data.py` (illustrative inputs + values published in the manuals).

## Narration
- Arabic, ar-SA-HamedNeural, normal speed (`project.toml`); fully diacritized.
- Terminology: الشَّوْط = pass (one piston stroke D1 → D2); الجَوْلَة = run. In the example one run is one pass.
  أَعْلَى المَجْرَى / أَسْفَلَ المَجْرَى = upstream / downstream (as in the prover series).
- Foreign terms written in Arabic letters:
  | Term | Narration spelling |
  |---|---|
  | Prover | بُرُوفَر |
  | Poppet | بُوبِت |
  | Double chronometry | الكْرُونُومِتْرِي المُزْدَوِج |
  | Coriolis | كُورْيُولِيس |
  | Water Draw | وُوتَر دْرُو |
  | Run Permissive | رَن بِيرْمِيسِيف |
  | Volume Pulse | فُولْيُوم بَلْس |
  | Meter Calibration / Prover Test / Prover Calibration | مِيتَر كَالِيبْرِيشِن / بْرُوفَر تِسْت / بْرُوفَر كَالِيبْرِيشِن |
  | LAD | لَاد |
  | Modbus | مُودْبَاس |
  | WinSFC | وِين إِسْ إِفْ سِي |
  | Upload / Download | أَبْلُود / دَاوْنْلُود |
  | Online / Offline | أُونْلَايْن / أُوفْلَايْن |
  | Calibration / Override (menus) | كَالِيبْرِيشِن / أُوفَرْرَايْد |
  | Prove Data | بْرُوف دَاتَا |
  | Fail Code | فِيل كُود |
  | Status Input / Switch Output | سْتَاتَس إِنْبُت / سْوِتْش أَوْتْبُت |
  | K-factor | مُعَامِلُ كَيْ |

## Terminology and on-screen conventions
- On screen: English labels and equations only.
- Colours: ACCENT_1 = prover and fluid, ACCENT_2 = meter, pulses and the flow computer, ACCENT_3 = measurement / OK / safe, ACCENT_4 = alarm, error, dangerous action.

## Data
- All numbers come from `projects/svp_winsfc/svp_winsfc_data.py`, which runs `self_test()` on import.
- Illustrative inputs (owner, 2026-09-26): K = 60000 pulses/m³, BPV = 0.25000 m³ at 15 °C, Q = 200.0 m³/h, 5 runs to average / 5 total, limit 0.050 %, Tp 40.0 °C, Td 35.0 °C, Tm 38.0 °C, Ga 0.0000318, Gl 0.0000173, P 500.0 kPa, D 600.0 mm, t 7.0 mm, E 193000000 kPa, CTPLp 0.97820, CTPLm 0.97990, run pulses 14976.40 / 14977.90 / 14975.10 / 14977.20 / 14975.40, Pt100 115.54 Ω, suspect density 700.0 kg/m³.

## Owner decisions
- 2026-09-26: project created; single video `svp_winsfc_full`; outline and scene plan above.
