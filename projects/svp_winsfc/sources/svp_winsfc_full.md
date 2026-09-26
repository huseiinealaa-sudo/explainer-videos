# svp_winsfc_full — research notes (claim → source → note)

Format per root `CLAUDE.md`: claim → source → short note. Page numbers are the printed page labels.
Research only verifies the cleaned source (`svp_winsfc_source.md`); [+] marks a sentence added or corrected from research.

## Sources
| Key | Document | Priority |
|---|---|---|
| **SVP** | [Honeywell Enraf Small Volume Prover Installation, Operation & Service Manual, models 35/50/85/120, part 44200001 Rev 3, 3rd ed. March 2016](https://prod-edam.honeywell.com/content/dam/honeywell-edam/pmt/hps/products/pmc/terminals/provers/small-value-provers-svp-and-controllers/small-volume-prover/pmt-hps-Honeywell-Enraf-Small-Volume-Prover-Installation-Operation-Service-Manual-035-120.pdf) (the 05/15/25 edition, [part 44200002](https://prod-edam.honeywell.com/content/dam/honeywell-edam/pmt/hps/products/pmc/terminals/provers/small-value-provers-svp-and-controllers/small-volume-prover/pmt-hps-Honeywell-Enraf-Small-Volume-Prover-Installation-Operation-Service-Manual-005-025.pdf), has the same text in every section cited) | 1 |
| **CTRL** | [Honeywell Enraf SVP Controller Operation Manual, part 44200004 Rev 2, March 2016](https://prod-edam.honeywell.com/content/dam/honeywell-edam/pmt/hps/products/pmc/terminals/provers/small-value-provers-svp-and-controllers/small-volume-prover-controller/pmt-hps-Honeywell-Enraf-SVP-Controller-Operation-Manual.pdf) | 1 |
| **DFC** | [Dynamic Flow Computers, SFC332PM Metric Operators Manual, Prover Version, 12/4/2025](https://dynamicflowcomputers.com/wp-content/uploads/SFC332P-Manual-Metric.pdf) (listed on the [SFC 332 technical manuals page](https://dynamicflowcomputers.com/products/sfc-332-product-line/sfc-332-series-technical-manuals/)) | 1 |
| DFC-web | [DFC SFC 332P product page](https://dynamicflowcomputers.com/products/sfc-332-product-line/sfc-332p/); [What is Dynacom](https://dynamicflowcomputers.com/wp-content/uploads/What-is-a-Dynacom-Application.pdf) | 1 |
| WIKA | [WIKA data sheet IN 00.29, Callendar-van Dusen equations (08/2014)](https://www.wika.co.jp/upload/DS_IN0029_en_co_59667.pdf) — quotes the EN/IEC 60751 coefficients | 1 |
| CFR | [43 CFR § 3174.1, definitions (US federal regulation, liquid measurement)](https://www.law.cornell.edu/cfr/text/43/3174.1) | 2 |
| Coastal | [Coastal Flow, Understanding Liquid Meter Provings and Proving Reports, class 4250.1](https://coastalflow.com/wp-content/uploads/2021/07/Understanding-Liquid-Meter-Provings.pdf) | 4 |

## Verified claims by segment
| Seg | Claim | Source | Note |
|---|---|---|---|
| 1 | The prover is classed as a Small Volume Unidirectional Piston Displacement Prover. | SVP §8.12 Table 28 p. 8-42 | FAQ. |
| 1 | [+] A large (typically pipe) prover needs more than 10,000 meter pulses to generate a meter factor; an SVP with double chronometry needs fewer. | SVP p. 8-42; DFC p. 1-40; Coastal p. 4–5 | Source said "per run"; Honeywell says "to generate a meter factor", DFC "per run", Coastal/API "per pass". Narration follows Honeywell. |
| 1 | Offered as a portable prover with trailer. | SVP Table 1 p. 1-3 | "P – Portable prover with trailer supplied". |
| 2 | Honed flow tube, chrome-plated bore; poppet valve coaxial in the free piston. | SVP p. 1-1; Table 3 p. 1-4 | |
| 2 | A piston shaft on both sides, so the displaced volume is the same and the prover may sit upstream or downstream of the meter. | SVP p. xvii item 5, §2.3 p. 2-1, p. 8-42 | |
| 2 | Guide block carries cam followers, bearing guide bars, flag, motor stop ramp; the upstream shaft connects to the guide block. | SVP Fig. 8-8 p. 8-14; §8.5 p. 8-5–8-6 | |
| 2 | Return by motor, gear reducer and chain. | SVP p. 1-1, §8.8 p. 8-14 | |
| 2 | Optical switches: 5 × 10⁻⁶ s, ±0.0005 % repeatability of linear measurement. | SVP p. 1-1 | 5 µs spoken; ±0.0005 % shown on screen only. |
| 2 | The switches sit on the switch bar in the drive end (thermometer T2 on the switch bar, under the drive cover). | SVP §5.3 step 15 p. 5-8 | |
| 2 | Switches are field replaceable without recalibration. | SVP §1.2 p. 1-2, §5.1 p. 5-1, §8.9 p. 8-37 | |
| 2 | Detector bar has its own temperature (Td) and linear coefficient (Gl). | SVP §5.5 p. 5-19; DFC p. 3-2 | |
| 3 | Stand-by: piston downstream, poppet open; FC signals the motor; piston disconnects; spring closes poppet; piston synchronised with the fluid; start/stop switches; shaft stopped mechanically; pressure opens poppet; flow continues. | SVP §1.5 p. 1-14 | |
| 3 | [+] "with little to no pulsation or surge". | SVP p. 1-14 | Source said "بلا نبضة ضغط"; narration "بِلَا نَبْضَةِ ضَغْطٍ تُذْكَرُ". |
| 3 | Motor switch timeout covers retraction to the motor stop switch; error Motor time out. | SVP §3.3.6.2.5 p. 3-12; §6.2.2 p. 6-1 | S85 factory value 58 s (data module). |
| 3 | For Coriolis/ultrasonic meters slow the prover to lengthen the run-up time (release → first switch). | SVP p. 8-42 | |
| 3 | Volume pulse 25 ms, sent when either switch is triggered on the downstream pass. | SVP §7.2.2 p. 7-6 | Given for the CONDAT wiring; it describes the controller's output. |
| 3 | During retraction the flag passes the downstream then the upstream sensor. | SVP §4.3 p. 4-2 | |
| 3 | Example: 4.5 s between the detectors. | data: SWEEP_TIME = BPV ÷ Q × 3600 | |
| 4 | The prover does not measure anything; it waits for a start signal from the FC and sends back pulses at the switches. | SVP p. 8-42 | |
| 4 | Three enclosures; SVP Controller Box wired at the factory, must not be modified; Power Box has two separate supplies (motor, clean/instrument); customer connections in the Power Box and CCB. | SVP §2.4.3 p. 2-6–2-7 | |
| 4 | CCB terminals 12 Feed+, 13/14 Run permissive +/−, 15 Common, 16/17 Volume pulse +/−. | SVP §7.2.4 p. 7-7; CTRL p. 6-5 | |
| 4 | Both signals pass an isolation stage (optocouplers) in the controller. | CTRL Fig. p. 6-5 | Drawing labelled "Isolation". The source's "prevents ground loops, protects each side" is not stated; narration only says the signals cross an optical isolator. |
| 4 | 1500 Ω current limiting resistor with 12–24 VDC; zero-ohm jumper from 6 to 12 V. | SVP §7.2 p. 7-4; CTRL p. 6-4 | On screen. |
| 4 | SFC332P switch outputs are open collector and need external DC power; all I/O optically isolated. | DFC p. 1-2, 1-28, 1-39, 2-16 | On screen note. |
| 4 | [+] "Prover does not cycle": no power; interface cable not properly connected; controller not in Meter Calibration. | SVP Table 25 p. 6-3 | Source omitted "no power". |
| 5 | LAD = Local Access Device, a hand-held controller. | SVP p. xi, §3.2.2 p. 3-2 | |
| 5 | Prover Status screen: mode, piston, motor, error, cycle, stop time, sweep time. | SVP §3.1 p. 3-1 | |
| 5 | Meter Calibration is the default mode; Prover Test only without run permissive; Prover Calibration ignores run permissive and is kept in NVM after power loss. | SVP §4.2 p. 4-1, §4.3 p. 4-3, §5.3 p. 5-7, p. 5-10 | |
| 5 | Four errors: Sensor out of sequence, Motor time out, Sensor stuck, Service due (default 1000 cycles). | SVP §6.2 p. 6-1–6-2; §3.3.6.4 p. 3-13 | |
| 5 | Motor parameters set at the factory per model; change only after consulting Honeywell. | SVP p. 3-8, p. 3-12 | |
| 5 | Dashboard: a working switch reads High; an opaque flag makes it Low. | SVP §6.3.1 p. 6-2 | On screen only. |
| 6 | Double chronometry: time A (first → final detector), time B (first meter pulse leading edge after A starts → first after A stops), C whole pulses; interpolated = C × A ÷ B. | DFC p. 1-40 | Our t_D = A, t_P = B, N = C. |
| 6 | Corrected prover volume = BPV × CTSp × CPSp × CTPLp; meter volume = counts ÷ K; corrected meter volume × CTPLm; MF = corrected prover ÷ corrected meter. | DFC p. 3-1–3-2 | |
| 6 | CTSp = [1 + (Tp − Tb)Ga][1 + (Td − Tb)Gl] (detector mounting ON); CPSp = 1 + (P − Pb)·ID ÷ (E·WT). | DFC p. 3-2; SVP p. 5-19 | |
| 6 | Actual K shown in the last prove data. | DFC p. 4-15 | K ÷ MF is derived (the K that makes the meter volume equal F). |
| 7 | Maintenance basis 100 passes/day, refined products, 25 °C, clean; before each session / monthly / semi-annually lists. | SVP §8.3 p. 8-1–8-2 | |
| 7 | Static leak test: 6 psid, wait ≥ 5 min, observe 20 min, drop > 25 % = seal leak; before water draw or when repeatability is hard. | SVP §5.2 p. 5-1–5-3 | |
| 7 | Water draw: ≥ 3 consecutive draws within 0.02 %, one at a 25 % different flow; recalibrate every year or as the responsible parties decide; required after complete switch bar replacement. | SVP §5.1 p. 5-1; p. 5-6, 5-12 | See conflict 4. |
| 8 | SFC332P talks Modbus (RTU/ASCII), baud 1200–19200, Unit ID 1–247; memory reset gives ID 1, 9600, RTU. | DFC p. 1-11, 2-3 | |
| 8 | Connect to Device / Go Offline. | DFC p. 2-19 | |
| 10 | Menus: Configuration File, View, Tools, Calibration, Parameter Overrides, Historical Data; Configure Device opens the configuration menu. | DFC ch. 2 p. 2-1–2-22; p. 1-14 | |
| 10 | Calibration: full / single / offset calibration of inputs and outputs. | DFC p. 1-34–1-38, 2-19 | |
| 10 | Overrides replace live values used in the proving calculations; Reset Prove Data Area resets a meter's previous prove data; Clear System resets all data. | DFC p. 2-20–2-21 | The 60-meter capacity and "previous three meter factors" are on DFC-web. |
| 11 | Prove Data fields: prover type (0–7), method (volume/mass), runs to average 1–10, total runs 1–20, abort time-out, pulse deviation (repeatability), detector switch type, single detector delay, prover volume "per water draw", diameter, wall thickness, modulus E, temperature sample period, allowable change, flow-rate change, prover/meter temperature deviation, base temperature, displacer shaft coefficient, area thermal coefficient, upstream signal polarity, run output polarity. | DFC p. 2-6–2-9 | No. of Pass per Run and Volume Resolution Decimal: DFC p. 4-6. Base temperature 0 = 15 °C, 1 = 20 °C: p. 4-6. |
| 11 | Ga for 316 SS = 3.18e-05 /°C; displacer-shaft coefficient for 304 SS = 1.73e-05 /°C. | DFC p. 2-9 | Our GA, GL. |
| 12 | Diagnostic menu shows live inputs and outputs: pulse inputs on top, status inputs below. | DFC p. 1-39 | |
| 12 | [+] Fail Code 0 = live value always; 1 = maintenance value always; 2 = maintenance value if the transmitter fails. | DFC p. 1-15, 2-13 | Fills the gap "Fail Code is a behaviour choice". |
| 12 | Flow rate = pulses/s × 3600 ÷ K. | DFC p. 3-1 | 3333.3 Hz → 200.0 m³/h. |
| 12 | Pt100 (EN/IEC 60751): R = R0(1 + At + Bt²), A = 3.9083e-3, B = −5.775e-7; α = 0.00385. | WIKA p. 1–2 | 115.54 Ω → 40.0 °C; linear 40.36 °C (conflict 1). |
| 12 | Transmitters and alarms are labelled by TAG ID; the value used comes from the input assignment. | DFC p. 2-10–2-14 | |
| 13 | Status input functions (Dialog Scroll, Dialog Select, Prove Request single/sequence, display freeze/toggle, Prover Ready) and switch output functions (Prove meter, Launch forward/reverse, Prove in progress, Compact prove run, Prove complete, Prove abort). | DFC p. 2-16 | No assignment numbers in the video. |
| 14 | [+] The prove completes when "Runs to Average" consecutive runs are within the limit; "Total Runs" is the maximum allowed. | DFC p. 2-6 | Source said "repeat until Total Runs, then check". |
| 14 | Repeatability (pulse deviation) = (highest − lowest) ÷ lowest × 100. | DFC p. 2-7 | 0.0187 % in our example. |
| 14 | Five runs within 0.05 % ≈ 0.027 % uncertainty (API MPMS 4.8 Annex A). | Coastal p. 3 | Not spoken; supports the 5-run / 0.050 % example. |
| 15 | Safety: covers in place; pressurise slowly (hydraulic shock); depressurise and drain before service; lockout-tagout inside the drive end cover; do not open electronics enclosures in an explosive atmosphere. | SVP p. xii–xiii, p. xix | |

## Conflicts and corrections (for the owner)
1. **Pt100 linear check.** (115.54 − 100) ÷ 0.385 = 40.36 °C, not 40.37 °C. 40.37 comes from the unrounded CVD resistance at 40 °C (115.5408 Ω). **Owner decision: the video shows 40.36 °C.**
2. **Composite MF = MF × CTPLm.** Not defined in the DFC manual (only the report field "Prover Meter Composite Factor", p. 4-13). Official definition: 43 CFR § 3174.1 (US federal regulation, liquid measurement, following API MPMS 12.2): "Composite meter factor means a meter factor corrected from normal operating pressure to base pressure", i.e. **CMF = MF × CPLm** (pressure correction only); MF × CTPLm is the combined correction, not the CMF. Source: https://www.law.cornell.edu/cfr/text/43/3174.1. **Owner decision (2026-09-26): removed from the video and from the data module.**
3. **Repeat until Total Runs.** DFC p. 2-6: the prove completes when "Runs to Average" consecutive runs meet the limit; "Total Runs" is the maximum. Narration corrected.
4. **Water draw interval.** SVP §5.1 p. 5-1: every year or as the responsible parties decide; SVP §8.11 p. 8-41 (service offering): "Water draw (Recommended every 2 years)". Narration follows §5.1 (owner decision).
5. **10,000 pulses "per run".** SVP p. 8-42: "to generate a meter factor"; narration follows Honeywell.
6. **"No pressure pulse".** SVP p. 1-14: "little to no pulsation or surge"; narration "بِلَا نَبْضَةِ ضَغْطٍ تُذْكَرُ".
7. **First causes of "prover does not cycle".** SVP Table 25 p. 6-3 lists no power first; narration: power, interface cable, controller mode.
8. **"Works with any flow computer that supports double chronometry".** SVP p. 1-2 / p. 2-6: industry standard flow computers equipped with double chronometry; other brands: consult Honeywell and the FC maker. Not spoken.
9. **Halving the maintenance intervals.** SVP p. 8-1: for fluids with entrained solids or low lubricity, and for high duty cycles ("3rd party service portables"), not for frequent moving. Not spoken (time).
10. **Prove Volume "a factory value until a water draw".** DFC p. 2-7: "prover volume … at reference conditions per water draw"; the factory value is itself a water draw (SVP §1.4 p. 1-13). Narration: "from the last water draw".
11. **Displacer Shaft Coeff. of Exp.** DFC p. 2-9 calls it the expansion coefficient of the prover piston (displacer) shaft; with "detector mounting ON" it is the Gl of CTSp with the shaft temperature Td (p. 3-2). Honeywell's Gl and Td are the detector (switch) bar's (SVP p. 5-8, 5-19). Same role; the video says "the bar's coefficient".
12. **Base temperature.** DFC p. 3-2 defines BPV at 20 °C in its text, but the field offers 15 °C or 20 °C (p. 4-6); 15 °C is valid.
13. **Units of D and t.** DFC metric asks for centimetres (p. 2-8); our example is in mm. CPSp uses only D ÷ t, so the result is the same.
14. **Name "WinSFC".** The DFC manual calls its Windows configuration program "Dynacom" (p. 1-5, 2-22); "WinSFC" does not appear in it. Owner decision: keep WinSFC only, no sentence about Dynacom.

## Kept from the cleaned source, not covered by the official manuals (screen details)
Comm. Status IDLE (ONLINE) / OFFLINE and the Calibration/Override menus disabled offline; per-window "Upload from FC / Download to FC" and "Upload Full / Download Full"; Window and Help menus; side buttons Historical Reports and Prover Diagram; Diagnostic columns mA/Ohm, Numerical, Calibrate; "Alarms: NONE". The manuals confirm the functions, not these labels. Owner decision: keep them all (direct observation of the software).

## Left out of the narration (time, or not verifiable)
- Not verifiable in the manuals: "the constrained motion on the bars ties the beam cut to the piston position alone"; "stability checks disabled by zero leave the judgement to people"; "a wire on the wrong terminal in the meter pulse cable made the provings wander" (sounds site-specific); "isolation prevents ground loops and protects each side".
- For time: aluminium and stainless switch bases must not be mixed (SVP p. 8-37); chain lubrication with dry PTFE lube (SVP p. 8-14); the field hook-up steps (hoses, venting to the drain system; SVP §4.1 p. 4-1); Motor off delay; the unknown piston position after a machine fault (SVP p. 4-2); the fixed-value sign of an override in reports (segment 12 keeps the round-value check); Composite MF (conflict 2, removed).
