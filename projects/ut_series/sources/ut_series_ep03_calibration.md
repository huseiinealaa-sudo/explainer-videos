# ut_series_ep03_calibration — research notes (claim → source → note)

Official reference: IAEA-TCS-67 (2017), https://www-pub.iaea.org/MTCD/Publications/PDF/TCS-67web.pdf. Printed page = PDF page − 13, checked on the downloaded file (2026-10-04).

| Claim | TCS-67 | Note |
|---|---|---|
| Calibration: verifying and adjusting equipment so results are reliable and reproducible; three parts: equipment characteristics, range, reference level (sensitivity) | §5.1, p. 177 | |
| Characteristics: horizontal linearity, screen-height linearity, amplitude-control linearity, resolution, dead zone, penetrative power | §5.3, p. 187–190 | "periodically" is not in the text; wear changes probe index and angle (p. 178) |
| Dead zone = depth below the entry surface that cannot be inspected because of the initial pulse | §5.3.6, p. 190 | |
| Resolution = telling apart close reflectors (V1: targets at 85, 91, 100 mm) | §5.3.4, p. 189 | |
| V1 block: 25 mm thickness, 100 mm quadrant, 1.5 mm hole, 50 mm hole with plastic insert, angle scales | §5.2.1, Fig. 5.1, p. 178 | read from the figure (image check) |
| Normal probe on V1 at position C: multiple back-wall echoes at 25, 50, 75, 100 … mm | §5.4.1.1, p. 191; Table 5.4, p. 192 | multiple echoes are used because of the zero error (p. 191) |
| Horizontal linearity from the same echoes | §5.3.1, p. 187 | first and fourth echo set, the others checked; tolerance 1 % (not spoken) |
| Refraction and mode conversion; longitudinal refracts more (faster) | §2.4.2.1, p. 112; §2.4.2.2, p. 113 | |
| First critical angle = asin(vL1/vL2); second = asin(vL1/vS2); at the second the shear wave becomes a surface wave | §2.4.2.2, p. 113 | |
| Perspex vL = 2730 m/s; steel vS = 3250 m/s | Table 2.1, p. 104; p. 114 | TCS-67's own wedge example uses both |
| Critical angles 27.46° and 57.14° | formulas above | data module; not printed in TCS-67 |
| Angle probe: wedge angle above the first critical angle, only shear in the part; the angle in steel is marked on the probe; the exit point is the probe index | §3.2.11, p. 144 | |
| Exit point: maximum echo of the 100 mm quadrant; the index is the point at the cut mark | §5.5.2.1, pp. 196–197 | |
| Range with angle probe: multiple echoes from the 100 mm quadrant | §5.5.1.1, p. 194 | |
| Angle check: maximum echo of the 1.5 mm hole or the plastic insert; read the scale at the index | §5.5.3.1, p. 197 | |
| Defect location: normal probe direct; angle probe d = R cosθ, R read on the calibrated screen; report the surface position too | §8.4.1, pp. 278–279 | TCS-67 calls the path R; surface distance R sinθ is derived |
| HSD = t tanθ, FSD = 2t tanθ, HSBPL = t/cosθ, FSBPL = 2t/cosθ | eqs. 6.2–6.5, p. 215 | 30 mm plate, 60°: 51.962 / 103.923 / 60.000 mm |
| DAC: equal side-drilled holes (angle) or flat-bottom holes (normal) at different depths in a calibration block; peaks joined | §5.7, p. 200 | largest echo set to 80 %, gain kept fixed; recording levels (50 %, 20 %) belong to episode 4 |
| DGS: another method to set sensitivity; distance (in near-field lengths), gain (dB), size (equivalent flat-bottom hole) | §5.8, pp. 201–202 | angle probes need their own diagram |
