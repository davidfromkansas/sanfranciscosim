"""Controlled review renders of the exported Pier 15 GLB.

    blender -b --python render_pier_15.py -- [--glb FILE] [--out DIR]
                                                    [--prefix pier-15]
                                                    [--night]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth; directions are true compass directions
(north = Blender +Y), which is how the asset is authored — the Embarcadero
frontage with the portal faces southwest, 233.9 deg, and the pier runs out into
the bay on 53.9 deg.

`--water` adds the low three-quarter view from the bay that the plan requires:
it is the only image that proves the pile field, the deck soffit and the
fendered edge were actually built. `--night` previews the app's dusk pass.
`--samples N` and `--only NAME` exist because this asset is 196 m across and a
full Cycles rig on a loaded machine is not a thing to run casually.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (1800, 700)    # very wide: a 249 m pier only 16.4 m tall
AER_RES = (1600, 1100)
TOP_RES = (1500, 1250)
BG = (0.86, 0.80, 0.69, 1.0)  # neutral warm tabletop background

VIEWS = [
    ("north", 0.0),  # camera stands to the north, looking south
    ("east", 90.0),
    ("south", 180.0),
    ("west", 270.0),
    # The pier sits at 53.9 deg, so all four compass elevations show it on the
    # diagonal. This fifth ortho is square on the Embarcadero frontage — the only
    # view in which the portal can actually be judged.
    ("frontage", 234.9),
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
    """Preview the app's night pass FAITHFULLY.

    assets.js draws the _Glow set in a separate UNLIT layer at
    opacity 0.12 + 0.95*uNight, so at full night the pixel the app shows is the
    material's base colour and nothing else. Driving Principled emission up
    instead (6.0, then 3.0) clipped every glow to white and made a #7ea8c8 roof
    monitor look like a lightbox — which is a rendering artefact, not the asset.
    Black base + emission at the palette colour, strength 1.0, under the Standard
    view transform, reproduces the app exactly.
    """
    for mat, bsdf in glow_materials():
        if not bsdf:
            continue
        rgb = tuple(bsdf.inputs["Base Color"].default_value)
        bsdf.inputs["Base Color"].default_value = (0.0, 0.0, 0.0, 1.0)
        bsdf.inputs["Emission Color"].default_value = rgb
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


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "pier-15.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "pier-15")
    night = "--night" in argv
    water = "--water" in argv
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

    if not night:
        fade_glow()

    if night:
        light_glow()
        aer = make_camera("cam_night")
        aer.data.lens = 70.0
        span = max(width, height)
        pitch = math.radians(35)
        az = math.radians(225)  # from the SW: the portal and the length of the pier
        r = span * 2.55
        bias = 0.10 * span
        tgt = Vector((center.x + bias * math.sin(az), center.y + bias * math.cos(az), 7.0))
        aer.location = Vector(
            (
                tgt.x + r * math.cos(pitch) * math.sin(az),
                tgt.y + r * math.cos(pitch) * math.cos(az),
                tgt.z + r * math.sin(pitch),
            )
        )
        aim(aer, tgt)
        render_to(os.path.join(out, f"{prefix}-aerial-night.png"), aer, AER_RES)
        return

    # --- four elevations: one rig, identical everything but azimuth ---------
    span = max(width, height)
    ortho_scale = span * 1.10
    dist = span * 3.0
    for name, az in VIEWS:
        if only and only != name:
            continue
        cam = make_camera(f"cam_{name}")
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = 74.0 if name == "frontage" else ortho_scale
        a = math.radians(az)
        cam.location = Vector(
            (center.x + dist * math.sin(a), center.y + dist * math.cos(a), center.z)
        )
        if name == "frontage":
            focus = Vector((-101.0, -84.1, 8.2))
            a2 = math.radians(234.9)
            cam.location = Vector((focus.x + dist * math.sin(a2),
                                   focus.y + dist * math.cos(a2), focus.z))
            aim(cam, focus)
            render_to(os.path.join(out, f"{prefix}-{name}.png"), cam, (1500, 800))
            continue
        aim(cam, center)
        render_to(os.path.join(out, f"{prefix}-{name}.png"), cam, RES)

    # --- top: the two roof monitors, the plant, the car park, the fendered edge -
    if not only or only == "top":
        top = make_camera("cam_top")
        top.data.type = "ORTHO"
        top.data.ortho_scale = width * 1.08
        top.location = Vector((center.x, center.y, mx.z + span))
        top.rotation_euler = (0, 0, 0)
        render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- low three-quarter from the bay: the piles, the soffit, the deck edge --
    if water:
        low = make_camera("cam_water")
        low.data.type = "PERSP"
        low.data.lens = 45.0
        pitch = math.radians(7)
        az = math.radians(318)   # from the water courtyard: piles, soffit, courtyard edge
        r = span * 1.55
        low.location = Vector(
            (
                center.x + r * math.cos(pitch) * math.sin(az),
                center.y + r * math.cos(pitch) * math.cos(az),
                6.0,
            )
        )
        aim(low, Vector((center.x, center.y, 6.0)))
        render_to(os.path.join(out, f"{prefix}-water.png"), low, (1800, 700))
        if only == "water":
            return

    if only and only != "aerial":
        return

    # --- beauty render from the app's high three-quarter aerial camera -----
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 70.0  # 196 m of pier: a 105 mm lens simply cannot hold it
    pitch = math.radians(38)  # 30-50 deg downward
    az = math.radians(225)  # from the SW — the only angle that shows the portal
    # and the full run of the pier at once (plan Part 1)
    r = span * 2.55
    bias = 0.10 * span
    tgt = Vector((center.x + bias * math.sin(az), center.y + bias * math.cos(az), 7.0))
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
