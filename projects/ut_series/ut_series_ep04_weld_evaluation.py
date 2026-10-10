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
                        knob, wedge_probe, WeldSection, small_scan)
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
    width = max(width, t.width + 1.15)                       # the box always holds its text
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
        fs = small_scan([5.0, 2.5], [(0, 1.0), (55, 0.9)], width=3.0, height=1.7, t_max=110.0, ticks=(0, 50, 100),
                        x_caption="", y_caption="")
        mis = tag_line("read as a root echo", "alert-triangle", ALERT_C, width=3.3).move_to([5.0, 1.0, 0])
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
        fs2 = small_scan([5.0, 2.5], [(0, 1.0), (50, 1.4)], width=3.0, height=1.7, t_max=110.0, ticks=(0, 50, 100),
                         x_caption="", y_caption="")
        good = tag_line("clear echo", "check", OK_C, width=3.0).move_to([5.0, 1.0, 0])
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
                ticks.add(Line([x, TOP - T, 0], [x, TOP - T - 0.3, 0], color=INK, stroke_width=4))
                tags.add(label(name, FS_TAG, INK, weight=BOLD).move_to([x, TOP - T - 0.62, 0]))
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

    # ---------------- Segment 2: the recording level on the DAC curve (§8.2) ----------------
    def seg2(self):
        c = lambda phrase, nth=1: self.cue(2, phrase, nth)
        S = self.start(2)
        H = lambda s: 3.0 * np.exp(-s / 45.0)                    # the DAC curve: identical reflectors fall with the path
        scan = AScan([(0, 1.8)], width=8.2, height=3.8, t_min=-6.0, t_max=110.0, ticks=(0, 25, 50, 75, 100), sigma=0.9,
                     x_caption="Sound path (mm)", y_caption="Echo amplitude")
        scan.shift(np.array([-2.0, 0.25, 0.0]) - scan.frame.get_center())
        shown = {"echoes": [(14, 0.6), (27, 1.1), (41, 0.35), (57, 0.8), (72, 0.45), (90, 0.9)]}
        scan.trace.add_updater(lambda m: (setattr(scan, "peaks", [(0, 1.8)] + shown["echoes"]), scan.update_trace(scan.t_max)))
        CX = 4.65                                                # centre of the right-hand column

        def curve(f, color, dashed=False, s0=3.0, s1=100.0, width=6):
            vm = VMobject(color=color, stroke_width=width)
            vm.set_points_smoothly([[scan.x_of(s), scan.y_base() + f(s), 0] for s in np.linspace(s0, s1, 120)])
            return DashedVMobject(vm, num_dashes=46, dashed_ratio=0.55) if dashed else vm

        # ---- not every signal is recorded ----
        self.play(FadeIn(scan), run_time=0.5)
        self.add(scan.trace)
        not_all = tag_line("not every signal is recorded", "x", ALERT_C, width=3.9).move_to([CX, 2.7, 0])
        self.sync(c("كُلُّ"))
        self.play(FadeIn(not_all, shift=UP * 0.1), run_time=0.4)
        # ---- the DAC curve: peaks of identical reflectors at different depths, joined ----
        self.sync(c("نَعْتَمِدُ") - 0.1)
        shown["echoes"] = []
        self.play(FadeOut(not_all), run_time=0.4)
        cal = [14.0, 45.0, 80.0]
        dots = VGroup()
        for s_, cue_word in zip(cal, ("قِمَمَ", "عَاكِسَاتٍ", "أَعْمَاقٍ")):
            self.sync(c(cue_word))
            shown["echoes"].append((s_, H(s_)))
            d_ = Dot([scan.x_of(s_), scan.y_base() + H(s_), 0], radius=0.09, color=ACCENT_3)
            dots.add(d_)
            self.play(GrowFromCenter(d_), run_time=0.3)
        dac = curve(H, ACCENT_3)
        self.sync(c("مُخْتَلِفَةٍ"))
        self.play(Create(dac, run_time=1.2, rate_func=linear))
        dac_lab = label("DAC curve", FS_NOTE, ACCENT_3, weight=BOLD).move_to([CX, 3.15, 0])
        self.sync(c("دِي", 1))
        self.play(FadeIn(dac_lab, shift=UP * 0.1), run_time=0.4)
        why1 = tag_line("the beam spreads", "arrows-exchange", INK, width=3.7, size=FS_TAG).move_to([CX, 2.2, 0])
        why2 = tag_line("the wave is attenuated", "wind", INK, width=3.9, size=FS_TAG).move_to([CX, 1.5, 0])
        self.sync(c("الحُزْمَةَ"))
        self.play(FadeIn(why1), run_time=0.4)
        self.sync(c("وَالمَوْجَةَ"))
        self.play(FadeIn(why2), run_time=0.4)
        # ---- a recording level, relative to the curve ----
        self.sync(c("وَيُحَدِّدُ", 1) - 0.1)
        self.play(FadeOut(why1), FadeOut(why2), run_time=0.4)
        rec = curve(lambda s: H(s) * D.ILLUSTRATIVE_RECORD_PCT_DAC / 100, ACCENT_2, dashed=True, width=5)
        rec_lab = label("Recording level", FS_TAG + 2, ACCENT_2, weight=BOLD).move_to([CX, 2.35, 0])
        note = VGroup(label("Illustrative levels", FS_TAG, ACCENT_1, weight=BOLD), label("(not code values)", FS_TAG - 4, GREY_INK))
        note.arrange(DOWN, buff=0.05).move_to([CX, 1.15, 0])
        self.sync(c("تَسْجِيلٍ"))
        self.play(Create(rec, run_time=1.0, rate_func=linear), FadeIn(rec_lab, shift=UP * 0.1))
        self.play(FadeIn(note), run_time=0.3)
        # an echo under the line is ignored; an echo above it is investigated and recorded
        s_lo, s_fl = 30.0, 60.0
        lo_h = H(s_lo) * D.ILLUSTRATIVE_ECHO_LOW_PCT_DAC / 100
        fl_h = H(s_fl) * D.AMP_PCT_DAC / 100
        ign = chip("Ignored", "x", GREY_INK, 2.5).move_to([CX, 0.45, 0])
        self.sync(c("صَدًى", 1) - 0.2)
        shown["echoes"].append((s_lo, lo_h))
        lo_dot = Dot([scan.x_of(s_lo), scan.y_base() + lo_h, 0], radius=0.08, color=GREY_INK)
        self.play(GrowFromCenter(lo_dot), run_time=0.3)
        self.sync(c("نُهْمِلُهُ") - 0.2)
        self.play(FadeIn(ign, shift=UP * 0.1), run_time=0.4)
        self.sync(c("وَصَدًى") - 0.1)
        shown["echoes"].append((s_fl, fl_h))
        fl_dot = Dot([scan.x_of(s_fl), scan.y_base() + fl_h, 0], radius=0.1, color=ACCENT_4)
        self.play(GrowFromCenter(fl_dot), run_time=0.3)
        head = chip("Investigate & record", "search", ACCENT_3, 3.4).move_to([CX, -0.45, 0])
        rows = VGroup(tag_line("location", "map-pin", INK, width=3.2, size=FS_TAG),
                      tag_line("type", "search", INK, width=3.2, size=FS_TAG),
                      tag_line("length", "ruler", INK, width=3.2, size=FS_TAG),
                      tag_line("amplitude vs the curve", "chart-bar", INK, width=3.7, size=FS_TAG))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([CX, -2.15, 0]).align_to(head, LEFT)
        self.sync(c("نَتَحَرَّى"))
        self.play(FadeIn(head, shift=UP * 0.1), run_time=0.4)
        for r_, w_ in zip(rows, ("مَوْقِعَهُ", "وَنَوْعَهُ", "وَطُولَهُ", "وَسَعَتَهُ")):
            self.sync(c(w_))
            self.play(FadeIn(r_, shift=RIGHT * 0.15), run_time=0.35)
        # ---- a higher level for evaluation or rejection, set by the code ----
        self.sync(c("وَيُحَدِّدُ", 2) - 0.1)
        ev = curve(lambda s: H(s) * D.ILLUSTRATIVE_EVAL_PCT_DAC / 100, ACCENT_4, dashed=True, width=5)
        ev_lab = label("Evaluation level", FS_TAG + 2, ACCENT_4, weight=BOLD).move_to([CX, 1.75, 0])
        self.sync(c("مُسْتَوًى"))
        self.play(Create(ev, run_time=1.0, rate_func=linear), FadeIn(ev_lab, shift=UP * 0.1))
        self.sync(c("لِلتَّقْيِيمِ"))
        self.play(Indicate(fl_dot, color=ACCENT_4, scale_factor=1.6), run_time=0.6)
        per = tag_line("the percentages differ from code to code", "arrows-exchange", INK, width=7.2, size=FS_TAG)
        per.move_to([-2.0, -2.9, 0])
        self.sync(c("وَالنِّسَبُ"))
        self.play(FadeIn(per, shift=UP * 0.1), run_time=0.4)
        self.sync(c("تَخْتَلِفُ"))
        self.play(rec.animate(run_time=0.5).shift(UP * 0.18), ev.animate(run_time=0.5).shift(DOWN * 0.12))
        self.play(rec.animate(run_time=0.5).shift(DOWN * 0.1), ev.animate(run_time=0.5).shift(UP * 0.1))
        self.sync(self.end(2))
        scan.trace.clear_updaters()
        self.clear()

    # ---------------- Segment 3: sizing the length by the 6 dB drop (§8.4.2.1) ----------------
    def seg3(self):
        c = lambda phrase, nth=1: self.cue(3, phrase, nth)
        S = self.start(3)
        MM, BW = 0.17, 8.0                                       # units per mm on the ruler; the beam width on the weld, mm
        FA, FB = D.POS_6DB_1, D.POS_6DB_2                        # the flaw's two ends as the 6 dB marks will find them
        X = lambda mm: -5.9 + MM * (mm - 100.0)
        BAND_Y = 1.5

        def amp(pos):
            ov = max(0.0, min(pos + BW / 2, FB) - max(pos - BW / 2, FA))
            return ov / BW                                       # the share of the beam that is on the flaw

        pos = ValueTracker(104.0)
        vis = ValueTracker(0.0)
        plate = Rectangle(width=10.0, height=3.4, color=INK, stroke_width=4).set_fill(PANEL_FILL, 1).move_to([-1.6, 1.5, 0])
        band = Rectangle(width=10.0, height=1.0, color=GREY_INK, stroke_width=2).set_fill(ACCENT_2, 0.16).move_to([-1.6, BAND_Y, 0])
        wlab = label("weld", FS_TAG, INK, weight=BOLD).move_to([2.7, 2.85, 0])
        flaw = Rectangle(width=X(FB) - X(FA), height=0.4, color=ACCENT_4, stroke_width=3).set_fill(ACCENT_4, 0.8)
        flaw.move_to([(X(FA) + X(FB)) / 2, BAND_Y, 0])
        ruler = Line([X(100), -0.75, 0], [X(150), -0.75, 0], color=INK, stroke_width=3)
        rticks = VGroup(*[Line([X(m), -0.75, 0], [X(m), -0.9, 0], color=INK, stroke_width=3) for m in range(100, 151, 10)])
        rlabs = VGroup(*[label(str(m), FS_TAG - 4, GREY_INK).move_to([X(m), -1.15, 0]) for m in range(100, 151, 10)])
        runit = label("mm", FS_TAG - 4, GREY_INK).move_to([X(150) + 0.5, -1.15, 0])

        probe = VGroup(RoundedRectangle(width=0.9, height=0.6, corner_radius=0.08, color=ACCENT_1, stroke_width=4).set_fill(BG, 1),
                       Polygon([-0.2, 0.3, 0], [0.2, 0.3, 0], [0, 0.55, 0], color=ACCENT_1, stroke_width=3).set_fill(ACCENT_1, 0.5))
        probe.add_updater(lambda m: m.move_to([X(pos.get_value()), 0.4, 0]))
        cone = Polygon([0, 0, 0], [1, 0, 0], [1, 1, 0], color=ACCENT_1, stroke_width=0)

        def cone_update(m):
            x0 = X(pos.get_value())
            half = BW * MM / 2
            m.become(Polygon([x0 - 0.17, 0.95, 0], [x0 + 0.17, 0.95, 0], [x0 + half, BAND_Y, 0], [x0 - half, BAND_Y, 0],
                             color=ACCENT_1, stroke_width=0).set_fill(ACCENT_1, 0.32 * vis.get_value()))
        cone.add_updater(cone_update)
        foot = Rectangle(width=BW * MM, height=0.5, color=ACCENT_1, stroke_width=3)
        foot.add_updater(lambda m: m.become(Rectangle(width=BW * MM, height=0.5, color=ACCENT_1, stroke_width=3)
                                            .set_fill(ACCENT_1, 0.25 * vis.get_value()).set_stroke(opacity=vis.get_value())
                                            .move_to([X(pos.get_value()), BAND_Y, 0])))
        axis_line = DashedLine([0, 0.95, 0], [0, 2.3, 0], color=ACCENT_1, stroke_width=3)
        axis_line.add_updater(lambda m: m.put_start_and_end_on([X(pos.get_value()), 0.95, 0], [X(pos.get_value()), 2.3, 0]))
        axis_line.set_stroke(opacity=0)

        MX, MY, MH = 5.95, 1.7, 2.8
        meter = Rectangle(width=0.7, height=MH, color=INK, stroke_width=3).set_fill(PANEL_FILL, 1).move_to([MX, MY, 0])
        fill = Rectangle(width=0.62, height=0.02, color=ACCENT_2, stroke_width=0).set_fill(ACCENT_2, 1)
        fill.add_updater(lambda m: m.become(Rectangle(width=0.62, height=max(amp(pos.get_value()) * (MH - 0.1), 0.02),
                                                      color=ACCENT_2, stroke_width=0).set_fill(ACCENT_2, 1)
                                            .move_to([MX, MY - MH / 2 + 0.05 + max(amp(pos.get_value()) * (MH - 0.1), 0.02) / 2, 0])))
        half_y = MY - MH / 2 + 0.05 + 0.5 * (MH - 0.1)
        half_line = DashedLine([MX - 0.35, half_y, 0], [MX + 0.35, half_y, 0], color=ACCENT_4, stroke_width=4)
        mcap = label("Echo height", FS_TAG - 2, INK, weight=BOLD).move_to([MX, 0.05, 0])
        full_tag = label("set to full", FS_TAG - 2, ACCENT_2, weight=BOLD).move_to([MX, 3.5, 0])
        drop_tag = label("6 dB drop", FS_TAG, ACCENT_4, weight=BOLD).move_to([MX - 1.6, half_y, 0])

        # ---- the probe finds the maximum, then moves along the flaw until the echo has halved ----
        self.play(FadeIn(plate), FadeIn(band), FadeIn(wlab), FadeIn(flaw), Create(ruler), FadeIn(rticks), FadeIn(rlabs),
                  FadeIn(runit), FadeIn(meter), FadeIn(mcap), run_time=0.8)
        self.add(fill)
        self.sync(c("نُحَرِّكُ"))
        self.add(cone, foot, probe)
        self.play(vis.animate(run_time=0.4).set_value(1.0))
        self.play(pos.animate(run_time=1.9, rate_func=smooth).set_value(123.5))
        self.sync(c("أَقْصَاهُ") + 0.2)
        self.play(FadeIn(full_tag, shift=DOWN * 0.1), run_time=0.4)
        self.sync(c("نُحَرِّكُهُ"))
        self.play(FadeOut(full_tag), run_time=0.3)
        self.play(pos.animate(run_time=3.2, rate_func=linear).set_value(float(FA)))
        self.sync(c("سِتَّةَ"))
        self.play(Create(half_line), FadeIn(drop_tag, shift=RIGHT * 0.1), run_time=0.5)
        # why one half: the beam axis is on the edge, half the beam on the flaw
        self.sync(c("مِحْوَرُ"))
        self.add(axis_line)
        self.play(axis_line.animate(run_time=0.4).set_stroke(opacity=1))
        out_t = label("outside", FS_TAG, GREY_INK, weight=BOLD).move_to([X(FA) - 1.0, 2.55, 0])
        in_t = label("on the flaw", FS_TAG, ACCENT_4, weight=BOLD).move_to([X(FA) + 1.1, 2.55, 0])
        self.sync(c("نِصْفُهَا") - 0.1)
        self.play(FadeIn(in_t, shift=DOWN * 0.1), run_time=0.4)
        self.sync(c("وَنِصْفُهَا") - 0.1)
        self.play(FadeIn(out_t, shift=DOWN * 0.1), run_time=0.4)
        # mark the position, then repeat towards the other end
        self.sync(c("نُعَلِّمُ") - 0.1)
        self.play(FadeOut(out_t), FadeOut(in_t), FadeOut(axis_line), run_time=0.4)
        self.remove(axis_line)

        def mark(mm):
            return Line([X(mm), -0.5, 0], [X(mm), -0.95, 0], color=ACCENT_3, stroke_width=7)
        m1 = mark(FA)
        self.sync(c("مَوْضِعَ"))
        self.play(Create(m1), run_time=0.4)
        self.sync(c("وَنُكَرِّرُ"))
        self.play(pos.animate(run_time=2.0, rate_func=smooth).set_value(float(FB)))
        m2 = mark(FB)
        self.sync(c("وَالمَسَافَةُ") - 0.2)
        self.play(Create(m2), run_time=0.4)
        len_arrow = DoubleArrow([X(FA), -1.7, 0], [X(FB), -1.7, 0], buff=0, color=ACCENT_3, stroke_width=4, tip_length=0.16)
        len_lab = label("length", FS_TAG, ACCENT_3, weight=BOLD).move_to([(X(FA) + X(FB)) / 2, -2.1, 0])
        self.sync(c("العَلَامَتَيْنِ"))
        self.play(GrowArrow(len_arrow), run_time=0.5)
        self.sync(c("طُولُ"))
        self.play(FadeIn(len_lab, shift=UP * 0.1), run_time=0.4)
        # ---- the worked example (the only one of the episode) ----
        l1 = label(f"{D.POS_6DB_1:.0f} mm", FS_TAG, ACCENT_3, weight=BOLD).move_to([X(FA) - 0.95, -1.7, 0])
        l2 = label(f"{D.POS_6DB_2:.0f} mm", FS_TAG, ACCENT_3, weight=BOLD).move_to([X(FB) + 0.95, -1.7, 0])
        self.sync(c("عَشَرَ", 1) + 0.1)
        self.play(FadeIn(l1, shift=RIGHT * 0.1), run_time=0.4)
        self.sync(c("وَثَلَاثِينَ", 1) + 0.1)
        self.play(FadeIn(l2, shift=LEFT * 0.1), run_time=0.4)
        n135 = label(f"{D.POS_6DB_2:.0f}", FS_EQUATION, ACCENT_3, weight=BOLD)
        minus = label("−", FS_EQUATION, INK, weight=BOLD)
        n112 = label(f"{D.POS_6DB_1:.0f}", FS_EQUATION, ACCENT_3, weight=BOLD)
        eq = label("=", FS_EQUATION, INK, weight=BOLD)
        res = label(f"{D.FLAW_LENGTH:.0f} mm", FS_EQUATION, ACCENT_4, weight=BOLD)
        calc = VGroup(n135, minus, n112, eq, res).arrange(RIGHT, buff=0.32).move_to([-1.65, -3.0, 0])
        self.sync(c("مِئَةٌ", 1))
        self.play(FadeIn(n135, shift=UP * 0.15), run_time=0.4)
        self.sync(c("نَاقِصُ"))
        self.play(FadeIn(minus), run_time=0.3)
        self.sync(c("مِئَةٍ", 3))
        self.play(FadeIn(n112, shift=UP * 0.15), run_time=0.4)
        self.sync(c("ثَلَاثَةٌ"))
        self.play(FadeIn(eq), FadeIn(res, shift=UP * 0.15), run_time=0.5)
        # ---- what the method is for ----
        self.sync(c("وَهٰذِهِ") - 0.1)
        self.play(FadeOut(calc), run_time=0.4)
        len_tag = tag_line("gives the length, not the height", "ruler", ACCENT_3, width=6.2).move_to([-1.65, -3.0, 0])
        self.sync(c("لِلطُّولِ"))
        self.play(FadeIn(len_tag, shift=UP * 0.1), run_time=0.4)
        beam_b = DoubleArrow([X(123.5) - BW * MM / 2, 2.4, 0], [X(123.5) + BW * MM / 2, 2.4, 0], buff=0, color=ACCENT_1,
                             stroke_width=3, tip_length=0.12)
        beam_l = label("beam width", FS_TAG - 4, ACCENT_1, weight=BOLD).next_to(beam_b, UP, 0.06)
        self.sync(c("وَتَصْلُحُ"))
        self.play(FadeOut(VGroup(l1, l2, len_arrow, len_lab, m1, m2, half_line, drop_tag)), pos.animate(run_time=0.9).set_value(123.5), run_time=0.9)
        self.sync(c("الأَكْبَرِ"))
        self.play(GrowArrow(beam_b), FadeIn(beam_l), run_time=0.5)
        ok_t = icon("check", OK_C, 0.5).move_to([X(FB) + 1.2, 2.45, 0])
        self.play(FadeIn(ok_t, scale=0.6), run_time=0.3)
        self.sync(c("وَالأَصْغَرُ") - 0.1)
        small = Dot([X(123.5), BAND_Y, 0], radius=0.09, color=ACCENT_4)
        self.play(FadeOut(len_tag), FadeOut(ok_t), ReplacementTransform(flaw, small), run_time=0.6)
        sm_tag = tag_line("smaller than the beam: compare the echo with", "alert-triangle", ALERT_C, width=6.9).move_to([-1.65, -1.9, 0])
        c_dac = chip("DAC curve", "chart-line", ACCENT_3, 2.9).move_to([-3.4, -3.0, 0])
        c_dgs = chip("DGS diagram", "chart-bar", ACCENT_1, 3.3).move_to([0.2, -3.0, 0])
        self.sync(c("نُقَدِّرُهُ"))
        self.play(FadeIn(sm_tag, shift=UP * 0.1), run_time=0.4)
        self.sync(c("بِمُنْحَنَى"))
        self.play(FadeIn(c_dac, shift=UP * 0.1), run_time=0.4)
        self.sync(c("بِمُخَطَّطِ"))
        self.play(FadeIn(c_dgs, shift=UP * 0.1), run_time=0.4)
        self.sync(self.end(3))
        for m_ in (probe, cone, foot, fill):
            m_.clear_updaters()
        self.clear()

    # ---------------- Segment 4: telling the flaw type from the echo (§8.5) ----------------
    def seg4(self):
        c = lambda phrase, nth=1: self.cue(4, phrase, nth)
        S = self.start(4)

        def mk_probe(x, y, ang, size=1.0, beam=1.3, color=ACCENT_1):
            """A plan-view angle probe centred on (x, y), pointing up when ang = 0 (turned counter-clockwise by ang)."""
            body = RoundedRectangle(width=0.9 * size, height=0.55 * size, corner_radius=0.08, color=color, stroke_width=4).set_fill(BG, 1)
            nose = Polygon([-0.2 * size, 0.275 * size, 0], [0.2 * size, 0.275 * size, 0], [0, 0.5 * size, 0],
                           color=color, stroke_width=3).set_fill(color, 0.5)
            bm = DashedLine([0, 0.5 * size, 0], [0, 0.5 * size + beam, 0], color=color, stroke_width=2)
            g = VGroup(body, nose, bm)
            g.rotate(ang, about_point=ORIGIN)
            return g.shift(np.array([x, y, 0.0]))

        # ---- the four probe movements, in plan view ----
        FX, FY = -2.5, 1.0                                       # the flaw, in the weld band
        plate = Rectangle(width=7.8, height=4.2, color=INK, stroke_width=4).set_fill(PANEL_FILL, 1).move_to([-2.5, 0.2, 0])
        band = Rectangle(width=7.8, height=0.8, color=GREY_INK, stroke_width=2).set_fill(ACCENT_2, 0.16).move_to([-2.5, FY, 0])
        wlab = label("weld", FS_TAG, INK, weight=BOLD).move_to([-5.8, 1.9, 0])
        flaw = Dot([FX, FY, 0], radius=0.13, color=ACCENT_4)
        R_ORB = 1.8
        glyph = [DoubleArrow([0, -0.4, 0], [0, 0.4, 0], buff=0, color=ACCENT_1, stroke_width=4, tip_length=0.15),
                 DoubleArrow([-0.4, 0, 0], [0.4, 0, 0], buff=0, color=ACCENT_1, stroke_width=4, tip_length=0.15),
                 Arc(radius=0.33, start_angle=0.5, angle=4.6, color=ACCENT_1, stroke_width=4).add_tip(tip_length=0.15),
                 VGroup(Arc(radius=0.5, start_angle=PI * 0.2, angle=PI * 0.6, arc_center=[0, -0.45, 0], color=ACCENT_1,
                            stroke_width=4).add_tip(tip_length=0.15), Dot([0, 0.05, 0], radius=0.07, color=ACCENT_4))]
        names = ("Transverse", "Lateral", "Rotational", "Orbital")
        rows = VGroup()
        for k, (g_, nm) in enumerate(zip(glyph, names)):
            g_.move_to([3.2, 2.2 - 1.3 * k, 0])
            t_ = label(nm, FS_NOTE, INK, weight=BOLD).next_to(g_, RIGHT, 0.35)
            rows.add(VGroup(g_, t_))
        P0 = np.array([FX, -0.75, 0.0])
        probe = mk_probe(*P0[:2], 0.0)
        self.play(FadeIn(plate), FadeIn(band), FadeIn(wlab), FadeIn(flaw), run_time=0.7)
        self.sync(c("بِأَرْبَعِ"))
        self.play(FadeIn(probe), run_time=0.4)
        self.sync(c("إِلَى"))
        self.play(FadeIn(rows[0], shift=LEFT * 0.15), run_time=0.4)
        self.play(UpdateFromAlphaFunc(probe, lambda m, a: m.become(mk_probe(P0[0], P0[1] + 0.6 * np.sin(a * TAU), 0.0))), run_time=1.6)
        self.sync(c("وَجَانِبِيًّا"))
        self.play(FadeIn(rows[1], shift=LEFT * 0.15), run_time=0.4)
        self.play(UpdateFromAlphaFunc(probe, lambda m, a: m.become(mk_probe(P0[0] + 1.0 * np.sin(a * TAU), P0[1], 0.0))), run_time=1.6)
        self.sync(c("وَدَوَرَانًا"))
        self.play(FadeIn(rows[2], shift=LEFT * 0.15), run_time=0.4)
        self.play(UpdateFromAlphaFunc(probe, lambda m, a: m.become(mk_probe(P0[0], P0[1], 0.6 * np.sin(a * TAU)))), run_time=1.6)
        self.sync(c("وَحَرَكَةً"))
        self.play(FadeIn(rows[3], shift=LEFT * 0.15), run_time=0.4)

        def orbit(m, a):
            th = 0.75 * np.sin(a * TAU)
            m.become(mk_probe(FX + R_ORB * np.sin(th), FY - R_ORB * np.cos(th), th, beam=R_ORB - 0.55))
        self.play(UpdateFromAlphaFunc(probe, orbit), run_time=1.8)

        # ---- four flaws: how each echo behaves while the probe moves ----
        self.sync(c("المَسَامَةُ") - 0.4)
        self.clear(run_time=0.5)
        PW, PH = 6.5, 3.3
        centers = [(-3.6, 1.75), (3.6, 1.75), (-3.6, -1.7), (3.6, -1.7)]
        titles = ("Isolated pore", "Porosity", "Slag inclusion", "Planar flaw")
        cap_cols = (INK, INK, INK, ALERT_C)

        def frame_of(k):
            px, py = centers[k]
            fr = RoundedRectangle(width=PW, height=PH, corner_radius=0.15, color=INK, stroke_width=3).set_fill(BG, 1).move_to([px, py, 0])
            tt = label(titles[k], FS_TAG, INK, weight=BOLD).move_to([px - PW / 2 + 0.2 + 0.0, py + PH / 2 - 0.3, 0])
            tt.align_to(fr, LEFT).shift(RIGHT * 0.2)
            return fr, tt

        def scan_of(k, peaks, sigma=1.0):
            px, py = centers[k]
            sc = small_scan([px + 1.6, py - 0.1], peaks, width=2.9, height=1.6, t_max=110.0, ticks=(0,), sigma=sigma,
                            x_caption="", y_caption="")
            return sc

        def note_of(k, text, color=INK, icon_name=None):
            px, py = centers[k]
            t_ = label(text, FS_TAG - 2, color, weight=BOLD)
            return t_.move_to([px, py - PH / 2 + 0.32, 0])

        def probe_updater(k, ph, fn):
            """The panel's probe follows tracker `ph` through fn(ph) -> (x, y, angle)."""
            g = mk_probe(*fn(ph.get_value()), size=0.55, beam=0.5)
            return g

        # (a) the isolated pore: a poor reflector, the same small echo from every side
        F = [np.array([centers[k][0] - 1.6, centers[k][1] + 0.2, 0.0]) for k in range(4)]
        R_P = 0.8
        ph_a = ValueTracker(0.0)
        fr_a, tt_a = frame_of(0)
        pore = Circle(radius=0.11, color=ACCENT_4, stroke_width=3).set_fill(ACCENT_4, 0.9).move_to(F[0])
        sc_a = scan_of(0, [(0, 0.75), (50, 0.28)])
        sc_a.trace.add_updater(lambda m: None)
        orb = lambda k_, ph: (F[k_][0] + R_P * np.sin(ph), F[k_][1] - R_P * np.cos(ph), ph)
        pr_a = mk_probe(*orb(0, 0.0), size=0.55, beam=0.4)
        n_a = note_of(0, "small, the same from every side")
        self.sync(c("المَسَامَةُ") - 0.1)
        self.play(FadeIn(fr_a), FadeIn(tt_a), FadeIn(pore), FadeIn(sc_a), FadeIn(sc_a.trace), FadeIn(pr_a), run_time=0.7)
        self.sync(c("كُرَوِيَّةٌ"))
        self.play(Indicate(pore, color=ACCENT_4, scale_factor=1.8), run_time=0.7)
        self.sync(c("ضَعِيفٌ"))
        self.play(FadeIn(n_a, shift=UP * 0.1), run_time=0.4)
        self.sync(c("يَتَغَيَّرُ", 1) - 0.3)
        self.play(UpdateFromAlphaFunc(pr_a, lambda m, a: m.become(mk_probe(*orb(0, 0.8 * np.sin(a * TAU)), size=0.55, beam=0.4))), run_time=3.0)

        # (b) porosity: many tiny echoes that rise and fall quickly and smoothly
        ph_b = ValueTracker(0.0)
        fr_b, tt_b = frame_of(1)
        pores = VGroup(*[Circle(radius=0.055, color=ACCENT_4, stroke_width=2).set_fill(ACCENT_4, 0.9)
                         .move_to(np.array([centers[1][0] - 1.6 + dx, centers[1][1] + 0.2 + dy, 0.0]))
                         for dx, dy in ((-0.45, 0.1), (-0.2, -0.12), (0.05, 0.14), (0.28, -0.05), (0.5, 0.1), (-0.05, -0.2))])
        sc_b = scan_of(1, [(0, 0.75)] + [(s_, 0.2) for s_ in (40, 46, 52, 58, 64, 70)], sigma=0.9)
        sc_b.trace.clear_updaters()
        sc_b.trace.add_updater(lambda m: (setattr(sc_b, "peaks", [(0, 0.75)] + [
            (s_, 0.06 + 0.2 * (0.5 + 0.5 * np.sin(5.0 * ph_b.get_value() + 1.3 * i))) for i, s_ in enumerate((40, 46, 52, 58, 64, 70))]),
                                          sc_b.update_trace(sc_b.t_max)))
        pr_b = mk_probe(centers[1][0] - 1.6, centers[1][1] + 0.2 - R_P, 0.0, size=0.55, beam=0.4)
        n_b = note_of(1, "tiny echoes, rising and falling")
        self.sync(c("وَالمَسَامِيَّةُ") - 0.2)
        self.play(FadeIn(fr_b), FadeIn(tt_b), FadeIn(pores), FadeIn(sc_b), FadeIn(sc_b.trace), FadeIn(pr_b), run_time=0.7)
        self.sync(c("كَثِيرَةٌ"))
        self.play(FadeIn(n_b, shift=UP * 0.1), run_time=0.4)
        self.sync(c("تَرْتَفِعُ"))
        self.play(UpdateFromAlphaFunc(pr_b, lambda m, a: (ph_b.set_value(1.6 * np.sin(a * TAU)),
                                                         m.become(mk_probe(centers[1][0] - 1.6 + 0.55 * np.sin(a * TAU), centers[1][1] + 0.2 - R_P, 0.0,
                                                                           size=0.55, beam=0.4)))), run_time=3.4)
        sc_b.trace.clear_updaters()

        # (c) slag: a tall, many-peaked "pine tree" echo that stays when the probe goes round
        fr_c, tt_c = frame_of(2)
        blob_pts = [(-0.28, -0.05), (-0.1, 0.2), (0.15, 0.17), (0.3, -0.02), (0.12, -0.2), (-0.15, -0.16)]
        blob = Polygon(*[np.array([F[2][0] + x, F[2][1] + y, 0.0]) for x, y in blob_pts], color=ACCENT_4,
                       stroke_width=3).set_fill(ACCENT_4, 0.85)
        pine = [(0, 0.75), (44, 0.35), (47, 0.62), (50, 0.45), (53, 0.8), (56, 0.52), (59, 0.68)]
        sc_c = scan_of(2, [(0, 0.75)], sigma=1.1)
        sc_c.trace.clear_updaters()
        shown_c = {"peaks": [(0, 0.75)]}
        sc_c.trace.add_updater(lambda m: (setattr(sc_c, "peaks", shown_c["peaks"]), sc_c.update_trace(sc_c.t_max)))
        pr_c = mk_probe(*orb(2, 0.0), size=0.55, beam=0.4)
        n_c = note_of(2, "tall, many peaks, steady all round")
        self.sync(c("وَالخَبَثُ") - 0.2)
        self.play(FadeIn(fr_c), FadeIn(tt_c), FadeIn(blob), FadeIn(sc_c), FadeIn(sc_c.trace), FadeIn(pr_c), run_time=0.7)
        self.sync(c("عَالِيًا"))
        shown_c["peaks"] = [(0, 0.75), (47, 0.62), (53, 0.8)]
        self.wait(0.5)
        self.sync(c("مُتَعَدِّدَ"))
        shown_c["peaks"] = pine
        self.play(FadeIn(n_c, shift=UP * 0.1), run_time=0.4)
        self.sync(c("يَتَغَيَّرُ", 2) - 0.2)
        self.play(UpdateFromAlphaFunc(pr_c, lambda m, a: m.become(mk_probe(*orb(2, 0.8 * np.sin(a * TAU)), size=0.55, beam=0.4))), run_time=3.0)
        sc_c.trace.clear_updaters()

        # (d) a planar flaw: strong square on, much weaker from any other side
        ph_d = ValueTracker(0.0)
        fr_d, tt_d = frame_of(3)
        bar = Rectangle(width=1.0, height=0.09, color=ACCENT_4, stroke_width=2).set_fill(ACCENT_4, 0.9).move_to(F[3])
        sc_d = scan_of(3, [(0, 0.75), (50, 0.8)], sigma=1.0)
        sc_d.trace.clear_updaters()
        shown_d = {"on": False}
        sc_d.trace.add_updater(lambda m: (setattr(sc_d, "peaks", [(0, 0.75)] + ([(50, 0.8 * np.exp(-(ph_d.get_value() / 0.3) ** 2))] if shown_d["on"] else [])),
                                          sc_d.update_trace(sc_d.t_max)))
        pr_d = mk_probe(*orb(3, 0.0), size=0.55, beam=0.4)
        n_d = note_of(3, "strong square on, then drops", ALERT_C)
        self.sync(c("وَالعَيْبُ") - 0.2)
        self.play(FadeIn(fr_d), FadeIn(tt_d), FadeIn(bar), FadeIn(sc_d), FadeIn(sc_d.trace), FadeIn(pr_d), run_time=0.7)
        self.sync(c("قَوِيٌّ"))
        shown_d["on"] = True
        self.play(Indicate(sc_d.frame, color=ACCENT_2, scale_factor=1.03), run_time=0.6)
        self.sync(c("وَيَهْبِطُ"))
        self.play(FadeIn(n_d, shift=UP * 0.1), run_time=0.4)
        self.play(UpdateFromAlphaFunc(pr_d, lambda m, a: (ph_d.set_value(0.9 * a),
                                                         m.become(mk_probe(*orb(3, 0.9 * a), size=0.55, beam=0.4)))), run_time=2.2)
        self.sync(c("الأَخْطَرُ"))
        self.play(Indicate(fr_d, color=ALERT_C, scale_factor=1.02), run_time=0.7)
        sc_d.trace.clear_updaters()

        # ---- the verdict joins the location with the behaviour ----
        self.sync(c("وَيَجْمَعُ") - 0.2)
        self.clear(run_time=0.5)
        wd = WeldSection(cx=-4.4, y_top=1.3, t=1.2, half_w=1.6)
        dot1 = Dot(wd.face_point(1, 0.8) + LEFT * 0.04, radius=0.08, color=ACCENT_4)
        dot2 = Dot([wd.cx, wd.y_top - 0.6, 0], radius=0.08, color=ACCENT_4)
        loc_t = label("Location", FS_NOTE, INK, weight=BOLD).move_to([-4.4, -0.75, 0])
        beh = small_scan([0.2, 0.5], [(0, 0.8), (50, 0.9), (62, 0.5)], width=3.0, height=1.8, t_max=110.0, ticks=(0,),
                         x_caption="", y_caption="")
        beh_t = label("Behaviour", FS_NOTE, INK, weight=BOLD).move_to([0.2, -0.8, 0])
        plus = label("+", FS_HEADING, INK, weight=BOLD).move_to([-2.1, 0.5, 0])
        eq = label("=", FS_HEADING, INK, weight=BOLD).move_to([2.35, 0.5, 0])
        ftype = chip("Flaw type", "search", ACCENT_3, 2.9).move_to([4.7, 0.5, 0])
        one = chip("one echo shape alone", "x", ALERT_C, 5.0).move_to([0.0, -2.3, 0])
        self.sync(c("المَوْقِعَ") - 0.1)
        self.play(FadeIn(wd), FadeIn(dot1), FadeIn(dot2), FadeIn(loc_t), run_time=0.6)
        self.sync(c("السُّلُوكِ") - 0.1)
        self.play(FadeIn(plus), FadeIn(beh), FadeIn(beh.trace), FadeIn(beh_t), run_time=0.6)
        self.play(FadeIn(eq), FadeIn(ftype, shift=LEFT * 0.15), run_time=0.5)
        self.sync(c("شَكْلَ") - 0.1)
        self.play(FadeIn(one, shift=UP * 0.1), run_time=0.5)
        self.sync(self.end(4))
        self.clear()

    # ---------------- Segment 5: the code decides; the report (§8.6, §8.7) ----------------
    def seg5(self):
        c = lambda phrase, nth=1: self.cue(5, phrase, nth)
        S = self.start(5)
        # ---- the inspector reports; the code decides ----
        insp = chip("Inspector: reports", "user", INK, 3.6).move_to([-4.3, 2.9, 0])
        no = icon("x", ALERT_C, 0.5).next_to(insp, RIGHT, 0.25)
        arrow1 = Arrow([-1.2, 2.9, 0], [0.1, 2.9, 0], buff=0, color=INK, stroke_width=4, tip_length=0.2)
        code = chip("The code decides", "scale", ACCENT_3, 3.6).move_to([2.4, 2.9, 0])
        sub = label("named in the contract", FS_TAG, GREY_INK).next_to(code, DOWN, 0.12)
        names = VGroup(chip("ASME VIII", "book", ACCENT_1, 3.1), chip("AWS D1.1", "book", ACCENT_1, 3.1),
                       chip("API 1104", "book", ACCENT_1, 3.1)).arrange(RIGHT, buff=0.35).move_to([0, 1.2, 0])
        self.sync(c("لَيْسَ"))
        self.play(FadeIn(insp, shift=RIGHT * 0.15), run_time=0.4)
        self.sync(c("لِلْفَاحِصِ"))
        self.play(FadeIn(no, scale=0.6), run_time=0.3)
        self.sync(c("بَلْ"))
        self.play(GrowArrow(arrow1), FadeIn(code, shift=LEFT * 0.15), FadeIn(sub), run_time=0.6)
        for k, w_ in enumerate(("إِيهْ", "دَبْلْيُو", "بِي")):
            self.sync(c(w_, 1 if w_ != "إِيهْ" else 1))
            self.play(FadeIn(names[k], shift=UP * 0.15), run_time=0.4)
        # ---- what the criteria rest on ----
        facts = VGroup(chip("Amplitude vs the reference", "chart-bar", INK, 4.0), chip("Flaw length", "ruler", INK, 3.0),
                       chip("Flaw type", "search", INK, 2.7)).arrange(RIGHT, buff=0.4).move_to([0, -0.4, 0])
        self.sync(c("سَعَةِ"))
        self.play(FadeIn(facts[0], shift=UP * 0.15), run_time=0.4)
        self.sync(c("طُولِ"))
        self.play(FadeIn(facts[1], shift=UP * 0.15), run_time=0.4)
        self.sync(c("وَنَوْعِهِ"))
        self.play(FadeIn(facts[2], shift=UP * 0.15), run_time=0.4)
        # ---- cracks, lack of fusion and lack of penetration are rejected whatever their length ----
        card = RoundedRectangle(width=11.4, height=1.9, corner_radius=0.2, color=ACCENT_4, stroke_width=4).set_fill(PANEL_FILL, 1)
        card.move_to([0, -2.5, 0])
        items = VGroup(tag_line("cracks", "alert-triangle", ALERT_C, width=3.2), tag_line("lack of fusion", "alert-triangle", ALERT_C, width=4.0),
                       tag_line("lack of penetration", "alert-triangle", ALERT_C, width=4.7)).arrange(RIGHT, buff=0.55)
        items.move_to(card.get_center() + UP * 0.35)
        stamp = label("Rejected, whatever the length", FS_NOTE, ALERT_C, weight=BOLD).move_to(card.get_center() + DOWN * 0.5)
        self.sync(c("يَرْفُضُ"))
        self.play(Create(card), run_time=0.5)
        self.sync(c("الشُّقُوقَ"))
        self.play(FadeIn(items[0], shift=UP * 0.1), run_time=0.35)
        self.sync(c("وَعَدَمَ", 1))
        self.play(FadeIn(items[1], shift=UP * 0.1), run_time=0.35)
        self.sync(c("وَعَدَمَ", 2))
        self.play(FadeIn(items[2], shift=UP * 0.1), run_time=0.35)
        self.sync(c("مَهْمَا"))
        self.play(FadeIn(stamp, scale=1.15), run_time=0.5)

        # ---- the report makes the test repeatable ----
        self.sync(c("وَالتَّقْرِيرُ") - 0.3)
        self.clear(run_time=0.5)
        FSZ = FS_TAG - 2
        MONO_W = Text("M" * 20, font=MONO, font_size=FSZ).width / 20          # width of one character
        kv = lambda k, v: f"{k:<18}: {v}"
        LINES = [("ULTRASONIC TEST REPORT   (illustrative)", BOLD),
                 (kv("Component / weld", f"butt weld, {D.PLATE_T:.0f} mm plate"), NORMAL),
                 (kv("Procedure / code", "as named in the contract"), NORMAL),
                 (kv("Instrument", "flaw detector"), NORMAL),
                 (kv("Probe", f"{D.PROBE_ANGLE:.0f} deg angle probe, {D.F_PROBE:.0f} MHz"), NORMAL),
                 (kv("Calibration", "V1 block, DAC curve, couplant"), NORMAL),
                 (kv("Scan areas", "both sides, half and full skip"), NORMAL)]
        rows = VGroup(*[Text(t, font=MONO, font_size=FSZ, weight=w) for t, w in LINES])
        COLS = (0, 6, 13, 22, 30, 38)
        head = [("No.", "Depth", "Surface", "Length", "Amp.", "Type"), ("", "(mm)", "(mm)", "(mm)", "(%DAC)", "")]
        data = (("1", f"{D.REPORT_DEPTH:.1f}", f"{D.REPORT_SURFACE_DIST:.1f}", f"{D.REPORT_LENGTH:.0f}", f"{D.AMP_PCT_DAC}", D.REPORT_TYPE),)

        def cell_row(vals, weight=NORMAL):
            cells = VGroup(*[Text(v, font=MONO, font_size=FSZ, weight=weight) if v else Rectangle(width=0.01, height=0.01, stroke_width=0, fill_opacity=0) for v in vals])
            for cell, col in zip(cells, COLS):
                cell.move_to(ORIGIN)
            return cells
        tbl_rows = [cell_row(head[0], BOLD), cell_row(head[1]), cell_row(data[0])]
        res_row = Text(kv("Result", D.REPORT_RESULT), font=MONO, font_size=FSZ, weight=BOLD)
        who_row = Text(kv("Inspector / date", "(name) / (date)"), font=MONO, font_size=FSZ)
        # stack the rows; the table rows are laid out on the character grid of the text rows
        stack = VGroup(*rows, *[VGroup(*r) for r in tbl_rows], res_row, who_row).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        left_x = stack.get_left()[0]
        for r in tbl_rows:
            for cell, col in zip(r, COLS):
                cell.move_to([left_x + col * MONO_W + cell.width / 2, r[0].get_center()[1], 0])
        paper = Rectangle(width=stack.width + 0.6, height=stack.height + 0.5, stroke_width=3, color=LINE_C).set_fill(BG, 1)
        doc = VGroup(paper, stack.move_to(paper))
        doc.scale_to_fit_height(5.6)
        if doc.width > 12.4:
            doc.scale_to_fit_width(12.4)
        doc.move_to([0, 0.05, 0])
        rows_all = list(rows) + [VGroup(*r) for r in tbl_rows] + [res_row, who_row]
        self.play(Create(paper), run_time=0.5)
        reveal = [("القِطْعَةَ", [0, 1]), ("وَالإِجْرَاءَ", [2]), ("وَالجِهَازَ", [3]), ("وَالمِجَسَّاتِ", [4]), ("وَالمُعَايَرَةَ", [5]),
                  ("وَمَنَاطِقَ", [6]), ("وَجَدْوَلَ", [7, 8, 9]), ("وَالنَّتِيجَةَ", [10]), ("وَاسْمَ", [11])]
        for word, idx in reveal:
            self.sync(c(word))
            self.play(*[FadeIn(rows_all[i], shift=RIGHT * 0.1) for i in idx], run_time=0.4)
        self.sync(c("وَهٰذَا"))
        data_cells = rows_all[9]
        boxes = VGroup()
        for word, k in (("عُمْقُهُ", 1), ("وَطُولُهُ", 3), ("وَسَعَتُهُ", 4)):
            self.sync(c(word))
            b_ = SurroundingRectangle(data_cells[k], color=ACCENT_4, buff=0.05, stroke_width=4)
            boxes.add(b_)
            self.play(Create(b_), run_time=0.4)
        self.sync(self.end(5))
        self.clear()

    # ---------------- Segment 6: a glimpse of PAUT and TOFD, and the series in one line (§9.1-9.2) ----------------
    def seg6(self):
        c = lambda phrase, nth=1: self.cue(6, phrase, nth)
        S = self.start(6)

        # ================= phased array =================
        TOPY, T = -0.6, 1.4
        wd = WeldSection(cx=-2.0, y_top=TOPY, t=T, half_w=4.6)           # the plate runs from x = -6.6 to 2.6
        EX, N, PITCH = -4.7, 8, 0.29
        el_x = [EX + (i - (N - 1) / 2) * PITCH for i in range(N)]
        block = Rectangle(width=N * PITCH + 0.2, height=0.42, color=ACCENT_1, stroke_width=3).set_fill(PANEL_FILL, 1)
        block.move_to([EX, TOPY + 0.21, 0])
        elems = VGroup(*[Rectangle(width=0.2, height=0.15, color=ACCENT_1, stroke_width=2).set_fill(ACCENT_1, 0.9)
                         .move_to([x, TOPY + 0.075, 0]) for x in el_x])
        array = VGroup(block, elems)
        paut_t = label("Phased array (PAUT)", FS_NOTE, ACCENT_1, weight=BOLD).move_to([-4.3, 3.3, 0])

        def vpath(alpha, color=ACCENT_1, width=4):
            a = np.radians(alpha)
            p0 = np.array([EX, TOPY, 0.0])
            p1 = np.array([EX + T * np.tan(a), TOPY - T, 0.0])
            p2 = np.array([EX + 2 * T * np.tan(a), TOPY, 0.0])
            return VGroup(DashedLine(p0, p1, color=color, stroke_width=width), DashedLine(p1, p2, color=color, stroke_width=width))

        self.sync(c("المَصْفُوفَةِ") - 0.2)
        self.play(FadeIn(wd), FadeIn(array), FadeIn(paut_t), run_time=0.7)
        t_many = tag_line("many small elements", "settings", INK, width=4.6).move_to([-3.9, 2.55, 0])
        self.sync(c("عَنَاصِرَ"))
        self.play(FadeIn(t_many, shift=RIGHT * 0.1), LaggedStart(*[Indicate(e, color=ACCENT_2, scale_factor=1.5) for e in elems],
                                                                  lag_ratio=0.2, run_time=1.4))
        # delays: each element fires a little later than the one before
        DT = 0.149
        bars = VGroup(*[Rectangle(width=0.2, height=0.12 + 0.1 * i, color=ACCENT_2, stroke_width=2).set_fill(ACCENT_2, 0.7)
                        .move_to([x, TOPY + 0.55 + (0.12 + 0.1 * i) / 2, 0]) for i, x in enumerate(el_x)])
        t_delay = tag_line("computed time delays", "clock", ACCENT_2, width=4.6).move_to([-3.9, 1.9, 0])
        tw = ValueTracker(0.0)
        arcs = VGroup(*[Arc(radius=0.05, start_angle=PI + 0.8, angle=PI - 1.3, arc_center=[x, TOPY, 0], color=ACCENT_1, stroke_width=2)
                        for x in el_x])

        def arcs_update(m):
            for i, (x, a_) in enumerate(zip(el_x, m)):
                r = min(max((tw.get_value() - i * DT) * 1.0, 0.0), 1.3)
                new = Arc(radius=max(r, 0.05), start_angle=PI + 0.8, angle=PI - 1.3, arc_center=[x, TOPY, 0], color=ACCENT_1, stroke_width=2)
                new.set_stroke(opacity=1.0 if r > 0.04 else 0.0)
                a_.become(new)
        arcs.add_updater(arcs_update)
        self.sync(c("بِتَأْخِيرَاتٍ"))
        self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.1, run_time=0.9), FadeIn(t_delay, shift=RIGHT * 0.1))
        self.add(arcs)
        self.play(tw.animate(run_time=2.1, rate_func=linear).set_value(2.6))
        # steered, then focused, without moving the probe
        self.sync(c("فَتُوَجَّهُ"))
        arcs.clear_updaters()
        beam = vpath(45)
        t_steer = tag_line("beam steered electronically", "arrows-exchange", ACCENT_1, width=5.4).move_to([-3.9, 1.35, 0])
        self.play(FadeOut(arcs), FadeIn(beam), FadeIn(t_steer, shift=RIGHT * 0.1), run_time=0.5)
        self.play(Transform(beam, vpath(60)), run_time=0.9)
        self.sync(c("وَتُرَكَّزُ"))
        fx, fy = -3.7, TOPY - 0.95
        focus_lines = VGroup(*[Line([el_x[i], TOPY, 0], [fx, fy, 0], color=ACCENT_2, stroke_width=3) for i in (0, 3, 7)])
        fdot = Dot([fx, fy, 0], radius=0.1, color=ACCENT_4)
        self.play(FadeOut(beam), FadeOut(t_steer), Create(focus_lines), GrowFromCenter(fdot), run_time=0.7)
        t_focus = tag_line("beam focused electronically", "eye", ACCENT_2, width=5.4).move_to([-3.9, 1.35, 0])
        self.play(FadeIn(t_focus, shift=RIGHT * 0.1), run_time=0.4)
        self.sync(c("دُونَ"))
        t_still = tag_line("the probe does not move", "check", OK_C, width=5.0).move_to([-3.9, 2.55, 0])
        self.play(FadeOut(t_many), FadeIn(t_still, shift=RIGHT * 0.1), run_time=0.5)
        # the sector scan: a fan of angles and a cross-section image
        self.sync(c("وَالمَسْحُ") - 0.1)
        self.play(FadeOut(VGroup(bars, t_delay, focus_lines, fdot, t_focus, t_still)), run_time=0.5)
        AX, AY, RIMG = 3.3, 3.2, 3.3
        pt = lambda ang, r: np.array([AX + r * np.sin(np.radians(ang)), AY - r * np.cos(np.radians(ang)), 0.0])
        arc_out = ArcBetweenPoints(pt(35, RIMG), pt(70, RIMG), angle=np.radians(35), color=GREY_INK, stroke_width=3)
        edge1 = Line(pt(35, 0.0), pt(35, RIMG), color=GREY_INK, stroke_width=3)
        edge2 = Line(pt(70, 0.0), pt(70, RIMG), color=GREY_INK, stroke_width=3)
        sector = VGroup(edge1, edge2, arc_out)
        lines = VGroup(*[Line(pt(a_, 0.0), pt(a_, RIMG), color=LINE_C, stroke_width=2) for a_ in np.linspace(36, 69, 12)])
        s_lab = label("S-scan: a cross-section image", FS_TAG, INK, weight=BOLD).move_to([4.2, 0.2, 0])
        al = ValueTracker(35.0)
        fan = always_redraw(lambda: vpath(al.get_value(), ACCENT_2, 3))
        flaw_pl = Dot(wd.face_point(-1, 0.86), radius=0.09, color=ACCENT_4)
        spot = Dot(pt(64.3, 2.5), radius=0.1, color=ACCENT_4)
        self.sync(c("القِطَاعِيُّ"))
        self.play(Create(sector), FadeIn(flaw_pl), run_time=0.6)
        self.sync(c("يَكْنُسُ"))
        self.add(fan)
        self.play(al.animate(run_time=2.6, rate_func=linear).set_value(70.0),
                  LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.09, run_time=2.6))
        self.remove(fan)
        self.sync(c("لِمَقْطَعِ") - 0.2)
        self.play(GrowFromCenter(spot), FadeIn(s_lab, shift=UP * 0.1), run_time=0.5)

        # ================= time of flight diffraction =================
        self.sync(c("وَفِي") - 0.1)
        self.clear(run_time=0.5)
        TY, TT = 1.7, 1.6
        wd2 = WeldSection(cx=0.0, y_top=TY, t=TT, half_w=5.6)
        XT, XR = -1.9, 1.9
        pt_t, pr_t = wedge_probe(XT, TY, facing=1, size=0.9), wedge_probe(XR, TY, facing=-1, size=0.9)
        tofd_t = label("TOFD", FS_NOTE, ACCENT_1, weight=BOLD).move_to([-5.8, 3.3, 0])
        tx = label("transmitter", FS_TAG, INK, weight=BOLD).move_to([XT - 0.6, 2.85, 0])
        rx = label("receiver", FS_TAG, INK, weight=BOLD).move_to([XR + 0.6, 2.85, 0])
        TS, RS = np.array([XT, TY, 0.0]), np.array([XR, TY, 0.0])
        crack = VGroup(Line([0, TY - 0.45, 0], [0, TY - 1.1, 0], color=ACCENT_4, stroke_width=6),
                       Dot([0, TY - 0.45, 0], radius=0.07, color=ACCENT_3), Dot([0, TY - 1.1, 0], radius=0.07, color=ACCENT_4))
        up_tip, low_tip = crack[1], crack[2]
        ray_up = always_redraw(lambda: VGroup(Line(TS, up_tip.get_center(), color=ACCENT_3, stroke_width=2),
                                              Line(up_tip.get_center(), RS, color=ACCENT_3, stroke_width=2)))
        ray_low = always_redraw(lambda: VGroup(Line(TS, low_tip.get_center(), color=ACCENT_4, stroke_width=2),
                                               Line(low_tip.get_center(), RS, color=ACCENT_4, stroke_width=2)))
        scr = AScan([], width=9.4, height=2.4, t_min=0.0, t_max=100.0, ticks=(), sigma=1.3, x_caption="Arrival time", y_caption="")
        scr.shift(np.array([0.0, -1.95, 0.0]) - scr.frame.get_center())
        shown = {"peaks": []}
        scr.trace.add_updater(lambda m: (setattr(scr, "peaks", shown["peaks"]), scr.update_trace(scr.t_max)))
        PK = {"lat": (18, 0.95), "up": (42, 0.55), "low": (54, 0.5), "bw": (78, 0.9)}

        def peak_label(key, text, color, side=0):
            t_, h_ = PK[key]
            lab = label(text, FS_TAG - 4, color, weight=BOLD)
            if side == 0:
                return lab.move_to([scr.x_of(t_), scr.y_base() + h_ + 0.28, 0])
            lab.move_to([scr.x_of(t_) + side * 0.0, scr.y_base() + h_ + 0.28, 0])
            return lab.next_to([scr.x_of(t_), scr.y_base() + h_ + 0.28, 0], RIGHT if side > 0 else LEFT, 0.06)
        l_lat = peak_label("lat", "lateral wave", ACCENT_1)
        l_up = peak_label("up", "upper tip", ACCENT_3, -1)
        l_low = peak_label("low", "lower tip", ACCENT_4, 1)
        l_bw = peak_label("bw", "back wall", ACCENT_2)
        self.sync(c("زَمَنِ", 1) + 0.0)
        self.play(FadeIn(wd2), FadeIn(tofd_t), run_time=0.6)
        self.sync(c("مِجَسَّانِ"))
        self.play(FadeIn(pt_t), FadeIn(pr_t), run_time=0.5)
        self.sync(c("مُرْسِلٌ"))
        self.play(FadeIn(tx, shift=DOWN * 0.1), run_time=0.4)
        self.sync(c("وَمُسْتَقْبِلٌ"))
        self.play(FadeIn(rx, shift=DOWN * 0.1), run_time=0.4)
        # first: the lateral wave along the surface
        self.sync(c("تَصِلُ") - 0.1)
        self.play(FadeIn(scr), run_time=0.4)
        self.add(scr.trace)
        self.sync(c("أَوَّلًا"))
        travel(self, wf(ACCENT_1, RIGHT, amp=0.12, length=0.4), [[XT + 0.1, TY + 0.06, 0], [XR - 0.1, TY + 0.06, 0]], 0.9)
        shown["peaks"] = [PK["lat"]]
        self.play(FadeIn(l_lat, shift=UP * 0.1), run_time=0.3)
        # last: the back-wall echo
        self.sync(c("وَأَخِيرًا"))
        bw_pts = [[XT, TY, 0], [0, TY - TT, 0], [XR, TY, 0]]
        bw_path = VGroup(DashedLine(bw_pts[0], bw_pts[1], color=ACCENT_2, stroke_width=3), DashedLine(bw_pts[1], bw_pts[2], color=ACCENT_2, stroke_width=3))
        self.play(Create(bw_path), run_time=0.5)
        travel(self, wf(ACCENT_2, DOWN, amp=0.12, length=0.4), bw_pts, 0.9)
        shown["peaks"] = [PK["lat"], PK["bw"]]
        self.sync(c("الخَلْفِيِّ"))
        self.play(FadeIn(l_bw, shift=UP * 0.1), run_time=0.3)
        # between: the diffraction from the two tips of a crack
        self.sync(c("وَبَيْنَهُمَا"))
        self.play(GrowFromCenter(crack), run_time=0.5)
        self.sync(c("إِشَارَتَا"))
        self.add(ray_up, ray_low)
        self.wait(0.5)
        shown["peaks"] = [PK["lat"], PK["up"], PK["bw"]]
        self.sync(c("الحَيْدِ", 2))
        self.play(FadeIn(l_up, shift=UP * 0.1), run_time=0.3)
        shown["peaks"] = [PK["lat"], PK["up"], PK["low"], PK["bw"]]
        self.sync(c("طَرَفَيِ"))
        self.play(FadeIn(l_low, shift=UP * 0.1), run_time=0.3)
        # the gap between the two diffraction signals gives the height
        gap = DoubleArrow([scr.x_of(PK["up"][0]) + 0.1, scr.y_base() + 0.14, 0], [scr.x_of(PK["low"][0]) - 0.1, scr.y_base() + 0.14, 0], buff=0,
                          color=ACCENT_3, stroke_width=3, tip_length=0.1)
        gap_lab = label("gap = crack height", FS_TAG - 4, ACCENT_3, weight=BOLD).move_to([(scr.x_of(PK["up"][0]) + scr.x_of(PK["low"][0])) / 2, scr.y_base() + 1.3, 0])
        gap_lead = DashedLine(gap_lab.get_bottom() + DOWN * 0.04, gap.get_center() + UP * 0.05, color=ACCENT_3, stroke_width=2)
        hgt = DoubleArrow([0.5, TY - 0.45, 0], [0.5, TY - 1.1, 0], buff=0, color=ACCENT_3, stroke_width=3, tip_length=0.1)
        self.sync(c("ارْتِفَاعَهُ") - 0.3)
        self.play(GrowArrow(gap), FadeIn(gap_lab), Create(gap_lead), GrowArrow(hgt), run_time=0.6)
        # whichever way the crack leans, its two tips still diffract
        self.sync(c("اتِّجَاهِ") - 0.3)
        self.play(FadeOut(hgt), Rotate(crack, angle=np.radians(35), about_point=np.array([0, TY - 0.78, 0])), run_time=0.8)
        self.play(Rotate(crack, angle=-np.radians(70), about_point=np.array([0, TY - 0.78, 0])), run_time=1.0)
        # the dead zone just under the surface
        self.sync(c("مِنْطَقَةٌ") - 0.2)
        self.play(Rotate(crack, angle=np.radians(35), about_point=np.array([0, TY - 0.78, 0])), run_time=0.5)
        dz = Rectangle(width=XR - XT, height=0.32, color=ALERT_C, stroke_width=0).set_fill(ALERT_C, 0.28).move_to([0, TY - 0.16 - 0.0, 0])
        dz_t = tag_line("dead zone under the surface", "alert-triangle", ALERT_C, width=6.4).move_to([-4.0, -0.4, 0])
        dz_lead = Arrow(dz_t.get_top() + UP * 0.04 + RIGHT * 1.8, [-1.3, TY - 0.2, 0], buff=0.05, color=ALERT_C, stroke_width=3, tip_length=0.14)
        self.play(FadeIn(dz), FadeIn(dz_t, shift=UP * 0.1), GrowArrow(dz_lead), run_time=0.5)

        # ================= the series in one line =================
        self.sync(c("وَهٰكَذَا") - 0.2)
        ray_up.clear_updaters()
        ray_low.clear_updaters()
        scr.trace.clear_updaters()
        self.clear(run_time=0.5)
        xs = [-5.0, -1.7, 1.7, 5.0]
        steps = (("Principle", "wifi"), ("Probe and beam", "tool"), ("Calibration", "ruler"), ("Flaw evaluation", "clipboard-check"))
        nodes = VGroup()
        for k, ((nm, ic), x) in enumerate(zip(steps, xs)):
            ring = Circle(radius=0.78, color=ACCENT_1, stroke_width=5).set_fill(PANEL_FILL, 1)
            ic_ = icon(ic, ACCENT_1, 0.85).move_to(ring)
            lab_ = label(nm, FS_NOTE, INK, weight=BOLD).next_to(ring, DOWN, 0.25)
            bd = badge(k + 1, ACCENT_1, 0.28).next_to(ring, UP, 0.2)
            g = VGroup(ring, ic_, lab_, bd).move_to([x, 0.3, 0]) if False else VGroup(ring, ic_, lab_, bd)
            g.shift(np.array([x, 0.3, 0.0]) - ring.get_center())
            nodes.add(g)
        arrows = VGroup(*[Arrow([xs[k] + 0.95, 0.3, 0], [xs[k + 1] - 0.95, 0.3, 0], buff=0, color=INK, stroke_width=4, tip_length=0.2)
                          for k in range(3)])
        for k, (word, nth) in enumerate((("المَبْدَأِ", 1), ("المِجَسِّ", 2), ("المُعَايَرَةِ", 1), ("الحُكْمِ", 1))):
            self.sync(c(word, nth) - 0.1)
            anims = [FadeIn(nodes[k], scale=0.8)]
            if k > 0:
                anims.append(GrowArrow(arrows[k - 1]))
            self.play(*anims, run_time=0.5)
        self.sync(self.end(6))
        self.clear()

    # ---------------- Segment 7: review, 8 questions (entries 7-31) ----------------
    def seg7(self):
        N_E = len(NARRATION)

        def art1():                       # a lamination turns the angle beam up to the cap
            TOP, T = 0.75, 1.4
            wd = WeldSection(cx=0.0, y_top=TOP, t=T, half_w=4.6)
            LX, YL = -2.3, TOP - 0.7
            lam = Ellipse(width=1.6, height=0.12, color=ACCENT_4, stroke_width=3).set_fill(ACCENT_4, 0.9).move_to([LX, YL, 0])
            npr = Probe(color=ACCENT_1)
            npr.shift(np.array([-4.0, TOP, 0.0]) - npr.face_point())
            XE = -3.47
            apr = wedge_probe(XE, TOP, size=0.9)
            hit = np.array([XE + (TOP - YL) * np.tan(np.radians(60)), YL, 0.0])
            land = np.array([XE + 2 * (TOP - YL) * np.tan(np.radians(60)), TOP + 0.04, 0.0])
            legs = VGroup(DashedLine(apr.exit, hit, color=ACCENT_1, stroke_width=3), DashedLine(hit, land, color=ACCENT_2, stroke_width=3))
            tag = tag_line("a false signal at the cap", "alert-triangle", ALERT_C, width=5.2).move_to([0.0, -1.55, 0])
            par = label("parent metal first, with a normal probe", FS_TAG, INK, weight=BOLD).move_to([-1.4, -1.05, 0])

            def show():
                self.play(FadeIn(wd), FadeIn(npr), FadeIn(par), run_time=0.7)

            def finish(*extra):
                self.play(FadeOut(npr), FadeOut(par), FadeIn(apr), Create(lam), *extra, run_time=0.7)
                self.play(Create(legs), run_time=0.7)
                self.play(FadeIn(tag, shift=UP * 0.1), Indicate(wd.cap, color=ACCENT_2, scale_factor=1.0), run_time=0.5)
            return show, finish

        def art2():                       # scan high, evaluate at the reference
            g = ValueTracker(1.0)
            scr = AScan([(0, 1.3), (40, 0.2), (75, 0.55)], width=6.6, height=2.9, t_min=-6.0, t_max=110.0, ticks=(0, 25, 50, 75, 100),
                        sigma=0.9, x_caption="Distance (mm)", y_caption="Echo amplitude")
            scr.shift(np.array([-2.2, -0.2, 0.0]) - scr.frame.get_center())
            scr.trace.add_updater(lambda m: (setattr(scr, "peaks", [(0, 1.3), (40, 0.2 * g.get_value()), (75, 0.55 * g.get_value())]),
                                             scr.update_trace(scr.t_max)))
            ref_y = scr.y_base() + 0.55
            ref = DashedLine([scr.frame.get_left()[0] + 0.5, ref_y, 0], [scr.frame.get_right()[0] - 0.3, ref_y, 0], color=ACCENT_3, stroke_width=3)
            ref_lab = label("reference level", FS_TAG, ACCENT_3, weight=BOLD).next_to(ref, UP, 0.08).align_to(ref, RIGHT)
            k1, k2 = knob("Scanning"), knob("Evaluating")
            k1.move_to([4.6, 0.8, 0]).set_turn(0.5)
            k2.move_to([4.6, -1.7, 0]).set_turn(0.5)

            def show():
                self.play(FadeIn(scr), FadeIn(k1), FadeIn(k2), run_time=0.7)
                self.add(scr.trace)

            def finish(*extra):
                self.play(g.animate(run_time=1.0).set_value(1.8), UpdateFromAlphaFunc(k1, lambda m, a: m.set_turn(0.5 + 0.35 * a)),
                          k1.ring.animate.set_stroke(ACCENT_2), *extra)
                self.play(g.animate(run_time=0.9).set_value(1.0), UpdateFromAlphaFunc(k1, lambda m, a: m.set_turn(0.85 - 0.35 * a)),
                          k1.ring.animate.set_stroke(INK), k2.ring.animate.set_stroke(ACCENT_3), Create(ref), FadeIn(ref_lab))
                scr.trace.clear_updaters()
            return show, finish

        def art3():                       # an echo under the recording line is ignored; one above it is recorded
            H = lambda s: 2.3 * np.exp(-s / 45.0)
            sc = small_scan([-0.3, -0.25], [(0, 1.3), (30, H(30) * D.ILLUSTRATIVE_ECHO_LOW_PCT_DAC / 100), (60, H(60) * D.AMP_PCT_DAC / 100)],
                            width=8.6, height=3.0, t_max=110.0, ticks=(0, 25, 50, 75, 100), x_caption="Sound path (mm)")

            def curve(f, color, dashed=False, width=5):
                vm = VMobject(color=color, stroke_width=width)
                vm.set_points_smoothly([[sc.x_of(s), sc.y_base() + f(s), 0] for s in np.linspace(3, 100, 100)])
                return DashedVMobject(vm, num_dashes=44, dashed_ratio=0.55) if dashed else vm
            dac = curve(H, ACCENT_3, width=6)
            rec = curve(lambda s: H(s) * D.ILLUSTRATIVE_RECORD_PCT_DAC / 100, ACCENT_2, True)
            lab = label("recording level (illustrative)", FS_TAG, ACCENT_2, weight=BOLD).move_to([-0.3, 1.55, 0])
            lo = Dot([sc.x_of(30), sc.y_base() + H(30) * D.ILLUSTRATIVE_ECHO_LOW_PCT_DAC / 100, 0], radius=0.08, color=GREY_INK)
            hi = Dot([sc.x_of(60), sc.y_base() + H(60) * D.AMP_PCT_DAC / 100, 0], radius=0.1, color=ACCENT_4)
            no = icon("x", GREY_INK, 0.45).move_to([sc.x_of(30), sc.y_base() + 0.75, 0])
            yes = icon("check", OK_C, 0.5).move_to([sc.x_of(60) + 0.45, sc.y_base() + 1.1, 0])

            def show():
                self.play(FadeIn(sc), FadeIn(sc.trace), Create(dac), Create(rec), FadeIn(lab), FadeIn(lo), FadeIn(hi), run_time=0.9)

            def finish(*extra):
                self.play(FadeIn(no, scale=0.6), FadeIn(yes, scale=0.6), *extra, run_time=0.6)
            return show, finish

        def art4():                       # at the 6 dB drop the beam axis is on the flaw edge
            MM, BW = 0.17, 8.0
            X = lambda mm: -4.0 + MM * (mm - 100.0)
            FA, FB = 112.0, 135.0
            pos = ValueTracker(123.5)
            band = Rectangle(width=10.0, height=1.0, color=GREY_INK, stroke_width=2).set_fill(ACCENT_2, 0.16).move_to([-1.6, 0.95, 0])
            flaw = Rectangle(width=X(FB) - X(FA), height=0.4, color=ACCENT_4, stroke_width=3).set_fill(ACCENT_4, 0.8)
            flaw.move_to([(X(FA) + X(FB)) / 2, 0.95, 0])
            foot = Rectangle(width=BW * MM, height=0.5, color=ACCENT_1, stroke_width=3)
            foot.add_updater(lambda m: m.become(Rectangle(width=BW * MM, height=0.5, color=ACCENT_1, stroke_width=3)
                                                .set_fill(ACCENT_1, 0.3).move_to([X(pos.get_value()), 0.95, 0])))
            probe = VGroup(RoundedRectangle(width=0.9, height=0.6, corner_radius=0.08, color=ACCENT_1, stroke_width=4).set_fill(BG, 1),
                           Polygon([-0.2, 0.3, 0], [0.2, 0.3, 0], [0, 0.55, 0], color=ACCENT_1, stroke_width=3).set_fill(ACCENT_1, 0.5))
            probe.add_updater(lambda m: m.move_to([X(pos.get_value()), -0.35, 0]))

            def amp(p_):
                ov = max(0.0, min(p_ + BW / 2, FB) - max(p_ - BW / 2, FA))
                return ov / BW
            MX, MY, MH = 5.2, 0.3, 2.4
            meter = Rectangle(width=0.7, height=MH, color=INK, stroke_width=3).set_fill(PANEL_FILL, 1).move_to([MX, MY, 0])
            fill = Rectangle(width=0.62, height=0.02, color=ACCENT_2, stroke_width=0).set_fill(ACCENT_2, 1)
            fill.add_updater(lambda m: m.become(Rectangle(width=0.62, height=max(amp(pos.get_value()) * (MH - 0.1), 0.02), color=ACCENT_2, stroke_width=0)
                                                .set_fill(ACCENT_2, 1).move_to([MX, MY - MH / 2 + 0.05 + max(amp(pos.get_value()) * (MH - 0.1), 0.02) / 2, 0])))
            half = DashedLine([MX - 0.35, MY - MH / 2 + 0.05 + 0.5 * (MH - 0.1), 0], [MX + 0.35, MY - MH / 2 + 0.05 + 0.5 * (MH - 0.1), 0],
                              color=ACCENT_4, stroke_width=4)
            tg = tag_line("half the beam on the flaw", "alert-triangle", ACCENT_4, width=5.0).move_to([-1.6, -1.55, 0])

            def show():
                self.play(FadeIn(band), FadeIn(flaw), FadeIn(meter), run_time=0.5)
                self.add(foot, probe, fill)
                self.wait(0.3)

            def finish(*extra):
                self.play(pos.animate(run_time=1.4).set_value(FA), Create(half), *extra)
                self.play(FadeIn(tg, shift=UP * 0.1), run_time=0.4)
                for m_ in (foot, probe, fill):
                    m_.clear_updaters()
            return show, finish

        def art5():                       # the two 6 dB marks and the length between them
            MM = 0.17
            X = lambda mm: -5.9 + MM * (mm - 100.0)
            ruler = Line([X(100), 0.2, 0], [X(150), 0.2, 0], color=INK, stroke_width=3)
            rt = VGroup(*[Line([X(m_), 0.2, 0], [X(m_), 0.05, 0], color=INK, stroke_width=3) for m_ in range(100, 151, 10)])
            rl = VGroup(*[label(str(m_), FS_TAG - 4, GREY_INK).move_to([X(m_), -0.2, 0]) for m_ in range(100, 151, 10)])
            ru = label("mm", FS_TAG - 4, GREY_INK).move_to([X(150) + 0.5, -0.2, 0])
            m1 = Line([X(D.POS_6DB_1), 0.45, 0], [X(D.POS_6DB_1), -0.4, 0], color=ACCENT_3, stroke_width=7)
            m2 = Line([X(D.POS_6DB_2), 0.45, 0], [X(D.POS_6DB_2), -0.4, 0], color=ACCENT_3, stroke_width=7)
            l1 = label(f"{D.POS_6DB_1:.0f} mm", FS_NOTE, ACCENT_3, weight=BOLD).move_to([X(D.POS_6DB_1) - 0.2, 1.1, 0])
            l2 = label(f"{D.POS_6DB_2:.0f} mm", FS_NOTE, ACCENT_3, weight=BOLD).move_to([X(D.POS_6DB_2) + 0.2, 1.1, 0])
            ask = label("length?", FS_HEADING, ACCENT_4, weight=BOLD).move_to([(X(D.POS_6DB_1) + X(D.POS_6DB_2)) / 2, -1.2, 0])
            arr = DoubleArrow([X(D.POS_6DB_1), -0.85, 0], [X(D.POS_6DB_2), -0.85, 0], buff=0, color=ACCENT_3, stroke_width=4, tip_length=0.16)
            lab = label("length", FS_NOTE, ACCENT_3, weight=BOLD).move_to([(X(D.POS_6DB_1) + X(D.POS_6DB_2)) / 2, -1.3, 0])

            def show():
                self.play(Create(ruler), FadeIn(rt), FadeIn(rl), FadeIn(ru), run_time=0.5)
                self.play(Create(m1), Create(m2), FadeIn(l1), FadeIn(l2), FadeIn(ask), run_time=0.7)

            def finish(*extra):
                self.play(FadeOut(ask), GrowArrow(arr), FadeIn(lab), *extra, run_time=0.7)
            return show, finish

        def art6():                       # a planar flaw loses its echo when the probe goes round it
            F = np.array([-3.0, 0.5, 0.0])
            R_P = 1.2
            ph = ValueTracker(0.0)
            bar = Rectangle(width=1.3, height=0.1, color=ACCENT_4, stroke_width=2).set_fill(ACCENT_4, 0.9).move_to(F)

            def mk(th):
                body = RoundedRectangle(width=0.9, height=0.55, corner_radius=0.08, color=ACCENT_1, stroke_width=4).set_fill(BG, 1)
                nose = Polygon([-0.2, 0.275, 0], [0.2, 0.275, 0], [0, 0.5, 0], color=ACCENT_1, stroke_width=3).set_fill(ACCENT_1, 0.5)
                bm = DashedLine([0, 0.5, 0], [0, 0.5 + R_P - 0.55, 0], color=ACCENT_1, stroke_width=2)
                g = VGroup(body, nose, bm)
                g.rotate(th, about_point=ORIGIN)
                return g.shift(np.array([F[0] + R_P * np.sin(th), F[1] - R_P * np.cos(th), 0.0]))
            pr = mk(0.0)
            sc = small_scan([2.6, 0.1], [(0, 1.0), (50, 1.4)], width=5.4, height=2.6, t_max=110.0, ticks=(0, 50, 100), x_caption="", y_caption="")
            sc.trace.add_updater(lambda m: (setattr(sc, "peaks", [(0, 1.0), (50, 1.4 * np.exp(-(ph.get_value() / 0.3) ** 2))]), sc.update_trace(sc.t_max)))
            tg = tag_line("pore and slag: unchanged", "check", OK_C, width=5.0).move_to([2.6, -1.7, 0])

            def show():
                self.play(FadeIn(bar), FadeIn(pr), FadeIn(sc), FadeIn(sc.trace), run_time=0.7)

            def finish(*extra):
                self.play(UpdateFromAlphaFunc(pr, lambda m, a: (ph.set_value(0.9 * a), m.become(mk(0.9 * a)))), *extra, run_time=1.6)
                self.play(FadeIn(tg, shift=UP * 0.1), run_time=0.4)
                sc.trace.clear_updaters()
            return show, finish

        def art7():                       # the code decides, not the inspector
            insp = chip("Inspector", "user", INK, 3.0).move_to([-4.2, 0.3, 0])
            code = chip("Code in the contract", "book", ACCENT_3, 4.2).move_to([4.0, 0.3, 0])
            dec = chip("Accept / reject", "scale", ACCENT_1, 3.8).move_to([0.0, 0.3, 0])
            q = label("?", FS_TITLE, ACCENT_2, weight=BOLD).move_to([0.0, 1.3, 0])
            a1 = Arrow(insp.get_right() + RIGHT * 0.1, dec.get_left() + LEFT * 0.1, buff=0, color=GREY_INK, stroke_width=4, tip_length=0.18)
            a2 = Arrow(code.get_left() + LEFT * 0.1, dec.get_right() + RIGHT * 0.1, buff=0, color=ACCENT_3, stroke_width=5, tip_length=0.2)
            rep = label("reports findings", FS_TAG, GREY_INK, weight=BOLD).move_to([-2.2, -0.7, 0])
            no = icon("x", ALERT_C, 0.5).move_to([-2.2, 0.85, 0])

            def show():
                self.play(FadeIn(insp), FadeIn(code), FadeIn(dec), FadeIn(q), run_time=0.7)

            def finish(*extra):
                self.play(FadeOut(q), GrowArrow(a2), GrowArrow(a1), FadeIn(rep), FadeIn(no, scale=0.6), *extra, run_time=0.8)
            return show, finish

        def art8():                       # TOFD: the arrival times of the two tip signals give the height
            TY, TT = 1.0, 1.0
            wd = WeldSection(cx=0.0, y_top=TY, t=TT, half_w=5.0)
            TS, RS = np.array([-1.7, TY, 0.0]), np.array([1.7, TY, 0.0])
            pa, pb = wedge_probe(-1.7, TY, facing=1, size=0.8), wedge_probe(1.7, TY, facing=-1, size=0.8)
            cr = VGroup(Line([0, TY - 0.25, 0], [0, TY - 0.7, 0], color=ACCENT_4, stroke_width=6),
                        Dot([0, TY - 0.25, 0], radius=0.07, color=ACCENT_3), Dot([0, TY - 0.7, 0], radius=0.07, color=ACCENT_4))
            rays = VGroup(Line(TS, [0, TY - 0.25, 0], color=ACCENT_3, stroke_width=2), Line([0, TY - 0.25, 0], RS, color=ACCENT_3, stroke_width=2),
                          Line(TS, [0, TY - 0.7, 0], color=ACCENT_4, stroke_width=2), Line([0, TY - 0.7, 0], RS, color=ACCENT_4, stroke_width=2))
            sc = small_scan([0.0, -1.2], [(18, 0.7), (42, 0.42), (54, 0.38), (78, 0.65)], width=8.4, height=1.8, t_min=0.0, t_max=100.0,
                            ticks=(), sigma=1.3, x_caption="Arrival time", y_caption="")
            gap = DoubleArrow([sc.x_of(42) + 0.1, sc.y_base() + 0.1, 0], [sc.x_of(54) - 0.1, sc.y_base() + 0.1, 0], buff=0, color=ACCENT_3,
                              stroke_width=3, tip_length=0.1)
            gl = label("this gap gives the height", FS_TAG - 2, ACCENT_3, weight=BOLD).move_to([(sc.x_of(42) + sc.x_of(54)) / 2 + 2.2, sc.y_base() + 1.0, 0])
            glead = DashedLine(gl.get_left() + LEFT * 0.04, gap.get_center() + UP * 0.05, color=ACCENT_3, stroke_width=2)
            hg = DoubleArrow([0.5, TY - 0.25, 0], [0.5, TY - 0.7, 0], buff=0, color=ACCENT_3, stroke_width=3, tip_length=0.1)

            def show():
                self.play(FadeIn(wd), FadeIn(pa), FadeIn(pb), FadeIn(cr), FadeIn(rays), FadeIn(sc), FadeIn(sc.trace), run_time=0.9)

            def finish(*extra):
                self.play(GrowArrow(gap), FadeIn(gl), Create(glead), GrowArrow(hg), *extra, run_time=0.8)
            return show, finish

        arts = [art1, art2, art3, art4, art5, art6, art7, art8]
        qs = [("Why examine the parent metal with a normal probe first?", "A lamination can reflect the angle beam and give a false signal"),
              ("Which sensitivity do you scan with, and which do you evaluate at?", "Scan above the reference; evaluate at the reference"),
              ("What do you do with an echo under the recording level, and one above it?", "Ignore the first; investigate and record the second"),
              ("Why stop at half the amplitude in the 6 dB drop method?", "The beam axis is then on the edge of the flaw"),
              (f"The echo dropped 6 dB at {D.POS_6DB_1:.0f} mm and at {D.POS_6DB_2:.0f} mm: how long is the flaw?", f"{D.FLAW_LENGTH:.0f} mm"),
              ("What happens to the echo of a planar flaw when you orbit the probe around it?", "It drops sharply, unlike a pore or slag"),
              ("Who decides to accept or reject a flaw?", "The code named in the contract, not the inspector"),
              ("What does time-of-flight diffraction use to find the height of a crack?", "The arrival times of the two tip diffraction signals")]
        cards = [(q, (lambda scene, f=f: f()), a) for (q, a), f in zip(qs, arts)]
        run_review(self, cards, self.cue(7, "بِثَمَانِيَةِ"), self.cue(7, "ثَلَاثُ"), N_E)

    # SEGMENTS-END


if __name__ == "__main__":
    main(__file__, "UtSeriesEp04", NARRATION)
