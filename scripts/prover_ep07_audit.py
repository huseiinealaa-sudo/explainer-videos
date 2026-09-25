"""Daniel Compact Prover series, episode 7: auditing the proving report and recomputing
one run step by step.

Audit practices follow Coastal Flow (report contents, MF shift), NFOGM (H. James), 43 CFR
3174.11, the API MPMS 4.8 contents and the Emerson ROC800L flow calculations manual ch. 6
(sources in sources/prover_ep07.md). The report is the simplified one of episode 6, with
the temperatures and correction factors added. Every number and name comes from
scripts/prover_demo_data.py (illustrative values only).

Build (from the repo root):
    python scripts/prover_ep07_audit.py --preview   # 480p15 -> tmp/prover_ep07_audit/preview.mp4
    python scripts/prover_ep07_audit.py             # 1080p30 -> output/prover_ep07_audit.mp4
"""
import argparse

from style import *
import prover_demo_data as D

# Fully diacritized narration (owner-approved 2026-09-25) — one entry per scene.
NARRATION = [
    # 1 intro
    "هٰذِهِ الحَلْقَةُ الأَخِيرَةُ مِنَ السِّلْسِلَةِ. نَأْخُذُ تَقْرِيرَ الإِثْبَاتِ المُبَسَّطَ مِنَ الحَلْقَةِ السَّادِسَةِ، فَنُدَقِّقُ بُنُودَهُ، ثُمَّ نُعِيدُ حِسَابَ الجَوْلَةِ الأُولَى خُطْوَةً خُطْوَةً.",
    # 2 purpose of the report
    "الغَايَةُ مِنَ التَّقْرِيرِ أَنْ يَحْمِلَ مَا يَكْفِي لِإِعَادَةِ حِسَابِ مُعَامِلِ العَدَّادِ فِي أَيِّ وَقْتٍ بَعْدَ الإِثْبَاتِ، فَيُعَرِّفُ المُعَايِرَ وَحَجْمَهُ، وَالعَدَّادَ. وَفِي إِيهْ بِي آي أَرْبَعَةٍ فَاصِلَةِ ثَمَانِيَةٍ قِسْمٌ لِتَقْيِيمِ نَتَائِجِ الإِثْبَاتِ.",
    # 3 identifiers and CSUM
    "نَبْدَأُ بِالمُعَرِّفَاتِ: رَقْمُ المُعَايِرِ، وَوَسْمُ العَدَّادِ، وَتَارِيخُ الإِثْبَاتِ، وَاسْمُ الإِعْدَادِ وَمَجْمُوعُهُ التَّحَقُّقِيُّ. نُقَارِنُ المَجْمُوعَ التَّحَقُّقِيَّ بِالقِيمَةِ المُعْتَمَدَةِ، كَمَا رَأَيْنَا فِي الحَلْقَةِ السَّادِسَةِ؛ فَإِنْ تَغَيَّرَ فَقَدْ تَغَيَّرَ الإِعْدَادُ، وَلَا نَثِقُ بِالأَرْقَامِ حَتَّى نَعْرِفَ السَّبَبَ.",
    # 4 base volume
    "ثُمَّ الحَجْمُ: عَدَّادُنَا بَعْدَ المُعَايِرِ، فَالصَّحِيحُ حَجْمُ أَسْفَلِ المَجْرَى، صِفْرٌ فَاصِلَةُ اثْنَيْنِ أَرْبَعَةٍ سِتَّةٍ ثَلَاثَةٍ مِتْرٍ مُكَعَّبٍ، كَمَا شَرَحْنَا فِي الحَلْقَةِ الخَامِسَةِ. وَنُطَابِقُهُ مَعَ شَهَادَةِ الوُوتَر دْرُو السَّارِيَةِ.",
    # 5 temperature and pressure
    "ثُمَّ الحَرَارَةُ وَالضَّغْطُ. المُعَايِرُ عِنْدَ ثَلَاثِينَ دَرَجَةً، وَالعَدَّادُ عِنْدَ تِسْعٍ وَعِشْرِينَ فَاصِلَةِ تِسْعٍ، فَالفَرْقُ عُشْرُ دَرَجَةٍ. وَالفَرْقُ مَقْبُولٌ مَا دَامَ ثَابِتًا مِنْ جَوْلَةٍ إِلَى جَوْلَةٍ، وَمِنْ إِثْبَاتٍ إِلَى آخَرَ. وَنَتَأَكَّدُ أَنَّ مُعَامِلَاتِ الضَّغْطِ فِي التَّقْرِيرِ هِيَ المُسْتَعْمَلَةُ فِي الحِسَابِ.",
    # 6 Table 54B
    "ثُمَّ جَدْوَلُ أَرْبَعَةٍ وَخَمْسِينَ بِي، إِصْدَارُ عَامِ أَلْفٍ وَتِسْعِمِئَةٍ وَثَمَانِينَ بِالوَحَدَاتِ الدَّوْلِيَّةِ. الكَثَافَةُ القِيَاسِيَّةُ ثَمَانُمِئَةٍ وَأَرْبَعُونَ، فَتَقَعُ فِي مَجْمُوعَةِ زُيُوتِ الوَقُودِ. وَنَتَحَقَّقُ أَنَّ الحَاسِبَةَ تَسْتَعْمِلُ ثَوَابِتَ هٰذِهِ المَجْمُوعَةِ، بِالدَّرَجَةِ المِئَوِيَّةِ لَا الفَهْرَنْهَايْتِيَّةِ.",
    # 7 repeatability and MF shift
    "ثُمَّ التَّكْرَارِيَّةُ: صِفْرٌ فَاصِلَةُ صِفْرٍ ثَلَاثَةٍ بِالمِئَةِ لِخَمْسِ جَوْلَاتٍ، ضِمْنَ حَدِّ صِفْرٍ فَاصِلَةِ صِفْرٍ خَمْسَةٍ، كَمَا فِي الحَلْقَةِ الثَّانِيَةِ. وَنُقَارِنُ المُعَامِلَ الجَدِيدَ بِالسَّابِقِ: فَمِنَ المُمَارَسَاتِ الشَّائِعَةِ أَلَّا يَتَغَيَّرَ بَيْنَ إِثْبَاتَيْنِ مُتَتَالِيَيْنِ أَكْثَرَ مِنْ رُبْعٍ فِي المِئَةِ، وَيُحَدِّدُ كُلُّ مُشَغِّلٍ أَوْ عَقْدٍ حَدَّهُ؛ فَإِنْ تَجَاوَزَهُ بُحِثَ عَنِ السَّبَبِ. وَرَسْمُ المُعَامِلَاتِ عَلَى مُخَطَّطٍ زَمَنِيٍّ يَكْشِفُ التَّغَيُّرَ التَّدْرِيجِيَّ.",
    # 8 step 1: corrected prover volume
    "الآنَ نُعِيدُ حِسَابَ الجَوْلَةِ الأُولَى، بِتَسَلْسُلِ إِيهْ بِي آي اثْنَيْ عَشَرَ فَاصِلَةِ اثْنَيْنِ. أَوَّلًا: حَجْمُ المُعَايِرِ المُصَحَّحُ يُسَاوِي الحَجْمَ الأَسَاسِيَّ، فِي سِي تِي إِسْ بِي مِنَ الحَلْقَةِ الخَامِسَةِ، وَسِي بِي إِسْ بِي، وَسِي تِي إِلْ بِي مِنَ الجَدْوَلِ، وَسِي بِي إِلْ بِي. وَالنَّاتِجُ صِفْرٌ فَاصِلَةُ اثْنَيْنِ أَرْبَعَةٍ ثَلَاثَةٍ اثْنَيْنِ ثَمَانِيَةٍ سِتَّةٍ مِتْرٍ مُكَعَّبٍ.",
    # 9 step 2: corrected meter volume
    "ثَانِيًا: حَجْمُ العَدَّادِ. النَّبَضَاتُ المُسْتَكْمَلَةُ مِنَ الحَلْقَةِ الخَامِسَةِ، أَرْبَعَةَ عَشَرَ أَلْفًا وَسَبْعُمِئَةٍ وَسِتٌّ وَتِسْعُونَ فَاصِلَةُ وَاحِدٍ سِتَّةٍ أَرْبَعَةٍ، نَقْسِمُهَا عَلَى كِي الاسْمِيِّ، سِتِّينَ أَلْفًا، ثُمَّ نَضْرِبُ فِي سِي تِي إِلْ إِمْ وَسِي بِي إِلْ إِمْ، فَنَحْصُلُ عَلَى صِفْرٍ فَاصِلَةِ اثْنَيْنِ أَرْبَعَةٍ ثَلَاثَةٍ خَمْسَةٍ ثَلَاثَةٍ صِفْرٍ.",
    # 10 step 3: MF + rounding
    "ثَالِثًا: مُعَامِلُ العَدَّادِ، كَمَا فِي الحَلْقَةِ الأُولَى: حَجْمُ المُعَايِرِ مَقْسُومًا عَلَى حَجْمِ العَدَّادِ، يُسَاوِي صِفْرًا فَاصِلَةَ تِسْعَةٍ تِسْعَةٍ تِسْعَةٍ صِفْرٍ صِفْرٍ، وَهُوَ مَا فِي التَّقْرِيرِ. وَالحَاسِبَاتُ تُقَرِّبُ المُعَامِلَاتِ وَالأَحْجَامَ بِقَوَاعِدَ مُحَدَّدَةٍ، فَنُعِيدُ الحِسَابَ بِقَوَاعِدِ التَّقْرِيبِ نَفْسِهَا، وَقَدْ يَخْتَلِفُ الرَّقْمُ الأَخِيرُ.",
    # 11 series summary
    "وَبِهٰذَا تَكْتَمِلُ السِّلْسِلَةُ: المُعَايِرُ المُدْمَجُ يُوَفِّرُ حَجْمًا مَرْجِعِيًّا دَقِيقًا، وَالحَاسِبَةُ تُحَوِّلُ النَّبَضَاتِ وَالتَّصْحِيحَاتِ إِلَى مُعَامِلٍ لِلْعَدَّادِ. وَالتَّقْرِيرُ الجَيِّدُ يُتِيحُ لِأَيِّ مُدَقِّقٍ أَنْ يُعِيدَ حِسَابَ هٰذَا المُعَامِلِ خُطْوَةً خُطْوَةً، فَيَصِلَ إِلَى الرَّقْمِ نَفْسِهِ.",
]

# Every spoken or shown demo value is checked against prover_demo_data; stop if it drifts.
assert f"{D.BPV_DOWNSTREAM:.4f}" == "0.2463"                                   # seg 4
assert (D.T_PROVER, D.T_METER) == (30.0, 29.9)                                 # seg 5
assert round(D.T_PROVER - D.T_METER, 6) == 0.1                                 # seg 5 "0.1"
assert D.RHO_15 == 840.0 and D.GROUP[0] == "Fuel oils"                         # seg 6
assert f"{D.REPEATABILITY:.2f}" == "0.03" and D.RUN_COUNT == 5                 # seg 7
assert D.REPEATABILITY_LIMIT == 0.05 and D.SUMMARY["repeatability_ok"]         # seg 7
assert D.MF_SHIFT_COMMON == 0.25                                               # seg 7 "1/4 %"
assert f"{D.PRV_VOL:.6f}" == "0.243286"                                        # seg 8
assert f"{D.CTSP:.6f}" == "1.000324"                                           # seg 8 (ep 5)
assert f"{D.RUN1['pulses']:.3f}" == "14796.164" and D.K_NOMINAL == 60000       # seg 9
assert f"{D.RUN1['mtr_vol']:.6f}" == "0.243530"                                # seg 9
assert f"{D.RUN1['mf']:.5f}" == "0.99900"                                      # seg 10
assert f"{D.PRV_VOL / D.RUN1['mtr_vol']:.5f}" == "0.99900"                     # seg 10

AUDIO_DIR = BUILD_DIR / "prover_ep07_audit" / "audio"

FLUID_C = "#1f5fa8"             # same colours as episodes 3-6
DRIVE_C = "#c25a12"
MEAS_C = "#2e7d32"
ALARM_C = "#c62828"
MONO = "DejaVu Sans Mono"
R_X = 3.45                      # centre of the right-hand column
R_W = 6.3                       # max width of the right-hand column


def label(text, size=FS_LABEL, color=INK, **kw):
    return Text(text, font_size=size, color=color, **kw)


def mono(text, size=FS_TAG, color=INK, **kw):
    return Text(text, font_size=size, color=color, font=MONO, **kw)


def fit(mob, width=13.2):
    """Keep a group inside the 16:9 frame with a side margin."""
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def ep_tag(n, color=GREY_INK):
    return label(f"Ep {n}", FS_TAG - 2, color, weight=BOLD)


def eqn(*parts, size=FS_EQUATION, color=INK, buff=0.18):
    """Equation built from Text pieces (no LaTeX in the container), indexable by part."""
    return VGroup(*[Text(p, font_size=size, color=color) for p in parts]).arrange(RIGHT,
                                                                                  buff=buff)


def report_lines():
    """The simplified episode 6 report, with temperatures and factors added."""
    r = D.RUNS
    return [
        (f"METER PROOF REPORT           {D.PROVING_DATE}", BOLD),                 # 0
        (f"PROVER {D.PROVER_SERIAL}   METER {D.METER_TAG}", NORMAL),              # 1
        (f"CONFIG {D.CONFIG_NAME}   CSUM {D.CONFIG_CSUM}", NORMAL),               # 2
        (f"BASE VOL {D.BPV_DOWNSTREAM:.4f} m3 (DOWNSTREAM)", NORMAL),              # 3
        (f"RATE {D.FLOW_RATE:.1f} m3/h   STD DENS {D.RHO_15:.1f}", NORMAL),        # 4
        (f"TEMP  PRV {D.T_PROVER:.1f} C   MTR {D.T_METER:.1f} C", NORMAL),         # 5
        (f"CTSp {D.CTSP:.6f}   CPSp {D.CPSP:.6f}", NORMAL),                         # 6
        (f"CTLp {D.CTLP:.6f}   CPLp {D.CPLP:.6f}", NORMAL),                         # 7
        (f"CTLm {D.CTLM:.6f}   CPLm {D.CPLM:.6f}", NORMAL),                         # 8
        (f"TABLE 54B (1980, SI)  {D.GROUP[0].upper()}", NORMAL),                    # 9
        (f"{'RUN':<4}{'PULSES':>11}{'M-FACTOR':>10}{'K-FACTOR':>11}", BOLD),        # 10
        *[(f"{x['run']:<4}{x['pulses']:>11.3f}{x['mf']:>10.5f}{x['k']:>11.3f}", NORMAL)
          for x in r],                                                              # 11-15
        (f"MF {D.MF_AVG:.5f}  K {D.K_FINAL:.3f}  REP {D.REPEATABILITY:.2f} %", BOLD),  # 16
    ]


class ProverEp07(SyncedScene):
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

        # ---------------- Segment 1: title ----------------
        series = label("Daniel Compact Prover  ·  Episode 7", FS_SUBTITLE, GREY_INK)
        title = Text("Auditing the Proving Report", font_size=FS_TITLE, weight=BOLD)
        line = Line(LEFT, RIGHT).set_width(title.width)
        sub = label("check the report  ·  recompute run 1 step by step", FS_BODY, GREY_INK)
        VGroup(series, title, line, sub).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        self.play(FadeIn(series, shift=DOWN * 0.2), run_time=0.8)
        self.play(Write(title), Create(line), run_time=1.6)
        self.sync(cue(1, "فَنُدَقِّقُ"))
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.8)
        self.sync(START[1] - 0.8)
        corner = label("Ep 7 · The report", FS_BODY - 6, weight=BOLD).to_corner(UL, buff=0.4)
        self.play(FadeOut(VGroup(series, line, sub)), Transform(title, corner), run_time=0.8)

        def section(text):
            new = label(text, FS_BODY - 6, weight=BOLD).to_corner(UL, buff=0.4)
            self.play(Transform(title, new), run_time=0.6)

        # ---------------- Segment 2: the report and its purpose ----------------
        rpt = VGroup(*[mono(t, FS_TAG - 6, weight=w) for t, w in report_lines()])
        rpt.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        paper = Rectangle(width=rpt.width + 0.5, height=rpt.height + 0.4, stroke_width=3,
                          color=INK)
        report = VGroup(paper, rpt.move_to(paper))
        report.scale_to_fit_height(5.7)
        if report.width > 6.4:
            report.scale_to_fit_width(6.4)
        report.move_to([-3.45, -0.05, 0])
        src = label("simplified report from Ep 6 (illustrative values)", FS_TAG - 4, GREY_INK)
        src.next_to(report, DOWN, 0.08)
        self.play(Create(paper), run_time=0.6)
        self.play(Write(rpt), FadeIn(src), run_time=2.2)

        goal = VGroup(label("Goal of the report", FS_BODY - 2, weight=BOLD),
                      label("enough data to recalculate the MF", FS_LABEL),
                      label("at any time after the proving", FS_LABEL),
                      label("identifies the prover, its volume, the meter", FS_LABEL - 2,
                            GREY_INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        fit(goal, R_W).move_to([R_X, 1.2, 0])
        api = VGroup(label("API MPMS 4.8", FS_LABEL, FLUID_C, weight=BOLD),
                     label("Assessment of Proving Results", FS_LABEL, FLUID_C))
        api.arrange(DOWN, buff=0.12)
        api_box = SurroundingRectangle(api, buff=0.2, color=FLUID_C, stroke_width=3,
                                       corner_radius=0.1)
        api_g = fit(VGroup(api_box, api), R_W).move_to([R_X, -1.4, 0])
        self.sync(cue(2, "الغَايَةُ") + 0.3)
        self.play(FadeIn(goal[0]), FadeIn(goal[1]), FadeIn(goal[2]), run_time=0.8)
        self.sync(cue(2, "فَيُعَرِّفُ"))
        self.play(FadeIn(goal[3]), run_time=0.5)
        self.sync(cue(2, "وَفِي إِيهْ"))
        self.play(Create(api_box), FadeIn(api), run_time=0.8)
        self.sync(START[2] - 0.5)
        self.play(FadeOut(VGroup(goal, api_g)), run_time=0.5)

        # Audit checklist (right column) + highlight on the report (left)
        CHECKS = ["Identifiers & CSUM", "Base volume", "Temperature & pressure",
                  "Table 54B group", "Repeatability & MF shift"]
        checklist = VGroup(*[label(f"{k + 1}  {c}", FS_LABEL - 2, GREY_INK)
                             for k, c in enumerate(CHECKS)])
        checklist.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        fit(checklist, R_W).align_to([0.55, 0, 0], LEFT).to_edge(UP, buff=0.45)
        hl = VMobject()

        def highlight(idx, color=MEAS_C):
            nonlocal hl
            box = SurroundingRectangle(VGroup(*[rpt[i] for i in idx]), buff=0.06,
                                       color=color, stroke_width=4, corner_radius=0.05)
            anims = [FadeOut(hl)] if hl.has_points() else []
            self.play(*anims, Create(box), run_time=0.5)
            hl = box

        def check(k):
            new = label(f"{k + 1}  {CHECKS[k]}", FS_LABEL - 2, INK, weight=BOLD)
            new.scale(checklist[k].height / new.height * 1.0)
            new.move_to(checklist[k]).align_to(checklist[k], LEFT)
            anims = []
            if k > 0:
                done = label(f"{k}  {CHECKS[k - 1]}  ✓", FS_LABEL - 2, MEAS_C)
                done.scale(checklist[k - 1].height / label(f"{k}  {CHECKS[k - 1]}",
                                                          FS_LABEL - 2).height)
                done.move_to(checklist[k - 1]).align_to(checklist[k - 1], LEFT)
                anims.append(Transform(checklist[k - 1], done))
            self.play(Transform(checklist[k], new), *anims, run_time=0.4)

        body = VGroup()

        def show_body(*lines):
            nonlocal body
            new = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            fit(new, R_W).next_to(checklist, DOWN, 0.45).align_to(checklist, LEFT)
            if len(body.submobjects):
                self.play(FadeOut(body), run_time=0.3)
            body = new
            return new

        # ---------------- Segment 3: identifiers and CSUM ----------------
        self.sync(START[2])
        section("Ep 7 · Audit the report")
        self.play(FadeIn(checklist), run_time=0.6)
        check(0)
        highlight([0, 1, 2])
        ids = show_body(
            label(f"Prover  {D.PROVER_SERIAL}", FS_LABEL),
            label(f"Meter   {D.METER_TAG}", FS_LABEL),
            label(f"Date    {D.PROVING_DATE}", FS_LABEL),
            label(f"Config  {D.CONFIG_NAME}", FS_LABEL))
        self.play(LaggedStart(*[FadeIn(m) for m in ids], lag_ratio=0.3), run_time=1.4)
        self.sync(cue(3, "نُقَارِنُ"))
        highlight([2])
        csum = VGroup(label(f"CSUM {D.CONFIG_CSUM}  =  approved {D.CONFIG_CSUM}  ✓", FS_LABEL,
                            MEAS_C, weight=BOLD),
                      ep_tag(6)).arrange(RIGHT, buff=0.3)
        fit(csum, R_W).next_to(ids, DOWN, 0.35).align_to(ids, LEFT)
        self.play(FadeIn(csum), run_time=0.6)
        body.add(csum)
        self.sync(cue(3, "فَإِنْ تَغَيَّرَ"))
        warn = label("changed → configuration changed → find the cause first", FS_TAG, ALARM_C)
        fit(warn, R_W).next_to(csum, DOWN, 0.25).align_to(ids, LEFT)
        self.play(FadeIn(warn), run_time=0.6)
        body.add(warn)

        # ---------------- Segment 4: base volume ----------------
        self.sync(START[3])
        check(1)
        highlight([3])
        vol = show_body(
            label("Meter downstream of the prover", FS_LABEL),
            VGroup(label(f"Downstream volume {D.BPV_DOWNSTREAM:.4f} m³  ✓", FS_LABEL, MEAS_C,
                         weight=BOLD), ep_tag(5)).arrange(RIGHT, buff=0.3),
            label(f"(upstream {D.BPV_UPSTREAM:.6f} m³: meter upstream only)", FS_TAG,
                  GREY_INK))
        self.play(FadeIn(vol[0]), run_time=0.5)
        self.sync(cue(4, "حَجْمُ أَسْفَلِ"))
        self.play(FadeIn(vol[1]), run_time=0.6)
        self.play(FadeIn(vol[2]), run_time=0.5)
        self.sync(cue(4, "وَنُطَابِقُهُ"))
        cert = label("= valid waterdraw certificate", FS_LABEL, FLUID_C)
        fit(cert, R_W).next_to(vol, DOWN, 0.3).align_to(vol, LEFT)
        self.play(FadeIn(cert), run_time=0.6)
        body.add(cert)

        # ---------------- Segment 5: temperature and pressure ----------------
        self.sync(START[4])
        check(2)
        highlight([5])
        dt = D.T_PROVER - D.T_METER
        tp = show_body(
            label(f"Prover {D.T_PROVER:.1f} °C   Meter {D.T_METER:.1f} °C", FS_LABEL),
            label(f"ΔT = {dt:.1f} °C", FS_LABEL, weight=BOLD))
        self.play(FadeIn(tp[0]), run_time=0.5)
        self.sync(cue(5, "فَالفَرْقُ"))
        self.play(FadeIn(tp[1]), run_time=0.5)
        self.sync(cue(5, "وَالفَرْقُ مَقْبُولٌ"))
        ok = VGroup(label("OK if it stays consistent", FS_LABEL - 2, MEAS_C),
                    label("run to run  ·  prove to prove", FS_LABEL - 2, MEAS_C))
        ok.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fit(ok, R_W).next_to(tp, DOWN, 0.3).align_to(tp, LEFT)
        self.play(FadeIn(ok), run_time=0.6)
        body.add(ok)
        self.sync(cue(5, "وَنَتَأَكَّدُ"))
        highlight([7, 8])
        cpl = label(f"CPLp {D.CPLP:.6f}  ·  CPLm {D.CPLM:.6f} → used in the calculation",
                    FS_TAG, FLUID_C)
        fit(cpl, R_W).next_to(ok, DOWN, 0.3).align_to(tp, LEFT)
        self.play(FadeIn(cpl), run_time=0.6)
        body.add(cpl)

        # ---------------- Segment 6: Table 54B ----------------
        self.sync(START[5])
        check(3)
        highlight([9])
        lo, hi = D.GROUP[1], D.GROUP[2]
        t54 = show_body(
            label("Table 54B  (1980, SI)", FS_LABEL, weight=BOLD),
            label(f"ρ15 = {D.RHO_15:.1f} kg/m³", FS_LABEL),
            label(f"{D.GROUP[0]}:  {lo} ≤ ρ < {hi:.0f}", FS_LABEL, MEAS_C, weight=BOLD),
            label("constants per °C  (not the per °F set)", FS_LABEL - 2, DRIVE_C))
        self.play(FadeIn(t54[0]), run_time=0.5)
        self.sync(cue(6, "الكَثَافَةُ"))
        self.play(FadeIn(t54[1]), run_time=0.5)
        self.sync(cue(6, "فَتَقَعُ"))
        self.play(FadeIn(t54[2]), run_time=0.5)
        self.sync(cue(6, "وَنَتَحَقَّقُ"))
        highlight([7, 8])
        self.play(FadeIn(t54[3]), run_time=0.5)
        ctl = label(f"→ CTLp {D.CTLP:.6f}   CTLm {D.CTLM:.6f}", FS_TAG, FLUID_C)
        fit(ctl, R_W).next_to(t54, DOWN, 0.25).align_to(t54, LEFT)
        self.play(FadeIn(ctl), run_time=0.5)
        body.add(ctl)

        # ---------------- Segment 7: repeatability and MF shift ----------------
        self.sync(START[6])
        check(4)
        highlight([16])
        rep = show_body(VGroup(
            label(f"Repeatability {D.REPEATABILITY:.2f} %  ≤  {D.REPEATABILITY_LIMIT:.2f} %  ✓",
                  FS_LABEL, MEAS_C, weight=BOLD),
            label(f"{D.RUN_COUNT} runs", FS_TAG, MEAS_C), ep_tag(2)).arrange(RIGHT, buff=0.3))
        self.play(FadeIn(rep), run_time=0.6)
        self.sync(cue(7, "وَنُقَارِنُ"))
        shift = VGroup(label(f"|new MF − previous MF|  ≤  {D.MF_SHIFT_COMMON} %", FS_LABEL,
                             weight=BOLD),
                       label("common practice · limit set by operator or contract", FS_TAG,
                             GREY_INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fit(shift, R_W).next_to(rep, DOWN, 0.3).align_to(rep, LEFT)
        self.play(FadeIn(shift), run_time=0.7)
        body.add(shift)
        self.sync(cue(7, "فَإِنْ تَجَاوَزَهُ"))
        inv = label("exceeded → investigate the cause", FS_TAG, ALARM_C)
        fit(inv, R_W).next_to(shift, DOWN, 0.15).align_to(rep, LEFT)
        self.play(FadeIn(inv), run_time=0.5)
        body.add(inv)
        self.sync(cue(7, "وَرَسْمُ"))
        # Schematic MF control chart (no values): a band around the mean, gradual drift.
        cw, ch = 5.4, 1.2
        cx = checklist.get_left()[0] + cw / 2 + 0.05
        cy = inv.get_bottom()[1] - 0.45 - ch / 2
        axis = VGroup(Line([cx - cw / 2, cy - ch / 2, 0], [cx + cw / 2, cy - ch / 2, 0]),
                      Line([cx - cw / 2, cy - ch / 2, 0], [cx - cw / 2, cy + ch / 2, 0]))
        axis.set_stroke(INK, 2)
        mid = DashedLine([cx - cw / 2, cy, 0], [cx + cw / 2, cy, 0], stroke_width=2,
                         color=GREY_INK)
        band = VGroup(*[DashedLine([cx - cw / 2, cy + s * ch * 0.38, 0],
                                   [cx + cw / 2, cy + s * ch * 0.38, 0], stroke_width=2,
                                   color=DRIVE_C) for s in (1, -1)])
        ys = [0.02, -0.05, 0.04, 0.0, 0.06, 0.1, 0.15, 0.2, 0.28, 0.44]
        dots = VGroup(*[Dot([cx - cw / 2 + 0.4 + k * (cw - 0.7) / (len(ys) - 1),
                             cy + y * ch, 0], radius=0.06,
                            color=ALARM_C if y * ch > ch * 0.38 else INK)
                        for k, y in enumerate(ys)])
        chart_t = label("MF history (schematic)", FS_TAG - 4, GREY_INK)
        chart_t.next_to(axis, UP, 0.05).align_to(axis, LEFT).shift(RIGHT * 0.1)
        self.play(Create(axis), Create(mid), Create(band), FadeIn(chart_t), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.2),
                  run_time=1.6)
        body.add(axis, mid, band, dots, chart_t)
        self.sync(START[7] - 0.3)
        done = label(f"5  {CHECKS[4]}  ✓", FS_LABEL - 2, MEAS_C)
        done.scale(checklist[4].height / label(f"5  {CHECKS[4]}", FS_LABEL - 2).height)
        done.move_to(checklist[4]).align_to(checklist[4], LEFT)
        self.play(Transform(checklist[4], done), run_time=0.3)

        # ---------------- Segment 8: step 1, corrected prover volume ----------------
        self.sync(START[7])
        clear(title)
        section("Ep 7 · Recompute run 1")
        seq = label("sequence: API MPMS 12.2", FS_TAG, GREY_INK).to_corner(UR, buff=0.45)
        self.play(FadeIn(seq), run_time=0.4)
        s1 = label("1  Corrected prover volume", FS_BODY, FLUID_C, weight=BOLD)
        s1.move_to([0, 2.5, 0])
        eq1 = eqn("Vp", "=", "BPV", "×", "CTSp", "×", "CPSp", "×", "CTLp", "×", "CPLp")
        eq1.move_to([0, 1.3, 0])
        val1 = eqn("=", f"{D.BPV_DOWNSTREAM:.4f}", "×", f"{D.CTSP:.6f}", "×", f"{D.CPSP:.6f}", "×",
                   f"{D.CTLP:.6f}", "×", f"{D.CPLP:.6f}", size=FS_EQUATION - 6)
        fit(val1).move_to([0, 0.2, 0])
        tags1 = VGroup(ep_tag(5, FLUID_C).next_to(val1[3], DOWN, 0.15),
                       label("54B", FS_TAG - 2, FLUID_C, weight=BOLD).next_to(val1[7], DOWN, 0.15))
        res1 = eqn("Vp", "=", f"{D.PRV_VOL:.6f}", "m³", size=FS_EQUATION + 4, color=FLUID_C)
        res1.move_to([0, -1.5, 0])
        res1_box = SurroundingRectangle(res1, buff=0.2, color=FLUID_C, stroke_width=4,
                                        corner_radius=0.1)
        self.play(FadeIn(s1), run_time=0.5)
        self.sync(cue(8, "حَجْمُ المُعَايِرِ"))
        self.play(Write(eq1), run_time=1.6)
        self.sync(cue(8, "فِي سِي تِي"))
        self.play(FadeIn(val1[:4]), FadeIn(tags1[0]), run_time=0.8)
        self.sync(cue(8, "وَسِي بِي إِسْ"))
        self.play(FadeIn(val1[4:6]), run_time=0.5)
        self.sync(cue(8, "وَسِي تِي إِلْ"))
        self.play(FadeIn(val1[6:8]), FadeIn(tags1[1]), run_time=0.5)
        self.sync(cue(8, "وَسِي بِي إِلْ"))
        self.play(FadeIn(val1[8:]), run_time=0.5)
        self.sync(cue(8, "وَالنَّاتِجُ"))
        self.play(Write(res1), Create(res1_box), run_time=1.2)

        # ---------------- Segment 9: step 2, corrected meter volume ----------------
        self.sync(START[8])
        vp_keep = VGroup(res1, res1_box)
        self.play(FadeOut(VGroup(s1, eq1, val1, tags1)),
                  vp_keep.animate.scale(0.7).move_to([-4.3, 2.55, 0]), run_time=0.8)
        s2 = label("2  Corrected meter volume", FS_BODY, DRIVE_C, weight=BOLD)
        s2.move_to([0, 1.85, 0])
        self.play(FadeIn(s2), run_time=0.5)
        self.sync(cue(9, "النَّبَضَاتُ"))
        iv = eqn("IV", "=", f"{D.RUN1['pulses']:.3f} ÷ {D.K_NOMINAL:.0f}", "=", f"{D.RUN1_IV:.6f}",
                 "m³").move_to([0, 0.75, 0])
        pul_tag = VGroup(label("interpolated pulses", FS_TAG - 2, DRIVE_C), ep_tag(5, DRIVE_C))
        pul_tag.arrange(RIGHT, buff=0.2).next_to(iv[2], UP, 0.15)
        self.play(Write(iv[:3]), FadeIn(pul_tag), run_time=1.4)
        self.sync(cue(9, "نَقْسِمُهَا"))
        self.play(Indicate(iv[2], color=DRIVE_C), run_time=0.8)
        self.play(FadeIn(iv[3:]), run_time=0.6)
        self.sync(cue(9, "ثُمَّ نَضْرِبُ"))
        eq2 = eqn("Vm", "=", "IV", "×", "CTLm", "×", "CPLm", "=", f"{D.RUN1_IV:.6f}", "×",
                  f"{D.CTLM:.6f}", "×", f"{D.CPLM:.6f}", size=FS_EQUATION - 6)
        fit(eq2).move_to([0, -0.55, 0])
        self.play(Write(eq2), run_time=1.8)
        self.sync(cue(9, "فَنَحْصُلُ"))
        res2 = eqn("Vm", "=", f"{D.RUN1['mtr_vol']:.6f}", "m³", size=FS_EQUATION + 4,
                   color=DRIVE_C).move_to([0, -1.9, 0])
        res2_box = SurroundingRectangle(res2, buff=0.2, color=DRIVE_C, stroke_width=4,
                                        corner_radius=0.1)
        self.play(Write(res2), Create(res2_box), run_time=1.2)

        # ---------------- Segment 10: step 3, MF ----------------
        self.sync(START[9])
        vm_keep = VGroup(res2, res2_box)
        self.play(FadeOut(VGroup(s2, iv, pul_tag, eq2)),
                  vm_keep.animate.scale(0.7).move_to([4.3, 2.55, 0]), run_time=0.8)
        s3 = VGroup(label("3  Meter factor", FS_BODY, MEAS_C, weight=BOLD), ep_tag(1, MEAS_C))
        s3.arrange(RIGHT, buff=0.3).move_to([0, 1.55, 0])
        self.play(FadeIn(s3), run_time=0.5)
        self.sync(cue(10, "حَجْمُ المُعَايِرِ"))
        eq3 = eqn("MF", "=", "Vp ÷ Vm", "=", f"{D.PRV_VOL:.6f} ÷ {D.RUN1['mtr_vol']:.6f}", "=",
                  f"{D.RUN1['mf']:.5f}", size=FS_EQUATION + 2)
        eq3.move_to([0, 0.2, 0])
        self.play(Write(eq3[:5]), run_time=1.6)
        self.sync(cue(10, "يُسَاوِي"))
        self.play(Write(eq3[5:]), run_time=0.8)
        box3 = SurroundingRectangle(eq3[6], buff=0.15, color=MEAS_C, stroke_width=4,
                                    corner_radius=0.08)
        self.play(Create(box3), run_time=0.5)
        self.sync(cue(10, "وَهُوَ مَا"))
        match = mono(f"REPORT  RUN 1  M-FACTOR {D.RUNS[0]['mf']:.5f}   ✓", FS_TAG, MEAS_C,
                     weight=BOLD).move_to([0, -1.2, 0])
        self.play(FadeIn(match, shift=UP * 0.1), run_time=0.6)
        self.sync(cue(10, "وَالحَاسِبَاتُ"))
        rnd = VGroup(label("Flow computers round factors and volumes by fixed rules", FS_LABEL,
                           GREY_INK),
                     label("→ recompute with the same rounding; the last digit may differ",
                           FS_LABEL, GREY_INK)).arrange(DOWN, buff=0.12)
        fit(rnd).move_to([0, -2.55, 0])
        self.play(FadeIn(rnd), run_time=0.8)

        # ---------------- Segment 11: series summary ----------------
        self.sync(START[10])
        clear(title)
        section("Daniel Compact Prover · Series summary")
        summ = VGroup(
            label("The compact prover gives an accurate reference volume", FS_SUMMARY),
            label("The flow computer turns pulses and corrections into the MF", FS_SUMMARY),
            label("A good report lets any auditor recompute the MF", FS_SUMMARY,
                  weight=BOLD),
            label("step by step, and reach the same number", FS_SUMMARY, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        fit(summ).move_to([0, 0.5, 0])
        for k, phrase in enumerate(["المُعَايِرُ المُدْمَجُ", "وَالحَاسِبَةُ",
                                    "وَالتَّقْرِيرُ", "خُطْوَةً خُطْوَةً"]):
            self.sync(cue(11, phrase))
            self.play(FadeIn(summ[k], shift=RIGHT * 0.2), run_time=0.5)
        self.sync(START[11] - 0.4)
        end = label("End of series  ·  thank you", FS_BODY, GREY_INK).move_to(DOWN * 2.4)
        self.play(FadeIn(end, shift=UP * 0.1), run_time=0.8)
        self.sync(START[11] + 2.0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="low-quality layout check")
    args = parser.parse_args()
    print(build(__file__, "ProverEp07", NARRATION, preview=args.preview))
