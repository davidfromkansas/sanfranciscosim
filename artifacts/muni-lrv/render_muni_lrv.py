"""Review renders of the exported Muni Metro LRV GLB.

    blender -b --python render_muni_lrv.py -- [--glb F] [--out DIR] [--samples N]

Renders the EXACT exported geometry — the GLB is re-imported into an empty
scene, so what is judged is what ships, not the authoring scene.

Outputs into renders/:
    muni-lrv-front.png  -rear.png  -left.png  -right.png    four elevations at
                                                            one ortho scale,
                                                            framing, light rig
                                                            and exposure
    muni-lrv-top.png       orthographic plan — the roof, the pantograph and the
                           articulation break
    muni-lrv-aerial.png    42 deg down, 100 mm lens (style bible §18)
    muni-lrv-night.png     the same aerial with the glow set ignited

The vehicle is double-ended (REFERENCE.md §3), so `-front` and `-rear` are two
views of the same geometry differing only in the destination sign and the fleet
number's A/B suffix. Both are rendered because both are cab elevations and the
rear is not a freebie.

No GPU here, so this is Cycles on CPU.

NIGHT PREVIEW GOTCHA: a glTF `emissiveFactor` of (0,0,0) makes Blender's
importer default Emission Color to white, so raising Emission Strength alone
lights every glow surface white. `ignite()` copies Base Color into Emission
Color first. The shipped asset keeps emission at 0.0 — the app's own night
layer is what drives the real thing.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

SLUG = "muni-lrv"


def argval(argv, flag, default=None):
    return argv[argv.index(flag) + 1] if flag in argv else default


def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


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


def ground(z=0.0, size=300.0, colour=(0.74, 0.72, 0.66)):
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
    cam.clip_start = 0.1
    cam.clip_end = 3000.0
    obj = bpy.data.objects.new(name, cam)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    direction = Vector(look) - Vector(loc)
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    return obj


def render(cam, path, res=(1800, 900), samples=64):
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
    # One broad key plus two fills, fixed in WORLD space so all four elevations
    # share the same lighting rather than each being relit to flatter itself.
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

    clear()
    objs, mn, mx = import_glb(glb)
    dims = [mx[i] - mn[i] for i in range(3)]
    cx, cy = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2
    cz = (mn[2] + mx[2]) / 2
    print(f"[render] imported {len(objs)} objects, dims={[round(d, 3) for d in dims]}")

    day_rig()
    ground()

    # --- four elevations: one ortho scale, one distance, one rig, one exposure.
    ORTHO = max(dims) * 1.10
    D = 60.0
    elevations = {
        # The LRV noses toward +Y after the round trip through glTF, so the
        # front elevation looks down -Y at it. Left/right are named from the
        # leading cab: forward +Y, up +Z => right is +X.
        "front": (cx, cy + D, cz),
        "rear": (cx, cy - D, cz),
        "left": (cx - D, cy, cz),
        "right": (cx + D, cy, cz),
    }
    for name, loc in elevations.items():
        # The two cab elevations are nearly square; the flanks are 23 m of a
        # 4.7 m tall object. Framing each to its own aspect at ONE ortho scale
        # keeps the four comparable without wasting most of the frame on sky.
        res = (1800, 1700) if name in ("front", "rear") else (2200, 620)
        scale = ORTHO * (0.22 if name in ("front", "rear") else 1.0)
        cam = camera(f"cam_{name}", loc, (cx, cy, cz), ortho_scale=scale)
        render(cam, os.path.join(out, f"{SLUG}-{name}.png"), res, samples)

    # --- plan view: the roof is a primary surface at the app's camera angle.
    cam = camera("cam_top", (cx, cy, mx[2] + D), (cx, cy, cz), ortho_scale=ORTHO)
    # Yaw the plan view so the 23 m length lies across the frame's long axis.
    cam.rotation_euler = (0.0, 0.0, math.radians(90.0))
    render(cam, os.path.join(out, f"{SLUG}-top.png"), (2200, 620), samples)

    # --- the aerial the style bible actually judges from: 42 deg down, long lens.
    pitch = math.radians(42.0)
    dist = 78.0
    # Front three-quarter: the cab's red horseshoe is the strongest recognition
    # cue (REFERENCE.md §4.1) and the destination sign is the "alive" cue, so
    # the aerial looks at the nose rather than the tail.
    yaw = math.radians(148.0)
    loc = (cx + dist * math.cos(pitch) * math.sin(yaw),
           cy - dist * math.cos(pitch) * math.cos(yaw),
           cz + dist * math.sin(pitch))
    cam_a = camera("cam_aerial", loc, (cx, cy, cz + 0.3), lens=100.0)
    render(cam_a, os.path.join(out, f"{SLUG}-aerial.png"), (1800, 1100), samples)

    # --- night: same camera, the glow set ignited, moonlit key floor.
    for lamp in [o for o in bpy.data.objects if o.type == "LIGHT"]:
        bpy.data.objects.remove(lamp, do_unlink=True)
    world((0.055, 0.075, 0.135), 1.0)
    sun("moon", (math.radians(58), 0.0, math.radians(212)), 0.42,
        angle=0.5, colour=(0.72, 0.80, 1.0))
    ignite()
    render(cam_a, os.path.join(out, f"{SLUG}-night.png"), (1800, 1100), samples)


if __name__ == "__main__":
    main()
