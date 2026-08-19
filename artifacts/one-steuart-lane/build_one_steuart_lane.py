"""Deterministic Blender build of the SF-SIM miniature One Steuart Lane.

    blender -b --python build_one_steuart_lane.py -- [--out DIR]

Writes one-steuart-lane.blend and one-steuart-lane.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the loader
applies no rotation. Origin = footprint AABB centre (anchor lon -122.3916888,
lat 37.7915643), min Z = 0, mechanical penthouse cap top exactly 67.06 m.

Design (see REFERENCE.md for the sources behind every number):

* SOM, 2021, for Paramount Group; 20 storeys, 220 ft (67.06 m) to the crest, on
  the 1,904 m2 lot of the demolished 75 Howard Street parking garage;
* the identity is the STACK: five volumes of three-to-four storeys sitting on a
  two-storey base, each stepping back from the one below **on alternating pairs
  of sides**, so from any corner the silhouette zig-zags. Everything else in this
  script is subordinate to that;
* second identity is the TRAVERTINE CAGE — continuous cream pilasters and lintels
  standing 0.37 m proud of glass that is always recessed behind them. The bay
  module is deliberately irregular (the real curtain wall cycles 4 / 6 / 8 ft
  panels), so the vertical rhythm is syncopated, never uniform;
* between every pair of volumes is one open terrace storey: a thin bright
  cantilevered slab plate on the lower volume's plan, a dark soffit, a clear
  glass balustrade set in from the edge, and planters;
* one module-wide slot of DEEP terraces runs the full height of each elevation —
  the "single bay of deep terraces running up each side" of the Chronicle's
  description;
* the base is a double-height dark storefront divided by clusters of vertical
  travertine baguettes, with the Steuart Lane entrance under a projecting flat
  glass canopy, and a set-back planted amenity level above it;
* the roof is a working roof, because the camera looks down: cream parapet ring,
  a field of dark PV strips, two round cooling towers in a mechanical yard, the
  mechanical penthouse box (the crest at 67.06 m), and a BMU crane on its track;
* night state: the real building is downlit from under its cantilevers, so the
  hero glow is a thin warm line under each of the four terrace slabs plus the
  base cornice — five horizontal bands that restate the horizontal massing —
  with a warm lobby band on Steuart Lane and a sparse scatter of lit units
  behind it. Nothing else glows.

Walls are SOLID prisms with no cut openings; every surface is drawn PROUD of the
shell and the openings read as recesses because the frame stands in front of the
glass (style bible s.5). This is the 300 Brannan / 500 Third idiom and it is why
the model needs no booleans. The one trap: a plate authored at a NEGATIVE offset
is buried inside the shell and renders as nothing at all — the first version of
this script recessed the glass that way and the whole tower came out blank cream. The stone bars are deliberately NOT bevelled: they are
hairline strips, a bevel doubles their triangle count and reads as nothing at the
app's scale.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/667097308 projected with the app's tangent projection
# (LON0 -122.4375, LAT0 37.77) and recentred on the footprint AABB centre.
# CCW, (x east, y north). 1,904.1 m2 against SOM's published 20,595 sq ft
# (1,913.3 m2) site area, -0.5%.
FOOTPRINT = [
    (2.020, 30.824),     # v0  N corner — Steuart St x Howard St
    (-31.049, -2.338),   # v1  W corner — Howard St x south-west lot line
    (-2.072, -30.824),   # v2  S corner — south-west x south-east lot lines
    (31.049, 2.548),     # v3  E corner — south-east lot line x Steuart St
]
E_HOWARD = (0, 1)    # NW frontage, 46.83 m, outward normal 314.9 deg true
E_SW = (1, 2)        # SW flank, 40.63 m, normal 224.5 deg — block interior
E_SE = (2, 3)        # SE flank, 47.02 m, normal 134.8 deg — block interior
E_STEUART = (3, 0)   # NE frontage, 40.52 m, normal 44.2 deg — the Bay elevation
EDGES = (E_STEUART, E_SE, E_SW, E_HOWARD)
EDGE_TAGS = ("ne", "se", "sw", "nw")

# ---- the stack ----------------------------------------------------------- #
# 20 storeys: a two-storey base, then 18 storeys distributed 3 / 4 / 4 / 4 / 3
# across five volumes (each volume after the first swallows the recessed terrace
# storey below it, which is how the real building reads — the terrace floor sits
# in the same plane as the volume above).
H_GF = 5.80          # double-height retail / lobby storey
H_BASE = 9.80        # top of the two-storey base
H_DECK = 63.494      # roof deck at the top of volume E
FLOOR_H = (H_DECK - H_BASE) / 18.0    # 2.983 m

H_PAR = 64.55        # parapet coping top
H_CREST = 67.06      # mechanical penthouse cap = 220 ft = the bbox top

SLAB_T = 0.34        # cantilevered terrace slab plate thickness
SLAB_OUT = 0.30      # how far the slab plate oversails its volume

# Per-volume (z0, z1) and per-edge insets in metres, ordered as EDGES:
# (Steuart NE, south-east, south-west, Howard NW).
#
# The insets ALTERNATE rather than shrink monotonically: each volume pulls back
# hard on one pair of sides while coming back OUT over the volume below on the
# other pair, so every junction is a step on every elevation and the corner
# zig-zags. A ziggurat of concentric setbacks was the first thing this script
# built and it read as a wedding cake, which is exactly what SOM did not do —
# SF YIMBY describes "five masses CANTILEVERED over ... private terraces".
#
# Cross-check on the numbers: these plans give ~29,600 m2 of gross floor area
# against the published 335,000 sq ft (31,120 m2), -5%. That agreement is the
# only evidence the setback depths are the right size, since none of them are
# published.
VOLUMES = [
    # tag, z0,                 z1,                  insets (NE, SE, SW, NW)
    ("A", H_BASE,              H_BASE + 3 * FLOOR_H,  (0.0, 0.0, 0.0, 0.0)),
    ("B", H_BASE + 3 * FLOOR_H + SLAB_T, H_BASE + 7 * FLOOR_H,  (4.6, 0.6, 4.8, 0.8)),
    ("C", H_BASE + 7 * FLOOR_H + SLAB_T, H_BASE + 11 * FLOOR_H, (0.8, 5.4, 1.0, 5.6)),
    ("D", H_BASE + 11 * FLOOR_H + SLAB_T, H_BASE + 15 * FLOOR_H, (5.6, 1.4, 5.8, 1.6)),
    ("E", H_BASE + 15 * FLOOR_H + SLAB_T, H_DECK,               (1.8, 6.6, 2.0, 6.8)),
]

# ---- the facade cage ----------------------------------------------------- #
# The real curtain wall cycles 4 / 6 / 8 ft panels. Modelled one-for-one that is
# ~19 modules across a 47 m elevation, which at the app's scale is a field of
# noise rather than a grid. The miniature keeps the RATIO and the syncopation but
# groups the panels roughly 3:2, landing 11-13 bays per elevation.
PIL_W = 0.58         # travertine pilaster width
GLASS_D = 0.07       # glass plate, drawn just PROUD of the volume shell
FRAME_D = 0.44       # frame face; FRAME_D - GLASS_D is the depth of every recess
LINTEL_H = 0.70      # travertine lintel band at every floor line
MOD_TARGET = 3.05    # mean bay module
MOD_PATTERN = (3.66, 2.75, 1.83, 2.75, 3.66, 2.75, 1.83, 3.66, 2.75, 1.83, 2.75, 3.66)

DEEP_BAY = {"ne": 3, "se": 5, "sw": 4, "nw": 6}   # index of the deep-terrace slot
DEEP_D = 1.45        # how far the deep bay is carved back

BEVEL_W = 0.13
BEVEL_SEG = 2

PALETTE_HEX = {
    "Toy_cream": "f2ede3",       # travertine — pilasters, lintels, parapet, slabs
    "Toy_sand": "ece4d4",        # base band stone, one step down
    "Toy_stone": "d9d2c2",       # terrace soffits
    "Toy_glass": "2a4d73",       # recessed vision glass — supplies all the dark
    "Toy_glassl": "6f95b8",      # sky-reflecting panes and balustrades
    "Toy_ink": "3a3530",         # blackened stainless: mullion caps, rails, fittings
    "Toy_steel": "9aa0a6",       # roof deck and plant  (NOT Toy_roofd — reads black)
    "Toy_navy": "2c4a70",        # rooftop photovoltaic array
    "Toy_sage": "8fa88a",        # terrace and street planting
    "Toy_bronze": "8a6a3f",      # entrance portal
    "Toy_cream_Glow": "f2ede3",  # hero: the under-slab downlight line
    "Toy_gold_Glow": "caa64a",   # the lobby band
    "Toy_glassl_Glow": "6f95b8",  # scattered lit units
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def poly_edge(poly, edge):
    """(a, b, length, tangent unit, outward normal) for a CCW polygon edge."""
    a, b = poly[edge[0]], poly[edge[1]]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> this points outward
    return a, b, length, t, n


def offset_polygon(poly, d):
    """Miter offset; positive d moves outward. `d` may be a scalar or one value
    per edge (edge i runs from vertex i to vertex i+1)."""
    npts = len(poly)
    ds = [d] * npts if isinstance(d, (int, float)) else list(d)
    normals = []
    for i in range(npts):
        a, b = poly[i], poly[(i + 1) % npts]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        normals.append((dy / length, -dx / length))
    out = []
    for i in range(npts):
        n1, n2 = normals[i - 1], normals[i]
        d1, d2 = ds[i - 1], ds[i]
        v = poly[i]
        det = n1[0] * n2[1] - n1[1] * n2[0]
        if abs(det) < 1e-6:
            out.append((v[0] + n2[0] * d2, v[1] + n2[1] * d2))
            continue
        c1 = v[0] * n1[0] + v[1] * n1[1] + d1
        c2 = v[0] * n2[0] + v[1] * n2[1] + d2
        out.append(((c1 * n2[1] - c2 * n1[1]) / det, (c2 * n1[0] - c1 * n2[0]) / det))
    return out


def volume_plan(insets):
    """Footprint inset per edge. EDGES order is (NE, SE, SW, NW); the polygon's
    own edge order is (NW, SW, SE, NE), so remap rather than trusting either."""
    per_edge = [0.0] * len(FOOTPRINT)
    for edge, inset in zip(EDGES, insets):
        per_edge[edge[0]] = -inset
    return offset_polygon(FOOTPRINT, per_edge)


# The building's own axes for roof layout: U runs along the Steuart frontage
# (south-east positive), V points out toward Steuart (north-east).
_, _, _, U, V = poly_edge(FOOTPRINT, E_STEUART)
U = (-U[0], -U[1])


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
    and flips signed volume."""
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
    """Closed extrusion of a plan polygon (walls + both caps)."""
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
    """Closed band following a plan polygon: 4 loops, quads between."""
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


def wall_box(name, poly, edge, s0, s1, z0, z1, d_in, d_out, mat):
    """Box hung on a facade: s runs along the edge from its first vertex, d is
    measured along the outward normal (negative = buried in the wall)."""
    a, _, _, t, n = poly_edge(poly, edge)

    def p(s, d):
        return (a[0] + t[0] * s + n[0] * d, a[1] + t[1] * s + n[1] * d)

    return quad_box(name, [p(s0, d_in), p(s1, d_in), p(s1, d_out), p(s0, d_out)], z0, z1, mat)


def uv_box(name, u, v, z0, z1, su, sv, mat):
    corners = [uv(u + du, v + dv) for du, dv in
               ((-su / 2, -sv / 2), (su / 2, -sv / 2), (su / 2, sv / 2), (-su / 2, sv / 2))]
    return quad_box(name, corners, z0, z1, mat)


def uv_cyl(name, u, v, z0, z1, radius, mat, segs=12):
    corners = [uv(u + radius * math.cos(2 * math.pi * k / segs),
                  v + radius * math.sin(2 * math.pi * k / segs)) for k in range(segs)]
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [tuple(range(segs - 1, -1, -1)), tuple(range(segs, 2 * segs))]
    for i in range(segs):
        j = (i + 1) % segs
        faces.append((i, j, segs + j, segs + i))
    return new_mesh(name, verts, faces, [mat])


# --------------------------------------------------------------- the facade


def module_spans(length):
    """Bay openings along an elevation, tiled symmetrically about its centre from
    the irregular 4 / 6 / 8 ft pattern and scaled to fit exactly. Returns
    [(s0, s1), ...] for the openings; the pilasters are the gaps between them
    plus one at each end."""
    nmods = max(3, int(round((length - PIL_W) / (MOD_TARGET + PIL_W))))
    widths = [MOD_PATTERN[i % len(MOD_PATTERN)] for i in range(nmods)]
    scale = (length - (nmods + 1) * PIL_W) / sum(widths)
    widths = [w * scale for w in widths]
    spans, s = [], PIL_W
    for w in widths:
        spans.append((s, s + w))
        s += w + PIL_W
    return spans


def elevation(tag, poly, edge, z0, z1, floors, mats, deep_idx, lit, openness=0.0):
    """One elevation of one volume, built as three layers standing proud of the
    solid shell: a dark glass plate just outside it, then the travertine cage —
    a cream lintel at every floor line and a cream pilaster at every module
    boundary — standing FRAME_D in front of that glass. One module is treated as
    the deep terrace bay: its glass sits flush with the shell and gets a slab and
    a balustrade per floor, so it reads as a loggia carved out of the cage."""
    _, _, length, _, _ = poly_edge(poly, edge)
    spans = module_spans(length)
    frame_d = FRAME_D + openness
    cream, glass, glassl, ink, stone = (mats["Toy_cream"], mats["Toy_glass"],
                                        mats["Toy_glassl"], mats["Toy_ink"],
                                        mats["Toy_stone"])

    # the glass plate — one box for the whole elevation, just proud of the shell
    wall_box(f"{tag}_glass", poly, edge, 0.0, length, z0, z1, -0.05, GLASS_D, glass)

    # the deep terrace bay: glass held back at the shell, with a slab and a rail
    # per floor standing in front of it
    di = deep_idx % len(spans)
    ds0, ds1 = spans[di]
    wall_box(f"{tag}_deep", poly, edge, ds0, ds1, z0, z1, -0.05, -0.02, stone)
    for fi in range(floors):
        zf = z0 + fi * FLOOR_H
        wall_box(f"{tag}_deckd{fi}", poly, edge, ds0, ds1, zf, zf + 0.20,
                 -0.04, frame_d - 0.10, cream)
        wall_box(f"{tag}_raild{fi}", poly, edge, ds0 + 0.10, ds1 - 0.10,
                 zf + 0.20, zf + 1.05, frame_d - 0.26, frame_d - 0.16, glassl)

    # lintels: a cream band at every floor line, plus one closing the volume top
    for fi in range(floors + 1):
        zf = min(z0 + fi * FLOOR_H, z1 - LINTEL_H)
        wall_box(f"{tag}_lint{fi}", poly, edge, 0.0, length, zf, zf + LINTEL_H,
                 -0.05, frame_d, cream)

    # pilasters: one at each end of every module opening
    stops = sorted({0.0, length} | {t for span in spans for t in span})
    for k, t in enumerate(stops):
        s0 = min(max(t - PIL_W / 2, 0.0), length - PIL_W)
        wall_box(f"{tag}_pil{k}", poly, edge, s0, s0 + PIL_W, z0, z1,
                 -0.05, frame_d, cream)

    # blackened-steel mullion caps: a hairline dark line down the wider modules
    for bi, (s0, s1) in enumerate(spans):
        if bi % 3 or bi == di or openness:
            continue
        sm = (s0 + s1) / 2
        wall_box(f"{tag}_mull{bi}", poly, edge, sm - 0.06, sm + 0.06, z0, z1,
                 GLASS_D - 0.02, GLASS_D + 0.09, ink)

    # night: a sparse scatter of lit units, never a whole floor, never a pattern
    for fi, bi in lit:
        if fi >= floors:
            continue
        s0, s1 = spans[bi % len(spans)]
        zf = z0 + fi * FLOOR_H
        wall_box(f"{tag}_lit{fi}_{bi}", poly, edge, s0 + 0.30, s1 - 0.30,
                 zf + LINTEL_H + 0.28, zf + FLOOR_H - 0.34,
                 GLASS_D, GLASS_D + 0.11, mats["Toy_glassl_Glow"])


# Scattered so no floor and no bay column reads as a band. Chosen per volume.
LIT = {
    ("A", "ne"): {(0, 3), (2, 9)},
    ("A", "se"): {(1, 2), (2, 12)},
    ("A", "sw"): {(0, 8)},
    ("A", "nw"): {(1, 5), (2, 14)},
    ("B", "ne"): {(1, 1), (3, 11)},
    ("B", "se"): {(0, 7), (2, 3)},
    ("B", "sw"): {(3, 10)},
    ("B", "nw"): {(1, 13), (2, 2)},
    ("C", "ne"): {(0, 6), (3, 2)},
    ("C", "se"): {(1, 10)},
    ("C", "sw"): {(2, 4), (3, 12)},
    ("C", "nw"): {(0, 9), (2, 1)},
    ("D", "ne"): {(2, 7)},
    ("D", "se"): {(0, 4), (3, 9)},
    ("D", "sw"): {(1, 6)},
    ("D", "nw"): {(3, 3), (1, 11)},
    ("E", "ne"): {(1, 5)},
    ("E", "se"): {(0, 8), (2, 2)},
    ("E", "sw"): set(),
    ("E", "nw"): {(2, 6)},
}


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
        if name.endswith("_Glow"):
            bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 0.0
        mats[name] = m
    return mats


def build_base(mats):
    """Two storeys: a double-height dark storefront divided by clusters of
    vertical travertine baguettes, a stone band, and a set-back planted amenity
    level above it. Every plate stands proud of the shell, as on the tower."""
    cream, sand, glass, ink = (mats["Toy_cream"], mats["Toy_sand"],
                               mats["Toy_glass"], mats["Toy_ink"])
    bevel(prism("base_body", FOOTPRINT, 0.0, H_BASE, sand, mat_caps=cream), width=0.16)

    for tag, edge in zip(EDGE_TAGS, EDGES):
        _, _, length, _, _ = poly_edge(FOOTPRINT, edge)
        # the dark storefront plane
        wall_box(f"{tag}_store", FOOTPRINT, edge, 0.35, length - 0.35, 0.35, H_GF - 0.80,
                 -0.05, 0.06, glass)
        # travertine baguettes: clusters of slender fins in front of the shopfronts
        nclust = max(3, int(length // 7.0))
        for c in range(nclust):
            uc = (c + 0.5) * length / nclust
            for f in range(4):
                sf = uc - 0.66 + f * 0.44
                wall_box(f"{tag}_bag{c}_{f}", FOOTPRINT, edge, sf, sf + 0.16,
                         0.35, H_GF - 0.80, 0.02, 0.30, cream)
        # the stone band capping the ground storey
        wall_box(f"{tag}_band", FOOTPRINT, edge, 0.0, length, H_GF - 0.80, H_GF + 0.35,
                 -0.05, 0.34, cream)
        # amenity level: glass held at the shell behind a planted terrace ledge
        wall_box(f"{tag}_am", FOOTPRINT, edge, 0.30, length - 0.30, H_GF + 0.35,
                 H_BASE - 0.60, -0.05, 0.04, glass)
        wall_box(f"{tag}_amsoff", FOOTPRINT, edge, 0.0, length, H_BASE - 0.60, H_BASE,
                 -0.05, 0.30, cream)
        for p in range(3):
            sp = (p + 0.5) * length / 3.0
            bevel(wall_box(f"{tag}_amplant{p}", FOOTPRINT, edge, sp - 1.2, sp + 1.2,
                           H_GF + 0.35, H_GF + 1.20, 0.06, 0.28,
                           mats["Toy_sage"]), width=0.07)
        # night: the base cornice downlight, the fifth band of the glow composition
        wall_box(f"{tag}_baseglow", FOOTPRINT, edge, 0.6, length - 0.6,
                 H_GF - 0.98, H_GF - 0.84, 0.10, 0.32, mats["Toy_cream_Glow"])

    # the Steuart Lane entrance: bronze portal under a projecting glass canopy
    _, _, length, _, _ = poly_edge(FOOTPRINT, E_STEUART)
    se = length * 0.24
    bevel(wall_box("entry_portal", FOOTPRINT, E_STEUART, se - 2.4, se + 2.4, 0.0, 5.10,
                   0.02, 0.34, mats["Toy_bronze"]), width=0.08)
    wall_box("entry_door", FOOTPRINT, E_STEUART, se - 1.5, se + 1.5, 0.10, 4.20,
             0.32, 0.42, ink)
    bevel(wall_box("entry_canopy", FOOTPRINT, E_STEUART, se - 2.8, se + 2.8, 5.10, 5.34,
                   0.10, 3.50, cream), width=0.07, segments=1)
    for k in (-1, 1):
        wall_box(f"entry_fin{k}", FOOTPRINT, E_STEUART, se + k * 2.65, se + k * 2.65 + 0.12,
                 5.34, 5.90, 0.30, 3.30, mats["Toy_glassl"])
    # the lobby band — the one warm accent at street level
    wall_box("entry_glow", FOOTPRINT, E_STEUART, se + 3.6, se + 15.0, 1.20, 3.90,
             0.07, 0.19, mats["Toy_gold_Glow"])


def build_roof(plan, mats):
    """A working roof, because the camera looks down: parapet ring, PV strips, two
    round cooling towers in a mechanical yard, the penthouse box (the crest) and
    a BMU crane on its track.

    Everything here is laid out in the building frame (U along the Steuart edge,
    V out toward Steuart) and must fit inside VOLUME E's plan, not the footprint's
    — E is 27 m along U against the lot's 47 m, and roof furniture sized for the
    lot hangs off the tower in mid-air."""
    cream, steel, navy, ink = (mats["Toy_cream"], mats["Toy_steel"],
                               mats["Toy_navy"], mats["Toy_ink"])
    ring_band("parapet", plan, H_DECK, H_PAR, -0.45, 0.02, cream)
    prism("roof_deck", offset_polygon(plan, -0.45), H_DECK - 0.10, H_DECK + 0.04, steel)

    _, _, u_len, _, _ = poly_edge(plan, E_STEUART)   # extent along U
    _, _, v_len, _, _ = poly_edge(plan, E_SE)        # extent along V
    hu, hv = u_len / 2 - 1.6, v_len / 2 - 2.4

    # Photovoltaic field: parallel strips running along V in two bays split by a
    # pale walkway, filling roughly half the deck. Google's z21 imagery shows the
    # array covering the north-west half with the plant yard opposite.
    for i in range(10):
        u = -hu + 0.9 + i * 1.95
        uv_box(f"pv{i}", u, hv - 8.6, H_DECK + 0.04, H_DECK + 0.50, 1.45, 16.0, navy)
    for i in range(7):
        u = -hu + 0.9 + i * 1.95
        uv_box(f"pvb{i}", u, hv - 22.0, H_DECK + 0.04, H_DECK + 0.50, 1.45, 8.0, navy)
    uv_box("pvwalk", -hu + 9.0, hv - 17.0, H_DECK + 0.04, H_DECK + 0.10,
           2.0 * hu - 7.0, 1.7, cream)

    # Mechanical yard at the south-east end of the deck: two round cooling towers
    for i in range(2):
        u = -hu + 3.4 + i * 5.6
        bevel(uv_cyl(f"ct{i}", u, -hv + 5.4, H_DECK + 0.04, H_DECK + 2.35, 2.05, steel),
              width=0.10, segments=1)
        uv_cyl(f"ctfan{i}", u, -hv + 5.4, H_DECK + 2.35, H_DECK + 2.55, 1.55, ink)
    for i in range(3):
        bevel(uv_box(f"plant{i}", -hu + 2.6 + i * 3.1, -hv + 11.2,
                     H_DECK + 0.04, H_DECK + 1.15, 2.4, 3.0, steel), width=0.08)

    # The mechanical penthouse box — the crest at 67.06 m
    bevel(uv_box("penthouse", hu - 3.6, -hv + 8.2, H_DECK + 0.04, H_CREST - 0.30,
                 5.6, 9.4, steel), width=0.12)
    uv_box("penthouse_cap", hu - 3.6, -hv + 8.2, H_CREST - 0.30, H_CREST, 6.2, 10.0, cream)

    # BMU (window-washing) crane on its track, held clear of the corner chamfers
    uv_box("bmu_track", hu - 2.6, 0.0, H_DECK + 0.04, H_DECK + 0.30, 0.85, v_len - 12.0,
           cream)
    uv_box("bmu_base", hu - 2.6, hv - 8.0, H_DECK + 0.30, H_DECK + 0.85, 2.4, 3.4, steel)
    uv_box("bmu_mast", hu - 2.6, hv - 8.0, H_DECK + 0.85, H_DECK + 3.10, 1.1, 1.1, steel)
    uv_box("bmu_boom", hu - 2.6, hv - 14.5, H_DECK + 2.65, H_DECK + 3.05, 0.7, 11.0, steel)
    uv_box("bmu_cw", hu - 2.6, hv - 5.4, H_DECK + 2.50, H_DECK + 3.10, 1.4, 2.2, ink)


def build_terrace(tag, insets_lo, insets_hi, z_top, mats):
    """The junction between two volumes.

    Because the volumes alternate in and out, a junction is a TERRACE on the edges
    where the volume above is set back, and a CANTILEVER on the edges where it
    oversails. Both get the same bright slab plate and dark soffit — that plate is
    what makes the stack read as stacked — but only a terrace edge gets a
    balustrade and planters, and the slab plan on each edge follows whichever of
    the two volumes is further out."""
    cream, stone = mats["Toy_cream"], mats["Toy_stone"]
    outer = [min(lo, hi) for lo, hi in zip(insets_lo, insets_hi)]
    plan = volume_plan(outer)

    ring_band(f"{tag}_soffit", plan, z_top - 0.24, z_top, -0.32, SLAB_OUT - 0.08, stone)
    ring_band(f"{tag}_slab", plan, z_top, z_top + SLAB_T, -0.42, SLAB_OUT, cream)
    # hero night band: the downlight line under every cantilever
    ring_band(f"{tag}_glow", plan, z_top - 0.40, z_top - 0.26, 0.02, SLAB_OUT - 0.10,
              mats["Toy_cream_Glow"])

    for edge, etag, lo, hi in zip(EDGES, EDGE_TAGS, insets_lo, insets_hi):
        if hi - lo < 0.6:
            continue  # a cantilever, not a terrace — nothing to stand on
        _, _, length, _, _ = poly_edge(plan, edge)
        depth = hi - lo
        # a clear glass balustrade reads as a PALE edge at city distance, not a
        # blue one — Toy_glassl here turned every terrace into a racing stripe
        wall_box(f"{tag}_{etag}_rail", plan, edge, 0.35, length - 0.35,
                 z_top + SLAB_T, z_top + SLAB_T + 0.92,
                 SLAB_OUT - 0.62, SLAB_OUT - 0.52, stone)
        for p in range(2):
            sp = (p + 0.5) * length / 2.0
            bevel(wall_box(f"{tag}_{etag}_plant{p}", plan, edge, sp - 1.4, sp + 1.4,
                           z_top + SLAB_T, z_top + SLAB_T + 0.85,
                           -depth + 0.35, -depth + 1.55,
                           mats["Toy_sage"]), width=0.07)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    mats = materials()

    build_base(mats)

    plans = []
    for tag, z0, z1, insets in VOLUMES:
        plan = volume_plan(insets)
        plans.append(plan)
        floors = int(round((z1 - z0) / FLOOR_H))
        bevel(prism(f"vol{tag}", plan, z0, z1, mats["Toy_cream"],
                    mat_caps=mats["Toy_steel"]), width=0.15)
        for edge, etag in zip(EDGES, EDGE_TAGS):
            # the crown volume reads noticeably more open than the rest in every
            # photograph — close to a pure travertine frame with sky behind it
            elevation(f"{tag}_{etag}", plan, edge, z0, z1, floors, mats,
                      DEEP_BAY[etag], LIT[(tag, etag)],
                      openness=0.45 if tag == "E" else 0.0)

    # the four junctions between the five volumes
    for i in range(4):
        build_terrace(f"terr{i}", VOLUMES[i][3], VOLUMES[i + 1][3], VOLUMES[i][2], mats)

    build_roof(plans[-1], mats)
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
    print("[build] anchor lon/lat: -122.3916888 37.7915643 (footprint AABB centre)")
    print("[build] Steuart front normal 44.2 deg true; SE 134.8; SW 224.5; Howard 314.9")
    print(f"[build] floor height {FLOOR_H:.3f} m; base {H_BASE}; deck {H_DECK}; "
          f"parapet {H_PAR}; crest {H_CREST}")
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

    blend = os.path.join(out, "one-steuart-lane.blend")
    glb = os.path.join(out, "one-steuart-lane.glb")
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
