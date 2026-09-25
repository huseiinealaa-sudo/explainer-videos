# Episode 1 — Proving principle and the MF equation: sources

Format: claim → source → note. Priority per CLAUDE.md (1 manufacturer, 2 API, 3 papers, 4 industry training).

## Verified claims

| # | Claim | Source | Note |
|---|---|---|---|
| 1 | Proving compares the meter reading with a known reference volume from the prover; the result is a meter factor applied to the meter's indicated volume. | [NIST, "Series 1 – Small Volume Provers: Identification, Terminology and Definitions" (2005), citing NIST HB 105-7](https://www.nist.gov/system/files/documents/2017/05/09/H-003.pdf) · [H. James, "Liquid Meter Proving Techniques", NFOGM](https://nfogm.no/wp-content/uploads/2014/07/Liquid-Meter-Proving-Techniques.pdf) | NIST: "MF = corrected prover volume / registered meter volume". James: MF "can be applied to the meter indicated volume output", traceable to reference standards. |
| 2 | MF is a multiplier (correction factor) on the meter readout. | [Daniel Compact Prover O&M manual 3-9008-701 Rev J (2015), §1.2 p.2](https://ia601908.us.archive.org/28/items/manualsonline-id-766b67ae-05b0-48b4-8423-66d6598b4e1f/766b67ae-05b0-48b4-8423-66d6598b4e1f.pdf) | "Meter Factor: Correction factor (multiplier) for meter readout". Priority 1. |
| 3 | MF is the basis of accuracy in custody transfer. | [H. James, NFOGM](https://nfogm.no/wp-content/uploads/2014/07/Liquid-Meter-Proving-Techniques.pdf) · [Coastal Flow, "Understanding Liquid Meter Provings and Proving Reports" (L. McCombs)](https://coastalflow.com/wp-content/uploads/2021/07/Understanding-Liquid-Meter-Provings.pdf) | Both describe proving of custody meters; Emerson's application note "Troubleshooting Custody Transfer Meter Factor Shifts" is on the same topic (PDF could not be downloaded from this session). |
| 4 | Meter and prover are connected in series; the volume swept by the displacer between the detectors equals the volume through the meter in the same interval. | [NIST Series 1, "Pipe prover"](https://www.nist.gov/system/files/documents/2017/05/09/H-003.pdf) | Direct statement. |
| 5 | The piston passes between two detectors; the volume between them is the base volume. On the Daniel compact prover the detectors are slotted optical switches triggered by a flag on the detector shaft. | [Daniel manual §1.3 pp.2–3](https://ia601908.us.archive.org/28/items/manualsonline-id-766b67ae-05b0-48b4-8423-66d6598b4e1f/766b67ae-05b0-48b4-8423-66d6598b4e1f.pdf) | "The passage of the flag through the slotted optical switches defines the displaced volume (base volume)". D1/D2 are our labels. |
| 6 | Base volume is certified by waterdraw; it is referred to 0 psig and the reference temperature. | [Daniel manual §2.3 p.23](https://ia601908.us.archive.org/28/items/manualsonline-id-766b67ae-05b0-48b4-8423-66d6598b4e1f/766b67ae-05b0-48b4-8423-66d6598b4e1f.pdf) | "certified at the factory using the volumetric displacement method (water draw) per API guidelines". |
| 7 | The flow computer counts meter pulses during the pass; the compact prover requires a computer capable of dual chronometry pulse interpolation (fraction of a pulse to 1 part in 10,000). | [Daniel manual §1.1 p.1, §2.2 pp.16–17](https://ia601908.us.archive.org/28/items/manualsonline-id-766b67ae-05b0-48b4-8423-66d6598b4e1f/766b67ae-05b0-48b4-8423-66d6598b4e1f.pdf) · [NIST Series 1](https://www.nist.gov/system/files/documents/2017/05/09/H-003.pdf) | NIST: small volume provers "can be used with less than 10,000 pulses; however, these provers use pulse interpolation". |
| 8 | MF = (BPV·CTSp·CPSp·CTLp·CPLp) / (IV·CTLm·CPLm), IV = pulses / K-factor. CTSp/CPSp: temperature/pressure effect on the prover steel; CTLp/CPLp: temperature/pressure effect on the liquid in the prover; CTLm/CPLm: on the liquid at the meter. | [Emerson ROC800L Flow Calculations User Manual D301688X012 (2017), ch. 6 pp.27–31](https://www.emerson.com/documents/automation/roc800l-flow-calculations-user-manual-en-132294.pdf) | Implements API MPMS Ch. 12.2: GSVp = BV·CCFp, CCFp = CTSp·CPSp·CTLp·CPLp; ISVm = (pulses/K-factor)·CCFm, CCFm = CTLm·CPLm; MF = GSVp/ISVm. "Pulse count … (whole or interpolated)". |
| 9 | MF < 1 → meter reads high (registers more than the true volume); MF > 1 → reads low. | [Coastal Flow training paper, p.3](https://coastalflow.com/wp-content/uploads/2021/07/Understanding-Liquid-Meter-Provings.pdf) | "a meter factor greater than 1 would mean that the flow meter is reading low. Conversely, if the meter factor is less than 1, the meter would be measuring high." Also follows directly from NIST's ratio. |
| 10 | Proven K-factor = nominal K / MF (the same correction expressed as pulses per unit volume). | [NIST Series 1, "K-factor"](https://www.nist.gov/system/files/documents/2017/05/09/H-003.pdf) · `scripts/prover_demo_data.py` | NIST: K-factor = meter pulses / corrected prover volume. Dividing by MF gives the same number. |
| 11 | Apply either the proven K or the MF, not both: applying both corrects the reading twice. | Derived from the identity in #10 (owner decision 2) | Background only: [Blue Chip MRC, "Meter factors"](https://bluechipmrc.com/measurement/meter-factors/) says the k-factor "can then be adjusted in lieu of the meter factor". Not cited in the narration. |

## Demo numbers used (from scripts/prover_demo_data.py only)
- Average MF = 0.99900 → spoken "0.999"; deviation ≈ 0.1 % over-registration.
- Final K = 60060.060 pls/m³ → spoken "about 60,060".
- Nominal K = 60000 pls/m³.

## Conflicts / open questions — owner decisions (2026-09-25)
1. **Inverted MF wording.** [Flow Management Devices, J. Lantzy, "Proving for Measurement Verification" (2025)](https://flowmd.com/wp-content/uploads/2025/06/Proving-for-Measurement-Verification-06-25-c.pdf) says MF "is the metered volume divided by the prover volume"; NIST, the Emerson ROC800L manual (API 12.2) and Coastal Flow say prover ÷ meter.
   **Decision:** follow the majority and API MPMS 12.2: MF = corrected prover volume ÷ corrected meter volume.
2. **"K or MF, not both."** Only a priority-4 source (Blue Chip MRC) was found.
   **Decision:** keep it as a derived statement ("applying both corrects the reading twice"), not attributed to any source.
3. **Pulse count vs. the 10,000 rule.** Demo data gives ≈14,796 pulses per pass (above 10,000).
   **Decision:** keep the wording "the manufacturer requires pulse interpolation"; do not show the pulse count as "too few".

## Note for episode 2
- Coriolis mass vs. volumetric proving: resolved by the owner, see `sources/prover_ep02.md`.
