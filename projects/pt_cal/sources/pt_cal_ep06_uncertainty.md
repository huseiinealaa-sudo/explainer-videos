# pt_cal_ep06_uncertainty — research notes (claim → source → note)

Sources: **[GUM]** JCGM 100:2008, Evaluation of measurement data — Guide to the expression of uncertainty
in measurement — https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf ; **[17025]** ISO/IEC 17025:2017;
**[MC6-BR]** MC6 brochure p12 (module accuracy and 1-year uncertainty, k = 2).

| # | Claim | Source | Result |
|---|---|---|---|
| 1 | Error vs accuracy vs uncertainty | [GUM] 2.2, 3.3.1 (uncertainty = doubt about the result) | confirmed |
| 2 | E = 0.48 %, U = 0.10 % → 0.38 … 0.58 % | `DEMO_LO`, `DEMO_HI` | confirmed |
| 3 | 0.5 % of reading at 10 % of span = 0.05 % of span | `RDG_AS_SPAN_PCT` | confirmed |
| 4 | TUR = tolerance / expanded uncertainty; 4:1 industry minimum | common industrial practice (e.g. ANSI/NCSL Z540.3 handbook) — not a GUM term | kept as the owner's practice; grades (≥10, 4–10, 2–4, <2) are the owner's |
| 5 | Rectangular u = a/√3 | [GUM] 4.3.7 | confirmed |
| 6 | Resolution u = d/(2√3) | [GUM] F.2.2.1 (half-width d/2, rectangular) | confirmed |
| 7 | Repeatability u = standard deviation (Type A) | [GUM] 4.2 | confirmed (for a single reading) |
| 8 | u_c = √Σu², U = k·u_c, k = 2 ≈ 95 % | [GUM] 5.1.2, 6.2.1, 6.3.3 | confirmed |
| 9 | Worked budget: u_c ≈ 0.01550, U ≈ 0.03099 kg/cm² (0.0738 %), TUR ≈ 6.78 | `U_C`, `U_EXP`, `U_EXP_PCT`, `TUR` | confirmed |
| 10 | **"Largest three: reference, repeatability, pressure stability"** | `BUDGET_RANKED`: reference 0.00883, repeatability 0.00800, **current 0.00751**, stability 0.00577 | **conflict with the data**: with the owner's inputs the third is the current measurement; stability is fourth. Halving stability: U 0.03099 → 0.02933 kg/cm², TUR 6.78 → 7.16 (a real but modest gain, not "halved") |
| 11 | "Seven contributions" incl. drift of the reference since its last calibration | the owner's budget has six inputs | note: the MC6 module's 1-year uncertainty "includes … typical long term stability for mentioned period" ([MC6-BR] p12 note 2), so drift sits inside the reference term of the example; narration says so |
| 12 | Guard band: PASS if \|E\| + U ≤ tol; FAIL if \|E\| − U > tol; between = zone of doubt | [17025] 7.8.6 + ILAC-G8:09/2019 (guarded acceptance) | consistent |
| 13 | 0.3714 + 0.0738 = 0.4452 % ≤ 0.50 % → PASS, margin 0.0548 % ≈ 11 % of tolerance | `GUARD_*` | confirmed |
| 14 | Certificate states U (k = 2) and the decision rule | [17025] 7.8.4.1, 7.8.6.2 | confirmed |
