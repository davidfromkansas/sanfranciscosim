"""Deterministic Blender build of the SF-SIM miniature 131 Steuart Street.

    blender -b --python build_131_steuart.py -- [--out DIR]

Writes 131-steuart.blend and 131-steuart.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint AABB centre (anchor lon -122.3924386,
lat 37.7930568), min Z = 0, penthouse barrel crown top exactly 27.7 m.

Design (see REFERENCE.md for the sources behind every number):

* OSM way/193054132, parcel 3715-025, extruded as one narrow 14.16 x 42.07 m
  through-lot slot running the full block depth from Steuart Street to The
  Embarcadero — a 1907 brick commercial block with TWO public ends and two
  blind party-wall flanks;
* the Steuart Street end (southwest, 224.9 deg) is the 1907 face: a tall
  green-banded storefront, six storeys of five-bay punched brick windows, a
  green string course at 17.4 m and a projecting green cornice topping at
  21.8 m;
* The Embarcadero end (northeast, 44.8 deg) is the 1983 face: pale cast stone
  with rounded corners and five continuous horizontal glazing bands, over a
  white shopfront ground floor;
* the crest, and the only silhouette break on this block, is the set-back
  glazed penthouse under a shallow cream barrel roof crowning at 27.7 m,
  occupying the north-east 10 m of the roof;
* the roof is a working roof: pale membrane, a light-monitor spine down the
  middle, two condenser clusters and a skylight;
* night state: the penthouse lantern is the hero glow, a scatter of lit upper
  bays is the supporting rhythm, the two entrances are the ground cue. Glow
  surfaces are thin shells proud of opaque glazing — the app renders _Glow in a
  separate layer at ~12% alpha by day, so a primary surface must never be
  authored as glow.

Heights are MEASURED, not published: two independent Street View camera solves
(least-squares fits of four known party-line corners, RMS 0.9 px) put the brick
cornice top at 21.8 m from Steuart Street and the same parapet at 21.6 m from
The Embarcadero, and the barrel crown at 27.5 m against a DataSF LiDAR maximum
of 27.77 m. See docs/asset-plans/131-steuart.md section 2.15.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/193054132 projected with the app's tangent projection (LON0 -122.4375,
# LAT0 37.77) and recentred on the footprint AABB centre. CCW, (x east, y north).
FOOTPRINT = [
    (-19.896, -9.954),    # v0  west corner   (Steuart x 121 Steuart)
    (-9.873, -19.958),    # v1  south corner  (Steuart x 141 Steuart)
    (19.896, 9.766),      # v2  east corner   (Embarcadero x 141)
    (9.636, 19.958),      # v3  north corner  (Embarcadero x 121)
]
E_STEUART = (0, 1)  # SW front, 14.16 m, outward normal 224.9 deg true
E_SE = (1, 2)       # SE party wall with 141 Steuart, 42.07 m, normal 135.0 deg
E_EMB = (2, 3)      # NE front, 14.46 m, outward normal 44.8 deg true
E_NW = (3, 0)       # NW party wall with 121 Steuart, 42.03 m, normal 314.6 deg

H_PLINTH = 0.45     # brick plinth under the storefront
H_GF = 5.20         # top of the ground-floor green band (measured)
H_BAND0 = 4.55      # green fascia over the shopfronts
H_STRING0, H_STRING1 = 17.15, 17.60   # green string course (measured 17.6 m)
H_ROOF = 21.40      # roof membrane surface behind the cornice
H_CORN0, H_CORN1 = 20.30, 21.80       # projecting cornice; top = 21.8 m measured
H_PENT = 24.70      # penthouse walls / top of its glazing
H_CREST = 27.70     # barrel crown = the architectural height
PENT_DEPTH = 10.0   # of the 42.07 m depth, measured back from the Embarcadero end
STONE_DEPTH = 8.0   # the 1983 cast-stone re-clad band at the Embarcadero end

# Six window rows, read off the rectified Street View elevation: five at a
# 2.35 m pitch, then a taller top storey above the string course.
ROWS = (5.55, 7.90, 10.25, 12.60, 14.95, 18.25)
WIN_H = 1.45        # rows 1-5
WIN_H_TOP = 1.65    # the taller attic storey
BAYS = 5

BEVEL_W = 0.10
BEVEL_SEG = 2

PALETTE_HEX = {
    "Toy_brick": "c96f4a",
    "Toy_rust": "a86444",
    "Toy_stone": "d9d2c2",
    "Toy_cream": "f2ede3",
    "Toy_sash": "2f4f49",   # the near-black green of the real cornice and
                            # shopfront joinery (precedent artifacts/21-south-park)
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_steel": "9aa0a6",
    "Toy_ink": "3a3530",
    "Toy_glassl_Glow": "6f95b8",
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


def poly_edge(edge, poly=None):
    """(a, b, length, tangent unit, outward normal) for a CCW footprint edge."""
    poly = poly or FOOTPRINT
    a, b = poly[edge[0]], poly[edge[1]]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> this points outward
    return a, b, length, t, n


def offset_polygon(poly, d):
    """Miter offset of a convex ring; positive d moves outward."""
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


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


# Depth-split rings. The parcel is a parallelogram, so cutting at a fraction of
# each long edge gives a clean perpendicular section.
def split_rings(depth_from_emb):
    _, _, l_se, _, _ = poly_edge(E_SE)
    _, _, l_nw, _, _ = poly_edge(E_NW)
    s1 = lerp(FOOTPRINT[1], FOOTPRINT[2], 1.0 - depth_from_emb / l_se)
    s2 = lerp(FOOTPRINT[3], FOOTPRINT[0], depth_from_emb / l_nw)
    near = [FOOTPRINT[0], FOOTPRINT[1], s1, s2]          # Steuart side, CCW
    far = [s1, FOOTPRINT[2], FOOTPRINT[3], s2]           # Embarcadero side, CCW
    return near, far


# The building's own axes: U runs along the long axis toward The Embarcadero,
# V points out toward the 141 Steuart party wall. Every roof object is laid out
# in this frame so the composition follows the block, not true north.
def _axes():
    _, _, _, t_se, n_se = poly_edge(E_SE)
    return t_se, n_se


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
    """Miniature-style edge softening (style bible s.4), width-clamped so thin
    plates cannot collapse into degenerate triangles."""
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
    """Positive signed volume — the validator's authoritative normals test for a
    union of closed solids."""
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


def ring_band(name, z0, z1, off_in, off_out, mat, poly=None):
    poly = poly or FOOTPRINT
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


def wall_box(name, edge, s0, s1, z0, z1, d_in, d_out, mat, poly=None):
    """Box hung on a facade: s along the edge from its first vertex, d measured
    along the outward normal (negative = buried in the wall)."""
    a, _, _, t, n = poly_edge(edge, poly)

    def p(s, d):
        return (a[0] + t[0] * s + n[0] * d, a[1] + t[1] * s + n[1] * d)

    return quad_box(name, [p(s0, d_in), p(s1, d_in), p(s1, d_out), p(s0, d_out)], z0, z1, mat)


def uv_box(name, u, v, z0, z1, su, sv, mat):
    corners = []
    for du, dv in ((-su / 2, -sv / 2), (su / 2, -sv / 2), (su / 2, sv / 2), (-su / 2, sv / 2)):
        corners.append(uv(u + du, v + dv))
    return quad_box(name, corners, z0, z1, mat)


def barrel(name, corners, z0, z_spring, z_crown, mat, segments=8):
    """Closed solid whose top is a shallow segmental arch spanning corners
    0-1 / 3-2 (i.e. across the building's width), with the ridge running along
    the long axis. corners are CCW plan points."""
    c0, c1, c2, c3 = corners
    rise = z_crown - z_spring
    chord = math.hypot(c1[0] - c0[0], c1[1] - c0[1])
    half = chord / 2.0
    R = (rise * rise + half * half) / (2.0 * rise)
    verts, faces = [], []
    # two rails: A from c0->c1 (south-west end), B from c3->c2
    for k in range(segments + 1):
        t = k / segments
        x = chord * (t - 0.5)
        z = z_spring + math.sqrt(max(R * R - x * x, 0.0)) - (R - rise)
        a = lerp(c0, c1, t)
        b = lerp(c3, c2, t)
        verts.append((a[0], a[1], z))
        verts.append((b[0], b[1], z))
    n = segments + 1
    base = len(verts)
    verts.extend([(c0[0], c0[1], z0), (c3[0], c3[1], z0), (c1[0], c1[1], z0), (c2[0], c2[1], z0)])
    b0, b3, b1, b2 = base, base + 1, base + 2, base + 3
    for k in range(segments):
        a0, b0k = 2 * k, 2 * k + 1
        a1, b1k = 2 * (k + 1), 2 * (k + 1) + 1
        faces.append((a0, a1, b1k, b0k))        # the vault surface
    # the two curved gable ends
    for k in range(segments):
        faces.append((2 * k, b0, b1, 2 * (k + 1)) if k == 0 else (2 * k, 2 * (k + 1), b1, b0))
        faces.append((2 * k + 1, 2 * (k + 1) + 1, b2, b3) if k == 0 else
                     (2 * k + 1, b3, b2, 2 * (k + 1) + 1))
    faces.append((b0, b3, b2, b1))              # base
    obj = new_mesh(name, verts, faces, [mat])
    return obj


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
        # Workbench's MATERIAL colour mode reads diffuse_color, not the BSDF, and
        # the review rig falls back to Workbench whenever this machine is loaded.
        m.diffuse_color = (*rgb, 1.0)
        m.roughness = 0.85
        if name.endswith("_Glow"):
            bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 0.0
        mats[name] = m
    return mats


def bay_spans(edge, nbays, margin=0.55, pier=1.30):
    """(s0, s1) of each window opening across a facade."""
    _, _, length, _, _ = poly_edge(edge)
    usable = length - 2 * margin
    win = (usable - (nbays - 1) * pier) / nbays
    return [(margin + k * (win + pier), margin + k * (win + pier) + win) for k in range(nbays)], win


# One bay in four lights at night, scattered so no floor reads as a band.
LIT_STEUART = {(0, 3), (1, 0), (1, 4), (2, 2), (3, 1), (3, 4), (4, 0), (5, 2)}


def punched_window(tag, edge, s0, s1, z0, z1, mats, lit=False):
    """One 1907 punched opening: a rust-lined reveal recessed behind the brick
    face, dark glass inside it, one meeting rail, a pale sill under it.

    The walls are solid prisms with nothing cut out of them, so the reveal is
    authored PROUD of the wall at a darker value — at city distance a dark
    plate on brick reads as a hole, and a hole costs four times the triangles.
    """
    bevel(wall_box(f"{tag}_reveal", edge, s0 - 0.10, s1 + 0.10, z0 - 0.10, z1 + 0.10,
                   -0.05, 0.04, mats["Toy_rust"]), width=0.04, segments=1)
    wall_box(f"{tag}_glass", edge, s0, s1, z0, z1, 0.03, 0.09, mats["Toy_glass"])
    zm = (z0 + z1) / 2
    wall_box(f"{tag}_rail", edge, s0, s1, zm - 0.035, zm + 0.035, 0.08, 0.11, mats["Toy_ink"])
    wall_box(f"{tag}_sill", edge, s0 - 0.18, s1 + 0.18, z0 - 0.24, z0 - 0.10,
             -0.02, 0.14, mats["Toy_stone"])
    if lit:
        wall_box(f"{tag}_lit", edge, s0 + 0.06, s1 - 0.06, z0 + 0.06, z1 - 0.06,
                 0.10, 0.13, mats["Toy_glassl_Glow"])


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    mats = materials()

    brick = mats["Toy_brick"]
    stone = mats["Toy_stone"]
    cream = mats["Toy_cream"]
    sash = mats["Toy_sash"]
    glass = mats["Toy_glass"]
    glassl = mats["Toy_glassl"]
    steel = mats["Toy_steel"]
    ink = mats["Toy_ink"]

    near, far = split_rings(STONE_DEPTH)

    # ---- 1. body: brick slab + the 1983 cast-stone band ------------------- #
    bevel(prism("body_brick", near, 0.0, H_ROOF, brick, mat_caps=steel), width=0.12)
    bevel(prism("body_stone", far, 0.0, H_ROOF, stone, mat_caps=steel), width=0.12)

    # ---- 2. ground floor -------------------------------------------------- #
    # Steuart Street: dark-green painted metal shopfront under the green board.
    _, _, l_st, _, _ = poly_edge(E_STEUART)
    bevel(wall_box("gf_st_band", E_STEUART, 0.0, l_st, H_BAND0, H_GF, -0.12, 0.16, sash),
          width=0.07)
    bevel(wall_box("gf_st_base", E_STEUART, 0.0, l_st, H_PLINTH, H_BAND0, -0.10, 0.05, sash),
          width=0.05)
    ec = l_st / 2
    # the recessed entry: an ink void with a gold-lit head, flanked by shopfronts
    wall_box("entry_void", E_STEUART, ec - 2.05, ec + 2.05, 0.0, H_BAND0 - 0.35,
             -0.55, 0.07, ink)
    wall_box("entry_glow", E_STEUART, ec - 1.85, ec + 1.85, H_BAND0 - 1.05, H_BAND0 - 0.55,
             0.08, 0.11, mats["Toy_gold_Glow"])
    for k, (a, b) in enumerate(((0.55, ec - 2.35), (ec + 2.35, l_st - 0.55))):
        wall_box(f"gf_st_shop{k}", E_STEUART, a, b, H_PLINTH + 0.35, H_BAND0 - 0.45,
                 0.06, 0.12, glass)
        wall_box(f"gf_st_shoplit{k}", E_STEUART, a + 0.25, b - 0.25, H_PLINTH + 0.55,
                 H_BAND0 - 0.65, 0.13, 0.16, mats["Toy_glassl_Glow"])

    # The Embarcadero: white-painted shopfront base, restaurant glazing.
    _, _, l_em, _, _ = poly_edge(E_EMB)
    bevel(wall_box("gf_em_base", E_EMB, 0.0, l_em, 0.0, H_GF, -0.10, 0.10, cream), width=0.07)
    wall_box("gf_em_glass", E_EMB, 0.70, l_em - 0.70, 0.75, H_GF - 0.75, 0.09, 0.15, glass)
    wall_box("gf_em_lit", E_EMB, 1.10, l_em - 1.10, 1.00, H_GF - 1.00, 0.16, 0.19,
             mats["Toy_glassl_Glow"])
    for k, s in enumerate((0.70, l_em / 2 - 0.22, l_em - 0.92)):
        wall_box(f"gf_em_pier{k}", E_EMB, s, s + 0.44, 0.0, H_GF, 0.09, 0.20, ink)

    # ---- 3. the Steuart Street brick elevation ---------------------------- #
    spans, _ = bay_spans(E_STEUART, BAYS)
    for ri, z0 in enumerate(ROWS):
        h = WIN_H_TOP if ri == len(ROWS) - 1 else WIN_H
        for bi, (s0, s1) in enumerate(spans):
            punched_window(f"st_w{ri}_{bi}", E_STEUART, s0, s1, z0, z0 + h, mats,
                           lit=(ri, bi) in LIT_STEUART)
    # green string course under the taller top storey
    bevel(wall_box("string_st", E_STEUART, -0.05, l_st + 0.05, H_STRING0, H_STRING1,
                   -0.06, 0.14, sash), width=0.05)

    # ---- 4. The Embarcadero cast-stone elevation -------------------------- #
    # Five continuous horizontal glazing bands instead of a punched grid: that
    # is what the 1983 re-clad actually does, and it is the fastest way to tell
    # the two ends apart from the air.
    for ri, z0 in enumerate(ROWS[:-1]):
        wall_box(f"em_band{ri}", E_EMB, 0.55, l_em - 0.55, z0, z0 + WIN_H + 0.25,
                 0.02, 0.10, glassl)
        wall_box(f"em_bandg{ri}", E_EMB, 0.75, l_em - 0.75, z0 + 0.12, z0 + WIN_H + 0.13,
                 0.10, 0.13, glass)
        bevel(wall_box(f"em_spandrel{ri}", E_EMB, -0.05, l_em + 0.05, z0 - 0.55, z0,
                       -0.04, 0.13, stone), width=0.05)
    bevel(wall_box("em_parapet_band", E_EMB, -0.05, l_em + 0.05, 19.95, H_CORN1,
                   -0.04, 0.16, stone), width=0.06)
    # two lit bands at night, low down where the offices actually stay on
    for ri in (1, 3):
        wall_box(f"em_lit{ri}", E_EMB, 1.00, l_em - 1.00, ROWS[ri] + 0.20,
                 ROWS[ri] + WIN_H + 0.05, 0.14, 0.17, mats["Toy_glassl_Glow"])

    # ---- 5. the two party walls ------------------------------------------- #
    # Blind brick, but not blank: 141 Steuart only reaches ~21.8 m and 121 only
    # ~29.6 m, so the strips above them are genuinely seen from the air.
    for tag, edge in (("se", E_SE), ("nw", E_NW)):
        _, _, l_f, _, _ = poly_edge(edge)
        # s runs from the Steuart end on the SE flank and from the Embarcadero
        # end on the NW one, so the brick run is at opposite ends of the two.
        s_lo, s_hi = ((1.2, l_f - STONE_DEPTH - 0.6) if tag == "se"
                      else (STONE_DEPTH + 0.6, l_f - 1.2))
        for z in (H_GF, ROWS[2], ROWS[4]):
            wall_box(f"flank_{tag}_line{int(z)}", edge, s_lo, s_hi, z - 0.09, z + 0.05,
                     -0.02, 0.05, mats["Toy_rust"])

    # ---- 6. cornice ------------------------------------------------------- #
    # The strongest horizontal on the block: a projecting dark-green sheet-metal
    # cornice topping at 21.8 m, returning onto both flanks.
    bevel(ring_band("cornice", H_CORN0, H_CORN1 - 0.22, -0.22, 0.42, sash), width=0.07)
    bevel(ring_band("cornice_cap", H_CORN1 - 0.22, H_CORN1, -0.30, 0.52, sash), width=0.05)
    bevel(ring_band("gravel_stop", H_ROOF, H_ROOF + 0.10, -1.60, -0.24, steel), width=0.04)

    # ---- 7. roof ---------------------------------------------------------- #
    # u runs toward The Embarcadero along the long axis; the origin is the
    # footprint centre, so the roof field is u in [-21, 21], v in [-7, 7].
    bevel(uv_box("monitor", -6.0, 0.0, H_ROOF, H_ROOF + 0.95, 17.5, 2.30, steel), width=0.10)
    bevel(uv_box("monitor_cap", -6.0, 0.0, H_ROOF + 0.95, H_ROOF + 1.15, 18.0, 2.70, cream),
          width=0.06)
    bevel(uv_box("stair_head", -17.0, -2.4, H_ROOF, H_ROOF + 1.85, 3.6, 3.0, cream),
          width=0.10)
    bevel(uv_box("skylight", 2.0, 3.3, H_ROOF, H_ROOF + 0.40, 3.6, 2.6, glass), width=0.06)
    for i, (u, v) in enumerate(((-13.5, 3.6), (-9.0, 3.9), (-2.0, -3.6), (2.5, -3.9))):
        bevel(uv_box(f"mech{i}", u, v, H_ROOF, H_ROOF + 1.15, 2.0, 1.7, cream), width=0.08)
    for i, (u, v) in enumerate(((-19.0, 3.5), (5.5, 4.2), (-11.5, -3.8), (-3.0, -4.0))):
        bevel(uv_box(f"vent{i}", u, v, H_ROOF, H_ROOF + 0.80, 0.65, 0.65, ink), width=0.05)
    uv_box("walkway", -6.0, -3.9, H_ROOF, H_ROOF + 0.06, 22.0, 1.2, stone)

    # ---- 8. the penthouse: the crest -------------------------------------- #
    _, pent = split_rings(PENT_DEPTH)
    pent_in = offset_polygon(pent, -0.45)
    bevel(prism("pent_body", pent_in, H_ROOF, H_PENT, stone, mat_caps=cream), width=0.14)
    # glazing on all four sides — it is a lantern, and it is what the bay sees
    for edge, poly in ((E_STEUART, pent_in), (E_SE, pent_in), (E_EMB, pent_in), (E_NW, pent_in)):
        _, _, l_p, _, _ = poly_edge(edge, poly)
        wall_box(f"pent_glass_{edge[0]}", edge, 0.45, l_p - 0.45, H_ROOF + 0.75,
                 H_PENT - 0.45, 0.02, 0.09, glassl, poly=poly)
        wall_box(f"pent_glow_{edge[0]}", edge, 0.65, l_p - 0.65, H_ROOF + 0.95,
                 H_PENT - 0.65, 0.09, 0.12, mats["Toy_glassl_Glow"], poly=poly)
    bevel(ring_band("pent_band", H_PENT - 0.45, H_PENT, -0.10, 0.22, cream, poly=pent_in),
          width=0.06)
    barrel("pent_roof", offset_polygon(pent_in, 0.18), H_PENT - 0.60, H_PENT, H_CREST, cream,
           segments=6)

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
    print(f"[build] xy centre offset=({round((mn[0]+mx[0])/2, 4)}, {round((mn[1]+mx[1])/2, 4)})")
    print("[build] anchor lon/lat: -122.3924386 37.7930568 (footprint AABB centre)")
    print("[build] Steuart front normal 224.9 deg true; Embarcadero front 44.8 deg")
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

    blend = os.path.join(out, "131-steuart.blend")
    glb = os.path.join(out, "131-steuart.glb")
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
