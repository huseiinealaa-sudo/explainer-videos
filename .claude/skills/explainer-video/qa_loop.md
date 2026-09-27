# Preview QA loop (at most 3 rounds per video or episode)

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

Round 1 runs on the whole video. Later rounds may run only the segments that changed
(`--segments`), but the last round before the 1080p render covers the whole video.

## 2. Read the overlap reports
Each finding has `time` / `until` (narration clock, s), `video_time` (in the preview file),
the two elements (`a`, `b`: name, text, bbox, cells), the amount (`area`, `share_of_text` or
`distance`, `font_size`), the grid `cell` and a `suggestion`. Severity: `critical` (texts
overlapping, a line through a text, a text touching its frame, anything off the frame, text
below the minimum size) or `improvement` (text inside the safe margin). A text inside its own
frame, a badge number or a ✓/✗ mark on its box is not a finding.

## 3. Call the critic
Use the Agent tool with `subagent_type: "video-critic"` (read-only, keeps its memory in
`.claude/agent-memory/video-critic/`). Prompt:

```
Review round <n> of <script>, run <run>.
QA folder: tmp/<script>/qa/<run>/   Script (narration): projects/<name>/<script>.py
Storyboard: projects/<name>/storyboard/<script>.md   Data: projects/<name>/<name>_data.py
Word timings: tmp/<script>/audio/seg{k}.json
Changes since the last round: <none | list of fixes>
```
If the `video-critic` agent type is not available in the session (agent files are loaded
when the session starts, so a newly created `.claude/agents/` folder needs a new session),
call a `general-purpose` agent with: "Act exactly as the agent defined in
.claude/agents/video-critic.md (read it first, including its memory file); read-only except
.claude/agent-memory/video-critic/", followed by the prompt above.

## 4. Fix and repeat
- Fix every critical and important issue of the critic and every critical overlap finding;
  take the cheap improvements too (improvements never block PASS). Fix layout by relative
  placement (`next_to`, `arrange`, `align_to`), not by nudging fixed coordinates.
- Record per round: counts before and after, what changed.
- PASS = no critical and no important issue. Stop at PASS, or after round 3: production
  then goes on, and whatever is still open goes to the PR description (skill step f).
- Commit `.claude/agent-memory/video-critic/MEMORY.md` with the video: the container is
  temporary, so the critic's memory survives only through the repository.
