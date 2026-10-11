"""ut_series: join the four episodes into output/ut_series_full.mp4.

A 3-second title card goes between episodes; the episodes are not re-rendered or re-encoded
(explainer.series.concat_series joins them in stream-copy mode and stops if any stream differs).

Build (from the repo root, with the virtual environment of the root CLAUDE.md active):
    python projects/ut_series/ut_series_full_series.py
"""
from explainer import OUTPUT_DIR
from explainer.series import concat_series

SERIES = "Ultrasonic Testing"
EPISODES = [
    ("ut_series_ep01_principle", "The principle"),
    ("ut_series_ep02_probe_beam", "The probe and the beam"),
    ("ut_series_ep03_calibration", "Calibration and angle-beam testing"),
    ("ut_series_ep04_weld_evaluation", "Weld examination and flaw evaluation"),
]
MAX_BYTES = 100 * 1024 * 1024

if __name__ == "__main__":
    out = concat_series([(OUTPUT_DIR / f"{stem}.mp4", title) for stem, title in EPISODES],
                        OUTPUT_DIR / "ut_series_full.mp4", series_title=SERIES)
    size = out.stat().st_size
    print(f"{out}: {size / 1e6:.1f} MB")
    assert size < MAX_BYTES, "over the 100 MB GitHub limit"
