# takeoff_lift — sources (claim → source → note)

Official sources (priority 1), checked 2026-09-30:
- **PHAK** = FAA, *Pilot's Handbook of Aeronautical Knowledge*, FAA-H-8083-25C (2023):
  https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/faa-h-8083-25c.pdf
- **AFH** = FAA, *Airplane Flying Handbook*, FAA-H-8083-3C:
  https://www.faa.gov/sites/faa.gov/files/regulations_policies/handbooks_manuals/aviation/airplane_handbook/00_afh_full.pdf
- **14 CFR 1.2** (definitions) and **14 CFR 25.107** (takeoff speeds), eCFR, up to date as of 2026-09-15:
  https://www.ecfr.gov/current/title-14/part-1/section-1.2 · https://www.ecfr.gov/current/title-14/part-25/section-25.107
- **NASA GRC** = NASA Glenn Research Center, *Incorrect Lift Theory* (equal transit):
  https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/wrong1.html

Page numbers are the printed page numbers of the handbooks.

| Seg | Claim (as narrated) | Source | Note |
|---|---|---|---|
| 1 | Educational-material sentence | root CLAUDE.md rule | technical, regulated topic |
| 2 | Four forces: lift up, weight down, thrust forward, drag back | PHAK 3-2, 5-1 | "thrust, drag, lift, and weight" |
| 2 | Weight = mass × gravity | PHAK 5-1 ("weight … force of gravity") | 70 000 × 9.81 = 686 700 N from the data module |
| 2 | Thrust > drag → the aircraft accelerates | PHAK 5-2, 5-3 | "For an aircraft to start moving, thrust must be exerted and be greater than drag"; "As long as the thrust continues to be greater than the drag, the aircraft continues to accelerate" |
| 2 | Lift grows with speed until it exceeds the weight | PHAK 5-4, 11-15 | lift ∝ V²; lift-off at the takeoff lift coefficient |
| 3 | [+] Chord line = straight line from leading edge to trailing edge | PHAK Glossary G-6 | needed to define the angle of attack |
| 3 | Angle of attack = angle between the chord line and the relative wind | PHAK 5-2 | "the acute angle between the chord line of the airfoil and the direction of the relative wind" |
| 3 | The wing turns the air down; reaction pushes the wing up (Newton 3) | PHAK 4-6, 4-8 | "downwash … Applying Newton's third law, the reaction … results in an upward forward force" |
| 3 | Pressure above lower than below (Bernoulli) | PHAK 4-6, 4-7, 4-8 | Bernoulli's principle of differential pressure |
| 3 | Two views of one phenomenon | PHAK 4-8 | "Both Bernoulli's Principle and Newton's Laws are in operation whenever lift is being generated" |
| 3 | More AoA → more lift up to a critical angle, then stall | PHAK 5-3, 5-5 (C_L curve peaks at the critical AoA), 5-25 | |
| 3 | [+] Stall = air separates from the wing surface, lift decreases rapidly | PHAK 5-25, Glossary G-28 | "a rapid decrease in lift caused by the separation of airflow from the wing's surface"; PHAK 5-25 warns that lift does not drop to zero, so the narration says "decreases rapidly", not "disappears" |
| 3 | Equal-transit myth is wrong; the air over the top arrives earlier | NASA GRC | "particles moving over the top arrive at the trailing edge before particles moving under the airfoil" |
| 4 | L = ½ ρ V² S C_L | PHAK 5-4 | written there as L = C_L · ρ · V²/2 · S |
| 4 | C_L depends on AoA and flaps; flaps raise it → takeoff at a lower speed | PHAK 5-5 (C_L vs AoA), 6-8 (flaps raise C_L), 5-50 (high-lift devices improve low-speed characteristics in takeoff; lower stall speed) | |
| 4 | Twice the speed → four times the lift | PHAK 5-4 | "an airplane traveling at 200 knots has four times the lift as the same airplane traveling at 100 knots" |
| 4 | V for L = W: 76.4 m/s ≈ 275 km/h | takeoff_data.py | illustrative inputs; this is the speed at which lift equals weight at C_L = 1.6, not a certified V-speed |
| 5 | V1 = maximum speed at which the pilot must take the first action to stop within the accelerate-stop distance | 14 CFR 1.2; AFH 16-12 | **corrected** (see below) |
| 5 | Before V1 reject on a serious failure, after V1 continue | AFH 16-12, 16-15; 14 CFR 1.2 (second sentence of the V1 definition) | "At speeds less than V1, it is considered safer to stop …" |
| 5 | VR = rotation speed; nose up → more AoA → more lift | 14 CFR 1.2; AFH 13-1, 16-12 | "speed at which back pressure is applied to rotate the airplane to a takeoff attitude" |
| 5 | V2 = takeoff safety speed, reached after lift-off | 14 CFR 1.2; AFH 16-12; 14 CFR 25.107(c)(2) | "a referenced airspeed obtained after lift-off"; V2 ≥ VR + the increment gained before 35 ft |
| 5 | V1 does not exceed VR | 14 CFR 25.107(e)(1)(i); AFH 16-12 | "VR … may not be less than V1" |
| 6 | Hot air is less dense | PHAK 5-5 | "Warm air is less dense than cool air" |
| 6 | Hot air → higher speed relative to the air, longer runway, same indicated airspeed | PHAK 5-5, 11-4, 11-16 | **corrected/precised** (see below) |
| 6 | Headwind helps: lift depends on airspeed, not ground speed | PHAK 11-15 | "The effect of a headwind is to allow the aircraft to reach the lift-off speed at a lower groundspeed" |
| 6 | Heavier → higher speed, V ∝ √W | PHAK 11-15 | "a 21 percent increase in takeoff weight requires a 10 percent increase in lift-off speed" (√1.21 = 1.10) |
| 6 | 45 °C → ρ ≈ 1.11, V 80.3 m/s (+5 %); headwind 10 m/s → 66.4 m/s ground speed; +10 % weight → +4.9 % | takeoff_data.py | ρ = p/(R T) at sea-level standard pressure |

## Corrections to the cleaned source (the source file itself is kept verbatim)
1. **V1** — source: «أعلى سرعة *يمكن* أن يبدأ عندها الطيار الإيقاف ليتوقف ضمن *المسافة المتاحة*».
   Official: "the maximum speed in the takeoff at which the pilot **must take the first action** (e.g., apply
   brakes, reduce thrust, deploy speed brakes) to stop the airplane within the **accelerate-stop distance**"
   (14 CFR 1.2; AFH 16-12). Narration: «أَعْلَى سُرْعَةٍ يَتَّخِذُ عِنْدَهَا الطَّيَّارُ أَوَّلَ إِجْرَاءٍ لِلْإِيقَافِ، لِيَتَوَقَّفَ ضِمْنَ مَسَافَةِ التَّسَارُعِ وَالتَّوَقُّفِ».
2. **Hot air** — source: «فتحتاج الطائرة سرعة أعلى». Official: at a higher density altitude the airplane
   "takes off at the same indicated airspeed (IAS) as at sea level, but because of the reduced air density,
   the TAS is greater" (PHAK 11-16; also 5-5). Narration: the speed *relative to the air* is higher, while the
   cockpit airspeed indicator shows the same value.
