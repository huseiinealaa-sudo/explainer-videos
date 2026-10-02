"""Narration timeline: segment lengths, word timings and SyncedScene.

A scene calls self.timeline(NARRATION, audio_dir) once, then places every animation
on the narration clock:
    self.sync(t)                 hold until absolute time t
    self.at(seg, frac)           a fraction of the way through segment seg (1-based)
    self.cue(seg, phrase)        the moment `phrase` is spoken in segment seg
    self.say(text) / clear()     bottom caption / fade everything out
cue() uses the edge-tts word timings saved next to the audio (seg{i}.json). Without
them (older audio) it falls back to the phrase's relative position in the text.

Every SyncedScene (old scripts included) also obeys two switches that the pipeline
passes as environment variables (see pipeline.render):
    EXPLAINER_WINDOW="t0,t1"     render only this part of the narration clock (segment
                                 previews): earlier animations run without frames
    EXPLAINER_QA=<json path>     QA mode: explainer.qa.overlap checks the screen after
                                 every animation and writes its raw findings there
    EXPLAINER_RENDER_LOG=<path>  where the scene records the clock time of its first frame
"""
import json
import os
import re
import subprocess
import unicodedata
from pathlib import Path

from contextlib import contextmanager

from manim import DOWN, UP, FadeIn, FadeOut, ManimColor, Scene, VMobject, Wait, logger
from manim.constants import DEFAULT_WAIT_TIME
from manim.utils.exceptions import EndSceneEarlyException

from . import theme as _theme
from .backgrounds import Background, make_background, theme_background
from .style import BG, CAPTION_Y, FS_LABEL, INK, fit, label

WINDOW_ENV, QA_ENV, RENDER_LOG_ENV = "EXPLAINER_WINDOW", "EXPLAINER_QA", "EXPLAINER_RENDER_LOG"


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


def _is_word_char(c):
    """A letter, a digit or a combining mark (Arabic diacritics are marks: 'الدَّفْعُ')."""
    return c.isalnum() or unicodedata.category(c).startswith("M")


def find_phrase(text, phrase, nth=1):
    """Index of the nth occurrence of `phrase` in `text`, whole words first.

    An occurrence is a whole word when no letter, digit or diacritic touches it on either
    side, so «الدفع» does not match inside «والدفع» while a lone «الدفع» exists later in the
    text. Only if the text has fewer than nth whole-word occurrences does the nth partial
    occurrence count. Returns -1 when the phrase is not there at all."""
    def hits(whole):
        i = text.find(phrase)
        while i >= 0:
            end = i + len(phrase)
            before = i > 0 and _is_word_char(text[i - 1]) and _is_word_char(phrase[0])
            after = end < len(text) and _is_word_char(text[end]) and _is_word_char(phrase[-1])
            if not whole or not (before or after):
                yield i
            i = text.find(phrase, i + 1)
    for whole in (True, False):
        found = list(hits(whole))
        if len(found) >= nth:
            return found[nth - 1]
    return -1


# ---------------- Scene ----------------
class SyncedScene(Scene):
    """Scene that places animations on the narration timeline."""

    window = None           # (t0, t1) on the narration clock, from EXPLAINER_WINDOW
    first_frame = None      # clock time of the first rendered frame
    qa = None               # explainer.qa.overlap.OverlapChecker in QA mode
    bg = None               # the Background on screen (None: the camera colour alone)
    zoomed = False          # True while motion.zoom_on has the content magnified (QA)

    # ---------- render window and QA mode (set by the pipeline) ----------
    def setup(self):
        super().setup()
        if os.environ.get(WINDOW_ENV):
            self.window = tuple(float(x) for x in os.environ[WINDOW_ENV].split(","))
        if os.environ.get(QA_ENV):
            from .qa.overlap import OverlapChecker
            self.qa = OverlapChecker()
        self.bg = None
        self.background()                           # the theme's own, plus the project's motion

    def play(self, *args, **kwargs):
        r = self.renderer
        if self.window is not None:
            t0, t1 = self.window
            if r.time >= t1 - 1e-3:                 # past the window: stop rendering
                raise EndSceneEarlyException()
            if self.first_frame is None:
                anims = self.compile_animations(
                    *args, **{k: v for k, v in kwargs.items() if not k.startswith("subcaption")})
                if r.time + self.get_run_time(anims) <= t0 + 1e-3:
                    self._play_without_frames(*args, **kwargs)
                    return
        if self.first_frame is None:
            self.first_frame = r.time
        self._pin_background()
        super().play(*args, **kwargs)
        if self.qa is not None and not (len(args) == 1 and isinstance(args[0], Wait)):
            self.qa.check(self, r.time)             # after every animation (pauses change nothing)

    def _play_without_frames(self, *args, **kwargs):
        """Run an animation before the window: its end state and clock time, no frames."""
        r = self.renderer
        keep = r._original_skipping_status
        r._original_skipping_status = True
        try:
            super().play(*args, **kwargs)
        finally:
            r._original_skipping_status = keep

    def wait(self, duration=DEFAULT_WAIT_TIME, stop_condition=None, frozen_frame=None):
        if self.window is not None:
            t, (t0, t1) = self.renderer.time, self.window
            if self.first_frame is None and t < t0 - 1e-3 and t + duration > t0 + 1e-3:
                super().wait(t0 - t, frozen_frame=frozen_frame)    # split the pause at t0
                duration -= t0 - t
            t = self.renderer.time
            if t < t1 < t + duration:
                duration = t1 - t
            if duration <= 1e-3:
                return
        super().wait(duration, stop_condition=stop_condition, frozen_frame=frozen_frame)

    def tear_down(self):
        super().tear_down()
        if os.environ.get(RENDER_LOG_ENV):
            Path(os.environ[RENDER_LOG_ENV]).write_text(json.dumps(
                {"first_frame": self.first_frame, "last_time": self.renderer.time,
                 "window": self.window}))
        if self.qa is not None:
            self.qa.write(os.environ[QA_ENV])

    # ---------- narration clock ----------
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
        elif rem < -0.05:       # the animations ran past the narration: tighten them
            logger.warning(f"SyncedScene.sync: {-rem:.2f} s late for t = {t:.2f} s")

    def start(self, seg):
        return self.START[seg - 1]

    def end(self, seg):
        return self.START[seg]

    def at(self, seg, frac):
        """Time a fraction `frac` of the way through segment seg (1-based)."""
        return self.START[seg - 1] + frac * (self.START[seg] - self.START[seg - 1])

    def cue(self, seg, phrase, nth=1):
        """Time at which `phrase` (its nth occurrence) starts in segment seg.

        Whole words match before partial ones (find_phrase). Uses the word timings when
        present, else the relative text position.
        """
        text = self.narration[seg - 1]
        i = find_phrase(text, phrase, nth)
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
        if not hasattr(self, "caption"):            # say() works without timeline()
            self.caption = VMobject()
        if self.caption.has_points() or len(self.caption.submobjects):
            self.play(FadeOut(self.caption), run_time=0.25)
        self.play(FadeIn(new, shift=UP * 0.08), run_time=0.4)
        self.caption = new
        return new

    def clear(self, *keep, run_time=0.6):
        """Fade out everything on screen except `keep` (and the background)."""
        gone = [m for m in self.mobjects if m not in keep and not _is_background(m)]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=run_time)
        self.caption = VMobject()


    # ---------- background and theme ----------
    def background(self, run_time=0.0, motion=None, **spec):
        """Set the scene's background (explainer/backgrounds.py, make_background): a colour,
        a gradient or an image, with optional slow motion. Without arguments it is the
        theme's own, plus the motion the project asks for (`[style] background`). run_time > 0
        crossfades from the previous one. Returns the Background (None for a plain colour).

        Layers sit at the back of scene.mobjects and carry updaters, so they move in waits too.
        """
        if motion is None:
            motion = _theme.project_motion()
        new = make_background(motion=motion, **spec) if spec else \
            theme_background(motion=motion)
        self._swap_background(new, run_time)
        return new

    def _camera_colour(self, colour):
        self.camera.background_color = ManimColor(colour)
        self.camera.init_background()

    def _swap_background(self, new, run_time):
        old = self.bg
        self.bg = new
        self._camera_colour(BG)             # a plain colour is the camera's own
        if run_time > 0:
            if new is None:
                new = make_background(color=BG)         # a plate to fade in over the old one
            self.bg = new
            self.play(FadeIn(new), *([FadeOut(old)] if old is not None else []),
                      run_time=run_time)
        elif new is not None:
            self.add(new)
            if old is not None:
                self.remove(old)
        elif old is not None:
            self.remove(old)
        self._pin_background()

    def _pin_background(self):
        """Keep the background first in scene.mobjects (behind everything)."""
        if self.bg is not None and (not self.mobjects or self.mobjects[0] is not self.bg):
            if self.bg in self.mobjects:
                self.mobjects.remove(self.bg)
            self.mobjects.insert(0, self.bg)

    def background_color_at(self, x, y):
        """RGB (0..1) of the surface behind a point of the screen: the QA contrast rule."""
        if self.bg is not None:
            return self.bg.color_at(x, y)
        return _theme._rgb(BG)

    def set_theme(self, name, run_time=1.0, keep=()):
        """Switch the colours of the video to theme `name` from this point on: the screen is
        cleared (except `keep`, which keeps its old colours), the colour tokens (INK, BG,
        ACCENT_1 ...) take the new theme's values and the background crossfades. Everything
        drawn afterwards uses the new theme; reset_theme() or themed() brings the project's
        theme back."""
        if name == _theme.current_theme():
            return
        self.clear(*keep, run_time=run_time / 2 if run_time else 0)
        _theme.set_theme(name)
        new = theme_background(motion=_theme.project_motion())
        self._swap_background(new, run_time / 2)

    def reset_theme(self, run_time=1.0):
        """Back to the project's theme (project.toml)."""
        self.set_theme(_theme.project_theme(), run_time)

    @contextmanager
    def themed(self, name, run_time=1.0):
        """`with self.themed("blueprint"):` the scenes inside use that theme; the project's
        comes back after."""
        before = _theme.current_theme()
        self.set_theme(name, run_time)
        try:
            yield
        finally:
            self.set_theme(before, run_time)


def _is_background(m):
    return isinstance(m, Background) or getattr(m, "is_background", False)
