"""svp_winsfc: every number shown or spoken in the video (illustrative values only).

Inputs are typed once here (the owner's illustrative set); everything derived is
computed at full precision, never typed by hand. self_test() runs on import, so a
drift stops the video script. Units: m3, degC, kPa, mm, ms (and s, Hz, ohm).

    python projects/svp_winsfc/svp_winsfc_data.py      # print the table
"""
import math

# ---------------- Inputs (illustrative) ----------------
K_FACTOR = 60000                  # pulses/m3 (meter K-factor)
BPV = 0.25000                     # m3, base prover volume at T_BASE
T_BASE = 15.0                     # degC
FLOW_RATE = 200.0                 # m3/h

REPEATABILITY_LIMIT = 0.050       # %
RUNS_TO_AVERAGE = 5
TOTAL_RUNS = 5

# Double chronometry, scaled-down example
CHRONO_N = 18                     # whole meter pulses counted during t_P
CHRONO_TD = 5.490                 # ms, detector 1 -> detector 2
CHRONO_TP = 5.400                 # ms, first whole pulse after D1 -> first after D2

T_PROVER = 40.0                   # degC, prover (flow tube)
T_DETECTOR = 35.0                 # degC, detector (switch) bar
T_METER = 38.0                    # degC
GA = 0.0000318                    # /degC, area coefficient of the flow tube
GL = 0.0000173                    # /degC, linear coefficient of the detector bar

P_PROVER = 500.0                  # kPa gauge
D_PROVER = 600.0                  # mm, inside diameter
WALL = 7.0                        # mm, wall thickness
E_MODULUS = 193000000.0           # kPa, modulus of elasticity

CTPL_P = 0.97820                  # liquid correction at the prover
CTPL_M = 0.97990                  # liquid correction at the meter

RUN_PULSES = [14976.40, 14977.90, 14975.10, 14977.20, 14975.40]   # interpolated, per run

PT100_R = 115.54                  # ohm, Diagnostic example
PT100_R0 = 100.0                  # ohm at 0 degC
CVD_A = 3.9083e-3                 # IEC 60751 (t >= 0 degC): R = R0 (1 + A t + B t^2)
CVD_B = -5.775e-7
PT100_ALPHA = 0.00385             # mean slope 0-100 degC -> linear check (R - 100) / 0.385

DENSITY_SUSPECT = 700.0           # kg/m3, the round value that should be questioned
VOLUME_PULSE_MS = 25              # ms, volume pulse from the SVP controller
MOTOR_SWITCH_TIMEOUT_EXAMPLE = 58 # s, factory setting of one model (S85)
SERVICE_DUE_CYCLES = 1000         # default cycle count threshold
BAUD_EXAMPLE = 9600               # bit/s, Modbus RTU example on RS-485

# ---------------- Published values (manuals; see sources/svp_winsfc_full.md) ----------------
LARGE_PROVER_PULSES = 10000       # a large (pipe) prover needs more than this per meter factor
DETECTOR_RESPONSE_US = 5          # microseconds, optical switch response
DETECTOR_REPEAT_PCT = 0.0005      # %, switch repeatability of linear measurement
CCB_TERMINALS = [(12, "Feed+ (flow computer)"), (13, "Run permissive +"),
                 (14, "Run permissive -"), (15, "Common (flow computer)"),
                 (16, "Volume pulse +"), (17, "Volume pulse -")]
LIMIT_RESISTOR_OHM = 1500         # with 12-24 VDC; a jumper from 6 to 12 VDC
LEAK_DP_PSID = 6                  # static leak test differential
LEAK_SETTLE_MIN = 5               # minutes before recording
LEAK_WATCH_MIN = 20               # minutes of observation
LEAK_MAX_DROP_PCT = 25            # % of the starting differential
WD_MIN_DRAWS = 3                  # consecutive water draws
WD_REPEAT_PCT = 0.02              # % between them
WD_FLOW_CHANGE_PCT = 25           # % flow change on at least one draw
WD_INTERVAL_YEARS = 1             # recommended recalibration interval (or per the authority)
MAINT_BASIS_PASSES_PER_DAY = 100  # basis of the maintenance intervals
FAIL_CODES = [(0, "live value always"), (1, "maintenance value always"),
              (2, "maintenance value if the signal fails")]

# Stroke profile for the cycle chart (segment 3): piston position in % of stroke
# (0 = parked downstream, 100 = motor stop switch upstream) against time in s.
DET_UP_POS = 85.0                 # % of stroke, upstream detector
DET_DN_POS = 15.0                 # % of stroke, downstream detector
T_STANDBY = 2.0                   # s parked
T_RETRACT = 10.0                  # s pulled upstream by the chain
T_RUNUP = 2.0                     # s from release to the upstream detector
T_STOP = 1.0                      # s from the downstream detector to the stop

# ---------------- Derived ----------------
NOMINAL_PULSES = BPV * K_FACTOR                          # pulses per pass
SWEEP_TIME = BPV / FLOW_RATE * 3600                      # s between the detectors
FREQ = FLOW_RATE * K_FACTOR / 3600                       # Hz
PULSE_FRACTION_PCT = 100 / NOMINAL_PULSES                # one pulse, % of a pass
FRACTION_OF_LIMIT = PULSE_FRACTION_PCT / REPEATABILITY_LIMIT

CHRONO_INTERP = CHRONO_N * CHRONO_TD / CHRONO_TP         # interpolated pulses
CHRONO_FREQ = CHRONO_N / (CHRONO_TP / 1000)              # Hz implied by the example

CTS_TUBE = 1 + (T_PROVER - T_BASE) * GA
CTS_DET = 1 + (T_DETECTOR - T_BASE) * GL
CTSP = CTS_TUBE * CTS_DET
CPSP = 1 + P_PROVER * D_PROVER / (E_MODULUS * WALL)

F_VOL = BPV * CTSP * CPSP * CTPL_P                       # m3, corrected prover volume
AVG_PULSES = sum(RUN_PULSES) / len(RUN_PULSES)
L_VOL = AVG_PULSES / K_FACTOR * CTPL_M                   # m3, corrected meter volume
MF = F_VOL / L_VOL
ACTUAL_K = K_FACTOR / MF
REPEATABILITY = (max(RUN_PULSES) - min(RUN_PULSES)) / min(RUN_PULSES) * 100

FREQ_SHOWN = round(FREQ, 1)                              # the value read on the screen
Q_FROM_FREQ = FREQ_SHOWN * 3600 / K_FACTOR               # m3/h

PT100_T_CVD = (-CVD_A + math.sqrt(CVD_A ** 2 - 4 * CVD_B * (1 - PT100_R / PT100_R0))) \
    / (2 * CVD_B)                                        # degC, IEC 60751 inverse
PT100_T_LINEAR = (PT100_R - PT100_R0) / (PT100_R0 * PT100_ALPHA)

# Cycle chart points (time s, position %)
_t1 = T_STANDBY
_t2 = _t1 + T_RETRACT
_t3 = _t2 + T_RUNUP
_t4 = _t3 + SWEEP_TIME
_t5 = _t4 + T_STOP
CYCLE_T = [0.0, _t1, _t2, _t3, _t4, _t5, _t5 + T_STANDBY]
CYCLE_POS = [0.0, 0.0, 100.0, DET_UP_POS, DET_DN_POS, 0.0, 0.0]
T_MEASURE_START, T_MEASURE_END = _t3, _t4


def self_test():
    assert NOMINAL_PULSES == 15000
    assert abs(SWEEP_TIME - 4.5) < 1e-12
    assert f"{FREQ:.2f}" == "3333.33"
    assert f"{PULSE_FRACTION_PCT:.5f}" == "0.00667"
    assert abs(CHRONO_INTERP - 18.3) < 1e-12
    assert abs(CHRONO_FREQ - FREQ) < 1e-6                # the mini example runs at FREQ
    assert f"{CTS_TUBE:.6f}" == "1.000795" and f"{CTS_DET:.6f}" == "1.000346"
    assert f"{CTSP:.7f}" == "1.0011413"
    assert f"{CPSP:.7f}" == "1.0002221"
    assert f"{AVG_PULSES:.2f}" == "14976.40"
    assert f"{REPEATABILITY:.4f}" == "0.0187" and REPEATABILITY < REPEATABILITY_LIMIT
    assert f"{F_VOL:.6f}" == "0.244883"
    assert f"{L_VOL:.6f}" == "0.244590"
    assert f"{MF:.5f}" == "1.00120"
    assert f"{ACTUAL_K:.0f}" == "59928"
    assert f"{FREQ_SHOWN:.1f}" == "3333.3" and f"{Q_FROM_FREQ:.1f}" == "200.0"
    assert f"{PT100_T_CVD:.1f}" == "40.0"
    assert f"{PT100_T_LINEAR:.2f}" == "40.36"          # shown as 40.36 (owner, 2026-09-26)
    assert RUNS_TO_AVERAGE <= TOTAL_RUNS == len(RUN_PULSES)
    assert DET_DN_POS < DET_UP_POS < 100
    assert NOMINAL_PULSES > LARGE_PROVER_PULSES           # our example is not "small" in pulses
    assert [t for t, _ in CCB_TERMINALS] == list(range(12, 18))


self_test()


def print_table():
    rows = [
        ("K-factor", f"{K_FACTOR}", "pulses/m3"),
        ("BPV", f"{BPV:.5f}", "m3"),
        ("Flow rate", f"{FLOW_RATE:.1f}", "m3/h"),
        ("Nominal pulses per pass", f"{NOMINAL_PULSES:.0f}", ""),
        ("Sweep time", f"{SWEEP_TIME:.1f}", "s"),
        ("Frequency", f"{FREQ:.2f}", "Hz"),
        ("One pulse of a pass", f"{PULSE_FRACTION_PCT:.5f}", "%"),
        ("  ... of the repeatability limit", f"{FRACTION_OF_LIMIT:.3f}", ""),
        ("Chronometry N x tD / tP", f"{CHRONO_INTERP:.1f}", "pulses"),
        ("CTSp tube term", f"{CTS_TUBE:.6f}", ""),
        ("CTSp detector term", f"{CTS_DET:.6f}", ""),
        ("CTSp", f"{CTSP:.7f}", ""),
        ("CPSp", f"{CPSP:.7f}", ""),
        ("F (corrected prover volume)", f"{F_VOL:.6f}", "m3"),
        ("Average pulses", f"{AVG_PULSES:.2f}", ""),
        ("L (corrected meter volume)", f"{L_VOL:.6f}", "m3"),
        ("MF", f"{MF:.5f}", ""),
        ("Actual K", f"{ACTUAL_K:.0f}", "pulses/m3"),
        ("Repeatability", f"{REPEATABILITY:.4f}", "%"),
        ("Q from Freq#1", f"{Q_FROM_FREQ:.1f}", "m3/h"),
        ("Pt100 115.54 ohm, CVD", f"{PT100_T_CVD:.3f}", "degC"),
        ("Pt100 115.54 ohm, linear", f"{PT100_T_LINEAR:.4f}", "degC"),
    ]
    for name, value, unit in rows:
        print(f"  {name:<34} {value:>14} {unit}")


if __name__ == "__main__":
    print_table()
