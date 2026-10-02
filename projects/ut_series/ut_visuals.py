"""ut_series: shared drawing primitives for the ultrasonic-testing episodes.

    from ut_visuals import wavefront

`wavefront` is the one way every episode draws an ultrasonic pulse travelling through a part:
a few arcs, like the Wi-Fi icon. They are the wave fronts of the pulse: convex in the direction
of travel, growing wider toward the front, the front arc strongest and the ones behind it
fainter. The first version of this shape is `wavefront()` of projects/ut_intro/ut_intro.py
(three same-size arcs); here the arcs are concentric so the front is the widest, the colours are
theme colours (never literals), and the group keeps its fade pattern when a scene fades it with
`set_stroke(opacity=...)`.

Colour roles of the series (project CLAUDE.md): ACCENT_1 the pulse going in, ACCENT_2 the echo
coming back, ACCENT_3 the transmitted pulse.
"""
from manim import *

from explainer import ACCENT_1


class Wavefront(VGroup):
    """Arcs of one pulse; `fades` is the opacity of each arc from the back to the front.
    set_stroke(opacity=x) / set_opacity(x) scale those fades by x (a plain VGroup would flatten
    them to x), so a scene can fade a travelling pulse in and out without losing its shape."""

    fades = (0.28, 0.55, 1.0)

    def set_stroke(self, color=None, width=None, opacity=None, background=None, family=True):
        # the group's own colour data first (VMobject.__init__ and Transform need it), then the arcs
        super().set_stroke(color=color, width=width, opacity=opacity, background=background,
                           family=False)
        for arc, f in zip(self.submobjects, self.fades):
            arc.set_stroke(color=color, width=width,
                           opacity=None if opacity is None else opacity * f,
                           background=background, family=family)
        return self

    def set_opacity(self, opacity, family=True):
        return self.set_stroke(opacity=opacity, family=family)


def wavefront(length=0.9, amp=0.28, cycles=None, color=ACCENT_1, direction=DOWN,
              stroke_width=4, n=3, spread=0.85):
    """A pulse as `n` wave-front arcs, centred on ORIGIN and moving along `direction`
    (DOWN from a probe, UP for the echo, RIGHT / LEFT sideways).

    amp     half the width of the front arc is 1.8 x amp (the sideways size of the beam)
    length  how far back the pulse reaches: the arcs are spaced at about 0.55 x length / (n - 1)
    spread  half the angle of every arc, in radians; the arcs share one centre, so the front
            one (the largest) is the widest and the ones behind it are narrower
    cycles  accepted and ignored (the signature matches the sine packet this replaces)

    Shrinking it sideways (`.stretch(k, 0)` for a vertical pulse) or lowering its opacity with
    `.set_stroke(opacity=...)` weakens it, as for attenuation.
    """
    r_front = 1.8 * amp / np.sin(spread)
    gap = min(0.55 * length / (n - 1), 0.35 * r_front)
    arcs = []
    for k in range(n):                                   # k = 0 is the rear arc
        radius = r_front - (n - 1 - k) * gap
        arcs.append(Arc(radius=radius, start_angle=-PI / 2 - spread, angle=2 * spread,
                        stroke_width=stroke_width, color=color))
    g = Wavefront(*arcs)
    g.fades = Wavefront.fades if n == 3 else tuple(np.linspace(0.28, 1.0, n))
    g.set_stroke(opacity=1)
    g.move_to(ORIGIN)
    return g.rotate(angle_of_vector(direction) - angle_of_vector(DOWN), about_point=ORIGIN)
