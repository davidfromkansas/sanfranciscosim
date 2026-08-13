"""Controlled review renders of the exported 590 Third Street GLB.

    blender -b --python render_590_third.py -- [--glb FILE] [--out DIR]
                                               [--prefix 590-third] [--night]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth; directions are true compass directions
(north = Blender +Y), which is how the asset is authored — the 3rd Street front
front faces north-east and the Brannan front south-east.

The hero view is the aerial from due east, where the two designed street
elevations meet at the 3rd/Brannan corner and the raised corner parapet reads
against the sky; the top view carries the brown roof and its light well.

--night previews the app's dusk pass: _Glow materials get their emission turned
up under a dark moonlit world, producing <prefix>-night.png.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (1500, 900)
AER_RES = (1600, 1100)
TOP_RES = (1500, 1500)
BG = (0.86, 0.80, 0.69, 1.0)  # neutral warm tabletop background

VIEWS = [
    ("north", 0.0),  # camera stands to the north, looking south
    ("east", 90.0),
    ("south", 180.0),
    ("west", 270.0),
]
# Due east: the 3rd Street front (normal 45.2 deg) and the Brannan front
# (normal 135.1 deg) are symmetric about this azimuth, so both designed
# elevations, the east corner and the raised parapet over it read in one frame
# (style bible s.18).
AERIAL_AZ = 90.0


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


def setup_world(night=False):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 64
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


def add_lights(span, night=False):
    """Simple tabletop lighting: broad soft key, cool fill, warm rim."""
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

    bpy.ops.mesh.primitive_plane_add(size=span * 3, location=(0, 0, -0.02))
    plane = bpy.context.object
    plane.name = "studio_floor"
    mat = bpy.data.materials.new("Studio_Table")
    mat.use_nodes = True
    shade = (0.05, 0.06, 0.09, 1.0) if night else (0.62, 0.55, 0.45, 1.0)
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = shade
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
    plane.data.materials.append(mat)
    return plane


def glow_materials():
    for mat in bpy.data.materials:
        if mat.use_nodes and mat.name.split(".")[0].endswith("_Glow"):
            yield mat, mat.node_tree.nodes.get("Principled BSDF")


def light_glow():
    """Preview the app's night pass: drive emission from Base Color.

    Raising Emission Strength alone is WRONG on a re-imported GLB and renders
    every glow surface white. glTF writes `emissiveFactor = 0` when the authored
    emission strength is 0, so the re-imported `_Glow` material carries a default
    WHITE emission colour. Copy Base Color into Emission Color at strength 1.0 —
    that is also exactly what the app does, since its night layer is an unlit
    overlay drawn at the material's own baked colour. See the note at the foot of
    `docs/asset-plans/README.md`; this bit `chase-center` first."""
    for mat, bsdf in glow_materials():
        if not bsdf:
            continue
        base = bsdf.inputs["Base Color"].default_value
        bsdf.inputs["Emission Color"].default_value = (base[0], base[1], base[2], 1.0)
        bsdf.inputs["Emission Strength"].default_value = 1.0


def fade_glow():
    """Preview the app's DAY state. assets.js/kit.js put _Glow surfaces in a
    separate unlit layer at opacity 0.12 + 0.95*uNight, so by day these shells
    are ~12% alpha and the opaque glazing behind them reads through."""
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


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "590-third.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "590-third")
    night = "--night" in argv
    only = arg("--only", "")
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    span = max(mx.x - mn.x, mx.y - mn.y)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world(night=night)
    add_lights(span, night=night)

    if not night:
        fade_glow()

    if night:
        light_glow()
        aer = make_camera("cam_night")
        aer.data.lens = 90.0
        pitch = math.radians(40)
        az = math.radians(AERIAL_AZ)
        r = span * 4.2
        aer.location = Vector((center.x + r * math.cos(pitch) * math.sin(az),
                               center.y + r * math.cos(pitch) * math.cos(az),
                               mn.z + r * math.sin(pitch)))
        aim(aer, Vector((center.x, center.y, mn.z + 3.8)))
        render_to(os.path.join(out, f"{prefix}-night.png"), aer, AER_RES)
        return

    # --- top view: the hero image for this asset ---------------------------
    if only in ("", "top"):
        top = make_camera("cam_top")
        top.data.type = "ORTHO"
        top.data.ortho_scale = span * 1.04
        top.location = Vector((center.x, center.y, mx.z + span))
        top.rotation_euler = (0, 0, 0)
        render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- beauty render from the app's high three-quarter aerial camera -----
    if only in ("", "aerial"):
        aer = make_camera("cam_aerial")
        aer.data.type = "PERSP"
        aer.data.lens = 105.0  # long lens, restrained perspective (style bible s.18)
        pitch = math.radians(40)  # 30-50 deg downward
        az = math.radians(AERIAL_AZ)
        r = span * 4.2
        aer.location = Vector((center.x + r * math.cos(pitch) * math.sin(az),
                               center.y + r * math.cos(pitch) * math.cos(az),
                               mn.z + r * math.sin(pitch)))
        aim(aer, Vector((center.x, center.y, mn.z + 3.8)))
        render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)

    # --- four elevations: one rig, identical everything but azimuth --------
    if only in ("", "elev"):
        ortho_scale = span * 1.06
        dist = span * 2.0
        for name, az in VIEWS:
            cam = make_camera(f"cam_{name}")
            cam.data.type = "ORTHO"
            cam.data.ortho_scale = ortho_scale
            a = math.radians(az)
            cam.location = Vector((center.x + dist * math.sin(a),
                                   center.y + dist * math.cos(a), mn.z + 4.8))
            aim(cam, Vector((center.x, center.y, mn.z + 4.8)))
            render_to(os.path.join(out, f"{prefix}-{name}.png"), cam, RES)


if __name__ == "__main__":
    main()
