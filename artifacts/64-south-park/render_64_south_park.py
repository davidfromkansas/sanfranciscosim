"""Controlled review renders of the exported South Park GLB.

    blender -b --python render_64_south_park.py -- [--glb FILE] [--out DIR]
                                              [--prefix 64-south-park] [--night]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships.

Subject-specific choices, all of them consequences of the park being a 159.5 x
23.5 m lozenge lying at 45.47 deg to the world axes:

* the four elevations are taken along the PARK's own axes, not the compass, and
  are named for the end or side they face: `ne-end` (Second Street), `sw-end`
  (Third Street), `nw-side` (Bryant side), `se-side` (Brannan side). A compass
  set would show four identical oblique views of the same lozenge.
* the TOP view is the primary review image, and the camera is ROLLED by
  90 - 45.4669 deg so the park lies horizontally in frame. Unrolled it runs
  corner to corner of a square and half the pixels are empty table. It must
  resolve into the six shapes of plan 2.9: kerb oval, bone ribbon, anthracite
  circle, five mint lawns, teal edge beds, grey-green crowns.
* the aerial stands to the SOUTH-WEST, which is where the app's camera preset
  puts it (yaw 315 = 180 - 225.47), looking north-east along the axis with the
  Shout nearest the camera.

--night previews the app's dusk pass: _Glow materials get their emission turned
up under a dark moonlit world. The night read to check for is ONE lit curve
threading a dark canopy — not a glowing slab, and not a dashed line.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

HEADING_LONG = 45.4669

RES = (1800, 560)          # letterbox: 160 m long and only 15 m tall
AER_RES = (1700, 1000)
TOP_RES = (2200, 560)      # the primary review image, rolled to run landscape
BG = (0.86, 0.80, 0.69, 1.0)

# name, azimuth = compass bearing FROM the park TO the camera
VIEWS = [
    ("ne-end", HEADING_LONG),             # stands off Second Street
    ("se-side", HEADING_LONG + 90.0),     # stands off Brannan
    ("sw-end", HEADING_LONG + 180.0),     # stands off Third Street
    ("nw-side", HEADING_LONG + 270.0),    # stands off Bryant
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


def setup_world(night=False):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 24
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


def add_lights(span, night=False):
    if night:
        moon = bpy.data.lights.new("moon", "SUN")
        moon.energy = 0.12
        moon.color = (0.65, 0.74, 1.0)
        moon.angle = math.radians(10)
        ob = bpy.data.objects.new("moon", moon)
        bpy.context.collection.objects.link(ob)
        ob.rotation_euler = (math.radians(55), 0, math.radians(140))
    else:
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

    bpy.ops.mesh.primitive_plane_add(size=span * 3, location=(0, 0, -0.02))
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
    for mat, bsdf in glow_materials():
        if bsdf:
            bsdf.inputs["Emission Strength"].default_value = 6.0


def fade_glow():
    """Preview the app's DAY state. assets.js/kit.js put _Glow surfaces in a
    separate unlit layer at opacity 0.12 + 0.95*uNight, so by day these shells
    are ~12% alpha and the opaque tablet behind them reads through."""
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


def orbit(center, azimuth_deg, pitch_deg, radius, z_center):
    a = math.radians(azimuth_deg)
    p = math.radians(pitch_deg)
    return Vector((center.x + radius * math.cos(p) * math.sin(a),
                   center.y + radius * math.cos(p) * math.cos(a),
                   z_center + radius * math.sin(p)))


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

    glb = arg("--glb", os.path.join(here, "64-south-park.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "64-south-park")
    night = "--night" in argv
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    height = mx.z - mn.z
    width = max(mx.x - mn.x, mx.y - mn.y)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    long_m = 168.0   # the oriented length plus canopy overhang, for framing only

    def fit_distance(lens_mm, cover_m):
        """Distance at which a `lens_mm` lens covers `cover_m` across the frame.
        The first rig used a multiple of the park length and cropped both ends
        off every perspective view — a 78 mm lens at 252 m covers 116 m, and
        this park is 168 m long."""
        return cover_m / (2.0 * math.tan(math.atan(18.0 / lens_mm)))
    setup_world(night=night)
    add_lights(width, night=night)

    if not night:
        fade_glow()

    if night:
        light_glow()
        aer = make_camera("cam_night")
        aer.data.lens = 78.0
        aer.location = orbit(center, 262.0, 31.0, fit_distance(78.0, long_m * 1.20), mn.z)
        aim(aer, Vector((center.x, center.y, mn.z + 3.0)))
        render_to(os.path.join(out, f"{prefix}-aerial-night.png"), aer, AER_RES)
        return

    # --- four elevations along the park's own axes -------------------------
    for name, az in VIEWS:
        cam = make_camera(f"cam_{name}")
        cam.data.type = "ORTHO"
        # the ends see 23.5 m of park, the sides see 159.5 m; one rig would
        # render the ends as two specks, so each pair gets its own scale.
        end_on = name.endswith("end")
        cam.data.ortho_scale = (long_m * 1.06) if not end_on else (long_m * 0.36)
        cam.location = orbit(center, az, 0.0, long_m * 2.4, center.z)
        # aim() rather than a hand-built euler: setting rotation_euler to
        # (90, 0, az) points the camera 90 degrees off the orbit position, so
        # nw-side and se-side came out as the same image.
        aim(cam, Vector((center.x, center.y, center.z)))
        render_to(os.path.join(out, f"{prefix}-{name}.png"), cam,
                  RES if not end_on else (900, 700))

    # --- top view: THE primary review image, rolled to lie landscape --------
    # A 52-degree key throws 10-sided crown shadows with straight edges across
    # the paving, and in a nadir view those read as black polygons cut into the
    # path. The plan is the subject here, so the top view gets its own near-
    # overhead key and a lifted ambient. Nothing else about the rig changes.
    for lamp in bpy.data.objects:
        if lamp.type == "LIGHT" and lamp.name == "key":
            lamp.rotation_euler = (math.radians(14), 0, math.radians(-38))
        if lamp.type == "LIGHT" and lamp.name == "fill":
            lamp.data.energy = 1.25
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.62

    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.ortho_scale = long_m * 1.04
    top.location = Vector((center.x, center.y, mx.z + width))
    top.rotation_euler = (0, 0, math.radians(90.0 - HEADING_LONG))
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # restore the standard rig for the perspective views
    for lamp in bpy.data.objects:
        if lamp.type == "LIGHT" and lamp.name == "key":
            lamp.rotation_euler = (math.radians(52), 0, math.radians(-38))
        if lamp.type == "LIGHT" and lamp.name == "fill":
            lamp.data.energy = 0.55
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.30

    # --- the app's high three-quarter aerial, from the west-south-west ------
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 78.0
    # 262 deg puts the camera WSW: 36 degrees off the park's own axis, so the
    # lozenge runs diagonally across the frame. Standing at 225 (straight down
    # the axis, where the app's fly-to preset sits) foreshortens 160 m of park
    # into a narrow vertical strip — that view belongs to -axis.png, not here.
    aer.location = orbit(center, 262.0, 34.0, fit_distance(78.0, long_m * 1.20), mn.z)
    aim(aer, Vector((center.x, center.y, mn.z + 3.0)))
    render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)

    # --- the signature composition: low three-quarter looking NORTH-EAST
    # along the park's own axis from the Third Street entry, past the Shout and
    # down the whole 160 m of the promenade. This is the view every photograph
    # of this park is taken from and the one the fly-to preset lands on.
    axis = make_camera("cam_axis")
    axis.data.type = "PERSP"
    axis.data.lens = 95.0
    axis.location = orbit(center, HEADING_LONG + 187.0, 13.0,
                          fit_distance(95.0, long_m * 0.62), mn.z)
    aim(axis, Vector((center.x, center.y, mn.z + 5.0)))
    render_to(os.path.join(out, f"{prefix}-axis.png"), axis, AER_RES)


if __name__ == "__main__":
    main()
