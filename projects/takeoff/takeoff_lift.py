"""takeoff: How does an airplane take off? Lift and takeoff speeds (single video).

Segments 1 and 5 are 3D (ThreeDScene camera: a simple airliner built from basic shapes on a
runway); segments 2-4, 6 and 7 are 2D, seen by the same camera in its default top-down
orientation. Storyboard: projects/takeoff/storyboard/takeoff_lift.md.

Build (from the repo root):
    python projects/takeoff/takeoff_lift.py --preview   # 480p15 -> tmp/takeoff_lift/preview.mp4
    python projects/takeoff/takeoff_lift.py             # 1080p30 -> output/takeoff_lift.mp4
"""
from explainer import *
import takeoff_data as D

# Fully diacritized narration (owner-approved 2026-09-30, cuts (a) and (b) applied) — one entry per segment.
NARRATION = [
    # 1 the question (3D)
    "هٰذِهِ مَادَّةٌ تَعْلِيمِيَّةٌ؛ وَالمَرْجِعُ المُلْزِمُ هُوَ الوَثَائِقُ الرَّسْمِيَّةُ وَالإِجْرَاءَاتُ المُعْتَمَدَةُ. "
    "طَائِرَةُ رُكَّابٍ كُتْلَتُهَا سَبْعُونَ طُنًّا تَقِفُ عَلَى المَدْرَجِ. "
    "فَكَيْفَ يَرْفَعُ الهَوَاءُ، وَهُوَ شَيْءٌ لَا نَرَاهُ، هٰذِهِ الكُتْلَةَ كُلَّهَا؟ "
    "الجَوَابُ فِي شَيْئَيْنِ: الجَنَاحِ، وَالسُّرْعَةِ.",
    # 2 the four forces
    "عَلَى الطَّائِرَةِ أَرْبَعُ قُوًى. الرَّفْعُ إِلَى الأَعْلَى، وَيُوَلِّدُهُ الجَنَاحُ. "
    "وَالوَزْنُ إِلَى الأَسْفَلِ: الكُتْلَةُ فِي تَسَارُعِ الجَاذِبِيَّةِ، سَبْعُونَ أَلْفَ كِيلُوغْرَامٍ فِي تِسْعَةٍ فَاصِلَةُ وَاحِدٍ وَثَمَانِينَ، "
    "أَيْ سِتُّمِئَةٍ وَسِتَّةٌ وَثَمَانُونَ أَلْفًا وَسَبْعُمِئَةِ نْيُوتِن. "
    "وَالدَّفْعُ إِلَى الأَمَامِ مِنَ المُحَرِّكَاتِ، وَالسَّحْبُ إِلَى الخَلْفِ، وَهُوَ مُقَاوَمَةُ الهَوَاءِ. "
    "فِي الإِقْلَاعِ يَكُونُ الدَّفْعُ أَكْبَرَ مِنَ السَّحْبِ، فَتَتَسَارَعُ الطَّائِرَةُ عَلَى المَدْرَجِ. "
    "وَكُلَّمَا زَادَتِ السُّرْعَةُ زَادَ الرَّفْعُ، حَتَّى يَتَجَاوَزَ الوَزْنَ، فَتَرْتَفِعُ الطَّائِرَةُ.",
    # 3 how the wing makes lift
    "هٰذَا مَقْطَعُ الجَنَاحِ. الخَطُّ المُسْتَقِيمُ مِنْ حَافَّتِهِ الأَمَامِيَّةِ إِلَى حَافَّتِهِ الخَلْفِيَّةِ هُوَ الوَتَرُ. "
    "وَزَاوِيَةُ الهُجُومِ هِيَ الزَّاوِيَةُ بَيْنَ الوَتَرِ وَاتِّجَاهِ الهَوَاءِ النِّسْبِيِّ. "
    "الجَنَاحُ يَحْرِفُ الهَوَاءَ إِلَى الأَسْفَلِ، فَيَدْفَعُهُ الهَوَاءُ إِلَى الأَعْلَى: قَانُونُ نْيُوتِن الثَّالِثُ. "
    "وَفِي الوَقْتِ نَفْسِهِ يَكُونُ الضَّغْطُ فَوْقَ الجَنَاحِ أَقَلَّ مِنْهُ تَحْتَهُ: مَبْدَأُ بِرْنُولِّي. "
    "وَالتَّفْسِيرَانِ وَجْهَانِ لِلظَّاهِرَةِ نَفْسِهَا. "
    "زِيَادَةُ زَاوِيَةِ الهُجُومِ تَزِيدُ الرَّفْعَ، حَتَّى زَاوِيَةٍ حَرِجَةٍ، يَنْفَصِلُ بَعْدَهَا الهَوَاءُ عَنْ سَطْحِ الجَنَاحِ، "
    "فَيَنْخَفِضُ الرَّفْعُ بِسُرْعَةٍ: وَهٰذَا هُوَ الانْهِيَارُ، أَوِ السْتُول. "
    "وَأَخِيرًا، خُرَافَةٌ شَائِعَةٌ: أَنَّ الهَوَاءَ فَوْقَ الجَنَاحِ وَتَحْتَهُ يَصِلَانِ إِلَى الحَافَّةِ الخَلْفِيَّةِ فِي اللَّحْظَةِ نَفْسِهَا. "
    "هٰذَا غَيْرُ صَحِيحٍ؛ الهَوَاءُ فَوْقَ الجَنَاحِ يَصِلُ أَبْكَرَ.",
    # 4 the lift equation and a worked example
    "وَالآنَ بِالأَرْقَامِ. الرَّفْعُ يُسَاوِي نِصْفَ كَثَافَةِ الهَوَاءِ، فِي مُرَبَّعِ السُّرْعَةِ، فِي مِسَاحَةِ الجَنَاحِ، فِي مُعَامِلِ الرَّفْعِ. "
    "وَمُعَامِلُ الرَّفْعِ يَعْتَمِدُ عَلَى زَاوِيَةِ الهُجُومِ وَعَلَى القَلَّابَاتِ؛ وَالقَلَّابَاتُ تَزِيدُهُ، فَتُقْلِعُ الطَّائِرَةُ بِسُرْعَةٍ أَقَلَّ. "
    "وَلِأَنَّ السُّرْعَةَ مُرَبَّعَةٌ، فَضِعْفُ السُّرْعَةِ يُعْطِي أَرْبَعَةَ أَضْعَافِ الرَّفْعِ. "
    "مِثَالٌ: نَجْعَلُ الرَّفْعَ مُسَاوِيًا لِلْوَزْنِ. الكَثَافَةُ وَاحِدٌ فَاصِلَةُ مِئَتَيْنِ وَخَمْسَةٍ وَعِشْرِينَ، "
    "وَالمِسَاحَةُ مِئَةٌ وَعِشْرُونَ مِتْرًا مُرَبَّعًا، وَمُعَامِلُ الرَّفْعِ بِالقَلَّابَاتِ وَاحِدٌ فَاصِلَةُ سِتَّةٍ. "
    "فَالسُّرْعَةُ اللَّازِمَةُ سِتَّةٌ وَسَبْعُونَ فَاصِلَةُ أَرْبَعَةٍ مِتْرًا فِي الثَّانِيَةِ، "
    "أَيْ نَحْوُ مِئَتَيْنِ وَخَمْسَةٍ وَسَبْعِينَ كِيلُومِتْرًا فِي السَّاعَةِ.",
    # 5 the runway run: V1, VR, V2 (3D)
    "وَالآنَ نُرَافِقُ الطَّائِرَةَ عَلَى المَدْرَجِ. أَوَّلًا فِي وَنْ، سُرْعَةُ القَرَارِ: "
    "أَعْلَى سُرْعَةٍ يَتَّخِذُ عِنْدَهَا الطَّيَّارُ أَوَّلَ إِجْرَاءٍ لِلْإِيقَافِ، لِيَتَوَقَّفَ ضِمْنَ مَسَافَةِ التَّسَارُعِ وَالتَّوَقُّفِ. "
    "قَبْلَهَا يُلْغَى الإِقْلَاعُ عِنْدَ عُطْلٍ خَطِيرٍ، وَبَعْدَهَا يُكْمَلُ. "
    "ثُمَّ فِي آرْ، سُرْعَةُ الدَّوَرَانِ: يَرْفَعُ الطَّيَّارُ مُقَدِّمَةَ الطَّائِرَةِ، فَتَزِيدُ زَاوِيَةُ الهُجُومِ وَيَزِيدُ الرَّفْعُ. "
    "ثُمَّ فِي تُو، سُرْعَةُ الأَمَانِ فِي الإِقْلَاعِ، تَبْلُغُهَا الطَّائِرَةُ بَعْدَ أَنْ تَرْتَفِعَ. "
    "التَّرْتِيبُ: فِي وَنْ، ثُمَّ فِي آرْ، ثُمَّ فِي تُو؛ وَفِي وَنْ لَا تَتَجَاوَزُ فِي آرْ.",
    # 6 heat, wind and weight
    "ثَلَاثَةُ عَوَامِلَ تُغَيِّرُ هٰذِهِ السُّرْعَةَ. أَوَّلًا الحَرَارَةُ: الهَوَاءُ الحَارُّ أَقَلُّ كَثَافَةً. "
    "عِنْدَ خَمْسٍ وَأَرْبَعِينَ دَرَجَةً تَنْخَفِضُ الكَثَافَةُ إِلَى نَحْوِ وَاحِدٍ فَاصِلَةُ أَحَدَ عَشَرَ، "
    "فَتَصِيرُ السُّرْعَةُ اللَّازِمَةُ بِالنِّسْبَةِ لِلْهَوَاءِ ثَمَانِينَ فَاصِلَةُ ثَلَاثَةٍ مِتْرًا فِي الثَّانِيَةِ، أَعْلَى بِنَحْوِ خَمْسَةٍ فِي المِئَةِ، "
    "وَيَلْزَمُ مَدْرَجٌ أَطْوَلُ؛ مَعَ أَنَّ عَدَّادَ السُّرْعَةِ فِي قُمْرَةِ القِيَادَةِ يُظْهِرُ القِيمَةَ نَفْسَهَا. "
    "ثَانِيًا الرِّيَاحُ المُعَاكِسَةُ تُسَاعِدُ، لِأَنَّ الرَّفْعَ يَعْتَمِدُ عَلَى سُرْعَةِ الطَّائِرَةِ بِالنِّسْبَةِ لِلْهَوَاءِ لَا لِلْأَرْضِ؛ "
    "فَمَعَ رِيَاحٍ مُعَاكِسَةٍ سُرْعَتُهَا عَشَرَةُ أَمْتَارٍ فِي الثَّانِيَةِ، تَكْفِي سُرْعَةٌ أَرْضِيَّةٌ قَدْرُهَا سِتَّةٌ وَسِتُّونَ فَاصِلَةُ أَرْبَعَةٍ. "
    "ثَالِثًا الوَزْنُ: السُّرْعَةُ اللَّازِمَةُ تَتَنَاسَبُ مَعَ الجَذْرِ التَّرْبِيعِيِّ لِلْوَزْنِ؛ "
    "فَطَائِرَةٌ أَثْقَلُ بِعَشَرَةٍ فِي المِئَةِ تَحْتَاجُ سُرْعَةً أَعْلَى بِنَحْوِ أَرْبَعَةٍ فَاصِلَةُ تِسْعَةٍ فِي المِئَةِ.",
    # 7 conclusion
    "الخُلَاصَةُ: الجَنَاحُ يُوَلِّدُ الرَّفْعَ، وَالرَّفْعُ يَنْمُو مَعَ مُرَبَّعِ السُّرْعَةِ، وَكَثَافَةُ الهَوَاءِ تُحَدِّدُ كَمْ نَحْتَاجُ مِنْهَا. "
    "الجَنَاحُ وَالسُّرْعَةُ وَكَثَافَةُ الهَوَاءِ مَعًا تُحَدِّدُ لَحْظَةَ الإِقْلَاعِ.",
]

# Every spoken or shown value is checked against the data module; stop if it drifts.
assert f"{D.MASS:.0f}" == "70000" and f"{D.G}" == "9.81"                          # seg 1, 2
assert f"{D.WEIGHT:,.0f}" == "686,700"                                            # seg 2, 4
assert (f"{D.RHO_15:.3f}", f"{D.WING_AREA:.0f}", f"{D.CL_TAKEOFF}") == ("1.225", "120", "1.6")
assert f"{D.V_15:.1f}" == "76.4" and f"{D.V_15_KMH:.0f}" == "275"                 # seg 4
assert f"{D.LIFT_RATIO_DOUBLE_SPEED:.0f}" == "4"                                  # seg 4
assert f"{D.T_HOT_C:.0f}" == "45" and f"{D.RHO_HOT:.2f}" == "1.11"                # seg 6
assert f"{D.V_HOT:.1f}" == "80.3" and f"{D.HOT_INCREASE * 100:.0f}" == "5"        # seg 6
assert f"{D.HEADWIND:.0f}" == "10" and f"{D.V_GROUND_HEADWIND:.1f}" == "66.4"     # seg 6
assert f"{D.WEIGHT_INCREASE * 100:.0f}" == "10" and f"{D.HEAVY_INCREASE * 100:.1f}" == "4.9"

AUDIO_DIR = audio_dir_for(__file__)

# ---------------- 3D helpers (segments 1 and 5) ----------------
# World units: x along the runway (nose towards +x), y across it, z up; ground at z = 0.
PLANE_LENGTH = 6.6
GEAR_X = -0.2                       # x of the main gear: the pivot of the rotation at VR
_HULL_R, _HULL_Z = 0.37, 0.95       # fuselage radius and height of its axis above the ground
SCENE_DROP = 1.7                    # segment 1 sinks the scene so the title fits above it
_SKIN, _SKIN_LINE = "#fbfbfb", "#3a3a3a"
_ENGINE_FILL = "#fbe6d3"            # very light orange tint (orange = engines)


def _far_anchor(z=-60.0):
    """A far-below point used as depth key: everything tied to it is painted first."""
    return Dot(point=[0, 0, z], radius=0.01)


def _flat(points, fill=_SKIN, opacity=1.0, stroke=_SKIN_LINE, width=1.4):
    """A flat polygon in 3D that takes part in the depth sorting of the camera."""
    poly = Polygon(*points, color=stroke, fill_color=fill, fill_opacity=opacity, stroke_width=width)
    poly.set_shade_in_3d(True)
    return poly


def _skin(surface):
    surface.set_style(fill_color=_SKIN, fill_opacity=1, stroke_color=GREY_INK, stroke_width=0.5)
    return surface


def airliner_3d(scale=1.0):
    """A generic twin-engine airliner from basic shapes: nose towards +x, standing on z = 0.

    Returns a VGroup with the parts as attributes: fuselage, wings (VGroup, both sides), tail,
    engines, gear, shadow; `pivot` is the point on the ground under the main gear (rotation
    about it lifts the nose: rotate about the y axis). No type, airline, logo or registration.
    """
    x0, x1, x_tail, x_nose = -PLANE_LENGTH / 2, PLANE_LENGTH / 2, -1.7, 2.3
    r0 = _HULL_R

    def hull(u, v):
        x = x0 + (x1 - x0) * u
        z_up = 0.0
        if x < x_tail:                                  # tail cone, swept up
            s = (x - x0) / (x_tail - x0)
            r, z_up = r0 * (0.1 + 0.9 * (1 - (1 - s) ** 2)), 0.32 * (1 - s) ** 2
        elif x > x_nose:                                # rounded nose
            q = (x - x_nose) / (x1 - x_nose)
            r = r0 * np.sqrt(max(1 - q * q, 0.02))          # never a point: a pole breaks the mesh
        else:
            r = r0
        return np.array([x, r * np.cos(v), _HULL_Z + z_up + r * np.sin(v)])

    fuselage = _skin(Surface(hull, u_range=[0, 1], v_range=[0, TAU], resolution=(32, 14),
                             checkerboard_colors=False))
    fuselage.set_style(fill_color="#f2f2f2", fill_opacity=1, stroke_color="#a8a8a8", stroke_width=0.35)
    fuselage.set_shade_in_3d(True)

    wing_z = _HULL_Z - 0.18
    wings = VGroup()
    for k in (1, -1):
        wings.add(_flat([[0.95, k * 0.3, wing_z], [-0.95, k * 3.0, wing_z + 0.22],
                         [-1.45, k * 3.0, wing_z + 0.22], [-0.75, k * 0.3, wing_z]]))
    tail = VGroup(*[_flat([[-2.55, k * 0.1, _HULL_Z + 0.25], [-3.15, k * 1.25, _HULL_Z + 0.42],
                           [-3.45, k * 1.25, _HULL_Z + 0.42], [-3.2, k * 0.1, _HULL_Z + 0.3]])
                    for k in (1, -1)])
    tail.add(_flat([[-1.9, 0, _HULL_Z + 0.3], [-3.0, 0, _HULL_Z + 1.15],
                    [-3.4, 0, _HULL_Z + 1.15], [-3.3, 0, _HULL_Z + 0.4]]))          # the fin

    engines = VGroup()
    for k in (1, -1):
        e = Cylinder(radius=0.27, height=1.1, direction=RIGHT, resolution=(6, 14), show_ends=True)
        e.set_style(fill_color=_ENGINE_FILL, fill_opacity=1, stroke_color=GREY_INK, stroke_width=0.5)
        e.set_shade_in_3d(True)
        e.move_to([0.55, k * 1.15, _HULL_Z - 0.5])
        engines.add(e, _flat([[0.35, k * 1.15, _HULL_Z - 0.28], [-0.1, k * 1.15, _HULL_Z - 0.28],
                              [-0.3, k * 1.15, wing_z + 0.08], [0.1, k * 1.15, wing_z + 0.08]],
                             fill=GREY_INK, stroke=GREY_INK, width=1))

    gear = VGroup()
    for x, y, h in [(GEAR_X, 0.9, 0.45), (GEAR_X, -0.9, 0.45), (1.7, 0.0, 0.5)]:
        strut = _flat([[x - 0.03, y, 0.17], [x + 0.03, y, 0.17], [x + 0.03, y, h + 0.3], [x - 0.03, y, h + 0.3]],
                      fill=GREY_INK, stroke=GREY_INK, width=1)
        wheel = Cylinder(radius=0.17, height=0.14, direction=UP, resolution=(4, 12))
        wheel.set_style(fill_color=GREY_INK, fill_opacity=1, stroke_color=INK, stroke_width=0.4)
        wheel.set_shade_in_3d(True)
        wheel.move_to([x, y, 0.17])
        gear.add(strut, wheel)

    shadow = Polygon([2.6, 0, 0.02], [0.9, 0.5, 0.02], [-0.9, 3.0, 0.02], [-1.45, 3.0, 0.02],
                     [-1.6, 0.5, 0.02], [-3.4, 0.9, 0.02], [-3.4, -0.9, 0.02], [-1.6, -0.5, 0.02],
                     [-1.45, -3.0, 0.02], [-0.9, -3.0, 0.02], [0.9, -0.5, 0.02],
                     color=PANEL_FILL, fill_color="#e4e4e4", fill_opacity=0.9, stroke_width=0)
    shadow.set_shade_in_3d(True)
    shadow.z_index_group = _far_anchor(-50.0)           # after the runway, before the plane

    plane = VGroup(shadow, gear, fuselage, wings, tail, engines)
    plane.shadow, plane.gear, plane.fuselage, plane.wings, plane.tail, plane.engines = (
        shadow, gear, fuselage, wings, tail, engines)
    plane.pivot = np.array([GEAR_X, 0.0, 0.0])
    if scale != 1.0:
        plane.scale(scale, about_point=ORIGIN)
        plane.pivot = plane.pivot * scale
    return plane


def runway_3d(x_start=-9.0, length=70.0, width=4.6):
    """A long light-grey runway with edge lines, a dashed centreline and threshold bars.

    Painted first whatever the camera angle (one depth key for the whole group).
    """
    x_end = x_start + length
    w = width / 2
    parts = VGroup(_flat([[x_start, -w, 0], [x_end, -w, 0], [x_end, w, 0], [x_start, w, 0]],
                         fill="#d2d2d2", stroke=GREY_INK, width=1.5))
    for k in (1, -1):                                   # edge lines
        parts.add(_flat([[x_start, k * (w - 0.12), 0.01], [x_end, k * (w - 0.12), 0.01],
                         [x_end, k * (w - 0.16), 0.01], [x_start, k * (w - 0.16), 0.01]],
                        fill=LIGHT_INK, stroke=LIGHT_INK, width=0.5))
    x = x_start + 4.2
    while x < x_end - 1.0:                              # dashed centreline
        parts.add(_flat([[x, -0.06, 0.01], [x + 1.4, -0.06, 0.01], [x + 1.4, 0.06, 0.01], [x, 0.06, 0.01]],
                        fill=WHITE, stroke=WHITE, width=0.5))
        x += 2.6
    for i in range(-4, 5):                              # threshold bars ("piano keys")
        if i == 0:
            continue
        y = i * 0.32
        parts.add(_flat([[x_start + 0.5, y - 0.09, 0.01], [x_start + 2.3, y - 0.09, 0.01],
                         [x_start + 2.3, y + 0.09, 0.01], [x_start + 0.5, y + 0.09, 0.01]],
                        fill=WHITE, stroke=WHITE, width=0.5))
    anchor = _far_anchor()
    for m in parts:
        m.z_index_group = anchor
    parts.anchor = anchor
    return parts


# ---------------- 2D helpers (segment 2) ----------------
RUNWAY_Y = -1.5                     # top edge of the runway (the wheels stand on it)
PLANE_SCALE = 1.2                   # side-view airliner scale (units of airliner_side)
CG_HEIGHT = 0.75 * PLANE_SCALE      # centre of the fuselage above the ground
PLANE_X = 1.8                       # x of the centre of gravity
LEN_W, LEN_T, LEN_D = 1.2, 3.4, 2.5  # weight arrow; thrust longer than drag (units)
BAR_W = 2.4                         # length of the weight bar; the lift bar is BAR_W * L / W
P_MAX = 1.10                        # V / V(L = W) at the end of the segment


def airliner_side():
    """A generic airliner in side view (nose to the right), centre of gravity at the origin.

    Parts as attributes: body, wings, engine, fin; `ground` is the wheel-bottom offset.
    """
    poly = lambda pts, **kw: Polygon(*[[x, y, 0] for x, y in pts], **kw)
    body = RoundedRectangle(width=3.6, height=0.56, corner_radius=0.28, color=INK,
                            fill_color=WHITE, fill_opacity=1, stroke_width=3)
    window = poly([(1.2, 0.04), (1.62, 0.04), (1.55, 0.18), (1.2, 0.18)], color=GREY_INK,
                     fill_color=PANEL_FILL, fill_opacity=1, stroke_width=1.5)
    fin = poly([(-1.25, 0.2), (-1.85, 0.95), (-1.45, 0.95), (-0.8, 0.25)], color=INK,
                  fill_color=WHITE, fill_opacity=1, stroke_width=3)
    wings = poly([(0.55, -0.1), (-0.35, -0.1), (-1.0, -0.52), (-0.7, -0.52)], color=INK,
                    fill_color=WHITE, fill_opacity=1, stroke_width=3)
    engine = RoundedRectangle(width=0.8, height=0.3, corner_radius=0.14, color=ACCENT_2,
                              fill_color=ACCENT_2, fill_opacity=0.35, stroke_width=3)
    engine.move_to([0.7, -0.47, 0])
    gear = VGroup()
    for x in (-0.35, 1.4):
        gear.add(Line([x, -0.28, 0], [x, -0.64, 0], color=GREY_INK, stroke_width=3),
                 Circle(radius=0.11, color=INK, fill_color=GREY_INK, fill_opacity=1,
                        stroke_width=2).move_to([x, -0.64, 0]))
    plane = VGroup(gear, fin, body, window, wings, engine)
    plane.body, plane.wings, plane.engine, plane.fin = body, wings, engine, fin
    return plane


class TakeoffLift(SyncedScene, ThreeDScene):
    """SyncedScene timing on a 3D camera: 2D segments keep the default top-down view."""

    def construct(self):
        self.timeline(NARRATION, AUDIO_DIR)

        # ---------------- Segment 1: the question (3D) ----------------
        self.segment_1()
        self.sync(self.end(1))

        # ---------------- Segment 2: the four forces ----------------
        self.segment_2()
        self.sync(self.end(2))

        # ---------------- Segment 3: how the wing makes lift ----------------
        self.sync(self.end(3))

        # ---------------- Segment 4: the lift equation, worked example ----------------
        self.sync(self.end(4))

        # ---------------- Segment 5: the runway run, V1 VR V2 (3D) ----------------
        self.sync(self.end(5))

        # ---------------- Segment 6: heat, wind and weight ----------------
        self.sync(self.end(6))

        # ---------------- Segment 7: conclusion ----------------
        self.sync(self.end(7) + 1.0)

    # ---------------- 3D camera helpers ----------------
    def camera_path(self, keys):
        """Drive the camera along keyframes [(t, phi_deg, theta_deg, zoom), ...] (the camera always looks at the origin: a moved
        frame centre is applied twice by ThreeDCamera and throws fixed-in-frame texts off) on the
        narration clock (smooth through the keys, no stop at each one). The driver is added FIRST so
        every 3D object after it is redrawn each frame (nothing is cached as a static picture)."""
        from scipy.interpolate import PchipInterpolator
        ts = [k[0] for k in keys]
        spline = PchipInterpolator(ts, np.array([k[1:4] for k in keys], dtype=float))
        driver = Mobject()
        driver.clock = self.renderer.time

        def follow(m, dt):
            m.clock += dt
            phi, theta, zoom = spline(min(max(m.clock, ts[0]), ts[-1]))
            self.camera.set_phi(phi * DEGREES)
            self.camera.set_theta(theta * DEGREES)
            self.camera.set_zoom(zoom)
        driver.add_updater(follow)
        follow(driver, 0)
        self.add(driver)
        return driver

    def fixed(self, *mobs):
        """Put texts and leaders in the frame (they ignore the camera); returns them as a group."""
        self.add_fixed_in_frame_mobjects(*mobs)
        self.remove(*mobs)                  # add_fixed_in_frame_mobjects also adds them: show them by FadeIn
        return VGroup(*mobs)

    def reset_camera_2d(self, driver=None):
        """Fade the 3D scene and its overlays out and restore the default top-down camera."""
        self.clear()
        if driver is not None:
            driver.clear_updaters()
        self.camera.fixed_in_frame_mobjects.clear()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1)
        self.camera.should_apply_shading = True

    # ---------------- Segment 1 ----------------
    def segment_1(self):
        c = lambda phrase, nth=1: self.cue(1, phrase, nth)
        runway, plane = runway_3d(), airliner_3d()
        t0 = self.start(1)
        driver = self.camera_path([
            (t0 + 0.0, 30, -62, 0.60),                      # high and wide
            (t0 + 7.0, 50, -50, 0.78),
            (t0 + 12.0, 68, -40, 1.05),                     # low three-quarter view beside the plane
            (t0 + 22.3, 74, -32, 1.12),
        ])
        self.camera.should_apply_shading = False            # flat whiteboard fills, exact colours
        runway.shift(IN * SCENE_DROP)                       # sit lower on screen: room for the title
        plane.shift(IN * SCENE_DROP)
        self.add(runway, plane)

        # disclaimer (the first sentence of the narration)
        note = fit(VGroup(label("Educational material. The binding reference is the official", FS_NOTE),
                          label("documentation and approved procedures.", FS_NOTE))
                   .arrange(DOWN, buff=0.12), 12.4)
        box = SurroundingRectangle(note, buff=0.2, color=LIGHT_INK, fill_color=WHITE,
                                   fill_opacity=0.92, stroke_width=1.5)
        disclaimer = self.fixed(box, note).to_edge(UP, buff=0.35)
        self.sync(t0 + 0.1)
        self.play(FadeIn(disclaimer, run_time=0.6))
        self.sync(c("طَائِرَةُ") - 0.7)
        self.play(FadeOut(disclaimer, run_time=0.6))

        # "m = 70 t" with a leader that follows the plane while the camera moves
        tag = label(f"m = {D.MASS / 1000:.0f} t", FS_LABEL)
        tag_box = SurroundingRectangle(tag, buff=0.15, color=ACCENT_4, fill_color=WHITE,
                                       fill_opacity=0.95, stroke_width=2)
        tag_grp = self.fixed(tag_box, tag).move_to([5.3, 0.9, 0])
        leader = Line(ORIGIN, RIGHT, color=ACCENT_4, stroke_width=2.5)
        dot = Dot(color=ACCENT_4, radius=0.07)

        def track(_):
            a = plane.fuselage.get_center() + np.array([1.2, 0, 0.42])
            end = self.camera.project_point(a)
            leader.put_start_and_end_on(tag_box.get_left(), end)
            dot.move_to(end)
        leader.add_updater(track)
        track(leader)
        self.fixed(leader, dot)
        self.sync(c("سَبْعُونَ") - 0.1)
        self.play(FadeIn(tag_grp, run_time=0.5), FadeIn(leader, run_time=0.5), FadeIn(dot, run_time=0.5))

        # the question and the answer as a title
        title = fit(label("How does an airplane take off?", FS_TITLE), 12.4).to_edge(UP, buff=0.35)
        self.fixed(title)
        self.sync(c("فَكَيْفَ") - 0.1)
        self.play(FadeIn(title, shift=DOWN * 0.15, run_time=0.6))
        sub = label("Lift and takeoff speeds", FS_SUBTITLE, GREY_INK)
        ic = icon("plane-departure", ACCENT_1, 0.6)
        sub_grp = VGroup(ic, sub).arrange(RIGHT, buff=0.25).next_to(title, DOWN, buff=0.25)
        self.fixed(ic, sub)
        self.sync(c("الجَوَابُ") - 0.1)
        self.play(FadeIn(sub_grp, run_time=0.5))

        # the wing, then the speed
        self.sync(c("الجَنَاحِ") - 0.05)
        self.play(plane.wings.animate(run_time=0.8).set_fill(ACCENT_1, 0.95).set_stroke(ACCENT_1))
        self.sync(c("وَالسُّرْعَةِ") - 0.05)
        streaks = VGroup()
        for i, (y, z, x) in enumerate([(-2.1, 0.6, 5), (-1.2, 1.5, 7), (-0.5, 0.35, 9), (0.4, 1.7, 6),
                                       (1.1, 0.5, 8), (1.9, 1.3, 5.5), (-1.7, 1.0, 10), (2.3, 0.4, 9.5)]):
            ln = Line([x, y, z - SCENE_DROP], [x + 2.2, y, z - SCENE_DROP], color=ACCENT_1, stroke_width=3.5)
            ln.set_shade_in_3d(True)
            streaks.add(ln)
        self.add(streaks)
        roll = self.end(1) - 0.65 - self.renderer.time
        self.play(FadeOut(VGroup(tag_grp, leader, dot), run_time=0.4),
                  streaks.animate(run_time=roll, rate_func=linear).shift(LEFT * 16),
                  plane.animate(run_time=roll, rate_func=rate_functions.ease_in_quad).shift(RIGHT * 2.5))
        self.reset_camera_2d(driver)

    # ---------------- Segment 2 ----------------
    def segment_2(self):
        c = lambda phrase, nth=1: self.cue(2, phrase, nth)
        t0, t_end = self.start(2), self.end(2)
        t_acc = c("فَتَتَسَارَعُ")                              # the run begins
        t_lift = c("الوَزْنَ") + 0.25                          # V reaches the speed where L = W
        st = dict(p=0.0, scroll=0.0, h=0.0, ang=0.0)

        plane = airliner_side().scale(PLANE_SCALE, about_point=ORIGIN)
        plane.shift([PLANE_X, RUNWAY_Y + CG_HEIGHT, 0])
        cg = lambda: plane.body.get_center()
        ratio = ValueTracker(0.0)                              # lift / weight
        gw, gt, gd = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)   # arrows growing
        ro = ValueTracker(0.0)                                 # opacity of the readout and bars

        # --- runway: two edge lines and a dashed centreline that scrolls with the speed
        top = Line([-6.85, RUNWAY_Y, 0], [6.85, RUNWAY_Y, 0], color=GREY_INK, stroke_width=3)
        bottom = Line([-6.85, RUNWAY_Y - 1.6, 0], [6.85, RUNWAY_Y - 1.6, 0], color=GREY_INK, stroke_width=3)
        dashes = VGroup(*[Line(ORIGIN, RIGHT * 0.6, color=LIGHT_INK, stroke_width=5) for _ in range(8)])

        def place_dashes(m):
            for i, d in enumerate(m):
                x = -6.8 + (i * 1.65 - st["scroll"]) % 13.2
                d.put_start_and_end_on([x, RUNWAY_Y - 0.95, 0], [x + 0.6, RUNWAY_Y - 0.95, 0])
        place_dashes(dashes)
        dashes.add_updater(place_dashes)

        # --- driver on the narration clock: speed, scrolling, lift-off (added first)
        driver = Mobject()
        driver.clock = self.renderer.time
        driver.last = (0.0, 0.0)

        def drive(m, dt):
            m.clock += dt
            T = m.clock
            p = min(max((T - t_acc) / (t_lift - t_acc), 0.0), P_MAX)
            st["p"] = p
            if T < t_lift:
                st["scroll"] += p * 5.0 * dt
            if T >= t_acc:
                ratio.set_value(p * p)
            s = min(max((T - t_lift) / (t_end - t_lift), 0.0), 1.0)
            h, ang = 1.5 * s ** 1.5, 6.0 * min(1.0, 3 * s)
            plane.shift(UP * (h - m.last[0]))
            plane.rotate((ang - m.last[1]) * DEGREES, about_point=plane.body.get_center())
            m.last = (h, ang)
        driver.add_updater(drive)
        self.add(driver)
        _play = self.play

        def synced_play(*a, **k):
            """Manim's first frame of every play has dt = 0: put the driver back on the clock."""
            _play(*a, **k)
            driver.clock = self.renderer.time
        self.play = synced_play

        # --- force arrows and their labels (follow the centre of gravity)
        def arrow(direction, colour, length):
            def build():
                L = length()
                if L < 0.08:
                    return VMobject()
                s = cg()
                return Arrow(s, s + direction * L, buff=0, color=colour, stroke_width=7,
                             tip_length=min(0.28, 0.5 * L), max_tip_length_to_length_ratio=0.6,
                             max_stroke_width_to_length_ratio=12)
            return always_redraw(build)

        def tag(text, colour, tip, direction, alpha):
            def build():
                t = label(text, FS_LABEL, colour).next_to(tip(), direction, buff=0.15)
                return t.set_opacity(alpha())
            return always_redraw(build)

        lift_len = lambda: LEN_W * ratio.get_value()
        lift_tip = lambda: cg() + UP * max(lift_len(), 0.9)
        a_lift = arrow(UP, ACCENT_1, lift_len)
        a_weight = arrow(DOWN, ACCENT_4, lambda: LEN_W * gw.get_value())
        a_thrust = arrow(RIGHT, ACCENT_2, lambda: LEN_T * gt.get_value())
        a_drag = arrow(LEFT, ACCENT_4, lambda: LEN_D * gd.get_value())
        on = lambda g: (lambda: min(1.0, max(0.0, (g.get_value() - 0.6) / 0.4)))
        gl = ValueTracker(0.0)                                  # the "Lift" tag stays once shown
        t_lift_tag = tag("Lift", ACCENT_1, lift_tip, UP, on(gl))
        t_weight = tag("Weight", ACCENT_4, lambda: cg() + DOWN * LEN_W, DOWN, on(gw))
        t_thrust = tag("Thrust", ACCENT_2, lambda: cg() + RIGHT * LEN_T, RIGHT, on(gt))
        t_drag = tag("Drag", ACCENT_4, lambda: cg() + LEFT * LEN_D, LEFT, on(gd))

        # --- the four forces come in, at their words
        self.sync(t0 + 0.1)
        sec = section_title(self, "The four forces")
        self.sec = sec
        self.play(Create(top), Create(bottom), FadeIn(plane, shift=DOWN * 0.2), FadeIn(dashes), run_time=1.0)
        self.add(a_lift, t_lift_tag, a_weight, t_weight, a_thrust, t_thrust, a_drag, t_drag)

        self.sync(c("الرَّفْعُ") - 0.1)
        self.play(ratio.animate.set_value(1.0), gl.animate.set_value(1.0), run_time=0.7)
        self.sync(c("الجَنَاحُ") - 0.1)
        self.play(plane.wings.animate.set_fill(ACCENT_1, 0.9).set_stroke(ACCENT_1), run_time=0.6)
        self.play(Flash(plane.wings.get_center(), color=ACCENT_1, flash_radius=0.5, line_length=0.15,
                        run_time=0.6))
        self.sync(c("وَالوَزْنُ") - 0.1)
        self.play(gw.animate.set_value(1.0), run_time=0.7)

        # weight calculation, line by line, from the data module
        w1 = label("W = m · g", FS_LABEL + 2, ACCENT_4)
        w2 = label(f"= {D.MASS:,.0f} kg × {D.G} m/s²", FS_LABEL)
        w3 = label(f"= {D.WEIGHT:,.0f} N", FS_LABEL + 2, ACCENT_4, weight=BOLD)
        calc = VGroup(w1, w2, w3).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        calc.next_to(sec, DOWN, buff=0.4).align_to(sec, LEFT)
        self.sync(c("الكُتْلَةُ") - 0.1)
        self.play(Write(w1), run_time=0.8)
        self.sync(c("سَبْعُونَ") - 0.1)
        self.play(Write(w2), run_time=1.2)
        self.sync(c("أَيْ") - 0.1)
        self.play(Write(w3), run_time=1.0)

        # thrust from the engines, drag from the air
        self.sync(c("وَالدَّفْعُ") - 0.1)
        self.play(gt.animate.set_value(1.0), run_time=0.7)
        self.sync(c("المُحَرِّكَاتِ") - 0.1)
        self.play(Indicate(plane.engine, color=ACCENT_2, scale_factor=1.5), run_time=0.9)
        self.sync(c("وَالسَّحْبُ") - 0.1)
        self.play(gd.animate.set_value(1.0), run_time=0.7)
        self.sync(c("مُقَاوَمَةُ") - 0.1)
        streaks = VGroup(*[Line([PLANE_X + 3.9, RUNWAY_Y + CG_HEIGHT + dy, 0],
                                [PLANE_X + 4.6, RUNWAY_Y + CG_HEIGHT + dy, 0],
                                color=ACCENT_1, stroke_width=4) for dy in (0.6, 1.0, 1.4)])
        self.play(FadeIn(streaks, run_time=0.3))
        self.play(streaks.animate(run_time=1.0, rate_func=linear).shift(LEFT * 1.6))
        self.play(FadeOut(streaks, run_time=0.3))

        # readout and bars: at rest the lift is zero
        v_read = always_redraw(lambda: label(f"V = {st['p'] * D.V_15:.1f} m/s", FS_LABEL)
                               .next_to(calc, DOWN, buff=0.45).align_to(calc, LEFT).set_opacity(ro.get_value()))
        n_lift = label("Lift", FS_NOTE, ACCENT_1)
        n_weight = label("Weight", FS_NOTE, ACCENT_4)
        names = VGroup(n_lift, n_weight).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        names.next_to(v_read, DOWN, buff=0.4).align_to(calc, LEFT)
        bx = names.get_right()[0] + 0.3
        bar_lift = always_redraw(lambda: Rectangle(width=max(BAR_W * ratio.get_value(), 0.02), height=0.28,
                                                   color=ACCENT_1, fill_color=ACCENT_1, fill_opacity=ro.get_value(),
                                                   stroke_width=0).move_to([bx, n_lift.get_center()[1], 0], LEFT)
                                 .set_stroke(opacity=0))
        bar_weight = Rectangle(width=BAR_W, height=0.28, color=ACCENT_4, fill_color=ACCENT_4,
                               fill_opacity=1, stroke_width=0).move_to([bx, n_weight.get_center()[1], 0], LEFT)
        mark = DashedLine([bx + BAR_W, n_lift.get_center()[1] + 0.3, 0],
                          [bx + BAR_W, n_weight.get_center()[1] - 0.3, 0], color=GREY_INK, stroke_width=2.5)
        self.sync(c("فِي الإِقْلَاعِ") - 0.1)
        self.add(v_read, bar_lift)
        self.play(FadeIn(names), FadeIn(bar_weight), FadeIn(mark), ro.animate.set_value(1.0),
                  ratio.animate.set_value(0.0), run_time=0.8)
        self.sync(c("الدَّفْعُ") - 0.1)
        self.say("Thrust > Drag", y=-3.5)
        self.sync(t_acc - 0.1)
        self.say("The plane accelerates", y=-3.5)
        self.sync(c("وَكُلَّمَا") - 0.1)
        self.say("More speed, more lift", y=-3.5)
        self.sync(c("حَتَّى") - 0.1)
        self.say("Lift > Weight: the plane rises", y=-3.5)
        self.sync(t_end)
        del self.play                                           # back to the class method


if __name__ == "__main__":
    main(__file__, "TakeoffLift", NARRATION)
