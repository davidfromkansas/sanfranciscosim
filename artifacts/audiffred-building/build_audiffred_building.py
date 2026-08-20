"""Deterministic Blender build of the SF-SIM miniature Audiffred Building
(1-21 Mission Street / 100 The Embarcadero, San Francisco Landmark No. 7).

    blender -b --python build_audiffred_building.py -- [--out DIR]

Writes audiffred-building.blend and audiffred-building.glb next to this file (or
into --out). Geometry is authored in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading - the
loader applies no rotation. Origin = model XY bbox centre, min Z = 0, barrel
vault ridge exactly 17.50 m.

Design (see REFERENCE.md for the sources behind every number):

* an 1889 Second Empire commercial block, brick with a wood-framed slate
  mansard, built for Hippolite d'Audiffret to a pattern-book Parisian model. The
  only building left intact on the landward side of The Embarcadero after 1906,
  gutted by a gas fire in 1978, rebuilt 1983-84 with a glazed barrel-vaulted
  penthouse over the roof. Boulevard restaurant on the ground floor since 1993;
* the recognition rests on the THREE-BAND HORIZONTAL SANDWICH: a cream cast-iron
  shopfront under a heavy white entablature, a red brick storey under a white
  corbel table, and a blue-grey slate mansard with white pedimented dormers and
  red brick chimneys. Three colours, two hard white lines, one dark roof;
* the fourth band is the 1984 addition: a glazed barrel vault riding just inside
  the mansard crest, running the length of Mission Street and mitring around
  both ends. It is the crest (17.50 m) and, under a camera that looks down, the
  most visible thing on the building;
* ONE elevation is the hero. Mission Street (41.82 m, north-west) is the address
  and the long side. The Embarcadero (14.00 m, north-east) and Steuart Street
  (14.00 m, south-west) are the short ends, each three bays wide with the NRHP's
  double-width corner windows. The south-east long side is a BLIND BRICK PARTY
  WALL: the nomination is explicit that the common wall continues straight to
  the roof while only the three exposed walls carry the mansard;
* the roof is a flat pale membrane deck at 15.40 m (DataSF LiDAR hgt_majority
  15.44 m / median 15.36 m over 2,238 cells, sigma 2.33) inside a navy mansard
  ring, with the verdigris vault ribbon on three sides and the plant grouped
  against the party wall so the ribbon stays unbroken. DataSF hgt_max 19.18 m is
  that plant, not architecture - see REPORT.md 1;
* night state: the entablature sign band glowing warm along all three public
  elevations (this is Boulevard, and it is what the building actually looks like
  after dark) plus an uneven scatter of lit brick-storey and dormer windows -
  offices upstairs, not a lit grid. Glow surfaces are single faces standing
  proud of the opaque glazing, never closed shells: the app renders _Glow in a
  separate layer and a closed shell is two alpha layers deep, so it reads far
  brighter by day than intended.

Authoring frame: the footprint is a clean 41.82 x 14.00 m rectangle at 45.2 deg
to the world axes, so everything is placed through Face frames built from the
four measured corners. Because the building sits at 45 deg the axis-aligned XY
bounding box comes out roughly SQUARE (~40 x 40 m) even though the building is
3:1. That is expected, not a scale error - check the footprint along the
building's OWN axes before concluding anything is wrong.
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
DESIGN_ANCHOR = (-122.3927748, 37.7933216)

# Wall box, from the OSM way 193054136 oriented bounding box. Cross-checked
# three ways: the NRHP nomination's surveyed lot ("45 feet 10 inches wide and
# 135 1/2 feet long" = 13.97 x 41.30 m), the Assessor's lot_area 6,301.63 sq ft
# = 585.4 m2, and this rectangle's own 585.6 m2.
FRONTAGE = 41.82           # Mission Street, the long address elevation
DEPTH = 14.00              # The Embarcadero / Steuart ends
FRONT_BEARING = 315.2      # Mission Street faces north-west
FLANK_BEARING = 225.2      # Steuart Street faces south-west

# Vertical stack. Only Z_DECK is measured; everything below it is photogrammetric,
# read off the Mission x Embarcadero corner elevation as proportions of the deck
# height (0.40 : 0.31 : 0.29), and Z_CREST is Overture's 17.4 m height reconciled
# with a photogrammetric read of the vault crown. See REPORT.md 1.
Z_SHOP = 5.35              # top of the cast-iron shopfront
Z_ENTAB = 6.15             # top of the entablature - the first white line
Z_BRICK = 10.55            # top of the brick storey
Z_CORBEL = 10.95           # top of the corbel table - the second white line,
                           # and the mansard springing
Z_DECK = 15.40             # flat roof deck / mansard crest - MEASURED
Z_CREST = 17.50            # barrel vault ridge - the bbox top, so the loader's
                           # targetHeightM / measuredHeight lands on exactly 1.0

MANSARD_IN = 1.60          # how far the mansard slope leans in over its height
CROWN_OUT = 0.30           # crown moulding projection past the mansard crest
CROWN_Z = (15.10, 15.55)

ENTAB_OUT = 0.45           # entablature projection
CORBEL_OUT = 0.35          # corbel table projection
SHOP_INSET = 0.15          # the brick above overhangs the shopfront slightly
PIER_W, PIER_OUT = 0.68, 0.18
QUOIN_W, QUOIN_OUT = 0.60, 0.10

EMBED = 0.03               # how far every applied band is sunk INTO the surface
                           # it sits on. Nothing here is allowed to have a face
                           # exactly coincident with another solid's face:
                           # coincident faces make the first-hit direction of a
                           # ray ambiguous and the contract's normals ray test
                           # counts the ambiguity as a flipped face. Overlapping
                           # solids are the supported model - the validator's
                           # authoritative normals test is per-object signed
                           # volume.

# Bays. Three per 14.00 m end (4.67 m pitch, the NRHP's double-width corner
# windows are what make the ends coarser than the front); thirteen per 41.82 m
# of Mission Street (3.22 m pitch). The Mission count is INFERRED off a
# foreshortened photograph - see REPORT.md 3.
N_BAY_FRONT = 13
N_BAY_END = 3

# Chimneys, as t-fractions along Mission and at the footprint corners.
CHIMNEY_FRONT_K = (3, 6, 10)     # bay boundaries k/13 along Mission
CHIMNEY_W, CHIMNEY_D = 0.90, 0.62
CHIMNEY_TOP = 16.30
CHIMNEY_CAP = 0.35

# Shopfront
SHOP_GLASS_Z = (0.90, 5.00)
AWNING_Z, AWNING_OUT, AWNING_T = 4.62, 0.70, 0.16
FRIEZE_Z = (5.45, 6.08)          # the 1924 Bank of Italy nautical band, modelled
                                 # as one recessed strip and applied ONLY to the
                                 # Embarcadero half of Mission and to the
                                 # Embarcadero end - the western half kept the
                                 # original plain sawtooth fascia.
SIGN_Z = (5.52, 6.02)            # the glowing sign strip inside the entablature

# Brick storey openings
WIN_W, WIN_ARCH = 1.55, 0.55     # opening width, and the rise of its arch head
WIN_Z = (7.00, 10.00)            # sill to the springing of the arch
WIN_RECESS = 0.14
SURROUND = 0.16
END_WIN_SCALE = 1.45             # the NRHP's double-width corner windows

# Dormers
DORM_W, DORM_H = 1.32, 3.05
DORM_Z0 = 11.30
DORM_OUT = 0.06                  # front face just proud of the wall plane below
DORM_DEEP = 0.95                 # how far back into the slope the box reaches
PED_H, PED_OUT, PED_OVER = 0.62, 0.22, 0.14

# Barrel vault. The first build made it a full semicircle springing straight off
# the deck: 4.2 m wide out of a 10.8 m deck, and from directly above it read as a
# fat green sausage laid across the roof rather than a glazed ribbon following
# the mansard. It now stands on a low curb and is narrower, which is also what
# the reference aerial shows.
VAULT_HW = 1.55                  # half-width of the springing
VAULT_CURB = 0.55                # verdigris upstand between deck and springing
VAULT_OFFSET = 3.35              # centreline, in from each exposed wall plane
VAULT_SEGS = 10                  # EVEN on purpose: with an odd count no ring
                                 # point lands on the crown and the bbox top
                                 # comes out 23 mm under Z_CREST
VAULT_END_T = 13.00              # how far each end run reaches toward the party
                                 # wall, measured from the Mission corner

# Which bays are lit at night, as (front, embarcadero, steuart) index sets.
# Uneven on purpose: these are offices over a restaurant, not a lit grid.
LIT_FRONT = (1, 2, 5, 8, 9, 12)
LIT_END_E = (0, 2)
LIT_END_S = (1,)
LIT_DORM_FRONT = (0, 3, 4, 7, 11)
LIT_DORM_END_E = (1,)
LIT_DORM_END_S = (0, 2)

BEVEL_W, BEVEL_SEG = 0.10, 2

PALETTE_HEX = {
    "Toy_brick": "c96f4a",   # the brick storey, the chimneys and the whole party
                             # wall. One of the two identity colours: nothing
                             # else on this block or in this district is brick.
    "Toy_navy": "2c4a70",    # the slate mansard on the three exposed faces. The
                             # other identity colour, and the largest single
                             # surface seen from the app's downward camera.
                             # DELIBERATELY NOT Toy_roofd (45454a): that material
                             # measured rgb(9, 9, 12) on a roof deck in the live
                             # scene - effectively black - and this surface is
                             # what the building is recognised by. Toy_navy is
                             # also what the NRHP's "hand-cut blue-grey slate"
                             # actually reads as in daylight.
    "Toy_trim": "f3efe6",    # entablature, corbel table, crown moulding, quoins,
                             # window surrounds, dormer hoods, chimney caps -
                             # every white line on the building
    "Toy_cream": "f2ede3",   # the cast-iron shopfront band and its piers
    "Toy_ink": "3a3530",     # shopfront glazing and awnings
    "Toy_glass": "2a4d73",   # the arched brick-storey windows
    "Toy_glassl": "6f95b8",  # dormer sashes: they read PALE in every reference
                             # photograph (blinds behind them), not dark
    "Toy_verdigris": "9fb8a8",  # the barrel vault. Chosen over Toy_glassl so the
                             # crest separates from the dormer sashes seen from
                             # directly above, and because a green-grey crown
                             # over a navy mansard is the more legible toy read.
    "Toy_sand": "ece4d4",    # the flat roof membrane deck. Pale on purpose: a
                             # dark deck measured 27% darker than its baked
                             # neighbours on 524-second and read as a hole.
    "Toy_steel": "9aa0a6",   # rooftop plant and hatch
    "Toy_gold_Glow": "caa64a",   # the entablature sign band - the night hero,
                             # running all 70 m of public elevation
    "Toy_glassl_Glow": "6f95b8",  # the lit windows at night. NOT Toy_glass_Glow
                             # (2a4d73): the app draws _Glow in a separate UNLIT
                             # layer, so at night the surface shows its RAW BASE
                             # COLOUR, and 2a4d73 is the dark navy of UNlit
                             # glass. The plan asked for "Toy_glass_Glow
                             # #6f95b8", which is a name/hex contradiction; the
                             # hex is the correct half. See REPORT.md 2.
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


_FN = _brg(FRONT_BEARING)             # outward from Mission Street (NW)
_FT = _brg(FRONT_BEARING + 90.0)      # along Mission, W corner -> N corner

W_COR = (_FN[0] * DEPTH / 2.0 - _FT[0] * FRONTAGE / 2.0,
         _FN[1] * DEPTH / 2.0 - _FT[1] * FRONTAGE / 2.0)
N_COR = (W_COR[0] + _FT[0] * FRONTAGE, W_COR[1] + _FT[1] * FRONTAGE)
E_COR = (N_COR[0] - _FN[0] * DEPTH, N_COR[1] - _FN[1] * DEPTH)
S_COR = (W_COR[0] - _FN[0] * DEPTH, W_COR[1] - _FN[1] * DEPTH)

FOOTPRINT = [W_COR, N_COR, E_COR, S_COR]
CX = sum(p[0] for p in FOOTPRINT) / 4.0
CY = sum(p[1] for p in FOOTPRINT) / 4.0


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
        # +1 when (t, n) is right-handed, -1 when the outward test had to negate
        # the normal. The two ends of this building have OPPOSITE handedness, so
        # anything wound by hand in face coordinates - the glow strips - has to
        # ask, or half of them end up facing into the building.
        self.hand = 1.0 if (self.t[0] * nrm[1] - self.t[1] * nrm[0]) > 0.0 else -1.0
        self.heading = (math.degrees(math.atan2(nrm[0], nrm[1])) + 360.0) % 360.0

    def xy(self, t, d):
        return (self.a[0] + self.t[0] * t + self.n[0] * d,
                self.a[1] + self.t[1] * t + self.n[1] * d)

    def rect(self, t0, t1, d0, d1):
        return [self.xy(t0, d0), self.xy(t1, d0), self.xy(t1, d1), self.xy(t0, d1)]


MISSION = Face(W_COR, N_COR)    # the address elevation, faces 315.2
EMBARC = Face(N_COR, E_COR)     # The Embarcadero end,   faces  45.2
PARTY = Face(E_COR, S_COR)      # blind party wall,      faces 135.2
STEUART = Face(W_COR, S_COR)    # Steuart Street end,    faces 225.2

# The three exposed elevations, in the order the bay loops walk them.
PUBLIC = (("f", MISSION, N_BAY_FRONT), ("e", EMBARC, N_BAY_END),
          ("s", STEUART, N_BAY_END))


def bay_centres(face, n):
    return [face.length * (i + 0.5) / n for i in range(n)]


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


def plate(name, poly3d_a, poly3d_b, mat):
    """Closed solid between two matching 3D rings (a loft with caps)."""
    n = len(poly3d_a)
    verts = list(poly3d_a) + list(poly3d_b)
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    return new_mesh(name, verts, faces, [mat], None)


def glow_quad(name, corners, mat):
    """A single OUTWARD-facing quad. Night glow is never a closed shell: the app
    draws _Glow in a separate layer that is translucent by day, so a closed box
    shows its front AND back face and reads at roughly twice the intended day
    alpha - enough to tint a whole facade."""
    return new_mesh(name, list(corners), [(0, 1, 2, 3)], [mat], recalc=False)


def face_glow(name, face, t0, t1, z0, z1, proud, mat):
    """Glow strip in a Face frame, wound so its single face points outward.

    The loop t0->t1->t1->t0 (bottom left, bottom right, top right, top left) has
    the normal t x z, which is MINUS the outward normal on a right-handed face
    and PLUS it on a left-handed one. Reversing by handedness is the whole fix:
    the first build wound all of them the same way and every glow strip on
    Mission, The Embarcadero and the party wall pointed into the building - 475
    of 31,500 validator rays, 1.5% against a 0.15% tolerance, and by day the app
    would have drawn them on the wrong side of the wall they light."""
    c = [face.xy(t0, proud) + (z0,), face.xy(t1, proud) + (z0,),
         face.xy(t1, proud) + (z1,), face.xy(t0, proud) + (z1,)]
    if face.hand > 0.0:
        c.reverse()
    return glow_quad(name, c, mat)


def bevel(obj, width=BEVEL_W, segments=BEVEL_SEG):
    """Miniature-style edge softening (style bible s.4). The offset is capped at
    a third of the object's thinnest dimension: glass panels, bands and glow
    strips are only 20-160 mm thick and a full bevel on those collapses opposing
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


def _winding(poly):
    s2 = 0.0
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        s2 += a[0] * b[1] - b[0] * a[1]
    return 1.0 if s2 > 0.0 else -1.0


def inset_polygon(poly, dists):
    """Offset each edge i of a simple polygon inward by dists[i] and re-intersect
    adjacent edges. A scalar `dists` insets uniformly; negative offsets outward.

    Which side is "inward" is decided by the polygon's own WINDING, not by which
    side the centroid happens to be on. Per-edge distances are what build the
    mansard: three sides lean in 1.60 m and the party wall leans in 0.00 m, so a
    uniform inset cannot express this roof."""
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
        out.append((p0[0] + d0[0] * t, p0[1] + d0[1] * t))
    return out


# The mansard leans in on the three exposed elevations only. Edge order follows
# FOOTPRINT: W->N Mission, N->E Embarcadero, E->S party wall, S->W Steuart.
MANSARD_DISTS = [MANSARD_IN, MANSARD_IN, 0.0, MANSARD_IN]
DECK_POLY = inset_polygon(FOOTPRINT, MANSARD_DISTS)


# ------------------------------------------------------------ facade pieces


def arch_outline(face, t_c, w, z0, z_spring, rise, segs=5):
    """A round-headed opening profile in a Face's (t, z) plane: vertical jambs to
    the springing, then a segmental head. Returned as a list of (t, z)."""
    h = w / 2.0
    r = (h * h + rise * rise) / (2.0 * rise)
    cz = z_spring + rise - r
    half = math.asin(min(1.0, h / r))
    # The arc's own endpoints ARE the springing points, so listing the springing
    # separately duplicates a vertex and gives every opening a zero-area quad on
    # each of its four strips: 228 degenerate triangles across the model in the
    # first build, and a normals ray test that cannot resolve them.
    pts = [(t_c - h, z0)]
    for i in range(segs + 1):
        a = -half + 2.0 * half * i / segs
        pts.append((t_c + r * math.sin(a), cz + r * math.cos(a)))
    pts.append((t_c + h, z0))
    return pts


def face_profile_solid(name, face, prof, d0, d1, mat):
    """Extrude a (t, z) profile outward through the wall between depths d0..d1."""
    inner = [face.xy(t, d0) + (z,) for t, z in prof]
    outer = [face.xy(t, d1) + (z,) for t, z in prof]
    return plate(name, inner, outer, mat)


def face_ring_solid(name, face, outer_prof, inner_prof, d0, d1, mat):
    """A picture-frame ring between two (t, z) profiles with equal point counts,
    extruded between depths d0..d1.

    The first build made this a filled arch plate, which simply covered the
    glazing behind it: every brick-storey opening rendered as a solid cream
    arch. A ring is four quad strips - front, back, outer wall, inner wall -
    and is the only construction that leaves a hole for the glass."""
    n = len(outer_prof)
    assert n == len(inner_prof)
    oa = [face.xy(t, d0) + (z,) for t, z in outer_prof]
    ob = [face.xy(t, d1) + (z,) for t, z in outer_prof]
    ia = [face.xy(t, d0) + (z,) for t, z in inner_prof]
    ib = [face.xy(t, d1) + (z,) for t, z in inner_prof]
    verts = oa + ob + ia + ib
    O0, O1, I0, I1 = 0, n, 2 * n, 3 * n
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((O0 + i, O0 + j, O1 + j, O1 + i))          # outer wall
        faces.append((I1 + i, I1 + j, I0 + j, I0 + i))          # inner wall
        faces.append((O1 + i, O1 + j, I1 + j, I1 + i))          # front annulus
        faces.append((I0 + i, I0 + j, O0 + j, O0 + i))          # back annulus
    # recalc, NOT an explicit winding. Face.n is negated on the elevations whose
    # (t, n) basis would otherwise point inward, so the two ends of the building
    # have OPPOSITE handedness and one fixed winding is inverted on one of them.
    # The first build wound these by hand and the three Steuart-end surrounds
    # came back with negative signed volume.
    return new_mesh(name, verts, faces, [mat], recalc=True)


def arched_window(name, face, t_c, w, mats, lit=False):
    """One brick-storey opening: a recessed glazed head, a proud white surround,
    and the corbelled brick eyebrow above it read as one arch band."""
    prof = arch_outline(face, t_c, w, WIN_Z[0], WIN_Z[1], WIN_ARCH)
    face_profile_solid(f"{name}_glass", face, prof, -WIN_RECESS, 0.01,
                       mats["Toy_glass"])
    outer = arch_outline(face, t_c, w + 2 * SURROUND, WIN_Z[0] - SURROUND,
                         WIN_Z[1], WIN_ARCH + SURROUND)
    face_ring_solid(f"{name}_surround", face, outer, prof, -EMBED, 0.13,
                    mats["Toy_trim"])
    prism(f"{name}_sill", face.rect(t_c - w / 2 - SURROUND - 0.06,
                                    t_c + w / 2 + SURROUND + 0.06, -EMBED, 0.16),
          WIN_Z[0] - SURROUND - 0.16, WIN_Z[0] - SURROUND, mats["Toy_trim"])
    if lit:
        face_glow(f"{name}_glow", face, t_c - w / 2 + 0.10, t_c + w / 2 - 0.10,
                  WIN_Z[0] + 0.15, WIN_Z[1] + WIN_ARCH - 0.25, 0.035,
                  mats["Toy_glassl_Glow"])


def shopfront_bay(name, face, t_c, pitch, mats):
    """One cast-iron bay: a dark glazed panel between two cream piers, under a
    dark awning. The fluting, the lattice wainscot and the floral 'A' capitals
    are dropped - at 3.2 m of bay they are sub-pixel."""
    gw = pitch - PIER_W - 0.10
    prism(f"{name}_glass", face.rect(t_c - gw / 2, t_c + gw / 2,
                                     -SHOP_INSET - 0.22, -SHOP_INSET + 0.01),
          SHOP_GLASS_Z[0], SHOP_GLASS_Z[1], mats["Toy_ink"])
    prism(f"{name}_awn", face.rect(t_c - gw / 2 - 0.08, t_c + gw / 2 + 0.08,
                                   -SHOP_INSET - EMBED, -SHOP_INSET + AWNING_OUT),
          AWNING_Z, AWNING_Z + AWNING_T, mats["Toy_ink"])


def dormer(name, face, t_c, mats, lit=False):
    """A box punched through the mansard slope with a white pedimented hood. The
    box front sits just proud of the wall plane below, which is how a real
    dormer meets a mansard."""
    t0, t1 = t_c - DORM_W / 2.0, t_c + DORM_W / 2.0
    z1 = DORM_Z0 + DORM_H
    prism(f"{name}_box", face.rect(t0, t1, -DORM_DEEP, DORM_OUT),
          DORM_Z0, z1, mats["Toy_trim"])
    prism(f"{name}_glass", face.rect(t0 + 0.22, t1 - 0.22,
                                     DORM_OUT - 0.10, DORM_OUT + 0.02),
          DORM_Z0 + 0.28, z1 - 0.22, mats["Toy_glassl"])
    # pediment: a triangular prism sitting on the box head
    ta, tb = t0 - PED_OVER, t1 + PED_OVER
    d0, d1 = DORM_OUT - EMBED, DORM_OUT + PED_OUT
    apex = ((ta + tb) / 2.0, z1 + PED_H)
    prof = [(ta, z1 - 0.06), (tb, z1 - 0.06), apex]
    inner = [face.xy(t, d0) + (z,) for t, z in prof]
    outer = [face.xy(t, d1) + (z,) for t, z in prof]
    plate(f"{name}_ped", inner, outer, mats["Toy_trim"])
    if lit:
        face_glow(f"{name}_glow", face, t0 + 0.26, t1 - 0.26,
                  DORM_Z0 + 0.34, z1 - 0.28, DORM_OUT + 0.05,
                  mats["Toy_glassl_Glow"])


def face_box(face, t_c, d_c, w, d):
    """A rectangle in a Face's own frame. Everything that sits ON this building -
    chimneys, plant, hatches, quoins - has to be built this way: the footprint is
    at 45.2 deg to the world axes, so a world-aligned box reads as a DIAMOND from
    directly above. The first build had four chimney caps and four plant blocks
    sitting on the roof at 45 degrees to the building under them."""
    return face.rect(t_c - w / 2.0, t_c + w / 2.0, d_c - d / 2.0, d_c + d / 2.0)


def chimney(name, face, t_c, d_c, mats):
    """Red brick stack with a white corbelled cap, built in the Face frame so it
    stands square to the building. It runs from below the mansard springing to
    just under the vault ridge, so it reads as masonry coming up THROUGH the
    slate rather than a post standing on it - and nothing may out-top Z_CREST."""
    prism(f"{name}_stack", face_box(face, t_c, d_c, CHIMNEY_W, CHIMNEY_D),
          Z_CORBEL - 0.40, CHIMNEY_TOP - CHIMNEY_CAP, mats["Toy_brick"])
    prism(f"{name}_cap",
          face_box(face, t_c, d_c, CHIMNEY_W + 0.20, CHIMNEY_D + 0.20),
          CHIMNEY_TOP - CHIMNEY_CAP - EMBED, CHIMNEY_TOP, mats["Toy_trim"])


def barrel_vault(name, path, mats):
    """Swept semicircular vault along a polyline, mitred at each turn.

    The cross-section frame at an interior vertex uses the ANGLE BISECTOR and is
    widened by 1/sin(half-angle), which is what makes the corner a clean mitre
    instead of a pinch. Springing at Z_DECK, ridge at Z_DECK + VAULT_R = Z_CREST,
    which is the model's height-normalisation target."""
    n = len(path)
    frames = []
    for i, p in enumerate(path):
        if i == 0:
            dx, dy = path[1][0] - p[0], path[1][1] - p[1]
            m = math.hypot(dx, dy)
            u, scale = (-dy / m, dx / m), 1.0
        elif i == n - 1:
            dx, dy = p[0] - path[-2][0], p[1] - path[-2][1]
            m = math.hypot(dx, dy)
            u, scale = (-dy / m, dx / m), 1.0
        else:
            ax, ay = p[0] - path[i - 1][0], p[1] - path[i - 1][1]
            bx, by = path[i + 1][0] - p[0], path[i + 1][1] - p[1]
            ma, mb = math.hypot(ax, ay), math.hypot(bx, by)
            ax, ay, bx, by = ax / ma, ay / ma, bx / mb, by / mb
            # bisector of the incoming and outgoing directions
            sx, sy = ax + bx, ay + by
            ms = math.hypot(sx, sy) or 1e-9
            sx, sy = sx / ms, sy / ms
            u = (-sy, sx)
            cosh = abs(ax * sx + ay * sy)        # cos(half turn)
            scale = 1.0 / max(cosh, 0.25)
        frames.append((p, u, scale))
    # Segmental profile: a circle through (+-VAULT_HW, z_spring) with its crown
    # on Z_CREST. Solving for the centre keeps it at or below the springing, so
    # the vault never overhangs its own curb.
    z_spring = Z_DECK + VAULT_CURB
    drop = (VAULT_HW ** 2 - (Z_CREST - z_spring) ** 2) / (2.0 * (Z_CREST - z_spring))
    drop = max(drop, 0.0)
    cz = z_spring - drop
    rad = Z_CREST - cz
    phi0 = math.atan2(drop, VAULT_HW)
    rings = []
    for (p, u, scale) in frames:
        ring = []
        for k in range(VAULT_SEGS + 1):
            a = phi0 + (math.pi - 2.0 * phi0) * k / VAULT_SEGS
            off = -rad * math.cos(a) * scale
            ring.append((p[0] + u[0] * off, p[1] + u[1] * off, cz + rad * math.sin(a)))
        rings.append(ring)
    verts, faces = [], []
    w = VAULT_SEGS + 1
    for r in rings:
        verts += r
    for i in range(len(rings) - 1):
        for k in range(VAULT_SEGS):
            a = i * w + k
            faces.append((a, a + 1, a + w + 1, a + w))
    # skirts down to the deck, so the vault is a closed solid
    base = len(verts)
    for r in rings:
        verts += [(r[0][0], r[0][1], Z_DECK - 0.12), (r[-1][0], r[-1][1], Z_DECK - 0.12)]
    # (the skirt below is the curb: it drops the springing straight to the deck)
    for i in range(len(rings) - 1):
        a0, b0 = i * w, (i + 1) * w
        a1, b1 = base + i * 2, base + (i + 1) * 2
        faces.append((a0, a1, b1, b0))
        faces.append((b0 + VAULT_SEGS, b1 + 1, a1 + 1, a0 + VAULT_SEGS))
        faces.append((a1, a1 + 1, b1 + 1, b1))
    for idx, sgn in ((0, 0), (len(rings) - 1, 1)):
        ring = list(range(idx * w, idx * w + w))
        cap = ring + [base + idx * 2 + 1, base + idx * 2]
        faces.append(tuple(cap if sgn else reversed(cap)))
    return new_mesh(name, verts, faces, [mats["Toy_verdigris"]])


# --------------------------------------------------------------------- build


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


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    mats = {k: make_material(k) for k in PALETTE}

    # 1. brick body, shopfront to corbel table
    # Z_SHOP - 0.02, not - 0.30: the brick body sits OUTSIDE the inset shopfront,
    # so any part of it below the entablature's underside shows as a stray orange
    # stripe over the cast iron. The first build left a 0.27 m one on all three
    # public elevations.
    prism("body_brick", FOOTPRINT, Z_SHOP - 0.02, Z_CORBEL, mats["Toy_brick"])

    # 2. the cast-iron shopfront band, set back so the brick overhangs it
    shop_poly = inset_polygon(FOOTPRINT, [SHOP_INSET, SHOP_INSET, 0.0, SHOP_INSET])
    prism("shopfront", shop_poly, 0.0, Z_SHOP, mats["Toy_cream"])
    # The shopfront prism is closed, so it also paints the party wall's ground
    # floor cream. There was never any cast iron on a common wall: face it back
    # to brick, so the party-wall render shows blind masonry top to bottom.
    prism("party_base", PARTY.rect(0.0, PARTY.length, -0.30, 0.01), 0.0, Z_SHOP,
          mats["Toy_brick"])
    for tag, face, n in PUBLIC:
        pitch = face.length / n
        for i, t in enumerate(bay_centres(face, n)):
            shopfront_bay(f"shop_{tag}{i}", face, t, pitch, mats)
        for k in range(n + 1):
            t = face.length * k / n
            prism(f"pier_{tag}{k}",
                  face.rect(max(0.0, t - PIER_W / 2), min(face.length, t + PIER_W / 2),
                            -SHOP_INSET - EMBED, -SHOP_INSET + PIER_OUT),
                  0.0, Z_SHOP, mats["Toy_cream"])

    # 3. the entablature - the first white line - with the 1924 nautical frieze
    #    on the Embarcadero half of Mission and around the Embarcadero end only,
    #    and the glowing sign band inside it
    entab_poly = inset_polygon(FOOTPRINT, [-ENTAB_OUT, -ENTAB_OUT, 0.0, -ENTAB_OUT])
    prism("entablature", entab_poly, Z_SHOP - EMBED, Z_ENTAB, mats["Toy_trim"])
    for tag, face, n in PUBLIC:
        if tag == "f":
            fr = [(face.length / 2.0, face.length)]      # Embarcadero half only
        elif tag == "e":
            fr = [(0.0, face.length)]
        else:
            fr = []
        for j, (t0, t1) in enumerate(fr):
            prism(f"frieze_{tag}{j}",
                  face.rect(t0 + 0.10, t1 - 0.10, ENTAB_OUT - 0.18, ENTAB_OUT + 0.02),
                  FRIEZE_Z[0], FRIEZE_Z[1], mats["Toy_cream"])
        face_glow(f"sign_{tag}_glow", face, 0.35, face.length - 0.35,
                  SIGN_Z[0], SIGN_Z[1], ENTAB_OUT + 0.04, mats["Toy_gold_Glow"])

    # 4. the brick storey: white quoins at the three exposed corners, arched
    #    openings under corbelled eyebrows
    for tag, face, n in PUBLIC:
        lit = {"f": LIT_FRONT, "e": LIT_END_E, "s": LIT_END_S}[tag]
        w = WIN_W * (END_WIN_SCALE if tag in ("e", "s") else 1.0)
        for i, t in enumerate(bay_centres(face, n)):
            arched_window(f"win_{tag}{i}", face, t, w, mats, lit=i in lit)
    # Quoins wrap a corner, so each is TWO proud strips, one per meeting face,
    # built in those faces' own frames. A single world-aligned square - which is
    # what the first build used - sticks a 0.57 m diagonal spur out past the wall
    # on a building set at 45 deg, and rendered as a slab floating off the end
    # elevation. Only the two fully exposed corners get them: the party wall has
    # no quoins on the real building.
    for cname, faces in (("N", ((MISSION, MISSION.length), (EMBARC, 0.0))),
                         ("W", ((MISSION, 0.0), (STEUART, 0.0)))):
        for k, (face, t_end) in enumerate(faces):
            t_c = (QUOIN_W / 2.0) if t_end == 0.0 else (t_end - QUOIN_W / 2.0)
            prism(f"quoin_{cname}{k}",
                  face.rect(t_c - QUOIN_W / 2.0, t_c + QUOIN_W / 2.0,
                            -EMBED, QUOIN_OUT),
                  Z_ENTAB, Z_BRICK, mats["Toy_trim"])

    # 5. the corbel table - the second white line
    corbel_poly = inset_polygon(FOOTPRINT, [-CORBEL_OUT, -CORBEL_OUT, 0.0, -CORBEL_OUT])
    prism("corbel_table", corbel_poly, Z_BRICK, Z_CORBEL, mats["Toy_trim"])

    # 6. the mansard: slate on the three exposed faces, brick straight up on the
    #    party wall, capped by the pale membrane deck
    # Z_CORBEL - 0.10, not Z_CORBEL: the brick body's top cap already sits on
    # Z_CORBEL, and two coincident 585 m2 horizontal faces make the first-hit
    # direction of a ray ambiguous for anything that reaches them.
    bot = [(x, y, Z_CORBEL - 0.10) for x, y in FOOTPRINT]
    top = [(x, y, Z_DECK) for x, y in DECK_POLY]
    n = len(bot)
    verts = bot + top
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    face_mats = [0, 0, 1, 0]                    # edge 2 (E->S) is the party wall
    faces.append(tuple(range(n - 1, -1, -1)))
    face_mats.append(1)
    faces.append(tuple(range(n, 2 * n)))
    face_mats.append(2)
    new_mesh("mansard", verts, faces,
             [mats["Toy_navy"], mats["Toy_brick"], mats["Toy_sand"]], face_mats)

    # 7. crown moulding at the mansard crest, three sides only
    crown_out = inset_polygon(DECK_POLY, [-CROWN_OUT, -CROWN_OUT, 0.0, -CROWN_OUT])
    crown_in = inset_polygon(DECK_POLY, [0.18, 0.18, 0.0, 0.18])
    ring_a = [(x, y, CROWN_Z[0]) for x, y in crown_out]
    ring_b = [(x, y, CROWN_Z[1]) for x, y in crown_out]
    plate("crown", ring_a, ring_b, mats["Toy_trim"])
    del crown_in

    # 8. dormers, one per bay on the three exposed faces
    for tag, face, n in PUBLIC:
        lit = {"f": LIT_DORM_FRONT, "e": LIT_DORM_END_E, "s": LIT_DORM_END_S}[tag]
        for i, t in enumerate(bay_centres(face, n)):
            dormer(f"dorm_{tag}{i}", face, t, mats, lit=i in lit)

    # 9. chimneys: the two fully exposed corners, the two party-wall corners, and
    #    three along Mission at bay boundaries
    for cname, face, t_c in (("W", MISSION, CHIMNEY_W / 2.0 + 0.05),
                             ("N", MISSION, MISSION.length - CHIMNEY_W / 2.0 - 0.05),
                             ("E", EMBARC, EMBARC.length - CHIMNEY_W / 2.0 - 0.05),
                             ("S", STEUART, STEUART.length - CHIMNEY_W / 2.0 - 0.05)):
        chimney(f"chim_{cname}", face, t_c, -CHIMNEY_D / 2.0 - 0.05, mats)
    for k in CHIMNEY_FRONT_K:
        chimney(f"chim_f{k}", MISSION, MISSION.length * k / N_BAY_FRONT,
                -CHIMNEY_D / 2.0 - 0.05, mats)

    # 10. the barrel vault - the 1984 penthouse and the crest
    path = [STEUART.xy(VAULT_END_T, -VAULT_OFFSET),
            MISSION.xy(VAULT_OFFSET, -VAULT_OFFSET),
            MISSION.xy(MISSION.length - VAULT_OFFSET, -VAULT_OFFSET),
            EMBARC.xy(VAULT_END_T, -VAULT_OFFSET)]
    barrel_vault("vault", path, mats)

    # 11. roof plant, grouped against the party wall so the vault ribbon stays
    #     unbroken. This is what DataSF's 19.18 m maximum is measuring; here it
    #     is modelled honestly and kept well under the crest.
    for i, (tt, dd, w, d, h) in enumerate(((16.4, 10.9, 3.2, 2.3, 1.70),
                                           (20.6, 11.3, 2.2, 1.7, 1.25),
                                           (24.2, 10.7, 2.6, 2.0, 1.45),
                                           (28.0, 11.4, 1.6, 1.4, 0.95))):
        prism(f"plant_{i}", face_box(MISSION, tt, -dd, w, d),
              Z_DECK - 0.05, Z_DECK + h, mats["Toy_steel"])
    prism("hatch", face_box(MISSION, 34.5, -10.2, 1.5, 1.2),
          Z_DECK - 0.05, Z_DECK + 0.55, mats["Toy_steel"])
    # The party wall carries a low brick firewall above the deck. It is true of
    # the real building, and it is what stops 586 m2 of pale membrane reading as
    # an open tray with one green ribbon dropped into it.
    prism("firewall", PARTY.rect(0.0, PARTY.length, -0.75, 0.0),
          Z_DECK - 0.10, Z_DECK + 0.62, mats["Toy_brick"])

    # 12. bevels. Applied bands, glazing and glow strips are left sharp or
    #     lightly bevelled: they are 20-160 mm thick and a full bevel collapses
    #     their opposing profiles.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        nm = obj.name
        if "_glow" in nm or "sign_" in nm:
            continue
        # The vault is already a swept arc: bevelling it costs triangles, adds
        # nothing at this scale, and rounds 5 mm off the ridge - which is the
        # model's height-normalisation target and has to land on 17.50 exactly.
        if nm == "vault":
            continue
        # The brick-storey openings are left SHARP. Each is a thin ring plus a
        # recessed glazed plate on a nine-point arch profile, and a one-segment
        # 40 mm bevel tripled them: 7,618 triangles for nineteen windows, more
        # than half the whole budget, for an arris nobody can see at 3.2 m of
        # bay. Sharp they cost 2.0k, which is what the plan allowed for them.
        if nm.startswith("win_"):
            continue
        if nm.startswith(("frieze_", "shop_", "dorm_")) or "_cap" in nm:
            bevel(obj, width=0.04, segments=1)
        elif nm.startswith(("entablature", "corbel_table", "crown", "pier_",
                            "quoin_", "plant_", "hatch")):
            bevel(obj, width=0.05, segments=1)
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
    print(f"[build] Mission {MISSION.heading:.2f} deg; Embarcadero {EMBARC.heading:.2f}; "
          f"party {PARTY.heading:.2f}; Steuart {STEUART.heading:.2f}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "audiffred-building.blend")
    glb = os.path.join(out, "audiffred-building.glb")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    bpy.ops.export_scene.gltf(
        filepath=glb, export_format="GLB", export_apply=True, export_yup=True,
        use_selection=False, export_cameras=False, export_lights=False,
        export_animations=False, export_skins=False, export_morph=False,
        export_materials="EXPORT", export_image_format="NONE",
    )
    print(f"[build] wrote {blend}")
    print(f"[build] wrote {glb}")


if __name__ == "__main__":
    main()
