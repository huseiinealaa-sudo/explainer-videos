# mc5_hart — verification of the refined source

Sources: [1] User Guide for MC5 HART Option (Main Firmware 1.90), printed page = PDF page + 131. [2] MC5 User Guide, printed page = PDF page − 8. [3] MC5-IS User Manual (manualslib, read with WebFetch). Result: ✔ confirmed, ✎ corrected, ◐ confirmed by a secondary source only, ○ not stated in the official documents (kept as in the owner's text, listed for the owner).

| § | Claim | Source and page | Result |
|---|---|---|---|
| 1.1 | Zero Pressure Module: D/Menu → A/Window 1 Setup (or B/Window 2 Setup) → 7 | [2] p. 40 | ✔ |
| 1.2 | D/Menu → B/Window 2 Setup if needed → 5/HART; the HART item is disabled if the other window reserves the E module | [1] p. 141 | ✔ |
| 1.2 | up to 16 instruments on one loop; the instrument is chosen with the 4th function key («4/Select» = D) | [1] p. 141; function keys are also numbered 1–4 («2/Edit» = B/Edit, [1] p. 145) | ✔ |
| 1.2 | polling addresses 0–15 (HART revision 5) | [1] p. 137 (MC5 supports HART revision 5); the range itself is the HART standard | ◐ |
| 1.2 | address 0 = analog 4–20 mA active; 1–15 = multidrop, current fixed near 4 mA | not in [1]/[2]; Endress+Hauser BA00486, SAMSON L452, ICPDAS HART notes | ◐ |
| 1.2 | no device found: check the supply and the HART resistor, then Restart | [1] p. 138 (the loop needs 230–600 Ω), p. 141 (Restart key) | ✔ |
| 1.3 | the HART menu replaces the window menu; the window quantity becomes the digital output (PV) | [1] p. 142 | ✔ |
| 1.3 | Disconnect Device is needed before changing the window quantity | [1] p. 142 | ✔ |
| 1.3 | item «Unit» (the source calls it Display Unit) changes only MC5's display, not the transmitter | [1] p. 142 shows «Unit [kPa]»; the statement itself is not written | ○ |
| 1.3 | items 6 Trim Instrument, 7 Add HART Instrument to Database; bottom keys Window 1 Setup / Window 2 Setup / Others / Close MENU | [1] pp. 143, 145 | ✔ (item 5 is empty in the manual's figure: drawn as a faint bar) |
| 1.4 | Device Information fields; editable: Tag, Serial Number, Date, Descriptor, Message | [1] p. 142 | ✎ «Software Version» and «Hardware Revision» (not «Software/Hardware Revision») |
| 1.5 | Device Settings fields and the nine editable ones | [1] p. 143 | ✎ labels are «Lower Range», «Upper Range», «Lower Limit», «Upper Limit», «Damping (s)» |
| 1.5 | buttons A/Close and C/Edit | [1] p. 143 shows only Close; [2] p. 129 shows Save / Next page / Edit / MENU on the form pages (Edit = C) | ○ (the Edit key of this page is kept as in the owner's text) |
| 1.5 | wait about 5 × the damping after each point | not stated; a first-order response reaches 99.3 % after 5 time constants | ○ |
| 1.5 | Linear for pressure, Square Root for differential-pressure flow only; Burst Off = answers only when asked; URL/LRL fixed limits; the range cannot be narrower than Minimum Span | the field names and values are in [1] p. 143 (Burst Mode Off, Linear); the explanations are HART practice | ○ |
| 1.6 | edit: choose the field, change, confirm with Enter | [2] p. 10 (Enter, or D/OK when available, finishes a number), p. 22 | ✔ |
| 1.6 | rerange example 15 kgf/cm²: 10 → 12 mA | computed: 4 + 16 × 15/40 = 10; 4 + 16 × 15/30 = 12 | ✔ |
| 2.2 | D/Menu → 6/Trim Instrument → pop-up AO or PV → «Reading HART instrument data. Please wait.» | [1] p. 143 | ✔ |
| 2.2 | for the Digital Output (PV): Instrument Input page → B/Next Page → Instrument Output → A/Trim; Select Output switches AO ↔ PV | [1] p. 144 | ✔ (written there for PV only; the video follows the PV path) |
| 2.2 | warning: do not alter any settings unless you have the knowledge and are authorized | [1] p. 144 | ✔ |
| 2.2 | field steps: tell the control room, loop on Manual, isolate trips | not in [1]/[2] (general practice, from the owner's text) | ○ |
| 2.3 | AO screen: Input = Current [Keyed] (the set point sent by MC5), Output = Current [E: Meas]; field «Enter measured 0%»; the error shows N/A in the field screen | [1] p. 149 | ✔ |
| 2.3 | trim menu: Trim Lower 0% Range, Trim Upper 100% Range, Check Any Value, Select Output, Device Information, Device Settings, End HART Adjustment | [1] p. 144, p. 148 | ✔ |
| 2.3 | C/Fetch copies the Output window value, D/Send sends it | [1] p. 149 | ✎ the original wrote «D Trim» |
| 2.3 | NAMUR NE 43: 3.8–20.5 mA measuring range; ≤ 3.6 or ≥ 21.0 mA failure | NE 43 itself is paid; summaries: Vaisala PR23 manual, ElectricalVolt, MicroControl (the exact failure bands differ slightly between manufacturers) | ◐ |
| 2.3 | check 3.8 / 4 / 12 / 20 / 20.5 mA, then trim lower, then upper | the check points are the owner's; the order follows [1] and [2] p. 108 («zero at the lower end, span at the higher end») | ✔ |
| 2.4 | PV screen: Input = reference pressure, Output = Pressure [E: HART\PV], field «Trim 0% to:», C/Fetch copies the Input window, D/Send | [1] p. 149 | ✔ |
| 2.4 | the upper trim near the top of the used range; the zero depends on the mounting position | not in [1]/[2] (general practice) | ○ |
| 2.6 | End HART Adjustment returns the transmitter to normal measurement | the menu item exists ([1] p. 144); its effect is not described | ○ |
| 3.1 | Add HART Instrument to Database → Analog or Digital; the data fetched (quantities, units, range, methods, Transfer Function, Setpoint Delay); the Tag goes to Device ID; no Position ID | [1] p. 145 | ✔ |
| 3.1 | two files for AO and PV | [1] p. 137 | ✔ |
| 3.1 | fields to review: Error Calculation Method, Reject if, Input Port, Calibration Method, Calibration Points, Output Port | [1] p. 145 | ✔ |
| 3.2 | four pages of instrument data | [2] p. 129: **five** pages (General Data, Input, Output, Calibration Settings, Calibration Instructions: Starting / Adjusting / Finishing Guide) | ✎ |
| 3.2 | General Data fields; the «Serial Number» row | [2] p. 129 shows Position ID, Position Name, Device ID, Device Name, Error Calc. Method, Reject if, Adjust if, Do not Adjust if, Adjust to | ○ (the owner's newer device shows Serial Number instead of Device Name) |
| 3.2 | **[check]** meaning of Reject if / Adjust if / Do not Adjust if / Adjust to | [2] p. 108: Reject if > = acceptance limit for the maximum error found; Adjust if > = the instrument must be adjusted if exceeded; Do not Adjust if < = adjusting is unnecessary; Adjust to < = after adjusting the maximum error should not exceed it | ✔ |
| 3.2 | Setpoint Delay: how long MC5 waits before saving the input and output values after the input reached the next point | [2] p. 131, [3] p. 130: the same, and «of use only when the Calibration Method is Automatic» (also the Autocapture feature, [2] p. 117) | ✎ added: only in Automatic |
| 3.2 | **[check]** Maximum Allowed Calibration Point Deviation | [2] p. 131: how far the input value of the saved point may be from the theoretical point; used in manual and automatic calibration | ✔ |
| 3.2 | **[check]** Calibration Period | [2] p. 131 shows «Cal. Period, Days» (< 360 in the figure) and no definition | ○ (the video says only «the calibration period in days») |
| 3.3 | **[check]** the ✓ mark in the instrument list | [2] p. 112: «the Position ID / Device ID of an already calibrated instrument is tick-marked» | ✔ |
| 3.3 | list keys A/Basic Mode, C/Select, D/MENU | [2] p. 112, p. 132 | ✔ |
| 3.4 | calibration window keys A/Back, B/Start, C/Adjust, D/MENU | [2] p. 114 shows Back / Start / Adjust / MENU. [3] p. 114, as read: «A typical calibration procedure using MC5-IS is as follows: We assume you have already selected the instrument …» and the figure labels «Start  Adjust  MENU» (the Back label and the A–D letters are not in the extracted text) | ✔ |
| 3.4 | window menu: Start HART Adjustment, Prescan [On], View Calibration Results, Zero Pressure Module, Close | [1] p. 147 (this is the figure's order; the owner's text lists Close first) | ✎ order |
| 3.4 | while recording: Stop Readings and Accept | [1] p. 147; [2] p. 116 calls the key «B/Accept Readings» | ✔ |
| 3.4 | **[check]** the role of C/Adjust against Start HART Adjustment | [2] p. 127: C/Adjust opens MC5's general adjustment utility, useful when MC5 generates or simulates the input; «for help on how to adjust/trim HART instruments, see Appendix 1» = the menu item Start HART Adjustment. [3] p. 126 (MC5-IS) opens the same section: «MC5-IS includes a special utility for adjusting instruments», useful when the input is generated or simulated. The newer firmware could not be compared | ✔ (for 1.90) |
| 3.5 | standard points 0 25 50 75 100 % up then down; hysteresis | [2] p. 108 (As Found graph at 0–100 %); the points are the instrument's «5 ↑↓» setting ([1] p. 146) | ✔ |
| 3.6 | As Found documents the state before any adjustment; As Left after; the As Found can be omitted when it is good | [2] pp. 108–109 | ✔ |
| 3.6 | adjust from inside the calibration: D/MENU → 1/Start HART Adjustment → input page → B → A/Trim; PV is selected, Select Output → AO | [1] pp. 147–148 (when the previous instrument was not the digital output, MC5 first asks to start the communication and select the instrument) | ✔ |
| 3.6 | calibrating the AO needs no HART communication | [1] pp. 137, 147 | ✔ |
| 3.7 | error types, decision tree, TUR ≥ 4 preferred | general metrology practice | ○ |
| 3.7 | View Calibration Results shows the saved tables and graphs | [2] p. 133 | ✔ |

## Numbers typed in the data module for episode 1
- `HART_MAX_DEVICES = 16`: [1] p. 141 («Up to 16 instruments may be connected to the same current loop»). `POLL_MAX = 15`: polling addresses 0–15 of HART revision 5 (MC5 supports revision 5, [1] p. 137). `I_LOW, I_HIGH = 4, 20` mA: the loop range.
