"""Fresh-scene contract validation for davies-symphony-hall.glb.

    blender -b --python validate_davies_symphony_hall.py -- [--glb FILE] [--out FILE]

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

TRI_BUDGET = 16000
TARGET_HEIGHT = 35.0
ARC_CX, ARC_CY, ARC_R = 10.03, -1.02, 44.75
RAY_RESIDUAL_TOLERANCE = 0.0015  # 0.15%, per the asset plan's normals gate


def rounded(v):
    return [round(x, 4) for x in v]


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "davies-symphony-hall.glb"))
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
    open_shell_objects = []
    inverted_volume_objects = []

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

        # Per-object signed volume: authoritative for the closed solids that
        # make up most of this asset (plinth, hall body, fins, slots, cornice,
        # terraces, plant). A closed mesh with outward normals has volume > 0.
        # glTF stores split vertices for flat shading, so a re-imported solid
        # has no shared edges until coincident vertices are welded. Weld into a
        # throwaway bmesh before asking whether it is closed.
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
        bm.transform(obj.matrix_world)
        closed = all(len(e.link_faces) == 2 for e in bm.edges)
        vol = 0.0
        for face in bm.faces:
            vs = face.verts
            for k in range(1, len(vs) - 1):
                a, b, c = vs[0].co, vs[k].co, vs[k + 1].co
                vol += a.dot(b.cross(c)) / 6.0
        bm.free()
        if not closed:
            open_shell_objects.append(obj.name)
        elif vol <= 0:
            inverted_volume_objects.append(obj.name)

        object_rows.append(
            {
                "name": obj.name,
                "triangles": len(me.loop_triangles),
                "closed_solid": closed,
                "signed_volume_m3": round(vol, 3),
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

    # Visibility-based outward-normal test. Most of the asset is a union of
    # closed solids (judged above by signed volume); the shell roof, its ribs
    # and the night-glow shells are deliberately single-sided, so a small
    # residual of back-facing first hits is expected and gated at 0.15%.
    ray_hits = 0
    ray_flipped = 0
    golden = math.pi * (3.0 - math.sqrt(5.0))
    targets = [
        Vector((center.x + dx * dims.x, center.y + dy * dims.y, mn.z + fz * dims.z))
        for dx, dy in ((0.0, 0.0), (-0.20, 0.20), (0.20, -0.20))
        for fz in (0.2, 0.45, 0.75)
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

    # The front arc is the building; measure it back out of the export. The
    # fins stand FIN_D/2 = 0.3 m proud of the wall line, so an arc fin's
    # centroid sits at R + 0.3; fins on the straight Grove and Van Ness flanks
    # are excluded by the selection band, not by the tolerance.
    ARC_FIN_R = ARC_R + 0.3
    arc_residuals = []
    for obj in meshes:
        if not obj.name.startswith("fin"):
            continue
        ev = obj.evaluated_get(dg)
        me = ev.to_mesh()
        cx = sum((obj.matrix_world @ v.co).x for v in me.vertices) / len(me.vertices)
        cy = sum((obj.matrix_world @ v.co).y for v in me.vertices) / len(me.vertices)
        d = math.hypot(cx - ARC_CX, cy - ARC_CY)
        if abs(d - ARC_FIN_R) < 1.2:
            arc_residuals.append(abs(d - ARC_FIN_R))
        ev.to_mesh_clear()
    arc_fin_count = len(arc_residuals)
    arc_max_residual = round(max(arc_residuals), 3) if arc_residuals else None

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
        "target_height_m": TARGET_HEIGHT,
        "loader_scale_factor": round(TARGET_HEIGHT / (mx.z - mn.z), 6),
        "xy_center_offset_m": [round(center.x, 4), round(center.y, 4)],
        "front_arc_radius_m": ARC_R,
        "front_arc_centre_local": [ARC_CX, ARC_CY],
        "front_arc_fins_measured": arc_fin_count,
        "front_arc_max_residual_m": arc_max_residual,
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
        "closed_solids_with_inverted_volume": sorted(inverted_volume_objects),
        "intentional_open_shells": sorted(open_shell_objects),
        "normal_ray_cast_first_hits": ray_hits,
        "normal_ray_cast_flipped_visible_faces": ray_flipped,
        "normal_ray_cast_residual": round(ray_residual, 6),
        "normal_orientation_status": "PASS"
        if invalid_normal_count == 0
        and not inverted_volume_objects
        and ray_hits > 0
        and ray_residual <= RAY_RESIDUAL_TOLERANCE
        else "FAIL",
        "normal_orientation_method": (
            "All source meshes run bmesh.ops.recalc_face_normals before export. "
            "Per-object signed volume is authoritative for the closed solids "
            "(must be > 0); the shell roof, ribs and night-glow shells are "
            "single-sided by design, so 22,500 deterministic visibility rays "
            "gate the back-facing residual at 0.15%."
        ),
        "unexpected_geometry_or_objects": unexpected,
        "material_contract_violations": sorted(off_contract),
        "object_details": sorted(object_rows, key=lambda x: x["name"]),
    }
    results["checks"] = {
        # 122.6 x 91.2 m block + a 1.2 m plinth apron, and the terraces
        # cantilevering 4.5 m off the north end of the arc
        "meters_and_plausible_dimensions": 34.5 <= dims.z <= 35.5
        and 120 <= dims.x <= 130
        and 90 <= dims.y <= 100,
        "crest_lands_on_target_height": abs(mx.z - TARGET_HEIGHT) <= 0.05,
        "base_at_z_zero": abs(mn.z) <= 0.5,
        "centered_xy": abs(center.x) <= 1.0 and abs(center.y) <= 1.0,
        "front_arc_preserved": arc_fin_count >= 20
        and arc_max_residual is not None
        and arc_max_residual <= 1.0,
        "under_triangle_budget": tris <= TRI_BUDGET,
        "no_image_textures": not bpy.data.images and not textured,
        "no_transparency": not transparent,
        "materials_follow_contract": not off_contract,
        "no_cameras_or_lights": not bpy.data.cameras and not bpy.data.lights,
        "no_animation_skin_or_constraints": animations == 0
        and results["armature_count"] == 0
        and results["constraint_count"] == 0,
        "transforms_applied": scales_applied,
        "no_negative_scales": negative_scale is False,
        "normals_outward": results["normal_orientation_status"] == "PASS",
        "no_degenerate_geometry": degenerate == 0,
        "no_unexpected_objects": not unexpected,
        "glow_present": any(m.endswith("_Glow") for m in results["materials"]),
    }
    results["overall"] = "PASS" if all(results["checks"].values()) else "FAIL"

    with open(output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        f.write("\n")
    print(json.dumps({k: v for k, v in results.items()
                      if k not in ("object_details", "material_details")}, indent=2))


if __name__ == "__main__":
    main()
