# pt_cal_ep06_trim — research notes (trim and error patterns)

Sources as in `pt_cal_ep05_verdict.md` ([R3051] Rosemount 3051 Reference Manual 00809-0100-4001 Rev KA; Beamex hysteresis blog).

| # | Claim | Source | Result |
|---|---|---|---|
| 8 | Calibration vs Trim vs Configuration vs Re-ranging; re-ranging does not touch the sensor | [R3051] p64: "Reranging does not change the factory sensor characterization curve"; analog output trim adjusts the D/A; sensor trim adjusts the sensor curve | confirmed |
| 9 | Chain: sensor → (zero/sensor trim) → PV → range → D/A (output trim) → DCS | [R3051] p64–65 (data flow: sensor → A/D [sensor trim] → micro → D/A [rerange, analog trim]); "a parameter change affects all values to the right of the changed parameter" | confirmed |
| 10 | Zero trim = true zero, fully vented; sensor trim = low then high reference; D/A trim = output 4 and 20 mA, enter measured; scaled D/A in another unit | [R3051] p69–72: zero trim "single-point offset … vent the transmitter"; sensor trim "two-point … Always adjust the low trim value first"; D/A trim steps 4–7; scaled D/A "user selectable reference scale other than 4 and 20 mA" | confirmed |
| 11 | Order: sensor/zero trim first, then D/A trim | [R3051] p65 (data flows left to right; a change affects everything to its right); Table 4-1 field tasks: zero trim, then optional analog output trim | confirmed |
| 12 | Before HART writes set loop to manual, etc. | [R3051] p69, p72 ("Select OK after setting the control loop to manual") | confirmed |
| 13 | Error patterns and the corrected example (+0.37 … −0.30) | least-squares fit in `pt_cal_data.py`: slope −0.68 % over the span, intercept +0.376 %, residuals ≤ 0.014 % → linear (zero + span) | confirmed |
| 14 | Hysteresis is not fixed by trimming | Beamex hysteresis blog ("cannot be completely eliminated, it can be managed") | consistent |

| 15 | On-screen remedies of the five patterns (seg 4): offset → zero trim; slope → zero + span trim; linearity → multi-point trim if the transmitter supports it, else replace; hysteresis → trim cannot fix, watch it; repeatability → most serious, candidate for replacement | owner's cleaned source §5 («قراءة نمط الأخطاء»), verbatim meaning | shown as the owner's text |
