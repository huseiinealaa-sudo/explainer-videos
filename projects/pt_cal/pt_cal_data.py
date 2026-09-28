"""pt_cal: every number shown or spoken in the series (illustrative values only).

Inputs are typed once here (illustrative, or published manual values with their source);
everything derived is computed at full precision and rounded only for display.
self_test() runs on import, so a drift stops every script that uses the data.

    python projects/pt_cal/pt_cal_data.py      # print the tables
"""
import math

# =====================================================================
# Transmitter under test (illustrative; the only tag used is PT-101)
# =====================================================================
TAG = "PT-101"
UNIT = "kg/cm²"                 # on-screen unit (kgf/cm²)
LRV = 0.0                       # kg/cm²
URV = 42.0                      # kg/cm²
SPAN = URV - LRV
I_LO, I_HI = 4.0, 20.0          # mA
I_SPAN = I_HI - I_LO            # 16 mA
TOL_PCT = 0.50                  # ± % of span (from the work order, illustrative)
TOL_ABS = TOL_PCT / 100 * SPAN  # kg/cm²

KGF_CM2_TO_BAR = 0.980665       # exact by definition (1 kgf/cm² = 98 066.5 Pa)


def i_linear(pv):
    """Expected current of a linear transmitter at the input pv."""
    return I_LO + (pv - LRV) / (URV - LRV) * I_SPAN


def i_sqrt(pv):
    """Expected current of a square-root transmitter at the input pv."""
    return I_LO + I_SPAN * math.sqrt((pv - LRV) / (URV - LRV))


def err_pct(i_meas, i_exp):
    """Error in % of the output span."""
    return (i_meas - i_exp) / I_SPAN * 100


# =====================================================================
# Ep 5 — the 41.928 example: nominal vs actual input
# =====================================================================
PV_NOMINAL = 42.000
PV_ACTUAL = 41.928              # what the pump actually reached
I_MEASURED = 20.0320            # mA

I_EXP_NOMINAL = i_linear(PV_NOMINAL)            # 20.000 (the Excel mistake)
I_EXP_ACTUAL = i_linear(PV_ACTUAL)              # 19.97257…
ERR_MA_WRONG = I_MEASURED - I_EXP_NOMINAL
ERR_MA_RIGHT = I_MEASURED - I_EXP_ACTUAL
ERR_PCT_WRONG = err_pct(I_MEASURED, I_EXP_NOMINAL)     # 0.200 %
ERR_PCT_RIGHT = err_pct(I_MEASURED, I_EXP_ACTUAL)      # 0.3714 %
PUMP_EFFECT_PCT = ERR_PCT_RIGHT - ERR_PCT_WRONG         # 0.1714 %
TOL_USED_WRONG = abs(ERR_PCT_WRONG) / TOL_PCT * 100     # 40 %
TOL_USED_RIGHT = abs(ERR_PCT_RIGHT) / TOL_PCT * 100     # 74.3 %
PASS_41928 = abs(ERR_PCT_RIGHT) <= TOL_PCT

# =====================================================================
# Ep 5 — square-root table (and Ep 3 DP example)
# =====================================================================
SQRT_POINTS_PCT = [0, 10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90, 100]
SQRT_TABLE = [(p, i_linear(LRV + p / 100 * SPAN), i_sqrt(LRV + p / 100 * SPAN))
              for p in SQRT_POINTS_PCT]
# values the owner's original guide printed wrongly or truncated (listed in the conflicts)
SQRT_GUIDE_ERRORS = {30: 12.762, 90: 19.177}
SQRT_GUIDE_TRUNCATED = {10: 9.059, 60: 16.393, 70: 17.386}
DP_50_SQRT_MA = I_LO + I_SPAN * math.sqrt(0.5)          # 15.314 mA
DP_50_LINEAR_MA = I_LO + I_SPAN * 0.5                   # 12 mA
# what a linear procedure reports for a square-root transmitter at 50 % (the "trap")
TRAP_50_ERR_PCT = err_pct(DP_50_SQRT_MA, DP_50_LINEAR_MA)   # 20.7 % of span

# =====================================================================
# Ep 6 — error-pattern example (errors in % of span), least-squares line
# =====================================================================
PATTERN_X = [0, 25, 50, 75, 100]                         # % of span
PATTERN_E = [0.37, 0.22, 0.03, -0.14, -0.30]             # % of span
_n = len(PATTERN_X)
_mx = sum(PATTERN_X) / _n
_me = sum(PATTERN_E) / _n
PATTERN_SLOPE = (sum((x - _mx) * (e - _me) for x, e in zip(PATTERN_X, PATTERN_E))
                 / sum((x - _mx) ** 2 for x in PATTERN_X))       # % per % of span
PATTERN_INTERCEPT = _me - PATTERN_SLOPE * _mx                    # % at 0 %
PATTERN_FIT = [PATTERN_INTERCEPT + PATTERN_SLOPE * x for x in PATTERN_X]
PATTERN_RESID = [e - f for e, f in zip(PATTERN_E, PATTERN_FIT)]
PATTERN_MAX_RESID = max(abs(r) for r in PATTERN_RESID)
PATTERN_MAX_ERR = max(abs(e) for e in PATTERN_E)
PATTERN_PASS = PATTERN_MAX_ERR <= TOL_PCT

# URV-change mistake (Ep 6): 12.5 mA at 50 % of a 0–10 bar transmitter, URV 10 -> 10.5 bar
MIS_URV_OLD, MIS_URV_NEW = 10.0, 10.5                    # bar
MIS_I_AT_50 = 12.5                                       # mA

# =====================================================================
# Ep 7 — uncertainty budget (kg/cm²) at the 100 % point, GUM
# =====================================================================
K = 2
A_REF = 0.0153          # reference pressure module, rectangular half-width
A_CURRENT = 0.0130      # current measurement (expressed in kg/cm²), rectangular
D_RES = 0.0010          # display resolution
S_REPEAT = 0.0080       # repeatability, standard deviation
A_TEMP = 0.0050         # temperature effect, rectangular
A_STAB = 0.0100         # pressure stability at capture, rectangular
BUDGET = [  # (name, input, divisor text, standard uncertainty)
    ("Reference module", A_REF, "a/√3", A_REF / math.sqrt(3)),
    ("Current measurement", A_CURRENT, "a/√3", A_CURRENT / math.sqrt(3)),
    ("Display resolution", D_RES, "d/(2√3)", D_RES / (2 * math.sqrt(3))),
    ("Repeatability", S_REPEAT, "s", S_REPEAT),
    ("Temperature", A_TEMP, "a/√3", A_TEMP / math.sqrt(3)),
    ("Pressure stability", A_STAB, "a/√3", A_STAB / math.sqrt(3)),
]
U_C = math.sqrt(sum(b[3] ** 2 for b in BUDGET))          # 0.01550 kg/cm²
U_EXP = K * U_C                                          # 0.03099 kg/cm²
U_EXP_PCT = U_EXP / SPAN * 100                           # 0.0738 % of span
TUR = TOL_ABS / U_EXP                                    # 6.78
BUDGET_RANKED = sorted(BUDGET, key=lambda b: -b[3])      # largest first

# halving the pressure-stability term (fix the leak, shorter hose, wait)
A_STAB_HALF = A_STAB / 2
U_C_HALF = math.sqrt(sum((b[3] if b[0] != "Pressure stability" else A_STAB_HALF / math.sqrt(3)) ** 2
                         for b in BUDGET))
U_EXP_HALF = K * U_C_HALF
U_EXP_HALF_PCT = U_EXP_HALF / SPAN * 100
TUR_HALF = TOL_ABS / U_EXP_HALF

# conservative decision rule on the 41.928 example
GUARD_SUM = abs(ERR_PCT_RIGHT) + U_EXP_PCT               # 0.4452 %
GUARD_MARGIN = TOL_PCT - GUARD_SUM                       # 0.0548 %
GUARD_MARGIN_OF_TOL = GUARD_MARGIN / TOL_PCT * 100       # ≈ 11 %
GUARD_PASS = GUARD_SUM <= TOL_PCT
GUARD_FAIL = abs(ERR_PCT_RIGHT) - U_EXP_PCT > TOL_PCT
ACCEPT_LIMIT_PCT = TOL_PCT - U_EXP_PCT                   # guard-banded acceptance limit

# why error ≠ uncertainty: E = 0.48 %, U = 0.10 %, tolerance 0.50 %
DEMO_E, DEMO_U = 0.48, 0.10
DEMO_LO, DEMO_HI = DEMO_E - DEMO_U, DEMO_E + DEMO_U       # 0.38 … 0.58 %

# % of reading vs % of span: 0.5 % of reading at 10 % of span
RDG_SPEC_PCT, RDG_AT_PCT_SPAN = 0.5, 10
RDG_AS_SPAN_PCT = RDG_SPEC_PCT * RDG_AT_PCT_SPAN / 100   # 0.05 % of span

# accuracy / uncertainty numbers quoted from specs (Ep 7 wording)
XMTR_ACCURACY_PCT = 0.075       # illustrative smart-transmitter spec, % of span
TUR_MIN = 4

# =====================================================================
# Ep 1 — choosing the module (MC6 brochure, 1-year uncertainty, k=2)  [new values, owner-approved 2026-09-28]
#   EXT60:  0 … 60 bar,  ±(0.01 % FS + 0.025 % RDG)
#   EXT600: 0 … 600 bar, ±(0.015 % FS + 0.025 % RDG)
# =====================================================================
URV_BAR = URV * KGF_CM2_TO_BAR                            # 41.19 bar
MOD_SMALL = ("EXT60", 60.0, 0.010, 0.025)
MOD_BIG = ("EXT600", 600.0, 0.015, 0.025)


def module_u_bar(mod, p_bar):
    _, fs, pfs, prdg = mod
    return pfs / 100 * fs + prdg / 100 * p_bar


U_SMALL_BAR = module_u_bar(MOD_SMALL, URV_BAR)            # 0.0163 bar
U_BIG_BAR = module_u_bar(MOD_BIG, URV_BAR)                # 0.1003 bar
U_SMALL_PCT = U_SMALL_BAR / URV_BAR * 100                 # % of transmitter span
U_BIG_PCT = U_BIG_BAR / URV_BAR * 100
MOD_RATIO = U_BIG_BAR / U_SMALL_BAR

# =====================================================================
# Ep 4 — pressure-decay curves (illustrative), 3 min, one reading per second, from 42 kg/cm²
# =====================================================================
DECAY_P0 = 42.0
DECAY_T_END = 180               # s
DECAY_DT = 1                    # s
THERM_A = 0.30                  # kg/cm², total thermal drop
THERM_TAU = 30.0                # s  (settles within about 2 min)
LEAK_RATE = 0.10                # kg/cm² per minute
MIX_A, MIX_TAU, MIX_RATE = 0.20, 25.0, 0.05


def p_thermal(t):
    return DECAY_P0 - THERM_A * (1 - math.exp(-t / THERM_TAU))


def p_leak(t):
    return DECAY_P0 - LEAK_RATE * t / 60


def p_mixed(t):
    return DECAY_P0 - MIX_A * (1 - math.exp(-t / MIX_TAU)) - MIX_RATE * t / 60


DECAY_T = list(range(0, DECAY_T_END + 1, DECAY_DT))
THERM_SETTLE_S = -THERM_TAU * math.log(0.02)             # 98 % of the drop reached (≈ 117 s)

# the five calibration points of the procedure
CAL_POINTS_PCT = [0, 25, 50, 75, 100]
EXERCISE_CYCLES = 3             # owner's procedure (Beamex blog: 2–3)
DECAY_TEST_MIN = 3              # min, one reading per second
ACCEPT_DEV_PCT = (2, 3)         # % of span, owner's recommendation
ACCEPT_DELAY_S = (30, 60)       # s, owner's recommendation
COLD_WAIT_MIN = (15, 30)        # min, cold transmitter
LINE_PRESSURE_BAR = 40          # bar, manifold example (owner's text)

# =====================================================================
# Published values quoted in the narration (Beamex manuals; source file and page in
# sources/pt_cal_ep0N_*.md). Typed once here so every spoken number has one home.
# =====================================================================
MC6_SCREEN_IN = 5.7                     # MC6-UM p24
MC5_DISCONTINUED = 2014                 # Beamex discontinued-products page
MC6_LOOP_V = 24                         # V, MC6-UM p47
MC6_HART_R_EXT = 250                    # Ω with an external supply, MC6-UM p60
MC6_MAX_VDC, MC6_MAX_VAC = 60, 30       # MC6-UM p11, MC6-BR p11
MC6_INT_MODULES, MC6_BARO_MODULES = 3, 1  # MC6-UM p21
EXT_MAX_BAR = 1000                      # MC6-BR p12
MC6_MODES = ["Meter", "Calibrator", "Documenting Calibrator", "Data Logger", "Communicator"]

PUMPS = [  # (model, medium, low, high, unit) — PG brochure 04/2025 and the manuals
    ("PGL", "air", -400, 400, "mbar"),
    ("PGV", "air", -0.95, 0, "bar"),
    ("PGM", "air", 0, 20, "bar"),
    ("PGC", "air", -0.95, 35, "bar"),
    ("PGPH", "air", -0.95, 140, "bar"),
    ("PGHH", "liquid", 0, 700, "bar"),
    ("PGXH", "liquid", 0, 700, "bar"),
    ("PGHS", "liquid", 0, 1000, "bar"),
]
EPG_RANGE = (-0.85, 20)                 # bar, ePG brochure
POC8_MAX_BAR = 210                      # POC8 brochure
PGHH_RESERVOIR_ML = 200                 # PGHH p7
PGHH_FILL = ("2/3", "3/4")              # PGHH p12
PGHH_HOSE_BAR = 630                     # PGHH p5, p8
HOSE_LOW_BAR = 40                       # 40 bar hoses, Bx G1/8 (MC6-BR p12, PGC p8)
HOSE_LOW_FITTING = "Bx G1/8"            # MC6-BR p12
HOSE_HIGH_FITTING = "Bx 1215"           # MC6-BR p12, PGHH p7
BAD_HOSE_BAR = 20                       # owner's example: 20 bar hose on a 40 bar system
PGHH_BLEED_BAR = 50                     # PGHH p13
PGHH_BLEED_REPEAT = (2, 3)              # PGHH p13
PGHH_WAIT_MIN = (2, 5)                  # PGHH p16
PGC_PUMP_MAX_BAR = (20, 25)             # PGC p12
AIR_WAIT_S = (30, 60)                   # PGC p12
BONDED_SEAL_MAX_BAR = 600               # PGHH p12


def self_test():
    assert TAG == "PT-101"
    assert abs(I_EXP_ACTUAL - 19.972571428571) < 1e-9
    assert f"{ERR_PCT_WRONG:.3f}" == "0.200"
    assert f"{ERR_PCT_RIGHT:.4f}" == "0.3714"
    assert f"{PUMP_EFFECT_PCT:.4f}" == "0.1714"
    assert f"{TOL_USED_WRONG:.0f}" == "40" and f"{TOL_USED_RIGHT:.1f}" == "74.3"
    assert PASS_41928
    expect = {10: "9.060", 20: "11.155", 25: "12.000", 30: "12.764", 40: "14.119",
              50: "15.314", 60: "16.394", 70: "17.387", 75: "17.856", 80: "18.311",
              90: "19.179", 0: "4.000", 100: "20.000"}
    for p, lin, sq in SQRT_TABLE:
        assert f"{sq:.3f}" == expect[p], (p, sq)
        assert abs(lin - (4 + 0.16 * p)) < 1e-9
    for p, v in SQRT_GUIDE_ERRORS.items():
        assert f"{i_sqrt(p / 100 * SPAN):.3f}" != f"{v:.3f}"
    for p, v in SQRT_GUIDE_TRUNCATED.items():       # truncation, not rounding
        assert math.floor(i_sqrt(p / 100 * SPAN) * 1000) / 1000 == v
    assert f"{DP_50_SQRT_MA:.3f}" == "15.314"
    assert f"{U_C:.5f}" == "0.01550" and f"{U_EXP:.5f}" == "0.03099"
    assert f"{U_EXP_PCT:.4f}" == "0.0738" and f"{TUR:.2f}" == "6.78"
    assert f"{GUARD_SUM:.4f}" == "0.4452" and f"{GUARD_MARGIN:.4f}" == "0.0548"
    assert round(GUARD_MARGIN_OF_TOL) == 11 and GUARD_PASS and not GUARD_FAIL
    assert f"{DEMO_LO:.2f}" == "0.38" and f"{DEMO_HI:.2f}" == "0.58"
    assert f"{RDG_AS_SPAN_PCT:.2f}" == "0.05"
    assert abs(PATTERN_SLOPE * 100 - (-0.68)) < 1e-9       # −0.68 % over the span
    assert PATTERN_MAX_RESID < 0.015 and PATTERN_PASS
    # the three largest contributions (the owner's text names stability as one of them)
    assert [b[0] for b in BUDGET_RANKED[:3]] == ["Reference module", "Repeatability",
                                                "Current measurement"]
    assert TUR_HALF > TUR
    assert U_BIG_BAR > 6 * U_SMALL_BAR
    assert 90 < THERM_SETTLE_S < 180
    assert abs(p_leak(DECAY_T_END) - (DECAY_P0 - 0.30)) < 1e-9


self_test()


def print_table():
    print(f"{TAG}  {LRV:g}–{URV:g} {UNIT}  →  4–20 mA, tolerance ±{TOL_PCT}% of span "
          f"(= ±{TOL_ABS:.3f} {UNIT})")
    print(f"41.928 example: I_exp nominal {I_EXP_NOMINAL:.4f}, actual {I_EXP_ACTUAL:.5f} mA; "
          f"error wrong {ERR_PCT_WRONG:.3f}% right {ERR_PCT_RIGHT:.4f}%; pump effect "
          f"{PUMP_EFFECT_PCT:.4f}%; tolerance used {TOL_USED_WRONG:.0f}% → {TOL_USED_RIGHT:.1f}%")
    print("Square-root table:  %   linear   sqrt")
    for p, lin, sq in SQRT_TABLE:
        print(f"   {p:>3}  {lin:7.3f}  {sq:7.3f}")
    print(f"DP 50 % with sqrt: {DP_50_SQRT_MA:.3f} mA; linear procedure would call it "
          f"{TRAP_50_ERR_PCT:.1f}% of span")
    print(f"Pattern: slope {PATTERN_SLOPE*100:.2f}% over the span, intercept "
          f"{PATTERN_INTERCEPT:.3f}%, residuals {[round(r, 3) for r in PATTERN_RESID]}")
    print("Budget (kg/cm²):")
    for n, a, how, u in BUDGET:
        print(f"   {n:<20} {a:.4f}  {how:<8} u = {u:.5f}")
    print(f"u_c = {U_C:.5f}, U = {U_EXP:.5f} ({U_EXP_PCT:.4f}% of span), TUR = {TUR:.2f}")
    print(f"stability halved: U = {U_EXP_HALF:.5f} ({U_EXP_HALF_PCT:.4f}%), TUR = {TUR_HALF:.2f}")
    print(f"Decision: {ERR_PCT_RIGHT:.4f} + {U_EXP_PCT:.4f} = {GUARD_SUM:.4f}% ≤ {TOL_PCT}% "
          f"→ PASS, margin {GUARD_MARGIN:.4f}% ({GUARD_MARGIN_OF_TOL:.0f}% of tolerance)")
    print(f"Module choice at {URV_BAR:.2f} bar: {MOD_SMALL[0]} ±{U_SMALL_BAR:.4f} bar "
          f"({U_SMALL_PCT:.3f}% of span), {MOD_BIG[0]} ±{U_BIG_BAR:.4f} bar "
          f"({U_BIG_PCT:.3f}%), ×{MOD_RATIO:.1f}")
    print(f"Decay: thermal settles ≈{THERM_SETTLE_S:.0f} s; at 180 s thermal "
          f"{p_thermal(180):.3f}, leak {p_leak(180):.3f}, mixed {p_mixed(180):.3f} {UNIT}")


if __name__ == "__main__":
    print_table()


# =====================================================================
# Ep 2 — illustrative on-screen values of the animations (not measurements)
# =====================================================================
SETUP_DEMO_PV = URV / 2                         # kg/cm², setup demo (50 % of span)
SETUP_DEMO_MA = i_linear(SETUP_DEMO_PV)         # 12.00 mA
STROKE_DEMO_BAR = [6.0, 12.0, 18.0]             # bar after each squeeze (illustrative)
FINE_STEP_BAR = 0.4                             # bar moved by one fine-adjust turn (illustrative)
BUBBLE_SHRINK = 0.4                             # a gas bubble at 50 bar drawn at 40 % size


def _self_test_ep2():
    assert f"{SETUP_DEMO_MA:.2f}" == "12.00"
    assert STROKE_DEMO_BAR == sorted(STROKE_DEMO_BAR) and STROKE_DEMO_BAR[-1] < PGHH_BLEED_BAR
    assert PUMPS[5][0] == "PGHH" and PUMPS[5][3] == 700 and PUMPS[7][3] == 1000


_self_test_ep2()
