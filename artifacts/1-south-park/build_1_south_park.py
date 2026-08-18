"""Deterministic Blender build of the SF-SIM miniature 1 South Park
(One South Park - the 1919 concrete tobacco warehouse converted to lofts 2007).

    blender -b --python build_1_south_park.py -- [--out DIR]

Writes 1-south-park.blend and 1-south-park.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading - the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, stair/lift overrun crest
exactly 20.20 m.

Design (see REFERENCE.md for the sources behind every number):

* a 1919-20 three-storey reinforced-concrete tobacco warehouse closing the east
  end of the South Park oval, converted 2004-07 by LDP Architecture into 35 loft
  condominiums plus ground-floor commercial, with TWO MORE STOREYS added as a
  set-back rooftop penthouse (permit PA #200405194312: existing 3 -> proposed 5)
  and two light courts carved down through the middle of the plan;
* it is a BLOCK, not a tooth in a row: 1,570 m2 on six sides, twice the plan area
  of anything else on the oval. Two hero elevations (33.0 m on South Park facing
  315.0, and 28.2 + 5.1 + 15.3 m on Second Street facing 44.6/45.3 with a real
  5.1 m re-entrant step) and two blind party walls (43.2 m south-west against
  17-19 South Park, whose roof is only 6.6 m so ~9 m of this wall is exposed;
  37.8 m south-east against 300 Brannan, which is taller and hides it);
* the recognition rests on the ARCADE. Every bay of both hero elevations is a
  tall round-arched opening, ~2.63 m wide, sill 1.05 m, impost 6.10 m, crown
  7.05 m, on a ~4.0 m pitch, with a white circular MEDALLION 0.75 m across in
  every spandrel at 7.00 m. Nothing else on this oval has either;
* above the arcade a projecting string course (7.50-8.20 m), then two storeys of
  big gridded steel sash - a taller row 8.35-11.00 and a shorter row
  11.90-13.90 - then a bold cornice, bed mould 14.55, crest 15.75 m;
* behind the cornice the roof does half the work, because the app's camera looks
  down: a dark charcoal two-level penthouse (roof 18.60 m) pushed to the
  north-east and south-east, a light court cut down through it to 9.40 m, a
  stair/lift overrun to 20.20 m, and LANDSCAPED TERRACES - warm timber decking,
  clipped hedge rows along both parapets, a lawn patch near the west corner -
  filling a 12 m band on the north-west and an 11 m band on the south-west;
* night state: the ARCADE is the hero, lit warm and continuous all the way round
  both street elevations, because that is what this building actually does at
  night (retail + lobby behind 24 glazed arches). Supporting it, an uneven
  scatter of about two thirds of the 48 upper windows - 35 flats, not an office
  floor - and one quiet cool band on the penthouse. Glow surfaces are single
  open plates standing proud of the opaque glazing, never closed shells: the app
  renders _Glow in a separate layer and a closed shell is two alpha layers deep,
  so it reads far brighter by day than intended.

Heights come from a rectified Street View elevation (the equirectangular tiles of
two panos whose positions were confirmed to under a metre against three known
footprint corners, reprojected onto each wall plane to give an orthographic
drawing with a metric grid) and from the DataSF LiDAR histogram, which is bimodal
and resolves to a 18.6 m penthouse over a 14.9 m deck. The two methods were not
tuned to each other and they agree.

Authoring frame: the block sits at ~45 deg to the world axes, so everything is
placed through Face frames built from the six measured footprint corners. The
axis-aligned XY bounding box is ~58 x 54 m even though no side is longer than
43 m. That is expected, not a scale error.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

LON0P, LAT0P = -122.4375, 37.77
LON_M = 111320.0 * math.cos(math.radians(LAT0P))
LAT_M = 110540.0

# Wall-box AABB centre of the cleaned six-sided footprint. The build recentres
# on the model's own AABB afterwards and report() prints the shipped anchor.
DESIGN_ANCHOR = (-122.3928634, 37.7820480)

# The footprint, metres east/north from DESIGN_ANCHOR. OSM way/112759870 has
# eight vertices, two of them 1.1 m and 2.7 m survey slivers; these six come
# from intersecting the six real wall lines. Order is S -> E -> Cc -> Dd -> N
# -> W, i.e. clockwise seen from above.
S_COR = (1.939, -26.843)     # south corner  (party x party)
E_COR = (28.847, -0.328)     # east corner   (party x Second Street)
C_COR = (9.003, 19.713)      # step, outer
D_COR = (5.387, 16.110)      # step, inner
N_COR = (-5.498, 26.843)     # north corner  (Second Street x South Park)
W_COR = (-28.847, 3.527)     # west corner   (South Park x party)

FOOTPRINT = [S_COR, E_COR, C_COR, D_COR, N_COR, W_COR]
CX = sum(p[0] for p in FOOTPRINT) / len(FOOTPRINT)
CY = sum(p[1] for p in FOOTPRINT) / len(FOOTPRINT)

# Storey lines, metres. Everything down to Z_CREST is read off the rectified
# Second Street elevation (+-0.4 m on the storey lines, +-0.6 m on the cornice);
# Z_PENT and Z_TOP are LiDAR (mode 18.76, hgt_max 20.22).
Z_PLINTH = 1.05
Z_IMPOST = 6.10
Z_ARCH = 7.05
Z_MED = 7.00
Z_STR0, Z_STR1 = 7.50, 8.20
Z_W1A, Z_W1B = 8.35, 11.00
Z_W2A, Z_W2B = 11.90, 13.90
Z_CORN0, Z_CORN1, Z_CREST = 14.55, 15.20, 15.75
Z_DECK = 15.00
Z_COURT = 9.40
Z_PENT = 18.60
Z_TOP = 20.20

# Arcade. Bay counts divide each hero face uniformly; the pitches that fall out
# are 4.03, 5.11, 3.82 and 4.13 m, all within 0.2 m of the 3.94 m pitch measured
# off the rectified elevation.
BAY_FRAC = 0.66          # arch width as a fraction of the bay pitch
ARCH_RISE = 0.42         # arch rise as a fraction of the arch width
ARCH_SEGS = 5            # half-arch segments
ARCHIVOLT = 0.24         # width of the white ring round each arch
ARCH_PROUD = 0.11
GLASS_RECESS = 0.16

MED_R = 0.45             # medallion radius (real 0.375 - exaggerated, see 2.6)
MED_PROUD = 0.10
MED_SEGS = 10

WIN_FRAC = 0.72          # upper-window width as a fraction of the bay pitch
WIN_RECESS = 0.14
WIN_SURROUND = 0.13

PLINTH_PROUD = 0.07
STRING_PROUD = 0.30
CORN_PROUD_0 = 0.28
CORN_PROUD_1 = 0.46
PARAPET_PROUD = 0.10

# Roof. Penthouse setbacks per face, in the order of HERO/PARTY faces below.
SETBACK = {"SE": 3.2, "NE_S": 3.6, "STEP": 3.0, "NE_N": 3.0, "NW": 9.5, "SW": 8.5}
# The light court, in the Second Street face frame: d = metres inward from that
# wall line, t = metres along it from the east corner. Sized and placed off the
# z21 satellite image; the floor is LiDAR hgt_min.
COURT_D0, COURT_D1 = 12.6, 18.1
COURT_T0, COURT_T1 = 2.6, 25.6
TERRACE_NW = 9.5
TERRACE_SW = 8.5
HEDGE_W, HEDGE_H = 0.85, 0.95

BEVEL_W, BEVEL_SEG = 0.09, 2

# Which upper windows are lit. Deterministic pseudo-random: 35 flats, not an
# office floor, so the scatter must be uneven and must not be a pattern.
LIT_SEED = 0x5f375a86


PALETTE_HEX = {
    "Toy_dove": "c9cecd",    # the body: all three storeys of wall on all six
                             # faces, the plinth and the piers. OFF-PALETTE (a
                             # WARN, not a fail) and deliberate. Both party-wall
                             # neighbours - 21-29 South Park and 300 Brannan -
                             # are Toy_stone (d9d2c2) bodies, and three adjacent
                             # Toy_stone blocks on one corner merge into a
                             # single beige mass from the aerial camera. The
                             # real paint is measurably cooler and lighter than
                             # either: sampled off the rectified elevation the
                             # wall is near-neutral with a faint cool cast.
                             # Set one step darker than the first pass (d4d6d4)
                             # so the Toy_white cornice, string course,
                             # archivolts and medallions read as trim rather
                             # than as more wall - at this scale a half-step
                             # between body and trim disappears.
    "Toy_white": "f7f4ec",   # cornice, string course, archivolts, medallions,
                             # window surrounds, parapet copings, pergolas
    "Toy_slate": "6f7883",   # the two-level penthouse and the stair/lift
                             # overrun. NOT Toy_roofd (45454a): that renders as
                             # rgb(9,9,12) under the app's lighting, and the
                             # penthouse is this model's second-biggest visible
                             # mass - it has to read as a dark grey, not a hole.
                             # Toy_slate is precedented by 300-brannan, the
                             # neighbour across this building's south-east party
                             # wall.
    "Toy_ink": "3a3530",     # arch reveals, the roller-shutter bay, penthouse
                             # mullions, mechanical blocks, court floor
    "Toy_glass": "2a4d73",   # upper-storey glazing
    "Toy_glassl": "6f95b8",  # arcade fanlights and the penthouse band
    "Toy_steel": "9aa0a6",   # roof membrane, penthouse roof, deck
    "Toy_rust": "a86444",    # roof-terrace timber decking
    "Toy_verdigris": "9fb8a8",  # terrace hedges, planters, the lawn plate
    "Toy_mustard_Glow": "d9a441",   # the arcade at night - the hero glow, the
                             # warm spill from the retail and the lobby behind
                             # 24 glazed arches
    "Toy_glassl_Glow": "6f95b8",    # lit flats and the penthouse band. NOT
                             # Toy_glass_Glow: the app draws _Glow in a separate
                             # UNLIT layer, so the surface shows its raw base
                             # colour and 2a4d73 is the navy of UNLIT glass.
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


# ----------------------------------------------------------------- geometry


class Face:
    """A local frame on one elevation: t runs along the face from `a` to `b`,
    d runs OUTWARD (away from the footprint centroid), z is world up."""

    def __init__(self, a, b, key):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        self.a, self.b, self.key = a, b, key
        self.length = n
        self.t = (dx / n, dy / n)
        nrm = (-self.t[1], self.t[0])
        mx, my = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
        if (mx + nrm[0] - CX) ** 2 + (my + nrm[1] - CY) ** 2 < (mx - CX) ** 2 + (
            my - CY
        ) ** 2:
            nrm = (-nrm[0], -nrm[1])
        self.n = nrm
        self.heading = (math.degrees(math.atan2(nrm[0], nrm[1])) + 360.0) % 360.0

    def xy(self, t, d):
        return (
            self.a[0] + self.t[0] * t + self.n[0] * d,
            self.a[1] + self.t[1] * t + self.n[1] * d,
        )

    def rect(self, t0, t1, d0, d1):
        return [self.xy(t0, d0), self.xy(t1, d0), self.xy(t1, d1), self.xy(t0, d1)]


SE = Face(S_COR, E_COR, "SE")        # party wall, 300 Brannan          -> 135.4
NE_S = Face(E_COR, C_COR, "NE_S")    # hero, Second Street              ->  45.3
STEP = Face(C_COR, D_COR, "STEP")    # hero, the re-entrant return      -> 315.1
NE_N = Face(D_COR, N_COR, "NE_N")    # hero, Second Street (recessed)   ->  44.6
NW = Face(N_COR, W_COR, "NW")        # hero, South Park street          -> 315.0
SW = Face(W_COR, S_COR, "SW")        # party wall, 17-19 South Park     -> 224.6

FACES = [SE, NE_S, STEP, NE_N, NW, SW]
# Hero faces and their bay counts. 7 + 1 + 4 + 8 = 20 structural bays; the two
# end bays of each run share their outer medallion with the neighbouring face.
HERO = [(NE_S, 7), (STEP, 1), (NE_N, 4), (NW, 8)]


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


def bevel(obj, width=BEVEL_W, segments=BEVEL_SEG):
    """Miniature-style edge softening (style bible s.4). The offset is capped at
    a third of the object's thinnest dimension: glazing plates, surrounds and
    copings are only 60-160 mm thick and a full bevel on those collapses
    opposing profiles into zero-area slivers even with clamp_overlap."""
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


def profile_solid(name, face, profile, d0, d1, mat):
    """Extrude a closed (t, z) profile on `face` outward from d0 to d1.

    This is how every opening in this model is made. A face-plane profile is the
    natural description of an arched opening, and extruding it along the wall
    normal gives a genuinely closed solid, so the validator's per-object signed
    volume test passes without a special case."""
    n = len(profile)
    verts = [face.xy(t, d0) + (z,) for t, z in profile]
    verts += [face.xy(t, d1) + (z,) for t, z in profile]
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    return new_mesh(name, verts, faces, [mat])


def profile_ring(name, face, inner, outer, d0, d1, mat):
    """A closed band between two (t, z) profiles with matching vertex counts,
    extruded from d0 to d1 - the archivolt and the window surround."""
    n = len(inner)
    assert len(outer) == n
    verts = [face.xy(t, d0) + (z,) for t, z in inner]
    verts += [face.xy(t, d0) + (z,) for t, z in outer]
    verts += [face.xy(t, d1) + (z,) for t, z in inner]
    verts += [face.xy(t, d1) + (z,) for t, z in outer]
    I0, O0, I1, O1 = 0, n, 2 * n, 3 * n
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((I0 + i, I0 + j, O0 + j, O0 + i))     # d0 annulus
        faces.append((I1 + i, I1 + j, O1 + j, O1 + i))     # d1 annulus
        faces.append((I0 + i, I0 + j, I1 + j, I1 + i))     # inner skin
        faces.append((O0 + i, O0 + j, O1 + j, O1 + i))     # outer skin
    return new_mesh(name, verts, faces, [mat])


def glow_plate(name, face, t0, t1, z0, z1, d, mat):
    """ONE outward-facing quad standing `d` proud of the wall.

    Night glow must never be a closed shell. The app draws _Glow in a separate
    layer that is translucent by day, so a closed box shows its front AND back
    face and reads at roughly twice the intended day alpha - enough to tint a
    whole facade. The winding is set explicitly here and never recalculated."""
    p = [face.xy(t0, d) + (z0,), face.xy(t1, d) + (z0,),
         face.xy(t1, d) + (z1,), face.xy(t0, d) + (z1,)]
    e1 = Vector(p[1]) - Vector(p[0])
    e2 = Vector(p[3]) - Vector(p[0])
    if e1.cross(e2).dot(Vector((face.n[0], face.n[1], 0.0))) < 0.0:
        p = list(reversed(p))
    return new_mesh(name, p, [(0, 1, 2, 3)], [mat], recalc=False)


def point_in_poly(p, poly):
    x, y = p
    inside = False
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        if (y0 > y) != (y1 > y):
            xi = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            if xi > x:
                inside = not inside
    return inside


def glow_seg(name, a, b, z0, z1, proud, mat, blockers=()):
    """One outward-facing glow quad along an arbitrary polygon edge - the
    penthouse band, whose plan is a clipped hexagon with no Face frame."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    m = math.hypot(dx, dy)
    if m < 1.6:
        return None
    nx, ny = dy / m, -dx / m
    mx, my = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
    if (mx + nx - CX) ** 2 + (my + ny - CY) ** 2 < (mx - CX) ** 2 + (my - CY) ** 2:
        nx, ny = -nx, -ny
    # Skip seams. The penthouse is TILED around the light court, so some of its
    # pieces' edges face another piece; a glow plate there is buried, and the
    # validator's ray test - which requires each glow face to be the first thing
    # hit from outside - fails on exactly those. One of 118 failed this way
    # before the probe went in.
    probe = (mx + nx * 1.2, my + ny * 1.2)
    for poly in blockers:
        if point_in_poly(probe, poly):
            return None
    ia = (a[0] + nx * proud + dx / m * 0.4, a[1] + ny * proud + dy / m * 0.4)
    ib = (b[0] + nx * proud - dx / m * 0.4, b[1] + ny * proud - dy / m * 0.4)
    p = [ia + (z0,), ib + (z0,), ib + (z1,), ia + (z1,)]
    e1 = Vector(p[1]) - Vector(p[0])
    e2 = Vector(p[3]) - Vector(p[0])
    if e1.cross(e2).dot(Vector((nx, ny, 0.0))) < 0.0:
        p = list(reversed(p))
    return new_mesh(name, p, [(0, 1, 2, 3)], [mat], recalc=False)


def _winding(poly):
    s2 = 0.0
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        s2 += a[0] * b[1] - b[0] * a[1]
    return 1.0 if s2 > 0.0 else -1.0


def inset_polygon(poly, dists):
    """Offset each edge of a simple polygon inward by its own distance and
    re-intersect adjacent edges. `dists` is one distance per edge (edge i runs
    poly[i] -> poly[i+1]) or a single scalar. Negative offsets outward.

    Which side is "inward" comes from the polygon's own WINDING, never from
    which side the centroid happens to lie on - the centroid test is wrong the
    moment a polygon has a reflex vertex, and this footprint has one at the
    re-entrant step."""
    n = len(poly)
    if not isinstance(dists, (list, tuple)):
        dists = [dists] * n
    side = _winding(poly)
    lines = []
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy) or 1e-9
        d = (dx / m, dy / m)
        nrm = (-d[1] * side, d[0] * side)
        lines.append(((a[0] + nrm[0] * dists[i], a[1] + nrm[1] * dists[i]), d))
    out = []
    for i in range(n):
        (p0, d0) = lines[i - 1]
        (p1, d1) = lines[i]
        den = d0[0] * d1[1] - d0[1] * d1[0]
        if abs(den) < 1e-9:
            out.append(p1)
            continue
        t = ((p1[0] - p0[0]) * d1[1] - (p1[1] - p0[1]) * d1[0]) / den
        q = (p0[0] + d0[0] * t, p0[1] + d0[1] * t)
        # Spike guard. At the RE-ENTRANT STEP - the one reflex vertex in this
        # footprint - the two offset lines meet far away and the intersection
        # shoots off into a long sail; a 12 m penthouse setback turns that into
        # a spike longer than the building. Capping the displacement replaces
        # the sail with a chamfer nobody can see at this scale.
        v = (q[0] - poly[i][0], q[1] - poly[i][1])
        m = math.hypot(v[0], v[1])
        cap = max(abs(dists[i]), abs(dists[i - 1])) * 1.45 + 0.05
        if m > cap and m > 1e-9:
            q = (poly[i][0] + v[0] * cap / m, poly[i][1] + v[1] * cap / m)
        out.append(q)
    return out


def ring(name, poly, thickness, z0, z1, mat, mat_top=None):
    """A closed band solid between `poly` and its inward offset - a parapet or a
    hedge row. NOT a prism of the inset polygon: that is a solid plateau, and
    building the parapet that way once buried the whole roof design under a
    15.6 m slab."""
    inner = inset_polygon(poly, thickness)
    n = len(poly)
    verts = [(x, y, z0) for x, y in poly]
    verts += [(x, y, z0) for x, y in inner]
    verts += [(x, y, z1) for x, y in poly]
    verts += [(x, y, z1) for x, y in inner]
    O0, I0, O1, I1 = 0, n, 2 * n, 3 * n
    faces, face_mats = [], []
    for i in range(n):
        j = (i + 1) % n
        faces.append((O0 + i, O0 + j, O1 + j, O1 + i)); face_mats.append(0)
        faces.append((I0 + i, I0 + j, I1 + j, I1 + i)); face_mats.append(0)
        faces.append((O0 + i, O0 + j, I0 + j, I0 + i)); face_mats.append(0)
        faces.append((O1 + i, O1 + j, I1 + j, I1 + i))
        face_mats.append(1 if mat_top else 0)
    mats = [mat, mat_top] if mat_top else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def open_ring(name, pts, thickness, z0, z1, mat):
    """The same band along an OPEN polyline - a hedge row that runs along two
    terrace edges and stops, rather than closing round the whole roof."""
    inner = []
    for i, (x, y) in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy) or 1e-9
        nx, ny = -dy / m, dx / m
        if (x + nx - CX) ** 2 + (y + ny - CY) ** 2 > (x - CX) ** 2 + (y - CY) ** 2:
            nx, ny = -nx, -ny
        inner.append((x + nx * thickness, y + ny * thickness))
    n = len(pts)
    verts = [(x, y, z0) for x, y in pts] + [(x, y, z0) for x, y in inner]
    verts += [(x, y, z1) for x, y in pts] + [(x, y, z1) for x, y in inner]
    O0, I0, O1, I1 = 0, n, 2 * n, 3 * n
    faces = []
    for i in range(n - 1):
        j = i + 1
        faces.append((O0 + i, O0 + j, O1 + j, O1 + i))
        faces.append((I0 + i, I0 + j, I1 + j, I1 + i))
        faces.append((O0 + i, O0 + j, I0 + j, I0 + i))
        faces.append((O1 + i, O1 + j, I1 + j, I1 + i))
    faces.append((O0, I0, I1, O1))
    faces.append((O0 + n - 1, I0 + n - 1, I1 + n - 1, O1 + n - 1))
    return new_mesh(name, verts, faces, [mat])


def poly_area(poly):
    s2 = 0.0
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        s2 += a[0] * b[1] - b[0] * a[1]
    return abs(s2) / 2.0


def poly_minus_slot(poly, face, d_near, d_far, t_lo, t_hi):
    """`poly` with a rectangular slot removed, returned as up to four simple
    pieces that tile it.

    The light court has to be a REAL hole - from the app's aerial camera a
    painted dark rectangle reads as a stain, not a court - and this model has no
    boolean anywhere else, so the hole is made by tiling around it. Each piece
    stays a closed prism, so the validator's per-object signed-volume test needs
    no special case. The pieces share internal faces at their joints; those are
    buried between two solids and never seen.

    The slot is described in `face`'s frame: d_near/d_far are inward distances
    from that wall, t_lo/t_hi positions along it."""
    n_in = (-face.n[0], -face.n[1])
    p_near = face.xy(0.0, -d_near)
    p_far = face.xy(0.0, -d_far)
    p_lo = face.xy(t_lo, 0.0)
    p_hi = face.xy(t_hi, 0.0)
    out = []
    out.append(clip_polygon(poly, p_near, n_in))              # NE of the slot
    out.append(clip_polygon(poly, p_far, face.n))             # SW of the slot
    mid = clip_polygon(clip_polygon(poly, p_near, face.n), p_far, n_in)
    if mid:
        out.append(clip_polygon(mid, p_lo, face.t))
        out.append(clip_polygon(mid, p_hi, (-face.t[0], -face.t[1])))
    return [q for q in out if len(q) >= 3 and poly_area(q) > 3.0]


def clip_polygon(poly, p, nrm):
    """Sutherland-Hodgman: keep the half-plane where (x - p) . nrm <= 0."""
    def sd(q):
        return (q[0] - p[0]) * nrm[0] + (q[1] - p[1]) * nrm[1]

    out = []
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        da, db = sd(a), sd(b)
        if da <= 0.0:
            out.append(a)
        if (da <= 0.0) != (db <= 0.0):
            f = da / (da - db)
            out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    # drop duplicates that the clip can create at a grazing vertex
    clean = []
    for q in out:
        if not clean or math.hypot(q[0] - clean[-1][0], q[1] - clean[-1][1]) > 1e-6:
            clean.append(q)
    if len(clean) > 2 and math.hypot(
        clean[0][0] - clean[-1][0], clean[0][1] - clean[-1][1]
    ) < 1e-6:
        clean.pop()
    return clean


# --------------------------------------------------------------- components


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


def arch_profile(t_c, w, z_sill, z_imp, rise, grow=0.0):
    """Closed (t, z) outline of one arched opening, walked anticlockwise from the
    bottom-left. `grow` inflates it uniformly, which is how the archivolt's outer
    profile is generated with the SAME vertex count as the inner one."""
    half = w / 2.0 + grow
    h_rise = rise * w + grow
    pts = [(t_c - half, z_sill - grow), (t_c + half, z_sill - grow),
           (t_c + half, z_imp)]
    for k in range(1, ARCH_SEGS):
        a = math.pi * k / (2.0 * ARCH_SEGS)
        pts.append((t_c + half * math.cos(a), z_imp + h_rise * math.sin(a)))
    pts.append((t_c, z_imp + h_rise))
    for k in range(ARCH_SEGS - 1, 0, -1):
        a = math.pi * k / (2.0 * ARCH_SEGS)
        pts.append((t_c - half * math.cos(a), z_imp + h_rise * math.sin(a)))
    pts.append((t_c - half, z_imp))
    return pts


def rect_profile(t_c, w, z0, z1, grow=0.0):
    half = w / 2.0 + grow
    return [(t_c - half, z0 - grow), (t_c + half, z0 - grow),
            (t_c + half, z1 + grow), (t_c - half, z1 + grow)]


def circle_profile(t_c, z_c, r, segs=MED_SEGS):
    return [(t_c + r * math.cos(2 * math.pi * i / segs),
             z_c + r * math.sin(2 * math.pi * i / segs)) for i in range(segs)]


def arcade(face, nbays, mats, lit, shutter_bay=None, entry_bay=None):
    """One hero elevation: plinth band, nbays arched openings with archivolts and
    two-tone glazing, and a medallion in every spandrel."""
    pitch = face.length / nbays
    w = pitch * BAY_FRAC
    rise = ARCH_RISE
    prism(f"{face.key}_plinth", face.rect(0.0, face.length, -0.02, PLINTH_PROUD),
          0.0, Z_PLINTH, mats["Toy_dove"])
    for i in range(nbays):
        t_c = (i + 0.5) * pitch
        nm = f"{face.key}_arch{i}"
        inner = arch_profile(t_c, w, Z_PLINTH, Z_IMPOST, rise)
        outer = arch_profile(t_c, w, Z_PLINTH, Z_IMPOST, rise, grow=ARCHIVOLT)
        profile_ring(f"{nm}_ring", face, inner, outer, -0.02, ARCH_PROUD,
                     mats["Toy_white"])
        # reveal: a dark plate filling the whole opening, then the glazing in
        # front of it, so the opening still reads dark at its edges
        profile_solid(f"{nm}_reveal", face, inner, -GLASS_RECESS, 0.005,
                      mats["Toy_ink"])
        if shutter_bay is not None and i == shutter_bay:
            profile_solid(f"{nm}_shutter", face,
                          rect_profile(t_c, w * 0.94, Z_PLINTH, Z_IMPOST),
                          -0.05, 0.02, mats["Toy_ink"])
            profile_solid(f"{nm}_fan", face,
                          arch_head_profile(t_c, w, Z_IMPOST, rise),
                          -0.05, 0.025, mats["Toy_glassl"])
            continue
        if entry_bay is not None and i == entry_bay:
            profile_solid(f"{nm}_entry", face,
                          rect_profile(t_c, w * 0.94, Z_PLINTH, Z_IMPOST),
                          -0.05, 0.02, mats["Toy_ink"])
            profile_solid(f"{nm}_fan", face,
                          arch_head_profile(t_c, w, Z_IMPOST, rise),
                          -0.05, 0.025, mats["Toy_glassl"])
        else:
            profile_solid(f"{nm}_glass", face,
                          rect_profile(t_c, w * 0.94, Z_PLINTH + 0.12, Z_IMPOST),
                          -0.05, 0.025, mats["Toy_glass"])
            profile_solid(f"{nm}_fan", face,
                          arch_head_profile(t_c, w, Z_IMPOST, rise),
                          -0.05, 0.025, mats["Toy_glassl"])
            # one mullion cross - enough to say "gridded sash" at this scale
            profile_solid(f"{nm}_mull_v", face,
                          rect_profile(t_c, 0.12, Z_PLINTH + 0.12, Z_IMPOST),
                          0.0, 0.06, mats["Toy_ink"])
            zm = (Z_PLINTH + 0.12 + Z_IMPOST) / 2.0
            profile_solid(f"{nm}_mull_h", face,
                          rect_profile(t_c, w * 0.94, zm - 0.06, zm + 0.06),
                          0.0, 0.06, mats["Toy_ink"])
        if lit:
            # Deliberately SMALLER than the opening. The app shows _Glow at
            # 0.12 + 0.95*uNight, so by day a plate that fills the arch tints
            # the whole arcade brown; keeping a margin of unlit Toy_glass round
            # it leaves the day read cool and still gives night a continuous
            # warm ribbon at eye level.
            glow_plate(f"{nm}_glow", face, t_c - w * 0.36, t_c + w * 0.36,
                       Z_PLINTH + 0.55, Z_IMPOST - 0.85, 0.075,
                       mats["Toy_mustard_Glow"])
    # medallions: one in every spandrel INCLUDING both ends, so the rhythm
    # continues round the corners
    for i in range(nbays + 1):
        t_c = i * pitch
        if t_c < MED_R + 0.35 or t_c > face.length - MED_R - 0.35:
            continue
        profile_solid(f"{face.key}_med{i}", face,
                      circle_profile(t_c, Z_MED, MED_R), -0.02, MED_PROUD,
                      mats["Toy_white"])


def arch_head_profile(t_c, w, z_imp, rise):
    """Just the semicircular head of an arch, closed along the impost line."""
    half = w * 0.47
    h_rise = rise * w * 0.94
    pts = [(t_c - half, z_imp), (t_c + half, z_imp)]
    for k in range(1, ARCH_SEGS):
        a = math.pi * k / (2.0 * ARCH_SEGS)
        pts.append((t_c + half * math.cos(a), z_imp + h_rise * math.sin(a)))
    pts.append((t_c, z_imp + h_rise))
    for k in range(ARCH_SEGS - 1, 0, -1):
        a = math.pi * k / (2.0 * ARCH_SEGS)
        pts.append((t_c - half * math.cos(a), z_imp + h_rise * math.sin(a)))
    return pts


def upper_windows(face, nbays, mats, rng):
    """Two rows of big steel-sash openings, one taller and one shorter, nearly
    filling their bays. One recessed glazing plate, one white surround and one
    mullion cross each - no pane grid, because at a 4 m bay pitch across 48 m of
    frontage a real grid is sub-pixel and turns the elevation into corduroy."""
    pitch = face.length / nbays
    w = pitch * WIN_FRAC
    for row, (z0, z1) in enumerate(((Z_W1A, Z_W1B), (Z_W2A, Z_W2B))):
        for i in range(nbays):
            t_c = (i + 0.5) * pitch
            nm = f"{face.key}_w{row}_{i}"
            inner = rect_profile(t_c, w, z0, z1)
            outer = rect_profile(t_c, w, z0, z1, grow=WIN_SURROUND)
            profile_ring(f"{nm}_surr", face, inner, outer, -0.02, 0.10,
                         mats["Toy_white"])
            profile_solid(f"{nm}_glass", face, inner, -WIN_RECESS, 0.015,
                          mats["Toy_glass"])
            profile_solid(f"{nm}_mv", face, rect_profile(t_c, 0.13, z0, z1),
                          0.0, 0.055, mats["Toy_ink"])
            zm = (z0 + z1) / 2.0
            profile_solid(f"{nm}_mh", face,
                          rect_profile(t_c, w, zm - 0.07, zm + 0.07),
                          0.0, 0.055, mats["Toy_ink"])
            rng[0] = (rng[0] * 1103515245 + 12345) & 0x7FFFFFFF
            if (rng[0] >> 16) % 100 < 64:
                glow_plate(f"{nm}_glow", face, t_c - w * 0.46, t_c + w * 0.46,
                           z0 + 0.10, z1 - 0.10, 0.05, mats["Toy_glassl_Glow"])


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mats = {k: make_material(k) for k in PALETTE_HEX}

    solids = []

    # ---- body -------------------------------------------------------------
    # Split at the light-court floor so the court can be a real hole through the
    # deck and the penthouse without a boolean: everything above Z_COURT is
    # tiled around the slot by poly_minus_slot().
    court_pieces = poly_minus_slot(FOOTPRINT, NE_S, COURT_D0, COURT_D1,
                                   COURT_T0, COURT_T1)
    solids.append(prism("body_lo", FOOTPRINT, 0.0, Z_COURT, mats["Toy_dove"]))
    for k, poly in enumerate(court_pieces):
        solids.append(prism(f"body_hi{k}", poly, Z_COURT, Z_DECK,
                            mats["Toy_dove"], mats["Toy_steel"]))
    print(f"[build] court pieces={len(court_pieces)} "
          f"areas={[round(poly_area(q), 1) for q in court_pieces]}")

    # ---- arcade and upper windows on the four hero planes -----------------
    rng = [LIT_SEED]
    for face, nbays in HERO:
        shutter = 5 if face is NW else None       # the car-stacker roller door
        entry = 1 if face is NW else None         # the residential entrance
        arcade(face, nbays, mats, lit=True, shutter_bay=shutter, entry_bay=entry)
        upper_windows(face, nbays, mats, rng)

    # ---- string course ----------------------------------------------------
    # Hero faces only: it is a street feature and the party walls are blind.
    for face, _ in HERO:
        solids.append(prism(f"{face.key}_string",
                            face.rect(-0.05, face.length + 0.05, -0.05,
                                      STRING_PROUD),
                            Z_STR0, Z_STR1, mats["Toy_white"]))

    # ---- cornice ----------------------------------------------------------
    # A full closed ring. On the two party walls the real building has a plain
    # parapet, but the ring is what the aerial camera reads as the top of the
    # block, and a cornice that stops dead at a corner reads as a modelling
    # error from above. Documented in REPORT.md.
    # RINGS, not prisms of the outset polygon: a prism there is a solid slab
    # across the whole plan, and it buried the entire roof design under a
    # 15.75 m plateau the first time.
    solids.append(ring("cornice_lo", inset_polygon(FOOTPRINT, -CORN_PROUD_0),
                       CORN_PROUD_0 + 0.55, Z_CORN0, Z_CORN1,
                       mats["Toy_white"]))
    solids.append(ring("cornice_hi", inset_polygon(FOOTPRINT, -CORN_PROUD_1),
                       CORN_PROUD_1 + 0.60, Z_CORN1, Z_CREST,
                       mats["Toy_white"]))
    # parapet RING standing on the deck, inboard of the cornice
    solids.append(ring("parapet", inset_polygon(FOOTPRINT, 0.22), 0.42,
                       Z_DECK, Z_CREST - 0.12, mats["Toy_dove"],
                       mats["Toy_white"]))

    # ---- roof terraces ----------------------------------------------------
    inner = inset_polygon(FOOTPRINT, 0.85)
    for face, depth, key in ((NW, TERRACE_NW, "NW"), (SW, TERRACE_SW, "SW")):
        strip = clip_polygon(inner, face.xy(0.0, -depth),
                             (-face.n[0], -face.n[1]))
        if face is SW:
            # The two terrace bands both reach the WEST corner, and two
            # coincident 0.14 m deck slabs there z-fought into a black patch on
            # the top view. The north-west band wins the corner; the south-west
            # one is clipped out of it.
            strip = clip_polygon(strip, NW.xy(0.0, -TERRACE_NW), NW.n)
        if len(strip) >= 3:
            solids.append(prism(f"terrace_{key}", strip, Z_DECK - 0.02,
                                Z_DECK + 0.12, mats["Toy_rust"]))
            print(f"[build] terrace {key} area={poly_area(strip):.1f} m2")
        # clipped hedge row along the parapet, inboard of it, as a straight
        # run along this face only
        solids.append(prism(f"hedge_{key}",
                            face.rect(1.2, face.length - 1.2,
                                      -1.05 - HEDGE_W, -1.05),
                            Z_DECK + 0.06, Z_DECK + HEDGE_H,
                            mats["Toy_verdigris"]))
    # the lawn patch near the west corner, on the north-west terrace
    solids.append(prism("lawn", [NW.xy(NW.length - 9.5, -2.6),
                                 NW.xy(NW.length - 3.4, -2.6),
                                 NW.xy(NW.length - 3.4, -7.4),
                                 NW.xy(NW.length - 9.5, -7.4)],
                        Z_DECK + 0.10, Z_DECK + 0.22, mats["Toy_verdigris"]))
    # planters punctuating the north-west deck
    for k, t in enumerate((4.0, 12.5, 20.0)):
        solids.append(prism(f"planter_nw{k}",
                            [NW.xy(t, -2.4), NW.xy(t + 3.0, -2.4),
                             NW.xy(t + 3.0, -3.9), NW.xy(t, -3.9)],
                            Z_DECK + 0.10, Z_DECK + 1.05,
                            mats["Toy_verdigris"]))
    # two pergolas on the south-west terrace
    for k, t in enumerate((12.0, 28.0)):
        for dx, dy in ((0.5, -2.0), (0.5, -7.0), (5.5, -2.0), (5.5, -7.0)):
            solids.append(prism(f"perg{k}post{int(dx * 10)}_{int(-dy * 10)}",
                                [SW.xy(t + dx - 0.11, dy - 0.11),
                                 SW.xy(t + dx + 0.11, dy - 0.11),
                                 SW.xy(t + dx + 0.11, dy + 0.11),
                                 SW.xy(t + dx - 0.11, dy + 0.11)],
                                Z_DECK + 0.10, Z_DECK + 2.15,
                                mats["Toy_ink"]))
        solids.append(prism(f"perg{k}_top",
                            [SW.xy(t + 0.1, -1.6), SW.xy(t + 5.9, -1.6),
                             SW.xy(t + 5.9, -7.4), SW.xy(t + 0.1, -7.4)],
                            Z_DECK + 2.15, Z_DECK + 2.26, mats["Toy_ink"]))
    for k, t in enumerate((5.0, 21.5, 36.0)):
        solids.append(prism(f"planter_sw{k}",
                            [SW.xy(t, -2.0), SW.xy(t + 2.8, -2.0),
                             SW.xy(t + 2.8, -3.4), SW.xy(t, -3.4)],
                            Z_DECK + 0.10, Z_DECK + 1.05,
                            mats["Toy_verdigris"]))

    # ---- penthouse, tiled around the same light court ---------------------
    pent_poly = inset_polygon(FOOTPRINT, [SETBACK[f.key] for f in FACES])
    print(f"[build] penthouse gross area={poly_area(pent_poly):.1f} m2 "
          f"({100 * poly_area(pent_poly) / poly_area(FOOTPRINT):.0f}% of plan)")
    pent_pieces = poly_minus_slot(pent_poly, NE_S, COURT_D0, COURT_D1,
                                  COURT_T0, COURT_T1)
    for k, poly in enumerate(pent_pieces):
        solids.append(prism(f"pent{k}", poly, Z_DECK - 0.05, Z_PENT,
                            mats["Toy_slate"], mats["Toy_steel"]))
        # RINGS again - a prism of the outset polygon is a slab coincident
        # with the penthouse roof, and the two z-fought into a moire across the
        # whole top.
        solids.append(ring(f"pent{k}_coping", inset_polygon(poly, -0.13),
                           0.40, Z_PENT, Z_PENT + 0.26, mats["Toy_white"]))
        solids.append(ring(f"pent{k}_band", inset_polygon(poly, -0.07),
                           0.22, Z_PENT - 2.85, Z_PENT - 0.70,
                           mats["Toy_glass"]))
        # night: one quiet cool band, an open plate proud of the glazing
        for a, b in zip(poly, poly[1:] + poly[:1]):
            # Only the two STREET sides light, and only for 1.1 m of the 2.15 m
            # band. An unbroken glow ribbon round the whole penthouse perimeter
            # out-shouted the arcade in the first night render, which inverts
            # the composition the style bible asks for: one hero (the arcade at
            # eye level, warm and continuous) plus quiet accents.
            hd = (math.degrees(math.atan2(b[0] - a[0], b[1] - a[1])) + 90.0) % 360.0
            if min(abs((hd - 45.0 + 180) % 360 - 180),
                   abs((hd - 315.0 + 180) % 360 - 180)) > 25.0:
                continue
            # ...and broken into ~4 m chunks with about half of them lit, so
            # the penthouse reads as a row of flats where some lights are on
            # rather than as one continuous LED strip. A 55 m unbroken ribbon
            # was still competing with the arcade after the first cutback.
            seglen = math.hypot(b[0] - a[0], b[1] - a[1])
            nch = max(1, int(round(seglen / 4.2)))
            for c in range(nch):
                rng[0] = (rng[0] * 1103515245 + 12345) & 0x7FFFFFFF
                if (rng[0] >> 17) % 100 >= 55:
                    continue
                f0, f1 = (c + 0.12) / nch, (c + 0.88) / nch
                p0 = (a[0] + (b[0] - a[0]) * f0, a[1] + (b[1] - a[1]) * f0)
                p1 = (a[0] + (b[0] - a[0]) * f1, a[1] + (b[1] - a[1]) * f1)
                glow_seg(f"pent{k}_{c}_glow", p0, p1,
                         Z_PENT - 2.30, Z_PENT - 1.35, 0.16,
                         mats["Toy_glassl_Glow"],
                         blockers=[q for q in pent_pieces if q is not poly])
    print(f"[build] penthouse pieces={len(pent_pieces)} "
          f"areas={[round(poly_area(q), 1) for q in pent_pieces]}")

    # ---- the light court itself -------------------------------------------
    court = [NE_S.xy(COURT_T0, -COURT_D0), NE_S.xy(COURT_T1, -COURT_D0),
             NE_S.xy(COURT_T1, -COURT_D1), NE_S.xy(COURT_T0, -COURT_D1)]
    solids.append(prism("court_floor", court, Z_COURT - 0.25, Z_COURT + 0.10,
                        mats["Toy_ink"]))
    solids.append(prism("court_green", inset_polygon(court, 1.5),
                        Z_COURT + 0.05, Z_COURT + 0.80, mats["Toy_verdigris"]))

    # ---- stair/lift overrun and mechanical --------------------------------
    ov = [NE_S.xy(11.0, -COURT_D1 - 2.2), NE_S.xy(17.5, -COURT_D1 - 2.2),
          NE_S.xy(17.5, -COURT_D1 - 7.2), NE_S.xy(11.0, -COURT_D1 - 7.2)]
    solids.append(prism("overrun", ov, Z_PENT - 0.2, Z_TOP, mats["Toy_slate"],
                        mats["Toy_steel"]))
    for k, (t, d) in enumerate(((4.0, -6.4), (22.0, -6.4))):
        solids.append(prism(f"mech{k}",
                            [NE_S.xy(t, d), NE_S.xy(t + 3.4, d),
                             NE_S.xy(t + 3.4, d - 2.6), NE_S.xy(t, d - 2.6)],
                            Z_PENT - 0.2, Z_PENT + 0.80, mats["Toy_ink"]))
    for k, (t, d) in enumerate(((8.0, -21.5), (24.0, -20.5))):
        solids.append(prism(f"vent{k}",
                            [NE_S.xy(t, d), NE_S.xy(t + 1.6, d),
                             NE_S.xy(t + 1.6, d - 1.6), NE_S.xy(t, d - 1.6)],
                            Z_PENT - 0.2, Z_PENT + 0.60, mats["Toy_steel"]))

    # Bevel the MASSING only. Every arch ring, glazing plate, surround and
    # mullion is a thin slab whose bevel triples its triangle count for an edge
    # softening nobody can see at 4 m bay pitch - the first build came out at
    # 67,890 triangles that way, more than three times the budget. The massing
    # is where the miniature's chunky-bevel language actually reads.
    NO_BEVEL = ("_ring", "_glass", "_fan", "_reveal", "_mull", "_surr",
                "_mv", "_mh", "_shutter", "_entry", "_glow", "pentglass_")
    for o in list(bpy.data.objects):
        if o.type != "MESH":
            continue
        if any(k in o.name for k in NO_BEVEL):
            continue
        bevel(o)


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
    print(f"[build] design (wall-box AABB centre) anchor: {DESIGN_ANCHOR}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    for f in FACES:
        print(f"[build] face {f.key:5s} len {f.length:6.2f} outward {f.heading:6.2f}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    recentre()
    report()

    blend = os.path.join(out, "1-south-park.blend")
    glb = os.path.join(out, "1-south-park.glb")
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
    )
    print(f"[build] wrote {glb}")


if __name__ == "__main__":
    main()
