"""pt_cal, episode 2 (model episode): generating the pressure — the hydraulic hand pump.

Every number on screen or in the narration comes from pt_cal_data. Sources: sources/pt_cal_source.md
(§2, §2-أ, §2-ب) and sources/pt_cal_ep02_pressure.md; storyboard: storyboard/pt_cal_ep02_pressure.md.
The pump, calibrator and transmitter are simplified custom drawings (no product images, no logos).

Build (from the repo root):
    python projects/pt_cal/pt_cal_ep02_pressure.py --preview   # 480p15 -> tmp/pt_cal_ep02_pressure/preview.mp4
    python projects/pt_cal/pt_cal_ep02_pressure.py             # 1080p30 -> output/pt_cal_ep02_pressure.mp4
"""
from explainer import *
import pt_cal_data as D

# Fully diacritized narration (owner-approved 2026-09-28) — one entry per segment.
NARRATION = [
    # 1 the pump makes the pressure; one tee feeds reference and transmitter
    "هٰذِهِ مَادَّةٌ تَعْلِيمِيَّةٌ؛ وَالمَرْجِعُ المُلْزِمُ أَدِلَّةُ الصَّانِعِ وَإِجْرَاءَاتُ مُنْشَأَتِكَ. الحَلْقَةُ الثَّانِيَةُ: تَوْلِيدُ الضَّغْطِ. المُعَايِرُ يَقِيسُ الضَّغْطَ وَلَا يَصْنَعُهُ؛ فَالمِضَخَّةُ تَرْفَعُهُ إِلَى كُلِّ نُقْطَةٍ وَتُثَبِّتُهُ، وَتُوصَلُ بِوَصْلَةٍ ثُلَاثِيَّةٍ إِلَى الوَحْدَةِ المَرْجِعِيَّةِ وَالمُرْسِلِ مَعًا، فَيَرَيَانِ الضَّغْطَ نَفْسَهُ.",
    # 2 the hand-pump family
    "وَمِضَخَّاتُ بِيمِكْس اليَدَوِيَّةُ نَوْعَانِ. هَوَائِيَّةٌ: بِي جِي إِلْ لِلضُّغُوطِ الصَّغِيرَةِ حَوْلَ الصِّفْرِ، وَبِي جِي فِي لِلتَّفْرِيغِ، وَبِي جِي إِمْ حَتَّى عِشْرِينَ بَار، وَبِي جِي سِي حَتَّى خَمْسَةٍ وَثَلَاثِينَ، وَبِي جِي بِي إِتْش المِنْضَدِيَّةُ حَتَّى مِئَةٍ وَأَرْبَعِينَ. وَهَيْدْرُولِيكِيَّةٌ بِالسَّائِلِ: بِي جِي إِتْش إِتْش وَبِي جِي إِكْس إِتْش حَتَّى سَبْعِمِئَةِ بَار، وَبِي جِي إِتْش إِس المِنْضَدِيَّةُ، بِمِقْبَضٍ لَوْلَبِيٍّ، حَتَّى أَلْفٍ.",
    # 3 anatomy of the hydraulic hand pump
    "لِنَفْتَحِ المِضَخَّةَ الهَيْدْرُولِيكِيَّةَ بِي جِي إِتْش إِتْش فِي رَسْمٍ مُبَسَّطٍ: خَزَّانٌ شَفَّافٌ سَعَتُهُ مِئَتَا مِلِّيلِتْرٍ، لَا يَقَعُ عَلَيْهِ الضَّغْطُ. وَمِقْبَضَانِ يَدْفَعَانِ مِكْبَسَ الضَّخِّ. وَمُحَدِّدُ شَوْطٍ بِوَضْعَيْنِ: التَّحْضِيرُ، وَالضَّغْطُ العَالِي. وَصِمَامُ تَنْفِيسٍ. وَمُعَدِّلُ حَجْمٍ لِلضَّبْطِ الدَّقِيقِ. وَمَنْفَذَانِ: جَانِبِيٌّ لِلْخُرْطُومِ، وَعُلْوِيٌّ لِوَحْدَةِ الضَّغْطِ الخَارِجِيَّةِ.",
    # 4 how it pumps; the fine adjust
    "حِينَ تَفْتَحُ المِقْبَضَيْنِ يَرْجِعُ المِكْبَسُ، فَيَسْحَبُ السَّائِلَ مِنَ الخَزَّانِ عَبْرَ صِمَامِ عَدَمِ رُجُوعٍ؛ وَحِينَ تَضُمُّهُمَا يَدْفَعُهُ عَبْرَ صِمَامٍ ثَانٍ إِلَى الخُرْطُومِ فَلَا يَعُودُ. وَالسَّائِلُ لَا يَكَادُ يَنْضَغِطُ، فَيَرْتَفِعُ الضَّغْطُ بِقَلِيلٍ مِنَ الحَجْمِ. وَإِذَا ثَقُلَ الضَّخُّ فَوَضْعُ الضَّغْطِ العَالِي يُقَصِّرُ الشَّوْطَ. أَمَّا مُعَدِّلُ الحَجْمِ فَمِكْبَسٌ صَغِيرٌ بِلَوْلَبٍ: تُدْخِلُهُ فَيَرْتَفِعُ الضَّغْطُ قَلِيلًا، وَتُخْرِجُهُ فَيَنْخَفِضُ. وَبِدُونِهِ تَتَأَرْجَحُ حَوْلَ النُّقْطَةِ، وَتُفْسِدُ الصُّعُودَ بِالتَّجَاوُزِ ثُمَّ العَوْدَةِ.",
    # 5 preparation: fill and bleed
    "التَّحْضِيرُ: امْلَأِ الخَزَّانَ بَيْنَ ثُلُثَيْهِ وَثَلَاثَةِ أَرْبَاعِهِ. ثُمَّ اطْرُدِ الهَوَاءَ: الخُرْطُومُ عَلَى المِضَخَّةِ وَطَرَفُهُ حُرٌّ، وَمُعَدِّلُ الحَجْمِ إِلَى نِهَايَتِهِ، وَالتَّنْفِيسُ مُغْلَقٌ، وَاضْخَخْ حَتَّى تَخْرُجَ قَطَرَاتُ السَّائِلِ، ثُمَّ صِلْهُ بِالمُرْسِلِ. بَعْدَهَا ارْفَعِ الضَّغْطَ إِلَى نَحْوِ خَمْسِينَ بَار وَنَفِّسْ، مَرَّتَيْنِ أَوْ ثَلَاثًا. فَنِظَامُ القِيَاسِ سَائِلٌ فَقَطْ، بِلَا غَازٍ؛ لِأَنَّ فُقَاعَةَ الهَوَاءِ تَنْضَغِطُ، فَتُطِيلُ الِاسْتِقْرَارَ وَتَبْدُو كَالتَّسْرِيبِ.",
    # 6 reaching the point; wait; leak
    "لِلْوُصُولِ إِلَى النُّقْطَةِ: ابْدَأْ بِوَضْعِ التَّحْضِيرِ وَاضْخَخْ، فَإِذَا ثَقُلَ الضَّخُّ فَانْتَقِلْ إِلَى الضَّغْطِ العَالِي. اقْتَرِبْ مِنْ أَسْفَلَ، وَأَكْمِلْ بِمُعَدِّلِ الحَجْمِ، وَعَيْنُكَ عَلَى المُؤَشِّرِ. بَعْدَ التَّوْلِيدِ قَدْ يَهْبِطُ الضَّغْطُ قَلِيلًا بِالأَثَرِ الحَرَارِيِّ أَوْ بِتَمَدُّدِ الخُرْطُومِ؛ فَانْتَظِرْ دَقِيقَتَيْنِ إِلَى خَمْسٍ ثُمَّ أَعِدْهُ. فَإِنِ اسْتَمَرَّ الهُبُوطُ بِثَبَاتٍ فَهُوَ تَسْرِيبٌ: نَفِّسْ، وَافْحَصِ الوَصَلَاتِ وَالحَشِيَّاتِ.",
    # 7 lowering, fluids, gas service
    "وَلِخَفْضِ الضَّغْطِ اسْتَعْمِلْ مُعَدِّلَ الحَجْمِ أَوَّلًا، وَافْتَحِ التَّنْفِيسَ بِحَذَرٍ تَجَنُّبًا لِصَدْمَةِ الضَّغْطِ، وَلَا تَفُكَّهُ كَامِلًا أَبَدًا. وَالسَّوَائِلُ المَسْمُوحَةُ اثْنَانِ: زَيْتٌ هَيْدْرُولِيكِيٌّ مَعْدِنِيٌّ خَفِيفٌ، أَوْ مَاءٌ مُقَطَّرٌ تُفْرِغُهُ بَعْدَ كُلِّ اسْتِعْمَالٍ؛ وَغَيْرُهُمَا يُتْلِفُ الحَشِيَّاتِ. وَلَا يَصْلُحُ السَّائِلُ لِمُرْسِلٍ سَيَعُودُ إِلَى خِدْمَةٍ غَازِيَّةٍ: فَيَبْقَى مِنْهُ أَثَرٌ فِي حُجْرَتِهِ، يَحْمِلُهُ إِلَى العَمَلِيَّةِ، أَوْ يَسْتَقِرُّ عَمُودًا يُزِيحُ القِرَاءَةَ. وَلِذٰلِكَ يَمْنَعُ الدَّلِيلُ خُرْطُومًا وَاحِدًا لِلْغَازِ وَالسَّائِلِ.",
    # 8 safety and hoses
    "وَمِنْ تَحْذِيرَاتِ الدَّلِيلِ: نَظَّارَةٌ وَاقِيَةٌ، وَالخُرْطُومُ الأَصْلِيُّ فَقَطْ. لَا تَمْلَأِ الخَزَّانَ فَوْقَ حَدِّهِ، وَلَا تُضِفْ سَائِلًا وَأَنْتَ تَرْفَعُ الضَّغْطَ؛ فَعِنْدَ التَّنْفِيسِ يَعُودُ السَّائِلُ كُلُّهُ فَيَفِيضُ، وَقَدْ يَنْكَسِرُ الخَزَّانُ. وَمُقَاوَمَةٌ قَوِيَّةٌ بِلَا ارْتِفَاعٍ فِي الضَّغْطِ تَعْنِي: تَوَقَّفْ وَابْحَثْ عَنِ العُطْلِ. وَلِكُلِّ مَدًى خُرْطُومُهُ: أَرْبَعُونَ بَار لِلْمَدَى المُنْخَفِضِ وَالمُتَوَسِّطِ، وَسِتُّمِئَةٍ وَثَلَاثُونَ لِلْعَالِي؛ وَخُرْطُومُ عِشْرِينَ عَلَى نِظَامِ أَرْبَعِينَ قُنْبُلَةٌ مَوْقُوتَةٌ. وَكُلُّ مُحَوِّلٍ إِضَافِيٍّ نُقْطَةُ تَسْرِيبٍ؛ فَأَقْصَرُ سِلْسِلَةٍ أَدَقُّ.",
    # 9 pneumatic pumps
    "وَالمِضَخَّاتُ الهَوَائِيَّةُ بِالمَبْدَإِ نَفْسِهِ: مِكْبَسٌ وَصِمَامُ عَدَمِ رُجُوعٍ. فِي بِي جِي سِي مِفْتَاحٌ لِلضَّغْطِ أَوِ التَّفْرِيغِ، لَا يُغَيَّرُ تَحْتَ الضَّغْطِ، وَالضَّخُّ يَبْلُغُ نَحْوَ عِشْرِينَ إِلَى خَمْسَةٍ وَعِشْرِينَ بَار، وَالبَاقِي بِمُعَدِّلِ الحَجْمِ. وَفِي بِي جِي بِي إِتْش: اضْخَخْ، ثُمَّ أَغْلِقْ صِمَامَ العَزْلِ، ثُمَّ اضْبِطْ بِالعَجَلَةِ. وَالهَوَاءُ خَفِيفٌ نَظِيفٌ، لٰكِنَّهُ يَسْخُنُ بِالضَّغْطِ، فَإِذَا بَرَدَ هَبَطَ الضَّغْطُ؛ فَانْتَظِرْ نِصْفَ دَقِيقَةٍ إِلَى دَقِيقَةٍ. وَهٰذَا الأَثَرُ فِي السَّائِلِ أَصْغَرُ بِكَثِيرٍ.",
    # 10 automatic generation
    "وَلِلتَّوْلِيدِ الآلِيِّ: إِي بِي جِي، مِضَخَّةٌ كَهْرَبَائِيَّةٌ بِالبَطَّارِيَّةِ، مِنْ سَالِبِ صِفْرٍ فَاصِلَةِ خَمْسَةٍ وَثَمَانِينَ إِلَى عِشْرِينَ بَار؛ يُعْطِيهَا إِمْ سِي سِكْس النُّقْطَةَ فَتَضْبِطُهَا وَحْدَهَا، وَتَعْمَلُ مَعَ أَيِّ مُعَايِرٍ آخَرَ. وَبِي أُو سِي ثَمَانِيَة، مُتَحَكِّمٌ آلِيٌّ مِنَ التَّفْرِيغِ حَتَّى مِئَتَيْنِ وَعَشَرَةِ بَار، مِنْضَدِيٌّ أَوْ فِي مَقْعَدِ سِنْتْرِيكَال لِلْوَرْشَةِ.",
]

# Every spoken or shown value is checked against the data module; stop if it drifts.
_P = {m: (lo, hi, u) for m, _, lo, hi, u in D.PUMPS}
assert _P["PGM"][1] == 20 and _P["PGC"][1] == 35 and _P["PGPH"][1] == 140          # seg 2
assert _P["PGHH"][1] == 700 == _P["PGXH"][1] and _P["PGHS"][1] == 1000             # seg 2
assert D.PGHH_RESERVOIR_ML == 200 and D.PGHH_FILL == ("2/3", "3/4")                # seg 3, 5
assert D.PGHH_BLEED_BAR == 50 and D.PGHH_BLEED_REPEAT == (2, 3)                     # seg 5
assert D.PGHH_WAIT_MIN == (2, 5)                                                    # seg 6
assert D.HOSE_LOW_BAR == 40 and D.PGHH_HOSE_BAR == 630 and D.BAD_HOSE_BAR == 20     # seg 8
assert D.PGC_PUMP_MAX_BAR == (20, 25) and D.AIR_WAIT_S == (30, 60)                  # seg 9
assert D.EPG_RANGE == (-0.85, 20) and D.POC8_MAX_BAR == 210                         # seg 10

AUDIO_DIR = audio_dir_for(__file__)

# ---------------- palette roles (project CLAUDE.md) ----------------
FLUID = ACCENT_1          # pressure, liquid, flow
MOVE = ACCENT_2           # hand and moving parts, heat
GOOD = ACCENT_3
BAD = ACCENT_4
AIR = GREY_INK
FLUID_FILL = "#cfe0f3"    # light blue fill of liquid volumes
BODY_FILL = "#f4f4f4"


def fmt(x, nd=1):
    """Number for the screen with a real minus sign."""
    s = f"{x:.{nd}f}"
    return s.replace("-", "−")


def rng(lo, hi, unit):
    return f"{fmt(lo, 2 if abs(lo) < 1 and lo else 0)} … {fmt(hi, 0)} {unit}".replace("−0 ", "0 ")


def P(x, y):
    """Point of the pump drawing (the whole cut-away is shifted by OX, OY)."""
    return np.array([x + 1.0, y + 0.3, 0.0])


def pipe(*pts, color=INK, width=6):
    m = VMobject(color=color, stroke_width=width)
    m.set_points_as_corners([np.array(p, dtype=float) for p in pts])
    return m


def flow(path, color=FLUID, width=10, time_width=0.6):
    """A pulse running along a path (liquid or air moving)."""
    return ShowPassingFlash(path.copy().set_stroke(color, width), time_width=time_width)


def tag(text, size=FS_TAG, color=INK, **kw):
    return label(text, size, color, **kw)


# =====================================================================
# The hydraulic hand pump (simplified cut-away, PGHH manual fig. 1)
# =====================================================================
class Pump:
    """Cut-away of a hydraulic hand pump; its moving parts follow ValueTrackers:
    lever (0 open … 1 squeezed), fine (0 out … 1 in), level (reservoir 0…1), press (bar),
    high (0 prime … 1 high: the stroke selector knob)."""

    def __init__(self):
        self.lever = ValueTracker(0.0)
        self.fine = ValueTracker(0.5)
        self.level = ValueTracker(0.7)
        self.press = ValueTracker(0.0)
        self.high = ValueTracker(0.0)
        # body and reservoir
        self.body = Rectangle(width=5.4, height=2.2, color=INK, stroke_width=4) \
            .set_fill(BODY_FILL, 1).move_to((P(-3.2, -1.6) + P(2.2, 0.6)) / 2)
        self.res = Rectangle(width=1.8, height=1.6, color=GREY_INK, stroke_width=4) \
            .move_to((P(-2.9, 0.9) + P(-1.1, 2.5)) / 2)
        self.plug = Rectangle(width=0.5, height=0.18, color=INK, stroke_width=3) \
            .set_fill(INK, 1).next_to(self.res, UP, buff=0)
        self.res_fluid = always_redraw(self._res_fluid)
        # suction line, inlet check valve, cylinder
        self.suction = pipe(P(-2.0, 0.9), P(-2.0, 0.05), P(-0.65, 0.05))
        self.cv1 = check_valve(size=0.42).move_to(P(-1.35, 0.05))
        self.cyl = VGroup(Line(P(-0.65, 0.2), P(-0.65, -1.45)), Line(P(-0.15, 0.2), P(-0.15, -1.45)),
                          Line(P(-0.65, 0.2), P(-0.15, 0.2))).set_stroke(INK, 4)
        self.chamber = always_redraw(self._chamber)
        self.piston = always_redraw(self._piston)
        # outlet check valve, gallery, return with vent valve, top port, fine adjust, side port
        self.gallery = pipe(P(-0.15, 0.05), P(2.2, 0.05))
        self.cv2 = check_valve(size=0.42).move_to(P(0.35, 0.05))
        self.ret = pipe(P(0.95, 0.05), P(0.95, 0.4), P(-1.5, 0.4), P(-1.5, 0.9))
        self.vent = gate_valve(size=0.38).move_to(P(0.15, 0.4))
        self.top = pipe(P(1.75, 0.05), P(1.75, 1.12))
        self.ext = Rectangle(width=1.8, height=0.75, color=INK, stroke_width=4) \
            .set_fill(WHITE, 1).move_to(P(1.75, 1.5))
        self.readout = always_redraw(self._readout)
        self.fine_line = pipe(P(1.35, 0.05), P(1.35, -0.9))
        self.fine_cyl = VGroup(Line(P(1.35, -0.72), P(2.2, -0.72)), Line(P(1.35, -1.08), P(2.2, -1.08))) \
            .set_stroke(INK, 4)
        self.plunger = always_redraw(self._plunger)
        self.port = pipe(P(2.2, 0.05), P(2.45, 0.05), width=8)
        # stroke selector and handles
        self.selector = always_redraw(self._selector)
        self.pivot = Dot(P(1.9, -1.85), radius=0.08, color=INK)
        self.grip = Line(P(-0.9, -1.75), P(-3.4, -1.75), stroke_width=10, color=INK)
        self.handle = always_redraw(self._handle)
        self.rod = always_redraw(self._rod)

    # ---- geometry that follows the trackers ----
    def lever_end(self):
        return P(-3.4, -3.0 + 0.9 * self.lever.get_value())

    def rod_foot(self):
        a, b = P(1.9, -1.85), self.lever_end()
        t = (1.9 + 0.4) / (1.9 + 3.4)
        return a + (b - a) * t

    def piston_y(self):
        return -1.0 + 0.4 * self.lever.get_value()

    def _res_fluid(self):
        lv = max(self.level.get_value(), 0.02)
        h = 1.6 * min(lv, 1.0)
        r = Rectangle(width=1.8, height=h, stroke_width=0).set_fill(FLUID_FILL, 1)
        return r.align_to(self.res, DOWN).align_to(self.res, LEFT)

    def _chamber(self):
        top = 0.2
        bot = self.piston_y() + 0.11
        r = Rectangle(width=0.46, height=top - bot, stroke_width=0).set_fill(FLUID_FILL, 1)
        return r.move_to(P(-0.4, (top + bot) / 2))

    def _piston(self):
        return Rectangle(width=0.46, height=0.22, color=MOVE, stroke_width=3) \
            .set_fill(MOVE, 1).move_to(P(-0.4, self.piston_y()))

    def _rod(self):
        return Line(self.rod_foot(), P(-0.4, self.piston_y() - 0.11), stroke_width=6, color=MOVE)

    def _handle(self):
        return Line(P(1.9, -1.85), self.lever_end(), stroke_width=10, color=MOVE)

    def _plunger(self):
        x = 1.95 - 0.4 * self.fine.get_value()
        pl = Rectangle(width=0.14, height=0.34, color=MOVE, stroke_width=2).set_fill(MOVE, 1) \
            .move_to(P(x, -0.9))
        fl = Rectangle(width=max(x - 0.07 - 1.35, 0.01), height=0.34, stroke_width=0) \
            .set_fill(FLUID_FILL, 1).move_to(P((1.35 + x - 0.07) / 2, -0.9))
        stem = Line(P(x + 0.07, -0.9), P(x + 0.6, -0.9), stroke_width=5, color=MOVE)
        knob = RoundedRectangle(width=0.2, height=0.5, corner_radius=0.05, color=MOVE,
                                stroke_width=3).set_fill(MOVE, 1).move_to(P(x + 0.7, -0.9))
        return VGroup(fl, pl, stem, knob)

    def _selector(self):
        x = -3.37 + 0.35 * self.high.get_value()
        return Rectangle(width=0.34, height=0.3, color=MOVE, stroke_width=3).set_fill(MOVE, 1) \
            .move_to(P(x, -0.9))

    def _readout(self):
        return fit(tag(f"{fmt(self.press.get_value())} bar", FS_TAG + 2), self.ext.width - 0.4).move_to(self.ext)

    # ---- groups ----
    def static(self):
        return VGroup(self.body, self.res, self.plug, self.suction, self.cv1, self.cyl,
                      self.gallery, self.cv2, self.ret, self.vent, self.top, self.ext,
                      self.fine_line, self.fine_cyl, self.port, self.pivot, self.grip)

    def moving(self):
        return VGroup(self.res_fluid, self.chamber, self.piston, self.rod, self.handle,
                      self.plunger, self.selector, self.readout)

    def paths(self):
        """Flow paths used by the pulses."""
        inlet = pipe(P(-2.0, 0.9), P(-2.0, 0.05), P(-0.65, 0.05))
        outlet = pipe(P(-0.15, 0.05), P(2.45, 0.05))
        vent = pipe(P(0.95, 0.05), P(0.95, 0.4), P(-1.5, 0.4), P(-1.5, 0.9))
        return inlet, outlet, vent


def transmitter(tag_loop="101"):
    """Generic pressure transmitter (no brand): body, process port on the left, ISA bubble."""
    body = RoundedRectangle(width=1.0, height=1.2, corner_radius=0.12, color=INK, stroke_width=4) \
        .set_fill(WHITE, 1)
    head = Circle(radius=0.42, color=INK, stroke_width=4).set_fill(WHITE, 1).next_to(body, UP, buff=0)
    port = Line(body.get_left(), body.get_left() + LEFT * 0.35, stroke_width=8, color=INK)
    bub = instrument("PT", tag_loop, size=0.9).next_to(head, RIGHT, buff=0.3)
    lead = Line(head.get_right(), bub.get_left(), stroke_width=2, color=GREY_INK)
    g = VGroup(body, head, port, bub, lead)
    g.port_point = lambda: port.get_end()
    g.body = body
    return g


def bottle(color, h=1.3):
    """A simple bottle outline filled with a liquid colour."""
    body = RoundedRectangle(width=0.8, height=h, corner_radius=0.12, color=INK, stroke_width=3)
    liquid = Rectangle(width=0.8, height=h * 0.7, stroke_width=0).set_fill(color, 1) \
        .align_to(body, DOWN)
    neck = Rectangle(width=0.32, height=0.3, color=INK, stroke_width=3).next_to(body, UP, buff=0)
    cap = Rectangle(width=0.4, height=0.12, color=INK, stroke_width=2).set_fill(INK, 1) \
        .next_to(neck, UP, buff=0)
    return VGroup(liquid, body, neck, cap)


def cross(mob, color=BAD, width=6):
    """Red X over a drawing (not over a text)."""
    a = Line(mob.get_corner(UL), mob.get_corner(DR), stroke_width=width, color=color)
    b = Line(mob.get_corner(DL), mob.get_corner(UR), stroke_width=width, color=color)
    return VGroup(a, b)


class PtCalEp02(SyncedScene):
    def c(self, seg, phrase, nth=1):
        return self.cue(seg, phrase, nth)

    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        self.seg1_setup()
        self.seg2_family()
        pump = Pump()
        self.pump = pump
        self.seg3_anatomy(pump)
        self.seg4_mechanism(pump)
        self.seg5_prepare(pump)
        self.seg6_point()
        self.seg7_lower()
        self.seg8_safety()
        self.seg9_pneumatic()
        self.seg10_auto()

    # ---------------- Segment 1: the pump makes the pressure ----------------
    def seg1_setup(self):
        title = title_card(self, "Generating the pressure",
                           "Hand pumps — the hydraulic pump in detail",
                           series="Pressure transmitter calibration · Episode 2 of 7")
        note = tag("Educational material — the manufacturer's manuals and your site procedures are binding",
                   FS_TAG, GREY_INK)
        fit(note).next_to(title, DOWN, buff=0.6)
        self.play(FadeIn(note), run_time=0.6)
        self.sync(self.c(1, "المُعَايِرُ يَقِيسُ") - 0.7)
        self.clear()
        self.sec = section_title(self, "The pump makes the pressure")
        # pump block, tee, reference module + calibrator, transmitter
        pump = RoundedRectangle(width=1.8, height=1.3, corner_radius=0.15, color=INK, stroke_width=4) \
            .set_fill(BODY_FILL, 1).move_to([-4.6, -0.8, 0])
        pump_lab = tag("Hand pump", FS_LABEL).next_to(pump, UP, buff=0.25)
        grip = Line(pump.get_corner(DL) + RIGHT * 0.2 + DOWN * 0.02,
                    pump.get_corner(DL) + LEFT * 0.9 + DOWN * 0.5, stroke_width=10, color=MOVE)
        tee = Dot([-1.2, -0.8, 0], radius=0.1, color=INK)
        p1 = pipe(pump.get_right(), tee.get_center())
        ext = Rectangle(width=2.5, height=0.9, color=INK, stroke_width=4).set_fill(WHITE, 1) \
            .move_to([-1.2, 1.6, 0])
        p2 = pipe(tee.get_center(), ext.get_bottom())
        ext_lab = tag("Reference module", FS_LABEL).next_to(ext, UP, buff=0.2)
        xm = transmitter().move_to([2.4, -0.8, 0])
        p3 = pipe(tee.get_center(), xm.port_point())
        cal = RoundedRectangle(width=2.2, height=1.4, corner_radius=0.15, color=INK, stroke_width=4) \
            .set_fill(WHITE, 1).move_to([4.9, 1.6, 0])
        cal_lab = tag("Calibrator", FS_LABEL).next_to(cal, UP, buff=0.2)
        cable = DashedLine(ext.get_right(), cal.get_left(), color=GREY_INK, stroke_width=3)
        wire = pipe(xm.body.get_right(), [4.9, -0.8 + 0.2, 0], cal.get_bottom(), color=MOVE, width=3)
        pv = ValueTracker(0.0)
        read_p = always_redraw(lambda: tag(f"{fmt(pv.get_value(), 2)} {D.UNIT}", FS_TAG)
                               .move_to(ext))
        read_i = always_redraw(lambda: tag(f"{fmt(D.i_linear(pv.get_value()), 2)} mA", FS_TAG + 2)
                               .move_to(cal))
        self.play(Create(pump), Create(grip), FadeIn(pump_lab), run_time=0.8)
        self.sync(self.c(1, "وَتُوصَلُ"))
        tee_lab = tag("tee", FS_TAG).next_to(tee, DOWN, buff=0.2)
        self.play(Create(p1), GrowFromCenter(tee), FadeIn(tee_lab), run_time=0.6)
        self.play(Create(p2), Create(p3), run_time=0.6)
        self.play(Create(ext), FadeIn(ext_lab), FadeIn(xm), run_time=0.8)
        self.play(Create(cal), FadeIn(cal_lab), Create(cable), Create(wire),
                  FadeIn(read_p), FadeIn(read_i), run_time=0.8)
        self.sync(self.c(1, "فَيَرَيَانِ"))
        path = pipe(pump.get_right(), tee.get_center())
        self.play(flow(path), grip.animate.rotate(0.25, about_point=grip.get_start()), run_time=0.5)
        self.play(flow(p2.copy()), flow(p3.copy()), pv.animate.set_value(D.SETUP_DEMO_PV),
                  grip.animate.rotate(-0.25, about_point=grip.get_start()), run_time=1.2)
        same = tag("same pressure, same moment", FS_LABEL, FLUID).move_to([-1.2, -2.6, 0])
        self.play(FadeIn(same), Indicate(ext), Indicate(xm.body), run_time=0.6)
        self.sync(self.end(1) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 2: the hand-pump family ----------------
    def seg2_family(self):
        section_title(self, "Beamex hand pumps: medium and range", prev=self.sec)
        x0, xneg, xlen = -1.2, 1.3, 7.5           # zero, width of −1 bar, width of 0 → 1000 bar

        def X(p):
            if p < 0:
                return x0 + xneg * p
            return x0 + xlen * np.log10(1 + p) / np.log10(1001)

        y_axis = -2.5
        axis = Line([X(-1), y_axis, 0], [X(1000), y_axis, 0], stroke_width=3, color=INK)
        ticks = VGroup()
        for p, t in [(-1, "−1"), (0, "0"), (1, "1"), (10, "10"), (100, "100"), (1000, "1000")]:
            ticks.add(Line([X(p), y_axis, 0], [X(p), y_axis - 0.12, 0], stroke_width=3, color=INK))
            ticks.add(tag(t, FS_AXIS).next_to([X(p), y_axis - 0.12, 0], DOWN, buff=0.1))
        unit = tag("bar (log scale above 0)", FS_AXIS, GREY_INK).next_to(ticks, DOWN, buff=0.15) \
            .align_to(axis, RIGHT)
        zero = DashedLine([X(0), 2.9, 0], [X(0), y_axis, 0], color=LIGHT_INK, stroke_width=2)
        legend = VGroup(
            VGroup(icon("wind", AIR, 0.42), tag("air", FS_LABEL, AIR)).arrange(RIGHT, buff=0.15),
            VGroup(icon("droplet", FLUID, 0.42), tag("liquid", FS_LABEL, FLUID)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.6).to_corner(UR, buff=0.4)
        self.play(Create(axis), FadeIn(ticks), FadeIn(unit), Create(zero), run_time=1.0)
        rows = []
        y = 2.35
        for model, medium, lo, hi, u in D.PUMPS:
            f = 0.001 if u == "mbar" else 1.0
            lo_b, hi_b = lo * f, hi * f
            col = AIR if medium == "air" else FLUID
            name = tag(model, FS_LABEL, col, weight=BOLD).move_to([-6.3, y, 0]).align_to([-6.75, 0, 0], LEFT)
            span = tag(rng(lo, hi, u), FS_TAG).next_to(name, RIGHT, buff=0.25)
            bar = Rectangle(width=max(X(hi_b) - X(lo_b), 0.05), height=0.3, stroke_width=0) \
                .set_fill(col, 0.85).move_to([(X(hi_b) + X(lo_b)) / 2, y, 0])
            rows.append((model, VGroup(name, span), bar))
            y -= 0.6
        cues = {"PGL": "بِي جِي إِلْ", "PGV": "بِي جِي فِي", "PGM": "بِي جِي إِمْ", "PGC": "بِي جِي سِي",
                "PGPH": "بِي جِي بِي إِتْش", "PGHH": "بِي جِي إِتْش إِتْش", "PGXH": "بِي جِي إِكْس إِتْش",
                "PGHS": "بِي جِي إِتْش إِس"}
        self.sync(self.c(2, "هَوَائِيَّةٌ"))
        self.play(FadeIn(legend[0]), run_time=0.4)
        for model, text, bar in rows:
            if model == "PGHH":
                self.sync(self.c(2, "وَهَيْدْرُولِيكِيَّةٌ"))
                self.play(FadeIn(legend[1]), run_time=0.4)
            self.sync(self.c(2, cues[model]))
            self.play(FadeIn(text, shift=RIGHT * 0.1), GrowFromEdge(bar, LEFT), run_time=0.6)
        bench = tag("bench · screw handle", FS_TAG, FLUID).next_to(rows[-1][2], DOWN, buff=0.1) \
            .align_to(rows[-1][2], RIGHT)
        self.sync(self.c(2, "بِمِقْبَضٍ"))
        self.play(FadeIn(bench), run_time=0.4)
        self.sync(self.end(2) - 0.5)
        self.clear(self.sec, run_time=0.5)

    # ---------------- Segment 3: anatomy of the hydraulic hand pump ----------------
    def seg3_anatomy(self, pm):
        section_title(self, "Hydraulic hand pump (simplified)", prev=self.sec)
        callouts = [("Reservoir\n200 ml", pm.res, LEFT),
                    ("Handles +\npump piston", pm.lever_end(), LEFT),
                    ("Stroke selector\nPrime / High", P(-3.37, -0.9), LEFT),
                    ("Vent\nvalve", pm.vent.get_left() + UP * 0.12, UP),
                    ("Fine\nadjust", P(2.7, -0.9), RIGHT),
                    ("Side port:\nhose", P(2.45, 0.05), RIGHT),
                    ("Top port:\nEXT", pm.ext, RIGHT)]
        cues = [self.c(3, "خَزَّانٌ"), self.c(3, "وَمِقْبَضَانِ"), self.c(3, "وَمُحَدِّدُ"),
                self.c(3, "وَصِمَامُ"), self.c(3, "وَمُعَدِّلُ"), self.c(3, "جَانِبِيٌّ"),
                self.c(3, "وَعُلْوِيٌّ")]
        self.sync(self.start(3) + 0.3)
        self.play(Create(pm.static()), run_time=2.2)
        self.play(FadeIn(pm.moving()), run_time=0.5)
        ghost = VectorizedPoint(ORIGIN)
        n1 = labeled_diagram(self, ghost, callouts[:1], cues=cues[:1], draw_time=0.01)[1]
        no_p = tag("not pressurised", FS_TAG, GREY_INK).next_to(n1[0][0], DOWN, buff=0.2)
        self.sync(self.c(3, "لَا يَقَعُ"))
        self.play(FadeIn(no_p), Indicate(pm.res, color=FLUID), run_time=0.8)
        n2 = labeled_diagram(self, ghost, callouts[1:2], cues=cues[1:2], draw_time=0.01, start=2)[1]
        self.sync(self.c(3, "مِكْبَسَ"))
        self.play(pm.lever.animate.set_value(1), Indicate(pm.piston, color=MOVE, scale_factor=1.4), run_time=0.8)
        self.play(pm.lever.animate.set_value(0), run_time=0.5)
        n2b = labeled_diagram(self, ghost, callouts[2:3], cues=cues[2:3], draw_time=0.01, start=3)[1]
        self.sync(self.c(3, "التَّحْضِيرُ"))
        self.play(Indicate(pm.selector, color=MOVE), run_time=0.6)
        self.sync(self.c(3, "وَالضَّغْطُ العَالِي"))
        self.play(pm.high.animate.set_value(1), run_time=0.5)
        self.play(pm.high.animate.set_value(0), run_time=0.5)
        n3 = labeled_diagram(self, ghost, callouts[3:], cues=cues[3:], draw_time=0.01, start=4)[1]
        self.labels3 = VGroup(n1, no_p, n2, n2b, n3)
        self.sync(self.end(3) - 0.5)
        self.play(FadeOut(self.labels3), pm.lever.animate.set_value(1), run_time=0.5)

    # ---------------- Segment 4: how it pumps; the fine adjust ----------------
    def seg4_mechanism(self, pm):
        self.sec = section_title(self, "How it pumps", prev=self.sec)
        inlet, outlet, _ = pm.paths()
        cv1_lab = tag("inlet check valve", FS_TAG, GOOD)
        cv2_lab = tag("outlet check valve", FS_TAG, GOOD)
        cv1_lab.move_to([-4.6, 1.0, 0])
        cv2_lab.move_to([4.6, 0.95, 0])
        cv1_link = Arrow(cv1_lab.get_right(), pm.cv1.get_top(), buff=0.1, stroke_width=3,
                         color=GOOD, max_tip_length_to_length_ratio=0.12)
        cv2_link = Arrow(cv2_lab.get_left(), pm.cv2.get_top(), buff=0.1, stroke_width=3,
                         color=GOOD, max_tip_length_to_length_ratio=0.12)
        # 1) handles open: piston back, suction through the inlet check valve
        self.sync(self.c(4, "حِينَ تَفْتَحُ"))
        self.play(pm.lever.animate.set_value(0.0), run_time=1.0)
        self.say("open → piston back → suction", y=-3.5)
        self.sync(self.c(4, "فَيَسْحَبُ"))
        self.play(flow(inlet), pm.level.animate.set_value(0.66), FadeIn(cv1_lab), GrowArrow(cv1_link),
                  pm.cv1.animate.set_color(GOOD), run_time=1.4)
        # 2) handles squeezed: pushed through the outlet check valve, no way back
        self.sync(self.c(4, "وَحِينَ تَضُمُّهُمَا"))
        self.say("squeeze → out, no return", y=-3.5)
        self.play(pm.lever.animate.set_value(1.0), flow(outlet), FadeIn(cv2_lab), GrowArrow(cv2_link),
                  pm.cv2.animate.set_color(GOOD), pm.cv1.animate.set_color(INK),
                  pm.press.animate.set_value(D.STROKE_DEMO_BAR[0]), run_time=1.4)
        # 3) liquid hardly compresses: small volume, big pressure rise
        self.sync(self.c(4, "وَالسَّائِلُ"))
        self.say("liquid: little volume, big pressure rise", y=-3.5)
        for p in D.STROKE_DEMO_BAR[1:]:
            self.play(pm.lever.animate.set_value(0.0), flow(inlet), run_time=0.5)
            self.play(pm.lever.animate.set_value(1.0), flow(outlet), pm.press.animate.set_value(p),
                      run_time=0.7)
        # 4) high-pressure position: shorter stroke
        self.sync(self.c(4, "وَإِذَا ثَقُلَ"))
        self.say("heavy → High = short stroke", y=-3.5)
        self.play(pm.high.animate.set_value(1), run_time=0.5)
        self.play(pm.lever.animate.set_value(0.6), run_time=0.5)
        self.play(pm.lever.animate.set_value(1.0), flow(outlet),
                  pm.press.animate.set_value(D.STROKE_DEMO_BAR[-1] + D.FINE_STEP_BAR * 3), run_time=0.7)
        self.play(FadeOut(VGroup(cv1_lab, cv2_lab, cv1_link, cv2_link)),
                  pm.cv2.animate.set_color(INK), run_time=0.4)
        # 5) the fine adjust: a small screw piston
        self.sync(self.c(4, "أَمَّا مُعَدِّلُ"))
        box = SurroundingRectangle(pm.plunger, color=MOVE, buff=0.12, corner_radius=0.08, stroke_width=4)
        self.say("fine adjust = small screw piston", y=-3.5)
        self.play(Create(box), run_time=0.5)
        base = pm.press.get_value()
        self.sync(self.c(4, "تُدْخِلُهُ"))
        self.play(pm.fine.animate.set_value(0.9), pm.press.animate.set_value(base + D.FINE_STEP_BAR),
                  run_time=1.0)
        self.sync(self.c(4, "وَتُخْرِجُهُ"))
        self.play(pm.fine.animate.set_value(0.2), pm.press.animate.set_value(base - D.FINE_STEP_BAR),
                  run_time=1.0)
        self.play(FadeOut(box), run_time=0.3)
        # 6) without it: oscillating around the point, overshoot on the way up
        self.sync(self.c(4, "وَبِدُونِهِ"))
        frame = Rectangle(width=3.0, height=1.5, color=GREY_INK, stroke_width=2).move_to([5.2, -2.35, 0])
        ty = frame.get_top()[1] - 0.45
        target = DashedLine([frame.get_left()[0] + 0.05, ty, 0], [frame.get_right()[0] - 0.05, ty, 0],
                            color=INK, stroke_width=2)
        x0 = frame.get_left()[0] + 0.1
        zig = VMobject(color=BAD, stroke_width=4).set_points_as_corners(
            [np.array([x0 + dx, ty + dy, 0]) for dx, dy in
             [(0, -0.9), (0.5, 0.3), (0.95, -0.3), (1.4, 0.25), (1.85, -0.2), (2.3, 0.15), (2.75, -0.1)]])
        z_lab = tag("no fine adjust:\nswinging around\nthe point (dashed)", FS_TAG, BAD) \
            .next_to(frame, UP, buff=0.15).align_to(frame, RIGHT)
        t_lab = VMobject()
        self.say("without it: overshoot", y=-3.5)
        self.play(Create(frame), Create(target), FadeIn(t_lab), FadeIn(z_lab), run_time=0.6)
        self.play(Create(zig), run_time=1.6)
        self.sync(self.end(4) - 0.5)
        self.play(FadeOut(VGroup(frame, target, t_lab, zig, z_lab)), FadeOut(self.caption), run_time=0.5)
        self.caption = VMobject()

    # ---------------- Segment 5: preparation, bleeding the air ----------------
    def seg5_prepare(self, pm):
        section_title(self, "Preparation: fill and bleed", prev=self.sec)
        self.play(pm.level.animate.set_value(0.15), pm.press.animate.set_value(0),
                  pm.lever.animate.set_value(0), pm.high.animate.set_value(0), run_time=0.8)
        # fill between 2/3 and 3/4
        lo = pm.res.get_bottom()[1] + pm.res.height * 2 / 3
        hi = pm.res.get_bottom()[1] + pm.res.height * 3 / 4
        band = VGroup(Line([pm.res.get_left()[0], lo, 0], [pm.res.get_right()[0], lo, 0]),
                      Line([pm.res.get_left()[0], hi, 0], [pm.res.get_right()[0], hi, 0])) \
            .set_stroke(GOOD, 3)
        b_lab = tag(f"fill {D.PGHH_FILL[0]} … {D.PGHH_FILL[1]}", FS_TAG, GOOD) \
            .next_to(pm.res, LEFT, buff=0.3)
        self.sync(self.c(5, "امْلَأِ"))
        self.play(Create(band), FadeIn(b_lab), run_time=0.6)
        self.play(pm.level.animate.set_value(0.71), run_time=1.4)
        # bleed: hose on the pump, free end over a tray
        hose = VMobject(color=INK, stroke_width=7).set_points_smoothly(
            [P(2.45, 0.05), P(3.4, 0.0), P(3.9, -0.8), P(4.1, -1.7)])
        tray = VGroup(Line(P(3.6, -2.25), P(4.6, -2.25)), Line(P(3.6, -2.25), P(3.55, -1.95)),
                      Line(P(4.6, -2.25), P(4.65, -1.95))).set_stroke(GREY_INK, 3)
        bubbles = VGroup(*[Circle(radius=0.07, color=AIR, stroke_width=2).set_fill(WHITE, 1)
                           .move_to(hose.point_from_proportion(a)) for a in (0.25, 0.5, 0.75)])
        free = tag("free end", FS_TAG).next_to(tray, DOWN, buff=0.2)
        self.sync(self.c(5, "اطْرُدِ"))
        self.play(Create(hose), Create(tray), FadeIn(bubbles), FadeIn(free), run_time=1.0)
        self.sync(self.c(5, "وَمُعَدِّلُ الحَجْمِ"))
        self.play(pm.fine.animate.set_value(1.0), Indicate(pm.plunger, color=MOVE), run_time=0.8)
        self.sync(self.c(5, "وَالتَّنْفِيسُ"))
        closed = tag("closed", FS_TAG, GOOD).next_to(pm.vent, UP, buff=0.35)
        self.play(pm.vent.animate.set_color(GOOD), FadeIn(closed), run_time=0.5)
        self.sync(self.c(5, "وَاضْخَخْ"))
        drops = VGroup()
        for k in range(3):
            self.play(pm.lever.animate.set_value(1), run_time=0.3)
            b = bubbles[2 - k] if k < 3 else None
            d = Dot(hose.get_end(), radius=0.06, color=FLUID)
            drops.add(d)
            anims = [pm.lever.animate.set_value(0), d.animate.shift(DOWN * 0.45)]
            if b is not None:
                anims.append(b.animate.move_to(hose.get_end()).set_opacity(0))
            self.play(*anims, run_time=0.35)
        self.play(hose.animate.set_color(FLUID), run_time=0.3)
        # connect to the transmitter
        self.sync(self.c(5, "ثُمَّ صِلْهُ"))
        xm = transmitter().move_to(P(4.3, 0.35))
        hose2 = VMobject(color=FLUID, stroke_width=7).set_points_smoothly(
            [P(2.45, 0.05), P(3.2, 0.05), xm.port_point()])
        self.play(FadeOut(VGroup(tray, drops, free, bubbles)), FadeIn(xm), Transform(hose, hose2),
                  run_time=1.0)
        self.xm, self.hose = xm, hose
        # 50 bar, vent, 2–3 times
        self.sync(self.c(5, "بَعْدَهَا"))
        count = tag(f"× {D.PGHH_BLEED_REPEAT[0]}–{D.PGHH_BLEED_REPEAT[1]}", FS_LABEL, MOVE) \
            .next_to(pm.ext, UP, buff=0.25)
        for k in range(2):
            self.play(pm.lever.animate.set_value(1), pm.press.animate.set_value(D.PGHH_BLEED_BAR),
                      run_time=0.9)
            self.play(pm.vent.animate.set_color(BAD), flow(pm.paths()[2]),
                      pm.press.animate.set_value(0), pm.lever.animate.set_value(0), run_time=0.8)
            self.play(pm.vent.animate.set_color(GOOD), run_time=0.2)
            if k == 0:
                self.play(FadeIn(count), run_time=0.3)
        # liquid only: a bubble compresses
        self.sync(self.c(5, "فَنِظَامُ"))
        rule = tag("liquid only — no gas", FS_LABEL, FLUID, weight=BOLD).to_edge(DOWN, buff=0.45) \
            .shift(RIGHT * 2.3)
        self.play(FadeIn(rule), FadeOut(closed), run_time=0.5)
        self.sync(self.c(5, "فُقَاعَةَ"))
        ring = Circle(radius=0.75, color=GREY_INK, stroke_width=3).set_fill(WHITE, 1).move_to([5.3, -1.35, 0])
        sect = VGroup(Line(ring.get_center() + np.array([-0.7, 0.3, 0]), ring.get_center() + np.array([0.7, 0.3, 0])),
                      Line(ring.get_center() + np.array([-0.7, -0.3, 0]), ring.get_center() + np.array([0.7, -0.3, 0]))) \
            .set_stroke(INK, 4)
        liq = Rectangle(width=1.4, height=0.6, stroke_width=0).set_fill(FLUID_FILL, 1).move_to(ring)
        bub = Circle(radius=0.26, color=AIR, stroke_width=3).set_fill(WHITE, 1).move_to(ring)
        link = DashedLine(ring.get_top(), hose.point_from_proportion(0.6), color=GREY_INK, stroke_width=2)
        b_note = tag("gas bubble compresses:\nslow settling, looks like a leak", FS_TAG, BAD) \
            .next_to(rule, UP, buff=0.25)
        b_note.align_to([6.6, 0, 0], RIGHT)
        self.play(FadeIn(ring), FadeIn(liq), Create(sect), FadeIn(bub), Create(link), run_time=0.6)
        self.play(bub.animate.scale(D.BUBBLE_SHRINK), pm.press.animate.set_value(D.PGHH_BLEED_BAR * 0.6),
                  pm.lever.animate.set_value(1), FadeIn(b_note), run_time=1.4)
        self.sync(self.end(5) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 6: reaching the point ----------------
    def seg6_point(self):
        section_title(self, "Reaching the point", prev=self.sec)
        ox, oy, w, h = -5.6, -2.3, 11.6, 4.6
        ax = VGroup(Arrow([ox, oy, 0], [ox + w, oy, 0], buff=0, stroke_width=3, color=INK,
                          max_tip_length_to_length_ratio=0.02),
                    Arrow([ox, oy, 0], [ox, oy + h, 0], buff=0, stroke_width=3, color=INK,
                          max_tip_length_to_length_ratio=0.03))
        xl = tag("time", FS_AXIS).next_to(ax[0], DOWN, buff=0.15).align_to(ax[0], RIGHT)
        yl = tag("pressure", FS_AXIS).next_to(ax[1], RIGHT, buff=0.15).align_to(ax[1], UP)
        ty = oy + 3.4
        target = DashedLine([ox, ty, 0], [ox + w - 0.3, ty, 0], color=INK, stroke_width=2)
        t_lab = tag("calibration point", FS_TAG).next_to(target, UP, buff=0.08).align_to(target, RIGHT)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(target), FadeIn(t_lab), run_time=0.8)

        def steps(x0, y0, n, dx, dy):
            pts = [[x0, y0, 0]]
            for _ in range(n):
                x, y = pts[-1][0], pts[-1][1]
                pts += [[x + dx * 0.4, y + dy, 0], [x + dx, y + dy, 0]]
            return pts

        prime = steps(ox, oy, 4, 0.45, 0.55)
        hi_ = steps(prime[-1][0], prime[-1][1], 3, 0.35, 0.22)
        x, y = hi_[-1][0], hi_[-1][1]
        fine = [[x, y, 0], [x + 1.0, ty - 0.05, 0], [x + 1.3, ty, 0]]
        c_prime = VMobject(color=MOVE, stroke_width=4).set_points_as_corners([np.array(p) for p in prime])
        c_high = VMobject(color=MOVE, stroke_width=4).set_points_as_corners([np.array(p) for p in hi_])
        c_fine = VMobject(color=GOOD, stroke_width=5).set_points_smoothly([np.array(p) for p in fine])
        l_prime = tag("Prime: full strokes", FS_TAG, MOVE).next_to(c_prime, RIGHT, buff=0.15) \
            .shift(DOWN * 0.5)
        l_high = tag("High: short strokes", FS_TAG, MOVE).next_to(c_high, RIGHT, buff=0.15) \
            .shift(DOWN * 0.35)
        l_fine = tag("fine adjust, from below", FS_TAG, GOOD).move_to([0, ty + 0.45, 0]) \
            .align_to([ox + 0.4, 0, 0], LEFT)
        self.sync(self.c(6, "ابْدَأْ"))
        self.play(Create(c_prime), FadeIn(l_prime), run_time=1.6)
        self.sync(self.c(6, "فَانْتَقِلْ"))
        self.play(Create(c_high), FadeIn(l_high), run_time=1.2)
        self.sync(self.c(6, "اقْتَرِبْ"))
        self.play(Create(c_fine), FadeIn(l_fine), run_time=1.4)
        eye = VGroup(icon("eye", INK, 0.45), tag("watch the indicator", FS_TAG)).arrange(RIGHT, buff=0.12) \
            .next_to(yl, RIGHT, buff=0.6)
        self.sync(self.c(6, "وَعَيْنُكَ"))
        self.play(FadeIn(eye), run_time=0.5)
        # settle: small sag (heat / hose), wait 2–5 min, re-trim
        x1 = fine[-1][0]
        sag = [[x1, ty, 0], [x1 + 0.5, ty - 0.22, 0], [x1 + 1.3, ty - 0.3, 0], [x1 + 2.2, ty - 0.31, 0]]
        c_sag = VMobject(color=MOVE, stroke_width=4).set_points_smoothly([np.array(p) for p in sag])
        s_lab = tag("small sag: heat, hose stretch", FS_TAG, MOVE).next_to(l_fine, RIGHT, buff=0.5)
        self.sync(self.c(6, "بَعْدَ التَّوْلِيدِ"))
        self.play(Create(c_sag), FadeIn(s_lab), run_time=1.4)
        wait = tag(f"wait {D.PGHH_WAIT_MIN[0]}–{D.PGHH_WAIT_MIN[1]} min, then re-trim", FS_TAG, GOOD)
        x2 = sag[-1][0]
        retrim = VMobject(color=GOOD, stroke_width=5).set_points_as_corners(
            [np.array(p) for p in [[x2, ty - 0.31, 0], [x2 + 0.25, ty, 0], [x2 + 1.3, ty, 0]]])
        wait.move_to([0, ty + 0.95, 0]).align_to([x2 - 0.3, 0, 0], LEFT)
        self.sync(self.c(6, "فَانْتَظِرْ"))
        self.play(FadeIn(wait), run_time=0.5)
        self.play(Create(retrim), run_time=0.8)
        # steady drop: a leak
        leak = DashedLine([x1, ty, 0], [x1 + 3.7, ty - 1.6, 0], color=BAD, stroke_width=4)
        l_leak = tag("steady drop = leak: vent, check fittings and seals", FS_TAG, BAD) \
            .next_to(leak.get_end(), DOWN, buff=0.2).align_to(ax[0], RIGHT)
        self.sync(self.c(6, "فَإِنِ اسْتَمَرَّ"))
        self.play(Create(leak), run_time=1.2)
        self.play(FadeIn(l_leak), run_time=0.5)
        self.sync(self.end(6) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 7: lowering, fluids, gas service ----------------
    def seg7_lower(self):
        pm = self.pump
        section_title(self, "Lowering the pressure · fluids", prev=self.sec)
        pm.press.set_value(D.STROKE_DEMO_BAR[-1])
        pm.fine.set_value(0.9)
        pm.lever.set_value(0)
        pm.vent.set_color(INK)
        for m in pm.moving():
            m.update()
        self.play(FadeIn(pm.static()), FadeIn(pm.moving()), run_time=0.6)
        self.sync(self.c(7, "اسْتَعْمِلْ"))
        l1 = tag("1  fine adjust out", FS_TAG + 2, GOOD).move_to([4.6, -1.15, 0]).align_to([3.4, 0, 0], LEFT)
        self.play(FadeIn(l1), run_time=0.4)
        self.play(pm.fine.animate.set_value(0.1), pm.press.animate.set_value(D.STROKE_DEMO_BAR[-1]
                                                                             - 2 * D.FINE_STEP_BAR),
                  run_time=1.6)
        self.sync(self.c(7, "وَافْتَحِ"))
        l2 = tag("2  vent: carefully", FS_TAG + 2, MOVE).next_to(l1, DOWN, buff=0.15).align_to(l1, LEFT)
        self.play(FadeIn(l2), pm.vent.animate.set_color(MOVE), flow(pm.paths()[2]),
                  pm.press.animate.set_value(0), run_time=2.2, rate_func=smooth)
        self.sync(self.c(7, "وَلَا تَفُكَّهُ"))
        l3 = tag("never unscrew fully", FS_TAG + 2, BAD).next_to(l2, DOWN, buff=0.15).align_to(l1, LEFT)
        stem = VGroup(Line(ORIGIN, UP * 0.7, stroke_width=6, color=INK),
                      RoundedRectangle(width=0.5, height=0.2, corner_radius=0.05, color=INK,
                                       stroke_width=3).set_fill(INK, 1).shift(UP * 0.8),
                      Dot(DOWN * 0.15, radius=0.08, color=INK)).scale(1.3).next_to(pm.vent, UP, buff=0.3)
        x = cross(stem)
        self.play(FadeIn(l3), FadeIn(stem), run_time=0.5)
        self.play(stem[:2].animate.shift(UP * 0.15), stem[2].animate.shift(DOWN * 0.1), Create(x),
                  run_time=0.8)
        self.sync(self.c(7, "وَالسَّوَائِلُ") - 0.5)
        self.clear(self.sec)
        # the two allowed fluids
        b1, b2, b3 = bottle("#e8d49a"), bottle(FLUID_FILL), bottle("#d9c2e8")
        for b in (b1, b2, b3):
            b.scale(1.4)
        row = VGroup(b1, b2, b3).arrange(RIGHT, buff=2.4).move_to([0, 0.8, 0])
        t1 = tag("mineral hydraulic oil\n(low viscosity)", FS_TAG).next_to(b1, DOWN, buff=0.25)
        t2 = tag("distilled water\ndrain after use", FS_TAG).next_to(b2, DOWN, buff=0.25)
        t3 = tag("any other fluid\ndamages the seals", FS_TAG, BAD).next_to(b3, DOWN, buff=0.25)
        ok1 = tag("✓", FS_BODY, GOOD).next_to(b1, UP, buff=0.15)
        ok2 = tag("✓", FS_BODY, GOOD).next_to(b2, UP, buff=0.15)
        self.sync(self.c(7, "زَيْتٌ"))
        self.play(FadeIn(b1), FadeIn(t1), FadeIn(ok1), run_time=0.6)
        self.sync(self.c(7, "أَوْ مَاءٌ"))
        self.play(FadeIn(b2), FadeIn(t2), FadeIn(ok2), run_time=0.6)
        self.sync(self.c(7, "وَغَيْرُهُمَا"))
        self.play(FadeIn(b3), FadeIn(t3), run_time=0.5)
        x3 = cross(b3)
        self.play(Create(x3), run_time=0.4)
        # a transmitter going back to gas service
        self.sync(self.c(7, "وَلَا يَصْلُحُ"))
        cell = RoundedRectangle(width=2.4, height=1.9, corner_radius=0.2, color=INK, stroke_width=4) \
            .move_to([0.2, 1.0, 0])
        film = VGroup(*[Dot(cell.get_center() + np.array([dx, -0.6, 0]), radius=0.09, color=FLUID)
                        for dx in (-0.75, -0.3, 0.2, 0.7)])
        c_lab = tag("transmitter chamber", FS_TAG).next_to(cell, UP, buff=0.2)
        gas = pipe(cell.get_right(), cell.get_right() + RIGHT * 3.2, color=AIR, width=8)
        g_lab = tag("gas service", FS_TAG, AIR).next_to(gas, UP, buff=0.2)
        self.play(FadeOut(VGroup(b1, b2, b3, t1, t2, t3, ok1, ok2, x3)), run_time=0.4)
        self.play(Create(cell), FadeIn(c_lab), FadeIn(film), run_time=0.7)
        self.play(Create(gas), FadeIn(g_lab), run_time=0.5)
        self.sync(self.c(7, "يَحْمِلُهُ"))
        mover = Dot(cell.get_right(), radius=0.08, color=BAD)
        self.play(MoveAlongPath(mover, gas), film[3].animate.set_color(BAD), run_time=1.2)
        self.sync(self.c(7, "أَوْ يَسْتَقِرُّ"))
        column = Rectangle(width=0.25, height=0.6, stroke_width=0).set_fill(FLUID, 0.8) \
            .next_to(cell, DOWN, buff=0).shift(LEFT * 0.6)
        leg = Line(cell.get_bottom() + LEFT * 0.6, cell.get_bottom() + LEFT * 0.6 + DOWN * 1.0,
                   stroke_width=3, color=INK)
        shift = tag("liquid column shifts the reading", FS_TAG, BAD).next_to(leg, LEFT, buff=0.3)
        self.play(Create(leg), GrowFromEdge(column, UP), FadeIn(shift), run_time=0.9)
        self.sync(self.c(7, "وَلِذٰلِكَ"))
        h_air = pipe([-6.4, -2.7, 0], [-5.2, -2.7, 0], color=AIR, width=9)
        h_liq = pipe([-5.2, -2.7, 0], [-4.0, -2.7, 0], color=FLUID, width=9)
        i_air = icon("wind", AIR, 0.38).next_to(h_air, UP, buff=0.15)
        i_liq = icon("droplet", FLUID, 0.38).next_to(h_liq, UP, buff=0.15)
        one = VGroup(h_air, h_liq, i_air, i_liq)
        rule = tag("one hose for both gas and liquid: not allowed", FS_TAG + 2, BAD) \
            .next_to(one, RIGHT, buff=0.4)
        two = VGroup(pipe([0, 0, 0], [1.0, 0, 0], color=AIR, width=9),
                     pipe([0, -0.35, 0], [1.0, -0.35, 0], color=FLUID, width=9)) \
            .next_to(rule, RIGHT, buff=0.5)
        ok = tag("✓", FS_BODY, GOOD).next_to(two, RIGHT, buff=0.15)
        self.play(Create(h_air), Create(h_liq), FadeIn(i_air), FadeIn(i_liq), run_time=0.5)
        self.play(Create(cross(VGroup(h_air, h_liq), width=5).scale(1.1)), FadeIn(rule), run_time=0.6)
        self.play(Create(two), FadeIn(ok), run_time=0.5)
        self.sync(self.end(7) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 8: safety and hoses ----------------
    def seg8_safety(self):
        section_title(self, "Safety and hoses", prev=self.sec)
        glasses = VGroup(icon("eye", INK, 0.6), tag("protective glasses", FS_LABEL)).arrange(RIGHT, buff=0.2)
        orig = VGroup(icon("shield-check", GOOD, 0.6), tag("original hose only", FS_LABEL)) \
            .arrange(RIGHT, buff=0.2)
        top = VGroup(glasses, orig).arrange(RIGHT, buff=1.2).move_to([0, 2.5, 0])
        self.sync(self.c(8, "نَظَّارَةٌ"))
        self.play(FadeIn(glasses), run_time=0.5)
        self.sync(self.c(8, "وَالخُرْطُومُ الأَصْلِيُّ"))
        self.play(FadeIn(orig), run_time=0.5)
        # overfilled reservoir overflows when the pressure is released
        res = Rectangle(width=1.6, height=1.8, color=GREY_INK, stroke_width=4).move_to([-4.6, 0.0, 0])
        maxl = DashedLine(res.get_left() + UP * 0.45, res.get_right() + UP * 0.45, color=GOOD,
                          stroke_width=3)
        max_lab = tag("max", FS_TAG, GOOD).next_to(maxl, LEFT, buff=0.15)
        lvl = ValueTracker(0.6)
        liq = always_redraw(lambda: Rectangle(width=1.6, height=1.8 * lvl.get_value(), stroke_width=0)
                            .set_fill(FLUID_FILL, 1).align_to(res, DOWN).align_to(res, LEFT))
        r_lab = tag("reservoir", FS_TAG).next_to(res, DOWN, buff=0.2)
        self.sync(self.c(8, "لَا تَمْلَأِ"))
        self.play(FadeIn(liq), Create(res), Create(maxl), FadeIn(max_lab), FadeIn(r_lab), run_time=0.7)
        add = VGroup(icon("droplet", FLUID, 0.45), tag("adding while pressurising", FS_TAG, BAD)) \
            .arrange(RIGHT, buff=0.15).next_to(res, RIGHT, buff=0.4).shift(UP * 0.6)
        self.sync(self.c(8, "وَلَا تُضِفْ"))
        self.play(FadeIn(add), lvl.animate.set_value(0.8), run_time=0.9)
        self.sync(self.c(8, "فَعِنْدَ التَّنْفِيسِ"))
        spill = VGroup(*[Dot(res.get_corner(UR) + np.array([0.12, -0.05 - 0.28 * k, 0]), radius=0.06,
                             color=BAD) for k in range(4)])
        back = tag("vent → all liquid returns → overflow, may break", FS_TAG, BAD) \
            .next_to(add, DOWN, buff=0.35).align_to(add, LEFT)
        vent = gate_valve(size=0.4).next_to(res, UP, buff=0.35)
        vl = pipe(vent.get_bottom(), res.get_top(), width=4)
        self.play(FadeIn(vent), Create(vl), run_time=0.3)
        self.play(vent.animate.set_color(MOVE), lvl.animate.set_value(1.0), res.animate.set_color(BAD),
                  FadeIn(back), run_time=0.8)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(d), d.animate.shift(DOWN * 0.6)) for d in spill],
                              lag_ratio=0.3), run_time=1.0)
        # strong counterforce without a pressure rise: stop
        self.sync(self.c(8, "وَمُقَاوَمَةٌ"))
        gauge = Rectangle(width=1.6, height=0.6, color=INK, stroke_width=3).move_to([-4.2, -2.6, 0])
        g_txt = tag(f"{fmt(D.STROKE_DEMO_BAR[1])} bar", FS_TAG + 2).move_to(gauge)
        push = Arrow([-2.2, -2.6, 0], [-2.2, -2.6, 0] + UP * 0.1, buff=0, stroke_width=8, color=BAD,
                     max_tip_length_to_length_ratio=0.35)
        push_lab = tag("hand force", FS_TAG, BAD).next_to(push, RIGHT, buff=0.2)
        stop = VGroup(icon("alert-triangle", BAD, 0.6),
                      tag("strong resistance, no pressure rise:\nstop and find the fault", FS_TAG, BAD)) \
            .arrange(RIGHT, buff=0.2).move_to([2.4, -2.5, 0])
        self.play(Create(gauge), FadeIn(g_txt), GrowArrow(push), run_time=0.4)
        self.play(push.animate.put_start_and_end_on([-2.2, -3.1, 0], [-2.2, -1.9, 0]), FadeIn(push_lab),
                  Indicate(g_txt, color=BAD), run_time=1.0)
        self.play(FadeIn(stop), run_time=0.5)
        self.sync(self.c(8, "وَلِكُلِّ مَدًى") - 0.4)
        self.play(FadeOut(VGroup(res, maxl, max_lab, liq, r_lab, add, spill, back, stop, top, vent, vl,
                                 gauge, g_txt, push, push_lab)), run_time=0.4)
        # hose ratings
        def hose(y, color, width):
            return VMobject(color=color, stroke_width=width).set_points_smoothly(
                [np.array(p) for p in [[-5.6, y, 0], [-4.2, y + 0.25, 0], [-2.8, y - 0.2, 0], [-1.6, y, 0]]])
        hl = hose(1.5, INK, 6)
        hh = hose(0.1, INK, 10)
        tl = tag(f"{D.HOSE_LOW_BAR} bar hose · {D.HOSE_LOW_FITTING} fittings\nlow and medium ranges", FS_TAG) \
            .next_to(hl, RIGHT, buff=0.3)
        th = tag(f"{D.PGHH_HOSE_BAR} bar hose · {D.HOSE_HIGH_FITTING} fittings\nhigh range", FS_TAG) \
            .next_to(hh, RIGHT, buff=0.3)
        self.play(Create(hl), FadeIn(tl), run_time=0.7)
        self.sync(self.c(8, "وَسِتُّمِئَةٍ"))
        self.play(Create(hh), FadeIn(th), run_time=0.7)
        self.sync(self.c(8, "وَخُرْطُومُ عِشْرِينَ"))
        bad = hose(-1.3, INK, 6)
        bulge = Ellipse(width=0.7, height=0.45, color=BAD, stroke_width=5).move_to(bad.point_from_proportion(0.5))
        tb = tag(f"{D.BAD_HOSE_BAR} bar hose on a {D.HOSE_LOW_BAR} bar system:\na time bomb", FS_TAG, BAD) \
            .next_to(bad, RIGHT, buff=0.3)
        self.play(Create(bad), FadeIn(tb), run_time=0.6)
        self.play(GrowFromCenter(bulge), bad.animate.set_color(BAD), run_time=0.7)
        # adapters: each one a possible leak
        self.sync(self.c(8, "وَكُلُّ مُحَوِّلٍ"))
        chain = VGroup(*[Rectangle(width=0.5, height=0.32, color=INK, stroke_width=3).set_fill(PANEL_FILL, 1)
                         for _ in range(4)]).arrange(RIGHT, buff=0.15).move_to([-4.1, -2.7, 0])
        links = VGroup(*[Line(chain[i].get_right(), chain[i + 1].get_left(), stroke_width=5, color=INK)
                         for i in range(3)])
        drops = VGroup(*[Dot(l.get_center() + DOWN * 0.3, radius=0.06, color=BAD) for l in links])
        tc = tag("every extra adapter = a possible leak → shortest chain", FS_TAG) \
            .next_to(chain, RIGHT, buff=0.4)
        self.play(FadeIn(chain), Create(links), run_time=0.6)
        self.play(FadeIn(drops, lag_ratio=0.3), FadeIn(tc), run_time=0.9)
        self.sync(self.end(8) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 9: pneumatic pumps ----------------
    def seg9_pneumatic(self):
        section_title(self, "Pneumatic hand pumps", prev=self.sec)
        # air pump: cylinder, piston, check valve, air particles
        cyl = VGroup(Line([-6.2, 1.9, 0], [-3.6, 1.9, 0]), Line([-6.2, 1.1, 0], [-3.6, 1.1, 0]),
                     Line([-3.6, 1.9, 0], [-3.6, 1.1, 0])).set_stroke(INK, 4)
        px = ValueTracker(-5.9)
        piston = always_redraw(lambda: Rectangle(width=0.22, height=0.8, color=MOVE, stroke_width=3)
                               .set_fill(MOVE, 1).move_to([px.get_value(), 1.5, 0]))
        cv = check_valve(size=0.42).move_to([-3.1, 1.5, 0])
        out = pipe([-3.6, 1.5, 0], cv.get_left(), width=6)
        out2 = pipe(cv.get_right(), [-1.9, 1.5, 0], width=6)
        heat = ValueTracker(0.0)
        dots = always_redraw(lambda: VGroup(*[
            Dot([px.get_value() + 0.25 + (k % 4) * (-3.75 - px.get_value() - 0.25) / 3.5,
                 1.3 + (k // 4) * 0.4, 0], radius=0.05,
                color=interpolate_color(ManimColor(AIR), ManimColor(MOVE), heat.get_value()))
            for k in range(8)]))
        lab = tag("piston + check valve", FS_TAG).next_to(cyl, DOWN, buff=0.25)
        self.sync(self.c(9, "مِكْبَسٌ"))
        self.play(Create(cyl), FadeIn(piston), Create(out), FadeIn(cv), Create(out2), FadeIn(dots),
                  FadeIn(lab), run_time=0.9)
        self.play(px.animate.set_value(-4.3), flow(out2, AIR), run_time=0.8)
        # PGC: pressure / vacuum selector; pump to ~20–25 bar, then fine adjust
        self.sync(self.c(9, "فِي بِي جِي سِي"))
        words = VGroup(tag("pressure", FS_TAG), tag("vacuum", FS_TAG)).arrange(RIGHT, buff=0.35)
        pill = SurroundingRectangle(words, buff=0.15, corner_radius=0.25, color=INK, stroke_width=3)
        sel = VGroup(pill, words)
        pgc = tag("PGC", FS_LABEL, AIR, weight=BOLD).next_to(sel, LEFT, buff=0.3)
        lock = VGroup(icon("lock", BAD, 0.4), tag("never switch under pressure", FS_TAG, BAD)) \
            .arrange(RIGHT, buff=0.15).next_to(sel, RIGHT, buff=0.3)
        fit(VGroup(pgc, sel, lock), 9.0).move_to([2.4, 2.45, 0])
        self.play(FadeIn(pgc), FadeIn(sel), run_time=0.5)
        self.sync(self.c(9, "لَا يُغَيَّرُ"))
        self.play(FadeIn(lock), run_time=0.4)
        self.sync(self.c(9, "وَالضَّخُّ"))
        x0, x1 = -0.2, 5.6
        strip = Line([x0, 1.3, 0], [x1, 1.3, 0], stroke_width=3, color=INK)
        f = lambda p: x0 + (x1 - x0) * p / _P["PGC"][1]                       # noqa: E731
        pumped = Rectangle(width=f(D.PGC_PUMP_MAX_BAR[1]) - x0, height=0.3, stroke_width=0) \
            .set_fill(AIR, 0.7).move_to([(x0 + f(D.PGC_PUMP_MAX_BAR[1])) / 2, 1.3, 0])
        finead = Rectangle(width=x1 - f(D.PGC_PUMP_MAX_BAR[1]), height=0.3, stroke_width=0) \
            .set_fill(MOVE, 0.7).move_to([(x1 + f(D.PGC_PUMP_MAX_BAR[1])) / 2, 1.3, 0])
        lp = tag(f"pumping: up to about {D.PGC_PUMP_MAX_BAR[0]}–{D.PGC_PUMP_MAX_BAR[1]} bar", FS_TAG, AIR) \
            .next_to(pumped, DOWN, buff=0.2).align_to(pumped, LEFT)
        lf = tag(f"fine adjust to {_P['PGC'][1]}", FS_TAG, MOVE).next_to(finead, UP, buff=0.2) \
            .align_to(finead, RIGHT)
        tks = VGroup(*[VGroup(Line([f(v), 1.1, 0], [f(v), 1.5, 0], stroke_width=2, color=INK))
                       for v in (0, D.PGC_PUMP_MAX_BAR[1], _P["PGC"][1])])
        t0 = tag("0", FS_TAG).next_to([f(0), 1.5, 0], UP, buff=0.08)
        self.play(Create(strip), Create(tks), FadeIn(t0), GrowFromEdge(pumped, LEFT), FadeIn(lp), run_time=0.8)
        self.play(GrowFromEdge(finead, LEFT), FadeIn(lf), run_time=0.6)
        # PGPH: pump → close the shut-off valve → adjust with the wheel
        self.sync(self.c(9, "وَفِي بِي جِي بِي إِتْش") - 0.2)
        ph = tag("PGPH", FS_LABEL, AIR, weight=BOLD).move_to([-5.5, -0.2, 0])
        self.play(FadeIn(ph), run_time=0.3)
        flow_ = process_flow(self, ["pump", "close shut-off valve", "adjust with the wheel"],
                             cues=[self.c(9, "اضْخَخْ"), self.c(9, "ثُمَّ أَغْلِقْ"),
                                   self.c(9, "ثُمَّ اضْبِطْ")], size=FS_TAG + 2, width=9.0,
                             pos=[1.3, -0.2, 0])
        # heat of compression: air warms, cools, the pressure sags; liquid hardly
        self.sync(self.c(9, "لٰكِنَّهُ يَسْخُنُ"))
        self.play(heat.animate.set_value(1), px.animate.set_value(-4.0), run_time=0.9)
        ox, oy = -1.5, -3.1
        ax = VGroup(Line([ox, oy, 0], [ox + 5.8, oy, 0]), Line([ox, oy, 0], [ox, oy + 1.9, 0])) \
            .set_stroke(INK, 3)
        yl = tag("pressure", FS_TAG).next_to(ax[1], LEFT, buff=0.15).align_to(ax[1], UP)
        xl = tag("time", FS_TAG).next_to(ax[0], RIGHT, buff=0.15)
        ts = np.linspace(0, 1, 30)
        air_c = VMobject(color=AIR, stroke_width=4).set_points_smoothly(
            [np.array([ox + 5.6 * t, oy + 1.6 - 0.7 * (1 - np.exp(-t / 0.18)), 0]) for t in ts])
        liq_c = VMobject(color=FLUID, stroke_width=4).set_points_smoothly(
            [np.array([ox + 5.6 * t, oy + 1.6 - 0.1 * (1 - np.exp(-t / 0.18)), 0]) for t in ts])
        la = tag("air", FS_TAG, AIR).next_to(air_c.get_end(), RIGHT, buff=0.1)
        ll = tag("liquid", FS_TAG, FLUID).next_to(liq_c.get_end(), RIGHT, buff=0.1)
        self.sync(self.c(9, "فَإِذَا بَرَدَ"))
        self.play(Create(ax), FadeIn(yl), FadeIn(xl), run_time=0.4)
        self.play(Create(air_c), heat.animate.set_value(0), FadeIn(la), run_time=1.4)
        wt = tag(f"wait {D.AIR_WAIT_S[0]}–{D.AIR_WAIT_S[1]} s", FS_TAG, GOOD).next_to(ax[0], UP, buff=1.95) \
            .align_to(ax[0], RIGHT)
        self.sync(self.c(9, "فَانْتَظِرْ"))
        self.play(FadeIn(wt), run_time=0.4)
        self.sync(self.c(9, "وَهٰذَا الأَثَرُ"))
        self.play(Create(liq_c), FadeIn(ll), run_time=1.0)
        self.sync(self.end(9) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 10: automatic generation ----------------
    def seg10_auto(self):
        section_title(self, "Automatic generation", prev=self.sec)
        epg = RoundedRectangle(width=3.4, height=1.6, corner_radius=0.18, color=INK, stroke_width=4) \
            .set_fill(WHITE, 1).move_to([-3.4, 0.9, 0])
        e_lab = tag("ePG", FS_BODY, weight=BOLD).move_to(epg.get_center() + UP * 0.35)
        bat = icon("battery", INK, 0.5).move_to(epg.get_center() + DOWN * 0.35 + LEFT * 0.95)
        e_rng = tag(f"{fmt(D.EPG_RANGE[0], 2)} … {D.EPG_RANGE[1]} bar", FS_TAG) \
            .next_to(epg, DOWN, buff=0.25)
        e_sub = tag("battery", FS_TAG, GREY_INK).next_to(bat, RIGHT, buff=0.15)
        self.sync(self.c(10, "إِي بِي جِي"))
        self.play(Create(epg), FadeIn(e_lab), FadeIn(bat), FadeIn(e_sub), FadeIn(e_rng), run_time=0.9)
        mc6 = RoundedRectangle(width=2.2, height=1.6, corner_radius=0.18, color=INK, stroke_width=4) \
            .set_fill(WHITE, 1).move_to([2.2, 0.9, 0])
        m_lab = tag("MC6", FS_BODY, weight=BOLD).move_to(mc6)
        self.sync(self.c(10, "يُعْطِيهَا"))
        self.play(Create(mc6), FadeIn(m_lab), run_time=0.6)
        sp = Arrow(mc6.get_left(), epg.get_right(), buff=0.15, stroke_width=4, color=MOVE,
                   max_tip_length_to_length_ratio=0.12)
        sp_lab = tag("set point", FS_TAG, MOVE).next_to(sp, UP, buff=0.12)
        self.play(GrowArrow(sp), FadeIn(sp_lab), run_time=0.6)
        auto = tag("regulates by itself: fully automatic", FS_TAG, GOOD).next_to(epg, UP, buff=0.2)
        self.sync(self.c(10, "فَتَضْبِطُهَا"))
        self.play(FadeIn(auto), Indicate(epg, color=GOOD), run_time=0.8)
        self.sync(self.c(10, "وَتَعْمَلُ مَعَ"))
        any_ = tag("also with any other calibrator\n(in place of a hand pump)", FS_TAG) \
            .next_to(e_rng, DOWN, buff=0.2).align_to(epg, LEFT)
        self.play(FadeIn(any_), run_time=0.5)
        self.sync(self.c(10, "وَبِي أُو سِي"))
        poc = RoundedRectangle(width=2.6, height=1.3, corner_radius=0.15, color=INK, stroke_width=4) \
            .set_fill(WHITE, 1).move_to([-3.2, -2.3, 0])
        p_lab = tag("POC8", FS_BODY, weight=BOLD).move_to(poc)
        p_rng = tag(f"automatic controller · vacuum … {D.POC8_MAX_BAR} bar", FS_TAG) \
            .next_to(poc, RIGHT, buff=0.4).shift(UP * 0.25)
        self.play(Create(poc), FadeIn(p_lab), FadeIn(p_rng), run_time=0.8)
        self.sync(self.c(10, "مِنْضَدِيٌّ"))
        p_where = VGroup(icon("building-factory", INK, 0.45), tag("bench, or built into a CENTRiCAL workshop bench",
                                                                  FS_TAG)).arrange(RIGHT, buff=0.15) \
            .next_to(p_rng, DOWN, buff=0.25).align_to(p_rng, LEFT)
        self.play(FadeIn(p_where), run_time=0.6)
        self.sync(self.end(10) - 0.2)
        self.clear(self.sec)
        steps = ["choose medium\nand range", "fill, bleed:\nliquid only", "approach\nfrom below",
                 "fine adjust", "wait, then\nre-trim"]
        process_flow(self, steps, size=FS_TAG + 2, width=12.4)
        self.wait(3.2)


if __name__ == "__main__":
    main(__file__, "PtCalEp02", NARRATION)
