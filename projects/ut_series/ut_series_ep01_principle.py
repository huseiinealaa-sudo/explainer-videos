"""ut_series, episode 1: Ultrasonic testing: the principle.

Build (from the repo root):
    python projects/ut_series/ut_series_ep01_principle.py --preview   # 480p15 -> tmp/ut_series_ep01_principle/preview.mp4
    python projects/ut_series/ut_series_ep01_principle.py             # 1080p30 -> output/ut_series_ep01_principle.mp4

Narration segments: 1-6 are the six sections of the source; 7 is the review intro and
8-31 are the eight review questions (question, 3 s silent countdown, answer).
"""
from explainer import *
import ut_series_data as D

# Fully diacritized narration (DRAFT, awaiting the owner's approval) — one entry per scene.
# Decimals are spoken digit by digit after «فَاصِلَةٌ».
NARRATION = [
    # 1  §1  what is UT
    "الفَحْصُ بِالمَوْجَاتِ فَوْقَ الصَّوْتِيَّةِ طَرِيقَةٌ لَا إِتْلَافِيَّةٌ: نُدْخِلُ فِي القِطْعَةِ مَوْجَاتٍ صَوْتِيَّةً عَالِيَةَ التَّرَدُّدِ. الأُذُنُ تَسْمَعُ حَتَّى عِشْرِينَ كِيلُوهِرْتْز، وَأَغْلَبُ الفَحْصِ بَيْنَ نِصْفِ مِيغَاهِرْتْز وَعِشْرِينَ مِيغَاهِرْتْز. تَفْقِدُ المَوْجَةُ بَعْضَ طَاقَتِهَا وَهِيَ تَسِيرُ، وَيُسَمَّى هٰذَا التَّوْهِينَ. وَنَقِيسُ الصَّدَى المُنْعَكِسَ عَنِ العُيُوبِ، أَوِ الشِّدَّةَ الوَاصِلَةَ إِلَى الوَجْهِ المُقَابِلِ. يُسْتَعْمَلُ لِكَشْفِ العُيُوبِ وَقِيَاسِ السَّمَاكَةِ وَتَقْدِيرِ بَعْضِ خَوَاصِّ المَادَّةِ وَبِنْيَتِهَا الحُبَيْبِيَّةِ. مِنْ مَزَايَاهُ: حَسَاسِيَّةٌ عَالِيَةٌ، وَاخْتِرَاقٌ يَبْلُغُ سِتَّةَ أَمْتَارٍ إِلَى سَبْعَةٍ مِنَ الفُولَاذِ، وَدِقَّةٌ فِي تَحْدِيدِ مَوْقِعِ العَيْبِ وَحَجْمِهِ، وَاسْتِجَابَةٌ سَرِيعَةٌ تَسْمَحُ بِالأَتْمَتَةِ، وَيَكْفِي سَطْحٌ وَاحِدٌ. وَمِنْ قُيُودِهِ: الشَّكْلُ الهَنْدَسِيُّ غَيْرُ المُلَائِمِ، وَالحُبَيْبَاتُ الخَشِنَةُ، وَالحَاجَةُ إِلَى وَسِيطٍ، وَتَأْثِيرُ اتِّجَاهِ العَيْبِ، وَالحَاجَةُ إِلَى مَرَاجِعَ وَمُعَايَرَةٍ، وَالسُّطُوحُ الخَشِنَةُ.",
    # 2  §2  wave properties
    "المَوْجَةُ الصَّوْتِيَّةُ اهْتِزَازٌ مِيكَانِيكِيٌّ: كُلُّ جُسَيْمٍ يَهْتَزُّ حَوْلَ مَوْضِعِهِ، وَالَّذِي يَنْتَقِلُ هُوَ الطَّاقَةُ لَا المَادَّةُ. لِذٰلِكَ تَحْتَاجُ وَسَطًا. التَّرَدُّدُ هُوَ عَدَدُ الِاهْتِزَازَاتِ فِي الثَّانِيَةِ، وَوَحْدَتُهُ الهِرْتْز. وَالسُّرْعَةُ تُحَدِّدُهَا المَادَّةُ وَنَوْعُ المَوْجَةِ، لَا التَّرَدُّدُ. وَالطُّولُ المَوْجِيُّ يُسَاوِي السُّرْعَةَ مَقْسُومَةً عَلَى التَّرَدُّدِ. فَفِي الفُولَاذِ، بِمِجَسٍّ خَمْسَةِ مِيغَاهِرْتْز، وَالسُّرْعَةُ خَمْسَةُ آلَافٍ وَتِسْعُ مِئَةٍ وَعِشْرُونَ مِتْرًا فِي الثَّانِيَةِ، يَكُونُ الطُّولُ المَوْجِيُّ وَاحِدًا فَاصِلَةً وَاحِدًا ثَمَانِيَةً أَرْبَعَةً مِلِّيمِتْرٍ. وَفِي المَاءِ صِفْرًا فَاصِلَةً اثْنَيْنِ تِسْعَةً سِتَّةً. لِمَاذَا نَرْفَعُ التَّرَدُّدَ؟ لِأَنَّ الطُّولَ الأَقْصَرَ يَكْشِفُ عُيُوبًا أَصْغَرَ، نَحْوَ نِصْفِ الطُّولِ المَوْجِيِّ أَوْ ثُلُثِهِ، لٰكِنَّهُ يَزِيدُ التَّوْهِينَ وَيُقَلِّلُ الِاخْتِرَاقَ. فَالِاخْتِيَارُ مُوَازَنَةٌ.",
    # 3  §3  wave types
    "لِلْمَوْجَاتِ أَنْوَاعٌ. فِي الطُّولِيَّةِ تَهْتَزُّ الجُسَيْمَاتُ فِي اتِّجَاهِ الِانْتِشَارِ نَفْسِهِ، وَتَنْتَقِلُ فِي الصُّلْبِ وَالسَّائِلِ وَالغَازِ، وَهِيَ الأَسْرَعُ. وَفِي المُسْتَعْرِضَةِ تَهْتَزُّ عَمُودِيًّا عَلَى الِاتِّجَاهِ، فَلَا تَنْتَقِلُ إِلَّا فِي الأَجْسَامِ الصُّلْبَةِ، لِأَنَّ السَّوَائِلَ وَالغَازَاتِ لَا تُقَاوِمُ القَصَّ. سُرْعَتُهَا فِي الفُولَاذِ ثَلَاثَةُ آلَافٍ وَمِئَتَانِ وَخَمْسُونَ مِتْرًا فِي الثَّانِيَةِ، أَيْ نَحْوُ خَمْسَةٍ وَخَمْسِينَ بِالمِئَةِ مِنَ الطُّولِيَّةِ. وَالسَّطْحِيَّةُ تَسِيرُ عَلَى السَّطْحِ بِعُمْقِ طُولٍ مَوْجِيٍّ وَاحِدٍ تَقْرِيبًا. وَمَوْجَاتُ لَامْبْ تَنْتَقِلُ فِي الصَّفَائِحِ الَّتِي لَا تَزِيدُ سَمَاكَتُهَا عَلَى ثَلَاثَةِ أَطْوَالٍ مَوْجِيَّةٍ. وَنُفَصِّلُهُمَا فِي الحَلْقَتَيْنِ القَادِمَتَيْنِ.",
    # 4  §4  impedance and reflection
    "المُعَاوَقَةُ الصَّوْتِيَّةُ هِيَ الكَثَافَةُ ضَرْبُ السُّرْعَةِ. وَعِنْدَ سُقُوطِ المَوْجَةِ عَمُودِيًّا عَلَى سَطْحٍ فَاصِلٍ، تَنْعَكِسُ نِسْبَةٌ هِيَ مُرَبَّعُ نَاتِجِ قِسْمَةِ فَرْقِ المُعَاوَقَتَيْنِ عَلَى مَجْمُوعِهِمَا، وَيَنْفُذُ البَاقِي. فِي الفُولَاذِ المُعَاوَقَةُ سِتَّةٌ وَأَرْبَعُونَ فَاصِلَةً أَرْبَعَةٌ سَبْعَةٌ مِيغَارَايْل، وَفِي المَاءِ وَاحِدٌ فَاصِلَةً أَرْبَعَةٌ ثَمَانِيَةٌ، فَيَنْعَكِسُ ثَمَانِيَةٌ وَثَمَانُونَ بِالمِئَةِ مِنَ الطَّاقَةِ. أَمَّا الهَوَاءُ فَمُعَاوَقَتُهُ أَرْبَعُ مِئَةٍ وَتِسْعًا وَعِشْرِينَ رَايْل فَقَطْ، فَيَنْعَكِسُ تِسْعَةٌ وَتِسْعُونَ فَاصِلَةً تِسْعَةٌ تِسْعَةٌ سِتَّةٌ بِالمِئَةِ. وَلِهٰذَا ثَلَاثُ نَتَائِجَ: طَبَقَةُ الهَوَاءِ بَيْنَ المِجَسِّ وَالقِطْعَةِ تَحْجُبُ الصَّوْتَ، فَنَضَعُ وَسِيطًا يَطْرُدُهَا. وَالعُيُوبُ المَمْلُوءَةُ بِالهَوَاءِ تَعْكِسُ بِقُوَّةٍ فَتَظْهَرُ. وَالجِدَارُ الخَلْفِيُّ يُعْطِي صَدًى قَوِيًّا.",
    # 5  §5  pulse-echo and the A-scan
    "فِي طَرِيقَةِ النَّبْضَةِ وَالصَّدَى يُرْسِلُ المِجَسُّ نَبْضَةً قَصِيرَةً ثُمَّ يَسْتَمِعُ. عَلَى شَاشَةِ إِيهْ سْكَانْ، المِحْوَرُ الأُفُقِيُّ هُوَ الزَّمَنُ، وَالعَمُودِيُّ سَعَةُ الصَّدَى. تَظْهَرُ النَّبْضَةُ الِابْتِدَائِيَّةُ، ثُمَّ صَدَى العَيْبِ إِنْ وُجِدَ، ثُمَّ صَدَى الجِدَارِ الخَلْفِيِّ. وَالعُمْقُ يُسَاوِي السُّرْعَةَ ضَرْبَ الزَّمَنِ مَقْسُومًا عَلَى اثْنَيْنِ، لِأَنَّ الصَّوْتَ يَقْطَعُ المَسَافَةَ ذَهَابًا وَإِيَابًا. لَوْحُ فُولَاذٍ سَمَاكَتُهُ خَمْسَةٌ وَعِشْرُونَ مِلِّيمِتْرًا: يَصِلُ صَدَى جِدَارِهِ الخَلْفِيِّ بَعْدَ ثَمَانِيَةٍ فَاصِلَةً أَرْبَعَةً خَمْسَةً مِيكْرُوثَانِيَةٍ، وَصَدَى عَيْبٍ عِنْدَ أَرْبَعَةٍ فَاصِلَةً صِفْرًا خَمْسَةً مِيكْرُوثَانِيَةٍ يَعْنِي عُمْقًا اثْنَيْ عَشَرَ مِلِّيمِتْرًا. وَلِهٰذَا تَلْزَمُ المُعَايَرَةُ: لَوْ ضُبِطَ الجِهَازُ عَلَى سُرْعَةِ الأَلُمْنْيُومِ وَنَحْنُ نَفْحَصُ الفُولَاذَ، لَقَرَأْنَا سَمَاكَةَ اللَّوْحِ سِتَّةً وَعِشْرِينَ فَاصِلَةً سَبْعَةً مِلِّيمِتْرٍ بَدَلَ خَمْسَةٍ وَعِشْرِينَ.",
    # 6  §6  the basic methods and the limits
    "لِلْفَحْصِ ثَلَاثُ طُرُقٍ. فِي النَّفَاذِ مِجَسَّانِ مُتَقَابِلَانِ، وَالعَيْبُ يَحْجُبُ جُزْءًا مِنَ الصَّوْتِ فَتَنْخَفِضُ الإِشَارَةُ، وَيَلْزَمُ الوُصُولُ إِلَى الجَانِبَيْنِ وَلَا يُعْطِي مَوْقِعَ العَيْبِ. وَفِي النَّبْضَةِ وَالصَّدَى مِجَسٌّ وَاحِدٌ مِنْ سَطْحٍ وَاحِدٍ يُعْطِي عُمْقَ العَيْبِ، وَهِيَ الأَكْثَرُ اسْتِعْمَالًا. وَفِي الرَّنِينِ نُغَيِّرُ التَّرَدُّدَ حَتَّى تُسَاوِيَ السَّمَاكَةُ نِصْفَ الطُّولِ المَوْجِيِّ لِنَقِيسَهَا. وَقُيُودُهَا: الوَسِيطُ ضَرُورِيٌّ، وَالعَيْبُ المُوَازِي لِلْحُزْمَةِ قَدْ لَا يُرَى، وَالحُبَيْبَاتُ الخَشِنَةُ تُشَتِّتُ الصَّوْتَ، وَلَا قِيَاسَ دُونَ مُعَايَرَةٍ.",
    # 7  §7  review: intro, then (question, 3 s countdown, answer) x 8
    "نُرَاجِعُ مَا تَعَلَّمْنَاهُ بِثَمَانِيَةِ أَسْئِلَةٍ. بَعْدَ كُلِّ سُؤَالٍ ثَلَاثُ ثَوَانٍ لِتُجِيبَ بِنَفْسِكَ.",
    "مَا مَدَى التَّرَدُّدَاتِ الَّذِي يَجْرِي بِهِ أَغْلَبُ الفَحْصِ؟", 3,
    "مِنْ نِصْفِ مِيغَاهِرْتْز إِلَى عِشْرِينَ مِيغَاهِرْتْز.",
    "لِمَاذَا نَضَعُ وَسِيطًا بَيْنَ المِجَسِّ وَالقِطْعَةِ؟", 3,
    "لِطَرْدِ الهَوَاءِ، لِأَنَّ سَطْحَ الفُولَاذِ مَعَ الهَوَاءِ يَعْكِسُ نَحْوَ تِسْعَةٍ وَتِسْعِينَ فَاصِلَةً تِسْعَةً تِسْعَةً سِتَّةً بِالمِئَةِ مِنَ الطَّاقَةِ.",
    "مَا الطُّولُ المَوْجِيُّ لِمِجَسٍّ خَمْسَةِ مِيغَاهِرْتْز فِي الفُولَاذِ؟", 3,
    "وَاحِدٌ فَاصِلَةً وَاحِدًا ثَمَانِيَةً أَرْبَعَةً مِلِّيمِتْرٍ.",
    "لِمَاذَا لَا تَنْتَقِلُ المَوْجَاتُ المُسْتَعْرِضَةُ فِي المَاءِ؟", 3,
    "لِأَنَّ السَّوَائِلَ لَا تُقَاوِمُ القَصَّ.",
    "مَاذَا يُمَثِّلُ مِحْوَرَا شَاشَةِ إِيهْ سْكَانْ؟", 3,
    "الأُفُقِيُّ الزَّمَنُ أَوِ المَسَافَةُ، وَالعَمُودِيُّ سَعَةُ الصَّدَى.",
    "صَدًى عِنْدَ أَرْبَعَةٍ فَاصِلَةً صِفْرًا خَمْسَةً مِيكْرُوثَانِيَةٍ فِي الفُولَاذِ، فَمَا عُمْقُ العَيْبِ؟", 3,
    "اثْنَا عَشَرَ مِلِّيمِتْرًا.",
    "لِمَاذَا نَقْسِمُ عَلَى اثْنَيْنِ فِي مُعَادَلَةِ العُمْقِ؟", 3,
    "لِأَنَّ الصَّوْتَ يَذْهَبُ وَيَعُودُ.",
    "مَا مَيْزَةُ النَّبْضَةِ وَالصَّدَى عَلَى النَّفَاذِ؟", 3,
    "تَكْفِي بِسَطْحٍ وَاحِدٍ وَتُعْطِي عُمْقَ العَيْبِ.",
]

# Every spoken or shown value is checked against the data module; stop if it drifts.
assert f"{D.LAMBDA_STEEL:.3f}" == "1.184" and f"{D.LAMBDA_WATER:.3f}" == "0.296"      # seg 2, Q3
assert f"{D.Z_STEEL:.2f}" == "46.47" and f"{D.Z_WATER:.2f}" == "1.48"                 # seg 4
assert f"{D.Z_AIR:.0f}" == "429"                                                       # seg 4
assert f"{D.R_STEEL_WATER * 100:.0f}" == "88" and f"{D.R_STEEL_AIR * 100:.3f}" == "99.996"
assert f"{D.T_BACKWALL_US:.2f}" == "8.45" and f"{D.T_FLAW_US:.2f}" == "4.05"          # seg 5, Q6
assert f"{D.FLAW_DEPTH_FROM_T:.1f}" == "12.0" and f"{D.READING_AL:.1f}" == "26.7"
assert f"{D.SHEAR_RATIO * 100:.0f}" == "55" and int(D.V_S_STEEL) == 3250               # seg 3

AUDIO_DIR = audio_dir_for(__file__)

# Colour roles of this project (project CLAUDE.md): ACCENT_1 sound / probe / incident wave,
# ACCENT_2 reflected wave / echo, ACCENT_3 transmitted wave / OK, ACCENT_4 flaw / alarm.


# ---------------- Drawing helpers (module level, shared by the segments) ----------------
# Each helper returns mobjects without animating them, takes no scene, and is parameterised so
# a later segment (and the review's mini drawings) can reuse it. Add new helpers below this line.

import numpy as np

# Numbers that only this segment speaks (not derived, not in the data module): the frequency
# range of the narration («عِشْرِينَ كِيلُوهِرْتْز», «نِصْفِ مِيغَاهِرْتْز … عِشْرِينَ مِيغَاهِرْتْز»,
# «سِتَّةَ أَمْتَارٍ إِلَى سَبْعَةٍ»). They are inputs, typed once here and used for every label.
AUDIBLE_MAX_KHZ = 20
UT_MIN_MHZ = 0.5
UT_MAX_MHZ = 20
PENETRATION_M = (6, 7)           # penetration in steel, metres


class FrequencyRuler(VGroup):
    """Log frequency axis with decade ticks; `band(f1, f2, ...)` gives a shaded band on it.

    Frequencies are in Hz. Positions are read from the axis at call time, so the ruler can be
    moved or scaled before the bands are made. Parts: axis, ticks, tick_labels, caption."""

    DECADES = [(1e1, "10 Hz"), (1e2, "100 Hz"), (1e3, "1 kHz"), (1e4, "10 kHz"),
               (1e5, "100 kHz"), (1e6, "1 MHz"), (1e7, "10 MHz"), (1e8, "100 MHz")]

    def __init__(self, width=11.5, f_min=1e1, f_max=1e8, size=FS_TAG - 2):
        axis = Line(LEFT * width / 2, RIGHT * width / 2, color=INK, stroke_width=4)
        ticks, labels = VGroup(), VGroup()
        for f, name in self.DECADES:
            if not f_min <= f <= f_max:
                continue
            x = -width / 2 + width * np.log10(f / f_min) / np.log10(f_max / f_min)
            t = Line([x, -0.09, 0], [x, 0.09, 0], color=INK, stroke_width=3)
            labels.add(label(name, size, INK).next_to(t, DOWN, 0.1))
            ticks.add(t)
        caption = label("frequency, log scale", size, GREY_INK)
        caption.next_to(labels, DOWN, 0.15).align_to(axis, RIGHT)
        super().__init__(axis, ticks, labels, caption)
        self.f_min, self.f_max = f_min, f_max
        self.axis, self.ticks, self.tick_labels, self.caption = axis, ticks, labels, caption

    def x_of(self, f):
        a, b = self.axis.get_start(), self.axis.get_end()
        return a[0] + (b[0] - a[0]) * np.log10(f / self.f_min) / np.log10(self.f_max / self.f_min)

    def band_rect(self, f1, f2, color, height=0.4):
        """Shaded band between f1 and f2 (Hz), standing on the axis."""
        x1, x2 = self.x_of(f1), self.x_of(f2)
        r = Rectangle(width=x2 - x1, height=height, color=color, stroke_width=3)
        r.set_fill(color, 0.3)
        return r.move_to([(x1 + x2) / 2, self.axis.get_y() + height / 2, 0])

    def band_label(self, rect, text, color=INK, size=FS_TAG):
        return label(text, size, color).next_to(rect, UP, 0.12)


class SteelBlock(VGroup):
    """A steel part seen in section: a filled rectangle. `body` is the rectangle."""

    def __init__(self, width=7.0, height=3.0):
        body = Rectangle(width=width, height=height, color=INK, stroke_width=4)
        body.set_fill(PANEL_FILL, 1)
        super().__init__(body)
        self.body = body


class Probe(VGroup):
    """An ultrasonic probe: housing, crystal (the face) and a cable stub. Its face is the
    bottom edge (the top edge when flip=True, a probe under a part). `face_point()` is the
    centre of the face."""

    def __init__(self, width=0.9, height=0.6, color=ACCENT_1, flip=False):
        housing = RoundedRectangle(width=width, height=height, corner_radius=0.08,
                                   color=color, stroke_width=4).set_fill(BG, 1)
        crystal = Rectangle(width=width * 0.85, height=0.12, color=color, stroke_width=3)
        crystal.set_fill(color, 1).next_to(housing, DOWN, buff=0)
        cable = Line(housing.get_top(), housing.get_top() + UP * 0.35, color=GREY_INK,
                     stroke_width=5)
        super().__init__(cable, housing, crystal)
        if flip:
            self.rotate(PI)
        self.housing, self.crystal, self.cable, self.flip = housing, crystal, cable, flip

    def face_point(self):
        return self.crystal.get_top() if self.flip else self.crystal.get_bottom()


def wave_packet(length=0.9, amp=0.28, cycles=5, color=ACCENT_1, direction=DOWN,
                stroke_width=4):
    """A short pulse (sine under a smooth envelope) centred on ORIGIN, travelling along
    `direction`. `amp` is its sideways size; `.stretch(k, 0)` shrinks it for attenuation
    when the direction is vertical."""
    def f(t):
        return np.array([amp * np.sin(PI * t) ** 2 * np.sin(TAU * cycles * t),
                         -(t - 0.5) * length, 0.0])
    m = ParametricFunction(f, t_range=[0, 1, 0.01], color=color, stroke_width=stroke_width)
    return m.rotate(angle_of_vector(direction) - angle_of_vector(DOWN))


class MethodSketch(VGroup):
    """Mini sketch of one way to read the sound. kind="echo": one probe on top, a flaw under
    it (pulse-echo). kind="through": a probe on each face and a received-signal meter
    (transmission). Parts: block, probe_a, flaw (echo), probe_b / meter_frame (through);
    `make_fill(level)` returns the meter fill (not part of the group, so it can grow)."""

    def __init__(self, kind="echo", width=4.6, height=2.2):
        block = SteelBlock(width, height)
        probe_a = Probe().next_to(block, UP, buff=0)
        parts = [block, probe_a]
        flaw = probe_b = frame = lab = None
        if kind == "echo":
            flaw = Ellipse(width=0.6, height=0.2, color=ACCENT_4, stroke_width=4)
            flaw.set_fill(ACCENT_4, 0.35).move_to(block.get_top() + DOWN * height * 0.4)
            parts.append(flaw)
        else:
            probe_b = Probe(color=ACCENT_3, flip=True).next_to(block, DOWN, buff=0)
            frame = Rectangle(width=1.5, height=0.26, color=INK, stroke_width=3)
            frame.next_to(probe_b, RIGHT, buff=0.4)
            lab = label("received signal", FS_TAG - 2, INK).next_to(frame, DOWN, 0.12)
            parts += [probe_b, frame, lab]
        super().__init__(*parts)
        self.kind, self.block, self.probe_a, self.flaw = kind, block, probe_a, flaw
        self.probe_b, self.meter_frame, self.meter_label = probe_b, frame, lab

    def beam_x(self):
        return self.block.get_center()[0]

    def make_fill(self, level=0.85):
        f = self.meter_frame
        r = Rectangle(width=(f.width - 0.08) * level, height=f.height - 0.08, color=ACCENT_3,
                      stroke_width=0).set_fill(ACCENT_3, 1)
        return r.align_to(f, LEFT).shift(RIGHT * 0.04).match_y(f)


def _wrap_two_lines(text, size):
    """The text as one label, or as two left-aligned lines split at the best space."""
    words = text.split()
    best = None
    for i in range(1, len(words)):
        a, b = label(" ".join(words[:i]), size), label(" ".join(words[i:]), size)
        w = max(a.width, b.width)
        if best is None or w < best[0]:
            best = (w, a, b)
    return best[1], best[2]


def chip(text, icon_name, color, width=4.1, size=FS_TAG - 1):
    """A short chip: a rounded frame in `color`, a Tabler icon, the text (wrapped to two lines
    when it does not fit). Returns a VGroup(frame, icon, text)."""
    room = width - 1.05
    one = label(text, size)
    if one.width <= room:
        txt = one
    else:
        a, b = _wrap_two_lines(text, size)
        txt = VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    frame = RoundedRectangle(width=width, height=max(0.62, txt.height + 0.4),
                             corner_radius=0.12, color=color, stroke_width=3).set_fill(PANEL_FILL, 1)
    ic = icon(icon_name, color, 0.42).move_to(frame.get_left() + RIGHT * 0.4)
    txt.move_to(frame).align_to(frame.get_left() + RIGHT * 0.75, LEFT)
    return VGroup(frame, ic, txt)


def chip_column(heading, items, color, width=4.1):
    """A column: a bold heading with a rule in `color`, then one chip per (text, icon) item.
    Returns VGroup(head, rule, chips) with .head, .rule, .chips."""
    head = label(heading, FS_BODY - 4, INK, weight=BOLD)
    rule = Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=5)
    chips = VGroup(*[chip(t, ic, color, width) for t, ic in items]).arrange(DOWN, buff=0.15)
    col = VGroup(head, rule, chips).arrange(DOWN, buff=0.15)
    col.head, col.rule, col.chips = head, rule, chips
    return col



class UtSeriesEp01(SyncedScene):
    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        self.seg1()
        self.seg2()
        self.seg3()
        self.seg4()
        self.seg5()
        self.seg6()
        self.seg7()

    # ---------------- Segment 1: what ultrasonic testing is (§1) ----------------
    def seg1(self):
        c = lambda phrase, nth=1: self.cue(1, phrase, nth)

        # ---- 0-4 s: title card, spoken while the title is on screen ----
        title_card(self, "Ultrasonic Testing", "The principle",
                   series="Ultrasonic Testing Series · Episode 1")
        self.sync(c("نُدْخِلُ") - 0.55)
        self.clear(run_time=0.5)

        # ---- 4-8 s: the part, the probe, high-frequency pulses go in ----
        block = SteelBlock(7.0, 3.0).move_to([0, -0.8, 0])
        probe = Probe().next_to(block, UP, buff=0)
        probe_tag = label("Probe", FS_NOTE).next_to(probe.housing, RIGHT, 0.25)
        block_tag = label("Steel part", FS_NOTE).next_to(block, DOWN, 0.2)
        top_y, bottom_y = block.get_top()[1], block.get_bottom()[1]
        x0 = block.get_center()[0]
        self.sync(c("نُدْخِلُ"))
        self.play(Create(block), FadeIn(probe, shift=DOWN * 0.5), run_time=0.8)
        self.play(FadeIn(probe_tag), FadeIn(block_tag), run_time=0.4)
        self.sync(c("مَوْجَاتٍ"))
        pulses = [wave_packet(length=0.8, amp=0.3, cycles=7) for _ in range(3)]
        for p_ in pulses:
            p_.move_to([x0, top_y - 0.4, 0])
        run = 1.5
        self.play(LaggedStart(*[Succession(
            FadeIn(p_, run_time=0.15),
            p_.animate(run_time=run, rate_func=linear).move_to([x0, bottom_y + 0.4, 0]))
            for p_ in pulses], lag_ratio=0.3))
        self.play(*[FadeOut(p_) for p_ in pulses], run_time=0.3)

        # ---- 8.7-15.2 s: the frequency ruler, the audible band, the UT band ----
        self.sync(c("الأُذُنُ"))
        ruler = FrequencyRuler(width=11.5)
        ruler.shift(UP * (2.45 - ruler.axis.get_y()))
        self.play(Create(ruler.axis), run_time=0.4)
        self.play(LaggedStart(*[AnimationGroup(Create(t), FadeIn(l))
                                for t, l in zip(ruler.ticks, ruler.tick_labels)],
                              lag_ratio=0.15), FadeIn(ruler.caption), run_time=0.9)
        self.sync(c("عِشْرِينَ"))
        audible = ruler.band_rect(20, AUDIBLE_MAX_KHZ * 1e3, GREY_INK)
        audible_tag = ruler.band_label(audible, f"Audible: up to {AUDIBLE_MAX_KHZ} kHz")
        self.play(GrowFromEdge(audible, LEFT), run_time=0.8)
        self.play(FadeIn(audible_tag), run_time=0.4)
        self.sync(c("نِصْفِ"))
        ut_band = ruler.band_rect(UT_MIN_MHZ * 1e6, UT_MAX_MHZ * 1e6, ACCENT_1)
        ut_tag = ruler.band_label(ut_band, f"Most UT: {UT_MIN_MHZ:g}–{UT_MAX_MHZ} MHz")
        self.play(GrowFromEdge(ut_band, LEFT), run_time=0.9)
        self.sync(c("وَعِشْرِينَ"))
        self.play(FadeIn(ut_tag), run_time=0.4)

        # ---- 16-21 s: attenuation: the pulse weakens as it travels ----
        self.sync(c("تَفْقِدُ"))
        run_pulse = wave_packet(length=0.9, amp=0.34, cycles=7)
        run_pulse.move_to([x0, top_y - 0.45, 0])
        self.play(FadeIn(run_pulse, run_time=0.2))
        self.play(run_pulse.animate(run_time=c("وَيُسَمَّى") - self.renderer.time + 0.2,
                                    rate_func=linear)
                  .move_to([x0, bottom_y + 0.55, 0]).stretch(0.25, 0).set_stroke(opacity=0.5))
        self.sync(c("التَّوْهِينَ"))
        ghosts = VGroup(
            wave_packet(length=0.9, amp=0.34, cycles=7).move_to([x0, top_y - 0.45 - 0.15, 0]),
            wave_packet(length=0.9, amp=0.34 * 0.6, cycles=7)
            .move_to([x0, (top_y + bottom_y) / 2 + 0.05, 0]))
        ghosts.set_stroke(opacity=0.45)
        attn = VGroup(label("Attenuation", FS_LABEL, INK, weight=BOLD),
                      label("energy lost\nalong the path", FS_TAG, GREY_INK)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        attn.next_to(block, RIGHT, 0.3).align_to(block, UP).shift(DOWN * 0.6)
        lead = Arrow(attn.get_left() + LEFT * 0.05, [x0 + 0.45, attn.get_left()[1] - 0.6, 0],
                     buff=0.0, stroke_width=3, color=ACCENT_1, tip_length=0.2)
        self.play(FadeIn(ghosts), FadeIn(attn, shift=LEFT * 0.2), GrowArrow(lead), run_time=0.7)

        # ---- 21.8-27.3 s: the two ways to read it ----
        self.sync(c("وَنَقِيسُ") - 0.6)
        self.clear(run_time=0.5)
        echo = MethodSketch("echo").move_to([-3.4, 0.45, 0])
        thru = MethodSketch("through").move_to([3.4, 0.45, 0])
        thru.shift(UP * (echo.block.get_center()[1] - thru.block.get_center()[1]))
        cap_y = thru.get_bottom()[1] - 0.4
        echo_cap = label("Pulse-echo: echo from the flaw", FS_TAG + 2).move_to([echo.get_x(), cap_y, 0])
        thru_cap = label("Transmission: intensity at the far face", FS_TAG + 2)
        thru_cap.move_to([thru.get_x(), cap_y, 0])
        self.sync(c("وَنَقِيسُ") - 0.1)
        self.play(FadeIn(echo), run_time=0.3)
        ex = echo.beam_x()
        e_top = echo.block.get_top()[1]
        e_flaw = echo.flaw.get_top()[1]
        go = wave_packet(length=0.7, amp=0.26, cycles=6).move_to([ex, e_top - 0.35, 0])
        self.play(FadeIn(echo_cap, run_time=0.4), FadeIn(go, run_time=0.15))
        self.play(go.animate(run_time=0.6, rate_func=linear).move_to([ex, e_flaw - 0.35, 0]))
        back = wave_packet(length=0.7, amp=0.26, cycles=6, color=ACCENT_2, direction=UP)
        back.move_to([ex, e_flaw + 0.35, 0])
        self.play(FadeOut(go, run_time=0.15), FadeIn(back, run_time=0.15),
                  Flash(echo.flaw, color=ACCENT_4, flash_radius=0.45, line_length=0.15,
                        run_time=0.4))
        self.play(back.animate(run_time=0.7, rate_func=linear).move_to([ex, e_top - 0.35 + 0.25, 0]))
        self.play(FadeOut(back, run_time=0.2))
        self.sync(c("أَوِ"))
        self.play(FadeIn(thru), FadeIn(thru_cap), run_time=0.4)
        tx = thru.beam_x()
        t_top, t_bot = thru.block.get_top()[1], thru.block.get_bottom()[1]
        sent = wave_packet(length=0.7, amp=0.26, cycles=6, color=ACCENT_3).move_to([tx, t_top - 0.35, 0])
        self.sync(c("الوَاصِلَةَ"))
        self.play(FadeIn(sent, run_time=0.15))
        self.play(sent.animate(run_time=1.1, rate_func=linear).move_to([tx, t_bot + 0.35, 0]))
        fill = thru.make_fill(0.85)
        self.play(FadeOut(sent, run_time=0.2), GrowFromEdge(fill, LEFT, run_time=0.7))

        # ---- 28-63 s: uses, advantages, limits, each chip when its word is spoken ----
        self.sync(c("يُسْتَعْمَلُ") - 0.7)
        self.clear(run_time=0.5)
        uses = chip_column("Uses", [("Flaw detection", "search"),
                                    ("Thickness gauging", "ruler"),
                                    ("Material properties and grain structure", "microscope")],
                           ACCENT_1)
        adv = chip_column("Advantages", [
            ("High sensitivity", "eye"),
            (f"{PENETRATION_M[0]}–{PENETRATION_M[1]} m penetration in steel", "arrows-exchange"),
            ("Accurate flaw position and size", "map-pin"),
            ("Fast response, allows automation", "bolt"),
            ("One surface is enough", "check")], ACCENT_3)
        lim = chip_column("Limits", [
            ("Unfavourable geometry", "tool"),
            ("Coarse grain", "filter"),
            ("Couplant needed", "droplet"),
            ("Flaw orientation matters", "refresh"),
            ("Reference blocks and calibration", "scale"),
            ("Rough surfaces", "wind")], ACCENT_4)
        cols = VGroup(uses, adv, lim).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to([0, 0.2, 0])
        events = [(c("يُسْتَعْمَلُ"), [uses.head, uses.rule])]
        events += list(zip([c(w) for w in ("لِكَشْفِ", "السَّمَاكَةِ", "خَوَاصِّ")], [[m] for m in uses.chips]))
        events += [(c("مَزَايَاهُ"), [adv.head, adv.rule])]
        events += list(zip([c(w) for w in ("حَسَاسِيَّةٌ", "وَاخْتِرَاقٌ", "وَدِقَّةٌ", "وَاسْتِجَابَةٌ", "وَيَكْفِي")],
                           [[m] for m in adv.chips]))
        events += [(c("قُيُودِهِ"), [lim.head, lim.rule])]
        events += list(zip([c(w) for w in ("الشَّكْلُ", "وَالحُبَيْبَاتُ", "وَسِيطٍ", "وَتَأْثِيرُ", "مَرَاجِعَ", "وَالسُّطُوحُ")],
                           [[m] for m in lim.chips]))
        for t, items in events:
            self.sync(t)
            self.play(*[FadeIn(m, shift=RIGHT * 0.2) for m in items], run_time=0.45)
        self.sync(self.end(1))
        self.clear()

    # ---------------- Segment 2: wave properties (§2) ----------------
    def seg2(self):
        self.sync(self.end(2))
        self.clear()

    # ---------------- Segment 3: wave types (§3) ----------------
    def seg3(self):
        self.sync(self.end(3))
        self.clear()

    # ---------------- Segment 4: impedance and reflection (§4) ----------------
    def seg4(self):
        self.sync(self.end(4))
        self.clear()

    # ---------------- Segment 5: pulse-echo and the A-scan (§5) ----------------
    def seg5(self):
        self.sync(self.end(5))
        self.clear()

    # ---------------- Segment 6: the basic methods and the limits (§6) ----------------
    def seg6(self):
        self.sync(self.end(6))
        self.clear()

    # ---------------- Segment 7: review (narration entries 7-31) ----------------
    # entry 7 intro; then for k = 1..8: question 8+3(k-1), silent 3 s countdown 9+3(k-1),
    # answer 10+3(k-1).
    def seg7(self):
        self.sync(self.end(len(NARRATION)) + 1.0)


if __name__ == "__main__":
    main(__file__, "UtSeriesEp01", NARRATION)
