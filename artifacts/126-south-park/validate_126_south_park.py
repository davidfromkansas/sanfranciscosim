"""Fresh-scene contract validation for 126-south-park.glb.

    blender -b --python validate_135_south_park.py -- [--glb FILE] [--out FILE]

This script factory-resets, imports only the final GLB, and writes the complete
machine-readable report. It does not inspect the source .blend.
"""

import json
import math
import os
import sys

import bpy
from mathutils import Vector

TRI_BUDGET = 7000


def rounded(v):
    return [round(x, 4) for x in v]


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "126-south-park.glb"))
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

    # --- plan-shape measurement: the waist and the three light wells ---------
    # The identity feature of this building is that its 6.99 m width pinches to
    # 4.01 m where two light wells cut in from opposite sides. Measure it on the
    # structural shell only ("body"): the applied linings and window panels sit
    # deliberately proud of it and would report a false, narrower waist.
    #
    # Sectioned by RAY CAST, not by binning vertices. The shell is a prism with
    # vertices only at its 16 footprint corners, so a vertex histogram samples
    # almost none of its length and reports whatever two corners happen to share
    # a bin. Firing a ray across the building at each depth measures the plan
    # where there is no vertex at all, which is most of it.
    #
    # Check the axis pairing, not just the angle: at +45 deg it is
    # (x*cos - y*sin) that carries the 29.79 m DEPTH and (x*sin + y*cos) the
    # 6.99 m width.
    ang = math.radians(45.0)
    ca, sa = math.cos(ang), math.sin(ang)
    shell = [o for o in meshes if o.name.split(".")[0].startswith("body")]

    def to_local(x, y):
        return (x * ca - y * sa, x * sa + y * ca)

    def to_world(depth, across):
        return (depth * ca + across * sa, -depth * sa + across * ca)

    d_lo, d_hi = 1e9, -1e9
    for obj in shell:
        for corner in obj.bound_box:
            w = obj.matrix_world @ Vector(corner)
            d, _ = to_local(w.x, w.y)
            d_lo, d_hi = min(d_lo, d), max(d_hi, d)

    REACH = 40.0
    profile = []
    step = 0.25
    n_steps = int((d_hi - d_lo - 1.0) / step)
    for i in range(n_steps + 1):
        d = d_lo + 0.5 + i * step
        lo = hi = None
        for sign in (1, -1):
            ox, oy = to_world(d, sign * REACH)
            dx, dy = to_world(0.0, -sign * 1.0)
            best = None
            for obj in shell:
                ok, loc, _n, _idx = obj.ray_cast(
                    Vector((ox, oy, 1.0)), Vector((dx, dy, 0.0)), distance=2 * REACH
                )
                if ok:
                    _, a = to_local(loc.x, loc.y)
                    if best is None or (sign * a) > (sign * best):
                        best = a
            if sign == 1:
                hi = best
            else:
                lo = best
        if lo is not None and hi is not None and hi - lo > 0.5:
            profile.append((d, hi - lo, lo, hi))

    waist = min((w for _, w, _, _ in profile), default=None)
    lo_ref = min((lo for _, _, lo, _ in profile), default=0.0)
    hi_ref = max((hi for _, _, _, hi in profile), default=0.0)

    def runs(flags):
        """Number of contiguous notched stretches along the depth."""
        count, prev = 0, False
        for f in flags:
            if f and not prev:
                count += 1
            prev = f
        return count

    # The two flanks are counted separately on purpose: the north-east well and
    # the first south-west well overlap for 1.99 m, so counting notched slices
    # without regard to side merges them and reports two wells instead of three.
    sw_runs = runs([lo > lo_ref + 0.4 for _, _, lo, _ in profile])
    ne_runs = runs([hi < hi_ref - 0.4 for _, _, _, hi in profile])
    well_count = sw_runs + ne_runs

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
        "anchor_lonlat": [-122.3945863, 37.7816006],
        "front_heading_deg_true": 135.3,
        "target_height_m": 7.6,
        "waist_min_width_m": round(waist, 3) if waist is not None else None,
        "waist_expected_m": 4.01,
        "light_well_notch_count": well_count,
        "light_well_notches_sw_flank": sw_runs,
        "light_well_notches_ne_flank": ne_runs,
        "plan_width_profile_method": (
            "The structural shell is sectioned by ray cast at z = 1.0 m every 0.25 m "
            "along its 29.79 m depth, firing inward from both flanks to find the wall "
            "faces; the narrowest section is the waist. Ray casting rather than vertex "
            "binning because the shell is a 16-corner prism with no vertices along its "
            "long walls. A slice whose low edge is "
            "inset more than 0.4 m counts as notched on the south-west flank and "
            "likewise for the north-east, and contiguous runs per flank are the light "
            "wells — counted per flank because the north-east well and the first "
            "south-west well overlap for 1.99 m and would otherwise merge into one. "
            "This is the check that distinguishes this asset from a plain box or a "
            "90-deg-rotated model, because its 45 deg heading makes the axis-aligned "
            "bounding box near-square."
        ),
        "signed_volume_outward_objects": volume_ok,
        "signed_volume_inverted_objects": sorted(volume_bad),
        "object_details": sorted(object_rows, key=lambda x: x["name"]),
    }
    results["checks"] = {
        # Plausibility window for THIS asset. A 6.90 x 29.79 m sliver at a ~45
        # deg heading has a near-SQUARE axis-aligned bbox of ~26.7 x 26.6 m,
        # which means the bbox alone cannot tell this model from one rotated 90
        # deg — so the waist measurement below, not this window, is what pins
        # the orientation and the plan shape.
        "meters_and_plausible_dimensions": 7.4 <= dims.z <= 7.8
        and 26.0 <= dims.x <= 27.6
        and 25.9 <= dims.y <= 27.4,
        "waist_pinches_to_4m": waist is not None and abs(waist - 4.01) <= 0.15,
        "three_light_wells_present": sw_runs == 2 and ne_runs == 1,
        "crest_normalized_to_target": abs(mx.z - 7.6) <= 0.02,
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
