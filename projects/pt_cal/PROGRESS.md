# pt_cal — production progress (resume from here)

Branch: `claude/lucid-tesla-g1fjg2`. Order after the owner's approval of ep02 (2026-09-28): ep06 → ep05 → ep01 → ep03 → ep04 → ep07 → full-series file → one PR (request steps 6–7: PR with durations/sizes/QA table, then privacy grep for 607458 / FQ-314 / 314-PT and `git diff main...HEAD --stat`).

Per episode: script `projects/pt_cal/pt_cal_epNN_<name>.py` (narration copied verbatim from `storyboard/pt_cal_epNN_<name>.md`) → `--preview --qa` until 0 critical (≤ 5 iterations) → video-critic rounds (≤ 3, commit + push after each) → full QA run → 1080p → commit + push → one-line report.

Timing: start 17:50:19 UTC; narration done 18:19:26; model episode 19:03 → 20:10; other episodes from 20:1x.

## Done
- ep02 `pt_cal_ep02_pressure` — 5:30, 12.2 MB, critic PASS (round 3), owner approved the level.

## In progress
- ep06 `pt_cal_ep06_trim` — writing the script.

## Next step
- Write `projects/pt_cal/pt_cal_ep06_trim.py`, run `python projects/pt_cal/pt_cal_ep06_trim.py --preview --qa`.
