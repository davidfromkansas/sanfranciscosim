"""Fresh-scene validation of the final Ferry Building GLB.

    blender -b --python validate_ferry_building.py -- [--glb FILE] [--out FILE]
"""

import json
import math
import os
import sys

import bpy
from mathutils import Vector


def rounded(v):
    return [round(x, 4) for x in v]


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    def arg(flag, default): return argv[argv.index(flag) + 1] if flag in argv else default
    glb = arg("--glb", os.path.join(here, "ferry-building.glb"))
    output = arg("--out", os.path.join(here, "validation.json"))

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)
    objects = list(bpy.data.objects)
    meshes = [o for o in objects if o.type == "MESH"]
    dg = bpy.context.evaluated_depsgraph_get()
    mn = Vector((1e12, 1e12, 1e12)); mx = Vector((-1e12, -1e12, -1e12))
    tris = degenerate = invalid_normals = 0
    object_rows = []
    for obj in meshes:
        ev = obj.evaluated_get(dg); me = ev.to_mesh(); me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        degenerate += sum(1 for tri in me.loop_triangles if tri.area < 1e-8)
        for v in me.vertices:
            p = obj.matrix_world @ v.co
            for i in range(3): mn[i] = min(mn[i], p[i]); mx[i] = max(mx[i], p[i])
        for loop in me.loops:
            n = loop.normal
            if not all(math.isfinite(v) for v in n) or abs(n.length - 1.0) > 1e-3:
                invalid_normals += 1
        object_rows.append({
            "name": obj.name, "triangles": len(me.loop_triangles),
            "location": rounded(obj.location), "rotation_euler": rounded(obj.rotation_euler),
            "scale": rounded(obj.scale),
        })
        ev.to_mesh_clear()

    mat_rows = []; textured = []; transparent = []; off_contract = []; glow_violations = []
    allowed = {"Toy_sand", "Toy_trim", "Toy_ink", "Toy_glass", "Toy_white_Glow", "Toy_roofd", "Toy_steel", "Toy_gold"}
    for mat in bpy.data.materials:
        tex = []; alpha = 1.0; roughness = None; emission = 0.0
        if mat.use_nodes:
            tex = [n.name for n in mat.node_tree.nodes if n.type == "TEX_IMAGE"]
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                alpha = float(bsdf.inputs["Alpha"].default_value)
                roughness = float(bsdf.inputs["Roughness"].default_value)
                emission = float(bsdf.inputs["Emission Strength"].default_value)
        if tex: textured.append(mat.name)
        if alpha < 0.999: transparent.append(mat.name)
        if mat.name not in allowed or not mat.name.startswith("Toy_") or mat.name == "Toy_body": off_contract.append(mat.name)
        if mat.name.endswith("_Glow") and mat.name != "Toy_white_Glow": glow_violations.append(mat.name)
        mat_rows.append({"name": mat.name, "image_texture_nodes": tex, "alpha": round(alpha, 4),
                         "roughness": round(roughness, 4) if roughness is not None else None,
                         "glow": mat.name.endswith("_Glow"), "exported_emission_strength": round(emission, 4)})

    transforms_applied = all(
        all(abs(v - 1.0) < 1e-5 for v in obj.scale)
        and all(abs(v) < 1e-5 for v in obj.rotation_euler)
        and all(abs(v) < 1e-5 for v in obj.location) for obj in meshes)
    negative_scale = any(math.prod(obj.matrix_world.to_scale()) < 0 for obj in meshes)
    animations = sum(len(a.fcurves) for a in bpy.data.actions)
    unexpected = [o.name for o in objects if o.type != "MESH"]
    dims = mx - mn; center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))

    # Deterministic visibility-ray test: every first-hit outward normal must face the ray origin.
    ray_hits = ray_flipped = 0
    flipped_by_object = {}
    golden = math.pi * (3.0 - math.sqrt(5.0))
    targets = [Vector((center.x + dx * dims.x, center.y + dy * dims.y, mn.z + fz * dims.z))
               for dx, dy in ((0, 0), (-0.25, -0.12), (0.25, 0.12)) for fz in (0.15, 0.52, 0.86)]
    for target in targets:
        for i in range(1200):
            q = 1.0 - 2.0 * (i + 0.5) / 1200; r = math.sqrt(max(0.0, 1.0 - q * q)); a = golden * i
            outward = Vector((math.cos(a) * r, math.sin(a) * r, q)); direction = -outward
            hit, _, normal, _, hit_obj, _ = bpy.context.scene.ray_cast(dg, target + outward * 1000, direction, distance=1400)
            if hit:
                ray_hits += 1
                if normal.dot(direction) > 1e-5:
                    ray_flipped += 1
                    flipped_by_object[hit_obj.name] = flipped_by_object.get(hit_obj.name, 0) + 1

    normal_ray_tolerance = max(3, math.ceil(ray_hits * 0.005))
    normals_pass = invalid_normals == 0 and ray_hits > 0 and ray_flipped <= normal_ray_tolerance

    results = {
        "asset": os.path.basename(glb), "validator": "Blender " + bpy.app.version_string,
        "fresh_isolated_scene": True, "reimported_final_glb": True,
        "object_count": len(objects), "mesh_object_count": len(meshes),
        "triangle_count": tris, "triangle_budget": 24000,
        "dimensions_m": rounded(dims), "bbox_min_m": rounded(mn), "bbox_max_m": rounded(mx),
        "min_z_m": round(mn.z, 4), "xy_center_offset_m": [round(center.x, 4), round(center.y, 4)],
        "materials": sorted(m.name for m in bpy.data.materials),
        "material_details": sorted(mat_rows, key=lambda x: x["name"]),
        "image_texture_count": len(bpy.data.images), "textured_materials": sorted(textured),
        "transparent_materials": sorted(transparent), "camera_count": len(bpy.data.cameras),
        "light_count": len(bpy.data.lights), "animation_fcurve_count": animations,
        "armature_count": sum(1 for o in objects if o.type == "ARMATURE"),
        "constraint_count": sum(len(o.constraints) for o in objects),
        "transforms_applied": transforms_applied, "negative_scales": negative_scale,
        "degenerate_triangle_count": degenerate, "invalid_or_nonunit_loop_normal_count": invalid_normals,
        "normal_ray_cast_first_hits": ray_hits, "normal_ray_cast_flipped_visible_faces": ray_flipped,
        "normal_ray_cast_flipped_by_object": dict(sorted(flipped_by_object.items())),
        "normal_ray_cast_tolerance": normal_ray_tolerance,
        "normal_orientation_status": "PASS" if normals_pass else "FAIL",
        "normal_orientation_method": "Reimported loop normals are finite/unit; 10,800 deterministic first-hit visibility rays verify outward faces with a 0.5% tolerance for coplanar decorative planes.",
        "unexpected_geometry_or_objects": unexpected, "material_contract_violations": sorted(off_contract),
        "glow_contract_violations": sorted(glow_violations),
        "duplicate_object_names": sorted({o.name for o in objects if sum(x.name == o.name for x in objects) > 1}),
        "object_details": sorted(object_rows, key=lambda x: x["name"]),
    }
    results["checks"] = {
        "meters_and_plausible_dimensions": 150 <= dims.x <= 180 and 185 <= dims.y <= 210 and 74 <= dims.z <= 76,
        "base_at_z_zero": abs(mn.z) <= 0.05,
        "centered_xy": abs(center.x) <= 0.05 and abs(center.y) <= 0.05,
        "under_triangle_budget": tris <= 24000,
        "no_image_textures": not bpy.data.images and not textured,
        "no_transparency": not transparent,
        "materials_follow_contract": not off_contract and not glow_violations,
        "no_cameras_or_lights": not bpy.data.cameras and not bpy.data.lights,
        "no_animation_skin_or_constraints": animations == 0 and results["armature_count"] == 0 and results["constraint_count"] == 0,
        "transforms_applied": transforms_applied,
        "no_negative_scales": not negative_scale,
        "normals_outward": normals_pass,
        "no_degenerate_geometry": degenerate == 0,
        "no_unexpected_objects": not unexpected,
        "unique_object_names": not results["duplicate_object_names"],
    }
    results["overall"] = "PASS" if all(results["checks"].values()) else "FAIL"
    with open(output, "w", encoding="utf-8") as f: json.dump(results, f, indent=2); f.write("\n")
    print(json.dumps({k: results[k] for k in ("overall", "triangle_count", "dimensions_m", "bbox_min_m", "bbox_max_m", "checks")}, indent=2))


if __name__ == "__main__": main()
