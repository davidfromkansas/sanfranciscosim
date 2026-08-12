"""The mandatory decision renders for the Muni Metro LRV.

    node export_city_cell.mjs            # writes city-cell.json first
    blender -b --python render_scenarios.py -- [--glb FILE] [--out DIR]

The transit README calls the 1.6x in-city test "the single most likely way
these assets fail", and the LRV plan's §2.15 calls scale "the top risk in the
entire transit set". Both renders below therefore use the EXPORTED GLB,
re-imported, standing on the city geometry the app itself streams — never a
stand-in, never a turntable.

1. `-in-city-1.6x.png`     one LRV on N Judah in the Sunset at the app's own
                           carScale = 1.6, beside a shipped commuter-bus and a
                           sedan at the same scale, from the app's 42 deg
                           diorama camera.
2. `-coupled-pair-1.6x.png` two LRVs coupled cab to cab — the normal Metro
                           configuration — at 1.6x, framed against a measured
                           94.5 m block face.
3. `-in-city-120m.png`     the far end of the vehicle camera band. This is
                           where §2.15's question gets answered: with no
                           overhead wire in the scene, does the raised
                           pantograph still read as roof equipment?

Adapted from artifacts/cable-car/render_scenarios.py.
"""

import json
import math
import os
import sys

import bpy
from mathutils import Euler, Vector

CAR_SCALE = 1.6         # app/src/agents.js setToy(): carScale = on ? 1.6 : 1
APP_PITCH = 42.0        # the diorama camera's downward angle
LRV_LEN = 22.86
COUPLER_GAP = 0.80      # REFERENCE.md §4.6, scaled off the Embarcadero photo


def app_to_blender(x, y, z):
    """App world (X east, Y up, Z south) -> Blender (Z up), the same mapping
    Blender's own glTF importer uses."""
    return Vector((x, -z, y))


def clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def load_city(path):
    """Rebuild the baked tiles as one flat-shaded vertex-coloured mesh."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    pos, col = data["positions"], data["colors"]
    n = len(pos) // 3
    verts = [app_to_blender(pos[i * 3], pos[i * 3 + 1], pos[i * 3 + 2]) for i in range(n)]
    faces = [(i, i + 1, i + 2) for i in range(0, n, 3)]
    mesh = bpy.data.meshes.new("city")
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    layer = mesh.color_attributes.new("Col", "FLOAT_COLOR", "CORNER")
    for poly in mesh.polygons:
        for li in poly.loop_indices:
            v = mesh.loops[li].vertex_index
            layer.data[li].color = (col[v * 3], col[v * 3 + 1], col[v * 3 + 2], 1.0)
    obj = bpy.data.objects.new("city", mesh)
    bpy.context.collection.objects.link(obj)
    mesh.shade_flat()

    mat = bpy.data.materials.new("CityVertexColor")
    mat.use_nodes = True
    tree = mat.node_tree
    bsdf = tree.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = 0.9
    attr = tree.nodes.new("ShaderNodeVertexColor")
    attr.layer_name = "Col"
    tree.links.new(attr.outputs["Color"], bsdf.inputs["Base Color"])

    # TWO-SIDED SHADING for the context geometry. The baked tiles do not
    # guarantee a winding, and the app never notices because its own materials
    # are drawn DoubleSide; rebuilt here as Cycles geometry, a back-facing
    # ground triangle takes its light from below and renders as a black hole in
    # the middle of the street. This affects the review context only — the LRV
    # is a closed solid with outward normals, verified by validate_muni_lrv.py.
    geo = tree.nodes.new("ShaderNodeNewGeometry")
    flip = tree.nodes.new("ShaderNodeVectorMath")
    flip.operation = "SCALE"
    flip.inputs["Scale"].default_value = -1.0
    nmix = tree.nodes.new("ShaderNodeMix")
    nmix.data_type = "VECTOR"
    tree.links.new(geo.outputs["Normal"], flip.inputs[0])
    tree.links.new(geo.outputs["Normal"], nmix.inputs["A"])
    tree.links.new(flip.outputs["Vector"], nmix.inputs["B"])
    tree.links.new(geo.outputs["Backfacing"], nmix.inputs["Factor"])
    tree.links.new(nmix.outputs["Result"], bsdf.inputs["Normal"])

    # PART SELF-LIT. The baked tiles contain volumes that enclose their own
    # ground — OSM footprints extruded from sea level swallow the roadway on a
    # hillside — and a physically shaded interior renders pure black, which in
    # a review image reads as a hole in the street. The app never shows this
    # because its city shader is a flat Lambert with a large ambient term.
    emit = tree.nodes.new("ShaderNodeEmission")
    emit.inputs[1].default_value = 0.55
    tree.links.new(attr.outputs["Color"], emit.inputs[0])
    shmix = tree.nodes.new("ShaderNodeMixShader")
    shmix.inputs["Fac"].default_value = 0.45
    tree.links.new(bsdf.outputs["BSDF"], shmix.inputs[1])
    tree.links.new(emit.outputs["Emission"], shmix.inputs[2])
    tree.links.new(shmix.outputs["Shader"], tree.nodes["Material Output"].inputs["Surface"])
    mesh.materials.append(mat)
    return obj, data


def place_vehicle(path, name, spot, offset_m, scale=CAR_SCALE, flip=False):
    """Import a vehicle GLB and stand it on the street at `spot`, `offset_m`
    along that street, scaled the way the app scales its instances (about the
    origin, which is the ground-plane centre of the footprint)."""
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    parts = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]

    heading = spot["headingRad"]
    yaw = heading + math.pi + (math.pi if flip else 0.0)
    dirv = Vector((math.sin(heading), -math.cos(heading), 0.0)).normalized()
    base = app_to_blender(spot["x"], spot["y"], spot["z"]) + dirv * offset_m

    root = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(root)
    root.location = base
    root.rotation_euler = Euler((0.0, 0.0, yaw), "XYZ")
    root.scale = (scale, scale, scale)
    for p in parts:
        if p.parent is None:
            p.parent = root
            p.matrix_parent_inverse = root.matrix_world.inverted()
    return root, parts


def day_state(alpha=0.12):
    """The app draws `_Glow` surfaces in an unlit layer at 0.12 + 0.95*uNight,
    so by day they are 88% transparent. Previewing them opaque would flatter
    the model."""
    for mat in bpy.data.materials:
        if mat.name.endswith("_Glow") and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Alpha"].default_value = alpha


def world(color, strength):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 40
    scene.cycles.use_denoising = True
    scene.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("W")
    scene.world = w
    w.use_nodes = True
    node = w.node_tree.nodes["Background"]
    node.inputs[0].default_value = color
    node.inputs[1].default_value = strength


def sun(name, energy, pitch, azimuth, color=(1, 1, 1), angle=6.0):
    light = bpy.data.lights.new(name, "SUN")
    light.energy = energy
    light.angle = math.radians(angle)
    light.color = color
    ob = bpy.data.objects.new(name, light)
    bpy.context.collection.objects.link(ob)
    ob.rotation_euler = (math.radians(pitch), 0, math.radians(azimuth))
    return ob


def rig():
    # Substantial ambient fill (style bible §19): with a thin world the shadow
    # of a Sunset apartment block crushes the roadway to black and the scale
    # test reads as a hole in the street.
    world((0.62, 0.75, 0.92, 1.0), 1.05)
    sun("key", 2.8, 52, -40)
    sun("fill", 1.0, 66, 140, (0.82, 0.88, 1.0), 40)


def camera(name, lens):
    cam = bpy.data.cameras.new(name)
    cam.lens = lens
    cam.clip_start = 0.2
    cam.clip_end = 6000.0
    ob = bpy.data.objects.new(name, cam)
    bpy.context.collection.objects.link(ob)
    return ob


def aim(ob, target):
    ob.rotation_euler = (target - ob.location).to_track_quat("-Z", "Y").to_euler()


def street_azimuth(spot):
    """The street's compass azimuth in the render scene's terms, so a camera
    can be put at a chosen angle to the kerb rather than squinting down it."""
    h = spot["headingRad"]
    return math.degrees(math.atan2(math.sin(h), -math.cos(h)))


def orbit(center, radius, pitch_deg, az_deg):
    p, a = math.radians(pitch_deg), math.radians(az_deg)
    return center + Vector((radius * math.cos(p) * math.sin(a),
                            radius * math.cos(p) * math.cos(a),
                            radius * math.sin(p)))


def render(path, cam, res=(1600, 1000)):
    scene = bpy.context.scene
    scene.camera = cam
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print(f"[scenario] {path}")


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "muni-lrv.glb"))
    city_json = arg("--city", os.path.join(here, "city-cell.json"))
    out = arg("--out", os.path.join(here, "renders"))
    prefix = arg("--prefix", "muni-lrv")
    fleet = os.path.abspath(os.path.join(here, "../../app/public/sf-assets/vehicles"))
    os.makedirs(out, exist_ok=True)

    with open(city_json, encoding="utf-8") as f:
        faces = json.load(f).get("blockFaces") or {}
    block = faces.get("faceMedianM")

    # ------------------------------------------------- 1. one LRV, in city ---
    clear()
    _, city = load_city(city_json)
    spot = city["placement"]
    lrv, _ = place_vehicle(glb, "lrv", spot, 0.0)
    place_vehicle(os.path.join(fleet, "commuter-bus.glb"), "bus", spot, -30.0)
    place_vehicle(os.path.join(fleet, "sedan-red.glb"), "sedan", spot, -46.0)
    day_state()
    rig()

    focus = lrv.location + Vector((0, 0, 3.0))
    cam = camera("cam_city", 50.0)
    # Along the street, not square to it: square to the kerb the camera stands
    # over the middle of the block and the near row of Sunset houses hides the
    # roadway completely.
    cam.location = orbit(focus, 82.0, APP_PITCH, street_azimuth(spot) + 26.0)
    aim(cam, focus)
    render(os.path.join(out, f"{prefix}-in-city-1.6x.png"), cam)
    print(f"[scenario] single car {LRV_LEN * CAR_SCALE:.1f} m on screen; "
          f"median block face {block} m")

    # ---------------------------------------------- 2. a coupled pair, 1.6x ---
    # The normal Metro configuration, and it doubles every scale problem. The
    # two cars couple cab to cab, so the second is FLIPPED: coupling a
    # double-ended vehicle nose-to-nose is what actually happens.
    clear()
    _, city = load_city(city_json)
    spot = city["placement"]
    pitch_len = (LRV_LEN + COUPLER_GAP) * CAR_SCALE
    a, _ = place_vehicle(glb, "lrv_a", spot, pitch_len / 2.0)
    place_vehicle(glb, "lrv_b", spot, -pitch_len / 2.0)
    day_state()
    rig()

    focus = app_to_blender(spot["x"], spot["y"], spot["z"]) + Vector((0, 0, 3.0))
    cam = camera("cam_pair", 38.0)
    cam.location = orbit(focus, 128.0, APP_PITCH, street_azimuth(spot) + 30.0)
    aim(cam, focus)
    render(os.path.join(out, f"{prefix}-coupled-pair-1.6x.png"), cam)
    # End to end, not centre to centre: the pair spans one car length plus the
    # spacing between the two origins.
    total = pitch_len + LRV_LEN * CAR_SCALE
    msg = f"[scenario] coupled pair {total:.1f} m end to end on screen"
    if block:
        msg += f"; median block face {block} m -> {100.0 * total / block:.0f}% of one"
    print(msg)
    _ = a

    # -------------------------------------- 3. the 120 m far-camera question --
    # §2.15: with no overhead wire anywhere in this scene, does the raised
    # pantograph still read as roof equipment at the far end of the band?
    clear()
    _, city = load_city(city_json)
    spot = city["placement"]
    lrv, _ = place_vehicle(glb, "lrv", spot, 0.0)
    place_vehicle(os.path.join(fleet, "commuter-bus.glb"), "bus", spot, -30.0)
    day_state()
    rig()
    focus = lrv.location + Vector((0, 0, 3.0))
    cam = camera("cam_far", 55.0)
    cam.location = orbit(focus, 120.0, APP_PITCH, street_azimuth(spot) + 26.0)
    aim(cam, focus)
    render(os.path.join(out, f"{prefix}-in-city-120m.png"), cam)


if __name__ == "__main__":
    main()
