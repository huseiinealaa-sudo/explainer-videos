"""pt_cal, episode 5: calculation, verdict and certificate.

Every number on screen or in the narration comes from pt_cal_data. Sources: sources/pt_cal_source.md (§5)
and sources/pt_cal_ep05_verdict.md; storyboard: storyboard/pt_cal_ep05_verdict.md.

Build (from the repo root):
    python projects/pt_cal/pt_cal_ep05_verdict.py --preview   # 480p15 -> tmp/pt_cal_ep05_verdict/preview.mp4
    python projects/pt_cal/pt_cal_ep05_verdict.py             # 1080p30 -> output/pt_cal_ep05_verdict.mp4
"""
from explainer import *
from pt_cal_common import *
import pt_cal_data as D

# Fully diacritized narration (owner-approved 2026-09-28) — one entry per segment.
NARRATION = [
    # 1
    "هٰذِهِ مَادَّةٌ تَعْلِيمِيَّةٌ؛ وَالمَرْجِعُ المُلْزِمُ الأَدِلَّةُ الرَّسْمِيَّةُ وَإِجْرَاءَاتُ مُنْشَأَتِكَ. فِي المُعَايِرِ المُوَثِّقِ تُعَرِّفُ الإِجْرَاءَ: رَمْزُ المُرْسِلَةِ، بِي تِي مِئَةٌ وَوَاحِد؛ وَمَدَى الدَّخْلِ، مِنْ صِفْرٍ إِلَى اثْنَيْنِ وَأَرْبَعِينَ كِيلُوغْرَامًا عَلَى السَّنْتِيمِتْرِ المُرَبَّعِ؛ وَالخَرْجُ مِنْ أَرْبَعَةٍ إِلَى عِشْرِينَ مِلِّي أَمْبِير؛ وَدَالَّةُ النَّقْلِ، خَطِّيَّةٌ أَمْ جَذْرٌ، وَهِيَ الحَقْلُ الأَكْثَرُ خَطَأً؛ وَخَمْسُ نِقَاطٍ صُعُودًا وَهُبُوطًا؛ وَالتَّفَاوُتُ مِنْ أَمْرِ العَمَلِ، نِصْفٌ بِالمِئَةِ مِنَ المَدَى؛ وَقَبُولُ النُّقْطَةِ؛ وَعَدَدُ التَّكْرَارِ، لِكَشْفِ التَّكْرَارِيَّةِ.",
    # 2
    "وَآزْ فَاوْنْد تُسَجَّلُ قَبْلَ أَيِّ مَسَاسٍ: لَا ضَبْطَ، وَلَا تَصْفِيرَ، وَلَا تَهْيِئَةَ. عَلَيْهَا وَحْدَهَا يُبْنَى الحُكْمُ عَلَى القِيَاسَاتِ السَّابِقَةِ، وَتَحْدِيدُ الفَتْرَةِ، وَرَصْدُ الِانْحِرَافِ عَبْرَ السِّنِينَ. وَآزْ لِفْت بَعْدَ الضَّبْطِ تُثْبِتُ العَوْدَةَ دَاخِلَ التَّفَاوُتِ؛ وَإِنْ نَجَحَ وَلَمْ يُلْمَسْ فَهُمَا مُتَسَاوِيَتَانِ مَعَ مُلَاحَظَةِ: لَا ضَبْطَ مَطْلُوبٌ. وَشَهَادَةٌ بِآزْ لِفْت وَحْدَهَا تُخْفِي الأَهَمَّ؛ وَفِي النَّقْلِ التِّجَارِيِّ لَا تَدْفَعُ عَنْ فَوَاتِيرِ الفَتْرَةِ السَّابِقَةِ.",
    # 3
    "وَالحِسَابُ: التَّيَّارُ المُتَوَقَّعُ عِنْدَ الدَّخْلِ الفِعْلِيِّ المَقِيسِ، لَا الِاسْمِيِّ: أَرْبَعَةٌ، زَائِدَ نِسْبَةِ الدَّخْلِ مِنَ المَدَى فِي سِتَّةَ عَشَرَ. وَالخَطَأُ: المَقِيسُ نَاقِصَ المُتَوَقَّعِ، مَقْسُومًا عَلَى سِتَّةَ عَشَرَ. مِثَالٌ: النُّقْطَةُ اثْنَانِ وَأَرْبَعُونَ، لٰكِنَّ المِضَخَّةَ وَقَفَتْ عِنْدَ وَاحِدٍ وَأَرْبَعِينَ فَاصِلَةَ تِسْعَةٍ اثْنَيْنِ ثَمَانِيَةٍ، وَالمَقِيسُ عِشْرُونَ فَاصِلَةَ صِفْرٍ ثَلَاثَةٍ اثْنَيْنِ. نَمُوذَجُ إِكْسِل بِعِشْرِينَ ثَابِتَةً يُعْطِي صِفْرًا فَاصِلَةَ اثْنَيْنِ بِالمِئَةِ. وَالصَّحِيحُ: المُتَوَقَّعُ تِسْعَةَ عَشَرَ فَاصِلَةَ تِسْعَةٍ سَبْعَةٍ اثْنَيْنِ سِتَّةٍ، فَالخَطَأُ صِفْرٌ فَاصِلَةُ ثَلَاثَةٍ سَبْعَةٍ وَاحِدٍ بِالمِئَةِ. بَقِيَ نَاجِحًا، لٰكِنَّ اسْتِهْلَاكَ التَّفَاوُتِ قَفَزَ مِنْ أَرْبَعِينَ بِالمِئَةِ إِلَى أَرْبَعَةٍ وَسَبْعِينَ، فَانْقَلَبَ تَقْدِيرُ حَالَةِ المُرْسِلِ.",
    # 4
    "وَلِلْجَذْرِ التَّرْبِيعِيِّ مُعَادَلَةٌ أُخْرَى: أَرْبَعَةٌ، زَائِدَ سِتَّةَ عَشَرَ فِي جَذْرِ النِّسْبَةِ. عِنْدَ عَشَرَةٍ بِالمِئَةِ: تِسْعَةٌ فَاصِلَةُ صِفْرٍ سِتَّةٍ، بَدَلَ خَمْسَةٍ فَاصِلَةِ سِتَّةٍ؛ وَعِنْدَ النِّصْفِ: خَمْسَةَ عَشَرَ فَاصِلَةَ ثَلَاثَةٍ، بَدَلَ اثْنَيْ عَشَرَ. وَالفَخُّ يُعْرَفُ هٰكَذَا: الصِّفْرُ وَالمِئَةُ مُمْتَازَتَانِ، وَالنِّقَاطُ الوُسْطَى رَاسِبَةٌ بِفُرُوقٍ ضَخْمَةٍ مُنْتَظِمَةٍ: المُرْسِلُ بِالجَذْرِ وَالإِجْرَاءُ خَطِّيٌّ. فَتَحَقَّقْ مِنْ دَالَّةِ النَّقْلِ عَبْرَ هَارْت قَبْلَ أَنْ تَضْبِطَ فَتُفْسِدَهُ.",
    # 5
    "وَفِي الشَّهَادَةِ: رَقْمٌ فَرِيدٌ، وَتَعْرِيفُ المُرْسِلَةِ، وَالمَدَى بِوَحْدَتِهِ الصَّحِيحَةِ، وَالتَّفَاوُتُ وَمَصْدَرُهُ، وَهُوِيَّةُ المَرْجِعِ وَشَهَادَتُهُ وَتَارِيخُ انْتِهَائِهَا، وَالظُّرُوفُ البِيئِيَّةُ، وَآزْ فَاوْنْد وَآزْ لِفْت كَامِلَتَيْنِ، وَعَدَمُ التَّأَكُّدِ بِمُعَامِلِ تَغْطِيَةٍ اثْنَيْنِ، وَالحُكْمُ وَقَاعِدَتُهُ، وَالتَّوَارِيخُ وَالتَّوَاقِيعُ. وَالمَرْجِعُ المُنْتَهِي يُبْطِلُ كُلَّ شَهَادَةٍ صَدَرَتْ بِهِ، لِانْقِطَاعِ الإِسْنَادِ إِلَى المَعَايِيرِ الوَطَنِيَّةِ؛ فَنَبِّهْ قَبْلَ شَهْرٍ. وَالفَتْرَةُ قَرَارٌ: الحَلَقَاتُ الحَرِجَةُ ثَلَاثَةٌ إِلَى سِتَّةِ أَشْهُرٍ، وَتَارِيخُ آزْ فَاوْنْد أَقْوَى العَوَامِلِ؛ فَمَنْ يَعُودُ دَائِمًا دَاخِلَ عِشْرِينَ بِالمِئَةِ مِنَ التَّفَاوُتِ تُطَالُ فَتْرَتُهُ، وَالمُقْتَرِبُ مِنَ الحَدِّ تُقَصَّرُ، مَعَ قَسْوَةِ الظُّرُوفِ وَتَوْصِيَةِ الصَّانِعِ وَالمُتَطَلَّبِ التَّنْظِيمِيِّ. وَالنَّتَائِجُ تُنْقَلُ إِلَكْتْرُونِيًّا إِلَى سِي إِمْ إِكْس أَوْ لُوجِيكَال، لَا بِالقَلَمِ. وَفِي الحَلْقَةِ القَادِمَةِ: مَتَى نَضْبِطُ المُرْسِلَ، وَكَيْفَ نَقْرَأُ نَمَطَ أَخْطَائِهِ.",
]

# Every spoken or shown value is checked against the data module; stop if it drifts.
assert D.TAG == "PT-101" and D.URV == 42 and D.TOL_PCT == 0.5                           # seg 1
assert f"{D.PV_ACTUAL:.3f}" == "41.928" and f"{D.I_MEASURED:.3f}" == "20.032"          # seg 3
assert f"{D.ERR_PCT_WRONG:.1f}" == "0.2" and f"{D.ERR_PCT_RIGHT:.3f}" == "0.371"        # seg 3
assert f"{D.I_EXP_ACTUAL:.4f}" == "19.9726" and round(D.TOL_USED_RIGHT) == 74          # seg 3
assert f"{D.SQRT_TABLE[1][2]:.2f}" == "9.06" and f"{D.DP_50_SQRT_MA:.1f}" == "15.3"     # seg 4
assert D.INTERVAL_CRITICAL_MONTHS == (3, 6) and D.EXTEND_WITHIN_PCT_OF_TOL == 20       # seg 5

AUDIO_DIR = audio_dir_for(__file__)


class PtCalEp05(SyncedScene):
    def c(self, seg, phrase, nth=1):
        return self.cue(seg, phrase, nth)

    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        self.seg1_fields()
        self.seg2_found_left()
        self.seg3_calc()
        self.seg4_sqrt()
        self.seg5_certificate()

    # ---------------- Segment 1: the procedure fields ----------------
    def seg1_fields(self):
        title_segment(self, "Calculation, verdict, certificate", "From readings to a defensible result", 5)
        self.sync(self.c(1, "فِي المُعَايِرِ") - 0.6)
        self.clear()
        self.sec = section_title(self, "Documenting Calibrator: the procedure")
        screen = RoundedRectangle(width=8.6, height=5.6, corner_radius=0.2, color=INK, stroke_width=4) \
            .move_to([-1.9, -0.45, 0])
        rows = [("Tag", D.TAG, "رَمْزُ"),
                ("Input", f"0 … {fmt(D.URV, 0)} {D.UNIT}", "وَمَدَى الدَّخْلِ"),
                ("Output", f"{fmt(D.I_LO, 0)} … {fmt(D.I_HI, 0)} mA", "وَالخَرْجُ"),
                ("Transfer function", "linear  |  square root", "وَدَالَّةُ النَّقْلِ"),
                ("Points", f"{len(D.CAL_POINTS_PCT)} up + {len(D.CAL_POINTS_PCT)} down", "وَخَمْسُ"),
                ("Tolerance", f"±{fmt(D.TOL_PCT, 2)} % of span · work order", "وَالتَّفَاوُتُ"),
                ("Point acceptance", "auto / manual", "وَقَبُولُ"),
                ("Repeats", "n → repeatability", "وَعَدَدُ")]
        lines = VGroup()
        for k, v, _ in rows:
            kk = tag(k, FS_TAG + 2, GREY_INK)
            vv = tag(v, FS_TAG + 2, INK)
            lines.add(VGroup(kk, vv))
        for i, ln in enumerate(lines):
            ln[0].move_to([-5.7, 1.65 - 0.62 * i, 0], aligned_edge=LEFT)
            ln[1].move_to([-2.7, 1.65 - 0.62 * i, 0], aligned_edge=LEFT)
        xm = transmitter().scale(0.9).move_to([4.8, 1.9, 0])
        self.play(Create(screen), FadeIn(xm), run_time=0.7)
        for ln, (_, _, ph) in zip(lines, rows):
            self.sync(self.c(1, ph))
            self.play(FadeIn(ln, shift=RIGHT * 0.1), run_time=0.4)
            if ph == "وَدَالَّةُ النَّقْلِ":
                warn = SurroundingRectangle(ln, color=BAD, buff=0.1, corner_radius=0.08, stroke_width=4)
                wl = tag("most frequent mistake", FS_TAG, BAD).next_to(screen, RIGHT, buff=0.3) \
                    .align_to(ln, DOWN)
                self.play(Create(warn), FadeIn(wl), run_time=0.5)
        self.sync(self.end(1) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 2: As-Found and As-Left ----------------
    def seg2_found_left(self):
        section_title(self, "As-Found first, As-Left after the trim", prev=self.sec)
        n = len(D.AF_HISTORY)
        ch = Chart(-6.0, -2.6, 7.2, 4.4, (0.5, n + 0.5), (0, 0.65),
                   xticks=[(k, f"year {k}") for k in range(1, n + 1)],
                   yticks=[(0, "0"), (D.TOL_PCT, fmt(D.TOL_PCT, 2))], ylabel="largest error, % of span")
        tol = ch.hline(D.TOL_PCT, BAD, dashed=True, width=3)
        tl = tag("tolerance", FS_TAG, BAD).next_to(tol, UP, buff=0.08).align_to(tol, LEFT).shift(RIGHT * 0.25)
        hand = VGroup(icon("lock", MOVE, 0.5), tag("no trim, no zero,\nno configuration", FS_TAG, MOVE)) \
            .arrange(RIGHT, buff=0.15).move_to([4.6, 2.3, 0])
        self.play(Create(ch.axes), FadeIn(ch.ticks), FadeIn(ch.yl), Create(tol), FadeIn(tl), run_time=0.8)
        self.sync(self.c(2, "لَا ضَبْطَ"))
        self.play(FadeIn(hand), run_time=0.5)
        dots = ch.dots([(k + 1, v) for k, v in enumerate(D.AF_HISTORY)], FLUID, 0.09)
        af = tag("As-Found", FS_TAG + 2, FLUID).next_to(dots[0], RIGHT, buff=0.2)
        self.sync(self.c(2, "عَلَيْهَا وَحْدَهَا"))
        self.play(FadeIn(af), LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.3), run_time=1.8)
        drift = Arrow(dots[0].get_center() + UP * 0.35, dots[-2].get_center() + UP * 0.35, buff=0.1,
                      stroke_width=3, color=GREY_INK, max_tip_length_to_length_ratio=0.08)
        dl = tag("drift over the years", FS_TAG, GREY_INK).next_to(drift, UP, buff=0.1).shift(LEFT * 0.6)
        self.sync(self.c(2, "وَرَصْدُ"))
        self.play(GrowArrow(drift), FadeIn(dl), run_time=0.7)
        self.sync(self.c(2, "وَآزْ لِفْت"))
        al = Dot(ch.p(n + 0.18, D.AL_AFTER_TRIM), radius=0.09, color=GOOD)
        trim = Arrow(dots[-1].get_center(), al.get_center(), buff=0.12, stroke_width=3, color=MOVE,
                     max_tip_length_to_length_ratio=0.2)
        all_ = tag("As-Left", FS_TAG + 2, GOOD).next_to(al, RIGHT, buff=0.15)
        self.play(Indicate(dots[-1], color=BAD, scale_factor=1.8), dots[-1].animate.set_color(BAD), run_time=0.6)
        self.play(GrowArrow(trim), FadeIn(al), FadeIn(all_), run_time=0.8)
        self.sync(self.c(2, "وَإِنْ نَجَحَ"))
        eq = tag("untouched: As-Found = As-Left\n'no adjustment required'", FS_TAG, GOOD) \
            .next_to(hand, DOWN, buff=0.45).align_to([1.8, 0, 0], LEFT)
        self.play(FadeIn(eq), run_time=0.5)
        self.sync(self.c(2, "وَشَهَادَةٌ"))
        cert = VGroup(Rectangle(width=3.4, height=1.6, color=INK, stroke_width=3),
                      tag("As-Found", FS_TAG, GREY_INK), tag("As-Left", FS_TAG))
        VGroup(cert[1], cert[2]).arrange(RIGHT, buff=0.5).move_to(cert[0].get_top() + DOWN * 0.35)
        vals = VGroup(*[Line(ORIGIN, RIGHT * 0.8, stroke_width=3, color=INK) for _ in range(3)]) \
            .arrange(DOWN, buff=0.2).next_to(cert[2], DOWN, buff=0.2)
        gaps = VGroup(*[DashedLine(ORIGIN, RIGHT * 0.8, stroke_width=2, color=LIGHT_INK) for _ in range(3)]) \
            .arrange(DOWN, buff=0.2).next_to(cert[1], DOWN, buff=0.2)
        cert.add(vals, gaps)
        cert.move_to([4.3, -1.3, 0])
        empty = cross(VGroup(cert[1]), BAD, 4, pad=0.05)
        ct = tag("custody transfer:\npast invoices\ncannot be defended", FS_TAG, BAD).next_to(cert, DOWN, buff=0.25)
        self.play(FadeIn(cert), run_time=0.5)
        self.play(Create(empty), run_time=0.4)
        self.sync(self.c(2, "وَفِي النَّقْلِ"))
        self.play(FadeIn(ct), run_time=0.5)
        self.sync(self.end(2) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 3: the calculation; the 41.928 example ----------------
    def seg3_calc(self):
        section_title(self, "Expected current at the actual input", prev=self.sec)
        e1 = equation(self, ["I_expected", "=", "4", "+", "(PV_actual − LRV) / (URV − LRV)", "×", "16"],
                      colors={0: MOVE, 4: FLUID}, size=FS_LABEL, pos=[0, 2.6, 0], run_time=1.0)
        self.sync(self.c(3, "وَالخَطَأُ"))
        e2 = equation(self, ["Error %", "=", "(I_measured − I_expected) / 16", "×", "100"],
                      colors={0: BAD}, size=FS_LABEL, pos=[0, 1.85, 0], run_time=0.9)
        # the pump stopped short of the nominal point
        self.sync(self.c(3, "مِثَالٌ"))
        x0, x1, v0, v1 = -5.6, 5.6, 41.85, 42.02
        X = lambda v: x0 + (x1 - x0) * (v - v0) / (v1 - v0)          # noqa: E731
        scale = Line([x0, 0.8, 0], [x1, 0.8, 0], stroke_width=3, color=INK)
        nom = VGroup(Line([X(D.PV_NOMINAL), 0.62, 0], [X(D.PV_NOMINAL), 0.98, 0], stroke_width=4, color=INK),
                     tag(f"nominal {fmt(D.PV_NOMINAL, 3)}", FS_TAG).next_to([X(D.PV_NOMINAL), 0.98, 0], UP,
                                                                           buff=0.08))
        ticks = VGroup(*[VGroup(Line([X(v), 0.7, 0], [X(v), 0.9, 0], stroke_width=2, color=INK),
                                tag(fmt(v, 2), FS_TAG - 2, GREY_INK).next_to([X(v), 0.7, 0], DOWN, buff=0.08))
                         for v in (41.90, 41.95)])
        act = Triangle(color=FLUID, stroke_width=3).set_fill(FLUID, 1).scale(0.13).rotate(PI) \
            .move_to([X(41.86), 0.98, 0])
        al = tag(f"pump stopped at {fmt(D.PV_ACTUAL, 3)} {D.UNIT}", FS_TAG, FLUID).next_to(act, UP, buff=0.1)
        self.play(Create(scale), FadeIn(nom), FadeIn(ticks), run_time=0.5)
        self.sync(self.c(3, "وَقَفَتْ"))
        self.play(FadeIn(act), act.animate.move_to([X(D.PV_ACTUAL), 0.98, 0]), run_time=0.9)
        al.next_to(act, UP, buff=0.1)
        self.play(FadeIn(al), run_time=0.4)
        self.sync(self.c(3, "وَالمَقِيسُ"))
        meas = tag(f"measured: {fmt(D.I_MEASURED, 4)} mA", FS_TAG + 2, MOVE).move_to([0, 0.05, 0])
        self.play(FadeIn(meas), run_time=0.5)
        left = card("Excel: fixed 20 mA",
                    f"4 + {fmt(D.PV_NOMINAL, 3)}/{fmt(D.SPAN, 0)} × 16 = {fmt(D.I_EXP_NOMINAL, 4)} mA\nerror = {fmt(D.ERR_PCT_WRONG, 3)} %",
                    BAD, 5.6).move_to([-3.2, -1.35, 0])
        right = card("actual input",
                     f"4 + {fmt(D.PV_ACTUAL, 3)}/{fmt(D.SPAN, 0)} × 16 = {fmt(D.I_EXP_ACTUAL, 4)} mA\nerror = {fmt(D.ERR_PCT_RIGHT, 3)} %",
                     GOOD, 5.6).move_to([3.2, -1.35, 0])
        self.sync(self.c(3, "نَمُوذَجُ"))
        self.play(FadeIn(left, shift=UP * 0.1), run_time=0.6)
        self.sync(self.c(3, "وَالصَّحِيحُ"))
        self.play(FadeIn(right, shift=UP * 0.1), run_time=0.6)

        def used_bar(frac, color, card_):
            frame = Rectangle(width=4.6, height=0.32, color=GREY_INK, stroke_width=2)
            frame.next_to(card_, DOWN, buff=0.35)
            fill = Rectangle(width=4.6 * frac, height=0.32, stroke_width=0).set_fill(color, 0.8) \
                .align_to(frame, LEFT).align_to(frame, DOWN)
            t = tag(f"{fmt(frac * 100, 0)} % of the tolerance used", FS_TAG, color).next_to(frame, DOWN, buff=0.1)
            return frame, fill, t

        f1, b1, t1 = used_bar(D.TOL_USED_WRONG / 100, BAD, left)
        f2, b2, t2 = used_bar(D.TOL_USED_RIGHT / 100, GOOD, right)
        self.sync(self.c(3, "بَقِيَ نَاجِحًا"))
        self.play(Create(f1), Create(f2), run_time=0.3)
        self.play(GrowFromEdge(b1, LEFT), FadeIn(t1), run_time=0.6)
        self.sync(self.c(3, "قَفَزَ"))
        self.play(GrowFromEdge(b2, LEFT), FadeIn(t2), run_time=0.9)
        self.sync(self.end(3) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 4: square-root transfer and the trap ----------------
    def seg4_sqrt(self):
        section_title(self, "Square-root transmitters", prev=self.sec)
        eq = equation(self, ["I", "=", "4", "+", "16", "×", "√( (PV − LRV) / (URV − LRV) )"],
                      colors={6: MOVE}, size=FS_LABEL, pos=[0, 2.75, 0], run_time=0.9)
        ch = Chart(-5.6, -3.2, 5.2, 4.6, (0, 100), (4, 20), xticks=[(0, "0"), (50, "50"), (100, "100 %")],
                   yticks=[(4, "4"), (12, "12"), (20, "20")], ylabel="mA")
        lin = ch.line([(0, 4), (100, 20)], GREY_INK, 3)
        sq = ch.line([(p, D.i_sqrt(D.LRV + p / 100 * D.SPAN)) for p in [q / 4 for q in range(0, 81)] + list(range(21, 101))],
                     MOVE, 4)
        ll = tag("linear", FS_TAG, GREY_INK).next_to(ch.p(85, 4 + 0.16 * 85), DR, buff=0.08)
        sl = tag("square root", FS_TAG, MOVE).move_to(ch.p(40, 17.6))
        self.play(Create(ch.axes), FadeIn(ch.ticks), FadeIn(ch.yl), Create(lin), FadeIn(ll), run_time=0.7)
        self.play(Create(sq), FadeIn(sl), run_time=1.0)
        rows = [[f"{p} %", fmt(l, 3), fmt(s, 3)] for p, l, s in D.SQRT_TABLE if p in D.SQRT_SHOW]
        tbl = data_table(self, ["input", "linear mA", "√ mA"], rows, pos=[3.7, -0.35, 0], size=FS_TAG + 2)

        def guide(pct, row):
            _, l, s = [r for r in D.SQRT_TABLE if r[0] == pct][0]
            g = VGroup(DashedLine(ch.p(pct, 4), ch.p(pct, s), color=MOVE, stroke_width=2),
                       Dot(ch.p(pct, s), radius=0.08, color=MOVE), Dot(ch.p(pct, l), radius=0.08, color=GREY_INK))
            return g

        self.sync(self.c(4, "عِنْدَ عَشَرَةٍ"))
        g1 = guide(10, 0)
        self.play(Create(g1), run_time=0.6)
        h1 = highlight_row(self, tbl, 0, MOVE)
        self.sync(self.c(4, "وَعِنْدَ النِّصْفِ"))
        g2 = guide(50, 2)
        self.play(Create(g2), run_time=0.6)
        h2 = highlight_row(self, tbl, 2, MOVE)
        # the trap: a linear procedure on a square-root transmitter
        self.sync(self.c(4, "وَالفَخُّ"))
        self.play(FadeOut(VGroup(g1, g2, h1, h2)), FadeOut(tbl), run_time=0.4)
        pts = D.CAL_POINTS_PCT
        dots = VGroup()
        bars = VGroup()
        for p in pts:
            s = [r[2] for r in D.SQRT_TABLE if r[0] == p][0]
            ok = p in (0, 100)
            col = GOOD if ok else BAD
            dots.add(Dot(ch.p(p, s), radius=0.09, color=col))
            if not ok:
                bars.add(Line(ch.p(p, 4 + 0.16 * p), ch.p(p, s), stroke_width=5, color=BAD))
        trap = VGroup(tag("0 % and 100 %: perfect", FS_TAG + 2, GOOD),
                      tag("middle points: large, regular 'errors'", FS_TAG + 2, BAD),
                      tag("→ √ transmitter, linear procedure", FS_TAG + 2, INK, weight=BOLD)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, 0.2, 0])
        self.play(FadeIn(dots), FadeIn(trap[0]), run_time=0.6)
        self.sync(self.c(4, "وَالنِّقَاطُ الوُسْطَى"))
        self.play(Create(bars), FadeIn(trap[1]), run_time=0.8)
        self.sync(self.c(4, "المُرْسِلُ بِالجَذْرِ"))
        self.play(FadeIn(trap[2]), run_time=0.5)
        self.sync(self.c(4, "فَتَحَقَّقْ"))
        hart = VGroup(icon("search", FLUID, 0.5), tag("check the transfer function\nover HART before any trim",
                                                      FS_TAG + 2, FLUID)).arrange(RIGHT, buff=0.2)
        hart.next_to(trap, DOWN, buff=0.5).align_to(trap, LEFT)
        self.play(FadeIn(hart), run_time=0.5)
        self.sync(self.end(4) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 5: certificate, traceability, interval ----------------
    def seg5_certificate(self):
        section_title(self, "Certificate, traceability, interval", prev=self.sec)
        items = [("unique number", "رَقْمٌ"), ("transmitter identity", "وَتَعْرِيفُ"),
                 ("range, correct unit", "وَالمَدَى"), ("tolerance + its source", "وَالتَّفَاوُتُ"),
                 ("reference + cert. expiry", "وَهُوِيَّةُ"), ("environment", "وَالظُّرُوفُ"),
                 ("As-Found and As-Left", "وَآزْ فَاوْنْد"), ("uncertainty, k = 2", "وَعَدَمُ التَّأَكُّدِ"),
                 ("verdict + decision rule", "وَالحُكْمُ"), ("dates, signatures", "وَالتَّوَارِيخُ")]
        paper = Rectangle(width=5.0, height=6.2, color=INK, stroke_width=3).move_to([-4.1, -0.45, 0])
        head = tag("Certificate", FS_LABEL, weight=BOLD).next_to(paper.get_top(), DOWN, buff=0.25)
        rows = VGroup(*[tag("✓  " + t, FS_TAG + 1) for t, _ in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rows.next_to(head, DOWN, buff=0.3).align_to(paper, LEFT).shift(RIGHT * 0.3)
        self.play(Create(paper), FadeIn(head), run_time=0.5)
        for r, (_, ph) in zip(rows, items):
            self.sync(self.c(5, ph))
            self.play(FadeIn(r, shift=RIGHT * 0.1), run_time=0.35)
        # traceability chain, broken by an expired reference
        self.sync(self.c(5, "وَالمَرْجِعُ المُنْتَهِي"))
        names = ["national\nstandard", "accredited\nlab", "your\nreference", "PT-101"]
        chain = VGroup(*[VGroup(RoundedRectangle(width=1.6, height=0.9, corner_radius=0.12, color=INK, stroke_width=3),
                                tag(n, FS_TAG - 2)) for n in names]).arrange(RIGHT, buff=0.3).move_to([3.1, 2.0, 0])
        for c in chain:
            c[1].move_to(c[0])
        trace = tag("traceability", FS_TAG, GREY_INK).next_to(chain, UP, buff=0.12).align_to(chain, RIGHT)
        links = VGroup(*[Line(chain[i].get_right(), chain[i + 1].get_left(), stroke_width=4, color=GOOD)
                         for i in range(3)])
        self.play(FadeIn(chain), Create(links), FadeIn(trace), run_time=0.8)
        cal = VGroup(icon("calendar", BAD, 0.45), tag("reference certificate expired", FS_TAG, BAD)) \
            .arrange(RIGHT, buff=0.15).next_to(chain, DOWN, buff=0.3)
        self.play(links[1].animate.set_color(BAD), FadeIn(cal), run_time=0.6)
        a_, b_ = links[1].get_start(), links[1].get_end()
        m_ = (a_ + b_) / 2
        stubs = VGroup(Line(a_, m_ + LEFT * 0.08, stroke_width=4, color=BAD), Line(m_ + RIGHT * 0.08, b_, stroke_width=4, color=BAD))
        brk = cross(Dot(m_, radius=0.06), BAD, 3, pad=0.04)
        self.remove(links[1])
        self.add(stubs)
        self.play(stubs[0].animate.shift(LEFT * 0.03), stubs[1].animate.shift(RIGHT * 0.03), Create(brk),
                  links[2].animate.set_color(BAD), chain[2][0].animate.set_stroke(BAD), chain[3][0].animate.set_stroke(BAD),
                  run_time=0.5)
        void = tag("every certificate issued with it is void", FS_TAG + 2, BAD).next_to(cal, DOWN, buff=0.2)
        self.play(FadeIn(void), paper.animate.set_stroke(BAD, 6), head.animate.set_color(BAD), run_time=0.6)
        self.sync(self.c(5, "فَنَبِّهْ"))
        alert = VGroup(icon("bell", MOVE, 0.4), tag(f"alert {D.REF_ALERT_MONTHS} month before expiry", FS_TAG, MOVE)) \
            .arrange(RIGHT, buff=0.15).next_to(void, DOWN, buff=0.2)
        self.play(FadeIn(alert), run_time=0.5)
        # the interval is a decision
        self.sync(self.c(5, "وَالفَتْرَةُ"))
        self.play(FadeOut(VGroup(void, cal)), alert.animate.next_to(chain, DOWN, buff=0.3), run_time=0.4)
        yb = -0.8
        MX = lambda m: -1.2 + 7.6 * m / 12                            # noqa: E731
        base = Line([MX(0), yb, 0], [MX(12), yb, 0], stroke_width=3, color=INK)
        bl = tag("calibration interval", FS_TAG, GREY_INK).next_to(base, UP, buff=0.2).align_to(base, LEFT)
        mt = VGroup(*[VGroup(Line([MX(m), yb - 0.1, 0], [MX(m), yb + 0.1, 0], stroke_width=2, color=INK),
                             tag(f"{m} mo" if m else "0", FS_TAG - 2, GREY_INK).next_to([MX(m), yb - 0.1, 0], DOWN, buff=0.08))
                      for m in (0, 3, 6, 12)])
        cur = ValueTracker(6)
        col = {"c": MOVE}
        seg = always_redraw(lambda: Line([MX(0), yb, 0], [MX(cur.get_value()), yb, 0], stroke_width=10,
                                         color=col["c"]))
        self.play(Create(base), FadeIn(bl), FadeIn(mt), FadeIn(seg), run_time=0.5)
        crit = tag(f"critical loops: {D.INTERVAL_CRITICAL_MONTHS[0]}–"
                   f"{D.INTERVAL_CRITICAL_MONTHS[1]} months", FS_TAG).next_to(mt, DOWN, buff=0.25) \
            .align_to(base, LEFT)
        self.sync(self.c(5, "الحَلَقَاتُ الحَرِجَةُ"))
        lo_, hi_ = D.INTERVAL_CRITICAL_MONTHS
        crange = Rectangle(width=MX(hi_) - MX(lo_), height=0.12, stroke_width=0).set_fill(FLUID, 0.2) \
            .move_to([(MX(lo_) + MX(hi_)) / 2, yb, 0])
        self.play(FadeIn(crit), FadeIn(crange), cur.animate.set_value(lo_), run_time=0.7)
        self.sync(self.c(5, "وَتَارِيخُ آزْ فَاوْنْد"))
        self.play(Indicate(rows[6], color=MOVE), run_time=0.6)
        self.sync(self.c(5, "فَمَنْ يَعُودُ"))
        longer = tag(f"As-Found always within {D.EXTEND_WITHIN_PCT_OF_TOL} % of tolerance → longer",
                     FS_TAG, GOOD).next_to(crit, DOWN, buff=0.15).align_to(base, LEFT)
        col["c"] = GOOD
        self.play(FadeIn(longer), cur.animate.set_value(12), run_time=0.9)
        self.sync(self.c(5, "وَالمُقْتَرِبُ"))
        shorter = tag("near the limit → shorter", FS_TAG, BAD).next_to(longer, DOWN, buff=0.15).align_to(base, LEFT)
        col["c"] = BAD
        self.play(FadeIn(shorter), cur.animate.set_value(D.INTERVAL_CRITICAL_MONTHS[0]), run_time=0.8)
        self.sync(self.c(5, "مَعَ قَسْوَةِ"))
        also = tag("also: conditions · maker's advice · regulation", FS_TAG, GREY_INK) \
            .next_to(shorter, DOWN, buff=0.15).align_to(base, LEFT)
        self.play(FadeIn(also), run_time=0.5)
        self.sync(self.c(5, "وَالنَّتَائِجُ"))
        elec = VGroup(icon("database", FLUID, 0.45), tag("electronic transfer to CMX / LOGiCAL — not by pen",
                                                         FS_TAG, FLUID)).arrange(RIGHT, buff=0.15)
        fit(elec, 7.4).next_to(also, DOWN, buff=0.3).align_to(base, LEFT)
        self.play(FadeIn(elec), run_time=0.6)
        self.sync(self.end(5) + 1.0)


if __name__ == "__main__":
    main(__file__, "PtCalEp05", NARRATION)
