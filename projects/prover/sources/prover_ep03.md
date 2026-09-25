# Episode 3 — Compact prover construction (10 components): sources

Format: claim → source → note. Priority per CLAUDE.md (1 manufacturer, 2 API, 3 papers, 4 industry training).

Main source (priority 1): [Daniel Compact Prover O&M manual 3-9008-701 Rev J, January 2015](https://ia601908.us.archive.org/28/items/manualsonline-id-766b67ae-05b0-48b4-8423-66d6598b4e1f/766b67ae-05b0-48b4-8423-66d6598b4e1f.pdf) — "manual" below. Page numbers are the printed manual pages (PDF page = printed page + 14).

## Owner decisions (2026-09-25)
1. **Ten-component grouping.** The manual heads only 7 components in §1.3 (flow tube, end connections, hydraulic cylinder, optical assembly, hydraulic control valve, hydraulic pump, pneumatic spring plenum). The owner approved the 10-item list below; it adds the measurement piston, the poppet valve and the interface enclosure, which the manual names in §1.2–§1.3 and Fig. 1-1 without separate headings. **Decision:** the narration presents them as "the main components" and never says the manual divides the prover into ten.
2. **Flow tube steel grade.** The manual (§1.4 p.6) says "17-4 stainless steel flow tube with hard chrome plating". A search summary of the newer [Emerson data sheet PS-002517 Rev C (2023)](https://www.emerson.com/documents/automation/product-data-sheet-emerson-s-next-generation-compact-prover-en-7273482.pdf) (next-generation model) mentions 304L. The PDF could not be opened from this session. **Decision:** do not name the grade.
3. **Plenum.** The manual shows a "pneumatic spring plenum" tank and a "pneumatic spring chamber" in the actuator cylinder (Fig. 3-1 p.28). **Decision:** treat them as one component.
4. **Scope.** Episode 3 gives each component's function only. The cycle belongs to episode 4. The plenum formula, R, double chronometry and CTSp belong to episode 5.

## Component list and layout
Order: flange end (front) → hydraulic/optical end (back), per Fig. 1-1 p.4 and Fig. 3-1 p.28. The inlet and outlet flanges are on the same end. The inlet pipe runs under the flow tube to the back, and flow then passes through the flow tube from back to front to the outlet.

| # | Component | Manual ref |
|---|---|---|
| 1 | End connections (inlet/outlet flanges) | §1.3 p.2; positive stop §3.1 p.27 |
| 2 | Flow tube | §1.3 p.2 |
| 3 | Measurement piston + Rulon riders | §1.3 p.2; §4.4.1 pp.53, 55 |
| 4 | Poppet valve | §1.2 p.1; §1.3 p.2 |
| 5 | Pneumatic spring plenum | §1.3 p.3 |
| 6 | Hydraulic cylinder | §1.3 p.2 |
| 7 | Hydraulic control valve | §1.3 p.3 |
| 8 | Hydraulic pump & motor (+ reservoir) | §1.3 p.3; Fig. 3-1 p.28 |
| 9 | Optical assembly (+ Invar rods) | §1.3 pp.2–3; §4.3.1 p.49 |
| 10 | Interface enclosure | §1.2 p.1; Fig. 1-1 p.4 |

## Verified claims (narration)

| # | Claim | Source | Note |
|---|---|---|---|
| 1 | The inlet and outlet end connections install the prover in the line (ANSI B16.5 raised-face flanges). | manual §1.3 p.2 | "The inlet and outlet end connections for installing the compact prover in line…" |
| 2 | [+] A positive stop in the outlet flange gives fail-safe operation and prevents accidental blockage of the flow. | manual §3.1 p.27 | "A positive stop feature is incorporated into the outlet flange for fail safe operation. This prevents any accidental blockage of the process flow stream." |
| 3 | [+] The flow tube is stainless steel with a precision-machined, hard-chrome-plated bore; it contains the piston, poppet valve and fail-safe mechanism. | manual §1.3 p.2 | Steel grade omitted (decision 2). |
| 4 | The measurement piston is free-flowing and moves downstream at the process flow rate, displacing the base volume in each pass. | manual §1.3 p.2; §3.1 p.27 | "free flowing measurement piston"; "the piston begins moving downstream at the process fluid flow rate". |
| 5 | [+] The piston carries seals that stop liquid bypassing it (checked by the seal leak test) and Rulon riders. | manual §4.1 pp.35–36; §4.4.1 pp.53, 55 | The leak check verifies the "measurement piston seals". The riders are only named: no priority 1–3 source found for their function (search hits were a Stirling-engine patent and a compressor patent), so the narration does not state it. |
| 6 | The poppet valve is inside the piston. When it is open, liquid flows through the piston; when it is closed, the liquid pushes the piston. | manual §1.2 p.1; §1.3 p.2; §3.1 p.27 | "piston … includes an internal poppet valve"; "Normal flow of the liquid will pass through the open poppet valve"; plenum pressure "closes the poppet valve, allowing the piston to proceed through a proving pass". |
| 7 | The plenum's gas charge supplies the energy to close the poppet valve and overcome shaft-seal friction. | manual §1.3 p.3 | Direct statement. |
| 8 | [+] The plenum is charged with dry nitrogen. | manual §3.2 p.30 | "must be charged with dry nitrogen for proper operation". Pressure value and formula left for episode 5. |
| 9 | The hydraulic cylinder's actuator piston is a barrier between the plenum gas and the hydraulic oil; it provides the forces to open and close the poppet; the actuator shaft links it to the poppet. | manual §1.3 p.2 | Direct statement. |
| 10 | The hydraulic control valve is a normally closed two-way valve, energized open during a pass and de-energized closed for the piston return. | manual §1.3 p.3 | Direct statement. |
| 11 | The hydraulic pump (vane type, electric motor) overcomes the plenum pressure to return the piston upstream, then holds pressure at no flow for minimum power. | manual §1.3 p.3 | Direct statement; reservoir shown in Fig. 3-1 p.28. |
| 12 | The optical assembly has 3 slotted optical switches: 1 for the standby position and 2 that define the displaced (base) volume. A flag on the detector shaft, attached to the piston, blocks the infrared light and generates the signal. | manual §1.3 pp.2–3 | Direct statement. |
| 13 | [+] The optical switches are spaced by Invar rods, whose thermal expansion coefficient is very small. | manual §4.3.1 p.49; §4.3.2 p.51 | "Invar Rods used for spacing the optical switches"; Eir = 0.00000144 /°C. The coefficient is not spoken (it belongs to the waterdraw calculations). |
| 14 | [+] The interface enclosure holds a circuit board that conditions the prover signals and sends them to the operating computer, which processes and summarises the proving data. | manual §1.1 p.1; §1.2 p.1 | "The Interface Enclosure contains a printed circuit board which conditions the signals…"; "The operating computer will process and summarize all proving data". |

## Series consistency (not research)
- The narration calls the 2 volume switches D1 and D2, the labels episodes 1–2 used for the detectors. This keeps the series consistent (owner decision 2026-09-25); it is not a research claim, so it has no [+] and no source.
- "الحاسبة" is used for the operating computer, as in episode 2; the FloBoss name is kept for episode 6 (owner decision).
- Rulon riders are named only; their function is not stated (owner decision).

## Numbers used (from projects/prover/prover_demo_data.py only)
- `len(PROVER_COMPONENTS)` = 10, `OPTICAL_SWITCH_COUNT` = 3, `VOLUME_SWITCH_COUNT` = 2, `len(CYCLE_STAGES)` = 5 (teaser).
