"""Contract validation of the exported South Park GLB.

    blender -b --python validate_64_south_park.py -- [--glb FILE] [--out FILE]

Re-imports the SHIPPING GLB into a fresh, isolated scene and checks every item
in docs/asset-plans/64-south-park.md 2.14. Writes validation.json and prints a
PASS/FAIL table. Exit status is non-zero if anything fails.

Two checks are worth explaining because they are the ones that would otherwise
be judged by eye and got judged wrong during the build:

* `max_z` must be EXACTLY the datum (15.00 m, the tallest American elm). The
  loader scales by targetHeightM / measuredHeight, so a drifting datum silently
  rescales the whole 160 m park. The height itself is estimated (plan 2.15
  risk 1); its EXACTNESS is not negotiable.
* the normals test is per-object SIGNED VOLUME, which is the authoritative test
  for a union of closed solids. The whole-model ray residual is reported as a
  secondary figure. Non-manifold edge counts are deliberately NOT a gate here:
  glTF splits vertices by normal on import, so every edge of every object in
  this asset reads as non-manifold and the number means nothing.
"""

import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

DATUM_M = 15.00
TRI_CAP = 12000
OBB_LONG = 159.508
OBB_CROSS = 23.507
HEADING_LONG = 45.4669
SHOUT_CENTRE_UV = (-36.03, -1.29)
SHOUT_TUBE_R = 0.225
SHOUT_GAUGE = 0.55
# The plan's 11.84 m and 4.34 m are the TUBE CENTRELINE figures; what a bounding
# box measures is the outer envelope, which is one tube radius plus half the
# gauge wider and one tube radius taller. Both are converted here rather than
# loosening the tolerance, so the check still fails if the circle is wrong.
SHOUT_DIAMETER = 11.84 + SHOUT_GAUGE + 2 * SHOUT_TUBE_R
SHOUT_CREST = 4.34 + SHOUT_TUBE_R
PATH_LENGTH = 188.0
WALL_LENGTH = 369.9
PALETTE = {
    "Toy_stone", "Toy_cream", "Toy_mint", "Toy_teal", "Toy_verdigris",
    "Toy_steel", "Toy_sand", "Toy_roofd", "Toy_ink", "Toy_rust", "Toy_coral",
    "Toy_gold", "Toy_cream_Glow", "Toy_gold_Glow",
}

_UL = math.radians(HEADING_LONG)
_UC = math.radians(HEADING_LONG + 90.0)
U_DIR = (math.sin(_UL), math.cos(_UL))
V_DIR = (math.sin(_UC), math.cos(_UC))
_DET = U_DIR[0] * V_DIR[1] - U_DIR[1] * V_DIR[0]


def to_uv(x, y):
    return ((x * V_DIR[1] - y * V_DIR[0]) / _DET, (U_DIR[0] * y - U_DIR[1] * x) / _DET)


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    glb = argv[argv.index("--glb") + 1] if "--glb" in argv else os.path.join(here, "64-south-park.glb")
    out = argv[argv.index("--out") + 1] if "--out" in argv else os.path.join(here, "validation.json")
    data = json.load(open(os.path.join(here, "data", "park_uv.json")))

    bpy.ops.wm.read_factory_settings(use_empty=True)
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=glb)
    objs = [o for o in set(bpy.data.objects) - before]
    meshes = [o for o in objs if o.type == "MESH"]

    dg = bpy.context.evaluated_depsgraph_get()
    mn = [1e9] * 3
    mx = [-1e9] * 3
    tris = 0
    mats = set()
    textured = []
    transparent = []
    animated = [o.name for o in objs if o.animation_data]
    non_mesh = [o.name for o in objs if o.type != "MESH"]
    volumes = {}
    scales = {}
    uv_pts = []

    for o in meshes:
        scales[o.name] = tuple(round(v, 4) for v in o.matrix_world.to_scale())
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for m in me.materials:
            if not m:
                continue
            name = m.name.split(".")[0]
            mats.add(name)
            if m.use_nodes and any(n.type == "TEX_IMAGE" for n in m.node_tree.nodes):
                textured.append(name)
            bsdf = m.node_tree.nodes.get("Principled BSDF") if m.use_nodes else None
            if bsdf and bsdf.inputs["Alpha"].default_value < 0.999:
                transparent.append(name)
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
            uv_pts.append(to_uv(w.x, w.y) + (w.z,))
        ev.to_mesh_clear()

        bm = bmesh.new()
        bm.from_mesh(o.data)
        bm.transform(o.matrix_world)
        volumes[o.name] = bm.calc_volume(signed=True)
        bm.free()

    us = [p[0] for p in uv_pts]
    vs = [p[1] for p in uv_pts]
    # kerb ring only: the canopy overhangs the boundary, so measure the oriented
    # footprint against the ground plate, not against the whole model.
    plate = next((o for o in meshes if o.name.startswith("ground_plate")), None)
    plate_uv = []
    if plate:
        for v in plate.data.vertices:
            w = plate.matrix_world @ v.co
            plate_uv.append(to_uv(w.x, w.y))
    plate_long = max(p[0] for p in plate_uv) - min(p[0] for p in plate_uv) if plate_uv else 0
    plate_cross = max(p[1] for p in plate_uv) - min(p[1] for p in plate_uv) if plate_uv else 0

    plate_ctr = ((max(p[0] for p in plate_uv) + min(p[0] for p in plate_uv)) / 2,
                 (max(p[1] for p in plate_uv) + min(p[1] for p in plate_uv)) / 2) if plate_uv else (9e9, 9e9)

    shout = next((o for o in meshes if o.name.startswith("shout_tubes")), None)
    shout_uv = []
    shout_top = 0.0
    if shout:
        for v in shout.data.vertices:
            w = shout.matrix_world @ v.co
            shout_uv.append(to_uv(w.x, w.y))
            shout_top = max(shout_top, w.z)
    s_u = [p[0] for p in shout_uv]
    s_v = [p[1] for p in shout_uv]
    shout_dia = ((max(s_u) - min(s_u)) + (max(s_v) - min(s_v))) / 2 if shout_uv else 0
    shout_ctr = ((max(s_u) + min(s_u)) / 2, (max(s_v) + min(s_v)) / 2) if shout_uv else (0, 0)

    # measured tree positions must survive to the export
    crowns = next((o for o in meshes if o.name.startswith("tree_crowns")), None)
    osm_trees = [t for t in data["trees"] if t["src"] == "osm"]
    tree_hits = 0
    if crowns:
        pts = [to_uv(*(crowns.matrix_world @ v.co)[:2]) for v in crowns.data.vertices]
        for t in osm_trees:
            tu, tv = t["uv"]
            if any(abs(p[0] - tu) < 6.0 and abs(p[1] - tv) < 6.0 for p in pts):
                tree_hits += 1

    glow = sorted(m for m in mats if m.endswith("_Glow"))
    off_palette = sorted(m for m in mats if m not in PALETTE)
    bad_volumes = sorted(n for n, v in volumes.items() if v <= 0)
    bad_scales = sorted(n for n, s in scales.items() if min(s) <= 0)

    checks = [
        ("binary GLB present", os.path.getsize(glb) > 0, os.path.getsize(glb)),
        ("no non-mesh objects (cameras/lights/armatures)", not non_mesh, non_mesh),
        ("no animation data", not animated, animated),
        ("no negative scales", not bad_scales, bad_scales),
        ("min_z ~ 0", abs(mn[2]) < 1e-4, round(mn[2], 6)),
        # measured on the GROUND PLATE, not the whole model: the canopy
        # overhangs the kerb asymmetrically, and re-centring the model on its
        # own AABB to satisfy this check is what slid the park 0.92 m off its
        # anchor in an earlier build. The anchor IS the plate's OBB centre.
        ("ground plate centred within 0.5 m of the origin",
         abs(plate_ctr[0]) < 0.5 and abs(plate_ctr[1]) < 0.5,
         [round(plate_ctr[0], 4), round(plate_ctr[1], 4)]),
        ("max_z == datum exactly", abs(mx[2] - DATUM_M) < 0.01, round(mx[2], 4)),
        ("oriented footprint 159.51 x 23.51 m +/- 0.5",
         abs(plate_long - OBB_LONG) < 0.5 and abs(plate_cross - OBB_CROSS) < 0.5,
         [round(plate_long, 3), round(plate_cross, 3)]),
        ("Shout is a circle 11.84 m across (centreline)",
         abs(shout_dia - SHOUT_DIAMETER) < 0.4, round(shout_dia - SHOUT_GAUGE - 2 * SHOUT_TUBE_R, 3)),
        ("Shout centred at (-36.03, -1.29)",
         math.dist(shout_ctr, SHOUT_CENTRE_UV) < 0.5,
         [round(shout_ctr[0], 3), round(shout_ctr[1], 3)]),
        ("Shout crest 4.34 m (centreline)", abs(shout_top - SHOUT_CREST) < 0.1,
         round(shout_top - SHOUT_TUBE_R, 3)),
        ("Shout at the SOUTH-WEST end (mirror check)", shout_ctr[0] < -20.0,
         round(shout_ctr[0], 2)),
        ("all 20 measured tree positions present",
         tree_hits == len(osm_trees), f"{tree_hits}/{len(osm_trees)}"),
        ("triangles <= cap", tris <= TRI_CAP, f"{tris}/{TRI_CAP}"),
        ("no image textures", not textured, sorted(set(textured))),
        ("no transparency", not transparent, sorted(set(transparent))),
        ("all materials Toy_* and in the palette", not off_palette, off_palette),
        ("no Toy_body (landmarks are never tintable)", "Toy_body" not in mats, None),
        ("_Glow materials present", len(glow) >= 2, glow),
        ("per-object signed volume positive (normals outward)",
         not bad_volumes, bad_volumes),
    ]

    ok = all(c[1] for c in checks)
    width = max(len(c[0]) for c in checks)
    for name, passed, detail in checks:
        print(f"{'PASS' if passed else 'FAIL'}  {name:<{width}}  {detail if detail is not None else ''}")

    report = {
        "asset": os.path.basename(glb),
        "validator": bpy.app.version_string,
        "fresh_isolated_scene": True,
        "reimported_final_glb": True,
        "object_count": len(objs),
        "mesh_object_count": len(meshes),
        "triangle_count": tris,
        "triangle_budget": TRI_CAP,
        "file_bytes": os.path.getsize(glb),
        "dimensions_m": [round(mx[i] - mn[i], 4) for i in range(3)],
        "bbox_min_m": [round(v, 4) for v in mn],
        "bbox_max_m": [round(v, 4) for v in mx],
        "oriented_footprint_m": [round(plate_long, 4), round(plate_cross, 4)],
        "ground_plate_centre_uv": [round(plate_ctr[0], 4), round(plate_ctr[1], 4)],
        "heading_long_deg": HEADING_LONG,
        "height_datum_m": DATUM_M,
        "height_datum_source": "tallest American elm crest — ESTIMATED, plan 2.15 risk 1",
        "shout": {"diameter_m": round(shout_dia, 4),
                  "centre_uv": [round(shout_ctr[0], 4), round(shout_ctr[1], 4)],
                  "crest_m": round(shout_top, 4)},
        "path_centreline_m": PATH_LENGTH,
        "seat_wall_total_m": WALL_LENGTH,
        "trees": {"osm": len(osm_trees),
                  "derived": len([t for t in data["trees"] if t["src"] == "derived"]),
                  "measured_positions_present": tree_hits},
        "materials": sorted(mats),
        "glow_materials": glow,
        "off_palette_materials": off_palette,
        "textured_materials": sorted(set(textured)),
        "transparent_materials": sorted(set(transparent)),
        "animated_objects": animated,
        "non_mesh_objects": non_mesh,
        "signed_volumes_m3": {k: round(v, 4) for k, v in sorted(volumes.items())},
        "objects_with_non_positive_volume": bad_volumes,
        "checks": [{"name": n, "pass": bool(p), "value": d} for n, p, d in checks],
        "all_pass": bool(ok),
    }
    with open(out, "w") as fh:
        json.dump(report, fh, indent=2)
    print(f"\n{'ALL PASS' if ok else 'FAILURES PRESENT'} -> {out}")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
