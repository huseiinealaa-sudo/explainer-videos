---
name: explainer-video
description: The production procedure for every explainer video in this repository. Load it for ANY request to make, continue, extend or redo a video, an episode or a series (e.g. "اصنع فيديو", "حلقة جديدة", "سلسلة", "حوّل هذا الملف إلى فيديو", "make an explainer video from this source", "produce episode 2", "re-render the preview"). It covers the whole path from the cleaned source to one pull request - material inventory, storyboard, narration with the quality gate, the preview QA loops (automatic overlap loop to zero critical findings, at most 5 iterations; then contact sheets, video-critic agent and fixes, at most 3 rounds), the 1080p render, the first-episode approval stop, the remaining episodes, the PR and the privacy check.
---

# Explainer video: from source to pull request

The rules live in the root `CLAUDE.md` (Quality standard, Fast workflow, Narration, Scene
library, Preview QA, Accuracy and privacy) and in `projects/<name>/CLAUDE.md`; this skill is
the order of work. Reply to the owner in Arabic. Record the start time with `date` when the
work begins and the end time when the PR is opened; time is measured, not targeted.

Reference files next to this one:
- `storyboard_template.md`: the storyboard table and how to fill it.
- `approval_message.md`: the one approval message (storyboard + narration + quality gate).
- `qa_loop.md`: the commands of the two preview QA loops and how to call the critic.
- `privacy_check.md`: the final privacy check of the pull request.

## Steps

### 0. Session setup
Run the session setup of the root `CLAUDE.md` (manim, `pip install -e .`, checks).

### a. Intake: source, data, material inventory, outline
1. Read the cleaned source `projects/<name>/sources/<name>_source.md` (new project: start
   from `templates/new_project/`, see its `CLAUDE.md`) and the project's data module
   `projects/<name>/<name>_data.py` if the topic has numbers.
2. Take the outline and constraints from the owner's request (episodes, audience, length,
   language, voice).
3. Make the **material inventory**: every main section of the source → its concepts, the
   mechanisms / motions / sequences to animate, the numbers (worked examples), and what
   needs privacy transformation (site cases, real numbers, screenshots → illustrative
   examples or simplified drawings). Size the video from it: 2–4 minutes per main section,
   one main idea per segment, series of 3–5-minute episodes by default.
4. Research only verifies (Fast workflow step 2); save sources per video in
   `projects/<name>/sources/<name>_<video>.md`.

### b. Storyboard before narration
Write `projects/<name>/storyboard/<name>_<video>.md` for every video or episode, using
`storyboard_template.md`: per segment the idea, what is drawn, what moves, the worked
example, the scene (library function or custom drawing) and the duration. Mechanisms and
motions are custom drawings; the library is for titles, equations, tables. For process
and instrument drawings, build from `explainer.symbols` (ISA valves, pumps, flow elements,
bubbles, joined by `connect()` with the right line type) and add `icon()` pictograms where a
label needs one (root `CLAUDE.md`, Scene library: Icons and engineering symbols). Keep text and
table scenes at about one third of each episode or less. The storyboard is shown with the
narration (step c), never approved on its own.

### c. All narration at once, with the quality gate
Write the fully diacritized narration of ALL episodes in one go, and present it in ONE
message together with the storyboard, the quality gate, source conflicts and new values
(format: `approval_message.md`). The quality gate lists per episode: the number of worked
examples, the number of custom drawings, the share of text-scene time, and everything left
out with its reason and a proposal. Nothing is dropped silently. Then wait for approval.

### d. After approval: the first episode (or the single video)
1. Write the script `projects/<name>/<name>_<video>.py` from the storyboard (`from explainer
   import *`, `SyncedScene`, cues from the word timings, numbers from the data module,
   layout by `next_to` / `arrange` / `align_to` inside the safe margin).
2. QA — two loops, counted separately (commands and critic call: `qa_loop.md`):
   - **Automatic loop, at most 5 iterations:** preview in QA mode (`--qa`) → overlap
     reports → fix every critical finding → again, until the reports show **zero critical
     findings**. Later iterations may run only the changed segments (`--segments`), the
     last one covers the whole video. No critic round is spent here.
   - **Critic loop, at most 3 rounds:** contact sheets + overlap reports → `video-critic`
     → fix every critical and important issue (and the cheap improvements) → run the
     automatic loop again on the changed segments → next critic round.
   - If critical findings are still open after 5 automatic iterations, call the critic
     anyway and list them in its prompt (time, elements, why they stayed); they count as
     open issues of that round.
   Severity: **critical** = an error of accuracy or numbers, an overlap, anything leaving
   the frame, unreadable text; **important** = drawing not matching the speech at that
   moment (a spoken motion that does not happen), or no visual pointer on the element
   being explained; **improvement** = everything else, never blocking.
   **PASS** = no critical and no important issue. Stop at PASS, or after critic round 3:
   then production goes on and what remains is listed in the PR (step f). Record per
   video the number of automatic iterations and critic rounds.
3. Render 1080p (`python projects/<name>/<name>_<video>.py`), check the file size (< 100 MB),
   commit the script, data, storyboard, sources, the video in `output/` and the critic's
   memory (`.claude/agent-memory/video-critic/`), and push the branch.
4. **Series: stop here** and present the first episode to the owner (link, duration, the QA
   rounds and their result, anything left open). The other episodes are completed only after
   the owner approves this level. This is the only stop after the narration approval,
   besides an error that blocks completion. A single video goes on to step e directly.

### e. The other episodes, one pull request, privacy check
1. Produce every other episode with the same loop (step d.1–d.3) without stopping; fix
   layout and sync as part of production.
2. Open ONE pull request for the whole work (series: also `concat_series` if the project
   asks for a full-series file). Its description gives the start and end times, the videos
   with durations, the QA result per episode, and step f.
3. Run the privacy check of `privacy_check.md` over everything the PR contains; fix and push
   on the same PR if anything is found, and say so in the PR.

### f. What remains after 3 critic rounds is reported, not hidden
Every issue still open after the third critic round (critic or overlap report) goes in the PR
description: episode, time, grid cell, the issue, and why it was left. Never present an
episode as clean when the last round was FIX.
