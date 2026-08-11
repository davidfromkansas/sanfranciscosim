"""Controlled renders of the exact exported Painted Ladies GLB.

    blender -b --python render_painted_ladies.py -- [--glb FILE] [--out DIR]

The four elevations share scale, framing, projection, exposure and lighting.
Compass labels describe where the camera stands, using the researched
orientation: +Y is true north and the six facades look west, so the "west"
elevation is the postcard view from Alamo Square Park.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

ELEV_RES = (1800, 900)
AER_RES = (1600, 1200)
TOP_RES = (900, 1500)
BG = (0.86, 0.80, 0.69, 1.0)
# True cardinal azimuths; the row itself sits 9.13 deg off cardinal, which the
# elevations show honestly rather than rotating the model to hide it.
VIEWS = [("north", 0.0), ("east", 90.0), ("south", 180.0), ("west", 270.0)]


def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def import_glb(path):
    bpy.ops.import_scene.gltf(filepath=path)
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for obj in objs:
        for corner in obj.bound_box:
            p = obj.matrix_world @ Vector(corner)
            for i in range(3):
                mn[i] = min(mn[i], p[i])
                mx[i] = max(mx[i], p[i])
    return objs, mn, mx


def setup_world():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.resolution_percentage = 100
    scene.view_settings.look = "None"
    scene.view_settings.view_transform = "Standard"
    scene.world = bpy.data.worlds.new("Studio")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = BG
    bg.inputs[1].default_value = 0.55


def aim(obj, target):
    obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()


def add_lights(span):
    key = bpy.data.lights.new("key", "AREA")
    key.energy = 900 * (span / 45.0) ** 2
    key.shape = "DISK"
    key.size = span * 0.75
    ob = bpy.data.objects.new("key", key)
    bpy.context.collection.objects.link(ob)
    ob.location = (span * -0.70, span * -0.55, span * 0.62)
    aim(ob, Vector((0, 0, 8)))

    fill = bpy.data.lights.new("fill", "AREA")
    fill.energy = 420 * (span / 45.0) ** 2
    fill.size = span * 0.55
    ob2 = bpy.data.objects.new("fill", fill)
    bpy.context.collection.objects.link(ob2)
    ob2.location = (span * 0.65, span * 0.45, span * 0.45)
    aim(ob2, Vector((0, 0, 8)))

    sun = bpy.data.lights.new("rim", "SUN")
    sun.energy = 1.15
    sun.angle = math.radians(9)
    ob3 = bpy.data.objects.new("rim", sun)
    bpy.context.collection.objects.link(ob3)
    ob3.rotation_euler = (math.radians(52), 0, math.radians(215))

    bpy.ops.mesh.primitive_plane_add(size=span * 4, location=(0, 0, -0.03))
    floor = bpy.context.object
    floor.name = "studio_floor"
    mat = bpy.data.materials.new("Studio_Table")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.62, 0.55, 0.45, 1)
    bsdf.inputs["Roughness"].default_value = 0.95
    floor.data.materials.append(mat)


def make_camera(name):
    cam = bpy.data.cameras.new(name)
    cam.clip_start = 1.0
    cam.clip_end = 5000
    obj = bpy.data.objects.new(name, cam)
    bpy.context.collection.objects.link(obj)
    return obj


def render(path, cam, res):
    scene = bpy.context.scene
    scene.camera = cam
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print(f"[render] {path}")


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "painted-ladies.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "painted-ladies")
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    setup_world()
    dims = mx - mn
    span = max(dims.x, dims.y)
    height = dims.z
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    add_lights(span)

    # One shared elevation rig: same ortho scale, distance, lighting and exposure.
    aspect = ELEV_RES[0] / ELEV_RES[1]
    ortho_scale = max(span * 1.10, height * aspect * 1.15)
    dist = span * 3.0
    for name, az in VIEWS:
        cam = make_camera("cam_" + name)
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = ortho_scale
        a = math.radians(az)
        cam.location = Vector(
            (center.x + dist * math.sin(a), center.y + dist * math.cos(a), center.z + 0.5)
        )
        aim(cam, Vector((center.x, center.y, center.z + 0.5)))
        render(os.path.join(out, f"{prefix}-{name}.png"), cam, ELEV_RES)

    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.ortho_scale = max(dims.y, dims.x) * 1.08
    top.location = Vector((center.x, center.y, mx.z + span))
    top.rotation_euler = (0, 0, 0)
    render(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # Aerial beauty shot: over Alamo Square, 38 deg down, long lens.
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 105
    pitch = math.radians(38)
    az = math.radians(248)
    radius = span * 3.4
    aer.location = Vector(
        (
            center.x + radius * math.cos(pitch) * math.sin(az),
            center.y + radius * math.cos(pitch) * math.cos(az),
            center.z + radius * math.sin(pitch),
        )
    )
    aim(aer, Vector((center.x, center.y, center.z + 1.0)))
    render(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)


if __name__ == "__main__":
    main()
