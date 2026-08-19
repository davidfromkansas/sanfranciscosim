"""Deterministic Blender build of the SF-SIM miniature 76-82 South Park.

    blender -b --python build_76_south_park.py -- [--out DIR]

Writes 76-south-park.blend and 76-south-park.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, penthouse crest exactly
16.28 m.

Design (see REFERENCE.md for the sources behind every number, and
docs/asset-plans/76-south-park.md for the dossier):

* a 1906 post-earthquake wood-frame flats building on the north-west rim of the
  South Park oval, occupying the whole of a ~22 ft x 97.6 ft lot — 6.90 m of
  frontage against 29.70 m of depth. Four levels. Party walls on BOTH sides;
* recognition rests on the PROPORTION first (it is more than four times deeper
  than it is wide) and on the STREET COMPOSITION second: a rusticated cast-stone
  base carrying a tall arched opening on the south-west half, a full-height
  stone pier, and a two-storey canted bay cantilevered off that pier on the
  north-east half;
* the silhouette steps on ONE side only. 84 South Park (south-west) is 1.72 m
  shorter, so a band of that party wall is exposed; 70 South Park (north-east)
  is only 0.21 m shorter, so that edge reads as a continuous roofline and gets
  no band. Getting that asymmetry right is the cheapest realism available here;
* the roof is flat at 13.08 m (LiDAR median, measured) with a 0.35 m parapet,
  and it is NOT empty: both rental listings document a COMMON ROOF DECK,
  furnished, with a barbecue, "open nights and weekends". The deck goes on the
  street third — that is where the "views of South Park" and "downtown views"
  the listings sell actually are — with a stair penthouse behind it;
* the penthouse rises to 16.28 m and is the tallest geometry, so it sets the
  normalization. It is built as a SINGLE SEPARATE OBJECT on purpose: the 2010
  LiDAR maximum it is derived from is 16.28 m over this footprint and 16.35 m
  over 70 South Park's, i.e. one tall element sits on or beside the shared party
  wall and the LiDAR cannot say which building owns it. Photogrammetry off the
  Hawthorne Group photograph brackets a 8-11 m setback at 15.7-16.8 m, which is
  why it is kept — but if better imagery kills it, deleting `roof_penthouse` and
  renormalizing to the 13.43 m parapet is the whole fix. See REPORT.md;
* the two-car garage both listings document is NOT confidently locatable on this
  elevation, and the 311 record points at the rear yard instead, so the
  south-west end of the ground floor is a neutral dark service bay rather than a
  detailed roll-up door;
* night state: three windows lit, unevenly — two in the bay on different levels,
  one in the grid window. This is three flats on a quiet residential oval; a
  fully lit grid would read as an office. Plus a thin warm spill in the entry
  recess and a low warm line along the roof-deck railing, which is the one place
  this building is documented to be used after dark. Glow surfaces are thin OPEN
  shells proud of the opaque glazing: the app renders _Glow in a separate layer
  that is not fully transparent by day, so a primary surface must never be
  authored as glow and a CLOSED glow shell reads as two stacked layers and tints
  the facade in daylight.

Authoring frame: the footprint is a clean rectangle at 45 deg to the world axes,
so everything is placed through local frames built from it — a FRONT frame (t
along the 6.90 m street frontage from the south-west party wall, d outward at
135 deg), a LONG frame (s from the street edge toward the rear, u across from
the south-west party wall), and three more frames on the canted bay's own faces.
Because the building sits at 45 deg, the axis-aligned XY bounding box is
~25.9 x 25.9 m even though the building is 6.90 x 29.70 m. That is expected, not
a scale error.
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

# Area centroid of the DataSF LiDAR footprint SF3775054 — the manifest anchor
# before recentring. See the plan's 2.3 and 2.13.
DESIGN_ANCHOR = (-122.3940150, 37.7820265)

# Lot. Three sources disagree and none is authoritative for both dimensions:
#   OSM way/124884340 trace        7.22 x 29.43 m  (traces run generous)
#   DataSF LiDAR raster SF3775054  6.93 x 30.60 m  (a measurement of the
#                                                   structure — best for WIDTH)
#   SF Assessor 2147.2 sqft / 97.6 ft depth
#                                  6.71 x 29.75 m  (recorded — best for DEPTH)
# 6.90 x 29.70 sits inside all three. See the plan's 2.3 and 2.15 risk 4.
FRONTAGE = 6.90
DEPTH = 29.70
AXIS_BEARING = 315.0      # street -> rear (north-west)
FRONT_BEARING = 135.0     # the street elevation faces south-east, onto the oval

Z_DECK = 13.08            # flat roof deck — MEASURED (DataSF LiDAR height median
                          # over 763 cells; for a flat roof the median is the
                          # deck). OSM height=13 agrees with it.
Z_PARAPET = 13.43         # deck + a 0.35 m parapet
Z_CREST = 16.28           # roof-stair penthouse — the LiDAR maximum, ATTRIBUTED.
                          # The bbox top and the manifest targetHeightM, so the
                          # loader's scale is exactly 1.0. See REPORT.md.

Z_FLANK = 11.36           # 84 South Park's roof (LiDAR median): everything above
                          # this on the south-west party wall is exposed
Z_NE_NEIGHBOUR = 12.87    # 70 South Park's roof — only 0.21 m below Z_DECK, so
                          # the north-east flank gets NO exposed band

# Floor lines. Four levels over 13.08 m: a taller commercial/service ground
# floor and three residential levels, which is what the January 2025 pano shows.
Z_L1, Z_L2, Z_L3 = 3.40, 6.90, 10.00

Z_STONE = Z_L2            # the rusticated base covers the ground floor and L1
Z_BAY0, Z_BAY1 = 7.05, 12.90
Z_CORBEL0, Z_CORBEL1 = 6.55, 7.05

ARCH_T0, ARCH_T1 = 0.35, 2.55   # the tall arched opening, south-west half
ARCH_Z0, ARCH_SPRING = 0.30, 4.30
ARCH_SEGS = 12
ARCH_DEPTH = 0.30

PIER_T0, PIER_T1 = 2.90, 3.90   # the full-height stone pier
PIER_PROUD = 0.14
STONE_PROUD = 0.09
GROOVE_Z = (2.30, 4.60)         # rustication courses in the base

# Canted bay, north-east half. Projection is exaggerated to 0.95 m (real bays
# project 0.6-0.9 m) so the shadow line reads from the app's aerial camera —
# style bible licence, recorded in the plan's 2.6.
BAY_T0, BAY_T1 = 3.90, 6.85
BAY_RETURN = 0.70               # lateral run of each angled return
BAY_PROJ = 0.95

GRID_T0, GRID_T1 = 0.45, 2.45   # the industrial multi-pane window, L2 south-west
GRID_Z0, GRID_Z1 = 7.45, 10.15
GRID_COLS, GRID_ROWS = 4, 3
MULLION = 0.06

SOFFIT_Z = 10.55                # shallow ledge over the grid window
L3SW_T = (0.95, 2.05)           # two small windows, L3 south-west
L3SW_Z0, L3SW_Z1 = 10.90, 12.45

ENTRY_T0, ENTRY_T1 = 3.95, 5.05  # recessed entry, just north-east of the pier
ENTRY_H, ENTRY_D = 2.85, 0.50
SHOP_T0, SHOP_T1 = 5.20, 6.75    # storefront glazing
SHOP_Z0, SHOP_Z1 = 0.45, 3.15
SERVICE_T0, SERVICE_T1 = 0.40, 2.50   # neutral dark service bay, south-west end
SERVICE_Z1 = 3.00
BAND_T0, BAND_T1 = 4.20, 6.70    # horizontal band window in the stone at L1
BAND_Z0, BAND_Z1 = 4.90, 6.35

# Juliet balcony at the band window. The first build put this at the top of the
# stone base spanning the bay's full width, where the bay's corbel — which
# projects 0.95 m over the same t range — swallowed it completely and it did not
# appear in a single render. The Hawthorne photograph puts the railing at roughly
# 37% of the facade height, which is the band-window sill, not the corbel line.
BALC_Z = 4.90
BALC_T0, BALC_T1 = 4.15, 6.75
BALC_D, BALC_H = 0.30, 0.90

WIN_W, WIN_H = 0.85, 1.75        # the bay's window module
WIN_RECESS = 0.10

# Roof. `s` runs from the street edge toward the rear, `u` across from the
# south-west party wall.
DECK_S0, DECK_S1 = 1.00, 9.20    # the roof deck, on the street third
DECK_U0, DECK_U1 = 0.45, 6.45
DECK_H = 0.18
RAIL_H = 0.92
PENT_S0, PENT_S1 = 9.90, 13.10   # stair penthouse, 3.2 m along the depth
PENT_U0, PENT_U1 = 3.40, 6.00    # 2.6 m across, toward the north-east party wall
MECH = ((16.20, 18.10, 1.30, 3.10, 0.55), (19.40, 20.60, 3.80, 5.20, 0.38))

REAR_DOOR_W, REAR_DOOR_H = 1.30, 2.25
REAR_STAIR_Z = (3.40, 6.90)

BEVEL_W, BEVEL_SEG = 0.10, 2

PALETTE_HEX = {
    "Toy_ink": "3a3530",     # the dark bronze-brown board body, the canted bay,
                             # the arch reveal, the entry recess, the service
                             # bay and the rear stair. The January 2025 pano is a
                             # north-west-facing wall in shade under a street
                             # tree and the Hawthorne photograph is in sun but
                             # possibly a decade old; both agree the body is DARK
                             # and WARM and that the base is distinctly paler.
                             # The value relation is confident, the hue is not —
                             # see REPORT.md.
    "Toy_stone": "d9d2c2",   # the rusticated cast-stone base, the full-height
                             # pier and the bay corbel
    "Toy_trim": "f3efe6",    # window sashes, bay trim, grid-window mullions,
                             # storefront mullions, parapet cap
    "Toy_glass": "2a4d73",   # all windows and the storefront band
    "Toy_steel": "9aa0a6",   # roof-deck railing, the first-floor balcony railing,
                             # rooftop mechanical plant
    "Toy_roofd": "45454a",   # the roof deck membrane, the penthouse and the
                             # north-west rear elevation
    "Toy_sand": "ece4d4",    # the exposed south-west flank band above 84
    "Toy_rust": "a86444",    # the roof-deck timber decking — the one warm note,
                             # and the only place a saturated accent can go on a
                             # building this narrow without turning it into a toy.
                             # Toy_brick (c96f4a) was tried first and REVERSED at
                             # first aerial review: 49 m2 of it on a 205 m2 roof
                             # read as a bright orange panel that took over the
                             # whole model. Toy_rust is weathered redwood, which
                             # is also what an SF roof deck actually looks like.
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


# ----------------------------------------------------------------- geometry

def _brg(deg):
    """Compass bearing -> unit vector in world XY (+X east, +Y north)."""
    r = math.radians(deg)
    return (math.sin(r), math.cos(r))


AXIS = _brg(AXIS_BEARING)          # street edge -> rear edge
PERP = _brg(AXIS_BEARING + 90.0)   # south-west edge -> north-east edge

_HC = (-AXIS[0] * DEPTH / 2.0, -AXIS[1] * DEPTH / 2.0)   # street-edge midpoint
STREET_SW = (_HC[0] - PERP[0] * FRONTAGE / 2.0, _HC[1] - PERP[1] * FRONTAGE / 2.0)
STREET_NE = (_HC[0] + PERP[0] * FRONTAGE / 2.0, _HC[1] + PERP[1] * FRONTAGE / 2.0)
REAR_NE = (STREET_NE[0] + AXIS[0] * DEPTH, STREET_NE[1] + AXIS[1] * DEPTH)
REAR_SW = (STREET_SW[0] + AXIS[0] * DEPTH, STREET_SW[1] + AXIS[1] * DEPTH)

FOOTPRINT = [STREET_SW, STREET_NE, REAR_NE, REAR_SW]

CX = sum(p[0] for p in FOOTPRINT) / 4.0
CY = sum(p[1] for p in FOOTPRINT) / 4.0


def long_xy(s, u):
    """LONG frame: s metres from the street edge toward the rear, u metres
    across from the south-west party wall."""
    return (
        STREET_SW[0] + AXIS[0] * s + PERP[0] * u,
        STREET_SW[1] + AXIS[1] * s + PERP[1] * u,
    )


def long_rect(s0, s1, u0, u1):
    return [long_xy(s0, u0), long_xy(s1, u0), long_xy(s1, u1), long_xy(s0, u1)]


class Face:
    """A local frame on one elevation: t runs along the face from `a` to `b`,
    d runs OUTWARD (away from the footprint centroid), z is world up."""

    def __init__(self, a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        self.a = a
        self.length = n
        self.t = (dx / n, dy / n)
        nrm = (-self.t[1], self.t[0])
        # Resolve the outward sense against the centroid rather than trusting
        # the winding order — the canted bay's own faces depend on this.
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


FRONT = Face(STREET_SW, STREET_NE)   # the street elevation, faces 135 deg
REAR = Face(REAR_NE, REAR_SW)        # the rear yard, faces 315 deg
FLANK_SW = Face(REAR_SW, STREET_SW)  # toward 84 South Park, faces 225 deg

# The canted bay's plan outline and its three own face frames.
BAY_P0 = FRONT.xy(BAY_T0, 0.0)
BAY_P1 = FRONT.xy(BAY_T0 + BAY_RETURN, BAY_PROJ)
BAY_P2 = FRONT.xy(BAY_T1 - BAY_RETURN, BAY_PROJ)
BAY_P3 = FRONT.xy(BAY_T1, 0.0)
BAY_PLAN = [BAY_P0, BAY_P1, BAY_P2, BAY_P3]
BAY_FRONT = Face(BAY_P1, BAY_P2)
BAY_SW = Face(BAY_P0, BAY_P1)
BAY_NE = Face(BAY_P2, BAY_P3)


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
    """Miniature-style edge softening (style bible s.4). The offset is capped at
    a third of the object's thinnest dimension: window fills, sills, mullions and
    glow shells are only 40-120 mm thick and a full bevel on those collapses
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


def profile_solid(name, face, pts_tz, d0, d1, mat):
    """Extrude a closed (t, z) profile on `face` along the face NORMAL from d0
    to d1. This is how the arched head is built: the arch curves in the plane of
    the elevation, so it cannot come out of prism(), which extrudes in Z."""
    n = len(pts_tz)
    verts = [face.xy(t, d0) + (z,) for t, z in pts_tz]
    verts += [face.xy(t, d1) + (z,) for t, z in pts_tz]
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    return new_mesh(name, verts, faces, [mat])


def arch_profile(t0, t1, z0, z_spring, segs=ARCH_SEGS):
    """Closed (t, z) profile: a rectangle from z0 to the springing line, capped
    by a semicircular head of radius (t1 - t0) / 2."""
    r = (t1 - t0) / 2.0
    tc = (t0 + t1) / 2.0
    pts = [(t0, z0), (t1, z0), (t1, z_spring)]
    for i in range(1, segs):
        a = math.pi * i / segs
        pts.append((tc + r * math.cos(a), z_spring + r * math.sin(a)))
    pts.append((t0, z_spring))
    return pts


def inset_polygon(poly, dist):
    """Offset every edge of a simple polygon inward by `dist` and re-intersect
    adjacent edges. Negative dist offsets outward (a proud band)."""
    n = len(poly)
    lines = []
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy)
        d = (dx / m, dy / m)
        nrm = (-d[1], d[0])
        if (a[0] + nrm[0] - CX) ** 2 + (a[1] + nrm[1] - CY) ** 2 > (a[0] - CX) ** 2 + (
            a[1] - CY
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
    """Closed band solid between `poly` and its offset — the parapet, and the
    roof-deck railing."""
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


def glow_shell(name, face, t0, t1, z0, z1, d, mats):
    """An OPEN shell (four side bands, no front or back cap) proud of the opaque
    glazing. A closed box here is two stacked alpha layers by day and tints the
    facade — see the module docstring."""
    m = 0.05
    # outer ring then inner ring, both at depth d
    outer = [(t0 - m, z0 - m), (t1 + m, z0 - m), (t1 + m, z1 + m), (t0 - m, z1 + m)]
    inner = [(t0 + m, z0 + m), (t1 - m, z0 + m), (t1 - m, z1 - m), (t0 + m, z1 - m)]
    verts = [face.xy(t, d) + (z,) for t, z in outer]
    verts += [face.xy(t, d) + (z,) for t, z in inner]
    faces = [(i, (i + 1) % 4, 4 + (i + 1) % 4, 4 + i) for i in range(4)]
    return new_mesh(name, verts, faces, [mats["Toy_glassl_Glow"]])


def window(name, face, t_centre, z_sill, mats, lit=False, wall_d=0.0,
           w=WIN_W, h=WIN_H):
    """A recessed opening with a proud sill and trim — the module used on the
    canted bay's three faces and on the rear elevation."""
    t0, t1 = t_centre - w / 2.0, t_centre + w / 2.0
    prism(
        f"{name}_fill",
        face.rect(t0, t1, -WIN_RECESS, wall_d + 0.02),
        z_sill,
        z_sill + h,
        mats["Toy_glass"],
    )
    prism(
        f"{name}_sill",
        face.rect(t0 - 0.09, t1 + 0.09, wall_d, wall_d + 0.09),
        z_sill - 0.11,
        z_sill,
        mats["Toy_trim"],
    )
    if lit:
        glow_shell(f"{name}_glow", face, t0, t1, z_sill, z_sill + h,
                   wall_d + 0.05, mats)


def build():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    scene = bpy.context.scene
    mats = {k: make_material(k) for k in PALETTE_HEX}

    # ---------------------------------------------------------- main volume
    prism("body", FOOTPRINT, 0.0, Z_DECK, mats["Toy_ink"], mat_top=mats["Toy_roofd"])

    # Parapet: a lift on the street end and both flanks. Built as a full rim and
    # then it is fine that it also runs the rear — a 0.35 m upstand is what a
    # flat-roofed row building has all round.
    rim("parapet", FOOTPRINT, 0.18, Z_DECK, Z_PARAPET, mats["Toy_stone"])

    # ------------------------------------------------------ rusticated base
    prism(
        "stone_base",
        FRONT.rect(0.0, FRONTAGE, 0.0, STONE_PROUD),
        0.0,
        Z_STONE,
        mats["Toy_stone"],
    )
    for i, z in enumerate(GROOVE_Z):
        prism(
            f"stone_groove_{i}",
            FRONT.rect(0.0, FRONTAGE, STONE_PROUD - 0.03, STONE_PROUD + 0.005),
            z,
            z + 0.07,
            mats["Toy_ink"],
        )

    # The full-height pier: the spine the bay's corbel springs from.
    prism(
        "stone_pier",
        FRONT.rect(PIER_T0, PIER_T1, 0.0, PIER_PROUD),
        0.0,
        Z_BAY1,
        mats["Toy_stone"],
    )

    # The tall arched opening, cut into the base as a dark recess.
    profile_solid(
        "arch_recess",
        FRONT,
        arch_profile(ARCH_T0, ARCH_T1, ARCH_Z0, ARCH_SPRING),
        STONE_PROUD - ARCH_DEPTH,
        STONE_PROUD + 0.01,
        mats["Toy_ink"],
    )

    # ------------------------------------------------------- ground floor
    prism(
        "service_bay",
        FRONT.rect(SERVICE_T0, SERVICE_T1, STONE_PROUD - ARCH_DEPTH - 0.04,
                   STONE_PROUD - ARCH_DEPTH + 0.02),
        0.0,
        SERVICE_Z1,
        mats["Toy_ink"],
    )
    prism(
        "entry_recess",
        FRONT.rect(ENTRY_T0, ENTRY_T1, -ENTRY_D, STONE_PROUD + 0.01),
        0.0,
        ENTRY_H,
        mats["Toy_ink"],
    )
    # A thin warm LINTEL band at the head of the recess, not a rectangular ring:
    # at 12% day alpha a ring reads as a pale panel floating in the doorway.
    prism(
        "entry_glow",
        FRONT.rect(ENTRY_T0 + 0.10, ENTRY_T1 - 0.10, STONE_PROUD + 0.02,
                   STONE_PROUD + 0.06),
        ENTRY_H - 0.34,
        ENTRY_H - 0.12,
        mats["Toy_trim_Glow"],
    )

    prism(
        "shopfront",
        FRONT.rect(SHOP_T0, SHOP_T1, STONE_PROUD - 0.14, STONE_PROUD + 0.01),
        SHOP_Z0,
        SHOP_Z1,
        mats["Toy_glass"],
    )
    for i in range(1, 3):
        t = SHOP_T0 + (SHOP_T1 - SHOP_T0) * i / 3.0
        prism(
            f"shop_mullion_{i}",
            FRONT.rect(t - MULLION / 2, t + MULLION / 2, STONE_PROUD - 0.14,
                       STONE_PROUD + 0.03),
            SHOP_Z0,
            SHOP_Z1,
            mats["Toy_trim"],
        )

    # A horizontal band window in the stone at L1, north-east of the pier.
    prism(
        "band_window",
        FRONT.rect(BAND_T0, BAND_T1, STONE_PROUD - 0.13, STONE_PROUD + 0.01),
        BAND_Z0,
        BAND_Z1,
        mats["Toy_glass"],
    )
    prism(
        "band_sill",
        FRONT.rect(BAND_T0 - 0.09, BAND_T1 + 0.09, STONE_PROUD, STONE_PROUD + 0.09),
        BAND_Z0 - 0.11,
        BAND_Z0,
        mats["Toy_trim"],
    )

    # ------------------------------------------- grid window + L3 south-west
    prism(
        "grid_fill",
        FRONT.rect(GRID_T0, GRID_T1, -0.12, 0.02),
        GRID_Z0,
        GRID_Z1,
        mats["Toy_glass"],
    )
    for i in range(1, GRID_COLS):
        t = GRID_T0 + (GRID_T1 - GRID_T0) * i / GRID_COLS
        prism(
            f"grid_mullion_v{i}",
            FRONT.rect(t - MULLION / 2, t + MULLION / 2, -0.12, 0.04),
            GRID_Z0,
            GRID_Z1,
            mats["Toy_trim"],
        )
    for j in range(1, GRID_ROWS):
        z = GRID_Z0 + (GRID_Z1 - GRID_Z0) * j / GRID_ROWS
        prism(
            f"grid_mullion_h{j}",
            FRONT.rect(GRID_T0, GRID_T1, -0.12, 0.04),
            z - MULLION / 2,
            z + MULLION / 2,
            mats["Toy_trim"],
        )
    # A FRAME, not a slab. The first build made this a solid prism across the
    # whole opening at d 0.00-0.08, which sat in front of the glazing and
    # rendered the building's second-largest window as a blank cream panel.
    for tag, (t0, t1, z0, z1) in {
        "l": (GRID_T0 - 0.10, GRID_T0, GRID_Z0 - 0.10, GRID_Z1 + 0.10),
        "r": (GRID_T1, GRID_T1 + 0.10, GRID_Z0 - 0.10, GRID_Z1 + 0.10),
        "b": (GRID_T0, GRID_T1, GRID_Z0 - 0.10, GRID_Z0),
        "t": (GRID_T0, GRID_T1, GRID_Z1, GRID_Z1 + 0.10),
    }.items():
        prism(
            f"grid_surround_{tag}",
            FRONT.rect(t0, t1, 0.0, 0.08),
            z0,
            z1,
            mats["Toy_trim"],
        )
    glow_shell("grid_glow", FRONT, GRID_T0, GRID_T1, GRID_Z0, GRID_Z1, 0.09, mats)

    prism(
        "soffit",
        FRONT.rect(GRID_T0 - 0.15, GRID_T1 + 0.15, 0.0, 0.50),
        SOFFIT_Z,
        SOFFIT_Z + 0.16,
        mats["Toy_ink"],
    )
    for i, t in enumerate(L3SW_T):
        window(f"l3sw_{i}", FRONT, t, L3SW_Z0, mats, w=0.80,
               h=L3SW_Z1 - L3SW_Z0)

    # ------------------------------------------------------------ canted bay
    prism("bay_corbel", BAY_PLAN, Z_CORBEL0, Z_CORBEL1, mats["Toy_stone"])
    prism("bay", BAY_PLAN, Z_BAY0, Z_BAY1, mats["Toy_ink"],
          mat_top=mats["Toy_roofd"])

    bay_front_c = BAY_FRONT.length / 2.0
    for lvl, z_sill in enumerate((Z_BAY0 + 0.55, Z_L3 + 0.55)):
        window(f"bay_front_{lvl}", BAY_FRONT, bay_front_c, z_sill, mats,
               lit=(lvl == 0), w=1.15)
        window(f"bay_sw_{lvl}", BAY_SW, BAY_SW.length / 2.0, z_sill, mats,
               w=0.52)
        window(f"bay_ne_{lvl}", BAY_NE, BAY_NE.length / 2.0, z_sill, mats,
               lit=(lvl == 1), w=0.52)

    # Balcony railing over the entry, under the bay.
    prism(
        "balcony_deck",
        FRONT.rect(BALC_T0, BALC_T1, STONE_PROUD, STONE_PROUD + BALC_D),
        BALC_Z - 0.12,
        BALC_Z,
        mats["Toy_stone"],
    )
    prism(
        "balcony_rail_top",
        FRONT.rect(BALC_T0, BALC_T1, STONE_PROUD + BALC_D - 0.05,
                   STONE_PROUD + BALC_D),
        BALC_Z + BALC_H - 0.06,
        BALC_Z + BALC_H,
        mats["Toy_steel"],
    )
    for i in range(9):
        t = BALC_T0 + (BALC_T1 - BALC_T0) * (i + 0.5) / 9.0
        prism(
            f"balcony_rail_{i}",
            FRONT.rect(t - 0.022, t + 0.022, STONE_PROUD + BALC_D - 0.05,
                       STONE_PROUD + BALC_D),
            BALC_Z,
            BALC_Z + BALC_H,
            mats["Toy_steel"],
        )

    # -------------------------------------------------- exposed SW flank band
    # ONLY on the south-west side. 70 South Park (north-east) is 0.21 m lower,
    # so that party wall is effectively invisible and gets nothing.
    prism(
        "flank_sw_band",
        FLANK_SW.rect(0.0, DEPTH, 0.0, 0.045),
        Z_FLANK,
        Z_DECK,
        mats["Toy_sand"],
    )

    # ------------------------------------------------------- rear elevation
    prism(
        "rear_face",
        REAR.rect(0.0, FRONTAGE, 0.0, 0.045),
        0.0,
        Z_DECK,
        mats["Toy_roofd"],
    )
    prism(
        "rear_door",
        REAR.rect(1.10, 1.10 + REAR_DOOR_W, -0.10, 0.06),
        0.0,
        REAR_DOOR_H,
        mats["Toy_ink"],
    )
    for row, z in enumerate((Z_L1 + 0.75, Z_L2 + 0.75, Z_L3 + 0.75)):
        for col, t in enumerate((1.75, 4.10, 5.60)):
            window(f"rear_{row}_{col}", REAR, t, z, mats, wall_d=0.045, w=0.80,
                   h=1.45)
    # Rear stair — the DBI record's "rear stairs", the only documented feature
    # on this elevation.
    prism(
        "rear_stair_stringer",
        REAR.rect(4.90, 6.55, 0.045, 1.15),
        REAR_STAIR_Z[0] - 0.18,
        REAR_STAIR_Z[0],
        mats["Toy_ink"],
    )
    prism(
        "rear_stair_upper",
        REAR.rect(4.90, 6.55, 0.045, 1.15),
        REAR_STAIR_Z[1] - 0.18,
        REAR_STAIR_Z[1],
        mats["Toy_ink"],
    )
    for i in range(4):
        t = 4.90 + 1.65 * (i + 0.5) / 4.0
        prism(
            f"rear_stair_post_{i}",
            REAR.rect(t - 0.04, t + 0.04, 1.05, 1.13),
            REAR_STAIR_Z[0],
            REAR_STAIR_Z[1],
            mats["Toy_ink"],
        )

    # ------------------------------------------------------------------ roof
    # The roof deck, on the street third. Both listings document it; the plan's
    # 2.9 argues for this position from what the listings say the views are.
    prism(
        "roof_deck",
        long_rect(DECK_S0, DECK_S1, DECK_U0, DECK_U1),
        Z_DECK,
        Z_DECK + DECK_H,
        mats["Toy_rust"],
    )
    deck_poly = long_rect(DECK_S0, DECK_S1, DECK_U0, DECK_U1)
    rim("roof_rail", deck_poly, 0.06, Z_DECK + DECK_H + RAIL_H - 0.05,
        Z_DECK + DECK_H + RAIL_H, mats["Toy_steel"])
    for i in range(9):
        s = DECK_S0 + (DECK_S1 - DECK_S0) * i / 8.0
        prism(
            f"roof_rail_post_s{i}",
            long_rect(s - 0.03, s + 0.03, DECK_U0, DECK_U0 + 0.06),
            Z_DECK + DECK_H,
            Z_DECK + DECK_H + RAIL_H,
            mats["Toy_steel"],
        )
        prism(
            f"roof_rail_post_n{i}",
            long_rect(s - 0.03, s + 0.03, DECK_U1 - 0.06, DECK_U1),
            Z_DECK + DECK_H,
            Z_DECK + DECK_H + RAIL_H,
            mats["Toy_steel"],
        )
    # Warm festoon lights along the railing — the deck is documented "open nights
    # and weekends", which is the whole reason it earns a glow. Authored as ten
    # DASHES rather than one continuous strip: the first night render made a
    # single 8.2 m bar that read as a neon tube and outshone the three lit
    # windows, which are supposed to be the hero.
    n_lamp = 10
    for i in range(n_lamp):
        s0 = DECK_S0 + (DECK_S1 - DECK_S0) * (i + 0.30) / n_lamp
        s1 = DECK_S0 + (DECK_S1 - DECK_S0) * (i + 0.70) / n_lamp
        prism(
            f"roof_lamp_glow_{i}",
            long_rect(s0, s1, DECK_U0 - 0.02, DECK_U0 + 0.02),
            Z_DECK + DECK_H + RAIL_H - 0.13,
            Z_DECK + DECK_H + RAIL_H - 0.08,
            mats["Toy_trim_Glow"],
        )

    # THE PENTHOUSE. One object, deletable in one step — see the docstring and
    # REPORT.md. This is the tallest geometry and it sets targetHeightM.
    prism(
        "roof_penthouse",
        long_rect(PENT_S0, PENT_S1, PENT_U0, PENT_U1),
        Z_DECK,
        Z_CREST,
        mats["Toy_roofd"],
    )

    for i, (s0, s1, u0, u1, h) in enumerate(MECH):
        prism(
            f"roof_mech_{i}",
            long_rect(s0, s1, u0, u1),
            Z_DECK,
            Z_DECK + h,
            mats["Toy_steel"],
        )

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.10/2. Windows, sills, mullions, grooves, rails and glow shells are small
    # and numerous — a token softening or none at all is what keeps this under
    # cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        n = obj.name
        # Substring tests, not endswith: the festoon lamps are named
        # roof_lamp_glow_<i>, and an earlier endswith("_glow") test missed them
        # and spent ~1,000 triangles bevelling ten 0.3 m boxes.
        if "_fill" in n or "_glow" in n or "_rail" in n or "_mullion" in n \
                or "_groove" in n or "_post_" in n:
            continue
        if n.endswith("_sill") or n.startswith(("rear_stair", "arch_recess")):
            bevel(obj, width=0.03, segments=1)
        else:
            bevel(obj)

    recentre()
    return scene


ANCHOR_SHIFT = [0.0, 0.0]


def recentre():
    """Move the model so its XY bounding-box centre is the origin, and carry the
    same shift into the anchor so the building stays on its real footprint
    (AGENTS rule 5)."""
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
    print(f"[build] footprint: {FRONTAGE:.2f} x {DEPTH:.2f} m = {FRONTAGE * DEPTH:.1f} m2")
    print(f"[build] design (LiDAR area-centroid) anchor: {DESIGN_ANCHOR}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] street elevation faces: {FRONT.heading:.2f} deg true")
    print(f"[build] rear faces: {REAR.heading:.2f} deg; SW flank faces: {FLANK_SW.heading:.2f} deg")
    print(f"[build] bay faces: front {BAY_FRONT.heading:.2f}, sw {BAY_SW.heading:.2f}, ne {BAY_NE.heading:.2f}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "76-south-park.blend")
    glb = os.path.join(out, "76-south-park.glb")
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
