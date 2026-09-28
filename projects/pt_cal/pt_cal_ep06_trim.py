"""pt_cal, episode 6: trim and reading error patterns.

Every number on screen or in the narration comes from pt_cal_data. Sources: sources/pt_cal_source.md (§5)
and sources/pt_cal_ep06_trim.md; storyboard: storyboard/pt_cal_ep06_trim.md. The transmitter is generic.

Build (from the repo root):
    python projects/pt_cal/pt_cal_ep06_trim.py --preview   # 480p15 -> tmp/pt_cal_ep06_trim/preview.mp4
    python projects/pt_cal/pt_cal_ep06_trim.py             # 1080p30 -> output/pt_cal_ep06_trim.mp4
"""
from explainer import *
from pt_cal_common import *
import pt_cal_data as D

# Fully diacritized narration (owner-approved 2026-09-28) — one entry per segment.
NARRATION = [
    # 1
    "هٰذِهِ مَادَّةٌ تَعْلِيمِيَّةٌ؛ وَالمَرْجِعُ المُلْزِمُ الأَدِلَّةُ الرَّسْمِيَّةُ وَإِجْرَاءَاتُ مُنْشَأَتِكَ. عَرَفْنَا كَيْفَ نَحْكُمُ عَلَى المُرْسِلِ؛ فَإِنْ رَسَبَ، فَكَيْفَ نُصْلِحُهُ؟ أَوَّلًا، أَرْبَعُ عَمَلِيَّاتٍ لَا تُخْلَطُ: المُعَايَرَةُ مُقَارَنَةٌ لَا تُغَيِّرُ شَيْئًا. وَالضَّبْطُ تَعْدِيلٌ دَاخِلِيٌّ تَلْزَمُهُ إِعَادَةُ مُعَايَرَةٍ. وَالتَّهْيِئَةُ: الوَحْدَةُ وَالتَّخْمِيدُ وَدَالَّةُ النَّقْلِ وَاتِّجَاهُ الإِنْذَارِ. وَتَغْيِيرُ المَدَى لَا يَمَسُّ الحَسَّاسَ وَلَا يُغْنِي عَنِ الضَّبْطِ. وَالخَطَأُ المِهْنِيُّ: فَنِّيٌّ يَجِدُ اثْنَيْ عَشَرَ وَنِصْفًا عِنْدَ الخَمْسِينَ، فَيُغَيِّرُ الحَدَّ الأَعْلَى مِنْ عَشَرَةِ بَار إِلَى عَشَرَةٍ وَنِصْفٍ، وَيَكْتُبُ نَاجِحًا. عَالَجَ الحَسَّاسَ بِالمَدَى، وَأَفْسَدَ الطَّرَفَيْنِ السَّلِيمَيْنِ، وَغَيَّرَ مَعْنَى الإِشَارَةِ فِي نِظَامِ التَّحَكُّمِ دُونَ عِلْمِ أَحَدٍ، وَلَمْ يُوَثِّقْ شَيْئًا.",
    # 2
    "وَفِي المُرْسِلِ الذَّكِيِّ سِلْسِلَةٌ: الحَسَّاسُ، ثُمَّ تَحْوِيلُ القِرَاءَةِ إِلَى المَدَى، ثُمَّ مُحَوِّلُ الخَرْجِ، ثُمَّ نِظَامُ التَّحَكُّمِ. ضَبْطُ الصِّفْرِ: صِفْرٌ حَقِيقِيٌّ بِتَهْوِيَةٍ كَامِلَةٍ. وَضَبْطُ الحَسَّاسِ: ضَغْطٌ مَرْجِعِيٌّ دَقِيقٌ عِنْدَ الطَّرَفِ الأَدْنَى ثُمَّ الأَعْلَى. وَضَبْطُ الخَرْجِ: يُخْرِجُ أَرْبَعَةً ثُمَّ عِشْرِينَ، وَتُدْخِلُ مَا قِسْتَهُ، أَوْ بِوَحْدَةٍ أُخْرَى فِي الضَّبْطِ المُقَيَّسِ. وَالتَّرْتِيبُ إِلْزَامِيٌّ: الحَسَّاسُ أَوَّلًا ثُمَّ الخَرْجُ؛ فَالعَكْسُ يُصَحِّحُ خَرْجًا عَلَى قِرَاءَةٍ خَاطِئَةٍ. وَقَبْلَ الكِتَابَةِ عَبْرَ هَارْت: احْفَظِ التَّهْيِئَةَ، وَدَوِّنْ كُلَّ تَغْيِيرٍ وَسَبَبَهُ. فَعِنْدَ الأَمْرِ يَقْفِزُ الخَرْجُ، وَقَدْ يَتَحَرَّكُ صِمَامٌ؛ فَأَبْلِغْ غُرْفَةَ التَّحَكُّمِ، وَضَعِ الحَلْقَةَ عَلَى اليَدَوِيِّ، ثُمَّ أَعِدْ كُلَّ شَيْءٍ، حَتَّى حِمَايَةَ الكِتَابَةِ.",
    # 3
    "مَتَى تَضْبِطُ؟ دَاخِلَ التَّفَاوُتِ: لَا تَضْبِطْ، وَوَثِّقْ. دَاخِلَهُ قُرْبَ الحَدِّ: لَا تَضْبِطْ، وَقَصِّرِ الفَتْرَةَ. خَارِجَهُ: اضْبِطْ، ثُمَّ آزْ لِفْت كَامِلَةً. خَارِجَهُ وَالضَّبْطُ لَا يُصْلِحُهُ: اسْتَبْدِلْهُ. وَخَطَأٌ مُنْتَظِمٌ فِي النِّقَاطِ الوُسْطَى فَقَطْ: افْحَصْ دَالَّةَ النَّقْلِ أَوَّلًا.",
    # 4
    "وَاقْرَأْ نَمَطَ الأَخْطَاءِ: ثَابِتٌ فِي كُلِّ النِّقَاطِ، انْزِيَاحُ صِفْرٍ يَكْفِيهِ ضَبْطُ الصِّفْرِ. يَتَدَرَّجُ مَعَ الضَّغْطِ، خَطَأُ مَيْلٍ يَحْتَاجُ ضَبْطَ الصِّفْرِ وَالمَدَى. طَرَفَانِ سَلِيمَانِ وَوَسَطٌ مُنْحَرِفٌ، خَطِّيَّةٌ. فَرْقٌ ثَابِتٌ بَيْنَ الصُّعُودِ وَالهُبُوطِ، تَخَلُّفٌ هِسْتِيرِيٌّ لَا يُصْلِحُهُ الضَّبْطُ. وَاخْتِلَافٌ عِنْدَ تَكْرَارِ النُّقْطَةِ، ضَعْفُ تَكْرَارِيَّةٍ، أَخْطَرُهَا. مِثَالٌ: مِنْ زَائِدِ صِفْرٍ فَاصِلَةِ ثَلَاثَةٍ سَبْعَةٍ عِنْدَ الصِّفْرِ، إِلَى نَاقِصِ صِفْرٍ فَاصِلَةِ ثَلَاثَةٍ عِنْدَ المِئَةِ، عَلَى خَطٍّ مُسْتَقِيمٍ: مَيْلٌ. لٰكِنَّهُ نَاجِحٌ، فَلَا يُلْمَسُ؛ تُسَجَّلُ المُلَاحَظَةُ وَتُقَصَّرُ الفَتْرَةُ.",
]

# Every spoken or shown value is checked against the data module; stop if it drifts.
assert D.MIS_I_AT_50 == 12.5 and D.MIS_URV_OLD == 10 and D.MIS_URV_NEW == 10.5     # seg 1
assert f"{D.PATTERN_SLOPE * 100:.2f}" == "-0.68" and D.PATTERN_MAX_RESID < 0.015     # seg 4
assert D.PATTERN_E[0] == 0.37 and D.PATTERN_E[-1] == -0.30 and D.PATTERN_PASS       # seg 4

AUDIO_DIR = audio_dir_for(__file__)


class PtCalEp06(SyncedScene):
    def c(self, seg, phrase, nth=1):
        return self.cue(seg, phrase, nth)

    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        self.seg1_operations()
        self.seg2_chain()
        self.seg3_when()
        self.seg4_patterns()

    # ---------------- Segment 1: four operations; the URV mistake ----------------
    def seg1_operations(self):
        title_segment(self, "Trim and error patterns", "When to adjust a transmitter, and how", 6)
        self.sync(self.c(1, "أَوَّلًا") - 0.6)
        self.clear()
        self.sec = section_title(self, "Four operations — do not mix them")
        cards = VGroup(
            card("Calibration", "compare only:\nnothing changes", FLUID, 3.1),
            card("Trim", "internal adjustment:\nrecalibrate after it", MOVE, 3.1),
            card("Configuration", "unit, damping,\ntransfer function, alarm", INK, 3.1),
            card("Re-ranging", "LRV / URV only:\nsensor untouched", GREY_INK, 3.1),
        ).arrange(RIGHT, buff=0.2)
        fit(cards, 13.0).move_to([0, 2.15, 0])
        for k, ph in enumerate(["المُعَايَرَةُ مُقَارَنَةٌ", "وَالضَّبْطُ", "وَالتَّهْيِئَةُ", "وَتَغْيِيرُ المَدَى"]):
            self.sync(self.c(1, ph))
            self.play(FadeIn(cards[k], shift=DOWN * 0.15), run_time=0.5)
        # the URV mistake on a 0–10 bar transmitter
        ch = Chart(-6.1, -3.1, 5.6, 3.4, (0, 11), (4, 21), xticks=[(0, "0"), (5, "5"), (10, "10")],
                   yticks=[(4, "4"), (12, "12"), (20, "20")], xlabel="bar", ylabel="mA")
        ideal = ch.line([(0, 4), (10, 20)], LIGHT_INK, 3)
        before = ch.line([(0, 4), (5, D.MIS_I_AT_50), (10, 20)], MOVE, 5, smooth=True)
        pt = Dot(ch.p(5, D.MIS_I_AT_50), radius=0.09, color=BAD)
        pt_lab = tag(f"{fmt(D.MIS_I_AT_50)} mA at 50 %", FS_TAG, BAD).next_to(pt, RIGHT, buff=0.2).shift(DOWN * 0.2)
        self.sync(self.c(1, "وَالخَطَأُ المِهْنِيُّ"))
        self.play(Create(ch.group), Create(ideal), run_time=0.8)
        self.sync(self.c(1, "يَجِدُ"))
        self.play(Create(before), FadeIn(pt), FadeIn(pt_lab), run_time=1.0)
        self.sync(self.c(1, "فَيُغَيِّرُ"))
        after = ch.line([(0, 4), (5, D.MIS_I_50_AFTER), (10, D.MIS_I_100_AFTER), (D.MIS_URV_NEW, 20)], MOVE, 5,
                        smooth=True)
        urv_old = Dot(ch.p(10, 4), radius=0.08, color=INK)
        urv = tag(f"URV {fmt(D.MIS_URV_OLD, 0)} → {fmt(D.MIS_URV_NEW)} bar", FS_TAG, MOVE) \
            .next_to(ch.p(10.5, 21), UP, buff=0.15).align_to(ch.axes[0], RIGHT)
        new_pt = ch.p(5, D.MIS_I_50_AFTER)
        mid = tag(f"{fmt(D.MIS_I_50_AFTER, 2)} mA — looks fine", FS_TAG, MOVE) \
            .next_to(new_pt, RIGHT, buff=0.2).shift(DOWN * 0.25)
        end_pt = Dot(ch.p(10, D.MIS_I_100_AFTER), radius=0.09, color=BAD)
        self.play(FadeIn(urv_old), FadeIn(urv), run_time=0.4)
        self.play(Transform(before, after), pt.animate.move_to(new_pt), FadeOut(pt_lab), run_time=1.4)
        self.play(FadeIn(mid), FadeIn(end_pt), run_time=0.5)
        self.sync(self.c(1, "وَيَكْتُبُ"))
        stamp = tag("PASS", FS_BODY, GOOD, weight=BOLD).move_to(ch.p(2.2, 18.5))
        self.play(FadeIn(stamp, scale=1.3), run_time=0.5)
        self.play(Create(cross(stamp)), run_time=0.4)
        # the four faults
        dcs = device("DCS", 1.6, 1.0, FS_LABEL).move_to([1.6, 0.0, 0])
        meaning = tag(f"20 mA now = {fmt(D.MIS_URV_NEW)} bar", FS_TAG + 2, BAD).next_to(dcs, RIGHT, buff=0.3)
        faults = VGroup(*[tag("✗  " + t, FS_TAG + 2, BAD) for t in [
            "sensor error 'fixed' with the range",
            f"good ends spoiled: {fmt(D.MIS_I_100_AFTER, 2)} mA at {fmt(D.MIS_URV_OLD, 0)} bar",
            "signal meaning changed, nobody told",
            "no As-Found, no As-Left"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        faults.move_to([3.4, -2.2, 0]).align_to([0.3, 0, 0], LEFT)
        for k, ph in enumerate(["عَالَجَ", "وَأَفْسَدَ", "وَغَيَّرَ مَعْنَى", "وَلَمْ يُوَثِّقْ"]):
            self.sync(self.c(1, ph))
            anims = [FadeIn(faults[k], shift=RIGHT * 0.15)]
            if k == 1:
                anims.append(Indicate(end_pt, color=BAD, scale_factor=1.8))
            if k == 2:
                anims += [FadeIn(dcs), FadeIn(meaning)]
            self.play(*anims, run_time=0.6)
        self.sync(self.end(1) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 2: the chain inside a smart transmitter ----------------
    def seg2_chain(self):
        section_title(self, "Smart transmitter: where each trim acts", prev=self.sec)
        steps = ["Sensor", "PV → % of range\n(LRV / URV)", "D/A output\n4–20 mA", "DCS"]
        cues = [self.c(2, "الحَسَّاسُ"), self.c(2, "ثُمَّ تَحْوِيلُ"), self.c(2, "ثُمَّ مُحَوِّلُ"),
                self.c(2, "ثُمَّ نِظَامُ")]
        flow_ = process_flow(self, steps, cues=cues, size=FS_TAG + 4, width=12.4, pos=[0, 2.1, 0])
        boxes, arrows = flow_[0], flow_[1]

        def trim_tag(text, box, y, color=MOVE):
            t = VGroup(icon("tool", color, 0.4), tag(text, FS_TAG, color)).arrange(RIGHT, buff=0.12)
            t.move_to([box.get_center()[0], y, 0])
            if t.get_left()[0] < -6.75:
                t.shift(RIGHT * (-6.75 - t.get_left()[0]))
            return t

        z = trim_tag("Zero trim:\nfully vented, true zero", boxes[0], 0.75)
        s = trim_tag("Sensor trim:\nreference low, then high", boxes[0], -0.35)
        d = trim_tag("D/A trim: outputs 4, then 20 mA;\nenter what you measure", boxes[2], 0.7)
        sc = tag("scaled D/A trim: same, in another unit", FS_TAG, GREY_INK).next_to(d, DOWN, buff=0.15) \
            .align_to(d, LEFT)
        l1 = Line(boxes[0].get_bottom(), z.get_top(), stroke_width=2, color=MOVE)
        l2 = Line(boxes[2].get_bottom(), d.get_top(), stroke_width=2, color=MOVE)
        self.sync(self.c(2, "ضَبْطُ الصِّفْرِ"))
        self.play(Create(l1), FadeIn(z), Indicate(boxes[0], color=MOVE), run_time=0.7)
        self.sync(self.c(2, "وَضَبْطُ الحَسَّاسِ"))
        self.play(FadeIn(s), run_time=0.5)
        self.sync(self.c(2, "وَضَبْطُ الخَرْجِ"))
        self.play(Create(l2), FadeIn(d), Indicate(boxes[2], color=MOVE), run_time=0.7)
        self.sync(self.c(2, "المُقَيَّسِ"))
        self.play(FadeIn(sc), run_time=0.4)
        # the order: sensor first, then output; a change ripples to the right
        self.sync(self.c(2, "وَالتَّرْتِيبُ"))
        b1 = badge(1, MOVE).next_to(VGroup(z, s), RIGHT, buff=0.2)
        b2 = badge(2, MOVE).next_to(d, RIGHT, buff=0.2)
        self.play(FadeIn(b1), FadeIn(b2), run_time=0.4)
        self.play(*[flow(a, MOVE, 8) for a in arrows], run_time=1.2)
        # wrong order: the output tuned on a reading that is still wrong
        self.sync(self.c(2, "فَالعَكْسُ"))
        ch = Chart(-6.2, -3.2, 3.2, 2.0, (0, 100), (4, 20))
        ideal = ch.line([(0, 4), (100, 20)], LIGHT_INK, 2)
        wrong = ch.line([(0, 4), (50, 13.4), (100, 20)], BAD, 4, smooth=True)
        ends = ch.dots([(0, 4), (100, 20)], GOOD)
        wl = tag("D/A trimmed first:\nends match, the middle\nstill carries the sensor error", FS_TAG, BAD) \
            .next_to(ch.axes, RIGHT, buff=0.35)
        self.play(Create(ch.axes), Create(ideal), run_time=0.4)
        self.play(Create(wrong), FadeIn(ends), FadeIn(wl), run_time=1.0)
        # HART writes on a transmitter in service
        self.sync(self.c(2, "وَقَبْلَ الكِتَابَةِ") - 0.3)
        self.play(FadeOut(VGroup(ch.axes, ideal, wrong, ends, wl)), run_time=0.3)
        save = VGroup(icon("database", INK, 0.5),
                      tag("save the configuration;\nlog each change: before, after, why", FS_TAG)) \
            .arrange(RIGHT, buff=0.2).move_to([-3.9, -1.2, 0])
        self.play(FadeIn(save), run_time=0.5)
        self.sync(self.c(2, "يَقْفِزُ"))
        tr = Chart(-6.3, -3.3, 2.6, 1.3, (0, 10), (0, 10))
        trace = tr.line([(0, 3), (4, 3), (4.05, 8), (10, 8)], MOVE, 4)
        tl = tag("output jumps", FS_TAG, MOVE).next_to(tr.axes, UP, buff=0.12).align_to(tr.axes, LEFT)
        valve = control_valve(size=0.9).move_to([-2.2, -2.6, 0])
        vl = tag("a valve may move", FS_TAG, BAD).next_to(valve, RIGHT, buff=0.25)
        self.play(Create(tr.axes), FadeIn(tl), run_time=0.3)
        self.play(Create(trace), FadeIn(valve), run_time=0.5)
        self.play(valve.animate.set_color(BAD).shift(UP * 0.12), FadeIn(vl), run_time=0.4)
        self.sync(self.c(2, "فَأَبْلِغْ") - 1.0)
        checklist(self, ["inform the control room", "loop to MANUAL", "afterwards: restore all,\nwrite protect ON"],
                  cues=[self.c(2, "فَأَبْلِغْ"), self.c(2, "وَضَعِ"), self.c(2, "ثُمَّ أَعِدْ")],
                  pos=[3.9, -2.1, 0], size=FS_TAG + 2)
        self.sync(self.end(2) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 3: when to trim ----------------
    def seg3_when(self):
        section_title(self, "When to trim", prev=self.sec)
        root = card("As-Found", "result against\nthe tolerance", INK, 2.6).move_to([-5.2, 0.0, 0])
        outs = [("within tolerance → do not trim · document", GOOD, "دَاخِلَ التَّفَاوُتِ"),
                ("within, near the limit → do not trim · shorten the interval", MOVE, "دَاخِلَهُ قُرْبَ"),
                ("out of tolerance → trim, then a full As-Left", MOVE, "خَارِجَهُ: اضْبِطْ"),
                ("out, and trim cannot fix it → replace", BAD, "خَارِجَهُ وَالضَّبْطُ"),
                ("regular error at mid-points only → check the transfer function", FLUID, "وَخَطَأٌ")]
        items = VGroup()
        for k, (t, col, _) in enumerate(outs):
            txt = tag(t, FS_TAG + 2, col)
            fr = RoundedRectangle(width=8.4, height=0.72, corner_radius=0.12, color=col, stroke_width=3)
            fit(txt, 7.9)
            items.add(VGroup(fr, txt.move_to(fr)))
        items.arrange(DOWN, buff=0.28).move_to([2.35, -0.1, 0])
        links = VGroup(*[Line(root.frame.get_right(), it[0].get_left(), stroke_width=3, color=LIGHT_INK)
                         for it in items])
        self.play(FadeIn(root), run_time=0.5)
        for it, ln, (t, col, ph) in zip(items, links, outs):
            self.sync(self.c(3, ph))
            self.play(Create(ln), FadeIn(it, shift=RIGHT * 0.15), run_time=0.5)
            self.play(ln.animate.set_color(col), run_time=0.2)
        self.sync(self.end(3) - 0.5)
        self.clear(self.sec, run_time=0.5)

    # ---------------- Segment 4: error patterns; the worked example ----------------
    def seg4_patterns(self):
        section_title(self, "Reading the error pattern", prev=self.sec)
        P = D.PATTERN_SHAPES
        xs = D.PATTERN_X
        specs = [("Offset", "zero trim", P["offset"], "ثَابِتٌ"),
                 ("Slope", "zero + span trim", P["slope"], "يَتَدَرَّجُ"),
                 ("Linearity", "multi-point trim,\nelse replace", P["linearity"], "طَرَفَانِ"),
                 ("Hysteresis", "trim cannot fix:\nwatch it", None, "فَرْقٌ ثَابِتٌ"),
                 ("Repeatability", "worst: candidate\nfor replacement", None, "وَاخْتِلَافٌ")]
        w, gap, y0 = 2.3, 0.3, 0.75
        x = -6.6
        for name, fix, ys, ph in specs:
            ch = Chart(x, y0, w, 1.8, (0, 100), (-0.45, 0.45))
            zero = ch.hline(0, LIGHT_INK)
            frame = Rectangle(width=w, height=1.8, color=GREY_INK, stroke_width=2).move_to(
                [x + w / 2, y0 + 0.9, 0])
            if name == "Hysteresis":
                pts = VGroup(ch.line(list(zip(xs, P["hysteresis_up"])), FLUID, 3),
                             ch.line(list(zip(xs, P["hysteresis_down"])), MOVE, 3),
                             ch.dots(list(zip(xs, P["hysteresis_up"])), FLUID),
                             ch.dots(list(zip(xs, P["hysteresis_down"])), MOVE))
            elif name == "Repeatability":
                pts = VGroup(*[ch.dots([(xx, v) for v in vs], BAD, 0.055) for xx, vs in zip(xs, P["repeatability"])])
            else:
                pts = VGroup(ch.line(list(zip(xs, ys)), MOVE, 3), ch.dots(list(zip(xs, ys)), MOVE))
            nm = tag(name, FS_TAG + 2, weight=BOLD).next_to(frame, DOWN, buff=0.15)
            fx = tag(fix, FS_TAG, GREY_INK, line_spacing=1.1).next_to(nm, DOWN, buff=0.1)
            self.sync(self.c(4, ph))
            self.play(Create(frame), Create(zero), FadeIn(nm), run_time=0.4)
            self.play(Create(pts), FadeIn(fx), run_time=0.8)
            x += w + gap
        # the worked example: +0.37 … −0.30 on a straight line
        self.sync(self.c(4, "مِثَالٌ"))
        ex = Chart(-5.9, -3.35, 6.2, 1.85, (0, 100), (-0.6, 0.6), xticks=[(0, "0"), (50, "50"), (100, "100 %")],
                   yticks=[(-0.5, "−0.5"), (0, "0"), (0.5, "+0.5")])
        band = ex.band(-D.TOL_PCT, D.TOL_PCT, GOOD, 0.1)
        zero = ex.hline(0, LIGHT_INK)
        dots = ex.dots(list(zip(D.PATTERN_X, D.PATTERN_E)), MOVE, 0.08)
        vals = VGroup(*[tag(sfmt(e), FS_TAG, MOVE).move_to([ex.p(x_, 0)[0], -1.2, 0])
                        for x_, e in zip(D.PATTERN_X, D.PATTERN_E)])
        self.play(FadeIn(band), Create(ex.axes), FadeIn(ex.ticks), Create(zero), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(dt, scale=1.5) for dt in dots], lag_ratio=0.25), FadeIn(vals), run_time=1.2)
        self.sync(self.c(4, "عَلَى خَطٍّ"))
        fitl = ex.line([(0, D.PATTERN_INTERCEPT), (100, D.PATTERN_INTERCEPT + D.PATTERN_SLOPE * 100)], MOVE, 3)
        info = VGroup(tag(f"errors in % of span; slope {fmt(D.PATTERN_SLOPE * 100, 2)} % over the span", FS_TAG + 1),
                      tag(f"residuals ≤ {fmt(D.PATTERN_MAX_RESID, 3)} %: a straight line", FS_TAG + 1)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, -1.6, 0]).align_to([0.8, 0, 0], LEFT)
        self.play(Create(fitl), FadeIn(info[0]), run_time=0.9)
        self.play(FadeIn(info[1]), run_time=0.4)
        self.sync(self.c(4, "لٰكِنَّهُ نَاجِحٌ"))
        verdict = VGroup(tag("PASS: do not touch", FS_LABEL, GOOD, weight=BOLD),
                         tag("note it · shorten the interval", FS_TAG + 2, GOOD)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(info, DOWN, buff=0.35).align_to(info, LEFT)
        self.play(FadeIn(verdict[0]), Indicate(band, color=GOOD), run_time=0.7)
        self.sync(self.c(4, "تُسَجَّلُ"))
        self.play(FadeIn(verdict[1]), run_time=0.5)
        self.sync(self.end(4) + 1.0)


if __name__ == "__main__":
    main(__file__, "PtCalEp06", NARRATION)
