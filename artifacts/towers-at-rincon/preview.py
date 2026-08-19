"""Fast Workbench turnarounds for build iteration (not a deliverable)."""
import math, os, sys
import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
here = os.path.dirname(os.path.abspath(__file__))
glb = os.path.join(here, "towers-at-rincon.glb")
out = os.path.join(here, "_preview")
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
mn = Vector((1e9,)*3); mx = Vector((-1e9,)*3)
for o in [o for o in bpy.data.objects if o.type == "MESH"]:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        for i in range(3):
            mn[i] = min(mn[i], w[i]); mx[i] = max(mx[i], w[i])
ctr = Vector(((mn.x+mx.x)/2, (mn.y+mx.y)/2, (mn.z+mx.z)/2))

# Workbench MATERIAL shading reads diffuse_color and the Standard view transform
# passes it straight through, so a linear value renders far too dark. Push the
# sRGB value into diffuse_color for the preview only.
def lin2srgb(c):
    return 12.92*c if c <= 0.0031308 else 1.055*(c**(1/2.4)) - 0.055
for m in bpy.data.materials:
    if not m.use_nodes: continue
    b = m.node_tree.nodes.get("Principled BSDF")
    if not b: continue
    c = b.inputs["Base Color"].default_value
    m.diffuse_color = (lin2srgb(c[0]), lin2srgb(c[1]), lin2srgb(c[2]), 1.0)
span = max(mx.x-mn.x, mx.y-mn.y, mx.z-mn.z)
sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sh = sc.display.shading
sh.light = "STUDIO"; sh.color_type = "MATERIAL"; sh.show_shadows = True
sh.show_cavity = True; sh.cavity_type = "BOTH"
sc.view_settings.view_transform = "Standard"
sc.render.film_transparent = False
sc.world = bpy.data.worlds.new("W"); sc.world.use_nodes = True
sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.86,0.80,0.69,1)

def cam(name):
    c = bpy.data.cameras.new(name); c.clip_start=0.5; c.clip_end=20000
    ob = bpy.data.objects.new(name, c); bpy.context.collection.objects.link(ob); return ob
def aim(ob, t):
    ob.rotation_euler = (t - ob.location).to_track_quat("-Z","Y").to_euler()
def shot(path, ob, res):
    sc.camera = ob; sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.filepath = path; bpy.ops.render.render(write_still=True); print("[prev]", path)

RAD = 3.1
for name, az, pitch in (("aerial", 90.0, 36.0), ("aerial2", 200.0, 30.0), ("street", 135.0, 8.0)):
    o = cam(name); o.data.lens = 78.0
    a, pr = math.radians(az), math.radians(pitch)
    o.location = Vector((ctr.x + span*RAD*math.cos(pr)*math.sin(a),
                         ctr.y + span*RAD*math.cos(pr)*math.cos(a),
                         ctr.z + span*RAD*math.sin(pr)))
    aim(o, Vector((ctr.x, ctr.y, ctr.z*0.9)))
    shot(os.path.join(out, f"{name}.png"), o, (1100, 850))

t = cam("top"); t.data.type = "ORTHO"; t.data.ortho_scale = span*1.12
t.location = Vector((ctr.x, ctr.y, mx.z + span)); t.rotation_euler = (0,0,math.radians(45.0))
shot(os.path.join(out, "top.png"), t, (1100, 1100))

e = cam("elev"); e.data.type = "ORTHO"; e.data.ortho_scale = span*1.12
a = math.radians(135.0)
e.location = Vector((ctr.x + span*3*math.sin(a), ctr.y + span*3*math.cos(a), ctr.z))
aim(e, ctr); shot(os.path.join(out, "howard.png"), e, (1100, 950))
