"""Controlled review renders of the exported 41-43 South Park GLB.

    blender -b --python render_41_south_park.py -- [--glb FILE] [--out DIR]
                                              [--prefix 41-south-park] [--night]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth.

The building sits 135 deg off the world axes, so for once the elevations DO face
the intercardinals and the filenames are literal:

    -north-west.png  street elevation, faces 315.22 deg (South Park, both bays)
    -south-east.png  rear elevation, faces 135.22 deg (the private yard)
    -north-east.png  party flank toward 35 South Park, faces 45.22 deg
    -south-west.png  party flank toward 45-49 South Park, faces 225.22 deg

The building is 3.5x deeper than it is wide, so the elevations are framed to the
long dimension and the two end views carry a lot of empty frame. That is
deliberate: a reviewer has to be able to compare opposite faces at one scale.

--night previews the app's dusk pass: _Glow materials get their emission turned
up under a dark moonlit world, producing <prefix>-aerial-night.png.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (1200, 1000)
AER_RES = (1600, 1200)
TOP_RES = (1100, 1400)   # portrait: the building is a 25 m sliver
BG = (0.86, 0.80, 0.69, 1.0)  # neutral warm tabletop background

FRONT_AZ = 315.22
LONG_AXIS = 135.22       # front -> rear bearing

VIEWS = [
    ("north-west", FRONT_AZ),           # street elevation, both bays
    ("south-east", FRONT_AZ + 180.0),   # rear
    ("north-east", 45.22),              # flank toward 35 South Park
    ("south-west", 225.22),             # flank toward 45-49 South Park
]

# A three-quarter a little north of the facade normal, so the NORTH-EAST half of
# the frontage — the oxblood bay and the entry stoop, which are what identify
# this house — sits nearest the camera, with the 24 m body receding to the
# south-east behind it. Square to the facade (315.2) flattens the two bays into
# one silhouette and hides the depth entirely.
AERIAL_AZ = 338.0
AERIAL_PITCH = 34.0
AERIAL_R = 3.40


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
        bg.inputs[1].default_value = 0.34   # a touch above 165's 0.30: this
                                            # building is charcoal and needs the
                                            # ambient to keep its mouldings read


def add_lights(height, night=False):
    """Simple tabletop lighting: broad soft key, cool fill, warm rim."""
    if night:
        moon = bpy.data.lights.new("moon", "SUN")
        moon.energy = 0.12
        moon.color = (0.65, 0.74, 1.0)
        moon.angle = math.radians(10)
        ob = bpy.data.objects.new("moon", moon)
        bpy.context.collection.objects.link(ob)
        ob.rotation_euler = (math.radians(55), 0, math.radians(200))
    else:
        key = bpy.data.lights.new("key", "SUN")
        key.energy = 2.4
        key.angle = math.radians(6)
        ob = bpy.data.objects.new("key", key)
        bpy.context.collection.objects.link(ob)
        # Keyed from the north-west so the street elevation is lit square-ish
        # and the cornice throws its shadow down the facade — the read that
        # tells a charcoal building apart from a charcoal box.
        ob.rotation_euler = (math.radians(48), 0, math.radians(325))

        fill = bpy.data.lights.new("fill", "SUN")
        fill.energy = 0.60
        fill.angle = math.radians(35)
        ob2 = bpy.data.objects.new("fill", fill)
        bpy.context.collection.objects.link(ob2)
        ob2.rotation_euler = (math.radians(65), 0, math.radians(150))

        rim = bpy.data.lights.new("rim", "SUN")
        rim.energy = 0.50
        rim.color = (1.0, 0.93, 0.82)
        ob3 = bpy.data.objects.new("rim", rim)
        bpy.context.collection.objects.link(ob3)
        ob3.rotation_euler = (math.radians(78), 0, math.radians(80))

    # A ground catcher gives the contact shadow that sells the miniature.
    bpy.ops.mesh.primitive_plane_add(size=height * 8, location=(0, 0, -0.02))
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
    """Preview the app's night pass: emission up on every _Glow material."""
    for mat, bsdf in glow_materials():
        if bsdf:
            bsdf.inputs["Emission Strength"].default_value = 6.0


def fade_glow():
    """Preview the app's DAY state. assets.js/kit.js put _Glow surfaces in a
    separate unlit layer at opacity 0.12 + 0.95*uNight, so by day these shells
    are ~12% alpha and the opaque surface behind them reads through. Rendering
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


def orbit(center, az_deg, pitch_deg, radius):
    a, p = math.radians(az_deg), math.radians(pitch_deg)
    return Vector(
        (
            center.x + radius * math.cos(p) * math.sin(a),
            center.y + radius * math.cos(p) * math.cos(a),
            center.z + radius * math.sin(p),
        )
    )


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

    glb = arg("--glb", os.path.join(here, "41-south-park.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "41-south-park")
    night = "--night" in argv
    only = arg("--only", None)
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

    span = max(width, height)

    if night:
        light_glow()
        aer = make_camera("cam_night")
        aer.data.lens = 78.0
        aer.location = orbit(center, AERIAL_AZ, AERIAL_PITCH, span * AERIAL_R)
        aim(aer, Vector((center.x, center.y, center.z * 0.9)))
        render_to(os.path.join(out, f"{prefix}-aerial-night.png"), aer, AER_RES)
        return

    # --- beauty render from the app's high three-quarter aerial camera ------
    # Rendered FIRST: this is the view the pipeline says to review and iterate
    # on before anything else is judged.
    if only in (None, "aerial"):
        aer = make_camera("cam_aerial")
        aer.data.type = "PERSP"
        aer.data.lens = 78.0  # long lens, restrained perspective (style bible §18)
        aer.location = orbit(center, AERIAL_AZ, AERIAL_PITCH, span * AERIAL_R)
        aim(aer, Vector((center.x, center.y, center.z * 0.92)))
        render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)
    if only == "aerial":
        return

    # --- four elevations: one rig, identical everything but azimuth ---------
    ortho_scale = span * 1.25
    dist = span * 3.0
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

    # --- top view: the pale roof, the terrace and spa, the cornice returns --
    # Rolled to the building's axis so the sliver runs up the frame with the
    # street end at the top. For a top-down camera image-up maps to world
    # (-sin rz, cos rz), so rz = LONG_AXIS - 90 puts the front direction up.
    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.ortho_scale = 28.0   # portrait frame: this is the VERTICAL extent
    top.location = Vector((center.x, center.y, mx.z + span))
    top.rotation_euler = (0, 0, math.radians(LONG_AXIS - 90.0))
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)


if __name__ == "__main__":
    main()
