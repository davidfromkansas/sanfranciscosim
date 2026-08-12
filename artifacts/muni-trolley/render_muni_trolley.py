"""Review renders of the exported Muni trolley coach GLB.

    blender -b --python render_muni_trolley.py -- [--glb F] [--out DIR] [--samples N]

Renders the EXACT exported geometry — the GLB is re-imported into an empty
scene, so what is judged is what ships.

Outputs into renders/:
    muni-trolley-40-front.png  -rear.png  -left.png  -right.png
                              four elevations, identical ortho scale, framing,
                              light rig and exposure
    muni-trolley-40-top.png    orthographic plan — THE view for this asset: it
                              is what proves the two poles are two poles, at a
                              spacing a two-wire overhead would actually use
    muni-trolley-40-aerial.png 42 deg down, 100 mm lens (style bible §18)
    muni-trolley-40-night.png  the same aerial with the glow set ignited

The two mandatory extra renders — the 1.6x in-city scale test and the 120 m
side-by-side against the hybrid bus — are in ``render_in_city.py``, because they
need real baked city geometry and both vehicles in one frame.

The rig is deliberately identical to ``render_muni_bus.py`` (same world, same
three suns, same exposure, same Standard view transform) so the two assets'
elevations can be compared without lighting being a variable. Only the frame
aspect differs: this vehicle is 5.79 m tall instead of 3.42 m, so a 1600x620
elevation would crop the poles off the asset whose entire job is the poles.

NIGHT PREVIEW GOTCHA: a glTF `emissiveFactor` of (0,0,0) makes Blender's
importer default Emission Color to white, so raising Emission Strength alone
lights every glow surface white. `ignite()` copies Base Color into Emission
Color first. The shipped asset keeps emission at 0.0.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

SLUG = "muni-trolley-40"


def argval(argv, flag, default=None):
    return argv[argv.index(flag) + 1] if flag in argv else default


def import_glb(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    objs = [o for o in set(bpy.data.objects) - before if o.type == "MESH"]
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    return objs, mn, mx


def world(top=(0.62, 0.70, 0.80), strength=1.0):
    w = bpy.data.worlds.new("W")
    bpy.context.scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (*top, 1.0)
    bg.inputs[1].default_value = strength


def sun(name, rot, energy, angle=0.14, colour=(1.0, 0.97, 0.92)):
    d = bpy.data.lights.new(name, type="SUN")
    d.energy = energy
    d.angle = angle
    d.color = colour
    o = bpy.data.objects.new(name, d)
    o.rotation_euler = rot
    bpy.context.collection.objects.link(o)
    return o


def ground(z=0.0, size=200.0, colour=(0.74, 0.72, 0.66)):
    """Renders only — the contact shadow that makes a miniature sit on a table
    (style bible §19). Never exported."""
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, z))
    o = bpy.context.object
    m = bpy.data.materials.new("Ground")
    m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*colour, 1)
    m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
    o.data.materials.append(m)
    return o


def camera(name, loc, look, lens=None, ortho_scale=None):
    cam = bpy.data.cameras.new(name)
    if ortho_scale is not None:
        cam.type = "ORTHO"
        cam.ortho_scale = ortho_scale
    else:
        cam.lens = lens or 85.0
    obj = bpy.data.objects.new(name, cam)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    direction = Vector(look) - Vector(loc)
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    return obj


def render(cam, path, res=(1600, 1000), samples=64):
    sc = bpy.context.scene
    sc.camera = cam
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "Standard"  # flat toy colour, no roll-off
    sc.view_settings.look = "None"
    sc.render.filepath = path
    sc.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(write_still=True)
    print(f"[render] {path}")


def ignite(strength=7.0):
    """Night preview only — see the module docstring."""
    for m in bpy.data.materials:
        if not m.name.endswith("_Glow") or not m.use_nodes:
            continue
        b = m.node_tree.nodes.get("Principled BSDF")
        if not b:
            continue
        b.inputs["Emission Color"].default_value = b.inputs["Base Color"].default_value
        b.inputs["Emission Strength"].default_value = strength


def day_rig():
    world((0.60, 0.69, 0.80), 0.95)
    sun("key", (math.radians(52), 0.0, math.radians(38)), 2.5)
    sun("fill", (math.radians(64), 0.0, math.radians(214)), 1.1,
        angle=0.6, colour=(0.86, 0.90, 1.0))
    sun("rim", (math.radians(76), 0.0, math.radians(128)), 0.55, angle=0.8)


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    glb = argval(argv, "--glb", os.path.join(here, f"{SLUG}.glb"))
    out = argval(argv, "--out", os.path.join(here, "renders"))
    samples = int(argval(argv, "--samples", "64"))
    os.makedirs(out, exist_ok=True)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    objs, mn, mx = import_glb(glb)
    dims = [mx[i] - mn[i] for i in range(3)]
    cx, cy = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2
    cz = (mn[2] + mx[2]) / 2
    print(f"[render] imported {len(objs)} objects, dims={[round(d, 3) for d in dims]}")

    day_rig()
    ground()

    # --- four elevations: one ortho scale, one distance, one rig, one exposure.
    ORTHO = max(dims) * 1.14
    D = 40.0
    ELEV_RES = (1600, 800)  # 2.0:1 — 7.1 m of vertical coverage clears the poles
    elevations = {
        # The coach noses toward +Y after the round trip through glTF, so the
        # front elevation looks down -Y at it. Left/right are named from the
        # driver's seat: forward +Y, up +Z => right is +X.
        "front": (cx, cy + D, cz),
        "rear": (cx, cy - D, cz),
        "left": (cx - D, cy, cz),
        "right": (cx + D, cy, cz),
    }
    for name, loc in elevations.items():
        cam = camera(f"cam_{name}", loc, (cx, cy, cz), ortho_scale=ORTHO)
        render(cam, os.path.join(out, f"{SLUG}-{name}.png"), ELEV_RES, samples)

    # --- plan view. The most important frame in this set: the two poles, their
    # 0.60 m spacing and their rearward trail are all only unambiguous from here.
    cam = camera("cam_top", (cx, cy, mx[2] + D), (cx, cy, cz), ortho_scale=ORTHO)
    cam.rotation_euler = (0.0, 0.0, math.radians(90.0))
    render(cam, os.path.join(out, f"{SLUG}-top.png"), ELEV_RES, samples)

    # --- the aerial the style bible actually judges from: 42 deg down, long lens.
    pitch = math.radians(42.0)
    dist = 48.0
    # A front three-quarter well round toward the side. A rear three-quarter was
    # tried first, on the reasoning that the poles live at the back — but the
    # poles trail aft, so a camera placed aft looks straight down them and they
    # foreshorten into stubs. Standing off the flank shows their full diagonal
    # AND keeps the destination sign in frame, which is what the night pass needs.
    yaw = math.radians(118.0)
    loc = (cx + dist * math.cos(pitch) * math.sin(yaw),
           cy - dist * math.cos(pitch) * math.cos(yaw),
           cz + dist * math.sin(pitch))
    cam_a = camera("cam_aerial", loc, (cx, cy, cz), lens=100.0)
    render(cam_a, os.path.join(out, f"{SLUG}-aerial.png"), (1600, 1000), samples)

    # --- night gets its own yaw, swung further toward the nose. The glow set's
    # most important surface is the destination sign and it faces dead ahead, so
    # the frame that has to prove the glow works cannot be the frame optimised
    # for the poles. The poles still read from here; the sign would not read
    # from there.
    yaw_n = math.radians(143.0)
    loc_n = (cx + dist * math.cos(pitch) * math.sin(yaw_n),
             cy - dist * math.cos(pitch) * math.cos(yaw_n),
             cz + dist * math.sin(pitch))
    cam_n = camera("cam_night", loc_n, (cx, cy, cz), lens=100.0)

    # --- night: the glow set ignited, moonlit key floor.
    for lamp in [o for o in bpy.data.objects if o.type == "LIGHT"]:
        bpy.data.objects.remove(lamp, do_unlink=True)
    world((0.055, 0.075, 0.135), 1.0)
    sun("moon", (math.radians(58), 0.0, math.radians(212)), 0.42,
        angle=0.5, colour=(0.72, 0.80, 1.0))
    ignite()
    render(cam_n, os.path.join(out, f"{SLUG}-night.png"), (1600, 1000), samples)


if __name__ == "__main__":
    main()
