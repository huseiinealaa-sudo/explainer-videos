"""pt_cal, episode 7: error, uncertainty and TUR.

Every number on screen or in the narration comes from pt_cal_data. Sources: sources/pt_cal_source.md (§6)
and sources/pt_cal_ep07_uncertainty.md (JCGM 100:2008; ISO/IEC 17025). Storyboard:
storyboard/pt_cal_ep07_uncertainty.md. The budget values are illustrative.

Build (from the repo root):
    python projects/pt_cal/pt_cal_ep07_uncertainty.py --preview   # 480p15 -> tmp/pt_cal_ep07_uncertainty/preview.mp4
    python projects/pt_cal/pt_cal_ep07_uncertainty.py             # 1080p30 -> output/pt_cal_ep07_uncertainty.mp4
"""
from explainer import *
from pt_cal_common import *
import pt_cal_data as D

# Fully diacritized narration (owner-approved 2026-09-28) — one entry per segment.
NARRATION = [
    # 1
    "هٰذِهِ مَادَّةٌ تَعْلِيمِيَّةٌ؛ وَالمَرْجِعُ المُلْزِمُ الأَدِلَّةُ الرَّسْمِيَّةُ وَإِجْرَاءَاتُ مُنْشَأَتِكَ. ثَلَاثُ كَلِمَاتٍ تُخْلَطُ كَثِيرًا. الخَطَأُ: فَرْقٌ مَقِيسٌ بِإِشَارَةٍ، مِثْلُ زَائِدِ صِفْرٍ فَاصِلَةِ ثَلَاثَةٍ سَبْعَةٍ وَاحِدٍ بِالمِئَةِ عِنْدَ قِمَّةِ المَدَى. وَالدِّقَّةُ: مُوَاصَفَةٌ يُعْلِنُهَا الصَّانِعُ، لَا قِيَاسٌ، كَمُرْسِلٍ دِقَّتُهُ صِفْرٌ فَاصِلَةُ صِفْرٍ سَبْعَةٍ خَمْسَةٍ بِالمِئَةِ. وَعَدَمُ التَّأَكُّدِ: مَدَى الشَّكِّ فِي قِيَاسِكَ أَنْتَ لِلْخَطَإِ. وَالفَرْقُ عَمَلِيٌّ: خَطَأٌ صِفْرٌ فَاصِلَةُ ثَمَانِيَةٍ وَأَرْبَعِينَ، وَالتَّفَاوُتُ نِصْفٌ بِالمِئَةِ، يَبْدُو نَاجِحًا؛ لٰكِنْ بِعَدَمِ تَأَكُّدٍ قَدْرُهُ صِفْرٌ فَاصِلَةُ وَاحِدٍ بِالمِئَةِ، يَقَعُ الخَطَأُ الحَقِيقِيُّ بَيْنَ صِفْرٍ فَاصِلَةِ ثَمَانِيَةٍ وَثَلَاثِينَ وَصِفْرٍ فَاصِلَةِ ثَمَانِيَةٍ وَخَمْسِينَ، فَقَدْ يَكُونُ رَاسِبًا وَأَنْتَ لَا تَدْرِي.",
    # 2
    "وَيُعَبَّرُ عَنِ الخَطَإِ نِسْبَةً مِنَ المَدَى، وَهُوَ الأَشْيَعُ فِي المَصَافِي؛ أَوْ مِنَ القِرَاءَةِ، فَيَضِيقُ عِنْدَ القِيَمِ الصَّغِيرَةِ، وَيَشِيعُ فِي مُوَاصَفَاتِ المَرَاجِعِ؛ أَوْ مِنَ الحَدِّ الأَعْلَى، فَيُطَابِقُ المَدَى حِينَ يَبْدَأُ مِنَ الصِّفْرِ فَقَطْ. وَالفَخُّ: نِصْفٌ بِالمِئَةِ مِنَ القِرَاءَةِ عِنْدَ عَشَرَةٍ بِالمِئَةِ مِنَ المَدَى، يُسَاوِي صِفْرًا فَاصِلَةَ صِفْرٍ خَمْسَةٍ بِالمِئَةِ مِنَ المَدَى فَقَطْ، فَرْقُ عَشَرَةِ أَضْعَافٍ.",
    # 3
    "وَنِسْبَةُ تِي يُو آر: التَّفَاوُتُ المَسْمُوحُ، مَقْسُومًا عَلَى عَدَمِ التَّأَكُّدِ المُوَسَّعِ لِقِيَاسِكَ؛ وَالحَدُّ الأَدْنَى المُتَعَارَفُ صِنَاعِيًّا أَرْبَعَةٌ إِلَى وَاحِدٍ. عَشَرَةٌ فَأَكْثَرُ مُمْتَازٌ. وَمِنْ أَرْبَعَةٍ إِلَى عَشَرَةٍ مَقْبُولٌ مَعَ ذِكْرِ عَدَمِ التَّأَكُّدِ. وَمِنِ اثْنَيْنِ إِلَى أَرْبَعَةٍ هَامِشِيٌّ، يَحْتَاجُ نِطَاقَ حِمَايَةٍ أَوْ مَرْجِعًا أَدَقَّ. وَأَقَلُّ مِنِ اثْنَيْنِ غَيْرُ مَقْبُولٍ.",
    # 4
    "وَالمِيزَانِيَّةُ سَبْعُ مُسَاهَمَاتٍ: دِقَّةُ وَحْدَةِ الضَّغْطِ، وَقِيَاسُ التَّيَّارِ، وَتَمْيِيزُ الشَّاشَةِ، وَالتَّكْرَارِيَّةُ، وَأَثَرُ الحَرَارَةِ، وَاسْتِقْرَارُ الضَّغْطِ لَحْظَةَ الِالْتِقَاطِ، وَهُنَا تَدْخُلُ مُشْكِلَةُ الِانْهِيَارِ كَمِّيًّا، وَانْحِرَافُ المَرْجِعِ مُنْذُ آخِرِ مُعَايَرَتِهِ. وَتُحَوَّلُ وَفْقَ دَلِيلِ جِي يُو إِمْ: المُوَاصَفَةُ ذَاتُ الحَدَّيْنِ تُقْسَمُ عَلَى جَذْرِ ثَلَاثَةٍ، وَتَمْيِيزُ الشَّاشَةِ عَلَى ضِعْفِ جَذْرِ ثَلَاثَةٍ، وَالتَّكْرَارِيَّةُ هِيَ الِانْحِرَافُ المِعْيَارِيُّ. ثُمَّ تُجْمَعُ تَرْبِيعِيًّا، وَتُضْرَبُ فِي مُعَامِلِ التَّغْطِيَةِ اثْنَيْنِ، لِثِقَةٍ نَحْوَ خَمْسَةٍ وَتِسْعِينَ بِالمِئَةِ.",
    # 5
    "مِثَالٌ تَوْضِيحِيٌّ بِالكِيلُوغْرَامِ عَلَى السَّنْتِيمِتْرِ المُرَبَّعِ: المَرْجِعُ صِفْرٌ فَاصِلَةُ صِفْرٍ وَاحِدٍ خَمْسَةٍ ثَلَاثَةٍ، يُصْبِحُ بَعْدَ القِسْمَةِ صِفْرًا فَاصِلَةَ صِفْرٍ صِفْرٍ ثَمَانِيَةٍ ثَمَانِيَةٍ؛ وَهٰكَذَا البَقِيَّةُ. وَانْحِرَافُ المَرْجِعِ هُنَا دَاخِلُ بَنْدِهِ، لِأَنَّ مُوَاصَفَةَ السَّنَةِ تَشْمَلُ الِاسْتِقْرَارَ الطَّوِيلَ. المَجْمُوعُ التَّرْبِيعِيُّ صِفْرٌ فَاصِلَةُ صِفْرٍ وَاحِدٍ خَمْسَةٍ خَمْسَةٍ، وَبِالضَّرْبِ فِي اثْنَيْنِ صِفْرٌ فَاصِلَةُ صِفْرٍ ثَلَاثَةٍ وَاحِدٍ، أَيْ صِفْرٌ فَاصِلَةُ صِفْرٍ سَبْعَةٍ أَرْبَعَةٍ بِالمِئَةِ مِنَ المَدَى، وَتِي يُو آر نَحْوُ سِتَّةٍ فَاصِلَةِ ثَمَانِيَةٍ. أَكْبَرُ المُسَاهَمَاتِ: المَرْجِعُ، ثُمَّ التَّكْرَارِيَّةُ، ثُمَّ التَّيَّارُ. أَمَّا اسْتِقْرَارُ الضَّغْطِ فَتَتَحَكَّمُ فِيهِ مَجَّانًا: أَصْلِحِ التَّسْرِيبَ، وَقَصِّرِ الخُرْطُومَ، وَانْتَظِرْ؛ فَإِنْ نَصَّفْتَهُ ارْتَفَعَ تِي يُو آر إِلَى نَحْوِ سَبْعَةٍ فَاصِلَةِ اثْنَيْنِ، دُونَ شِرَاءِ شَيْءٍ.",
    # 6
    "وَنِطَاقُ الحِمَايَةِ يُضَيِّقُ حُدُودَ القَبُولِ بِمِقْدَارِ عَدَمِ التَّأَكُّدِ. قَاعِدَةُ قَرَارٍ مُتَحَفِّظَةٌ: نَاجِحٌ إِذَا لَمْ يَتَجَاوَزِ الخَطَأُ زَائِدَ عَدَمِ التَّأَكُّدِ التَّفَاوُتَ؛ وَرَاسِبٌ إِذَا تَجَاوَزَهُ الخَطَأُ نَاقِصَ عَدَمِ التَّأَكُّدِ؛ وَمَا بَيْنَهُمَا مِنْطَقَةُ شَكٍّ، تَحْتَاجُ قَرَارًا هَنْدَسِيًّا مُوَثَّقًا. فِي مِثَالِنَا: صِفْرٌ فَاصِلَةُ ثَلَاثَةٍ سَبْعَةٍ وَاحِدٍ أَرْبَعَةٍ، زَائِدَ صِفْرٍ فَاصِلَةِ صِفْرٍ سَبْعَةٍ ثَلَاثَةٍ ثَمَانِيَةٍ، يُسَاوِي صِفْرًا فَاصِلَةَ أَرْبَعَةٍ أَرْبَعَةٍ خَمْسَةٍ اثْنَيْنِ بِالمِئَةِ، دُونَ النِّصْفِ: نَاجِحٌ مُؤَكَّدٌ، بِهَامِشٍ نَحْوَ أَحَدَ عَشَرَ بِالمِئَةِ مِنَ التَّفَاوُتِ فَقَطْ؛ فَالتَّوْصِيَةُ: قَصِّرِ الفَتْرَةَ، وَرَاقِبِ الِاتِّجَاهَ.",
    # 7
    "وَفِي الشَّهَادَةِ: عَدَمُ التَّأَكُّدِ المُوَسَّعُ بِمُعَامِلِ تَغْطِيَةٍ اثْنَيْنِ، وَقَاعِدَةُ القَرَارِ. فَشَهَادَةٌ تُعْلِنُ «نَاجِحٌ» دُونَهُمَا تُخْفِي المَعْلُومَةَ الَّتِي تُحَدِّدُ قِيمَةَ الحُكْمِ. وَبِهٰذَا يَكْتَمِلُ الجُزْءُ الأَوَّلُ: مُعَايَرَةُ مُرْسِلَاتِ الضَّغْطِ.",
]

# Every spoken or shown value is checked against the data module; stop if it drifts.
assert f"{D.ERR_PCT_RIGHT:.3f}" == "0.371" and D.XMTR_ACCURACY_PCT == 0.075               # seg 1
assert (D.DEMO_E, D.DEMO_U, f"{D.DEMO_LO:.2f}", f"{D.DEMO_HI:.2f}") == (0.48, 0.10, "0.38", "0.58")  # seg 1
assert f"{D.RDG_AS_SPAN_PCT:.2f}" == "0.05" and D.TUR_MIN == 4                           # seg 2, 3
assert f"{D.A_REF:.4f}" == "0.0153" and f"{D.BUDGET[0][3]:.4f}" == "0.0088"              # seg 5
assert f"{D.U_C:.4f}" == "0.0155" and f"{D.U_EXP:.3f}" == "0.031"                        # seg 5
assert f"{D.U_EXP_PCT:.3f}" == "0.074" and f"{D.TUR:.1f}" == "6.8" and f"{D.TUR_HALF:.1f}" == "7.2"
assert f"{D.GUARD_SUM:.4f}" == "0.4452" and round(D.GUARD_MARGIN_OF_TOL) == 11           # seg 6

AUDIO_DIR = audio_dir_for(__file__)


class PtCalEp07(SyncedScene):
    def c(self, seg, phrase, nth=1):
        return self.cue(seg, phrase, nth)

    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        self.seg1_words()
        self.seg2_expression()
        self.seg3_tur()
        self.seg4_budget()
        self.seg5_example()
        self.seg6_guard()
        self.seg7_certificate()

    def axis(self, y=-0.6, lo=0.0, hi=0.7, x0=-6.0, x1=6.0):
        """Horizontal error axis in % of span; returns (group, X())."""
        X = lambda v: x0 + (x1 - x0) * (v - lo) / (hi - lo)          # noqa: E731
        line = Line([x0, y, 0], [x1, y, 0], stroke_width=3, color=INK)
        ticks = VGroup()
        for v in np.arange(lo, hi + 1e-9, 0.1):
            ticks.add(Line([X(v), y - 0.1, 0], [X(v), y + 0.1, 0], stroke_width=2, color=INK))
            ticks.add(tag(fmt(v, 1), FS_TAG).next_to([X(v), y - 0.1, 0], DOWN, buff=0.1))
        unit = tag("error, % of span", FS_TAG, GREY_INK).next_to(line, DOWN, buff=0.55).align_to(line, RIGHT)
        return VGroup(line, ticks, unit), X

    # ---------------- Segment 1: error, accuracy, uncertainty ----------------
    def seg1_words(self):
        title_segment(self, "Error, uncertainty and TUR", "How much can you trust a PASS?", 7)
        self.sync(self.c(1, "ثَلَاثُ كَلِمَاتٍ") - 0.6)
        self.clear()
        self.sec = section_title(self, "Three words that get mixed up")
        cards = VGroup(card("Error", f"measured, with a sign\n{sfmt(D.ERR_PCT_RIGHT, 3)} % at 100 %", FLUID, 4.0),
                       card("Accuracy", f"a maker's specification\ne.g. ±{fmt(D.XMTR_ACCURACY_PCT, 3)} %", GREY_INK, 4.0),
                       card("Uncertainty", "the doubt in YOUR\nmeasurement of the error", MOVE, 4.0)) \
            .arrange(RIGHT, buff=0.3).move_to([0, 1.9, 0])
        for k, ph in enumerate(["الخَطَأُ:", "وَالدِّقَّةُ", "وَعَدَمُ التَّأَكُّدِ"]):
            self.sync(self.c(1, ph))
            self.play(FadeIn(cards[k], shift=DOWN * 0.1), run_time=0.5)
        # E = 0.48 %, U = 0.10 %: the true error may pass the limit
        self.sync(self.c(1, "وَالفَرْقُ"))
        ax, X = self.axis(y=-1.3)
        tol = DashedLine([X(D.TOL_PCT), -1.3, 0], [X(D.TOL_PCT), 0.3, 0], color=BAD, stroke_width=4)
        tl = tag(f"tolerance {fmt(D.TOL_PCT, 2)} %", FS_TAG + 1, BAD).next_to(tol, UP, buff=0.1)
        dot = Dot([X(D.DEMO_E), -1.3, 0], radius=0.11, color=FLUID)
        dl = tag(f"E = {fmt(D.DEMO_E, 2)} %: looks like a PASS", FS_TAG + 1, FLUID).next_to(dot, UP, buff=0.55) \
            .align_to([X(D.TOL_PCT) - 0.3, 0, 0], RIGHT)
        self.play(Create(ax), Create(tol), FadeIn(tl), run_time=0.6)
        self.play(FadeIn(dot, scale=1.5), FadeIn(dl), run_time=0.5)
        self.sync(self.c(1, "لٰكِنْ بِعَدَمِ"))
        band = Rectangle(width=X(D.DEMO_HI) - X(D.DEMO_LO), height=0.24, stroke_width=0).set_fill(MOVE, 0.45) \
            .move_to([(X(D.DEMO_LO) + X(D.DEMO_HI)) / 2, -1.3, 0]).set_z_index(-1)
        bl = tag(f"U = ±{fmt(D.DEMO_U, 2)} % → true error {fmt(D.DEMO_LO, 2)} … {fmt(D.DEMO_HI, 2)} %", FS_TAG + 1, MOVE) \
            .next_to(ax, DOWN, buff=0.1).shift(LEFT * 1.2)
        self.play(GrowFromCenter(band), FadeIn(bl), run_time=0.8)
        self.sync(self.c(1, "فَقَدْ يَكُونُ"))
        maybe = tag("may be a FAIL", FS_TAG + 2, BAD, weight=BOLD).next_to(tol, RIGHT, buff=0.25).set_y(dl.get_y())
        self.play(FadeIn(maybe), Indicate(band, color=BAD), run_time=0.7)
        self.sync(self.end(1) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 2: % of span, % of reading, % of URV ----------------
    def seg2_expression(self):
        section_title(self, "Expressing the error", prev=self.sec)
        ch = Chart(-5.6, -2.9, 6.6, 4.4, (0, 100), (0, 0.6), xticks=[(0, "0"), (10, "10"), (50, "50"), (100, "100 %")],
                   yticks=[(0.5, "0.5 %")], xlabel="point, % of span", ylabel="allowed error, % of span")
        span_b = ch.line([(0, D.RDG_SPEC_PCT), (100, D.RDG_SPEC_PCT)], FLUID, 4)
        rdg = ch.line([(0, 0), (100, D.RDG_SPEC_PCT)], MOVE, 4)
        self.play(Create(ch.axes), FadeIn(ch.ticks), FadeIn(ch.xl), FadeIn(ch.yl), run_time=0.6)
        l1 = tag("% of span: the refinery usual", FS_TAG + 1, FLUID).move_to([4.2, 1.6, 0]).align_to([1.4, 0, 0], LEFT)
        l2 = tag("% of reading: narrows at small values\n(common in reference specs)", FS_TAG + 1, MOVE) \
            .next_to(l1, DOWN, buff=0.3).align_to(l1, LEFT)
        l3 = tag("% of URV: equals % of span\nonly if LRV = 0", FS_TAG + 1, GREY_INK).next_to(l2, DOWN, buff=0.3) \
            .align_to(l1, LEFT)
        fit(VGroup(l1, l2, l3), 5.4).align_to([1.4, 0, 0], LEFT)
        self.play(Create(span_b), FadeIn(l1), run_time=0.6)
        self.sync(self.c(2, "أَوْ مِنَ القِرَاءَةِ"))
        self.play(Create(rdg), FadeIn(l2), run_time=0.8)
        self.sync(self.c(2, "أَوْ مِنَ الحَدِّ"))
        self.play(FadeIn(l3), run_time=0.5)
        self.sync(self.c(2, "وَالفَخُّ"))
        g = DashedLine(ch.p(10, 0), ch.p(10, D.RDG_SPEC_PCT), color=BAD, stroke_width=3)
        d = Dot(ch.p(10, D.RDG_AS_SPAN_PCT), radius=0.09, color=BAD)
        t = tag(f"{fmt(D.RDG_SPEC_PCT, 1)} % of reading at {D.RDG_AT_PCT_SPAN} %\n"
                f"= {fmt(D.RDG_AS_SPAN_PCT, 2)} % of span: ten times smaller", FS_TAG + 1, BAD)
        fit(t, 5.4).next_to(l3, DOWN, buff=0.45).align_to(l1, LEFT)
        self.play(Create(g), FadeIn(d, scale=1.5), FadeIn(t), run_time=0.8)
        self.sync(self.end(2) - 0.5)
        self.clear(self.sec, run_time=0.5)

    # ---------------- Segment 3: TUR ----------------
    def seg3_tur(self):
        section_title(self, "Test Uncertainty Ratio", prev=self.sec)
        eq = equation(self, ["TUR", "=", "tolerance", "÷", "expanded uncertainty U"], colors={0: FLUID, 4: MOVE},
                      size=FS_LABEL, pos=[0, 2.3, 0], run_time=0.9)
        X = lambda v: -6.0 + 12.0 * v / 12.0                         # noqa: E731
        zones = [(0, 2, BAD, "< 2: not acceptable"), (2, 4, MOVE, "2–4: marginal\n(guard band or better ref.)"),
                 (4, 10, FLUID, "4–10: acceptable,\nstate U"), (10, 12, GOOD, "≥ 10: excellent")]
        bars = VGroup()
        labs = VGroup()
        for lo, hi, col, txt in zones:
            r = Rectangle(width=X(hi) - X(lo), height=0.5, stroke_width=0).set_fill(col, 0.55) \
                .move_to([(X(lo) + X(hi)) / 2, 0.4, 0])
            bars.add(r)
            labs.add(tag(txt, FS_TAG, col).next_to(r, DOWN, buff=1.1 if lo == 0 else 0.35))
        ticks = VGroup(*[tag(str(v), FS_TAG).next_to([X(v), 0.65, 0], UP, buff=0.08) for v in (0, 2, 4, 10)])
        minl = tag(f"industrial minimum {D.TUR_MIN} : 1", FS_TAG + 2, INK, weight=BOLD).move_to([0, -1.9, 0])
        self.sync(self.c(3, "وَالحَدُّ الأَدْنَى"))
        self.play(FadeIn(bars[2]), FadeIn(ticks), FadeIn(minl), run_time=0.6)
        order = [3, 2, 1, 0]
        cues = ["عَشَرَةٌ فَأَكْثَرُ", "وَمِنْ أَرْبَعَةٍ", "وَمِنِ اثْنَيْنِ", "وَأَقَلُّ"]
        for k, ph in zip(order, cues):
            self.sync(self.c(3, ph))
            self.play(FadeIn(bars[k]), FadeIn(labs[k]), run_time=0.45)
        self.sync(self.end(3) - 0.5)
        self.clear(self.sec, run_time=0.5)

    # ---------------- Segment 4: the budget and the conversions ----------------
    def seg4_budget(self):
        section_title(self, "The uncertainty budget", prev=self.sec)
        names = ["pressure module", "current measurement", "display resolution", "repeatability", "temperature",
                 "pressure stability at capture", "reference drift since cal."]
        cues = ["دِقَّةُ وَحْدَةِ", "وَقِيَاسُ التَّيَّارِ", "وَتَمْيِيزُ", "وَالتَّكْرَارِيَّةُ", "وَأَثَرُ",
                "وَاسْتِقْرَارُ", "وَانْحِرَافُ"]
        chips = VGroup(*[card(n, "", MOVE if k == 5 else INK, 4.0, FS_TAG) for k, n in enumerate(names)]) \
            .arrange(DOWN, buff=0.12).move_to([-4.2, -0.3, 0])
        for k, ph in enumerate(cues):
            self.sync(self.c(4, ph))
            self.play(FadeIn(chips[k], shift=RIGHT * 0.1), run_time=0.25)
            if k == 5:
                dn = tag("← the decay problem, in numbers", FS_TAG, MOVE).next_to(chips[5], RIGHT, buff=0.2)
                self.play(FadeIn(dn), run_time=0.4)
        self.sync(self.c(4, "وَتُحَوَّلُ"))
        self.play(FadeOut(dn), run_time=0.2)
        conv = VGroup(tag("GUM (JCGM 100):", FS_TAG + 2, weight=BOLD),
                      tag("spec ± a (rectangular):  u = a / √3", FS_TAG + 2),
                      tag("display resolution d:  u = d / (2√3)", FS_TAG + 2),
                      tag("repeatability:  u = standard deviation s", FS_TAG + 2),
                      tag("u_c = √( Σ uᵢ² )", FS_TAG + 2, FLUID),
                      tag("U = k · u_c,  k = 2  (about 95 %)", FS_TAG + 2, MOVE, weight=BOLD)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.0, -0.3, 0]).align_to([-0.8, 0, 0], LEFT)
        self.play(FadeIn(conv[0]), run_time=0.3)
        div = {0: "÷√3", 1: "÷√3", 4: "÷√3", 5: "÷√3", 2: "÷2√3", 3: "= s", 6: "in row 1"}
        divs = VGroup(*[tag(div[k], FS_TAG - 2, FLUID).next_to(chips[k], RIGHT, buff=0.1) for k in range(7)])
        groups = {"المُوَاصَفَةُ": [0, 1, 4, 5, 6], "وَتَمْيِيزُ الشَّاشَةِ عَلَى": [2], "وَالتَّكْرَارِيَّةُ هِيَ": [3]}
        for k, ph in zip(range(1, 4), groups):
            self.sync(self.c(4, ph))
            idx = groups[ph]
            self.play(FadeIn(conv[k], shift=RIGHT * 0.1), *[FadeIn(divs[i]) for i in idx],
                      *[chips[i].frame.animate.set_stroke(FLUID) for i in idx], run_time=0.5)
        self.sync(self.c(4, "ثُمَّ تُجْمَعُ"))
        sq = VGroup(*[divs[i].copy() for i in range(6)])
        self.add(sq)
        self.play(FadeIn(conv[4], shift=RIGHT * 0.1),
                  *[m.animate.move_to(conv[4].get_left() + RIGHT * 0.3).scale(0.4).set_opacity(0) for m in sq],
                  run_time=0.9)
        self.remove(sq)
        self.sync(self.c(4, "وَتُضْرَبُ"))
        self.play(FadeIn(conv[5], shift=RIGHT * 0.1), Indicate(conv[5], color=MOVE), run_time=0.6)
        self.sync(self.end(4) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 5: the worked budget ----------------
    def seg5_example(self):
        section_title(self, f"Worked example ({D.UNIT}, illustrative)", prev=self.sec)
        rows = [[n, fmt(a, 4), how, fmt(u, 5)] for n, a, how, u in D.BUDGET]
        tbl = data_table(self, ["contribution", "input", "divide", "u"], rows,
                         cues=[self.c(5, "المَرْجِعُ")] + [self.c(5, "وَهٰكَذَا")] * 5, pos=[-2.2, 0.55, 0],
                         size=FS_TAG + 1, width=8.6)
        self.sync(self.c(5, "وَانْحِرَافُ"))
        drift = tag("reference drift:\ninside its row\n(1-year spec\nincludes stability)", FS_TAG, GREY_INK) \
            .next_to(tbl, RIGHT, buff=0.4).align_to(tbl, UP)
        self.play(FadeIn(drift), run_time=0.5)
        res = VGroup(tag(f"u_c = {fmt(D.U_C, 5)}", FS_TAG + 2, FLUID),
                     tag(f"U = 2 × u_c = {fmt(D.U_EXP, 5)} {D.UNIT}", FS_TAG + 2, MOVE),
                     tag(f"= {fmt(D.U_EXP_PCT, 4)} % of span", FS_TAG + 2, MOVE),
                     tag(f"TUR = {fmt(D.TOL_PCT, 2)} ÷ {fmt(D.U_EXP_PCT, 4)} ≈ {fmt(D.TUR, 1)}", FS_TAG + 2, INK, weight=BOLD)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(tbl, DOWN, buff=0.35).align_to(tbl, LEFT)
        self.sync(self.c(5, "المَجْمُوعُ"))
        self.play(FadeIn(res[0]), run_time=0.4)
        self.sync(self.c(5, "وَبِالضَّرْبِ"))
        self.play(FadeIn(res[1]), run_time=0.4)
        self.sync(self.c(5, "أَيْ صِفْرٌ"))
        self.play(FadeIn(res[2]), run_time=0.4)
        self.sync(self.c(5, "وَتِي يُو آر"))
        self.play(FadeIn(res[3]), run_time=0.4)
        # ranking: the three largest, and the one you control for free
        self.sync(self.c(5, "أَكْبَرُ"))
        rank = D.BUDGET_RANKED
        ch = Chart(2.9, -3.2, 3.6, 2.4, (0, 7), (0, 0.01))
        bars = VGroup()
        for i, (n, _, _, u) in enumerate(rank):
            col = FLUID if i < 3 else (MOVE if n == "Pressure stability" else LIGHT_INK)
            b = Rectangle(width=0.4, height=max(ch.p(0, u)[1] - ch.y0, 0.02), stroke_width=0).set_fill(col, 0.85)
            b.move_to([ch.p(i + 0.6, 0)[0], ch.y0 + b.height / 2, 0])
            bars.add(b)
        short = {"Reference module": "ref", "Repeatability": "rep", "Current measurement": "I",
                 "Pressure stability": "stab", "Temperature": "T", "Display resolution": "d"}
        bnames = VGroup(*[tag(short[r[0]], FS_TAG - 4, GREY_INK).next_to([b.get_x(), ch.y0, 0], DOWN, buff=0.08)
                          for r, b in zip(rank, bars)])
        top3 = tag("top 3: reference,\nrepeatability, current", FS_TAG, FLUID).next_to(ch.axes, UP, buff=0.12) \
            .align_to(ch.axes, LEFT)
        self.play(FadeOut(drift), Create(ch.axes), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15),
                  FadeIn(top3), FadeIn(bnames), run_time=1.2)
        row_of = {n: i for i, (n, _, _, _) in enumerate(D.BUDGET)}
        hls = []
        for i, ph in enumerate([None, "ثُمَّ التَّكْرَارِيَّةُ", "ثُمَّ التَّيَّارُ"]):
            if ph:
                self.sync(self.c(5, ph))
            self.play(Indicate(bars[i], color=FLUID, scale_factor=1.3), run_time=0.4)
            hls.append(highlight_row(self, tbl, row_of[rank[i][0]], FLUID))
        self.sync(self.c(5, "أَمَّا اسْتِقْرَارُ"))
        k = [i for i, b in enumerate(rank) if b[0] == "Pressure stability"][0]
        free = tag("stability: yours\nto control, free", FS_TAG, MOVE).next_to(top3, UP, buff=0.12).align_to(top3, LEFT)
        self.play(Indicate(bars[k], color=MOVE, scale_factor=1.3), FadeIn(free), FadeOut(VGroup(*hls)), run_time=0.7)
        self.sync(self.c(5, "فَإِنْ نَصَّفْتَهُ"))
        half = D.A_STAB_HALF / np.sqrt(3)
        self.play(bars[k].animate.stretch_to_fit_height(max(ch.p(0, half)[1] - ch.y0, 0.02), about_edge=DOWN),
                  run_time=0.7)
        tur2 = tag(f"TUR ≈ {fmt(D.TUR, 1)} → ≈ {fmt(D.TUR_HALF, 1)}\nnothing bought", FS_TAG + 1, GOOD, weight=BOLD) \
            .next_to(free, UP, buff=0.3).align_to(free, LEFT)
        self.play(FadeIn(tur2), run_time=0.5)
        self.sync(self.end(5) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 6: guard band and the decision rule ----------------
    def seg6_guard(self):
        section_title(self, "Guard band and decision rule", prev=self.sec)
        ax, X = self.axis(y=-0.2)
        acc = D.ACCEPT_LIMIT_PCT
        z_pass = Rectangle(width=X(acc) - X(0), height=0.9, stroke_width=0).set_fill(GOOD, 0.25) \
            .move_to([(X(0) + X(acc)) / 2, 0.35, 0])
        z_doubt = Rectangle(width=X(D.TOL_PCT + D.U_EXP_PCT) - X(acc), height=0.9, stroke_width=0) \
            .set_fill(GREY_INK, 0.25).move_to([(X(acc) + X(D.TOL_PCT + D.U_EXP_PCT)) / 2, 0.35, 0])
        z_fail = Rectangle(width=X(0.7) - X(D.TOL_PCT + D.U_EXP_PCT), height=0.9, stroke_width=0) \
            .set_fill(BAD, 0.25).move_to([(X(D.TOL_PCT + D.U_EXP_PCT) + X(0.7)) / 2, 0.35, 0])
        tol = DashedLine([X(D.TOL_PCT), -0.3, 0], [X(D.TOL_PCT), 1.35, 0], color=BAD, stroke_width=4)
        self.play(Create(ax), Create(tol), run_time=0.6)
        # the guard band narrows the acceptance limit by U
        ya = -1.35
        end = ValueTracker(D.TOL_PCT)
        accb = always_redraw(lambda: Line([X(0), ya, 0], [X(end.get_value()), ya, 0], stroke_width=10, color=GOOD))
        accl = tag("acceptance", FS_TAG, GOOD).next_to([X(0), ya, 0], UP, buff=0.12).align_to([X(0), 0, 0], LEFT)
        self.play(FadeIn(accb), FadeIn(accl), run_time=0.5)
        self.sync(self.c(6, "يُضَيِّقُ"))
        self.play(end.animate.set_value(acc), run_time=1.0)
        gb = BraceBetweenPoints([X(acc), ya - 0.08, 0], [X(D.TOL_PCT), ya - 0.08, 0], direction=DOWN, color=MOVE)
        gbl = tag("guard band = U", FS_TAG, MOVE).next_to(gb, DOWN, buff=0.05)
        self.play(FadeIn(gb), FadeIn(gbl), run_time=0.5)
        rules = VGroup(tag("PASS if |E| + U ≤ tolerance", FS_TAG + 2, GOOD),
                       tag("FAIL if |E| − U > tolerance", FS_TAG + 2, BAD),
                       tag("between: zone of doubt → documented engineering decision", FS_TAG + 2, GREY_INK)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([0, 2.5, 0])
        zt = [tag(t, FS_TAG, c, weight=BOLD).move_to(z).align_to(z, UP).shift(DOWN * 0.08)
              for t, c, z in (("PASS", GOOD, z_pass), ("FAIL", BAD, z_fail), ("doubt", GREY_INK, z_doubt))]
        zt[2].align_to(z_doubt, LEFT).shift(RIGHT * 0.12)
        self.sync(self.c(6, "نَاجِحٌ إِذَا"))
        self.play(FadeIn(z_pass), FadeIn(zt[0]), FadeIn(rules[0]), run_time=0.6)
        self.sync(self.c(6, "وَرَاسِبٌ"))
        self.play(FadeIn(z_fail), FadeIn(zt[1]), FadeIn(rules[1]), run_time=0.6)
        self.sync(self.c(6, "وَمَا بَيْنَهُمَا"))
        self.play(FadeIn(z_doubt), FadeIn(zt[2]), FadeIn(rules[2]), run_time=0.6)
        # the 41.928 result
        self.sync(self.c(6, "فِي مِثَالِنَا"))
        e = Dot([X(D.ERR_PCT_RIGHT), 0.35, 0], radius=0.11, color=FLUID)
        el = tag(f"E = {fmt(D.ERR_PCT_RIGHT, 4)} %", FS_TAG + 1, FLUID).move_to([0, -0.85, 0]) \
            .align_to([X(D.ERR_PCT_RIGHT) - 1.2, 0, 0], LEFT)
        self.play(FadeIn(e, scale=1.5), FadeIn(el), run_time=0.5)
        self.sync(self.c(6, "زَائِدَ صِفْرٍ"))
        yr = 1.1
        u = Rectangle(width=X(D.GUARD_SUM) - X(D.ERR_PCT_RIGHT), height=0.16, stroke_width=0).set_fill(MOVE, 0.9) \
            .move_to([(X(D.ERR_PCT_RIGHT) + X(D.GUARD_SUM)) / 2, yr, 0])
        ul = tag("E + U", FS_TAG, MOVE).next_to(u, LEFT, buff=0.15)
        self.play(GrowFromEdge(u, LEFT), FadeIn(ul), run_time=0.6)
        self.sync(self.c(6, "يُسَاوِي"))
        s = tag(f"{fmt(D.ERR_PCT_RIGHT, 4)} + {fmt(D.U_EXP_PCT, 4)} = {fmt(D.GUARD_SUM, 4)} % ≤ {fmt(D.TOL_PCT, 2)} %",
                FS_TAG + 2, INK, weight=BOLD).move_to([0, -2.5, 0])
        self.play(FadeIn(s), run_time=0.5)
        self.sync(self.c(6, "نَاجِحٌ مُؤَكَّدٌ"))
        m = BraceBetweenPoints([X(D.GUARD_SUM), yr + 0.1, 0], [X(D.TOL_PCT), yr + 0.1, 0], direction=UP, color=GOOD)
        ml = tag(f"margin {fmt(D.GUARD_MARGIN, 4)} % ≈ {round(D.GUARD_MARGIN_OF_TOL)} % of tolerance", FS_TAG + 1, GOOD) \
            .next_to(s, DOWN, buff=0.25)
        self.play(FadeIn(m), FadeIn(ml), Indicate(e, color=GOOD, scale_factor=1.5), run_time=0.6)
        self.sync(self.c(6, "فَالتَّوْصِيَةُ"))
        rec = tag("→ shorten the interval, watch the trend", FS_TAG + 2, MOVE).next_to(ml, DOWN, buff=0.2)
        self.play(FadeIn(rec), run_time=0.5)
        self.sync(self.end(6) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 7: the certificate; end of part 1 ----------------
    def seg7_certificate(self):
        section_title(self, "On the certificate", prev=self.sec)
        paper = Rectangle(width=6.2, height=3.2, color=INK, stroke_width=3).move_to([-3.0, 0.2, 0])
        lines = VGroup(tag("verdict: PASS", FS_TAG + 2),
                       tag(f"U = ±{fmt(D.U_EXP_PCT, 3)} % (k = 2)", FS_TAG + 2, MOVE, weight=BOLD),
                       tag("decision rule: guard band = U", FS_TAG + 2, MOVE, weight=BOLD)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(paper)
        self.play(Create(paper), FadeIn(lines[0]), run_time=0.5)
        self.play(FadeIn(lines[1]), run_time=0.4)
        self.sync(self.c(7, "وَقَاعِدَةُ"))
        self.play(FadeIn(lines[2]), run_time=0.4)
        self.sync(self.c(7, "فَشَهَادَةٌ"))
        warn = tag("'PASS' without U and the rule\nhides what the verdict is worth", FS_TAG + 2, BAD) \
            .next_to(paper, RIGHT, buff=0.6)
        self.play(FadeIn(warn), run_time=0.5)
        self.sync(self.c(7, "وَبِهٰذَا"))
        end = tag("End of part 1: pressure transmitter calibration", FS_LABEL, weight=BOLD).move_to([0, -2.7, 0])
        self.play(FadeIn(end), run_time=0.6)
        self.sync(self.end(7) + 1.5)


if __name__ == "__main__":
    main(__file__, "PtCalEp07", NARRATION)
