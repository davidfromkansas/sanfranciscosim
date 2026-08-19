"""Deterministic Blender build of the SF-SIM miniature 132 The Embarcadero.

    blender -b --python build_132_embarcadero.py -- [--out DIR]

Writes 132-embarcadero.blend and 132-embarcadero.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = footprint OBB centre (anchor
lon -122.3925476, lat 37.7931482), min Z = 0, bulkhead crest exactly 29.57 m.

Design (see REFERENCE.md for the sources behind every number):

* the OSM footprint (way 193054135) reduced to its minimum-area rectangle —
  13.75 m of street frontage running 42.95 m back through the lot, at 44.95 deg
  off the world axes. Three surveys agree to within 5%: OSM 590.6 m2, DataSF
  LiDAR 617 m2, Assessor floor area / 7 storeys 585 m2. OSM is used because it
  is the only one whose corners sit on the party walls this row actually shares;
* the building is a SLAB ON EDGE. 13.75 m wide, 42.95 m deep, both long sides
  party walls. There is no silhouette to work with, so the recognition load
  falls on colour (the only red brick in its stretch of the row), on the
  proportion, and on the crown band;
* the CROWN BAND is the cue that gets the geometry: a 2.50 m pale band at
  24.40-26.90 m standing 0.15 m proud with a chamfered underside, wrapped as a
  continuous ring. The plan called for it on the two frontages with 1 m returns;
  it is run all the way round instead because the northwest party wall is
  exposed above ~18 m and reads from the aerial camera, and because a closed
  ring is both cheaper and cleaner than four mitred stubs;
* SEVEN storeys, and the two frontages do NOT match. The Embarcadero side opens
  up: a storefront base, a brick spandrel course with wall lights, and a
  full-width second-floor glazed ribbon at 4.37-6.11 m. The Steuart side is an
  institution's front door: a dark recessed entrance under a projecting brick
  lintel with a gold lettering strip, and a BLIND second floor. That asymmetry
  is deliberate and must survive any simplification;
* floors 3-7 carry the same six-bay punched grid on both fronts, on the sills
  measured photogrammetrically from panorama OLku-hi1dEEvbjsiBr8EWw: 7.45,
  10.70, 14.37, 17.87, 21.37 m, openings 1.58 m tall on a 2.292 m bay;
* heights: roof deck 26.82 m (DataSF LiDAR hgt_median), parapet 27.40 m
  (photogrammetric, 40 samples, sigma 0.08 m), bulkhead crest 29.57 m (LiDAR
  hgt_max, read as the lift overrun a 1984 seven-storey office with traction
  lifts must have — see REPORT.md s.3, this is the one inferred number);
* night state: the Embarcadero ribbon and storefront are the hero — a
  continuous bright horizontal at the waterfront, which is what this building
  actually does after dark. The Steuart gold lettering strip and a scattered
  third of the upper windows support it. Glow shells are thin and their back
  faces are buried inside the opaque fill behind them; a CLOSED glow box is two
  alpha layers and reads ~23% by day, which would tint the brick;
* TWO COLOUR CORRECTIONS made after the first review render, both on recorded
  project lessons: the roof deck is Toy_sand, not the plan's Toy_roofd, because
  Toy_roofd measures rgb(9,9,12) on a horizontal deck in the app and reads as a
  black hole from the downward camera (524-second's shipped value, and the same
  trap 358-brannan recorded); and the crown band is Toy_stone rather than
  Toy_trim, and 1.50 m rather than 2.50 m, because near-white at 2.5 m turned the
  building into a red box wearing a white collar and because the band's depth is
  the least certain facade dimension in the dossier (asset plan 2.15 risk 4);
* DEVIATION from the plan: the kerbside bollard row is NOT modelled. It stands
  1.6 m clear of the wall, so including it would push the axis-aligned bounding
  box out on the Steuart side only and move the base-centre origin ~0.34 m off
  the surveyed anchor. Data accuracy (AGENTS rule 5) beats the detail.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way 193054135 projected with the app's tangent projection, reduced to its
# minimum-area OBB and recentred on the OBB centre. CCW in (x=east, y=north).
_HALF_W = 13.75 / 2.0        # street frontage
_HALF_D = 42.95 / 2.0        # depth, Embarcadero -> Steuart
_F = (math.sin(math.radians(134.95)), math.cos(math.radians(134.95)))  # along the street line
_G = (math.sin(math.radians(44.95)), math.cos(math.radians(44.95)))    # toward the Embarcadero

FOOTPRINT = [
    (_HALF_D * _G[0] + _HALF_W * _F[0], _HALF_D * _G[1] + _HALF_W * _F[1]),  # Emb / SE
    (_HALF_D * _G[0] - _HALF_W * _F[0], _HALF_D * _G[1] - _HALF_W * _F[1]),  # Emb / NW
    (-_HALF_D * _G[0] - _HALF_W * _F[0], -_HALF_D * _G[1] - _HALF_W * _F[1]),  # Steuart / NW
    (-_HALF_D * _G[0] + _HALF_W * _F[0], -_HALF_D * _G[1] + _HALF_W * _F[1]),  # Steuart / SE
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_EMB = 0      # 13.75 m, faces NE  44.95 deg — The Embarcadero, the address
EDGE_NW = 1       # 42.95 m, faces NW 314.95 deg — party wall, 110-116 The Embarcadero
EDGE_STEUART = 2  # 13.75 m, faces SW 224.95 deg — Steuart Street, the entrance
EDGE_SE = 3       # 42.95 m, faces SE 134.95 deg — party wall, Steuart Place

Z_DECK = 26.82        # roof membrane (DataSF LiDAR hgt_median — measured)
Z_PARAPET = 27.40     # parapet coping top (photogrammetric — measured)
Z_CREST = 29.57       # lift/stair bulkhead top = the bbox top (LiDAR hgt_max — inferred)

Z_CROWN0, Z_CROWN1 = 25.40, 26.90   # the pale crown band
PARAPET_T = 0.40
COPING_H = 0.12
CROWN_PROJ = 0.15

# Floors 3-7: (sill, head). Photogrammetric, panorama OLku-hi1dEEvbjsiBr8EWw.
WINDOW_ROWS = [(7.45, 9.03), (10.70, 12.28), (14.37, 15.95), (17.87, 19.45), (21.37, 22.95)]
BAYS = 6
OPEN_W = 1.62

# Embarcadero base
Z_SHOP0, Z_SHOP1 = 0.30, 3.10       # storefront glazing
Z_SPAN0, Z_SPAN1 = 3.10, 3.55       # brick spandrel course over it
Z_RIB0, Z_RIB1 = 4.37, 6.11         # the second-floor glazed ribbon
SHOP_BAYS = 3
SHOP_W = 3.60
RIBBON_W = 12.85

# Steuart base
Z_ENTRY0, Z_ENTRY1 = 0.00, 3.30     # the recessed entrance bay
Z_LETTER0, Z_LETTER1 = 3.55, 4.05   # the incised lettering, read as one strip
Z_LINTEL0, Z_LINTEL1 = 4.30, 4.85   # the projecting brick hood
ENTRY_W = 5.60
LETTER_W = 9.00
LINTEL_PROJ = 0.25
DOOR_W, DOOR_H = 1.15, 2.45

# Roof. (u, v): u along the Embarcadero edge from its southeast corner,
# v INTO the block toward Steuart. The Embarcadero third of the deck is left
# clean so the crown band reads uninterrupted from the water.
BULKHEAD = (6.90, 33.20, 5.50, 4.00)    # u, v, su, sv
ANTENNA = (6.90, 12.60, 4.00, 2.00)
PLANT = ((4.30, 21.00, 2.40, 2.00, 1.50), (9.40, 22.80, 2.00, 1.80, 1.15),
         (6.60, 27.40, 3.20, 1.60, 0.90))
VENTS = ((3.60, 17.20), (10.10, 30.30))
MASTS = (-1.35, 0.0, 1.35)

PALETTE_HEX = {
    "Toy_brick": "c96f4a",
    "Toy_trim": "f3efe6",
    "Toy_stone": "d9d2c2",
    "Toy_sand": "ece4d4",
    "Toy_roofd": "45454a",
    "Toy_ink": "3a3530",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_navy": "2f4763",
    "Toy_slate": "6f7883",
    "Toy_steel": "9aa0a6",
    "Toy_gold": "caa64a",
    "Toy_glass_Glow": "6f95b8",
    "Toy_glassl_Glow": "6f95b8",
    "Toy_trim_Glow": "f3efe6",
    "Toy_gold_Glow": "caa64a",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def edge_frame(poly, i):
    """Edge i of a CCW polygon: (origin, length, tangent unit, outward normal)."""
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def poly_edge(i):
    return edge_frame(FOOTPRINT, i)


def offset_polygon(poly, d):
    """Miter offset of the convex CCW footprint; positive d moves outward."""
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


def bay_centres(edge, count):
    _a, length, _t, _n = poly_edge(edge)
    pitch = length / count
    return [(i + 0.5) * pitch for i in range(count)]


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


def ring_profile(name, poly, section, mat):
    """Closed ring swept round a footprint from an arbitrary cross-section.
    `section` is a list of (outward offset, z) points; consecutive loops are
    joined cyclically, so the result is a closed manifold solid — which the
    signed-volume normals gate requires. An open sloped band is NOT acceptable:
    the first build authored the crown's underside chamfer as a bare skirt and
    the validator flagged it as inverted, because an open surface has no sign."""
    loops = [offset_polygon(poly, off) for off, _z in section]
    npts = len(loops[0])
    nsec = len(section)
    verts = []
    for loop, (_off, z) in zip(loops, section):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(nsec):
        a0, b0 = k * npts, ((k + 1) % nsec) * npts
        for i in range(npts):
            j = (i + 1) % npts
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def wall_panel(name, frame, u_centre, profile, d0, d1, mat):
    a, t, n = frame
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


def edge_wall(edge):
    a, _length, t, n = poly_edge(edge)
    return (a, t, n)


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
    Embarcadero edge from its southeast corner, v runs INTO the block."""
    origin, _l, t, n = poly_edge(EDGE_EMB)
    cx = origin[0] + t[0] * u - n[0] * v
    cy = origin[1] + t[1] * u - n[1] * v
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=math.atan2(t[1], t[0]))


def roof_cyl(name, u, v, z0, z1, r, mat, segs=8):
    origin, _l, t, n = poly_edge(EDGE_EMB)
    cx = origin[0] + t[0] * u - n[0] * v
    cy = origin[1] + t[1] * u - n[1] * v
    ring = [
        (cx + r * math.cos(2 * math.pi * i / segs), cy + r * math.sin(2 * math.pi * i / segs))
        for i in range(segs)
    ]
    return prism(name, ring, z0, z1, mat)


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


def rect_opening(tag, frame, u, w, z0, z1, frame_mat, fill_mat, base_d, glow_mat=None,
                 inset=0.16, glow_inset=0.30):
    """Frame panel + a smaller fill that protrudes further, so the frame reads
    as a border ring around the opening. No booleans, all closed solids. The
    glow shell's back face sits INSIDE the fill so only one alpha layer shows."""
    wall_panel(f"{tag}_frame", frame, u, rect_profile(w, z0, z1), 0.0, base_d + 0.06, frame_mat)
    wall_panel(
        f"{tag}_fill",
        frame,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        0.0,
        base_d + 0.13,
        fill_mat,
    )
    if glow_mat is not None:
        wall_panel(
            f"{tag}_glow",
            frame,
            u,
            rect_profile(w - 2 * glow_inset, z0 + glow_inset, z1 - glow_inset),
            base_d + 0.10,
            base_d + 0.17,
            glow_mat,
        )


# Floors 3-7, bays 0-5. The lit set is scattered rather than banded — an office
# with people still in it, not a lit-up box (the lesson recorded on 524-second).
LIT = {(0, 1), (0, 4), (1, 0), (1, 3), (2, 2), (2, 5), (3, 1), (3, 4), (4, 0), (4, 3)}


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    brick = material("Toy_brick")
    trim = material("Toy_trim")
    roofd = material("Toy_roofd")
    ink = material("Toy_ink")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    navy = material("Toy_navy")
    slate = material("Toy_slate")
    steel = material("Toy_steel")
    stone = material("Toy_stone")
    sand = material("Toy_sand")
    gold = material("Toy_gold")
    glass_glow = material("Toy_glass_Glow")
    glassl_glow = material("Toy_glassl_Glow")
    trim_glow = material("Toy_trim_Glow")
    gold_glow = material("Toy_gold_Glow")

    emb = edge_wall(EDGE_EMB)
    steuart = edge_wall(EDGE_STEUART)
    _a, len_emb, _t, _n = poly_edge(EDGE_EMB)

    # --- shell: red brick body, its cap IS the roof deck --------------------
    prism("body", FOOTPRINT, 0.0, Z_DECK, brick, mat_caps=sand)

    # --- the crown band: the one cue this building has ----------------------
    # A continuous ring, not two fronts with returns: the northwest party wall
    # is exposed above ~18 m and reads from the aerial camera.
    ring_profile(
        "crown",
        FOOTPRINT,
        [
            (0.0, Z_CROWN0 - 0.30),   # springing, flush with the brick
            (CROWN_PROJ, Z_CROWN0),   # out over a 0.30 m chamfer
            (CROWN_PROJ, Z_CROWN1),   # the band face
            (0.0, Z_CROWN1),          # back to the wall under the parapet
        ],
        stone,
    )

    # --- parapet and coping, continuous on all four sides -------------------
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET - COPING_H, -PARAPET_T, 0.02, brick)
    ring_band("coping", FOOTPRINT, Z_PARAPET - COPING_H, Z_PARAPET, -PARAPET_T - 0.05, 0.08, ink)

    # --- floors 3-7: the six-bay punched grid, both frontages ---------------
    for edge, frame, tag in ((EDGE_EMB, emb, "e"), (EDGE_STEUART, steuart, "s")):
        for row, (z0, z1) in enumerate(WINDOW_ROWS):
            for bay, u in enumerate(bay_centres(edge, BAYS)):
                lit = glass_glow if (row, bay) in LIT else None
                rect_opening(
                    f"win_{tag}{row}{bay}", frame, u, OPEN_W, z0, z1, trim, glass, 0.0,
                    glow_mat=lit, inset=0.13, glow_inset=0.26,
                )

    # --- The Embarcadero base: storefront, spandrel course, glazed ribbon ---
    for i, u in enumerate(bay_centres(EDGE_EMB, SHOP_BAYS)):
        rect_opening(
            f"shop{i}", emb, u, SHOP_W, Z_SHOP0, Z_SHOP1, navy, glassl, 0.0,
            glow_mat=glassl_glow, inset=0.18, glow_inset=0.34,
        )
    wall_panel(
        "spandrel", emb, len_emb / 2.0,
        rect_profile(len_emb, Z_SPAN0, Z_SPAN1), 0.0, 0.10, brick,
    )
    for i, u in enumerate(bay_centres(EDGE_EMB, SHOP_BAYS)):
        wall_panel(
            f"walllight{i}", emb, u,
            rect_profile(0.26, Z_SPAN0 + 0.09, Z_SPAN1 - 0.09), 0.05, 0.17, trim_glow,
        )
    rect_opening(
        "ribbon", emb, len_emb / 2.0, RIBBON_W, Z_RIB0, Z_RIB1, trim, glassl, 0.0,
        glow_mat=glassl_glow, inset=0.16, glow_inset=0.32,
    )

    # --- Steuart Street: the institution's front door ------------------------
    wall_panel(
        "entry_recess", steuart, len_emb / 2.0,
        rect_profile(ENTRY_W, Z_ENTRY0, Z_ENTRY1), 0.0, 0.04, ink,
    )
    wall_panel(
        "entry_glass", steuart, len_emb / 2.0,
        rect_profile(3.20, Z_ENTRY0 + 0.15, Z_ENTRY1 - 0.20), 0.0, 0.11, glassl,
    )
    wall_panel(
        "entry_glass_glow", steuart, len_emb / 2.0,
        rect_profile(2.86, Z_ENTRY0 + 0.32, Z_ENTRY1 - 0.37), 0.08, 0.15, glassl_glow,
    )
    for i, u in enumerate((2.35, len_emb - 2.35)):
        wall_panel(
            f"service_door{i}", steuart, u,
            rect_profile(DOOR_W, 0.0, DOOR_H), 0.0, 0.07, navy,
        )
    wall_panel(
        "letters", steuart, len_emb / 2.0,
        rect_profile(LETTER_W, Z_LETTER0, Z_LETTER1), 0.0, 0.07, gold,
    )
    wall_panel(
        "letters_glow", steuart, len_emb / 2.0,
        rect_profile(LETTER_W - 0.30, Z_LETTER0 + 0.09, Z_LETTER1 - 0.09), 0.04, 0.12, gold_glow,
    )
    wall_panel(
        "lintel", steuart, len_emb / 2.0,
        rect_profile(len_emb, Z_LINTEL0, Z_LINTEL1), 0.0, LINTEL_PROJ, brick,
    )

    # --- roof: bulkhead, plant, antenna platform ----------------------------
    u, v, su, sv = BULKHEAD
    roof_box("bulkhead", u, v, Z_DECK, Z_CREST - 0.14, su, sv, slate)
    roof_box("bulkhead_cap", u, v, Z_CREST - 0.14, Z_CREST, su + 0.24, sv + 0.24, stone)

    for i, (pu, pv, psu, psv, ph) in enumerate(PLANT):
        roof_box(f"plant{i}", pu, pv, Z_DECK, Z_DECK + ph, psu, psv, slate)
    for i, (vu, vv) in enumerate(VENTS):
        roof_box(f"vent{i}", vu, vv, Z_DECK, Z_DECK + 0.55, 0.70, 0.70, roofd)

    au, av, asu, asv = ANTENNA
    roof_box("antenna_deck", au, av, Z_DECK, Z_DECK + 0.40, asu, asv, slate)
    for i, du in enumerate(MASTS):
        roof_cyl(f"mast{i}", au + du, av, Z_DECK + 0.40, Z_DECK + 2.20, 0.11, steel, segs=6)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.10/2. Applied panels are small and numerous — their frames get a
    # token 1-segment softening and the fills/glow shells none at all.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")) or obj.name.startswith(("mast", "walllight")):
            continue
        if obj.name.endswith("_frame") or obj.name.startswith(
            ("letters", "service_door", "entry_", "spandrel", "vent")
        ):
            bevel(obj, width=0.035, segments=1)
        else:
            bevel(obj, width=0.10, segments=2)

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
    print("[build] anchor lon/lat: -122.3925476 37.7931482 (footprint OBB centre)")
    print("[build] Embarcadero front heading: 44.95 deg true (NE)")
    print("[build] Steuart Street front heading: 224.95 deg true (SW)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "132-embarcadero.blend")
    glb = os.path.join(out, "132-embarcadero.glb")
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
