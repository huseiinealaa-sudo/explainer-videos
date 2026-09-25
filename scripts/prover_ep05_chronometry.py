"""Daniel Compact Prover series, episode 5: double chronometry, plenum pressure,
upstream/downstream volumes and CTSp.

Equations follow the Daniel manual 3-9008-701 Rev J (§2.2.2, §3.2, Table 1-2, §4.3) and
the Emerson ROC800L flow calculations manual §6.1.1 (sources in sources/prover_ep05.md).
Every number comes from scripts/prover_demo_data.py.

Build (from the repo root):
    python scripts/prover_ep05_chronometry.py --preview   # 480p15 -> tmp/prover_ep05_chronometry/preview.mp4
    python scripts/prover_ep05_chronometry.py             # 1080p30 -> output/prover_ep05_chronometry.mp4
"""
import argparse

from style import *
import prover_demo_data as D

# Fully diacritized narration (owner-approved 2026-09-25) — one entry per scene.
NARRATION = [
    # 1 intro
    "فِي هٰذِهِ الحَلْقَةِ أَرْبَعَةُ مَوْضُوعَاتٍ تَقُومُ عَلَيْهَا دِقَّةُ المُعَايِرِ: الكْرُونُومِتْرِي المُزْدَوَجُ، وَضَغْطُ البْلِينَم، وَالحَجْمَانِ أَعْلَى المَجْرَى وَأَسْفَلَهُ، وَتَصْحِيحُ سِي تِي إِسْ بِي.",
    # 2 chronometry: why
    "لَا يَحْوِي الشَّوْطُ عَدَدًا صَحِيحًا مِنَ النَّبَضَاتِ، فَالعَلَمُ يَقْطَعُ المِفْتَاحَ بَيْنَ نَبْضَتَيْنِ. فَيُخْطِئُ العَدُّ البَسِيطُ حَتَّى نَبْضَةٍ فِي كُلِّ شَوْطٍ، وَيَلْزَمُهُ عَشَرَةُ آلَافِ نَبْضَةٍ لِيَبْقَى الخَطَأُ ضِمْنَ صِفْرٍ فَاصِلَةِ صِفْرٍ وَاحِدٍ بِالمِئَةِ. أَمَّا المُعَايِرُ الصَّغِيرُ فَيَسْتَكْمِلُ كَسْرَ النَّبْضَةِ.",
    # 3 chronometry: how
    "تَعُدُّ الحَاسِبَةُ الزَّمَنَ بِجُزْءٍ مِنْ مِلْيُونٍ مِنَ الثَّانِيَةِ، بِمُؤَقِّتَيْنِ. المُؤَقِّتُ إِيهْ مِنَ المِفْتَاحِ الأَوَّلِ إِلَى الأَخِيرِ. وَالمُؤَقِّتُ بِي مِنْ أَوَّلِ نَبْضَةٍ بَعْدَ بَدْءِ إِيهْ، إِلَى أَوَّلِ نَبْضَةٍ بَعْدَ تَوَقُّفِهِ، وَفِيهِ تُعَدُّ النَّبَضَاتُ الكَامِلَةُ، سِي. فَالنَّبَضَاتُ المُسْتَكْمَلَةُ تُسَاوِي سِي فِي نِسْبَةِ إِيهْ إِلَى بِي.",
    # 4 chronometry: example
    "فِي شَوْطٍ مِنْ مِثَالِنَا، النَّبَضَاتُ الكَامِلَةُ أَرْبَعَةَ عَشَرَ أَلْفًا وَسَبْعُمِئَةٍ وَسِتٌّ وَتِسْعُونَ، وَبَيْنَ المُؤَقِّتَيْنِ نَحْوُ تِسْعٍ وَثَلَاثِينَ مِيكْرُوثَانِيَةً، فَيُضَافُ صِفْرٌ فَاصِلَةُ وَاحِدٍ سِتَّةٍ أَرْبَعَةٍ مِنْ نَبْضَةٍ.",
    # 5 plenum: formula
    "ثَانِيًا: البْلِينَم، وَيُشْحَنُ بِالنِّيتْرُوجِينِ الجَافِّ. ضَغْطُهُ يُسَاوِي ضَغْطَ الخَطِّ مَقْسُومًا عَلَى آر، زَائِدَ سِتِّينَ بِي إِسْ آي جِي. وَآر خَمْسَةٌ لِلْمَقَاسِ أَرْبَعٍ وَعِشْرِينَ بُوصَةً، وَخَمْسَةٌ فَاصِلَةُ ثَمَانِيَةٍ ثَمَانِيَةٍ قَبْلَ عَامِ أَلْفَيْنِ وَسِتَّةٍ. وَالسِّتُّونَ لِلتَّرْكِيبِ الأُفُقِيِّ، وَتَصِيرُ أَرْبَعِينَ فِي الرَّأْسِيِّ.",
    # 6 plenum: example
    "فِي مِثَالِنَا: أَرْبَعُونَ عَلَى خَمْسَةٍ، زَائِدَ سِتِّينَ، تُسَاوِي ثَمَانِيَةً وَسِتِّينَ. وَيُوصِي الدَّلِيلُ بِضَغْطٍ يَزِيدُ عَلَيْهَا حَتَّى خَمْسَةٍ بِالمِئَةِ، أَيْ إِلَى وَاحِدٍ وَسَبْعِينَ فَاصِلَةِ أَرْبَعَةٍ.",
    # 7 upstream / downstream volumes
    "ثَالِثًا: الحَجْمَانِ. حِينَ يَتَّصِلُ عَمُودٌ بِجِهَةٍ وَاحِدَةٍ مِنَ المِكْبَسِ، يَخْتَلِفُ الحَجْمَانِ، فَيُعَايَرُ كِلَاهُمَا. عَدَّادُنَا بَعْدَ المُعَايِرِ، فَنَسْتَعْمِلُ حَجْمَ أَسْفَلِ المَجْرَى: صِفْرٌ فَاصِلَةُ اثْنَيْنِ أَرْبَعَةٍ سِتَّةٍ ثَلَاثَةٍ مِتْرٍ مُكَعَّبٍ. وَحَجْمُ أَعْلَى المَجْرَى، صِفْرٌ فَاصِلَةُ اثْنَيْنِ أَرْبَعَةٍ أَرْبَعَةٍ أَرْبَعَةٍ اثْنَيْنِ، لِلْعَدَّادِ قَبْلَ المُعَايِرِ. وَالحَجْمُ الخَطَأُ يُزِيحُ المُعَامِلَ نَحْوَ ثَلَاثَةِ أَرْبَاعِ الوَاحِدِ بِالمِئَةِ.",
    # 8 CTSp: two terms
    "رَابِعًا: سِي تِي إِسْ بِي. المَفَاتِيحُ خَارِجَ الأُنْبُوبِ عَلَى قُضْبَانِ إِنْفَار، فَلِلتَّصْحِيحِ حَدَّانِ مَضْرُوبَانِ. حَدُّ الأُنْبُوبِ بِمُعَامِلٍ مِسَاحِيٍّ، ضِعْفِ الطُّولِيِّ، لِأَنَّ المَقْطَعَ يَتَّسِعُ فِي بُعْدَيْنِ. وَحَدُّ القُضْبَانِ بِحَرَارَتِهَا وَمُعَامِلِهَا الطُّولِيِّ، لِأَنَّهَا تُحَدِّدُ المَسَافَةَ بَيْنَ المِفْتَاحَيْنِ.",
    # 9 CTSp: example
    "فِي مِثَالِنَا الأُنْبُوبُ عِنْدَ ثَلَاثِينَ دَرَجَةً، فَحَدُّهُ وَاحِدٌ فَاصِلَةُ صِفْرٍ صِفْرٍ صِفْرٍ ثَلَاثَةٍ اثْنَيْنِ أَرْبَعَةٍ. وَالقُضْبَانُ عِنْدَ خَمْسَ عَشْرَةَ دَرَجَةً، فَحَدُّهَا وَاحِدٌ، وَهٰذَا لَا يَتَحَقَّقُ دَائِمًا فِي الوَاقِعِ. وَفِي الوُوتَر دْرُو يُجِيزُ الدَّلِيلُ أَخْذَ حَرَارَةِ الجَوِّ بَدَلًا مِنْ حَرَارَةِ القُضْبَانِ.",
    # 10 summary + next
    "الخُلَاصَةُ: كَسْرُ النَّبْضَةِ يُسْتَكْمَلُ، وَالبْلِينَم يَتْبَعُ ضَغْطَ الخَطِّ، وَالحَجْمُ يَتْبَعُ مَوْقِعَ العَدَّادِ، وَسِي تِي إِسْ بِي يَجْمَعُ الأُنْبُوبَ وَالقُضْبَانَ. فِي الحَلْقَةِ القَادِمَةِ: فْلُو بُوس إِسْ سِتُّمِئَةٍ بْلَس، وَجَلْسَةُ إِثْبَاتٍ نَمُوذَجِيَّةٌ.",
]

# Every spoken number is checked against prover_demo_data; stop if it drifts.
assert 100 / 10000 == 0.01                                          # seg 2 "10,000 → 0.01 %"
assert D.CHRONO_WHOLE == 14796                                      # seg 4 "14,796"
assert round((D.CHRONO_TIME_A - D.CHRONO_TIME_B) * 1e6) == 39       # seg 4 "about 39 µs"
assert f"{D.CHRONO_PULSES - D.CHRONO_WHOLE:.3f}" == "0.164"         # seg 4 "0.164 pulse"
assert (D.PLENUM_LINE_PRESSURE, D.PLENUM_RATIO, D.PLENUM_OFFSET) == (40, 5, 60)  # seg 5, 6
assert D.PLENUM_PRESSURE == 68 and f"{D.PLENUM_MAX:.1f}" == "71.4"  # seg 6 "68", "71.4"
assert D.PLENUM_TOLERANCE == 5                                      # seg 6 "up to 5 %"
assert f"{D.BPV_DOWNSTREAM:.4f}" == "0.2463"                        # seg 7 downstream
assert f"{D.BPV_UPSTREAM:.5f}" == "0.24442"                         # seg 7 upstream
assert round((1 - D.VOLUME_RATIO) * 100, 2) == 0.76                 # seg 7 "about 3/4 %"
assert D.GC_STEEL == 2 * 0.0000108                                  # seg 8 "twice the linear"
assert (D.T_PROVER, D.T_BASE, D.T_DETECTOR) == (30, 15, 15)         # seg 9
assert f"{D.CTSP_TUBE:.6f}" == "1.000324" and D.CTSP_INVAR == 1     # seg 9

AUDIO_DIR = BUILD_DIR / "prover_ep05_chronometry" / "audio"

FLUID_C = "#1f5fa8"             # same group colours as episodes 3-4
DRIVE_C = "#c25a12"
MEAS_C = "#2e7d32"
TOPICS = ["Double chronometry", "Plenum pressure", "Upstream / downstream volumes", "CTSp"]


def label(text, size=FS_LABEL, color=INK, **kw):
    return Text(text, font_size=size, color=color, **kw)


def fit(mob, width=13.2):
    """Keep a group inside the 16:9 frame with a side margin."""
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def boxed(mob, color=INK, pad=0.25, width=3):
    return VGroup(SurroundingRectangle(mob, buff=pad, color=color, stroke_width=width,
                                       corner_radius=0.1), mob)


class ProverEp05(SyncedScene):
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

        caption = VMobject()

        def say(text, color=INK, y=-3.25):
            nonlocal caption
            new = fit(label(text, FS_LABEL, color)).move_to([0, y, 0])
            if caption.has_points() or len(caption.submobjects):
                self.play(FadeOut(caption), run_time=0.25)
            self.play(FadeIn(new, shift=UP * 0.08), run_time=0.4)
            caption = new

        def clear(*keep, run_time=0.6):
            nonlocal caption
            gone = [m for m in self.mobjects if m not in keep]
            if gone:
                self.play(*[FadeOut(m) for m in gone], run_time=run_time)
            caption = VMobject()

        # ---------------- Segment 1: title ----------------
        series = label("Daniel Compact Prover  ·  Episode 5", FS_SUBTITLE, GREY_INK)
        title = Text("Four Keys to Accuracy", font_size=FS_TITLE, weight=BOLD)
        line = Line(LEFT, RIGHT).set_width(title.width)
        VGroup(series, title, line).arrange(DOWN, buff=0.35).move_to(UP * 1.7)
        items = VGroup(*[label(f"{k + 1}   {t}", FS_BODY) for k, t in enumerate(TOPICS)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(line, DOWN, 0.6)
        self.play(FadeIn(series, shift=DOWN * 0.2), Write(title), Create(line), run_time=1.8)
        for k, phrase in enumerate(["الكْرُونُومِتْرِي", "وَضَغْطُ", "وَالحَجْمَانِ", "وَتَصْحِيحُ"]):
            self.sync(cue(1, phrase))
            self.play(FadeIn(items[k], shift=RIGHT * 0.2), run_time=0.5)
        self.sync(START[1] - 0.8)
        corner = label("Ep 5 · 1  Double chronometry", FS_BODY - 6, weight=BOLD)
        corner.to_corner(UL, buff=0.4)
        self.play(FadeOut(VGroup(series, line, items)), Transform(title, corner), run_time=0.8)

        def section(text):
            new = label(text, FS_BODY - 6, weight=BOLD).to_corner(UL, buff=0.4)
            self.play(Transform(title, new), run_time=0.6)

        # ---------------- Segments 2-4: double chronometry ----------------
        # Schematic pulse train (not to scale): period P, rising edges at X0 + k P.
        P, X0, Y0, H = 1.1, -5.6, -0.9, 0.7
        D1_X, D2_X = -4.2, 3.95
        n_pulses = 12
        wave_pts = [[X0 - 0.4, Y0, 0]]
        for k in range(n_pulses):
            x = X0 + k * P
            wave_pts += [[x, Y0, 0], [x, Y0 + H, 0], [x + P / 2, Y0 + H, 0], [x + P / 2, Y0, 0]]
        wave_pts.append([X0 + n_pulses * P - 0.2, Y0, 0])
        wave = VMobject().set_points_as_corners(wave_pts).set_stroke(FLUID_C, 4)
        wave_lbl = label("meter pulses", FS_TAG, FLUID_C).move_to([-5.9, Y0 + H + 0.35, 0])
        edges = [X0 + k * P for k in range(n_pulses)]
        b_start = min(e for e in edges if e > D1_X)
        b_stop = min(e for e in edges if e > D2_X)
        whole = round((b_stop - b_start) / P)

        def switch(x, name):
            ln = DashedLine([x, Y0 - 0.5, 0], [x, 1.25, 0], stroke_width=4, color=MEAS_C)
            tag = label(name, FS_LABEL, MEAS_C, weight=BOLD).next_to(ln, UP, 0.1)
            return VGroup(ln, tag)

        sw1, sw2 = switch(D1_X, "D1"), switch(D2_X, "D2")
        note = label("schematic, not to scale", FS_TAG - 4, GREY_INK).move_to([5.3, Y0 - 0.6, 0])
        frac_l = Rectangle(width=b_start - D1_X, height=H + 0.2, stroke_width=0,
                           fill_color=DRIVE_C, fill_opacity=0.25)
        frac_l.move_to([(D1_X + b_start) / 2, Y0 + H / 2, 0])
        frac_r = Rectangle(width=b_stop - D2_X, height=H + 0.2, stroke_width=0,
                           fill_color=DRIVE_C, fill_opacity=0.25)
        frac_r.move_to([(D2_X + b_stop) / 2, Y0 + H / 2, 0])

        self.sync(START[1])
        self.play(Create(wave), FadeIn(wave_lbl), FadeIn(note), run_time=1.6)
        self.play(FadeIn(sw1), FadeIn(sw2), run_time=0.8)
        say("A pass does not hold a whole number of pulses")
        self.sync(cue(2, "فَالعَلَمُ"))
        self.play(FadeIn(frac_l), FadeIn(frac_r), run_time=0.6)
        say("The flag trips a switch between two pulses", DRIVE_C)
        self.sync(cue(2, "فَيُخْطِئُ"))
        err = VGroup(label("Simple count:  ± 1 pulse per pass", FS_LABEL, weight=BOLD),
                     label("needs ≥ 10,000 pulses  →  error ≤ 0.01 %", FS_LABEL))
        err.arrange(DOWN, buff=0.2).move_to([0, 2.15, 0])
        self.play(FadeIn(err[0]), run_time=0.5)
        self.sync(cue(2, "وَيَلْزَمُهُ"))
        self.play(FadeIn(err[1]), run_time=0.5)
        self.sync(cue(2, "أَمَّا"))
        say("Small volume prover: interpolate the fraction of a pulse", MEAS_C)

        # Segment 3: the two timers
        self.sync(START[2])
        self.play(FadeOut(err), run_time=0.4)
        clock = label("master clock: 1 µs  (0.000001 s)", FS_LABEL, weight=BOLD).move_to([0, 2.3, 0])
        self.play(FadeIn(clock), run_time=0.6)
        say("Two timers, A and B")
        self.sync(cue(3, "المُؤَقِّتُ إِيهْ"))
        a_ar = DoubleArrow([D1_X, 1.0, 0], [D2_X, 1.0, 0], buff=0, stroke_width=4, color=MEAS_C,
                           tip_length=0.2)
        a_lbl = label("Time A:  D1 → D2", FS_LABEL, MEAS_C, weight=BOLD).next_to(a_ar, UP, 0.08)
        self.play(GrowFromCenter(a_ar), FadeIn(a_lbl), run_time=0.8)
        self.sync(cue(3, "وَالمُؤَقِّتُ بِي"))
        b_y = Y0 - 0.45
        b_ar = DoubleArrow([b_start, b_y, 0], [b_stop, b_y, 0], buff=0, stroke_width=4,
                           color=FLUID_C, tip_length=0.2)
        b_lbl = label("Time B:  first pulse edge after D1 → first pulse edge after D2", FS_TAG,
                      FLUID_C, weight=BOLD).next_to(b_ar, DOWN, 0.12)
        fit(b_lbl, 12.5)
        ticks = VGroup(*[Line([e, Y0 - 0.2, 0], [e, Y0 + H + 0.2, 0], stroke_width=3, color=FLUID_C)
                         for e in (b_start, b_stop)])
        self.play(Create(ticks), GrowFromCenter(b_ar), FadeIn(b_lbl), run_time=0.8)
        self.sync(cue(3, "وَفِيهِ"))
        nums = VGroup(*[label(str(k + 1), FS_TAG, INK, weight=BOLD)
                        .move_to([b_start + (k + 0.5) * P, Y0 + H + 0.3, 0]) for k in range(whole)])
        self.play(LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.15), run_time=1.2)
        say(f"C = whole pulses in Time B  (here {whole}, schematic)", FLUID_C)
        self.sync(cue(3, "فَالنَّبَضَاتُ"))
        self.play(FadeOut(clock), run_time=0.3)
        formula = boxed(label("Interpolated pulses  =  C × A / B", FS_EQUATION, weight=BOLD))
        formula.move_to([0, 2.35, 0])
        self.play(FadeIn(formula), run_time=0.7)
        say("Accurate to 1 part in 10,000 of a pulse (manual)")

        # Segment 4: our example
        self.sync(START[3])
        clear(title, formula)
        rows = [("C", f"{D.CHRONO_WHOLE}", "whole pulses"),
                ("A", f"{D.CHRONO_TIME_A:.6f} s", "D1 → D2"),
                ("B", f"{D.CHRONO_TIME_B:.6f} s", "whole pulses"),
                ("A − B", f"≈ {(D.CHRONO_TIME_A - D.CHRONO_TIME_B) * 1e6:.0f} µs", ""),
                ("C × A / B", f"{D.CHRONO_WHOLE * D.CHRONO_TIME_A / D.CHRONO_TIME_B:.3f}",
                 "pulses")]
        table = VGroup()
        for k, (a, b, c) in enumerate(rows):
            color = MEAS_C if k == 4 else INK
            table.add(VGroup(label(a, FS_BODY, color, weight=BOLD),
                             label(b, FS_BODY, color, weight=BOLD if k == 4 else NORMAL),
                             label(c, FS_LABEL, GREY_INK)))
        for k, r in enumerate(table):
            y = 0.9 - k * 0.75
            r[0].move_to([-2.2 - r[0].width / 2, y, 0])     # right-aligned symbols
            r[1].move_to([-1.6 + r[1].width / 2, y, 0])     # left-aligned values
            r[2].move_to([2.6 + r[2].width / 2, y, 0])      # left-aligned notes
        ex = label("One illustrative pass (run 1)", FS_LABEL, GREY_INK).move_to([0, 1.5, 0])
        self.play(FadeIn(ex), FadeIn(table[0]), run_time=0.6)
        self.sync(cue(4, "وَبَيْنَ"))
        self.play(FadeIn(table[1]), FadeIn(table[2]), run_time=0.6)
        self.play(FadeIn(table[3]), run_time=0.5)
        self.sync(cue(4, "فَيُضَافُ"))
        self.play(FadeIn(table[4]), run_time=0.6)
        plus = label(f"+ {D.CHRONO_PULSES - D.CHRONO_WHOLE:.3f} pulse", FS_BODY, DRIVE_C,
                     weight=BOLD).next_to(table[4], DOWN, 0.4)
        self.play(FadeIn(plus, shift=UP * 0.1), Circumscribe(table[4][1], color=MEAS_C),
                  run_time=1.0)

        # ---------------- Segments 5-6: plenum pressure ----------------
        self.sync(START[4])
        clear(title)
        section("Ep 5 · 2  Plenum pressure")
        n2 = label("charged with dry nitrogen (N₂)", FS_LABEL, DRIVE_C).move_to([0, 2.5, 0])
        self.play(FadeIn(n2), run_time=0.5)
        self.sync(cue(5, "ضَغْطُهُ"))
        eq = VGroup(label("Plenum  =", FS_EQUATION, weight=BOLD),
                    VGroup(label("Line gauge (psig)", FS_EQUATION - 4, DRIVE_C, weight=BOLD),
                           Line(LEFT, RIGHT, stroke_width=3).set_width(4.0),
                           label("R", FS_EQUATION - 4, DRIVE_C, weight=BOLD)).arrange(DOWN, buff=0.12),
                    label("+  60 psig", FS_EQUATION, weight=BOLD)).arrange(RIGHT, buff=0.3)
        eq = boxed(fit(eq)).move_to([0, 1.1, 0])
        self.play(FadeIn(eq), run_time=0.9)
        say("Daniel manual, §3.2")
        self.sync(cue(5, "وَآر"))
        r_note = VGroup(label("R = 5  for the 24-inch prover", FS_LABEL, weight=BOLD),
                        label("(5.88 if shipped before 1 Jan 2006)", FS_LABEL - 2, GREY_INK))
        r_note.arrange(DOWN, buff=0.12).move_to([-3.3, -1.0, 0])
        self.play(FadeIn(r_note), run_time=0.6)
        self.sync(cue(5, "وَالسِّتُّونَ"))
        c_note = VGroup(label("60 psig: horizontal", FS_LABEL, weight=BOLD),
                        label("40 psig: vertical", FS_LABEL, GREY_INK))
        c_note.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.3, -1.0, 0])
        self.play(FadeIn(c_note), run_time=0.6)

        self.sync(START[5])
        self.play(FadeOut(VGroup(n2, r_note, c_note)), eq.animate.move_to([0, 2.1, 0]),
                  run_time=0.6)
        calc = label(f"{D.PLENUM_LINE_PRESSURE:.0f} / {D.PLENUM_RATIO:.0f}  +  "
                     f"{D.PLENUM_OFFSET:.0f}  =  {D.PLENUM_PRESSURE:.0f} psig",
                     FS_EQUATION + 4, DRIVE_C, weight=BOLD).move_to([0, 0.55, 0])
        self.play(Write(calc), run_time=1.4)
        say(f"Our example: line pressure {D.PLENUM_LINE_PRESSURE:.0f} psig, R = "
            f"{D.PLENUM_RATIO:.0f}", DRIVE_C)
        self.sync(cue(6, "وَيُوصِي"))
        # pressure scale 60 ... 75 psig with the recommended band
        lo, hi, x_l, x_r, y = 60.0, 75.0, -5.0, 5.0, -1.3

        def px(v):
            return x_l + (v - lo) / (hi - lo) * (x_r - x_l)

        axis = NumberLine(x_range=[lo, hi, 5], length=x_r - x_l, include_numbers=False,
                          color=INK, stroke_width=3).move_to([0, y, 0])
        ticks_l = VGroup(*[label(f"{v:.0f}", FS_TAG, GREY_INK).move_to([px(v), y - 0.4, 0])
                           for v in (60, 65, 70, 75)])
        band = Rectangle(width=px(D.PLENUM_MAX) - px(D.PLENUM_PRESSURE), height=0.45,
                         stroke_width=0, fill_color=DRIVE_C, fill_opacity=0.35)
        band.move_to([(px(D.PLENUM_MAX) + px(D.PLENUM_PRESSURE)) / 2, y, 0])
        b_lo = label(f"{D.PLENUM_PRESSURE:.0f}", FS_LABEL, DRIVE_C, weight=BOLD)
        b_lo.move_to([px(D.PLENUM_PRESSURE), y + 0.55, 0])
        b_hi = label(f"{D.PLENUM_MAX:.1f}", FS_LABEL, DRIVE_C, weight=BOLD)
        b_hi.move_to([px(D.PLENUM_MAX), y + 0.55, 0])
        unit = label("psig", FS_TAG, GREY_INK).next_to(axis, RIGHT, 0.2)
        self.play(Create(axis), FadeIn(ticks_l), FadeIn(unit), run_time=0.8)
        self.play(GrowFromEdge(band, LEFT), FadeIn(b_lo), FadeIn(b_hi), run_time=0.8)
        say(f"Recommended: 0 to +{D.PLENUM_TOLERANCE:.0f} %  →  {D.PLENUM_PRESSURE:.0f} to "
            f"{D.PLENUM_MAX:.1f} psig", DRIVE_C)

        # ---------------- Segment 7: upstream / downstream volumes ----------------
        self.sync(START[6])
        clear(title)
        section("Ep 5 · 3  Upstream / downstream volumes")
        # schematic: piston with a shaft on one side only
        tube = Rectangle(width=6.0, height=1.1, stroke_width=4, color=INK).move_to([0, 1.8, 0])
        piston = Rectangle(width=0.35, height=1.0, stroke_width=4, color=INK, fill_color=INK,
                           fill_opacity=0.15).move_to([0, 1.8, 0])
        shaft = Line([-3.8, 1.8, 0], [-0.18, 1.8, 0], stroke_width=8, color=DRIVE_C)
        sh_lbl = label("shaft on one side", FS_TAG, DRIVE_C).move_to([-4.9, 2.2, 0])
        flow = Arrow([-4.6, 0.95, 0], [4.6, 0.95, 0], buff=0, stroke_width=4, color=FLUID_C,
                     max_tip_length_to_length_ratio=0.03)
        up_t = label("Upstream", FS_LABEL, FLUID_C, weight=BOLD).move_to([-1.6, 2.65, 0])
        dn_t = label("Downstream", FS_LABEL, FLUID_C, weight=BOLD).move_to([1.6, 2.65, 0])
        self.play(Create(tube), FadeIn(piston), Create(shaft), GrowArrow(flow), run_time=1.0)
        self.play(FadeIn(sh_lbl), FadeIn(up_t), FadeIn(dn_t), run_time=0.6)
        say("A shaft on one side → the two volumes differ → both are calibrated")

        def vol_card(name, value, use, color, bold):
            txt = VGroup(label(name, FS_LABEL, color, weight=BOLD),
                         label(value, FS_BODY, color, weight=BOLD if bold else NORMAL),
                         label(use, FS_TAG, GREY_INK)).arrange(DOWN, buff=0.12)
            box = RoundedRectangle(width=5.6, height=1.6, corner_radius=0.15,
                                   stroke_width=5 if bold else 3, color=color)
            return VGroup(box, fit(txt, 5.2).move_to(box))

        dn = vol_card("Downstream volume = BPV", f"{D.BPV_DOWNSTREAM:.4f} m³",
                      "meter downstream of the prover  (our case)", MEAS_C, True)
        up = vol_card("Upstream volume", f"{D.BPV_UPSTREAM:.5f} m³",
                      "meter upstream of the prover", GREY_INK, False)
        cards = VGroup(up, dn).arrange(RIGHT, buff=0.5).move_to([0, -0.5, 0])
        self.sync(cue(7, "عَدَّادُنَا"))
        self.play(FadeIn(dn, shift=UP * 0.1), run_time=0.6)
        say("Our meter is downstream of the prover", MEAS_C)
        self.sync(cue(7, "وَحَجْمُ أَعْلَى"))
        self.play(FadeIn(up, shift=UP * 0.1), run_time=0.6)
        ratio = label(f"up / down = {D.VOLUME_RATIO}  (manual Table 1-2, 24-inch)", FS_TAG,
                      GREY_INK).next_to(cards, DOWN, 0.2)
        self.play(FadeIn(ratio), run_time=0.4)
        self.sync(cue(7, "وَالحَجْمُ الخَطَأُ"))
        say(f"Wrong volume → MF off by ≈ {(1 - D.VOLUME_RATIO) * 100:.2f} %", DRIVE_C)

        # ---------------- Segments 8-9: CTSp ----------------
        self.sync(START[7])
        clear(title)
        section("Ep 5 · 4  CTSp")
        # schematic: flow tube with the switches on external Invar rods
        tube = Rectangle(width=6.4, height=1.0, stroke_width=4, color=INK).move_to([0, 1.55, 0])
        rods = VGroup(*[Line([-3.0, 2.35 + dy, 0], [3.0, 2.35 + dy, 0], stroke_width=3,
                             color=MEAS_C) for dy in (-0.1, 0.1)])
        sws = VGroup(*[Rectangle(width=0.16, height=0.42, stroke_width=0, fill_color=INK,
                                 fill_opacity=1).move_to([x, 2.35, 0]) for x in (-2.0, 2.0)])
        sw_t = VGroup(label("D1", FS_TAG, MEAS_C, weight=BOLD).move_to([-2.0, 2.8, 0]),
                      label("D2", FS_TAG, MEAS_C, weight=BOLD).move_to([2.0, 2.8, 0]))
        rod_t = VGroup(label("Invar rods", FS_TAG, MEAS_C, weight=BOLD),
                       label("outside the tube", FS_TAG - 2, MEAS_C)).arrange(DOWN, buff=0.05)
        rod_t.next_to(rods, RIGHT, 0.3)
        tube_t = label("flow tube", FS_TAG, FLUID_C).move_to([4.2, 1.55, 0])
        self.play(Create(tube), FadeIn(tube_t), run_time=0.7)
        self.sync(cue(8, "المَفَاتِيحُ"))
        self.play(Create(rods), FadeIn(sws), FadeIn(sw_t), FadeIn(rod_t), run_time=0.8)
        say("Switches on external Invar rods → two multiplied terms", MEAS_C)
        ct_head = label("CTSp  =", FS_EQUATION, weight=BOLD)
        t1 = label("[1 + (Tp − 15) × 0.0000216]", FS_EQUATION - 6, FLUID_C, weight=BOLD)
        times = label("×", FS_EQUATION, weight=BOLD)
        t2 = label("[1 + (Td − 15) × 0.00000144]", FS_EQUATION - 6, MEAS_C, weight=BOLD)
        ct = fit(VGroup(ct_head, t1, times, t2).arrange(RIGHT, buff=0.2), 13.0).move_to([0, 0.2, 0])
        self.play(FadeIn(ct_head), FadeIn(times), FadeIn(t1), FadeIn(t2), run_time=0.8)
        self.sync(cue(8, "حَدُّ الأُنْبُوبِ"))
        n1 = VGroup(label("flow tube, temperature Tp", FS_TAG, FLUID_C, weight=BOLD),
                    label("area coefficient = 2 × 0.0000108 /°C", FS_TAG, FLUID_C),
                    label("(the cross-section grows in two dimensions)", FS_TAG - 2, GREY_INK))
        n1.arrange(DOWN, buff=0.08).next_to(t1, DOWN, 0.35)
        self.play(FadeIn(n1), Indicate(tube, color=FLUID_C), run_time=0.9)
        self.sync(cue(8, "وَحَدُّ القُضْبَانِ"))
        n2 = VGroup(label("Invar rods, temperature Td", FS_TAG, MEAS_C, weight=BOLD),
                    label("linear coefficient 0.00000144 /°C", FS_TAG, MEAS_C),
                    label("(the rods set the distance D1 → D2)", FS_TAG - 2, GREY_INK))
        n2.arrange(DOWN, buff=0.08).next_to(t2, DOWN, 0.35)
        dist = DoubleArrow([-2.0, 3.1, 0], [2.0, 3.1, 0], buff=0, stroke_width=3, color=MEAS_C,
                           tip_length=0.15)
        self.play(FadeIn(n2), GrowFromCenter(dist), run_time=0.9)
        say("Base temperature 15 °C in our example", GREY_INK)

        self.sync(START[8])
        self.play(FadeOut(VGroup(n1, n2, dist)), run_time=0.4)
        v1 = label(f"[1 + ({D.T_PROVER:.0f} − 15) × 0.0000216] = {D.CTSP_TUBE:.6f}",
                   FS_LABEL + 2, FLUID_C, weight=BOLD)
        v2 = label(f"[1 + ({D.T_DETECTOR:.0f} − 15) × 0.00000144] = {D.CTSP_INVAR:.0f}",
                   FS_LABEL + 2, MEAS_C, weight=BOLD)
        v3 = label(f"CTSp = {D.CTSP:.6f}", FS_EQUATION, weight=BOLD)
        vals = VGroup(v1, v2, v3).arrange(DOWN, buff=0.28).move_to([0, -1.25, 0])
        self.play(FadeIn(v1), run_time=0.6)
        say(f"Tube at Tp = {D.T_PROVER:.0f} °C", FLUID_C)
        self.sync(cue(9, "وَالقُضْبَانُ"))
        self.play(FadeIn(v2), run_time=0.6)
        say(f"Rods at Td = {D.T_DETECTOR:.0f} °C in our example — not always so in the field",
            MEAS_C)
        self.sync(cue(9, "وَفِي الوُوتَر"))
        self.play(FadeIn(boxed(v3, pad=0.15)), run_time=0.6)
        say("Water draw: the manual allows ambient temperature for Td", GREY_INK)

        # ---------------- Segment 10: summary + next ----------------
        self.sync(START[9])
        clear(title)
        section("Ep 5 · Summary")
        summ = VGroup(
            label("1   Double chronometry: interpolates the fraction of a pulse", FS_SUMMARY),
            label("2   Plenum = line / R + 60: follows the line pressure", FS_SUMMARY),
            label("3   Base volume: chosen by the meter position", FS_SUMMARY),
            label("4   CTSp = flow tube term × Invar rod term", FS_SUMMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        fit(summ).move_to([0, 0.5, 0])
        for k, phrase in enumerate(["كَسْرُ", "وَالبْلِينَم", "وَالحَجْمُ", "وَسِي تِي"]):
            self.sync(cue(10, phrase))
            self.play(FadeIn(summ[k], shift=RIGHT * 0.2), run_time=0.5)
        self.sync(cue(10, "فِي الحَلْقَةِ"))
        say("Next: FloBoss S600+  ·  a typical proving session", GREY_INK, y=-2.6)
        self.sync(START[10] + 2.0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="low-quality layout check")
    args = parser.parse_args()
    print(build(__file__, "ProverEp05", NARRATION, preview=args.preview))
