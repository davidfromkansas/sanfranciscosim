"""Deterministic Blender build of the SF-SIM miniature 300 Brannan Street.

    blender -b --python build_300_brannan.py -- [--out DIR]

Writes 300-brannan.blend and 300-brannan.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint AABB centre (anchor lon -122.3925543,
lat 37.7818313), min Z = 0, rooftop penthouse cap top exactly 25.20 m.

Design (see REFERENCE.md for the sources behind every number):

* the DataSF surveyed polygon (block 3775 lot 008), simplified to seven vertices
  and extruded as one 1,136 m2 full-lot concrete block — the 1912 Blinn Estate
  Building, Charles C. Frye & George A. Schastey, six storeys, 70 ft to the
  parapet;
* the identity is the CANTED CORNER across Second and Brannan carrying one
  window bay per floor, over a charcoal base whose heavy cornice returns round
  it;
* second identity is the tonal grid: light `Toy_stone` pilasters running the
  full height of both frontages against continuous dark `Toy_roofd` bay stripes,
  which is how the deep recesses of the real steel-sash bays read at city
  distance;
* one very tall charcoal ground storey — segmental-arched openings on Second
  Street (one of them a roll-up loading bay), rectangular storefronts on Brannan,
  a black fire escape on Brannan;
* the Stanford Street alley flank keeps the rhythm without the pilasters; the
  north-west lot-line wall is a finished blank plane, which is what a 1912 party
  wall is;
* the roof is a working roof: dark membrane, the penthouse cluster just
  north-west of centre (the crest at 25.20 m), the mechanical platform toward
  Brannan, a tank and vents;
* night state: the canted corner is the hero — its bay lit on all five upper
  floors over a lit ground-floor band that returns round the cant — with a third
  of the frontage bays scattered behind it. Glow surfaces are thin plates proud
  of opaque glazing — the app renders _Glow in a separate layer at ~12% alpha by
  day (more where a closed shell stacks two layers), so a primary surface must
  never be authored as glow.

Walls are SOLID prisms with no cut openings; every opening is drawn proud of the
wall and reads as a recess because the pilasters stand 0.30 m out in front of it
(style bible s.5). This is the 500 Third Street idiom and it is why the model
needs no booleans.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF footprint (ynuv-fyni, mblr SF3775008) projected with the app's tangent
# projection (LON0 -122.4375, LAT0 37.77), simplified to seven vertices and
# recentred on the footprint AABB centre. CCW, (x east, y north). 1,136.5 m2
# against the survey's 1,139.8 m2.
FOOTPRINT = [
    (3.036, 23.634),      # v0  N corner   — Second St x NW party line
    (-22.883, -2.212),    # v1  W corner   — NW party line x Stanford St
    (-1.837, -23.634),    # v2  S corner   — Stanford St x Brannan St
    (1.839, -20.035),     # v3  notch, 1.19 m in from the Brannan wall plane
    (2.660, -20.830),     # v4  notch, back out — start of the Brannan frontage
    (22.437, -1.398),     # v5  south end of the canted corner
    (22.883, 3.629),      # v6  north end of the canted corner
]
E_PARTY = (0, 1)   # NW lot-line wall, 36.60 m, outward normal 315.1 deg true
E_STAN = (1, 2)    # SW Stanford Street alley flank, 30.03 m, normal 225.5 deg
E_NOTCH_A = (2, 3)  # 5.14 m set back 1.19 m from the Brannan plane, normal 135.6
E_NOTCH_B = (3, 4)  # 1.14 m return, normal 224.1 deg
E_BRAN = (4, 5)    # SE Brannan Street front, 27.73 m, normal 135.5 deg
E_CANT = (5, 6)    # the canted corner, 5.05 m, normal 95.1 deg
E_SECOND = (6, 0)  # NE Second Street front, 28.18 m, normal 45.2 deg

H_PLINTH = 0.45    # stone plinth under the charcoal base
H_GF = 5.00        # top of the charcoal ground storey
H_BELT0, H_BELT1 = 4.80, 5.58   # the heavy base cornice band
H_ROOF = 20.84     # roof membrane surface (DataSF LiDAR median)
FLOOR_H = (H_ROOF - H_BELT1) / 5.0   # 3.088 m
FLOORS = tuple(H_BELT1 + i * FLOOR_H for i in range(5))
WIN_LO, WIN_HI = 0.55, 2.66   # window band within a floor
H_PAR = 21.18      # parapet below its coping
H_PAR_CAP = 21.34  # parapet coping top = 70 ft, the architectural height
H_BULK = 23.40     # secondary bulkhead
H_PENT = 24.95     # penthouse walls
H_CREST = 25.20    # penthouse cap top = the export's bounding-box top

BAYS_SECOND = 6
BAYS_BRAN = 6
BAYS_CANT = 1
BAYS_STAN = 6
PIL_W = 0.95       # pilaster strip width on the two frontages and the cant
PIL_D = 0.30       # pilaster projection — this is what makes the bays read deep
CAP_H = 0.50       # stepped capital block at the top of every pilaster

BEVEL_W = 0.12
BEVEL_SEG = 2

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_ink": "3a3530",
    "Toy_roofd": "45454a",
    "Toy_slate": "6f7883",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_steel": "9aa0a6",
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


# The building's own axes for roof layout: U runs along the Brannan frontage
# (north-east positive), V points out toward Brannan (south-east). Laying the
# roof out in this frame keeps the penthouse's long axis parallel to Brannan,
# which is how the nadir imagery reads it.
def _axes():
    _, _, _, t_bran, n_bran = poly_edge(E_BRAN)
    return t_bran, n_bran


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

    Width is clamped to 40% of the object's thinnest dimension; without that,
    beveling a thin plate at full width collapses faces into zero-area triangles
    and flips signed volume (the failure documented in 500 Third's build).
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
    bm.to_mesh(bm_target := obj.data)
    bm.free()
    bm_target.shade_flat()
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


def arch_plate(name, edge, s0, s1, z0, z1, rise, d_in, d_out, mat, segs=7):
    """A wall plate whose top is a segmental (flattened) arch — the South End
    Historic District's signature ground-floor opening. Extruded along the
    facade normal, closed, so it survives the signed-volume normals test."""
    a, _, _, t, n = poly_edge(edge)
    half = (s1 - s0) / 2.0
    sc = (s0 + s1) / 2.0
    # circle through (s0, z1-rise), (sc, z1), (s1, z1-rise)
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
        return (a[0] + t[0] * s + n[0] * d, a[1] + t[1] * s + n[1] * d, 0.0)

    verts = []
    for d in (d_in, d_out):
        for s, z in profile:
            x, y, _ = p(s, d)
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


def bay_spans(edge, nbays, pil_w=PIL_W):
    """(s0, s1) of each bay opening, with a pilaster between and at both ends."""
    _, _, length, _, _ = poly_edge(edge)
    bay = (length - (nbays + 1) * pil_w) / nbays
    out = []
    for k in range(nbays):
        s0 = pil_w + k * (bay + pil_w)
        out.append((s0, s0 + bay))
    return out, bay


def pilasters(tag, edge, nbays, mats, z0, z1):
    _, _, length, _, _ = poly_edge(edge)
    _, bay = bay_spans(edge, nbays)
    for k in range(nbays + 1):
        s0 = k * (bay + PIL_W)
        bevel(
            wall_box(f"{tag}_pil{k}", edge, s0, s0 + PIL_W, z0, z1 - CAP_H, -0.05,
                     PIL_D, mats["Toy_stone"]),
            width=0.07,
        )
        # stepped capital: the one piece of moulding the miniature keeps
        bevel(
            wall_box(f"{tag}_cap{k}", edge, s0 - 0.12, s0 + PIL_W + 0.12, z1 - CAP_H, z1,
                     -0.05, PIL_D + 0.10, mats["Toy_trim"]),
            width=0.06,
        )


def glazed_elevation(tag, edge, nbays, mats, lit, pil=True):
    """One frontage: a continuous dark stripe per bay (this is the deep recess),
    light pilasters standing in front of it, and a glazed panel with a light sill
    per floor inside each stripe."""
    spans, _ = bay_spans(edge, nbays, PIL_W if pil else 0.70)
    stone, trim, roofd, glass = (mats["Toy_stone"], mats["Toy_trim"],
                                 mats["Toy_roofd"], mats["Toy_glass"])
    for bi, (s0, s1) in enumerate(spans):
        # the bay stripe: full height of the upper block, slightly proud so it
        # is not z-fighting the body, and 0.30 m behind the pilaster faces
        bevel(
            wall_box(f"{tag}_bay{bi}", edge, s0, s1, H_BELT1, H_ROOF, -0.06, 0.04, roofd),
            width=0.06, segments=1,
        )
        for fi, base in enumerate(FLOORS):
            z0, z1 = base + WIN_LO, base + WIN_HI
            wall_box(f"{tag}_g{fi}_{bi}", edge, s0 + 0.30, s1 - 0.30, z0, z1,
                     0.03, 0.12, glass)
            wall_box(f"{tag}_sill{fi}_{bi}", edge, s0 + 0.16, s1 - 0.16, z0 - 0.28,
                     z0 - 0.10, 0.03, 0.16, trim)
            if (fi, bi) in lit:
                wall_box(f"{tag}_lit{fi}_{bi}", edge, s0 + 0.38, s1 - 0.38, z0 + 0.16,
                         z1 - 0.16, 0.13, 0.16, mats["Toy_glassl_Glow"])
    if pil:
        pilasters(tag, edge, nbays, mats, H_BELT1, H_ROOF)


# Roughly a third of the bays, scattered so no floor reads as a band. The cant
# is handled separately: it is lit on every floor, on purpose.
LIT_SECOND = {(0, 4), (1, 0), (2, 2), (2, 5), (3, 1), (4, 3)}
LIT_BRAN = {(0, 2), (1, 4), (2, 0), (3, 5), (4, 1), (4, 4)}
LIT_CANT = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)}
LIT_STAN = set()


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
    ink = mats["Toy_ink"]
    roofd = mats["Toy_roofd"]
    slate = mats["Toy_slate"]
    glassl = mats["Toy_glassl"]
    steel = mats["Toy_steel"]

    # ---- 1. body + roof field -------------------------------------------- #
    bevel(prism("body", FOOTPRINT, 0.0, H_ROOF, stone, mat_caps=roofd), width=0.14)

    # ---- 2. the charcoal ground storey ------------------------------------ #
    # On the three exposed elevations and the cant. The party wall keeps bare
    # stucco, which is what a lot-line wall is.
    for tag, edge in (("second", E_SECOND), ("cant", E_CANT), ("bran", E_BRAN),
                      ("na", E_NOTCH_A), ("nb", E_NOTCH_B), ("stan", E_STAN)):
        _, _, length, _, _ = poly_edge(edge)
        bevel(wall_box(f"gf_{tag}", edge, 0.0, length, H_PLINTH, H_GF, -0.10, 0.07, roofd),
              width=0.06)

    # Second Street: segmental-arched openings, one of them the loading bay
    spans_2, _ = bay_spans(E_SECOND, BAYS_SECOND)
    for bi, (s0, s1) in enumerate(spans_2):
        if bi == BAYS_SECOND - 1:  # roll-up loading door at the party-wall end
            bevel(wall_box(f"gf_second_roll{bi}", E_SECOND, s0 + 0.30, s1 - 0.30,
                           H_PLINTH + 0.05, H_GF - 1.35, 0.06, 0.13, steel), width=0.05)
            continue
        arch_plate(f"gf_second_a{bi}", E_SECOND, s0 + 0.25, s1 - 0.25, H_PLINTH + 0.15,
                   H_GF - 0.90, 0.42, 0.06, 0.12, glassl)
    # Brannan: rectangular storefronts, with the main entrance in bay 2
    spans_b, _ = bay_spans(E_BRAN, BAYS_BRAN)
    for bi, (s0, s1) in enumerate(spans_b):
        wall_box(f"gf_bran_g{bi}", E_BRAN, s0 + 0.25, s1 - 0.25, H_PLINTH + 0.15,
                 H_GF - 0.90, 0.06, 0.12, glassl)
    eb0, eb1 = spans_b[2]
    bevel(wall_box("entry_canopy", E_BRAN, eb0 - 0.20, eb1 + 0.20, H_GF - 1.90,
                   H_GF - 1.58, 0.06, 1.05, ink), width=0.06)
    # the cant's own recessed corner entrance
    _, _, l_cant, _, _ = poly_edge(E_CANT)
    wall_box("gf_cant_g", E_CANT, 1.05, l_cant - 1.05, H_PLINTH + 0.15, H_GF - 0.90,
             0.06, 0.12, glassl)

    # the heavy base cornice, all the way round — thickened so it survives at
    # thumbnail size and carries the cant
    bevel(ring_band("belt", H_BELT0, H_BELT1 - 0.16, -0.20, 0.74, ink), width=0.09)
    bevel(ring_band("belt_cap", H_BELT1 - 0.16, H_BELT1, -0.24, 0.62, stone), width=0.06)

    # night: the ground-floor band under the cornice, returning round the cant
    for tag, edge, s0, s1 in (
        ("cantband", E_CANT, 0.75, l_cant - 0.75),
        ("branband", E_BRAN, spans_b[2][0], spans_b[2][1]),
        ("secondband", E_SECOND, spans_2[0][0], spans_2[0][1]),
    ):
        wall_box(f"gf_glow_{tag}", edge, s0 + 0.45, s1 - 0.45, H_PLINTH + 0.45,
                 H_GF - 1.20, 0.13, 0.16, mats["Toy_trim_Glow"])

    # ---- 3. the glazed elevations ----------------------------------------- #
    glazed_elevation("second", E_SECOND, BAYS_SECOND, mats, LIT_SECOND)
    glazed_elevation("bran", E_BRAN, BAYS_BRAN, mats, LIT_BRAN)
    glazed_elevation("cant", E_CANT, BAYS_CANT, mats, LIT_CANT)
    glazed_elevation("stan", E_STAN, BAYS_STAN, mats, LIT_STAN, pil=False)
    glazed_elevation("nota", E_NOTCH_A, 1, mats, {(1, 0), (3, 0)}, pil=False)

    # ---- 4. Stanford flank trim and the north-west party wall -------------- #
    _, _, l_stan, _, _ = poly_edge(E_STAN)
    for fi, base in enumerate(FLOORS):
        wall_box(f"stan_line{fi}", E_STAN, 0.4, l_stan - 0.4, base - 0.10, base + 0.08,
                 -0.02, 0.10, stone)
    bevel(wall_box("stan_door", E_STAN, 13.4, 16.6, 0.0, 4.05, -0.02, 0.11, ink),
          width=0.05)
    spans_s, _ = bay_spans(E_STAN, BAYS_STAN, 0.70)
    for bi, (s0, s1) in enumerate(spans_s):
        if bi in (2, 3):
            continue
        wall_box(f"gf_stan_g{bi}", E_STAN, s0 + 0.45, s1 - 0.45, H_PLINTH + 0.35,
                 H_GF - 1.15, 0.06, 0.12, glassl)

    _, _, l_party, _, _ = poly_edge(E_PARTY)
    for k in range(5):
        s_ = 1.6 + k * 6.9
        bevel(wall_box(f"party_lis{k}", E_PARTY, s_, s_ + 1.10, 0.0, H_ROOF, -0.05,
                       0.12, trim), width=0.05, segments=1)
    for base in FLOORS[1:]:
        wall_box("party_line", E_PARTY, 1.0, l_party - 1.0, base - 0.10, base + 0.06,
                 0.0, 0.16, trim)
    # a sparse scatter of small punched openings on the top two floors only —
    # the storeys that actually stand clear of 577 Second and 318 Brannan
    for fi in (3, 4):
        base = FLOORS[fi]
        for k, s in enumerate((6.0, 12.5, 19.0, 25.5, 31.0)):
            wall_box(f"party_w{fi}_{k}", E_PARTY, s, s + 1.30, base + 1.05,
                     base + 2.35, 0.0, 0.10, roofd)

    # ---- 5. fire escape on Brannan ---------------------------------------- #
    fe0 = spans_b[1][0] + 0.4
    fe1 = spans_b[1][1] - 0.4
    for fi, base in enumerate(FLOORS):
        bevel(wall_box(f"fe_land{fi}", E_BRAN, fe0, fe1, base + 0.10, base + 0.28,
                       0.05, 1.05, ink), width=0.05, segments=1)
        wall_box(f"fe_railA{fi}", E_BRAN, fe0, fe1, base + 0.28, base + 1.20,
                 0.98, 1.05, ink)
        if fi:
            wall_box(f"fe_stair{fi}", E_BRAN, fe0 + 0.15, fe0 + 0.95,
                     FLOORS[fi - 1] + 0.28, base + 0.10, 0.60, 0.72, ink)
    for k, s in enumerate((fe0, fe1 - 0.14)):
        wall_box(f"fe_post{k}", E_BRAN, s, s + 0.14, H_PLINTH, FLOORS[-1] + 1.20,
                 0.92, 1.06, ink)

    # ---- 6. parapet -------------------------------------------------------- #
    bevel(ring_band("parapet", H_ROOF, H_PAR, -0.40, 0.08, stone), width=0.06)
    bevel(ring_band("parapet_cap", H_PAR, H_PAR_CAP, -0.50, 0.18, trim), width=0.05)

    # ---- 7. roof ----------------------------------------------------------- #
    # Penthouse cluster just north-west of centre (v negative = away from
    # Brannan), plant toward Brannan — matching the nadir imagery. The penthouse
    # is the crest and the only thing that breaks the parapet silhouette.
    bevel(uv_box("pent", 1.0, -2.6, H_ROOF, H_PENT, 8.0, 6.4, slate), width=0.14)
    bevel(uv_box("pent_cap", 1.0, -2.6, H_PENT, H_CREST, 8.4, 6.8, trim), width=0.08)
    bevel(uv_box("bulk", -5.6, -0.6, H_ROOF, H_BULK, 5.0, 4.0, slate), width=0.12)
    bevel(uv_box("bulk_cap", -5.6, -0.6, H_BULK, H_BULK + 0.22, 5.3, 4.3, trim), width=0.06)

    bevel(uv_box("mech_pad", -0.5, 5.6, H_ROOF, H_ROOF + 0.18, 12.0, 6.4, trim), width=0.05)
    for i in range(4):
        bevel(uv_box(f"mech{i}", -5.0 + i * 3.2, 5.6, H_ROOF + 0.18, H_ROOF + 1.35,
                     2.1, 1.5, steel), width=0.08)
    bevel(uv_cyl("tank", -10.8, -4.2, H_ROOF, H_ROOF + 2.40, 1.10, steel), width=0.06)
    for i, (u, v) in enumerate(((9.5, -8.5), (-14.5, 5.5), (12.0, 8.0), (-9.0, 10.5))):
        bevel(uv_box(f"vent{i}", u, v, H_ROOF, H_ROOF + 0.85, 0.75, 0.75, roofd), width=0.05)
    for i, (u, v, su) in enumerate(((6.0, 11.5, 9.0), (-2.0, -9.5, 11.0))):
        bevel(uv_box(f"duct{i}", u, v, H_ROOF, H_ROOF + 0.55, su, 0.75, roofd), width=0.05)
    bevel(uv_box("hatch", 6.5, -5.0, H_ROOF, H_ROOF + 0.55, 2.0, 1.6, roofd), width=0.06)
    uv_box("walk", 1.0, 1.6, H_ROOF, H_ROOF + 0.06, 8.0, 2.2, trim)

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
    print("[build] anchor lon/lat: -122.3925543 37.7818313 (footprint AABB centre)")
    print("[build] Second St front normal 45.2 deg true; Brannan 135.5; cant 95.1")
    print(f"[build] floor height {FLOOR_H:.3f} m; deck {H_ROOF}; parapet {H_PAR_CAP}; crest {H_CREST}")
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

    blend = os.path.join(out, "300-brannan.blend")
    glb = os.path.join(out, "300-brannan.glb")
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
