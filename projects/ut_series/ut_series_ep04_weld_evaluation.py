"""ut_series, episode 4: Weld examination and flaw evaluation.

Build (from the repo root, with the virtual environment of the root CLAUDE.md active):
    python projects/ut_series/ut_series_ep04_weld_evaluation.py --preview   # 480p15 -> tmp/ut_series_ep04_weld_evaluation/preview.mp4
    python projects/ut_series/ut_series_ep04_weld_evaluation.py             # 1080p30 -> output/ut_series_ep04_weld_evaluation.mp4

Narration segments: 1-6 are the six sections of the source (TCS-67 §6.1.3, §8.2-8.7, §9.1-9.2); 7 is the review
intro and 8-31 are the eight review questions (question, 3 s silent countdown, answer).
"""
from explainer import *
import numpy as np
import ut_series_data as D
from ut_visuals import (wavefront, Probe, SteelBlock, AScan, tag_line, wrap_two_lines, signal_bar,
                        knob, wedge_probe, WeldSection)
from ut_review import run_review, fly, pk

# Fully diacritized narration, approved by the owner on 2026-10-10 (with his three edits: ASME spelling, the slag sentence).
# Decimals would be spoken digit by digit after «فَاصِلَةٌ» (none in this episode).
NARRATION = [
    # 1  §1 the weld examination procedure (TCS-67 §6.1.3)
    "قَبْلَ الفَحْصِ نَقْرَأُ الإِجْرَاءَ المَكْتُوبَ: تَصْمِيمَ الوُصْلَةِ وَسَمَاكَتَهَا وَزَاوِيَةَ حَافَتِهَا وَطَرِيقَةَ اللِّحَامِ. وَنَتَأَكَّدُ أَنَّ السَّطْحَ خَالٍ مِنَ الرَّشَاشِ، أَمْلَسُ بِمَا يَكْفِي لِحَرَكَةِ المِجَسِّ. نَبْدَأُ بِالمَعْدِنِ الأَسَاسِ بِالمِجَسِّ العَمُودِيِّ، لِأَنَّ التَّصَفُّحَ قَدْ يَعْكِسُ الحُزْمَةَ المَائِلَةَ إِلَى تَاجِ اللِّحَامِ، فَتُظَنُّ إِشَارَتُهُ صَدَى جَذْرٍ. ثُمَّ نَخْتَارُ زَاوِيَةَ المِجَسِّ بِحَسَبِ زَاوِيَةِ حَافَةِ اللِّحَامِ، لِتَسْقُطَ الحُزْمَةُ عَلَى وَجْهِ الِانْصِهَارِ قَرِيبًا مِنَ العَمُودِيِّ، فَيَظْهَرَ عَدَمُ الِانْصِهَارِ بِوُضُوحٍ. وَنَمْسَحُ مِنْ جَانِبَيِ اللِّحَامِ بِنِصْفِ قَفْزَةٍ وَقَفْزَةٍ كَامِلَةٍ، وَمُوَازِيًا لَهُ بَحْثًا عَنِ الشُّقُوقِ المُسْتَعْرِضَةِ. وَنَمْسَحُ بِحَسَاسِيَّةٍ أَعْلَى مِنَ المَرْجِعِ كَيْلَا يَفُوتَنَا عَيْبٌ، ثُمَّ نُقَيِّمُ كُلَّ إِشَارَةٍ عِنْدَ حَسَاسِيَّةِ المَرْجِعِ.",
    # 2  §2 the recording level (§8.2)
    "لَا تُسَجَّلُ كُلُّ إِشَارَةٍ. نَعْتَمِدُ عَلَى مُنْحَنَى دِي إِيهْ سِي، وَهُوَ خَطٌّ يَصِلُ قِمَمَ أَصْدَاءِ عَاكِسَاتٍ مُتَمَاثِلَةٍ عَلَى أَعْمَاقٍ مُخْتَلِفَةٍ، وَيَهْبِطُ مَعَ العُمْقِ لِأَنَّ الحُزْمَةَ تَتَّسِعُ وَالمَوْجَةَ تَتَوَهَّنُ. وَيُحَدِّدُ الإِجْرَاءُ أَوِ الكُودُ مُسْتَوَى تَسْجِيلٍ نِسْبَةً إِلَى هٰذَا المُنْحَنَى. صَدًى تَحْتَهُ نُهْمِلُهُ، وَصَدًى فَوْقَهُ نَتَحَرَّى عَنْهُ وَنُسَجِّلُ مَوْقِعَهُ وَنَوْعَهُ وَطُولَهُ وَسَعَتَهُ. وَيُحَدِّدُ الكُودُ أَيْضًا مُسْتَوًى أَعْلَى لِلتَّقْيِيمِ أَوِ الرَّفْضِ، وَالنِّسَبُ تَخْتَلِفُ مِنْ كُودٍ لِآخَرَ.",
    # 3  §3 sizing the length by the 6 dB drop (§8.4.2.1): the one worked example
    "لِقِيَاسِ طُولِ العَيْبِ نُحَرِّكُ المِجَسَّ حَتَّى يَبْلُغَ الصَّدَى أَقْصَاهُ، ثُمَّ نُحَرِّكُهُ عَلَى طُولِ العَيْبِ حَتَّى تَهْبِطَ السَّعَةُ إِلَى النِّصْفِ، أَيْ سِتَّةَ دِيسِيبِلْ. فَعِنْدَهَا يَقَعُ مِحْوَرُ الحُزْمَةِ عَلَى طَرَفِ العَيْبِ تَمَامًا: نِصْفُهَا عَلَيْهِ وَنِصْفُهَا خَارِجَهُ. نُعَلِّمُ مَوْضِعَ المِجَسِّ، وَنُكَرِّرُ نَحْوَ الطَّرَفِ الآخَرِ، وَالمَسَافَةُ بَيْنَ العَلَامَتَيْنِ هِيَ طُولُ العَيْبِ. مِثَالٌ: هَبَطَتِ السَّعَةُ سِتَّةَ دِيسِيبِلْ عِنْدَ مِئَةٍ وَاثْنَيْ عَشَرَ مِلِّيمِتْرًا مِنْ مَرْجِعِ اللِّحَامِ، وَعِنْدَ مِئَةٍ وَخَمْسَةٍ وَثَلَاثِينَ فِي الِاتِّجَاهِ الآخَرِ. فَالطُّولُ مِئَةٌ وَخَمْسَةٌ وَثَلَاثُونَ نَاقِصُ مِئَةٍ وَاثْنَيْ عَشَرَ، أَيْ ثَلَاثَةٌ وَعِشْرُونَ مِلِّيمِتْرًا. وَهٰذِهِ الطَّرِيقَةُ لِلطُّولِ، وَتَصْلُحُ لِلْعُيُوبِ الأَكْبَرِ مِنْ عَرْضِ الحُزْمَةِ؛ وَالأَصْغَرُ نُقَدِّرُهُ بِمُقَارَنَةِ سَعَتِهِ بِمُنْحَنَى دِي إِيهْ سِي أَوْ بِمُخَطَّطِ دِي جِي إِسْ.",
    # 4  §4 telling the flaw type from the echo (§8.5)
    "نَحْكُمُ عَلَى نَوْعِ العَيْبِ مِنْ سُلُوكِ صَدَاهُ حِينَ نُحَرِّكُ المِجَسَّ بِأَرْبَعِ حَرَكَاتٍ: إِلَى الأَمَامِ وَالخَلْفِ عَمُودِيًّا عَلَى اللِّحَامِ، وَجَانِبِيًّا مُوَازِيًا لَهُ، وَدَوَرَانًا حَوْلَ مِحْوَرِ المِجَسِّ، وَحَرَكَةً مَدَارِيَّةً حَوْلَ العَيْبِ. المَسَامَةُ المُنْفَرِدَةُ كُرَوِيَّةٌ، فَهِيَ عَاكِسٌ ضَعِيفٌ، وَصَدَاهَا صَغِيرٌ لَا يَتَغَيَّرُ مِنْ أَيِّ اتِّجَاهٍ. وَالمَسَامِيَّةُ أَصْدَاءٌ صَغِيرَةٌ كَثِيرَةٌ تَرْتَفِعُ وَتَهْبِطُ بِسُرْعَةٍ وَنُعُومَةٍ. وَالخَبَثُ قَدْ يُعْطِي صَدًى عَالِيًا كَالشَّقِّ، مُتَعَدِّدَ القِمَمِ كَشَجَرَةِ صَنَوْبَرٍ، لَا يَتَغَيَّرُ ارْتِفَاعُهُ حِينَ نَدُورُ حَوْلَهُ. وَالعَيْبُ المُسْتَوِي، كَالشَّقِّ وَعَدَمِ الِانْصِهَارِ، صَدَاهُ قَوِيٌّ حِينَ تَسْقُطُ الحُزْمَةُ عَلَيْهِ عَمُودِيَّةً، وَيَهْبِطُ كَثِيرًا مِنَ الِاتِّجَاهِ الآخَرِ، وَهُوَ الأَخْطَرُ. وَيَجْمَعُ الحُكْمُ المَوْقِعَ مَعَ السُّلُوكِ، لَا شَكْلَ صَدًى وَاحِدٍ.",
    # 5  §5 accept / reject by the code, and the report (§8.6, §8.7)
    "الحُكْمُ بِالقَبُولِ أَوِ الرَّفْضِ لَيْسَ لِلْفَاحِصِ، بَلْ لِمَعَايِيرِ الكُودِ المَذْكُورِ فِي العَقْدِ، مِثْلِ إِيهْ إِسْ إِمْ إِي وَإِيهْ دَبْلْيُو إِسْ وَإِيهْ بِي آيْ. وَتَعْتَمِدُ مَعَايِيرُهَا عَادَةً عَلَى سَعَةِ الصَّدَى نِسْبَةً إِلَى المَرْجِعِ، وَعَلَى طُولِ العَيْبِ وَنَوْعِهِ. وَكَثِيرٌ مِنَ الأَكْوَادِ يَرْفُضُ الشُّقُوقَ وَعَدَمَ الِانْصِهَارِ وَعَدَمَ التَّغَلْغُلِ مَهْمَا كَانَ طُولُهَا. وَالتَّقْرِيرُ يَجْعَلُ الفَحْصَ قَابِلًا لِلْمُرَاجَعَةِ وَالتَّكْرَارِ: يَذْكُرُ القِطْعَةَ وَاللِّحَامَ، وَالإِجْرَاءَ وَالكُودَ، وَالجِهَازَ وَالمِجَسَّاتِ وَزَوَايَاهَا، وَالمُعَايَرَةَ وَالحَسَاسِيَّةَ وَالوَسِيطَ، وَمَنَاطِقَ المَسْحِ، وَجَدْوَلَ الإِشَارَاتِ، وَالنَّتِيجَةَ، وَاسْمَ الفَاحِصِ وَالتَّارِيخَ. وَهٰذَا تَقْرِيرٌ تَوْضِيحِيٌّ لِلْعَيْبِ نَفْسِهِ: عُمْقُهُ خَمْسَةٌ وَعِشْرُونَ مِلِّيمِتْرًا، وَطُولُهُ ثَلَاثَةٌ وَعِشْرُونَ، وَسَعَتُهُ ثَمَانُونَ بِالمِئَةِ مِنَ المُنْحَنَى.",
    # 6  §6 a glimpse of PAUT and TOFD, and the close of the series (§9.1-9.2)
    "وَلَمْحَةٌ عَمَّا بَعْدَ المَسْحِ اليَدَوِيِّ. فِي المَصْفُوفَةِ الطَّوْرِيَّةِ يَحْمِلُ المِجَسُّ عَنَاصِرَ صَغِيرَةً كَثِيرَةً تُطْلَقُ بِتَأْخِيرَاتٍ زَمَنِيَّةٍ مَحْسُوبَةٍ، فَتُوَجَّهُ الحُزْمَةُ وَتُرَكَّزُ إِلِكْتْرُونِيًّا دُونَ تَحْرِيكِ المِجَسِّ. وَالمَسْحُ القِطَاعِيُّ يَكْنُسُ مَدًى مِنَ الزَّوَايَا وَيَرْسُمُ صُورَةً لِمَقْطَعِ اللِّحَامِ. وَفِي زَمَنِ الحَيْدِ مِجَسَّانِ عَلَى جَانِبَيِ اللِّحَامِ، مُرْسِلٌ وَمُسْتَقْبِلٌ: تَصِلُ أَوَّلًا المَوْجَةُ الجَانِبِيَّةُ، وَأَخِيرًا صَدَى الجِدَارِ الخَلْفِيِّ، وَبَيْنَهُمَا إِشَارَتَا الحَيْدِ مِنْ طَرَفَيِ الشَّقِّ، وَمِنْ زَمَنِ وُصُولِهِمَا نَحْسُبُ ارْتِفَاعَهُ بِدِقَّةٍ، دُونَ اعْتِمَادٍ كَبِيرٍ عَلَى اتِّجَاهِ العَيْبِ، وَمِنْ قُيُودِهِ مِنْطَقَةٌ مَيِّتَةٌ تَحْتَ السَّطْحِ. وَهٰكَذَا مَشَيْنَا مِنَ المَبْدَأِ إِلَى المِجَسِّ وَالحُزْمَةِ، ثُمَّ إِلَى المُعَايَرَةِ، ثُمَّ إِلَى الحُكْمِ عَلَى العَيْبِ.",
    # 7  review: intro, then (question, 3 s countdown, answer) x 8
    "نُرَاجِعُ مَا تَعَلَّمْنَاهُ بِثَمَانِيَةِ أَسْئِلَةٍ. بَعْدَ كُلِّ سُؤَالٍ ثَلَاثُ ثَوَانٍ لِتُجِيبَ بِنَفْسِكَ.",
    "لِمَاذَا نَفْحَصُ المَعْدِنَ الأَسَاسَ بِالمِجَسِّ العَمُودِيِّ أَوَّلًا؟", 3,
    "لِأَنَّ التَّصَفُّحَ قَدْ يَعْكِسُ الحُزْمَةَ المَائِلَةَ فَيُعْطِي إِشَارَةً مُضَلِّلَةً.",
    "بِأَيِّ حَسَاسِيَّةٍ نَمْسَحُ، وَبِأَيِّ حَسَاسِيَّةٍ نُقَيِّمُ؟", 3,
    "نَمْسَحُ بِحَسَاسِيَّةٍ أَعْلَى، وَنُقَيِّمُ عِنْدَ حَسَاسِيَّةِ المَرْجِعِ.",
    "مَاذَا نَفْعَلُ بِصَدًى تَحْتَ مُسْتَوَى التَّسْجِيلِ، وَبِصَدًى فَوْقَهُ؟", 3,
    "نُهْمِلُ الأَوَّلَ، وَنَتَحَرَّى عَنِ الثَّانِي وَنُسَجِّلُهُ.",
    "لِمَاذَا نَتَوَقَّفُ عِنْدَ نِصْفِ السَّعَةِ فِي طَرِيقَةِ هُبُوطِ سِتَّةِ دِيسِيبِلْ؟", 3,
    "لِأَنَّ مِحْوَرَ الحُزْمَةِ يَكُونُ عِنْدَئِذٍ عَلَى طَرَفِ العَيْبِ.",
    "هَبَطَتِ السَّعَةُ سِتَّةَ دِيسِيبِلْ عِنْدَ مِئَةٍ وَاثْنَيْ عَشَرَ وَعِنْدَ مِئَةٍ وَخَمْسَةٍ وَثَلَاثِينَ مِلِّيمِتْرًا: مَا طُولُ العَيْبِ؟", 3,
    "ثَلَاثَةٌ وَعِشْرُونَ مِلِّيمِتْرًا.",
    "مَاذَا يَحْدُثُ لِصَدَى العَيْبِ المُسْتَوِي حِينَ نَدُورُ حَوْلَهُ؟", 3,
    "يَهْبِطُ كَثِيرًا، بِخِلَافِ المَسَامَةِ وَالخَبَثِ.",
    "مَنْ يَحْكُمُ بِقَبُولِ العَيْبِ أَوْ رَفْضِهِ؟", 3,
    "مَعَايِيرُ الكُودِ المَذْكُورِ فِي العَقْدِ، لَا الفَاحِصُ.",
    "مَاذَا يَسْتَعْمِلُ زَمَنُ الحَيْدِ لِحِسَابِ ارْتِفَاعِ الشَّقِّ؟", 3,
    "زَمَنَ وُصُولِ إِشَارَتَيِ الحَيْدِ مِنْ طَرَفَيْهِ.",
]

# Every spoken or shown value is checked against the data module; stop if it drifts.
assert D.FLAW_LENGTH == 23.0 and int(D.POS_6DB_1) == 112 and int(D.POS_6DB_2) == 135      # seg 3, review Q5
assert abs(D.DROP_6DB_DB + 6.02) < 5e-3 and D.AMP_RATIO_6DB == 0.5                       # seg 3 (6 dB = one half)
assert f"{D.REPORT_DEPTH:.1f}" == "25.0" and f"{D.REPORT_SURFACE_DIST:.1f}" == "43.3"    # seg 5 (the flaw of episode 3)
assert D.AMP_PCT_DAC == 80 and int(D.REPORT_LENGTH) == 23                                # seg 5
assert D.ILLUSTRATIVE_ECHO_LOW_PCT_DAC < D.ILLUSTRATIVE_RECORD_PCT_DAC < D.ILLUSTRATIVE_EVAL_PCT_DAC < D.AMP_PCT_DAC   # seg 2

AUDIO_DIR = audio_dir_for(__file__)

# Colour roles of this project (project CLAUDE.md): ACCENT_1 sound / probe / incident wave,
# ACCENT_2 reflected wave / echo, ACCENT_3 transmitted wave / OK, ACCENT_4 flaw / alarm.


# ---- Helpers shared by the segments ----
def chip(text, icon_name, color=INK, width=3.2):
    """A rounded note with an icon and a short text (parts: box, icon, txt)."""
    ic = icon(icon_name, color, 0.42)
    t = label(text, FS_TAG, INK, weight=BOLD)
    box = RoundedRectangle(width=width, height=0.7, corner_radius=0.18, color=color, stroke_width=3).set_fill(PANEL_FILL, 1)
    ic.move_to(box.get_left() + RIGHT * 0.42)
    t.next_to(ic, RIGHT, 0.18)
    g = VGroup(box, ic, t)
    g.box, g.icon, g.txt = box, ic, t
    return g


def right_angle_mark(point, d1, d2, size=0.2, color=INK):
    """A small square marking a right angle at `point` between the unit directions d1 and d2."""
    d1, d2 = np.array(d1, dtype=float), np.array(d2, dtype=float)
    return Polygon(point, point + d1 * size, point + (d1 + d2) * size, point + d2 * size, color=color, stroke_width=3)


def wf(color, direction, amp=0.2, length=0.55):
    """A small pulse (wave-front arcs) for the section drawings."""
    return wavefront(length=length, amp=amp, color=color, direction=direction)


def travel(scene, mob, pts, run_time, rate_func=linear):
    """A pulse travels through the points `pts` in turn (equal speed), and is removed on arrival."""
    pts = [np.array(p, dtype=float) for p in pts]
    mob.move_to(pts[0])
    scene.add(mob)
    lens = [np.linalg.norm(b - a) for a, b in zip(pts, pts[1:])]
    tot = sum(lens)
    for (a, b), ln in zip(zip(pts, pts[1:]), lens):
        scene.play(mob.animate(run_time=run_time * ln / tot, rate_func=rate_func).move_to(b))
    scene.remove(mob)

# HELPERS-END


class UtSeriesEp04(SyncedScene):
    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        self.seg1()
        self.seg2()
        self.seg3()
        self.seg4()
        self.seg5()
        self.seg6()
        self.seg7()

    # ---------------- Segment 1: the weld examination procedure (§6.1.3) ----------------
    def seg1(self):
        c = lambda phrase, nth=1: self.cue(1, phrase, nth)
        S = self.start(1)
        title_card(self, "Ultrasonic Testing", "Weld examination and flaw evaluation",
                   series="Ultrasonic Testing Series · Episode 4", run_time=1.6)
        self.sync(S + 2.0)
        self.clear(run_time=0.4)

        TOP, T = 0.0, 1.4
        wd = WeldSection(cx=0.0, y_top=TOP, t=T, half_w=6.2)
        W, G = wd.w, wd.gap
        apex = np.array([0.0, TOP - T * W / (W - G), 0.0])

        def edge_angle():
            """The edge angle at the vee: an arc about the virtual apex, with its label and leader."""
            arc = Arc(radius=1.15, start_angle=PI / 2 - np.radians(30), angle=np.radians(60), arc_center=apex,
                      color=ACCENT_1, stroke_width=5)
            lab = label("edge angle", FS_TAG, ACCENT_1, weight=BOLD).move_to([0.0, TOP + 0.85, 0])
            lead = Arrow(lab.get_bottom() + DOWN * 0.04, arc.point_from_proportion(0.5), buff=0.06, color=ACCENT_1,
                         stroke_width=3, tip_length=0.14)
            return arc, lab, lead

        # ---- what we know first: the written procedure ----
        self.play(FadeIn(wd, run_time=0.6))
        head = chip("Written procedure", "file-text", ACCENT_1, 3.6).move_to([0, 3.2, 0])
        row = VGroup(chip("Joint design", "tools", INK, 2.9), chip("Thickness", "ruler", INK, 2.9),
                     chip("Edge angle", "filter", INK, 2.9), chip("Welding method", "flame", INK, 2.9))
        row.arrange(RIGHT, buff=0.25).move_to([0, 2.35, 0])
        self.sync(c("الإِجْرَاءَ"))
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.4)
        self.sync(c("الوُصْلَةِ"))
        flash = wd.weld.copy().set_stroke(ACCENT_1, 6).set_fill(opacity=0)
        self.play(FadeIn(row[0], shift=DOWN * 0.15), ShowPassingFlash(flash, time_width=1.0), run_time=0.7)
        self.sync(c("وَسَمَاكَتَهَا"))
        dim = DoubleArrow([-5.6, TOP, 0], [-5.6, TOP - T, 0], buff=0, color=ACCENT_1, stroke_width=3, tip_length=0.14)
        dim_lab = label("thickness", FS_TAG, ACCENT_1, weight=BOLD).move_to([-5.6, TOP + 0.45, 0])
        self.play(FadeIn(row[1], shift=DOWN * 0.15), GrowArrow(dim), FadeIn(dim_lab), run_time=0.6)
        self.sync(c("وَزَاوِيَةَ"))
        arc, arc_lab, arc_lead = edge_angle()
        self.play(FadeIn(row[2], shift=DOWN * 0.15), Create(arc), FadeIn(arc_lab), GrowArrow(arc_lead), run_time=0.7)
        self.sync(c("وَطَرِيقَةَ"))
        self.play(FadeIn(row[3], shift=DOWN * 0.15), Indicate(wd.weld, color=ACCENT_2, scale_factor=1.0), run_time=0.7)

        # ---- the surface: free of spatter and smooth ----
        self.sync(c("وَنَتَأَكَّدُ") + 0.1)
        self.play(FadeOut(VGroup(head, row, dim, dim_lab, arc, arc_lab, arc_lead)), run_time=0.5)
        sx = [-5.7, -5.0, -4.3, -3.6, -2.9, -2.2, 1.5, 2.2, 2.9, 3.6, 4.3, 5.2]
        dots = VGroup(*[Dot([x, TOP + 0.05 + 0.03 * (k % 3), 0], radius=0.05 + 0.02 * (k % 2), color=ACCENT_2)
                        for k, x in enumerate(sx)])
        self.sync(c("الرَّشَاشِ"))
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.08, run_time=0.9))
        self.sync(c("أَمْلَسُ"))
        brush = RoundedRectangle(width=0.22, height=0.5, corner_radius=0.06, color=ACCENT_1, stroke_width=3)
        brush.set_fill(ACCENT_1, 0.4).move_to([-6.1, TOP + 0.3, 0])
        self.play(FadeIn(brush, run_time=0.2))
        self.play(brush.animate(run_time=1.6, rate_func=linear).move_to([6.1, TOP + 0.3, 0]),
                  LaggedStart(*[FadeOut(d) for d in dots], lag_ratio=0.08, run_time=1.5))
        self.play(FadeOut(brush, run_time=0.2))
        ok_t = tag_line("free of spatter, smooth enough for the probe", "check", OK_C, width=7.4).move_to([0, 1.7, 0])
        self.sync(c("بِمَا"))
        self.play(FadeIn(ok_t, shift=UP * 0.15), run_time=0.5)

        # ---- the parent metal first, with the normal probe: a lamination can mislead the angle beam ----
        LX = -2.3                                              # centre of the lamination
        Y_LAM = TOP - 0.7
        lam = Ellipse(width=1.6, height=0.12, color=ACCENT_4, stroke_width=3).set_fill(ACCENT_4, 0.9).move_to([LX, Y_LAM, 0])
        lam_tag = label("lamination", FS_TAG, ACCENT_4, weight=BOLD).move_to([LX, TOP - T - 0.55, 0])
        lam_lead = Arrow(lam_tag.get_top() + UP * 0.04, [LX, Y_LAM - 0.1, 0], buff=0.05, color=ACCENT_4, stroke_width=3,
                         tip_length=0.12)
        par = label("parent metal", FS_TAG, INK, weight=BOLD).move_to([-4.6, TOP - T - 0.55, 0])
        self.sync(c("بِالمَعْدِنِ"))
        self.play(FadeOut(ok_t), FadeIn(par, shift=UP * 0.1), run_time=0.5)
        npr = Probe(color=ACCENT_1)
        npr.shift(np.array([LX, TOP, 0.0]) - npr.face_point())
        self.sync(c("بِالمِجَسِّ", 1) - 0.1)
        self.play(FadeIn(npr, shift=DOWN * 0.2), run_time=0.4)
        nb = DashedLine([LX, TOP, 0], [LX, Y_LAM + 0.07, 0], color=ACCENT_1, stroke_width=3)
        self.sync(c("العَمُودِيِّ"))
        self.play(Create(lam), run_time=0.4)
        self.add(nb)
        travel(self, wf(ACCENT_1, DOWN, amp=0.18), [[LX, TOP - 0.05, 0], [LX, Y_LAM + 0.12, 0]], 0.5)
        travel(self, wf(ACCENT_2, UP, amp=0.18), [[LX, Y_LAM + 0.12, 0], [LX, TOP - 0.05, 0]], 0.5)
        self.play(FadeIn(lam_tag), GrowArrow(lam_lead), run_time=0.4)
        # the angle beam: the lamination reflects it up to the cap, where it reads like a root echo
        XE = -3.47                                             # exit point of the 60 degree probe
        hit = np.array([XE + (TOP - Y_LAM) * np.tan(np.radians(60)), Y_LAM, 0.0])
        land = np.array([XE + 2 * (TOP - Y_LAM) * np.tan(np.radians(60)), TOP + 0.04, 0.0])
        self.sync(c("لِأَنَّ"))
        apr = wedge_probe(XE, TOP, size=0.9)
        self.play(FadeOut(npr), FadeOut(nb), FadeIn(apr), run_time=0.5)
        self.sync(c("يَعْكِسُ"))
        leg1 = DashedLine(apr.exit, hit, color=ACCENT_1, stroke_width=3)
        self.play(Create(leg1), run_time=0.5)
        leg2 = DashedLine(hit, land, color=ACCENT_2, stroke_width=3)
        self.sync(c("تَاجِ") - 0.3)
        self.play(Create(leg2), run_time=0.5)
        self.play(Indicate(wd.cap, color=ACCENT_2, scale_factor=1.0), run_time=0.5)
        fs = small_scan([5.0, 1.5], [(0, 1.1), (55, 0.95)], width=3.0, height=2.0, t_max=110.0, ticks=(0, 50, 100),
                        x_caption="", y_caption="")
        mis = tag_line("read as a root echo", "alert-triangle", ALERT_C, width=3.3).move_to([5.0, 0.15, 0])
        self.sync(c("فَتُظَنُّ"))
        self.play(FadeIn(fs), FadeIn(fs.trace), run_time=0.5)
        self.sync(c("جَذْرٍ") - 0.2)
        self.play(FadeIn(mis, shift=UP * 0.1), run_time=0.4)

        # ---- the probe angle follows the edge angle: the beam meets the fusion face square on ----
        self.sync(c("ثُمَّ", 1) - 0.1)
        self.play(FadeOut(VGroup(lam, lam_tag, lam_lead, par, apr, leg1, leg2, fs, fs.trace, mis)), run_time=0.5)
        FR = 0.9                                               # where on the right fusion face the lack of fusion is
        F = wd.face_point(1, FR)
        dface = wd.face_r.get_end() - wd.face_r.get_start()
        dface = dface / np.linalg.norm(dface)
        depth = TOP - F[1]
        lof = Line(wd.face_point(1, 0.76), wd.face_point(1, 0.98), color=ACCENT_4, stroke_width=9)
        lof_tag = label("lack of fusion", FS_TAG, ACCENT_4, weight=BOLD).move_to([3.1, TOP - 1.25, 0])
        lof_lead = Arrow(lof_tag.get_left() + LEFT * 0.04, F + RIGHT * 0.08, buff=0.05, color=ACCENT_4, stroke_width=3, tip_length=0.12)
        v45 = np.array([np.sin(np.radians(45)), -np.cos(np.radians(45)), 0.0])
        refl = 2 * np.dot(v45, dface) * dface - v45
        ghost_start = np.array([F[0] - depth * np.tan(np.radians(45)), TOP, 0.0])
        g_in = DashedLine(ghost_start, F, color=GREY_INK, stroke_width=3)
        g_out = DashedLine(F, F + refl * 2.0, color=ACCENT_2, stroke_width=3)
        wrong = tag_line("slanted hit: the echo is lost", "alert-triangle", ALERT_C, width=4.6).move_to([-3.6, 1.7, 0])
        self.sync(c("نَخْتَارُ"))
        self.play(Create(lof), FadeIn(lof_tag), GrowArrow(lof_lead), run_time=0.6)
        self.sync(c("المِجَسِّ", 2))
        self.play(Create(g_in), run_time=0.4)
        self.play(Create(g_out), FadeIn(wrong, shift=UP * 0.1), run_time=0.5)
        self.sync(c("زَاوِيَةِ") + 0.1)
        arc, arc_lab, arc_lead = edge_angle()
        self.play(Create(arc), FadeIn(arc_lab), GrowArrow(arc_lead), run_time=0.6)
        self.sync(c("لِتَسْقُطَ"))
        self.play(FadeOut(VGroup(g_in, g_out, wrong, arc, arc_lab, arc_lead)), run_time=0.4)
        XE60 = F[0] - depth * np.tan(np.radians(60))
        apr = wedge_probe(XE60, TOP, size=0.9)
        beam = DashedLine(apr.exit, F, color=ACCENT_1, stroke_width=4)
        self.play(FadeIn(apr), Create(beam), run_time=0.6)
        self.sync(c("وَجْهِ") + 0.3)
        self.play(Indicate(wd.face_r, color=ACCENT_1, scale_factor=1.0), run_time=0.5)
        v60 = np.array([np.sin(np.radians(60)), -np.cos(np.radians(60)), 0.0])
        sq = right_angle_mark(F, -dface, -v60, size=0.24, color=ACCENT_1)
        self.sync(c("العَمُودِيِّ", 2) - 0.2)
        self.play(Create(sq), run_time=0.4)
        fs2 = small_scan([5.0, 1.5], [(0, 1.1), (50, 1.5)], width=3.0, height=2.0, t_max=110.0, ticks=(0, 50, 100),
                         x_caption="", y_caption="")
        good = tag_line("clear echo", "check", OK_C, width=3.0).move_to([5.0, 0.15, 0])
        self.sync(c("عَدَمُ"))
        travel(self, wf(ACCENT_2, -v60, amp=0.2), [F, apr.exit + np.array([0, 0.05, 0])], 0.7)
        self.play(FadeIn(fs2), FadeIn(fs2.trace), FadeIn(good, shift=UP * 0.1), run_time=0.5)

        # ---- the scan lines: half skip and full skip, from both sides; parallel to the weld for transverse cracks ----
        self.sync(c("وَنَمْسَحُ", 1) - 0.1)
        self.play(FadeOut(VGroup(lof, lof_tag, lof_lead, apr, beam, sq, fs2, fs2.trace, good)), run_time=0.5)
        HALF, FULL = T * np.tan(np.radians(60)), 2 * T * np.tan(np.radians(60))
        ticks, tags = VGroup(), VGroup()
        for sgn in (-1, 1):
            for dist, name in ((HALF, "½ skip"), (FULL, "full skip")):
                x = sgn * dist
                ticks.add(Line([x, TOP, 0], [x, TOP + 0.3, 0], color=INK, stroke_width=4))
                tags.add(label(name, FS_TAG, INK, weight=BOLD).move_to([x, TOP + 0.62, 0]))
        pl_a, pr_a = wedge_probe(-HALF, TOP, facing=1, size=0.9), wedge_probe(HALF, TOP, facing=-1, size=0.9)
        beams_a = VGroup(DashedLine([-HALF, TOP, 0], [0, TOP - T, 0], color=ACCENT_1, stroke_width=4),
                         DashedLine([HALF, TOP, 0], [0, TOP - T, 0], color=ACCENT_1, stroke_width=4))
        self.sync(c("جَانِبَيِ"))
        self.play(FadeIn(pl_a), FadeIn(pr_a), Create(beams_a), run_time=0.6)
        self.sync(c("بِنِصْفِ"))
        self.play(FadeIn(ticks[1]), FadeIn(tags[1]), FadeIn(ticks[2]), FadeIn(tags[2]), run_time=0.5)
        self.sync(c("وَقَفْزَةٍ"))
        pl_b, pr_b = wedge_probe(-FULL, TOP, facing=1, size=0.9), wedge_probe(FULL, TOP, facing=-1, size=0.9)
        beams_b = VGroup(
            VGroup(DashedLine([-FULL, TOP, 0], [-HALF, TOP - T, 0], color=ACCENT_1, stroke_width=4),
                   DashedLine([-HALF, TOP - T, 0], [0, TOP, 0], color=ACCENT_2, stroke_width=4)),
            VGroup(DashedLine([FULL, TOP, 0], [HALF, TOP - T, 0], color=ACCENT_1, stroke_width=4),
                   DashedLine([HALF, TOP - T, 0], [0, TOP, 0], color=ACCENT_2, stroke_width=4)))
        self.play(FadeIn(ticks[0]), FadeIn(tags[0]), FadeIn(ticks[3]), FadeIn(tags[3]),
                  Transform(pl_a, pl_b), Transform(pr_a, pr_b), FadeOut(beams_a), run_time=0.7)
        self.play(Create(beams_b), run_time=0.7)
        # parallel to the weld: a plan view with a transverse crack
        self.sync(c("وَمُوَازِيًا") - 0.3)
        self.play(FadeOut(VGroup(wd, ticks, tags, pl_a, pr_a, beams_b)), run_time=0.5)
        plate = Rectangle(width=11.6, height=3.4, color=INK, stroke_width=4).set_fill(PANEL_FILL, 1).move_to([0, 0.1, 0])
        band = Rectangle(width=11.6, height=0.8, color=GREY_INK, stroke_width=2).set_fill(ACCENT_2, 0.16).move_to([0, 0.1, 0])
        wlab = label("weld", FS_TAG, INK, weight=BOLD).move_to([-4.9, 1.15, 0])
        crack = Line([1.9, -0.2, 0], [1.9, 0.4, 0], color=ACCENT_4, stroke_width=7)
        clab = label("transverse crack", FS_TAG, ACCENT_4, weight=BOLD).move_to([1.9, 1.15, 0])
        plan_probe = RoundedRectangle(width=0.9, height=0.5, corner_radius=0.08, color=ACCENT_1, stroke_width=4).set_fill(BG, 1)
        nose = Polygon([0.45, -0.25, 0], [0.45, 0.25, 0], [0.7, 0, 0], color=ACCENT_1, stroke_width=3).set_fill(ACCENT_1, 0.5)
        pp = VGroup(plan_probe, nose).move_to([-3.6, 0.1, 0])
        cone = Polygon([-3.0, 0.1, 0], [1.8, 0.3, 0], [1.8, -0.1, 0], color=ACCENT_1, stroke_width=0).set_fill(ACCENT_1, 0.18)
        par_tag = tag_line("scan parallel to the weld: transverse cracks", "search", ACCENT_1, width=7.8).move_to([0, -2.35, 0])
        self.sync(c("بَحْثًا"))
        self.play(FadeIn(plate), FadeIn(band), FadeIn(wlab), FadeIn(crack), FadeIn(clab), FadeIn(pp), run_time=0.6)
        self.play(FadeIn(cone), FadeIn(par_tag, shift=UP * 0.1), run_time=0.4)
        self.sync(c("المُسْتَعْرِضَةِ") + 0.2)
        self.play(pp.animate(run_time=1.0).shift(RIGHT * 1.0))
        travel(self, wf(ACCENT_2, LEFT, amp=0.14, length=0.4), [[1.8, 0.1, 0], [-1.5, 0.1, 0]], 0.8)

        # ---- two sensitivities: scan high, evaluate at the reference ----
        self.sync(c("وَنَمْسَحُ", 2) - 0.3)
        self.clear(run_time=0.5)
        g = ValueTracker(1.0)
        scr = AScan([(0, 1.5), (40, 0.22), (75, 0.62)], width=6.8, height=3.2, t_min=-6.0, t_max=110.0,
                    ticks=(0, 25, 50, 75, 100), sigma=0.9, x_caption="Distance (mm)", y_caption="Echo amplitude")
        scr.shift(np.array([-2.4, 0.3, 0.0]) - scr.frame.get_center())
        scr.trace.add_updater(lambda m: (setattr(scr, "peaks", [(0, 1.5), (40, 0.22 * g.get_value()), (75, 0.62 * g.get_value())]),
                                         scr.update_trace(scr.t_max)))
        ref_y = scr.y_base() + 0.62
        ref = DashedLine([scr.frame.get_left()[0] + 0.5, ref_y, 0], [scr.frame.get_right()[0] - 0.3, ref_y, 0],
                         color=ACCENT_3, stroke_width=3)
        ref_lab = label("reference level", FS_TAG, ACCENT_3, weight=BOLD).next_to(ref, UP, 0.08).align_to(ref, RIGHT)
        k_scan, k_eval = knob("Scanning"), knob("Evaluating")
        k_scan.move_to([4.9, 1.5, 0]).set_turn(0.5)
        k_eval.move_to([4.9, -1.5, 0]).set_turn(0.5)
        self.play(FadeIn(scr), run_time=0.5)
        self.add(scr.trace)
        self.sync(c("بِحَسَاسِيَّةٍ"))
        self.play(FadeIn(k_scan), FadeIn(k_eval), run_time=0.4)
        self.sync(c("أَعْلَى"))
        self.play(g.animate(run_time=1.2).set_value(1.8), UpdateFromAlphaFunc(k_scan, lambda m, a: m.set_turn(0.5 + 0.35 * a)),
                  k_scan.ring.animate.set_stroke(ACCENT_2))
        weak_tag = tag_line("nothing is missed", "eye", ACCENT_2, width=3.3).move_to([4.9, -3.1, 0])
        self.sync(c("كَيْلَا"))
        self.play(Indicate(scr.frame, color=ACCENT_2, scale_factor=1.0), run_time=0.5)
        self.sync(c("يَفُوتَنَا"))
        self.play(FadeIn(weak_tag, shift=UP * 0.1), run_time=0.4)
        self.sync(c("نُقَيِّمُ"))
        self.play(FadeOut(weak_tag), g.animate(run_time=1.0).set_value(1.0),
                  UpdateFromAlphaFunc(k_scan, lambda m, a: m.set_turn(0.85 - 0.35 * a)),
                  k_scan.ring.animate.set_stroke(INK), k_eval.ring.animate.set_stroke(ACCENT_3))
        self.sync(c("عِنْدَ"))
        self.play(Create(ref), FadeIn(ref_lab), run_time=0.5)
        self.sync(c("المَرْجِعِ", 2))
        self.play(Indicate(ref, color=ACCENT_3, scale_factor=1.0), run_time=0.5)
        self.sync(self.end(1))
        scr.trace.clear_updaters()
        self.clear()

    def seg2(self):
        self.sync(self.end(2))

    def seg3(self):
        self.sync(self.end(3))

    def seg4(self):
        self.sync(self.end(4))

    def seg5(self):
        self.sync(self.end(5))

    def seg6(self):
        self.sync(self.end(6))

    def seg7(self):
        self.sync(self.end(len(NARRATION)))

    # SEGMENTS-END


if __name__ == "__main__":
    main(__file__, "UtSeriesEp04", NARRATION)
