"""rt_intro: every number shown or spoken in the video (illustrative values only).

Inputs are typed once here; everything derived is computed at full precision, never
typed by hand. self_test() runs on import, so a drift stops the video script.
Units: mm (and days).

    python projects/rt_intro/rt_intro_data.py      # print the table
"""
# ---------------- Inputs (illustrative) ----------------
F = 3.0                     # mm, source size (largest projected dimension)
d = 20.0                    # mm, source side of the weld -> film (film in contact: the thickness)
D1 = 400.0                  # mm, source -> source side of the weld (first set-up)
D2 = 200.0                  # mm, the source moved closer (half the distance)
UG_MAX = 0.51               # mm, illustrative limit (0.020 in, ASME V, thickness under 2 in)

# ---------------- Published value (see sources/rt_intro_principle.md) ----------------
IR192_HALF_LIFE_DAYS = 74   # days, approximate (73.8 d)


# ---------------- Derived ----------------
def ug(f, d_, big_d):
    """Geometric unsharpness Ug = F × d / D (similar triangles)."""
    return f * d_ / big_d


UG1 = ug(F, d, D1)          # mm
UG2 = ug(F, d, D2)          # mm
UG_RATIO = UG2 / UG1        # halving D doubles Ug
D_MIN = F * d / UG_MAX      # mm, smallest source distance that keeps Ug <= UG_MAX


def self_test():
    assert F > 0 and d > 0 and D1 > 0 and D2 > 0 and UG_MAX > 0
    assert abs(UG1 - 0.15) < 1e-12, UG1
    assert abs(UG2 - 0.30) < 1e-12, UG2
    assert abs(UG_RATIO - 2.0) < 1e-12, UG_RATIO
    assert abs(D_MIN - 117.64705882352942) < 1e-9, D_MIN
    assert f"{D_MIN:.1f}" == "117.6"
    assert abs(ug(F, d, D_MIN) - UG_MAX) < 1e-12        # the limit is met exactly at D_MIN
    assert UG1 <= UG_MAX and UG2 <= UG_MAX              # both set-ups pass the limit
    assert abs(UG_MAX / 25.4 - 0.020) < 1e-3            # 0.51 mm is 0.020 in
    assert IR192_HALF_LIFE_DAYS == 74


self_test()


def print_table():
    for name, value, unit in [("F (source size)", f"{F:.1f}", "mm"),
                              ("d (object-film)", f"{d:.1f}", "mm"),
                              ("D1", f"{D1:.1f}", "mm"),
                              ("D2", f"{D2:.1f}", "mm"),
                              ("Ug1 = F d / D1", f"{UG1:.2f}", "mm"),
                              ("Ug2 = F d / D2", f"{UG2:.2f}", "mm"),
                              ("Ug2 / Ug1", f"{UG_RATIO:.0f}", ""),
                              ("Ug max (illustr.)", f"{UG_MAX:.2f}", "mm"),
                              ("D min = F d / Ug max", f"{D_MIN:.6f}", "mm"),
                              ("Ir-192 half-life", f"{IR192_HALF_LIFE_DAYS}", "days")]:
        print(f"  {name:<22} {value:>12} {unit}")


if __name__ == "__main__":
    print_table()
