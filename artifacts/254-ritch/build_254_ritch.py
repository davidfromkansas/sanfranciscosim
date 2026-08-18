"""Deterministic Blender build of the SF-SIM miniature 252-254 Ritch Street.

    blender -b --python build_254_ritch.py -- [--out DIR]

Writes 254-ritch.blend and 254-ritch.glb next to this file (or into --out).
Geometry is authored in world space in metres, Z up, +X east, +Y north, so the
model drops into the city at its real-world heading - the loader applies no
rotation. Origin = model XY bbox centre, min Z = 0, roof flue cap exactly 8.80 m.

Design (see REFERENCE.md for the sources behind every number):

* a 1915 two-flat on Ritch Street, one of the SoMa alleys between Bryant and
  Brannan. 7.60 m of frontage, 14.2 m deep, two storeys over a raised base,
  flat roof. Assessor block 3776 lot 106, address range 252-254: one parcel,
  one building, two front doors;
* the recognition rests on COLOUR. Every painted surface - siding, base, bay,
  cornice, doors, stoop - is one dark warm grey (#756f69). The neighbour at
  248-250 is cream, and so is most of the block. From the app's aerial camera
  this is "the dark house in the row" and nothing else about it matters as much;
* the south-east 3.68 m of the frontage is a two-storey canted bay, three
  sashes per storey. The north-west 2.28 m carries one upper window and, at
  ground level, a recessed entry holding TWO doors (254 south-east, 252
  north-west) under a small bracketed hood, reached by a six-step stoop;
* the south-east flank is EXPOSED - the lot next door is a surface parking lot -
  so three of the four elevations are public. Only the north-west party wall
  against 248-250 is blind;
* the roof is the other half of the asset. Flat, and a pale membrane clearly
  LIGHTER than the walls, which is the real relationship and also what makes the
  outline read from directly overhead. Two light wells cut through it (one
  against the party wall, one notched into the exposed flank), a small
  mechanical cluster sits mid-roof, and a capped flue near the party wall is the
  tallest thing on the building;
* heights: LiDAR median 8.04 m (roof deck), LiDAR maximum 8.81 m (the flue).
  A photogrammetric check on the straight-on listing elevation, scaled off the
  7.60 m frontage, put the roof edge at 7.8 m and agreed with the design section
  at the floor line, the upper sill and the upper head to within 5 cm;
* night state: the three upper bay sashes lit warm plus a spill in the entry
  recess. The single north-west upper window stays dark - the upper unit was
  vacant at the 2025 sale and a fully lit two-flat reads as an office. Glow
  surfaces are single faces standing proud of the opaque glazing, never closed
  shells: the app renders _Glow in a separate layer and a closed shell is two
  alpha layers deep, so it reads far brighter by day than intended.

Authoring frame: the footprint is a clean rectangle at 45.05 deg to the world
axes, so everything is placed through Face frames built from the four measured
wall-box corners. Because the building sits at 45 deg the axis-aligned XY
bounding box is ~15.8 x 15.8 m even though the building is 7.60 x 14.2 m. That
is expected, not a scale error.
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

# Centre of the measured wall box - the plan's design anchor, before recentring.
# Placed in the DataSF FOOTPRINT frame, not the surveyed parcel frame: both
# DataSF footprints on this pair of lots sit ~1.2 m north-west of the parcels,
# in step with each other, and 248-250 stays baked from its footprint. Anchoring
# on the parcel would open a 1.2 m slot between this asset's party wall and its
# neighbour's, which is the one error the aerial camera would actually see.
# See docs/asset-plans/254-ritch.md 2.3.
DESIGN_ANCHOR = (-122.3956361, 37.7801244)

FRONTAGE = 7.60            # surveyed parcel width (25 ft)
DEPTH = 14.20              # DataSF LiDAR depth, front wall read 1.00 m behind
                           # the property line and the LiDAR's 0.64 m front
                           # extent read as the cornice overhang
FRONT_BEARING = 45.05      # the Ritch Street elevation faces north-east
FLANK_BEARING = 135.05     # the exposed flank faces south-east (parking lot)

Z_BASE = 1.35              # top of the raised base band / porch floor
Z_FLOOR = 4.30             # floor line, and the crest of the entry hood
Z_WALL = 7.45              # cornice springing
Z_DECK = 7.95              # flat roof deck - MEASURED (LiDAR median 8.04 m)
Z_CREST = 8.05             # cornice crest
Z_CURB = 8.20              # light-well curbs
Z_MECH = 8.50              # condenser on its stand
Z_TOP = 8.80               # roof flue cap - MEASURED (LiDAR hgt_max 8.81 m) and
                           # the bbox top, so the loader's targetHeightM /
                           # measuredHeight lands on exactly 1.0

BASE_PROUD = 0.06

# Front layout, t metres from the NORTH-WEST (party) corner, read off the
# straight-on listing elevation with the 7.60 m frontage as the scale bar.
ENT_T0, ENT_T1 = 0.37, 2.65        # entry recess
ENT_D = 0.30                       # how far the recess reads back from the wall
UPWIN_T, UPWIN_W = 1.70, 1.10      # the single upper window over the entry
BAY_T0, BAY_T1 = 3.33, 7.01        # canted bay
BAY_PROJ = 0.60                    # 45 deg cheeks, so each cheek runs 0.60 in t

# Openings.
WIN_H = 1.70
SILL_LO, SILL_UP = 2.05, 5.15      # ground and upper sills
WIN_RECESS = 0.12
FRAME_PROUD = 0.08
BAY_SASH_CHEEK = 0.55
BAY_SASH_FACE = 1.40

DOOR_W, DOOR_H = 0.88, 2.15
HOOD_Z0, HOOD_Z1 = 3.95, Z_FLOOR
HOOD_PROUD = 0.20

STOOP_W = 1.60
STOOP_T = 1.51                     # centred on the entry recess
STOOP_STEPS = 6
STOOP_RUN = 0.30
STOOP_CHEEK = 0.20

CORN_Z = (Z_WALL, 7.65, 7.85, Z_CREST)
CORN_OUT = (0.12, 0.24, 0.35)
CORN_RETURN = 0.35                 # how far the cornice turns each flank

# Roof, in the roof frame: s metres back from the front wall, u metres across
# from the north-west party wall. Both wells and the mechanical cluster are
# measured off the top-down drone frame against the 14.2 m roof as a scale bar.
WELL_A = (7.00, 8.10, 0.00, 2.10)  # against the party wall
WELL_B = (4.20, 7.80, 6.20, 7.60)  # notched into the exposed flank
WELL_LINER_Z = (4.60, 7.30)
WELL_LINER_INSET = 0.06
CURB_W = 0.20

MECH_S, MECH_U = (6.10, 7.80), (3.30, 4.30)
FLUE_S, FLUE_U, FLUE_R = 9.00, 0.55, 0.175

EMBED = 0.03               # how far every applied band is sunk INTO the surface
                           # it sits on. Nothing here is allowed to have a face
                           # exactly coincident with another solid's face:
                           # coincident faces make the first-hit direction of a
                           # ray ambiguous and the contract's normals ray test
                           # counts the ambiguity as a flipped face. Overlapping
                           # solids are the supported model - the validator's
                           # authoritative normals test is per-object signed
                           # volume.

BEVEL_W, BEVEL_SEG = 0.10, 2

PALETTE_HEX = {
    "Toy_slate": "756f69",   # EVERY painted surface: siding on all four
                             # elevations, base band, bay, both cornices, the
                             # doors, the entry hood, the stoop, window
                             # surrounds. OFF-PALETTE (a WARN, not a fail) and
                             # deliberate - this is the style bible's SF
                             # painted-residential exception. The facade
                             # median-samples at #6b696a in overcast light and
                             # #5e5652 in shade; this is that colour lifted ~8%
                             # so it survives the app's Lambert shading. No
                             # palette entry is usable: Toy_steel (9aa0a6) is far
                             # too light and destroys the one cue this building
                             # has, and Toy_roofd (45454a) has already been
                             # observed rendering as rgb(9,9,12) - effectively
                             # black - on a roof deck in this app. If the aerial
                             # render still reads muddy, lift toward 857e76;
                             # never go darker.
    "Toy_stone": "d9d2c2",   # the roof membrane and the light-well curbs. The
                             # roof is LIGHTER than the walls. That is the real
                             # relationship (measured #cac8c9 overcast against
                             # #6b696a walls) and it is also what makes the
                             # outline read from directly overhead. Do not
                             # "correct" it to a dark roof colour.
    "Toy_ink": "3a3530",     # entry recess lining, both light-well shafts, the
                             # rear door reveal
    "Toy_glass": "2a4d73",   # all glazing
    "Toy_steel": "9aa0a6",   # roof flue, condenser, vent, equipment box
    "Toy_gold_Glow": "caa64a",   # the three upper bay sashes at night. The app
                             # draws _Glow in a separate UNLIT layer, so at
                             # night the surface shows its raw base colour -
                             # Toy_glass_Glow (2a4d73) would render a dark
                             # window pretending to be a lit one.
    "Toy_trim_Glow": "f6e6c4",   # the warm spill in the entry recess
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


_FN = _brg(FRONT_BEARING)             # outward from the street elevation (NE)
_FT = _brg(FRONT_BEARING + 90.0)      # along the front, NW corner -> SE corner

NW_F = (_FN[0] * DEPTH / 2.0 - _FT[0] * FRONTAGE / 2.0,
        _FN[1] * DEPTH / 2.0 - _FT[1] * FRONTAGE / 2.0)
SE_F = (NW_F[0] + _FT[0] * FRONTAGE, NW_F[1] + _FT[1] * FRONTAGE)
SE_R = (SE_F[0] - _FN[0] * DEPTH, SE_F[1] - _FN[1] * DEPTH)
NW_R = (NW_F[0] - _FN[0] * DEPTH, NW_F[1] - _FN[1] * DEPTH)

BOX = [NW_F, SE_F, SE_R, NW_R]
CX = sum(p[0] for p in BOX) / 4.0
CY = sum(p[1] for p in BOX) / 4.0


class Face:
    """A local frame on one elevation: t runs along the face from `a` to `b`,
    d runs OUTWARD (away from the footprint centroid), z is world up."""

    def __init__(self, a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        self.a, self.b, self.length = a, b, n
        self.t = (dx / n, dy / n)
        nrm = (-self.t[1], self.t[0])
        if (a[0] + nrm[0] - CX) ** 2 + (a[1] + nrm[1] - CY) ** 2 < (a[0] - CX) ** 2 + (
            a[1] - CY
        ) ** 2:
            nrm = (-nrm[0], -nrm[1])
        self.n = nrm
        self.heading = (math.degrees(math.atan2(nrm[0], nrm[1])) + 360.0) % 360.0

    def xy(self, t, d):
        return (self.a[0] + self.t[0] * t + self.n[0] * d,
                self.a[1] + self.t[1] * t + self.n[1] * d)

    def rect(self, t0, t1, d0, d1):
        return [self.xy(t0, d0), self.xy(t1, d0), self.xy(t1, d1), self.xy(t0, d1)]


FRONT = Face(NW_F, SE_F)     # Ritch Street, faces 45.05
FLANK = Face(SE_F, SE_R)     # the parking lot, faces 135.05 - EXPOSED
REAR = Face(SE_R, NW_R)      # the rear yard, faces 225.05
PARTY = Face(NW_R, NW_F)     # 248-250 Ritch, faces 315.05 - blind


def roof_xy(s, u):
    """Roof frame: s metres back from the front wall, u metres across from the
    north-west party wall."""
    return (NW_F[0] - _FN[0] * s + _FT[0] * u, NW_F[1] - _FN[1] * s + _FT[1] * u)


def roof_rect(s0, s1, u0, u1):
    return [roof_xy(s0, u0), roof_xy(s1, u0), roof_xy(s1, u1), roof_xy(s0, u1)]


def footprint():
    """The wall box with both light wells bitten out of it, walked clockwise in
    the roof frame: front edge, exposed flank (with well B), rear, party wall
    (with well A). One simple polygon, so the top cap IS the roof plane with its
    two holes already in it."""
    sA0, sA1, uA0, uA1 = WELL_A
    sB0, sB1, uB0, uB1 = WELL_B
    return [
        roof_xy(0.0, 0.0),                    # NW front corner
        roof_xy(0.0, FRONTAGE),               # SE front corner
        roof_xy(sB0, FRONTAGE),               # down the exposed flank...
        roof_xy(sB0, uB0),                    # ...into well B
        roof_xy(sB1, uB0),
        roof_xy(sB1, FRONTAGE),               # ...and back out
        roof_xy(DEPTH, FRONTAGE),             # SE rear corner
        roof_xy(DEPTH, 0.0),                  # NW rear corner
        roof_xy(sA1, 0.0),                    # up the party wall...
        roof_xy(sA1, uA1),                    # ...into well A
        roof_xy(sA0, uA1),
        roof_xy(sA0, 0.0),                    # ...and back out
    ]


def bay_polyline():
    """The canted bay's outer run on the front face: wall, cheek, face, cheek,
    wall. Used both as the bay's own plan and, spliced into the front line, as
    the path the main cornice follows."""
    return [
        FRONT.xy(BAY_T0, 0.0),
        FRONT.xy(BAY_T0 + BAY_PROJ, BAY_PROJ),
        FRONT.xy(BAY_T1 - BAY_PROJ, BAY_PROJ),
        FRONT.xy(BAY_T1, 0.0),
    ]


def cornice_polyline():
    """The whole street elevation as one open polyline, with the bay spliced in
    and a short return onto each flank."""
    return ([FRONT.xy(-CORN_RETURN, -CORN_RETURN), FRONT.xy(-CORN_RETURN, 0.0)]
            + [FRONT.xy(0.0, 0.0)] + bay_polyline()
            + [FRONT.xy(FRONTAGE, 0.0),
               FRONT.xy(FRONTAGE + CORN_RETURN, 0.0),
               FRONT.xy(FRONTAGE + CORN_RETURN, -CORN_RETURN)])


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


def ring_band(name, outer, inset, z0, z1, mat):
    """A closed rectangular band between `outer` and its inward offset. Used for
    the light-well curbs: three overlapping boxes meeting at the corners left
    coincident faces that rendered as black squares from the aerial camera."""
    n = len(outer)
    cx = sum(p[0] for p in outer) / n
    cy = sum(p[1] for p in outer) / n
    inner = []
    for x, y in outer:
        dx, dy = cx - x, cy - y
        m = math.hypot(dx, dy) or 1e-9
        inner.append((x + dx / m * inset * math.sqrt(2.0),
                      y + dy / m * inset * math.sqrt(2.0)))
    verts = [(x, y, z0) for x, y in outer] + [(x, y, z0) for x, y in inner]
    verts += [(x, y, z1) for x, y in outer] + [(x, y, z1) for x, y in inner]
    O0, I0, O1, I1 = 0, n, 2 * n, 3 * n
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces += [(O0 + i, O0 + j, O1 + j, O1 + i),
                  (I0 + j, I0 + i, I1 + i, I1 + j),
                  (O0 + j, O0 + i, I0 + i, I0 + j),
                  (O1 + i, O1 + j, I1 + j, I1 + i)]
    return new_mesh(name, verts, faces, [mat], recalc=False)


def disc(name, cx, cy, z0, z1, r, segs, mat):
    poly = [(cx + r * math.cos(2 * math.pi * i / segs),
             cy + r * math.sin(2 * math.pi * i / segs)) for i in range(segs)]
    return prism(name, poly, z0, z1, mat)


def _polyline_side(pts):
    """Decide, ONCE for a whole open polyline, which side is outward. Every
    polyline here faces within 45 deg of the front normal, so the handedness is
    constant along it - but it must not be taken per segment from the footprint
    centroid, which is the trap that folds bands at corner geometry. The MIDDLE
    segment always faces squarely out, so the handedness comes from that one."""
    i = max(0, (len(pts) - 1) // 2)
    a, b = pts[i], pts[i + 1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    mid = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
    return 1.0 if (-dy) * (mid[0] - CX) + dx * (mid[1] - CY) > 0.0 else -1.0


def polyline_offset(pts, d, side=None):
    """Offset an OPEN polyline by `d` metres along each segment's outward normal,
    re-intersecting neighbouring segments."""
    n = len(pts)
    if side is None:
        side = _polyline_side(pts)
    lines = []
    for i in range(n - 1):
        a, b = pts[i], pts[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy) or 1e-9
        u = (dx / m, dy / m)
        nrm = (-u[1] * side, u[0] * side)
        lines.append(((a[0] + nrm[0] * d, a[1] + nrm[1] * d), u))
    out = [lines[0][0]]
    for i in range(1, n - 1):
        (p0, u0), (p1, u1) = lines[i - 1], lines[i]
        den = u0[0] * u1[1] - u0[1] * u1[0]
        if abs(den) < 1e-9:
            out.append(p1)
            continue
        t = ((p1[0] - p0[0]) * u1[1] - (p1[1] - p0[1]) * u1[0]) / den
        q = (p0[0] + u0[0] * t, p0[1] + u0[1] * t)
        # Spike guard: at a reflex vertex the two offset lines meet far away and
        # the intersection shoots off into a sail. Cap it at 1.3x the offset.
        v = (q[0] - pts[i][0], q[1] - pts[i][1])
        m = math.hypot(v[0], v[1])
        cap = abs(d) * 1.30 + 1e-6
        if m > cap:
            q = (pts[i][0] + v[0] * cap / m, pts[i][1] + v[1] * cap / m)
        out.append(q)
    a, b = pts[-2], pts[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    m = math.hypot(dx, dy) or 1e-9
    u = (dx / m, dy / m)
    nrm = (-u[1] * side, u[0] * side)
    out.append((b[0] + nrm[0] * d, b[1] + nrm[1] * d))
    return out


def arc_band(name, pts, z0, z1, d0, d1, mat):
    """A closed solid swept along an OPEN polyline: the cross-section is the
    rectangle (d0..d1) x (z0..z1), where d is measured outward from the wall."""
    side = _polyline_side(pts)
    a = polyline_offset(pts, d0, side)
    b = polyline_offset(pts, d1, side)
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


def glow_quad(name, p0, p1, z0, z1, mat, proud):
    """ONE outward-facing quad standing `proud` metres off the segment p0->p1.

    Night glow must never be a closed shell. The app draws _Glow in a separate
    layer that is translucent by day, so a closed box shows its front AND back
    face and reads at roughly twice the intended day alpha - enough to tint a
    whole facade. One single-sided quad is the correct construction, and the
    winding is set explicitly (never recalculated) so the face points out."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    m = math.hypot(dx, dy) or 1e-9
    nx, ny = dy / m, -dx / m
    mid = ((p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0)
    a, b = p0, p1
    if nx * (mid[0] - CX) + ny * (mid[1] - CY) < 0.0:
        a, b = p1, p0
        nx, ny = -nx, -ny
    a2 = (a[0] + nx * proud, a[1] + ny * proud)
    b2 = (b[0] + nx * proud, b[1] + ny * proud)
    verts = [(a2[0], a2[1], z0), (b2[0], b2[1], z0),
             (b2[0], b2[1], z1), (a2[0], a2[1], z1)]
    return new_mesh(name, verts, [(0, 1, 2, 3)], [mat], recalc=False)


def bevel(obj, width=BEVEL_W, segments=BEVEL_SEG):
    """Miniature-style edge softening (style bible s.4). The offset is capped at
    a third of the object's thinnest dimension: glass fills, frames and glow
    shells are only 20-160 mm thick and a full bevel on those collapses opposing
    profiles into zero-area slivers even with clamp_overlap."""
    thin = min((d for d in obj.dimensions if d > 1e-6), default=width)
    offset = min(width, thin * 0.30)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(bm, geom=list(bm.verts) + list(bm.edges), offset=offset,
                    segments=segments, profile=0.5, affect="EDGES",
                    clamp_overlap=True)
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-4)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-4, edges=list(bm.edges))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


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


def window(name, face, t_c, z_sill, mats, w, h=WIN_H, d=0.0):
    """A recessed opening with a proud sill and surround. `d` shifts the whole
    module outward, for openings that sit on the bay rather than the wall."""
    t0, t1 = t_c - w / 2.0, t_c + w / 2.0
    prism(f"{name}_fill", face.rect(t0, t1, d - WIN_RECESS, d + 0.02),
          z_sill, z_sill + h, mats["Toy_glass"])
    prism(f"{name}_sill", face.rect(t0 - 0.10, t1 + 0.10, d - EMBED, d + FRAME_PROUD),
          z_sill - 0.10, z_sill, mats["Toy_slate"])
    prism(f"{name}_head", face.rect(t0 - 0.10, t1 + 0.10, d - EMBED, d + FRAME_PROUD),
          z_sill + h, z_sill + h + 0.10, mats["Toy_slate"])
    for k, (a, b) in enumerate(((t0 - 0.10, t0), (t1, t1 + 0.10))):
        prism(f"{name}_jamb{k}", face.rect(a, b, d - EMBED, d + FRAME_PROUD * 0.7),
              z_sill, z_sill + h, mats["Toy_slate"])


# --------------------------------------------------------------------- build


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"
    mats = {k: make_material(k) for k in PALETTE_HEX}

    fp = footprint()

    # 1. main volume. The top cap IS the roof plane, with both light wells
    #    already bitten out of the plan, so the wells are real holes rather
    #    than painted rectangles.
    prism("body", fp, 0.0, Z_DECK, mats["Toy_slate"], mats["Toy_stone"])

    # 2. raised base band, proud, on the three public elevations only - it must
    #    not push 60 mm into the neighbour on the party side.
    for nm, f in (("front", FRONT), ("flank", FLANK), ("rear", REAR)):
        prism(f"base_{nm}", f.rect(0.0, f.length, -EMBED, BASE_PROUD), 0.0, Z_BASE,
              mats["Toy_slate"])

    # 3. the canted bay: two storeys, carried on a flared skirt that dies into
    #    the base band.
    bay = bay_polyline()
    bay_closed = bay + [FRONT.xy(BAY_T1, -0.30), FRONT.xy(BAY_T0, -0.30)]
    prism("bay", bay_closed, Z_BASE - 0.25, Z_WALL, mats["Toy_slate"])
    arc_band("bay_skirt", bay, Z_BASE - 0.25, Z_BASE + 0.20, -EMBED, 0.09,
             mats["Toy_slate"])
    arc_band("bay_cornice", bay, 7.20, Z_WALL, -EMBED, 0.10, mats["Toy_slate"])

    # bay glazing: three sashes per storey - a narrow one on each 45 deg cheek
    # and a wide one on the front face.
    for si, z_sill in enumerate((SILL_LO, SILL_UP)):
        for k in range(3):
            p0, p1 = bay[k], bay[k + 1]
            w = BAY_SASH_FACE if k == 1 else BAY_SASH_CHEEK
            seg = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
            f = (1.0 - w / seg) / 2.0
            a = (p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)
            b = (p0[0] + (p1[0] - p0[0]) * (1.0 - f), p0[1] + (p1[1] - p0[1]) * (1.0 - f))
            sub = Face(a, b)
            window(f"baywin{si}{k}", sub, sub.length / 2.0, z_sill, mats, w=w)
            if si == 1:
                glow_quad(f"baywin{si}{k}_glow", a, b, z_sill, z_sill + WIN_H,
                          mats["Toy_gold_Glow"], 0.05)

    # 4. the north-west third of the frontage: one upper window, and the entry.
    window("upwin", FRONT, UPWIN_T, SILL_UP, mats, w=UPWIN_W)   # NOT lit at night

    # The dark field of the recess. Its outer face stands only 5 mm proud of the
    # wall - just enough to be visible without a boolean cut - and the door
    # slabs then stand 15 mm proud of IT, which is what makes two doors read
    # inside one dark opening. An earlier pass had this block ending 20 mm proud
    # and the doors sitting behind it; the whole entry rendered as one flat
    # rectangle. See REPORT.md 1.
    prism("entry_recess", FRONT.rect(ENT_T0, ENT_T1, -ENT_D, 0.005), Z_BASE, HOOD_Z0,
          mats["Toy_ink"])
    # A porch light over the doors, not a lit doorway. Sized as one transom
    # band: at full doorway size this read as a white slab that swallowed the
    # entry and was brighter than the two lit rooms above it. See REPORT.md 5.
    glow_quad("entry_glow", FRONT.xy(ENT_T0 + 0.30, 0.0), FRONT.xy(ENT_T1 - 0.30, 0.0),
              Z_BASE + 2.25, Z_BASE + 2.55, mats["Toy_trim_Glow"], 0.035)
    # The two doors are held apart and in from the reveals so the dark field
    # of the recess shows between and around them. At the plan's 1.00 m width
    # they left 40 mm of ink between and the entry read as a flush pair of
    # panels rather than a hole. See REPORT.md 4.
    for k, t_c in enumerate((ENT_T0 + 0.58, ENT_T1 - 0.58)):
        t0, t1 = t_c - DOOR_W / 2.0, t_c + DOOR_W / 2.0
        prism(f"door{k}", FRONT.rect(t0, t1, -ENT_D + 0.04, 0.020),
              Z_BASE, Z_BASE + DOOR_H, mats["Toy_slate"])
        prism(f"door{k}_light", FRONT.rect(t0 + 0.22, t1 - 0.22, -0.06, 0.035),
              Z_BASE + 1.10, Z_BASE + 1.85, mats["Toy_glass"])
    prism("entry_hood", FRONT.rect(ENT_T0 - 0.14, ENT_T1 + 0.14, -EMBED, HOOD_PROUD),
          HOOD_Z0, HOOD_Z1, mats["Toy_slate"])

    # 5. the stoop: six treads and one solid cheek wall on the south-east side.
    rise = Z_BASE / STOOP_STEPS
    for k in range(STOOP_STEPS):
        d1 = (STOOP_STEPS - k) * STOOP_RUN
        prism(f"stoop{k}",
              FRONT.rect(STOOP_T - STOOP_W / 2.0, STOOP_T + STOOP_W / 2.0, -EMBED, d1),
              0.0, (k + 1) * rise, mats["Toy_slate"])
    prism("stoop_cheek",
          FRONT.rect(STOOP_T + STOOP_W / 2.0, STOOP_T + STOOP_W / 2.0 + STOOP_CHEEK,
                     -EMBED, STOOP_STEPS * STOOP_RUN),
          0.0, Z_BASE + 0.10, mats["Toy_slate"])

    # 6. the cornice: three corbelled steps following the front line with the
    #    bay spliced in, returning half a metre onto each flank. This is the one
    #    piece of ornament on the building; the real dentil course and modillion
    #    blocks are sub-pixel at this scale, so what has to read is the
    #    PROJECTION, not the blocks.
    cp = cornice_polyline()
    for k in range(3):
        arc_band(f"cornice{k}", cp, CORN_Z[k], CORN_Z[k + 1] + (0.0 if k == 2 else EMBED),
                 -EMBED, CORN_OUT[k], mats["Toy_slate"])

    # 7. floor-line shadow groove on the two elevations that are seen.
    for nm, f in (("front", FRONT), ("flank", FLANK)):
        prism(f"groove_{nm}", f.rect(0.0, f.length, -0.05, 0.01),
              Z_FLOOR - 0.04, Z_FLOOR, mats["Toy_ink"])

    # 8. the roof. Both wells get a dark liner sunk below the deck so they read
    #    as holes rather than painted rectangles from directly overhead, and a
    #    pale curb on their roof-side edges - which is what the drone frame
    #    actually shows.
    # A light well is an UPPER-STOREY shaft, not a slot to the ground: the plan
    # bite that puts the hole in the roof runs the whole height of the wall, so
    # each well is plugged back to solid below the shaft. Without this the
    # exposed flank rendered as a two-storey canyon and the party wall as a gash.
    # See REPORT.md 2.
    # Each plug stops at the screen's inner face rather than at the wall plane.
    # Running it all the way out left the plug's outer face exactly coplanar with
    # the screen's over the lower storey, and two coincident faces z-fought into
    # a mottled ghost rectangle on the exposed flank. See REPORT.md 3.
    for nm, (s0, s1, u0, u1) in (("a", WELL_A), ("b", WELL_B)):
        pu0 = u0 + 0.25 if nm == "a" else u0
        pu1 = u1 if nm == "a" else u1 - 0.25
        prism(f"well_{nm}_plug", roof_rect(s0, s1, pu0, pu1), 0.0,
              WELL_LINER_Z[0] + 0.10, mats["Toy_slate"])
        i = WELL_LINER_INSET
        prism(f"well_{nm}_liner",
              roof_rect(s0 + i, s1 - i, u0 + i, u1 - i),
              WELL_LINER_Z[0], WELL_LINER_Z[1], mats["Toy_ink"])
    # Both mouths are screened, so each well is an interior shaft read only from
    # above. The party wall has to stay a clean plane so the two roofs abut; the
    # exposed flank photographs as an unbroken wall, and left open the 3.6 x 1.4 m
    # bite read from the aerial camera as a garage door. See REPORT.md 3.
    prism("well_a_screen", roof_rect(WELL_A[0], WELL_A[1], 0.0, 0.25), 0.0, Z_DECK,
          mats["Toy_slate"])
    prism("well_b_screen", roof_rect(WELL_B[0], WELL_B[1], FRONTAGE - 0.25, FRONTAGE),
          0.0, Z_DECK, mats["Toy_slate"])
    c = CURB_W
    for nm, (s0, s1, u0, u1) in (("a", WELL_A), ("b", WELL_B)):
        ring_band(f"curb_{nm}", roof_rect(s0 - c, s1 + c, u0 - c, u1 + c), c,
                  Z_DECK - EMBED, Z_CURB, mats["Toy_stone"])

    # A low upstand on the flank and the rear, where the street cornice does not
    # reach. A flat SF roof is a tray, not a slab, and without this the roof edge
    # read as a bare sheet from the aerial camera.
    for nm, f in (("flank", FLANK), ("rear", REAR)):
        prism(f"parapet_{nm}", f.rect(0.0, f.length, -0.10, 0.03), Z_DECK - EMBED,
              Z_DECK + 0.16, mats["Toy_slate"])

    # mechanical cluster: mini-split condenser on a low stand, one mushroom vent
    # and a small equipment box. Nothing here may approach the flue.
    prism("mech_stand", roof_rect(MECH_S[0] + 0.15, MECH_S[1] - 0.15,
                                  MECH_U[0] + 0.10, MECH_U[1] - 0.10),
          Z_DECK - EMBED, Z_DECK + 0.20, mats["Toy_steel"])
    prism("mech_condenser", roof_rect(MECH_S[0], MECH_S[1], MECH_U[0], MECH_U[1]),
          Z_DECK + 0.20 - EMBED, Z_MECH, mats["Toy_steel"])
    prism("mech_box", roof_rect(8.60, 9.00, 4.90, 5.20), Z_DECK - EMBED,
          Z_DECK + 0.25, mats["Toy_steel"])
    v = roof_xy(5.30, 4.60)
    disc("mech_vent", v[0], v[1], Z_DECK - EMBED, Z_DECK + 0.35, 0.09, 8,
         mats["Toy_steel"])

    # the flue. THE TALLEST GEOMETRY IN THE EXPORT: its cap top is Z_TOP and the
    # loader's height normalization is taken from it. Exaggerated to a chunky
    # 0.35 m cylinder so it survives at thumbnail size and so the scale does not
    # rest on a hairline object.
    fxy = roof_xy(FLUE_S, FLUE_U)
    disc("flue", fxy[0], fxy[1], Z_DECK - EMBED, Z_TOP - 0.12, FLUE_R, 10,
         mats["Toy_steel"])
    disc("flue_cap", fxy[0], fxy[1], Z_TOP - 0.12 - EMBED, Z_TOP, FLUE_R + 0.06, 10,
         mats["Toy_steel"])

    # 9. rear elevation: a door and two windows. Visible only from the air, and
    #    unverified - kept as plain as the plan says rather than invented into a
    #    stair or a deck.
    # The rear door sits at the RAISED floor level, not at grade: the ground
    # storey is 1.35 m up and the base band runs across the rear too, so a door
    # started at z=0 was three-quarters buried behind the band and rendered as a
    # small square. No rear stair - nothing in the sources shows one.
    prism("rear_door", REAR.rect(2.10, 3.10, -0.12, 0.02), Z_BASE, Z_BASE + DOOR_H,
          mats["Toy_ink"])
    for k, t_c in enumerate((4.60, 6.20)):
        window(f"rearwin{k}", REAR, t_c, SILL_UP, mats, w=0.90, h=1.50)

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.10/2. Glazing, frames, sills, glow shells and the cornice steps are small
    # or already stepped - a token softening or none at all is what keeps this
    # under cap, and three corbelled steps read as chunky whether or not their
    # arrises are rounded.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        n = obj.name
        if "_glow" in n or "_fill" in n or "_light" in n or "groove_" in n:
            continue
        if n.startswith(("cornice", "curb_", "stoop", "mech_", "flue", "parapet_")) \
                or n.endswith(("_sill", "_head")) or "_jamb" in n:
            continue
        if "skirt" in n or "_cornice" in n or n.startswith("base_"):
            bevel(obj, width=0.04, segments=1)
        else:
            bevel(obj)

    recentre()
    return scene


ANCHOR_SHIFT = [0.0, 0.0]


def recentre():
    """Move the model so its XY bbox centre is the origin (contract rule 2). The
    manifest anchor is DESIGN_ANCHOR moved by the same vector, so the building
    still lands on its real footprint."""
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
    print(f"[build] design (wall-box centre) anchor: {DESIGN_ANCHOR}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] front faces {FRONT.heading:.2f} deg; flank {FLANK.heading:.2f}; "
          f"rear {REAR.heading:.2f}; party {PARTY.heading:.2f}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "254-ritch.blend")
    glb = os.path.join(out, "254-ritch.glb")
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
