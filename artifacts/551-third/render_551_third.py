"""Review renders for the 551 Third Street asset.

Always renders the file that ships: the GLB is re-imported into a fresh scene,
so what you look at is what the app will load.

    blender -b --python render_551_third.py -- --glb 551-third.glb --outdir .
"""

import argparse
import math
import os
import sys

import bpy
import mathutils

SAMPLES = 32
ENGINE = "BLENDER_EEVEE"
RES = 1100


def fresh(glb):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)
    objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    mn = [1e9] * 3
    mx = [-1e9] * 3
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ mathutils.Vector(c)
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    return objs, mn, mx


def setup(night=False):
    sc = bpy.context.scene
    sc.render.engine = ENGINE
    if ENGINE == "CYCLES":
        sc.cycles.device = "CPU"
        sc.cycles.samples = SAMPLES
        sc.cycles.use_denoising = True
    else:
        sc.eevee.taa_render_samples = SAMPLES
        sc.eevee.use_shadows = True
    sc.render.resolution_x = RES
    sc.render.resolution_y = RES
    sc.render.film_transparent = False
    world = bpy.data.worlds.new("W")
    sc.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    if night:
        bg.inputs[0].default_value = (0.020, 0.026, 0.042, 1)
        bg.inputs[1].default_value = 1.0
    else:
        bg.inputs[0].default_value = (0.86, 0.83, 0.76, 1)
        bg.inputs[1].default_value = 1.0

    sun_data = bpy.data.lights.new("Sun", type="SUN")
    sun_data.energy = 0.35 if night else 3.4
    sun_data.angle = math.radians(6)
    sun = bpy.data.objects.new("Sun", sun_data)
    bpy.context.scene.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(52), 0, math.radians(-135 if not night else -60))

    if night:
        for m in bpy.data.materials:
            if not m.use_nodes:
                continue
            bsdf = m.node_tree.nodes.get("Principled BSDF")
            if not bsdf:
                continue
            if m.name.endswith("_Glow"):
                # glTF writes emissiveFactor 0, so drive emission from Base Color
                bsdf.inputs["Emission Color"].default_value = bsdf.inputs[
                    "Base Color"
                ].default_value
                bsdf.inputs["Emission Strength"].default_value = 1.0


def add_camera(name, loc, look, ortho_scale=None):
    cd = bpy.data.cameras.new(name)
    if ortho_scale:
        cd.type = "ORTHO"
        cd.ortho_scale = ortho_scale
    else:
        cd.lens = 85
    cam = bpy.data.objects.new(name, cd)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = loc
    d = mathutils.Vector(look) - mathutils.Vector(loc)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    return cam


def render(path):
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb", default="551-third.glb")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--only", default="")
    args = ap.parse_args(argv)

    objs, mn, mx = fresh(args.glb)
    cx, cy = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2
    cz = (mn[2] + mx[2]) / 2
    span = max(mx[0] - mn[0], mx[1] - mn[1])
    print(f"[render] dims={[round(mx[i]-mn[i],2) for i in range(3)]} minz={round(mn[2],3)}")

    setup(night=False)
    o = os.path.abspath(args.outdir)
    R = span * 0.62

    # The lot sits on the 45-degree SoMa grid, so a true-cardinal orthographic
    # camera sees every face obliquely and none of them square on.  The four
    # required elevations are therefore aimed along the SITE axes and labelled
    # with the true bearing they look from (see REPORT.md).
    def eye(bearing, dist=90):
        b = math.radians(bearing)
        return (cx + dist * math.sin(b), cy + dist * math.cos(b), cz + 2)

    views = {
        "top": ((cx, cy, mx[2] + 60), (cx, cy, cz), span * 1.1),
        "south": (eye(225), (cx, cy, cz), span * 1.02),  # 3rd Street front, SW
        "north": (eye(45), (cx, cy, cz), span * 1.02),   # rear, NE
        "west": (eye(315), (cx, cy, cz), span * 1.02),   # side toward South Park
        "east": (eye(135), (cx, cy, cz), span * 1.02),   # side toward Brannan
    }
    for name, (loc, look, sc) in views.items():
        if args.only and args.only != name:
            continue
        for c in [x for x in bpy.context.scene.objects if x.type == "CAMERA"]:
            bpy.data.objects.remove(c, do_unlink=True)
        add_camera(name, loc, look, ortho_scale=sc)
        render(os.path.join(o, f"551-third-{name}.png"))

    # high three-quarter aerial, the style bible's judging camera
    if not args.only or args.only == "aerial":
        for c in [x for x in bpy.context.scene.objects if x.type == "CAMERA"]:
            bpy.data.objects.remove(c, do_unlink=True)
        az, el = math.radians(215), math.radians(38)
        d = span * 2.4
        add_camera(
            "aerial",
            (cx + d * math.cos(el) * math.sin(az), cy + d * math.cos(el) * math.cos(az), cz + d * math.sin(el)),
            (cx, cy, cz + 1.5),
        )
        render(os.path.join(o, "551-third-aerial.png"))

    if not args.only or args.only == "night":
        objs, mn, mx = fresh(args.glb)
        setup(night=True)
        # A canopy soffit is only visible from below eye level, which the app's
        # 30-50 degree camera never reaches — so the night hero is the fascia
        # lightbar ring read from above, and this render shows that.
        az, el = math.radians(212), math.radians(27)
        d = span * 2.15
        add_camera(
            "night",
            (cx + d * math.cos(el) * math.sin(az), cy + d * math.cos(el) * math.cos(az), cz + d * math.sin(el)),
            (cx, cy, cz + 0.8),
        )
        render(os.path.join(o, "551-third-night.png"))


if __name__ == "__main__":
    main()
