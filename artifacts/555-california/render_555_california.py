"""Controlled review renders of the exported 555 California Street GLB.

    blender -b --python render_555_california.py -- [--glb FILE] [--out DIR]
                                                    [--prefix 555-california]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth; directions are true compass directions
(north = Blender +Y), which is how the asset is authored.

A final pass re-lights the same scene to preview the app's dusk system and
writes 555-california-night.png.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (900, 1500)
AER_RES = (1400, 1200)
TOP_RES = (1200, 1200)
BG = (0.86, 0.80, 0.69, 1.0)  # neutral warm tabletop background

VIEWS = [
    ("north", 0.0),  # camera stands to the north, looking south
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


def setup_world():
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
    bg.inputs[0].default_value = BG
    bg.inputs[1].default_value = 0.30


def add_lights(height):
    """Simple tabletop lighting: broad soft key, cool fill, warm rim."""
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

    # A ground catcher gives the contact shadow that sells the miniature.
    bpy.ops.mesh.primitive_plane_add(size=height * 4, location=(0, 0, -0.02))
    plane = bpy.context.object
    plane.name = "studio_floor"
    mat = bpy.data.materials.new("Studio_Table")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (
        0.62,
        0.55,
        0.45,
        1.0,
    )
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
    plane.data.materials.append(mat)
    return plane


def daylight_glow():
    """Match the app's DAY appearance of `_Glow` surfaces.

    assets.js puts every `_Glow` face in a separate unlit MeshBasicMaterial whose
    opacity is `0.12 + 0.95 * uNight`. In daylight that is 12% - the lit panes
    are a whisper over the glass, not opaque cream. Rendering them solid would
    show a building the app never draws, so the day pass dials them down here.
    The shipped GLB itself stays fully opaque, as the contract requires.
    """
    for mat in bpy.data.materials:
        if not mat.name.endswith("_Glow") or not mat.use_nodes:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Alpha"].default_value = 0.12


def night_glow():
    """Match the app's NIGHT appearance: the glow layer at full self-lit colour."""
    for mat in bpy.data.materials:
        if not mat.name.endswith("_Glow") or not mat.use_nodes:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Alpha"].default_value = 1.0
            bsdf.inputs["Emission Strength"].default_value = (
                7.0 if mat.name.startswith("Toy_red") else 4.2
            )


def make_camera(name):
    cam = bpy.data.cameras.new(name)
    cam.clip_start = 1.0
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

    glb = arg("--glb", os.path.join(here, "555-california.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "555-california")
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    daylight_glow()
    height = mx.z - mn.z
    width = max(mx.x - mn.x, mx.y - mn.y)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world()
    add_lights(height)

    # --- four elevations: one rig, identical everything but azimuth ---------
    ortho_scale = height * 1.12
    dist = height * 3.0
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

    # --- top view: the flat crown, parapet, penthouse and setback shoulders --
    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.ortho_scale = width * 1.5
    top.location = Vector((center.x, center.y, mx.z + height))
    top.rotation_euler = (0, 0, 0)
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- beauty render from the app's high three-quarter aerial camera -----
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 105.0  # long lens, restrained perspective (style bible s.18)
    pitch = math.radians(38)  # 30-50 deg downward
    az = math.radians(205)  # from the south-southwest: California Street corner
    r = height * 4.2
    aer.location = Vector(
        (
            center.x + r * math.cos(pitch) * math.sin(az),
            center.y + r * math.cos(pitch) * math.cos(az),
            center.z + r * math.sin(pitch),
        )
    )
    aim(aer, Vector((center.x, center.y, center.z * 0.92)))
    render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)

    # --- night state: simulate the app's dusk system ------------------------
    # In the app (assets.js + kit.js updateLandmarkGlow), every material named
    # *_Glow is drawn as an UNLIT overlay whose opacity rises with the real San
    # Francisco sun elevation (uNight 0 -> 1). Full night = the glow surfaces at
    # their own baked colour, self-luminous. Here: emission on for *_Glow, a dim
    # cool moon key, and a deep dusk sky.
    world = bpy.context.scene.world
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.012, 0.020, 0.045, 1.0)
    bg.inputs[1].default_value = 0.22
    for light in bpy.data.lights:
        if light.name == "key":
            light.energy = 0.26
            light.color = (0.62, 0.72, 1.0)  # moonlight
        elif light.name == "fill":
            light.energy = 0.06
            light.color = (0.5, 0.6, 0.9)
        else:
            light.energy = 0.0
    night_glow()
    render_to(os.path.join(out, f"{prefix}-night.png"), aer, AER_RES)


if __name__ == "__main__":
    main()
