"""Illustrative data for the Daniel Compact Prover series (single source of truth).

The repository is PUBLIC: every value here is a demo input or is derived from
demo inputs with public equations (API MPMS / Table 54B 1980). No site data.
Episode scripts import from this module; never type derived values by hand:

    from prover_demo_data import DATA, RUNS, SUMMARY

Run directly to print every value as a table:

    python projects/prover/prover_demo_data.py
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

# CTSp for a small volume prover with external detector switches (API MPMS 12.2;
# Emerson ROC800L Flow Calculations manual §6.1.1; Daniel manual 3-9008-701 Rev J
# §4.3.2 pp.50-51, where the same two terms appear in the water-draw factor Css):
#
#     CTSp = [1 + (Tp - Tb) x Gc] x [1 + (Td - Tb) x Gl]
#             flow-tube term          Invar-rod term
#
# Gc = 0.0000216 /degC is the AREA (squared) coefficient of the flow tube, i.e.
#      twice the linear coefficient 0.0000108 /degC (manual table p.51).
# Gl = 0.00000144 /degC is the linear coefficient of the Invar rods that space the
#      optical switches (manual p.51).
# Td is the temperature of the Invar rods; the manual allows the ambient
#      temperature to be used instead (§4.3.1 item 5, p.49).
# In our example the rods are at 15 degC, so the Invar term equals exactly 1 and
# CTSp equals the flow-tube term alone. This is a choice for the example: in the
# field the rods are rarely at the reference temperature, and the term is not 1.
GC_STEEL = 0.0000216        # 1/degC, area thermal expansion of the flow tube (2 x 0.0000108)
GL_INVAR = 0.00000144       # 1/degC, linear thermal expansion of the Invar rods
T_BASE = 15.0               # degC
T_DETECTOR = 15.0           # degC, Invar rod (detector) temperature Td in our example
REPEATABILITY_LIMIT = 0.05  # %

# Public reference values (not site data), used by episode 2.
# API MPMS Ch. 4.8 Annex A: largest allowed repeatability range (%) for a given
# number of consecutive runs, so that the MF uncertainty stays within +/-0.027 %.
# Sources: Flow Management Devices (Lantzy 2025) Table 1, Coastal Flow Figure A,
# Buttler (Emerson, FLOMEKO 2019) for 5, 6 and 10 runs. See projects/prover/sources/prover_ep02.md.
MF_UNCERTAINTY_TARGET = 0.027   # %
API_48_REPEATABILITY = {
    3: 0.02, 4: 0.03, 5: 0.05, 6: 0.06, 7: 0.08, 8: 0.09, 9: 0.10, 10: 0.12,
    11: 0.13, 12: 0.14, 13: 0.15, 14: 0.16, 15: 0.17, 16: 0.18, 17: 0.19,
    18: 0.20, 19: 0.21, 20: 0.22,
}
# Typical minimum pass (flight) time for Coriolis meters on a small volume
# prover (Flow Management Devices, Lantzy 2025, p.13).
CORIOLIS_MIN_PASS_TIME = 0.8    # s

# Public manufacturer facts used by episodes 3 and 4 (Daniel O&M manual
# 3-9008-701 Rev J; see projects/prover/sources/prover_ep03.md and prover_ep04.md).
PROVER_COMPONENTS = [           # owner-approved grouping, front -> back
    "End connections", "Flow tube", "Measurement piston", "Poppet valve",
    "Pneumatic spring plenum", "Hydraulic cylinder", "Hydraulic control valve",
    "Hydraulic pump", "Optical assembly", "Interface enclosure",
]
OPTICAL_SWITCH_COUNT = 3        # 1 standby + 2 volume switches (manual §1.3)
VOLUME_SWITCH_COUNT = 2
CYCLE_STAGES = [                # manual §3.1, figure titles 3-1 ... 3-5
    "Standby position", "Initial motion", "Proving", "End of proving run",
    "Piston returning to upstream position",
]

# Average interpolated pulses per pass for each run (double chronometry gives
# fractional pulses). Chosen so average MF ~ 0.9990 and repeatability ~ 0.03 %.
RUN_PULSES = [14796.164, 14798.386, 14795.423, 14793.943, 14796.905]

# Common practice for the change in MF between two successive provings (episode 7).
# Not an API requirement we could read: Coastal Flow p.3 ("typical meter or contract
# allowance ... +/- 0.0025 shift for volume"), NFOGM (H. James) p.3, 43 CFR 3174.11(e)(1).
# Each operator or contract sets its own limit. See projects/prover/sources/prover_ep07.md.
MF_SHIFT_COMMON = 0.25       # %

# Plenum example
PLENUM_LINE_PRESSURE = 40.0  # psig
PLENUM_RATIO = 5.0           # R
PLENUM_OFFSET = 60.0         # psig, fixed term in (line / R) + 60 (horizontal prover)
# Manual §3.2 step 3 and Table 3-1 (pp.30-32): Plenum = line gauge (psig) / R + 60;
# R = 5 for the 24-inch prover (5.88 if shipped before 1 Jan 2006); 40 psig replaces
# 60 for a vertical installation; charge within 0 to +5 % of the calculated value.
PLENUM_TOLERANCE = 5.0       # %, upper guideline above the calculated pressure

# Upstream / downstream base volumes. A prover with a shaft on one side of the
# piston has two different volumes (NIST HB 105-7 §7.3.1). The manual gives the
# ratio upstream / downstream for the 24-inch prover (Table 1-2 p.8, post-2006,
# the same era as R = 5). Our meter is downstream of the prover, so BPV is the
# downstream volume; the upstream volume is derived from the ratio.
VOLUME_RATIO = 0.992369      # upstream / downstream, 24-inch (0.993464 before 2006)

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


def ctsp(temp, temp_detector=T_DETECTOR):
    """CTSp = [1 + (Tp - Tb) Gc] x [1 + (Td - Tb) Gl] (see the note above GC_STEEL)."""
    return (1 + GC_STEEL * (temp - T_BASE)) * (1 + GL_INVAR * (temp_detector - T_BASE))


# ---------------- Derived values ----------------
GROUP = table_54b_group(RHO_15)
ALPHA = alpha_54b(RHO_15)
CTSP_TUBE = 1 + GC_STEEL * (T_PROVER - T_BASE)
CTSP_INVAR = 1 + GL_INVAR * (T_DETECTOR - T_BASE)
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

TOTAL_PASSES = PASSES_PER_RUN * RUN_COUNT
PASS_TIME = BPV / FLOW_RATE * 3600          # s
FREQUENCY = FLOW_RATE * K_NOMINAL / 3600    # Hz

PLENUM_PRESSURE = PLENUM_LINE_PRESSURE / PLENUM_RATIO + PLENUM_OFFSET  # psig
PLENUM_MAX = PLENUM_PRESSURE * (1 + PLENUM_TOLERANCE / 100)            # psig

BPV_DOWNSTREAM = BPV                        # m3, meter downstream of the prover
BPV_UPSTREAM = BPV * VOLUME_RATIO           # m3

# Double chronometry (manual §2.2.2 pp.16-17, Fig. 2-2), one illustrative pass of
# run 1: Time A = flag D1 -> D2; Time B = first meter pulse edge after A starts ->
# first pulse edge after A stops; C = whole pulses counted in B.
# Interpolated pulses = C x A / B.
CHRONO_TIME_A = PASS_TIME                   # s
CHRONO_PULSES = RUN_PULSES[0]               # interpolated pulses
CHRONO_WHOLE = math.floor(CHRONO_PULSES)    # C
CHRONO_TIME_B = CHRONO_TIME_A * CHRONO_WHOLE / CHRONO_PULSES   # s

# Run 1 recalculated step by step (episode 7), full precision as in the report.
RUN1 = RUNS[0]
RUN1_IV = RUN1["pulses"] / K_NOMINAL        # m3, indicated volume

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
    "total_passes": TOTAL_PASSES, "pass_time": PASS_TIME, "frequency": FREQUENCY,
    "plenum_line_pressure": PLENUM_LINE_PRESSURE, "plenum_ratio": PLENUM_RATIO,
    "plenum_pressure": PLENUM_PRESSURE, "plenum_max": PLENUM_MAX,
    "t_detector": T_DETECTOR, "ctsp_tube": CTSP_TUBE, "ctsp_invar": CTSP_INVAR,
    "volume_ratio": VOLUME_RATIO, "bpv_downstream": BPV_DOWNSTREAM,
    "bpv_upstream": BPV_UPSTREAM,
    "chrono_time_a": CHRONO_TIME_A, "chrono_time_b": CHRONO_TIME_B,
    "chrono_whole": CHRONO_WHOLE, "chrono_pulses": CHRONO_PULSES,
    **SUMMARY,
}



def self_test():
    """Stop the script if CTL drifts from the reference Table 54B values."""
    assert TABLE_54B_GROUPS == [
        ("Gasolines", 653.0, 770.5, "K", 346.4228, 0.4388),
        ("Transition zone", 770.5, 787.5, "AB", -0.00336312, 2680.3206),
        ("Jet fuels", 787.5, 838.5, "K", 594.5418, 0.0),
        ("Fuel oils", 838.5, 1075.0, "K", 186.9696, 0.4862),
    ], "Table 54B (1980, SI) constants changed"
    assert abs(CTLP - 0.987296) < 0.000001, f"CTLp = {CTLP:.7f}, expected 0.987296"
    assert abs(CTLM - 0.987381) < 0.000001, f"CTLm = {CTLM:.7f}, expected 0.987381"
    assert GROUP[0] == "Fuel oils", GROUP
    assert len(RUN_PULSES) == RUN_COUNT
    assert abs(MF_AVG - 0.9990) < 0.00005, MF_AVG
    assert abs(REPEATABILITY - 0.03) < 0.005, REPEATABILITY
    assert SUMMARY["repeatability_ok"], REPEATABILITY
    assert API_48_REPEATABILITY[RUN_COUNT] == REPEATABILITY_LIMIT, "limit must match API 4.8"
    assert PASS_TIME > CORIOLIS_MIN_PASS_TIME, PASS_TIME
    assert len(PROVER_COMPONENTS) == 10, PROVER_COMPONENTS
    assert len(CYCLE_STAGES) == 5, CYCLE_STAGES
    assert OPTICAL_SWITCH_COUNT == 1 + VOLUME_SWITCH_COUNT
    # CTSp: full small-volume-prover form; Invar term is exactly 1 at Td = 15 C
    assert GC_STEEL == 2 * 0.0000108 and GL_INVAR == 0.00000144
    assert T_DETECTOR == 15.0 and CTSP_INVAR == 1.0, CTSP_INVAR
    assert abs(CTSP - 1.000324) < 1e-9 and CTSP == CTSP_TUBE * CTSP_INVAR, CTSP
    # Plenum: 40 / 5 + 60 = 68 psig (manual §3.2), guideline up to +5 %
    assert PLENUM_PRESSURE == 68.0 and abs(PLENUM_MAX - 71.4) < 1e-9, PLENUM_PRESSURE
    # Upstream / downstream base volumes (manual Table 1-2, 24-inch)
    assert BPV_DOWNSTREAM == 0.2463
    assert abs(BPV_UPSTREAM / BPV_DOWNSTREAM - 0.992369) < 1e-9
    assert abs(BPV_UPSTREAM - 0.244420) < 0.0000005 and BPV_UPSTREAM < BPV_DOWNSTREAM
    # Double chronometry example
    assert f"{CHRONO_TIME_A:.6f}" == "3.546720", CHRONO_TIME_A
    assert CHRONO_WHOLE == 14796
    assert f"{CHRONO_TIME_B:.6f}" == "3.546681", CHRONO_TIME_B
    assert abs(CHRONO_WHOLE * CHRONO_TIME_A / CHRONO_TIME_B - CHRONO_PULSES) < 1e-6
    # Episode 7: run 1 recalculation (corrected prover / meter volumes and MF)
    assert RUN1["pulses"] == CHRONO_PULSES == 14796.164
    assert f"{PRV_VOL:.6f}" == "0.243286", PRV_VOL
    assert f"{RUN1_IV:.6f}" == "0.246603", RUN1_IV
    assert f"{RUN1['mtr_vol']:.6f}" == "0.243530", RUN1["mtr_vol"]
    assert f"{RUN1['mf']:.5f}" == "0.99900", RUN1["mf"]
    assert MF_SHIFT_COMMON == 0.25


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
    row("Tube term 1 + 0.0000216 (Tp - 15)", f"{CTSP_TUBE:.6f}")
    row("Invar term 1 + 0.00000144 (Td - 15)", f"{CTSP_INVAR:.6f}  (Td = {T_DETECTOR:.1f} C)")
    row("CTSp = tube term x Invar term", f"{CTSP:.6f}")
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
    row("Frequency = Q x K / 3600", f"{FREQUENCY:.1f} Hz (nominal K)")
    row("Total passes = passes x runs", f"{PASSES_PER_RUN} x {RUN_COUNT} = {TOTAL_PASSES}")
    row("Coriolis typical min pass time", f"{CORIOLIS_MIN_PASS_TIME} s")
    row("Plenum = line / R + 60",
        f"{PLENUM_LINE_PRESSURE:.0f} / {PLENUM_RATIO:.0f} + {PLENUM_OFFSET:.0f}"
        f" = {PLENUM_PRESSURE:.0f} psig")
    row("Plenum guideline (0 to +5 %)", f"{PLENUM_PRESSURE:.1f} to {PLENUM_MAX:.1f} psig")

    print("\nBASE VOLUMES (meter downstream of the prover)")
    row("Downstream volume = BPV", f"{BPV_DOWNSTREAM:.6f} m3")
    row("Volume ratio up / down (24-inch)", f"{VOLUME_RATIO}")
    row("Upstream volume = BPV x ratio", f"{BPV_UPSTREAM:.6f} m3")

    print("\nDOUBLE CHRONOMETRY (run 1, one illustrative pass)")
    row("Time A (D1 -> D2)", f"{CHRONO_TIME_A:.6f} s")
    row("Time B (whole pulses)", f"{CHRONO_TIME_B:.6f} s")
    row("C = whole pulses", f"{CHRONO_WHOLE}")
    row("Interpolated = C x A / B", f"{CHRONO_WHOLE * CHRONO_TIME_A / CHRONO_TIME_B:.3f}")

    print("\nRUN 1 RECALCULATED (episode 7)")
    row("PRV VOL = BPV CTSp CPSp CTLp CPLp", f"{PRV_VOL:.6f} m3")
    row("IV = pulses / K_nom", f"{RUN1['pulses']:.3f} / {K_NOMINAL:.0f} = {RUN1_IV:.6f} m3")
    row("MTR VOL = IV CTLm CPLm", f"{RUN1['mtr_vol']:.6f} m3")
    row("MF = PRV VOL / MTR VOL", f"{RUN1['mf']:.5f}")
    row("Common MF shift allowance", f"{MF_SHIFT_COMMON} % (operator / contract)")

    print("\nAPI MPMS 4.8 REPEATABILITY LIMITS (MF uncertainty "
          f"+/-{MF_UNCERTAINTY_TARGET} %)")
    for n, lim in API_48_REPEATABILITY.items():
        row(f"{n} runs", f"{lim:.2f} %" + ("   <- this series" if n == RUN_COUNT else ""))


if __name__ == "__main__":
    print_table()
