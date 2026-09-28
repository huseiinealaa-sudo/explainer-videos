# ISA-5.1 symbols: where each drawing comes from

ANSI/ISA-5.1 (*Instrumentation Symbols and Identification*) is a paid standard, and no copy
of it was used. Every symbol in `explainer/symbols/isa.py` was **drawn in code** from the
descriptions and figures of the free references below; no image was copied.

## References
| Key | Reference | Licence / access | Notes |
|---|---|---|---|
| **K** | Tony R. Kuphaldt, *Lessons In Industrial Instrumentation*, v2.32 (2019), §7.5 "Instrument and process equipment symbols" (book pp. 544–552): 7.5.1 line types, 7.5.3 instrument bubbles, 7.5.4 process valve types, 7.5.5 valve actuator types, 7.5.8 flow measurement devices, 7.5.9 process equipment. PDF: https://www.ibiblio.org/kuphaldt/socratic/sinst/book/liii_2v32.pdf (also published as the control.com textbook: https://control.com/textbook/instrumentation-documents/instrument-and-process-equipment-symbols/) | CC BY 4.0, free | Primary reference. Its line-type note tracks the ANSI/ISA-5.1-2009 edition (the discrete-signal backslash and the triple-slash electrical form were removed in 2009). |
| **K16** | Same book, ch. 16 (Foundation Fieldbus), p. 1166: "lines with hollow circles represent data sent between functions within the same physical device" | CC BY 4.0 | Data / software link line. |
| **I** | *ISA-5.1, Instrumentation Symbols and Identification*, InTech, Sept/Oct 2020 (T. McAvinew), https://www.isa.org/intech/2020/september-october/isa-5-1-instrumentation-symbols-and-identification, and the ISA-5.1 update article on automation.com (https://www.automation.com/article/document-projects-updated-isa51-standard) | free (ISA / automation.com) | Confirms that the updated standard clarified "circle-in-square" (shared display / shared control, DCS) and "diamond-in-square" (PLC). The article bodies were not reachable from the build container (HTTP 403): the claim is taken from their summaries; see "Partly verified" below. |
| **W** | Wikipedia, *Piping and instrumentation diagram*, symbol gallery (ISO 10628 style: pump, compressor, heat exchanger) https://en.wikipedia.org/wiki/Piping_and_instrumentation_diagram | CC BY-SA, free | Cross-check of the equipment outlines. |

## Symbol → source
| Group | Symbol (function) | Drawn as | Source |
|---|---|---|---|
| Valves | `gate_valve` | two triangles tip to tip (two-way body) | K 7.5.4 "Valve (generic)"; see decision 1 |
| | `globe_valve` | two-way body + solid dot | K 7.5.4 "Globe valve" |
| | `ball_valve` | two-way body + open circle | K 7.5.4 "Ball valve" (second form) |
| | `butterfly_valve` | two flanges + slanted disc with shaft dot | K 7.5.4 "Butterfly valve" |
| | `check_valve` | \|\\\| body + free-flow arrow above | K 7.5.4 "Check valve (generic)" |
| | `control_valve` | two-way body + stem + dome (spring-and-diaphragm actuator) | K 7.5.5 "Diaphragm" |
| | `relief_valve` | angle body (inlet below, outlet right) + spring on the stem | K 7.5.4 "Pressure relief or safety valve" |
| Pumps and machines | `centrifugal_pump` | casing circle, tangential discharge at the top, base | K 7.5.9 "Centrifugal pump"; W "Pump" |
| | `pd_pump` | stepped casing, rotors, suction left, discharge right | K 7.5.9 "Positive-displacement pump" |
| | `compressor` | circle with two lines converging from inlet to outlet | W "Vacuum pump or compressor" (K 7.5.9 draws machine types pictorially) |
| | `tank` | vertical shell with cone roof | K 7.5.9 "Pressure vessels" (outline); W vessels |
| | `heat_exchanger` | shell circle, tube zigzag through it, shell nozzles top/bottom | K 7.5.9 "Shell-and-tube heat exchanger"; W "Heat exchanger" |
| Flow measurement | `orifice_plate` | two short bars across the pipe | K 7.5.8 "Orifice plate" |
| | `turbine_meter` | box across the pipe + two-bladed rotor | K 7.5.8 "Turbine" |
| | `magnetic_flowmeter` | box across the pipe + "M" | K 7.5.8 "Magnetic" |
| | `coriolis_meter` | box across the pipe + small wave (vibrating tube) | K 7.5.8 "Coriolis" |
| | `vortex_meter` | box across the pipe + triangle (bluff body) | K 7.5.8 "Vortex" |
| Bubbles | `instrument(..., "field")` | circle, no line | K 7.5.3 "Field mounted" |
| | `"panel"` | circle + solid line (primary location, accessible to the operator) | K 7.5.3 "Main control panel front-mounted" |
| | `"behind_panel"` | circle + dashed line (not accessible to the operator) | K 7.5.3 "Main control panel rear-mounted" |
| | `"dcs"` | circle in square + solid line (shared display / shared control) | K 7.5.3 "Shared instruments"; I |
| | `"plc"` | diamond in square + solid line | K 7.5.3 "Logic" (diamond); I (diamond-in-square = PLC) — partly verified |
| Lines | `process` | heavy solid | K 7.5.1 "Process flow line" |
| | `connection` | thin solid | K 7.5.1 "Instrument supply or process connection (impulse line)" |
| | `pneumatic` | thin line with double slashes | K 7.5.1 "Pneumatic signal" |
| | `electrical` | dashed | K 7.5.1 "Electric signal" |
| | `capillary` | thin line with crosses | K 7.5.1 "Capillary tube" |
| | `data` | thin line with small open circles | K 7.5.1 "Data link (common system)"; K16 |

## Decisions and partly verified points
1. **Gate valve.** K draws the gate valve as two short bars between the pipe ends, and the
   bowtie as the *generic* valve; most P&ID legends and the ISA generic two-way body use the
   bowtie for gate valves. The library uses the bowtie (the common form) and the globe / ball
   variants add their dot / circle to it. K's bar form can be added later as an option.
2. **PLC bubble.** K's free edition shows logic as a plain diamond; the diamond-*in-square*
   form for PLC functions is taken from the ISA-5.1 summaries (I). Their full text could not be
   read in the build container, so this symbol is marked partly verified.
3. **Compressor.** K draws compressor types pictorially; the circle with converging lines
   (W, ISO 10628 style) is the form used on P&IDs and was chosen.
4. **Line spacing.** Mark spacing (slashes, crosses, circles) is a drawing choice
   (`MARK_SPACING`), not set by the references.
5. Loop numbers and tags in examples (FT-101, FIC-101, FY-101, FV-101 ...) are illustrative.
