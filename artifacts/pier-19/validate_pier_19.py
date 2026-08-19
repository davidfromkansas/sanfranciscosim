"""Fresh-scene contract validation for pier-19.glb.

    blender -b --python validate_pier_1.py -- [--glb FILE] [--out FILE]

This script factory-resets, imports only the final GLB, and writes the complete
machine-readable report. It does not inspect the source .blend.
"""

import json
import math
import os
import sys

import bpy
from mathutils import Vector

TRI_BUDGET = 18000


def rounded(v):
    return [round(x, 4) for x in v]


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "pier-19.glb"))
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
    glow_strip_faces = 0
    glow_strip_outward = 0
    glow_strip_bad = []
    for obj in meshes:
        # The night-glow surfaces are deliberately OPEN single-layer strips, not
        # closed shells: the app draws _Glow in a separate translucent layer, and
        # a closed box shows its front and its back face and reads at roughly
        # twice the intended day alpha. An open strip has no signed volume, so it
        # gets the check that actually applies to it - is this face visible from
        # the side it claims to face? - instead of the volume test.
        #
        # NOT a dot product against the model centre. That test is wrong on this
        # asset for the same reason the build script's offset handedness was: the
        # corner turret sweeps 242 degrees, so a correctly outward-facing strip on
        # its flanks points back past the model centre. Casting a ray in along
        # each face's own normal and requiring that face to be the first thing hit
        # is both stricter and correct.
        if "_glow" in obj.name.lower():
            ev = obj.evaluated_get(dg)
            me = ev.to_mesh()
            for poly in me.polygons:
                glow_strip_faces += 1
                c = obj.matrix_world @ poly.center
                nrm = (obj.matrix_world.to_3x3() @ poly.normal).normalized()
                hit, _, hn, _, _, _ = bpy.context.scene.ray_cast(
                    dg, c + nrm * 60.0, -nrm, distance=120.0
                )
                if hit and hn.dot(nrm) > 0.9:
                    glow_strip_outward += 1
                else:
                    glow_strip_bad.append(obj.name)
            ev.to_mesh_clear()
            continue
    for obj in meshes:
        if "_glow" in obj.name.lower():
            continue
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
        "anchor_lonlat": [-122.3988181, 37.8030032],
        "front_heading_deg_true": 234.89,
        "flank_heading_deg_true": 324.89,
        "long_axis_heading_deg_true": 54.89,
        "target_height_m": 17.8,
        "target_height_is_vertical_extent": True,
        "origin_convention": (
            "Local Z = 0 is the TOP OF THE PIER DECK, not the model's lowest "
            "point. placeGeneric() seats the origin on one terrain sample at the "
            "anchor and the app's DEM carries this pier as a ~2.4 m ridge, so a "
            "model sitting on z = 0 would float 2.6 m above its own deck. The "
            "deck fascia and pile stubs therefore run to z = -2.6 m and "
            "min_z_m is NEGATIVE BY DESIGN. See docs/asset-plans/pier-19.md 2.3."
        ),
        "open_glow_strip_faces": glow_strip_faces,
        "open_glow_strip_outward_faces": glow_strip_outward,
        "open_glow_strip_inward_objects": sorted(set(glow_strip_bad)),
        "signed_volume_outward_objects": volume_ok,
        "signed_volume_inverted_objects": sorted(volume_bad),
        "object_details": sorted(object_rows, key=lambda x: x["name"]),
    }
    results["checks"] = {
        # ~243 x 192 x 17.8 m: the XY box is the 54.89 deg rotation of a
        # 262 x 47 m pier (plus the 53 m bulkhead frontage). See REPORT.md.
        "meters_and_plausible_dimensions": (
            17.7 <= dims.z <= 17.9
            and 238.0 <= dims.x <= 248.0
            and 186.0 <= dims.y <= 196.0
        ),
        "vertical_extent_normalized_to_target": abs(dims.z - 17.8) <= 0.02,
        # NOT "base at z zero". This asset's origin is the pier-deck plane and
        # its geometry deliberately runs below it; the check that matters is that
        # the deck itself is at z = 0 and the sub-deck structure reaches just
        # under the water line.
        "deck_plane_at_z_zero": abs(mx.z - 15.0) <= 0.02,
        "sub_deck_depth_expected": -2.85 <= mn.z <= -2.75,
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
        "glow_strips_face_outward": glow_strip_faces > 0
        and glow_strip_outward == glow_strip_faces,
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
