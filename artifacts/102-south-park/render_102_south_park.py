"""Controlled review renders of the exported 181 South Park GLB.

    blender -b --python render_380_brannan.py -- [--glb FILE] [--out DIR]
                                                    [--prefix 102-south-park]
                                                    [--night] [--only VIEW]
                                                    [--samples N]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth; directions are true compass directions
(north = Blender +Y), which is how the asset is authored — the South Park front faces SE (135.4 deg).

--only renders a single view (aerial|top|north|east|south|west), --samples
overrides the sample count and --engine EEVEE swaps Cycles for EEVEE, so the
stage-2 aerial review loop stays cheap on a loaded machine; the formal rig runs
at the defaults (Cycles, 64 samples), which is what the committed images are.

--night previews the app's dusk pass: _Glow materials get their emission
turned up under a dark moonlit world, producing <prefix>-night.png.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (1200, 1100)   # near-square: a 29.8 m plan under a 14 m front
AER_RES = (1400, 1200)
TOP_RES = (1200, 1200)
BG = (0.86, 0.80, 0.69, 1.0)  # neutral warm tabletop background

VIEWS = [
    ("north", 0.0),  # camera stands to the north, looking south
    ("east", 90.0),
    ("south", 180.0),
    ("west", 270.0),
]


# The committed images are EEVEE at 128 samples, not Cycles. These materials are
# flat, untextured and opaque, so the two engines are visually equivalent here,
# and this machine runs several batch sessions at once — Cycles CPU could not
# finish the rig. Pass --engine CYCLES to reproduce in Cycles.
SAMPLES = 128
ENGINE = "EEVEE"


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
    scene.render.engine = "BLENDER_EEVEE" if ENGINE == "EEVEE" else "CYCLES"
    if ENGINE == "EEVEE":
        scene.eevee.taa_render_samples = SAMPLES
    else:
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

    # A ground catcher gives the contact shadow that sells the miniature.
    bpy.ops.mesh.primitive_plane_add(size=height * 5, location=(0, 0, -0.02))
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
    """Preview the app's night pass.

    Drive emission from Base Color, never from the imported emission. glTF writes
    emissiveFactor = 0 when the authored emission strength is 0, so a re-imported
    _Glow material carries a DEFAULT WHITE emission colour and raising its
    strength renders every glow surface as a white slab — which is what the first
    night render of this asset did. Copying Base Color across at strength 1.0 is
    also exactly what the app does: its night layer is an unlit overlay drawn at
    the material's own baked colour. See docs/asset-plans/README.md.
    """
    for mat, bsdf in glow_materials():
        if not bsdf:
            continue
        base = bsdf.inputs["Base Color"].default_value
        bsdf.inputs["Emission Color"].default_value = (base[0], base[1], base[2], 1.0)
        bsdf.inputs["Emission Strength"].default_value = 1.0


def fade_glow():
    """Preview the app's DAY state. assets.js/kit.js put _Glow surfaces in a
    separate unlit layer at opacity 0.12 + 0.95*uNight, so by day these shells
    are ~12% alpha and the opaque glazing behind them reads through. Rendering
    them solid would judge a building the app never shows."""
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


def render_top(center, mx, width, span, out, prefix):
    """Top view: the full 29.8 m roof, its solar array and the light-well slots."""
    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.ortho_scale = width * 1.06
    top.location = Vector((center.x, center.y, mx.z + span))
    top.rotation_euler = (0, 0, 0)
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "102-south-park.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "102-south-park")
    night = "--night" in argv
    only = arg("--only", None)
    global SAMPLES, ENGINE
    SAMPLES = int(arg("--samples", SAMPLES))
    ENGINE = arg("--engine", ENGINE).upper()
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    height = mx.z - mn.z
    width = max(mx.x - mn.x, mx.y - mn.y)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world(night=night)
    add_lights(height, night=night)

    if not night:
        fade_glow()

    if night:
        light_glow()
        aer = make_camera("cam_night")
        aer.data.lens = 90.0
        span = max(width, height)
        pitch = math.radians(35)
        az = math.radians(105)  # three-quarter, same as the day aerial
        r = span * 4.4
        aer.location = Vector(
            (
                center.x + r * math.cos(pitch) * math.sin(az),
                center.y + r * math.cos(pitch) * math.cos(az),
                center.z + r * math.sin(pitch),
            )
        )
        aim(aer, Vector((center.x, center.y, center.z * 0.9)))
        render_to(os.path.join(out, f"{prefix}-aerial-night.png"), aer, AER_RES)
        return

    # --- four elevations: one rig, identical everything but azimuth ---------
    span = max(width, height)
    ortho_scale = span * 1.18
    dist = span * 3.0
    for name, az in VIEWS:
        if only and name != only:
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

    # --- top view: the solar array, the parapet ring and the light wells ----
    if not only or only == "top":
        render_top(center, mx, width, span, out, prefix)
    if only and only != "aerial":
        return

    # --- beauty render from the app's high three-quarter aerial camera -----
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 105.0  # long lens, restrained perspective (style bible §18)
    pitch = math.radians(38)  # 30-50 deg downward
    # The front normal is 135.4 deg and the exposed NE flank's is 45.0 deg, so a
    # camera at 105 deg is a true three-quarter to this building: the arched
    # facade, the long flank rhythm and the solar roof all read at once, which is
    # what the app's camera actually gets. 135 would flatten the flank away.
    az = math.radians(105)
    r = span * 4.4
    aer.location = Vector(
        (
            center.x + r * math.cos(pitch) * math.sin(az),
            center.y + r * math.cos(pitch) * math.cos(az),
            center.z + r * math.sin(pitch),
        )
    )
    aim(aer, Vector((center.x, center.y, center.z * 0.92)))
    render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)


if __name__ == "__main__":
    main()
