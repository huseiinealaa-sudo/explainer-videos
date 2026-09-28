# symbol_gallery — Symbol Gallery   (1:48, 10 silent segments)

Silent catalogue (no narration, owner's request): the "drawing–speech fit" axis is judged as
**drawing–name fit**: each drawing must match the name under it and the ISA-5.1 form listed
in `explainer/symbols/SOURCES.md`. Durations come from `symbol_gallery_data.DURATIONS`.

| # | Idea (one per segment) | What is drawn | What moves | Worked example | Scene | Duration |
|---|---|---|---|---|---|---|
| 1 | What this catalogue covers | title, series line, subtitle | title written | — | title_card | 0:06 |
| 2 | Tabler icons, page 1 (25 of 50) | 7-column grid, each icon with its name; caption with icon() signature, Tabler version, MIT | icons drawn one after another | — | icon_grid (new library block) | 0:11 |
| 3 | Tabler icons, page 2 (25 of 50) | same | same | — | icon_grid | 0:11 |
| 4 | ISA valves | gate, globe, ball, butterfly, check, control valve (diaphragm), relief/safety — each with short process stubs and its name | symbols drawn in turn; ports flash as orange dots | — | custom (explainer.symbols) | 0:12 |
| 5 | ISA pumps and machines | centrifugal pump, PD pump, compressor, tank, heat exchanger + names | drawn in turn; ports flash | — | custom | 0:10 |
| 6 | ISA flow measurement | orifice plate, turbine, magnetic, Coriolis, vortex (in-line, flow left→right) + names | drawn in turn; ports flash | — | custom | 0:10 |
| 7 | Instrument bubbles by location | field FT-101, panel PIC-102, behind panel PY-103, DCS FIC-101, PLC LSH-104 + location names | drawn in turn | — | custom | 0:12 |
| 8 | ISA line types | process, connection (impulse), pneumatic, electrical, capillary, data/software link + names | each line drawn left→right | — | custom | 0:11 |
| 9 | A flow control loop joined with connect() | tank → pump → orifice plate (FE) → control valve FV-101 → out; FT-101 on the orifice taps; FIC-101 (DCS); FY-101 (I/P) on the valve; legend | process drawn in flow order; then FT, electrical FT→FIC, FIC→FY, pneumatic FY→actuator; legend | loop 101 (illustrative) | custom | 0:24 |
| 10 | How to call the new functions | four code lines | lines fade in | — | text | 0:06 |

Text-scene share: title 6 s + code lines 6 s = 12 s / 113 s ≈ 11 % (limit ~33 %)
Custom drawings: 7 segments (4–9 + icon grids)   Worked examples: none (no numbers; loop 101 is a tag)
Left out (with reason and proposal): valve actuators other than the diaphragm, fail-position
marks and the other bubble shapes (auxiliary panel, computer function) are outside the
requested list; they can be added to `isa.py` the same way when a project needs them.
