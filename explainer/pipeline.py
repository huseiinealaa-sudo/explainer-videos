"""Production pipeline: project settings -> narration audio (+ word timings) -> render -> mp4.

    1. synthesize(NARRATION, audio_dir)        -> seg1.mp3 + seg1.json ... segN
    2. render(__file__, "SceneName", preview)  -> silent Manim video
    3. merge_audio_video(video, audio_dir, n, out_path)
build() runs all three; main() adds the --preview command-line switch.
"""
import argparse
import asyncio
import json
import ssl
import subprocess
import tomllib
from pathlib import Path

from .style import BUILD_DIR, FINAL_FPS, FINAL_RESOLUTION, OUTPUT_DIR
from .timing import segment_paths, timing_path

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
def render(script, scene, preview=False, media_dir=None):
    """Render a scene with Manim and return the path of the silent video.

    preview=True renders low quality (480p15) for a quick layout check.
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
                    str(script), scene], check=True)
    return media_dir / "videos" / script.stem / folder / f"{scene}.mp4"


def merge_audio_video(video, audio_dir, n, out_path):
    """Concatenate the narration segments and mux them onto the video."""
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
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(narration),
                    "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-af", "apad", "-shortest", "-movflags", "+faststart",
                    str(out_path)], check=True)
    return out_path


def audio_dir_for(script):
    """Build folder for a script's narration: tmp/<script>/audio."""
    return BUILD_DIR / Path(script).stem / "audio"


def build(script, scene, narration, preview=False):
    """Full pipeline: narration audio -> render -> merged mp4.

    Voice and rate come from the project's project.toml (see project_settings).
    Final videos go to output/<script>.mp4; previews to tmp/<script>/preview.mp4.
    """
    name = Path(script).stem
    s = project_settings(script)
    audio_dir = audio_dir_for(script)
    synthesize(narration, audio_dir, voice=s["voice"], rate=s["rate"])
    video = render(script, scene, preview=preview)
    out = (BUILD_DIR / name / "preview.mp4") if preview else (OUTPUT_DIR / f"{name}.mp4")
    return merge_audio_video(video, audio_dir, len(narration), out)


def main(script, scene, narration):
    """Command line of a video script: `python <script> [--preview]`."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="low-quality layout check")
    args = parser.parse_args()
    print(build(script, scene, narration, preview=args.preview))
