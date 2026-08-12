"""The two mandatory extra renders: the 1.6x in-city scale test and the
side-by-side against the hybrid bus at the app's camera distance.

    blender -b --python render_in_city.py -- [--out DIR] [--samples N]

WHY THIS SCRIPT EXISTS
----------------------
`docs/asset-plans/transit/README.md` calls the 1.6x scale test "the single most
likely way these assets fail, and it will not show up on an isolated turntable".
The plan additionally requires a side-by-side against `muni-bus-40`, because if
a player cannot tell the two coaches apart at the app's camera distance the
poles are too thin and this asset has failed its one job.

WHAT "REAL BAKED CITY GEOMETRY" MEANS HERE
------------------------------------------
The city is rebuilt from the repository's OWN shipped tiles — the same bytes the
browser streams — decoded here with the record layouts documented in
`app/src/tilebin.js`:

    app/public/tiles/toy/<cell>.bin          building footprints + base/top y
    app/public/tiles/toystreets/<cell>.bin   street polylines + per-point y
    app/public/tiles/toy.json                the palette and the class widths

Real footprints, real heights, real positions, real palette. What is NOT
reproduced is the toy shader's window banding, the storefront strip, landcover,
trees and street furniture — this is a massing stand-in for scale judgement, not
a second renderer. Everything the two renders are used to decide (how tall the
poles stand against the housing, whether the two coaches read apart) depends on
massing and silhouette, which is exactly what is here.

THE CAMERA IS THE APP'S CAMERA
------------------------------
`app/src/camera.js` locks diorama mode to **pitch 42 deg**; `app/src/main.js`
sets **`camera.fov = 18`** (three.js fov is VERTICAL). Both are reproduced
exactly, at 1920x1080, so a pixel here is a pixel there. `DIORAMA.min = 150`, so
150 m is the closest a player can actually get — that frame is rendered too, and
it is the honest worst case for reading the poles.

Vehicle scale is `carScale = 1.6` from `agents.js` `setToy()`, applied to the
shipped GLBs exactly as the app applies it to its fleet instances.
"""

import json
import math
import os
import struct
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
TILES = os.path.join(REPO, "app", "public", "tiles")

TROLLEY = os.path.join(HERE, "muni-trolley-40.glb")
BUS = os.path.join(os.path.dirname(HERE), "muni-bus", "muni-bus-40.glb")

CAR_SCALE = 1.6          # agents.js setToy()
DIORAMA_PITCH = 42.0     # camera.js DIORAMA.pitch
DIORAMA_FOV_V = 18.0     # main.js camera.fov in toy mode (three.js fov = vertical)
DIORAMA_MIN_D = 150.0    # camera.js DIORAMA.min — the closest a player can get

# California & Larkin, on the 1 California — the line the shipped sign names.
# Nob Hill: real two- and three-storey housing, which is what the poles have to
# stand against.
SITE_LON, SITE_LAT = -122.4185, 37.7915
LON0, LAT0 = -122.4375, 37.77


def project(lon, lat):
    """The ONE projection, mirrored from AGENTS.md. +x east, -z north, metres."""
    return ((lon - LON0) * 111320.0 * math.cos(math.radians(LAT0)),
            -(lat - LAT0) * 110540.0)


# ------------------------------------------------------------ tile decoding


def _read(buf, fmt, off, n):
    size = struct.calcsize(fmt)
    return struct.unpack_from(f"<{n}{fmt}", buf, off), off + size * n


def read_buildings(buf):
    """app/src/tilebin.js readBuildings(), transcribed."""
    version = struct.unpack_from("<H", buf, 4)[0]
    count, vertex_total, index_total = struct.unpack_from("<III", buf, 8)
    origin_x, origin_z, quant = struct.unpack_from("<fff", buf, 20)
    off = 32
    _vert_off, off = _read(buf, "I", off, count)
    _idx_off, off = _read(buf, "I", off, count)
    vert_count, off = _read(buf, "H", off, count)
    _idx_count, off = _read(buf, "H", off, count)
    base_y, off = _read(buf, "h", off, count)
    top_y, off = _read(buf, "h", off, count)
    palette, off = _read(buf, "B", off, count)
    _seed, off = _read(buf, "B", off, count)
    roof_palette = None
    if version >= 2:
        _flags, off = _read(buf, "B", off, count)
        roof_palette, off = _read(buf, "B", off, count)
    if version >= 3:
        for _ in range(3):
            _x, off = _read(buf, "B", off, count)
    off = (off + 1) // 2 * 2
    verts, off = _read(buf, "h", off, vertex_total * 2)
    return dict(count=count, origin_x=origin_x, origin_z=origin_z, quant=quant,
                vert_off=_vert_off, vert_count=vert_count, base_y=base_y,
                top_y=top_y, palette=palette, roof_palette=roof_palette,
                verts=verts)


def read_streets(buf):
    """app/src/tilebin.js readStreets(), transcribed."""
    count, point_total = struct.unpack_from("<II", buf, 8)
    origin_x, origin_z, quant = struct.unpack_from("<fff", buf, 20)
    off = 32
    pt_off, off = _read(buf, "I", off, count)
    pt_count, off = _read(buf, "H", off, count)
    klass, off = _read(buf, "B", off, count)
    _flags, off = _read(buf, "B", off, count)
    off = (off + 1) // 2 * 2
    xz, off = _read(buf, "h", off, point_total * 2)
    y, off = _read(buf, "h", off, point_total)
    return dict(count=count, origin_x=origin_x, origin_z=origin_z, quant=quant,
                pt_off=pt_off, pt_count=pt_count, klass=klass, xz=xz, y=y)


def cells_around(x, z, radius_cells=2):
    meta = json.load(open(os.path.join(TILES, "toy.json")))
    g = meta["grid"]
    size = meta["cellSize"]
    cx = int(math.floor((x - g["originX"]) / size))
    cz = int(math.floor((z - g["originZ"]) / size))
    keys = [f"{cx + dx}_{cz + dz}"
            for dx in range(-radius_cells, radius_cells + 1)
            for dz in range(-radius_cells, radius_cells + 1)]
    return meta, keys


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def flat_material(name, rgb, rough=0.9):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    b = mat.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*[srgb_to_linear(c) for c in rgb], 1.0)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = 0.0
    return mat


# ------------------------------------------------------------- city building


def build_city(meta, keys):
    """Extrude the baked footprints and lay the baked street ribbons."""
    palette = [p["color"] for p in meta["palette"]]
    classes = meta["streetClasses"]

    verts, faces, mat_idx = [], [], []
    mats = {}

    def mat_for(rgb, tag):
        key = f"{tag}_{int(rgb[0] * 255)}_{int(rgb[1] * 255)}_{int(rgb[2] * 255)}"
        if key not in mats:
            mats[key] = (len(mats), flat_material(key, rgb))
        return mats[key][0]

    n_buildings = 0
    for key in keys:
        path = os.path.join(TILES, "toy", f"{key}.bin")
        if not os.path.exists(path):
            continue
        d = read_buildings(open(path, "rb").read())
        for b in range(d["count"]):
            n = d["vert_count"][b]
            if n < 3:
                continue
            vo = d["vert_off"][b]
            base = d["base_y"][b] * 0.1
            top = d["top_y"][b] * 0.1
            if top - base < 0.5:
                continue
            wall = palette[d["palette"][b] % len(palette)]
            roof = palette[(d["roof_palette"][b] if d["roof_palette"] else 0) % len(palette)]
            ring = [(d["origin_x"] + d["verts"][(vo + k) * 2] * d["quant"],
                     d["origin_z"] + d["verts"][(vo + k) * 2 + 1] * d["quant"])
                    for k in range(n)]
            b0 = len(verts)
            # Blender is Z-up and the city data is Y-up: (x, y, z)_city ->
            # (x, -z, y)_blender, the same handedness swap the GLB round trip uses.
            verts.extend([(px, -pz, base) for px, pz in ring])
            verts.extend([(px, -pz, top) for px, pz in ring])
            wi = mat_for(wall, "wall")
            ri = mat_for(roof, "roof")
            for k in range(n):
                k2 = (k + 1) % n
                faces.append((b0 + k, b0 + k2, b0 + n + k2, b0 + n + k))
                mat_idx.append(wi)
            faces.append(tuple(b0 + n + k for k in range(n)))
            mat_idx.append(ri)
            n_buildings += 1

    # The baked street tiers, by class index (toy.json streetClasses): 0-6 are
    # carriageways, 7-8 sidewalks, 9-11 painted markings. Drawing all three as
    # one dark ribbon would put asphalt where the app draws pavement and lose
    # the road markings that give the diorama its scale cues, so each tier gets
    # its own flat colour and its own lift out of the z-fight.
    TIERS = (
        ("asphalt", range(0, 7), (0.235, 0.235, 0.251), 0.02),
        ("sidewalk", range(7, 9), (0.784, 0.765, 0.706), 0.05),
        ("marking", range(9, 12), (0.925, 0.910, 0.870), 0.09),
    )
    tier_of = {k: t for t in TIERS for k in t[1]}

    road_verts = {t[0]: [] for t in TIERS}
    road_faces = {t[0]: [] for t in TIERS}
    roads = []           # kept for placing the vehicles on a real centreline
    for key in keys:
        path = os.path.join(TILES, "toystreets", f"{key}.bin")
        if not os.path.exists(path):
            continue
        d = read_streets(open(path, "rb").read())
        for l in range(d["count"]):
            n = d["pt_count"][l]
            if n < 2:
                continue
            kl = d["klass"][l]
            cls = classes[kl] if kl < len(classes) else classes[-1]
            tier = tier_of.get(kl, TIERS[0])
            half = cls["width"] / 2.0
            po = d["pt_off"][l]
            pts = [(d["origin_x"] + d["xz"][(po + k) * 2] * d["quant"],
                    d["y"][po + k] * 0.1,
                    d["origin_z"] + d["xz"][(po + k) * 2 + 1] * d["quant"])
                   for k in range(n)]
            if tier[0] == "asphalt":
                roads.append({"pts": pts, "width": cls["width"], "klass": kl})
            rv, rf = road_verts[tier[0]], road_faces[tier[0]]
            for k in range(n - 1):
                x0, y0, z0 = pts[k]
                x1, y1, z1 = pts[k + 1]
                dx, dz = x1 - x0, z1 - z0
                ln = math.hypot(dx, dz)
                if ln < 1e-3:
                    continue
                nx, nz = -dz / ln * half, dx / ln * half
                b0 = len(rv)
                rv.extend([
                    (x0 + nx, -(z0 + nz), y0 + tier[3]), (x0 - nx, -(z0 - nz), y0 + tier[3]),
                    (x1 - nx, -(z1 - nz), y1 + tier[3]), (x1 + nx, -(z1 + nz), y1 + tier[3]),
                ])
                rf.append((b0, b0 + 1, b0 + 2, b0 + 3))

    mesh = bpy.data.meshes.new("city_buildings")
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    ordered = sorted(mats.values(), key=lambda kv: kv[0])
    for _i, m in ordered:
        mesh.materials.append(m)
    mesh.validate()
    for i, poly in enumerate(mesh.polygons):
        poly.material_index = mat_idx[i]
    mesh.shade_flat()
    obj = bpy.data.objects.new("city_buildings", mesh)
    bpy.context.collection.objects.link(obj)

    for tag, _ks, rgb, _lift in TIERS:
        if not road_faces[tag]:
            continue
        rmesh = bpy.data.meshes.new(f"city_{tag}")
        rmesh.from_pydata([Vector(v) for v in road_verts[tag]], [], road_faces[tag])
        rmesh.materials.append(flat_material(f"street_{tag}", rgb))
        rmesh.validate()
        rmesh.shade_flat()
        bpy.context.collection.objects.link(bpy.data.objects.new(f"city_{tag}", rmesh))

    print(f"[in-city] {n_buildings} baked buildings, {len(roads)} baked street lines "
          f"from {len(keys)} cells")
    return roads


def pick_road(roads, x, z, min_width=11.0):
    """Nearest reasonably wide baked street segment to the site — the vehicles
    are placed on real street geometry rather than a made-up line.

    The baked polylines are subdivided at roughly one segment per 10 m, so the
    length filter has to be well under that: an earlier 12 m floor rejected the
    entire city.
    """
    best = None
    for r in roads:
        if r["width"] < min_width:
            continue
        for k in range(len(r["pts"]) - 1):
            a, b = r["pts"][k], r["pts"][k + 1]
            if math.hypot(b[0] - a[0], b[2] - a[2]) < 6.0:
                continue
            mx, mz = (a[0] + b[0]) / 2, (a[2] + b[2]) / 2
            d = math.hypot(mx - x, mz - z)
            if best is None or d < best[0]:
                best = (d, a, b, r["width"])
    return best


# ---------------------------------------------------------------- placement


def place_glb(path, name, location, heading, scale):
    """Import a shipped GLB, scale it by `carScale`, and point the nose down the
    street. Nothing about the file is edited — this is the same geometry the
    manifest would name."""
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    objs = [o for o in set(bpy.data.objects) - before]
    parent = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(parent)
    for o in objs:
        if o.parent is None:
            o.parent = parent
    parent.scale = (scale, scale, scale)
    # Authored nose is +Y in Blender; rotate about Z so it runs down the street.
    parent.rotation_euler = (0.0, 0.0, heading)
    parent.location = location
    return parent


def app_camera(target, distance, yaw_deg, res=(1920, 1080)):
    """The app's own diorama camera: 42 deg down, 18 deg VERTICAL fov."""
    cam = bpy.data.cameras.new("cam_app")
    cam.sensor_fit = "VERTICAL"
    cam.sensor_height = 24.0
    cam.lens = 12.0 / math.tan(math.radians(DIORAMA_FOV_V / 2.0))
    obj = bpy.data.objects.new("cam_app", cam)
    bpy.context.collection.objects.link(obj)
    pitch = math.radians(DIORAMA_PITCH)
    yaw = math.radians(yaw_deg)
    obj.location = (target[0] + distance * math.cos(pitch) * math.sin(yaw),
                    target[1] - distance * math.cos(pitch) * math.cos(yaw),
                    target[2] + distance * math.sin(pitch))
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()
    return obj, res


def day_rig():
    w = bpy.data.worlds.new("W")
    bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.60, 0.69, 0.80, 1.0)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.95
    for nm, rot, e, ang, col in (
        ("key", (52, 0, 38), 2.5, 0.14, (1.0, 0.97, 0.92)),
        ("fill", (64, 0, 214), 1.1, 0.6, (0.86, 0.90, 1.0)),
        ("rim", (76, 0, 128), 0.55, 0.8, (1.0, 0.97, 0.92)),
    ):
        d = bpy.data.lights.new(nm, type="SUN")
        d.energy, d.angle, d.color = e, ang, col
        o = bpy.data.objects.new(nm, d)
        o.rotation_euler = tuple(math.radians(v) for v in rot)
        bpy.context.collection.objects.link(o)


def render(cam, res, path, samples):
    sc = bpy.context.scene
    sc.camera = cam
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.render.filepath = path
    sc.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(write_still=True)
    print(f"[in-city] {path}")


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = argv[argv.index("--out") + 1] if "--out" in argv else os.path.join(HERE, "renders")
    samples = int(argv[argv.index("--samples") + 1] if "--samples" in argv else 48)
    os.makedirs(out, exist_ok=True)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    x, z = project(SITE_LON, SITE_LAT)
    meta, keys = cells_around(x, z)
    roads = build_city(meta, keys)
    day_rig()

    hit = pick_road(roads, x, z)
    if hit is None:
        raise SystemExit("no baked street near the site")
    _d, a, b, width = hit
    # City (x, y, z) -> Blender (x, -z, y). The street's Blender-plane direction:
    dx, dy = b[0] - a[0], -(b[2] - a[2])
    # A Z rotation by h sends the authored nose (+Y) to (-sin h, cos h), so the
    # heading that points the nose down the street is atan2(-dx, dy). Dropping
    # that minus mirrors every vehicle about the street's north axis and parks
    # the coach diagonally through the buildings — which is how it was caught.
    heading = math.atan2(-dx, dy)
    ux, uy = -math.sin(heading), math.cos(heading)     # along the street
    road_y = (a[1] + b[1]) / 2.0
    mid = ((a[0] + b[0]) / 2.0, -(a[2] + b[2]) / 2.0, road_y)
    print(f"[in-city] street width {width} m, heading {math.degrees(heading):.1f} deg, "
          f"y {road_y:.2f} m")

    # --- frame 1: the coach alone in the real city at 1.6x, from 150 m, which
    #     is the closest the diorama camera is allowed to get.
    place_glb(TROLLEY, "trolley", (mid[0], mid[1], mid[2]), heading, CAR_SCALE)
    cam, res = app_camera((mid[0], mid[1], mid[2] + 3.0), DIORAMA_MIN_D,
                          math.degrees(heading) + 128.0)
    render(cam, res, os.path.join(out, "muni-trolley-40-in-city-1.6x.png"), samples)

    # --- frames 2-4: the side-by-side. The two coaches queued in the same lane
    #     26 m apart — what a player actually sees on a trolleybus line, not two
    #     turntable models placed next to each other. ONE arrangement, rendered
    #     at three distances, so the only variable between the frames is range.
    #
    #     120 m is the far vehicle distance the transit README budgets against.
    #     150 m is `DIORAMA.min` — the closest the player is allowed to get, and
    #     therefore the honest best case. 90 m is below both and exists only to
    #     confirm what the detail looks like when it is not the limiting factor.
    gap = 26.0
    place_glb(BUS, "bus", (mid[0] + ux * gap, mid[1] + uy * gap, mid[2]), heading, CAR_SCALE)
    trolley = bpy.data.objects["trolley"]
    trolley.location = (mid[0] - ux * 4.0, mid[1] - uy * 4.0, mid[2])
    look = (mid[0] + ux * (gap - 4.0) / 2.0, mid[1] + uy * (gap - 4.0) / 2.0, mid[2] + 3.0)
    for dist, tag in ((120.0, "120m"), (DIORAMA_MIN_D, "150m-app-min"), (90.0, "90m")):
        cam, res = app_camera(look, dist, math.degrees(heading) + 96.0)
        render(cam, res,
               os.path.join(out, f"muni-trolley-40-vs-hybrid-bus-{tag}.png"), samples)


if __name__ == "__main__":
    main()
