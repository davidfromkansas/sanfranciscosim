# Phase A forensic inspection — run headless:
#   "$BLENDER" -b --python inspect.py -- <input.glb> <out.json>
import bpy, sys, json, os, gzip, math
from collections import defaultdict
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
INPUT, OUTJSON = argv[0], argv[1]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=INPUT)

report = {}
raw = os.path.getsize(INPUT)
with open(INPUT, "rb") as f:
    gz = len(gzip.compress(f.read(), 9))
report["file_bytes"] = {"raw": raw, "gzip9": gz}

objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
depsgraph = bpy.context.evaluated_depsgraph_get()

per_obj = []
total_tris = total_verts = 0
mat_users = defaultdict(list)       # material name -> object names
mesh_signature = defaultdict(list)  # (verts, tris, dims-rounded) -> objects
prim_count = 0
attr_formats = set()
degenerate = 0
coincident_candidates = 0

for o in objs:
    me = o.data
    me.calc_loop_triangles()
    tris = len(me.loop_triangles)
    verts = len(me.vertices)
    total_tris += tris
    total_verts += verts
    dims = tuple(round(d, 4) for d in o.dimensions)
    mats = sorted({m.name for m in me.materials if m}) or ["<none>"]
    prim_count += max(1, len([m for m in me.materials if m]))
    for m in mats:
        mat_users[m].append(o.name)
    mesh_signature[(verts, tris, dims)].append(o.name)
    per_obj.append({"name": o.name, "tris": tris, "verts": verts,
                    "dims": [round(d, 3) for d in o.dimensions], "materials": mats})
    if me.uv_layers: attr_formats.add("UV")
    if me.color_attributes: attr_formats.add("COLOR")
    attr_formats.add("NORMAL")
    # degenerate faces
    for t in me.loop_triangles:
        if t.area < 1e-6:  # < 1 mm^2
            degenerate += 1
    # coincident-vert estimate: hash rounded positions
    seen = defaultdict(int)
    for v in me.vertices:
        seen[tuple(round(c, 3) for c in v.co)] += 1
    coincident_candidates += sum(n - 1 for n in seen.values() if n > 1)

per_obj.sort(key=lambda r: -r["tris"])
report["objects"] = len(objs)
report["total_tris"] = total_tris
report["total_verts"] = total_verts
report["primitives_est"] = prim_count
report["top20"] = per_obj[:20]
report["vertex_attrs"] = sorted(attr_formats)

mats_out = []
for name in sorted(mat_users):
    mats_out.append({"name": name, "glow": name.endswith("_Glow"),
                     "user_objects": len(mat_users[name])})
report["materials"] = mats_out
report["textures"] = [i.name for i in bpy.data.images if i.name not in ("Render Result", "Viewer Node")]

# scene bbox from world-space corners
mins = Vector((1e18,) * 3); maxs = Vector((-1e18,) * 3)
for o in objs:
    for c in o.bound_box:
        w = o.matrix_world @ Vector(c)
        mins = Vector(map(min, mins, w)); maxs = Vector(map(max, maxs, w))
dims = maxs - mins
center = (maxs + mins) / 2
report["bbox"] = {"dims": [round(v, 4) for v in dims],
                  "min": [round(v, 4) for v in mins],
                  "origin_offset_xy": [round(center.x, 4), round(center.y, 4)],
                  "base_z": round(mins.z, 4)}

# duplicate-mesh census
dups = [{"signature": {"verts": k[0], "tris": k[1], "dims": list(k[2])},
         "objects": v} for k, v in mesh_signature.items() if len(v) > 1]
dups.sort(key=lambda d: -d["signature"]["tris"] * len(d["objects"]))
report["duplicate_mesh_groups"] = dups
report["dup_redundant_tris"] = sum(d["signature"]["tris"] * (len(d["objects"]) - 1) for d in dups)

# join candidates: objects sharing exactly one material
joinable = {m: v for m, v in mat_users.items() if len(v) > 1}
report["join_candidates"] = {m: len(v) for m, v in sorted(joinable.items())}

report["degenerate_tris"] = degenerate
report["coincident_vert_pairs"] = coincident_candidates

# over-tessellation: screen-pixel chord error at landmark near distance
long_axis = max(dims)
near = 1.5 * long_axis
# app-style camera: ~40 deg vfov, 1080 px tall -> world size of one pixel at distance
px_world = 2 * near * math.tan(math.radians(20)) / 1080
report["over_tess"] = {"near_distance_m": round(near, 2),
                       "one_px_world_m": round(px_world, 4),
                       "note": "cylinders whose chord error < one_px_world_m can halve segments"}

with open(OUTJSON, "w") as f:
    json.dump(report, f, indent=1)
print("INSPECT-OK", raw, gz, len(objs), total_tris, total_verts)
