"""Generic twin-jet airliner (no livery, no logo) as plain mesh data, shared by styles A and C.

Plane frame: +X nose, +Y right wing, +Z up, origin = fuselage centre, metres (length 40 m).
build() returns parts: dict(name, group, smooth, verts, faces, mats). group is "body" or "gear"
(the gear group retracts). mats[i] is a material key for face i.
"""
import math

PIVOT = (-2.0, 0.0, -4.2)  # main-gear ground contact, in the plane frame
R_BODY = 2.05


def _loft(name, xs, radius_fn, zoff_fn, mat_fn, n_ring, centre=(0.0, 0.0, 0.0), caps=None, smooth=True, group="body"):
    verts, faces, mats = [], [], []
    for x in xs:
        r = max(radius_fn(x), 0.03)
        zo = zoff_fn(x)
        for j in range(n_ring):
            th = 2 * math.pi * j / n_ring
            verts.append((x + centre[0], centre[1] + r * math.cos(th), centre[2] + zo + r * math.sin(th)))
    for i in range(len(xs) - 1):
        xm = 0.5 * (xs[i] + xs[i + 1])
        for j in range(n_ring):
            a, b = i * n_ring + j, i * n_ring + (j + 1) % n_ring
            c, d = (i + 1) * n_ring + (j + 1) % n_ring, (i + 1) * n_ring + j
            faces.append((a, b, c, d))
            mats.append(mat_fn(xm, 2 * math.pi * (j + 0.5) / n_ring))
    if caps:
        for end, mat in caps:  # end = 0 (first ring) or -1 (last ring)
            base = 0 if end == 0 else (len(xs) - 1) * n_ring
            ring = [base + j for j in range(n_ring)]
            faces.append(tuple(ring if end else ring[::-1]))
            mats.append(mat)
    return dict(name=name, group=group, smooth=smooth, verts=verts, faces=faces, mats=mats)


def _lerp(p, q, t):
    return tuple(p[k] + (q[k] - p[k]) * t for k in range(3))


def _prism(name, bottom, top, mat, sub=(1, 1), group="body", top_mat=None):
    """Hexahedron from two quads. sub=(nu, nv) subdivides bottom/top faces (u: p0->p3, v: p0->p1)."""
    verts, faces, mats = [], [], []

    def grid(quad):
        p0, p1, p2, p3 = quad
        nu, nv = sub
        base = len(verts)
        for i in range(nu + 1):
            left = _lerp(p0, p3, i / nu)
            right = _lerp(p1, p2, i / nu)
            for j in range(nv + 1):
                verts.append(_lerp(left, right, j / nv))
        for i in range(nu):
            for j in range(nv):
                a = base + i * (nv + 1) + j
                faces.append((a, a + 1, a + nv + 2, a + nv + 1))

    grid(bottom)
    mats.extend([mat] * len(faces))
    n0 = len(faces)
    grid(top)
    mats.extend([top_mat or mat] * (len(faces) - n0))
    # side walls (corner verts of each grid)
    nu, nv = sub
    stride = (nu + 1) * (nv + 1)

    def corner(g, i, j):
        return g * stride + i * (nv + 1) + j

    for (ia, ja), (ib, jb) in [((0, 0), (0, nv)), ((0, nv), (nu, nv)), ((nu, nv), (nu, 0)), ((nu, 0), (0, 0))]:
        faces.append((corner(0, ia, ja), corner(0, ib, jb), corner(1, ib, jb), corner(1, ia, ja)))
        mats.append(mat)
    return dict(name=name, group=group, smooth=False, verts=verts, faces=faces, mats=mats)


def _box(name, x0, x1, y0, y1, z0, z1, mat, group="body"):
    b = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)]
    t = [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    return _prism(name, b, t, mat, group=group)


def _wheel(name, cx, cy, cz, r, w, n, mat, group="gear"):
    verts, faces, mats = [], [], []
    for side in (-0.5, 0.5):
        for k in range(n):
            a = 2 * math.pi * k / n
            verts.append((cx + r * math.cos(a), cy + side * w, cz + r * math.sin(a)))
    for k in range(n):
        k2 = (k + 1) % n
        faces.append((k, k2, n + k2, n + k))
        mats.append(mat)
    faces.append(tuple(range(n)))
    faces.append(tuple(range(2 * n - 1, n - 1, -1)))
    mats.extend([mat, mat])
    return dict(name=name, group=group, smooth=False, verts=verts, faces=faces, mats=mats)


def _fuselage_profile(x):
    if x > 10:
        r = R_BODY * math.sqrt(max(0.0, 1 - ((x - 10) / 10) ** 2))
        zo = -0.25 * ((x - 10) / 10) ** 2
    elif x >= -8:
        r, zo = R_BODY, 0.0
    else:
        u = (-8 - x) / 12
        r = R_BODY * (1 - u ** 1.8) ** 0.55
        zo = 1.7 * u ** 2
    return r, zo


def build(detail="high"):
    hi = detail == "high"
    n_ring = 32 if hi else 16
    n_st = 72 if hi else 40
    parts = []

    # fuselage: white, blue cheat-line, grey belly, dark cockpit glass
    def fus_mat(xm, th):
        if 13.0 < xm < 16.6 and abs(th - math.pi / 2) < 0.8:
            return "glass"
        if -12 < xm < 12 and (2 * math.pi - 0.55 <= th <= 2 * math.pi - 0.2 or math.pi + 0.2 <= th <= math.pi + 0.55):
            return "blue"
        if math.pi + 0.55 < th < 2 * math.pi - 0.55:
            return "belly"
        return "white"

    xs = [-20 + 40 * i / (n_st - 1) for i in range(n_st)]
    parts.append(_loft("fuselage", xs, lambda x: _fuselage_profile(x)[0], lambda x: _fuselage_profile(x)[1], fus_mat, n_ring))

    # cabin windows: single flat quads on both sides
    wv, wf, wm = [], [], []
    for k in range(25):
        x = -10.0 + 0.85 * k
        for s in (1, -1):
            y = s * (2.03 + 0.05)
            i0 = len(wv)
            wv += [(x - 0.22, y, 0.33), (x + 0.22, y, 0.33), (x + 0.22, y, 0.63), (x - 0.22, y, 0.63)]
            wf.append((i0, i0 + 1, i0 + 2, i0 + 3))
            wm.append("glass")
    parts.append(dict(name="windows", group="body", smooth=False, verts=wv, faces=wf, mats=wm))

    # wings (swept, low, dihedral) + winglets
    sub = (4, 2) if not hi else (6, 3)
    for s, tag in ((1, "R"), (-1, "L")):
        rl, rt = (4.0, s * 1.6, -0.9), (-5.0, s * 1.6, -0.9)
        tt, tl = (-9.5, s * 17.4, 0.9), (-6.5, s * 17.4, 0.9)
        bot = [(p[0], p[1], p[2] - 0.35 * (1.0 if p is rl or p is rt else 0.2)) for p in (rl, rt, tt, tl)]
        top = [(p[0], p[1], p[2] + 0.35 * (1.0 if p is rl or p is rt else 0.2)) for p in (rl, rt, tt, tl)]
        if s < 0:
            bot, top = bot[::-1], top[::-1]  # keep u/v grids consistent for the mirrored wing
        parts.append(_prism("wing" + tag, bot, top, "belly", sub=sub, top_mat="white"))
        x0, x1 = -6.5, -9.5
        parts.append(
            _prism(
                "winglet" + tag,
                [(x0, s * 17.3, 1.0), (x1, s * 17.3, 1.0), (-9.6, s * 17.3, 3.0), (-8.3, s * 17.3, 3.0)],
                [(x0, s * 17.6, 1.0), (x1, s * 17.6, 1.0), (-9.6, s * 17.6, 3.0), (-8.3, s * 17.6, 3.0)],
                "blue",
            )
        )
        # engine nacelle + pylon
        cx, cy, cz = 0.7, s * 6.5, -1.9

        def eng_r(x):
            if x > 2.2:
                return 1.2 - 0.12 * ((x - 2.2) / 0.7) ** 2
            if x >= 0.0:
                return 1.2
            return 1.2 * (1 - 0.42 * ((-x) / 1.6) ** 1.5)

        exs = [-1.6 + 4.5 * i / (13 if hi else 9) for i in range(14 if hi else 10)]
        parts.append(
            _loft("engine" + tag, exs, eng_r, lambda x: 0.0, lambda xm, th: "engine", 24 if hi else 12,
                  centre=(cx - 0.7 + 0.0, cy, cz), caps=[(0, "dark"), (-1, "dark")])
        )
        parts.append(_box("pylon" + tag, -0.9, 2.3, s * 6.4, s * 6.6, -1.0, -0.2, "white"))
        # nav light on the wing tip (red left, green right)
        lx = -8.0
        parts.append(_box("navlight" + tag, lx - 0.15, lx + 0.15, s * 17.6 - 0.15 * s, s * 17.6 + 0.15 * s, 0.85, 1.15,
                          "nav_green" if s > 0 else "nav_red"))

    # vertical fin (blue) and horizontal stabilisers
    parts.append(
        _prism("fin", [(-11.0, -0.15, 1.9), (-19.0, -0.15, 2.0), (-20.5, -0.15, 9.0), (-15.5, -0.15, 9.0)],
               [(-11.0, 0.15, 1.9), (-19.0, 0.15, 2.0), (-20.5, 0.15, 9.0), (-15.5, 0.15, 9.0)], "blue")
    )
    parts.append(_box("navtail", -20.7, -20.3, -0.12, 0.12, 8.6, 8.9, "nav_white"))
    for s, tag in ((1, "R"), (-1, "L")):
        rl, rt = (-15.0, s * 0.8, 1.0), (-19.5, s * 0.8, 1.0)
        tt, tl = (-20.0, s * 7.0, 1.5), (-17.5, s * 7.0, 1.5)
        bot = [(p[0], p[1], p[2] - 0.12) for p in (rl, rt, tt, tl)]
        top = [(p[0], p[1], p[2] + 0.12) for p in (rl, rt, tt, tl)]
        if s < 0:
            bot, top = bot[::-1], top[::-1]
        parts.append(_prism("stab" + tag, bot, top, "white", sub=(2, 2) if not hi else (3, 2)))

    # landing gear (retracts): two main legs with twin wheels, nose leg
    n_w = 14 if hi else 10
    for s, tag in ((1, "R"), (-1, "L")):
        parts.append(_box("strut" + tag, -2.1, -1.9, s * 3.5, s * 3.7, -3.5, -0.9, "gear", group="gear"))
        for k in (-0.4, 0.4):
            parts.append(_wheel("wheel%s%d" % (tag, int(k * 10)), -2.0, s * 3.6 + k, -3.5, 0.7, 0.35, n_w, "dark"))
    parts.append(_box("nose_strut", 12.4, 12.6, -0.1, 0.1, -3.6, -1.9, "gear", group="gear"))
    for k in (-0.3, 0.3):
        parts.append(_wheel("nosewheel%d" % int(k * 10), 12.5, k, -3.6, 0.6, 0.3, n_w, "dark"))
    return parts


if __name__ == "__main__":
    for d in ("high", "low"):
        ps = build(d)
        print(d, len(ps), "parts", sum(len(p["faces"]) for p in ps), "faces")


def flight_table(duration=10.0, dt=0.002):
    """Shared kinematics: list of (x, z, pitch_rad, gear_scale) per dt. Metres; 0 -> 80 m/s roll, rotate at 6.2 s, lift-off ~7 s."""
    def smooth(a, b, t):
        u = min(1.0, max(0.0, (t - a) / (b - a)))
        return u * u * (3 - 2 * u)

    out, x, z = [], 0.0, 0.0
    for k in range(int(duration / dt) + 1):
        t = k * dt
        v = 11.4 * t if t < 7.0 else 11.4 * 7.0 + 4.0 * (t - 7.0)
        gamma = math.radians(11.0) * smooth(7.0, 9.2, t)
        out.append((x, z, math.radians(13.0) * smooth(6.2, 8.2, t), max(0.001, 1.0 - smooth(8.4, 9.1, t))))
        x += v * math.cos(gamma) * dt
        z += v * math.sin(gamma) * dt
    return out
