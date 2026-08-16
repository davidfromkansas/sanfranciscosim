"""Fresh-scene contract validation for letterman-digital-arts-center.glb.

    blender -b --python validate_letterman_digital_arts_center.py -- [--glb FILE]
                                                              [--out FILE]

This script factory-resets, imports only the final GLB, and writes the complete
machine-readable report. It does not inspect the source .blend.
"""

import json
import math
import os
import sys

import bpy
from mathutils import Vector

TRI_BUDGET = 27000


def rounded(v):
    return [round(x, 4) for x in v]


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "letterman-digital-arts-center.glb"))
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
    glow_materials = []
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
        if mat.name.endswith("_Glow"):
            glow_materials.append(mat.name)
        mat_rows.append(
            {
                "name": mat.name,
                "image_texture_nodes": tex,
                "alpha": round(alpha, 4),
                "roughness": round(roughness, 4) if roughness is not None else None,
                "glow": mat.name.endswith("_Glow"),
            }
        )

    # which objects carry the glow materials — the contract limits night glow
    glow_objects = sorted(
        {
            o.name
            for o in meshes
            for slot in o.material_slots
            if slot.material and slot.material.name.endswith("_Glow")
        }
    )

    transforms_applied = all(
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

    # Visibility-based outward-normal test. The asset mixes closed solids with
    # single-sided facade panels, so signed-volume tests do not apply: cast a
    # deterministic sphere of rays toward nine interior targets; the first face
    # each ray meets is visible from outside and must oppose the ray direction.
    ray_hits = 0
    ray_flipped = 0
    flipped_examples = []
    golden = math.pi * (3.0 - math.sqrt(5.0))
    targets = [
        Vector((center.x + dx * dims.x, center.y + dy * dims.y, mn.z + fz * dims.z))
        for dx, dy in ((0.0, 0.0), (-0.22, -0.12), (0.28, 0.06))
        for fz in (0.12, 0.35, 0.75)
    ]
    for target in targets:
        for i in range(2500):
            y = 1.0 - 2.0 * (i + 0.5) / 2500
            r = math.sqrt(max(0.0, 1.0 - y * y))
            a = golden * i
            outward = Vector((math.cos(a) * r, math.sin(a) * r, y))
            direction = -outward
            hit, _, normal, _, obj, _ = bpy.context.scene.ray_cast(
                dg, target + outward * 800.0, direction, distance=1600.0
            )
            if hit:
                ray_hits += 1
                if normal.dot(direction) > 1e-5:
                    ray_flipped += 1
                    if obj is not None and obj.name not in flipped_examples:
                        flipped_examples.append(obj.name)

    # Ground-hugging single-sided ribbons (the walk, the stream, the water
    # tops) are open shells lying flat on the meadow: a ray fired from below
    # the diorama meets their unlit back face, which the visibility test scores
    # as flipped even though they are correctly wound upward. They are checked
    # separately — every face must point up — and excluded from the ray verdict.
    # Only the two true open ribbons. The lagoon and fountain water are closed
    # prisms whose bottom faces legitimately point down.
    RIBBONS = {"walk", "stream"}
    ribbon_down = 0
    for obj in meshes:
        if obj.name not in RIBBONS:
            continue
        me = obj.evaluated_get(dg).to_mesh()
        ribbon_down += sum(1 for p in me.polygons if p.normal.z < 0.0)
        obj.evaluated_get(dg).to_mesh_clear()
    ray_flipped_solid = ray_flipped - sum(
        1 for n in flipped_examples if n in RIBBONS
    )
    flipped_examples = [n for n in flipped_examples if n not in RIBBONS]
    normals_ok = (
        invalid_normal_count == 0
        and ray_hits > 0
        and ray_flipped_solid <= 0
        and ribbon_down == 0
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
        "xy_center_offset_m": [round(center.x, 4), round(center.y, 4)],
        "materials": sorted(mat.name for mat in bpy.data.materials),
        "material_details": sorted(mat_rows, key=lambda x: x["name"]),
        "image_texture_count": len(bpy.data.images),
        "textured_materials": sorted(textured),
        "transparent_materials": sorted(transparent),
        "glow_materials": sorted(glow_materials),
        "glow_objects": glow_objects,
        "camera_count": len(bpy.data.cameras),
        "light_count": len(bpy.data.lights),
        "animation_fcurve_count": animations,
        "armature_count": sum(1 for o in objects if o.type == "ARMATURE"),
        "constraint_count": sum(len(o.constraints) for o in objects),
        "transforms_applied": transforms_applied,
        "negative_scales": negative_scale,
        "degenerate_triangle_count": degenerate,
        "invalid_or_nonunit_loop_normal_count": invalid_normal_count,
        "normal_ray_cast_first_hits": ray_hits,
        "normal_ray_cast_flipped_visible_faces": ray_flipped,
        "normal_ray_cast_flipped_solid_faces": ray_flipped_solid,
        "ground_ribbon_downward_faces": ribbon_down,
        "normal_ray_cast_flipped_objects": flipped_examples[:20],
        "normal_orientation_status": "PASS" if normals_ok else "FAIL",
        "normal_orientation_method": (
            "Closed solids run bmesh.ops.recalc_face_normals; facade panels are "
            "wound explicitly. Reimported loop normals must be finite and unit "
            "length, and 22,500 deterministic visibility rays toward nine "
            "interior targets must never meet a flipped first face."
        ),
        "unexpected_geometry_or_objects": unexpected,
        "material_contract_violations": sorted(off_contract),
        "object_details": sorted(object_rows, key=lambda x: x["name"]),
    }
    results["checks"] = {
        # Campus asset: ~312 x 298 m of grounds, 22 m to the tallest roof vent
        # (the verified-estimated architectural height, so the loader's
        # targetHeightM / measuredHeight lands at 1.0).
        "meters_and_plausible_dimensions": 21.5 <= dims.z <= 22.5
        and 290 <= dims.x <= 330
        and 280 <= dims.y <= 315,
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
        "transforms_applied": transforms_applied,
        "no_negative_scales": not negative_scale,
        "normals_outward": normals_ok,
        "no_degenerate_geometry": degenerate == 0,
        "no_unexpected_objects": not unexpected,
        # Night glow must stay on the declared surfaces: Building B's entrance
        # canopy fascia and door (b_glow_*), and the lit-room window veneers
        # (win_<X>_lit). Nothing else in a campus lights up.
        "glow_limited_to_declared_night_surfaces": all(
            n.startswith("b_glow_") or n.endswith("_lit")
            for n in glow_objects
        )
        and len(glow_objects) > 0,
    }
    results["overall"] = "PASS" if all(results["checks"].values()) else "FAIL"

    with open(output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        f.write("\n")
    print(json.dumps({k: results[k] for k in ("asset", "object_count",
                                              "triangle_count", "dimensions_m",
                                              "min_z_m", "xy_center_offset_m",
                                              "materials", "glow_objects",
                                              "checks", "overall")}, indent=2))


if __name__ == "__main__":
    main()
