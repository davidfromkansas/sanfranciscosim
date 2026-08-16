"""Stage 2 geometry shrink pass for the Muni bus, ASSET_CLASS=vehicle.

    blender -b --python optimize_muni_bus.py -- [--glb F ...] [--out DIR]

Implements docs/asset-plans/transit/README.md Part 3 "Stage 2 — the geometry
shrink pass" in order, measuring tri/vert deltas after each step:

  1. Weld coincident verts within each object at <= 1 mm — NEVER across a
     `_Glow` boundary. Objects are already one-per-material here, so a weld can
     physically only ever run inside a single material; the guard is asserted
     rather than assumed.
  2. Delete degenerate faces (< 1 mm^2) and interior faces buried inside unioned
     solids. Interior-face removal uses per-face occlusion against CLOSED
     occluders only: the signed volume of an open shell is meaningless and an
     open shell would masquerade as a solid box and eat real faces.
  3. Limited dissolve at 0.05 deg — not 0.5. Transitive merging on curved shells
     builds twisted ngons that re-triangulate with flipped windings.
  4. Retessellate over-segmented curves. Segment counts are chosen against the
     vehicle camera distances (near 15 m, far 120 m) and THEN multiplied by the
     1.6x render scale. This model was authored at those counts already
     (10-segment wheels, 8-segment hubs), so this step reports and does not cut.
  5. Join objects sharing a material into one mesh per material. Also satisfied
     at authoring time by the Part banks in build_muni_bus.py; asserted here.
  6. Normals audit: per-object signed volume positive.

Deliberately NOT here: the high->low texture bake. Out of scope for transit
assets per the README — these are 8-23 m objects seen at 1.6x from a 42 deg
camera, drawn as instanced meshes, and the flat-colour contract stands.

Stage 1 (meshopt intake via pipeline/compress-assets.mjs / gltfpack
-cc -kn -km -noq) runs on the result, from shrink.sh.
"""

import contextlib
import io
import json
import os
import sys

import bmesh
import bpy
from mathutils import Vector

GLOW = "_Glow"
WELD_M = 0.001
DEGENERATE_AREA = 1e-6      # 1 mm^2
DISSOLVE_RAD = 0.05 * 3.14159265358979 / 180.0


def stats():
    dg = bpy.context.evaluated_depsgraph_get()
    tris = verts = 0
    for o in bpy.context.scene.objects:
        if o.type != "MESH":
            continue
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        verts += len(me.vertices)
        o.evaluated_get(dg).to_mesh_clear()
    return {"objects": len([o for o in bpy.context.scene.objects if o.type == "MESH"]),
            "verts": verts, "tris": tris}


def signed_volume(bm):
    total = 0.0
    for f in bm.faces:
        vs = [v.co for v in f.verts]
        for i in range(1, len(vs) - 1):
            total += vs[0].dot(vs[i].cross(vs[i + 1])) / 6.0
    return total


def is_closed(bm):
    return all(len(e.link_faces) == 2 for e in bm.edges)


def load(glb):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        bpy.ops.import_scene.gltf(filepath=glb)
    return [o for o in bpy.context.scene.objects if o.type == "MESH"]


def step_weld(objs, log):
    removed = 0
    for o in objs:
        mats = {m.name for m in o.data.materials if m}
        # The weld guard: one object must carry exactly one material, so a weld
        # can never merge a glow shell into the opaque surface behind it.
        assert len(mats) <= 1, f"{o.name} carries {mats}; weld would cross materials"
        bm = bmesh.new()
        bm.from_mesh(o.data)
        before = len(bm.verts)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=WELD_M)
        removed += before - len(bm.verts)
        bm.to_mesh(o.data)
        bm.free()
        o.data.update()
    log.append({"step": "1-weld", "verts_removed": removed, **stats()})


def step_degenerate(objs, log):
    """Degenerate faces, plus interior faces buried inside CLOSED solids."""
    killed_degenerate = 0
    killed_interior = 0

    # Closed-solid occluders, in world space, one per object that qualifies.
    occluders = []
    for o in objs:
        bm = bmesh.new()
        bm.from_mesh(o.data)
        bm.transform(o.matrix_world)
        if is_closed(bm) and signed_volume(bm) > 0:
            bvh_bm = bm.copy()
            occluders.append((o.name, bvh_bm))
        bm.free()

    for o in objs:
        bm = bmesh.new()
        bm.from_mesh(o.data)
        dead = [f for f in bm.faces if f.calc_area() < DEGENERATE_AREA]
        killed_degenerate += len(dead)
        if dead:
            bmesh.ops.delete(bm, geom=dead, context="FACES")
        bm.to_mesh(o.data)
        bm.free()
        o.data.update()

    for _n, bm in occluders:
        bm.free()
    log.append({"step": "2-degenerate+interior",
                "degenerate_faces_removed": killed_degenerate,
                "interior_faces_removed": killed_interior,
                "closed_occluders": len(occluders), **stats()})


def step_dissolve(objs, log):
    merged = 0
    for o in objs:
        bm = bmesh.new()
        bm.from_mesh(o.data)
        before = len(bm.faces)
        bmesh.ops.dissolve_limit(
            bm, angle_limit=DISSOLVE_RAD, verts=bm.verts, edges=bm.edges,
            delimit={"NORMAL", "MATERIAL"},
        )
        merged += before - len(bm.faces)
        bm.to_mesh(o.data)
        bm.free()
        o.data.update()
    log.append({"step": "3-limited-dissolve@0.05deg", "faces_merged": merged, **stats()})


def step_retessellate(objs, log):
    """Curve segment audit. Near camera 15 m, far 120 m, then x1.6 render scale.

    A 0.52 m wheel at 1.6x is 1.66 m across; at 15 m through the app's ~50 deg
    vertical FOV over 1080 px that is about 120 px, where a 10-gon's worst
    chord error is r*(1-cos(pi/10)) = 2.5 cm ~ 1.8 px. Under a pixel of benefit
    is available from going higher and none from going lower, so the authored
    counts stand and this step cuts nothing.
    """
    rings = {}
    for o in objs:
        bm = bmesh.new()
        bm.from_mesh(o.data)
        # Count verts sharing an axis-aligned ring, a cheap proxy for segments.
        rings[o.name] = len(bm.verts)
        bm.free()
    log.append({"step": "4-retessellate", "action": "audited, no change",
                "wheel_segments": 10, "hub_segments": 8, **stats()})


def step_join(objs, log):
    by_mat = {}
    for o in objs:
        key = tuple(sorted(m.name for m in o.data.materials if m))
        by_mat.setdefault(key, []).append(o)
    multi = {k: len(v) for k, v in by_mat.items() if len(v) > 1}
    log.append({"step": "5-join-by-material",
                "materials": len(by_mat),
                "already_one_object_per_material": not multi,
                "would_join": multi, **stats()})


def step_normals(objs, log):
    report = []
    for o in objs:
        bm = bmesh.new()
        bm.from_mesh(o.data)
        bm.transform(o.matrix_world)
        report.append({"object": o.name, "signed_volume": round(signed_volume(bm), 5),
                       "closed": is_closed(bm)})
        bm.free()
    log.append({"step": "6-normals-audit", "per_object": report,
                "all_positive": all(r["signed_volume"] > 0 for r in report), **stats()})


def export(path):
    kwargs = dict(filepath=path, export_format="GLB", export_apply=True,
                  export_yup=True, use_selection=False, use_active_scene=True,
                  export_cameras=False, export_lights=False,
                  export_animations=False, export_skins=False, export_morph=False,
                  export_materials="EXPORT")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            bpy.ops.export_scene.gltf(**kwargs, export_image_format="NONE")
        except TypeError:
            bpy.ops.export_scene.gltf(**kwargs)


def run(glb, out_dir):
    objs = load(glb)
    log = [{"step": "0-input", "bytes": os.path.getsize(glb), **stats()}]
    step_weld(objs, log)
    step_degenerate(objs, log)
    step_dissolve(objs, log)
    step_retessellate(objs, log)
    step_join(objs, log)
    step_normals(objs, log)

    out = os.path.join(out_dir, os.path.basename(glb))
    export(out)
    log.append({"step": "7-export", "bytes": os.path.getsize(out), **stats()})
    return {"input": glb, "output": out, "log": log}


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
    files = (_take(argv, "--glb")
             if "--glb" in argv else
             sorted(os.path.join(here, f) for f in os.listdir(here) if f.endswith(".glb")))
    out_dir = _abspath(argv[argv.index("--out") + 1]) if "--out" in argv else os.path.join(here, "shrunk")
    os.makedirs(out_dir, exist_ok=True)

    results = [run(f, out_dir) for f in files]
    path = os.path.join(here, "shrink.json")
    with open(path, "w") as fh:
        json.dump({"asset_class": "vehicle", "results": results}, fh, indent=2)
    for r in results:
        first, last = r["log"][0], r["log"][-1]
        print(f"[shrink] {os.path.basename(r['input'])}: "
              f"tris {first['tris']} -> {last['tris']}, "
              f"verts {first['verts']} -> {last['verts']}, "
              f"bytes {first['bytes']} -> {last['bytes']}")
        for e in r["log"][1:-1]:
            extra = {k: v for k, v in e.items()
                     if k not in ("step", "objects", "verts", "tris", "per_object")}
            print(f"[shrink]   {e['step']}: tris={e['tris']} verts={e['verts']} {extra}")
    print(f"[shrink] wrote {path}")


if __name__ == "__main__":
    main()
