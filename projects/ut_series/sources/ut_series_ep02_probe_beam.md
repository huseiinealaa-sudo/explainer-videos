# ut_series_ep02_probe_beam — research notes (claim → source → note)

Official reference: IAEA-TCS-67 (2017), https://www-pub.iaea.org/MTCD/Publications/PDF/TCS-67web.pdf. Printed page = PDF page − 13, checked on the downloaded file (2026-10-04).

| Claim | TCS-67 | Note |
|---|---|---|
| Direct effect (pressure → voltage) receives; inverse effect (voltage → deformation) generates | §2.6.1, p. 118 | one crystal does both in pulse-echo |
| Materials: quartz; polarized ceramics (barium titanate, lead zirconate titanate) | §2.6.1.1, pp. 119–121; Table 2.2, p. 122 | ceramics "nearly completely replaced quartz" (p. 120); lithium sulphate and lead metaniobate also listed |
| Thinner crystal → higher frequency; resonance when thickness = half a wavelength | eq. 3.3 f = v/2t, §3.2.1, p. 138 | spoken as a concept; no equation (owner decision 2026-10-04) |
| Probe parts: crystal, backing, matching network, case; wear face | §3.2, pp. 137–138; §3.2.4, p. 139 | corrects "electrical connector" |
| Backing controls resolution and sensitivity; strong damping = high resolution, low sensitivity | §3.2.2, p. 139; bandwidth p. 145 | "resolution" = separating two close echoes in depth (same page) |
| Single-crystal normal probe: large initial pulse, large dead zone; poor for thin walls and near-surface flaws | §3.2.7, p. 141 | |
| Twin-crystal probe: two crystals, acoustic barrier, delay blocks, short dead zone; thin walls and near-surface flaws; remaining wall thickness | §3.2.9, pp. 142–144 | "corroded walls" is not in the text |
| Angle probe: perspex wedge, angle of incidence above the first critical angle, only shear enters | §3.2.11, p. 144 | detail in episode 3 |
| Immersion: probe and part in water; laboratory and automatic installations | §3.3.4, p. 153; §3.2.10, p. 144 | |
| Focused probe: curved crystal or lens, higher sensitivity over a range | §3.2.8, pp. 141–142 | |
| Near field: interference of the sources over the crystal; flaws there "must be carefully interpreted", multiple indications; plastic shoes help | §2.7.1.1, p. 125 | corrects "unreliable" |
| Last maximum at N; far field after N; transition zone N–3N; constant divergence beyond about 3N | §2.7.1, p. 124; §2.7.1.3, p. 126 | adds the transition zone to the owner's text |
| N = D²/4λ = D² f/4v; larger diameter or higher frequency → longer N | eq. 2.18, §2.7.1.2, p. 125; §2.7.3, p. 127 | |
| Example: 10 mm, 4 MHz, steel → 16.83 mm (v = 5940) | p. 128 | ours: v = 5920 → 16.892 mm ≈ 16.9 (data module) |
| Beam half angle sin(γ/2) = Kλ/D; K = 1.22 at the 0 % edge; 0.51 at −6 dB (pulse-echo, circular) | eq. 2.19, p. 126; Tables 2.3–2.4, p. 127; example p. 128 | resolves the [تحقق]; angles are to the beam edge |
| Larger crystal or higher frequency → narrower beam | §2.7.3, p. 127 | |
| Attenuation = absorption (→ heat) + scattering (+ other losses) | §2.5.2, p. 118; §2.8.1.1–2.8.1.2, pp. 129–130 | |
| Scattering rises rapidly with grain size; absorption ∝ frequency, much slower than scattering | §2.8.1.2, p. 130; §2.8.1.5, p. 131 | frequency dependence of scattering is implied, not worded |
| Castings (coarse grain) are tested at lower frequencies | §6.1 castings, p. 161 | |
| Austenitic welds: improved tests at low frequency (1.5 MHz), short pulses | §6.1.7.5, p. 230 | |
| Computed values: λ = 1.48 mm, N = 16.892 mm, half angles 10.40° / 21.17° / 5.18° | formulas above | `ut_series_data.py`, `self_test()` |
