# Storyboard template

File: `projects/<name>/storyboard/<name>_<video>.md`, one per video or episode, written
before the narration and shown to the owner with it. The critic reads it after every preview.

```markdown
# <name>_<video> — <episode title>   (target <m:ss>, <N> segments)

| # | Idea (one per segment) | What is drawn | What moves | Worked example | Scene | Duration |
|---|---|---|---|---|---|---|
| 1 | Why a prover: the meter must be checked in service | meter, prover, pipe loop | liquid flows meter → prover | — | title_card + custom loop drawing | 0:40 |
| 2 | The piston sweeps a known volume between two detectors | flow tube, piston, D1, D2 | piston travels D1 → D2, pulses counted | 15 000 pulses ÷ 0.25 m³ = 60 000 pls/m³ | custom (mechanism) | 0:55 |
| 3 | Meter factor | MF equation | parts coloured in turn | MF = 0.25000 ÷ 0.24970 = 1.0012 | worked_calculation | 0:35 |

Text-scene share: <text and table seconds> / <total seconds> = <NN %> (limit ~33 %)
Custom drawings: <n>   Worked examples: <n>
Left out (with reason and proposal): <none | list>
```

How to fill it:
- **Idea**: one sentence, the single main idea of the segment (what it is, why it matters).
- **What is drawn**: the objects on screen, English labels only.
- **What moves**: every mechanism, motion or sequence as an animation (piston travels,
  valve closes, pulses flow, a value lights up). "Nothing moves" is a warning sign for
  anything that is a mechanism.
- **Worked example**: at most ONE step-by-step example per episode, for its most important
  equation (one the technician uses at work); every other number is a visual result (bars,
  comparisons, a reading on a screen) without calculation steps. The numbers come from the
  data module (name the variables), never typed by hand.
- **Scene**: a library function (`title_card`, `equation`, `worked_calculation`,
  `data_table` ...) for general structure, or "custom" for mechanisms and motions. Count
  text-only scenes (bullets, tables, equation-only screens, summary, document panel) for the
  text-scene share.
- **Duration**: an estimate from the narration length (Arabic narration at normal speed is
  about 2.2 words per second); the final durations come from the audio.
