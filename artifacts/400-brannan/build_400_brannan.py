"""Deterministic Blender build of the SF-SIM miniature 400 Brannan Street.

    blender -b --python build_400_brannan.py -- [--out DIR]

Writes 400-brannan.blend and 400-brannan.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint AABB centre (anchor lon -122.3946805,
lat 37.7800981), min Z = 0, roof-bulkhead crest exactly 8.8 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3776114) simplified from 13 to 5
  vertices (491.7 m2 against the survey's 489.4), a 23.89 x 23.07 m corner block
  with a notch bitten out of its west corner where the 574 Third apartment
  complex wraps round it, sitting 45.2 deg off the world axes like the whole
  SoMa grid;
* two finished street elevations meeting at a sharp corner — that corner is the
  building's entire job in the city, so both faces get the same treatment and
  nothing is cheated on the Third Street side;
* light warm body over a near-black base, the tonal split that reads at any
  distance;
* the identity feature: one continuous black awning shelf at shopfront height,
  running the full length of both frontages and mitred round the corner;
* wide LANDSCAPE industrial sash upstairs — the proportion that separates this
  from every residential neighbour on the block;
* night state: the shopfront band under the awnings on both frontages (this is
  a corner with cafes on it) plus four lit upper windows. Glow surfaces are thin
  shells proud of the opaque glazing — the app renders _Glow in a separate layer
  at ~12% alpha by day, so a primary surface is never authored as glow;
* a designed roof for the app's downward camera: parapet ring under a stone
  coping, a mechanical group set back toward the block interior (matching the
  nadir imagery, which shows the street-facing third of the deck empty), a
  hatch, and the bulkhead that sets the 8.8 m crest.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF building footprint SF3776114 projected with the app's tangent
# projection, recentred on the AABB centre and simplified to 5 vertices. CCW.
# Vertex 1 is the reflex corner of the northwest notch.
FOOTPRINT = [
    (-1.365, 16.605),    # 0  N corner
    (-2.955, 11.195),    # 1  notch (reflex)
    (-15.485, -2.395),   # 2  W corner
    (-0.875, -16.605),   # 3  S corner
    (15.485, -0.335),    # 4  E corner
]

# Edge i runs FOOTPRINT[i] -> FOOTPRINT[i+1]. Outward normals verified against
# the survey.
EDGE_NW_UPPER = 0   # 5.63 m,  faces NW — party wall against 574 Third
EDGE_NW_LOWER = 1   # 18.47 m, faces NW — party wall against 574 Third
EDGE_REAR = 2       # 20.38 m, faces SW 224.2 deg — block interior
EDGE_BRANNAN = 3    # 23.07 m, faces SE 135.2 deg — Brannan Street
EDGE_THIRD = 4      # 23.89 m, faces NE  45.2 deg — Third Street

Z_DECK = 7.77        # roof deck (DataSF LiDAR median, sigma 0.64 m)
Z_PARAPET = 8.6      # parapet crest (inferred: deck + 0.83 m)
Z_CREST = 8.8        # roof bulkhead top -> the bbox top, = targetHeightM
Z_BASE = 0.75        # dark base band
Z_SHOP0, Z_SHOP1 = 0.90, 3.40    # shopfront glazing
Z_AWN0, Z_AWN1 = 3.50, 3.95      # awning shelf
Z_COURSE = 4.05                  # floor-line course
Z_WIN0, Z_WIN1 = 4.85, 6.45      # upper sash band (1.6 m tall, landscape)

PARAPET_T = 0.35
AWNING_D = 0.60

PALETTE_HEX = {
    "Toy_sand": "ece4d4",
    "Toy_stone": "d9d2c2",
    "Toy_ink": "3a3530",
    "Toy_glass": "2a4d73",
    "Toy_trim": "f3efe6",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_glass_Glow": "6f95b8",
    "Toy_trim_Glow": "f3efe6",
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
    """Edge i of FOOTPRINT: (origin, length, tangent unit, outward normal)."""
    a = FOOTPRINT[i]
    b = FOOTPRINT[(i + 1) % len(FOOTPRINT)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def offset_polygon(poly, d):
    """Miter offset of the CCW footprint; positive d moves outward."""
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
    """Miniature-style edge softening (style bible s.4). Width is capped at a
    third of the thinnest dimension: the applied panels here are 60-130 mm thick
    and a flat 0.12 m bevel on those collapses opposing profiles into slivers."""
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
    """Closed extrusion of a CCW polygon (walls + both caps)."""
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
    """Closed band following a footprint: 4 loops, quads between."""
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
    """Closed prism of a (u, z) profile lying in the plane of wall `edge`,
    extruded outward from offset d0 to d1 along that wall's normal."""
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


def roof_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the roof, aligned to the building's own grid: u runs along the
    Brannan edge from its west end, v runs INTO the block."""
    origin, _l, t, n = poly_edge(EDGE_BRANNAN)
    cx = origin[0] + t[0] * u - n[0] * v
    cy = origin[1] + t[1] * u - n[1] * v
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


# --------------------------------------------------------------------- parts


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None, inset=0.18):
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, 0.06, frame_mat)
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        0.0,
        0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = inset + 0.14
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            0.10,
            0.17,
            glow_mat,
        )


def street_elevation(tag, edge, bays, shop_spans, entrance_us, lit_bays, mats,
                     rolldoor=None, lit_shops=()):
    """One finished street front: shopfront band, awning shelf, upper sash."""
    ink, glass, trim, glassl_glow, trim_glow, sand = mats
    _a, length, _t, _n = poly_edge(edge)

    # shopfront band: recessed dark reveals with glazing, divided by piers
    for i, (u, w) in enumerate(shop_spans):
        rect_opening(
            f"{tag}_shop{i}", edge, u, w, Z_SHOP0, Z_SHOP1, ink, glass,
            trim_glow if i in lit_shops else None, inset=0.22,
        )
    for i, u in enumerate(entrance_us):
        rect_opening(f"{tag}_door{i}", edge, u, 1.35, 0.0, 2.85, ink, ink, inset=0.16)

    if rolldoor is not None:
        u, w = rolldoor
        rect_opening(f"{tag}_freight", edge, u, w, 0.0, 3.30, ink, trim, inset=0.16)

    # the identity feature: one continuous awning shelf, full length
    face_panel(
        f"{tag}_awning", edge, length / 2.0, rect_profile(length - 0.25, Z_AWN0, Z_AWN1),
        0.0, AWNING_D, ink,
    )

    # upper floor: landscape sash, a few lit at night
    for i in range(bays):
        u = length / (2.0 * bays) + i * (length / bays)
        rect_opening(
            f"{tag}_win{i}", edge, u, 2.75, Z_WIN0, Z_WIN1, trim, glass,
            glassl_glow if i in lit_bays else None, inset=0.14,
        )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    sand = material("Toy_sand")
    stone = material("Toy_stone")
    ink = material("Toy_ink")
    glass = material("Toy_glass")
    trim = material("Toy_trim")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    gglow = material("Toy_glass_Glow")
    tglow = material("Toy_trim_Glow")

    # --- body: one stucco-over-masonry box, its top cap IS the roof deck ----
    prism("body", FOOTPRINT, 0.0, Z_DECK, sand, mat_caps=roofd)

    # --- dark base band, wrapping all four sides ---------------------------
    ring_band("base", FOOTPRINT, 0.0, Z_BASE, 0.0, 0.10, ink)

    # --- floor-line course --------------------------------------------------
    ring_band("course", FOOTPRINT, Z_COURSE, Z_COURSE + 0.22, 0.0, 0.12, stone)

    # --- parapet ring + stone coping ---------------------------------------
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET - 0.16, -PARAPET_T, 0.0, sand)
    ring_band("coping", FOOTPRINT, Z_PARAPET - 0.16, Z_PARAPET, -PARAPET_T - 0.07, 0.07, stone)

    mats = (ink, glass, trim, gglow, tglow, sand)

    # --- Brannan Street elevation (SE, bearing 135.2) -----------------------
    # roll-up freight door at the southwest end, then the shopfront run under
    # the awning; address plates 410 / 406 / 400 read SW -> NE in the 2016
    # photography, which is the order the openings follow here.
    len_b = poly_edge(EDGE_BRANNAN)[1]
    street_elevation(
        "bran", EDGE_BRANNAN, 6,
        shop_spans=[(7.7, 3.0), (11.6, 3.0), (15.5, 3.0), (19.4, 3.0)],
        entrance_us=[13.55, 21.9],
        lit_bays={1, 4},
        mats=mats,
        rolldoor=(3.1, 4.0),
        lit_shops={2, 3},
    )

    # --- Third Street elevation (NE, bearing 45.2) --------------------------
    # More glass, no freight door: this is the cafe side (590 and 592 Third).
    len_t = poly_edge(EDGE_THIRD)[1]
    street_elevation(
        "third", EDGE_THIRD, 6,
        shop_spans=[(3.3, 3.4), (7.6, 3.4), (12.6, 3.4), (16.9, 3.4), (21.2, 3.0)],
        entrance_us=[10.1],
        lit_bays={0, 3, 5},
        mats=mats,
        lit_shops={0, 3, 4},
    )

    # --- party walls: quiet, finished, no invented grid ---------------------
    # Sparse high-level openings only, on the half of each wall that the app's
    # aerial camera can actually see past the neighbours.
    for tag, edge, us in (
        ("rear", EDGE_REAR, (4.6, 9.4, 14.2)),
        ("nw", EDGE_NW_LOWER, (5.0, 10.4, 15.0)),
    ):
        for i, u in enumerate(us):
            rect_opening(f"{tag}win{i}", edge, u, 1.3, Z_WIN0 + 0.2, Z_WIN1 - 0.2, sand, glass,
                         inset=0.14)

    # --- roof: the surface the app's camera sees most -----------------------
    # u runs along the Brannan edge from its west end, v goes back into the
    # block. The nadir imagery shows the street-facing third of the deck empty
    # and the units grouped toward the interior, so that is where they go.
    roof_box("mech_plinth", 10.4, 13.0, Z_DECK, Z_DECK + 0.18, 7.6, 4.4, roofd)
    roof_box("mech_a", 8.4, 12.6, Z_DECK, Z_DECK + 0.8, 1.8, 1.3, steel)
    roof_box("mech_b", 11.0, 13.4, Z_DECK, Z_DECK + 0.6, 1.2, 1.0, steel)
    roof_box("mech_c", 13.4, 11.8, Z_DECK, Z_DECK + 1.0, 0.9, 0.9, steel)
    roof_box("duct", 9.8, 14.6, Z_DECK + 0.2, Z_DECK + 0.45, 0.6, 2.0, steel)
    roof_box("hatch", 17.0, 9.6, Z_DECK, Z_DECK + 0.45, 1.4, 1.1, roofd)
    roof_box("skylight_kerb", 5.6, 9.4, Z_DECK, Z_DECK + 0.2, 2.2, 2.2, stone)
    roof_box("bulkhead", 15.0, 14.4, Z_DECK, Z_CREST, 3.2, 2.4, roofd)

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.12/2; window frames get a token 1-segment softening; fills and glow
    # shells get none, which is what keeps this under the 8,000-triangle cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")):
            continue
        if obj.name.endswith("_frame"):
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
    print("[build] anchor lon/lat: -122.3946805 37.7800981 (footprint AABB centre)")
    print("[build] Third front heading 45.2 deg; Brannan front heading 135.2 deg")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "400-brannan.blend")
    glb = os.path.join(out, "400-brannan.glb")
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
