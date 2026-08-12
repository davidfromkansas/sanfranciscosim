"""Contract validation of the EXPORTED Muni bus GLBs.

    blender -b --python validate_muni_bus.py -- [--glb F ...] [--out validation.json]

Every GLB is re-imported into a FRESH, EMPTY scene and the re-import is what is
measured — never the authoring scene. That is the whole point: a build script
can be right about geometry it never actually exported.

Checks (vehicle contract — .agents/skills/sf-asset-check/SKILL.md with the
overrides in docs/asset-plans/transit/README.md):

  object count · triangle count · dimensions · bbox min/max · min y ·
  XZ centre offset · FRONT-FACE DIRECTION · material names · image-texture
  count · camera count · light count · animation count · applied-transform
  status · negative-scale status · per-object signed volume ·
  per-material contract compliance (flat, opaque, no textures, emission 0)

Blender re-imports glTF with the Y-up conversion undone, so "min y" and "front
faces -Z" are asserted in **glTF space** by converting back: glTF (x, y, z) =
Blender (x, z, -y). `glb_inspect.mjs` reads the same quantities straight out of
the raw buffers as an independent second opinion.
"""

import json
import math
import os
import sys

import bpy
from mathutils import Vector

TRI_BUDGET = 3000
GLOW_SUFFIX = "_Glow"
# The vehicle contract's tolerances.
TOL_MIN_Y = 0.05
TOL_CENTRE = 0.10


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
            out["emission_strength"] = round(bsdf.inputs["Emission Strength"].default_value, 4)
    return out


def validate(glb):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.data.scenes.new("Validate")
    bpy.context.window.scene = scene
    for s in list(bpy.data.scenes):
        if s is not scene:
            bpy.data.scenes.remove(s)
    bpy.ops.import_scene.gltf(filepath=glb)

    objs = [o for o in bpy.context.scene.objects]
    meshes = [o for o in objs if o.type == "MESH"]
    cams = [o for o in objs if o.type == "CAMERA"]
    lights = [o for o in objs if o.type == "LIGHT"]
    armatures = [o for o in objs if o.type == "ARMATURE"]

    dg = bpy.context.evaluated_depsgraph_get()
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
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
        for v in me.vertices:
            w = o.matrix_world @ v.co
            g = to_gltf(w)
            for i in range(3):
                mn[i] = min(mn[i], g[i])
                mx[i] = max(mx[i], g[i])
                omn[i] = min(omn[i], g[i])
                omx[i] = max(omx[i], g[i])
        ev.to_mesh_clear()

        loc, _rot, scl = o.matrix_world.decompose()
        if any(abs(s - 1.0) > 1e-4 for s in scl) or loc.length > 1e-4:
            unapplied.append(o.name)
        if scl.x * scl.y * scl.z < 0:
            negative_scale.append(o.name)
        per_object.append({
            "name": o.name,
            "materials": [m.name for m in o.data.materials if m],
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

    # FRONT-FACE DIRECTION, measured rather than asserted: the headlight glow is
    # only ever on the nose, so whichever end of Z it sits on IS the front.
    front = None
    head = next((o for o in per_object if "white_Glow" in " ".join(o["materials"])), None)
    if head:
        front = "-Z" if (head["gltf_min"][2] + head["gltf_max"][2]) / 2 < 0 else "+Z"

    checks = {
        "front_faces_minus_z": front == "-Z",
        "min_y_zero": abs(mn[1]) <= TOL_MIN_Y,
        "centred_in_xz": max(abs(centre_xz[0]), abs(centre_xz[1])) <= TOL_CENTRE,
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
        "emission_zero": all(
            m["emission_strength"] in (None, 0.0) for m in mat_reports
        ),
        "no_toy_body": "Toy_body" not in mats,
        "glow_materials_present": any(m["glow"] for m in mat_reports),
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
    """Blender's cwd is the shell's, so relative --glb args must be resolved
    before the importer sees them or it reports 'Please select a file'."""
    return p if os.path.isabs(p) else os.path.abspath(p)


def _take(argv, flag):
    """Args after `flag` up to the next `--option`. Consuming to the end of the
    list swallows the following flag's VALUE — which arrives here as a directory
    path and makes the glTF importer report "Please select a file"."""
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
    out = _abspath(argv[argv.index("--out") + 1]) if "--out" in argv else os.path.join(here, "validation.json")

    results = [validate(f) for f in files]
    payload = {
        "asset": "muni-bus-40",
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
              f"front={r['front_face_direction']}")
        for k, v in r["checks"].items():
            if not v:
                print(f"[validate]     FAILED CHECK: {k}")
    print(f"[validate] wrote {out}")


if __name__ == "__main__":
    main()
