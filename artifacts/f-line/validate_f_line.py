"""Fresh-scene contract validation for the F-line PCC GLB.

    blender -b --python validate_f_line.py -- [--glb FILE] [--out FILE]
                                              [--stage authored|shipped]

Factory-resets, imports only the GLB, and writes the machine-readable report.
It never inspects the source .blend.

REPORTING SPACE.  Blender's glTF importer converts the file's Y-up axes back to
Z-up, so this scene's +Y is the file's -Z.  Every geometric figure below is
converted back into glTF/three space before it is reported -

    (gx, gy, gz) = (bx, bz, -by)

- because that is the space `app/src/agents.js` and `vehicles_manifest.json`
speak: front -Z, up +Y, wheels at min y = 0.

THIS ASSET INVERTS ONE GATE.  Every other vehicle and landmark in the repo is
checked for the ABSENCE of `Toy_body`; the F-line PCC is checked for its
PRESENCE, because the cities-series liveries are delivered by per-instance
tinting of that one material (historic-streetcar.md s.2.6).  If `Toy_body`
vanishes - merged away by the shrink pass or by gltfpack without `-km` - every
PCC in the city becomes one colour and the failure is silent.  Hence
`toy_body_present_and_addressable`, gated at BOTH stages.

THE OTHER HARD GATE is per-object signed volume.  A vehicle is a union of
solids and `mergeVehicle()` in agents.js REVERSES any source mesh whose signed
volume is negative, so a negative part ships inside out.
"""

import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

TRI_BUDGET = 4000
PUBLISHED_L = 14.76     # 48 ft 5 in, Muni 1050 class
PUBLISHED_W = 2.54      # 8 ft 4 in
PUBLISHED_H = 3.124     # 10 ft 3 in, rail to roof crown (the trolley pole is above it)
GAUGE = 1.435           # standard gauge

# `Toy_body` is this asset's sanctioned exception, not a violation.
TINTABLE = "Toy_body"

PALETTE_KEYS = {
    "cream", "sand", "trim", "teal", "coral", "mustard", "mint", "sky", "navy",
    "glass", "glassl", "ink", "roofd", "brick", "stone", "red", "steel", "rust",
    "gold", "ioorange", "verdigris", "white",
}

# Which surfaces the livery tint is allowed to own.  Recorded so a later
# session can prove the split did not drift: the shell is the ONLY object that
# may carry Toy_body, and it must also carry the fixed trim materials.
TINTED_OBJECT = "body_shell"


def rounded(v, n=4):
    return [round(x, n) for x in v]


def to_gltf(v):
    """Blender (x, y, z) -> glTF (x, z, -y)."""
    return Vector((v.x, v.z, -v.y))


def signed_volume(mesh, matrix):
    """Divergence-theorem volume of the world-space mesh.  Positive means the
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
    normal and this asset is shaded flat, so a re-imported cube arrives as six
    topologically disconnected quads.  Testing the raw import reports every
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

    glb = arg("--glb", os.path.join(here, "f-line-pcc.authored.glb"))
    output = arg("--out", os.path.join(here, "validation.json"))
    # "authored" = straight out of build_f_line.py, where every component is
    # still its own object and per-object closure means something.  "shipped" =
    # after the shrink's join-by-material step, where closure is structurally
    # inapplicable and is reported as an observation instead
    # (docs/asset-plans/transit/README.md Part 3 step 5 asks for that join).
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
    wheel_x = []
    body_extent = None

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
        # Gauge is measured from the WHEEL OBJECTS, not from a material extent:
        # the wheels share Toy_roofd with the roof ventilators and the drip
        # rails, whose X extent is the whole car.
        if obj.name.split(".")[0].startswith("wheel_"):
            wheel_x.append((omn.x + omx.x) / 2)
        if obj.name.split(".")[0] == TINTED_OBJECT:
            body_extent = (omn.copy(), omx.copy())
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
                "materials": sorted({m.name for m in me.materials if m}),
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
        base = None
        if mat.use_nodes:
            tex = [n.name for n in mat.node_tree.nodes if n.type == "TEX_IMAGE"]
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                alpha = float(bsdf.inputs["Alpha"].default_value)
                roughness = float(bsdf.inputs["Roughness"].default_value)
                emission = float(bsdf.inputs["Emission Strength"].default_value)
                c = bsdf.inputs["Base Color"].default_value
                base = "#" + "".join(
                    f"{round(255 * (1.055 * (v ** (1 / 2.4)) - 0.055 if v > 0.0031308 else 12.92 * v)):02x}"
                    for v in c[:3]
                )
        if tex:
            textured.append(mat.name)
        if alpha < 0.999:
            transparent.append(mat.name)
        if not mat.name.startswith("Toy_"):
            off_contract.append(mat.name)
        key = mat.name[len("Toy_") :].replace("_Glow", "")
        if mat.name.startswith("Toy_") and key != "body" and key not in PALETTE_KEYS:
            off_palette_warn.append(mat.name)
        mat_rows.append(
            {
                "name": mat.name,
                "base_color_hex": base,
                "image_texture_nodes": tex,
                "alpha": round(alpha, 4),
                "roughness": round(roughness, 4) if roughness is not None else None,
                "emission_strength": round(emission, 4) if emission is not None else None,
                "glow": mat.name.endswith("_Glow"),
                "tintable": mat.name == TINTABLE,
            }
        )

    material_names = sorted(m.name for m in bpy.data.materials)

    # ------------------------------------------------------------- orientation
    # Front = the cab end.  Two independent asymmetries prove it, reported in
    # glTF space where the front must be -Z: the headlight glow sits at the
    # extreme front, and the mustard route board sits behind it (the interior
    # strips share that material, so the test is on the board's LEADING edge).
    def gz_range(mat_name):
        ext = material_extent.get(mat_name)
        if not ext:
            return None
        # glTF z = -Blender y, so a Blender y range maps to a flipped z range.
        return [round(-ext[1], 3), round(-ext[0], 3)]

    lamp_gz = gz_range("Toy_white_Glow")
    tail_gz = gz_range("Toy_red_Glow")
    gmn, gmx = to_gltf(bmn), to_gltf(bmx)
    gmn, gmx = (
        Vector((min(gmn.x, gmx.x), min(gmn.y, gmx.y), min(gmn.z, gmx.z))),
        Vector((max(gmn.x, gmx.x), max(gmn.y, gmx.y), max(gmn.z, gmx.z))),
    )
    dims = gmx - gmn
    center = Vector(((gmn.x + gmx.x) / 2, (gmn.y + gmx.y) / 2, (gmn.z + gmx.z) / 2))
    front_is_neg_z = bool(
        lamp_gz and tail_gz and lamp_gz[0] < gmn.z + 0.30 and tail_gz[0] > lamp_gz[1]
    )

    measured_gauge = None
    if wheel_x:
        measured_gauge = round(max(wheel_x) - min(wheel_x), 4)

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

    tinted_objects = sorted(
        r["name"] for r in object_rows if TINTABLE in r["materials"]
    )
    tinted_tris = sum(r["triangles"] for r in object_rows if TINTABLE in r["materials"])

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
        "published_height_note": (
            "Published height 3.124 m is rail to the top of the roof crown. The "
            "model's bbox y is taller because the trolley pole and the roof "
            "ventilators stand above the crown; body_height_m below is the "
            "figure to compare against the published one."
        ),
        "body_height_m": round(body_extent[1].z, 4) if body_extent else None,
        "bbox_min_m": rounded(gmn, 4),
        "bbox_max_m": rounded(gmx, 4),
        "min_y_m": round(gmn.y, 4),
        "min_y_represents": (
            "the WHEEL CONTACT PATCH, i.e. the top of rail. This scene contains "
            "no rails (docs/asset-plans/transit/README.md, the no-rails-no-wires "
            "decision), so top of rail coincides with the street surface and the "
            "car grounds exactly like a bus - it sits one rail-head lower "
            "relative to the pavement than a real streetcar would."
        ),
        "xz_center_offset_m": [round(center.x, 4), round(center.z, 4)],
        "front_face_direction": "-Z" if front_is_neg_z else "UNPROVEN",
        "front_face_evidence": {
            "headlight_glow_z_range_m": lamp_gz,
            "taillight_glow_z_range_m": tail_gz,
            "test": "single central headlight at the -Z extreme; tail lights entirely behind it",
        },
        "wheel_gauge_m": measured_gauge,
        "wheel_gauge_expected_m": GAUGE,
        "wheel_object_count": len(wheel_x),
        "materials": material_names,
        "material_details": sorted(mat_rows, key=lambda x: x["name"]),
        "tintable_material": TINTABLE,
        "tintable_present": TINTABLE in material_names,
        "tintable_objects": tinted_objects,
        "tintable_triangle_count": tinted_tris,
        "tintable_note": (
            "app/src/kitfleet.js multiplies a per-instance colour into this "
            "material's authored #d8d3c8. Everything NOT on this material - "
            "roof, glazing, reveals, trucks, wheels, pole, anti-climbers, "
            "headlight, route board - is fixed, so a tint cannot wash the trim "
            "out. Requires the kitfleet.js tinting path to be ported into "
            "agents.js; see REPORT.md."
        ),
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
        "glow_materials": sorted(m for m in material_names if m.endswith("_Glow")),
        "off_palette_warnings": sorted(off_palette_warn),
        "material_contract_violations": sorted(off_contract),
        "unexpected_geometry_or_objects": unexpected,
        "object_details": sorted(object_rows, key=lambda x: x["name"]),
    }

    per_object_checks = {
        "every_object_is_a_closed_solid": not open_objects,
        "every_object_signed_volume_positive": not inverted_objects,
        "tint_confined_to_the_body_shell": tinted_objects == [TINTED_OBJECT],
        "eight_wheels": len(wheel_x) == 8,
        # Gauge is measured from the wheel OBJECTS, so like closure it is only
        # meaningful before the shrink pass joins them into a per-material
        # group. Gated on the authored export; reported as an observation on
        # the shipped one.
        "standard_gauge_wheels": measured_gauge is not None
        and abs(measured_gauge - GAUGE) <= 0.02,
    }
    results["stage"] = stage
    results["checks"] = {
        "meters_and_published_dimensions": (
            abs(dims.z - PUBLISHED_L) <= 0.02
            and dims.x <= PUBLISHED_W + 0.05
            and (body_extent is None or abs(body_extent[1].z - PUBLISHED_H) <= 0.05)
        ),
        "ground_at_min_y_zero": abs(gmn.y) <= 0.05,
        "centered_in_xz_footprint": abs(center.x) <= 0.10 and abs(center.z) <= 0.10,
        "front_faces_minus_z": front_is_neg_z,
        "under_triangle_budget": tris <= TRI_BUDGET,
        "no_image_textures": not bpy.data.images and not textured,
        "no_transparency": not transparent,
        "materials_follow_contract": not off_contract,
        # INVERTED for this asset: Toy_body must be PRESENT and separately
        # addressable, or the entire cities-series livery design is dead.
        "toy_body_present_and_addressable": TINTABLE in material_names,
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
        "glow_set_complete": sorted(results["glow_materials"])
        == ["Toy_mustard_Glow", "Toy_red_Glow", "Toy_white_Glow"],
    }
    if stage == "authored":
        results["checks"].update(per_object_checks)
    else:
        results["per_object_observations"] = per_object_checks
        results["per_object_note"] = (
            "Not gated at this stage. The shrink pass joins the authored "
            "objects into per-material groups and deletes provably buried "
            "faces, so a group is a union of solids rather than one closed "
            "solid, and the wheels no longer exist as separate objects. What "
            "still has to hold - and is gated in shrink-stats.json as "
            "merge_vehicle_safe - is that every group's signed volume stays "
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
            "asset", "object_count", "triangle_count", "dimensions_m",
            "body_height_m", "min_y_m", "xz_center_offset_m",
            "front_face_direction", "wheel_gauge_m", "tintable_present",
            "tintable_objects", "open_shell_objects",
            "inverted_or_zero_volume_objects", "off_palette_warnings",
            "materials", "checks", "overall",
        )
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
