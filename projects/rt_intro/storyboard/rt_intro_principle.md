# rt_intro_principle — Industrial radiography: principle and geometric unsharpness   (target ~4:10, measured narration 4:29, 6 segments)

Durations are the measured narration audio (ar-SA-HamedNeural, normal speed). All numbers from
`rt_intro_data.py` (F, d, D1, D2, UG1, UG2, UG_RATIO, UG_MAX, D_MIN, IR192_HALF_LIFE_DAYS).
Colours: ACCENT_1 blue = radiation (rays, beam); ACCENT_2 orange = the source (focal spot,
capsule, its size F); ACCENT_3 green = within the limit; ACCENT_4 red = defects, out of limit.
Film darkness is drawn in grey (darker = more radiation reached the film).

| # | Idea (one per segment) | What is drawn | What moves | Worked example | Scene | Duration |
|---|---|---|---|---|---|---|
| 1 | RT reveals internal defects without damaging the part and leaves a permanent record | title + disclaimer box; butt-weld cross-section (two plates, V weld) with four defects: porosity, slag, lack of fusion, crack; source above, film below | each defect is drawn and named at its word; rays travel source → weld → film; the defect shadows develop on the film; the film slides into a record folder ("permanent record") | — | title_card + custom drawing | 0:39 |
| 2 | Differential absorption: a void lets more radiation through (darker), a denser inclusion less (lighter) | long wave (light) and short wave (X / gamma); steel plate cross-section with thickness t, a void and a tungsten inclusion; rays; film strip under the plate | the wave compresses to a short wavelength and passes into the metal; rays cross the plate, the transmitted ray width shrinks with the metal crossed; the effective-thickness bracket shortens at the void; the film darkens: grey background, dark patch under the void, light patch under the tungsten | — | custom (mechanism) | 0:47 |
| 3 | Two sources: an X-ray tube you switch off, an Ir-192 capsule that never switches off; both have a size F | left: X-ray tube (glass envelope, cathode filament, anode target, focal spot, kV supply, switch); right: shielded container, guide tube, capsule, exposure head at the exposure position | electrons fly cathode → target, X-rays leave the focal spot; kV knob turns and the beam gets more penetrating; the switch goes OFF and the beam stops; the capsule is pushed along the guide tube to the exposure position and radiates in all directions; "half-life ≈ 74 days" tag; both sources zoom to show their size F | — | custom (two mechanisms side by side) | 0:53 |
| 4 | A source of size F casts a penumbra of width Ug = F·d/D; three ways to reduce it | source (point, then segment F), plate with an opaque edge on its source side, film; rays from both ends of the source; umbra / penumbra; dimension lines D and d; the two similar triangles; the equation Ug = F × d / D | the point source grows to size F and the sharp edge splits into a penumbra; the two similar triangles light up in turn; D and d are drawn at their words; then F shrinks, the source moves up (D grows), the film moves up (d shrinks), and the penumbra narrows each time; last line: ASME V recommends a maximum, the binding limit comes from the referencing Code | — | custom (geometry, ValueTracker-driven) + equation (Text pieces) | 0:58 |
| 5 | Worked example: halving D doubles Ug; the smallest allowed D for a 0.51 mm limit | left: worked_calculation; right: the geometry rig (not to scale) with a D scale, readouts D and Ug, penumbra brace | lines of the calculation at their numbers; the source slides 400 → 200 mm and the penumbra visibly doubles (Ug 0.15 → 0.30 mm, "×2"); the limit line 0.51 appears and the source slides to D_min = 117.6 mm, zone closer than D_min turns red | Ug1 = 3.0 × 20 / 400 = 0.15 mm; Ug2 = 3.0 × 20 / 200 = 0.30 mm (×2); D_min = 3.0 × 20 / 0.51 = 117.6 mm | worked_calculation + custom rig | 0:48 |
| 6 | Summary | framed three takeaways | lines appear at their words | — | summary_box | 0:25 |

Text-scene share: title/disclaimer ≈ 9 s + summary 25 s = ≈ 34 s / 269 s = **≈ 13 %** (limit ~33 %).
The equation (seg 4) and the calculation (seg 5) stay beside a moving drawing, so they are not text-only screens.
Custom drawings: **5** (segments 1–5)   Worked examples: **1** (three calculations: Ug1, Ug2, D_min)
Left out (owner-approved, request of 2026-09-27): radiation safety, inverse square law, source decay
beyond the half-life value, IQI, film density, digital radiography, defect interpretation.
