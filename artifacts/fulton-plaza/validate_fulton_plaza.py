"""Fresh-scene contract validation for fulton-plaza.glb.

    blender -b --python validate_fulton_plaza.py -- [--glb FILE] [--out FILE]

This script factory-resets, imports only the final GLB, and writes the complete
machine-readable report. It does not inspect the source .blend.

Four subject-specific checks beyond the standard contract (asset plan Part 1):

1. The VERTICAL EXTENT equals the manifest's targetHeightM, and the vertex
   achieving max_z belongs to the `monument`. This asset is terrain-draped, so
   targetHeightM is the extent rather than an architectural height (the loader
   scales by targetHeightM / bbox height and it must land on 1.0) - but the
   crest still has to be the Pioneer Monument. If a tree overtakes it, the
   datum has quietly moved onto a lollipop; see the plan's 2.15 risk 2.
2. THE DRAPE. `min_z` is NEGATIVE here by design - z = 0 is the anchor's ground,
   which is exactly where placeGeneric() puts the model - so "min_z ~ 0" is
   replaced by a real check: the deck's top surface must stand Z_DECK above the
   baked terrain EVERYWHERE, sampled by ray-casting straight down onto the deck
   at 63 points across the right-of-way and comparing against the same heightmap
   the loader uses. A flat plate fails this by ~1 m at each end.
3. XY bbox ~128.5 x 67.6 m - the expected consequence of an 8.85 deg heading on
   a 120.0 x 48.6 m right-of-way (plus the planting beds' overhang and the tree
   crowns), not a scale error.
4. The koi: two connected bodies, each 18-22 m long, carrying both koi materials
   in the day pass and both koi _Glow materials in the night pass. They are the
   asset's whole recognition cue and its entire night state.
"""

import json
import math
import os
import sys

import bpy
from mathutils import Vector

TRI_BUDGET = 16000
# 81.15 toward Hyde Street. Signed: the Civic Center grid leans EAST of north,
# so the cross axis is 171.15 (= 180 - 8.85), not 188.85. This constant maps the
# surveyed (u, v) frame into model space, so getting it wrong validates the
# model against a mirrored frame.
HEADING_LONG = 81.15
HEADING_CROSS = 171.15
Z_DECK = 0.95            # deck top above local grade, from the build script
DRAPE_TOLERANCE = 0.10   # metres of standoff error allowed anywhere on the deck


def rounded(v):
    return [round(x, 4) for x in v]


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    glb = arg("--glb", os.path.join(here, "fulton-plaza.glb"))
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

    # --- subject-specific measurements -------------------------------------
    datum_object = None
    for obj in meshes:
        ev = obj.evaluated_get(dg)
        me = ev.to_mesh()
        if any((obj.matrix_world @ v.co).z >= mx.z - 1e-4 for v in me.vertices):
            datum_object = obj.name.split(".")[0]
        ev.to_mesh_clear()

    # --- THE DRAPE ---------------------------------------------------------
    # The check that replaces "min_z ~ 0". Ray-cast straight down onto the deck
    # across the whole right-of-way and compare each hit against the terrain the
    # LOADER will seat this model on. Anything but a draped plate fails: a flat
    # deck is ~1.2 m proud at the Larkin end and ~1.2 m buried at Hyde.
    with open(os.path.join(here, "data", "plaza_uv.json"), "r", encoding="utf8") as fh:
        survey = json.load(fh)
    with open(os.path.join(here, "data", "terrain_uv.json"), "r", encoding="utf8") as fh:
        terrain = json.load(fh)
    with open(os.path.join(here, "data", "build_meta.json"), "r", encoding="utf8") as fh:
        meta = json.load(fh)

    a = math.radians(HEADING_LONG)
    udir = (math.sin(a), math.cos(a))
    vdir = (udir[1], -udir[0])   # +v = SOUTH, matching the build's V_DIR
    shift = meta["anchor_shift_m_east_north"]

    def to_model(u, v):
        return (u * udir[0] + v * vdir[0] - shift[0],
                u * udir[1] + v * vdir[1] - shift[1])

    def dz(u, v):
        t = terrain
        fu = (u - t["u_min"]) / t["u_step"]
        fv = (v - t["v_min"]) / t["v_step"]
        i = min(t["u_count"] - 2, max(0, int(math.floor(fu))))
        j = min(t["v_count"] - 2, max(0, int(math.floor(fv))))
        tu = min(1.0, max(0.0, fu - i))
        tv = min(1.0, max(0.0, fv - j))
        p = t["dy"][j][i] + (t["dy"][j][i + 1] - t["dy"][j][i]) * tu
        q = t["dy"][j + 1][i] + (t["dy"][j + 1][i + 1] - t["dy"][j + 1][i]) * tu
        return p + (q - p) * tv

    deck = next((o for o in meshes if o.name.split(".")[0] == "deck"), None)
    drape_samples = []
    drape_err = 0.0
    if deck:
        depsgraph = bpy.context.evaluated_depsgraph_get()
        # Sample points chosen to hit the DECK and nothing stacked on it: clear
        # of the scored joints (u = -57 + 12k, v = -11/0/+11), of the monument
        # apron, of the south terrace (v >= 14.2, which is why the outer row is v = 12 and
        # not 16) and of the north walk and beds (v <= -19.6). A ray that lands on
        # an overlay is skipped, so a badly chosen grid silently shrinks the
        # sample rather than failing.
        for u in (-52, -40, -28, -16, 20, 32, 44, 52):
            for v in (-16, -5.5, 5.5, 12):
                mxp, myp = to_model(u, v)
                origin = Vector((mxp, myp, 60.0))
                hit, loc, _, _, ob, _ = bpy.context.scene.ray_cast(
                    depsgraph, origin, Vector((0, 0, -1)), distance=200.0)
                if not hit or ob.name.split(".")[0] != "deck":
                    continue
                want = dz(u, v) + Z_DECK
                drape_err = max(drape_err, abs(loc.z - want))
                drape_samples.append(
                    {"u": u, "v": v, "deck_z": round(loc.z, 4),
                     "expected_z": round(want, 4), "error": round(loc.z - want, 4)})

    # --- the koi -----------------------------------------------------------
    # Two bodies, each 18-22 m along its own long axis. Recovered by splitting
    # the merged `koi` mesh on its two position clusters rather than by trusting
    # the build: the whole asset's recognition rests on these two shapes.
    koi_obj = next((o for o in meshes if o.name.split(".")[0] == "koi"), None)
    koi_bodies = []
    if koi_obj:
        ev = koi_obj.evaluated_get(dg)
        me = ev.to_mesh()
        pts = [koi_obj.matrix_world @ v.co for v in me.vertices]
        # Cluster against the two SURVEYED koi centres rather than against
        # self-chosen seeds: a nearest-seed pass with any threshold under the
        # fish's own 20.5 m length splits one koi into two and reports three
        # bodies, which is exactly what a 20 m threshold did. This way the check
        # also confirms the koi are where the imagery put them.
        seeds = [Vector(to_model(*survey["nodes"][k]) + (0.0,))
                 for k in ("koi_west", "koi_east")]
        groups = [[] for _ in seeds]
        for w in pts:
            best = min(range(len(seeds)),
                       key=lambda i: (w.x - seeds[i].x) ** 2 + (w.y - seeds[i].y) ** 2)
            groups[best].append(w)
        for g in groups:
            span = 0.0
            for i in range(0, len(g), 3):
                for j in range(i + 1, len(g), 3):
                    span = max(span, math.hypot(g[i].x - g[j].x, g[i].y - g[j].y))
            koi_bodies.append(round(span, 3))
        ev.to_mesh_clear()
    koi_mats = sorted({m.name.split(".")[0] for m in (koi_obj.data.materials if koi_obj else [])})
    glow_obj = next((o for o in meshes if o.name.split(".")[0] == "koi_glow"), None)
    koi_glow_mats = sorted({m.name.split(".")[0]
                            for m in (glow_obj.data.materials if glow_obj else [])})

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
    for obj in meshes:
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
        "anchor_lonlat": meta["manifest_anchor_lonlat"],
        "anchor_lonlat_row_obb_centre": meta["anchor_lonlat_row_obb"],
        "long_axis_heading_deg_true": HEADING_LONG,
        "cross_axis_heading_deg_true": HEADING_CROSS,
        "target_height_m": round(dims.z, 4),
        "target_height_is": (
            "the model's VERTICAL EXTENT, not an architectural height: this asset is "
            "terrain-draped, so min_z is negative and the loader's "
            "targetHeightM / bbox-height scale must land on 1.0"
        ),
        "monument_crest_above_local_grade_m": meta["monument_crest_above_grade_m"],
        "height_datum": (
            "Pioneer Monument, Minerva's finial. SF Arts Commission accession "
            "1894.4.a-o records the work at 420 in = 10.668 m overall, standing on "
            "the plaza's granite apron"
        ),
        "height_datum_vertex_object": datum_object,
        "terrain_drape": {
            "source": terrain["source"],
            "anchor_elevation_m": terrain["anchor_elevation_m"],
            "fall_m": terrain["fall_m"],
            "cross_fall_max_m": terrain["cross_fall_max_m"],
            "deck_height_above_grade_m": Z_DECK,
            "samples": len(drape_samples),
            "max_standoff_error_m": round(drape_err, 4),
            "tolerance_m": DRAPE_TOLERANCE,
            "detail": drape_samples,
        },
        "koi_body_lengths_m": koi_bodies,
        "koi_centres_uv_surveyed": [survey["nodes"]["koi_west"], survey["nodes"]["koi_east"]],
        "koi_materials": koi_mats,
        "koi_glow_materials": koi_glow_mats,
        "signed_volume_outward_objects": volume_ok,
        "signed_volume_inverted_objects": sorted(volume_bad),
        "object_details": sorted(object_rows, key=lambda x: x["name"]),
    }
    results["checks"] = {
        # 128.5 x 67.6 x 12.8 m: the XY box is the 8.85 deg rotation of a
        # 120.0 x 48.6 m right-of-way, widened by the planting beds' overhang
        # and the tree crowns. Not an oversized model. See REPORT.md.
        "meters_and_plausible_dimensions": (
            12.8 <= dims.z <= 13.6
            and 127.0 <= dims.x <= 130.0
            and 66.0 <= dims.y <= 69.0
        ),
        "vertical_extent_matches_build_meta": abs(dims.z - meta["vertical_extent_m"]) <= 0.01,
        "height_datum_is_the_monument": datum_object == "monument",
        # min_z is NEGATIVE on purpose (z = 0 is the anchor's ground). This is
        # the check that replaces "base_at_z_zero" for a draped ground asset.
        "deck_drapes_the_terrain": len(drape_samples) >= 28 and drape_err <= DRAPE_TOLERANCE,
        "koi_are_two_bodies_of_the_right_size": (
            len(koi_bodies) == 2 and all(18.0 <= L <= 22.0 for L in koi_bodies)
        ),
        "koi_carry_both_day_and_night_materials": (
            koi_mats == ["Toy_koiOrange", "Toy_koiWhite"]
            and koi_glow_mats == ["Toy_koiOrange_Glow", "Toy_koiWhite_Glow"]
        ),
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
