"""Controlled review renders of the exported Pier 1 GLB.

    blender -b --python render_pier_9.py -- [--glb FILE] [--out DIR]
                                            [--prefix pier-9] [--night]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene, so
every image depicts exactly the geometry that ships. The four elevations share one
camera rig (same orthographic scale, framing, lighting, exposure and projection)
and differ only in azimuth.

The pier lies at 53.77 deg to the world axes, so the cameras are aligned to the
PIER's axes, not to true compass directions - otherwise every "elevation" would be
an oblique three-quarter and a reviewer could not compare opposite faces. Each view
keeps its nearest compass filename:

    -west.png   the EMBARCADERO facade, faces 233.8 deg - the frontispiece
    -east.png   the north-east end wall, faces 53.8 deg, and the open deck
    -north.png  the north-west shed flank, faces 323.8 deg (the Pier 15 slip)
    -south.png  the south-east shed flank, faces 143.8 deg (the Pier 7 side)

Plus -facade.png, a square-on long-lens look at the frontispiece, which is the
one thing none of the 234 m-wide elevations shows at a readable size.

--night previews the app's dusk pass: _Glow materials get their emission turned
up under a dark moonlit world, producing <prefix>-aerial-night.png.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (3200, 440)          # the pier is 234 m long; a square frame wastes it
AER_RES = (1800, 1150)
TOP_RES = (2600, 900)
FAC_RES = (1500, 950)
BG = (0.86, 0.80, 0.69, 1.0)

AXIS = 54.59               # long axis, to the north-east
FRONT_AZ = (AXIS + 180.0) % 360.0     # the Embarcadero facade faces 233.77

VIEWS = [
    ("west", FRONT_AZ),        # Embarcadero facade
    ("east", AXIS),            # north-east end
    ("north", AXIS + 270.0),   # north-west flank
    ("south", AXIS + 90.0),    # south-east flank
]

# Over the Embarcadero, off the facade's outboard shoulder: the only azimuth that
# reads the frontispiece, the south-east flank running away, the taper and the
# whole roof at once - which is the view the app's camera preset flies to.
AERIAL_AZ = FRONT_AZ + 30.0
AERIAL_PITCH = 31.0
AERIAL_R = 1.45
# The frontispiece is 24 m of a 234 m asset, so both aerials aim a third of the
# way up the pier rather than at the bbox centre; aiming at the centre pushed the
# bulkhead into the corner of the frame and cropped it.
AIM_ALONG_FRAC = 0.34
# The Bay side: the outer end, the open deck and the solar field looking back at
# the city. The half of the asset the first aerial cannot show.
AERIAL2_AZ = AXIS - 28.0
AERIAL2_PITCH = 28.0


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
    # EEVEE Next: this asset is 234 m long and every review image is either
    # 3200 px wide or a 1800 px aerial. Cycles on CPU took minutes per frame for
    # flat-colour geometry with three sun lamps; EEVEE renders the same read in
    # seconds. Soft shadows and AO are on, which is all the miniature look needs.
    engine = os.environ.get("SF_ENGINE", "BLENDER_EEVEE")
    scene.render.engine = engine
    if engine == "CYCLES":
        scene.cycles.device = "CPU"
        scene.cycles.samples = 48
        scene.cycles.use_denoising = True
    else:
        scene.eevee.taa_render_samples = 64
        scene.eevee.use_shadows = True
        scene.eevee.use_raytracing = True
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


def add_lights(height, night=False):
    if night:
        moon = bpy.data.lights.new("moon", "SUN")
        moon.energy = 0.12
        moon.color = (0.65, 0.74, 1.0)
        moon.angle = math.radians(10)
        ob = bpy.data.objects.new("moon", moon)
        bpy.context.collection.objects.link(ob)
        ob.rotation_euler = (math.radians(55), 0, math.radians(200))
    else:
        key = bpy.data.lights.new("key", "SUN")
        key.energy = 2.1
        key.angle = math.radians(6)
        ob = bpy.data.objects.new("key", key)
        bpy.context.collection.objects.link(ob)
        # Keyed from the south-west so the frontispiece catches the light and the
        # monitor spine and both solar fields throw shadows across the roof.
        ob.rotation_euler = (math.radians(48), 0, math.radians(215))

        fill = bpy.data.lights.new("fill", "SUN")
        fill.energy = 0.55
        fill.angle = math.radians(35)
        ob2 = bpy.data.objects.new("fill", fill)
        bpy.context.collection.objects.link(ob2)
        ob2.rotation_euler = (math.radians(65), 0, math.radians(40))

        rim = bpy.data.lights.new("rim", "SUN")
        rim.energy = 0.45
        rim.color = (1.0, 0.93, 0.82)
        ob3 = bpy.data.objects.new("rim", rim)
        bpy.context.collection.objects.link(ob3)
        ob3.rotation_euler = (math.radians(78), 0, math.radians(320))

    # The Bay stands in for the studio floor: the pier's whole point is that it
    # is over water, and a tabletop plane at the model's base would hide the
    # piles. The plane sits at the model's local water line (-0.2 m).
    bpy.ops.mesh.primitive_plane_add(size=1400.0, location=(0, 0, -0.2))
    plane = bpy.context.object
    plane.name = "studio_water"
    mat = bpy.data.materials.new("Studio_Water")
    mat.use_nodes = True
    shade = (0.02, 0.04, 0.07, 1.0) if night else (0.13, 0.28, 0.30, 1.0)
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = shade
    mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.42
    plane.data.materials.append(mat)
    return plane


def principled(mat):
    """The glTF importer does not always name the node "Principled BSDF"; look it
    up by type. Looking it up by name returned None here, fade_glow() silently
    did nothing, and every glow surface rendered opaque tan in the day pass."""
    for n in mat.node_tree.nodes:
        if n.type == "BSDF_PRINCIPLED":
            return n
    return None


def glow_materials():
    for mat in bpy.data.materials:
        if mat.use_nodes and mat.name.split(".")[0].endswith("_Glow"):
            yield mat, principled(mat)


def light_glow():
    """Preview the app's night pass. Emission is driven from Base Color at a
    restrained strength: glTF writes emissiveFactor = 0 for an authored strength
    of 0, so a re-imported _Glow material carries a DEFAULT WHITE emission and
    every glow surface renders as a white slab unless this is set explicitly."""
    for mat, bsdf in glow_materials():
        if not bsdf:
            continue
        base = bsdf.inputs["Base Color"].default_value
        bsdf.inputs["Emission Color"].default_value = base
        # 1.8, not 3.0: the app's night layer draws _Glow at its own base colour
        # with no multiplier, so a strong push here would flatter a glow colour
        # that is wrong. At 3.0 the cool clerestory (cbd8e0) blew to flat white
        # and the render stopped being evidence.
        bsdf.inputs["Emission Strength"].default_value = 1.8


# Toy_glass, linear - what every glow quad in this asset stands proud of.
GLASS_LIN = (0.0243, 0.0722, 0.1746)


def fade_glow():
    """Preview the app's DAY state. assets.js draws _Glow surfaces in a separate
    unlit layer at opacity 0.12 + 0.95*uNight, so by day a glow surface is 12%
    of its own colour over whatever it stands in front of.

    That is previewed here by BAKING the blend into the base colour and keeping
    the surface opaque, rather than by setting a 12% alpha: EEVEE's blended
    render method needs more setup than one property, and a glow quad that
    renders opaque turns every lit window into a flat tan panel - which is a
    render bug that looks exactly like an art problem."""
    for mat, bsdf in glow_materials():
        if not bsdf:
            continue
        c = bsdf.inputs["Base Color"].default_value
        mix = tuple(0.12 * c[i] + 0.88 * GLASS_LIN[i] for i in range(3))
        bsdf.inputs["Base Color"].default_value = mix + (1.0,)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = 0.0


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


def orbit(center, az_deg, pitch_deg, radius):
    a, p = math.radians(az_deg), math.radians(pitch_deg)
    return Vector((center.x + radius * math.cos(p) * math.sin(a),
                   center.y + radius * math.cos(p) * math.cos(a),
                   center.z + radius * math.sin(p)))


def aim_point(center, mn, height):
    """A point AIM_ALONG_FRAC of the pier's length back toward the bulkhead."""
    r = math.radians(FRONT_AZ)
    d = 254.0 * AIM_ALONG_FRAC
    return Vector((center.x + d * math.sin(r), center.y + d * math.cos(r),
                   mn.z + height * 0.5))


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

    glb = arg("--glb", os.path.join(here, "pier-9.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "pier-9")
    night = "--night" in argv
    only = arg("--only", None)
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    height = mx.z - mn.z
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world(night=night)
    add_lights(height, night=night)
    if not night:
        if "--noglow" in argv:
            for o in list(bpy.data.objects):
                if o.type == "MESH" and any(
                        m and m.name.split(".")[0].endswith("_Glow")
                        for m in o.data.materials):
                    bpy.data.objects.remove(o, do_unlink=True)
        else:
            fade_glow()

    span = 258.0          # the pier's own length, not the 45-degree bbox
    if night:
        light_glow()
        aer = make_camera("cam_night")
        aer.data.lens = 62.0
        tgt = aim_point(center, mn, height)
        aer.location = orbit(tgt, AERIAL_AZ, AERIAL_PITCH, span * AERIAL_R)
        aim(aer, tgt)
        render_to(os.path.join(out, f"{prefix}-aerial-night.png"), aer, AER_RES)
        return

    if only in (None, "elev"):
        ortho_scale = span * 1.06
        dist = span * 3.0
        for name, az in VIEWS:
            cam = make_camera(f"cam_{name}")
            cam.data.type = "ORTHO"
            cam.data.ortho_scale = ortho_scale
            a = math.radians(az)
            cam.location = Vector((center.x + dist * math.sin(a),
                                   center.y + dist * math.cos(a),
                                   mn.z + height * 0.5))
            aim(cam, Vector((center.x, center.y, mn.z + height * 0.5)))
            render_to(os.path.join(out, f"{prefix}-{name}.png"), cam, RES)

    if only in (None, "top"):
        top = make_camera("cam_top")
        top.data.type = "ORTHO"
        top.data.ortho_scale = span * 1.10
        top.location = Vector((center.x, center.y, mx.z + span))
        # Roll so image-right is the pier's along direction. For a top-down
        # camera with rotation (0, 0, rz), image-right maps to world
        # (cos rz, sin rz); the along direction is (sin AXIS, cos AXIS), so
        # rz = 90 - AXIS. Getting this backwards renders the pier diagonally
        # across a 2600x900 frame and crops both ends.
        top.rotation_euler = (0, 0, math.radians(90.0 - AXIS))
        render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    if only in (None, "aerial"):
        aer = make_camera("cam_aerial")
        aer.data.type = "PERSP"
        aer.data.lens = 62.0
        tgt = aim_point(center, mn, height)
        aer.location = orbit(tgt, AERIAL_AZ, AERIAL_PITCH, span * AERIAL_R)
        aim(aer, tgt)
        render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)

        aer2 = make_camera("cam_aerial_ne")
        aer2.data.type = "PERSP"
        aer2.data.lens = 62.0
        tgt2 = Vector((center.x, center.y, mn.z + height * 0.5))
        aer2.location = orbit(tgt2, AERIAL2_AZ, AERIAL2_PITCH, span * 1.45)
        aim(aer2, tgt2)
        render_to(os.path.join(out, f"{prefix}-aerial-ne.png"), aer2, AER_RES)

    if only in (None, "facade"):
        fac = make_camera("cam_facade")
        fac.data.type = "PERSP"
        fac.data.lens = 135.0
        # The frontispiece is 24 m of a 234 m asset: framed on the bulkhead, not
        # on the model centre, or it is 40 pixels wide.
        r = math.radians(FRONT_AZ)
        bulk = Vector((center.x + 100.0 * math.sin(r), center.y + 100.0 * math.cos(r),
                       mn.z + height * 0.45))
        fac.location = Vector((bulk.x + 165.0 * math.sin(r) * math.cos(math.radians(11)),
                               bulk.y + 165.0 * math.cos(r) * math.cos(math.radians(11)),
                               bulk.z + 165.0 * math.sin(math.radians(11))))
        aim(fac, bulk)
        render_to(os.path.join(out, f"{prefix}-facade.png"), fac, FAC_RES)


if __name__ == "__main__":
    main()
