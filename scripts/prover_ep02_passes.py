"""Daniel Compact Prover series, episode 2: pass, run, repeatability, Coriolis specifics.

Every number on screen or in the narration comes from prover_demo_data.

Build (from the repo root):
    python scripts/prover_ep02_passes.py --preview   # 480p15 -> tmp/prover_ep02_passes/preview.mp4
    python scripts/prover_ep02_passes.py             # 1080p30 -> output/prover_ep02_passes.mp4
"""
import argparse

from style import *
import prover_demo_data as D

# Fully diacritized narration — one entry per scene.
NARRATION = [
    # 1 intro
    "فِي هٰذِهِ الحَلْقَةِ: الشَّوْطُ وَالجَوْلَةُ، وَالتَّكْرَارِيَّةُ الَّتِي نَحْكُمُ بِهَا عَلَى قَبُولِ الإِثْبَاتِ، وَخُصُوصِيَّةُ عَدَّادَاتِ كُورْيُولِيس.",
    # 2 pass
    "الشَّوْطُ حَرَكَةٌ وَاحِدَةٌ لِلْمِكْبَسِ بَيْنَ الكَاشِفَيْنِ، يُزِيحُ فِيهَا الحَجْمَ الأَسَاسِيَّ مَرَّةً وَاحِدَةً، وَتَعُدُّ الحَاسِبَةُ خِلَالَهَا نَبَضَاتِ العَدَّادِ. وَبَعْدَ نِهَايَةِ الشَّوْطِ، يُعِيدُ النِّظَامُ الهِيدْرُولِيكِيُّ المِكْبَسَ إِلَى وَضْعِ الانْتِظَارِ، فَيَصِيرُ المُعَايِرُ جَاهِزًا لِشَوْطٍ جَدِيدٍ.",
    # 3 run
    "أَمَّا الجَوْلَةُ فَمَجْمُوعَةُ أَشْوَاطٍ مُتَتَالِيَةٍ، يُؤْخَذُ مُتَوَسِّطُهَا نَتِيجَةً وَاحِدَةً، فَلِكُلِّ جَوْلَةٍ مُعَامِلُهَا وَكِي خَاصٌّ بِهَا. فِي بَيَانَاتِنَا التَّوْضِيحِيَّةِ: ثَلَاثَةُ أَشْوَاطٍ فِي كُلِّ جَوْلَةٍ، وَخَمْسُ جَوْلَاتٍ، أَيْ خَمْسَةَ عَشَرَ شَوْطًا فِي الإِثْبَاتِ كُلِّهِ. وَتَضَعُ بَعْضُ الإِجْرَاءَاتِ حَدًّا أَعْلَى لِعَدَدِ الأَشْوَاطِ فِي الجَوْلَةِ، حَتَّى لَا يُخْفِيَ المُتَوَسِّطُ ضَعْفَ التَّكْرَارِيَّةِ.",
    # 4 pass time + nominal frequency
    "وَزَمَنُ الشَّوْطِ هُوَ الحَجْمُ الأَسَاسِيُّ مَقْسُومًا عَلَى التَّدَفُّقِ، بِالثَّوَانِي. فَعِنْدَ مِئَتَيْنِ وَخَمْسِينَ مِتْرًا مُكَعَّبًا فِي السَّاعَةِ، يَدُومُ الشَّوْطُ ثَلَاثَةً فَاصِلَةَ خَمْسَةٍ أَرْبَعَةٍ سَبْعَةٍ مِنَ الثَّوَانِي. وَالتَّرَدُّدُ الاسْمِيُّ لِنَبَضَاتِ العَدَّادِ نَحْوُ أَرْبَعَةِ آلَافٍ وَمِئَةٍ وَسَبْعَةٍ وَسِتِّينَ هِيرْتْز، مَحْسُوبًا بِكِي الاسْمِيِّ؛ أَمَّا النَّبَضَاتُ الفِعْلِيَّةُ فَتَخْتَلِفُ قَلِيلًا بِسَبَبِ التَّصْحِيحَاتِ وَمُعَامِلِ العَدَّادِ.",
    # 5 repeatability
    "وَالتَّكْرَارِيَّةُ تَقِيسُ تَقَارُبَ نَتَائِجِ الجَوْلَاتِ: نَطْرَحُ أَصْغَرَ قِيمَةٍ لِكِي مِنْ أَكْبَرِهَا، وَنَقْسِمُ الفَرْقَ عَلَى الأَصْغَرِ، وَنَضْرِبُ فِي مِئَةٍ. فِي مِثَالِنَا، أَكْبَرُ قِيمَةٍ نَحْوُ سِتِّينَ أَلْفًا وَتِسْعَةٍ وَسِتِّينَ، وَأَصْغَرُهَا نَحْوُ سِتِّينَ أَلْفًا وَوَاحِدٍ وَخَمْسِينَ، فَالتَّكْرَارِيَّةُ صِفْرٌ فَاصِلَةُ صِفْرٍ ثَلَاثَةٍ بِالمِئَةِ، ضِمْنَ حَدِّ صِفْرٍ فَاصِلَةِ صِفْرٍ خَمْسَةٍ.",
    # 6 API MPMS 4.8 table
    "وَهٰذَا الحَدُّ مِنْ جَدْوَلٍ فِي إِي بِي آي، الفَصْلِ الرَّابِعِ، القِسْمِ الثَّامِنِ، يَرْبِطُ عَدَدَ الجَوْلَاتِ بِأَقْصَى تَكْرَارِيَّةٍ، لِيَبْقَى عَدَمُ اليَقِينِ فِي مُعَامِلِ العَدَّادِ ضِمْنَ صِفْرٍ فَاصِلَةِ صِفْرٍ اثْنَيْنِ سَبْعَةٍ بِالمِئَةِ: ثَلَاثُ جَوْلَاتٍ حَدُّهَا صِفْرٌ فَاصِلَةُ صِفْرٍ اثْنَيْنِ، وَأَرْبَعٌ صِفْرٌ فَاصِلَةُ صِفْرٍ ثَلَاثَةٍ، وَخَمْسٌ صِفْرٌ فَاصِلَةُ صِفْرٍ خَمْسَةٍ. فَكُلَّمَا زَادَتِ الجَوْلَاتُ اتَّسَعَ الحَدُّ، لِأَنَّ المُتَوَسِّطَ يُصْبِحُ أَوْثَقَ. وَإِذَا فَشِلَتِ التَّكْرَارِيَّةُ، فَالمُمَارَسَةُ الشَّائِعَةُ اسْتِبْعَادُ البَيَانَاتِ وَإِعَادَةُ الإِثْبَاتِ.",
    # 7 Coriolis: manufactured pulses, damping, pass time
    "وَالآنَ إِلَى خُصُوصِيَّةِ كُورْيُولِيس. نَبَضَاتُ هٰذَا العَدَّادِ لَا تَأْتِي مِنْ جُزْءٍ دَوَّارٍ، بَلْ تُوَلِّدُهَا إِلِكْتْرُونِيَّاتُ المُرْسِلِ بَعْدَ مُعَالَجَةِ الإِشَارَةِ، فَتَتَأَخَّرُ قَلِيلًا. لِذٰلِكَ يُضْبَطُ التَّخْمِيدُ عَلَى أَسْرَعِ اسْتِجَابَةٍ أَثْنَاءَ الإِثْبَاتِ، فَتَصِيرُ القِرَاءَةُ أَكْثَرَ تَذَبْذُبًا، وَيُعَوَّضُ ذٰلِكَ بِزَمَنِ شَوْطٍ كَافٍ وَبِمُتَوَسِّطِ عِدَّةِ أَشْوَاطٍ. وَشَوْطُنَا أَطْوَلُ بِكَثِيرٍ مِنْ ثَمَانِيَةِ أَعْشَارِ الثَّانِيَةِ، وَهُوَ الحَدُّ الأَدْنَى النَّمَطِيُّ لِكُورْيُولِيس.",
    # 8 Coriolis: mass or volumetric proving (owner decision)
    "وَيُمْكِنُ ضَبْطُ عَدَّادِ كُورْيُولِيس لِيُعْطِيَ كُتْلَةً أَوْ حَجْمًا، فَيُثْبَتُ كُتْلِيًّا أَوْ حَجْمِيًّا. وَهٰذِهِ السِّلْسِلَةُ تَتْبَعُ الطَّرِيقَةَ الحَجْمِيَّةَ كَمَا فِي الدَّلِيلِ، وَلِهٰذَا يَحْمِلُ التَّقْرِيرُ تَصْحِيحَاتِ السَّائِلِ، سِي تِي إِلْ وَسِي بِي إِلْ. أَمَّا إِثْبَاتُ الكُتْلَةِ بِمُعَايِرٍ حَجْمِيٍّ، فَيَحْسُبُ الكُتْلَةَ مِنَ الحَجْمِ وَالكَثَافَةِ، فَيَشْتَرِطُ كَثَافَةً مُسْتَقِرَّةً. وَيُعَادُ الإِثْبَاتُ كُلَّمَا ضُبِطَ صِفْرُ العَدَّادِ.",
    # 9 summary + next
    "الخُلَاصَةُ: الشَّوْطُ حَرَكَةٌ وَاحِدَةٌ لِلْمِكْبَسِ، وَالجَوْلَةُ مُتَوَسِّطُ عِدَّةِ أَشْوَاطٍ، وَالتَّكْرَارِيَّةُ تَحْكُمُ عَلَى تَقَارُبِ الجَوْلَاتِ ضِمْنَ حَدٍّ يَتَّسِعُ بِعَدَدِهَا. فِي الحَلْقَةِ القَادِمَةِ: مُكَوِّنَاتُ المُعَايِرِ المُدْمَجِ العَشَرَةُ.",
]

# Every spoken number is checked against prover_demo_data; stop if it drifts.
assert D.PASSES_PER_RUN == 3                                  # seg 3 "three passes per run"
assert D.RUN_COUNT == 5                                       # seg 3 "five runs"
assert D.TOTAL_PASSES == 15                                   # seg 3 "fifteen passes"
assert round(D.FLOW_RATE) == 250                              # seg 4 "250 m3/h"
assert f"{D.PASS_TIME:.3f}" == "3.547"                        # seg 4 "3.547 s"
assert round(D.FREQUENCY) == 4167                             # seg 4 "about 4167 Hz" (nominal)
assert round(D.K_MAX) == 60069                                # seg 5 "about 60,069"
assert round(D.K_MIN) == 60051                                # seg 5 "about 60,051"
assert f"{D.REPEATABILITY:.2f}" == "0.03"                     # seg 5 "0.03 %"
assert D.REPEATABILITY_LIMIT == 0.05                          # seg 5, 6 "0.05 %"
assert D.MF_UNCERTAINTY_TARGET == 0.027                       # seg 6 "0.027 %"
assert (D.API_48_REPEATABILITY[3], D.API_48_REPEATABILITY[4],
        D.API_48_REPEATABILITY[5]) == (0.02, 0.03, 0.05)      # seg 6 table rows
assert D.CORIOLIS_MIN_PASS_TIME == 0.8                        # seg 7 "0.8 s"
assert D.PASS_TIME > D.CORIOLIS_MIN_PASS_TIME                 # seg 7 "much longer"

AUDIO_DIR = BUILD_DIR / "prover_ep02_passes" / "audio"

PROVER_C = "#1f5fa8"            # prover side (same colours as episode 1)
METER_C = "#c25a12"             # meter side
OK_C = "#2e7d32"                # pass / accepted

BPV_TXT = f"{D.BPV:.4f}"
Q_TXT = f"{D.FLOW_RATE:.1f}"
K_NOM_TXT = f"{D.K_NOMINAL:.0f}"
PASS_TXT = f"{D.PASS_TIME:.3f}"
FREQ_TXT = f"{D.FREQUENCY:.1f}"
KMAX_TXT = f"{D.K_MAX:.3f}"
KMIN_TXT = f"{D.K_MIN:.3f}"
REP_TXT = f"{D.REPEATABILITY:.4f}"
LIM_TXT = f"{D.REPEATABILITY_LIMIT:.2f}"

# Prover diagram geometry
PIPE_Y = -0.4
PRV_L, PRV_R = -5.0, 3.0
PRV_H = 1.3
D1_X, D2_X = -2.6, 1.8
STANDBY_X = -4.6


def label(text, size=FS_LABEL, color=INK, **kw):
    return Text(text, font_size=size, color=color, **kw)


def fit(mob, width=13.2):
    """Keep a group inside the 16:9 frame with a side margin."""
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def boxed(mob, color=INK, buff=0.3):
    return SurroundingRectangle(mob, buff=buff, corner_radius=0.15, stroke_width=4, color=color)


class ProverEp02(SyncedScene):
    def construct(self):
        START = segment_starts(AUDIO_DIR, len(NARRATION))

        def at(seg, frac):
            """Absolute time at a fraction of narration segment `seg` (1-based)."""
            return START[seg - 1] + frac * (START[seg] - START[seg - 1])

        def clear(keep=()):
            self.play(*[FadeOut(m) for m in self.mobjects if m not in keep], run_time=0.6)

        # ---------------- Segment 1: title ----------------
        series = label("Daniel Compact Prover  ·  Episode 2", FS_SUBTITLE, GREY_INK)
        title = Text("Pass, Run & Repeatability", font_size=FS_TITLE - 4, weight=BOLD)
        fit(title, 12.6)
        line = Line(LEFT, RIGHT).set_width(title.width)
        sub = label("… and what is special about Coriolis meters", FS_BODY, GREY_INK)
        head = VGroup(series, title, line, sub).arrange(DOWN, buff=0.35).move_to(UP * 0.4)

        self.play(FadeIn(series, shift=DOWN * 0.2), run_time=1.0)
        self.play(Write(title), run_time=2.0)
        self.play(Create(line), run_time=0.8)
        self.sync(at(1, 0.7))
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=1.0)
        self.sync(START[1] - 0.8)
        corner = label("Ep 2 · Pass, Run, Repeatability", FS_BODY - 6, weight=BOLD)
        corner.to_corner(UL, buff=0.4)
        self.play(FadeOut(VGroup(series, line, sub)), Transform(title, corner), run_time=0.8)

        # ---------------- Segment 2: one pass ----------------
        prover = Rectangle(width=PRV_R - PRV_L, height=PRV_H, stroke_width=5, color=PROVER_C)
        prover.move_to([(PRV_L + PRV_R) / 2, PIPE_Y, 0])
        pipe_in = Line([-6.9, PIPE_Y, 0], [PRV_L, PIPE_Y, 0], stroke_width=6)
        pipe_out = Line([PRV_R, PIPE_Y, 0], [6.9, PIPE_Y, 0], stroke_width=6)
        flow = Arrow([-6.8, PIPE_Y + 0.35, 0], [-5.9, PIPE_Y + 0.35, 0], buff=0, stroke_width=3,
                     color=GREY_INK, max_tip_length_to_length_ratio=0.3)
        flow_lbl = label("flow", FS_TAG, GREY_INK).next_to(flow, UP, 0.08)
        top_y = PIPE_Y + PRV_H / 2
        dets = VGroup()
        for x, name in ((D1_X, "D1"), (D2_X, "D2")):
            tri = Triangle(stroke_width=3, color=INK, fill_color=INK, fill_opacity=1)
            tri.scale(0.12).rotate(PI).move_to([x, top_y + 0.12, 0])
            tick = DashedLine([x, top_y, 0], [x, PIPE_Y - PRV_H / 2, 0], stroke_width=2,
                              color=GREY_INK)
            dets.add(VGroup(tri, tick, label(name, FS_LABEL, weight=BOLD).next_to(tri, UP, 0.1)))
        prv_lbl = label("Compact prover", FS_LABEL, PROVER_C).next_to(prover, DOWN, 0.25)
        prv_lbl.align_to(prover, LEFT)

        piston_x = ValueTracker(STANDBY_X)
        piston = always_redraw(lambda: Rectangle(
            width=0.22, height=PRV_H - 0.08, stroke_width=3, color=INK, fill_color=INK,
            fill_opacity=0.85).move_to([piston_x.get_value(), PIPE_Y, 0]))

        def swept():
            x = min(max(piston_x.get_value(), D1_X), D2_X)
            w = max(x - D1_X, 0.001)
            return Rectangle(width=w, height=PRV_H - 0.1, stroke_width=0, fill_color=PROVER_C,
                             fill_opacity=0.28).move_to([D1_X + w / 2, PIPE_Y, 0])

        vol = always_redraw(swept)
        pulses = ValueTracker(0)
        counter = always_redraw(lambda: label(f"meter pulses: {pulses.get_value():,.0f}",
                                              FS_LABEL, METER_C).move_to([0, 2.0, 0]))
        one_pass = label("1 pass  =  piston D1 → D2  =  one BPV", FS_BODY, weight=BOLD)
        one_pass.move_to(DOWN * 2.2)
        ret = CurvedArrow([D2_X + 0.6, PIPE_Y - 0.9, 0], [STANDBY_X, PIPE_Y - 0.9, 0],
                          angle=-TAU / 8, stroke_width=3, color=GREY_INK)
        ret_lbl = label("hydraulic return to standby  →  ready for the next pass",
                        FS_LABEL, GREY_INK).move_to(DOWN * 3.1)

        self.play(Create(pipe_in), Create(prover), Create(pipe_out), run_time=1.3)
        self.play(GrowArrow(flow), FadeIn(flow_lbl), FadeIn(prv_lbl), FadeIn(dets), run_time=1.0)
        self.add(vol, piston)
        self.play(piston_x.animate.set_value(D1_X), run_time=0.8, rate_func=linear)
        self.add(counter)
        self.play(piston_x.animate.set_value(D2_X), pulses.animate.set_value(D.RUN_PULSES[0]),
                  run_time=3.5, rate_func=linear)
        self.play(piston_x.animate.set_value(D2_X + 0.6), run_time=0.4, rate_func=linear)
        self.play(Write(one_pass), run_time=1.2)
        self.sync(at(2, 0.55))
        self.play(FadeOut(vol), Create(ret), run_time=0.8)
        self.play(piston_x.animate.set_value(STANDBY_X), run_time=2.0)
        self.play(FadeIn(ret_lbl, shift=UP * 0.1), run_time=0.8)
        self.sync(START[2] - 0.6)
        self.remove(counter, piston)
        clear(keep=(title,))

        # ---------------- Segment 3: runs made of passes ----------------
        heading = Text("Run = average of consecutive passes", font_size=FS_HEADING - 4,
                       weight=BOLD).move_to(UP * 2.6)
        cell_w, cell_h = 1.25, 0.5
        rows = VGroup()
        for r in range(1, D.RUN_COUNT + 1):
            name = label(f"Run {r}", FS_LABEL, weight=BOLD)
            cells = VGroup(*[
                VGroup(Rectangle(width=cell_w, height=cell_h, stroke_width=3, color=PROVER_C),
                       label(f"pass {p}", FS_TAG, PROVER_C))
                for p in range(1, D.PASSES_PER_RUN + 1)])
            for c in cells:
                c[1].move_to(c[0])
            cells.arrange(RIGHT, buff=0.12)
            arrow = label("→", FS_LABEL, GREY_INK)
            res = label("MF, K", FS_LABEL, METER_C, weight=BOLD)
            rows.add(VGroup(name, cells, arrow, res).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(LEFT * 1.2 + DOWN * 0.1)
        avg_note = label("average", FS_TAG, GREY_INK).next_to(rows[0][2], UP, 0.05)
        total = label(f"{D.PASSES_PER_RUN} passes × {D.RUN_COUNT} runs = {D.TOTAL_PASSES} passes",
                      FS_BODY, weight=BOLD).move_to(DOWN * 2.35)
        cap = VGroup(label("Some procedures cap", FS_TAG, GREY_INK),
                     label("the passes per run, so", FS_TAG, GREY_INK),
                     label("averaging cannot hide", FS_TAG, GREY_INK),
                     label("poor repeatability", FS_TAG, GREY_INK)).arrange(DOWN, buff=0.06)
        cap_box = boxed(cap, GREY_INK, 0.18)
        VGroup(cap, cap_box).next_to(rows, RIGHT, 0.5)
        demo = label("Illustrative data", FS_TAG, GREY_INK).next_to(title, DOWN, 0.2)
        demo.align_to(title, LEFT)

        self.play(Write(heading), run_time=1.2)
        self.play(FadeIn(rows[0][0]), LaggedStart(*[Create(c) for c in rows[0][1]],
                                                  lag_ratio=0.3), run_time=1.2)
        self.play(FadeIn(rows[0][2]), FadeIn(avg_note), Write(rows[0][3]), run_time=1.0)
        self.sync(at(3, 0.3))
        self.play(FadeIn(demo), LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in rows[1:]],
                                            lag_ratio=0.35), run_time=2.2)
        self.sync(at(3, 0.5))
        self.play(Write(total), run_time=1.2)
        self.sync(at(3, 0.72))
        self.play(Create(cap_box), FadeIn(cap), run_time=1.0)
        self.sync(START[3] - 0.6)
        clear(keep=(title,))

        # ---------------- Segment 4: pass time and nominal frequency ----------------
        h4 = Text("How long is one pass?", font_size=FS_HEADING, weight=BOLD).move_to(UP * 2.6)
        eq_t = label("Pass time  =  BPV ÷ Q × 3600", FS_EQUATION, weight=BOLD).move_to(UP * 1.5)
        val_t = label(f"= {BPV_TXT} m³ ÷ {Q_TXT} m³/h × 3600  =  {PASS_TXT} s", FS_BODY)
        val_t.next_to(eq_t, DOWN, 0.3)
        # timeline bar: one pass
        bar_l, bar_r, bar_y = -4.5, 4.5, -0.5
        axis = Line([bar_l, bar_y, 0], [bar_r, bar_y, 0], stroke_width=3, color=GREY_INK)
        t_val = ValueTracker(0)
        bar = always_redraw(lambda: Rectangle(
            width=max((bar_r - bar_l) * t_val.get_value() / D.PASS_TIME, 0.001), height=0.35,
            stroke_width=0, fill_color=PROVER_C, fill_opacity=0.5)
            .move_to([bar_l, bar_y + 0.2, 0], aligned_edge=LEFT))
        clock = always_redraw(lambda: label(f"{t_val.get_value():.3f} s", FS_LABEL, PROVER_C)
                              .next_to([bar_r, bar_y + 0.2, 0], RIGHT, 0.2))
        d1t = label("D1", FS_TAG).next_to([bar_l, bar_y, 0], DOWN, 0.1)
        d2t = label("D2", FS_TAG).next_to([bar_r, bar_y, 0], DOWN, 0.1)
        eq_f = label(f"Frequency = Q × K ÷ 3600 = {Q_TXT} × {K_NOM_TXT} ÷ 3600", FS_LABEL,
                     METER_C).move_to(DOWN * 1.7)
        val_f = label(f"≈ {FREQ_TXT} Hz  (nominal, with nominal K)", FS_BODY, METER_C,
                      weight=BOLD).next_to(eq_f, DOWN, 0.2)
        note_f = label("Actual pulses per pass differ slightly: corrections and MF",
                       FS_LABEL, GREY_INK).move_to(DOWN * 3.2)

        self.play(Write(h4), run_time=1.0)
        self.play(Write(eq_t), run_time=1.5)
        self.sync(at(4, 0.2))
        self.play(FadeIn(val_t), run_time=1.0)
        self.play(Create(axis), FadeIn(d1t), FadeIn(d2t), run_time=0.6)
        self.add(bar, clock)
        self.sync(at(4, 0.3))
        self.play(t_val.animate.set_value(D.PASS_TIME), run_time=D.PASS_TIME, rate_func=linear)
        self.play(Circumscribe(val_t, color=INK), run_time=1.0)
        self.sync(at(4, 0.5))
        self.play(Write(eq_f), run_time=1.3)
        self.play(FadeIn(val_f, shift=UP * 0.1), run_time=1.0)
        self.sync(at(4, 0.8))
        self.play(FadeIn(note_f), run_time=1.0)
        self.sync(START[4] - 0.6)
        self.remove(bar, clock)
        clear(keep=(title,))

        # ---------------- Segment 5: repeatability ----------------
        h5 = Text("Repeatability", font_size=FS_HEADING, weight=BOLD).move_to(UP * 2.7)
        formula = label("(K max − K min) ÷ K min × 100", FS_EQUATION, weight=BOLD)
        formula.move_to(UP * 1.8)
        table = VGroup()
        head_row = VGroup(label("Run", FS_LABEL, GREY_INK), label("K-factor (pls/m³)", FS_LABEL,
                                                                  GREY_INK))
        table.add(head_row)
        for r in D.RUNS:
            table.add(VGroup(label(f"{r['run']}", FS_LABEL), label(f"{r['k']:.3f}", FS_LABEL)))
        for row in table:
            row[0].set_x(-4.6)
            row[1].set_x(-2.2)
        table.arrange(DOWN, buff=0.14).move_to([-3.4, -0.7, 0])
        for row in table:
            row[0].set_x(-4.6)
            row[1].set_x(-2.2)
        i_max = max(range(len(D.RUNS)), key=lambda i: D.RUNS[i]["k"]) + 1
        i_min = min(range(len(D.RUNS)), key=lambda i: D.RUNS[i]["k"]) + 1
        mx_box = SurroundingRectangle(table[i_max], color=METER_C, buff=0.08, stroke_width=3)
        mn_box = SurroundingRectangle(table[i_min], color=PROVER_C, buff=0.08, stroke_width=3)
        mx_tag = label("max", FS_TAG, METER_C).next_to(mx_box, RIGHT, 0.15)
        mn_tag = label("min", FS_TAG, PROVER_C).next_to(mn_box, RIGHT, 0.15)
        calc = VGroup(
            label(f"({KMAX_TXT} − {KMIN_TXT})", FS_LABEL),
            label(f"÷ {KMIN_TXT} × 100", FS_LABEL),
            label(f"= {REP_TXT} %", FS_EQUATION, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([2.9, -0.2, 0])
        verdict = label(f"≤ {LIM_TXT} %  →  ACCEPTED", FS_BODY, OK_C, weight=BOLD)
        verdict.next_to(calc, DOWN, 0.4).align_to(calc, LEFT)

        self.play(Write(h5), run_time=1.0)
        self.play(Write(formula), run_time=1.8)
        self.sync(at(5, 0.3))
        self.play(FadeIn(table), run_time=1.0)
        self.play(Create(mx_box), FadeIn(mx_tag), run_time=0.8)
        self.sync(at(5, 0.55))
        self.play(Create(mn_box), FadeIn(mn_tag), run_time=0.8)
        self.play(FadeIn(calc[:2]), run_time=1.0)
        self.sync(at(5, 0.72))
        self.play(Write(calc[2]), run_time=1.0)
        self.sync(at(5, 0.85))
        self.play(FadeIn(verdict, shift=UP * 0.1), run_time=0.8)
        self.sync(START[5] - 0.6)
        clear(keep=(title,))

        # ---------------- Segment 6: API MPMS 4.8 table ----------------
        h6 = Text("API MPMS Ch. 4.8", font_size=FS_HEADING, weight=BOLD).move_to(UP * 2.7)
        h6b = label(f"Repeatability limit vs. number of runs  (MF uncertainty ±{D.MF_UNCERTAINTY_TARGET} %)",
                    FS_LABEL, GREY_INK).next_to(h6, DOWN, 0.2)
        fit(h6b)
        shown = [n for n in (3, 4, 5, 6)]
        api_rows = VGroup(VGroup(label("Runs", FS_LABEL, GREY_INK),
                                 label("Max repeatability", FS_LABEL, GREY_INK)))
        for n in shown:
            api_rows.add(VGroup(label(f"{n}", FS_BODY, weight=BOLD),
                                label(f"{D.API_48_REPEATABILITY[n]:.2f} %", FS_BODY)))
        api_rows.add(VGroup(label("…", FS_BODY, GREY_INK), label("…", FS_BODY, GREY_INK)))
        api_rows.arrange(DOWN, buff=0.18).move_to([-2.8, -0.6, 0])
        for row in api_rows:
            row[0].set_x(-4.3)
            row[1].set_x(-1.9)
        hl = SurroundingRectangle(api_rows[shown.index(D.RUN_COUNT) + 1], color=OK_C, buff=0.1,
                                  stroke_width=4)
        hl_tag = label("this series", FS_TAG, OK_C).next_to(hl, LEFT, 0.15)
        wider = VGroup(label("More runs  →  wider limit", FS_BODY, weight=BOLD),
                       label("(the average becomes more reliable)", FS_LABEL, GREY_INK)
                       ).arrange(DOWN, buff=0.15).move_to([3.2, 0.2, 0])
        fail = VGroup(label("Repeatability fails?", FS_LABEL, METER_C, weight=BOLD),
                      label("common practice: discard", FS_LABEL, METER_C),
                      label("the data and re-prove", FS_LABEL, METER_C)
                      ).arrange(DOWN, buff=0.1).move_to([3.2, -2.0, 0])
        fail_box = boxed(fail, METER_C, 0.2)

        self.play(Write(h6), run_time=1.0)
        self.sync(at(6, 0.15))
        self.play(FadeIn(h6b), FadeIn(api_rows[0]), run_time=1.0)
        self.sync(at(6, 0.42))
        for k, frac in ((1, 0.42), (2, 0.5), (3, 0.57)):
            self.sync(at(6, frac))
            self.play(FadeIn(api_rows[k], shift=RIGHT * 0.1), run_time=0.6)
        self.play(Create(hl), FadeIn(hl_tag), run_time=0.8)
        self.sync(at(6, 0.66))
        self.play(FadeIn(api_rows[4]), FadeIn(api_rows[5]), FadeIn(wider), run_time=1.0)
        self.sync(at(6, 0.8))
        self.play(Create(fail_box), FadeIn(fail), run_time=1.0)
        self.sync(START[6] - 0.6)
        clear(keep=(title,))

        # ---------------- Segment 7: Coriolis manufactured pulses ----------------
        h7 = Text("Coriolis specifics", font_size=FS_HEADING, weight=BOLD).move_to(UP * 2.7)

        def chain(names, color):
            boxes = VGroup()
            for n in names:
                t = label(n, FS_LABEL, color)
                boxes.add(VGroup(RoundedRectangle(width=t.width + 0.5, height=0.7,
                                                  corner_radius=0.12, stroke_width=3,
                                                  color=color), t))
            for b in boxes:
                b[1].move_to(b[0])
            boxes.arrange(RIGHT, buff=0.6)
            arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.08,
                                    stroke_width=3, color=color)
                              for i in range(len(boxes) - 1)])
            return VGroup(boxes, arrows)

        mech = chain(["rotating element", "pulses"], GREY_INK)
        cor = chain(["vibrating tubes", "transmitter signal processing", "manufactured pulses"],
                    METER_C)
        mech_lbl = label("Turbine / PD", FS_LABEL, GREY_INK, weight=BOLD)
        cor_lbl = label("Coriolis", FS_LABEL, METER_C, weight=BOLD)
        r1 = VGroup(mech_lbl, mech).arrange(RIGHT, buff=0.4)
        r2 = VGroup(cor_lbl, cor).arrange(RIGHT, buff=0.4)
        fit(VGroup(r1, r2).arrange(DOWN, buff=0.4, aligned_edge=LEFT)).move_to(UP * 1.15)
        delay = label("small delay", FS_TAG, METER_C).next_to(cor[1][1], DOWN, 0.1)
        damp = label("Damping set to fastest response  →  noisier reading", FS_BODY)
        damp.move_to(DOWN * 0.5)
        fix = label("Remedy: adequate pass time  +  average several passes per run",
                    FS_LABEL, OK_C, weight=BOLD).move_to(DOWN * 1.3)
        fit(fix)
        # pass time comparison bars
        scale = 2.0                       # units per second
        b_min = Rectangle(width=D.CORIOLIS_MIN_PASS_TIME * scale, height=0.32, stroke_width=0,
                          fill_color=GREY_INK, fill_opacity=0.6)
        b_our = Rectangle(width=D.PASS_TIME * scale, height=0.32, stroke_width=0,
                          fill_color=PROVER_C, fill_opacity=0.6)
        bars = VGroup(b_min, b_our).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        bars.move_to([-1.2, -2.6, 0], aligned_edge=LEFT)
        l_min = label(f"{D.CORIOLIS_MIN_PASS_TIME} s  typical minimum", FS_TAG, GREY_INK)
        l_min.next_to(b_min, RIGHT, 0.2)
        l_our = label(f"{PASS_TXT} s  our pass", FS_TAG, PROVER_C, weight=BOLD)
        l_our.next_to(b_our, RIGHT, 0.2)
        bar_hdr = label("Pass time", FS_LABEL, weight=BOLD).next_to(bars, LEFT, 0.4)

        self.play(Write(h7), run_time=1.0)
        self.sync(at(7, 0.12))
        self.play(FadeIn(r1), run_time=0.8)
        self.play(FadeIn(cor_lbl), FadeIn(cor[0][0]), run_time=0.6)
        self.play(GrowArrow(cor[1][0]), FadeIn(cor[0][1]), run_time=0.7)
        self.play(GrowArrow(cor[1][1]), FadeIn(cor[0][2]), FadeIn(delay), run_time=0.7)
        self.sync(at(7, 0.42))
        self.play(Write(damp), run_time=1.3)
        self.sync(at(7, 0.62))
        self.play(FadeIn(fix, shift=UP * 0.1), run_time=1.0)
        self.sync(at(7, 0.78))
        self.play(FadeIn(bar_hdr), GrowFromEdge(b_min, LEFT), FadeIn(l_min), run_time=0.8)
        self.play(GrowFromEdge(b_our, LEFT), FadeIn(l_our), run_time=1.0)
        self.sync(START[7] - 0.6)
        clear(keep=(title,))

        # ---------------- Segment 8: mass or volumetric proving ----------------
        h8 = Text("Mass or volumetric proving", font_size=FS_HEADING, weight=BOLD)
        h8.move_to(UP * 2.7)

        def card(lines, color, w=5.6, h=3.2):
            txt = VGroup(*[label(t, FS_BODY if i == 0 else FS_LABEL, color,
                                 weight=BOLD if i == 0 else NORMAL)
                           for i, t in enumerate(lines)]).arrange(DOWN, buff=0.18)
            b = Rectangle(width=w, height=h, stroke_width=4, color=color)
            fit(txt, w - 0.4).move_to(b)
            return VGroup(b, txt)

        c_mass = card(["Mass", "MF (mass)", "with a volume prover:", "mass = volume × density",
                       "→ density must be stable"], GREY_INK)
        c_vol = card(["Volumetric", "MF (volume)", "this series, as in the manual",
                      "report carries CTL · CPL"], PROVER_C)
        cards = fit(VGroup(c_mass, c_vol).arrange(RIGHT, buff=0.6)).move_to(DOWN * 0.2)
        chosen = label("✓", FS_HEADING, OK_C, weight=BOLD).next_to(c_vol[0], UP, 0.1)
        chosen.align_to(c_vol[0], RIGHT)
        zero = label("Re-prove whenever the meter is zeroed", FS_BODY, weight=BOLD)
        zero.move_to(DOWN * 2.8)

        self.play(Write(h8), run_time=1.0)
        self.play(Create(c_mass[0]), FadeIn(c_mass[1][:2]),
                  Create(c_vol[0]), FadeIn(c_vol[1][:2]), run_time=1.2)
        self.sync(at(8, 0.2))
        self.play(FadeIn(c_vol[1][2]), FadeIn(chosen), run_time=0.8)
        self.sync(at(8, 0.38))
        self.play(FadeIn(c_vol[1][3]), run_time=0.8)
        self.sync(at(8, 0.55))
        self.play(FadeIn(c_mass[1][2:]), run_time=1.0)
        self.sync(at(8, 0.84))
        self.play(Write(zero), run_time=1.0)
        self.sync(START[8] - 0.6)
        clear(keep=(title,))

        # ---------------- Segment 9: summary ----------------
        h9 = Text("In one sentence", font_size=FS_HEADING, weight=BOLD).move_to(UP * 2.4)
        summ = VGroup(
            label("Pass  =  one piston stroke D1 → D2", FS_SUMMARY),
            label("Run  =  average of several passes", FS_SUMMARY),
            label("Repeatability  =  spread of the runs, within a limit", FS_SUMMARY),
            label("that widens with the number of runs (API 4.8)", FS_SUMMARY, GREY_INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.2)
        fit(summ)
        nxt = label("Next: compact prover construction (10 components)", FS_BODY, GREY_INK)
        nxt.move_to(DOWN * 2.8)

        self.play(Write(h9), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.1) for s in summ], lag_ratio=0.5),
                  run_time=3.5)
        self.sync(at(9, 0.72))
        self.play(FadeIn(nxt, shift=UP * 0.1), run_time=1.0)
        self.sync(START[9] + 2.0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="low-quality layout check")
    args = parser.parse_args()
    print(build(__file__, "ProverEp02", NARRATION, preview=args.preview))
