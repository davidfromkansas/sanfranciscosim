"""Controlled review renders of the exported 8 Mission Street GLB.

    blender -b --python render_8_mission.py -- [--glb FILE] [--out DIR]
                                            [--prefix 8-mission] [--night]

Always renders the EXPORTED asset: the GLB is re-imported into an empty scene,
so every image depicts exactly the geometry that ships. The four elevations
share one camera rig (same orthographic scale, framing, lighting, exposure and
projection) and differ only in azimuth.

The block sits at ~45 deg to the world axes, so the cameras are aligned to the
BUILDING's axes, not to true compass directions - otherwise every "elevation"
would be an oblique three-quarter and a reviewer could not compare opposite
faces. Each view keeps the nearest compass filename:

    -south.png  MISSION STREET, faces 135.37 deg - the hero elevation: the
                arcaded ground floor, the entry canopy, the plaster attic, the
                turret at the left edge and the concave notch at the right
    -east.png   THE EMBARCADERO, faces 45.37 deg - the second hero: glazed
                bays on brick piers, and the A/B step
    -west.png   STEUART STREET, faces 225.37 deg - the long elevation, and the
                only one that shows all THREE plateaus in a row
    -north.png  DON CHEE WAY, faces 315.37 deg - the plaza end, deliberately
                blank, with the notch returns beside it

Plus -steps.png (the massing check) and -top.png (the three parapet rings).

Engine: BLENDER_EEVEE. David's Mac runs many landmark sessions at once and CPU
Cycles makes no progress above load ~150 (see the render-contention note in
REPORT.md); EEVEE renders the same flat Toy_* materials, shadows and the glow
layer in seconds. Nothing this pass judges - silhouette, massing, step,
material band, which surfaces glow - needs path tracing.

--night previews the app's dusk pass: _Glow materials get their emission turned
up under a dark moonlit world, producing <prefix>-aerial-night.png.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

RES = (1400, 1000)
AER_RES = (1600, 1200)
TOP_RES = (1200, 1500)
STEP_RES = (1600, 900)
BG = (0.86, 0.80, 0.69, 1.0)

MISSION_AZ = 135.37
EMBARC_AZ = 45.37
STEUART_AZ = 225.37
DONCHEE_AZ = 315.37

VIEWS = [
    ("south", MISSION_AZ),
    ("east", EMBARC_AZ),
    ("west", STEUART_AZ),
    ("north", DONCHEE_AZ),
]

# Due EAST, on the bisector of the two hero elevations (135.37 and 45.37), so
# the Mission front, the Embarcadero front and the turret between them are all
# in one frame. This is the azimuth the app's own preset uses
# (landmarks.mjs yaw 90 -> camera bearing 90).
AERIAL_AZ = 90.37
AERIAL_PITCH = 32.0
AERIAL_R = 2.55


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
    # BLENDER_EEVEE, not BLENDER_EEVEE_NEXT - that is the 5.2 enum name.
    scene.render.engine = "BLENDER_EEVEE"
    scene.eevee.taa_render_samples = 64
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "Standard"   # AgX eats the palette
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
        moon.energy = 0.14
        moon.color = (0.65, 0.74, 1.0)
        moon.angle = math.radians(10)
        ob = bpy.data.objects.new("moon", moon)
        bpy.context.collection.objects.link(ob)
        ob.rotation_euler = (math.radians(55), 0, math.radians(200))
    else:
        key = bpy.data.lights.new("key", "SUN")
        key.energy = 2.4
        key.angle = math.radians(6)
        ob = bpy.data.objects.new("key", key)
        bpy.context.collection.objects.link(ob)
        # Keyed from the south-east so the Mission front is lit and the three
        # parapets and the turret all throw shadows across the terraces.
        ob.rotation_euler = (math.radians(48), 0, math.radians(120))

        # The four elevations share one rig, so the two elevations facing away
        # from the key are lit only by this. 0.60 left the Don Chee end an
        # unreadable flat brick slab; 1.00 keeps the key's shadow story and
        # still shows the openings on the shaded faces.
        fill = bpy.data.lights.new("fill", "SUN")
        fill.energy = 1.00
        fill.angle = math.radians(35)
        ob2 = bpy.data.objects.new("fill", fill)
        bpy.context.collection.objects.link(ob2)
        ob2.rotation_euler = (math.radians(65), 0, math.radians(300))

        rim = bpy.data.lights.new("rim", "SUN")
        rim.energy = 0.45
        rim.color = (1.0, 0.93, 0.82)
        ob3 = bpy.data.objects.new("rim", rim)
        bpy.context.collection.objects.link(ob3)
        ob3.rotation_euler = (math.radians(78), 0, math.radians(20))

    bpy.ops.mesh.primitive_plane_add(size=height * 12, location=(0, 0, -0.02))
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
    """Preview the app's night pass. glTF writes emissiveFactor = 0 when the
    authored strength is 0, so a re-imported _Glow material carries a DEFAULT
    WHITE emission - copy the material's own Base Color across before raising
    the strength, or every glow surface renders as a white slab (the
    chase-center failure)."""
    for mat, bsdf in glow_materials():
        if not bsdf:
            continue
        base = bsdf.inputs["Base Color"].default_value
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = base
        bsdf.inputs["Emission Strength"].default_value = 3.2


def fade_glow():
    """Preview the app's DAY state: _Glow surfaces live in a separate unlit
    layer at opacity 0.12 + 0.95*uNight, so by day they are ~12% alpha."""
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


def orbit(center, az_deg, pitch_deg, radius):
    a, p = math.radians(az_deg), math.radians(pitch_deg)
    return Vector((center.x + radius * math.cos(p) * math.sin(a),
                   center.y + radius * math.cos(p) * math.cos(a),
                   center.z + radius * math.sin(p)))


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

    glb = arg("--glb", os.path.join(here, "8-mission.glb"))
    out = arg("--out", here)
    prefix = arg("--prefix", "8-mission")
    night = "--night" in argv
    os.makedirs(out, exist_ok=True)

    clear()
    _, mn, mx = import_glb(glb)
    height = mx.z - mn.z
    width = max(mx.x - mn.x, mx.y - mn.y)
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))
    setup_world(night=night)
    add_lights(height, night=night)

    if not night:
        fade_glow()

    span = max(width, height)

    if night:
        light_glow()
        aer = make_camera("cam_night")
        aer.data.lens = 78.0
        aer.location = orbit(center, AERIAL_AZ, AERIAL_PITCH, span * AERIAL_R)
        aim(aer, Vector((center.x, center.y, mn.z + height * 0.55)))
        render_to(os.path.join(out, f"{prefix}-aerial-night.png"), aer, AER_RES)
        return

    # --- four elevations: one rig, identical everything but azimuth --------
    ortho_scale = span * 1.05
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

    # --- top view: the three parapet rings, the terraces, the turret and the
    # notch. Rolled to the building's own axis so the block sits square in
    # frame with Mission Street at the bottom.
    top = make_camera("cam_top")
    top.data.type = "ORTHO"
    top.data.sensor_fit = "VERTICAL"     # the roll puts the 64 m axis VERTICAL
    # Frame on the BUILDING's own axes, not on the world bounding box. The L is
    # not centred inside its world bbox (the notch takes a corner out), so a
    # camera parked at the bbox centre and rolled 45 deg crops the plaza end.
    rz = math.radians(MISSION_AZ - 90.0)
    up = Vector((-math.sin(rz), math.cos(rz), 0.0))
    rt = Vector((math.cos(rz), math.sin(rz), 0.0))
    pts = [o.matrix_world @ Vector(c)
           for o in bpy.data.objects if o.type == "MESH" and o.name != "studio_floor"
           for c in o.bound_box]
    us = [p.x * up.x + p.y * up.y for p in pts]
    rs = [p.x * rt.x + p.y * rt.y for p in pts]
    cu, cr = (min(us) + max(us)) / 2, (min(rs) + max(rs)) / 2
    top.data.ortho_scale = (max(us) - min(us)) * 1.06
    top.location = Vector((up.x * cu + rt.x * cr, up.y * cu + rt.y * cr,
                           mx.z + span))
    # For a top-down camera image-up maps to world (-sin rz, cos rz); rolling to
    # MISSION_AZ - 90 puts the Mission end at the BOTTOM of the frame, i.e. the
    # tall end nearest the reader, terraces receding. sensor_fit must be
    # VERTICAL: the roll stands the building's 64 m axis up the frame, and the
    # default AUTO fit sizes to the 1500 px width instead and crops it.
    top.rotation_euler = (0, 0, math.radians(MISSION_AZ - 90.0))
    render_to(os.path.join(out, f"{prefix}-top.png"), top, TOP_RES)

    # --- the massing check. Orthographic from the SOUTH-WEST with a slight
    # downward tilt: the Steuart elevation is the only one that contains all
    # three plateaus, so this is where the three parapet lines either read as
    # three lines or the massing has collapsed. (The plan asked for a
    # north-east view; the north-east elevation only carries two of the three
    # plateaus, so this is the honest frame - see REPORT.md.)
    st = make_camera("cam_steps")
    st.data.type = "ORTHO"
    st.data.ortho_scale = span * 1.02
    st.location = orbit(center, STEUART_AZ, 16.0, span * 3.0)
    aim(st, Vector((center.x, center.y, mn.z + height * 0.42)))
    render_to(os.path.join(out, f"{prefix}-steps.png"), st, STEP_RES)

    # --- beauty render from the app's high three-quarter aerial camera -----
    aer = make_camera("cam_aerial")
    aer.data.type = "PERSP"
    aer.data.lens = 78.0
    aer.location = orbit(center, AERIAL_AZ, AERIAL_PITCH, span * AERIAL_R)
    aim(aer, Vector((center.x, center.y, mn.z + height * 0.55)))
    render_to(os.path.join(out, f"{prefix}-aerial.png"), aer, AER_RES)


if __name__ == "__main__":
    main()
