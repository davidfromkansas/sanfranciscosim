# Phase E A/B renders — run once per GLB:
#   "$BLENDER" -b --python render_ab.py -- <file.glb> <out_prefix>
# Produces: <prefix>_day_near.png  _day_far.png  _night_near.png  _night_far.png
#           <prefix>_elev_{n,e,s,w}.png   (day state, orthographic elevations)
# Landmark camera: 42 deg elevation aerial, near = 1.5x long axis, far = 6x.
import bpy, sys, math, contextlib, io
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
GLB, PREFIX = argv[0], argv[1]

RES = (960, 720)
FOV_DEG = 40.0
AZIMUTH = math.radians(80.0)   # compass ~10 deg: the street elevation, the
                               # blue gate and the taper all in one frame. The
                               # generic 45 deg looks straight down the blind
                               # east party flank, where nothing is at risk.
ELEV = math.radians(42.0)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]

mins = Vector((1e18,) * 3); maxs = Vector((-1e18,) * 3)
for o in objs:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        mins = Vector(map(min, mins, w)); maxs = Vector(map(max, maxs, w))
center = (mins + maxs) / 2
long_axis = max(maxs - mins)
NEAR, FAR = 1.5 * long_axis, 6.0 * long_axis

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 64
scene.cycles.use_denoising = False
scene.render.resolution_x, scene.render.resolution_y = RES
scene.render.film_transparent = True

cam_data = bpy.data.cameras.new("abcam")
cam_data.angle = math.radians(FOV_DEG)
cam_data.clip_start = 1.0
cam_data.clip_end = 50000.0  # far view of tall landmarks exceeds the 1 km default
cam = bpy.data.objects.new("abcam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam

def aim(dist, azimuth=AZIMUTH, elev=ELEV, ortho=None):
    off = Vector((math.cos(azimuth) * math.cos(elev),
                  math.sin(azimuth) * math.cos(elev),
                  math.sin(elev))) * dist
    cam.location = center + off
    d = (center - cam.location).normalized()
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    if ortho:
        cam_data.type = "ORTHO"
        cam_data.ortho_scale = ortho
    else:
        cam_data.type = "PERSP"

sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
scene.collection.objects.link(sun)
scene.world = bpy.data.worlds.new("w")
scene.world.use_nodes = True
wbg = scene.world.node_tree.nodes["Background"]

glow_mats = [m for m in bpy.data.materials if m.name.endswith("_Glow")]

def set_state(state):
    if state == "day":
        sun.data.energy = 4.0
        sun.data.color = (1.0, 0.96, 0.9)
        sun.rotation_euler = (math.radians(50), 0, math.radians(-120))
        wbg.inputs[0].default_value = (0.85, 0.88, 0.92, 1)
        wbg.inputs[1].default_value = 0.6
        for m in glow_mats:
            bsdf = m.node_tree.nodes.get("Principled BSDF")
            bsdf.inputs["Alpha"].default_value = 0.12
            bsdf.inputs["Emission Strength"].default_value = 0.0
            m.surface_render_method = "BLENDED"
    else:
        sun.data.energy = 0.15
        sun.data.color = (0.7, 0.78, 1.0)
        sun.rotation_euler = (math.radians(35), 0, math.radians(60))
        wbg.inputs[0].default_value = (0.02, 0.03, 0.06, 1)
        wbg.inputs[1].default_value = 0.4
        for m in glow_mats:
            bsdf = m.node_tree.nodes.get("Principled BSDF")
            bsdf.inputs["Alpha"].default_value = 1.0
            bsdf.inputs["Emission Color"].default_value = bsdf.inputs["Base Color"].default_value
            bsdf.inputs["Emission Strength"].default_value = 6.0
            m.surface_render_method = "BLENDED"

def shoot(path):
    scene.render.filepath = path
    with contextlib.redirect_stdout(io.StringIO()):
        bpy.ops.render.render(write_still=True)
    print("RENDERED", path)

for state in ("day", "night"):
    set_state(state)
    for dist, tag in ((NEAR, "near"), (FAR, "far")):
        aim(dist)
        shoot(f"{PREFIX}_{state}_{tag}.png")

# N/E/S/W orthographic elevations, day state (contact sheet inputs)
set_state("day")
scale = long_axis * 1.15
for az, tag in ((math.pi / 2, "n"), (0.0, "e"), (-math.pi / 2, "s"), (math.pi, "w")):
    aim(3 * long_axis, azimuth=az, elev=math.radians(2), ortho=scale)
    shoot(f"{PREFIX}_elev_{tag}.png")
print("RENDER-AB-DONE", NEAR, FAR)
