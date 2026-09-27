"""Contact sheets: the frames of a preview laid out for review (the video critic reads them).

A frame every 3 s of the narration clock, plus one at the start and one at the end of
each segment (the fullest frame of its last 1.5 s, before the closing fade). Each frame
gets a transparent 6×6 grid, A1 (top-left) ... F6 (bottom-right) — the same cells as the
overlap report — and its time in the top-right corner; the frames are then joined 3×3
per sheet. Frames are also kept one by one, full size, for a closer look.
"""
import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from ..timing import media_duration

GRID, COLS = 6, "ABCDEF"


def _font(size, bold=False):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)
    except OSError:
        return ImageFont.load_default(size)


def clock(t):
    """Narration clock as m:ss.s (the overlap report uses the same clock, in seconds)."""
    return f"{int(t // 60)}:{t % 60:04.1f}"


def grab(video, t, path):
    """Frame of `video` at t seconds (video time) as a PNG."""
    Path(path).unlink(missing_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(t, 0):.3f}", "-i", str(video),
                    "-frames:v", "1", str(path)], check=True)
    if not Path(path).exists():
        raise RuntimeError(f"no frame at {t:.2f} s in {video}")
    return Image.open(path).convert("RGB")


def ink(img):
    """Share of non-white pixels: how full the frame is."""
    grey = img.convert("L").resize((160, 90))
    return sum(v < 200 for v in grey.getdata()) / (160 * 90)


def annotate(img, label):
    """Draw the 6×6 grid with its cell names and the time label on a frame."""
    img = img.convert("RGBA")
    w, h = img.size
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    small = _font(max(10, h // 42))
    for i in range(1, GRID):
        d.line([(round(i * w / GRID), 0), (round(i * w / GRID), h)], fill=(0, 110, 255, 80))
        d.line([(0, round(i * h / GRID)), (w, round(i * h / GRID))], fill=(0, 110, 255, 80))
    for r in range(GRID):
        for c in range(GRID):
            d.text((c * w / GRID + 3, r * h / GRID + 2), f"{COLS[c]}{r + 1}", font=small,
                   fill=(0, 90, 220, 150))
    big = _font(max(12, h // 30), bold=True)
    x0, y0, x1, y1 = d.textbbox((0, 0), label, font=big)
    tw, th = x1 - x0, y1 - y0
    d.rectangle([w - tw - 14, 2, w - 3, th + 12], fill=(255, 255, 255, 225),
                outline=(0, 0, 0, 140))
    d.text((w - tw - 8 - x0, 6 - y0), label, font=big, fill=(0, 0, 0, 255))
    return Image.alpha_composite(img, layer).convert("RGB")


def plan(offset, duration, segments, every=3.0, fps=15):
    """Frames to take, [(clock time, tag, segment), ...]: every `every` s of the clock,
    the start of each segment (+1 s, once its first element is drawn) and its end."""
    t0, t1, dt = offset, offset + duration, 1.0 / fps
    marks = []
    for seg, s, e in segments:
        if t0 - 1e-6 <= s < t1 - dt:
            marks.append((min(s + 1.0, e - dt, t1 - dt), f"start of seg {seg}", seg))
        if t0 < e and e - dt <= t1 + 1e-6:
            marks.append((None, f"end of seg {seg}", (seg, max(s, t0), min(e, t1))))
    k = math.ceil((t0 - 1e-6) / every)
    while k * every < t1 - dt:
        t = k * every
        seg = next((sg for sg, s, e in segments if s <= t < e), None)
        marks.append((t, "", seg))
        k += 1
    return marks


def contact_sheets(video, out_dir, offset=0.0, segments=(), every=3.0, cols=3, rows=3,
                   title="", fps=15):
    """Write frames/ and sheets/ under out_dir; return the index (also saved as index.json).

    offset: narration time of the video's first frame; segments: [(k, start, end), ...]
    on the narration clock.
    """
    video, out_dir = Path(video), Path(out_dir)
    fdir, sdir = out_dir / "frames", out_dir / "sheets"
    for d in (fdir, sdir):
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob("*.png"):
            old.unlink()
    duration = media_duration(video)
    frames = []
    for t, tag, seg in plan(offset, duration, segments, every, fps):
        if t is None:                       # end of a segment: the fullest frame of its end
            k, s, e = seg
            tries = sorted({max(s, e - x) for x in (1.5, 1.2, 0.9, 0.6, 0.3, 1.0 / fps)})
            shots = [(ink(grab(video, c - offset, fdir / "_probe.png")), c) for c in tries]
            t, seg = max(shots)[1], k
        path = fdir / f"f{len(frames):03d}.png"
        img = grab(video, t - offset, path)
        label = clock(t) + (f"  seg {seg}" if seg else "") + (f"  {tag.split(' of')[0]}"
                                                               if tag else "")
        annotate(img, label).save(path)
        frames.append({"clock": round(t, 2), "video_time": round(t - offset, 2),
                       "segment": seg, "tag": tag, "file": str(path)})
    (fdir / "_probe.png").unlink(missing_ok=True)
    frames.sort(key=lambda f: f["clock"])
    for i, f in enumerate(frames):                   # name them in time order
        new = fdir / f"t{f['clock']:07.2f}_{i:03d}.png"
        Path(f["file"]).rename(new)
        f["file"] = str(new)
    per = cols * rows
    sheets = []
    for n, i in enumerate(range(0, len(frames), per), 1):
        chunk = frames[i:i + per]
        imgs = [Image.open(f["file"]) for f in chunk]
        w, h = imgs[0].size
        used = math.ceil(len(chunk) / cols)
        gap, head = 8, max(36, h // 12)
        sheet = Image.new("RGB", (cols * w + (cols + 1) * gap, head + used * h + (used + 1) * gap),
                          (228, 228, 228))
        d = ImageDraw.Draw(sheet)
        total = math.ceil(len(frames) / per)
        d.text((gap, gap), f"{title}   sheet {n}/{total}   {clock(chunk[0]['clock'])} – "
                           f"{clock(chunk[-1]['clock'])}   (grid A1 top-left … F6 bottom-right)",
               font=_font(max(14, head // 2), bold=True), fill=(0, 0, 0))
        for j, (img, f) in enumerate(zip(imgs, chunk)):
            r, c = divmod(j, cols)
            sheet.paste(img, (gap + c * (w + gap), head + gap + r * (h + gap)))
            f["sheet"], f["position"] = n, j + 1
        path = sdir / f"sheet_{n:02d}.png"
        sheet.save(path, optimize=True)
        sheets.append(str(path))
    index = {"video": str(video), "clock_offset": round(offset, 3), "every": every,
             "grid": "6x6: columns A-F left to right, rows 1-6 top to bottom",
             "sheets": sheets, "frames": frames}
    (out_dir / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1))
    return index
