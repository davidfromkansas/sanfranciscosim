"""Deterministic Blender build of the SF-SIM miniature 248-250 Ritch Street.

    blender -b --python build_248_ritch.py -- [--out DIR]

Writes 248-ritch.blend and 248-ritch.glb next to this file (or into --out).
Geometry is authored in world space in metres, Z up, +X east, +Y north, so the
model drops into the city at its real-world heading - the loader applies no
rotation. Origin = model XY bbox centre, min Z = 0, cornice crown exactly 8.60 m.

Design (see REFERENCE.md and docs/asset-plans/248-ritch.md for the sources):

* a 1915 wood-frame two-flat on a 25 x 75 ft SoMa alley lot, 2,100 sq ft over two
  storeys and a raised basement, never altered vertically in seven permits;
* the house occupies the front 13.90 m of a 23.9 m lot. The rear third is garden
  and is NOT part of this asset - the Case B exclusion clears the whole parcel and
  the app's ground plane is what should show there;
* the recognition rests on three things: the CANTED BAY through both storeys on
  the south-east half of a 7.60 m front, the BRACKETED CORNICE stepping around it,
  and the TWO ENTRIES side by side under one hood - 250 to the south-east, 248 to
  the north-west - each on its own stoop;
* the only public elevation faces north-east (outward normal 45.05 deg true) onto
  Ritch Street. The south-east flank is a party wall against 252-254, which is
  within 0.1 m of the same height, so it never shows. The NORTH-WEST flank is
  a party wall against 246 Ritch, which is 15.87 m tall - nearly twice this house
  - so that wall IS exposed in the app and is finished like a real wall;
* every height below was measured, not estimated. The roof deck at 7.95 m is the
  DataSF LiDAR median over 657 cells; the cornice crest at 8.60 m is the mean of
  two independent derivations (a two-level mixture solve on the same LiDAR summary
  giving 8.65 m, and a Street View panorama rectified against three surveyed
  corners giving 8.50 m). The LiDAR MAXIMUM of 14.27 m is refused - it is the
  five-storey neighbour bleeding across the party line. The internal structure
  1.46 + 3.26 + 3.26 = 7.98 m reproduces the LiDAR roof to 0.03 m without having
  been fitted to it, which is what licenses "measured";
* night state is domestic, not commercial: the six bay panes and the two door
  transoms only. The flat-wall window and the whole rear stay dark. Glow surfaces
  are single outward-facing quads standing proud of the opaque glazing, never
  closed shells - the app draws _Glow in a separate layer and a closed shell is
  two alpha layers deep, so it reads far brighter by day than intended.

Authoring frame: the footprint is a clean rectangle at 45.05 deg to the world
axes, so everything is placed through Face frames built from the four surveyed
corners. Because the building sits at 45 deg the axis-aligned XY bounding box is
~15.2 x 15.2 m even though the building is 7.60 x 13.90 m. That is expected.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# The project's tangent projection (AGENTS.md), used only to convert the final
# recentring shift back into a lon/lat anchor.
LON0P, LAT0P = -122.4375, 37.77
LON_M = 111320.0 * math.cos(math.radians(LAT0P))
LAT_M = 110540.0

# Centre of the built quad - the plan's design anchor, before recentring.
DESIGN_ANCHOR = (-122.3956780, 37.7801725)

# Wall box. FRONTAGE is the SURVEYED parcel frontage (DataSF acdm-wktn, blklot
# 3776105: 7.601 m between the two party lines). DEPTH is the built depth, which
# is NOT the lot depth: two independent derivations agree that the house covers
# the front ~14 m of a 23.9 m lot (LiDAR two-level mixture 14.05 m, OSM oriented
# bbox 13.84 m).
FRONTAGE = 7.60
DEPTH = 13.90
FRONT_BEARING = 45.05      # the Ritch Street elevation faces north-east
FLANK_SE_BEARING = 135.05  # party wall against 252-254
REAR_BEARING = 225.05      # onto the garden
FLANK_NW_BEARING = 315.05  # party wall against 246 - the EXPOSED one

# Every one of these is a measurement off the rectified panorama unless marked.
Z_WT = 1.46                # main floor level / top of the raised basement
Z_SILL1 = 2.31             # lower bay sill course
Z_HEAD1 = 4.00             # lower window heads
Z_HOOD0, Z_HOOD1 = 3.95, 4.25   # the entry hood band
Z_BAYCAP = 5.44            # upper bay sill course
Z_HEAD2 = 7.26             # upper window heads
Z_SPRING = 7.60            # cornice springing / top of the wall plane
Z_DECK = 7.95              # flat roof deck - MEASURED (LiDAR median 7.95 m)
Z_PARAPET = 8.35           # rear and flank upstand
Z_CREST = 8.60             # cornice crown - the bbox top, so the loader's
                           # targetHeightM / measuredHeight lands on exactly 1.0

BASE_PROUD = 0.06          # the basement stands slightly proud of the siding
WT_H = 0.12                # water table cap

# The canted bay. Real projection is nearer 0.40 m; 0.55 is the style bible's
# semantic exaggeration (s.7), and it is the ONLY exaggeration in this model -
# the height is deliberately not touched, because the whole point of this asset
# is that it is short next to 246 Ritch.
BAY_T = 2.20               # centre, metres from the SOUTH-EAST party line
BAY_FACE = 2.30            # flat front face
BAY_PROJ = 0.55            # projection; at 45 deg the lateral run equals it
BAY_CHORD = BAY_FACE + 2.0 * BAY_PROJ     # 3.40
BAY_Z0, BAY_Z1 = Z_WT, Z_SPRING

SILL_OUT = 0.12            # bay sill courses and the water table
SILL_H = 0.14

# Cornice: dentil band, then modillion brackets, then the crown. That is the
# order in the photograph and it is what carries the 8.60 m crest.
CORN_DENTIL = (Z_SPRING, 7.90, 0.13)      # z0, z1, projection
CORN_BRACKET = (7.88, 8.27)               # z0, z1
CORN_CROWN = (8.25, Z_CREST, 0.40)
BRACKET = (0.20, 0.30)                    # width along the wall, depth out
BRACKET_PITCH = 0.78
CORN_RETURN = 1.30         # how far the cornice runs onto each flank

# Entries. Two doors in 7.60 m of frontage is the visible signature of a
# two-flat and the reason the address is a range.
ENT_T0, ENT_T1 = 4.30, 7.45
ENT_RECESS = 0.35
DOOR_W, DOOR_H = 0.95, 2.05
DOOR_T = (4.95, 6.65)      # 250 to the south-east, 248 to the north-west
STOOP_D = 1.20
STOOP_STEPS = 4

WIN_RECESS = 0.10
FRAME_OUT = 0.07
EMBED = 0.03               # how far every applied band is sunk INTO the surface
                           # it sits on. Nothing here may have a face exactly
                           # coincident with another solid's face: coincident
                           # faces make the first-hit direction of a ray
                           # ambiguous and the contract's normals ray test counts
                           # the ambiguity as a flipped face.
GLASS_PROUD = 0.035

BEVEL_W, BEVEL_SEG = 0.10, 2

PALETTE_HEX = {
    "Toy_cream": "f2ede3",   # the body - every square metre of painted shiplap
                             # on all four sides. This is the style bible's SF
                             # painted-residential exception; the real house is a
                             # warm off-white and cream is the palette entry for
                             # it. 49 South Park deliberately avoided Toy_cream
                             # because 104-106 South Park already had it 90 m
                             # away; there is no cream landmark within 300 m of
                             # Ritch Street, so the conflict does not arise here.
    "Toy_trim": "f3efe6",    # window architraves, the cornice crown and
                             # brackets, the entry hood, vent stacks
    "Toy_stone": "d9d2c2",   # the dentil band under the brackets, so the
                             # ornament separates from the wall without
                             # introducing a third hue
    "Toy_steel": "9aa0a6",   # the SECOND COLOUR, and the one that makes this
                             # house recognisable: every sill course, the bay
                             # caps, the water table, the raised basement, both
                             # door leaves and both stoops. The real trim is a
                             # slate blue-grey and this is the palette's nearest.
                             # Also the roof deck membrane.
    "Toy_glass": "2a4d73",   # all windows
    "Toy_ink": "3a3530",     # the entry recess interior, the basement service
                             # opening, the chimney cap, the roof hatch
    "Toy_glassl_Glow": "6f95b8",  # the lit bay panes and door transoms at night.
                             # NOT Toy_glass_Glow (2a4d73). The app draws _Glow
                             # in a separate UNLIT layer, so at night the surface
                             # shows its raw BASE colour - and 2a4d73 is the dark
                             # navy of unlit glass, which renders as a dark
                             # window pretending to be a lit one.
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


# ----------------------------------------------------------------- geometry


def _brg(deg):
    """Compass bearing -> unit vector in world XY (+X east, +Y north)."""
    r = math.radians(deg)
    return (math.sin(r), math.cos(r))


_FN = _brg(FRONT_BEARING)              # outward from the Ritch Street front
_FT = _brg(FRONT_BEARING - 90.0)       # along the front, E corner -> S corner,
                                       # i.e. south-east party line -> north-west

# Corner names follow docs/asset-plans/248-ritch.md 2.3.
_C = (0.0, 0.0)
E_COR = (_C[0] + _FN[0] * DEPTH / 2.0 - _FT[0] * FRONTAGE / 2.0,
         _C[1] + _FN[1] * DEPTH / 2.0 - _FT[1] * FRONTAGE / 2.0)
S_COR = (E_COR[0] + _FT[0] * FRONTAGE, E_COR[1] + _FT[1] * FRONTAGE)
W_COR = (S_COR[0] - _FN[0] * DEPTH, S_COR[1] - _FN[1] * DEPTH)
N_COR = (E_COR[0] - _FN[0] * DEPTH, E_COR[1] - _FN[1] * DEPTH)

FOOTPRINT = [E_COR, S_COR, W_COR, N_COR]
CX = sum(p[0] for p in FOOTPRINT) / 4.0
CY = sum(p[1] for p in FOOTPRINT) / 4.0


class Face:
    """A local frame on one elevation: t runs along the face from `a` to `b`,
    d runs OUTWARD, z is world up.

    The outward normal is given EXPLICITLY as a bearing rather than derived from
    the footprint centroid. The bay's two 45 deg returns are the reason: a
    centroid test decides handedness from where the building's middle happens to
    be, and on a projecting element whose face looks sideways that answer is not
    reliable. Every face in this model knows which way it looks."""

    def __init__(self, a, b, normal_bearing):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        self.a = a
        self.b = b
        self.length = n
        self.t = (dx / n, dy / n)
        self.n = _brg(normal_bearing)
        self.heading = normal_bearing % 360.0

    def xy(self, t, d):
        return (
            self.a[0] + self.t[0] * t + self.n[0] * d,
            self.a[1] + self.t[1] * t + self.n[1] * d,
        )

    def rect(self, t0, t1, d0, d1):
        return [self.xy(t0, d0), self.xy(t1, d0), self.xy(t1, d1), self.xy(t0, d1)]


FRONT = Face(E_COR, S_COR, FRONT_BEARING)          # Ritch Street, faces 45.05
PARTY_NW = Face(S_COR, W_COR, FLANK_NW_BEARING)    # against 246, faces 315.05
REAR = Face(W_COR, N_COR, REAR_BEARING)            # garden, faces 225.05
PARTY_SE = Face(N_COR, E_COR, FLANK_SE_BEARING)    # against 252-254, faces 135.05

# The bay's three outer faces, each with its own explicit outward bearing. A
# canted bay's returns sit 45 deg either side of the front normal.
_BT0 = BAY_T - BAY_CHORD / 2.0        # where the bay leaves the wall (low t)
_BT1 = BAY_T + BAY_CHORD / 2.0        # where it returns to the wall (high t)
_BF0 = BAY_T - BAY_FACE / 2.0
_BF1 = BAY_T + BAY_FACE / 2.0

BAY_ARC = [
    FRONT.xy(_BT0, 0.0),
    FRONT.xy(_BF0, BAY_PROJ),
    FRONT.xy(_BF1, BAY_PROJ),
    FRONT.xy(_BT1, 0.0),
]

BAY_RET_SE = Face(BAY_ARC[0], BAY_ARC[1], FRONT_BEARING + 45.0)
BAY_FRONT = Face(BAY_ARC[1], BAY_ARC[2], FRONT_BEARING)
BAY_RET_NW = Face(BAY_ARC[2], BAY_ARC[3], FRONT_BEARING - 45.0)
BAY_FACES = [BAY_RET_SE, BAY_FRONT, BAY_RET_NW]

# The bay as a closed plan polygon, with its two wall ends pushed slightly INTO
# the wall so no face is coincident with the body's.
BAY_POLY = [
    FRONT.xy(_BT0, -0.06),
    BAY_ARC[1],
    BAY_ARC[2],
    FRONT.xy(_BT1, -0.06),
]

# The cornice runs along the front with the bay spliced in, and returns
# CORN_RETURN metres onto each flank. It is an OPEN polyline, not a ring: the
# rear carries no cornice (2.4), and an open run avoids every reflex-vertex
# offset failure a closed ring would hit at the two bay junctions.
CORNICE_PATH = (
    [PARTY_SE.xy(PARTY_SE.length - CORN_RETURN, 0.0), E_COR]
    + BAY_ARC
    + [S_COR, PARTY_NW.xy(CORN_RETURN, 0.0)]
)
# E_COR and BAY_ARC[0] are distinct (the bay starts 0.5 m along), as are
# BAY_ARC[3] and S_COR.


# --------------------------------------------------------------- mesh helpers


def new_mesh(name, verts, faces, materials, face_mats=None, recalc=True):
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
    if recalc:
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()
    mesh.shade_flat()
    return obj


def prism(name, poly_xy, z0, z1, mat, mat_top=None):
    """Closed extrusion of a world-XY polygon (walls + both caps)."""
    n = len(poly_xy)
    verts = [(x, y, z0) for x, y in poly_xy] + [(x, y, z1) for x, y in poly_xy]
    faces, face_mats = [], []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
        face_mats.append(0)
    faces.append(tuple(range(n - 1, -1, -1)))
    face_mats.append(0)
    faces.append(tuple(range(n, 2 * n)))
    face_mats.append(1 if mat_top else 0)
    mats = [mat, mat_top] if mat_top else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def bevel(obj, width=BEVEL_W, segments=BEVEL_SEG):
    """Miniature-style edge softening (style bible s.4). The offset is capped at
    a third of the object's thinnest dimension: bands, frames and glow plates are
    only 30-140 mm thick and a full bevel collapses opposing profiles into
    zero-area slivers even with clamp_overlap."""
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


def _seg_normal(a, b, side):
    dx, dy = b[0] - a[0], b[1] - a[1]
    m = math.hypot(dx, dy) or 1e-9
    return (-dy / m * side, dx / m * side)


def _path_side(pts):
    """Handedness of an open polyline, taken ONCE from the MIDDLE segment, which
    is the one guaranteed to face squarely out. Never per-segment and never from
    the building centroid: on the bay returns those answers disagree."""
    i = max(0, (len(pts) - 1) // 2)
    a, b = pts[i], pts[i + 1]
    mid = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
    n = _seg_normal(a, b, 1.0)
    return 1.0 if n[0] * (mid[0] - CX) + n[1] * (mid[1] - CY) > 0.0 else -1.0


def path_offset(pts, d, side=None):
    """Offset an OPEN polyline by `d` metres along each segment's outward normal,
    re-intersecting neighbouring segments.

    The spike cap matters here. Both junctions where the bay meets the wall are
    REFLEX seen from outside; at a 45 deg reflex turn the two offset lines meet
    2.6 x d away, which at the crown's 0.40 m is a 1.05 m sail sticking out of the
    facade. Capping the displacement replaces the sail with a chamfer nobody can
    see at this scale."""
    if side is None:
        side = _path_side(pts)
    n = len(pts)
    lines = []
    for i in range(n - 1):
        a, b = pts[i], pts[i + 1]
        u_len = math.hypot(b[0] - a[0], b[1] - a[1]) or 1e-9
        u = ((b[0] - a[0]) / u_len, (b[1] - a[1]) / u_len)
        nrm = _seg_normal(a, b, side)
        lines.append(((a[0] + nrm[0] * d, a[1] + nrm[1] * d), u))
    out = [lines[0][0]]
    for i in range(1, n - 1):
        (p0, u0) = lines[i - 1]
        (p1, u1) = lines[i]
        den = u0[0] * u1[1] - u0[1] * u1[0]
        if abs(den) < 1e-9:
            out.append(p1)
            continue
        t = ((p1[0] - p0[0]) * u1[1] - (p1[1] - p0[1]) * u1[0]) / den
        q = (p0[0] + u0[0] * t, p0[1] + u0[1] * t)
        v = (q[0] - pts[i][0], q[1] - pts[i][1])
        m = math.hypot(v[0], v[1])
        cap = abs(d) * 1.45
        if m > cap and m > 1e-9:
            q = (pts[i][0] + v[0] * cap / m, pts[i][1] + v[1] * cap / m)
        out.append(q)
    a, b = pts[-2], pts[-1]
    nrm = _seg_normal(a, b, side)
    out.append((b[0] + nrm[0] * d, b[1] + nrm[1] * d))
    return out


def path_band(name, pts, z0, z1, d0, d1, mat):
    """A closed solid swept along an OPEN polyline: cross-section is the
    rectangle (d0..d1) x (z0..z1), d measured outward from the path."""
    side = _path_side(pts)
    a = path_offset(pts, d0, side)
    b = path_offset(pts, d1, side)
    verts, faces = [], []
    for i in range(len(pts)):
        verts += [(a[i][0], a[i][1], z0), (b[i][0], b[i][1], z0),
                  (b[i][0], b[i][1], z1), (a[i][0], a[i][1], z1)]
    for i in range(len(pts) - 1):
        k, m = 4 * i, 4 * (i + 1)
        faces += [(k, k + 1, m + 1, m), (k + 1, k + 2, m + 2, m + 1),
                  (k + 2, k + 3, m + 3, m + 2), (k + 3, k, m, m + 3)]
    faces.append((0, 3, 2, 1))
    k = 4 * (len(pts) - 1)
    faces.append((k, k + 1, k + 2, k + 3))
    return new_mesh(name, verts, faces, [mat])


def glow_plate(name, face, t0, t1, z0, z1, mat, proud):
    """ONE outward-facing quad standing `proud` metres off a face.

    Night glow must never be a closed shell. The app draws _Glow in a separate
    layer that is translucent by day, so a closed box shows its front AND its
    back face and reads at roughly twice the intended day alpha - enough to tint
    a whole facade. One single-sided quad is the correct construction, and the
    winding is set explicitly and never recalculated."""
    p0 = face.xy(t0, proud)
    p1 = face.xy(t1, proud)
    verts = [(p0[0], p0[1], z0), (p1[0], p1[1], z0),
             (p1[0], p1[1], z1), (p0[0], p0[1], z1)]
    return new_mesh(name, verts, [(0, 1, 2, 3)], [mat], recalc=False)


def make_material(name):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = PALETTE[name] + (1.0,)
    bsdf.inputs["Roughness"].default_value = 0.85
    if "Metallic" in bsdf.inputs:
        bsdf.inputs["Metallic"].default_value = 0.0
    if name.endswith("_Glow") and "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = PALETTE[name] + (1.0,)
        bsdf.inputs["Emission Strength"].default_value = 1.0
    return mat


def window(name, face, t_c, z0, z1, mats, w, sill=True):
    """A recessed opening with a proud architrave and, optionally, a sill."""
    t0, t1 = t_c - w / 2.0, t_c + w / 2.0
    prism(f"{name}_glass", face.rect(t0, t1, -WIN_RECESS, 0.01), z0, z1,
          mats["Toy_glass"])
    # architrave: four thin members around the opening, so the cream frame reads
    # against the cream wall by its shadow rather than by colour
    prism(f"{name}_jamb0", face.rect(t0 - 0.11, t0, -EMBED, FRAME_OUT),
          z0 - 0.02, z1 + 0.11, mats["Toy_trim"])
    prism(f"{name}_jamb1", face.rect(t1, t1 + 0.11, -EMBED, FRAME_OUT),
          z0 - 0.02, z1 + 0.11, mats["Toy_trim"])
    prism(f"{name}_head", face.rect(t0 - 0.11, t1 + 0.11, -EMBED, FRAME_OUT + 0.03),
          z1, z1 + 0.11, mats["Toy_trim"])
    if sill:
        prism(f"{name}_sill", face.rect(t0 - 0.13, t1 + 0.13, -EMBED, FRAME_OUT + 0.05),
              z0 - 0.12, z0, mats["Toy_steel"])


# --------------------------------------------------------------------- build


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    mats = {k: make_material(k) for k in PALETTE_HEX}

    # 1. the body: one prism, ground to the roof deck, capped with the membrane.
    # The body starts 30 mm up, not at 0. The basement below is the piece that
    # defines min Z; lifting the body keeps their bottom caps from being coplanar
    # where they overlap in plan, which is the same ambiguous-first-hit problem
    # the basement's side faces had.
    prism("body", FOOTPRINT, 0.03, Z_DECK, mats["Toy_cream"], mats["Toy_steel"])

    # 2. the raised basement, standing slightly proud of the siding, and the
    #    water table that caps it. Base / body / cap is what makes this read as
    #    an SF flat rather than a box.
    # Proud on ALL FOUR sides, not just the front. The first pass offset only the
    # street face and left the two flanks and the rear exactly coincident with
    # the body prism's walls; coincident faces make the first-hit direction of a
    # ray ambiguous, and the party-wall elevation rendered the basement as a
    # dark band you could see through into the building. Every applied solid in
    # this model either stands clear of its host or is sunk into it by EMBED -
    # never flush.
    base_poly = [
        (c[0] + (fa.n[0] + fb.n[0]) * BASE_PROUD,
         c[1] + (fa.n[1] + fb.n[1]) * BASE_PROUD)
        for c, fa, fb in (
            (E_COR, FRONT, PARTY_SE), (S_COR, FRONT, PARTY_NW),
            (W_COR, REAR, PARTY_NW), (N_COR, REAR, PARTY_SE),
        )
    ]
    prism("basement", base_poly, 0.0, Z_WT, mats["Toy_steel"])
    path_band("water_table",
              [PARTY_SE.xy(PARTY_SE.length - 0.6, 0.0), E_COR, S_COR,
               PARTY_NW.xy(0.6, 0.0)],
              Z_WT - WT_H, Z_WT + 0.04, -EMBED, SILL_OUT + BASE_PROUD,
              mats["Toy_steel"])

    # 3. the canted bay, through both storeys, on the south-east half.
    prism("bay", BAY_POLY, BAY_Z0, BAY_Z1, mats["Toy_cream"])
    for tag, z in (("lo", Z_SILL1), ("hi", Z_BAYCAP)):
        path_band(f"bay_cap_{tag}", BAY_ARC, z - SILL_H, z + 0.03,
                  -EMBED, SILL_OUT, mats["Toy_steel"])

    # 4. bay glazing: three separate lights per storey (narrow / wide / narrow),
    #    one per bay face. NOT a continuous ribbon - a Victorian bay has three
    #    sashes with solid mullions between them, and a ribbon reads as a
    #    shopfront.
    bay_win = []
    for lvl, (z0, z1) in enumerate(((Z_SILL1 + 0.06, Z_HEAD1),
                                    (Z_BAYCAP + 0.06, Z_HEAD2))):
        for k, f in enumerate(BAY_FACES):
            w = min(0.55, f.length - 0.16) if k != 1 else 1.30
            window(f"baywin{lvl}{k}", f, f.length / 2.0, z0, z1, mats, w)
            bay_win.append((f, f.length / 2.0, w, z0, z1))

    # 5. the flat north-west half of the front: one tall window upstairs, the
    #    twin entries below.
    window("upperwin", FRONT, 5.60, 5.60, Z_HEAD2, mats, 0.90)

    # The entry is built the way every opening in this project is: LAYERED PROUD
    # PANELS, not a hole. A first pass modelled it as a genuine 0.35 m recess -
    # an ink solid sunk into the wall with the doors inside it - and the doors,
    # the transoms and both glow plates ended up buried in the ink block, so the
    # whole entry rendered as one black rectangle. The wall is a closed prism and
    # nothing cuts it; anything meant to be seen has to stand in front of it.
    # Two SEPARATE pockets, not one. A single 3.15 m ink panel across the whole
    # entry zone put a 0.75 m black band between the doors where the real
    # building has a wall pier, and the entry read as one dark slot instead of
    # two front doors.
    for k, t in enumerate(DOOR_T):
        prism(f"entry_pocket{k}",
              FRONT.rect(t - DOOR_W / 2.0 - 0.13, t + DOOR_W / 2.0 + 0.13,
                         -ENT_RECESS, 0.015),
              Z_WT, Z_HOOD0 - 0.05, mats["Toy_ink"])
    for k, t in enumerate(DOOR_T):
        prism(f"door{k}", FRONT.rect(t - DOOR_W / 2.0, t + DOOR_W / 2.0,
                                     0.015, 0.085),
              Z_WT, Z_WT + DOOR_H, mats["Toy_steel"])
        # transom over each door - the two lights that glow at night
        prism(f"transom{k}", FRONT.rect(t - DOOR_W / 2.0, t + DOOR_W / 2.0,
                                        0.015, 0.065),
              Z_WT + DOOR_H + 0.05, Z_WT + DOOR_H + 0.42, mats["Toy_glass"])

    # the hood: one continuous dentilled band over both entries
    hood = [FRONT.xy(ENT_T0 - 0.30, 0.0), FRONT.xy(FRONTAGE, 0.0)]
    path_band("hood", hood, Z_HOOD0, Z_HOOD1, -EMBED, 0.30, mats["Toy_trim"])
    path_band("hood_dentil", hood, Z_HOOD0 - 0.13, Z_HOOD0, -EMBED, 0.19,
              mats["Toy_stone"])

    # 6. the two stoops. Four steps each, the north-west one with a handrail.
    for k, t in enumerate(DOOR_T):
        for s in range(STOOP_STEPS):
            # step 0 is the bottom and the DEEPEST; the top step is a landing
            # 0.30 m deep at the threshold. The first pass had this inverted and
            # the two stoops merged into one grey plinth across the whole front.
            depth = STOOP_D * (STOOP_STEPS - s) / STOOP_STEPS
            prism(f"stoop{k}_{s}",
                  FRONT.rect(t - DOOR_W / 2.0 - 0.09, t + DOOR_W / 2.0 + 0.09,
                             -0.05, depth),
                  0.006, Z_WT * (s + 1) / STOOP_STEPS, mats["Toy_steel"])
    # One rail on the north-west stoop only - the 2025 Street View shows a thin
    # metal handrail there and none on the other. Two posts and a raked bar; at
    # 8.6 m of building the balusters a real rail has are sub-pixel.
    rail_t = DOOR_T[1] + DOOR_W / 2.0 + 0.11
    for k, (d, z0, z1) in enumerate(((0.16, 0.30, Z_WT + 0.50),
                                     (STOOP_D - 0.14, 0.02, 0.98))):
        prism(f"rail_post{k}", FRONT.rect(rail_t, rail_t + 0.06, d, d + 0.06),
              z0, z1, mats["Toy_trim"])
    prism("rail_bar", FRONT.rect(rail_t, rail_t + 0.06, 0.14, STOOP_D - 0.08),
          0.92, Z_WT + 0.50, mats["Toy_trim"])

    # 7. the raised basement's two openings.
    window("bwin", FRONT, BAY_T, 0.52, 1.06, mats, 0.70, sill=False)
    prism("bservice", FRONT.rect(6.05, 6.90, -0.12, BASE_PROUD + 0.01),
          0.18, 1.28, mats["Toy_ink"])

    # 8. the cornice: dentil band, modillion brackets, crown. It steps around
    #    the bay and returns onto both flanks; the rear has none.
    z0, z1, out = CORN_DENTIL
    path_band("cornice_dentil", CORNICE_PATH, z0, z1, -EMBED, out, mats["Toy_stone"])
    z0, z1, out = CORN_CROWN
    path_band("cornice_crown", CORNICE_PATH, z0, z1, -EMBED, out, mats["Toy_trim"])

    # brackets, walked along the cornice path at a fixed pitch so they follow the
    # bay's two angles instead of jumping it
    side = _path_side(CORNICE_PATH)
    seglen = [math.hypot(CORNICE_PATH[i + 1][0] - CORNICE_PATH[i][0],
                         CORNICE_PATH[i + 1][1] - CORNICE_PATH[i][1])
              for i in range(len(CORNICE_PATH) - 1)]
    total = sum(seglen)
    nbr = int(total / BRACKET_PITCH)
    step = total / nbr
    bz0, bz1 = CORN_BRACKET
    for k in range(nbr):
        s = (k + 0.5) * step
        i = 0
        while i < len(seglen) - 1 and s > seglen[i]:
            s -= seglen[i]
            i += 1
        a, b = CORNICE_PATH[i], CORNICE_PATH[i + 1]
        u = ((b[0] - a[0]) / seglen[i], (b[1] - a[1]) / seglen[i])
        nrm = _seg_normal(a, b, side)
        c = (a[0] + u[0] * s, a[1] + u[1] * s)
        hw, dp = BRACKET[0] / 2.0, BRACKET[1]
        poly = [
            (c[0] - u[0] * hw - nrm[0] * EMBED, c[1] - u[1] * hw - nrm[1] * EMBED),
            (c[0] + u[0] * hw - nrm[0] * EMBED, c[1] + u[1] * hw - nrm[1] * EMBED),
            (c[0] + u[0] * hw + nrm[0] * dp, c[1] + u[1] * hw + nrm[1] * dp),
            (c[0] - u[0] * hw + nrm[0] * dp, c[1] - u[1] * hw + nrm[1] * dp),
        ]
        prism(f"bracket_{k}", poly, bz0, bz1, mats["Toy_trim"])

    # 9. the parapet upstand on the rear and the two flanks. The front's parapet
    #    IS the cornice, which is why the crest is only on the street side.
    for nm, f in (("se", PARTY_SE), ("nw", PARTY_NW), ("rear", REAR)):
        path_band(f"upstand_{nm}", [f.xy(0.0, 0.0), f.xy(f.length, 0.0)],
                  Z_DECK - EMBED, Z_PARAPET, -0.22, 0.02, mats["Toy_cream"])

    # 10. the roof. Re-roofed May 2023 ($24,800), so the membrane is clean and
    #     light. The camera looks down and an empty 7.6 x 13.9 m deck is the one
    #     thing the style bible will not forgive; nothing here may approach the
    #     8.60 m crest.
    def rxy(s, u):
        """Roof frame: s metres back from the front wall, u metres across from
        the south-east party wall."""
        return (E_COR[0] - _FN[0] * s + _FT[0] * u, E_COR[1] - _FN[1] * s + _FT[1] * u)

    def rrect(s0, s1, u0, u1):
        return [rxy(s0, u0), rxy(s1, u0), rxy(s1, u1), rxy(s0, u1)]

    # Bulkhead top in Toy_steel, not Toy_ink. A dark roof object on a landmark
    # this small reads as a black hole from the app's downward camera - the
    # recorded failure is a whole roof deck in Toy_roofd rendering rgb(9,9,12).
    # Only the hatch, which is genuinely a dark opening, stays dark.
    prism("roof_bulkhead", rrect(9.6, 11.3, 4.5, 6.3), Z_DECK - EMBED, 8.52,
          mats["Toy_cream"], mats["Toy_steel"])
    prism("roof_hatch", rrect(7.4, 8.4, 1.1, 2.1), Z_DECK - EMBED, Z_DECK + 0.26,
          mats["Toy_ink"])
    # the chimney the 2008 permit implies: two fireplaces removed, their
    # "chimneys 1/2 way back on side"
    prism("chimney", rrect(6.6, 7.2, 0.35, 0.95), Z_DECK - EMBED, 8.42,
          mats["Toy_stone"])
    prism("chimney_cap", rrect(6.5, 7.3, 0.28, 1.02), 8.42 - EMBED, 8.54,
          mats["Toy_ink"])
    # A 7.6 x 13.9 m membrane deck is the largest single surface the app's
    # downward camera sees on this asset, and an empty slab is what the style
    # bible will not forgive. Everything added here is what a re-roofed flat
    # deck actually carries: welded seams every 2.2 m, a walk pad from the
    # bulkhead to the hatch, and two drains at the low (rear) corners. No solar,
    # no deck furniture, no planters - there is no evidence for any of it.
    for k in range(6):
        sv = 1.9 + k * 2.2
        prism(f"roof_seam{k}", rrect(sv, sv + 0.09, 0.35, FRONTAGE - 0.35),
              Z_DECK - EMBED, Z_DECK + 0.035, mats["Toy_steel"])
    prism("roof_walkpad", rrect(8.0, 9.8, 1.35, 1.95), Z_DECK - EMBED,
          Z_DECK + 0.05, mats["Toy_stone"])
    prism("roof_walkpad2", rrect(9.4, 10.0, 1.35, 4.6), Z_DECK - EMBED,
          Z_DECK + 0.05, mats["Toy_stone"])
    for k, (sv, u) in enumerate(((13.1, 0.75), (13.1, 6.85))):
        prism(f"roof_drain{k}", rrect(sv, sv + 0.45, u - 0.22, u + 0.22),
              Z_DECK - 0.10, Z_DECK + 0.02, mats["Toy_ink"])
    for k, (sv, u) in enumerate(((4.6, 6.4), (5.4, 6.8), (11.9, 1.6))):
        p = rxy(sv, u)
        r = 0.12
        poly = [(p[0] + r * math.cos(2 * math.pi * i / 6),
                 p[1] + r * math.sin(2 * math.pi * i / 6)) for i in range(6)]
        prism(f"roof_vent{k}", poly, Z_DECK - EMBED, Z_DECK + 0.55, mats["Toy_trim"])

    # 10b. the two chimney breasts. The 2008 permit removed two fireplaces and
    #      describes their "chimneys 1/2 way back on side", which is exactly
    #      where a 1915 two-flat carries them: a shallow pilaster on each party
    #      wall, half the depth back. They are the only event on either flank,
    #      and the north-west one earns its place - 246 Ritch next door is
    #      15.87 m against this building's 8.6, so that wall is genuinely
    #      exposed in the app and a blank 13.9 x 8 m slab is not a designed
    #      surface. No windows are invented to go with them: unlike 550 Third,
    #      no permit here records property-line windows.
    for nm, f, s0 in (("se", PARTY_SE, 6.55), ("nw", PARTY_NW, 6.30)):
        prism(f"breast_{nm}", f.rect(s0, s0 + 0.95, -EMBED, 0.22),
              0.20, Z_SPRING + 0.10, mats["Toy_cream"])
    prism("chimney_nw", PARTY_NW.rect(6.45, 7.25, -0.05, 0.30), Z_DECK - EMBED,
          8.30, mats["Toy_stone"])
    prism("chimney_nw_cap", PARTY_NW.rect(6.38, 7.32, -0.05, 0.37), 8.30 - EMBED,
          8.42, mats["Toy_ink"])

    # 11. the rear elevation. Nothing observed it; the 2008 permit put vinyl
    #     siding on the back of #250 only, "not visible from the street", so it
    #     is utilitarian, not designed. Three modest openings and a door.
    window("rearwin0", REAR, 2.10, 4.90, 6.60, mats, 0.85)
    window("rearwin1", REAR, 5.50, 4.90, 6.60, mats, 0.85)
    window("rearwin2", REAR, 2.10, 2.30, 3.90, mats, 0.85)
    prism("rear_door", REAR.rect(5.05, 5.95, -0.10, 0.04), Z_WT, Z_WT + 2.10,
          mats["Toy_ink"])
    prism("rear_stair", REAR.rect(4.70, 6.30, -0.05, 1.35), 0.006, Z_WT + 0.10,
          mats["Toy_steel"])

    # 12. night state: the six bay panes and the two door transoms. Uneven on
    #     purpose - two flats, not an office floor. Single-layer plates only.
    for i, (f, t_c, w, z0, z1) in enumerate(bay_win):
        # The name matters: the validator routes anything containing "_glow" to
        # the open-strip test (is this single face the first thing a ray fired
        # along its own normal hits?) instead of the signed-volume test, which
        # is meaningless for a one-quad object. Named "bayglow" without the
        # underscore, these six plates skipped that check entirely and were
        # scored - accidentally, on the sign of a degenerate volume - as closed
        # solids.
        glow_plate(f"bay_glow{i}", f, t_c - w / 2.0 + 0.04, t_c + w / 2.0 - 0.04,
                   z0 + 0.05, z1 - 0.05, mats["Toy_glassl_Glow"], GLASS_PROUD)
    for k, t in enumerate(DOOR_T):
        glow_plate(f"transom_glow{k}", FRONT, t - DOOR_W / 2.0 + 0.05,
                   t + DOOR_W / 2.0 - 0.05, Z_WT + DOOR_H + 0.09,
                   Z_WT + DOOR_H + 0.38, mats["Toy_glassl_Glow"], 0.10)

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.10/2. Frames, sills, bands, brackets and glow plates are small and
    # numerous - a token softening or none at all is what keeps this under cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        n = obj.name
        if "glow" in n or "_glass" in n or "_jamb" in n or "_head" in n \
                or n.endswith("_sill") or n.startswith(("bracket_", "roof_vent",
                                                        "cornice_", "hood",
                                                        "upstand_", "water_table",
                                                        "bay_cap_", "roof_seam",
                                                        "roof_walkpad", "rail_")):
            continue
        if n.startswith(("stoop", "transom", "door", "handrail", "chimney_cap")):
            bevel(obj, width=0.04, segments=1)
        else:
            bevel(obj)

    recentre()
    return scene


# Metres east / north from DESIGN_ANCHOR to the model's XY bbox centre, filled in
# by recentre(). The manifest anchor is DESIGN_ANCHOR moved by this vector, so the
# origin sits at the bbox centre (contract rule 2) while the building still lands
# on its real footprint. The shift here is small but not zero: the two stoops
# project 1.20 m past the street wall onto the pavement, exactly as they do in
# the real city, and they pull the bbox centre north-east.
ANCHOR_SHIFT = [0.0, 0.0]


def recentre():
    mn = Vector((1e9, 1e9))
    mx = Vector((-1e9, -1e9))
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    for o in meshes:
        for v in o.data.vertices:
            for i in range(2):
                mn[i] = min(mn[i], v.co[i])
                mx[i] = max(mx[i], v.co[i])
    cx, cy = (mn[0] + mx[0]) / 2.0, (mn[1] + mx[1]) / 2.0
    ANCHOR_SHIFT[0], ANCHOR_SHIFT[1] = cx, cy
    for o in meshes:
        for v in o.data.vertices:
            v.co.x -= cx
            v.co.y -= cy


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
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    lon = DESIGN_ANCHOR[0] + ANCHOR_SHIFT[0] / LON_M
    lat = DESIGN_ANCHOR[1] + ANCHOR_SHIFT[1] / LAT_M
    print(f"[build] wall box: {FRONTAGE:.2f} x {DEPTH:.2f} m = {FRONTAGE * DEPTH:.1f} m2")
    print(f"[build] design (built-quad centre) anchor: {DESIGN_ANCHOR}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] front faces {FRONT.heading:.2f} deg; NW party {PARTY_NW.heading:.2f}; "
          f"SE party {PARTY_SE.heading:.2f}; rear {REAR.heading:.2f}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "248-ritch.blend")
    glb = os.path.join(out, "248-ritch.glb")
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
