"""rt_intro: industrial radiography — the principle and geometric unsharpness (single episode).

Every number on screen or in the narration comes from rt_intro_data. Sources and the owner's
decisions: sources/rt_intro_principle.md and CLAUDE.md in this folder; storyboard in
storyboard/rt_intro_principle.md.

Build (from the repo root):
    python projects/rt_intro/rt_intro_principle.py --preview   # 480p15 -> tmp/rt_intro_principle/preview.mp4
    python projects/rt_intro/rt_intro_principle.py             # 1080p30 -> output/rt_intro_principle.mp4
"""
from explainer import *
import rt_intro_data as D

# Fully diacritized narration (owner-approved 2026-09-27) — one entry per scene.
NARRATION = [
    # 1 disclaimer + what RT is and why
    "هٰذِهِ مَادَّةٌ تَعْلِيمِيَّةٌ؛ وَالمَرْجِعُ المُلْزِمُ هُوَ الوَثَائِقُ الرَّسْمِيَّةُ وَالإِجْرَاءَاتُ المُعْتَمَدَةُ. التَّصْوِيرُ الإِشْعَاعِيُّ الصِّنَاعِيُّ، آرْ تِي، طَرِيقَةُ فَحْصٍ لَا إِتْلَافِيٍّ، تَكْشِفُ العُيُوبَ الدَّاخِلِيَّةَ فِي القِطْعَةِ دُونَ إِتْلَافِهَا، مِثْلَ المَسَامِيَّةِ، وَشَوَائِبِ الخَبَثِ، وَعَدَمِ الانْصِهَارِ، وَالشُّقُوقِ فِي اللِّحَامَاتِ. تَمُرُّ الأَشِعَّةُ عَبْرَ القِطْعَةِ، وَتَسْقُطُ عَلَى فِيلْمٍ أَوْ كَاشِفٍ خَلْفَهَا، فَتَتَكَوَّنُ صُورَةٌ ظِلِّيَّةٌ لِدَاخِلِ القِطْعَةِ. وَمِنْ مَزَايَاهُ أَنَّهُ يُعْطِي سِجِلًّا دَائِمًا، يُمْكِنُ مُرَاجَعَتُهُ لَاحِقًا.",
    # 2 differential absorption
    "الأَشِعَّةُ السِّينِيَّةُ وَأَشِعَّةُ غَامَا مَوْجَاتٌ كَهْرُومِغْنَاطِيسِيَّةٌ، طُولُهَا المَوْجِيُّ قَصِيرٌ جِدًّا، فَتَنْفُذُ فِي المَعَادِنِ. وَيَمْتَصُّ المَعْدِنُ جُزْءًا مِنْهَا، يَزْدَادُ بِزِيَادَةِ سَمَاكَتِهِ وَكَثَافَتِهِ. فَحَيْثُ يُوجَدُ فَرَاغٌ دَاخِلِيٌّ، كَمَسَامَةٍ أَوْ شَقٍّ، تَقِلُّ السَّمَاكَةُ الفِعْلِيَّةُ لِلْمَعْدِنِ فِي مَسَارِ الشُّعَاعِ، فَيَصِلُ إِلَى الفِيلْمِ إِشْعَاعٌ أَكْثَرُ، وَيَظْهَرُ مَكَانُهُ أَغْمَقَ بَعْدَ التَّحْمِيضِ. وَحَيْثُ تُوجَدُ شَائِبَةٌ أَكْثَفُ مِنَ المَعْدِنِ، مِثْلُ التَّنْغِسْتِنِ، يُمْتَصُّ إِشْعَاعٌ أَكْثَرُ، فَيَظْهَرُ مَكَانُهَا أَفْتَحَ. فَالفَرْقُ فِي الإِشْعَاعِ النَّافِذِ هُوَ الَّذِي يَرْسُمُ العَيْبَ، وَالصُّورَةُ خَرِيطَةٌ لِتَغَيُّرِ السَّمَاكَةِ وَالكَثَافَةِ دَاخِلَ القِطْعَةِ.",
    # 3 X-ray tube or Ir-192
    "وَلِلْأَشِعَّةِ مَصْدَرَانِ. جِهَازُ الأَشِعَّةِ السِّينِيَّةِ أُنْبُوبٌ تَتَسَارَعُ فِيهِ الإِلِكْتْرُونَاتُ بِجُهْدٍ عَالٍ حَتَّى تَصْطَدِمَ بِهَدَفٍ مَعْدِنِيٍّ، فَتَنْطَلِقُ الأَشِعَّةُ مِنْ مِنْطَقَةٍ صَغِيرَةٍ هِيَ البُقْعَةُ البُؤْرِيَّةُ. يَعْمَلُ بِالكَهْرَبَاءِ وَيُطْفَأُ بِإِطْفَائِهَا، وَتُضْبَطُ طَاقَةُ أَشِعَّتِهِ بِالجُهْدِ، بِالكِيلُوفُولْت. وَمَصْدَرُ غَامَا نَظِيرٌ مُشِعٌّ، كَالإِيرِيدْيُومِ مِئَةٍ وَاثْنَيْنِ وَتِسْعِينَ، فِي كَبْسُولَةٍ صَغِيرَةٍ دَاخِلَ حَاوِيَةٍ مُدَرَّعَةٍ، تُدْفَعُ إِلَى مَوْضِعِ التَّصْوِيرِ عَبْرَ أُنْبُوبِ تَوْجِيهٍ. لَا يَحْتَاجُ كَهْرَبَاءَ، وَيَسْهُلُ حَمْلُهُ إِلَى المَيْدَانِ، لٰكِنَّهُ لَا يُطْفَأُ، وَنَشَاطُهُ يَتَنَاقَصُ مَعَ الزَّمَنِ؛ فَعُمْرُ النِّصْفِ لَهُ نَحْوُ أَرْبَعَةٍ وَسَبْعِينَ يَوْمًا. وَفِي الحَالَتَيْنِ لِلْمَصْدَرِ حَجْمٌ فِعْلِيٌّ، إِفْ، وَلَيْسَ نُقْطَةً.",
    # 4 geometric unsharpness
    "لَوْ كَانَ المَصْدَرُ نُقْطَةً، لَكَانَ ظِلُّ حَافَّةِ العَيْبِ حَادًّا. لٰكِنَّ لِلْمَصْدَرِ حَجْمًا، إِفْ؛ فَكُلُّ حَافَّةٍ تُلْقِي ظِلَّيْنِ مِنْ طَرَفَيِ المَصْدَرِ، وَبَيْنَهُمَا مِنْطَقَةُ شِبْهِ ظِلٍّ تَجْعَلُ الحَافَّةَ ضَبَابِيَّةً عَلَى الفِيلْمِ. عَرْضُهَا هُوَ عَدَمُ الوُضُوحِ الهَنْدَسِيِّ، يُو جِي، وَمِنْ تَشَابُهِ المُثَلَّثَيْنِ: يُو جِي يُسَاوِي إِفْ فِي دِي الصَّغِيرَةِ، مَقْسُومًا عَلَى دِي الكَبِيرَةِ. إِفْ أَكْبَرُ بُعْدٍ مُسْقَطٍ لِلْمَصْدَرِ أَوِ البُقْعَةِ البُؤْرِيَّةِ، وَدِي الكَبِيرَةُ مِنَ المَصْدَرِ إِلَى جِهَةِ المَصْدَرِ فِي القِطْعَةِ، وَدِي الصَّغِيرَةُ مِنْ تِلْكَ الجِهَةِ إِلَى الفِيلْمِ، وَهِيَ سَمَاكَةُ القِطْعَةِ تَقْرِيبًا إِذَا كَانَ الفِيلْمُ مُلَاصِقًا. فَلِتَحْسِينِ الوُضُوحِ ثَلَاثُ طُرُقٍ: مَصْدَرٌ أَصْغَرُ، أَوْ إِبْعَادُ المَصْدَرِ، أَوْ تَقْرِيبُ الفِيلْمِ مِنَ القِطْعَةِ. وَيُوصِي القِسْمُ الخَامِسُ مِنْ كُودِ أَزْمِي بِحَدٍّ أَعْلَى لَهُ، أَمَّا الحَدُّ المُلْزِمُ فَيُحَدِّدُهُ الكُودُ المُحِيلُ أَوِ العَقْدُ.",
    # 5 worked example (numbers checked against rt_intro_data below)
    "مِثَالٌ: مَصْدَرٌ حَجْمُهُ ثَلَاثَةُ مِلِّيمِتْرَاتٍ، وَلِحَامٌ سَمَاكَتُهُ عِشْرُونَ مِلِّيمِتْرًا وَالفِيلْمُ مُلَاصِقٌ لَهُ، فَدِي الصَّغِيرَةُ عِشْرُونَ. عِنْدَ أَرْبَعِمِئَةِ مِلِّيمِتْرٍ: ثَلَاثَةٌ فِي عِشْرِينَ عَلَى أَرْبَعِمِئَةٍ، يُعْطِي صِفْرًا فَاصِلَةَ خَمْسَةَ عَشَرَ مِنَ المِلِّيمِتْرِ. وَلَوْ قَرَّبْنَا المَصْدَرَ إِلَى مِئَتَيْنِ، صَارَ صِفْرًا فَاصِلَةَ ثَلَاثِينَ؛ تَضَاعَفَ التَّشَوُّشُ حِينَ نَصَّفْنَا المَسَافَةَ. وَإِذَا أَخَذْنَا حَدًّا تَوْضِيحِيًّا قَدْرُهُ صِفْرٌ فَاصِلَةُ وَاحِدٍ وَخَمْسِينَ، وَهُوَ القِيمَةُ القُصْوَى المُوصَى بِهَا فِي أَزْمِي لِلسَّمَاكَةِ الأَقَلِّ مِنْ إِنْشَيْنِ، فَأَقَلُّ مَسَافَةٍ مَسْمُوحَةٍ: ثَلَاثَةٌ فِي عِشْرِينَ عَلَى صِفْرٍ فَاصِلَةِ وَاحِدٍ وَخَمْسِينَ، أَيْ نَحْوُ مِئَةٍ وَسَبْعَةَ عَشَرَ مِلِّيمِتْرًا وَسِتَّةِ أَعْشَارٍ.",
    # 6 summary
    "الخُلَاصَةُ: الصُّورَةُ الإِشْعَاعِيَّةُ خَرِيطَةٌ لِلسَّمَاكَةِ وَالكَثَافَةِ؛ الفَرَاغُ أَغْمَقُ، وَالشَّائِبَةُ الأَكْثَفُ أَفْتَحُ. وَالمَصْدَرُ جِهَازُ أَشِعَّةٍ سِينِيَّةٍ يُطْفَأُ، أَوْ نَظِيرٌ مُشِعٌّ مَحْمُولٌ لَا يُطْفَأُ. وَحَجْمُ المَصْدَرِ يُسَبِّبُ عَدَمَ الوُضُوحِ الهَنْدَسِيِّ، وَنُقَلِّلُهُ بِمَصْدَرٍ أَصْغَرَ، أَوْ مَسَافَةٍ أَكْبَرَ، أَوْ فِيلْمٍ مُلَاصِقٍ.",
]

# Every spoken or shown number is checked against the data module; stop if it drifts.
assert f"{D.F:.1f}" == "3.0" and f"{D.d:.0f}" == "20"                       # seg 5 "three", "twenty"
assert f"{D.D1:.0f}" == "400" and f"{D.D2:.0f}" == "200"                    # seg 5 "400", "200"
assert f"{D.UG1:.2f}" == "0.15" and f"{D.UG2:.2f}" == "0.30"                # seg 5 "0.15", "0.30"
assert round(D.UG_RATIO) == 2                                               # seg 5 "doubled"
assert f"{D.UG_MAX:.2f}" == "0.51" and f"{D.D_MIN:.1f}" == "117.6"          # seg 5 "0.51", "117.6"
assert D.IR192_HALF_LIFE_DAYS == 74                                         # seg 3 "about 74 days"

AUDIO_DIR = audio_dir_for(__file__)

# ---------------- palette roles (project CLAUDE.md) ----------------
RAY_C = ACCENT_1            # radiation
SRC_C = ACCENT_2            # the source, its size F
OK_LIM = ACCENT_3           # within the limit
DEF_C = ACCENT_4            # defects, out of limit
PLATE = "#e3e3e3"           # steel cross-section
WELD = "#cdcdcd"            # weld metal
FILM_NEW = "#f6f6f6"        # unexposed film
EXPOSED = "#4d4d4d"         # film where the full beam arrived
SHADOW = "#e9e9e9"          # film behind an opaque part


def grey(level):
    """Film tone from the share of radiation that reached it (0 → white, 1 → near black)."""
    v = int(round(245 - 200 * min(max(level, 0.0), 1.0)))
    return f"#{v:02x}{v:02x}{v:02x}"


def callout(text, target, pos, color=INK, size=FS_LABEL):
    """Label at `pos` with an arrow to the point `target` (used when the part is spoken)."""
    lab = label(text, size, color).move_to(pos)
    tgt = np.array(target, dtype=float)
    c = lab.get_center()
    v = tgt - c
    half = np.array([lab.width / 2 + 0.08, lab.height / 2 + 0.08])
    t = min(half[i] / abs(v[i]) for i in range(2) if abs(v[i]) > 1e-9)
    start = c + v * min(t, 1.0)
    arr = Arrow(start, tgt, buff=0.04, stroke_width=3, color=color,
                max_tip_length_to_length_ratio=0.18, max_stroke_width_to_length_ratio=8)
    return VGroup(lab, arr)


def bump(x0, x1, y, h, n=24):
    """Closed cap (weld reinforcement) above (h > 0) or below (h < 0) the line y."""
    xs = np.linspace(x0, x1, n)
    pts = [[x, y + h * (1 - ((2 * x - x0 - x1) / (x1 - x0)) ** 2), 0] for x in xs]
    return Polygon(*pts, color=INK, stroke_width=3).set_fill(WELD, 1)


def film_tones(x0, x1, y_top, h, stops):
    """Film strip filled from `stops`: [(x, tone_level), ...] sorted in x; linear between stops."""
    g = VGroup()
    for (xa, la), (xb, lb) in zip(stops[:-1], stops[1:]):
        xa, xb = max(xa, x0), min(xb, x1)
        if xb - xa < 1e-4:
            continue
        n = 1 if abs(la - lb) < 1e-6 else max(2, int((xb - xa) / 0.02))
        w = (xb - xa) / n
        for k in range(n):
            lv = la + (lb - la) * (k + 0.5) / n
            g.add(Rectangle(width=w + 0.004, height=h, stroke_width=0)
                  .set_fill(grey(lv), 1).move_to([xa + w * (k + 0.5), y_top - h / 2, 0]))
    frame = Rectangle(width=x1 - x0, height=h, stroke_width=2, color=INK)
    frame.move_to([(x0 + x1) / 2, y_top - h / 2, 0])
    return VGroup(g, frame)


class Rig:
    """Source of size F above a plate whose opaque feature starts at the edge xe (source side),
    and a film under the plate. F, D (source → source side) and the gap film–plate are
    ValueTrackers; everything is redrawn from them, so moving a tracker moves the drawing."""

    def __init__(self, xe, px0, px1, y_top, thick, F, Dd, gap, feat_x1, film_h=0.2):
        self.xe, self.px0, self.px1, self.y_top, self.thick = xe, px0, px1, y_top, thick
        self.feat_x1, self.film_h = feat_x1, film_h
        self.F, self.D, self.gap = ValueTracker(F), ValueTracker(Dd), ValueTracker(gap)
        self.plate = Rectangle(width=px1 - px0, height=thick, color=INK, stroke_width=3)
        self.plate.set_fill(PLATE, 1).move_to([(px0 + px1) / 2, y_top - thick / 2, 0])
        self.feature = Rectangle(width=feat_x1 - xe, height=0.12, stroke_width=2, color=DEF_C)
        self.feature.set_fill(DEF_C, 0.85).move_to([(xe + feat_x1) / 2, y_top - 0.09, 0])
        self.source = always_redraw(self._source)
        self.rays = always_redraw(self._rays)
        self.film = always_redraw(self._film)

    # geometry
    def ys(self):
        return self.y_top + self.D.get_value()

    def film_top(self):
        return self.y_top - self.thick - self.gap.get_value()

    def d(self):
        return self.y_top - self.film_top()

    def pen(self):
        """Penumbra edges on the film for the edge xe: (left, right)."""
        half = self.F.get_value() * self.d() / self.D.get_value() / 2
        return self.xe - half, self.xe + half

    def _source(self):
        f = max(self.F.get_value(), 0.001)
        if f < 0.06:
            return Dot([self.xe, self.ys(), 0], radius=0.09, color=SRC_C)
        return Rectangle(width=f, height=0.14, stroke_width=2, color=SRC_C).set_fill(SRC_C, 1) \
            .move_to([self.xe, self.ys(), 0])

    def _rays(self):
        f, ys, yf = self.F.get_value(), self.ys(), self.film_top()
        e = np.array([self.xe, self.y_top, 0])
        out = VGroup()
        for sx in (self.xe - f / 2, self.xe + f / 2):
            s = np.array([sx, ys, 0])
            k = (ys - yf) / (ys - self.y_top)
            end = s + (e - s) * k
            out.add(Line(s, end, stroke_width=2.5, color=RAY_C))
        return out

    def _film(self):
        a, b = self.pen()
        full, dark = 0.02, 1.0
        stops = [(self.px0, dark), (a, dark), (b, full), (self.px1, full)]
        if b - a < 0.004:
            stops = [(self.px0, dark), (self.xe, dark), (self.xe + 0.004, full), (self.px1, full)]
        return film_tones(self.px0, self.px1, self.film_top(), self.film_h, stops)

    def triangles(self):
        f, ys, yf = self.F.get_value(), self.ys(), self.film_top()
        a, b = self.pen()
        s1, s2 = [self.xe - f / 2, ys, 0], [self.xe + f / 2, ys, 0]
        e = [self.xe, self.y_top, 0]
        t1 = Polygon(s1, s2, e, stroke_width=0).set_fill(SRC_C, 0.35)
        t2 = Polygon(e, [a, yf, 0], [b, yf, 0], stroke_width=0).set_fill(RAY_C, 0.35)
        return t1, t2


def dim_line(x, y0, y1, text, color=INK, side=LEFT):
    """Vertical dimension line with arrows at both ends and a label beside it."""
    arr = DoubleArrow([x, y0, 0], [x, y1, 0], buff=0, stroke_width=3, color=color,
                      tip_length=0.16, max_tip_length_to_length_ratio=0.45)
    lab = label(text, FS_LABEL, color, weight=BOLD).next_to(arr, side, 0.12)
    return VGroup(arr, lab)


class RtIntroPrinciple(SyncedScene):
    def c(self, seg, phrase, nth=1):
        return self.cue(seg, phrase, nth)

    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        self.seg1()
        self.seg2()
        self.seg3()
        self.seg4()
        self.seg5()
        self.seg6()

    # =====================================================================
    # Segment 1: what RT is, why (title, weld with four defects, shadow picture, record)
    # =====================================================================
    def seg1(self):
        s = 1
        head = title_card(self, "Industrial Radiography", "Principle & geometric unsharpness",
                          series="Radiographic testing (RT) · Introduction")
        notes = VGroup(label("Educational material. The binding reference is the official",
                             FS_NOTE, GREY_INK),
                       label("documentation and the approved procedures.", FS_NOTE, GREY_INK))
        notes.arrange(DOWN, buff=0.12).next_to(head, DOWN, 0.6)
        box = SurroundingRectangle(notes, buff=0.22, corner_radius=0.12, stroke_width=3,
                                   color=GREY_INK)
        self.play(Create(box), FadeIn(notes), run_time=1.0)
        self.sync(self.c(s, "التَّصْوِيرُ") - 0.7)
        self.clear()
        self.sec = section_title(self, "1  What radiography does")

        # weld cross-section: two plates, V groove, cap and root
        YT, YB = 1.2, -0.4
        lp = Polygon([-4.4, YT, 0], [-2.0, YT, 0], [-0.5, YB, 0], [-4.4, YB, 0],
                     color=INK, stroke_width=3).set_fill(PLATE, 1)
        rp = Polygon([4.4, YT, 0], [2.0, YT, 0], [0.5, YB, 0], [4.4, YB, 0],
                     color=INK, stroke_width=3).set_fill(PLATE, 1)
        weld = Polygon([-2.0, YT, 0], [2.0, YT, 0], [0.5, YB, 0], [-0.5, YB, 0],
                       color=INK, stroke_width=3).set_fill(WELD, 1)
        cap, root = bump(-2.15, 2.15, YT, 0.28), bump(-0.62, 0.62, YB, -0.14)
        joint = VGroup(lp, rp, weld, cap, root)
        wlab = label("Butt weld", FS_NOTE, GREY_INK).move_to([-3.3, 0.4, 0])
        self.play(Create(joint), FadeIn(wlab), run_time=1.6)
        self.say("Non-destructive: the part stays usable")

        # the four defects, each drawn and named at its word
        pores = VGroup(*[Circle(radius=0.075, color=DEF_C, stroke_width=3).set_fill(WHITE, 1)
                         .move_to([x, y, 0]) for x, y in ((-0.95, 0.85), (-0.72, 0.66),
                                                          (-1.12, 0.6), (-0.8, 1.02))])
        slag = Polygon([-0.55, -0.02, 0], [-0.3, 0.06, 0], [0.05, 0.02, 0], [0.18, -0.08, 0],
                       [-0.1, -0.14, 0], [-0.45, -0.12, 0], color=DEF_C,
                       stroke_width=3).set_fill(DEF_C, 0.35)
        lof = Line([0.9, 0.1, 0], [1.33, 0.56, 0], color=DEF_C, stroke_width=7)
        crack = VMobject(color=DEF_C, stroke_width=4).set_points_as_corners(
            [[0.2, 0.3, 0], [0.33, 0.5, 0], [0.18, 0.68, 0], [0.32, 0.9, 0], [0.24, 1.05, 0]])
        items = [(pores, "المَسَامِيَّةِ", "Porosity", [-0.95, 0.92, 0], [-4.5, 2.75, 0]),
                 (slag, "وَشَوَائِبِ", "Slag inclusion", [-0.45, -0.1, 0], [-4.7, -1.0, 0]),
                 (lof, "وَعَدَمِ", "Lack of fusion", [1.2, 0.42, 0], [4.7, -1.0, 0]),
                 (crack, "وَالشُّقُوقِ", "Crack", [0.3, 0.9, 0], [3.9, 2.75, 0])]
        tags = VGroup()
        for mob, word, text, tgt, pos in items:
            self.sync(self.c(s, word))
            co = callout(text, tgt, pos, DEF_C)
            tags.add(co)
            self.play(Create(mob), FadeIn(co[0]), GrowArrow(co[1]), run_time=0.8)
        defects = VGroup(pores, slag, lof, crack)

        # radiation from the source through the weld onto the film
        self.sync(self.c(s, "تَمُرُّ"))
        S = np.array([0.0, 3.0, 0])
        src = Dot(S, radius=0.13, color=SRC_C)
        src_l = label("Source", FS_NOTE, SRC_C).next_to(src, RIGHT, 0.15)
        FY = -1.9
        film = Rectangle(width=7.2, height=0.22, stroke_width=2, color=INK).set_fill(FILM_NEW, 1)
        film.move_to([0, FY, 0])
        ftop = FY + 0.11
        rays = VGroup(*[Line(S, [x, ftop, 0], stroke_width=3, color=RAY_C, stroke_opacity=0.8)
                        for x in np.linspace(-3.3, 3.3, 7)])
        self.say("Rays pass through the part")
        self.play(FadeIn(src), FadeIn(src_l), run_time=0.5)
        self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.08), run_time=1.3)
        self.sync(self.c(s, "فِيلْمٍ"))
        film_l = label("Film / detector", FS_NOTE).next_to(film, RIGHT, 0.2)
        self.play(FadeIn(film), FadeIn(film_l), run_time=0.7)

        # shadow picture: each defect projected from the source onto the film
        def shadow(mob, h=0.14):
            pts = mob.get_all_points()
            k = (S[1] - ftop) / (S[1] - pts[:, 1])
            xs = S[0] + (pts[:, 0] - S[0]) * k
            w = max(xs.max() - xs.min(), 0.06)
            return RoundedRectangle(width=w, height=h, corner_radius=min(w, h) / 2.2,
                                    stroke_width=0).set_fill("#262626", 1) \
                .move_to([(xs.max() + xs.min()) / 2, FY, 0])
        marks = VGroup(*[shadow(p, 0.1) for p in pores], shadow(slag), shadow(lof, 0.08),
                       shadow(crack, 0.16))
        self.sync(self.c(s, "صُورَةٌ") - 0.3)
        self.say("A shadow picture of the inside")
        self.play(film.animate.set_fill("#a4a4a4", 1), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in marks], lag_ratio=0.1),
                  Indicate(defects, color=DEF_C, scale_factor=1.08), run_time=1.4)

        # a permanent record: the developed film goes to the archive
        self.sync(self.c(s, "سِجِلًّا") - 0.3)
        sheet = VGroup(film, marks)
        self.play(FadeOut(rays), FadeOut(src), FadeOut(src_l), FadeOut(film_l),
                  FadeOut(self.caption), run_time=0.5)
        self.caption = VMobject()
        self.play(sheet.animate.stretch_to_fit_height(0.8).scale(0.8).move_to([-1.2, -2.45, 0]),
                  run_time=1.0)
        stack = VGroup(*[film.copy().set_fill(FILM_NEW, 1).set_stroke(GREY_INK, 2)
                         .shift(RIGHT * 0.14 * k + UP * 0.12 * k) for k in (2, 1)])
        rec = VGroup(label("Permanent record", FS_LABEL, weight=BOLD),
                     label("review it later", FS_NOTE, GREY_INK)).arrange(DOWN, buff=0.1)
        rec.next_to(stack, RIGHT, 0.35)
        self.bring_to_back(stack)
        self.play(FadeIn(stack, shift=DOWN * 0.1), FadeIn(rec, shift=LEFT * 0.2), run_time=0.8)
        self.sync(self.end(s) - 0.6)
        self.clear(self.sec)

    # =====================================================================
    # Segment 2: differential absorption
    # =====================================================================
    def seg2(self):
        s = 2
        section_title(self, "2  Differential absorption", prev=self.sec)
        Y0 = 1.35
        light = FunctionGraph(lambda x: Y0 + 0.4 * np.sin(2 * PI * (x + 6) / 2.4),
                              x_range=[-6.0, -0.4], color=GREY_INK, stroke_width=4)
        light_l = label("Light: long wavelength", FS_NOTE, GREY_INK).next_to(light, DOWN, 0.3)
        self.play(Create(light), FadeIn(light_l), run_time=1.4)
        self.sync(self.c(s, "طُولُهَا"))
        xray = FunctionGraph(lambda x: Y0 + 0.4 * np.sin(2 * PI * (x + 6) / 0.32),
                             x_range=[-6.0, -0.4], color=RAY_C, stroke_width=4)
        xray_l = label("X-rays / gamma: very short wavelength", FS_NOTE, RAY_C)
        xray_l.move_to(light_l)
        self.play(Transform(light, xray), Transform(light_l, xray_l), run_time=1.4)
        self.sync(self.c(s, "فَتَنْفُذُ"))
        blk = Rectangle(width=1.4, height=1.8, color=INK, stroke_width=3).set_fill(PLATE, 1)
        blk.move_to([1.3, Y0, 0])
        blk_l = label("Metal", FS_NOTE).next_to(blk, UP, 0.15)

        def amp(x):
            return 0.4 if x < 0.6 else (0.4 - 0.25 * (x - 0.6) / 1.4 if x < 2.0 else 0.15)
        through = FunctionGraph(lambda x: Y0 + amp(x) * np.sin(2 * PI * (x + 6) / 0.32),
                                x_range=[-0.4, 5.6], color=RAY_C, stroke_width=4)
        self.play(FadeIn(blk), FadeIn(blk_l), run_time=0.5)
        self.add_foreground_mobject(through)
        self.play(Create(through), run_time=1.3)
        self.remove_foreground_mobject(through)
        self.add(through)
        self.sync(self.c(s, "وَيَمْتَصُّ") - 0.5)
        gone = VGroup(light, light_l, blk, blk_l, through)

        # plate with a thin step, a void and a tungsten inclusion; parallel beam; film
        TOP, TOP_THIN, BOT, STEP = 1.2, 0.5, -0.2, -3.3
        X0, X1 = -5.2, 5.4
        plate = Polygon([X0, BOT, 0], [X1, BOT, 0], [X1, TOP, 0], [STEP, TOP, 0],
                        [STEP, TOP_THIN, 0], [X0, TOP_THIN, 0], color=INK,
                        stroke_width=3).set_fill(PLATE, 1)
        FT, FH = -1.55, 0.34
        MU, MU_W = 0.9, 5.4          # illustrative absorption per unit (steel, tungsten)
        cells = {"thin": (X0, STEP), "a": (STEP, -0.45), "void": (-0.45, 0.45),
                 "b": (0.45, 2.38), "w": (2.38, 2.82), "c": (2.82, X1)}
        cell = {k: Rectangle(width=b - a, height=FH, stroke_width=0).set_fill(FILM_NEW, 1)
                .move_to([(a + b) / 2, FT - FH / 2, 0]) for k, (a, b) in cells.items()}
        film_frame = Rectangle(width=X1 - X0, height=FH, stroke_width=2, color=INK)
        film_frame.move_to([(X0 + X1) / 2, FT - FH / 2, 0])
        film = VGroup(*cell.values(), film_frame)
        film_l = label("Film", FS_NOTE).next_to(film_frame, DOWN, 0.15).align_to(film_frame, LEFT)
        self.play(FadeOut(gone), Create(plate), FadeIn(film), FadeIn(film_l), run_time=1.0)

        def beam(x, t_metal, extra=0.0):
            top = TOP_THIN if x < STEP else TOP
            i = np.exp(-MU * t_metal - extra)
            inc = Line([x, 2.55, 0], [x, top, 0], stroke_width=12, color=RAY_C,
                       stroke_opacity=0.55)
            out = Line([x, BOT, 0], [x, FT, 0], stroke_width=max(14 * i, 1.2), color=RAY_C,
                       stroke_opacity=0.55)
            return inc, out, i
        t_full, t_thin = TOP - BOT, TOP_THIN - BOT
        base = [beam(-4.25, t_thin), beam(-2.0, t_full), beam(1.4, t_full)]
        self.sync(self.c(s, "جُزْءًا") - 0.3)
        self.play(*[Create(b[0]) for b in base], run_time=0.8)
        self.play(*[Create(b[1]) for b in base], run_time=0.8)
        self.sync(self.c(s, "سَمَاكَتِهِ") - 0.3)
        br_thin = Brace(Line([X0, BOT, 0], [X0, TOP_THIN, 0]), direction=LEFT, buff=0.08)
        br_thick = Brace(Line([X1, BOT, 0], [X1, TOP, 0]), direction=RIGHT, buff=0.08)
        l_thin = label("thin", FS_NOTE).next_to(br_thin, LEFT, 0.08)
        l_thick = label("thick", FS_NOTE).next_to(br_thick, RIGHT, 0.08)
        lv_thin, lv_full = 1.5 * np.exp(-MU * t_thin), 1.5 * np.exp(-MU * t_full)
        self.play(GrowFromCenter(br_thin), GrowFromCenter(br_thick), FadeIn(l_thin),
                  FadeIn(l_thick),
                  cell["thin"].animate.set_fill(grey(lv_thin), 1),
                  *[cell[k].animate.set_fill(grey(lv_full), 1) for k in ("a", "void", "b", "w", "c")],
                  run_time=1.0)
        self.say("Absorbed part grows with thickness and density")

        # the void: less metal in the beam path, more radiation, darker film
        self.sync(self.c(s, "فَرَاغٌ"))
        void = Ellipse(width=0.9, height=0.5, color=DEF_C, stroke_width=3).set_fill(WHITE, 1)
        void.move_to([0, 0.5, 0])
        void_l = label("Void", FS_LABEL, DEF_C).next_to(void, RIGHT, 0.25)
        self.play(GrowFromCenter(void), FadeIn(void_l), run_time=0.7)
        self.sync(self.c(s, "تَقِلُّ"))
        vin, vout, vi = beam(0.0, t_full - 0.5)
        path = VGroup(Line([0.12, TOP, 0], [0.12, 0.75, 0]), Line([0.12, 0.25, 0], [0.12, BOT, 0]))
        path.set_stroke(GREY_INK, 6)
        self.play(Create(vin), run_time=0.6)
        self.play(Create(path), run_time=0.6)
        self.say("Void: less metal in the beam path")
        self.sync(self.c(s, "فَيَصِلُ"))
        self.play(Create(vout), run_time=0.8)
        self.sync(self.c(s, "أَغْمَقَ") - 0.2)
        dark_l = label("darker", FS_LABEL, weight=BOLD).next_to(cell["void"], DOWN, 0.15)
        self.play(cell["void"].animate.set_fill(grey(1.5 * vi), 1), FadeIn(dark_l), run_time=0.8)

        # the denser inclusion: more absorbed, lighter film
        self.sync(self.c(s, "شَائِبَةٌ"))
        w = Circle(radius=0.22, color=DEF_C, stroke_width=3).set_fill("#5a1010", 1).move_to([2.6, 0.5, 0])
        w_l = label("Tungsten", FS_LABEL, DEF_C).next_to(w, RIGHT, 0.3)
        self.play(GrowFromCenter(w), FadeIn(w_l), run_time=0.7)
        self.say("Denser inclusion: more radiation absorbed")
        self.sync(self.c(s, "يُمْتَصُّ"))
        win, wout, wi = beam(2.6, t_full - 0.44, extra=MU_W * 0.44)
        self.play(Create(win), run_time=0.6)
        self.play(Create(wout), run_time=0.6)
        self.sync(self.c(s, "أَفْتَحَ") - 0.2)
        light_l2 = label("lighter", FS_LABEL, weight=BOLD).next_to(cell["w"], DOWN, 0.15)
        self.play(cell["w"].animate.set_fill(grey(1.5 * wi), 1), FadeIn(light_l2), run_time=0.8)

        # the difference draws the defect: the film is a map
        self.sync(self.c(s, "فَالفَرْقُ"))
        outs = VGroup(*[b[1] for b in base], vout, wout)
        self.play(Indicate(outs, color=RAY_C, scale_factor=1.0), run_time=1.2)
        self.sync(self.c(s, "وَالصُّورَةُ") - 0.2)
        frame = emphasize(self, film, color=RAY_C, buff=0.1)
        self.say("Radiograph = map of thickness and density")
        self.sync(self.end(s) - 0.6)
        self.clear(self.sec)

    # =====================================================================
    # Segment 3: X-ray tube or Ir-192
    # =====================================================================
    def seg3(self):
        s = 3
        section_title(self, "3  The radiation source", prev=self.sec)
        div = DashedLine([0, 2.9, 0], [0, -1.5, 0], color=LIGHT_INK, stroke_width=2)
        h_x = label("X-ray tube", FS_BODY - 4, weight=BOLD).move_to([-3.5, 2.8, 0])
        self.play(Create(div), run_time=0.5)

        # ---- the X-ray tube
        self.sync(self.c(s, "جِهَازُ") - 0.2)
        env = RoundedRectangle(width=4.4, height=1.5, corner_radius=0.6, color=INK,
                               stroke_width=3).set_fill("#f7fbff", 1).move_to([-3.6, 1.3, 0])
        cup = Rectangle(width=0.22, height=0.7, color=INK, stroke_width=3).set_fill(PLATE, 1)
        cup.move_to([-5.42, 1.3, 0])
        coil = VMobject(color=INK, stroke_width=3).set_points_as_corners(
            [[-5.2 + 0.07 * (k % 2), 1.08 + 0.055 * k, 0] for k in range(9)])
        rod = Line([-1.35, 1.3, 0], [-2.35, 1.3, 0], stroke_width=10, color=INK)
        target = Polygon([-2.3, 1.72, 0], [-2.3, 0.88, 0], [-2.52, 0.95, 0], [-2.78, 1.62, 0],
                         color=INK, stroke_width=3).set_fill("#b0b0b0", 1)
        tube = VGroup(env, cup, coil, rod, target)
        l_cat = label("Cathode (−)", FS_NOTE).move_to([-5.2, 2.3, 0])
        l_an = label("Anode (+), target", FS_NOTE).move_to([-1.75, 2.3, 0])
        self.play(Write(h_x), Create(tube), run_time=1.4)
        self.play(FadeIn(l_cat), FadeIn(l_an), run_time=0.5)

        self.sync(self.c(s, "الإِلِكْتْرُونَاتُ") - 0.2)
        hv = RoundedRectangle(width=2.2, height=0.8, corner_radius=0.12, color=INK,
                              stroke_width=3).move_to([-5.15, -0.55, 0])
        dial = Circle(radius=0.24, color=INK, stroke_width=3).move_to([-4.6, -0.55, 0])
        needle = Line(dial.get_center(), dial.get_center() + 0.2 * rotate_vector(LEFT, -PI / 5),
                      stroke_width=3, color=INK)
        hv_t = label("HV  kV", FS_NOTE).move_to([-5.55, -0.55, 0])
        wire = Line([-5.42, 0.95, 0], [-5.42, -0.15, 0], stroke_width=3, color=GREY_INK)
        e_l = label("electrons", FS_NOTE, GREY_INK).move_to([-3.85, 0.25, 0])
        self.play(Create(hv), Create(dial), Create(needle), FadeIn(hv_t), Create(wire),
                  FadeIn(e_l), run_time=0.8)

        def electrons():
            dots = VGroup(*[Dot([-5.1, 1.3 + dy, 0], radius=0.05, color=INK)
                            for dy in (-0.12, 0.0, 0.12)])
            self.add(dots)
            self.play(LaggedStart(*[d.animate.move_to([-2.5, 1.28 + 0.2 * (k - 1) * 0.3, 0])
                                    for k, d in enumerate(dots)], lag_ratio=0.25),
                      run_time=0.9, rate_func=rate_functions.ease_in_quad)
            self.remove(dots)
        for _ in range(2):
            electrons()
        self.sync(self.c(s, "بِهَدَفٍ") - 0.1)
        electrons()
        self.play(Indicate(target, color=SRC_C), run_time=0.6)

        spot = Dot([-2.62, 1.28, 0], radius=0.085, color=SRC_C)
        cone = Polygon([-2.62, 1.2, 0], [-3.45, -1.45, 0], [-1.8, -1.45, 0], stroke_width=0)
        cone.set_fill(RAY_C, 0.28)
        self.sync(self.c(s, "فَتَنْطَلِقُ"))
        self.add(spot)
        self.play(GrowFromPoint(cone, [-2.62, 1.2, 0]), run_time=0.9)
        l_x = label("X-rays", FS_NOTE, RAY_C).move_to([-2.62, -1.75, 0])
        self.play(FadeIn(l_x), run_time=0.4)
        self.sync(self.c(s, "البُقْعَةُ") - 0.2)
        fs = callout("Focal spot", spot.get_center(), [-1.0, 0.25, 0], SRC_C, FS_NOTE)
        self.play(spot.animate.scale(1.4), FadeIn(fs[0]), GrowArrow(fs[1]), run_time=0.7)

        # power switch: ON, then OFF → the beam stops
        self.sync(self.c(s, "بِالكَهْرَبَاءِ") - 0.2)
        sw = RoundedRectangle(width=0.9, height=0.4, corner_radius=0.2, color=INK,
                              stroke_width=3).move_to([-5.45, -1.5, 0])
        knob = Dot(sw.get_right() + LEFT * 0.2, radius=0.14, color=OK_C)
        sw_t = label("ON", FS_NOTE, OK_C).next_to(sw, RIGHT, 0.15)
        self.play(Create(sw), FadeIn(knob), FadeIn(sw_t), run_time=0.6)
        self.sync(self.c(s, "وَيُطْفَأُ"))
        off_t = label("OFF", FS_NOTE, ALERT_C).move_to(sw_t, aligned_edge=LEFT)
        self.play(knob.animate.move_to(sw.get_left() + RIGHT * 0.2).set_color(ALERT_C),
                  Transform(sw_t, off_t), FadeOut(cone), FadeOut(l_x), run_time=0.7)
        self.sync(self.c(s, "وَتُضْبَطُ") - 0.3)
        on_t = label("ON", FS_NOTE, OK_C).move_to(sw_t, aligned_edge=LEFT)
        self.play(knob.animate.move_to(sw.get_right() + LEFT * 0.2).set_color(OK_C),
                  Transform(sw_t, on_t), FadeIn(cone), FadeIn(l_x), run_time=0.6)
        self.sync(self.c(s, "بِالجُهْدِ") - 0.2)
        deep = cone.copy().set_fill(RAY_C, 0.55)
        kv_l = label("higher kV:\nmore penetrating", FS_NOTE, RAY_C).move_to([-4.9, -2.5, 0])
        self.play(Rotate(needle, -PI / 2, about_point=dial.get_center()),
                  Transform(cone, deep), FadeIn(kv_l), run_time=1.2)

        # ---- the gamma source
        self.sync(self.c(s, "وَمَصْدَرُ") - 0.2)
        h_g = label("Gamma source (Ir-192)", FS_BODY - 4, weight=BOLD).move_to([3.5, 2.8, 0])
        cont = RoundedRectangle(width=2.0, height=1.5, corner_radius=0.2, color=INK,
                                stroke_width=6).set_fill("#9a9a9a", 1).move_to([2.2, 1.2, 0])
        cap = RoundedRectangle(width=0.36, height=0.18, corner_radius=0.08, color=SRC_C,
                               stroke_width=2).set_fill(SRC_C, 1).move_to([2.2, 1.2, 0])
        self.play(Write(h_g), run_time=0.8)
        self.sync(self.c(s, "كَبْسُولَةٍ") - 0.2)
        self.play(FadeIn(cap, scale=2), run_time=0.5)
        l_cap = label("Capsule", FS_NOTE, SRC_C).next_to(cap, UP, 0.12)
        self.play(FadeIn(l_cap), run_time=0.4)
        self.sync(self.c(s, "حَاوِيَةٍ") - 0.1)
        self.play(FadeOut(l_cap), run_time=0.2)
        self.play(DrawBorderThenFill(cont), run_time=0.8)
        self.bring_to_front(cap)
        l_cont = label("Shielded container", FS_NOTE).next_to(cont, UP, 0.15)
        self.play(FadeIn(l_cont), run_time=0.4)

        self.sync(self.c(s, "تُدْفَعُ") - 0.2)
        guide = CubicBezier([3.2, 1.2, 0], [4.7, 1.2, 0], [5.45, 0.4, 0], [5.45, -0.95, 0],
                            color=GREY_INK, stroke_width=7)
        head = Square(side_length=0.36, color=INK, stroke_width=3).set_fill(PLATE, 1)
        head.move_to([5.45, -1.13, 0])
        l_guide = label("Guide tube", FS_NOTE).move_to([5.3, 1.55, 0])
        self.play(Create(guide), FadeIn(head), run_time=0.8)
        self.play(cap.animate.move_to([3.2, 1.2, 0]), run_time=0.5, rate_func=linear)
        self.play(MoveAlongPath(cap, guide), FadeIn(l_guide), run_time=1.4, rate_func=linear)
        self.play(cap.animate.move_to(head.get_center()), run_time=0.3)
        self.bring_to_front(cap)
        burst = VGroup(*[Line(head.get_center() + 0.3 * rotate_vector(RIGHT, a),
                              head.get_center() + 0.7 * rotate_vector(RIGHT, a),
                              stroke_width=3, color=RAY_C) for a in np.linspace(0, TAU, 12,
                                                                                endpoint=False)])
        l_exp = label("Exposure\nposition", FS_NOTE).next_to(head, DOWN, 0.85)
        self.play(LaggedStart(*[Create(b) for b in burst], lag_ratio=0.05), FadeIn(l_exp),
                  run_time=0.8)

        tag_pos = [1.85, 0.05, 0]
        tags = [("يَحْتَاجُ", "No power needed", INK), ("المَيْدَانِ", "Portable: field work", INK),
                ("يُطْفَأُ", "Cannot be switched off", ALERT_C),
                ("فَعُمْرُ", f"Half-life ≈ {D.IR192_HALF_LIFE_DAYS} days", INK)]
        prev = None
        for word, text, col in tags:
            self.sync(self.c(s, word, 1) if word != "يُطْفَأُ" else self.c(s, "لَا يُطْفَأُ"))
            t = label(text, FS_NOTE, col)
            if prev is None:
                t.move_to(tag_pos)
            else:
                t.next_to(prev, DOWN, 0.2).align_to(prev, LEFT)
            anims = [FadeIn(t, shift=RIGHT * 0.15)]
            if word == "يُطْفَأُ":
                anims.append(Indicate(burst, color=RAY_C, scale_factor=1.15))
            self.play(*anims, run_time=0.6)
            prev = t

        # both sources have a size F: magnified insets
        self.sync(self.c(s, "حَجْمٌ") - 0.3)

        def inset(center, obj):
            ring = Circle(radius=0.55, color=SRC_C, stroke_width=3).set_fill(WHITE, 1).move_to(center)
            obj.move_to(ring.get_center() + DOWN * 0.12)
            arr = DoubleArrow(obj.get_left() + UP * 0.25, obj.get_right() + UP * 0.25, buff=0,
                              stroke_width=3, color=SRC_C, tip_length=0.12,
                              max_tip_length_to_length_ratio=0.3)
            f = label("F", FS_LABEL, SRC_C, weight=BOLD).next_to(arr, UP, 0.03)
            return VGroup(ring, obj, arr, f)
        big_spot = Ellipse(width=0.62, height=0.2, color=SRC_C).set_fill(SRC_C, 1)
        big_cap = RoundedRectangle(width=0.62, height=0.22, corner_radius=0.08, color=SRC_C,
                                   stroke_width=2).set_fill(SRC_C, 1)
        in1, in2 = inset([-1.0, -2.45, 0], big_spot), inset([3.2, -2.5, 0], big_cap)
        lk1 = DashedLine(spot.get_center(), in1[0].get_top(), color=SRC_C, stroke_width=2)
        lk2 = DashedLine(cap.get_center(), in2[0].get_top(), color=SRC_C, stroke_width=2)
        self.play(Create(lk1), Create(lk2), FadeIn(in1[0]), FadeIn(in2[0]), run_time=0.6)
        self.play(FadeIn(in1[1:]), FadeIn(in2[1:]), run_time=0.7)
        self.sync(self.end(s) - 0.6)
        self.clear(self.sec)

    # =====================================================================
    # Segment 4: geometric unsharpness
    # =====================================================================
    def seg4(self):
        s = 4
        section_title(self, "4  Geometric unsharpness", prev=self.sec)
        r = Rig(xe=-2.2, px0=-5.4, px1=0.9, y_top=-1.0, thick=0.6, F=0.0, Dd=2.8, gap=0.4,
                feat_x1=0.9)
        l_plate = label("Part", FS_NOTE).move_to([-4.6, -1.3, 0])
        l_film = label("Film", FS_NOTE).next_to(r.film, DOWN, 0.12).align_to(r.plate, LEFT)
        l_def = callout("Defect edge", [-2.1, -1.06, 0], [-0.4, 0.3, 0], DEF_C, FS_NOTE)
        self.play(Create(r.plate), FadeIn(r.feature), FadeIn(l_plate), run_time=0.8)
        self.add(r.film, r.rays, r.source)
        self.play(FadeIn(l_film), FadeIn(l_def[0]), GrowArrow(l_def[1]), run_time=0.6)
        self.say("Point source: sharp shadow edge")

        self.sync(self.c(s, "لٰكِنَّ"))
        l_F = always_redraw(lambda: label("F", FS_LABEL, SRC_C, weight=BOLD)
                            .next_to(r.source, RIGHT, 0.15))
        self.play(r.F.animate.set_value(1.2), run_time=1.6)
        self.play(FadeIn(l_F), run_time=0.3)
        self.say("Real source of size F")
        self.sync(self.c(s, "ظِلَّيْنِ"))
        self.play(Indicate(r.rays, color=SRC_C, scale_factor=1.0), run_time=1.0)
        self.sync(self.c(s, "مِنْطَقَةُ"))
        a, b = r.pen()
        yf = r.film_top()
        pz = Rectangle(width=b - a, height=r.film_h + 0.12, color=SRC_C, stroke_width=3)
        pz.move_to([(a + b) / 2, yf - r.film_h / 2, 0])
        l_pen = label("penumbra", FS_NOTE, SRC_C).next_to(pz, DOWN, 0.12)
        self.play(Create(pz), FadeIn(l_pen), run_time=0.7)
        self.say("Penumbra: the edge is blurred")

        self.sync(self.c(s, "عَرْضُهَا"))
        ug_l = label("width = Ug", FS_NOTE, SRC_C, weight=BOLD).next_to(l_pen, RIGHT, 0.2)
        self.play(FadeIn(ug_l), Indicate(pz, color=SRC_C), run_time=0.8)
        self.sync(self.c(s, "تَشَابُهِ"))
        t1, t2 = r.triangles()
        self.play(FadeIn(t1), run_time=0.6)
        self.play(FadeIn(t2), run_time=0.6)

        self.sync(self.c(s, "يُو جِي يُسَاوِي") - 0.2)
        eq = equation(self, ["Ug", "=", "F", "×", "d", "/", "D"],
                      colors={0: SRC_C, 2: SRC_C}, pos=[4.2, 2.3, 0], run_time=1.2)
        self.say("Similar triangles: Ug / d = F / D")

        # definitions with their dimension lines
        dx = -5.75

        def dline_D():
            return dim_line(dx, r.ys(), r.y_top, "D", INK, LEFT)

        def dline_d():
            return dim_line(dx, r.y_top, r.film_top(), "d", INK, LEFT)
        defs = VGroup(label("F = largest projected size of the source", FS_TAG + 2),
                      label("D = source → source side of the part", FS_TAG + 2),
                      label("d = source side of the part → film", FS_TAG + 2))
        defs.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(eq, DOWN, 0.45)
        fit(defs, 5.4).align_to([1.35, 0, 0], LEFT)
        self.sync(self.c(s, "إِفْ أَكْبَرُ") - 0.1)
        self.play(FadeIn(defs[0], shift=RIGHT * 0.2), Indicate(eq[2], color=SRC_C),
                  Indicate(r.source, color=SRC_C), run_time=0.8)
        self.sync(self.c(s, "وَدِي الكَبِيرَةُ"))
        dD = always_redraw(dline_D)
        guideS = always_redraw(lambda: DashedLine([dx, r.ys(), 0], [r.xe - r.F.get_value() / 2 - 0.1,
                                                                    r.ys(), 0],
                                                  color=LIGHT_INK, stroke_width=2))
        guideT = DashedLine([dx, r.y_top, 0], [r.px0, r.y_top, 0], color=LIGHT_INK, stroke_width=2)
        self.play(FadeIn(defs[1], shift=RIGHT * 0.2), FadeIn(dD), Create(guideS), Create(guideT),
                  Indicate(eq[6]), run_time=0.8)
        self.sync(self.c(s, "وَدِي الصَّغِيرَةُ"))
        dd = always_redraw(dline_d)
        guideF = always_redraw(lambda: DashedLine([dx, r.film_top(), 0], [r.px0, r.film_top(), 0],
                                                  color=LIGHT_INK, stroke_width=2))
        self.play(FadeIn(defs[2], shift=RIGHT * 0.2), FadeIn(dd), Create(guideF),
                  Indicate(eq[4]), run_time=0.8)
        self.sync(self.c(s, "سَمَاكَةُ") - 0.2)
        ghost = DashedLine([r.px0, r.y_top - r.thick, 0], [r.px1, r.y_top - r.thick, 0],
                           color=GREY_INK, stroke_width=3)
        self.say("Film in contact: d ≈ thickness of the part")
        self.play(Create(ghost), Indicate(r.plate, color=GREY_INK, scale_factor=1.0), run_time=0.8)

        # three ways to a sharper image, each one moving the drawing
        self.sync(self.c(s, "فَلِتَحْسِينِ") - 0.2)
        self.play(FadeOut(t1), FadeOut(t2), FadeOut(pz), FadeOut(ug_l), FadeOut(ghost),
                  FadeOut(l_pen), run_time=0.5)
        pz2 = always_redraw(lambda: Rectangle(width=max(r.pen()[1] - r.pen()[0], 0.01),
                                              height=r.film_h + 0.12, color=SRC_C,
                                              stroke_width=3)
                            .move_to([r.xe, r.film_top() - r.film_h / 2, 0]))
        self.add(pz2)
        ways = VGroup(label("✓ smaller source (F ↓)", FS_TAG + 2, OK_LIM),
                      label("✓ source farther (D ↑)", FS_TAG + 2, OK_LIM),
                      label("✓ film close to the part (d ↓)", FS_TAG + 2, OK_LIM))
        ways.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(defs, DOWN, 0.4).align_to(defs, LEFT)
        self.sync(self.c(s, "مَصْدَرٌ أَصْغَرُ"))
        self.play(r.F.animate.set_value(0.6), FadeIn(ways[0]), run_time=1.1)
        self.sync(self.c(s, "إِبْعَادُ"))
        self.play(r.D.animate.set_value(3.9), FadeIn(ways[1]), run_time=1.2)
        self.sync(self.c(s, "تَقْرِيبُ"))
        self.play(r.gap.animate.set_value(0.0), l_film.animate.shift(UP * 0.4), FadeIn(ways[2]),
                  run_time=1.1)
        self.sync(self.c(s, "وَيُوصِي") - 0.2)
        note = VGroup(label("ASME V, T-274: recommended maximum Ug", FS_TAG + 2),
                      label("Binding limit: referencing Code or contract", FS_TAG + 2, ALERT_C))
        note.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fit(note, 5.1).next_to(ways, DOWN, 0.4).align_to(ways, LEFT)
        box = SurroundingRectangle(note, buff=0.15, corner_radius=0.08, color=GREY_INK,
                                   stroke_width=2)
        self.play(FadeOut(self.caption), run_time=0.2)
        self.caption = VMobject()
        self.play(FadeIn(note[0]), Create(box), run_time=0.7)
        self.sync(self.c(s, "أَمَّا"))
        self.play(FadeIn(note[1]), run_time=0.6)
        self.sync(self.end(s) - 0.6)
        self.clear(self.sec)

    # =====================================================================
    # Segment 5: worked example
    # =====================================================================
    def seg5(self):
        s = 5
        section_title(self, "5  Worked example", prev=self.sec)
        SCALE = 100.0                                  # mm per drawing unit for D (not to scale)
        r = Rig(xe=3.3, px0=1.3, px1=5.3, y_top=-1.1, thick=1.1, F=1.5, Dd=D.D1 / SCALE, gap=0.0,
                feat_x1=5.3)
        tag = label("not to scale", FS_TAG, GREY_INK).next_to(self.sec, RIGHT, buff=0.6) \
            .align_to(self.sec, DOWN)
        self.play(Create(r.plate), FadeIn(r.feature), FadeIn(tag), run_time=0.8)
        self.add(r.film, r.rays, r.source)
        l_F = always_redraw(lambda: label(f"F = {D.F:.1f} mm", FS_NOTE, SRC_C)
                            .next_to(r.source, UP, 0.15))
        self.sync(self.c(s, "ثَلَاثَةُ") - 0.2)
        self.play(FadeIn(l_F), Indicate(r.source, color=SRC_C), run_time=0.7)
        self.sync(self.c(s, "سَمَاكَتُهُ"))
        l_t = label(f"weld {D.d:.0f} mm", FS_NOTE).next_to(r.plate, LEFT, 0.2)
        self.play(FadeIn(l_t), Indicate(r.plate, color=GREY_INK, scale_factor=1.0), run_time=0.7)
        dx = 5.85
        dd = dim_line(dx, r.y_top, r.film_top(), "d", INK, RIGHT)
        dD = always_redraw(lambda: dim_line(dx, r.ys(), r.y_top, "D", INK, RIGHT))
        gS = always_redraw(lambda: DashedLine([r.xe + r.F.get_value() / 2 + 0.1, r.ys(), 0],
                                              [dx, r.ys(), 0], color=LIGHT_INK, stroke_width=2))
        self.sync(self.c(s, "فَدِي") - 0.1)
        self.play(FadeIn(dd), run_time=0.6)

        def readout():
            dmm = r.D.get_value() * SCALE
            ug = D.ug(D.F, D.d, dmm)
            col = ALERT_C if ug > D.UG_MAX + 1e-9 else INK
            g = VGroup(label(f"D = {dmm:.1f} mm" if abs(dmm - round(dmm)) > 0.05
                             else f"D = {dmm:.0f} mm", FS_NOTE),
                       label(f"Ug = {ug:.2f} mm", FS_NOTE, col, weight=BOLD))
            return g.arrange(RIGHT, buff=0.5).move_to([3.3, -2.75, 0])
        ro = always_redraw(readout)
        pz = always_redraw(lambda: Rectangle(width=max(r.pen()[1] - r.pen()[0], 0.01),
                                             height=r.film_h + 0.12, color=SRC_C, stroke_width=3)
                           .move_to([r.xe, r.film_top() - r.film_h / 2, 0]))

        # D1: calculation beside the drawing
        self.sync(self.c(s, "عِنْدَ"))
        self.play(FadeIn(dD), Create(gS), FadeIn(ro), FadeIn(pz), run_time=0.8)
        calc = worked_calculation(
            self, ["Ug", "=", "F", "×", "d", "/", "D"],
            ["=", f"{D.F:.1f}", "×", f"{D.d:.0f}", "/", f"{D.D1:.0f}"],
            f"= {D.UG1:.2f} mm",
            cues=[self.c(s, "عِنْدَ") + 0.9, self.c(s, "ثَلَاثَةٌ") - 0.2, self.c(s, "يُعْطِي")],
            pos=[-3.6, 1.35, 0], size=36)

        # D2: the source moves closer, the penumbra doubles
        self.sync(self.c(s, "قَرَّبْنَا"))
        self.play(r.D.animate.set_value(D.D2 / SCALE), run_time=2.0)
        self.sync(self.c(s, "صَارَ") - 0.2)
        line2 = VGroup(label(f"D = {D.D2:.0f} mm  →  Ug = {D.UG2:.2f} mm", FS_LABEL))
        line2.next_to(calc, DOWN, 0.5)
        self.play(Write(line2), run_time=0.9)
        self.sync(self.c(s, "تَضَاعَفَ"))
        x2 = label(f"× {D.UG_RATIO:.0f}", FS_BODY, SRC_C, weight=BOLD).next_to(line2, RIGHT, 0.3)
        self.play(FadeIn(x2, scale=1.5), Indicate(pz, color=SRC_C), run_time=0.8)

        # the limit and the smallest distance
        self.sync(self.c(s, "صِفْرٌ فَاصِلَةُ") - 0.2)
        lim = VGroup(label("Illustrative limit:", FS_LABEL, OK_LIM),
                     label(f"Ug ≤ {D.UG_MAX:.2f} mm", FS_LABEL, OK_LIM))
        lim.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(line2, DOWN, 0.4).align_to(line2, LEFT)
        self.play(FadeIn(lim, shift=UP * 0.1), run_time=0.6)
        self.sync(self.c(s, "أَزْمِي") - 0.2)
        asme = VGroup(label("ASME V recommended max.", FS_TAG, GREY_INK),
                      label("for thickness < 2 in", FS_TAG, GREY_INK))
        asme.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        asme.next_to(lim, DOWN, 0.15).align_to(lim, LEFT)
        self.play(FadeIn(asme), run_time=0.5)
        self.sync(self.c(s, "فَأَقَلُّ") - 0.3)
        pair = VGroup(lim, asme)
        target = pair.copy().arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-3.4, 2.2, 0])
        self.play(FadeOut(VGroup(calc, line2, x2)), Transform(pair, target), run_time=0.7)
        calc2 = worked_calculation(
            self, ["Dmin", "=", "F", "×", "d", "/", "Ug max"],
            ["=", f"{D.F:.1f}", "×", f"{D.d:.0f}", "/", f"{D.UG_MAX:.2f}"],
            f"= {D.D_MIN:.1f} mm",
            cues=[self.c(s, "فَأَقَلُّ") + 0.5, self.c(s, "ثَلَاثَةٌ", 2) - 0.2, self.c(s, "أَيْ")],
            pos=[-3.6, -0.4, 0], size=36)
        zone = Rectangle(width=r.px1 - r.px0, height=D.D_MIN / SCALE, stroke_width=0)
        zone.set_fill(ALERT_C, 0.12).move_to([(r.px0 + r.px1) / 2, r.y_top + D.D_MIN / SCALE / 2, 0])
        dmin_line = DashedLine([r.px0, r.y_top + D.D_MIN / SCALE, 0],
                               [r.px1, r.y_top + D.D_MIN / SCALE, 0], color=ALERT_C, stroke_width=3)
        z_l = label("too close", FS_TAG, ALERT_C).move_to([1.95, r.y_top + 0.5, 0])
        self.play(r.D.animate.set_value(D.D_MIN / SCALE), FadeIn(zone), Create(dmin_line),
                  FadeIn(z_l), run_time=1.6)
        self.sync(self.end(s) - 0.6)
        self.clear(self.sec)

    # =====================================================================
    # Segment 6: summary
    # =====================================================================
    def seg6(self):
        s = 6
        self.play(FadeOut(self.sec), run_time=0.4)
        summary_box(self, "Summary",
                    ["Radiograph = map of thickness and density",
                     "Void → darker · denser inclusion → lighter",
                     "X-ray tube switches off · Ir-192 cannot",
                     "Ug = F·d/D: smaller F, larger D, film close"],
                    cues=[self.c(s, "الصُّورَةُ"), self.c(s, "الفَرَاغُ"),
                          self.c(s, "وَالمَصْدَرُ"), self.c(s, "وَحَجْمُ")])
        self.sync(self.end(s) + 1.0)


if __name__ == "__main__":
    main(__file__, "RtIntroPrinciple", NARRATION)
