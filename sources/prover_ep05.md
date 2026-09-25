# Episode 5 — Double chronometry, plenum pressure, upstream/downstream volumes, CTSp: sources

Format: claim → source → note. Priority per CLAUDE.md (1 manufacturer, 2 API, 3 papers, 4 industry training).

Main source (priority 1): [Daniel Compact Prover O&M manual 3-9008-701 Rev J, January 2015](https://ia601908.us.archive.org/28/items/manualsonline-id-766b67ae-05b0-48b4-8423-66d6598b4e1f/766b67ae-05b0-48b4-8423-66d6598b4e1f.pdf) — "manual" below. Page numbers are the printed manual pages. The manual's equations are images; they were read from rendered pages.

Other sources:
- [Emerson ROC800L Flow Calculations User Manual D301688X012 (2017)](https://www.emerson.com/documents/automation/roc800l-flow-calculations-user-manual-en-132294.pdf) — priority 1, implements API MPMS 12.2 ("ROC800L" below).
- [NIST Handbook 105-7, Specifications and Tolerances for Dynamic Small Volume Provers (1996)](https://www.nist.gov/system/files/documents/pml/wmd/105-7-2.pdf) — priority 2 (official).
- [Smith Meter Technical Paper TP02006 Rev 0.1 (5/09), "Utilizing the Smith Meter UPC Compensator with Helical Rotor Turbine Meters"](https://kb.guidantmeasurement.com/MS-Tech/TP02006.pdf) — priority 1 (manufacturer), cites API MPMS 4.6.
- [API MPMS 4.6 Pulse Interpolation, GlobalSpec summary](https://standards.globalspec.com/std/14474038/MPMS%204.6) — priority 2 (official summary).
- [US patent 11709090 (Emerson/Daniel), "Technique to identify anomaly amongst base prover volumes"](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11709090) — quotes the API 12.2 CTSp form for externally mounted detectors (supporting only).

## Mandatory verification results (reported to the owner before writing)
1. **CTSp includes an Invar term.** Manual §4.3.2 pp.50–51 (water draw factor Css) divides by `[1 + (Tp − Tb)·Eft] · [1 + (Td − Tb)·Eir]`: flow tube (Eft, the "squared" = area coefficient; 0.0000216 /°C in the manual's table) and Invar rods (Eir = 0.00000144 /°C). ROC800L §6.1.1 pp.28–29 gives the proving form for small volume provers with external detector switches: `CTSp = [1 + (Tp − Tcal)·Y1] × [1 + (Td − Tcal)·Y2]`, Td = temperature of the displacer (detector) shaft. The old demo value 1.000324 was the tube term alone.
2. **Plenum formula verified**: manual §3.2 step 3 p.30 + Table 3-1 p.31: `Plenum Pressure = Pipeline Gauge (psig) / R + 60 psig`.
3. **Upstream/downstream volumes**: manual §1.4 p.7 ("Volume Ratio (Upstream/Downstream Volume)") and Table 1-2 p.8 (24": 0.992369; 0.993464 pre-2006).
4. **Double chronometry**: manual §2.2.2 pp.16–17, Fig. 2-2.

## Owner decisions (2026-09-25)
1. **CTSp — option (a).** Keep the published values of episodes 1–4. `T_DETECTOR = 15.0 °C` was added, so the Invar term equals exactly 1 and CTSp stays 1.000324. The episode shows the full two-term equation and says the example rods are at 15 °C, which does not always hold in the field. The tube coefficient 0.0000216 is an area coefficient (2 × 0.0000108 linear).
2. **Volumes.** BPV 0.2463 m³ is the downstream volume (our meter is downstream of the prover). Upstream = 0.2463 × 0.992369 = 0.244420 m³ (post-2006 ratio, same era as R = 5).
3. **Why they differ.** Use NIST's general wording (a shaft on one side of the displacer); do not name the shaft or explain which side is larger beyond the numbers.
4. **Chronometry example** (one illustrative pass of run 1): A = PASS_TIME = 3.546720 s, C = 14796, B = A·C/N = 3.546681 s, interpolated N = 14796.164.
5. **Terminology.** Narration: حَجْمُ أَعْلَى المَجْرَى (upstream) / حَجْمُ أَسْفَلِ المَجْرَى (downstream); on screen "Upstream" / "Downstream". Not "front/back" (الأمامي/الخلفي), because episodes 3–4 draw FRONT = outlet (downstream) and BACK = inlet (upstream). Recorded in CLAUDE.md.
6. **Narration approved as trimmed** (347 words, ≈ 3.5 min). The sentences cut for length are listed under "Left out" and are not to be restored.

## Verified claims (narration)

| # | Claim | Source | Note |
|---|---|---|---|
| 1 | A pass does not contain a whole number of meter pulses: the flag can trip a switch at any moment between two pulses. | manual Fig. 2-2 p.17 | The figure shows the switch edges falling between pulse edges. |
| 2 | [+] Simple counting has an uncertainty of up to ±1 pulse per pass; 10,000 whole pulses keep it within ±0.01 %. | Smith Meter TP02006 p.1–2 | "the ±1 count maximum uncertainty of each proving pass"; "±1 count (i.e., ±0.01% for 10,000 counts)". |
| 3 | [+] Double chronometry is used mostly in small volume provers, and in pipe provers when 10,000 pulses cannot be achieved. | API MPMS 4.6 summary (GlobalSpec); NIST H-003 (ep01 #7) | "most widely used in small volume provers". |
| 4 | The computer needs a master oscillator counting time in 0.000001 s; it runs two timers, A and B. | manual §2.2.2 p.16 | Direct statement. |
| 5 | Time A: first detector switch → final detector switch. Time B: leading edge of the first meter pulse after A starts → leading edge of the first pulse after A stops. C = whole pulses. | manual §2.2.2 p.16, Fig. 2-2 | Direct statement. |
| 6 | Interpolated pulses = C × A / B, to 1 part in 10,000 of a pulse. | manual §2.2.2 p.16 | Manual: K = (A/B)·C/D; C·A/B is the interpolated pulse count. |
| 7 | Example: C = 14,796; A and B differ by about 39 µs; the fraction added is 0.164 pulse. | `prover_demo_data.py` (CHRONO_*) | Derived, not a site value. |
| 8 | [+] The plenum is charged with dry nitrogen. | manual §3.2 step 3 p.30 | Direct statement. |
| 9 | Plenum pressure = line gauge (psig) / R + 60 psig; R is a known constant per prover size. | manual §3.2 step 3 p.30 | Direct statement. |
| 10 | [+] R = 5 for the 24-inch prover; 5.88 if shipped before 1 January 2006. | manual Table 3-1 p.31 | Footnote on the 24" row. |
| 11 | [+] 60 psig applies to horizontal installation; 40 psig replaces it for a vertical one. | manual §3.2 note 2 p.32 | Direct statement. |
| 12 | Example: 40 / 5 + 60 = 68 psig. | `prover_demo_data.py` (PLENUM_PRESSURE) | |
| 13 | [+] Guideline: 0 to +5 % above the calculated value, i.e. 68 to 71.4 psig. | manual §3.2 p.32 note 1 | 71.4 = PLENUM_MAX. |
| 14 | [+] A prover with a single shaft attached to only one side of the displacer has different upstream and downstream volumes; both are calibrated. | NIST HB 105-7 §7.3.1 | "the two volumes will differ". Owner decision 3. |
| 15 | Both volumes are calibrated; the ratio for the 24" prover is 0.992369 (on screen). | manual §2.3 p.23; §4.2.1 p.37; Table 1-2 p.8 | |
| 16 | The downstream volume is used when the meter is downstream of the prover; the upstream volume when it is upstream. | manual §2.3 p.23; §4.3.2 p.52 | "Enter the downstream base volume … if the meter under test is located downstream of the prover." |
| 17 | Example: downstream = BPV = 0.2463 m³; upstream = 0.24442 m³. | `prover_demo_data.py` (BPV_*) | Owner decision 2. |
| 18 | Entering the wrong volume would shift the factor by about three quarters of a percent. | derived: 1 − 0.992369 = 0.763 % | Derived statement, not attributed to a source. |
| 19 | On a small volume prover the detectors are outside the flow tube on Invar rods, so CTSp has two multiplied terms: flow tube and rods. | ROC800L §6.1.1; manual §4.3.1 item 5 p.49, §4.3.2 pp.50–51 | "Td … temperature of the Invar Rods used for spacing the optical switches." |
| 20 | Tube term uses an area (squared) coefficient, twice the linear one, because the cross-section expands in two dimensions. | manual p.50 ("squared coefficient") and table p.51 | 0.0000216 = 2 × 0.0000108 (owner decision 1). |
| 21 | Rod term uses the rods' temperature and linear coefficient, because the rods set the distance between the switches. | manual pp.49, 51; ROC800L §6.1.1 | Eir = 0.00000144 /°C. |
| 23 | [+] In the water draw the manual allows the ambient temperature to be used for Td. | manual §4.3.1 item 5 p.49 | "As an option, ambient temperature may be used." Stated for the water draw only. |
| 24 | Example: Tp = 30 °C → tube term 1.000324; Td = 15 °C → rod term 1; CTSp = 1.000324 (on screen). In the field the rod term is not always 1. | `prover_demo_data.py` (CTSP_*) | Owner decision 1. |

## Left out
- Cut for length (owner decision 6, do not restore): "without interpolation one pulse is ≈ 0.007 % here"; "vent the excess plenum pressure or charge from the supply bottle" (manual §3.2 p.32); "the Invar linear coefficient is 7.5 times smaller than the tube's" (derived); "CTSp raises the prover volume by ≈ 3 parts in 10,000" (derived); "1 part in 10,000 of a pulse" is kept on screen only (manual §2.2.2).
- Tcal vs Tb naming: the ROC800L uses "calibration temperature", the manual "reference temperature"; the narration says "base temperature, 15 °C in our example".
- Flow tube steel grade (series rule): the coefficient is shown only as a number.
- Automatic plenum adjustment panel (manual §2.2.4) — equipment option, not needed for the formula.

## Numbers used (from scripts/prover_demo_data.py only)
- CHRONO_TIME_A = 3.546720 s, CHRONO_TIME_B = 3.546681 s, CHRONO_WHOLE = 14796, CHRONO_PULSES = 14796.164.
- PLENUM_LINE_PRESSURE = 40, PLENUM_RATIO = 5, PLENUM_PRESSURE = 68, PLENUM_MAX = 71.4 psig.
- VOLUME_RATIO = 0.992369, BPV_DOWNSTREAM = 0.2463 m³, BPV_UPSTREAM = 0.244420 m³.
- GC_STEEL = 0.0000216, GL_INVAR = 0.00000144, T_PROVER = 30, T_DETECTOR = 15, CTSP_TUBE = 1.000324, CTSP_INVAR = 1, CTSP = 1.000324.
