"""Controlled review renders of the exported Palace of Fine Arts GLB.

    blender -b --python render_palace_of_fine_arts.py -- [--glb FILE] [--out DIR]
                                                         [--prefix palace-of-fine-arts]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth; directions are true compass directions
(north = Blender +Y), which is how the asset is authored. The composition is
low and wide, so the elevations are landscape-format.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (1600, 760)
AER_RES = (1400, 1200)
TOP_RES = (1400, 1400)
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


def add_lights(extent):
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
    bpy.ops.mesh.primitive_plane_add(size=extent * 4, location=(0, 0, -0.02))
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

    glb = arg("--glb", os.path.join(here, "palace-of-fine-arts.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "palace-of-fine-arts")
    night = "--night" in argv
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    extent = max(mx.x - mn.x, mx.y - mn.y)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world()
    add_lights(extent)

    if night:
        # Preview of the app's night pass: same asset, emission raised on the
        # _Glow materials, moonlit world. The shipped GLB itself is unchanged
        # (its emission strength is 0; the app drives it after dark).
        scene = bpy.context.scene
        scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.010, 0.016, 0.045, 1.0)
        scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.55
        for light in bpy.data.lights:
            light.energy *= 0.035  # moonlight remnant of the day rig
            light.color = (0.65, 0.75, 1.0)
        for mat in bpy.data.materials:
            if not mat.name.startswith("Toy_") or not mat.use_nodes:
                continue
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if not bsdf:
                continue
            if mat.name.endswith("_Glow"):
                bsdf.inputs["Emission Color"].default_value = bsdf.inputs["Base Color"].default_value
                bsdf.inputs["Emission Strength"].default_value = 6.0
        night_prefix = f"{prefix}-night"
        aerN = make_camera("cam_night_aerial")
        aerN.data.type = "PERSP"
        aerN.data.lens = 105.0
        pitch = math.radians(38)
        az = math.radians(118)
        r = extent * 3.4
        aerN.location = Vector(
            (
                center.x + r * math.cos(pitch) * math.sin(az),
                center.y + r * math.cos(pitch) * math.cos(az),
                center.z + r * math.sin(pitch),
            )
        )
        aim(aerN, Vector((center.x, center.y, center.z * 0.5)))
        render_to(os.path.join(out, f"{night_prefix}-aerial.png"), aerN, AER_RES)

        eastN = make_camera("cam_night_east")
        eastN.data.type = "ORTHO"
        eastN.data.ortho_scale = extent * 1.10
        eastN.location = Vector((center.x + extent * 3.0, center.y, center.z))
        aim(eastN, center)
        render_to(os.path.join(out, f"{night_prefix}-east.png"), eastN, RES)
        return

    # --- four elevations: one rig, identical everything but azimuth ---------
    ortho_scale = extent * 1.10
    dist = extent * 3.0
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

    # --- top view: dome, peristyle ring and the curved pergola rooflines ----
    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.ortho_scale = extent * 1.15
    top.location = Vector((center.x, center.y, mx.z + extent))
    top.rotation_euler = (0, 0, 0)
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- beauty render from the app's high three-quarter aerial camera -----
    # From the east-southeast: the lagoon side, the composition's true front.
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 105.0  # long lens, restrained perspective (style bible s.18)
    pitch = math.radians(38)  # 30-50 deg downward
    az = math.radians(118)  # compass azimuth of the camera relative to center
    r = extent * 3.4
    aer.location = Vector(
        (
            center.x + r * math.cos(pitch) * math.sin(az),
            center.y + r * math.cos(pitch) * math.cos(az),
            center.z + r * math.sin(pitch),
        )
    )
    aim(aer, Vector((center.x, center.y, center.z * 0.5)))
    render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)


if __name__ == "__main__":
    main()
