"""Deterministic Blender build of the SF-SIM miniature 550 Third Street.

    blender -b --python build_550_third.py -- [--out DIR]

Writes 550-third.blend and 550-third.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint AABB centre (anchor lon -122.3953409,
lat 37.7804407), min Z = 0, penthouse roof slab top exactly 11.0 m.

Design (see REFERENCE.md for the sources behind every number):

* the true OSM polygon (way/124889472, block 3776 lot 005) extruded as a long
  low painted-masonry bar — a through lot, 3rd Street (NE) to Ritch Street (SW),
  party walls on both long sides;
* the roof IS the facade for this asset (style bible s.10): five big skylights in
  a row, a paver walk dog-legging between them, the glass penthouse pavilion
  under its thin cantilevered slab, a garden deck behind the tall street
  parapet, a sloped stair penthouse, an elevator overrun, and the four heat
  pumps at the Ritch end;
* the 3rd Street elevation: pilaster strips, two big steel-sash window grids,
  a recessed entry, and oversized 550 numerals on the tall parapet;
* the SE party wall's punched property-line windows and the Ritch Street
  roll-up doors, both added by DBI PA 202302061449;
* night state: the penthouse reads as a lantern over a dark bar, the five
  skylights glow from the office below (the aerial identity), one small glow at
  the street entry. Glow surfaces are thin shells proud of opaque glazing — the
  app renders _Glow in a separate layer at ~12% alpha by day, so a primary
  surface must never be authored as glow.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/124889472 projected with the app's tangent projection (LON0 -122.4375,
# LAT0 37.77) and recentred on the footprint AABB centre. CCW, (x east, y north).
FOOTPRINT = [
    (-24.507, -8.943),   # v0  west corner   (Ritch / NW party wall)
    (-9.891, -25.104),   # v1  south corner  (Ritch / SE party wall)
    (7.515, -7.915),     # v2  kink in the SE party wall
    (24.507, 8.932),     # v3  east corner   (3rd St / SE party wall)
    (8.087, 25.104),     # v4  north corner  (3rd St / NW party wall)
]
E_RITCH = (0, 1)  # SW rear, 21.79 m, outward normal 227.8 deg true
E_SE_A = (1, 2)  # SE party wall, 24.46 m, normal 135.4 deg
E_SE_B = (2, 3)  # SE party wall, 23.93 m, normal 135.2 deg
E_THIRD = (3, 4)  # NE front, 23.05 m, outward normal 44.6 deg true
E_NW = (4, 0)  # NW party wall, 47.13 m, normal 313.8 deg

H_ROOF = 7.45  # roof membrane surface (2010 LiDAR median 7.23 + deck build-up)
H_PAR = 8.08  # side and rear parapet, below its coping
H_PAR_CAP = 8.20  # side and rear parapet coping top
H_PAR_F = 8.88  # 3rd Street parapet, below its coping (it screens the deck)
H_PAR_F_CAP = 9.00  # 3rd Street parapet coping top
H_PENT0 = 7.45  # penthouse glazing springs off the deck
H_PENT1 = 10.45  # penthouse glazing head / underside of the slab
H_CREST = 11.00  # penthouse roof slab top = the architectural height
H_ELEV = 10.65  # elevator overrun, deliberately below the crest
H_STAIR0, H_STAIR1 = 9.20, 10.40  # stair penthouse mono-pitch, low to high

FLOOR1 = (1.30, 3.60)  # ground-floor window band
FLOOR2 = (4.30, 6.60)  # upper-floor window band

BEVEL_W = 0.10
BEVEL_SEG = 2

PALETTE_HEX = {
    "Toy_white": "f7f4ec",
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_ink": "3a3530",
    "Toy_steel": "9aa0a6",
    "Toy_roofd": "45454a",
    "Toy_mint": "8fd0a8",
    "Toy_teal": "3fa8a0",
    "Toy_brick": "c96f4a",
    "Toy_glassl_Glow": "6f95b8",
    "Toy_white_Glow": "f7f4ec",
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


# The building's own axes: U runs the long way toward 3rd Street, W across it
# toward the SE party wall. Every roof object is laid out in this frame so the
# composition follows the building rather than true north.
def _axes():
    _, _, _, t_third, _ = poly_edge(E_THIRD)
    _, _, _, t_se, _ = poly_edge(E_SE_B)
    ux, uy = t_se  # SE wall runs from Ritch toward 3rd Street
    return (ux, uy), (-t_third[0], -t_third[1])


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


def uw_box(name, u, w, z0, z1, su, sw, mat):
    """Box centred at (u, w) in the building frame, su along U, sw along W."""
    corners = []
    for du, dw in ((-su / 2, -sw / 2), (su / 2, -sw / 2), (su / 2, sw / 2), (-su / 2, sw / 2)):
        corners.append(uw(u + du, w + dw))
    return quad_box(name, corners, z0, z1, mat)


def uw_wedge(name, u, w, su, sw, z_lo, z_hi, mat):
    """Mono-pitch solid: low edge at -su/2, high edge at +su/2."""
    c = [uw(u + du, w + dw) for du, dw in
         ((-su / 2, -sw / 2), (su / 2, -sw / 2), (su / 2, sw / 2), (-su / 2, sw / 2))]
    verts = [(x, y, 0.0) for x, y in c]
    verts = [(c[i][0], c[i][1], H_ROOF) for i in range(4)]
    tops = [z_lo, z_hi, z_hi, z_lo]
    verts += [(c[i][0], c[i][1], tops[i]) for i in range(4)]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


# ------------------------------------------------------------------- glyphs

# Stroke rectangles in a 1x1 glyph cell, (x0, y0, x1, y1), origin bottom-left.
GLYPHS = {
    "5": [(0.0, 0.82, 1.0, 1.0), (0.0, 0.44, 0.22, 0.86), (0.0, 0.42, 0.85, 0.6),
          (0.78, 0.1, 1.0, 0.52), (0.0, 0.0, 0.9, 0.18)],
    "0": [(0.0, 0.0, 1.0, 0.18), (0.0, 0.82, 1.0, 1.0),
          (0.0, 0.1, 0.22, 0.92), (0.78, 0.1, 1.0, 0.92)],
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


def window_grid(tag, edge, s0, s1, z0, z1, mats, cols=4, rows=2):
    """Steel-sash bay applied to the facade plane: ink backing plate, one glass
    slab, mullion grid. Everything is built PROUD of the wall — the walls are
    solid prisms with no cut openings, so anything at negative depth is buried
    inside the shell and invisible. The apparent recess comes from the pilasters
    standing 0.20 m out in front of this assembly (style bible s.5: windows are
    graphical elements before they are literal openings)."""
    wall_box(f"{tag}_reveal", edge, s0, s1, z0, z1, 0.0, 0.04, mats["Toy_ink"])
    wall_box(f"{tag}_glass", edge, s0 + 0.10, s1 - 0.10, z0 + 0.10, z1 - 0.10,
             0.03, 0.11, mats["Toy_glass"])
    span = s1 - s0
    for c in range(1, cols):
        s = s0 + span * c / cols
        wall_box(f"{tag}_mull_v{c}", edge, s - 0.055, s + 0.055, z0 + 0.10, z1 - 0.10,
                 0.09, 0.15, mats["Toy_ink"])
    for r in range(1, rows):
        z = z0 + (z1 - z0) * r / rows
        wall_box(f"{tag}_mull_h{r}", edge, s0 + 0.10, s1 - 0.10, z - 0.06, z + 0.06,
                 0.09, 0.15, mats["Toy_ink"])


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    mats = materials()

    white = mats["Toy_white"]
    stone = mats["Toy_stone"]
    trim = mats["Toy_trim"]
    glass = mats["Toy_glass"]
    glassl = mats["Toy_glassl"]
    ink = mats["Toy_ink"]
    steel = mats["Toy_steel"]
    roofd = mats["Toy_roofd"]
    mint = mats["Toy_mint"]
    teal = mats["Toy_teal"]
    brick = mats["Toy_brick"]

    # ---- 1. body + roof field ------------------------------------------- #
    bevel(prism("body", FOOTPRINT, 0.0, H_ROOF, white, mat_caps=stone), width=0.12)

    # ---- 2. parapets ----------------------------------------------------- #
    bevel(ring_band("parapet", H_ROOF, H_PAR, -0.35, 0.0, white), width=0.06)
    bevel(ring_band("parapet_cap", H_PAR, H_PAR_CAP, -0.42, 0.07, ink), width=0.05)
    _, _, l_third, _, _ = poly_edge(E_THIRD)
    bevel(wall_box("parapet_front", E_THIRD, 0.0, l_third, H_PAR_CAP, H_PAR_F,
                   -0.35, 0.0, white), width=0.06)
    bevel(wall_box("parapet_front_cap", E_THIRD, -0.07, l_third + 0.07, H_PAR_F,
                   H_PAR_F_CAP, -0.42, 0.07, ink), width=0.05)

    # ---- 3. 3rd Street elevation (s runs from v3 east corner to v4 north) - #
    for tag, (s0, s1) in (("pil_a", (0.0, 1.0)), ("pil_b", (8.2, 9.4)),
                          ("pil_c", (16.6, 18.8)), ("pil_d", (21.6, l_third))):
        bevel(wall_box(tag, E_THIRD, s0, s1, 0.0, H_ROOF, -0.05, 0.20, white), width=0.05)
    for tag, (s0, s1) in (("winA", (1.0, 8.2)), ("winB", (9.4, 16.6))):
        window_grid(f"{tag}_lo", E_THIRD, s0 + 0.35, s1 - 0.35, *FLOOR1, mats)
        window_grid(f"{tag}_hi", E_THIRD, s0 + 0.35, s1 - 0.35, *FLOOR2, mats)
    # entry bay: a dark plate between the pilasters reads as the recess, with the
    # door and transom stepped out in front of it
    # unbevelled: a 3 cm plate cannot carry a bevel without clamping to
    # zero-area faces (the validator's degenerate-geometry gate catches this)
    wall_box("entry_reveal", E_THIRD, 18.8, 21.6, 0.0, 4.30, 0.0, 0.03, ink)
    wall_box("entry_door", E_THIRD, 19.5, 20.9, 0.0, 2.75, 0.02, 0.09, ink)
    wall_box("entry_transom", E_THIRD, 19.2, 21.2, 2.90, 3.90, 0.02, 0.09, glass)
    wall_box("entry_transom_glow", E_THIRD, 19.25, 21.15, 2.95, 3.85, 0.095, 0.13,
             mats["Toy_white_Glow"])
    bevel(wall_box("entry_lintel", E_THIRD, 18.6, 21.8, 4.30, 4.62, 0.0, 0.16, steel),
          width=0.05)
    # oversized 550 on the tall street parapet (style bible s.8). Unbevelled on
    # purpose: the thinnest stroke is 0.10 m, so any bevel wide enough to catch
    # light clamps into degenerate faces, and at this size it would never read.
    facade_text("num", E_THIRD, "550", 9.55, 8.32, 0.56, 0.10, ink, gap=0.22)

    # ---- 4. SE party wall: punched property-line windows ------------------ #
    for edge, tag, count, s_first, step in ((E_SE_A, "pw_a", 4, 4.2, 5.2),
                                            (E_SE_B, "pw_b", 4, 2.6, 5.2)):
        for i in range(count):
            s = s_first + i * step
            wall_box(f"{tag}_{i}_reveal", edge, s, s + 0.95, 5.60, 6.55,
                     0.0, 0.05, ink)
            wall_box(f"{tag}_{i}_glass", edge, s + 0.13, s + 0.82, 5.73, 6.42,
                     0.04, 0.10, glass)

    # ---- 5. Ritch Street rear: garage doors + window band ----------------- #
    _, _, l_ritch, _, _ = poly_edge(E_RITCH)
    for i, s0 in enumerate((2.6, 8.0)):
        bevel(wall_box(f"garage_{i}", E_RITCH, s0, s0 + 3.6, 0.0, 3.40, 0.0, 0.07, ink),
              width=0.02)
        for j in range(1, 4):
            z = 0.85 * j
            wall_box(f"garage_{i}_rib{j}", E_RITCH, s0 + 0.08, s0 + 3.52, z - 0.05,
                     z + 0.05, 0.05, 0.11, steel)
    bevel(wall_box("garage_lintel", E_RITCH, 2.2, 12.0, 3.40, 3.72, 0.0, 0.16, steel),
          width=0.05)
    bevel(wall_box("rear_door", E_RITCH, 13.4, 14.7, 0.0, 2.45, 0.0, 0.07, ink),
          width=0.02)
    window_grid("rear_band", E_RITCH, 2.6, l_ritch - 2.8, 4.40, 5.80, mats, cols=6, rows=1)

    # ---- 6. skylight row: the aerial identity ----------------------------- #
    for i, u in enumerate((2.6, -2.4, -7.4, -12.4, -17.4)):
        bevel(uw_box(f"sky_{i}_frame", u, -1.0, H_ROOF, H_ROOF + 0.36, 3.4, 5.6, steel),
              width=0.07)
        uw_box(f"sky_{i}_pane", u, -1.0, H_ROOF + 0.30, H_ROOF + 0.52, 2.9, 5.1, glassl)
        # the glow shell is inset and lifted clear of the pane: coincident faces
        # z-fight, and at 12% day alpha that reads as a triangulated smear.
        uw_box(f"sky_{i}_glow", u, -1.0, H_ROOF + 0.535, H_ROOF + 0.575, 2.7, 4.9,
               mats["Toy_glassl_Glow"])

    # ---- 7. paver walk: a Z through the roof (segments butt, never overlap) - #
    uw_box("walk_a", 1.15, 5.4, H_ROOF, H_ROOF + 0.06, 13.9, 1.6, steel)
    uw_box("walk_b", -5.0, -0.6, H_ROOF, H_ROOF + 0.06, 1.6, 10.4, steel)
    uw_box("walk_c", -13.0, -6.6, H_ROOF, H_ROOF + 0.06, 17.6, 1.6, steel)

    # ---- 8. roof deck at the 3rd Street end ------------------------------- #
    uw_box("deck_pavers", 16.6, 0.0, H_ROOF, H_ROOF + 0.08, 13.0, 20.0, steel)
    uw_box("deck_lawn", 20.0, 5.6, H_ROOF + 0.06, H_ROOF + 0.14, 4.0, 5.6, mint)
    for i, (u, w, su, sw) in enumerate(((22.5, 0.0, 0.9, 18.0), (19.6, -9.0, 6.4, 0.9),
                                        (19.6, 9.0, 6.4, 0.9))):
        bevel(uw_box(f"planter_{i}", u, w, H_ROOF + 0.06, H_ROOF + 0.42, su, sw, ink),
              width=0.05)
        bevel(uw_box(f"hedge_{i}", u, w, H_ROOF + 0.42, H_ROOF + 1.05, su - 0.12,
                     sw - 0.12, mint), width=0.08)
    for i, (u, w) in enumerate(((19.0, -6.0), (20.8, -6.0), (18.0, -3.2))):
        bevel(uw_box(f"lounge_{i}", u, w, H_ROOF + 0.08, H_ROOF + 0.62, 2.2, 1.1, teal),
              width=0.08)
    bevel(uw_box("firepit", 20.2, -1.4, H_ROOF + 0.08, H_ROOF + 0.58, 1.4, 1.4, brick),
          width=0.06)
    bevel(uw_box("table", 13.0, -6.0, H_ROOF + 0.60, H_ROOF + 0.74, 1.1, 4.6, trim),
          width=0.05)
    for i, w in enumerate((-7.0, -5.0)):
        bevel(uw_box(f"bench_{i}", 13.0, w, H_ROOF + 0.08, H_ROOF + 0.42, 0.45, 4.6, trim),
              width=0.05)

    # ---- 9. penthouse pavilion ------------------------------------------- #
    bevel(uw_box("pent_glass", 13.6, 3.2, H_PENT0, H_PENT1, 6.4, 8.0, glassl), width=0.05)
    uw_box("pent_glow", 13.6, 3.2, H_PENT0 + 0.15, H_PENT1 - 0.10, 6.5, 8.1,
           mats["Toy_glassl_Glow"])
    for i, (du, dw, su, sw) in enumerate(((-3.2, 0, 0.22, 8.0), (3.2, 0, 0.22, 8.0),
                                          (0, -4.0, 6.4, 0.22), (0, 4.0, 6.4, 0.22))):
        uw_box(f"pent_mull_{i}", 13.6 + du, 3.2 + dw, H_PENT0, H_PENT1, su, sw, ink)
    bevel(uw_box("pent_slab", 13.6, 3.2, H_PENT1, H_CREST, 8.2, 9.8, trim), width=0.07)

    # ---- 10. stair penthouse + elevator overrun --------------------------- #
    bevel(uw_wedge("stair_pent", 6.8, -6.2, 4.4, 3.8, H_STAIR0, H_STAIR1, white),
          width=0.07)
    uw_box("stair_skylight", 7.9, -6.2, H_STAIR1 - 0.10, H_STAIR1 + 0.02, 1.0, 2.6, glassl)
    bevel(uw_box("elevator", 6.6, -1.2, H_ROOF, H_ELEV, 2.9, 2.9, white), width=0.07)

    # ---- 11. mechanical cluster at the Ritch end -------------------------- #
    bevel(uw_box("mech_curb", -21.2, -0.8, H_ROOF, H_ROOF + 0.16, 3.2, 15.0, roofd),
          width=0.05)
    for i, w in enumerate((-6.2, -2.5, 1.2, 4.9)):
        bevel(uw_box(f"mech_{i}", -21.2, w, H_ROOF + 0.12, H_ROOF + 1.02, 1.5, 2.3, roofd),
              width=0.08)
    # the ducts stay tight to the plant curb: scattered roof props read as noise
    for i, w in enumerate((-4.7, 3.6)):
        bevel(uw_box(f"duct_{i}", -17.9, w, H_ROOF + 0.06, H_ROOF + 0.52, 4.0, 0.75, roofd),
              width=0.06)

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
    print("[build] anchor lon/lat: -122.3953409 37.7804407 (footprint AABB centre)")
    print("[build] long axis 45.3 deg true; 3rd Street front normal 44.6 deg true")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "550-third.blend")
    glb = os.path.join(out, "550-third.glb")
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
