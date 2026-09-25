"""Narration timeline: segment lengths, word timings and SyncedScene.

A scene calls self.timeline(NARRATION, audio_dir) once, then places every animation
on the narration clock:
    self.sync(t)                 hold until absolute time t
    self.at(seg, frac)           a fraction of the way through segment seg (1-based)
    self.cue(seg, phrase)        the moment `phrase` is spoken in segment seg
    self.say(text) / clear()     bottom caption / fade everything out
cue() uses the edge-tts word timings saved next to the audio (seg{i}.json). Without
them (older audio) it falls back to the phrase's relative position in the text.
"""
import json
import re
import subprocess
from pathlib import Path

from manim import DOWN, UP, FadeIn, FadeOut, Scene, VMobject

from .style import CAPTION_Y, FS_LABEL, INK, fit, label


# ---------------- Audio segments ----------------
def media_duration(path):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)])
    return float(out)


def segment_paths(audio_dir, n):
    return [Path(audio_dir) / f"seg{i}.mp3" for i in range(1, n + 1)]


def timing_path(audio_dir, i):
    return Path(audio_dir) / f"seg{i}.json"


def segment_starts(audio_dir, n):
    """Start time of each segment, plus the total length as the last entry."""
    starts = [0.0]
    for p in segment_paths(audio_dir, n):
        starts.append(starts[-1] + media_duration(p))
    return starts


# ---------------- Word timings ----------------
_PUNCT = re.compile(r"[^\w؀-ۿ]+")


def align_words(text, words):
    """Character position in `text` of each timed word (None if it cannot be found).

    Words are matched in order from a moving cursor; a word the voice normalised
    (punctuation, quotes) is retried with the punctuation stripped.
    """
    pos, cursor = [], 0
    for w in words:
        j = text.find(w["text"], cursor)
        if j < 0:
            core = _PUNCT.sub("", w["text"])
            j = text.find(core, cursor) if core else -1
            n = len(core)
        else:
            n = len(w["text"])
        if j < 0 or j - cursor > 40:          # lost: do not jump far ahead
            pos.append(None)
            continue
        pos.append(j)
        cursor = j + n
    return pos


def load_word_timings(audio_dir, i, text):
    """[(char_pos, start_s), ...] for segment i, or None if absent or stale."""
    path = timing_path(audio_dir, i)
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    if data.get("text") != text or not data.get("words"):
        return None
    pos = align_words(text, data["words"])
    marks = [(p, w["start"]) for p, w in zip(pos, data["words"]) if p is not None]
    return marks or None


def word_coverage(audio_dir, narration):
    """Fraction of timed words aligned to the text, per segment (a quick health check)."""
    out = []
    for i, text in enumerate(narration, 1):
        path = timing_path(audio_dir, i)
        if not path.exists():
            out.append(None)
            continue
        words = json.loads(path.read_text())["words"]
        pos = align_words(text, words)
        out.append(sum(p is not None for p in pos) / max(len(pos), 1))
    return out


# ---------------- Scene ----------------
class SyncedScene(Scene):
    """Scene that places animations on the narration timeline."""

    def timeline(self, narration, audio_dir):
        """Load segment starts and word timings; returns START (N + 1 entries)."""
        self.narration = list(narration)
        self.audio_dir = Path(audio_dir)
        self.START = segment_starts(audio_dir, len(self.narration))
        self.words = [load_word_timings(audio_dir, i, t)
                      for i, t in enumerate(self.narration, 1)]
        self.caption = VMobject()
        return self.START

    def sync(self, t):
        """Hold until absolute time t on the narration timeline."""
        rem = t - self.renderer.time
        if rem > 1e-3:
            self.wait(rem)

    def start(self, seg):
        return self.START[seg - 1]

    def end(self, seg):
        return self.START[seg]

    def at(self, seg, frac):
        """Time a fraction `frac` of the way through segment seg (1-based)."""
        return self.START[seg - 1] + frac * (self.START[seg] - self.START[seg - 1])

    def cue(self, seg, phrase, nth=1):
        """Time at which `phrase` (its nth occurrence) starts in segment seg.

        Uses the word timings when present, else the relative text position.
        """
        text = self.narration[seg - 1]
        i = -1
        for _ in range(nth):
            i = text.find(phrase, i + 1)
            assert i >= 0, (seg, phrase)
        marks = self.words[seg - 1]
        if marks:
            # the timed word that contains position i, else the next one
            before = [(p, s) for p, s in marks if p <= i]
            if before and not any(c.isspace() for c in text[before[-1][0]:i]):
                return self.START[seg - 1] + before[-1][1]
            after = [s for p, s in marks if p > i]
            if after:
                return self.START[seg - 1] + after[0]
        return self.at(seg, i / len(text))

    def say(self, text, color=INK, y=CAPTION_Y, size=FS_LABEL):
        """Replace the bottom caption line."""
        new = fit(label(text, size, color)).move_to([0, y, 0])
        if self.caption.has_points() or len(self.caption.submobjects):
            self.play(FadeOut(self.caption), run_time=0.25)
        self.play(FadeIn(new, shift=UP * 0.08), run_time=0.4)
        self.caption = new
        return new

    def clear(self, *keep, run_time=0.6):
        """Fade out everything on screen except `keep`."""
        gone = [m for m in self.mobjects if m not in keep]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=run_time)
        self.caption = VMobject()
