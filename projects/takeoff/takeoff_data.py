"""takeoff: every number shown or spoken in the video (illustrative values only).

A generic airliner (no real type, no airline). Inputs are typed once here; everything
derived is computed at full precision, never typed by hand. self_test() runs on import so
a drift stops the script that uses the data.

    python projects/takeoff/takeoff_data.py      # print the table
"""
import math

# ---------------- Inputs (illustrative) ----------------
MASS = 70000.0             # kg (70 t)
G = 9.81                   # m/s²
WING_AREA = 120.0          # m², S
CL_TAKEOFF = 1.6           # lift coefficient with takeoff flaps
RHO_15 = 1.225             # kg/m³, sea-level standard air at 15 °C
P0 = 101325.0              # Pa, sea-level standard pressure
R_AIR = 287.05             # J/(kg·K), specific gas constant of dry air
T_HOT = 318.15             # K (45 °C)
HEADWIND = 10.0            # m/s
WEIGHT_INCREASE = 0.10     # +10 %

# ---------------- Derived ----------------
WEIGHT = MASS * G                                       # N
RHO_HOT = P0 / (R_AIR * T_HOT)                          # kg/m³ at 45 °C, same pressure
T_HOT_C = T_HOT - 273.15                                # °C


def speed_for_lift(weight, rho, area=WING_AREA, cl=CL_TAKEOFF):
    """Speed (m/s, relative to the air) at which L = ½ ρ V² S C_L equals the weight."""
    return math.sqrt(2 * weight / (rho * area * cl))


def lift(v, rho=RHO_15, area=WING_AREA, cl=CL_TAKEOFF):
    """L = ½ ρ V² S C_L (N)."""
    return 0.5 * rho * v ** 2 * area * cl


V_15 = speed_for_lift(WEIGHT, RHO_15)                   # m/s, airspeed at 15 °C
V_15_KMH = V_15 * 3.6                                   # km/h
V_HOT = speed_for_lift(WEIGHT, RHO_HOT)                 # m/s, airspeed at 45 °C
V_HOT_KMH = V_HOT * 3.6
HOT_INCREASE = V_HOT / V_15 - 1                         # fraction (~5 %)
V_GROUND_HEADWIND = V_15 - HEADWIND                     # m/s, ground speed at lift-off
WEIGHT_HEAVY = WEIGHT * (1 + WEIGHT_INCREASE)           # N
V_HEAVY = speed_for_lift(WEIGHT_HEAVY, RHO_15)          # m/s
HEAVY_INCREASE = V_HEAVY / V_15 - 1                     # fraction (~4.9 %) = √1.1 − 1
LIFT_RATIO_DOUBLE_SPEED = lift(2 * V_15) / lift(V_15)   # 4


def self_test():
    assert MASS > 0 and WING_AREA > 0 and CL_TAKEOFF > 0 and T_HOT > 273.15
    assert abs(WEIGHT - 686700.0) < 1e-6, WEIGHT
    assert abs(RHO_HOT - 1.1095) < 5e-4, RHO_HOT
    assert abs(P0 / (R_AIR * 288.15) - RHO_15) < 1e-3            # RHO_15 is consistent with P0, R
    assert abs(V_15 - 76.4) < 0.05 and abs(V_15_KMH - 275) < 0.5, (V_15, V_15_KMH)
    assert abs(V_HOT - 80.3) < 0.05, V_HOT
    assert abs(HOT_INCREASE - 0.05) < 0.005, HOT_INCREASE
    assert abs(V_GROUND_HEADWIND - 66.4) < 0.05, V_GROUND_HEADWIND
    assert abs(HEAVY_INCREASE - (math.sqrt(1 + WEIGHT_INCREASE) - 1)) < 1e-12
    assert abs(HEAVY_INCREASE - 0.049) < 0.0005, HEAVY_INCREASE
    assert abs(LIFT_RATIO_DOUBLE_SPEED - 4.0) < 1e-12
    assert abs(lift(V_15) - WEIGHT) < 1e-6                       # L = W at V_15


self_test()


def print_table():
    rows = [("Mass", f"{MASS:,.0f}", "kg"), ("Weight W = m g", f"{WEIGHT:,.0f}", "N"),
            ("Wing area S", f"{WING_AREA:.0f}", "m²"), ("C_L (takeoff flaps)", f"{CL_TAKEOFF}", ""),
            ("ρ at 15 °C", f"{RHO_15:.3f}", "kg/m³"), ("ρ at 45 °C", f"{RHO_HOT:.4f}", "kg/m³"),
            ("V (L = W) at 15 °C", f"{V_15:.2f}", "m/s"), ("  = ", f"{V_15_KMH:.1f}", "km/h"),
            ("V (L = W) at 45 °C", f"{V_HOT:.2f}", "m/s"), ("  = ", f"{V_HOT_KMH:.1f}", "km/h"),
            ("  increase", f"{HOT_INCREASE * 100:.2f}", "%"),
            ("Ground speed, 10 m/s headwind", f"{V_GROUND_HEADWIND:.2f}", "m/s"),
            ("V, weight +10 %", f"{V_HEAVY:.2f}", "m/s"),
            ("  increase", f"{HEAVY_INCREASE * 100:.2f}", "%"),
            ("Lift ratio at 2 V", f"{LIFT_RATIO_DOUBLE_SPEED:.0f}", "×")]
    for name, value, unit in rows:
        print(f"  {name:<32} {value:>10} {unit}")


if __name__ == "__main__":
    print_table()
