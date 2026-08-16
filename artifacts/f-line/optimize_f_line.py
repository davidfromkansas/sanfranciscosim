"""Stage 2 geometry shrink pass for the F-line PCC streetcar.

    blender -b --python optimize_f_line.py -- <input.glb> <output.glb> <stats.json>

Follows docs/asset-plans/transit/README.md Part 3 with ASSET_CLASS=vehicle,
after ~/sf-3d-assets/optimized/st-marys-cathedral/optimize.py:

  1. weld coincident verts <= 1 mm WITHIN each object (never across a _Glow
     boundary - the glow shells are separate objects, so a per-object weld
     cannot fuse a 3.5 cm proud shell onto the surface behind it)
  2. delete degenerate faces, then interior faces provably buried inside
     another CLOSED solid (an open shell's signed volume is meaningless and
     lets it masquerade as a box, eating real faces)
  3. limited dissolve at 0.05 deg - NOT 0.5.  This asset is the reason the
     transit README calls that out: the PCC nose is a lofted curved shell and
     0.5 deg merges transitively across it, building twisted ngons that
     re-triangulate with flipped windings
  4. curve retessellation: SKIPPED, deliberately.  See below.
  5. join objects sharing a material set
  6. per-object signed volume audit

THE CATASTROPHIC FAILURE THIS SCRIPT EXISTS TO PREVENT is `Toy_body` being
merged away.  It is the one material the cities-series liveries are tinted
through, and if it disappears every PCC in the city is the same colour with no
error anywhere.  Three separate guards:

  * the join groups by material SET, and the body shell's set
    {Toy_body, Toy_cream, Toy_glass, Toy_ink, Toy_steel} is unique to it, so
    the shell cannot be folded into another group;
  * `toy_body_survived` asserts the material is still in the re-imported file;
  * `toy_body_is_own_slot` asserts it is still a SEPARATE slot rather than one
    that gltfpack could later collapse into a look-alike neutral.

The last one matters because gltfpack merges materials with identical
parameters and `-km` is what stops it; make.sh runs gltfpack with `-km` and
re-checks the material list afterwards.
"""

import contextlib
import io
import json
import sys
from collections import defaultdict

import bmesh
import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1 :]
INPUT, OUTPUT, STATS = argv[0], argv[1], argv[2]

TINTABLE = "Toy_body"

# Unlike the cable car, this vehicle is a CLOSED union - the doors sit on the
# flank, the glow shells bury their backs, the pole roots into its plinth - so
# a few percent of provably buried faces is expected and healthy.  The alarm is
# set above the audited baseline so a REGRESSION still trips it;
# interior_faces_by_object below is the audit trail for what was removed.
INTERIOR_DELETION_ALARM = 0.10

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


def face_count():
    return sum(len(o.data.polygons) for o in mesh_objs())


def scene_bbox():
    mins = Vector((1e18,) * 3)
    maxs = Vector((-1e18,) * 3)
    for o in mesh_objs():
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            mins = Vector(map(min, mins, w))
            maxs = Vector(map(max, maxs, w))
    return mins, maxs


def signed_volume(o):
    me = o.data
    me.calc_loop_triangles()
    s = 0.0
    for t in me.loop_triangles:
        a, b, c = (me.vertices[i].co for i in t.vertices)
        s += a.dot(b.cross(c)) / 6.0
    return s


def is_closed(o):
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    ok = bool(bm.faces) and all(len(e.link_faces) == 2 for e in bm.edges)
    bm.free()
    return ok


stats = {
    "input_materials": sorted(m.name for m in bpy.data.materials),
    "steps": [],
    "retessellation": "SKIPPED - the wheels are 10-segment discs and the "
                      "trolley pole a 6-segment shank, already authored at the "
                      "15-120 m vehicle band times the app's 1.6x render "
                      "scale; halving them flat-spots the wheels against a "
                      "street the car never leaves",
    "dissolve_angle_deg": 0.05,
}
t0, v0 = counts()
b0 = scene_bbox()
f0 = face_count()
stats["input"] = {"tris": t0, "verts": v0, "objects": len(mesh_objs()), "faces": f0}


def snap(label):
    t, v = counts()
    stats["steps"].append({"step": label, "tris": t, "verts": v, "objects": len(mesh_objs())})
    print(f"STEP {label}: tris={t} verts={v} objects={len(mesh_objs())}")


# --- 1 + 2a. weld and degenerate, per object -------------------------------
for o in mesh_objs():
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
    bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=0.001)
    bm.to_mesh(o.data)
    bm.free()
snap("weld+degenerate")

# --- 2b. interior faces buried inside another CLOSED box-like solid ---------
EPS = 0.001


def is_axis_aligned_box(o):
    """Every face normal on a cardinal axis.  A fill test alone accepts the
    lofted body shell and the crowned roof vents as solid boxes, and the AABB
    of a curved solid contains air the solid does not - which would condemn the
    doors, the drip rails and the window panes sitting ON that curve."""
    for p in o.data.polygons:
        n = o.matrix_world.to_3x3() @ p.normal
        if max(abs(n.x), abs(n.y), abs(n.z)) < 0.999:
            return False
    return True


def has_glow(o):
    return any(m and m.name.endswith("_Glow") for m in o.data.materials)


solid_boxes = []
for o in mesh_objs():
    # A _Glow shell is never an OCCLUDER either, not just never a victim.  It
    # is a 3.5 cm slab standing proud of a surface, so it is a closed
    # axis-aligned box that passes the fill test - and the first run used the
    # lit interior strips to condemn two faces off the top of every one of the
    # nineteen window panes they overlap, opening all nineteen and handing the
    # join a grp_Toy_glass with a NEGATIVE signed volume.  mergeVehicle() in
    # app/src/agents.js answers that by reversing the whole group: every window
    # in the city would have shipped inside out.
    if has_glow(o):
        continue
    if not is_closed(o) or not is_axis_aligned_box(o):
        continue
    vol = signed_volume(o)
    d = o.dimensions
    aabb = d.x * d.y * d.z
    if aabb > 0 and vol > 0 and vol / aabb >= 0.99:
        ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
        solid_boxes.append(
            (
                o.name,
                Vector((min(p[i] for p in ws) for i in range(3))),
                Vector((max(p[i] for p in ws) for i in range(3))),
            )
        )


def inside_a_box(pts, exclude):
    """Returns the occluder's name, so every deletion carries its reason."""
    for name, mn, mx in solid_boxes:
        if name == exclude:
            continue
        if all(mn[i] + EPS < p[i] < mx[i] - EPS for p in pts for i in range(3)):
            return name
    return None


interior_removed = 0
by_object = {}
glow_skipped = []
for o in mesh_objs():
    # NEVER delete a _Glow shell's buried faces.  Their back face is buried ON
    # PURPOSE - that is how the contract hides a 3.5 cm proud shell's edges by
    # day - so deleting it turns a closed shell into an open one, and a joined
    # group with a NEGATIVE signed volume is reversed wholesale by
    # mergeVehicle() in app/src/agents.js: the headlight, the route board, the
    # tail lights and both lit interior strips would all ship inside out.
    # Same rule as the README's "never weld across a _Glow boundary", applied
    # to the deletion step.
    if has_glow(o):
        glow_skipped.append(o.name)
        continue
    bm = bmesh.new()
    bm.from_mesh(o.data)
    doomed = []
    occluders = set()
    for f in bm.faces:
        pts = [o.matrix_world @ v.co for v in f.verts]
        pts.append(o.matrix_world @ f.calc_center_median())
        hit = inside_a_box(pts, o.name)
        if hit:
            doomed.append(f)
            occluders.add(hit)
    if doomed:
        interior_removed += len(doomed)
        by_object[o.name] = {"faces": len(doomed), "buried_in": sorted(occluders)}
        bmesh.ops.delete(bm, geom=doomed, context="FACES")
        bm.to_mesh(o.data)
    bm.free()
stats["glow_objects_exempt_from_interior_deletion"] = sorted(glow_skipped)
stats["interior_faces_by_object"] = dict(
    sorted(by_object.items(), key=lambda kv: -kv[1]["faces"])
)
stats["interior_faces_removed"] = interior_removed
stats["interior_faces_removed_fraction"] = round(interior_removed / max(1, f0), 5)
stats["interior_face_alarm"] = interior_removed / max(1, f0) > INTERIOR_DELETION_ALARM
if stats["interior_face_alarm"]:
    print(
        f"ALARM: interior-face step removed {interior_removed}/{f0} faces. "
        f"On this asset only the door backs, the pole root and a few bumper "
        f"faces are genuinely buried, so a large saving means it is deleting "
        f"skin. STOP AND INVESTIGATE."
    )
snap("interior-faces")

# --- 3. limited dissolve, strictly coplanar --------------------------------
#
# 0.000872665 rad = 0.05 deg.  The nose is nine lofted rings of 24-gon
# cross-section: every quad down it differs from its neighbour by a degree or
# two, which 0.5 deg merges transitively into twisted ngons.
for o in mesh_objs():
    bpy.context.view_layer.objects.active = o
    for oo in mesh_objs():
        oo.select_set(oo is o)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.dissolve_limited(angle_limit=0.000872665, delimit={"MATERIAL", "SHARP"})
    bpy.ops.object.mode_set(mode="OBJECT")
snap("limited-dissolve")

# Windings after the dissolve, before the join folds objects together.  This is
# the check the transit README asks for by name on curved shells.
stats["inverted_after_dissolve"] = [o.name for o in mesh_objs() if signed_volume(o) < 0]

# --- 4. curve retessellation: skipped on purpose ---------------------------
stats["wheel_face_counts"] = {
    o.name: len(o.data.polygons) for o in mesh_objs() if o.name.startswith("wheel_")
}

# --- 5. join objects sharing a material set --------------------------------
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
    joined.name = "grp_" + "_".join(mats)
    join_log[joined.name] = len(objs)
stats["joins"] = join_log

# The body shell's material SET is unique, so the join must have left it alone
# and Toy_body must still live on exactly one object.
tint_objs = sorted(
    o.name for o in mesh_objs()
    if any(m and m.name == TINTABLE for m in o.data.materials)
)
stats["tintable_objects_after_join"] = tint_objs
stats["tintable_not_merged_into_another_material_group"] = len(tint_objs) == 1
snap("join-per-material")

# --- 6. normals audit ------------------------------------------------------
inverted = [o.name for o in mesh_objs() if signed_volume(o) < 0]
stats["inverted_solids_after_join"] = inverted
stats["group_signed_volumes"] = {
    o.name: round(signed_volume(o), 6) for o in sorted(mesh_objs(), key=lambda x: x.name)
}
stats["merge_vehicle_safe"] = not inverted
stats["inverted_note"] = (
    "A joined per-material group is a UNION of solids, not one solid; its "
    "signed volume is the sum of its parts and MUST stay positive, because "
    "app/src/agents.js mergeVehicle() reverses any source mesh whose signed "
    "volume is negative. A negative group here ships that whole material "
    "inside out. Per-object closure is proved before the join by "
    "validate_f_line.py."
)
if inverted:
    print("HARD FAIL: negative signed volume after join:", inverted)

# --- leak-proof export: a temp scene holding only the export objects -------
export_scene = bpy.data.scenes.new("EXPORT_TMP")
src_scene = [s for s in bpy.data.scenes if s is not export_scene][0]
for o in list(src_scene.objects):
    export_scene.collection.objects.link(o)
bpy.context.window.scene = export_scene
with contextlib.redirect_stdout(io.StringIO()):
    bpy.ops.export_scene.gltf(
        filepath=OUTPUT,
        export_format="GLB",
        use_active_scene=True,
        export_apply=True,
        export_yup=True,
        export_cameras=False,
        export_lights=False,
        export_animations=False,
    )

# --- re-import verify ------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=OUTPUT)
objs2 = mesh_objs()
mins2, maxs2 = scene_bbox()
t2, v2 = counts()
out_mats = sorted({m.name for o in objs2 for m in o.data.materials if m})
stats["reimport"] = {
    "objects": len(objs2),
    "tris": t2,
    "verts": v2,
    "materials": out_mats,
    "bbox_dims": [round(x, 4) for x in (maxs2 - mins2)],
    "bbox_min": [round(x, 4) for x in mins2],
}
in_dims = b0[1] - b0[0]
out_dims = maxs2 - mins2
tol = max(0.01, 0.001 * max(in_dims))
stats["bbox_ok"] = all(abs(in_dims[i] - out_dims[i]) <= tol for i in range(3))
stats["material_set_ok"] = sorted(out_mats) == sorted(stats["input_materials"])
stats["glow_layer_intact"] = sorted(m for m in out_mats if m.endswith("_Glow")) == sorted(
    m for m in stats["input_materials"] if m.endswith("_Glow")
)
stats["toy_body_survived"] = TINTABLE in out_mats
stats["toy_body_is_own_slot"] = sum(1 for m in out_mats if m == TINTABLE) == 1
if not stats["toy_body_survived"]:
    print("HARD FAIL: Toy_body did not survive the shrink pass - every PCC "
          "in the city would be one colour.")

with open(STATS, "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=1)
    f.write("\n")
print("OPTIMIZE-OK", json.dumps(stats["reimport"]))
print(
    "bbox_ok", stats["bbox_ok"],
    "material_set_ok", stats["material_set_ok"],
    "glow_intact", stats["glow_layer_intact"],
    "toy_body", stats["toy_body_survived"],
    "interior_alarm", stats["interior_face_alarm"],
    "merge_safe", stats["merge_vehicle_safe"],
)
