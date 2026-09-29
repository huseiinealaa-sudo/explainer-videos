"""pt_cal, episode 4: the ten-step procedure and pressure decay.

Every number on screen or in the narration comes from pt_cal_data. Sources: sources/pt_cal_source.md (§4)
and sources/pt_cal_ep04_procedure.md; storyboard: storyboard/pt_cal_ep04_procedure.md. The decay curves
are illustrative (pt_cal_data.p_thermal / p_leak / p_mixed), not measurements.

Build (from the repo root):
    python projects/pt_cal/pt_cal_ep04_procedure.py --preview   # 480p15 -> tmp/pt_cal_ep04_procedure/preview.mp4
    python projects/pt_cal/pt_cal_ep04_procedure.py             # 1080p30 -> output/pt_cal_ep04_procedure.mp4
"""
from explainer import *
from pt_cal_common import *
import pt_cal_data as D

# Fully diacritized narration (owner-approved 2026-09-28) — one entry per segment.
NARRATION = [
    # 1
    "هٰذِهِ مَادَّةٌ تَعْلِيمِيَّةٌ؛ وَالمَرْجِعُ المُلْزِمُ الأَدِلَّةُ الرَّسْمِيَّةُ وَإِجْرَاءَاتُ مُنْشَأَتِكَ. الإِجْرَاءُ عَشْرُ خُطُوَاتٍ. الأُولَى: التَّحْضِيرُ الوَرَقِيُّ: أَمْرُ العَمَلِ، وَتَصْرِيحُ العَمَلِ، وَبَيَانَاتُ المُرْسِلِ، وَشَهَادَةُ جِهَازِكَ سَارِيَةً. الثَّانِيَةُ: العَزْلُ، وَإِبْلَاغُ غُرْفَةِ التَّحَكُّمِ. الثَّالِثَةُ: التَّوْصِيلُ، مِنْ صِفْرِ مِلِّي أَمْبِير، وَالخُرْطُومُ غَيْرُ مَشْدُودٍ. الرَّابِعَةُ: تَصْفِيرُ وَحْدَةِ الضَّغْطِ. الخَامِسَةُ: اخْتِبَارُ التَّسْرِيبِ. السَّادِسَةُ: التَّمْرِينُ، ثَلَاثُ دَوْرَاتٍ مِنَ الصِّفْرِ إِلَى المِئَةِ وَالعَوْدَةُ. السَّابِعَةُ: آزْ فَاوْنْد، خَمْسُ نِقَاطٍ صُعُودًا ثُمَّ هُبُوطًا، قَبْلَ أَيِّ مَسَاسٍ؛ وَهِيَ أَثْمَنُ البَيَانَاتِ. الثَّامِنَةُ: القَرَارُ؛ فَإِنْ نَجَحَ فَلَا تَلْمَسْهُ. التَّاسِعَةُ: إِنْ رَسَبَ فَالضَّبْطُ، ثُمَّ آزْ لِفْت كَامِلَةً. العَاشِرَةُ: الإِرْجَاعُ بِالعَكْسِ، وَالتَّحَقُّقُ مَعَ غُرْفَةِ التَّحَكُّمِ، وَالشَّهَادَةُ، وَالمَوْعِدُ القَادِمُ.",
    # 2
    "وَالقَاعِدَةُ الذَّهَبِيَّةُ: فِي الصُّعُودِ اقْتَرِبْ مِنْ كُلِّ نُقْطَةٍ مِنْ أَسْفَلَ فَقَطْ، وَفِي الهُبُوطِ مِنْ أَعْلَى فَقَطْ. فَإِنْ تَجَاوَزْتَ ثُمَّ رَجَعْتَ، دَخَلَ التَّخَلُّفُ الهِسْتِيرِيُّ فِي قِرَاءَةٍ تَظُنُّهَا لِلْخَطِّيَّةِ، فَفَسَدَ الرَّقْمَانِ.",
    # 3
    "وَإِذَا هَبَطَ الضَّغْطُ فَشَخِّصْ قَبْلَ أَنْ تُصْلِحَ: اضْغَطْ إِلَى المِئَةِ بِالمِئَةِ، وَأَغْلِقْ صِمَامَ المِضَخَّةِ، وَشَغِّلْ مُسَجِّلَ البَيَانَاتِ عَلَى وَحْدَةِ الضَّغْطِ، قِرَاءَةً كُلَّ ثَانِيَةٍ لِثَلَاثِ دَقَائِقَ، وَانْظُرْ إِلَى شَكْلِ المُنْحَنَى لَا إِلَى مِقْدَارِ الهُبُوطِ. هُبُوطٌ سَرِيعٌ يَتَبَاطَأُ ثُمَّ يَسْتَقِرُّ خِلَالَ دَقِيقَةٍ إِلَى ثَلَاثٍ: أَثَرٌ حَرَارِيٌّ طَبِيعِيٌّ. هُبُوطٌ بِمُعَدَّلٍ ثَابِتٍ لَا يَتَوَقَّفُ: تَسْرِيبٌ يَجِبُ إِصْلَاحُهُ. وَسَرِيعٌ ثُمَّ بَطِيءٌ بِلَا اسْتِقْرَارٍ: الِاثْنَانِ مَعًا؛ أَصْلِحِ التَّسْرِيبَ ثُمَّ أَعِدِ الِاخْتِبَارَ. لَاحِظْ أَنَّ المُنْحَنَيَيْنِ الأَوَّلَيْنِ انْتَهَيَا عِنْدَ القِيمَةِ نَفْسِهَا تَقْرِيبًا.",
    # 4
    "السَّبَبُ الأَوَّلُ حَرَارِيٌّ: ضَغْطُ الهَوَاءِ يَرْفَعُ حَرَارَتَهُ فَوْرًا، وَمَعَ تَبَرُّدِهِ يَنْخَفِضُ الضَّغْطُ دُونَ أَيِّ تَسْرِيبٍ؛ وَيَشْتَدُّ الأَثَرُ مَعَ ارْتِفَاعِ الضَّغْطِ، فَهُوَ عِنْدَ المِئَةِ أَسْوَأُ مِنْهُ عِنْدَ الرُّبْعِ. وَالثَّانِي التَّسْرِيبُ: الوَصَلَاتُ السَّرِيعَةُ وَحَلَقَاتُهَا المَطَّاطِيَّةُ أَوَّلًا، ثُمَّ المُحَوِّلَاتُ اللَّوْلَبِيَّةُ وَشَرِيطُهَا المَلْفُوفُ خَطَأً، وَصِمَامُ عَدَمِ الرُّجُوعِ فِي المِضَخَّةِ، وَوَصْلَةُ العَمَلِيَّةِ فِي المُرْسِلِ. وَالثَّالِثُ نِظَامٌ لَمْ يُمَرَّنْ: فَالحَلَقَاتُ وَالغِشَاءُ تَحْتَاجُ أَنْ تَسْتَقِرَّ فِي مَوَاضِعِهَا.",
    # 5
    "وَالعِلَاجُ: خُرْطُومٌ أَقْصَرُ، وَمُحَوِّلَاتٌ أَقَلُّ، وَخُرْطُومٌ مَعْدِنِيٌّ مَجْدُولٌ بَدَلَ البِلَاسْتِيكِيِّ، وَانْتِظَارُ نِصْفِ دَقِيقَةٍ إِلَى دَقِيقَةٍ عِنْدَ النُّقْطَةِ، وَلِلضُّغُوطِ العَالِيَةِ المِضَخَّةُ الهَيْدْرُولِيكِيَّةُ إِنْ سَمَحَ إِجْرَاءُ القِسْمِ. وَفِي المُعَايِرِ المُوَثِّقِ ثَلَاثَةُ إِعْدَادَاتٍ لِلْقَبُولِ الآلِيِّ: أَقْصَى انْحِرَافٍ عَنِ النُّقْطَةِ، وَنَقْتَرِحُ اثْنَيْنِ إِلَى ثَلَاثَةٍ بِالمِئَةِ مِنَ المَدَى؛ وَفَحْصُ الِاسْتِقْرَارِ؛ وَزَمَنُ انْتِظَارٍ، ثَلَاثُونَ إِلَى سِتِّينَ ثَانِيَةً. وَتَوْسِيعُ النَّافِذَةِ لَا يُضْعِفُ الدِّقَّةَ: فَالجِهَازُ يُسَجِّلُ الدَّخْلَ الفِعْلِيَّ وَيَحْسُبُ الخَطَأَ مُقَابِلَهُ، وَيَلْتَقِطُ الدَّخْلَ وَالخَرْجَ فِي اللَّحْظَةِ نَفْسِهَا. أَمَّا القِرَاءَةُ بِالعَيْنِ وَالكِتَابَةُ، فَالضَّغْطُ يَهْبِطُ بَيْنَ النَّظْرَتَيْنِ.",
    # 6
    "وَأَخْطَاءٌ أُخْرَى شَائِعَةٌ: تَغْيِيرُ وَضْعِ التَّرْكِيبِ دُونَ إِعَادَةِ التَّصْفِيرِ، فَالجَاذِبِيَّةُ تُزِيحُ صِفْرَ الغِشَاءِ. وَتَخْمِيدٌ مُرْتَفِعٌ يُؤَخِّرُ القِرَاءَةَ فَتَظُنُّهَا اسْتَقَرَّتْ؛ اخْفِضْهُ ثُمَّ أَعِدْهُ. وَسَائِلٌ مَحْبُوسٌ فِي خُطُوطِ النَّبْضِ يُضِيفُ ضَغْطًا سَاكِنًا، فَصَرِّفْهَا. وَمُرْسِلٌ بَارِدٌ مِنَ الخَارِجِ، فَاتْرُكْهُ رُبْعَ سَاعَةٍ إِلَى نِصْفِ سَاعَةٍ لِيَتَعَادَلَ. وَتَجَاوُزُ مَدَى وَحْدَةِ الضَّغْطِ.",
]

# Every spoken or shown value is checked against the data module; stop if it drifts.
assert D.EXERCISE_CYCLES == 3 and len(D.CAL_POINTS_PCT) == 5                             # seg 1
assert D.DECAY_TEST_MIN == 3 and D.DECAY_DT == 1 and D.DECAY_T_END == 180               # seg 3
assert 60 <= D.THERM_SETTLE_S <= 180                                                    # seg 3 "1 to 3 min"
assert D.ACCEPT_DEV_PCT == (2, 3) and D.ACCEPT_DELAY_S == (30, 60)                      # seg 5
assert D.COLD_WAIT_MIN == (15, 30) and D.AIR_WAIT_S == (30, 60)                         # seg 5, 6

AUDIO_DIR = audio_dir_for(__file__)

STEPS = ["Paperwork", "Isolate", "Connect", "Zero", "Leak test", "Exercise", "As-Found", "Decide",
         "Trim + As-Left", "Return"]
STEP_CUES = ["الأُولَى", "الثَّانِيَةُ", "الثَّالِثَةُ", "الرَّابِعَةُ", "الخَامِسَةُ", "السَّادِسَةُ",
             "السَّابِعَةُ", "الثَّامِنَةُ", "التَّاسِعَةُ", "العَاشِرَةُ"]


class PtCalEp04(SyncedScene):
    def c(self, seg, phrase, nth=1):
        return self.cue(seg, phrase, nth)

    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        self.seg1_steps()
        self.seg2_rule()
        self.seg3_decay()
        self.seg4_causes()
        self.seg5_remedy()
        self.seg6_mistakes()

    # ---------------- Segment 1: ten steps ----------------
    def step_visual(self, k):
        """The small drawing under the step pills for step k (0-based)."""
        y = -1.1
        if k == 0:
            return VGroup(VGroup(icon("file-text", INK, 0.7), icon("clipboard-check", INK, 0.7),
                                 icon("calendar", INK, 0.7)).arrange(RIGHT, buff=0.5),
                          tag("work order · permit · transmitter data · your valid certificate", FS_TAG + 2)) \
                .arrange(DOWN, buff=0.4).move_to([0, y, 0])
        if k == 1:
            return VGroup(VGroup(icon("lock", MOVE, 0.7), gate_valve(size=0.8).set_fill(INK, 1)).arrange(RIGHT, buff=0.6),
                          tag("isolate · tell the control room", FS_TAG + 2)).arrange(DOWN, buff=0.4).move_to([0, y, 0])
        if k == 2:
            return VGroup(VGroup(device("0 mA", 1.4, 0.8, FS_TAG + 2),
                                 poly([[0, 0, 0], [0.8, -0.35, 0], [1.6, 0, 0], [2.4, -0.3, 0]], INK, 5, True))
                          .arrange(RIGHT, buff=0.3),
                          tag("start from 0 mA · hose not strained", FS_TAG + 2)).arrange(DOWN, buff=0.4).move_to([0, y, 0])
        if k == 3:
            return VGroup(device("0.000 bar", 2.2, 0.8, FS_LABEL),
                          tag("vented: zero the pressure module", FS_TAG + 2)).arrange(DOWN, buff=0.4).move_to([0, y, 0])
        if k == 4:
            ch = Chart(-2.0, y - 0.6, 4.0, 1.2, (0, 10), (0, 10))
            return VGroup(ch.axes, ch.line([(0, 8), (10, 7.9)], GOOD, 4),
                          tag("leak test: pressure holds", FS_TAG + 2).next_to(ch.axes, DOWN, buff=0.25))
        if k == 5:
            ch = Chart(-2.6, y - 0.7, 5.2, 1.4, (0, 6), (0, 100))
            pts = [(i, 100 if i % 2 else 0) for i in range(7)]
            g = VGroup(ch.axes, ch.line(pts, MOVE, 4),
                       tag(f"exercise: {D.EXERCISE_CYCLES} cycles 0 → 100 % → 0", FS_TAG + 2)
                       .next_to(ch.axes, DOWN, buff=0.25))
            g.anim_index = 1
            return g
        if k == 6:
            ch = Chart(-2.6, y - 0.7, 5.2, 1.4, (0, 8), (0, 100))
            seq = D.CAL_POINTS_PCT + D.CAL_POINTS_PCT[-2::-1]
            dots = ch.dots([(i, v) for i, v in enumerate(seq)], FLUID, 0.08)
            return VGroup(ch.axes, dots, tag("As-Found: 5 points up, then down — before any touch", FS_TAG + 2)
                          .next_to(ch.axes, DOWN, buff=0.25))
        if k == 7:
            return VGroup(tag("PASS → do not touch, go to step 10", FS_TAG + 2, GOOD),
                          tag("FAIL → continue", FS_TAG + 2, BAD)).arrange(DOWN, buff=0.3).move_to([0, y, 0])
        if k == 8:
            return VGroup(VGroup(icon("tool", MOVE, 0.7), icon("check", GOOD, 0.7)).arrange(RIGHT, buff=0.5),
                          tag("trim, then a full As-Left calibration", FS_TAG + 2)).arrange(DOWN, buff=0.4).move_to([0, y, 0])
        return VGroup(VGroup(icon("refresh", INK, 0.7), icon("file-text", GOOD, 0.7), icon("calendar", INK, 0.7))
                      .arrange(RIGHT, buff=0.5),
                      tag("reverse sequence · check with the control room · certificate · next date", FS_TAG + 2)) \
            .arrange(DOWN, buff=0.4).move_to([0, y, 0])

    def seg1_steps(self):
        title_segment(self, "The procedure and pressure decay", "Ten steps, one golden rule, one diagnostic test", 4)
        self.sync(self.c(1, "الإِجْرَاءُ") - 0.6)
        self.clear()
        self.sec = section_title(self, "Ten steps")
        pills = VGroup(*[card(f"{k + 1}  {s}", "", INK, 2.45, FS_TAG) for k, s in enumerate(STEPS)])
        rows = VGroup(VGroup(*pills[:5]).arrange(RIGHT, buff=0.15), VGroup(*pills[5:]).arrange(RIGHT, buff=0.15)) \
            .arrange(DOWN, buff=0.2)
        fit(rows, 13.0).move_to([0, 2.05, 0])
        self.play(FadeIn(rows, lag_ratio=0.05), run_time=1.0)
        cur = None
        for k, ph in enumerate(STEP_CUES):
            self.sync(self.c(1, ph))
            vis = self.step_visual(k)
            anims = [pills[k].frame.animate.set_stroke(FLUID, 6).set_fill(FLUID, 0.12)]
            if k > 0:
                anims.append(pills[k - 1].frame.animate.set_stroke(GREY_INK, 3).set_fill(WHITE, 1))
            if cur is not None:
                anims.append(FadeOut(cur))
            self.play(*anims, run_time=0.35)
            if hasattr(vis, "anim_index"):
                rest = VGroup(*[m for i, m in enumerate(vis) if i != vis.anim_index])
                self.play(FadeIn(rest), run_time=0.3)
                self.play(Create(vis[vis.anim_index]), run_time=2.4, rate_func=linear)
            elif k == 6:
                self.play(FadeIn(vis[0]), FadeIn(vis[2]), run_time=0.3)
                self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in vis[1]], lag_ratio=0.35), run_time=2.2)
            else:
                self.play(FadeIn(vis, shift=UP * 0.1), run_time=0.5)
            if k == 6:
                gem = tag("the most valuable data", FS_TAG + 2, FLUID, weight=BOLD).next_to(vis, DOWN, buff=0.15)
                self.sync(self.c(1, "أَثْمَنُ"))
                self.play(FadeIn(gem), run_time=0.4)
                vis.add(gem)
            cur = vis
        self.sync(self.end(1) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 2: the golden rule ----------------
    def seg2_rule(self):
        section_title(self, "Golden rule: approach from one direction", prev=self.sec)
        ch = Chart(-5.3, -3.0, 6.6, 5.2, (0, 20), (0, 110), yticks=[(v, f"{v} %") for v in D.CAL_POINTS_PCT],
                   xlabel="time")
        targets = VGroup(*[ch.hline(v, LIGHT_INK) for v in D.CAL_POINTS_PCT])
        up, t = [], 0
        for v in D.CAL_POINTS_PCT:
            up += [(t, v - 4 if v else 0), (t + 0.6, v), (t + 1.6, v)]
            t += 2
        down = []
        for v in D.CAL_POINTS_PCT[-2::-1]:
            down += [(t, v + 4), (t + 0.6, v), (t + 1.6, v)]
            t += 2
        path_up = ch.line([(0, 0)] + up, GOOD, 4)
        path_dn = ch.line([up[-1]] + down, GOOD, 4)
        self.play(Create(ch.axes), FadeIn(ch.ticks), FadeIn(ch.xl), Create(targets), run_time=0.7)
        l_up = tag("rising: from below only", FS_TAG + 1, GOOD).move_to([4.3, 1.6, 0]).align_to([1.6, 0, 0], LEFT)
        l_dn = tag("falling: from above only", FS_TAG + 1, GOOD).next_to(l_up, DOWN, buff=0.2).align_to(l_up, LEFT)
        self.play(Create(path_up), FadeIn(l_up), run_time=2.4, rate_func=linear)
        self.sync(self.c(2, "وَفِي الهُبُوطِ"))
        self.play(Create(path_dn), FadeIn(l_dn), run_time=2.0, rate_func=linear)
        self.sync(self.c(2, "فَإِنْ تَجَاوَزْتَ"))
        over = ch.line([(4, 46), (4.5, 58), (5.2, 50)], BAD, 5)
        ol = tag("overshoot, then back:\nhysteresis read as linearity", FS_TAG + 1, BAD) \
            .next_to(l_dn, DOWN, buff=0.4).align_to(l_up, LEFT)
        self.play(Create(over), run_time=0.8)
        self.sync(self.c(2, "دَخَلَ"))
        d_bad = Dot(ch.p(5.2, 50), radius=0.09, color=BAD)
        d_ok = Dot(ch.p(4.6, 50), radius=0.08, color=GREY_INK)
        hy = DoubleArrow(ch.p(6.0, 50), ch.p(6.0, 58), buff=0, stroke_width=3, color=BAD, tip_length=0.12)
        hyl = tag("overshoot", FS_TAG - 2, BAD).next_to(hy, RIGHT, buff=0.1).shift(UP * 0.12)
        same = tag("same 50 %, different reading", FS_TAG, BAD).next_to(ol, DOWN, buff=0.2).align_to(ol, LEFT)
        self.play(FadeIn(d_bad), FadeIn(d_ok), GrowFromCenter(hy), FadeIn(hyl), FadeIn(ol), FadeIn(same), run_time=0.8)
        self.sync(self.c(2, "فَفَسَدَ"))
        self.play(Indicate(d_bad, color=BAD, scale_factor=1.8), Indicate(d_ok, color=BAD, scale_factor=1.8), run_time=0.6)
        both = tag("both numbers spoiled", FS_TAG + 2, BAD, weight=BOLD).next_to(same, DOWN, buff=0.25).align_to(ol, LEFT)
        self.play(FadeIn(both), Indicate(over, color=BAD), run_time=0.6)
        self.sync(self.end(2) - 0.5)
        self.clear(self.sec, run_time=0.5)

    # ---------------- Segment 3: the decay test, read the shape ----------------
    def seg3_decay(self):
        section_title(self, "Pressure decay: read the shape, not the amount", prev=self.sec)
        setup = VGroup(tag("pump to 100 % · close the pump valve", FS_TAG + 1),
                       tag(f"Data Logger: 1 reading / s for {D.DECAY_TEST_MIN} min", FS_TAG + 1)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fit(setup, 5.5).move_to([3.9, 2.35, 0]).align_to([1.1, 0, 0], LEFT)
        self.play(FadeIn(setup[0]), run_time=0.5)
        self.sync(self.c(3, "وَشَغِّلْ"))
        self.play(FadeIn(setup[1]), run_time=0.5)
        ch = Chart(-5.8, -3.1, 7.0, 4.6, (0, D.DECAY_T_END), (41.6, 42.05),
                   xticks=[(0, "0"), (60, "1"), (120, "2"), (180, "3 min")],
                   yticks=[(D.DECAY_P0, fmt(D.DECAY_P0, 2)), (D.DECAY_P0 - D.THERM_A, fmt(D.DECAY_P0 - D.THERM_A, 2))], ylabel=D.UNIT)
        self.play(Create(ch.axes), FadeIn(ch.ticks), FadeIn(ch.yl), run_time=0.6)
        ts = D.DECAY_T[::3]
        curves = [(D.p_thermal, MOVE, "thermal: fast, slows, settles", "هُبُوطٌ سَرِيعٌ يَتَبَاطَأُ"),
                  (D.p_leak, BAD, "leak: steady, never stops", "هُبُوطٌ بِمُعَدَّلٍ"),
                  (D.p_mixed, "#7b3fa0", "both: fast, then a steady slope", "وَسَرِيعٌ ثُمَّ")]
        labs = VGroup()
        for k, (f, col, txt, ph) in enumerate(curves):
            self.sync(self.c(3, ph))
            cv = ch.line([(t, f(t)) for t in ts], col, 4)
            lab = VGroup(Line(ORIGIN, RIGHT * 0.5, stroke_width=5, color=col), tag(txt, FS_TAG + 1, col)) \
                .arrange(RIGHT, buff=0.15)
            fit(lab, 5.0).move_to([4.2, 0.9 - 0.55 * k, 0]).align_to([1.6, 0, 0], LEFT)
            labs.add(lab)
            self.play(Create(cv), FadeIn(lab), run_time=2.2, rate_func=linear)
        fixf = fit(tag("fix the leak, then repeat the test", FS_TAG + 1, BAD), 5.0).next_to(labs, DOWN, buff=0.3).align_to(labs, LEFT)
        self.sync(self.c(3, "أَصْلِحِ"))
        self.play(FadeIn(fixf), run_time=0.5)
        self.sync(self.c(3, "لَاحِظْ"))
        end = Circle(radius=0.25, color=INK, stroke_width=3).move_to(ch.p(D.DECAY_T_END, D.p_leak(D.DECAY_T_END)))
        same = tag("same end value", FS_TAG + 1).next_to(end, RIGHT, buff=0.12)
        self.play(Create(end), FadeIn(same), run_time=0.6)
        self.sync(self.end(3) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 4: causes ----------------
    def seg4_causes(self):
        section_title(self, "Three causes", prev=self.sec)
        # 1 heat of compression
        cyl = VGroup(Line([-6.3, 2.2, 0], [-3.9, 2.2, 0]), Line([-6.3, 1.2, 0], [-3.9, 1.2, 0]),
                     Line([-3.9, 2.2, 0], [-3.9, 1.2, 0])).set_stroke(INK, 4)
        px = ValueTracker(-6.1)
        heat = ValueTracker(0.0)
        piston = always_redraw(lambda: Rectangle(width=0.2, height=1.0, color=MOVE, stroke_width=3).set_fill(MOVE, 1)
                               .move_to([px.get_value(), 1.7, 0]))
        dots = always_redraw(lambda: VGroup(*[
            Dot([px.get_value() + 0.25 + (k % 4) * (-4.1 - px.get_value() - 0.25) / 3.3, 1.45 + (k // 4) * 0.5, 0],
                radius=0.06, color=interpolate_color(ManimColor(GREY_INK), ManimColor(MOVE), heat.get_value()))
            for k in range(8)]))
        h1 = tag("1  heat: compressed air\nwarms, then cools", FS_TAG + 1, MOVE).next_to(cyl, DOWN, buff=0.2) \
            .align_to(cyl, LEFT)
        self.play(Create(cyl), FadeIn(piston), FadeIn(dots), FadeIn(h1), run_time=0.6)
        self.play(px.animate.set_value(-4.9), heat.animate.set_value(1), run_time=1.0)
        self.sync(self.c(4, "وَمَعَ تَبَرُّدِهِ"))
        ch = Chart(-6.3, -1.3, 3.4, 1.4, (0, 10), (0, 1.0))
        sag25 = ch.line([(t, 0.9 - 0.1 * (1 - np.exp(-t / 2))) for t in np.linspace(0, 10, 20)], GREY_INK, 3)
        sag100 = ch.line([(t, 0.9 - 0.6 * (1 - np.exp(-t / 2))) for t in np.linspace(0, 10, 20)], MOVE, 4)
        self.play(heat.animate.set_value(0), Create(ch.axes), Create(sag100), run_time=1.4)
        self.sync(self.c(4, "وَيَشْتَدُّ"))
        l1 = VGroup(tag("at 100 %", FS_TAG, MOVE).next_to(sag100.get_end(), RIGHT, buff=0.1),
                    tag("at 25 %", FS_TAG, GREY_INK).next_to(ch.p(10, 0.8), RIGHT, buff=0.1).shift(UP * 0.1))
        self.play(Create(sag25), FadeIn(l1), run_time=0.8)
        # 2 leak points along the chain
        self.sync(self.c(4, "وَالثَّانِي التَّسْرِيبُ"))
        parts = VGroup(*[device(n, 2.4, 0.7, FS_TAG - 2) for n in
                         ("pump", "quick\nconnector", "threaded\nadapter", "transmitter\nconnection")])
        parts.arrange(DOWN, buff=0.25).move_to([1.5, 0.75, 0])
        links = VGroup(*[Line(parts[i].box.get_bottom(), parts[i + 1].box.get_top(), stroke_width=5, color=INK)
                         for i in range(3)])
        h2 = tag("2  leaks", FS_TAG + 1, BAD).next_to(parts, LEFT, buff=0.5).align_to(parts, UP)
        self.play(FadeIn(parts), Create(links), FadeIn(h2), run_time=0.6)
        notes = [(1, "O-rings first", "الوَصَلَاتُ السَّرِيعَةُ"), (2, "tape wrapped wrong", "ثُمَّ المُحَوِّلَاتُ"),
                 (0, "check valve", "وَصِمَامُ عَدَمِ"), (3, "process connection", "وَوَصْلَةُ")]
        for i, txt, ph in notes:
            self.sync(self.c(4, ph))
            d = Dot(parts[i].box.get_right() + RIGHT * 0.2, radius=0.07, color=BAD)
            t = tag(txt, FS_TAG - 2, BAD).next_to(d, RIGHT, buff=0.35)
            self.play(FadeIn(d), d.animate.shift(RIGHT * 0.1), FadeIn(t), parts[i].box.animate.set_stroke(BAD), run_time=0.5)
        # 3 not exercised
        self.sync(self.c(4, "وَالثَّالِثُ"))
        groove = VGroup(Line([1.2, -1.9, 0], [1.8, -1.9, 0]), Line([1.8, -1.9, 0], [1.8, -2.3, 0]),
                        Line([1.8, -2.3, 0], [2.6, -2.3, 0]), Line([2.6, -2.3, 0], [2.6, -1.9, 0]),
                        Line([2.6, -1.9, 0], [3.2, -1.9, 0])).set_stroke(INK, 4)
        oring = Circle(radius=0.18, color=MOVE, stroke_width=4).move_to([2.2, -1.55, 0])
        h3 = tag("3  not exercised:\nO-rings and diaphragm\nstill settling", FS_TAG + 1, MOVE) \
            .next_to(groove, RIGHT, buff=0.3)
        fit(h3, 3.2).next_to(groove, RIGHT, buff=0.3)
        self.play(Create(groove), FadeIn(oring), FadeIn(h3), run_time=0.6)
        self.play(oring.animate.move_to([2.2, -2.1, 0]), run_time=0.8)
        self.sync(self.end(4) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 5: remedies; acceptance settings ----------------
    def seg5_remedy(self):
        section_title(self, "Remedies · automatic acceptance", prev=self.sec)
        long_h = poly([[-6.3, 2.3, 0], [-5.4, 2.7, 0], [-4.4, 1.9, 0], [-3.4, 2.5, 0], [-2.6, 2.3, 0]], INK, 6, True)
        short_h = poly([[-6.3, 2.3, 0], [-5.1, 2.35, 0], [-4.2, 2.3, 0]], GOOD, 6, True)
        self.play(Create(long_h), run_time=0.5)
        self.play(Transform(long_h, short_h), run_time=0.7)
        rem = VGroup(tag("shorter hose, fewer adapters", FS_TAG + 1, GOOD),
                     tag("metal braided hose instead of flexible plastic", FS_TAG + 1, GOOD),
                     tag(f"wait {D.AIR_WAIT_S[0]}–{D.AIR_WAIT_S[1]} s at the point", FS_TAG + 1, GOOD),
                     tag("high pressure: the hydraulic pump, if the procedure allows", FS_TAG + 1, GOOD)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([2.6, 2.05, 0]).align_to([-3.6, 0, 0], LEFT)
        for r, ph in zip(rem, ["خُرْطُومٌ أَقْصَرُ", "وَخُرْطُومٌ مَعْدِنِيٌّ", "وَانْتِظَارُ", "وَلِلضُّغُوطِ"]):
            self.sync(self.c(5, ph))
            self.play(FadeIn(r, shift=RIGHT * 0.1), run_time=0.4)
        # the acceptance window on a live pressure trace
        self.sync(self.c(5, "وَفِي المُعَايِرِ"))
        ch = Chart(-6.2, -3.0, 6.6, 2.4, (0, 10), (0, 10), xlabel="time")
        band = ch.band(6.6, 7.4, GOOD, 0.15)
        tgt = ch.hline(7, INK)
        live = ch.line([(t, 7 - 3.2 * np.exp(-t / 1.6) + 0.1 * np.sin(3 * t) * np.exp(-t / 3)) for t in np.linspace(0, 10, 40)],
                       FLUID, 4, smooth=True)
        s1 = tag(f"Max. Point Deviation:\n{D.ACCEPT_DEV_PCT[0]}–{D.ACCEPT_DEV_PCT[1]} % of span (suggested)",
                 FS_TAG, GOOD)
        s2 = tag("Stability check", FS_TAG, GOOD)
        s3 = tag(f"Point Delay: {D.ACCEPT_DELAY_S[0]}–{D.ACCEPT_DELAY_S[1]} s", FS_TAG, GOOD)
        sets = VGroup(s1, s2, s3).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.9, -0.55, 0]) \
            .align_to([1.0, 0, 0], LEFT)
        self.play(Create(ch.axes), FadeIn(ch.xl), Create(tgt), run_time=0.5)
        self.sync(self.c(5, "أَقْصَى"))
        self.play(FadeIn(band), FadeIn(s1), run_time=0.5)
        self.play(Create(live), run_time=1.4)
        self.sync(self.c(5, "وَفَحْصُ"))
        ok = icon("check", GOOD, 0.35).next_to(ch.p(6, 7), UP, buff=0.3)
        self.play(FadeIn(s2), FadeIn(ok, scale=1.4), run_time=0.4)
        self.sync(self.c(5, "وَزَمَنُ"))
        pd = BraceBetweenPoints(ch.p(5, 9.7), ch.p(7.5, 9.7), direction=UP, color=GOOD)
        pdl = tag("Point Delay", FS_TAG - 2, GOOD).next_to(pd, UP, buff=0.05)
        self.play(FadeIn(s3), FadeIn(pd), FadeIn(pdl), run_time=0.5)
        # why a wide window is fine: Accept captures both at once
        self.sync(self.c(5, "وَتَوْسِيعُ"))
        cap = DashedLine(ch.p(7.5, 0), ch.p(7.5, 9.5), color=GOOD, stroke_width=3)
        cl = tag("Accept: actual input + output,\nsame instant", FS_TAG, GOOD).next_to(sets, DOWN, buff=0.4) \
            .align_to(sets, LEFT)
        self.play(Create(cap), FadeIn(cl), run_time=0.6)
        self.sync(self.c(5, "أَمَّا القِرَاءَةُ"))
        fall = ch.line([(t, 7.2 - 0.25 * t) for t in np.linspace(1, 9, 10)], BAD, 3)
        pen = VGroup(DashedLine(ch.p(3, 0), ch.p(3, 9.5), color=BAD, stroke_width=2),
                     DashedLine(ch.p(5, 0), ch.p(5, 9.5), color=BAD, stroke_width=2))
        pl = fit(tag("by eye and pen: the pressure\nfalls between the two looks", FS_TAG, BAD), 5.6) \
            .next_to(cl, DOWN, buff=0.2).align_to(cl, LEFT)
        p3, p5 = ch.p(3, 7.2 - 0.25 * 3), ch.p(5, 7.2 - 0.25 * 5)
        looks = VGroup(Dot(p3, radius=0.08, color=BAD), Dot(p5, radius=0.08, color=BAD),
                       DoubleArrow([p5[0] + 0.25, p3[1], 0], [p5[0] + 0.25, p5[1], 0], buff=0, stroke_width=3,
                                   color=BAD, tip_length=0.1))
        self.play(FadeOut(VGroup(live, cap, ok, pd, pdl)), Create(fall), Create(pen), FadeIn(pl), FadeIn(looks),
                  run_time=0.8)
        self.sync(self.end(5) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 6: other common mistakes ----------------
    def seg6_mistakes(self):
        section_title(self, "Other common mistakes", prev=self.sec)
        xs = [-5.2, -2.6, 0.0, 2.6, 5.2]
        panels = VGroup(*[RoundedRectangle(width=2.4, height=2.6, corner_radius=0.15, color=GREY_INK, stroke_width=2)
                          .move_to([x, 0.9, 0]) for x in xs])
        texts = ["mounting changed:\nre-zero (gravity\nshifts diaphragm)", "damping high:\nlower it, then\nrestore it",
                 "liquid in the\nimpulse lines:\ndrain them",
                 f"cold from outside:\nwait {D.COLD_WAIT_MIN[0]}–{D.COLD_WAIT_MIN[1]} min", "module range\nexceeded"]
        cues = ["تَغْيِيرُ وَضْعِ", "وَتَخْمِيدٌ", "وَسَائِلٌ", "وَمُرْسِلٌ بَارِدٌ", "وَتَجَاوُزُ"]
        caps = VGroup(*[fit(tag(t, FS_TAG - 2, line_spacing=1.1), 2.4).next_to(p, DOWN, buff=0.2) for t, p in zip(texts, panels)])
        for k, ph in enumerate(cues):
            self.sync(self.c(6, ph))
            p = panels[k]
            c = p.get_center()
            if k == 0:
                x = transmitter(bubble=False).scale(0.55).move_to(c)
                self.play(Create(p), FadeIn(x), FadeIn(caps[k]), run_time=0.4)
                self.play(Rotate(x, -0.6), run_time=0.6)
                zs = tag("zero shifted", FS_TAG - 4, BAD).next_to(x, DOWN, buff=0.1)
                zs.set_y(p.get_bottom()[1] + 0.25)
                self.sync(self.c(6, "فَالجَاذِبِيَّةُ"))
                self.play(FadeIn(zs), run_time=0.4)
                self.play(Transform(zs, tag("re-zero → 0", FS_TAG - 4, GOOD).move_to(zs)), run_time=0.5)
            elif k == 1:
                ch = Chart(c[0] - 1.0, c[1] - 0.8, 2.0, 1.6, (0, 10), (0, 10))
                step = ch.line([(0, 2), (3, 2), (3, 8), (10, 8)], GREY_INK, 2)
                lag = ch.line([(t, 2 + 6 * (1 - np.exp(-(t - 3) / 2.5)) if t > 3 else 2) for t in np.linspace(0, 10, 30)],
                              MOVE, 4, smooth=True)
                self.play(Create(p), FadeIn(ch.axes), Create(step), FadeIn(caps[k]), run_time=0.4)
                self.play(Create(lag), run_time=0.8)
                fast = ch.line([(t, 2 + 6 * (1 - np.exp(-(t - 3) / 0.5)) if t > 3 else 2) for t in np.linspace(0, 10, 40)],
                               GOOD, 4, smooth=True)
                self.sync(self.c(6, "اخْفِضْهُ"))
                self.play(Create(fast), lag.animate.set_stroke(opacity=0.3), run_time=0.7)
            elif k == 2:
                u = poly([c + [-0.7, 0.8, 0], c + [-0.7, -0.6, 0], c + [0.7, -0.6, 0], c + [0.7, 0.8, 0]], INK, 5)
                slug = Rectangle(width=0.18, height=0.5, stroke_width=0).set_fill(FLUID, 1).move_to(c + [-0.7, -0.3, 0])
                self.play(Create(p), Create(u), FadeIn(caps[k]), run_time=0.4)
                self.play(FadeIn(slug), slug.animate.shift(DOWN * 0.05), run_time=0.5)
                self.sync(self.c(6, "فَصَرِّفْهَا"))
                self.play(slug.animate.shift(DOWN * 0.25).set_opacity(0), run_time=0.7)
            elif k == 3:
                g = VGroup(icon("temperature", FLUID, 0.8), icon("clock", INK, 0.7)).arrange(RIGHT, buff=0.3).move_to(c)
                self.play(Create(p), FadeIn(g), FadeIn(caps[k]), run_time=0.5)
                self.sync(self.c(6, "لِيَتَعَادَلَ"))
                self.play(g[0].animate.set_color(INK), Rotate(g[1], -TAU / 2), run_time=0.9)
            else:
                g = VGroup(icon("gauge", BAD, 0.9), icon("alert-triangle", BAD, 0.6)).arrange(RIGHT, buff=0.2).move_to(c)
                self.play(Create(p), FadeIn(g), FadeIn(caps[k]), run_time=0.5)
        self.sync(self.end(6) + 1.0)


if __name__ == "__main__":
    main(__file__, "PtCalEp04", NARRATION)
