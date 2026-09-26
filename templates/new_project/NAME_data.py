"""NAME: every number shown or spoken in the videos (illustrative values only).

Optional: delete this file if the topic shows no numbers. Inputs are typed once here;
everything derived is computed, never typed by hand. self_test() runs on import so a
drift stops every script that uses the data.

    python projects/NAME/NAME_data.py      # print the table
"""
# ---------------- Inputs (illustrative) ----------------
FLOW_RATE = 250.0          # m3/h
VOLUME = 0.25              # m3

# ---------------- Derived ----------------
FILL_TIME = VOLUME / FLOW_RATE * 3600      # s


def self_test():
    assert FLOW_RATE > 0 and VOLUME > 0
    assert abs(FILL_TIME - 3.6) < 1e-9, FILL_TIME


self_test()


def print_table():
    for name, value, unit in [("Flow rate", f"{FLOW_RATE:.1f}", "m3/h"),
                              ("Volume", f"{VOLUME:.2f}", "m3"),
                              ("Fill time", f"{FILL_TIME:.1f}", "s")]:
        print(f"  {name:<12} {value:>8} {unit}")


if __name__ == "__main__":
    print_table()
