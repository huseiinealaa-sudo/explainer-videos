# mc5_hart: Production Progress

Start of the session: 2026-10-16 11:11:36 UTC. The manager (main session) wrote and built every segment and fixed every finding itself (owner's cost rule); sub-agents only for the critic and, after the critic loop, the final render.

## Episode 1: mc5_hart_ep01_connect

| Segment | Built by | Calls | Automatic loop (critical findings) |
|---|---|---|---|
| 1–16 | manager | script written once, fixed in segment batches | first runs 3, 14, 9, 25, 40, 8, 14 across batches → 0 in the whole-video run |

- Final render (1080p, RENDER_OK): duration 5:06.13, size 11.61 MiB (12,173,119 bytes); git hash before: none (no earlier output file), after: 5c3f1d574afbc1a0696563cf35ad43ecb41c2eb6.

- Critic: round 1 FIX (1 critical, 5 important, 11 improvements, whole episode) → round 2 FIX (0 critical, 2 important, 5 improvements, changed segments) → round 3 FIX (1 critical, 0 important, 4 improvements, changed segments). All round-3 items except one optional timing remark (the 2.0 s mark stays 2.4 s before the segment end) were fixed afterwards by the manager and checked by the automatic loop (whole video 0 critical, 0 improvement); the critic did not re-review those last fixes (3-round limit).
- Automatic loop: segment batches, then 5 whole-video runs; the last one 0 critical and 0 improvement findings.
- Text-scene share: the storyboard says 20 %; the critic counted about 22–27 % depending on what is counted (limit about 33 %).
- Hash check by the manager: `git hash-object` equals the «after» row.
