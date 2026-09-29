"""Final 1080p render of ONE episode, with a verdict that cannot report a render that did not happen.

    python -m explainer.final_render projects/<name>/<script>.py [--expected SECONDS]

The only way the render-runner agent renders a final video (.claude/agents/render-runner.md).
It was written after PR #19, where a render cut off by the Bash time limit was reported as
done: the "after" row was read from the old file.

    1. Before: git hash-object, size and ffprobe duration/resolution of output/<script>.mp4
       (if it exists).
    2. Starts `python <script>` detached, its output in tmp/<script>/final_render/render.log,
       its exit code written to exit_code when it ends, and waits for it with a progress
       line every minute. The wait stops after --wait seconds (default 540, under the
       10-minute limit of one Bash command); the render keeps running, and running the
       same command again waits on it instead of starting a second one (state.json).
    3. After: the exit code is 0, the file exists, its hash changed, it is 1920x1080, and
       its duration matches the expected one (the narration audio, or --expected) within
       1 s.
    4. Prints one verdict line: RENDER_OK with a before/after table, or RENDER_FAILED with
       the reasons and the last 20 lines of the log; RENDER_RUNNING only when the wait
       window ended first (run the same command again). Exit code 0 / 1 / 3.
"""
import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from .style import BUILD_DIR, FINAL_RESOLUTION, OUTPUT_DIR, ROOT

TOLERANCE = 1.0             # seconds between the video and the expected duration
WAIT = 540                  # seconds one invocation waits (one Bash command allows 600)
PROGRESS_EVERY = 60         # seconds between progress lines
MAX_HOURS = 3               # a render still running after this is stopped and failed
LOG_TAIL = 20

# The detached child: runs the command, then writes its exit code (atomically) when it ends,
# so a later invocation can read the result even if the one that started it was killed.
CHILD = 'log=$1; rc=$2; shift 2; "$@" >"$log" 2>&1; echo $? >"$rc.tmp"; mv "$rc.tmp" "$rc"'


# ---------------- Measurements ----------------
def git_hash(path):
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def probe(path):
    """(duration, width, height) with ffprobe; None where it cannot be read."""
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height:format=duration", "-of", "json",
             str(path)], text=True, stderr=subprocess.DEVNULL)
        data = json.loads(out)
    except (subprocess.CalledProcessError, json.JSONDecodeError, OSError):
        return None, None, None
    s = (data.get("streams") or [{}])[0]
    d = data.get("format", {}).get("duration")
    return (float(d) if d not in (None, "N/A") else None), s.get("width"), s.get("height")


def snapshot(path):
    """Fingerprint of a video file, or None if it does not exist."""
    path = Path(path)
    if not path.is_file():
        return None
    duration, width, height = probe(path)
    return {"hash": git_hash(path), "size": path.stat().st_size, "duration": duration,
            "width": width, "height": height, "mtime": path.stat().st_mtime}


def expected_duration(audio_dir):
    """Total length of the narration segments seg1.mp3, seg2.mp3 ... (in order, stopping at
    the first missing one): the length the merged video must have."""
    from .timing import media_duration
    total, i = 0.0, 1
    while (Path(audio_dir) / f"seg{i}.mp3").is_file():
        total += media_duration(Path(audio_dir) / f"seg{i}.mp3")
        i += 1
    return total if i > 1 else None


# ---------------- Verdict ----------------
def check(before, after, exit_code, expected, tolerance=TOLERANCE, resolution=FINAL_RESOLUTION):
    """Reasons the render failed (an empty list means RENDER_OK)."""
    reasons = []
    if exit_code != 0:
        reasons.append(f"render exit code {exit_code}, not 0")
    if after is None:
        reasons.append("output file missing after the render")
        return reasons
    if before is not None and after["hash"] == before["hash"]:
        reasons.append(f"output unchanged: git hash {after['hash'][:12]} same as before")
    if (after["width"], after["height"]) != tuple(resolution):
        reasons.append(f"resolution {after['width']}x{after['height']}, "
                       f"not {resolution[0]}x{resolution[1]}")
    if after["duration"] is None:
        reasons.append("duration unreadable by ffprobe")
    elif expected is None:
        reasons.append("expected duration unknown (no narration audio; pass --expected)")
    elif abs(after["duration"] - expected) > tolerance:
        reasons.append(f"duration {after['duration']:.2f} s, expected {expected:.2f} s "
                       f"(difference {after['duration'] - expected:+.2f} s > {tolerance:g} s)")
    return reasons


def mmss(seconds):
    if seconds is None:
        return "?"
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:05.2f}"


def table(name, before, after):
    rows = ["| | git hash | size (bytes) | size (MiB) | duration | resolution |",
            "|---|---|---|---|---|---|"]
    for tag, snap in (("before", before), ("after", after)):
        if snap is None:
            rows.append(f"| {tag} | (no file) | | | | |")
        else:
            rows.append(f"| {tag} | {snap['hash'][:12]} | {snap['size']:,} | "
                        f"{snap['size'] / 2**20:.2f} | {mmss(snap['duration'])} | "
                        f"{snap['width']}x{snap['height']} |")
    return f"{name}\n" + "\n".join(rows)


def tail(path, n=LOG_TAIL):
    try:
        lines = Path(path).read_text(errors="replace").splitlines()
    except OSError:
        return "(no log)"
    return "\n".join(lines[-n:]) if lines else "(empty log)"


def verdict(state, exit_code):
    """The final report: (ok, text)."""
    out = Path(state["output"])
    after = snapshot(out)
    expected = state.get("expected")
    if expected is None:
        expected = expected_duration(state["audio_dir"])
    reasons = check(state["before"], after, exit_code, expected)
    try:
        name = str(out.relative_to(ROOT))
    except ValueError:
        name = str(out)
    if reasons:
        return False, (f"RENDER_FAILED: {'; '.join(reasons)}\n"
                       f"{table(name, state['before'], after)}\n"
                       f"--- last {LOG_TAIL} lines of {state['log']} ---\n{tail(state['log'])}")
    return True, (f"RENDER_OK: {name} rendered, exit 0, hash changed, "
                  f"{after['width']}x{after['height']}, {mmss(after['duration'])} "
                  f"(expected {mmss(expected)})\n{table(name, state['before'], after)}")


# ---------------- Detached render ----------------
_CHILDREN = {}              # pid -> Popen of renders started by this process


def alive(pid):
    if pid in _CHILDREN:                     # our own child: poll() also reaps a zombie
        return _CHILDREN[pid].poll() is None
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def read_exit_code(state):
    p = Path(state["exit_code"])
    if not p.is_file():
        return None
    try:
        return int(p.read_text().strip())
    except ValueError:
        return -1


def start(cmd, output, work_dir, audio_dir, expected=None):
    """Snapshot the output, start cmd detached and return its state (also saved to disk)."""
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    log, rc = work_dir / "render.log", work_dir / "exit_code"
    for p in (log, rc, work_dir / "exit_code.tmp"):
        p.unlink(missing_ok=True)
    state = {"cmd": [str(c) for c in cmd], "output": str(output), "audio_dir": str(audio_dir),
             "log": str(log), "exit_code": str(rc), "expected": expected,
             "before": snapshot(output), "started": time.time(), "reported": False}
    proc = subprocess.Popen(["sh", "-c", CHILD, "sh", str(log), str(rc), *state["cmd"]],
                            cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL, start_new_session=True)
    state["pid"] = proc.pid
    _CHILDREN[proc.pid] = proc
    save(work_dir, state)
    return state


def save(work_dir, state):
    (Path(work_dir) / "state.json").write_text(json.dumps(state, indent=1))


def load(work_dir):
    p = Path(work_dir) / "state.json"
    return json.loads(p.read_text()) if p.is_file() else None


def progress_line(state):
    elapsed = time.time() - state["started"]
    try:
        lines = Path(state["log"]).read_text(errors="replace").splitlines()
    except OSError:
        lines = []
    last = lines[-1].strip()[:100] if lines else ""
    return f"RENDER_PROGRESS {mmss(elapsed)} elapsed, log {len(lines)} lines: {last}"


def wait(state, window=WAIT, poll=2.0, every=PROGRESS_EVERY, out=print):
    """Wait for the render's exit code for at most `window` seconds; None if still running."""
    t0 = next_line = time.time()
    next_line += every
    while True:
        code = read_exit_code(state)
        if code is not None:
            return code
        if not alive(state["pid"]):
            time.sleep(poll)                 # the exit code is written just after the exit
            code = read_exit_code(state)
            return -2 if code is None else code
        now = time.time()
        if now - state["started"] > MAX_HOURS * 3600:
            try:
                os.killpg(state["pid"], signal.SIGTERM)
            except OSError:
                pass
            return -3
        if now >= next_line:
            out(progress_line(state), flush=True)
            next_line += every
        if now - t0 >= window:
            return None
        time.sleep(poll)


EXIT_NOTES = {-1: "exit code file unreadable", -2: "render process ended without an exit code",
              -3: f"render still running after {MAX_HOURS} h: stopped"}


def run(cmd, output, work_dir, audio_dir, expected=None, window=WAIT, out=print, **wait_kw):
    """Start (or re-attach to) the render and report. Returns 0 OK, 1 FAILED, 3 RUNNING."""
    state = load(work_dir)
    if state and not state.get("reported") and (read_exit_code(state) is not None
                                                or alive(state["pid"])):
        out(f"RENDER_ATTACH: waiting on the render started "
            f"{mmss(time.time() - state['started'])} ago (pid {state['pid']})", flush=True)
    else:
        state = start(cmd, output, work_dir, audio_dir, expected)
        out(f"RENDER_START: pid {state['pid']}, log {state['log']}", flush=True)
    code = wait(state, window=window, out=out, **wait_kw)
    if code is None:
        out(f"RENDER_RUNNING: still rendering after this {window:g} s window; "
            f"run the same command again to keep waiting.\n{progress_line(state)}", flush=True)
        return 3
    proc = _CHILDREN.pop(state["pid"], None)
    if proc is not None:                     # reap our child (it exits just after the code)
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            pass
    ok, text = verdict(state, code)
    if code in EXIT_NOTES:
        text = text.replace("\n", f" ({EXIT_NOTES[code]})\n", 1)
    state["reported"] = True
    state["result"] = "RENDER_OK" if ok else "RENDER_FAILED"
    save(work_dir, state)
    out(text, flush=True)
    return 0 if ok else 1


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m explainer.final_render",
                                     description="Final 1080p render of one episode, verified.")
    parser.add_argument("script", help="projects/<name>/<script>.py")
    parser.add_argument("--expected", type=float,
                        help="expected duration in seconds (default: the narration audio)")
    parser.add_argument("--wait", type=float, default=WAIT,
                        help=f"seconds this call waits before RENDER_RUNNING (default {WAIT})")
    args = parser.parse_args(argv)
    script = Path(args.script).resolve()
    if not script.is_file():
        print(f"RENDER_FAILED: script not found: {args.script}")
        return 1
    name = script.stem
    return run([sys.executable, str(script)], OUTPUT_DIR / f"{name}.mp4",
               BUILD_DIR / name / "final_render", BUILD_DIR / name / "audio",
               expected=args.expected, window=args.wait)


if __name__ == "__main__":
    sys.exit(main())
