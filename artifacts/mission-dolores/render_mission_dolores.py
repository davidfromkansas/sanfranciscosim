"""Controlled review renders of the exported Mission Dolores GLB.

    blender -b --python render_mission_dolores.py -- [--glb FILE] [--out DIR]
                                                     [--prefix mission-dolores]
                                                     [--only north,aerial,...]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (identical orthographic scale, framing, lighting, exposure
and projection) and differ only in azimuth. Directions are true compass
directions - the asset is authored with Blender +Y = true north, +X = east, and
both facades face EAST onto Dolores Street (REFERENCE.md §3).
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (1250, 950)
AER_RES = (1500, 1050)
TOP_RES = (1300, 1300)
BG = (0.86, 0.80, 0.69, 1.0)  # neutral warm tabletop background

VIEWS = [
    ("north", 0.0),  # camera stands to the north, looking south
    ("east", 90.0),  # the Dolores Street identity view
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
    scene.cycles.samples = 48
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
    ob.rotation_euler = (math.radians(50), 0, math.radians(-52))

    fill = bpy.data.lights.new("fill", "SUN")
    fill.energy = 0.55
    fill.angle = math.radians(35)
    ob2 = bpy.data.objects.new("fill", fill)
    bpy.context.collection.objects.link(ob2)
    ob2.rotation_euler = (math.radians(65), 0, math.radians(150))

    rim = bpy.data.lights.new("rim", "SUN")
    rim.energy = 0.45
    rim.color = (1.0, 0.93, 0.82)
    ob3 = bpy.data.objects.new("rim", rim)
    bpy.context.collection.objects.link(ob3)
    ob3.rotation_euler = (math.radians(78), 0, math.radians(70))

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


def day_mode():
    """Mimic the app's DAY state for the glow layer.

    kit.js updateLandmarkGlow sets the glow layer's opacity to
    0.12 + 0.95 * uNight, so by daylight every *_Glow surface is a 12 %
    unlit ghost over the opaque day surface behind it. Rendering the glow
    shells fully opaque would misrepresent how the asset actually looks in
    the city, so the review renders match the app.
    """
    for mat in bpy.data.materials:
        if mat.name.endswith("_Glow") and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Alpha"].default_value = 0.12


def night_mode():
    """Simulate the app's dusk system.

    In the app (assets.js + kit.js updateLandmarkGlow) every material named
    *_Glow is drawn as an UNLIT overlay whose opacity rises with the real San
    Francisco sun elevation (uNight 0 -> 1). Full night = the glow surfaces at
    their own baked colour, self-luminous. Here: emission on for *_Glow, a dim
    cool moon key, and a deep dusk sky.
    """
    world = bpy.context.scene.world
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.012, 0.020, 0.045, 1.0)
    bg.inputs[1].default_value = 0.22
    for light in bpy.data.lights:
        if light.name == "key":
            light.energy = 0.30
            light.color = (0.62, 0.72, 1.0)  # moonlight
        elif light.name == "fill":
            light.energy = 0.06
            light.color = (0.5, 0.6, 0.9)
        else:
            light.energy = 0.0
    table = bpy.data.materials.get("Studio_Table")
    if table:
        table.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (
            0.08,
            0.08,
            0.10,
            1.0,
        )
    for mat in bpy.data.materials:
        if mat.name.endswith("_Glow") and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Alpha"].default_value = 1.0
                # The shipped GLB carries emissiveFactor 0 (correct - the asset
                # must not self-emit; the app supplies the night pass). The
                # glTF importer therefore hands back Emission COLOUR = white,
                # so raising only Emission Strength would light every window
                # white regardless of its real colour. Drive the emission from
                # the material's own base colour instead, which is exactly what
                # the app's unlit glow layer uses, at strength ~1 so the value
                # matches the baked colour rather than blowing out.
                base = bsdf.inputs["Base Color"].default_value
                bsdf.inputs["Emission Color"].default_value = (
                    base[0],
                    base[1],
                    base[2],
                    1.0,
                )
                bsdf.inputs["Emission Strength"].default_value = 1.0


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "mission-dolores.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "mission-dolores")
    only = arg("--only", "")
    only = set(only.split(",")) if only else None
    os.makedirs(out, exist_ok=True)

    def want(name):
        return only is None or name in only

    clear()
    _, mn, mx = import_glb(glb)
    height = mx.z - mn.z
    width = max(mx.x - mn.x, mx.y - mn.y)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world()
    add_lights(width)
    day_mode()

    # --- four elevations: one rig, identical everything but azimuth ---------
    ortho_scale = width * 1.18
    dist = width * 3.0
    for name, az in VIEWS:
        if not want(name):
            continue
        cam = make_camera(f"cam_{name}")
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = ortho_scale
        a = math.radians(az)
        cam.location = Vector(
            (center.x + dist * math.sin(a), center.y + dist * math.cos(a), height * 0.46)
        )
        aim(cam, Vector((center.x, center.y, height * 0.46)))
        render_to(os.path.join(out, f"{prefix}-{name}.png"), cam, RES)

    # --- top view: both tile roofs, the crossing dome and the tower caps ----
    if want("top"):
        top = make_camera("cam_top")
        top.data.type = "ORTHO"
        top.data.ortho_scale = width * 1.12
        top.location = Vector((center.x, center.y, mx.z + width))
        top.rotation_euler = (0, 0, 0)
        render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- beauty render from the app's high three-quarter aerial camera ------
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 105.0  # long lens, restrained perspective (style bible §18)
    pitch = math.radians(36)  # 30-50 deg downward
    az = math.radians(118)  # ESE: the street facades plus both roofs
    r = width * 4.6  # far enough that both buildings sit inside the frame
    aer.location = Vector(
        (
            center.x + r * math.cos(pitch) * math.sin(az),
            center.y + r * math.cos(pitch) * math.cos(az),
            center.z + r * math.sin(pitch),
        )
    )
    aim(aer, Vector((center.x - 1.0, center.y - 1.0, height * 0.26)))
    if want("aerial"):
        render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)

    # --- night state --------------------------------------------------------
    if want("night"):
        night_mode()
        render_to(os.path.join(out, f"{prefix}-night.png"), aer, AER_RES)

        ncam = make_camera("cam_night_front")
        ncam.data.type = "PERSP"
        ncam.data.lens = 58.0
        pitch_n = math.radians(11)
        az_n = math.radians(96)  # standing on Dolores Street
        rn = width * 2.5
        ncam.location = Vector(
            (
                center.x + rn * math.cos(pitch_n) * math.sin(az_n),
                center.y + rn * math.cos(pitch_n) * math.cos(az_n),
                center.z + rn * math.sin(pitch_n),
            )
        )
        aim(ncam, Vector((center.x, center.y - 1.0, height * 0.34)))
        render_to(os.path.join(out, f"{prefix}-night-front.png"), ncam, (1400, 1000))


if __name__ == "__main__":
    main()
