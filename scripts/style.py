"""Shared whiteboard style and production helpers for explainer videos.

Import from every video script:

    from style import *

Pipeline (see scripts/ut_intro.py for a complete example):
    1. synthesize(NARRATION, audio_dir)        -> seg1.mp3 ... segN.mp3
    2. render(__file__, "SceneName", preview)  -> silent Manim video
    3. merge_audio_video(video, audio_dir, n, out_path)
Inside the scene, segment_starts(audio_dir, n) + SyncedScene.sync() keep
each scene exactly as long as its narration segment.
"""
import asyncio
import ssl
import subprocess
from pathlib import Path

from manim import *

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"
BUILD_DIR = ROOT / "tmp"            # git-ignored: audio, media cache, previews

# ---------------- Colors ----------------
BG = WHITE
INK = BLACK
GREY_INK = "#555555"                # secondary strokes, notes, ray traces

# ---------------- Fonts & text sizes ----------------
FONT = "DejaVu Sans"
FS_TITLE = 64                       # opening title
FS_HEADING = 44                     # summary heading
FS_EQUATION = 40
FS_SUBTITLE = 38
FS_BODY = 36                        # bullets, corner title, panel titles
FS_SUMMARY = 34                     # summary lines
FS_SYMBOL = 30                      # single italic symbols (t, d)
FS_LABEL = 28                       # diagram labels
FS_NOTE = 26                        # material names, secondary labels
FS_AXIS = 24                        # axis labels, side notes
FS_TAG = 22                         # peak tags, small annotations

# ---------------- Render settings ----------------
FINAL_RESOLUTION = (1920, 1080)
FINAL_FPS = 30

config.background_color = BG
Text.set_default(color=INK, font=FONT)
VMobject.set_default(color=INK)

# ---------------- Narration (edge-tts) ----------------
VOICE = "ar-SA-HamedNeural"
PROXY_CA_BUNDLE = "/root/.ccr/ca-bundle.crt"


def synthesize(segments, audio_dir, voice=VOICE, force=False):
    """Write each fully diacritized narration segment to audio_dir/seg{i}.mp3.

    Existing files are kept unless force=True, so re-renders reuse the
    approved audio. edge-tts hardcodes certifi, which fails behind the
    session proxy, so its SSL context is patched to the proxy CA bundle.
    """
    import edge_tts
    import edge_tts.communicate as communicate

    if Path(PROXY_CA_BUNDLE).exists():
        communicate._SSL_CTX = ssl.create_default_context(cafile=PROXY_CA_BUNDLE)

    audio_dir = Path(audio_dir)
    audio_dir.mkdir(parents=True, exist_ok=True)

    async def run():
        for i, text in enumerate(segments, 1):
            path = audio_dir / f"seg{i}.mp3"
            if force or not path.exists():
                await edge_tts.Communicate(text, voice).save(str(path))

    asyncio.run(run())


# ---------------- Timing ----------------
def media_duration(path):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)])
    return float(out)


def segment_paths(audio_dir, n):
    return [Path(audio_dir) / f"seg{i}.mp3" for i in range(1, n + 1)]


def segment_starts(audio_dir, n):
    """Start time of each segment, plus the total length as the last entry."""
    starts = [0.0]
    for p in segment_paths(audio_dir, n):
        starts.append(starts[-1] + media_duration(p))
    return starts


class SyncedScene(Scene):
    """Scene that can hold until an absolute time on the narration timeline."""

    def sync(self, t):
        rem = t - self.renderer.time
        if rem > 1e-3:
            self.wait(rem)


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


def build(script, scene, narration, preview=False):
    """Full pipeline: narration audio -> render -> merged mp4.

    Final videos go to output/<script>.mp4; previews to tmp/<script>/preview.mp4.
    """
    name = Path(script).stem
    audio_dir = BUILD_DIR / name / "audio"
    synthesize(narration, audio_dir)
    video = render(script, scene, preview=preview)
    out = (BUILD_DIR / name / "preview.mp4") if preview else (OUTPUT_DIR / f"{name}.mp4")
    return merge_audio_video(video, audio_dir, len(narration), out)
