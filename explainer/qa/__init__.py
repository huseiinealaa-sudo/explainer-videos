"""QA tools for previews: the automatic overlap check and the contact sheets.

    python projects/<name>/<script>.py --segments 2 --qa     # scripts that end with main()
    python -m explainer.qa projects/<name>/<script>.py --segments 2   # any script (old ones too)

Both render a low-quality preview in QA mode and write tmp/<script>/qa/<run>/
(run = full | seg02 | seg02-03):
    overlap_raw.json       every finding on the narration clock (written by the scene)
    overlap/segNN.json     one overlap report per narration segment
    sheets/sheet_NN.png    contact sheets: 3×3 frames with the 6×6 grid and their times
    frames/*.png           the same frames one by one, full size
    index.json             frame list (clock time, segment, sheet and position)
    qa_summary.json        what was checked and the finding counts per segment
The video critic (.claude/agents/video-critic.md) reads these files.
`python -m explainer.qa.selftest` checks the overlap rules on small layouts (no rendering).
"""
import json
from pathlib import Path

from ..timing import media_duration
from .contact_sheet import contact_sheets
from .overlap import OverlapChecker, analyse, collect, report_by_segment  # noqa: F401


def finish_qa(video, qa_dir, starts, offset, segments, script=""):
    """After a QA-mode render: overlap reports per segment + contact sheets + summary.

    segments: the narration segments the preview was asked for (1-based).
    """
    qa_dir = Path(qa_dir)
    duration = media_duration(video)
    segs = list(segments)
    meta = {"script": script, "preview": str(video)}
    counts = report_by_segment(qa_dir / "overlap_raw.json", starts, qa_dir / "overlap", segs,
                               offset=offset, meta=meta)
    title = f"{script}  ·  {Path(video).name}"
    index = contact_sheets(video, qa_dir, offset=offset, title=title,
                           segments=[(k, starts[k - 1], starts[k]) for k in segs])
    summary = {**meta, "clock_offset": round(offset, 3), "duration": round(duration, 2),
               "segments": segs, "findings": counts, "overlap_reports":
               [str(qa_dir / "overlap" / f"seg{k:02d}.json") for k in segs],
               "sheets": index["sheets"], "frames": len(index["frames"])}
    (qa_dir / "qa_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"QA {script}: {qa_dir}")
    for k in segs:
        c = counts[k]
        print(f"  segment {k:2d}: {c['critical']} critical, {c['important']} important")
    print(f"  {len(index['frames'])} frames on {len(index['sheets'])} sheets")
    return summary
