"""Review renders of the exported street kit GLBs.

    blender -b --python render_streetkit.py -- [--kit DIR] [--out DIR]

Every piece is re-imported from its exported GLB into an empty scene and shot
from the app's own diorama camera angle (42 degrees down, three-quarter yaw), so
the images show exactly the geometry that ships, judged from the angle the
style bible says to judge it from.
"""

import json
import math
import os
import sys

import bpy
from mathutils import Vector

RES = (520, 620)
BG = (0.86, 0.80, 0.69, 1.0)
PITCH = math.radians(42)
YAW = math.radians(35)


def setup_world():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    scene.view_settings.view_transform = "Standard"
    world = bpy.data.worlds.new("Studio")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = BG
    bg.inputs[1].default_value = 0.35


def add_lights(size):
    key = bpy.data.lights.new("key", "SUN")
    key.energy = 2.4
    key.angle = math.radians(8)
    ob = bpy.data.objects.new("key", key)
    bpy.context.collection.objects.link(ob)
    ob.rotation_euler = (math.radians(50), 0, math.radians(-40))

    fill = bpy.data.lights.new("fill", "SUN")
    fill.energy = 0.6
    fill.angle = math.radians(40)
    ob2 = bpy.data.objects.new("fill", fill)
    bpy.context.collection.objects.link(ob2)
    ob2.rotation_euler = (math.radians(66), 0, math.radians(135))

    bpy.ops.mesh.primitive_plane_add(size=max(12.0, size * 6), location=(0, 0, -0.005))
    plane = bpy.context.object
    mat = bpy.data.materials.new("Studio_Table")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes["Principled BSDF"]
    nodes.inputs["Base Color"].default_value = (0.66, 0.60, 0.50, 1.0)
    nodes.inputs["Roughness"].default_value = 0.95
    plane.data.materials.append(mat)


def render_piece(glb, out_path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    setup_world()
    bpy.ops.import_scene.gltf(filepath=glb)
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    size = max((mx - mn).x, (mx - mn).y, (mx - mn).z)
    centre = (mn + mx) / 2
    add_lights(size)

    cam = bpy.data.cameras.new("cam")
    cam.type = "ORTHO"
    cam.ortho_scale = size * 1.5
    cam.clip_start = 0.01
    cam.clip_end = 500
    ob = bpy.data.objects.new("cam", cam)
    bpy.context.collection.objects.link(ob)
    dist = size * 4 + 6
    ob.location = centre + Vector(
        (
            math.sin(YAW) * math.cos(PITCH) * dist,
            -math.cos(YAW) * math.cos(PITCH) * dist,
            math.sin(PITCH) * dist,
        )
    )
    direction = centre - ob.location
    ob.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    scene = bpy.context.scene
    scene.camera = ob
    scene.render.resolution_x, scene.render.resolution_y = RES
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    print(f"[render] {out_path}")


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    kit = arg(
        "--kit",
        os.path.abspath(os.path.join(here, "..", "..", "app", "public", "sf-assets", "streetkit")),
    )
    out = arg("--out", os.path.join(here, "renders"))
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(kit, "streetkit_index.json"), encoding="utf8") as fh:
        index = json.load(fh)
    only = arg("--only", None)
    for piece in index["pieces"]:
        if only and piece["id"] != only:
            continue
        render_piece(os.path.join(kit, piece["file"]), os.path.join(out, f"{piece['id']}.png"))


if __name__ == "__main__":
    main()
