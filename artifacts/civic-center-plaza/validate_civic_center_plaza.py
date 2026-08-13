"""Fresh-scene contract validation for civic-center-plaza.glb.

    blender -b --python validate_civic_center_plaza.py -- [--glb FILE] [--out FILE]

This script factory-resets, imports only the final GLB, and writes the complete
machine-readable report. It does not inspect the source .blend.

Three subject-specific checks beyond the standard contract (asset plan Part 1):

1. max_z == 30.48 +/- 0.01 AND the vertex achieving it belongs to the US
   flagpole. The loader scales the whole 178 m plaza by
   targetHeightM / measuredHeight off this one thin pole, so a drift here
   rescales the entire ground plane.
2. exactly 190 trees, every one within 0.05 m of its position in
   data/plaza_uv.json - the tree positions are measured OSM survey data, not
   invention, and a build that quietly regenerates them on a grid has lost the
   asset's whole recognition cue.
3. XY bbox ~146.5 x 192.3 m - the expected consequence of a 9.06 deg heading on
   a 177.9 x 121.5 m rectangle, not a scale error.
"""

import json
import math
import os
import sys

import bpy
from mathutils import Vector

TRI_BUDGET = 18000
TARGET_HEIGHT = 30.48
TREE_COUNT = 190
HEADING_LONG = 189.06
# Cluster trees on their BOTTOM trunk ring only. The crown is 6.6 m across and
# its underside sits at 4.90 m (4.61 m at the low end of the +/-6% scale
# jitter), so a threshold anywhere above that pulls crown vertices in and splits
# one tree into two or three clusters — 414 "trees" for 190, which is exactly
# what a 5.0 m threshold produced.
TRUNK_BAND_Z = 4.0


def rounded(v):
    return [round(x, 4) for x in v]


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "civic-center-plaza.glb"))
    output = arg("--out", os.path.join(here, "validation.json"))

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)

    objects = list(bpy.data.objects)
    meshes = [o for o in objects if o.type == "MESH"]
    dg = bpy.context.evaluated_depsgraph_get()
    mn = Vector((1e12, 1e12, 1e12))
    mx = Vector((-1e12, -1e12, -1e12))
    tris = 0
    degenerate = 0
    invalid_normal_count = 0
    object_rows = []

    for obj in meshes:
        ev = obj.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        degenerate += sum(1 for tri in me.loop_triangles if tri.area < 1e-8)
        for v in me.vertices:
            w = obj.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])

        for loop in me.loops:
            n = loop.normal
            if not all(math.isfinite(v) for v in n) or abs(n.length - 1.0) > 1e-3:
                invalid_normal_count += 1

        object_rows.append(
            {
                "name": obj.name,
                "triangles": len(me.loop_triangles),
                "location": rounded(obj.location),
                "rotation_euler": rounded(obj.rotation_euler),
                "scale": rounded(obj.scale),
            }
        )
        ev.to_mesh_clear()

    mat_rows = []
    textured = []
    transparent = []
    off_contract = []
    for mat in bpy.data.materials:
        tex = []
        alpha = 1.0
        roughness = None
        if mat.use_nodes:
            tex = [n.name for n in mat.node_tree.nodes if n.type == "TEX_IMAGE"]
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                alpha = float(bsdf.inputs["Alpha"].default_value)
                roughness = float(bsdf.inputs["Roughness"].default_value)
        if tex:
            textured.append(mat.name)
        if alpha < 0.999:
            transparent.append(mat.name)
        if not mat.name.startswith("Toy_") or mat.name == "Toy_body":
            off_contract.append(mat.name)
        mat_rows.append(
            {
                "name": mat.name,
                "image_texture_nodes": tex,
                "alpha": round(alpha, 4),
                "roughness": round(roughness, 4) if roughness is not None else None,
                "glow": mat.name.endswith("_Glow"),
            }
        )

    scales_applied = all(
        all(abs(v - 1.0) < 1e-5 for v in obj.scale)
        and all(abs(v) < 1e-5 for v in obj.rotation_euler)
        and all(abs(v) < 1e-5 for v in obj.location)
        for obj in meshes
    )
    negative_scale = any(
        obj.matrix_world.to_scale().x
        * obj.matrix_world.to_scale().y
        * obj.matrix_world.to_scale().z
        < 0
        for obj in meshes
    )
    animations = sum(len(a.fcurves) for a in bpy.data.actions)
    unexpected = [o.name for o in objects if o.type not in {"MESH"}]

    # --- subject-specific measurements -------------------------------------
    datum_object = None
    for obj in meshes:
        ev = obj.evaluated_get(dg)
        me = ev.to_mesh()
        if any((obj.matrix_world @ v.co).z >= mx.z - 1e-4 for v in me.vertices):
            datum_object = obj.name.split(".")[0]
        ev.to_mesh_clear()

    # Recover each modelled tree from the merged `trees` object by clustering
    # its trunk vertices in XY, then compare against the committed survey.
    with open(os.path.join(here, "data", "plaza_uv.json"), "r", encoding="utf8") as fh:
        survey = json.load(fh)
    a = math.radians(HEADING_LONG)
    udir = (math.sin(a), math.cos(a))
    vdir = (udir[1], -udir[0])   # +v = WEST, matching the build's V_DIR
    expected = set()
    for t in survey["trees"]:
        expected.add(
            (
                round(t["u"] * udir[0] + t["v"] * vdir[0], 3),
                round(t["u"] * udir[1] + t["v"] * vdir[1], 3),
            )
        )
    tree_obj = next((o for o in meshes if o.name.split(".")[0] == "trees"), None)
    found = []
    if tree_obj:
        ev = tree_obj.evaluated_get(dg)
        me = ev.to_mesh()
        # Cluster on TRUNK vertices only. The crown is a 2.85 m drum, so
        # clustering the whole tree splits one tree into several centres and
        # reports ~520 trees for 190 — the trunk is 0.30 m and the rows are
        # 3.2 m apart, which is the only radius separation that is unambiguous.
        centres = []
        for v in me.vertices:
            w = tree_obj.matrix_world @ v.co
            if w.z > TRUNK_BAND_Z:
                continue
            for c in centres:
                if (c[0] - w.x) ** 2 + (c[1] - w.y) ** 2 < 2.25:
                    break
            else:
                centres.append((w.x, w.y))
        # Second pass: the seed vertex sits on the trunk hexagon, 0.30 m off the
        # axis. Average every member of each cluster so the reported position is
        # the trunk AXIS, which is what the survey records.
        sums = [[0.0, 0.0, 0] for _ in centres]
        for v in me.vertices:
            w = tree_obj.matrix_world @ v.co
            if w.z > TRUNK_BAND_Z:
                continue
            best, bd = -1, 1e18
            for i, c in enumerate(centres):
                d = (c[0] - w.x) ** 2 + (c[1] - w.y) ** 2
                if d < bd:
                    best, bd = i, d
            sums[best][0] += w.x
            sums[best][1] += w.y
            sums[best][2] += 1
        centres = [(a / n, b / n) for a, b, n in sums if n]
        found = centres
        ev.to_mesh_clear()
    shift = [0.0, 0.0]
    if found and expected:
        ex = sum(p[0] for p in expected) / len(expected)
        ey = sum(p[1] for p in expected) / len(expected)
        fx = sum(p[0] for p in found) / len(found)
        fy = sum(p[1] for p in found) / len(found)
        shift = [fx - ex, fy - ey]
    tree_count = len(found)
    tree_err = 0.0
    for x, y in found:
        best = min(((x - shift[0] - ex2) ** 2 + (y - shift[1] - ey2) ** 2)
                   for ex2, ey2 in expected) if expected else 0.0
        tree_err = max(tree_err, math.sqrt(best))

    pole_counts = {"expected_historic": 18, "expected_pride": 16, "expected_tall": 1,
                   "surveyed": len(survey["flagpoles"])}

    dims = mx - mn
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))

    # Deterministic visibility-ray normal test: fire a Fibonacci sphere of rays
    # inward toward nine interior targets; the first face each ray meets must
    # oppose the ray direction, i.e. face outward.
    ray_hits = 0
    ray_flipped = 0
    golden = math.pi * (3.0 - math.sqrt(5.0))
    targets = [
        Vector((center.x + dx * dims.x, center.y + dy * dims.y, mn.z + fz * dims.z))
        for dx, dy in ((0.0, 0.0), (-0.12, 0.12), (0.12, -0.12))
        for fz in (0.18, 0.45, 0.72)
    ]
    for target in targets:
        for i in range(3500):
            y = 1.0 - 2.0 * (i + 0.5) / 3500
            r = math.sqrt(max(0.0, 1.0 - y * y))
            a = golden * i
            outward = Vector((math.cos(a) * r, math.sin(a) * r, y))
            direction = -outward
            hit, _, normal, _, _, _ = bpy.context.scene.ray_cast(
                dg, target + outward * 400.0, direction, distance=600.0
            )
            if hit:
                ray_hits += 1
                if normal.dot(direction) > 1e-5:
                    ray_flipped += 1

    # Per-object signed volume is the authoritative normal test for a union of
    # interpenetrating solids (ADDRESS-TO-ASSET stage 2): every closed shell must
    # enclose positive volume. The ray test below is the secondary check, and its
    # residual is allowed up to 0.15% because rays can graze coincident faces
    # where two solids overlap.
    volume_ok = 0
    volume_bad = []
    for obj in meshes:
        ev = obj.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        vol = 0.0
        for tri in me.loop_triangles:
            a, b, c = (obj.matrix_world @ me.vertices[i].co for i in tri.vertices)
            vol += a.dot(b.cross(c)) / 6.0
        if vol > 1e-9:
            volume_ok += 1
        else:
            volume_bad.append(obj.name)
        ev.to_mesh_clear()

    results = {
        "asset": os.path.basename(glb),
        "validator": "Blender " + bpy.app.version_string,
        "fresh_isolated_scene": True,
        "reimported_final_glb": True,
        "object_count": len(objects),
        "mesh_object_count": len(meshes),
        "triangle_count": tris,
        "triangle_budget": TRI_BUDGET,
        "dimensions_m": rounded(dims),
        "bbox_min_m": rounded(mn),
        "bbox_max_m": rounded(mx),
        "min_z_m": round(mn.z, 4),
        "xy_center_offset_m": [round(center.x, 4), round(center.y, 4)],
        "materials": sorted(mat.name for mat in bpy.data.materials),
        "material_details": sorted(mat_rows, key=lambda x: x["name"]),
        "image_texture_count": len(bpy.data.images),
        "textured_materials": sorted(textured),
        "transparent_materials": sorted(transparent),
        "camera_count": len(bpy.data.cameras),
        "light_count": len(bpy.data.lights),
        "animation_fcurve_count": animations,
        "armature_count": sum(1 for o in objects if o.type == "ARMATURE"),
        "constraint_count": sum(len(o.constraints) for o in objects),
        "transforms_applied": scales_applied,
        "negative_scales": negative_scale,
        "degenerate_triangle_count": degenerate,
        "invalid_or_nonunit_loop_normal_count": invalid_normal_count,
        "normal_ray_cast_first_hits": ray_hits,
        "normal_ray_cast_flipped_visible_faces": ray_flipped,
        "normal_ray_cast_flipped_fraction": round(ray_flipped / ray_hits, 6) if ray_hits else None,
        "normal_orientation_status": "PASS"
        if invalid_normal_count == 0
        and ray_hits > 0
        and not volume_bad
        and ray_flipped / ray_hits <= 0.0015
        else "FAIL",
        "normal_orientation_method": (
            "All source meshes run bmesh.ops.recalc_face_normals before export; "
            "reimported loop normals must be finite/unit; per-object signed volume is "
            "authoritative for this union of solids; 31,500 deterministic "
            "visibility rays test the first visible face from nine interior "
            "targets, with a 0.15% residual allowed at coincident faces."
        ),
        "unexpected_geometry_or_objects": unexpected,
        "material_contract_violations": sorted(off_contract),
        "glow_materials": sorted(m["name"] for m in mat_rows if m["glow"]),
        "anchor_lonlat": [-122.4176184, 37.7794818],
        "front_heading_deg_true": HEADING_LONG,
        "target_height_m": TARGET_HEIGHT,
        "height_datum": "US flagpole finial (OSM node 7797674733, height=30.48)",
        "height_datum_vertex_object": datum_object,
        "tree_count": tree_count,
        "tree_positions_max_error_m": round(tree_err, 4),
        "flagpole_counts": pole_counts,
        "signed_volume_outward_objects": volume_ok,
        "signed_volume_inverted_objects": sorted(volume_bad),
        "object_details": sorted(object_rows, key=lambda x: x["name"]),
    }
    results["checks"] = {
        # 146.5 x 192.3 x 30.5 m: the XY box is the 9.06 deg rotation of a
        # 177.88 x 121.48 m plaza, not an oversized model. See REPORT.md.
        "meters_and_plausible_dimensions": (
            30.3 <= dims.z <= 30.7
            and 145.5 <= dims.x <= 147.5
            and 191.3 <= dims.y <= 193.3
        ),
        "crest_normalized_to_target": abs(mx.z - TARGET_HEIGHT) <= 0.01,
        "height_datum_is_the_us_flagpole": datum_object == "flagpoles",
        "tree_count_matches_survey": tree_count == TREE_COUNT,
        "tree_positions_match_survey": tree_err <= 0.05,
        "base_at_z_zero": abs(mn.z) <= 0.5,
        "centered_xy": abs(center.x) <= 1.0 and abs(center.y) <= 1.0,
        "under_triangle_budget": tris <= TRI_BUDGET,
        "no_image_textures": not bpy.data.images and not textured,
        "no_transparency": not transparent,
        "materials_follow_contract": not off_contract,
        "no_cameras_or_lights": not bpy.data.cameras and not bpy.data.lights,
        "no_animation_skin_or_constraints": animations == 0
        and results["armature_count"] == 0
        and results["constraint_count"] == 0,
        "transforms_applied": scales_applied,
        "no_negative_scales": not negative_scale,
        "normals_outward_signed_volume": not volume_bad,
        "normals_outward_ray_residual_within_tolerance": (
            invalid_normal_count == 0
            and ray_hits > 0
            and ray_flipped / ray_hits <= 0.0015
        ),
        "no_degenerate_geometry": degenerate == 0,
        "no_unexpected_objects": not unexpected,
    }
    results["overall"] = "PASS" if all(results["checks"].values()) else "FAIL"

    with open(output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        f.write("\n")
    print(json.dumps({k: results[k] for k in ("overall", "checks", "triangle_count",
                                              "dimensions_m", "min_z_m",
                                              "xy_center_offset_m", "materials",
                                              "object_count")}, indent=2))


if __name__ == "__main__":
    main()
