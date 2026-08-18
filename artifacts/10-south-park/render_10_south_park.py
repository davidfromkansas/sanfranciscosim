"""Controlled review renders of the exported 10 South Park GLB.

    blender -b --python render_10_south_park.py -- [--glb F] [--out DIR] [--cycles]

Renders the file that SHIPS (a fresh import of the GLB), never the build scene.

Four orthographic elevations sharing scale, framing, lighting and exposure, a
top view, a high three-quarter aerial over the south-south-east (both front
planes plus the courtyard), and a night aerial.

Engine: Workbench by default. The machine this repo is authored on runs many
Blender sessions at once and Cycles frames stop making progress above load ~300;
`.agents/skills/sf-asset-check/SKILL.md` sanctions Workbench, it renders flat
Toy_* colours faithfully, and it is deterministic. It CANNOT render emission, so
the night frame is always Cycles regardless of the flag — and its `_Glow`
materials are driven from Base Color, because glTF writes emissiveFactor = 0
when the authored strength is 0 and a re-imported _Glow otherwise renders as a
white slab (see the note at the end of docs/asset-plans/README.md).
"""

import math
import os
import sys

import bpy
from mathutils import Vector

ARGV = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []


def opt(key, default=None):
    return ARGV[ARGV.index(key) + 1] if key in ARGV else default


HERE = os.path.dirname(os.path.abspath(__file__))
GLB = opt("--glb", os.path.join(HERE, "10-south-park.glb"))
OUT = opt("--out", HERE)
PREFIX = "10-south-park"
CYCLES = "--cycles" in ARGV

RES = (1400, 1000)
BG = (0.902, 0.882, 0.847, 1.0)


def clear():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for block in (bpy.data.meshes, bpy.data.cameras, bpy.data.lights, bpy.data.materials):
        for item in list(block):
            block.remove(item)


def load():
    bpy.ops.import_scene.gltf(filepath=GLB)
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    return objs, mn, mx


def world():
    w = bpy.data.worlds.new("w")
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = BG
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.85
    bpy.context.scene.world = w


def sun(elev=52.0, azim=35.0, energy=3.0):
    d = bpy.data.lights.new("sun", "SUN")
    d.energy = energy
    d.angle = 0.10
    o = bpy.data.objects.new("sun", d)
    bpy.context.collection.objects.link(o)
    o.rotation_euler = (math.radians(90.0 - elev), 0.0, math.radians(azim))
    return o


def engine(night=False):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    if night or CYCLES:
        sc.render.engine = "CYCLES"
        sc.cycles.device = "CPU"
        sc.cycles.samples = 48 if night else 64
        sc.cycles.use_denoising = True
    else:
        sc.render.engine = "BLENDER_WORKBENCH"
        sd = sc.display.shading
        sd.light, sd.color_type = "STUDIO", "MATERIAL"
        sd.show_shadows = True
        sd.show_cavity = True
        sd.cavity_type = "BOTH"
        sc.display.render_aa = "16"


def camera(ctr, bearing, pitch, dist, lens=None, ortho_scale=None):
    d = bpy.data.cameras.new("cam")
    if ortho_scale:
        d.type = "ORTHO"
        d.ortho_scale = ortho_scale
    else:
        d.lens = lens or 85.0
    cam = bpy.data.objects.new("cam", d)
    bpy.context.collection.objects.link(cam)
    br, pr = math.radians(bearing), math.radians(pitch)
    cam.location = ctr + Vector(
        (math.sin(br) * math.cos(pr) * dist,
         math.cos(br) * math.cos(pr) * dist,
         math.sin(pr) * dist)
    )
    cam.rotation_euler = (ctr - cam.location).normalized().to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    return cam


def shoot(name):
    path = os.path.join(OUT, f"{PREFIX}-{name}.png")
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print(f"[render] wrote {path}")


def glow_from_base():
    """glTF writes emissiveFactor = 0 when the authored emission strength is 0, so
    a re-imported _Glow material carries a DEFAULT WHITE emission. Copy Base Color
    into Emission Color at strength 1.0 — which is also exactly what the app does,
    since its night layer is an unlit overlay at the material's own baked colour."""
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if not bsdf:
            continue
        if mat.name.endswith("_Glow"):
            base = bsdf.inputs["Base Color"].default_value
            bsdf.inputs["Emission Color"].default_value = base
            bsdf.inputs["Emission Strength"].default_value = 1.0
        elif "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = 0.0


def main():
    os.makedirs(OUT, exist_ok=True)
    clear()
    objs, mn, mx = load()
    ctr = (mn + mx) / 2.0
    span = max((mx - mn)[i] for i in range(2))
    print(f"[render] imported {len(objs)} objects, dims "
          f"{[round((mx - mn)[i], 3) for i in range(3)]}")

    world()
    sun()
    engine()

    # four elevations, one shared orthographic scale and one shared light
    ground = Vector((ctr.x, ctr.y, (mn.z + mx.z) / 2.0))
    for name, bearing in (("north", 0.0), ("east", 90.0), ("south", 180.0), ("west", 270.0)):
        for c in [o for o in bpy.data.objects if o.type == "CAMERA"]:
            bpy.data.objects.remove(c, do_unlink=True)
        camera(ground, bearing, 0.0, span * 2.0, ortho_scale=span * 1.12)
        shoot(name)

    for c in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(c, do_unlink=True)
    # A true nadir, north up: build the camera by hand rather than via camera(),
    # because a track-quat at 89.9 deg pitch resolves its up vector to SOUTH and
    # silently renders the plan upside down.
    d = bpy.data.cameras.new("cam")
    d.type = "ORTHO"
    d.ortho_scale = span * 1.08
    cam = bpy.data.objects.new("cam", d)
    bpy.context.collection.objects.link(cam)
    cam.location = Vector((ctr.x, ctr.y, mx.z + span))
    cam.rotation_euler = (0.0, 0.0, 0.0)
    bpy.context.scene.camera = cam
    shoot("top")

    # the app's camera: 30-50 degrees down, long lens, over the south-south-east
    for c in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(c, do_unlink=True)
    camera(ctr, 158.0, 34.0, span * 2.6, lens=58.0)
    shoot("aerial")

    # the facade, straight onto the bowed hero plane
    for c in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(c, do_unlink=True)
    front = Vector((ctr.x + 7.5, ctr.y - 8.5, ctr.z - 1.0))
    camera(front, 182.0, 12.0, span * 1.15, lens=78.0)
    shoot("facade")

    # night
    glow_from_base()
    engine(night=True)
    for lamp in [o for o in bpy.data.objects if o.type == "LIGHT"]:
        bpy.data.objects.remove(lamp, do_unlink=True)
    w = bpy.context.scene.world
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.035, 0.042, 0.062, 1.0)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.55
    sun(elev=28.0, azim=200.0, energy=0.22)
    for c in [o for o in bpy.data.objects if o.type == "CAMERA"]:
        bpy.data.objects.remove(c, do_unlink=True)
    camera(ctr, 158.0, 34.0, span * 2.6, lens=58.0)
    shoot("aerial-night")


if __name__ == "__main__":
    main()
