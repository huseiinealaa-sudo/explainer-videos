# Episode 4 — Operating cycle (5 stages) and why flow never stops: sources

Format: claim → source → note. Priority per CLAUDE.md (1 manufacturer, 2 API, 3 papers, 4 industry training).

Main source (priority 1): [Daniel Compact Prover O&M manual 3-9008-701 Rev J, January 2015](https://ia601908.us.archive.org/28/items/manualsonline-id-766b67ae-05b0-48b4-8423-66d6598b4e1f/766b67ae-05b0-48b4-8423-66d6598b4e1f.pdf) — "manual" below. Page numbers are the printed manual pages.

## The five stages (official)
Manual §3.1 p.27 gives "The operational sequence of the compact prover" as five numbered steps, each with a figure (pp.28–30).

| # | Stage (figure title) | Narration term | Ref |
|---|---|---|---|
| 1 | Standby position | وَضْعُ الانْتِظَارِ | §3.1 step 1; Fig. 3-1 p.28 |
| 2 | Initial motion | بَدْءُ الحَرَكَةِ | step 2; Fig. 3-2 p.28 |
| 3 | Proving | الإِثْبَاتُ (الشَّوْطُ) | step 3; Fig. 3-3 p.29 |
| 4 | End of proving run | نِهَايَةُ الشَّوْطِ | step 4; Fig. 3-4 p.29 |
| 5 | Piston returning to upstream position | عَوْدَةُ المِكْبَسِ | step 5; Fig. 3-5 p.30 |

## Owner decisions (2026-09-25)
1. **"End of proving run" = end of the pass.** The manual's figure title says "run", but step 5 ends with "The prover is now ready to begin another pass". **Decision:** the narration says «نِهَايَةُ الشَّوْطِ» (series terminology: pass = الشوط, run = الجولة).
2. **Stage 3 name.** **Decision:** «الإِثْبَاتُ (الشَّوْطُ)», consistent with episode 1 (proving = إثبات), not «المعايرة».
3. **Scope.** No double chronometry, plenum pressure formula/R or CTSp (episode 5).

## Verified claims (narration)

| # | Claim | Source | Note |
|---|---|---|---|
| 1 | Standby: piston upstream, poppet open, held by hydraulic pressure on the actuator piston; liquid passes through the open poppet. | manual §3.1 step 1 p.27; §1.3 p.2 | "Normal flow of the liquid will pass through the open poppet valve." |
| 2 | [+] The prover stays in standby until the computer sends the RUN command. | manual §5.2 p.74, Fig. 5-1 t1/t8 | "Compact prover remains in this condition until RUN command is received from computer." |
| 3 | Initial motion: the hydraulic control valve opens and releases the hydraulic pressure; plenum pressure on the actuator piston closes the poppet; the piston moves downstream at the process flow rate. | manual §3.1 step 2 p.27 | Direct statement. |
| 4 | Proving (the pass): the flag on the piston trips the volume switches; the signals go to the computer instantly; between them the piston displaces the base volume while meter pulses are counted. | manual §3.1 step 3 p.27; §1.3 pp.2–3 | Pulse counting between the switches: episodes 1–2 (sources/prover_ep01.md #5, #7). How the computer times the pulses is left for episode 5. |
| 5 | In our example the pass takes about 3.5 s. | `scripts/prover_demo_data.py` (PASS_TIME = 3.547 s) | Spoken as "about three and a half seconds". |
| 6 | End of the pass: at the second volume switch the control valve closes, hydraulic pressure builds and pushes the actuator piston upstream, opening the poppet; liquid again flows through the piston. | manual §3.1 step 4 p.27 | Direct statement (owner decision 1: "end of the pass"). |
| 7 | Return: actuator piston, measurement piston, poppet, actuator shaft, detector shaft and flag return to standby; the pump then holds pressure; ready for another pass. | manual §3.1 step 5 p.27 | Direct statement. |
| 8 | [+] The computer ignores the switch signals during the return stroke. | manual §5.2 p.74, Fig. 5-1 t6/t7 | "Computer ignores pulses during return stroke." |
| 9 | In our data the cycle repeats 3 times per run. | `scripts/prover_demo_data.py` (PASSES_PER_RUN = 3) | Series terminology: pass = الشوط, run = الجولة. |
| 10 | Flow never stops: through the open poppet in standby/return; during the pass the piston moves with the liquid. | manual §1.2 p.1; §1.3 p.2; §3.1 p.27 | "continuous flow for … proving … in an operational line"; "operated with minimal disturbance to flow". |
| 11 | [+] A properly adjusted plenum keeps the pressure differential across the piston very small, a few inches of water column. | manual §1.3 p.3 | "When properly adjusted, this charge allows for minimum pressure differential (usually only a few inches of water column) across the piston." The formula stays in episode 5. |
| 12 | [+] Fail-safe: the positive stop in the outlet flange prevents accidental blockage of the flow. | manual §1.2 p.1; §3.1 p.27 | "inherent fail-safe feature constructed to assure uninterrupted liquid flow"; "positive stop … prevents any accidental blockage of the process flow stream". |
| 13 | So the meter is proved in service without shutting the line. | manual §1.2 p.1 | "proving of liquid flow meters in an operational line … with minimal disturbance to flow". |

## Left out
- The Emerson data sheet summary says "without interrupting normal flow and without the use of manually operated bypass valves". The PDF could not be opened from this session, so the claim is not used.
- The double-block-and-bleed diversion before proving (manual §2.1, §3.2 step 7) belongs to operating procedure, not to the cycle.

## Numbers used (from scripts/prover_demo_data.py only)
- `len(CYCLE_STAGES)` = 5; `PASS_TIME` = 3.547 s (spoken "about 3.5 s"); `PASSES_PER_RUN` = 3.
