"""Production pipeline: project settings -> narration audio (+ word timings) -> render -> mp4.

    1. synthesize(NARRATION, audio_dir)        -> seg1.mp3 + seg1.json ... segN
    2. render(__file__, "SceneName", preview)  -> silent Manim video
    3. merge_audio_video(video, audio_dir, n, out_path)
build() runs all three; main() adds the command-line switches:
    --preview          480p15 layout check -> tmp/<script>/preview.mp4
    --segments 2|2-3   only these narration segments (a preview) -> tmp/<script>/preview_seg02.mp4
    --qa               QA mode: overlap report + contact sheets in tmp/<script>/qa/<run>/
"""
import argparse
import asyncio
import json
import os
import ssl
import subprocess
import tomllib
from pathlib import Path

from .style import BUILD_DIR, FINAL_FPS, FINAL_RESOLUTION, OUTPUT_DIR
from .timing import (QA_ENV, RENDER_LOG_ENV, WINDOW_ENV, segment_paths, segment_starts,
                     timing_path)

PROXY_CA_BUNDLE = "/root/.ccr/ca-bundle.crt"

# ---------------- Project settings (projects/<name>/project.toml) ----------------
DEFAULT_VOICES = {"ar": "ar-SA-HamedNeural", "en": "en-US-GuyNeural"}
DEFAULT_PROJECT = {"language": "ar", "voice": DEFAULT_VOICES["ar"], "rate": "+0%"}
VOICE = DEFAULT_PROJECT["voice"]


def project_settings(script):
    """Language, voice and rate for the script's project.

    Reads project.toml next to the script ([narration] table, or top-level keys).
    Missing file or keys fall back to Arabic, ar-SA-HamedNeural, normal speed; a
    language without a voice gets that language's default voice.
    """
    path = Path(script).resolve().parent / "project.toml"
    data = tomllib.loads(path.read_text()) if path.exists() else {}
    data = data.get("narration", data)
    lang = data.get("language", DEFAULT_PROJECT["language"])
    return {"language": lang,
            "voice": data.get("voice", DEFAULT_VOICES.get(lang, DEFAULT_PROJECT["voice"])),
            "rate": data.get("rate", DEFAULT_PROJECT["rate"])}


# ---------------- Narration (edge-tts) ----------------
def synthesize(segments, audio_dir, voice=VOICE, force=False, rate="+0%"):
    """Write each narration segment to audio_dir/seg{i}.mp3, and its word timings
    (edge-tts WordBoundary events) to audio_dir/seg{i}.json.

    Existing segments are kept unless force=True, so re-renders reuse the approved
    audio; a segment whose timing file is missing is synthesized again so the audio
    and its timings always come from the same run. edge-tts hardcodes certifi, which
    fails behind the session proxy, so its SSL context is patched to the proxy CA bundle.
    """
    import edge_tts
    import edge_tts.communicate as communicate

    if Path(PROXY_CA_BUNDLE).exists():
        communicate._SSL_CTX = ssl.create_default_context(cafile=PROXY_CA_BUNDLE)

    audio_dir = Path(audio_dir)
    audio_dir.mkdir(parents=True, exist_ok=True)

    async def one(i, text):
        mp3, js = audio_dir / f"seg{i}.mp3", timing_path(audio_dir, i)
        if not force and mp3.exists() and js.exists():
            return
        com = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
        audio, words = bytearray(), []
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                audio += chunk["data"]
            elif chunk["type"] == "WordBoundary":
                start = chunk["offset"] / 1e7          # 100-ns ticks -> seconds
                words.append({"text": chunk["text"], "start": round(start, 4),
                              "end": round(start + chunk["duration"] / 1e7, 4)})
        mp3.write_bytes(audio)
        js.write_text(json.dumps({"voice": voice, "rate": rate, "text": text,
                                  "words": words}, ensure_ascii=False, indent=1))

    async def run():
        for i, text in enumerate(segments, 1):
            await one(i, text)

    asyncio.run(run())


# ---------------- Render & merge ----------------
def render(script, scene, preview=False, media_dir=None, env=None):
    """Render a scene with Manim and return the path of the silent video.

    preview=True renders low quality (480p15) for a quick layout check. env adds
    environment variables for the scene (render window, QA mode: see timing.py).
    """
    script = Path(script)
    media_dir = Path(media_dir or BUILD_DIR / script.stem / "media")
    if preview:
        args, folder = ["-ql"], "480p15"
    else:
        w, h = FINAL_RESOLUTION
        args = ["-r", f"{w},{h}", "--fps", str(FINAL_FPS)]
        folder = f"{h}p{FINAL_FPS}"
    subprocess.run(["manim", *args, "--disable_caching", "--media_dir", str(media_dir),
                    str(script), scene], check=True, env={**os.environ, **(env or {})})
    return media_dir / "videos" / script.stem / folder / f"{scene}.mp4"


def merge_audio_video(video, audio_dir, n, out_path, offset=0.0):
    """Concatenate the narration segments and mux them onto the video.

    offset: narration time of the video's first frame (segment previews start later).
    """
    audio_dir = Path(audio_dir)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    concat_list = audio_dir / "list.txt"
    concat_list.write_text("".join(f"file '{p.resolve()}'\n"
                                   for p in segment_paths(audio_dir, n)))
    narration = audio_dir / "narration.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(concat_list), "-c:a", "pcm_s16le", str(narration)],
                   check=True)
    seek = ["-ss", f"{offset:.3f}"] if offset > 0 else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), *seek, "-i", str(narration),
                    "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-af", "apad", "-shortest", "-movflags", "+faststart",
                    str(out_path)], check=True)
    return out_path


def audio_dir_for(script):
    """Build folder for a script's narration: tmp/<script>/audio."""
    return BUILD_DIR / Path(script).stem / "audio"


def parse_segments(spec, n):
    """'2' or '2-3' (1-based, inclusive) -> (first, last), checked against n segments."""
    a, _, b = str(spec).partition("-")
    first, last = int(a), int(b or a)
    if not 1 <= first <= last <= n:
        raise ValueError(f"segments {spec!r} outside 1-{n}")
    return first, last


def build(script, scene, narration, preview=False, segments=None, qa=False):
    """Full pipeline: narration audio -> render -> merged mp4.

    Voice and rate come from the project's project.toml (see project_settings).
    Final videos go to output/<script>.mp4; previews to tmp/<script>/preview.mp4.
    segments ('2' or '2-3') renders only those narration segments, always as a preview:
    tmp/<script>/preview_seg02.mp4. qa=True adds QA mode: the overlap report per segment
    and the contact sheets go to tmp/<script>/qa/<run>/ (run = full | seg02 | seg02-03).
    """
    name = Path(script).stem
    s = project_settings(script)
    audio_dir = audio_dir_for(script)
    synthesize(narration, audio_dir, voice=s["voice"], rate=s["rate"])
    starts = segment_starts(audio_dir, len(narration))
    build_dir = BUILD_DIR / name
    build_dir.mkdir(parents=True, exist_ok=True)
    env, run = {RENDER_LOG_ENV: str(build_dir / "render.json")}, "full"
    wanted = range(1, len(narration) + 1)
    if segments:
        first, last = parse_segments(segments, len(narration))
        end = starts[last] if last < len(narration) else 1e9     # the last one runs to the end
        env[WINDOW_ENV] = f"{starts[first - 1]},{end}"
        run = f"seg{first:02d}" + (f"-{last:02d}" if last != first else "")
        wanted = range(first, last + 1)
        preview = True
    qa_dir = build_dir / "qa" / run
    if qa:
        qa_dir.mkdir(parents=True, exist_ok=True)
        env[QA_ENV] = str(qa_dir / "overlap_raw.json")
    log = build_dir / "render.json"
    log.unlink(missing_ok=True)
    video = render(script, scene, preview=preview, env=env)
    offset = (json.loads(log.read_text())["first_frame"] or 0.0) if log.exists() else 0.0
    if preview:
        out = build_dir / ("preview.mp4" if run == "full" else f"preview_{run}.mp4")
    else:
        out = OUTPUT_DIR / f"{name}.mp4"
    merge_audio_video(video, audio_dir, len(narration), out, offset=offset)
    if qa:
        from .qa import finish_qa
        finish_qa(out, qa_dir, starts, offset, wanted, script=name)
    return out


def main(script, scene, narration):
    """Command line of a video script: `python <script> [--preview] [--segments 2] [--qa]`."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="low-quality layout check")
    parser.add_argument("--segments", help="only these narration segments, e.g. 2 or 2-3 "
                                           "(a low-quality preview)")
    parser.add_argument("--qa", action="store_true",
                        help="QA mode: overlap report + contact sheets in tmp/<script>/qa/")
    args = parser.parse_args()
    print(build(script, scene, narration, preview=args.preview, segments=args.segments,
                qa=args.qa))
