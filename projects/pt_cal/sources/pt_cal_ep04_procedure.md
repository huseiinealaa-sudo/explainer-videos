# pt_cal_ep04_procedure — research notes (claim → source → note)

Sources: **[MC6-UM]** (ep01 notes); **[PGHH]**, **[PGM]**, **[PGC]**, **[PGHS]** (ep02 notes);
priority 2: Beamex blog — adiabatic process (https://blog.beamex.com/adiabatic-process-in-pressure-calibration),
hysteresis (https://blog.beamex.com/hysteresis-in-pressure-calibration), pressure gauges
(https://blog.beamex.com/how-to-calibrate-pressure-gauges).

| # | Claim | Source | Result |
|---|---|---|---|
| 1 | Ten steps, As-Found before any adjustment | owner's procedure; consistent with [R3051] p68 (compare first, then trim) | kept |
| 2 | Exercise: three full cycles 0 → 100 % → 0 | blog (gauges): "supply the nominal max pressure … vent … repeat this process 2-3 times" | consistent (2–3); owner's "three" kept |
| 3 | Golden rule: rising from below only, falling from above only | blog (hysteresis): "approach the increasing points from below, and not overshoot and come back down" | confirmed |
| 4 | Decay test: pump to 100 %, close the pump valve, Data Logger 1 s for 3 min, read the **shape** | [MC6-UM] p37, p125 (Data Logger); blog: "The pressure drop caused by the adiabatic process is first fast, but then slows down and eventually stabilizes … the pressure drop caused by a leak is linear" | confirmed. [MC6-UM] p166 also has a "Leak / Stability Test" tool (note only, not added) |
| 5 | Thermal: compressing air heats it; cooling lowers pressure without a leak; worse at high pressure | [PGM] p4 (PDF 7); blog ("the faster you change the pressure, the more the medium temperature will change") | confirmed |
| 6 | Thermal settles in 1–3 min | blog: "A minute or two should do the trick"; [PGC] p12: 30–60 s; [PGHH] p16: 2–5 min (hydraulic, with hose stretch) | consistent; illustrative curve settles ≈ 2 min (`THERM_TAU` = 30 s) |
| 7 | Leak points: quick connectors (O-rings), threaded adapters (PTFE tape), pump check valve, process connection | [PGHH] p16 (check seals 1, 2, 9); [PGM] p5 (check-valve seal) | consistent |
| 8 | Remedies: shorter hose, fewer adapters, wait 30–60 s, hydraulic for high pressure | [PGC] p12 (30–60 s); [PGHS] p16 | consistent |
| 9 | Acceptance settings "(check the menu names in the MC6 manual)": manual/automatic, max deviation 2–3 % of span, settle 30–60 s | [MC6-UM] p79–80: **Automatic Acceptance**, **Max. Point Deviation (% of span)**, **Stability** (input and output), **Point Delay** (s) | **names corrected** to the manual's; 2–3 % and 30–60 s are the owner's recommended values (not from the manual) |
| 10 | Wider window does not weaken accuracy: the actual input is recorded; Accept captures both at once | [MC6-UM] p80 ("the readings are saved"; input and output read together) | confirmed |
| 11 | Other mistakes: re-zero after changing mounting position | [R3051] p53, p71 ("zero trim … compensating for mounting position effects") | confirmed |
| 12 | Cold transmitter: wait 15–30 min | [PGHS] p16 gives 15–30 min for the pump/fluid to equalize; for the transmitter it is the owner's practice | kept |

## Illustrative decay curves (data module, not real measurements)
From 42 kg/cm², 181 readings (1 per second): thermal = 42 − 0.30·(1 − e^(−t/30 s)); leak = 42 − 0.10·t/60;
mixed = 42 − 0.20·(1 − e^(−t/25 s)) − 0.05·t/60. At 180 s thermal and leak both end near 41.70 kg/cm² —
chosen on purpose: the shape, not the amount, tells them apart.
