"""Controlled review renders of the exported Pier 7 GLB.

    blender -b --python render_pier_7.py -- [--glb FILE] [--out DIR]
                                            [--prefix pier-7] [--night]
                                            [--water] [--axis]
                                            [--samples N] [--only NAME]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig; directions are true compass directions (north = Blender
+Y). The pier runs out into the bay on 54.65 deg; the entry faces 234.65 deg.

`--water` adds the low three-quarter from the bay that proves the pile field
and deck soffit exist. `--axis` adds the eye-level view down the pier from the
entry plaza — the classic Pier 7 photograph, and the only view in which the
lamp-row rhythm can actually be judged. `--night` previews the app's dusk pass
(and renders both the aerial and the axis view).
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (2400, 500)    # very long: a 257 m pier only 7.6 m tall
AER_RES = (1600, 1000)
TOP_RES = (1800, 1250)
BG = (0.86, 0.80, 0.69, 1.0)

VIEWS = [
    ("north", 0.0),
    ("east", 90.0),
    ("south", 180.0),
    ("west", 270.0),
]


def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def import_glb(path):
    bpy.ops.import_scene.gltf(filepath=path)
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


SAMPLES = 64


def setup_world(night=False):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = SAMPLES
    scene.cycles.use_denoising = True
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "Standard"
    world = bpy.data.worlds.new("Studio")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    if night:
        bg.inputs[0].default_value = (0.010, 0.016, 0.035, 1.0)
        bg.inputs[1].default_value = 1.0
    else:
        bg.inputs[0].default_value = BG
        bg.inputs[1].default_value = 0.30


def add_lights(height, night=False):
    if night:
        moon = bpy.data.lights.new("moon", "SUN")
        moon.energy = 0.12
        moon.color = (0.65, 0.74, 1.0)
        moon.angle = math.radians(10)
        ob = bpy.data.objects.new("moon", moon)
        bpy.context.collection.objects.link(ob)
        ob.rotation_euler = (math.radians(55), 0, math.radians(140))
    else:
        key = bpy.data.lights.new("key", "SUN")
        key.energy = 2.1
        key.angle = math.radians(6)
        ob = bpy.data.objects.new("key", key)
        bpy.context.collection.objects.link(ob)
        ob.rotation_euler = (math.radians(52), 0, math.radians(-38))

        fill = bpy.data.lights.new("fill", "SUN")
        fill.energy = 0.55
        fill.angle = math.radians(35)
        ob2 = bpy.data.objects.new("fill", fill)
        bpy.context.collection.objects.link(ob2)
        ob2.rotation_euler = (math.radians(65), 0, math.radians(140))

        rim = bpy.data.lights.new("rim", "SUN")
        rim.energy = 0.45
        rim.color = (1.0, 0.93, 0.82)
        ob3 = bpy.data.objects.new("rim", rim)
        bpy.context.collection.objects.link(ob3)
        ob3.rotation_euler = (math.radians(78), 0, math.radians(60))

    bpy.ops.mesh.primitive_plane_add(size=1400, location=(0, 0, -0.02))
    plane = bpy.context.object
    plane.name = "studio_floor"
    mat = bpy.data.materials.new("Studio_Table")
    mat.use_nodes = True
    # By day the pier stands in the bay: a deep tabletop "water" plane.
    shade = (0.016, 0.028, 0.055, 1.0) if night else (0.23, 0.34, 0.42, 1.0)
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = shade
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.65
    plane.data.materials.append(mat)
    return plane


def glow_materials():
    for mat in bpy.data.materials:
        if mat.use_nodes and mat.name.split(".")[0].endswith("_Glow"):
            yield mat, mat.node_tree.nodes.get("Principled BSDF")


def light_glow():
    """Preview the app's night pass FAITHFULLY: black base + emission at the
    palette colour, strength 1.0, Standard view transform (see pier-3)."""
    for mat, bsdf in glow_materials():
        if not bsdf:
            continue
        rgb = tuple(bsdf.inputs["Base Color"].default_value)
        bsdf.inputs["Base Color"].default_value = (0.0, 0.0, 0.0, 1.0)
        bsdf.inputs["Emission Color"].default_value = rgb
        bsdf.inputs["Emission Strength"].default_value = 1.0


def fade_glow():
    """Preview the app's DAY state: _Glow drawn unlit at ~12% alpha."""
    for mat, bsdf in glow_materials():
        if not bsdf:
            continue
        bsdf.inputs["Alpha"].default_value = 0.12
        mat.surface_render_method = "BLENDED"


def make_camera(name):
    cam = bpy.data.cameras.new(name)
    cam.clip_start = 0.5
    cam.clip_end = 20000.0
    ob = bpy.data.objects.new(name, cam)
    bpy.context.collection.objects.link(ob)
    return ob


def aim(ob, target):
    d = target - ob.location
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def render_to(path, cam, res):
    scene = bpy.context.scene
    scene.camera = cam
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print(f"[render] {path}")


AXIS_DEG = 54.65


def axis_camera(center, night=False):
    """Eye-level down the pier from the entry plaza: the classic photograph."""
    cam = make_camera("cam_axis")
    cam.data.lens = 32.0
    a = math.radians(AXIS_DEG)
    # stand just shoreward of the plaza, 1.7 m above the deck (z = 4.7)
    d = -136.0
    cam.location = Vector((d * math.sin(a), d * math.cos(a), 4.9))
    tgt = Vector((40.0 * math.sin(a), 40.0 * math.cos(a), 4.2))
    aim(cam, tgt)
    return cam


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "pier-7.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "pier-7")
    night = "--night" in argv
    water = "--water" in argv
    axis = "--axis" in argv
    only = arg("--only", "")
    global SAMPLES
    SAMPLES = int(arg("--samples", "64"))
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    height = mx.z - mn.z
    width = max(mx.x - mn.x, mx.y - mn.y)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world(night=night)
    add_lights(height, night=night)

    if night:
        light_glow()
        aer = make_camera("cam_night")
        aer.data.lens = 58.0
        span = max(width, height)
        pitch = math.radians(35)
        az = math.radians(225)
        r = span * 2.9
        tgt = Vector((center.x, center.y, 3.0))
        aer.location = Vector((tgt.x + r * math.cos(pitch) * math.sin(az),
                               tgt.y + r * math.cos(pitch) * math.cos(az),
                               tgt.z + r * math.sin(pitch)))
        aim(aer, tgt)
        render_to(os.path.join(out, f"{prefix}-aerial-night.png"), aer, AER_RES)
        cam = axis_camera(center, night=True)
        render_to(os.path.join(out, f"{prefix}-axis-night.png"), cam, (1400, 900))
        return

    fade_glow()

    span = max(width, height)
    ortho_scale = span * 1.10
    dist = span * 3.0
    for name, az in VIEWS:
        if only and only != name:
            continue
        cam = make_camera(f"cam_{name}")
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = ortho_scale
        a = math.radians(az)
        cam.location = Vector(
            (center.x + dist * math.sin(a), center.y + dist * math.cos(a), center.z)
        )
        aim(cam, center)
        render_to(os.path.join(out, f"{prefix}-{name}.png"), cam, RES)

    if not only or only == "top":
        top = make_camera("cam_top")
        top.data.type = "ORTHO"
        top.data.ortho_scale = width * 1.08
        top.location = Vector((center.x, center.y, mx.z + span))
        top.rotation_euler = (0, 0, 0)
        render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    if water and (not only or only == "water"):
        low = make_camera("cam_water")
        low.data.type = "PERSP"
        low.data.lens = 45.0
        pitch = math.radians(6)
        az = math.radians(150)   # from the SE, three-quarter down the flank
        r = span * 1.25
        low.location = Vector(
            (
                center.x + r * math.cos(pitch) * math.sin(az),
                center.y + r * math.cos(pitch) * math.cos(az),
                4.5,
            )
        )
        aim(low, Vector((center.x, center.y, 4.0)))
        render_to(os.path.join(out, f"{prefix}-water.png"), low, (1800, 700))
        if only == "water":
            return

    if axis and (not only or only == "axis"):
        cam = axis_camera(center)
        render_to(os.path.join(out, f"{prefix}-axis.png"), cam, (1400, 900))
        if only == "axis":
            return

    if only and only != "aerial":
        return

    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 58.0
    pitch = math.radians(38)
    az = math.radians(225)   # from the SW: plaza in front, lamp rows running away
    r = span * 2.9
    tgt = Vector((center.x, center.y, 3.0))
    aer.location = Vector(
        (
            tgt.x + r * math.cos(pitch) * math.sin(az),
            tgt.y + r * math.cos(pitch) * math.cos(az),
            tgt.z + r * math.sin(pitch),
        )
    )
    aim(aer, tgt)
    render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)


if __name__ == "__main__":
    main()
