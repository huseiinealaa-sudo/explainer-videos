"""ut_series, episode 3: Calibration and angle-beam testing.

Build (from the repo root):
    python projects/ut_series/ut_series_ep03_calibration.py --preview   # 480p15 -> tmp/ut_series_ep03_calibration/preview.mp4
    python projects/ut_series/ut_series_ep03_calibration.py             # 1080p30 -> output/ut_series_ep03_calibration.mp4

Narration segments: 1-6 are the six sections of the source (TCS-67 §2.4.2, §5, §8.4.1); 7 is the review
intro and 8-31 are the eight review questions (question, 3 s silent countdown, answer).
"""
from explainer import *
import numpy as np
import ut_series_data as D
from ut_visuals import wavefront, Probe, SteelBlock, AScan, tag_line, wrap_two_lines, signal_bar
from ut_review import run_review, fly, pk

# Fully diacritized narration, approved by the owner on 2026-10-04 (with his four edits).
# Decimals are spoken digit by digit after «فَاصِلَةٌ».
NARRATION = [
    # 1  §1 why calibrate
    "الجِهَازُ يَقِيسُ زَمَنًا، وَالمُعَايَرَةُ تَجْعَلُ شَاشَتَهُ تَقْرَأُ مَسَافَةً صَحِيحَةً، وَتَضْبِطُ حَسَاسِيَّتَهُ عَلَى مَرْجِعٍ مَعْرُوفٍ. وَنَتَحَقَّقُ كَذٰلِكَ مِنْ خَصَائِصِ الجِهَازِ: الخَطِّيَّةُ الأُفُقِيَّةُ، أَيْ تَنَاسُبُ المَسَافَاتِ عَلَى الشَّاشَةِ مَعَ المَسَافَاتِ الحَقِيقِيَّةِ. وَالخَطِّيَّةُ الرَّأْسِيَّةُ، أَيْ تَنَاسُبُ ارْتِفَاعِ الصَّدَى مَعَ سَعَتِهِ. وَالتَّمْيِيزُ، أَيْ فَصْلُ عَاكِسَيْنِ مُتَقَارِبَيْنِ. وَالمِنْطَقَةُ المَيِّتَةُ، وَهِيَ العُمْقُ القَرِيبُ مِنَ السَّطْحِ الَّذِي تُخْفِي فِيهِ النَّبْضَةُ الِابْتِدَائِيَّةُ الأَصْدَاءَ. وَنُعِيدُ الفَحْصَ لِأَنَّ البِلَى يُغَيِّرُ نُقْطَةَ الخُرُوجِ وَزَاوِيَةَ المِجَسِّ.",
    # 2  §2 the V1 block and the time base
    "كُتْلَةُ آيْ آيْ دَبْلْيُو فِي وَاحِدْ كُتْلَةٌ فُولَاذِيَّةٌ قِيَاسِيَّةٌ سَمَاكَتُهَا خَمْسَةٌ وَعِشْرُونَ مِلِّيمِتْرًا، فِيهَا قَوْسٌ نِصْفُ قُطْرِهِ مِئَةُ مِلِّيمِتْرٍ، وَثَقْبٌ قُطْرُهُ وَاحِدٌ فَاصِلَةٌ خَمْسَةٌ مِلِّيمِتْرٍ، وَثَقْبٌ كَبِيرٌ بِحَشْوَةٍ بِلَاسْتِيكِيَّةٍ، وَتَدْرِيجٌ لِلزَّوَايَا. نَضَعُ المِجَسَّ العَمُودِيَّ عَلَى السَّمَاكَةِ، فَيَرْتَدُّ الصَّوْتُ بَيْنَ الوَجْهَيْنِ مَرَّةً بَعْدَ مَرَّةٍ، وَتَظْهَرُ أَصْدَاءٌ مُتَعَدِّدَةٌ لِلْجِدَارِ الخَلْفِيِّ عَلَى أَبْعَادٍ مُتَسَاوِيَةٍ، وَيَضْعُفُ كُلُّ صَدًى عَنِ الَّذِي قَبْلَهُ. نَضْبِطُ التَّأْخِيرَ وَالمَدَى حَتَّى تَقَعَ الأَصْدَاءُ عِنْدَ خَمْسَةٍ وَعِشْرِينَ وَخَمْسِينَ وَخَمْسَةٍ وَسَبْعِينَ وَمِئَةٍ، عَلَى مَدًى قَدْرُهُ مِئَةُ مِلِّيمِتْرٍ. وَتَسَاوِي المَسَافَاتِ بَيْنَهَا يَتَحَقَّقُ بِهِ أَيْضًا مِنَ الخَطِّيَّةِ الأُفُقِيَّةِ.",
    # 3  §3 refraction and the two critical angles
    "حِينَ تَسْقُطُ المَوْجَةُ بِزَاوِيَةٍ عَلَى سَطْحٍ فَاصِلٍ تَنْكَسِرُ، وَتَنْقَسِمُ فِي الفُولَاذِ إِلَى مَوْجَةٍ طُولِيَّةٍ وَمَوْجَةٍ مُسْتَعْرِضَةٍ بِزَاوِيَتَيْنِ مُخْتَلِفَتَيْنِ، وَالطُّولِيَّةُ تَنْكَسِرُ أَكْثَرَ لِأَنَّهَا أَسْرَعُ. بِزِيَادَةِ زَاوِيَةِ الإِسْفِينِ تَصِلُ الطُّولِيَّةُ المُنْكَسِرَةُ إِلَى تِسْعِينَ دَرَجَةً وَتَخْتَفِي مِنَ القِطْعَةِ. هٰذِهِ الزَّاوِيَةُ الحَرِجَةُ الأُولَى، وَهِيَ نَحْوُ سَبْعَةٍ وَعِشْرِينَ فَاصِلَةٍ خَمْسَةٍ دَرَجَةً لِإِسْفِينٍ مِنَ البِيرْسْبِكْسْ عَلَى الفُولَاذِ، وَبَعْدَهَا تَبْقَى فِي الفُولَاذِ مَوْجَةٌ مُسْتَعْرِضَةٌ وَحْدَهَا. وَبِزِيَادَةٍ أَكْبَرَ تَصِلُ المُسْتَعْرِضَةُ إِلَى تِسْعِينَ دَرَجَةً: الزَّاوِيَةُ الحَرِجَةُ الثَّانِيَةُ، نَحْوُ سَبْعَةٍ وَخَمْسِينَ دَرَجَةً، وَبَعْدَهَا تَتَوَلَّدُ مَوْجَةٌ سَطْحِيَّةٌ. لِهٰذَا تُصَمَّمُ المِجَسَّاتُ المَائِلَةُ بَيْنَ الزَّاوِيَتَيْنِ، فَتُعْطِي مَوْجَةً مُسْتَعْرِضَةً وَحْدَهَا وَصَدًى وَاحِدًا وَاضِحًا. وَالزَّاوِيَةُ المَكْتُوبَةُ عَلَى المِجَسِّ، خَمْسٌ وَأَرْبَعُونَ أَوْ سِتُّونَ أَوْ سَبْعُونَ دَرَجَةً، هِيَ زَاوِيَةُ المُسْتَعْرِضَةِ فِي الفُولَاذِ.",
    # 4  §4 exit point, range and angle check
    "لِنَجِدَ نُقْطَةَ الخُرُوجِ نُحَرِّكُ المِجَسَّ المَائِلَ عَلَى الكُتْلَةِ حَتَّى يَبْلُغَ صَدَى القَوْسِ أَقْصَاهُ، فَتَكُونُ نُقْطَةُ الخُرُوجِ فَوْقَ مَرْكَزِ القَوْسِ، وَنُعَلِّمُهَا عَلَى المِجَسِّ. وَلِمُعَايَرَةِ المَدَى نَجْعَلُ صَدَى القَوْسِ عِنْدَ مِئَةِ مِلِّيمِتْرٍ عَلَى الشَّاشَةِ. وَلِلتَّحَقُّقِ مِنَ الزَّاوِيَةِ نُحَرِّكُ المِجَسَّ حَتَّى يَبْلُغَ صَدَى الثَّقْبِ المَرْجِعِيِّ أَقْصَاهُ، ثُمَّ نَقْرَأُ الزَّاوِيَةَ عَلَى تَدْرِيجِ الكُتْلَةِ عِنْدَ نُقْطَةِ الخُرُوجِ.",
    # 5  §5 sound path, skip distance and flaw location; the one worked example
    "بَعْدَ المُعَايَرَةِ تَقْرَأُ الشَّاشَةُ مَسَارَ الصَّوْتِ، وَهُوَ طُولُ الطَّرِيقِ المَائِلِ إِلَى العَاكِسِ، وَنَرْمُزُ إِلَيْهِ بِالحَرْفِ إِسْ. السَّاقُ الأُولَى مِنْ سَطْحِ المِجَسِّ إِلَى الجِدَارِ الخَلْفِيِّ، ثُمَّ تَرْتَدُّ الحُزْمَةُ صَاعِدَةً فِي السَّاقِ الثَّانِيَةِ، وَالمَسَافَةُ السَّطْحِيَّةُ لِنِهَايَةِ السَّاقَيْنِ هِيَ القَفْزَةُ الكَامِلَةُ. فِي لَوْحٍ سَمَاكَتُهُ ثَلَاثُونَ مِلِّيمِتْرًا وَمِجَسٍّ سِتِّينَ دَرَجَةً، نِصْفُ القَفْزَةِ هُوَ المَسَافَةُ عَلَى السَّطْحِ لِسَاقٍ وَاحِدَةٍ، وَالقَفْزَةُ الكَامِلَةُ ضِعْفُهَا. مِثَالٌ: صَدَى عَيْبٍ عِنْدَ مَسَارِ خَمْسِينَ مِلِّيمِتْرًا بِمِجَسٍّ سِتِّينَ دَرَجَةً. العُمْقُ يُسَاوِي المَسَارَ ضَرْبَ جَيْبِ تَمَامِ سِتِّينَ، أَيْ خَمْسِينَ ضَرْبَ نِصْفٍ، خَمْسَةً وَعِشْرِينَ مِلِّيمِتْرًا. وَالمَسَافَةُ السَّطْحِيَّةُ مِنْ نُقْطَةِ الخُرُوجِ تُسَاوِي المَسَارَ ضَرْبَ جَيْبِ سِتِّينَ، ثَلَاثَةً وَأَرْبَعِينَ فَاصِلَةً ثَلَاثَةً مِلِّيمِتْرٍ. وَالعُمْقُ أَقَلُّ مِنْ سَمَاكَةِ اللَّوْحِ، فَالعَيْبُ عَلَى السَّاقِ الأُولَى. أَمَّا فِي السَّاقِ الثَّانِيَةِ فَيُقَاسُ العُمْقُ مِنَ الجِدَارِ الخَلْفِيِّ صُعُودًا.",
    # 6  §6 the DAC curve and a glimpse of DGS
    "عَاكِسَانِ مُتَمَاثِلَانِ عَلَى عُمْقَيْنِ مُخْتَلِفَيْنِ لَا يُعْطِيَانِ صَدًى بِالِارْتِفَاعِ نَفْسِهِ، لِأَنَّ الحُزْمَةَ تَتَّسِعُ وَالمَوْجَةَ تَتَوَهَّنُ مَعَ المَسَافَةِ. لِذٰلِكَ نَبْنِي مُنْحَنًى: نُسَجِّلُ قِمَمَ أَصْدَاءِ ثُقُوبٍ جَانِبِيَّةٍ مُتَمَاثِلَةٍ عَلَى أَعْمَاقٍ مُخْتَلِفَةٍ فِي كُتْلَةٍ مَرْجِعِيَّةٍ، وَنَصِلُ بَيْنَهَا. هٰذَا مُنْحَنَى تَصْحِيحِ المَسَافَةِ وَالسَّعَةِ، وَيُخْتَصَرُ دِي إِيهْ سِي. وَبَعْدَهُ يُقَارَنُ صَدَى أَيِّ عَيْبٍ بِالمُنْحَنَى عِنْدَ عُمْقِهِ، لَا بِارْتِفَاعِهِ المُطْلَقِ. وَلَمْحَةٌ أُخْرَى: مُخَطَّطُ دِي جِي إِسْ، وَهُوَ طَرِيقَةٌ أُخْرَى لِضَبْطِ الحَسَاسِيَّةِ، يَرْبِطُ المَسَافَةَ وَالكَسْبَ وَالحَجْمَ المُكَافِئَ لِعَاكِسٍ قِيَاسِيٍّ.",
    # 7  review: intro, then (question, 3 s countdown, answer) x 8
    "نُرَاجِعُ مَا تَعَلَّمْنَاهُ بِثَمَانِيَةِ أَسْئِلَةٍ. بَعْدَ كُلِّ سُؤَالٍ ثَلَاثُ ثَوَانٍ لِتُجِيبَ بِنَفْسِكَ.",
    "مَاذَا تَفْعَلُ المُعَايَرَةُ بِالشَّاشَةِ وَبِالحَسَاسِيَّةِ؟", 3,
    "الشَّاشَةُ تَقْرَأُ مَسَافَةً صَحِيحَةً، وَالحَسَاسِيَّةُ تُضْبَطُ عَلَى مَرْجِعٍ.",
    "لِمَاذَا نَسْتَعْمِلُ أَصْدَاءً مُتَعَدِّدَةً لِلْجِدَارِ الخَلْفِيِّ؟", 3,
    "لِأَنَّهَا مُتَسَاوِيَةُ البُعْدِ، فَنَضْبِطُ عَلَيْهَا الشَّاشَةَ.",
    "مَا الزَّاوِيَةُ الحَرِجَةُ الأُولَى؟", 3,
    "زَاوِيَةُ الإِسْفِينِ الَّتِي تَخْتَفِي عِنْدَهَا الطُّولِيَّةُ مِنَ القِطْعَةِ.",
    "لِمَاذَا تُصَمَّمُ المِجَسَّاتُ المَائِلَةُ بَيْنَ الزَّاوِيَتَيْنِ الحَرِجَتَيْنِ؟", 3,
    "لِتَبْقَى مَوْجَةٌ مُسْتَعْرِضَةٌ وَحْدَهَا، فَيَظْهَرُ صَدًى وَاحِدٌ وَاضِحٌ.",
    "مَاذَا تَعْنِي الزَّاوِيَةُ المَكْتُوبَةُ عَلَى المِجَسِّ المَائِلِ؟", 3,
    "زَاوِيَةُ المَوْجَةِ المُسْتَعْرِضَةِ فِي الفُولَاذِ.",
    "كَيْفَ نُحَدِّدُ نُقْطَةَ خُرُوجِ الحُزْمَةِ؟", 3,
    "نُحَرِّكُ المِجَسَّ حَتَّى يَبْلُغَ صَدَى القَوْسِ أَقْصَاهُ.",
    "صَدَى عَيْبٍ عِنْدَ مَسَارِ خَمْسِينَ مِلِّيمِتْرًا بِمِجَسِّ سِتِّينَ دَرَجَةً فِي لَوْحٍ سَمَاكَتُهُ ثَلَاثُونَ مِلِّيمِتْرًا: مَا عُمْقُهُ، وَعَلَى أَيِّ سَاقٍ؟", 3,
    "خَمْسَةٌ وَعِشْرُونَ مِلِّيمِتْرًا، عَلَى السَّاقِ الأُولَى.",
    "لِمَاذَا لَا يَكْفِي ارْتِفَاعُ الصَّدَى لِلْحُكْمِ عَلَى العَيْبِ؟", 3,
    "الحُزْمَةُ تَتَّسِعُ وَالمَوْجَةُ تَتَوَهَّنُ؛ فَنُقَارِنُ بِمُنْحَنَى دِي إِيهْ سِي.",
]

# Every spoken or shown value is checked against the data module; stop if it drifts.
assert [f"{a:.1f}" for a in (D.CRIT_1, D.CRIT_2)] == ["27.5", "57.1"]               # seg 3 (about 27.5 and about 57)
assert D.CRIT_1 < 45 < 60 < 70 and D.CRIT_2 < 90                                    # seg 3
assert f"{D.DEPTH:.1f}" == "25.0" and f"{D.SURFACE_DIST:.1f}" == "43.3"             # seg 5, review Q7
assert D.DEPTH < D.PLATE_T and int(D.PLATE_T) == 30 and int(D.PATH_S) == 50         # seg 5, review Q7
assert D.V1_ECHOES == [25.0, 50.0, 75.0, 100.0] and int(D.V1_QUADRANT_R) == 100     # seg 2, 4

AUDIO_DIR = audio_dir_for(__file__)

# Colour roles of this project (project CLAUDE.md): ACCENT_1 sound / probe / incident wave,
# ACCENT_2 reflected wave / echo, ACCENT_3 transmitted wave / OK, ACCENT_4 flaw / alarm.


# ---- Segment 1 helpers: the instrument screen, the knob, the worn wedge ----
def knob(caption, size=0.55, color=INK):
    """A round knob with a pointer (`pointer` turns with `set_turn(0..1)`) and a caption below."""
    ring = Circle(radius=size, color=color, stroke_width=4).set_fill(PANEL_FILL, 1)
    ptr = Line(ORIGIN, UP * size * 0.8, color=ACCENT_2, stroke_width=5)
    cap = label(caption, FS_TAG, INK, weight=BOLD).next_to(ring, DOWN, 0.12)
    g = VGroup(ring, ptr, cap)
    g.ring, g.pointer, g.caption, g.size = ring, ptr, cap, size

    def set_turn(v):
        a = PI * 0.75 - v * PI * 1.5            # sweeps from the lower left to the lower right
        c0 = ring.get_center()
        ptr.put_start_and_end_on(c0, c0 + size * 0.8 * np.array([np.cos(a), np.sin(a), 0]))
        return g
    g.set_turn = set_turn
    set_turn(0.5)
    return g


def small_scan(center, peaks, width=6.0, height=2.3, t_max=110.0, ticks=(0, 25, 50, 75, 100), sigma=0.9,
               x_caption="Distance (mm)", y_caption="Echo amplitude"):
    """An AScan placed with its frame centred on `center`, its trace fully drawn (`trace` is not added)."""
    sc = AScan(peaks, width=width, height=height, t_min=-6.0, t_max=t_max, ticks=ticks, sigma=sigma,
               x_caption=x_caption, y_caption=y_caption)
    sc.shift(np.array([center[0], center[1], 0.0]) - sc.frame.get_center())
    sc.update_trace(sc.t_max)
    return sc


# ---- Segment 2 helpers: the V1 block ----
V1_SCALE = 0.027         # units per mm (300 mm long, 100 mm high)


class V1Block(VGroup):
    """The IIW V1 calibration block seen from the side (a simplified drawing of TCS-67 Fig. 5.1), its
    top surface at height `y_top`, its left end at `x0`: the 100 mm quadrant (centre P = the beam exit
    point on the top surface), the 50 mm hole with its plastic insert, the 1.5 mm hole and the angle
    scale. Parts: body, arc, hole_big, insert, hole_small, scale (ticks), P (point), top, bottom;
    `scale_x(angle)` is the x of an angle tick on the top surface."""

    def __init__(self, x0=-6.4, y_top=1.3, s=V1_SCALE):
        self.s, self.x0, self.y_top = s, x0, y_top
        L, H = 300 * s, 100 * s
        R = D.V1_QUADRANT_R * s
        self.P = np.array([x0 + R, y_top, 0.0])
        self.bottom = y_top - H
        pts = [[x0, y_top, 0], [x0 + L, y_top, 0], [x0 + L, y_top - H, 0], [x0 + R, y_top - H, 0]]
        arc = Arc(radius=R, start_angle=-PI / 2, angle=-PI / 2, arc_center=self.P, color=INK, stroke_width=4)
        body_pts = [np.array(p, dtype=float) for p in pts] + list(arc.points[::6]) + [np.array([x0, y_top, 0.0])]
        self.body = VMobject(color=INK, stroke_width=4).set_points_as_corners(body_pts).set_fill(PANEL_FILL, 1)
        self.arc = arc
        hx = x0 + 215 * s
        hy = y_top - 50 * s
        self.hole_big = Circle(radius=25 * s, color=INK, stroke_width=3).set_fill(BG, 1).move_to([hx, hy, 0])
        self.insert = Circle(radius=25 * s * 0.55, color=ACCENT_1, stroke_width=3).set_fill(ACCENT_1, 0.25).move_to([hx, hy, 0])
        self.hole_x = x0 + 60 * s
        self.hole_small = Dot([self.hole_x, y_top - 30 * s, 0], radius=0.06, color=INK)
        ticks = VGroup()
        self._tick_x = {}
        for k, ang in enumerate((40, 45, 50, 55, 60, 65, 70)):
            x = self.hole_x + 30 * np.tan(np.radians(ang)) * s        # the exit point whose beam meets the small hole
            self._tick_x[ang] = x
            major = ang % 10 == 0
            ticks.add(Line([x, y_top, 0], [x, y_top - (0.2 if major else 0.12), 0], color=INK, stroke_width=3))
        self.scale = ticks
        self.top = Line([x0, y_top, 0], [x0 + L, y_top, 0], color=INK, stroke_width=4)
        super().__init__(self.body, self.hole_big, self.insert, self.hole_small, ticks)

    def scale_x(self, angle):
        return self._tick_x[angle]

    def tick_label(self, angle):
        return label(f"{angle}", FS_TAG - 4, INK).move_to([self._tick_x[angle], self.y_top - 0.38, 0])


def wedge_probe(x_exit, y_top, facing=1, color=ACCENT_1, size=1.0):
    """An angle probe: a plastic wedge whose front (the exit point) is at x_exit on the surface y_top,
    with the crystal on its slanted back. facing = 1: the beam goes to the right.
    Returns VGroup(wedge, crystal) with .exit (point)."""
    w, h = 0.9 * size, 0.55 * size
    pts = [[x_exit, y_top, 0], [x_exit - facing * w, y_top, 0], [x_exit - facing * w, y_top + h, 0]]
    wedge = Polygon(*pts, color=GREY_INK, stroke_width=3).set_fill(color, 0.18)
    crystal = Line(pts[1], pts[2], color=color, stroke_width=8)
    g = VGroup(wedge, crystal)
    g.exit = np.array([x_exit, y_top, 0.0])
    g.wedge, g.crystal = wedge, crystal
    return g


# ---- Segment 3 helpers: refraction at a perspex-steel interface ----
class Refraction(VGroup):
    """A longitudinal wave in perspex hitting a steel interface at height `y0` at point (x0, y0): the
    incident ray, the refracted longitudinal ray (ACCENT_3), the refracted shear ray (ACCENT_2) and the
    surface wave that remains after the second critical angle. `set_alpha(deg)` redraws them with Snell's
    law and the velocities of the data module. A refracted ray is hidden once its angle would pass 90 degrees."""

    def __init__(self, x0=-2.8, y0=0.4, length=2.6):
        self.x0, self.y0, self.L = x0, y0, length
        self.alpha = 0.0
        self.show_inc, self.show_l, self.show_s = False, False, False   # the scene switches them on at their cues
        self.inc = Line(ORIGIN, RIGHT, color=ACCENT_1, stroke_width=6)
        self.crystal = Line(ORIGIN, RIGHT, color=ACCENT_1, stroke_width=10)
        self.rl = Line(ORIGIN, RIGHT, color=ACCENT_3, stroke_width=6)
        self.rs = Line(ORIGIN, RIGHT, color=ACCENT_2, stroke_width=6)
        self.surf = ParametricFunction(lambda t: np.array([x0 + t, y0 + 0.07 * np.sin(9 * t), 0.0]),
                                       t_range=[0, 2.3], color=ACCENT_2, stroke_width=5)
        self.normal = DashedLine([x0, y0 + 2.2, 0], [x0, y0 - 2.5, 0], color=GREY_INK, stroke_width=2)
        super().__init__(self.normal, self.surf, self.rl, self.rs, self.inc, self.crystal)
        self.set_alpha(15.0)

    def _ray(self, line, ang_deg, side, visible, length):
        """Set `line` from the interface point along `ang_deg` from the normal (side = +1 steel / -1 perspex)."""
        a = np.radians(ang_deg)
        d = np.array([np.sin(a), side * np.cos(a), 0.0])
        p0 = np.array([self.x0, self.y0, 0.0])
        if side < 0:                                   # the incident ray comes from the upper left
            line.put_start_and_end_on(p0 + np.array([-np.sin(a), np.cos(a), 0.0]) * length, p0)
        else:
            line.put_start_and_end_on(p0, p0 + d * length)
        line.set_stroke(opacity=1.0 if visible else 0.0)

    def set_alpha(self, deg):
        self.alpha = deg
        a = np.radians(deg)
        sin_l = np.sin(a) * D.V_L_STEEL / D.V_L_PERSPEX
        sin_s = np.sin(a) * D.V_S_STEEL / D.V_L_PERSPEX
        self._ray(self.inc, deg, -1, self.show_inc, self.L)
        # the crystal: a short bar across the incident ray at its far end
        s = self.inc.get_start()
        perp = np.array([np.cos(a), np.sin(a), 0.0])
        self.crystal.put_start_and_end_on(s - perp * 0.35, s + perp * 0.35)
        self.crystal.set_stroke(opacity=1.0 if self.show_inc else 0.0)
        self.normal.set_stroke(opacity=1.0 if self.show_inc else 0.0)
        vis_l, vis_s = sin_l < 0.999, sin_s < 0.999
        shown_l, shown_s = vis_l and self.show_l, vis_s and self.show_s
        self._ray(self.rl, np.degrees(np.arcsin(min(sin_l, 1.0))), +1, shown_l, self.L)
        self._ray(self.rs, np.degrees(np.arcsin(min(sin_s, 1.0))), +1, shown_s, self.L * 0.9)
        self.surf.set_stroke(opacity=1.0 if (self.show_s and not vis_s) else 0.0)
        return self

    def beta_l(self):
        return float(np.degrees(np.arcsin(min(np.sin(np.radians(self.alpha)) * D.V_L_STEEL / D.V_L_PERSPEX, 1.0))))

    def beta_s(self):
        return float(np.degrees(np.arcsin(min(np.sin(np.radians(self.alpha)) * D.V_S_STEEL / D.V_L_PERSPEX, 1.0))))


class AngleGauge(VGroup):
    """A horizontal 0-90 degree bar with the two critical marks, the band between them, and a pointer
    (`set_alpha`). Parts: bar, ends, pointer, band, mark_1, mark_2 (lines)."""

    def __init__(self, x0=2.7, x1=6.5, y=-0.9):
        self.x0, self.x1, self.y = x0, x1, y
        self.k = (x1 - x0) / 90.0
        self.bar = Line([x0, y, 0], [x1, y, 0], color=INK, stroke_width=5)
        self.ends = VGroup(label("0°", FS_TAG - 2, GREY_INK).move_to([x0, y - 0.3, 0]),
                           label("90°", FS_TAG - 2, GREY_INK).move_to([x1, y - 0.3, 0]))
        self.pointer = Triangle(color=INK, stroke_width=2).set_fill(INK, 1).scale(0.13).rotate(PI)
        xa, xb = self.x_of(D.CRIT_1), self.x_of(D.CRIT_2)
        self.band = Rectangle(width=xb - xa, height=0.32, color=OK_C, stroke_width=0).set_fill(OK_C, 0.3)
        self.band.move_to([(xa + xb) / 2, y + 0.16, 0])
        self.mark_1 = Line([xa, y - 0.12, 0], [xa, y + 0.45, 0], color=ACCENT_3, stroke_width=4)
        self.mark_2 = Line([xb, y - 0.12, 0], [xb, y + 0.45, 0], color=ACCENT_2, stroke_width=4)
        super().__init__(self.bar, self.ends, self.band, self.mark_1, self.mark_2, self.pointer)
        self.set_alpha(15.0)

    def x_of(self, deg):
        return self.x0 + self.k * deg

    def set_alpha(self, deg):
        self.pointer.move_to([self.x_of(deg), self.y + 0.3 + 0.26, 0])
        return self


# HELPERS-END


class UtSeriesEp03(SyncedScene):
    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        self.seg1()
        self.seg2()
        self.seg3()
        self.seg4()
        self.seg5()
        self.seg6()
        self.seg7()

    # ---------------- Segment 1: why calibrate (§5.1, §5.3) ----------------
    def seg1(self):
        c = lambda phrase, nth=1: self.cue(1, phrase, nth)
        S = self.start(1)
        title_card(self, "Ultrasonic Testing", "Calibration and angle-beam testing",
                   series="Ultrasonic Testing Series · Episode 3", run_time=1.6)
        self.sync(c("وَالمُعَايَرَةُ") - 0.1)
        self.clear(run_time=0.5)

        # ---- the instrument reads a time; calibration makes it read a distance, and sets the gain ----
        PEAKS_T = [(0.0, 1.3), (4.0, 0.45), (8.4, 0.9)]
        scan = AScan(PEAKS_T, width=7.4, height=3.0, t_min=-0.6, t_max=10.0, ticks=(0, 2, 4, 6, 8, 10),
                     x_caption="Time (µs)", y_caption="Echo amplitude")
        scan.shift(np.array([-1.2, 0.5, 0.0]) - scan.frame.get_center())
        tr = ValueTracker(0.0)                                  # gain: 0 (weak flaw echo) .. 1 (at the reference line)
        scan.trace.add_updater(lambda m: (setattr(scan, "peaks", [(0.0, 1.3), (4.0, 0.45 + 1.0 * tr.get_value()),
                                                                   (8.4, 0.9 + 0.2 * tr.get_value())]),
                                          scan.update_trace(scan.t_max)))
        ref_y = scan.y_base() + 1.45
        ref_line = DashedLine([scan.frame.get_left()[0] + 0.5, ref_y, 0], [scan.frame.get_right()[0] - 0.3, ref_y, 0],
                              color=ACCENT_3, stroke_width=3)
        ref_lab = label("reference level", FS_TAG, ACCENT_3, weight=BOLD).next_to(ref_line, UP, 0.08).align_to(ref_line, RIGHT)
        gain = knob("Gain").move_to([5.6, 1.4, 0])
        gain.set_turn(0.2)
        self.sync(S + 2.1)
        self.play(FadeIn(scan), run_time=0.7)
        self.add(scan.trace)
        self.sync(c("تَقْرَأُ"))
        new_ticks = VGroup(*[label(t, FS_TAG - 2, GREY_INK).move_to(old.get_center())
                             for t, old in zip(("0", "10", "20", "30", "40", "50"), scan.tick_labels)])
        new_cap = label("Distance (mm)", FS_TAG, INK).move_to(scan.x_caption).align_to(scan.x_caption, RIGHT)
        self.play(FadeOut(scan.tick_labels), FadeOut(scan.x_caption), run_time=0.4)
        self.play(FadeIn(new_ticks), FadeIn(new_cap), run_time=0.5)
        self.sync(c("وَتَضْبِطُ"))
        self.play(FadeIn(gain), FadeIn(ref_line), FadeIn(ref_lab), run_time=0.5)
        self.sync(c("حَسَاسِيَّتَهُ") + 0.2)
        self.play(tr.animate(run_time=1.6).set_value(1.0), UpdateFromAlphaFunc(
            gain, lambda m, a: m.set_turn(0.2 + 0.5 * a)))
        scan.trace.clear_updaters()

        # ---- the four instrument checks ----
        self.sync(c("وَنَتَحَقَّقُ") - 0.2)
        self.clear(run_time=0.5)
        PW = 6.0
        pos = {"h": (-3.65, 1.55), "v": (3.65, 1.55), "r": (-3.65, -1.85), "d": (3.65, -1.85)}

        def panel_title(key, text):
            x, y = pos[key]
            return label(text, FS_NOTE, INK, weight=BOLD).move_to([x, y + 1.38, 0])

        # 1. horizontal linearity: equally spaced echoes
        sh = small_scan(pos["h"], [(0, 1.3), (25, 1.0), (50, 0.8), (75, 0.62), (100, 0.5)], width=PW, height=2.0)
        th = panel_title("h", "Horizontal linearity")
        guides = VGroup(*[DashedLine([sh.x_of(v), sh.y_base() - 0.05, 0], [sh.x_of(v), sh.y_base() + 1.5, 0],
                                     color=ACCENT_3, stroke_width=2) for v in (25, 50, 75, 100)])
        ok_h = tag_line("equal spacing", "check", OK_C, width=3.2, size=FS_TAG).move_to([pos["h"][0] + 1.4, pos["h"][1] + 0.55, 0])
        # 2. vertical linearity: heights in proportion
        sv = small_scan(pos["v"], [(0, 1.3), (35, 1.2), (70, 0.6)], width=PW, height=2.0)
        tv = panel_title("v", "Vertical linearity")
        ok_v = tag_line("height follows amplitude", "check", OK_C, width=3.8, size=FS_TAG).move_to([pos["v"][0] + 1.0, pos["v"][1] + 0.55, 0])
        ratio = label("2 : 1", FS_NOTE, ACCENT_2, weight=BOLD).move_to([sv.x_of(35) + 0.7, sv.y_base() + 1.0, 0])
        # 3. resolution: two close reflectors, merged then resolved
        sg = ValueTracker(4.0)
        sr = small_scan(pos["r"], [(0, 1.3), (85, 1.0), (92, 0.95)], width=PW, height=2.0, sigma=4.0)
        tr_ = panel_title("r", "Resolution")
        sr.trace.add_updater(lambda m: (setattr(sr, "sigma", sg.get_value()), sr.update_trace(sr.t_max)))
        res_t = tag_line("two close reflectors told apart", "check", OK_C, width=4.6, size=FS_TAG).move_to([pos["r"][0] + 0.2, pos["r"][1] + 0.62, 0])
        # 4. dead zone: the initial pulse hides a near-surface echo
        sd = small_scan(pos["d"], [(0, 1.4), (7, 0.55), (45, 1.0)], width=PW, height=2.0, sigma=4.5)
        td = panel_title("d", "Dead zone")
        dz = Rectangle(width=sd.x_of(14) - sd.x_of(-4), height=1.5, color=ACCENT_4, stroke_width=0).set_fill(ACCENT_4, 0.15)
        dz.move_to([(sd.x_of(14) + sd.x_of(-4)) / 2, sd.y_base() + 0.7, 0])
        hid = label("echo hidden", FS_TAG, ACCENT_4, weight=BOLD).move_to([sd.x_of(30), sd.y_base() + 1.3, 0])

        self.sync(c("الخَطِّيَّةُ"))
        self.play(FadeIn(sh), FadeIn(sh.trace), FadeIn(th), run_time=0.6)
        self.sync(c("تَنَاسُبُ"))
        self.play(Create(guides), run_time=0.7)
        self.play(FadeIn(ok_h), run_time=0.3)
        self.sync(c("وَالخَطِّيَّةُ"))
        self.play(FadeIn(sv), FadeIn(sv.trace), FadeIn(tv), run_time=0.6)
        self.sync(c("ارْتِفَاعِ"))
        self.play(FadeIn(ratio), FadeIn(ok_v), run_time=0.5)
        self.sync(c("وَالتَّمْيِيزُ"))
        self.play(FadeIn(sr), FadeIn(tr_), run_time=0.5)
        self.add(sr.trace)
        self.sync(c("فَصْلُ"))
        self.play(sg.animate(run_time=1.5).set_value(0.9))
        sr.trace.clear_updaters()
        self.play(FadeIn(res_t), run_time=0.3)
        self.sync(c("وَالمِنْطَقَةُ"))
        self.play(FadeIn(sd), FadeIn(sd.trace), FadeIn(td), run_time=0.6)
        self.sync(c("تُخْفِي"))
        self.play(FadeIn(dz), FadeIn(hid), run_time=0.5)

        # ---- a worn wedge changes the exit point and the angle ----
        self.sync(c("وَنُعِيدُ") - 0.3)
        self.clear(run_time=0.5)
        top_y = -0.3
        plate = SteelBlock(9.0, 2.0).move_to([0, top_y - 1.0, 0])
        w_new = wedge_probe(-1.2, top_y, size=1.5)
        w_old_pts = [[-1.2, top_y, 0], [-2.55, top_y, 0], [-2.55, top_y + 0.82, 0]]
        idx_new = Triangle(color=ACCENT_2, stroke_width=2).set_fill(ACCENT_2, 1).scale(0.12).rotate(PI).move_to([-1.2, top_y + 0.17, 0])
        idx_lab = label("exit point (index)", FS_TAG, ACCENT_2, weight=BOLD).next_to(idx_new, UP, 0.3).shift(RIGHT * 0.9)
        beam = DashedLine([-1.2, top_y, 0], [1.6, top_y - 1.6, 0], color=ACCENT_1, stroke_width=3)
        self.sync(c("وَنُعِيدُ"))
        self.play(Create(plate), FadeIn(w_new), run_time=0.7)
        self.play(FadeIn(idx_new), FadeIn(idx_lab), Create(beam), run_time=0.6)
        self.sync(c("البِلَى"))
        worn = Polygon([-1.5, top_y, 0], [-2.55, top_y, 0], [-2.55, top_y + 0.82, 0], color=GREY_INK,
                       stroke_width=3).set_fill(ACCENT_1, 0.18)
        beam2 = DashedLine([-1.5, top_y, 0], [1.6, top_y - 1.45, 0], color=ACCENT_1, stroke_width=3)
        self.play(Transform(w_new.wedge, worn), idx_new.animate.shift(LEFT * 0.3),
                  Transform(beam, beam2), run_time=1.0)
        shift_lab = label("wear moves the exit point and changes the angle", FS_NOTE, ALERT_C, weight=BOLD)
        shift_lab.move_to([0, 2.3, 0])
        self.play(FadeIn(shift_lab), run_time=0.5)
        self.sync(self.end(1))
        self.clear()

    # ---------------- Segment 2: the V1 block and the time base (§5.2.1, §5.4) ----------------
    def seg2(self):
        c = lambda phrase, nth=1: self.cue(2, phrase, nth)
        S = self.start(2)
        # ---- the block and its features, each named when it is spoken ----
        v1 = V1Block(x0=-6.4, y_top=1.3)
        name = label("IIW V1 block", FS_LABEL, INK, weight=BOLD).move_to([-2.4, 3.2, 0])
        depth = np.array([0.5, 0.35, 0.0])                       # the oblique depth (the 25 mm thickness)
        back = VGroup(*[Line(p, p + depth, color=GREY_INK, stroke_width=3) for p in
                        (np.array([-6.4, 1.3, 0.0]), np.array([-6.4 + 300 * V1_SCALE, 1.3, 0.0]),
                         np.array([-6.4 + 300 * V1_SCALE, 1.3 - 100 * V1_SCALE, 0.0]))])
        back_top = Line(np.array([-6.4, 1.3, 0.0]) + depth, np.array([-6.4 + 300 * V1_SCALE, 1.3, 0.0]) + depth,
                        color=GREY_INK, stroke_width=3)
        back_side = Line(np.array([-6.4 + 300 * V1_SCALE, 1.3, 0.0]) + depth,
                         np.array([-6.4 + 300 * V1_SCALE, 1.3 - 100 * V1_SCALE, 0.0]) + depth, color=GREY_INK, stroke_width=3)
        dim25 = DoubleArrow(np.array([-6.4 + 300 * V1_SCALE + 0.15, 1.3 - 0.0, 0.0]),
                            np.array([-6.4 + 300 * V1_SCALE + 0.15, 1.3, 0.0]) + depth, buff=0, color=ACCENT_3,
                            stroke_width=3, tip_length=0.12)
        lab25 = label(f"{D.V1_THICKNESS:.0f} mm", FS_TAG, ACCENT_3, weight=BOLD).next_to(dim25, RIGHT, 0.1)

        def call(text, target, color, dx, dy):
            lab = label(text, FS_TAG, color, weight=BOLD).move_to(np.array(target) + np.array([dx, dy, 0.0]))
            lead = Line(lab.get_edge_center(DOWN if dy > 0 else UP) + (UP * 0.04 if dy < 0 else DOWN * 0.04), target,
                        color=color, stroke_width=2)
            return VGroup(lab, lead)
        self.sync(S + 0.1)
        self.play(FadeIn(name), Create(v1.body), run_time=0.8)
        self.sync(c("سَمَاكَتُهَا"))
        self.play(Create(back), Create(back_top), Create(back_side), Create(dim25), FadeIn(lab25), run_time=0.8)
        self.sync(c("قَوْسٌ"))
        arc_hl = v1.arc.copy().set_color(ACCENT_2).set_stroke(width=7)
        arc_c = call(f"{D.V1_QUADRANT_R:.0f} mm quadrant", [v1.x0 + 0.4, v1.bottom + 0.55, 0.0], ACCENT_2, -0.2, -1.4)
        self.play(Create(arc_hl), FadeIn(arc_c), run_time=0.7)
        self.sync(c("وَثَقْبٌ"))
        hs = v1.hole_small
        hs_c = call(f"{D.V1_HOLE_D:g} mm hole", hs.get_center(), ACCENT_4, 0.0, -1.0)
        self.play(Indicate(hs, color=ACCENT_4, scale_factor=3), FadeIn(hs_c), run_time=0.7)
        self.sync(c("كَبِيرٌ"))
        hb_c = call("large hole with a plastic insert", v1.hole_big.get_bottom(), ACCENT_1, -0.3, -0.75)
        self.play(Indicate(v1.insert, color=ACCENT_1, scale_factor=1.2), FadeIn(hb_c), run_time=0.7)
        self.sync(c("وَتَدْرِيجٌ"))
        tick_lbs = VGroup(*[v1.tick_label(a) for a in (40, 50, 60, 70)])
        sc_c = call("angle scale", [v1.scale_x(50), v1.y_top, 0.0], INK, 0.0, 0.8)
        self.play(Indicate(v1.scale, color=INK), FadeIn(tick_lbs), FadeIn(sc_c), run_time=0.7)

        # ---- the normal probe across the thickness: the sound bounces between the faces ----
        self.sync(c("نَضَعُ") - 0.3)
        self.clear(run_time=0.5)
        PX, PY, PW_, PH_ = -5.0, 0.2, 1.5, 3.2                   # the 25 mm thickness drawn large (a section)
        sect = SteelBlock(PW_, PH_).move_to([PX, PY, 0])
        probe = Probe().rotate(PI / 2).next_to(sect, LEFT, 0.0)
        sect_t = label(f"{D.V1_THICKNESS:.0f} mm", FS_NOTE, ACCENT_3, weight=BOLD).next_to(sect, DOWN, 0.2)
        dimw = DoubleArrow(sect.get_corner(DL) + DOWN * 0.15, sect.get_corner(DR) + DOWN * 0.15, buff=0, color=ACCENT_3,
                           stroke_width=3, tip_length=0.12)
        sect_t.next_to(dimw, DOWN, 0.08)
        # the screen (distance axis 0-100 mm)
        ECH = list(D.V1_ECHOES)
        g = ValueTracker(0.0)                        # 0: mis-set screen, 1: calibrated
        pos_before = [10 + 20 * (k + 1) for k in range(4)]                  # equal spacing, wrong scale and offset
        heights = [1.35, 1.05, 0.8, 0.6]
        scr = AScan([(0.0, 1.5)], width=7.0, height=2.9, t_min=-6.0, t_max=110.0, ticks=(0, 25, 50, 75, 100),
                    sigma=0.9, x_caption="Distance (mm)", y_caption="Echo amplitude")
        scr.shift(np.array([1.8, 1.3, 0.0]) - scr.frame.get_center())
        scr.trace.add_updater(lambda m: (setattr(scr, "peaks", [(0.0, 1.5)] + [
            ((1 - g.get_value()) * b + g.get_value() * e, h) for b, e, h in zip(pos_before, ECH, heights)][:int(shown.get_value())]),
            scr.update_trace(scr.t_max)))
        shown = ValueTracker(0.0)                    # how many back-wall echoes are on the screen
        self.sync(c("نَضَعُ"))
        self.play(Create(sect), FadeIn(probe), Create(dimw), FadeIn(sect_t), FadeIn(scr), run_time=0.7)
        self.add(scr.trace)
        # bounces
        self.sync(c("فَيَرْتَدُّ"))
        bx = lambda k: PX + (PW_ / 2 - 0.35) * (1 if k % 2 == 0 else -1)
        for k in range(4):
            amp = 0.3 * (0.8 ** k)
            p_ = wavefront(length=0.5, amp=amp + 0.12, cycles=4, color=ACCENT_1 if k % 2 == 0 else ACCENT_2,
                           direction=RIGHT if k % 2 == 0 else LEFT)
            x0 = PX - PW_ / 2 + 0.3 if k % 2 == 0 else PX + PW_ / 2 - 0.3
            x1 = PX + PW_ / 2 - 0.3 if k % 2 == 0 else PX - PW_ / 2 + 0.3
            p_.move_to([x0, PY + 0.6 - 0.4 * k, 0])
            self.add(p_)
            self.play(p_.animate(run_time=0.55, rate_func=linear).move_to([x1, PY + 0.6 - 0.4 * k, 0])
                      .set_stroke(opacity=0.9 - 0.2 * k))
            self.remove(p_)
            self.play(shown.animate(run_time=0.2).set_value(k + 1))
        self.sync(c("وَيَضْعُفُ"))
        weak = tag_line("each echo weaker than the last", "alert-triangle", ALERT_C, width=5.0)
        weak.next_to(scr, DOWN, 0.9).align_to(scr.frame, LEFT)
        self.play(FadeIn(weak), run_time=0.4)
        # ---- delay and range: the echoes are set on 25, 50, 75, 100 ----
        self.sync(c("نَضْبِطُ"))
        k_delay = knob("Delay").move_to([-0.8, -2.2, 0])
        k_range = knob("Range").move_to([0.9, -2.2, 0])
        self.play(FadeOut(weak), FadeIn(k_delay), FadeIn(k_range), run_time=0.4)
        self.sync(c("حَتَّى"))
        self.play(g.animate(run_time=2.4, rate_func=smooth).set_value(1.0),
                  UpdateFromAlphaFunc(k_delay, lambda m, a: m.set_turn(0.3 + 0.2 * a)),
                  UpdateFromAlphaFunc(k_range, lambda m, a: m.set_turn(0.7 - 0.3 * a)))
        scr.trace.clear_updaters()
        scr.peaks = [(0.0, 1.5)] + list(zip(ECH, heights))
        scr.update_trace(scr.t_max)
        marks = VGroup(*[DashedLine([scr.x_of(v), scr.y_base() - 0.05, 0], [scr.x_of(v), scr.y_base() + 1.7, 0],
                                    color=ACCENT_3, stroke_width=2) for v in ECH])
        self.play(Create(marks), run_time=0.5)
        # ---- equal spacing also checks the horizontal linearity ----
        self.sync(c("وَتَسَاوِي"))
        gaps = VGroup(*[DoubleArrow([scr.x_of(a_), scr.y_base() + 1.95, 0], [scr.x_of(b_), scr.y_base() + 1.95, 0], buff=0,
                                    color=ACCENT_3, stroke_width=3, tip_length=0.1)
                        for a_, b_ in zip([0] + ECH[:-1], ECH)])
        eq = tag_line("equal spacing: horizontal linearity", "check", OK_C, width=5.6)
        eq.next_to(scr, DOWN, 0.9).align_to(scr.frame, LEFT)
        self.play(Create(gaps), run_time=0.6)
        self.play(FadeIn(eq), run_time=0.4)
        self.sync(self.end(2))
        self.clear()

    # ---------------- Segment 3: refraction and the two critical angles (§2.4.2) ----------------
    def seg3(self):
        c = lambda phrase, nth=1: self.cue(3, phrase, nth)
        S = self.start(3)
        X0, Y0 = -2.9, 0.5
        # the two media: perspex wedge above, steel below
        perspex = Rectangle(width=7.0, height=2.9, color=INK, stroke_width=3).set_fill(ACCENT_1, 0.1)
        perspex.move_to([X0 + 0.3, Y0 + 1.45, 0])
        steel = Rectangle(width=7.0, height=3.6, color=INK, stroke_width=3).set_fill(PANEL_FILL, 1)
        steel.move_to([X0 + 0.3, Y0 - 1.8, 0])
        p_lab = label("Perspex wedge", FS_NOTE, GREY_INK, weight=BOLD).move_to([X0 - 1.9, Y0 + 2.45, 0])
        s_lab = label("Steel", FS_NOTE, GREY_INK, weight=BOLD).move_to([X0 - 2.6, Y0 - 3.15, 0])
        rf = Refraction(X0, Y0)
        rf.set_alpha(15.0)
        gauge = AngleGauge(2.9, 6.5, y=-0.9)
        g_head = label("Wedge angle", FS_NOTE, INK, weight=BOLD).move_to([4.7, -0.1, 0])
        al = ValueTracker(15.0)
        rf.add_updater(lambda m: m.set_alpha(al.get_value()))
        gauge.add_updater(lambda m: m.set_alpha(al.get_value()))
        legend = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=ACCENT_1, stroke_width=6), label("incident longitudinal", FS_TAG, INK)).arrange(RIGHT, buff=0.15),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=ACCENT_3, stroke_width=6), label("refracted longitudinal", FS_TAG, INK)).arrange(RIGHT, buff=0.15),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=ACCENT_2, stroke_width=6), label("refracted shear", FS_TAG, INK)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.7, 2.7, 0])

        self.sync(S + 0.1)
        self.play(FadeIn(perspex), FadeIn(steel), FadeIn(p_lab), FadeIn(s_lab), run_time=0.6)
        # ---- 1.4-14 s: refraction and mode conversion ----
        self.sync(c("بِزَاوِيَةٍ"))
        rf.show_inc = True
        rf.set_alpha(15.0)
        self.add(rf)
        self.play(FadeIn(legend[0]), run_time=0.5)
        a15 = np.radians(15)
        fly(self, wavefront(length=0.5, amp=0.3, cycles=4, color=ACCENT_1, direction=np.array([np.sin(a15), -np.cos(a15), 0])),
            rf.inc.get_start() + (rf.inc.get_end() - rf.inc.get_start()) * 0.15,
            rf.inc.get_start() + (rf.inc.get_end() - rf.inc.get_start()) * 0.9, 0.7)
        self.sync(c("طُولِيَّةٍ"))
        rf.show_l = True
        self.play(FadeIn(legend[1]), Indicate(rf.rl, color=ACCENT_3, scale_factor=1.0), run_time=0.7)
        self.sync(c("مُسْتَعْرِضَةٍ"))
        rf.show_s = True
        self.play(FadeIn(legend[2]), Indicate(rf.rs, color=ACCENT_2, scale_factor=1.0), run_time=0.7)
        self.sync(c("وَالطُّولِيَّةُ"))
        self.play(FadeIn(gauge), FadeIn(g_head), run_time=0.5)
        bend = label("the longitudinal ray bends more: it is faster", FS_TAG, ACCENT_3, weight=BOLD)
        bend.move_to([X0 + 0.4, Y0 - 3.45, 0])
        self.sync(c("أَسْرَعُ") - 0.6)
        self.play(FadeIn(bend), run_time=0.4)
        # ---- 14.3-21 s: the wedge angle grows until the longitudinal ray leaves ----
        self.sync(c("بِزِيَادَةِ"))
        self.play(FadeOut(bend), al.animate(run_time=c("تِسْعِينَ") + 0.6 - self.renderer.time, rate_func=linear)
                  .set_value(D.CRIT_1 + 0.3))
        self.sync(c("هٰذِهِ"))
        lab1 = label("first critical angle", FS_TAG, ACCENT_3, weight=BOLD).move_to([gauge.x_of(D.CRIT_1) - 0.5, -0.45, 0])
        self.play(FadeIn(lab1), Flash(gauge.mark_1, color=ACCENT_3, flash_radius=0.4, line_length=0.12), run_time=0.6)
        self.sync(c("سَبْعَةٍ"))
        v1 = label(f"≈ {D.CRIT_1:.1f}°", FS_LABEL, ACCENT_3, weight=BOLD).move_to([gauge.x_of(D.CRIT_1) - 0.3, -1.6, 0])
        self.play(FadeIn(v1), run_time=0.4)
        # ---- 29.6-34 s: only the shear wave remains ----
        self.sync(c("وَبَعْدَهَا"))
        self.play(al.animate(run_time=3.0, rate_func=smooth).set_value(42.0))
        only = label("only the shear wave enters the steel", FS_TAG, ACCENT_2, weight=BOLD).move_to([X0 + 0.4, Y0 - 3.45, 0])
        self.play(FadeIn(only), run_time=0.4)
        # ---- 34.1-45 s: the shear wave leaves too: a surface wave ----
        self.sync(c("وَبِزِيَادَةٍ"))
        self.play(FadeOut(only), al.animate(run_time=c("تِسْعِينَ", 2) + 0.4 - self.renderer.time, rate_func=linear)
                  .set_value(D.CRIT_2 + 0.3))
        self.sync(c("الزَّاوِيَةُ", 2))
        lab2 = label("second critical angle", FS_TAG, ACCENT_2, weight=BOLD).move_to([gauge.x_of(D.CRIT_2) + 0.35, -0.45, 0])
        self.play(FadeIn(lab2), Flash(gauge.mark_2, color=ACCENT_2, flash_radius=0.4, line_length=0.12), run_time=0.6)
        self.sync(c("سَبْعَةٍ", 2))
        v2 = label(f"≈ {D.CRIT_2:.0f}°", FS_LABEL, ACCENT_2, weight=BOLD).move_to([gauge.x_of(D.CRIT_2) + 0.3, -1.6, 0])
        self.play(FadeIn(v2), run_time=0.4)
        self.sync(c("سَطْحِيَّةٌ"))
        surf = label("surface wave", FS_TAG, ACCENT_2, weight=BOLD).move_to([X0 + 2.1, Y0 - 0.45, 0])
        self.play(al.animate(run_time=0.8).set_value(D.CRIT_2 + 3.0), FadeIn(surf), run_time=0.8)
        # ---- 45.7-54 s: angle probes work between the two angles ----
        self.sync(c("لِهٰذَا"))
        self.play(FadeOut(surf), al.animate(run_time=1.2).set_value(45.0), run_time=1.2)
        zone = label("angle probes work here", FS_TAG, OK_C, weight=BOLD)
        zone.move_to([(gauge.x_of(D.CRIT_1) + gauge.x_of(D.CRIT_2)) / 2, -1.25, 0])
        self.sync(c("بَيْنَ"))
        self.play(FadeOut(v1), FadeOut(v2), FadeIn(zone), run_time=0.5)
        self.sync(c("وَصَدًى"))
        one = tag_line("shear wave only: one clear echo", "check", OK_C, width=5.0, size=FS_TAG)
        one.move_to([4.7, -2.7, 0])
        self.play(FadeIn(one), run_time=0.4)
        # ---- 54.6-62 s: the angle written on the probe is the shear angle in the steel ----
        self.sync(c("وَالزَّاوِيَةُ") - 0.3)
        rf.clear_updaters()
        gauge.clear_updaters()
        self.clear(run_time=0.5)
        top = 1.2
        blk = SteelBlock(8.6, 3.4).move_to([0.5, top - 1.7, 0])
        wp = wedge_probe(-1.0, top, size=1.5)
        ex = np.array([-1.0, top, 0.0])
        rays = []
        for ang, col, cue in ((45, ACCENT_1, "خَمْسٌ"), (60, ACCENT_3, "سِتُّونَ"), (70, ACCENT_2, "سَبْعُونَ")):
            a = np.radians(ang)
            end = ex + np.array([np.sin(a), -np.cos(a), 0.0]) * 3.0
            r_ = Arrow(ex, end, buff=0, color=col, stroke_width=5, tip_length=0.2)
            arc = Arc(radius=0.95, start_angle=-PI / 2, angle=a, arc_center=ex, color=col, stroke_width=3)
            lab = label(f"{ang}°", FS_LABEL, col, weight=BOLD).move_to(end + np.array([0.45, -0.1, 0.0]))
            rays.append((cue, VGroup(r_, arc, lab)))
        normal = DashedLine(ex, ex + DOWN * 2.7, color=GREY_INK, stroke_width=2)
        self.play(Create(blk), FadeIn(wp), Create(normal), run_time=0.6)
        self.sync(c("المَكْتُوبَةُ"))
        written = label("angle written on the probe", FS_NOTE, INK, weight=BOLD).move_to([-3.6, top + 0.9, 0])
        self.play(FadeIn(written), run_time=0.4)
        for cue, g in rays:
            self.sync(c(cue))
            self.play(Create(g[0]), Create(g[1]), FadeIn(g[2]), run_time=0.5)
        self.sync(c("هِيَ"))
        note = label("the shear-wave angle in the steel", FS_LABEL, ACCENT_3, weight=BOLD).move_to([0.5, -2.7, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.sync(self.end(3))
        self.clear()

    # ---------------- Segment 4: the exit point and the angle check (§5.5) ----------------
    def seg4(self):
        c = lambda phrase, nth=1: self.cue(4, phrase, nth)
        S = self.start(4)
        v1 = V1Block(x0=-6.4, y_top=0.9)
        P = v1.P
        R = D.V1_QUADRANT_R * V1_SCALE
        name = label("IIW V1 block (simplified)", FS_NOTE, GREY_INK, weight=BOLD).move_to([-2.4, 3.3, 0])
        # ---- phase 1: the angle probe faces the quadrant ----
        xe = ValueTracker(P[0] + 1.1)
        d1 = np.array([-np.sin(np.radians(45)), -np.cos(np.radians(45)), 0.0])

        def hit_len(E):
            b = float(np.dot(d1, E - P)); cc = float(np.dot(E - P, E - P)) - R * R
            return -b + np.sqrt(max(b * b - cc, 0.0))
        probe1 = always_redraw(lambda: wedge_probe(xe.get_value(), v1.y_top, facing=-1, size=1.3))
        beam1 = always_redraw(lambda: DashedLine(np.array([xe.get_value(), v1.y_top, 0.0]),
                                                  np.array([xe.get_value(), v1.y_top, 0.0]) + d1 * hit_len(np.array([xe.get_value(), v1.y_top, 0.0])),
                                                  color=ACCENT_1, stroke_width=3))
        amp1 = lambda: float(np.exp(-((xe.get_value() - P[0]) / 0.42) ** 2))
        scr = AScan([(0.0, 1.5), (100.0, 0.2)], width=4.4, height=2.6, t_min=-6.0, t_max=110.0, ticks=(0, 50, 100),
                    sigma=1.0, x_caption="Distance (mm)", y_caption="Echo amplitude")
        scr.shift(np.array([4.6, 1.9, 0.0]) - scr.frame.get_center())
        mode = ValueTracker(0.0)                      # 0: the arc echo at 100 mm, 1: the small-hole echo at 60 mm
        xe2 = ValueTracker(0.0)
        x60 = v1.scale_x(60)
        amp2 = lambda: float(np.exp(-((xe2.get_value() - x60) / 0.2) ** 2))

        def retrace(m):
            if mode.get_value() < 0.5:
                scr.peaks = [(0.0, 1.5), (100.0, 0.12 + 1.35 * amp1())]
            else:
                scr.peaks = [(0.0, 1.5), (60.0, 0.12 + 1.35 * amp2())]
            scr.update_trace(scr.t_max)
        scr.trace.add_updater(retrace)

        self.sync(S + 0.1)
        self.play(FadeIn(name), Create(v1.body), FadeIn(v1.hole_big), FadeIn(v1.insert), FadeIn(v1.hole_small),
                  FadeIn(v1.scale), FadeIn(probe1), Create(beam1), FadeIn(scr), run_time=0.9)
        self.add(scr.trace)
        # slide the probe until the echo from the arc is at its maximum
        self.sync(c("نُحَرِّكُ"))
        self.play(xe.animate(run_time=1.7, rate_func=smooth).set_value(P[0] - 0.55))
        self.play(xe.animate(run_time=c("أَقْصَاهُ") - self.renderer.time + 0.1, rate_func=smooth).set_value(P[0]))
        peak = label("maximum echo", FS_TAG, ACCENT_2, weight=BOLD)
        peak.move_to([scr.x_of(100) - 1.0, scr.y_base() + 1.9, 0])
        self.play(FadeIn(peak), run_time=0.3)
        # the exit point is above the centre of the arc
        self.sync(c("فَتَكُونُ"))
        centre = Dot(P, radius=0.09, color=ACCENT_2)
        lab_c = label("exit point = centre of the arc", FS_NOTE, ACCENT_2, weight=BOLD).move_to([P[0] - 1.3, v1.y_top + 1.35, 0])
        lead_c = Arrow(lab_c.get_bottom() + DOWN * 0.03, P + UP * 0.1, buff=0.04, color=ACCENT_2, stroke_width=3, tip_length=0.15)
        self.play(GrowFromCenter(centre), FadeIn(lab_c), GrowArrow(lead_c), run_time=0.7)
        self.sync(c("وَنُعَلِّمُهَا"))
        idx = Triangle(color=ACCENT_2, stroke_width=2).set_fill(ACCENT_2, 1).scale(0.1).rotate(PI).move_to(P + UP * 0.2)
        lab_i = label("mark it on the probe", FS_NOTE, ACCENT_2, weight=BOLD).move_to([P[0] + 2.7, v1.y_top + 1.35, 0])
        lead_i = Arrow(lab_i.get_left() + LEFT * 0.03, P + RIGHT * 0.22 + UP * 0.2, buff=0.04, color=ACCENT_2, stroke_width=3, tip_length=0.15)
        self.play(FadeIn(idx), FadeIn(lab_i), GrowArrow(lead_i), run_time=0.6)
        # the range: the arc echo is set on 100 mm
        self.sync(c("وَلِمُعَايَرَةِ"))
        self.play(FadeOut(lab_c), FadeOut(lead_c), FadeOut(lab_i), FadeOut(lead_i), FadeOut(idx), FadeOut(peak), run_time=0.4)
        self.sync(c("مِئَةِ"))
        hundred = DashedLine([scr.x_of(100), scr.y_base() - 0.05, 0], [scr.x_of(100), scr.y_base() + 1.9, 0], color=ACCENT_3, stroke_width=3)
        lab100 = label("range: arc echo on 100 mm", FS_TAG, ACCENT_3, weight=BOLD).next_to(scr, DOWN, 0.55).align_to(scr.frame, RIGHT)
        self.play(Create(hundred), FadeIn(lab100), run_time=0.6)
        # ---- phase 2: the angle check on the small hole ----
        self.sync(c("وَلِلتَّحَقُّقِ"))
        self.play(FadeOut(probe1), FadeOut(beam1), FadeOut(centre), FadeOut(hundred), FadeOut(lab100), run_time=0.5)
        probe1.clear_updaters()
        beam1.clear_updaters()
        xe2.set_value(v1.scale_x(70) + 0.15)
        a2 = np.radians(60)
        d2 = np.array([-np.sin(a2), -np.cos(a2), 0.0])
        probe2 = always_redraw(lambda: wedge_probe(xe2.get_value(), v1.y_top, facing=-1, size=1.3))
        beam2 = always_redraw(lambda: DashedLine(np.array([xe2.get_value(), v1.y_top, 0.0]), v1.hole_small.get_center(),
                                                  color=ACCENT_1, stroke_width=3))
        tick_lbs = VGroup(*[v1.tick_label(a) for a in (45, 60, 70)])
        mode.set_value(1.0)
        self.add(probe2, beam2)
        self.play(FadeIn(tick_lbs), run_time=0.4)
        self.sync(c("نُحَرِّكُ", 2))
        self.play(xe2.animate(run_time=1.6, rate_func=smooth).set_value(x60 - 0.35))
        self.play(xe2.animate(run_time=c("أَقْصَاهُ", 2) - self.renderer.time + 0.1, rate_func=smooth).set_value(x60))
        hole_lab = label("1.5 mm hole echo at its maximum", FS_TAG, ACCENT_2, weight=BOLD).next_to(scr, DOWN, 0.55).align_to(scr.frame, RIGHT)
        self.play(FadeIn(hole_lab), run_time=0.3)
        self.sync(c("نَقْرَأُ"))
        read_ring = Circle(radius=0.28, color=ACCENT_3, stroke_width=4).move_to([x60, v1.y_top - 0.38, 0])
        reading = label("60°", FS_LABEL, ACCENT_3, weight=BOLD).move_to([x60, v1.y_top - 1.0, 0])
        self.play(Create(read_ring), FadeIn(reading), run_time=0.6)
        self.sync(self.end(4))
        scr.trace.clear_updaters()
        probe2.clear_updaters()
        beam2.clear_updaters()
        self.clear()

    # ---------------- Segment 5: sound path, skip distance, flaw location (§5.6.2, §8.4.1) ----------------
    def seg5(self):
        c = lambda phrase, nth=1: self.cue(5, phrase, nth)
        S = self.start(5)
        ss = 0.08                                            # units per mm
        T_MM, TH = D.PLATE_T, np.radians(D.PROBE_ANGLE)
        XE, TOPY = -5.4, 1.9
        plate = SteelBlock(9.8, T_MM * ss).move_to([XE + 4.5, TOPY - T_MM * ss / 2, 0])
        bot = TOPY - T_MM * ss
        wp = wedge_probe(XE, TOPY, size=1.3)
        ex = np.array([XE, TOPY, 0.0])
        flaw_p = np.array([XE + D.SURFACE_DIST * ss, TOPY - D.DEPTH * ss, 0.0])
        bounce = np.array([XE + D.HALF_SKIP * ss, bot, 0.0])
        end2 = np.array([XE + D.FULL_SKIP * ss, TOPY, 0.0])
        # the sound path to the flaw (S)
        s_arrow = Arrow(ex, flaw_p, buff=0, color=ACCENT_1, stroke_width=5, tip_length=0.2)
        s_lab = label("S", FS_LABEL, ACCENT_1, weight=BOLD).move_to((ex + flaw_p) / 2 + np.array([0.0, 0.42, 0.0]))
        flaw = Ellipse(width=0.42, height=0.2, color=ACCENT_4, stroke_width=3).set_fill(ACCENT_4, 0.8).move_to(flaw_p)
        screen_note = tag_line("S is read on the calibrated screen", "gauge", INK, width=5.8, size=FS_TAG)
        screen_note.move_to([0.6, -1.6, 0])
        self.sync(S + 0.1)
        self.play(Create(plate), FadeIn(wp), run_time=0.7)
        self.sync(c("مَسَارَ"))
        self.play(GrowArrow(s_arrow), FadeIn(flaw, scale=0.5), run_time=0.8)
        self.sync(c("بِالحَرْفِ"))
        self.play(FadeIn(s_lab), run_time=0.4)
        self.sync(c("بَعْدَ"))
        self.play(FadeIn(screen_note), run_time=0.4)
        # ---- the two legs and the skips ----
        self.sync(c("السَّاقُ"))
        self.play(FadeOut(s_arrow), FadeOut(s_lab), FadeOut(flaw), FadeOut(screen_note), run_time=0.4)
        leg1 = Arrow(ex, bounce, buff=0, color=ACCENT_1, stroke_width=5, tip_length=0.2)
        leg2 = Arrow(bounce, end2, buff=0, color=ACCENT_2, stroke_width=5, tip_length=0.2)
        l1 = label("1st leg", FS_TAG, ACCENT_1, weight=BOLD).move_to([XE + 1.4, bot - 0.5, 0])
        l2 = label("2nd leg", FS_TAG, ACCENT_2, weight=BOLD).move_to([XE + 6.6, bot - 0.5, 0])
        lead1 = Line(l1.get_top() + UP * 0.03, (ex + bounce) * 0.5 + (bounce - ex) * 0.05 + DOWN * 0.0, color=ACCENT_1, stroke_width=2)
        lead1.put_start_and_end_on(l1.get_top() + UP * 0.03, ex + (bounce - ex) * 0.62)
        lead2 = Line(l2.get_top() + UP * 0.03, bounce + (end2 - bounce) * 0.4, color=ACCENT_2, stroke_width=2)
        self.play(GrowArrow(leg1), run_time=0.9)
        self.play(FadeIn(l1), Create(lead1), run_time=0.3)
        self.sync(c("ثُمَّ"))
        self.play(GrowArrow(leg2), run_time=0.9)
        self.play(FadeIn(l2), Create(lead2), run_time=0.3)

        def skip_bracket(x_end, y, text, color):
            br = DoubleArrow([XE, y, 0], [x_end, y, 0], buff=0, color=color, stroke_width=3, tip_length=0.14)
            tk = VGroup(DashedLine([XE, TOPY + 0.08, 0], [XE, y, 0], color=GREY_INK, stroke_width=2),
                        DashedLine([x_end, TOPY + 0.08, 0], [x_end, y, 0], color=GREY_INK, stroke_width=2))
            tx = label(text, FS_TAG, color, weight=BOLD).next_to(br, RIGHT, 0.15)
            return VGroup(br, tk, tx)
        full = skip_bracket(end2[0], 3.4, "full skip", INK)
        half = skip_bracket(bounce[0], 2.95, "half skip", GREY_INK)
        self.sync(c("وَالمَسَافَةُ"))
        self.play(Create(full), run_time=0.7)
        self.sync(c("نِصْفُ"))
        self.play(Create(half), run_time=0.7)
        # ---- the example: one flaw, one path, one angle ----
        self.sync(c("مِثَالٌ") - 0.3)
        self.play(FadeOut(VGroup(leg1, leg2, l1, l2, lead1, lead2, full, half)), run_time=0.4)
        S_MM = D.PATH_S
        s_hot = Arrow(ex, flaw_p, buff=0, color=ACCENT_4, stroke_width=6, tip_length=0.2)
        vert = DashedLine(flaw_p, [flaw_p[0], TOPY, 0], color=INK, stroke_width=3)
        horiz = DashedLine([XE, TOPY + 0.0, 0], [flaw_p[0], TOPY, 0], color=INK, stroke_width=3)
        normal = DashedLine(ex, ex + DOWN * 1.4, color=GREY_INK, stroke_width=2)
        arc = Arc(radius=0.9, start_angle=-PI / 2, angle=TH, arc_center=ex, color=ACCENT_2, stroke_width=4)
        lab_a = label(f"{D.PROBE_ANGLE:.0f}°", FS_TAG, ACCENT_2, weight=BOLD).move_to(ex + np.array([0.82, -1.2, 0.0]))
        lab_s = label(f"S = {S_MM:.0f} mm", FS_TAG, ACCENT_4, weight=BOLD).move_to((ex + flaw_p) / 2 + np.array([-0.2, 0.55, 0.0]))
        lab_d = label("d", FS_LABEL, ACCENT_4, weight=BOLD).move_to([flaw_p[0] + 0.35, TOPY - D.DEPTH * ss / 2, 0])
        lab_x = label("x", FS_LABEL, ACCENT_4, weight=BOLD).move_to([(XE + flaw_p[0]) / 2, TOPY + 0.45, 0])
        self.sync(c("صَدَى"))
        self.play(FadeIn(flaw, scale=0.5), GrowArrow(s_hot), Create(normal), run_time=0.8)
        self.sync(c("بِمِجَسٍّ"))
        self.play(Create(arc), FadeIn(lab_a), FadeIn(lab_s), run_time=0.6)
        # d = S cos(angle)
        f1 = Text(f"d  =  S × cos {D.PROBE_ANGLE:.0f}°", font_size=28)
        v1_ = Text(f"=  {S_MM:.0f} × {np.cos(TH):.1f}", font_size=26, color=GREY_INK)
        r1 = Text(f"d = {D.DEPTH:.1f} mm", font_size=30, color=ACCENT_4, weight=BOLD)
        f2 = Text(f"x  =  S × sin {D.PROBE_ANGLE:.0f}°", font_size=28)
        v2_ = Text(f"=  {S_MM:.0f} × {np.sin(TH):.3f}", font_size=26, color=GREY_INK)
        r2 = Text(f"x = {D.SURFACE_DIST:.1f} mm", font_size=30, color=ACCENT_2, weight=BOLD)
        blk1 = VGroup(f1, v1_, r1).arrange(DOWN, buff=0.28)
        blk2 = VGroup(f2, v2_, r2).arrange(DOWN, buff=0.28)
        calc = fit(VGroup(blk1, blk2).arrange(DOWN, buff=0.7), 3.2).move_to([5.3, 0.5, 0])
        fr1 = SurroundingRectangle(r1, color=ACCENT_4, buff=0.2, corner_radius=0.1, stroke_width=4)
        fr2 = SurroundingRectangle(r2, color=ACCENT_2, buff=0.2, corner_radius=0.1, stroke_width=4)
        self.sync(c("العُمْقُ"))
        self.play(Create(vert), FadeIn(lab_d), Write(f1, run_time=1.2))
        self.sync(c("خَمْسِينَ", 2))
        self.play(FadeIn(v1_, shift=DOWN * 0.15), run_time=0.8)
        self.sync(c("خَمْسَةً"))
        self.play(Write(r1, run_time=0.8), Create(fr1, run_time=0.8))
        self.sync(c("وَالمَسَافَةُ", 2))
        self.play(Create(horiz), FadeIn(lab_x), Write(f2, run_time=1.2))
        self.sync(c("سِتِّينَ", 4))
        self.play(FadeIn(v2_, shift=DOWN * 0.15), run_time=0.8)
        self.sync(c("ثَلَاثَةً"))
        self.play(Write(r2, run_time=0.8), Create(fr2, run_time=0.8))
        # ---- the depth is less than the thickness: the first leg ----
        self.sync(c("وَالعُمْقُ"))
        bar_t = Rectangle(width=T_MM * ss * 1.4, height=0.26, color=GREY_INK, stroke_width=0).set_fill(GREY_INK, 0.5)
        bar_d = Rectangle(width=D.DEPTH * ss * 1.4, height=0.26, color=ACCENT_4, stroke_width=0).set_fill(ACCENT_4, 0.8)
        bars = VGroup(bar_t, bar_d).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-4.6, -1.7, 0])
        lt = label(f"plate {D.PLATE_T:.0f} mm", FS_TAG, INK, weight=BOLD).next_to(bar_t, RIGHT, 0.2)
        ld = label(f"depth {D.DEPTH:.1f} mm", FS_TAG, ACCENT_4, weight=BOLD).next_to(bar_d, RIGHT, 0.2)
        self.play(FadeIn(bars), FadeIn(lt), FadeIn(ld), run_time=0.6)
        self.sync(c("فَالعَيْبُ"))
        first = tag_line("less than the thickness: the flaw is on the first leg", "check", OK_C, width=7.0, size=FS_TAG)
        first.move_to([-2.0, -2.55, 0])
        self.play(FadeIn(first), run_time=0.5)
        # ---- the second leg: the depth is counted up from the back wall ----
        self.sync(c("أَمَّا"))
        self.play(FadeOut(VGroup(bars, lt, ld, first)), run_time=0.4)
        leg1b = Arrow(ex, bounce, buff=0, color=ACCENT_1, stroke_width=4, tip_length=0.18).set_opacity(0.6)
        leg2b = Arrow(bounce, end2, buff=0, color=ACCENT_2, stroke_width=5, tip_length=0.2)
        f2p = bounce + (end2 - bounce) * 0.55
        flaw2 = Ellipse(width=0.42, height=0.2, color=ACCENT_4, stroke_width=3).set_fill(ACCENT_4, 0.8).move_to(f2p)
        up = DoubleArrow([f2p[0] + 0.5, bot, 0], [f2p[0] + 0.5, f2p[1], 0], buff=0, color=ACCENT_3, stroke_width=3, tip_length=0.14)
        up_lab = label("depth counted up from the back wall", FS_TAG, ACCENT_3, weight=BOLD).move_to([-2.2, -1.9, 0])
        up_lead = Line(up_lab.get_right() + RIGHT * 0.03, [f2p[0] + 0.5, bot - 0.02, 0], color=ACCENT_3, stroke_width=2)
        self.sync(c("فِي", 5) if False else c("فَيُقَاسُ"))
        self.play(Create(leg1b), Create(leg2b), FadeIn(flaw2), run_time=0.8)
        self.play(Create(up), FadeIn(up_lab), Create(up_lead), run_time=0.7)
        self.sync(self.end(5))
        self.clear()

    # ---------------- Segment 6: the DAC curve and a glimpse of DGS (§5.7, §5.8) ----------------
    def seg6(self):
        c = lambda phrase, nth=1: self.cue(6, phrase, nth)
        S = self.start(6)
        TOPY = 1.7
        blk = SteelBlock(6.0, 3.2).move_to([-3.2, TOPY - 1.6, 0])
        depths = [0.55, 1.25, 2.15]                              # units; the beam is at 45 degrees
        hx = [-4.9, -3.2, -1.5]
        holes = VGroup(*[Circle(radius=0.11, color=INK, stroke_width=3).set_fill(BG, 1).move_to([x, TOPY - d, 0])
                         for x, d in zip(hx, depths)])
        paths = [d * np.sqrt(2) / 0.08 for d in depths]          # mm on the screen (0.08 units per mm)
        hfun = lambda s: 2.25 * np.exp(-s / 25.9)                # the echo of identical holes shrinks with the path
        probe_xs = [x - d for x, d in zip(hx, depths)]
        name = label("Reference block with identical side-drilled holes", FS_NOTE, INK, weight=BOLD).move_to([-3.2, 3.05, 0])
        scr = AScan([(0.0, 1.8)], width=5.2, height=3.0, t_min=-3.0, t_max=60.0, ticks=(0, 20, 40, 60), sigma=0.8,
                    x_caption="Sound path (mm)", y_caption="Echo amplitude")
        scr.shift(np.array([4.2, 0.9, 0.0]) - scr.frame.get_center())
        shown = {"echoes": []}

        def put_echoes(extra=()):
            scr.peaks = [(0.0, 1.8)] + shown["echoes"] + list(extra)
            scr.update_trace(scr.t_max)
        scr.trace.add_updater(lambda m: put_echoes())
        cur = {"k": 0}
        def probe_at(k, x_override=None):
            x = probe_xs[k] if x_override is None else x_override
            g = wedge_probe(x, TOPY, size=0.9)
            beam = Arrow(g.exit, [hx[k], TOPY - depths[k], 0], buff=0.0, color=ACCENT_1, stroke_width=4, tip_length=0.16)
            return VGroup(g, beam)
        # ---- two identical reflectors, two different echo heights ----
        self.sync(S + 0.1)
        self.play(FadeIn(name), Create(blk), FadeIn(holes), FadeIn(scr), run_time=0.9)
        self.add(scr.trace)
        self.sync(c("عُمْقَيْنِ"))
        pr = probe_at(0)
        self.play(FadeIn(pr), run_time=0.4)
        shown["echoes"] = [(paths[0], hfun(paths[0]))]
        self.sync(c("صَدًى"))
        self.play(Transform(pr, probe_at(2)), run_time=0.7)
        shown["echoes"] = [(paths[0], hfun(paths[0])), (paths[2], hfun(paths[2]))]
        flat = DashedLine([scr.x_of(paths[0]), scr.y_base() + hfun(paths[0]), 0], [scr.x_of(paths[2]) + 0.4, scr.y_base() + hfun(paths[0]), 0],
                          color=GREY_INK, stroke_width=2)
        diff = DoubleArrow([scr.x_of(paths[2]) + 0.25, scr.y_base() + hfun(paths[0]), 0],
                           [scr.x_of(paths[2]) + 0.25, scr.y_base() + hfun(paths[2]), 0], buff=0, color=ACCENT_2, stroke_width=3, tip_length=0.12)
        self.play(Create(flat), Create(diff), run_time=0.6)
        self.sync(c("لِأَنَّ"))
        why1 = tag_line("the beam spreads", "arrows-exchange", INK, width=3.6, size=FS_TAG)
        why2 = tag_line("the wave is attenuated", "wind", INK, width=3.8, size=FS_TAG)
        why = VGroup(why1, why2).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, -1.55, 0])
        self.sync(c("تَتَّسِعُ"))
        self.play(FadeIn(why1), run_time=0.4)
        self.sync(c("تَتَوَهَّنُ"))
        self.play(FadeIn(why2), run_time=0.4)
        # ---- build the curve: the three peaks, joined ----
        self.sync(c("لِذٰلِكَ"))
        self.play(FadeOut(why), FadeOut(flat), FadeOut(diff), run_time=0.4)
        shown["echoes"] = []
        self.play(Transform(pr, probe_at(0)), run_time=0.5)
        dots = VGroup()
        self.sync(c("نُسَجِّلُ"))
        for k, cue_word in ((0, "قِمَمَ"), (1, "ثُقُوبٍ"), (2, "أَعْمَاقٍ")):
            self.sync(c(cue_word))
            if k > 0:
                self.play(Transform(pr, probe_at(k)), run_time=0.5)
            shown["echoes"].append((paths[k], hfun(paths[k])))
            d_ = Dot([scr.x_of(paths[k]), scr.y_base() + hfun(paths[k]), 0], radius=0.09, color=ACCENT_3)
            dots.add(d_)
            self.play(GrowFromCenter(d_), run_time=0.3)
        self.sync(c("وَنَصِلُ"))
        ss_ = np.linspace(3.0, 52.0, 120)
        dac = VMobject(color=ACCENT_3, stroke_width=6)
        dac.set_points_smoothly([[scr.x_of(s_), scr.y_base() + hfun(s_), 0] for s_ in ss_])
        self.play(FadeOut(pr), Create(dac, run_time=1.4, rate_func=linear))
        self.sync(c("مُنْحَنَى", 2))
        dac_lab = label("DAC curve", FS_NOTE, ACCENT_3, weight=BOLD).move_to([scr.x_of(40) + 0.2, scr.y_base() + 1.4, 0])
        self.play(FadeIn(dac_lab), run_time=0.5)
        self.sync(c("دِي"))
        abbr = label("DAC = distance-amplitude correction", FS_TAG, ACCENT_3, weight=BOLD).next_to(scr, DOWN, 0.55).align_to(scr.frame, RIGHT)
        self.play(FadeIn(abbr), run_time=0.5)
        # ---- a flaw echo is compared with the curve at its own depth ----
        self.sync(c("وَبَعْدَهُ"))
        fl_x, fl_s = -0.55, 31.0
        flaw = Ellipse(width=0.34, height=0.2, color=ACCENT_4, stroke_width=3).set_fill(ACCENT_4, 0.8).move_to([-2.0, TOPY - 1.7, 0])
        fl_path = 1.7 * np.sqrt(2) / 0.08
        fl_h = hfun(fl_path) * 1.35
        shown["echoes"].append((fl_path, fl_h))
        self.play(FadeIn(flaw, scale=0.5), run_time=0.4)
        fl_dot = Dot([scr.x_of(fl_path), scr.y_base() + fl_h, 0], radius=0.1, color=ACCENT_4)
        cmp_ = DoubleArrow([scr.x_of(fl_path) + 0.28, scr.y_base() + hfun(fl_path), 0], [scr.x_of(fl_path) + 0.28, scr.y_base() + fl_h, 0],
                           buff=0, color=ACCENT_4, stroke_width=3, tip_length=0.12)
        self.sync(c("بِالمُنْحَنَى"))
        self.play(GrowFromCenter(fl_dot), Create(cmp_), run_time=0.6)
        note = label("compared with the curve at its depth", FS_TAG, ACCENT_4, weight=BOLD).next_to(abbr, DOWN, 0.2).align_to(abbr, RIGHT)
        self.sync(c("عُمْقِهِ"))
        self.play(FadeIn(note), run_time=0.4)
        self.sync(c("بِارْتِفَاعِهِ"))
        flat2 = DashedLine([scr.x_of(3), scr.y_base() + hfun(paths[0]), 0], [scr.x_of(56), scr.y_base() + hfun(paths[0]), 0],
                           color=GREY_INK, stroke_width=3)
        cross = icon("x", ALERT_C, 0.4).move_to([scr.x_of(52), scr.y_base() + hfun(paths[0]) + 0.35, 0])
        self.play(Create(flat2), FadeIn(cross), run_time=0.5)
        # ---- a glimpse of DGS ----
        self.sync(c("وَلَمْحَةٌ") - 0.3)
        scr.trace.clear_updaters()
        self.clear(run_time=0.5)
        AX0, AX1, AY0, AY1 = -4.2, 4.2, -2.6, 2.4
        x_ax = Arrow([AX0, AY0, 0], [AX1 + 0.3, AY0, 0], buff=0, color=INK, stroke_width=3, tip_length=0.2)
        y_ax = Arrow([AX0, AY0, 0], [AX0, AY1 + 0.3, 0], buff=0, color=INK, stroke_width=3, tip_length=0.2)
        xl = label("Distance", FS_NOTE, INK, weight=BOLD).next_to(x_ax, DOWN, 0.15).align_to(x_ax, RIGHT)
        yl = label("Gain (dB)", FS_NOTE, INK, weight=BOLD).next_to(y_ax, LEFT, 0.15).align_to(y_ax, UP)
        title = label("DGS diagram", FS_LABEL, ACCENT_3, weight=BOLD).move_to([0, 3.35, 0])
        curves = VGroup()
        names = VGroup()
        for k, (nm, col) in enumerate((("small reflector", ACCENT_4), ("larger", ACCENT_2), ("larger still", ACCENT_1), ("back wall", ACCENT_3))):
            t = np.linspace(0, 1, 60)
            xs = AX0 + 0.5 + t * (AX1 - AX0 - 1.2)
            ys = AY0 + 0.4 + (3.6 - 0.75 * k) * 0.55 * t ** 0.8 * (1.0 - 0.1 * k) + 0.35 * (3 - k) * 0.25
            crv = VMobject(color=col, stroke_width=5)
            crv.set_points_smoothly([[x, y, 0] for x, y in zip(xs, ys)])
            curves.add(crv)
            names.add(label(nm, FS_TAG, col, weight=BOLD).next_to(crv.get_end(), RIGHT, 0.12))
        self.sync(c("مُخَطَّطُ"))
        self.play(Create(x_ax), Create(y_ax), FadeIn(xl), FadeIn(yl), FadeIn(title), run_time=0.7)
        self.sync(c("طَرِيقَةٌ"))
        self.play(*[Create(cv) for cv in curves], run_time=1.2)
        self.play(FadeIn(names), run_time=0.4)
        self.sync(c("الحَسَاسِيَّةِ"))
        self.play(Indicate(yl, color=ACCENT_3), run_time=0.5)
        self.sync(c("المَسَافَةَ"))
        self.play(Indicate(xl, color=ACCENT_3), run_time=0.5)
        self.sync(c("وَالحَجْمَ"))
        self.play(Indicate(names, color=INK, scale_factor=1.05), run_time=0.6)
        self.sync(self.end(6))
        self.clear()

    # ---------------- Segment 7: review, 8 questions (entries 7-31) ----------------
    def seg7(self):
        N_E = len(NARRATION)

        def art1():                       # time becomes distance, gain goes to a reference
            scan = small_scan([0.0, -0.1], [(0, 1.3), (30, 0.5), (65, 0.9)], width=8.6, height=3.0, t_max=110.0,
                              ticks=(0, 25, 50, 75, 100), x_caption="Time (µs)")
            ref_y = scan.y_base() + 1.5
            ref = DashedLine([scan.frame.get_left()[0] + 0.5, ref_y, 0], [scan.frame.get_right()[0] - 0.3, ref_y, 0],
                            color=ACCENT_3, stroke_width=3)
            ref_t = label("reference level", FS_TAG, ACCENT_3, weight=BOLD).next_to(ref, UP, 0.08).align_to(ref, RIGHT)
            ask = label("?", FS_TITLE, ACCENT_2, weight=BOLD).move_to([scan.frame.get_right()[0] - 1.0, scan.y_base() + 0.9, 0])
            new_cap = label("Distance (mm)", FS_TAG, INK).move_to(scan.x_caption).align_to(scan.x_caption, RIGHT)

            def show():
                self.play(FadeIn(scan), FadeIn(scan.trace), FadeIn(ask), run_time=0.7)

            def finish(*extra):
                self.play(FadeOut(scan.x_caption), FadeIn(new_cap), FadeIn(ref), FadeIn(ref_t), FadeOut(ask), *extra, run_time=0.7)
            return show, finish

        def art2():                       # equal back-wall echoes on the screen
            scan = small_scan([0.0, -0.1], [(0, 1.5), (14, 1.3), (36, 1.0), (58, 0.75), (80, 0.55)], width=8.6, height=3.0,
                              t_max=110.0)
            marks = VGroup(*[DashedLine([scan.x_of(v), scan.y_base() - 0.05, 0], [scan.x_of(v), scan.y_base() + 1.7, 0],
                                        color=ACCENT_3, stroke_width=2) for v in D.V1_ECHOES])
            weak = label("each echo weaker", FS_TAG, ACCENT_2, weight=BOLD).move_to([scan.x_of(80) + 0.3, scan.y_base() + 1.5, 0])

            def show():
                self.play(FadeIn(scan), FadeIn(scan.trace), run_time=0.7)

            def finish(*extra):
                scan.peaks = [(0, 1.5)] + list(zip(D.V1_ECHOES, (1.3, 1.0, 0.75, 0.55)))
                self.remove(scan.trace)
                scan.update_trace(scan.t_max)
                self.play(Create(marks), FadeIn(scan.trace), FadeIn(weak), *extra, run_time=0.8)
            return show, finish

        def art3():                       # the longitudinal ray reaches the surface and leaves
            def build():
                rf = Refraction(-1.8, 0.3, length=2.0)
                rf.show_inc = rf.show_l = rf.show_s = True
                rf.set_alpha(15.0)
                return rf
            rf = build()
            perspex = Rectangle(width=6.0, height=2.0, color=INK, stroke_width=3).set_fill(ACCENT_1, 0.1).move_to([-1.0, 1.3, 0])
            steel = Rectangle(width=6.0, height=2.4, color=INK, stroke_width=3).set_fill(PANEL_FILL, 1).move_to([-1.0, -0.9, 0])
            al = ValueTracker(15.0)
            rf.add_updater(lambda m: m.set_alpha(al.get_value()))
            tag = label("wedge angle: 15°", FS_TAG, INK, weight=BOLD).move_to([4.2, 0.2, 0])
            both = label("longitudinal + shear", FS_TAG, ACCENT_3, weight=BOLD).move_to([4.2, -0.4, 0])
            gone = label("longitudinal ray at the surface: it leaves the part", FS_TAG, ACCENT_3, weight=BOLD).move_to([3.3, -0.4, 0])
            gone.scale_to_fit_width(4.6).move_to([4.5, -0.4, 0])

            def show():
                self.play(FadeIn(perspex), FadeIn(steel), FadeIn(rf), FadeIn(tag), FadeIn(both), run_time=0.7)

            def finish(*extra):
                tag2 = label(f"wedge angle: {D.CRIT_1:.1f}°", FS_TAG, ACCENT_3, weight=BOLD).move_to(tag)
                self.play(al.animate(run_time=1.6, rate_func=linear).set_value(D.CRIT_1 + 0.3), ReplacementTransform(tag, tag2),
                          ReplacementTransform(both, gone), *extra)
                rf.clear_updaters()
            return show, finish

        def art4():                       # the working band between the two angles
            g = AngleGauge(-4.0, 4.0, y=-0.2)
            lab1 = label("first critical angle", FS_TAG, ACCENT_3, weight=BOLD).move_to([g.x_of(D.CRIT_1) - 0.9, 0.6, 0])
            lab2 = label("second critical angle", FS_TAG, ACCENT_2, weight=BOLD).move_to([g.x_of(D.CRIT_2) + 0.8, 0.6, 0])
            ask = label("?", FS_TITLE, ACCENT_2, weight=BOLD).move_to([(g.x_of(D.CRIT_1) + g.x_of(D.CRIT_2)) / 2, -1.3, 0])
            res = tag_line("only a shear wave: one clear echo", "check", OK_C, width=6.0, size=FS_NOTE)
            res.move_to([0, -1.3, 0])

            def show():
                self.play(FadeIn(g), FadeIn(lab1), FadeIn(lab2), FadeIn(ask), run_time=0.7)

            def finish(*extra):
                self.play(FadeOut(ask), FadeIn(res), Indicate(g.band, color=OK_C), *extra, run_time=0.8)
            return show, finish

        def art5():                       # the angle on the probe
            top = 0.7
            blk = SteelBlock(7.0, 2.8).move_to([0.3, top - 1.4, 0])
            wp = wedge_probe(-1.4, top, size=1.4)
            ex = np.array([-1.4, top, 0.0])
            a = np.radians(60)
            end = ex + np.array([np.sin(a), -np.cos(a), 0.0]) * 2.6
            ray = Arrow(ex, end, buff=0, color=ACCENT_3, stroke_width=5, tip_length=0.2)
            normal = DashedLine(ex, ex + DOWN * 2.0, color=GREY_INK, stroke_width=2)
            arc = Arc(radius=0.9, start_angle=-PI / 2, angle=a, arc_center=ex, color=ACCENT_2, stroke_width=4)
            ask = label("?°", FS_LABEL, ACCENT_2, weight=BOLD).move_to(ex + np.array([0.75, -1.2, 0.0]))
            ans = label("60° = shear angle in the steel", FS_LABEL, ACCENT_2, weight=BOLD).move_to([3.0, -1.9, 0])
            probe_txt = label("60°", FS_TAG, INK, weight=BOLD).move_to(wp.get_center() + LEFT * 0.1 + UP * 0.05)

            def show():
                self.play(Create(blk), FadeIn(wp), FadeIn(probe_txt), run_time=0.6)
                self.play(Create(normal), GrowArrow(ray), Create(arc), FadeIn(ask), run_time=0.6)

            def finish(*extra):
                self.play(ReplacementTransform(ask, ans), *extra, run_time=0.6)
            return show, finish

        def art6():                       # the exit point is above the centre of the arc
            v1 = V1Block(x0=-5.4, y_top=0.9)
            P = v1.P
            wp = wedge_probe(P[0] + 1.2, v1.y_top, facing=-1, size=1.2)
            ask = label("exit point?", FS_NOTE, ACCENT_2, weight=BOLD).move_to([P[0] + 2.7, v1.y_top + 1.1, 0])
            dot = Dot(P, radius=0.1, color=ACCENT_2)
            lab = label("exit point = centre of the arc", FS_NOTE, ACCENT_2, weight=BOLD).move_to([P[0] - 0.7, v1.y_top + 1.4, 0])
            lead = Arrow(lab.get_bottom() + DOWN * 0.03, P + UP * 0.1, buff=0.04, color=ACCENT_2, stroke_width=3, tip_length=0.15)

            def show():
                self.play(Create(v1.body), FadeIn(v1.hole_big), FadeIn(v1.insert), FadeIn(v1.hole_small), FadeIn(v1.scale),
                          FadeIn(wp), FadeIn(ask), run_time=0.8)

            def finish(*extra):
                self.play(wp.animate.shift(LEFT * 1.2), FadeOut(ask), run_time=0.8)
                self.play(GrowFromCenter(dot), FadeIn(lab), GrowArrow(lead), *extra, run_time=0.6)
            return show, finish

        def art7():                       # depth of the flaw at path 50 mm, 60 degrees, plate 30 mm
            ss = 0.07
            XE, TOPY = -4.0, 1.3
            plate = SteelBlock(9.0, D.PLATE_T * ss).move_to([XE + 4.0, TOPY - D.PLATE_T * ss / 2, 0])
            ex = np.array([XE, TOPY, 0.0])
            a = np.radians(D.PROBE_ANGLE)
            fl = ex + np.array([D.SURFACE_DIST * ss, -D.DEPTH * ss, 0.0])
            wp = wedge_probe(XE, TOPY, size=1.1)
            ray = Arrow(ex, fl, buff=0, color=ACCENT_4, stroke_width=5, tip_length=0.2)
            flaw = Ellipse(width=0.36, height=0.18, color=ACCENT_4, stroke_width=3).set_fill(ACCENT_4, 0.8).move_to(fl)
            ls = label(f"S = {D.PATH_S:.0f} mm", FS_TAG, ACCENT_4, weight=BOLD).move_to((ex + fl) / 2 + np.array([-0.2, 0.55, 0.0]))
            tl = label(f"plate {D.PLATE_T:.0f} mm · probe {D.PROBE_ANGLE:.0f}°", FS_NOTE, INK, weight=BOLD).move_to([3.2, 1.4, 0])
            vert = DashedLine(fl, [fl[0], TOPY, 0], color=INK, stroke_width=3)
            ask = label("d = ?", FS_LABEL, ACCENT_2, weight=BOLD).move_to([fl[0] + 1.0, TOPY - D.DEPTH * ss / 2, 0])
            ans = label(f"d = {D.DEPTH:.1f} mm", FS_LABEL, ACCENT_2, weight=BOLD).move_to(ask)
            leg = tag_line(f"{D.DEPTH:.1f} < {D.PLATE_T:.0f}: first leg", "check", OK_C, width=4.6, size=FS_NOTE)
            leg.move_to([1.4, -1.9, 0])

            def show():
                self.play(Create(plate), FadeIn(wp), FadeIn(tl), run_time=0.6)
                self.play(GrowArrow(ray), FadeIn(flaw), FadeIn(ls), FadeIn(ask), run_time=0.6)

            def finish(*extra):
                self.play(Create(vert), ReplacementTransform(ask, ans), *extra, run_time=0.6)
                self.play(FadeIn(leg), run_time=0.4)
            return show, finish

        def art8():                       # DAC: the curve through identical reflectors, the flaw against it
            hfun = lambda s: 2.25 * np.exp(-s / 25.9)
            scan = small_scan([0.0, -0.2], [(0, 1.8)], width=8.6, height=3.2, t_max=60.0, ticks=(0, 20, 40, 60),
                              x_caption="Sound path (mm)")
            pts = [10, 22, 38]
            dots = VGroup(*[Dot([scan.x_of(s), scan.y_base() + hfun(s), 0], radius=0.09, color=ACCENT_3) for s in pts])
            scan.peaks = [(0, 1.8)] + [(s, hfun(s)) for s in pts]
            scan.update_trace(scan.t_max)
            dac = VMobject(color=ACCENT_3, stroke_width=6)
            dac.set_points_smoothly([[scan.x_of(s), scan.y_base() + hfun(s), 0] for s in np.linspace(3, 52, 100)])
            fl_s = 30.0
            fl_dot = Dot([scan.x_of(fl_s), scan.y_base() + hfun(fl_s) * 1.35, 0], radius=0.1, color=ACCENT_4)
            cmp_ = DoubleArrow([scan.x_of(fl_s) + 0.25, scan.y_base() + hfun(fl_s), 0], [scan.x_of(fl_s) + 0.25, scan.y_base() + hfun(fl_s) * 1.35, 0],
                               buff=0, color=ACCENT_4, stroke_width=3, tip_length=0.12)
            ask = label("flaw?", FS_NOTE, ACCENT_4, weight=BOLD).move_to([scan.x_of(fl_s) + 1.2, scan.y_base() + 1.6, 0])
            lab = label("compare at its depth", FS_NOTE, ACCENT_4, weight=BOLD).move_to([scan.x_of(fl_s) + 1.6, scan.y_base() + 1.9, 0])

            def show():
                self.play(FadeIn(scan), FadeIn(scan.trace), FadeIn(dots), run_time=0.7)
                self.play(FadeIn(fl_dot), FadeIn(ask), run_time=0.4)

            def finish(*extra):
                self.play(Create(dac), ReplacementTransform(ask, lab), Create(cmp_), *extra, run_time=0.9)
            return show, finish

        arts = [art1, art2, art3, art4, art5, art6, art7, art8]
        qs = [("What does calibration do to the screen and to the sensitivity?",
               "The screen reads a true distance; the gain is set on a known reference"),
              ("Why use multiple back-wall echoes on the block?", "They are equally spaced: set the screen on them"),
              ("What is the first critical angle?", "The wedge angle at which the longitudinal wave leaves the part"),
              ("Why are angle probes designed between the two critical angles?",
               "Only a shear wave stays in the steel: one clear echo"),
              ("What does the angle written on an angle probe mean?", "The shear-wave angle in the steel"),
              ("How do you find the beam exit point?", "Move the probe until the arc echo peaks"),
              (f"Flaw echo at a {D.PATH_S:.0f} mm path, {D.PROBE_ANGLE:.0f}° probe, {D.PLATE_T:.0f} mm plate: how deep, and on which leg?",
               f"{D.DEPTH:.1f} mm, on the first leg"),
              ("Why is the echo height alone not enough to judge a flaw?",
               "The beam spreads and the wave fades: compare with a DAC curve")]
        cards = [(q, (lambda scene, f=f: f()), a) for (q, a), f in zip(qs, arts)]
        run_review(self, cards, self.cue(7, "بِثَمَانِيَةِ"), self.cue(7, "ثَلَاثُ"), N_E)

    # SEGMENTS-END


if __name__ == "__main__":
    main(__file__, "UtSeriesEp03", NARRATION)
