"""Deterministic Blender build of the SF-SIM miniature 8 Mission Street
(1 Hotel San Francisco, formerly Hotel Vitale).

    blender -b --python build_8_mission.py -- [--out DIR]

Writes 8-mission.blend and 8-mission.glb next to this file (or into --out).
Geometry is authored in world space in metres, Z up, +X east, +Y north, so the
model drops into the city at its real-world heading - the loader applies no
rotation. Origin = model XY bbox centre, min Z = 0, turret crown exactly
28.66 m.

Design (see REFERENCE.md for the sources behind every number):

* Heller Manus Architects, 2005. A 200-room hotel filling the whole block
  between Mission Street, Steuart Street, The Embarcadero and Don Chee Way,
  directly across the water side of the Embarcadero from the Ferry Building;
* the identity is STEPPED MASSING. Eight storeys on the Mission end
  (25.10 m), descending across two setbacks to six (19.64 m) and four
  (14.18 m) toward Harry Bridges Plaza. Prop K shadow limits on the plaza are
  why: the building is tallest where it faces the three-storey Audiffred and
  lowest where it faces the 42-storey One Market tower;
* two opposed corner events. A CONVEX circular turret (r 4.52 m) at the
  Mission x Embarcadero corner carrying seven round suites and a dark metal
  lantern crown - the crest and the night hero - and a CONCAVE notch
  (r 5.96 m) cut into the Mission x Steuart corner. Build one of them the
  wrong way round and the building is unrecognisable;
* three material bands: a rough pale limestone plinth, brown brick for most
  of the height, and a light plaster attic over the top two storeys of the
  Mission block, recessed behind the brick below it;
* the plan is an L. The north corner of the block is a Muni subway vent shaft
  on the same parcel, and it is NOT part of this asset - the integration
  exclusion radius (10 m) is sized specifically to leave it standing;
* the roof is the review view. Plateau A is the working roof - membrane,
  mechanical field, the turret, the spa pavilion in its bamboo. Plateaus B and
  C are planted terrace decks, stepping down and away to the north-west;
* night state: the turret's glazed bands are the hero (seven circular suites
  as a lantern on the waterfront), the entrance canopy carries a warm strip,
  and about a fifth of the guest-room windows are lit in an irregular
  scatter. Every glow surface is a single outward-facing layer standing proud
  of the opaque glazing, never a closed shell: the app draws _Glow in a
  separate layer that is translucent by day, and a closed shell is two alpha
  layers deep.

Authoring frame: everything is laid out in the building's own (u, v) frame -
u along the 64.08 m Steuart/Embarcadero axis toward bearing 135.3665 deg
(Mission Street), v along the 42.07 m axis toward bearing 225.3665 deg
(Steuart Street) - and mapped to world XY once. Because the block sits at
~45 deg to the world axes the axis-aligned XY bounding box is ~75 x 75 m even
though the building is 64.08 x 42.07 m. That is expected, not a scale error.
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

# OBB centre of OSM way 193054134, the plan's design anchor (before recentring).
DESIGN_ANCHOR = (-122.3932805, 37.7937365)

U_BEARING = 135.3665      # +u: outward normal of the Mission Street elevation
V_BEARING = 225.3665      # +v: outward normal of the Steuart Street elevation

# Footprint, in (u, v) metres from the OBB centre. Every number measured from
# the OSM ring (2.3 of the plan) except where noted.
U_SE = 32.00              # Mission Street wall
U_MID = 6.00              # plateau A / B setback          (estimated, 2.15.1)
U_WEST = -11.40           # plateau B / C setback = the notch's east return
U_NW = -32.00             # Don Chee Way end wall
V_SW = 21.00              # Steuart Street wall
V_NE = -20.75             # The Embarcadero wall
V_NOTCH = 3.30            # the notch's south return

TUR_U, TUR_V, TUR_R = 27.57, -16.52, 4.52     # turret circle, fitted to OSM
NOTCH_U, NOTCH_V, NOTCH_R = 32.29, 21.01, 5.96  # concave notch, fitted to OSM
TUR_SEGS = 24
NOTCH_SEGS = 8

# Storey grid. The two measured LiDAR roof planes (mode 25.10 m over 8 storeys,
# median 19.64 m over 6) fix the typical floor at 2.73 m and leave a 5.99 m
# ground floor, which matches the arcaded double-height lobby and restaurant in
# the photographs.
Z_GROUND = 5.99
Z_FLOOR = 2.73
Z_A = 25.10               # plateau A parapet - LiDAR mode, MEASURED
Z_B = 19.64               # plateau B parapet - LiDAR median, MEASURED
Z_C = Z_GROUND + 3 * Z_FLOOR   # 14.18 m, four storeys - DERIVED (2.15.2)
Z_CROWN = 28.66           # turret crown - LiDAR max, MEASURED. The bbox top.

Z_ATTIC = Z_B             # the plaster attic starts where plateau B stops
PLINTH_Z = 1.50
PLINTH_PROUD = 0.13
ATTIC_INSET = 0.30
PARAPET_H = 0.95
COPING_H = 0.22
COPING_OUT = 0.10

EMBED = 0.02

# Arcade / entrance
ARCH_W = 5.20
ARCH_SPRING = 3.60
ARCH_TOP = 5.30
ARCH_D = 0.42
CANOPY_W = 6.40
CANOPY_R = 2.55
CANOPY_PROJ = 2.20
CANOPY_Z = 5.35

# Punched windows
WIN_W = 1.55
WIN_H = 1.85
WIN_SILL = 0.70           # above each storey's floor line
WIN_RECESS = 0.22
# The plaster attic's two storeys are squeezed between the 19.64 m setback and
# the 24.15 m parapet base, so they get their own shorter, lower opening. Reusing
# the body window there pushed the top row through the parapet.
WIN_H_ATTIC = 1.30
WIN_SILL_ATTIC = 0.50

# Projecting glazed bays (The Embarcadero, and two on Steuart)
BAY_W = 3.30
BAY_PROJ = 0.55

PIER_W = 1.00
PIER_PROUD = 0.13

BEVEL_W = 0.10
BEVEL_SEG = 2

PALETTE_HEX = {
    "Toy_brick": "c96f4a",
    "Toy_sand": "ece4d4",
    "Toy_stone": "d9d2c2",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_slate": "39434f",
    "Toy_steel": "9aa0a6",
    "Toy_leaf": "6d8558",
    "Toy_sage": "8f9b86",
    "Toy_glassl_Glow": "6f95b8",
    "Toy_gold_Glow": "caa64a",
    "Toy_glass_Glow": "6f95b8",
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


UH = _brg(U_BEARING)
VH = _brg(V_BEARING)


def W(u, v):
    """(u, v) in the building's own frame -> world XY metres."""
    return (UH[0] * u + VH[0] * v, UH[1] * u + VH[1] * v)


def arc_uv(cu, cv, r, a0, a1, segs):
    """Points on a circle in the (u, v) frame, angles in degrees, inclusive."""
    out = []
    for i in range(segs + 1):
        a = math.radians(a0 + (a1 - a0) * i / segs)
        out.append((cu + r * math.cos(a), cv + r * math.sin(a)))
    return out


def _tangent_angles():
    """Where the turret circle crosses the two wall lines it stands in.

    The circle's centre is 4.43 m from the Mission wall and 4.23 m from The
    Embarcadero wall against a radius of 4.52, so it crosses BOTH and pokes a
    little way past each - 0.09 m and 0.29 m. Each wall therefore has two
    crossings, and the outline must leave through the FIRST one it reaches
    walking toward the corner, then run round the outside of the circle. Taking
    the far crossing instead buries ~1.8 m of wall inside the drum and leaves
    interior faces the normals gate will find."""
    du = U_SE - TUR_U
    dv = V_NE - TUR_V
    dv_se = math.sqrt(max(TUR_R ** 2 - du ** 2, 1e-6))
    du_ne = math.sqrt(max(TUR_R ** 2 - dv ** 2, 1e-6))
    a_se = math.degrees(math.atan2(dv_se, du))                # on u = U_SE
    a_ne = math.degrees(math.atan2(dv, -du_ne))               # on v = V_NE
    return a_se, a_ne, (TUR_V + dv_se), (TUR_U - du_ne)


A_SE, A_NE, V_TUR_SE, U_TUR_NE = _tangent_angles()


def turret_outline():
    """The turret arc, walking from the Mission wall round the east corner to
    The Embarcadero wall (i.e. from A_SE down through -90 deg to A_NE)."""
    a1 = A_NE if A_NE < A_SE else A_NE - 360.0
    return arc_uv(TUR_U, TUR_V, TUR_R, A_SE, a1, TUR_SEGS)


def _notch_tangents():
    """Where the concave notch circle crosses the two walls it is cut out of."""
    dv = V_SW - NOTCH_V
    du = U_SE - NOTCH_U
    u_sw = NOTCH_U - math.sqrt(max(NOTCH_R ** 2 - dv ** 2, 1e-6))
    v_se = NOTCH_V - math.sqrt(max(NOTCH_R ** 2 - du ** 2, 1e-6))
    return u_sw, v_se


U_NOTCH_SW, V_NOTCH_SE = _notch_tangents()


def notch_outline():
    """The concave Mission x Steuart corner, walking from the Steuart wall to
    the Mission wall. Bulges INTO the plan, which is the whole point."""
    a0 = math.degrees(math.atan2(V_SW - NOTCH_V, U_NOTCH_SW - NOTCH_U))
    a1 = math.degrees(math.atan2(V_NOTCH_SE - NOTCH_V, U_SE - NOTCH_U))
    if a1 < a0:
        a1 += 360.0
    return arc_uv(NOTCH_U, NOTCH_V, NOTCH_R, a0, a1, NOTCH_SEGS)


def dedupe(poly, tol=0.02):
    """Drop consecutive points closer together than `tol`, wrapping.

    Not cosmetic. An arc spliced in next to the wall point it starts from
    leaves a near-zero-length edge, whose direction is numerical noise; every
    offset ring built from that polygon then shoots a spike out of that corner.
    On the first build that put the plaster attic 0.29 m PROUD of the brick
    instead of 0.30 m recessed - the recess simply vanished - and dashed the
    parapet. Tolerance is 20 mm because the notch tangents and the wall corners
    agree only to a couple of centimetres."""
    out = []
    for p in poly:
        if out and math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) < tol:
            continue
        out.append(p)
    while len(out) > 2 and math.hypot(out[0][0] - out[-1][0],
                                      out[0][1] - out[-1][1]) < tol:
        out.pop()
    return out


def footprint_uv():
    """The whole L, in (u, v), clockwise in that frame."""
    poly = [(U_SE, V_NOTCH_SE)]
    poly += turret_outline()
    poly += [
        (U_WEST, V_NE),
        (U_WEST, V_NOTCH),
        (U_NW, V_NOTCH),
        (U_NW, V_SW),
        (U_NOTCH_SW, V_SW),
    ]
    poly += notch_outline()
    return dedupe(poly)


def plateau_a_uv():
    poly = [(U_SE, V_NOTCH_SE)]
    poly += turret_outline()
    poly += [(U_MID, V_NE), (U_MID, V_SW), (U_NOTCH_SW, V_SW)]
    poly += notch_outline()
    return dedupe(poly)


def plateau_b_uv():
    return [(U_MID, V_NE), (U_WEST, V_NE), (U_WEST, V_SW), (U_MID, V_SW)]


def plateau_c_uv():
    return [(U_WEST, V_NOTCH), (U_NW, V_NOTCH), (U_NW, V_SW), (U_WEST, V_SW)]


def to_world(poly_uv):
    return [W(u, v) for u, v in poly_uv]


FOOTPRINT = to_world(footprint_uv())
CX = sum(p[0] for p in FOOTPRINT) / len(FOOTPRINT)
CY = sum(p[1] for p in FOOTPRINT) / len(FOOTPRINT)


class Face:
    """A local frame on one elevation: t runs along the face from `a` to `b`,
    d runs OUTWARD, z is world up. `out` fixes the outward side explicitly -
    the footprint centroid is not a safe reference on an L-shaped plan whose
    notch returns face back across the plan."""

    def __init__(self, a_uv, b_uv, out_uv):
        a, b = W(*a_uv), W(*b_uv)
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        self.a, self.b, self.length = a, b, n
        self.t = (dx / n, dy / n)
        nrm = (-self.t[1], self.t[0])
        ref = W(*out_uv)
        mid = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
        if (mid[0] + nrm[0] - ref[0]) ** 2 + (mid[1] + nrm[1] - ref[1]) ** 2 > (
            mid[0] - ref[0]
        ) ** 2 + (mid[1] - ref[1]) ** 2:
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


# Elevations. `out_uv` is a point clearly on the outside of that wall.
MISSION = Face((U_SE, V_TUR_SE), (U_SE, V_NOTCH_SE), (U_SE + 20, 0))
STEUART_A = Face((U_NOTCH_SW, V_SW), (U_MID, V_SW), (0, V_SW + 20))
STEUART_B = Face((U_MID, V_SW), (U_WEST, V_SW), (0, V_SW + 20))
STEUART_C = Face((U_WEST, V_SW), (U_NW, V_SW), (0, V_SW + 20))
EMBARC_A = Face((U_TUR_NE, V_NE), (U_MID, V_NE), (0, V_NE - 20))
EMBARC_B = Face((U_MID, V_NE), (U_WEST, V_NE), (0, V_NE - 20))
DONCHEE = Face((U_NW, V_NOTCH), (U_NW, V_SW), (U_NW - 20, 0))
NOTCH_S = Face((U_NW, V_NOTCH), (U_WEST, V_NOTCH), (0, V_NOTCH - 20))
NOTCH_E = Face((U_WEST, V_NOTCH), (U_WEST, V_NE), (U_WEST - 20, 0))


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


def _winding(poly):
    s2 = 0.0
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        s2 += a[0] * b[1] - b[0] * a[1]
    return 1.0 if s2 > 0.0 else -1.0


def inset_polygon(poly, dist):
    """Offset every edge inward by `dist`, re-intersecting adjacent edges;
    negative offsets outward. Which side is inward comes from the polygon's own
    WINDING, never from a centroid test - on an L-shaped plan with a concave
    notch and a 122 deg turret arc, some segments' outward normals point back
    across the centroid and a centroid test folds the band."""
    n = len(poly)
    side = _winding(poly)
    lines = []
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy) or 1e-9
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
        # Spike guard: at a reflex vertex the two offset lines meet far away and
        # the intersection shoots off into a long sail.
        v = (q[0] - poly[i][0], q[1] - poly[i][1])
        m = math.hypot(v[0], v[1])
        cap = abs(dist) * 1.35
        if m > cap and m > 1e-9:
            q = (poly[i][0] + v[0] * cap / m, poly[i][1] + v[1] * cap / m)
        out.append(q)
    return out


def relax_polygon(poly, r):
    """Chamfer every reflex vertex of the polygon so an outward offset has
    somewhere to go. Required before any proud ring on this plan: the notch and
    both turret junctions are reflex seen from outside."""
    n = len(poly)
    sgn = _winding(poly)
    out = []
    for i in range(n):
        a, c, b = poly[i - 1], poly[i], poly[(i + 1) % n]
        ux, uy = c[0] - a[0], c[1] - a[1]
        vx, vy = b[0] - c[0], b[1] - c[1]
        lu, lv = math.hypot(ux, uy), math.hypot(vx, vy)
        if lu < 1e-9 or lv < 1e-9:
            continue
        cross = (ux * vy - uy * vx) * sgn
        if cross >= 0.0:                       # convex
            out.append(c)
            continue
        d = min(r, lu * 0.45, lv * 0.45)
        out.append((c[0] - ux / lu * d, c[1] - uy / lu * d))
        out.append((c[0] + vx / lv * d, c[1] + vy / lv * d))
    return out


def rim(name, poly, inset, z0, z1, mat):
    """Closed band solid between `poly` and its offset - a parapet, a coping or
    a proud string course."""
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


def profile_solid(name, face, pts_tz, d0, d1, mat):
    """Extrude a closed (t, z) profile drawn in a face's plane outward from d0
    to d1. Used for the arched ground-floor openings, whose shape lives in the
    elevation rather than in plan."""
    n = len(pts_tz)
    verts = [(*face.xy(t, d0), z) for t, z in pts_tz]
    verts += [(*face.xy(t, d1), z) for t, z in pts_tz]
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    return new_mesh(name, verts, faces, [mat])


def disc(name, cu, cv, z0, z1, r, segs, mat, mat_top=None):
    poly = [W(cu + r * math.cos(2 * math.pi * i / segs),
              cv + r * math.sin(2 * math.pi * i / segs)) for i in range(segs)]
    return prism(name, poly, z0, z1, mat, mat_top)


def _glow_quads(name, quads, mat):
    """Build an OPEN, single-layer glow strip from explicit (p0, p1, z0, z1,
    outward) records, winding every quad from the supplied outward vector.

    Night glow must never be a closed shell: the app draws _Glow in a separate
    layer that is translucent by day, and a closed box shows its front AND its
    back face, so it reads at roughly twice the intended day alpha - enough to
    tint a whole facade. One layer of one-sided quads is the correct
    construction, and the winding is SET, never recalculated (recalc on an open
    strip is undefined) and never inferred from the model centroid (the turret
    sweeps past it, and the concave notch faces the opposite way from every
    convex surface on the building)."""
    verts, faces = [], []
    for p, q, z0, z1, out in quads:
        dx, dy = q[0] - p[0], q[1] - p[1]
        if math.hypot(dx, dy) < 1e-6 or abs(z1 - z0) < 1e-6:
            continue
        # quad (p,z0) (q,z0) (q,z1) (p,z1) has normal (dy, -dx, 0)
        if dy * out[0] - dx * out[1] < 0.0:
            p, q = q, p
        k = len(verts)
        verts += [(p[0], p[1], z0), (q[0], q[1], z0),
                  (q[0], q[1], z1), (p[0], p[1], z1)]
        faces.append((k, k + 1, k + 2, k + 3))
    if not faces:
        return None
    return new_mesh(name, verts, faces, [mat], recalc=False)


def ring_glow(name, cu, cv, r, z0, z1, mat, a0_deg, a1_deg, segs=14):
    """A single-layer outward-facing glow band along an arc of a circle.

    The arc is explicit and NOT the whole circle. The turret is inscribed in
    the corner - it clears the Mission wall by 0.09 m and The Embarcadero wall
    by 0.29 m - so below the roofline only about 122 degrees of its drum is
    outside the building. A glow band round the full circumference buries two
    thirds of itself inside the walls, where it lights nothing and fails the
    validator's "is this face the first thing a ray along its own normal hits"
    test."""
    quads = []
    c = W(cu, cv)
    for i in range(segs):
        b0 = math.radians(a0_deg + (a1_deg - a0_deg) * i / segs)
        b1 = math.radians(a0_deg + (a1_deg - a0_deg) * (i + 1) / segs)
        bm = (b0 + b1) / 2.0
        p = W(cu + r * math.cos(b0), cv + r * math.sin(b0))
        q = W(cu + r * math.cos(b1), cv + r * math.sin(b1))
        m = W(cu + r * math.cos(bm), cv + r * math.sin(bm))
        quads.append((p, q, z0, z1, (m[0] - c[0], m[1] - c[1])))
    return _glow_quads(name, quads, mat)


def face_glow(name, face, t0, t1, z0, z1, d, mat):
    """One outward-facing quad in a wall plane, standing `d` proud."""
    return _glow_quads(name, [(face.xy(t0, d), face.xy(t1, d), z0, z1, face.n)],
                       mat)


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


# ----------------------------------------------------------- facade elements


def hash01(n):
    n = (n ^ 61) ^ (n >> 16)
    n = (n + (n << 3)) & 0xFFFFFFFF
    n = n ^ (n >> 4)
    n = (n * 0x27D4EB2D) & 0xFFFFFFFF
    n = n ^ (n >> 15)
    return (n & 0xFFFFFF) / 0xFFFFFF


LIT = []          # (face, t0, t1, z0, z1) collected for the night pass


def storey_z(k):
    """Floor line of storey k (k=1 is the ground floor)."""
    return 0.0 if k <= 1 else Z_GROUND + (k - 2) * Z_FLOOR


def window(name, face, t_c, k, mats, seed=0, lit_p=0.20, dshift=0.0,
           attic=False):
    """One recessed opening on storey k, with a proud stone sill. `dshift` moves
    the whole opening inward, which is how the plaster attic's windows sit on
    the recessed attic plane instead of floating 0.30 m proud of it."""
    h = WIN_H_ATTIC if attic else WIN_H
    z = storey_z(k) + (WIN_SILL_ATTIC if attic else WIN_SILL)
    t0, t1 = t_c - WIN_W / 2.0, t_c + WIN_W / 2.0
    prism(f"{name}_glass",
          face.rect(t0, t1, -WIN_RECESS - dshift, -0.06 - dshift), z, z + h,
          mats["Toy_glass"])
    prism(f"{name}_sill",
          face.rect(t0 - 0.12, t1 + 0.12, -EMBED - dshift, 0.09 - dshift),
          z - 0.14, z, mats["Toy_stone"])
    if hash01(seed) < lit_p:
        LIT.append((face, t0 + 0.14, t1 - 0.14, z + 0.16, z + h - 0.16,
                    -dshift))


def window_run(tag, face, top_z, storeys, mats, pitch, margin=1.35, pair=1.05,
               attic_from=None):
    """Paired punched windows on a regular bay grid, every storey from 2 up.
    Storeys at or above `attic_from` are drawn on the recessed attic plane."""
    span = face.length - 2 * margin
    n = max(1, int(round(span / pitch)))
    step = span / n
    seed = abs(hash(tag)) & 0xFFFF
    for b in range(n):
        t_c = margin + step * (b + 0.5)
        for k in range(2, storeys + 1):
            at = (attic_from is not None and storey_z(k) >= attic_from - 0.01)
            sill = WIN_SILL_ATTIC if at else WIN_SILL
            hgt = WIN_H_ATTIC if at else WIN_H
            head = storey_z(k) + sill + hgt
            # A window may not break the wall it is in: the body run stops at
            # the setback, the attic run stops at the parapet base.
            cap = (top_z - PARAPET_H - 0.08) if at else (
                attic_from - 0.10 if attic_from is not None
                else top_z - PARAPET_H - 0.35)
            if head > cap:
                continue
            for s, dt in ((0, -pair), (1, pair)):
                window(f"{tag}_w{b}_{k}_{s}", face, t_c + dt, k, mats,
                       seed=seed + b * 97 + k * 13 + s,
                       dshift=ATTIC_INSET if at else 0.0, attic=at)
    return n, step, margin


def piers(tag, face, top_z, mats, n, step, margin, z0=None, z1=None):
    """A brick pier on every bay boundary, from the arcade head to the parapet.

    On plateau A the run STOPS at the attic line: the plaster attic is a
    recessed volume, and a brick pier carried through it at the outer wall plane
    hides the recess and turns the whole elevation back into one brick block -
    which is precisely what the first build did."""
    z0 = Z_GROUND if z0 is None else z0
    z1 = top_z - PARAPET_H if z1 is None else z1
    for b in range(n + 1):
        t_c = margin + step * b
        prism(f"{tag}_pier{b}",
              face.rect(t_c - PIER_W / 2.0, t_c + PIER_W / 2.0, -EMBED, PIER_PROUD),
              z0, z1, mats["Toy_brick"])
    # a stone sill course marking the top of the brick, under the attic
    if z1 < top_z - PARAPET_H - 0.1:
        prism(f"{tag}_sillcourse",
              face.rect(-0.1, face.length + 0.1, -EMBED, PIER_PROUD + 0.10),
              z1, z1 + 0.34, mats["Toy_stone"])


def arch(name, face, t_c, mats, w=ARCH_W, depth=ARCH_D):
    """A round-arched recessed opening: rectangle up to the springing, then a
    segmental head, with a plain stone reveal round it. No keystone, no
    mouldings - all sub-pixel at city scale.

    Built as two NESTED solids, not as a quad strip between an outer and an
    inner path. The strip construction pinched to zero at the springing points
    and produced degenerate triangles and non-unit loop normals on nine of the
    eleven arches."""
    def profile(rad, lift):
        pts = [(t_c - rad, 0.35), (t_c + rad, 0.35), (t_c + rad, ARCH_SPRING)]
        for i in range(1, 8):
            a = math.pi * i / 8.0
            pts.append((t_c + rad * math.cos(a),
                        ARCH_SPRING + rad * math.sin(a) * 0.78 + lift))
        pts.append((t_c - rad, ARCH_SPRING))
        return pts

    profile_solid(f"{name}_reveal", face, profile(w / 2.0 + 0.26, 0.20),
                  -0.16, 0.02, mats["Toy_stone"])
    profile_solid(f"{name}_void", face, profile(w / 2.0, 0.0),
                  -depth, -0.14, mats["Toy_glass"])


def glass_bay(name, face, t_c, z0, z1, mats, seed=0):
    """A steel-framed glazed bay standing proud of the brick piers. This is what
    makes The Embarcadero elevation read as glass on brick where Mission reads
    as brick with holes."""
    h = BAY_W / 2.0
    prism(f"{name}_glass", face.rect(t_c - h, t_c + h, -EMBED, BAY_PROJ),
          z0, z1, mats["Toy_glass"])
    for s, dt in ((0, -1), (1, 1)):
        prism(f"{name}_mull{s}",
              face.rect(t_c + dt * h - 0.16, t_c + dt * h + 0.16,
                        -EMBED, BAY_PROJ + 0.07),
              z0, z1, mats["Toy_slate"])
    prism(f"{name}_head", face.rect(t_c - h - 0.2, t_c + h + 0.2, -EMBED,
                                    BAY_PROJ + 0.07),
          z1, z1 + 0.30, mats["Toy_slate"])
    prism(f"{name}_cill", face.rect(t_c - h - 0.2, t_c + h + 0.2, -EMBED,
                                    BAY_PROJ + 0.07),
          z0 - 0.30, z0, mats["Toy_slate"])
    k = int((z1 - z0) // Z_FLOOR)
    for i in range(k):
        zz = z0 + Z_FLOOR * i
        prism(f"{name}_tr{i}", face.rect(t_c - h, t_c + h, BAY_PROJ - 0.02,
                                         BAY_PROJ + 0.05),
              zz + Z_FLOOR - 0.30, zz + Z_FLOOR - 0.10, mats["Toy_slate"])
        if hash01(seed + i * 31) < 0.28:
            LIT.append((face, t_c - h + 0.2, t_c + h - 0.2,
                        zz + 0.35, zz + Z_FLOOR - 0.55, BAY_PROJ))


# --------------------------------------------------------------------- build


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    mats = {k: make_material(k) for k in PALETTE}

    pa = to_world(plateau_a_uv())
    pb = to_world(plateau_b_uv())
    pc = to_world(plateau_c_uv())

    # 1. The three plateaus. A stops at the attic line; the plaster attic is a
    #    separate, inset solid on top of it, which is both the recess the
    #    photographs show and the cheapest way to get it.
    prism("plateau_a", pa, 0.0, Z_ATTIC, mats["Toy_brick"])
    attic = inset_polygon(pa, ATTIC_INSET)
    prism("attic", attic, Z_ATTIC - EMBED, Z_A, mats["Toy_sand"], mats["Toy_sand"])
    prism("plateau_b", pb, 0.0, Z_B, mats["Toy_brick"], mats["Toy_sand"])
    prism("plateau_c", pc, 0.0, Z_C, mats["Toy_brick"], mats["Toy_sand"])

    # 2. Rough limestone plinth, standing proud on every elevation.
    for tag, poly in (("a", pa), ("b", pb), ("c", pc)):
        prism(f"plinth_{tag}",
              inset_polygon(relax_polygon(poly, PLINTH_PROUD + 0.10),
                            -PLINTH_PROUD),
              0.0, PLINTH_Z, mats["Toy_stone"])

    # 3. Parapets and copings, one ring per plateau. These three rings are what
    #    encode the massing when the asset is seen from directly above.
    for tag, poly, top in (("a", attic, Z_A), ("b", pb, Z_B), ("c", pc, Z_C)):
        # relax_polygon is applied ONLY to the ring that offsets outward (the
        # coping). An inward offset at a reflex vertex converges and needs no
        # chamfer, and chamfering the 8-segment notch arc for no reason turns it
        # into a zigzag.
        # 30 mm proud of the wall plane. Built flush, the ring's outer face is
        # exactly coplanar with the wall below it and the two z-fight, which
        # renders as a dashed brick band along the whole parapet.
        rim(f"parapet_{tag}",
            inset_polygon(relax_polygon(poly, 0.10), -0.03), 0.45,
            top - PARAPET_H, top - COPING_H, mats["Toy_brick"])
        rim(f"coping_{tag}",
            inset_polygon(relax_polygon(poly, COPING_OUT + 0.08), -COPING_OUT),
            0.42 + 2 * COPING_OUT, top - COPING_H, top, mats["Toy_stone"])

    # 4. Mission Street - the hero elevation. Five bays, an arcaded ground floor
    #    and the barrel-vaulted entry canopy over the middle one.
    n, step, margin = window_run("mis", MISSION, Z_A, 8, mats, pitch=6.15,
                                 attic_from=Z_ATTIC)
    piers("mis", MISSION, Z_A, mats, n, step, margin, z1=Z_ATTIC)
    ent_t = margin + step * (n / 2.0)
    for b in range(n):
        arch(f"mis_arch{b}", MISSION, margin + step * (b + 0.5), mats)
    canopy(MISSION, ent_t, mats)
    notch_lobby(mats)

    # 5. Steuart Street - the long elevation, and the one that shows all three
    #    plateaus from the street.
    for tag, face, top, st, pitch in (
        ("stA", STEUART_A, Z_A, 8, 6.20),
        ("stB", STEUART_B, Z_B, 6, 5.80),
        ("stC", STEUART_C, Z_C, 4, 5.15),
    ):
        n, step, margin = window_run(tag, face, top, st, mats, pitch=pitch,
                                     attic_from=Z_ATTIC if tag == "stA" else None)
        piers(tag, face, top, mats, n, step, margin,
              z1=Z_ATTIC if tag == "stA" else None)
        for b in range(n):
            arch(f"{tag}_arch{b}", face, margin + step * (b + 0.5), mats,
                 w=ARCH_W - 0.6)
    # Two projecting bays on the Steuart wall, as in the photographs.
    glass_bay("st_bay0", STEUART_A, STEUART_A.length * 0.34, Z_GROUND,
              Z_A - PARAPET_H - 0.5, mats, seed=11)
    glass_bay("st_bay1", STEUART_B, STEUART_B.length * 0.55, Z_GROUND,
              Z_B - PARAPET_H - 0.5, mats, seed=23)

    # 6. The Embarcadero - glass on brick. Tall glazed bays between the piers,
    #    a plain glazed restaurant frontage at grade.
    for tag, face, top, st, nb in (("emA", EMBARC_A, Z_A, 8, 3),
                                   ("emB", EMBARC_B, Z_B, 6, 3)):
        margin = 1.5
        span = face.length - 2 * margin
        step = span / nb
        piers(tag, face, top, mats, nb, step, margin,
              z1=Z_ATTIC if tag == "emA" else None)
        for b in range(nb):
            glass_bay(f"{tag}_bay{b}", face, margin + step * (b + 0.5),
                      Z_GROUND, (Z_ATTIC if tag == "emA" else top - PARAPET_H - 0.5),
                      mats, seed=b * 71 + len(tag))
        if tag == "emA":
            for b in range(nb):
                for k in (7, 8):
                    window(f"{tag}_att{b}_{k}", face, margin + step * (b + 0.5),
                           k, mats, seed=900 + b * 7 + k, dshift=ATTIC_INSET,
                           attic=True)
        prism(f"{tag}_shopfront",
              face.rect(margin - 0.4, face.length - margin + 0.4, -0.22, 0.01),
              PLINTH_Z, Z_GROUND - 0.55, mats["Toy_glass"])

    # 7. Don Chee Way and the two notch returns. King's "drab brown slab": one
    #    sparse column of openings on the plaza end, a plain grid on the returns
    #    that face the vent shaft. Deliberately blank - do not populate it.
    # Two sparse columns and a service door. King calls this wall "as drab as
    # can be" and its blankness is a documented feature, so it stays the
    # plainest elevation on the building - but a 17.7 x 14.2 m dead surface is
    # not what the style bible means by that, and this face is the one the
    # Ferry Building crowd actually walks past.
    for c in (0.32, 0.68):
        for k in (2, 3, 4):
            window(f"dc_w{c:.2f}_{k}", DONCHEE, DONCHEE.length * c, k, mats,
                   seed=int(500 + c * 100) + k, lit_p=0.30)
    prism("dc_door",
          DONCHEE.rect(DONCHEE.length * 0.5 - 1.1, DONCHEE.length * 0.5 + 1.1,
                       -0.18, 0.01),
          PLINTH_Z - 0.3, PLINTH_Z + 2.5, mats["Toy_slate"])
    prism("dc_doorhead",
          DONCHEE.rect(DONCHEE.length * 0.5 - 1.35, DONCHEE.length * 0.5 + 1.35,
                       -EMBED, 0.24),
          PLINTH_Z + 2.5, PLINTH_Z + 2.8, mats["Toy_stone"])
    n, step, margin = window_run("nsS", NOTCH_S, Z_C, 4, mats, pitch=6.6)
    piers("nsS", NOTCH_S, Z_C, mats, n, step, margin)
    n, step, margin = window_run("nsE", NOTCH_E, Z_B, 6, mats, pitch=6.4)
    piers("nsE", NOTCH_E, Z_B, mats, n, step, margin)

    # 8. The turret. Brick to the fourth floor, glazed above with brick ribs,
    #    then the dark metal lantern crown. This block sets the bounding-box top
    #    and must land exactly on 28.66 m.
    turret(mats)

    # 9. The roofs (2.9 of the plan). Plateau A is the working roof; B and C are
    #    the planted terrace decks that make the cascade read from the aerial.
    roof_a(pa, mats)
    terrace(pb, Z_B, "b", mats)
    terrace(pc, Z_C, "c", mats)

    # 10. Night pass: one outward-facing quad per lit opening, proud of the
    #     glazing behind it. Collected during the facade passes so the scatter
    #     follows the real openings rather than a separate invented grid.
    for i, (face, t0, t1, z0, z1, d) in enumerate(LIT):
        face_glow(f"lit{i}_glow", face, t0, t1, z0, z1, d + 0.06,
                  mats["Toy_glass_Glow"])

    # Bevel budget: the plateau masses, the attic, the turret and the plinth
    # carry the miniature read and get the full 0.10/2. Everything thin,
    # numerous or already faceted stays sharp - it looks identical from the
    # app's camera and costs thousands of triangles.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        nm = obj.name
        if nm.startswith(("plateau_", "attic", "plinth_", "turret_body",
                          "turret_crown", "spa", "canopy_vault")):
            bevel(obj)
        elif nm.startswith(("parapet_", "coping_", "roof_plant", "terr_bed")):
            bevel(obj, width=0.05, segments=1)

    recentre()
    return scene


def canopy(face, t_c, mats):
    """The metal-and-glass canopy over the Mission porte-cochere.

    The curve is in the WALL plane - a segmental arch about 6.4 m wide rising
    ~1.6 m - and the shell projects forward from it. The first build swept a
    half-cylinder whose axis ran out from the wall and clamped the back half to
    d = 0, which collapsed into a dark wedge with no arch in it at all."""
    segs = 10
    rise = 1.55
    half = CANOPY_W / 2.0
    outer, inner = [], []
    for i in range(segs + 1):
        f = -1.0 + 2.0 * i / segs
        t = t_c + half * f
        z = CANOPY_Z + rise * math.cos(f * math.pi / 2.0)
        outer.append((t, z))
        inner.append((t, z - 0.34))
    prof = outer + list(reversed(inner))
    profile_solid("canopy_vault", face, prof, 0.0, CANOPY_PROJ, mats["Toy_slate"])
    # glazed infill under the shell, as one thin panel per bay of the arch
    for i in range(segs):
        t0, z0 = outer[i]
        t1, z1 = outer[i + 1]
        prism(f"canopy_glass{i}",
              face.rect(t0, t1, 0.12, CANOPY_PROJ - 0.12),
              min(z0, z1) - 0.30, min(z0, z1) - 0.16, mats["Toy_glassl"])
    # brackets back to the wall
    for dt in (-half + 0.35, half - 0.35):
        prism("canopy_stay%+0.2f" % dt,
              face.rect(t_c + dt - 0.14, t_c + dt + 0.14, 0.0, CANOPY_PROJ),
              CANOPY_Z - 0.45, CANOPY_Z - 0.22, mats["Toy_slate"])
    # the warm strip under the canopy - the second night cue
    face_glow("canopy_glow", face, t_c - half + 0.3, t_c + half - 0.3,
              CANOPY_Z - 0.42, CANOPY_Z - 0.08, CANOPY_PROJ - 0.10,
              mats["Toy_gold_Glow"])


def notch_lobby(mats):
    """The concave Mission x Steuart corner is not blank brick: John King's
    review puts "opaque glass that allows light into the lobby" on exactly this
    curve. Two glazed bands recessed into the arc, plus a night glow - the
    curve is the second-most photographed thing about this building and an
    11 m blind wall on it is a hole in the elevation."""
    for tag, z0, z1, rin, rout in (("base", PLINTH_Z, ARCH_TOP + 0.4, 0.30, 0.04),
                                   ("lobby", ARCH_TOP + 1.1, Z_ATTIC - 1.2,
                                    0.26, 0.04)):
        a0 = math.degrees(math.atan2(V_SW - NOTCH_V, U_NOTCH_SW - NOTCH_U))
        a1 = math.degrees(math.atan2(V_NOTCH_SE - NOTCH_V, U_SE - NOTCH_U))
        if a1 < a0:
            a1 += 360.0
        pad = (a1 - a0) * 0.06
        outer = arc_uv(NOTCH_U, NOTCH_V, NOTCH_R + rout, a0 + pad, a1 - pad, 8)
        innr = arc_uv(NOTCH_U, NOTCH_V, NOTCH_R + rin, a0 + pad, a1 - pad, 8)
        prism(f"notch_{tag}", [W(*p) for p in outer + list(reversed(innr))],
              z0, z1, mats["Toy_glass"])
    # mullions on the curve, so it reads as glazing rather than a void
    a0 = math.degrees(math.atan2(V_SW - NOTCH_V, U_NOTCH_SW - NOTCH_U))
    a1 = math.degrees(math.atan2(V_NOTCH_SE - NOTCH_V, U_SE - NOTCH_U))
    if a1 < a0:
        a1 += 360.0
    for i in range(1, 5):
        a = a0 + (a1 - a0) * i / 5.0
        cu = NOTCH_U + (NOTCH_R + 0.10) * math.cos(math.radians(a))
        cv = NOTCH_V + (NOTCH_R + 0.10) * math.sin(math.radians(a))
        disc(f"notch_mull{i}", cu, cv, PLINTH_Z, Z_ATTIC - 1.2, 0.22, 6,
             mats["Toy_stone"])
    # Night: a single-layer strip proud of the glass on the curve. This surface
    # is CONCAVE, so "outward" points TOWARD the notch circle's centre - the
    # opposite of every other glow surface on the building.
    quads = []
    pts = arc_uv(NOTCH_U, NOTCH_V, NOTCH_R - 0.04, a0 + (a1 - a0) * 0.06,
                 a1 - (a1 - a0) * 0.06, 8)
    c = W(NOTCH_U, NOTCH_V)
    for i in range(len(pts) - 1):
        p, q = W(*pts[i]), W(*pts[i + 1])
        mid = ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)
        quads.append((p, q, PLINTH_Z + 0.3, ARCH_TOP - 0.4,
                      (c[0] - mid[0], c[1] - mid[1])))
    _glow_quads("notch_glow", quads, mats["Toy_glassl_Glow"])


def turret(mats):
    """Circular turret at the Mission x Embarcadero corner: seven round suites
    and a lantern crown. r 4.52 m, fitted to the OSM arc; it projects only about
    0.3 m past each wall plane, exactly as built - the exaggeration allowance is
    spent on the CROWN, which flares to r 5.90 m, not on the drum."""
    disc("turret_body", TUR_U, TUR_V, 0.0, Z_C, TUR_R, TUR_SEGS, mats["Toy_brick"])
    disc("turret_glass", TUR_U, TUR_V, Z_C - EMBED, Z_A + 0.55, TUR_R - 0.06,
         TUR_SEGS, mats["Toy_glass"])
    # brick ribs between the glazed bands, one per suite
    for i in range(8):
        a = 2 * math.pi * (i + 0.5) / 8
        cu = TUR_U + (TUR_R - 0.25) * math.cos(a)
        cv = TUR_V + (TUR_R - 0.25) * math.sin(a)
        disc(f"turret_rib{i}", cu, cv, Z_C - EMBED, Z_A + 0.55, 0.40, 6,
             mats["Toy_brick"])
    # cornice / crown transition
    disc("turret_band", TUR_U, TUR_V, Z_A + 0.55, Z_A + 1.05, TUR_R + 0.16, TUR_SEGS,
         mats["Toy_stone"])
    disc("turret_crown", TUR_U, TUR_V, Z_A + 1.05, 27.55, TUR_R + 0.22, TUR_SEGS,
         mats["Toy_slate"], mats["Toy_slate"])
    # The radiating fin canopies. Restrained on purpose: the first build spun
    # them out to r 5.9 with a small centre cap and the crown read from the
    # aerial as a black propeller rather than a lantern. The brim now overhangs
    # the 4.52 m drum by about a metre and the centre drum is the tall part.
    for i in range(8):
        a = 2 * math.pi * i / 8
        c, s = math.cos(a), math.sin(a)
        r0, r1, hw = 2.30, 5.45, 0.78
        quad = [(TUR_U + r0 * c - hw * s, TUR_V + r0 * s + hw * c),
                (TUR_U + r1 * c - hw * 0.45 * s, TUR_V + r1 * s + hw * 0.45 * c),
                (TUR_U + r1 * c + hw * 0.45 * s, TUR_V + r1 * s - hw * 0.45 * c),
                (TUR_U + r0 * c + hw * s, TUR_V + r0 * s - hw * c)]
        prism(f"turret_fin{i}", [W(*p) for p in quad], 27.10, 27.52,
              mats["Toy_slate"])
    # the lantern itself: the centre drum carries the crest, so the fins read as
    # a brim around it rather than as the silhouette
    disc("turret_cap", TUR_U, TUR_V, 27.55 - 0.6, Z_CROWN, 2.55, 12,
         mats["Toy_slate"], mats["Toy_slate"])
    # night hero: two open glazing bands, single-layer, proud of the glass
    # The two shaft bands sit 0.05 m proud, INSIDE the eight brick ribs (r 4.67),
    # so the ribs break the lantern into lit bays at night - seven circular
    # suites, not a floodlit drum. The crown band above the parapet has to clear
    # them instead (0.26 m), because up there the ribs are the outermost thing
    # and a band tucked inside them is blocked by its own building.
    exp0, exp1 = A_SE - 3.0, (A_NE if A_NE < A_SE else A_NE - 360.0) + 3.0
    ring_glow("turret_glow_lo", TUR_U, TUR_V, TUR_R + 0.05,
              Z_C + 0.55, Z_C + 2.05, mats["Toy_glassl_Glow"], exp0, exp1)
    ring_glow("turret_glow_hi", TUR_U, TUR_V, TUR_R + 0.05,
              Z_C + 3.30, Z_A - 0.55, mats["Toy_glassl_Glow"], exp0, exp1)
    # Above the parapet the drum is free on the two street sides, so the
    # lantern can wrap 260 degrees - but not the full circle: its landward
    # quadrant looks straight into the roof screen and the vent stacks, and a
    # glow face buried behind roof furniture lights nothing.
    ring_glow("turret_glow_top", TUR_U, TUR_V, TUR_R + 0.26,
              Z_A + 0.10, Z_A + 0.50, mats["Toy_glassl_Glow"], 195.0, 455.0,
              segs=18)


def roof_a(pa, mats):
    """Plateau A: pale membrane, the mechanical field grouped at the Mission
    end, and the rooftop spa pavilion with its bamboo on the Embarcadero corner
    - Conde Nast puts the spa on "a rooftop corner ... overlooking the Ferry
    Building", which is this one, not the Steuart one. Nothing here may
    approach the turret crown: there is only 3.56 m of headroom between plateau
    A and the 28.66 m bounding-box top, and anything that out-tops the crown
    steals the loader's height normalization."""
    def r(u0, u1, v0, v1):
        return [W(u0, v0), W(u1, v0), W(u1, v1), W(u0, v1)]

    # The membrane follows the PLATEAU polygon, never a bounding rectangle: a
    # rectangle over the Mission end pokes straight out through the concave
    # notch, which is invisible in every elevation and obvious from above.
    prism("roof_membrane", inset_polygon(pa, 1.25),
          Z_A - 0.05, Z_A + 0.02, mats["Toy_sand"])
    # mechanical field (satellite imagery: chillers and fan units toward the
    # Mission end, clear of the terraces and the spa)
    for i, (u0, u1, v0, v1, h) in enumerate((
        (16.4, 21.8, -12.2, -7.0, 2.05),
        (16.4, 20.6, -6.0, -1.8, 1.65),
        (23.0, 26.8, -11.8, -8.4, 1.45),
        (23.0, 25.6, -7.2, -3.4, 1.90),
        (17.2, 20.6, 1.0, 5.4, 1.30),
    )):
        prism(f"roof_plant{i}", r(u0, u1, v0, v1), Z_A - EMBED, Z_A + h,
              mats["Toy_steel"], mats["Toy_slate"])
    for i, (u, v) in enumerate(((14.0, -3.2), (22.4, 1.4), (26.4, 1.6),
                                (13.4, 2.6), (27.0, -4.0))):
        disc(f"roof_vent{i}", u, v, Z_A - EMBED, Z_A + 0.85, 0.34, 8,
             mats["Toy_slate"])
    prism("roof_hatch", r(12.0, 13.4, 6.4, 8.0), Z_A - EMBED, Z_A + 0.45,
          mats["Toy_slate"])
    # A louvred screen round the plant field, and the small roof deck over the
    # notch corner - the satellite imagery shows tables and a curved balcony
    # there. Between them they stop plateau A reading as an empty pale plane.
    for i, (u0, u1, v0, v1) in enumerate(((15.6, 27.6, -13.2, -12.9),
                                          (15.6, 15.9, -13.2, 6.4),
                                          (15.6, 27.6, 6.1, 6.4))):
        prism(f"roof_screen{i}", r(u0, u1, v0, v1), Z_A - EMBED, Z_A + 1.55,
              mats["Toy_steel"], mats["Toy_steel"])
    prism("roof_deck", r(20.4, 29.4, 9.0, 17.6), Z_A - 0.02, Z_A + 0.14,
          mats["Toy_stone"])
    for i, (u, v) in enumerate(((22.0, 11.0), (25.4, 12.6), (23.2, 15.0))):
        disc(f"roof_parasol{i}", u, v, Z_A + 0.10, Z_A + 2.35, 0.16, 6,
             mats["Toy_steel"])
        disc(f"roof_parasol{i}_top", u, v, Z_A + 2.35, Z_A + 2.55, 1.35, 8,
             mats["Toy_sand"], mats["Toy_sand"])
    # Spa Vitale: a rooftop corner pavilion in a bamboo garden (Conde Nast,
    # Ocean Home), on the Embarcadero corner of the tall block.
    prism("spa_deck", r(6.9, 16.8, -19.6, -8.2), Z_A - 0.02, Z_A + 0.14,
          mats["Toy_stone"])
    prism("spa_pavilion", r(7.6, 13.6, -19.0, -13.4), Z_A - EMBED, Z_A + 2.45,
          mats["Toy_sand"], mats["Toy_sand"])
    prism("spa_glazing", r(7.6, 13.6, -13.6, -13.3), Z_A + 0.80, Z_A + 2.05,
          mats["Toy_glassl"])
    for i, (u, v, s) in enumerate(((8.0, -11.8, 1.5), (10.6, -12.4, 1.2),
                                   (13.4, -11.6, 1.35), (15.2, -12.6, 1.1))):
        prism(f"spa_bamboo{i}", r(u, u + s, v, v + s), Z_A + 0.10, Z_A + 2.20,
              mats["Toy_sage"], mats["Toy_sage"])


def terrace(poly, top, tag, mats):
    """A planted roof-terrace deck: large turf panels with paved circulation
    between them, inset from the parapet. NOT a full green lid - the satellite
    imagery shows a grid of planted panels with paths, and a solid slab of
    Toy_leaf reads as a billiard table from the aerial camera."""
    bed = inset_polygon(poly, 1.05)
    prism(f"terr_bed_{tag}", bed, top - 0.06, top + 0.10, mats["Toy_stone"])
    lo = min(p[0] for p in bed), min(p[1] for p in bed)
    # panels are laid out in the (u, v) frame so they line up with the block
    # Deliberately many small panels with wide paths between them. A handful of
    # big rectangles is what the satellite imagery looks like at a glance and
    # what the first build did, and from the app's aerial camera it reads as a
    # billiard table rather than as a garden.
    if tag == "b":
        us = [(-9.8, -6.3), (-5.5, -2.0), (-1.2, 2.3), (3.1, 4.8)]
        vs = [(-18.6, -14.6), (-13.8, -9.8), (-9.0, -5.0), (-4.2, -0.2),
              (0.6, 4.6), (5.4, 9.4), (10.2, 14.2), (15.0, 18.9)]
    else:
        us = [(-30.6, -27.1), (-26.3, -22.8), (-22.0, -18.5), (-17.7, -13.6)]
        vs = [(5.2, 9.2), (10.0, 14.0), (14.8, 18.9)]
    cells = [(u0, u1, v0, v1) for (u0, u1) in us for (v0, v1) in vs]
    for i, (u0, u1, v0, v1) in enumerate(cells):
        prism(f"terr_{tag}_{i}",
              [W(u0, v0), W(u1, v0), W(u1, v1), W(u0, v1)],
              top + 0.08, top + 0.22, mats["Toy_leaf"], mats["Toy_leaf"])
    # a railing line along the parapet, so the decks read as accessible
    rim(f"terr_rail_{tag}", inset_polygon(poly, 0.30),
        0.09, top + 0.02, top + 0.42, mats["Toy_steel"])


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
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] plateaus A={Z_A} B={Z_B} C={Z_C:.2f} crown={Z_CROWN}")
    print(f"[build] Mission faces {MISSION.heading:.2f} deg ({MISSION.length:.2f} m); "
          f"Steuart {STEUART_C.heading:.2f} ({STEUART_A.length + STEUART_B.length + STEUART_C.length:.2f} m); "
          f"Embarcadero {EMBARC_A.heading:.2f} ({EMBARC_A.length + EMBARC_B.length:.2f} m); "
          f"Don Chee {DONCHEE.heading:.2f} ({DONCHEE.length:.2f} m)")
    print(f"[build] turret tangents: v={V_TUR_SE:.2f} on Mission, u={U_TUR_NE:.2f} on Embarcadero")
    print(f"[build] lit openings={len(LIT)}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "8-mission.blend")
    glb = os.path.join(out, "8-mission.glb")
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
