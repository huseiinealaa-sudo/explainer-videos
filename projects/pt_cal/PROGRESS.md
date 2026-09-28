# pt_cal — production progress (resume from here)

Branch: `claude/lucid-tesla-g1fjg2`. Order after the owner's approval of ep02 (2026-09-28): ep06 → ep05 → ep01 → ep03 → ep04 → ep07 → full-series file → one PR (request steps 6–7: PR with durations/sizes/QA table, then privacy grep for 607458 / FQ-314 / 314-PT and `git diff main...HEAD --stat`).

Per episode: script `projects/pt_cal/pt_cal_epNN_<name>.py` (narration copied verbatim from `storyboard/pt_cal_epNN_<name>.md`) → `--preview --qa` until 0 critical (≤ 5 iterations) → video-critic rounds (≤ 3, commit + push after each) → full QA run → 1080p → commit + push → one-line report.

Timing: start 17:50:19 UTC; narration done 18:19:26; model episode 19:03 → 20:10; other episodes from 22:50:41.

## Done
- ep02 `pt_cal_ep02_pressure` — 5:30, 12.2 MB, critic PASS (round 3), owner approved the level.

## In progress
- ep06 `pt_cal_ep06_trim` — automatic loop to 0 critical; critic round 1 = FIX (3 critical, 14 improvements); fixes committed. Next: full QA (it5) → critic round 2.
- ep05 `pt_cal_ep05_verdict` — automatic loop at 0 critical (seg 5 re-run it4 = 0). Next: full run, then critic round 1.
- ep01 `pt_cal_ep01_device` — automatic loop at 0 critical (seg 8 re-run it3 = 0). Next: full run, then critic.
- ep03 `pt_cal_ep03_setup` — it2: 8 critical (segs 1, 3, 6, 7) → fixing.
- ep04 `pt_cal_ep04_procedure` — it1 stopped on a cue assertion in seg 5 ('وَخُرْطُومٌ أَقْصَرُ') → fixing.
- ep07 `pt_cal_ep07_uncertainty` — it1: 25 critical (segs 1, 2, 3, 4, 5, 7) → fixing.
- QA helper used: scratchpad `qarun.sh <script> <tag> --preview|--segments N` (prints the critical findings).

## Next step
- ep06 full QA it5 → video-critic round 2; in parallel fix ep03/ep04/ep07 automatic-loop findings.
