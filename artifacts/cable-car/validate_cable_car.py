"""Fresh-scene contract validation for cable-car-powell.glb.

    blender -b --python validate_cable_car.py -- [--glb FILE] [--out FILE]

Factory-resets, imports only the final GLB, and writes the machine-readable
report. It never inspects the source .blend.

REPORTING SPACE.  Blender's glTF importer converts the file's Y-up axes back to
Z-up, so this scene's +Y is the file's -Z. Every geometric figure below is
converted back into glTF/three space before it is reported -

    (gx, gy, gz) = (bx, bz, -by)

- because that is the space `app/src/agents.js` and `vehicles_manifest.json`
speak: front -Z, up +Y, wheels at min y = 0.

THE HARD GATE is per-object signed volume. The vehicle is deliberately open -
no side walls over the grip section, voids between the roof posts - so any
component modelled as a shell instead of a solid produces an open mesh whose
signed volume is meaningless. Every object is therefore checked twice: closed
(every edge has exactly two faces) AND positive signed volume.
"""

import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

TRI_BUDGET = 6000
PUBLISHED_L = 8.40      # 27 ft 6 in
PUBLISHED_W = 2.40      # 8 ft, over the running boards
PUBLISHED_H = 3.18      # 10 ft 5 in, to the monitor deck
GAUGE = 1.067           # 3 ft 6 in

# Materials the contract allows to be off-palette, each with its reason.
OFF_PALETTE = {
    "Toy_maroon": "the Powell livery; Toy_brick #c96f4a reads as terracotta",
    "Toy_oak": "varnished wood - posts, benches, window frames, monitor wall",
    "Toy_p_tan": "figure heads; the contract palette carries no skin tone",
}
PALETTE_KEYS = {
    "cream", "sand", "trim", "teal", "coral", "mustard", "mint", "sky", "navy",
    "glass", "glassl", "ink", "roofd", "brick", "stone", "red", "steel", "rust",
    "gold", "ioorange", "verdigris", "white",
}


def rounded(v, n=4):
    return [round(x, n) for x in v]


def to_gltf(v):
    """Blender (x, y, z) -> glTF (x, z, -y)."""
    return Vector((v.x, v.z, -v.y))


def signed_volume(mesh, matrix):
    """Divergence-theorem volume of the world-space mesh. Positive means the
    faces wind outward; negative means the solid is inside out."""
    mesh.calc_loop_triangles()
    total = 0.0
    for tri in mesh.loop_triangles:
        a, b, c = (matrix @ mesh.vertices[i].co for i in tri.vertices)
        total += a.dot(b.cross(c)) / 6.0
    return total


def is_closed(mesh):
    """Every edge bounded by exactly two faces, after welding coincident verts.

    The weld is not optional: the glTF exporter splits a vertex per distinct
    normal, and this asset is shaded flat, so a re-imported cube arrives as six
    topologically disconnected quads. Testing the raw import reports every
    object in the file as an open shell.
    """
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    ok = bool(bm.faces) and all(len(e.link_faces) == 2 for e in bm.edges)
    bm.free()
    return ok


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "cable-car-powell.authored.glb"))
    output = arg("--out", os.path.join(here, "validation.json"))
    # "authored" = the export straight out of build_cable_car.py, where every
    # component is still its own object and the per-object closure gate means
    # something. "shipped" = after the shrink's join-by-material step, where
    # the 227 objects have become 20 per-material groups: closure and the
    # figure-name checks are then structurally inapplicable and are reported as
    # observations instead of gates (docs/asset-plans/transit/README.md Part 3
    # step 5 asks for exactly that join).
    stage = arg("--stage", "authored")

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)

    objects = list(bpy.data.objects)
    meshes = [o for o in objects if o.type == "MESH"]
    dg = bpy.context.evaluated_depsgraph_get()

    bmn = Vector((1e12, 1e12, 1e12))
    bmx = Vector((-1e12, -1e12, -1e12))
    tris = 0
    degenerate = 0
    bad_normals = 0
    open_objects = []
    inverted_objects = []
    object_rows = []
    material_extent = {}

    for obj in meshes:
        ev = obj.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        degenerate += sum(1 for t in me.loop_triangles if t.area < 1e-9)
        for loop in me.loops:
            n = loop.normal
            if not all(math.isfinite(v) for v in n) or abs(n.length - 1.0) > 1e-3:
                bad_normals += 1

        vol = signed_volume(me, obj.matrix_world)
        closed = is_closed(me)
        if not closed:
            open_objects.append(obj.name)
        if vol <= 0:
            inverted_objects.append(obj.name)

        omn = Vector((1e12, 1e12, 1e12))
        omx = Vector((-1e12, -1e12, -1e12))
        for v in me.vertices:
            w = obj.matrix_world @ v.co
            for i in range(3):
                bmn[i] = min(bmn[i], w[i])
                bmx[i] = max(bmx[i], w[i])
                omn[i] = min(omn[i], w[i])
                omx[i] = max(omx[i], w[i])
        for m in me.materials:
            if not m:
                continue
            cur = material_extent.setdefault(m.name, [1e12, -1e12, 1e12, -1e12])
            cur[0] = min(cur[0], omn.y)
            cur[1] = max(cur[1], omx.y)
            cur[2] = min(cur[2], omn.x)
            cur[3] = max(cur[3], omx.x)

        object_rows.append(
            {
                "name": obj.name,
                "triangles": len(me.loop_triangles),
                "closed_solid": closed,
                "signed_volume_m3": round(vol, 6),
                "location": rounded(obj.location),
                "rotation_euler": rounded(obj.rotation_euler),
                "scale": rounded(obj.scale),
            }
        )
        ev.to_mesh_clear()

    # ---------------------------------------------------------------- materials
    mat_rows = []
    textured = []
    transparent = []
    off_contract = []
    off_palette_warn = []
    for mat in bpy.data.materials:
        tex = []
        alpha = 1.0
        roughness = None
        emission = None
        if mat.use_nodes:
            tex = [n.name for n in mat.node_tree.nodes if n.type == "TEX_IMAGE"]
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                alpha = float(bsdf.inputs["Alpha"].default_value)
                roughness = float(bsdf.inputs["Roughness"].default_value)
                emission = float(bsdf.inputs["Emission Strength"].default_value)
        if tex:
            textured.append(mat.name)
        if alpha < 0.999:
            transparent.append(mat.name)
        if not mat.name.startswith("Toy_") or mat.name == "Toy_body":
            off_contract.append(mat.name)
        key = mat.name[len("Toy_") :].replace("_Glow", "")
        if mat.name.startswith("Toy_") and not key.startswith("p_") and key not in PALETTE_KEYS:
            off_palette_warn.append(mat.name)
        mat_rows.append(
            {
                "name": mat.name,
                "image_texture_nodes": tex,
                "alpha": round(alpha, 4),
                "roughness": round(roughness, 4) if roughness is not None else None,
                "emission_strength": round(emission, 4) if emission is not None else None,
                "glow": mat.name.endswith("_Glow"),
            }
        )

    # ------------------------------------------------------------- orientation
    # The front is the gripman's end. Two independent asymmetries prove it:
    # the headlamp glow sits at the extreme front, and the enclosed cabin's
    # glazing sits behind the mid-point. Reported in glTF space, where the
    # front must be -Z.
    def gz_range(mat_name):
        ext = material_extent.get(mat_name)
        if not ext:
            return None
        # glTF z = -Blender y, so a Blender y range maps to a flipped z range.
        return [round(-ext[1], 3), round(-ext[0], 3)]

    lamp_gz = gz_range("Toy_white_Glow")
    glass_gz = gz_range("Toy_glass")
    gmn, gmx = to_gltf(bmn), to_gltf(bmx)
    gmn, gmx = (
        Vector((min(gmn.x, gmx.x), min(gmn.y, gmx.y), min(gmn.z, gmx.z))),
        Vector((max(gmn.x, gmx.x), max(gmn.y, gmx.y), max(gmn.z, gmx.z))),
    )
    dims = gmx - gmn
    center = Vector(((gmn.x + gmx.x) / 2, (gmn.y + gmx.y) / 2, (gmn.z + gmx.z) / 2))
    front_is_neg_z = bool(
        lamp_gz and glass_gz and lamp_gz[0] < gmn.z + 0.20 and glass_gz[0] > lamp_gz[1]
    )

    # Wheel gauge, measured from the wheel material's own X extent.
    wheel_ext = material_extent.get("Toy_roofd")
    measured_gauge = round((wheel_ext[3] + wheel_ext[2]), 4) if wheel_ext else None
    if wheel_ext:
        # centres of the two wheel bands: outer extent minus half the tread
        measured_gauge = round(wheel_ext[3] * 2 - 0.12, 4)

    scales_applied = all(
        all(abs(v - 1.0) < 1e-5 for v in o.scale)
        and all(abs(v) < 1e-5 for v in o.rotation_euler)
        and all(abs(v) < 1e-5 for v in o.location)
        for o in meshes
    )
    negative_scale = any(
        o.matrix_world.to_scale().x * o.matrix_world.to_scale().y * o.matrix_world.to_scale().z < 0
        for o in meshes
    )
    animations = sum(len(a.fcurves) for a in bpy.data.actions)
    unexpected = [o.name for o in objects if o.type != "MESH"]

    figures = [r for r in object_rows if r["name"].split(".")[0].startswith(
        ("gripman", "conductor", "rider_"))]
    standees = {n.split("_")[1] for n in (r["name"] for r in figures) if n.startswith("rider_s")}

    results = {
        "asset": os.path.basename(glb),
        "validator": "Blender " + bpy.app.version_string,
        "fresh_isolated_scene": True,
        "reimported_final_glb": True,
        "reporting_space": "glTF / three.js (Y up, front -Z); converted from Blender by (x, z, -y)",
        "object_count": len(objects),
        "mesh_object_count": len(meshes),
        "triangle_count": tris,
        "triangle_budget": TRI_BUDGET,
        "dimensions_m": rounded(dims, 3),
        "published_dimensions_m": [PUBLISHED_W, PUBLISHED_H, PUBLISHED_L],
        "bbox_min_m": rounded(gmn, 4),
        "bbox_max_m": rounded(gmx, 4),
        "min_y_m": round(gmn.y, 4),
        "min_y_represents": (
            "the wheel contact patch on the STREET surface. There are no rails "
            "in this scene (docs/asset-plans/transit/README.md), so there is no "
            "top-of-rail question: the car grounds exactly like a bus."
        ),
        "xz_center_offset_m": [round(center.x, 4), round(center.z, 4)],
        "front_face_direction": "-Z" if front_is_neg_z else "UNPROVEN",
        "front_face_evidence": {
            "headlamp_glow_z_range_m": lamp_gz,
            "cabin_glazing_z_range_m": glass_gz,
            "test": "headlamp at the -Z extreme; cabin glazing entirely behind it",
        },
        "wheel_gauge_m": measured_gauge,
        "wheel_gauge_expected_m": GAUGE,
        "materials": sorted(m.name for m in bpy.data.materials),
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
        "invalid_or_nonunit_loop_normal_count": bad_normals,
        "open_shell_objects": sorted(open_objects),
        "inverted_or_zero_volume_objects": sorted(inverted_objects),
        "glow_materials": sorted(m.name for m in bpy.data.materials if m.name.endswith("_Glow")),
        "off_palette_warnings": {
            m: OFF_PALETTE.get(m, "undocumented off-palette colour")
            for m in sorted(off_palette_warn)
        },
        "material_contract_violations": sorted(off_contract),
        "unexpected_geometry_or_objects": unexpected,
        "figure_object_count": len(figures),
        "figure_triangle_count": sum(r["triangles"] for r in figures),
        "object_details": sorted(object_rows, key=lambda x: x["name"]),
    }

    per_object_checks = {
        "every_object_is_a_closed_solid": not open_objects,
        "every_object_signed_volume_positive": not inverted_objects,
        "gripman_and_conductor_present": all(
            any(r["name"].startswith(who) for r in object_rows)
            for who in ("gripman", "conductor")
        ),
        "at_least_three_standees_on_running_boards": len(standees) >= 3,
    }
    results["stage"] = stage
    results["checks"] = {
        "meters_and_published_dimensions": (
            abs(dims.z - PUBLISHED_L) <= 0.02
            and abs(dims.y - PUBLISHED_H) <= 0.05
            and dims.x <= PUBLISHED_W + 0.06
        ),
        "ground_at_min_y_zero": abs(gmn.y) <= 0.05,
        "centered_in_xz_footprint": abs(center.x) <= 0.10 and abs(center.z) <= 0.10,
        "front_faces_minus_z": front_is_neg_z,
        "narrow_gauge_wheels": measured_gauge is not None and abs(measured_gauge - GAUGE) <= 0.02,
        "under_triangle_budget": tris <= TRI_BUDGET,
        "no_image_textures": not bpy.data.images and not textured,
        "no_transparency": not transparent,
        "materials_follow_contract": not off_contract,
        "no_toy_body": "Toy_body" not in {m.name for m in bpy.data.materials},
        "no_cameras_or_lights": not bpy.data.cameras and not bpy.data.lights,
        "no_animation_skin_or_constraints": (
            animations == 0 and results["armature_count"] == 0 and results["constraint_count"] == 0
        ),
        "transforms_applied": scales_applied,
        "no_negative_scales": not negative_scale,
        "normals_finite_and_unit": bad_normals == 0,
        "no_degenerate_geometry": degenerate == 0,
        "no_unexpected_objects": not unexpected,
        "glow_set_is_night_only": all(
            m["emission_strength"] in (0.0, None) for m in mat_rows if m["glow"]
        ),
        "glow_materials_present": len(results["glow_materials"]) >= 2,
    }
    if stage == "authored":
        results["checks"].update(per_object_checks)
    else:
        results["per_object_observations"] = per_object_checks
        results["per_object_note"] = (
            "Not gated at this stage. The shrink pass joins the 227 authored "
            "objects into 20 per-material groups and deletes provably buried "
            "faces, so a group is a union of solids rather than one closed "
            "solid. What still has to hold - and is gated in shrink-stats.json "
            "as merge_vehicle_safe - is that every group's signed volume stays "
            "POSITIVE, because mergeVehicle() reverses any source mesh whose "
            "volume is negative. Per-object closure is gated on the authored "
            "export in validation.json."
        )
    results["overall"] = "PASS" if all(results["checks"].values()) else "FAIL"

    with open(output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        f.write("\n")

    summary = {
        k: results[k]
        for k in (
            "asset", "object_count", "triangle_count", "dimensions_m", "min_y_m",
            "xz_center_offset_m", "front_face_direction", "wheel_gauge_m",
            "open_shell_objects", "inverted_or_zero_volume_objects",
            "off_palette_warnings", "materials", "checks", "overall",
        )
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
