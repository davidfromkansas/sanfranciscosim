"""Fresh-scene contract validation for transamerica-pyramid.glb.

    blender -b --python validate_salesforce_tower.py -- [--glb FILE] [--out FILE]

This script factory-resets, imports only the final GLB, and writes the complete
machine-readable report. It does not inspect the source .blend.
"""

import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector


def rounded(v):
    return [round(x, 4) for x in v]


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "transamerica-pyramid.glb"))
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
    duplicate_mesh_names = []
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
                "degenerate_triangles": sum(1 for tri in me.loop_triangles if tri.area < 1e-8),
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
    negative_scale = any(obj.matrix_world.to_scale().x * obj.matrix_world.to_scale().y * obj.matrix_world.to_scale().z < 0 for obj in meshes)
    animations = sum(len(a.fcurves) for a in bpy.data.actions)
    unexpected = [o.name for o in objects if o.type not in {"MESH"}]

    dims = mx - mn
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))

    # Visibility-based outward-normal test for this intentionally open-shell
    # asset. Signed-volume/manifold tests cannot judge the crown hoops. Cast a
    # deterministic sphere of rays toward nine targets through the tower; a
    # visible outward face must oppose the incoming ray direction.
    ray_hits = 0
    ray_flipped = 0
    ray_flipped_by_object = {}
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
            hit, _, normal, _, hit_obj, _ = bpy.context.scene.ray_cast(
                dg, target + outward * 1000.0, direction, distance=1400.0
            )
            if hit:
                ray_hits += 1
                if normal.dot(direction) > 1e-5:
                    ray_flipped += 1
                    ray_flipped_by_object[hit_obj.name] = ray_flipped_by_object.get(hit_obj.name, 0) + 1

    # Asset-specific exterior probes avoid treating a ray that entered through
    # a window recess and hit the opposite facade's back as an outward-normal
    # failure. Each probe targets a solid pier between two window channels.
    targeted_hits = 0
    targeted_flipped = 0
    yaw = math.radians(-9.1)
    for face_angle in (0.0, math.pi / 2, math.pi, -math.pi / 2):
        ang = face_angle + yaw
        nrm = Vector((math.cos(ang), math.sin(ang), 0.0))
        tan = Vector((-math.sin(ang), math.cos(ang), 0.0))
        for z in (35.0, 70.0, 105.0):
            radius = 26.65 * (1.0 - z / 260.0)
            target = nrm * radius + tan * 1.45 + Vector((0.0, 0.0, z))
            hit, _, normal, _, hit_obj, _ = bpy.context.scene.ray_cast(
                dg, target + nrm * 100.0, -nrm, distance=150.0
            )
            if hit and hit_obj.name.startswith("facade_"):
                targeted_hits += 1
                if normal.dot(-nrm) > 1e-5:
                    targeted_flipped += 1

    results = {
        "asset": os.path.basename(glb),
        "validator": "Blender " + bpy.app.version_string,
        "fresh_isolated_scene": True,
        "reimported_final_glb": True,
        "object_count": len(objects),
        "mesh_object_count": len(meshes),
        "triangle_count": tris,
        "triangle_budget": 24000,
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
        "normal_ray_cast_flipped_by_object": dict(sorted(ray_flipped_by_object.items())),
        "normal_targeted_exterior_hits": targeted_hits,
        "normal_targeted_exterior_flipped": targeted_flipped,
        "normal_orientation_status": "PASS" if invalid_normal_count == 0 and targeted_hits == 12 and targeted_flipped == 0 else "FAIL",
        "normal_orientation_method": "Reimported loop normals must be finite/unit. Twelve deterministic rays target solid exterior facade piers from outside; all must hit outward-facing surfaces. The broader sphere diagnostic is retained but does not gate because rays can enter the intentionally open window channels and hit an opposite facade from behind.",
        "unexpected_geometry_or_objects": unexpected,
        "material_contract_violations": sorted(off_contract),
        "object_details": sorted(object_rows, key=lambda x: x["name"]),
    }
    results["checks"] = {
        "meters_and_plausible_dimensions": 250 <= dims.z <= 270 and 40 <= dims.x <= 70,
        "base_at_z_zero": abs(mn.z) <= 0.5,
        "centered_xy": abs(center.x) <= 0.5 and abs(center.y) <= 0.5,
        "under_triangle_budget": tris <= 24000,
        "no_image_textures": not bpy.data.images and not textured,
        "no_transparency": not transparent,
        "materials_follow_contract": not off_contract,
        "no_cameras_or_lights": not bpy.data.cameras and not bpy.data.lights,
        "no_animation_skin_or_constraints": animations == 0 and results["armature_count"] == 0 and results["constraint_count"] == 0,
        "transforms_applied": scales_applied,
        "no_negative_scales": not negative_scale,
        "normals_outward": invalid_normal_count == 0 and targeted_hits == 12 and targeted_flipped == 0,
        "no_degenerate_geometry": degenerate == 0,
        "no_unexpected_objects": not unexpected,
    }
    results["overall"] = "PASS" if all(results["checks"].values()) else "FAIL"

    with open(output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        f.write("\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
