"""Render controlled review views of the exact exported City Hall GLB.

    blender -b --python render_city_hall.py -- [--glb FILE] [--out DIR]

The four elevations share orthographic scale, framing, lighting, and exposure.
Compass labels name the camera's true-world position; +Y is true north.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

ELEV_RES = (1600, 900)
AER_RES = (1600, 1200)
TOP_RES = (1400, 1400)
BG = (0.86, 0.80, 0.69, 1.0)
VIEWS = [("north", 0.0), ("east", 90.0), ("south", 180.0), ("west", 270.0)]


def aim(obj, target):
    obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()


def make_camera(name):
    cam = bpy.data.cameras.new(name)
    cam.clip_start = 1.0; cam.clip_end = 5000
    obj = bpy.data.objects.new(name, cam)
    bpy.context.collection.objects.link(obj)
    return obj


def bounds(objects):
    mn = Vector((1e9, 1e9, 1e9)); mx = Vector((-1e9, -1e9, -1e9))
    for obj in objects:
        for corner in obj.bound_box:
            p = obj.matrix_world @ Vector(corner)
            for i in range(3):
                mn[i] = min(mn[i], p[i]); mx[i] = max(mx[i], p[i])
    return mn, mx


def setup_world(span):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.resolution_percentage = 100
    scene.view_settings.look = "None"
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.exposure = 0.25
    scene.world = bpy.data.worlds.new("Warm studio")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = BG; bg.inputs[1].default_value = 0.6

    key = bpy.data.lights.new("key", "AREA"); key.energy = 1900; key.shape = "DISK"; key.size = span * 0.7
    key_obj = bpy.data.objects.new("key", key); bpy.context.collection.objects.link(key_obj)
    key_obj.location = (-span * 0.7, -span * 0.8, span * 0.9); aim(key_obj, Vector((0, 0, 30)))
    fill = bpy.data.lights.new("fill", "AREA"); fill.energy = 950; fill.size = span * 0.6
    fill_obj = bpy.data.objects.new("fill", fill); bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (span * 0.75, span * 0.25, span * 0.55); aim(fill_obj, Vector((0, 0, 28)))
    sun = bpy.data.lights.new("rim", "SUN"); sun.energy = 1.4; sun.angle = math.radians(10)
    sun_obj = bpy.data.objects.new("rim", sun); bpy.context.collection.objects.link(sun_obj)
    sun_obj.rotation_euler = (math.radians(42), 0, math.radians(135))

    bpy.ops.mesh.primitive_plane_add(size=span * 4, location=(0, 0, -0.04))
    floor = bpy.context.object; floor.name = "studio_floor"
    mat = bpy.data.materials.new("Studio_Table"); mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.58, 0.49, 0.37, 1)
    bsdf.inputs["Roughness"].default_value = 0.95
    floor.data.materials.append(mat)


def render(path, camera, resolution):
    scene = bpy.context.scene
    scene.camera = camera
    scene.render.resolution_x, scene.render.resolution_y = resolution
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print(f"[render] {path}")


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    def arg(flag, default): return argv[argv.index(flag) + 1] if flag in argv else default
    glb = arg("--glb", os.path.join(here, "city-hall.glb"))
    out = arg("--out", here); os.makedirs(out, exist_ok=True)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    mn, mx = bounds(meshes); dims = mx - mn
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    span = max(dims.x, dims.y)
    setup_world(span)

    aspect = ELEV_RES[0] / ELEV_RES[1]
    ortho_scale = max(span * 1.18, dims.z * aspect * 1.25)
    distance = span * 2.7
    for name, azimuth in VIEWS:
        a = math.radians(azimuth)
        cam = make_camera("cam_" + name); cam.data.type = "ORTHO"; cam.data.ortho_scale = ortho_scale
        cam.location = Vector((center.x + distance * math.sin(a), center.y + distance * math.cos(a), center.z + 2.0))
        aim(cam, center)
        render(os.path.join(out, f"city-hall-{name}.png"), cam, ELEV_RES)

    top = make_camera("cam_top"); top.data.type = "ORTHO"; top.data.ortho_scale = span * 1.18
    top.location = Vector((center.x, center.y, mx.z + span * 1.2)); top.rotation_euler = (0, 0, 0)
    render(os.path.join(out, "city-hall-top.png"), top, TOP_RES)

    # Southeast/Plaza-facing beauty view: 39 degrees down with a long lens.
    aerial = make_camera("cam_aerial"); aerial.data.type = "PERSP"; aerial.data.lens = 78
    pitch = math.radians(39); azimuth = math.radians(135); radius = span * 3.1
    aerial.location = Vector((center.x + radius * math.cos(pitch) * math.sin(azimuth),
                              center.y + radius * math.cos(pitch) * math.cos(azimuth),
                              center.z + radius * math.sin(pitch)))
    aim(aerial, Vector((center.x, center.y, 25.0)))
    render(os.path.join(out, "city-hall-aerial.png"), aerial, AER_RES)


if __name__ == "__main__":
    main()
