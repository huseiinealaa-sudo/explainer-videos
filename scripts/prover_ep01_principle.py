"""Daniel Compact Prover series, episode 1: proving principle and the MF equation.

Every number on screen or in the narration comes from prover_demo_data.

Build (from the repo root):
    python scripts/prover_ep01_principle.py --preview   # 480p15 -> tmp/prover_ep01_principle/preview.mp4
    python scripts/prover_ep01_principle.py             # 1080p30 -> output/prover_ep01_principle.mp4
"""
import argparse

from style import *
import prover_demo_data as D

# Approved, fully diacritized narration — one entry per scene.
NARRATION = [
    # 1 disclaimer + intro
    "هٰذِهِ مَادَّةٌ تَعْلِيمِيَّةٌ، وَالمَرْجِعُ المُلْزِمُ هُوَ دَلِيلُ الشَّرِكَةِ المُصَنِّعَةِ وَإِجْرَاءَاتُ المَوْقِعِ المُعْتَمَدَةُ. فِي هٰذِهِ الحَلْقَةِ: مَبْدَأُ الإِثْبَاتِ، وَمُعَادَلَةُ مُعَامِلِ العَدَّادِ.",
    # 2 definition
    "الإِثْبَاتُ هُوَ مُقَارَنَةُ قِرَاءَةِ العَدَّادِ بِحَجْمٍ مَرْجِعِيٍّ مَعْرُوفٍ بِدِقَّةٍ، يُوَفِّرُهُ المُعَايِرُ. وَالنَّاتِجُ رَقْمٌ وَاحِدٌ: مُعَامِلُ العَدَّادِ، إِمْ إِفْ، يُضْرَبُ فِي قِرَاءَةِ العَدَّادِ فَيُصَحِّحُهَا، وَعَلَيْهِ تَقُومُ دِقَّةُ نَقْلِ المِلْكِيَّةِ.",
    # 3 loop: series, piston, D1-D2, BPV, waterdraw
    "يُرَكَّبُ العَدَّادُ وَالمُعَايِرُ عَلَى التَّوَالِي، فَيَمُرُّ السَّائِلُ نَفْسُهُ فِيهِمَا. وَحِينَ يَقْطَعُ المِكْبَسُ المَسَافَةَ بَيْنَ الكَاشِفَيْنِ، دِي وَنْ وَدِي تُو، يُزِيحُ حَجْمًا مَعْرُوفًا هُوَ الحَجْمُ الأَسَاسِيُّ، بِي بِي فِي، المُثْبَتُ فِي شَهَادَةِ المُعَايَرَةِ بِالمَاءِ، وُوتَر دْرُو.",
    # 4 pulses, interpolation, correction, division
    "وَفِي الأَثْنَاءِ تَعُدُّ الحَاسِبَةُ التَّدَفُّقِيَّةُ نَبَضَاتِ العَدَّادِ. وَلِأَنَّ حَجْمَ المُعَايِرِ المُدْمَجِ صَغِيرٌ، تَشْتَرِطُ الشَّرِكَةُ المُصَنِّعَةُ حِسَابَ أَجْزَاءِ النَّبْضَةِ أَيْضًا، وَنَشْرَحُهُ فِي الحَلْقَةِ الخَامِسَةِ. ثُمَّ تُصَحَّحُ الكَمِّيَّتَانِ إِلَى الظُّرُوفِ المَرْجِعِيَّةِ نَفْسِهَا، وَتُقْسَمُ إِحْدَاهُمَا عَلَى الأُخْرَى.",
    # 5 idea in one line
    "بِاخْتِصَارٍ: المُعَايِرُ لَا يُعَايِرُ العَدَّادَ بِطَرِيقَةٍ سِحْرِيَّةٍ؛ هُوَ يُوَفِّرُ مَرْجِعًا حَجْمِيًّا مَعْلُومًا، وَالعَدَّادُ يُعْطِي قِرَاءَةً مُسْتَقِلَّةً لِلسَّائِلِ نَفْسِهِ، وَالحَاسِبَةُ تُقَارِنُ وَتَحْسُبُ وَتُوَثِّقُ.",
    # 6 equation, prover side
    "فِي بَسْطِ المُعَادَلَةِ جَانِبُ المُعَايِرِ: الحَجْمُ الأَسَاسِيُّ مَضْرُوبًا فِي أَرْبَعَةِ مُعَامِلَاتٍ. سِي تِي إِسْ بِي وَسِي بِي إِسْ بِي يُصَحِّحَانِ أَثَرَ الحَرَارَةِ وَالضَّغْطِ فِي جِسْمِ المُعَايِرِ، وَسِي تِي إِلْ بِي وَسِي بِي إِلْ بِي يُصَحِّحَانِ أَثَرَهُمَا فِي السَّائِلِ دَاخِلَهُ.",
    # 7 equation, meter side
    "وَفِي المَقَامِ جَانِبُ العَدَّادِ: الحَجْمُ المُشَارُ إِلَيْهِ، آيْ فِي، وَهُوَ عَدَدُ النَّبَضَاتِ مَقْسُومًا عَلَى مُعَامِلِ كِي الاسْمِيِّ، مَضْرُوبًا فِي سِي تِي إِلْ إِمْ وَسِي بِي إِلْ إِمْ لِتَصْحِيحِ السَّائِلِ عِنْدَ العَدَّادِ.",
    # 8 reading MF
    "وَمُعَامِلُ العَدَّادِ نِسْبَةٌ، لَا فَرْقٌ. إِذَا كَانَ أَصْغَرَ مِنْ وَاحِدٍ، فَالعَدَّادُ يُسَجِّلُ أَكْثَرَ مِنَ الحَجْمِ الحَقِيقِيِّ، وَإِذَا كَانَ أَكْبَرَ مِنْ وَاحِدٍ، فَهُوَ يُسَجِّلُ أَقَلَّ. وَالانْحِرَافُ هُوَ الفَرْقُ بَيْنَهُ وَبَيْنَ الوَاحِدِ.",
    # 9 example (spoken numbers are checked against prover_demo_data below)
    "فِي بَيَانَاتِنَا التَّوْضِيحِيَّةِ، مُتَوَسِّطُ المُعَامِلِ صِفْرٌ فَاصِلَةُ تِسْعَةٍ تِسْعَةٍ تِسْعَةٍ؛ أَيْ أَنَّ العَدَّادَ يُسَجِّلُ زِيَادَةً بِنَحْوِ عُشْرٍ فِي المِئَةِ. وَبِصِيغَةٍ أُخْرَى: كِي المُثْبَتُ يُسَاوِي كِي الاسْمِيَّ مَقْسُومًا عَلَى المُعَامِلِ، أَيْ نَحْوَ سِتِّينَ أَلْفًا وَسِتِّينَ نَبْضَةً لِكُلِّ مِتْرٍ مُكَعَّبٍ.",
    # 10 K or MF + outro
    "وَانْتَبِهْ: يُطَبَّقُ أَحَدُهُمَا فَقَطْ، كِي المُثْبَتُ أَوْ مُعَامِلُ العَدَّادِ، لَا كِلَاهُمَا؛ لِأَنَّ تَطْبِيقَهُمَا مَعًا يَعْنِي تَصْحِيحَ القِرَاءَةِ مَرَّتَيْنِ. فِي الحَلْقَةِ القَادِمَةِ: الشَّوْطُ، وَالجَوْلَةُ، وَالتَّكْرَارِيَّةُ.",
]

# The spoken numbers in segment 9 are rounded from the demo data; stop if it drifts.
assert round(D.MF_AVG, 3) == 0.999                  # "0.999"
assert round((1 - D.MF_AVG) * 100, 1) == 0.1        # "about one tenth of a percent", reads high
assert round(D.K_NOMINAL) == 60000                  # "sixty thousand"
assert round(D.K_FINAL) == 60060                    # "about 60,060"

AUDIO_DIR = BUILD_DIR / "prover_ep01_principle" / "audio"

PROVER_C = "#1f5fa8"            # prover side of the equation and diagram
METER_C = "#c25a12"             # meter side

MF_TXT = f"{D.MF_AVG:.5f}"
K_NOM_TXT = f"{D.K_NOMINAL:.0f}"
K_FIN_TXT = f"{D.K_FINAL:.3f}"
BPV_TXT = f"{D.BPV:.4f}"
DEV_PCT = (D.MF_AVG - 1) * 100

# Diagram geometry
PIPE_Y = -0.6
MTR_X = -4.6
PRV_L, PRV_R = -2.6, 3.6
PRV_H = 1.2
D1_X, D2_X = -0.9, 2.6
PISTON_START = -2.2


def label(text, size=FS_LABEL, color=INK, **kw):
    return Text(text, font_size=size, color=color, **kw)


def fit(mob, width=13.2):
    """Keep a group inside the 16:9 frame with a side margin."""
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def boxed(mob, color=INK, buff=0.3):
    return SurroundingRectangle(mob, buff=buff, corner_radius=0.15, stroke_width=4, color=color)


class ProverEp01(SyncedScene):
    def construct(self):
        START = segment_starts(AUDIO_DIR, len(NARRATION))

        # ---------------- Segment 1: disclaimer + title ----------------
        series = label("Daniel Compact Prover  ·  Episode 1", FS_SUBTITLE, GREY_INK)
        title = Text("Proving Principle & the Meter Factor", font_size=FS_TITLE - 8, weight=BOLD)
        line = Line(LEFT, RIGHT).set_width(title.width)
        fit(title, 12.6)
        line.set_width(title.width)
        head = VGroup(series, title, line).arrange(DOWN, buff=0.35).move_to(UP * 1.2)
        note = label("Educational material. The binding reference is the manufacturer's manual",
                     FS_NOTE, GREY_INK)
        note2 = label("and the approved site procedures.", FS_NOTE, GREY_INK)
        notes = VGroup(note, note2).arrange(DOWN, buff=0.15).move_to(DOWN * 1.6)
        notes_box = boxed(notes, GREY_INK, 0.25)

        self.play(FadeIn(series, shift=DOWN * 0.2), run_time=1.0)
        self.play(Write(title), run_time=2.0)
        self.play(Create(line), Create(notes_box), FadeIn(notes), run_time=1.5)
        self.sync(START[1] - 0.8)
        corner = label("Ep 1 · Proving Principle", FS_BODY - 6, weight=BOLD).to_corner(UL, buff=0.4)
        self.play(FadeOut(VGroup(series, line, notes, notes_box)),
                  Transform(title, corner), run_time=0.8)

        # ---------------- Segment 2: definition ----------------
        t0 = START[1]
        heading = Text("Proving", font_size=FS_HEADING, weight=BOLD).move_to(UP * 2.6)
        m_txt = VGroup(label("Meter reading", FS_BODY, METER_C, weight=BOLD),
                       label("indicated volume", FS_NOTE, METER_C)).arrange(DOWN, buff=0.12)
        p_txt = VGroup(label("Known reference volume", FS_BODY, PROVER_C, weight=BOLD),
                       label("from the prover", FS_NOTE, PROVER_C)).arrange(DOWN, buff=0.12)
        m_box, p_box = boxed(m_txt, METER_C), boxed(p_txt, PROVER_C)
        m_grp, p_grp = VGroup(m_box, m_txt), VGroup(p_box, p_txt)
        vs = label("compared with", FS_LABEL, GREY_INK)
        row = fit(VGroup(m_grp, vs, p_grp).arrange(RIGHT, buff=0.5)).move_to(UP * 1.1)

        mf = Text("Meter Factor  (MF)", font_size=FS_EQUATION, weight=BOLD).move_to(DOWN * 0.6)
        arr_m = Arrow(m_box.get_bottom(), mf.get_top() + LEFT * 1.2, buff=0.12, stroke_width=4)
        arr_p = Arrow(p_box.get_bottom(), mf.get_top() + RIGHT * 1.2, buff=0.12, stroke_width=4)
        use = label("Corrected volume  =  MF × meter reading", FS_BODY).move_to(DOWN * 1.9)
        ct = label("Basis of custody-transfer accuracy", FS_LABEL, GREY_INK).move_to(DOWN * 2.8)

        self.play(Write(heading), run_time=1.0)
        self.play(Create(m_box), FadeIn(m_txt), run_time=1.2)
        self.play(FadeIn(vs), run_time=0.6)
        self.sync(t0 + 3.0)
        self.play(Create(p_box), FadeIn(p_txt), run_time=1.2)
        self.sync(t0 + 7.5)
        self.play(GrowArrow(arr_m), GrowArrow(arr_p), Write(mf), run_time=1.5)
        self.sync(t0 + 11.0)
        self.play(Write(use), run_time=1.5)
        self.sync(t0 + 14.8)
        self.play(FadeIn(ct, shift=UP * 0.1), run_time=1.0)
        self.sync(START[2] - 0.6)
        self.play(FadeOut(VGroup(heading, m_grp, vs, p_grp, mf, arr_m, arr_p, use, ct)),
                  run_time=0.6)

        # ---------------- Segment 3: proving loop ----------------
        t0 = START[2]
        pipe_in = Line([-6.9, PIPE_Y, 0], [MTR_X - 0.8, PIPE_Y, 0], stroke_width=6)
        meter_body = RoundedRectangle(width=1.6, height=0.5, corner_radius=0.1,
                                      stroke_width=5, color=METER_C).move_to([MTR_X, PIPE_Y, 0])
        tube = ArcBetweenPoints([MTR_X - 0.55, PIPE_Y + 0.25, 0], [MTR_X + 0.55, PIPE_Y + 0.25, 0],
                                angle=-PI * 0.9, stroke_width=5, color=METER_C)
        meter = VGroup(meter_body, tube)
        meter_lbl = label("Coriolis meter", FS_LABEL, METER_C).next_to(meter_body, DOWN, 0.3)
        pipe_mid = Line([MTR_X + 0.8, PIPE_Y, 0], [PRV_L, PIPE_Y, 0], stroke_width=6)
        prover = Rectangle(width=PRV_R - PRV_L, height=PRV_H, stroke_width=5, color=PROVER_C)
        prover.move_to([(PRV_L + PRV_R) / 2, PIPE_Y, 0])
        prv_lbl = label("Compact prover", FS_LABEL, PROVER_C)
        prv_lbl.move_to([(PRV_L + PRV_R) / 2, PIPE_Y - 2.15, 0])
        pipe_out = Line([PRV_R, PIPE_Y, 0], [6.9, PIPE_Y, 0], stroke_width=6)
        flow_arrows = VGroup(*[Arrow([x, PIPE_Y + 0.35, 0], [x + 0.7, PIPE_Y + 0.35, 0], buff=0,
                                     stroke_width=3, color=GREY_INK,
                                     max_tip_length_to_length_ratio=0.3)
                               for x in (-6.6, -3.5, 4.5)])
        flow_lbl = label("flow", FS_TAG, GREY_INK).next_to(flow_arrows[0], UP, 0.08)

        top_y = PIPE_Y + PRV_H / 2
        dets = VGroup()
        det_lbls = VGroup()
        for x, name in ((D1_X, "D1"), (D2_X, "D2")):
            tri = Triangle(stroke_width=3, color=INK, fill_color=INK, fill_opacity=1)
            tri.scale(0.12).rotate(PI).move_to([x, top_y + 0.12, 0])
            tick = DashedLine([x, top_y, 0], [x, PIPE_Y - PRV_H / 2, 0], stroke_width=2,
                              color=GREY_INK)
            dets.add(VGroup(tri, tick))
            det_lbls.add(label(name, FS_LABEL, weight=BOLD).next_to(tri, UP, 0.1))

        piston_x = ValueTracker(PISTON_START)
        piston = always_redraw(lambda: Rectangle(
            width=0.22, height=PRV_H - 0.08, stroke_width=3, color=INK, fill_color=INK,
            fill_opacity=0.85).move_to([piston_x.get_value(), PIPE_Y, 0]))

        def swept():
            x = min(max(piston_x.get_value(), D1_X), D2_X)
            w = max(x - D1_X, 0.001)
            return Rectangle(width=w, height=PRV_H - 0.1, stroke_width=0, fill_color=PROVER_C,
                             fill_opacity=0.28).move_to([D1_X + w / 2, PIPE_Y, 0])

        vol = always_redraw(swept)
        bpv = label(f"BPV = {BPV_TXT} m³", FS_BODY - 4, PROVER_C, weight=BOLD)
        bpv.move_to([(D1_X + D2_X) / 2, PIPE_Y - 1.1, 0]).align_to([D1_X - 0.1, 0, 0], LEFT)
        wd = label("certified by waterdraw", FS_TAG, GREY_INK).next_to(bpv, DOWN, 0.12)
        brace = BraceBetweenPoints([D2_X, PIPE_Y - 0.65, 0], [D1_X, PIPE_Y - 0.65, 0],
                                   color=PROVER_C)

        self.play(Create(pipe_in), Create(meter), Create(pipe_mid), run_time=1.5)
        self.play(FadeIn(meter_lbl), run_time=0.6)
        self.play(Create(prover), Create(pipe_out), FadeIn(prv_lbl), run_time=1.3)
        self.play(*[GrowArrow(a) for a in flow_arrows], FadeIn(flow_lbl), run_time=1.0)
        self.add(vol, piston)
        self.sync(t0 + 5.6)
        self.play(FadeIn(dets), Write(det_lbls), run_time=1.0)
        self.play(piston_x.animate.set_value(D2_X + 0.5), run_time=5.0, rate_func=linear)
        self.play(GrowFromCenter(brace), Write(bpv), run_time=1.2)
        self.sync(t0 + 14.8)
        self.play(FadeIn(wd, shift=UP * 0.1), run_time=0.8)

        # ---------------- Segment 4: pulse counting, correction, division ----------------
        t0 = START[3]
        fc_title = label("Flow computer", FS_LABEL, weight=BOLD)
        pulses = ValueTracker(0)
        counter = always_redraw(lambda: label(f"N = {pulses.get_value():,.3f} pulses", FS_TAG)
                                .next_to(fc_title, DOWN, 0.12))
        fc_box = Rectangle(width=4.2, height=1.2, stroke_width=4, color=INK)
        fc_box.move_to([0.5, 2.2, 0])
        fc_title.move_to(fc_box.get_top() + DOWN * 0.35)
        sig_m = DashedLine([MTR_X, PIPE_Y + 0.75, 0], [MTR_X, 2.2, 0], stroke_width=3,
                           color=METER_C)
        sig_m2 = DashedLine([MTR_X, 2.2, 0], fc_box.get_left(), stroke_width=3, color=METER_C)
        sig_d1 = DashedLine([D1_X, top_y + 0.55, 0], [D1_X, fc_box.get_bottom()[1], 0],
                            stroke_width=3, color=PROVER_C)
        sig_d2 = DashedLine([D2_X, top_y + 0.55, 0], [D2_X, fc_box.get_bottom()[1], 0],
                            stroke_width=3, color=PROVER_C)
        pls_lbl = label("meter pulses", FS_TAG, METER_C).next_to(sig_m2, UP, 0.08)
        det_sig = label("detector signals", FS_TAG, PROVER_C).next_to(sig_d2, RIGHT, 0.1)

        self.play(FadeOut(wd), FadeOut(brace), FadeOut(bpv), run_time=0.5)
        self.play(Create(fc_box), Write(fc_title), run_time=1.0)
        self.play(Create(sig_m), Create(sig_m2), FadeIn(pls_lbl),
                  Create(sig_d1), Create(sig_d2), FadeIn(det_sig), run_time=1.2)
        self.add(counter)
        piston_x.set_value(PISTON_START)
        self.play(piston_x.animate.set_value(D1_X), run_time=0.8, rate_func=linear)
        self.play(piston_x.animate.set_value(D2_X), pulses.animate.set_value(D.RUN_PULSES[0]),
                  run_time=3.5, rate_func=linear)
        self.play(piston_x.animate.set_value(D2_X + 0.5), run_time=0.4, rate_func=linear)

        frac = label("whole pulses + a fraction of a pulse", FS_TAG, GREY_INK)
        frac2 = label("(pulse interpolation: Episode 5)", FS_TAG, GREY_INK)
        fr = VGroup(frac, frac2).arrange(DOWN, buff=0.08).move_to([(D1_X + D2_X) / 2, -1.75, 0])
        self.sync(t0 + 6.0)
        self.play(FadeIn(fr, shift=LEFT * 0.1), run_time=1.0)

        div_p = label("Prover volume @ reference conditions", FS_LABEL, PROVER_C)
        div_s = label("÷", FS_EQUATION, weight=BOLD)
        div_m = label("Meter volume @ reference conditions", FS_LABEL, METER_C)
        div = fit(VGroup(div_p, div_s, div_m).arrange(RIGHT, buff=0.3)).move_to([0, -2.9, 0])
        self.play(FadeOut(prv_lbl), FadeOut(meter_lbl), run_time=0.4)
        self.sync(t0 + 13.5)
        self.play(FadeIn(div_p, shift=UP * 0.1), FadeIn(div_m, shift=UP * 0.1), run_time=1.2)
        self.sync(t0 + 18.2)
        self.play(Write(div_s), Circumscribe(div, color=INK), run_time=1.5)
        diagram = VGroup(pipe_in, meter, pipe_mid, prover, pipe_out, flow_arrows, flow_lbl,
                         dets, det_lbls, fc_box, fc_title, sig_m, sig_m2, sig_d1, sig_d2,
                         pls_lbl, det_sig, fr, div)
        self.sync(START[4] - 0.6)
        self.play(FadeOut(diagram), FadeOut(counter), FadeOut(piston), FadeOut(vol),
                  run_time=0.6)
        self.remove(counter, piston, vol)

        # ---------------- Segment 5: the idea in one line ----------------
        t0 = START[4]
        idea = Text("The idea in one line", font_size=FS_HEADING, weight=BOLD).move_to(UP * 2.5)
        magic = label("No “magic” calibration", FS_BODY, GREY_INK).next_to(idea, DOWN, 0.4)

        def card(t1, t2, color):
            txt = VGroup(label(t1, FS_BODY, color, weight=BOLD),
                         label(t2, FS_LABEL, color)).arrange(DOWN, buff=0.2)
            b = Rectangle(width=4.1, height=2.0, stroke_width=4, color=color)
            fit(txt, 3.7).move_to(b)
            return VGroup(b, txt)

        c1 = card("Prover", "known reference volume", PROVER_C)
        c2 = card("Meter", "independent reading", METER_C)
        c3 = card("Flow computer", "compare · compute · record", INK)
        cards = fit(VGroup(c1, c2, c3).arrange(RIGHT, buff=0.3)).move_to(DOWN * 0.8)
        self.play(Write(idea), run_time=1.0)
        self.play(FadeIn(magic), run_time=0.8)
        self.sync(t0 + 4.5)
        self.play(Create(c1[0]), FadeIn(c1[1]), run_time=1.0)
        self.sync(t0 + 8.2)
        self.play(Create(c2[0]), FadeIn(c2[1]), run_time=1.0)
        self.sync(t0 + 11.3)
        self.play(Create(c3[0]), FadeIn(c3[1]), run_time=1.0)
        self.sync(START[5] - 0.6)
        self.play(FadeOut(VGroup(idea, magic, cards)), run_time=0.6)

        # ---------------- Segment 6: equation, prover side ----------------
        t0 = START[5]
        mf_eq = Text("MF =", font_size=FS_EQUATION + 4, weight=BOLD)
        num_terms = ["BPV", "CTSp", "CPSp", "CTLp", "CPLp"]
        num = VGroup()
        for i, s in enumerate(num_terms):
            if i:
                num.add(label("×", FS_EQUATION, PROVER_C))
            num.add(Text(s, font_size=FS_EQUATION, color=PROVER_C, weight=BOLD))
        num.arrange(RIGHT, buff=0.22)
        den_terms = ["IV", "CTLm", "CPLm"]
        den = VGroup()
        for i, s in enumerate(den_terms):
            if i:
                den.add(label("×", FS_EQUATION, METER_C))
            den.add(Text(s, font_size=FS_EQUATION, color=METER_C, weight=BOLD))
        den.arrange(RIGHT, buff=0.22)
        bar = Line(LEFT, RIGHT, stroke_width=4).set_width(num.width + 0.3)
        frac_grp = VGroup(num, bar, den).arrange(DOWN, buff=0.25)
        eq = VGroup(mf_eq, frac_grp).arrange(RIGHT, buff=0.35).move_to(UP * 0.3)

        side_p = label("■ prover side", FS_LABEL, PROVER_C)
        side_m = label("■ meter side", FS_LABEL, METER_C)
        VGroup(side_p, side_m).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.4)

        def tag(term, text, color, up=True):
            t = label(text, FS_TAG, color)
            t.next_to(term, UP if up else DOWN, 0.18)
            return t

        # num: [BPV, ×, CTSp, ×, CPSp, ×, CTLp, ×, CPLp]
        tg_bpv = tag(num[0], "base volume", PROVER_C)
        tg_ts = tag(num[2], "steel · temp.", PROVER_C)
        tg_ps = tag(num[4], "steel · press.", PROVER_C)
        tg_tl = tag(num[6], "liquid · temp.", PROVER_C)
        tg_pl = tag(num[8], "liquid · press.", PROVER_C)
        up_tags = VGroup(tg_ts, tg_tl)
        up_tags.shift(UP * 0.35)            # stagger so neighbours never overlap
        conn = VGroup(*[Line(t.get_bottom(), term.get_top(), stroke_width=1.5, color=GREY_INK,
                             buff=0.05)
                        for t, term in ((tg_ts, num[2]), (tg_tl, num[6]))])

        self.play(Write(mf_eq), Create(bar), run_time=1.0)
        self.play(Write(num[0]), FadeIn(tg_bpv), FadeIn(side_p), run_time=1.0)
        self.sync(t0 + 2.8)
        self.play(LaggedStart(*[Write(num[i]) for i in range(1, 9)], lag_ratio=0.25),
                  run_time=2.2)
        self.sync(t0 + 5.5)
        self.play(Indicate(num[2], color=PROVER_C), FadeIn(tg_ts), Create(conn[0]),
                  run_time=1.0)
        self.play(Indicate(num[4], color=PROVER_C), FadeIn(tg_ps), run_time=1.0)
        self.sync(t0 + 11.5)
        self.play(Indicate(num[6], color=PROVER_C), FadeIn(tg_tl), Create(conn[1]),
                  run_time=1.0)
        self.play(Indicate(num[8], color=PROVER_C), FadeIn(tg_pl), run_time=1.0)

        # ---------------- Segment 7: equation, meter side ----------------
        t0 = START[6]
        tg_iv = tag(den[0], "indicated volume", METER_C, up=False)
        tg_tm = tag(den[2], "liquid · temp.", METER_C, up=False)
        tg_pm = tag(den[4], "liquid · press.", METER_C, up=False)
        tg_tm.shift(DOWN * 0.35)
        conn_m = Line(tg_tm.get_top(), den[2].get_bottom(), stroke_width=1.5, color=GREY_INK,
                      buff=0.05)
        iv_def = VGroup(
            Text("IV = N ÷ KF", font_size=FS_EQUATION - 4, color=METER_C, weight=BOLD),
            label("N  = meter pulses (whole + fraction)", FS_TAG, METER_C),
            label(f"KF = nominal K-factor ({K_NOM_TXT} pls/m³)", FS_TAG, METER_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, -2.9, 0])
        iv_box = boxed(iv_def, METER_C, 0.2)

        self.play(Write(den[0]), FadeIn(side_m), FadeIn(tg_iv), run_time=1.2)
        self.sync(t0 + 3.6)
        self.play(Create(iv_box), Write(iv_def[0]), run_time=1.2)
        self.play(FadeIn(iv_def[1]), FadeIn(iv_def[2]), run_time=1.0)
        self.sync(t0 + 8.2)
        self.play(Write(den[1:]), run_time=1.2)
        self.play(FadeIn(tg_tm), Create(conn_m), FadeIn(tg_pm), run_time=1.0)
        self.sync(START[7] - 0.8)
        eq_all = VGroup(eq, side_p, side_m)
        tags_all = VGroup(tg_bpv, tg_ts, tg_ps, tg_tl, tg_pl, conn, tg_iv, tg_tm, tg_pm, conn_m,
                          iv_def, iv_box)
        self.play(FadeOut(tags_all), FadeOut(VGroup(side_p, side_m)),
                  eq.animate.scale(0.55).to_corner(UR, buff=0.3), run_time=0.8)

        # ---------------- Segment 8: reading MF ----------------
        t0 = START[7]
        lo, hi = 0.996, 1.004
        nl = NumberLine(x_range=[lo, hi, 0.001], length=11.0, include_tip=False,
                        stroke_width=4, color=INK, tick_size=0.1).move_to(DOWN * 0.2)
        tick_lbls = VGroup(*[label(f"{v:.3f}", FS_TAG, GREY_INK).next_to(nl.n2p(v), DOWN, 0.2)
                             for v in (0.997, 0.998, 0.999, 1.001, 1.002, 1.003)])
        one = Text("1", font_size=FS_EQUATION, weight=BOLD).next_to(nl.n2p(1.0), DOWN, 0.2)
        one_tick = Line(nl.n2p(1.0) + UP * 0.3, nl.n2p(1.0) + DOWN * 0.1, stroke_width=5)
        ratio = label("MF is a ratio, not a difference", FS_BODY, weight=BOLD).move_to(UP * 2.0)
        left_zone = Rectangle(width=nl.n2p(1.0)[0] - nl.n2p(lo)[0], height=0.5, stroke_width=0,
                              fill_color=METER_C, fill_opacity=0.15)
        left_zone.move_to((nl.n2p(lo) + nl.n2p(1.0)) / 2 + UP * 0.25)
        right_zone = Rectangle(width=nl.n2p(hi)[0] - nl.n2p(1.0)[0], height=0.5, stroke_width=0,
                               fill_color=PROVER_C, fill_opacity=0.15)
        right_zone.move_to((nl.n2p(1.0) + nl.n2p(hi)) / 2 + UP * 0.25)
        l_txt = VGroup(label("MF < 1", FS_LABEL, METER_C, weight=BOLD),
                       label("meter registers MORE", FS_TAG, METER_C),
                       label("than the true volume", FS_TAG, METER_C)
                       ).arrange(DOWN, buff=0.08).next_to(left_zone, UP, 0.25)
        r_txt = VGroup(label("MF > 1", FS_LABEL, PROVER_C, weight=BOLD),
                       label("meter registers LESS", FS_TAG, PROVER_C),
                       label("than the true volume", FS_TAG, PROVER_C)
                       ).arrange(DOWN, buff=0.08).next_to(right_zone, UP, 0.25)
        dev = label("deviation = MF − 1", FS_BODY).move_to(DOWN * 1.9)

        self.play(Write(ratio), run_time=1.2)
        self.play(Create(nl), Create(one_tick), Write(one), FadeIn(tick_lbls), run_time=1.5)
        self.sync(t0 + 4.0)
        self.play(FadeIn(left_zone), FadeIn(l_txt, shift=DOWN * 0.1), run_time=1.2)
        self.sync(t0 + 9.0)
        self.play(FadeIn(right_zone), FadeIn(r_txt, shift=DOWN * 0.1), run_time=1.2)
        self.sync(t0 + 13.2)
        self.play(Write(dev), run_time=1.2)

        # ---------------- Segment 9: demo example ----------------
        t0 = START[8]
        demo = label("Illustrative data", FS_TAG, GREY_INK).next_to(title, DOWN, 0.2)
        demo.align_to(title, LEFT)
        marker = Triangle(color=INK, fill_color=INK, fill_opacity=1, stroke_width=2).scale(0.14)
        marker.rotate(PI).next_to(nl.n2p(D.MF_AVG), UP, 0.02)
        mk_line = DashedLine(nl.n2p(D.MF_AVG), nl.n2p(D.MF_AVG) + UP * 0.45, stroke_width=3)
        avg = label(f"average MF = {MF_TXT}", FS_LABEL, weight=BOLD)
        avg.next_to(nl.n2p(D.MF_AVG), DOWN, 0.95)
        avg_box = boxed(avg, INK, 0.12)
        dev_val = label(f"deviation = {DEV_PCT:+.2f} %".replace("-", "−") + f"  →  meter reads ≈ {abs(DEV_PCT):.1f} % high",
                        FS_LABEL).move_to(DOWN * 2.0)
        kp = Text("K proven = K nominal ÷ MF", font_size=FS_BODY, weight=BOLD).move_to(DOWN * 2.8)
        kp_val = label(f"= {K_NOM_TXT} ÷ {MF_TXT} = {K_FIN_TXT} pls/m³", FS_BODY)
        kp_val.next_to(kp, DOWN, 0.25)

        self.play(FadeIn(demo), FadeOut(tick_lbls[:2]), run_time=0.6)
        self.play(FadeIn(marker, shift=DOWN * 0.2), Create(mk_line), run_time=0.8)
        self.play(FadeIn(avg), Create(avg_box), run_time=1.0)
        self.sync(t0 + 4.8)
        self.play(ReplacementTransform(dev, dev_val), run_time=1.2)
        self.sync(t0 + 9.5)
        self.play(Write(kp), run_time=1.4)
        self.sync(t0 + 14.5)
        self.play(Write(kp_val), run_time=1.6)
        self.play(Circumscribe(VGroup(kp, kp_val), color=INK), run_time=1.2)
        self.sync(START[9] - 0.6)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not title], run_time=0.6)

        # ---------------- Segment 10: K or MF, not both + outro ----------------
        t0 = START[9]
        rule = Text("Apply ONE of them — not both", font_size=FS_HEADING, weight=BOLD)
        rule.move_to(UP * 2.3)
        opt_a = VGroup(label("Option A", FS_LABEL, GREY_INK),
                       label(f"K = {K_FIN_TXT} pls/m³ (proven)", FS_LABEL, weight=BOLD),
                       label("MF = 1.00000", FS_LABEL, weight=BOLD)).arrange(DOWN, buff=0.15)
        opt_b = VGroup(label("Option B", FS_LABEL, GREY_INK),
                       label(f"K = {K_NOM_TXT} pls/m³ (nominal)", FS_LABEL, weight=BOLD),
                       label(f"MF = {MF_TXT}", FS_LABEL, weight=BOLD)).arrange(DOWN, buff=0.15)
        ga, gb = VGroup(boxed(opt_a), opt_a), VGroup(boxed(opt_b), opt_b)
        orr = label("or", FS_BODY, GREY_INK)
        opts = fit(VGroup(ga, orr, gb).arrange(RIGHT, buff=0.5)).move_to(UP * 0.3)
        both = label("Proven K  +  MF  →  reading corrected twice", FS_BODY).move_to(DOWN * 1.6)
        cross = Cross(both, stroke_width=5, stroke_color=INK)
        nxt = label("Next: pass · run · repeatability", FS_BODY, GREY_INK).move_to(DOWN * 3.0)

        self.play(Write(rule), run_time=1.2)
        self.play(Create(ga[0]), FadeIn(opt_a), run_time=1.0)
        self.play(FadeIn(orr), Create(gb[0]), FadeIn(opt_b), run_time=1.0)
        self.sync(t0 + 6.5)
        self.play(FadeIn(both), run_time=0.8)
        self.play(Create(cross), run_time=0.8)
        self.sync(t0 + 11.8)
        self.play(FadeIn(nxt, shift=UP * 0.1), run_time=1.0)
        self.sync(START[10] + 2.0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="low-quality layout check")
    args = parser.parse_args()
    print(build(__file__, "ProverEp01", NARRATION, preview=args.preview))
