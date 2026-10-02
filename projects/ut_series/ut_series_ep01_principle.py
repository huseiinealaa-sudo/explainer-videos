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
# «سِتَّةَ أَمْتَارٍ إِلَى سَبْعَةٍ»). They come from the data module and are used for every label.
AUDIBLE_MIN_HZ, AUDIBLE_MAX_KHZ = D.AUDIBLE_MIN_HZ, D.AUDIBLE_MAX_KHZ
UT_MIN_MHZ, UT_MAX_MHZ = D.UT_MIN_MHZ, D.UT_MAX_MHZ
PENETRATION_M = D.PENETRATION_M      # penetration in steel, metres


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


# ---- Segment 2 helpers: a particle chain that carries a pulse, a labelled wave, a flaw lane ----
UNITS_PER_MM = 2.2        # on-screen scale of the wavelength drawings (units per mm); steel and
                          # water share it, so their waves are drawn to the same scale


def _spring(a, b, y, coils=6, h=0.065, color=GREY_INK):
    """A zigzag spring between x = a and x = b on height y."""
    xs = np.linspace(a, b, 2 * coils + 1)
    pts = [[xs[0], y, 0]]
    pts += [[xs[k], y + (h if k % 2 else -h), 0] for k in range(1, 2 * coils)]
    pts.append([xs[-1], y, 0])
    s = VMobject(color=color, stroke_width=3)
    s.set_points_as_corners(pts)
    return s


class ParticleChain(VGroup):
    """A row of particles joined by springs, along which pulses run (a longitudinal wave).

    Every particle only oscillates about its rest place; the pulse is the envelope that moves.
    Positions are absolute (the chain is centred on x = 0 at height `y`; do not move it).
    `launches` are the times (on the chain's own clock) at which pulses start at `x_start`;
    the clock runs by the updater `advance(dt)` that the scene adds. The tagged particle
    (index `tag`) is drawn larger in `tag_color`; `ring` is the dashed ghost circle at its rest
    position and `guide` a short dashed vertical through it. `pulse_x(k)` is the centre of
    pulse k now."""

    def __init__(self, n=19, spacing=0.6, amp=0.17, wavelength=3.6, pulse_width=1.6, speed=2.6,
                 tag=9, y=0.0, radius=0.11, tag_radius=0.16, tag_color=ACCENT_1,
                 x_start=-9.0, launches=(), x0=0.0, transverse=False, guide_dir=None,
                 guide_len=0.55):
        self.n, self.spacing, self.amp, self.wavelength = n, spacing, amp, wavelength
        self.transverse = transverse
        self.pulse_width, self.speed, self.tag, self.y = pulse_width, speed, tag, y
        self.radius, self.tag_radius = radius, tag_radius
        self.x_start, self.launches, self.t = x_start, list(launches), 0.0
        self.rest = [x0 + (i - (n - 1) / 2) * spacing for i in range(n)]
        self.dots = VGroup(*[Dot([x, y, 0], radius=tag_radius if i == tag else radius,
                                 color=tag_color if i == tag else INK)
                             for i, x in enumerate(self.rest)])
        self.springs = VGroup(*[VMobject() for _ in range(n - 1)])
        super().__init__(self.springs, self.dots)
        self.update_to(0.0)
        self.ring = DashedVMobject(Circle(radius=tag_radius, color=GREY_INK, stroke_width=3)
                                   .move_to([self.rest[tag], y, 0]), num_dashes=14)
        g = np.array(guide_dir if guide_dir is not None else UP, dtype=float) * guide_len
        centre = np.array([self.rest[tag], y, 0.0])
        self.guide = DashedLine(centre - g, centre + g, color=GREY_INK, stroke_width=2)

    def pulse_x(self, k=0):
        return self.x_start + self.speed * (self.t - self.launches[k])

    def displacement(self, x0):
        u = 0.0
        for tl in self.launches:
            s = x0 - (self.x_start + self.speed * (self.t - tl))
            if abs(s) > 4 * self.pulse_width:
                continue
            u += self.amp * np.exp(-(s / self.pulse_width) ** 2) * np.sin(TAU * s / self.wavelength)
        return u

    def update_to(self, t):
        self.t = t
        if self.transverse:                    # particles move across the row; straight links
            ys = [self.y + self.displacement(x) for x in self.rest]
            for d, x, y_ in zip(self.dots, self.rest, ys):
                d.move_to([x, y_, 0])
            for i, sp in enumerate(self.springs):
                sp.set_points_as_corners([[self.rest[i], ys[i], 0], [self.rest[i + 1], ys[i + 1], 0]])
                sp.set_stroke(GREY_INK, 3)
            return
        xs = [x + self.displacement(x) for x in self.rest]
        for i, (d, x) in enumerate(zip(self.dots, xs)):
            d.move_to([x, self.y, 0])
        for i, sp in enumerate(self.springs):
            r0 = self.tag_radius if i == self.tag else self.radius
            r1 = self.tag_radius if i + 1 == self.tag else self.radius
            sp.set_points_as_corners(_spring(xs[i] + r0, xs[i + 1] - r1, self.y).get_anchors())
            sp.set_stroke(GREY_INK, 3)

    def advance(self, dt):
        self.update_to(self.t + dt)


class LabelledWave(VGroup):
    """A sine wave of wavelength `wavelength` (units) over `width`, built around the origin
    (`shift` it into place), with a crest-to-crest bracket labelled `tag`. Crests are at
    x = n * wavelength; the bracket spans crests `crest_n` and `crest_n + 1`.
    Parts: wave, dots (the two crests), guides, bracket, tag."""

    def __init__(self, wavelength=2.6, width=9.0, amp=0.45, color=ACCENT_1, tag="λ",
                 stroke_width=4, tag_size=FS_SYMBOL, crest_n=0):
        k = TAU / wavelength
        wave = ParametricFunction(lambda t: np.array([t, amp * np.cos(k * t), 0.0]),
                                  t_range=[-width / 2, width / 2, min(0.02, wavelength / 30)],
                                  color=color, stroke_width=stroke_width)
        xa = crest_n * wavelength
        xb = xa + wavelength
        yb = amp + 0.3
        dots = VGroup(*[Dot([x, amp, 0], radius=0.07, color=color) for x in (xa, xb)])
        guides = VGroup(*[DashedLine([x, amp + 0.08, 0], [x, yb, 0], color=GREY_INK,
                                     stroke_width=2) for x in (xa, xb)])
        bracket = DoubleArrow([xa, yb, 0], [xb, yb, 0], buff=0, color=INK, stroke_width=3,
                              tip_length=min(0.15, wavelength * 0.2))
        text = label(tag, tag_size, INK).next_to(bracket, UP, 0.08)
        super().__init__(wave, dots, guides, bracket, text)
        self.wave, self.dots, self.guides, self.bracket, self.tag = wave, dots, guides, bracket, text
        self.wavelength, self.amp = wavelength, amp


class ScatterLane(VGroup):
    """A strip of steel with a probe on its left end, a small flaw on its axis and a wave
    train that runs in from the probe. Built on the axis y = 0 (`shift` it into place and
    keep `self.y` equal to the shift). The incident wave is ACCENT_1, the part that goes
    on beyond the flaw ACCENT_3 (amplitude `transmit`), the echo ACCENT_2 (amplitude
    `reflect`, drawn above the axis). The scene adds `lane.add_updater(lambda m, dt: m.advance(dt))`
    and calls `start()` when the wave should leave the probe."""

    def __init__(self, wavelength, x0=-2.2, length=8.0, flaw_at=4.6, flaw_w=0.5, speed=1.6,
                 amp=0.26, transmit=1.0, reflect=0.1, height=1.7):
        self.x0, self.length, self.speed, self.amp = x0, length, speed, amp
        self.wavelength, self.transmit, self.reflect = wavelength, transmit, reflect
        self.xf, self.flaw_half = x0 + flaw_at, flaw_w / 2
        self.y, self.t, self.running = 0.0, 0.0, False
        rect = Rectangle(width=length, height=height, color=INK, stroke_width=3)
        rect.set_fill(PANEL_FILL, 1).move_to([x0 + length / 2, 0, 0])
        self.flaw = Ellipse(width=flaw_w, height=flaw_w * 0.8, color=ACCENT_4, stroke_width=3)
        self.flaw.set_fill(ACCENT_4, 0.5).move_to([self.xf, 0, 0])
        self.probe = Probe().rotate(PI / 2).next_to(rect, LEFT, buff=0)
        self.rect = rect
        self.inc, self.trn, self.ref = (VMobject(color=c, stroke_width=4)
                                        for c in (ACCENT_1, ACCENT_3, ACCENT_2))
        for m in (self.inc, self.trn, self.ref):
            m.set_points_as_corners([[x0, 0, 0], [x0 + 0.01, 0, 0]])
            m.set_stroke(opacity=0)
        super().__init__(rect, self.flaw, self.probe, self.inc, self.trn, self.ref)

    def start(self):
        self.running = True
        for m in (self.inc, self.trn, self.ref):
            m.set_stroke(opacity=1)

    def _curve(self, mob, xs, amp, y, phase):
        if len(xs) < 2:
            mob.set_points_as_corners([[self.x0, y, 0], [self.x0 + 0.01, y, 0]])
            mob.set_stroke(opacity=0)
            return
        k = TAU / self.wavelength
        pts = [[x, y + amp * np.sin(k * phase(x)), 0] for x in xs]
        mob.set_points_as_corners(pts)
        mob.set_stroke(opacity=1)

    def advance(self, dt):
        if not self.running:
            return
        self.t += dt
        c, t, x0 = self.speed, self.t, self.x0
        front = x0 + c * t
        xa = self.xf - self.flaw_half
        xb = self.xf + self.flaw_half
        x_end = x0 + self.length
        grid = lambda a, b: np.linspace(a, b, max(2, int((b - a) / 0.03)))
        # incident wave (from the probe to the flaw), then the part that goes on beyond it
        self._curve(self.inc, grid(x0, min(front, xa)) if front > x0 else [], self.amp,
                    self.y + 0.3, lambda x: x - x0 - c * t)
        self._curve(self.trn, grid(xb, min(front, x_end)) if front > xb else [],
                    self.amp * self.transmit, self.y + 0.3, lambda x: x - x0 - c * t)
        # the echo runs back from the flaw once the front has reached it
        t_hit = (xa - x0) / c
        if t > t_hit and self.reflect > 0:
            xr = xa - c * (t - t_hit)
            self._curve(self.ref, grid(max(xr, x0), xa) if xr < xa else [],
                        self.amp * self.reflect, self.y - 0.3,
                        lambda x: x + c * (t - t_hit) - xa)
        else:
            self._curve(self.ref, [], 0, self.y, lambda x: 0)



class WaveField(VGroup):
    """A grid of particles in a part (surface wave) or a plate (Lamb wave) with live motion.

    kind="surface": the grid hangs below the free surface `y_top`; the motion is an ellipse
    whose size dies away with depth (`wavelength` is the depth scale: about one wavelength).
    kind="lamb": a plate of thickness `plate_h` whose two faces move in opposite sense across
    the plate (symmetric mode). Columns are `dx` apart and centred on `x_c`; `depths` are the
    row depths below `y_top`. The scene adds `field.add_updater(lambda m, dt: m.advance(dt))`.
    `tag_col` is the column of the tagged particle on the top row; `path` is the dashed
    ellipse it follows (not part of the group, so the scene can show it at its cue)."""

    def __init__(self, kind, x_c, y_top, cols=8, dx=0.6, depths=(0.4, 0.9, 1.4, 1.9),
                 wavelength=2.4, amp=0.24, speed=1.2, plate_h=1.5, tag_col=3):
        self.kind, self.y_top, self.plate_h = kind, y_top, plate_h
        self.k = TAU / wavelength
        self.omega = self.k * speed
        self.amp, self.wavelength, self.t = amp, wavelength, 0.0
        self.xs = [x_c + (j - (cols - 1) / 2) * dx for j in range(cols)]
        self.depths = list(depths)
        self.cells = [(j, i) for i in range(len(self.depths)) for j in range(cols)]
        self.tag_col = tag_col
        dots = []
        for j, i in self.cells:
            tagged = (i == 0 and j == tag_col)
            dots.append(Dot(radius=0.14 if tagged else 0.075,
                            color=ACCENT_1 if tagged else INK))
        self.dots = VGroup(*dots)
        super().__init__(self.dots)
        ax, az = self._axes(0)
        self.path = DashedVMobject(
            Ellipse(width=2 * ax, height=2 * az, color=GREY_INK, stroke_width=3)
            .move_to([self.xs[tag_col], y_top - self.depths[0], 0]), num_dashes=24)
        self.update_to(0.0)

    def _amps(self, i):
        """Horizontal and vertical amplitude of row i."""
        if self.kind == "surface":
            f = float(np.exp(-2.2 * self.depths[i] / self.wavelength))
            return self.amp * f, 1.4 * self.amp * f
        s = (self.plate_h / 2 - self.depths[i]) / (self.plate_h / 2)     # +1 top face, -1 bottom
        return 0.6 * self.amp, 1.3 * self.amp * s

    def _axes(self, i):
        ax, az = self._amps(i)
        return ax, abs(az)

    def update_to(self, t):
        self.t = t
        for d, (j, i) in zip(self.dots, self.cells):
            x = self.xs[j]
            phi = self.k * x - self.omega * t
            ax, az = self._amps(i)
            d.move_to([x - ax * np.sin(phi), self.y_top - self.depths[i] + az * np.cos(phi), 0])

    def advance(self, dt):
        self.update_to(self.t + dt)


# ---- Segment 4 helpers: energy arrows, the reflection formula, the interface drawing ----
def energy_arrow(tail, head, thickness, color, head_len=0.34, head_extra=0.12):
    """A horizontal block arrow from `tail` to `head` whose shaft is `thickness` thick (the
    thickness stands for the share of the energy it carries). The head is a little wider than the
    shaft so that even a hairline shaft keeps a visible tip."""
    tx, ty = float(tail[0]), float(tail[1])
    hx = float(head[0])
    d = 1.0 if hx > tx else -1.0
    half = max(thickness, 0.012) / 2
    hh = max(half + head_extra, 0.13)
    xs = hx - d * head_len
    pts = [[tx, ty + half, 0], [xs, ty + half, 0], [xs, ty + hh, 0], [hx, ty, 0],
           [xs, ty - hh, 0], [xs, ty - half, 0], [tx, ty - half, 0]]
    arrow = Polygon(*pts, color=color, stroke_width=1.5)
    arrow.set_fill(color, 1)
    return arrow


def big_paren(height, side=LEFT, color=INK, stroke_width=4):
    """A tall round bracket: `side` = LEFT gives "(", RIGHT gives ")"."""
    sign = 1 if side is LEFT or np.allclose(side, LEFT) else -1
    arc = ArcBetweenPoints([0, height / 2, 0], [0, -height / 2, 0], angle=sign * 0.95,
                           color=color, stroke_width=stroke_width)
    return arc


class ReflectionFormula(VGroup):
    """R = ((Z₂ − Z₁) / (Z₂ + Z₁))²  and  T = 1 − R, built from Text pieces (no LaTeX), with the
    brackets drawn. Parts, so that a scene can reveal them one after the other:
    `r_lhs` ("R =") · `parens` (the two big brackets and the square) · `num` · `bar` · `den` ·
    `t_line` ("T = 1 − R"). The group is built at its final place: add each part with FadeIn."""

    def __init__(self, size=FS_EQUATION + 6, gap=1.1):
        mk = lambda s, col=INK, sz=size: Text(s, font_size=sz, color=col)
        r_lhs = VGroup(mk("R", ACCENT_2), mk("=")).arrange(RIGHT, buff=0.25)
        num, den = mk("(Z₂ − Z₁)"), mk("(Z₂ + Z₁)")
        w = max(num.width, den.width) + 0.2
        bar = Line(LEFT * w / 2, RIGHT * w / 2, color=INK, stroke_width=4)
        frac = VGroup(num, bar, den).arrange(DOWN, buff=0.14)
        h = frac.height + 0.35
        lp, rp = big_paren(h, LEFT), big_paren(h, RIGHT)
        quo = VGroup(lp, frac, rp).arrange(RIGHT, buff=0.14)
        sq = mk("2", INK, int(size * 0.62)).next_to(rp, UR, buff=0.04).shift(DOWN * 0.12)
        r_formula = VGroup(r_lhs, quo, sq).arrange(RIGHT, buff=0.28)
        sq.next_to(rp, UR, buff=0.04).shift(DOWN * 0.12)        # arrange moved it: re-place it
        t_line = VGroup(mk("T", ACCENT_3), mk("="), mk("1"), mk("−"), mk("R", ACCENT_2)
                        ).arrange(RIGHT, buff=0.22)
        t_line.next_to(r_formula, RIGHT, buff=gap)
        super().__init__(r_formula, t_line)
        self.r_lhs, self.num, self.bar, self.den, self.t_line = r_lhs, num, bar, den, t_line
        self.parens = VGroup(lp, rp, sq)
        self.lp, self.rp, self.sq = lp, rp, sq


def medium_tag(name, calc, result, result_color=INK):
    """The three lines under a medium: its name, the product that gives Z, and Z itself. Parts:
    `name_`, `calc_`, `result_` (arranged already, so each can be revealed on its own)."""
    n = label(name, FS_NOTE, INK, weight=BOLD)
    c = label(calc, FS_TAG, GREY_INK)
    r = label(result, FS_NOTE, result_color, weight=BOLD)
    g = VGroup(n, c, r).arrange(DOWN, buff=0.1)
    g.name_, g.calc_, g.result_ = n, c, r
    return g


class EnergyBar(VGroup):
    """A bar for the split of the energy: the left part is the reflected share (ACCENT_2, from the
    left), the right part the transmitted share (ACCENT_3, from the right). `frame`, `refl`, `trans`;
    `refl` and `trans` are not in the group (the scene grows them). The transmitted part keeps a
    minimum width of 0.015 so a share like 0.004 % still shows as a sliver."""

    def __init__(self, r_share, width=10.0, height=0.5):
        frame = Rectangle(width=width, height=height, color=INK, stroke_width=3)
        frame.set_fill(PANEL_FILL, 1)
        super().__init__(frame)
        self.frame = frame
        w_r = width * r_share
        w_t = max(width * (1 - r_share), 0.015)
        self.refl = Rectangle(width=w_r, height=height, color=ACCENT_2, stroke_width=0)
        self.refl.set_fill(ACCENT_2, 1).align_to(frame, LEFT).match_y(frame)
        self.trans = Rectangle(width=w_t, height=height, color=ACCENT_3, stroke_width=0)
        self.trans.set_fill(ACCENT_3, 1).align_to(frame, RIGHT).match_y(frame)


class CouplantRig(VGroup):
    """A probe held a gap above a part, with the tag "Probe" beside it. `gap_fill()` is the couplant
    that fills the gap (not in the group until `add`ed). Slide the group to move probe and film."""

    def __init__(self, x, surface_y, gap=0.9):
        self.surface_y, self.gap = surface_y, gap
        probe = Probe().next_to([x, surface_y + gap, 0], UP, buff=0)
        tag = label("Probe", FS_TAG, ACCENT_1, weight=BOLD).next_to(probe.housing, RIGHT, 0.2)
        super().__init__(probe, tag)
        self.probe, self.tag = probe, tag

    def face_y(self):
        return self.probe.face_point()[1]

    def x(self):
        return self.probe.face_point()[0]

    def gap_fill(self):
        w = self.probe.crystal.width
        f = Rectangle(width=w, height=self.gap, color=ACCENT_3, stroke_width=2)
        f.set_fill(ACCENT_3, 0.45)
        return f.move_to([self.x(), self.surface_y + self.gap / 2, 0])


# ---- Segment 5 helpers: the A-scan screen and the thickness gauge (the review reuses both) ----
class AScan(VGroup):
    """An A-scan screen: a framed plot with a time axis (µs) and an echo-amplitude axis.

    `peaks` is a list of (time µs, height in units); the signal is the sum of narrow peaks of
    width `sigma` µs on a flat baseline. Parts of the group: frame, x_axis, y_axis, ticks,
    tick_labels, x_caption, y_caption. `trace` (the signal drawn up to a time), `cursor` (a short
    vertical time cursor on the baseline) and `pen` (a dot on the tip of the trace) are not in the group: the scene adds them and calls
    `update_trace(t)` / `set_cursor(t)` (inside an updater when a clock drives them).
    Positions are read from the frame at call time, so `shift` / `move_to` the group first;
    do not scale it. `x_of(t)` is the screen x of time t, `apex(k)` the top of peak k."""

    def __init__(self, peaks, width=6.4, height=2.5, t_min=-0.6, t_max=10.0,
                 ticks=(0, 2, 4, 6, 8, 10), sigma=0.14, x_caption="Time (µs)",
                 y_caption="Echo amplitude"):
        self.peaks, self.t_min, self.t_max, self.sigma = list(peaks), t_min, t_max, sigma
        self._lx, self._rx = -width / 2 + 0.25, width / 2 - 0.3       # x of t_min / t_max
        self._by = -height / 2 + 0.55                                 # baseline, from the centre
        frame = Rectangle(width=width, height=height, color=INK, stroke_width=3)
        frame.set_fill(PANEL_FILL, 1)
        x_axis = Arrow([self._lx, self._by, 0], [width / 2 - 0.08, self._by, 0], buff=0,
                       color=INK, stroke_width=3, tip_length=0.16)
        y_axis = Arrow([self._lx, self._by, 0], [self._lx, height / 2 - 0.08, 0], buff=0,
                       color=INK, stroke_width=3, tip_length=0.16)
        tick_x = [self._lx + (t - t_min) * (self._rx - self._lx) / (t_max - t_min) for t in ticks]
        tick_marks = VGroup(*[Line([x, self._by, 0], [x, self._by + 0.1, 0], color=INK,
                                   stroke_width=3) for x in tick_x])
        tick_labels = VGroup(*[label(f"{t:g}", FS_TAG - 2, GREY_INK).move_to([x, self._by - 0.28, 0])
                               for t, x in zip(ticks, tick_x)])
        xc = label(x_caption, FS_TAG, INK).next_to(frame, DOWN, 0.1).align_to(frame, RIGHT)
        yc = label(y_caption, FS_TAG, INK).rotate(PI / 2).next_to(frame, LEFT, 0.1)
        super().__init__(frame, x_axis, y_axis, tick_marks, tick_labels, xc, yc)
        self.frame, self.x_axis, self.y_axis = frame, x_axis, y_axis
        self.ticks, self.tick_labels, self.x_caption, self.y_caption = tick_marks, tick_labels, xc, yc
        self.trace = VMobject(color=INK, stroke_width=3)
        self.trace.set_points_as_corners([[0, 0, 0], [0.01, 0, 0]]).set_stroke(opacity=0)
        self.cursor = Line(ORIGIN, UP, color=ACCENT_1, stroke_width=3)
        self.cursor.set_stroke(opacity=0)
        self.pen = Dot(ORIGIN, radius=0.08, color=ACCENT_1)           # rides the tip of the trace
        self.pen.set_opacity(0)

    def x_of(self, t):
        k = (self._rx - self._lx) / (self.t_max - self.t_min)
        return self.frame.get_center()[0] + self._lx + (t - self.t_min) * k

    def y_base(self):
        return self.frame.get_center()[1] + self._by

    def signal(self, t):
        return sum(a * np.exp(-((t - tp) / self.sigma) ** 2) for tp, a in self.peaks)

    def apex(self, k):
        tp, a = self.peaks[k]
        return np.array([self.x_of(tp), self.y_base() + a, 0.0])

    def update_trace(self, t_end, step=0.02):
        """Redraw `trace` from t_min up to t_end (µs)."""
        t_end = min(t_end, self.t_max)
        if t_end <= self.t_min + step:
            self.trace.set_stroke(opacity=0)
            self.pen.set_opacity(0)
            return self.trace
        ts = np.arange(self.t_min, t_end + 1e-9, step)
        pts = [[self.x_of(t), self.y_base() + self.signal(t), 0.0] for t in ts]
        self.trace.set_points_as_corners(pts)
        self.trace.set_stroke(color=INK, width=3, opacity=1)
        self.pen.set_opacity(1).move_to(pts[-1])
        return self.trace

    def set_cursor(self, t):
        """Put the cursor at time t (µs): a short bar standing on the baseline."""
        x = self.x_of(min(max(t, self.t_min), self.t_max))
        self.cursor.put_start_and_end_on([x, self.y_base() - 0.08, 0], [x, self.y_base() + 0.5, 0])
        self.cursor.set_stroke(opacity=1 if t >= self.t_min else 0)
        return self.cursor


class ThicknessGauge(VGroup):
    """A digital thickness gauge: a case with a display, an echo-time line and a velocity
    setting (one radio row per option). Parts: case, title, display, value (the reading text),
    echo (or None), head, rows (one `circle + text` group per option), marker (the filled dot of
    the selected row). `reading(text, color)` returns a new reading text placed on the display
    (Transform `value` into it); `marker_pos(k)` is where the marker sits for option k."""

    def __init__(self, reading, options, selected=0, echo_text=None, width=4.8, value_size=56,
                 reading_color=OK_C):
        self.value_size = value_size
        title = label("Thickness gauge", FS_NOTE, INK, weight=BOLD)
        display = Rectangle(width=width - 0.7, height=1.15, color=INK, stroke_width=3)
        display.set_fill(BG, 1)
        value = label(reading, value_size, reading_color, weight=BOLD)
        echo = label(echo_text, FS_TAG, GREY_INK) if echo_text else None
        head = label("Velocity setting", FS_TAG, GREY_INK)
        rows = VGroup()
        for name, v in options:
            ring = Circle(radius=0.12, color=INK, stroke_width=3)
            txt = label(f"{name}  {v:.0f} m/s", FS_LABEL - 4, INK)
            rows.add(VGroup(ring, txt).arrange(RIGHT, buff=0.25))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        stack = VGroup(title, display, *( [echo] if echo else [] ), head, rows)
        stack.arrange(DOWN, buff=0.28)
        head.align_to(display, LEFT)
        rows.align_to(display, LEFT).shift(RIGHT * 0.15)
        if echo:
            echo.align_to(display, LEFT)
        value.move_to(display)
        case = RoundedRectangle(width=width, height=stack.height + 0.5, corner_radius=0.15,
                                color=INK, stroke_width=4)
        case.set_fill(PANEL_FILL, 1).move_to(stack)
        self._rows = rows
        marker = Dot(rows[selected][0].get_center(), radius=0.07, color=ACCENT_1)
        super().__init__(case, stack, value, marker)
        self.case, self.title, self.display, self.value = case, title, display, value
        self.echo, self.head, self.rows, self.marker = echo, head, rows, marker

    def marker_pos(self, k):
        return self.rows[k][0].get_center()

    def reading(self, text, color):
        return label(text, self.value_size, color, weight=BOLD).move_to(self.display)


# ---- Segment 6 helpers: the three method panels ----
def tag_line(text, icon_name, color, width=3.9, size=FS_AXIS):
    """A short note without a frame: a Tabler icon in `color` and the text (two lines when it
    does not fit `width`). Parts: icon, txt."""
    ic = icon(icon_name, color, 0.4)
    room = width - 0.65
    one = label(text, size, INK)
    if one.width <= room:
        txt = one
    else:
        a, b = _wrap_two_lines(text, size)
        txt = VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    g = VGroup(ic, txt).arrange(RIGHT, buff=0.2)
    g.icon, g.txt = ic, txt
    return g


def method_head(text, cx, y_head, y_rule, color, width=3.8):
    """A panel heading (bold) centred on cx with a coloured rule under it."""
    head = label(text, FS_NOTE, INK, weight=BOLD)
    fit(head, width).move_to([cx, y_head, 0])
    rule = Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=5)
    rule.move_to([cx, y_rule, 0])
    return head, rule


def signal_bar(frame, level, color):
    """The fill of a horizontal meter `frame` up to `level` (0-1)."""
    r = Rectangle(width=max((frame.width - 0.08) * level, 0.02), height=frame.height - 0.08,
                  color=color, stroke_width=0).set_fill(color, 1)
    return r.align_to(frame, LEFT).shift(RIGHT * 0.04).match_y(frame)


def resonance_gain(f, width=0.12):
    """Received amplitude (0-1) of a plate driven at f, in units of its first resonance f1."""
    return 1.0 / (1.0 + ((f - 1.0) / width) ** 2)



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
        audible = ruler.band_rect(AUDIBLE_MIN_HZ, AUDIBLE_MAX_KHZ * 1e3, GREY_INK)
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
        c = lambda phrase, nth=1: self.cue(2, phrase, nth)
        S = self.start(2)

        # ---- A, 0-11 s: particles only oscillate, the energy travels; no medium, no wave ----
        chain_y = 0.5
        chain = ParticleChain(n=17, spacing=0.66, amp=0.2, wavelength=3.96, pulse_width=1.7,
                              tag=8, y=chain_y)
        bands = VGroup(*[Rectangle(width=2.4, height=0.9, color=ACCENT_1, stroke_width=0)
                         .set_fill(ACCENT_1, 0) for _ in range(2)])

        def move_bands(m):
            for k, b in enumerate(m):
                if k >= len(chain.launches):
                    continue
                xc = chain.pulse_x(k)
                b.move_to([xc, chain_y, 0])
                b.set_fill(ACCENT_1, 0.16 * float(np.clip(4.8 - abs(xc), 0, 1)))
        bands.add_updater(move_bands)
        self.add(bands)
        self.play(FadeIn(chain), FadeIn(chain.ring), FadeIn(chain.guide), run_time=0.7)
        T0 = self.renderer.time
        chain.launches = [S + 0.3 - T0, S + 2.6 - T0]          # pulse 1 and pulse 2
        move_bands(bands)
        chain.add_updater(lambda m, dt: m.advance(dt))

        energy_on = ValueTracker(0)
        energy = VGroup(Arrow(LEFT * 0.7, RIGHT * 0.7, buff=0, color=ACCENT_1, stroke_width=5,
                              tip_length=0.2),
                        label("energy", FS_NOTE, ACCENT_1))
        energy[1].next_to(energy[0], UP, 0.08)
        energy.add_updater(lambda m: (m.move_to([chain.pulse_x(1), chain_y + 1.0, 0]),
                                      m.set_opacity(energy_on.get_value())))
        self.add(energy)

        note = VGroup(label("Each particle moves back and forth", FS_NOTE),
                      label("about its rest place (dashed ring)", FS_NOTE)
                      ).arrange(DOWN, buff=0.08).next_to(chain.guide, DOWN, 0.25)
        matter = label("Matter stays, energy moves", FS_LABEL, INK, weight=BOLD)
        matter.next_to(note, DOWN, 0.25)
        self.sync(c("جُسَيْمٍ"))
        self.play(FadeIn(note), run_time=0.5)
        self.sync(c("يَنْتَقِلُ"))
        self.play(energy_on.animate.set_value(1), run_time=0.4)
        self.sync(c("المَادَّةُ"))
        self.play(FadeIn(matter), run_time=0.4)
        self.sync(S + 7.75)
        self.play(energy_on.animate.set_value(0), run_time=0.4)
        self.sync(c("لِذٰلِكَ"))
        chain.clear_updaters()
        energy.clear_updaters()
        bands.clear_updaters()
        self.play(FadeOut(bands), FadeOut(chain), FadeOut(chain.ring), FadeOut(chain.guide), FadeOut(note),
                  FadeOut(matter), FadeOut(energy), run_time=0.6)
        self.sync(c("تَحْتَاجُ"))
        lone = wave_packet(length=1.1, amp=0.3, cycles=5, direction=RIGHT)
        lone.move_to([-3.5, chain_y, 0])
        none_tag = label("No medium, no wave", FS_HEADING, INK, weight=BOLD).move_to([0, -0.9, 0])
        self.play(FadeIn(lone, run_time=0.2))
        self.play(AnimationGroup(
            lone.animate(run_time=0.9, rate_func=linear).shift(RIGHT * 2.0).set_stroke(opacity=0),
            Succession(Wait(max(0.01, c("وَسَطًا") - self.renderer.time)),
                       FadeIn(none_tag, run_time=0.4))))
        self.sync(c("التَّرَدُّدُ") - 0.4)
        self.clear(run_time=0.4)

        # ---- B1, 11.5-16.6 s: frequency = cycles per second ----
        self.sync(c("التَّرَدُّدُ"))
        head = label("Frequency, f", FS_HEADING, INK, weight=BOLD).move_to([0, 2.8, 0])
        self.play(FadeIn(head), run_time=0.4)
        W, cycles, amp, y_s = 8.0, 5, 0.65, 1.1
        axis = Arrow([-W / 2 - 0.2, y_s, 0], [W / 2 + 0.5, y_s, 0], buff=0, color=GREY_INK,
                     stroke_width=3, tip_length=0.2)
        time_lbl = label("time", FS_TAG, GREY_INK).next_to(axis.get_end(), DOWN, 0.1)
        sine = ParametricFunction(
            lambda t: np.array([t, y_s + amp * np.sin(TAU * cycles * (t + W / 2) / W), 0.0]),
            t_range=[-W / 2, W / 2, 0.02], color=ACCENT_1, stroke_width=5)
        sine_time = 1.2
        crest_dots = []
        for k in range(cycles):
            x = -W / 2 + (k + 0.25) * W / cycles
            d = Dot([x, y_s + amp, 0], radius=0.09, color=ACCENT_2)
            crest_dots.append(Succession(Wait((x + W / 2) / W * sine_time),
                                         GrowFromCenter(d, run_time=0.2)))
        self.sync(c("عَدَدُ") - 0.25)
        self.play(Create(axis), FadeIn(time_lbl), run_time=0.25)
        self.play(Create(sine, rate_func=linear, run_time=sine_time), *crest_dots)
        self.sync(c("الثَّانِيَةِ"))
        y_b = 0.0
        one_s = VGroup(DoubleArrow([-W / 2, y_b, 0], [W / 2, y_b, 0], buff=0, color=INK,
                                   stroke_width=3, tip_length=0.15),
                       label("1 second", FS_LABEL, INK)).arrange(DOWN, buff=0.1)
        self.play(FadeIn(one_s, run_time=0.5))
        self.sync(c("الثَّانِيَةِ") + 0.5)
        per_s = label("f = number of cycles per second", FS_LABEL, INK, weight=BOLD)
        per_s.next_to(one_s, DOWN, 0.5)
        self.play(FadeIn(per_s, run_time=0.3))
        self.sync(c("وَوَحْدَتُهُ"))
        unit = label("Unit: hertz (Hz)", FS_LABEL, ACCENT_1, weight=BOLD).next_to(per_s, DOWN, 0.3)
        self.play(FadeIn(unit, run_time=0.4))
        self.sync(c("وَالسُّرْعَةُ") - 0.35)
        self.clear(run_time=0.35)

        # ---- B2, 17-21 s: the speed is set by the material, not by f ----
        self.sync(c("وَالسُّرْعَةُ"))
        h1 = label("Speed v: set by the material and the wave type", FS_LABEL + 2, INK,
                   weight=BOLD).move_to([0, 2.8, 0])
        h2 = label("not by the frequency: both pulses have the same f", FS_LABEL, GREY_INK)
        h2.next_to(h1, DOWN, 0.2)
        lane_w = 8.4
        lanes = VGroup(*[Rectangle(width=lane_w, height=1.0, color=INK, stroke_width=3)
                         .set_fill(PANEL_FILL, 1) for _ in range(2)]).arrange(DOWN, buff=0.7)
        lanes.move_to([0.9, 0.1, 0])
        names = VGroup(label("Steel", FS_NOTE, INK).next_to(lanes[0], LEFT, 0.25),
                       label("Water", FS_NOTE, INK).next_to(lanes[1], LEFT, 0.25))
        self.play(FadeIn(h1), FadeIn(lanes), FadeIn(names), run_time=0.5)
        ratio = D.V_L_STEEL / D.V_WATER                    # 4.0: steel is four times faster
        t_move_w = 3.45
        t_move_s = t_move_w / ratio
        xs0, xs1 = lanes[0].get_left()[0] + 0.7, lanes[0].get_right()[0] - 0.7
        mk = lambda lane: wave_packet(length=0.9, amp=0.27, cycles=5, direction=RIGHT
                                      ).move_to([xs0, lane.get_center()[1], 0])
        steel_runs = []
        for _ in range(round(ratio)):
            p_ = mk(lanes[0])
            steel_runs += [FadeIn(p_, run_time=0.03),
                           p_.animate(run_time=t_move_s, rate_func=linear).move_to(
                               [xs1, lanes[0].get_center()[1], 0]),
                           FadeOut(p_, run_time=0.03)]
        water_p = mk(lanes[1])
        water_run = Succession(FadeIn(water_p, run_time=0.15),
                               water_p.animate(run_time=t_move_w, rate_func=linear).move_to(
                                   [xs1, lanes[1].get_center()[1], 0]))
        self.sync(c("تُحَدِّدُهَا") - 0.3)
        lead = max(0.01, c("التَّرَدُّدُ", 2) - self.renderer.time)
        self.play(AnimationGroup(Succession(*steel_runs), water_run,
                                 Succession(Wait(lead), FadeIn(h2, run_time=0.4))))
        self.sync(c("وَالطُّولُ") - 0.3)
        self.clear(run_time=0.3)

        # ---- C, 21.7-44 s: wavelength, λ = v ÷ f, steel and water at 5 MHz ----
        self.sync(c("وَالطُّولُ"))
        steel_lw = LabelledWave(D.LAMBDA_STEEL * UNITS_PER_MM, tag="λ  (wavelength)")
        steel_lw.shift(UP * 2.35)
        self.play(Create(steel_lw.wave, run_time=0.55))
        self.play(FadeIn(steel_lw.dots), FadeIn(steel_lw.guides), GrowFromCenter(steel_lw.bracket),
                  FadeIn(steel_lw.tag), run_time=0.45)
        self.sync(c("يُسَاوِي"))
        eq = equation(self, ["λ", "=", "v", "÷", "f"], colors={0: ACCENT_1}, size=FS_EQUATION + 4,
                      pos=[0, 0.6, 0], run_time=1.0, buff=0.9)
        caps = VGroup(*[label(t, FS_TAG, GREY_INK).next_to(eq[k], DOWN, 0.15)
                        for k, t in ((0, "wavelength"), (2, "speed"), (4, "frequency"))])
        self.sync(c("السُّرْعَةَ") + 0.55)
        self.play(FadeIn(caps[0]), FadeIn(caps[1]), run_time=0.4)
        self.sync(c("التَّرَدُّدِ"))
        self.play(FadeIn(caps[2]), run_time=0.4)
        self.sync(c("فَفِي") - 0.35)
        self.play(FadeOut(eq), FadeOut(caps), run_time=0.35)
        f_txt = f"{D.F_PROBE:g} MHz"
        self.sync(c("فَفِي"))
        steel_name = label("Steel", FS_NOTE, INK).next_to(steel_lw.wave, LEFT, 0.25)
        self.play(FadeIn(steel_name), run_time=0.3)
        steel_calc = worked_calculation(
            self, ["λ steel", "=", "v", "÷", "f"],
            ["λ", "=", f"{D.V_L_STEEL:.0f} m/s", "÷", f_txt],
            f"= {D.LAMBDA_STEEL:.3f} mm",
            cues=[c("فَفِي") + 0.3, c("وَالسُّرْعَةُ", 2), c("وَاحِدًا")],
            pos=[0, -1.85, 0], size=30)
        self.sync(c("وَفِي") - 0.65)
        self.play(steel_calc.animate.shift(LEFT * 3.4), run_time=0.5)
        water_calc = worked_calculation(
            self, ["λ water", "=", "v", "÷", "f"],
            ["λ", "=", f"{D.V_WATER:.0f} m/s", "÷", f_txt],
            f"= {D.LAMBDA_WATER:.3f} mm",
            cues=[c("وَفِي"), c("وَفِي") + 1.0, c("وَفِي") + 2.0],
            pos=[3.4, -1.85, 0], size=30)
        water_lw = LabelledWave(D.LAMBDA_WATER * UNITS_PER_MM, tag="λ", stroke_width=3)
        water_lw.shift(UP * 0.95)
        water_name = label("Water", FS_NOTE, INK).next_to(water_lw.wave, LEFT, 0.25)
        self.sync(c("صِفْرًا") + 2.0)
        self.play(Create(water_lw.wave, run_time=0.5), FadeIn(water_name))
        self.play(FadeIn(water_lw.dots), FadeIn(water_lw.guides), GrowFromCenter(water_lw.bracket),
                  FadeIn(water_lw.tag), run_time=0.4)
        self.sync(c("لِمَاذَا") - 0.4)
        self.clear(run_time=0.4)

        # ---- D, 44-58 s: a short wave sees a small flaw; the price is penetration ----
        self.sync(c("لِمَاذَا"))
        lane_long = ScatterLane(3.0, transmit=0.95, reflect=0.08)
        lane_short = ScatterLane(1.0, transmit=0.45, reflect=0.6)
        for lane, y in ((lane_long, 2.55), (lane_short, 0.6)):
            lane.shift(UP * y)
            lane.y = y
        tags = VGroup(
            VGroup(label("Long wave", FS_NOTE, INK, weight=BOLD),
                   label("low frequency", FS_TAG, GREY_INK)).arrange(DOWN, aligned_edge=RIGHT,
                                                                       buff=0.06),
            VGroup(label("Short wave", FS_NOTE, INK, weight=BOLD),
                   label("high frequency", FS_TAG, GREY_INK)).arrange(DOWN, aligned_edge=RIGHT,
                                                                        buff=0.06))
        for tg, lane in zip(tags, (lane_long, lane_short)):
            tg.next_to(lane.probe, LEFT, 0.3)
        self.play(FadeIn(lane_long), FadeIn(lane_short), FadeIn(tags), run_time=0.7)
        lane_long.add_updater(lambda m, dt: m.advance(dt))
        lane_short.add_updater(lambda m, dt: m.advance(dt))
        self.sync(c("لِأَنَّ") + 0.15)
        lane_long.start()
        lane_short.start()
        note_d = label(f"Smallest flaw seen ≈ λ/2 to λ/3 = {D.MIN_FLAW_HALF:.3f}–"
                       f"{D.MIN_FLAW_THIRD:.3f} mm (steel, {f_txt})", FS_NOTE, INK)
        note_d.move_to([0, -0.55, 0])
        self.sync(c("نَحْوَ"))
        self.play(FadeIn(note_d), run_time=0.4)
        # trade-off chart: sensitivity rises with f, penetration falls
        ay0 = -3.2
        x_ax = Arrow([-3.0, ay0, 0], [3.2, ay0, 0], buff=0, color=GREY_INK, stroke_width=3,
                     tip_length=0.18)
        y_ax = Arrow([-3.0, ay0, 0], [-3.0, -1.2, 0], buff=0, color=GREY_INK, stroke_width=3,
                     tip_length=0.18)
        f_lbl = label("frequency f", FS_TAG, GREY_INK).next_to(x_ax.get_end(), DOWN, 0.1)
        sens = Line([-2.8, -2.8, 0], [3.0, -1.5, 0], color=ACCENT_3, stroke_width=5)
        pen = Line([-2.8, -1.5, 0], [3.0, -2.8, 0], color=ACCENT_1, stroke_width=5)
        sens_t = label("Sensitivity", FS_TAG, ACCENT_3, weight=BOLD).next_to(sens.get_end(), RIGHT, 0.15)
        pen_t = label("Penetration", FS_TAG, ACCENT_1, weight=BOLD).next_to(pen.get_end(), RIGHT, 0.15)
        self.sync(c("لٰكِنَّهُ") - 0.3)
        self.play(Create(x_ax), Create(y_ax), FadeIn(f_lbl), run_time=0.3)
        self.play(Create(sens), FadeIn(sens_t), run_time=0.6)
        self.sync(c("التَّوْهِينَ"))
        self.play(Create(pen, run_time=1.4), FadeIn(pen_t, run_time=0.4))
        self.sync(c("فَالِاخْتِيَارُ"))
        cross = Dot([0.1, -2.15, 0], radius=0.11, color=INK)
        bal = label("balance", FS_LABEL, INK, weight=BOLD).next_to(cross, UP, 0.45)
        self.play(GrowFromCenter(cross), FadeIn(bal), run_time=0.5)
        lane_long.clear_updaters()
        lane_short.clear_updaters()
        self.sync(self.end(2))
        self.clear()

    # ---------------- Segment 3: wave types (§3) ----------------
    def seg3(self):
        c = lambda phrase, nth=1: self.cue(3, phrase, nth)
        S = self.start(3)
        ratio = D.SHEAR_RATIO

        # ---- A, 0-20 s: two panels run side by side; the solid / liquid / gas table ----
        PW, P_TOP, P_BOT = 6.5, 3.8, 0.05
        xc_l, xc_t = -3.5, 3.5
        frames = VGroup(*[RoundedRectangle(width=PW, height=P_TOP - P_BOT, corner_radius=0.12,
                                           color=GREY_INK, stroke_width=3).set_fill(PANEL_FILL, 1)
                          .move_to([x, (P_TOP + P_BOT) / 2, 0]) for x in (xc_l, xc_t)])

        def lattice(x_c, transverse):
            """Three rows of 15 particles; the middle row carries the tagged particle."""
            if transverse:      # same frequency as the other panel, so slower and shorter
                lam, spd, amp, pw = 3.0 * ratio, 2.0 * ratio, 0.22, 1.7 * ratio
            else:
                lam, spd, amp, pw = 3.0, 2.0, 0.25, 1.7
            back = 6.6 / spd + 0.3                  # pre-roll: the wave already fills the row
            launches = [-back + 1.5 * k for k in range(int((back + 30) / 1.5) + 1)]
            rows = []
            for y in (2.3, 1.6, 0.9):
                tagged = abs(y - 1.6) < 1e-6
                rows.append(ParticleChain(
                    n=15, spacing=0.4, amp=amp, wavelength=lam, pulse_width=pw, speed=spd,
                    tag=7 if tagged else -1, y=y, radius=0.07, tag_radius=0.15,
                    x0=x_c, x_start=x_c - 3.6, launches=launches, transverse=transverse,
                    guide_dir=UP if transverse else RIGHT, guide_len=0.32 if transverse else 0.4))
            return rows

        rows_l, rows_t = lattice(xc_l, False), lattice(xc_t, True)
        tag_l, tag_t = rows_l[1], rows_t[1]
        for r in rows_l + rows_t:
            r.add_updater(lambda m, dt: m.advance(dt))

        def panel_head(x_c, title, sub):
            t = label(title, FS_NOTE, INK, weight=BOLD).move_to([x_c, 3.4, 0])
            u = fit(label(sub, FS_TAG, GREY_INK), PW - 0.5).move_to([x_c, 3.0, 0])
            return VGroup(t, u)

        def prop_arrow(x_c):
            a = Arrow([x_c - 2.7, 0.4, 0], [x_c - 1.2, 0.4, 0], buff=0, color=INK, stroke_width=5,
                      tip_length=0.22)
            t = label("propagation", FS_TAG, INK).next_to(a, RIGHT, 0.2)
            return VGroup(a, t)

        head_l = panel_head(xc_l, "Longitudinal wave", "blue particle moves along the travel direction")
        head_t = panel_head(xc_t, "Transverse (shear) wave", "blue particle moves across the travel direction")
        prop_l, prop_t = prop_arrow(xc_l), prop_arrow(xc_t)

        self.sync(S + 0.1)
        self.play(FadeIn(frames), *[FadeIn(r) for r in rows_l + rows_t], run_time=0.6)
        for r in rows_l + rows_t:            # the pulses run from here on (updaters set after FadeIn)
            r.update()
        self.sync(c("الطُّولِيَّةِ"))
        self.play(FadeIn(head_l), run_time=0.4)
        self.sync(c("الجُسَيْمَاتُ"))
        self.play(FadeIn(tag_l.ring), Create(tag_l.guide), run_time=0.4)
        self.sync(c("الِانْتِشَارِ"))
        self.play(GrowArrow(prop_l[0]), FadeIn(prop_l[1]), run_time=0.5)

        # the solid / liquid / gas table, longitudinal row first
        col_w = [3.3, 2.1, 2.1, 2.1]
        tx0, ty0, row_h = -4.8, -0.3, 0.75
        xs_edge = [tx0 + sum(col_w[:i]) for i in range(5)]
        cx = [(xs_edge[i] + xs_edge[i + 1]) / 2 for i in range(4)]
        cy = [ty0 - row_h * (i + 0.5) for i in range(3)]
        tbl_frame = Rectangle(width=sum(col_w), height=3 * row_h, color=INK, stroke_width=3)
        tbl_frame.set_fill(PANEL_FILL, 1).move_to([tx0 + sum(col_w) / 2, ty0 - 1.5 * row_h, 0])
        rules = VGroup(*[Line([tx0, ty0 - row_h * k, 0], [tx0 + sum(col_w), ty0 - row_h * k, 0],
                              color=GREY_INK, stroke_width=2) for k in (1, 2)],
                       *[Line([xs_edge[k], ty0, 0], [xs_edge[k], ty0 - 3 * row_h, 0],
                              color=GREY_INK, stroke_width=2) for k in (1, 2, 3)])
        solid_mark = Square(0.34, color=INK, stroke_width=3).set_fill(INK, 0.25)
        heads = []
        for k, (name, mark) in enumerate([("Solid", solid_mark), ("Liquid", icon("droplet", ACCENT_1, 0.45)),
                                          ("Gas", icon("wind", GREY_INK, 0.45))]):
            h = VGroup(mark, label(name, FS_NOTE, INK, weight=BOLD)).arrange(RIGHT, buff=0.15)
            heads.append(h.move_to([cx[k + 1], cy[0], 0]))
        row_l = label("Longitudinal", FS_NOTE, INK).move_to([cx[0], cy[1], 0])
        row_t = label("Transverse", FS_NOTE, INK).move_to([cx[0], cy[2], 0])
        row_l.align_to([xs_edge[0] + 0.25, 0, 0], LEFT)
        row_t.align_to([xs_edge[0] + 0.25, 0, 0], LEFT)
        yes = lambda k, r: icon("check", ACCENT_3, 0.5).move_to([cx[k + 1], cy[r], 0])
        no = lambda k, r: icon("x", ACCENT_4, 0.5).move_to([cx[k + 1], cy[r], 0])

        self.sync(c("وَتَنْتَقِلُ"))
        self.play(FadeIn(tbl_frame), FadeIn(rules), *[FadeIn(h) for h in heads], FadeIn(row_l),
                  run_time=0.5)
        for k, w in enumerate(("الصُّلْبِ", "وَالسَّائِلِ", "وَالغَازِ")):
            self.sync(c(w))
            self.play(GrowFromCenter(yes(k, 1), run_time=0.3))
        fast = label("fastest", FS_TAG, ACCENT_1, weight=BOLD)
        fast.next_to(tbl_frame, RIGHT, 0.15).match_y(row_l)
        self.sync(c("الأَسْرَعُ"))
        self.play(FadeIn(fast, shift=LEFT * 0.15), run_time=0.4)

        self.sync(c("المُسْتَعْرِضَةِ"))
        self.play(FadeIn(head_t), FadeIn(row_t), run_time=0.4)
        self.sync(c("تَهْتَزُّ", 2))
        self.play(FadeIn(tag_t.ring), Create(tag_t.guide), run_time=0.4)
        self.sync(c("الِاتِّجَاهِ"))
        self.play(GrowArrow(prop_t[0]), FadeIn(prop_t[1]), run_time=0.5)
        self.sync(c("فَلَا"))
        qs = [label("?", FS_NOTE, GREY_INK, weight=BOLD).move_to([cx[k + 1], cy[2], 0]) for k in range(3)]
        self.play(*[FadeIn(q) for q in qs], run_time=0.3)

        def flip(q, mark):
            self.play(q.animate(run_time=0.12).stretch(0.02, 0))
            self.remove(q)
            self.play(GrowFromCenter(mark, run_time=0.25))
            return mark
        self.sync(c("الصُّلْبَةِ"))
        flip(qs[0], yes(0, 2))
        self.sync(c("السَّوَائِلَ"))
        x_liq = flip(qs[1], no(1, 2))
        self.sync(c("وَالغَازَاتِ"))
        x_gas = flip(qs[2], no(2, 2))
        shear_note = label("liquids and gases do not resist shear", FS_LABEL, ACCENT_4, weight=BOLD)
        shear_note.next_to(tbl_frame, DOWN, 0.3)
        self.sync(c("تُقَاوِمُ"))
        self.play(FadeIn(shear_note, shift=UP * 0.1), run_time=0.4)
        self.sync(c("القَصَّ"))
        self.play(Indicate(x_liq, color=ACCENT_4, scale_factor=1.3),
                  Indicate(x_gas, color=ACCENT_4, scale_factor=1.3), run_time=0.6)

        # ---- B, 20.9-29.4 s: the speeds in steel: shear is about 55 % of longitudinal ----
        self.sync(self.cue(3, "سُرْعَتُهَا") - 0.55)
        for r in rows_l + rows_t:
            r.clear_updaters()
        self.clear(run_time=0.5)
        self.sync(c("سُرْعَتُهَا"))
        bx0, s_px = -6.2, 8.6 / D.V_L_STEEL
        v_l, v_s = ValueTracker(0), ValueTracker(0)
        bar_l_y, bar_s_y, bar_h = 1.5, -0.6, 0.7

        def make_bar(v, y, fill):
            return always_redraw(lambda: Rectangle(
                width=max(0.01, s_px * v.get_value()), height=bar_h, color=ACCENT_1, stroke_width=3
            ).set_fill(ACCENT_1, fill).move_to([bx0, y, 0], aligned_edge=LEFT))

        def make_val(v, y):
            return always_redraw(lambda: label(f"{v.get_value():.0f} m/s", FS_NOTE, INK, weight=BOLD)
                                 .move_to([bx0 + max(0.01, s_px * v.get_value()) + 0.2, y, 0],
                                          aligned_edge=LEFT))
        head_b = label("Wave speed in steel", FS_BODY, INK, weight=BOLD).move_to([0, 3.2, 0])
        lab_s = label("Transverse (shear)", FS_NOTE, INK).move_to([bx0 + 0.2, bar_s_y + 0.65, 0], aligned_edge=LEFT)
        lab_l = label("Longitudinal", FS_NOTE, INK).move_to([bx0 + 0.2, bar_l_y + 0.65, 0], aligned_edge=LEFT)
        axis_b = Line([bx0, bar_l_y + 0.4, 0], [bx0, bar_s_y - 0.4, 0], color=INK, stroke_width=4)
        bar_s, val_s = make_bar(v_s, bar_s_y, 0.3), make_val(v_s, bar_s_y)
        bar_l, val_l = make_bar(v_l, bar_l_y, 0.55), make_val(v_l, bar_l_y)
        self.play(FadeIn(head_b), FadeIn(lab_s), Create(axis_b), run_time=0.5)
        self.add(bar_s, val_s)
        self.sync(c("ثَلَاثَةُ"))
        self.play(v_s.animate(rate_func=linear).set_value(D.V_S_STEEL),
                  run_time=c("مِتْرًا") + 0.3 - self.renderer.time)
        self.sync(c("أَيْ") - 0.05)
        self.add(bar_l, val_l)
        self.play(FadeIn(lab_l, run_time=0.2), v_l.animate(rate_func=smooth).set_value(D.V_L_STEEL),
                  run_time=0.5)
        x_end = bx0 + s_px * D.V_S_STEEL
        ratio_line = DashedLine([x_end, bar_s_y + bar_h / 2, 0], [x_end, bar_l_y + bar_h / 2, 0],
                                color=INK, stroke_width=3)
        ratio_tag = label(f"× {ratio:.2f}", FS_LABEL, ACCENT_1, weight=BOLD)
        ratio_tag.next_to(ratio_line, RIGHT, 0.15).match_y(ratio_line)
        self.sync(c("خَمْسَةٍ"))
        self.play(Create(ratio_line), FadeIn(ratio_tag), run_time=0.45)
        calc = label(f"{D.V_S_STEEL:.0f} ÷ {D.V_L_STEEL:.0f} = {ratio:.2f}", FS_LABEL + 2, INK, weight=BOLD)
        calc.move_to([0, -2.0, 0])
        self.sync(c("وَخَمْسِينَ"))
        self.play(FadeIn(calc), run_time=0.4)
        pct = label(f"≈ {ratio * 100:.0f} % of the longitudinal speed", FS_LABEL, ACCENT_1)
        pct.next_to(calc, DOWN, 0.25)
        self.sync(c("بِالمِئَةِ"))
        self.play(FadeIn(pct), run_time=0.4)
        self.sync(c("وَالسَّطْحِيَّةُ") - 0.5)
        for m in (bar_s, val_s, bar_l, val_l):
            m.clear_updaters()
        self.clear(run_time=0.4)

        # ---- C, 29.8-36 s: surface wave: a layer one wavelength deep, elliptical paths ----
        self.sync(c("وَالسَّطْحِيَّةُ"))
        sx, s_top, s_h, s_w = -4.0, 2.8, 3.6, 4.9
        s_lam = 3.0
        s_block = Rectangle(width=s_w, height=s_h, color=INK, stroke_width=4).set_fill(PANEL_FILL, 1)
        s_block.move_to([sx, s_top - s_h / 2, 0])
        surf = WaveField("surface", sx, s_top, cols=8, dx=0.6, depths=(0.5, 1.1, 1.7, 2.3),
                         wavelength=s_lam, amp=0.3, speed=1.2)
        surf_t = label("Surface wave", FS_NOTE, INK, weight=BOLD).next_to(s_block, UP, 0.3)
        self.play(FadeIn(s_block), FadeIn(surf), FadeIn(surf_t), run_time=0.5)
        surf.add_updater(lambda m, dt: m.advance(dt))
        surf_cap = label("elliptical particle paths", FS_TAG, GREY_INK).next_to(s_block, DOWN, 0.2)
        self.sync(c("تَسِيرُ"))
        self.play(FadeIn(surf.path), FadeIn(surf_cap), run_time=0.4)
        d_line = DashedLine([sx - s_w / 2, s_top - s_lam, 0], [sx + s_w / 2, s_top - s_lam, 0],
                            color=INK, stroke_width=3)
        d_br = DoubleArrow([sx + s_w / 2 + 0.3, s_top, 0], [sx + s_w / 2 + 0.3, s_top - s_lam, 0],
                           buff=0, color=INK, stroke_width=3, tip_length=0.15)
        d_lab = label("≈ 1 λ", FS_NOTE, INK).next_to(d_br, RIGHT, 0.1)
        self.sync(c("بِعُمْقِ"))
        self.play(Create(d_line), GrowFromCenter(d_br), run_time=0.5)
        self.sync(c("وَاحِدٍ"))
        self.play(FadeIn(d_lab), run_time=0.3)

        # ---- D, 35.2-45 s: Lamb wave: a thin plate, thickness at most 3 wavelengths ----
        self.sync(c("وَمَوْجَاتُ"))
        lx, l_top, l_h, l_w = 2.85, 2.8, 1.8, 4.6
        l_plate = Rectangle(width=l_w, height=l_h, color=INK, stroke_width=4).set_fill(PANEL_FILL, 1)
        l_plate.move_to([lx, l_top - l_h / 2, 0])
        lamb = WaveField("lamb", lx, l_top, cols=8, dx=0.55, depths=(0.25, 0.7, 1.15, 1.55),
                         wavelength=2.2, amp=0.2, speed=1.1, plate_h=l_h, tag_col=3)
        lamb_t = label("Lamb wave", FS_NOTE, INK, weight=BOLD).next_to(l_plate, UP, 0.3)
        lamb_t.match_y(surf_t)
        self.play(FadeIn(l_plate), FadeIn(lamb), FadeIn(lamb_t), FadeIn(lamb.path), run_time=0.5)
        lamb.add_updater(lambda m, dt: m.advance(dt))
        lamb_cap = label("thin plate", FS_TAG, GREY_INK).next_to(l_plate, DOWN, 0.2)
        self.sync(c("الصَّفَائِحِ"))
        self.play(FadeIn(lamb_cap), run_time=0.3)
        t_br = DoubleArrow([lx + l_w / 2 + 0.3, l_top, 0], [lx + l_w / 2 + 0.3, l_top - l_h, 0],
                           buff=0, color=INK, stroke_width=3, tip_length=0.15)
        t_lab = label("≤ 3 λ", FS_NOTE, INK).next_to(t_br, RIGHT, 0.1)
        self.sync(c("سَمَاكَتُهَا"))
        self.play(GrowFromCenter(t_br), run_time=0.4)
        self.sync(c("ثَلَاثَةِ"))
        self.play(FadeIn(t_lab), run_time=0.3)
        self.sync(c("وَنُفَصِّلُهُمَا"))
        pills = VGroup()
        for tgt in (s_block, l_plate):
            txt = label("Next episodes", FS_NOTE, ACCENT_1, weight=BOLD)
            pill = RoundedRectangle(width=txt.width + 0.5, height=0.6, corner_radius=0.3,
                                    color=ACCENT_1, stroke_width=3).set_fill(PANEL_FILL, 1)
            pills.add(VGroup(pill, txt))
        pills[0].move_to([sx, -2.2, 0])
        pills[1].move_to([lx, -2.2, 0])
        self.play(*[FadeIn(p_, shift=UP * 0.15) for p_ in pills], run_time=0.5)
        self.sync(self.end(3))
        surf.clear_updaters()
        lamb.clear_updaters()
        self.clear()

    # ---------------- Segment 4: impedance and reflection (§4) ----------------
    def seg4(self):
        c = lambda phrase, nth=1: self.cue(4, phrase, nth)

        # ---- A, 0-4 s: acoustic impedance Z = density x velocity ----
        self.sync(c("المُعَاوَقَةُ"))
        eq = equation(self, ["Z", "=", "ρ", "×", "v"], colors={0: ACCENT_1},
                      size=FS_EQUATION + 16, pos=[0, 0.7, 0], run_time=0.5, buff=0.55)
        caps = VGroup(*[label(t, FS_LABEL, GREY_INK).next_to(eq[k], DOWN, 0.25)
                        for k, t in ((0, "acoustic\nimpedance"), (2, "density"), (4, "speed"))])
        self.sync(c("الصَّوْتِيَّةُ"))
        self.play(FadeIn(caps[0]), run_time=0.3)
        self.sync(c("الكَثَافَةُ"))
        self.play(FadeIn(caps[1]), run_time=0.3)
        self.sync(c("السُّرْعَةِ"))
        self.play(FadeIn(caps[2]), run_time=0.3)
        self.sync(c("وَعِنْدَ") - 0.35)
        self.play(FadeOut(eq), FadeOut(caps), run_time=0.35)

        # ---- B, 4.2-7.6 s: a wave hits the interface between two media at 90 degrees ----
        BLK_W, BLK_H, BLK_Y = 5.5, 2.4, 0.8
        Y_INC, Y_REF, Y_TRN, X_ARR, T0 = 1.25, 0.5, 0.85, 3.0, 0.4
        steel_blk = Rectangle(width=BLK_W, height=BLK_H, color=INK, stroke_width=4)
        steel_blk.set_fill(PANEL_FILL, 1).move_to([-BLK_W / 2, BLK_Y, 0])
        water_blk = Rectangle(width=BLK_W, height=BLK_H, color=INK, stroke_width=4)
        water_blk.set_fill(PANEL_FILL, 0.45).move_to([BLK_W / 2, BLK_Y, 0])
        generic = VGroup(label("Medium 1  (Z₁)", FS_NOTE, GREY_INK).next_to(steel_blk, DOWN, 0.2),
                         label("Medium 2  (Z₂)", FS_NOTE, GREY_INK).next_to(water_blk, DOWN, 0.2))
        inc = energy_arrow([-X_ARR, Y_INC, 0], [-0.05, Y_INC, 0], T0, ACCENT_1)
        inc_lab = label("Incident", FS_TAG, ACCENT_1, weight=BOLD).next_to(inc, LEFT, 0.12)
        normal_lab = label("normal incidence (90°)", FS_TAG, GREY_INK)
        normal_lab.move_to(water_blk.get_corner(UL) + DR * 0.22, aligned_edge=UL)
        iface_lab = label("Interface", FS_TAG, GREY_INK).move_to([0, steel_blk.get_bottom()[1] - 0.3, 0])
        iface_arr = Arrow(iface_lab.get_top() + UP * 0.03, [0, steel_blk.get_bottom()[1], 0], buff=0,
                          color=GREY_INK, stroke_width=3, tip_length=0.15)
        self.sync(c("وَعِنْدَ"))
        self.play(Create(steel_blk), Create(water_blk), FadeIn(generic), run_time=0.75)
        self.sync(c("المَوْجَةِ"))
        self.play(GrowFromPoint(inc, [-X_ARR, Y_INC, 0]), FadeIn(inc_lab), run_time=0.5)
        self.sync(c("عَمُودِيًّا"))
        self.play(FadeIn(normal_lab), run_time=0.3)
        self.sync(c("سَطْحٍ"))
        self.play(FadeIn(iface_lab), GrowArrow(iface_arr),
                  Flash([0, Y_INC, 0], color=ACCENT_1, flash_radius=0.4, line_length=0.15,
                        run_time=0.5), run_time=0.5)

        # ---- C, 7.8-14.5 s: the reflection formula, with its brackets, and T = 1 - R ----
        fm = ReflectionFormula(size=FS_EQUATION + 6)
        fm.scale_to_fit_height(1.15)
        fit(fm, 12.4).move_to([0, 3.12, 0])
        self.sync(c("تَنْعَكِسُ"))
        self.play(FadeIn(fm.r_lhs), FadeOut(normal_lab), run_time=0.4)
        self.sync(c("مُرَبَّعُ"))
        self.play(FadeIn(fm.parens), run_time=0.4)
        self.sync(c("فَرْقِ"))
        self.play(FadeIn(fm.num, shift=DOWN * 0.1), run_time=0.4)
        self.sync(c("عَلَى", 2))
        self.play(Create(fm.bar), run_time=0.25)
        self.sync(c("مَجْمُوعِهِمَا"))
        self.play(FadeIn(fm.den, shift=UP * 0.1), run_time=0.4)
        self.sync(c("وَيَنْفُذُ"))
        self.play(FadeIn(fm.t_line), run_time=0.5)

        # ---- D, 15.4-27.5 s: steel against water: 88.0 % reflected, 12.0 % transmitted ----
        steel_tag = medium_tag("Steel", f"{D.RHO_STEEL:.0f} kg/m³ × {D.V_L_STEEL:.0f} m/s",
                               f"Z₁ = {D.Z_STEEL:.2f} MRayl").next_to(steel_blk, DOWN, 0.2)
        water_tag = medium_tag("Water", f"{D.RHO_WATER:.0f} kg/m³ × {D.V_WATER:.0f} m/s",
                               f"Z₂ = {D.Z_WATER:.2f} MRayl").next_to(water_blk, DOWN, 0.2)
        self.sync(c("الفُولَاذِ"))
        self.play(FadeOut(generic[0]), FadeIn(steel_tag.name_), run_time=0.3)
        self.sync(c("المُعَاوَقَةُ", 2))
        self.play(FadeIn(steel_tag.calc_), run_time=0.35)
        self.sync(c("سِتَّةٌ"))
        self.play(FadeIn(steel_tag.result_, shift=UP * 0.1), run_time=0.4)
        self.sync(c("المَاءِ"))
        self.play(FadeOut(generic[1]), FadeIn(water_tag.name_), run_time=0.3)
        self.sync(c("وَاحِدٌ"))
        self.play(FadeIn(water_tag.calc_), run_time=0.3)
        self.play(FadeIn(water_tag.result_, shift=UP * 0.1), run_time=0.4)

        def split(r):
            """Reflected and transmitted arrows (+ labels) for the reflected share r."""
            ref = energy_arrow([-0.05, Y_REF, 0], [-X_ARR, Y_REF, 0], T0 * r, ACCENT_2)
            trn = energy_arrow([0.05, Y_TRN, 0], [X_ARR, Y_TRN, 0], T0 * (1 - r), ACCENT_3)
            ref_l = label("Reflected", FS_TAG, ACCENT_2, weight=BOLD).next_to(ref, LEFT, 0.12)
            trn_l = label("Transmitted", FS_TAG, ACCENT_3, weight=BOLD).next_to(trn, RIGHT, 0.12)
            return ref, trn, ref_l, trn_l

        def split_in(ref, trn, ref_l, trn_l, bar):
            self.play(Flash([0, Y_INC, 0], color=ACCENT_1, flash_radius=0.4, line_length=0.15,
                            run_time=0.4),
                      GrowFromPoint(ref, [-0.05, Y_REF, 0]), GrowFromPoint(trn, [0.05, Y_TRN, 0]),
                      FadeIn(ref_l), FadeIn(trn_l), FadeIn(bar), run_time=0.7)

        def bar_labels(bar, r_txt, t_txt):
            lr = label(r_txt, FS_LABEL, ACCENT_2, weight=BOLD).next_to(bar.frame, DOWN, 0.2)
            lr.align_to(bar.frame, LEFT)
            lt = label(t_txt, FS_LABEL, ACCENT_3, weight=BOLD).next_to(bar.frame, DOWN, 0.2)
            lt.align_to(bar.frame, RIGHT)
            return lr, lt

        bar_w = EnergyBar(D.R_STEEL_WATER)
        bar_w.move_to([0, -2.2, 0])
        for part in (bar_w.refl, bar_w.trans):
            part.align_to(bar_w.frame, LEFT if part is bar_w.refl else RIGHT).match_y(bar_w.frame)
        lr_w, lt_w = bar_labels(bar_w, f"Reflected  {D.R_STEEL_WATER * 100:.1f} %",
                                f"Transmitted  {D.T_STEEL_WATER * 100:.1f} %")
        ref_w, trn_w, ref_wl, trn_wl = split(D.R_STEEL_WATER)
        self.sync(c("فَيَنْعَكِسُ"))
        split_in(ref_w, trn_w, ref_wl, trn_wl, bar_w)
        self.sync(c("ثَمَانِيَةٌ", 2))
        self.play(GrowFromEdge(bar_w.refl, LEFT), run_time=0.65)
        self.sync(c("وَثَمَانُونَ"))
        self.play(FadeIn(lr_w), run_time=0.3)
        self.sync(c("بِالمِئَةِ"))
        self.play(GrowFromEdge(bar_w.trans, RIGHT), run_time=0.5)
        self.sync(c("الطَّاقَةِ"))
        self.play(FadeIn(lt_w), run_time=0.3)

        # ---- E, 27.9-37.5 s: steel against air: 99.996 % reflected ----
        air_tag = medium_tag("Air", f"{D.RHO_AIR:g} kg/m³ × {D.V_AIR:.0f} m/s",
                             f"Z₂ = {D.Z_AIR:.0f} Rayl").next_to(water_blk, DOWN, 0.2)
        bar_a = EnergyBar(D.R_STEEL_AIR)
        bar_a.move_to([0, -2.2, 0])
        bar_a.refl.align_to(bar_a.frame, LEFT).match_y(bar_a.frame)
        bar_a.trans.align_to(bar_a.frame, RIGHT).match_y(bar_a.frame)
        lr_a, lt_a = bar_labels(bar_a, f"Reflected  {D.R_STEEL_AIR * 100:.3f} %",
                                f"Transmitted  {D.T_STEEL_AIR * 100:.3f} %")
        ref_a, trn_a, ref_al, trn_al = split(D.R_STEEL_AIR)
        self.sync(c("أَمَّا"))
        self.play(*[FadeOut(m) for m in (ref_w, trn_w, ref_wl, trn_wl, bar_w, bar_w.refl,
                                         bar_w.trans, lr_w, lt_w, water_tag)], run_time=0.22)
        self.sync(c("الهَوَاءُ"))
        self.play(water_blk.animate.set_fill(PANEL_FILL, 0.0), FadeIn(air_tag.name_), run_time=0.4)
        self.sync(c("فَمُعَاوَقَتُهُ"))
        self.play(FadeIn(air_tag.calc_), run_time=0.3)
        self.sync(c("أَرْبَعُ"))
        self.play(FadeIn(air_tag.result_, shift=UP * 0.1), run_time=0.4)
        self.sync(c("فَيَنْعَكِسُ", 2))
        split_in(ref_a, trn_a, ref_al, trn_al, bar_a)
        self.sync(c("تِسْعَةٌ"))
        self.play(GrowFromEdge(bar_a.refl, LEFT), run_time=2.6, rate_func=linear)
        self.play(FadeIn(lr_a), run_time=0.3)
        self.sync(c("بِالمِئَةِ", 2))
        self.play(FadeIn(bar_a.trans), FadeIn(lt_a), run_time=0.4)

        # ---- F, 38-54 s: three consequences: air gap and couplant, air-filled flaw, back wall ----
        self.sync(c("وَلِهٰذَا") - 0.4)
        self.clear(run_time=0.4)
        head = label("Three consequences", FS_BODY, INK, weight=BOLD).move_to([0, 3.35, 0])
        self.sync(c("ثَلَاثُ"))
        self.play(FadeIn(head), run_time=0.4)
        t_top, g = 0.3, 0.9
        part = SteelBlock(7.6, 2.9).move_to([-2.2, t_top - 1.45, 0])
        wall_line = Line(part.body.get_corner(DL), part.body.get_corner(DR), color=INK, stroke_width=8)
        wall_tag = label("Back wall", FS_TAG, GREY_INK).next_to(wall_line, DOWN, 0.15)
        wall_tag.align_to(wall_line, LEFT).shift(RIGHT * 0.3)
        steel_name = label("Steel part", FS_TAG, GREY_INK).move_to(
            part.body.get_corner(DL) + UR * 0.2, aligned_edge=DL)
        rig = CouplantRig(-4.0, t_top, gap=g)
        px0 = rig.x()
        gap_dim = DoubleArrow([px0 + 0.65, t_top, 0], [px0 + 0.65, t_top + g, 0], buff=0,
                              color=GREY_INK, stroke_width=3, tip_length=0.12)
        gap_lab = label("Air gap", FS_TAG, GREY_INK).next_to(gap_dim, RIGHT, 0.12)
        chips = VGroup(
            chip("Air gap blocks the sound; couplant drives it out", "wind", ACCENT_2, 4.6),
            chip("Air-filled flaws reflect strongly, so they show", "search", ACCENT_4, 4.6),
            chip("The back wall gives a strong echo", "arrows-exchange", ACCENT_2, 4.6),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([4.5, 0.4, 0])

        self.play(Create(part), FadeIn(rig), run_time=0.6)
        self.play(FadeIn(wall_line), FadeIn(steel_name), run_time=0.3)

        def hop(color, x, y0, y1, run, direction, amp=0.22, length=0.5, cycles=4, extra=()):
            """A pulse of `color` leaves y0 and travels to y1 along x (`extra` animations play
            together with its first appearance)."""
            p_ = wave_packet(length=length, amp=amp, cycles=cycles, color=color, direction=direction)
            p_.move_to([x, y0, 0])
            self.play(FadeIn(p_, run_time=0.1), *extra)
            self.play(p_.animate(run_time=run, rate_func=linear).move_to([x, y1, 0]))
            return p_

        # 1. the air gap: the pulse bounces back; couplant fills the gap and the pulse goes in
        self.sync(c("طَبَقَةُ"))
        self.play(FadeIn(chips[0], shift=LEFT * 0.2), FadeIn(gap_dim), FadeIn(gap_lab), run_time=0.45)
        face = rig.face_y()
        y_a, y_b = face - 0.3, t_top + 0.28            # in the gap: just under the face / on the surface
        for t_start in (c("الهَوَاءِ") - 0.05, c("وَالقِطْعَةِ") - 0.1):
            self.sync(t_start)
            down = hop(ACCENT_1, px0, y_a, y_b, 0.35, DOWN)
            up = wave_packet(length=0.5, amp=0.22, cycles=4, color=ACCENT_2, direction=UP)
            up.move_to([px0, y_b, 0])
            self.play(FadeOut(down, run_time=0.1), FadeIn(up, run_time=0.1),
                      Flash([px0, t_top, 0], color=ACCENT_2, flash_radius=0.3, line_length=0.1,
                            run_time=0.25))
            self.play(up.animate(run_time=0.35, rate_func=linear).move_to([px0, y_a, 0]))
            self.play(FadeOut(up, run_time=0.1))
        blocked = icon("x", ACCENT_4, 0.5).move_to([px0, t_top - 0.55, 0])
        self.sync(c("الصَّوْتَ"))
        self.play(GrowFromCenter(blocked), run_time=0.3)
        self.sync(c("فَنَضَعُ"))
        drop = icon("droplet", ACCENT_3, 0.55).move_to([px0 - 1.4, t_top + g / 2, 0])
        self.play(FadeIn(drop, shift=DOWN * 0.2), run_time=0.4)
        self.sync(c("وَسِيطًا"))
        coup_lab = label("Couplant", FS_TAG, ACCENT_3, weight=BOLD)
        film = rig.gap_fill()
        coup_lab.move_to(gap_lab.get_center(), aligned_edge=LEFT).align_to(gap_lab, LEFT)
        self.play(drop.animate(run_time=0.5).move_to([px0 - 0.15, t_top + g / 2, 0]),
                  FadeOut(gap_lab, run_time=0.3), FadeIn(coup_lab, run_time=0.4))
        self.sync(c("يَطْرُدُهَا"))
        self.play(FadeOut(drop, run_time=0.2), FadeOut(gap_dim, run_time=0.3),
                  GrowFromCenter(film), FadeOut(blocked, run_time=0.3), run_time=0.4)
        rig.add(film, coup_lab)
        go = wave_packet(length=0.6, amp=0.24, cycles=5, color=ACCENT_3, direction=DOWN)
        go.move_to([px0, face - 0.35, 0])
        self.play(FadeIn(go, run_time=0.1))
        self.play(go.animate(run_time=0.7, rate_func=linear).move_to([px0, t_top - 0.9, 0])
                  .set_stroke(opacity=0.35))
        self.play(FadeOut(go, run_time=0.2))

        # 2. an air-filled flaw reflects
        crack = Ellipse(width=1.0, height=0.16, color=ACCENT_4, stroke_width=4)
        crack.set_fill(ACCENT_4, 0.6)
        px1 = -2.0
        crack.move_to([px1, t_top - 1.0, 0])
        crack_tag = label("Air-filled crack", FS_TAG, ACCENT_4, weight=BOLD).next_to(crack, DOWN, 0.2)
        self.sync(c("وَالعُيُوبُ"))
        self.play(rig.animate(run_time=0.6).shift(RIGHT * (px1 - px0)),
                  FadeIn(chips[1], shift=LEFT * 0.2), FadeIn(crack, scale=0.5), run_time=0.6)
        self.sync(c("المَمْلُوءَةُ"))
        self.play(FadeIn(crack_tag), run_time=0.2)
        self.sync(c("بِالهَوَاءِ") - 0.5)
        y0, y1 = face - 0.35, crack.get_top()[1] + 0.35
        go2 = hop(ACCENT_1, px1, y0, y1, 0.65, DOWN, amp=0.26, length=0.7, cycles=6)
        back = wave_packet(length=0.7, amp=0.26, cycles=6, color=ACCENT_2, direction=UP)
        back.move_to([px1, y1, 0])
        self.sync(c("تَعْكِسُ"))
        self.play(FadeOut(go2, run_time=0.12), FadeIn(back, run_time=0.12),
                  Flash(crack, color=ACCENT_4, flash_radius=0.7, line_length=0.18, run_time=0.4))
        self.play(back.animate(run_time=0.8, rate_func=linear).move_to([px1, y0, 0]))
        self.sync(c("فَتَظْهَرُ"))
        self.play(FadeOut(back, run_time=0.15),
                  Flash(crack, color=ACCENT_4, flash_radius=0.7, line_length=0.18, run_time=0.5))

        # 3. the back wall gives a strong echo
        px2 = -0.5
        self.sync(c("وَالجِدَارُ") - 0.9)
        self.play(rig.animate(run_time=0.8).shift(RIGHT * (px2 - px1)), FadeOut(crack_tag, run_time=0.4))
        self.sync(c("وَالجِدَارُ"))
        wall_y = part.body.get_bottom()[1]
        go3 = hop(ACCENT_1, px2, face - 0.35, wall_y + 0.4, 1.0, DOWN, amp=0.3, length=0.7, cycles=6,
                  extra=(FadeIn(chips[2], shift=LEFT * 0.2, run_time=0.1), FadeIn(wall_tag, run_time=0.1)))
        echo = wave_packet(length=0.9, amp=0.42, cycles=6, color=ACCENT_2, direction=UP,
                           stroke_width=5)
        echo.move_to([px2, wall_y + 0.45, 0])
        self.play(FadeOut(go3, run_time=0.12), FadeIn(echo, run_time=0.12),
                  Flash([px2, wall_y, 0], color=ACCENT_2, flash_radius=0.6, line_length=0.2,
                        run_time=0.4))
        self.play(echo.animate(run_time=1.3, rate_func=linear).move_to([px2, face - 0.35, 0]))
        self.sync(self.end(4))
        self.clear()

    # ---------------- Segment 5: pulse-echo and the A-scan (§5) ----------------
    def seg5(self):
        c = lambda phrase, nth=1: self.cue(5, phrase, nth)

        # ---- geometry and the one shared clock ----
        PLATE_W, PLATE_H, PLATE_CX, PLATE_TOP = 6.4, 1.9, -3.0, 2.35
        MM = PLATE_H / D.THICKNESS                    # screen units per mm of depth
        V = D.V_L_STEEL / 1000.0                      # mm per µs
        SLOWMO = 0.5                                  # screen seconds per µs of real time
        T_START, T_END = -0.5, 10.0                   # clock range (µs)
        t_fl, t_bw = D.T_FLAW_US, D.T_BACKWALL_US
        COL_X = 4.35                                  # centre of the right-hand column
        bx = PLATE_CX
        top_y, bot_y = PLATE_TOP, PLATE_TOP - PLATE_H
        yz = lambda z: top_y - z * MM                 # screen y of depth z (mm)

        plate = SteelBlock(PLATE_W, PLATE_H).move_to([PLATE_CX, PLATE_TOP - PLATE_H / 2, 0])
        probe = Probe().next_to(plate, UP, buff=0)
        flaw = Ellipse(width=0.5, height=0.16, color=ACCENT_4, stroke_width=4)
        flaw.set_fill(ACCENT_4, 0.5).move_to([bx, yz(D.FLAW_DEPTH), 0])
        wall = Line(plate.body.get_corner(DL), plate.body.get_corner(DR), color=INK, stroke_width=8)
        flaw_tag = label("Flaw", FS_TAG, ACCENT_4, weight=BOLD).next_to(flaw, RIGHT, 0.15)
        wall_tag = label("Back wall", FS_TAG, GREY_INK).move_to(
            plate.body.get_corner(DL) + UR * 0.28, aligned_edge=DL)
        steel_tag = label("Steel plate", FS_TAG, GREY_INK).move_to(
            plate.body.get_corner(DR) + UL * 0.28, aligned_edge=DR)

        asc = AScan([(0.0, 1.6), (t_fl, 0.5), (t_bw, 0.95)])
        asc.shift(np.array([PLATE_CX, -1.35, 0]) - asc.frame.get_center())   # the frame, not the group
        asc_tag = label("A-scan screen", FS_TAG, INK, weight=BOLD).next_to(asc.frame, UP, 0.12)
        asc_tag.align_to(asc.frame, LEFT)

        # ---- 0.3-5 s: the probe sends a short pulse, then listens ----
        chips = VGroup(chip("Send a short pulse", "bolt", ACCENT_1, 4.4),
                       chip("Listen for the echoes", "wifi", ACCENT_2, 4.4)
                       ).arrange(DOWN, buff=0.4).move_to([COL_X, 1.4, 0])
        self.sync(c("طَرِيقَةِ"))
        self.play(Create(plate), FadeIn(probe, shift=DOWN * 0.5), run_time=0.8)
        self.play(FadeIn(flaw), Create(wall), run_time=0.4)
        self.sync(c("نَبْضَةً"))
        demo = wave_packet(length=0.55, amp=0.3, cycles=5).move_to([bx, top_y - 0.4, 0])
        self.play(FadeIn(chips[0], shift=LEFT * 0.2, run_time=0.3), FadeIn(demo, run_time=0.15))
        self.play(demo.animate(run_time=0.75, rate_func=linear).move_to([bx, top_y - 1.2, 0])
                  .set_stroke(opacity=0))
        self.remove(demo)
        self.sync(c("يَسْتَمِعُ"))
        demo2 = wave_packet(length=0.55, amp=0.14, cycles=5, color=ACCENT_2, direction=UP)
        demo2.move_to([bx, top_y - 1.2, 0]).set_stroke(opacity=0)
        self.add(demo2)
        self.play(FadeIn(chips[1], shift=LEFT * 0.2),
                  demo2.animate(run_time=0.7, rate_func=linear).move_to([bx, top_y - 0.4, 0])
                  .set_stroke(opacity=1))
        self.play(FadeOut(demo2, run_time=0.2))

        # ---- 5.8-12.4 s: the A-scan screen, its two axes ----
        self.sync(c("شَاشَةِ"))
        self.play(FadeIn(asc.frame), FadeIn(asc_tag), run_time=0.5)
        self.sync(c("الأُفُقِيُّ"))
        self.play(Create(asc.x_axis), FadeIn(asc.ticks), run_time=0.5)
        self.sync(c("الزَّمَنُ"))
        self.play(FadeIn(asc.tick_labels), FadeIn(asc.x_caption), run_time=0.5)
        self.sync(c("وَالعَمُودِيُّ"))
        self.play(Create(asc.y_axis), run_time=0.5)
        self.sync(c("سَعَةُ"))
        self.play(FadeIn(asc.y_caption), run_time=0.4)

        # ---- 12.5-18.2 s: one clock drives the pulse in the plate and the cursor on the screen ----
        clock = ValueTracker(T_START)
        panel = RoundedRectangle(width=4.2, height=1.0, corner_radius=0.12, color=INK,
                                 stroke_width=3).set_fill(PANEL_FILL, 1).move_to([COL_X, 2.55, 0])
        clock_anchor = panel.get_left() + RIGHT * 0.5
        clock_txt = always_redraw(lambda: label(f"t = {max(clock.get_value(), 0):.2f} µs", 40, INK)
                                  .move_to(clock_anchor, aligned_edge=LEFT))
        slow = label(f"Slow motion: 1 µs = {SLOWMO:g} s", FS_TAG, GREY_INK)
        slow.next_to(panel, DOWN, 0.2)
        sw_pulse = wave_packet(length=0.8, amp=0.13, cycles=4, color=ACCENT_1, direction=RIGHT)
        sw_echo = wave_packet(length=0.8, amp=0.13, cycles=4, color=ACCENT_2, direction=LEFT)
        legend = VGroup(
            VGroup(sw_pulse, label("Pulse", FS_NOTE, INK)).arrange(RIGHT, buff=0.3),
            VGroup(sw_echo, label("Echo", FS_NOTE, INK)).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        legend.move_to([COL_X, 0.4, 0]).align_to(panel, LEFT).shift(RIGHT * 0.3)

        def driven(mob, z_fn, t0, t1, z_a, z_b):
            """Move `mob` along the beam by the clock: depth z_fn(t) while t0 <= t <= t1; it fades
            in over the first and out over the last 0.4 units of its path (z_a -> z_b, mm)."""
            mob.set_stroke(opacity=0)

            def upd(m):
                t = clock.get_value()
                if t < t0 or t > t1:
                    m.set_stroke(opacity=0)
                    return
                z = z_fn(t)
                m.move_to([bx, yz(z), 0])
                op = min(1.0, abs(z - z_a) * MM / 0.4, abs(z - z_b) * MM / 0.4)
                m.set_stroke(opacity=max(op, 0.0))
            mob.add_updater(upd)
            return mob

        def ring_at(point, t_hit, color):
            ring = Circle(radius=0.2, color=color, stroke_width=4).move_to(point)
            ring.set_stroke(opacity=0)

            def upd(m):
                dt = clock.get_value() - t_hit
                if 0 <= dt <= 0.8:
                    m.set_width(2 * (0.15 + 0.5 * dt / 0.8)).move_to(point)
                    m.set_stroke(opacity=1 - dt / 0.8)
                else:
                    m.set_stroke(opacity=0)
            ring.add_updater(upd)
            return ring

        h_fl = t_fl / 2                                  # the pulse reaches the flaw
        h_bw = t_bw / 2                                  # ... and the back wall
        inc = driven(wave_packet(length=0.55, amp=0.3, cycles=5), lambda t: V * t,
                     0.0, h_fl, 0.0, D.FLAW_DEPTH)
        thru = driven(wave_packet(length=0.55, amp=0.24, cycles=5),
                      lambda t: D.FLAW_DEPTH + V * (t - h_fl), h_fl, h_bw, D.FLAW_DEPTH, D.THICKNESS)
        echo_f = driven(wave_packet(length=0.55, amp=0.14, cycles=5, color=ACCENT_2, direction=UP),
                        lambda t: D.FLAW_DEPTH - V * (t - h_fl), h_fl, t_fl, D.FLAW_DEPTH, 0.0)
        echo_b = driven(wave_packet(length=0.55, amp=0.22, cycles=5, color=ACCENT_2, direction=UP),
                        lambda t: D.THICKNESS - V * (t - h_bw), h_bw, t_bw, D.THICKNESS, 0.0)
        ring_f = ring_at([bx, yz(D.FLAW_DEPTH), 0], h_fl, ACCENT_4)
        ring_w = ring_at([bx, bot_y, 0], h_bw, ACCENT_2)
        asc.trace.add_updater(lambda m: asc.update_trace(clock.get_value()))
        asc.cursor.add_updater(lambda m: asc.set_cursor(clock.get_value()))
        movers = [inc, thru, echo_f, echo_b, ring_f, ring_w, asc.trace, asc.cursor, asc.pen]

        dot_i, dot_f, dot_b = (Dot(asc.apex(k), radius=0.07, color=col)
                               for k, col in enumerate((ACCENT_1, ACCENT_2, ACCENT_2)))
        tag_i = label("Initial pulse", FS_TAG, ACCENT_1, weight=BOLD).next_to(dot_i, RIGHT, 0.15)
        tag_f = label("Flaw echo", FS_TAG, ACCENT_2, weight=BOLD).next_to(dot_f, UP, 0.12)
        tag_b = label("Back-wall echo", FS_TAG, ACCENT_2, weight=BOLD).next_to(dot_b, UP, 0.12)
        tag_b.shift(LEFT * (tag_b.get_right()[0] - (asc.frame.get_right()[0] - 0.2)))   # inside the frame

        def sweep(t_to, *extra):
            dt = (t_to - clock.get_value()) * SLOWMO
            self.play(clock.animate(run_time=dt, rate_func=linear).set_value(t_to), *extra)

        self.sync(c("تَظْهَرُ"))
        self.play(FadeOut(chips), FadeIn(panel), FadeIn(slow), run_time=0.4)
        self.add(clock_txt, *movers)
        self.sync(c("النَّبْضَةُ"))                      # clock = T_START: the pulse is sent
        sweep(0.5, FadeIn(legend[0], run_time=0.3))                     # the initial pulse rises on the screen
        self.sync(c("الِابْتِدَائِيَّةُ"))
        sweep(h_fl, FadeIn(tag_i, run_time=0.3), FadeIn(dot_i, run_time=0.3))         # the pulse runs down to the flaw
        sweep(t_fl, FadeIn(legend[1], run_time=0.3), FadeIn(flaw_tag, run_time=0.3))                    # part reflects, part goes on; echo returns
        sweep(6.3, FadeIn(tag_f, run_time=0.3), FadeIn(dot_f, run_time=0.3))          # the flaw echo is on the screen
        sweep(t_bw)                                       # the back-wall echo travels up
        sweep(T_END, FadeIn(tag_b, run_time=0.3), FadeIn(dot_b, run_time=0.3),
              FadeIn(wall_tag, run_time=0.3))
        for m in movers + [clock_txt]:
            m.clear_updaters()
        self.remove(inc, thru, echo_f, echo_b, ring_f, ring_w)

        # ---- 18.9-26 s: depth = speed x time / 2, and why it is halved ----
        self.sync(c("وَالعُمْقُ") - 0.5)
        self.play(FadeOut(panel), FadeOut(clock_txt), FadeOut(slow), FadeOut(legend),
                  FadeOut(asc.cursor), FadeOut(asc.pen), run_time=0.4)
        EQ_Y = 2.3
        mk = lambda s, col=INK: Text(s, font_size=48, color=col)
        eq_d, eq_is, eq_v = mk("d"), mk("="), mk("v", ACCENT_1)
        eq_x, eq_t, eq_h = mk("×"), mk("t", ACCENT_2), mk("÷ 2", ACCENT_2)
        eq = VGroup(eq_d, eq_is, eq_v, eq_x, eq_t, eq_h).arrange(RIGHT, buff=0.32)
        eq.move_to([COL_X, EQ_Y, 0])
        caps = {k: label(t, FS_TAG, GREY_INK).next_to(m, DOWN, 0.2)
                for k, m, t in (("d", eq_d, "depth"), ("v", eq_v, "speed"), ("t", eq_t, "time"))}
        self.sync(c("وَالعُمْقُ"))
        self.play(FadeIn(eq_d), FadeIn(eq_is), FadeIn(caps["d"]), run_time=0.4)
        self.sync(c("السُّرْعَةَ"))
        self.play(FadeIn(eq_v), FadeIn(caps["v"]), run_time=0.35)
        self.sync(c("ضَرْبَ"))
        self.play(FadeIn(eq_x), run_time=0.25)
        self.sync(c("الزَّمَنِ"))
        self.play(FadeIn(eq_t), FadeIn(caps["t"]), run_time=0.35)
        self.sync(c("عَلَى", 2))
        self.play(FadeIn(eq_h, shift=LEFT * 0.15), run_time=0.3)
        self.sync(c("اثْنَيْنِ"))
        two_box = emphasize(self, eq_h, color=ACCENT_2, run_time=0.5)
        self.sync(c("لِأَنَّ"))
        trip = label("round trip: there and back", FS_NOTE, ACCENT_2)
        trip.move_to([COL_X, EQ_Y - 1.55, 0])
        self.play(FadeIn(trip), run_time=0.4)
        a_dn = Arrow([bx - 0.85, top_y - 0.06, 0], [bx - 0.85, bot_y + 0.06, 0], buff=0,
                     color=ACCENT_1, stroke_width=4, tip_length=0.2)
        a_up = Arrow([bx - 1.3, bot_y + 0.06, 0], [bx - 1.3, top_y - 0.06, 0], buff=0,
                     color=ACCENT_2, stroke_width=4, tip_length=0.2)
        l_dn = label("there", FS_TAG, ACCENT_1, weight=BOLD).next_to(a_dn, RIGHT, 0.12).shift(UP * 0.45)
        l_up = label("back", FS_TAG, ACCENT_2, weight=BOLD).next_to(a_up, LEFT, 0.12).shift(UP * 0.45)
        self.sync(c("ذَهَابًا"))
        self.play(GrowArrow(a_dn), FadeIn(l_dn), run_time=0.45)
        self.sync(c("وَإِيَابًا"))
        self.play(GrowArrow(a_up), FadeIn(l_up), run_time=0.45)

        # ---- 26.9-36 s: the plate, 25 mm; the back-wall echo at 8.45 µs ----
        self.sync(c("لَوْحُ") - 0.1)
        self.play(FadeOut(a_dn), FadeOut(a_up), FadeOut(l_dn), FadeOut(l_up), run_time=0.3)
        dim25 = DoubleArrow([0.5, top_y, 0], [0.5, bot_y, 0], buff=0, color=GREY_INK,
                            stroke_width=3, tip_length=0.15)
        lab25 = label(f"{D.THICKNESS:.0f} mm", FS_TAG, INK, weight=BOLD).next_to(dim25, RIGHT, 0.12)
        self.sync(c("فُولَاذٍ"))
        self.play(FadeIn(steel_tag), run_time=0.3)
        self.sync(c("سَمَاكَتُهُ"))
        self.play(GrowFromCenter(dim25), FadeIn(lab25), run_time=0.45)
        t_bw_tag = label(f"{D.T_BACKWALL_US:.2f} µs", FS_TAG, INK, weight=BOLD).next_to(tag_b, UP, 0.08)
        self.sync(c("يَصِلُ"))
        self.play(Flash([bx, bot_y, 0], color=ACCENT_2, flash_radius=0.5,
                                          line_length=0.15, run_time=0.4))
        self.sync(c("خَمْسَةً"))
        self.play(FadeIn(t_bw_tag), run_time=0.3)

        # ---- 36-43.5 s: the flaw echo at 4.05 µs gives 12.0 mm ----
        self.sync(c("وَصَدَى") - 0.4)
        self.play(FadeOut(eq), FadeOut(VGroup(*caps.values())), FadeOut(two_box), FadeOut(trip),
                  run_time=0.35)
        t_fl_tag = label(f"{D.T_FLAW_US:.2f} µs", FS_TAG, INK, weight=BOLD).next_to(tag_f, UP, 0.08)
        self.sync(c("وَصَدَى"))
        self.play(Flash(flaw.get_center(), color=ACCENT_4, flash_radius=0.45, line_length=0.12,
                        run_time=0.4))
        T_TAG = c("خَمْسَةً", 2)                      # the "4.05 µs" tag appears while the calculation plays
        t_fl_tag.set_opacity(0)
        t_fl_tag.add_updater(lambda m: m.set_opacity(
            min(1.0, max(0.0, (self.renderer.time - T_TAG) / 0.3))))
        self.add(t_fl_tag)
        calc = worked_calculation(
            self, ["d", "=", "v", "×", "t", "÷ 2"],
            ["=", f"{D.V_L_STEEL:.0f} m/s", "×", f"{D.T_FLAW_US:.2f} µs", "÷ 2"],
            f"d = {D.FLAW_DEPTH_FROM_T:.1f} mm",
            cues=[c("عَيْبٍ"), c("خَمْسَةً", 2) + 0.2, c("اثْنَيْ")],
            pos=[COL_X, 0.9, 0], color=ACCENT_4, size=32)
        t_fl_tag.clear_updaters()
        t_fl_tag.set_opacity(1)
        dim12 = DoubleArrow([bx - 1.2, top_y, 0], [bx - 1.2, yz(D.FLAW_DEPTH), 0], buff=0,
                            color=ACCENT_4, stroke_width=3, tip_length=0.12)
        guide = DashedLine([bx - 1.2, yz(D.FLAW_DEPTH), 0], [flaw.get_left()[0] - 0.05, yz(D.FLAW_DEPTH), 0],
                           color=ACCENT_4, stroke_width=2)
        lab12 = label(f"{D.FLAW_DEPTH_FROM_T:.1f} mm", FS_TAG, ACCENT_4, weight=BOLD)
        lab12.next_to(dim12, LEFT, 0.12)
        self.play(GrowFromCenter(dim12), Create(guide), FadeIn(lab12), run_time=0.5)

        # ---- 43.9-57 s: calibration: the wrong velocity setting reads 26.7 mm ----
        self.sync(c("وَلِهٰذَا") - 0.3)
        self.play(FadeOut(calc), FadeOut(dim12), FadeOut(guide), FadeOut(lab12), FadeOut(t_fl_tag),
                  FadeOut(flaw_tag), run_time=0.4)
        gauge = ThicknessGauge(f"{D.THICKNESS:.1f} mm",
                               [("Steel", D.V_L_STEEL), ("Aluminium", D.V_L_ALUMINIUM)],
                               selected=0, echo_text=f"Echo time  {D.T_BACKWALL_US:.2f} µs", width=4.6)
        gauge.move_to([4.55, -0.05, 0])
        cable_top = probe.cable.get_top()
        wire = VMobject(color=GREY_INK, stroke_width=4)
        wire.set_points_as_corners([cable_top, [4.55, cable_top[1], 0], gauge.case.get_top()])
        self.sync(c("تَلْزَمُ"))
        self.play(FadeIn(gauge, shift=LEFT * 0.2), run_time=0.5)
        self.sync(c("الجِهَازُ"))
        self.play(Create(wire), run_time=0.6)
        self.sync(c("الأَلُمْنْيُومِ"))
        al_box = SurroundingRectangle(gauge.rows[1], color=ACCENT_2, buff=0.1, corner_radius=0.1,
                                      stroke_width=3)
        self.play(Create(al_box), run_time=0.4)
        self.sync(c("نَفْحَصُ"))
        steel_box = SurroundingRectangle(steel_tag, color=ACCENT_1, buff=0.1, corner_radius=0.1,
                                         stroke_width=3)
        self.play(FadeOut(al_box), Create(steel_box), run_time=0.4)
        self.sync(c("سَمَاكَةَ"))
        wrong = gauge.reading(f"{D.READING_AL:.1f} mm", ALERT_C)
        self.play(FadeOut(steel_box), gauge.marker.animate.move_to(gauge.marker_pos(1)),
                  Transform(gauge.value, wrong), run_time=0.6)
        true_tag = label(f"True thickness: {D.THICKNESS:.0f} mm", FS_NOTE, OK_C, weight=BOLD)
        true_tag.next_to(gauge.case, DOWN, 0.25)
        self.sync(c("بَدَلَ"))
        self.play(FadeIn(true_tag), run_time=0.4)
        self.play(Indicate(lab25, color=OK_C, scale_factor=1.2), run_time=0.6)
        self.sync(self.end(5))
        self.clear()

    # ---------------- Segment 6: the basic methods and the limits (§6) ----------------
    def seg6(self):
        c = lambda phrase, nth=1: self.cue(6, phrase, nth)

        CX = (-4.5, 0.0, 4.5)                  # column centres of the three panels
        Y_HEAD, Y_RULE, Y_TOP, Y_TAGS = 3.45, 3.12, 1.85, -2.0
        BLOCK_W = 3.4

        def fly(mob, p0, p1, run_time, *extra):
            """A pulse travels from p0 to p1 (and is removed on arrival)."""
            mob.move_to(p0)
            self.add(mob)
            self.play(mob.animate(run_time=run_time, rate_func=linear).move_to(p1), *extra)
            self.remove(mob)

        # ================= panel 1: through transmission =================
        x1 = CX[0]
        head1, rule1 = method_head("Through transmission", x1, Y_HEAD, Y_RULE, ACCENT_3)
        block1 = SteelBlock(BLOCK_W, 1.8).move_to([x1, Y_TOP - 0.9, 0])
        top1, bot1 = Y_TOP, Y_TOP - 1.8
        pa = Probe().next_to(block1, UP, buff=0)
        pb = Probe(color=ACCENT_3, flip=True).next_to(block1, DOWN, buff=0)
        sends = label("Sends", FS_TAG, ACCENT_1, weight=BOLD).next_to(pa.housing, RIGHT, 0.2)
        recvs = label("Receives", FS_TAG, ACCENT_3, weight=BOLD).next_to(pb.housing, RIGHT, 0.2)
        beam1 = Rectangle(width=0.77, height=1.8, color=ACCENT_3, stroke_width=0)
        beam1.set_fill(ACCENT_3, 0.25).move_to(block1)
        meter = Rectangle(width=1.9, height=0.28, color=INK, stroke_width=3)
        meter.move_to([x1, pb.get_bottom()[1] - 0.32, 0])
        meter_wire = Line(pb.cable.get_end(), meter.get_top(), color=GREY_INK, stroke_width=4)
        meter_lab = label("Received signal", FS_TAG, INK).next_to(meter, DOWN, 0.12)
        fill = signal_bar(meter, 0.02, ACCENT_3)
        flaw1 = Ellipse(width=0.55, height=0.3, color=ACCENT_4, stroke_width=4)
        flaw1.set_fill(ACCENT_4, 0.45).move_to([x1, top1 - 0.95, 0])
        fl_bot = flaw1.get_bottom()[1]
        shadow = Rectangle(width=0.55, height=fl_bot - bot1, color=GREY_INK, stroke_width=0)
        shadow.set_fill(GREY_INK, 0.35).move_to([x1, (fl_bot + bot1) / 2, 0])
        shadow_lab = label("Shadow", FS_TAG - 2, GREY_INK).next_to(shadow, RIGHT, 0.25)
        ghosts = VGroup(*[DashedVMobject(Ellipse(width=0.55, height=0.3, color=GREY_INK,
                                                 stroke_width=3).move_to([x1, y, 0]),
                                         num_dashes=18)
                          for y in (top1 - 0.4, bot1 + 0.4)])
        tag1a = tag_line("Needs both sides", "arrows-exchange", ALERT_C)
        tag1b = tag_line("Does not give the flaw location", "map-pin", ALERT_C)
        tag1a.move_to([x1, Y_TAGS, 0]).align_to([x1 - 1.9, 0, 0], LEFT).align_to([0, Y_TAGS, 0], UP)
        tag1b.next_to(tag1a, DOWN, 0.2, aligned_edge=LEFT)

        # ================= panel 2: pulse-echo =================
        x2 = CX[1]
        head2, rule2 = method_head("Pulse-echo", x2, Y_HEAD, Y_RULE, ACCENT_1)
        block2 = SteelBlock(BLOCK_W, 2.6).move_to([x2, Y_TOP - 1.3, 0])
        probe2 = Probe().next_to(block2, UP, buff=0)
        flaw2 = Ellipse(width=0.6, height=0.2, color=ACCENT_4, stroke_width=4)
        flaw2.set_fill(ACCENT_4, 0.45).move_to([x2, Y_TOP - 1.0, 0])
        surface2 = Line([x2 - BLOCK_W / 2, Y_TOP, 0], [x2 + BLOCK_W / 2, Y_TOP, 0],
                        color=ACCENT_1, stroke_width=9)
        dim_d = DoubleArrow([x2 + 0.5, Y_TOP - 0.06, 0], [x2 + 0.5, flaw2.get_center()[1], 0],
                            buff=0, color=ACCENT_4, stroke_width=3, tip_length=0.14)
        guide_d = DashedLine(flaw2.get_right() + RIGHT * 0.05, [x2 + 0.5, flaw2.get_center()[1], 0],
                             color=ACCENT_4, stroke_width=2)
        lab_d = label("depth", FS_TAG, ACCENT_4, weight=BOLD).next_to(dim_d, RIGHT, 0.1)
        tag2a = tag_line("One surface", "check", OK_C)
        tag2b = tag_line("Gives depth", "ruler", OK_C)
        tag2a.move_to([x2, Y_TAGS, 0]).align_to([x2 - 1.9, 0, 0], LEFT).align_to([0, Y_TAGS, 0], UP)
        tag2b.next_to(tag2a, DOWN, 0.2, aligned_edge=LEFT)
        pill_txt = label("Most used", FS_NOTE, INK, weight=BOLD)
        pill_ic = icon("check", OK_C, 0.42)
        pill_in = VGroup(pill_ic, pill_txt).arrange(RIGHT, buff=0.2)
        pill = RoundedRectangle(width=pill_in.width + 0.6, height=0.7, corner_radius=0.35,
                                color=OK_C, stroke_width=4).set_fill(PANEL_FILL, 1)
        pill_in.move_to(pill)
        pill_all = VGroup(pill, pill_in).move_to([x2, -1.45, 0])

        # ================= panel 3: resonance =================
        x3 = CX[2]
        PLATE_W, PLATE_T = 3.6, 1.4
        head3, rule3 = method_head("Resonance", x3, Y_HEAD, Y_RULE, ACCENT_2)
        plate = SteelBlock(PLATE_W, PLATE_T).move_to([x3, Y_TOP - PLATE_T / 2, 0])
        probe3 = Probe().next_to(plate, UP, buff=0)
        centre = DashedLine([x3, Y_TOP, 0], [x3, Y_TOP - PLATE_T, 0], color=GREY_INK, stroke_width=2)
        f_trk = ValueTracker(0.5)               # drive frequency in units of f1 (the first resonance)
        zs = np.linspace(0.0, 1.0, 50)

        def lobe_side(sign):
            def make():
                f = f_trk.get_value()
                a = 0.1 + 0.52 * resonance_gain(f)
                pts = [[x3 + sign * a * np.sin(PI * f * z), Y_TOP - z * PLATE_T, 0] for z in zs]
                m = VMobject(color=ACCENT_2, stroke_width=5)
                m.set_points_as_corners(pts)
                return m
            return make
        lobes = VGroup(always_redraw(lobe_side(1)), always_redraw(lobe_side(-1)))
        # amplitude-versus-frequency graph under the plate
        G_L, G_W, G_B, G_H = x3 - 1.7, 3.4, -1.3, 1.05
        F0, F1 = 0.4, 1.6
        gx = lambda f: G_L + (f - F0) / (F1 - F0) * G_W
        gy = lambda f: G_B + G_H * (0.06 + 0.94 * resonance_gain(f))
        ax_x = Arrow([G_L - 0.1, G_B, 0], [G_L + G_W + 0.2, G_B, 0], buff=0, color=INK,
                     stroke_width=3, tip_length=0.15)
        ax_y = Arrow([G_L, G_B, 0], [G_L, G_B + G_H + 0.2, 0], buff=0, color=INK,
                     stroke_width=3, tip_length=0.15)
        g_title = label("Received amplitude", FS_TAG, INK).move_to([x3, 0.12, 0])
        g_x = label("Frequency", FS_TAG, INK).next_to(ax_x, DOWN, 0.1).align_to(ax_x, RIGHT)
        full = np.linspace(F0, F1, 120)
        ghost = VMobject(color=GREY_INK, stroke_width=3)
        ghost.set_points_as_corners([[gx(f), gy(f), 0] for f in full]).set_stroke(opacity=0.55)
        trace = always_redraw(lambda: VMobject(color=ACCENT_2, stroke_width=5).set_points_as_corners(
            [[gx(f), gy(f), 0] for f in np.linspace(F0, max(f_trk.get_value(), F0 + 0.02), 60)]))
        knob = always_redraw(lambda: Dot([gx(f_trk.get_value()), gy(f_trk.get_value()), 0],
                                         radius=0.11, color=ACCENT_1))
        dim_t = DoubleArrow([x3 - 1.05, Y_TOP - 0.05, 0], [x3 - 1.05, Y_TOP - PLATE_T + 0.05, 0],
                            buff=0, color=INK, stroke_width=3, tip_length=0.14)
        lab_t = label("t", FS_LABEL, INK, weight=BOLD).next_to(dim_t, LEFT, 0.12)
        lab_half = label("λ / 2", FS_TAG, ACCENT_2, weight=BOLD).move_to(
            [x3 + 0.62 + 0.15 + 0.4, Y_TOP - PLATE_T / 2, 0])
        tag3 = tag_line("Measures thickness", "ruler", OK_C)
        tag3.move_to([x3, Y_TAGS, 0]).align_to([x3 - 1.9, 0, 0], LEFT).align_to([0, Y_TAGS, 0], UP)

        # ---- 2.7-12.6 s: through transmission ----
        self.sync(c("النَّفَاذِ"))
        self.play(FadeIn(head1), Create(rule1), Create(block1), run_time=0.6)
        self.sync(c("مِجَسَّانِ"))
        self.play(FadeIn(pa, shift=DOWN * 0.3), FadeIn(pb, shift=UP * 0.3), FadeIn(sends),
                  FadeIn(recvs), run_time=0.5)
        self.sync(c("مُتَقَابِلَانِ"))
        self.play(FadeIn(meter), Create(meter_wire), FadeIn(meter_lab), FadeIn(beam1), run_time=0.35)
        self.add(fill)
        pk = wave_packet(length=0.55, amp=0.28, cycles=5, color=ACCENT_3, direction=DOWN)
        fly(pk, [x1, top1 - 0.3, 0], [x1, bot1 + 0.3, 0], 0.5)
        self.play(Transform(fill, signal_bar(meter, 0.9, ACCENT_3)), run_time=0.3)
        self.sync(c("وَالعَيْبُ"))
        self.play(FadeIn(flaw1, scale=1.3), run_time=0.4)
        self.sync(c("يَحْجُبُ"))
        pk = wave_packet(length=0.55, amp=0.28, cycles=5, color=ACCENT_3, direction=DOWN)
        fly(pk, [x1, top1 - 0.3, 0], [x1, flaw1.get_top()[1] + 0.25, 0], 0.4)
        pk2 = wave_packet(length=0.4, amp=0.1, cycles=5, color=ACCENT_3, direction=DOWN)
        pk2.move_to([x1, fl_bot - 0.25, 0])
        self.add(pk2)
        self.play(FadeIn(shadow), FadeIn(shadow_lab), pk2.animate(run_time=0.45, rate_func=linear)
                  .move_to([x1, bot1 + 0.25, 0]), Indicate(flaw1, color=ACCENT_4, scale_factor=1.2,
                                                         run_time=0.45))
        self.remove(pk2)
        self.sync(c("فَتَنْخَفِضُ"))
        self.play(Transform(fill, signal_bar(meter, 0.28, ACCENT_4)), run_time=0.6)
        self.sync(c("وَيَلْزَمُ"))
        self.play(FadeIn(tag1a, shift=UP * 0.15), run_time=0.4)
        self.sync(c("الجَانِبَيْنِ"))
        self.play(Indicate(pa, color=ACCENT_1, scale_factor=1.15),
                  Indicate(pb, color=ACCENT_3, scale_factor=1.15), run_time=0.7)
        self.sync(c("وَلَا"))
        self.play(FadeIn(tag1b, shift=UP * 0.15), run_time=0.4)
        self.sync(c("مَوْقِعَ"))
        self.play(FadeIn(ghosts), run_time=0.5)

        # ---- 13.5-20.5 s: pulse-echo ----
        self.sync(c("وَفِي"))
        self.play(FadeIn(head2), Create(rule2), Create(block2), FadeIn(flaw2), run_time=0.5)
        self.sync(c("مِجَسٌّ"))
        self.play(FadeIn(probe2, shift=DOWN * 0.3), run_time=0.4)
        self.play(Indicate(probe2, color=ACCENT_1, scale_factor=1.15), run_time=0.5)
        self.sync(c("سَطْحٍ"))
        self.play(Create(surface2), FadeIn(tag2a, shift=UP * 0.15), run_time=0.5)
        self.sync(c("يُعْطِي", 2))
        pk = wave_packet(length=0.5, amp=0.26, cycles=5, color=ACCENT_1, direction=DOWN)
        fly(pk, [x2, Y_TOP - 0.3, 0], [x2, flaw2.get_top()[1] + 0.22, 0], 0.4)
        echo = wave_packet(length=0.5, amp=0.13, cycles=5, color=ACCENT_2, direction=UP)
        echo.move_to([x2, flaw2.get_top()[1] + 0.22, 0])
        self.add(echo)
        self.play(echo.animate(run_time=0.5, rate_func=linear).move_to([x2, Y_TOP - 0.3, 0]),
                  Flash(flaw2.get_center(), color=ACCENT_4, flash_radius=0.4, line_length=0.1,
                        run_time=0.4),
                  GrowFromCenter(dim_d), Create(guide_d), FadeIn(lab_d))
        self.remove(echo)
        self.play(FadeIn(tag2b, shift=UP * 0.15), run_time=0.35)
        self.sync(c("الأَكْثَرُ"))
        self.play(FadeIn(pill_all, scale=0.8), run_time=0.4)
        self.sync(c("اسْتِعْمَالًا"))
        frame2 = SurroundingRectangle(VGroup(head2, rule2, block2, probe2, tag2a, tag2b, pill_all),
                                      color=OK_C, buff=0.17, corner_radius=0.2, stroke_width=4)
        self.play(Create(frame2), run_time=0.5)

        # ---- 20.9-27 s: resonance ----
        self.sync(c("وَفِي", 2))
        self.play(FadeIn(head3), Create(rule3), run_time=0.4)
        self.sync(c("الرَّنِينِ"))
        self.play(Create(plate), FadeIn(probe3, shift=DOWN * 0.3), Create(centre), run_time=0.4)
        self.add(lobes)
        self.sync(c("نُغَيِّرُ"))
        self.play(Create(ax_x), Create(ax_y), FadeIn(g_title), FadeIn(g_x), Create(ghost),
                  run_time=0.5)
        self.add(trace, knob)
        self.sync(c("التَّرَدُّدَ"))
        self.play(f_trk.animate(run_time=c("السَّمَاكَةُ") - self.renderer.time, rate_func=linear)
                  .set_value(1.0))
        self.sync(c("نِصْفَ"))
        self.play(GrowFromCenter(dim_t), FadeIn(lab_t), FadeIn(lab_half),
                  Flash([gx(1.0), gy(1.0), 0], color=ACCENT_2, flash_radius=0.4, line_length=0.1,
                        run_time=0.5), run_time=0.5)
        self.sync(c("لِنَقِيسَهَا"))
        self.play(FadeIn(tag3, shift=UP * 0.15), run_time=0.4)

        # ---- 27.4-37.3 s: the limits ----
        self.sync(c("وَقُيُودُهَا") - 0.35)
        self.clear(run_time=0.45)
        lim_head = label("Limits", FS_HEADING, ALERT_C, weight=BOLD).move_to([0, 3.0, 0])
        lim_rule = Line(LEFT * 1.4, RIGHT * 1.4, color=ALERT_C, stroke_width=5)
        lim_rule.next_to(lim_head, DOWN, 0.15)
        chips = [chip("Couplant needed", "droplet", ALERT_C, 6.0, FS_LABEL),
                 chip("Flaw parallel to the beam may not be seen", "eye", ALERT_C, 6.0, FS_LABEL),
                 chip("Coarse grains scatter the sound", "wind", ALERT_C, 6.0, FS_LABEL),
                 chip("No measurement without calibration", "scale", ALERT_C, 6.0, FS_LABEL)]
        for ch, (px, py) in zip(chips, ((-3.3, 1.2), (3.3, 1.2), (-3.3, -0.9), (3.3, -0.9))):
            ch.move_to([px, py, 0])
        self.sync(c("وَقُيُودُهَا"))
        self.play(FadeIn(lim_head), Create(lim_rule), run_time=0.5)
        for ch, phrase in zip(chips, (c("الوَسِيطُ"), c("المُوَازِي"), c("الخَشِنَةُ"), c("قِيَاسَ"))):
            self.sync(phrase)
            self.play(FadeIn(ch, shift=UP * 0.2), run_time=0.4)
            self.play(Indicate(ch[1], color=ALERT_C, scale_factor=1.3), run_time=0.5)
        self.sync(self.end(6))
        self.clear()

    # ---------------- Segment 7: review (narration entries 7-31) ----------------
    # entry 7 intro; then for k = 1..8: question 8+3(k-1), silent 3 s countdown 9+3(k-1),
    # answer 10+3(k-1).
    def seg7(self):
        self.sync(self.end(len(NARRATION)) + 1.0)


if __name__ == "__main__":
    main(__file__, "UtSeriesEp01", NARRATION)
