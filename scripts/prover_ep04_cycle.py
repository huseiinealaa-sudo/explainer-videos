"""Daniel Compact Prover series, episode 4: the operating cycle (5 stages) and why flow never stops.

Stages follow the Daniel manual 3-9008-701 Rev J, §3.1 and Figs 3-1 … 3-5 (sources in
sources/prover_ep04.md). The diagram is the episode 3 side view, simplified: liquid
enters the flow tube at the back (left), so standby (upstream) is at the back, the piston
travels to the front during the pass and returns to the back.

Build (from the repo root):
    python scripts/prover_ep04_cycle.py --preview   # 480p15 -> tmp/prover_ep04_cycle/preview.mp4
    python scripts/prover_ep04_cycle.py             # 1080p30 -> output/prover_ep04_cycle.mp4
"""
import argparse

from style import *
import prover_demo_data as D

# Fully diacritized narration — one entry per scene.
NARRATION = [
    # 1 intro
    "فِي الحَلْقَةِ السَّابِقَةِ تَعَرَّفْنَا عَلَى مُكَوِّنَاتِ المُعَايِرِ العَشَرَةِ. وَفِي هٰذِهِ الحَلْقَةِ نَرَاهَا تَعْمَلُ مَعًا: دَوْرَةُ العَمَلِ بِمَرَاحِلِهَا الخَمْسِ، كَمَا يَصِفُهَا دَلِيلُ الشَّرِكَةِ المُصَنِّعَةِ، ثُمَّ الجَوَابُ عَنْ سُؤَالٍ مُهِمٍّ: لِمَاذَا لَا يَنْقَطِعُ التَّدَفُّقُ؟",
    # 2 stage 1: standby
    "المَرْحَلَةُ الأُولَى: وَضْعُ الانْتِظَارِ. المِكْبَسُ فِي أَعْلَى المَجْرَى، وَصِمَامُ بُوبِت مَفْتُوحٌ، فَيَمُرُّ السَّائِلُ عَبْرَ المِكْبَسِ. وَيُمْسِكُهُ فِي مَكَانِهِ الضَّغْطُ الهِيدْرُولِيكِيُّ عَلَى مِكْبَسِ المُشَغِّلِ. وَيَبْقَى المُعَايِرُ هٰكَذَا حَتَّى تُرْسِلَ الحَاسِبَةُ أَمْرَ البَدْءِ.",
    # 3 stage 2: initial motion
    "المَرْحَلَةُ الثَّانِيَةُ: بَدْءُ الحَرَكَةِ. يُفْتَحُ صِمَامُ التَّحَكُّمِ الهِيدْرُولِيكِيِّ، فَيَتَحَرَّرُ الضَّغْطُ الهِيدْرُولِيكِيُّ. عِنْدَئِذٍ يَدْفَعُ ضَغْطُ البْلِينَم مِكْبَسَ المُشَغِّلِ، فَيُغْلِقُ صِمَامَ بُوبِت، وَيَبْدَأُ المِكْبَسُ التَّحَرُّكَ مَعَ السَّائِلِ، بِسُرْعَةِ التَّدَفُّقِ نَفْسِهَا.",
    # 4 stage 3: proving (the pass)
    "المَرْحَلَةُ الثَّالِثَةُ: الإِثْبَاتُ، أَيِ الشَّوْطُ. يَقْطَعُ العَلَمُ المُثَبَّتُ بِالمِكْبَسِ مِفْتَاحَيِ الحَجْمِ، دِي وَنْ ثُمَّ دِي تُو، وَتَصِلُ إِشَارَتَاهُمَا إِلَى الحَاسِبَةِ فَوْرًا. وَبَيْنَهُمَا يُزِيحُ المِكْبَسُ الحَجْمَ الأَسَاسِيَّ، وَتَعُدُّ الحَاسِبَةُ نَبَضَاتِ العَدَّادِ. فِي مِثَالِنَا، يَسْتَغْرِقُ ذٰلِكَ نَحْوَ ثَلَاثِ ثَوَانٍ وَنِصْفٍ.",
    # 5 stage 4: end of the pass
    "المَرْحَلَةُ الرَّابِعَةُ: نِهَايَةُ الشَّوْطِ. حِينَ يَقْطَعُ العَلَمُ المِفْتَاحَ الثَّانِيَ، يُغْلَقُ صِمَامُ التَّحَكُّمِ، فَيَرْتَفِعُ الضَّغْطُ الهِيدْرُولِيكِيُّ، وَيَدْفَعُ مِكْبَسَ المُشَغِّلِ نَحْوَ أَعْلَى المَجْرَى، فَيُفْتَحُ صِمَامُ بُوبِت، وَيَعُودُ السَّائِلُ يَمُرُّ عَبْرَ المِكْبَسِ.",
    # 6 stage 5: piston return
    "المَرْحَلَةُ الخَامِسَةُ: عَوْدَةُ المِكْبَسِ. تَعُودُ المَجْمُوعَةُ المُتَحَرِّكَةُ كُلُّهَا إِلَى وَضْعِ الانْتِظَارِ: مِكْبَسُ المُشَغِّلِ، وَمِكْبَسُ القِيَاسِ، وَالصِّمَامُ، وَالعَمُودَانِ، وَالعَلَمُ. وَتَتَجَاهَلُ الحَاسِبَةُ إِشَارَاتِ المَفَاتِيحِ أَثْنَاءَ العَوْدَةِ. ثُمَّ تَحْفَظُ المِضَخَّةُ الضَّغْطَ، وَيَصِيرُ المُعَايِرُ جَاهِزًا لِشَوْطٍ جَدِيدٍ. وَفِي بَيَانَاتِنَا، تَتَكَرَّرُ الدَّوْرَةُ ثَلَاثَ مَرَّاتٍ فِي كُلِّ جَوْلَةٍ.",
    # 7 why flow never stops
    "فَلِمَاذَا لَا يَنْقَطِعُ التَّدَفُّقُ؟ فِي الانْتِظَارِ وَالعَوْدَةِ، يَمُرُّ السَّائِلُ عَبْرَ الصِّمَامِ المَفْتُوحِ دَاخِلَ المِكْبَسِ. وَأَثْنَاءَ الشَّوْطِ يُغْلَقُ الصِّمَامُ، لٰكِنَّ المِكْبَسَ يَتَحَرَّكُ مَعَ السَّائِلِ فَلَا يَحْجِزُهُ. وَالبْلِينَم المَضْبُوطُ جَيِّدًا يُبْقِي فَرْقَ الضَّغْطِ عَبْرَ المِكْبَسِ صَغِيرًا جِدًّا، بِضْعَ بُوصَاتٍ مِنْ عَمُودِ المَاءِ فَقَطْ.",
    # 8 fail-safe
    "وَفَوْقَ ذٰلِكَ، صُمِّمَ المُعَايِرُ لِيَبْقَى آمِنًا عِنْدَ الخَلَلِ: فَالمَصَدُّ فِي شَفَةِ الخُرُوجِ يَمْنَعُ أَيَّ انْسِدَادٍ عَرَضِيٍّ لِلتَّدَفُّقِ. لِذٰلِكَ يُثْبَتُ العَدَّادُ وَهُوَ فِي الخِدْمَةِ، دُونَ إِيقَافِ الخَطِّ.",
    # 9 summary + next
    "الخُلَاصَةُ: انْتِظَارٌ، فَانْطِلَاقٌ، فَشَوْطٌ، فَنِهَايَةٌ، فَعَوْدَةٌ، وَالسَّائِلُ يَتَدَفَّقُ فِي كُلِّ لَحْظَةٍ. فِي الحَلْقَةِ القَادِمَةِ: الكْرُونُومِتْرِي المُزْدَوَجُ، وَضَغْطُ البْلِينَم، وَالحَجْمَانِ أَعْلَى المَجْرَى وَأَسْفَلَهُ، وَتَصْحِيحُ سِي تِي إِسْ بِي.",
]

# On-screen stage names (owner-approved wording of the manual's figure titles).
STAGE_LABELS = ["Standby", "Initial motion", "Proving (pass)", "End of pass", "Piston return"]

# Every spoken number is checked against prover_demo_data; stop if it drifts.
assert len(D.CYCLE_STAGES) == 5 == len(STAGE_LABELS)          # seg 1 "five stages"
assert round(D.PASS_TIME * 2) / 2 == 3.5                      # seg 4 "about 3.5 s"
assert D.PASSES_PER_RUN == 3                                  # seg 6 "three times per run"

AUDIO_DIR = BUILD_DIR / "prover_ep04_cycle" / "audio"

FLUID_C = "#1f5fa8"             # same group colours as episode 3
DRIVE_C = "#c25a12"
MEAS_C = "#2e7d32"

# Diagram geometry: episode 3 layout, raised to leave room for the stage bar.
TUBE_L, TUBE_R, TUBE_Y, TUBE_H = -1.8, 3.4, 0.8, 1.3
PIPE_Y = -0.8
ENTRY_X = -1.35
FLANGE_X = 4.3
PISTON_X = -0.8                 # standby (back / upstream)
POPPET_LIFT = 0.55              # poppet opens upstream, off its seat (manual §3.1 step 4)
CYL_L, CYL_R, CYL_H = -4.9, -2.8, 0.62
ACT_X = -4.45                   # actuator piston at standby, poppet open
ACT_TRAVEL = 1.0                # drawn shorter than the piston travel (schematic)
ACT_CLOSE = 0.25                # extra downstream shift that seats the poppet
BAR_L, BAR_R, BAR_Y = -6.0, -3.0, 2.05
SHAFT_Y = 1.6
SW_X = {"STBY": -5.6, "D1": -4.5, "D2": -3.4}
TRAVEL = 2.4                    # piston / flag travel, back -> front
S_D1 = (SW_X["D1"] - SW_X["STBY"]) / TRAVEL
S_D2 = (SW_X["D2"] - SW_X["STBY"]) / TRAVEL
VALVE = np.array([-3.15, -0.1, 0])
PUMP = np.array([-4.6, -0.95, 0])
PC = np.array([-6.4, 0.0, 0])
BAR_ROW_Y = -2.35               # stage bar
CAPTION_Y = -3.2


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
    return VGroup(path.copy().set_stroke(INK, width), path.copy().set_stroke(BG, width - 7))


def arrow(a, b, color=GREY_INK, width=4, ratio=0.3):
    return Arrow(np.array([*a, 0]), np.array([*b, 0]), buff=0, stroke_width=width, color=color,
                 max_tip_length_to_length_ratio=ratio)


class ProverEp04(SyncedScene):
    def construct(self):
        START = segment_starts(AUDIO_DIR, len(NARRATION))

        def at(seg, frac):
            return START[seg - 1] + frac * (START[seg] - START[seg - 1])

        def cue(seg, phrase):
            """Time at which `phrase` starts in segment `seg` (by text position)."""
            text = NARRATION[seg - 1]
            i = text.find(phrase)
            assert i >= 0, (seg, phrase)
            return at(seg, i / len(text))

        # ---------------- Segment 1: title ----------------
        series = label("Daniel Compact Prover  ·  Episode 4", FS_SUBTITLE, GREY_INK)
        title = Text("The Operating Cycle", font_size=FS_TITLE, weight=BOLD)
        line = Line(LEFT, RIGHT).set_width(title.width)
        sub = label(f"{len(D.CYCLE_STAGES)} stages  ·  and why the flow never stops",
                    FS_BODY, GREY_INK)
        VGroup(series, title, line, sub).arrange(DOWN, buff=0.35).move_to(UP * 0.5)
        prev = label(f"Previously: the {len(D.PROVER_COMPONENTS)} main components",
                     FS_LABEL, GREY_INK).move_to(DOWN * 2.4)

        self.play(FadeIn(series, shift=DOWN * 0.2), FadeIn(prev), run_time=1.0)
        self.sync(cue(1, "وَفِي هٰذِهِ"))
        self.play(Write(title), Create(line), run_time=1.8)
        self.sync(cue(1, "دَوْرَةُ العَمَلِ"))
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.8)
        self.sync(cue(1, "ثُمَّ الجَوَابُ") - 0.8)
        corner = label("Ep 4 · Operating cycle", FS_BODY - 6, weight=BOLD).to_corner(UL, buff=0.4)
        self.play(FadeOut(VGroup(series, line, sub, prev)), Transform(title, corner),
                  run_time=0.8)

        # ---------------- State trackers ----------------
        s = ValueTracker(0.0)       # assembly travel: 0 = standby (back), 1 = end (front)
        p = ValueTracker(1.0)       # poppet: 1 = open, 0 = closed
        hp = ValueTracker(1.0)      # hydraulic pressure on the oil side: 1 = held, 0 = released

        def px():
            return PISTON_X + s.get_value() * TRAVEL

        def ax():
            return ACT_X + s.get_value() * ACT_TRAVEL + (1 - p.get_value()) * ACT_CLOSE

        # ---------------- Static diagram ----------------
        out_pipe = pipe([(TUBE_R, TUBE_Y), (5.0, TUBE_Y)])
        in_pipe = pipe([(5.0, PIPE_Y), (ENTRY_X, PIPE_Y), (ENTRY_X, TUBE_Y - TUBE_H / 2)])
        flanges = VGroup(*[Rectangle(width=0.22, height=h, stroke_width=4, color=INK,
                                     fill_color=BG, fill_opacity=1).move_to([x, y, 0])
                           for x, y, h in ((TUBE_R + 0.11, TUBE_Y, TUBE_H + 0.35),
                                           (FLANGE_X, PIPE_Y, 0.85), (FLANGE_X, TUBE_Y, 0.85))])
        stop = Line([TUBE_R - 0.05, TUBE_Y - 0.35, 0], [TUBE_R - 0.05, TUBE_Y + 0.35, 0],
                    stroke_width=7, color=FLUID_C)
        tube = Rectangle(width=TUBE_R - TUBE_L, height=TUBE_H, stroke_width=5, color=INK)
        tube.move_to([(TUBE_L + TUBE_R) / 2, TUBE_Y, 0])
        cap = Rectangle(width=0.2, height=TUBE_H + 0.35, stroke_width=4, color=INK)
        cap.move_to([TUBE_L - 0.1, TUBE_Y, 0])
        out_arrow = arrow((5.1, TUBE_Y), (6.3, TUBE_Y))
        in_arrow = arrow((6.3, PIPE_Y), (5.1, PIPE_Y))
        out_lbl = label("OUTLET", FS_TAG, GREY_INK, weight=BOLD).next_to(out_arrow, DOWN, 0.1)
        in_lbl = label("INLET", FS_TAG, GREY_INK, weight=BOLD).next_to(in_arrow, DOWN, 0.1)
        entry = arrow((ENTRY_X, PIPE_Y + 0.1), (ENTRY_X, TUBE_Y - 0.75), FLUID_C, 3)
        front = label("FRONT →", FS_TAG, GREY_INK).move_to([5.7, 3.1, 0])
        back = label("← BACK (upstream)", FS_TAG, GREY_INK).move_to([0.6, 3.1, 0])
        tank = RoundedRectangle(width=4.0, height=0.62, corner_radius=0.3, stroke_width=4,
                                color=INK).move_to([0.9, 2.35, 0])
        n2 = label("plenum N₂", FS_TAG, DRIVE_C, weight=BOLD).move_to(tank)
        cyl = Rectangle(width=CYL_R - CYL_L, height=CYL_H, stroke_width=4, color=INK)
        cyl.move_to([(CYL_L + CYL_R) / 2, TUBE_Y, 0])
        gas_t = label("gas", FS_TAG - 4, GREY_INK).next_to(cyl, UP, 0.06).align_to(cyl, LEFT)
        oil_t = label("oil", FS_TAG - 4, DRIVE_C).next_to(cyl, UP, 0.06).align_to(cyl, RIGHT)
        valve = VGroup(Polygon(VALVE + [-0.3, 0.2, 0], VALVE, VALVE + [-0.3, -0.2, 0]),
                       Polygon(VALVE + [0.3, 0.2, 0], VALVE, VALVE + [0.3, -0.2, 0])
                       ).set_stroke(INK, 3)
        v_line = Line(VALVE + [0, 0.2, 0], [VALVE[0], TUBE_Y - CYL_H / 2, 0], stroke_width=3,
                      color=DRIVE_C)
        pump = VGroup(Circle(radius=0.34, stroke_width=4, color=INK).move_to(PUMP),
                      Triangle(stroke_width=0, fill_color=INK, fill_opacity=1).scale(0.12)
                      .move_to(PUMP + [0, 0.18, 0]))
        motor = VGroup(Rectangle(width=0.7, height=0.5, stroke_width=4, color=INK),
                       label("M", FS_TAG, INK, weight=BOLD)).move_to(PUMP + [-0.95, 0, 0])
        res = VGroup(Rectangle(width=0.95, height=0.55, stroke_width=4, color=INK),
                     label("oil", FS_TAG - 4, GREY_INK)).move_to([-2.95, -1.45, 0])
        p_lines = VGroup(
            VMobject().set_points_as_corners([PUMP + [0.34, 0, 0], [VALVE[0], PUMP[1], 0],
                                              VALVE + [0, -0.2, 0]]),
            VMobject().set_points_as_corners([PUMP + [0, -0.34, 0], [PUMP[0], -1.45, 0],
                                              [-3.42, -1.45, 0]]),
        ).set_stroke(DRIVE_C, 3)
        rods = VGroup(*[Line([BAR_L, BAR_Y + dy, 0], [BAR_R, BAR_Y + dy, 0], stroke_width=3,
                             color=MEAS_C) for dy in (-0.22, 0.22)])
        switches, sw_lbls = VGroup(), VGroup()
        for name, x in SW_X.items():
            switches.add(VGroup(*[Rectangle(width=0.1, height=0.3, stroke_width=0,
                                            fill_color=INK, fill_opacity=1)
                                  .move_to([x + dx, BAR_Y, 0]) for dx in (-0.09, 0.09)]))
            sw_lbls.add(label(name, FS_TAG, INK if name == "STBY" else MEAS_C,
                              weight=BOLD).move_to([x, BAR_Y + 0.5, 0]))
        pc_box = VGroup(Rectangle(width=1.25, height=0.6, stroke_width=4, color=INK),
                        label("computer", FS_TAG - 6, MEAS_C)).move_to(PC)
        sig = VMobject().set_points_as_corners([[BAR_L, BAR_Y, 0], [PC[0], BAR_Y, 0],
                                                PC + [0, 0.3, 0]])
        sig = DashedVMobject(sig.set_stroke(MEAS_C, 3), num_dashes=18)
        diagram = VGroup(in_pipe, out_pipe, flanges, stop, tube, cap, out_arrow, in_arrow,
                         out_lbl, in_lbl, entry, front, back, tank, n2, cyl, gas_t, oil_t,
                         valve, v_line, pump, motor, res, p_lines, rods, switches, sw_lbls,
                         pc_box, sig)

        # ---------------- Moving parts ----------------
        def piston_mob():
            x = px()
            body = Rectangle(width=0.42, height=TUBE_H - 0.1, stroke_width=4, color=INK,
                             fill_color=INK, fill_opacity=0.15).move_to([x, TUBE_Y, 0])
            gap = Rectangle(width=0.44, height=0.38, stroke_width=0, fill_color=BG,
                            fill_opacity=p.get_value()).move_to([x, TUBE_Y, 0])
            dx = -POPPET_LIFT * p.get_value()
            poppet = Polygon([x + 0.05 + dx, TUBE_Y + 0.19, 0], [x + 0.34 + dx, TUBE_Y + 0.1, 0],
                             [x + 0.34 + dx, TUBE_Y - 0.1, 0], [x + 0.05 + dx, TUBE_Y - 0.19, 0],
                             stroke_width=3, color=INK, fill_color=FLUID_C, fill_opacity=0.6)
            return VGroup(body, gap, poppet)

        def drive_mob():
            a = ax()
            top, bot = TUBE_Y + CYL_H / 2 - 0.03, TUBE_Y - CYL_H / 2 + 0.03
            oil = Rectangle(width=max(CYL_R - a - 0.07, 0.01), height=top - bot, stroke_width=0,
                            fill_color=DRIVE_C, fill_opacity=0.08 + 0.4 * hp.get_value())
            oil.move_to([(a + 0.07 + CYL_R) / 2, TUBE_Y, 0])
            act = Rectangle(width=0.14, height=CYL_H - 0.06, stroke_width=0, fill_color=DRIVE_C,
                            fill_opacity=1).move_to([a, TUBE_Y, 0])
            dx = -POPPET_LIFT * p.get_value()
            shaft = Line([a + 0.07, TUBE_Y, 0], [px() + 0.05 + dx, TUBE_Y, 0], stroke_width=4,
                         color=DRIVE_C)
            return VGroup(oil, act, shaft)

        def flag_mob():
            fx = SW_X["STBY"] + s.get_value() * TRAVEL
            return VGroup(Line([fx, SHAFT_Y, 0], [fx, BAR_Y + 0.12, 0], stroke_width=5,
                               color=MEAS_C),
                          Line([fx, SHAFT_Y, 0], [fx + 1.2, SHAFT_Y, 0], stroke_width=4,
                               color=MEAS_C))

        def through_mob():
            x = px()
            return Arrow([x - 0.95, TUBE_Y, 0], [x + 1.05, TUBE_Y, 0], buff=0, stroke_width=4,
                         color=FLUID_C, max_tip_length_to_length_ratio=0.15
                         ).set_opacity(max(p.get_value() * 2 - 1, 0))

        def push_mob():
            x = px()
            return Arrow([x - 1.0, TUBE_Y + 0.35, 0], [x - 0.3, TUBE_Y + 0.35, 0], buff=0,
                         stroke_width=4, color=FLUID_C, max_tip_length_to_length_ratio=0.3
                         ).set_opacity(max(1 - p.get_value() * 2, 0))

        drive = always_redraw(drive_mob)
        piston = always_redraw(piston_mob)
        flag = always_redraw(flag_mob)
        through = always_redraw(through_mob)
        push = always_redraw(push_mob)

        # ---------------- Stage bar and captions ----------------
        cells = VGroup()
        for k, name in enumerate(STAGE_LABELS):
            box = RoundedRectangle(width=2.55, height=0.52, corner_radius=0.12, stroke_width=3,
                                   color=GREY_INK)
            cells.add(VGroup(box, fit(label(f"{k + 1}  {name}", FS_TAG - 3, GREY_INK), 2.35)
                             .move_to(box)))
        cells.arrange(RIGHT, buff=0.1).move_to([0, BAR_ROW_Y, 0])
        fit(cells, 13.4)
        lit = VMobject()

        def light(k, color=INK):
            nonlocal lit
            box = cells[k][0]
            new = VGroup(box.copy().set_stroke(color, 5).set_fill(color, 0.12),
                         fit(label(f"{k + 1}  {STAGE_LABELS[k]}", FS_TAG - 3, color,
                                   weight=BOLD), 2.35).move_to(box))
            anims = [FadeIn(new), cells[k][1].animate.set_opacity(0)]
            if len(lit.submobjects):
                anims += [FadeOut(lit), cells[lit.k][1].animate.set_opacity(1)]
            self.play(*anims, run_time=0.5)
            new.k = k
            lit = new

        caption = VMobject()

        def say(text, color=INK):
            nonlocal caption
            new = fit(label(text, FS_LABEL, color)).move_to([0, CAPTION_Y, 0])
            if len(caption.submobjects) or caption.has_points():
                self.play(FadeOut(caption), run_time=0.25)
            self.play(FadeIn(new, shift=UP * 0.08), run_time=0.4)
            caption = new

        # draw the diagram (end of segment 1)
        self.play(LaggedStart(Create(in_pipe), Create(out_pipe), FadeIn(flanges), Create(tube),
                              Create(cap), lag_ratio=0.2), FadeIn(front), FadeIn(back),
                  run_time=1.6)
        self.add(drive, piston, flag)
        self.play(FadeIn(VGroup(stop, tank, n2, cyl, gas_t, oil_t, valve, v_line, pump, motor,
                                res, p_lines, rods, switches, sw_lbls, pc_box, sig)),
                  GrowArrow(in_arrow), GrowArrow(out_arrow), FadeIn(in_lbl), FadeIn(out_lbl),
                  GrowArrow(entry), run_time=1.2)
        self.play(FadeIn(cells), run_time=0.8)

        # ---------------- Segment 2: stage 1, standby ----------------
        self.sync(START[1])
        light(0)
        say("Piston at the back (upstream)  ·  poppet open")
        self.add(through)
        self.sync(cue(2, "فَيَمُرُّ"))
        say("Liquid flows through the open poppet", FLUID_C)
        self.sync(cue(2, "وَيُمْسِكُهُ"))
        say("Held by hydraulic pressure on the actuator piston", DRIVE_C)
        self.play(Indicate(oil_t, color=DRIVE_C), run_time=0.8)
        self.sync(cue(2, "وَيَبْقَى"))
        run_lbl = label("RUN ?", FS_TAG, MEAS_C, weight=BOLD).next_to(pc_box, DOWN, 0.15)
        self.play(FadeIn(run_lbl), run_time=0.5)
        say("Waits for the RUN command from the computer", MEAS_C)

        # ---------------- Segment 3: stage 2, initial motion ----------------
        self.sync(START[2])
        light(1)
        run_go = label("RUN ▶", FS_TAG, MEAS_C, weight=BOLD).move_to(run_lbl)
        v_open = label("OPEN", FS_TAG, DRIVE_C, weight=BOLD).next_to(valve, LEFT, 0.15)
        self.play(Transform(run_lbl, run_go), FadeIn(v_open), run_time=0.6)
        say("Hydraulic control valve opens  →  hydraulic pressure released", DRIVE_C)
        self.play(hp.animate.set_value(0.0), run_time=1.0)
        self.sync(cue(3, "عِنْدَئِذٍ"))
        say("Plenum pressure pushes the actuator piston  →  poppet closes", DRIVE_C)
        self.play(p.animate.set_value(0.0), run_time=1.2)
        self.sync(cue(3, "وَيَبْدَأُ"))
        say("The piston starts to move with the liquid, at the flow rate", FLUID_C)
        self.add(push)
        self.play(s.animate.set_value(0.12), run_time=2.0, rate_func=rate_functions.ease_in_quad)

        # ---------------- Segment 4: stage 3, proving (the pass) ----------------
        self.sync(START[3])
        light(2, FLUID_C)
        self.play(FadeOut(run_lbl), run_time=0.3)
        say("The flag trips the volume switches D1, then D2")
        self.play(s.animate.set_value(S_D1), run_time=1.2, rate_func=linear)
        self.play(Flash([SW_X["D1"], BAR_Y, 0], color=MEAS_C, line_length=0.25), run_time=0.5)
        self.sync(cue(4, "وَبَيْنَهُمَا"))
        say("D1 → D2: base volume displaced  ·  meter pulses counted")
        clock_t = ValueTracker(0.0)
        clock = always_redraw(lambda: label(f"{clock_t.get_value():.3f} s", FS_LABEL, FLUID_C,
                                            weight=BOLD).move_to([1.2, TUBE_Y - 1.1, 0]))
        self.add(clock)
        self.play(s.animate.set_value(S_D2), clock_t.animate.set_value(D.PASS_TIME),
                  run_time=D.PASS_TIME, rate_func=linear)
        self.play(Flash([SW_X["D2"], BAR_Y, 0], color=MEAS_C, line_length=0.25), run_time=0.5)
        self.sync(cue(4, "فِي مِثَالِنَا"))
        say(f"Our example: {D.PASS_TIME:.3f} s  (≈ 3.5 s)", FLUID_C)

        # ---------------- Segment 5: stage 4, end of the pass ----------------
        self.sync(START[4])
        self.remove(clock)
        light(3, DRIVE_C)
        self.play(s.animate.set_value(1.0), run_time=0.6, rate_func=linear)
        v_closed = label("CLOSED", FS_TAG, DRIVE_C, weight=BOLD).next_to(valve, LEFT, 0.15)
        self.play(Transform(v_open, v_closed), run_time=0.5)
        say("At D2 the control valve closes  →  hydraulic pressure builds", DRIVE_C)
        self.play(hp.animate.set_value(1.0), run_time=1.0)
        self.sync(cue(5, "وَيَدْفَعُ"))
        say("The actuator piston is pushed back  →  the poppet opens", DRIVE_C)
        self.play(p.animate.set_value(1.0), run_time=1.2)
        self.sync(cue(5, "وَيَعُودُ"))
        say("Liquid flows through the piston again", FLUID_C)

        # ---------------- Segment 6: stage 5, piston return ----------------
        self.sync(START[5])
        light(4, MEAS_C)
        self.play(FadeOut(v_open), run_time=0.3)
        say("The whole moving assembly returns to standby, at the back")
        self.play(s.animate.set_value(0.0), run_time=4.0)
        self.sync(cue(6, "وَتَتَجَاهَلُ"))
        ign = label("switch signals ignored on return", FS_TAG, MEAS_C).move_to([-2.6, 2.95, 0])
        self.play(FadeIn(ign), run_time=0.5)
        say("The computer ignores the switch signals during the return", MEAS_C)
        self.sync(cue(6, "ثُمَّ تَحْفَظُ"))
        self.play(FadeOut(ign), Indicate(pump, color=DRIVE_C), run_time=1.0)
        say("The pump holds the pressure  ·  ready for the next pass", DRIVE_C)
        self.sync(cue(6, "وَفِي بَيَانَاتِنَا"))
        say(f"Our data: the cycle runs {D.PASSES_PER_RUN} times per run  "
            f"({D.PASSES_PER_RUN} passes)")

        # ---------------- Segment 7: why the flow never stops ----------------
        self.sync(START[6])
        self.play(FadeOut(lit), cells[lit.k][1].animate.set_opacity(1), run_time=0.3)
        lit = VMobject()
        why = label("Why does the flow never stop?", FS_LABEL + 2, weight=BOLD)
        why.move_to([3.3, 3.1, 0])
        self.play(FadeOut(front), FadeOut(back), Write(why), run_time=0.8)
        self.sync(cue(7, "فِي الانْتِظَارِ"))
        say("Standby and return: liquid passes through the open poppet", FLUID_C)
        self.play(Indicate(in_arrow, color=FLUID_C), Indicate(out_arrow, color=FLUID_C),
                  run_time=1.0)
        self.sync(cue(7, "وَأَثْنَاءَ"))
        say("During the pass: poppet closed, but the piston moves with the liquid", FLUID_C)
        self.play(p.animate.set_value(0.0), run_time=0.6)
        self.play(s.animate.set_value(0.55), run_time=2.2, rate_func=linear)
        self.sync(cue(7, "وَالبْلِينَم"))
        dp = label("ΔP across piston: a few inches of water", FS_TAG - 5, DRIVE_C, weight=BOLD)
        dp.move_to([1.75, TUBE_Y - 1.0, 0])
        self.play(FadeIn(dp), s.animate.set_value(1.0), run_time=1.6, rate_func=linear)
        say("A well-adjusted plenum keeps the pressure difference very small", DRIVE_C)
        self.sync(START[7] - 1.6)
        self.play(FadeOut(dp), p.animate.set_value(1.0), run_time=0.6)
        self.play(s.animate.set_value(0.0), run_time=0.9)

        # ---------------- Segment 8: fail-safe ----------------
        self.sync(START[7])
        stop_lbl = label("positive stop", FS_TAG, FLUID_C, weight=BOLD)
        stop_lbl.next_to(flanges[0], UP, 0.12)
        self.play(FadeIn(stop_lbl), Circumscribe(stop, color=FLUID_C), run_time=1.0)
        say("Fail-safe: the positive stop prevents any accidental blockage", FLUID_C)
        self.sync(cue(8, "لِذٰلِكَ"))
        say("The meter is proved in service, without shutting the line", INK)
        self.play(Indicate(in_arrow, color=FLUID_C), Indicate(out_arrow, color=FLUID_C),
                  run_time=1.0)

        # ---------------- Segment 9: summary + next ----------------
        self.sync(START[8])
        self.play(FadeOut(stop_lbl), FadeOut(why), run_time=0.4)
        for k in range(len(STAGE_LABELS)):
            self.play(cells[k][0].animate.set_stroke(INK, 4).set_fill(FLUID_C, 0.1),
                      cells[k][1].animate.set_color(INK), run_time=0.35)
        say("Standby → start → pass → end → return  ·  the liquid flows at every moment", FLUID_C)
        self.sync(cue(9, "فِي الحَلْقَةِ"))
        say("Next: double chronometry · plenum pressure · upstream/downstream volumes · CTSp",
            GREY_INK)
        self.sync(START[9] + 2.0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="low-quality layout check")
    args = parser.parse_args()
    print(build(__file__, "ProverEp04", NARRATION, preview=args.preview))
