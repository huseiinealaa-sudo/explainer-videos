# Preview QA: two loops per video or episode, counted separately

1. **Automatic loop** (steps 1, 2, 4a): preview with `--qa` → overlap reports → fix every
   critical finding → again, until **zero critical findings**; at most **5 iterations**.
   It spends no critic round.
2. **Critic loop** (steps 3, 4b): the `video-critic` reviews, the fixes are made, the
   automatic loop runs again on the changed segments, next round; at most **3 rounds**.

Who runs what (root `CLAUDE.md`, Delegation): the per-segment automatic loop (steps 1, 2,
4a on `--segments`) runs inside the `scene-builder` agent, one call per segment, prompt =
project path, episode, segment id (+ the critic's issues for that segment in step 4b). The
whole-video QA run and the critic call (step 3) are the manager's; the manager reads the
agents' summaries, the counts and the reports, not the render logs. Segments of one script
run one after the other (they share `tmp/<script>/render.json` and the manim output file);
different scripts may run in parallel. The limits below are the same whoever runs them.

## 1. Preview in QA mode
```bash
# scripts that end with main(__file__, ...):
python projects/<name>/<script>.py --preview --qa          # whole video -> qa/full/
python projects/<name>/<script>.py --segments 4 --qa       # one segment -> qa/seg04/
python projects/<name>/<script>.py --segments 4-6 --qa     # a range     -> qa/seg04-06/
# any script, older ones included (prover series, ut_intro):
python -m explainer.qa projects/<name>/<script>.py [--segments 4]
```
Outputs in `tmp/<script>/qa/<run>/`: `overlap/segNN.json` (one overlap report per segment),
`sheets/sheet_NN.png` (contact sheets, 3×3 frames, 6×6 grid A1–F6, times on the narration
clock), `frames/*.png` (full-size frames), `index.json`, `qa_summary.json`. The console prints
the finding counts per segment.

Iteration 1 runs on the whole video (or, when segments are built by `scene-builder`, on
each segment as it is built, then once on the whole video by the manager). Later iterations may run only the segments that
changed (`--segments`), but the last run before a critic round and the last run before the
1080p render cover the whole video.

## 2. Read the overlap reports
Each finding has `time` / `until` (narration clock, s), `video_time` (in the preview file),
the two elements (`a`, `b`: name, text, bbox, cells), the amount (`area`, `share_of_text` or
`distance`, `gap`, `font_size`), the grid `cell` and a `suggestion`. Severity: `critical`
(texts overlapping, a line through a text, a text closer than `CLEARANCE` to a line, arrow
or shape outside its frame — `text_near_shape`, touching included —, a text touching its
frame, anything off the frame, text below the minimum size) or `improvement` (text inside
the safe margin). A text inside its own frame, a label's own leader arrow, a badge number or
a ✓/✗ mark on its box is not a finding.

Count the critical findings of all segments (the console prints them per segment). If it
is not zero, fix them (step 4a) and run step 1 again; after the 5th iteration go on to the
critic whatever the count.

## 3. Call the critic
Use the Agent tool with `subagent_type: "video-critic"` (read-only, keeps its memory in
`.claude/agent-memory/video-critic/`). Prompt:

```
Review round <n> of <script>, run <run>.
QA folder: tmp/<script>/qa/<run>/   Script (narration): projects/<name>/<script>.py
Storyboard: projects/<name>/storyboard/<script>.md   Data: projects/<name>/<name>_data.py
Word timings: tmp/<script>/audio/seg{k}.json
Changes since the last round: <none | list of fixes>
Automatic loop: <k> iterations, critical findings now <0 | n: time, elements, why they stayed>
```
The critic updates its memory file itself (Write/Edit, limited to
`.claude/agent-memory/video-critic/` by the hook `.claude/hooks/critic_memory_guard.py`) and
ends its report with a `Memory:` line; check the file changed as that line says.
Agent files are read when the session starts: a new `.claude/agents/` folder, or a change to
`video-critic.md` (its tools, its hook), takes effect only in a new session. Check the
critic's tools in the agent list (Read, Glob, Grep, Write, Edit). If the `video-critic` agent
type is not available in the session,
call a `general-purpose` agent with: "Act exactly as the agent defined in
.claude/agents/video-critic.md (read it first, including its memory file); read-only except
.claude/agent-memory/video-critic/", followed by the prompt above. That fallback has no
hook, so check with `git status` that it changed no other file.

## 4. Fix and repeat
a. **Automatic loop:** fix every critical overlap finding, then step 1 again (at most 5
   iterations; per segment, inside `scene-builder`; if it fails twice on the same segment
   the manager takes it over). Fix layout by relative placement (`next_to`, `arrange`, `align_to`, buff ≥
   0.15), not by nudging fixed coordinates; check the moved element against every text or
   shape added later in the segment (a fix often creates the next finding).
b. **Critic loop:** fix every critical and important issue of the critic; take the cheap
   improvements too (improvements never block PASS). The manager sorts the issues by
   segment and sends each segment's issues to `scene-builder`. Then the automatic loop again on the
   changed segments, then the next critic round.
- Record per video: automatic iterations (critical count after each) and critic rounds
  (counts before and after, what changed); per segment in `projects/<name>/PROGRESS.md`:
  the agent that built it and its number of calls.
- After the last round, the 1080p render, the size table and the commit of `output/` go
  to `render-runner` (SKILL.md step d.3).
- PASS = no critical and no important issue. Stop at PASS, or after critic round 3:
  production then goes on, and whatever is still open goes to the PR description (skill
  step f).
- Commit `.claude/agent-memory/video-critic/MEMORY.md` with the video: the container is
  temporary, so the critic's memory survives only through the repository.
