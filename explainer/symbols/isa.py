"""ISA-5.1 style P&ID symbols drawn in code (no copied images), with ports for signal lines.

Every symbol is a function that returns a `Symbol` (a VGroup) of one size and colour:
    v = control_valve(size=1.0, color=INK)
    v.port("in"), v.port("out"), v.port("actuator")    # points that move with the symbol
    v.port_names()                                     # the ports it offers
Instrument bubbles carry the function letters and the loop number:
    ft = instrument("FT", "101", location="field")     # field | panel | behind_panel | dcs | plc
Lines join two ports by an ISA line type, routed straight or in right angles:
    connect(ft, "top", fic, "bottom", kind="electrical", route="vh")
    kinds: process | connection | pneumatic | electrical | capillary | data   (SIGNAL_KINDS)

The unit is `size` (1.0 = a valve body 0.9 units wide); strokes are STROKE (process lines
PROCESS_STROKE). Loop numbers and tags in examples are illustrative only (FT-101 ...).
Where each drawing comes from (free references, the standard itself is paid) is listed in
explainer/symbols/SOURCES.md; ISA_GROUPS names the symbols by group for catalogues.
"""
import numpy as np
from manim import (DOWN, LEFT, ORIGIN, PI, RIGHT, UP, Arc, Circle, Dot, Line, Polygon,
                   Square, VGroup, VMobject, VectorizedPoint, DashedVMobject)

from ..style import BG, FS_TAG, INK, MIN_FONT_SIZE, label

__all__ = ["Symbol", "gate_valve", "globe_valve", "ball_valve", "butterfly_valve",
           "check_valve", "control_valve", "relief_valve", "centrifugal_pump", "pd_pump",
           "compressor", "tank", "heat_exchanger", "orifice_plate", "turbine_meter",
           "magnetic_flowmeter", "coriolis_meter", "vortex_meter", "instrument",
           "signal_line", "connect", "SIGNAL_KINDS", "LOCATIONS", "ISA_GROUPS"]

STROKE = 3                  # symbol outlines and signal lines
PROCESS_STROKE = 6          # process flow lines and in-line pipe stubs
MARK_SPACING = 0.9          # distance between line-type marks (slashes, crosses, circles)
TAG_SIZE = FS_TAG           # largest font of the function letters and loop number


class Symbol(VGroup):
    """A drawn symbol plus named ports (invisible points that move with it)."""

    def __init__(self, *mobs, name="", **kw):
        super().__init__(*mobs, **kw)
        self.symbol_name = name
        self._ports = {}

    def add_port(self, name, point):
        vp = VectorizedPoint(np.array(point, dtype=float))
        self._ports[name] = vp
        self.add(vp)
        return self

    def port(self, name):
        if name not in self._ports:
            raise KeyError(f"{self.symbol_name}: no port {name!r} (has {self.port_names()})")
        return self._ports[name].get_center()

    def port_names(self):
        return list(self._ports)


def _p(x, y):
    return np.array([x, y, 0.0])


def _poly(*pts, color=INK, width=STROKE, close=False):
    m = VMobject(color=color, stroke_width=width)
    pts = [_p(*p) for p in pts]
    m.set_points_as_corners(pts + ([pts[0]] if close else []))
    return m


def _line(a, b, color=INK, width=STROKE):
    return Line(_p(*a), _p(*b), color=color, stroke_width=width)


def _finish(sym, size, color):
    """Scale from the unit drawing (size 1) and colour every stroke."""
    for m in sym.family_members_with_points():
        if isinstance(m, VectorizedPoint):
            continue
        m.set_stroke(color)
        if m.get_fill_opacity() > 0 and getattr(m, "keep_fill", None) is None:
            m.set_fill(color)
    sym.scale(size, about_point=ORIGIN)
    return sym


def _bowtie(color):
    """Two triangles meeting at the centre: the two-way valve body (0.9 × 0.5)."""
    return _poly((-0.45, 0.25), (-0.45, -0.25), (0.45, 0.25), (0.45, -0.25), color=color,
                 close=True)


def _two_way(name, extra, size, color):
    s = Symbol(_bowtie(color), *extra, name=name)
    s.add_port("in", _p(-0.45, 0)).add_port("out", _p(0.45, 0))
    return _finish(s, size, color)


# ---------------- valves ----------------
def gate_valve(size=1.0, color=INK):
    """Gate valve: the plain two-way body (two triangles tip to tip)."""
    return _two_way("gate valve", [], size, color)


def globe_valve(size=1.0, color=INK):
    """Globe valve: two-way body with a solid dot at the centre."""
    return _two_way("globe valve", [Dot(ORIGIN, radius=0.07, color=color)], size, color)


def ball_valve(size=1.0, color=INK):
    """Ball valve: two-way body with an open circle (the ball) at the centre."""
    ball = Circle(radius=0.13, color=color, stroke_width=STROKE).set_fill(BG, 1)
    ball.keep_fill = True
    return _two_way("ball valve", [ball], size, color)


def butterfly_valve(size=1.0, color=INK):
    """Butterfly valve: two end flanges and the disc, a slanted line with its shaft dot."""
    flanges = VGroup(_line((-0.3, 0.3), (-0.3, -0.3)), _line((0.3, 0.3), (0.3, -0.3)))
    disc = _line((-0.12, -0.24), (0.12, 0.24))
    s = Symbol(flanges, disc, Dot(ORIGIN, radius=0.06), name="butterfly valve")
    s.add_port("in", _p(-0.3, 0)).add_port("out", _p(0.3, 0))
    return _finish(s, size, color)


def check_valve(size=1.0, color=INK):
    """Check valve: |\\| body with the free-flow direction arrow above (left to right)."""
    body = _poly((-0.3, 0.3), (-0.3, -0.3), color=color)
    diag = _poly((-0.3, 0.3), (0.3, -0.3), color=color)
    right = _poly((0.3, 0.3), (0.3, -0.3), color=color)
    arrow = _poly((-0.2, 0.45), (0.12, 0.45), color=color)
    head = Polygon(_p(0.22, 0.45), _p(0.1, 0.5), _p(0.1, 0.4), color=color,
                   stroke_width=STROKE).set_fill(color, 1)
    s = Symbol(body, diag, right, arrow, head, name="check valve")
    s.add_port("in", _p(-0.3, 0)).add_port("out", _p(0.3, 0))
    return _finish(s, size, color)


def control_valve(size=1.0, color=INK):
    """Control valve with a spring-and-diaphragm actuator: two-way body, stem, dome."""
    stem = _line((0, 0), (0, 0.55))
    dome = Arc(radius=0.3, start_angle=0, angle=PI, color=color, stroke_width=STROKE)
    dome.move_arc_center_to(_p(0, 0.55))
    base = _line((-0.3, 0.55), (0.3, 0.55))
    s = Symbol(_bowtie(color), stem, dome, base, name="control valve")
    s.add_port("in", _p(-0.45, 0)).add_port("out", _p(0.45, 0))
    s.add_port("actuator", _p(0, 0.85))
    return _finish(s, size, color)


def relief_valve(size=1.0, color=INK):
    """Pressure relief / safety valve: angle body (inlet below, outlet right), spring on top."""
    inlet = _poly((0, 0), (-0.25, -0.45), (0.25, -0.45), color=color, close=True)
    outlet = _poly((0, 0), (0.45, 0.25), (0.45, -0.25), color=color, close=True)
    stem = _line((0, 0), (0, 0.18))
    zig = [(0, 0.18)] + [((-0.14 if k % 2 == 0 else 0.14), 0.24 + 0.08 * k)
                         for k in range(5)] + [(0, 0.66)]
    spring = _poly(*zig, color=color)
    s = Symbol(inlet, outlet, stem, spring, name="relief valve")
    s.add_port("in", _p(0, -0.45)).add_port("out", _p(0.45, 0))
    return _finish(s, size, color)


# ---------------- pumps and machines ----------------
def centrifugal_pump(size=1.0, color=INK):
    """Centrifugal pump: casing circle, suction at the centre from the left, tangential
    discharge at the top to the right, and a base."""
    r = 0.4
    casing = Circle(radius=r, color=color, stroke_width=STROKE)
    discharge = _line((0, r), (0.55, r), width=PROCESS_STROKE)     # the discharge nozzle
    feet = _poly((-0.3, -0.5), (-0.2, -r * 0.8), color=color)
    feet2 = _poly((0.3, -0.5), (0.2, -r * 0.8), color=color)
    base = _line((-0.42, -0.5), (0.42, -0.5))
    s = Symbol(casing, discharge, feet, feet2, base, name="centrifugal pump")
    s.add_port("in", _p(-r, 0)).add_port("out", _p(0.55, r))
    return _finish(s, size, color)


def pd_pump(size=1.0, color=INK):
    """Positive displacement pump: stepped casing with suction left and discharge right."""
    casing = _poly((-0.35, -0.25), (0.45, -0.25), (0.45, 0.05), (0.1, 0.05), (0.1, 0.4),
                   (-0.35, 0.4), color=color, close=True)
    rotor = VGroup(Circle(radius=0.09, color=color, stroke_width=STROKE).move_to(_p(-0.23, 0.08)),
                   Circle(radius=0.09, color=color, stroke_width=STROKE).move_to(_p(-0.05, 0.08)))
    s = Symbol(casing, rotor, name="positive displacement pump")
    s.add_port("in", _p(-0.35, -0.1)).add_port("out", _p(0.45, -0.1))
    return _finish(s, size, color)


def compressor(size=1.0, color=INK):
    """Compressor: casing circle with two lines converging from inlet (left) to outlet
    (right), the flow path narrowing as the gas is compressed."""
    r = 0.42
    casing = Circle(radius=r, color=color, stroke_width=STROKE)
    a, b = np.deg2rad(125), np.deg2rad(30)
    top = _line((r * np.cos(a), r * np.sin(a)), (r * np.cos(b), r * np.sin(b)))
    bot = _line((r * np.cos(a), -r * np.sin(a)), (r * np.cos(b), -r * np.sin(b)))
    s = Symbol(casing, top, bot, name="compressor")
    s.add_port("in", _p(-r, 0)).add_port("out", _p(r, 0))
    return _finish(s, size, color)


def tank(size=1.0, color=INK, width=1.1, height=1.3):
    """Atmospheric storage tank: vertical shell with a cone roof.

    Ports: top (roof nozzle), inlet (upper left side), outlet (bottom of the right side),
    bottom (centre of the floor)."""
    w, h = width / 2, height / 2
    shell = _poly((-w, h), (-w, -h), (w, -h), (w, h), color=color)
    roof = _poly((-w, h), (0, h + 0.25), (w, h), color=color)
    s = Symbol(shell, roof, name="tank")
    s.add_port("top", _p(0, h + 0.25)).add_port("inlet", _p(-w, h - 0.3))
    s.add_port("outlet", _p(w, -h + 0.2)).add_port("bottom", _p(0, -h))
    return _finish(s, size, color)


def heat_exchanger(size=1.0, color=INK):
    """Shell-and-tube heat exchanger: shell circle with the tube bundle drawn as a zigzag
    passing through it. Tube side left/right, shell side top/bottom."""
    r = 0.42
    shell = Circle(radius=r, color=color, stroke_width=STROKE)
    tube = _poly((-0.6, 0), (-0.22, 0), (-0.1, 0.2), (0.06, -0.2), (0.2, 0.08), (0.28, 0),
                 (0.6, 0), color=color)
    shell_in = _line((0, r), (0, r + 0.18))
    shell_out = _line((0, -r), (0, -r - 0.18))
    s = Symbol(shell, tube, shell_in, shell_out, name="heat exchanger")
    s.add_port("tube_in", _p(-0.6, 0)).add_port("tube_out", _p(0.6, 0))
    s.add_port("shell_in", _p(0, r + 0.18)).add_port("shell_out", _p(0, -r - 0.18))
    return _finish(s, size, color)


# ---------------- flow measurement (in-line, flow left to right) ----------------
def _inline(name, body, size, color, tap_y):
    stubs = VGroup(_line((-0.6, 0), (-0.3, 0), width=PROCESS_STROKE),
                   _line((0.3, 0), (0.6, 0), width=PROCESS_STROKE))
    s = Symbol(stubs, *body, name=name)
    s.add_port("in", _p(-0.6, 0)).add_port("out", _p(0.6, 0)).add_port("tap", _p(0, tap_y))
    return _finish(s, size, color)


def _meter_box():
    return Square(side_length=0.6, color=INK, stroke_width=STROKE)


def orifice_plate(size=1.0, color=INK):
    """Orifice plate: the plate between two flanges, two short bars across the pipe."""
    pipe = _line((-0.3, 0), (0.3, 0), width=PROCESS_STROKE)
    plates = VGroup(_line((-0.06, 0.3), (-0.06, -0.3)), _line((0.06, 0.3), (0.06, -0.3)))
    return _inline("orifice plate", [pipe, plates], size, color, 0.3)


def turbine_meter(size=1.0, color=INK):
    """Turbine meter: a box across the pipe with the rotor drawn as a two-bladed propeller."""
    blade = VGroup(Circle(radius=0.11, color=INK, stroke_width=STROKE).stretch(0.45, 0)
                   .move_to(_p(0, 0.11)),
                   Circle(radius=0.11, color=INK, stroke_width=STROKE).stretch(0.45, 0)
                   .move_to(_p(0, -0.11)))
    return _inline("turbine meter", [_meter_box(), blade], size, color, 0.3)


def magnetic_flowmeter(size=1.0, color=INK):
    """Magnetic flowmeter: a box across the pipe with the letter M."""
    m = label("M", TAG_SIZE + 2, INK)
    return _inline("magnetic flowmeter", [_meter_box(), m], size, color, 0.3)


def coriolis_meter(size=1.0, color=INK):
    """Coriolis meter: a box across the pipe with the vibrating tube drawn as a small wave."""
    wave = _poly((-0.2, 0), (-0.1, 0), (-0.03, 0.1), (0.05, -0.1), (0.1, 0), (0.2, 0),
                 color=INK)
    return _inline("Coriolis meter", [_meter_box(), wave], size, color, 0.3)


def vortex_meter(size=1.0, color=INK):
    """Vortex meter: a box across the pipe with the bluff body drawn as a triangle."""
    bluff = _poly((-0.13, 0.15), (-0.13, -0.15), (0.14, 0), color=INK, close=True)
    return _inline("vortex meter", [_meter_box(), bluff], size, color, 0.3)


# ---------------- instrument bubbles ----------------
LOCATIONS = {
    "field": "discrete instrument, field mounted (circle, no line)",
    "panel": "discrete instrument, primary location, accessible to the operator "
             "(circle, solid line)",
    "behind_panel": "discrete instrument, primary location, not accessible to the operator "
                    "(circle, dashed line)",
    "dcs": "shared display / shared control, DCS (circle in square, solid line)",
    "plc": "programmable logic control, PLC (diamond in square, solid line)",
}


TEXT_CLEAR = 0.07           # between a bubble's text and its outline or centre line


def _bubble_text(text, size, color, bold, y_edge, half_width):
    """The largest font (text_size down to MIN_FONT_SIZE) whose box fits the shape.

    y_edge(h): distance from the centre line to the text's outer edge for a text h high;
    half_width(y): the shape's half width at that height."""
    for fs in range(size, MIN_FONT_SIZE - 1, -1):
        t = label(text, fs, color, **({"weight": "BOLD"} if bold else {}))
        if t.width / 2 <= half_width(y_edge(t.height)) - TEXT_CLEAR:
            return t
    return t


def instrument(function, loop="", location="field", size=1.0, color=INK, text_size=TAG_SIZE):
    """Instrument bubble: function letters (FT, PIC ...) above, loop number below.

    location: field | panel | behind_panel | dcs | plc (see LOCATIONS). The bubble is 1 unit
    across at size 1; its text takes the largest font from text_size down to MIN_FONT_SIZE
    that keeps TEXT_CLEAR from the outline. Ports top, bottom, left, right on the outer
    outline. Loop numbers in examples are illustrative.
    """
    if location not in LOCATIONS:
        raise ValueError(f"location must be one of {list(LOCATIONS)}")
    r = 0.5
    parts = []
    if location == "plc":
        parts.append(_poly((-r, 0), (0, r), (r, 0), (0, -r), color=color, close=True))
        half_width = lambda y: r - y                                      # noqa: E731
    else:
        parts.append(Circle(radius=r, color=color, stroke_width=STROKE))
        half_width = lambda y: np.sqrt(max(r * r - y * y, 0.0))           # noqa: E731
    if location in ("dcs", "plc"):
        parts.append(Square(side_length=2 * r, color=color, stroke_width=STROKE))
    gap = TEXT_CLEAR / 2                          # field: letters and number just apart
    if location != "field":
        bar = _line((-r, 0), (r, 0))
        if location == "behind_panel":
            bar = DashedVMobject(bar, num_dashes=7)
        parts.append(bar)
        gap = TEXT_CLEAR
    has_loop = loop != ""
    lift = gap if has_loop else 0.0
    y_edge = (lambda h: lift + h) if has_loop else (lambda h: h / 2)      # noqa: E731
    top = _bubble_text(function, text_size, color, True, y_edge, half_width)
    texts = VGroup(top)
    if has_loop:
        bottom = _bubble_text(str(loop), text_size, color, False, y_edge, half_width)
        top.move_to(_p(0, lift + top.height / 2))
        bottom.move_to(_p(0, -lift - bottom.height / 2))
        texts.add(bottom)
    s = Symbol(*parts, texts, name=f"{location} instrument")
    s.function, s.loop, s.location = function, loop, location
    s.tag = f"{function}-{loop}" if has_loop else function
    s.texts = texts
    s.add_port("top", _p(0, r)).add_port("bottom", _p(0, -r))
    s.add_port("left", _p(-r, 0)).add_port("right", _p(r, 0))
    s.scale(size, about_point=ORIGIN)
    return s


# ---------------- signal and process lines ----------------
SIGNAL_KINDS = {
    "process": "process flow line: heavy solid",
    "connection": "instrument supply or process connection (impulse line): thin solid",
    "pneumatic": "pneumatic signal: thin line with double slashes",
    "electrical": "electrical (electronic) signal: dashed line",
    "capillary": "capillary tube: thin line with crosses",
    "data": "data link / software link (shared system): thin line with small open circles",
}


def _route(a, b, route):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    if route == "straight" or np.isclose(a[0], b[0]) or np.isclose(a[1], b[1]):
        return [a, b]
    if route == "hv":
        return [a, _p(b[0], a[1]), b]
    if route == "vh":
        return [a, _p(a[0], b[1]), b]
    if route == "hvh":
        xm = (a[0] + b[0]) / 2
        return [a, _p(xm, a[1]), _p(xm, b[1]), b]
    if route == "vhv":
        ym = (a[1] + b[1]) / 2
        return [a, _p(a[0], ym), _p(b[0], ym), b]
    raise ValueError(f"route must be straight | hv | vh | hvh | vhv, not {route!r}")


def _marks_along(pts, spacing, end_gap):
    """(point, unit direction) every `spacing` along the polyline, `end_gap` from its ends."""
    segs = [(p, q) for p, q in zip(pts, pts[1:]) if np.linalg.norm(q - p) > 1e-9]
    total = sum(np.linalg.norm(q - p) for p, q in segs)
    if total <= 2 * end_gap:
        return []
    n = max(1, int((total - 2 * end_gap) // spacing) + 1)
    first = (total - (n - 1) * spacing) / 2
    out, s0 = [], 0.0
    targets = [first + k * spacing for k in range(n)]
    for p, q in segs:
        L = np.linalg.norm(q - p)
        d = (q - p) / L
        for t in targets:
            if s0 <= t <= s0 + L:
                out.append((p + d * (t - s0), d))
        s0 += L
    return out


def signal_line(points, kind="electrical", color=INK, arrow=False, spacing=MARK_SPACING,
                end_gap=0.3):
    """A line of ISA type `kind` through `points` (corners); returns a VGroup.

    group[0] is the path (dashed for electrical); the marks follow. arrow=True puts an
    arrowhead at the last point (flow or signal direction).
    """
    if kind not in SIGNAL_KINDS:
        raise ValueError(f"kind must be one of {list(SIGNAL_KINDS)}")
    pts = [np.array(p, dtype=float) for p in points]
    width = PROCESS_STROKE if kind == "process" else STROKE - 0.5
    path = VMobject(color=color, stroke_width=width)
    path.set_points_as_corners(pts)
    if kind == "electrical":
        length = sum(np.linalg.norm(q - p) for p, q in zip(pts, pts[1:]))
        path = DashedVMobject(path, num_dashes=max(2, int(length / 0.16)), dashed_ratio=0.55)
    group = VGroup(path)
    marks = _marks_along(pts, spacing, end_gap)
    for c, d in marks:
        nrm = np.array([-d[1], d[0], 0.0])
        if kind == "pneumatic":
            for off in (-0.05, 0.05):
                slant = (nrm + 0.5 * d) / np.linalg.norm(nrm + 0.5 * d) * 0.12
                m = c + d * off
                group.add(Line(m - slant, m + slant, color=color, stroke_width=STROKE - 0.5))
        elif kind == "capillary":
            for v in (nrm + d, nrm - d):
                v = v / np.linalg.norm(v) * 0.1
                group.add(Line(c - v, c + v, color=color, stroke_width=STROKE - 0.5))
        elif kind == "data":
            group.add(Circle(radius=0.055, color=color, stroke_width=STROKE - 0.5)
                      .set_fill(BG, 1).move_to(c))
    if arrow:
        d = pts[-1] - pts[-2]
        d = d / np.linalg.norm(d)
        nrm = np.array([-d[1], d[0], 0.0])
        tip, L, w = pts[-1], 0.2, 0.09
        group.add(Polygon(tip, tip - d * L + nrm * w, tip - d * L - nrm * w, color=color,
                          stroke_width=1).set_fill(color, 1))
    group.kind = kind
    return group


def connect(a, port_a, b, port_b, kind="electrical", route="straight", via=None, color=INK,
            arrow=False, **kw):
    """Join port `port_a` of symbol a to port `port_b` of symbol b with an ISA line type.

    route: straight | hv (horizontal then vertical) | vh | hvh | vhv, or pass `via`
    (a list of corner points). Returns the line (a VGroup from signal_line)."""
    pa, pb = a.port(port_a), b.port(port_b)
    pts = [pa, *[np.array(v, dtype=float) for v in via], pb] if via else _route(pa, pb, route)
    return signal_line(pts, kind=kind, color=color, arrow=arrow, **kw)


# Catalogue order (used by projects/symbol_gallery): group -> [(function, display name)].
ISA_GROUPS = {
    "Valves": [("gate_valve", "Gate"), ("globe_valve", "Globe"), ("ball_valve", "Ball"),
               ("butterfly_valve", "Butterfly"), ("check_valve", "Check"),
               ("control_valve", "Control valve (diaphragm)"),
               ("relief_valve", "Relief / safety")],
    "Pumps and machines": [("centrifugal_pump", "Centrifugal pump"),
                           ("pd_pump", "Positive displacement pump"),
                           ("compressor", "Compressor"), ("tank", "Tank"),
                           ("heat_exchanger", "Heat exchanger")],
    "Flow measurement": [("orifice_plate", "Orifice plate"), ("turbine_meter", "Turbine"),
                         ("magnetic_flowmeter", "Magnetic"), ("coriolis_meter", "Coriolis"),
                         ("vortex_meter", "Vortex")],
}
