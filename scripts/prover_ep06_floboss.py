"""Daniel Compact Prover series, episode 6: the FloBoss S600+ in its field case, the web
interface and a typical proving session.

Facts follow the Emerson S600+ data sheet D301151X012, the S600+ instruction manual
D301150X412 (ch. 6, webserver) and the Config600 user manual (§5.7.3, Appendix B.2);
the field case follows the owner's description (sources in sources/prover_ep06.md).
Every screen is a simplified drawing, not a copy of a real screen. Every number and
name comes from scripts/prover_demo_data.py (illustrative values only).

Build (from the repo root):
    python scripts/prover_ep06_floboss.py --preview   # 480p15 -> tmp/prover_ep06_floboss/preview.mp4
    python scripts/prover_ep06_floboss.py             # 1080p30 -> output/prover_ep06_floboss.mp4
"""
import argparse

from style import *
import prover_demo_data as D

# Fully diacritized narration (owner-approved 2026-09-25) — one entry per scene.
NARRATION = [
    # 1 intro
    "رَأَيْنَا المُعَايِرَ فِي الحَلْقَاتِ السَّابِقَةِ، وَفِي هٰذِهِ الحَلْقَةِ نَرَى الحَاسِبَةَ الَّتِي تُدِيرُهُ: فْلُو بُوس إِسْ سِتُّمِئَةٍ بْلَس، فِي حَقِيبَتِهَا المَيْدَانِيَّةِ، ثُمَّ وَاجِهَةَ المُتَصَفِّحِ، ثُمَّ جَلْسَةَ إِثْبَاتٍ نَمُوذَجِيَّةً.",
    # 2 the S600+
    "فْلُو بُوس إِسْ سِتُّمِئَةٍ بْلَس حَاسِبَةُ تَدَفُّقٍ لِلْقِيَاسِ المَالِيِّ وَنَقْلِ المِلْكِيَّةِ، وَمِنْ تَطْبِيقَاتِهَا إِثْبَاتُ العَدَّادَاتِ. لَهَا شَاشَةٌ مِنْ ثَمَانِيَةِ أَسْطُرٍ وَلَوْحَةُ مَفَاتِيحَ، فَتُرَاجَعُ القِيَمُ وَتُعَدَّلُ دُونَ حَاسُوبٍ. وَلِلْمُعَايِرِ المُدْمَجِ تَحْتَاجُ وَحْدَةَ مُعَايِرٍ خَاصَّةً، وَتَدْعَمُ الكْرُونُومِتْرِي المُزْدَوَجَ.",
    # 3 the field case (owner's description)
    "وَفِي المَيْدَانِ تُوضَعُ الحَاسِبَةُ فِي حَقِيبَةٍ سَوْدَاءَ مَحْمُولَةٍ. عَلَى لَوْحَتِهَا وَاجِهَةُ الحَاسِبَةِ، وَفَوْقَهَا أَزْرَارٌ وَمُؤَشِّرَاتٌ لِلتَّشْغِيلِ وَطِبَاعَةِ التَّقْرِيرِ وَحَالَةِ الكَوَاشِفِ. وَفِي أَعْلَاهَا مُوَصِّلَاتُ الكَابِلَاتِ وَمِفْتَاحُ الكَهْرَبَاءِ، وَعَلَى جَانِبِهَا مَنَافِذُ الاتِّصَالِ. وَمِنْهَا تَخْرُجُ الكَابِلَاتُ إِلَى العَدَّادِ وَالمُعَايِرِ فَتَرْبِطُهَا جَمِيعًا.",
    # 4 signals
    "وَعَبْرَ هٰذِهِ الكَابِلَاتِ تَقْرَأُ الحَاسِبَةُ حَرَارَةَ المُعَايِرِ وَضَغْطَهُ عِنْدَ الدُّخُولِ وَالخُرُوجِ، وَضَغْطَ البْلِينَم، وَإِشَارَةَ الكَاشِفِ، وَنَبَضَاتِ العَدَّادِ. وَتُرْسِلُ أَوَامِرَ تَشْغِيلِ الهِيدْرُولِيك، وَإِطْلَاقِ الشَّوْطِ، وَشَحْنِ البْلِينَم أَوْ تَنْفِيسِهِ.",
    # 5 web interface
    "وَلِلْحَاسِبَةِ خَادِمُ وِيبٍ مُدْمَجٌ. نَكْتُبُ عُنْوَانَهَا فِي المُتَصَفِّحِ، ثُمَّ اسْمَ المُسْتَخْدِمِ وَكَلِمَةَ المُرُورِ، وَمُسْتَوَى الأَمَانِ يُحَدِّدُ مَا نَرَاهُ. فِي الأَعْلَى شَرِيطُ القَوَائِمِ: التَّقَارِيرُ، وَالإِنْذَارَاتُ، وَالقِيَمُ الحَالِيَّةُ، وَغَيْرُهَا، وَعَلَى اليَسَارِ شَجَرَةُ الاخْتِيَارَاتِ.",
    # 6 web rules
    "يُمْكِنُ فَتْحُ خَمْسِ جَلَسَاتٍ مَعًا، لٰكِنَّ التَّحَكُّمَ لِوَاحِدَةٍ فَقَطْ: أَوَّلُ مَنْ يَدْخُلُ يُعَدِّلُ، وَالبَاقُونَ يُشَاهِدُونَ. وَالنَّصُّ الغَامِقُ قَابِلٌ لِلتَّعْدِيلِ، وَالأَحْمَرُ فِي حَالَةِ إِنْذَارٍ. وَتُصَدَّرُ التَّقَارِيرُ مِلَفَّ سِي إِسْ فِي، أَوْ إِلَى ذَاكِرَةِ يُو إِسْ بِي. وَنَخْرُجُ دَائِمًا بِزِرِّ تَسْجِيلِ الخُرُوجِ، لَا بِإِغْلَاقِ المُتَصَفِّحِ.",
    # 7 session: login, CSUM, start, stability
    "وَالآنَ جَلْسَةٌ نَمُوذَجِيَّةٌ بِقِيَمِنَا التَّوْضِيحِيَّةِ. نَدْخُلُ إِلَى الوَاجِهَةِ، وَنَتَحَقَّقُ أَنَّ المَجْمُوعَ التَّحَقُّقِيَّ لِلْإِعْدَادِ لَمْ يَتَغَيَّرْ، فَأَيُّ تَغْيِيرٍ فِيهِ يُطْلِقُ إِنْذَارًا. ثُمَّ نَبْدَأُ الإِثْبَاتَ: تُشَغِّلُ الحَاسِبَةُ نَبَضَاتِ العَدَّادِ وَالهِيدْرُولِيك، وَتَنْتَظِرُ اسْتِقْرَارَ الحَرَارَةِ وَالضَّغْطِ وَالتَّدَفُّقِ، ثُمَّ تُبْقِيهِ مُدَّةً مُحَدَّدَةً، فَإِنْ فُقِدَ أُلْغِيَ الإِثْبَاتُ.",
    # 8 session: runs
    "ثُمَّ الجَوْلَاتُ. فِي كُلِّ شَوْطٍ تَضْبِطُ الحَاسِبَةُ البْلِينَم، وَتُطْلِقُ المِكْبَسَ، وَتَنْتَظِرُ الكَاشِفَ الأَوَّلَ ثُمَّ الثَّانِيَ، وَتَحْسُبُ، ثُمَّ تُعِيدُ المِكْبَسَ. ثَلَاثَةُ أَشْوَاطٍ فِي الجَوْلَةِ، وَخَمْسُ جَوْلَاتٍ، وَالتَّكْرَارِيَّةُ صِفْرٌ فَاصِلَةُ صِفْرٍ ثَلَاثَةٍ بِالمِئَةِ، ضِمْنَ الحَدِّ.",
    # 9 session: download, accept, report, log off
    "بَعْدَهَا تُنَزِّلُ الحَاسِبَةُ النَّتِيجَةَ: مُعَامِلُ العَدَّادِ صِفْرٌ فَاصِلَةُ تِسْعَةٍ تِسْعَةٍ تِسْعَةٍ. وَفِي إِعْدَادِنَا لَا يُسْتَعْمَلُ حَتَّى يُقْبَلَ مَحَلِّيًّا أَوْ مِنْ حَاسُوبِ الإِشْرَافِ. وَفِي نِهَايَةِ الجَوْلَاتِ تُصْدِرُ الحَاسِبَةُ تَقْرِيرَ الإِثْبَاتِ، ثُمَّ نُنْهِي التَّسَلْسُلَ، وَنَخْرُجُ مِنَ الوَاجِهَةِ.",
    # 10 summary + next
    "الخُلَاصَةُ: الحَاسِبَةُ فِي حَقِيبَتِهَا تَرْبِطُ العَدَّادَ بِالمُعَايِرِ، وَتُدِيرُ الإِثْبَاتَ مَرْحَلَةً مَرْحَلَةً، وَالمُتَصَفِّحُ يُتِيحُ مُتَابَعَتَهُ. فِي الحَلْقَةِ الأَخِيرَةِ: نُدَقِّقُ التَّقْرِيرَ، وَنُعِيدُ حِسَابَ جَوْلَةٍ خُطْوَةً خُطْوَةً.",
]

# Every spoken or shown demo value is checked against prover_demo_data; stop if it drifts.
assert D.PASSES_PER_RUN == 3 and D.RUN_COUNT == 5                  # seg 8
assert f"{D.REPEATABILITY:.2f}" == "0.03" and D.SUMMARY["repeatability_ok"]   # seg 8
assert round(D.MF_AVG, 3) == 0.999 and f"{D.MF_AVG:.5f}" == "0.99900"         # seg 9
assert (D.PROVER_SERIAL, D.METER_TAG) == ("PRV-DEMO-001", "FT-DEMO-01")
assert (D.CONFIG_NAME, D.CONFIG_CSUM) == ("DEMO_PRV_CFG", "a1b2")

AUDIO_DIR = BUILD_DIR / "prover_ep06_floboss" / "audio"

FLUID_C = "#1f5fa8"             # same group colours as episodes 3-5
DRIVE_C = "#c25a12"
MEAS_C = "#2e7d32"
ALARM_C = "#c62828"
MONO = "DejaVu Sans Mono"
DEMO_URL = "http://192.0.2.10"  # IETF documentation address (RFC 5737), not a device

# S600+ web menu bar (instruction manual Table 6-1)
MENU = ["Reports", "Alarms", "Current", "Flow Rates", "Totals", "Operator", "Plant I/O",
        "System Settings", "Tech/Engineer", "Calculations", "Diags", "Log Off"]
# Default prove sequence (Config600 Table B-14) and compact run control (Table B-17)
SEQ_START = ["IDLE", "PULSES ON", "ENABLE HYDRAULICS", "PRV FLOW/T/P STAB"]
PASS_STAGES = ["CONTROL PLENUM", "LAUNCH", "WAIT 1ST HIT", "WAIT 2ND HIT", "PASS CALCS",
               "RETRIEVE"]
SEQ_END = ["KF DOWNLOAD", "AWAIT REPROVE", "TERMINATE"]
STEPS = ["Log in", "Check CSUM", "Start prove", "Stability", f"{D.RUN_COUNT} runs × "
         f"{D.PASSES_PER_RUN} passes", "Repeatability", "MF download", "Accept",
         "Report · Log Off"]


def label(text, size=FS_LABEL, color=INK, **kw):
    return Text(text, font_size=size, color=color, **kw)


def mono(text, size=FS_TAG, color=INK, **kw):
    return Text(text, font_size=size, color=color, font=MONO, **kw)


def fit(mob, width=13.2):
    """Keep a group inside the 16:9 frame with a side margin."""
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def s600_front(height=4.6):
    """Simplified S600+ front: 8-line display, 29-key keypad, status LED."""
    w = height * 85 / 269
    body = RoundedRectangle(width=w, height=height, corner_radius=0.08, stroke_width=4,
                            color=INK, fill_color=BG, fill_opacity=1)
    disp = Rectangle(width=w * 0.84, height=height * 0.3, stroke_width=3, color=INK)
    disp.move_to(body.get_top() + DOWN * (height * 0.05 + height * 0.15))
    lines = VGroup(*[Line(LEFT, RIGHT, stroke_width=2, color=GREY_INK)
                     .set_width(w * (0.7 if k % 3 else 0.5))
                     for k in range(8)]).arrange(DOWN, buff=height * 0.3 / 11)
    lines.move_to(disp).align_to(disp, LEFT).shift(RIGHT * w * 0.06)
    keys = VGroup()
    for k in range(29):
        r, c = divmod(k, 5)
        keys.add(RoundedRectangle(width=w * 0.13, height=height * 0.045, corner_radius=0.02,
                                  stroke_width=2, color=INK)
                 .move_to([(c - 2) * w * 0.17, -r * height * 0.075, 0]))
    keys.next_to(disp, DOWN, height * 0.06)
    led = Circle(radius=w * 0.045, stroke_width=2, color=INK, fill_color=MEAS_C,
                 fill_opacity=1).move_to(body.get_bottom() + UP * height * 0.06)
    return VGroup(body, disp, lines, keys, led)


def stage_chain(names, width=10.0, size=FS_TAG - 4, color=INK):
    boxes = VGroup()
    for n in names:
        t = label(n, size, color, weight=BOLD)
        b = RoundedRectangle(width=t.width + 0.3, height=0.5, corner_radius=0.1,
                             stroke_width=3, color=GREY_INK)
        boxes.add(VGroup(b, t.move_to(b)))
    boxes.arrange(RIGHT, buff=0.4)
    arrows = VGroup(*[Arrow(boxes[k].get_right(), boxes[k + 1].get_left(), buff=0.05,
                            stroke_width=3, color=GREY_INK, max_tip_length_to_length_ratio=0.4)
                      for k in range(len(boxes) - 1)])
    chain = VGroup(boxes, arrows)
    return fit(chain, width)


class ProverEp06(SyncedScene):
    def construct(self):
        START = segment_starts(AUDIO_DIR, len(NARRATION))

        def at(seg, frac):
            return START[seg - 1] + frac * (START[seg] - START[seg - 1])

        def cue(seg, phrase):
            """Time at which `phrase` starts in segment `seg` (by text position)."""
            text = NARRATION[seg - 1]
            i = text.find(phrase)
            assert i >= 0, (seg, phrase)
            return at(seg, i / len(text))

        caption = VMobject()

        def say(text, color=INK, y=-3.3):
            nonlocal caption
            new = fit(label(text, FS_LABEL, color)).move_to([0, y, 0])
            if caption.has_points() or len(caption.submobjects):
                self.play(FadeOut(caption), run_time=0.25)
            self.play(FadeIn(new, shift=UP * 0.08), run_time=0.4)
            caption = new

        def clear(*keep, run_time=0.6):
            nonlocal caption
            gone = [m for m in self.mobjects if m not in keep]
            if gone:
                self.play(*[FadeOut(m) for m in gone], run_time=run_time)
            caption = VMobject()

        def light(chain, k, color=MEAS_C):
            box = chain[0][k]
            return AnimationGroup(box[0].animate.set_stroke(color, 5).set_fill(color, 0.12),
                                  box[1].animate.set_color(color))

        # ---------------- Segment 1: title ----------------
        series = label("Daniel Compact Prover  ·  Episode 6", FS_SUBTITLE, GREY_INK)
        title = Text("FloBoss S600+ in the Field", font_size=FS_TITLE, weight=BOLD)
        line = Line(LEFT, RIGHT).set_width(title.width)
        sub = label("field case  ·  web interface  ·  a typical proving session", FS_BODY,
                    GREY_INK)
        VGroup(series, title, line, sub).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        self.play(FadeIn(series, shift=DOWN * 0.2), run_time=0.8)
        self.sync(cue(1, "فْلُو بُوس"))
        self.play(Write(title), Create(line), run_time=1.6)
        self.sync(cue(1, "فِي حَقِيبَتِهَا"))
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.8)
        self.sync(START[1] - 0.8)
        corner = label("Ep 6 · FloBoss S600+", FS_BODY - 6, weight=BOLD).to_corner(UL, buff=0.4)
        self.play(FadeOut(VGroup(series, line, sub)), Transform(title, corner), run_time=0.8)

        def section(text):
            new = label(text, FS_BODY - 6, weight=BOLD).to_corner(UL, buff=0.4)
            self.play(Transform(title, new), run_time=0.6)

        # ---------------- Segment 2: the S600+ ----------------
        front = s600_front(4.9).move_to([-3.8, -0.3, 0])
        name = label("FloBoss S600+", FS_LABEL, weight=BOLD).next_to(front, UP, 0.15)
        self.play(Create(front[0]), FadeIn(name), run_time=0.8)
        self.play(Create(front[1]), Create(front[2]), FadeIn(front[3]), FadeIn(front[4]),
                  run_time=1.2)
        facts = VGroup(
            label("Fiscal / custody-transfer flow computer", FS_LABEL),
            label("applications include meter proving", FS_LABEL - 2, GREY_INK),
            label("8-line display  ·  29-key keypad", FS_LABEL),
            label("view or change values without a PC", FS_LABEL - 2, GREY_INK),
            label("Compact prover: Prover module (P154)", FS_LABEL, MEAS_C),
            label("dual chronometry", FS_LABEL - 2, MEAS_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        fit(facts, 7.6).move_to([2.6, 0.2, 0])
        self.sync(cue(2, "حَاسِبَةُ"))
        self.play(FadeIn(facts[0]), FadeIn(facts[1]), run_time=0.6)
        self.sync(cue(2, "لَهَا شَاشَةٌ"))
        self.play(FadeIn(facts[2]), FadeIn(facts[3]), Indicate(front[1], color=FLUID_C),
                  run_time=0.8)
        self.play(Indicate(front[3], color=FLUID_C), run_time=0.7)
        self.sync(cue(2, "وَلِلْمُعَايِرِ"))
        self.play(FadeIn(facts[4]), run_time=0.5)
        self.sync(cue(2, "وَتَدْعَمُ"))
        self.play(FadeIn(facts[5]), run_time=0.5)
        say("Emerson S600+ data sheet · Config600 manual", GREY_INK)

        # ---------------- Segment 3: the field case ----------------
        self.sync(START[2])
        clear(title)
        section("Ep 6 · The field case")
        CASE_W, CASE_H, CX, CY = 7.2, 5.4, -1.2, -0.25
        case = RoundedRectangle(width=CASE_W, height=CASE_H, corner_radius=0.3, stroke_width=6,
                                color=INK, fill_color=INK, fill_opacity=0.88).move_to([CX, CY, 0])
        handle = RoundedRectangle(width=1.6, height=0.35, corner_radius=0.15, stroke_width=6,
                                  color=INK).next_to(case, UP, 0)
        panel = RoundedRectangle(width=CASE_W - 0.7, height=CASE_H - 0.7, corner_radius=0.15,
                                 stroke_width=3, color=INK, fill_color=BG, fill_opacity=1)
        panel.move_to(case)
        self.play(FadeIn(case), Create(handle), run_time=0.8)
        self.play(FadeIn(panel), run_time=0.5)
        say("Portable black field case (owner's description)")
        # computer front, lying on the panel
        small = s600_front(2.9).move_to([CX, CY - 0.75, 0])
        brand = label("EMERSON", FS_TAG - 2, INK, weight=BOLD).next_to(small, LEFT, 0.6)
        self.sync(cue(3, "عَلَى لَوْحَتِهَا"))
        self.play(FadeIn(small), FadeIn(brand), run_time=0.7)
        # buttons and lamps above the computer
        btn_y = CY + 1.0
        run_b = VGroup(Circle(radius=0.14, stroke_width=3, color=INK, fill_color=MEAS_C,
                              fill_opacity=0.8), label("RUN", FS_TAG - 6, INK, weight=BOLD))
        prt_b = VGroup(Circle(radius=0.14, stroke_width=3, color=INK, fill_color=FLUID_C,
                              fill_opacity=0.6), label("PRINT REPORT", FS_TAG - 6, INK, weight=BOLD))
        det_l = VGroup(Circle(radius=0.14, stroke_width=3, color=INK, fill_color=DRIVE_C,
                              fill_opacity=0.8), label("DETECTORS", FS_TAG - 6, INK, weight=BOLD))
        buttons = VGroup()
        for b in (run_b, prt_b, det_l):
            b[1].next_to(b[0], DOWN, 0.06)
            buttons.add(b)
        buttons.arrange(RIGHT, buff=0.55).move_to([CX, btn_y, 0])
        self.sync(cue(3, "وَفَوْقَهَا"))
        self.play(LaggedStart(*[FadeIn(b) for b in buttons], lag_ratio=0.3), run_time=1.0)
        # top row: round connectors, power switch, two fuses
        top_y = CY + CASE_H / 2 - 0.75
        conns = VGroup(*[VGroup(Circle(radius=0.2, stroke_width=3, color=INK),
                                Circle(radius=0.08, stroke_width=2, color=INK))
                         for _ in range(4)]).arrange(RIGHT, buff=0.3)
        power = VGroup(Rectangle(width=0.5, height=0.32, stroke_width=3, color=INK),
                       Line(UP * 0.12, DOWN * 0.12, stroke_width=4, color=ALARM_C))
        power_t = label("POWER", FS_TAG - 8, INK).next_to(power, DOWN, 0.04)
        fuses = VGroup(*[RoundedRectangle(width=0.36, height=0.16, corner_radius=0.07,
                                          stroke_width=3, color=INK) for _ in range(2)])
        fuses.arrange(DOWN, buff=0.1)
        fuse_t = label("FUSES", FS_TAG - 8, INK).next_to(fuses, DOWN, 0.04)
        top = VGroup(conns, VGroup(power, power_t), VGroup(fuses, fuse_t)).arrange(RIGHT, buff=0.5)
        top.move_to([CX, top_y, 0])
        self.sync(cue(3, "وَفِي أَعْلَاهَا"))
        self.play(FadeIn(top), run_time=0.8)
        # side: communication ports and two ventilation openings
        side_x = CX + CASE_W / 2 - 0.9
        ports = VGroup(*[VGroup(Rectangle(width=0.36, height=0.22, stroke_width=3, color=INK),
                                label(t, FS_TAG - 9, INK)) for t in ("Modbus", "Printer", "Network")])
        for p in ports:
            p[1].next_to(p[0], DOWN, 0.03)
        ports.arrange(DOWN, buff=0.12).move_to([side_x, CY + 0.15, 0])
        vents = VGroup(*[VGroup(*[Line(LEFT * 0.22, RIGHT * 0.22, stroke_width=3, color=GREY_INK)
                                  for _ in range(4)]).arrange(DOWN, buff=0.07) for _ in range(2)])
        vents.arrange(DOWN, buff=0.25).move_to([side_x, CY - 1.65, 0])
        self.sync(cue(3, "وَعَلَى جَانِبِهَا"))
        self.play(FadeIn(ports), FadeIn(vents), run_time=0.8)
        # cables to the meter and the prover
        meter = VGroup(RoundedRectangle(width=2.4, height=0.9, corner_radius=0.1, stroke_width=4,
                                        color=FLUID_C),
                       label("Meter", FS_LABEL, FLUID_C, weight=BOLD))
        meter.add(label(D.METER_TAG, FS_TAG - 4, GREY_INK))
        meter[1:].arrange(DOWN, buff=0.05).move_to(meter[0])
        meter.move_to([5.4, 1.2, 0])
        prover = VGroup(RoundedRectangle(width=2.4, height=0.9, corner_radius=0.1, stroke_width=4,
                                         color=DRIVE_C),
                        label("Prover", FS_LABEL, DRIVE_C, weight=BOLD))
        prover.add(label(D.PROVER_SERIAL, FS_TAG - 4, GREY_INK))
        prover[1:].arrange(DOWN, buff=0.05).move_to(prover[0])
        prover.move_to([5.4, -1.6, 0])
        start_m = np.array([CX + CASE_W / 2, CY + 1.3, 0])
        c_meter = VMobject().set_points_smoothly([start_m, start_m + RIGHT * 0.7 + UP * 0.1,
                                                   meter.get_left() + LEFT * 0.7,
                                                   meter.get_left()])
        c_meter.set_stroke(INK, 5)
        start_p = np.array([CX + CASE_W / 2, CY - 1.1, 0])
        c_prov = VMobject().set_points_smoothly([start_p, start_p + RIGHT * 0.7 + DOWN * 0.1,
                                                  prover.get_left() + LEFT * 0.7,
                                                  prover.get_left()])
        c_prov.set_stroke(INK, 5)
        self.sync(cue(3, "وَمِنْهَا"))
        self.play(FadeIn(meter), FadeIn(prover), run_time=0.5)
        self.play(Create(c_meter), Create(c_prov), run_time=1.2)
        say("Cables link the computer, the meter and the prover")

        # ---------------- Segment 4: signals ----------------
        self.sync(START[3])
        case_all = VGroup(case, handle, panel, small, brand, buttons, top, ports, vents)
        self.play(FadeOut(VGroup(c_meter, c_prov)), FadeOut(caption), run_time=0.4)
        caption = VMobject()
        self.play(case_all.animate.scale(0.5).move_to([-4.5, 0.9, 0]),
                  meter.animate.move_to([4.9, 2.1, 0]), prover.animate.move_to([4.9, 0.1, 0]),
                  run_time=1.0)
        section("Ep 6 · Signals")
        edge = case_all.get_right()
        ins = VGroup(label("prover inlet / outlet temperature", FS_TAG),
                     label("prover inlet / outlet pressure", FS_TAG),
                     label("plenum pressure", FS_TAG),
                     label("detector switch", FS_TAG))
        ins.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        outs = VGroup(label("hydraulics on / off", FS_TAG),
                      label("launch (RUN)", FS_TAG),
                      label("plenum charge / vent", FS_TAG))
        outs.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        pulses = label("meter pulses", FS_TAG)
        ex_ = edge[0]
        a_pulse = Arrow(meter.get_left(), [ex_, 1.7, 0], buff=0.15, stroke_width=4,
                        color=FLUID_C, max_tip_length_to_length_ratio=0.06)
        a_in = Arrow(prover.get_left() + UP * 0.2, [ex_, 0.75, 0], buff=0.15, stroke_width=4,
                     color=DRIVE_C, max_tip_length_to_length_ratio=0.06)
        a_out = Arrow([ex_, 0.25, 0], prover.get_left() + DOWN * 0.25, buff=0.15,
                      stroke_width=4, color=MEAS_C, max_tip_length_to_length_ratio=0.06)
        pulses.set_color(FLUID_C).next_to(a_pulse.get_center(), UP, 0.1)
        in_t = label("IN  (from the prover)", FS_TAG, DRIVE_C, weight=BOLD)
        in_grp = VGroup(in_t, ins).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        in_grp.set_color(DRIVE_C).move_to([-3.2, -1.95, 0])
        out_t = label("OUT  (to the prover)", FS_TAG, MEAS_C, weight=BOLD)
        out_grp = VGroup(out_t, outs).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        out_grp.set_color(MEAS_C).move_to([3.0, -1.85, 0])
        self.play(GrowArrow(a_in), FadeIn(in_grp[0]), run_time=0.6)
        for k, phrase in enumerate(["حَرَارَةَ", "وَضَغْطَهُ", "وَضَغْطَ البْلِينَم", "وَإِشَارَةَ"]):
            self.sync(cue(4, phrase))
            self.play(FadeIn(ins[k], shift=RIGHT * 0.1), run_time=0.4)
        self.sync(cue(4, "وَنَبَضَاتِ"))
        self.play(GrowArrow(a_pulse), FadeIn(pulses), run_time=0.6)
        self.sync(cue(4, "وَتُرْسِلُ"))
        self.play(GrowArrow(a_out), FadeIn(out_grp[0]), run_time=0.6)
        for k, phrase in enumerate(["تَشْغِيلِ", "وَإِطْلَاقِ", "وَشَحْنِ"]):
            self.sync(cue(4, phrase))
            self.play(FadeIn(outs[k], shift=RIGHT * 0.1), run_time=0.4)
        say("Config600 manual, Appendix B.2.1", GREY_INK)

        # ---------------- Segments 5-6: web interface ----------------
        self.sync(START[4])
        clear(title)
        section("Ep 6 · Web interface")
        WIN_W, WIN_H, WY = 12.6, 5.2, -0.25
        win = RoundedRectangle(width=WIN_W, height=WIN_H, corner_radius=0.12, stroke_width=4,
                               color=INK).move_to([0, WY, 0])
        bar_y = WY + WIN_H / 2 - 0.35
        tbar = Line([-WIN_W / 2, bar_y - 0.35, 0], [WIN_W / 2, bar_y - 0.35, 0], stroke_width=3,
                    color=INK)
        dots = VGroup(*[Circle(radius=0.07, stroke_width=2, color=INK) for _ in range(3)])
        dots.arrange(RIGHT, buff=0.1).move_to([-WIN_W / 2 + 0.45, bar_y, 0])
        addr_box = RoundedRectangle(width=6.5, height=0.42, corner_radius=0.1, stroke_width=2,
                                    color=GREY_INK).move_to([-1.2, bar_y, 0])
        self.play(Create(win), Create(tbar), FadeIn(dots), Create(addr_box), run_time=1.0)
        say("Embedded web server (S600+ manual, ch. 6)")
        self.sync(cue(5, "نَكْتُبُ"))
        addr = mono(DEMO_URL, FS_TAG - 2).move_to(addr_box).align_to(addr_box, LEFT).shift(RIGHT * 0.2)
        self.play(AddTextLetterByLetter(addr), run_time=1.2)
        self.sync(cue(5, "ثُمَّ اسْمَ"))
        dlg = RoundedRectangle(width=5.0, height=2.3, corner_radius=0.1, stroke_width=4,
                               color=INK, fill_color=BG, fill_opacity=1).move_to([0, WY - 0.2, 0])
        dlg_t = VGroup(label("User name", FS_TAG), label("Password", FS_TAG))
        dlg_t.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(dlg).shift(LEFT * 1.3 + UP * 0.2)
        fields = VGroup(*[Rectangle(width=2.2, height=0.36, stroke_width=2, color=GREY_INK)
                          .next_to(t, RIGHT, 0.35) for t in dlg_t])
        for f in fields:
            f.set_x(dlg.get_x() + 1.0)
        dots_pw = mono("••••••", FS_TAG).move_to(fields[1])
        user = mono("operator", FS_TAG - 2).move_to(fields[0])
        ok = VGroup(RoundedRectangle(width=0.9, height=0.36, corner_radius=0.08, stroke_width=2,
                                     color=INK), label("OK", FS_TAG - 4, weight=BOLD))
        ok[1].move_to(ok[0])
        ok.next_to(fields, DOWN, 0.3).align_to(fields, RIGHT)
        self.play(FadeIn(dlg), FadeIn(dlg_t), FadeIn(fields), run_time=0.6)
        self.play(FadeIn(user), FadeIn(dots_pw), FadeIn(ok), run_time=0.6)
        self.sync(cue(5, "وَمُسْتَوَى"))
        say("The security level decides what each user sees", DRIVE_C)
        # menu bar, hierarchy tree, display area
        menu = VGroup(*[label(m, FS_TAG - 6, ALARM_C if m == "Log Off" else INK, weight=BOLD)
                        for m in MENU]).arrange(RIGHT, buff=0.26)
        fit(menu, WIN_W - 0.5).move_to([0, bar_y - 0.62, 0])
        m_line = Line([-WIN_W / 2, bar_y - 0.9, 0], [WIN_W / 2, bar_y - 0.9, 0], stroke_width=2,
                      color=GREY_INK)
        tree_x = -WIN_W / 2 + 2.6
        t_line = Line([tree_x, bar_y - 0.9, 0], [tree_x, WY - WIN_H / 2, 0], stroke_width=2,
                      color=GREY_INK)
        tree = VGroup(label("▾ Reports", FS_TAG - 4, weight=BOLD),
                      label("   Current", FS_TAG - 4), label("   Prove", FS_TAG - 4),
                      label("   Alarm log", FS_TAG - 4), label("   Event log", FS_TAG - 4))
        tree.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        tree.move_to([-WIN_W / 2 + 0.25 + tree.width / 2, bar_y - 1.1 - tree.height / 2, 0])
        area_c = [(tree_x + WIN_W / 2) / 2, WY - 0.55, 0]
        rows = VGroup(*[mono(t, FS_TAG - 4, c, weight=w) for t, c, w in (
            (f"Prover            {D.PROVER_SERIAL}", INK, NORMAL),
            (f"Meter             {D.METER_TAG}", INK, NORMAL),
            ("Plenum pressure   68.0 psig", INK, BOLD),
            ("Prover temp.      30.0 C", INK, NORMAL),
            ("Detector          ALARM", ALARM_C, BOLD))]).arrange(DOWN, aligned_edge=LEFT,
                                                                   buff=0.2)
        rows.move_to(area_c)
        self.sync(cue(5, "فِي الأَعْلَى"))
        self.play(FadeOut(VGroup(dlg, dlg_t, fields, user, dots_pw, ok)), run_time=0.4)
        self.play(FadeIn(menu, lag_ratio=0.1), Create(m_line), run_time=1.2)
        for k, phrase in enumerate(["التَّقَارِيرُ", "وَالإِنْذَارَاتُ", "وَالقِيَمُ"]):
            self.sync(cue(5, phrase))
            self.play(Indicate(menu[k], color=FLUID_C), run_time=0.6)
        self.sync(cue(5, "وَعَلَى اليَسَارِ"))
        self.play(Create(t_line), FadeIn(tree, lag_ratio=0.2), run_time=0.8)
        self.play(FadeIn(rows), run_time=0.6)
        say("Menu bar on top  ·  hierarchy menu on the left  ·  display area", GREY_INK)

        # Segment 6: web rules
        self.sync(START[5])
        self.play(FadeOut(rows), run_time=0.3)
        pcs = VGroup()
        for k in range(5):
            scr = RoundedRectangle(width=0.9, height=0.6, corner_radius=0.05, stroke_width=3,
                                   color=MEAS_C if k == 0 else GREY_INK)
            base = Line(LEFT * 0.2, RIGHT * 0.2, stroke_width=3,
                        color=MEAS_C if k == 0 else GREY_INK).next_to(scr, DOWN, 0.06)
            tag = label("control" if k == 0 else "view", FS_TAG - 6,
                        MEAS_C if k == 0 else GREY_INK, weight=BOLD if k == 0 else NORMAL)
            tag.next_to(base, DOWN, 0.06)
            pcs.add(VGroup(scr, base, tag))
        pcs.arrange(RIGHT, buff=0.35).move_to([area_c[0], WY + 0.6, 0])
        self.play(LaggedStart(*[FadeIn(p) for p in pcs], lag_ratio=0.2), run_time=1.0)
        say("Up to 5 sessions  ·  only one point of control", MEAS_C)
        self.sync(cue(6, "وَالنَّصُّ"))
        ex = VGroup(mono("Plenum pressure   68.0 psig", FS_TAG - 2, weight=BOLD),
                    mono("Detector          ALARM", FS_TAG - 2, ALARM_C, weight=BOLD))
        ex.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([area_c[0] - 1.0, WY - 1.0, 0])
        ex_t = VGroup(label("bold = can be changed", FS_TAG - 2, INK),
                      label("red = in alarm", FS_TAG - 2, ALARM_C))
        for t, e in zip(ex_t, ex):
            t.next_to(e, RIGHT, 0.5)
        self.play(FadeIn(ex[0]), FadeIn(ex_t[0]), run_time=0.5)
        self.play(FadeIn(ex[1]), FadeIn(ex_t[1]), run_time=0.5)
        self.sync(cue(6, "وَتُصَدَّرُ"))
        csv = VGroup(RoundedRectangle(width=0.9, height=0.4, corner_radius=0.08, stroke_width=3,
                                      color=FLUID_C), label("CSV", FS_TAG - 4, FLUID_C, weight=BOLD))
        csv[1].move_to(csv[0])
        usb = VGroup(RoundedRectangle(width=0.9, height=0.4, corner_radius=0.08, stroke_width=3,
                                      color=FLUID_C), label("USB", FS_TAG - 4, FLUID_C, weight=BOLD))
        usb[1].move_to(usb[0])
        exp = VGroup(csv, usb).arrange(RIGHT, buff=0.3).move_to([area_c[0], WY - 2.2, 0])
        self.play(FadeIn(exp), run_time=0.5)
        say("Export: CSV button on screen, or USB flash drive", FLUID_C)
        self.sync(cue(6, "وَنَخْرُجُ"))
        self.play(Circumscribe(menu[-1], color=ALARM_C, time_width=0.8), run_time=1.2)
        say("Always Log Off — do not just close the browser", ALARM_C)

        # ---------------- Segments 7-9: typical proving session ----------------
        self.sync(START[6])
        clear(title)
        section("Ep 6 · A typical proving session (demo values)")
        steps = VGroup(*[label(f"{k + 1}  {s}", FS_TAG - 2, GREY_INK) for k, s in enumerate(STEPS)])
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-5.35, -0.2, 0])
        s_line = Line([-3.3, 2.6, 0], [-3.3, -3.0, 0], stroke_width=2, color=GREY_INK)
        self.play(FadeIn(steps, lag_ratio=0.1), Create(s_line), run_time=1.2)
        R_X = 1.8                                   # centre of the right-hand work area
        cur = [None]

        def step(k):
            new = label(f"{k + 1}  {STEPS[k]}", FS_TAG - 2, MEAS_C, weight=BOLD)
            new.move_to(steps[k]).align_to(steps[k], LEFT)
            anims = [Transform(steps[k], new)]
            if cur[0] is not None:
                done = label(f"{cur[0] + 1}  {STEPS[cur[0]]}  ✓", FS_TAG - 2, INK)
                done.move_to(steps[cur[0]]).align_to(steps[cur[0]], LEFT)
                anims.append(Transform(steps[cur[0]], done))
            self.play(*anims, run_time=0.4)
            cur[0] = k

        step(0)
        login = mono(f"{DEMO_URL}   user: operator   ✓", FS_TAG - 2).move_to([R_X, 2.3, 0])
        self.play(FadeIn(login), run_time=0.5)
        self.sync(cue(7, "وَنَتَحَقَّقُ"))
        step(1)
        cfg = VGroup(mono(f"Config  {D.CONFIG_NAME}", FS_LABEL - 2, weight=BOLD),
                     mono(f"CSUM    {D.CONFIG_CSUM}   ✓ unchanged", FS_LABEL - 2, MEAS_C,
                          weight=BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        cfg.move_to([R_X, 1.35, 0])
        self.play(FadeIn(cfg), run_time=0.6)
        self.sync(cue(7, "فَأَيُّ"))
        say("Any change raises the CONF CSUM alarm (Config600)", ALARM_C)
        self.sync(cue(7, "ثُمَّ نَبْدَأُ"))
        step(2)
        chain1 = stage_chain(SEQ_START, 9.8).move_to([R_X, 0.0, 0])
        self.play(FadeIn(chain1), run_time=0.6)
        self.play(light(chain1, 0), run_time=0.3)
        self.play(light(chain1, 1), run_time=0.4)
        self.play(light(chain1, 2), run_time=0.4)
        self.sync(cue(7, "وَتَنْتَظِرُ"))
        step(3)
        self.play(light(chain1, 3, DRIVE_C), run_time=0.5)
        stab = VGroup(label("wait for stable T, P and flow  →  hold for a set time", FS_TAG),
                      label("stability lost during the hold  →  prove aborted", FS_TAG, ALARM_C))
        stab.arrange(DOWN, buff=0.15).move_to([R_X, -1.2, 0])
        self.play(FadeIn(stab[0]), run_time=0.5)
        self.sync(cue(7, "فَإِنْ فُقِدَ"))
        self.play(FadeIn(stab[1]), run_time=0.5)

        # Segment 8: runs
        self.sync(START[7])
        self.play(FadeOut(VGroup(login, cfg, chain1, stab)), FadeOut(caption), run_time=0.5)
        caption = VMobject()
        step(4)
        chain2 = stage_chain(PASS_STAGES, 9.8).move_to([R_X, 2.3, 0])
        loop = CurvedArrow(chain2[0][-1].get_bottom() + DOWN * 0.05,
                           chain2[0][0].get_bottom() + DOWN * 0.05, angle=-TAU / 10,
                           stroke_width=3, color=GREY_INK, tip_length=0.15)
        loop_t = label("next pass", FS_TAG - 6, GREY_INK).next_to(loop, DOWN, 0.05)
        self.play(FadeIn(chain2), run_time=0.6)
        for k, phrase in enumerate(["تَضْبِطُ", "وَتُطْلِقُ", "وَتَنْتَظِرُ", "ثُمَّ الثَّانِيَ",
                                    "وَتَحْسُبُ", "ثُمَّ تُعِيدُ"]):
            self.sync(cue(8, phrase))
            self.play(light(chain2, k), run_time=0.35)
        self.play(Create(loop), FadeIn(loop_t), run_time=0.5)
        self.sync(cue(8, "ثَلَاثَةُ"))
        hdr = mono(f"{'RUN':<5}{'PASSES':>7}{'M-FACTOR':>11}{'K-FACTOR':>12}", FS_TAG - 2,
                   weight=BOLD)
        lines = VGroup(hdr, *[mono(f"{r['run']:<5}{D.PASSES_PER_RUN:>7}{r['mf']:>11.5f}"
                                   f"{r['k']:>12.3f}", FS_TAG - 2) for r in D.RUNS])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([R_X, -0.55, 0])
        self.play(FadeIn(lines[0]), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(l) for l in lines[1:]], lag_ratio=0.25), run_time=1.4)
        self.sync(cue(8, "وَالتَّكْرَارِيَّةُ"))
        step(5)
        rep = label(f"Repeatability {D.REPEATABILITY:.2f} %  ≤  {D.REPEATABILITY_LIMIT:.2f} %  ✓",
                    FS_LABEL, MEAS_C, weight=BOLD).next_to(lines, DOWN, 0.3)
        self.play(FadeIn(rep), run_time=0.6)

        # Segment 9: download, accept, report, log off
        self.sync(START[8])
        self.play(FadeOut(VGroup(chain2, loop, loop_t, lines, rep)), run_time=0.5)
        step(6)
        chain3 = stage_chain(SEQ_END, 9.8).move_to([R_X, 2.3, 0])
        self.play(FadeIn(chain3), run_time=0.5)
        self.play(light(chain3, 0), run_time=0.4)
        mf = label(f"(MF = {D.MF_AVG:.5f})", FS_LABEL, MEAS_C, weight=BOLD)
        mf.next_to(chain3[0][0], DOWN, 0.2)
        self.play(FadeIn(mf), run_time=0.5)
        self.sync(cue(9, "وَفِي إِعْدَادِنَا"))
        step(7)
        acc = label("used only after it is accepted: locally or by the supervisory computer",
                    FS_TAG, DRIVE_C)
        fit(acc, 9.6).next_to(mf, DOWN, 0.3).set_x(R_X)
        self.play(FadeIn(acc), run_time=0.5)
        self.sync(cue(9, "وَفِي نِهَايَةِ"))
        step(8)
        self.play(FadeOut(VGroup(mf, acc)), run_time=0.3)
        rpt_lines = [
            (f"METER PROOF REPORT                 {D.PROVING_DATE}", BOLD),
            (f"PROVER {D.PROVER_SERIAL}   METER {D.METER_TAG}", NORMAL),
            (f"CONFIG {D.CONFIG_NAME}   CSUM {D.CONFIG_CSUM}", NORMAL),
            (f"BASE VOL {D.BPV:.4f} m3   RATE {D.FLOW_RATE:.1f} m3/h", NORMAL),
            (f"STD DENSITY {D.RHO_15:.1f} kg/m3", NORMAL),
            (f"{'RUN':<5}{'PULSES':>11}{'M-FACTOR':>11}{'K-FACTOR':>12}", BOLD),
            *[(f"{r['run']:<5}{r['pulses']:>11.3f}{r['mf']:>11.5f}{r['k']:>12.3f}", NORMAL)
              for r in D.RUNS],
            (f"MF {D.MF_AVG:.5f}   K {D.K_FINAL:.3f}   REPEAT. {D.REPEATABILITY:.2f} %", BOLD),
        ]
        rpt = VGroup(*[mono(t, FS_TAG - 6, weight=w) for t, w in rpt_lines])
        rpt.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        paper = Rectangle(width=rpt.width + 0.5, height=rpt.height + 0.4, stroke_width=3,
                          color=INK)
        report = VGroup(paper, rpt.move_to(paper)).move_to([R_X, -0.6, 0])
        self.play(light(chain3, 1), run_time=0.3)
        self.play(FadeIn(paper), Write(rpt), run_time=1.6)
        self.play(light(chain3, 2), run_time=0.4)
        self.sync(cue(9, "وَنَخْرُجُ"))
        say("Log Off", ALARM_C)
        self.sync(START[9] - 0.3)
        done = label(f"9  {STEPS[8]}  ✓", FS_TAG - 2, INK).move_to(steps[8]).align_to(steps[8], LEFT)
        self.play(Transform(steps[8], done), run_time=0.3)

        # ---------------- Segment 10: summary + next ----------------
        self.sync(START[9])
        clear(title)
        section("Ep 6 · Summary")
        summ = VGroup(
            label("1   The field case links the computer, the meter and the prover", FS_SUMMARY),
            label("2   The S600+ runs the prove stage by stage", FS_SUMMARY),
            label("3   The web interface lets you follow it", FS_SUMMARY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        fit(summ).move_to([0, 0.6, 0])
        for k, phrase in enumerate(["الحَاسِبَةُ فِي", "وَتُدِيرُ", "وَالمُتَصَفِّحُ"]):
            self.sync(cue(10, phrase))
            self.play(FadeIn(summ[k], shift=RIGHT * 0.2), run_time=0.5)
        self.sync(cue(10, "فِي الحَلْقَةِ"))
        say("Next: auditing the report — recompute one run step by step", GREY_INK, y=-2.4)
        self.sync(START[10] + 2.0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="low-quality layout check")
    args = parser.parse_args()
    print(build(__file__, "ProverEp06", NARRATION, preview=args.preview))
