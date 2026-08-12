"""Contract validation of the EXPORTED Muni trolley coach GLBs.

    blender -b --python validate_muni_trolley.py -- [--glb F ...] [--out validation.json]

Every GLB is re-imported into a FRESH, EMPTY scene and the re-import is what is
measured — never the authoring scene.

Same checks as `../muni-bus/validate_muni_bus.py`, with three additions this
asset needs and the bus did not:

  * **POLE DIRECTION.** The poles must trail AFT. Measured, not asserted: the
    `Toy_ink` pole shoes are the only ink geometry above the roof crown, so the
    sign of their z against the nose settles it. A coach with its poles leaning
    toward the nose is wrong from every angle and looks fine on a turntable.

  * **FOOTPRINT centring, separately from bbox centring.** The vehicle contract
    says "origin centred in the X/Z **footprint**". The poles are overhead
    structure that never touches the road, so the footprint is the body — and
    the body is what `agents.js` puts on the street path. Both numbers are
    reported; the footprint one is the gate. See REPORT.md §3.

  * **HEIGHT.** ~5.8 m instead of ~3.4 m is correct and intentional for this
    asset, so it is recorded rather than left to be "fixed" later.

Blender re-imports glTF with the Y-up conversion undone, so "min y" and "front
faces -Z" are asserted in **glTF space** by converting back: glTF (x, y, z) =
Blender (x, z, -y). `glb_inspect.mjs` reads the same quantities straight out of
the raw buffers as an independent second opinion.
"""

import json
import os
import sys

import bpy
from mathutils import Vector

TRI_BUDGET = 3400
GLOW_SUFFIX = "_Glow"
TOL_MIN_Y = 0.05
TOL_CENTRE = 0.10
ROOF_CROWN = 3.22       # build cfg z_roof — the top of the body, i.e. the footprint
# Everything above this is unambiguously pole assembly: the tallest roof
# equipment (the HVAC pod's louvres) tops out at 3.42 m, so 4.5 m cannot catch
# it. An earlier draft used the roof crown and silently swept up those louvres,
# which made the aft-trail check read the wrong geometry and fail a correct model.
POLE_ZONE_Y = 4.5


def to_gltf(v):
    """Blender (x, y, z) -> glTF (x, z, -y)."""
    return Vector((v.x, v.z, -v.y))


def signed_volume(mesh, matrix):
    total = 0.0
    mesh.calc_loop_triangles()
    for t in mesh.loop_triangles:
        a, b, c = (matrix @ mesh.vertices[i].co for i in t.vertices)
        total += a.dot(b.cross(c)) / 6.0
    return total


def material_report(mat):
    out = {
        "name": mat.name,
        "glow": mat.name.endswith(GLOW_SUFFIX),
        "prefixed": mat.name.startswith("Toy_"),
        "textures": 0,
        "base_color": None,
        "emission_strength": None,
        "alpha": None,
        "metallic": None,
        "roughness": None,
    }
    if not mat.use_nodes:
        return out
    out["textures"] = sum(1 for n in mat.node_tree.nodes if n.type == "TEX_IMAGE")
    bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf:
        c = bsdf.inputs["Base Color"].default_value
        out["base_color"] = [round(v, 4) for v in c[:3]]
        out["alpha"] = round(bsdf.inputs["Alpha"].default_value, 4)
        out["metallic"] = round(bsdf.inputs["Metallic"].default_value, 4)
        out["roughness"] = round(bsdf.inputs["Roughness"].default_value, 4)
        if "Emission Strength" in bsdf.inputs:
            out["emission_strength"] = round(
                bsdf.inputs["Emission Strength"].default_value, 4)
    return out


def validate(glb):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.data.scenes.new("Validate")
    bpy.context.window.scene = scene
    for s in list(bpy.data.scenes):
        if s is not scene:
            bpy.data.scenes.remove(s)
    bpy.ops.import_scene.gltf(filepath=glb)

    objs = list(bpy.context.scene.objects)
    meshes = [o for o in objs if o.type == "MESH"]
    cams = [o for o in objs if o.type == "CAMERA"]
    lights = [o for o in objs if o.type == "LIGHT"]
    armatures = [o for o in objs if o.type == "ARMATURE"]

    dg = bpy.context.evaluated_depsgraph_get()
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    # Footprint bounds: everything at or below the roof crown, i.e. the body.
    fmn = Vector((1e9, 1e9, 1e9))
    fmx = Vector((-1e9, -1e9, -1e9))
    # glTF z of every vertex in the pole zone, for the aft-trail check, and the
    # set of materials found up there, for the no-glow-at-the-shoe check.
    pole_zone_z = []
    pole_zone_mats = set()
    tris = 0
    per_object = []
    unapplied = []
    negative_scale = []
    for o in meshes:
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        n = len(me.loop_triangles)
        tris += n
        vol = signed_volume(me, o.matrix_world)
        omn = Vector((1e9, 1e9, 1e9))
        omx = Vector((-1e9, -1e9, -1e9))
        mats_here = [m.name for m in o.data.materials if m]
        for v in me.vertices:
            w = o.matrix_world @ v.co
            g = to_gltf(w)
            for i in range(3):
                mn[i] = min(mn[i], g[i])
                mx[i] = max(mx[i], g[i])
                omn[i] = min(omn[i], g[i])
                omx[i] = max(omx[i], g[i])
            if g[1] <= ROOF_CROWN + 1e-4:
                for i in range(3):
                    fmn[i] = min(fmn[i], g[i])
                    fmx[i] = max(fmx[i], g[i])
            if g[1] >= POLE_ZONE_Y:
                pole_zone_z.append(g[2])
                pole_zone_mats.update(mats_here)
        ev.to_mesh_clear()

        loc, _rot, scl = o.matrix_world.decompose()
        if any(abs(s - 1.0) > 1e-4 for s in scl) or loc.length > 1e-4:
            unapplied.append(o.name)
        if scl.x * scl.y * scl.z < 0:
            negative_scale.append(o.name)
        per_object.append({
            "name": o.name,
            "materials": mats_here,
            "triangles": n,
            "signed_volume": round(vol, 5),
            "signed_volume_positive": vol > 0,
            "gltf_min": [round(v, 4) for v in omn],
            "gltf_max": [round(v, 4) for v in omx],
            "constraints": len(o.constraints),
            "vertex_groups": len(o.vertex_groups),
            "shape_keys": bool(o.data.shape_keys),
        })

    mats = sorted({m.name for o in meshes for m in o.data.materials if m})
    mat_reports = [material_report(bpy.data.materials[n]) for n in mats]

    dims = [round(mx[i] - mn[i], 4) for i in range(3)]
    centre_xz = [round((mn[0] + mx[0]) / 2, 4), round((mn[2] + mx[2]) / 2, 4)]
    footprint_centre_xz = [round((fmn[0] + fmx[0]) / 2, 4),
                           round((fmn[2] + fmx[2]) / 2, 4)]
    footprint_dims = [round(fmx[i] - fmn[i], 4) for i in range(3)]

    # FRONT-FACE DIRECTION, measured: the headlight glow only ever sits on the
    # nose, so whichever end of Z it is on IS the front.
    front = None
    head = next((o for o in per_object if "white_Glow" in " ".join(o["materials"])), None)
    if head:
        front = "-Z" if (head["gltf_min"][2] + head["gltf_max"][2]) / 2 < 0 else "+Z"

    # POLE TRAIL: front is -Z, so aft is +Z and every vertex in the pole zone
    # must sit at positive z. If the poles ever lean toward the nose this is the
    # check that catches it.
    poles_trail_aft = bool(pole_zone_z) and min(pole_zone_z) > 0.0

    checks = {
        "front_faces_minus_z": front == "-Z",
        "poles_trail_aft": poles_trail_aft,
        "min_y_zero": abs(mn[1]) <= TOL_MIN_Y,
        "footprint_centred_in_xz": max(abs(footprint_centre_xz[0]),
                                       abs(footprint_centre_xz[1])) <= TOL_CENTRE,
        "triangles_within_budget": tris <= TRI_BUDGET,
        "no_cameras": not cams,
        "no_lights": not lights,
        "no_animations": not bpy.data.actions,
        "no_armatures": not armatures,
        "no_shape_keys": not any(o["shape_keys"] for o in per_object),
        "no_constraints": not any(o["constraints"] for o in per_object),
        "transforms_applied": not unapplied,
        "no_negative_scale": not negative_scale,
        "all_signed_volumes_positive": all(o["signed_volume_positive"] for o in per_object),
        "all_materials_toy_prefixed": all(m["prefixed"] for m in mat_reports),
        "no_image_textures": sum(m["textures"] for m in mat_reports) == 0,
        "no_transparency": all(m["alpha"] in (None, 1.0) for m in mat_reports),
        "emission_zero": all(m["emission_strength"] in (None, 0.0) for m in mat_reports),
        "no_toy_body": "Toy_body" not in mats,
        "glow_materials_present": any(m["glow"] for m in mat_reports),
        # Real trolley shoes spark intermittently; a permanently lit one reads
        # as a rendering bug, so the brief forbids a glow up here.
        "no_glow_in_pole_zone": not any(m.endswith(GLOW_SUFFIX) for m in pole_zone_mats),
        "material_set_matches_hybrid_bus": set(mats) == {
            "Toy_silver", "Toy_white", "Toy_munired", "Toy_ink", "Toy_glass",
            "Toy_steel", "Toy_tire", "Toy_mustard_Glow", "Toy_white_Glow",
            "Toy_red_Glow",
        },
        "one_primitive_per_material": len(meshes) == len(mats),
    }

    return {
        "file": os.path.basename(glb),
        "bytes": os.path.getsize(glb),
        "objects": len(meshes),
        "total_objects_in_scene": len(objs),
        "triangles": tris,
        "triangle_budget": TRI_BUDGET,
        "dims_gltf_xyz": dims,
        "bbox_gltf_min": [round(v, 4) for v in mn],
        "bbox_gltf_max": [round(v, 4) for v in mx],
        "min_y": round(mn[1], 4),
        "centre_offset_xz": centre_xz,
        "footprint_dims_gltf_xyz": footprint_dims,
        "footprint_centre_offset_xz": footprint_centre_xz,
        "pole_zone_z_range": [round(min(pole_zone_z), 4), round(max(pole_zone_z), 4)]
                             if pole_zone_z else None,
        "pole_zone_materials": sorted(pole_zone_mats),
        "front_face_direction": front,
        "materials": mats,
        "material_detail": mat_reports,
        "image_textures": sum(m["textures"] for m in mat_reports),
        "cameras": len(cams),
        "lights": len(lights),
        "animations": len(bpy.data.actions),
        "armatures": len(armatures),
        "objects_with_unapplied_transforms": unapplied,
        "objects_with_negative_scale": negative_scale,
        "per_object": per_object,
        "checks": checks,
        "pass": all(checks.values()),
    }


def _abspath(p):
    return p if os.path.isabs(p) else os.path.abspath(p)


def _take(argv, flag):
    if flag not in argv:
        return []
    out = []
    for a in argv[argv.index(flag) + 1 :]:
        if a.startswith("--"):
            break
        out.append(_abspath(a))
    return out


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    if "--glb" in argv:
        files = _take(argv, "--glb")
    else:
        files = sorted(
            os.path.join(here, f) for f in os.listdir(here) if f.endswith(".glb")
        )
    out = (_abspath(argv[argv.index("--out") + 1]) if "--out" in argv
           else os.path.join(here, "validation.json"))

    results = [validate(f) for f in files]
    payload = {
        "asset": "muni-trolley-40",
        "contract": "vehicle (docs/asset-plans/transit/README.md overrides)",
        "validated": [r["file"] for r in results],
        "all_pass": all(r["pass"] for r in results),
        "results": results,
    }
    with open(out, "w") as fh:
        json.dump(payload, fh, indent=2)

    for r in results:
        status = "PASS" if r["pass"] else "FAIL"
        print(f"[validate] {status}  {r['file']}  objects={r['objects']} "
              f"tris={r['triangles']} dims={r['dims_gltf_xyz']} minY={r['min_y']} "
              f"front={r['front_face_direction']} "
              f"footprintCentre={r['footprint_centre_offset_xz']}")
        for k, v in r["checks"].items():
            if not v:
                print(f"[validate]     FAILED CHECK: {k}")
    print(f"[validate] wrote {out}")


if __name__ == "__main__":
    main()
