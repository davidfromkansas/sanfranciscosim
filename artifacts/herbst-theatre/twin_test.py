"""The twin test: render the Herbst Theatre GLB beside the War Memorial Opera
House GLB, both at scale 1.0, at their real relative position and bearing.

    blender -b --python twin_test.py -- [--out DIR]

`docs/asset-plans/herbst-theatre.md` makes this a gate, not a nicety. The two
buildings are officially "substantially identical structures" (SF Landmark #84),
so the asset is only correct if the base course, the cornice line and the roof
colour line up across the memorial court. This script proves it by placing both
exported GLBs the way `placeGeneric` will: each is dropped so its bbox CENTRE
sits on its manifest anchor, projected with the repo's own local tangent
projection. Nothing is nudged.

Note on appearance: this rig deliberately does NOT apply the day-state glow
alpha (0.12) that `render_herbst_theatre.py` uses, so the `_Glow` panes read at
full opacity in both models. That is not the app's daytime look — it is here
because the lit arches make the bay rhythms and the cornice line far easier to
compare between the two buildings, which is the only thing this gate judges.
Both assets are treated identically, so the comparison stays valid.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

# Manifest anchors: Opera House from its shipped entry, Herbst from its REPORT.
OPERA = ("../war-memorial-opera-house/war-memorial-opera-house.glb",
         -122.4209170, 37.7786126)
HERBST = ("herbst-theatre.glb", -122.4210157, 37.7795789)

# app/src/data.js projection, verbatim (AGENTS: ONE projection function).
LON0, LAT0 = -122.4375, 37.77
KX = 111320.0 * math.cos(math.radians(LAT0))
KY = 110540.0


def project(lon, lat):
    return ((lon - LON0) * KX, -(lat - LAT0) * KY)


def bbox(objs):
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    return mn, mx


def place(path, lon, lat):
    """Import and translate so the bbox centre lands on the anchor. Blender is
    +Y north / +X east; the app is +X east / -Z north, so the app's z maps to
    Blender's -y."""
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    objs = [o for o in set(bpy.data.objects) - before if o.type == "MESH"]
    mn, mx = bbox(objs)
    x, z = project(lon, lat)
    off = Vector((x - (mn.x + mx.x) / 2, -z - (mn.y + mx.y) / 2, -mn.z))
    for o in objs:
        o.location += off
    return objs, mn, mx


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    out = argv[argv.index("--out") + 1] if "--out" in argv else here

    bpy.ops.wm.read_factory_settings(use_empty=True)
    for rel, lon, lat in (OPERA, HERBST):
        objs, mn, mx = place(os.path.join(here, rel), lon, lat)
        print(f"[twin] {os.path.basename(rel)}  height={mx.z - mn.z:.3f} m  "
              f"objects={len(objs)}")

    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    scene.view_settings.view_transform = "Standard"
    world = bpy.data.worlds.new("Studio")
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (
        0.86, 0.80, 0.69, 1.0)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.30

    for name, energy, rot in (
        ("key", 2.1, (52, 0, -38)),
        ("fill", 0.55, (65, 0, 140)),
    ):
        light = bpy.data.lights.new(name, "SUN")
        light.energy = energy
        light.angle = math.radians(6 if name == "key" else 35)
        ob = bpy.data.objects.new(name, light)
        bpy.context.collection.objects.link(ob)
        ob.rotation_euler = tuple(math.radians(a) for a in rot)

    bpy.ops.mesh.primitive_plane_add(size=1200, location=(0, 0, -0.02))
    mat = bpy.data.materials.new("Studio_Table")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (
        0.62, 0.55, 0.45, 1.0)
    bpy.context.object.data.materials.append(mat)

    meshes = [o for o in bpy.data.objects if o.type == "MESH"
              and o.name != "Plane"]
    mn, mx = bbox(meshes)
    centre = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    span = max(mx.x - mn.x, mx.y - mn.y)

    def shoot(name, cam, res):
        scene.camera = cam
        scene.render.resolution_x, scene.render.resolution_y = res
        scene.render.image_settings.file_format = "PNG"
        scene.render.filepath = os.path.join(out, name)
        bpy.ops.render.render(write_still=True)
        print(f"[twin] {scene.render.filepath}")

    # 1. The pair from the app's high three-quarter aerial, over the court.
    cam = bpy.data.cameras.new("aerial")
    cam.lens = 90.0
    cam.clip_end = 20000
    ob = bpy.data.objects.new("aerial", cam)
    bpy.context.collection.objects.link(ob)
    pitch, az, r = math.radians(34), math.radians(104), span * 2.6
    ob.location = Vector((centre.x + r * math.cos(pitch) * math.sin(az),
                          centre.y + r * math.cos(pitch) * math.cos(az),
                          mn.z + r * math.sin(pitch)))
    d = Vector((centre.x, centre.y, mn.z + 18)) - ob.location
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    shoot("herbst-theatre-twin-aerial.png", ob, (1600, 1100))

    # 2. Straight-on from Van Ness: the cornice-line alignment gate. Ortho, so
    #    a mismatch of even a metre is unmissable.
    cam2 = bpy.data.cameras.new("front")
    cam2.type = "ORTHO"
    cam2.ortho_scale = span * 1.05
    cam2.clip_end = 20000
    ob2 = bpy.data.objects.new("front", cam2)
    bpy.context.collection.objects.link(ob2)
    a = math.radians(81.11)          # look due west along the shared bearing
    ob2.location = Vector((centre.x + 900 * math.sin(a),
                           centre.y + 900 * math.cos(a), mn.z + 16))
    d2 = Vector((centre.x, centre.y, mn.z + 16)) - ob2.location
    ob2.rotation_euler = d2.to_track_quat("-Z", "Y").to_euler()
    shoot("herbst-theatre-twin-front.png", ob2, (1900, 800))


if __name__ == "__main__":
    main()
