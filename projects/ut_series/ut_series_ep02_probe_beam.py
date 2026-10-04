"""ut_series, episode 2: The probe and the beam.

Build (from the repo root):
    python projects/ut_series/ut_series_ep02_probe_beam.py --preview   # 480p15 -> tmp/ut_series_ep02_probe_beam/preview.mp4
    python projects/ut_series/ut_series_ep02_probe_beam.py             # 1080p30 -> output/ut_series_ep02_probe_beam.mp4

Narration segments: 1-6 are the six sections of the source (TCS-67 §2.6-2.8, §3.2); 7 is the review
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
    # 1  §1 the piezoelectric effect
    "قَلْبُ المِجَسِّ بَلُّورَةٌ تَعْمَلُ بِالتَّأْثِيرِ الكَهْرَضَغْطِيِّ: حِينَ يُسَلَّطُ عَلَيْهَا جَهْدٌ كَهْرَبَائِيٌّ تَتَشَوَّهُ فَتَهْتَزُّ، وَحِينَ تُضْغَطُ تُوَلِّدُ جَهْدًا. وَبِهٰذَا يُرْسِلُ المِجَسُّ الصَّوْتَ وَيَسْتَقْبِلُهُ بِالبَلُّورَةِ نَفْسِهَا. نَبْضَةُ الجِهَازِ الكَهْرَبَائِيَّةُ تَجْعَلُ البَلُّورَةَ تَهْتَزُّ فَتُوَلِّدُ المَوْجَةَ، وَالصَّدَى العَائِدُ يَهُزُّهَا فَتُوَلِّدُ إِشَارَةً تَظْهَرُ عَلَى الشَّاشَةِ. مِنَ المَوَادِّ الكُوَارْتْزُ، وَالسِّيرَامِيكُ المُسْتَقْطَبُ مِثْلُ تِيتَانَاتِ البَارِيُومِ وَزِرْكُونَاتِ تِيتَانَاتِ الرَّصَاصِ. وَسَمَاكَةُ البَلُّورَةِ تُحَدِّدُ تَرَدُّدَهَا: تَهْتَزُّ بِتَرَدُّدِهَا الأَسَاسِيِّ حِينَ تُسَاوِي سَمَاكَتُهَا نِصْفَ الطُّولِ المَوْجِيِّ فِيهَا، فَالبَلُّورَةُ الأَرَقُّ تَرَدُّدُهَا أَعْلَى.",
    # 2  §2 the structure of the probe
    "يَتَأَلَّفُ المِجَسُّ مِنَ البَلُّورَةِ، وَخَلْفَهَا مَادَّةُ التَّخْمِيدِ الَّتِي تَمْتَصُّ الِاهْتِزَازَ الخَلْفِيَّ فَتُوقِفُ رَنِينَ البَلُّورَةِ بِسُرْعَةٍ. وَأَمَامَهَا وَجْهٌ حَامٍ يَقِيهَا التَّآكُلَ، وَتَصِلُهَا بِالجِهَازِ دَارَةُ مُوَاءَمَةٍ كَهْرَبَائِيَّةٌ، وَالكُلُّ دَاخِلَ غِلَافٍ. التَّخْمِيدُ القَوِيُّ يُعْطِي نَبْضَةً قَصِيرَةً، فَنُمَيِّزُ عَيْبَيْنِ مُتَقَارِبَيْنِ فِي العُمْقِ، لٰكِنَّهُ يُقَلِّلُ الطَّاقَةَ وَالحَسَاسِيَّةَ. وَالتَّخْمِيدُ الخَفِيفُ يُعْطِي العَكْسَ: نَبْضَةً أَطْوَلَ وَحَسَاسِيَّةً أَعْلَى. فَاخْتِيَارُ المِجَسِّ مُوَازَنَةٌ بَيْنَهُمَا.",
    # 3  §3 the types of probes
    "لِلْمِجَسَّاتِ أَنْوَاعٌ. العَمُودِيُّ بِبَلُّورَةٍ وَاحِدَةٍ يُرْسِلُ مَوْجَةً طُولِيَّةً عَمُودِيَّةً عَلَى السَّطْحِ، لِقِيَاسِ السَّمَاكَةِ وَكَشْفِ العُيُوبِ المُوَازِيَةِ لِلسَّطْحِ كَالتَّصَفُّحِ. وَالمُزْدَوَجُ فِيهِ بَلُّورَةٌ تُرْسِلُ وَأُخْرَى تَسْتَقْبِلُ، بَيْنَهُمَا حَاجِزٌ صَوْتِيٌّ، فَتَقْصُرُ المِنْطَقَةُ المَيِّتَةُ قُرْبَ السَّطْحِ، وَيَصْلُحُ لِلسَّمَاكَاتِ الرَّقِيقَةِ وَالعُيُوبِ القَرِيبَةِ مِنَ السَّطْحِ وَقِيَاسِ السَّمَاكَةِ المُتَبَقِّيَةِ لِلْجُدْرَانِ. وَالمَائِلُ بَلُّورَتُهُ عَلَى إِسْفِينٍ بِلَاسْتِيكِيٍّ مَائِلٍ، فَتَنْكَسِرُ المَوْجَةُ وَتَدْخُلُ القِطْعَةَ بِزَاوِيَةٍ. وَهُوَ لِلَّحَامِ، لِأَنَّ عُيُوبَهُ المُسْتَوِيَةَ كَالشُّقُوقِ وَعَدَمِ الِانْصِهَارِ قَدْ لَا تَعْكِسُ الحُزْمَةَ العَمُودِيَّةَ. وَفِي الغَمْرِ تَكُونُ القِطْعَةُ وَالمِجَسُّ فِي المَاءِ، وَالمَاءُ هُوَ الوَسِيطُ، لِلْفَحْصِ الآلِيِّ. وَالمُرَكَّزُ عَدَسَةٌ تَجْمَعُ الحُزْمَةَ لِتَحْسِينِ كَشْفِ العُيُوبِ الصَّغِيرَةِ فِي مَدًى مُحَدَّدٍ مِنَ العُمْقِ.",
    # 4  §4 near field and far field; the one worked example
    "قُرْبَ المِجَسِّ تَتَدَاخَلُ المَوْجَاتُ الخَارِجَةُ مِنْ أَجْزَاءِ البَلُّورَةِ المُخْتَلِفَةِ، فَتَتَذَبْذَبُ الشِّدَّةُ بَيْنَ قَوِيَّةٍ وَضَعِيفَةٍ. هٰذِهِ المِنْطَقَةُ القَرِيبَةُ، وَالعَيْبُ فِيهَا يُفَسَّرُ بِحَذَرٍ، فَقَدْ يُعْطِي إِشَارَاتٍ مُتَعَدِّدَةً وَتَتَغَيَّرُ سَعَةُ صَدَاهُ كَثِيرًا. وَبَعْدَهَا مِنْطَقَةٌ انْتِقَالِيَّةٌ ثُمَّ المِنْطَقَةُ البَعِيدَةُ، تَسْتَقِرُّ فِيهَا الحُزْمَةُ وَتَضْعُفُ الشِّدَّةُ تَدْرِيجِيًّا مَعَ البُعْدِ. وَأَقْوَى صَدًى مِنْ عَاكِسٍ عَلَى المِحْوَرِ يَكُونُ قُرْبَ نِهَايَةِ المِنْطَقَةِ القَرِيبَةِ. وَنَحْسُبُ طُولَهَا بِقِسْمَةِ مُرَبَّعِ قُطْرِ البَلُّورَةِ عَلَى أَرْبَعَةِ أَمْثَالِ الطُّولِ المَوْجِيِّ. مِثَالٌ: مِجَسٌّ قُطْرُهُ عَشَرَةُ مِلِّيمِتْرَاتٍ وَتَرَدُّدُهُ أَرْبَعَةُ مِيغَاهِرْتْز فِي الفُولَاذِ. طُولُهُ المَوْجِيُّ وَاحِدٌ فَاصِلَةٌ أَرْبَعَةٌ ثَمَانِيَةٌ مِلِّيمِتْرٍ، وَمُرَبَّعُ القُطْرِ مِئَةٌ، فَطُولُ المِنْطَقَةِ القَرِيبَةِ سِتَّةَ عَشَرَ فَاصِلَةً تِسْعَةً مِلِّيمِتْرٍ، وَالعَيْبُ الأَقْرَبُ مِنْ سَبْعَةَ عَشَرَ مِلِّيمِتْرًا تَقْرِيبًا يَقَعُ فِيهَا. وَالنَّتِيجَةُ لِلْفَنِّيِّ: البَلُّورَةُ الأَكْبَرُ أَوِ التَّرَدُّدُ الأَعْلَى يُطِيلَانِ المِنْطَقَةَ القَرِيبَةَ، وَلِلْعُيُوبِ القَرِيبَةِ مِنَ السَّطْحِ نَسْتَعْمِلُ المِجَسَّ المُزْدَوَجَ أَوْ مِجَسًّا بِخَطِّ تَأْخِيرٍ.",
    # 5  §5 beam spread
    "فِي المِنْطَقَةِ البَعِيدَةِ تَتَّسِعُ الحُزْمَةُ كَمَخْرُوطٍ. وَكُلَّمَا كَبُرَتِ البَلُّورَةُ أَوِ ارْتَفَعَ التَّرَدُّدُ ضَاقَتِ الحُزْمَةُ. الحُزْمَةُ الضَّيِّقَةُ تُحَدِّدُ مَوْقِعَ العَيْبِ بِدِقَّةٍ أَكْبَرَ، وَالوَاسِعَةُ تُغَطِّي مِسَاحَةً أَكْبَرَ. فَإِذَا خَفَضْنَا التَّرَدُّدَ إِلَى النِّصْفِ اتَّسَعَتِ الحُزْمَةُ نَحْوَ الضِّعْفِ، وَإِذَا ضَاعَفْنَا قُطْرَ البَلُّورَةِ ضَاقَتْ إِلَى النِّصْفِ تَقْرِيبًا.",
    # 6  §6 attenuation
    "تَضْعُفُ المَوْجَةُ وَهِيَ تَسِيرُ لِسَبَبَيْنِ: التَّشَتُّتُ عِنْدَ حُدُودِ الحُبَيْبَاتِ، وَالِامْتِصَاصُ الَّذِي يُحَوِّلُ جُزْءًا مِنْ طَاقَتِهَا حَرَارَةً. وَيَزْدَادُ التَّشَتُّتُ مَعَ خُشُونَةِ الحُبَيْبَاتِ وَمَعَ ارْتِفَاعِ التَّرَدُّدِ. لِذٰلِكَ تُفْحَصُ المَوَادُّ خَشِنَةُ الحُبَيْبَاتِ، كَالمَسْبُوكَاتِ وَلِحَامَاتِ الفُولَاذِ الأُوسْتِنِيتِيِّ، بِتَرَدُّدَاتٍ أَقَلَّ. وَهٰذَا يُكَمِّلُ المُوَازَنَةَ الَّتِي رَأَيْنَاهَا فِي الحَلْقَةِ الأُولَى: التَّرَدُّدُ العَالِي يَكْشِفُ عُيُوبًا أَصْغَرَ، لٰكِنَّهُ يَتَوَهَّنُ أَسْرَعَ.",
    # 7  review: intro, then (question, 3 s countdown, answer) x 8
    "نُرَاجِعُ مَا تَعَلَّمْنَاهُ بِثَمَانِيَةِ أَسْئِلَةٍ. بَعْدَ كُلِّ سُؤَالٍ ثَلَاثُ ثَوَانٍ لِتُجِيبَ بِنَفْسِكَ.",
    "لِمَاذَا يُرْسِلُ المِجَسُّ الصَّوْتَ وَيَسْتَقْبِلُهُ بِالبَلُّورَةِ نَفْسِهَا؟", 3,
    "بِالتَّأْثِيرِ الكَهْرَضَغْطِيِّ: الجَهْدُ يُحَرِّكُهَا وَالضَّغْطُ يُوَلِّدُ جَهْدًا.",
    "كَيْفَ يَتَغَيَّرُ تَرَدُّدُ البَلُّورَةِ مَعَ سَمَاكَتِهَا؟", 3,
    "كُلَّمَا رَقَّتِ البَلُّورَةُ ارْتَفَعَ تَرَدُّدُهَا.",
    "مَا فَائِدَةُ مَادَّةِ التَّخْمِيدِ، وَمَا ثَمَنُهَا؟", 3,
    "تُوقِفُ الرَّنِينَ فَيَتَحَسَّنُ التَّمْيِيزُ، وَثَمَنُهَا الحَسَاسِيَّةُ.",
    "أَيُّ مِجَسٍّ لِلسَّمَاكَاتِ الرَّقِيقَةِ وَالعُيُوبِ القَرِيبَةِ مِنَ السَّطْحِ؟", 3,
    "المُزْدَوَجُ، لِأَنَّ مِنْطَقَتَهُ المَيِّتَةَ قَصِيرَةٌ.",
    "لِمَاذَا نَحْذَرُ فِي تَفْسِيرِ العُيُوبِ فِي المِنْطَقَةِ القَرِيبَةِ؟", 3,
    "لِأَنَّ تَدَاخُلَ المَوْجَاتِ يُعْطِي إِشَارَاتٍ مُتَعَدِّدَةً وَسَعَةً مُتَغَيِّرَةً.",
    "مِجَسٌّ قُطْرُهُ عَشَرَةُ مِلِّيمِتْرَاتٍ وَتَرَدُّدُهُ أَرْبَعَةُ مِيغَاهِرْتْز فِي الفُولَاذِ: كَمْ طُولُ مِنْطَقَتِهِ القَرِيبَةِ؟", 3,
    "نَحْوُ سِتَّةَ عَشَرَ فَاصِلَةً تِسْعَةً مِلِّيمِتْرٍ.",
    "مَاذَا يَحْدُثُ لِلْحُزْمَةِ إِذَا كَبُرَتِ البَلُّورَةُ أَوِ ارْتَفَعَ التَّرَدُّدُ؟", 3,
    "تَضِيقُ، فَيَتَحَدَّدُ مَوْقِعُ العَيْبِ بِدِقَّةٍ أَكْبَرَ.",
    "لِمَاذَا نَخْفِضُ التَّرَدُّدَ فِي المَسْبُوكَاتِ خَشِنَةِ الحُبَيْبَاتِ؟", 3,
    "التَّشَتُّتُ يَزْدَادُ مَعَ الخُشُونَةِ وَالتَّرَدُّدِ، فَيَتَوَهَّنُ الصَّوْتُ.",
]

# Every spoken or shown value is checked against the data module; stop if it drifts.
assert f"{D.NEAR_FIELD:.1f}" == "16.9" and abs(D.LAMBDA_EP2 - 1.48) < 1e-9          # seg 4, review Q6
assert round(D.NEAR_FIELD) == 17                                                    # "nearer than 17 mm"
assert D.BEAM_HALF_ANGLES[1] > 1.9 * D.BEAM_HALF_ANGLES[0] > 0                      # seg 5: half the frequency, about twice the angle
assert 1.9 < D.BEAM_HALF_ANGLES[0] / D.BEAM_HALF_ANGLES[2] < 2.1                    # seg 5: double the diameter, about half the angle

AUDIO_DIR = audio_dir_for(__file__)

# Colour roles of this project (project CLAUDE.md): ACCENT_1 sound / probe / incident wave,
# ACCENT_2 reflected wave / echo, ACCENT_3 transmitted wave / OK, ACCENT_4 flaw / alarm.


# ---- Segment 1 helpers: the crystal slab (its thickness can change) ----
class Crystal(VGroup):
    """A piezoelectric crystal: a slab between two electrode plates, standing on `y_bottom`
    at `x`. `set_h(h)` changes the thickness keeping the bottom fixed (the electrode on top
    follows). Parts: slab, top_plate, bottom_plate."""

    def __init__(self, x, y_bottom, width=1.9, height=0.8, color=ACCENT_1):
        self.x, self.y0, self.w, self.h = x, y_bottom, width, height
        self.slab = Rectangle(width=width, height=height, color=color, stroke_width=4)
        self.slab.set_fill(color, 0.3)
        self.top_plate = Line(LEFT, RIGHT, color=GREY_INK, stroke_width=8)
        self.bottom_plate = Line(LEFT, RIGHT, color=GREY_INK, stroke_width=8)
        super().__init__(self.slab, self.top_plate, self.bottom_plate)
        self.set_h(height)

    def set_h(self, h):
        self.h = h
        self.slab.stretch_to_fit_height(h).move_to([self.x, self.y0 + h / 2, 0])
        a, b = self.x - self.w / 2 - 0.15, self.x + self.w / 2 + 0.15
        self.top_plate.put_start_and_end_on([a, self.y0 + h, 0], [b, self.y0 + h, 0])
        self.bottom_plate.put_start_and_end_on([a, self.y0, 0], [b, self.y0, 0])
        return self


def chip_box(text, color, size=FS_TAG, width=None):
    """A rounded note box in `color` (frame and text), fitted to its text."""
    txt = label(text, size, INK)
    box = RoundedRectangle(width=(width or txt.width + 0.5), height=txt.height + 0.3,
                           corner_radius=0.12, color=color, stroke_width=3).set_fill(PANEL_FILL, 1)
    txt.move_to(box)
    return VGroup(box, txt)


# ---- Segment 2 helpers: the probe cutaway and the damped pulse traces ----
def damped_signal(t, pulses, f=2.2, tau=0.3):
    """Rectified ringing of several bursts: each (t0, amplitude) rings at frequency f and dies
    away with time constant tau (a short tau is strong damping)."""
    total = 0.0
    for t0, a in pulses:
        s = t - t0
        total = total + np.where(s >= 0, a * np.exp(-s / tau) * np.sin(TAU * f * s), 0.0)
    return np.abs(total)


def trace_panel(pulses, tau, width=5.4, height=1.7, t_max=5.0, color=INK):
    """A framed panel with the rectified ringing of `pulses` (the transmit pulse at t = 0 and the
    echoes of two close flaws). Parts: frame, trace, base (baseline y), x(t) -> screen x."""
    frame = Rectangle(width=width, height=height, color=INK, stroke_width=3).set_fill(PANEL_FILL, 1)
    base_y = -height / 2 + 0.35
    x0, x1 = -width / 2 + 0.3, width / 2 - 0.25
    xs = lambda t: x0 + (x1 - x0) * t / t_max
    ts = np.linspace(0, t_max, 700)
    ys = damped_signal(ts, pulses, tau=tau)
    ys = np.minimum(ys, height - 0.6)
    trace = VMobject(color=color, stroke_width=3)
    trace.set_points_as_corners([[xs(t), base_y + y * 0.8, 0] for t, y in zip(ts, ys)])
    base = Line([x0 - 0.1, base_y, 0], [x1 + 0.1, base_y, 0], color=GREY_INK, stroke_width=2)
    g = VGroup(frame, base, trace)
    g.frame, g.trace, g.base, g.xs, g.base_y = frame, trace, base, xs, base_y
    return g
# (the panel's x(t) is in its own coordinates: shift the group, then use g.get_center())


# ---- Segment 3 helpers: the panels of the five probe types ----
PANEL_W, PANEL_H = 4.35, 3.2
BLOCK_H = 1.1


def type_panel(cx, cy, title, note):
    """Frame, title (top) and one-line note (bottom) of a probe-type panel centred on (cx, cy).
    Returns VGroup(frame, title, note) with .frame, .title, .note."""
    frame = RoundedRectangle(width=PANEL_W, height=PANEL_H, corner_radius=0.14, color=GREY_INK,
                             stroke_width=3).set_fill(PANEL_FILL, 1).move_to([cx, cy, 0])
    t = label(title, FS_NOTE, INK, weight=BOLD).move_to([cx, cy + PANEL_H / 2 - 0.27, 0])
    n = label(note, FS_TAG - 2, GREY_INK).move_to([cx, cy - PANEL_H / 2 + 0.27, 0])
    g = VGroup(frame, t, n)
    g.frame, g.title, g.note = frame, t, n
    return g


def part_block(cx, cy, width=3.4, height=BLOCK_H):
    """A steel block whose top surface is at height cy (centred on cx)."""
    return SteelBlock(width, height).move_to([cx, cy - height / 2, 0])


def small_probe(color=ACCENT_1):
    return Probe(width=0.7, height=0.45, color=color)


# ---- Segment 4 helpers: the near-field beam, its intensity along the axis, the size bars ----
NF_SCALE = 0.11        # units per mm of depth in the beam drawing (the 10 mm crystal is 1.1 units wide)


def axis_intensity(s_mm, d_mm=D.PROBE_D_MM, lam_mm=D.LAMBDA_EP2):
    """On-axis intensity of a circular crystal (TCS-67 Fig. 2.21 shape): sin^2(pi/lambda (sqrt(a^2 + s^2) - s)),
    a = D/2; its last maximum is at s = N = D^2 / 4 lambda."""
    a = d_mm / 2
    return np.sin(np.pi / lam_mm * (np.sqrt(a * a + s_mm ** 2) - s_mm)) ** 2


def beam_outline(x_axis, y_top, n_mm, d_mm, theta_deg, depth_mm, scale=NF_SCALE, color=ACCENT_1):
    """Filled outline of the beam from a crystal of diameter d_mm: it narrows to about 0.6 of the
    crystal width at N (the focus), then spreads with the half angle theta_deg (to the beam edge)."""
    t = np.tan(np.radians(theta_deg))
    ss = np.linspace(0, depth_mm, 90)
    half = np.where(ss <= n_mm, 0.5 * d_mm * (1 - 0.4 * ss / n_mm),
                    0.5 * d_mm * 0.6 + t * (ss - n_mm)) * scale
    ys = y_top - ss * scale
    right = [[x_axis + h, y, 0] for h, y in zip(half, ys)]
    left = [[x_axis - h, y, 0] for h, y in zip(half[::-1], ys[::-1])]
    shape = VMobject(color=color, stroke_width=3)
    shape.set_points_as_corners(right + left + [right[0]])
    shape.set_fill(color, 0.12)
    return shape


# ---- Segment 5 helpers: a probe with its beam cone and the half-angle mark ----
CONE_SCALE = 0.11       # units per mm of crystal diameter (the same as the near-field drawing)


class BeamCone(VGroup):
    """A probe of diameter `d_mm` on `top_y` and its far-field beam: two edge lines spreading with
    the half angle `theta_deg` (to the beam edge) down to `depth` units, a dashed axis, and the
    half-angle arc with its value. Parts: probe, cone, axis, arc, value, flank_x(y) (the x of the
    right edge at height y)."""

    def __init__(self, x, d_mm, theta_deg, top_y=1.9, depth=3.9, color=ACCENT_1, cable=True):
        w = d_mm * CONE_SCALE
        t = np.tan(np.radians(theta_deg))
        self.x, self.w, self.t, self.top_y, self.depth = x, w, t, top_y, depth
        self.probe = Probe(width=w / 0.85, height=0.55, color=color).next_to(np.array([x, top_y, 0.0]), UP, 0)
        if not cable:
            self.probe.remove(self.probe.cable)
        r_end = [x + w / 2 + depth * t, top_y - depth, 0]
        l_end = [x - w / 2 - depth * t, top_y - depth, 0]
        self.cone = Polygon([x - w / 2, top_y, 0], [x + w / 2, top_y, 0], r_end, l_end,
                            color=color, stroke_width=3).set_fill(color, 0.12)
        self.axis = DashedLine([x, top_y, 0], [x, top_y - depth, 0], color=GREY_INK, stroke_width=2)
        edge = np.array([x + w / 2, top_y, 0.0])
        self.guide = DashedLine(edge, edge + DOWN * 1.5, color=INK, stroke_width=2)
        th = np.radians(theta_deg)
        self.arc = Arc(radius=1.3, start_angle=-PI / 2, angle=th, arc_center=edge, color=ACCENT_2, stroke_width=5)
        self.theta = theta_deg
        super().__init__(self.probe, self.cone, self.axis, self.guide, self.arc)

    def chord(self, depth_units):
        """Half width of the beam at `depth_units` below the crystal."""
        return self.w / 2 + depth_units * self.t


# ---- Segment 6 helpers: grains, scattering arrows, a frequency dial ----
def grain_lines(x0, x1, y0, y1, cell, seed=3, color=GREY_INK, jitter=0.28):
    """Grain boundaries: the lines of a jittered grid of side `cell` filling the box (a small `cell` is
    fine grain, a large one coarse grain). Returns a VGroup of line segments."""
    rng = np.random.default_rng(seed)
    nx, ny = int(round((x1 - x0) / cell)), int(round((y1 - y0) / cell))
    xs = np.linspace(x0, x1, nx + 1)
    ys = np.linspace(y0, y1, ny + 1)
    pts = {}
    for i in range(nx + 1):
        for j in range(ny + 1):
            jx = 0 if i in (0, nx) else rng.uniform(-jitter, jitter) * cell
            jy = 0 if j in (0, ny) else rng.uniform(-jitter, jitter) * cell
            pts[(i, j)] = np.array([xs[i] + jx, ys[j] + jy, 0.0])
    lines = VGroup()
    for i in range(nx + 1):
        for j in range(ny + 1):
            if i < nx and j not in (0, ny):
                lines.add(Line(pts[(i, j)], pts[(i + 1, j)], color=color, stroke_width=2))
            if j < ny and i not in (0, nx):
                lines.add(Line(pts[(i, j)], pts[(i, j + 1)], color=color, stroke_width=2))
    return lines


class FrequencyDial(VGroup):
    """A half-circle dial with a needle: `set_value(v)` (0 low .. 1 high) turns the needle.
    Parts: arc, ticks, needle, caption."""

    def __init__(self, radius=1.1, caption="frequency"):
        self.radius = radius
        self.arc = Arc(radius=radius, start_angle=0, angle=PI, color=INK, stroke_width=5)
        self.ticks = VGroup(*[Line(radius * 0.88 * np.array([np.cos(a), np.sin(a), 0]),
                                    radius * np.array([np.cos(a), np.sin(a), 0]), color=INK, stroke_width=3)
                              for a in np.linspace(0, PI, 6)])
        self.needle = Line(ORIGIN, radius * 0.85 * UP, color=ACCENT_2, stroke_width=6)
        self.hub = Dot(ORIGIN, radius=0.08, color=INK)
        self.caption = label(caption, FS_TAG, INK, weight=BOLD).move_to([0, -0.4, 0])
        super().__init__(self.arc, self.ticks, self.needle, self.hub, self.caption)
        self.value = 0.5
        self.set_value(0.5)

    def set_value(self, v):
        self.value = v
        a = PI * (1 - v)
        c0 = self.arc.get_arc_center()
        self.needle.put_start_and_end_on(c0, c0 + self.radius * 0.85 * np.array([np.cos(a), np.sin(a), 0]))
        return self


# HELPERS-END


class UtSeriesEp02(SyncedScene):
    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        self.seg1()
        self.seg2()
        self.seg3()
        self.seg4()
        self.seg5()
        self.seg6()
        self.seg7()

    # ---------------- Segment 1: the piezoelectric crystal (§2.6) ----------------
    def seg1(self):
        c = lambda phrase, nth=1: self.cue(1, phrase, nth)
        S = self.start(1)

        # ---- 0-3 s: title card ----
        title_card(self, "Ultrasonic Testing", "The probe and the beam",
                   series="Ultrasonic Testing Series · Episode 2", run_time=1.6)
        self.sync(c("بِالتَّأْثِيرِ") + 0.5)
        self.clear(run_time=0.5)

        # ---- the crystal on a steel part, the pulser's voltage, the pressure ----
        XC, BLK_TOP = -3.4, -0.35
        block = SteelBlock(5.2, 2.2).move_to([XC, BLK_TOP - 1.1, 0])
        cry = Crystal(XC, BLK_TOP, width=2.2, height=1.0)
        cry_tag = label("Crystal", FS_LABEL, ACCENT_1, weight=BOLD).next_to(cry, LEFT, 0.45)
        part_tag = label("Steel part", FS_TAG, GREY_INK).next_to(block, DOWN, 0.15)
        self.sync(S + 2.4)
        self.play(Create(block), FadeIn(cry), FadeIn(cry_tag), FadeIn(part_tag), run_time=0.9)

        # voltage on -> the crystal deforms and vibrates
        plus = label("+", FS_LABEL + 4, ACCENT_2, weight=BOLD)
        minus = label("−", FS_LABEL + 4, ACCENT_2, weight=BOLD)
        osc = ValueTracker(0.0)                       # 0: still, > 0: vibration amplitude
        freq = ValueTracker(1.0)
        clock = ValueTracker(0.0)
        sq = ValueTracker(0.0)                        # squeeze: pressure on the crystal
        cry.add_updater(lambda m: m.set_h(1.0 - sq.get_value()
                                          + osc.get_value() * np.sin(TAU * 3.0 * clock.get_value())))
        clock.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(clock)
        self.sync(c("يُسَلَّطُ"))
        plus.move_to([XC + 1.55, BLK_TOP + 1.0, 0])
        minus.move_to([XC + 1.55, BLK_TOP + 0.4, 0])
        volt_lab = label("voltage applied", FS_TAG, ACCENT_2).next_to(plus, RIGHT, 0.15).shift(DOWN * 0.45)
        self.play(FadeIn(plus), FadeIn(minus), FadeIn(volt_lab), run_time=0.4)
        self.play(osc.animate(run_time=0.6).set_value(0.16))
        self.sync(c("وَحِينَ"))
        self.play(osc.animate(run_time=0.3).set_value(0.0), FadeOut(plus), FadeOut(minus),
                  FadeOut(volt_lab), run_time=0.3)
        # pressure on -> a voltage appears
        self.sync(c("تُضْغَطُ"))
        press = Arrow(cry.top_plate.get_center() + UP * 1.1, cry.top_plate.get_center() + UP * 0.12,
                      buff=0, color=ACCENT_4, stroke_width=7, tip_length=0.25)
        press_lab = label("pressure", FS_TAG, ACCENT_4, weight=BOLD).next_to(press, RIGHT, 0.12)
        meter = Rectangle(width=1.6, height=0.28, color=INK, stroke_width=3).set_fill(PANEL_FILL, 1)
        meter.next_to(cry, RIGHT, 0.8).shift(UP * 0.2)
        meter_lab = label("voltage", FS_TAG, GREY_INK).next_to(meter, UP, 0.1)
        fill = signal_bar(meter, 0.8, ACCENT_2)
        self.play(GrowArrow(press), FadeIn(press_lab), FadeIn(meter), FadeIn(meter_lab),
                  sq.animate.set_value(0.16), run_time=0.5)
        self.play(GrowFromEdge(fill, LEFT), run_time=0.5)
        self.sync(c("وَبِهٰذَا"))
        self.play(FadeOut(press), FadeOut(press_lab), FadeOut(meter), FadeOut(meter_lab),
                  FadeOut(fill), sq.animate.set_value(0.0), run_time=0.5)

        # ---- the pulse sends, the echo returns, the screen shows it ----
        PEAKS = [(0.0, 1.3), (5.5, 0.85)]
        scan = AScan(PEAKS, width=5.8, height=2.5, t_min=-0.6, t_max=10.0, ticks=(),
                     x_caption="Time", y_caption="Signal")
        scan.shift(np.array([3.6, 1.5, 0.0]) - scan.frame.get_center())
        scan_tag = label("Screen", FS_LABEL, INK, weight=BOLD).next_to(scan.frame, UP, 0.12)
        pulser = chip_box("Instrument pulse", ACCENT_2, FS_TAG)
        pulser.move_to([XC, 1.75, 0])
        spark = Arrow(pulser.get_bottom(), cry.top_plate.get_center() + UP * 0.05, buff=0.05,
                      color=ACCENT_2, stroke_width=5, tip_length=0.2)
        flaw = Ellipse(width=0.7, height=0.24, color=ACCENT_4, stroke_width=4)
        flaw.set_fill(ACCENT_4, 0.4).move_to([XC, BLK_TOP - 1.45, 0])
        self.sync(c("نَبْضَةُ"))
        self.play(FadeIn(pulser), FadeIn(flaw), FadeIn(scan), FadeIn(scan_tag), run_time=0.6)
        self.add(scan.trace)
        T_SW0, T_SW1 = c("تَجْعَلُ") + 0.3, c("إِشَارَةً") + 1.6      # the screen's sweep follows the clock
        scan.trace.clear_updaters()
        scan.trace.add_updater(lambda m: scan.update_trace(
            scan.t_min + (scan.t_max - scan.t_min) * float(np.clip(
                (self.renderer.time - T_SW0) / (T_SW1 - T_SW0), 0, 1))))
        self.sync(c("تَجْعَلُ") - 0.1)
        self.play(GrowArrow(spark), run_time=0.4)
        self.sync(T_SW0)
        self.play(osc.animate(run_time=0.3).set_value(0.16), FadeOut(spark, run_time=0.3))
        self.sync(c("المَوْجَةَ"))
        down = wavefront(length=0.7, amp=0.3, cycles=6).move_to([XC, BLK_TOP - 0.3, 0])
        self.add(down)
        self.play(osc.animate(run_time=0.3).set_value(0.0),
                  down.animate(run_time=0.9, rate_func=linear).move_to([XC, flaw.get_top()[1] - 0.25, 0]))
        back = wavefront(length=0.7, amp=0.3, cycles=6, color=ACCENT_2, direction=UP)
        back.move_to([XC, flaw.get_top()[1] + 0.25, 0])
        self.sync(c("وَالصَّدَى"))
        self.play(FadeOut(down, run_time=0.1), FadeIn(back, run_time=0.1),
                  Flash(flaw, color=ACCENT_4, flash_radius=0.5, line_length=0.15, run_time=0.4))
        self.play(back.animate(run_time=0.8, rate_func=linear).move_to([XC, BLK_TOP - 0.3, 0]))
        self.sync(c("يَهُزُّهَا"))
        self.play(FadeOut(back, run_time=0.1), Flash(cry, color=ACCENT_2, flash_radius=0.8,
                                                       line_length=0.15, run_time=0.4))
        self.play(osc.animate(run_time=0.2).set_value(0.1))
        self.sync(c("إِشَارَةً") + 0.8)
        pop = Circle(radius=0.2, color=ACCENT_2, stroke_width=4).move_to(scan.apex(1))
        self.play(Create(pop), run_time=0.4)
        self.play(osc.animate(run_time=0.3).set_value(0.0))

        # ---- the materials ----
        self.sync(c("الكُوَارْتْزُ"))
        quartz = chip_box("Quartz", ACCENT_1, FS_NOTE)
        ceram = chip_box("Polarized ceramic:\nbarium titanate, PZT", ACCENT_1, FS_NOTE)
        mats = VGroup(quartz, ceram).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        mats.move_to([3.6, -1.35, 0])
        mat_head = label("Crystal materials", FS_TAG, GREY_INK).next_to(mats, UP, 0.15).align_to(mats, LEFT)
        self.play(FadeIn(mat_head), FadeIn(quartz, shift=RIGHT * 0.2), run_time=0.5)
        self.sync(c("وَالسِّيرَامِيكُ"))
        self.play(FadeIn(ceram, shift=RIGHT * 0.2), run_time=0.5)

        # ---- thickness sets the frequency ----
        self.sync(c("وَسَمَاكَةُ") - 0.4)
        scan.trace.clear_updaters()
        cry.clear_updaters()
        clock.clear_updaters()
        self.clear(run_time=0.5)
        BASE_Y = -0.8
        thick = Crystal(-4.0, BASE_Y, width=1.9, height=1.5)
        thin = Crystal(2.3, BASE_Y, width=1.9, height=0.7)
        ck = ValueTracker(0.0)
        ck.add_updater(lambda m, dt: m.increment_value(dt))
        amp = ValueTracker(0.0)
        thick.add_updater(lambda m: m.set_h(1.5 + amp.get_value() * np.sin(TAU * 1.0 * ck.get_value())))
        thin.add_updater(lambda m: m.set_h(0.7 + amp.get_value() * 0.5 * np.sin(TAU * 2.0 * ck.get_value())))
        lab_k = VGroup(label("Thick crystal", FS_LABEL, INK, weight=BOLD),
                       label("lower frequency", FS_NOTE, ACCENT_1)).arrange(DOWN, buff=0.1)
        lab_n = VGroup(label("Thin crystal", FS_LABEL, INK, weight=BOLD),
                       label("higher frequency", FS_NOTE, ACCENT_1)).arrange(DOWN, buff=0.1)
        lab_k.move_to([-4.0, BASE_Y - 0.95, 0])
        lab_n.move_to([2.3, BASE_Y - 0.95, 0])
        self.sync(c("وَسَمَاكَةُ"))
        self.add(ck)
        self.play(FadeIn(thick), FadeIn(thin), FadeIn(lab_k), FadeIn(lab_n), run_time=0.6)
        self.play(amp.animate(run_time=0.5).set_value(0.12))

        def half_wave(crystal, x_off):
            """A half wavelength drawn across the thickness, to the right of the crystal."""
            h = crystal.h
            x = crystal.x + crystal.w / 2 + x_off
            curve = ParametricFunction(lambda s: np.array([x + 0.42 * np.sin(PI * s), BASE_Y + h * s, 0]),
                                       t_range=[0, 1], color=ACCENT_3, stroke_width=5)
            dim = DoubleArrow([x + 0.75, BASE_Y, 0], [x + 0.75, BASE_Y + h, 0], buff=0,
                              color=ACCENT_3, stroke_width=3, tip_length=0.14)
            tag = label("½ wavelength", FS_TAG - 2, ACCENT_3, weight=BOLD).next_to(dim, RIGHT, 0.1)
            return VGroup(curve, dim, tag)
        hw_k, hw_n = half_wave(thick, 0.35), half_wave(thin, 0.2)
        self.sync(c("نِصْفَ"))
        self.play(Create(hw_k), Create(hw_n), run_time=0.9)
        self.sync(c("فَالبَلُّورَةُ"))
        head = label("Thickness = half a wavelength  →  the fundamental frequency", FS_LABEL, INK, weight=BOLD)
        head.move_to([0, 2.7, 0])
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.5)
        self.sync(self.end(1))
        for m in (thick, thin, ck):
            m.clear_updaters()
        self.clear()

    # ---------------- Segment 2: the structure of the probe (§3.2.1-3.2.4) ----------------
    def seg2(self):
        c = lambda phrase, nth=1: self.cue(2, phrase, nth)
        S = self.start(2)

        # ---- the cutaway: case, protective face, crystal, backing, matching circuit, cable ----
        PX, PW = -4.7, 2.4
        case_top, case_bot = 2.0, -2.5
        case = RoundedRectangle(width=PW, height=case_top - case_bot, corner_radius=0.18,
                                color=INK, stroke_width=5).set_fill(BG, 1)
        case.move_to([PX, (case_top + case_bot) / 2, 0])
        face = Rectangle(width=PW - 0.3, height=0.16, color=ACCENT_3, stroke_width=3).set_fill(ACCENT_3, 0.6)
        face.move_to([PX, case_bot + 0.2, 0])
        crys = Rectangle(width=PW - 0.3, height=0.42, color=ACCENT_1, stroke_width=4).set_fill(ACCENT_1, 0.35)
        crys.next_to(face, UP, 0)
        backing = Rectangle(width=PW - 0.3, height=1.9, color=GREY_INK, stroke_width=3).set_fill(PANEL_FILL, 1)
        backing.next_to(crys, UP, 0)
        hatch = VGroup(*[Line(backing.get_corner(DL) + RIGHT * k * 0.32,
                              backing.get_corner(DL) + RIGHT * k * 0.32 + UP * 0.32 + RIGHT * 0.32,
                              color=LIGHT_INK, stroke_width=2)
                         for k in range(int((PW - 0.3) / 0.32 - 0.4))])
        hatch_rows = VGroup(*[hatch.copy().shift(UP * r * 0.34) for r in range(5)])
        net = Rectangle(width=1.4, height=0.55, color=ACCENT_2, stroke_width=4).set_fill(PANEL_FILL, 1)
        net.move_to([PX, case_top - 0.5, 0])
        net_sym = label("L C", FS_TAG, ACCENT_2, weight=BOLD).move_to(net)
        wire_in = VGroup(
            Line([PX - PW / 2 + 0.1, crys.get_center()[1], 0], [PX - PW / 2 + 0.1, net.get_center()[1], 0],
                 color=ACCENT_2, stroke_width=4),
            Line([PX - PW / 2 + 0.1, net.get_center()[1], 0], net.get_left(), color=ACCENT_2, stroke_width=4))
        cable = Line(case.get_top(), case.get_top() + UP * 0.8, color=GREY_INK, stroke_width=8)
        wire_net = Line(net.get_top(), case.get_top(), color=ACCENT_2, stroke_width=4)

        def side_label(text, part, color, dx=0.6, dy=0.0):
            lab = label(text, FS_NOTE, color, weight=BOLD)
            lab.next_to(case, RIGHT, 0.7).set_y(part.get_center()[1] + dy)
            lead = Line(lab.get_left() + LEFT * 0.05, part.get_right() + RIGHT * 0.02, color=color,
                        stroke_width=3)
            return VGroup(lab, lead)

        self.sync(S + 0.1)
        self.play(Create(case), run_time=0.5)
        self.sync(c("البَلُّورَةِ"))
        self.play(FadeIn(face), FadeIn(crys), run_time=0.4)
        lab_cry = side_label("Crystal", crys, ACCENT_1)
        self.play(FadeIn(lab_cry), run_time=0.4)
        self.sync(c("مَادَّةُ"))
        self.play(FadeIn(backing), FadeIn(hatch_rows), run_time=0.4)
        lab_back = side_label("Backing (damping)", backing, GREY_INK)
        self.play(FadeIn(lab_back), run_time=0.4)
        # the back vibration enters the backing and dies away
        self.sync(c("الِاهْتِزَازَ"))
        bw = wavefront(length=0.6, amp=0.4, cycles=4, color=ACCENT_1, direction=UP).move_to(
            [PX, crys.get_top()[1] + 0.35, 0])
        self.add(bw)
        self.play(bw.animate(run_time=1.4, rate_func=linear).move_to([PX, backing.get_top()[1] - 0.3, 0])
                  .set_stroke(opacity=0.0))
        self.remove(bw)
        # the protective face, the matching circuit, the case
        self.sync(c("وَجْهٌ"))
        lab_face = side_label("Protective face", face, ACCENT_3, dy=-0.1)
        self.play(FadeIn(lab_face), Indicate(face, color=ACCENT_3, scale_factor=1.1), run_time=0.6)
        self.sync(c("دَارَةُ"))
        self.play(Create(wire_in), FadeIn(net), FadeIn(net_sym), run_time=0.6)
        self.play(Create(wire_net), Create(cable), run_time=0.4)
        lab_net = side_label("Matching circuit", net, ACCENT_2)
        lab_net[0].shift(UP * 0.05)
        self.play(FadeIn(lab_net), run_time=0.4)
        lab_dev = label("to the instrument", FS_TAG, GREY_INK).next_to(cable, RIGHT, 0.15)
        self.play(FadeIn(lab_dev), run_time=0.3)
        self.sync(c("غِلَافٍ"))
        lab_case = label("Case", FS_NOTE, INK, weight=BOLD).next_to(case, DOWN, 0.15)
        self.play(Indicate(case, color=INK, scale_factor=1.04), FadeIn(lab_case), run_time=0.6)

        # ---- damping: short pulse resolves two close flaws, ringing pulse merges them ----
        self.sync(c("التَّخْمِيدُ"))
        PULSES = [(0.0, 1.9), (3.0, 1.0), (3.45, 1.0)]       # transmit pulse, two close flaws
        strong = trace_panel(PULSES, tau=0.12, width=5.6, height=1.7)
        light = trace_panel(PULSES, tau=0.7, width=5.6, height=1.7)
        strong.move_to([3.9, 1.85, 0])
        light.move_to([3.9, -1.5, 0])
        h_s = label("Strong damping", FS_NOTE, INK, weight=BOLD).next_to(strong, UP, 0.12).align_to(strong, LEFT)
        h_l = label("Light damping", FS_NOTE, INK, weight=BOLD).next_to(light, UP, 0.12).align_to(light, LEFT)
        flaw_ticks = VGroup()
        for panel in (strong, light):
            for tt in (3.0, 3.45):
                x = panel.get_center()[0] + panel.xs(tt)
                y = panel.get_center()[1] + panel.base_y
                flaw_ticks.add(Triangle(color=ACCENT_4, stroke_width=2).set_fill(ACCENT_4, 1)
                               .scale(0.08).move_to([x, y - 0.12, 0]))
        legend = VGroup(Triangle(color=ACCENT_4, stroke_width=2).set_fill(ACCENT_4, 1).scale(0.09),
                        label("two close flaws", FS_TAG, ACCENT_4, weight=BOLD)).arrange(RIGHT, buff=0.12)
        legend.move_to([3.9, 3.5, 0])
        self.play(FadeIn(strong.frame), FadeIn(strong.base), FadeIn(h_s), run_time=0.4)
        self.play(Create(strong.trace, run_time=1.2, rate_func=linear))
        self.play(FadeIn(flaw_ticks[0:2]), FadeIn(legend), run_time=0.4)
        res_s = tag_line("Two flaws told apart", "check", OK_C, width=4.6, size=FS_TAG)
        pen_s = tag_line("less energy: lower sensitivity", "alert-triangle", ALERT_C, width=4.8, size=FS_TAG)
        res_s.next_to(strong, DOWN, 0.12).align_to(strong, LEFT)
        pen_s.next_to(res_s, DOWN, 0.08).align_to(res_s, LEFT)
        self.sync(c("فَنُمَيِّزُ"))
        self.play(FadeIn(res_s, shift=RIGHT * 0.2), run_time=0.5)
        self.sync(c("لٰكِنَّهُ"))
        self.play(FadeIn(pen_s, shift=RIGHT * 0.2), run_time=0.5)
        self.sync(c("وَالتَّخْمِيدُ"))
        self.play(FadeIn(light.frame), FadeIn(light.base), FadeIn(h_l), run_time=0.4)
        self.play(Create(light.trace, run_time=1.4, rate_func=linear))
        self.play(FadeIn(flaw_ticks[2:4]), run_time=0.4)
        res_l = tag_line("Longer pulse: the two flaws merge", "x", ALERT_C, width=5.0, size=FS_TAG)
        pen_l = tag_line("more energy: higher sensitivity", "bolt", OK_C, width=4.8, size=FS_TAG)
        res_l.next_to(light, DOWN, 0.12).align_to(light, LEFT)
        pen_l.next_to(res_l, DOWN, 0.08).align_to(res_l, LEFT)
        self.sync(c("نَبْضَةً", 2))
        self.play(FadeIn(res_l, shift=RIGHT * 0.2), run_time=0.5)
        self.sync(c("وَحَسَاسِيَّةً"))
        self.play(FadeIn(pen_l, shift=RIGHT * 0.2), run_time=0.5)
        self.sync(c("مُوَازَنَةٌ"))
        self.play(Indicate(VGroup(res_s, pen_s), color=INK, scale_factor=1.05),
                  Indicate(VGroup(res_l, pen_l), color=INK, scale_factor=1.05), run_time=0.8)
        self.sync(self.end(2))
        self.clear()

    # ---------------- Segment 3: the types of probes (§3.2.6-3.2.12) ----------------
    def seg3(self):
        c = lambda phrase, nth=1: self.cue(3, phrase, nth)
        S = self.start(3)
        TOP_Y, BOT_Y = 1.95, -1.6
        XS = (-4.6, 0.0, 4.6)
        pulse = lambda col, d, amp=0.2: wavefront(length=0.4, amp=amp, cycles=4, color=col, direction=d)

        def shoot(p0, p1, col, rt=0.5, amp=0.2, angled=None):
            fly(self, pulse(col, angled if angled is not None else (DOWN if p1[1] < p0[1] else UP), amp),
                p0, p1, rt)

        # ---- panel 1: the normal probe, a lamination parallel to the surface ----
        cx, cy = XS[0], TOP_Y
        p1 = type_panel(cx, cy, "Normal probe", "Thickness, lamination")
        blk1 = part_block(cx, cy)
        pr1 = small_probe().next_to(blk1, UP, 0)
        lam = Ellipse(width=1.7, height=0.12, color=ACCENT_4, stroke_width=3).set_fill(ACCENT_4, 0.5)
        lam.move_to([cx, cy - 0.6, 0])
        lam_t = label("lamination", FS_TAG - 2, ACCENT_4).next_to(lam, DOWN, 0.1)
        self.sync(c("لِلْمِجَسَّاتِ"))
        self.play(FadeIn(p1.frame), FadeIn(p1.title), run_time=0.4)
        self.sync(c("العَمُودِيُّ"))
        self.play(Create(blk1), FadeIn(pr1), run_time=0.5)
        self.sync(c("طُولِيَّةً"))
        shoot([cx, cy - 0.2, 0], [cx, cy - 0.45, 0], ACCENT_1, 0.35)
        self.sync(c("المُوَازِيَةِ"))
        self.play(FadeIn(lam), FadeIn(lam_t), run_time=0.4)
        shoot([cx, cy - 0.2, 0], [cx, cy - 0.5, 0], ACCENT_1, 0.3)
        shoot([cx, cy - 0.5, 0], [cx, cy - 0.15, 0], ACCENT_2, 0.4)
        self.play(FadeIn(p1.note), run_time=0.3)

        # ---- panel 2: twin crystal, short dead zone ----
        cx, cy = XS[1], TOP_Y
        p2 = type_panel(cx, cy, "Twin-crystal probe", "Thin walls, near surface")
        blk2 = part_block(cx, cy)
        hous = RoundedRectangle(width=1.0, height=0.45, corner_radius=0.07, color=INK,
                                stroke_width=4).set_fill(BG, 1).next_to(blk2, UP, 0)
        cr_t = Rectangle(width=0.4, height=0.1, color=ACCENT_1, stroke_width=2).set_fill(ACCENT_1, 1)
        cr_r = Rectangle(width=0.4, height=0.1, color=ACCENT_2, stroke_width=2).set_fill(ACCENT_2, 1)
        cr_t.move_to(hous.get_bottom() + LEFT * 0.26 + UP * 0.05)
        cr_r.move_to(hous.get_bottom() + RIGHT * 0.26 + UP * 0.05)
        barrier = Line(hous.get_bottom() + UP * 0.02, hous.get_top() + DOWN * 0.02, color=INK, stroke_width=5)
        cab = Line(hous.get_top(), hous.get_top() + UP * 0.3, color=GREY_INK, stroke_width=5)
        tw = VGroup(cab, hous, cr_t, cr_r, barrier)
        send_t = label("send", FS_TAG - 3, ACCENT_1, weight=BOLD).next_to(hous, LEFT, 0.1)
        recv_t = label("receive", FS_TAG - 3, ACCENT_2, weight=BOLD).next_to(hous, RIGHT, 0.1)
        dz = Rectangle(width=3.4, height=0.42, color=ACCENT_4, stroke_width=0).set_fill(ACCENT_4, 0.22)
        dz.align_to(blk2, UP).match_x(blk2)
        dz_note = label("dead zone hides the flaw", FS_TAG - 2, ACCENT_4, weight=BOLD).move_to(p2.note)
        ok_note = label("short dead zone: flaw seen", FS_TAG - 2, OK_C, weight=BOLD).move_to(p2.note)
        near = Ellipse(width=0.6, height=0.14, color=ACCENT_4, stroke_width=3).set_fill(ACCENT_4, 0.6)
        near.move_to([cx + 0.7, cy - 0.28, 0])
        self.sync(c("وَالمُزْدَوَجُ"))
        self.play(FadeIn(p2.frame), FadeIn(p2.title), run_time=0.4)
        self.play(Create(blk2), FadeIn(tw), FadeIn(send_t), FadeIn(recv_t), run_time=0.5)
        self.sync(c("حَاجِزٌ"))
        self.play(Indicate(barrier, color=INK, scale_factor=1.6), run_time=0.5)
        self.play(FadeIn(near), FadeIn(dz), FadeIn(dz_note), run_time=0.4)
        self.sync(c("المِنْطَقَةُ"))
        self.play(dz.animate.stretch_to_fit_height(0.12).align_to(blk2, UP).set_fill(ACCENT_4, 0.22),
                  ReplacementTransform(dz_note, ok_note), run_time=0.6)
        shoot([cx - 0.26, cy - 0.12, 0], [cx + 0.7, cy - 0.28, 0], ACCENT_1, 0.35,
              angled=np.array([0.7, -0.5, 0]))
        shoot([cx + 0.7, cy - 0.28, 0], [cx + 0.26, cy - 0.12, 0], ACCENT_2, 0.35,
              angled=np.array([-0.5, 0.3, 0]))
        self.sync(c("وَيَصْلُحُ"))
        self.play(ReplacementTransform(ok_note, p2.note), run_time=0.3)

        # ---- panel 3: angle probe on a wedge, a weld with a slanted planar flaw ----
        cx, cy = XS[2], TOP_Y
        p3 = type_panel(cx, cy, "Angle probe", "Welds: planar flaws")
        blk3 = part_block(cx, cy)
        weld = Polygon([cx + 0.7, cy, 0], [cx + 1.5, cy, 0], [cx + 1.3, cy + 0.14, 0], [cx + 0.9, cy + 0.14, 0],
                       color=GREY_INK, stroke_width=2).set_fill(LIGHT_INK, 0.6)
        wx0 = cx + 1.1
        crack = Line([wx0 - 0.28, cy - 0.35, 0], [wx0 + 0.2, cy - 0.85, 0], color=ACCENT_4, stroke_width=6)
        wedge = Polygon([cx - 1.4, cy, 0], [cx - 0.4, cy, 0], [cx - 1.4, cy + 0.6, 0],
                        color=GREY_INK, stroke_width=3).set_fill(ACCENT_1, 0.15)
        wprobe = Probe(width=0.55, height=0.3).rotate(-0.9).move_to([cx - 1.18, cy + 0.42, 0])
        wedge_t = label("wedge", FS_TAG - 3, GREY_INK).next_to(wedge, DOWN, 0.55).shift(LEFT * 0.15)
        # the beam leaves the wedge at its exit point and runs down to the crack
        ex = np.array([cx - 0.7, cy, 0.0])
        hit = np.array([wx0 - 0.04, cy - 0.6, 0.0])
        beam_dir = hit - ex
        beam = DashedLine(ex, hit, color=ACCENT_1, stroke_width=3)
        vert = DashedLine([hit[0] + 0.45, cy - 0.02, 0], [hit[0] + 0.45, cy - 1.05, 0], color=GREY_INK, stroke_width=2)
        vert_note = label("vertical beam: weak echo", FS_TAG - 2, GREY_INK, weight=BOLD).move_to(p3.note)
        self.sync(c("وَالمَائِلُ"))
        self.play(FadeIn(p3.frame), FadeIn(p3.title), run_time=0.4)
        self.play(Create(blk3), FadeIn(wedge), FadeIn(wprobe), run_time=0.5)
        self.sync(c("إِسْفِينٍ"))
        self.play(FadeIn(wedge_t), Indicate(wedge, color=ACCENT_1, scale_factor=1.08), run_time=0.5)
        self.sync(c("فَتَنْكَسِرُ"))
        self.play(Create(beam), run_time=0.6)
        shoot(ex + beam_dir * 0.1, hit - beam_dir * 0.15, ACCENT_1, 0.5, angled=beam_dir)
        self.sync(c("لِلَّحَامِ"))
        self.play(FadeIn(weld), FadeIn(crack), run_time=0.5)
        shoot(hit - beam_dir * 0.25, hit, ACCENT_1, 0.3, angled=beam_dir)
        shoot(hit, ex + beam_dir * 0.1, ACCENT_2, 0.5, angled=-beam_dir)
        self.sync(c("قَدْ"))
        self.play(Create(vert), run_time=0.4)
        self.play(FadeIn(vert_note), run_time=0.3)
        self.sync(c("العَمُودِيَّةَ") + 0.3)
        self.play(ReplacementTransform(vert_note, p3.note), run_time=0.3)

        # ---- panel 4: immersion (bottom row, left) ----
        cx, cy = -2.3, BOT_Y
        p4 = type_panel(cx, cy, "Immersion probe", "Automatic testing")
        blk4 = SteelBlock(3.0, 0.55).move_to([cx, cy - 0.55 - 0.275, 0])
        water = Rectangle(width=3.7, height=1.05, color=ACCENT_1, stroke_width=0).set_fill(ACCENT_1, 0.18)
        water.align_to(blk4, DOWN).move_to([cx, cy - 0.55 + 0.525, 0])
        pr4 = small_probe().move_to([cx - 0.6, cy + 0.3, 0])
        wnote = label("water is the couplant", FS_TAG - 2, ACCENT_1, weight=BOLD).move_to(p4.note)
        self.sync(c("وَفِي"))
        self.play(FadeIn(p4.frame), FadeIn(p4.title), run_time=0.4)
        self.play(Create(blk4), FadeIn(water), run_time=0.5)
        self.sync(c("المَاءِ"))
        self.play(FadeIn(pr4), run_time=0.5)
        self.sync(c("وَالمَاءُ"))
        self.play(FadeIn(wnote), run_time=0.3)
        shoot([cx - 0.6, cy - 0.05, 0], [cx - 0.6, cy - 0.45, 0], ACCENT_1, 0.5)
        self.sync(c("لِلْفَحْصِ"))
        self.play(pr4.animate.shift(RIGHT * 1.2), run_time=0.8)
        self.play(pr4.animate.shift(LEFT * 0.6), run_time=0.5)
        self.play(ReplacementTransform(wnote, p4.note), run_time=0.3)

        # ---- panel 5: focused probe, a lens gathers the beam ----
        cx, cy = 2.3, BOT_Y
        p5 = type_panel(cx, cy, "Focused probe", "Small flaws at a set depth")
        blk5 = part_block(cx, cy - 0.05, height=1.0)
        pr5 = Probe(width=1.0, height=0.45).next_to(blk5, UP, 0.0)
        lens = Arc(radius=0.9, start_angle=-PI / 2 - 0.55, angle=1.1, color=ACCENT_3, stroke_width=6)
        lens.move_to(pr5.get_bottom() + DOWN * 0.04, aligned_edge=UP)
        fx, fy = cx, cy - 0.05 - 0.55
        edge_l, edge_r = pr5.get_bottom() + LEFT * 0.4, pr5.get_bottom() + RIGHT * 0.4
        cone = VGroup(Line(edge_l, [fx, fy, 0], color=ACCENT_1, stroke_width=3),
                      Line(edge_r, [fx, fy, 0], color=ACCENT_1, stroke_width=3))
        small = Ellipse(width=0.22, height=0.14, color=ACCENT_4, stroke_width=3).set_fill(ACCENT_4, 0.6)
        small.move_to([fx, fy, 0])
        lens_t = label("lens", FS_TAG - 3, ACCENT_3, weight=BOLD).next_to(pr5, RIGHT, 0.15).shift(DOWN * 0.1)
        self.sync(c("وَالمُرَكَّزُ"))
        self.play(FadeIn(p5.frame), FadeIn(p5.title), run_time=0.4)
        self.play(Create(blk5), FadeIn(pr5), run_time=0.5)
        self.sync(c("عَدَسَةٌ"))
        self.play(Create(lens), FadeIn(lens_t), run_time=0.5)
        self.sync(c("تَجْمَعُ"))
        self.play(Create(cone, lag_ratio=0.0), run_time=0.7)
        self.sync(c("الصَّغِيرَةِ"))
        self.play(FadeIn(small), Flash(small, color=ACCENT_4, flash_radius=0.3, line_length=0.1, run_time=0.4))
        self.play(FadeIn(p5.note), run_time=0.3)
        self.sync(self.end(3))
        self.clear()

    # ---------------- Segment 4: near field and far field (§2.7.1) ----------------
    def seg4(self):
        c = lambda phrase, nth=1: self.cue(4, phrase, nth)
        S = self.start(4)
        N_MM, D_MM = D.NEAR_FIELD, D.PROBE_D_MM
        sc = NF_SCALE
        BX, TOP = -4.6, 2.4                                 # beam axis x, surface height
        yd = lambda s: TOP - s * sc                         # screen height of depth s (mm)
        DEPTH_MM = 3 * N_MM + 2
        block = SteelBlock(2.8, DEPTH_MM * sc).move_to([BX, TOP - DEPTH_MM * sc / 2, 0])
        probe = Probe(width=D_MM * sc / 0.85, height=0.6).next_to(block, UP, 0)
        beam = beam_outline(BX, TOP, N_MM, D_MM, D.BEAM_HALF_ANGLES[0], DEPTH_MM)
        # the intensity along the axis, to the right of the block (the same depth axis)
        PX0, PAMP = -2.7, 2.5
        s_all = np.linspace(1.0, DEPTH_MM, 1500)
        pts = [[PX0 + PAMP * axis_intensity(s), yd(s), 0] for s in s_all]
        k_n = int(np.searchsorted(s_all, N_MM))
        near_curve = VMobject(color=ACCENT_4, stroke_width=4).set_points_as_corners(pts[:k_n + 1])
        rest_curve = VMobject(color=ACCENT_3, stroke_width=4).set_points_as_corners(pts[k_n:])
        base = Line([PX0, TOP, 0], [PX0, yd(DEPTH_MM), 0], color=GREY_INK, stroke_width=2)
        i_lab = label("Intensity on the axis", FS_TAG, GREY_INK).move_to([PX0 + 1.3, TOP + 0.45, 0])
        # N and 3N marks
        def mark(s, text, color):
            ln = DashedLine([BX - 1.4, yd(s), 0], [PX0 + PAMP + 0.1, yd(s), 0], color=color, stroke_width=2)
            tx = label(text, FS_SYMBOL, color, weight=BOLD).next_to(ln, RIGHT, 0.12)
            return VGroup(ln, tx)
        mark_n = mark(N_MM, "N", ACCENT_4)
        mark_3n = mark(3 * N_MM, "3N", ACCENT_3)
        # zone brackets
        ZX = 1.2
        def zone(s0, s1, text, color):
            br = DoubleArrow([ZX, yd(s0) - 0.04, 0], [ZX, yd(s1) + 0.04, 0], buff=0, color=color,
                             stroke_width=3, tip_length=0.12)
            tx = label(text, FS_TAG, color, weight=BOLD).next_to(br, RIGHT, 0.12)
            return VGroup(br, tx)
        z_near = zone(0, N_MM, "Near field", ACCENT_4)
        z_tran = zone(N_MM, 3 * N_MM, "Transition", GREY_INK)
        z_far = zone(3 * N_MM, DEPTH_MM, "Far field", ACCENT_3)
        d_dim = DoubleArrow(probe.crystal.get_corner(DL) + DOWN * 0.0 + LEFT * 0.0, probe.crystal.get_corner(DR),
                            buff=0, color=INK, stroke_width=3, tip_length=0.1)
        # ---- 0-8 s: the beam leaves the crystal; the waves interfere, the intensity swings ----
        self.sync(S + 0.1)
        self.play(Create(block), FadeIn(probe), run_time=0.7)
        self.sync(c("تَتَدَاخَلُ"))
        self.play(FadeIn(beam), run_time=0.6)
        self.sync(c("فَتَتَذَبْذَبُ"))
        self.play(FadeIn(base), FadeIn(i_lab), Create(near_curve, run_time=2.0, rate_func=linear))
        self.sync(c("هٰذِهِ"))
        self.play(Create(mark_n), Create(z_near[0]), FadeIn(z_near[1]), run_time=0.6)
        # ---- a flaw in the near field: several echoes, changing height ----
        near_flaw = Ellipse(width=0.34, height=0.16, color=ACCENT_4, stroke_width=3).set_fill(ACCENT_4, 0.7)
        near_flaw.move_to([BX, yd(0.5 * N_MM), 0])
        far_flaw = near_flaw.copy().move_to([BX, yd(2.0 * N_MM), 0])
        scan_a = AScan([(0.0, 1.2), (3.2, 0.5), (4.1, 1.0), (5.0, 0.35)], width=3.4, height=1.6, t_min=-0.6,
                       t_max=7.0, ticks=(), sigma=0.14, x_caption="", y_caption="")
        scan_a.shift(np.array([5.2, 2.55, 0.0]) - scan_a.frame.get_center())
        scan_b = AScan([(0.0, 1.2), (4.4, 0.9)], width=3.4, height=1.6, t_min=-0.6, t_max=7.0, ticks=(),
                       sigma=0.14, x_caption="", y_caption="")
        scan_b.shift(np.array([5.2, 2.55, 0.0]) - scan_b.frame.get_center())
        for sc_ in (scan_a, scan_b):
            sc_.update_trace(sc_.t_max)
        multi = label("several echoes", FS_TAG, ACCENT_4, weight=BOLD)
        multi.next_to(scan_a.frame, DOWN, 0.12).align_to(scan_a.frame, RIGHT)
        single = label("one clear echo", FS_TAG, ACCENT_3, weight=BOLD)
        single.next_to(scan_b.frame, DOWN, 0.12).align_to(scan_b.frame, RIGHT)
        self.sync(c("وَالعَيْبُ"))
        self.play(FadeIn(near_flaw, scale=0.5), run_time=0.4)
        self.sync(c("إِشَارَاتٍ"))
        self.play(FadeIn(scan_a), FadeIn(scan_a.trace), FadeIn(multi), run_time=0.6)
        self.sync(c("وَبَعْدَهَا"))
        self.play(Create(mark_3n), Create(z_tran[0]), FadeIn(z_tran[1]), run_time=0.6)
        self.sync(c("البَعِيدَةُ"))
        self.play(Create(z_far[0]), FadeIn(z_far[1]), FadeOut(scan_a), FadeOut(scan_a.trace), FadeOut(multi),
                  FadeOut(near_flaw), FadeIn(far_flaw, scale=0.5), run_time=0.6)
        self.play(FadeIn(scan_b), FadeIn(scan_b.trace), FadeIn(single), run_time=0.5)
        self.sync(c("وَتَضْعُفُ"))
        self.play(Create(rest_curve, run_time=1.8, rate_func=linear))
        # ---- the strongest echo is near the end of the near field ----
        self.sync(c("وَأَقْوَى"))
        n_dot = Dot([PX0 + PAMP * axis_intensity(N_MM), yd(N_MM), 0], radius=0.11, color=ACCENT_2)
        n_lab = label("strongest echo: at N", FS_NOTE, ACCENT_2, weight=BOLD).move_to([5.2, yd(N_MM), 0])
        self.play(FadeOut(scan_b), FadeOut(scan_b.trace), FadeOut(single), FadeOut(far_flaw),
                  GrowFromCenter(n_dot), FadeIn(n_lab), run_time=0.6)
        # ---- the one worked example: N = D^2 / (4 lambda) ----
        self.sync(c("وَنَحْسُبُ"))
        f_ = Text("N  =  D²  ÷  (4 λ)", font_size=32)
        v_ = Text(f"=  {D.PROBE_D_MM:.0f}²  ÷  (4 × {D.LAMBDA_EP2:.2f})", font_size=28, color=GREY_INK)
        r_ = Text(f"N = {D.NEAR_FIELD:.1f} mm", font_size=36, color=ACCENT_4, weight=BOLD)
        calc = fit(VGroup(f_, v_, r_).arrange(DOWN, buff=0.5), 3.4).move_to([5.2, -0.9, 0])
        calc_frame = SurroundingRectangle(r_, color=ACCENT_4, buff=0.28, corner_radius=0.1, stroke_width=4)
        self.play(Write(f_, run_time=1.2))
        # the given values, each when its word is spoken
        self.sync(c("مِجَسٌّ"))
        spec_d = label(f"D = {D.PROBE_D_MM:.0f} mm", FS_LABEL, INK, weight=BOLD)
        spec_f = label(f"f = {D.PROBE_F_MHZ:.0f} MHz", FS_LABEL, INK, weight=BOLD)
        spec_l = label(f"λ = {D.LAMBDA_EP2:.2f} mm", FS_LABEL, INK, weight=BOLD)
        specs = VGroup(spec_d, spec_f, spec_l).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([5.2, 2.3, 0])
        d_dim.put_start_and_end_on(probe.crystal.get_corner(UL) + UP * 0.35 + LEFT * 0.0,
                                   probe.crystal.get_corner(UR) + UP * 0.35)
        self.sync(c("قُطْرُهُ"))
        self.play(FadeIn(spec_d, shift=LEFT * 0.2), GrowFromCenter(d_dim), run_time=0.5)
        self.sync(c("وَتَرَدُّدُهُ"))
        self.play(FadeIn(spec_f, shift=LEFT * 0.2), run_time=0.5)
        self.sync(c("طُولُهُ"))
        self.play(FadeIn(spec_l, shift=LEFT * 0.2), run_time=0.5)
        self.sync(c("وَمُرَبَّعُ"))
        self.play(FadeIn(v_, shift=DOWN * 0.15, run_time=1.0))
        self.sync(c("فَطُولُ"))
        self.play(Write(r_, run_time=1.0), Create(calc_frame, run_time=1.0))
        self.sync(c("وَالعَيْبُ", 2))
        near_zone = Rectangle(width=2.8, height=N_MM * sc, color=ACCENT_4, stroke_width=0)
        near_zone.set_fill(ACCENT_4, 0.12).move_to([BX, TOP - N_MM * sc / 2, 0])
        close_flaw = near_flaw.copy().move_to([BX, yd(0.7 * N_MM), 0])
        self.play(FadeIn(near_zone), FadeIn(close_flaw, scale=0.5), run_time=0.6)
        # ---- the result for the technician: a bigger crystal or a higher frequency lengthens N ----
        self.sync(c("البَلُّورَةُ", 2) - 0.2)
        self.play(*[FadeOut(m) for m in (calc, calc_frame, specs, d_dim)], run_time=0.5)
        cases = [("2 MHz, 10 mm", D.NEAR_FIELDS[1], GREY_INK), ("4 MHz, 10 mm", D.NEAR_FIELDS[0], ACCENT_4),
                 ("4 MHz, 20 mm", D.NEAR_FIELDS[2], ACCENT_2)]
        bars, names = VGroup(), VGroup()
        for k, (nm, n_mm, col) in enumerate(cases):
            b = Rectangle(width=n_mm * 0.05, height=0.34, color=col, stroke_width=0).set_fill(col, 1)
            b.move_to([3.5 + b.width / 2, 2.2 - 0.85 * k, 0])
            bars.add(b)
            names.add(label(nm, FS_TAG, INK).next_to(b, UP, 0.05).align_to(b, LEFT))
        head = label("Near field length N", FS_NOTE, INK, weight=BOLD).next_to(names[0], UP, 0.2).align_to(names[0], LEFT)
        self.play(FadeIn(head), run_time=0.3)
        self.sync(c("البَلُّورَةُ", 2))
        self.play(GrowFromEdge(bars[1], LEFT), FadeIn(names[1]), run_time=0.5)
        self.play(GrowFromEdge(bars[2], LEFT), FadeIn(names[2]), run_time=0.7)
        self.sync(c("التَّرَدُّدُ", 2))
        self.play(GrowFromEdge(bars[0], LEFT), FadeIn(names[0]), run_time=0.5)
        # remedies
        twin_p = VGroup(RoundedRectangle(width=0.9, height=0.45, corner_radius=0.07, color=INK, stroke_width=4).set_fill(BG, 1),
                        Line(ORIGIN, UP * 0.4, color=INK, stroke_width=5))
        twin_p[1].move_to(twin_p[0]).shift(DOWN * 0.0)
        tp = VGroup(twin_p[0], Line(twin_p[0].get_top(), twin_p[0].get_bottom(), color=INK, stroke_width=5))
        tw_c1 = Rectangle(width=0.36, height=0.09, color=ACCENT_1, stroke_width=2).set_fill(ACCENT_1, 1)
        tw_c2 = Rectangle(width=0.36, height=0.09, color=ACCENT_2, stroke_width=2).set_fill(ACCENT_2, 1)
        tw_c1.move_to(twin_p[0].get_bottom() + LEFT * 0.23 + UP * 0.045)
        tw_c2.move_to(twin_p[0].get_bottom() + RIGHT * 0.23 + UP * 0.045)
        twin_all = VGroup(tp, tw_c1, tw_c2)
        twin_t = label("Twin-crystal probe", FS_TAG, INK, weight=BOLD).next_to(twin_all, DOWN, 0.15)
        delay_h = RoundedRectangle(width=0.9, height=0.4, corner_radius=0.07, color=ACCENT_1, stroke_width=4).set_fill(BG, 1)
        delay_b = Rectangle(width=0.9, height=0.45, color=GREY_INK, stroke_width=3).set_fill(ACCENT_1, 0.15)
        delay_b.next_to(delay_h, DOWN, 0)
        delay_all = VGroup(delay_h, delay_b)
        delay_t = label("Delay-line probe", FS_TAG, INK, weight=BOLD).next_to(delay_all, DOWN, 0.15)
        rem = VGroup(VGroup(twin_all, twin_t), VGroup(delay_all, delay_t)).arrange(DOWN, buff=0.35)
        rem.move_to([5.2, -1.85, 0])
        rem_head = label("Flaws near the surface", FS_NOTE, INK, weight=BOLD).next_to(rem, UP, 0.3)
        self.sync(c("وَلِلْعُيُوبِ"))
        self.play(FadeIn(rem_head), run_time=0.3)
        self.sync(c("المُزْدَوَجَ"))
        self.play(FadeIn(VGroup(twin_all, twin_t), shift=UP * 0.15), run_time=0.5)
        self.sync(c("بِخَطِّ"))
        self.play(FadeIn(VGroup(delay_all, delay_t), shift=UP * 0.15), run_time=0.5)
        self.sync(self.end(4))
        self.clear()

    # ---------------- Segment 5: beam spread (§2.7.2-2.7.3) ----------------
    def seg5(self):
        c = lambda phrase, nth=1: self.cue(5, phrase, nth)
        S = self.start(5)
        ang = D.BEAM_HALF_ANGLES
        ref = BeamCone(-4.7, D.BEAM_CASES[0][1], ang[0])
        wide = BeamCone(0.0, D.BEAM_CASES[1][1], ang[1])
        narrow = BeamCone(4.7, D.BEAM_CASES[2][1], ang[2])

        def caption(cone, text):
            """The first caption line under a cone: its case and its half angle (a visual result)."""
            return label(text, FS_TAG - 2, INK, weight=BOLD).move_to([cone.x, -2.7, 0])
        cap_ref = caption(ref, f"4 MHz · 10 mm · {ang[0]:.1f}°")
        cap_wide = caption(wide, f"2 MHz · 10 mm · {ang[1]:.1f}°")
        cap_narrow = caption(narrow, f"4 MHz · 20 mm · {ang[2]:.1f}°")
        edge_lab = label("half angle, to the beam edge", FS_TAG - 2, GREY_INK).move_to([ref.x, -3.0, 0])

        # the first cone
        self.sync(S + 0.1)
        self.sync(c("تَتَّسِعُ"))
        self.play(FadeIn(ref.probe), run_time=0.3)
        self.play(FadeIn(ref.cone, scale=0.8, run_time=0.9), FadeIn(ref.axis), FadeIn(cap_ref))
        self.sync(c("كَمَخْرُوطٍ") + 0.3)
        self.play(Create(ref.guide), Create(ref.arc), FadeIn(edge_lab), run_time=0.7)
        # bigger crystal or higher frequency: a narrower beam
        up1 = tag_line("bigger crystal", "arrows-exchange", INK, width=3.4)
        up2 = tag_line("higher frequency", "wifi", INK, width=3.4)
        arrow_n = label("→ narrower beam", FS_NOTE, ACCENT_3, weight=BOLD)
        head = VGroup(up1, up2).arrange(RIGHT, buff=0.7)
        head_all = VGroup(head, arrow_n).arrange(RIGHT, buff=0.5).move_to([1.4, 3.4, 0])
        self.sync(c("كَبُرَتِ"))
        self.play(FadeIn(up1, shift=DOWN * 0.15), FadeIn(narrow.probe), run_time=0.4)
        self.play(FadeIn(narrow.cone, scale=0.8, run_time=0.8), FadeIn(narrow.axis), FadeIn(cap_narrow))
        self.play(Create(narrow.guide), Create(narrow.arc), run_time=0.5)
        self.sync(c("ارْتَفَعَ"))
        self.play(FadeIn(up2, shift=DOWN * 0.15), run_time=0.4)
        self.sync(c("ضَاقَتِ"))
        self.play(FadeIn(arrow_n, shift=LEFT * 0.15), run_time=0.4)
        # the narrow beam pins the flaw down
        yf = narrow.top_y - 3.0
        flaw_n = Ellipse(width=0.34, height=0.18, color=ACCENT_4, stroke_width=3).set_fill(ACCENT_4, 0.8)
        flaw_n.move_to([narrow.x, yf, 0])
        w_n = narrow.chord(3.0)
        span_n = DoubleArrow([narrow.x - w_n, yf - 0.35, 0], [narrow.x + w_n, yf - 0.35, 0], buff=0,
                             color=ACCENT_4, stroke_width=3, tip_length=0.12)
        note_n = label("narrow: precise position", FS_TAG - 2, ACCENT_3, weight=BOLD)
        self.sync(c("الضَّيِّقَةُ"))
        self.play(FadeIn(flaw_n, scale=0.5), Create(span_n), run_time=0.6)
        note_n.next_to(cap_narrow, DOWN, 0.1)
        self.play(FadeIn(note_n), run_time=0.3)
        # the wide beam covers more area
        self.sync(c("وَالوَاسِعَةُ"))
        self.play(FadeIn(wide.probe), run_time=0.3)
        self.play(FadeIn(wide.cone, scale=0.8, run_time=0.8), FadeIn(wide.axis), FadeIn(cap_wide))
        flaw_w = flaw_n.copy().move_to([wide.x, yf, 0])
        w_w = wide.chord(3.0)
        span_w = DoubleArrow([wide.x - w_w, yf - 0.35, 0], [wide.x + w_w, yf - 0.35, 0], buff=0,
                             color=ACCENT_4, stroke_width=3, tip_length=0.12)
        note_w = label("wide: more area covered", FS_TAG - 2, ACCENT_1, weight=BOLD).next_to(cap_wide, DOWN, 0.1)
        self.sync(c("تُغَطِّي"))
        self.play(FadeIn(flaw_w, scale=0.5), Create(span_w), run_time=0.6)
        self.play(FadeIn(note_w), run_time=0.3)
        # half the frequency, about twice the angle
        self.sync(c("فَإِذَا"))
        self.play(Create(wide.guide), Create(wide.arc), run_time=0.6)
        rule_w = label("½ frequency → about 2× angle", FS_TAG - 2, ACCENT_2, weight=BOLD)
        rule_w.next_to(note_w, DOWN, 0.1)
        self.sync(c("اتَّسَعَتِ"))
        self.play(FadeIn(rule_w), Indicate(cap_wide, color=ACCENT_2, scale_factor=1.1), run_time=0.6)
        # double the diameter, about half the angle
        self.sync(c("ضَاعَفْنَا"))
        rule_n = label("2× diameter → about ½ angle", FS_TAG - 2, ACCENT_2, weight=BOLD)
        rule_n.next_to(note_n, DOWN, 0.1)
        self.play(FadeIn(rule_n), Indicate(cap_narrow, color=ACCENT_2, scale_factor=1.1), run_time=0.6)
        self.sync(self.end(5))
        self.clear()

    # ---------------- Segment 6: attenuation (§2.8) ----------------
    def seg6(self):
        c = lambda phrase, nth=1: self.cue(6, phrase, nth)
        S = self.start(6)
        BW, BH = 5.6, 2.5
        # ---- two blocks: scattering at the grain boundaries, absorption into heat ----
        blk_s = Rectangle(width=BW, height=BH, color=INK, stroke_width=4).set_fill(PANEL_FILL, 1).move_to([-3.6, 0.9, 0])
        blk_a = Rectangle(width=BW, height=BH, color=INK, stroke_width=4).set_fill(PANEL_FILL, 1).move_to([3.6, 0.9, 0])
        fine = grain_lines(-6.4, -0.8, -0.35, 2.15, 0.62, seed=4)
        head_s = label("Scattering", FS_LABEL, INK, weight=BOLD).next_to(blk_s, UP, 0.15).align_to(blk_s, LEFT)
        head_a = label("Absorption", FS_LABEL, INK, weight=BOLD).next_to(blk_a, UP, 0.15).align_to(blk_a, LEFT)
        y_ax = 0.9
        def lane_pulse(x, color=ACCENT_1, amp=0.3):
            return wavefront(length=0.7, amp=amp, cycles=5, color=color, direction=RIGHT).move_to([x, y_ax, 0])
        self.sync(S + 0.1)
        self.play(FadeIn(blk_s), FadeIn(blk_a), FadeIn(head_s), FadeIn(head_a), run_time=0.6)
        # scattering: the pulse loses energy sideways at the boundaries
        self.sync(c("التَّشَتُّتُ"))
        self.play(Create(fine, lag_ratio=0.02, run_time=0.7))
        p_s = lane_pulse(-6.2)
        self.add(p_s)
        xs_hit = [-5.3, -4.4, -3.5, -2.6, -1.7]
        scat = VGroup()
        for k, xh in enumerate(xs_hit):
            self.play(p_s.animate(run_time=0.3, rate_func=linear).move_to([xh, y_ax, 0])
                      .stretch(0.8, 1).set_stroke(opacity=max(0.2, 0.85 - 0.14 * k)))
            for dy in (0.55, -0.55):
                a = Arrow([xh, y_ax + 0.05 * np.sign(dy), 0], [xh + 0.25, y_ax + dy, 0], buff=0, color=ACCENT_2,
                          stroke_width=3, tip_length=0.12)
                scat.add(a)
            self.add(scat[-2], scat[-1])
        # absorption: the pulse warms the material
        self.sync(c("وَالِامْتِصَاصُ"))
        p_a = lane_pulse(0.9)
        glow = Rectangle(width=BW - 0.2, height=BH - 0.2, color=ACCENT_2, stroke_width=0).set_fill(ACCENT_2, 0.0)
        glow.move_to(blk_a)
        heat = icon("flame", ACCENT_2, 0.6).move_to(blk_a.get_corner(UR) + LEFT * 0.4 + UP * 0.45)
        heat_t = label("heat", FS_TAG, INK, weight=BOLD).next_to(heat, LEFT, 0.12)
        self.add(glow, p_a)
        self.play(p_a.animate(run_time=2.2, rate_func=linear).move_to([6.3, y_ax, 0])
                  .stretch(0.35, 1).set_stroke(opacity=0.25),
                  glow.animate(run_time=2.2).set_fill(ACCENT_2, 0.3), FadeIn(heat, run_time=1.0),
                  FadeIn(heat_t, run_time=1.0))
        # ---- coarse grain scatters more; a higher frequency scatters more ----
        self.sync(c("وَيَزْدَادُ"))
        self.play(*[FadeOut(m) for m in (blk_a, head_a, glow, p_a, heat, heat_t)], FadeOut(scat), FadeOut(p_s),
                  run_time=0.5)
        coarse = grain_lines(-6.4, -0.8, -0.35, 2.15, 1.25, seed=7)
        self.play(ReplacementTransform(fine, coarse), run_time=0.8)
        coarse_t = tag_line("coarse grain: more scattering", "alert-triangle", ALERT_C, width=5.6, size=FS_NOTE)
        coarse_t.move_to([-3.6, -0.95, 0])
        self.sync(c("خُشُونَةِ"))
        self.play(FadeIn(coarse_t), run_time=0.4)
        p_c = lane_pulse(-6.2)
        self.add(p_c)
        self.play(p_c.animate(run_time=1.0, rate_func=linear).move_to([-3.4, y_ax, 0]).stretch(0.45, 1)
                  .set_stroke(opacity=0.35))
        # a higher frequency: tighter waves scatter more
        self.sync(c("ارْتِفَاعِ"))
        long_w = wavefront(length=1.1, amp=0.3, cycles=3, color=ACCENT_1, direction=RIGHT, n=3, spread=0.85)
        short_w = wavefront(length=0.5, amp=0.3, cycles=3, color=ACCENT_1, direction=RIGHT, n=5, spread=0.85)
        fr_lo = VGroup(long_w, label("low frequency", FS_TAG, INK, weight=BOLD)).arrange(DOWN, buff=0.15)
        fr_hi = VGroup(short_w, label("high frequency\nmore scattering", FS_TAG, ACCENT_2, weight=BOLD)).arrange(DOWN, buff=0.15)
        fr = VGroup(fr_lo, fr_hi).arrange(RIGHT, buff=0.6).move_to([3.6, 1.1, 0])
        self.play(FadeOut(p_c), FadeIn(fr_lo), run_time=0.4)
        self.play(FadeIn(fr_hi, shift=LEFT * 0.2), run_time=0.5)
        # ---- so coarse-grained parts are tested at a lower frequency ----
        self.sync(c("لِذٰلِكَ") - 0.2)
        self.play(FadeOut(fr), FadeOut(coarse_t), run_time=0.4)
        dial = FrequencyDial(radius=1.2).move_to([3.7, 0.2, 0])
        dial.set_value(0.8)
        self.play(FadeIn(dial), run_time=0.4)
        cast = chip_box("Castings", ACCENT_1, FS_NOTE)
        weld = chip_box("Austenitic steel welds", ACCENT_1, FS_NOTE)
        chips = VGroup(cast, weld).arrange(DOWN, buff=0.25).move_to([3.7, -2.0, 0])
        self.sync(c("كَالمَسْبُوكَاتِ"))
        self.play(FadeIn(cast, shift=UP * 0.15), run_time=0.4)
        self.sync(c("الأُوسْتِنِيتِيِّ"))
        self.play(FadeIn(weld, shift=UP * 0.15), run_time=0.4)
        self.sync(c("بِتَرَدُّدَاتٍ"))
        self.play(dial.animate.set_value(0.2), run_time=1.2)
        low_t = label("lower frequency", FS_NOTE, ACCENT_3, weight=BOLD).next_to(dial, UP, 0.25)
        self.play(FadeIn(low_t), run_time=0.3)
        # ---- the balance of episode 1: a high frequency finds smaller flaws but fades faster ----
        self.sync(c("وَهٰذَا") - 0.3)
        self.clear(run_time=0.5)
        x_ax = Arrow([-5.0, -2.2, 0], [5.0, -2.2, 0], buff=0, color=INK, stroke_width=3, tip_length=0.2)
        y_ax_ = Arrow([-5.0, -2.2, 0], [-5.0, 2.4, 0], buff=0, color=INK, stroke_width=3, tip_length=0.2)
        f_lbl = label("frequency", FS_TAG, INK).next_to(x_ax, DOWN, 0.1).align_to(x_ax, RIGHT)
        sens = Line([-4.6, -1.6, 0], [4.4, 1.6, 0], color=ACCENT_3, stroke_width=5)
        pen = Line([-4.6, 1.6, 0], [4.4, -1.6, 0], color=ACCENT_1, stroke_width=5)
        sens_t = label("Smaller flaws found", FS_NOTE, ACCENT_3, weight=BOLD).next_to(sens.get_end(), UP, 0.2).shift(LEFT * 1.0)
        pen_t = label("Penetration", FS_NOTE, ACCENT_1, weight=BOLD).next_to(pen.get_start(), UP, 0.2).shift(RIGHT * 1.0)
        self.play(Create(x_ax), Create(y_ax_), FadeIn(f_lbl), run_time=0.4)
        self.sync(c("يَكْشِفُ"))
        self.play(Create(sens), FadeIn(sens_t), run_time=0.8)
        self.sync(c("لٰكِنَّهُ"))
        self.play(Create(pen), FadeIn(pen_t), run_time=0.9)
        self.sync(self.end(6) - 0.3)
        self.clear(run_time=0.3)

    # ---------------- Segment 7: review, 8 questions (entries 7-31) ----------------
    def seg7(self):
        N_E = len(NARRATION)

        def mini_probe(width=0.9, height=0.5):
            p_ = Probe(width=width, height=height)
            p_.remove(p_.cable)
            return p_

        def art1():                       # voltage deforms the crystal, pressure makes a voltage
            cry = Crystal(-2.6, -1.5, width=2.6, height=1.3)
            tag = label("Crystal", FS_LABEL, ACCENT_1, weight=BOLD).next_to(cry, LEFT, 0.5)
            q = label("?", FS_TITLE, ACCENT_2, weight=BOLD).next_to(cry, RIGHT, 0.9)

            def show():
                self.play(FadeIn(cry), FadeIn(tag), FadeIn(q), run_time=0.6)
                self.play(cry.animate.set_h(1.55), run_time=0.4)
                self.play(cry.animate.set_h(1.3), run_time=0.4)

            def finish(*extra):
                volt = label("voltage → it deforms", FS_NOTE, ACCENT_2, weight=BOLD).next_to(cry, RIGHT, 0.5).shift(UP * 0.5)
                pres = label("pressure → it makes a voltage", FS_NOTE, ACCENT_4, weight=BOLD).next_to(cry, RIGHT, 0.5).shift(DOWN * 0.3)
                self.play(FadeOut(q), FadeIn(volt), FadeIn(pres), *extra, run_time=0.6)
            return show, finish

        def art2():                       # a thick and a thin crystal
            thick = Crystal(-3.0, -1.7, width=2.0, height=1.5)
            thin = Crystal(3.0, -1.7, width=2.0, height=0.7)
            lk = label("thick", FS_LABEL, INK, weight=BOLD).next_to(thick, DOWN, 0.2)
            ln = label("thin", FS_LABEL, INK, weight=BOLD).next_to(thin, DOWN, 0.2)
            qk = label("f ?", FS_LABEL, ACCENT_2, weight=BOLD).next_to(thick, UP, 0.25)
            qn = label("f ?", FS_LABEL, ACCENT_2, weight=BOLD).next_to(thin, UP, 0.25)

            def show():
                self.play(FadeIn(thick), FadeIn(thin), FadeIn(lk), FadeIn(ln), FadeIn(qk), FadeIn(qn), run_time=0.7)

            def finish(*extra):
                lo = label("lower frequency", FS_NOTE, ACCENT_1, weight=BOLD).move_to(qk)
                hi = label("higher frequency", FS_NOTE, ACCENT_1, weight=BOLD).move_to(qn)
                self.play(ReplacementTransform(qk, lo), ReplacementTransform(qn, hi), *extra, run_time=0.6)
            return show, finish

        def art3():                       # the damped pulse and the ringing pulse
            PULSES = [(0.0, 1.9), (3.0, 1.0), (3.45, 1.0)]
            strong = trace_panel(PULSES, tau=0.12, width=5.2, height=1.6).move_to([-3.4, -0.7, 0])
            light = trace_panel(PULSES, tau=0.7, width=5.2, height=1.6).move_to([3.4, -0.7, 0])
            hs = label("Strong damping", FS_NOTE, INK, weight=BOLD).next_to(strong, UP, 0.12)
            hl = label("Light damping", FS_NOTE, INK, weight=BOLD).next_to(light, UP, 0.12)
            qs = label("?", FS_TITLE, ACCENT_2, weight=BOLD).move_to(strong).shift(DOWN * 0.0)

            def show():
                self.play(FadeIn(strong.frame), FadeIn(strong.base), FadeIn(light.frame), FadeIn(light.base),
                          FadeIn(hs), FadeIn(hl), run_time=0.5)
                self.play(Create(strong.trace, rate_func=linear), Create(light.trace, rate_func=linear), run_time=1.0)

            def finish(*extra):
                a = tag_line("short pulse: resolution", "check", OK_C, width=4.6, size=FS_TAG).next_to(strong, DOWN, 0.15)
                b = tag_line("cost: sensitivity", "alert-triangle", ALERT_C, width=4.6, size=FS_TAG).next_to(light, DOWN, 0.15)
                self.play(FadeIn(a), FadeIn(b), *extra, run_time=0.6)
            return show, finish

        def art4():                       # a single-crystal dead zone hides a near-surface flaw, the twin probe sees it
            blk = SteelBlock(5.0, 1.6).move_to([0, -0.6, 0])
            top = blk.get_top()[1]
            dz = Rectangle(width=5.0, height=0.55, color=ACCENT_4, stroke_width=0).set_fill(ACCENT_4, 0.22)
            dz.align_to(blk, UP).match_x(blk)
            fl = Ellipse(width=0.55, height=0.16, color=ACCENT_4, stroke_width=3).set_fill(ACCENT_4, 0.7)
            fl.move_to([1.0, top - 0.3, 0])
            pr = mini_probe().next_to(blk, UP, 0)
            dz_t = label("dead zone: the flaw is hidden", FS_TAG, ACCENT_4, weight=BOLD).next_to(blk, DOWN, 0.15)

            def show():
                self.play(Create(blk), FadeIn(pr), FadeIn(dz), FadeIn(fl), FadeIn(dz_t), run_time=0.7)

            def finish(*extra):
                tp = VGroup(RoundedRectangle(width=1.1, height=0.5, corner_radius=0.07, color=INK, stroke_width=4).set_fill(BG, 1))
                c1 = Rectangle(width=0.42, height=0.1, color=ACCENT_1, stroke_width=2).set_fill(ACCENT_1, 1)
                c2 = Rectangle(width=0.42, height=0.1, color=ACCENT_2, stroke_width=2).set_fill(ACCENT_2, 1)
                tp.next_to(blk, UP, 0)
                c1.move_to(tp[0].get_bottom() + LEFT * 0.28 + UP * 0.05)
                c2.move_to(tp[0].get_bottom() + RIGHT * 0.28 + UP * 0.05)
                twin = VGroup(tp, c1, c2, Line(tp[0].get_top(), tp[0].get_bottom(), color=INK, stroke_width=5))
                ok = label("twin crystal: short dead zone, the flaw is seen", FS_TAG, OK_C, weight=BOLD).move_to(dz_t)
                self.play(FadeOut(pr), FadeIn(twin), dz.animate.stretch_to_fit_height(0.12).align_to(blk, UP),
                          ReplacementTransform(dz_t, ok), *extra, run_time=0.8)
                fly(self, pk(ACCENT_1, DOWN), [0.3, top + 0.3, 0], [1.0, top - 0.3, 0], 0.4)
                self.play(Flash(fl, color=ACCENT_4, flash_radius=0.4, line_length=0.12, run_time=0.4))
            return show, finish

        def art5():                       # the near field: the intensity swings
            N_MM = D.NEAR_FIELD
            sc = 0.11
            y0 = 0.75
            s_all = np.linspace(1.0, N_MM * 1.0, 700)
            xs0 = -2.0
            pts = [[xs0 + 2.6 * axis_intensity(s), y0 - s * sc, 0] for s in s_all]
            curve = VMobject(color=ACCENT_4, stroke_width=4).set_points_as_corners(pts)
            base = Line([xs0, y0, 0], [xs0, y0 - N_MM * sc, 0], color=GREY_INK, stroke_width=2)
            blk = SteelBlock(1.7, N_MM * sc).move_to([-3.4, y0 - N_MM * sc / 2, 0])
            pr = mini_probe().next_to(blk, UP, 0)
            lab = label("near field: intensity swings", FS_NOTE, ACCENT_4, weight=BOLD).move_to([3.4, 0.9, 0])
            sc_ = AScan([(0.0, 1.2), (3.2, 0.5), (4.1, 1.0), (5.0, 0.35)], width=3.6, height=1.6, t_min=-0.6,
                        t_max=7.0, ticks=(), sigma=0.14, x_caption="", y_caption="")
            sc_.shift(np.array([3.4, -0.5, 0.0]) - sc_.frame.get_center())
            sc_.update_trace(sc_.t_max)
            multi = label("one flaw, several indications", FS_TAG, ACCENT_4, weight=BOLD).next_to(sc_.frame, DOWN, 0.12)

            def show():
                self.play(Create(blk), FadeIn(pr), FadeIn(base), run_time=0.5)
                self.play(Create(curve, run_time=1.0, rate_func=linear), FadeIn(lab))

            def finish(*extra):
                self.play(FadeIn(sc_), FadeIn(sc_.trace), FadeIn(multi), *extra, run_time=0.6)
            return show, finish

        def art6():                       # the worked example's result: N = 16.9 mm
            N_MM = D.NEAR_FIELD
            sc = 0.11
            y0 = 0.85
            blk = SteelBlock(2.4, 2.2).move_to([-2.6, y0 - 1.1, 0])
            pr = mini_probe(D.PROBE_D_MM * sc / 0.85, 0.5).next_to(blk, UP, 0)
            beam = beam_outline(-2.6, y0, N_MM, D.PROBE_D_MM, D.BEAM_HALF_ANGLES[0], 20.0)
            ask = label("N = ?", FS_HEADING, ACCENT_4, weight=BOLD).move_to([2.8, -0.6, 0])
            tags = VGroup(label(f"{D.PROBE_D_MM:.0f} mm", FS_NOTE, INK, weight=BOLD),
                          label(f"{D.PROBE_F_MHZ:.0f} MHz", FS_NOTE, INK, weight=BOLD),
                          label("steel", FS_NOTE, INK, weight=BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            tags.move_to([2.8, 0.55, 0])
            yN = y0 - N_MM * sc
            mk = DashedLine([-4.2, yN, 0], [-1.0, yN, 0], color=ACCENT_4, stroke_width=3)
            dim = DoubleArrow([-4.35, y0, 0], [-4.35, yN, 0], buff=0, color=ACCENT_4, stroke_width=3, tip_length=0.14)
            res = label(f"N ≈ {D.NEAR_FIELD:.1f} mm", FS_HEADING, ACCENT_4, weight=BOLD).move_to([2.8, -0.6, 0])

            def show():
                self.play(Create(blk), FadeIn(pr), FadeIn(beam), FadeIn(tags), FadeIn(ask), run_time=0.7)

            def finish(*extra):
                self.play(Create(mk), Create(dim), ReplacementTransform(ask, res), *extra, run_time=0.7)
            return show, finish

        def art7():                       # a bigger crystal narrows the beam
            a = BeamCone(-3.4, D.BEAM_CASES[0][1], D.BEAM_HALF_ANGLES[0], top_y=0.7, depth=2.3, cable=False)
            b = BeamCone(3.4, D.BEAM_CASES[2][1], D.BEAM_HALF_ANGLES[2], top_y=0.7, depth=2.3, cable=False)
            qa = label("?", FS_TITLE, ACCENT_2, weight=BOLD).move_to([0, -0.4, 0])
            na = label("10 mm crystal", FS_TAG, INK, weight=BOLD).move_to([-3.4, -2.0, 0])
            nb = label("20 mm crystal", FS_TAG, INK, weight=BOLD).move_to([3.4, -2.0, 0])

            def show():
                self.play(FadeIn(a.probe), FadeIn(a.cone), FadeIn(a.axis), FadeIn(na), run_time=0.6)

            def finish(*extra):
                self.play(FadeIn(b.probe), FadeIn(b.cone), FadeIn(b.axis), FadeIn(nb), *extra, run_time=0.7)
                nar = label("narrower beam", FS_NOTE, ACCENT_3, weight=BOLD).move_to([0, -0.4, 0])
                self.play(FadeIn(nar), run_time=0.4)
            return show, finish

        def art8():                       # coarse grain scatters the sound, lower the frequency
            blk = Rectangle(width=6.0, height=2.4, color=INK, stroke_width=4).set_fill(PANEL_FILL, 1).move_to([-2.4, -0.5, 0])
            gr = grain_lines(-5.4, 0.6, -1.7, 0.7, 1.2, seed=5)
            cap = label("coarse-grained casting", FS_TAG, INK, weight=BOLD).next_to(blk, DOWN, 0.15)
            dial = FrequencyDial(radius=1.0).move_to([4.2, -1.0, 0])
            dial.set_value(0.8)

            def show():
                self.play(FadeIn(blk), Create(gr, lag_ratio=0.02), FadeIn(cap), FadeIn(dial), run_time=0.9)

            def finish(*extra):
                self.play(dial.animate.set_value(0.2), *extra, run_time=1.0)
                lo = label("lower frequency", FS_NOTE, ACCENT_3, weight=BOLD).next_to(dial, UP, 0.25)
                self.play(FadeIn(lo), run_time=0.3)
            return show, finish

        arts = [art1, art2, art3, art4, art5, art6, art7, art8]
        qs = [("Why can one crystal both send and receive sound?",
               "The piezoelectric effect: voltage moves it, pressure makes voltage"),
              ("How does a crystal's frequency change with its thickness?", "The thinner the crystal, the higher its frequency"),
              ("What is the backing for, and what does it cost?", "It stops the ringing, so resolution improves; it costs sensitivity"),
              ("Which probe for thin walls and flaws near the surface?", "The twin-crystal probe: its dead zone is short"),
              ("Why interpret flaws in the near field with care?", "Wave interference gives several indications and a changing amplitude"),
              (f"A {D.PROBE_D_MM:.0f} mm, {D.PROBE_F_MHZ:.0f} MHz probe in steel: how long is its near field?",
               f"About {D.NEAR_FIELD:.1f} mm"),
              ("What happens to the beam if the crystal is bigger or the frequency higher?",
               "It narrows, so the flaw position is more precise"),
              ("Why use a lower frequency on coarse-grained castings?",
               "Scattering grows with grain size and frequency, so the sound fades")]
        cards = [(q, (lambda scene, f=f: f()), a) for (q, a), f in zip(qs, arts)]
        run_review(self, cards, self.cue(7, "بِثَمَانِيَةِ"), self.cue(7, "ثَلَاثُ"), N_E)

    # SEGMENTS-END


if __name__ == "__main__":
    main(__file__, "UtSeriesEp02", NARRATION)
