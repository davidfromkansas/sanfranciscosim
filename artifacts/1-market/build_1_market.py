"""Deterministic Blender build of the SF-SIM miniature 1 Market Street.

    blender -b --python build_1_market.py -- [--out DIR]

Writes 1-market.blend and 1-market.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint AABB centre (anchor lon -122.3948075,
lat 37.7938412), min Z = 0, rooftop plant cap top exactly 48.70 m.

Design (see REFERENCE.md for the sources behind every number):

* the DataSF surveyed polygon (block 3713 lot 006, mblr SF3713006), simplified to
  eight vertices — a U, not a box: three deep wings of Roman brick around a
  55.49 x 35.90 m courtyard that opens south-east to Mission Street. The 1916-17
  Southern Pacific Building, Bliss & Faville, eleven storeys;
* the crown is the subject: a very deep bracketed cornice over a colonnaded
  attic storey, top at the measured 46.10 m. Its projection is exaggerated,
  which is the one place the semantic-exaggeration budget is spent;
* the base is a two-storey cream terra-cotta arcade on all three street
  frontages, with the monumental arched portal at the centre of Market and a
  balcony on brackets over it;
* the shaft is the fine 2.25 m punched-window rhythm — 38 bays on Market, 29 on
  each flank — built as full-height brick mullion strips over per-storey glazing
  bands and cream sill courses, so the openings read small against a big brick
  field at city distance;
* the roof is a first-class elevation: the U-shaped deck inside the cornice
  parapet, two plant enclosures on the Market wing (the taller sets the 48.70 m
  crest), stair bulkheads and vents;
* the courtyard carries the glazed atrium roof of One Market Plaza. It is in
  scope because the exclusion radius that removes this building's procedural
  footprint necessarily removes the atrium's too — the two rings share a vertex
  7.3 m from the anchor — so without it the scene has a 55 x 36 m hole;
* night state: the atrium is the hero, glowing warm from a plate *under* the
  glazing (never a closed shell — the app draws _Glow in a separate layer at
  ~12% alpha per layer, so a shell reads as two layers by day and tints the
  surface); the base arcade is a continuous warm band; a sparse scatter of lit
  upper bays sits behind both.

Walls are SOLID prisms with no cut openings; every opening is drawn proud of the
wall and reads as a recess because the mullions and piers stand out in front of
it (style bible s.5). This is the 300 Brannan / 500 Third idiom and it is why
the model needs no booleans.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF footprint (ynuv-fyni, mblr SF3713006) projected with the app's tangent
# projection (LON0 -122.4375, LAT0 37.77), simplified to eight vertices, wall
# plane set 1.15 m inside the surveyed ring (the survey captures the cornice and
# base overhang), and recentred on the footprint AABB centre. CCW, (x east,
# y north). 3,643.9 m2 against the assessor's 3,669 m2 per-floor plate.
FOOTPRINT = [
    (-6.953, -53.483),    # v0  S corner   — Spear St x Mission St
    (3.257, -43.356),     # v1  inner corner of the Spear wing's Mission return
    (-22.025, -17.868),   # v2  Spear wing, court face
    (17.371, 21.210),     # v3  Market wing, court face — north-east end
    (42.653, -4.278),     # v4  Steuart wing, court face
    (53.537, 6.518),      # v5  inner corner of the Steuart wing's Mission return
    (6.952, 53.482),      # v6  N corner   — Market St x Steuart St
    (-53.538, -6.519),    # v7  W corner   — Market St x Spear St
]
E_MISS_S = (0, 1)    # Mission St return, Spear end, 14.38 m, normal 135.2 deg
E_CRT_SW = (1, 2)    # court face of the Spear wing, 35.90 m, normal 45.2
E_CRT_NW = (2, 3)    # court face of the Market wing, 55.49 m, normal 135.2
E_CRT_NE = (3, 4)    # court face of the Steuart wing, 35.90 m, normal 225.2
E_MISS_N = (4, 5)    # Mission St return, Steuart end, 15.33 m, normal 135.2
E_STEUART = (5, 6)   # Steuart Street flank, 66.15 m, normal 45.2
E_MARKET = (6, 7)    # Market Street front, 85.20 m, normal 315.2
E_SPEAR = (7, 0)     # Spear Street flank, 66.15 m, normal 225.2

STREET_EDGES = (E_MARKET, E_STEUART, E_SPEAR, E_MISS_N, E_MISS_S)
COURT_EDGES = (E_CRT_NW, E_CRT_NE, E_CRT_SW)

BAY = 2.25            # measured window pitch (rectified Street View elevation)
BAYS = {
    E_MARKET: 38, E_STEUART: 29, E_SPEAR: 29, E_MISS_N: 7, E_MISS_S: 6,
    E_CRT_NW: 24, E_CRT_NE: 16, E_CRT_SW: 16,
}
# arcade openings are two window bays wide
ARC_BAYS = {E_MARKET: 19, E_STEUART: 14, E_SPEAR: 14, E_MISS_N: 3, E_MISS_S: 3}

H_PLINTH = 0.55       # granite plinth under the terra-cotta base
H_ARC0, H_ARC1 = 1.10, 10.20   # arcade opening band
H_BASE = 13.00        # top of the two-storey terra-cotta base
H_BELT0, H_BELT1 = 13.00, 14.00   # base entablature + balustrade
H_ROOF = 44.10        # roof deck / underside of the crowning cornice
FLOORS_N = 8
FLOOR_H = (40.80 - H_BELT1) / FLOORS_N      # 3.35 m
FLOORS = tuple(H_BELT1 + i * FLOOR_H for i in range(FLOORS_N))
WIN_LO, WIN_HI = 0.80, 2.62   # glazing band within a floor
H_ATT0, H_ATT1 = 40.80, 44.10      # attic colonnade storey — a full storey
H_CORN0 = 44.60               # corona springs from the architrave
H_CORN1 = 45.55               # top of the corona
H_CREST_CORN = 46.10          # crowning cornice top — the architectural height
H_BULK = 47.10                # stair bulkheads
H_PLANT = 48.10               # plant enclosure walls
H_PLANT_CAP = 48.40           # plant enclosure cap
H_CREST = 48.70               # fan-bank disc top = the export's bounding-box top

# the glazed atrium roof of One Market Plaza, filling the court
H_ATR_EAVE = 35.20
H_ATR_APEX = 43.50

MUL_W = 0.95          # brick mullion strip width (2.25 m bay - 1.30 m opening)
MUL_D = 0.26          # mullion projection — this is what makes the bays read deep
PIER_D = 0.34         # arcade pier projection

BEVEL_W = 0.14
BEVEL_SEG = 2

PALETTE_HEX = {
    "Toy_brick": "c96f4a",
    "Toy_cream": "f2ede3",
    "Toy_sand": "ece4d4",
    "Toy_trim": "f3efe6",
    "Toy_stone": "d9d2c2",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_slate": "6f7883",
    "Toy_steel": "9aa0a6",
    "Toy_roofd": "45454a",
    "Toy_ink": "3a3530",
    "Toy_gold_Glow": "caa64a",
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


def poly_edge(edge):
    """(a, b, length, tangent unit, outward normal) for a CCW footprint edge."""
    a, b = FOOTPRINT[edge[0]], FOOTPRINT[edge[1]]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> this points outward
    return a, b, length, t, n


def offset_polygon(poly, d):
    """Miter offset of the footprint; positive d moves outward."""
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


# The building's own axes: U runs along the Market frontage toward Steuart
# (north-east), V points from Market into the block toward Mission (south-east).
# The model origin is the footprint AABB centre, which is also the centre of the
# outer diamond, so (u, v) = (0, 0) is that centre. The Market wall is at
# v = -33.07 and the Mission faces at v = +33.07.
def _axes():
    _, _, _, t_market, _ = poly_edge(E_MARKET)
    u = (-t_market[0], -t_market[1])          # north-east along Market
    v = (u[1], -u[0])                          # rotate -90 deg -> south-east
    return u, v


U, V = _axes()
V_MARKET_WALL = -33.07
V_COURT_NW = -2.83          # court face of the Market wing
V_MISSION = 33.07
U_COURT_SW, U_COURT_NE = -28.22, 27.27


def uv(u, v):
    return (U[0] * u + V[0] * v, U[1] * u + V[1] * v)


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


def bevel(obj, width=BEVEL_W, segments=BEVEL_SEG):
    """Miniature-style edge softening on the chunky solids (style bible s.4).

    Width is clamped to 40% of the object's thinnest dimension; without that,
    beveling a thin plate at full width collapses faces into zero-area triangles
    and flips signed volume.
    """
    thin = min(obj.dimensions)
    width = min(width, thin * 0.4)
    if width < 1e-4:
        return obj
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(
        bm,
        geom=list(bm.verts) + list(bm.edges),
        offset=width,
        segments=segments,
        profile=0.5,
        affect="EDGES",
        clamp_overlap=True,
    )
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(target := obj.data)
    bm.free()
    target.shade_flat()
    return obj


def ensure_outward(obj):
    """Guarantee positive signed volume — the validator's authoritative normals
    test for a union of closed solids."""
    me = obj.data
    me.calc_loop_triangles()
    vol = 0.0
    for tri in me.loop_triangles:
        a, b, c = (obj.matrix_world @ me.vertices[i].co for i in tri.vertices)
        vol += a.dot(b.cross(c)) / 6.0
    if vol > 0.0:
        return obj
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.reverse_faces(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    me.shade_flat()
    return obj


def prism(name, poly, z0, z1, mat, mat_caps=None):
    """Closed extrusion of the footprint (walls + both caps)."""
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


def ring_band(name, z0, z1, off_in, off_out, mat):
    """Closed band following the footprint: 4 loops, quads between."""
    lo_in = offset_polygon(FOOTPRINT, off_in)
    lo_out = offset_polygon(FOOTPRINT, off_out)
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


def quad_box(name, corners, z0, z1, mat):
    """Closed box from four CCW plan corners."""
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


def wall_box(name, edge, s0, s1, z0, z1, d_in, d_out, mat):
    """Box hung on a facade: s along the edge from its first vertex, d measured
    along the outward normal (negative = buried in the wall)."""
    a, _, _, t, n = poly_edge(edge)

    def p(s, d):
        return (a[0] + t[0] * s + n[0] * d, a[1] + t[1] * s + n[1] * d)

    return quad_box(name, [p(s0, d_in), p(s1, d_in), p(s1, d_out), p(s0, d_out)], z0, z1, mat)


def arch_plate(name, edge, s0, s1, z0, z1, rise, d_in, d_out, mat, segs=8):
    """A wall plate whose top is a round arch. Extruded along the facade normal,
    closed, so it survives the signed-volume normals test."""
    a, _, _, t, n = poly_edge(edge)
    half = (s1 - s0) / 2.0
    sc = (s0 + s1) / 2.0
    radius = (half * half + rise * rise) / (2.0 * rise)
    cz = z1 - radius
    profile = [(s0, z0), (s1, z0)]
    for k in range(segs + 1):
        frac = 1.0 - k / segs
        s = s0 + (s1 - s0) * frac
        dz = radius * radius - (s - sc) * (s - sc)
        profile.append((s, cz + math.sqrt(max(dz, 0.0))))
    npts = len(profile)

    def p(s, d):
        return (a[0] + t[0] * s + n[0] * d, a[1] + t[1] * s + n[1] * d)

    verts = []
    for d in (d_in, d_out):
        for s, z in profile:
            x, y = p(s, d)
            verts.append((x, y, z))
    faces = [tuple(range(npts - 1, -1, -1)), tuple(range(npts, 2 * npts))]
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    return new_mesh(name, verts, faces, [mat])


def uv_box(name, u, v, z0, z1, su, sv, mat):
    """Box centred at (u, v) in the building frame, su along U, sv along V."""
    corners = []
    for du, dv in ((-su / 2, -sv / 2), (su / 2, -sv / 2), (su / 2, sv / 2), (-su / 2, sv / 2)):
        corners.append(uv(u + du, v + dv))
    return quad_box(name, corners, z0, z1, mat)


def uv_cyl(name, u, v, z0, z1, radius, mat, segs=10):
    corners = []
    for k in range(segs):
        ang = 2 * math.pi * k / segs
        corners.append(uv(u + radius * math.cos(ang), v + radius * math.sin(ang)))
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [tuple(range(segs - 1, -1, -1)), tuple(range(segs, 2 * segs))]
    for i in range(segs):
        j = (i + 1) % segs
        faces.append((i, j, segs + j, segs + i))
    return new_mesh(name, verts, faces, [mat])


def hip_roof(name, u0, u1, v0, v1, z_eave, z_apex, ridge_frac, mat):
    """Closed hip roof over a (u, v) rectangle: 4 eave corners + a ridge along U.
    Bottom face closes the solid so signed volume stays positive."""
    uc, vc = (u0 + u1) / 2.0, (v0 + v1) / 2.0
    ru = (u1 - u0) * ridge_frac / 2.0
    pts = [uv(u0, v0), uv(u1, v0), uv(u1, v1), uv(u0, v1)]
    verts = [(x, y, z_eave) for x, y in pts]
    verts.append((*uv(uc - ru, vc), z_apex))
    verts.append((*uv(uc + ru, vc), z_apex))
    faces = [
        (3, 2, 1, 0),      # bottom
        (0, 1, 5, 4),      # long side v0
        (2, 3, 4, 5),      # long side v1
        (1, 2, 5),         # hip end u1
        (3, 0, 4),         # hip end u0
    ]
    return new_mesh(name, verts, faces, [mat])


# --------------------------------------------------------------- the build


def materials():
    mats = {}
    for name, rgb in PALETTE.items():
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        bsdf = m.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.85
        bsdf.inputs["Metallic"].default_value = 0.0
        # Workbench's MATERIAL colour mode reads diffuse_color, not the BSDF —
        # without this the fast review renders come out untinted grey.
        m.diffuse_color = (*rgb, 1.0)
        m.roughness = 0.85
        if name.endswith("_Glow"):
            bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 0.0
        mats[name] = m
    return mats


def bay_spans(edge, nbays, mul_w=MUL_W):
    """(s0, s1) of each opening, with a mullion between and at both ends."""
    _, _, length, _, _ = poly_edge(edge)
    bay = (length - (nbays + 1) * mul_w) / nbays
    out = []
    for k in range(nbays):
        s0 = mul_w + k * (bay + mul_w)
        out.append((s0, s0 + bay))
    return out, bay


def brick_elevation(tag, edge, mats, lit=(), court=False):
    """One shaft elevation: a dark glazing band per storey set slightly proud of
    the wall, full-height brick mullion strips standing 0.26 m in front of it,
    and a cream sill course under each band. The mullions are what make the
    small openings read as punched holes rather than a curtain wall."""
    nbays = BAYS[edge]
    _, _, length, _, _ = poly_edge(edge)
    _, bay = bay_spans(edge, nbays)
    brick, cream, glass = mats["Toy_brick"], mats["Toy_cream"], mats["Toy_glass"]
    sand = mats["Toy_sand"]
    d_out = MUL_D if not court else MUL_D * 0.6
    # brick spandrel bands stand proud with the mullions; the glazing sits 0.21 m
    # behind them, so the openings read as punched holes rather than a curtain
    # wall — and the wall never needs a boolean.
    edges_z = [H_BELT1]
    for fi, base in enumerate(FLOORS):
        edges_z += [base + WIN_LO, base + WIN_HI]
    edges_z.append(H_ATT0)
    for k in range(0, len(edges_z) - 1, 2):
        wall_box(f"{tag}_span{k}", edge, 0.0, length, edges_z[k], edges_z[k + 1],
                 -0.05, d_out, brick)
    for fi, base in enumerate(FLOORS):
        z0, z1 = base + WIN_LO, base + WIN_HI
        wall_box(f"{tag}_gl{fi}", edge, MUL_W * 0.5, length - MUL_W * 0.5, z0, z1,
                 -0.06, 0.05, glass)
        if not court:
            wall_box(f"{tag}_sill{fi}", edge, 0.25, length - 0.25, z0 - 0.22, z0 - 0.06,
                     -0.04, d_out + 0.07, sand)
    # full-height mullion strips
    for k in range(nbays + 1):
        s0 = k * (bay + MUL_W)
        wall_box(f"{tag}_mul{k}", edge, s0, s0 + MUL_W, H_BELT1, H_ATT0, -0.05,
                 d_out, brick)
    # a light string course at the seventh floor, where the real facade has its
    # run of small bracketed balconies
    if not court:
        wall_box(f"{tag}_string", edge, 0.25, length - 0.25, FLOORS[5] - 0.34,
                 FLOORS[5] - 0.02, -0.04, d_out + 0.34, cream)
    # night: a sparse scatter of lit bays
    spans, _ = bay_spans(edge, nbays)
    for fi, bi in lit:
        s0, s1 = spans[bi]
        base = FLOORS[fi]
        wall_box(f"{tag}_lit{fi}_{bi}", edge, s0 + 0.18, s1 - 0.18, base + WIN_LO + 0.14,
                 base + WIN_HI - 0.14, 0.06, 0.11, mats["Toy_glassl_Glow"])


def attic_colonnade(tag, edge, mats, court=False):
    """The colonnaded attic storey: a recessed dark band with one square-section
    terra-cotta colonnette per bay standing in front of it."""
    nbays = BAYS[edge]
    _, _, length, _, _ = poly_edge(edge)
    cream, glass = mats["Toy_cream"], mats["Toy_glass"]
    wall_box(f"{tag}_att", edge, 0.15, length - 0.15, H_ATT0 + 0.55, H_ATT1 - 0.45,
             -0.06, 0.06, glass)
    wall_box(f"{tag}_attsill", edge, 0.15, length - 0.15, H_ATT0, H_ATT0 + 0.55,
             -0.05, MUL_D + 0.24, cream)
    wall_box(f"{tag}_attlint", edge, 0.15, length - 0.15, H_ATT1 - 0.45, H_ATT1,
             -0.05, MUL_D + 0.24, cream)
    if court:
        return
    step = length / nbays
    for k in range(nbays + 1):
        s0 = min(max(k * step - 0.32, 0.0), length - 0.64)
        wall_box(f"{tag}_col{k}", edge, s0, s0 + 0.64, H_ATT0 + 0.55, H_ATT1 - 0.45,
                 -0.05, MUL_D + 0.20, cream)


def arcade(tag, edge, mats, portal=False):
    """The two-storey terra-cotta base: recessed openings between piers, with the
    monumental arched portal at the centre of the Market elevation."""
    nb = ARC_BAYS[edge]
    spans, _ = bay_spans(edge, nb, 1.60)
    _, _, length, _, _ = poly_edge(edge)
    glass, cream, gold = mats["Toy_glass"], mats["Toy_cream"], mats["Toy_gold_Glow"]
    mid = nb // 2
    # piers between the openings, standing 0.34 m proud of the base wall face
    for k in range(nb + 1):
        _, bw = bay_spans(edge, nb, 1.60)
        ps = k * (bw + 1.60)
        bevel(wall_box(f"{tag}_pier{k}", edge, ps, ps + 1.60, H_PLINTH, H_ARC1 + 1.15,
                       0.10, 0.34 + PIER_D, cream), width=0.09, segments=1)
    for bi, (s0, s1) in enumerate(spans):
        if portal and bi == mid:
            continue
        arch_plate(f"{tag}_arc{bi}", edge, s0, s1, H_ARC0, H_ARC1, 1.35, 0.22, 0.40,
                   glass)
        # night: a warm band low in every opening
        wall_box(f"{tag}_arcglow{bi}", edge, s0 + 0.55, s1 - 0.55, H_ARC0 + 0.45,
                 H_ARC0 + 1.60, 0.41, 0.45, gold)
    if portal:
        p0, p1 = spans[mid]
        p0, p1 = p0 - 2.10, p1 + 2.10
        bevel(arch_plate(f"{tag}_portal_sur", edge, p0 - 0.85, p1 + 0.85, H_PLINTH,
                         H_ARC1 + 2.20, 3.40, 0.10, 0.86, cream), width=0.10)
        arch_plate(f"{tag}_portal", edge, p0, p1, H_ARC0 - 0.55, H_ARC1 + 1.30, 2.85,
                   0.70, 0.92, mats["Toy_ink"])
        wall_box(f"{tag}_portalglow", edge, p0 + 0.62, p1 - 0.62, H_ARC0 + 0.10,
                 H_ARC0 + 3.10, 0.93, 0.97, gold)
    return spans


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    mats = materials()

    brick = mats["Toy_brick"]
    cream = mats["Toy_cream"]
    sand = mats["Toy_sand"]
    stone = mats["Toy_stone"]
    slate = mats["Toy_slate"]
    steel = mats["Toy_steel"]
    roofd = mats["Toy_roofd"]
    ink = mats["Toy_ink"]

    # ---- 1. body + roof deck ---------------------------------------------- #
    bevel(prism("body", FOOTPRINT, 0.0, H_ROOF, brick, mat_caps=slate), width=0.18)

    # ---- 2. the terra-cotta base ------------------------------------------ #
    bevel(ring_band("plinth", 0.0, H_PLINTH, -0.10, 0.42, stone), width=0.08)
    bevel(ring_band("base", H_PLINTH, H_BASE, -0.10, 0.34, cream), width=0.10)
    for tag, edge in (("market", E_MARKET), ("steuart", E_STEUART), ("spear", E_SPEAR),
                      ("missn", E_MISS_N), ("misss", E_MISS_S)):
        arcade(tag, edge, mats, portal=(edge is E_MARKET))
    # base entablature: cornice band, frieze, balustrade
    bevel(ring_band("belt", H_BELT0 - 0.55, H_BELT0, -0.14, 0.92, cream), width=0.10)
    bevel(ring_band("frieze", H_BELT0, H_BELT1 - 0.34, -0.10, 0.50, sand), width=0.07)
    bevel(ring_band("balus", H_BELT1 - 0.34, H_BELT1, -0.14, 0.70, cream), width=0.06)

    # the balcony over the Market portal, on three brackets
    _, _, l_mkt, _, _ = poly_edge(E_MARKET)
    bcen = l_mkt / 2.0
    for k, ds in enumerate((-3.4, 0.0, 3.4)):
        bevel(wall_box(f"balc_brk{k}", E_MARKET, bcen + ds - 0.45, bcen + ds + 0.45,
                       H_BELT0 - 1.55, H_BELT0 - 0.25, 0.80, 1.95, cream), width=0.10)
    bevel(wall_box("balc_slab", E_MARKET, bcen - 4.6, bcen + 4.6, H_BELT0 - 0.25,
                   H_BELT0 + 0.20, 0.70, 2.35, cream), width=0.08)
    bevel(wall_box("balc_rail", E_MARKET, bcen - 4.6, bcen + 4.6, H_BELT0 + 0.20,
                   H_BELT0 + 1.15, 2.00, 2.35, cream), width=0.07)

    # ---- 3. the shaft ------------------------------------------------------ #
    lit_market = {(0, 3), (1, 11), (1, 26), (2, 6), (2, 19), (3, 31), (4, 1),
                  (4, 14), (5, 23), (5, 35), (6, 9), (7, 17), (7, 29)}
    lit_steuart = {(0, 21), (1, 5), (2, 13), (3, 25), (4, 2), (5, 17), (6, 9), (7, 27)}
    lit_spear = {(1, 8), (2, 22), (4, 4), (5, 15), (7, 25)}
    brick_elevation("market", E_MARKET, mats, lit_market)
    brick_elevation("steuart", E_STEUART, mats, lit_steuart)
    brick_elevation("spear", E_SPEAR, mats, lit_spear)
    brick_elevation("missn", E_MISS_N, mats, {(2, 3), (5, 1)})
    brick_elevation("misss", E_MISS_S, mats, {(3, 2), (6, 4)})
    for tag, edge in (("crtnw", E_CRT_NW), ("crtne", E_CRT_NE), ("crtsw", E_CRT_SW)):
        brick_elevation(tag, edge, mats, court=True)

    # ---- 4. the attic colonnade and the crowning cornice ------------------- #
    for tag, edge in (("market", E_MARKET), ("steuart", E_STEUART), ("spear", E_SPEAR),
                      ("missn", E_MISS_N), ("misss", E_MISS_S)):
        attic_colonnade(tag, edge, mats)
    for tag, edge in (("crtnw", E_CRT_NW), ("crtne", E_CRT_NE), ("crtsw", E_CRT_SW)):
        attic_colonnade(tag, edge, mats, court=True)
    # the crown: architrave, deep bracketed corona, cap. Its projection is
    # exaggerated ~25% over the survey, on purpose — it is the silhouette.
    bevel(ring_band("corn_arch", H_ROOF, H_CORN0, -0.12, 0.60, cream), width=0.09)
    bevel(ring_band("corn_corona", H_CORN0, H_CORN1, -0.16, 1.85, cream), width=0.12)
    bevel(ring_band("corn_cap", H_CORN1, H_CREST_CORN, -0.20, 1.55, sand), width=0.10)

    # ---- 5. the roof ------------------------------------------------------- #
    # Plant enclosures on the Market wing (v negative). The taller one is the
    # crest and the only thing that breaks the cornice silhouette.
    vm = (V_MARKET_WALL + V_COURT_NW) / 2.0     # -17.95, centre of the Market wing
    bevel(uv_box("plant_pad", -6.0, vm + 1.0, H_ROOF, H_ROOF + 0.30, 30.0, 11.0, stone),
          width=0.08)
    for i, (u, sv) in enumerate(((-17.0, 8.4), (2.0, 8.4))):
        bevel(uv_box(f"plant{i}", u, vm + 1.0, H_ROOF + 0.30, H_PLANT, 11.0, sv, slate),
              width=0.16)
        bevel(uv_box(f"plant_cap{i}", u, vm + 1.0, H_PLANT, H_PLANT_CAP, 11.6,
                     sv + 0.6, steel), width=0.10)
        for k in range(3):
            bevel(uv_cyl(f"fan{i}_{k}", u - 3.4 + k * 3.4, vm + 1.0, H_PLANT_CAP,
                         H_CREST, 1.55, steel, segs=10), width=0.07)
    bevel(uv_box("bulk_a", 20.0, vm - 3.0, H_ROOF, H_BULK, 6.0, 5.0, slate), width=0.14)
    bevel(uv_box("bulk_a_cap", 20.0, vm - 3.0, H_BULK, H_BULK + 0.28, 6.4, 5.4, steel),
          width=0.08)
    bevel(uv_box("bulk_b", 33.0, vm + 4.0, H_ROOF, H_ROOF + 2.10, 5.0, 4.4, slate),
          width=0.12)
    # flank-wing furniture
    for i, (u, v, su, sv, h) in enumerate((
        (36.0, 10.0, 4.2, 3.0, 1.30), (36.5, 22.0, 3.4, 3.4, 0.95),
        (-36.0, 8.0, 4.2, 3.0, 1.30), (-36.5, 21.0, 3.4, 3.4, 0.95),
        (-24.0, vm - 8.0, 3.0, 2.4, 0.90), (10.0, vm - 8.5, 3.0, 2.4, 0.90),
        (28.0, vm + 6.0, 2.6, 2.2, 0.80), (-32.0, vm + 6.0, 2.6, 2.2, 0.80),
    )):
        bevel(uv_box(f"vent{i}", u, v, H_ROOF, H_ROOF + h, su, sv, roofd), width=0.07)
    for i, (u, v, su) in enumerate(((-8.0, vm - 9.5, 22.0), (36.0, 16.0, 9.0),
                                    (-36.0, 15.0, 9.0))):
        bevel(uv_box(f"duct{i}", u, v, H_ROOF, H_ROOF + 0.60, su, 1.10, steel), width=0.06)
    uv_box("walk_a", 0.0, vm - 12.0, H_ROOF, H_ROOF + 0.07, 62.0, 3.0, stone)
    uv_box("walk_b", 36.0, 14.0, H_ROOF, H_ROOF + 0.07, 3.0, 26.0, stone)
    uv_box("walk_c", -36.0, 13.0, H_ROOF, H_ROOF + 0.07, 3.0, 26.0, stone)

    # ---- 6. the glazed atrium roof over the court -------------------------- #
    au0, au1 = U_COURT_SW + 0.45, U_COURT_NE - 0.45
    av0, av1 = V_COURT_NW + 0.45, V_MISSION - 0.45
    bevel(hip_roof("atrium_glass", au0, au1, av0, av1, H_ATR_EAVE, H_ATR_APEX, 0.34,
                   mats["Toy_glassl"]), width=0.10)
    # a light eaves gutter and a ridge cap — nothing else. Segmented hip members
    # read as a staircase of blocks at this scale, so the glazed planes carry it.
    bevel(uv_box("atrium_eave", (au0 + au1) / 2, (av0 + av1) / 2, H_ATR_EAVE - 0.55,
                 H_ATR_EAVE + 0.12, au1 - au0 + 0.75, av1 - av0 + 0.75, cream), width=0.09)
    uc, vc = (au0 + au1) / 2, (av0 + av1) / 2
    ru = (au1 - au0) * 0.34 / 2
    bevel(uv_box("atrium_ridge", uc, vc, H_ATR_APEX - 0.26, H_ATR_APEX + 0.18,
                 2 * ru + 1.1, 1.05, cream), width=0.09)
    # Night hero: the glazed roof itself lights up. The glow has to sit OUTSIDE
    # the opaque glazing — a plate tucked under it is simply invisible — so this
    # is a thin shell 0.12 m proud of the glass. A closed shell stacks two alpha
    # layers and reads ~23% by day, which is why its colour is the glazing's own
    # `Toy_glassl` value: by day the overlay is invisible, at night the whole
    # hip becomes a cool lantern over the court.
    hip_roof("atrium_glow", au0 - 0.12, au1 + 0.12, av0 - 0.12, av1 + 0.12,
             H_ATR_EAVE - 0.12, H_ATR_APEX + 0.12, 0.34, mats["Toy_glassl_Glow"])

    return scene


def finish():
    for obj in [o for o in bpy.data.objects if o.type == "MESH"]:
        ensure_outward(obj)


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
        o.evaluated_get(dg).to_mesh_clear()
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print("[build] anchor lon/lat: -122.3948075 37.7938412 (footprint AABB centre)")
    print("[build] Market normal 315.2 deg true; Steuart 45.2; Spear 225.2; Mission 135.2")
    print(f"[build] floor height {FLOOR_H:.3f} m; deck {H_ROOF}; cornice {H_CREST_CORN}; crest {H_CREST}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    finish()
    report()

    blend = os.path.join(out, "1-market.blend")
    glb = os.path.join(out, "1-market.glb")
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
