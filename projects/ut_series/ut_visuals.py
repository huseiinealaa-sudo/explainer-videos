"""ut_series: shared drawing primitives for the ultrasonic-testing episodes.

    from ut_visuals import wavefront, Probe, SteelBlock, AScan, tag_line

`wavefront` is the one way every episode draws an ultrasonic pulse travelling through a part:
a few arcs, like the Wi-Fi icon. They are the wave fronts of the pulse: convex in the direction
of travel, growing wider toward the front, the front arc strongest and the ones behind it
fainter. The first version of this shape is `wavefront()` of projects/ut_intro/ut_intro.py
(three same-size arcs); here the arcs are concentric so the front is the widest, the colours are
theme colours (never literals), and the group keeps its fade pattern when a scene fades it with
`set_stroke(opacity=...)`.

Colour roles of the series (project CLAUDE.md): ACCENT_1 the pulse going in, ACCENT_2 the echo
coming back, ACCENT_3 the transmitted pulse.
"""
from manim import *

from explainer import *    # noqa: F401,F403  (theme colours, label, fonts, icon, badge, fit)
from explainer import ACCENT_1


class Wavefront(VGroup):
    """Arcs of one pulse; `fades` is the opacity of each arc from the back to the front.
    set_stroke(opacity=x) / set_opacity(x) scale those fades by x (a plain VGroup would flatten
    them to x), so a scene can fade a travelling pulse in and out without losing its shape."""

    fades = (0.28, 0.55, 1.0)

    def set_stroke(self, color=None, width=None, opacity=None, background=None, family=True):
        # the group's own colour data first (VMobject.__init__ and Transform need it), then the arcs
        super().set_stroke(color=color, width=width, opacity=opacity, background=background,
                           family=False)
        for arc, f in zip(self.submobjects, self.fades):
            arc.set_stroke(color=color, width=width,
                           opacity=None if opacity is None else opacity * f,
                           background=background, family=family)
        return self

    def set_opacity(self, opacity, family=True):
        return self.set_stroke(opacity=opacity, family=family)


def wavefront(length=0.9, amp=0.28, cycles=None, color=ACCENT_1, direction=DOWN,
              stroke_width=4, n=3, spread=0.85):
    """A pulse as `n` wave-front arcs, centred on ORIGIN and moving along `direction`
    (DOWN from a probe, UP for the echo, RIGHT / LEFT sideways).

    amp     half the width of the front arc is 1.8 x amp (the sideways size of the beam)
    length  how far back the pulse reaches: the arcs are spaced at about 0.55 x length / (n - 1)
    spread  half the angle of every arc, in radians; the arcs share one centre, so the front
            one (the largest) is the widest and the ones behind it are narrower
    cycles  accepted and ignored (the signature matches the sine packet this replaces)

    Shrinking it sideways (`.stretch(k, 0)` for a vertical pulse) or lowering its opacity with
    `.set_stroke(opacity=...)` weakens it, as for attenuation.
    """
    r_front = 1.8 * amp / np.sin(spread)
    gap = min(0.55 * length / (n - 1), 0.35 * r_front)
    arcs = []
    for k in range(n):                                   # k = 0 is the rear arc
        radius = r_front - (n - 1 - k) * gap
        arcs.append(Arc(radius=radius, start_angle=-PI / 2 - spread, angle=2 * spread,
                        stroke_width=stroke_width, color=color))
    g = Wavefront(*arcs)
    g.fades = Wavefront.fades if n == 3 else tuple(np.linspace(0.28, 1.0, n))
    g.set_stroke(opacity=1)
    g.move_to(ORIGIN)
    return g.rotate(angle_of_vector(direction) - angle_of_vector(DOWN), about_point=ORIGIN)


# ---------------- Shared by episodes 2-4 (the same shapes episode 1 builds inside its script) ----------------
class SteelBlock(VGroup):
    """A steel part seen in section: a filled rectangle. `body` is the rectangle."""

    def __init__(self, width=7.0, height=3.0):
        body = Rectangle(width=width, height=height, color=INK, stroke_width=4)
        body.set_fill(PANEL_FILL, 1)
        super().__init__(body)
        self.body = body


class Probe(VGroup):
    """An ultrasonic probe: housing, crystal (the face) and a cable stub. Its face is the
    bottom edge (the top edge when flip=True). `face_point()` is the centre of the face."""

    def __init__(self, width=0.9, height=0.6, color=ACCENT_1, flip=False):
        housing = RoundedRectangle(width=width, height=height, corner_radius=0.08,
                                   color=color, stroke_width=4).set_fill(BG, 1)
        crystal = Rectangle(width=width * 0.85, height=0.12, color=color, stroke_width=3)
        crystal.set_fill(color, 1).next_to(housing, DOWN, buff=0)
        cable = Line(housing.get_top(), housing.get_top() + UP * 0.35, color=GREY_INK,
                     stroke_width=5)
        super().__init__(cable, housing, crystal)
        if flip:
            self.rotate(PI)
        self.housing, self.crystal, self.cable, self.flip = housing, crystal, cable, flip

    def face_point(self):
        return self.crystal.get_top() if self.flip else self.crystal.get_bottom()


def wrap_two_lines(text, size, weight=None):
    """The text as two labels split at the space that makes the wider one narrowest."""
    kw = {} if weight is None else {"weight": weight}
    words = text.split()
    best = None
    for i in range(1, len(words)):
        a, b = label(" ".join(words[:i]), size, **kw), label(" ".join(words[i:]), size, **kw)
        w = max(a.width, b.width)
        if best is None or w < best[0]:
            best = (w, a, b)
    return best[1], best[2]


def tag_line(text, icon_name, color, width=3.9, size=FS_AXIS):
    """A short note without a frame: a Tabler icon in `color` and the text (two lines when it
    does not fit `width`). Parts: icon, txt."""
    ic = icon(icon_name, color, 0.4)
    room = width - 0.65
    one = label(text, size, INK)
    if one.width <= room:
        txt = one
    else:
        a, b = wrap_two_lines(text, size)
        txt = VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    g = VGroup(ic, txt).arrange(RIGHT, buff=0.2)
    g.icon, g.txt = ic, txt
    return g


def signal_bar(frame, level, color):
    """The fill of a horizontal meter `frame` up to `level` (0-1)."""
    r = Rectangle(width=max((frame.width - 0.08) * level, 0.02), height=frame.height - 0.08,
                  color=color, stroke_width=0).set_fill(color, 1)
    return r.align_to(frame, LEFT).shift(RIGHT * 0.04).match_y(frame)


class AScan(VGroup):
    """An A-scan screen: a framed plot with an x axis and an echo-amplitude axis.

    `peaks` is a list of (x position in axis units, height); the signal is the sum of narrow peaks
    of width `sigma` on a flat baseline. Parts of the group: frame, x_axis, y_axis, ticks,
    tick_labels, x_caption, y_caption. `trace` (the signal drawn up to x), `cursor` and `pen` are
    not in the group: the scene adds them and calls `update_trace(x)` / `set_cursor(x)`.
    Positions are read from the frame at call time, so `shift` / `move_to` the group first; do not
    scale it. `x_of(t)` is the screen x of axis value t, `apex(k)` the top of peak k."""

    def __init__(self, peaks, width=6.4, height=2.5, t_min=-0.6, t_max=10.0,
                 ticks=(0, 2, 4, 6, 8, 10), sigma=0.14, x_caption="Time (µs)",
                 y_caption="Echo amplitude"):
        self.peaks, self.t_min, self.t_max, self.sigma = list(peaks), t_min, t_max, sigma
        self._lx, self._rx = -width / 2 + 0.25, width / 2 - 0.3
        self._by = -height / 2 + 0.55
        frame = Rectangle(width=width, height=height, color=INK, stroke_width=3)
        frame.set_fill(PANEL_FILL, 1)
        x_axis = Arrow([self._lx, self._by, 0], [width / 2 - 0.08, self._by, 0], buff=0,
                       color=INK, stroke_width=3, tip_length=0.16)
        y_axis = Arrow([self._lx, self._by, 0], [self._lx, height / 2 - 0.08, 0], buff=0,
                       color=INK, stroke_width=3, tip_length=0.16)
        tick_x = [self._lx + (t - t_min) * (self._rx - self._lx) / (t_max - t_min) for t in ticks]
        tick_marks = VGroup(*[Line([x, self._by, 0], [x, self._by + 0.1, 0], color=INK,
                                   stroke_width=3) for x in tick_x])
        tick_labels = VGroup(*[label(f"{t:g}", FS_TAG - 2, GREY_INK).move_to([x, self._by - 0.28, 0])
                               for t, x in zip(ticks, tick_x)])
        xc = (label(x_caption, FS_TAG, INK).next_to(frame, DOWN, 0.1).align_to(frame, RIGHT)
              if x_caption else VGroup())
        yc = (label(y_caption, FS_TAG, INK).rotate(PI / 2).next_to(frame, LEFT, 0.1)
              if y_caption else VGroup())
        super().__init__(frame, x_axis, y_axis, tick_marks, tick_labels, xc, yc)
        self.frame, self.x_axis, self.y_axis = frame, x_axis, y_axis
        self.ticks, self.tick_labels, self.x_caption, self.y_caption = tick_marks, tick_labels, xc, yc
        self.trace = VMobject(color=INK, stroke_width=3)
        self.trace.set_points_as_corners([[0, 0, 0], [0.01, 0, 0]]).set_stroke(opacity=0)
        self.cursor = Line(ORIGIN, UP, color=ACCENT_1, stroke_width=3)
        self.cursor.set_stroke(opacity=0)
        self.pen = Dot(ORIGIN, radius=0.08, color=ACCENT_1)
        self.pen.set_opacity(0)

    def x_of(self, t):
        k = (self._rx - self._lx) / (self.t_max - self.t_min)
        return self.frame.get_center()[0] + self._lx + (t - self.t_min) * k

    def y_base(self):
        return self.frame.get_center()[1] + self._by

    def signal(self, t):
        return sum(a * np.exp(-((t - tp) / self.sigma) ** 2) for tp, a in self.peaks)

    def apex(self, k):
        tp, a = self.peaks[k]
        return np.array([self.x_of(tp), self.y_base() + a, 0.0])

    def update_trace(self, t_end, step=None):
        t_end = min(t_end, self.t_max)
        step = step or (self.t_max - self.t_min) / 500
        if t_end <= self.t_min + step:
            self.trace.set_stroke(opacity=0)
            self.pen.set_opacity(0)
            return self.trace
        ts = np.arange(self.t_min, t_end + 1e-9, step)
        pts = [[self.x_of(t), self.y_base() + self.signal(t), 0.0] for t in ts]
        self.trace.set_points_as_corners(pts)
        self.trace.set_stroke(color=INK, width=3, opacity=1)
        self.pen.set_opacity(1).move_to(pts[-1])
        return self.trace

    def set_cursor(self, t):
        x = self.x_of(min(max(t, self.t_min), self.t_max))
        self.cursor.put_start_and_end_on([x, self.y_base() - 0.08, 0], [x, self.y_base() + 0.5, 0])
        self.cursor.set_stroke(opacity=1 if t >= self.t_min else 0)
        return self.cursor


# ---------------- Added for episode 4 (weld drawings); shared by any later episode ----------------
import ut_series_data as D                                    # noqa: E402  (the wedge uses the perspex and shear velocities)


def knob(caption, size=0.55, color=INK):
    """A round knob with a pointer (`pointer` turns with `set_turn(0..1)`) and a caption below.
    (The same drawing as the `knob` of episode 3's script, which keeps its own copy.)"""
    ring = Circle(radius=size, color=color, stroke_width=4).set_fill(PANEL_FILL, 1)
    ptr = Line(ORIGIN, UP * size * 0.8, color=ACCENT_2, stroke_width=5)
    cap = label(caption, FS_TAG, INK, weight=BOLD).next_to(ring, DOWN, 0.12)
    g = VGroup(ring, ptr, cap)
    g.ring, g.pointer, g.caption, g.size = ring, ptr, cap, size

    def set_turn(v):
        a = PI * 0.75 - v * PI * 1.5            # sweeps from the lower left to the lower right
        c0 = ring.get_center()
        ptr.put_start_and_end_on(c0, c0 + size * 0.8 * np.array([np.cos(a), np.sin(a), 0]))
        return g
    g.set_turn = set_turn
    set_turn(0.5)
    return g


def wedge_probe(x_exit, y_top, facing=1, color=ACCENT_1, size=1.0, beta=D.PROBE_ANGLE):
    """An angle probe on a plastic wedge (as episode 3): the sole runs on both sides of the exit point, the
    crystal sits on the slanted top face perpendicular to the beam. facing = 1: the beam goes to the right.
    Returns VGroup(wedge, crystal, beam_in) with .exit (the exit point), .wedge, .crystal, .beam_in."""
    a = np.arcsin(np.sin(np.radians(beta)) * D.V_L_PERSPEX / D.V_S_STEEL)
    L, hh = 0.85 * size, 0.32 * size
    b = np.array([facing * np.sin(a), -np.cos(a), 0.0])
    p = np.array([facing * np.cos(a), np.sin(a), 0.0])
    ex0 = np.array([x_exit, y_top, 0.0])
    cen = ex0 - b * L
    e_f, e_b = cen + p * hh, cen - p * hh
    front_bottom = np.array([x_exit + facing * 0.38 * size, y_top, 0.0])
    back_bottom = np.array([x_exit - facing * (L * np.sin(a) + 0.5 * size), y_top, 0.0])
    wedge = Polygon(front_bottom, back_bottom, e_b, e_f, color=GREY_INK, stroke_width=3).set_fill(color, 0.18)
    crystal = Line(e_b, e_f, color=color, stroke_width=9)
    beam_in = DashedLine(cen, ex0, color=color, stroke_width=2)
    g = VGroup(wedge, crystal, beam_in)
    g.exit, g.wedge, g.crystal, g.beam_in = ex0, wedge, crystal, beam_in
    return g


class WeldSection(VGroup):
    """A single-vee butt weld in section: two plates, the vee filled with weld metal, a cap above and a root bead
    below. The top surface is at `y_top`, the weld centre line at x = `cx`, the plates run `half_w` to each side.
    `prep_deg` is the weld preparation angle (the whole vee); a fusion face is inclined prep/2 from the vertical.
    Parts: plate_l, plate_r, weld, cap, root, face_l, face_r (the fusion faces, top to bottom).
    `face_point(side, frac)`: the point on the fusion face of side +1 (right) / -1 (left), frac 0 at the top
    surface and 1 at the bottom. `surface_x(dist)`: x on the top surface `dist` units from the centre line."""

    def __init__(self, cx=0.0, y_top=1.0, t=1.4, prep_deg=60.0, half_w=6.0, gap=0.1):
        self.cx, self.y_top, self.t, self.prep, self.half_w, self.gap = cx, y_top, t, prep_deg, half_w, gap
        yb = y_top - t
        w = gap + t * np.tan(np.radians(prep_deg / 2))
        self.w, self.y_bot = w, yb
        left = Polygon([cx - half_w, y_top, 0], [cx - w, y_top, 0], [cx - gap, yb, 0], [cx - half_w, yb, 0],
                       color=INK, stroke_width=4).set_fill(PANEL_FILL, 1)
        right = Polygon([cx + half_w, y_top, 0], [cx + w, y_top, 0], [cx + gap, yb, 0], [cx + half_w, yb, 0],
                        color=INK, stroke_width=4).set_fill(PANEL_FILL, 1)
        weld = Polygon([cx - w, y_top, 0], [cx + w, y_top, 0], [cx + gap, yb, 0], [cx - gap, yb, 0],
                       color=GREY_INK, stroke_width=2).set_fill(ACCENT_2, 0.16)
        xs = np.linspace(-w - 0.12, w + 0.12, 24)
        cap = Polygon(*[[cx + x, y_top + 0.17 * (1 - (x / (w + 0.12)) ** 2), 0] for x in xs],
                      color=INK, stroke_width=3).set_fill(ACCENT_2, 0.16)
        rx = np.linspace(-gap - 0.1, gap + 0.1, 12)
        root = Polygon(*[[cx + x, yb - 0.11 * (1 - (x / (gap + 0.1)) ** 2), 0] for x in rx],
                       color=INK, stroke_width=3).set_fill(ACCENT_2, 0.16)
        face_l = Line([cx - w, y_top, 0], [cx - gap, yb, 0], color=INK, stroke_width=4)
        face_r = Line([cx + w, y_top, 0], [cx + gap, yb, 0], color=INK, stroke_width=4)
        super().__init__(left, right, weld, cap, root, face_l, face_r)
        self.plate_l, self.plate_r, self.weld, self.cap, self.root = left, right, weld, cap, root
        self.face_l, self.face_r = face_l, face_r

    def face_point(self, side, frac):
        x_top, x_bot = self.cx + side * self.w, self.cx + side * self.gap
        return np.array([x_top + (x_bot - x_top) * frac, self.y_top - self.t * frac, 0.0])

    def surface_x(self, dist):
        return self.cx + dist


def vee_arrow_to(frm, to, color=ACCENT_1, width=4, dashed=True):
    """A beam leg from `frm` to `to` (an arrow, dashed or plain) for the section drawings."""
    return (DashedLine(frm, to, color=color, stroke_width=width) if dashed
            else Arrow(frm, to, buff=0, color=color, stroke_width=width, tip_length=0.16))


def small_scan(center, peaks, width=6.0, height=2.3, t_max=110.0, ticks=(0, 25, 50, 75, 100), sigma=0.9,
               x_caption="Distance (mm)", y_caption="Echo amplitude", t_min=-6.0):
    """An AScan placed with its frame centred on `center`, its trace fully drawn (`trace` is not added)."""
    sc = AScan(peaks, width=width, height=height, t_min=t_min, t_max=t_max, ticks=ticks, sigma=sigma,
               x_caption=x_caption, y_caption=y_caption)
    sc.shift(np.array([center[0], center[1], 0.0]) - sc.frame.get_center())
    sc.update_trace(sc.t_max)
    return sc
