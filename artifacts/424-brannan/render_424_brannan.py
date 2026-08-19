"""Controlled review renders of the exported 424 Brannan GLB.

    blender -b --python render_424_brannan.py -- [--glb FILE] [--out DIR]
                                             [--prefix 424-brannan] [--night]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships.

Subject-specific choices:

* the TOP view is the PRIMARY review image, not the aerial. This asset is a
  ground graphic — a Z of pale slab with five rows of stalls on it — and the
  plan is where it is judged. The camera is ROLLED by 90 - 45.2 deg so the lot
  sits square in frame instead of running corner to corner;
* the four elevations are taken along the SITE's own axes and named for the
  frontage they face: `ritch` (the 68.4 m fence), `brannan` (the neck and the
  sign), `zoe` (the gate), `north` (the party boundary and the notch). A compass
  set would give four identical obliques of the same rhomboid;
* a GRAZING view is added, 6 deg above the plate looking north-west along the
  Ritch row. A draped plate that has gone wrong shows there and nowhere else;
* the aerial stands to the south-east, over Brannan, which is the approach the
  app's fly-to preset uses and the only angle from which the neck, the gate and
  the sign all read at once.

--night previews the app's dusk pass. The read to check for is THREE lit things
in a dark field — the sign, the booth window, three lamp heads — and a plate
that has gone completely dark.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

HEADING_U = 45.2

RES = (1800, 400)          # letterbox: ~80 m of lot, 8.6 m of model
AER_RES = (1700, 1050)
TOP_RES = (1180, 1560)     # portrait: the lot is 80 m by 48 m in its own frame
BG = (0.86, 0.80, 0.69, 1.0)

VIEWS = [
    ("ritch", HEADING_U),               # stands off Ritch Street (north-east)
    ("brannan", HEADING_U + 90.0),      # stands off Brannan (south-east)
    ("zoe", HEADING_U + 180.0),         # stands off Zoe (south-west)
    ("north", HEADING_U + 270.0),       # the party boundary and the notch
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

    bpy.ops.mesh.primitive_plane_add(size=span * 3, location=(0, 0, -1.30))
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
    """glTF writes emissiveFactor = 0 when the authored emission strength is 0,
    so a re-imported _Glow material carries a DEFAULT WHITE emission and every
    glow surface renders as a white slab. Drive emission from Base Color, which
    is also exactly what the app does — its night layer is an unlit overlay at
    the material's own baked colour (plans README, caught on chase-center)."""
    for mat, bsdf in glow_materials():
        if not bsdf:
            continue
        base = bsdf.inputs["Base Color"].default_value
        bsdf.inputs["Emission Color"].default_value = base
        bsdf.inputs["Emission Strength"].default_value = 2.4


def fade_glow():
    """Preview the app's DAY state. assets.js puts _Glow surfaces in a separate
    unlit layer at opacity 0.12 + 0.95*uNight, so by day the shells are ~12%
    alpha and the opaque surface behind them reads through. Emission is zeroed
    as well as alpha: the inherited version of this helper only dropped Alpha,
    which washes a hero shell to flat pale grey in the DAY render (46 South
    Park, Aug 2026)."""
    for mat, bsdf in glow_materials():
        if not bsdf:
            continue
        bsdf.inputs["Alpha"].default_value = 0.12
        bsdf.inputs["Emission Strength"].default_value = 0.0
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


def fit_ortho(cam, objs, res, margin=1.06):
    """Set ortho_scale and re-centre from the model's ACTUAL extent in camera
    space.

    Deriving the scale from the site's u/v extents by hand got two of the four
    elevations wrong (the Brannan view framed 22 m of a 47 m lot), because which
    site axis ends up horizontal depends on the track-quat aim() lands on.
    Projecting the bounding-box corners through the camera's own inverse matrix
    cannot get that wrong — as long as the depsgraph is flushed first, since a
    camera created this frame still carries an identity matrix_world until it is.
    """
    bpy.context.view_layer.update()
    inv = cam.matrix_world.inverted()
    xs, ys = [], []
    for o in objs:
        for c in o.bound_box:
            p = inv @ (o.matrix_world @ Vector(c))
            xs.append(p.x)
            ys.append(p.y)
    sx = max(xs) - min(xs)
    sy = max(ys) - min(ys)
    aspect = res[0] / res[1]
    cam.data.ortho_scale = max(sx, sy * aspect if aspect >= 1 else sy) * margin
    mid = Vector(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, 0.0))
    cam.location = cam.location + (cam.matrix_world.to_3x3() @ mid)
    bpy.context.view_layer.update()
    return cam


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

    glb = arg("--glb", os.path.join(here, "424-brannan.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "424-brannan")
    night = "--night" in argv
    os.makedirs(out, exist_ok=True)

    clear()
    objs, mn, mx = import_glb(glb)
    width = max(mx.x - mn.x, mx.y - mn.y)

    # Frame on the SITE's own bounding box. The lot lies at 45.2 deg, so its
    # world bbox centre sits 7.3 m from its own centre; aiming at the world one
    # pushed the Brannan neck out of every frame in the first rig.
    th = math.radians(HEADING_U)
    su0, su1, sv0, sv1 = 1e9, -1e9, 1e9, -1e9
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            u = w.x * math.sin(th) + w.y * math.cos(th)
            v = w.x * math.sin(th + math.pi / 2) + w.y * math.cos(th + math.pi / 2)
            su0, su1 = min(su0, u), max(su1, u)
            sv0, sv1 = min(sv0, v), max(sv1, v)
    uc, vc = (su0 + su1) / 2, (sv0 + sv1) / 2
    cx = uc * math.sin(th) + vc * math.sin(th + math.pi / 2)
    cy = uc * math.cos(th) + vc * math.cos(th + math.pi / 2)
    center = Vector((cx, cy, (mn.z + mx.z) / 2))
    site_u = su1 - su0            # ~48 m across the belly
    site_v = sv1 - sv0            # ~80 m from Zoe to Brannan
    site_m = max(site_u, site_v)

    def fit_distance(lens_mm, cover_m):
        return cover_m / (2.0 * math.tan(math.atan(18.0 / lens_mm)))

    setup_world(night=night)
    add_lights(width, night=night)

    if night:
        light_glow()
        aer = make_camera("cam_night")
        aer.data.lens = 62.0
        aer.location = orbit(center, 158.0, 30.0, fit_distance(62.0, site_m * 1.15), mn.z)
        aim(aer, Vector((center.x, center.y, mn.z + 1.5)))
        render_to(os.path.join(out, f"{prefix}-aerial-night.png"), aer, AER_RES)
        return

    fade_glow()

    # --- four elevations along the site's own axes -------------------------
    for name, az in VIEWS:
        cam = make_camera(f"cam_{name}")
        cam.data.type = "ORTHO"
        cam.location = orbit(center, az, 0.0, site_m * 2.4, center.z)
        aim(cam, Vector((center.x, center.y, center.z)))
        fit_ortho(cam, objs, RES, margin=1.06)
        render_to(os.path.join(out, f"{prefix}-{name}.png"), cam, RES)

    # --- top view: THE primary review image, rolled to sit square ----------
    # A 52-degree key throws long fence-post shadows straight across the stalls
    # and in a nadir view those read as extra striping. The plan is the subject
    # here, so the top view gets its own near-overhead key and a lifted ambient.
    for lamp in bpy.data.objects:
        if lamp.type == "LIGHT" and lamp.name == "key":
            lamp.rotation_euler = (math.radians(14), 0, math.radians(-38))
        if lamp.type == "LIGHT" and lamp.name == "fill":
            lamp.data.energy = 1.25
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.62

    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.location = Vector((center.x, center.y, mx.z + width))
    top.rotation_euler = (0, 0, math.radians(90.0 - HEADING_U))
    bpy.context.view_layer.update()
    fit_ortho(top, objs, TOP_RES, margin=1.05)
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    for lamp in bpy.data.objects:
        if lamp.type == "LIGHT" and lamp.name == "key":
            lamp.rotation_euler = (math.radians(52), 0, math.radians(-38))
        if lamp.type == "LIGHT" and lamp.name == "fill":
            lamp.data.energy = 0.55
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.30

    # --- the app's high three-quarter aerial, from over Brannan ------------
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 62.0
    aer.location = orbit(center, 158.0, 34.0, fit_distance(62.0, site_m * 1.15), mn.z)
    aim(aer, Vector((center.x, center.y, mn.z + 1.5)))
    render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)

    # --- grazing: 6 degrees above the plate, looking north-west along the
    # Ritch row from the Brannan gate. The drape check, and the only view in
    # which the fence, the sign and the stall rows all stack up.
    graze = make_camera("cam_graze")
    graze.data.type = "PERSP"
    graze.data.lens = 85.0
    graze.location = orbit(center, HEADING_U + 100.0, 6.0,
                           fit_distance(85.0, site_m * 0.72), mn.z + 1.0)
    aim(graze, Vector((center.x, center.y, mn.z + 2.2)))
    render_to(os.path.join(out, f"{prefix}-grazing.png"), graze, AER_RES)


if __name__ == "__main__":
    main()
