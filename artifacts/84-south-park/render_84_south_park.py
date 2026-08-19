"""Controlled review renders of the exported 84 South Park GLB.

    blender -b --python render_84_south_park.py -- [--glb FILE] [--out DIR]
                                              [--prefix 84-south-park] [--night]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth.

The building sits at 45 deg to the world axes, so the cameras are aligned to the
BUILDING's axes, not to true compass directions — otherwise every "elevation"
would be an oblique three-quarter and a reviewer could not compare opposite
faces. Each view keeps the nearest compass filename:

    -south.png  STREET elevation, faces 135.18 deg (the South Park oval; the
                public face: green wall, projecting box, entrance slot)
    -north.png  REAR elevation, faces 315.18 deg (the two-storey wing and its
                planted terrace)
    -west.png   south-west party flank, faces 225.18 deg (toward 86-96; blind,
                the neighbour is only 0.2 m shorter)
    -east.png   north-east party flank, faces 45.18 deg (toward 76-82; blind,
                the neighbour is 1.6 m taller)

Plus -facade.png, a square-on long-lens look at the street front, and -roof.png,
a tight top-down. Neither party flank is ever seen in the app, so the roof is
this asset's entire silhouette and one small contact-sheet tile is not enough to
judge it.

The building is more than 4x deeper than it is wide, so the elevations are framed
to the long dimension and the two end views carry a lot of empty frame. That is
deliberate: a reviewer has to be able to compare opposite faces at one scale.

--night previews the app's dusk pass: _Glow materials get their emission
turned up under a dark moonlit world, producing <prefix>-aerial-night.png.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (1200, 1000)
AER_RES = (1600, 1200)
TOP_RES = (1000, 1500)   # portrait: the building is a 29.7 m sliver
BG = (0.86, 0.80, 0.69, 1.0)  # neutral warm tabletop background

FRONT_AZ = 135.18        # the street elevation faces south-east
LONG_AXIS = 315.18       # front -> rear bearing

# Azimuths are the bearings each elevation FACES, so the camera stands on that
# side looking back at the building.
VIEWS = [
    ("south", FRONT_AZ),          # street elevation, the public face
    ("north", FRONT_AZ + 180.0),  # rear, on Taber Place
    ("west", 225.18),             # flank toward 86-96, blind
    ("east", 45.18),              # flank toward 76-82, blind
]

# A three-quarter swung round from the facade normal toward the south-west, so
# one frame reads the three things that matter: the street elevation, the 30 m
# depth running away with its step down to the rear wing, and the roof with its
# pergola. Square to the facade (135.18) would flatten the last two, which are
# the recognition cues from the air.
AERIAL_AZ = 172.0
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
        ob.rotation_euler = (math.radians(55), 0, math.radians(200))
    else:
        key = bpy.data.lights.new("key", "SUN")
        key.energy = 2.1
        key.angle = math.radians(6)
        ob = bpy.data.objects.new("key", key)
        bpy.context.collection.objects.link(ob)
        # Keyed from the south-east so the street elevation catches the light
        # and the cornice throws a shadow down the facade.
        ob.rotation_euler = (math.radians(50), 0, math.radians(160))

        fill = bpy.data.lights.new("fill", "SUN")
        fill.energy = 0.55
        fill.angle = math.radians(35)
        ob2 = bpy.data.objects.new("fill", fill)
        bpy.context.collection.objects.link(ob2)
        ob2.rotation_euler = (math.radians(65), 0, math.radians(330))

        rim = bpy.data.lights.new("rim", "SUN")
        rim.energy = 0.45
        rim.color = (1.0, 0.93, 0.82)
        ob3 = bpy.data.objects.new("rim", rim)
        bpy.context.collection.objects.link(ob3)
        ob3.rotation_euler = (math.radians(78), 0, math.radians(250))

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
            # 3.2 (the 106 South Park value) still blew both windows to flat
            # white here: this front has only two lit openings and they are the
            # largest on the building. 2.1 keeps the glass colour readable and
            # keeps the entrance spill from disappearing beside them.
            bsdf.inputs["Emission Strength"].default_value = 2.1


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

    glb = arg("--glb", os.path.join(here, "84-south-park.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "84-south-park")
    night = "--night" in argv
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

    # --- top view: the roof, which IS this asset's silhouette ---------------
    # Rolled to the building's axis so the sliver runs up the frame with the
    # street end at the top, rather than diagonally across it.
    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.ortho_scale = 33.5   # portrait frame: this is the VERTICAL extent
    top.location = Vector((center.x, center.y, mx.z + span))
    # Roll so image-up is the front direction (bearing LONG_AXIS + 180), i.e.
    # the street end at the top of the frame. For a top-down camera image-up
    # maps to world (-sin rz, cos rz), which gives rz = LONG_AXIS - 90.
    top.rotation_euler = (0, 0, math.radians(LONG_AXIS - 90.0))
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- tight top-down: 3x the contact sheet's top tile --------------------
    # Both party flanks are blind, so the roof carries the whole silhouette and
    # the contact-sheet tile is far too small to judge the skylight asymmetry,
    # the pergola's openness or the rear terrace.
    roof = make_camera("cam_roof")
    roof.data.type = "ORTHO"
    roof.data.ortho_scale = 32.0
    roof.location = Vector((center.x, center.y, mx.z + span))
    roof.rotation_euler = (0, 0, math.radians(LONG_AXIS - 90.0))
    render_to(os.path.join(out, f"{prefix}-roof.png"), roof, (1400, 2100))

    # --- beauty render from the app's high three-quarter aerial camera -----
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 78.0  # long lens, restrained perspective (style bible §18)
    aer.location = orbit(center, AERIAL_AZ, AERIAL_PITCH, span * AERIAL_R)
    aim(aer, Vector((center.x, center.y, center.z * 0.92)))
    render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)

    # --- square-on look at the 135 deg street front ------------------------
    # The four cardinal elevations all take this building obliquely; this is the
    # frame a reviewer judges the facade from. Long lens, slight downward tilt
    # so the cornice and the roof edge read.
    fac = make_camera("cam_facade")
    fac.data.type = "PERSP"
    fac.data.lens = 110.0
    fac.location = orbit(center, FRONT_AZ, 12.0, span * 3.6)
    aim(fac, Vector((center.x, center.y, mn.z + height * 0.48)))
    render_to(os.path.join(out, f"{prefix}-facade.png"), fac, (900, 1200))


if __name__ == "__main__":
    main()
