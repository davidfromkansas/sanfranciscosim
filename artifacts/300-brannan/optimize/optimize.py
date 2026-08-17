# Phase B geometry cleanup + leak-proof export — run headless:
#   "$BLENDER" -b --python optimize.py -- <input.glb> <output_mid.glb> <stats.json>
#
# Steps (per GLB-OPTIMIZE-PROMPT v1 §3):
#   1. weld coincident verts <=1mm within each object (glow shells are separate
#      objects, so a per-object weld can never fuse glow onto base surfaces)
#   2. delete degenerate faces; delete interior faces strictly buried inside
#      another box-like solid (AABB-fill >= 95%) — provable-invisible only
#   3. (SKIPPED) limited dissolve — see the note at the step
#   4. (skipped) curve retess — the cupola is a silhouette-defining hypar shell
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
for o in mesh_objs():
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
    bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=0.001)
    bm.to_mesh(o.data)
    bm.free()
snap("weld+degenerate")

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

# --- 3. limited dissolve: SKIPPED for this asset ---
# GLB-OPTIMIZE-PROMPT v2 s.3 step 3: "Skip this step entirely on assets with
# large coplanar ring bands." 300 Brannan carries FOUR full-footprint ring
# bands built with ring_band() — the base cornice (belt), its stone cap
# (belt_cap), the parapet and the parapet coping. Their top and bottom faces
# are perfectly coplanar annuli, so even a strictly-coplanar dissolve merges
# each ring into one annulus ngon whose re-triangulation emits metre-long
# slivers; those pass every area-based degeneracy test and only surface after
# the shipping swap, as invalid_or_nonunit_loop_normal_count in the packed
# file. On 350-brannan the same step was worth 0.4% of triangles. Not worth it.
stats["limited_dissolve"] = "skipped: four coplanar ring bands (see comment)"
snap("limited-dissolve-skipped")

# --- 5. join per material (multi-material objects keep their own mesh) ---
groups = defaultdict(list)
for o in mesh_objs():
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
