"""mc5_hart: every number shown or spoken in the videos (ALL values are illustrative).

Inputs are typed once here; everything derived is computed, never typed by hand. self_test()
runs on import, so a drift stops every script that uses the data.

    python projects/mc5_hart/mc5_hart_data.py      # print the tables
"""

# ---------------- Inputs (illustrative) ----------------
UNIT = "kgf/cm²"
LRV, URV = 0.0, 40.0                  # lower / upper range value
URL, LRL, MIN_SPAN = 50.00, 0.00, 0.50    # sensor limits and minimum span
TAG, DEVICE_ID, SERIAL = "PT-101", "12345678", "1234567"
DAMPING = 0.40                        # s
TRANSFER_FUNCTION, BURST_MODE, POLLING_ADDRESS = "Linear", "Off", 0
# Device Information fields that are not numbers (placeholders, no real maker or date)
MANUFACTURER, DEVICE_TYPE, SW_REV, HW_REV = "Maker X", "Pressure TX", "1.0", "1.0"
DATE, DESCRIPTOR, MESSAGE = "15.03.2026", "DEMO", "ILLUSTRATIVE"
REF_MODULE_MAX = 60.0                 # the reference pressure module covers 0…60 (not exceeded)

HART_MAX_DEVICES, POLL_MAX = 16, 15      # devices on one loop [1 p. 141]; polling addresses 0…15 (HART revision 5, [1 p. 137])
I_LOW, I_HIGH = 4.0, 20.0              # the loop current range, mA
REF_ZERO_DRIFT = 0.012                # kgf/cm², the reference reading before the zeroing (episode 1)

# Rerange example (episode 1, the only worked example there)
URV_NEW, P_EX = 30.0, 15.0

# AO check, commanded -> measured (mA)
AO_CHECK = [(3.8, 3.8002), (4.0, 4.0003), (12.0, 12.0010), (20.0, 20.0016), (20.5, 20.5017)]

# Sensor zero offset before the PV trim (episode 2 story)
PV_OFFSET = -0.160                    # kgf/cm²

# Calibration (episode 3)
REJECT_IF = 0.25                      # % of span
ADJUST_IF, DO_NOT_ADJUST_IF, ADJUST_TO = 0.15, 0.05, 0.05     # % of span (illustrative)
MAX_POINT_DEVIATION, CAL_PERIOD_DAYS = 0.10, 365              # %, days (illustrative)
SETPOINT_DELAY = 5.0                  # s
POINTS = [0.0, 10.0, 20.0, 30.0, 40.0]            # 5 points up, then down
HYSTERESIS = 0.004                    # kgf/cm², descending points only
NAMUR = {"low_fault": 3.6, "low_meas": 3.8, "high_meas": 20.5, "high_fault": 21.0}  # NE 43


# ---------------- Derived ----------------
SPAN = URV - LRV


def I_of(p, lrv=LRV, urv=URV):
    """Ideal loop current (mA) for pressure p."""
    return 4.0 + 16.0 * (p - lrv) / (urv - lrv)


def err_pct(i_meas, i_ideal):
    """Error in % of span (16 mA)."""
    return (i_meas - i_ideal) / 16.0 * 100.0


I_BEFORE = I_of(P_EX)                                   # 10.000 mA
I_AFTER = I_of(P_EX, urv=URV_NEW)                       # 12.000 mA
# a control system still scaled 0…URV reads this pressure for the new current (episode 1, segment 15)
P_MISREAD = LRV + (I_AFTER - 4.0) / 16.0 * (URV - LRV)  # 20.0

AO_ERR = [(cmd, meas, meas - cmd, err_pct(meas, cmd)) for cmd, meas in AO_CHECK]
AO_MAX_ERR_PCT = max(abs(e[3]) for e in AO_ERR)


def ao_circuit_error(i):
    """Output-circuit error (mA) at current i: linear between the checked points."""
    pts = [(c, m - c) for c, m in AO_CHECK]
    if i <= pts[0][0]:
        return pts[0][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if i <= x1:
            return y0 + (y1 - y0) * (i - x0) / (x1 - x0)
    return pts[-1][1]


# Story: vented transmitter, reference 0.000
I_STORY_ZERO = I_of(PV_OFFSET) + 0.0003                 # the output circuit error at 4 mA
ERR_STORY_ZERO = err_pct(I_STORY_ZERO, 4.0)             # about -0.398 %
PV_AFTER_TRIM, I_AFTER_TRIM = 0.0, I_of(0.0) + 0.0003


def calibration(offset, hysteresis):
    """Rows of one run: (point %, direction, applied P, PV shown, current mA, error % of span).
    Ascending 0…100 %, then descending back; the top point is recorded once."""
    rows = []
    order = [(p, "up") for p in POINTS] + [(p, "down") for p in reversed(POINTS[:-1])]
    for p, d in order:
        pv = p + offset + (hysteresis if d == "down" else 0.0)
        i_ideal = I_of(p)
        i_meas = I_of(pv) + ao_circuit_error(I_of(pv))
        rows.append({"pct": (p - LRV) / SPAN * 100.0, "dir": d, "p": p, "pv": pv,
                     "i": i_meas, "ideal": i_ideal, "err": err_pct(i_meas, i_ideal)})
    return rows


AS_FOUND = calibration(PV_OFFSET, HYSTERESIS)
AS_LEFT = calibration(0.0, HYSTERESIS)


def max_abs_err(rows):
    return max(abs(r["err"]) for r in rows)


def max_hysteresis(rows):
    """Largest |descending - ascending| current difference at the same point, in % of span."""
    up = {r["p"]: r for r in rows if r["dir"] == "up"}
    return max(abs(r["err"] - up[r["p"]]["err"]) for r in rows if r["dir"] == "down")


AS_FOUND_MAX, AS_LEFT_MAX = max_abs_err(AS_FOUND), max_abs_err(AS_LEFT)
HYST_PCT = max_hysteresis(AS_FOUND)                     # also as pressure: HYSTERESIS / SPAN


def self_test():
    assert SPAN == 40.0 and LRV < URV <= URL and LRL <= LRV and SPAN >= MIN_SPAN
    assert URV_NEW - LRV >= MIN_SPAN and URV_NEW <= URL and URV < REF_MODULE_MAX
    assert abs(I_BEFORE - 10.000) < 1e-12 and abs(I_AFTER - 12.000) < 1e-12
    assert abs(I_of(LRV) - 4) < 1e-12 and abs(I_of(URV) - 20) < 1e-12
    assert HART_MAX_DEVICES == POLL_MAX + 1 and I_HIGH - I_LOW == 16.0
    assert abs(P_MISREAD - 20.0) < 1e-9 and P_MISREAD != P_EX
    assert abs(I_STORY_ZERO - 3.9363) < 1e-9, I_STORY_ZERO
    assert abs(ERR_STORY_ZERO - (-0.398125)) < 1e-9, ERR_STORY_ZERO
    assert abs(I_AFTER_TRIM - 4.0003) < 1e-12 and PV_AFTER_TRIM == 0.0
    # AO check: the output circuit passes (well inside the reject limit)
    assert all(abs(e[3] - w) < 1e-9 for e, w in zip(AO_ERR, [0.00125, 0.001875, 0.00625, 0.01, 0.010625])), AO_ERR
    assert AO_MAX_ERR_PCT < REJECT_IF
    # NAMUR bands are in order
    assert NAMUR["low_fault"] < NAMUR["low_meas"] < 4 < 20 < NAMUR["high_meas"] < NAMUR["high_fault"]
    # Calibration runs: 5 points up + 4 down
    assert len(AS_FOUND) == len(AS_LEFT) == 9
    assert abs(HYST_PCT - HYSTERESIS / SPAN * 100.0) < 0.002 and abs(HYSTERESIS / SPAN * 100 - 0.01) < 1e-12
    # the story value is the same figure the As Found table shows at 0 %
    assert round(AS_FOUND[0]["i"], 4) == round(I_STORY_ZERO, 4)
    # As Found fails, As Left passes
    assert AS_FOUND_MAX > REJECT_IF, AS_FOUND_MAX
    assert AS_LEFT_MAX <= REJECT_IF and AS_LEFT_MAX < ADJUST_TO, AS_LEFT_MAX
    assert ADJUST_TO <= DO_NOT_ADJUST_IF < ADJUST_IF < REJECT_IF
    assert all(abs(r["pv"] - r["p"] - PV_OFFSET - (HYSTERESIS if r["dir"] == "down" else 0)) < 1e-12
               for r in AS_FOUND)


self_test()


def fmt(x, nd=3):
    """Number as shown on the screens (minus sign U+2212)."""
    return f"{x:.{nd}f}".replace("-", "−")


def print_table():
    print(f"I before / after rerange: {I_BEFORE:.3f} / {I_AFTER:.3f} mA at {P_EX} {UNIT}")
    for cmd, meas, d, e in AO_ERR:
        print(f"  AO {cmd:>5.1f} -> {meas:.4f}  err {e:+.4f} % of span")
    print(f"story zero: {I_STORY_ZERO:.4f} mA  {ERR_STORY_ZERO:+.3f} %   after trim {I_AFTER_TRIM:.4f} mA")
    for name, rows in (("As Found", AS_FOUND), ("As Left", AS_LEFT)):
        print(name, f"max |err| {max_abs_err(rows):.4f} %  hysteresis {max_hysteresis(rows):.4f} %")
        for r in rows:
            print(f"  {r['pct']:5.1f} % {r['dir']:>4}  PV {r['pv']:+.3f}  I {r['i']:.4f} mA  err {r['err']:+.4f} %")


if __name__ == "__main__":
    print_table()
