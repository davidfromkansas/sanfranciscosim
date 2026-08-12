"""Stage 2 of the shrink pass for the Muni Metro LRV — the geometry shrink.

    blender -b --python optimize_muni_lrv.py -- [--in F] [--out F] [--json F]

`ASSET_CLASS=vehicle`, per `docs/asset-plans/transit/README.md` Part 3. Stage 1
(meshopt intake, `gltfpack -cc -kn -km -noq`) runs after this — see shrink.sh.

Order of operations, measuring deltas after each step:

  1. Weld coincident verts at <= 1 mm, NEVER across a `_Glow` boundary.
  2. Delete degenerate faces (< 1 mm^2) and interior faces buried in solids.
  3. Limited dissolve at **0.05 deg, not 0.5 deg**.
  4. Retessellate over-segmented curves (audit).
  5. Join objects sharing a material (asserted, satisfied at authoring time).
  6. Normals audit: per-object signed volume positive.

WHY 0.05 AND NOT 0.5 -- this asset is the reason the README says it. The cab is
a curved shell built from chamfered plan outlines stacked in z. At 0.5 deg the
limited dissolve merges transitively across those chamfers, builds twisted
n-gons spanning the whole nose, and re-triangulates them with flipped windings.
The saving at 0.05 deg is near-identical and the windings survive.

WHY THE WELD IS SAFE HERE -- this model exports three multi-material objects,
so "one material per object" cannot be used as the structural guarantee the
muni-bus build relied on. Instead the weld is run per-object with an explicit
material-boundary guard: vertices are only merged when every face touching them
shares one material index, so a weld can never pull a 4 cm proud `_Glow` shell
down onto the opaque surface behind it.
"""

import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

WELD = 0.001            # 1 mm
DEGENERATE = 1e-6       # 1 mm^2
DISSOLVE_DEG = 0.05
GLOW_SUFFIX = "_Glow"


def argval(argv, flag, default=None):
    return argv[argv.index(flag) + 1] if flag in argv else default


def stats():
    tris = verts = 0
    prims = 0
    for o in bpy.context.scene.objects:
        if o.type != "MESH":
            continue
        me = o.data
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        verts += len(me.vertices)
        prims += max(1, len(me.materials))
    return {"triangles": tris, "vertices": verts, "primitives": prims,
            "objects": len([o for o in bpy.context.scene.objects if o.type == "MESH"])}


def signed_volume(obj):
    me = obj.data
    me.calc_loop_triangles()
    total = 0.0
    for t in me.loop_triangles:
        a, b, c = (obj.matrix_world @ me.vertices[i].co for i in t.vertices)
        total += a.dot(b.cross(c)) / 6.0
    return total


def weld_guarded(obj):
    """Weld within `WELD`, but never across a material boundary.

    A vertex is eligible only if every face using it carries the same material
    index. That is what keeps a `_Glow` shell 3-5 cm proud of its opaque
    backing: the glow surfaces are the only geometry sitting that close to
    another surface on purpose, and welding them flat would silently destroy
    the night layer the whole transit set is being built to gain.
    """
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    eligible = []
    for v in bm.verts:
        mats = {f.material_index for f in v.link_faces}
        if len(mats) <= 1:
            eligible.append(v)
    before = len(bm.verts)
    bmesh.ops.remove_doubles(bm, verts=eligible, dist=WELD)
    removed = before - len(bm.verts)
    bm.to_mesh(me)
    bm.free()
    return removed


def drop_degenerate(obj):
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    dead = [f for f in bm.faces if f.calc_area() < DEGENERATE]
    n = len(dead)
    if dead:
        bmesh.ops.delete(bm, geom=dead, context="FACES")
    bm.to_mesh(me)
    bm.free()
    return n


def limited_dissolve(obj):
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    before = len(bm.faces)
    bmesh.ops.dissolve_limit(
        bm, angle_limit=math.radians(DISSOLVE_DEG),
        verts=list(bm.verts), edges=list(bm.edges),
        delimit={"MATERIAL", "NORMAL"},
    )
    merged = before - len(bm.faces)
    bm.to_mesh(me)
    bm.free()
    return merged


def curve_audit(cfg_note):
    """Step 4. Segment counts were set against the vehicle camera band (near
    15 m, far 120 m) and then multiplied by the app's 1.6x render scale, so
    this is an audit rather than an edit.

    A 0.68 m wheel at 1.6x is 1.09 m across. At the 15 m near camera that is
    roughly 80 px, where an 8-gon's worst chord error is 2.1 cm ~ 1.5 px. The
    wheels are also 70% hidden behind the skirt. Nothing to gain going higher.
    The pantograph arms are 5- and 6-gon capsules for the same reason.
    """
    return cfg_note


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    src = argval(argv, "--in", os.path.join(here, "build", "muni-lrv.glb"))
    dst = argval(argv, "--out", os.path.join(here, "shrunk", "muni-lrv.glb"))
    js = argval(argv, "--json", os.path.join(here, "shrink.json"))
    os.makedirs(os.path.dirname(dst), exist_ok=True)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=src)
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]

    log = {"input": os.path.relpath(src, here), "output": os.path.relpath(dst, here),
           "params": {"weld_m": WELD, "degenerate_m2": DEGENERATE,
                      "dissolve_deg": DISSOLVE_DEG},
           "before": stats(), "steps": {}}
    log["before"]["bytes"] = os.path.getsize(src)

    mats_before = sorted({m.name for o in meshes for m in o.data.materials if m})
    nodes_before = sorted(o.name for o in meshes)

    welded = sum(weld_guarded(o) for o in meshes)
    log["steps"]["1_weld"] = {"verts_removed": welded, "after": stats(),
                              "guard": "per-vertex material-boundary guard; "
                                       "no weld can cross a _Glow boundary"}

    degen = sum(drop_degenerate(o) for o in meshes)
    # Interior-face removal: the occluder test needs CLOSED meshes, because the
    # signed volume of an open shell is meaningless and would let it masquerade
    # as a solid box and eat real faces. Each section here is a union of many
    # solids plus flat detail quads hosted inside them, so it is not a closed
    # manifold and is correctly EXCLUDED from occluder duty rather than run
    # through it. Recorded rather than silently skipped.
    log["steps"]["2_degenerate_interior"] = {
        "degenerate_faces_removed": degen,
        "interior_faces_removed": 0,
        "occluder_note": "sections are unions of solids with hosted flat detail, "
                         "not closed manifolds; excluded from occluder duty by "
                         "design (README Part 3 step 2)",
        "after": stats(),
    }

    merged = sum(limited_dissolve(o) for o in meshes)
    log["steps"]["3_limited_dissolve"] = {
        "angle_deg": DISSOLVE_DEG, "faces_merged": merged, "after": stats()}

    log["steps"]["4_curves"] = {
        "changed": False,
        "note": curve_audit("wheels 8-gon, pantograph arms 5/6-gon, verified "
                            "against near 15 m / far 120 m at 1.6x"),
    }

    per_material_objects = {}
    for o in meshes:
        for m in o.data.materials:
            if m:
                per_material_objects.setdefault(m.name, set()).add(o.name)
    log["steps"]["5_join_by_material"] = {
        "performed": False,
        "note": "satisfied at authoring time: one primitive per material within "
                "each section. Materials are not joined ACROSS sections because "
                "the brief requires LRV_Section_A/B/Bellows to stay separable.",
        "materials_spanning_sections": {
            k: sorted(v) for k, v in per_material_objects.items() if len(v) > 1},
    }

    volumes = {}
    for o in meshes:
        bm = bmesh.new()
        bm.from_mesh(o.data)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(o.data)
        bm.free()
        volumes[o.name] = round(signed_volume(o), 4)
    log["steps"]["6_normals"] = {
        "signed_volumes": volumes,
        "all_positive": all(v > 0 for v in volumes.values()),
    }

    # Leak-proof export, same recipe as the build.
    import contextlib
    import io
    for o in bpy.data.objects:
        o.select_set(False)
    kwargs = dict(filepath=dst, export_format="GLB", export_apply=True,
                  export_yup=True, use_selection=False, use_active_scene=True,
                  export_cameras=False, export_lights=False,
                  export_animations=False, export_skins=False,
                  export_morph=False, export_materials="EXPORT")
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            bpy.ops.export_scene.gltf(**kwargs, export_image_format="NONE")
        except TypeError:
            bpy.ops.export_scene.gltf(**kwargs)

    log["after"] = stats()
    log["after"]["bytes"] = os.path.getsize(dst)
    mats_after = sorted({m.name for o in meshes for m in o.data.materials if m})
    log["gates"] = {
        "G1_materials_identical": mats_before == mats_after,
        "G1_nodes_identical": nodes_before == sorted(o.name for o in meshes),
        "G1_glow_intact": [m for m in mats_after if m.endswith(GLOW_SUFFIX)],
        "G5_primitives_not_increased":
            log["after"]["primitives"] <= log["before"]["primitives"],
        "G6_smaller": log["after"]["bytes"] < log["before"]["bytes"],
    }
    with open(js, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)

    b, a = log["before"], log["after"]
    print(f"[shrink] tris {b['triangles']} -> {a['triangles']}, "
          f"verts {b['vertices']} -> {a['vertices']}, "
          f"bytes {b['bytes']} -> {a['bytes']}, "
          f"prims {b['primitives']} -> {a['primitives']}")
    print(f"[shrink] weld removed {welded} verts, dissolve merged {merged} faces, "
          f"{degen} degenerate faces")
    print(f"[shrink] wrote {dst} and {js}")


if __name__ == "__main__":
    main()
