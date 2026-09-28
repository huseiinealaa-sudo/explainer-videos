# pt_cal — production progress (resume from here)

Branch: `claude/lucid-tesla-g1fjg2`. Order after the owner's approval of ep02 (2026-09-28): ep06 → ep05 → ep01 → ep03 → ep04 → ep07 → full-series file → one PR (request steps 6–7: PR with durations/sizes/QA table, then privacy grep for 607458 / FQ-314 / 314-PT and `git diff main...HEAD --stat`).

Per episode: script `projects/pt_cal/pt_cal_epNN_<name>.py` (narration copied verbatim from `storyboard/pt_cal_epNN_<name>.md`) → `--preview --qa` until 0 critical (≤ 5 iterations) → video-critic rounds (≤ 3, commit + push after each) → full QA run → 1080p → commit + push → one-line report.

Timing: start 17:50:19 UTC; narration done 18:19:26; model episode 19:03 → 20:10; other episodes from 22:50:41.

## Done
- ep02 `pt_cal_ep02_pressure` — 5:30, 12.2 MB, critic PASS (round 3), owner approved the level.
- ep06 `pt_cal_ep06_trim` — 3:01, 7.8 MB, critic PASS (round 2); open: text-scene share ≈ 40 %, save-note placement, valve stem motion, out-of-band dot style (improvements).

## In progress
- ep05 `pt_cal_ep05_verdict` — automatic loop at 0 critical (full it5); critic round 1 running.
- ep01 `pt_cal_ep01_device` — automatic loop at 0 critical (full it4); critic round 1 running.
- ep03 `pt_cal_ep03_setup` — fixes applied; full QA it5 running.
- ep04 `pt_cal_ep04_procedure` — fixes applied (leak chain vertical); full QA it7 running.
- ep07 `pt_cal_ep07_uncertainty` — automatic loop at 0 critical (full it2); critic after ep04.
- Series script written: `pt_cal_full_series.py` (run after all 7 are rendered).

## Next step
- Fix ep05/ep01 critic findings → next rounds → 1080p; then ep03, ep04, ep07 critic rounds; then the series file and the PR.
