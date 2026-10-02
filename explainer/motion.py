"""Motion tools: five ready-made moves for any scene (documented in the root CLAUDE.md,
Scene library). Like the scene library they take the running scene first, play their
animation and return what they made; `cues` / times come from scene.cue(seg, phrase).

    zoom_on(scene, target, factor=2.0, hold=1.5)    magnify the screen on one element, hold, return
    stagger_in(scene, items, shift=UP * 0.3)        items enter one after another (or at cues)
    move_along_path(scene, mob, path, run_time=2)   an element travels along a path
    pulse(scene, mob, times=2)                      a highlight pulse on the element being explained
    parallax(scene, [(layer, depth), ...], shift)   layers slide by depth: near ones travel farther

zoom_on works on the content, not on a camera: every mobject on screen (the background stays put and the
bottom caption fades out while it is magnified) is scaled about the target with its strokes and shifted so the target
lands at the centre; the same steps then run backwards. The result is that of
a camera move without changing the scene class, so every script can use it. While it is
magnified, scene.zoomed is True and the QA overlap check skips its frame and safe-margin rules
(content outside the view is the point), still reporting overlaps and contrast.
"""
import numpy as np
from manim import (LEFT, UP, AnimationGroup, Create, FadeIn, FadeOut, Indicate, LaggedStart,
                   MoveAlongPath, SurroundingRectangle, UpdateFromAlphaFunc, VMobject,
                   linear, smooth)

from .style import ACCENT_1, GREY_INK

__all__ = ["zoom_on", "stagger_in", "move_along_path", "pulse", "parallax"]


def _content(scene, keep=()):
    """What a zoom moves: everything on screen but the background, the caption and `keep`."""
    skip = {id(m) for m in keep}
    caption = getattr(scene, "caption", None)
    if caption is not None:
        skip.add(id(caption))
    return [m for m in scene.mobjects
            if id(m) not in skip and not getattr(m, "is_background", False)]


def _zoom_step(m, factor, center, forward):
    """An animation of m that magnifies (forward) or restores it, in small exact steps: at
    each frame it scales by the change since the previous frame about `center` (strokes
    included) and shifts the centre towards the middle of the screen. Plain steps, not a
    Transform, so any mobject (groups, images, symbols) takes part, and the way back
    undoes the way in."""
    state = {"alpha": 0.0}

    def step(mob, alpha):
        a = alpha if forward else 1 - alpha         # progress of the magnification, 0..1
        ratio = (1 + (factor - 1) * a) / (1 + (factor - 1) * state["alpha"])
        for f in mob.get_family():
            if isinstance(f, VMobject):
                f.set_stroke(width=f.get_stroke_width() * ratio)
        # the target has moved by -center * alpha so far: that is where it is scaled about
        mob.scale(ratio, about_point=center * (1 - state["alpha"]))
        mob.shift(-center * (a - state["alpha"]))
        state["alpha"] = a
    if not forward:
        state["alpha"] = 1.0
    return UpdateFromAlphaFunc(m, step)


def zoom_on(scene, target, factor=2.0, hold=1.5, run_time=0.9, during=None, keep=()):
    """Zoom the screen on `target` (a mobject or a point), hold, and come back.

    during(scene) runs while magnified instead of a plain wait of `hold` seconds, e.g. a
    pulse or an annotation. Returns the list of mobjects that were moved."""
    center = np.array(target.get_center() if hasattr(target, "get_center") else target,
                      dtype=float)
    content = _content(scene, keep)
    caption = getattr(scene, "caption", None)
    caption = caption if caption is not None and len(caption.get_family()) > 1 else None
    scene.zoomed = True
    # the bottom caption steps aside while the content is magnified under it
    scene.play(*[_zoom_step(m, factor, center, True) for m in content],
               *([FadeOut(caption)] if caption is not None else []),
               run_time=run_time, rate_func=smooth)
    if during is not None:
        during(scene)
    elif hold:
        scene.wait(hold)
    scene.play(*[_zoom_step(m, factor, center, False) for m in content],
               *([FadeIn(caption)] if caption is not None else []),
               run_time=run_time, rate_func=smooth)
    scene.zoomed = False
    return content


def stagger_in(scene, items, shift=UP * 0.3, lag=0.18, run_time=0.6, cues=None, scale=None):
    """Items enter one after another: each fades in while sliding by `shift` (and growing from
    `scale` if given), starting `lag` seconds after the one before. With `cues` (a time per
    item) each enters at its time instead."""
    items = list(items)
    anims = [FadeIn(m, shift=shift, scale=scale if scale is not None else 1) for m in items]
    if cues is not None:
        for k, a in enumerate(anims):
            if k < len(cues) and cues[k] is not None:
                scene.sync(cues[k])
            scene.play(a, run_time=run_time)
        return items
    total = run_time + lag * max(len(items) - 1, 0)
    scene.play(LaggedStart(*anims, lag_ratio=lag / run_time, run_time=total))
    return items


def move_along_path(scene, mob, path, run_time=2.0, rotate=False, trail=False, color=GREY_INK,
                    rate_func=smooth):
    """Move `mob` along `path` (a VMobject, or a list of points joined smoothly); its centre
    follows the path from its start to its end. rotate=True turns it to follow the tangent;
    trail=True draws the path behind it (returned, so the caller can fade it)."""
    if not isinstance(path, VMobject):
        pts = [np.array(p, dtype=float) for p in path]
        path = VMobject().set_points_smoothly(pts)
    mob.move_to(path.get_start())
    anims = []
    if rotate:
        state = {"angle": 0.0}

        def follow(m, alpha):
            a = float(rate_func(alpha))
            p = path.point_from_proportion(a)
            ahead = path.point_from_proportion(min(a + 0.01, 1.0))
            behind = path.point_from_proportion(max(a - 0.01, 0.0))
            angle = np.arctan2(*(ahead - behind)[[1, 0]])
            m.rotate(angle - state["angle"])
            state["angle"] = angle
            m.move_to(p)
        anims.append(UpdateFromAlphaFunc(mob, follow, rate_func=linear))
    else:
        anims.append(MoveAlongPath(mob, path, rate_func=rate_func))
    trace = None
    if trail:
        trace = path.copy().set_fill(opacity=0).set_stroke(color, width=3, opacity=0.6)
        anims.append(Create(trace, rate_func=rate_func))
    scene.play(AnimationGroup(*anims), run_time=run_time)
    return trace if trail else path


def pulse(scene, mob, color=ACCENT_1, times=2, scale=1.12, run_time=0.9, ring=True):
    """A highlight pulse on the element being explained: it swells and takes `color`, and a
    ring spreads from it and fades, `times` times. Nothing is left on screen."""
    for _ in range(times):
        anims = [Indicate(mob, scale_factor=scale, color=color)]
        spread = None
        if ring:
            spread = SurroundingRectangle(mob, color=color, buff=0.1, corner_radius=0.12,
                                          stroke_width=4)
            scene.add(spread)
            anims.append(spread.animate.scale(1.4).set_stroke(opacity=0))
        scene.play(*anims, run_time=run_time)
        if spread is not None:
            scene.remove(spread)
    return mob


def parallax(scene, layers, shift=LEFT * 1.5, run_time=3.0, rate_func=smooth):
    """Layers of different depth slide together by `shift`, scaled by each layer's depth:
    layers = [(mobject, depth), ...] with depth 0 for the far backdrop (stands still) up to 1
    (and beyond) for the nearest layer, which travels farthest. The sense of depth comes from
    the different speeds."""
    scene.play(*[m.animate.shift(np.array(shift, dtype=float) * depth)
                 for m, depth in layers], run_time=run_time, rate_func=rate_func)
    return [m for m, _ in layers]
