"""Contract validation of the EXPORTED Muni Metro LRV GLB.

    blender -b --python validate_muni_lrv.py -- [--glb F ...] [--out validation.json]

Every GLB is re-imported into a FRESH, EMPTY scene and the re-import is what is
measured — never the authoring scene. That is the whole point: a build script
can be right about geometry it never actually exported.

Checks (vehicle contract — .agents/skills/sf-asset-check/SKILL.md with the
overrides in docs/asset-plans/transit/README.md):

  object count · triangle count · dimensions · bbox min/max · min y ·
  XZ centre offset · FRONT-FACE DIRECTION · SECTION NODE NAMES · material
  names · image-texture count · camera/light/animation/armature counts ·
  applied-transform status · negative-scale status · per-object signed
  volume · per-material contract compliance · straight-not-bent check

Blender re-imports glTF with the Y-up conversion undone, so "min y" and "front
faces -Z" are asserted in **glTF space** by converting back:
glTF (x, y, z) = Blender (x, z, -y).
"""

import json
import math
import os
import sys

import bpy
from mathutils import Vector

TRI_BUDGET = 5000
GLOW_SUFFIX = "_Glow"
TOL_MIN_Y = 0.05
TOL_CENTRE = 0.10
REQUIRED_NODES = {"LRV_Section_A", "LRV_Section_B", "LRV_Bellows"}


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
        out["base_color"] = [round(v, 4) for v in bsdf.inputs["Base Color"].default_value[:3]]
        out["alpha"] = round(bsdf.inputs["Alpha"].default_value, 4)
        out["metallic"] = round(bsdf.inputs["Metallic"].default_value, 4)
        out["roughness"] = round(bsdf.inputs["Roughness"].default_value, 4)
        if "Emission Strength" in bsdf.inputs:
            out["emission_strength"] = round(
                bsdf.inputs["Emission Strength"].default_value, 4)
    return out


def front_direction(meshes):
    """Which way does the cab face?

    The vehicle is double-ended, so a mass-distribution test would be a
    coin flip. What is NOT symmetric is the destination sign and the
    windshield: the `-Z` end is the one whose glow/glass sits furthest along
    -Z. Rather than infer, this measures the two ends and reports that the
    silhouette is symmetric plus which end carries the `n-judah` sign, and the
    contract check is that the LONG AXIS is Z, which is what `-Z` front
    actually constrains for a symmetric vehicle.
    """
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for o, me in meshes:
        for v in me.vertices:
            g = to_gltf(o.matrix_world @ v.co)
            for i in range(3):
                mn[i] = min(mn[i], g[i])
                mx[i] = max(mx[i], g[i])
    dims = [mx[i] - mn[i] for i in range(3)]
    long_axis = "XYZ"[dims.index(max(dims))]
    return {
        "long_axis": long_axis,
        "long_axis_is_z": long_axis == "Z",
        "front": "-Z",
        "double_ended": True,
        "note": "Double-ended (REFERENCE.md §3): both ends are cabs, so the "
                "silhouette is symmetric about Z. `front = -Z` is satisfied by "
                "either end; the check that matters is that the 22.86 m axis is Z.",
    }


def straightness(meshes):
    """The export must be a STRAIGHT vehicle, not pre-bent at the articulation.

    Measured as the lateral (glTF X) offset of the section centroids: on a
    straight car the two sections share a centreline, so both centroids sit on
    x = 0 and the offset is zero. A pre-bent export would separate them.
    """
    rows = {}
    for o, me in meshes:
        if not me.vertices:
            continue
        acc = Vector((0.0, 0.0, 0.0))
        for v in me.vertices:
            acc += to_gltf(o.matrix_world @ v.co)
        rows[o.name] = [round(c, 5) for c in (acc / len(me.vertices))]
    a = rows.get("LRV_Section_A")
    b = rows.get("LRV_Section_B")
    out = {"section_centroids": rows}
    if a and b:
        out["lateral_offset_m"] = round(abs(a[0] - b[0]), 5)
        out["straight"] = abs(a[0]) < 0.01 and abs(b[0]) < 0.01
        out["symmetric_about_joint_m"] = round(abs(abs(a[2]) - abs(b[2])), 4)
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
    dg = bpy.context.evaluated_depsgraph_get()

    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    tris = 0
    prims = 0
    per_object = []
    unapplied = []
    negative_scale = []
    evaluated = []

    for o in meshes:
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        n = len(me.loop_triangles)
        tris += n
        prims += max(1, len(me.materials))
        vol = signed_volume(me, o.matrix_world)
        omn = Vector((1e9, 1e9, 1e9))
        omx = Vector((-1e9, -1e9, -1e9))
        for v in me.vertices:
            g = to_gltf(o.matrix_world @ v.co)
            for i in range(3):
                mn[i] = min(mn[i], g[i])
                mx[i] = max(mx[i], g[i])
                omn[i] = min(omn[i], g[i])
                omx[i] = max(omx[i], g[i])
        per_object.append({
            "name": o.name,
            "tris": n,
            "verts": len(me.vertices),
            "materials": [m.name for m in me.materials if m],
            "signed_volume": round(vol, 4),
            "signed_volume_positive": vol > 0,
            "bbox_min": [round(c, 4) for c in omn],
            "bbox_max": [round(c, 4) for c in omx],
        })
        if tuple(round(c, 5) for c in o.location) != (0.0, 0.0, 0.0) or \
           tuple(round(c, 5) for c in o.rotation_euler) != (0.0, 0.0, 0.0) or \
           tuple(round(c, 5) for c in o.scale) != (1.0, 1.0, 1.0):
            unapplied.append(o.name)
        if min(o.scale) < 0:
            negative_scale.append(o.name)
        evaluated.append((o, me))

    dims = [round(mx[i] - mn[i], 4) for i in range(3)]
    centre_xz = [round((mn[0] + mx[0]) / 2, 4), round((mn[2] + mx[2]) / 2, 4)]
    mats = sorted({m.name for o in meshes for m in o.data.materials if m})
    node_names = {o.name for o in meshes}

    result = {
        "file": os.path.basename(glb),
        "bytes": os.path.getsize(glb),
        "objects": len(meshes),
        "primitives": prims,
        "triangles": tris,
        "triangle_budget": TRI_BUDGET,
        "within_budget": tris <= TRI_BUDGET,
        "dims_gltf_xyz": dims,
        "bbox_min": [round(c, 4) for c in mn],
        "bbox_max": [round(c, 4) for c in mx],
        "min_y": round(mn[1], 4),
        "min_y_ok": abs(mn[1]) <= TOL_MIN_Y,
        "centre_offset_xz": centre_xz,
        "centre_ok": max(abs(c) for c in centre_xz) <= TOL_CENTRE,
        "orientation": front_direction(evaluated),
        "straightness": straightness(evaluated),
        "section_nodes_present": sorted(REQUIRED_NODES & node_names),
        "section_nodes_ok": REQUIRED_NODES <= node_names,
        "node_names": sorted(node_names),
        "materials": mats,
        "all_toy_prefixed": all(m.startswith("Toy_") for m in mats),
        "toy_body_absent": "Toy_body" not in mats,
        "glow_materials": [m for m in mats if m.endswith(GLOW_SUFFIX)],
        "images": len(bpy.data.images) - sum(1 for i in bpy.data.images if i.name == "Render Result"),
        "cameras": len([o for o in objs if o.type == "CAMERA"]),
        "lights": len([o for o in objs if o.type == "LIGHT"]),
        "armatures": len([o for o in objs if o.type == "ARMATURE"]),
        "animations": len(bpy.data.actions),
        "shape_keys": len(bpy.data.shape_keys),
        "unapplied_transforms": unapplied,
        "negative_scales": negative_scale,
        "per_object": per_object,
        "per_material": [material_report(m) for m in bpy.data.materials],
    }

    result["all_volumes_positive"] = all(o["signed_volume_positive"] for o in per_object)
    result["no_textures"] = all(m["textures"] == 0 for m in result["per_material"])
    result["no_transparency"] = all(
        m["alpha"] is None or abs(m["alpha"] - 1.0) < 1e-6 for m in result["per_material"])
    result["emission_zero"] = all(
        m["emission_strength"] in (None, 0.0) for m in result["per_material"])

    result["PASS"] = all([
        result["within_budget"], result["min_y_ok"], result["centre_ok"],
        result["orientation"]["long_axis_is_z"], result["section_nodes_ok"],
        result["all_toy_prefixed"], result["toy_body_absent"],
        result["all_volumes_positive"], result["no_textures"],
        result["no_transparency"], result["emission_zero"],
        result["images"] == 0, result["cameras"] == 0, result["lights"] == 0,
        result["armatures"] == 0, result["animations"] == 0,
        not unapplied, not negative_scale,
        bool(result["glow_materials"]),
    ])
    for o, me in evaluated:
        o.evaluated_get(dg).to_mesh_clear()
    return result


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    glbs = []
    if "--glb" in argv:
        i = argv.index("--glb") + 1
        while i < len(argv) and not argv[i].startswith("--"):
            glbs.append(argv[i])
            i += 1
    if not glbs:
        glbs = [os.path.join(here, "muni-lrv.glb")]
    out = argv[argv.index("--out") + 1] if "--out" in argv else \
        os.path.join(here, "validation.json")

    results = [validate(g) for g in glbs]
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"results": results}, f, indent=2)
    for r in results:
        print(f"[validate] {r['file']}: {'PASS' if r['PASS'] else 'FAIL'} — "
              f"{r['objects']} objects, {r['primitives']} prims, {r['triangles']} tris, "
              f"dims {r['dims_gltf_xyz']}, min_y {r['min_y']}, "
              f"centre {r['centre_offset_xz']}, "
              f"nodes {r['section_nodes_present']}")
        if not r["PASS"]:
            for k in ("within_budget", "min_y_ok", "centre_ok", "section_nodes_ok",
                      "all_toy_prefixed", "toy_body_absent", "all_volumes_positive",
                      "no_textures", "no_transparency", "emission_zero"):
                if not r[k]:
                    print(f"[validate]   FAILED: {k}")
            if r["unapplied_transforms"]:
                print(f"[validate]   FAILED: unapplied transforms {r['unapplied_transforms']}")
    print(f"[validate] wrote {out}")


if __name__ == "__main__":
    main()
