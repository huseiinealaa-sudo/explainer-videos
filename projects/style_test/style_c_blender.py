"""Style C: headless Blender (bpy, Cycles CPU) - airliner takeoff at sunset. One attempt, 15-minute budget.

Run through run_c.sh (installs bpy, enforces the hard limit, encodes). Needs env C_WORK and C_START_EPOCH.
The renderer picks (fps, samples) from a timed test frame so that the whole attempt fits the budget.
"""
import json
import math
import os
import random
import sys
import time

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import airliner_geom  # noqa: E402

WORK = os.environ["C_WORK"]
T_START = float(os.environ["C_START_EPOCH"])
BUDGET = 900.0 - 60.0  # keep 60 s for encoding
FRAMES = os.path.join(WORK, "frames")
os.makedirs(FRAMES, exist_ok=True)
DURATION = 10.0
W, H = 1280, 720
SUN = Vector((1.0, 0.47, 0.115)).normalized()  # direction towards the sun (ahead of the plane, far side)
FILL = Vector((-0.25, -1.0, 0.35)).normalized()  # cool fill from the camera side


def lin(hexstr):
    h = hexstr.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)


def log(msg):
    print("[C %6.1fs] %s" % (time.time() - T_START, msg), flush=True)


# ------------------------------------------------------------------ scene, render settings
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = W, H, 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.render.use_persistent_data = True
scene.cycles.max_bounces = 4
scene.cycles.diffuse_bounces, scene.cycles.glossy_bounces = 2, 3
scene.cycles.use_adaptive_sampling = True
for attr, val in (("use_denoising", True), ("denoiser", "OPENIMAGEDENOISE")):
    try:
        setattr(scene.cycles, attr, val)
    except Exception as exc:  # noqa: BLE001
        log("denoise setting skipped: %s" % exc)
for vt in ("AgX", "Filmic", "Standard"):
    try:
        scene.view_settings.view_transform = vt
        break
    except Exception:  # noqa: BLE001
        continue


# ------------------------------------------------------------------ materials
def material(name, color, rough=0.5, metal=0.0, emit=None, strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*lin(color), 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        for key in ("Emission Color", "Emission"):
            if key in b.inputs:
                b.inputs[key].default_value = (*lin(emit), 1)
                break
        b.inputs["Emission Strength"].default_value = strength
    return m


MATS = {
    "white": material("white", "#f1eeee", 0.22),
    "blue": material("blue", "#2b7bd6", 0.3),
    "belly": material("belly", "#c6c3cf", 0.35),
    "engine": material("engine", "#d6d4da", 0.3, 0.5),
    "glass": material("glass", "#0b0f1a", 0.05),
    "dark": material("dark", "#0a0a0e", 0.8),
    "gear": material("gear", "#8b8b96", 0.4, 0.6),
    "nav_red": material("nav_red", "#ff2020", 0.3, emit="#ff2020", strength=60),
    "nav_green": material("nav_green", "#20ff60", 0.3, emit="#20ff60", strength=60),
    "nav_white": material("nav_white", "#ffffff", 0.3, emit="#ffffff", strength=60),
}


def mesh_object(name, verts, faces, mat_slots=None, face_mats=None, smooth=False, parent=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    for m in mat_slots or []:
        me.materials.append(m)
    if face_mats is not None:
        for p, mi in zip(me.polygons, face_mats):
            p.material_index = mi
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    scene.collection.objects.link(ob)
    if parent is not None:
        ob.parent = parent
    return ob


def recalc_normals(ob):
    import bmesh

    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(ob.data)
    bm.free()


def box(name, cx, cy, cz, sx, sy, sz, mat):
    x0, x1, y0, y1, z0, z1 = cx - sx / 2, cx + sx / 2, cy - sy / 2, cy + sy / 2, cz - sz / 2, cz + sz / 2
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    ob = mesh_object(name, v, f, [mat])
    recalc_normals(ob)
    return ob


# ------------------------------------------------------------------ world: sunset gradient + glow
world = bpy.data.worlds.new("Sunset")
scene.world = world
world.use_nodes = True
nt = world.node_tree
nt.nodes.clear()
N = nt.nodes.new
tc = N("ShaderNodeTexCoord")
sep = N("ShaderNodeSeparateXYZ")
mr = N("ShaderNodeMapRange")
mr.inputs["From Min"].default_value, mr.inputs["From Max"].default_value = 0.0, 0.75
mr.clamp = True
ramp = N("ShaderNodeValToRGB")
stops = [(0.0, "#ffb45e"), (0.06, "#ff7a45"), (0.16, "#d1467f"), (0.35, "#6b2f8f"), (0.65, "#2a1b66"), (1.0, "#0d1236")]
ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[0].color = stops[0][0], (*lin(stops[0][1]), 1)
ramp.color_ramp.elements[1].position, ramp.color_ramp.elements[1].color = stops[-1][0], (*lin(stops[-1][1]), 1)
for pos, col in stops[1:-1]:
    el = ramp.color_ramp.elements.new(pos)
    el.color = (*lin(col), 1)
bg1 = N("ShaderNodeBackground")
dot = N("ShaderNodeVectorMath")
dot.operation = "DOT_PRODUCT"
dot.inputs[1].default_value = SUN
mr2 = N("ShaderNodeMapRange")
mr2.inputs["From Min"].default_value, mr2.inputs["From Max"].default_value = 0.82, 1.0
mr2.clamp = True
pw = N("ShaderNodeMath")
pw.operation = "POWER"
pw.inputs[1].default_value = 2.2
glow = N("ShaderNodeMath")
glow.operation = "MULTIPLY"
glow.inputs[1].default_value = 5.0
bg2 = N("ShaderNodeBackground")
bg2.inputs["Color"].default_value = (*lin("#ff9a48"), 1)
add = N("ShaderNodeAddShader")
out = N("ShaderNodeOutputWorld")
L = nt.links.new
L(tc.outputs["Generated"], sep.inputs["Vector"])
L(sep.outputs["Z"], mr.inputs["Value"])
L(mr.outputs["Result"], ramp.inputs["Fac"])
L(ramp.outputs["Color"], bg1.inputs["Color"])
L(tc.outputs["Generated"], dot.inputs[0])
L(dot.outputs["Value"], mr2.inputs["Value"])
L(mr2.outputs["Result"], pw.inputs[0])
L(pw.outputs["Value"], glow.inputs[0])
L(glow.outputs["Value"], bg2.inputs["Strength"])
L(bg1.outputs["Background"], add.inputs[0])
L(bg2.outputs["Background"], add.inputs[1])
L(add.outputs["Shader"], out.inputs["Surface"])

# lights: low warm sun (key), cool fill from the camera side, visible sun disc
for name, vec, color, energy, angle in (("Sun", SUN, "#ff8a3c", 5.5, 0.03), ("Fill", FILL, "#c778b8", 1.6, 0.35)):
    ld = bpy.data.lights.new(name, "SUN")
    ld.color, ld.energy, ld.angle = lin(color), energy, angle
    lo = bpy.data.objects.new(name, ld)
    scene.collection.objects.link(lo)
    lo.rotation_euler = (-vec).to_track_quat("-Z", "Y").to_euler()
bpy.ops.mesh.primitive_uv_sphere_add(radius=150, segments=24, ring_count=12, location=tuple(6000 * SUN))
sun_disc = bpy.context.active_object
sun_disc.data.materials.append(material("sun", "#ffd9a0", 1.0, emit="#ffb060", strength=40))

# ------------------------------------------------------------------ ground, runway, scenery
ground = mesh_object("Ground", [(-9000, -9000, -0.05), (9000, -9000, -0.05), (9000, 9000, -0.05), (-9000, 9000, -0.05)],
                     [(0, 1, 2, 3)], [material("ground", "#1c1a12", 0.95)])

rw_len, rw_w, rw_cx = 1900.0, 45.0, 600.0
rv = [(rw_cx - rw_len / 2, -rw_w / 2, 0), (rw_cx + rw_len / 2, -rw_w / 2, 0), (rw_cx + rw_len / 2, rw_w / 2, 0), (rw_cx - rw_len / 2, rw_w / 2, 0)]
rm = bpy.data.materials.new("runway")
rm.use_nodes = True
rn = rm.node_tree.nodes
rb = rn["Principled BSDF"]
rb.inputs["Roughness"].default_value = 0.38
tco = rn.new("ShaderNodeTexCoord")
sx = rn.new("ShaderNodeSeparateXYZ")
shift = rn.new("ShaderNodeMath"); shift.operation = "ADD"; shift.inputs[1].default_value = 1000.0
mod = rn.new("ShaderNodeMath"); mod.operation = "MODULO"; mod.inputs[1].default_value = 50.0
lt = rn.new("ShaderNodeMath"); lt.operation = "LESS_THAN"; lt.inputs[1].default_value = 30.0
ay = rn.new("ShaderNodeMath"); ay.operation = "ABSOLUTE"
ay_lt = rn.new("ShaderNodeMath"); ay_lt.operation = "LESS_THAN"; ay_lt.inputs[1].default_value = 0.45
dash = rn.new("ShaderNodeMath"); dash.operation = "MULTIPLY"
ay_gt = rn.new("ShaderNodeMath"); ay_gt.operation = "GREATER_THAN"; ay_gt.inputs[1].default_value = 21.2
ay_lt2 = rn.new("ShaderNodeMath"); ay_lt2.operation = "LESS_THAN"; ay_lt2.inputs[1].default_value = 21.8
edge = rn.new("ShaderNodeMath"); edge.operation = "MULTIPLY"
paint = rn.new("ShaderNodeMath"); paint.operation = "ADD"; paint.use_clamp = True
noise = rn.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 0.35
paint_col = rn.new("ShaderNodeVectorMath"); paint_col.operation = "SCALE"
paint_col.inputs[0].default_value = lin("#d8d2cc")
mix = rn.new("ShaderNodeVectorMath"); mix.operation = "ADD"
asphalt = rn.new("ShaderNodeValToRGB")
asphalt.color_ramp.elements[0].color = (*lin("#2b2733"), 1)
asphalt.color_ramp.elements[1].color = (*lin("#3c3645"), 1)
rl = rm.node_tree.links.new
rl(tco.outputs["Object"], sx.inputs["Vector"])
rl(sx.outputs["X"], shift.inputs[0]); rl(shift.outputs["Value"], mod.inputs[0]); rl(mod.outputs["Value"], lt.inputs[0])
rl(sx.outputs["Y"], ay.inputs[0]); rl(ay.outputs["Value"], ay_lt.inputs[0])
rl(lt.outputs["Value"], dash.inputs[0]); rl(ay_lt.outputs["Value"], dash.inputs[1])
rl(ay.outputs["Value"], ay_gt.inputs[0]); rl(ay.outputs["Value"], ay_lt2.inputs[0])
rl(ay_gt.outputs["Value"], edge.inputs[0]); rl(ay_lt2.outputs["Value"], edge.inputs[1])
rl(dash.outputs["Value"], paint.inputs[0]); rl(edge.outputs["Value"], paint.inputs[1])
rl(tco.outputs["Object"], noise.inputs["Vector"]); rl(noise.outputs["Fac"], asphalt.inputs["Fac"])
rl(paint.outputs["Value"], paint_col.inputs["Scale"])
rl(asphalt.outputs["Color"], mix.inputs[0]); rl(paint_col.outputs["Vector"], mix.inputs[1])
rl(mix.outputs["Vector"], rb.inputs["Base Color"])
runway = mesh_object("Runway", rv, [(0, 1, 2, 3)], [rm])

# edge lights (shared mesh)
bpy.ops.mesh.primitive_ico_sphere_add(radius=0.35, subdivisions=1, location=(0, 0, 0.35))
lamp = bpy.context.active_object
lamp.data.materials.append(material("edgelight", "#ffd9a0", 0.5, emit="#ffc880", strength=30))
for side in (-1, 1):
    for k in range(-8, 40):
        dup = lamp.copy()
        dup.location = (k * 40.0, side * 24.5, 0.35)
        scene.collection.objects.link(dup)
scene.collection.objects.unlink(lamp)

# distant mountains (two hazy ridges) and airport buildings on the far side for depth
rng = random.Random(7)
for name, yy, hmax, col, em in (("ridge_far", 4600, 420, "#6d3f86", 0.9), ("ridge_near", 2900, 230, "#3a2358", 0.35)):
    nx, ny = 260, 6
    verts, faces = [], []
    for i in range(nx + 1):
        x = -3500 + 9000 * i / nx
        hgt = hmax * (0.55 + 0.25 * math.sin(i * 0.11 + yy) + 0.18 * math.sin(i * 0.37) + 0.12 * rng.random())
        for j in range(ny + 1):
            verts.append((x, yy + j * 60, -5 + hgt * (1 - (j / ny) ** 1.8)))
    for i in range(nx):
        for j in range(ny):
            a = i * (ny + 1) + j
            faces.append((a, a + 1, a + ny + 2, a + ny + 1))
    mm = material(name, col, 1.0, emit=col, strength=em)
    ob = mesh_object(name, verts, faces, [mm], smooth=True)
    recalc_normals(ob)

wall = material("wall", "#15121f", 0.8)
glass_em = material("glow_windows", "#ffcf7a", 0.4, emit="#ffbf60", strength=6)
box("terminal", 330, 250, 8, 260, 34, 16, wall)
box("terminal_windows", 330, 232.6, 8, 250, 0.3, 3.0, glass_em)
for i, hx in enumerate((-70, -10, 50)):
    box("hangar%d" % i, hx, 190, 10, 52, 44, 20, wall)
box("tower", 560, 170, 22, 9, 9, 44, wall)
box("tower_cab", 560, 170, 47, 16, 16, 7, glass_em)
for i in range(8):
    box("post%d" % i, 120 + i * 120, 120, 6, 0.6, 0.6, 12, wall)

# ------------------------------------------------------------------ the airliner
pivot = bpy.data.objects.new("pivot", None)
scene.collection.objects.link(pivot)
body = bpy.data.objects.new("body", None)
scene.collection.objects.link(body)
body.parent = pivot
body.location = (-airliner_geom.PIVOT[0], -airliner_geom.PIVOT[1], -airliner_geom.PIVOT[2])
GEAR0 = Vector((0, 0, -1.0))
gear = bpy.data.objects.new("gear", None)
scene.collection.objects.link(gear)
gear.parent = body
gear.location = GEAR0
for part in airliner_geom.build("high"):
    keys = list(dict.fromkeys(part["mats"]))
    ob = mesh_object(part["name"], part["verts"], part["faces"], [MATS[k] for k in keys],
                     [keys.index(k) for k in part["mats"]], smooth=part["smooth"])
    recalc_normals(ob)
    if part["group"] == "gear":
        ob.parent, ob.location = gear, -GEAR0
    else:
        ob.parent = body

# ------------------------------------------------------------------ motion
def smoothstep(a, b, t):
    u = min(1.0, max(0.0, (t - a) / (b - a)))
    return u * u * (3 - 2 * u)


ACC = 11.4
STATE = []  # (x, z, pitch) sampled at dt
x = z = 0.0
DT = 0.002
for k in range(int(DURATION / DT) + 1):
    t = k * DT
    v = ACC * t if t < 7.0 else ACC * 7.0 + 4.0 * (t - 7.0)
    gamma = math.radians(11.0) * smoothstep(7.0, 9.2, t)
    STATE.append((x, z, math.radians(13.0) * smoothstep(6.2, 8.2, t)))
    x += v * math.cos(gamma) * DT
    z += v * math.sin(gamma) * DT

cam_data = bpy.data.cameras.new("Cam")
cam_data.lens = 40
cam = bpy.data.objects.new("Cam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
target = bpy.data.objects.new("Target", None)
scene.collection.objects.link(target)
tr = cam.constraints.new("TRACK_TO")
tr.target, tr.track_axis, tr.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"


def pose(t):
    px, pz, pitch = STATE[min(int(round(t / DT)), len(STATE) - 1)]
    pivot.location = (px, 0.0, pz)
    pivot.rotation_euler = (0.0, -pitch, 0.0)
    g = max(0.001, 1.0 - smoothstep(8.4, 9.1, t))
    gear.scale = (g, g, g)
    centre = Matrix.Rotation(-pitch, 3, "Y") @ Vector((2.0, 0.0, 4.2)) + Vector((px, 0.0, pz))
    cam.location = (0.88 * centre.x - 25.0, -75.0 - 2.0 * t, 3.0 + 0.9 * t)
    target.location = (centre.x + 30.0, 0.0, centre.z * 0.85 + 5.0)


def render_frame(i, t):
    pose(t)
    scene.render.filepath = os.path.join(FRAMES, "f%04d.png" % i)
    bpy.ops.render.render(write_still=True)


# ------------------------------------------------------------------ timed test frame -> choose fps / samples
log("scene built; timing a test frame at 16 spp")
scene.cycles.samples = 16
t0 = time.time()
render_frame(9999, 6.4)
t_test = time.time() - t0
os.replace(os.path.join(FRAMES, "f9999.png"), os.path.join(WORK, "test_frame.png"))
avail = BUDGET - (time.time() - T_START)
log("test frame %.1f s, %.0f s available" % (t_test, avail))
choice = None
for fps, spp in ((24, 16), (16, 16), (12, 16), (12, 8), (8, 8)):
    est = fps * DURATION * t_test * (spp / 16.0) * 0.85  # adaptive sampling + persistent data
    if est <= avail:
        choice = (fps, spp, est)
        break
if choice is None:
    log("ABORT: even 8 fps / 8 spp does not fit the budget")
    json.dump(dict(status="over_budget", t_test=t_test, avail=avail), open(os.path.join(WORK, "render.json"), "w"))
    sys.exit(3)
fps, spp, est = choice
scene.cycles.samples = spp
n = int(fps * DURATION)
log("rendering %d frames at %d fps, %d spp (estimate %.0f s)" % (n, fps, spp, est))
t_r = time.time()
for i in range(n):
    render_frame(i, i / fps)
    if time.time() - T_START > BUDGET + 30:
        log("ABORT: budget exceeded at frame %d" % i)
        json.dump(dict(status="over_budget", frames_done=i, fps=fps), open(os.path.join(WORK, "render.json"), "w"))
        sys.exit(4)
json.dump(dict(status="ok", fps=fps, samples=spp, frames=n, t_test=t_test, render_s=time.time() - t_r, bpy=bpy.app.version_string),
          open(os.path.join(WORK, "render.json"), "w"))
log("render done")
