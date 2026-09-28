"""pt_cal: join the seven episodes into output/pt_cal_full_series.mp4.

A 3-second title card goes between episodes; the episodes are not re-rendered or re-encoded
(explainer.series.concat_series joins them in stream-copy mode and stops if any stream differs).

Build (from the repo root):
    python projects/pt_cal/pt_cal_full_series.py
"""
from explainer import OUTPUT_DIR
from explainer.series import concat_series

SERIES = "Pressure transmitter calibration with the MC6"
EPISODES = [
    ("pt_cal_ep01_device", "The calibrator and its pressure modules"),
    ("pt_cal_ep02_pressure", "Generating the pressure"),
    ("pt_cal_ep03_setup", "Preparation, connection, safety"),
    ("pt_cal_ep04_procedure", "The procedure and pressure decay"),
    ("pt_cal_ep05_verdict", "Calculation, verdict, certificate"),
    ("pt_cal_ep06_trim", "Trim and error patterns"),
    ("pt_cal_ep07_uncertainty", "Error, uncertainty and TUR"),
]
MAX_BYTES = 100 * 1024 * 1024

if __name__ == "__main__":
    out = concat_series([(OUTPUT_DIR / f"{stem}.mp4", title) for stem, title in EPISODES],
                        OUTPUT_DIR / "pt_cal_full_series.mp4", series_title=SERIES)
    size = out.stat().st_size
    print(f"{out}: {size / 1e6:.1f} MB")
    assert size < MAX_BYTES, "over the 100 MB GitHub limit"
