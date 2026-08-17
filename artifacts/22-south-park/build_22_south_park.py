"""Deterministic Blender build of the SF-SIM miniature Hotel Madrid
(22-24 South Park).

    blender -b --python build_22_south_park.py -- [--out DIR]

Writes 22-south-park.blend and 22-south-park.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, cornice crest exactly
14.22 m.

Design (see REFERENCE.md for the sources behind every number):

* a 1915 three-storey-over-basement Type V wood-frame residential hotel on the
  north rim of the South Park oval, built as the EIMOTO HOTEL for the Japanese
  community around the park, bought and rehabilitated by Mission Housing in 1987,
  and now the third building in the South Park Scattered Sites programme with the
  Park View (102) and the Gran Oriente Filipino (104-106) — both already in this
  repo's manifest;
* the lot is a TRAPEZOID, not a rectangle. The oval turns through this frontage,
  so the two party walls are parallel at 315.18 deg but 36.28 m (north-east) and
  only 30.13 m (south-west) long, the Taber Place rear is 13.68 m, and the South
  Park front is a 14.99 m chord carrying 15.15 m of concave arc (sagitta 0.93 m,
  radius 30.8 m, sweeping 28 deg). The arc is built as FOUR segments, which
  reproduces the sagitta to 6 cm and conveniently gives one segment per bay;
* recognition rests on the COLOUR PAIR and the CORNICE: sage-green lap siding
  with salmon-clay window casings, under a deep bracketed rust-clay cornice, over
  a dark slate-blue storefront divided by a rust belt course. Nothing else on this
  stretch of the rim wears any of it;
* the sage-green FIRE ESCAPE on the street face is the third cue and an unusual
  one — most SF fire escapes are black, this one is painted out in the body
  colour;
* the roof carries a large PV array from the 2019-21 rehabilitation and a light
  well on the north-east flank (permit-confirmed, and the reason the DataSF
  footprint is 372 m2 on a 444 m2 lot). The light well is modelled as a dark
  recessed pocket rather than a 3 m shaft: at the app's 30-50 deg camera a 1.8 m
  slot is fully self-occluding, so the shaft would be geometry nobody can see;
* height: the roof deck is the LiDAR median, 12.39 m (std 0.63 m over the
  footprint — a very flat roof). The 14.22 m maximum is taken as the
  parapet-frieze-cornice assembly and is the bbox top. Unlike its neighbours it
  CANNOT be party-wall bleed: both neighbours are shorter (10 South Park
  11.88-12.27 m, 26-28 South Park 8.35 m), so a contaminated cell could only pull
  the maximum down;
* night state: the taqueria storefront warm across the south-west half, five of
  the eight upper windows lit unevenly. Glow surfaces are thin CLOSED shells (an
  open face has no signed volume and fails the normals contract) covering only the
  lower part of each opening, because a closed shell is two alpha layers and reads
  ~23% by day rather than the app's nominal 12%.

Authoring frame: a LONG frame (s along the north-east party wall from the East
corner toward Taber Place, u across toward the south-west party wall) plus four
FRONT frames, one per arc segment, each with t along the segment and d outward.
Because the building sits at 45 deg to the world axes the axis-aligned XY
bounding box is ~35 x 35 m even though the building is 36.3 m by 13.7 m. That is
expected, not a scale error.
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

# Area centroid of the DataSF surveyed parcel 3775-048.
DESIGN_ANCHOR = (-122.3936498, 37.7822952)

# The parcel's own vertices, metres east/north from DESIGN_ANCHOR. The four arc
# points between the East and South corners are measured parcel vertices, not an
# interpolation.
E_CORNER = (18.78, -9.51)     # South Park x the 10 South Park party wall
ARC = [
    (18.78, -9.51),
    (15.16, -10.17),
    (11.63, -11.21),          # mid-face, 0.93 m behind the chord
    (8.22, -12.61),
    (4.75, -14.79),           # South corner: South Park x the 26-28 party wall
]
W_CORNER = (-16.49, 6.58)     # Taber Place x the 26-28 party wall
N_CORNER = (-6.79, 16.23)     # Taber Place x the 10 South Park party wall

FOOTPRINT = ARC + [W_CORNER, N_CORNER]

AXIS_BEARING = 315.18         # along the party walls, front -> Taber Place
REAR_BEARING = 315.18         # the Taber Place elevation faces this way

Z_DECK = 12.39                # flat roof deck — MEASURED (DataSF LiDAR median;
                              # mean 12.35, majority 12.52, std 0.63 m)
Z_FRIEZE = 13.30              # top of the parapet frieze
Z_CREST = 14.22               # cornice crown — MEASURED (LiDAR max). The bbox top
                              # and the manifest targetHeightM, so the loader's
                              # scale is exactly 1.0. See REPORT.md for why this
                              # maximum is believed where 26-28's was not.
Z_WELL = 11.50                # light-well pocket floor (a legible recess, not the
                              # real 9.31 m shaft — see the header)

Z_SHOP = 4.30                 # top of the storefront band = the belt course
Z_BELT_H = 0.35               # belt-course height
Z_F2, Z_F3 = 4.75, 8.75       # second- and third-storey window sills
WIN_H = 3.40                  # upper-storey opening height
WIN_W = 2.30                  # upper-storey opening width (a "pair" read as one)
CASE_W = 0.22                 # salmon-clay casing band width
WIN_RECESS = 0.16

SHOP_PROUD = 0.06
BELT_PROUD = 0.16
CORNICE_PROUD = 0.55
FRIEZE_PROUD = 0.12
BRACKET_W, BRACKET_D, BRACKET_DROP = 0.35, 0.42, 0.62
N_BRACKET_FRONT = 6
N_BRACKET_REAR = 3

FAN_R, FAN_D = 0.30, 0.14     # the round white exhaust fan on the sign band
AWN_W, AWN_D = 2.60, 1.00     # the curved barrel awning over the residential entry

FE_Z = (4.75, 8.75)           # fire-escape landings, second and third floors
FE_L, FE_D, FE_RAIL = 3.00, 1.20, 1.05

# LONG-frame extents (s from the East corner along the NE party wall,
# u across toward the SW party wall).
DEPTH_NE = 36.28              # the north-east party wall
DEPTH_SW = 30.13              # the south-west party wall
REAR_W = 13.68                # the Taber Place elevation

PARAPET_INSET = 0.26
ROOF_SLAB = 0.12

# Light well, in the LONG frame: a slot on the north-east flank at mid-depth. The
# DataSF ring traces it as ~16 m long and under 2 m wide, which is what puts the
# LiDAR minimum at 9.31 m on an otherwise 0.63 m-sd roof.
WELL_S0, WELL_S1 = 12.0, 26.0
WELL_U0, WELL_U1 = 0.55, 2.35

# PV array: two bands over the south-west two thirds, clear of the well.
PV_BANDS = ((6.2, 18.6), (19.8, 30.6))
PV_U0, PV_U1 = 4.40, 11.85
PV_RAIL, PV_PANEL = 0.18, 0.10

BEVEL_W, BEVEL_SEG = 0.12, 2

PALETTE_HEX = {
    "Toy_verdigris": "9fb8a8",  # body walls on both public elevations and both
                                # party walls, and the fire escape. The observed
                                # sage is a shade darker and greyer; this is the
                                # closest palette entry. Toy_teal (3fa8a0) is far
                                # too saturated and would make the building read
                                # as a novelty.
    "Toy_sand": "ece4d4",       # window casings, the Taber Place bay and door
    "Toy_rust": "a86444",       # the cornice, its brackets, the belt course, the
                                # barrel awning, the residential entry frame
    "Toy_navy": "2c4a70",       # the storefront band; the PV array
    "Toy_glass": "2a4d73",      # all windows and the storefront glazing
    "Toy_trim": "f3efe6",       # storefront window frames, the round exhaust fan
    "Toy_stone": "d9d2c2",      # the flat roof deck
    "Toy_steel": "9aa0a6",      # PV rails, mechanical plant
    "Toy_ink": "3a3530",        # the light-well floor and the storefront bulkhead
    "Toy_roofd": "45454a",      # the door onto the fire escape. The plan put this
                                # in Toy_ink; at the app's camera an ink door
                                # inside an ink-bulkheaded facade read as a hole
                                # punched in the wall rather than as a doorway.
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


def _brg(deg):
    r = math.radians(deg)
    return (math.sin(r), math.cos(r))


AXIS = _brg(AXIS_BEARING)          # East corner -> North corner
PERP = _brg(AXIS_BEARING - 90.0)   # north-east party wall -> south-west one
                                   # (origin is the EAST corner, so u runs SW)


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


CX, CY, FOOT_AREA = _area_centroid(FOOTPRINT)


def long_xy(s, u):
    """LONG frame: s metres from the East corner along the north-east party wall
    toward Taber Place, u metres across toward the south-west party wall."""
    return (
        E_CORNER[0] + AXIS[0] * s + PERP[0] * u,
        E_CORNER[1] + AXIS[1] * s + PERP[1] * u,
    )


def long_rect(s0, s1, u0, u1):
    return [long_xy(s0, u0), long_xy(s1, u0), long_xy(s1, u1), long_xy(s0, u1)]


class Face:
    """A local frame on one elevation: t along the face from `a` to `b`, d
    OUTWARD (away from the footprint centroid), z world up."""

    def __init__(self, a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        self.a = a
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


# Four street-facing segments, numbered 1..4 from the East (north-east) corner
# toward the South (south-west) corner. One per facade bay.
SEGS = [Face(ARC[i], ARC[i + 1]) for i in range(4)]
REAR = Face(W_CORNER, N_CORNER)          # Taber Place, faces 315.2 deg
FLANK_NE = Face(N_CORNER, E_CORNER)      # toward 10 South Park, faces 45.2 deg
FLANK_SW = Face(ARC[4], W_CORNER)        # toward 26-28, faces 225.2 deg


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
    """Offset every edge of a simple polygon inward by `dist` and re-intersect
    adjacent edges.

    "Inward" is resolved against the polygon's OWN area centroid, not the
    building's. Using the global centroid works for the parapet (whose polygon is
    the footprint) but silently shears any smaller polygon that sits off to one
    side — the light-well curb came out inverted and self-intersecting, and every
    flipped ray in the normals test landed on it."""
    ox, oy, _ = _area_centroid(poly)
    n = len(poly)
    lines = []
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy)
        d = (dx / m, dy / m)
        nrm = (-d[1], d[0])
        if (a[0] + nrm[0] - ox) ** 2 + (a[1] + nrm[1] - oy) ** 2 > (a[0] - ox) ** 2 + (
            a[1] - oy
        ) ** 2:
            nrm = (-nrm[0], -nrm[1])
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


def barrel(name, face, t_c, width, depth, z, mat, segs=7):
    """A quarter-cylinder awning: the curved barrel over the residential entry."""
    verts, faces = [], []
    for i in range(segs + 1):
        a = math.pi / 2.0 * i / segs
        d = depth * math.sin(a)
        h = depth * (1.0 - math.cos(a)) * 0.55
        for side, t in ((0, t_c - width / 2.0), (1, t_c + width / 2.0)):
            x, y = face.xy(t, d)
            verts.append((x, y, z - h))
    for i in range(segs):
        a0, b0 = 2 * i, 2 * i + 1
        a1, b1 = 2 * (i + 1), 2 * (i + 1) + 1
        faces.append((a0, b0, b1, a1))
    # close the ends and the underside so the shell is a solid
    verts.append(face.xy(t_c - width / 2.0, 0.0) + (z - depth * 0.55,))
    verts.append(face.xy(t_c + width / 2.0, 0.0) + (z - depth * 0.55,))
    lo0, lo1 = len(verts) - 2, len(verts) - 1
    faces.append((0, lo0, lo1, 1))
    faces.append((2 * segs, 2 * segs + 1, lo1, lo0))
    faces.append(tuple([2 * i for i in range(segs + 1)] + [lo0]))
    faces.append(tuple([lo1] + [2 * i + 1 for i in range(segs, -1, -1)]))
    return new_mesh(name, verts, faces, [mat])


def disc(name, face, t_c, z_c, r, depth, mat, segs=12):
    """A short cylinder standing proud of an elevation — the exhaust fan."""
    verts, faces = [], []
    for i in range(segs):
        a = 2 * math.pi * i / segs
        t = t_c + r * math.cos(a)
        z = z_c + r * math.sin(a)
        for d in (0.0, depth):
            verts.append(face.xy(t, d) + (z,))
    for i in range(segs):
        j = (i + 1) % segs
        faces.append((2 * i, 2 * j, 2 * j + 1, 2 * i + 1))
    faces.append(tuple(2 * i for i in range(segs - 1, -1, -1)))
    faces.append(tuple(2 * i + 1 for i in range(segs)))
    return new_mesh(name, verts, faces, [mat])


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


def upper_window(name, face, t_c, z_sill, mats, lit=False, door=False, wall_d=0.0):
    """One upper-storey opening: a recessed glazed panel inside a flat salmon-clay
    casing band. The casing is the recognition cue, not the sash — a real 1915
    paired double-hung is noise at the app's camera."""
    t0, t1 = t_c - WIN_W / 2.0, t_c + WIN_W / 2.0
    z1 = z_sill + WIN_H
    prism(
        f"{name}_fill",
        face.rect(t0, t1, -WIN_RECESS, wall_d + 0.02),
        z_sill,
        z1,
        mats["Toy_roofd"] if door else mats["Toy_glass"],
    )
    for tag, r in (
        ("l", (t0 - CASE_W, t0, z_sill - CASE_W, z1 + CASE_W)),
        ("r", (t1, t1 + CASE_W, z_sill - CASE_W, z1 + CASE_W)),
        ("b", (t0, t1, z_sill - CASE_W, z_sill)),
        ("t", (t0, t1, z1, z1 + CASE_W)),
    ):
        prism(
            f"{name}_case_{tag}",
            face.rect(r[0], r[1], wall_d - 0.03, wall_d + 0.10),
            r[2],
            r[3],
            mats["Toy_sand"],
        )
    if lit:
        # Closed thin shell over the LOWER 55% only: a closed _Glow shell is two
        # alpha layers by day (1 - 0.88^2 = 0.23, not 0.12), so a full-opening
        # shell in a saturated colour would tint the whole facade.
        prism(
            f"{name}_glow",
            face.rect(t0 + 0.14, t1 - 0.14, 0.03, 0.07),
            z_sill + 0.15,
            z_sill + 0.15 + (WIN_H - 0.30) * 0.55,
            mats["Toy_glassl_Glow"],
        )


def build():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for block in (bpy.data.meshes, bpy.data.materials):
        for item in list(block):
            block.remove(item)

    scene = bpy.context.scene
    mats = {k: make_material(k) for k in PALETTE}

    # -------------------------------------------------------------- massing
    prism("body", FOOTPRINT, 0.0, Z_DECK, mats["Toy_verdigris"])

    # ------------------------------------------------- the storefront band
    # A proud dark band on the four street segments only — the party walls have
    # no storefront and the Taber Place rear has its own treatment.
    for i, seg in enumerate(SEGS):
        prism(
            f"shop_band_{i}",
            seg.rect(0.0, seg.length, -0.04, SHOP_PROUD),
            0.0,
            Z_SHOP,
            mats["Toy_navy"],
        )
        prism(
            f"shop_bulkhead_{i}",
            seg.rect(0.0, seg.length, -0.05, SHOP_PROUD + 0.04),
            0.0,
            0.55,
            mats["Toy_ink"],
        )

    # Ground-floor openings. Segments 1-2 (north-east) are the residential half:
    # the lobby entrance under its barrel awning, and one glazed bay. Segments 3-4
    # (south-west) are the taqueria: a long run of glass and a recessed entry,
    # with the round exhaust fan at the south-west end of the sign band.
    def shop_opening(name, seg, t0, t1, z0, z1, frame):
        prism(
            f"{name}_fill",
            seg.rect(t0, t1, -0.14, SHOP_PROUD + 0.02),
            z0,
            z1,
            mats["Toy_glass"],
        )
        for tag, r in (
            ("l", (t0 - 0.14, t0, z0 - 0.14, z1 + 0.14)),
            ("r", (t1, t1 + 0.14, z0 - 0.14, z1 + 0.14)),
            ("b", (t0, t1, z0 - 0.14, z0)),
            ("t", (t0, t1, z1, z1 + 0.14)),
        ):
            prism(
                f"{name}_frame_{tag}",
                seg.rect(r[0], r[1], SHOP_PROUD - 0.03, SHOP_PROUD + 0.09),
                r[2],
                r[3],
                mats[frame],
            )

    s0 = SEGS[0]
    shop_opening("res_entry", s0, s0.length / 2 - 0.85, s0.length / 2 + 0.85,
                 0.55, 3.15, "Toy_rust")
    barrel("res_awning", s0, s0.length / 2, AWN_W, AWN_D, 3.62, mats["Toy_rust"])

    s1 = SEGS[1]
    shop_opening("res_bay", s1, 0.55, s1.length - 0.55, 0.90, 3.35, "Toy_trim")

    s2 = SEGS[2]
    shop_opening("taq_glass", s2, 0.40, s2.length - 0.40, 0.90, 3.35, "Toy_trim")

    s3 = SEGS[3]
    shop_opening("taq_entry", s3, 1.55, 2.95, 0.55, 3.15, "Toy_trim")
    disc("fan", s3, s3.length - 0.75, 3.72, FAN_R, SHOP_PROUD + FAN_D,
         mats["Toy_trim"])

    # ------------------------------------------------------- the belt course
    for i, seg in enumerate(SEGS):
        prism(
            f"belt_{i}",
            seg.rect(-0.02, seg.length + 0.02, -0.04, BELT_PROUD),
            Z_SHOP,
            Z_SHOP + Z_BELT_H,
            mats["Toy_rust"],
        )
    # short returns so the belt course does not stop dead at the party walls
    prism("belt_ret_ne", FLANK_NE.rect(FLANK_NE.length - 0.9, FLANK_NE.length,
                                       -0.04, BELT_PROUD),
          Z_SHOP, Z_SHOP + Z_BELT_H, mats["Toy_rust"])
    prism("belt_ret_sw", FLANK_SW.rect(0.0, 0.9, -0.04, BELT_PROUD),
          Z_SHOP, Z_SHOP + Z_BELT_H, mats["Toy_rust"])

    # -------------------------------------- upper storeys: four bays, two floors
    # Bay 1 (segment 1, north-east) carries the fire-escape DOOR on the second
    # floor and a window on the third — which is what the escape actually serves.
    for i, seg in enumerate(SEGS):
        t_c = seg.length / 2.0
        upper_window(f"f2_b{i}", seg, t_c, Z_F2, mats,
                     lit=(i in (1, 3)), door=(i == 0))
        upper_window(f"f3_b{i}", seg, t_c, Z_F3, mats, lit=(i in (0, 2, 3)))

    # ---------------------------------------------- Taber Place rear elevation
    # A finished elevation, not a service back: the same sage siding and clay
    # trim, a shallow canted bay at the upper floors, two ground-floor openings
    # and a service door.
    bay_t0, bay_t1 = REAR_W / 2 - 1.30, REAR_W / 2 + 1.30
    prism(
        "rear_bay",
        REAR.rect(bay_t0, bay_t1, -0.04, 0.50),
        Z_SHOP + Z_BELT_H,
        Z_F3 + WIN_H + CASE_W,
        mats["Toy_verdigris"],
    )
    for z in (Z_F2, Z_F3):
        prism(
            f"rear_bay_glass_{int(z)}",
            REAR.rect(bay_t0 + 0.30, bay_t1 - 0.30, 0.36, 0.54),
            z,
            z + WIN_H,
            mats["Toy_glass"],
        )
    upper_window("rear_f2_a", REAR, 2.05, Z_F2, mats, wall_d=0.0)
    upper_window("rear_f3_a", REAR, 2.05, Z_F3, mats, lit=True, wall_d=0.0)
    upper_window("rear_f2_b", REAR, REAR_W - 2.05, Z_F2, mats, wall_d=0.0)
    upper_window("rear_f3_b", REAR, REAR_W - 2.05, Z_F3, mats, wall_d=0.0)
    # ground floor: two tall grille-protected openings and a service door,
    # simplified to plain recesses in clay surrounds
    for k, t_c in enumerate((3.60, 6.30)):
        prism(
            f"rear_grille_{k}",
            REAR.rect(t_c - 0.75, t_c + 0.75, -0.14, 0.02),
            0.95,
            3.55,
            mats["Toy_ink"],
        )
        for tag, r in (
            ("l", (t_c - 0.75 - 0.18, t_c - 0.75, 0.80, 3.72)),
            ("r", (t_c + 0.75, t_c + 0.75 + 0.18, 0.80, 3.72)),
            ("t", (t_c - 0.75, t_c + 0.75, 3.55, 3.72)),
            ("b", (t_c - 0.75, t_c + 0.75, 0.80, 0.95)),
        ):
            prism(f"rear_grille_{k}_case_{tag}", REAR.rect(r[0], r[1], -0.03, 0.09),
                  r[2], r[3], mats["Toy_sand"])
    prism("rear_door", REAR.rect(8.15, 9.25, -0.10, 0.06), 0.0, 2.35,
          mats["Toy_sand"])
    prism("rear_service_gate", REAR.rect(10.30, 12.90, -0.08, 0.06), 0.0, 3.05,
          mats["Toy_sand"])
    # lap siding, read as three shallow grooves per storey on the rear only
    for i, z in enumerate((5.4, 6.6, 7.8, 9.4, 10.6, 11.8)):
        prism(f"rear_groove_{i}", REAR.rect(0.0, REAR_W, -0.06, 0.02), z, z + 0.07,
              mats["Toy_sand"])

    # ------------------------------------------------------------- the cornice
    # Frieze all round (it is the wall carried up), then the projecting crown and
    # its brackets on the two PUBLIC elevations only — a party wall has no
    # cornice. The crown is the crest and lands at exactly Z_CREST.
    rim("frieze", FOOTPRINT, PARAPET_INSET, Z_DECK - 0.03, Z_FRIEZE, mats["Toy_verdigris"])

    def cornice_on(face, tag, n_brackets, t0=0.0, t1=None):
        t1 = face.length if t1 is None else t1
        prism(f"cornice_frieze_{tag}", face.rect(t0, t1, -0.04, FRIEZE_PROUD),
              Z_DECK, Z_FRIEZE, mats["Toy_rust"])
        prism(f"cornice_crown_{tag}", face.rect(t0 - 0.05, t1 + 0.05, -0.04,
                                                CORNICE_PROUD),
              Z_FRIEZE, Z_CREST, mats["Toy_rust"])
        for k in range(n_brackets):
            tc = t0 + (t1 - t0) * (k + 0.5) / n_brackets
            prism(
                f"cornice_bracket_{tag}_{k}",
                face.rect(tc - BRACKET_W / 2, tc + BRACKET_W / 2, -0.03, BRACKET_D),
                Z_FRIEZE - BRACKET_DROP,
                Z_FRIEZE,
                mats["Toy_rust"],
            )

    for i, seg in enumerate(SEGS):
        cornice_on(seg, f"f{i}", 2 if i < 3 else 2)
    cornice_on(REAR, "rear", N_BRACKET_REAR)
    # 1.0 m returns so the cornice dies into the party walls rather than stopping
    cornice_on(FLANK_NE, "ret_ne", 1, t0=FLANK_NE.length - 1.0)
    cornice_on(FLANK_SW, "ret_sw", 1, t0=0.0, t1=1.0)

    # ---------------------------------------------------------------- the roof
    inner = inset_polygon(FOOTPRINT, PARAPET_INSET)
    prism("roof_slab", inner, Z_DECK - 0.03, Z_DECK + ROOF_SLAB, mats["Toy_stone"],
          mat_top=mats["Toy_stone"])
    Z_ROOF = Z_DECK + ROOF_SLAB

    # Light well: a legible recessed pocket with a raised curb, not the real 3 m
    # shaft — at the app's 30-50 deg camera a 1.8 m slot is fully self-occluding.
    prism("well_floor", long_rect(WELL_S0, WELL_S1, WELL_U0, WELL_U1),
          Z_ROOF - 0.03, Z_ROOF + 0.03, mats["Toy_ink"], mat_top=mats["Toy_ink"])
    rim("well_curb", long_rect(WELL_S0 - 0.22, WELL_S1 + 0.22,
                               WELL_U0 - 0.22, WELL_U1 + 0.22),
        0.22, Z_ROOF - 0.03, Z_ROOF + 0.26, mats["Toy_verdigris"])

    # PV array from the 2019-21 rehabilitation: two slabs on rails, never
    # individual modules — a real array here is 40-plus panels and would eat the
    # whole triangle budget for something that reads as one dark rectangle.
    for k, (a, b) in enumerate(PV_BANDS):
        prism(f"pv_rail_{k}", long_rect(a, b, PV_U0, PV_U1), Z_ROOF - 0.03,
              Z_ROOF + PV_RAIL, mats["Toy_steel"])
        prism(f"pv_panel_{k}", long_rect(a - 0.15, b + 0.15, PV_U0 - 0.15,
                                         PV_U1 + 0.15),
              Z_ROOF + PV_RAIL, Z_ROOF + PV_RAIL + PV_PANEL, mats["Toy_navy"],
              mat_top=mats["Toy_navy"])

    prism("roof_mech_a", long_rect(32.4, 34.2, 3.10, 5.30), Z_ROOF - 0.03, Z_ROOF + 0.55,
          mats["Toy_steel"])
    prism("roof_mech_b", long_rect(32.6, 33.9, 6.10, 7.40), Z_ROOF - 0.03, Z_ROOF + 0.38,
          mats["Toy_steel"])
    prism("roof_mech_c", long_rect(33.0, 34.0, 8.30, 9.20), Z_ROOF - 0.03, Z_ROOF + 0.32,
          mats["Toy_steel"])

    # ------------------------------------------------------- the fire escape
    # Painted out in the body colour, which is the unusual thing about it.
    for k, z in enumerate(FE_Z):
        seg = SEGS[0] if k == 0 else SEGS[0]
        tc = seg.length / 2.0
        prism(f"fe_deck_{k}", seg.rect(tc - FE_L / 2, tc + FE_L / 2, 0.0, FE_D),
              z - 0.20, z, mats["Toy_verdigris"])
        prism(f"fe_rail_{k}", seg.rect(tc - FE_L / 2, tc + FE_L / 2,
                                       FE_D - 0.10, FE_D),
              z, z + FE_RAIL, mats["Toy_verdigris"])
    # one diagonal stair slab between the two landings
    seg = SEGS[0]
    tc = seg.length / 2.0
    a = seg.xy(tc + FE_L / 2 - 0.15, 0.30)
    b = seg.xy(tc - FE_L / 2 + 0.15, 0.30)
    c = seg.xy(tc - FE_L / 2 + 0.15, 0.86)
    d = seg.xy(tc + FE_L / 2 - 0.15, 0.86)
    new_mesh(
        "fe_stair",
        [
            a + (FE_Z[0],), b + (FE_Z[1],), c + (FE_Z[1],), d + (FE_Z[0],),
            a + (FE_Z[0] - 0.16,), b + (FE_Z[1] - 0.16,), c + (FE_Z[1] - 0.16,),
            d + (FE_Z[0] - 0.16,),
        ],
        [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3),
         (3, 7, 4, 0)],
        [mats["Toy_verdigris"]],
    )

    # ---------------------------------------------------------- night state
    # Hero glow: the taqueria storefront across the south-west half. Warm, and the
    # one genuinely lit and busy thing on this stretch of the rim after dark.
    for tag, seg, t0, t1 in (("a", SEGS[2], 0.40, SEGS[2].length - 0.40),
                             ("b", SEGS[3], 1.55, 2.95)):
        prism(
            f"taq_glow_{tag}",
            seg.rect(t0 + 0.12, t1 - 0.12, SHOP_PROUD + 0.03, SHOP_PROUD + 0.07),
            1.05,
            1.80,
            mats["Toy_mustard_Glow"],
        )

    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        n = obj.name
        if n.endswith(("_fill", "_glow")) or "_case_" in n or "_frame_" in n \
                or "_groove_" in n:
            continue
        if n.startswith(("cornice_bracket", "fe_", "roof_mech", "pv_", "belt_",
                         "shop_bulkhead", "well_curb", "fan", "rear_groove")):
            bevel(obj, width=0.04, segments=1)
        else:
            bevel(obj)

    recentre()
    return scene


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
    print(f"[build] footprint area: {FOOT_AREA:.1f} m2 (surveyed parcel 444.5)")
    print(f"[build] party walls: NE {DEPTH_NE:.2f} m, SW {DEPTH_SW:.2f} m; rear {REAR_W:.2f} m")
    print(f"[build] front arc segments: {[round(s.length, 2) for s in SEGS]} "
          f"= {sum(s.length for s in SEGS):.2f} m")
    print(f"[build] design (parcel area-centroid) anchor: {DESIGN_ANCHOR}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] front segment headings: {[round(s.heading, 1) for s in SEGS]}")
    print(f"[build] rear {REAR.heading:.2f}; NE flank {FLANK_NE.heading:.2f}; "
          f"SW flank {FLANK_SW.heading:.2f}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "22-south-park.blend")
    glb = os.path.join(out, "22-south-park.glb")
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
