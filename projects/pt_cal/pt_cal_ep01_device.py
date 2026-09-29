"""pt_cal, episode 1: the MC6 calibrator, its electrical side, its pressure modules and its modes.

Every number on screen or in the narration comes from pt_cal_data. Sources: sources/pt_cal_source.md (§1)
and sources/pt_cal_ep01_device.md; storyboard: storyboard/pt_cal_ep01_device.md. The calibrator is a
simplified custom drawing (no product image, no logo; model names as text only).

Build (from the repo root):
    python projects/pt_cal/pt_cal_ep01_device.py --preview   # 480p15 -> tmp/pt_cal_ep01_device/preview.mp4
    python projects/pt_cal/pt_cal_ep01_device.py             # 1080p30 -> output/pt_cal_ep01_device.mp4
"""
from explainer import *
from pt_cal_common import *
import pt_cal_data as D

# Fully diacritized narration (owner-approved 2026-09-28) — one entry per segment.
NARRATION = [
    # 1
    "هٰذِهِ مَادَّةٌ تَعْلِيمِيَّةٌ؛ وَالمَرْجِعُ المُلْزِمُ أَدِلَّةُ الصَّانِعِ الرَّسْمِيَّةُ وَإِجْرَاءَاتُ مُنْشَأَتِكَ. فِي هٰذِهِ السِّلْسِلَةِ نُعَايِرُ مُرْسِلَ ضَغْطٍ بِجِهَازِ إِمْ سِي سِكْس، مِنْ شَرِكَةِ بِيمِكْس الفِنْلَنْدِيَّةِ. وَالجِهَازُ ثَلَاثَةُ أَجْهِزَةٍ فِي عُلْبَةٍ وَاحِدَةٍ: مِقْيَاسٌ دَقِيقٌ يَقْرَأُ الإِشَارَاتِ، وَمُوَلِّدُ إِشَارَاتٍ يُغَذِّي المُرْسِلَ، وَحَاسُوبُ تَوْثِيقٍ يَحْفَظُ الإِجْرَاءَ وَالنَّتِيجَةَ.",
    # 2
    "وَلِلْجِهَازِ عَائِلَةٌ. إِمْ سِي فَايْف هُوَ الجِيلُ الأَقْدَمُ، تَوَقَّفَ إِنْتَاجُهُ عَامَ أَلْفَيْنِ وَأَرْبَعَةَ عَشَرَ، وَمَا زَالَ يَعْمَلُ فِي وِرَشٍ كَثِيرَةٍ، وَلَهُ نُسْخَةٌ آمِنَةٌ ذَاتِيًّا. وَإِمْ سِي سِكْس هُوَ الحَالِيُّ: شَاشَةُ لَمْسٍ مُلَوَّنَةٌ، خَمْسٌ فَاصِلَةُ سَبْعَةٍ بُوصَةً، وَخَمْسَةُ أَنْمَاطِ عَمَلٍ، وَاتِّصَالُ هَارْت وَفِيلْدْبَاس وَبْرُوفِيبَاس. وَإِمْ سِي سِكْس إِكْس نُسْخَتُهُ الآمِنَةُ ذَاتِيًّا لِلْمَنَاطِقِ الخَطِرَةِ، وَدَبْلْيُو إِس مَحَطَّةٌ لِلْوَرْشَةِ، وَتِي لِلْحَرَارَةِ، وَنَتْرُكُهُ لِجُزْءٍ آخَرَ.",
    # 3
    "عَلَى جِهَةِ خَرْجِ المُرْسِلِ يَقِيسُ الجِهَازُ تَيَّارَ حَلْقَةٍ خَارِجِيَّةٍ لَهَا تَغْذِيَتُهَا؛ أَوْ يُغَذِّي هُوَ المُرْسِلَ بِأَرْبَعَةٍ وَعِشْرِينَ فُولْت، وَيَقِيسُ تَيَّارَهُ مَعًا، وَهٰذَا الأَشْيَعُ فِي الوَرْشَةِ. وَمَعَ تَغْذِيَتِهِ الدَّاخِلِيَّةِ مُمَانَعَةُ هَارْت مُدْمَجَةٌ، فَلَا حَاجَةَ لِمُقَاوِمَةٍ؛ أَمَّا مَعَ تَغْذِيَةٍ خَارِجِيَّةٍ فَقَدْ تَلْزَمُ مُقَاوِمَةٌ قَدْرُهَا مِئَتَانِ وَخَمْسُونَ أُومًا. وَلَا تَتَجَاوَزْ بَيْنَ أَيِّ طَرَفَيْنِ سِتِّينَ فُولْت مُسْتَمِرًّا، أَوْ ثَلَاثِينَ مُتَرَدِّدًا.",
    # 4
    "وَفِي الدَّلِيلِ مَحْذُورٌ مُهِمٌّ: إِذَا كَانَ الجِهَازُ يُوَلِّدُ تَيَّارًا، وَانْفَتَحَتِ الحَلْقَةُ، رَفَعَ جُهْدَهُ لِيُحَافِظَ عَلَى التَّيَّارِ؛ فَإِذَا أُغْلِقَتْ مِنْ جَدِيدٍ قَفَزَ التَّيَّارُ لَحْظَةً، وَقَدْ يُتْلِفُ مُكَوِّنَاتِ الحَلْقَةِ. وَالقَاعِدَةُ: اضْبِطِ الخَرْجَ عَلَى صِفْرِ مِلِّي أَمْبِير قَبْلَ تَوْصِيلِ أَيِّ حَلْقَةٍ.",
    # 5
    "وَعَلَى جِهَةِ الضَّغْطِ ثَلَاثَةُ أَنْوَاعٍ مِنَ الوَحَدَاتِ. الدَّاخِلِيَّةُ مُرَكَّبَةٌ بِمَدًى ثَابِتٍ: حَتَّى ثَلَاثِ وَحَدَاتٍ نِسْبِيَّةٍ أَوْ تَفَاضُلِيَّةٍ، وَوَحْدَةٌ بَارُومِتْرِيَّةٌ وَاحِدَةٌ. وَالخَارِجِيَّةُ تُوصَلُ بِمَنْفَذٍ مُخَصَّصٍ، مِنَ التَّفْرِيغِ حَتَّى أَلْفِ بَار. وَالبَارُومِتْرِيَّةُ تَقِيسُ الضَّغْطَ الجَوِّيَّ، وَبِوُجُودِهَا تُعْرَضُ قِرَاءَةُ أَيِّ وَحْدَةٍ نِسْبِيَّةٍ ضَغْطًا مُطْلَقًا أَيْضًا.",
    # 6
    "فَأَيَّ وَحْدَةٍ تَخْتَارُ؟ أَصْغَرَ وَحْدَةٍ يُغَطِّي مَدَاهَا مَدَى المُرْسِلِ؛ لِأَنَّ جُزْءًا مِنْ دِقَّتِهَا نِسْبَةٌ مِنْ مَدَاهَا الكَامِلِ، لَا مِنَ الضَّغْطِ المُطَبَّقِ. مِثَالٌ: مُرْسِلٌ مَدَاهُ اثْنَانِ وَأَرْبَعُونَ كِيلُوغْرَامًا عَلَى السَّنْتِيمِتْرِ المُرَبَّعِ، أَيْ نَحْوُ وَاحِدٍ وَأَرْبَعِينَ بَار. بِوَحْدَةِ سِتِّينَ بَار يَكُونُ عَدَمُ التَّأَكُّدِ عِنْدَ القِمَّةِ نَحْوَ صِفْرٍ فَاصِلَةِ صِفْرٍ وَاحِدٍ سِتَّةٍ بَار؛ وَبِوَحْدَةِ سِتِّمِئَةٍ نَحْوَ صِفْرٍ فَاصِلَةِ وَاحِدٍ بَار، أَسْوَأَ بِسِتَّةِ أَضْعَافٍ. وَقَبْلَ كُلِّ عَمَلٍ: افْتَحِ المَنْفَذَ لِلْجَوِّ تَمَامًا وَصَفِّرِ الوَحْدَةَ؛ وَإِلَّا دَخَلَ خَطَأٌ ثَابِتٌ فِي كُلِّ النِّقَاطِ.",
    # 7
    "وَلِلْجِهَازِ خَمْسَةُ أَنْمَاطٍ. المِقْيَاسُ: إِشَارَةٌ وَاحِدَةٌ لِلْفَحْصِ السَّرِيعِ، بِلَا تَوْثِيقٍ. وَالمُعَايِرُ: الدَّخْلُ وَالخَرْجُ مَعًا، وَالخَطَأُ لَحْظِيًّا بِلَا حِفْظٍ. وَالمُعَايِرُ المُوَثِّقُ هُوَ القَلْبُ: تُعَرِّفُ فِيهِ المُرْسِلَ وَمَدَاهُ وَتَفَاوُتَهُ وَنِقَاطَهُ، فَيَقُودُ الإِجْرَاءَ وَيَحْفَظُ النَّتَائِجَ قَبْلَ الضَّبْطِ وَبَعْدَهُ، وَكُلُّ شَهَادَةٍ تَمُرُّ مِنْهُ. وَمُسَجِّلُ البَيَانَاتِ: قِيمَةٌ مُقَابِلَ الزَّمَنِ، لِتَشْخِيصِ انْهِيَارِ الضَّغْطِ وَالأَعْطَالِ المُتَقَطِّعَةِ. وَالمُتَّصِلُ: يَقْرَأُ تَهْيِئَةَ المُرْسِلِ الذَّكِيِّ وَيُغَيِّرُهَا وَيُرْسِلُ أَوَامِرَ الضَّبْطِ. وَالخَطَأُ الأَشْيَعُ: العَمَلُ كُلُّهُ فِي نَمَطِ المُعَايِرِ، ثُمَّ نَقْلُ الأَرْقَامِ بِالقَلَمِ؛ فَتَضِيعُ مُزَامَنَةُ القِرَاءَتَيْنِ، وَحِسَابُ الخَطَإِ مِنَ الدَّخْلِ الفِعْلِيِّ، وَسِلْسِلَةُ التَّوْثِيقِ الإِلِكْتْرُونِيَّةُ.",
    # 8
    "وَأَخِيرًا: إِمْ سِي سِكْس العَادِيُّ لَيْسَ آمِنًا ذَاتِيًّا؛ فَبَطَّارِيَّتُهُ وَدَوَائِرُهُ قَدْ تُنْتِجُ شَرَارَةً. فَفِي المِنْطَقَةِ المُصَنَّفَةِ خِيَارَانِ لَا ثَالِثَ لَهُمَا: جِهَازٌ مُعْتَمَدٌ لَهَا، مِثْلُ إِمْ سِي سِكْس إِكْس، أَوْ فَصْلُ المُرْسِلِ وَنَقْلُهُ إِلَى الوَرْشَةِ.",
]

# Every spoken or shown value is checked against the data module; stop if it drifts.
assert D.MC5_DISCONTINUED == 2014 and D.MC6_SCREEN_IN == 5.7 and len(D.MC6_MODES) == 5   # seg 2, 7
assert D.MC6_LOOP_V == 24 and D.MC6_HART_R_EXT == 250                                    # seg 3
assert D.MC6_MAX_VDC == 60 and D.MC6_MAX_VAC == 30                                        # seg 3
assert D.MC6_INT_MODULES == 3 and D.MC6_BARO_MODULES == 1 and D.EXT_MAX_BAR == 1000       # seg 5
assert round(D.URV_BAR) == 41 and f"{D.U_SMALL_BAR:.3f}" == "0.016"                       # seg 6
assert f"{D.U_BIG_BAR:.1f}" == "0.1" and round(D.MOD_RATIO) == 6                          # seg 6

AUDIO_DIR = audio_dir_for(__file__)


def calibrator(w=2.8, h=3.6):
    """Simplified documenting calibrator: case, screen, keys, terminals, pressure ports."""
    case = RoundedRectangle(width=w, height=h, corner_radius=0.25, color=INK, stroke_width=4).set_fill(WHITE, 1)
    screen = Rectangle(width=w - 0.6, height=h * 0.42, color=INK, stroke_width=3).set_fill(PANEL_FILL, 1)
    screen.move_to(case.get_top() + DOWN * (0.35 + screen.height / 2))
    keys = VGroup(*[RoundedRectangle(width=0.36, height=0.22, corner_radius=0.05, color=GREY_INK,
                                     stroke_width=2) for _ in range(8)]).arrange_in_grid(2, 4, buff=0.14)
    keys.next_to(screen, DOWN, buff=0.3)
    terms = VGroup(*[Circle(radius=0.08, color=INK, stroke_width=2) for _ in range(6)]).arrange(RIGHT, buff=0.18)
    terms.next_to(keys, DOWN, buff=0.3)
    g = VGroup(case, screen, keys, terms)
    g.case, g.screen, g.terms = case, screen, terms
    return g


class PtCalEp01(SyncedScene):
    def c(self, seg, phrase, nth=1):
        return self.cue(seg, phrase, nth)

    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        self.seg1_three()
        self.seg2_family()
        self.seg3_electrical()
        self.seg4_open_loop()
        self.seg5_modules()
        self.seg6_choose()
        self.seg7_modes()
        self.seg8_ex()

    # ---------------- Segment 1: three instruments in one box ----------------
    def seg1_three(self):
        title_segment(self, "The calibrator and its pressure modules", "Beamex MC6 — what it is, what it does", 1)
        self.sync(self.c(1, "وَالجِهَازُ ثَلَاثَةُ") - 0.6)
        self.clear()
        self.sec = section_title(self, "Three instruments in one box")
        cal = calibrator().move_to([-4.3, -0.4, 0])
        name = tag("MC6 (simplified drawing)", FS_TAG, GREY_INK).next_to(cal, DOWN, buff=0.2)
        self.play(Create(cal), FadeIn(name), run_time=0.8)
        parts = [("Meter", "reads the signals", "gauge", FLUID, "مِقْيَاسٌ"),
                 ("Generator + loop supply", "powers the transmitter", "bolt", MOVE, "وَمُوَلِّدُ"),
                 ("Documenting computer", "stores procedure and result", "database", GOOD, "وَحَاسُوبُ")]
        rows = VGroup()
        for t, sub, ic, col, _ in parts:
            box = card(t, sub, col, 5.6)
            ico = icon(ic, col, 0.55).move_to(box.frame.get_left() + RIGHT * 0.5)
            box[1].shift(RIGHT * 0.3)
            rows.add(VGroup(box, ico))
        rows.arrange(DOWN, buff=0.35).move_to([2.3, -0.4, 0])
        for r, (_, _, _, col, ph) in zip(rows, parts):
            self.sync(self.c(1, ph))
            link = Arrow(cal.case.get_right(), r[0].frame.get_left(), buff=0.1, stroke_width=3, color=col,
                         max_tip_length_to_length_ratio=0.08)
            self.play(GrowArrow(link), FadeIn(r, shift=RIGHT * 0.2), run_time=0.6)
        self.sync(self.end(1) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 2: the family ----------------
    def seg2_family(self):
        section_title(self, "The family", prev=self.sec)
        mc5 = card("MC5", f"older generation\ndiscontinued {D.MC5_DISCONTINUED}", GREY_INK, 3.2).move_to([-4.9, 1.2, 0])
        mc5is = card("MC5-IS", "intrinsically safe version", GREY_INK, 3.2).move_to([-4.9, -1.2, 0])
        mc6 = card("MC6", f"{fmt(D.MC6_SCREEN_IN)}-inch colour touch screen\n{len(D.MC6_MODES)} modes · "
                   "HART / FF / Profibus PA", FLUID, 4.4).move_to([0.2, 1.2, 0])
        kids = VGroup(card("MC6-Ex", "intrinsically safe\n(Ex ia), hazardous areas", GOOD, 3.3),
                      card("MC6-WS", "workshop\nstation", INK, 2.4),
                      card("MC6-T", "temperature\n(part 2)", LIGHT_INK, 2.4)).arrange(RIGHT, buff=0.35)
        kids.move_to([2.3, -1.6, 0])
        a1 = Arrow(mc5.frame.get_right(), mc6.frame.get_left(), buff=0.1, stroke_width=3, color=GREY_INK,
                   max_tip_length_to_length_ratio=0.1)
        a2 = Line(mc5.frame.get_bottom(), mc5is.frame.get_top(), stroke_width=3, color=GREY_INK)
        links = VGroup(*[Line(mc6.frame.get_bottom(), k.frame.get_top(), stroke_width=3, color=LIGHT_INK) for k in kids])
        shield = icon("shield-check", GOOD, 0.45).next_to(kids[0].frame, UP, buff=0.1).align_to(kids[0].frame, LEFT)
        self.play(FadeIn(mc5), run_time=0.5)
        self.sync(self.c(2, "وَلَهُ نُسْخَةٌ"))
        self.play(Create(a2), FadeIn(mc5is), run_time=0.5)
        self.sync(self.c(2, "وَإِمْ سِي سِكْس هُوَ"))
        self.play(GrowArrow(a1), FadeIn(mc6), run_time=0.6)
        for k, ph in zip(range(3), ["وَإِمْ سِي سِكْس إِكْس", "وَدَبْلْيُو", "وَتِي"]):
            self.sync(self.c(2, ph))
            anims = [Create(links[k]), FadeIn(kids[k], shift=DOWN * 0.1)]
            if k == 0:
                anims.append(FadeIn(shield))
            self.play(*anims, run_time=0.5)
        self.sync(self.end(2) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 3: the electrical side ----------------
    def seg3_electrical(self):
        section_title(self, "Transmitter output: measure, or supply and measure", prev=self.sec)

        def loop(cx, supply_label, supply_col, resistor, sup_w=2.3):
            xm = transmitter(bubble=False).scale(0.8).move_to([cx - 1.7, 0.9, 0])
            xt = tag(D.TAG, FS_TAG, FLUID).next_to(xm, UP, buff=0.12)
            cal = device("MC6\nmA in", 1.7, 1.2, FS_TAG + 2).move_to([cx + 1.6, 0.9, 0])
            sup = device(supply_label, sup_w, 0.9, FS_TAG).move_to([cx, -1.4, 0])
            sup.box.set_stroke(supply_col)
            yt = xm.body.get_right()[1] + 0.2
            top = pipe(xm.body.get_right() + UP * 0.2, [cal.box.get_left()[0], yt, 0], width=3)
            left = pipe(xm.body.get_bottom(), [xm.body.get_bottom()[0], -1.4, 0], sup.box.get_left(), width=3)
            right = pipe(cal.box.get_bottom(), [cal.box.get_bottom()[0], -1.4, 0], sup.box.get_right(), width=3)
            path = pipe(sup.box.get_left(), [xm.body.get_bottom()[0], -1.4, 0], xm.body.get_bottom(),
                        xm.body.get_right() + UP * 0.2, [cal.box.get_left()[0], yt, 0], cal.box.get_bottom(),
                        [cal.box.get_bottom()[0], -1.4, 0], sup.box.get_right(), width=3)
            g = VGroup(xm, cal, sup, top, left, right, xt)
            r = None
            if resistor:
                r = VGroup(Rectangle(width=0.7, height=0.28, color=MOVE, stroke_width=3).set_fill(WHITE, 1)
                           .move_to([cal.box.get_bottom()[0], -0.5, 0]).rotate(PI / 2))
                r.add(tag(f"{D.MC6_HART_R_EXT} Ω", FS_TAG, MOVE).next_to(r[0], RIGHT, buff=0.12))
            return g, path, r

        ga, pa, ra = loop(-3.6, "external\nloop supply", INK, True)
        gb, pb, _ = loop(3.6, f"MC6 +{D.MC6_LOOP_V} V\nloop supply", MOVE, False)
        la = tag("(a) external loop: MC6 measures", FS_TAG + 1).next_to(ga, UP, buff=0.3)
        lb = tag("(b) MC6 supplies + measures", FS_TAG + 1, MOVE).next_to(gb, UP, buff=0.3)
        self.play(FadeIn(ga), FadeIn(la), run_time=0.8)
        self.play(flow(pa, FLUID, 6), run_time=1.2)
        self.sync(self.c(3, "أَوْ يُغَذِّي"))
        self.play(FadeIn(gb), FadeIn(lb), run_time=0.8)
        self.play(flow(pb, MOVE, 6), run_time=1.2)
        self.sync(self.c(3, "وَهٰذَا الأَشْيَعُ"))
        self.play(Indicate(lb, color=MOVE), run_time=0.6)
        self.sync(self.c(3, "مُمَانَعَةُ"))
        hart = tag("HART impedance built in", FS_TAG, GOOD).next_to(gb[2].box, DOWN, buff=0.2)
        self.play(FadeIn(hart), run_time=0.5)
        self.sync(self.c(3, "مُقَاوِمَةٌ قَدْرُهَا"))
        self.play(FadeIn(ra), run_time=0.6)
        self.sync(self.c(3, "وَلَا تَتَجَاوَزْ"))
        plate = VGroup(icon("alert-triangle", BAD, 0.5),
                       tag(f"never more than {D.MC6_MAX_VDC} V DC / {D.MC6_MAX_VAC} V AC between any terminals",
                           FS_TAG + 2, BAD)).arrange(RIGHT, buff=0.2).move_to([0, -2.9, 0])
        self.play(FadeIn(plate), run_time=0.6)
        self.sync(self.end(3) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 4: open loop during current generation ----------------
    def seg4_open_loop(self):
        section_title(self, "Warning from the manual: open loop", prev=self.sec)
        cal = device(f"MC6 generates\n{fmt(D.LOOP_DEMO_MA)} mA", 2.4, 1.3, FS_TAG + 2).move_to([-5.0, 0.8, 0])
        rx = device("loop\n(receiver)", 2.0, 1.3, FS_TAG + 2).move_to([-0.6, 0.8, 0])
        top = pipe(cal.box.get_right() + UP * 0.3, rx.box.get_left() + UP * 0.3, width=3)
        bot_a = pipe(cal.box.get_right() + DOWN * 0.3, [-3.2, 0.5, 0], width=3)
        bot_b = pipe([-2.3, 0.5, 0], rx.box.get_left() + DOWN * 0.3, width=3)
        sw = Line([-3.2, 0.5, 0], [-2.3, 0.5, 0], stroke_width=4, color=INK)
        pivot = Dot([-3.2, 0.5, 0], radius=0.06, color=INK)
        swl = tag("loop contact", FS_TAG).next_to(sw, DOWN, buff=0.25)
        volt = ValueTracker(0.2)
        vbar = always_redraw(lambda: Rectangle(width=0.4, height=max(volt.get_value() * 2.0, 0.02), stroke_width=0)
                             .set_fill(MOVE, 0.9).move_to([-5.0, -2.1 + volt.get_value(), 0]))
        vframe = Rectangle(width=0.4, height=2.0, color=INK, stroke_width=2).move_to([-5.0, -1.1, 0])
        vl = tag("output voltage", FS_TAG, MOVE).next_to(vframe, RIGHT, buff=0.2)
        ch = Chart(1.3, -2.9, 5.2, 2.6, (0, 10), (0, 30), yticks=[(D.LOOP_DEMO_MA, fmt(D.LOOP_DEMO_MA, 0))],
                   xlabel="time", ylabel="loop current, mA")
        self.play(FadeIn(cal), FadeIn(rx), Create(top), Create(bot_a), Create(bot_b), Create(sw), FadeIn(pivot),
                  FadeIn(swl), run_time=0.8)
        self.play(Create(vframe), FadeIn(vbar), FadeIn(vl), Create(ch.axes), FadeIn(ch.ticks), FadeIn(ch.xl),
                  FadeIn(ch.yl), run_time=0.6)
        steady = ch.line([(0, D.LOOP_DEMO_MA), (3, D.LOOP_DEMO_MA)], MOVE, 4)
        self.play(Create(steady), run_time=0.6)
        self.sync(self.c(4, "وَانْفَتَحَتِ"))
        gap = ch.line([(3, D.LOOP_DEMO_MA), (3, 0), (5.5, 0)], MOVE, 4)
        self.play(Rotate(sw, 0.5, about_point=[-3.2, 0.5, 0]), Create(gap), run_time=0.6)
        self.sync(self.c(4, "رَفَعَ جُهْدَهُ"))
        self.play(volt.animate.set_value(1.0), vframe.animate.set_color(BAD), run_time=1.2)
        self.sync(self.c(4, "فَإِذَا أُغْلِقَتْ"))
        spike = ch.line([(5.5, 0), (5.6, 27), (6.0, D.LOOP_DEMO_MA), (8, D.LOOP_DEMO_MA)], BAD, 4)
        sl = tag("current peak", FS_TAG, BAD).next_to(ch.p(5.6, 27), RIGHT, buff=0.15)
        self.play(Rotate(sw, -0.5, about_point=[-3.2, 0.5, 0]), Create(spike), FadeIn(sl), volt.animate.set_value(0.2),
                  run_time=0.8)
        self.play(Flash(rx.box.get_left(), color=BAD, flash_radius=0.4), rx.box.animate.set_stroke(BAD), run_time=0.6)
        self.sync(self.c(4, "وَالقَاعِدَةُ"))
        rule = VGroup(icon("check", GOOD, 0.5), tag("set the output to 0 mA before connecting any loop",
                                                    FS_TAG + 2, GOOD)).arrange(RIGHT, buff=0.2)
        rule.move_to([-2.6, -3.2, 0]).align_to([-6.5, 0, 0], LEFT)
        self.play(FadeIn(rule), rx.box.animate.set_stroke(INK), vframe.animate.set_color(INK), run_time=0.6)
        self.sync(self.end(4) - 0.5)
        self.clear(self.sec, run_time=0.5)

    # ---------------- Segment 5: pressure modules ----------------
    def seg5_modules(self):
        section_title(self, "Pressure modules", prev=self.sec)
        cal = calibrator().move_to([-4.2, -0.3, 0])
        ports = VGroup(*[Circle(radius=0.14, color=FLUID, stroke_width=3) for _ in range(3)]).arrange(RIGHT, buff=0.3)
        ports.next_to(cal.case, UP, buff=0.12).shift(LEFT * 0.4)
        baro = Circle(radius=0.1, color=GREY_INK, stroke_width=3).next_to(ports, LEFT, buff=0.35)
        px = Square(side_length=0.25, color=MOVE, stroke_width=3).next_to(cal.case, RIGHT, buff=0).shift(UP * 0.8)
        self.play(FadeIn(cal), run_time=0.5)
        self.sync(self.c(5, "الدَّاخِلِيَّةُ"))
        il = tag(f"internal: up to {D.MC6_INT_MODULES} gauge / differential", FS_TAG + 2, FLUID) \
            .move_to([1.8, 2.3, 0]).align_to([-0.7, 0, 0], LEFT)
        l1 = Arrow(il.get_left(), ports[-1].get_top() + UP * 0.05, buff=0.1, stroke_width=3, color=FLUID,
                   max_tip_length_to_length_ratio=0.1)
        self.play(FadeIn(ports, lag_ratio=0.3), FadeIn(il), GrowArrow(l1), run_time=0.8)
        self.sync(self.c(5, "وَوَحْدَةٌ بَارُومِتْرِيَّةٌ"))
        bl = tag(f"+ {D.MC6_BARO_MODULES} barometric", FS_TAG + 2, GREY_INK).next_to(il, DOWN, buff=0.2).align_to(il, LEFT)
        self.play(FadeIn(baro), FadeIn(bl), run_time=0.5)
        self.sync(self.c(5, "وَالخَارِجِيَّةُ"))
        ext = device("EXT", 1.2, 0.8, FS_LABEL).move_to([0.2, -1.2, 0])
        cable = pipe(px.get_right(), [-1.2, px.get_center()[1], 0], [-1.2, -1.2, 0], ext.box.get_left(),
                     color=MOVE, width=3)
        el = tag("external module on a cable", FS_TAG + 2, MOVE).next_to(ext, RIGHT, buff=0.3)
        self.play(FadeIn(px), Create(cable), FadeIn(ext), FadeIn(el), run_time=0.8)
        self.sync(self.c(5, "مِنَ التَّفْرِيغِ"))
        bar = Line([-1.6, -2.6, 0], [6.4, -2.6, 0], stroke_width=3, color=INK)
        fill = Rectangle(width=8.0, height=0.26, stroke_width=0).set_fill(MOVE, 0.5).move_to(bar)
        ends = VGroup(tag("vacuum", FS_TAG).next_to(bar.get_start(), DOWN, buff=0.3),
                      tag(f"{D.EXT_MAX_BAR} bar", FS_TAG).next_to(bar.get_end(), DOWN, buff=0.3).align_to(bar, RIGHT))
        self.play(Create(bar), GrowFromEdge(fill, LEFT), FadeIn(ends), run_time=0.9)
        self.sync(self.c(5, "وَالبَارُومِتْرِيَّةُ تَقِيسُ"))
        eqn = VGroup(tag("gauge reading", FS_TAG + 2, FLUID), tag("+", FS_TAG + 2),
                     tag("barometric", FS_TAG + 2, GREY_INK), tag("=", FS_TAG + 2),
                     tag("absolute", FS_TAG + 2, INK, weight=BOLD)).arrange(RIGHT, buff=0.2)
        eqn.next_to(bl, DOWN, buff=0.45).align_to(il, LEFT)
        self.play(Indicate(baro, color=GREY_INK, scale_factor=1.6), run_time=0.6)
        self.sync(self.c(5, "وَبِوُجُودِهَا"))
        self.play(FadeIn(eqn, lag_ratio=0.2), run_time=1.0)
        self.sync(self.end(5) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 6: choosing the module; zero ----------------
    def seg6_choose(self):
        section_title(self, "Smallest module that covers the range", prev=self.sec)
        spec = tag("module accuracy = % of full scale + % of reading", FS_TAG + 2).move_to([0, 2.6, 0])
        self.play(FadeIn(spec), run_time=0.5)
        self.sync(self.c(6, "لِأَنَّ جُزْءًا"))
        self.play(Indicate(spec, color=MOVE), run_time=0.6)
        self.sync(self.c(6, "مِثَالٌ"))
        info = tag(f"transmitter 0–{fmt(D.URV, 0)} {D.UNIT} ≈ 0–{fmt(D.URV_BAR, 2)} bar", FS_TAG + 2, FLUID) \
            .next_to(spec, DOWN, buff=0.35)
        self.play(FadeIn(info), run_time=0.5)
        ch = Chart(-5.8, -2.6, 5.0, 3.2, (0, 2.6), (0, 0.11), yticks=[(0, "0"), (0.05, "0.05"), (0.1, "0.10")],
                   ylabel="1-year uncertainty at the top, bar")
        b1 = Rectangle(width=1.2, height=ch.p(0, D.U_SMALL_BAR)[1] - ch.y0, stroke_width=0).set_fill(GOOD, 0.85)
        b1.move_to(ch.p(0.8, D.U_SMALL_BAR / 2))
        b2 = Rectangle(width=1.2, height=ch.p(0, D.U_BIG_BAR)[1] - ch.y0, stroke_width=0).set_fill(BAD, 0.85)
        b2.move_to(ch.p(1.9, D.U_BIG_BAR / 2))
        n1 = tag(D.MOD_SMALL[0], FS_TAG + 2).next_to(b1, DOWN, buff=0.15)
        n2 = tag(D.MOD_BIG[0], FS_TAG + 2).next_to([b2.get_center()[0], ch.y0, 0], DOWN, buff=0.15)
        v1 = tag(f"±{fmt(D.U_SMALL_BAR, 3)}", FS_TAG, GOOD).next_to(b1, UP, buff=0.1)
        v2 = tag(f"±{fmt(D.U_BIG_BAR, 3)}", FS_TAG, BAD).next_to(b2, UP, buff=0.1)
        self.play(Create(ch.axes), FadeIn(ch.ticks), FadeIn(ch.yl), run_time=0.5)
        self.sync(self.c(6, "بِوَحْدَةِ سِتِّينَ"))
        self.play(GrowFromEdge(b1, DOWN), FadeIn(n1), FadeIn(v1), run_time=0.7)
        self.sync(self.c(6, "وَبِوَحْدَةِ سِتِّمِئَةٍ"))
        self.play(GrowFromEdge(b2, DOWN), FadeIn(n2), FadeIn(v2), run_time=0.8)
        self.sync(self.c(6, "أَسْوَأَ"))
        x6 = tag(f"≈ × {round(D.MOD_RATIO)} worse", FS_LABEL, BAD, weight=BOLD).next_to(v2, RIGHT, buff=0.3)
        self.play(FadeIn(x6, scale=1.3), run_time=0.5)
        # zero before work
        self.sync(self.c(6, "وَقَبْلَ كُلِّ عَمَلٍ"))
        ro = ValueTracker(D.ZERO_OFFSET_DEMO_BAR)
        box = Rectangle(width=2.6, height=0.8, color=INK, stroke_width=3).move_to([3.9, 0.2, 0])
        rd = always_redraw(lambda: tag(f"{fmt(ro.get_value(), 3)} bar", FS_LABEL).move_to(box))
        vent = VGroup(icon("wind", FLUID, 0.45), tag("port open to air", FS_TAG, FLUID)).arrange(RIGHT, buff=0.12) \
            .next_to(box, UP, buff=0.2)
        mini = Chart(1.6, -3.1, 4.6, 1.6, (0, 100), (-0.02, 0.03))
        zl = mini.hline(0, LIGHT_INK)
        dots = mini.dots([(p, D.ZERO_OFFSET_DEMO_BAR) for p in D.CAL_POINTS_PCT], BAD)
        ml = tag("same offset in every point", FS_TAG, BAD).next_to(mini.axes, UP, buff=0.12).align_to(mini.axes, LEFT)
        self.play(Create(box), FadeIn(rd), FadeIn(vent), Create(mini.axes), Create(zl), FadeIn(dots), FadeIn(ml),
                  run_time=0.8)
        self.sync(self.c(6, "وَصَفِّرِ"))
        zb = tag("Zero", FS_TAG + 2, GOOD, weight=BOLD).next_to(box, RIGHT, buff=0.3)
        ml2 = tag("offset removed in every point", FS_TAG, GOOD).move_to(ml, aligned_edge=LEFT)
        self.play(FadeIn(zb), Transform(ml, ml2), ro.animate.set_value(0.0), dots.animate.move_to([dots.get_center()[0], mini.p(0, 0)[1], 0])
                  .set_color(GOOD), run_time=1.0)
        self.sync(self.end(6) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 7: the five modes; the pen mistake ----------------
    def seg7_modes(self):
        section_title(self, "Five modes", prev=self.sec)
        descs = ["one signal,\nquick check,\nno record", "input + output,\nlive error,\nnot saved",
                 "the heart:\nprocedure, points,\nAs-Found / As-Left",
                 "value vs time:\npressure decay,\nintermittent faults",
                 "HART / FF / PA:\nread, change,\ntrim commands"]
        cues = ["المِقْيَاسُ", "وَالمُعَايِرُ:", "وَالمُعَايِرُ المُوَثِّقُ", "وَمُسَجِّلُ", "وَالمُتَّصِلُ"]
        cards = VGroup(*[card(m.replace("Documenting ", "Documenting\n"), d, FLUID if i == 2 else INK, 2.55, FS_TAG - 2)
                         for i, (m, d) in enumerate(zip(D.MC6_MODES, descs))]).arrange(RIGHT, buff=0.3)
        fit(cards, 13.0).move_to([0, 1.5, 0])
        for k, ph in enumerate(cues):
            self.sync(self.c(7, ph))
            self.play(FadeIn(cards[k], shift=DOWN * 0.15), run_time=0.45)
            if k == 2:
                heart = SurroundingRectangle(cards[2], color=FLUID, buff=0.08, corner_radius=0.15, stroke_width=6)
                self.play(Create(heart), run_time=0.4)
        # the pen mistake: two readings at two moments
        self.sync(self.c(7, "وَالخَطَأُ الأَشْيَعُ"))
        ch = Chart(-6.2, -3.0, 5.6, 1.9, (0, 10), (0, 10), xlabel="time")
        curve = ch.line([(t, 8.5 - 0.5 * t) for t in np.linspace(0, 10, 12)], FLUID, 4)
        t1, t2 = 3, 7
        r1 = DashedLine(ch.p(t1, 0), ch.p(t1, 9.5), color=BAD, stroke_width=2)
        r2 = DashedLine(ch.p(t2, 0), ch.p(t2, 9.5), color=BAD, stroke_width=2)
        lt = VGroup(tag("input read", FS_TAG, BAD).next_to(r1.get_end(), UP, buff=0.05).align_to(r1, RIGHT),
                    tag("output read later", FS_TAG, BAD).next_to(r2.get_end(), UP, buff=0.05).align_to(r2, LEFT))
        self.play(Create(ch.axes), FadeIn(ch.xl), Create(curve), run_time=0.7)
        self.play(Create(r1), Create(r2), FadeIn(lt), run_time=0.7)
        acc = VGroup(tag("synchronised readings", FS_TAG + 1, BAD),
                     tag("error from the actual input", FS_TAG + 1, BAD),
                     tag("electronic record chain", FS_TAG + 1, BAD)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.5, -2.3, 0]).align_to([0.9, 0, 0], LEFT)
        ta = 5
        ra = DashedLine(ch.p(ta, 0), ch.p(ta, 9.5), color=GOOD, stroke_width=3)
        da = Dot(ch.p(ta, 8.5 - 0.5 * ta), radius=0.08, color=GOOD)
        al = tag("documenting mode: both at once", FS_TAG, GOOD).next_to(lt, UP, buff=0.12).set_x(ra.get_x())
        lost = tag("pen and paper lose:", FS_TAG + 2, BAD, weight=BOLD).next_to(acc, UP, buff=0.2).align_to(acc, LEFT)
        self.sync(self.c(7, "فَتَضِيعُ"))
        self.play(FadeIn(lost), FadeIn(acc[0]), Create(ra), FadeIn(da), FadeIn(al), run_time=0.6)
        self.sync(self.c(7, "وَحِسَابُ"))
        self.play(FadeIn(acc[1]), run_time=0.4)
        self.sync(self.c(7, "وَسِلْسِلَةُ"))
        self.play(FadeIn(acc[2]), run_time=0.4)
        self.sync(self.end(7) - 0.6)
        self.clear(self.sec)

    # ---------------- Segment 8: not intrinsically safe ----------------
    def seg8_ex(self):
        section_title(self, "Hazardous area: two options, no third", prev=self.sec)
        zone = DashedVMobject(RoundedRectangle(width=6.4, height=4.6, corner_radius=0.4, color=BAD, stroke_width=4),
                              num_dashes=40).move_to([-3.1, -0.4, 0])
        zl = VGroup(icon("flame", BAD, 0.45), tag("classified area", FS_TAG + 2, BAD)).arrange(RIGHT, buff=0.12) \
            .next_to(zone, UP, buff=0.12).align_to(zone, LEFT)
        mc6 = device("MC6", 1.8, 1.2, FS_LABEL).move_to([-4.6, 0.2, 0])
        xm = transmitter(bubble=False).scale(0.8).move_to([-1.7, -0.9, 0])
        xm = VGroup(xm, tag(D.TAG, FS_TAG, FLUID).next_to(xm, UP, buff=0.12))
        self.play(Create(zone), FadeIn(zl), FadeIn(mc6), FadeIn(xm), run_time=0.8)
        self.sync(self.c(8, "بَطَّارِيَّتُهُ"))
        spark = VGroup(*[Line(ORIGIN, 0.35 * np.array([np.cos(a), np.sin(a), 0]), stroke_width=4, color=BAD)
                         for a in np.linspace(0, TAU, 9)[:-1]]).move_to(mc6.box.get_corner(UR))
        self.play(GrowFromCenter(spark), mc6.box.animate.set_stroke(BAD), run_time=0.5)
        nis = tag("not intrinsically\nsafe", FS_TAG + 1, BAD).next_to(mc6, DOWN, buff=0.2)
        self.play(FadeIn(nis), Create(cross(Dot(radius=0.13).next_to(mc6.box, LEFT, buff=0.15), BAD, 5, pad=0.02)), run_time=0.5)
        self.sync(self.c(8, "جِهَازٌ مُعْتَمَدٌ"))
        ex = device("MC6-Ex", 1.9, 1.2, FS_LABEL).move_to([-4.6, -1.85, 0])
        ex.box.set_stroke(GOOD)
        exl = VGroup(icon("shield-check", GOOD, 0.4), tag("option 1: approved for the area", FS_TAG + 2, GOOD)) \
            .arrange(RIGHT, buff=0.12).move_to([3.5, ex.get_y(), 0]).align_to([0.9, 0, 0], LEFT)
        exa = Arrow(exl.get_left(), ex.box.get_right(), buff=0.1, stroke_width=3, color=GOOD,
                    max_tip_length_to_length_ratio=0.08)
        self.play(FadeIn(ex), FadeIn(exl), GrowArrow(exa), run_time=0.6)
        self.sync(self.c(8, "أَوْ فَصْلُ"))
        shop = device("workshop", 2.2, 1.2, FS_LABEL).move_to([4.8, 0.9, 0])
        self.play(FadeIn(shop), run_time=0.4)
        opt2 = tag("option 2: disconnect and\ntake it to the workshop", FS_TAG + 2, GOOD).next_to(shop, UP, buff=0.55) \
            .align_to(shop, RIGHT)
        self.play(xm.animate.move_to(shop.box.get_left() + LEFT * 1.3), FadeIn(opt2), run_time=1.2)
        self.sync(self.end(8) + 1.0)


if __name__ == "__main__":
    main(__file__, "PtCalEp01", NARRATION)
