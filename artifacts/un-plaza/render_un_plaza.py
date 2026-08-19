"""Controlled review renders of the exported Civic Center Plaza GLB.

    blender -b --python render_civic_center_plaza.py -- [--glb FILE] [--out DIR]
                                                  [--prefix un-plaza]
                                                  [--night]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth; directions are true compass directions
(north = Blender +Y), which is how the asset is authored - the plaza's long axis
runs 170.94 deg toward Grove Street.

Two subject-specific views beyond the standard set:

* the TOP view is the primary review image for this asset, not a supporting one
  - the plaza is 178 x 121 m and 30 m tall, so the plan IS the design. It is
  rendered larger than the elevations and must resolve into six shapes: two
  green bosque slabs, four bright lawn rectangles, one pale gravel bar, two
  colour playground pads.
* -axis.png is a low three-quarter looking WEST along the central court, the
  real plaza's signature composition (City Hall would fill the far end).

--night previews the app's dusk pass: _Glow materials get their emission
turned up under a dark moonlit world, producing <prefix>-aerial-night.png. The
night read to check for is a lit orthogonal walk grid on a dark field.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (1900, 460)    # extreme letterbox: 215 m across and only 13 m tall
AER_RES = (1700, 1150)
TOP_RES = (2100, 1620)   # the primary review image; landscape, the plaza runs E-W
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


def setup_world(night=False):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    # 24 samples: this asset is flat-colour Lambert-ish geometry under three sun
    # lamps with no GI to converge, so the denoiser resolves it cleanly and the
    # difference from 64 is invisible at review size. It also keeps the eight
    # images tractable on a loaded machine.
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


def add_lights(height, night=False, span=None):
    """Simple tabletop lighting: broad soft key, cool fill, warm rim."""
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

    # A ground catcher gives the contact shadow that sells the miniature.
    # sized off the PLAN, not the height: this asset is 215 m across and 13 m
    # tall, so height*5 left a 65 m table visible as a beige rectangle inside
    # the frame of every review render.
    bpy.ops.mesh.primitive_plane_add(size=max(height * 5, (span or height) * 2.4),
                                     location=(0, 0, -0.02))
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
            bsdf.inputs["Emission Strength"].default_value = 6.0


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

    glb = arg("--glb", os.path.join(here, "un-plaza.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "un-plaza")
    night = "--night" in argv
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    height = mx.z - mn.z
    width = max(mx.x - mn.x, mx.y - mn.y)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world(night=night)
    add_lights(height, night=night, span=max(width, height))

    if not night:
        fade_glow()

    if night:
        light_glow()
        aer = make_camera("cam_night")
        aer.data.lens = 78.0
        span = max(width, height)
        pitch = math.radians(31)
        az = math.radians(145)  # off the southeast, matching the day aerial
        r = span * 2.15
        aer.location = Vector(
            (
                center.x + r * math.cos(pitch) * math.sin(az),
                center.y + r * math.cos(pitch) * math.cos(az),
                center.z + r * math.sin(pitch),
            )
        )
        aim(aer, Vector((center.x, center.y, center.z * 0.9)))
        render_to(os.path.join(out, f"{prefix}-aerial-night.png"), aer, AER_RES)
        return

    # --- four elevations: one rig, identical everything but azimuth ---------
    span = max(width, height)
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

    # --- top view: THE primary review image for this asset ------------------
    # One red wedge, two dark-green bars, one pale granite band, one pale skate
    # pad, one pale grey pile. If any of those six merges into its neighbour,
    # the tonal separation is wrong (plan 2.9). It must read RED at 600 m.
    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.ortho_scale = width * 1.04
    top.location = Vector((center.x, center.y, mx.z + span))
    top.rotation_euler = (0, 0, 0)
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- beauty render from the app's high three-quarter aerial camera -----
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 78.0  # long lens, restrained perspective (style bible §18)
    pitch = math.radians(38)  # 30-50 deg downward; steeper than a building
                              # needs, because on this asset the plan is the
                              # subject and a shallow angle hides it
    # Off the SOUTH-EAST flank, over Market Street, which is how the plaza is
    # actually approached and the only angle from which the wedge, the
    # colonnade and the fountain are all visible at once. Looking down the
    # 80.94 deg axis instead collapses the colonnade into a single column.
    az = math.radians(128)
    r = span * 2.15
    aer.location = Vector(
        (
            center.x + r * math.cos(pitch) * math.sin(az),
            center.y + r * math.cos(pitch) * math.cos(az),
            center.z + r * math.sin(pitch),
        )
    )
    aim(aer, Vector((center.x, center.y, mn.z + 6.0)))
    render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)

    # --- the signature composition: low three-quarter looking WEST along the
    # Fulton axis from the Market end, the view the plaza was designed to
    # create. City Hall would fill the far end; it is not part of this asset.
    axis = make_camera("cam_axis")
    axis.data.type = "PERSP"
    axis.data.lens = 95.0
    apitch = math.radians(11)
    r2 = span * 1.05
    axis.location = Vector(
        (
            center.x + r2 * math.cos(apitch) * math.sin(math.radians(80.94)),
            center.y + r2 * math.cos(apitch) * math.cos(math.radians(80.94)),
            mn.z + r2 * math.sin(apitch),
        )
    )
    aim(axis, Vector((center.x, center.y, mn.z + 5.0)))
    render_to(os.path.join(out, f"{prefix}-axis.png"), axis, AER_RES)


if __name__ == "__main__":
    main()
