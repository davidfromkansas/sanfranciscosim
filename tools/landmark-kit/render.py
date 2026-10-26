"""Review renders + contact sheet for a landmark GLB (Transbay batch).

    blender -b --python tools/landmark-kit/render.py -- --glb FILE --out DIR
        --prefix SLUG [--samples 32] [--only aerial,night]

Always renders the EXPORTED asset re-imported into an empty scene. Four
orthographic elevations from true compass directions (north = +Y) share one
rig; the top view shows the roof; the aerial is the app's high three-quarter
camera (38 degrees down, long lens); the night aerial lights the `_Glow`
materials the way the app's dusk pass does. By day `_Glow` faces are hidden,
because the app renders them almost fully transparent in daylight.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

BG = (0.86, 0.80, 0.69, 1.0)
NIGHT_BG = (0.035, 0.045, 0.09, 1.0)


def import_glb(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    mn = Vector((1e9,) * 3)
    mx = Vector((-1e9,) * 3)
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    return objs, mn, mx


def set_glow(mode):
    """mode: 'hide' (day) or 'emit' (night)."""
    for m in bpy.data.materials:
        if not m.name.endswith("_Glow") or not m.use_nodes:
            continue
        nt = m.node_tree
        out = [n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"][0]
        bsdf = nt.nodes.get("Principled BSDF")
        if mode == "hide":
            tr = nt.nodes.get("DayHide") or nt.nodes.new("ShaderNodeBsdfTransparent")
            tr.name = "DayHide"
            nt.links.new(tr.outputs[0], out.inputs[0])
        else:
            nt.links.new(bsdf.outputs[0], out.inputs[0])
            bsdf.inputs["Emission Color"].default_value = bsdf.inputs["Base Color"].default_value
            bsdf.inputs["Emission Strength"].default_value = 1.6


def setup(samples, night=False):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("Studio")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = NIGHT_BG if night else BG
    bg.inputs[1].default_value = 0.3 if night else 0.55
    for o in [o for o in bpy.data.objects if o.type == "LIGHT"]:
        bpy.data.objects.remove(o)
    sun = bpy.data.lights.new("Key", "SUN")
    sun.energy = 0.2 if night else 2.6
    sun.angle = math.radians(8)
    so = bpy.data.objects.new("Key", sun)
    sc.collection.objects.link(so)
    so.rotation_euler = (math.radians(42), 0, math.radians(150))


def ground(mn, mx, night=False):
    size = max(mx.x - mn.x, mx.y - mn.y, (mx.z - mn.z) * 0.6) * 6
    bpy.ops.mesh.primitive_plane_add(size=size, location=((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, -0.02))
    g = bpy.context.object
    g.name = "__ground"
    m = bpy.data.materials.new("__ground")
    m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.08, 0.08, 0.1, 1) if night else (0.36, 0.35, 0.33, 1)
    g.data.materials.append(m)


def camera(name, loc, target, ortho=None, lens=105):
    cam = bpy.data.cameras.new(name)
    if ortho:
        cam.type = "ORTHO"
        cam.ortho_scale = ortho
    else:
        cam.lens = lens
    cam.clip_end = 20000
    co = bpy.data.objects.new(name, cam)
    bpy.context.scene.collection.objects.link(co)
    d = (target - loc).normalized()
    co.location = loc
    co.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = co
    return co


def render(path, res):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

    def arg(f, d=None):
        return argv[argv.index(f) + 1] if f in argv else d

    glb, out, prefix = arg("--glb"), arg("--out"), arg("--prefix")
    samples = int(arg("--samples", "32"))
    only = arg("--only")
    only = set(only.split(",")) if only else None
    os.makedirs(out, exist_ok=True)
    objs, mn, mx = import_glb(glb)
    ctr = (mn + mx) / 2
    H = mx.z - mn.z
    W = max(mx.x - mn.x, mx.y - mn.y)
    ground(mn, mx)
    setup(samples)
    set_glow("hide")
    files = []

    tall = H > W * 1.1
    eres = (700, 1100) if tall else (1100, 800)
    oscale = max(H * 1.12, W * 1.12 * (eres[1] / eres[0])) if tall else max(W * 1.15, H * 1.12 * eres[0] / eres[1])
    tgt = Vector((ctr.x, ctr.y, mn.z + H / 2))
    for name, az in (("north", 0), ("east", 90), ("south", 180), ("west", 270)):
        if only and name not in only:
            continue
        a = math.radians(az)
        loc = tgt + Vector((math.sin(a), math.cos(a), 0)) * (W * 4 + 200)
        camera("cam_" + name, loc, tgt, ortho=oscale)
        p = os.path.join(out, f"{prefix}-{name}.png")
        render(p, eres)
        files.append(p)

    if not only or "top" in only:
        camera("cam_top", Vector((ctr.x, ctr.y, mx.z + 500)), Vector((ctr.x, ctr.y + 0.001, mn.z)),
               ortho=W * 1.25)
        p = os.path.join(out, f"{prefix}-top.png")
        render(p, (1000, 1000))
        files.append(p)

    def aerial(path, night):
        a, e = math.radians(215), math.radians(38)
        d = Vector((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e)))
        span = max(H, W * 1.4)
        dist = span * 3.2
        camera("cam_aerial", tgt + d * dist, tgt, lens=105)
        render(path, (1100, 1100) if tall else (1300, 1000))

    if not only or "aerial" in only:
        p = os.path.join(out, f"{prefix}-aerial.png")
        aerial(p, False)
        files.append(p)
    if not only or "night" in only:
        setup(samples, night=True)
        bpy.data.objects.remove(bpy.data.objects["__ground"])
        ground(mn, mx, night=True)
        set_glow("emit")
        p = os.path.join(out, f"{prefix}-aerial-night.png")
        aerial(p, True)
        files.append(p)

    if not only:
        contact_sheet(out, prefix)


def contact_sheet(out, prefix):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    names = ["aerial", "aerial-night", "top", "north", "east", "south", "west"]
    ims = []
    for n in names:
        p = os.path.join(out, f"{prefix}-{n}.png")
        if os.path.exists(p):
            ims.append((n, Image.open(p).convert("RGB")))
    if not ims:
        return
    th = 520
    tiles = []
    for n, im in ims:
        w = int(im.width * th / im.height)
        t = im.resize((w, th))
        ImageDraw.Draw(t).text((10, 8), n, fill=(30, 30, 30) if "night" not in n else (230, 230, 230))
        tiles.append(t)
    row1, row2 = tiles[:3], tiles[3:]
    W = max(sum(t.width for t in row1), sum(t.width for t in row2)) + 20
    sheet = Image.new("RGB", (W, th * (2 if row2 else 1) + 30), (245, 242, 236))
    x = 10
    for t in row1:
        sheet.paste(t, (x, 10))
        x += t.width
    x = 10
    for t in row2:
        sheet.paste(t, (x, th + 20))
        x += t.width
    sheet.save(os.path.join(out, f"{prefix}-contact-sheet.png"))


if __name__ == "__main__":
    main()
