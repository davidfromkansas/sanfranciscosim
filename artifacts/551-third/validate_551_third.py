"""Contract validation for 551-third.glb.

Validates the RE-IMPORT of the exported file in a fresh, empty scene — never the
authoring scene — per .agents/skills/sf-asset-check/SKILL.md.

    blender -b --python validate_551_third.py -- --glb 551-third.glb --out validation.json
"""

import argparse
import json
import math
import sys

import bmesh
import bpy
import mathutils

TRI_CAP = 12000
TARGET_HEIGHT = 6.6
PALETTE = {
    "Toy_cream": "f2ede3",
    "Toy_trim": "f3efe6",
    "Toy_teal": "3fa8a0",
    "Toy_mustard": "d9a441",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_ink": "3a3530",
    "Toy_roofd": "45454a",
    "Toy_stone": "d9d2c2",
    "Toy_red": "c4453c",
    "Toy_steel": "9aa0a6",
    "Toy_white": "f7f4ec",
}
EXPECTED_GLOW = {"Toy_trim_Glow", "Toy_mustard_Glow", "Toy_glassl_Glow"}
RAY_DIRS = 26  # deterministic lattice of directions for the visibility test


def signed_volume(obj, dg):
    ev = obj.evaluated_get(dg)
    me = ev.to_mesh()
    me.calc_loop_triangles()
    total = 0.0
    M = obj.matrix_world
    for t in me.loop_triangles:
        a, b, c = (M @ me.vertices[i].co for i in t.vertices)
        total += a.dot(b.cross(c)) / 6.0
    ev.to_mesh_clear()
    return total


def ray_residual(objs, dg, mn, mx):
    """Deterministic outward-normal check.

    Fire rays from far outside along a fixed direction lattice; every first hit
    should present a face whose normal opposes the ray. The residual is the
    share of first hits that do not.
    """
    dirs = []
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            for k in (-1, 0, 1):
                if i or j or k:
                    dirs.append(mathutils.Vector((i, j, k)).normalized())
    assert len(dirs) == RAY_DIRS
    centre = mathutils.Vector(((mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, (mn[2] + mx[2]) / 2))
    radius = max(mx[i] - mn[i] for i in range(3)) * 1.5
    hits = 0
    bad = 0
    cast = 0
    depsgraph = dg
    # Fan offsets are scaled to the model's own half-extent, not to the cast
    # radius: this asset is a wide flat plate, and a fan sized to the cast
    # distance sprays most rays past it entirely.
    half = max(mx[i] - mn[i] for i in range(3)) / 2
    steps = [-0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9]
    for d in dirs:
        for du in steps:
            for dv in steps:
                up = mathutils.Vector((0, 0, 1))
                if abs(d.dot(up)) > 0.9:
                    up = mathutils.Vector((1, 0, 0))
                e1 = d.cross(up).normalized()
                e2 = d.cross(e1).normalized()
                origin = centre + d * radius + e1 * (du * half) + e2 * (dv * half)
                ok, loc, nrm, idx, obj, mat = bpy.context.scene.ray_cast(
                    depsgraph, origin, -d
                )
                cast += 1
                if not ok:
                    continue
                hits += 1
                if nrm.dot(-d) > 0:  # normal points along the ray => facing away
                    bad += 1
    return hits, bad, (bad / hits * 100.0 if hits else 0.0), cast


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb", default="551-third.glb")
    ap.add_argument("--out", default="validation.json")
    args = ap.parse_args(argv)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=args.glb)
    objs = [o for o in set(bpy.data.objects) - before]
    meshes = [o for o in objs if o.type == "MESH"]
    dg = bpy.context.evaluated_depsgraph_get()

    mn = [1e9] * 3
    mx = [-1e9] * 3
    tris = 0
    mats = set()
    textured = []
    animated = []
    negscale = []
    unapplied = []
    inverted = []
    for o in objs:
        if o.animation_data:
            animated.append(o.name)
        if o.type != "MESH":
            continue
        s = o.matrix_world.to_scale()
        if min(s) < 0:
            negscale.append(o.name)
        if (
            abs(s[0] - 1) > 1e-4
            or abs(s[1] - 1) > 1e-4
            or abs(s[2] - 1) > 1e-4
            or o.matrix_world.to_euler()[:] != (0.0, 0.0, 0.0)
        ):
            unapplied.append(o.name)
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for m in me.materials:
            if not m:
                continue
            mats.add(m.name)
            if m.use_nodes and any(n.type == "TEX_IMAGE" for n in m.node_tree.nodes):
                textured.append(m.name)
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
        ev.to_mesh_clear()
        if signed_volume(o, dg) <= 0:
            inverted.append(o.name)

    hits, bad, residual, cast = ray_residual(meshes, dg, mn, mx)

    dims = [round(mx[i] - mn[i], 3) for i in range(3)]
    centre_xy = [round((mn[0] + mx[0]) / 2, 3), round((mn[1] + mx[1]) / 2, 3)]
    glow = {m for m in mats if m.endswith("_Glow")}
    non_toy = sorted(m for m in mats if not m.startswith("Toy_"))
    off_palette = sorted(
        m for m in mats if (m[:-5] if m.endswith("_Glow") else m) not in PALETTE
    )

    checks = {
        "fresh_scene_reimport": True,
        "min_z_at_zero": abs(mn[2]) <= 0.5,
        "xy_centred": max(abs(c) for c in centre_xy) <= 1.0,
        "bbox_top_is_target_height": abs(mx[2] - TARGET_HEIGHT) <= 0.005,
        "triangles_within_cap": tris <= TRI_CAP,
        "all_materials_toy": not non_toy,
        "materials_on_palette": not off_palette,
        "no_toy_body": "Toy_body" not in mats,
        "no_image_textures": not textured,
        "glow_set_as_planned": glow == EXPECTED_GLOW,
        "no_cameras": not [o for o in objs if o.type == "CAMERA"],
        "no_lights": not [o for o in objs if o.type == "LIGHT"],
        "no_animation": not animated,
        "no_armatures": not [o for o in objs if o.type == "ARMATURE"],
        "no_negative_scale": not negscale,
        "transforms_applied": not unapplied,
        "normals_signed_volume": not inverted,
        "normals_ray_residual": residual <= 0.15,
        "ray_coverage_meaningful": hits >= 200,
    }

    result = {
        "asset": "551-third",
        "glb": args.glb,
        "objects": len(objs),
        "meshes": len(meshes),
        "triangles": tris,
        "triangle_cap": TRI_CAP,
        "dims_m": dims,
        "bbox_min": [round(v, 4) for v in mn],
        "bbox_max": [round(v, 4) for v in mx],
        "min_z": round(mn[2], 4),
        "center_xy": centre_xy,
        "target_height_m": TARGET_HEIGHT,
        "materials": sorted(mats),
        "glow_materials": sorted(glow),
        "non_toy_materials": non_toy,
        "off_palette_materials": off_palette,
        "textured_materials": sorted(set(textured)),
        "animated_objects": animated,
        "negative_scale_objects": negscale,
        "unapplied_transform_objects": unapplied,
        "inverted_volume_objects": inverted,
        "ray_test": {
            "directions": RAY_DIRS,
            "rays_cast": cast,
            "hits": hits,
            "back_facing_first_hits": bad,
            "residual_pct": round(residual, 4),
            "threshold_pct": 0.15,
        },
        "checks": checks,
        "result": "PASS" if all(checks.values()) else "FAIL",
        "failed_checks": [k for k, v in checks.items() if not v],
    }
    with open(args.out, "w") as f:
        json.dump(result, f, indent=2)
    print("VALIDATION " + json.dumps({"result": result["result"], "failed": result["failed_checks"], "tris": tris, "dims": dims}))


if __name__ == "__main__":
    main()
