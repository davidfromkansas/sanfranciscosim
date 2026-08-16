# Phase B geometry cleanup + leak-proof export — run headless:
#   "$BLENDER" -b --python optimize.py -- <input.glb> <output_mid.glb> <stats.json>
#
# Steps (per GLB-OPTIMIZE-PROMPT v1 §3):
#   1. weld coincident verts <=1mm within each object (glow shells are separate
#      objects, so a per-object weld can never fuse glow onto base surfaces)
#   2. delete degenerate faces; delete interior faces strictly buried inside
#      another box-like solid (AABB-fill >= 95%) — provable-invisible only
#   3. (SKIPPED) limited dissolve — see the block below; this asset is exactly
#      the "large coplanar ring band" case the prompt warns about
#   4. (skipped) curve retess — the tree crowns and the Shout's tubes are
#      silhouette-defining, and the 72 promenade tablets are already 4-gons
#   5. join objects per material (no manifest node names, no Toy_body here)
#   7. signed-volume normals audit
import bpy, bmesh, sys, json, contextlib, io
from collections import defaultdict
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
INPUT, OUTPUT, STATS = argv[0], argv[1], argv[2]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=INPUT)

def mesh_objs():
    return [o for o in bpy.context.scene.objects if o.type == "MESH"]

def counts():
    t = v = 0
    for o in mesh_objs():
        o.data.calc_loop_triangles()
        t += len(o.data.loop_triangles)
        v += len(o.data.vertices)
    return t, v

def scene_bbox():
    mins = Vector((1e18,) * 3); maxs = Vector((-1e18,) * 3)
    for o in mesh_objs():
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            mins = Vector(map(min, mins, w)); maxs = Vector(map(max, maxs, w))
    return mins, maxs

def signed_volume(o):
    me = o.data
    me.calc_loop_triangles()
    s = 0.0
    for t in me.loop_triangles:
        a, b, c = (me.vertices[i].co for i in t.vertices)
        s += a.dot(b.cross(c)) / 6.0
    return s

stats = {"input_materials": sorted(m.name for m in bpy.data.materials),
         "steps": []}
t0, v0 = counts()
b0 = scene_bbox()
stats["input"] = {"tris": t0, "verts": v0, "objects": len(mesh_objs())}

def snap(label):
    t, v = counts()
    stats["steps"].append({"step": label, "tris": t, "verts": v})
    print(f"STEP {label}: tris={t} verts={v}")

# --- 1+2a. weld + degenerate, per object ---
#
# Per-asset adaptation: RE-ASSERT FLAT SHADING after the weld. Every surface in
# this asset is authored flat, and the glTF round-trip brings the flat look back
# as custom split normals. bmesh's remove_doubles fuses the vertices those
# normals hang off and the mesh falls back to smooth, which on a draped ground
# plate built from 24 transverse bands rounds every band seam into a ripple.
# Measured on this asset before the fix: the A/B day-near delta was 1.03%, all
# of it from Phase B (the meshopt pack contributed 0.0006%), and the diff showed
# soft streaks along the promenade and the lawn edges. Nothing in G1/G2/G3/G5
# catches it — materials, bbox, volumes and submesh counts are all unchanged.
#
# ...and then the weld was turned OFF anyway, because it earns nothing here.
# Measured: with the weld the packed file is 397,624 bytes, without it 397,368 —
# 256 bytes, 0.06%. It reduces the Blender-side vertex count from 21,618 to
# 6,466 and the exporter then splits every one of them straight back apart,
# because on an all-flat asset each face needs its own normal. So the step buys
# nothing and has already shipped one wrong-looking build. Degenerate-face
# removal stays (it is free and cannot smooth anything), and the shade_flat()
# call stays as a guard, so that re-enabling the weld cannot quietly reintroduce
# the ripple.
WELD = False
for o in mesh_objs():
    bm = bmesh.new()
    bm.from_mesh(o.data)
    if WELD:
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
    bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=0.001)
    bm.to_mesh(o.data)
    bm.free()
    o.data.shade_flat()
stats["weld"] = "disabled: 256 bytes (0.06%) for a step that smooths flat shading"
snap("degenerate-only (weld disabled)")

# --- 2b. interior faces provably buried inside box-like solids ---
EPS = 0.001
solid_boxes = []  # (name, world-aabb min, max) for objects filling >=95% of AABB
def is_closed(o):
    bm = bmesh.new()
    bm.from_mesh(o.data)
    open_edges = any(len(e.link_faces) != 2 for e in bm.edges)
    bm.free()
    return not open_edges

for o in mesh_objs():
    # occluders must be CLOSED solids: signed volume of an open shell is
    # meaningless and let the cupola/crown shells masquerade as solid boxes
    # (deleted 165 rays' worth of real cupola faces before this check)
    if not is_closed(o):
        continue
    vol = signed_volume(o)
    d = o.dimensions
    aabb_vol = d.x * d.y * d.z
    if aabb_vol > 0 and vol > 0 and vol / aabb_vol >= 0.95:
        ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
        mn = Vector((min(p[i] for p in ws) for i in range(3)))
        mx = Vector((max(p[i] for p in ws) for i in range(3)))
        solid_boxes.append((o.name, mn, mx))

def inside_a_box(pts, exclude_name):
    for name, mn, mx in solid_boxes:
        if name == exclude_name:
            continue
        if all(mn[i] + EPS < p[i] < mx[i] - EPS for p in pts for i in range(3)):
            return True
    return False

interior_removed = 0
for o in mesh_objs():
    bm = bmesh.new()
    bm.from_mesh(o.data)
    doomed = []
    for f in bm.faces:
        pts = [o.matrix_world @ v.co for v in f.verts]
        pts.append(o.matrix_world @ f.calc_center_median())
        if inside_a_box(pts, o.name):
            doomed.append(f)
    if doomed:
        interior_removed += len(doomed)
        bmesh.ops.delete(bm, geom=doomed, context="FACES")
        bm.to_mesh(o.data)
    bm.free()
stats["interior_faces_removed"] = interior_removed
snap("interior-faces")

# --- 3. limited dissolve — DELIBERATELY SKIPPED on this asset ---
# GLB-OPTIMIZE-PROMPT §3.3: skip on assets with large coplanar ring bands. This
# one has two — the kerb is a 0.70 m band that follows the whole 47-vertex
# footprint, and the ground plate's top and bottom are the same annulus — plus
# 72 promenade tablets and 13 bed polygons whose caps are all perfectly
# coplanar. Dissolving those merges each ring into one annulus ngon whose
# re-triangulation emits metre-long, sub-millimetre slivers that pass every
# area-based degeneracy test and only surface later as
# invalid_or_nonunit_loop_normal_count in the packed file (measured on
# 350-brannan, 13 Aug 2026). The step is worth a few dozen triangles here
# against that; it is not run. Nothing downstream depends on it.
stats["limited_dissolve"] = "skipped: coplanar ring bands (kerb, plate, tablets, beds)"
snap("limited-dissolve-SKIPPED")

# --- 5. join per material (multi-material objects keep their own mesh) ---
#
# Per-asset adaptation: two objects are held OUT of the join. The stage-2
# contract validator (../validate_64_south_park.py) locates the ground plate to
# measure the oriented 159.5 x 23.5 m footprint and the anchor offset, and the
# tree crowns to confirm all 20 measured tree positions survived the export.
# Both look them up by name, and a per-material join buries `ground_plate`
# inside grp_Toy_stone and `tree_crowns` inside grp_Toy_verdigris — after which
# the shipped file can no longer be checked against the survey it was built
# from. Two extra primitives (13 -> 15) is the whole cost; the loader merges
# everything to <= 2 draw calls regardless.
KEEP_NAMES = {"ground_plate", "tree_crowns"}
groups = defaultdict(list)
for o in mesh_objs():
    if o.name.split(".")[0] in KEEP_NAMES:
        continue
    mats = tuple(sorted({m.name for m in o.data.materials if m}))
    groups[mats].append(o)
join_log = {}
for mats, objs in groups.items():
    if len(objs) < 2:
        continue
    for oo in mesh_objs():
        oo.select_set(False)
    for oo in objs:
        oo.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    joined = bpy.context.view_layer.objects.active
    joined.name = "grp_" + "_".join(mats) if len(mats) > 1 else "grp_" + mats[0]
    join_log[joined.name] = len(objs)
stats["joins"] = join_log
snap("join-per-material")

# --- 7. normals audit ---
inverted = [o.name for o in mesh_objs() if signed_volume(o) < 0]
stats["inverted_solids"] = inverted
if inverted:
    print("WARNING inverted solids:", inverted)

# --- leak-proof export: temp scene with only the export objects ---
export_scene = bpy.data.scenes.new("EXPORT_TMP")
src_scene = [s for s in bpy.data.scenes if s is not export_scene][0]
for o in list(src_scene.objects):
    export_scene.collection.objects.link(o)
bpy.context.window.scene = export_scene
with contextlib.redirect_stdout(io.StringIO()):
    bpy.ops.export_scene.gltf(filepath=OUTPUT, export_format="GLB",
                              use_active_scene=True, export_apply=True,
                              export_yup=True)

# --- re-import verify ---
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=OUTPUT)
objs2 = [o for o in bpy.context.scene.objects if o.type == "MESH"]
mins2, maxs2 = scene_bbox()
stats["reimport"] = {
    "objects": len(objs2),
    "materials": sorted({m.name for o in objs2 for m in o.data.materials if m}),
    "bbox_dims": [round(v, 4) for v in (maxs2 - mins2)],
    "bbox_min": [round(v, 4) for v in mins2],
}
in_dims = b0[1] - b0[0]
out_dims = maxs2 - mins2
tol = max(0.01, 0.001 * max(in_dims))
stats["bbox_ok"] = all(abs(in_dims[i] - out_dims[i]) <= tol for i in range(3))
stats["material_set_ok"] = (sorted(stats["reimport"]["materials"]) ==
                            sorted(stats["input_materials"]))

with open(STATS, "w") as f:
    json.dump(stats, f, indent=1)
print("OPTIMIZE-OK", json.dumps(stats["reimport"]))
print("bbox_ok", stats["bbox_ok"], "material_set_ok", stats["material_set_ok"],
      "inverted", inverted)
