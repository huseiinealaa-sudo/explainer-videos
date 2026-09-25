"""Ultrasonic Testing (UT) intro — reference template for explainer videos.

Build (from the repo root):
    python scripts/ut_intro.py --preview   # 480p15 layout check -> tmp/ut_intro/preview.mp4
    python scripts/ut_intro.py             # final 1080p30        -> output/ut_intro.mp4
"""
import argparse

import numpy as np

from style import *

# Approved, fully diacritized narration — one entry per scene.
NARRATION = [
    "الفَحْصُ بِالمَوْجَاتِ فَوْقَ الصَّوْتِيَّةِ هُوَ أَحَدُ أَهَمِّ طُرُقِ الفَحْصِ غَيْرِ الإِتْلَافِيِّ؛ إِذْ نَكْشِفُ بِهِ العُيُوبَ الدَّاخِلِيَّةَ فِي المَوَادِّ، دُونَ أَنْ نُلْحِقَ بِهَا أَيَّ ضَرَرٍ.",
    "لِنَنْظُرْ إِلَى مَقْطَعٍ فِي قِطْعَةٍ مَعْدِنِيَّةٍ، يُوجَدُ فِي دَاخِلِهَا عَيْبٌ صَغِيرٌ. نَضَعُ عَلَى سَطْحِهَا مِجَسًّا يُرْسِلُ المَوْجَاتِ وَيَسْتَقْبِلُهَا، مَعَ طَبَقَةٍ رَقِيقَةٍ مِنْ مَادَّةِ الاقْتِرَانِ، لِأَنَّ الهَوَاءَ يَمْنَعُ مُرُورَ المَوْجَاتِ.",
    "يُطْلِقُ المِجَسُّ نَبْضَةً صَوْتِيَّةً عَالِيَةَ التَّرَدُّدِ، تَنْتَقِلُ دَاخِلَ المَعْدِنِ. وَحِينَ تَصْطَدِمُ بِالعَيْبِ يَرْتَدُّ جُزْءٌ مِنْهَا، وَيُكْمِلُ البَاقِي طَرِيقَهُ حَتَّى يَرْتَدَّ عَنِ الجِدَارِ الخَلْفِيِّ.",
    "تَظْهَرُ هَذِهِ الأَصْدَاءُ عَلَى شَاشَةِ «إِيه-سْكَان» فِي صُورَةِ قِمَمٍ: قِمَّةُ الإِرْسَالِ أَوَّلًا، ثُمَّ قِمَّةُ العَيْبِ، ثُمَّ قِمَّةُ الجِدَارِ الخَلْفِيِّ. وَبِمَعْرِفَةِ سُرْعَةِ الصَّوْتِ فِي المَعْدِنِ وَزَمَنِ وُصُولِ الصَّدَى، نَحْسُبُ عُمْقَ العَيْبِ بِدِقَّةٍ.",
    "إِذَنْ: يَكْشِفُ الفَحْصُ بِالمَوْجَاتِ فَوْقَ الصَّوْتِيَّةِ العُيُوبَ الدَّاخِلِيَّةَ، وَيُحَدِّدُ أَعْمَاقَهَا بِقِيَاسِ زَمَنِ ارْتِدَادِ الصَّدَى، دُونَ أَنْ يُتْلِفَ القِطْعَةَ.",
]

AUDIO_DIR = BUILD_DIR / "ut_intro" / "audio"

# Geometry of the metal cross-section
TOP, BOT = 1.2, -2.6
LEFT_X, RIGHT_X = -6.3, -0.7
PX = -3.5                       # probe x
DEF_Y = -0.5                    # defect centre
DEF_TOP = DEF_Y + 0.15
DEPTH_FRAC = (TOP - DEF_Y) / (TOP - BOT)


def wavefront(width=1.2, up=False, n=3, opacity=1.0):
    g = VGroup()
    for k in range(n):
        a = Arc(radius=width, start_angle=-PI / 2 - 0.5, angle=1.0,
                stroke_width=5, color=INK)
        a.shift(UP * (width - k * 0.14))
        g.add(a)
    g.move_to(ORIGIN)
    if up:
        g.rotate(PI)
    g.set_stroke(opacity=opacity)
    return g


class UTIntro(SyncedScene):
    def construct(self):
        START = segment_starts(AUDIO_DIR, len(NARRATION))

        # ---------------- Segment 1: definition ----------------
        title = Text("Ultrasonic Testing (UT)", font_size=FS_TITLE, weight=BOLD)
        title.to_edge(UP, buff=1.0)
        line = Line(LEFT, RIGHT).set_width(title.width).next_to(title, DOWN, 0.2)
        sub = Text("A Non-Destructive Testing (NDT) method", font_size=FS_SUBTITLE)
        sub.next_to(line, DOWN, 0.5)
        b1 = Text("•  Finds hidden internal defects", font_size=FS_BODY)
        b2 = Text("•  Uses high-frequency sound waves", font_size=FS_BODY)
        b3 = Text("•  No damage to the part", font_size=FS_BODY)
        bullets = VGroup(b1, b2, b3).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        bullets.next_to(sub, DOWN, 0.8)

        self.play(Write(title), run_time=2)
        self.play(Create(line), FadeIn(sub, shift=UP * 0.2), run_time=1.5)
        self.play(Write(b1), run_time=1.6)
        self.play(Write(b2), run_time=1.6)
        self.sync(START[0] + 7.5)
        self.play(Write(b3), run_time=1.5)
        self.sync(START[1] - 0.8)
        small_title = Text("Ultrasonic Testing (UT)", font_size=FS_BODY, weight=BOLD)
        small_title.to_corner(UL, buff=0.4)
        self.play(FadeOut(VGroup(line, sub, bullets)),
                  Transform(title, small_title), run_time=0.8)

        # ---------------- Segment 2: cross-section + probe + couplant ----------------
        t0 = START[1]
        block = Polygon([LEFT_X, TOP, 0], [RIGHT_X, TOP, 0],
                        [RIGHT_X, BOT, 0], [LEFT_X, BOT, 0], stroke_width=5, color=INK)
        steel = Text("Steel", font_size=FS_NOTE, color=GREY_INK)
        steel.move_to([LEFT_X + 0.55, BOT + 0.35, 0])
        self.play(Create(block), run_time=2.2)
        self.play(FadeIn(steel), run_time=1.0)

        defect = Ellipse(width=0.8, height=0.3, fill_color=INK,
                         fill_opacity=0.85, stroke_width=4, color=INK).move_to([PX + 0.15, DEF_Y, 0])
        def_lbl = Text("Defect", font_size=FS_LABEL).move_to([RIGHT_X - 1.0, DEF_Y + 0.9, 0])
        def_arr = Arrow(def_lbl.get_bottom(), defect.get_right() + RIGHT * 0.05,
                        buff=0.1, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        bw_lbl = Text("Back Wall", font_size=FS_LABEL).next_to([RIGHT_X - 1.0, BOT, 0], DOWN, 0.2)
        self.sync(t0 + 3.2)
        self.play(GrowFromCenter(defect), run_time=1.0)
        self.play(Write(def_lbl), GrowArrow(def_arr), run_time=1.0)
        self.play(Write(bw_lbl), Indicate(Line([LEFT_X, BOT, 0], [RIGHT_X, BOT, 0],
                                               stroke_width=8)), run_time=1.0)

        # couplant layer + probe
        coup = Rectangle(width=1.3, height=0.1, fill_color=GREY_INK, fill_opacity=0.5,
                         stroke_width=2, color=GREY_INK).move_to([PX, TOP + 0.05, 0])
        probe = Rectangle(width=1.0, height=0.7, stroke_width=5, color=INK,
                          fill_color=BG, fill_opacity=1).next_to(coup, UP, 0)
        crystal = Line(probe.get_corner(DL) + UP * 0.12 + RIGHT * 0.1,
                       probe.get_corner(DR) + UP * 0.12 + LEFT * 0.1, stroke_width=6)
        cable = CubicBezier(probe.get_top(), probe.get_top() + UP * 0.6,
                            probe.get_top() + UP * 0.1 + RIGHT * 0.9,
                            probe.get_top() + UP * 0.55 + RIGHT * 1.3, stroke_width=4,
                            color=INK)
        probe_grp = VGroup(probe, crystal, cable)
        probe_lbl = Text("Probe", font_size=FS_LABEL).next_to(probe, LEFT, 0.9)
        probe_arr = Arrow(probe_lbl.get_right(), probe.get_left(), buff=0.1,
                          stroke_width=3, max_tip_length_to_length_ratio=0.25)
        self.sync(t0 + 6.0)
        self.play(Create(probe_grp), run_time=1.8)
        self.play(Write(probe_lbl), GrowArrow(probe_arr), run_time=0.9)

        coup_lbl = Text("Couplant", font_size=FS_LABEL).move_to([PX + 2.3, TOP + 0.75, 0])
        coup_arr = Arrow(coup_lbl.get_left(), coup.get_right(), buff=0.08,
                         stroke_width=3, max_tip_length_to_length_ratio=0.25)
        self.sync(t0 + 9.8)
        self.play(FadeIn(coup), run_time=0.8)
        self.play(Write(coup_lbl), GrowArrow(coup_arr), run_time=1.0)

        air = Text("Air gap blocks ultrasound", font_size=FS_AXIS, color=GREY_INK)
        air.next_to(coup_lbl, RIGHT, 0.4)
        self.sync(t0 + 13.8)
        self.play(FadeIn(air, shift=DOWN * 0.1), run_time=0.8)
        self.sync(START[2] - 0.5)
        self.play(FadeOut(air), run_time=0.5)

        # ---------------- Segment 3: pulse travels & echoes ----------------
        t0 = START[2]
        v = 0.6
        y0 = TOP - 0.1
        t_def = (y0 - DEF_TOP) / v
        t_bw = (y0 - (BOT + 0.1)) / v
        tau = ValueTracker(0)

        main = wavefront(1.2)
        echo1 = wavefront(0.7, up=True)
        echo2 = wavefront(1.2, up=True)

        def upd_main(m):
            t = tau.get_value()
            vis = 0 <= t <= t_bw
            y = y0 - v * min(t, t_bw)
            m.move_to([PX, y, 0])
            m.set_stroke(opacity=(1.0 if t < t_def else 0.6) if vis else 0)

        def upd_e1(m):
            t = tau.get_value()
            vis = t_def <= t <= 2 * t_def
            m.move_to([PX + 0.15, DEF_TOP + v * max(t - t_def, 0), 0])
            m.set_stroke(opacity=0.8 if vis else 0)

        def upd_e2(m):
            t = tau.get_value()
            vis = t_bw <= t <= 2 * t_bw
            m.move_to([PX, BOT + 0.1 + v * max(t - t_bw, 0), 0])
            m.set_stroke(opacity=0.8 if vis else 0)

        main.add_updater(upd_main)
        echo1.add_updater(upd_e1)
        echo2.add_updater(upd_e2)
        upd_main(main); upd_e1(echo1); upd_e2(echo2)
        self.add(main, echo1, echo2)

        send_lbl = Text("Sound pulse", font_size=FS_TAG).move_to([LEFT_X + 1.25, 0.3, 0])
        self.play(Indicate(probe_grp, scale_factor=1.08, color=INK),
                  FadeIn(send_lbl), run_time=1.2)
        self.play(tau.animate.set_value(2 * t_bw), run_time=2 * t_bw, rate_func=linear)

        # leave the ray paths as a trace
        path_down = Arrow([PX - 0.35, y0, 0], [PX - 0.35, BOT + 0.05, 0], buff=0,
                          stroke_width=3, color=GREY_INK, max_tip_length_to_length_ratio=0.06)
        path_e1 = Arrow([PX + 0.25, DEF_TOP + 0.05, 0], [PX + 0.25, y0, 0], buff=0,
                        stroke_width=3, color=GREY_INK, max_tip_length_to_length_ratio=0.15)
        path_e2 = Arrow([PX + 0.6, BOT + 0.05, 0], [PX + 0.6, y0, 0], buff=0,
                        stroke_width=3, color=GREY_INK, max_tip_length_to_length_ratio=0.06)
        for m in (main, echo1, echo2):
            m.clear_updaters()
        self.remove(main, echo1, echo2)
        self.play(GrowArrow(path_down), GrowArrow(path_e1), GrowArrow(path_e2),
                  FadeOut(send_lbl), run_time=min(1.0, START[3] - self.renderer.time))
        self.sync(START[3])

        # ---------------- Segment 4: A-Scan ----------------
        t0 = START[3]
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 5, 1], x_length=5.0, y_length=3.0,
                  tips=True, axis_config={"color": INK, "include_ticks": False,
                                          "stroke_width": 4})
        ax.move_to([3.7, -0.1, 0])
        scan_title = Text("A-Scan", font_size=FS_BODY, weight=BOLD).next_to(ax, UP, 0.45)
        x_lbl = Text("Time", font_size=FS_AXIS).next_to(ax.x_axis.get_end(), DOWN, 0.15)
        x_lbl.shift(LEFT * 0.3)
        y_lbl = Text("Amplitude", font_size=FS_AXIS).rotate(PI / 2).next_to(ax.y_axis, LEFT, 0.15)

        x_ip = 0.6
        x_bw = 8.6
        x_df = x_ip + (x_bw - x_ip) * DEPTH_FRAC
        peaks = [(x_ip, 4.5), (x_df, 2.2), (x_bw, 3.4)]

        def trace(x):
            y = 0.06 * abs(np.sin(37 * x)) * abs(np.cos(11 * x))
            for xp, a in peaks:
                y += a * np.exp(-((x - xp) / 0.13) ** 2) * abs(np.cos(22 * (x - xp)))
            return y

        cuts = [0, 2.5, 6.3, 9.8]
        parts = [ax.plot(trace, x_range=[cuts[i], cuts[i + 1], 0.005],
                         stroke_width=3.5, color=INK) for i in range(3)]
        names = ["Initial Pulse", "Defect Echo", "Back-Wall Echo"]
        tags = VGroup()
        for (xp, a), n in zip(peaks, names):
            tg = Text(n, font_size=FS_TAG).next_to(ax.c2p(xp, a), UP, 0.12)
            tags.add(tg)
        tags[0].shift(RIGHT * 0.75)

        # time-of-flight and depth
        ty = ax.c2p(0, -0.45)[1]
        t_arrow = DoubleArrow([ax.c2p(x_ip, 0)[0], ty, 0], [ax.c2p(x_df, 0)[0], ty, 0],
                              buff=0, stroke_width=3, tip_length=0.18)
        t_txt = Text("t", font_size=FS_SYMBOL, slant=ITALIC).next_to(t_arrow, RIGHT, 0.15)
        screen = SurroundingRectangle(VGroup(ax, scan_title, x_lbl, y_lbl, t_arrow, t_txt),
                                      buff=0.3, corner_radius=0.15, stroke_width=4,
                                      color=INK)
        self.play(Create(screen), run_time=1.2)
        self.play(Create(ax), Write(scan_title), FadeIn(x_lbl), FadeIn(y_lbl), run_time=1.5)
        self.sync(t0 + 3.6)
        self.play(Create(parts[0]), Write(tags[0]), run_time=1.6)
        self.sync(t0 + 5.3)
        self.play(Create(parts[1]), Write(tags[1]), Indicate(defect, color=INK),
                  run_time=1.6)
        self.sync(t0 + 7.0)
        self.play(Create(parts[2]), Write(tags[2]), run_time=1.8)

        d_arrow = DoubleArrow([LEFT_X + 0.5, TOP, 0], [LEFT_X + 0.5, DEF_Y, 0],
                              buff=0, stroke_width=3, tip_length=0.18)
        d_txt = Text("d", font_size=FS_SYMBOL, slant=ITALIC).next_to(d_arrow, RIGHT, 0.1)
        dash = DashedLine([LEFT_X + 0.3, DEF_Y, 0], [PX - 0.25, DEF_Y, 0],
                          stroke_width=2, color=GREY_INK)
        eq = Text("d = v · t / 2", font_size=FS_EQUATION, weight=BOLD)
        eq.move_to([3.7, -3.0, 0])
        eq_note = Text("v = speed of sound in the metal", font_size=FS_TAG, color=GREY_INK)
        eq_note.next_to(eq, DOWN, 0.12)
        self.sync(t0 + 10.3)
        self.play(GrowFromCenter(t_arrow), Write(t_txt), run_time=1.0)
        self.play(Create(dash), GrowFromCenter(d_arrow), Write(d_txt), run_time=1.2)
        self.play(Write(eq), run_time=1.5)
        self.play(FadeIn(eq_note), run_time=0.8)
        self.play(Circumscribe(eq, color=INK), run_time=1.2)
        self.sync(START[4] - 0.8)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not title], run_time=0.8)

        # ---------------- Segment 5: summary ----------------
        t0 = START[4]
        head = Text("In short", font_size=FS_HEADING, weight=BOLD)
        l1 = Text("Send a sound pulse into the part", font_size=FS_SUMMARY)
        l2 = Text("Listen for echoes from defects & back wall", font_size=FS_SUMMARY)
        l3 = Text("Echo time  →  defect depth:   d = v · t / 2", font_size=FS_SUMMARY)
        l4 = Text("No damage to the part", font_size=FS_SUMMARY)
        steps = VGroup(l1, l2, l3, l4).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        nums = VGroup(*[Text(f"{i}.", font_size=FS_SUMMARY, weight=BOLD).next_to(l, LEFT, 0.25)
                        for i, l in enumerate(steps, 1)])
        body = VGroup(nums, steps)
        grp = VGroup(head, body).arrange(DOWN, buff=0.6).move_to(DOWN * 0.2)
        box = SurroundingRectangle(grp, buff=0.45, corner_radius=0.2, stroke_width=4,
                                   color=INK)
        self.play(Write(head), Create(box), run_time=1.2)
        for n, l in zip(nums, steps):
            self.play(Write(n), Write(l), run_time=1.3)
        self.sync(START[5] + 0.6)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="low-quality layout check")
    args = parser.parse_args()
    print(build(__file__, "UTIntro", NARRATION, preview=args.preview))
