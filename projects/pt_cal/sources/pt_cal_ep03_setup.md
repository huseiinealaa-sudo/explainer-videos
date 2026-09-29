# pt_cal_ep03_setup — research notes (claim → source → note)

Sources:
- **[R3051]** Emerson, Rosemount 3051 Pressure Transmitter Reference Manual, 00809-0100-4001 Rev KA (May 2017), HART — https://www.instrumart.com/assets/rosemount_3051-hart_manual.pdf (Emerson document; used only for generic terms and the manifold sequence; the transmitter is shown unbranded)
- **[MC6-UM]**, **[MC6-BR]** as in ep01 notes.
- **[OSHA]** OSHA, Hydrogen Sulfide — https://www.osha.gov/hydrogen-sulfide and https://www.osha.gov/hydrogen-sulfide/hazards
- Priority 2: Beamex blog, "Calibrating a square rooting pressure transmitter" — https://blog.beamex.com/2015/12/10/calibrating-a-square-rooting-pressure-transmitter

| # | Claim (owner's text) | Source | Result |
|---|---|---|---|
| 1 | Gauge zeroed when vented; absolute references vacuum, not zeroed by venting | [R3051] p71: "Do not perform a zero trim on … Absolute Pressure Transmitters. Zero trim is zero based, and absolute pressure transmitters reference absolute zero … perform a low trim" | confirmed |
| 2 | Absolute needs BARO or an absolute reference | [MC6-BR] p12 note 3 (gauge modules shown as absolute with PB/EXT B) | confirmed |
| 3 | DP = HP − LP | [R3051] p53 (H / L sides) | confirmed |
| 4 | 50 % DP with square root in the transmitter ≈ 15.314 mA | computed: 4 + 16·√0.5 = 15.3137 (`pt_cal_data.DP_50_SQRT_MA`); blog confirms the transfer function | confirmed |
| 5 | (A) workshop: MC6 supplies 24 V and measures; HART available directly | [MC6-UM] p47, p60; [MC6-BR] p9 (built-in HART impedance) | confirmed |
| 6 | (B) live loop: DCS supplies, calibrator measures only | [MC6-UM] p47 (external supply) | confirmed |
| 7 | (C) across the transmitter's test diode | [R3051] p69: "connecting the meter to the test terminals on the terminal block" | test terminals confirmed; the diode-leakage-at-temperature remark is the owner's practice, kept without a new number |
| 8 | HART needs ≥ 250 Ω; plant loop may already have it; modem in parallel | [MC6-UM] p60 ("250 Ω for HART" with external supply); [R3051] power-supply section | confirmed |
| 9 | **Manifold: "closing LP alone at 40 bar applies full line pressure to one side"; "absolute rule: open equalize first, before closing any isolate valve"; isolation: equalize → close HP → close LP → vent; return: close vent → equalize open → open HP → open LP → close equalize last** | [R3051] p53–54 (3- and 5-valve manifolds, zero trim at static line pressure): "In normal operation the two isolate (block) valves … open and the equalize valve closed. 1. … close the isolate valve on the low side … 2. Open the equalize valve … 3. After performing a zero trim … close the equalize valve. 4. Finally, to return the transmitter to service, open the low side isolate valve." | **correction** (see below) |
| 10 | Forgetting to close equalize → reads zero | [R3051] p53–54 (equalize open = both sides at the same pressure) | confirmed |
| 11 | H₂S heavier than air, collects low; smell disappears at high concentration | [OSHA] main page: "It is heavier than air and may travel along the ground. It can build up in low-lying areas, and in confined spaces." "After a while at low or more quickly at high concentrations, you can no longer smell it"; hazards page: loss of smell (olfactory fatigue or paralysis) at 100–150 ppm | confirmed |
| 12 | Zones 0/1/2 definitions | IEC 60079-10-1 zone definitions (continuous / likely in normal operation / not likely, short period) | consistent; equipment categories per site procedure (owner's text kept) |
| 13 | Safety items (permit, gas test, PPE, LOTO, DBB, SIS bypass) | site / company procedures (not a single public document) | kept as the owner's procedure text; no new facts added |

## Correction to #9 (manifold)
- Physics: closing an isolate valve traps the pressure already on that side; it does not add line
  pressure to one side. The damaging case is a **large differential**: one side vented (or at a low
  pressure) while the other still holds line pressure with the equalize valve closed — e.g. opening
  a drain/vent before equalizing, or opening one isolate valve on a vented body without equalizing.
- Official order ([R3051] p54) for a 3-valve manifold: **close the LP isolate valve → open the
  equalize valve** (not "equalize first": with both isolate valves open, opening the equalize valve
  first connects the HP and LP process lines through the manifold). Return: **close equalize → open
  LP isolate**.
- Narration (proposal): isolation = close LP isolate → open equalize → close HP isolate → open the
  vent slowly (away from the face) → confirm zero. Return = close the vent → (equalize open) open HP
  isolate slowly (both sides rise together) → **close equalize** → open LP isolate → leak check, watch
  the reading with the control room. Rule stated: "never let one side be vented or depressurised
  while the other holds line pressure; equalize before venting and before pressurising".
