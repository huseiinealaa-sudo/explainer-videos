"""pt_cal: drawing helpers shared by the episode scripts (episode 2 keeps its own copies).

Palette roles (project CLAUDE.md): ACCENT_1 blue = pressure / input / fluid; ACCENT_2 orange =
generated signal, output, moving parts, heat; ACCENT_3 green = correct / PASS; ACCENT_4 red =
danger, error, leak, FAIL.
"""
import re
from pathlib import Path

from explainer import *

FLUID = ACCENT_1
MOVE = ACCENT_2
GOOD = ACCENT_3
BAD = ACCENT_4
AIR = GREY_INK
FLUID_FILL = "#cfe0f3"
BODY_FILL = "#f4f4f4"
SERIES = "Pressure transmitter calibration"
NOTE = "Educational material — the manufacturer's manuals and your site procedures are binding"


def fmt(x, nd=1):
    """Number for the screen with a real minus sign."""
    return f"{x:.{nd}f}".replace("-", "−")


def sfmt(x, nd=2):
    """Signed number (+0.37 / −0.30)."""
    return ("+" if x > 0 else "") + fmt(x, nd)


def tag(text, size=FS_TAG, color=INK, **kw):
    return label(text, size, color, **kw)


def pipe(*pts, color=INK, width=6):
    m = VMobject(color=color, stroke_width=width)
    m.set_points_as_corners([np.array(p, dtype=float) for p in pts])
    return m


def poly(pts, color=INK, width=4, smooth=False):
    m = VMobject(color=color, stroke_width=width)
    pts = [np.array(p, dtype=float) for p in pts]
    if smooth:
        m.set_points_smoothly(pts)
    else:
        m.set_points_as_corners(pts)
    return m


def flow(path, color=FLUID, width=10, time_width=0.6):
    return ShowPassingFlash(path.copy().set_stroke(color, width), time_width=time_width)


def cross(mob, color=BAD, width=6, pad=0.1):
    """Red X over a drawing (built on a padded box, so a flat item still gets a real X)."""
    box = SurroundingRectangle(mob, buff=pad)
    a = Line(box.get_corner(UL), box.get_corner(DR), stroke_width=width, color=color)
    b = Line(box.get_corner(DL), box.get_corner(UR), stroke_width=width, color=color)
    return VGroup(a, b)


def card(title, body, color=INK, width=3.0, size=FS_TAG, fill=WHITE):
    """Rounded card: bold title and a few lines, text kept clear of the outline."""
    t = tag(title, size + 2, color, weight=BOLD)
    b = tag(body, size, INK, line_spacing=1.1) if body else VGroup()
    inner = VGroup(t, b).arrange(DOWN, buff=0.18) if body else VGroup(t)
    fit(inner, width - 0.4)
    frame = RoundedRectangle(width=width, height=inner.height + 0.5, corner_radius=0.15, color=color,
                             stroke_width=4).set_fill(fill, 1)
    inner.move_to(frame)
    g = VGroup(frame, inner)
    g.frame = frame
    return g


def transmitter(tag_loop="101", bubble=True):
    """Generic pressure transmitter (no brand): body, process port on the left, ISA bubble."""
    body = RoundedRectangle(width=1.0, height=1.2, corner_radius=0.12, color=INK, stroke_width=4) \
        .set_fill(WHITE, 1)
    head = Circle(radius=0.42, color=INK, stroke_width=4).set_fill(WHITE, 1).next_to(body, UP, buff=0)
    port = Line(body.get_left(), body.get_left() + LEFT * 0.35, stroke_width=8, color=INK)
    parts = [body, head, port]
    if bubble:
        bub = instrument("PT", tag_loop, size=0.9).next_to(head, RIGHT, buff=0.3)
        lead = Line(head.get_right(), bub.get_left(), stroke_width=2, color=GREY_INK)
        parts += [bub, lead]
    g = VGroup(*parts)
    g.port_point = lambda: port.get_end()
    g.body = body
    g.head = head
    return g


def device(name, width=2.2, height=1.4, size=FS_BODY):
    """Simplified box for a calibrator or a system (no product image)."""
    box = RoundedRectangle(width=width, height=height, corner_radius=0.15, color=INK, stroke_width=4) \
        .set_fill(WHITE, 1)
    t = tag(name, size, weight=BOLD).move_to(box)
    fit(t, width - 0.4)
    g = VGroup(box, t)
    g.box = box
    return g


class Chart:
    """Plain axes (no LaTeX): data (x, y) → scene point with p(x, y); ticks labelled with Text."""

    def __init__(self, x0, y0, w, h, xr, yr, xticks=(), yticks=(), xlabel="", ylabel="",
                 size=FS_TAG, arrows=False):
        self.x0, self.y0, self.w, self.h, self.xr, self.yr = x0, y0, w, h, xr, yr
        a = Line([x0, y0, 0], [x0 + w, y0, 0], stroke_width=3, color=INK)
        b = Line([x0, y0, 0], [x0, y0 + h, 0], stroke_width=3, color=INK)
        self.axes = VGroup(a, b)
        self.ticks = VGroup()
        for v, t in xticks:
            px = self.p(v, yr[0])
            self.ticks.add(Line(px, px + DOWN * 0.1, stroke_width=2, color=INK))
            self.ticks.add(tag(t, size).next_to(px + DOWN * 0.1, DOWN, buff=0.08))
        for v, t in yticks:
            py = self.p(xr[0], v)
            self.ticks.add(Line(py, py + LEFT * 0.1, stroke_width=2, color=INK))
            self.ticks.add(tag(t, size).next_to(py + LEFT * 0.1, LEFT, buff=0.08))
        self.xl = tag(xlabel, size, GREY_INK).next_to(a, DOWN, buff=0.45).align_to(a, RIGHT) \
            if xlabel else VGroup()
        self.yl = tag(ylabel, size, GREY_INK).next_to(b, UP, buff=0.15).align_to(b, LEFT) \
            if ylabel else VGroup()
        self.group = VGroup(self.axes, self.ticks, self.xl, self.yl)

    def p(self, x, y):
        fx = (x - self.xr[0]) / (self.xr[1] - self.xr[0])
        fy = (y - self.yr[0]) / (self.yr[1] - self.yr[0])
        return np.array([self.x0 + fx * self.w, self.y0 + fy * self.h, 0.0])

    def line(self, pts, color=INK, width=4, smooth=False):
        return poly([self.p(x, y) for x, y in pts], color, width, smooth)

    def dots(self, pts, color=INK, r=0.07):
        return VGroup(*[Dot(self.p(x, y), radius=r, color=color) for x, y in pts])

    def hline(self, y, color=INK, dashed=True, width=2):
        a, b = self.p(self.xr[0], y), self.p(self.xr[1], y)
        return DashedLine(a, b, color=color, stroke_width=width) if dashed else Line(a, b, color=color,
                                                                                    stroke_width=width)

    def band(self, lo, hi, color=GOOD, opacity=0.12):
        a, b = self.p(self.xr[0], lo), self.p(self.xr[1], hi)
        return Rectangle(width=b[0] - a[0], height=b[1] - a[1], stroke_width=0) \
            .set_fill(color, opacity).move_to((a + b) / 2)


def title_segment(scene, title, subtitle, episode):
    """Title card with the series line and the educational-material notice."""
    t = title_card(scene, title, subtitle, series=f"{SERIES} · Episode {episode} of 7")
    note = fit(tag(NOTE, FS_TAG, GREY_INK)).next_to(t, DOWN, buff=0.6)
    scene.play(FadeIn(note), run_time=0.6)
    return VGroup(t, note)


def narration_from_storyboard(md_path):
    """The approved narration of an episode (numbered lines under '## Narration')."""
    md = Path(md_path).read_text().split("## Narration", 1)[1]
    return [m.group(1).strip() for m in re.finditer(r"^\d+\.\s+(.*)$", md, re.M)]
