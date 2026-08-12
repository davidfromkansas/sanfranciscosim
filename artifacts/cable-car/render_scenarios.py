"""The three mandatory decision renders for the Powell cable car.

    node export_city_cell.mjs          # writes city-cell.json first
    blender -b --python render_scenarios.py -- [--glb FILE] [--out DIR]

1. `-in-city.png`   the car at the app's 1.6x render scale, standing on a real
                    baked SF street with the real baked buildings around it,
                    beside a shipped bus and sedan at the same 1.6x. This is the
                    single most likely way a transit asset fails and it does not
                    show up on a turntable (transit README, "The app renders
                    vehicles at 1.6x real scale").
2. `-tilted.png`    the same car on a real 20% residential grade, from the app
                    camera: do the roofline, running boards and figures still
                    read when the whole vehicle is pitched?
3. `-backlit.png`   the car silhouetted against a bright sky from the app's
                    42-degree camera at 120 m. If the open sections do not
                    survive this, the model has lost its identity.

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
    nrm = data["normals"]
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
    # guarantee a winding, and the app never notices because its own materials
    # are drawn DoubleSide; rebuilt here as Cycles geometry, a back-facing
    # ground triangle takes its light from below and renders as a black hole in
    # the middle of the street.  Flipping the shading normal on backfaces makes
    # every face light as if it were facing the camera.  This affects the
    # review context only - the cable car itself is a closed solid with
    # outward normals, verified by validate_cable_car.py.
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
    # ground - OSM footprints extruded from sea level swallow the roadway on a
    # hillside - and a physically shaded interior renders pure black, which in
    # a review image reads as a hole in the street rather than as what it is.
    # The app never shows this because its city shader is a flat Lambert with
    # a large ambient term. Mixing 45% emission of each face's own colour
    # reproduces that, so no context surface can go to zero. The cable car
    # itself is shaded normally - it is the thing under review.
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
    _ = nrm  # normals are recomputed from the winding; kept in the file for reuse
    return obj, data


def place_vehicle(path, name, spot, offset_m, pitch_deg, scale=CAR_SCALE):
    """Import a vehicle GLB and stand it on the street at `spot`, `offset_m`
    along that street, pitched to the grade and scaled the way the app scales
    its instances (about the origin, which is the ground-plane centre)."""
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    parts = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]

    heading = spot["headingRad"]
    yaw = heading + math.pi                     # car front (+Y) up the street
    dirv = Vector((math.sin(heading), -math.cos(heading), 0.0)).normalized()
    base = app_to_blender(spot["x"], spot["y"], spot["z"]) + dirv * offset_m
    base.z += offset_m * math.tan(math.radians(pitch_deg)) * (1 if offset_m > 0 else 1)

    root = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(root)
    root.location = base
    # XYZ euler = Rz(yaw) @ Rx(pitch): pitch about the car's own lateral axis
    # first, then yaw onto the street.
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
    can be put square to the kerb instead of squinting down the roadway."""
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

    glb = arg("--glb", os.path.join(here, "cable-car-powell.glb"))
    # Russian Hill, cell 19_8: the Powell-Hyde blocks. It carries both the
    # level segment the scale test stands on and the 20.2% segment the grade
    # test uses, so both renders are the same real piece of city.
    city_json = arg("--city", os.path.join(here, "city-cell.json"))
    city_flat = arg("--city-flat", city_json)
    out = arg("--out", os.path.join(here, "renders"))
    prefix = arg("--prefix", "cable-car-powell")
    fleet = os.path.abspath(os.path.join(here, "../../app/public/sf-assets/vehicles"))
    os.makedirs(out, exist_ok=True)

    # ---------------------------------------------------------- 1. in city ---
    clear()
    _, city = load_city(city_flat)
    level = city["placementFlat"] or city["placement"]

    car, _ = place_vehicle(glb, "cablecar", level, 0.0, 0.0)
    place_vehicle(os.path.join(fleet, "commuter-bus.glb"), "bus", level, -20.0, 0.0)
    place_vehicle(os.path.join(fleet, "sedan-red.glb"), "sedan", level, 13.0, 0.0)
    day_state()
    # Substantial ambient fill (style bible s.19): at 0.55 world / 0.5 fill the
    # shadow of a Russian Hill apartment block crushes the roadway to pure
    # black and the scale test reads as a hole in the street.
    world((0.62, 0.75, 0.92, 1.0), 1.05)
    sun("key", 2.8, 52, -40)
    sun("fill", 1.0, 66, 140, (0.82, 0.88, 1.0), 40)

    focus = car.location + Vector((0, 0, 3.0))
    cam = camera("cam_city", 50.0)
    # DOWN the street, not across it: square to the kerb the camera stands over
    # the middle of a block and the near row of houses hides the roadway
    # completely (first attempt did exactly that).
    cam.location = orbit(focus, 58.0, APP_PITCH, street_azimuth(level) + 24.0)
    aim(cam, focus)
    render(os.path.join(out, f"{prefix}-in-city.png"), cam, (1500, 1000))

    # ------------------------------------------------------- 2. on the grade -
    clear()
    _, city = load_city(city_json)
    grade = city["placement"]
    pitch = math.degrees(math.atan(grade["gradePct"] / 100.0))
    car, _ = place_vehicle(glb, "cablecar", grade, 0.0, pitch)
    day_state()
    # Substantial ambient fill (style bible s.19): at 0.55 world / 0.5 fill the
    # shadow of a Russian Hill apartment block crushes the roadway to pure
    # black and the scale test reads as a hole in the street.
    world((0.62, 0.75, 0.92, 1.0), 1.05)
    sun("key", 2.8, 52, -40)
    sun("fill", 1.0, 66, 140, (0.82, 0.88, 1.0), 40)

    focus = car.location + Vector((0, 0, 2.6))
    cam = camera("cam_grade", 62.0)
    # Square to the kerb, not along it: a camera pointed up the roadway turns
    # the pitch into foreshortening and proves nothing about the grade.
    cam.location = orbit(focus, 64.0, APP_PITCH, street_azimuth(grade) + 90.0)
    aim(cam, focus)
    render(os.path.join(out, f"{prefix}-tilted.png"), cam, (1500, 1000))
    print(f"[scenario] tilted at {grade['gradePct']:.1f}% ({pitch:.1f} deg), "
          f"{grade['klass']} street")

    # ----------------------------------------------------------- 3. backlit --
    # No city: the point is the SILHOUETTE. Bright sky behind, the sun aimed
    # into the camera, the car in its own shadow, framed as it appears at 120 m
    # through the app's 55 mm-equivalent lens.
    clear()
    bpy.ops.import_scene.gltf(filepath=glb)
    for o in bpy.data.objects:
        if o.type == "MESH":
            o.scale = (CAR_SCALE, CAR_SCALE, CAR_SCALE)
    bpy.context.view_layer.update()
    day_state()
    # A bright emissive backdrop rather than a blown-out world: the test is
    # whether the VOIDS punch through as bright shapes, which needs the car
    # dark and the background bright, not everything bright.
    world((0.46, 0.52, 0.60, 1.0), 0.30)
    sun("fill", 0.45, 58, -150, (0.80, 0.86, 1.0), 45)

    center = Vector((0, 0, 3.18 * CAR_SCALE * 0.5))
    cam = camera("cam_backlit", 55.0)
    cam.location = orbit(center, FAR_M, APP_PITCH, 298.0)
    aim(cam, center)

    away = (center - cam.location).normalized()
    bpy.ops.mesh.primitive_plane_add(size=260, location=center + away * 55.0)
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
    # A crop at the same distance, so the openness can be judged at the pixel
    # size the app actually draws.
    cam.data.lens = 300.0
    render(os.path.join(out, f"{prefix}-backlit-detail.png"), cam, (1500, 1000))


if __name__ == "__main__":
    main()
