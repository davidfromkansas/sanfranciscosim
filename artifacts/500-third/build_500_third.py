"""Deterministic Blender build of the SF-SIM miniature 500 Third Street.

    blender -b --python build_500_third.py -- [--out DIR]

Writes 500-third.blend and 500-third.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint AABB centre (anchor lon -122.3958224,
lat 37.7808279), min Z = 0, rooftop bulkhead cap top exactly 26.5 m.

Design (see REFERENCE.md for the sources behind every number):

* the true OSM polygon (way/147508936, block 3776 lot 115) extruded as one
  near-square 58.6 x 47.7 m concrete-frame block filling its quarter block at
  3rd and Bryant — a 1927 industrial loft with all four elevations exposed;
* five storeys: one tall charcoal storefront ground floor under four identical
  upper floors of big steel-sash windows, flat parapet at 23.0 m;
* the identity is the WINDOW GRID, repeated across the 3rd Street (9 bays),
  Bryant Street (7) and south-east (7) elevations and deliberately absent from
  the Ritch Street service rear;
* the one event: the raised, capped corner crown at the north corner carrying an
  illuminated sign band on both faces, with a row of flag masts along the two
  street parapets;
* the roof is a working roof, not a designed one: pale membrane, the bulkhead
  penthouse north (the crest), the mechanical cluster south;
* night state: the crown sign band is the hero glow, a scatter of lit upper bays
  is the supporting rhythm, the entry transom and two lobby bays are the ground
  cue. Glow surfaces are thin shells proud of opaque glazing — the app renders
  _Glow in a separate layer at ~12% alpha by day, so a primary surface must
  never be authored as glow.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/147508936 projected with the app's tangent projection (LON0 -122.4375,
# LAT0 37.77) and recentred on the footprint AABB centre. CCW, (x east, y north).
FOOTPRINT = [
    (-4.197, 37.788),    # v0  north corner  (3rd x Bryant)
    (-37.293, 3.465),    # v1  west corner   (Bryant x Ritch)
    (3.933, -37.788),    # v2  south corner  (Ritch x SE lot)
    (37.293, -3.587),    # v3  east corner   (SE lot x 3rd)
]
E_BRYANT = (0, 1)  # NW front, 47.68 m, outward normal 314.0 deg true
E_RITCH = (1, 2)  # SW service rear, 58.32 m, normal 225.0 deg
E_SE = (2, 3)  # SE elevation over the parking lot, 47.78 m, normal 134.3 deg
E_THIRD = (3, 0)  # NE front, 58.59 m, outward normal 44.9 deg true

H_GF = 5.60  # top of the charcoal storefront band
H_PLINTH = 0.55  # stone plinth under the storefront
H_BELT0, H_BELT1 = 5.60, 6.00  # belt cornice over the ground floor
FLOORS = (6.00, 10.00, 14.00, 18.00)  # four upper floors, 4.00 m each
WIN_LO, WIN_HI = 0.85, 3.75  # window band within a floor
H_ROOF = 22.00  # roof membrane surface
H_PAR = 22.85  # parapet below its coping
H_PAR_CAP = 23.00  # parapet coping top
H_CROWN = 24.95  # raised corner crown below its cap
H_CROWN_CAP = 25.15  # corner crown cap top
H_BULK = 26.30  # bulkhead walls
H_CREST = 26.50  # bulkhead cap top = the architectural height
H_ELEV = 25.20  # elevator overrun, deliberately below the crest
H_MAST = 26.20  # flag masts, also below the crest

BAYS_THIRD = 9
BAYS_BRYANT = 7
BAYS_SE = 7
PIL_W = 0.85  # pilaster strip width
PIL_D = 0.22  # pilaster projection

BEVEL_W = 0.10
BEVEL_SEG = 2

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_sand": "ece4d4",
    "Toy_white": "f7f4ec",
    "Toy_ink": "3a3530",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_steel": "9aa0a6",
    "Toy_roofd": "45454a",
    "Toy_red": "c4453c",
    "Toy_navy": "2c4a70",
    "Toy_white_Glow": "f7f4ec",
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


# The building's own axes: U runs along the 3rd Street frontage (north-west
# positive), V points out toward 3rd Street. Every roof object is laid out in
# this frame so the composition follows the block rather than true north.
def _axes():
    _, _, _, t_third, n_third = poly_edge(E_THIRD)
    return t_third, n_third


U, V = _axes()


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

    The width is clamped to 40% of the object's thinnest dimension. Without the
    clamp, beveling a 0.05 m deep window reveal at 0.05 m collapses faces:
    clamp_overlap keeps the mesh watertight but leaves zero-area triangles, and
    a few reveals came out with inverted signed volume. Six objects and 630
    degenerate triangles failed the validator that way.
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
    # clamp_overlap keeps the mesh watertight but leaves zero-length edges behind
    # on the thin plates; dissolving them is what gets the validator's
    # degenerate-triangle count to zero.
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(bm_target := obj.data)
    bm.free()
    bm_target.shade_flat()
    return obj


def ensure_outward(obj):
    """Guarantee positive signed volume, which is the validator's authoritative
    normals test for a union of closed solids. recalc_face_normals gets it right
    for every solid here except a handful of the thin window plates, where the
    beveller leaves it ambiguous; flipping those is exact, not a guess."""
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
    along the outward normal (negative = recessed into the wall)."""
    a, _, _, t, n = poly_edge(edge)

    def p(s, d):
        return (a[0] + t[0] * s + n[0] * d, a[1] + t[1] * s + n[1] * d)

    return quad_box(name, [p(s0, d_in), p(s1, d_in), p(s1, d_out), p(s0, d_out)], z0, z1, mat)


def uv_box(name, u, v, z0, z1, su, sv, mat):
    """Box centred at (u, v) in the building frame, su along U, sv along V."""
    corners = []
    for du, dv in ((-su / 2, -sv / 2), (su / 2, -sv / 2), (su / 2, sv / 2), (-su / 2, sv / 2)):
        corners.append(uv(u + du, v + dv))
    return quad_box(name, corners, z0, z1, mat)


# ------------------------------------------------------------------- glyphs

# Stroke rectangles in a 1x1 glyph cell, (x0, y0, x1, y1), origin bottom-left.
GLYPHS = {
    "5": [(0.0, 0.82, 1.0, 1.0), (0.0, 0.44, 0.22, 0.86), (0.0, 0.42, 0.85, 0.6),
          (0.78, 0.1, 1.0, 0.52), (0.0, 0.0, 0.9, 0.18)],
    "0": [(0.0, 0.0, 1.0, 0.18), (0.0, 0.82, 1.0, 1.0),
          (0.0, 0.1, 0.22, 0.92), (0.78, 0.1, 1.0, 0.92)],
}


def facade_text(name, edge, text, s_start, z_base, size, depth, mat, gap=0.24, d0=0.0):
    """Extruded block numerals lying on a facade plane."""
    a, _, _, t, n = poly_edge(edge)
    objs = []
    cursor = s_start
    for k, ch in enumerate(text):
        for j, (x0, y0, x1, y1) in enumerate(GLYPHS[ch]):
            ss0, ss1 = cursor + x0 * size, cursor + x1 * size
            zz0, zz1 = z_base + y0 * size, z_base + y1 * size
            corners = [
                (a[0] + t[0] * ss0, a[1] + t[1] * ss0),
                (a[0] + t[0] * ss1, a[1] + t[1] * ss1),
            ]
            base = [
                (corners[0][0] + n[0] * d0, corners[0][1] + n[1] * d0),
                (corners[1][0] + n[0] * d0, corners[1][1] + n[1] * d0),
            ]
            quad = [
                base[0],
                base[1],
                (base[1][0] + n[0] * depth, base[1][1] + n[1] * depth),
                (base[0][0] + n[0] * depth, base[0][1] + n[1] * depth),
            ]
            objs.append(quad_box(f"{name}_{k}_{j}", quad, zz0, zz1, mat))
        cursor += size + gap
    return objs


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


def bay_spans(edge, nbays):
    """(s0, s1) of each bay opening, with a pilaster between and at both ends."""
    _, _, length, _, _ = poly_edge(edge)
    bay = (length - (nbays + 1) * PIL_W) / nbays
    out = []
    for k in range(nbays):
        s0 = PIL_W + k * (bay + PIL_W)
        out.append((s0, s0 + bay))
    return out, bay


def pilasters(tag, edge, nbays, mats, z0, z1):
    _, _, length, _, _ = poly_edge(edge)
    spans, bay = bay_spans(edge, nbays)
    for k in range(nbays + 1):
        s0 = k * (bay + PIL_W)
        bevel(
            wall_box(f"{tag}_pil{k}", edge, s0, s0 + PIL_W, z0, z1, -0.05, PIL_D,
                     mats["Toy_trim"]),
            width=0.06,
        )


def window_unit(tag, edge, s0, s1, z0, z1, mats, lit=False):
    """One steel-sash bay: ink reveal, glass slab, a 2 x 2 mullion cross.

    Everything is built PROUD of the wall — the walls are solid prisms with no
    cut openings, so anything at negative depth is buried inside the shell and
    invisible. The apparent recess comes from the pilasters standing 0.22 m out
    in front of this assembly (style bible s.5: windows are graphical elements
    before they are literal openings). Real sashes here are ~8 x 6 panes; a
    single cross is what survives at city distance.
    """
    bevel(wall_box(f"{tag}_reveal", edge, s0, s1, z0, z1, -0.06, 0.05, mats["Toy_ink"]),
          width=0.05, segments=1)
    wall_box(f"{tag}_glass", edge, s0 + 0.16, s1 - 0.16, z0 + 0.14, z1 - 0.14,
             0.04, 0.12, mats["Toy_glass"])
    sm = (s0 + s1) / 2
    zm = (z0 + z1) / 2
    wall_box(f"{tag}_mullv", edge, sm - 0.07, sm + 0.07, z0 + 0.14, z1 - 0.14,
             0.10, 0.16, mats["Toy_ink"])
    wall_box(f"{tag}_mullh", edge, s0 + 0.16, s1 - 0.16, zm - 0.07, zm + 0.07,
             0.10, 0.16, mats["Toy_ink"])
    if lit:
        wall_box(f"{tag}_lit", edge, s0 + 0.20, s1 - 0.20, z0 + 0.18, z1 - 0.18,
                 0.12, 0.15, mats["Toy_glassl_Glow"])


# One bay in four lights up at night, scattered so no floor reads as a band.
LIT_THIRD = {(0, 2), (1, 6), (1, 7), (2, 1), (2, 4), (3, 3), (3, 8)}
LIT_BRYANT = {(0, 5), (1, 1), (2, 3), (2, 6), (3, 0)}
LIT_SE = {(0, 4), (1, 2), (3, 5)}


def glazed_elevation(tag, edge, nbays, mats, lit):
    spans, _ = bay_spans(edge, nbays)
    _, _, length, _, _ = poly_edge(edge)
    pilasters(tag, edge, nbays, mats, H_BELT1, H_ROOF)
    for fi, base in enumerate(FLOORS):
        z0, z1 = base + WIN_LO, base + WIN_HI
        # continuous sill band under each window band: the horizontal counterpart
        # to the pilaster rhythm, and what keeps the grid from reading as dots
        wall_box(f"{tag}_sill{fi}", edge, 0.0, length, z0 - 0.30, z0 - 0.12,
                 -0.05, 0.14, mats["Toy_trim"])
        for bi, (s0, s1) in enumerate(spans):
            window_unit(f"{tag}_w{fi}_{bi}", edge, s0 + 0.30, s1 - 0.30, z0, z1,
                        mats, lit=(fi, bi) in lit)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    mats = materials()

    stone = mats["Toy_stone"]
    trim = mats["Toy_trim"]
    sand = mats["Toy_sand"]
    white = mats["Toy_white"]
    ink = mats["Toy_ink"]
    glass = mats["Toy_glass"]
    glassl = mats["Toy_glassl"]
    steel = mats["Toy_steel"]
    roofd = mats["Toy_roofd"]

    # ---- 1. body + roof field -------------------------------------------- #
    bevel(prism("body", FOOTPRINT, 0.0, H_ROOF, stone, mat_caps=sand), width=0.14)

    # ---- 2. ground floor -------------------------------------------------- #
    # A charcoal storefront band on the three public elevations only; Ritch
    # Street keeps the bare concrete plinth it really has.
    for tag, edge, nbays in (("third", E_THIRD, BAYS_THIRD),
                             ("bryant", E_BRYANT, BAYS_BRYANT),
                             ("se", E_SE, BAYS_SE)):
        _, _, length, _, _ = poly_edge(edge)
        bevel(wall_box(f"gf_{tag}", edge, 0.0, length, H_PLINTH, H_GF, -0.10, 0.06, ink),
              width=0.06)
        spans, _ = bay_spans(edge, nbays)
        for bi, (s0, s1) in enumerate(spans):
            wall_box(f"gf_{tag}_g{bi}", edge, s0 + 0.35, s1 - 0.35, H_PLINTH + 0.55,
                     H_GF - 0.55, 0.05, 0.11, glass)

    # belt cornice over the ground floor, all the way round
    bevel(ring_band("belt", H_BELT0, H_BELT1, -0.20, 0.25, trim), width=0.06)

    # main entry on 3rd Street, in the middle bay
    spans_third, _ = bay_spans(E_THIRD, BAYS_THIRD)
    es0, es1 = spans_third[BAYS_THIRD // 2]
    ec = (es0 + es1) / 2
    bevel(wall_box("entry_head", E_THIRD, ec - 2.6, ec + 2.6, H_GF - 1.35, H_GF - 0.15,
                   0.06, 0.30, ink), width=0.06)
    wall_box("entry_door", E_THIRD, ec - 1.5, ec + 1.5, 0.0, H_GF - 1.75, 0.06, 0.12, ink)
    wall_box("entry_transom", E_THIRD, ec - 1.5, ec + 1.5, H_GF - 1.70, H_GF - 1.40,
             0.07, 0.13, glassl)
    wall_box("entry_transom_glow", E_THIRD, ec - 1.4, ec + 1.4, H_GF - 1.66, H_GF - 1.44,
             0.13, 0.16, mats["Toy_glassl_Glow"])
    for obj in facade_text("num500", E_THIRD, "500", ec - 1.85, H_GF - 1.18, 0.85, 0.14,
                           trim, gap=0.30, d0=0.30):
        pass
    # two lit lobby bays flanking the entry (the only ground-level night cue)
    for bi in (BAYS_THIRD // 2 - 1, BAYS_THIRD // 2 + 1):
        s0, s1 = spans_third[bi]
        wall_box(f"gf_lit{bi}", E_THIRD, s0 + 0.45, s1 - 0.45, H_PLINTH + 0.70,
                 H_GF - 0.70, 0.12, 0.15, mats["Toy_glassl_Glow"])

    # ---- 3. the three glazed elevations ----------------------------------- #
    glazed_elevation("third", E_THIRD, BAYS_THIRD, mats, LIT_THIRD)
    glazed_elevation("bryant", E_BRYANT, BAYS_BRYANT, mats, LIT_BRYANT)
    glazed_elevation("se", E_SE, BAYS_SE, mats, LIT_SE)

    # ---- 4. Ritch Street service rear ------------------------------------- #
    _, _, l_ritch, _, _ = poly_edge(E_RITCH)
    for k, s in enumerate((16.0, 34.0)):
        bevel(wall_box(f"ritch_roll{k}", E_RITCH, s, s + 4.0, 0.0, 4.2, -0.02, 0.10, ink),
              width=0.05)
    wall_box("ritch_door", E_RITCH, 24.5, 25.7, 0.0, 2.4, -0.02, 0.10, ink)
    bevel(wall_box("ritch_louvre", E_RITCH, 44.0, 47.0, 1.6, 4.0, -0.02, 0.12, roofd),
          width=0.05)
    for fi, base in enumerate(FLOORS):
        for k, s in enumerate((10.0, 21.0, 30.0, 41.0, 50.0)):
            wall_box(f"ritch_w{fi}_{k}", E_RITCH, s, s + 1.25, base + 1.30, base + 2.55,
                     0.0, 0.10, glass)
    # the rear keeps the belt and pilaster-free wall, but not a blank top: one
    # shallow strip marks the floor line so the mass does not read as a slab
    for base in FLOORS[1:]:
        wall_box("ritch_line", E_RITCH, 1.0, l_ritch - 1.0, base - 0.12, base + 0.06,
                 0.0, 0.09, trim)

    # ---- 5. parapet, corner crown, flag masts ----------------------------- #
    bevel(ring_band("parapet", H_ROOF, H_PAR, -0.30, 0.0, stone), width=0.06)
    bevel(ring_band("parapet_cap", H_PAR, H_PAR_CAP, -0.38, 0.10, trim), width=0.05)

    _, _, l_third, _, _ = poly_edge(E_THIRD)
    _, _, l_bryant, _, _ = poly_edge(E_BRYANT)
    # the crown wraps the north corner: 13 m of the 3rd Street parapet (which
    # ends at the north corner) and 11 m of the Bryant parapet (which starts
    # there)
    crown = (
        ("third", E_THIRD, l_third - 13.0, l_third),
        ("bryant", E_BRYANT, 0.0, 11.0),
    )
    for tag, edge, s0, s1 in crown:
        bevel(wall_box(f"crown_{tag}", edge, s0, s1, H_PAR_CAP, H_CROWN, -0.30, 0.10,
                       stone), width=0.06)
        bevel(wall_box(f"crown_{tag}_cap", edge, s0 - 0.10, s1 + 0.10, H_CROWN,
                       H_CROWN_CAP, -0.38, 0.20, ink), width=0.05)
        wall_box(f"crown_{tag}_sign", edge, s0 + 1.1, s1 - 1.1, H_CROWN - 1.35,
                 H_CROWN - 0.20, 0.10, 0.24, mats["Toy_white_Glow"])

    for k in range(5):
        s = 6.0 + k * 8.2
        bevel(wall_box(f"mast_third{k}", E_THIRD, s, s + 0.18, H_PAR_CAP, H_MAST,
                       -0.34, -0.16, steel), width=0.03)
        wall_box(f"flag_third{k}", E_THIRD, s + 0.18, s + 1.35, H_MAST - 1.05,
                 H_MAST - 0.30, -0.28, -0.22,
                 mats["Toy_red"] if k % 2 == 0 else mats["Toy_navy"])
    for k in range(3):
        s = 18.0 + k * 8.2
        bevel(wall_box(f"mast_bryant{k}", E_BRYANT, s, s + 0.18, H_PAR_CAP, H_MAST,
                       -0.34, -0.16, steel), width=0.03)
        wall_box(f"flag_bryant{k}", E_BRYANT, s + 0.18, s + 1.35, H_MAST - 1.05,
                 H_MAST - 0.30, -0.28, -0.22,
                 mats["Toy_navy"] if k % 2 == 0 else mats["Toy_red"])

    # ---- 6. roof --------------------------------------------------------- #
    # bulkhead north-east of centre (the stair/elevator head), plant to the
    # south — the asymmetry is what makes the roof read as a working roof
    bevel(ring_band("gravel_stop", H_ROOF, H_ROOF + 0.10, -2.20, -0.32, trim), width=0.04)

    bevel(uv_box("bulkhead", 2.0, 3.0, H_ROOF, H_BULK, 16.0, 11.0, white), width=0.12)
    bevel(uv_box("bulkhead_cap", 2.0, 3.0, H_BULK, H_CREST, 16.3, 11.3, steel), width=0.06)
    bevel(uv_box("elev", -10.5, 4.0, H_ROOF, H_ELEV, 5.2, 4.6, white), width=0.10)

    # walkway from the bulkhead door down the middle of the plant field
    uv_box("walk_a", 2.0, -6.0, H_ROOF, H_ROOF + 0.06, 3.0, 9.0, trim)
    uv_box("walk_b", -6.0, -10.0, H_ROOF, H_ROOF + 0.06, 19.0, 2.4, trim)
    for i, (u, v) in enumerate(((-20.0, 12.0), (20.0, -14.0), (-22.0, -16.0))):
        bevel(uv_box(f"hatch{i}", u, v, H_ROOF, H_ROOF + 0.55, 2.0, 1.6, roofd), width=0.06)
    for i, (u, v) in enumerate(((-24.0, 6.0), (16.0, 14.0), (24.0, 4.0), (-14.0, 17.0))):
        bevel(uv_box(f"vent{i}", u, v, H_ROOF, H_ROOF + 0.85, 0.7, 0.7, roofd), width=0.05)

    for i in range(5):
        bevel(uv_box(f"mech_a{i}", -16.0 + i * 8.0, -6.5, H_ROOF, H_ROOF + 1.10,
                     1.7, 1.2, roofd), width=0.07)
    for i in range(5):
        bevel(uv_box(f"mech_b{i}", -16.0 + i * 8.0, -13.5, H_ROOF, H_ROOF + 1.10,
                     1.7, 1.2, roofd), width=0.07)
    for i, u in enumerate((-11.0, 5.0)):
        bevel(uv_box(f"duct{i}", u, -17.5, H_ROOF, H_ROOF + 0.60, 6.0, 0.8, roofd),
              width=0.05)
    bevel(uv_box("antenna", 22.0, -8.0, H_ROOF, H_ROOF + 3.0, 0.22, 0.22, steel),
          width=0.04)
    bevel(uv_box("cabinet", 20.2, -8.0, H_ROOF, H_ROOF + 1.30, 1.6, 1.1, roofd),
          width=0.07)

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
    print("[build] anchor lon/lat: -122.3958224 37.7808279 (footprint AABB centre)")
    print("[build] 3rd Street front normal 44.9 deg true; Bryant front normal 314.0 deg")
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

    blend = os.path.join(out, "500-third.blend")
    glb = os.path.join(out, "500-third.glb")
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
