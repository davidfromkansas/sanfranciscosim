"""Deterministic Blender build of the SF-SIM miniature 10 South Park
(the South Park Lofts, 1993, Ramon Zambrano).

    blender -b --python build_10_south_park.py -- [--out DIR]

Writes 10-south-park.blend and 10-south-park.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, roof-bulkhead crest
exactly 14.67 m.

Design (see REFERENCE.md for the sources behind every number):

* a 1993 ten-unit live/work loft condominium on the north-east arc of the South
  Park oval, block 3775 lots 106-115, all ten condo lots sharing one 585 m2
  through-lot that runs from South Park at the south-east to Taber Place at the
  north-west. It is TWO buildings — a 262 m2 front block and a 181 m2 rear block
  — around a ~142 m2 landscaped courtyard with a pond;
* the lot is a TRAPEZOID. The oval turns its east end through this frontage, so
  the north-east party wall (against 2 South Park) is 42.34 m and the south-west
  one (against 22-24 South Park) only 36.28 m. The 16.77 m frontage is 8.13 m of
  straight wall facing 135.2 deg, a ~30 deg break, then 8.64 m of shallow arc
  (R 35.3 m, sweep 14.1 deg) facing very nearly due south — 44.5 deg of total
  turn. The arc is built as FOUR segments off the surveyed parcel vertices;
* recognition rests on the WINDOW BANDS. Two stacked 16-foot loft tiers, each
  read as a lower row (square window + round-arched wood French door on a
  wrought-iron juliet balcony) under an upper row that is one 4.9 m window band
  in a broad pale surround, with a LONG FLATTENED OVAL drawn across it in heavy
  mullion. Nothing else on the oval wears that ornament;
* second cue is the COLOUR: apricot stucco on a rim of sage clapboard, cream
  ashlar and red brick;
* third is the plan — a pentagon with a hole in the middle — and the two stacked
  LOGGIAS, 2.4 m wide and recessed 1.2 m, which are the only real depth in the
  elevation and the only thing that reads as shadow from the app's camera;
* both party walls are blind AND buried: 22-24 South Park is 14.22 m and 2 South
  Park 17.72 m, so unlike its neighbours this building never shows a flank;
* height: the roof deck is the LiDAR median, 12.27 m (front block; the rear block
  reads 11.88 m over ground that is 0.47 m higher, so the two decks are level in
  absolute terms and are modelled level here). The parapet crest at 13.10 m is
  PHOTOGRAMMETRIC — derived from Street View pano aFRDCNG9w0lcHJ9ngJI8LQ across
  bearings 314-354 deg, flat to +-0.06 m while the range varied 41%. The 14.67 m
  LiDAR maximum is the roof stair bulkhead and is the bbox top;
* night state: the four front window bands and the Taber Place windows are the
  glow; the loggias, the arched doors, both garages and both roofs stay dark.
  Glow surfaces are thin CLOSED shells (an open face has no signed volume and
  fails the normals contract) covering only part of each band, because a closed
  shell is two alpha layers and reads ~23% by day rather than the nominal 12%.

Authoring frame: world metres east/north from DESIGN_ANCHOR (the parcel's vertex
mean), plus a Face frame per elevation with t along the face and d outward.
Because the lot sits at 45 deg to the world axes the axis-aligned XY bounding box
is ~40 x 36 m even though the lot is 14.2 m by 42.3 m. That is expected, not a
scale error.
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

# Vertex mean of the DataSF surveyed parcel 3775-106 (= 107..115, one geometry).
DESIGN_ANCHOR = (-122.393446, 37.782262)

# Lot vertices, metres east/north from DESIGN_ANCHOR. Everything on the South
# Park front and both party walls is a surveyed parcel vertex; the interior lines
# (front-block rear wall, rear-block front wall, the north-east wing) come from
# the two DataSF LiDAR footprints 201006.0015438 and 201006.0030231.
F_NE = (13.803, -0.051)      # South Park x the 2 South Park party wall
F_BRK = (8.032, -5.777)      # the ~30 deg break in the frontage
A1 = (6.150, -5.600)         # arc
A2 = (3.696, -5.531)         # arc
A3 = (1.851, -5.601)         # arc
F_SW = (-0.588, -5.829)      # South Park x the 22-24 South Park party wall
FB_SW = (-11.746, 5.400)     # front block, rear wall at the SW party wall
FB_NE = (-1.683, 15.534)     # front block, rear wall at the NE party wall
RB_SW = (-18.781, 12.479)    # rear block, front wall at the SW party wall
RB_W = (-10.425, 20.894)     # rear block, front wall, inner end of the wing
RB_WF = (-7.282, 17.773)     # rear block wing, forward face, west end
RB_NE = (-5.593, 19.473)     # rear block wing, forward face at the NE party wall
NE_KINK = (-0.935, 14.782)   # the NE party wall's one surveyed kink
SW_REAR = (-26.162, 19.906)  # Taber Place x the 22-24 party wall
NE_REAR = (-16.036, 29.989)  # Taber Place x the 2 South Park party wall

FRONT_CHAIN = [F_NE, F_BRK, A1, A2, A3, F_SW]

# Front block: the front chain, down the SW party wall, across the rear wall,
# back up the NE party wall. The LOGGIA notch is cut out of the front chain's
# north-east end (see LOGGIA_T below), so the body prism carries the recess and
# no boolean is needed.
LOT = FRONT_CHAIN + [SW_REAR, NE_REAR]

REAR_BLOCK = [RB_SW, RB_W, RB_WF, RB_NE, NE_REAR, SW_REAR]
COURTYARD = [FB_SW, FB_NE, RB_NE, RB_WF, RB_W, RB_SW]

AXIS_BEARING = 315.2         # front -> Taber Place, along both party walls

# ------------------------------------------------------------------- heights

Z_G = 3.30                   # top of the garage/entry level = tier-1 floor
Z_T1 = 8.20                  # tier-1 / tier-2 division (each tier 4.90 m = 16 ft)
Z_DECK = 12.30               # flat roof deck (LiDAR median 12.27 front, 11.88
                             # rear over ground 0.47 m higher — level, so modelled
                             # level)
Z_PARAPET = 13.10            # parapet crest — PHOTOGRAMMETRIC, see the header
Z_BULK = 14.67               # roof stair bulkhead crest — LiDAR maximum. The bbox
                             # top and the manifest targetHeightM, so the loader's
                             # scale is exactly 1.0.
Z_RISE = 0.45                # the site rises this much from South Park to Taber

# Openings, per tier: a lower row (square window + arched French door) and an
# upper row (the wide banded window with the oval).
ROW_LO = (0.25, 2.55)        # sill / head, relative to the tier floor
ROW_HI = (2.80, 4.35)        # the wide band
DOOR_LO = (0.05, 2.55)       # the arched French door runs to the balcony deck

# Station layout along the SOUTH-WEST front plane (t metres from the SW party
# wall corner), read metrically off the Street View panorama by mapping bearings
# through the surveyed front polyline. See REFERENCE.md section 3.
T_WIN = (0.60, 1.90)         # square window, both tiers
T_DOOR = (1.95, 3.05)        # round-arched wood French door + juliet balcony
T_BAND = (0.60, 5.50)        # the wide window band with the oval
T_RAIL = (1.20, 5.50)        # the balcony rail line
LOGGIA_T = (5.50, 7.90)      # the recessed loggia, both tiers
T_GAR = (2.60, 7.20)         # the garage door
T_ENTRY = (0.60, 2.00)       # the recessed pedestrian entry

LOGGIA_D = 1.20              # loggia recess depth
BAND_CASE = 0.30             # width of the pale surround around a window band
WIN_RECESS = 0.14
OVAL_T = (1.30, 4.20)        # the oval motif's extent inside the band
OVAL_BAR = 0.16              # mullion thickness

# North-east front plane (7.83 m, behind the sidewalk magnolia in every capture).
T_NE_BAND = ((0.85, 2.95), (4.30, 6.85))

# Taber Place elevation (14.29 m): paired windows over a solid base.
T_TB_WIN = (1.55, 4.10, 6.65, 9.20)
TB_WIN_W = 1.50
T_TB_DOOR = (0.35, 1.20)
T_TB_GAR = (11.10, 13.80)

PARAPET_INSET = 0.26
PARAPET_CAP = 0.10
BULK = ((-1.5, 4.2), (-2.6, 0.0))   # bulkhead, in the front block's roof frame

BEVEL_W, BEVEL_SEG = 0.11, 2

PALETTE_HEX = {
    "Toy_apricot": "dda87b",    # body stucco, both blocks, every elevation.
                                # OFF-PALETTE: the project palette has no warm
                                # mid-orange (rust a86444 is far too dark, brick
                                # c96f4a too red, mustard d9a441 too yellow) and
                                # this building's colour is its second-strongest
                                # recognition cue. Off-palette is a WARN, not a
                                # FAIL, and this block already carries
                                # Toy_verdigris, Toy_sash and Toy_plum.
    "Toy_sand": "ece4d4",       # window surrounds, parapet cap, the pale bands
    "Toy_glass": "2a4d73",      # all glazing
    "Toy_ink": "3a3530",        # mullions, THE OVAL MOTIF, all ironwork, the
                                # loggia soffits, the entry slot
    "Toy_rust": "a86444",       # the natural-stained wood French doors
    "Toy_stone": "d9d2c2",      # both roof decks and the courtyard paving.
                                # NOT Toy_roofd: it renders rgb(9,9,12) under the
                                # app's lighting and a roof deck in it reads black.
    "Toy_steel": "9aa0a6",      # the bulkhead, roof mechanical, the roof panel
    "Toy_mint": "8fd0a8",       # courtyard planting
    "Toy_plum": "6b4270",       # the courtyard's purple-bronze specimen tree
    "Toy_navy": "2c4a70",       # the pond
    "Toy_glassl_Glow": "6f95b8",
    "Toy_mustard_Glow": "d9a441",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


# ----------------------------------------------------------------- geometry


def _area_centroid(poly):
    a = cx = cy = 0.0
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        cr = x0 * y1 - x1 * y0
        a += cr
        cx += (x0 + x1) * cr
        cy += (y0 + y1) * cr
    a *= 0.5
    return cx / (6 * a), cy / (6 * a), abs(a)


LOT_CX, LOT_CY, LOT_AREA = _area_centroid(LOT)


class Face:
    """A local frame on one elevation: t along the face from `a` to `b`, d
    OUTWARD, z world up.

    Outward is resolved from the WINDING of the polygon the face belongs to, not
    from a centroid: on a five-sided lot with a re-entrant courtyard a centroid
    test folds the corner faces inward (see the offset-handedness note in
    REPORT.md)."""

    def __init__(self, a, b, ox, oy, flip=False):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        self.a = a
        self.b = b
        self.length = n
        self.t = (dx / n, dy / n)
        nrm = (-self.t[1], self.t[0])
        mx, my = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
        if (mx + nrm[0] - ox) ** 2 + (my + nrm[1] - oy) ** 2 < (mx - ox) ** 2 + (
            my - oy
        ) ** 2:
            nrm = (-nrm[0], -nrm[1])
        if flip:
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


# The four street-facing segments of the bowed south-west two-thirds, plus the
# straight north-east third, plus Taber Place. Outward is taken against the lot's
# own area centroid, which is correct for every one of these because they are all
# on the lot's convex hull.
SEG_NE = Face(F_NE, F_BRK, LOT_CX, LOT_CY)      # straight, faces 135.2 deg
ARC_SEGS = [
    Face(F_BRK, A1, LOT_CX, LOT_CY),
    Face(A1, A2, LOT_CX, LOT_CY),
    Face(A2, A3, LOT_CX, LOT_CY),
    Face(A3, F_SW, LOT_CX, LOT_CY),
]
REAR = Face(SW_REAR, NE_REAR, LOT_CX, LOT_CY)   # Taber Place, faces 315.2 deg


class Chain:
    """The bowed front read as ONE face frame: t runs from the south-west party
    wall corner along the arc to the break, so the metric station layout measured
    off the panorama can be applied without caring which facet a station lands
    on."""

    def __init__(self, pts):
        self.pts = pts
        self.cum = [0.0]
        for i in range(len(pts) - 1):
            self.cum.append(
                self.cum[-1]
                + math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
            )
        self.length = self.cum[-1]
        self.faces = [Face(pts[i], pts[i + 1], LOT_CX, LOT_CY) for i in range(len(pts) - 1)]

    def _seg(self, t):
        for i in range(len(self.faces)):
            if t <= self.cum[i + 1] + 1e-6:
                return i, t - self.cum[i]
        return len(self.faces) - 1, t - self.cum[-2]

    def xy(self, t, d):
        i, s = self._seg(max(0.0, min(t, self.length)))
        return self.faces[i].xy(s, d)

    def rect(self, t0, t1, d0, d1):
        return [self.xy(t0, d0), self.xy(t1, d0), self.xy(t1, d1), self.xy(t0, d1)]

    def poly(self, t0, t1, d):
        """The outward offset of the chain between t0 and t1 — used where a
        recess or a band has to follow the bow rather than chord it."""
        out = []
        i0, _ = self._seg(t0)
        i1, _ = self._seg(t1)
        out.append(self.xy(t0, d))
        for i in range(i0 + 1, i1 + 1):
            out.append(self.faces[i].xy(0.0, d))
        out.append(self.xy(t1, d))
        return out


def facing(a, b, want):
    """A Face whose outward normal is the KNOWN world heading of that wall, never
    a centroid guess. The front block's rear wall sits within a metre of the lot's
    area centroid, so a centroid test there is a coin toss — and on the two party
    walls it points out of the building, which put the first pass's roof furniture
    in mid-air over the neighbours."""
    f = Face(a, b, LOT_CX, LOT_CY)
    if abs(((f.heading - want + 180) % 360) - 180) > 90:
        f = Face(a, b, LOT_CX, LOT_CY, flip=True)
    return f


FRONT = Chain([F_SW, A3, A2, A1, F_BRK])        # 8.64 m, the bowed hero plane
FRONT_NE = Face(F_BRK, F_NE, LOT_CX, LOT_CY)    # 8.13 m, straight, 135.2 deg


# --------------------------------------------------------------- mesh helpers


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


def inset_polygon(poly, dist):
    """Offset every edge inward by `dist` and re-intersect adjacent edges.

    "Inward" comes from the polygon's WINDING, never from a centroid. The rear
    block's outline is L-shaped — the north-east wing puts a re-entrant corner in
    it — and a centroid test picks the wrong side for the edges around that
    corner, which self-intersects the inner ring. The signed volume of the
    resulting parapet still came out positive, so only the ray test caught it:
    every one of the 127 flipped visible faces in the first validation run was on
    `rear_parapet` or `rear_cap`. This is the offset-handedness trap in a second
    disguise; see REPORT.md section 5.
    """
    n = len(poly)
    area2 = sum(
        poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1]
        for i in range(n)
    )
    sgn = 1.0 if area2 > 0 else -1.0    # CCW: the interior is left of each edge
    lines = []
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy)
        d = (dx / m, dy / m)
        nrm = (-d[1] * sgn, d[0] * sgn)
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
        out.append((p0[0] + d0[0] * t, p0[1] + d0[1] * t))
    return out


def rim(name, poly, inset, z0, z1, mat):
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


def ring_prism(name, outer, inner, z0, z1, mat):
    """A closed band between two matching polygons — used for the oval motif and
    for window surrounds that have to follow the bow."""
    n = len(outer)
    verts = [(x, y, z0) for x, y in outer] + [(x, y, z0) for x, y in inner]
    verts += [(x, y, z1) for x, y in outer] + [(x, y, z1) for x, y in inner]
    O0, I0, O1, I1 = 0, n, 2 * n, 3 * n
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((O0 + i, O0 + j, O1 + j, O1 + i))
        faces.append((I0 + i, I0 + j, I1 + j, I1 + i))
        faces.append((O0 + i, O0 + j, I0 + j, I0 + i))
        faces.append((O1 + i, O1 + j, I1 + j, I1 + i))
    return new_mesh(name, verts, faces, [mat])


def box_on(face, name, t0, t1, d0, d1, z0, z1, mat, mat_top=None):
    return prism(name, face.rect(t0, t1, d0, d1), z0, z1, mat, mat_top)


# --------------------------------------------------------------------- build


def make_material(name):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = PALETTE[name] + (1.0,)
    bsdf.inputs["Roughness"].default_value = 0.85
    # Workbench's MATERIAL shading reads diffuse_color, not the BSDF, and the
    # review rig runs Workbench under machine contention. Keep them in step.
    mat.diffuse_color = PALETTE[name] + (1.0,)
    mat.roughness = 0.85
    if "Metallic" in bsdf.inputs:
        bsdf.inputs["Metallic"].default_value = 0.0
    if name.endswith("_Glow") and "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = PALETTE[name] + (1.0,)
        bsdf.inputs["Emission Strength"].default_value = 1.0
    return mat


def surround(name, face, t0, t1, z0, z1, mats, d_out=0.14, w=BAND_CASE, sill=True):
    """The broad pale flat band around a window band. This is what makes the
    bands read as bands from the app's camera — not the glazing."""
    zb = z0 - w if sill else z0
    bands = [
        ("l", (t0 - w, t0, zb, z1 + w)),
        ("r", (t1, t1 + w, zb, z1 + w)),
        ("t", (t0, t1, z1, z1 + w)),
    ]
    if sill:
        bands.append(("b", (t0, t1, z0 - w, z0)))
    for tag, r in bands:
        prism(
            f"{name}_{tag}",
            face.rect(r[0], r[1], -0.03, d_out),
            r[2],
            r[3],
            mats["Toy_sand"],
        )


def glazing(name, face, t0, t1, z0, z1, mats, bars=3, midrail=True):
    prism(name, face.rect(t0, t1, -WIN_RECESS, 0.02), z0, z1, mats["Toy_glass"])
    span = t1 - t0
    for i in range(1, bars + 1):
        t = t0 + span * i / (bars + 1)
        prism(
            f"{name}_bar{i}",
            face.rect(t - 0.05, t + 0.05, 0.05, 0.11),
            z0,
            z1,
            mats["Toy_ink"],
        )
    if not midrail:
        return
    zm = (z0 + z1) / 2.0
    prism(
        f"{name}_rail",
        face.rect(t0, t1, 0.05, 0.11),
        zm - 0.05,
        zm + 0.05,
        mats["Toy_ink"],
    )


def oval(name, face, t_c, z_c, rt, rz, mats, segs=16):
    """The building's one ornament: a long flattened ellipse in heavy mullion,
    drawn across the middle of a window band, with a small circle curled onto its
    south-west end. Modelled as a closed ring band so it has signed volume."""
    outer, inner = [], []
    for i in range(segs):
        a = 2.0 * math.pi * i / segs
        for lst, k in ((outer, 1.0), (inner, 0.0)):
            rr_t = rt + (OVAL_BAR / 2.0 if k else -OVAL_BAR / 2.0)
            rr_z = rz + (OVAL_BAR / 2.0 if k else -OVAL_BAR / 2.0)
            lst.append(face.xy(t_c + rr_t * math.cos(a), 0.04))
        # z handled below by using two ring_prisms is not possible for an
        # ellipse; build explicit verts instead.
    verts, faces = [], []
    for i in range(segs):
        a = 2.0 * math.pi * i / segs
        ct, sz = math.cos(a), math.sin(a)
        for kt, kz in ((rt + OVAL_BAR / 2.0, rz + OVAL_BAR / 2.0),
                       (rt - OVAL_BAR / 2.0, rz - OVAL_BAR / 2.0)):
            for d in (0.05, 0.13):
                verts.append(face.xy(t_c + kt * ct, d) + (z_c + kz * sz,))
    for i in range(segs):
        j = (i + 1) % segs
        o0, o1 = 4 * i, 4 * i + 1          # outer back, outer front
        i0, i1 = 4 * i + 2, 4 * i + 3      # inner back, inner front
        p0, p1 = 4 * j, 4 * j + 1
        q0, q1 = 4 * j + 2, 4 * j + 3
        faces.append((o0, o1, p1, p0))     # outer wall
        faces.append((i1, i0, q0, q1))     # inner wall
        faces.append((o1, i1, q1, p1))     # front
        faces.append((i0, o0, p0, q0))     # back
    obj = new_mesh(name, verts, faces, [mats["Toy_ink"]])
    # the curl: a small circle tangent to the ellipse's south-west end
    verts, faces = [], []
    r_o, r_i = 0.40, 0.40 - OVAL_BAR
    cx_t = t_c - rt * 0.86
    cz = z_c - rz * 0.30
    for i in range(8):
        a = 2.0 * math.pi * i / 8
        ct, sz = math.cos(a), math.sin(a)
        for rr in (r_o, r_i):
            for d in (0.05, 0.13):
                verts.append(face.xy(cx_t + rr * ct, d) + (cz + rr * sz,))
    for i in range(8):
        j = (i + 1) % 8
        o0, o1, i0, i1 = 4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3
        p0, p1, q0, q1 = 4 * j, 4 * j + 1, 4 * j + 2, 4 * j + 3
        faces.append((o0, o1, p1, p0))
        faces.append((i1, i0, q0, q1))
        faces.append((o1, i1, q1, p1))
        faces.append((i0, o0, p0, q0))
    new_mesh(f"{name}_curl", verts, faces, [mats["Toy_ink"]])
    return obj


def arched_door(name, face, t0, t1, z0, z1, mats, segs=5):
    """A round-arched wood French door: a flat leaf up to the springing, then a
    semicircular head built as a fan of quads."""
    w = t1 - t0
    z_spring = z1 - w / 2.0
    prism(name, face.rect(t0, t1, -0.10, 0.04), z0, z_spring, mats["Toy_rust"])
    tc = (t0 + t1) / 2.0
    r = w / 2.0
    poly = [face.xy(t0, 0.0)]
    for i in range(segs + 1):
        a = math.pi * i / segs
        poly.append(None)
    verts, faces = [], []
    for i in range(segs + 1):
        a = math.pi - math.pi * i / segs
        for d in (-0.10, 0.04):
            verts.append(face.xy(tc + r * math.cos(a), d) + (z_spring + r * math.sin(a),))
    base = len(verts)
    for d in (-0.10, 0.04):
        verts.append(face.xy(tc, d) + (z_spring,))
    c0, c1 = base, base + 1
    for i in range(segs):
        a0, b0 = 2 * i, 2 * i + 1
        a1, b1 = 2 * (i + 1), 2 * (i + 1) + 1
        faces.append((a0, b0, b1, a1))
        faces.append((a0, a1, c0))
        faces.append((b1, b0, c1))
    faces.append((0, 1, c1, c0))
    faces.append((2 * segs + 1, 2 * segs, c0, c1))
    new_mesh(f"{name}_head", verts, faces, [mats["Toy_rust"]])
    # the surround
    surround(f"{name}_case", face, t0, t1, z0, z1, mats, d_out=0.09, w=0.18)


def juliet(name, face, t0, t1, z, mats, depth=0.34, h=1.02):
    """Wrought-iron juliet balcony: a projecting grate slab, two posts and a top
    rail. The scrollwork goes; the silhouette is the cue."""
    prism(f"{name}_grate", face.rect(t0 - 0.20, t1 + 0.20, 0.0, depth), z - 0.10, z,
          mats["Toy_ink"])
    for tag, t in (("l", t0 - 0.18), ("r", t1 + 0.18)):
        prism(f"{name}_post_{tag}", face.rect(t - 0.05, t + 0.05, depth - 0.10, depth - 0.01),
              z, z + h, mats["Toy_ink"])
    prism(f"{name}_rail", face.rect(t0 - 0.22, t1 + 0.22, depth - 0.11, depth - 0.01),
          z + h - 0.09, z + h, mats["Toy_ink"])


def railing(name, face, t0, t1, z, mats, d=0.05, h=1.05):
    prism(f"{name}_rail", face.rect(t0, t1, d, d + 0.09), z + h - 0.09, z + h, mats["Toy_ink"])
    prism(f"{name}_kick", face.rect(t0, t1, d, d + 0.09), z + 0.04, z + 0.16, mats["Toy_ink"])
    n = max(2, int((t1 - t0) / 2.4))
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        prism(f"{name}_post{i}", face.rect(t - 0.035, t + 0.035, d + 0.01, d + 0.08),
              z + 0.04, z + h, mats["Toy_ink"])


def tier_front(tier, z0, mats):
    """One 4.90 m loft tier on the bowed south-west front: a lower row (square
    window + arched French door on a juliet balcony) under an upper row that is
    one 4.9 m banded window carrying the oval."""
    lo0, lo1 = z0 + ROW_LO[0], z0 + ROW_LO[1]
    hi0, hi1 = z0 + ROW_HI[0], z0 + ROW_HI[1]
    tag = f"t{tier}"
    # the wide band
    surround(f"{tag}_band", FRONT, T_BAND[0], T_BAND[1], hi0, hi1, mats)
    glazing(f"{tag}_bandglass", FRONT, T_BAND[0], T_BAND[1], hi0, hi1, mats, bars=3)
    oval(f"{tag}_oval", FRONT, (OVAL_T[0] + OVAL_T[1]) / 2.0, (hi0 + hi1) / 2.0,
         (OVAL_T[1] - OVAL_T[0]) / 2.0, (hi1 - hi0) * 0.31, mats)
    # lower row
    surround(f"{tag}_win", FRONT, T_WIN[0], T_WIN[1], lo0, lo1, mats, w=0.20)
    glazing(f"{tag}_winglass", FRONT, T_WIN[0], T_WIN[1], lo0, lo1, mats, bars=1,
             midrail=False)
    arched_door(f"{tag}_door", FRONT, T_DOOR[0], T_DOOR[1], z0 + DOOR_LO[0],
                z0 + DOOR_LO[1], mats)
    juliet(f"{tag}_juliet", FRONT, T_DOOR[0] - 0.15, T_DOOR[1] + 0.15, z0 + 0.05, mats)
    # night: a closed thin shell over the LOWER 55% of the band only
    prism(f"{tag}_glow", FRONT.rect(T_BAND[0] + 0.45, T_BAND[1] - 0.45, 0.02, 0.05),
          hi0 + 0.16, hi0 + 0.16 + (hi1 - hi0) * 0.45, mats["Toy_glassl_Glow"])
    # the straight north-east third: two narrower bands per tier
    for k, (a, b) in enumerate(T_NE_BAND):
        surround(f"{tag}_ne{k}", FRONT_NE, a, b, hi0, hi1, mats, w=0.24)
        glazing(f"{tag}_neg{k}", FRONT_NE, a, b, hi0, hi1, mats, bars=2, midrail=False)
        surround(f"{tag}_nel{k}", FRONT_NE, a, b, lo0, lo1, mats, w=0.24)
        glazing(f"{tag}_nelg{k}", FRONT_NE, a, b, lo0, lo1, mats, bars=2, midrail=False)
        prism(f"{tag}_neglow{k}", FRONT_NE.rect(a + 0.35, b - 0.35, 0.02, 0.05),
              hi0 + 0.16, hi0 + 0.16 + (hi1 - hi0) * 0.45, mats["Toy_glassl_Glow"])


def build():
    for scene in list(bpy.data.scenes)[1:]:
        bpy.data.scenes.remove(scene)
    scene = bpy.context.scene
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for item in list(block):
            block.remove(item)

    mats = {k: make_material(k) for k in PALETTE_HEX}

    # ---- front block --------------------------------------------------------
    # The loggia is cut out of the body prism rather than booleaned in: the front
    # chain re-enters at LOGGIA_T with the wall pushed back LOGGIA_D. The notch
    # spans the A1 vertex (t = 6.75 m on an 8.64 m chain), so it carries that
    # vertex's own inward offset as a third point or the bow folds through it.
    P0 = FRONT.xy(LOGGIA_T[0], 0.0)
    Q0 = FRONT.xy(LOGGIA_T[0], -LOGGIA_D)
    QM = FRONT.xy(FRONT.cum[3], -LOGGIA_D)          # the A1 vertex, offset in
    Q1 = FRONT.xy(LOGGIA_T[1], -LOGGIA_D)
    P1 = FRONT.xy(LOGGIA_T[1], 0.0)
    NOTCH = [P0, P1, Q1, QM, Q0]

    front_outline_full = [F_SW, A3, A2, A1, F_BRK, F_NE, FB_NE, FB_SW]
    front_outline_notch = [F_SW, A3, A2, P0, Q0, QM, Q1, P1, F_BRK, F_NE, FB_NE, FB_SW]

    prism("front_body", front_outline_notch, 0.0, Z_DECK, mats["Toy_apricot"],
          mats["Toy_stone"])
    # garage level fills the notch flush with the street wall
    prism("front_base_fill", NOTCH, 0.0, Z_G, mats["Toy_apricot"])
    # the slab between the two loggias, and the roof over the upper one
    prism("loggia_mid", NOTCH, Z_T1 - 0.30, Z_T1, mats["Toy_apricot"])
    prism("loggia_head", NOTCH, Z_DECK - 0.45, Z_DECK, mats["Toy_apricot"],
          mats["Toy_stone"])
    for tier, z in ((1, Z_G), (2, Z_T1)):
        railing(f"loggia{tier}", FRONT, LOGGIA_T[0] + 0.12, LOGGIA_T[1] - 0.12, z,
                mats, d=-0.10)
        prism(f"loggia{tier}_floor", NOTCH, z - 0.02, z + 0.10, mats["Toy_ink"])

    rim("front_parapet", front_outline_full, PARAPET_INSET, Z_DECK, Z_PARAPET - PARAPET_CAP,
        mats["Toy_apricot"])
    rim("front_cap", front_outline_full, PARAPET_INSET, Z_PARAPET - PARAPET_CAP, Z_PARAPET,
        mats["Toy_sand"])

    # ---- front block: street elevation --------------------------------------
    tier_front(1, Z_G, mats)
    tier_front(2, Z_T1, mats)

    # ground floor: the recessed pedestrian entry and the garage door
    prism("entry_slot", FRONT.rect(T_ENTRY[0], T_ENTRY[1], -0.85, -0.02), 0.0, 2.70,
          mats["Toy_ink"])
    surround("entry_case", FRONT, T_ENTRY[0], T_ENTRY[1], 0.0, 2.70, mats, d_out=0.08,
             w=0.20, sill=False)
    prism("entry_glow", FRONT.rect(T_ENTRY[0] + 0.30, T_ENTRY[1] - 0.30, -0.80, -0.74),
          0.55, 2.20, mats["Toy_mustard_Glow"])
    prism("garage", FRONT.rect(T_GAR[0], T_GAR[1], -0.14, 0.02), 0.0, 2.45,
          mats["Toy_apricot"])
    for k, z in enumerate((0.85, 1.55, 2.25)):
        prism(f"garage_reveal{k}", FRONT.rect(T_GAR[0] + 0.10, T_GAR[1] - 0.10, -0.20, -0.12),
              z, z + 0.10, mats["Toy_ink"])

    # ---- rear block ---------------------------------------------------------
    prism("rear_body", REAR_BLOCK, 0.0, Z_DECK, mats["Toy_apricot"], mats["Toy_stone"])
    rim("rear_parapet", REAR_BLOCK, PARAPET_INSET, Z_DECK, Z_PARAPET - PARAPET_CAP,
        mats["Toy_apricot"])
    rim("rear_cap", REAR_BLOCK, PARAPET_INSET, Z_PARAPET - PARAPET_CAP, Z_PARAPET,
        mats["Toy_sand"])

    # Taber Place elevation: paired windows over a solid base, a gated door at one
    # end and the second garage at the other.
    for tier, z0 in ((1, Z_G), (2, Z_T1)):
        hi0, hi1 = z0 + ROW_HI[0] - 0.55, z0 + ROW_HI[1] - 0.35
        for k, t in enumerate(T_TB_WIN):
            surround(f"tb{tier}_{k}", REAR, t, t + TB_WIN_W, hi0, hi1, mats, w=0.22)
            glazing(f"tb{tier}g_{k}", REAR, t, t + TB_WIN_W, hi0, hi1, mats, bars=1,
                    midrail=False)
            if k % 2 == 0:
                prism(f"tb{tier}glow_{k}",
                      REAR.rect(t + 0.28, t + TB_WIN_W - 0.28, 0.02, 0.05),
                      hi0 + 0.16, hi0 + 0.16 + (hi1 - hi0) * 0.45,
                      mats["Toy_glassl_Glow"])
    prism("tb_door", REAR.rect(T_TB_DOOR[0], T_TB_DOOR[1], -0.10, 0.03), Z_RISE, Z_RISE + 2.35,
          mats["Toy_ink"])
    surround("tb_door_case", REAR, T_TB_DOOR[0], T_TB_DOOR[1], Z_RISE, Z_RISE + 2.35, mats,
             d_out=0.08, w=0.18, sill=False)
    prism("tb_garage", REAR.rect(T_TB_GAR[0], T_TB_GAR[1], -0.13, 0.02), Z_RISE,
          Z_RISE + 2.45, mats["Toy_apricot"])
    for k, z in enumerate((0.85, 1.60)):
        prism(f"tb_garage_reveal{k}",
              REAR.rect(T_TB_GAR[0] + 0.10, T_TB_GAR[1] - 0.10, -0.19, -0.11),
              Z_RISE + z, Z_RISE + z + 0.10, mats["Toy_ink"])

    # ---- courtyard elevations ------------------------------------------------
    # The listings call these "a wall of windows with French doors to the shared
    # courtyard", so both court faces are one tall glazed slot per unit rather
    # than a grid of separate openings — cheaper, and closer to what is there.
    court_f = facing(FB_NE, FB_SW, 315.2)    # front block, rear wall
    court_r = facing(RB_SW, RB_W, 135.2)     # rear block, front wall
    for nm, f, stations, base in (
        ("cf", court_f, (1.60, 5.90, 10.20), 0.0),
        ("cr", court_r, (1.10, 4.60, 8.10), Z_RISE * 0.55),
    ):
        top = base + Z_T1 + ROW_LO[1]
        for k, t in enumerate(stations):
            w = 1.90 if k < len(stations) - 1 else 1.30
            prism(f"{nm}_slot{k}", f.rect(t, t + w, -0.12, 0.02), base + 0.15, top,
                  mats["Toy_glass"])
            prism(f"{nm}_jambL{k}", f.rect(t - 0.16, t, -0.03, 0.10), base + 0.15,
                  top + 0.16, mats["Toy_sand"])
            prism(f"{nm}_jambR{k}", f.rect(t + w, t + w + 0.16, -0.03, 0.10), base + 0.15,
                  top + 0.16, mats["Toy_sand"])
            prism(f"{nm}_head{k}", f.rect(t - 0.16, t + w + 0.16, -0.03, 0.10), top,
                  top + 0.16, mats["Toy_sand"])
            for lvl, z in ((1, base + Z_G), (2, base + Z_T1)):
                prism(f"{nm}_band{k}_{lvl}", f.rect(t, t + w, 0.01, 0.09), z - 0.22, z,
                      mats["Toy_sand"])
            prism(f"{nm}_glow{k}", f.rect(t + 0.30, t + w - 0.30, 0.02, 0.05),
                  base + Z_G + 0.35, base + Z_G + 1.90, mats["Toy_glassl_Glow"])

    # ---- roofs --------------------------------------------------------------
    # The stair bulkhead: the tallest thing in the model, at the front block's
    # courtyard edge. Placed in the front block's own frame so it lands square.
    bulk_face = facing(FB_SW, FB_NE, 135.2)
    prism("bulkhead", bulk_face.rect(6.10, 11.80, 0.55, 2.95), Z_DECK, Z_BULK,
          mats["Toy_steel"])
    for k, (t, w) in enumerate(((1.30, 1.10),)):
        prism(f"mech{k}", bulk_face.rect(t, t + w, 0.70, 1.70), Z_DECK, Z_DECK + 0.85,
              mats["Toy_steel"])
    ne_roof = Face(FB_NE, F_NE, LOT_CX, LOT_CY, flip=True)   # d runs SW, into the roof
    prism("roof_panel", ne_roof.rect(6.0, 8.6, 0.80, 2.60), Z_DECK, Z_DECK + 0.12,
          mats["Toy_ink"])
    for k, t in enumerate((11.4,)):
        prism(f"roof_mech{k}", ne_roof.rect(t, t + 1.3, 0.90, 2.10), Z_DECK, Z_DECK + 0.80,
              mats["Toy_steel"])
    rear_roof = facing(RB_SW, RB_W, 135.2)
    for k, t in enumerate((3.4,)):
        prism(f"rear_mech{k}", rear_roof.rect(t, t + 1.2, -4.6, -3.4), Z_DECK,
              Z_DECK + 0.70, mats["Toy_steel"])

    # ---- courtyard ----------------------------------------------------------
    prism("court_slab", COURTYARD, 0.0, Z_RISE * 0.55, mats["Toy_stone"])
    court_sw = Face(FB_SW, RB_SW, LOT_CX, LOT_CY)
    court_ne = Face(RB_NE, FB_NE, LOT_CX, LOT_CY)
    for nm, f, ln in (("bed_sw", court_sw, court_sw.length), ("bed_ne", court_ne, court_ne.length)):
        prism(nm, f.rect(0.9, ln - 0.9, -1.35, -0.15), Z_RISE * 0.55,
              Z_RISE * 0.55 + 0.55, mats["Toy_mint"])
    # the pond
    cx, cy, _ = _area_centroid(COURTYARD)
    ring = []
    for i in range(12):
        a = 2.0 * math.pi * i / 12
        ring.append((cx - 1.55 + 1.65 * math.cos(a) * 1.25, cy - 1.15 + 1.65 * math.sin(a)))
    prism("pond", ring, Z_RISE * 0.55 - 0.02, Z_RISE * 0.55 + 0.16, mats["Toy_navy"])
    # the specimen tree
    trunk = []
    tx, ty = cx + 1.6, cy + 1.2
    for i in range(8):
        a = 2.0 * math.pi * i / 8
        trunk.append((tx + 0.15 * math.cos(a), ty + 0.15 * math.sin(a)))
    prism("tree_trunk", trunk, Z_RISE * 0.55, Z_RISE * 0.55 + 2.10, mats["Toy_ink"])
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.55,
                                          location=(tx, ty, Z_RISE * 0.55 + 3.35))
    canopy = bpy.context.object
    canopy.name = "tree_canopy"
    canopy.scale = (1.0, 1.0, 0.78)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    canopy.data.materials.append(mats["Toy_plum"])
    canopy.data.shade_flat()

    # Two bevel segments only on the volumes that carry the silhouette; one on
    # everything else. At the app's camera the difference is invisible and it is
    # worth ~9,000 triangles.
    HERO = {"front_body", "rear_body", "front_parapet", "rear_parapet", "front_cap",
            "rear_cap", "bulkhead", "loggia_head", "loggia_mid", "front_base_fill",
            "court_slab", "garage", "tb_garage", "entry_slot"}
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name == "tree_canopy":
            continue
        if obj.name in HERO:
            bevel(obj, width=BEVEL_W, segments=BEVEL_SEG)
            continue
        if "oval" in obj.name or "curl" in obj.name:
            continue          # a bevel on a 0.19 m ring eats the ring
        thin = min((d for d in obj.dimensions if d > 1e-6), default=1.0)
        if thin < 0.16:
            continue          # applied hairline band — see the note above
        bevel(obj, width=0.05, segments=1)

    recentre()
    return scene


ANCHOR_SHIFT = [0.0, 0.0]


def recentre():
    mn = Vector((1e9, 1e9))
    mx = Vector((-1e9, -1e9))
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    for o in meshes:
        for v in o.data.vertices:
            w = o.matrix_world @ v.co
            for i in range(2):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    cx, cy = (mn[0] + mx[0]) / 2.0, (mn[1] + mx[1]) / 2.0
    ANCHOR_SHIFT[0], ANCHOR_SHIFT[1] = cx, cy
    for o in meshes:
        o.location.x -= cx
        o.location.y -= cy
    bpy.context.view_layer.update()
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    for o in meshes:
        o.select_set(False)


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
    print(f"[build] lot area: {LOT_AREA:.1f} m2 (surveyed parcel 585.0)")
    print(f"[build] bowed front {FRONT.length:.2f} m in {len(FRONT.faces)} facets; "
          f"straight NE third {FRONT_NE.length:.2f} m; Taber rear {REAR.length:.2f} m")
    print(f"[build] headings: bowed front {[round(f.heading, 1) for f in FRONT.faces]}, "
          f"NE third {FRONT_NE.heading:.1f}, Taber {REAR.heading:.1f}")
    print(f"[build] design anchor: {DESIGN_ANCHOR}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    low = []
    for o in objs:
        zs = [(o.matrix_world @ v.co).z for v in o.data.vertices]
        if min(zs) < -0.001:
            low.append((o.name, round(min(zs), 3)))
    print(f"[build] objects below z=0: {sorted(low, key=lambda t: t[1])[:8]}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "10-south-park.blend")
    glb = os.path.join(out, "10-south-park.glb")
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
