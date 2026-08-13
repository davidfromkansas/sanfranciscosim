"""Controlled review renders of the exported 542 Presidio Boulevard GLB.

    blender -b --python render_542_presidio_blvd.py -- [--glb FILE] [--out DIR]
                                                       [--prefix 542-presidio-blvd]
                                                       [--only aerial]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth; directions are true compass directions
(north = Blender +Y), which is how the asset is authored.

This building is wider than it is tall, so the shared ortho scale is driven by
the plan extent rather than the height. The night pass re-renders the aerial
with the _Glow materials switched on, which is the only difference.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (1200, 900)
AER_RES = (1400, 1050)
TOP_RES = (1200, 1200)
BG = (0.86, 0.80, 0.69, 1.0)  # neutral warm tabletop background
BG_NIGHT = (0.055, 0.065, 0.095, 1.0)

VIEWS = [
    ("north", 0.0),  # camera stands to the north, looking south
    ("east", 90.0),
    ("south", 180.0),
    ("west", 270.0),
]

# The entrance front faces ESE (bearing 121 deg); this three-quarter azimuth
# shows that front plus the SSW hip end, which is how the city camera sees it.
AERIAL_AZ = 150.0


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
    bg.inputs[0].default_value = BG_NIGHT if night else BG
    bg.inputs[1].default_value = 0.10 if night else 0.30


def add_lights(height, night=False):
    """Simple tabletop lighting: broad soft key, cool fill, warm rim."""
    k = 0.13 if night else 1.0
    key = bpy.data.lights.new("key", "SUN")
    key.energy = 2.1 * k
    key.angle = math.radians(6)
    if night:
        key.color = (0.72, 0.80, 1.0)
    ob = bpy.data.objects.new("key", key)
    bpy.context.collection.objects.link(ob)
    ob.rotation_euler = (math.radians(52), 0, math.radians(-38))

    fill = bpy.data.lights.new("fill", "SUN")
    fill.energy = 0.55 * k
    fill.angle = math.radians(35)
    ob2 = bpy.data.objects.new("fill", fill)
    bpy.context.collection.objects.link(ob2)
    ob2.rotation_euler = (math.radians(65), 0, math.radians(140))

    rim = bpy.data.lights.new("rim", "SUN")
    rim.energy = 0.45 * k
    rim.color = (1.0, 0.93, 0.82)
    ob3 = bpy.data.objects.new("rim", rim)
    bpy.context.collection.objects.link(ob3)
    ob3.rotation_euler = (math.radians(78), 0, math.radians(60))

    # A ground catcher gives the contact shadow that sells the miniature.
    bpy.ops.mesh.primitive_plane_add(size=height * 12, location=(0, 0, -0.02))
    plane = bpy.context.object
    plane.name = "studio_floor"
    mat = bpy.data.materials.new("Studio_Table")
    mat.use_nodes = True
    base = (0.10, 0.11, 0.14, 1.0) if night else (0.62, 0.55, 0.45, 1.0)
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = base
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
    plane.data.materials.append(mat)
    return plane


def light_the_glow():
    """Night pass: the _Glow materials are what the app lights after dark."""
    for mat in bpy.data.materials:
        if not mat.name.endswith("_Glow") or not mat.use_nodes:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if not bsdf:
            continue
        # The asset ships with emission strength 0, so glTF writes an
        # emissiveFactor of black and the re-import has no glow colour left to
        # restore. Drive emission from the surviving base colour instead -
        # otherwise every lit surface renders as clipped white regardless of
        # its palette entry, which is what the app would never do.
        base = bsdf.inputs["Base Color"].default_value
        bsdf.inputs["Emission Color"].default_value = base
        strength = 6.0 if mat.name == "Toy_white_Glow" else 3.0
        bsdf.inputs["Emission Strength"].default_value = strength
        print(f"[render] glow on: {mat.name} @ {strength} "
              f"rgb=({base[0]:.3f},{base[1]:.3f},{base[2]:.3f})")


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


def aerial_camera(center, span, height):
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 105.0  # long lens, restrained perspective (style bible s.18)
    pitch = math.radians(38)  # 30-50 deg downward
    az = math.radians(AERIAL_AZ)
    r = span * 3.4
    aer.location = Vector(
        (
            center.x + r * math.cos(pitch) * math.sin(az),
            center.y + r * math.cos(pitch) * math.cos(az),
            center.z + r * math.sin(pitch),
        )
    )
    aim(aer, Vector((center.x, center.y, center.z * 0.85)))
    return aer


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "542-presidio-blvd.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "542-presidio-blvd")
    only = arg("--only", "")
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    height = mx.z - mn.z
    span = max(mx.x - mn.x, mx.y - mn.y)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world()
    add_lights(height)

    # This asset is far wider than it is tall, so the plan extent drives the
    # shared ortho scale; height-driven framing would crop the eaves.
    ortho_scale = span * 1.15
    dist = span * 3.0

    if only in ("", "aerial"):
        aer = aerial_camera(center, span, height)
        render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)
    if only == "aerial":
        return
    if only == "night":
        setup_world(night=True)
        for lt in [o for o in bpy.data.objects if o.type in ("LIGHT", "MESH")
                   if o.name in ("key", "fill", "rim", "studio_floor")]:
            bpy.data.objects.remove(lt, do_unlink=True)
        add_lights(height, night=True)
        light_the_glow()
        render_to(os.path.join(out, f"{prefix}-night.png"),
                  aerial_camera(center, span, height), AER_RES)
        return

    # --- four elevations: one rig, identical everything but azimuth ---------
    for name, az in VIEWS:
        cam = make_camera(f"cam_{name}")
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = ortho_scale
        a = math.radians(az)
        cam.location = Vector(
            (center.x + dist * math.sin(a), center.y + dist * math.cos(a), center.z)
        )
        aim(cam, center)
        render_to(os.path.join(out, f"{prefix}-{name}.png"), cam, RES)

    # --- top view: the roof, which is this asset's dominant surface ---------
    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.ortho_scale = span * 1.15
    top.location = Vector((center.x, center.y, mx.z + span))
    top.rotation_euler = (0, 0, 0)
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- night: same aerial framing, glow on --------------------------------
    clear()
    _, mn, mx = import_glb(glb)
    setup_world(night=True)
    add_lights(height, night=True)
    light_the_glow()
    naer = aerial_camera(center, span, height)
    render_to(os.path.join(out, f"{prefix}-night.png"), naer, AER_RES)


if __name__ == "__main__":
    main()
