"""Deterministic Blender build of the SF-SIM miniature 599 Third Street.

    blender -b --python build_599_third.py -- [--out DIR]

Writes 599-third.blend and 599-third.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint AABB centre (anchor lon -122.3942739,
lat 37.7804504), min Z = 0, penthouse top exactly 18.30 m.

Design (see REFERENCE.md for the sources behind every number):

* the true OSM polygon (way/124890326, block 3775 map lot 140) extruded as a
  four-storey buff stucco block holding the north corner of 3rd and Brannan —
  a corner wall, not a tower;
* TWO designed street elevations: 3rd Street (SW, 24.0 m, the address face) with
  a centred dark entry recess carrying the 599 numerals and a steel chevron
  brace, and Brannan Street (SE, 36.5 m) as six bays of pure rhythm;
* the ground-floor cafe is on 3rd Street at the north-west end, NOT at the
  corner — measured from the OSM node, see REPORT.md correction 1;
* the north-west face is NOT a party wall: it looks across an open Shell station
  forecourt, so it is articulated rather than blind (REPORT.md correction 2);
* the roof is a working landscape, not a designed terrace: per-loft skylights and
  condenser boxes on a loose grid, three private deck pads, and the stair /
  elevator penthouse that is the true crest at 18.30 m;
* night state is a SCATTER, not a display: about a third of the loft windows lit
  in an irregular pattern, the roof skylights glowing from the lofts below, and
  two ground-level cues at the entry and the cafe. Glow surfaces are thin shells
  proud of opaque glazing — the app renders _Glow in a separate layer at ~12%
  alpha by day, so a primary surface must never be authored as glow. Glow COLOUR
  must be light: the app draws that layer unlit at the material's own baked
  colour, so a dark navy glow would make a lit window read darker than an unlit
  one. Lit lofts are warm Toy_mustard_Glow, skylights cool Toy_glassl_Glow.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/124890326 projected with the app's tangent projection (LON0 -122.4375,
# LAT0 37.77) and recentred on the footprint AABB centre. CCW, (x east, y north).
# A true rectangle: 36.51 x 24.01 m, every vertex 21.78-21.92 m from the anchor.
FOOTPRINT = [
    (-4.435, -21.323),   # v0  south corner  (3rd / Brannan) — the hero corner
    (21.471, 4.411),     # v1  east corner   (Brannan / NE)
    (4.426, 21.323),     # v2  north corner  (NE / NW)
    (-21.471, -4.411),   # v3  west corner   (NW / 3rd)
]
E_BRANNAN = (0, 1)  # SE front, 36.51 m, outward normal 135.2 deg true
E_NE = (1, 2)  # NE interior face, 24.01 m, normal 44.8 deg (toward 380 Brannan)
E_NW = (2, 3)  # NW face, 36.51 m, normal 315.2 deg (toward the Shell forecourt)
E_THIRD = (3, 0)  # SW front, 24.01 m, outward normal 224.8 deg true

L_BRANNAN = 36.51
L_THIRD = 24.01

H_ROOF_STRUCT = 15.60  # top of the wall shell / underside of the parapet
H_ROOF = 15.70  # roof membrane surface
H_PAR = 15.86  # parapet below its coping (0.14 m of coping above it:
# a 0.10 m band cannot carry a 0.05 m bevel on both faces without clamping to
# zero-area geometry, which the validator's degenerate gate rejects)
H_PAR_CAP = 16.00  # parapet coping top — the main architectural height
H_CREST = 18.30  # stair/elevator penthouse top = the target height

# Four storeys: a taller ground floor under three loft levels.
FLOORS = (0.00, 4.20, 8.00, 11.80)
# (z0, z1) window band per storey, ground floor deeper than the lofts.
BANDS = ((0.90, 3.60), (5.10, 7.50), (8.90, 11.30), (12.70, 15.10))

BEVEL_W = 0.10
BEVEL_SEG = 2

PALETTE_HEX = {
    "Toy_sand": "ece4d4",
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_ink": "3a3530",
    "Toy_steel": "9aa0a6",
    "Toy_stone": "d9d2c2",
    "Toy_roofd": "45454a",
    "Toy_coral": "e8735a",
    "Toy_mustard_Glow": "d9a441",
    "Toy_glassl_Glow": "6f95b8",
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


# The building's own axes: U runs the long way along Brannan (from the 3rd/Brannan
# corner toward the east corner), W across it toward 3rd Street's far end. Every
# roof object is laid out in this frame so the composition follows the building
# rather than true north. u spans +-18.25, w spans +-12.00.
def _axes():
    _, _, _, t_brannan, _ = poly_edge(E_BRANNAN)
    _, _, _, t_third, _ = poly_edge(E_THIRD)
    return t_brannan, (-t_third[0], -t_third[1])


U, W = _axes()


def uw(u, w):
    return (U[0] * u + W[0] * w, U[1] * u + W[1] * w)


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
    """Miniature-style edge softening on the chunky solids (style bible s.4)."""
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
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
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


def facade_prism(name, edge, sz, d0, d1, mat):
    """Solid whose profile is an arbitrary polygon in the facade's (s, z) plane,
    extruded along the outward normal from d0 to d1. This is what lets the
    chevron brace be two clean angled members instead of a stair of boxes."""
    a, _, _, t, n = poly_edge(edge)

    def p(s, d):
        return (a[0] + t[0] * s + n[0] * d, a[1] + t[1] * s + n[1] * d)

    m = len(sz)
    verts = [(*p(s, d0), z) for s, z in sz] + [(*p(s, d1), z) for s, z in sz]
    faces = []
    for i in range(m):
        j = (i + 1) % m
        faces.append((i, j, m + j, m + i))
    faces.append(tuple(range(m - 1, -1, -1)))
    faces.append(tuple(range(m, 2 * m)))
    return new_mesh(name, verts, faces, [mat])


def uw_box(name, u, w, z0, z1, su, sw, mat):
    """Box centred at (u, w) in the building frame, su along U, sw along W."""
    corners = []
    for du, dw in ((-su / 2, -sw / 2), (su / 2, -sw / 2), (su / 2, sw / 2), (-su / 2, sw / 2)):
        corners.append(uw(u + du, w + dw))
    return quad_box(name, corners, z0, z1, mat)


# ------------------------------------------------------------------- glyphs

# Stroke rectangles in a 1x1 glyph cell, (x0, y0, x1, y1), origin bottom-left.
GLYPHS = {
    "5": [(0.0, 0.82, 1.0, 1.0), (0.0, 0.44, 0.22, 0.86), (0.0, 0.42, 0.85, 0.6),
          (0.78, 0.1, 1.0, 0.52), (0.0, 0.0, 0.9, 0.18)],
    "9": [(0.0, 0.82, 1.0, 1.0), (0.0, 0.48, 0.22, 0.9), (0.78, 0.0, 1.0, 0.9),
          (0.0, 0.44, 0.9, 0.62), (0.0, 0.0, 0.85, 0.18)],
}


def facade_text(name, edge, text, s_start, z_base, size, depth, mat, gap=0.24):
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
            quad = [
                corners[0],
                corners[1],
                (corners[1][0] + n[0] * depth, corners[1][1] + n[1] * depth),
                (corners[0][0] + n[0] * depth, corners[0][1] + n[1] * depth),
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


def loft_window(tag, edge, s0, s1, z0, z1, mats, cols=3, rows=2, lit=False):
    """The building's signature unit: a white-framed multi-pane industrial grid
    sitting almost flush in buff stucco. Built PROUD of the wall — the shell is a
    solid prism with no cut openings, so anything at negative depth is buried
    inside it and invisible. The apparent recess comes from the pilasters
    standing 0.18 m out in front (style bible s.5: windows are graphical elements
    before they are literal openings)."""
    wall_box(f"{tag}_frame", edge, s0, s1, z0, z1, 0.0, 0.08, mats["Toy_trim"])
    wall_box(f"{tag}_glass", edge, s0 + 0.14, s1 - 0.14, z0 + 0.14, z1 - 0.14,
             0.05, 0.12, mats["Toy_glass"])
    span, rise = s1 - s0, z1 - z0
    for c in range(1, cols):
        s = s0 + span * c / cols
        wall_box(f"{tag}_mv{c}", edge, s - 0.05, s + 0.05, z0 + 0.14, z1 - 0.14,
                 0.10, 0.15, mats["Toy_trim"])
    for r in range(1, rows):
        z = z0 + rise * r / rows
        wall_box(f"{tag}_mh{r}", edge, s0 + 0.14, s1 - 0.14, z - 0.05, z + 0.05,
                 0.10, 0.15, mats["Toy_trim"])
    if lit:
        # thin shell lifted clear of the pane: coincident faces z-fight, and at
        # 12% day alpha that reads as a triangulated smear.
        wall_box(f"{tag}_glow", edge, s0 + 0.18, s1 - 0.18, z0 + 0.18, z1 - 0.18,
                 0.125, 0.145, mats["Toy_mustard_Glow"])


def punched(tag, edge, s, z, mats, size=0.85):
    """Small square opening for the two interior faces."""
    wall_box(f"{tag}_reveal", edge, s, s + size, z, z + size, 0.0, 0.05, mats["Toy_ink"])
    wall_box(f"{tag}_glass", edge, s + 0.12, s + size - 0.12, z + 0.12, z + size - 0.12,
             0.04, 0.10, mats["Toy_glass"])


# Which loft windows are lit at night. Irregular on purpose: an even grid reads
# as an office block and destroys the one thing that says "people live here".
LIT_THIRD = {("A", 1, 0), ("A", 3, 1), ("B", 1, 1), ("B", 2, 0), ("B", 3, 0)}
LIT_BRANNAN = {(0, 2), (1, 1), (1, 3), (2, 1), (3, 2), (3, 3), (4, 1), (5, 2), (5, 3)}


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    mats = materials()

    sand = mats["Toy_sand"]
    trim = mats["Toy_trim"]
    glass = mats["Toy_glass"]
    glassl = mats["Toy_glassl"]
    ink = mats["Toy_ink"]
    steel = mats["Toy_steel"]
    stone = mats["Toy_stone"]
    roofd = mats["Toy_roofd"]
    coral = mats["Toy_coral"]

    # ---- 1. body + roof field -------------------------------------------- #
    bevel(prism("body", FOOTPRINT, 0.0, H_ROOF_STRUCT, sand, mat_caps=sand), width=0.14)
    prism("roof_field", offset_polygon(FOOTPRINT, -0.30), H_ROOF_STRUCT, H_ROOF, stone)

    # ---- 2. parapet ------------------------------------------------------- #
    bevel(ring_band("parapet", H_ROOF_STRUCT, H_PAR, -0.30, 0.0, sand), width=0.06)
    bevel(ring_band("parapet_cap", H_PAR, H_PAR_CAP, -0.38, 0.08, ink), width=0.04)

    # ---- 3. 3rd Street elevation (SW) ------------------------------------- #
    # s runs from v3 (west corner, beside the Shell forecourt) to v0 (the
    # 3rd/Brannan hero corner). Two window bays flanking a centred entry recess.
    for tag, (s0, s1) in (("t_pil0", (0.00, 0.90)), ("t_pil1", (8.20, 9.10)),
                          ("t_pil2", (14.90, 15.80)), ("t_pil3", (23.10, L_THIRD))):
        bevel(wall_box(tag, E_THIRD, s0, s1, 0.0, H_ROOF_STRUCT, -0.05, 0.18, sand),
              width=0.05)
    for bay, base in (("A", 0.90), ("B", 15.80)):
        for k, (w0, w1) in enumerate(((base + 0.40, base + 3.55),
                                      (base + 3.75, base + 6.90))):
            for lvl, (z0, z1) in enumerate(BANDS):
                if bay == "A" and lvl == 0:
                    continue  # the cafe occupies bay A's ground floor
                loft_window(f"t_{bay}{k}_{lvl}", E_THIRD, w0, w1, z0, z1, mats,
                            lit=(bay, k, lvl) in LIT_THIRD)

    # cafe: the 2017 garage conversion, on 3rd Street at the north-west end
    # (measured from the OSM node, not at the corner — see REPORT.md)
    wall_box("cafe_reveal", E_THIRD, 1.20, 7.60, 0.0, 3.70, 0.0, 0.04, ink)
    wall_box("cafe_glass", E_THIRD, 1.45, 7.35, 0.20, 3.35, 0.03, 0.10, glass)
    wall_box("cafe_glow", E_THIRD, 1.60, 7.20, 0.35, 3.20, 0.105, 0.125,
             mats["Toy_trim_Glow"])
    for i, s in enumerate((3.05, 4.65, 6.25)):
        wall_box(f"cafe_mull{i}", E_THIRD, s - 0.05, s + 0.05, 0.20, 3.35, 0.09, 0.14, ink)
    bevel(wall_box("cafe_awning", E_THIRD, 1.10, 7.70, 3.60, 3.86, 0.10, 1.05, coral),
          width=0.06)

    # entry recess: a dark plate between the pilasters reads as the recess, with
    # the doors, numerals and chevron stepped out in front of it. Unbevelled —
    # a 4 cm plate cannot carry a bevel without clamping to zero-area faces
    # (the validator's degenerate-geometry gate catches this).
    wall_box("entry_reveal", E_THIRD, 9.10, 14.90, 0.0, 14.60, 0.0, 0.04, ink)
    wall_box("entry_door", E_THIRD, 10.70, 13.30, 0.0, 3.00, 0.03, 0.10, glass)
    wall_box("entry_door_glow", E_THIRD, 10.85, 13.15, 0.15, 2.85, 0.105, 0.125,
             mats["Toy_trim_Glow"])
    bevel(wall_box("entry_jamb_l", E_THIRD, 10.55, 10.75, 0.0, 3.20, 0.03, 0.16, ink),
          width=0.03)
    bevel(wall_box("entry_jamb_r", E_THIRD, 13.25, 13.45, 0.0, 3.20, 0.03, 0.16, ink),
          width=0.03)
    bevel(wall_box("entry_lintel", E_THIRD, 10.40, 13.60, 3.20, 3.50, 0.03, 0.18, steel),
          width=0.05)
    # oversized 599 above the doors (style bible s.8). Unbevelled on purpose:
    # the thinnest stroke is 0.16 m, so any bevel wide enough to catch light
    # clamps into degenerate faces, and at this size it would never read.
    facade_text("num", E_THIRD, "599", 10.20, 4.20, 0.95, 0.12, mats["Toy_trim"], gap=0.30)
    # the stack of small square punched windows up the recess centreline
    for i, z in enumerate((6.20, 8.00, 9.80, 11.60)):
        wall_box(f"entry_sq{i}", E_THIRD, 11.65, 12.35, z, z + 0.70, 0.03, 0.10, glass)
    # the steel chevron brace — the one piece of structural drama on the building.
    # Two clean angled members, deliberately over-thickened (style bible s.9): the
    # real section would vanish at city distance, and a stepped approximation
    # reads as noise rather than structure.
    apex_s, apex_z = 12.00, 14.30
    foot_z, half = 11.90, 0.26
    for i, s_foot in enumerate((9.35, 14.65)):
        # arms cross slightly past the centreline so the apex closes; two solids
        # overlapping is fine (the asset is a union of closed solids), a 0.3 m
        # gap at the apex is not — it reads as two loose sticks.
        s_apex = apex_s + (-0.12 if i else 0.12)
        facade_prism(
            f"chevron_{i}",
            E_THIRD,
            [(s_foot, foot_z - half), (s_apex, apex_z - half),
             (s_apex, apex_z + half), (s_foot, foot_z + half)],
            0.05,
            0.36,
            steel,
        )

    # ---- 4. Brannan Street elevation (SE) --------------------------------- #
    # Six bays of one wide window unit each, four storeys, no interruption.
    pil_w, bay_w = 0.80, (L_BRANNAN - 7 * 0.80) / 6.0
    for k in range(7):
        s0 = k * (bay_w + pil_w)
        bevel(wall_box(f"b_pil{k}", E_BRANNAN, s0, s0 + pil_w, 0.0, H_ROOF_STRUCT,
                       -0.05, 0.18, sand), width=0.05)
    for k in range(6):
        s0 = pil_w + k * (bay_w + pil_w)
        for lvl, (z0, z1) in enumerate(BANDS):
            loft_window(f"b_{k}_{lvl}", E_BRANNAN, s0 + 0.35, s0 + bay_w - 0.35, z0, z1,
                        mats, cols=4, lit=(k, lvl) in LIT_BRANNAN)

    # ---- 5. the two interior faces ---------------------------------------- #
    # NW is NOT a party wall: it faces the open Shell station forecourt, so it
    # gets a real (if reduced) rhythm. NE looks over 380 Brannan's 12.6 m roof.
    for i in range(6):
        s = 3.4 + i * 5.4
        for lvl, z in enumerate((5.30, 9.10, 12.90)):
            punched(f"nw_{i}_{lvl}", E_NW, s, z, mats)
    for i in range(4):
        s = 3.0 + i * 5.4
        for lvl, z in enumerate((9.10, 12.90)):
            punched(f"ne_{i}_{lvl}", E_NE, s, z, mats)

    # ---- 6. the working roof ---------------------------------------------- #
    # Skylight + condenser clusters on a loose two-across grid down the long
    # axis: roughly one per loft, read as "many" rather than counted.
    sky_u = (-14.6, -11.0, -7.4, -3.8, -0.2, 3.4, 7.0, 10.6, 14.2)
    for i, u in enumerate(sky_u):
        w = -5.6 if i % 2 == 0 else 4.4
        bevel(uw_box(f"sky_{i}_frame", u, w, H_ROOF, H_ROOF + 0.26, 1.6, 1.2, trim),
              width=0.05)
        uw_box(f"sky_{i}_pane", u, w, H_ROOF + 0.22, H_ROOF + 0.36, 1.25, 0.9, glassl)
        uw_box(f"sky_{i}_glow", u, w, H_ROOF + 0.375, H_ROOF + 0.405, 1.1, 0.8,
               mats["Toy_glassl_Glow"])
        bevel(uw_box(f"cond_{i}", u + 1.9, w + (1.6 if i % 2 == 0 else -1.6),
                     H_ROOF, H_ROOF + 0.62, 0.95, 0.75, roofd), width=0.06)
    for i, (u, w) in enumerate(((-16.2, 1.0), (-2.0, 8.6), (12.0, -8.8))):
        bevel(uw_box(f"cond_x{i}", u, w, H_ROOF, H_ROOF + 0.62, 0.95, 0.75, roofd),
              width=0.06)
    # private deck pads — the 2002 as-built roof open space
    for i, (u, w) in enumerate(((-12.6, 8.4), (1.6, -9.0), (15.2, 6.2))):
        bevel(uw_box(f"deck_{i}", u, w, H_ROOF, H_ROOF + 0.16, 4.2, 3.2, sand), width=0.04)
    # stair / elevator penthouse: the crest, and the only vertical event up here
    bevel(uw_box("penthouse", 6.4, 0.6, H_ROOF, H_CREST, 7.6, 5.2, trim), width=0.10)
    # coping as four thin bars around the top edge, NOT a lid: a full-plan cap
    # box reads from above as a black hole punched in the roof.
    for i, (du, dw, su, sw) in enumerate(((0, -2.68, 8.06, 0.30), (0, 2.68, 8.06, 0.30),
                                          (-3.88, 0, 0.30, 5.36), (3.88, 0, 0.30, 5.36))):
        bevel(uw_box(f"penthouse_cope{i}", 6.4 + du, 0.6 + dw, H_CREST - 0.20, H_CREST,
                     su, sw, ink), width=0.05)
    for i, (du, dw, su, sw) in enumerate(((0, -2.6, 3.4, 0.14), (0, 2.6, 3.4, 0.14),
                                          (-3.8, 0, 0.14, 2.4), (3.8, 0, 0.14, 2.4))):
        uw_box(f"pent_win{i}", 6.4 + du, 0.6 + dw, 16.60, 17.80, su, sw, glassl)

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
        o.evaluated_get(dg).to_mesh_clear()
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print("[build] anchor lon/lat: -122.3942739 37.7804504 (footprint AABB centre)")
    print("[build] long axis 44.8 deg true; 3rd Street front normal 224.8 deg true")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "599-third.blend")
    glb = os.path.join(out, "599-third.glb")
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
