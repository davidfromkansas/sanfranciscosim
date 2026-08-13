"""Controlled review renders of the exported Herbst Theatre (War Memorial Veterans Building) GLB.

    blender -b --python render_war_memorial_opera_house.py -- [--glb FILE] [--out DIR]
                                                     [--prefix herbst-theatre]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth; directions are true compass directions
(north = Blender +Y, how the asset is authored). The building axis actually bears
81 deg, so the east/west views face the colonnade front and Franklin rear a few degrees
off-axis, exactly as the city camera would.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (1600, 1100)
AER_RES = (1500, 1150)
TOP_RES = (1600, 900)
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


def add_lights(height):
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
    bpy.ops.mesh.primitive_plane_add(size=height * 10, location=(0, 0, -0.02))
    plane = bpy.context.object
    plane.name = "studio_floor"
    mat = bpy.data.materials.new("Studio_Table")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (
        0.62, 0.55, 0.45, 1.0,
    )
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
    plane.data.materials.append(mat)
    return plane


def day_state():
    """Mimic the app's DAYTIME appearance of _Glow surfaces.

    The loader draws every *_Glow material as a separate unlit overlay whose
    opacity is `0.12 + 0.95 * uNight` (app/src/kit.js updateLandmarkGlow), so
    by day a glow shell is only 12% present. The shipped GLB is fully opaque
    (contract); this transparency exists in the render scene ONLY, so the day
    images show what the city actually shows.
    """
    for mat in bpy.data.materials:
        if mat.name.endswith("_Glow") and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Alpha"].default_value = 0.12


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

    glb = arg("--glb", os.path.join(here, "herbst-theatre.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "herbst-theatre")
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    day_state()
    height = mx.z - mn.z
    span = max(mx.x - mn.x, mx.y - mn.y)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world()
    add_lights(height)

    # --- four elevations: one rig, identical everything but azimuth ---------
    ortho_scale = span * 1.08          # one shared scale so all four compare
    dist = span * 3.0
    for name, az in VIEWS:
        cam = make_camera(f"cam_{name}")
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = ortho_scale
        a = math.radians(az)
        cam.location = Vector(
            (center.x + dist * math.sin(a), center.y + dist * math.cos(a),
             center.z + height * 0.02)
        )
        aim(cam, center)
        render_to(os.path.join(out, f"{prefix}-{name}.png"), cam, RES)

    # --- top view: the roofscape design -------------------------------------
    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.ortho_scale = span * 1.12
    top.location = Vector((center.x, center.y, mx.z + span))
    top.rotation_euler = (0, 0, math.radians(-81.11) + math.pi / 2)
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- beauty render from the app's high three-quarter aerial camera ------
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 88.0               # long lens, restrained perspective (s.18)
    pitch = math.radians(38)           # 30-50 deg downward
    az = math.radians(112)             # from the ESE: entrance front + memorial-court flank
    r = span * 3.15
    aer.location = Vector(
        (
            center.x + r * math.cos(pitch) * math.sin(az),
            center.y + r * math.cos(pitch) * math.cos(az),
            center.z + r * math.sin(pitch),
        )
    )
    aim(aer, Vector((center.x, center.y, mn.z + height * 0.30)))
    render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)

    # --- night state: simulate the app's dusk system ------------------------
    # In the app every *_Glow material is drawn as an UNLIT overlay whose
    # opacity rises with the real SF sun elevation; full night = the glow
    # surfaces self-luminous at their baked colour. Here: emission on for
    # *_Glow, a dim cool moon key, and a deep dusk sky.
    world = bpy.context.scene.world
    bgn = world.node_tree.nodes["Background"]
    bgn.inputs[0].default_value = (0.012, 0.020, 0.045, 1.0)
    bgn.inputs[1].default_value = 0.22
    for light in bpy.data.lights:
        if light.name == "key":
            light.energy = 0.28
            light.color = (0.62, 0.72, 1.0)          # moonlight
        elif light.name == "fill":
            light.energy = 0.06
            light.color = (0.5, 0.6, 0.9)
        else:
            light.energy = 0.0
    for mat in bpy.data.materials:
        if mat.name.endswith("_Glow") and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Alpha"].default_value = 1.0     # uNight -> 1
                # The GLB ships emission OFF (contract), so its emissiveFactor
                # is (0,0,0) and the glTF importer defaults Emission Color to
                # WHITE - driving strength alone would light every pane white
                # and misrepresent the asset. The app's glow layer uses each
                # surface's own baked colour, so take emission from Base Color.
                base = bsdf.inputs["Base Color"].default_value
                bsdf.inputs["Emission Color"].default_value = base
                # Kept low on purpose: the app's glow layer is UNLIT and casts
                # no light, so a Cycles emission strong enough to spill across
                # the stonework would flatter the asset into something the city
                # never shows.
                bsdf.inputs["Emission Strength"].default_value = {
                    "Toy_white_Glow": 3.4,      # colonnade floodlight soffit strip
                }.get(mat.name, 2.4)            # lit arch panes
    render_to(os.path.join(out, f"{prefix}-night.png"), aer, AER_RES)

    # night entrance closeup: the floodlit colonnade from Van Ness
    ncam = make_camera("cam_night_east")
    ncam.data.type = "PERSP"
    ncam.data.lens = 60.0
    pitch_n = math.radians(12)
    az_n = math.radians(85)
    # Distance from the SPAN, not the height: this building is short and
    # wide (31 x 67 m), so a height-derived distance framed four bays.
    rn = max(height * 2.0, span * 1.55)
    ncam.location = Vector(
        (
            center.x + rn * math.cos(pitch_n) * math.sin(az_n),
            center.y + rn * math.cos(pitch_n) * math.cos(az_n),
            mn.z + rn * math.sin(pitch_n),
        )
    )
    aim(ncam, Vector((center.x, center.y, mn.z + height * 0.38)))
    render_to(os.path.join(out, f"{prefix}-night-east.png"), ncam, (1300, 1100))


if __name__ == "__main__":
    main()
