"""Symbol gallery: a silent catalogue of the Tabler icons and the ISA-5.1 symbols.

Shows every vendored icon (explainer.icons) in a grid with its name, then the ISA symbols
(explainer.symbols) group by group with their names, the instrument bubbles, the line types,
and a small flow control loop joined with connect(). No narration: NARRATION holds the
length of each silent segment (seconds, from symbol_gallery_data.py).

Build (from the repo root):
    python projects/symbol_gallery/symbol_gallery.py --preview --qa   # -> tmp/symbol_gallery/
    python projects/symbol_gallery/symbol_gallery.py                  # -> output/symbol_gallery.mp4
"""
from explainer import *
from explainer.symbols import isa
import symbol_gallery_data as D

NARRATION = list(D.DURATIONS.values())          # silent segments (seconds)
SEG = {name: k + 1 for k, name in enumerate(D.DURATIONS)}
AUDIO_DIR = audio_dir_for(__file__)

NAME_SIZE = FS_TAG                              # names under icons and symbols
SYMBOL_SIZE = 1.4                               # ISA symbols in the group pages


def stubs(sym, length=0.35):
    """Short process pipes from a symbol's in/out ports, pointing away from its centre
    (none for in-line flow elements: they carry their own pipe stubs)."""
    out = VGroup()
    if "tap" in sym.port_names():
        return out
    for p in ("in", "out"):
        if p not in sym.port_names():
            continue
        a = sym.port(p)
        d = a - sym.get_center()
        d = RIGHT * np.sign(d[0]) if abs(d[0]) >= abs(d[1]) else UP * np.sign(d[1])
        out.add(Line(a, a + d * length, stroke_width=isa.PROCESS_STROKE, color=INK))
    return out


def named(drawing, name, buff=0.22):
    """VGroup(drawing, name below it)."""
    return VGroup(drawing, label(name, NAME_SIZE).next_to(drawing, DOWN, buff))


class SymbolGallery(SyncedScene):
    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        self.head = None

        # ---------------- title ----------------
        s = SEG["title"]
        title_card(self, "Symbol Gallery", "Tabler icons  ·  ISA-5.1 P&ID symbols",
                   series="explainer-videos  ·  catalogue")
        self.sync(self.end(s) - 0.7)
        self.clear()

        # ---------------- icons ----------------
        for k, page in enumerate(D.ICON_PAGES):
            s = SEG[f"icons_{k + 1}"]
            self.heading(f"Tabler icons  ({k + 1}/{len(D.ICON_PAGES)})")
            grid = icon_grid(page, cols=D.ICON_COLS, size=0.75, cell=(1.88, 1.4), name_size=16)
            fit(grid).move_to(DOWN * 0.2)
            self.play(LaggedStart(*[AnimationGroup(Create(c[0]), FadeIn(c[1]))
                                    for c in grid], lag_ratio=0.12), run_time=3.2)
            self.say(f"icon(name, color, size, stroke_width)  ·  Tabler {TABLER_VERSION}, MIT",
                     GREY_INK, size=FS_NOTE)
            self.sync(self.end(s) - 0.6)
            self.clear(self.head)

        # ---------------- ISA symbol groups ----------------
        for key, (group, items) in zip(("valves", "machines", "flow"), ISA_GROUPS.items()):
            s = SEG[key]
            self.heading(f"ISA-5.1  ·  {group}")
            cells = VGroup()
            for fn, name in items:
                sym = getattr(isa, fn)(size=SYMBOL_SIZE)
                cells.add(named(VGroup(sym, stubs(sym)), name))
            if len(cells) > 5:                          # two rows: equal columns
                cells.arrange_in_grid(cols=4, buff=(0.6, 0.7), cell_alignment=DOWN,
                                      col_widths=[max(c.width for c in cells)] * 4)
            else:
                cells.arrange(RIGHT, buff=0.6, aligned_edge=DOWN)
            fit(cells).move_to(DOWN * 0.1)
            self.play(LaggedStart(*[AnimationGroup(Create(c[0]), FadeIn(c[1], shift=UP * 0.1))
                                    for c in cells], lag_ratio=0.35), run_time=4.0)
            self.say("drawn in code  ·  each symbol has ports for signal lines", GREY_INK,
                     size=FS_NOTE)
            self.ports_flash(cells)
            self.sync(self.end(s) - 0.6)
            self.clear(self.head)

        # ---------------- instrument bubbles ----------------
        s = SEG["bubbles"]
        self.heading("ISA-5.1  ·  Instrument bubbles")
        cells = VGroup(*[named(instrument(f, n, loc, size=1.5), name)
                         for loc, f, n, name in D.BUBBLES])
        cells.arrange(RIGHT, buff=0.75, aligned_edge=UP)
        fit(cells).move_to(UP * 0.3)
        self.play(LaggedStart(*[AnimationGroup(Create(c[0]), FadeIn(c[1], shift=UP * 0.1))
                                for c in cells], lag_ratio=0.4), run_time=4.0)
        self.say("instrument(function, loop, location)  ·  letters above, loop number below",
                 GREY_INK, size=FS_NOTE)
        self.sync(self.end(s) - 0.6)
        self.clear(self.head)

        # ---------------- line types ----------------
        s = SEG["lines"]
        self.heading("ISA-5.1  ·  Line types")
        rows = VGroup()
        for kind, name in D.LINES:
            ln = signal_line([LEFT * 2.6, RIGHT * 2.6], kind)
            rows.add(VGroup(label(name, FS_LABEL), ln))
        for k, r in enumerate(rows):                # lines share a left edge: names end there
            r[1].move_to(RIGHT * 2.4 + DOWN * (k * 0.8))
            r[0].next_to(r[1], LEFT, 0.6)
        fit(rows).move_to(DOWN * 0.1)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), Create(r[1])) for r in rows],
                              lag_ratio=0.35), run_time=4.0)
        self.say("signal_line(points, kind)  ·  connect(a, port, b, port, kind, route)",
                 GREY_INK, size=FS_NOTE)
        self.sync(self.end(s) - 0.6)
        self.clear(self.head)

        # ---------------- example control loop ----------------
        self.control_loop(SEG["loop"])
        self.clear()

        # ---------------- end ----------------
        s = SEG["end"]
        lines = VGroup(mono("from explainer import *", FS_BODY, weight=BOLD),
                       mono("icon(\"gauge\", ACCENT_1, size=1.0)", FS_LABEL),
                       mono("v = control_valve();  v.port(\"actuator\")", FS_LABEL),
                       mono("connect(fic, \"right\", fy, \"left\", kind=\"electrical\")",
                            FS_LABEL))
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        fit(lines).move_to(UP * 0.3)
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in lines], lag_ratio=0.3),
                  run_time=2.0)
        self.sync(self.end(s) + 0.5)

    # ---------------- helpers ----------------
    def heading(self, text):
        self.head = section_title(self, text, prev=self.head)
        if self.head not in self.mobjects:
            self.add(self.head)

    def ports_flash(self, cells):
        """Show every port as a small dot for a moment."""
        dots = VGroup()
        for c in cells:
            sym = c[0][0]
            for p in sym.port_names():
                dots.add(Dot(sym.port(p), radius=0.06, color=ACCENT_2))
        self.play(FadeIn(dots), run_time=0.5)
        self.wait(1.2)
        self.play(FadeOut(dots), run_time=0.5)

    def control_loop(self, s):
        self.heading("Example  ·  flow control loop")
        k, y = 1.3, -1.25                            # symbol size, suction line height
        tk = tank(size=k)
        tk.shift(np.array([-5.4, y, 0]) - tk.port("outlet"))
        pump = centrifugal_pump(size=k)
        pump.shift(np.array([-3.3, y, 0]) - pump.port("in"))
        y2 = pump.port("out")[1]                     # discharge line height
        fe = orifice_plate(size=k)
        fe.shift(np.array([-1.3, y2, 0]) - fe.port("in"))
        fv = control_valve(size=k)
        fv.shift(np.array([2.5, y2, 0]) - fv.port("in"))
        ft = instrument(*D.LOOP_TAGS["FT"], "field", size=1.1)
        ft.move_to([fe.port("tap")[0], y2 + 1.75, 0])
        fy = instrument(*D.LOOP_TAGS["FY"], "field", size=1.1)
        fy.move_to([fv.port("actuator")[0], y2 + 3.0, 0])
        fic = instrument(*D.LOOP_TAGS["FIC"], "dcs", size=1.1)
        fic.move_to([(ft.get_x() + fy.get_x()) / 2, fy.get_y(), 0])

        # process
        p1 = connect(tk, "outlet", pump, "in", kind="process")
        p2 = connect(pump, "out", fe, "in", kind="process")
        p3 = connect(fe, "out", fv, "in", kind="process")
        p4 = signal_line([fv.port("out"), fv.port("out") + RIGHT * 1.9], "process", arrow=True)
        self.play(Create(tk), run_time=0.8)
        self.play(Create(p1), Create(pump), run_time=0.9)
        self.play(Create(p2), Create(fe), run_time=0.8)
        self.play(Create(p3), Create(fv), Create(p4), run_time=1.0)
        names = VGroup(
            label("Tank", NAME_SIZE).next_to(tk, DOWN, 0.2),
            label("Pump", NAME_SIZE).next_to(pump, DOWN, 0.2),
            label("Orifice plate FE-{}".format(D.LOOP_TAGS["FE"][1]), NAME_SIZE)
            .next_to(fe, DOWN, 0.25),
            label("Control valve FV-101", NAME_SIZE).next_to(fv, DOWN, 0.25),
        )
        self.play(FadeIn(names), run_time=0.5)
        self.say("Process: tank → pump → flow element → control valve", GREY_INK,
                 size=FS_NOTE)
        self.sync(self.at(s, 0.3))

        # measurement -> controller -> I/P -> valve
        c1 = connect(fe, "tap", ft, "bottom", kind="connection")
        c2 = connect(ft, "right", fic, "bottom", kind="electrical", route="hv")
        c3 = connect(fic, "right", fy, "left", kind="electrical")
        c4 = connect(fy, "bottom", fv, "actuator", kind="pneumatic", spacing=0.55,
                     end_gap=0.25)
        tags = VGroup(
            label("Flow transmitter", NAME_SIZE).next_to(ft, LEFT, 0.25),
            label("Flow controller (DCS)", NAME_SIZE).next_to(fic, LEFT, 0.25),
            label("I/P converter", NAME_SIZE).next_to(fy, RIGHT, 0.25),
        )
        self.play(Create(c1), Create(ft), FadeIn(tags[0]), run_time=1.0)
        self.say(f"FT-101 measures the flow: {D.SIGNAL} (electrical) to the controller",
                 GREY_INK, size=FS_NOTE)
        self.play(Create(c2), Create(fic), FadeIn(tags[1]), run_time=1.2)
        self.sync(self.at(s, 0.55))
        self.say("FIC-101 in the DCS drives FY-101 (electrical), which moves FV-101 (pneumatic)",
                 GREY_INK, size=FS_NOTE)
        self.play(Create(c3), Create(fy), FadeIn(tags[2]), run_time=1.0)
        self.play(Create(c4), run_time=1.0)
        self.sync(self.at(s, 0.75))

        # legend of the line types used
        legend = VGroup()
        for kind in ("process", "connection", "electrical", "pneumatic"):
            legend.add(VGroup(signal_line([LEFT * 0.6, RIGHT * 0.6], kind, spacing=0.6,
                                          end_gap=0.25),
                              label(kind, FS_TAG, GREY_INK)).arrange(RIGHT, buff=0.2))
        legend.arrange_in_grid(cols=2, buff=(0.6, 0.25), cell_alignment=LEFT)
        legend.next_to(names[3], DOWN, 0.3).align_to(p4, RIGHT)
        self.play(FadeIn(legend), run_time=0.6)
        self.sync(self.end(s) - 0.6)


if __name__ == "__main__":
    main(__file__, "SymbolGallery", NARRATION)
