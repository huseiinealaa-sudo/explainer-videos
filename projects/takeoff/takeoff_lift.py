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
    fuselage.set_style(fill_color="#f2f2f2", fill_opacity=1, stroke_color="#a8a8a8", stroke_width=0.35,
                       stroke_opacity=0.15)                 # no lat/long mesh lines: a smooth hull
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
        e = Cylinder(radius=0.27, height=1.1, direction=RIGHT, resolution=(6, 14), show_ends=True,
                     checkerboard_colors=False)
        e.set_style(fill_color=_ENGINE_FILL, fill_opacity=1, stroke_color=GREY_INK, stroke_width=0,
                    stroke_opacity=0)                       # no basket pattern on the nacelles
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


# ---------------- 2D helpers (segment 3): the wing section and the flow round it ----------------
# The section is a Joukowski profile (computed, not drawn by hand) and the streamlines are the potential
# flow past it with the Kutta condition: faster and lower-pressure over the top, deflected down behind.
_J_A, _J_EPS, _J_DEL = 1.0, 0.15, 0.07
_J_MU = complex(-_J_EPS, _J_DEL)
_J_R = abs(_J_A - _J_MU)
_J_PROFILE = _J_MU + _J_R * np.exp(1j * np.linspace(0, TAU, 160, endpoint=False))
_J_PROFILE = _J_PROFILE + _J_A ** 2 / _J_PROFILE
_J_TE = complex(2 * _J_A, 0)
_J_LE = _J_PROFILE[np.argmax(abs(_J_PROFILE - _J_TE))]
_J_THETA = np.angle(_J_TE - _J_LE)                      # tilt of the chord line in the profile's own frame
_J_SCALE = 4.6 / abs(_J_TE - _J_LE)                     # chord length on screen: 4.6 units
_J_PIVOT = _J_LE + 0.25 * (_J_TE - _J_LE)               # quarter chord: the wing pitches about it
WING_PIVOT = np.array([-3.0, -0.35])                    # where the quarter chord sits on screen
ALPHA_WORK, ALPHA_CRIT, ALPHA_STALL = 9.0, 15.0, 19.0   # degrees, schematic (drawn larger than real)
FLOW_X0, FLOW_X1 = -5.5, 3.3                            # streamlines are drawn between these x
# sketch of C_L against the angle of attack (no values are shown): rises, peaks, then falls but not to 0
_CL_CURVE = None


def cl_curve(alpha):
    """Schematic lift coefficient (0..1, peak at ALPHA_CRIT) for an angle of attack in degrees."""
    global _CL_CURVE
    if _CL_CURVE is None:
        from scipy.interpolate import PchipInterpolator
        pts = [(0, .12), (3, .31), (6, .52), (9, .75), (12, .93), (14, .99), (15, 1.0), (16, .97),
               (17, .86), (19, .66), (22, .50), (24, .44)]
        _CL_CURVE = PchipInterpolator(*zip(*pts))
    return float(_CL_CURVE(min(max(alpha, 0.0), 24.0)))


def _cplx(p):
    return complex(p[0], p[1])


class WingFlow:
    """The wing at `alpha` degrees (chord tilted nose-up about the quarter chord) in a horizontal wind."""

    def __init__(self, alpha):
        self.al = np.radians(alpha)
        self.af = self.al + _J_THETA                    # wind direction in the profile's frame
        zp = _J_A - _J_MU                               # Kutta: the velocity at the trailing edge is finite
        g = -(np.exp(-1j * self.af) - _J_R ** 2 * np.exp(1j * self.af) / zp ** 2) * 2 * np.pi * zp / 1j
        self.gam = g.real
        self.pivot = _cplx(WING_PIVOT)

    def to_world(self, z):
        return self.pivot + _J_SCALE * np.exp(-1j * (self.al + _J_THETA)) * (np.asarray(z) - _J_PIVOT)

    def to_z(self, w):
        return _J_PIVOT + np.exp(1j * (self.al + _J_THETA)) * (w - self.pivot) / _J_SCALE

    def velocity(self, w):
        z = self.to_z(w)
        s = np.sqrt(z * z - 4 * _J_A ** 2 + 0j)
        z1, z2 = (z + s) / 2, (z - s) / 2
        zt = z1 if abs(z1 - _J_MU) > abs(z2 - _J_MU) else z2
        zp = zt - _J_MU
        dw = np.exp(-1j * self.af) - _J_R ** 2 * np.exp(1j * self.af) / zp ** 2 + 1j * self.gam / (2 * np.pi * zp)
        return np.conj(dw / (1 - _J_A ** 2 / zt ** 2)) * np.exp(-1j * (self.al + _J_THETA))

    def outline(self):
        return self.to_world(_J_PROFILE)

    def le(self):
        return self.to_world(_J_LE)

    def te(self):
        return self.to_world(_J_TE)

    def stream(self, y0, x0=-6.6, dt=0.05, x1=FLOW_X1, nmax=1500):
        """Streamline from (x0, y0) as complex points, one every dt of flow time (speed 1 far away)."""
        w, pts, f = complex(x0, y0), [complex(x0, y0)], self.velocity
        for _ in range(nmax):
            k1 = f(w)
            k2 = f(w + dt / 2 * k1)
            k3 = f(w + dt / 2 * k2)
            k4 = f(w + dt * k3)
            w = w + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            pts.append(w)
            if w.real > x1:
                break
        return np.array(pts)

    def divider(self):
        """Seed height (at x = -6.6) of the streamline that splits at the leading edge."""
        le = self.le()
        lo, hi = -2.5, 2.5
        for _ in range(28):
            mid = (lo + hi) / 2
            s = self.stream(mid, dt=0.06, x1=le.real + 0.3)
            over = s[np.argmin(abs(s.real - le.real))].imag > le.imag
            lo, hi = (lo, mid) if over else (mid, hi)
        return (lo + hi) / 2


def _pts3(cs):
    cs = np.asarray(cs)
    return [[c.real, c.imag, 0.0] for c in cs]


def _polyline(cs, color, width, opacity=1.0):
    m = VMobject(color=color, stroke_width=width, stroke_opacity=opacity)
    m.set_points_as_corners(_pts3(cs))
    return m


def _minus(color):
    return VGroup(Circle(radius=0.19, color=color, stroke_width=3),
                  Line([-0.11, 0, 0], [0.11, 0, 0], color=color, stroke_width=4))


def _plus(color):
    return VGroup(Circle(radius=0.19, color=color, stroke_width=3),
                  Line([-0.11, 0, 0], [0.11, 0, 0], color=color, stroke_width=4),
                  Line([0, -0.11, 0], [0, 0.11, 0], color=color, stroke_width=4))


# ---------------- 2D helpers (segment 4): the lift equation ----------------
# Schematic lift coefficients for the flap drawing (only bar lengths, no numbers are shown for them):
# wing at zero angle of attack and at the working angle without flaps; with takeoff flaps it is CL_TAKEOFF.
CL_ZERO_S, CL_CLEAN_S = 0.85, 1.1


def _cl_label(size, color=INK):
    """C with a small subscript L (no LaTeX in the container)."""
    c = label("C", size, color)
    sub = label("L", max(int(size * 0.65), 16), color)
    sub.next_to(c, RIGHT, buff=0.03).align_to(c, DOWN).shift(DOWN * 0.08)
    return VGroup(c, sub)


def _stack(*lines, size=FS_TAG, color=GREY_INK):
    return VGroup(*[label(t, size, color) for t in lines]).arrange(DOWN, buff=0.05)


def _sqrt_frac(num, den, color=INK, width=3):
    """A square root over a fraction, from a VGroup numerator and denominator (returns a VGroup)."""
    bar = Line(LEFT, RIGHT, color=color, stroke_width=width)
    frac = VGroup(num, bar, den).arrange(DOWN, buff=0.14)
    w = max(num.width, den.width) + 0.25
    bar.put_start_and_end_on(bar.get_center() + LEFT * w / 2, bar.get_center() + RIGHT * w / 2)
    left, right = frac.get_left()[0] - 0.1, frac.get_right()[0] + 0.1
    top, bot = frac.get_top()[1] + 0.14, frac.get_bottom()[1]
    cy = (top + bot) / 2
    rad = VMobject(color=color, stroke_width=width)
    rad.set_points_as_corners([[left - 0.36, cy - 0.02, 0], [left - 0.27, cy + 0.06, 0],
                               [left - 0.14, bot - 0.06, 0], [left - 0.03, top, 0], [right, top, 0]])
    grp = VGroup(rad, frac)
    grp.num, grp.bar, grp.den, grp.rad, grp.frac = num, bar, den, rad, frac
    return grp

# ---------------- 2D helpers (segment 6): heat, wind and weight ----------------
GAUGE_MARK = 0.62                   # needle position (0..1 of the dial) at the lift-off reading, the same for both dials


def _gauge(r=0.8):
    """A round airspeed dial without numbers: face, ticks, a green mark at GAUGE_MARK, hub. Needle: see _needle."""
    ang = lambda u: 225 * DEGREES - 270 * DEGREES * u
    dirn = lambda u: np.array([np.cos(ang(u)), np.sin(ang(u)), 0.0])
    face = Circle(radius=r * 1.08, color=INK, fill_color=WHITE, fill_opacity=1, stroke_width=3)
    ticks = VGroup(*[Line(dirn(u) * r * 0.82, dirn(u) * r * 0.98, color=GREY_INK, stroke_width=3)
                     for u in np.linspace(0, 1, 9)])
    mark = Line(dirn(GAUGE_MARK) * r * 0.74, dirn(GAUGE_MARK) * r * 1.0, color=ACCENT_3, stroke_width=7)
    hub = Dot(ORIGIN, radius=0.06, color=INK)
    g = VGroup(face, ticks, mark, hub)
    g.r, g.dirn = r, dirn
    return g


def _needle(gauge, u):
    """Needle of a dial that follows a ValueTracker u (0..1)."""
    return always_redraw(lambda: Line(gauge.get_center(), gauge.get_center() + gauge.dirn(u.get_value()) * gauge.r * 0.7,
                                      color=INK, stroke_width=5))


def _jiggle_dots(box, bases0, bases1, keep, tracker, color, amp0, amp1, hz):
    """Air molecules in a box: they wobble round their base points. With a tracker s (0..1) the dots not in `keep`
    fade out, the others spread to bases1 and wobble wider (warm air: fewer, faster molecules)."""
    dots = VGroup(*[Dot(ORIGIN, radius=0.075, color=color) for _ in bases0])
    ph = np.random.RandomState(3).uniform(0, 6.28, (len(bases0), 2))
    dots.t = 0.0

    def upd(m, dt):
        m.t += dt
        s = tracker.get_value() if tracker is not None else 0.0
        amp = amp0 + (amp1 - amp0) * s
        for k, d in enumerate(m):
            b = bases0[k]
            if k in keep:
                b = (1 - s) * bases0[k] + s * bases1[k]
            w = np.array([np.sin(hz * m.t + ph[k, 0]), np.cos(1.3 * hz * m.t + ph[k, 1]), 0.0])
            d.move_to(box.get_center() + b + amp * w)
            d.set_fill(color, opacity=1.0 if k in keep else 1.0 - s)
    dots.add_updater(upd)
    upd(dots, 0)
    return dots


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
        self.segment_3()
        self.sync(self.end(3))

        # ---------------- Segment 4: the lift equation, worked example ----------------
        self.segment_4()
        self.sync(self.end(4))

        # ---------------- Segment 5: the runway run, V1 VR V2 (3D) ----------------
        self.segment_5()
        self.sync(self.end(5))

        # ---------------- Segment 6: heat, wind and weight ----------------
        self.segment_6()
        self.sync(self.end(6))

        # ---------------- Segment 7: conclusion ----------------
        self.segment_7()
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
        # the answer starts the airflow and the roll (slowly, until the end); the wing turns blue at its word
        streaks = VGroup()
        for i, (y, z, x) in enumerate([(-2.1, 0.6, 5), (-1.2, 1.5, 7), (-0.5, 0.35, 9), (0.4, 1.7, 6),
                                       (1.1, 0.5, 8), (1.9, 1.3, 5.5), (-1.7, 1.0, 10), (2.3, 0.4, 9.5)]):
            ln = Line([x, y, z - SCENE_DROP], [x + 2.2, y, z - SCENE_DROP], color=ACCENT_1, stroke_width=3.5)
            ln.set_shade_in_3d(True)
            streaks.add(ln)
        t_go = c("الجَوَابُ") - 0.1
        t_stop = self.end(1) - 0.65
        span = t_stop - t_go
        STREAK_SHIFT, ROLL_SHIFT = 10.0, 2.0                # units over the whole span
        clock = dict(t=0.0)

        def drift(_, dt):
            dt = min(dt, max(span - clock["t"], 0.0))
            u = clock["t"] / span
            streaks.shift(LEFT * STREAK_SHIFT / span * dt)
            plane.shift(RIGHT * ROLL_SHIFT * 2 * u / span * dt)       # ease-in: speed grows with time
            clock["t"] += dt
        driver_mob = Mobject()
        driver_mob.add_updater(drift)
        self.sync(t_go)
        self.add(streaks, driver_mob)
        self.play(FadeIn(sub_grp, run_time=0.5))

        # the wing, then the speed
        self.sync(c("الجَنَاحِ") - 0.05)
        wing_from = [(m.get_fill_color(), m.get_stroke_color()) for m in plane.wings]

        def tint(wings, a):                                 # colour only: the roll keeps moving the points
            for m, (f, s) in zip(wings, wing_from):
                m.set_fill(interpolate_color(f, ManimColor(ACCENT_1), a), 0.95)
                m.set_stroke(interpolate_color(s, ManimColor(ACCENT_1), a))
        self.play(UpdateFromAlphaFunc(plane.wings, tint, run_time=0.8))
        self.sync(c("وَالسُّرْعَةِ") - 0.05)
        self.play(FadeOut(VGroup(tag_grp, leader, dot), run_time=0.4))
        self.sync(t_stop)
        driver_mob.clear_updaters()
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
        STUB = 0.2                                              # lift at the first mention: a short stub, it grows with V
        lift_tip = lambda: cg() + UP * max(lift_len(), 0.6)
        a_lift = arrow(UP, ACCENT_1, lift_len)
        a_weight = arrow(DOWN, ACCENT_4, lambda: LEN_W * gw.get_value())
        a_thrust = arrow(RIGHT, ACCENT_2, lambda: LEN_T * gt.get_value())
        a_drag = arrow(LEFT, ACCENT_4, lambda: LEN_D * gd.get_value())
        on = lambda g: (lambda: min(1.0, max(0.0, (g.get_value() - 0.6) / 0.4)))
        gl = ValueTracker(0.0)                                  # the "Lift" tag is shown with the lift arrow
        # the tag follows the arrow: full while the arrow is at least a stub, gone when the arrow is
        lift_on = lambda: min(1.0, gl.get_value(), lift_len() / (LEN_W * STUB))
        t_lift_tag = tag("Lift", ACCENT_1, lift_tip, UP, lift_on)
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
        self.play(ratio.animate.set_value(STUB), gl.animate.set_value(1.0), run_time=0.7)
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
        w_pair = a_weight.copy()                                  # static copy of the arrow: the pointer for «الكُتْلَةُ»
        self.play(Write(w1), Indicate(w_pair, color=INK, scale_factor=1.3, run_time=1.2), run_time=1.2)
        self.remove(w_pair)
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
        at_rest = fit(label("At rest: V = 0, lift ≈ 0", FS_LABEL)).move_to([0, -3.5, 0])
        self.play(FadeIn(names), FadeIn(bar_weight), FadeIn(mark), ro.animate.set_value(1.0),
                  ratio.animate.set_value(0.0), FadeIn(at_rest, shift=UP * 0.08), run_time=0.8)
        self.caption = at_rest
        self.sync(c("الدَّفْعُ", 2) - 0.1)            # 2nd: «يَكُونُ الدَّفْعُ» (the 1st is inside «وَالدَّفْعُ»)
        self.say("Thrust > Drag", y=-3.5)
        self.sync(t_acc - 0.1)
        self.say("The plane accelerates", y=-3.5)
        self.sync(c("وَكُلَّمَا") - 0.1)
        self.say("More speed, more lift", y=-3.5)
        self.sync(c("حَتَّى") - 0.1)
        self.say("Lift > Weight: the plane rises", y=-3.5)
        self.sync(t_end)
        del self.play                                           # back to the class method

    # ---------------- Segment 3 ----------------
    def segment_3(self):
        c = lambda phrase, nth=1: self.cue(3, phrase, nth)
        t0, t_end = self.start(3), self.end(3)
        P = np.array([WING_PIVOT[0], WING_PIVOT[1], 0.0])
        f0, f9, f19 = WingFlow(0.0), WingFlow(ALPHA_WORK), WingFlow(ALPHA_STALL)
        le0, te0, le9, te9 = f0.le(), f0.te(), f9.le(), f9.te()
        p3 = lambda z: np.array([z.real, z.imag, 0.0])
        alpha = ValueTracker(0.0)                       # pitch of the wing section (degrees)
        fv, cf = ValueTracker(0.0), ValueTracker(0.0)   # section visible / chord line drawn (0..1)
        adot = ValueTracker(ALPHA_WORK)                 # angle shown by the dot on the C_L curve and by the lift arrow
        lv, dv = ValueTracker(0.0), ValueTracker(0.0)   # lift arrow / downwash arrow visible (0..1)
        lab_push, lab_lift = ValueTracker(0.0), ValueTracker(0.0)   # opacity of the two lift labels
        PANEL_X = 5.3                                   # centre of the right-hand panel
        K_ARROW = 2.4                                   # arrow length (units) per unit of C_L

        # --- the wing section and its chord line follow the pitch tracker
        def build_foil():
            fl, v = WingFlow(alpha.get_value()), fv.get_value()
            body = Polygon(*_pts3(fl.outline()), color=INK, fill_color=WHITE, fill_opacity=v, stroke_width=3.5)
            body.set_stroke(opacity=v)
            chord = DashedLine(p3(fl.le()), p3(fl.te()), dash_length=0.14, color=GREY_INK, stroke_width=3)
            n = len(chord)
            for i, d in enumerate(chord):
                d.set_stroke(opacity=1.0 if (i + 1) / n <= cf.get_value() + 1e-6 else 0.0)
            return VGroup(body, chord)
        foil = always_redraw(build_foil)

        # --- lift arrow (from the quarter chord, straight up) and its two labels
        def lift_len():
            return lv.get_value() * K_ARROW * cl_curve(adot.get_value())

        def build_lift():
            L = lift_len()
            if L < 0.1:                                 # invisible stand-in (an empty VMobject leaves a dot at the origin)
                return Arrow(P, P + UP * 0.2, buff=0, color=ACCENT_1).set_opacity(0.0)
            return Arrow(P, P + UP * L, buff=0, color=ACCENT_1, stroke_width=8, tip_length=min(0.3, 0.5 * L),
                         max_tip_length_to_length_ratio=0.6, max_stroke_width_to_length_ratio=12)
        lift_arrow = always_redraw(build_lift)
        lift_lbl_push = always_redraw(lambda: label("Wing pushed up", FS_LABEL, ACCENT_1)
                                      .next_to(P + UP * max(lift_len(), 0.2), UP, buff=0.15)
                                      .set_opacity(lab_push.get_value()))
        lift_lbl = always_redraw(lambda: label("Lift", FS_LABEL, ACCENT_1, weight=BOLD)
                                 .next_to(P + UP * max(lift_len(), 0.2), UP, buff=0.15)
                                 .set_opacity(lab_lift.get_value()))

        # --- clear segment 2 (stop its drivers first) and turn its heading into this one's
        for m in self.mobjects:
            m.clear_updaters(recursive=True)
        head = label("How the wing makes lift", FS_BODY - 6, weight=BOLD).to_corner(UL, buff=0.4)
        gone = [m for m in self.mobjects if m is not self.sec]
        self.play(*[FadeOut(m) for m in gone], Transform(self.sec, head), run_time=0.6)
        self.caption = VMobject()
        self.add(foil, lift_arrow, lift_lbl_push, lift_lbl)

        # --- the section appears
        self.sync(t0 + 0.6)
        self.play(fv.animate.set_value(1.0), run_time=1.0)

        # --- leading edge, trailing edge, chord: the chord line is drawn from edge to edge while they are named
        edge_l = label("Leading edge", FS_LABEL).move_to(p3(le0) + np.array([-1.3, 0.95, 0]))
        edge_l_arrow = Arrow(edge_l.get_bottom() + DOWN * 0.08 + RIGHT * 0.5, p3(le0) + np.array([-0.08, 0.06, 0]),
                             buff=0, color=GREY_INK, stroke_width=3, tip_length=0.18)
        edge_t = label("Trailing edge", FS_LABEL).next_to(p3(te0), RIGHT, buff=0.3)
        speed = 1.0 / 3.5                                # chord fraction per second, constant
        t_le, t_te = c("حَافَّتِهِ الأَمَامِيَّةِ"), c("حَافَّتِهِ الخَلْفِيَّةِ")
        t_a = c("الخَطُّ") - 0.1
        self.sync(t_a)
        self.play(cf.animate(rate_func=linear).set_value((t_le - t_a) * speed), run_time=t_le - t_a)
        self.play(FadeIn(VGroup(edge_l, edge_l_arrow), run_time=0.4), Flash(p3(le0), color=ACCENT_1, flash_radius=0.4, line_length=0.12,
                                                      run_time=0.5),
                  cf.animate(rate_func=linear).set_value((t_te - t_a) * speed), run_time=t_te - t_le)
        self.play(FadeIn(edge_t, run_time=0.4), Flash(p3(te0), color=ACCENT_1, flash_radius=0.4, line_length=0.12,
                                                      run_time=0.5),
                  cf.animate(rate_func=linear).set_value(1.0), run_time=0.6)
        dim_y = le0.imag - 1.0
        dim = DoubleArrow([le0.real, dim_y, 0], [te0.real, dim_y, 0], buff=0, color=GREY_INK, stroke_width=3,
                          tip_length=0.18)
        ext = VGroup(*[Line([z.real, z.imag - 0.55, 0], [z.real, dim_y - 0.15, 0], color=GREY_INK, stroke_width=2)
                       for z in (le0, te0)])
        chord_lbl = label("Chord", FS_LABEL).next_to(dim, DOWN, buff=0.2)
        self.sync(c("هُوَ الوَتَرُ") - 0.1)
        self.play(FadeIn(ext), GrowFromCenter(dim), FadeIn(chord_lbl), run_time=0.7)

        # --- angle of attack: the section pitches nose-up against the wind direction
        ref = DashedLine(p3(le9) + LEFT * 2.4, p3(le9), dash_length=0.14, color=GREY_INK, stroke_width=3)
        chord_ext = DashedLine(p3(le9), p3(le9) + 2.4 * np.array([-np.cos(f9.al), np.sin(f9.al), 0]),
                               dash_length=0.14, color=GREY_INK, stroke_width=3)
        arc = Arc(radius=2.0, start_angle=PI - f9.al, angle=f9.al, arc_center=p3(le9), color=INK, stroke_width=4)
        a_sym = label("α", FS_TITLE // 2 + 4, INK, weight=BOLD).next_to(       # above the wedge, at the arc's open end
            p3(le9) + 2.15 * np.array([-np.cos(f9.al), np.sin(f9.al), 0]), UP, buff=0.12)
        a_name = label("Angle of\nattack", FS_LABEL).next_to(ref, DOWN, buff=0.3).align_to(ref, LEFT)
        self.sync(c("وَزَاوِيَةُ") - 0.1)
        self.play(FadeOut(VGroup(edge_l, edge_l_arrow, edge_t, dim, ext, chord_lbl)), alpha.animate.set_value(ALPHA_WORK),
                  run_time=1.2, rate_func=smooth)
        self.sync(c("الزَّاوِيَةُ بَيْنَ") - 0.1)
        self.play(Create(ref), Create(chord_ext), run_time=0.4)
        self.play(Create(arc), FadeIn(a_sym), FadeIn(a_name), run_time=0.5)
        self.sync(c("الوَتَرِ") - 0.05)
        hi = Line(p3(le9), p3(te9), color=INK, stroke_width=7)
        self.play(Create(hi, run_time=0.25))
        self.play(FadeOut(hi, run_time=0.25))

        # --- the relative wind arrives
        div = f9.divider()
        wind_y = [div - 1.0, div - 0.5, div + 1.75]
        wind = VGroup(*[Arrow([-6.75, y, 0], [-5.7, y, 0], buff=0, color=ACCENT_1, stroke_width=5, tip_length=0.24)
                        for y in wind_y])
        wind_lbl = label("Relative wind", FS_LABEL, ACCENT_1).next_to(wind[2], UP, buff=0.2).align_to(wind[2], LEFT)
        self.sync(c("وَاتِّجَاهِ") - 0.1)
        self.play(LaggedStart(*[GrowArrow(a) for a in wind], lag_ratio=0.2), ref.animate.set_color(ACCENT_1),
                  run_time=0.5)
        self.sync(c("الهَوَاءِ النِّسْبِيِّ") - 0.1)
        self.play(FadeIn(wind_lbl, run_time=0.5))

        # --- the flow: streamlines and moving air parcels
        seeds = [div + d for d in (-1.0, -0.5, -0.25, -0.1, 0.12, 0.35, 0.65, 1.05, 1.75)]
        paths = []
        for y in seeds:
            st = f9.stream(y)
            paths.append(st[np.argmax(st.real >= FLOW_X0):])
        lines = VGroup(*[_polyline(pth, ACCENT_1, 3) for pth in paths])
        fvv = ValueTracker(0.0)
        parcels = VGroup(*[Dot(radius=0.07, color=ACCENT_1).set_opacity(0.0) for _ in paths for _ in range(4)])
        for i, d in enumerate(parcels):
            d.path, d.phase = paths[i // 4], (i % 4) / 4 + 0.06 * (i // 4)
        parcels.clock = 0.0

        def move_parcels(m, dt):
            m.clock += dt
            for d in m:
                n = len(d.path)
                idx = (d.phase * n + m.clock * 1.7 / 0.05) % (n - 1)
                i, fr = int(idx), idx - int(idx)
                q = d.path[i] * (1 - fr) + d.path[i + 1] * fr
                d.move_to([q.real, q.imag, 0])
                d.set_opacity(fvv.get_value() * min(1.0, idx / (n - 1) / 0.05, (1 - idx / (n - 1)) / 0.05))
        parcels.add_updater(move_parcels)
        self.sync(c("الجَنَاحُ يَحْرِفُ") - 0.1)
        self.add(parcels)
        self.play(FadeOut(wind_lbl, run_time=0.3), FadeOut(VGroup(a_name, a_sym, arc, ref, chord_ext), run_time=0.3),
                  LaggedStart(*[Create(l) for l in lines], lag_ratio=0.1, run_time=1.4),
                  fvv.animate(run_time=1.4).set_value(1.0))

        # --- Newton: the wing pushes the air down, the air pushes the wing up
        x_dw = te9.real + 1.15
        down_len = K_ARROW * cl_curve(ALPHA_WORK)
        down_arrow = always_redraw(lambda: Arrow([x_dw, te9.imag + 0.1, 0],
                                                 [x_dw, te9.imag + 0.1 - max(down_len * dv.get_value(), 0.02), 0],
                                                 buff=0, color=ACCENT_1, stroke_width=8, tip_length=0.3,
                                                 max_tip_length_to_length_ratio=0.6, max_stroke_width_to_length_ratio=12)
                                   if dv.get_value() > 0.06 else
                                   Arrow([x_dw, te9.imag, 0], [x_dw, te9.imag - 0.2, 0], buff=0).set_opacity(0.0))
        down_lbl = label("Air pushed down", FS_LABEL, ACCENT_1).move_to([x_dw + 0.3, te9.imag + 0.1 - down_len - 0.45, 0])
        down_lbl.set_opacity(0.0)
        self.add(down_arrow)
        self.sync(c("الأَسْفَلِ") - 0.1)
        self.play(dv.animate.set_value(1.0), lines.animate.set_stroke(opacity=0.35), down_lbl.animate.set_opacity(1.0),
                  run_time=0.7)
        self.sync(c("فَيَدْفَعُهُ") - 0.1)
        self.play(lv.animate.set_value(1.0), lab_push.animate.set_value(1.0), run_time=0.8)

        def panel_tag(line1, line2, color, y):
            """A boxed two-line tag in the right-hand panel (x from 3.75 to 6.85)."""
            txt = fit(VGroup(label(line1, FS_AXIS, INK, weight=BOLD), label(line2, FS_AXIS, GREY_INK))
                      .arrange(DOWN, buff=0.1), 2.7)
            box = SurroundingRectangle(txt, buff=0.2, color=color, corner_radius=0.1, stroke_width=3)
            return VGroup(box, txt).move_to([PANEL_X, y, 0])
        newton = panel_tag("Newton's third law", "action = reaction", ACCENT_1, 2.35)
        self.sync(c("قَانُونُ") - 0.1)
        self.play(FadeIn(newton, shift=LEFT * 0.2), run_time=0.6)

        # --- Bernoulli: lower pressure above, higher pressure below
        marks_up_x, marks_lo_x = [-2.2, -1.5, -0.8, -0.1], [-3.6, -2.6, -1.6, -0.6]
        out9 = f9.outline()

        def surface(x, top):
            near = out9[abs(out9.real - x) < 0.06]
            return near.imag.max() if top else near.imag.min()
        m_up = VGroup(*[_minus(ACCENT_1).move_to([x, surface(x, True) + 0.42, 0]) for x in marks_up_x])
        m_lo = VGroup(*[_plus(INK).move_to([x, surface(x, False) - 0.42, 0]) for x in marks_lo_x])
        lo_lbl = label("Low pressure", FS_LABEL, ACCENT_1).next_to(m_up, UP, buff=0.25)
        hi_lbl = label("High pressure", FS_LABEL, INK).next_to(m_lo, DOWN, buff=0.25)
        bern = panel_tag("Bernoulli", "low pressure above", ACCENT_1, 0.6)
        self.sync(c("وَفِي الوَقْتِ") - 0.1)
        self.play(FadeOut(parcels, run_time=0.4), FadeOut(lines, run_time=0.4), FadeOut(wind, run_time=0.4),
                  dv.animate(run_time=0.4).set_value(0.0),
                  FadeOut(down_lbl, run_time=0.4), lv.animate(run_time=0.4).set_value(0.0),
                  lab_push.animate(run_time=0.4).set_value(0.0), run_time=0.5)
        parcels.clear_updaters()
        self.remove(parcels, lines)
        self.sync(c("فَوْقَ الجَنَاحِ") - 0.1)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in m_up], lag_ratio=0.15), FadeIn(lo_lbl), run_time=0.8)
        self.sync(c("تَحْتَهُ") - 0.5)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in m_lo], lag_ratio=0.15), FadeIn(hi_lbl), run_time=0.8)
        self.sync(c("مَبْدَأُ") - 0.1)
        self.play(FadeIn(bern, shift=LEFT * 0.2), run_time=0.6)

        # --- the two views are one phenomenon: the same lift
        eq = label("=", FS_TITLE // 2, INK, weight=BOLD)
        same = label("same lift", FS_AXIS, ACCENT_1)
        VGroup(eq, same).arrange(RIGHT, buff=0.25).move_to([PANEL_X, 1.48, 0])
        self.sync(c("وَالتَّفْسِيرَانِ") - 0.1)
        self.play(FadeIn(eq, scale=1.4), run_time=0.5)
        self.sync(c("لِلظَّاهِرَةِ") - 0.1)
        self.play(FadeOut(VGroup(m_up, m_lo, lo_lbl, hi_lbl), run_time=0.5), lv.animate.set_value(1.0),
                  lab_lift.animate.set_value(1.0), FadeIn(same), run_time=0.8)

        # --- angle of attack, lift and the stall
        ox, oy, sx, sy = 4.25, -2.3, 0.1, 2.7                   # origin of the chart and its scales (per degree, per C_L)
        cpt = lambda a: np.array([ox + sx * a, oy + sy * cl_curve(a), 0.0])
        ax_x = Arrow([ox, oy, 0], [6.75, oy, 0], buff=0, color=INK, stroke_width=3, tip_length=0.2)
        ax_y = Arrow([ox, oy, 0], [ox, oy + 3.0, 0], buff=0, color=INK, stroke_width=3, tip_length=0.2)
        x_lbl = fit(label("Angle of attack α", FS_AXIS), 2.9).next_to(ax_x, DOWN, buff=0.2).align_to(ax_x, RIGHT)
        y_lbl = VGroup(label("Lift coefficient C", FS_AXIS), label("L", FS_AXIS)).arrange(RIGHT, buff=0.02,
                                                                                        aligned_edge=DOWN)
        y_lbl[1].shift(DOWN * 0.07)
        y_lbl.rotate(PI / 2).next_to(ax_y, LEFT, buff=0.12).align_to(ax_y, DOWN).shift(UP * 0.1)
        curve = _polyline([complex(*cpt(a)[:2]) for a in np.linspace(0, 24, 90)], ACCENT_1, 5)
        dot = always_redraw(lambda: Dot(cpt(adot.get_value()), radius=0.1, color=ACCENT_4, stroke_width=0))
        chart = VGroup(ax_x, ax_y, x_lbl, y_lbl)
        self.sync(c("زِيَادَةُ") - 0.5)
        self.play(FadeOut(VGroup(newton, bern, eq, same), run_time=0.5), FadeIn(chart), run_time=0.6)
        self.play(Create(curve, run_time=0.9, rate_func=linear))
        self.add(dot)
        # pitch up step by step: the wing rotates, the dot climbs the curve, the arrow grows
        self.sync(c("زِيَادَةُ") + 0.9)
        self.play(alpha.animate.set_value(12.0), adot.animate.set_value(12.0), run_time=1.6, rate_func=smooth)
        self.sync(c("حَتَّى") - 0.1)
        crit_lbl = label("Critical angle", FS_LABEL, INK).next_to(cpt(ALPHA_CRIT), UP, buff=0.55).shift(LEFT * 0.3)
        crit_line = DashedLine(crit_lbl.get_bottom() + DOWN * 0.06 + RIGHT * 0.3, cpt(ALPHA_CRIT) + UP * 0.15,
                               dash_length=0.1, color=GREY_INK, stroke_width=3)
        t_crit = c("زَاوِيَةٍ حَرِجَةٍ") - 0.4          # the fade starts ~0.3 s late (first frame of the play)
        self.play(alpha.animate.set_value(ALPHA_CRIT), adot.animate.set_value(ALPHA_CRIT), run_time=1.6,
                  rate_func=smooth,
                  *[Succession(Wait(t_crit - self.renderer.time), FadeIn(crit_lbl, run_time=0.4))],
                  *[Succession(Wait(t_crit - self.renderer.time), Create(crit_line, run_time=0.4))])

        # --- past it the flow separates: red eddies over the upper surface
        seeds19 = [f19.divider() + d for d in (-1.0, -0.5, -0.25, -0.1, 0.12, 0.35, 0.65, 1.05, 1.75)]
        sep_x = f19.le().real + 0.38 * (f19.te().real - f19.le().real)
        att, low, eddy_src = VGroup(), VGroup(), []
        for y in seeds19:
            st = f19.stream(y)
            st = st[np.argmax(st.real >= FLOW_X0):]
            over = st[np.argmin(abs(st.real - f19.le().real))].imag > f19.le().imag
            if over and y > seeds19[3]:
                j = np.argmax(st.real >= sep_x)
                att.add(_polyline(st[:j + 1], ACCENT_1, 3))
                eddy_src.append(st[j])
            else:
                low.add(_polyline(st, ACCENT_1, 3))
        eph = ValueTracker(0.0)
        eph.add_updater(lambda m, dt: m.increment_value(2.2 * dt))

        def build_eddies():
            out = VGroup()
            for k, q in enumerate(eddy_src):
                tau = np.linspace(0, (FLOW_X1 - q.real) / 1.1, 80)
                r = np.minimum(0.05 + 0.13 * tau, 0.36)
                th = 3.4 * tau - eph.get_value() + 1.7 * k
                x = q.real + 1.1 * tau + r * np.sin(th) - r[0] * np.sin(th[0])
                y = q.imag + 0.12 * tau * (1 + 0.3 * k) + r * (np.cos(th) - np.cos(th[0]))
                out.add(_polyline([complex(a, b) for a, b in zip(x, y)], ACCENT_4, 3))
            return out
        eddies = always_redraw(build_eddies)
        sep_lbl = label("Air separates", FS_LABEL, ACCENT_4)
        sep_lbl.next_to(build_eddies(), UP, buff=0.3)
        stall_flow = VGroup(att, low)
        self.sync(c("يَنْفَصِلُ") - 0.3)
        self.add(eph)
        self.play(alpha.animate(run_time=0.9, rate_func=smooth).set_value(ALPHA_STALL),
                  Succession(Wait(0.6), AnimationGroup(FadeIn(stall_flow, run_time=0.6), FadeIn(eddies, run_time=0.6),
                                                       FadeIn(sep_lbl, run_time=0.6))))

        # --- lift drops quickly: the arrow shrinks (it does not vanish), the dot falls along the curve
        self.sync(c("فَيَنْخَفِضُ") - 0.1)
        self.play(adot.animate.set_value(ALPHA_STALL), run_time=1.3, rate_func=smooth)
        stall_lbl = label("Stall", FS_LABEL + 2, ACCENT_4, weight=BOLD).move_to(cpt(21.0) + np.array([-0.35, -0.6, 0]))
        self.sync(c("الانْهِيَارُ") - 0.1)
        self.play(FadeIn(stall_lbl, scale=1.3), run_time=0.5)

        # --- back to a normal angle; the myth of equal transit times
        self.sync(c("وَأَخِيرًا") - 0.7)
        self.play(FadeOut(VGroup(stall_flow, eddies, sep_lbl, chart, curve, crit_lbl, crit_line, stall_lbl), run_time=0.6),
                  FadeOut(dot, run_time=0.6), alpha.animate.set_value(ALPHA_WORK), lv.animate.set_value(0.0),
                  lab_lift.animate.set_value(0.0), run_time=1.0, rate_func=smooth)
        eph.clear_updaters()

        up = f9.stream(div + 0.03, dt=0.03, x1=te9.real + 0.06)
        lo = f9.stream(div - 0.03, dt=0.03, x1=te9.real + 0.06)
        start_x, finish_x = le9.real - 1.0, te9.real + 0.05
        up, lo = [q[np.argmax(q.real >= start_x):] for q in (up, lo)]
        up, lo = [q[:np.argmax(q.real >= finish_x) + 1] for q in (up, lo)]
        rate = len(up) / 1.5                                     # path steps per second: the upper parcel takes 1.5 s
        pr = ValueTracker(0.0)
        parcel_up = Dot(p3(up[0]), radius=0.1, color=ACCENT_1, stroke_width=0)
        parcel_lo = Dot(p3(lo[0]), radius=0.1, color=INK, stroke_width=0)

        def at(path, sec):
            i = min(sec * rate, len(path) - 1.0)
            k, fr = int(i), i - int(i)
            q = path[k] if k >= len(path) - 1 else path[k] * (1 - fr) + path[k + 1] * fr
            return p3(q)
        parcel_up.add_updater(lambda m: m.move_to(at(up, pr.get_value())))
        parcel_lo.add_updater(lambda m: m.move_to(at(lo, pr.get_value())))
        trail_up = TracedPath(parcel_up.get_center, stroke_color=ACCENT_1, stroke_width=4)
        trail_lo = TracedPath(parcel_lo.get_center, stroke_color=INK, stroke_width=4)
        y_mid = (up[0].imag + lo[0].imag) / 2
        start_line = DashedLine([start_x, y_mid - 0.8, 0], [start_x, y_mid + 0.8, 0], dash_length=0.12,
                                color=GREY_INK, stroke_width=3)
        finish_line = DashedLine([finish_x, y_mid - 1.0, 0], [finish_x, y_mid + 1.3, 0], dash_length=0.12,
                                 color=GREY_INK, stroke_width=3)
        start_lbl = label("Start", FS_NOTE, GREY_INK).next_to(start_line, DOWN, buff=0.15)
        finish_lbl = label("Finish", FS_NOTE, GREY_INK).next_to(finish_line, DOWN, buff=0.15)
        myth = fit(VGroup(label("Myth:", FS_AXIS, ACCENT_4, weight=BOLD),
                          label("equal transit time", FS_AXIS, ACCENT_4)).arrange(DOWN, buff=0.1), 2.7)
        box_m = SurroundingRectangle(myth, buff=0.2, color=ACCENT_4, corner_radius=0.1, stroke_width=3)
        myth_grp = VGroup(box_m, myth).move_to([PANEL_X, 1.5, 0])
        no = VGroup(icon("x", ACCENT_4, 0.7), label("Not true", FS_LABEL, ACCENT_4, weight=BOLD)).arrange(RIGHT, buff=0.2)
        no.next_to(myth_grp, DOWN, buff=0.35)
        self.sync(c("خُرَافَةٌ") - 0.1)
        self.play(FadeIn(myth_grp, shift=LEFT * 0.2), run_time=0.6)
        self.sync(c("الهَوَاءَ فَوْقَ الجَنَاحِ") - 0.1)
        self.play(FadeIn(start_line), FadeIn(start_lbl), FadeIn(parcel_up), FadeIn(parcel_lo), run_time=0.6)
        self.sync(c("الحَافَّةِ الخَلْفِيَّةِ") - 0.1)
        self.play(FadeIn(finish_line), FadeIn(finish_lbl), run_time=0.5)
        self.sync(c("هٰذَا غَيْرُ") - 0.1)
        self.play(FadeIn(no, scale=1.3), myth.animate.set_opacity(0.45), box_m.animate.set_stroke(opacity=0.45),
                  run_time=0.5)
        self.add(trail_up, trail_lo)
        first = label("Upper air arrives first", FS_LABEL, ACCENT_1)
        first.next_to(finish_line.get_top(), UP, buff=0.2)
        t_run = c("الهَوَاءُ فَوْقَ") - 0.15
        self.sync(t_run)
        self.play(pr.animate(rate_func=linear).set_value(len(lo) / rate), run_time=len(lo) / rate,
                  *[Succession(Wait(max(c("أَبْكَرَ") - 0.1 - t_run, 0.0)), FadeIn(first, run_time=0.4))])
        self.sync(t_end)
        for m in self.mobjects:                                 # leave nothing running for the next segment
            m.clear_updaters(recursive=True)

    # ---------------- Segment 4 ----------------
    def segment_4(self):
        c = lambda phrase, nth=1: self.cue(4, phrase, nth)
        T = lambda phrase, dt=0.1, nth=1: c(phrase, nth) - dt
        t_end = self.end(4)
        p3 = lambda z: np.array([z.real, z.imag, 0.0])

        # --- the heading of segment 3 becomes this one's; everything else leaves
        head = label("The lift equation", FS_BODY - 6, weight=BOLD).to_corner(UL, buff=0.4)
        gone = [m for m in self.mobjects if m is not self.sec]
        self.play(*[FadeOut(m) for m in gone], Transform(self.sec, head), run_time=0.6)
        self.caption = VMobject()

        # --- the equation L = 1/2 rho V^2 S C_L, one factor at a time, each with its name
        E = 46
        parts = VGroup(label("L", E, ACCENT_1, weight=BOLD), label("=", E), label("½", E), label("ρ", E),
                       label("V²", E), label("S", E), _cl_label(E)).arrange(RIGHT, buff=1.0)
        parts.move_to([-0.4, 2.5, 0])
        names = {3: _stack("air", "density"), 4: _stack("speed", "squared"), 5: _stack("wing", "area"),
                 6: _stack("lift", "coefficient")}
        for k, n in names.items():
            n.next_to(parts, DOWN, buff=0.3).set_x(parts[k].get_center()[0])
        self.sync(T("الرَّفْعُ"))
        self.play(FadeIn(parts[0], shift=DOWN * 0.15), FadeIn(parts[1], shift=DOWN * 0.15), run_time=0.5)
        for k, when in [(2, T("نِصْفَ", 0.05)), (3, T("كَثَافَةِ", 0.05)), (4, T("مُرَبَّعِ", 0.05)),
                        (5, T("مِسَاحَةِ", 0.05)), (6, T("مُعَامِلِ", 0.05))]:
            self.sync(when)
            anims = [FadeIn(parts[k], shift=DOWN * 0.15)]
            if k in names:
                anims.append(FadeIn(names[k], shift=DOWN * 0.1))
            self.play(*anims, run_time=0.4)

        # ================= phase A: angle of attack and flaps raise C_L =================
        FX, FY = -2.6, -1.5                                 # centre of the chord of the drawn section
        f0 = WingFlow(0.0)
        chord = 4.2
        k = chord / abs(f0.te() - f0.le())
        mid = (f0.le() + f0.te()) / 2
        place = lambda z: (np.asarray(z) - mid) * k + complex(FX, FY)
        pts = place(f0.outline())
        pts = pts.real + 1j * (FY + 1.9 * (pts.imag - FY))      # drawn thicker than the computed profile, for legibility
        pts = np.roll(pts, -int(np.argmax(abs(pts - place(f0.te())))))       # start at the leading edge
        le_z, te_z = place(f0.le()), place(f0.te())
        xc = le_z.real + 0.68 * chord                         # the flap is the last 32 % of the chord (schematic)
        idx = np.where(pts.real >= xc)[0]
        assert np.all(np.diff(idx) == 1)
        flap_c = pts[idx[0]: idx[-1] + 1]
        main_c = np.concatenate([pts[idx[-1] + 1:], pts[:idx[0]]])
        main = Polygon(*_pts3(main_c), color=INK, fill_color=WHITE, fill_opacity=1, stroke_width=3.5)
        flap = Polygon(*_pts3(flap_c), color=ACCENT_2, fill_color=WHITE, fill_opacity=1, stroke_width=3.5)
        hinge = Dot(p3(pts[idx[-1]]) + UP * 0.03, radius=0.06, color=ACCENT_2)
        foil = VGroup(main, flap, hinge)
        pivot_z = le_z + 0.25 * (te_z - le_z)                 # quarter chord: the wing pitches about it
        pivot = p3(pivot_z)

        LIFT_OFF = 0.55                                       # the arrow starts inside the wing and clears its top
        cl, clsp, lv = ValueTracker(CL_ZERO_S), ValueTracker(CL_ZERO_S), ValueTracker(0.0)

        def build_arrow():
            L = cl.get_value()
            a = Arrow(pivot, pivot + UP * (L + LIFT_OFF), buff=0, color=ACCENT_1, stroke_width=8, tip_length=0.3,
                      max_tip_length_to_length_ratio=0.6, max_stroke_width_to_length_ratio=12)
            return a.set_opacity(lv.get_value())
        lift_arrow = always_redraw(build_arrow)
        lift_lbl = always_redraw(lambda: label("Lift", FS_LABEL, ACCENT_1, weight=BOLD)
                                 .next_to(pivot + UP * (cl.get_value() + LIFT_OFF), RIGHT, buff=0.15).set_opacity(lv.get_value()))

        BAR_H, BAR_MAX, SPEED_W = 0.32, 3.2, 2.4
        n_cl = _cl_label(FS_LABEL)
        n_sp = label("Speed needed", FS_LABEL)
        bnames = VGroup(n_cl, n_sp).arrange(DOWN, aligned_edge=RIGHT, buff=0.9).move_to([1.5, -1.4, 0])
        bx = bnames.get_right()[0] + 0.3
        bv = ValueTracker(0.0)
        bar_cl = always_redraw(lambda: Rectangle(width=max(BAR_MAX * cl.get_value() / D.CL_TAKEOFF, 0.02), height=BAR_H,
                                                 color=ACCENT_1, fill_color=ACCENT_1, fill_opacity=bv.get_value(),
                                                 stroke_width=0).move_to([bx, n_cl.get_center()[1], 0], LEFT)
                               .set_stroke(opacity=0))
        bar_sp = always_redraw(lambda: Rectangle(width=SPEED_W * np.sqrt(CL_CLEAN_S / clsp.get_value()), height=BAR_H,
                                                 color=GREY_INK, fill_color=GREY_INK, fill_opacity=bv.get_value(),
                                                 stroke_width=0).move_to([bx, n_sp.get_center()[1], 0], LEFT)
                               .set_stroke(opacity=0))

        # the section arrives with the sentence about the lift coefficient
        self.sync(T("وَمُعَامِلُ الرَّفْعِ"))
        self.add(lift_arrow, lift_lbl)
        self.play(FadeIn(foil, shift=UP * 0.2), lv.animate.set_value(1.0), run_time=0.6)
        self.play(Indicate(parts[6], color=ACCENT_1, scale_factor=1.25), run_time=0.6)
        self.sync(T("يَعْتَمِدُ"))
        self.add(bar_cl, bar_sp)
        self.play(FadeIn(bnames), bv.animate.set_value(1.0), run_time=0.5)

        # angle of attack: the section pitches nose-up, the arrow and the bar grow, the needed speed falls
        alpha = np.radians(ALPHA_WORK)
        le_after = p3(pivot_z + np.exp(-1j * alpha) * (le_z - pivot_z))
        ref = DashedLine(le_after + LEFT * 1.5, le_after, dash_length=0.14, color=GREY_INK, stroke_width=3)
        chord_ext = DashedLine(le_after, le_after + 1.5 * np.array([-np.cos(alpha), np.sin(alpha), 0]), dash_length=0.14,
                               color=GREY_INK, stroke_width=3)
        arc = Arc(radius=1.3, start_angle=PI - alpha, angle=alpha, arc_center=le_after, color=INK, stroke_width=4)
        a_sym = label("α", FS_LABEL + 4, INK, weight=BOLD).move_to(
            le_after + 1.75 * np.array([-np.cos(alpha / 2), np.sin(alpha / 2), 0]))
        self.sync(T("زَاوِيَةِ", 0.05))
        self.play(foil.animate.rotate(-alpha, about_point=pivot), cl.animate.set_value(CL_CLEAN_S),
                  clsp.animate.set_value(CL_CLEAN_S), run_time=0.8, rate_func=smooth)
        self.play(Create(ref), Create(chord_ext), Create(arc), FadeIn(a_sym), run_time=0.4)

        # flaps: the trailing edge drops, C_L grows, then the speed needed falls
        FLAP_DEG = 22
        flap_end = flap.copy().rotate(-np.radians(FLAP_DEG), about_point=hinge.get_center())
        flap_lbl = label("Flap", FS_LABEL, ACCENT_2).next_to(flap_end, DOWN, buff=0.25)
        self.sync(T("القَلَّابَاتِ", 0.1))
        self.play(FadeIn(flap_lbl, shift=UP * 0.1), Indicate(flap, color=ACCENT_2, scale_factor=1.15), run_time=0.7)
        self.sync(T("وَالقَلَّابَاتُ", 0.05))
        self.play(Rotate(flap, -np.radians(FLAP_DEG), about_point=hinge.get_center()),
                  cl.animate.set_value(D.CL_TAKEOFF), run_time=1.1, rate_func=smooth)
        self.sync(T("فَتُقْلِعُ", 0.05))
        self.play(clsp.animate.set_value(D.CL_TAKEOFF), run_time=1.2, rate_func=smooth)

        # ================= phase B: double the speed, four times the lift =================
        CELL = 1.15
        cell = lambda: Square(CELL, color=ACCENT_1, fill_color=ACCENT_1, fill_opacity=0.3, stroke_width=3)
        sq1 = cell()
        cells2 = VGroup(*[cell() for _ in range(4)]).arrange_in_grid(2, 2, buff=0)
        VGroup(sq1, cells2).arrange(RIGHT, buff=3.4, aligned_edge=DOWN).move_to([0, -1.3, 0])
        outline2 = Square(2 * CELL, color=ACCENT_1, stroke_width=3).move_to(cells2)
        dim1 = DoubleArrow(sq1.get_corner(DL) + DOWN * 0.3, sq1.get_corner(DR) + DOWN * 0.3, buff=0, color=INK,
                           stroke_width=3, tip_length=0.15)
        dim2 = DoubleArrow(cells2.get_corner(DL) + DOWN * 0.3, cells2.get_corner(DR) + DOWN * 0.3, buff=0, color=INK,
                           stroke_width=3, tip_length=0.15)
        v1 = label("V", FS_LABEL).next_to(dim1, DOWN, buff=0.15)
        v2 = label("2V", FS_LABEL).next_to(dim2, DOWN, buff=0.15)
        l1 = label("lift L", FS_LABEL, ACCENT_1).next_to(sq1, UP, buff=0.25)
        l2 = label(f"lift {D.LIFT_RATIO_DOUBLE_SPEED:.0f} L", FS_LABEL, ACCENT_1, weight=BOLD).next_to(cells2, UP, buff=0.25)
        arr = Arrow(sq1.get_right() + RIGHT * 0.35, [cells2.get_left()[0] - 0.35, sq1.get_center()[1], 0], buff=0, color=INK, stroke_width=4,
                    tip_length=0.22)
        x4 = label(f"× {D.LIFT_RATIO_DOUBLE_SPEED:.0f}", FS_TITLE // 2 + 4, ACCENT_1, weight=BOLD).next_to(arr, UP, buff=0.15)
        self.sync(T("وَلِأَنَّ", 0.1))
        self.play(FadeOut(VGroup(foil, bnames, ref, chord_ext, arc, a_sym, flap_lbl)), lv.animate.set_value(0.0),
                  bv.animate.set_value(0.0), run_time=0.5)
        self.remove(lift_arrow, lift_lbl, bar_cl, bar_sp)
        self.sync(T("السُّرْعَةَ", 0.1))
        self.play(FadeIn(sq1, scale=0.8), GrowFromCenter(dim1), FadeIn(v1), FadeIn(l1), run_time=0.6)
        self.sync(T("مُرَبَّعَةٌ", 0.05))
        self.play(Indicate(parts[4], color=ACCENT_1, scale_factor=1.25), run_time=0.6)
        self.sync(T("فَضِعْفُ", 0.05))
        self.play(FadeIn(outline2), GrowFromCenter(dim2), FadeIn(v2), run_time=0.6)
        self.sync(T("أَرْبَعَةَ", 0.05))
        self.play(LaggedStart(*[FadeIn(q) for q in cells2], lag_ratio=0.3), run_time=0.6)
        self.sync(T("أَضْعَافِ", 0.02))
        self.play(FadeIn(l2, shift=UP * 0.1), GrowArrow(arr), FadeIn(x4, scale=1.3), run_time=0.5)

        # ================= phase C: the worked example, L = W =================
        w_grp = VGroup(label("=", E), label("W", E, ACCENT_4, weight=BOLD)).arrange(RIGHT, buff=0.3)
        w_grp.next_to(parts, RIGHT, buff=0.45)
        # the formula solved for V, then the same with the numbers (both centred)
        SZ = 34
        rho_s, S_s, cl_s = label("ρ", SZ), label("S", SZ), _cl_label(SZ)
        den_f = VGroup(rho_s, S_s, cl_s).arrange(RIGHT, buff=0.3)
        num_f = VGroup(label("2", SZ), label("W", SZ, ACCENT_4, weight=BOLD)).arrange(RIGHT, buff=0.1)
        form = VGroup(label("V =", SZ), _sqrt_frac(num_f, den_f)).arrange(RIGHT, buff=0.3)
        form.next_to(parts, DOWN, buff=0.55).set_x(0)

        n1 = label(f"2 × {D.WEIGHT:,.0f} N", SZ, ACCENT_4)
        d1, dx1, d2, dx2, d3 = (label(f"{D.RHO_15:.3f}", SZ), label("×", SZ), label(f"{D.WING_AREA:.0f}", SZ),
                                label("×", SZ), label(f"{D.CL_TAKEOFF}", SZ))
        den_v = VGroup(d1, dx1, d2, dx2, d3).arrange(RIGHT, buff=0.25)
        sub = VGroup(label("V =", SZ), _sqrt_frac(n1, den_v)).arrange(RIGHT, buff=0.3)
        sub.next_to(form, DOWN, buff=0.45).set_x(0)
        u1 = label("kg/m³", FS_TAG, GREY_INK).next_to(d1, DOWN, buff=0.15)
        u2 = label("m²", FS_TAG, GREY_INK).next_to(d2, DOWN, buff=0.15)
        r1 = label(f"V = {D.V_15:.1f} m/s", FS_LABEL + 12, ACCENT_1, weight=BOLD)
        r2 = label(f"≈ {D.V_15_KMH:.0f} km/h", FS_LABEL + 12, ACCENT_1, weight=BOLD)
        res = VGroup(r1, r2).arrange(RIGHT, buff=0.4)
        res.next_to(sub, DOWN, buff=0.75).set_x(0)
        box1 = SurroundingRectangle(r1, buff=0.18, color=ACCENT_1, corner_radius=0.1, stroke_width=4)
        box2 = SurroundingRectangle(res, buff=0.18, color=ACCENT_1, corner_radius=0.1, stroke_width=4)

        self.sync(T("مِثَالٌ", 0.1))
        self.play(FadeOut(VGroup(sq1, cells2, outline2, dim1, dim2, v1, v2, l1, l2, arr, x4, *names.values())),
                  Transform(self.sec, label("Worked example", FS_BODY - 6, weight=BOLD).to_corner(UL, buff=0.4)),
                  run_time=0.6)
        self.sync(T("الرَّفْعَ مُسَاوِيًا", 0.05))
        self.play(Indicate(parts[0], color=ACCENT_1, scale_factor=1.3), run_time=0.6)
        self.sync(T("لِلْوَزْنِ", 0.05))
        self.play(FadeIn(w_grp, shift=LEFT * 0.15), run_time=0.5)
        self.sync(T("الكَثَافَةُ", 0.9))
        self.play(FadeIn(form, shift=DOWN * 0.15), run_time=0.8)
        self.sync(T("الكَثَافَةُ", 0.1))
        self.play(FadeIn(sub[0]), FadeIn(sub[1].rad), FadeIn(sub[1].bar), FadeIn(n1), run_time=0.6)
        self.sync(T("وَاحِدٌ", 0.05))
        self.play(FadeIn(d1, shift=DOWN * 0.1), FadeIn(u1), run_time=0.5)
        self.play(Indicate(rho_s, color=ACCENT_1, scale_factor=1.4), run_time=0.5)
        self.sync(T("وَالمِسَاحَةُ", 0.05))
        self.play(FadeIn(VGroup(dx1, d2), shift=DOWN * 0.1), FadeIn(u2), run_time=0.5)
        self.play(Indicate(S_s, color=ACCENT_1, scale_factor=1.4), run_time=0.5)
        self.sync(T("وَمُعَامِلُ الرَّفْعِ بِالقَلَّابَاتِ", 0.05))
        self.play(FadeIn(VGroup(dx2, d3), shift=DOWN * 0.1), run_time=0.5)
        self.play(Indicate(cl_s, color=ACCENT_1, scale_factor=1.4), run_time=0.5)
        self.sync(T("فَالسُّرْعَةُ", 0.05))
        self.play(Indicate(form[0], color=ACCENT_1, scale_factor=1.25), run_time=0.6)
        self.sync(T("سِتَّةٌ", 0.05))
        self.play(FadeIn(r1, shift=DOWN * 0.1), Create(box1), run_time=0.7)
        self.sync(T("أَيْ نَحْوُ", 0.05))
        self.play(FadeIn(r2, shift=DOWN * 0.1), Transform(box1, box2), run_time=0.7)
        self.sync(t_end)

    # ---------------- Segment 5 ----------------
    def segment_5(self):
        """The runway run (3D): the plane stays at the origin, the ground runs (and later sinks) under it."""
        c = lambda phrase, nth=1: self.cue(5, phrase, nth)
        t0, t_end = self.start(5), self.end(5)
        t_stop = t_end - 0.7                                    # the last 0.6 s clear the screen (2D camera returns)
        DROP5, PITCH_MAX, K_RUN, H_CLIMB = 0.9, 16.0, 9.0, 5.0
        t_v1, t_vr, t_v2 = c("قَبْلَهَا"), c("يَرْفَعُ"), c("تَرْتَفِعَ") + 0.3
        t_rot1 = c("وَيَزِيدُ الرَّفْعُ") + 0.6                 # nose-up finished
        t_lift = c("وَيَزِيدُ الرَّفْعُ") + 1.4                 # the wheels leave the ground

        # --- 2D leftovers of segment 4 leave, then the 3D scene starts (camera driver first)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        self.caption = VMobject()
        self.camera.should_apply_shading = False
        cam = self.camera_path([
            (t0, 72, -128, 0.95), (t0 + 12, 74, -118, 1.0), (t_vr, 78, -102, 1.05),
            (t_rot1 + 1.0, 80, -96, 1.05), (t0 + 34, 82, -108, 0.9), (t_end, 84, -122, 0.78)])

        # --- the plane at the origin (nose +x), the ground and its shadow
        plane = airliner_3d()
        shadow = plane.shadow
        body = VGroup(plane.gear, plane.fuselage, plane.wings, plane.tail, plane.engines)
        body.shift(IN * DROP5)
        shadow.shift(IN * DROP5)
        pivot = plane.pivot + IN * DROP5
        runway = runway_3d(x_start=-12.0, length=122.0)
        runway.shift(IN * DROP5)
        n_thr = 8
        n_dash = len(runway) - 3 - n_thr
        dashes, thr = list(runway[3:3 + n_dash]), list(runway[3 + n_dash:])
        PERIOD = 2.6 * n_dash
        for d in dashes:
            d.bx = d.get_center()[0]
            d.cx = d.bx
        st = dict(X=0.0, pitch=0.0, h=0.0, p=0.0)
        ground_last = dict(h=0.0, X=0.0)

        # --- speed profile: pointer position p (0..1 of the tape), concave: the acceleration falls with speed
        from scipy.interpolate import PchipInterpolator
        pk = [(0.0, 0.0), (0.7, 0.0), (3.0, 0.07), (t_v1 - t0, 0.42), (t_vr - t0, 0.62), (t_v2 - t0, 0.86),
              (t_end - t0, 0.95)]
        p_of = PchipInterpolator([k[0] for k in pk], [k[1] for k in pk])
        grid = np.arange(0, t_end - t0 + 0.05, 0.02)
        x_of = np.concatenate([[0.0], np.cumsum(K_RUN * p_of(grid[1:]) * 0.02)])
        smooth01 = lambda u: float(rate_functions.smooth(min(max(u, 0.0), 1.0)))

        # --- the tape (fixed in frame)
        TX0, TX1, TY, BH = -5.5, 5.5, 2.85, 0.44
        tx = lambda p: TX0 + (TX1 - TX0) * p
        P_V1, P_VR, P_V2 = 0.42, 0.62, 0.86
        base = Rectangle(width=TX1 - TX0, height=BH, color=GREY_INK, fill_color=PANEL_FILL, fill_opacity=1,
                         stroke_width=2).move_to([0, TY, 0])
        speed_lbl = label("Speed", FS_NOTE, GREY_INK).next_to(base, UP, buff=0.12).align_to(base, LEFT)
        pointer = Polygon([-0.15, -0.24, 0], [0.15, -0.24, 0], [0, 0, 0], color=INK, fill_color=INK,
                          fill_opacity=1, stroke_width=1)
        marks = []
        for name, full, p in [("V1", "Decision\nspeed", P_V1), ("VR", "Rotation", P_VR),
                              ("V2", "Takeoff\nsafety speed", P_V2)]:
            tick = Line([tx(p), TY + BH / 2, 0], [tx(p), TY + BH / 2 + 0.2, 0], color=INK, stroke_width=4)
            sym = label(name, FS_LABEL, INK, weight=BOLD).next_to(tick, UP, buff=0.06)
            nm = label(full, FS_AXIS, GREY_INK, line_spacing=0.5)
            nm.move_to([tx(p), TY - BH / 2 - 0.55 - nm.height / 2, 0])
            marks.append(dict(p=p, tick=tick, sym=sym, name=nm, lit=False))
        red = Rectangle(width=tx(P_V1) - TX0, height=BH, color=ACCENT_4, fill_color=ACCENT_4, fill_opacity=0.9,
                        stroke_width=0).move_to([(TX0 + tx(P_V1)) / 2, TY, 0])
        green = Rectangle(width=TX1 - tx(P_V1), height=BH, color=ACCENT_3, fill_color=ACCENT_3, fill_opacity=0.9,
                          stroke_width=0).move_to([(TX1 + tx(P_V1)) / 2, TY, 0])
        z_rej = VGroup(icon("hand-stop", WHITE, 0.32), label("Reject", FS_AXIS, WHITE, weight=BOLD)).arrange(RIGHT, buff=0.15)
        z_rej.move_to(red)
        z_con = VGroup(icon("check", WHITE, 0.32), label("Continue", FS_AXIS, WHITE, weight=BOLD)).arrange(RIGHT, buff=0.15)
        z_con.move_to(green)

        # --- accelerate-stop distance: an illustrative bracket under the scene (fixed in frame, no numbers)
        AY, xa, xb, xc = -3.0, -4.6, 0.4, 4.6
        d_acc = Arrow([xa, AY, 0], [xb - 0.05, AY, 0], buff=0, color=ACCENT_2, stroke_width=6, tip_length=0.22)
        d_stop = Arrow([xb + 0.05, AY, 0], [xc, AY, 0], buff=0, color=ACCENT_4, stroke_width=6, tip_length=0.22)
        d_ticks = VGroup(*[Line([x, AY - 0.16, 0], [x, AY + 0.16, 0], color=INK, stroke_width=4) for x in (xa, xb, xc)])
        d_acc_t = label("accelerate", FS_AXIS, ACCENT_2, weight=BOLD).next_to(d_acc, DOWN, buff=0.15)
        d_stop_t = label("stop", FS_AXIS, ACCENT_4, weight=BOLD).next_to(d_stop, DOWN, buff=0.15)
        d_title = label("Accelerate-stop distance", FS_LABEL, INK, weight=BOLD)
        d_box = SurroundingRectangle(d_title, buff=0.14, color=GREY_INK, fill_color=WHITE, fill_opacity=0.95,
                                     corner_radius=0.1, stroke_width=2)
        d_head = VGroup(d_box, d_title).next_to(d_ticks, UP, buff=0.12).set_x(0.5 * (xa + xc))
        d_all = self.fixed(d_acc, d_stop, d_ticks, d_acc_t, d_stop_t, d_box, d_title)

        # --- angle of attack (3D lines that follow the nose) and its label; lift arrow above the wing
        av, lg = ValueTracker(0.0), ValueTracker(0.0)
        NOSE = np.array([PLANE_LENGTH / 2 - 0.0, 0.0, _HULL_Z]) + IN * DROP5
        NOSE[0] = 3.3

        def rot(pt):
            d = np.asarray(pt, dtype=float) - pivot
            a = st["pitch"] * DEGREES
            return pivot + np.array([d[0] * np.cos(a) - d[2] * np.sin(a), d[1], d[0] * np.sin(a) + d[2] * np.cos(a)])

        def line3(a, b, color, width):
            m = VMobject(color=color, stroke_width=width, stroke_opacity=av.get_value())
            m.set_points_as_corners([a, b])
            m.set_shade_in_3d(True)
            return m

        def aoa_geom():
            cn, a, r = rot(NOSE), st["pitch"] * DEGREES + 1e-3, 1.8
            wind = line3(cn, cn + np.array([2.4, 0, 0]), ACCENT_1, 5)
            axis = line3(cn, cn + 2.4 * np.array([np.cos(a), 0, np.sin(a)]), GREY_INK, 5)
            arc = VMobject(color=INK, stroke_width=6, stroke_opacity=av.get_value())
            arc.set_points_as_corners([cn + r * np.array([np.cos(u), 0, np.sin(u)]) for u in np.linspace(0, a, 12)])
            arc.set_shade_in_3d(True)
            return VGroup(wind, axis, arc)
        aoa = always_redraw(aoa_geom)
        aoa_mid = lambda: rot(NOSE) + 1.8 * np.array([np.cos(st["pitch"] * DEGREES / 2), 0,
                                                       np.sin(st["pitch"] * DEGREES / 2)])
        aoa_txt = label("Angle of attack", FS_NOTE, INK)
        aoa_box = SurroundingRectangle(aoa_txt, buff=0.15, color=INK, fill_color=WHITE, fill_opacity=0.95, stroke_width=2)
        aoa_grp = VGroup(aoa_box, aoa_txt).move_to([5.0, 0.15, 0])
        aoa_leader = Line(ORIGIN, RIGHT, color=INK, stroke_width=2.5)
        aoa_dot = Dot(color=INK, radius=0.06)

        B0 = np.array([0.3, -1.6, _HULL_Z - 0.18 + 0.14]) + IN * DROP5

        def lift_geom():
            b, L = rot(B0), 0.25 + 1.0 * lg.get_value()
            w, hw, hl = 0.09, 0.22, 0.36
            pts = [[b[0] - w, b[1], b[2]], [b[0] + w, b[1], b[2]], [b[0] + w, b[1], b[2] + L - hl],
                   [b[0] + hw, b[1], b[2] + L - hl], [b[0], b[1], b[2] + L], [b[0] - hw, b[1], b[2] + L - hl],
                   [b[0] - w, b[1], b[2] + L - hl]]
            return _flat(pts, fill=ACCENT_1, opacity=min(1.0, 5 * lg.get_value()), stroke=ACCENT_1, width=1)
        lift = always_redraw(lift_geom)
        lift_txt = label("Lift", FS_LABEL, ACCENT_1, weight=BOLD)
        lift_txt.set_opacity(0.0)

        # --- the driver of the scene state (added right after the camera driver)
        state = Mobject()
        state.clock = self.renderer.time

        def drive(m, dt):
            m.clock += dt
            T = m.clock - t0
            st["p"] = float(p_of(min(max(T, 0.0), t_end - t0)))
            st["X"] = float(np.interp(T, grid, x_of))
            pitch = PITCH_MAX * smooth01((m.clock - t_vr) / (t_rot1 - t_vr))
            st["h"] = H_CLIMB * min(max((m.clock - t_lift) / (t_stop - t_lift), 0.0), 1.0) ** 1.5
            body.rotate(-(pitch - st["pitch"]) * DEGREES, axis=UP, about_point=pivot)
            st["pitch"] = pitch
            # ground: the dashes run cyclically, the threshold bars leave, everything sinks with h
            dz = -(st["h"] - ground_last["h"])
            for d in dashes:
                nx = -12.0 + ((d.bx + 12.0 - st["X"]) % PERIOD)
                d.shift([nx - d.cx, 0, dz])
                d.cx = nx
            for k in thr:
                k.shift([-(st["X"] - ground_last["X"]), 0, dz])
                k.set_opacity(max(0.0, 1.0 - st["X"] / 9.0))
            for k in list(runway[:3]) + [shadow]:
                k.shift([0, 0, dz])
            ground_last.update(h=st["h"], X=st["X"])
            # the tape
            pointer.move_to([tx(st["p"]), TY - BH / 2 - 0.12 - 0.02, 0])
            for mk in marks:
                lit = st["p"] >= mk["p"]
                if lit != mk["lit"]:
                    mk["lit"] = lit
                    for part in (mk["tick"], mk["sym"], mk["name"]):
                        part.set_color(ACCENT_2 if lit else (INK if part is not mk["name"] else GREY_INK))
            # labels that follow 3D points
            proj = lambda pt: self.camera.project_point(pt)
            aoa_leader.put_start_and_end_on(aoa_box.get_top() + UP * 0.02, proj(aoa_mid()))
            aoa_dot.move_to(proj(aoa_mid()))
            b = rot(B0)
            lift_txt.move_to(proj(b + np.array([0, 0, 0.25 + 0.5 * lg.get_value()])) + LEFT * 0.62)
            lift_txt.set_opacity(min(1.0, 3 * lg.get_value()))
        state.add_updater(drive)
        self.add(state)
        drive(state, 0)

        _play = self.play

        def synced_play(*a, **k):
            """Manim's first frame of every play has dt = 0: put the drivers back on the clock."""
            _play(*a, **k)
            cam.clock = state.clock = self.renderer.time
        self.play = synced_play

        # --- fade the scene in under a white cover
        cover = Rectangle(width=15, height=9, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=0)
        self.fixed(cover)
        self.add(runway, shadow, body)
        self.add(cover)
        self.play(FadeOut(cover), run_time=0.8)

        # --- the tape and the three speeds
        self.fixed(base, speed_lbl, pointer, red, green, z_rej, z_con, aoa_grp, aoa_leader, aoa_dot, lift_txt)
        self.fixed(*[part for mk in marks for part in (mk["tick"], mk["sym"], mk["name"])])
        self.add(lift_txt)
        self.sync(c("وَالآنَ") + 1.5)
        self.play(FadeIn(base), FadeIn(speed_lbl), FadeIn(pointer), run_time=0.6)
        m1, m2, m3 = marks
        self.sync(c("أَوَّلًا") - 0.1)
        self.play(FadeIn(VGroup(m1["tick"], m1["sym"])), run_time=0.4)
        self.sync(c("سُرْعَةُ القَرَارِ") - 0.1)
        self.play(FadeIn(m1["name"], shift=DOWN * 0.1), run_time=0.5)

        # V1: the accelerate-stop distance, then reject before it, continue after it
        self.sync(c("مَسَافَةِ") - 0.1)
        self.play(FadeIn(d_head), FadeIn(d_ticks), run_time=0.5)
        self.sync(c("التَّسَارُعِ") - 0.1)
        self.play(GrowArrow(d_acc), FadeIn(d_acc_t), run_time=0.7)
        self.sync(c("وَالتَّوَقُّفِ") - 0.1)
        self.play(GrowArrow(d_stop), FadeIn(d_stop_t), run_time=0.7)
        self.sync(c("قَبْلَهَا") - 0.2)
        self.play(FadeIn(red), FadeIn(z_rej), run_time=0.6)
        self.sync(c("وَبَعْدَهَا") - 0.2)
        self.play(FadeOut(VGroup(d_head, d_ticks, d_acc, d_stop, d_acc_t, d_stop_t)), FadeIn(green), FadeIn(z_con),
                  run_time=0.6)

        # VR: the nose goes up, the angle of attack and the lift grow
        self.sync(c("ثُمَّ فِي آرْ") - 0.1)
        self.play(FadeIn(VGroup(m2["tick"], m2["sym"])), run_time=0.4)
        self.sync(c("سُرْعَةُ الدَّوَرَانِ") - 0.1)
        self.play(FadeIn(m2["name"], shift=DOWN * 0.1), run_time=0.5)
        self.sync(c("فَتَزِيدُ زَاوِيَةُ") - 0.1)
        self.add(aoa)
        self.play(av.animate.set_value(1.0), FadeIn(aoa_grp), FadeIn(aoa_leader), FadeIn(aoa_dot), run_time=0.6)
        self.sync(c("وَيَزِيدُ الرَّفْعُ") - 0.1)
        self.add(lift)
        self.play(lg.animate.set_value(1.0), run_time=1.0)

        # V2: reached after lift-off
        self.sync(c("ثُمَّ فِي تُو") - 0.1)
        self.play(FadeIn(VGroup(m3["tick"], m3["sym"])), FadeOut(VGroup(aoa_grp, aoa_leader, aoa_dot)),
                  av.animate.set_value(0.0), run_time=0.5)
        self.remove(aoa)
        self.sync(c("سُرْعَةُ الأَمَانِ") - 0.1)
        self.play(FadeIn(m3["name"], shift=DOWN * 0.1), run_time=0.5)

        # the order V1 <= VR, then V2
        o_v1, o_le, o_vr, o_then, o_v2 = [label(t, FS_SUBTITLE, INK, weight=BOLD) for t in ("V1", "≤", "VR", "then", "V2")]
        order = VGroup(o_v1, o_le, o_vr, o_then, o_v2).arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        o_comma = label(",", FS_SUBTITLE, INK, weight=BOLD).next_to(o_vr, RIGHT, buff=0.04).align_to(o_vr, DOWN).shift(DOWN * 0.1)
        VGroup(o_then, o_v2).shift(RIGHT * 0.2)
        order.add(o_comma)
        o_box = SurroundingRectangle(order, buff=0.25, color=ACCENT_2, fill_color=WHITE, fill_opacity=0.95,
                                     corner_radius=0.1, stroke_width=3)
        order_grp = VGroup(o_box, order).to_edge(DOWN, buff=0.45)
        self.fixed(o_box, order)
        self.sync(c("التَّرْتِيبُ") - 0.1)
        self.play(FadeIn(order_grp, shift=UP * 0.15), run_time=0.6)
        for word, part in [(c("فِي وَنْ", 2), o_v1), (c("ثُمَّ فِي آرْ", 2), o_vr), (c("ثُمَّ فِي تُو", 2), o_v2)]:
            self.sync(word - 0.05)
            self.play(Indicate(part, color=ACCENT_2, scale_factor=1.35), run_time=0.6)
        self.sync(c("لَا تَتَجَاوَزُ") - 0.1)
        self.play(Indicate(o_le, color=ACCENT_2, scale_factor=1.6), run_time=0.7)

        # clear the screen and give segment 6 the default top-down camera
        self.sync(t_stop)
        del self.play
        self.reset_camera_2d(cam)
        state.clear_updaters()

    # ---------------- Segment 6 ----------------
    def segment_6(self):
        """Three factors move the lift-off speed: warm air, a headwind, weight (2D, flat top-down camera)."""
        c = lambda phrase, nth=1: self.cue(6, phrase, nth)
        T = lambda phrase, dt=0.1, nth=1: c(phrase, nth) - dt
        t0, t_end = self.start(6), self.end(6)
        T_STD_C = D.P0 / (D.R_AIR * D.RHO_15) - 273.15          # the temperature behind RHO_15 (15 °C)
        assert f"{T_STD_C:.0f}" == "15"
        heavy_f = 1 + D.WEIGHT_INCREASE                          # W -> 1.10 W

        # ---------- the three factors: a big row first, then a stage bar on top with a marker on the current one
        names = [("temperature", "Heat"), ("wind", "Headwind"), ("weight", "Weight")]
        big = VGroup(*[VGroup(icon(n, INK, 1.3), label(t, FS_BODY)).arrange(DOWN, buff=0.25) for n, t in names])
        big.arrange(RIGHT, buff=1.8, aligned_edge=UP).move_to([0, 0.2, 0])
        stage = VGroup(*[VGroup(icon(n, INK, 0.5), label(t, FS_LABEL)).arrange(RIGHT, buff=0.15) for n, t in names])
        stage.arrange(RIGHT, buff=0.9).move_to([1.0, 3.3, 0])
        ring = lambda i: RoundedRectangle(width=stage[i].width + 0.4, height=stage[i].height + 0.3, corner_radius=0.12,
                                          color=ACCENT_1, stroke_width=3.5).move_to(stage[i])
        marker = ring(0)

        self.sync(T("ثَلَاثَةُ", -0.1))
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in big], lag_ratio=0.8), run_time=2.2)

        # ================= (a) warm air =================
        BW, BH = 2.7, 2.0
        box_c = Rectangle(width=BW, height=BH, color=GREY_INK, fill_color=PANEL_FILL, fill_opacity=0.5, stroke_width=3)
        box_h = Rectangle(width=BW, height=BH, color=GREY_INK, fill_color=PANEL_FILL, fill_opacity=0.5, stroke_width=3)
        VGroup(box_c, box_h).arrange(RIGHT, buff=0.8).move_to([-3.55, 0.95, 0])
        cols, rows = 6, 4
        rng = np.random.RandomState(6)
        gx = np.linspace(-BW / 2 + 0.3, BW / 2 - 0.3, cols)
        gy = np.linspace(-BH / 2 + 0.3, BH / 2 - 0.3, rows)
        bases0 = [np.array([gx[i], gy[j], 0.0]) + np.array([*rng.uniform(-0.1, 0.1, 2), 0.0])
                  for j in range(rows) for i in range(cols)]
        keep = [j * cols + i for j in range(rows) for i in range(cols) if (i + j) % 2 == 0]      # 12 of the 24 stay
        hx, hy = np.linspace(-BW / 2 + 0.4, BW / 2 - 0.4, 4), np.linspace(-BH / 2 + 0.4, BH / 2 - 0.4, 3)
        spread = [np.array([hx[i], hy[j], 0.0]) for j in range(3) for i in range(4)]
        bases1 = {k: spread[n] for n, k in enumerate(keep)}
        thin = ValueTracker(0.0)
        dots_c = _jiggle_dots(box_c, bases0, bases0, list(range(24)), None, ACCENT_1, 0.05, 0.05, 5.0)
        dots_h = _jiggle_dots(box_h, bases0, bases1, keep, thin, ACCENT_2, 0.06, 0.15, 7.5)
        tmp_c = VGroup(icon("temperature", ACCENT_1, 0.45), label(f"{T_STD_C:.0f} °C", FS_LABEL)).arrange(RIGHT, buff=0.12)
        tmp_h = VGroup(icon("temperature", ACCENT_2, 0.45), label(f"{D.T_HOT_C:.0f} °C", FS_LABEL, ACCENT_2)).arrange(RIGHT, buff=0.12)
        tmp_c.next_to(box_c, UP, buff=0.2)
        tmp_h.next_to(box_h, UP, buff=0.2)
        rho_c = label(f"ρ = {D.RHO_15:.3f} kg/m³", FS_AXIS, ACCENT_1).next_to(box_c, DOWN, buff=0.22)
        rho_h = label(f"ρ = {D.RHO_HOT:.2f} kg/m³", FS_AXIS, ACCENT_2).next_to(box_h, DOWN, buff=0.22)

        # airspeed bars (right column, top)
        X0, kv = 1.6, 3.0 / D.V_15
        sp_head = label("Airspeed needed for lift-off", FS_AXIS, GREY_INK)
        sp_head.move_to([3.7, 2.5, 0])
        bar = lambda w, y: Rectangle(width=w, height=0.36, color=ACCENT_1, fill_color=ACCENT_1, fill_opacity=0.9,
                                     stroke_width=0).move_to([X0 + w / 2, y, 0])
        sp_c, sp_h = bar(kv * D.V_15, 1.85), bar(kv * D.V_HOT, 1.2)
        sp_tc = label(f"{T_STD_C:.0f} °C", FS_AXIS).next_to(sp_c, LEFT, buff=0.15)
        sp_th = label(f"{D.T_HOT_C:.0f} °C", FS_AXIS, ACCENT_2).next_to(sp_h, LEFT, buff=0.15)
        sp_vc = label(f"{D.V_15:.1f} m/s", FS_LABEL).next_to(sp_c, RIGHT, buff=0.15)
        sp_vh = label(f"{D.V_HOT:.1f} m/s", FS_LABEL, ACCENT_2)
        sp_vh.next_to(sp_h, RIGHT, buff=0.15)
        sp_ref = DashedLine([X0 + kv * D.V_15, 2.1, 0], [X0 + kv * D.V_15, 1.0, 0], dash_length=0.1, color=GREY_INK, stroke_width=2.5)
        sp_plus = label(f"+{D.HOT_INCREASE * 100:.0f} %", FS_LABEL, ACCENT_2, weight=BOLD)
        sp_plus.next_to(sp_h, DOWN, buff=0.12).align_to(sp_h, RIGHT)

        # runway needed (left column, bottom): longer for warm air, no number
        rw_head = label("Runway needed", FS_AXIS, GREY_INK)
        rw_head.move_to([-3.55, -1.3, 0])
        rw_x0 = -5.4
        rbar = lambda w, y: Rectangle(width=w, height=0.36, color=GREY_INK, fill_color=GREY_INK, fill_opacity=0.5,
                                      stroke_width=0).move_to([rw_x0 + w / 2, y, 0])
        rw_c, rw_h, rw_h2 = rbar(2.6, -1.95), rbar(2.6, -2.6), rbar(3.5, -2.6)
        rw_tc = label(f"{T_STD_C:.0f} °C", FS_AXIS).next_to(rw_c, LEFT, buff=0.15)
        rw_th = label(f"{D.T_HOT_C:.0f} °C", FS_AXIS, ACCENT_2).next_to(rw_h, LEFT, buff=0.15)
        rw_long = label("longer", FS_LABEL, ACCENT_2, weight=BOLD).next_to(rw_h2, RIGHT, buff=0.2)

        # the cockpit airspeed indicator reads the same in both cases (dial without numbers)
        dial_head = label("Cockpit airspeed indicator", FS_AXIS, GREY_INK).move_to([3.7, -0.4, 0])
        g_c, g_h = _gauge(0.8), _gauge(0.8)
        g_c.move_to([2.3, -1.65, 0])
        g_h.move_to([5.1, -1.65, 0])
        u_c, u_h = ValueTracker(0.0), ValueTracker(0.0)
        nd_c, nd_h = _needle(g_c, u_c), _needle(g_h, u_h)
        g_tc = label(f"{T_STD_C:.0f} °C", FS_AXIS).next_to(g_c, DOWN, buff=0.25)
        g_th = label(f"{D.T_HOT_C:.0f} °C", FS_AXIS, ACCENT_2).next_to(g_h, DOWN, buff=0.25)
        g_eq = label("=", FS_HEADING, ACCENT_3, weight=BOLD).move_to([3.7, -1.65, 0])
        g_same = label("same reading", FS_LABEL, ACCENT_3, weight=BOLD).move_to([3.7, -3.4, 0])

        # --- the big row becomes the stage bar, marker on "Heat"
        self.sync(T("أَوَّلًا", 0.25))
        self.play(FadeOut(big, shift=UP * 0.3), FadeIn(stage, shift=DOWN * 0.15), Create(marker), run_time=0.7)

        # --- dense cold air, then warm air
        self.sync(T("الهَوَاءُ الحَارُّ", 0.1))
        self.play(FadeIn(VGroup(box_c, dots_c, tmp_c, rho_c)), run_time=0.5)
        self.sync(T("الحَارُّ", 0.1))
        self.play(FadeIn(VGroup(box_h, dots_h, tmp_h[0])), run_time=0.3)
        self.sync(T("أَقَلُّ", 0.05))
        self.play(thin.animate.set_value(1.0), run_time=1.3, rate_func=smooth)
        self.sync(T("خَمْسٍ", 0.05))
        self.play(FadeIn(tmp_h[1], shift=LEFT * 0.1), run_time=0.4)
        self.sync(T("الكَثَافَةُ", 0.05))
        self.play(Indicate(rho_c, color=ACCENT_2, scale_factor=1.15), run_time=0.7)
        self.sync(T("وَاحِدٍ", 0.05))
        self.play(FadeIn(rho_h, shift=DOWN * 0.1), run_time=0.5)

        # --- airspeed bars: 76.4 → 80.3 m/s, about 5 % more
        self.sync(T("فَتَصِيرُ", 0.05))
        self.play(FadeIn(sp_head, shift=DOWN * 0.1), run_time=0.5)
        self.sync(T("السُّرْعَةُ اللَّازِمَةُ", 0.05))
        self.play(GrowFromEdge(sp_c, LEFT), FadeIn(sp_tc), run_time=0.7)
        self.play(FadeIn(sp_vc, shift=RIGHT * 0.1), run_time=0.3)
        self.sync(T("بِالنِّسْبَةِ", 0.05))
        self.play(Circumscribe(sp_head, color=ACCENT_1, buff=0.12, run_time=0.9))
        self.sync(T("ثَمَانِينَ", 0.05))
        self.play(GrowFromEdge(sp_h, LEFT), FadeIn(sp_th), Create(sp_ref), run_time=0.9)
        self.sync(T("ثَلَاثَةٍ", 0.05))
        self.play(FadeIn(sp_vh, shift=RIGHT * 0.1), run_time=0.4)
        self.sync(T("خَمْسَةٍ", 0.05))
        self.play(FadeIn(sp_plus, shift=UP * 0.1), run_time=0.5)

        # --- a longer runway
        self.sync(T("وَيَلْزَمُ", 0.05))
        self.play(FadeIn(rw_head), GrowFromEdge(rw_c, LEFT), GrowFromEdge(rw_h, LEFT), FadeIn(rw_tc), FadeIn(rw_th),
                  run_time=0.7)
        self.sync(T("أَطْوَلُ", 0.15))
        self.play(Transform(rw_h, rw_h2), run_time=0.7)
        self.play(FadeIn(rw_long, shift=RIGHT * 0.1), run_time=0.4)

        # --- the cockpit airspeed indicator shows the same value
        self.sync(T("عَدَّادَ", 0.05))
        self.add(nd_c, nd_h)
        self.play(FadeIn(VGroup(dial_head, g_c, g_h, nd_c, nd_h, g_tc, g_th)), run_time=0.6)
        self.sync(T("فِي قُمْرَةِ", 0.2))
        self.play(u_c.animate.set_value(GAUGE_MARK), run_time=0.9, rate_func=smooth)
        self.sync(T("يُظْهِرُ", 0.05))
        self.play(u_h.animate.set_value(GAUGE_MARK), run_time=0.9, rate_func=smooth)
        self.sync(T("نَفْسَهَا", 0.05))
        self.play(FadeIn(g_eq), FadeIn(g_same, shift=UP * 0.1), run_time=0.6)

        # ================= (b) headwind =================
        A = VGroup(box_c, box_h, dots_c, dots_h, tmp_c, tmp_h, rho_c, rho_h, sp_head, sp_c, sp_h, sp_tc, sp_th, sp_vc,
                   sp_vh, sp_ref, sp_plus, rw_head, rw_c, rw_h, rw_tc, rw_th, rw_long, dial_head, g_c, g_h, nd_c, nd_h,
                   g_tc, g_th, g_eq, g_same)
        RWY = 0.8                                            # top edge of the runway
        PS = 0.9
        plane = airliner_side().scale(PS, about_point=ORIGIN)
        plane.shift([-2.0, RWY + 0.75 * PS, 0])
        cg = plane.body.get_center()
        rw_top = Line([-6.85, RWY, 0], [6.85, RWY, 0], color=GREY_INK, stroke_width=3)
        rw_bot = Line([-6.85, RWY - 0.9, 0], [6.85, RWY - 0.9, 0], color=GREY_INK, stroke_width=3)
        rw_dash = VGroup(*[Line([x, RWY - 0.45, 0], [x + 0.6, RWY - 0.45, 0], color=LIGHT_INK, stroke_width=5)
                           for x in np.arange(-6.6, 6.6, 1.65)])
        ground = VGroup(rw_top, rw_bot, rw_dash)
        w_arrow = Arrow([5.9, 1.75, 0], [3.0, 1.75, 0], buff=0, color=ACCENT_1, stroke_width=7, tip_length=0.3)
        w_row = VGroup(icon("wind", ACCENT_1, 0.6), label("Headwind", FS_LABEL, ACCENT_1),
                       label(f"{D.HEADWIND:.0f} m/s", FS_LABEL, ACCENT_1, weight=BOLD)).arrange(RIGHT, buff=0.2)
        w_row.move_to([4.45, 2.5, 0])
        streaks = VGroup(*[Line(ORIGIN, RIGHT * 0.7, color=ACCENT_1, stroke_width=4) for _ in range(3)])
        streaks.t = 0.0
        s_y = [1.05, 1.35, 1.2]

        def flow(m, dt):
            m.t += dt
            for i, sl in enumerate(m):
                x = 6.3 - ((m.t * 2.2 + i * 1.9) % 5.2)
                sl.put_start_and_end_on([x + 0.7, s_y[i], 0], [x, s_y[i], 0])
                sl.set_stroke(opacity=float(min(1.0, (x - 1.1) / 0.6, (6.3 - x) / 0.6)) if 1.1 < x < 6.3 else 0.0)
        streaks.add_updater(flow)
        flow(streaks, 0)
        lift_a = Arrow(cg + UP * 0.3, cg + UP * 1.05, buff=0, color=ACCENT_1, stroke_width=7, tip_length=0.28)
        lift_t = label("Lift", FS_LABEL, ACCENT_1).next_to(lift_a, RIGHT, buff=0.12)

        K = 0.07
        AX0 = -3.3
        ya, yg = -0.85, -1.85
        air_l = label("Airspeed", FS_LABEL, ACCENT_1).move_to([-6.5, ya, 0], LEFT)
        air_a = Arrow([AX0, ya, 0], [AX0 + K * D.V_15, ya, 0], buff=0, color=ACCENT_1, stroke_width=8, tip_length=0.3)
        air_v = label(f"{D.V_15:.1f} m/s", FS_LABEL, ACCENT_1).next_to(air_a, RIGHT, buff=0.2)
        gr_l = label("Ground speed", FS_LABEL).move_to([-6.5, yg, 0], LEFT)
        gr_a = Arrow([AX0, yg, 0], [AX0 + K * D.V_GROUND_HEADWIND, yg, 0], buff=0, color=INK, stroke_width=8, tip_length=0.3)
        gr_gap = DashedLine([AX0 + K * D.V_GROUND_HEADWIND, yg, 0], [AX0 + K * D.V_15, yg, 0], dash_length=0.1,
                            color=ACCENT_1, stroke_width=6)
        gr_gap_t = label(f"{D.HEADWIND:.0f} m/s", FS_AXIS, ACCENT_1).next_to(gr_gap, DOWN, buff=0.2)
        gr_v = label(f"{D.V_GROUND_HEADWIND:.1f} m/s", FS_LABEL).next_to(gr_gap, RIGHT, buff=0.2)
        eq_cap = label("Ground speed = airspeed − wind", FS_AXIS, GREY_INK)
        eq = label(f"{D.V_15:.1f} − {D.HEADWIND:.0f} = {D.V_GROUND_HEADWIND:.1f} m/s", FS_LABEL + 6, INK, weight=BOLD)
        VGroup(eq_cap, eq).arrange(DOWN, buff=0.15).move_to([-0.5, -3.1, 0])

        self.sync(T("ثَانِيًا", 0.1))
        self.play(FadeOut(A), Transform(marker, ring(1)), FadeIn(VGroup(ground, plane)), run_time=0.6)
        for m in A:
            m.clear_updaters()
        self.remove(nd_c, nd_h)
        self.sync(T("المُعَاكِسَةُ", 0.05))
        self.add(streaks)
        self.play(FadeIn(w_row[0]), FadeIn(w_row[1]), FadeIn(w_arrow, shift=LEFT * 0.6), run_time=0.8)
        self.sync(T("الرَّفْعَ", 0.05))
        self.play(GrowArrow(lift_a), FadeIn(lift_t), run_time=0.6)
        self.sync(T("سُرْعَةِ الطَّائِرَةِ", 0.05))
        self.play(FadeIn(air_l), GrowArrow(air_a), run_time=0.7)
        self.play(FadeIn(air_v, shift=RIGHT * 0.1), run_time=0.25)
        self.sync(T("بِالنِّسْبَةِ", 0.05, 2))
        self.play(Circumscribe(VGroup(w_arrow, w_row[:2]), color=ACCENT_1, buff=0.15), run_time=0.9)
        self.sync(T("لِلْأَرْضِ", 0.05))
        self.play(Circumscribe(ground, color=GREY_INK, buff=0.1), run_time=0.8)
        self.sync(T("عَشَرَةُ", 0.05))
        self.play(FadeIn(w_row[2], shift=LEFT * 0.1), run_time=0.4)
        self.sync(T("أَرْضِيَّةٌ", 0.05))
        self.play(FadeIn(gr_l), run_time=0.4)
        self.sync(T("سِتَّةٌ", 0.05))
        self.play(GrowArrow(gr_a), run_time=0.8)
        self.play(Create(gr_gap), FadeIn(gr_gap_t), run_time=0.5)
        self.sync(T("أَرْبَعَةٍ", 0.05))
        self.play(FadeIn(gr_v, shift=RIGHT * 0.1), run_time=0.4)
        self.play(FadeIn(VGroup(eq_cap, eq), shift=UP * 0.1), run_time=0.6)

        # ================= (c) weight =================
        B = VGroup(ground, plane, w_row, w_arrow, streaks, lift_a, lift_t, air_l, air_a, air_v, gr_l, gr_a, gr_gap,
                   gr_gap_t, gr_v, eq_cap, eq)
        WX = -4.6
        wt_head = VGroup(icon("weight", ACCENT_4, 1.0), label("Weight", FS_LABEL, ACCENT_4)).arrange(RIGHT, buff=0.2)
        wt_head.move_to([WX + 0.5, 2.1, 0])
        mk_w = lambda L: Arrow([WX, 1.3, 0], [WX, 1.3 - L, 0], buff=0, color=ACCENT_4, stroke_width=9, tip_length=0.32)
        w_a, w_a2 = mk_w(2.0), mk_w(2.0 * heavy_f)
        w_t1 = label("W", FS_LABEL + 6, ACCENT_4, weight=BOLD).next_to(Point([WX, 0.6, 0]), RIGHT, buff=0.3)
        w_t2 = label(f"{heavy_f:.2f} W", FS_LABEL + 6, ACCENT_4, weight=BOLD).next_to(Point([WX, 0.6, 0]), RIGHT, buff=0.3)
        w_old = DashedLine([WX - 0.35, 1.3 - 2.0, 0], [WX + 0.35, 1.3 - 2.0, 0], dash_length=0.08, color=GREY_INK, stroke_width=2.5)
        w_plus = label(f"+{D.WEIGHT_INCREASE * 100:.0f} %", FS_LABEL, ACCENT_4, weight=BOLD).next_to(w_a2, DOWN, buff=0.2)

        VX0, kw = -0.4, 4.4 / D.V_15
        v_head = label("Speed needed for lift-off", FS_AXIS, GREY_INK).move_to([2.4, 2.3, 0])
        vbar = lambda w, y: Rectangle(width=w, height=0.4, color=ACCENT_1, fill_color=ACCENT_1, fill_opacity=0.9,
                                      stroke_width=0).move_to([VX0 + w / 2, y, 0])
        v_b1, v_b2 = vbar(kw * D.V_15, 1.6), vbar(kw * D.V_HEAVY, 0.85)
        v_t1 = label("W", FS_LABEL, ACCENT_4, weight=BOLD).next_to(v_b1, LEFT, buff=0.15)
        v_t2 = label(f"{heavy_f:.2f} W", FS_LABEL, ACCENT_4, weight=BOLD).next_to(v_b2, LEFT, buff=0.15)
        v_v1 = label(f"{D.V_15:.1f} m/s", FS_LABEL, ACCENT_1).next_to(v_b1, RIGHT, buff=0.3)
        v_ref = DashedLine([VX0 + kw * D.V_15, 1.85, 0], [VX0 + kw * D.V_15, 0.62, 0], dash_length=0.1, color=GREY_INK, stroke_width=2.5)
        v_plus = label(f"+{D.HEAVY_INCREASE * 100:.1f} %", FS_LABEL + 4, ACCENT_1, weight=BOLD).next_to(v_b2, RIGHT, buff=0.3)
        f1 = label("V ∝ √", FS_HEADING, INK)
        f2 = label("W", FS_HEADING, ACCENT_4, weight=BOLD)
        form = VGroup(f1, f2).arrange(RIGHT, buff=0.04).move_to([2.4, -0.55, 0])
        calc = label(f"V × √{heavy_f:.2f} = V × {np.sqrt(heavy_f):.3f}", FS_LABEL, INK).move_to([2.4, -1.6, 0])

        self.sync(T("ثَالِثًا", 0.1))
        self.play(FadeOut(B), Transform(marker, ring(2)), run_time=0.55)
        for m in B:
            m.clear_updaters(recursive=True)
        self.sync(T("الوَزْنُ", 0.05))
        self.play(FadeIn(wt_head, shift=DOWN * 0.1), GrowArrow(w_a), FadeIn(w_t1), run_time=0.7)
        self.sync(T("السُّرْعَةُ اللَّازِمَةُ", 0.05, 2))
        self.play(FadeIn(v_head), GrowFromEdge(v_b1, LEFT), FadeIn(v_t1), run_time=0.7)
        self.play(FadeIn(v_v1, shift=RIGHT * 0.1), run_time=0.3)
        self.sync(T("تَتَنَاسَبُ", 0.05))
        self.play(FadeIn(f1, shift=DOWN * 0.1), run_time=0.6)
        self.sync(T("الجَذْرِ", 0.05))
        self.play(FadeIn(f2, shift=DOWN * 0.1), run_time=0.5)
        self.sync(T("بِعَشَرَةٍ", 0.05))
        self.add(w_old)
        self.play(Transform(w_a, w_a2), Transform(w_t1, w_t2), FadeIn(w_plus, shift=UP * 0.1), run_time=0.9)
        self.sync(T("سُرْعَةً أَعْلَى", 0.05))
        self.play(GrowFromEdge(v_b2, LEFT), FadeIn(v_t2), Create(v_ref), FadeIn(calc, shift=UP * 0.1), run_time=1.2)
        self.sync(T("تِسْعَةٍ", 0.05))
        self.play(FadeIn(v_plus, shift=RIGHT * 0.1), run_time=0.5)
        self.sync(t_end)

    # ---------------- Segment 7 ----------------
    def segment_7(self):
        """Conclusion: three summary lines at their words, then a plane runs along a runway and climbs a dashed path."""
        c = lambda phrase, nth=1: self.cue(7, phrase, nth)
        t_end = self.end(7)

        # --- the plane, its runway and the dashed climb path (built now, shown at the second sentence)
        RY, X0, X1, X2 = -3.3, -5.6, -0.6, 5.6            # runway height, run start, take-off point, path end
        Y_END = -2.0
        path_fn = lambda s: np.array([X1 + (X2 - X1) * s, RY + (Y_END - RY) * s ** 1.7, 0])
        plane_ic = icon("plane-departure", INK, 0.9)
        off = plane_ic.height / 2 + 0.06                   # the wheels' height above the line
        runway = Line([X0 - 0.3, RY, 0], [X1, RY, 0], color=GREY_INK, stroke_width=4)
        climb = DashedVMobject(ParametricFunction(path_fn, t_range=[0, 1], color=GREY_INK, stroke_width=4),
                               num_dashes=22, color=GREY_INK)
        plane_ic.move_to([X0, RY + off, 0])

        # --- the box: heading, then the lines at their words (library)
        self.clear(run_time=0.3)
        box = summary_box(self, "Summary",
                          ["The wing makes lift", "Lift grows with V²", "Air density sets the speed needed"],
                          cues=[c("الجَنَاحُ"), c("وَالرَّفْعُ"), c("وَكَثَافَةُ")], pos=[0, 0.75, 0])
        lines = box[1][1]                                   # the three body lines

        # --- second sentence: each factor pulses at its word while the plane rolls
        t_roll, t_lift = c("الجَنَاحُ", 2), c("لَحْظَةَ")

        def move(m):
            t = self.renderer.time
            if t < t_lift:
                s = min(max((t - t_roll) / (t_lift - t_roll), 0.0), 1.0)
                m.move_to([X0 + (X1 - X0) * s ** 2, RY + off, 0])
            else:
                s = min((t - t_lift) / (t_end - 0.2 - t_lift), 1.0)
                s = s * s * (3 - 2 * s) * 0.5 + s * 0.5     # ease, but keep moving to the end
                m.move_to(path_fn(s) + UP * off)
        plane_ic.add_updater(move)

        def hold(t):                                        # like sync(), but the plane's updater keeps running while we wait
            rem = t - self.renderer.time
            if rem > 1e-3:
                self.wait(rem, frozen_frame=False)

        hold(c("مِنْهَا"))
        self.play(Create(runway), FadeIn(plane_ic), run_time=0.6)
        hold(c("الجَنَاحُ", 2) - 0.05)
        self.play(Indicate(lines[0], color=ACCENT_1, scale_factor=1.05), run_time=0.5)
        hold(c("وَالسُّرْعَةُ") - 0.05)
        self.play(Indicate(lines[1], color=ACCENT_1, scale_factor=1.05), run_time=0.5)
        hold(c("وَكَثَافَةُ", 2) - 0.05)
        self.play(Indicate(lines[2], color=ACCENT_1, scale_factor=1.05), run_time=0.5)
        hold(t_lift - 0.05)
        self.play(Create(climb), run_time=max(t_end - 0.2 - t_lift, 0.5), rate_func=linear)
        hold(t_end)


if __name__ == "__main__":
    main(__file__, "TakeoffLift", NARRATION)
