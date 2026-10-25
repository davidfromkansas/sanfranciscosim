"""Fresh-scene contract validation for a landmark GLB (Transbay batch).

    blender -b --python tools/landmark-kit/validate.py -- --glb FILE --out FILE
        --height 326.0 [--budget 27000] [--anchor LON,LAT]

Factory-resets, imports only the final GLB and writes the machine-readable
report. Generalised from artifacts/8-mission/validate_8_mission.py: the same
contract checks, normals tests (per-object signed volume + deterministic
visibility rays, 0.15% residual) and glow-strip orientation test.
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
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

    def arg(flag, default=None):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb")
    output = arg("--out")
    target_h = float(arg("--height"))
    budget = int(arg("--budget", "27000"))
    anchor = arg("--anchor")

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)

    objects = list(bpy.data.objects)
    meshes = [o for o in objects if o.type == "MESH"]
    dg = bpy.context.evaluated_depsgraph_get()
    mn = Vector((1e12,) * 3)
    mx = Vector((-1e12,) * 3)
    tris = degenerate = invalid_normal = verts_total = 0
    rows = []
    for obj in meshes:
        ev = obj.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        verts_total += len(me.vertices)
        degenerate += sum(1 for t in me.loop_triangles if t.area < 1e-8)
        for v in me.vertices:
            w = obj.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
        for loop in me.loops:
            n = loop.normal
            if not all(math.isfinite(c) for c in n) or abs(n.length - 1.0) > 1e-3:
                invalid_normal += 1
        rows.append({"name": obj.name, "triangles": len(me.loop_triangles),
                     "location": rounded(obj.location), "rotation_euler": rounded(obj.rotation_euler),
                     "scale": rounded(obj.scale)})
        ev.to_mesh_clear()

    mat_rows, textured, transparent, off_contract = [], [], [], []
    for mat in bpy.data.materials:
        tex, alpha, rough = [], 1.0, None
        if mat.use_nodes:
            tex = [n.name for n in mat.node_tree.nodes if n.type == "TEX_IMAGE"]
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                alpha = float(bsdf.inputs["Alpha"].default_value)
                rough = float(bsdf.inputs["Roughness"].default_value)
        if tex:
            textured.append(mat.name)
        if alpha < 0.999:
            transparent.append(mat.name)
        if not mat.name.startswith("Toy_") or mat.name == "Toy_body":
            off_contract.append(mat.name)
        mat_rows.append({"name": mat.name, "image_texture_nodes": tex, "alpha": round(alpha, 4),
                         "roughness": round(rough, 4) if rough is not None else None,
                         "glow": mat.name.endswith("_Glow")})

    applied = all(all(abs(v - 1) < 1e-5 for v in o.scale) and all(abs(v) < 1e-5 for v in o.rotation_euler)
                  and all(abs(v) < 1e-5 for v in o.location) for o in meshes)
    negative = any(o.matrix_world.to_scale().x * o.matrix_world.to_scale().y * o.matrix_world.to_scale().z < 0
                   for o in meshes)
    anims = sum(len(a.fcurves) for a in bpy.data.actions) if hasattr(bpy.types.Action, "fcurves") else len(bpy.data.actions)
    unexpected = [o.name for o in objects if o.type != "MESH"]
    dims = mx - mn
    center = (mn + mx) / 2

    # Visibility rays from interior targets: the first visible face must face the ray's origin.
    hits = flipped = 0
    golden = math.pi * (3.0 - math.sqrt(5.0))
    R = max(dims) * 1.5
    targets = [Vector((center.x + dx * dims.x, center.y + dy * dims.y, mn.z + fz * dims.z))
               for dx, dy in ((0.0, 0.0), (-0.12, 0.12), (0.12, -0.12)) for fz in (0.18, 0.45, 0.72)]
    for target in targets:
        for i in range(2500):
            y = 1.0 - 2.0 * (i + 0.5) / 2500
            r = math.sqrt(max(0.0, 1.0 - y * y))
            a = golden * i
            outward = Vector((math.cos(a) * r, math.sin(a) * r, y))
            hit, _, normal, _, obj, _ = bpy.context.scene.ray_cast(dg, target + outward * R, -outward, distance=2 * R)
            if hit and obj is not None and "_glow" in obj.name.lower():
                continue  # glow skins are single-sided sheets; tested separately
            if hit:
                hits += 1
                if normal.dot(-outward) > 1e-5:
                    flipped += 1

    vol_ok, vol_bad = 0, []
    glow_faces = glow_out = 0
    for obj in meshes:
        ev = obj.evaluated_get(dg)
        me = ev.to_mesh()
        if "_glow" in obj.name.lower():
            for poly in me.polygons:
                glow_faces += 1
                c = obj.matrix_world @ poly.center
                nrm = (obj.matrix_world.to_3x3() @ poly.normal).normalized()
                # a glow skin faces outward if nothing body-side blocks the view from outside
                hit, _, hn, _, hobj, _ = bpy.context.scene.ray_cast(dg, c + nrm * 0.02, nrm, distance=0.5)
                if not hit or (hobj is not None and "_glow" in hobj.name.lower()):
                    glow_out += 1
            ev.to_mesh_clear()
            continue
        me.calc_loop_triangles()
        vol = 0.0
        for t in me.loop_triangles:
            a, b, c = (obj.matrix_world @ me.vertices[i].co for i in t.vertices)
            vol += a.dot(b.cross(c)) / 6.0
        if vol > 1e-9:
            vol_ok += 1
        else:
            vol_bad.append(obj.name)
        ev.to_mesh_clear()

    frac = flipped / hits if hits else None
    res = {
        "asset": os.path.basename(glb),
        "validator": "Blender " + bpy.app.version_string,
        "fresh_isolated_scene": True,
        "reimported_final_glb": True,
        "object_count": len(objects),
        "mesh_object_count": len(meshes),
        "triangle_count": tris,
        "vertex_count_blender": verts_total,
        "triangle_budget": budget,
        "dimensions_m": rounded(dims),
        "bbox_min_m": rounded(mn),
        "bbox_max_m": rounded(mx),
        "min_z_m": round(mn.z, 4),
        "xy_center_offset_m": [round(center.x, 4), round(center.y, 4)],
        "target_height_m": target_h,
        "materials": sorted(m.name for m in bpy.data.materials),
        "material_details": sorted(mat_rows, key=lambda x: x["name"]),
        "image_texture_count": len(bpy.data.images),
        "textured_materials": sorted(textured),
        "transparent_materials": sorted(transparent),
        "camera_count": len(bpy.data.cameras),
        "light_count": len(bpy.data.lights),
        "animation_count": anims,
        "armature_count": sum(1 for o in objects if o.type == "ARMATURE"),
        "constraint_count": sum(len(o.constraints) for o in objects),
        "transforms_applied": applied,
        "negative_scales": negative,
        "degenerate_triangle_count": degenerate,
        "invalid_or_nonunit_loop_normal_count": invalid_normal,
        "normal_ray_cast_first_hits": hits,
        "normal_ray_cast_flipped_visible_faces": flipped,
        "normal_ray_cast_flipped_fraction": round(frac, 6) if frac is not None else None,
        "signed_volume_outward_objects": vol_ok,
        "signed_volume_inverted_objects": vol_bad,
        "glow_faces": glow_faces,
        "glow_faces_unobstructed_outward": glow_out,
        "unexpected_objects": unexpected,
        "material_contract_violations": sorted(off_contract),
        "glow_materials": sorted(m["name"] for m in mat_rows if m["glow"]),
        "object_details": rows,
    }
    if anchor:
        res["anchor_lonlat"] = [float(v) for v in anchor.split(",")]
    res["checks"] = {
        "crest_normalized_to_target": abs(mx.z - target_h) <= 0.02,
        "plausible_metre_dimensions": 2.0 < dims.x < 500 and 2.0 < dims.y < 500,
        "base_at_z_zero": abs(mn.z) <= 0.5,
        "centered_xy": abs(center.x) <= 1.0 and abs(center.y) <= 1.0,
        "under_triangle_budget": tris <= budget,
        "no_image_textures": not bpy.data.images and not textured,
        "no_transparency": not transparent,
        "materials_follow_contract": not off_contract,
        "has_night_glow": bool(res["glow_materials"]),
        "no_cameras_or_lights": not bpy.data.cameras and not bpy.data.lights,
        "no_animation_skin_or_constraints": anims == 0 and res["armature_count"] == 0 and res["constraint_count"] == 0,
        "transforms_applied": applied,
        "no_negative_scales": not negative,
        "normals_outward_signed_volume": not vol_bad,
        "normals_outward_ray_residual_within_tolerance": invalid_normal == 0 and hits > 0 and frac <= 0.0015,
        "glow_skins_face_outward": glow_faces > 0 and glow_out >= 0.97 * glow_faces,
        "no_degenerate_geometry": degenerate == 0,
        "no_unexpected_objects": not unexpected,
    }
    res["overall"] = "PASS" if all(res["checks"].values()) else "FAIL"
    with open(output, "w") as f:
        json.dump(res, f, indent=2)
        f.write("\n")
    print(json.dumps({k: res[k] for k in ("overall", "triangle_count", "dimensions_m", "min_z_m",
                                          "xy_center_offset_m", "materials")}, indent=1))
    print({k: v for k, v in res["checks"].items() if not v} or "all checks pass")


if __name__ == "__main__":
    main()
