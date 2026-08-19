"""Controlled review renders of the exported "The Towers at Rincon" GLB.

    blender -b --python render_towers_at_rincon.py -- [--glb FILE] [--out DIR]
                                          [--prefix towers-at-rincon] [--night]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth.

The block is a diamond at 45 deg to the world axes, so the four cameras are
aligned to the STREETS rather than to true compass points - otherwise every
"elevation" would be an oblique three-quarter and a reviewer could not compare
opposite faces. Each view keeps the nearest compass filename:

    -south.png  HOWARD STREET, faces 135 deg - the address elevation, the
                entrance canopy and the arched window, the west tower behind
    -east.png   STEUART STREET, faces 45 deg - the water side, where the east
                tower stands full height over the street
    -west.png   SPEAR STREET, faces 225 deg - the west tower's bow
    -north.png  faces 315 deg - the Rincon Annex party side and the mouth of
                the open garden courtyard

Plus -facade.png, a square-on long-lens look at the Howard elevation, and
-top.png, which is what the app's camera mostly sees: two tower roofs with their
arched caps, and the courtyard cut into the block.

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
TOP_RES = (1300, 1300)   # the cornice ring and its seven bulges
BG = (0.86, 0.80, 0.69, 1.0)  # neutral warm tabletop background

FRONT_AZ = 135.0         # the South Park elevation faces north-west
LONG_AXIS = 315.0        # front -> rear bearing

# Azimuths are the bearings each elevation FACES, so the camera stands on that
# side looking back at the building.
VIEWS = [
    ("south", 135.0),   # HOWARD STREET, the address elevation
    ("east", 45.0),     # STEUART STREET, the water side - the second hero
    ("west", 225.0),    # SPEAR STREET
    ("north", 315.0),   # the Rincon Annex party side, and the courtyard mouth
]

# Straight over the WEST corner, on the bisector of the two hero elevations
# (315.8 and 225.8). This is the only azimuth that reads all three things that
# matter at once: the park front, the 17.7 m alley flank running away, and the
# rounded corner turret that joins them and carries the crown. It is also the
# view the app's own camera preset is set to (landmarks.mjs yaw 270).
AERIAL_AZ = 90.0
AERIAL_PITCH = 36.0
AERIAL_R = 2.10


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
    scene.cycles.samples = 48
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
        # Keyed from the north-west so the park front catches the light and the
        # cornice and the seven bay caps all throw shadows down the facade.
        ob.rotation_euler = (math.radians(50), 0, math.radians(340))

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
            # 3.2, the 106 South Park value, for the same reason: the lit
            # windows are Toy_glassl_Glow (6f95b8) and a stronger push blows
            # them to flat white. The first pass here used 4.2, which was
            # covering for a glow colour that was too dark to read in the app -
            # exactly the flattery a night render must not provide. See
            # REPORT.md 6.
            bsdf.inputs["Emission Strength"].default_value = 3.2


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

    glb = arg("--glb", os.path.join(here, "towers-at-rincon.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "towers-at-rincon")
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
    ortho_scale = span * 1.18
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

    # --- top view: the cornice RING with its three rounded and four canted
    # bulges, the roof furniture, and the turret crown. Rolled to the building's
    # axis so the box sits square in frame with the park front at the top.
    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.ortho_scale = 125.0   # portrait frame: this is the VERTICAL extent
    top.location = Vector((center.x, center.y, mx.z + span))
    # Roll so image-up is the front direction (bearing LONG_AXIS + 180), i.e.
    # the street end at the top of the frame. For a top-down camera image-up
    # maps to world (-sin rz, cos rz), which gives rz = LONG_AXIS - 90.
    top.rotation_euler = (0, 0, math.radians(LONG_AXIS - 90.0))
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- beauty render from the app's high three-quarter aerial camera -----
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 78.0  # long lens, restrained perspective (style bible §18)
    aer.location = orbit(center, AERIAL_AZ, AERIAL_PITCH, span * AERIAL_R)
    aim(aer, Vector((center.x, center.y, center.z * 0.92)))
    render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)

    # --- square-on look at the 315.8 deg park front ------------------------
    # The four cardinal elevations all take this building obliquely; this is the
    # frame a reviewer judges the facade from. Long lens, slight downward tilt
    # so the cornice and the roof edge read.
    fac = make_camera("cam_facade")
    fac.data.type = "PERSP"
    fac.data.lens = 110.0
    fac.location = orbit(center, FRONT_AZ, 12.0, span * 3.2)
    aim(fac, Vector((center.x, center.y, mn.z + height * 0.48)))
    render_to(os.path.join(out, f"{prefix}-facade.png"), fac, (900, 1200))


if __name__ == "__main__":
    main()
