"""Scene gallery: one clip per function of the scene library (explainer/scenes.py).

A catalogue to pick scenes from for new projects: each segment names one function in
the narration, shows its name in the top-left corner and a one-line description at the
bottom, then runs the function with illustrative values from scene_gallery_data.py.

Build (from the repo root):
    python projects/scene_gallery/template_scene_gallery.py --preview   # -> tmp/template_scene_gallery/preview.mp4
    python projects/scene_gallery/template_scene_gallery.py             # -> output/template_scene_gallery.mp4
"""
from pathlib import Path

from explainer import *
import scene_gallery_data as D

# Fully diacritized narration (owner-approved <date>) — one entry per segment.
NARRATION = [
    # 1 intro
    "هٰذَا كَتَالُوجُ مَكْتَبَةِ المَشَاهِدِ. نَعْرِضُ فِيهِ سَبْعَ عَشْرَةَ دَالَّةً، كُلَّ دَالَّةٍ فِي مَقْطَعٍ مُسْتَقِلٍّ، وَاسْمُهَا مَكْتُوبٌ عَلَى الشَّاشَةِ.",
    # 2 title_card
    "المَشْهَدُ الأَوَّلُ: بِطَاقَةُ العُنْوَانِ. تَفْتَتِحُ الفِيدْيُو بِسَطْرٍ لِلسِّلْسِلَةِ، وَعُنْوَانٍ رَئِيسِيٍّ، وَعُنْوَانٍ فَرْعِيٍّ.",
    # 3 section_title
    "الثَّانِي: عُنْوَانُ القِسْمِ. يَظْهَرُ صَغِيرًا فِي الزَّاوِيَةِ، ثُمَّ يَتَحَوَّلُ إِلَى عُنْوَانِ القِسْمِ التَّالِي.",
    # 4 bullet_list
    "الثَّالِثُ: قَائِمَةُ النِّقَاطِ. تَظْهَرُ كُلُّ نُقْطَةٍ لَحْظَةَ ذِكْرِهَا: الأُولَى، ثُمَّ الثَّانِيَةُ، ثُمَّ الثَّالِثَةُ.",
    # 5 equation
    "الرَّابِعُ: المُعَادَلَةُ. تُبْنَى مِنْ قِطَعٍ نَصِّيَّةٍ، فَنُلَوِّنُ أَيَّ جُزْءٍ مِنْهَا، أَوْ نُحِيطُهُ بِإِطَارٍ.",
    # 6 worked_calculation
    "الخَامِسُ: الحِسَابُ خُطْوَةً خُطْوَةً. المُعَادَلَةُ، ثُمَّ التَّعْوِيضُ بِالقِيَمِ، ثُمَّ النَّتِيجَةُ فِي إِطَارٍ.",
    # 7 labeled_diagram
    "السَّادِسُ: الرَّسْمُ المُعَلَّمُ. نَرْسُمُ الشَّكْلَ، ثُمَّ نُضِيفُ إِلَيْهِ تَسْمِيَاتٍ مُرَقَّمَةً بِأَسْهُمٍ.",
    # 8 process_flow
    "السَّابِعُ: مُخَطَّطُ الخُطُوَاتِ. صَنَادِيقُ تَصِلُ بَيْنَهَا أَسْهُمٌ، ثُمَّ نُضِيءُ الخُطْوَةَ الَّتِي نَشْرَحُهَا.",
    # 9 stage_bar
    "الثَّامِنُ: شَرِيطُ المَرَاحِلِ. يُبَيِّنُ المَرْحَلَةَ الحَالِيَّةَ، وَيَنْتَقِلُ مُؤَشِّرُهُ مِنْ مَرْحَلَةٍ إِلَى أُخْرَى.",
    # 10 data_table
    "التَّاسِعُ: جَدْوَلُ البَيَانَاتِ. تَظْهَرُ صُفُوفُهُ تِبَاعًا، ثُمَّ نُمَيِّزُ الصَّفَّ الَّذِي يَعْنِينَا.",
    # 11 comparison
    "العَاشِرُ: المُقَارَنَةُ. بِطَاقَتَانِ مُتَجَاوِرَتَانِ، ثُمَّ عَلَامَةٌ عَلَى الخِيَارِ المُعْتَمَدِ.",
    # 12 line_chart
    "الحَادِيَ عَشَرَ: المُخَطَّطُ الخَطِّيُّ. يَرْسُمُ القِيَمَ فَوْقَ نِطَاقِ القَبُولِ، وَيُلَوِّنُ النُّقْطَةَ الخَارِجَةَ عَنْهُ بِالأَحْمَرِ.",
    # 13 bar_chart
    "الثَّانِيَ عَشَرَ: مُخَطَّطُ الأَعْمِدَةِ. أَعْمِدَةٌ بِقِيَمِهَا، وَخَطٌّ لِلْحَدِّ، وَالعَمُودُ الَّذِي يَتَجَاوَزُهُ بِالأَحْمَرِ.",
    # 14 checklist
    "الثَّالِثَ عَشَرَ: قَائِمَةُ التَّحَقُّقِ. نُؤَشِّرُ كُلَّ بَنْدٍ بِالقَبُولِ، أَوْ بِالرَّفْضِ.",
    # 15 summary_box
    "الرَّابِعَ عَشَرَ: صُنْدُوقُ الخُلَاصَةِ. يَجْمَعُ النِّقَاطَ الرَّئِيسِيَّةَ فِي نِهَايَةِ الحَلْقَةِ.",
    # 16 concept_map
    "الخَامِسَ عَشَرَ: خَرِيطَةُ المَفَاهِيمِ، لِلْمَوَاضِيعِ الَّتِي بِلَا أَرْقَامٍ. فِكْرَةٌ فِي الوَسَطِ، تَتَفَرَّعُ مِنْهَا أَفْكَارٌ مُرْتَبِطَةٌ.",
    # 17 timeline
    "السَّادِسَ عَشَرَ: الخَطُّ الزَّمَنِيُّ. أَحْدَاثٌ مُرَتَّبَةٌ عَلَى سَهْمِ الزَّمَنِ، كُلُّ حَدَثٍ فِي مَوْضِعِهِ.",
    # 18 image_panel
    "السَّابِعَ عَشَرَ: لَوْحَةُ الصُّورَةِ. تَعْرِضُ رَسْمًا أَوْ صُورَةً فِي إِطَارٍ، مَعَ تَعْلِيقٍ وَمَصْدَرٍ.",
    # 19 outro
    "هٰذِهِ هِيَ المَكْتَبَةُ كَامِلَةً. نَخْتَارُ مِنْهَا مَشَاهِدَ كُلِّ مَشْرُوعٍ جَدِيدٍ، وَلَا نَرْسُمُ مِنَ الصِّفْرِ إِلَّا مَا لَا تُغَطِّيهِ.",
]

# One line on screen per function (English only on screen).
DESCRIPTIONS = {
    "title_card": "Opening title with series line and subtitle",
    "section_title": "Corner heading that turns into the next one",
    "bullet_list": "Points revealed as they are spoken",
    "equation": "Equation from Text pieces: colour or frame any part",
    "worked_calculation": "Formula, substituted values, boxed result",
    "labeled_diagram": "Any drawing with numbered callouts",
    "process_flow": "Boxes and arrows; light the current step",
    "stage_bar": "Stages with a moving marker",
    "data_table": "Rows appear in turn; mark the one that matters",
    "comparison": "Two cards side by side, with a verdict",
    "line_chart": "Trend against an acceptance band",
    "bar_chart": "Bars, values and a limit line",
    "checklist": "Each item ticked or crossed",
    "summary_box": "Framed key takeaways",
    "concept_map": "A central idea and linked ideas (no numbers needed)",
    "timeline": "Dated events along an arrow (no numbers needed)",
    "image_panel": "Framed picture with caption and credit",
}
assert list(DESCRIPTIONS) == LIBRARY and len(NARRATION) == len(LIBRARY) + 2

AUDIO_DIR = audio_dir_for(__file__)
SKETCH = Path(__file__).resolve().parent / "assets" / "sketch.svg"


class SceneGallery(SyncedScene):
    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)
        n = len(LIBRARY)

        # ---------------- Segment 1: intro ----------------
        title_card(self, "Scene Library", f"{n} building blocks  ·  explainer.scenes",
                   series="explainer-videos  ·  catalogue")
        self.sync(self.end(1) - 0.7)
        self.clear()

        head = None
        for k, name in enumerate(LIBRARY):
            seg = k + 2
            text = VGroup(mono(f"{k + 1:02d} / {n}", FS_TAG, GREY_INK),
                          mono(f"{name}()", FS_BODY - 4, ACCENT_1, weight=BOLD))
            text.arrange(RIGHT, buff=0.3).to_corner(UL, buff=0.4)
            if head is None:
                head = text
                self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.5)
            else:
                self.play(Transform(head, text), run_time=0.5)
            self.say(DESCRIPTIONS[name], GREY_INK)
            getattr(self, f"demo_{name}")(seg)
            self.sync(self.end(seg) - 0.6)
            self.clear(head)

        # ---------------- Segment 19: outro (index of all functions) ----------------
        seg = len(NARRATION)
        self.play(FadeOut(head), run_time=0.4)
        cols = 3
        names = VGroup(*[mono(f"{k + 1:02d}  {m}()", FS_TAG + 2) for k, m in enumerate(LIBRARY)])
        grid = VGroup(*[VGroup(*names[c::cols]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
                        for c in range(cols)]).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        top = label("from explainer import *", FS_BODY, weight=BOLD, font=MONO)
        fit(VGroup(top, grid).arrange(DOWN, buff=0.5)).move_to(UP * 0.3)
        self.play(Write(top), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in names], lag_ratio=0.08),
                  run_time=2.5)
        self.sync(self.cue(seg, "نَخْتَارُ"))
        self.say("Pick scenes here; draw custom Manim only where the library stops",
                 GREY_INK)
        self.sync(self.end(seg) + 1.0)

    # ---------------- one demo per library function ----------------
    def demo_title_card(self, seg):
        title_card(self, "Episode Title", "One-line subtitle", series="Series name  ·  Episode 1",
                   y=0.6)

    def demo_section_title(self, seg):
        box = RoundedRectangle(width=5.2, height=2.4, corner_radius=0.2, stroke_width=3,
                               color=LIGHT_INK)
        hint = label("the heading lives in the top-left corner", FS_TAG, LIGHT_INK)
        hint.move_to(box)
        self.play(Create(box), FadeIn(hint), run_time=0.6)
        sec = label("1  Principle", FS_BODY - 6, ACCENT_2, weight=BOLD).move_to(UP * 1.8)
        self.play(Write(sec), run_time=0.6)
        self.sync(self.cue(seg, "ثُمَّ"))
        new = label("2  Components", FS_BODY - 6, ACCENT_2, weight=BOLD).move_to(UP * 1.8)
        self.play(Transform(sec, new), run_time=0.8)

    def demo_bullet_list(self, seg):
        bullet_list(self, ["First point", "Second point", "Third point"], heading="Key points",
                    cues=[self.cue(seg, "الأُولَى"), self.cue(seg, "الثَّانِيَةُ"),
                          self.cue(seg, "الثَّالِثَةُ")])

    def demo_equation(self, seg):
        eq = equation(self, ["MF", "=", "V", "prover", "÷", "V", "meter"],
                      colors={2: ACCENT_1, 3: ACCENT_1, 5: ACCENT_2, 6: ACCENT_2})
        self.sync(self.cue(seg, "فَنُلَوِّنُ"))
        self.play(Indicate(VGroup(eq[2], eq[3]), color=ACCENT_1), run_time=0.8)
        self.sync(self.cue(seg, "نُحِيطُهُ"))
        emphasize(self, VGroup(eq[5], eq[6]), ACCENT_2)

    def demo_worked_calculation(self, seg):
        worked_calculation(self, ["A", "=", "B", "×", "C"],
                           ["=", f"{D.CALC_B:.2f}", "×", f"{D.CALC_C:.2f}"],
                           f"= {D.CALC_A:.2f}",
                           cues=[self.cue(seg, "المُعَادَلَةُ"), self.cue(seg, "التَّعْوِيضُ"),
                                 self.cue(seg, "النَّتِيجَةُ")])

    def demo_labeled_diagram(self, seg):
        tank = RoundedRectangle(width=1.8, height=2.4, corner_radius=0.15, stroke_width=4,
                                color=INK).move_to([-3.2, 0, 0])
        pipe = Line([-2.3, -0.8, 0], [2.4, -0.8, 0], stroke_width=6, color=INK)
        pump = Circle(radius=0.55, stroke_width=4, color=INK).move_to([0.2, -0.8, 0])
        gauge = Circle(radius=0.35, stroke_width=4, color=INK).move_to([1.6, 0.4, 0])
        stem = Line([1.6, -0.8, 0], [1.6, 0.05, 0], stroke_width=4, color=INK)
        diagram = VGroup(tank, pipe, pump, stem, gauge).move_to(UP * 0.2)
        labeled_diagram(self, diagram,
                        [("Tank", tank, UL), ("Pump", pump, DOWN), ("Gauge", gauge, UR)],
                        cues=[self.cue(seg, "نُضِيفُ")] + [None, None], draw_time=1.6)

    def demo_process_flow(self, seg):
        flow = process_flow(self, ["Input", "Process", "Check", "Output"])
        self.sync(self.cue(seg, "نُضِيءُ"))
        highlight_step(self, flow, 1)
        highlight_step(self, flow, 2)

    def demo_stage_bar(self, seg):
        stages = ["Standby", "Start", "Measure", "End", "Return"]
        bar = stage_bar(self, stages, active=0, y=0.2)
        self.sync(self.cue(seg, "وَيَنْتَقِلُ"))
        for k in range(1, len(stages)):
            set_stage(self, bar, k)
            self.wait(0.25)

    def demo_data_table(self, seg):
        t = data_table(self, ["Run", "Value", "Deviation", "Result"], D.TABLE_ROWS,
                       size=FS_LABEL, pos=UP * 0.3)
        self.sync(self.cue(seg, "نُمَيِّزُ"))
        highlight_row(self, t, D.TABLE_BAD_ROW, ALERT_C)

    def demo_comparison(self, seg):
        comparison(self, ["Option A", "manual reading", "slower"],
                   ["Option B", "automatic logging", "faster"], verdict="right",
                   cues=[None, self.cue(seg, "مُتَجَاوِرَتَانِ"), self.cue(seg, "عَلَامَةٌ")],
                   pos=UP * 0.3)

    def demo_line_chart(self, seg):
        line_chart(self, D.CHART_X, D.CHART_Y, "Reading", "Value", band=D.CHART_BAND,
                   pos=UP * 0.3)

    def demo_bar_chart(self, seg):
        bar_chart(self, D.BAR_LABELS, D.BAR_VALUES, unit=" s", limit=D.BAR_LIMIT,
                  pos=UP * 0.2)

    def demo_checklist(self, seg):
        checklist(self, ["Power on", "Zero checked", "Leak test"], failed={2},
                  cues=[self.cue(seg, "نُؤَشِّرُ"), None, self.cue(seg, "بِالرَّفْضِ")],
                  pos=UP * 0.3)

    def demo_summary_box(self, seg):
        summary_box(self, "Summary", ["What it is", "How it works", "What to check"],
                    pos=UP * 0.3)

    def demo_concept_map(self, seg):
        concept_map(self, "Energy", ["Heat", "Work", "Light", "Sound", "Motion"],
                    links=["is", "does", None, None, None],
                    cues=[self.cue(seg, "تَتَفَرَّعُ")] + [None] * 4, radius=(4.0, 2.1),
                    pos=UP * 0.2)

    def demo_timeline(self, seg):
        timeline(self, [("Step 1", "Idea"), ("Step 2", "Prototype"), ("Step 3", "Test"),
                        ("Step 4", "Release")], cues=[self.cue(seg, "أَحْدَاثٌ")] + [None] * 3,
                 y=0.3)

    def demo_image_panel(self, seg):
        image_panel(self, SKETCH, caption="Tank, pump and gauge", credit="Drawing: own sketch",
                    height=3.4, max_width=8.0, pos=UP * 0.4)


if __name__ == "__main__":
    main(__file__, "SceneGallery", NARRATION)
