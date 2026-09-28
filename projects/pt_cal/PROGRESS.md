# pt_cal — production progress (resume from here)

Branch: `claude/lucid-tesla-g1fjg2`. Order after the owner's approval of ep02 (2026-09-28): ep06 → ep05 → ep01 → ep03 → ep04 → ep07 → full-series file → one PR (request steps 6–7: PR with durations/sizes/QA table, then privacy grep for 607458 / FQ-314 / 314-PT and `git diff main...HEAD --stat`).

Per episode: script `projects/pt_cal/pt_cal_epNN_<name>.py` (narration copied verbatim from `storyboard/pt_cal_epNN_<name>.md`) → `--preview --qa` until 0 critical (≤ 5 iterations) → video-critic rounds (≤ 3, commit + push after each) → full QA run → 1080p → commit + push → one-line report.

Timing: start 17:50:19 UTC; narration done 18:19:26; model episode 19:03 → 20:10; other episodes from 20:1x.

## Done
- ep02 `pt_cal_ep02_pressure` — 5:30, 12.2 MB, critic PASS (round 3), owner approved the level.

## In progress
- ep06 `pt_cal_ep06_trim` — automatic loop 13 → 1 → 0 (seg 4); full verification run (it4) running; next: video-critic round 1.
- ep05 `pt_cal_ep05_verdict` — automatic loop 28 → 2 → fixed; it3 running.
- ep01 `pt_cal_ep01_device` — automatic loop 13 → fixed; it2 running.
- ep03 `pt_cal_ep03_setup` — script written; it1 running.
- ep04, ep07 — scripts not written yet.
- QA helper used: scratchpad `qarun.sh <script> <tag> --preview|--segments N` (prints the critical findings).

## Next step
- Read the four QA outputs, fix, repeat to 0 critical; call video-critic for ep06 first (order ep06, ep05, ep01, ep03, ep04, ep07); write `pt_cal_ep04_procedure.py` and `pt_cal_ep07_uncertainty.py`.
