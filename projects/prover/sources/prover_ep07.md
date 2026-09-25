# Episode 7 — Auditing the proving report, recomputing one run: sources (research draft)

Format: claim → source → note. Priority per CLAUDE.md (1 manufacturer, 2 API, 3 papers, 4 industry training).
Status: narration approved by the owner (2026-09-25); owner decisions below. API MPMS 4.8, 12.2 and 13.2 are paywalled:
only their official tables of contents / publisher summaries were read, so no numeric limit is attributed to API
unless a secondary source quotes it.

Main sources:
- [API MPMS Ch. 4.8, 2nd ed. (2013), official preview (contents)](https://www.api.org/~/media/files/publications/whats%20new/4_8%20e2%20pa) — "API 4.8 preview" (priority 2).
- [API MPMS 12.2.3 "Proving Reports", publisher summary (GlobalSpec)](https://standards.globalspec.com/std/559270/api-mpms-12-2-3) — "12.2.3 summary" (priority 2).
- [Emerson ROC800L Flow Calculations User Manual D301688X012 (2017), ch. 6 pp.27–35](https://www.emerson.com/documents/automation/roc800l-flow-calculations-user-manual-en-132294.pdf) — "ROC800L manual" (priority 1).
- [43 CFR 3174.11, Meter-proving requirements (US BLM regulation)](https://www.law.cornell.edu/cfr/text/43/3174.11) — "43 CFR" (official regulation citing API).
- [Buttler (Emerson), FLOMEKO 2019](https://www.imeko.org/publications/tc9-2019/IMEKO-TC9-2019-042.pdf) (priority 3).
- [H. James, "Liquid Meter Proving Techniques", NFOGM](https://nfogm.no/wp-content/uploads/2014/07/Liquid-Meter-Proving-Techniques.pdf) (priority 3/4).
- [Coastal Flow, L. McCombs, "Understanding Liquid Meter Provings and Proving Reports"](https://coastalflow.com/wp-content/uploads/2021/07/Understanding-Liquid-Meter-Provings.pdf) — "Coastal" (priority 4).

## Owner decisions (2026-09-25)
1. **Rounding:** full precision (run 1 MF = 0.99900, as in the report); keep the rounding sentence in segment 10.
2. **MF shift 0.25 %:** worded as a common practice whose limit the operator or contract sets, not an API requirement (`MF_SHIFT_COMMON` in prover_demo_data.py).
3. **Conflicts 3 and 4:** handled as proposed (no side taken on pass/fail strictness; Table 54B named by group and edition only).

## Candidate claims

| # | Claim | Source | Note |
|---|---|---|---|
| 1 | [+] The purpose of the proving report is to hold enough information to recalculate the meter factor at any time after the proving; it identifies the prover and its volume and the meter. | Coastal p.3 ("The goal of the report is to document and provide the information necessary to recalculate the meter factor any time after the proving"), p.7 | Coastal also says "and the location of the meter"; left out (site data is never shown). |
| 2 | [+] API 4.8 has a section "Assessment of Proving Results" (number of runs, meter factor, application of meter factors), a subsection "Temperature and Pressure Variations", a normative Annex A "Evaluating Meter Proving Data" and an informative Annex D "Proving Form Examples". | API 4.8 preview, contents pp. v–vi | Used only to frame the audit; no numbers taken from it. |
| 3 | The configuration checksum: a change raises the CONF CSUM alarm, so the report CSUM is compared with the approved one. | Episode 6 sources #7 (Config600 manual §9.1.4) | Links to episode 6. Demo: DEMO_PRV_CFG / a1b2. |
| 4 | [+] A report lists the base prover volume and its certification (waterdraw) date among the prover data. | Coastal p.2 "Prover Information: Base Prover Volume, Certification Date …" | Our demo has no certificate date (site data); the narration says only "matches the valid waterdraw certificate". |
| 5 | Downstream volume 0.2463 m³ applies because the meter is downstream of the prover. | Episode 5 (owner decision), `prover_demo_data.BPV_DOWNSTREAM` | Links to episode 5. |
| 6 | [+] A temperature (or pressure) difference between prover and meter is acceptable, but it should stay consistent run to run and prove to prove; variations prove to prove are one of the most common reasons for meter factor shifts. | Coastal p.4 | Demo: 30.0 vs 29.9 °C → 0.1 °C. Pressures: the demo data has only CPLp / CPLm (no pressures), so the narration checks the factors, not pressures. |
| 7 | Table 54B (1980, SI): ρ15 = 840.0 kg/m³ lies in the Fuel oils group (838.5 ≤ ρ < 1075); constants are per °C, not the per-°F constants of Tables 6B / 2004. | `prover_demo_data.TABLE_54B_GROUPS` (series data, PR #4) | Not re-verified against a public copy of the 1980 tables in this session (conflict 4). |
| 8 | Repeatability 0.03 % for 5 runs, within the 0.05 % limit (API 4.8 Annex A via secondary sources). | Episode 2 sources #6–7 | Links to episode 2. |
| 9 | [+] The new meter factor is compared with the previous one; a commonly used allowance is ±0.0025 (0.25 %) for volume proves; the tolerance is set by the user / contract; if exceeded, the cause is investigated. | Coastal p.3 ("A typical meter or contract allowance is +/- 0.0025 shift for volume, while +/- 0.0050 for mass proves. Variance tolerances are a user defined …") · James (NFOGM) p.3 ("Failure to achieve a factor within 0.25% of the previous proving without a defendable reason" as a commonly accepted rejection criterion) · 43 CFR 3174.11(e)(1) ("If the difference between meter factors established in two successive provings exceeds ±0.0025, the meter must be immediately removed from service") · Buttler p.2 ("an uncharacteristically large shift in the average MF compared to the last proving … the meter should be thoroughly inspected") | Conflict 2: not found in the API text we could read; worded as "common practice". The demo has no previous MF, so no example number is shown. |
| 10 | [+] Tracking meter factors on a chart shows gradual changes, seasonal shifts and meter failure. | James (NFOGM) p.3 ("Track and chart your meter factors … Gradual changes, Seasonal shifts … Meter failure") · Coastal p.7 · API MPMS 13.2 scope ([Ambrit summary](https://www.ambrit.com/api-13-2-statistical-methods-of-evaluating-meter-proving-data/): 13.2 evaluates meter performance where MFs are developed per API 12.2) | |
| 11 | [+] The meter factor must be computed in the sequence of API 12.2.3, which specifies the equations, the calculation sequence, discrimination levels and rounding rules. | 43 CFR 3174.11(c)(5) ("Meter factor computations must follow the sequence described in API 12.2.3") · 12.2.3 summary | |
| 12 | GSVp = BPV × CTSp × CPSp × CTLp × CPLp; ISVm = pulses ÷ K × CTLm × CPLm; MF = GSVp ÷ ISVm (pulses whole or interpolated). | ROC800L manual §6.1–6.3 pp.27–31 · episode 1 sources #8 | Links to episode 1. |
| 13 | [+] Flow computers round each correction factor and volume to fixed decimals before combining them (e.g. ROC800L: CTL, CPL, CTS, CPS, CCF to 5 decimals; volumes in m³ to 6 decimals; run MF to 5 decimals; final MF to 4), so a hand recalculation must use the same rounding as the report. | ROC800L manual Tables 6-2 to 6-10 pp.28–33 ("The interim correction factors are rounded before the combined correction factors are calculated") | Conflict 1. |

## Recalculation of run 1 (all values from projects/prover/prover_demo_data.py)
| Step | Value | Episode |
|---|---|---|
| BPV (downstream) | 0.2463 m³ | 5 |
| CTSp = [1 + 15 × 0.0000216] × 1 | 1.000324 | 5 |
| CPSp | 1.000000 | 1 |
| CTLp (54B, Fuel oils, 30.0 °C) | 0.987296 | 7 |
| CPLp | 1.000150 | 1 |
| Corrected prover volume | 0.243286 m³ | 1 |
| Interpolated pulses (run 1) | 14796.164 | 5 |
| IV = pulses ÷ 60000 | 0.246603 m³ | 1 |
| CTLm (29.9 °C) × CPLm | 0.987381 × 1.000160 | 7 |
| Corrected meter volume | 0.243530 m³ | 1 |
| MF = 0.243286 ÷ 0.243530 | 0.99900 | 1 |

## Conflicts found (to show the owner)
1. **Rounding.** The series computes in full precision (report MF run 1 = 0.99900). With ROC800L-style rounding (factors to 5 decimals, volumes to 6) run 1 gives CCFp 0.98776, CCFm 0.98754, GSVp 0.243285, ISVm 0.243530 → MF 0.99899; the average stays 0.99899 → final MF (4 dp) 0.9990. API 12.2.3 itself (paywalled) could not be read, and the S600+ rounding rules were not found. Proposal: keep the full-precision chain (matches episodes 1–6 and the report) and add one sentence that computers round by fixed rules, so the auditor uses the same rules and the last digit may differ.
2. **MF shift limit 0.25 %.** Found in industry papers and a US regulation, not in API text we could read; Coastal says the tolerance is user/contract defined, 43 CFR makes it a mandatory ±0.0025. Proposal: say "common practice … each operator or contract sets its limit".
3. **Pass/fail strictness.** Coastal p.3: failing the uncertainty target "is not an absolute pass or fail" if the MF is close to the previous one; 43 CFR and Buttler (episode 2) treat failed repeatability as a re-prove. Our demo passes, so the narration does not take a side.
4. **Table 54B constants.** Not re-verified against a public copy in this session; they are the series values used since episode 1 (PR #4). Narration names the group and edition only.
