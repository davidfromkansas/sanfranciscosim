"""Controlled review renders of the exported de Young Museum GLB.

    blender -b --python render_de_young.py -- [--glb FILE] [--out DIR]
                                               [--prefix de-young]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth; directions are true compass directions
(north = Blender +Y), which is how the asset is authored.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (1500, 900)  # landscape: the museum is long and low
AER_RES = (1400, 1200)
TOP_RES = (1300, 1300)
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
    # Emulate the app's DAY state: the loader draws `_Glow` faces in an unlit
    # bucket at 12% opacity (kit.js updateLandmarkGlow), so by day the dark
    # glass backing panes read through them.
    for mat in bpy.data.materials:
        if mat.name.endswith("_Glow") and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Alpha"].default_value = 0.13
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


def add_lights(size):
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


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "de-young.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "de-young")
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    span = max(mx.x - mn.x, mx.y - mn.y)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world()
    add_lights(span)

    # --- four elevations: one rig, identical everything but azimuth ---------
    ortho_scale = span * 1.10
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

    # --- top view: roof planes, courtyard voids and the twisted tower head --
    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.ortho_scale = span * 1.12
    top.location = Vector((center.x, center.y, mx.z + span))
    top.rotation_euler = (0, 0, 0)
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- beauty render from the app's high three-quarter aerial camera ------
    # From the south-east: the Music-Concourse front, the entrance cut and
    # the tower at the NE end all in one view (style bible s.18).
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 105.0  # long lens, restrained perspective
    pitch = math.radians(38)  # 30-50 deg downward
    az = math.radians(140)
    r = span * 3.4
    aer.location = Vector(
        (
            center.x + r * math.cos(pitch) * math.sin(az),
            center.y + r * math.cos(pitch) * math.cos(az),
            center.z + r * math.sin(pitch),
        )
    )
    aim(aer, Vector((center.x, center.y, center.z * 0.6)))
    render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)

    # --- night state preview -------------------------------------------------
    # Emulates the app at uNight = 1: `_Glow` materials render unlit at their
    # flat colour (the loader's MeshBasicMaterial bucket), the body sits in a
    # cool moonlit key, and the night floor stays readable (testing skill:
    # zenith no darker than #1a2340).
    to_night(span)
    render_to(os.path.join(out, f"{prefix}-night.png"), aer, AER_RES)


def to_night(span):
    scene = bpy.context.scene
    world = scene.world
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.055, 0.072, 0.14, 1.0)  # app night zenith floor
    bg.inputs[1].default_value = 0.55

    for ob in list(bpy.data.objects):
        if ob.type == "LIGHT":
            bpy.data.objects.remove(ob, do_unlink=True)
    moon = bpy.data.lights.new("moon", "SUN")
    moon.energy = 0.32
    moon.angle = math.radians(3)
    moon.color = (0.72, 0.80, 1.0)
    ob = bpy.data.objects.new("moon", moon)
    bpy.context.collection.objects.link(ob)
    ob.rotation_euler = (math.radians(55), 0, math.radians(150))

    floor_mat = bpy.data.materials.get("Studio_Table")
    if floor_mat:
        floor_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (
            0.045, 0.055, 0.085, 1.0,
        )

    for mat in bpy.data.materials:
        if not mat.name.endswith("_Glow") or not mat.use_nodes:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if not bsdf:
            continue
        base = list(bsdf.inputs["Base Color"].default_value)[:3]
        # The app renders glow as UNLIT flat colour (no bounce light), so the
        # preview keeps emission modest rather than flooding the courts.
        bsdf.inputs["Alpha"].default_value = 1.0  # night: full-strength glow
        bsdf.inputs["Emission Color"].default_value = (*base, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 3.5 if "white" in mat.name else 1.7

    # a touch of fog-glow bloom sells the lantern; skip silently if the
    # compositor API differs
    try:
        scene.use_nodes = True
        tree = scene.node_tree
        tree.nodes.clear()
        layers = tree.nodes.new("CompositorNodeRLayers")
        glare = tree.nodes.new("CompositorNodeGlare")
        glare.glare_type = "FOG_GLOW"
        glare.quality = "HIGH"
        glare.mix = -0.4
        glare.threshold = 1.0
        comp = tree.nodes.new("CompositorNodeComposite")
        tree.links.new(layers.outputs["Image"], glare.inputs["Image"])
        tree.links.new(glare.outputs["Image"], comp.inputs["Image"])
    except Exception as exc:  # pragma: no cover - compositor API drift
        print(f"[render] no bloom ({exc})")


if __name__ == "__main__":
    main()
