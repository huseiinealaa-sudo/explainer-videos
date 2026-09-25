# Episode 6 — FloBoss S600+, web interface, typical proving session: sources (research draft)

Format: claim → source → note. Priority per CLAUDE.md (1 manufacturer, 2 API, 3 papers, 4 industry training).
Status: research notes + owner decisions; narration drafted for approval.

Main sources (priority 1, Emerson):
- [FloBoss S600+ Product Data Sheet D301151X012 (Jan 2023)](https://www.emerson.com/documents/automation/s600-product-data-sheet-en-132238.pdf) — "data sheet".
- [FloBoss S600+ Instruction Manual D301150X412 (May 2024)](https://www.emerson.com/documents/automation/s600-instruction-manual-en-132470.pdf) — "S600+ manual".
- [Config600 Configuration Software User Manual (Oct 2024)](https://www.emerson.com/documents/automation/config600-configuration-software-user-manual-en-132292.pdf) — "Config600 manual"; §5.7.3 (compact prover), Appendix B.2 (compact prover, liquid only).

## Owner decisions (2026-09-25)
1. **«الحقيبة» = the field case (owner's description, not a published source; not marked [+]).** A black portable Emerson field case with a FloBoss S600+ inside; power and signal cables leave the case to the meter and the prover and link them all. Drawing (simplified, no photo): a white panel inside the case with the Emerson name and the S600+ front (display + keypad); at the top: round signal-cable connectors, the main power switch and two fuses; above the computer: a row of buttons and lamps, including RUN, PRINT REPORT and a detector-status lamp; on the side: communication ports (Modbus, printer, network) and two ventilation openings; two lines from the case to the meter and the prover. No serial numbers, connector names or other details.
2. **Proof report:** say "at the end of the runs the computer issues the proving report", without claiming it is a default; show a simplified report with our demo values (conflict 1 below).
3. **Maximum passes per run:** not mentioned (conflict 2 below).
4. **STAB STATUS and CERTIFICATION DATE:** dropped; use only the documented stage names (conflict 3 below).
5. **Typical session:** the nine steps proposed (log in → check CSUM → start → stability → 5 runs of 3 passes → repeatability 0.03 % → MF download → accept → report and Log Off), demo values only.
6. **What KF DOWNLOAD sends (owner check, 2026-09-25).** Config600 Table B-15 stage 19 "K-factor Download": "Copy proof K-factor, meter factor, flow rate, and frequency into proving stream data points … The stream metering calculations do not use these until commanded separately." §5.7.3 notes: "Applications typically use the original K-factor from the meter calibration report and update the meter factor … Alternatively, the meter factor can remain unchanged and the K-factor … updated." It depends on the configuration. **Choice:** the typical case, consistent with episode 1 (K stays 60000, MF = 0.999; "K or MF, not both"): the narration keeps "the meter factor 0.999", and the screen shows "KF DOWNLOAD (MF = 0.99900)".

## Candidate claims (verified in the sources)

| # | Claim | Source | Note |
|---|---|---|---|
| 1 | The S600+ is a panel-mount fiscal flow computer for liquid and gas; applications include custody transfer and meter proving. | data sheet p.1 | |
| 2 | Front panel: 8-line LCD (128 × 64, 8 lines of 20 characters) and a 29-key keypad; view or change parameters without a PC; 3-colour alarm/status LED. | data sheet pp.1, 12 | |
| 3 | Painted, welded steel outer case with plastic front panel; circuit boards slide in from the rear. | data sheet p.12 | Possible meaning of «الحقيبة» (question 1). |
| 4 | Modules: CPU (P152), I/O (P144) with Pulse Mezzanine (P148); optional Prover module (P154), HART (P188). Compact proving needs CPU + I/O + Prover (P154). | data sheet p.2; Config600 manual B.2.1 | |
| 5 | Prover support: compact, uni/bi-directional, master meter, dual chronometry; up to two provers (not simultaneously). | data sheet p.6 | |
| 6 | Configuration is made with the Windows tool Config600 and sent to the S600+. | data sheet p.2; Config600 manual ch.9 | |
| 7 | Config600 applies a checksum to the configuration file; the S600+ warns if it does not match. The S600+ also computes a configuration checksum continuously; a change raises the "CONF CSUM" alarm. | Config600 manual §9.1.4; alarm list | Our demo: DEMO_PRV_CFG / CSUM a1b2. |
| 8 | Embedded web server: remote access to reports, displays, diagnostics; user name + password; the security level decides what each user sees. | S600+ manual ch.6 p.6-1 to 6-3; data sheet p.2 | |
| 9 | Access: type the S600+ IP address in the browser (http://…); Microsoft Edge recommended. | S600+ manual §6.2 | Demo screens use a placeholder address only. |
| 10 | Menu bar: Reports, Alarms, Current, Flow Rates, Totals, Operator, Plant I/O, System Settings, Tech/Engineer, Calculations, Diags, Log Off; hierarchy menu on the left, display area on the right. | S600+ manual Table 6-1, Fig. 6-2 | Drawn as a simplified mock-up, not a copy. |
| 11 | Up to five web sessions, but only one point of control: the first user (front panel or web) can change data; others only view. | S600+ manual §6.2 | |
| 12 | Always use Log Off (not just close the browser), to release control and clear the cache. | S600+ manual §6.2, §6.3 | |
| 13 | Bold text can be changed; red text is in alarm; some screens have a CSV button to export. | S600+ manual §6.3 | |
| 14 | Reports, alarms and events can be exported to a USB flash drive (front panel or web: Tech/Engineer > USB). | S600+ manual §3 "USB Port", §5.14 | |
| 15 | Compact prover inputs: inlet/outlet/plenum pressure, inlet/outlet temperature, raw meter pulses, prove enable, prover ready (upstream), detector switch. Outputs: hydraulics on/off, launch (run), plenum charge, plenum vent. | Config600 manual B.2.1 | Links to episodes 4–5. |
| 16 | The S600+ can hold the plenum pressure within limits with the charge/vent outputs (R constant and ± tolerance in the prover constants). | Config600 manual B.2.1; §5.7.3 Constants | |
| 17 | The stream computer sends a raw pulse output to the prover computer, which counts pulses during the pass. | Config600 manual B.2.3 | |
| 18 | Pulse interpolation is used when the count is low (typically < 10,000); dual chronometry is the standard method; resolves better than the API 1 part in 10,000. | Config600 manual B.2.3 | Links to episode 5. |
| 19 | CTSp in the S600+ uses the tube coefficient and the Invar rod coefficient, with an "Ambient Temp" entry for the rods; calibration temperature default 15. | Config600 manual §5.7.3 Constants | Consistent with episode 5. |
| 20 | Prove sequence (default): IDLE → INITIALISE → PULSES ON → ENABLE HYDRAULICS → PRV FLOW/T/P STAB → PROOF RUN → KF DOWNLOAD → AWAIT REPROVE (Continue/Terminate) → PS PULSES OFF → TERMINATE. | Config600 manual Table B-14 | |
| 21 | Run control (compact): WAIT READY → WAIT STAB → HOLD STAB → CONTROL PLENUM → PRE FLIGHT AVG → LAUNCH → WAIT 1ST HIT → WAIT 2ND HIT → PASS CALCS → RETRIEVE (next pass) → RUN CALCS → … → STD RPT CHECKS → FINAL AVG → REPORT STAGE. | Config600 manual Table B-17 | |
| 22 | Stability: wait time (default 300 s) then hold time (default 10 s); the run aborts if stability is lost during the hold. | Config600 manual §5.7.3 Run Data | |
| 23 | Runs Reqd default 5 consecutive runs within tolerance; Runs Max default 12. | Config600 manual §5.7.3 Run Data | Our data: 5 runs. |
| 24 | The prove sequence downloads a K-factor and a meter factor; typically the K-factor stays and the MF is updated (or vice versa). | Config600 manual §5.7.3 notes | Consistent with episode 1 ("K or MF, not both"). |
| 25 | Official vs Unofficial prove: an Unofficial prove does not download results; shown in the report header. | Config600 manual §5.7.3 notes | |
| 26 | Results are downloaded but not used until accepted locally or by a supervisory computer (non-Aramco style). | Config600 manual §5.7.3 | |
| 27 | Report "METER PROOF REPORT": header (stream, proving rate, standard density, base volume, temperatures, pressures) and one line per trial/run with temperatures, pressures, density, pulses, flow rate, K-factor. | Config600 manual B.2.10 | Demo report drawn with our values only. |

## Conflicts found (to show the owner)
1. **Proof report for compact provers.** Config600 manual §5.7.3 and B.2 say "The S600+ does not create a proof report, although you can add this option through a user stage"; but Table B-17 has stage 24 "REPORT STAGE — Generates the proof report", and B.2.10 shows proof report layouts.
2. **Passes per run.** §5.7.3 Run Data: "Passes Reqd … to a maximum of 5. The default is 5"; B.2 text: "a default of 5, a maximum of 39". Our data (3 passes) is within both.
3. **Screen fields in the owner's outline** (STAB STATUS, CERTIFICATION DATE) do not appear in these Emerson manuals; they may be site-specific display labels.

## Numbers and names used (from scripts/prover_demo_data.py only)
- PROVER_SERIAL PRV-DEMO-001, METER_TAG FT-DEMO-01, CONFIG_NAME DEMO_PRV_CFG, CONFIG_CSUM a1b2, PROVING_DATE 15/03/2026.
- PASSES_PER_RUN 3, RUN_COUNT 5, REPEATABILITY 0.03 %, REPEATABILITY_LIMIT 0.05 %, MF_AVG 0.99900, K_FINAL 60060.060, RUNS table.
- Web address on screen: 192.0.2.10 (IETF documentation range, RFC 5737), not a real device.
