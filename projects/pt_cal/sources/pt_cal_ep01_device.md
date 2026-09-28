# pt_cal_ep01_device — research notes (claim → source → note)

Priority-1 sources (all free at beamex.com; page = the manual's printed page):
- **[MC6-UM]** Beamex MC6 User Manual, English, published 2026-06 — https://www.beamex.com/app/uploads/2026/06/mc6-user-manualeng.pdf
- **[MC6-BR]** Beamex MC6 brochure (2024) — https://www.beamex.com/app/uploads/2024/06/mc6-brochure.pdf
- **[MC6EX-UM]** Beamex MC6-Ex User Manual (2026-04) — https://www.beamex.com/app/uploads/2026/04/mc6-ex-user-manualeng.pdf
- **[DISC]** Beamex, Discontinued products — https://www.beamex.com/calibrators/discontinued-beamex-products/
- Product pages: https://www.beamex.com/calibrators/beamex-mc6-ws/ , https://www.beamex.com/calibrators/beamex-mc6-t/

| # | Claim (owner's text) | Source | Result / note |
|---|---|---|---|
| 1 | MC6 = meter + signal generator/loop supply + documenting computer | [MC6-BR] p3 ("calibrator and communicator … documenting"); [MC6-UM] p68 (Documenting Calibrator) | confirmed (teaching summary) |
| 2 | MC5 older generation, discontinued, MC5-IS intrinsically safe version | [DISC]: "MC5 … discontinued in 2014 … replacement MC6"; "MC5-IS … replacement MC6-Ex" | confirmed. **"monochrome screen and keypad" not found in an official page** → proposal: say only "older generation, discontinued in 2014" (owner decides) |
| 3 | MC6 5.7-inch colour touch screen (تحقق) | [MC6-UM] p24: "backlit 5.7" TFT LCD … 640×480 … touch panel"; [MC6-BR] p3 "5.7" color touch-screen" | **confirmed** |
| 4 | Five modes; HART, FF, Profibus PA built in | [MC6-BR] p3: "five different user interface modes … Meter, Calibrator, Data Logger, Documenting Calibrator and Communicator"; "fieldbus communicator for HART, FOUNDATION Fieldbus and Profibus PA" | confirmed. [+] note: the communicator protocols are options ([MC6-UM] p… "Communicator options for HART, FOUNDATION Fieldbus H1, or Profibus PA") — narration says "can carry", not "always" |
| 5 | MC6-Ex intrinsically safe (Ex ia) | [MC6EX-UM] marking "Ex ia IIC T4 Ga" (IECEx/ATEX) and "Class I, Zone 0, AEx ia IIC T4 Ga" | confirmed |
| 6 | MC6-WS workshop station; MC6-T temperature | product pages | confirmed (MC6-T out of this part) |
| 7 | E side: measure current from external loop; +24 V supply and measure | [MC6-UM] p47: "decide whether MC6 will supply the 24 V loop supply voltage. If it does not, an external device must be used" | confirmed |
| 8 | **"internal 250 Ω HART resistor enabled instead of an external one"** | [MC6-BR] p11: "Built-in 24 VDC loop supply (low impedance, HART impedance or FF/PA impedance)"; p9: "built-in loop supply and impedances for different buses … no need to use any external loop supply or resistors"; [MC6-UM] p60: with an **external** supply "you might need an external resistor—250 Ω for HART" | **correction**: the manual does not state an internal 250 Ω resistor; it states a built-in *HART impedance* with the internal 24 V supply, and 250 Ω external when the loop has its own supply. Narration follows the official wording |
| 9 | max input 60 VDC and 30 VAC (تحقق) | [MC6-BR] p11 "Max. input voltage 30 V AC, 60 V DC"; [MC6-UM] p11 "Do not exceed 60 V DC / 30 V AC / 100 mA between any terminals" | **confirmed** |
| 10 | Loop opened during current generation → voltage rises; current peak on re-closing; set 0 mA first | [MC6-UM] p56: "If the loop is opened during current generation, MC6 attempts to maintain the current by increasing its output voltage. When the loop is closed again, a short current peak may occur … Always set the output to 0 mA before connecting the loop." | confirmed |
| 11 | INT: up to 3 gauge/differential + 1 barometric | [MC6-UM] p21; [MC6-BR] p12 note | confirmed |
| 12 | EXT external via dedicated port, vacuum to 1000 bar | [MC6-UM] p21 ("barometric up to 1000 bar"), p43 (4-pin LEMO, PX connector); [MC6-BR] p12 (EXT1C −1 bar … EXT1000) | confirmed |
| 13 | BARO → any gauge module also shown as absolute | [MC6-BR] p12 note 3 | confirmed |
| 14 | Choose the smallest module; accuracy is "mostly % of full scale" | [MC6-BR] p12: accuracy/uncertainty = "% FS + % RDG" (e.g. EXT60 1-yr ±(0.01 % FS + 0.025 % RDG)) | **refined**: part of the spec is % of full scale, part % of reading; the FS part is what grows with a bigger module |
| 15 | **"0–42 kg/cm² transmitter with a 700 bar module"** | [MC6-BR] p12 module list: EXT250, EXT600, EXT1000 — no 700 bar module | **correction**: no 700 bar module exists; the example uses EXT600 vs EXT60 (new values from the brochure, computed in `pt_cal_data.py`: ±0.100 vs ±0.016 bar at 42 kg/cm², ×6.2). Needs owner approval (new values) |
| 16 | Vent the port and Zero before work | [MC6-UM] p41: "If a selected pressure module does not display zero when no pressure is applied, it must be zeroed … ensure zero gauge pressure is applied, then press the Zero button" | confirmed |
| 17 | Modes: Meter reads one signal; Calibrator; Documenting Calibrator is for documented calibration; Data Logger; Communicator | [MC6-UM] p64 ("Meter … one signal at a time"), p67 ("To document calibration data automatically, use the Documenting Calibrator mode"), p68, p125, p134 | confirmed |
| 18 | Standard MC6 not intrinsically safe; Ex area → MC6-Ex or move to workshop | [MC6-UM] safety chapter (MC6 carries no Ex marking; MC6-Ex does) | confirmed in substance; "no third option" is the owner's site rule, kept as the owner's wording |
| 19 | Pressure units | [MC6-BR] p12 lists kgf/cm² | on-screen unit "kg/cm²" (owner's convention) |

Left for the owner: #2 (monochrome detail), #15 (new example values).
