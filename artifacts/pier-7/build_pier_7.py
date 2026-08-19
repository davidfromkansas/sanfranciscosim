"""Deterministic Blender build of the SF-SIM miniature Pier 7 (Broadway public
access pier).

    blender -b --python build_pier_7.py -- [--out DIR]

Writes pier-7.blend and pier-7.glb next to this file (or into --out). Geometry
is authored directly in world space in metres, Z up, +X east, +Y north, so the
model drops into the city at its real-world heading — the loader applies no
rotation.

Origin = the OSM pier polygon's OBB centre (anchor lon -122.3955159,
lat 37.7994429), over open water. `placeGeneric` seats generic landmarks at
max(0, sampleElevation(x, z)) and the app's terrain samples 0.00 across the
whole footprint, so **Z = 0 here is the waterline**. Everything is quoted above
that datum: pile heads 2.4 m, deck top 3.0 m, railing 4.07 m, and the lamp
globes topping out at exactly 7.6 m — the bounding-box top and the manifest's
targetHeightM.

Design (see REFERENCE.md and docs/asset-plans/pier-7.md for sources):

* the measured OSM footprint (way 23605169, `man_made=pier`) — 257.3 x 26.9 m,
  long axis bearing 54.65 deg, five parts: entry plaza (20.7 x 12.3 m, rounded
  seaward corners) / 7.5 m walkway / 16.8 m mid-pier fishing bay / 7.4 m
  walkway / the 26.9 m-wide end platform. There is NO building on this pier;
  the 1990 ROMA Design Group deck furniture IS the design;
* a pile field and a deck soffit, because the thing stands in 35 ft of water
  and the app's camera reaches water level;
* the identity feature: TWO dead-straight rows of single-globe Embarcadero
  lamp standards, 44 of them, on a strict beat the full length. The globes are
  enlarged to 0.5 m so they read as dots from the aerial camera;
* the 42-inch ornamental iron railing simplified to posts + two rails, near-
  black, on every edge except the open shore end where the pier meets the
  Embarcadero promenade;
* the timber deck as a warm plank field with a darker centre lane, a granite
  entry-plaza band with Steve Gillman's two granite "Bay Bench" blocks and the
  bronze water-viewing grill, iron-and-wood benches against the rails, and two
  steel fish-cleaning stations on the end platform;
* night state: the 44 lamp globes and NOTHING else. The real pier at night is
  two dotted lines of warm light over black water; restraint is the design.
  The globes are solid Toy_amber_Glow spheres standing proud on their posts —
  the luminaire is the object, never a shell over another surface.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way 23605169 projected with the app's tangent projection, recentred on the
# footprint OBB centre, and expressed in the pier frame: s along the axis
# (bearing 54.65 deg, negative = the Embarcadero shore end, positive = the Bay
# end), t across it (positive toward the SE). CCW.
FOOTPRINT_ST = [
    (-128.32, 2.52),
    (-128.64, -9.39),
    (-123.62, -9.46),
    (-123.47, -4.96),
    (-118.81, -4.90),
    (-118.15, -4.69),
    (-117.47, -4.34),
    (-116.94, -3.82),
    (-116.60, -3.21),
    (-116.28, -0.84),
    (-21.93, -2.04),
    (-19.93, -3.22),
    (-19.91, -4.23),
    (-15.73, -6.60),
    (-4.51, -6.86),
    (-0.24, -4.43),
    (-0.19, -3.48),
    (1.91, -2.29),
    (113.00, -3.59),
    (112.89, -5.78),
    (117.24, -8.60),
    (117.09, -13.45),
    (124.01, -13.45),
    (128.48, -6.08),
    (128.64, 5.64),
    (124.38, 13.45),
    (117.63, 13.39),
    (117.44, 8.55),
    (113.06, 6.03),
    (112.97, 3.79),
    (2.01, 5.12),
    (0.00, 6.35),
    (0.01, 7.22),
    (-4.36, 9.83),
    (-15.38, 9.96),
    (-19.66, 7.57),
    (-19.68, 6.65),
    (-21.96, 5.46),
    (-116.20, 6.71),
    (-116.17, 7.95),
    (-116.30, 8.59),
    (-116.56, 9.20),
    (-116.92, 9.76),
    (-117.40, 10.24),
    (-117.95, 10.61),
    (-118.59, 10.87),
    (-122.69, 11.06),
    (-126.12, 11.18),
    (-128.10, 11.23),
]

AXIS_DEG = 54.65
AX = (math.sin(math.radians(AXIS_DEG)), math.cos(math.radians(AXIS_DEG)))
LT = (math.cos(math.radians(AXIS_DEG)), -math.sin(math.radians(AXIS_DEG)))

Z_PILE_TOP = 2.40   # deck soffit
Z_DECK = 3.00       # deck slab top (= the Embarcadero promenade, met flush)
Z_SURF = 3.08       # timber walking surface over the slab
Z_BULL = 3.35       # bullrail top
Z_RAIL_MID0, Z_RAIL_MID1 = 3.60, 3.68
Z_RAIL_TOP0, Z_RAIL_TOP1 = 3.99, 4.07   # 42 in = 1.07 m above the deck surface
Z_POST_TOP = 4.12
Z_LAMP_POST = 6.80
Z_GLOBE_C = 7.35
R_GLOBE = 0.25      # globe top = 7.60 = the bbox top = targetHeightM

RAIL_INSET = 0.50   # railing line, in from the deck edge
PILE_STEP = 5.6
POST_STEP = 3.8
LAMP_EDGE_IN = 0.85

# Piecewise-linear edge tables (s, t) for furniture placement: the deck edges
# drift a metre or two over 257 m and everything must follow the real edge.
EDGE_SE = [
    (-128.64, -9.39), (-123.62, -9.46), (-123.47, -4.96), (-116.60, -3.21),
    (-116.28, -0.84), (-21.93, -2.04), (-19.91, -4.23), (-15.73, -6.60),
    (-4.51, -6.86), (-0.19, -3.48), (1.91, -2.29), (113.00, -3.59),
    (112.89, -5.78), (117.24, -8.60), (117.09, -13.45), (124.01, -13.45),
    (128.48, -6.08),
]
EDGE_NW = [
    (-128.10, 11.23), (-118.59, 10.87), (-116.20, 6.71), (-21.96, 5.46),
    (-19.66, 7.57), (-15.38, 9.96), (-4.36, 9.83), (0.01, 7.22),
    (2.01, 5.12), (112.97, 3.79), (113.06, 6.03), (117.44, 8.55),
    (117.63, 13.39), (124.38, 13.45), (128.64, 5.64),
]

PALETTE_HEX = {
    # Warm plank timber; the palette has no wood, rust a86444 is too red and
    # would read as brick from altitude. Off-palette is a WARN, not a FAIL
    # (contract rule 7) — stated in REPORT.md.
    "Toy_timber": "8a6a4a",
    "Toy_timberd": "7a5c3e",   # the darker centre lane of the plank field
    "Toy_ink": "3a3530",       # ironwork + fascia; do not go darker, the app's
                               # light crushes near-black to black
    "Toy_stone": "d9d2c2",     # granite plaza band + Bay Bench blocks
    "Toy_steel": "9aa0a6",     # fish-cleaning stations
    "Toy_gold": "caa64a",      # the bronze grill
    # The base colour IS the night look (the app draws _Glow unlit at the
    # material's own colour): warm pale lamplight, never saturated yellow.
    "Toy_amber_Glow": "f6e3c0",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def pw(s, t):
    """Pier frame (along-axis, across-axis) -> world (x, y)."""
    return (AX[0] * s + LT[0] * t, AX[1] * s + LT[1] * t)


def edge_t(s, table):
    """Across-pier position of a deck edge at station s (piecewise linear)."""
    if s <= table[0][0]:
        return table[0][1]
    for (s0, t0), (s1, t1) in zip(table, table[1:]):
        if s <= s1:
            f = (s - s0) / (s1 - s0) if s1 > s0 else 0.0
            return t0 + (t1 - t0) * f
    return table[-1][1]


def offset_polygon(poly, d):
    """Miter offset of a CCW polygon; positive d moves outward."""
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


def offset_polyline(pts, d):
    """Miter offset of an OPEN polyline; positive d moves left of travel."""
    npts = len(pts)
    normals = []
    for i in range(npts - 1):
        a, b = pts[i], pts[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        normals.append((-dy / length, dx / length))
    out = []
    for i in range(npts):
        if i == 0:
            n = normals[0]
        elif i == npts - 1:
            n = normals[-1]
        else:
            n1, n2 = normals[i - 1], normals[i]
            nx, ny = n1[0] + n2[0], n1[1] + n2[1]
            ln = math.hypot(nx, ny) or 1.0
            n = (nx / ln, ny / ln)
            dot = max(0.35, n[0] * normals[i][0] + n[1] * normals[i][1])
            n = (n[0] / dot, n[1] / dot)
        out.append((pts[i][0] + n[0] * d, pts[i][1] + n[1] * d))
    return out


def point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


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


def triangulate(obj):
    """Ear-clip concave ngon caps at build time so export tessellation can
    never produce a bad triangle over the pier's necked footprint."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def bevel(obj, width=0.10, segments=2):
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
    """Closed extrusion of a CCW (s, t) polygon (walls + both caps)."""
    npts = len(poly)
    world = [pw(s, t) for s, t in poly]
    verts = [(x, y, z0) for x, y in world] + [(x, y, z1) for x, y in world]
    faces, face_mats = [], []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
        face_mats.append(0)
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    face_mats += [1 if mat_caps else 0] * 2
    mats = [mat, mat_caps] if mat_caps else [mat]
    return triangulate(new_mesh(name, verts, faces, mats, face_mats))


def sbox(name, s0, s1, t0, t1, z0, z1, mat):
    """Axis-aligned box in the PIER frame."""
    corners = [pw(s0, t0), pw(s1, t0), pw(s1, t1), pw(s0, t1)]
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, [mat])


def ngon_post(name, s, t, z0, z1, r, mat, seg=6):
    ring = [(s + r * math.cos(2 * math.pi * k / seg), t + r * math.sin(2 * math.pi * k / seg))
            for k in range(seg)]
    return prism(name, ring, z0, z1, mat)


def ring_band(name, poly, z0, z1, off_in, off_out, mat):
    """Closed band following a CCW (s, t) polygon: 4 loops, quads between."""
    lo_in = offset_polygon(poly, off_in)
    lo_out = offset_polygon(poly, off_out)
    npts = len(lo_in)
    verts = []
    for loop, z in ((lo_in, z0), (lo_out, z0), (lo_out, z1), (lo_in, z1)):
        verts.extend([(*pw(s, t), z) for s, t in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * npts, ((k + 1) % 4) * npts
        for i in range(npts):
            j = (i + 1) % npts
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def strip_band(name, pts, z0, z1, half_w, mat):
    """Closed rectangular tube along an OPEN (s, t) polyline (a rail)."""
    left = offset_polyline(pts, half_w)
    right = offset_polyline(pts, -half_w)
    npts = len(pts)
    verts = []
    for loop, z in ((right, z0), (left, z0), (left, z1), (right, z1)):
        verts.extend([(*pw(s, t), z) for s, t in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * npts, ((k + 1) % 4) * npts
        for i in range(npts - 1):
            faces.append((a0 + i, a0 + i + 1, b0 + i + 1, b0 + i))
    # end caps
    faces.append((0, npts, 2 * npts, 3 * npts))
    faces.append((4 * npts - 1, 3 * npts - 1, 2 * npts - 1, npts - 1))
    return new_mesh(name, verts, faces, [mat])


def globe(name, s, t, zc, r, mat, useg=8, vseg=5):
    from mathutils import Matrix

    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=useg, v_segments=vseg, radius=r)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    x, y = pw(s, t)
    # Bake the placement into the vertices: every object in the export must
    # carry an identity transform (contract: applied transforms).
    mesh.transform(Matrix.Translation((x, y, zc)))
    mesh.materials.append(mat)
    mesh.shade_flat()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


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


# --------------------------------------------------------------------- build


def lamp(n, s, t, ink, glow):
    """One Embarcadero-style single-globe standard. Top = exactly 7.60 m."""
    sbox(f"lampbase{n}", s - 0.16, s + 0.16, t - 0.16, t + 0.16, Z_SURF, Z_SURF + 0.32, ink)
    ngon_post(f"lamppost{n}", s, t, Z_SURF + 0.32, Z_LAMP_POST, 0.085, ink, seg=6)
    ngon_post(f"lampcollar{n}", s, t, Z_LAMP_POST, Z_LAMP_POST + 0.18, 0.14, ink, seg=6)
    globe(f"lampglobe{n}", s, t, Z_GLOBE_C, R_GLOBE, glow)


def bench(n, s, t_edge, inward, timber, ink):
    """Iron-and-wood bench, back against the railing, facing the deck centre.
    `inward` is +1 when the deck centre is at greater t, else -1."""
    tb = t_edge + inward * (RAIL_INSET + 0.30)          # back plane
    tf = tb + inward * 0.55                             # seat front
    t0, t1 = min(tb, tf), max(tb, tf)
    sbox(f"benchseat{n}", s - 0.9, s + 0.9, t0, t1, Z_SURF + 0.38, Z_SURF + 0.46, timber)
    bt0, bt1 = (tb, tb + inward * 0.10) if inward > 0 else (tb + inward * 0.10, tb)
    sbox(f"benchback{n}", s - 0.9, s + 0.9, bt0, bt1, Z_SURF + 0.46, Z_SURF + 0.95, timber)
    for ds in (-0.78, 0.78):
        sbox(f"benchleg{n}_{ds > 0}", s + ds - 0.05, s + ds + 0.05, t0 + 0.02, t1 - 0.02,
             Z_SURF, Z_SURF + 0.38, ink)


def build():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for item in list(block):
            block.remove(item)
    scene = bpy.context.scene

    timber = material("Toy_timber")
    timberd = material("Toy_timberd")
    ink = material("Toy_ink")
    stone = material("Toy_stone")
    steel = material("Toy_steel")
    gold = material("Toy_gold")
    glow = material("Toy_amber_Glow")

    # ---------------------------------------------------------- substructure
    # Pile bents along both deck edges, doubled rows under the mid bay and the
    # end platform. Hard-capped so a footprint edit cannot blow the budget.
    inner = offset_polygon(FOOTPRINT_ST, -0.15)
    piles = 0
    s = -126.0
    while s <= 126.0 and piles < 150:
        for table, sign in ((EDGE_SE, 1.0), (EDGE_NW, -1.0)):
            te = edge_t(s, table) + sign * 0.55
            if point_in_poly(s, te, inner):
                sbox(f"pile{piles}", s - 0.22, s + 0.22, te - 0.22, te + 0.22,
                     0.0, Z_PILE_TOP, ink)
                piles += 1
            # second row where the deck is wide
            if -21.0 <= s <= 1.0 or s >= 114.0 or s <= -117.0:
                ti = te + sign * 5.0
                if point_in_poly(s, ti, inner):
                    sbox(f"pile{piles}", s - 0.22, s + 0.22, ti - 0.22, ti + 0.22,
                         0.0, Z_PILE_TOP, ink)
                    piles += 1
        s += PILE_STEP

    # Deck slab (ink fascia walls + soffit) and the timber walking surface,
    # whose own 8 cm edge reads as the plank layer over the dark slab.
    prism("deck_slab", FOOTPRINT_ST, Z_PILE_TOP, Z_DECK, ink)
    prism("deck_surface", FOOTPRINT_ST, Z_DECK, Z_SURF, timber)

    # Bullrail: chunky timber curb ring at the deck edge.
    ring_band("bullrail", FOOTPRINT_ST, Z_SURF, Z_BULL, -0.28, 0.0, timber)

    # The darker plank lane down the middle of both walkways ties the deck
    # into one long gesture (and is the only "graphic" on the asset).
    sbox("lane_shore", -116.4, -22.0, 0.9, 4.9, Z_SURF, Z_SURF + 0.015, timberd)
    sbox("lane_bay", 2.0, 113.0, -1.3, 2.7, Z_SURF, Z_SURF + 0.015, timberd)

    # Granite entry-plaza band, the two Gillman "Bay Bench" blocks, and the
    # bronze grill between them.
    sbox("plaza", -128.45, -117.6, -9.2, 11.0, Z_SURF, Z_SURF + 0.02, stone)
    for i, tb in enumerate((-4.6, 6.4)):
        b = sbox(f"baybench{i}", -123.8, -121.2, tb - 1.3, tb + 1.3,
                 Z_SURF + 0.02, Z_SURF + 0.45, stone)
        bevel(b, width=0.10, segments=2)
    sbox("grill", -123.1, -121.9, 0.3, 1.7, Z_SURF + 0.02, Z_SURF + 0.055, gold)

    # ------------------------------------------------------------- railing
    # Open boundary polyline: the whole perimeter except the shore edge, where
    # the pier meets the promenade. Posts + two rails, near-black.
    boundary = FOOTPRINT_ST[1:]
    rail_line = offset_polyline(boundary, RAIL_INSET)  # CCW: left of travel = inward
    strip_band("rail_top", rail_line, Z_RAIL_TOP0, Z_RAIL_TOP1, 0.045, ink)
    strip_band("rail_mid", rail_line, Z_RAIL_MID0, Z_RAIL_MID1, 0.035, ink)
    posts = 0
    acc = 0.0
    for a, b in zip(rail_line, rail_line[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        while acc <= seg:
            f = acc / seg
            ps, pt = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
            sbox(f"railpost{posts}", ps - 0.045, ps + 0.045, pt - 0.045, pt + 0.045,
                 Z_SURF, Z_POST_TOP, ink)
            posts += 1
            acc += POST_STEP
        acc -= seg

    # --------------------------------------------------------------- lamps
    lamps = []
    stations = [(-110.0 + 11.4 * k) for k in range(8)]          # shore walkway
    stations += [-16.0, -4.0]                                    # mid bay
    stations += [(10.0 + 12.5 * k) for k in range(9)]            # bay walkway
    for s in stations:
        lamps.append((s, edge_t(s, EDGE_SE) + LAMP_EDGE_IN))
        lamps.append((s, edge_t(s, EDGE_NW) - LAMP_EDGE_IN))
    for tl in (-10.5, -3.5, 3.5, 10.5):                          # end platform
        lamps.append((122.0, tl))
    lamps.append((-126.3, -7.6))                                 # plaza pair
    lamps.append((-126.3, 9.4))
    for n, (s, t) in enumerate(lamps):
        lamp(n, s, t, ink, glow)

    # -------------------------------------------------------------- benches
    benches = 0
    for s in (-100.0, -78.0, -56.0, -34.0):                      # shore walkway
        bench(benches, s, edge_t(s, EDGE_SE), +1, timber, ink); benches += 1
        bench(benches, s, edge_t(s, EDGE_NW), -1, timber, ink); benches += 1
    for s in (-14.0, -8.0):                                      # mid bay
        bench(benches, s, edge_t(s, EDGE_SE), +1, timber, ink); benches += 1
        bench(benches, s, edge_t(s, EDGE_NW), -1, timber, ink); benches += 1
    for s in (30.0, 62.0, 94.0):                                 # bay walkway
        bench(benches, s, edge_t(s, EDGE_SE), +1, timber, ink); benches += 1
        bench(benches, s, edge_t(s, EDGE_NW), -1, timber, ink); benches += 1
    for s in (121.5, 126.0):                                     # end platform
        bench(benches, s, edge_t(s, EDGE_SE), +1, timber, ink); benches += 1
        bench(benches, s, edge_t(s, EDGE_NW), -1, timber, ink); benches += 1

    # ------------------------------------------------- fish-cleaning stations
    for i, tf in enumerate((-9.5, 9.5)):
        sbox(f"fishtop{i}", 118.6, 120.2, tf - 0.45, tf + 0.45,
             Z_SURF + 0.82, Z_SURF + 0.92, steel)
        for ds in (0.15, 1.45):
            sbox(f"fishleg{i}_{ds}", 118.6 + ds - 0.06, 118.6 + ds + 0.06,
                 tf - 0.35, tf + 0.35, Z_SURF, Z_SURF + 0.82, steel)

    # ------------------------------------------------------------------ bevels
    # The deck masses carry the miniature read. The 44 lamps, ~190 railing
    # posts, rails, piles, benches and lanes are sub-pixel edges — beveling
    # them would double the budget for nothing.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if name.startswith(("deck_", "bullrail", "plaza")):
            bevel(obj, width=0.06, segments=1)

    print(f"[build] piles={piles} rail_posts={posts} lamps={len(lamps)} benches={benches}")
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
    print("[build] anchor lon/lat: -122.3955159 37.7994429 (OSM pier polygon OBB centre)")
    print("[build] pier axis 54.65 deg true; entry faces 234.65 deg (SW)")
    print("[build] Z=0 is the WATERLINE: piles 0-2.4, deck 3.0, lamp tops 7.6")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "pier-7.blend")
    glb = os.path.join(out, "pier-7.glb")
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
