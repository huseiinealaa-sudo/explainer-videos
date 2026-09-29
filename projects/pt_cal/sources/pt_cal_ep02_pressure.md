# pt_cal_ep02_pressure — research notes (claim → source → note)

Priority-1 sources (Beamex Oy Ab, free at beamex.com/manuals-and-brochures and the product pages;
page = printed page; for PGXH/PGM/PGPH the PDF page is also given):
- **[PGHH]** PGHH Hydraulic Calibration Pump User Manual, 8802700 / Version 2.0a (2026) — https://www.beamex.com/app/uploads/2026/05/pghh-user-manualeng.pdf
- **[PGXH]** PGXH Instruction Manual, 8801400 (2009) — https://www.beamex.com/app/uploads/2018/11/PGXH_Instruction_Manual.pdf
- **[PGHS]** PGHS Hydraulic Calibration Pump User Manual, 8888600 / Version 1.0 (2026) — https://www.beamex.com/app/uploads/2026/04/pghs-user-manualeng.pdf
- **[PGC]** PGC Calibration Pump User Manual, 8804900 / Version 2.0a — https://www.beamex.com/app/uploads/2026/05/pgc-user-manualeng.pdf
- **[PGM]** PGM Instruction Manual, 8801300 — https://www.beamex.com/app/uploads/2016/10/PGM-Manual.pdf
- **[PGPH]** PGPH Instruction Manual, 8804400 / Version 1.1 — https://www.beamex.com/app/uploads/2016/10/PGPH-Instruction-Manual.pdf
- **[PGV]** PGV Manual — https://www.beamex.com/app/uploads/2016/10/PGV-Manual.pdf
- **[PGL]** PGL User Manual — https://www.beamex.com/app/uploads/2023/03/pgl-user-manual.pdf
- **[PG-BR]** Beamex PG calibration pumps brochure (04/2025) — https://www.beamex.com/app/uploads/2025/04/beamex-pg-pumps-brochure-eng.pdf
- **[EPG-BR]** ePG brochure (12/2025) — https://www.beamex.com/app/uploads/2025/12/beamex-epg-brochure-eng.pdf ; **[EPG-UM]** ePG User Manual 8805000 / 3.0a — https://www.beamex.com/app/uploads/2024/04/epg-user-manualeng-1.pdf
- **[POC8-BR]** POC8 brochure — https://www.beamex.com/app/uploads/2024/01/beamex-poc8-brochure-eng.pdf
- **[MC6-BR]** MC6 brochure (2024) — https://www.beamex.com/app/uploads/2024/06/mc6-brochure.pdf
- Priority 2: Beamex blog, "Understanding the adiabatic process in pressure calibration" (2024-01-17) — https://blog.beamex.com/adiabatic-process-in-pressure-calibration

## A. The owner's claims
| # | Claim | Source | Result |
|---|---|---|---|
| 1 | PGL −400…+400 mbar, screw coarse + fine | [PG-BR] p7; [PGL] p1 | confirmed |
| 2 | PGV vacuum −0.95…0 bar | [PGV] spec ("0 to −0.95 bar") | confirmed |
| 3 | PGM 0…20 bar, fine volume control | [PG-BR] p3; [PGM] p2 (PDF 5) | confirmed |
| 4 | PGC −0.95…35 bar, pressure/vacuum selector, fine adjust | [PG-BR] p4; [PGC] p3, p8 | confirmed |
| 5 | PGPH −0.95…140 bar bench pump with volume adjuster | [PG-BR] p6 ("table pressure generator … adjustable volume control"); [PGPH] p1, p7 | confirmed |
| 6 | PGHH liquid (mineral oil or distilled water) 0…700 bar, volume adjuster | [PGHH] p3, p7 | confirmed |
| 7 | PGXH liquid up to 700 bar | [PGXH] p2 (PDF 5) | confirmed |
| 8 | **PGHS up to 1000 bar "with a small internal volume that speeds stabilisation"** | [PGHS] p3, p8 (0…1000 bar, bench pump, three-arm handle, priming pump) | 1000 bar **confirmed**; **"small internal volume speeds stabilisation" not found** in [PGHS] (it says the opposite risk: air or temperature differences lengthen stabilisation, p16, p20) → **correction**: describe PGHS as a bench pump with a three-arm screw handle and a priming pump |
| 9 | ePG battery pump −0.85…20 bar; controlled by MC6 → fully automatic; works with any calibrator | [EPG-BR] p2–3; [EPG-UM] p20 ("can communicate with Beamex MC6 family calibrators, making it possible to perform fully automatic pressure calibrations"; needs MC6 firmware 4.30+ and the ePG option) | confirmed; [+] "with the MC6 option" |
| 10 | POC8 automatic controller vacuum…210 bar, bench or in CENTRiCAL, with MC6 and software | [POC8-BR] p1 | confirmed |
| 11 | Fine adjust changes the volume slightly → fine control; without it you oscillate and overshoot | [PGHH] p3 ("adjustable volume (called Fine adjust) for fine-tuning"); overshoot → Beamex hysteresis blog (see ep04 notes) | confirmed |
| 12 | Air: thermal effect; hydraulic almost free of it | [PGM] p4 (PDF 7) thermodynamic note; blog: "more prominent in air or gas-operated calibration pumps than in hydraulic (water or oil) ones" | confirmed. **Refined**: [PGHH] p16 still says the pressure "may drop slightly due to the thermodynamic effects or the Pressure Hose stretching" → narration says "much smaller", not "none" |
| 13 | Hydraulic needs cleaning; not for a transmitter returning to sensitive gas service | [PGHH] p12–13 (system liquid only; process media compatible; flush DUT); [PGC] p7 ("Never use the same hose for both gases and liquids") | consistent; the reason is stated as a teaching conclusion from these lines |
| 14 | 40 bar hoses + Bx G1/8 low/medium; 630 bar hoses + Bx 1215 high (تحقق) | [MC6-BR] p12 (P100m…P20C: "Bx G1/8" male compatible with Beamex 40 bar hoses"; P60, P100, P160: "Bx 1215 male compatible with Beamex 630 bar hoses"); [PGC] p8 (40 bar T-hose); [PGHH] p4, p8 (630 bar hose, Bx 1215) | **confirmed** |
| 15 | Every extra adapter a potential leak; shortest chain best | owner's practice; [PGHH] p5 (use only original fittings) | kept (practice) |

## B. The completed section (hydraulic hand pump, pneumatic pumps) — see `pt_cal_source.md` §2-أ/2-ب
Every line there carries its page. The narration of segments 2–6 and 8 is built only from those lines.

## C. Notes
- [PGC] p7 warns: "Do not use Teflon (PTFE) tape to seal any parts of the pump" — consistent with ep04's
  "PTFE tape on adapters" (that refers to threaded adapters of the setup, not to the pump body).
- Check valves: the hand-pump principle (piston + check valve) is from [PGM] p5–6 (PDF 8–9:
  "Main piston", "Check valve"); the PGHH manual names the handles, the stroke selector and the vent
  valve but not its internal valves, so the PGHH drawing is labelled "simplified".
