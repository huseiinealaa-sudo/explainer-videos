"""pt_cal, episode 3: transmitter types, connections, the 3-valve manifold, safety.

Every number on screen or in the narration comes from pt_cal_data. Sources: sources/pt_cal_source.md (§3)
and sources/pt_cal_ep03_setup.md (manifold sequence: Rosemount 3051 Reference Manual p53–54, owner-approved
correction). Storyboard: storyboard/pt_cal_ep03_setup.md. The transmitter is generic (no brand).

Build (from the repo root):
    python projects/pt_cal/pt_cal_ep03_setup.py --preview   # 480p15 -> tmp/pt_cal_ep03_setup/preview.mp4
    python projects/pt_cal/pt_cal_ep03_setup.py             # 1080p30 -> output/pt_cal_ep03_setup.mp4
"""
from explainer import *
from pt_cal_common import *
import pt_cal_data as D

# Fully diacritized narration (owner-approved 2026-09-28) — one entry per segment.
NARRATION = [
    # 1
    "هٰذِهِ مَادَّةٌ تَعْلِيمِيَّةٌ؛ وَالمَرْجِعُ المُلْزِمُ الأَدِلَّةُ الرَّسْمِيَّةُ وَإِجْرَاءَاتُ مُنْشَأَتِكَ. قَبْلَ التَّوْصِيلِ اعْرِفْ نَوْعَ المُرْسِلِ. النِّسْبِيُّ مَرْجِعُهُ الضَّغْطُ الجَوِّيُّ، فَيُصَفَّرُ وَمَنْفَذُهُ مَفْتُوحٌ لِلْجَوِّ، وَلَا تُعَايِرْهُ فِي رِيحٍ عَاصِفَةٍ. وَالمُطْلَقُ مَرْجِعُهُ الفَرَاغُ، فَلَا يُصَفَّرُ بِفَتْحِهِ لِلْجَوِّ، وَيَحْتَاجُ وَحْدَةً بَارُومِتْرِيَّةً أَوْ مَرْجِعًا مُطْلَقًا. وَالتَّفَاضُلِيُّ يَقِيسُ الفَرْقَ بَيْنَ مَنْفَذَيْنِ: عَالٍ وَمُنْخَفِضٍ، وَهُوَ الأَخْطَرُ مِيكَانِيكِيًّا. وَالنِّسْبِيُّ المَخْتُومُ كَالنِّسْبِيِّ، لٰكِنَّ لَهُ انْزِيَاحَ صِفْرٍ ثَابِتًا لَا يُلْغِيهِ فَتْحُهُ لِلْجَوِّ.",
    # 2
    "وَإِذَا كَانَ المُرْسِلُ التَّفَاضُلِيُّ عَلَى لَوْحِ عِيَارٍ، وَاسْتِخْرَاجُ الجَذْرِ التَّرْبِيعِيِّ مُفَعَّلٌ دَاخِلَهُ، فَنِصْفُ الضَّغْطِ التَّفَاضُلِيِّ لَا يُقَابِلُ اثْنَيْ عَشَرَ مِلِّي أَمْبِير، بَلْ نَحْوَ خَمْسَةَ عَشَرَ فَاصِلَةَ ثَلَاثَةٍ وَاحِدٍ أَرْبَعَةٍ.",
    # 3
    "وَلِلتَّوْصِيلِ الكَهْرَبَائِيِّ ثَلَاثُ حَالَاتٍ. الأُولَى، الوَرْشَةُ: المُعَايِرُ يُغَذِّي المُرْسِلَ بِأَرْبَعَةٍ وَعِشْرِينَ فُولْت وَيَقِيسُ تَيَّارَهُ، وَهَارْت مُتَاحٌ مُبَاشَرَةً. الثَّانِيَةُ، الحَلْقَةُ الحَيَّةُ: نِظَامُ التَّحَكُّمِ يُغَذِّي، وَالمُعَايِرُ يَقِيسُ فَقَطْ، وَالتَّحَكُّمُ فَعَّالٌ. الثَّالِثَةُ: القِيَاسُ عَلَى تَوَازِي دَايُودِ الِاخْتِبَارِ فِي المُرْسِلِ، دُونَ قَطْعِ الحَلْقَةِ؛ لٰكِنَّ تَسَرُّبَ الدَّايُودِ يَزْدَادُ فِي الحَرَارَةِ فَتَتَأَثَّرُ الدِّقَّةُ. وَهَارْت يَحْتَاجُ مُقَاوَمَةَ حَلْقَةٍ لَا تَقِلُّ عَنْ مِئَتَيْنِ وَخَمْسِينَ أُومًا؛ وَفِي حَلْقَةِ المَصْنَعِ قَدْ تَكُونُ مَوْجُودَةً فَلَا تُضِفْ ثَانِيَةً، وَالمُودِمُ عَلَى التَّوَازِي لَا عَلَى التَّوَالِي.",
    # 4
    "وَالتَّفَاضُلِيُّ يُرَكَّبُ عَلَى مَشْعَبٍ ثُلَاثِيٍّ: صِمَامُ عَزْلٍ لِلْعَالِي، وَصِمَامُ عَزْلٍ لِلْمُنْخَفِضِ، وَصِمَامُ مُعَادَلَةٍ بَيْنَهُمَا. غِشَاؤُهُ مُصَمَّمٌ لِفَرْقٍ صَغِيرٍ، وَضَغْطُ الخَطِّ قَدْ يَبْلُغُ أَرْبَعِينَ بَار. فَالخَطَرُ أَنْ يُنَفَّسَ جَانِبٌ وَالآخَرُ تَحْتَ ضَغْطِ الخَطِّ: يَقَعُ الضَّغْطُ كُلُّهُ فَرْقًا عَلَى الغِشَاءِ، فَيَتَمَدَّدُ نِهَائِيًّا. وَالتَّسَلْسُلُ فِي الدَّلِيلِ المَرْجِعِيِّ: أَغْلِقْ عَزْلَ المُنْخَفِضِ، ثُمَّ افْتَحِ المُعَادَلَةَ، ثُمَّ أَغْلِقْ عَزْلَ العَالِي، ثُمَّ افْتَحِ التَّنْفِيسَ بِحَذَرٍ بَعِيدًا عَنْ وَجْهِكَ، وَتَحَقَّقْ مِنْ صِفْرِ الضَّغْطِ.",
    # 5
    "وَلِلْإِعَادَةِ: أَغْلِقِ التَّنْفِيسَ، وَالمُعَادَلَةُ مَفْتُوحَةٌ، وَافْتَحْ عَزْلَ العَالِي بِبُطْءٍ، فَيَرْتَفِعُ الجَانِبَانِ مَعًا. ثُمَّ أَغْلِقِ المُعَادَلَةَ، ثُمَّ افْتَحْ عَزْلَ المُنْخَفِضِ، وَافْحَصِ التَّسْرِيبَ، وَرَاقِبِ القِرَاءَةَ مَعَ غُرْفَةِ التَّحَكُّمِ. وَالخَطَأُ المُتَأَخِّرُ نِسْيَانُ المُعَادَلَةِ مَفْتُوحَةً: يَقْرَأُ المُرْسِلُ صِفْرًا مَهْمَا تَغَيَّرَ الجَرَيَانُ، وَقَدْ لَا يَنْتَبِهُ أَحَدٌ أَيَّامًا.",
    # 6
    "وَقَبْلَ البَدْءِ: تَصْرِيحُ عَمَلٍ سَارٍ يُحَدِّدُ المُعِدَّةَ وَالنِّطَاقَ وَالمُدَّةَ، وَفَحْصُ غَازَاتٍ قَبْلَ العَمَلِ وَأَثْنَاءَهُ، وَمُعِدَّاتُ وِقَايَةٍ وَكَاشِفُ غَازٍ شَخْصِيٌّ، وَمَعْرِفَةُ المَخَارِجِ وَنُقْطَةِ التَّجَمُّعِ وَمَحَطَّةِ غَسْلِ العُيُونِ، وَلَا عَمَلَ مُنْفَرِدًا فِي مِنْطَقَةٍ مُصَنَّفَةٍ أَوْ مَكَانٍ مُغْلَقٍ. وَكِبْرِيتِيدُ الهِيدْرُوجِينِ أَثْقَلُ مِنَ الهَوَاءِ، يَتَجَمَّعُ فِي المُنْخَفَضَاتِ؛ وَيَشُلُّ حَاسَّةَ الشَّمِّ فِي التَّرَاكِيزِ العَالِيَةِ، فَغِيَابُ رَائِحَتِهِ لَيْسَ أَمَانًا. وَالمَشْعَبُ المَفْتُوحُ يُطْلِقُهُ فِي وَجْهِكَ: صَرِّفْ إِلَى نِظَامٍ مُغْلَقٍ حَيْثُ أَمْكَنَ، وَقِفْ وَالرِّيحُ خَلْفَكَ.",
    # 7
    "وَالمَنَاطِقُ الخَطِرَةُ ثَلَاثٌ: صِفْر، خَلِيطٌ قَابِلٌ لِلِاشْتِعَالِ بِاسْتِمْرَارٍ؛ وَوَاحِد، مُحْتَمَلٌ فِي التَّشْغِيلِ الطَّبِيعِيِّ؛ وَاثْنَان، غَيْرُ مُتَوَقَّعٍ، وَإِنْ حَدَثَ فَقَصِيرٌ. وَالهَاتِفُ وَالكَامِيرَا تَحْتَ القَيْدِ نَفْسِهِ. وَلِعَزْلِ العَمَلِيَّةِ: اعْرِفْ وَسَطَهَا مِنْ وَرَقَةِ بَيَانَاتِ السَّلَامَةِ، وَاعْزِلْ عَزْلًا مُزْدَوِجًا مَعَ تَنْفِيسٍ، فَصِمَامٌ وَاحِدٌ لَيْسَ عَزْلًا، وَضَعْ قُفْلًا وَبِطَاقَةً بِاسْمِكَ، وَافْتَرِضْ ضَغْطًا مَحْبُوسًا حَتَّى يَثْبُتَ العَكْسُ. وَلِعَزْلِ الحَلْقَةِ: أَبْلِغْ غُرْفَةَ التَّحَكُّمِ، وَضَعِ الحَلْقَةَ عَلَى اليَدَوِيِّ، وَتَجَاوَزِ الإِنْذَارَاتِ بِإِجْرَاءٍ مُعْتَمَدٍ؛ وَمُرْسِلُ نِظَامِ السَّلَامَةِ الآلِيِّ يُتَجَاوَزُ بِإِجْرَاءٍ خَاصٍّ وَسُلْطَةٍ أَعْلَى.",
    # 8
    "وَأَثْنَاءَ المُعَايَرَةِ: لَا تَتَجَاوَزْ مَدَى وَحْدَةِ الضَّغْطِ، وَقِفْ جَانِبًا لَا أَمَامَ الوَصَلَاتِ، وَثَبِّتِ الخُرْطُومَ حَتَّى لَا يَسُوطَ أَحَدًا، وَنَفِّسْ بِبُطْءٍ دَائِمًا. وَنَفَّاثُ السَّائِلِ الدَّقِيقُ يَخْتَرِقُ الجِلْدَ بِإِصَابَةٍ بَالِغَةٍ قَدْ لَا تَظْهَرُ، فَلَا تَفْحَصِ التَّسْرِيبَ بِيَدِكَ. وَاحْذَرِ الضَّغْطَ المَحْبُوسَ بَيْنَ صِمَامَيْنِ مُغْلَقَيْنِ.",
]

# Every spoken or shown value is checked against the data module; stop if it drifts.
assert f"{D.DP_50_SQRT_MA:.3f}" == "15.314" and D.DP_50_LINEAR_MA == 12                  # seg 2
assert D.MC6_LOOP_V == 24 and D.MC6_HART_R_EXT == 250                                    # seg 3
assert D.LINE_PRESSURE_BAR == 40                                                         # seg 4

AUDIO_DIR = audio_dir_for(__file__)


def cell_drawing(kind, w=2.6, h=1.7):
    """A pressure cell: process chamber (left), diaphragm, reference chamber (right)."""
    box = Rectangle(width=w, height=h, color=INK, stroke_width=4).set_fill(WHITE, 1)
    bow = ValueTracker(0.0)
    cx = box.get_center()[0]
    dia = always_redraw(lambda: VMobject(color=MOVE, stroke_width=5).set_points_smoothly(
        [box.get_top() + DOWN * 0.02, box.get_center() + RIGHT * bow.get_value(),
         box.get_bottom() + UP * 0.02]))
    port = Line(box.get_left(), box.get_left() + LEFT * 0.45, stroke_width=8, color=INK)
    g = VGroup(box, port)
    if kind == "gauge":
        vent = Line(box.get_right(), box.get_right() + RIGHT * 0.35, stroke_width=4, color=INK)
        g.add(vent)
    if kind == "dp":
        lp = Line(box.get_right(), box.get_right() + RIGHT * 0.45, stroke_width=8, color=INK)
        g.add(lp)
    g.bow, g.dia, g.box = bow, dia, box
    return g


class Manifold:
    """3-valve manifold on a DP cell. States (1 open / 0 closed) in ValueTrackers; the pressure on each
    side of the diaphragm follows from them (line pressure on both process lines)."""

    def __init__(self, ox=-2.8):
        self.ox = ox
        self.hp, self.lp, self.eq, self.vent = (ValueTracker(v) for v in (1, 1, 0, 0))
        self.xh, self.xl = ox - 1.4, ox + 1.4
        self.cell = Rectangle(width=3.6, height=1.5, color=INK, stroke_width=4).set_fill(WHITE, 1) \
            .move_to([ox, -1.3, 0])
        self.lines = VGroup(
            pipe([self.xh, 2.7, 0], [self.xh, -0.55, 0], width=6),
            pipe([self.xl, 2.7, 0], [self.xl, -0.55, 0], width=6),
            pipe([self.xh, 0.4, 0], [self.xl, 0.4, 0], width=4),
            pipe([self.xl - 0.4, -2.05, 0], [self.xl - 0.4, -2.6, 0], width=4))
        self.process = VGroup(tag("process HP", FS_TAG, FLUID).next_to([self.xh, 2.7, 0], UP, buff=0.1),
                              tag("process LP", FS_TAG, FLUID).next_to([self.xl, 2.7, 0], UP, buff=0.1))
        self.valves = always_redraw(self._valves)
        self.fill = always_redraw(self._fill)
        self.dia = always_redraw(self._dia)
        self.names = VGroup(tag("HP isolate", FS_TAG).next_to([self.xh - 0.3, 1.6, 0], LEFT, buff=0.1),
                            tag("LP isolate", FS_TAG).next_to([self.xl + 0.3, 1.6, 0], RIGHT, buff=0.1),
                            tag("equalize", FS_TAG).next_to([self.ox, 0.4 + 0.3, 0], UP, buff=0.05),
                            tag("vent", FS_TAG).next_to([self.xl - 0.4 + 0.3, -2.45, 0], RIGHT, buff=0.1))
        self.readout = always_redraw(self._readout)

    def pressures(self):
        P = D.LINE_PRESSURE_BAR
        h = P if self.hp.get_value() > 0.5 else None
        l = P if self.lp.get_value() > 0.5 else None
        eq = self.eq.get_value() > 0.5
        vent = self.vent.get_value() > 0.5
        if eq:
            joined = h if h is not None else l
            h = l = joined
        if vent:
            l = 0.0
            if eq:
                h = 0.0
        return (h if h is not None else self._last.get("h", P), l if l is not None else self._last.get("l", P))

    _last = {}

    def _valves(self):
        def v(x, y, t, rot):
            s = gate_valve(size=0.5).rotate(rot).move_to([x, y, 0])
            on = t.get_value() > 0.5
            s.set_color(GOOD if on else INK)
            if not on:
                for m in s.family_members_with_points():
                    m.set_fill(INK, 1)
            return s
        return VGroup(v(self.xh, 1.6, self.hp, PI / 2), v(self.xl, 1.6, self.lp, PI / 2),
                      v(self.ox, 0.4, self.eq, 0), v(self.xl - 0.4, -2.35, self.vent, PI / 2))

    def _fill(self):
        h, l = self.pressures()
        Manifold._last = {"h": h, "l": l}
        c = lambda p: FLUID if p > 0.5 else WHITE          # noqa: E731
        return VGroup(Rectangle(width=1.7, height=1.4, stroke_width=0).set_fill(c(h), 0.25)
                      .move_to(self.cell.get_center() + LEFT * 0.9),
                      Rectangle(width=1.7, height=1.4, stroke_width=0).set_fill(c(l), 0.25)
                      .move_to(self.cell.get_center() + RIGHT * 0.9))

    def _dia(self):
        h, l = self.pressures()
        bow = 0.65 * (h - l) / D.LINE_PRESSURE_BAR
        col = BAD if abs(h - l) > 1 else MOVE
        c = self.cell.get_center()
        return VMobject(color=col, stroke_width=6).set_points_smoothly(
            [c + UP * 0.72, c + RIGHT * bow, c + DOWN * 0.72])

    def _readout(self):
        h, l = self.pressures()
        return VGroup(tag(f"HP side {fmt(h, 0)} bar", FS_TAG, FLUID if h else GREY_INK),
                      tag(f"LP side {fmt(l, 0)} bar", FS_TAG, FLUID if l else GREY_INK)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(self.cell, DOWN, buff=0.3).align_to(self.cell, LEFT)

    def static(self):
        return VGroup(self.lines, self.cell, self.process, self.names)

    def moving(self):
        return VGroup(self.fill, self.dia, self.valves, self.readout)


class PtCalEp03(SyncedScene):
    def c(self, seg, phrase, nth=1):
        return self.cue(seg, phrase, nth)

    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        self.seg1_types()
        self.seg2_dp_sqrt()
        self.seg3_connections()
        self.seg4_isolate()
        self.seg5_return()
        self.seg6_safety()
        self.seg7_zones()
        self.seg8_pressure()

    # ---------------- Segment 1: four transmitter types ----------------
    def seg1_types(self):
        title_segment(self, "Preparation, connection, safety", "Know the transmitter before you connect it", 3)
        self.sync(self.c(1, "قَبْلَ التَّوْصِيلِ") - 0.6)
        self.clear()
        self.sec = section_title(self, "Four transmitter types: what is the reference?")
        kinds = [("Gauge\nref: atmosphere", "gauge", "النِّسْبِيُّ مَرْجِعُهُ"),
                 ("Absolute\nref: vacuum", "absolute", "وَالمُطْلَقُ"),
                 ("Differential\nHP − LP", "dp", "وَالتَّفَاضُلِيُّ"),
                 ("Sealed gauge\nref: sealed", "sealed", "وَالنِّسْبِيُّ المَخْتُومُ")]
        cells = VGroup(*[cell_drawing(k, 2.0, 1.5) for _, k, _ in kinds]).arrange(RIGHT, buff=0.8)
        cells.move_to([0.0, 0.7, 0])
        names = VGroup(*[tag(n, FS_TAG + 1, weight=BOLD).next_to(c.box, UP, buff=0.25) for (n, _, _), c in zip(kinds, cells)])
        notes = [tag("vented: reads 0\navoid gusty wind", FS_TAG - 1),
                 tag("vented: reads\natmospheric\n→ BARO or\nabsolute ref.", FS_TAG - 1),
                 tag("most fragile", FS_TAG - 1, BAD),
                 tag("fixed zero offset\nthat venting\ndoes not remove", FS_TAG - 1)]
        refs = VGroup(*[tag(r, FS_TAG - 6, GREY_INK).move_to(c.box.get_corner(DR) + LEFT * 0.08 + UP * 0.1,
                                                               aligned_edge=DR)
                        for r, c in zip(["atm", "vac", "LP", "seal"], cells)])
        for n_, c in zip(notes, cells):
            n_.next_to(c.box, DOWN, buff=0.35)
        for k, ((n, kind, ph), c) in enumerate(zip(kinds, cells)):
            self.sync(self.c(1, ph))
            self.play(Create(c[:2]), FadeIn(c[2:]), FadeIn(c.dia), FadeIn(names[k]), FadeIn(refs[k]), run_time=0.6)
            push = Arrow(c.box.get_left() + LEFT * 0.75, c.box.get_left() + LEFT * 0.05, buff=0, stroke_width=5,
                         color=FLUID, max_tip_length_to_length_ratio=0.35).shift(DOWN * 0.45)
            self.play(GrowArrow(push), c.bow.animate.set_value(0.35), run_time=0.6)
            if kind == "dp":
                back = Arrow(c.box.get_right() + RIGHT * 0.75, c.box.get_right() + RIGHT * 0.05, buff=0, stroke_width=3,
                             color=FLUID, max_tip_length_to_length_ratio=0.35).shift(DOWN * 0.45)
                self.play(GrowArrow(back), c.bow.animate.set_value(0.15), run_time=0.5)
                self.play(FadeOut(back), run_time=0.2)
            self.play(FadeOut(push), c.bow.animate.set_value({"sealed": 0.08, "absolute": 0.35}.get(kind, 0.0)),
                      FadeIn(notes[k]), run_time=0.6)
            if kind == "gauge":
                self.sync(self.c(1, "رِيحٍ"))
                wind = icon("wind", GREY_INK, 0.45).next_to(c.box, DOWN, buff=0.12).align_to(c.box, RIGHT)
                notes[0].next_to(wind, DOWN, buff=0.1).align_to(c.box, LEFT)
                self.play(FadeIn(wind), c.bow.animate.set_value(0.12), run_time=0.4)
                self.play(c.bow.animate.set_value(-0.1), run_time=0.3)
                self.play(c.bow.animate.set_value(0.0), run_time=0.3)
            if kind == "dp":
                self.sync(self.c(1, "الأَخْطَرُ"))
                self.play(Indicate(c.box, color=BAD), run_time=0.6)
        self.sync(self.end(1) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 2: DP with square root ----------------
    def seg2_dp_sqrt(self):
        section_title(self, "DP on an orifice plate, square root inside", prev=self.sec)
        orf = orifice_plate(size=1.4).move_to([-4.2, 0.3, 0])
        run_in = pipe(orf.port("in") + LEFT * 1.4, orf.port("in"), width=8)
        run_out = pipe(orf.port("out"), orf.port("out") + RIGHT * 1.4, width=8)
        dp = device("DP", 1.2, 0.8, FS_LABEL).move_to([-4.2, -1.8, 0])
        taps = VGroup(pipe(orf.port("in") + RIGHT * 0.25, [-4.6, -1.4, 0], width=3),
                      pipe(orf.port("out") + LEFT * 0.25, [-3.8, -1.4, 0], width=3))
        self.play(Create(run_in), FadeIn(orf), Create(run_out), Create(taps), FadeIn(dp), run_time=0.8)
        self.play(flow(pipe(orf.port("in") + LEFT * 1.4, orf.port("out") + RIGHT * 1.4), FLUID, 8), run_time=0.9)
        ch = Chart(0.2, -2.8, 5.6, 4.6, (0, 100), (4, 20), xticks=[(0, "0"), (50, "50 %"), (100, "100")],
                   yticks=[(4, "4"), (12, "12"), (20, "20")], xlabel="DP", ylabel="mA")
        lin = ch.line([(0, 4), (100, 20)], GREY_INK, 3)
        sq = ch.line([(p, D.i_sqrt(D.LRV + p / 100 * D.SPAN)) for p in [q / 4 for q in range(0, 81)] + list(range(21, 101))],
                     MOVE, 4)
        self.play(Create(ch.axes), FadeIn(ch.ticks), FadeIn(ch.xl), FadeIn(ch.yl), Create(lin), run_time=0.6)
        self.play(Create(sq), run_time=0.8)
        self.sync(self.c(2, "فَنِصْفُ"))
        g = DashedLine(ch.p(50, 4), ch.p(50, D.DP_50_SQRT_MA), color=MOVE, stroke_width=2)
        d1 = Dot(ch.p(50, D.DP_50_LINEAR_MA), radius=0.08, color=GREY_INK)
        d2 = Dot(ch.p(50, D.DP_50_SQRT_MA), radius=0.09, color=MOVE)
        t1 = tag(f"not {fmt(D.DP_50_LINEAR_MA, 0)} mA", FS_TAG, GREY_INK).next_to(d1, RIGHT, buff=0.15)
        self.play(Create(g), FadeIn(d1), FadeIn(t1), run_time=0.6)
        self.sync(self.c(2, "بَلْ"))
        t2 = tag(f"{fmt(D.DP_50_SQRT_MA, 3)} mA", FS_TAG + 2, MOVE, weight=BOLD).next_to(d2, UL, buff=0.1)
        wk = tag(f"4 + 16 × √0.5 = {fmt(D.DP_50_SQRT_MA, 3)} mA", FS_TAG + 1, MOVE) \
            .next_to(ch.axes, UP, buff=0.55).align_to(ch.axes, LEFT).shift(RIGHT * 0.7)
        self.play(FadeIn(d2, scale=1.5), FadeIn(t2), FadeIn(wk), run_time=0.6)
        self.sync(self.end(2) - 0.5)
        self.clear(self.sec, run_time=0.5)

    # ---------------- Segment 3: three electrical connections; HART ----------------
    def seg3_connections(self):
        section_title(self, "Three electrical connections", prev=self.sec)

        def panel(cx, title, col):
            fr = RoundedRectangle(width=4.2, height=3.3, corner_radius=0.15, color=col, stroke_width=3) \
                .move_to([cx, 1.05, 0])
            t = tag(title, FS_TAG + 2, col, weight=BOLD).next_to(fr.get_top(), DOWN, buff=0.2)
            return fr, t

        xa, xb, xc = -4.55, 0, 4.55
        fa, ta = panel(xa, "A  workshop", MOVE)
        fb, tb = panel(xb, "B  live loop", FLUID)
        fc, tc = panel(xc, "C  test diode", GREY_INK)
        # A: MC6 supplies 24 V and measures
        xa_t = transmitter(bubble=False).scale(0.55).move_to([xa - 1.1, 0.7, 0])
        ma = device(f"MC6\n{D.MC6_LOOP_V} V + mA", 1.8, 0.95, FS_TAG).move_to([xa + 0.95, 0.7, 0])
        la = pipe(xa_t.body.get_right() + UP * 0.1, ma.box.get_left() + UP * 0.1, width=3)
        la2 = pipe(xa_t.body.get_bottom(), [xa_t.body.get_bottom()[0], -0.3, 0], [ma.box.get_bottom()[0], -0.3, 0],
                   ma.box.get_bottom(), width=3)
        ha = tag("HART available", FS_TAG, GOOD).move_to([xa, -0.9, 0])
        # B: DCS supplies, MC6 in series measures
        xb_t = transmitter(bubble=False).scale(0.55).move_to([xb - 1.2, 0.7, 0])
        dcs = device("DCS\nsupply", 1.3, 0.85, FS_TAG).move_to([xb + 1.3, 0.8, 0])
        mb = device("MC6 mA", 1.4, 0.55, FS_TAG).move_to([xb, -0.25, 0])
        lb = pipe(xb_t.body.get_right() + UP * 0.1, dcs.box.get_left() + UP * 0.1, width=3)
        lb2 = pipe(xb_t.body.get_bottom(), [xb_t.body.get_bottom()[0], -0.25, 0], mb.box.get_left(), width=3)
        lb3 = pipe(mb.box.get_right(), [dcs.box.get_bottom()[0], -0.25, 0], dcs.box.get_bottom(), width=3)
        # C: meter across the test diode, loop not broken
        xc_t = transmitter(bubble=False).scale(0.55).move_to([xc - 1.0, 0.7, 0])
        diode = VGroup(Triangle(color=INK, stroke_width=3).scale(0.14).rotate(-PI / 2),
                       Line(UP * 0.14, DOWN * 0.14, stroke_width=3, color=INK).shift(RIGHT * 0.15)) \
            .move_to([xc + 0.4, 0.95, 0])
        dl = pipe(xc_t.body.get_right() + UP * 0.25, diode.get_left(), width=3)
        dl2 = pipe(diode.get_right(), [xc + 1.6, 0.95, 0], width=3)
        mc = device("MC6 mA", 1.4, 0.55, FS_TAG).move_to([xc + 0.7, -0.15, 0])
        par = VGroup(pipe([xc + 0.15, 0.95, 0], [xc + 0.15, 0.13, 0], width=2),
                     pipe([xc + 1.25, 0.95, 0], [xc + 1.25, 0.13, 0], width=2))
        self.play(Create(fa), FadeIn(ta), FadeIn(xa_t), FadeIn(tag(D.TAG, FS_TAG - 2, FLUID).next_to(xa_t, UP, buff=0.08)), FadeIn(ma), Create(la), Create(la2), run_time=0.8)
        self.play(flow(la2, MOVE, 5), flow(la, MOVE, 5), FadeIn(ha), run_time=1.0)
        self.sync(self.c(3, "الثَّانِيَةُ"))
        self.play(Create(fb), FadeIn(tb), FadeIn(xb_t), FadeIn(tag(D.TAG, FS_TAG - 2, FLUID).next_to(xb_t, UP, buff=0.08)), FadeIn(dcs), FadeIn(mb), Create(lb), Create(lb2), Create(lb3),
                  run_time=0.8)
        live = tag("control active", FS_TAG, BAD).move_to([xb, 2.05, 0]).shift(DOWN * 0.05)
        self.sync(self.c(3, "وَالتَّحَكُّمُ فَعَّالٌ"))
        self.play(FadeIn(live), flow(lb2, FLUID, 5), run_time=0.8)
        self.sync(self.c(3, "الثَّالِثَةُ"))
        self.play(Create(fc), FadeIn(tc), FadeIn(xc_t), FadeIn(tag(D.TAG, FS_TAG - 2, FLUID).next_to(xc_t, UP, buff=0.08)), FadeIn(diode), Create(dl), Create(dl2), run_time=0.8)
        self.play(FadeIn(mc), Create(par), run_time=0.6)
        self.sync(self.c(3, "لٰكِنَّ تَسَرُّبَ"))
        heat = VGroup(icon("temperature", BAD, 0.4), tag("hot: diode leakage\n→ reading shifts", FS_TAG, BAD)) \
            .arrange(RIGHT, buff=0.1).move_to([xc, -1.2, 0])
        self.play(FadeIn(heat), run_time=0.6)
        # HART: 250 Ω, not a second one; modem in parallel
        self.sync(self.c(3, "وَهَارْت يَحْتَاجُ"))
        yw, xr = -2.2, -3.2
        wire = VGroup(Line([-6.2, yw, 0], [xr - 0.55, yw, 0], stroke_width=3, color=INK),
                      Line([xr + 0.55, yw, 0], [-0.4, yw, 0], stroke_width=3, color=INK))
        rbox = Rectangle(width=1.1, height=0.36, color=MOVE, stroke_width=3).set_fill(WHITE, 1).move_to([xr, yw, 0])
        wl = tag("loop", FS_TAG - 2, GREY_INK).next_to(wire[0], UP, buff=0.08).align_to(wire[0], LEFT)
        rl = tag(f"≥ {D.MC6_HART_R_EXT} Ω loop resistance", FS_TAG + 1, MOVE).next_to(rbox, UP, buff=0.15)
        self.play(Create(wire), FadeIn(rbox), FadeIn(wl), FadeIn(rl), run_time=0.6)
        self.sync(self.c(3, "فَلَا تُضِفْ"))
        one = tag("often already in the DCS input:\ndo not add a second", FS_TAG + 1, GREY_INK) \
            .next_to(wire[1], RIGHT, buff=0.3)
        self.play(Indicate(rbox, color=MOVE), FadeIn(one), run_time=0.6)
        self.sync(self.c(3, "وَالمُودِمُ"))
        mdm = device("HART modem", 1.9, 0.45, FS_TAG - 2).move_to([xr, yw - 0.95, 0])
        mdm.box.set_stroke(GOOD)
        leads = VGroup(pipe([xr - 0.55, yw, 0], [xr - 0.55, mdm.box.get_top()[1], 0], color=GOOD, width=3),
                       pipe([xr + 0.55, yw, 0], [xr + 0.55, mdm.box.get_top()[1], 0], color=GOOD, width=3))
        pl = tag("in parallel ✓", FS_TAG + 1, GOOD).next_to(mdm, LEFT, buff=0.3)
        sl = tag("never in series ✗", FS_TAG + 1, BAD).next_to(one, DOWN, buff=0.2).align_to(one, LEFT)
        self.play(Create(leads), FadeIn(mdm), FadeIn(pl), run_time=0.7)
        self.play(FadeIn(sl), run_time=0.4)
        self.sync(self.end(3) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 4: the 3-valve manifold; isolation ----------------
    def seg4_isolate(self):
        section_title(self, "3-valve manifold: isolating the DP cell", prev=self.sec)
        mf = Manifold()
        self.mf = mf
        self.play(Create(mf.static()), FadeIn(mf.moving()), run_time=1.2)
        for k, (ph, pt) in enumerate(zip(["صِمَامُ عَزْلٍ لِلْعَالِي", "وَصِمَامُ عَزْلٍ لِلْمُنْخَفِضِ", "وَصِمَامُ مُعَادَلَةٍ"],
                                         [[mf.xh, 1.6, 0], [mf.xl, 1.6, 0], [mf.ox, 0.4, 0]])):
            self.sync(self.c(4, ph))
            self.play(Circumscribe(mf.names[k], color=MOVE), Flash(pt, color=MOVE, flash_radius=0.4), run_time=0.6)
        self.sync(self.c(4, "غِشَاؤُهُ"))
        self.play(Indicate(mf.dia, color=MOVE), run_time=0.6)
        line = tag(f"line pressure {D.LINE_PRESSURE_BAR} bar on both sides", FS_TAG + 1, FLUID) \
            .move_to([3.6, 2.4, 0]).align_to([0.9, 0, 0], LEFT)
        self.sync(self.c(4, "وَضَغْطُ الخَطِّ"))
        self.play(FadeIn(line), run_time=0.5)
        # the danger: one side vented while the other holds line pressure
        self.sync(self.c(4, "فَالخَطَرُ"))
        danger = tag("one side vented, the other at line\npressure: full pressure across\nthe diaphragm",
                     FS_TAG + 1, BAD).next_to(line, DOWN, buff=0.3).align_to(line, LEFT)
        self.play(mf.lp.animate.set_value(0), run_time=0.4)
        self.play(mf.vent.animate.set_value(1), FadeIn(danger), run_time=0.8)
        self.sync(self.c(4, "فَيَتَمَدَّدُ"))
        self.play(Flash(mf.cell.get_center(), color=BAD, flash_radius=0.6), run_time=0.6)
        self.play(mf.vent.animate.set_value(0), mf.lp.animate.set_value(1), FadeOut(danger), run_time=0.6)
        # the reference-manual sequence
        steps = ["1  close LP isolate", "2  open equalize", "3  close HP isolate",
                 "4  open vent slowly, face away", "5  check: zero pressure"]
        lst = VGroup(*[tag(s, FS_TAG + 1) for s in steps]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        lst.next_to(line, DOWN, buff=0.45).align_to(line, LEFT)
        src = tag("per the transmitter reference manual", FS_TAG - 2, GREY_INK).next_to(lst, DOWN, buff=0.25) \
            .align_to(lst, LEFT)
        acts = [("أَغْلِقْ عَزْلَ المُنْخَفِضِ", mf.lp, 0), ("ثُمَّ افْتَحِ المُعَادَلَةَ", mf.eq, 1),
                ("ثُمَّ أَغْلِقْ عَزْلَ العَالِي", mf.hp, 0), ("ثُمَّ افْتَحِ التَّنْفِيسَ", mf.vent, 1)]
        self.sync(self.c(4, "وَالتَّسَلْسُلُ") )
        self.play(FadeIn(src), run_time=0.3)
        for k, (ph, tr, val) in enumerate(acts):
            self.sync(self.c(4, ph))
            self.play(FadeIn(lst[k], shift=RIGHT * 0.1), lst[k].animate.set_color(GOOD), tr.animate.set_value(val),
                      run_time=0.9 if k < 3 else 1.4)
        self.sync(self.c(4, "وَتَحَقَّقْ"))
        self.play(FadeIn(lst[4]), lst[4].animate.set_color(GOOD), Indicate(mf.readout, color=GOOD), run_time=0.7)
        self.lst4 = VGroup(line, lst, src)
        self.sync(self.end(4) - 0.4)

    # ---------------- Segment 5: return to service; the forgotten equalize ----------------
    def seg5_return(self):
        mf = self.mf
        self.sec = section_title(self, "Return to service", prev=self.sec)
        self.play(FadeOut(self.lst4), run_time=0.4)
        steps = ["1  close vent", "2  equalize open: open HP slowly", "3  close equalize",
                 "4  open LP isolate", "5  leak check, watch the reading"]
        lst = VGroup(*[tag(s, FS_TAG + 2) for s in steps]).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        lst.move_to([3.4, 1.3, 0]).align_to([1.0, 0, 0], LEFT)
        acts = [("أَغْلِقِ التَّنْفِيسَ", mf.vent, 0), ("وَافْتَحْ عَزْلَ العَالِي", mf.hp, 1),
                ("ثُمَّ أَغْلِقِ المُعَادَلَةَ", mf.eq, 0), ("ثُمَّ افْتَحْ عَزْلَ المُنْخَفِضِ", mf.lp, 1)]
        for k, (ph, tr, val) in enumerate(acts):
            self.sync(self.c(5, ph))
            self.play(FadeIn(lst[k], shift=RIGHT * 0.1), lst[k].animate.set_color(GOOD), tr.animate.set_value(val),
                      run_time=1.2 if k == 1 else 0.8)
        self.sync(self.c(5, "وَافْحَصِ"))
        self.play(FadeIn(lst[4]), lst[4].animate.set_color(GOOD), run_time=0.5)
        # the late mistake: equalize left open
        self.sync(self.c(5, "وَالخَطَأُ المُتَأَخِّرُ"))
        ring = Circle(radius=0.29, color=BAD, stroke_width=5).move_to([mf.ox, 0.4, 0])
        self.play(mf.eq.animate.set_value(1), Create(ring), lst[2].animate.set_color(BAD),
                  mf.names[2].animate.set_color(BAD), run_time=0.6)
        rd = tag("DP reading: 0\nwhatever the flow", FS_TAG + 2, BAD, weight=BOLD).next_to(lst, DOWN, buff=0.5) \
            .align_to(lst, LEFT)
        arrows = VGroup(*[Arrow([mf.xh - 0.6, 2.4 - 0.5 * k, 0], [mf.xh - 0.1, 2.4 - 0.5 * k, 0], buff=0,
                                stroke_width=4, color=FLUID, max_tip_length_to_length_ratio=0.3) for k in range(2)])
        self.play(FadeIn(rd), FadeIn(arrows, lag_ratio=0.5), run_time=0.8)
        fl = tag("flow", FS_TAG, FLUID).next_to(arrows, LEFT, buff=0.15)
        self.play(FadeIn(fl), run_time=0.3)
        self.sync(self.c(5, "مَهْمَا"))
        for f in (1.8, 0.5):
            self.play(arrows.animate.stretch(f, 0, about_edge=RIGHT), Indicate(rd, color=BAD, scale_factor=1.05),
                      run_time=0.8)
        self.play(Indicate(mf.dia, color=BAD), run_time=0.7)
        self.sync(self.end(5) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 6: before starting; H2S ----------------
    def seg6_safety(self):
        section_title(self, "Before starting", prev=self.sec)
        items = ["valid permit: equipment, scope, time", "gas test before and during",
                 "PPE + personal gas detector", "exits, muster point, eyewash", "never alone in a classified area"]
        checklist(self, items, cues=[self.c(6, "تَصْرِيحُ"), self.c(6, "وَفَحْصُ"), self.c(6, "وَمُعِدَّاتُ"),
                                     self.c(6, "وَمَعْرِفَةُ"), self.c(6, "وَلَا عَمَلَ")],
                  pos=[-3.4, 0.6, 0], size=FS_TAG + 1)
        # H2S: heavier than air, collects low
        self.sync(self.c(6, "وَكِبْرِيتِيدُ"))
        ground = pipe([0.8, -1.9, 0], [2.6, -1.9, 0], [2.9, -2.9, 0], [4.3, -2.9, 0], [4.6, -1.9, 0], [6.7, -1.9, 0],
                      color=INK, width=4)
        src = Dot([1.4, -1.6, 0], radius=0.1, color=GREY_INK)
        gas = VGroup(*[Circle(radius=0.12, color=GREY_INK, stroke_width=2).set_fill(GREY_INK, 0.45)
                       .move_to([1.4, -1.6, 0]) for _ in range(6)])
        hl = tag("H₂S: heavier than air →\ncollects in pits and low points", FS_TAG + 1, BAD) \
            .move_to([3.0, 2.2, 0]).align_to([0.6, 0, 0], LEFT)
        self.play(Create(ground), FadeIn(src), FadeIn(hl), run_time=0.6)
        self.play(*[g.animate.move_to([3.0 + 0.25 * k, -2.7 + 0.12 * (k % 2), 0]) for k, g in enumerate(gas)],
                  run_time=1.6)
        self.sync(self.c(6, "وَيَشُلُّ"))
        smell = tag("smell disappears at\nhigh concentration:\nno smell ≠ safe", FS_TAG + 1, BAD) \
            .next_to(hl, DOWN, buff=0.3).align_to(hl, LEFT)
        self.play(FadeIn(smell), run_time=0.6)
        self.sync(self.c(6, "وَالمَشْعَبُ"))
        vv = gate_valve(size=0.45).rotate(PI / 2).move_to([3.6, -1.2, 0])
        vvl = tag("open vent", FS_TAG - 2, GREY_INK).next_to(vv, LEFT, buff=0.15)
        plume = VGroup(*[Circle(radius=0.1, color=GREY_INK, stroke_width=2).set_fill(GREY_INK, 0.4)
                         .move_to(vv.get_top()) for _ in range(4)])
        self.play(FadeIn(vv), FadeIn(vvl), FadeIn(plume), run_time=0.4)
        self.play(*[m.animate.move_to([3.2 - 0.45 * i, -0.75 + 0.1 * (i % 2), 0]).set_opacity(0.15)
                    for i, m in enumerate(plume)], run_time=1.0)
        person = icon("user", INK, 0.8).move_to([5.8, -1.45, 0])
        wind = Arrow([6.8, -0.55, 0], [5.3, -0.55, 0], buff=0, stroke_width=4, color=FLUID,
                     max_tip_length_to_length_ratio=0.2)
        wl = tag("wind", FS_TAG, FLUID).next_to(wind, UP, buff=0.08)
        self.play(FadeIn(person), GrowArrow(wind), FadeIn(wl), run_time=0.6)
        self.sync(self.c(6, "صَرِّفْ"))
        tip = tag("drain to a closed system\nstand with the wind at your back", FS_TAG, GOOD) \
            .next_to(ground, DOWN, buff=0.2).align_to([0.8, 0, 0], LEFT)
        self.play(FadeIn(tip), run_time=0.6)
        self.sync(self.end(6) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 7: zones; process and loop isolation ----------------
    def seg7_zones(self):
        section_title(self, "Hazardous zones · isolation", prev=self.sec)
        vessel = tank(size=0.75).move_to([-4.6, 0.5, 0])
        z0 = Ellipse(width=1.4, height=1.7, color=BAD, stroke_width=4).move_to(vessel)
        z1 = Ellipse(width=2.7, height=2.8, color=MOVE, stroke_width=4).move_to(vessel)
        z2 = DashedVMobject(Ellipse(width=4.0, height=3.7, color=GREY_INK, stroke_width=3), num_dashes=40).move_to(vessel)
        labels = [tag("Zone 0: flammable mixture always", FS_TAG, BAD),
                  tag("Zone 1: likely in normal operation", FS_TAG, MOVE),
                  tag("Zone 2: not expected, short if it occurs", FS_TAG, GREY_INK)]
        VGroup(*labels).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(z2, DOWN, buff=0.2).align_to([-6.6, 0, 0], LEFT)
        self.play(FadeIn(vessel), run_time=0.4)
        for z, l, ph in zip([z0, z1, z2], labels, ["صِفْر", "وَوَاحِد", "وَاثْنَان"]):
            self.sync(self.c(7, ph))
            self.play(Create(z), FadeIn(l), run_time=0.6)
        self.sync(self.c(7, "وَالهَاتِفُ"))
        ph_note = tag("phone and camera: same restriction", FS_TAG, BAD).next_to(labels[2], DOWN, buff=0.1).align_to(labels[2], LEFT)
        self.play(FadeIn(ph_note), run_time=0.5)
        # process isolation: double block and bleed, lock and tag
        self.sync(self.c(7, "وَلِعَزْلِ العَمَلِيَّةِ"))
        sds = VGroup(icon("file-text", INK, 0.45), tag("process fluid from the safety data sheet", FS_TAG + 1)) \
            .arrange(RIGHT, buff=0.15).move_to([2.8, 2.5, 0]).align_to([-0.15, 0, 0], LEFT)
        self.play(FadeIn(sds), run_time=0.5)
        self.sync(self.c(7, "وَاعْزِلْ"))
        v1 = gate_valve(size=0.6).move_to([-0.3, 1.5, 0])
        v2 = gate_valve(size=0.6).move_to([1.5, 1.5, 0])
        run = VGroup(pipe([-1.2, 1.5, 0], v1.port("in"), width=6), pipe(v1.port("out"), v2.port("in"), width=6),
                     pipe(v2.port("out"), [2.4, 1.5, 0], width=6))
        bleed = gate_valve(size=0.45).rotate(PI / 2).move_to([0.6, 0.75, 0])
        bl = pipe([0.6, 1.5, 0], bleed.get_top(), width=4)
        dbb = tag("double block and bleed", FS_TAG + 1, GOOD).move_to([4.2, 1.6, 0]).align_to([2.7, 0, 0], LEFT)
        self.play(Create(run), FadeIn(v1), FadeIn(v2), Create(bl), FadeIn(bleed), run_time=0.7)
        self.play(*[v.animate.set_fill(INK, 1) for v in (v1, v2)], bleed.animate.set_color(GOOD), FadeIn(dbb),
                  run_time=0.6)
        self.sync(self.c(7, "فَصِمَامٌ وَاحِدٌ"))
        one = tag("one valve is not isolation", FS_TAG + 1, BAD).next_to(dbb, DOWN, buff=0.2).align_to(dbb, LEFT)
        x1 = cross(v1, BAD, 4, pad=0.08)
        self.play(FadeIn(one), v2.animate.set_opacity(0.2), bleed.animate.set_stroke(opacity=0.2), Create(x1),
                  run_time=0.5)
        self.sync(self.c(7, "وَضَعْ قُفْلًا") - 0.4)
        self.play(v2.animate.set_opacity(1), bleed.animate.set_stroke(opacity=1), FadeOut(x1), run_time=0.4)
        lock = VGroup(icon("lock", MOVE, 0.5), tag("lock + tag with your name", FS_TAG + 1, MOVE)) \
            .arrange(RIGHT, buff=0.12).move_to([0, -0.05, 0]).align_to([0.0, 0, 0], LEFT)
        self.play(FadeIn(lock), FadeIn(icon("lock", MOVE, 0.32).next_to(v1, UP, buff=0.04)), run_time=0.5)
        self.sync(self.c(7, "وَافْتَرِضْ"))
        trapped = tag("assume trapped pressure\nuntil proven otherwise", FS_TAG, BAD).next_to(lock, DOWN, buff=0.12) \
            .align_to(lock, LEFT)
        self.play(FadeIn(trapped), run_time=0.5)
        # loop isolation
        self.sync(self.c(7, "وَلِعَزْلِ الحَلْقَةِ"))
        cr = device("control room", 2.4, 0.8, FS_TAG + 2).move_to([1.2, -1.55, 0])
        sw = VGroup(tag("AUTO", FS_TAG + 2, GREY_INK), tag("→", FS_TAG + 2), tag("MAN", FS_TAG + 2, MOVE, weight=BOLD)) \
            .arrange(RIGHT, buff=0.15).next_to(cr, RIGHT, buff=0.3)
        self.play(FadeIn(cr), run_time=0.4)
        self.sync(self.c(7, "وَضَعِ الحَلْقَةَ"))
        self.play(FadeIn(sw, lag_ratio=0.3), run_time=0.6)
        self.sync(self.c(7, "وَتَجَاوَزِ"))
        byp = tag("alarm bypass: approved, documented", FS_TAG + 1, GREY_INK).next_to(cr, DOWN, buff=0.2).align_to([0.0, 0, 0], LEFT)
        self.play(FadeIn(byp), run_time=0.4)
        self.sync(self.c(7, "وَمُرْسِلُ نِظَامِ"))
        sis = VGroup(icon("shield-check", BAD, 0.45), tag("SIS: special procedure,\nhigher authority", FS_TAG + 1, BAD)) \
            .arrange(RIGHT, buff=0.12).next_to(byp, DOWN, buff=0.2).align_to([0.0, 0, 0], LEFT)
        self.play(FadeIn(sis), run_time=0.5)
        self.sync(self.end(7) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 8: pressure hazards during calibration ----------------
    def seg8_pressure(self):
        section_title(self, "During calibration", prev=self.sec)
        mod = device("module\nrange", 1.6, 1.0, FS_TAG).move_to([-5.3, 1.4, 0])
        over = tag("never above the module range", FS_TAG + 1, BAD).next_to(mod, RIGHT, buff=0.3)
        self.play(FadeIn(mod), FadeIn(over), run_time=0.5)
        self.sync(self.c(8, "وَقِفْ"))
        fitting = Circle(radius=0.25, color=INK, stroke_width=4).move_to([-4.6, -0.8, 0])
        hose = poly([fitting.get_right(), [-3.5, -0.5, 0], [-2.6, -1.3, 0], [-1.6, -1.0, 0]], INK, 6, smooth=True)
        front = icon("user", BAD, 0.7).move_to([-4.6, 0.3, 0])
        side = icon("user", GOOD, 0.7).move_to([-6.0, -0.8, 0])
        self.play(Create(fitting), Create(hose), FadeIn(front), run_time=0.5)
        self.play(Create(cross(front)), FadeIn(side), run_time=0.5)
        self.sync(self.c(8, "وَثَبِّتِ"))
        tie = VGroup(*[Line([x, -1.55, 0], [x, -0.75, 0], stroke_width=4, color=GOOD) for x in (-3.3, -2.2)])
        tl = tag("hose secured: no whip", FS_TAG + 1, GOOD).next_to(hose, DOWN, buff=0.55)
        self.play(Create(tie), FadeIn(tl), run_time=0.5)
        self.sync(self.c(8, "وَنَفِّسْ"))
        slow = tag("vent slowly, always", FS_TAG + 1, MOVE).next_to(tl, DOWN, buff=0.2)
        self.play(FadeIn(slow), run_time=0.4)
        self.sync(self.c(8, "وَنَفَّاثُ"))
        pin = Dot([1.4, 0.8, 0], radius=0.07, color=INK)
        jet = VGroup(*[Line([1.4, 0.8, 0], [1.4 + 1.2 * np.cos(a), 0.8 + 1.2 * np.sin(a), 0], stroke_width=3, color=BAD)
                       for a in (-0.15, 0, 0.15)])
        hand = VGroup(icon("alert-triangle", BAD, 0.5), tag("fine liquid jet can enter the skin:\n"
                                                           "never feel for a leak by hand", FS_TAG + 1, BAD)) \
            .arrange(RIGHT, buff=0.15).move_to([3.75, -0.3, 0])
        self.play(FadeIn(pin), Create(jet), FadeIn(hand), run_time=0.8)
        self.sync(self.c(8, "وَاحْذَرِ"))
        a = gate_valve(size=0.55).move_to([1.0, -2.2, 0]).set_fill(INK, 1)
        b = gate_valve(size=0.55).move_to([3.6, -2.2, 0]).set_fill(INK, 1)
        mid = Rectangle(width=a.get_right()[0] - b.get_left()[0], height=0.2, stroke_width=0)
        mid = Rectangle(width=b.get_left()[0] - a.get_right()[0], height=0.2, stroke_width=0) \
            .set_fill(BAD, 0.6).move_to([(a.get_right()[0] + b.get_left()[0]) / 2, -2.2, 0])
        tp = tag("trapped pressure between\ntwo closed valves", FS_TAG + 1, BAD).next_to(VGroup(a, b), UP, buff=0.25)
        self.play(FadeIn(a), FadeIn(b), GrowFromCenter(mid), FadeIn(tp), run_time=0.8)
        self.sync(self.end(8) + 1.0)


if __name__ == "__main__":
    main(__file__, "PtCalEp03", NARRATION)
