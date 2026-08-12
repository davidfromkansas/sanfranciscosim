"""Controlled review renders of the exported Powell cable car GLB.

    blender -b --python render_cable_car.py -- [--glb FILE] [--out DIR]
                                               [--prefix cable-car-powell]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. Blender's glTF importer
converts Y-up back to Z-up, so in this scene the car's front (glTF -Z) is again
Blender +Y.

The four elevations share one orthographic rig and differ only in azimuth. The
aerial uses the app's camera: a long lens at 42 degrees, the pitch
`app/src/camera.js` actually flies the diorama at.

Day images knock every *_Glow material down to alpha 0.12, which is what the
loader's `0.12 + 0.95 * uNight` shows at noon - the shipped GLB is fully opaque
per contract, the transparency lives only in this render scene.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (1500, 900)
AER_RES = (1500, 1050)
TOP_RES = (1500, 620)
BG = (0.86, 0.80, 0.69, 1.0)

# Camera azimuth measured about +Z, 0 = standing at +Y looking back down -Y.
VIEWS = [("front", 0.0), ("right", 90.0), ("rear", 180.0), ("left", 270.0)]


def import_glb(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
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


def setup_world(bg=BG, strength=0.32):
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
    node = world.node_tree.nodes["Background"]
    node.inputs[0].default_value = bg
    node.inputs[1].default_value = strength
    return node


def add_lights(size, floor=True):
    key = bpy.data.lights.new("key", "SUN")
    key.energy = 2.2
    key.angle = math.radians(7)
    ob = bpy.data.objects.new("key", key)
    bpy.context.collection.objects.link(ob)
    ob.rotation_euler = (math.radians(50), 0, math.radians(-42))

    fill = bpy.data.lights.new("fill", "SUN")
    fill.energy = 0.6
    fill.angle = math.radians(38)
    ob2 = bpy.data.objects.new("fill", fill)
    bpy.context.collection.objects.link(ob2)
    ob2.rotation_euler = (math.radians(64), 0, math.radians(135))

    rim = bpy.data.lights.new("rim", "SUN")
    rim.energy = 0.5
    rim.color = (1.0, 0.93, 0.82)
    ob3 = bpy.data.objects.new("rim", rim)
    bpy.context.collection.objects.link(ob3)
    ob3.rotation_euler = (math.radians(76), 0, math.radians(64))

    if floor:
        bpy.ops.mesh.primitive_plane_add(size=size * 8, location=(0, 0, -0.004))
        plane = bpy.context.object
        plane.name = "studio_floor"
        mat = bpy.data.materials.new("Studio_Table")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (0.60, 0.53, 0.43, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.95
        plane.data.materials.append(mat)


def day_state():
    """Glow surfaces are 88% transparent by day in the app; match that here so
    the review images show what the city shows, not what the file contains."""
    for mat in bpy.data.materials:
        if mat.name.endswith("_Glow") and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Alpha"].default_value = 0.12


def night_state(strengths=None):
    """The app's dusk system: *_Glow becomes an opaque UNLIT overlay at its own
    baked colour. The GLB ships emissiveFactor (0,0,0), which makes Blender's
    importer default Emission Color to WHITE, so emission is taken from Base
    Color or every glow surface previews white."""
    strengths = strengths or {"Toy_white_Glow": 4.0, "Toy_mustard_Glow": 3.0}
    for mat in bpy.data.materials:
        if mat.name.endswith("_Glow") and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Alpha"].default_value = 1.0
                bsdf.inputs["Emission Color"].default_value = bsdf.inputs[
                    "Base Color"
                ].default_value
                bsdf.inputs["Emission Strength"].default_value = strengths.get(
                    mat.name, 2.6
                )


def make_camera(name, lens=None, ortho=None):
    cam = bpy.data.cameras.new(name)
    cam.clip_start = 0.05
    cam.clip_end = 4000.0
    if ortho is not None:
        cam.type = "ORTHO"
        cam.ortho_scale = ortho
    else:
        cam.type = "PERSP"
        cam.lens = lens or 85.0
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


def orbit(center, radius, pitch_deg, az_deg):
    p, a = math.radians(pitch_deg), math.radians(az_deg)
    return Vector(
        (
            center.x + radius * math.cos(p) * math.sin(a),
            center.y + radius * math.cos(p) * math.cos(a),
            center.z + radius * math.sin(p),
        )
    )


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "cable-car-powell.glb"))
    out = arg("--out", os.path.join(here, "renders"))
    prefix = arg("--prefix", "cable-car-powell")
    os.makedirs(out, exist_ok=True)

    _, mn, mx = import_glb(glb)
    day_state()
    span = max(mx.x - mn.x, mx.y - mn.y)
    height = mx.z - mn.z
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world()
    add_lights(span)

    # --- elevations: one rig, azimuth only ----------------------------------
    for name, az in VIEWS:
        # ortho_scale spans the LONGER image axis, so an end elevation needs
        # roughly height / (res_y / res_x) or the monitor deck gets cropped.
        scale = span * 1.10 if name in ("left", "right") else height * 2.05
        cam = make_camera(f"cam_{name}", ortho=scale)
        cam.location = orbit(center, span * 3.0, 0.0, az)
        cam.location.z = center.z
        aim(cam, center)
        render_to(os.path.join(out, f"{prefix}-{name}.png"), cam, RES)

    # --- roof: the monitor deck and the letterboards -------------------------
    top = make_camera("cam_top", ortho=span * 1.06)
    top.location = Vector((center.x, center.y, mx.z + span))
    # Turned 90 degrees so the 8.4 m length runs along the image's LONG axis -
    # ortho_scale spans the longer axis, and unturned the car is cropped to a
    # sliver of roof.
    top.rotation_euler = (0, 0, math.radians(90))
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- the app's aerial: 42 degrees, long lens ----------------------------
    aer = make_camera("cam_aerial", lens=90.0)
    aer.location = orbit(center, span * 4.4, 42.0, 128.0)
    aim(aer, Vector((center.x, center.y, mn.z + height * 0.42)))
    render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)

    # --- night: the lit cabin seen THROUGH the open sections ----------------
    bgn = bpy.context.scene.world.node_tree.nodes["Background"]
    bgn.inputs[0].default_value = (0.012, 0.020, 0.045, 1.0)
    bgn.inputs[1].default_value = 0.20
    for light in bpy.data.lights:
        if light.name == "key":
            light.energy = 0.30
            light.color = (0.62, 0.72, 1.0)
        elif light.name == "fill":
            light.energy = 0.07
            light.color = (0.5, 0.6, 0.9)
        else:
            light.energy = 0.0
    night_state()
    render_to(os.path.join(out, f"{prefix}-night.png"), aer, AER_RES)


if __name__ == "__main__":
    main()
