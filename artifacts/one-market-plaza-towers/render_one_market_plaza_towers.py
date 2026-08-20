"""Controlled review renders of the exported One Market Plaza towers GLB.

    blender -b --python render_one_market_plaza_towers.py -- [--glb FILE] [--out DIR]
                                               [--prefix one-market-plaza-towers] [--night]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth; directions are true compass directions
(north = Blender +Y), which is how the asset is authored — the Market Street
front faces north-west.

The subject of this building is the U and its crown, so the aerial camera sits on
the Market x Steuart corner; the "east" elevation looks straight into the open
side of the courtyard. The top view is the important one — it is the only view
that shows the U, the glazed atrium roof and the plant crest together.

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

# The block sits at 45 deg to the compass, so cardinal cameras would each show
# two faces at once. These are TRUE elevations: one camera per measured face
# normal, named for the street it faces.
VIEWS = [
    ("north", 45.2),   # Steuart Street / Don Chee Way
    ("east", 135.2),   # Mission Street — the public front
    ("south", 225.2),  # south-west flank
    ("west", 315.2),   # the shared boundary with the Southern Pacific Building
]
# The subject is the HEIGHT CONTRAST between the two shafts, which no top view can
# show, so the aerial sits south-east on Mission Street at a low pitch and both
# towers are seen against each other.
AERIAL_AZ = 122.0
AERIAL_PITCH = 26.0


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


# --fast swaps Cycles for Workbench (day) / EEVEE (night). Cycles is the
# reference engine, but this machine runs many parallel Blender sessions and a
# Cycles frame was getting ~5% of one core; the flat-colour toy palette survives
# the swap intact, and the night pass still needs a real emission-capable engine.
FAST = False
GPU = False  # set by --gpu: Cycles on Metal, which this Mac has


def enable_metal():
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "METAL"
    if hasattr(prefs, "get_devices"):
        prefs.get_devices()
    for dev in prefs.devices:
        dev.use = dev.type == "METAL"


def setup_world(night=False):
    scene = bpy.context.scene
    if FAST and night:
        scene.render.engine = "BLENDER_EEVEE"
    elif FAST:
        scene.render.engine = "BLENDER_WORKBENCH"
        scene.display.shading.light = "STUDIO"
        scene.display.shading.color_type = "MATERIAL"
        # Workbench's shadow map leaks light through the proud window reveals and
        # sprays bright speckles across the roof and the cast shadow. Cavity +
        # studio lighting carries the form without the artefact.
        scene.display.shading.show_shadows = False
        scene.display.shading.show_cavity = True
        scene.display.shading.cavity_type = "BOTH"
    else:
        scene.render.engine = "CYCLES"
        if GPU:
            enable_metal()
            scene.cycles.device = "GPU"
        else:
            scene.cycles.device = "CPU"
        scene.cycles.samples = 40
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
    """Preview the app's night pass. The app draws _Glow in a separate UNLIT
    layer, so at night a glow surface reads at exactly its base colour. A high
    emission strength blows a light colour (the atrium glazing) out to white and
    flatters a dark one, so this rig stays low and close to the real thing."""
    for mat, bsdf in glow_materials():
        if not bsdf:
            continue
        # The glTF round-trip drops the emissive colour (it was exported with
        # strength 0), so every imported material comes back with Emission Color
        # = white. Turning the strength up on that renders EVERY glow surface
        # blown-out white and hides what the app will actually show, which is the
        # material's own BASE colour, unlit. Copy base -> emission first.
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

    glb = arg("--glb", os.path.join(here, "one-market-plaza-towers.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "one-market-plaza-towers")
    night = "--night" in argv
    global FAST, GPU
    FAST = "--fast" in argv
    GPU = "--gpu" in argv
    only = arg("--only", "")
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    # a 177 m tower on a 128 m footprint: frame on the LONGEST axis, or the
    # aerial camera sits inside the building and clips the top off
    span = max(mx.x - mn.x, mx.y - mn.y, mx.z - mn.z)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world(night=night)
    add_lights(span, night=night)

    if not night:
        fade_glow()

    if night:
        light_glow()
        aer = make_camera("cam_night")
        aer.data.lens = 62.0
        pitch = math.radians(AERIAL_PITCH)
        az = math.radians(AERIAL_AZ)
        r = span * 3.2
        aer.location = Vector((center.x + r * math.cos(pitch) * math.sin(az),
                               center.y + r * math.cos(pitch) * math.cos(az),
                               mn.z + r * math.sin(pitch)))
        aim(aer, Vector((center.x, center.y, mn.z + (mx.z - mn.z) * 0.42)))
        render_to(os.path.join(out, f"{prefix}-night.png"), aer, AER_RES)
        return

    # --- top view: the roof composition check ------------------------------
    if only in ("", "top"):
        top = make_camera("cam_top")
        top.data.type = "ORTHO"
        top.data.ortho_scale = span * 1.06
        top.location = Vector((center.x, center.y, mx.z + span))
        top.rotation_euler = (0, 0, 0)
        render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- beauty render from the app's high three-quarter aerial camera -----
    if only in ("", "aerial"):
        aer = make_camera("cam_aerial")
        aer.data.type = "PERSP"
        aer.data.lens = 62.0  # long lens, restrained perspective (style bible s.18)
        pitch = math.radians(AERIAL_PITCH)
        az = math.radians(AERIAL_AZ)
        r = span * 3.2
        aer.location = Vector((center.x + r * math.cos(pitch) * math.sin(az),
                               center.y + r * math.cos(pitch) * math.cos(az),
                               mn.z + r * math.sin(pitch)))
        aim(aer, Vector((center.x, center.y, mn.z + (mx.z - mn.z) * 0.42)))
        render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)

    # --- four elevations: one rig, identical everything but azimuth --------
    if only in ("", "elev"):
        ortho_scale = max(span, mx.z - mn.z) * 1.10
        dist = span * 2.0
        for name, az in VIEWS:
            cam = make_camera(f"cam_{name}")
            cam.data.type = "ORTHO"
            cam.data.ortho_scale = ortho_scale
            a = math.radians(az)
            cam.location = Vector((center.x + dist * math.sin(a),
                                   center.y + dist * math.cos(a), mn.z + 60.0))
            aim(cam, Vector((center.x, center.y, mn.z + 60.0)))
            render_to(os.path.join(out, f"{prefix}-{name}.png"), cam, RES)


if __name__ == "__main__":
    main()
