"""ut_series: every number shown or spoken in the videos (illustrative values only).

Inputs are typed once here; everything derived is computed, never typed by hand.
self_test() runs on import so a drift stops every script that uses the data.

Sources: IAEA-TCS-67 (2017), Table 2.1 (p. 104), §2.2.4 (p. 102), §2.3.5 (p. 108),
§2.4.1 (pp. 109-111); episode 2: §2.7.1.2 eq. 2.18 (p. 125), §2.7.2 eq. 2.19 and Tables 2.3-2.4
(pp. 126-127); episode 3: §2.4.2.2 (pp. 113-114), Fig. 5.1 and Table 5.4 (pp. 178, 192),
§8.4.1 (p. 279), eqs. 6.2-6.5 (p. 215). Every velocity and density below is the value of TCS-67 Table 2.1
(steel = the row "steel (calibration block)", shear velocity 3250 m/s from the same table;
air = 330 m/s, 1.3 kg/m3). Owner decision 2026-10-02: TCS-67 values replace the first draft's
3240 m/s, 343 m/s and 1.2 kg/m3.

    python projects/ut_series/ut_series_data.py      # print the table
"""
import math

# ---------------- Inputs (illustrative) ----------------
V_L_STEEL = 5920.0         # m/s   longitudinal wave in steel
V_S_STEEL = 3250.0         # m/s   shear (transverse) wave in steel (TCS-67 Table 2.1)
V_WATER = 1480.0           # m/s   longitudinal wave in water
V_AIR = 330.0              # m/s   sound in air (TCS-67 Table 2.1)
V_L_ALUMINIUM = 6320.0     # m/s   longitudinal wave in aluminium

RHO_STEEL = 7850.0         # kg/m3
RHO_WATER = 1000.0         # kg/m3
RHO_AIR = 1.3              # kg/m3 (TCS-67 Table 2.1)

F_PROBE = 5.0              # MHz
THICKNESS = 25.0           # mm    steel plate
FLAW_DEPTH = 12.0          # mm    flaw below the probe surface

# ---- Episode 2: the probe and the beam (V_L_STEEL above is the steel velocity) ----
PROBE_D_MM = 10.0          # mm    crystal diameter of the worked example (TCS-67 p. 128 uses 10 mm too)
PROBE_F_MHZ = 4.0          # MHz   its frequency
BEAM_K_EDGE = 1.22         # K of eq. 2.19 for the 0 % (extreme) edge of a circular crystal (Tables 2.3, 2.4)
BEAM_CASES = [             # (frequency MHz, diameter mm) shown as results only: the three cones
    (4.0, 10.0),           # reference
    (2.0, 10.0),           # lower frequency -> wider
    (4.0, 20.0),           # bigger crystal -> narrower
]

# ---- Episode 3: calibration and angle-beam testing ----
V_L_PERSPEX = 2730.0       # m/s   longitudinal wave in perspex (TCS-67 Table 2.1, p. 104; p. 114)
V1_THICKNESS = 25.0        # mm    IIW V1 block, the normal-beam path (Fig. 5.1, p. 178)
V1_RANGE = 100.0           # mm    screen range of the calibration (Table 5.4, position C, p. 192)
V1_QUADRANT_R = 100.0      # mm    radius of the V1 quadrant (angle probes: exit point and range)
V1_HOLE_D = 1.5            # mm    small through hole (probe-angle check)
V1_BIG_HOLE_D = 50.0       # mm    large hole with its plastic insert
PLATE_T = 30.0             # mm    plate of the skip example
PROBE_ANGLE = 60.0         # deg   shear-wave angle in steel written on the probe
PATH_S = 50.0              # mm    sound path read on the calibrated screen (the worked example)

# Ranges quoted from TCS-67 (audible range §2.1 p. 99; UT range §1.1.2.6 p. 9; penetration p. 9)
AUDIBLE_MIN_HZ = 20        # Hz
AUDIBLE_MAX_KHZ = 20       # kHz
UT_MIN_MHZ = 0.5           # MHz   most UT is done between UT_MIN_MHZ and UT_MAX_MHZ
UT_MAX_MHZ = 20            # MHz
PENETRATION_M = (6, 7)     # m of steel

# ---------------- Derived ----------------
def derive():
    """Everything computed from the inputs."""
    d = {}
    f_hz = F_PROBE * 1e6
    d["LAMBDA_STEEL"] = V_L_STEEL / f_hz * 1e3                    # mm
    d["LAMBDA_WATER"] = V_WATER / f_hz * 1e3                      # mm
    d["LAMBDA_STEEL_M"] = V_L_STEEL / f_hz                        # m
    d["MIN_FLAW_HALF"] = d["LAMBDA_STEEL"] / 2                    # mm  (about lambda/2)
    d["MIN_FLAW_THIRD"] = d["LAMBDA_STEEL"] / 3                   # mm  (about lambda/3)
    d["SHEAR_RATIO"] = V_S_STEEL / V_L_STEEL
    d["Z_STEEL"] = RHO_STEEL * V_L_STEEL / 1e6                    # MRayl
    d["Z_WATER"] = RHO_WATER * V_WATER / 1e6                      # MRayl
    d["Z_AIR"] = RHO_AIR * V_AIR                                  # Rayl
    z_steel, z_water, z_air = d["Z_STEEL"] * 1e6, d["Z_WATER"] * 1e6, d["Z_AIR"]
    d["R_STEEL_WATER"] = ((z_water - z_steel) / (z_water + z_steel)) ** 2
    d["T_STEEL_WATER"] = 1 - d["R_STEEL_WATER"]
    d["R_STEEL_AIR"] = ((z_air - z_steel) / (z_air + z_steel)) ** 2
    d["T_STEEL_AIR"] = 1 - d["R_STEEL_AIR"]
    d["T_BACKWALL_US"] = 2 * (THICKNESS / 1e3) / V_L_STEEL * 1e6   # us
    d["T_FLAW_US"] = 2 * (FLAW_DEPTH / 1e3) / V_L_STEEL * 1e6      # us
    d["FLAW_DEPTH_FROM_T"] = V_L_STEEL * round(d["T_FLAW_US"], 3) * 1e-6 / 2 * 1e3   # mm, from 4.054 us
    d["READING_AL"] = V_L_ALUMINIUM * d["T_BACKWALL_US"] * 1e-6 / 2 * 1e3            # mm
    # ---- episode 2 ----
    d["LAMBDA_EP2"] = V_L_STEEL / (PROBE_F_MHZ * 1e6) * 1e3                           # mm
    d["NEAR_FIELD"] = PROBE_D_MM ** 2 / (4 * d["LAMBDA_EP2"])                          # mm, eq. 2.18
    d["BEAM_HALF_ANGLES"] = []                                                         # deg, eq. 2.19
    d["NEAR_FIELDS"] = []                                                              # mm
    for f_mhz, dia in BEAM_CASES:
        lam = V_L_STEEL / (f_mhz * 1e6) * 1e3
        d["BEAM_HALF_ANGLES"].append(math.degrees(math.asin(BEAM_K_EDGE * lam / dia)))
        d["NEAR_FIELDS"].append(dia ** 2 / (4 * lam))
    # ---- episode 3 ----
    d["CRIT_1"] = math.degrees(math.asin(V_L_PERSPEX / V_L_STEEL))                     # deg, first critical angle
    d["CRIT_2"] = math.degrees(math.asin(V_L_PERSPEX / V_S_STEEL))                     # deg, second critical angle
    th = math.radians(PROBE_ANGLE)
    d["DEPTH"] = PATH_S * math.cos(th)                                                 # mm, d = R cos(theta) (p. 279)
    d["SURFACE_DIST"] = PATH_S * math.sin(th)                                          # mm, from the exit point
    d["HALF_SKIP"] = PLATE_T * math.tan(th)                                            # mm, eq. 6.2
    d["FULL_SKIP"] = 2 * PLATE_T * math.tan(th)                                        # mm, eq. 6.3
    d["HALF_SKIP_PATH"] = PLATE_T / math.cos(th)                                       # mm, eq. 6.4
    d["V1_ECHOES"] = [V1_THICKNESS * k for k in range(1, int(V1_RANGE // V1_THICKNESS) + 1)]   # mm on the screen
    return d


_D = derive()
LAMBDA_STEEL = _D["LAMBDA_STEEL"]                 # 1.184 mm
LAMBDA_WATER = _D["LAMBDA_WATER"]                 # 0.296 mm
LAMBDA_STEEL_M = _D["LAMBDA_STEEL_M"]             # 0.001184 m
MIN_FLAW_HALF = _D["MIN_FLAW_HALF"]               # 0.592 mm
MIN_FLAW_THIRD = _D["MIN_FLAW_THIRD"]             # 0.395 mm
SHEAR_RATIO = _D["SHEAR_RATIO"]                   # 0.549
Z_STEEL = _D["Z_STEEL"]                           # 46.472 MRayl
Z_WATER = _D["Z_WATER"]                           # 1.48 MRayl
Z_AIR = _D["Z_AIR"]                               # 429 Rayl
R_STEEL_WATER = _D["R_STEEL_WATER"]               # 0.88035
T_STEEL_WATER = _D["T_STEEL_WATER"]
R_STEEL_AIR = _D["R_STEEL_AIR"]                   # 0.999963
T_STEEL_AIR = _D["T_STEEL_AIR"]
T_BACKWALL_US = _D["T_BACKWALL_US"]               # 8.4459 us
T_FLAW_US = _D["T_FLAW_US"]                       # 4.0541 us
FLAW_DEPTH_FROM_T = _D["FLAW_DEPTH_FROM_T"]       # 12.0 mm
READING_AL = _D["READING_AL"]                     # 26.689 mm
READING_AL_FACTOR = V_L_ALUMINIUM / V_L_STEEL     # displayed / true thickness

# episode 2
LAMBDA_EP2 = _D["LAMBDA_EP2"]                     # 1.48 mm
NEAR_FIELD = _D["NEAR_FIELD"]                     # 16.892 mm
BEAM_HALF_ANGLES = _D["BEAM_HALF_ANGLES"]         # [10.40, 21.17, 5.18] deg to the beam edge
NEAR_FIELDS = _D["NEAR_FIELDS"]                   # mm, for the three cones
# episode 3
CRIT_1 = _D["CRIT_1"]                             # 27.46 deg
CRIT_2 = _D["CRIT_2"]                             # 57.14 deg
DEPTH = _D["DEPTH"]                               # 25.000 mm
SURFACE_DIST = _D["SURFACE_DIST"]                 # 43.301 mm
HALF_SKIP = _D["HALF_SKIP"]                       # 51.962 mm
FULL_SKIP = _D["FULL_SKIP"]                       # 103.923 mm
HALF_SKIP_PATH = _D["HALF_SKIP_PATH"]             # 60.000 mm
V1_ECHOES = _D["V1_ECHOES"]                       # [25, 50, 75, 100] mm


def self_test():
    assert V_L_STEEL > V_S_STEEL > 0 and V_WATER > 0 and V_AIR > 0
    assert V_L_ALUMINIUM > V_L_STEEL
    assert RHO_STEEL > RHO_WATER > RHO_AIR > 0
    assert 0 < FLAW_DEPTH < THICKNESS
    assert AUDIBLE_MIN_HZ < AUDIBLE_MAX_KHZ * 1e3 < UT_MIN_MHZ * 1e6 < F_PROBE * 1e6 < UT_MAX_MHZ * 1e6
    assert PENETRATION_M == (6, 7)
    # the expected results of the brief, each to its stated precision
    assert abs(LAMBDA_STEEL - 1.184) < 1e-9, LAMBDA_STEEL
    assert abs(LAMBDA_WATER - 0.296) < 1e-9, LAMBDA_WATER
    assert abs(LAMBDA_STEEL_M - 0.001184) < 1e-12, LAMBDA_STEEL_M
    assert abs(SHEAR_RATIO - 0.549) < 5e-4, SHEAR_RATIO
    assert abs(Z_STEEL - 46.472) < 1e-9, Z_STEEL
    assert abs(Z_WATER - 1.48) < 1e-9, Z_WATER
    assert abs(Z_AIR - 429.0) < 1e-9, Z_AIR
    assert abs(R_STEEL_WATER - 0.88035) < 5e-6, R_STEEL_WATER
    assert abs(R_STEEL_AIR - 0.999963) < 5e-7, R_STEEL_AIR
    assert abs(R_STEEL_WATER + T_STEEL_WATER - 1) < 1e-12
    assert abs(R_STEEL_AIR + T_STEEL_AIR - 1) < 1e-12
    assert abs(T_BACKWALL_US - 8.4459) < 5e-5, T_BACKWALL_US
    assert abs(T_FLAW_US - 4.0541) < 5e-5, T_FLAW_US
    assert abs(READING_AL - 26.689) < 5e-4, READING_AL
    assert abs(FLAW_DEPTH_FROM_T - 12.0) < 1e-3, FLAW_DEPTH_FROM_T
    # the flaw echo is exactly at the middle of the plate's round trip (12 mm is not 25/2, so
    # it is checked as a ratio of times, not assumed)
    assert abs(T_FLAW_US / T_BACKWALL_US - FLAW_DEPTH / THICKNESS) < 1e-12
    # the figures spoken and shown, as text, from the values above
    assert f"{R_STEEL_WATER * 100:.1f}" == "88.0"
    assert f"{R_STEEL_AIR * 100:.3f}" == "99.996"
    assert f"{SHEAR_RATIO:.2f}" == "0.55"
    assert f"{T_BACKWALL_US:.2f}" == "8.45" and f"{T_FLAW_US:.2f}" == "4.05"
    assert f"{READING_AL:.1f}" == "26.7"
    assert f"{Z_AIR:.0f}" == "429" and int(V_S_STEEL) == 3250
    # ---- episode 2 ----
    assert abs(LAMBDA_EP2 - 1.48) < 1e-9, LAMBDA_EP2
    assert abs(NEAR_FIELD - 16.892) < 5e-4, NEAR_FIELD
    assert f"{NEAR_FIELD:.1f}" == "16.9" and round(NEAR_FIELD) == 17
    assert abs(NEAR_FIELD - PROBE_D_MM ** 2 * PROBE_F_MHZ * 1e6 / (4 * V_L_STEEL * 1e3)) < 1e-9   # D2 f / 4 v, eq. 2.18
    assert len(BEAM_HALF_ANGLES) == 3
    for got, want in zip(BEAM_HALF_ANGLES, (10.40, 21.17, 5.18)):
        assert abs(got - want) < 5e-3, (got, want)
    assert [f"{a:.2f}" for a in BEAM_HALF_ANGLES] == ["10.40", "21.17", "5.18"]
    # the stated trends: lower frequency or smaller crystal -> wider beam; bigger crystal -> longer near field
    assert BEAM_HALF_ANGLES[1] > BEAM_HALF_ANGLES[0] > BEAM_HALF_ANGLES[2]
    assert NEAR_FIELDS[2] > NEAR_FIELDS[0] > NEAR_FIELDS[1]
    # ---- episode 3 ----
    assert V_L_PERSPEX < V_S_STEEL < V_L_STEEL                  # a wedge needs v(perspex) < v(shear in steel)
    assert abs(CRIT_1 - 27.46) < 5e-3, CRIT_1
    assert abs(CRIT_2 - 57.14) < 5e-3, CRIT_2
    assert f"{CRIT_1:.2f}" == "27.46" and f"{CRIT_2:.2f}" == "57.14"
    assert CRIT_1 < CRIT_2 < 90
    assert abs(DEPTH - 25.000) < 5e-4, DEPTH
    assert abs(SURFACE_DIST - 43.301) < 5e-4, SURFACE_DIST
    assert abs(HALF_SKIP - 51.962) < 5e-4, HALF_SKIP
    assert abs(FULL_SKIP - 103.923) < 5e-4, FULL_SKIP
    assert abs(HALF_SKIP_PATH - 60.000) < 5e-4, HALF_SKIP_PATH
    assert abs(FULL_SKIP - 2 * HALF_SKIP) < 1e-9
    assert abs(DEPTH ** 2 + SURFACE_DIST ** 2 - PATH_S ** 2) < 1e-9             # the same right triangle
    assert DEPTH < PLATE_T                                       # the example flaw is on the first leg
    assert PATH_S < HALF_SKIP_PATH                               # ... and the path ends before the back wall
    assert abs(HALF_SKIP_PATH * math.cos(math.radians(PROBE_ANGLE)) - PLATE_T) < 1e-9
    assert V1_ECHOES == [25.0, 50.0, 75.0, 100.0] and V1_ECHOES[-1] == V1_RANGE
    assert f"{DEPTH:.1f}" == "25.0" and f"{SURFACE_DIST:.1f}" == "43.3"
    assert f"{HALF_SKIP:.1f}" == "52.0" and f"{FULL_SKIP:.1f}" == "103.9"


self_test()


def print_table():
    rows = [("lambda steel", f"{LAMBDA_STEEL:.3f}", "mm"),
            ("lambda water", f"{LAMBDA_WATER:.3f}", "mm"),
            ("lambda/2, lambda/3 steel", f"{MIN_FLAW_HALF:.3f} / {MIN_FLAW_THIRD:.3f}", "mm"),
            ("Vs / Vl steel", f"{SHEAR_RATIO:.3f}", ""),
            ("Z steel", f"{Z_STEEL:.3f}", "MRayl"),
            ("Z water", f"{Z_WATER:.3f}", "MRayl"),
            ("Z air", f"{Z_AIR:.1f}", "Rayl"),
            ("R steel-water", f"{R_STEEL_WATER:.5f}", ""),
            ("R steel-air", f"{R_STEEL_AIR:.6f}", ""),
            ("T steel-water", f"{T_STEEL_WATER:.5f}", ""),
            ("back-wall time", f"{T_BACKWALL_US:.4f}", "us"),
            ("flaw time", f"{T_FLAW_US:.4f}", "us"),
            ("flaw depth from 4.054 us", f"{FLAW_DEPTH_FROM_T:.3f}", "mm"),
            ("reading at Al velocity", f"{READING_AL:.3f}", "mm"),
            ("ep2 lambda (4 MHz, steel)", f"{LAMBDA_EP2:.3f}", "mm"),
            ("ep2 near field N", f"{NEAR_FIELD:.3f}", "mm"),
            ("ep2 beam half angles", " / ".join(f"{a:.2f}" for a in BEAM_HALF_ANGLES), "deg"),
            ("ep3 critical angles", f"{CRIT_1:.2f} / {CRIT_2:.2f}", "deg"),
            ("ep3 depth, surface distance", f"{DEPTH:.3f} / {SURFACE_DIST:.3f}", "mm"),
            ("ep3 half / full skip", f"{HALF_SKIP:.3f} / {FULL_SKIP:.3f}", "mm"),
            ("ep3 half-skip path", f"{HALF_SKIP_PATH:.3f}", "mm")]
    for name, value, unit in rows:
        print(f"  {name:<26} {value:>16} {unit}")


if __name__ == "__main__":
    print_table()
