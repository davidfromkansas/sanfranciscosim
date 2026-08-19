"""Deterministic Blender build of the SF-SIM miniature 45-49 South Park
(the Gran Oriente Filipino Residence).

    blender -b --python build_49_south_park.py -- [--out DIR]

Writes 49-south-park.blend and 49-south-park.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading - the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, corner-bay crown exactly
13.00 m.

Design (see REFERENCE.md for the sources behind every number):

* a 1909 three-storey-over-raised-basement Edwardian flats building, wood frame,
  7 units, on the corner of the South Park oval and Jack London Alley. Bought by
  the Gran Oriente Filipino - the first Filipino-founded Masonic lodge in the
  United States - in September 1947 and still owned by them. Half of a proposed
  Article 10 landmark complex whose other half, 104-106 South Park, is already in
  this manifest as `106-south-park`;
* the recognition rests entirely on the BAYS. Seven of them: three rounded (one
  per exposed corner) and four canted between them, all spanning the second and
  third storeys only, all carried on one shared bracket shelf, all capped by one
  unbroken bracketed cornice. The hero is the rounded corner TURRET that wraps
  the South Park x Jack London Alley corner and whose crown is the tallest point
  of the building;
* two elevations are hero elevations. The north-west front (12.90 m) faces the
  park; the south-west flank (17.70 m) faces the alley and is fully exposed. Only
  the north-east side is a party wall, shared with 41-43 South Park (2.3 m
  shorter, so the top of this wall shows in the baked city);
* the ground floor is the odd, heraldic part: two entrances recessed behind iron
  gates and flanked by columns with Corinthian capitals, with four QUATREFOIL
  stained-glass rosettes distributed around them. At 13 m of frontage the real
  0.9 m rosettes are sub-pixel, so they are exaggerated to 1.30 m - the one place
  the ground-floor detail budget is spent;
* under all of it a dark raised basement of painted brick with a thin red-oxide
  water-table stripe at its head. Base / body / cap is what makes this read as an
  SF Edwardian rather than a box;
* the roof is flat at 12.05 m (DataSF LiDAR median 12.08 m over 1,099 cells,
  sigma 0.73; OSM way/71211339 tags height=12) with the cornice crest at 12.30 m
  and the turret crown at 13.00 m (LiDAR hgt_max 13.00 m). From above the story
  is the cornice RING: it is not a rectangle, the bays push it out into three
  rounded and four canted bulges along two of its four sides;
* night state: the turret fully lit plus an uneven scatter of the other bays -
  seven apartments, not an office floor - and a warm spill in the two entrance
  recesses. Glow surfaces are single faces standing proud of the opaque glazing,
  never closed shells: the app renders _Glow in a separate layer and a closed
  shell is two alpha layers deep, so it reads far brighter by day than intended.

Authoring frame: the footprint is a clean rectangle at 45.8 deg to the world
axes, so everything is placed through Face frames built from the four measured
wall-box corners. Because the building sits at 45 deg the axis-aligned XY
bounding box is ~22 x 22 m even though the building is 12.90 x 17.70 m. That is
expected, not a scale error.
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
DESIGN_ANCHOR = (-122.3935869, 37.7814643)

# Wall box, from the DataSF LiDAR footprint 201006.0014671 (mblr SF3775039):
# its 12.88 m front edge and its 17.71 m south-west flank edge are the two clean
# measured sides. The rest of the 278.6 m2 outline is bay and cornice overhang
# plus the rear stairs, which is exactly what a roof-derived outline traces.
FRONTAGE = 12.90
DEPTH = 17.70
FRONT_BEARING = 315.8      # the South Park elevation faces north-west
FLANK_BEARING = 225.8      # the Jack London Alley flank faces south-west

Z_BASE = 1.50              # top of the raised basement
Z_ST1 = 4.80               # top of the first storey / underside of the bays
Z_ST3 = 11.20              # top of the third storey / cornice springing
Z_DECK = 12.05             # flat roof deck - MEASURED (LiDAR median 12.08 m)
Z_CREST = 12.30            # cornice crest
Z_CROWN = 13.00            # turret crown - MEASURED (LiDAR hgt_max 13.00 m) and
                           # the bbox top, so the loader's targetHeightM /
                           # measuredHeight lands on exactly 1.0

BASE_PROUD = 0.06          # the basement stands slightly proud of the siding
STRIPE_H = 0.10            # red-oxide water table at the head of the basement

# Bay sizes and the cornice projection are coupled and were tuned together at
# stage 2. The cornice follows the bay outline, so its outward offset has to fit
# inside the flat gap between two neighbouring bays: with the plan's 3.40 m
# rounded / 3.00 m canted bays the front's three gaps came out at 0.15-1.00 m,
# the 0.55 m cornice crossed itself in them, and the render showed black wedges
# where the offset polygon folded through itself. Shrinking the bays to
# 3.10 / 2.60 and the cornice to 0.38 puts every front gap at 0.83 m, which is
# wider than two 0.38 m offsets meeting. See REPORT.md 2.
BAY_PROJ = 0.90            # canted and flat-wall rounded bays
BAY_CHORD_R = 3.10         # rounded bay chord
BAY_CHORD_C = 2.60         # canted bay chord
BAY_FACE_C = 1.70          # canted bay front face
ROUND_SEGS = 6
TURRET_ATTACH = 2.10       # turret pickup along each wall from the corner
TURRET_REACH = 1.15        # how far the turret bulges past the corner point
TURRET_SEGS = 8

SHELF_Z0, SHELF_Z1 = 4.55, 4.80   # the one shared bracket shelf under every bay
SHELF_PROUD = 0.10

GLASS2_Z = (5.50, 7.45)    # second-storey bay glazing band
GLASS3_Z = (8.70, 10.65)   # third-storey bay glazing band
GLASS_PROUD = 0.035
FRAME_PROUD = 0.10
EMBED = 0.03               # how far every applied band is sunk INTO the surface
                           # it sits on. Nothing in this model is allowed to have
                           # a face exactly coincident with another solid's face:
                           # coincident faces make the first-hit direction of a
                           # ray ambiguous, and the contract's normals ray test
                           # counts the ambiguity as a flipped face. Measured at
                           # stage 4: 21 of 17,312 first hits (0.12%) before this
                           # constant existed, all of them on bay glazing bands,
                           # bay frames and cornice steps whose inner face lay
                           # exactly on the wall. Overlapping solids are the
                           # supported model here - the validator's authoritative
                           # normals test is per-object signed volume.
FRAME_H = 0.15
GLASS_INSET = 0.32         # how far the glazing band stops short of the wall at
                           # each end of a bay, so the body colour shows at every
                           # bay junction instead of one continuous blue ring

CORN_Z = (11.20, 11.44, 11.70, 12.30)
CORN_OUT = (0.12, 0.24, 0.38)
BRACKET = (0.22, 0.30, 0.26)      # width along the wall, depth out, height
BRACKET_PITCH = 0.62

WIN_W, WIN_H, WIN_RECESS = 1.10, 2.10, 0.12
BWIN_W, BWIN_H = 0.70, 0.45       # basement openings
ENT_W, ENT_H, ENT_D = 1.60, 2.90, 0.35
COL_R, COL_H = 0.15, 2.90
QUAT_D = 1.30                     # quatrefoil rosette across - EXAGGERATED from
                                  # the real ~0.90 m, see REFERENCE.md
QUAT_Z = 3.85

# Ground-floor front layout, t metres from the WEST (alley) corner. Read off the
# January 2017 designation-report photograph: window, rosette, entrance, two
# rosettes, entrance, rosette, window.
FRONT_WIN_T = (0.95, 11.95)
FRONT_ENT_T = (4.10, 8.80)
FRONT_QUAT_T = (2.50, 5.70, 7.20, 10.40)

FLANK_WIN_T = (3.30, 4.60, 6.80, 8.10, 10.30, 11.60, 13.80, 15.10)
FRONT_BWIN_T = (2.00, 4.10, 6.40, 8.80, 11.00)
FLANK_BWIN_T = (2.50, 5.00, 7.50, 10.00, 12.50, 15.00)

# Bays, t metres from the WEST corner along each elevation. The turret is not in
# these lists: it is centred on the corner itself and belongs to neither face.
FRONT_ROUND_T = (11.34,)
FRONT_CANT_T = (4.23, 7.66)
FLANK_ROUND_T = (16.15,)
FLANK_CANT_T = (5.83, 10.86)

# Which bays are lit at night, by object-name prefix. Uneven on purpose.
LIT_BAYS = {"turret": (True, True), "front_round_0": (False, True),
            "front_cant_0": (True, False), "front_cant_1": (False, False),
            "flank_round_0": (True, True), "flank_cant_0": (False, True),
            "flank_cant_1": (True, False)}

BEVEL_W, BEVEL_SEG = 0.10, 2

PALETTE_HEX = {
    "Toy_sage": "b5b4a2",    # the body - all three storeys of wall and every
                             # bay's solid faces. The pale, faintly green-grey
                             # painted wood siding. OFF-PALETTE (a WARN, not a
                             # fail) and deliberate: this is the style bible's SF
                             # painted-residential exception, the palette has no
                             # pale sage, and the whole elevation depends on the
                             # BODY reading a clear step darker than the cream
                             # trim. Toy_stone (d9d2c2) was the plan's choice and
                             # was tried first; at stage 2 it rendered as a
                             # second cream and the seven bays vanished into
                             # their own trim - see REPORT.md 1. The VALUE
                             # relations (pale body, lighter trim, much darker
                             # basement, thin red line) are confident; the hue is
                             # read from two January 2017 photographs taken
                             # overcast, in shadow, behind a street tree.
                             # Deliberately NOT Toy_cream either: 104-106 South
                             # Park is Toy_cream and sits 90 m away on the same
                             # oval under the same owner.
    "Toy_trim": "f3efe6",    # cornice, brackets, bay frames, window trim and
                             # sills, columns, quatrefoil plates, vent stacks
    "Toy_roofd": "45454a",   # the raised basement (painted brick) and the roof
                             # mechanical block. The palette has no true olive;
                             # this is the closest to the real dark grey-green.
    "Toy_red": "c4453c",     # the water-table stripe at the head of the basement
    "Toy_glass": "2a4d73",   # all windows and all bay glazing
    "Toy_navy": "2c4a70",    # the quatrefoil rosettes' glazed centres
    "Toy_ink": "3a3530",     # entrance openings and gates, basement openings,
                             # roof hatch
    "Toy_steel": "9aa0a6",   # the flat roof deck. Satellite imagery shows a
                             # taupe / warm mid-grey membrane, clearly darker
                             # than the near-white roofs across the alley.
    "Toy_glassl": "6f95b8",  # the roof skylight bank
    "Toy_glassl_Glow": "6f95b8",  # the lit bay windows at night.
                             # NOT Toy_glass_Glow (2a4d73). The app draws _Glow
                             # in a separate UNLIT layer at opacity
                             # 0.12 + 0.95*uNight, so at night the surface shows
                             # its raw base colour - and 2a4d73 is the dark navy
                             # of unlit glass, which renders as a dark window
                             # pretending to be a lit one. The Blender night
                             # render hid it, because emission strength 4.2 made
                             # even a dark colour bright; the app does not
                             # multiply by anything. Caught in local QA at 22:30
                             # against neighbours whose windows were plainly
                             # brighter. See REPORT.md 6.
    "Toy_trim_Glow": "f3efe6",
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


# The wall box, laid out from its centre. FRONT_BEARING is the outward normal of
# the park elevation, so the front edge itself runs at FRONT_BEARING + 90.
_FN = _brg(FRONT_BEARING)             # outward from the front (NW)
_FT = _brg(FRONT_BEARING + 90.0)      # along the front, W corner -> N corner
_KN = _brg(FLANK_BEARING)             # outward from the alley flank (SW)

_C = (0.0, 0.0)
W_COR = (_C[0] + _FN[0] * DEPTH / 2.0 - _FT[0] * FRONTAGE / 2.0,
         _C[1] + _FN[1] * DEPTH / 2.0 - _FT[1] * FRONTAGE / 2.0)
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
        self.a = a
        self.b = b
        self.length = n
        self.t = (dx / n, dy / n)
        nrm = (-self.t[1], self.t[0])
        if (a[0] + nrm[0] - CX) ** 2 + (a[1] + nrm[1] - CY) ** 2 < (a[0] - CX) ** 2 + (
            a[1] - CY
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


FRONT = Face(W_COR, N_COR)    # South Park, faces 315.8
PARTY = Face(N_COR, E_COR)    # 41-43 South Park, faces 45.8
REAR = Face(E_COR, S_COR)     # the gap and the Masonic Temple, faces 135.8
FLANK = Face(W_COR, S_COR)    # Jack London Alley, faces 225.8


# --------------------------------------------------------------- bay outlines


def round_bay_arc(face, t_c, chord=BAY_CHORD_R, proj=BAY_PROJ, segs=ROUND_SEGS):
    """Circular-segment bay on a straight wall. Returns arc points in world XY,
    running in the direction of increasing t. Both endpoints sit exactly on the
    wall line, so the arc can be spliced straight into the building outline."""
    r = (chord * chord / 4.0 + proj * proj) / (2.0 * proj)
    dc = proj - r
    half = math.asin((chord / 2.0) / r)
    pts = []
    for i in range(segs + 1):
        ang = -half + (2.0 * half) * i / segs
        pts.append(face.xy(t_c + r * math.sin(ang), dc + r * math.cos(ang)))
    return pts


def cant_bay_arc(face, t_c, chord=BAY_CHORD_C, front=BAY_FACE_C, proj=BAY_PROJ):
    """Canted (angled) bay: two returns and a flat face. Endpoints on the wall."""
    lat = (chord - front) / 2.0
    return [
        face.xy(t_c - chord / 2.0, 0.0),
        face.xy(t_c - front / 2.0, proj),
        face.xy(t_c + front / 2.0, proj),
        face.xy(t_c + chord / 2.0, 0.0),
    ]


def turret_arc(segs=TURRET_SEGS, attach=TURRET_ATTACH, reach=TURRET_REACH):
    """The rounded corner bay that wraps the West corner. Built in the corner's
    own (e, g) frame: e outward along the corner bisector, g across it. Runs from
    the FLANK wall round to the FRONT wall, i.e. in the direction of increasing
    t on the front."""
    bis = (FRONT_BEARING + FLANK_BEARING) / 2.0          # 270.8 deg, due west
    e = _brg(bis)
    g = _brg(bis + 90.0)
    a = attach / math.sqrt(2.0)
    c = (reach ** 2 - 2.0 * a * a) / (2.0 * a + 2.0 * reach)
    r = reach - c
    half = math.atan2(a, -(a + c))
    pts = []
    for i in range(segs + 1):
        ang = -half + (2.0 * half) * i / segs
        de = c + r * math.cos(ang)
        dg = r * math.sin(ang)
        pts.append((W_COR[0] + e[0] * de + g[0] * dg,
                    W_COR[1] + e[1] * de + g[1] * dg))
    return pts


def bay_outline():
    """The building outline with every bay spliced in: one simple polygon that
    the cornice can follow. Walk N -> E -> S (plain walls), then up the flank to
    the West corner picking up its bays in decreasing t, round the turret, then
    along the front in increasing t."""
    poly = [N_COR, E_COR]
    for t_c in sorted(FLANK_ROUND_T + FLANK_CANT_T, reverse=True):
        arc = (round_bay_arc(FLANK, t_c) if t_c in FLANK_ROUND_T
               else cant_bay_arc(FLANK, t_c))
        poly += list(reversed(arc))
    poly += turret_arc()
    for t_c in sorted(FRONT_ROUND_T + FRONT_CANT_T):
        poly += (round_bay_arc(FRONT, t_c) if t_c in FRONT_ROUND_T
                 else cant_bay_arc(FRONT, t_c))
    return poly


def all_bays():
    """(name, closed plan polygon, open outer polyline) for every bay. The two
    differ only in that the closed form runs back along the wall line; the glow
    strip needs the outer run alone."""
    out = []
    ta = turret_arc()
    out.append(("turret", ta + [W_COR], ta))
    for i, t_c in enumerate(FRONT_ROUND_T):
        a = round_bay_arc(FRONT, t_c)
        out.append((f"front_round_{i}", a, a))
    for i, t_c in enumerate(FRONT_CANT_T):
        a = cant_bay_arc(FRONT, t_c)
        out.append((f"front_cant_{i}", a, a))
    for i, t_c in enumerate(FLANK_ROUND_T):
        a = round_bay_arc(FLANK, t_c)
        out.append((f"flank_round_{i}", a, a))
    for i, t_c in enumerate(FLANK_CANT_T):
        a = cant_bay_arc(FLANK, t_c)
        out.append((f"flank_cant_{i}", a, a))
    return out


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


def glow_band(name, pts, z0, z1, mat, proud):
    """An OPEN, single-layer strip of outward-facing quads along the polyline
    `pts`, pushed `proud` metres out along each segment's outward normal.

    Night glow must never be a closed shell. The app draws _Glow in a separate
    layer that is translucent by day, so a closed box shows its front AND back
    face and reads at roughly twice the intended day alpha - enough to tint a
    whole facade. One layer of one-sided quads is the correct construction, and
    the winding is set explicitly (never recalculated) so the single face points
    out of the building."""
    verts, faces = [], []
    side = _polyline_side(pts)
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy)
        if m < 1e-6:
            continue
        nx, ny = dy / m, -dx / m
        if side > 0.0:
            # The quad's own normal follows (dy, -dx), so flipping the SEGMENT
            # flips the face too - do not just negate the offset. Handedness is
            # taken once for the whole run by _polyline_side().
            a, b = b, a
            nx, ny = -nx, -ny
        a2 = (a[0] + nx * proud, a[1] + ny * proud)
        b2 = (b[0] + nx * proud, b[1] + ny * proud)
        k = len(verts)
        verts += [(a2[0], a2[1], z0), (b2[0], b2[1], z0),
                  (b2[0], b2[1], z1), (a2[0], a2[1], z1)]
        faces.append((k, k + 1, k + 2, k + 3))
    if not faces:
        return None
    return new_mesh(name, verts, faces, [mat], recalc=False)


def bevel(obj, width=BEVEL_W, segments=BEVEL_SEG):
    """Miniature-style edge softening (style bible s.4). The offset is capped at
    a third of the object's thinnest dimension: glass bands, frames and glow
    shells are only 20-160 mm thick and a full bevel on those collapses opposing
    profiles into zero-area slivers even with clamp_overlap."""
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


def _winding(poly):
    """+1 for a counter-clockwise polygon, -1 for clockwise."""
    s2 = 0.0
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        s2 += a[0] * b[1] - b[0] * a[1]
    return 1.0 if s2 > 0.0 else -1.0


def inset_polygon(poly, dist):
    """Offset every edge of a simple polygon inward by `dist` and re-intersect
    adjacent edges. Negative dist offsets outward (a proud band).

    Which side is "inward" is decided by the polygon's own WINDING, not by which
    side the building centroid happens to be on. The centroid test that stood
    here was wrong for exactly the shapes this asset is made of: on the corner
    turret, which sweeps 242 degrees, and on a rounded bay near a far corner,
    some segments' outward normals point back past the centroid, so those
    segments offset the wrong way and the band folded. It cost 36 of 17,316
    first-hit rays at stage 4 - over the 0.15% contract tolerance - before the
    cause was found. See REPORT.md 5."""
    n = len(poly)
    side = _winding(poly)          # interior is left of each edge when CCW
    lines = []
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy)
        if m < 1e-9:
            m = 1e-9
        d = (dx / m, dy / m)
        nrm = (-d[1] * side, d[0] * side)
        lines.append(((a[0] + nrm[0] * dist, a[1] + nrm[1] * dist), d))
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
        # Spike guard. At a REFLEX vertex - which is what every junction between
        # a bay and the wall is, seen from outside - the two offset lines meet
        # far away and the intersection shoots off into a long sail. Capping the
        # displacement at 2x the offset replaces the sail with a chamfer nobody
        # can see at this scale, and is the difference between a clean cornice
        # and a black self-intersecting one.
        v = (q[0] - poly[i][0], q[1] - poly[i][1])
        m = math.hypot(v[0], v[1])
        cap = abs(dist) * 1.30
        if m > cap and m > 1e-9:
            q = (poly[i][0] + v[0] * cap / m, poly[i][1] + v[1] * cap / m)
        out.append(q)
    return out


def relax_polygon(poly, r):
    """Chamfer every REFLEX vertex of a clockwise-wound polygon.

    Offsetting outward is well behaved at a convex corner - the vertex simply
    moves out by dist/cos(half-turn) - but at a reflex corner the two offset
    lines meet in a fold, and an extruded folded polygon renders as black
    wedges with the ring's inside surface pointing at the camera. Every junction
    where a bay meets the wall is reflex, and the turret's are the worst of them
    because it wraps a 90 deg corner and comes back into both walls at a steep
    angle. Replacing each reflex vertex with a short chamfer gives the offset
    somewhere to go. `r` must exceed the largest offset the cornice uses."""
    n = len(poly)
    out = []
    for i in range(n):
        a, c, b = poly[i - 1], poly[i], poly[(i + 1) % n]
        ux, uy = c[0] - a[0], c[1] - a[1]
        vx, vy = b[0] - c[0], b[1] - c[1]
        lu, lv = math.hypot(ux, uy), math.hypot(vx, vy)
        if lu < 1e-9 or lv < 1e-9:
            continue
        if ux * vy - uy * vx <= 0.0:          # convex under clockwise winding
            out.append(c)
            continue
        d = min(r, lu * 0.45, lv * 0.45)
        out.append((c[0] - ux / lu * d, c[1] - uy / lu * d))
        out.append((c[0] + vx / lv * d, c[1] + vy / lv * d))
    return out


def rim(name, poly, inset, z0, z1, mat):
    """Closed band solid between `poly` and its offset - a cornice step or a
    proud string course."""
    inner = inset_polygon(poly, inset)
    n = len(poly)
    verts = [(x, y, z0) for x, y in poly]
    verts += [(x, y, z0) for x, y in inner]
    verts += [(x, y, z1) for x, y in poly]
    verts += [(x, y, z1) for x, y in inner]
    O0, I0, O1, I1 = 0, n, 2 * n, 3 * n
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((O0 + i, O0 + j, O1 + j, O1 + i))
        faces.append((I0 + i, I0 + j, I1 + j, I1 + i))
        faces.append((O0 + i, O0 + j, I0 + j, I0 + i))
        faces.append((O1 + i, O1 + j, I1 + j, I1 + i))
    return new_mesh(name, verts, faces, [mat])


def _polyline_side(pts):
    """Decide, ONCE for a whole open polyline, which side is outward.

    Every polyline here is a convex bay arc traced in one direction, so the
    outward side is constant along it - but it cannot be found per segment from
    the building centroid, because the turret sweeps 242 degrees and its end
    segments face sideways or backwards. The MIDDLE segment always faces
    squarely out, so the handedness is taken from that one and applied to the
    rest."""
    i = max(0, (len(pts) - 1) // 2)
    a, b = pts[i], pts[i + 1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    mid = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
    return 1.0 if (-dy) * (mid[0] - CX) + dx * (mid[1] - CY) > 0.0 else -1.0


def polyline_offset(pts, d):
    """Offset an OPEN polyline by `d` metres along each segment's outward normal
    (outward = away from the footprint centroid), re-intersecting neighbouring
    segments. The endpoints just move perpendicular to their own segment."""
    n = len(pts)
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
        (p0, u0) = lines[i - 1]
        (p1, u1) = lines[i]
        den = u0[0] * u1[1] - u0[1] * u1[0]
        if abs(den) < 1e-9:
            out.append(p1)
            continue
        t = ((p1[0] - p0[0]) * u1[1] - (p1[1] - p0[1]) * u1[0]) / den
        out.append((p0[0] + u0[0] * t, p0[1] + u0[1] * t))
    last, ulast = lines[-1]
    out.append((last[0] + ulast[0] * math.hypot(pts[-1][0] - pts[-2][0],
                                                pts[-1][1] - pts[-2][1]),
                last[1] + ulast[1] * math.hypot(pts[-1][0] - pts[-2][0],
                                                pts[-1][1] - pts[-2][1])))
    return out


def trim_polyline(pts, dist):
    """Shorten an open polyline by `dist` at both ends, so a band laid along it
    stops short of the wall junction and lets the body colour show at the edge of
    every bay."""
    def cut(seq):
        left = dist
        out = list(seq)
        while left > 1e-6 and len(out) > 2:
            a, b = out[0], out[1]
            seg = math.hypot(b[0] - a[0], b[1] - a[1])
            if seg > left + 1e-6:
                f = left / seg
                out[0] = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
                left = 0.0
            else:
                out.pop(0)
                left -= seg
        return out
    return list(reversed(cut(list(reversed(cut(pts))))))


def arc_band(name, pts, z0, z1, d0, d1, mat):
    """A closed solid swept along an OPEN polyline: the cross-section is the
    rectangle (d0..d1) x (z0..z1), where d is measured outward from the wall.

    Bay glazing and bay frames are built this way rather than as outset rings of
    the whole bay polygon. An outset ring wraps the chord too, so the glass ran
    round the back into the wall and every bay read as a solid blue barrel; this
    lays the band on the bay's OUTER faces only."""
    a = polyline_offset(pts, d0)
    b = polyline_offset(pts, d1)
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


def disc(name, cx, cy, z0, z1, r, segs, mat):
    poly = [(cx + r * math.cos(2 * math.pi * i / segs),
             cy + r * math.sin(2 * math.pi * i / segs)) for i in range(segs)]
    return prism(name, poly, z0, z1, mat)


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


def window(name, face, t_c, z_sill, mats, w=WIN_W, h=WIN_H):
    """A recessed opening with a proud sill and trim - the first-storey and flank
    module. The bays carry their own glazing and do not use this."""
    t0, t1 = t_c - w / 2.0, t_c + w / 2.0
    prism(f"{name}_fill", face.rect(t0, t1, -WIN_RECESS, 0.02), z_sill, z_sill + h,
          mats["Toy_glass"])
    prism(f"{name}_sill", face.rect(t0 - 0.10, t1 + 0.10, -EMBED, 0.10),
          z_sill - 0.12, z_sill, mats["Toy_trim"])


def quatrefoil(name, face, t_c, mats):
    """Four overlapping lobes in a heavy cream plate with a dark glazed centre.
    Real diameter is about 0.90 m; this is 1.30 m - the one piece of semantic
    exaggeration on the ground floor, because at 12.90 m of frontage the real
    thing is a couple of pixels and it is what the building is remembered by."""
    r = QUAT_D / 2.0
    lobe = r * 0.42
    off = r - lobe
    for k, (dt, dz) in enumerate(((-off, 0.0), (off, 0.0), (0.0, -off), (0.0, off))):
        poly = []
        for i in range(8):
            a = 2 * math.pi * i / 8
            poly.append(face.xy(t_c + dt + lobe * math.cos(a), 0.02))
        # lobes are built as flat plates in the wall plane: sweep t and z, not d
        verts = []
        for i in range(8):
            a = 2 * math.pi * i / 8
            verts.append(face.xy(t_c + dt + lobe * math.cos(a), 0.0))
        zs = [QUAT_Z + dz + lobe * math.sin(2 * math.pi * i / 8) for i in range(8)]
        v = [(verts[i][0], verts[i][1], zs[i]) for i in range(8)]
        vo = [(p[0] + face.n[0] * 0.10, p[1] + face.n[1] * 0.10, p[2]) for p in v]
        faces = [(i, (i + 1) % 8, 8 + (i + 1) % 8, 8 + i) for i in range(8)]
        faces.append(tuple(range(7, -1, -1)))
        faces.append(tuple(range(8, 16)))
        new_mesh(f"{name}_lobe{k}", v + vo, faces, [mats["Toy_trim"]])
    disc_pts = []
    for i in range(10):
        a = 2 * math.pi * i / 10
        p = face.xy(t_c + r * 0.40 * math.cos(a), 0.11)
        disc_pts.append((p[0], p[1], QUAT_Z + r * 0.40 * math.sin(a)))
    back = [(p[0] - face.n[0] * 0.03, p[1] - face.n[1] * 0.03, p[2]) for p in disc_pts]
    n = len(disc_pts)
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    new_mesh(f"{name}_glass", disc_pts + back, faces, [mats["Toy_navy"]])


def entrance(name, face, t_c, mats):
    """A shallow recess behind a flat dark gate, framed by a pair of columns with
    a chunky square abacus for a Corinthian capital. No fluting, no acanthus, no
    ironwork - all sub-pixel at this scale."""
    t0, t1 = t_c - ENT_W / 2.0, t_c + ENT_W / 2.0
    prism(f"{name}_recess", face.rect(t0, t1, -ENT_D, 0.02), Z_BASE, Z_BASE + ENT_H,
          mats["Toy_ink"])
    prism(f"{name}_head", face.rect(t0 - 0.22, t1 + 0.22, -EMBED, 0.14),
          Z_BASE + ENT_H, Z_BASE + ENT_H + 0.26, mats["Toy_trim"])
    for s, dt in ((0, -1), (1, 1)):
        cx, cy = face.xy(t_c + dt * (ENT_W / 2.0 + 0.20), 0.16)
        disc(f"{name}_col{s}", cx, cy, Z_BASE + 0.14, Z_BASE + COL_H, COL_R, 8,
             mats["Toy_trim"])
        prism(f"{name}_cap{s}",
              face.rect(t_c + dt * (ENT_W / 2.0 + 0.20) - 0.21,
                        t_c + dt * (ENT_W / 2.0 + 0.20) + 0.21, -EMBED, 0.37),
              Z_BASE + COL_H, Z_BASE + COL_H + 0.18, mats["Toy_trim"])
        prism(f"{name}_base{s}",
              face.rect(t_c + dt * (ENT_W / 2.0 + 0.20) - 0.21,
                        t_c + dt * (ENT_W / 2.0 + 0.20) + 0.21, -EMBED, 0.37),
              Z_BASE, Z_BASE + 0.14, mats["Toy_trim"])
    glow_band(f"{name}_glow",
              [face.xy(t0 + 0.12, -ENT_D + 0.04), face.xy(t1 - 0.12, -ENT_D + 0.04)],
              Z_BASE + 0.20, Z_BASE + ENT_H - 0.30, mats["Toy_trim_Glow"], 0.0)


def bay(name, poly, arc, mats):
    """One bay: solid body from the bracket shelf to the cornice springing, a
    shared bracket shelf below it, two glazing bands and their cream frames.

    `poly` is the closed plan polygon (used for the solids); `arc` is the open
    outer polyline only (used for the glow strip, which must not wrap round the
    back onto the wall)."""
    # Up to the DECK, not to Z_ST3. Stopping at the third-storey ceiling left an
    # open well between the bay and the cornice that read from directly above as
    # a dark hole punched in every bulge - see REPORT.md 3.
    prism(f"{name}_body", poly, SHELF_Z1 - EMBED, Z_DECK, mats["Toy_sage"])
    prism(f"{name}_shelf", inset_polygon(poly, -SHELF_PROUD), SHELF_Z0,
          SHELF_Z1 + EMBED, mats["Toy_trim"])
    lit = LIT_BAYS.get(name, (False, False))
    run = trim_polyline(arc, GLASS_INSET)
    for k, (z0, z1) in enumerate((GLASS2_Z, GLASS3_Z)):
        arc_band(f"{name}_glass{k}", run, z0, z1, -EMBED, GLASS_PROUD,
                 mats["Toy_glass"])
        arc_band(f"{name}_frame{k}a", run, z0 - FRAME_H, z0, -EMBED, FRAME_PROUD,
                 mats["Toy_trim"])
        arc_band(f"{name}_frame{k}b", run, z1, z1 + FRAME_H, -EMBED, FRAME_PROUD,
                 mats["Toy_trim"])
        if lit[k]:
            glow_band(f"{name}_glow{k}", run, z0 + 0.10, z1 - 0.10,
                      mats["Toy_glassl_Glow"], GLASS_PROUD + 0.03)


def cornice(poly, mats):
    """Three corbelled steps following the bay outline, so the cornice hugs every
    bay and the ring reads from above as a rectangle with seven bulges. Bracket
    blocks are placed only along the straight wall runs - on the arcs the
    corbelling alone carries the reading, and thirty-four modelled brackets would
    cost more than the whole roof."""
    # Each step is built from a base polygon sunk EMBED into the wall, so the
    # ring's inner surface is buried rather than coincident with the body.
    poly = relax_polygon(poly, CORN_OUT[2] + 0.20)
    base = inset_polygon(poly, EMBED)
    rim("cornice_bed", base, -(CORN_OUT[0] + EMBED), CORN_Z[0], CORN_Z[1],
        mats["Toy_trim"])
    rim("cornice_mid", base, -(CORN_OUT[1] + EMBED), CORN_Z[1], CORN_Z[2],
        mats["Toy_trim"])
    rim("cornice_crown", base, -(CORN_OUT[2] + EMBED), CORN_Z[2], CORN_Z[3],
        mats["Toy_trim"])
    # Bracket blocks go only on the flat runs of the two HERO elevations. The
    # party wall is blind and the rear faces a 6 m gap, so a bracket run there
    # buys nothing and costs ~1,000 triangles; both keep the plain corbelled
    # cornice instead. On the arcs the corbelling alone carries the reading.
    z0 = CORN_Z[1] - BRACKET[2]
    for face, spans in ((FRONT, ((2.20, 2.85),)),
                        (FLANK, ((2.25, 4.40), (7.25, 9.45), (12.25, 14.45)))):
        for t0, t1 in spans:
            n = max(1, int((t1 - t0) / BRACKET_PITCH))
            for i in range(n):
                t = t0 + (t1 - t0) * (i + 0.5) / n
                prism(f"bracket_{face.heading:.0f}_{t:.2f}",
                      face.rect(t - BRACKET[0] / 2.0, t + BRACKET[0] / 2.0,
                                CORN_OUT[0], CORN_OUT[0] + BRACKET[1]),
                      z0, CORN_Z[1], mats["Toy_trim"])


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    mats = {k: make_material(k) for k in PALETTE}

    outline = bay_outline()

    # 1. body: raised basement -> roof deck, in one solid. The top face is the
    #    flat roof membrane, which the cornice ring then stands proud of.
    prism("body", FOOTPRINT, Z_BASE - 0.20, Z_DECK, mats["Toy_sage"],
          mats["Toy_steel"])

    # 2. raised basement, standing slightly proud, with its red water table
    base_poly = inset_polygon(FOOTPRINT, -BASE_PROUD)
    prism("basement", base_poly, 0.0, Z_BASE - STRIPE_H + EMBED,
          mats["Toy_roofd"])
    rim("water_table", inset_polygon(base_poly, EMBED), -(0.03 + EMBED),
        Z_BASE - STRIPE_H, Z_BASE, mats["Toy_red"])
    for t in FRONT_BWIN_T:
        prism(f"bwin_f_{t:.2f}",
              FRONT.rect(t - BWIN_W / 2, t + BWIN_W / 2, BASE_PROUD - 0.10,
                         BASE_PROUD + 0.01),
              0.55, 0.55 + BWIN_H, mats["Toy_ink"])
    for t in FLANK_BWIN_T:
        prism(f"bwin_k_{t:.2f}",
              FLANK.rect(t - BWIN_W / 2, t + BWIN_W / 2, BASE_PROUD - 0.10,
                         BASE_PROUD + 0.01),
              0.55, 0.55 + BWIN_H, mats["Toy_ink"])

    # 3. first storey: the heraldic ground floor on the front, plain on the flank
    for i, t in enumerate(FRONT_WIN_T):
        window(f"fwin_{i}", FRONT, t, Z_BASE + 0.95, mats)
    for i, t in enumerate(FRONT_ENT_T):
        entrance(f"ent_{i}", FRONT, t, mats)
    for i, t in enumerate(FRONT_QUAT_T):
        quatrefoil(f"quat_{i}", FRONT, t, mats)
    for i, t in enumerate(FLANK_WIN_T):
        window(f"kwin_{i}", FLANK, t, Z_BASE + 0.95, mats)

    # 4. the bays - the whole point of the building
    for name, poly, arc in all_bays():
        bay(name, poly, arc, mats)

    # 5. cornice on the bay outline
    cornice(outline, mats)

    # 6. the turret crown: the only thing above the cornice, and the model's
    #    height normalization target (LiDAR hgt_max 13.00 m).
    # Re-derived from the turret's own construction at a smaller attach/reach,
    # never by offsetting the turret polygon. That polygon closes back on W_COR
    # through two wall-line edges, and offsetting it - in either direction -
    # drives a sail out of the shallow junction at each arc end. Two extra calls
    # to turret_arc() are cheaper than any repair.
    prism("crown_step",
          turret_arc(attach=TURRET_ATTACH + 0.40, reach=TURRET_REACH + 0.38)
          + [W_COR], CORN_Z[3] - EMBED, 12.66, mats["Toy_trim"])
    prism("crown_cap",
          turret_arc(attach=TURRET_ATTACH - 0.10, reach=TURRET_REACH + 0.02)
          + [W_COR], 12.66 - EMBED, Z_CROWN, mats["Toy_trim"])

    # 7. roof furniture (2026 satellite imagery: a hatch near the centre, a
    #    skylight bank toward the rear third, vent stacks, one small unit).
    #    Nothing here may approach the crown.
    def rxy(s, u):
        """Roof frame: s metres back from the front wall, u metres across from
        the Jack London Alley wall."""
        return (W_COR[0] - _FN[0] * s + _FT[0] * u, W_COR[1] - _FN[1] * s + _FT[1] * u)

    def rrect(s0, s1, u0, u1):
        return [rxy(s0, u0), rxy(s1, u0), rxy(s1, u1), rxy(s0, u1)]

    # Two brick chimney stacks - a 1909 wood-frame flats building has them, the
    # 2017 corner photograph shows white vent pipes clustered near the park end
    # beside a taller dark stack, and an empty 12 x 18 m deck under the app's
    # aerial camera is the one thing the style bible will not forgive. Nothing
    # here goes above 12.90 m: the turret crown at 13.00 has to stay the tallest
    # geometry or the loader's height normalization picks a chimney.
    prism("roof_chimney_a", rrect(6.4, 7.5, 1.35, 2.35), Z_DECK - EMBED, 12.88,
          mats["Toy_roofd"])
    prism("roof_chimney_b", rrect(13.2, 14.3, 9.2, 10.2), Z_DECK - EMBED, 12.80,
          mats["Toy_roofd"])
    prism("roof_bulkhead", rrect(9.4, 11.6, 4.4, 6.6), Z_DECK - EMBED, 12.72,
          mats["Toy_sage"], mats["Toy_roofd"])
    prism("roof_hatch", rrect(4.6, 5.7, 6.4, 7.5), Z_DECK - EMBED, Z_DECK + 0.30,
          mats["Toy_ink"])
    prism("roof_skylight_a", rrect(13.0, 14.6, 3.2, 6.4), Z_DECK - EMBED, Z_DECK + 0.26,
          mats["Toy_glassl"])
    prism("roof_skylight_b", rrect(15.2, 16.4, 6.9, 9.1), Z_DECK - EMBED, Z_DECK + 0.26,
          mats["Toy_glassl"])
    prism("roof_curb", rrect(2.4, 3.6, 8.6, 11.2), Z_DECK - EMBED, Z_DECK + 0.18,
          mats["Toy_trim"])
    for k, (sv, u) in enumerate(((2.6, 2.2), (3.3, 3.1), (4.1, 2.4),
                                 (11.4, 10.6), (16.2, 2.6))):
        p = rxy(sv, u)
        disc(f"roof_vent{k}", p[0], p[1], Z_DECK - EMBED, Z_DECK + 0.70, 0.13, 6,
             mats["Toy_trim"])

    # 8. rear: one simplified stair box, the only thing the permits record out
    #    there (2010 and 2016 "repair (e) wood stair at rear of building"). It is
    #    invisible from every camera angle the app allows, and it exists so the
    #    rear is not a blank slab.
    prism("rear_stair", REAR.rect(3.2, 7.4, 0.0, 1.60), 0.0, Z_ST1,
          mats["Toy_sage"])
    prism("rear_door", REAR.rect(9.2, 10.4, -0.10, 0.06), Z_BASE,
          Z_BASE + 2.20, mats["Toy_ink"])

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.10/2. Glazing bands, frames, sills, glow shells, rosette lobes and the
    # bracket run are small and numerous - a token softening or none at all is
    # what keeps this under cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        n = obj.name
        if "_glass" in n or "_glow" in n or "_frame" in n or n.endswith("_sill"):
            continue
        # Anything that is already a stepped or faceted profile, or is smaller
        # than the bevel would be visible at, is left sharp. The cornice alone
        # cost 2,800 triangles to bevel and looked identical from the app's
        # camera: three corbelled steps read as chunky whether or not their
        # arrises are rounded.
        if n.startswith(("cornice_", "bracket_", "bwin_", "roof_vent")) \
                or "_lobe" in n or "_col" in n or "_cap" in n or "_base" in n:
            continue
        if n.startswith("water_table") or "_head" in n:
            bevel(obj, width=0.04, segments=1)
        else:
            bevel(obj)

    recentre()
    return scene


# Metres east / north from DESIGN_ANCHOR to the model's XY bbox centre, filled in
# by recentre(). The manifest anchor is DESIGN_ANCHOR moved by this vector, so the
# origin sits at the bbox centre (contract rule 2) while the building still lands
# on its real footprint.
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
    print(f"[build] design (wall-box centre) anchor: {DESIGN_ANCHOR}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] front faces {FRONT.heading:.2f} deg; flank {FLANK.heading:.2f}; "
          f"party {PARTY.heading:.2f}; rear {REAR.heading:.2f}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "49-south-park.blend")
    glb = os.path.join(out, "49-south-park.glb")
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
