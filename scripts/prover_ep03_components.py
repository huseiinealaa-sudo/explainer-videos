"""Daniel Compact Prover series, episode 3: compact prover construction (10 components).

The component list and every number come from prover_demo_data (owner-approved
list in CLAUDE.md, sources in sources/prover_ep03.md). The diagram is a simplified
side view after the Daniel manual 3-9008-701 Rev J, Figs 1-1 and 3-1: flanges at the
front (right), hydraulic and optical parts at the back (left).

Build (from the repo root):
    python scripts/prover_ep03_components.py --preview   # 480p15 -> tmp/prover_ep03_components/preview.mp4
    python scripts/prover_ep03_components.py             # 1080p30 -> output/prover_ep03_components.mp4
"""
import argparse

from style import *
import prover_demo_data as D

# Fully diacritized narration — one entry per scene.
NARRATION = [
    # 1 intro
    "فِي الحَلْقَةِ السَّابِقَةِ عَرَفْنَا الشَّوْطَ وَالجَوْلَةَ، وَكَيْفَ نَحْكُمُ عَلَى تَكْرَارِيَّةِ الإِثْبَاتِ. وَفِي هٰذِهِ الحَلْقَةِ نَفْتَحُ المُعَايِرَ المُدْمَجَ، وَنَتَعَرَّفُ عَلَى مُكَوِّنَاتِهِ الرَّئِيسِيَّةِ العَشَرَةِ: اسْمِ كُلٍّ مِنْهَا، وَمَوْقِعِهِ، وَوَظِيفَتِهِ.",
    # 2 layout + component 1 (end connections)
    "نَرْسُمُ المُعَايِرَ مِنَ الأَمَامِ إِلَى الخَلْفِ، فِي ثَلَاثِ مَجْمُوعَاتٍ: مَسَارِ السَّائِلِ، ثُمَّ مَنْظُومَةِ الحَرَكَةِ، ثُمَّ مَنْظُومَةِ القِيَاسِ. فِي الأَمَامِ، المُكَوِّنُ الأَوَّلُ: شَفَتَا الدُّخُولِ وَالخُرُوجِ، تُرَكِّبَانِ المُعَايِرَ عَلَى خَطِّ التَّشْغِيلِ. وَفِي شَفَةِ الخُرُوجِ مَصَدٌّ لِلْأَمَانِ، يَمْنَعُ انْسِدَادَ التَّدَفُّقِ عَرَضًا.",
    # 3 component 2 (flow tube)
    "الثَّانِي: أُنْبُوبُ التَّدَفُّقِ، مِنَ الفُولَاذِ المُقَاوِمِ لِلصَّدَأِ، وَسَطْحُهُ الدَّاخِلِيُّ مَشْغُولٌ بِدِقَّةٍ وَمَطْلِيٌّ بِالكُرُومِ الصُّلْبِ. فِيهِ يَدْخُلُ السَّائِلُ مِنَ الخَلْفِ وَيَخْرُجُ مِنَ الأَمَامِ، وَهُوَ يَحْتَوِي المِكْبَسَ، وَالصِّمَامَ، وَآلِيَّةَ الأَمَانِ.",
    # 4 components 3-4 (piston, poppet)
    "الثَّالِثُ: مِكْبَسُ القِيَاسِ، مِكْبَسٌ حُرٌّ يَتَحَرَّكُ مَعَ السَّائِلِ، فَيُزِيحُ الحَجْمَ الأَسَاسِيَّ فِي كُلِّ شَوْطٍ. وَعَلَيْهِ مَوَانِعُ تَسَرُّبٍ تَمْنَعُ السَّائِلَ مِنْ تَجَاوُزِهِ، وَحَلَقَاتٌ مِنْ مَادَّةِ رُولُون. وَالرَّابِعُ: صِمَامُ بُوبِت، دَاخِلَ المِكْبَسِ نَفْسِهِ. حِينَ يَكُونُ مَفْتُوحًا يَمُرُّ السَّائِلُ عَبْرَ المِكْبَسِ، وَحِينَ يُغْلَقُ يَدْفَعُ السَّائِلُ المِكْبَسَ أَمَامَهُ.",
    # 5 components 5-6 (plenum, hydraulic cylinder)
    "ثُمَّ مَنْظُومَةُ الحَرَكَةِ. الخَامِسُ: بْلِينَم النَّابِضِ الهَوَائِيِّ، شِحْنَةٌ مِنَ النِّيتْرُوجِينِ الجَافِّ المَضْغُوطِ، تُعْطِي الطَّاقَةَ اللَّازِمَةَ لِإِغْلَاقِ الصِّمَامِ، وَلِلتَّغَلُّبِ عَلَى احْتِكَاكِ مَوَانِعِ التَّسَرُّبِ. وَالسَّادِسُ: الأُسْطُوَانَةُ الهِيدْرُولِيكِيَّةُ. فِيهَا مِكْبَسُ المُشَغِّلِ، يَفْصِلُ بَيْنَ الغَازِ وَالزَّيْتِ، وَيَتَّصِلُ بِالصِّمَامِ عَبْرَ عَمُودِ المُشَغِّلِ، فَيُوَفِّرُ قُوَى فَتْحِهِ وَإِغْلَاقِهِ.",
    # 6 components 7-8 (control valve, pump)
    "السَّابِعُ: صِمَامُ التَّحَكُّمِ الهِيدْرُولِيكِيِّ، صِمَامٌ مُغْلَقٌ فِي وَضْعِهِ الطَّبِيعِيِّ، يُفْتَحُ أَثْنَاءَ الشَّوْطِ، وَيُغْلَقُ لِإِعَادَةِ المِكْبَسِ. وَالثَّامِنُ: المِضَخَّةُ الهِيدْرُولِيكِيَّةُ وَمُحَرِّكُهَا الكَهْرَبَائِيُّ، مَعَ خَزَّانِ الزَّيْتِ. تَتَغَلَّبُ عَلَى ضَغْطِ البْلِينَم فَتُعِيدُ المِكْبَسَ إِلَى وَضْعِ الانْتِظَارِ، ثُمَّ تَحْفَظُ الضَّغْطَ دُونَ تَدَفُّقٍ، تَوْفِيرًا لِلطَّاقَةِ.",
    # 7 component 9 (optical assembly)
    "وَأَخِيرًا مَنْظُومَةُ القِيَاسِ. التَّاسِعُ: المَجْمُوعَةُ البَصَرِيَّةُ، وَفِيهَا ثَلَاثَةُ مَفَاتِيحَ بَصَرِيَّةٍ: وَاحِدٌ لِوَضْعِ الانْتِظَارِ، وَاثْنَانِ يُحَدِّدَانِ الحَجْمَ الأَسَاسِيَّ، وَهُمَا الكَاشِفَانِ دِي وَنْ وَدِي تُو فِي الحَلْقَتَيْنِ السَّابِقَتَيْنِ. وَيَمُرُّ بَيْنَهَا عَلَمٌ مُثَبَّتٌ بِالمِكْبَسِ عَبْرَ عَمُودِ الكَاشِفِ، فَيَحْجُبُ الضَّوْءَ وَيُوَلِّدُ الإِشَارَةَ. وَتُثَبَّتُ المَسَافَةُ بَيْنَ المَفَاتِيحِ بِقُضْبَانٍ مِنْ سَبِيكَةِ إِنْفَار، الَّتِي تَكَادُ لَا تَتَمَدَّدُ بِالحَرَارَةِ.",
    # 8 component 10 (interface enclosure)
    "العَاشِرُ: صُنْدُوقُ الوَاجِهَةِ، فِيهِ لَوْحَةٌ إِلِكْتْرُونِيَّةٌ تُهَيِّئُ إِشَارَاتِ المُعَايِرِ، وَتُرْسِلُهَا إِلَى الحَاسِبَةِ، الَّتِي تُعَالِجُ بَيَانَاتِ الأَشْوَاطِ وَتُلَخِّصُهَا.",
    # 9 summary + next
    "الخُلَاصَةُ: مَسَارٌ لِلسَّائِلِ فِيهِ مِكْبَسٌ بِصِمَامٍ دَاخِلِيٍّ، تُحَرِّكُهُ مَنْظُومَةٌ هَوَائِيَّةٌ وَهِيدْرُولِيكِيَّةٌ، وَتَرْصُدُهُ مَنْظُومَةٌ بَصَرِيَّةٌ. فِي الحَلْقَةِ القَادِمَةِ: كَيْفَ تَعْمَلُ هٰذِهِ المُكَوِّنَاتُ مَعًا فِي دَوْرَةِ العَمَلِ بِمَرَاحِلِهَا الخَمْسِ، وَلِمَاذَا لَا يَنْقَطِعُ التَّدَفُّقُ.",
]

# Every spoken number is checked against prover_demo_data; stop if it drifts.
assert len(D.PROVER_COMPONENTS) == 10                         # seg 1 "ten main components"
assert D.OPTICAL_SWITCH_COUNT == 3                            # seg 7 "three optical switches"
assert D.VOLUME_SWITCH_COUNT == 2                             # seg 7 "two define the base volume"
assert D.OPTICAL_SWITCH_COUNT - D.VOLUME_SWITCH_COUNT == 1    # seg 7 "one for standby"
assert len(D.CYCLE_STAGES) == 5                               # seg 9 "five stages"

AUDIO_DIR = BUILD_DIR / "prover_ep03_components" / "audio"

FLUID_C = "#1f5fa8"             # group 1: fluid path (prover blue, as in episodes 1-2)
DRIVE_C = "#c25a12"             # group 2: drive system
MEAS_C = "#2e7d32"              # group 3: measurement and signals
GROUPS = [("Fluid path", FLUID_C, range(0, 4)),
          ("Drive system", DRIVE_C, range(4, 8)),
          ("Measurement & signals", MEAS_C, range(8, 10))]

# Diagram geometry (x: back = left, front = right)
TUBE_L, TUBE_R, TUBE_Y, TUBE_H = -1.8, 3.4, 0.45, 1.3
PIPE_Y = -1.15                  # inlet pipe under the flow tube
ENTRY_X = -1.35                 # inlet elbow into the upstream end of the tube
PISTON_X = -0.8                 # standby position
FLANGE_X = 4.3                  # inlet/outlet line flanges
CYL_L, CYL_R, CYL_H = -4.9, -2.8, 0.62
ACT_X = -3.6                    # actuator piston
BAR_L, BAR_R, BAR_Y = -6.0, -3.0, 1.7
SHAFT_Y = 1.25                  # detector shaft height
SW_X = {"STBY": -5.6, "D1": -4.5, "D2": -3.4}
VALVE_X = -3.15
CAPTION_Y = -2.75


def label(text, size=FS_LABEL, color=INK, **kw):
    return Text(text, font_size=size, color=color, **kw)


def fit(mob, width=13.2):
    """Keep a group inside the 16:9 frame with a side margin."""
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def pipe(points, width=16):
    """Whiteboard pipe: a thick ink stroke with a white core."""
    path = VMobject().set_points_as_corners([np.array([x, y, 0]) for x, y in points])
    outer = path.copy().set_stroke(INK, width)
    inner = path.copy().set_stroke(BG, width - 7)
    return VGroup(outer, inner)


def badge(n, color, pos):
    c = Circle(radius=0.2, stroke_width=3, color=color, fill_color=BG, fill_opacity=1)
    t = label(str(n), FS_TAG, color, weight=BOLD).move_to(c)
    return VGroup(c, t).move_to(pos)


def group_of(i):
    for name, color, idx in GROUPS:
        if i in idx:
            return name, color


class ProverEp03(SyncedScene):
    def construct(self):
        START = segment_starts(AUDIO_DIR, len(NARRATION))

        def at(seg, frac):
            """Absolute time at a fraction of narration segment `seg` (1-based)."""
            return START[seg - 1] + frac * (START[seg] - START[seg - 1])

        def cue(seg, phrase):
            """Time at which `phrase` starts in segment `seg` (by text position)."""
            text = NARRATION[seg - 1]
            i = text.find(phrase)
            assert i >= 0, (seg, phrase)
            return at(seg, i / len(text))

        # ---------------- Segment 1: title ----------------
        series = label("Daniel Compact Prover  ·  Episode 3", FS_SUBTITLE, GREY_INK)
        title = Text("Compact Prover Construction", font_size=FS_TITLE - 4, weight=BOLD)
        fit(title, 12.6)
        line = Line(LEFT, RIGHT).set_width(title.width)
        sub = label(f"The {len(D.PROVER_COMPONENTS)} main components: name, location, function",
                    FS_BODY, GREY_INK)
        fit(sub, 12.6)
        head = VGroup(series, title, line, sub).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        prev = label("Previously: pass, run, repeatability", FS_LABEL, GREY_INK)
        prev.move_to(DOWN * 2.6)

        self.play(FadeIn(series, shift=DOWN * 0.2), run_time=1.0)
        self.play(FadeIn(prev), run_time=0.8)
        self.sync(cue(1, "وَفِي هٰذِهِ"))
        self.play(Write(title), Create(line), run_time=2.0)
        self.sync(cue(1, "العَشَرَةِ"))
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=1.0)
        self.sync(START[1] - 0.8)
        corner = label("Ep 3 · Construction", FS_BODY - 6, weight=BOLD).to_corner(UL, buff=0.4)
        self.play(FadeOut(VGroup(series, line, sub, prev)), Transform(title, corner),
                  run_time=0.8)

        # ---------------- Diagram parts ----------------
        # 1 End connections (front)
        out_pipe = pipe([(TUBE_R, TUBE_Y), (5.0, TUBE_Y)])
        in_pipe = pipe([(5.0, PIPE_Y), (ENTRY_X, PIPE_Y), (ENTRY_X, TUBE_Y - TUBE_H / 2)])
        flanges = VGroup(*[Rectangle(width=0.22, height=h, stroke_width=4, color=INK,
                                     fill_color=BG, fill_opacity=1).move_to([x, y, 0])
                           for x, y, h in ((TUBE_R + 0.11, TUBE_Y, TUBE_H + 0.35),
                                           (FLANGE_X, PIPE_Y, 0.85), (FLANGE_X, TUBE_Y, 0.85))])
        stop = Line([TUBE_R - 0.05, TUBE_Y - 0.35, 0], [TUBE_R - 0.05, TUBE_Y + 0.35, 0],
                    stroke_width=7, color=FLUID_C)
        stop_lbl = label("positive stop", FS_TAG, FLUID_C).next_to(flanges[0], UP, 0.12)
        out_arrow = Arrow([5.1, TUBE_Y, 0], [6.3, TUBE_Y, 0], buff=0, stroke_width=4,
                          color=GREY_INK, max_tip_length_to_length_ratio=0.3)
        in_arrow = Arrow([6.3, PIPE_Y, 0], [5.1, PIPE_Y, 0], buff=0, stroke_width=4,
                         color=GREY_INK, max_tip_length_to_length_ratio=0.3)
        out_lbl = label("OUTLET", FS_TAG, GREY_INK, weight=BOLD).next_to(out_arrow, DOWN, 0.1)
        in_lbl = label("INLET", FS_TAG, GREY_INK, weight=BOLD).next_to(in_arrow, DOWN, 0.1)
        front = label("FRONT →", FS_TAG, GREY_INK).move_to([5.7, 3.1, 0])
        back = label("← BACK", FS_TAG, GREY_INK).move_to([-1.0, 3.1, 0])
        c1 = VGroup(out_pipe, in_pipe, flanges, out_arrow, in_arrow, out_lbl, in_lbl)

        # 2 Flow tube
        tube = Rectangle(width=TUBE_R - TUBE_L, height=TUBE_H, stroke_width=5, color=INK)
        tube.move_to([(TUBE_L + TUBE_R) / 2, TUBE_Y, 0])
        cap = Rectangle(width=0.2, height=TUBE_H + 0.35, stroke_width=4, color=INK)
        cap.move_to([TUBE_L - 0.1, TUBE_Y, 0])
        bore = DashedLine([TUBE_L + 0.2, TUBE_Y - TUBE_H / 2 + 0.08, 0],
                          [TUBE_R - 0.2, TUBE_Y - TUBE_H / 2 + 0.08, 0], stroke_width=2,
                          color=GREY_INK)
        tube_flow = VGroup(*[Arrow([x, TUBE_Y - 0.3, 0], [x + 0.7, TUBE_Y - 0.3, 0], buff=0,
                                   stroke_width=3, color=FLUID_C,
                                   max_tip_length_to_length_ratio=0.3) for x in (0.4, 1.8)])
        entry_flow = Arrow([ENTRY_X, PIPE_Y + 0.1, 0], [ENTRY_X, TUBE_Y - 0.75, 0], buff=0,
                           stroke_width=3, color=FLUID_C, max_tip_length_to_length_ratio=0.3)
        c2 = VGroup(tube, cap)

        # 3 Measurement piston (+ seals, Rulon riders) and 4 poppet valve
        piston = Rectangle(width=0.42, height=TUBE_H - 0.1, stroke_width=4, color=INK,
                           fill_color=INK, fill_opacity=0.15).move_to([PISTON_X, TUBE_Y, 0])
        seals = VGroup(*[Line([PISTON_X + dx, TUBE_Y + s * (TUBE_H / 2 - 0.05), 0],
                              [PISTON_X + dx, TUBE_Y + s * (TUBE_H / 2 - 0.2), 0],
                              stroke_width=6, color=FLUID_C)
                         for dx in (-0.12, 0.12) for s in (1, -1)])
        riders_lbl = label("seals · Rulon riders", FS_TAG, FLUID_C)
        riders_lbl.move_to([PISTON_X + 0.75, TUBE_Y + TUBE_H / 2 + 0.25, 0])
        gap_h = 0.38
        poppet_open = Rectangle(width=0.44, height=gap_h, stroke_width=0, fill_color=BG,
                                fill_opacity=1).move_to(piston)
        poppet = Polygon([PISTON_X + 0.05, TUBE_Y + gap_h / 2, 0],
                         [PISTON_X + 0.34, TUBE_Y + 0.1, 0], [PISTON_X + 0.34, TUBE_Y - 0.1, 0],
                         [PISTON_X + 0.05, TUBE_Y - gap_h / 2, 0], stroke_width=3,
                         color=INK, fill_color=FLUID_C, fill_opacity=0.6)
        poppet.shift(RIGHT * 0.32)                 # open: pulled downstream of the piston
        c3 = VGroup(piston, seals)

        # 5 Pneumatic spring plenum (tank on top)
        tank = RoundedRectangle(width=4.0, height=0.62, corner_radius=0.3, stroke_width=4,
                                color=INK).move_to([0.9, 2.0, 0])
        n2 = label("N₂", FS_LABEL, DRIVE_C, weight=BOLD).move_to(tank)

        # 6 Hydraulic cylinder: actuator piston + actuator shaft
        cyl = Rectangle(width=CYL_R - CYL_L, height=CYL_H, stroke_width=4, color=INK)
        cyl.move_to([(CYL_L + CYL_R) / 2, TUBE_Y, 0])
        act = Rectangle(width=0.14, height=CYL_H - 0.06, stroke_width=0, fill_color=DRIVE_C,
                        fill_opacity=1).move_to([ACT_X, TUBE_Y, 0])
        gas_t = label("gas", FS_TAG - 4, GREY_INK).move_to([(CYL_L + ACT_X) / 2, TUBE_Y + 0.16, 0])
        oil_t = label("oil", FS_TAG - 4, GREY_INK).move_to([(ACT_X + CYL_R) / 2, TUBE_Y + 0.16, 0])
        a_shaft = Line([ACT_X + 0.07, TUBE_Y, 0], [PISTON_X + 0.05, TUBE_Y, 0], stroke_width=4,
                       color=DRIVE_C)
        shaft_lbl = label("actuator shaft", FS_TAG, DRIVE_C).move_to([-2.3, TUBE_Y + 0.95, 0])
        c6 = VGroup(cyl, act, gas_t, oil_t, a_shaft)

        # 7 Hydraulic control valve and 8 pump & motor + reservoir
        vpos = np.array([VALVE_X, -0.45, 0])
        valve = VGroup(Polygon(vpos + [-0.3, 0.2, 0], vpos + [0, 0, 0], vpos + [-0.3, -0.2, 0]),
                       Polygon(vpos + [0.3, 0.2, 0], vpos + [0, 0, 0], vpos + [0.3, -0.2, 0])
                       ).set_stroke(INK, 3)
        v_line = Line(vpos + [0, 0.2, 0], [VALVE_X, TUBE_Y - CYL_H / 2, 0], stroke_width=3,
                      color=DRIVE_C)
        nc = label("N.C.", FS_TAG - 4, GREY_INK).next_to(valve, LEFT, 0.15)
        ppos = np.array([-4.6, -1.3, 0])
        pump = VGroup(Circle(radius=0.34, stroke_width=4, color=INK).move_to(ppos),
                      Triangle(stroke_width=0, fill_color=INK, fill_opacity=1).scale(0.12)
                      .move_to(ppos + [0, 0.18, 0]))
        motor = VGroup(Rectangle(width=0.7, height=0.5, stroke_width=4, color=INK),
                       label("M", FS_TAG, INK, weight=BOLD)).move_to(ppos + [-0.95, 0, 0])
        res = VGroup(Rectangle(width=0.95, height=0.55, stroke_width=4, color=INK),
                     label("oil", FS_TAG - 4, GREY_INK)).move_to([-2.95, -1.8, 0])
        p_lines = VGroup(
            VMobject().set_points_as_corners([ppos + [0.34, 0, 0], [VALVE_X, -1.3, 0],
                                              vpos + [0, -0.2, 0]]),
            VMobject().set_points_as_corners([ppos + [0, -0.34, 0], [-4.6, -1.8, 0],
                                              [-3.42, -1.8, 0]]),
        ).set_stroke(DRIVE_C, 3)
        c7 = VGroup(valve, v_line, nc)
        c8 = VGroup(pump, motor, res, p_lines)

        # 9 Optical assembly: switch bar on Invar rods, 3 slotted switches, flag, detector shaft
        rods = VGroup(*[Line([BAR_L, BAR_Y + dy, 0], [BAR_R, BAR_Y + dy, 0], stroke_width=3,
                             color=MEAS_C) for dy in (-0.22, 0.22)])
        rods_lbl = label("Invar rods", FS_TAG, MEAS_C).next_to(rods, RIGHT, 0.15)
        switches, sw_lbls = VGroup(), VGroup()
        for name, x in SW_X.items():
            sw = VGroup(Rectangle(width=0.1, height=0.3, stroke_width=0, fill_color=INK,
                                  fill_opacity=1).move_to([x - 0.09, BAR_Y, 0]),
                        Rectangle(width=0.1, height=0.3, stroke_width=0, fill_color=INK,
                                  fill_opacity=1).move_to([x + 0.09, BAR_Y, 0]))
            switches.add(sw)
            sw_lbls.add(label(name, FS_TAG, INK if name == "STBY" else MEAS_C,
                              weight=BOLD).move_to([x, BAR_Y + 0.5, 0]))
        flag_x = ValueTracker(SW_X["STBY"])
        flag = always_redraw(lambda: Line([flag_x.get_value(), SHAFT_Y, 0],
                                          [flag_x.get_value(), BAR_Y + 0.12, 0],
                                          stroke_width=5, color=MEAS_C))
        d_shaft = always_redraw(lambda: Line(            # stub: moves with the piston
            [flag_x.get_value(), SHAFT_Y, 0], [flag_x.get_value() + 1.2, SHAFT_Y, 0],
            stroke_width=4, color=MEAS_C))
        c9 = VGroup(rods, switches, sw_lbls)

        # 10 Interface enclosure
        box = VGroup(Rectangle(width=1.1, height=0.8, stroke_width=4, color=INK),
                     Rectangle(width=0.7, height=0.35, stroke_width=2, color=MEAS_C)
                     ).move_to([-6.35, -0.35, 0])
        sig = DashedLine([BAR_L, BAR_Y, 0], [-6.35, BAR_Y, 0], stroke_width=3, color=MEAS_C)
        sig2 = DashedLine([-6.35, BAR_Y, 0], [-6.35, 0.05, 0], stroke_width=3, color=MEAS_C)
        to_pc = Arrow([-6.35, -0.75, 0], [-6.35, -1.7, 0], buff=0, stroke_width=4,
                      color=MEAS_C, max_tip_length_to_length_ratio=0.25)
        pc = label("computer", FS_TAG, MEAS_C).next_to(to_pc, DOWN, 0.08)
        c10 = VGroup(box, sig, sig2)

        badge_pos = [(FLANGE_X, -0.35), (2.9, -0.45), (PISTON_X - 0.05, -0.45),
                     (PISTON_X + 0.85, -0.45), (3.25, 2.0), (CYL_L - 0.35, TUBE_Y),
                     (VALVE_X + 0.6, -0.45), (-4.05, -0.8), (BAR_L - 0.45, BAR_Y + 0.5),
                     (-5.45, -0.35)]
        badges = [badge(i + 1, group_of(i)[1], [x, y, 0]) for i, (x, y) in enumerate(badge_pos)]

        caption = VMobject()

        def show_caption(i, note):
            nonlocal caption
            gname, color = group_of(i)
            head = label(f"{i + 1}  {D.PROVER_COMPONENTS[i]}", FS_BODY, color, weight=BOLD)
            tag = label(gname, FS_TAG, GREY_INK)
            first = VGroup(head, tag).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
            txt = label(note, FS_LABEL, INK)
            new = fit(VGroup(first, txt).arrange(DOWN, buff=0.14)).move_to([0, CAPTION_Y, 0])
            if len(caption.submobjects):
                self.play(FadeOut(caption), run_time=0.3)
            self.play(FadeIn(new, shift=UP * 0.1), run_time=0.45)
            caption = new

        # ---------------- Segment 2: layout + 1 end connections ----------------
        groups = VGroup(*[label(f"{k + 1}. {name}", FS_BODY, color, weight=BOLD)
                          for k, (name, color, _) in enumerate(GROUPS)])
        groups.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.3)
        g_head = label("Front → back, in three groups", FS_HEADING - 6, weight=BOLD)
        g_head.move_to(UP * 2.2)

        self.play(Write(g_head), run_time=1.0)
        for k, phrase in enumerate(("مَسَارِ", "مَنْظُومَةِ الحَرَكَةِ", "مَنْظُومَةِ القِيَاسِ")):
            self.sync(cue(2, phrase))
            self.play(FadeIn(groups[k], shift=RIGHT * 0.15), run_time=0.6)
        self.sync(cue(2, "فِي الأَمَامِ") - 0.2)
        self.play(FadeOut(g_head), FadeOut(groups), run_time=0.5)
        self.play(FadeIn(front), FadeIn(back), Create(c1[0]), Create(c1[1]), run_time=1.2)
        self.play(FadeIn(flanges), GrowArrow(out_arrow), GrowArrow(in_arrow), FadeIn(out_lbl),
                  FadeIn(in_lbl), FadeIn(badges[0]), run_time=0.9)
        show_caption(0, "Install the prover in the line")
        self.sync(cue(2, "وَفِي شَفَةِ"))
        self.play(Create(stop), FadeIn(stop_lbl), run_time=0.8)
        show_caption(0, "Positive stop in the outlet flange: flow is never blocked")

        # ---------------- Segment 3: 2 flow tube ----------------
        self.sync(START[2])
        self.play(FadeOut(stop_lbl), Create(tube), Create(cap), FadeIn(badges[1]), run_time=1.2)
        show_caption(1, "Stainless steel, precision-machined, hard-chrome bore")
        self.play(Create(bore), run_time=0.6)
        self.sync(cue(3, "فِيهِ يَدْخُلُ"))
        self.play(GrowArrow(entry_flow), run_time=0.6)
        self.play(LaggedStart(*[GrowArrow(a) for a in tube_flow], lag_ratio=0.4), run_time=1.0)
        self.sync(cue(3, "وَهُوَ يَحْتَوِي"))
        show_caption(1, "Contains the piston, the poppet valve and the fail-safe")

        # ---------------- Segment 4: 3 piston, 4 poppet valve ----------------
        self.sync(START[3])
        self.play(FadeIn(piston), FadeIn(badges[2]), run_time=0.8)
        show_caption(2, "Free piston: moves with the liquid, sweeps the base volume")
        self.sync(cue(4, "وَعَلَيْهِ"))
        self.play(Create(seals), FadeIn(riders_lbl), run_time=0.8)
        show_caption(2, "Seals stop liquid bypassing it  ·  Rulon riders")
        self.sync(cue(4, "وَالرَّابِعُ"))
        self.play(FadeOut(riders_lbl), FadeIn(poppet_open), FadeIn(poppet), FadeIn(badges[3]),
                  run_time=0.8)
        show_caption(3, "Valve inside the piston")
        self.sync(cue(4, "حِينَ يَكُونُ"))
        through = Arrow([PISTON_X - 0.9, TUBE_Y, 0], [PISTON_X + 1.1, TUBE_Y, 0], buff=0,
                        stroke_width=4, color=FLUID_C, max_tip_length_to_length_ratio=0.15)
        state = label("OPEN: liquid flows through the piston", FS_TAG, FLUID_C, weight=BOLD)
        state.move_to([1.3, TUBE_Y + 0.25, 0])
        self.play(GrowArrow(through), FadeIn(state), run_time=0.8)
        self.sync(cue(4, "وَحِينَ يُغْلَقُ"))
        closed_state = label("CLOSED: liquid pushes the piston", FS_TAG, FLUID_C, weight=BOLD)
        closed_state.move_to(state)
        push = Arrow([PISTON_X - 1.0, TUBE_Y + 0.35, 0], [PISTON_X - 0.3, TUBE_Y + 0.35, 0],
                     buff=0, stroke_width=4, color=FLUID_C, max_tip_length_to_length_ratio=0.3)
        self.play(FadeOut(through), poppet.animate.shift(LEFT * 0.32), FadeOut(poppet_open),
                  Transform(state, closed_state), GrowArrow(push), run_time=1.0)
        self.sync(START[4] - 1.2)
        self.play(FadeOut(push), FadeOut(state), poppet.animate.shift(RIGHT * 0.32),
                  FadeIn(poppet_open), run_time=0.8)
        self.bring_to_front(poppet)

        # ---------------- Segment 5: 5 plenum, 6 hydraulic cylinder ----------------
        self.sync(START[4])
        self.play(Create(tank), FadeIn(badges[4]), run_time=1.0)
        show_caption(4, "Pneumatic spring")
        self.sync(cue(5, "شِحْنَةٌ"))
        self.play(Write(n2), run_time=0.6)
        show_caption(4, "Dry nitrogen charge")
        self.sync(cue(5, "تُعْطِي"))
        show_caption(4, "Energy to close the poppet and overcome seal friction")
        self.sync(cue(5, "وَالسَّادِسُ"))
        self.play(Create(cyl), FadeIn(badges[5]), run_time=1.0)
        show_caption(5, "Hydraulic cylinder with the actuator piston")
        self.sync(cue(5, "يَفْصِلُ"))
        self.play(FadeIn(act), FadeIn(gas_t), FadeIn(oil_t), run_time=0.8)
        show_caption(5, "Actuator piston: barrier between gas and oil")
        self.sync(cue(5, "وَيَتَّصِلُ"))
        self.play(Create(a_shaft), FadeIn(shaft_lbl), run_time=1.0)
        self.sync(cue(5, "فَيُوَفِّرُ"))
        show_caption(5, "Actuator shaft: forces to open and close the poppet")
        self.sync(START[5] - 0.6)
        self.play(FadeOut(shaft_lbl), run_time=0.4)

        # ---------------- Segment 6: 7 control valve, 8 pump ----------------
        self.play(Create(valve), Create(v_line), FadeIn(badges[6]), run_time=1.0)
        self.play(FadeIn(nc), run_time=0.4)
        show_caption(6, "Normally closed: open during a pass, closed for the return")
        self.sync(cue(6, "وَالثَّامِنُ"))
        self.play(Create(pump), FadeIn(motor), FadeIn(res), FadeIn(badges[7]), run_time=1.0)
        self.play(Create(p_lines), run_time=0.8)
        show_caption(7, "Pump & motor, with the oil reservoir")
        self.sync(cue(6, "تَتَغَلَّبُ"))
        show_caption(7, "Overcomes the plenum pressure to return the piston")
        self.sync(cue(6, "ثُمَّ تَحْفَظُ"))
        show_caption(7, "Then holds the pressure at no flow, to save power")

        # ---------------- Segment 7: 9 optical assembly ----------------
        self.sync(START[6])
        self.play(Create(rods), FadeIn(badges[8]), run_time=0.8)
        show_caption(8, f"{D.OPTICAL_SWITCH_COUNT} slotted optical switches")
        self.sync(cue(7, "وَفِيهَا"))
        self.play(LaggedStart(*[FadeIn(s) for s in switches], lag_ratio=0.4), run_time=1.0)
        self.sync(cue(7, "وَاحِدٌ"))
        self.play(FadeIn(sw_lbls[0]), run_time=0.5)
        self.sync(cue(7, "وَاثْنَانِ"))
        self.play(FadeIn(sw_lbls[1:]), run_time=0.6)
        show_caption(8, f"1 standby switch  +  {D.VOLUME_SWITCH_COUNT} volume switches (D1, D2)")
        self.sync(cue(7, "وَيَمُرُّ"))
        self.add(d_shaft, flag)
        self.play(Create(d_shaft), run_time=0.01)
        show_caption(8, "Flag on the detector shaft, attached to the piston")
        self.play(flag_x.animate.set_value(SW_X["D1"]), piston.animate.shift(RIGHT * 1.1),
                  seals.animate.shift(RIGHT * 1.1), poppet.animate.shift(RIGHT * 1.1),
                  poppet_open.animate.shift(RIGHT * 1.1), run_time=1.6)
        self.play(Flash([SW_X["D1"], BAR_Y, 0], color=MEAS_C, line_length=0.25), run_time=0.7)
        self.sync(cue(7, "فَيَحْجُبُ"))
        show_caption(8, "The flag blocks the light  →  a signal")
        self.sync(cue(7, "وَتُثَبَّتُ"))
        self.play(flag_x.animate.set_value(SW_X["STBY"]), piston.animate.shift(LEFT * 1.1),
                  seals.animate.shift(LEFT * 1.1), poppet.animate.shift(LEFT * 1.1),
                  poppet_open.animate.shift(LEFT * 1.1), run_time=1.0)
        self.play(FadeIn(rods_lbl), Indicate(rods, color=MEAS_C), run_time=1.0)
        show_caption(8, "Invar rods fix the switch spacing: almost no thermal expansion")

        # ---------------- Segment 8: 10 interface enclosure ----------------
        self.sync(START[7])
        self.play(Create(box), FadeIn(badges[9]), run_time=0.8)
        show_caption(9, "Circuit board conditions the prover signals")
        self.play(Create(sig), run_time=0.5)
        self.play(Create(sig2), run_time=0.4)
        self.sync(cue(8, "وَتُرْسِلُهَا"))
        self.play(GrowArrow(to_pc), FadeIn(pc), run_time=0.8)
        self.sync(cue(8, "الَّتِي"))
        show_caption(9, "The computer processes and summarises the pass data")

        # ---------------- Segment 9: summary + next ----------------
        self.sync(START[8])
        self.play(FadeOut(caption), run_time=0.5)
        legend = VGroup(*[label(f"{name}  {idx.start + 1}–{idx.stop}", FS_LABEL, color,
                                weight=BOLD) for name, color, idx in GROUPS])
        legend.arrange(RIGHT, buff=0.7).move_to([0, CAPTION_Y + 0.25, 0])
        fit(legend)
        summ = label("Fluid path + piston with an internal valve, driven by gas and "
                     "hydraulics, watched by optics", FS_LABEL, INK)
        fit(summ).next_to(legend, DOWN, 0.2)
        self.play(FadeIn(legend, shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(summ), run_time=0.8)
        self.sync(cue(9, "فِي الحَلْقَةِ"))
        nxt = label(f"Next: the operating cycle in {len(D.CYCLE_STAGES)} stages  ·  "
                    "why flow never stops", FS_BODY, GREY_INK, weight=BOLD)
        fit(nxt).move_to([0, CAPTION_Y - 0.2, 0])
        self.play(FadeOut(legend), FadeOut(summ), run_time=0.4)
        self.play(FadeIn(nxt, shift=UP * 0.1), run_time=0.8)
        self.sync(START[9] + 2.0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="low-quality layout check")
    args = parser.parse_args()
    print(build(__file__, "ProverEp03", NARRATION, preview=args.preview))
