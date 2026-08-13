"""Deterministic Blender build of the SF-SIM miniature 500 Van Ness Avenue
(The Corinthian — 1915 apartment building over a bank/retail base at the
north-east corner of Van Ness Avenue and McAllister Street, Civic Center).

    blender -b --python build_500_van_ness.py -- [--out DIR]

Writes 500-van-ness.blend and 500-van-ness.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = footprint ring bbox centre (anchor lon
-122.4199220, lat 37.7804082), min Z = 0, crest normalized to exactly 17.0 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured OSM way/355209013 ring, Douglas-Peucker simplified at 0.3 m to
  8 vertices (area within 0.15% of the survey): a rectangle rotated 8.8 deg off
  the compass grid, with one rectangular notch cut into the Van Ness side;
* that notch is the entrance light court, and it is what splits the Van Ness
  front into the two equal pavilions the building is composed of. It is carved
  ABOVE the retail base only — the shopfronts run continuously to the sidewalk;
* the facade system, and the reason this building is recognisable: eight
  projecting bay windows over floors 2-4, alternating rounded (segmental bow)
  and square, two per Van Ness pavilion and four along McAllister;
* the lid: a deep bracketed cornice, a panelled parapet set back behind it, and
  a row of urn finials on the parapet piers that set the 17.0 m crest;
* the plinth: a dark recessed shopfront band under a saturated blue sign fascia
  — the one saturated accent on an otherwise near-white building;
* two black zigzag fire escapes on the McAllister face, the most San-Franciscan
  thing about it (style bible s.8, identity is architecture);
* a designed roof for the app's downward camera: pale membrane deck, the open
  Van Ness court, a second interior light well, a stair penthouse, a mechanical
  cluster and a skylight pair;
* night state: the sign fascia is the hero, supported by the entrance soffit and
  a deterministic ~1/3 scatter of warm lit apartment windows. Glow surfaces are
  thin shells proud of the opaque glazing (the app renders _Glow in a separate
  layer that is ~12% alpha by day — never author a primary surface as glow).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/355209013 ring, projected with the app's tangent projection
# (LON0 -122.4375, LAT0 37.77) and recentred on the ring bbox centre. CCW.
# Vertices 1..4 bracket the Van Ness entrance court notch.
RING = [
    (-20.00, 15.62),   # 0  NW corner
    (-17.67, 0.87),    # 1  court, north side
    (-10.17, 2.11),    # 2  court, north-east
    (-9.17, -4.68),    # 3  court, south-east
    (-16.61, -5.87),   # 4  court, south side
    (-14.29, -20.91),  # 5  SW corner (Van Ness / McAllister)
    (20.00, -15.62),   # 6  SE corner
    (14.27, 20.91),    # 7  NE corner
]

# Edge roles, by index into RING (edge i runs RING[i] -> RING[i+1]):
E_WEST_N, E_COURT_N, E_COURT_BACK, E_COURT_S = 0, 1, 2, 3
E_WEST_S, E_SOUTH, E_EAST, E_NORTH = 4, 5, 6, 7
STREET_EDGES = (E_WEST_N, E_WEST_S, E_SOUTH)
COURT_EDGES = (E_COURT_N, E_COURT_BACK, E_COURT_S)

# The court notch as its own CCW quad, so the retail base can fill it.
COURT = [RING[4], RING[3], RING[2], RING[1]]

# Second light well, read off the Esri aerial: designed, not surveyed.
WELL_C = (3.0, 1.0)
WELL_SX, WELL_SY = 7.0, 5.6

Z_BASE = 4.70        # top of the retail base / first residential floor level
Z_BELT0, Z_BELT1 = 4.55, 4.95    # the belt course straddling that datum
Z_DECK = 15.50       # flat roof deck — 2010 LiDAR hgt_median over the footprint
Z_CORN0, Z_CORN1 = 15.50, 16.20  # the deep bracketed cornice
Z_SUB0 = 15.02                   # its lower step (the "bracket" band)
Z_PAR0, Z_PAR1 = 16.20, 16.60    # panelled parapet, set back behind the cornice
Z_PIER1 = 16.85                  # top of the parapet piers, under the urns
Z_CREST = 17.00                  # urns + raised pediment panels -> the bbox top

FLOORS = 3                       # residential floors above the retail base
FLOOR_H = (Z_DECK - Z_BASE) / FLOORS     # 3.60 m
WIN_Z0, WIN_Z1 = 1.05, 2.75      # window sill/head within each floor band

# The oriels are the whole reason this building is recognisable, so they are
# pushed to the top of the plausible range (style bible s.3: semantic scale) —
# a 0.9 m projection disappeared at the app's camera on the first review pass.
BAY_PROJ = 1.30      # how far the oriels stand off the wall
BAY_W_SQ = 3.30      # square bay chord
BAY_W_RD = 3.80      # rounded bay chord (see arc fit below)
BAY_SEG = 10         # segments across a rounded bay (style bible s.4: 8-14)
CORN_PROJ = 1.45     # cornice projects past the bays, so it caps everything
SUB_PROJ = 0.60

WIN_W, WIN_D = 1.40, 0.12
WIN_SPACING = 2.55

PALETTE_HEX = {
    "Toy_cream": "f2ede3",    # painted stucco walls
    "Toy_trim": "f3efe6",     # cornice, parapet, belt course, bay caps, finials
    "Toy_glass": "2a4d73",    # apartment windows
    "Toy_ink": "3a3530",      # shopfront glazing, fire escapes, entrance recess
    "Toy_stone": "d9d2c2",    # retail base frame and plinth
    "Toy_navy": "2c4a70",     # the retail sign fascia
    "Toy_steel": "9aa0a6",    # roof membrane
    "Toy_roofd": "45454a",    # penthouse, mechanical
    "Toy_glassl": "6f95b8",   # skylights, light-well glazing
    "Toy_gold_Glow": "caa64a",  # night: warm lit apartment windows
    "Toy_sky_Glow": "6db3d9",   # night: sign fascia + entrance soffit
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


# --------------------------------------------------------------- 2D helpers


def poly_edge(poly, i):
    """Edge i of poly: (origin, length, tangent unit, outward normal)."""
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    return a, length, t, (t[1], -t[0])


def edge_point(poly, i, u, off=0.0):
    """World point u metres along edge i, off metres outward from the wall."""
    a, _l, t, n = poly_edge(poly, i)
    return (a[0] + t[0] * u + n[0] * off, a[1] + t[1] * u + n[1] * off)


def edge_yaw(poly, i):
    _a, _l, t, _n = poly_edge(poly, i)
    return math.atan2(t[1], t[0])


def offset_polygon(poly, d):
    """Miter offset of a CCW footprint; positive d moves outward."""
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


def point_in(poly, x, y):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            if x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
                inside = not inside
    return inside


def bow_polygon(poly, i, u_mid, chord, proj, seg=BAY_SEG):
    """Segmental-bow footprint for a rounded bay, CCW in world coordinates.

    A circle whose centre sits `depth` INSIDE the wall gives a shallow bow of
    the wanted chord and projection: r = (chord^2/4 + proj^2) / (2*proj).
    """
    r = (chord * chord / 4.0 + proj * proj) / (2.0 * proj)
    depth = r - proj
    half = math.asin(min(1.0, (chord / 2.0) / r))
    pts = []
    for k in range(seg + 1):
        a = -half + 2 * half * k / seg
        du = r * math.sin(a)
        dn = r * math.cos(a) - depth
        pts.append(edge_point(poly, i, u_mid + du, dn))
    # close along the wall line, slightly inside it so the solid unions cleanly
    pts.append(edge_point(poly, i, u_mid + chord / 2.0, -0.25))
    pts.append(edge_point(poly, i, u_mid - chord / 2.0, -0.25))
    return pts


def bow_strip(poly, i, u_mid, chord, proj, off_in, off_out, seg=BAY_SEG):
    """Thin curved shell following a bow — the rounded bays' glazing."""
    r = (chord * chord / 4.0 + proj * proj) / (2.0 * proj)
    depth = r - proj
    half = math.asin(min(1.0, (chord / 2.0) / r))
    inner, outer = [], []
    for k in range(seg + 1):
        a = -half + 2 * half * k / seg
        du = r * math.sin(a)
        dn = r * math.cos(a) - depth
        inner.append(edge_point(poly, i, u_mid + du, dn + off_in))
        outer.append(edge_point(poly, i, u_mid + du, dn + off_out))
    return inner + outer[::-1]


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

    Width is capped at a third of the object's thinnest dimension: a flat bevel
    on a thin applied panel relies entirely on clamp_overlap, which collapses
    opposing profiles into zero-area slivers. The remove_doubles /
    dissolve_degenerate pass sweeps up whatever clamping still pinches shut.

    Only edges where two faces actually meet at an angle are bevelled. Handing
    bevel the whole mesh also rounds the INTERIOR edges of an n-gon — after a
    boolean the roof cap is one n-gon around a hole, and bevelling its
    triangulation fan drew bright creases straight across the deck (caught on
    the second review pass of this asset).
    """
    thin = min((d for d in obj.dimensions if d > 1e-6), default=width)
    offset = min(width, thin * 0.30)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    sharp = [
        e for e in bm.edges
        if len(e.link_faces) == 2 and e.calc_face_angle(0.0) > math.radians(18.0)
    ]
    if not sharp:
        bm.free()
        return obj
    bmesh.ops.bevel(
        bm,
        geom=sharp + [v for v in bm.verts if any(e in sharp for e in v.link_edges)],
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


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0):
    """Box with local +x along yaw and local +y 90 deg ccw of it."""
    c, s = math.cos(yaw), math.sin(yaw)
    corners = []
    for lx, ly in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)):
        corners.append((cx + lx * c - ly * s, cy + lx * s + ly * c))
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4),
             (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, [mat])


def cylinder(name, cx, cy, z0, z1, r, mat, seg=8, r_top=None):
    rt = r if r_top is None else r_top
    lo = [(cx + r * math.cos(2 * math.pi * k / seg), cy + r * math.sin(2 * math.pi * k / seg))
          for k in range(seg)]
    hi = [(cx + rt * math.cos(2 * math.pi * k / seg), cy + rt * math.sin(2 * math.pi * k / seg))
          for k in range(seg)]
    verts = [(x, y, z0) for x, y in lo] + [(x, y, z1) for x, y in hi]
    faces = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]
    faces.append(tuple(range(seg - 1, -1, -1)))
    faces.append(tuple(range(seg, 2 * seg)))
    return new_mesh(name, verts, faces, [mat])


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


# ------------------------------------------------------------- the bay plan

# (edge, u along that edge, kind). Rounded bays sit at the corners of each
# pavilion, square ones inboard — the rhythm read off the Street View captures.
BAYS = [
    (E_WEST_N, 3.70, "round"),
    (E_WEST_N, 11.20, "square"),
    (E_WEST_S, 4.00, "square"),
    (E_WEST_S, 11.50, "round"),
    (E_SOUTH, 5.00, "round"),
    (E_SOUTH, 13.40, "square"),
    (E_SOUTH, 21.80, "round"),
    (E_SOUTH, 30.20, "square"),
]


def bay_span(kind):
    return BAY_W_RD if kind == "round" else BAY_W_SQ


def floor_levels():
    return [Z_BASE + f * FLOOR_H for f in range(FLOORS)]


# --------------------------------------------------------------------- build


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    cream = material("Toy_cream")
    trim = material("Toy_trim")
    glass = material("Toy_glass")
    ink = material("Toy_ink")
    stone = material("Toy_stone")
    navy = material("Toy_navy")
    steel = material("Toy_steel")
    roofd = material("Toy_roofd")
    glassl = material("Toy_glassl")
    gold_glow = material("Toy_gold_Glow")
    sky_glow = material("Toy_sky_Glow")

    # --- the body, with the second light well cut out of it -----------------
    body = prism("body", RING, 0.0, Z_DECK, cream, mat_caps=steel)
    well = [
        (WELL_C[0] - WELL_SX / 2, WELL_C[1] - WELL_SY / 2),
        (WELL_C[0] + WELL_SX / 2, WELL_C[1] - WELL_SY / 2),
        (WELL_C[0] + WELL_SX / 2, WELL_C[1] + WELL_SY / 2),
        (WELL_C[0] - WELL_SX / 2, WELL_C[1] + WELL_SY / 2),
    ]
    cutter = prism("well_cutter", well, Z_BASE + 0.20, Z_DECK + 2.0, cream)
    mod = body.modifiers.new("well", "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.solver = "EXACT"
    mod.object = cutter
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.modifier_apply(modifier="well")
    bpy.data.objects.remove(cutter, do_unlink=True)
    bm = bmesh.new()
    bm.from_mesh(body.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(body.data)
    bm.free()
    prism("well_floor", offset_polygon(well, -0.03), Z_BASE - 0.4, Z_BASE + 0.2,
          cream, mat_caps=steel)

    # --- the retail base fills the court notch: shopfronts run to the kerb --
    prism("base_infill", COURT, 0.0, Z_BASE, stone, mat_caps=stone)

    # --- the plinth / shopfront band / sign fascia --------------------------
    # The dark band is drawn just PROUD of the wall, between a plinth and a head
    # that stand further out — the same trick the 505 Van Ness piers use. An
    # actually-recessed band cannot be seen at all: the body is a solid prism, so
    # a ring_band at a negative offset sits inside it (caught on the first
    # elevation render, where the whole retail base came out blank cream).
    ring_band("plinth", RING, 0.0, 0.70, 0.0, 0.16, stone)
    ring_band("shopfront", RING, 0.70, 3.55, 0.0, 0.05, ink)
    ring_band("shop_head", RING, 3.55, 3.72, 0.0, 0.20, stone)
    ring_band("fascia", RING, 3.72, 4.52, 0.0, 0.24, navy)
    ring_band("fascia_glow", RING, 3.86, 4.38, 0.24, 0.32, sky_glow)
    # the same band across the court infill, so the base reads continuous
    ring_band("plinth_court", COURT, 0.0, 0.70, 0.0, 0.16, stone)
    ring_band("shopfront_court", COURT, 0.70, 3.55, 0.0, 0.05, ink)
    ring_band("shop_head_court", COURT, 3.55, 3.72, 0.0, 0.20, stone)
    ring_band("fascia_court", COURT, 3.72, 4.52, 0.0, 0.24, navy)

    # Shopfront piers on the two street faces only — they break the 50 m of dark
    # glazing into bays and read the base as a colonnade from the aerial. The
    # party walls keep a plain base, which is also how they distinguish
    # themselves from the show faces.
    npier = 0
    for edge in STREET_EDGES:
        _a, length, _t, _n = poly_edge(RING, edge)
        count = max(2, int(round(length / 5.6)))
        for k in range(count + 1):
            u = length * k / count
            bx, by = edge_point(RING, edge, u, 0.14)
            box(f"shoppier{npier}", bx, by, 0.0, 3.72, 0.62, 0.60, stone,
                yaw=edge_yaw(RING, edge))
            npier += 1
    print(f"[build] shopfront piers: {npier}")

    # --- the belt course at the top of the base -----------------------------
    ring_band("belt", RING, Z_BELT0, Z_BELT1, 0.0, 0.28, trim)
    ring_band("belt_court", COURT, Z_BELT0, Z_BELT1, 0.0, 0.28, trim)

    # --- the eight bay windows ----------------------------------------------
    levels = floor_levels()
    for bi, (edge, u, kind) in enumerate(BAYS):
        yaw = edge_yaw(RING, edge)
        if kind == "round":
            poly = bow_polygon(RING, edge, u, BAY_W_RD, BAY_PROJ)
            prism(f"bay{bi}", poly, Z_BELT1, Z_DECK, cream)
            for fi, z in enumerate(levels):
                strip = bow_strip(RING, edge, u, BAY_W_RD * 0.90, BAY_PROJ,
                                  -0.06, 0.06)
                prism(f"bayglass{bi}_{fi}", strip, z + WIN_Z0 - 0.10,
                      z + WIN_Z1 + 0.10, glass)
        else:
            cx, cy = edge_point(RING, edge, u, BAY_PROJ / 2.0 - 0.20)
            prism(
                f"bay{bi}",
                [
                    edge_point(RING, edge, u - BAY_W_SQ / 2, -0.25),
                    edge_point(RING, edge, u + BAY_W_SQ / 2, -0.25),
                    edge_point(RING, edge, u + BAY_W_SQ / 2, BAY_PROJ),
                    edge_point(RING, edge, u - BAY_W_SQ / 2, BAY_PROJ),
                ],
                Z_BELT1,
                Z_DECK,
                cream,
            )
            for fi, z in enumerate(levels):
                fx, fy = edge_point(RING, edge, u, BAY_PROJ + 0.02)
                box(f"bayglass{bi}_{fi}", fx, fy, z + WIN_Z0 - 0.10,
                    z + WIN_Z1 + 0.10, BAY_W_SQ * 0.86, 0.10, glass, yaw=yaw)
                for side in (-1, 1):
                    sx, sy = edge_point(RING, edge,
                                        u + side * (BAY_W_SQ / 2 - 0.02),
                                        BAY_PROJ / 2.0)
                    box(f"bayside{bi}_{fi}_{side}", sx, sy, z + WIN_Z0 - 0.10,
                        z + WIN_Z1 + 0.10, 0.10, BAY_PROJ * 0.74, glass, yaw=yaw)
        # the bay's own little cap, tucked under the main cornice
        if kind == "round":
            cap = bow_strip(RING, edge, u, BAY_W_RD, BAY_PROJ, -0.30, 0.16)
            prism(f"baycap{bi}", cap, Z_DECK - 0.30, Z_DECK, trim)
        else:
            cxc, cyc = edge_point(RING, edge, u, BAY_PROJ / 2.0 - 0.10)
            box(f"baycap{bi}", cxc, cyc, Z_DECK - 0.30, Z_DECK,
                BAY_W_SQ + 0.32, BAY_PROJ + 0.42, trim, yaw=yaw)

    # --- punched windows on the wall between the bays -----------------------
    def bay_blocks(edge):
        return [(u - bay_span(k) / 2 - 0.9, u + bay_span(k) / 2 + 0.9)
                for e, u, k in BAYS if e == edge]

    win_slots = []
    for edge in STREET_EDGES + COURT_EDGES:
        _a, length, _t, _n = poly_edge(RING, edge)
        blocks = bay_blocks(edge)
        count = max(1, int(round(length / WIN_SPACING)))
        for k in range(count):
            u = length * (k + 0.5) / count
            if any(lo < u < hi for lo, hi in blocks):
                continue
            if u < 1.5 or u > length - 1.5:
                continue
            win_slots.append((edge, u))

    for wi, (edge, u) in enumerate(win_slots):
        yaw = edge_yaw(RING, edge)
        for fi, z in enumerate(levels):
            wx, wy = edge_point(RING, edge, u, WIN_D / 2 - 0.03)
            box(f"win{wi}_{fi}", wx, wy, z + WIN_Z0, z + WIN_Z1,
                WIN_W, WIN_D, glass, yaw=yaw)

    # --- the residential entrance, at the back of the court -----------------
    _a, court_len, _t, _n = poly_edge(RING, E_COURT_BACK)
    ex, ey = edge_point(RING, E_COURT_BACK, court_len / 2, 0.10)
    eyaw = edge_yaw(RING, E_COURT_BACK)
    box("entry_recess", ex, ey, 0.0, 3.30, 3.60, 0.22, ink, yaw=eyaw)
    box("entry_surround", ex, ey, 0.0, 3.70, 4.30, 0.34, trim, yaw=eyaw)
    box("entry_soffit_glow", ex, ey, 3.32, 3.58, 3.30, 0.30, sky_glow, yaw=eyaw)

    # --- two zigzag fire escapes on McAllister ------------------------------
    _a, south_len, _t, _n = poly_edge(RING, E_SOUTH)
    syaw = edge_yaw(RING, E_SOUTH)
    for ei, u in enumerate((9.30, 26.00)):
        for fi, z in enumerate(levels):
            lx, ly = edge_point(RING, E_SOUTH, u, 0.55)
            box(f"fe{ei}_land{fi}", lx, ly, z + 0.60, z + 0.72, 2.60, 1.10,
                ink, yaw=syaw)
            box(f"fe{ei}_rail{fi}", *edge_point(RING, E_SOUTH, u, 1.05),
                z + 0.72, z + 1.62, 2.60, 0.08, ink, yaw=syaw)
            if fi:
                # the diagonal run down to the landing below
                mx_, my_ = edge_point(RING, E_SOUTH, u + 1.55, 0.55)
                box(f"fe{ei}_run{fi}", mx_, my_, z - FLOOR_H + 0.66, z + 0.66,
                    0.55, 0.95, ink, yaw=syaw)

    # --- the lid: bracket band, cornice, parapet, finials -------------------
    ring_band("cornice_sub", RING, Z_SUB0, Z_CORN0, 0.0, SUB_PROJ, trim)
    ring_band("cornice", RING, Z_CORN0, Z_CORN1, 0.0, CORN_PROJ, trim)
    ring_band("parapet", RING, Z_PAR0, Z_PAR1, 0.10, 0.42, trim)
    ring_band("parapet_court", COURT, Z_PAR0, Z_PAR1, 0.10, 0.42, trim)

    # Piers with urns, and a raised pediment panel centred on each show face.
    # The first review pass had 19 thin finials, which read as noise from the
    # app's camera: fewer and chunkier is the style bible's s.9 answer.
    finials = 0
    for edge in STREET_EDGES:
        _a, length, _t, _n = poly_edge(RING, edge)
        count = max(2, int(round(length / 7.0)))
        for k in range(count + 1):
            u = length * k / count
            fx, fy = edge_point(RING, edge, u, 0.26)
            box(f"pier{finials}", fx, fy, Z_PAR1, Z_PIER1, 1.10, 0.66, trim,
                yaw=edge_yaw(RING, edge))
            cylinder(f"urn{finials}", fx, fy, Z_PIER1 - 0.02, Z_CREST, 0.34,
                     trim, seg=8, r_top=0.18)
            finials += 1
        # the raised parapet panel between the outer piers of this face
        pcx, pcy = edge_point(RING, edge, length / 2, 0.26)
        box(f"pediment{edge}", pcx, pcy, Z_PAR1 - 0.05, Z_CREST,
            min(length * 0.42, 9.0), 0.52, trim, yaw=edge_yaw(RING, edge))
    print(f"[build] parapet piers/urns: {finials}")

    # --- the roof, because the camera looks down (style bible s.10) ---------
    def on_roof(x, y, margin=2.2):
        if not point_in(offset_polygon(RING, -margin), x, y):
            return False
        if point_in(offset_polygon(COURT, margin), x, y):
            return False
        wellm = [(WELL_C[0] - WELL_SX / 2 - margin, WELL_C[1] - WELL_SY / 2 - margin),
                 (WELL_C[0] + WELL_SX / 2 + margin, WELL_C[1] - WELL_SY / 2 - margin),
                 (WELL_C[0] + WELL_SX / 2 + margin, WELL_C[1] + WELL_SY / 2 + margin),
                 (WELL_C[0] - WELL_SX / 2 - margin, WELL_C[1] + WELL_SY / 2 + margin)]
        return not point_in(wellm, x, y)

    candidates = []
    gx = -18.0
    while gx < 19.0:
        gy = -19.0
        while gy < 20.0:
            if on_roof(gx, gy, margin=3.4):
                candidates.append((round(gx, 2), round(gy, 2)))
            gy += 4.0
        gx += 4.0
    print(f"[build] roof candidates on deck: {len(candidates)}")

    def nearest(tx, ty, taken):
        pool = [p for p in candidates if p not in taken]
        return min(pool, key=lambda p: (p[0] - tx) ** 2 + (p[1] - ty) ** 2)

    # One mechanical cluster and one skylight pair — clusters, not a scatter
    # (style bible s.10). The first review pass sprayed twelve lone vent pipes
    # across the deck and they read as pimples.
    taken = set()
    px_, py_ = nearest(-7.0, -11.0, taken)
    taken.add((px_, py_))
    # Kept below Z_CREST on purpose: the parapet is the crest, and a penthouse
    # poking through it would both contradict the photographs and hand the
    # loader's height normalization to a service box.
    box("penthouse", px_, py_, Z_DECK, Z_DECK + 0.98, 5.4, 4.0, roofd)
    box("penthouse_cap", px_, py_, Z_DECK + 0.98, Z_DECK + 1.16, 5.9, 4.5, trim)
    for vi, (ox, oy) in enumerate(((3.5, 0.9), (3.5, -0.9), (4.7, 0.0))):
        cylinder(f"vent{vi}", px_ + ox, py_ + oy, Z_DECK, Z_DECK + 0.85, 0.30,
                 steel, seg=8)

    px_, py_ = nearest(9.0, 13.0, taken)
    taken.add((px_, py_))
    box("plantroom", px_, py_, Z_DECK, Z_DECK + 1.05, 4.6, 3.2, roofd)
    box("plantroom_cap", px_, py_, Z_DECK + 1.05, Z_DECK + 1.22, 5.0, 3.6, trim)

    px_, py_ = nearest(-8.0, 12.0, taken)
    taken.add((px_, py_))
    for si, oy in enumerate((-1.9, 1.9)):
        box(f"skylight_kerb{si}", px_, py_ + oy, Z_DECK, Z_DECK + 0.26,
            3.6, 2.4, trim)
        box(f"skylight{si}", px_, py_ + oy, Z_DECK + 0.20, Z_DECK + 0.56,
            3.1, 1.9, glassl)

    px_, py_ = nearest(12.0, -12.0, taken)
    taken.add((px_, py_))
    box("hatch", px_, py_, Z_DECK, Z_DECK + 0.70, 2.2, 1.7, roofd)

    # --- night: a restrained scatter of warm lit apartment windows ----------
    # Thin shells proud of the opaque glazing, never a primary surface.
    lit = 0
    for wi, (edge, u) in enumerate(win_slots):
        yaw = edge_yaw(RING, edge)
        for fi, z in enumerate(levels):
            if (wi * 3 + fi * 2) % 7 not in (0, 3):
                continue
            gx_, gy_ = edge_point(RING, edge, u, WIN_D / 2 + 0.04)
            box(f"lit{wi}_{fi}", gx_, gy_, z + WIN_Z0 + 0.32, z + WIN_Z1 - 0.32,
                WIN_W - 0.55, 0.06, gold_glow, yaw=yaw)
            lit += 1
    for bi, (edge, u, kind) in enumerate(BAYS):
        yaw = edge_yaw(RING, edge)
        for fi, z in enumerate(levels):
            if (bi + fi) % 3:
                continue
            gx_, gy_ = edge_point(RING, edge, u, BAY_PROJ + 0.10)
            box(f"baylit{bi}_{fi}", gx_, gy_, z + WIN_Z0 + 0.30, z + WIN_Z1 - 0.30,
                bay_span(kind) * 0.48, 0.06, gold_glow, yaw=yaw)
            lit += 1
    print(f"[build] lit window shells: {lit}")

    # Bevel budget: the chunky masses carry the miniature read and take the full
    # 0.12/2. The thin applied shells (glazing, glow, bands) get none — that is
    # what keeps this comfortably under the 14,000-triangle cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if name.startswith(("win", "lit", "baylit", "bayglass", "bayside",
                            "shopfront", "fascia", "entry_soffit", "skylight",
                            "shoppier",
                            "urn")):
            continue
        if name.startswith(("plinth", "belt", "shop_head", "parapet", "pier",
                            "pediment", "cornice", "baycap", "fe")):
            bevel(obj, width=0.10, segments=1)
            continue
        bevel(obj, width=0.12, segments=2)

    return scene


def normalize():
    """Sit the model on z=0, centre it in x/y on the FOOTPRINT RING, and put the
    crest at exactly Z_CREST so the loader's targetHeightM / measuredHeight
    scale lands on 1.000. Edits vertex data, so object transforms stay identity."""
    dg = bpy.context.evaluated_depsgraph_get()
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    for o in meshes:
        me = o.evaluated_get(dg).to_mesh()
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    rx = [p[0] for p in RING]
    ry = [p[1] for p in RING]
    dx = (min(rx) + max(rx)) / 2.0
    dy = (min(ry) + max(ry)) / 2.0
    sz = Z_CREST / (mx.z - mn.z)
    for o in meshes:
        for v in o.data.vertices:
            v.co.x -= dx
            v.co.y -= dy
            v.co.z = (v.co.z - mn.z) * sz
    print(f"[build] normalize: dx={dx:.4f} dy={dy:.4f} z-scale={sz:.6f}")


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
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 4) for i in range(2)]}")
    print("[build] anchor lon/lat: -122.4199220 37.7804082 (ring bbox centre)")
    _a, _l, _t, n = poly_edge(RING, E_COURT_BACK)
    print(f"[build] entrance heading: {math.degrees(math.atan2(n[0], n[1])) % 360:.1f} deg true")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    normalize()
    report()

    blend = os.path.join(out, "500-van-ness.blend")
    glb = os.path.join(out, "500-van-ness.glb")
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
