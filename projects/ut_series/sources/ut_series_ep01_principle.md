# ut_series_ep01_principle — research notes (claim → source → note)

Official reference: IAEA-TCS-67 (2017), https://www-pub.iaea.org/MTCD/Publications/PDF/TCS-67web.pdf. Page numbers are the printed ones (PDF page − 13), checked on the downloaded file.
Supporting source IAEA-TCS-10 (1999): not used, the INIS record is behind a Cloudflare check (HTTP 403) and no direct PDF link was found; TCS-67 (2017) is the newer text.

## A. Claims confirmed as written
| Claim in the source file | TCS-67 | Note |
|---|---|---|
| UT uses high-frequency sound; most inspection at 0.5–20 MHz; attenuation; pulse-echo or transmitted intensity | §1.1.2.6, p. 9; §2.1, p. 99 | the same range is repeated in §2.1 |
| Audible range up to about 20 kHz; above it is ultrasonic; propagates in solid, liquid and gas, not in vacuum | §2.1, p. 99 | audible range is given as 20 Hz–20 kHz |
| Uses: flaw detection, thickness, mechanical properties and grain structure | §1.1.2.6 (a), (b), p. 9 | |
| Advantages (5) and limitations (6) | §1.1.2.6, p. 9 | penetration "up to about 7 m of steel" and "6 to 7 m in steel" (both on p. 9) |
| Vibration of particles transfers the energy through elastic coupling | §2.1, pp. 99–100 | |
| Wave velocity depends on elastic modulus and density, independent of frequency | §2.3.5, p. 108 | |
| λ = v / f (v = fλ) | eq. 2.5, p. 101 | |
| Longitudinal waves propagate in solids, liquids and gases | §2.3.1, p. 105 | |
| Transverse waves only in solids | §2.3.2, p. 106 | TCS-67 gives the reason as too weak an attraction between the molecules of liquids and gases; "liquids do not resist shear" is the usual equivalent wording |
| vs / vl = 0.55 for steel | eq. 2.13, p. 108 | p. 106 says "about 50 percent" in general |
| Surface (Rayleigh) wave: about one wavelength deep; speed about 90 % of the shear wave | §2.3.3, p. 106; eq. 2.12, p. 108 | |
| Z = ρ v | eq. 2.6, p. 103 | |
| R = ((Z2 − Z1)/(Z2 + Z1))², T = 1 − R | eqs. 2.14–2.16, pp. 109–110 | TCS-67's own example water → steel gives 88 % (p. 111), the same as steel → water |
| Z water 1.48 MRayl; steel (calibration block) ρ = 7850, vl = 5920, Z = 46.472 MRayl | Table 2.1, p. 104 | matches `Z_STEEL` exactly |
| Couplant eliminates the air between probe and part | §5.9, p. 203 | |
| Pulse-echo: same side, most commonly used; the screen is calibrated to separate flaw echo from back-wall echo | §3.1.2, p. 134 | |
| A-scan: horizontal = elapsed time, vertical = echo amplitude; depth and size estimated from it | §4.3.2, p. 169 | outside the source file's page range; the initial pulse is also called the "main bang" (§4.1) |
| Through transmission: two probes, a defect lowers the received amplitude, needs both sides | §3.1.1, p. 133 | |
| Computed values: λ steel/water, Z, R steel–water and steel–air, echo times, depth, aluminium reading | formulas above | computed in `ut_series_data.py` with `self_test()`; not printed in TCS-67 |

## B. Corrections and conflicts (all listed in the approval message)
| # | Claim in the source file | Correction / conflict | Source |
|---|---|---|---|
| 1 | [تحقق] smallest detectable flaw "about half a wavelength" | TCS-67 says flaws "of the order of λ/2 or λ/3 can be detected"; its example uses λ/3. The narration says "half or a third of the wavelength". | §2.2.4, p. 102; example p. 103 |
| 2 | Lamb waves travel in plates "whose thickness approaches the wavelength" | A plate of thickness equal to three wavelengths or less. The narration says "not more than three wavelengths". | §2.3.4, p. 107 |
| 3 | Couplant "water, oil, gel or glycerine" | TCS-67 lists glycerine, water, oils, petroleum greases, silicon grease, wall-paper paste and commercial pastes; "gel" is not named. Question 2 and segment 4 speak of "a couplant" without the list. | §5.9, p. 203 |
| 4 | Through-transmission "does not give the flaw depth" | It gives neither the size nor the location. Narration: "does not give the location of the flaw". | §3.1.1, p. 133 |
| 5 | Resonance: "a standing wave forms in the thickness" | Resonance occurs when the thickness equals half a wavelength or a multiple of it; t = v / 2f; now largely superseded by pulse-echo. Narration: "until the thickness equals half the wavelength". | §3.1.3, pp. 135–136 |
| 6 | Shear velocity in steel 3240 m/s | Table 2.1 gives 3250 m/s for both steels. The ratio shown, 0.55, equals TCS-67's own eq. 2.13. | Table 2.1, p. 104; p. 108 |
| 7 | Air: 343 m/s, 1.2 kg/m³, Z = 412 Rayl | Table 2.1: 330 m/s, 1.3 kg/m³, Z = 430 Rayl. [+] 343 m/s and 1.204 kg/m³ (Z ≈ 413 Rayl) are the values of air at 20 °C: https://sengpielaudio.com/TemperatureSound.htm (priority-4 source). The reflection to 3 decimals, 99.996 %, is the same with either set. | Table 2.1, p. 104 |
| 8 | Steel 5920 m/s, Z = 46.47 MRayl | Matches the row "steel (calibration block)". The row "steel (low alloy)" is 5940 m/s, 46.62 MRayl, and is the one used in TCS-67's own examples (p. 103, p. 111). The reflection is 88 % either way. | Table 2.1, p. 104 |

## C. Page ranges of the source file
§1.1.2.6 p. 9, chapter 2 pp. 99–132 and §3.1 pp. 133–136 are all confirmed. Claims in section 5 of the source (A-scan axes) and the couplant statement come from §4.3.2 (p. 169) and §5.9 (p. 203), outside those ranges.
