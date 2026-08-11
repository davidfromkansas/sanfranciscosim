"""Controlled review renders of the exported Conservatory of Flowers GLB.

    blender -b --python render_conservatory_of_flowers.py -- [--glb FILE]
        [--out DIR] [--prefix conservatory-of-flowers]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The night render
previews the app's dusk system: _Glow materials are lit emissively (in the app
their unlit layer fades in with uNight) under a moonlit sky. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth; directions are true compass directions
(north = Blender +Y), which is how the asset is authored — the building's long
axis runs 81 deg cw from north, so the north/south views face the wings and
the east/west views face the wing ends.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (1500, 700)  # long, low building: landscape elevations
AER_RES = (1400, 1100)
TOP_RES = (1500, 800)
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


def add_lights(size):
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
    bpy.ops.mesh.primitive_plane_add(size=size * 4, location=(0, 0, -0.02))
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

    glb = arg("--glb", os.path.join(here, "conservatory-of-flowers.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "conservatory-of-flowers")
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    # Day state faithful to the app: the glow layer renders at 0.12 opacity
    # while the sun is up (opacity = 0.12 + 0.95 * uNight in app/src/kit.js).
    for mat in bpy.data.materials:
        if mat.name.endswith("_Glow") and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Alpha"].default_value = 0.12
            mat.surface_render_method = "BLENDED"
    height = mx.z - mn.z
    width = max(mx.x - mn.x, mx.y - mn.y)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world()
    add_lights(width)

    # --- four elevations: one rig, identical everything but azimuth ---------
    ortho_scale = width * 1.10
    dist = width * 2.5
    for name, az in VIEWS:
        cam = make_camera(f"cam_{name}")
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = ortho_scale
        a = math.radians(az)
        cam.location = Vector(
            (
                center.x + dist * math.sin(a),
                center.y + dist * math.cos(a),
                center.z + height * 0.25,
            )
        )
        aim(cam, Vector((center.x, center.y, center.z)))
        render_to(os.path.join(out, f"{prefix}-{name}.png"), cam, RES)

    # --- top view: dome ribs, vault roofs, vents and cresting ---------------
    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.ortho_scale = width * 1.12
    top.location = Vector((center.x, center.y, mx.z + width))
    top.rotation_euler = (0, 0, 0)
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- beauty render from the app's high three-quarter aerial camera -----
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 105.0  # long lens, restrained perspective (style bible s.18)
    pitch = math.radians(38)  # 30-50 deg downward
    az = math.radians(196)  # from the south-southwest: the JFK Drive approach
    r = width * 2.6
    aer.location = Vector(
        (
            center.x + r * math.cos(pitch) * math.sin(az),
            center.y + r * math.cos(pitch) * math.cos(az),
            center.z + r * math.sin(pitch),
        )
    )
    aim(aer, Vector((center.x, center.y, center.z * 0.85)))
    render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)

    # --- night state: what the app's dusk system ignites -------------------
    # The app draws _Glow surfaces unlit, fading in with uNight (0 by day,
    # 1 once the sun is 10 deg down). Here: emission on, moonlight, dark sky.
    for mat in bpy.data.materials:
        if mat.name.endswith("_Glow") and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Emission Strength"].default_value = 4.0
                bsdf.inputs["Alpha"].default_value = 1.0
        elif mat.name == "Studio_Table" and mat.use_nodes:
            mat.node_tree.nodes["Principled BSDF"].inputs[
                "Base Color"
            ].default_value = (0.10, 0.11, 0.15, 1.0)
    world_bg = bpy.context.scene.world.node_tree.nodes["Background"]
    world_bg.inputs[0].default_value = (0.020, 0.030, 0.060, 1.0)
    world_bg.inputs[1].default_value = 0.28
    for light in bpy.data.lights:
        light.energy *= 0.10
        light.color = (0.62, 0.72, 1.0)
    render_to(os.path.join(out, f"{prefix}-night.png"), aer, AER_RES)


if __name__ == "__main__":
    main()
