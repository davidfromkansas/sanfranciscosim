"""Deterministic Blender build of the SF-SIM miniature 26-28 South Park
(51 Taber Place).

    blender -b --python build_26_south_park.py -- [--out DIR]

Writes 26-south-park.blend and 26-south-park.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, parapet crest exactly
9.05 m.

Design (see REFERENCE.md for the sources behind every number):

* a 1907 two-storey-over-basement through-lot on the north rim of the South Park
  oval, occupying the whole of a surveyed 30.13 x 6.69 m parcel — 6.69 m of
  frontage against 30.13 m of depth, a 4.5:1 sliver;
* the recognition rests entirely on PROPORTION and on the STEP. Both long sides
  are party walls; the Hotel Madrid at 22-24 is 4.0 m taller and 44-46 South
  Park is 5.2 m taller, so this roof is a notch in an otherwise continuous
  roofline and the model's job in the scene is to be the low dark gap;
* the height is the one real judgement in this asset. The DataSF LiDAR record
  for SF3775049 reports hgt_max 13.59 m, which is REJECTED: it matches 44-46
  South Park's own roof-plane median (13.52 m) to 7 cm, on a 7.65 m-wide raster
  footprint whose 50 cm cells are dilated into both taller party walls. The
  median (8.35 m) and majority (8.36 m) agree to 1 cm and are the deck; the
  crest is a conventional 0.70 m parapet above it. See REPORT.md;
* the street elevation is near-black and unornamented: one recessed glazed
  opening and a 1.6 m-deep entry notch at ground level, and above them the top
  floor held back 3.0 m from the frontage, leaving an OPEN DECK behind a solid
  rail — the 1984 permit's "new garage with open deck", and the only
  three-dimensional move on the whole building;
* the Taber Place rear carries the garage and, with the front, the only glazing
  the building has: "two sides of windows" is literally true here, and the
  middle 24 m of a 30 m slot is daylit by skylights instead;
* night state is the quietest in the South Park set on purpose: a warm spill in
  the entry notch and two lit windows, nothing else. Glow surfaces are thin
  CLOSED shells proud of the opaque glazing (an open face has no signed volume
  and fails the normals contract). A closed shell is two alpha layers, so by day
  it reads ~23% not the app's nominal 12% — which is why each one covers only the
  lower 55% of its opening, in a desaturated colour.

Authoring frame: the parcel is a true rectangle at 45 deg to the world axes
(measured edge dot product 0.2 m^2 over a 6.7 x 30.1 m rectangle), so everything
is placed through two local frames built from it — a FRONT frame (t along the
6.69 m street frontage, d outward at 135.2 deg) and a LONG frame (s from the
street edge toward Taber Place, u across from the south-west party wall).
Because the building sits at 45 deg, the axis-aligned XY bounding box is
~26.0 x 26.0 m even though the building is 6.69 x 30.13 m. That is expected, not
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

# Area centroid of the DataSF surveyed parcel 3775-049 — the manifest anchor
# before recentring, and the centre of the bake-time exclusion circle. See the
# plan's 2.3 and 2.13.
DESIGN_ANCHOR = (-122.3937435, 37.7822367)

# Lot, from DataSF parcels acdm-wktn blklot 3775049: an exact four-vertex
# parallelogram whose shoelace area (201.5 m2) equals its oriented bounding
# rectangle's, and which matches the Assessor's lot_area (2,167.22 sq ft =
# 201.3 m2) to 0.1%. The building fills it.
FRONTAGE = 6.69
DEPTH = 30.13
AXIS_BEARING = 315.18     # street -> rear (Taber Place, north-west)
FRONT_BEARING = 135.18    # the street elevation faces south-east, onto the oval

Z_DECK = 8.35             # flat roof deck — MEASURED (DataSF LiDAR height median,
                          # majority 8.36 m, i.e. agreeing to 1 cm)
Z_CREST = 9.05            # parapet crest: a conventional 0.70 m parapet on the
                          # measured deck. The bbox top and the manifest
                          # targetHeightM, so the loader's scale is exactly 1.0.
                          # NOT the 13.59 m LiDAR maximum — see the header and
                          # REPORT.md.

Z_FLOOR2 = 4.30           # second floor level = the open deck's floor
SETBACK = 3.00            # the top floor is held back this far from the frontage
DECK_SLAB = 0.12
RAIL_H, RAIL_T = 0.90, 0.13
FIN_W = 0.45              # the party walls returning to the frontage past the deck

PARAPET_INSET = 0.22
ROOF_SLAB = 0.12

# Street elevation, ground floor
SP_WIN_T0, SP_WIN_T1 = 0.55, 3.15      # the wide low window pair, read as one
SP_WIN_Z0, SP_WIN_Z1 = 1.05, 3.35
SP_ENTRY_T0, SP_ENTRY_T1 = 3.75, 5.55  # the recessed double-door entry
SP_ENTRY_D = 1.60
SP_ENTRY_H = 3.05
# Street elevation, second floor (3.0 m behind the frontage)
SP_UP_T0, SP_UP_T1 = 1.60, 5.10
SP_UP_Z0, SP_UP_Z1 = 5.35, 7.55

# Taber Place rear
TP_WIN_T0, TP_WIN_T1 = 0.85, 5.85
TP_UP_Z0, TP_UP_Z1 = 4.90, 7.90
TP_LO_Z0, TP_LO_Z1 = 1.50, 4.00
TP_GAR_T0, TP_GAR_T1 = 0.60, 3.60      # the glazed garage door
TP_GAR_Z1 = 2.60
TP_DOOR_T0, TP_DOOR_T1 = 4.30, 5.30    # the personnel door
TP_DOOR_Z1 = 2.20

WIN_RECESS = 0.16
FRAME_T = 0.14
GROOVE_D = 0.06

SKY_W, SKY_L, SKY_H = 1.55, 2.40, 0.38
# Skylight centres from the street edge. The leasing listing sells "skylights"
# without a count; five over the rear two thirds is what a 30 m slot with two
# blind party walls actually needs, and three read as an under-designed roof at
# the app's camera (style bible: the camera looks down, roofs are facades).
SKY_S = (6.6, 10.6, 14.6, 18.6, 22.6)

BEVEL_W, BEVEL_SEG = 0.12, 2

PALETTE_HEX = {
    "Toy_ink": "3a3530",      # the body — all four elevations, both party walls,
                              # the parapet. The palette has no true black and
                              # this building should not have one either; the
                              # real facade is a very dark warm charcoal.
    "Toy_roofd": "45454a",    # entry and personnel door panels, rear siding grooves
    "Toy_steel": "9aa0a6",    # deck rail, garage panel, skylight kerbs, plant
    "Toy_trim": "f3efe6",     # every window frame band and the entry head band
    "Toy_glass": "2a4d73",    # all glazing and the skylight tops
    "Toy_stone": "d9d2c2",    # the flat roof deck and the open deck floor — kept
                              # a clear value ABOVE the body so that from the
                              # aerial camera the deck reads as a floor at the
                              # bottom of a 4-5 m canyon, not as shadow
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
    """LONG frame: s metres from the street edge toward Taber Place, u metres
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


FRONT = Face(STREET_SW, STREET_NE)   # South Park, faces 135.2 deg
REAR = Face(REAR_NE, REAR_SW)        # Taber Place, faces 315.2 deg
FLANK_SW = Face(REAR_SW, STREET_SW)  # toward 44-46, faces 225.2 deg
FLANK_NE = Face(STREET_NE, REAR_NE)  # toward the Hotel Madrid, faces 45.2 deg


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
    a third of the object's thinnest dimension: window fills, frames and glow
    shells are only 40-160 mm thick and a full bevel on those collapses opposing
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
    """Closed band solid between `poly` and its offset — the parapet."""
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


def opening(name, face, t0, t1, z0, z1, mats, lit=False):
    """A recessed glazed opening with a flat frame band around it — the module
    used on both end elevations. There is no sill course on this building: the
    facade is a flat dark plane and the frame is the only relief."""
    prism(
        f"{name}_fill",
        face.rect(t0, t1, -WIN_RECESS, 0.02),
        z0,
        z1,
        mats["Toy_glass"],
    )
    # frame: four flat bands lying on the wall plane, framing the recess
    for tag, r in (
        ("l", (t0 - FRAME_T, t0, z0 - FRAME_T, z1 + FRAME_T)),
        ("r", (t1, t1 + FRAME_T, z0 - FRAME_T, z1 + FRAME_T)),
        ("b", (t0, t1, z0 - FRAME_T, z0)),
        ("t", (t0, t1, z1, z1 + FRAME_T)),
    ):
        prism(
            f"{name}_frame_{tag}",
            face.rect(r[0], r[1], 0.0, 0.09),
            r[2],
            r[3],
            mats["Toy_trim"],
        )
    if lit:
        # Closed thin shell, not an open face: the repo's normals contract runs a
        # per-object signed-volume test and an open plane has none. The shell is
        # then TWO alpha layers by day (1 - 0.88^2 = 0.23, not 0.12), so it covers
        # only the LOWER 55% of the opening — which is also what a lit room
        # actually looks like — in a desaturated blue.
        prism(
            f"{name}_glow",
            face.rect(t0 + 0.12, t1 - 0.12, 0.03, 0.07),
            z0 + 0.10,
            z0 + 0.10 + (z1 - z0 - 0.20) * 0.55,
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
    # Ground storey. Built as four pieces rather than one box, so the 1.6 m entry
    # notch is a real void in the mass instead of a recess drawn on a solid wall
    # — at the app's camera a painted-on entrance reads as a sticker.
    prism(
        "body_ground_front_sw",
        long_rect(0.0, SP_ENTRY_D, 0.0, SP_ENTRY_T0),
        0.0,
        Z_FLOOR2,
        mats["Toy_ink"],
    )
    prism(
        "body_ground_front_ne",
        long_rect(0.0, SP_ENTRY_D, SP_ENTRY_T1, FRONTAGE),
        0.0,
        Z_FLOOR2,
        mats["Toy_ink"],
    )
    prism(
        "body_ground_header",
        long_rect(0.0, SP_ENTRY_D, SP_ENTRY_T0, SP_ENTRY_T1),
        SP_ENTRY_H,
        Z_FLOOR2,
        mats["Toy_ink"],
    )
    prism(
        "body_ground_main",
        long_rect(SP_ENTRY_D, DEPTH, 0.0, FRONTAGE),
        0.0,
        Z_FLOOR2,
        mats["Toy_ink"],
    )

    # Upper storey: held back SETBACK from the South Park frontage.
    prism(
        "body_upper",
        long_rect(SETBACK, DEPTH, 0.0, FRONTAGE),
        Z_FLOOR2,
        Z_DECK,
        mats["Toy_ink"],
    )

    # The two party walls return to the frontage past the terrace, so from the
    # street the deck reads as a slot between two fins rather than as a missing
    # storey. Both are real lot-line walls.
    prism("fin_sw", long_rect(0.0, SETBACK, 0.0, FIN_W), Z_FLOOR2, Z_DECK, mats["Toy_ink"])
    prism(
        "fin_ne",
        long_rect(0.0, SETBACK, FRONTAGE - FIN_W, FRONTAGE),
        Z_FLOOR2,
        Z_DECK,
        mats["Toy_ink"],
    )

    # -------------------------------------------------------- the open deck
    # The slab sits ON the ground storey's roof, not flush into it: coplanar caps
    # z-fight and the darker one wins, which buried the whole terrace on the
    # first build.
    prism(
        "deck_floor",
        long_rect(0.0, SETBACK, FIN_W, FRONTAGE - FIN_W),
        Z_FLOOR2,
        Z_FLOOR2 + DECK_SLAB,
        mats["Toy_stone"],
        mat_top=mats["Toy_stone"],
    )
    prism(
        "deck_rail",
        long_rect(0.06, 0.06 + RAIL_T, FIN_W, FRONTAGE - FIN_W),
        Z_FLOOR2 + DECK_SLAB,
        Z_FLOOR2 + DECK_SLAB + RAIL_H,
        mats["Toy_steel"],
    )

    # ------------------------------------------------- South Park elevation
    opening("sp_win", FRONT, SP_WIN_T0, SP_WIN_T1, SP_WIN_Z0, SP_WIN_Z1, mats)

    # The entry notch is a real void (see body_ground above). What is added here
    # is only what stands inside or around it.
    prism(
        "entry_door",
        long_rect(SP_ENTRY_D - 0.10, SP_ENTRY_D, SP_ENTRY_T0 + 0.10, SP_ENTRY_T1 - 0.10),
        0.0,
        2.55,
        mats["Toy_roofd"],
    )
    prism(
        "entry_head",
        FRONT.rect(SP_ENTRY_T0 - 0.20, SP_ENTRY_T1 + 0.20, 0.0, 0.12),
        SP_ENTRY_H,
        SP_ENTRY_H + 0.28,
        mats["Toy_trim"],
    )
    prism(
        "entry_step",
        long_rect(-0.34, SP_ENTRY_D, SP_ENTRY_T0, SP_ENTRY_T1),
        0.0,
        0.17,
        mats["Toy_stone"],
        mat_top=mats["Toy_stone"],
    )

    # Second floor, standing SETBACK behind the frontage — the window the deck
    # looks into. Its own Face frame sits on the set-back wall plane.
    set_back_face = Face(long_xy(SETBACK, 0.0), long_xy(SETBACK, FRONTAGE))
    opening(
        "sp_up", set_back_face, SP_UP_T0, SP_UP_T1, SP_UP_Z0, SP_UP_Z1, mats, lit=True
    )

    # ------------------------------------------------ Taber Place elevation
    opening("tp_up", REAR, TP_WIN_T0, TP_WIN_T1, TP_UP_Z0, TP_UP_Z1, mats, lit=True)
    opening("tp_lo", REAR, TP_WIN_T0, TP_WIN_T1, TP_LO_Z0, TP_LO_Z1, mats)
    prism(
        "tp_garage",
        REAR.rect(TP_GAR_T0, TP_GAR_T1, -0.14, 0.02),
        0.0,
        TP_GAR_Z1,
        mats["Toy_steel"],
    )
    prism(
        "tp_door",
        REAR.rect(TP_DOOR_T0, TP_DOOR_T1, -0.18, 0.02),
        0.0,
        TP_DOOR_Z1,
        mats["Toy_roofd"],
    )
    # Lap siding, read as three shallow grooves per storey on this face only.
    for i, z in enumerate((1.05, 2.20, 3.35, 4.95, 6.10, 7.25)):
        prism(
            f"tp_groove_{i}",
            REAR.rect(0.0, FRONTAGE, -GROOVE_D, 0.0),
            z,
            z + 0.07,
            mats["Toy_roofd"],
        )

    # -------------------------------------------------------------- the roof
    rim("parapet", FOOTPRINT, PARAPET_INSET, Z_DECK, Z_CREST, mats["Toy_ink"])
    # Same rule as the deck: the membrane sits ON the storey cap, never flush
    # with it. A pale deck inside a dark parapet is what stops a 30 m roof at the
    # bottom of a 4-5 m canyon reading as shadow.
    prism(
        "roof_slab",
        inset_polygon(FOOTPRINT, PARAPET_INSET),
        Z_DECK,
        Z_DECK + ROOF_SLAB,
        mats["Toy_stone"],
        mat_top=mats["Toy_stone"],
    )
    for i, s in enumerate(SKY_S):
        prism(
            f"skylight_kerb_{i}",
            long_rect(s - SKY_L / 2, s + SKY_L / 2, FRONTAGE / 2 - SKY_W / 2, FRONTAGE / 2 + SKY_W / 2),
            Z_DECK + ROOF_SLAB,
            Z_DECK + ROOF_SLAB + SKY_H - 0.08,
            mats["Toy_steel"],
        )
        prism(
            f"skylight_glass_{i}",
            long_rect(
                s - SKY_L / 2 + 0.10,
                s + SKY_L / 2 - 0.10,
                FRONTAGE / 2 - SKY_W / 2 + 0.10,
                FRONTAGE / 2 + SKY_W / 2 - 0.10,
            ),
            Z_DECK + ROOF_SLAB + SKY_H - 0.08,
            Z_DECK + ROOF_SLAB + SKY_H,
            mats["Toy_glass"],
            mat_top=mats["Toy_glass"],
        )
    # Plant is capped at 0.45 m so the parapet stays the tallest geometry and the
    # loader's targetHeightM / measuredHeight lands on 1.0.
    prism("roof_mech_a", long_rect(26.5, 28.1, 1.20, 2.95), Z_DECK + ROOF_SLAB, Z_DECK + ROOF_SLAB + 0.45,
          mats["Toy_steel"])
    prism("roof_mech_b", long_rect(26.8, 27.9, 3.65, 4.55), Z_DECK + ROOF_SLAB, Z_DECK + ROOF_SLAB + 0.32,
          mats["Toy_steel"])

    # ---------------------------------------------------------- night state
    # A single open face inside the entry notch: at night this is what says the
    # notch is a door, and by day it is one 12%-alpha layer, not two.
    prism(
        "entry_glow",
        long_rect(0.20, SP_ENTRY_D - 0.14, SP_ENTRY_T0 + 0.14, SP_ENTRY_T1 - 0.14),
        SP_ENTRY_H - 0.10,
        SP_ENTRY_H - 0.05,
        mats["Toy_trim_Glow"],
    )

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.12/2. Frames, grooves, glow shells and window fills are small and
    # numerous — a token softening or none at all is what keeps this under cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        n = obj.name
        if n.endswith(("_fill", "_glow")) or "_groove_" in n or "_frame_" in n:
            continue
        if n.startswith(("skylight", "entry_head", "entry_step", "roof_mech")):
            bevel(obj, width=0.04, segments=1)
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
    print(f"[build] design (parcel area-centroid) anchor: {DESIGN_ANCHOR}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] street elevation faces: {FRONT.heading:.2f} deg true")
    print(f"[build] rear faces: {REAR.heading:.2f} deg; SW flank {FLANK_SW.heading:.2f}; NE flank {FLANK_NE.heading:.2f}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "26-south-park.blend")
    glb = os.path.join(out, "26-south-park.glb")
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
