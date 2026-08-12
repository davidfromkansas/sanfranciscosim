"""The mandatory decision renders for the F-line PCC.

    node export_city_cell.mjs          # writes city-cell.json first
    blender -b --python render_scenarios.py -- [--glb FILE] [--out DIR]

1. `-in-city.png`     the car at the app's 1.6x render scale, standing on real
                      baked lower Market with the real baked downtown around
                      it, beside a shipped bus and sedan at the same 1.6x. At
                      1.6x a PCC renders at 23.6 m; this is the single most
                      likely way a transit asset fails and it does not show up
                      on a turntable (transit README, "The app renders vehicles
                      at 1.6x real scale").
2. `-livery-*.png`    the SAME geometry with each proposed cities-series tint
                      applied through kitfleet.js's own arithmetic, from the
                      app camera. This is the render that proves the tinting
                      design before anyone writes the agents.js change: if a
                      livery reads muddy, or the fixed cream and silver fight
                      the body colour, it shows up here.
3. `-backlit.png`     the car silhouetted against a bright sky from the app's
                      42-degree camera at 120 m. The nose and the trolley pole
                      are the whole silhouette; if they do not survive this,
                      the car is a tram.

Every image uses the EXPORTED GLB, re-imported, and the city geometry the app
itself streams - never a stand-in.
"""

import json
import math
import os
import sys

import bpy
from mathutils import Euler, Vector

CAR_SCALE = 1.6         # app/src/agents.js setToy(): carScale = on ? 1.6 : 1
APP_PITCH = 42.0        # the diorama camera's downward angle
FAR_M = 120.0           # the far end of the vehicle camera band

# app/src/kitfleet.js: `Toy_body` is authored mid-warm-grey and the batch colour
# MULTIPLIES it, so a tint has to be divided by the body colour to land on the
# palette entry.  Reproduced exactly, clamp included, so the sheet proves the
# real shader arithmetic rather than an approximation of it.
BODY_BASE = (0.694, 0.659, 0.586)
TINT_CLAMP = 2.5

# The five cities-series liveries chosen in REFERENCE.md s.5.  Each is a car
# that really runs on the F line and each reads with ONE body colour against
# the model's fixed cream letterboard and silver roof.
LIVERIES = [
    ("muni-wings", "#2f7a55", 'Muni "Wings" 1948 - 1006/1008'),
    ("st-louis", "#c4453c", "St. Louis Public Service - 1050"),
    ("boston", "#e0762f", "Boston Elevated Railway - 1059"),
    ("los-angeles", "#e0af35", "Los Angeles Railway - 1052"),
    ("baltimore", "#3f9aa8", "Baltimore Transit - 1063"),
]


def srgb_to_linear(hexcode):
    h = hexcode.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


def apply_tint(hexcode):
    mat = bpy.data.materials.get("Toy_body")
    if not mat or not mat.use_nodes:
        raise SystemExit("FAIL: no Toy_body material - the livery design is dead")
    target = srgb_to_linear(hexcode)
    factor = [min(TINT_CLAMP, target[i] / BODY_BASE[i]) for i in range(3)]
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    base = bsdf.inputs["Base Color"].default_value
    bsdf.inputs["Base Color"].default_value = (
        base[0] * factor[0], base[1] * factor[1], base[2] * factor[2], 1.0
    )
    return factor


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
    pos = data["positions"]
    col = data["colors"]
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

    # TWO-SIDED SHADING for the context geometry.  The baked tiles do not
    # guarantee a winding and the app never notices because its own materials
    # are drawn DoubleSide; rebuilt here as Cycles geometry, a back-facing
    # ground triangle takes its light from below and renders as a black hole in
    # the middle of the street.  The streetcar itself is shaded normally - it
    # is the thing under review.
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

    # PART SELF-LIT.  The baked tiles contain volumes that enclose their own
    # ground, and a physically shaded interior renders pure black, which in a
    # review image reads as a hole in the street rather than as what it is. The
    # app never shows this because its city shader is a flat Lambert with a
    # large ambient term; mixing 45% emission of each face's own colour
    # reproduces that.
    emit = tree.nodes.new("ShaderNodeEmission")
    emit.inputs[1].default_value = 0.55
    tree.links.new(attr.outputs["Color"], emit.inputs[0])
    shmix = tree.nodes.new("ShaderNodeMixShader")
    shmix.inputs["Fac"].default_value = 0.45
    out = tree.nodes["Material Output"]
    tree.links.new(bsdf.outputs["BSDF"], shmix.inputs[1])
    tree.links.new(emit.outputs["Emission"], shmix.inputs[2])
    tree.links.new(shmix.outputs["Shader"], out.inputs["Surface"])
    mesh.materials.append(mat)
    return obj, data


def place_vehicle(path, name, spot, offset_m, pitch_deg, scale=CAR_SCALE):
    """Import a vehicle GLB and stand it on the street at `spot`, `offset_m`
    along that street, scaled the way the app scales its instances (about the
    origin, which is the ground-plane centre)."""
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    parts = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]

    heading = spot["headingRad"]
    yaw = heading + math.pi                     # car front (+Y) up the street
    dirv = Vector((math.sin(heading), -math.cos(heading), 0.0)).normalized()
    base = app_to_blender(spot["x"], spot["y"], spot["z"]) + dirv * offset_m
    base.z += offset_m * math.tan(math.radians(pitch_deg))

    root = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(root)
    root.location = base
    root.rotation_euler = Euler((math.radians(pitch_deg), 0.0, yaw), "XYZ")
    root.scale = (scale, scale, scale)
    for p in parts:
        if p.parent is None:
            p.parent = root
            p.matrix_parent_inverse = root.matrix_world.inverted()
    return root, parts


def day_state(alpha=0.12):
    for mat in bpy.data.materials:
        if mat.name.endswith("_Glow") and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Alpha"].default_value = alpha


def world(color, strength):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    scene.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("W")
    scene.world = w
    w.use_nodes = True
    node = w.node_tree.nodes["Background"]
    node.inputs[0].default_value = color
    node.inputs[1].default_value = strength
    return node


def sun(name, energy, pitch, azimuth, color=(1, 1, 1), angle=6.0):
    light = bpy.data.lights.new(name, "SUN")
    light.energy = energy
    light.angle = math.radians(angle)
    light.color = color
    ob = bpy.data.objects.new(name, light)
    bpy.context.collection.objects.link(ob)
    ob.rotation_euler = (math.radians(pitch), 0, math.radians(azimuth))
    return ob


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
    can be put along the kerb instead of squinting across it."""
    h = spot["headingRad"]
    return math.degrees(math.atan2(math.sin(h), -math.cos(h)))


def orbit(center, radius, pitch_deg, az_deg):
    p, a = math.radians(pitch_deg), math.radians(az_deg)
    return center + Vector(
        (
            radius * math.cos(p) * math.sin(a),
            radius * math.cos(p) * math.cos(a),
            radius * math.sin(p),
        )
    )


def render(path, cam, res):
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

    glb = arg("--glb", os.path.join(here, "f-line-pcc.glb"))
    city_json = arg("--city", os.path.join(here, "city-cell.json"))
    out = arg("--out", os.path.join(here, "renders"))
    prefix = arg("--prefix", "f-line-pcc")
    fleet = os.path.abspath(os.path.join(here, "../../app/public/sf-assets/vehicles"))
    os.makedirs(out, exist_ok=True)

    # ---------------------------------------------------------- 1. in city ---
    clear()
    _, city = load_city(city_json)
    market = city["placement"]

    car, _ = place_vehicle(glb, "pcc", market, 0.0, 0.0)
    place_vehicle(os.path.join(fleet, "commuter-bus.glb"), "bus", market, -30.0, 0.0)
    place_vehicle(os.path.join(fleet, "sedan-red.glb"), "sedan", market, 20.0, 0.0)
    apply_tint(LIVERIES[0][1])
    day_state()
    # Substantial ambient fill (style bible s.19): a downtown tower's shadow
    # crushes lower Market to pure black at a smaller world/fill, and the scale
    # test then reads as a hole in the street.
    world((0.62, 0.75, 0.92, 1.0), 0.80)
    sun("key", 2.6, 52, -40)
    sun("fill", 1.0, 66, 140, (0.82, 0.88, 1.0), 40)

    focus = car.location + Vector((0, 0, 3.4))
    cam = camera("cam_city", 58.0)
    # A three-quarter view across the kerb, which is only possible because
    # export_city_cell.mjs stands the car on the EMBARCADERO. On lower Market
    # the same offset put the camera inside a tower twice; on the waterfront
    # nothing within the crop clears 60 m and the flank - which is where the
    # livery lives - is fully visible.
    cam.location = orbit(focus, 80.0, APP_PITCH, street_azimuth(market) - 32.0)
    aim(cam, focus)
    render(os.path.join(out, f"{prefix}-in-city.png"), cam, (1500, 1000))
    print(f"[scenario] in-city on a {market['klass']} at {market['gradePct']:.1f}% grade, "
          f"car rendered at {14.76 * CAR_SCALE:.1f} m")

    # -------------------------------------------------------- 2. liveries ---
    # One image per tint, same camera, same light, same geometry.  Composed
    # into the livery sheet by make_contact_sheet.py.
    for slug, hexcode, label in LIVERIES:
        clear()
        bpy.ops.import_scene.gltf(filepath=glb)
        factor = apply_tint(hexcode)
        day_state()
        world((0.86, 0.80, 0.69, 1.0), 0.42)
        sun("key", 2.4, 50, -42)
        sun("fill", 0.7, 64, 135, (0.9, 0.94, 1.0), 38)
        bpy.ops.mesh.primitive_plane_add(size=140, location=(0, 0, -0.004))
        floor = bpy.context.object
        fmat = bpy.data.materials.new("Sheet_Floor")
        fmat.use_nodes = True
        fmat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (
            0.60, 0.53, 0.43, 1.0
        )
        floor.data.materials.append(fmat)

        centre = Vector((0, 0, 1.5))
        cam = camera(f"cam_{slug}", 88.0)
        cam.location = orbit(centre, 46.0, APP_PITCH, 126.0)
        aim(cam, centre)
        render(os.path.join(out, f"{prefix}-livery-{slug}.png"), cam, (1100, 760))
        print(f"[scenario] livery {slug} {hexcode} factor="
              f"{[round(f, 3) for f in factor]}  {label}")

    # ----------------------------------------------------------- 3. backlit --
    # No city: the point is the SILHOUETTE.  Bright sky behind, the car in its
    # own shadow, framed as it appears at 120 m through the app's lens.
    clear()
    bpy.ops.import_scene.gltf(filepath=glb)
    for o in bpy.data.objects:
        if o.type == "MESH":
            o.scale = (CAR_SCALE, CAR_SCALE, CAR_SCALE)
    bpy.context.view_layer.update()
    day_state()
    world((0.46, 0.52, 0.60, 1.0), 0.30)
    sun("fill", 0.45, 58, -150, (0.80, 0.86, 1.0), 45)

    center = Vector((0, 0, 3.124 * CAR_SCALE * 0.5))
    # A long lens, not the wide one the cable car used: at 70 mm the 23.6 m car
    # was a chip in the middle of a white frame and the silhouette - which is
    # the entire point of this render - could not be judged.
    cam = camera("cam_backlit", 155.0)
    cam.location = orbit(center, FAR_M, APP_PITCH, 300.0)
    aim(cam, center)

    away = (center - cam.location).normalized()
    bpy.ops.mesh.primitive_plane_add(size=300, location=center + away * 60.0)
    sky = bpy.context.object
    sky.name = "backdrop"
    sky.rotation_euler = (-away).to_track_quat("Z", "Y").to_euler()
    smat = bpy.data.materials.new("Backdrop")
    smat.use_nodes = True
    nt = smat.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    emit = nt.nodes.new("ShaderNodeEmission")
    emit.inputs[0].default_value = (1.0, 0.98, 0.94, 1.0)
    emit.inputs[1].default_value = 9.0
    nt.links.new(emit.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    sky.data.materials.append(smat)
    render(os.path.join(out, f"{prefix}-backlit.png"), cam, (1500, 1000))


if __name__ == "__main__":
    main()
