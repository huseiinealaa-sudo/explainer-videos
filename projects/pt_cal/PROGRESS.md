# pt_cal — production progress (resume from here)

Branch: `claude/lucid-tesla-g1fjg2`. Order after the owner's approval of ep02 (2026-09-28): ep06 → ep05 → ep01 → ep03 → ep04 → ep07 → full-series file → one PR (request steps 6–7: PR with durations/sizes/QA table, then privacy grep for 607458 / FQ-314 / 314-PT and `git diff main...HEAD --stat`).

Per episode: script `projects/pt_cal/pt_cal_epNN_<name>.py` (narration copied verbatim from `storyboard/pt_cal_epNN_<name>.md`) → `--preview --qa` until 0 critical (≤ 5 iterations) → video-critic rounds (≤ 3, commit + push after each) → full QA run → 1080p → commit + push → one-line report.

Timing: start 17:50:19 UTC; narration done 18:19:26; model episode 19:03 → 20:10; other episodes from 22:50:41.

## Done
- ep02 `pt_cal_ep02_pressure` — 5:30, 12.2 MB, critic PASS (round 3), owner approved the level.
- ep06 `pt_cal_ep06_trim` — 3:01, 7.8 MB, critic PASS (round 2).
- ep05 `pt_cal_ep05_verdict` — 3:45, 9.0 MB, critic PASS (round 2).
- ep01 `pt_cal_ep01_device` — 4:21, 9.0 MB, critic PASS (round 2).

## Open items (owner decides after viewing)
- Text-scene share above the ~33 % guideline: ep01 ≈ 38 %, ep05 ≈ 40 %, ep06 ≈ 40 % (critic measures). Not treated now, per the owner (2026-09-29).

## In progress
- ep07 `pt_cal_ep07_uncertainty` — critic round 1 = FIX (4 important: seg 6 E+U arrow in the doubt zone; guard band never narrowed / zones unnamed; seg 4 conversions only listed; seg 5 bars unnamed). Fixing.
- ep04 `pt_cal_ep04_procedure` — critic round 1 = FIX (3 important: seg 2 hysteresis not drawn; seg 5 stability/delay text only; seg 6 fixes not animated). Fixing.
- ep03 `pt_cal_ep03_setup` — critic round 1 interrupted by the usage limit; re-run.
- Series script written: `pt_cal_full_series.py` (run after all 7 are rendered).
- Usage-limit pause: 2026-09-28 23:59 → 2026-09-29 16:30 UTC (excluded from times).

## Next step
- ep03 critic round 1 (re-run); fix ep07 and ep04 findings → critic round 2 → 1080p; then series file, PR, privacy grep.
