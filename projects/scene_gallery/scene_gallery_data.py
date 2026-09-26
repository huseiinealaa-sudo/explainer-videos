"""Scene gallery: the illustrative numbers shown in the catalogue (no real data).

    python projects/scene_gallery/scene_gallery_data.py      # print the values
"""
# worked_calculation: A = B × C
CALC_B = 2.50
CALC_C = 4.00
CALC_A = CALC_B * CALC_C

# data_table: three runs, value and deviation from the target
TABLE_TARGET = 10.00
TABLE_VALUES = [10.02, 9.98, 10.40]
TABLE_TOLERANCE = 0.10
TABLE_ROWS = [[k + 1, f"{v:.2f}", f"{v - TABLE_TARGET:+.2f}",
               "OK" if abs(v - TABLE_TARGET) <= TABLE_TOLERANCE else "HIGH"]
              for k, v in enumerate(TABLE_VALUES)]
TABLE_BAD_ROW = next(k for k, r in enumerate(TABLE_ROWS) if r[3] != "OK")

# line_chart: six readings against an acceptance band
CHART_X = [1, 2, 3, 4, 5, 6]
CHART_Y = [1.00, 1.08, 0.96, 1.26, 1.04, 1.01]
CHART_BAND = (0.90, 1.20)
CHART_OUTLIERS = [x for x, y in zip(CHART_X, CHART_Y)
                  if not CHART_BAND[0] <= y <= CHART_BAND[1]]

# bar_chart: four durations against a limit
BAR_LABELS = ["A", "B", "C", "D"]
BAR_VALUES = [3.2, 4.1, 5.6, 2.0]
BAR_LIMIT = 5.0
BAR_OVER = [n for n, v in zip(BAR_LABELS, BAR_VALUES) if v > BAR_LIMIT]

# document_panel: a short illustrative report built from the table rows above
DOC_LINES = [("TEST REPORT                 DEMO-001", "BOLD")] + [
    f"TARGET {TABLE_TARGET:.2f}   TOLERANCE {TABLE_TOLERANCE:.2f}",
    f"{'RUN':<5}{'VALUE':>8}{'DEV':>8}{'RESULT':>9}"] + [
    f"{r[0]:<5}{r[1]:>8}{r[2]:>8}{r[3]:>9}" for r in TABLE_ROWS] + [
    (f"MEAN {sum(TABLE_VALUES) / len(TABLE_VALUES):.2f}", "BOLD")]
DOC_CHECK_LINE = 3 + TABLE_BAD_ROW        # the out-of-tolerance run


def self_test():
    assert abs(CALC_A - 10.0) < 1e-9, CALC_A
    assert TABLE_BAD_ROW == 2 and TABLE_ROWS[2][3] == "HIGH", TABLE_ROWS
    assert CHART_OUTLIERS == [4], CHART_OUTLIERS
    assert BAR_OVER == ["C"], BAR_OVER
    assert "HIGH" in DOC_LINES[DOC_CHECK_LINE], DOC_LINES


self_test()

if __name__ == "__main__":
    print(f"A = {CALC_B:.2f} x {CALC_C:.2f} = {CALC_A:.2f}")
    for r in TABLE_ROWS:
        print("row", r)
    print("chart outliers", CHART_OUTLIERS, "bars over limit", BAR_OVER)
