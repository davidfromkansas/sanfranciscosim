"""Controlled review renders of the exported Letterman Digital Arts Center GLB.

    blender -b --python render_letterman_digital_arts_center.py -- [--glb FILE]
                                                            [--out DIR]
                                                            [--prefix NAME]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth; directions are true compass directions
(north = Blender +Y), which is how the asset is authored — so the south and
west views show Building B and the Letterman Drive entrance side.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

# The campus is 312 m wide and 22 m tall: a 4:3 elevation frame would render
# the buildings as a hairline. Elevations get a letterbox frame sized to the
# real aspect, still one shared rig — same scale, lighting and projection.
RES = (1800, 460)
AER_RES = (1400, 1200)
TOP_RES = (1400, 1200)
BG = (0.86, 0.80, 0.69, 1.0)  # neutral warm tabletop background
NIGHT_BG = (0.045, 0.055, 0.10, 1.0)  # deep blue dusk, matching the app's night sky

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


def apply_day():
    """Reproduce the app's DAYTIME treatment of the glow buffer.

    `updateLandmarkGlow` never hides the glow mesh — at noon it still draws at
    opacity 0.12. Rendering those faces opaque would flatter the asset with
    gold windows the scene never shows, so the day renders put the same 0.12
    alpha on every `_Glow` material and let the body geometry read through.
    """
    for mat in bpy.data.materials:
        if not mat.use_nodes or not mat.name.endswith("_Glow"):
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Alpha"].default_value = 0.12


def apply_night():
    """Reproduce the app's night pass on the re-imported materials.

    In the app there is no night mesh and no switch inside the GLB: `assets.js`
    splits the file into a lit body buffer and one unlit glow buffer purely by
    the `_Glow` material-name suffix, and `updateLandmarkGlow` ramps that
    buffer's opacity from 0.12 to 1.0 as `shared.uNight` goes 0 -> 1. Here the
    equivalent is: `_Glow` materials become pure emission at full strength,
    everything else keeps its colour under a dim moonlit key.
    """
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if not bsdf:
            continue
        if mat.name.endswith("_Glow"):
            color = bsdf.inputs["Base Color"].default_value
            bsdf.inputs["Emission Color"].default_value = color
            # The app draws glow faces as flat unlit colour with no bloom, so
            # keep this close to 1.0: a hot value would flatter the asset into
            # something the scene will never show.
            bsdf.inputs["Emission Strength"].default_value = 1.6
        else:
            base = bsdf.inputs["Base Color"].default_value
            bsdf.inputs["Base Color"].default_value = (
                base[0] * 0.36,
                base[1] * 0.40,
                base[2] * 0.52,
                1.0,
            )


def setup_world(night=False):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 128 if night else 64
    scene.cycles.use_denoising = True
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "Standard"
    world = bpy.data.worlds.new("Studio")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = NIGHT_BG if night else BG
    bg.inputs[1].default_value = 0.09 if night else 0.30


def add_lights(size, night=False):
    """Simple tabletop lighting: broad soft key, cool fill, warm rim.

    At night the same rig drops to a dim cool moon key so the emissive
    surfaces — and only those — carry the image.
    """
    dim = 0.10 if night else 1.0
    key = bpy.data.lights.new("key", "SUN")
    key.energy = 2.1 * dim
    key.angle = math.radians(6)
    if night:
        key.color = (0.62, 0.72, 1.0)
    ob = bpy.data.objects.new("key", key)
    bpy.context.collection.objects.link(ob)
    ob.rotation_euler = (math.radians(52), 0, math.radians(-38))

    fill = bpy.data.lights.new("fill", "SUN")
    fill.energy = 0.55 * dim
    fill.angle = math.radians(35)
    if night:
        fill.color = (0.55, 0.66, 1.0)
    ob2 = bpy.data.objects.new("fill", fill)
    bpy.context.collection.objects.link(ob2)
    ob2.rotation_euler = (math.radians(65), 0, math.radians(140))

    rim = bpy.data.lights.new("rim", "SUN")
    rim.energy = 0.45 * dim
    rim.color = (0.6, 0.7, 1.0) if night else (1.0, 0.93, 0.82)
    ob3 = bpy.data.objects.new("rim", rim)
    bpy.context.collection.objects.link(ob3)
    ob3.rotation_euler = (math.radians(78), 0, math.radians(60))

    # A ground catcher gives the contact shadow that sells the miniature.
    bpy.ops.mesh.primitive_plane_add(size=size * 6, location=(0, 0, -0.02))
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

    glb = arg("--glb", os.path.join(here, "letterman-digital-arts-center.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "letterman-digital-arts-center")
    night = "--night" in argv
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    height = mx.z - mn.z
    width = max(mx.x - mn.x, mx.y - mn.y)
    extent = max(width, height)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world(night)
    add_lights(extent, night)

    # Night pass: only the beauty views, so the day contact sheet stays intact.
    if night:
        apply_night()
        aer = make_camera("cam_night")
        aer.data.type = "PERSP"
        aer.data.lens = 105.0
        pitch, az, r = math.radians(34), math.radians(238), extent * 3.4
        aer.location = Vector(
            (
                center.x + r * math.cos(pitch) * math.sin(az),
                center.y + r * math.cos(pitch) * math.cos(az),
                center.z + r * math.sin(pitch),
            )
        )
        aim(aer, Vector((center.x, center.y, center.z * 0.78)))
        render_to(os.path.join(out, f"{prefix}-night.png"), aer, AER_RES)

        elev = make_camera("cam_night_west")
        elev.data.type = "ORTHO"
        elev.data.ortho_scale = width * 1.06
        elev.location = Vector((center.x - extent * 3.0, center.y,
                                mn.z + height * 0.55))
        aim(elev, Vector((center.x, center.y, mn.z + height * 0.55)))
        render_to(os.path.join(out, f"{prefix}-night-west.png"), elev, RES)
        return

    apply_day()

    # --- four elevations: one rig, identical everything but azimuth ---------
    ortho_scale = width * 1.06
    dist = extent * 3.0
    for name, az in VIEWS:
        cam = make_camera(f"cam_{name}")
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = ortho_scale
        a = math.radians(az)
        cam.location = Vector(
            (center.x + dist * math.sin(a), center.y + dist * math.cos(a),
             mn.z + height * 0.55)
        )
        aim(cam, Vector((center.x, center.y, mn.z + height * 0.55)))
        render_to(os.path.join(out, f"{prefix}-{name}.png"), cam, RES)

    # --- top view: the roof design, courtyard, crown --------------------------
    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.ortho_scale = width * 1.25
    top.location = Vector((center.x, center.y, mx.z + height))
    top.rotation_euler = (0, 0, 0)
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- beauty render from the app's high three-quarter aerial camera ------
    # From the south-west so Building B's entrance, the Yoda forecourt, the
    # campus courtyards and the lagoon all read (style bible §18).
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 105.0
    pitch = math.radians(40)
    az = math.radians(235)
    r = extent * 3.4
    aer.location = Vector(
        (
            center.x + r * math.cos(pitch) * math.sin(az),
            center.y + r * math.cos(pitch) * math.cos(az),
            center.z + r * math.sin(pitch),
        )
    )
    aim(aer, Vector((center.x, center.y, center.z * 0.72)))
    render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)


if __name__ == "__main__":
    main()
