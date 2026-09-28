# pt_cal_ep05_verdict — research notes (claim → source → note)

Sources: **[R3051]** Rosemount 3051 Reference Manual 00809-0100-4001 Rev KA (ep03 notes);
**[17025]** ISO/IEC 17025:2017 §7.8 (reporting of results; calibration certificates 7.8.2, 7.8.4; decision rule 7.8.6);
**[MC6-UM]**; Beamex blog "Calibrating a square rooting pressure transmitter" (priority 2).

| # | Claim | Source | Result |
|---|---|---|---|
| 1 | I_expected at the actual measured input; error in % of 16 mA; PASS if \|E\| ≤ tol | standard definitions | computed in `pt_cal_data.py` |
| 2 | 41.928 example: 0.200 % vs 0.371 %, 40 % → 74 % of tolerance | `ERR_PCT_WRONG` 0.200, `ERR_PCT_RIGHT` 0.3714, `TOL_USED_*` 40 / 74.3, pump effect 0.1714 | confirmed |
| 3 | Square-root I = 4 + 16·√(…) and table | `SQRT_TABLE` | **corrections**: the owner's original guide printed 12.762 (30 %) and 19.177 (90 %) — correct 12.764 and 19.179; 9.059, 16.393, 17.386 are truncations of 9.0596, 16.3935, 17.3866 → rounded 9.060, 16.394, 17.387 |
| 4 | Trap: 0 % and 100 % fine, middle points "fail" by large regular amounts → sqrt vs linear mismatch | e.g. 50 %: 15.314 vs 12.000 mA = 20.7 % of span (`TRAP_50_ERR_PCT`) | confirmed |
| 5 | Certificate elements, U with k = 2, decision rule | [17025] 7.8.2.1, 7.8.4.1 (uncertainty, traceability, environmental conditions), 7.8.6 (decision rule) | confirmed |
| 6 | Expired reference breaks traceability | [17025] 6.4, 6.5 (metrological traceability, calibrated equipment) | consistent |
| 7 | Interval is a decision (criticality, As-Found history, conditions, manufacturer, regulation) | [R3051] p66 "Calibration frequency can vary greatly depending on the application, performance requirements, and process conditions" | consistent |
| 8 | Calibration vs Trim vs Configuration vs Re-ranging; re-ranging does not touch the sensor | [R3051] p64: "Reranging does not change the factory sensor characterization curve"; analog output trim adjusts the D/A; sensor trim adjusts the sensor curve | confirmed |
| 9 | Chain: sensor → (zero/sensor trim) → PV → range → D/A (output trim) → DCS | [R3051] p64–65 (data flow: sensor → A/D [sensor trim] → micro → D/A [rerange, analog trim]); "a parameter change affects all values to the right of the changed parameter" | confirmed |
| 10 | Zero trim = true zero, fully vented; sensor trim = low then high reference; D/A trim = output 4 and 20 mA, enter measured; scaled D/A in another unit | [R3051] p69–72: zero trim "single-point offset … vent the transmitter"; sensor trim "two-point … Always adjust the low trim value first"; D/A trim steps 4–7; scaled D/A "user selectable reference scale other than 4 and 20 mA" | confirmed |
| 11 | Order: sensor/zero trim first, then D/A trim | [R3051] p65 (data flows left to right; a change affects everything to its right); Table 4-1 field tasks: zero trim, then optional analog output trim | confirmed |
| 12 | Before HART writes set loop to manual, etc. | [R3051] p69, p72 ("Select OK after setting the control loop to manual") | confirmed |
| 13 | Error patterns and the corrected example (+0.37 … −0.30) | least-squares fit in `pt_cal_data.py`: slope −0.68 % over the span, intercept +0.376 %, residuals ≤ 0.014 % → linear (zero + span) | confirmed |
| 14 | Hysteresis is not fixed by trimming | Beamex hysteresis blog ("cannot be completely eliminated, it can be managed") | consistent |
