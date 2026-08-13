"""Fresh-scene contract validation for 542-presidio-blvd.glb.

    blender -b --python validate_542_presidio_blvd.py -- [--glb FILE] [--out FILE]

This script factory-resets, imports only the final GLB, and writes the complete
machine-readable report. It does not inspect the source .blend.

Normals: this asset is a union of closed convex solids, so the authoritative
test is per-object signed volume - every solid must enclose a positive volume,
which is true if and only if its faces point outward. A deterministic
visibility ray cast runs as a secondary check; interpenetrating solids (the
tile courses straddle the roof plane by design) make a small residual legal
there, so it is held to the pipeline's 0.15% ceiling rather than to zero.
"""

import json
import math
import os
import sys

import bpy
from mathutils import Vector

TRI_BUDGET = 8000
H_CREST = 10.6
RAY_RESIDUAL_CEILING = 0.0015  # 0.15%, per the stage-2 normals gate


def rounded(v):
    return [round(x, 4) for x in v]


def signed_volume(me, matrix):
    """Six times the signed volume of a closed mesh, via the divergence theorem."""
    total = 0.0
    me.calc_loop_triangles()
    for tri in me.loop_triangles:
        a, b, c = (matrix @ me.vertices[i].co for i in tri.vertices)
        total += a.dot(b.cross(c))
    return total / 6.0


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "542-presidio-blvd.glb"))
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
    inverted_solids = []

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

        vol = signed_volume(me, obj.matrix_world)
        if vol <= 0.0:
            inverted_solids.append(obj.name)

        object_rows.append(
            {
                "name": obj.name,
                "triangles": len(me.loop_triangles),
                "signed_volume_m3": round(vol, 5),
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
        if mat.surface_render_method != "DITHERED" and alpha < 0.999:
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

    # Secondary, deterministic visibility test: fire a Fibonacci sphere of rays
    # inward at nine targets and check the first face each one meets opposes it.
    ray_hits = 0
    ray_flipped = 0
    golden = math.pi * (3.0 - math.sqrt(5.0))
    targets = [
        Vector((center.x + dx * dims.x, center.y + dy * dims.y, mn.z + fz * dims.z))
        for dx, dy in ((0.0, 0.0), (-0.18, -0.18), (0.18, 0.18))
        for fz in (0.18, 0.52, 0.86)
    ]
    for target in targets:
        for i in range(2500):
            y = 1.0 - 2.0 * (i + 0.5) / 2500
            r = math.sqrt(max(0.0, 1.0 - y * y))
            a = golden * i
            outward = Vector((math.cos(a) * r, math.sin(a) * r, y))
            direction = -outward
            hit, _, normal, _, _, _ = bpy.context.scene.ray_cast(
                dg, target + outward * 1000.0, direction, distance=1400.0
            )
            if hit:
                ray_hits += 1
                if normal.dot(direction) > 1e-5:
                    ray_flipped += 1

    ray_residual = (ray_flipped / ray_hits) if ray_hits else 1.0
    normals_ok = (
        invalid_normal_count == 0
        and not inverted_solids
        and ray_hits > 0
        and ray_residual <= RAY_RESIDUAL_CEILING
    )

    glow_mats = sorted(m.name for m in bpy.data.materials if m.name.endswith("_Glow"))

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
        "crest_height_m": round(dims.z, 4),
        "loader_scale_at_target_height": round(H_CREST / dims.z, 5),
        "materials": sorted(mat.name for mat in bpy.data.materials),
        "material_details": sorted(mat_rows, key=lambda x: x["name"]),
        "glow_materials": glow_mats,
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
        "inverted_solids": inverted_solids,
        "normal_ray_cast_first_hits": ray_hits,
        "normal_ray_cast_flipped_visible_faces": ray_flipped,
        "normal_ray_cast_residual": round(ray_residual, 6),
        "normal_ray_cast_residual_ceiling": RAY_RESIDUAL_CEILING,
        "normal_orientation_status": "PASS" if normals_ok else "FAIL",
        "normal_orientation_method": (
            "Authoritative: per-object signed volume must be positive for every "
            "closed solid in the union. Secondary: 22,500 deterministic "
            "visibility rays; the tile courses straddle the roof plane by "
            "design, so a residual up to 0.15% is allowed there."
        ),
        "unexpected_geometry_or_objects": unexpected,
        "material_contract_violations": sorted(off_contract),
        "object_details": sorted(object_rows, key=lambda x: x["name"]),
    }
    results["checks"] = {
        "meters_and_plausible_dimensions": (
            10.0 <= dims.z <= 11.5 and 18.0 <= dims.x <= 30.0 and 18.0 <= dims.y <= 30.0
        ),
        "base_at_z_zero": abs(mn.z) <= 0.5,
        "centered_xy": abs(center.x) <= 1.0 and abs(center.y) <= 1.0,
        "crest_normalised_to_target": abs(dims.z - H_CREST) <= 0.02,
        "under_triangle_budget": tris <= TRI_BUDGET,
        "no_image_textures": not bpy.data.images and not textured,
        "no_transparency": not transparent,
        "materials_follow_contract": not off_contract,
        "glow_present_and_restrained": 1 <= len(glow_mats) <= 2,
        "no_cameras_or_lights": not bpy.data.cameras and not bpy.data.lights,
        "no_animation_skin_or_constraints": (
            animations == 0
            and results["armature_count"] == 0
            and results["constraint_count"] == 0
        ),
        "transforms_applied": scales_applied,
        "no_negative_scales": not negative_scale,
        "normals_outward": normals_ok,
        "no_degenerate_geometry": degenerate == 0,
        "no_unexpected_objects": not unexpected,
    }
    results["overall"] = "PASS" if all(results["checks"].values()) else "FAIL"

    with open(output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        f.write("\n")
    print(json.dumps(results["checks"], indent=2))
    print("overall:", results["overall"])


if __name__ == "__main__":
    main()
