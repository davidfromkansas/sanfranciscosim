"""Fresh-scene contract validation for one-market-plaza-towers.glb.

    blender -b --python validate_one_market_plaza_towers.py -- [--glb FILE] [--out FILE]

Factory-resets, imports only the final GLB, and writes the complete
machine-readable report. It does not inspect the source .blend.

Normals are checked two ways, because this asset is a union of ~330 closed
solids rather than one shell:
  * per-object signed volume — authoritative here. Every object is a closed
    solid, so a correctly oriented one has positive signed volume.
  * a deterministic visibility-ray test from interior targets — informative,
    but a union of solids legitimately shows a small residual where one solid's
    outward face is buried inside another, so the gate is <= 0.15%.
"""

import json
import math
import os
import sys

import bpy
from mathutils import Vector

# The manifest target height: the Spear Tower's rooftop plant cap, which must be the
# export bounding-box top so the loader's targetHeightM / measuredHeight is 1.0.
TARGET_HEIGHT_M = 177.6

TRI_BUDGET = 26000
RAY_RESIDUAL_MAX = 0.0015  # 0.15% for a union of solids


def rounded(v):
    return [round(x, 4) for x in v]


def signed_volume(mesh, matrix):
    total = 0.0
    mesh.calc_loop_triangles()
    for tri in mesh.loop_triangles:
        a, b, c = (matrix @ mesh.vertices[i].co for i in tri.vertices)
        total += a.dot(b.cross(c)) / 6.0
    return total


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "one-market-plaza-towers.glb"))
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
    inverted_objects = []

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
            inverted_objects.append(obj.name)

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
    # inward toward nine interior targets; the first face each ray meets should
    # oppose the ray direction.
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

    ray_residual = (ray_flipped / ray_hits) if ray_hits else 1.0
    normals_ok = (
        invalid_normal_count == 0
        and not inverted_objects
        and ray_hits > 0
        and ray_residual <= RAY_RESIDUAL_MAX
    )

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
        "max_z_m": round(mx.z, 4),
        "loader_scale_factor": round(TARGET_HEIGHT_M / dims.z, 6),
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
        "inverted_signed_volume_objects": inverted_objects,
        "normal_ray_cast_first_hits": ray_hits,
        "normal_ray_cast_flipped_visible_faces": ray_flipped,
        "normal_ray_cast_residual": round(ray_residual, 6),
        "normal_ray_cast_residual_gate": RAY_RESIDUAL_MAX,
        "normal_orientation_status": "PASS" if normals_ok else "FAIL",
        "normal_orientation_method": (
            "All source meshes run bmesh.ops.recalc_face_normals before export. "
            "Per-object signed volume is authoritative for this union of closed "
            "solids and must be positive for every object; 31,500 deterministic "
            "visibility rays from nine interior targets must leave a residual of "
            "at most 0.15%, which is the share of first hits that legitimately "
            "land on a face buried inside a neighbouring solid."
        ),
        "unexpected_geometry_or_objects": unexpected,
        "material_contract_violations": sorted(off_contract),
        "glow_materials": sorted(m["name"] for m in mat_rows if m["glow"]),
        "anchor_lonlat": [-122.3941803, 37.7933169],
        "long_axis_heading_deg_true": 135.2,
        "front_normal_heading_deg_true": 135.2,
        "object_details": sorted(object_rows, key=lambda x: x["name"]),
    }
    results["checks"] = {
        # 1 Market: crest 48.70 m; the XY box is ~112 m because the footprint
        # is a 45-deg-rotated U 85.2 x 66.2 m at the wall plane and the cornice
        # projects 1.85 m beyond it. Ranges adapted from the 300-brannan copy.
        # One Market Plaza towers: Spear's plant crest 177.60 m; the XY box is
        # ~123 x 129 m, the 45-deg envelope of the lot-007 footprint plus the
        # pier projection. Adapted from the 1-market copy.
        "meters_and_plausible_dimensions": (
            177.5 <= dims.z <= 177.7 and 118.0 <= dims.x <= 128.0
            and 124.0 <= dims.y <= 134.0
        ),
        "base_at_z_zero": abs(mn.z) <= 0.5,
        "crest_is_target_height": abs(mx.z - TARGET_HEIGHT_M) <= 0.01,
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
        "normals_outward": normals_ok,
        "no_degenerate_geometry": degenerate == 0,
        "no_unexpected_objects": not unexpected,
    }
    results["overall"] = "PASS" if all(results["checks"].values()) else "FAIL"

    with open(output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        f.write("\n")
    print(
        json.dumps(
            {
                k: results[k]
                for k in (
                    "overall",
                    "checks",
                    "triangle_count",
                    "dimensions_m",
                    "min_z_m",
                    "max_z_m",
                    "loader_scale_factor",
                    "xy_center_offset_m",
                    "materials",
                    "object_count",
                    "inverted_signed_volume_objects",
                    "normal_ray_cast_residual",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
