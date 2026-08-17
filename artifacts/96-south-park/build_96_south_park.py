"""Deterministic Blender build of the SF-SIM miniature 86-96 South Park.

    blender -b --python build_96_south_park.py -- [--out DIR]

Writes 96-south-park.blend and 96-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = axis-aligned bbox centre of the modelled
footprint (anchor lon -122.3941704, lat 37.7818909), min Z = 0, rooftop cylinder
cap exactly 13.7 m.

Design (see REFERENCE.md for the sources behind every number, and REPORT.md for
the corrections this build made to the plan):

* Levy Design Partners (Toby S. Levy, FAIA), 1996. Four live/work residential
  units over two commercial spaces, framed entirely in lightweight steel;
  "an ambiguated facade of cubic forms" (SF Heritage);
* a CORNER lot: South Park on the SE front, Jack London Alley down the whole
  30.06 m SW flank, Taber Place at the rear, party wall with 84 South Park on
  the NE. Three designed elevations, not one;
* a collage of stepped volumes in three materials — dark glazed blue-grey brick
  to 4.5 m, light ribbed metal above, a bronze-brown volume at the alley corner;
* two rust-orange perforated steel gates, one per street elevation, and a
  continuous band of coloured mosaic tile at 2.6-2.9 m: the only saturated
  things on the building;
* a vertical-ribbed metal cylinder on the rear block's roof, its cap at 13.7 m
  and the bbox top. The rear-NE corner of the lot is an open yard, so the roof
  reads as an L;
* night state: the two ground-floor commercial fronts are the hero glow, with a
  sparse scatter of lit loft windows above. Glow surfaces are thin shells proud
  of the opaque glazing (the app renders _Glow in a separate layer that reads
  roughly a quarter opaque by day — never author a primary surface as glow).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# The lot frame the building was designed in: s across the frontage (positive
# northeast, toward 84 South Park), t into the depth (positive away from the
# park). Converted to world metres with the parcel's own measured axes.
U_S = (0.70988, 0.70432)      # +s, in (east, north) — northeast, along the frontage
U_T = (-0.70552, 0.70868)     # +t, in (east, north) — northwest, into the depth
HALF_W = 7.2195               # 14.439 m of South Park frontage
HALF_D = 15.028               # 30.056 m deep
# The origin is the bbox centre, not the lot centre: the L-shaped plan pushes
# the axis-aligned bbox 2.261 m northwest of the lot centroid, and the contract
# wants the model centred in x/y. Every st() below is shifted by this.
ORIGIN_DY = 2.261


def st(s, t):
    """Lot coordinates -> Blender world XY (metres, +X east, +Y north)."""
    return (
        U_S[0] * s + U_T[0] * t,
        U_S[1] * s + U_T[1] * t + ORIGIN_DY,
    )


# Modelled footprint: the full surveyed lot less the rear-northeast yard
# (6.42 x 8.73 m at the Taber Place / 84 South Park inside corner). CCW.
S_YARD = 0.80        # yard's southwest edge, in s
T_YARD = 6.30        # yard's park-side edge, in t

FOOTPRINT = [
    st(-HALF_W, -HALF_D),    # 0  front, southwest (the alley corner)
    st(HALF_W, -HALF_D),     # 1  front, northeast (the party-wall corner)
    st(HALF_W, T_YARD),      # 2
    st(S_YARD, T_YARD),      # 3
    st(S_YARD, HALF_D),      # 4
    st(-HALF_W, HALF_D),     # 5  rear, southwest
]

# Indices into FOOTPRINT for the elevations. Verified by outward normal in
# report(): 135.1 / 45.2 / 315.1 / 45.2 / 315.1 / 225.2 deg.
EDGE_FRONT = 0     # 14.44 m, faces SE 135.1 — South Park; u=0 at the ALLEY corner
EDGE_PARTY = 1     # 21.33 m, faces NE  45.2 — party wall with 84 South Park
EDGE_YARD_N = 2    # 6.42 m,  faces NW 315.1 — into the rear yard
EDGE_YARD_E = 3    # 8.73 m,  faces NE  45.2 — into the rear yard
EDGE_REAR = 4      # 8.02 m,  faces NW 315.1 — Taber Place
EDGE_ALLEY = 5     # 30.06 m, faces SW 225.2 — Jack London Alley; u=0 at the REAR

# Heights. The 2010 LiDAR over the two footprint rings gives majority planes at
# 9.49 m and 9.86 m, medians at 11.15 m and 12.32 m, and maxima at 13.28 m and
# 13.73 m. That distribution is read as THREE planes, not two: a main roof at
# 10.0 m over most of the plan, two upper volumes at 12.3 m, and the cylinder
# and gable above them. Reading the medians as parapets (as the plan first did)
# flattens the building into a box; the majority plane is what most of the roof
# actually is.
Z_DECK = 10.00            # main roof plate — the LiDAR majority plane
Z_PARAPET = 10.50
Z_UPPER = 12.30           # the two upper volumes — the LiDAR medians
Z_UPPER_PARAPET = 12.75
Z_GABLE = 13.35           # ridge of the gabled roof on the front upper volume
Z_PERGOLA = 11.20
Z_CREST = 13.70           # cylinder cap — THE BBOX TOP
Z_BRICK = 4.20            # top of the dark glazed brick base
Z_BAND_A, Z_BAND_B = 2.60, 2.90   # the mosaic tile band

# Floor plates: a tall 4.2 m commercial ground floor, two loft levels to the
# main roof, and a fourth inside the upper volumes.
Z_F2, Z_F3, Z_F4 = 4.90, 7.50, 10.40

# The two upper volumes, in lot coordinates.
UPA = (0.40, HALF_W, -HALF_D, -8.20)      # front, northeast — carries the gable
UPB = (-HALF_W, -0.40, 2.60, HALF_D)      # rear, southwest — carries the cylinder

CYL_SEGS = 16             # a faceted drum reads as a cylinder at diorama scale
CYL_R = 2.75
# Mid-flank on Jack London Alley, deliberately overhanging the alley wall by
# 1.83 m: the drum has to silhouette from the street as well as read as a circle
# from the air, and a drum tucked behind a parapet does neither.
CYL_S, CYL_T = -6.30, 1.20
ARCH_SEGS = 5             # the front archway's barrel soffit

PALETTE_HEX = {
    "Toy_steel_l": "b9bec4",   # ribbed metal body, cylinder, gable, bulkhead
    "Toy_slate": "39434f",     # THE dark glazed blue-grey brick base
    "Toy_teal": "3f7f86",      # THE mosaic tile band
    "Toy_bronze": "7a5f4a",    # the bronze-brown corner volume and alley panel
    "Toy_orange": "d4622a",    # THE two perforated steel gates
    "Toy_glass": "2a4d73",     # glazing
    "Toy_ink": "3a3530",       # frames, reveals, doors, pergola
    "Toy_steel": "9aa0a6",     # copings, railings, vents, cylinder cap
    "Toy_trim": "f3efe6",      # the archway soffit
    "Toy_stone": "d9d2c2",     # concrete plinth, alley stoop
    "Toy_ash": "c8c4bc",       # roof decks
    "Toy_verdigris": "9fb8a8", # rooftop planters
    "Toy_mustard_Glow": "d9a441",  # the two commercial fronts at night
    "Toy_glassl_Glow": "6f95b8",   # lit loft windows
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def poly_edge(i, poly=None):
    """Edge i of the footprint: (origin, length, tangent unit, outward normal)."""
    poly = FOOTPRINT if poly is None else poly
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


def arch_profile(w, z_sill, z_spring, segs=ARCH_SEGS):
    """(u, z) profile of a barrel-soffit opening: a rectangle up to the springing
    line, then a half-round of radius w/2 over it."""
    r = w / 2.0
    pts = [(-r, z_sill), (r, z_sill), (r, z_spring)]
    for i in range(1, segs):
        a = math.pi * i / segs
        pts.append((r * math.cos(a), z_spring + r * math.sin(a)))
    pts.append((-r, z_spring))
    return pts


def rect_lot(s0, s1, t0, t1):
    """CCW rectangle in lot coordinates -> world polygon."""
    return [st(s0, t0), st(s1, t0), st(s1, t1), st(s0, t1)]


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
    """Miniature-style edge softening on the chunky solids (style bible s.4).
    Width is capped at a third of the object's thinnest dimension so the thin
    applied panels do not collapse into slivers."""
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


def prism(name, poly, z0, z1, mat):
    """Closed extrusion of a CCW polygon (walls + both caps)."""
    npts = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def offset_polygon(poly, d):
    """Miter offset of a CCW polygon; positive d moves outward. Reflex corners
    (the rear-yard notch) are handled by the same intersection formula."""
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


def edge_box(name, edge, u_centre, su, z0, z1, d0, d1, mat):
    """Axis box on a wall's own (u, normal) frame."""
    return face_panel(name, edge, u_centre, rect_profile(su, z0, z1), d0, d1, mat)


def lot_box(name, s0, s1, t0, t1, z0, z1, mat):
    """Box on the building's own lot grid."""
    return prism(name, rect_lot(s0, s1, t0, t1), z0, z1, mat)


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
        # Flagged for the app's night pass; emission is off in the day asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------------- parts


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads as
    a border ring around a recessed opening. No booleans, all closed solids."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, 0.07, frame_mat)
    inset = 0.15
    face_panel(
        f"{tag}_fill", edge, u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset), 0.0, 0.13, fill_mat,
    )
    if glow_mat is not None:
        g = 0.27
        face_panel(
            f"{tag}_glow", edge, u,
            rect_profile(w - 2 * g, z0 + g, z1 - g), 0.10, 0.17, glow_mat,
        )


def gate(tag, edge, u, w, z0, z1, orange, ink):
    """One of the two rust-orange perforated steel gates: a dark reveal with a
    single flat saturated plane in it. Widened and brightened past reality —
    these are the building's identity accent (plan 2.6)."""
    face_panel(f"{tag}_reveal", edge, u, rect_profile(w + 0.42, z0, z1 + 0.21),
               -0.12, 0.06, ink)
    face_panel(f"{tag}_leaf", edge, u, rect_profile(w, z0, z1), 0.02, 0.15, orange)


def window_box(tag, edge, u, w, z0, z1, ink, glass, steel, glow=None):
    """A projecting bay: a slab standing proud of the wall with glazing in its
    outer face and one railing bar across it."""
    d = 0.45
    face_panel(f"{tag}_box", edge, u, rect_profile(w + 0.30, z0 - 0.14, z1 + 0.14),
               0.0, d, ink)
    face_panel(f"{tag}_fill", edge, u, rect_profile(w, z0, z1), d - 0.04, d + 0.07, glass)
    face_panel(f"{tag}_rail", edge, u, rect_profile(w + 0.44, z0 + 0.72, z0 + 0.80),
               d + 0.04, d + 0.12, steel)
    if glow is not None:
        face_panel(f"{tag}_glow", edge, u,
                   rect_profile(w - 0.26, z0 + 0.13, z1 - 0.13), d + 0.04, d + 0.11, glow)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    metal = material("Toy_steel_l")
    brick = material("Toy_slate")
    slate = brick
    mosaic = material("Toy_teal")
    bronze = material("Toy_bronze")
    orange = material("Toy_orange")
    glass = material("Toy_glass")
    ink = material("Toy_ink")
    steel = material("Toy_steel")
    trim = material("Toy_trim")
    stone = material("Toy_stone")
    ash = material("Toy_ash")
    verd = material("Toy_verdigris")
    shop_glow = material("Toy_mustard_Glow")
    loft_glow = material("Toy_glassl_Glow")

    len_front = poly_edge(EDGE_FRONT)[1]   # 14.44 m
    len_alley = poly_edge(EDGE_ALLEY)[1]   # 30.06 m

    # --- massing: one L-shaped plate, two upper volumes on top ---------------
    # The whole footprint rises to 10.0 m (the LiDAR majority plane). Two upper
    # volumes stand 2.3 m above it on diagonally opposite corners — the front
    # northeast (carrying the gable) and the rear southwest (carrying the
    # cylinder). Those two steps are the silhouette.
    prism("body", FOOTPRINT, 0.0, Z_DECK, metal)
    prism("upper_front", rect_lot(*UPA), Z_DECK - 0.60, Z_UPPER, metal)
    prism("upper_rear", rect_lot(*UPB), Z_DECK - 0.60, Z_UPPER, metal)

    # --- the dark glazed brick base, all the way round -----------------------
    # The value split at 4.2 m is the building's structure; it wraps the party
    # wall and the yard faces too, because a base that stops is a mistake.
    ring_band("brick_base", FOOTPRINT, 0.32, Z_BRICK, -0.02, 0.11, brick)
    ring_band("plinth", FOOTPRINT, 0.0, 0.34, -0.02, 0.15, stone)

    # --- the mosaic tile band ------------------------------------------------
    # One flat 0.30 m stripe on the two street elevations only. At city scale
    # the stripe IS the detail; individual tiles are sub-pixel.
    edge_box("band_front", EDGE_FRONT, len_front / 2.0, len_front - 0.10,
             Z_BAND_A, Z_BAND_B, 0.08, 0.24, mosaic)
    edge_box("band_alley", EDGE_ALLEY, len_alley / 2.0, len_alley - 0.10,
             Z_BAND_A, Z_BAND_B, 0.08, 0.24, mosaic)

    # --- the bronze corner volume -------------------------------------------
    # The southwest third of the front elevation, wrapping onto the alley
    # corner. Proud of the front block, and a different material: seam number
    # two.
    prism("bronze_corner", rect_lot(-HALF_W - 0.30, -2.40, -HALF_D - 0.30, -9.10),
          Z_BRICK - 0.30, Z_DECK + 0.55, bronze)
    ring_band("bronze_coping", rect_lot(-HALF_W - 0.30, -2.40, -HALF_D - 0.30, -9.10),
              Z_DECK + 0.55, Z_DECK + 0.65, -0.34, 0.06, steel)

    # ============================ South Park front ==========================
    # u runs from the ALLEY corner (u=0) to the party-wall corner (u=14.44).

    # The recessed archway with its barrel soffit: the deep opening at the
    # southwest end of the frontage.
    face_panel("arch_soffit", EDGE_FRONT, 2.65,
               arch_profile(3.50, 0.0, 1.85), -1.60, -0.02, trim)
    face_panel("arch_reveal", EDGE_FRONT, 2.65,
               arch_profile(3.86, 0.0, 1.94), -0.02, 0.16, ink)

    # The big storefront under the middle of the frontage, and its warm night.
    rect_opening("shopfront", EDGE_FRONT, 6.60, 3.40, 0.55, 3.25, ink, glass, shop_glow)
    # A second, smaller commercial opening toward the party wall.
    rect_opening("front_office", EDGE_FRONT, 12.60, 2.30, 0.55, 3.10, ink, glass, shop_glow)
    # The dark recessed entrance between them.
    rect_opening("front_door", EDGE_FRONT, 9.30, 1.20, 0.0, 2.70, ink, ink)
    # THE front gate — between the painted "88" and "86".
    gate("gate_front", EDGE_FRONT, 10.70, 1.80, 0.0, 3.55, orange, ink)

    # Upper glazing: two bands over the northeast two-thirds, one of them a
    # projecting bay, plus a fourth-floor band inside the upper volume.
    # Irregular by design — nothing on this facade lines up.
    LIT_FRONT = {("a", 1), ("b", 0)}
    for i, u in enumerate((6.20, 9.70, 12.90)):
        rect_opening(f"fa_{i}", EDGE_FRONT, u, 2.55, Z_F2, Z_F2 + 2.10, ink, glass,
                     loft_glow if ("a", i) in LIT_FRONT else None)
    window_box("fb_0", EDGE_FRONT, 6.20, 2.30, Z_F3, Z_F3 + 2.10, ink, glass, steel,
               loft_glow if ("b", 0) in LIT_FRONT else None)
    for i, u in enumerate((9.70, 12.90)):
        rect_opening(f"fb_{i+1}", EDGE_FRONT, u, 2.30, Z_F3, Z_F3 + 2.10, ink, glass)
    # Fourth floor, in the upper volume only: one long band of glazing.
    rect_opening("fc_0", EDGE_FRONT, 11.20, 5.60, Z_F4, Z_F4 + 1.60, ink, glass, loft_glow)
    # The bronze volume's own openings, on its own plane (0.30 m proud).
    for i, z0 in enumerate((Z_F2, Z_F3)):
        face_panel(f"bronze_win{i}_frame", EDGE_FRONT, 2.20,
                   rect_profile(3.10, z0, z0 + 2.10), 0.30, 0.37, ink)
        face_panel(f"bronze_win{i}_fill", EDGE_FRONT, 2.20,
                   rect_profile(2.80, z0 + 0.15, z0 + 1.95), 0.30, 0.43, glass)

    # --- the gabled roof on the front upper volume ---------------------------
    # A prism whose (u, z) profile is a gable, lying in the front wall's plane
    # and extruded 6.8 m back over the upper volume.
    gable_prof = [(-3.45, Z_UPPER - 0.18), (3.45, Z_UPPER - 0.18), (0.0, Z_GABLE)]
    face_panel("gable", EDGE_FRONT, 11.05, gable_prof, -7.00, -0.04, metal)

    # ======================= Jack London Alley flank ========================
    # u runs from the REAR (u=0, Taber Place end) to the FRONT (u=30.06).
    # Sparse, tall openings in the brick base; a looser rhythm above.
    rect_opening("alley_garage", EDGE_ALLEY, 2.60, 3.20, 0.32, 3.20, ink, ink)
    for i, u in enumerate((7.40, 11.00, 20.40, 26.60)):
        rect_opening(f"alley_g{i}", EDGE_ALLEY, u, 1.05, 0.60, 3.15, ink, glass,
                     shop_glow if i == 3 else None)
    rect_opening("alley_door", EDGE_ALLEY, 23.60, 1.30, 0.30, 2.80, ink, ink, shop_glow)
    # THE alley gate at "94 / 96", with its stoop.
    gate("gate_alley", EDGE_ALLEY, 19.10, 1.80, 0.55, 3.85, orange, ink)
    edge_box("gate_stoop", EDGE_ALLEY, 19.10, 2.50, 0.0, 0.55, 0.05, 1.15, stone)

    # A bronze panel three windows wide, mid-flank: seam number three.
    edge_box("alley_bronze", EDGE_ALLEY, 6.60, 8.60, Z_BRICK, Z_UPPER - 0.55,
             0.0, 0.26, bronze)

    # Two upper registers on a regular 4.3 m rhythm — regular, because a 30 m
    # wall of randomly placed holes reads as noise, and the irregularity that
    # matters is already carried by the bronze panel and the volume steps.
    LIT_ALLEY = {("a", 1), ("a", 4), ("b", 0), ("b", 4)}
    for i in range(7):
        u = 2.35 + i * 4.30
        d = 0.26 if 2.3 <= u <= 10.9 else 0.0
        face_panel(f"aa_{i}_frame", EDGE_ALLEY, u,
                   rect_profile(1.85, Z_F2, Z_F2 + 2.10), d, d + 0.07, ink)
        face_panel(f"aa_{i}_fill", EDGE_ALLEY, u,
                   rect_profile(1.55, Z_F2 + 0.15, Z_F2 + 1.95), d, d + 0.13, glass)
        if ("a", i) in LIT_ALLEY:
            face_panel(f"aa_{i}_glow", EDGE_ALLEY, u,
                       rect_profile(1.29, Z_F2 + 0.28, Z_F2 + 1.82), d + 0.10, d + 0.17,
                       loft_glow)
    for i in range(7):
        u = 2.35 + i * 4.30
        if i in (1, 5):
            window_box(f"ab_{i}", EDGE_ALLEY, u, 2.10, Z_F3, Z_F3 + 2.10,
                       ink, glass, steel,
                       loft_glow if ("b", i) in LIT_ALLEY else None)
            continue
        d = 0.26 if 2.3 <= u <= 10.9 else 0.0
        face_panel(f"ab_{i}_frame", EDGE_ALLEY, u,
                   rect_profile(1.85, Z_F3, Z_F3 + 2.10), d, d + 0.07, ink)
        face_panel(f"ab_{i}_fill", EDGE_ALLEY, u,
                   rect_profile(1.55, Z_F3 + 0.15, Z_F3 + 1.95), d, d + 0.13, glass)
        if ("b", i) in LIT_ALLEY:
            face_panel(f"ab_{i}_glow", EDGE_ALLEY, u,
                       rect_profile(1.29, Z_F3 + 0.28, Z_F3 + 1.82), d + 0.10, d + 0.17,
                       loft_glow)
    # Fourth floor, inside the rear upper volume: three openings at the Taber
    # Place end of the flank.
    for i, u in enumerate((3.10, 7.40, 11.70)):
        rect_opening(f"ac_{i}", EDGE_ALLEY, u, 1.85, Z_F4, Z_F4 + 1.60, ink, glass,
                     loft_glow if i == 1 else None)

    # ===================== Taber Place rear + the yard ======================
    rect_opening("rear_rollup", EDGE_REAR, 2.30, 3.00, 0.32, 3.30, ink, ink)
    rect_opening("rear_door", EDGE_REAR, 5.60, 1.00, 0.0, 2.30, ink, ink)
    for fi, zf in enumerate((Z_F2, Z_F3, Z_F4)):
        for i, u in enumerate((2.60, 5.90)):
            rect_opening(f"rear{fi}_{i}", EDGE_REAR, u, 1.30, zf, zf + 1.60, ink, glass)
    for i, u in enumerate((2.00, 4.40)):
        rect_opening(f"yardn_{i}", EDGE_YARD_N, u, 1.40, Z_F2, Z_F2 + 2.10, ink, glass)
    for i, u in enumerate((2.20, 5.20, 7.30)):
        rect_opening(f"yarde_{i}", EDGE_YARD_E, u, 1.40, Z_F2, Z_F2 + 2.10, ink, glass)
    rect_opening("yarde_door", EDGE_YARD_E, 3.70, 1.10, 0.32, 2.60, ink, ink)

    # ============ party wall with 84 South Park: blind, no openings =========

    # --- parapets: one ring on the main plate, one on each upper volume ------
    ring_band("parapet_main", FOOTPRINT, Z_DECK, Z_PARAPET, -0.30, 0.04, metal)
    ring_band("coping_main", FOOTPRINT, Z_PARAPET, Z_PARAPET + 0.12, -0.34, 0.08, steel)
    prism("deck_main", offset_polygon(FOOTPRINT, -0.32), Z_DECK - 0.02, Z_DECK + 0.05, ash)
    # The rear upper volume has a parapet; the front one has a gabled roof and
    # gets an eaves band instead.
    upb_ring = rect_lot(*UPB)
    ring_band("parapet_upb", upb_ring, Z_UPPER, Z_UPPER_PARAPET, -0.28, 0.04, metal)
    ring_band("coping_upb", upb_ring, Z_UPPER_PARAPET, Z_UPPER_PARAPET + 0.11,
              -0.32, 0.08, steel)
    prism("deck_upb", offset_polygon(upb_ring, -0.30), Z_UPPER - 0.02, Z_UPPER + 0.05, ash)

    # ------------------------ THE rooftop cylinder ---------------------------
    # A 16-sided drum on the alley edge, mid-flank: it grows out of the wall at
    # 5.0 m, overhangs it by 1.83 m, and stands 3.7 m clear of the 10.0 m main
    # plate. It silhouettes against the sky from the street and reads as a circle
    # from the air. The cap is the bbox top.
    cyl = []
    for i in range(CYL_SEGS):
        a = 2.0 * math.pi * i / CYL_SEGS
        cyl.append(st(CYL_S + CYL_R * math.cos(a), CYL_T + CYL_R * math.sin(a)))
    # Darker than the body: a pale drum on a pale wall under a pale roof deck
    # vanishes from the aerial camera, which is the one view it exists for.
    prism("cylinder", cyl, 5.00, Z_CREST, steel)
    # A dark coping RING, not a lid: from above the drum has to read as a
    # mid-grey circle with a rim, and a solid dark cap reads as a hole.
    ring_band("cylinder_cap", cyl, Z_CREST - 0.22, Z_CREST, -0.16, 0.14, slate)

    # --- rooftop pergola over the terrace between the two upper volumes ------
    for i, (ps, pt) in enumerate(((-3.20, -6.60), (-0.20, -6.60),
                                  (-3.20, -3.20), (-0.20, -3.20))):
        lot_box(f"pergola_post{i}", ps - 0.09, ps + 0.09, pt - 0.09, pt + 0.09,
                Z_DECK, Z_PERGOLA, ink)
    for i in range(5):
        s0 = -3.29 + i * 0.78
        lot_box(f"pergola_beam{i}", s0, s0 + 0.11, -6.69, -3.11,
                Z_PERGOLA - 0.13, Z_PERGOLA, ink)
    lot_box("pergola_edge_a", -3.29, -0.11, -6.69, -6.58, Z_PERGOLA - 0.24, Z_PERGOLA, ink)
    lot_box("pergola_edge_b", -3.29, -0.11, -3.22, -3.11, Z_PERGOLA - 0.24, Z_PERGOLA, ink)
    for i, ps in enumerate((-2.90, -0.60)):
        lot_box(f"planter{i}", ps - 0.45, ps + 0.45, -5.40, -4.50,
                Z_DECK, Z_DECK + 0.55, verd)

    # --- the rest of the roof furniture --------------------------------------
    lot_box("stair_bulkhead", 2.60, 4.80, 1.60, 3.90, Z_DECK, 11.60, metal)
    lot_box("vent_a", 4.40, 4.90, -3.60, -3.10, Z_DECK, Z_DECK + 0.70, steel)
    lot_box("vent_b", 5.60, 6.10, 4.20, 4.70, Z_DECK, Z_DECK + 0.60, steel)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. The applied panels are small and numerous — their frames get a
    # token 1-segment softening and the fills, glow shells, gate leaves, bands
    # and pergola members none at all.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if (name.endswith(("_fill", "_glow", "_leaf", "_rail", "_soffit"))
                or name.startswith(("pergola_", "band_"))):
            continue
        if name.endswith(("_frame", "_reveal", "_box")) or name == "gable":
            bevel(obj, width=0.05, segments=1)
        elif name.startswith(("cylinder", "coping_", "deck_", "parapet_", "eaves_")):
            bevel(obj, width=0.06, segments=1)
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
    for tag, e in (("front(SouthPark)", EDGE_FRONT), ("party(84)", EDGE_PARTY),
                   ("yard-N", EDGE_YARD_N), ("yard-E", EDGE_YARD_E),
                   ("rear(TaberPl)", EDGE_REAR), ("alley(JackLondon)", EDGE_ALLEY)):
        _a, ln, _t, n = poly_edge(e)
        print(f"[build] edge {tag}: len={ln:.2f} outward normal="
              f"{math.degrees(math.atan2(n[0], n[1])) % 360:.1f} deg")
    print("[build] anchor lon/lat: -122.3941704 37.7818909 (modelled-footprint bbox centre)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "96-south-park.blend")
    glb = os.path.join(out, "96-south-park.glb")
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
