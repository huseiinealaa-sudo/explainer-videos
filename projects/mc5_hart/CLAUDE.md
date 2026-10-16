# Project: mc5_hart — Calibrating smart pressure transmitters with the Beamex MC5 over HART (3 episodes)

Project-specific rules. The general rules in the root `CLAUDE.md` also apply; where they differ, this file wins for this project.

## Scope (owner decision)
The videos are about the **options inside the calibrator and its screens only**. They do not explain the transmitter or its nameplate, the MC5 ports, the wiring, and there is no separate safety section (the field safety steps appear only where the manual's warning belongs, episode 2).

## Series
Three episodes, 5–6 minutes each, about 17 minutes in total, produced in this order. Episode 1 is produced first and waits for the owner's approval of its level before episodes 2–3.
| # | Episode | Source sections | Status |
|---|---|---|---|
| 1 | MC5 + HART: Connect & Configure | 1.1–1.6 | narration approved |
| 2 | Trim Instrument: AO vs PV | 2.1–2.6 | narration approved |
| 3 | Calibration Mode: As Found / As Left | 3.1–3.7 | narration approved |

## Theme
- `project.toml` → `[style] theme = "light"` (the white board, owner decision), 1080p. Colours in scripts are the theme names (`INK`, `ACCENT_1` …), never literals.

## Source
- Official references (priority 1): [1] *User Guide for MC5 HART Option* (Appendix 1, printed pp. 136–149; Main Firmware 1.90) https://www.beamex.com/app/uploads/2022/11/beamex-mc5-hart-option-manual-eng.pdf — printed page = PDF page + 131. [2] *MC5 User Guide* https://www.beamex.com/app/uploads/2016/10/MC5_User_Guide.pdf — printed page = PDF page − 8. [3] *MC5-IS User Manual* https://www.manualslib.com/manual/1343176/Beamex-Mc5-Is.html (readable with WebFetch; direct downloads are blocked by Cloudflare).
- Primary reference for the content: `projects/mc5_hart/sources/mc5_hart_source.md` (the owner's refined text, kept as given).
- Verification notes and corrections: `projects/mc5_hart/sources/mc5_hart_verification.md` (claim → source → page → result).
- The manuals describe firmware 1.90 (screens of 2000–2002). The owner's refined text also follows screens of a newer device; where the two differ, the difference is listed for the owner and not decided here.

## Narration
- Language / voice / speed: see `project.toml` (Arabic, ar-SA-HamedNeural, normal speed). Fully diacritized.
- Terms (owner decision 2026-10-16): «الدَّخْل» for input (never «الدخول» in that sense), «الوَسْم» for Tag, no number chains in the voice (numbers stay on the screen, the voice says the meaning).
- Decimals are spoken digit by digit after «فَاصِلَةٌ»; rounded figures are spoken in words («نَحْوُ سَالِبِ أَرْبَعَةِ أَعْشَارٍ بِالمِئَةِ»).
- On-screen text is English (menu names exactly as the MC5 shows them); the narration names the menu items in Arabic and spells foreign terms in Arabic letters.
- Foreign terms written in the narration's letters:
  | Term | Narration spelling |
  |---|---|
  | MC5 | إِمْ سِي فايْف |
  | Beamex | بِيمِكْس |
  | HART | هارْت |
  | Trim | تْرِمْ |
  | Fetch | فِتْش |
  | Send | سِنْد |
  | As Found | آز فاونْد |
  | As Left | آز لِفْت |
  | PV | بِي فِي |
  | AO | إِيهْ أُو |
  | Multidrop | مَلْتِي دْرُوبْ |
  | Burst | بِيرْسْت |
  | Edit / Enter / Restart | إِدِيت / إِنْتَر / رِيسْتَارْت |
  | End HART Adjustment | إِنْد هارْت أَدْجَسْتْمِنْت |
  | NAMUR NE 43 | نَامُور إِنْ إِي ثَلَاثَةٍ وَأَرْبَعِينَ |
  | mA | مِلِّي أَمْبِيرٍ |
  | kgf/cm² | كِيلُوغْرَامًا لِكُلِّ سَنْتِيمِتْرٍ مُرَبَّعٍ |
  | keys A B C D | إِيه، بِي، سِي، دِي |
  | Port E | المَنْفَذُ إِي |

## Videos
| # | Script / output | Topic | Status |
|---|---|---|---|
| 1 | `mc5_hart_ep01_connect` | Connect and configure | narration approved |
| 2 | `mc5_hart_ep02_trim` | Trim Instrument, AO vs PV | narration approved |
| 3 | `mc5_hart_ep03_calibration` | Calibration Mode, As Found / As Left | narration approved |
| — | `mc5_hart_full_series` | the three episodes joined with title cards | `output/mc5_hart_full.mp4` |

## The MC5 screen (`mc5_visuals.py`)
- One reusable component, `MC5`, draws the screen only: status bar, two windows or the three-part calibration layout (Input / Output / Error graph), a numbered side menu with an inverted cursor, pop-ups, the soft key row and the A B C D keys with a press motion. A monospaced LCD look, no logo and no brand name. The look was fixed by one still frame (`storyboard/mc5_screen_frame.png`) before any render.
- A menu item the video does not name is drawn as a faint bar, never as invented text. Editable values are ACCENT_1. The status bar always carries «Illustrative».
- Look and keys follow the manuals: soft key labels at the bottom of the screen, function keys A–D below it (the manual also numbers them 1–4: «4/Select» = D/Select; «2/Edit» = B/Edit), numeric keys 1–7 select menu items, Enter or D/OK finishes a number.

## Terminology and on-screen conventions
- PV = the digital output (the sensor reading as HART reports it); AO = the analog 4–20 mA output; Trim = the transmitter adjustment; rerange = changing LRV/URV (not a calibration).
- Colours: ACCENT_1 = editable value / selected key / the transmitter side, ACCENT_2 = the measured value and the error dots, ACCENT_3 = pass / OK, ACCENT_4 = fail / alarm.
- Illustrative values only; no site, personal or confidential data, no screenshots.

## Data
- All numbers come from `projects/mc5_hart/mc5_hart_data.py`, which runs `self_test()` on import (`python projects/mc5_hart/mc5_hart_data.py` prints the tables).
- Inputs (all illustrative): unit kgf/cm²; LRV 0, URV 40, span 40; URL 50.00, LRL 0.00, minimum span 0.50; Tag PT-101, Device ID 12345678, serial 1234567; damping 0.40 s, Linear, Burst Off, polling address 0; rerange URV 40 → 30 at 15 kgf/cm² (10.000 → 12.000 mA); AO check 3.8→3.8002, 4→4.0003, 12→12.0010, 20→20.0016, 20.5→20.5017 mA; sensor offset −0.160 (3.9363 mA, −0.398 %; after the trim PV 0.000 and 4.0003 mA); Reject if > 0.25 % of span, setpoint delay 5.0 s, 5 points up and down (0, 10, 20, 30, 40), hysteresis +0.004 kgf/cm² on the descending points.
- Values added by the manager and shown to the owner for approval: Adjust if 0.15, Do not Adjust if 0.05, Adjust to 0.05 (% of span), maximum point deviation 0.10 %, calibration period 365 days, reference module 0…60 kgf/cm², the Device Information placeholders (Maker X, Pressure TX, 15.03.2026 …).

## Environment notes
- On Python 3.13 use the virtual environment of the root `CLAUDE.md`. In this container `edge-tts` 7.2.8 was refused with 403 by the speech service; `pip install -U edge-tts` (7.3.1) fixed it.

## Owner decisions
- 2026-10-16: new project `mc5_hart`, three episodes of 5–6 minutes, theme light; only the calibrator's options and screens (no transmitter explanation, no ports, no wiring, no separate safety section); this session produces episodes 1–3; no review questions.
- 2026-10-16: narration approved with six wording edits (no number chains, الدَّخْل, الوَسْم, the AO link in episode 2 segment 5, the C/Adjust sentence, the pressure unit), the Device Information date 15.03.2026, and Device Settings shown as two scrolled pages.
- 2026-10-16: cost rules: the manager writes, builds and fixes by itself; haiku agents only for rendering, QA runs, contact sheets and joining, with a report of at most 15 lines; the critic by its definition (first round on the whole episode, later rounds on the changed segments); commit and push before every render and every critic round.
