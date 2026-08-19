"""Deterministic Blender build of the SF-SIM miniature 560 Third Street.

    blender -b --python build_560_third.py -- [--out DIR]

Writes 560-third.blend and 560-third.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint oriented-bbox centre (anchor lon -122.3951188,
lat 37.7804142), min Z = 0, parapet crest exactly 7.2 m.

Design (see REFERENCE.md for the sources behind every number):

* the OSM footprint (way/124903642) exactly as traced — a 9.40 m front, 9.98 m
  rear, 24 m deep sliver on the SoMa grid (44.1 / 315.1 / 224.9 / 134.9 deg
  outward normals). The slight taper is kept: the neighbours in the bake were
  traced from the same source and line up with it;
* ONE public elevation. Three sides are party walls buried behind 550 Third
  (7.2 m, 11.0 m post-2025) and 574 Third (11.05 m), so they are clean planes
  with a parapet cap and nothing else. Detail spent there is detail stolen from
  the two surfaces that are seen;
* a near-black painted box — Toy_ink walls, one step darker than anything else
  on the block face. This is the identity: the building is the low dark notch
  between a brown 3-storey block and a cream 2-storey warehouse, and it has to
  read as a gap from the app's aerial camera before any detail resolves;
* the Third Street front: a dark glazed shopfront with the entry door at the
  574 end, one head band, and above it a single wide four-pane window band
  filling most of a 9.4 m frontage. That is the whole elevation — no cornice,
  no signage, no ornament, because the real one has none;
* a designed roof, which is over 90% of what this asset ever shows: pale
  membrane field inside a dark parapet ring with a light steel cap, two large
  skylights, a compact mechanical cluster and a hatch in the rear third;
* night state: the upper band as one warm lantern across the full frontage (the
  Feb 2017 dusk reference), the two skylights glowing from the loft below, and
  a single small cue at the door. Nothing else lights.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/124903642, projected with the app's tangent projection and recentred
# on the oriented-bbox centre. CCW (shoelace area +232.6 m2).
FOOTPRINT = [
    (11.71, 5.31),      # 0  E corner  (Third St / 574 Third party line)
    (4.96, 11.86),      # 1  N corner  (Third St / 550 Third party line)
    (-12.03, -4.99),    # 2  W corner  (rear / 550 Third)
    (-4.97, -12.04),    # 3  S corner  (rear / 574 Third)
]

# Edge i runs FOOTPRINT[i] -> FOOTPRINT[i+1].
EDGE_THIRD = 0   #  9.40 m, faces NE  44.1 — Third Street front, the only public face
EDGE_NW = 1      # 23.93 m, faces NW 315.1 — party wall with 550 Third
EDGE_REAR = 2    #  9.98 m, faces SW 224.9 — rear party wall (550 Third wraps behind)
EDGE_SE = 3      # 24.07 m, faces SE 134.9 — party wall with 574 Third

Z_ROOF = 6.66        # roof structure top (DataSF LiDAR SF3776007 median 6.66)
Z_MEMB = 6.78        # membrane build-up over the structure
Z_PARAPET = 7.20     # parapet crest -> the bbox top, = targetHeightM
PARAPET_T = 0.30
CAP_T = 0.10         # steel coping band

Z_BASE = 0.15                    # dark base rail under the shopfront
Z_SHOP0, Z_SHOP1 = 0.15, 3.30    # shopfront glazing
Z_HEAD0, Z_HEAD1 = 3.30, 3.55    # storefront head band
BAND = (4.05, 6.05)              # the upper window band

FRONT_W = 9.40       # measured length of EDGE_THIRD
SHOP_W = 8.40
BAND_W = 8.00
DOOR_U = 1.15        # door centre, measured from the 574 (south-east) end
DOOR_W = 1.10

PALETTE_HEX = {
    "Toy_ink": "3a3530",        # the painted charcoal shell — walls and parapet
    "Toy_roofd": "45454a",      # frames, mullions, head band, base rail, plant
    "Toy_steel": "9aa0a6",      # parapet coping, skylight frames, roof hatch
    "Toy_stone": "d9d2c2",      # roof membrane field
    "Toy_glass": "2a4d73",      # window and shopfront glazing
    "Toy_glassl": "6f95b8",     # skylight panes, door vision panel
    # The dusk reference is unambiguously warm: the upper band reads as one
    # amber rectangle in a black facade. Toy_glass_Glow (a blue) would have
    # thrown that away, so the hero glow is the palette's mustard instead.
    "Toy_mustard_Glow": "d9a441",
    "Toy_glassl_Glow": "6f95b8",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def poly_edge(i):
    a = FOOTPRINT[i]
    b = FOOTPRINT[(i + 1) % len(FOOTPRINT)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def offset_polygon(poly, d):
    npts = len(poly)
    normals = []
    for i in range(npts):
        a, b = poly[i], poly[(i + 1) % npts]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        normals.append((dy / length, -dx / length))
    out = []
    for i in range(npts):
        n1, n2 = normals[i - 1], normals[i]
        v = poly[i]
        det = n1[0] * n2[1] - n1[1] * n2[0]
        if abs(det) < 1e-6:
            out.append((v[0] + n2[0] * d, v[1] + n2[1] * d))
            continue
        c1 = v[0] * n1[0] + v[1] * n1[1] + d
        c2 = v[0] * n2[0] + v[1] * n2[1] + d
        out.append(((c1 * n2[1] - c2 * n1[1]) / det, (c2 * n1[0] - c1 * n2[0]) / det))
    return out


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


# -------------------------------------------------------------- mesh helpers


def new_mesh(name, verts, faces, materials, face_mats=None):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    for m in materials:
        mesh.materials.append(m)
    if face_mats:
        for poly, mi in zip(mesh.polygons, face_mats):
            poly.material_index = mi
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.shade_flat()
    return obj


def bevel(obj, width=0.12, segments=2):
    thin = min((d for d in obj.dimensions if d > 1e-6), default=width)
    offset = min(width, thin * 0.30)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(
        bm,
        geom=list(bm.verts) + list(bm.edges),
        offset=offset,
        segments=segments,
        profile=0.5,
        affect="EDGES",
        clamp_overlap=True,
    )
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-4)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-4, edges=list(bm.edges))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def prism(name, poly, z0, z1, mat, mat_caps=None):
    npts = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces, face_mats = [], []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
        face_mats.append(0)
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    face_mats += [1 if mat_caps else 0] * 2
    mats = [mat, mat_caps] if mat_caps else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def ring_band(name, poly, z0, z1, off_in, off_out, mat):
    lo_in = offset_polygon(poly, off_in)
    lo_out = offset_polygon(poly, off_out)
    npts = len(lo_in)
    verts = []
    for loop, z in ((lo_in, z0), (lo_out, z0), (lo_out, z1), (lo_in, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * npts, ((k + 1) % 4) * npts
        for i in range(npts):
            j = (i + 1) % npts
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def face_panel(name, edge, u_centre, profile, d0, d1, mat):
    a, _length, t, n = poly_edge(edge)
    verts = []
    for d in (d0, d1):
        for du, z in profile:
            px = a[0] + t[0] * (u_centre + du) + n[0] * d
            py = a[1] + t[1] * (u_centre + du) + n[1] * d
            verts.append((px, py, z))
    npts = len(profile)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0):
    c, s = math.cos(yaw), math.sin(yaw)
    corners = []
    for lx, ly in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)):
        corners.append((cx + lx * c - ly * s, cy + lx * s + ly * c))
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


def cyl(name, cx, cy, z0, z1, r, mat, seg=8):
    ring = [
        (cx + r * math.cos(2 * math.pi * k / seg), cy + r * math.sin(2 * math.pi * k / seg))
        for k in range(seg)
    ]
    return prism(name, ring, z0, z1, mat)


def roof_point(u, v):
    """World XY of a point on the roof grid: u along the Third Street edge from
    its south-east (574) end, v INTO the block."""
    origin, _l, t, n = poly_edge(EDGE_THIRD)
    return (origin[0] + t[0] * u - n[0] * v, origin[1] + t[1] * u - n[1] * v)


def roof_box(name, u, v, z0, z1, su, sv, mat):
    origin, _l, t, n = poly_edge(EDGE_THIRD)
    cx, cy = roof_point(u, v)
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=math.atan2(t[1], t[0]))


def material(name):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    rgb = PALETTE[name]
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    bsdf.inputs["Metallic"].default_value = 0.0
    if name.endswith("_Glow"):
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


def skylight(tag, u, v, su, sv, steel, glassl, glow):
    """Frame proud of the membrane with a raised pane and a thin glow shell.
    Everything on this roof stays at or below the 7.20 m parapet crest, so the
    crest is the bbox top and the loader's scale factor lands on 1.0."""
    roof_box(f"{tag}_frame", u, v, Z_MEMB - 0.05, Z_MEMB + 0.22, su, sv, steel)
    roof_box(f"{tag}_pane", u, v, Z_MEMB + 0.18, Z_MEMB + 0.30, su - 0.34, sv - 0.34, glassl)
    roof_box(f"{tag}_glow", u, v, Z_MEMB + 0.28, Z_MEMB + 0.34, su - 0.62, sv - 0.62, glow)


# --------------------------------------------------------------------- build


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    ink = material("Toy_ink")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    stone = material("Toy_stone")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    mglow = material("Toy_mustard_Glow")
    lglow = material("Toy_glassl_Glow")

    # --- body: the painted charcoal shell -----------------------------------
    prism("body", FOOTPRINT, 0.0, Z_ROOF, ink, mat_caps=ink)

    # --- roof membrane field, inside the parapet line ------------------------
    prism("membrane", offset_polygon(FOOTPRINT, -PARAPET_T), Z_ROOF - 0.02, Z_MEMB, stone)

    # --- parapet ring + steel coping ----------------------------------------
    ring_band("parapet", FOOTPRINT, Z_ROOF, Z_PARAPET - CAP_T, -PARAPET_T, 0.0, ink)
    ring_band("coping", FOOTPRINT, Z_PARAPET - CAP_T, Z_PARAPET, -PARAPET_T - 0.06, 0.06, steel)

    # ============================ Third Street front ========================
    # Everything below is authored on EDGE_THIRD, u measured from the south-east
    # (574 Third) corner. d is proud of the wall along the outward normal.

    # base rail under the shopfront
    face_panel("front_base", EDGE_THIRD, FRONT_W / 2.0,
               rect_profile(FRONT_W, 0.0, Z_BASE), 0.0, 0.14, roofd)

    # shopfront: one dark glazed plane in a frame
    face_panel("shop_frame", EDGE_THIRD, FRONT_W / 2.0,
               rect_profile(SHOP_W, Z_SHOP0, Z_SHOP1), 0.0, 0.08, roofd)
    face_panel("shop_fill", EDGE_THIRD, FRONT_W / 2.0,
               rect_profile(SHOP_W - 0.44, Z_SHOP0 + 0.22, Z_SHOP1 - 0.22), 0.0, 0.15, glass)
    # two slim shopfront mullions, so the ground floor reads as a storefront
    # rather than as a hole punched in the wall
    for k, du in enumerate((-1.05, 1.75)):
        face_panel(f"shop_mull{k}", EDGE_THIRD, FRONT_W / 2.0 + du,
                   rect_profile(0.14, Z_SHOP0 + 0.14, Z_SHOP1 - 0.14), 0.0, 0.20, roofd)

    # entry door at the south-east end of the shopfront, with a vision panel
    face_panel("door_leaf", EDGE_THIRD, DOOR_U,
               rect_profile(DOOR_W, Z_SHOP0, 2.55), 0.0, 0.24, roofd)
    face_panel("door_vision", EDGE_THIRD, DOOR_U,
               rect_profile(DOOR_W - 0.34, 0.80, 2.30), 0.0, 0.30, glassl)
    face_panel("door_glow", EDGE_THIRD, DOOR_U,
               rect_profile(DOOR_W - 0.52, 0.92, 2.18), 0.27, 0.33, mglow)

    # storefront head band, full width
    face_panel("front_head", EDGE_THIRD, FRONT_W / 2.0,
               rect_profile(FRONT_W, Z_HEAD0, Z_HEAD1), 0.0, 0.18, roofd)

    # --- the upper window band: the elevation's whole architecture -----------
    face_panel("band_frame", EDGE_THIRD, FRONT_W / 2.0,
               rect_profile(BAND_W, BAND[0], BAND[1]), 0.0, 0.08, roofd)
    face_panel("band_fill", EDGE_THIRD, FRONT_W / 2.0,
               rect_profile(BAND_W - 0.36, BAND[0] + 0.18, BAND[1] - 0.18), 0.0, 0.15, glass)
    # The glow shell is deliberately smaller than the pane: assets.js renders
    # _Glow at 12% alpha by DAY, so a full-pane shell washes the daytime glazing
    # to grey. This keeps the day read blue and the night read a full lantern.
    face_panel("band_glow", EDGE_THIRD, FRONT_W / 2.0,
               rect_profile(BAND_W - 0.86, BAND[0] + 0.42, BAND[1] - 0.42), 0.12, 0.18, mglow)
    # four panes -> three internal mullions
    for k, du in enumerate((-2.0, 0.0, 2.0)):
        face_panel(f"band_mull{k}", EDGE_THIRD, FRONT_W / 2.0 + du,
                   rect_profile(0.16, BAND[0] + 0.10, BAND[1] - 0.10), 0.0, 0.21, roofd)
    # sill, reading as one crisp line under the band
    face_panel("band_sill", EDGE_THIRD, FRONT_W / 2.0,
               rect_profile(BAND_W + 0.30, BAND[0] - 0.16, BAND[0]), 0.0, 0.24, roofd)

    # ================================ roof ==================================
    # Two big skylights on the centreline, then the plant cluster in the rear
    # third. Nothing else: this is a 233 m2 roof and it turns to clutter fast.
    skylight("sky_a", FRONT_W / 2.0, 7.5, 3.2, 2.2, steel, glassl, lglow)
    skylight("sky_b", FRONT_W / 2.0, 14.5, 3.2, 2.2, steel, glassl, lglow)

    roof_box("plant_curb", FRONT_W / 2.0, 19.4, Z_MEMB, Z_MEMB + 0.08, 5.6, 2.0, roofd)
    for k, u in enumerate((3.3, 6.4)):
        roof_box(f"plant{k}", u, 19.4, Z_MEMB + 0.08, Z_PARAPET, 1.30, 0.90, roofd)
    roof_box("plant_duct", FRONT_W / 2.0, 20.9, Z_MEMB, Z_MEMB + 0.26, 4.2, 0.34, roofd)
    for k, (u, v) in enumerate(((2.3, 22.2), (7.1, 20.9))):
        cx, cy = roof_point(u, v)
        cyl(f"vent{k}", cx, cy, Z_MEMB, Z_MEMB + 0.42, 0.20, roofd)
    roof_box("hatch", 6.5, 22.3, Z_MEMB, Z_MEMB + 0.35, 1.00, 0.90, steel)

    # Bevel budget: chunky masses get the full 0.12/2; frames and mullions a
    # token 1-segment softening; fills and glow shells none.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow", "_vision", "_pane")):
            continue
        if obj.name.endswith(("_frame", "_head", "_base", "_sill", "_leaf")) or "_mull" in obj.name:
            bevel(obj, width=0.05, segments=1)
        else:
            bevel(obj, width=0.12, segments=2)

    return scene


def report():
    dg = bpy.context.evaluated_depsgraph_get()
    tris = 0
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    for o in objs:
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    print("[build] anchor lon/lat: -122.3951188 37.7804142 (footprint OBB centre)")
    print("[build] Third front outward normal 44.1 deg; long axis 43.9 deg")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "560-third.blend")
    glb = os.path.join(out, "560-third.glb")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    bpy.ops.export_scene.gltf(
        filepath=glb,
        export_format="GLB",
        export_apply=True,
        export_yup=True,
        use_selection=False,
        export_cameras=False,
        export_lights=False,
        export_animations=False,
        export_skins=False,
        export_morph=False,
        export_materials="EXPORT",
        export_image_format="NONE",
    )
    print(f"[build] wrote {blend}")
    print(f"[build] wrote {glb}")


if __name__ == "__main__":
    main()
