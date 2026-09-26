"""Join finished episodes into one series file, with a short title card between them.

    concat_series([("output/x_ep01.mp4", "Title 1"), ("output/x_ep02.mp4", "Title 2")],
                  "output/x_full_series.mp4", series_title="My Series")

The episodes are NOT re-rendered or re-encoded: each card is rendered with Manim and
encoded with the same settings as pipeline.merge_audio_video (H.264 yuv420p, AAC at the
episodes' sample rate and channel count, silent), then everything is joined with the
ffmpeg concat demuxer in stream-copy mode. It stops before joining if any stream
parameter differs, so a re-encode never happens silently.
"""
import json
import subprocess
from pathlib import Path

from manim import (BOLD, DOWN, LEFT, RIGHT, Create, FadeIn, FadeOut, Line, Scene, Text,
                   VGroup, Write, tempconfig)

from .style import BUILD_DIR, FS_HEADING, FS_SUBTITLE, GREY_INK
from .timing import media_duration

MAX_BYTES = 100 * 1024 * 1024       # GitHub file limit

KEYS = {"video": ["codec_name", "profile", "level", "pix_fmt", "width", "height",
                  "r_frame_rate", "time_base", "extradata_hash"],
        "audio": ["codec_name", "profile", "sample_rate", "channels", "channel_layout",
                  "time_base", "extradata_hash"]}


def probe(path):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-show_data_hash",
         "sha256", "-of", "json", str(path)])
    return json.loads(out)


def signature(path):
    sig = {}
    for s in probe(path)["streams"]:
        sig[s["codec_type"]] = {k: s.get(k) for k in KEYS[s["codec_type"]]}
    return sig


def card_scene(n, title, series_title, seconds, label="Episode"):
    """Title card: series name, 'Episode N — title' and a rule, `seconds` long."""
    class Card(Scene):
        def construct(self):
            parts = []
            if series_title:
                parts.append(Text(series_title, font_size=FS_SUBTITLE, color=GREY_INK))
            head = Text(f"{label} {n} — {title}", font_size=FS_HEADING + 4, weight=BOLD)
            if head.width > 13.0:
                head.scale_to_fit_width(13.0)
            line = Line(LEFT, RIGHT).set_width(head.width)
            group = VGroup(*parts, head, line).arrange(DOWN, buff=0.35)
            self.play(*[FadeIn(p) for p in parts], Write(head), Create(line), run_time=1.2)
            self.wait(seconds - 1.2 - 0.5)
            self.play(FadeOut(group), run_time=0.5)

    Card.__name__ = Card.__qualname__ = f"Card{n}"
    return Card


def render_card(scene_cls, width, height, fps, media_dir):
    with tempconfig({"pixel_width": width, "pixel_height": height, "frame_rate": fps,
                     "media_dir": str(media_dir), "disable_caching": True,
                     "output_file": scene_cls.__name__, "verbosity": "WARNING"}):
        scene = scene_cls()
        scene.render()
        return Path(scene.renderer.file_writer.movie_file_path)


def encode_card(video, out, seconds, sample_rate, channels):
    """Same x264 / AAC settings as pipeline.merge_audio_video, with silent audio."""
    layout = "mono" if int(channels) == 1 else "stereo"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video),
                    "-f", "lavfi", "-i", f"anullsrc=r={sample_rate}:cl={layout}",
                    "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-t", f"{seconds}", "-movflags", "+faststart", str(out)], check=True)


def concat_series(episodes, out, series_title=None, card_seconds=3.0, work_dir=None,
                  label="Episode", first_card=False):
    """Join `episodes` [(path, title), ...] into `out` with title cards between them.

    first_card=True also puts a card before episode 1. Returns the output path.
    """
    out = Path(out)
    work_dir = Path(work_dir or BUILD_DIR / out.stem)
    work_dir.mkdir(parents=True, exist_ok=True)
    paths = [Path(p) for p, _ in episodes]
    ref = signature(paths[0])
    v, a = ref["video"], ref["audio"]
    num, den = map(int, v["r_frame_rate"].split("/"))

    parts = []
    for n, (path, (_, title)) in enumerate(zip(paths, episodes), start=1):
        if n > 1 or first_card:
            cls = card_scene(n, title, series_title, card_seconds, label)
            silent = render_card(cls, v["width"], v["height"], num / den, work_dir / "media")
            card = work_dir / f"card_{n:02d}.mp4"
            encode_card(silent, card, card_seconds, a["sample_rate"], a["channels"])
            parts.append(card)
        parts.append(path)

    bad = [(p.name, signature(p)) for p in parts if signature(p) != ref]
    if bad:
        for name, sig in bad:
            print("MISMATCH", name, sig, "\nREF", ref)
        raise SystemExit("Stream parameters differ: joining would need a re-encode. Stopped.")

    concat = work_dir / "list.txt"
    concat.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(concat), "-c", "copy", "-movflags", "+faststart", str(out)],
                   check=True)

    size = out.stat().st_size
    total = media_duration(out)
    expected = sum(media_duration(p) for p in parts)
    print(f"{out}  {size / 1e6:.1f} MB  {total:.2f} s (parts sum {expected:.2f} s)")
    assert size < MAX_BYTES, f"{size} bytes >= 100 MB"
    assert abs(total - expected) < 1.0, (total, expected)
    return out
