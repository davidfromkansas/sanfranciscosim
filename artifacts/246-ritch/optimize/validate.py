# Gate G1/G2 validation (Blender side) — run headless:
#   "$BLENDER" -b --python validate.py -- <input.glb> <optimized.glb> <out.json>
#
# Two per-asset adaptations over tools/glb-optimize/validate.py, both required by
# any asset with deliberately single-sided surfaces (the glow shells here are thin
# panels), and both learned on davies-symphony-hall:
#
#  1. glTF stores SPLIT vertices for flat shading, so on re-import every solid
#     reads as an open shell and a naive signed-volume gate is vacuous. Weld into
#     a THROWAWAY bmesh first, then judge. (Never weld the geometry you ship —
#     that is a different question, measured in the four-variant table in
#     REPORT.md.)
#  2. The absolute 0.15% ray-flip gate is wrong for such assets: they carry a
#     standing residual of their own. The gate exists to catch the OPTIMIZER
#     flipping windings, so ray-test the input too and gate on the DELTA.
import bpy, bmesh, sys, json, math, random
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
INPUT, OPT, OUTJSON = argv[0], argv[1], argv[2]

def load(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    return [o for o in bpy.context.scene.objects if o.type == "MESH"]

def stats(objs):
    mins = Vector((1e18,) * 3); maxs = Vector((-1e18,) * 3)
    tris = verts = 0
    for o in objs:
        o.data.calc_loop_triangles()
        tris += len(o.data.loop_triangles)
        verts += len(o.data.vertices)
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            mins = Vector(map(min, mins, w)); maxs = Vector(map(max, maxs, w))
    mats = sorted({m.name for o in objs for m in o.data.materials if m})
    prims = sum(max(1, len([m for m in o.data.materials if m])) for o in objs)
    return {"tris": tris, "verts": verts, "objects": len(objs),
            "primitives": prims, "materials": mats,
            "bbox_dims": [round(v, 5) for v in (maxs - mins)],
            "bbox_min": [round(v, 5) for v in mins],
            "center_xy": [round((maxs[0] + mins[0]) / 2, 5),
                          round((maxs[1] + mins[1]) / 2, 5)]}

def signed_volumes(objs):
    """Signed volume per object, judged on a welded throwaway copy.

    Also reports whether the welded copy is closed — an open shell's signed
    volume is meaningless and must not be gated on."""
    out = {}
    for o in objs:
        bm = bmesh.new()
        bm.from_mesh(o.data)
        bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-4)
        closed = all(len(e.link_faces) == 2 for e in bm.edges)
        me = bpy.data.meshes.new("_tmp_weld")
        bm.to_mesh(me)
        bm.free()
        me.calc_loop_triangles()
        s = 0.0
        for t in me.loop_triangles:
            a, b, c = (me.vertices[i].co for i in t.vertices)
            s += a.dot(b.cross(c)) / 6.0
        out[o.name] = {"volume": round(s, 6), "closed": closed}
        bpy.data.meshes.remove(me)
    return out

def ray_test(objs, n=22500):
    # first-visible-face winding test: from outside sphere, cast toward bbox
    mins = Vector((1e18,) * 3); maxs = Vector((-1e18,) * 3)
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            mins = Vector(map(min, mins, w)); maxs = Vector(map(max, maxs, w))
    center = (mins + maxs) / 2
    radius = (maxs - mins).length
    rng = random.Random(42)
    deps = bpy.context.evaluated_depsgraph_get()
    scene = bpy.context.scene
    hits = flipped = 0
    for _ in range(n):
        u, v = rng.random(), rng.random()
        theta = 2 * math.pi * u
        phi = math.acos(2 * v - 1)
        d = Vector((math.sin(phi) * math.cos(theta),
                    math.sin(phi) * math.sin(theta), math.cos(phi)))
        target = Vector((mins[i] + rng.random() * (maxs[i] - mins[i])
                         for i in range(3)))
        origin = target - d * radius * 2
        ok, loc, normal, idx, obj, mw = scene.ray_cast(deps, origin, d,
                                                       distance=radius * 4)
        if ok:
            hits += 1
            if normal.dot(d) > 1e-6:
                flipped += 1
    return {"rays": n, "hits": hits, "flipped": flipped,
            "flipped_fraction": round(flipped / max(1, hits), 6)}

report = {}
objs_in = load(INPUT)
report["input"] = stats(objs_in)

objs_out = load(OPT)  # fresh load replaces scene, so recompute input stats first
report["output"] = stats(objs_out)
report["output_signed_volumes"] = signed_volumes(objs_out)
# Only CLOSED solids can be judged by signed volume (GLB-OPTIMIZE-PROMPT s.3.2).
report["inverted_solids"] = [k for k, v in report["output_signed_volumes"].items()
                             if v["closed"] and v["volume"] < 0]
report["open_shells"] = [k for k, v in report["output_signed_volumes"].items() if not v["closed"]]
report["ray_test_output"] = ray_test(objs_out)
objs_in2 = load(INPUT)
report["ray_test_input"] = ray_test(objs_in2)
report["ray_flip_delta"] = round(report["ray_test_output"]["flipped_fraction"]
                                 - report["ray_test_input"]["flipped_fraction"], 6)

din = report["input"]["bbox_dims"]; dout = report["output"]["bbox_dims"]
tol = max(0.01, 0.001 * max(din))
report["gates"] = {
    "G1_materials_identical": report["input"]["materials"] == report["output"]["materials"],
    "G2_bbox_ok": all(abs(din[i] - dout[i]) <= tol for i in range(3)),
    "G2_origin_ok": (all(abs(report["input"]["center_xy"][i] - report["output"]["center_xy"][i]) <= 0.01 for i in range(2))
                     and abs(report["input"]["bbox_min"][2] - report["output"]["bbox_min"][2]) <= 0.01),
    "G2_volumes_positive": not report["inverted_solids"],
    # Delta, not absolute: the gate exists to catch the optimizer flipping
    # windings, and this asset's own standing residual is whatever it is.
    "G2_ray_flip_ok": report["ray_flip_delta"] <= 0.0015,
    "G5_primitives_ok": report["output"]["primitives"] <= report["input"]["primitives"],
}
with open(OUTJSON, "w") as f:
    json.dump(report, f, indent=1)
print("VALIDATE-OK", json.dumps(report["gates"]))
print("ray in ", json.dumps(report["ray_test_input"]))
print("ray out", json.dumps(report["ray_test_output"]))
print("delta", report["ray_flip_delta"], "open shells", report["open_shells"])
