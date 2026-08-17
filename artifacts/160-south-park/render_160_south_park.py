"""Controlled review renders of the exported 160 South Park GLB.

    blender -b --python render_160_south_park.py -- [--glb FILE] [--out DIR]
                                               [--prefix 160-south-park] [--night]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth.

The building sits ~108 deg off the world axes, so the cameras are aligned to the
BUILDING's axes, not to true compass directions — otherwise every "elevation"
would be an oblique three-quarter and a reviewer could not compare opposite
faces. Each view keeps the nearest compass filename:

    -east.png   street elevation, faces 108.13 deg (South Park, the arch)
    -west.png   rear elevation, faces 288.13 deg (the rear yard)
    -north.png  party flank toward 156 South Park, faces 45.1 deg
    -south.png  party flank toward 164 South Park, faces 225.1 deg

The building is 4.3x deeper than it is wide, so the elevations are framed to the
long dimension and the two end views carry a lot of empty frame. That is
deliberate: a reviewer has to be able to compare opposite faces at one scale.
Because that framing makes the 6.2 m street elevation tiny — and the street
elevation carries the entire design — a fifth view, -facade.png, renders it
square-on at its own scale.

--night previews the app's dusk pass: _Glow materials get their emission
turned up under a dark moonlit world, producing <prefix>-aerial-night.png.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (1200, 1000)
FACADE_RES = (900, 1100)
AER_RES = (1600, 1200)
TOP_RES = (1100, 1400)   # portrait: the building is a 26.5 m sliver
BG = (0.86, 0.80, 0.69, 1.0)  # neutral warm tabletop background

FRONT_AZ = 108.13
LONG_AXIS = 299.3        # front -> rear bearing, used for the top view's roll

# Azimuths are the bearings each elevation FACES, so the camera stands on that
# side looking back at the building.
VIEWS = [
    ("east", FRONT_AZ),           # street elevation, with the arch
    ("west", FRONT_AZ + 180.0),   # rear
    ("north", 45.1),              # flank toward 156
    ("south", 225.1),             # flank toward 164
]

# A three-quarter just south of the facade normal: it reads the arch and the
# tile eave square enough to recognise, and the body running away to the
# north-west behind them, which is the proportion cue. Square to the facade
# hides the depth; much further round throws the facade to the edge of frame
# behind 26 m of blank party wall.
AERIAL_AZ = 96.0
AERIAL_PITCH = 34.0
AERIAL_R = 3.30

# Frontage chord midpoint in MODEL coordinates (design polygon front chord
# midpoint 11.913, -4.431 less the build's recentring shift 0.466, 1.301).
FRONT_MID = (11.447, -5.732)


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


def add_lights(height, night=False):
    """Simple tabletop lighting: broad soft key, cool fill, warm rim."""
    if night:
        moon = bpy.data.lights.new("moon", "SUN")
        moon.energy = 0.12
        moon.color = (0.65, 0.74, 1.0)
        ob = bpy.data.objects.new("moon", moon)
        bpy.context.collection.objects.link(ob)
        ob.rotation_euler = (math.radians(55), 0, math.radians(250))
    else:
        key = bpy.data.lights.new("key", "SUN")
        key.energy = 2.1
        key.angle = math.radians(6)
        ob = bpy.data.objects.new("key", key)
        bpy.context.collection.objects.link(ob)
        # Keyed from the south-east so the street elevation is lit, the
        # archivolt throws a shadow inside the arch, and the tile eave casts a
        # line down the facade — the three things being judged.
        ob.rotation_euler = (math.radians(48), 0, math.radians(140))

        fill = bpy.data.lights.new("fill", "SUN")
        fill.energy = 0.55
        fill.angle = math.radians(35)
        ob2 = bpy.data.objects.new("fill", fill)
        bpy.context.collection.objects.link(ob2)
        ob2.rotation_euler = (math.radians(65), 0, math.radians(310))

        rim = bpy.data.lights.new("rim", "SUN")
        rim.energy = 0.45
        rim.color = (1.0, 0.93, 0.82)
        ob3 = bpy.data.objects.new("rim", rim)
        bpy.context.collection.objects.link(ob3)
        ob3.rotation_euler = (math.radians(78), 0, math.radians(230))

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
    """Preview the app's night pass. glTF writes emissiveFactor = 0 when the
    authored emission strength is 0, so a re-imported _Glow material carries a
    DEFAULT WHITE emission — raising Emission Strength alone renders every glow
    surface as a white slab. Copy Base Color into Emission Color first, which is
    also exactly what the app does (its night layer is an unlit overlay drawn at
    the material's own baked colour). See docs/asset-plans/README.md."""
    for mat, bsdf in glow_materials():
        if not bsdf:
            continue
        base = bsdf.inputs["Base Color"].default_value
        bsdf.inputs["Emission Color"].default_value = (base[0], base[1], base[2], 1.0)
        bsdf.inputs["Emission Strength"].default_value = 3.5


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

    glb = arg("--glb", os.path.join(here, "160-south-park.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "160-south-park")
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

    # --- the street elevation, square-on and at its own scale ---------------
    # Rendered first because it is what gets iterated on.
    if only in (None, "facade", "aerial"):
        a = math.radians(FRONT_AZ)
        fc = make_camera("cam_facade")
        fc.data.type = "ORTHO"
        fc.data.ortho_scale = 12.0   # portrait frame: this is the VERTICAL extent
        # Aim at the FRONTAGE MIDPOINT, not the body centre: the facade is at
        # one end of a 26 m strip and centring on the strip puts it off-frame.
        # FRONT_MID is the frontage chord's midpoint in model coordinates —
        # the design polygon's front chord midpoint less the build's recentring
        # shift. Hard-coded rather than derived from the bbox, because the bbox
        # of a bent strip says nothing about where its short end is.
        front = Vector((FRONT_MID[0], FRONT_MID[1], height / 2))
        fc.location = Vector(
            (front.x + 60.0 * math.sin(a), front.y + 60.0 * math.cos(a), height / 2)
        )
        aim(fc, front)
        render_to(os.path.join(out, f"{prefix}-facade.png"), fc, FACADE_RES)

    # --- beauty render from the app's high three-quarter aerial camera -----
    if only in (None, "aerial"):
        aer = make_camera("cam_aerial")
        aer.data.type = "PERSP"
        aer.data.lens = 78.0  # long lens, restrained perspective (style bible §18)
        aer.location = orbit(center, AERIAL_AZ, AERIAL_PITCH, span * AERIAL_R)
        aim(aer, Vector((center.x, center.y, center.z * 0.92)))
        render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)

    if only == "aerial" or only == "facade":
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

    # --- top view: the bend, the flat roof and the tile band ---------------
    # Rolled to the building's axis so the sliver runs up the frame with the
    # street end at the bottom, rather than diagonally across it.
    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.ortho_scale = 30.0   # portrait frame: this is the VERTICAL extent
    top.location = Vector((center.x, center.y, mx.z + span))
    # For a top-down camera at rotation (0, 0, rz), image-up maps to world
    # (-sin rz, cos rz). Setting rz = -LONG_AXIS puts image-up along the FRONT ->
    # REAR direction, so the strip runs up the frame with the street end and its
    # tile band at the bottom — the way the app's camera meets it coming across
    # the park. LONG_AXIS +/- 90 lays the strip across the frame instead.
    top.rotation_euler = (0, 0, math.radians(-LONG_AXIS))
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)


if __name__ == "__main__":
    main()
