# rt_intro_principle — sources (claim → source → note)

Research only verifies the cleaned source `rt_intro_source.md`. Priority-1 references:

- **[IAEA-3]** IAEA, *Industrial Radiography — Manual for the syllabi contained in IAEA-TECDOC-628*,
  Training Course Series No. 3, Vienna, 1992. Catalogue page:
  https://www.iaea.org/publications/345/industrial-radiography-manual-for-the-syllabi-contained-in-iaea-tecdoc-628-training-guidelines-in-non-destructive-testing-techniques
  (full text read from the public copy http://argo.aec.org.sy/ndt/pdf/specifications/IAEA-TECDOC-628/No3.pdf,
  Wayback snapshot 2024-12-08; page numbers below are the printed page numbers of the manual).
- **[ASME-V-2010]** ASME BPVC Section V (2010), Article 2, T-274.1 and T-274.2 — official text
  published as law by Public.Resource.Org: https://archive.org/details/gov.law.asme.bpvc.v.2010
- **[ASME-I-PW51]** ASME Section I rewrite project 22-1403, PW-51 (19 July 2022), existing and
  proposed text of PW-51.1 (2021 edition): https://cstools.asme.org/csconnect/Filedownload.cfm?thisfile=R0221403.pdf&dir=public
- **[NIDC]** U.S. DOE National Isotope Development Center, *Iridium-192 Product Information*
  (decay data from NNDC): https://isotopes.gov/sites/default/files/2019-09/Ir-192.pdf
- Secondary (context only): ndt.net, *ASME Section V Edition 2019 Code Changes* (NDE India 2019,
  CP025): https://www.ndt.net/article/nde-india2019/papers/CP025.pdf

## Section 1 — what RT is, why it is used
| Claim | Source | Note |
|---|---|---|
| RT is an NDT method: components examined for flaws without harming their use | [IAEA-3] Foreword | ✓ |
| Porosity, slag, lack of fusion, cracks in welds are revealed | [IAEA-3] §9.4.1 pp. 248–250 (gas pores, slag, tungsten inclusions, lack of penetration and fusion, cracks) | ✓ |
| Radiation passes through the part onto a film or detector behind it; a shadow picture forms | [IAEA-3] §2.1.1 p. 99 ("shadow pictures"), §2.3.1 p. 110; filmless detectors §4.15 p. 161 | ✓ |
| Film gives a permanent record | [IAEA-3] §2.5.1 p. 120 ("the advantage of providing a permanent record") | ✓ |

## Section 2 — differential absorption
| Claim | Source | Note |
|---|---|---|
| X- and gamma rays are electromagnetic radiation of very short wavelength | [IAEA-3] §2.1.2 p. 99 ("several thousand times smaller wavelengths" than light) | ✓ |
| The amount absorbed grows with thickness and density | [IAEA-3] §2.3.1 p. 110 ("depends on the quality of radiation, material/density of specimen and the thickness traversed"), I = I₀·exp(−μx), μ depends on the material/density (p. 110, §2.3.2 p. 112) | ✓ |
| A void = less metal in the beam → more radiation reaches the film → darker | [IAEA-3] §2.3.1 p. 110 ("a change in thickness (e.g. a void)"); §9.4.1 p. 248 (gas pore: "sharply defined dark shadow") | ✓ |
| A denser inclusion (tungsten) absorbs more → lighter | [IAEA-3] §2.3.1 p. 110 ("change in density (e.g. inclusion of foreign material)"); §9.4.1 p. 249 ("tungsten inclusions appear as very light marks") | ✓ |
| The picture maps changes of thickness and density | [IAEA-3] §2.3.1 p. 110 ("corresponding changes in the transmitted beam intensity recorded in a radiograph") | ✓ |

## Section 3 — the source: X-ray tube or Ir-192
| Claim | Source | Note |
|---|---|---|
| Electrons accelerated by a high voltage strike a metal target and X-rays are produced | [IAEA-3] §3.1 p. 123 | ✓ |
| The area of the target struck is the focal spot | [IAEA-3] §3.1.3 p. 124 ("called the focus"; effective / optical focal spot) | ✓ |
| Beam energy set by the tube voltage (kV) | [IAEA-3] §3.1.8 p. 125 (kV control), §3.1.10 p. 129 ("an increase in kV results in … more penetrating X-rays") | ✓ |
| Works on electricity, stops when switched off | [IAEA-3] p. 142 contrasts gamma "cannot be turned off"; p. 327 | ✓ note: "some X-ray sets can continue to emit X-rays for a few seconds after the HT has been switched off" (safety detail, not in this episode) |
| Ir-192 in a small capsule, kept in a shielded container (projector) | [IAEA-3] §3.2.2 p. 136, §3.2.3 pp. 136–137 (lead, tungsten or depleted uranium) | ✓ |
| Pushed out to the exposure position through guide tubes | [IAEA-3] §3.2.3.4 p. 138 ("pushed out of its shielding to a desired position via guide tubes") | ✓ |
| No electricity needed, field work | [IAEA-3] p. 142, advantages of gamma sources ("No external power supply is necessary therefore, tests can be performed in remote areas") | ✓ |
| Cannot be switched off | [IAEA-3] p. 142 ("the radiation cannot be turned off") | ✓ |
| Ir-192 half-life about 74 days | [IAEA-3] p. 134 (74.4 d) and Table 3.2 p. 135 (74 d); [NIDC] 73.829 d | ✓ "about 74 days" holds; current data 73.83 d |
| The source has a real size F, not a point | [IAEA-3] §6.1.3 p. 180 ("a source of finite dimension") | ✓ |

## Section 4 — geometric unsharpness
| Claim | Source | Note |
|---|---|---|
| A finite source casts an umbra and a penumbra; the penumbra makes the edge unsharp | [IAEA-3] §6.1.3 p. 180, Fig. 6.3 | ✓ |
| Similar triangles: P = F·ofd / (sfd − ofd) | [IAEA-3] eq. 6.2 p. 180 | ✓ same as Ug = F·d/D with d = ofd and D = sfd − ofd |
| Ug = Fd/D | [ASME-V-2010] T-274.1 | ✓ |
| F = the maximum projected dimension of the radiating source (or effective focal spot) | [ASME-V-2010] T-274.1 | ✓ ASME adds: "in the plane perpendicular to the distance D from the weld or object being radiographed" |
| D = distance from the source to the source side of the object | [ASME-V-2010] T-274.1: "distance from source of radiation to weld or object being radiographed" | precision note: ASME names the object, not its side; D + d = source-to-film distance makes the source side the consistent reading ([IAEA-3] p. 180 uses sfd − ofd). "D and d shall be determined at the approximate center of the area of interest." |
| d = distance from the source side of the object to the film | [ASME-V-2010] T-274.1: "distance from source side of weld or object being radiographed to the film" | ✓ exact |
| Three ways to improve: smaller source, larger distance, film close to the part | [IAEA-3] §6.1.3 p. 181 | ✓ |
| "The specifications set an upper limit for Ug" | [ASME-V-2010] T-274.2: "**Recommended** maximum values for geometric unsharpness are as follows"; [ASME-I-PW51] PW-51.1: "The requirements of T-274 are to be used as a guide but not for the rejection of radiographs unless the geometrical unsharpness exceeds 0.07 in. (1.8 mm)" | **corrected**: in ASME V the table is recommended; the binding limit comes from the referencing Code or the contract. The 2019–2025 texts of Section V are paywalled and could not be read; the secondary source (ndt.net CP025, 2019) quotes the same Section I / VIII-1 guide rule. |

## Section 5 — worked example (numbers from `rt_intro_data.py`)
| Claim | Source | Note |
|---|---|---|
| 0.020 in (0.51 mm) for thickness under 2 in | [ASME-V-2010] T-274.2 table "Under 2 (50) … 0.020 (0.51)" | ✓ value; wording corrected to "recommended maximum" |
| Ug1 = 3.0 × 20 / 400 = 0.15 mm; Ug2 = 0.30 mm; ratio 2; Dmin = 117.647… mm | arithmetic, `rt_intro_data.self_test()` | ✓ |
