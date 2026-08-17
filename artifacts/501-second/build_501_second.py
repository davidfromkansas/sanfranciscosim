"""Deterministic Blender build of the SF-SIM miniature 501 Second Street.

    blender -b --python build_501_second.py -- [--out DIR]

Writes 501-second.blend and 501-second.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint OBB centre (anchor lon -122.3929683,
lat 37.7831785), min Z = 0, penthouse roof exactly 37.70 m.

Design (see REFERENCE.md for the sources behind every number):

* the OSM footprint (way 112758588) reduced to its minimum-area rectangle —
  72.79 x 42.24 m, 3,074 m2, at 45.4 deg off the world axes. DataSF LiDAR
  (SF3774067) independently gives 72.67 x 42.39 m and 3,107 m2, a 1% agreement,
  so unlike 524-second there is no footprint conflict to adjudicate here;
* the recognition cue is SIZE plus a TRIPARTITE COMPOSITION. This is the
  largest bespoke footprint in the SoMa set — five times 524-second, eighteen
  times 358-brannan — and a proper 1925 Renaissance-Revival commercial block:
  a two-storey base under a bracketed belt cornice at 11.6 m, a five-storey
  shaft of vertical piers, a carved frieze, a projecting main cornice at
  31.1-32.2 m, and a plain parapet to a MEASURED 33.0 m;
* the second cue is COLOUR: cream cast stone in a district of red brick. The
  contrast against 524-second, 78 m away across Second Street, is half of why
  this building is identifiable from the air;
* three public elevations, not one. Second Street (SW, 42.24 m) is the address;
  BRYANT STREET (NW, 72.79 m) is the hero and carries the main entrance under a
  flat canopy lettered "501 SECOND"; the Federal Street side (SE, 72.79 m) is a
  real but plainer elevation. Only the northeast end is a party wall;
* the penthouse at 37.70 m is the crest and the only silhouette break on an
  otherwise dead-level parapet. DataSF hgt_max 37.66 m is REAL here — 6.41 m
  std over 12,467 cells with a modal plane at 33.26 m, and the nearest taller
  neighbour is 60 m away. That is the opposite call from 524-second, where the
  equivalent maximum was edge bleed. Reconcile per building, never by habit;
* a light court cut into the roof: a 3,074 m2 footprint against a 2,758 m2
  typical floor leaves 316 m2 unaccounted for, and the aerial shows the notch;
* the roof membrane is Toy_sand from the start. Settled empirically on
  524-second in the same session: Toy_roofd was rejected at authoring time,
  Toy_steel shipped, and the live scene then measured its lit deck 27% darker
  than the baked neighbours. This roof is three times bigger;
* night state: the entrance canopy sign strip is the hero glow, supported by a
  SCATTER of lit windows across several floors — a full multi-tenant office
  building, not a uniform grid and not a single lit floor. Glow surfaces are
  thin shells proud of the opaque surface behind them (the app renders _Glow in
  a separate layer that is ~12% alpha by day).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way 112758588 projected with the app's tangent projection, reduced to its
# minimum-area OBB and recentred on the OBB centre. CCW in (x=east, y=north).
FOOTPRINT = [
    (-40.74, -10.51),   # west corner  (Second St x Bryant St)
    (-11.10, -40.59),   # south corner
    (40.74, 10.51),     # east corner
    (11.10, 40.59),     # north corner
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_SECOND = 0   # 42.24 m, faces SW 225.4 deg — Second Street, the address
EDGE_FEDERAL = 1  # 72.79 m, faces SE 135.4 deg — Federal Street side, plainer
EDGE_PARTY = 2    # 42.24 m, faces NE  45.4 deg — party wall to 533 Second
EDGE_BRYANT = 3   # 72.79 m, faces NW 315.4 deg — Bryant Street, the hero

# Only the parapet and the crest are measured; the floor split is
# photogrammetric, derived by dividing the measured 33.0 m across the permits'
# 2 + 5 storey reading.
Z_BASE = 11.60          # top of the two-storey base = belt cornice springing
Z_BELT1 = 12.50         # top of the belt cornice
FLOOR_H = 3.90          # shaft floor-to-floor
SHAFT_FLOORS = 5
Z_FRIEZE0 = 29.90
Z_CORNICE0 = 30.85      # main cornice springing
Z_CORNICE1 = 32.20      # top of the main cornice
Z_PARAPET = 33.00       # DataSF LiDAR hgt_majority 33.26 / median 32.72; OSM height=33
Z_CREST = 37.70         # penthouse roof = the bbox top (DataSF hgt_max 37.66)

Z_G0, Z_G1 = 1.20, 5.20      # ground-storey openings
Z_G2, Z_G3 = 6.40, 10.60     # second-storey openings (the base is TWO storeys)
Z_ENTRY_TOP = 5.20           # the Bryant entrance recess
Z_CANOPY0, Z_CANOPY1 = 5.20, 5.62
SHAFT_WIN_H = 2.80           # shaft opening height within each floor
SHAFT_WIN_SILL = 0.70        # sill above each floor line

SKIN = 0.10
# First aerial review: at PIER_W 0.90 / PIER_PROJ 0.12 the shaft read as a flat
# grid of horizontal slots and the tripartite composition — the whole identity —
# did not survive at distance. Piers widened and pushed out, both cornices
# thickened and their projection increased. This is where the style bible's
# semantic exaggeration is spent on this asset; the shadow line a deep cornice
# throws is what makes the three horizontal moves legible from the air.
PIER_W = 1.30
PIER_PROJ = 0.22
BELT_PROJ = 0.80
CORNICE_PROJ = 1.20
PARAPET_T = 0.40

# Bay counts per public elevation. 26 bays x 5 shaft floors = 130 openings is
# the triangle risk in this asset; the plan's rule is to cut bays before cutting
# cornices, because the cornices are the identity and the windows are texture.
BAYS_SECOND = 7
BAYS_BRYANT = 13
BAYS_FEDERAL = 13

LIGHT_COURT = (14.0, 9.0, 26.0)   # w, d, floor height
PENTHOUSE = (16.0, 11.0)          # w, d

PALETTE_HEX = {
    # The identity colour: cast stone / terracotta, cream, in a brick district.
    "Toy_cream": "f2ede3",
    "Toy_stone": "d9d2c2",
    # Roof membrane and light-court floor. Pale from the start — see docstring.
    "Toy_sand": "ece4d4",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_ink": "3a3530",
    "Toy_glass_Glow": "6f95b8",
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
    """Structural bay centres along an edge, in that edge's u coordinate."""
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
    """Miniature-style edge softening (style bible s.4). Width is capped at a
    third of the object's thinnest dimension: the applied panels here are only
    60-200 mm thick, and a flat bevel on those relies entirely on clamp_overlap,
    which collapses opposing profiles into zero-area slivers."""
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


def wall_panel(name, frame, u_centre, profile, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in a wall plane, extruded outward
    from offset d0 to d1 along that wall's normal. `frame` is (origin, t, n)."""
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


def face_panel(name, edge, u_centre, profile, d0, d1, mat):
    return wall_panel(name, edge_wall(edge), u_centre, profile, d0, d1, mat)


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
    Bryant Street edge from its NORTH corner (0 .. 72.79), v runs INTO the block
    away from Bryant (0 .. 42.24)."""
    origin, _l, t, n = poly_edge(EDGE_BRYANT)
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
        # Flagged for the app's night pass; emission is off in the day asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat




# --------------------------------------------------------------------- parts


def rect_opening(tag, frame, u, w, z0, z1, frame_mat, fill_mat, base_d, glow_mat=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads
    as a border ring around a recessed opening. No booleans, all closed solids."""
    wall_panel(f"{tag}_frame", frame, u, rect_profile(w, z0, z1), 0.0, base_d + 0.06, frame_mat)
    inset = 0.16
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
        g = 0.28
        wall_panel(
            f"{tag}_glow",
            frame,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            base_d + 0.10,
            base_d + 0.17,
            glow_mat,
        )


def cornice(tag, edges, z0, z1, proj, mat):
    """A projecting horizontal band on selected faces only. Built per face
    rather than as a ring_band so the party wall can be left plain — a mitred
    ring would carry the cornice around a wall that is hard against 533 Second."""
    for e in edges:
        _a, length, _t, _n = poly_edge(e)
        face_panel(f"{tag}_{e}", e, length / 2.0, rect_profile(length, z0, z1), 0.0, proj, mat)


def shaft_floor_z(k):
    """Floor line k of the shaft, k = 0..SHAFT_FLOORS-1."""
    return Z_BELT1 + k * FLOOR_H


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    cream = material("Toy_cream")
    stone = material("Toy_stone")
    sand = material("Toy_sand")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    ink = material("Toy_ink")
    glass_glow = material("Toy_glass_Glow")
    gold_glow = material("Toy_gold_Glow")

    PUBLIC = (EDGE_SECOND, EDGE_BRYANT, EDGE_FEDERAL)
    BAYS = {EDGE_SECOND: BAYS_SECOND, EDGE_BRYANT: BAYS_BRYANT, EDGE_FEDERAL: BAYS_FEDERAL}

    # --- shell -------------------------------------------------------------
    # The cap sits at Z_PARAPET - 0.25, not at Z_PARAPET: the roof deck is laid
    # on top of it as four slabs around the light court, so the court reads as a
    # 0.25 m recess in the pale deck with no boolean anywhere. See REPORT.md.
    Z_COURT = Z_PARAPET - 0.25
    prism("body", FOOTPRINT, 0.0, Z_COURT, cream, mat_caps=sand)

    # --- the three horizontal moves ----------------------------------------
    cornice("belt", PUBLIC, Z_BASE, Z_BELT1, BELT_PROJ, stone)
    cornice("frieze", PUBLIC, Z_FRIEZE0, Z_CORNICE0, 0.05, cream)
    # the main cornice DOES return on the party wall: it is the top of the
    # building and the aerial camera sees all four edges of it
    cornice("cornice", (0, 1, 2, 3), Z_CORNICE0, Z_CORNICE1, CORNICE_PROJ, stone)
    ring_band("parapet", FOOTPRINT, Z_CORNICE1, Z_PARAPET - 0.14, -PARAPET_T, 0.0, cream)
    ring_band(
        "coping", FOOTPRINT, Z_PARAPET - 0.14, Z_PARAPET, -PARAPET_T - 0.05, 0.05, stone
    )

    # --- piers and openings, per public elevation ---------------------------
    for e in PUBLIC:
        _a, length, _t, _n = poly_edge(e)
        n_bays = BAYS[e]
        frame = edge_wall(e)
        pitch = length / n_bays
        # pier on every bay boundary, including both ends
        for i in range(n_bays + 1):
            wall_panel(
                f"pier{e}_{i}",
                frame,
                min(max(i * pitch, PIER_W / 2.0), length - PIER_W / 2.0),
                rect_profile(PIER_W, Z_BELT1, Z_CORNICE0),
                0.0,
                PIER_PROJ,
                cream,
            )
        open_w = pitch - PIER_W - 0.35
        for i, u in enumerate(bay_centres(e, n_bays)):
            # base storey: one tall opening per bay
            # the base is TWO storeys, not one tall one — the first build merged
            # them and lost the horizontal that the belt cornice answers
            rect_opening(f"base{e}_{i}", frame, u, open_w, Z_G0, Z_G1, stone, glass, SKIN)
            rect_opening(f"base2{e}_{i}", frame, u, open_w, Z_G2, Z_G3, stone, glass, SKIN)
            # shaft: one opening per bay per floor
            for k in range(SHAFT_FLOORS):
                z0 = shaft_floor_z(k) + SHAFT_WIN_SILL
                lit = (i * 7 + k * 3 + e) % 11 < 2   # a scatter, not a grid
                rect_opening(
                    f"sh{e}_{i}_{k}",
                    frame,
                    u,
                    open_w,
                    z0,
                    z0 + SHAFT_WIN_H,
                    stone,
                    glass,
                    0.0,
                    glass_glow if lit else None,
                )

    # --- Bryant Street: the main entrance and its lit canopy ----------------
    _a_b, len_b, _t_b, _n_b = poly_edge(EDGE_BRYANT)
    bryant = edge_wall(EDGE_BRYANT)
    u_entry = len_b * 0.34
    wall_panel(
        "entry_recess", bryant, u_entry, rect_profile(4.60, 0.0, Z_ENTRY_TOP), 0.0, SKIN + 0.02, ink
    )
    wall_panel(
        "entry_canopy",
        bryant,
        u_entry,
        rect_profile(5.40, Z_CANOPY0, Z_CANOPY1),
        0.0,
        SKIN + 1.60,
        stone,
    )
    # the night hero: the "501 SECOND" strip on the canopy fascia
    wall_panel(
        "entry_sign_glow",
        bryant,
        u_entry,
        rect_profile(4.20, Z_CANOPY0 + 0.10, Z_CANOPY1 - 0.10),
        SKIN + 1.58,
        SKIN + 1.66,
        gold_glow,
    )
    # a second, plainer recessed service bay beside it
    wall_panel(
        "service_recess",
        bryant,
        u_entry + 8.4,
        rect_profile(4.00, 0.0, 4.40),
        0.0,
        SKIN + 0.02,
        ink,
    )

    # --- roof ---------------------------------------------------------------
    # u runs along the Bryant edge from its north corner (0 .. 72.79); v runs
    # into the block away from Bryant (0 .. 42.24).
    cw, cd, _cz = LIGHT_COURT
    cu, cv = len_b * 0.62, 21.1          # court centre, toward the Federal side
    deck_t = 0.25
    # four slabs forming the deck frame around the court
    for tag, u, v, su, sv in (
        ("n", len_b / 2.0, (cv - cd / 2.0) / 2.0, len_b, cv - cd / 2.0),
        ("s", len_b / 2.0, (cv + cd / 2.0 + 42.24) / 2.0, len_b, 42.24 - (cv + cd / 2.0)),
        ("w", (cu - cw / 2.0) / 2.0, cv, cu - cw / 2.0, cd),
        ("e", (cu + cw / 2.0 + len_b) / 2.0, cv, len_b - (cu + cw / 2.0), cd),
    ):
        roof_box(f"deck_{tag}", u, v, Z_COURT, Z_COURT + deck_t, su, sv, sand)
    # The court itself. A true 7 m well would need a boolean or a much heavier
    # annulus body; the first top-view review showed that the 0.25 m step alone
    # is invisible from directly overhead, where there is no grazing light to
    # throw a shadow. It is therefore a DARK panel set in the gap between the
    # deck slabs — at the app's camera distance that is exactly what a light
    # court looks like, and it costs 12 triangles. Recorded in REPORT.md.
    roof_box("court", cu, cv, Z_COURT - 0.02, Z_COURT + 0.08, cw, cd, roofd)

    # penthouse: the crest, toward the Second Street (west) end
    pw, pd = PENTHOUSE
    roof_box("penthouse", len_b * 0.18, 19.0, Z_COURT, Z_CREST, pw, pd, cream)
    roof_box(
        "penthouse_cap", len_b * 0.18, 19.0, Z_CREST - 0.30, Z_CREST, pw + 0.5, pd + 0.5, sand
    )
    roof_box(
        "penthouse_glaze", len_b * 0.18, 19.0 - pd / 2.0 + 0.1, Z_CREST - 2.6, Z_CREST - 0.9,
        pw - 3.0, 0.3, glassl,
    )

    # plant, grouped against the party-wall (east) end so the middle stays open
    for i, (u, v, sw, sd, h) in enumerate(
        (
            (61.0, 9.5, 4.2, 3.0, 1.80),
            (66.0, 14.0, 3.4, 2.6, 1.45),
            (57.5, 15.5, 3.0, 2.4, 1.20),
        )
    ):
        roof_box(f"plant{i}", u, v, Z_COURT + deck_t, Z_COURT + deck_t + h, sw, sd, steel)
    for i, (u, v) in enumerate(
        ((36.0, 8.0), (44.0, 33.0), (24.5, 12.0), (50.0, 6.5), (31.0, 27.0))
    ):
        roof_box(f"vent{i}", u, v, Z_COURT + deck_t, Z_COURT + deck_t + 0.85, 1.30, 1.30, roofd)
    roof_box("hatch", 26.0, 34.0, Z_COURT + deck_t, Z_COURT + deck_t + 0.60, 1.80, 1.40, roofd)
    # a stair bulkhead at the Federal end, so the roof has a second positive
    # shape besides the penthouse across 3,074 m2 of otherwise flat deck
    roof_box("bulkhead", 52.0, 36.0, Z_COURT + deck_t, Z_COURT + deck_t + 2.60, 6.0, 4.4, cream)

    # Bevel budget: the chunky masses and the three cornices carry the miniature
    # read, so they get the full 0.10/2. Applied panels are small and numerous —
    # their frames get a token 1-segment softening and the fills/glow shells none.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")):
            continue
        if obj.name.endswith("_frame") or obj.name.startswith(("pier", "frieze")):
            bevel(obj, width=0.04, segments=1)
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
    print("[build] anchor lon/lat: -122.3929683 37.7831785 (footprint OBB centre)")
    print("[build] Second Street front heading: 225.4 deg true (SW)")
    print("[build] Bryant Street elevation heading: 315.4 deg true (NW)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "501-second.blend")
    glb = os.path.join(out, "501-second.glb")
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
