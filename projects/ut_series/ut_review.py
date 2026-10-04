"""ut_series: the review segment (intro + 8 question cards), shared by episodes 2-4.

Same card engine as the review of episode 1 (question, a mini drawing, a 3-second silent
countdown ring, the answer with its tick), written once as a function:

    run_review(scene, cards)

`cards` is a list of 8 tuples (question, art, answer): `art(scene)` returns `(show, finish)`;
`show()` plays when the question appears, `finish(*extra)` when the answer appears (it must play
the extra animations together with its own). NARRATION entries: the intro is entry 7, card k
(1..8) uses entries 8 + 3(k-1) (question), 9 + 3(k-1) (silent countdown), 10 + 3(k-1) (answer).
"""
import numpy as np
from explainer import *
from ut_visuals import wavefront, wrap_two_lines

ART_CY = -0.35                                  # centre height of the mini drawings
RING_C = np.array([0.0, -2.95, 0.0])            # countdown ring / answer line


def fly(scene, mob, p0, p1, run_time):
    """A pulse travels from p0 to p1 (and is removed on arrival)."""
    mob.move_to(p0)
    scene.add(mob)
    scene.play(mob.animate(run_time=run_time, rate_func=linear).move_to(p1))
    scene.remove(mob)


def pk(color, direction, amp=0.2):
    """A small pulse (wave-front arcs) for the mini drawings."""
    return wavefront(length=0.6, amp=amp * 1.2, cycles=4, color=color, direction=direction)


def two_bold(text, size, width):
    """One bold label, or two centred lines split at the best space when too wide."""
    one = label(text, size, INK, weight=BOLD)
    if one.width <= width:
        return one
    a, b = wrap_two_lines(text, size, weight=BOLD)
    return VGroup(a, b).arrange(DOWN, buff=0.1)


def head_row(k):
    txt = label(f"Q {k} / 8", FS_LABEL, ACCENT_1, weight=BOLD)
    pill = RoundedRectangle(width=txt.width + 0.5, height=0.55, corner_radius=0.27,
                            color=ACCENT_1, stroke_width=4).set_fill(PANEL_FILL, 1)
    txt.move_to(pill)
    dots = VGroup(*[Circle(radius=0.09, stroke_width=3,
                           color=ACCENT_1 if i < k else GREY_INK)
                    .set_fill(ACCENT_1 if i < k else BG, 1) for i in range(8)])
    dots.arrange(RIGHT, buff=0.18)
    return VGroup(VGroup(pill, txt), dots).arrange(RIGHT, buff=0.5).move_to([0, 3.3, 0])


def question_text(text):
    for size in (36, 32, 28):           # one line, else two lines, else a smaller size
        one = label(text, size, INK)
        if one.width <= 11.8:
            g = one
            break
        a, b = wrap_two_lines(text, size)
        g = VGroup(a, b).arrange(DOWN, buff=0.1)
        if g.width <= 12.4:
            break
    return g.move_to([0, 2.75 - g.height / 2, 0])


def answer_block(text):
    t = two_bold(text, 38, 9.8)
    if t.width > 9.8 or isinstance(t, VGroup):
        t = two_bold(text, 30, 9.8)
    tick = icon("check", OK_C, 0.62)
    return VGroup(tick, t).arrange(RIGHT, buff=0.3).move_to(RING_C)


def card(scene, k, question, art, answer):
    sq, sc, sa = 8 + 3 * (k - 1), 9 + 3 * (k - 1), 10 + 3 * (k - 1)
    head, q = head_row(k), question_text(question)
    scene.sync(scene.start(sq))
    scene.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(q, shift=DOWN * 0.2), run_time=0.5)
    show, finish = art(scene)
    show()
    # ---- the silent countdown: the ring empties, the digits 3, 2, 1 each on its second
    scene.sync(scene.start(sc))
    trk = ValueTracker(0.0)
    track = Circle(radius=0.55, color=LIGHT_INK, stroke_width=8).move_to(RING_C)
    track.set_fill(PANEL_FILL, 1)
    arc = always_redraw(lambda: Arc(radius=0.55, start_angle=PI / 2,
                                    angle=max(TAU * (1 - trk.get_value()), 1e-3),
                                    arc_center=RING_C, color=INK, stroke_width=8))
    digit = lambda n: label(str(n), FS_HEADING, INK, weight=BOLD).move_to(RING_C)
    d = digit(3)
    scene.add(track, arc)
    scene.play(FadeIn(track, run_time=0.2), FadeIn(d, scale=1.5, run_time=0.25),
               trk.animate(run_time=1.0, rate_func=linear).set_value(1 / 3))
    for n, goal, t0 in ((2, 2 / 3, 1.0), (1, 1.0, 2.0)):
        scene.sync(scene.start(sc) + t0)
        nd = digit(n)
        scene.play(FadeOut(d, run_time=0.15), FadeIn(nd, scale=1.5, run_time=0.25),
                   trk.animate(run_time=scene.end(sc) - scene.start(sc) - t0
                               if n == 1 else 1.0, rate_func=linear).set_value(goal))
        d = nd
    # ---- the answer: ring out, answer line with its tick in, the drawing completed
    scene.sync(scene.start(sa))
    arc.clear_updaters()
    ans = answer_block(answer)
    finish(FadeOut(track, run_time=0.3), FadeOut(arc, run_time=0.3),
           FadeOut(d, run_time=0.3), FadeIn(ans, shift=UP * 0.15, run_time=0.4))
    scene.sync(scene.end(sa) - 0.45)
    scene.clear(run_time=0.45)


def intro(scene, cue_badges, cue_three):
    """The review title, the eight badges (at `cue_badges`) and the 3-second note (at `cue_three`)."""
    scene.sync(scene.start(7))
    r_head = label("Review", FS_TITLE, INK, weight=BOLD).move_to([0, 2.3, 0])
    r_rule = Line(LEFT * 1.8, RIGHT * 1.8, color=ACCENT_1, stroke_width=5)
    r_rule.next_to(r_head, DOWN, 0.2)
    scene.play(FadeIn(r_head, shift=DOWN * 0.2), Create(r_rule), run_time=0.6)
    r_badges = VGroup(*[badge(n, ACCENT_1, 0.34) for n in range(1, 9)]).arrange(RIGHT, buff=0.45)
    r_badges.move_to([0, 0.5, 0])
    scene.sync(cue_badges)
    scene.play(LaggedStart(*[FadeIn(b, scale=0.6) for b in r_badges], lag_ratio=0.25,
                           run_time=1.6))
    r_ring = Circle(radius=0.55, color=LIGHT_INK, stroke_width=8).set_fill(PANEL_FILL, 1)
    r_three = label("3", FS_HEADING, INK, weight=BOLD).move_to(r_ring)
    r_note = label("seconds to answer yourself", FS_LABEL, INK)
    r_row = VGroup(VGroup(r_ring, r_three), r_note).arrange(RIGHT, buff=0.4)
    r_row.move_to([0, -1.5, 0])
    r_trk = ValueTracker(0.0)
    r_arc = always_redraw(lambda: Arc(radius=0.55, start_angle=PI / 2,
                                      angle=max(TAU * (1 - r_trk.get_value()), 1e-3),
                                      arc_center=r_ring.get_center(), color=INK, stroke_width=8))
    scene.sync(cue_three)
    scene.add(r_arc)
    scene.play(FadeIn(r_ring, run_time=0.3), FadeIn(r_three, run_time=0.3),
               FadeIn(r_note, shift=LEFT * 0.2, run_time=0.4))
    scene.play(r_trk.animate(run_time=scene.end(7) - 0.45 - scene.renderer.time,
                             rate_func=linear).set_value(1.0))
    r_arc.clear_updaters()
    scene.clear(run_time=0.45)


def run_review(scene, cards, cue_badges, cue_three, n_entries):
    """The whole review: intro, then the cards; ends on the last narration entry."""
    intro(scene, cue_badges, cue_three)
    for k, (question, art, answer) in enumerate(cards, 1):
        card(scene, k, question, art, answer)
    scene.sync(scene.end(n_entries))
