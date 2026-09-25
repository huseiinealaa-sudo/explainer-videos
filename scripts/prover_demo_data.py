"""Illustrative data for the Daniel Compact Prover series (single source of truth).

The repository is PUBLIC: every value here is a demo input or is derived from
demo inputs with public equations (API MPMS / Table 54B 1980). No site data.
Episode scripts import from this module; never type derived values by hand:

    from prover_demo_data import DATA, RUNS, SUMMARY

Run directly to print every value as a table:

    python scripts/prover_demo_data.py
"""
import math

# ---------------- Base data (inputs only) ----------------
PROVER_SERIAL = "PRV-DEMO-001"
METER_TAG = "FT-DEMO-01"
METER_SERIAL = "MM-DEMO-0001"
METER_TYPE = "Coriolis (Micro Motion, generic)"
CONFIG_NAME = "DEMO_PRV_CFG"
CONFIG_CSUM = "a1b2"
PROVING_DATE = "15/03/2026"

BPV = 0.2463                # m3, nominal base prover volume (24-inch model)
K_NOMINAL = 60000.0         # pls/m3, nominal meter K-factor
FLOW_RATE = 250.0           # m3/h
RHO_15 = 840.0              # kg/m3, standard density at 15 degC
T_PROVER = 30.0             # degC
T_METER = 29.9              # degC
CPSP = 1.000000
CPLP = 1.000150
CPLM = 1.000160
PASSES_PER_RUN = 3
RUN_COUNT = 5

GC_STEEL = 0.0000216        # 1/degC, area thermal expansion of the flow tube
T_BASE = 15.0               # degC
REPEATABILITY_LIMIT = 0.05  # %

# Average interpolated pulses per pass for each run (double chronometry gives
# fractional pulses). Chosen so average MF ~ 0.9990 and repeatability ~ 0.03 %.
RUN_PULSES = [14796.164, 14798.386, 14795.423, 14793.943, 14796.905]

# Plenum example
PLENUM_LINE_PRESSURE = 40.0  # psig
PLENUM_RATIO = 5.0           # R
PLENUM_OFFSET = 60.0         # psig, fixed term in (line / R) + 60

# ---------------- API Table 54B (1980, SI) ----------------
# rho = standard density at 15 degC in kg/m3, dT = T - 15 in degC.
# alpha15 = K0 / rho^2 + K1 / rho          (regular groups)
# alpha15 = A + B / rho^2                  (transition zone)
# CTL = exp(-alpha15 * dT * (1 + 0.8 * alpha15 * dT))
# These are the per-degC constants of the metric table. Do NOT use the
# per-degF constants of Tables 6B / 2004 (e.g. fuel oils 103.8720 / 0.2701).
TABLE_54B_GROUPS = [
    # (name, rho_min, rho_max, kind, c1, c2)
    ("Gasolines", 653.0, 770.5, "K", 346.4228, 0.4388),
    ("Transition zone", 770.5, 787.5, "AB", -0.00336312, 2680.3206),
    ("Jet fuels", 787.5, 838.5, "K", 594.5418, 0.0),
    ("Fuel oils", 838.5, 1075.0, "K", 186.9696, 0.4862),
]

def table_54b_group(rho):
    for group in TABLE_54B_GROUPS:
        if group[1] <= rho < group[2]:
            return group
    raise ValueError(f"density {rho} kg/m3 is outside Table 54B")


def alpha_54b(rho):
    _, _, _, kind, c1, c2 = table_54b_group(rho)
    if kind == "AB":
        return c1 + c2 / rho**2
    return c1 / rho**2 + c2 / rho


def ctl_54b(rho, temp):
    alpha = alpha_54b(rho)
    dt = temp - T_BASE
    return math.exp(-alpha * dt * (1 + 0.8 * alpha * dt))


def ctsp(temp):
    return 1 + GC_STEEL * (temp - T_BASE)


# ---------------- Derived values ----------------
GROUP = table_54b_group(RHO_15)
ALPHA = alpha_54b(RHO_15)
CTSP = ctsp(T_PROVER)
CTLP = ctl_54b(RHO_15, T_PROVER)
CTLM = ctl_54b(RHO_15, T_METER)

PRV_VOL = BPV * CTSP * CPSP * CTLP * CPLP   # same for every run (steady conditions)

RUNS = []
for i, pulses in enumerate(RUN_PULSES, start=1):
    mtr_vol = pulses / K_NOMINAL * CTLM * CPLM
    mf = PRV_VOL / mtr_vol
    RUNS.append({
        "run": i,
        "pulses": pulses,
        "prv_vol": PRV_VOL,
        "mtr_vol": mtr_vol,
        "mf": mf,
        "k": K_NOMINAL / mf,
    })

MF_AVG = sum(r["mf"] for r in RUNS) / len(RUNS)
K_FINAL = K_NOMINAL / MF_AVG
K_MAX = max(r["k"] for r in RUNS)
K_MIN = min(r["k"] for r in RUNS)
REPEATABILITY = (K_MAX - K_MIN) / K_MIN * 100

PASS_TIME = BPV / FLOW_RATE * 3600          # s
FREQUENCY = FLOW_RATE * K_NOMINAL / 3600    # Hz

PLENUM_PRESSURE = PLENUM_LINE_PRESSURE / PLENUM_RATIO + PLENUM_OFFSET  # psig

SUMMARY = {
    "mf_avg": MF_AVG,
    "k_final": K_FINAL,
    "k_max": K_MAX,
    "k_min": K_MIN,
    "repeatability": REPEATABILITY,
    "repeatability_ok": REPEATABILITY <= REPEATABILITY_LIMIT,
}

DATA = {
    "prover_serial": PROVER_SERIAL, "meter_tag": METER_TAG,
    "meter_serial": METER_SERIAL, "meter_type": METER_TYPE,
    "config_name": CONFIG_NAME, "config_csum": CONFIG_CSUM,
    "proving_date": PROVING_DATE,
    "bpv": BPV, "k_nominal": K_NOMINAL, "flow_rate": FLOW_RATE,
    "rho_15": RHO_15, "t_prover": T_PROVER, "t_meter": T_METER,
    "cpsp": CPSP, "cplp": CPLP, "cplm": CPLM,
    "passes_per_run": PASSES_PER_RUN, "run_count": RUN_COUNT,
    "table_54b_group": GROUP[0], "alpha": ALPHA,
    "ctsp": CTSP, "ctlp": CTLP, "ctlm": CTLM, "prv_vol": PRV_VOL,
    "pass_time": PASS_TIME, "frequency": FREQUENCY,
    "plenum_line_pressure": PLENUM_LINE_PRESSURE, "plenum_ratio": PLENUM_RATIO,
    "plenum_pressure": PLENUM_PRESSURE,
    **SUMMARY,
}



def self_test():
    """Stop the script if CTL drifts from the reference Table 54B values."""
    assert abs(CTLP - 0.987296) < 0.000001, f"CTLp = {CTLP:.7f}, expected 0.987296"
    assert abs(CTLM - 0.987381) < 0.000001, f"CTLm = {CTLM:.7f}, expected 0.987381"
    assert GROUP[0] == "Fuel oils", GROUP
    assert len(RUN_PULSES) == RUN_COUNT
    assert abs(MF_AVG - 0.9990) < 0.00005, MF_AVG
    assert abs(REPEATABILITY - 0.03) < 0.005, REPEATABILITY
    assert SUMMARY["repeatability_ok"], REPEATABILITY


self_test()


def print_table():
    def row(label, value):
        print(f"  {label:<34} {value}")

    print("BASE DATA (illustrative inputs)")
    row("Prover serial", PROVER_SERIAL)
    row("Meter tag / serial", f"{METER_TAG} / {METER_SERIAL}")
    row("Meter type", METER_TYPE)
    row("Configuration / CSUM", f"{CONFIG_NAME} / {CONFIG_CSUM}")
    row("Proving date", PROVING_DATE)
    row("BPV", f"{BPV:.4f} m3")
    row("Nominal K-factor", f"{K_NOMINAL:.0f} pls/m3")
    row("Flow rate Q", f"{FLOW_RATE:.1f} m3/h")
    row("Standard density (15 C)", f"{RHO_15:.1f} kg/m3")
    row("Prover / meter temperature", f"{T_PROVER:.1f} / {T_METER:.1f} C")
    row("CPSp / CPLp / CPLm", f"{CPSP:.6f} / {CPLP:.6f} / {CPLM:.6f}")
    row("Passes per run / runs", f"{PASSES_PER_RUN} / {RUN_COUNT}")

    lo, hi, kind, c1, c2 = GROUP[1:]
    consts = f"K0 = {c1}, K1 = {c2}" if kind == "K" else f"A = {c1}, B = {c2}"
    print("\nCORRECTION FACTORS")
    row("Table 54B group", f"{GROUP[0]} ({lo} <= rho < {hi})")
    row("Group constants", consts)
    row("alpha15 = K0/rho^2 + K1/rho", f"{ALPHA:.9f} 1/C")
    row("CTSp = 1 + 0.0000216 (Tp - 15)", f"{CTSP:.6f}")
    row("CTLp (Tp = 30.0 C)", f"{CTLP:.6f}")
    row("CTLm (Tm = 29.9 C)", f"{CTLM:.6f}")
    row("PRV VOL = BPV CTSp CPSp CTLp CPLp", f"{PRV_VOL:.6f} m3")

    print("\nPROVING RUNS  (pulses = average interpolated pulses per pass)")
    print(f"  {'Run':<4}{'Pulses':>12}{'PRV VOL m3':>13}{'MTR VOL m3':>13}"
          f"{'M-FACTOR':>11}{'K-FACTOR':>13}")
    for r in RUNS:
        print(f"  {r['run']:<4}{r['pulses']:>12.3f}{r['prv_vol']:>13.6f}"
              f"{r['mtr_vol']:>13.6f}{r['mf']:>11.5f}{r['k']:>13.3f}")

    print("\nRESULTS")
    row("Average MF", f"{MF_AVG:.5f}")
    row("Final K = K_nom / MF_avg", f"{K_FINAL:.3f} pls/m3")
    row("K max / K min", f"{K_MAX:.3f} / {K_MIN:.3f}")
    row("Repeatability (Kmax-Kmin)/Kmin",
        f"{REPEATABILITY:.4f} %  (limit {REPEATABILITY_LIMIT} %: "
        f"{'PASS' if SUMMARY['repeatability_ok'] else 'FAIL'})")

    print("\nTIMING & PLENUM")
    row("Pass time = BPV / Q x 3600", f"{PASS_TIME:.3f} s")
    row("Frequency = Q x K / 3600", f"{FREQUENCY:.1f} Hz")
    row("Plenum = line / R + 60",
        f"{PLENUM_LINE_PRESSURE:.0f} / {PLENUM_RATIO:.0f} + {PLENUM_OFFSET:.0f}"
        f" = {PLENUM_PRESSURE:.0f} psig")


if __name__ == "__main__":
    print_table()
