"""Daniel Compact Prover: concatenate the 7 episodes into output/prover_full_series.mp4.

A 3-second title card ("Episode N — <title>", white background, black text, silent audio)
goes between each pair of episodes. The episodes are NOT re-rendered or re-encoded: the
cards are encoded with the same settings as style.merge_audio_video (H.264 High yuv420p
1080p30, AAC mono at the narration sample rate), then everything is joined with the
ffmpeg concat demuxer in stream-copy mode. The script stops before joining if any stream
parameter differs, so a re-encode never happens silently.

Build (from the repo root):
    python projects/prover/prover_full_series.py
"""
import json
import subprocess
import sys
from pathlib import Path

# Shared style.py lives in scripts/ until the explainer package replaces it.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from style import *  # noqa: E402

EPISODES = [
    ("prover_ep01_principle", "Proving Principle & the Meter Factor"),
    ("prover_ep02_passes", "Pass, Run & Repeatability"),
    ("prover_ep03_components", "Compact Prover Construction"),
    ("prover_ep04_cycle", "The Operating Cycle"),
    ("prover_ep05_chronometry", "Four Keys to Accuracy"),
    ("prover_ep06_floboss", "FloBoss S600+ in the Field"),
    ("prover_ep07_audit", "Auditing the Proving Report"),
]
CARD_SECONDS = 3.0
WORK_DIR = BUILD_DIR / "prover_full_series"
OUT = OUTPUT_DIR / "prover_full_series.mp4"
MAX_BYTES = 100 * 1024 * 1024


def make_card_scene(n, title):
    class Card(Scene):
        def construct(self):
            series = Text("Daniel Compact Prover", font_size=FS_SUBTITLE, color=GREY_INK)
            head = Text(f"Episode {n} — {title}", font_size=FS_HEADING + 4, weight=BOLD)
            if head.width > 13.0:
                head.scale_to_fit_width(13.0)
            line = Line(LEFT, RIGHT).set_width(head.width)
            VGroup(series, head, line).arrange(DOWN, buff=0.35)
            self.play(FadeIn(series), Write(head), Create(line), run_time=1.2)
            self.wait(CARD_SECONDS - 1.2 - 0.5)
            self.play(FadeOut(VGroup(series, head, line)), run_time=0.5)

    Card.__name__ = Card.__qualname__ = f"Card{n}"
    return Card


# Manim finds the scenes by name in this module.
for _n, (_stem, _title) in enumerate(EPISODES, start=1):
    if _n > 1:
        globals()[f"Card{_n}"] = make_card_scene(_n, _title)


def probe(path):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-show_data_hash",
         "sha256", "-of", "json", str(path)])
    return json.loads(out)


KEYS = {"video": ["codec_name", "profile", "level", "pix_fmt", "width", "height",
                  "r_frame_rate", "time_base", "extradata_hash"],
        "audio": ["codec_name", "profile", "sample_rate", "channels", "channel_layout",
                  "time_base", "extradata_hash"]}


def signature(path):
    sig = {}
    for s in probe(path)["streams"]:
        sig[s["codec_type"]] = {k: s.get(k) for k in KEYS[s["codec_type"]]}
    return sig


def encode_card(video, out, sample_rate):
    """Same x264 / AAC settings as style.merge_audio_video, with silent mono audio."""
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video),
                    "-f", "lavfi", "-i", f"anullsrc=r={sample_rate}:cl=mono",
                    "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-t", f"{CARD_SECONDS}", "-movflags", "+faststart", str(out)], check=True)


def main():
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    episodes = [OUTPUT_DIR / f"{stem}.mp4" for stem, _ in EPISODES]
    ref = signature(episodes[0])
    rate = ref["audio"]["sample_rate"]

    parts = []
    for n, path in enumerate(episodes, start=1):
        if n > 1:
            silent = render(__file__, f"Card{n}")
            card = WORK_DIR / f"card_{n:02d}.mp4"
            encode_card(silent, card, rate)
            parts.append(card)
        parts.append(path)

    bad = [(p.name, signature(p)) for p in parts if signature(p) != ref]
    if bad:
        for name, sig in bad:
            print("MISMATCH", name, sig, "\nREF", ref)
        raise SystemExit("Stream parameters differ: joining would need a re-encode. Stopped.")

    concat = WORK_DIR / "list.txt"
    concat.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(concat), "-c", "copy", "-movflags", "+faststart", str(OUT)],
                   check=True)

    size = OUT.stat().st_size
    total = media_duration(OUT)
    expected = sum(media_duration(p) for p in parts)
    print(f"{OUT}  {size / 1e6:.1f} MB  {total:.2f} s (parts sum {expected:.2f} s)")
    assert size < MAX_BYTES, f"{size} bytes >= 100 MB"
    assert abs(total - expected) < 1.0, (total, expected)
    return OUT


if __name__ == "__main__":
    main()
