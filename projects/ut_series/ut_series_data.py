"""ut_series: every number shown or spoken in the videos (illustrative values only).

Inputs are typed once here; everything derived is computed, never typed by hand.
self_test() runs on import so a drift stops every script that uses the data.

Sources: IAEA-TCS-67 (2017), Table 2.1 (p. 104), §2.2.4 (p. 102), §2.3.5 (p. 108),
§2.4.1 (pp. 109-111). Every velocity and density below is the value of TCS-67 Table 2.1
(steel = the row "steel (calibration block)", shear velocity 3250 m/s from the same table;
air = 330 m/s, 1.3 kg/m3). Owner decision 2026-10-02: TCS-67 values replace the first draft's
3240 m/s, 343 m/s and 1.2 kg/m3.

    python projects/ut_series/ut_series_data.py      # print the table
"""
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


def self_test():
    assert V_L_STEEL > V_S_STEEL > 0 and V_WATER > 0 and V_AIR > 0
    assert V_L_ALUMINIUM > V_L_STEEL
    assert RHO_STEEL > RHO_WATER > RHO_AIR > 0
    assert 0 < FLAW_DEPTH < THICKNESS
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
            ("reading at Al velocity", f"{READING_AL:.3f}", "mm")]
    for name, value, unit in rows:
        print(f"  {name:<26} {value:>16} {unit}")


if __name__ == "__main__":
    print_table()
