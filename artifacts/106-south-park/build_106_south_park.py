"""Deterministic Blender build of the SF-SIM miniature 104-106 South Park
(the Gran Oriente Filipino Hotel).

    blender -b --python build_106_south_park.py -- [--out DIR]

Writes 106-south-park.blend and 106-south-park.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, cornice crest exactly
11.58 m.

Design (see REFERENCE.md for the sources behind every number):

* a 1907 three-storey-over-basement wood-frame rooming house by W. L. Schmolle,
  on the north-west rim of the South Park oval, occupying the whole of a
  24 ft x 97.5 ft lot — 7.32 m of frontage against 29.72 m of depth;
* the recognition rests on the PROPORTION and on the STEPPED SILHOUETTE: the
  neighbour on the south-west (108-110 South Park) is 3.2 m shorter and the one
  on the north-east (102 South Park) is 1.9 m taller, so this building stands as
  a single tooth proud of one side of the row, with a band of its south-west
  party wall exposed and clad in horizontal wood boards;
* the street elevation is a regular THREE-BAY grid of six windows over a
  two-part ground floor: a recessed entry vestibule at the south-west end and a
  run of shopfront glass to the north-east of it, separated from the upper
  storeys by the dark sign band that carries the metal "GRAN ORIENTE FILIPINO"
  lettering — the one thing on the building that says what it is;
* the ornament is GONE. The painted trompe-l'oeil pediment lintels and the
  painted Corinthian columns that the 2019 National Register nomination and
  every pre-2021 photograph record were removed in the 2020-21 Mission Housing
  rehabilitation, along with the entrance gates. Only the lettering was kept.
  This model is the 2026 building, not the nominated one;
* the roof is flat at 11.02 m with the cornice lifting the street end to
  11.58 m, and it is NOT empty: Bing/Maxar aerial imagery masked to this
  footprint shows a long photovoltaic array over the north-east half of the
  rear two thirds, a run of raised skylights along the south-west edge (the
  nomination's three large rectangular skylights, installed 1927), and a
  cluster of mechanical plant at the street end;
* night state: four of the six upper street windows lit, unevenly — this is 24
  studios of affordable housing on a quiet residential oval, and an evenly lit
  grid would read institutional — plus a thin warm spill in the entry recess.
  Glow surfaces are thin shells proud of the opaque glazing: the app renders
  _Glow in a separate layer that is ~12% alpha by day, so a primary surface must
  never be authored as glow.

Authoring frame: the footprint is a clean rectangle at 45 deg to the world axes,
so everything is placed through two local frames built from it — a FRONT frame
(t along the 7.32 m street frontage, d outward at 135 deg) and a LONG frame
(s from the street edge toward Taber Place, u across from the south-west party
wall). Because the building sits at 45 deg, the axis-aligned XY bounding box is
~26.4 x 26.4 m even though the building is 7.32 x 29.72 m. That is expected, not
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

# Area centroid of the DataSF LiDAR footprint SF3775058 — the manifest anchor
# before recentring, and (unusually for this oval) also a workable centre for
# the bake-time exclusion circle. See the plan's 2.3 and 2.13.
DESIGN_ANCHOR = (-122.3944106, 37.7817227)

# Lot, from the National Register nomination: 24 ft x 97.5 ft, fully occupied.
# The DataSF LiDAR footprint (30.02 x 7.02 m) and OSM way/124884343
# (29.80 x 7.29 m) both agree with it to ~0.2 m per side.
FRONTAGE = 7.32
DEPTH = 29.72
AXIS_BEARING = 315.0      # street -> rear (north-west)
FRONT_BEARING = 135.0     # the street elevation faces south-east, onto the oval

Z_DECK = 11.02            # flat roof deck — MEASURED (DataSF LiDAR height median
                          # over 824 cells, sd 0.67 m; for a flat roof the median
                          # is the deck). OSM height=11 agrees with it.
Z_CREST = 11.58           # cornice crest = 38 ft, PUBLISHED in the NR nomination.
                          # The bbox top and the manifest targetHeightM, so the
                          # loader's scale is exactly 1.0. The LiDAR maximum of
                          # 13.50 m is the taller neighbour bleeding across the
                          # party wall, not a penthouse — see REPORT.md.

Z_SHOP = 3.30             # top of the ground-floor stucco band
Z_SIGN0, Z_SIGN1 = 3.30, 3.90   # the "GRAN ORIENTE FILIPINO" sign band
Z_SILL2, Z_SILL3 = 4.75, 8.20   # second- and third-storey window sills
Z_FLANK = 7.80            # 108-110 South Park's roof (LiDAR median 7.76 m):
                          # everything above this on the south-west party wall
                          # is exposed and boarded

SHOP_PROUD = 0.05
SIGN_PROUD = 0.07
CORNICE_PROUD = 0.22
DENTIL_Z0, DENTIL_Z1 = 10.78, 10.90
PARAPET_H, PARAPET_W = 0.18, 0.20

WIN_W, WIN_H = 0.95, 1.85
WIN_RECESS = 0.12
BAY_T = (1.83, 3.66, 5.49)      # three bays across a 7.32 m frontage

VEST_T0, VEST_T1 = 0.30, 1.85   # entry vestibule, SOUTH-WEST end of the frontage
VEST_H, VEST_D = 2.85, 1.10
SHOPFRONT_T0, SHOPFRONT_T1 = 2.30, 6.95
SHOPFRONT_Z0, SHOPFRONT_Z1 = 1.05, 3.10

REAR_CLAD = 0.04                # asbestos-shingle cladding depth on the rear
REAR_DOOR_W, REAR_DOOR_H = 1.40, 2.30
FE_Z = (3.95, 7.50)             # fire-escape platforms, second and third floors
# The REAR face frame runs t = 0 at the NORTH-EAST party wall to t = 7.32 at the
# south-west one, so the nomination's "two eastern bays" are the first two.
FE_T0, FE_T1 = 1.45, 4.05

BEVEL_W, BEVEL_SEG = 0.10, 2

PALETTE_HEX = {
    "Toy_cream": "f2ede3",   # the upper two storeys' painted stucco, and the
                             # roof parapet. The 2020-21 repaint reads as a pale
                             # warm off-white against a distinctly darker ground
                             # floor; the VALUE relation is confident, the hue is
                             # read from shaded photography — see REPORT.md.
    "Toy_steel": "9aa0a6",   # ground-floor stucco band, shopfront bulkhead,
                             # rooftop mechanical plant
    "Toy_ink": "3a3530",     # sign band, vestibule recess and door, rear service
                             # entrance, fire escape, photovoltaic array
    "Toy_trim": "f3efe6",    # cornice, dentil course, window trim and sills,
                             # shopfront mullions, skylight kerbs, sign inset
    "Toy_glass": "2a4d73",   # all windows, the shopfront band, the skylight tops
    "Toy_sand": "ece4d4",    # the exposed south-west flank boarding. The plan
                             # called for Toy_rust here, as the building's one
                             # warm accent. REVERSED after the first aerial
                             # review: a saturated 29.7 m band read as a painted
                             # racing stripe and dominated the whole model, and
                             # it is also almost certainly wrong — the 2020-21
                             # repaint covered this strip along with everything
                             # else, and the January 2025 Street View pano shows
                             # pale wall above 108-110's roof, no brown. The
                             # stepped silhouette does not need a stripe: in the
                             # baked city the shorter neighbour supplies the step
                             # for free. See REPORT.md.
    "Toy_stone": "d9d2c2",   # the flat roof deck. The 2020-21 rehabilitation left
                             # a pale cool-roof membrane, which is what the aerial
                             # imagery shows and is what makes the dark array and
                             # the skylights read from the app's camera.
    "Toy_roofd": "45454a",   # the Taber Place rear face (asbestos shingle in an
                             # alley — the plainest, darkest surface here)
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

# Footprint corners, metres east/north from DESIGN_ANCHOR, wound CCW.
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
        # Resolve the outward sense against the centroid rather than trusting
        # the winding order.
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
REAR = Face(REAR_NE, REAR_SW)        # Taber Place, faces 315 deg
FLANK_SW = Face(REAR_SW, STREET_SW)  # toward 108-110, faces 225 deg


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
    a third of the object's thinnest dimension: window fills, sills and glow
    shells are only 40-120 mm thick and a full bevel on those collapses opposing
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
    """Closed band solid between `poly` and its offset — a parapet or a proud
    string course."""
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


def edge_return(name, a, b, length, thickness, z0, z1, mat):
    """A short proud band running from corner `a` along the edge a->b: the
    cornice die at each front corner, so the cornice does not stop dead."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    m = math.hypot(dx, dy)
    d = (dx / m, dy / m)
    nrm = (-d[1], d[0])
    if (a[0] + nrm[0] - CX) ** 2 + (a[1] + nrm[1] - CY) ** 2 < (a[0] - CX) ** 2 + (
        a[1] - CY
    ) ** 2:
        nrm = (-nrm[0], -nrm[1])
    p1 = (a[0] + d[0] * length, a[1] + d[1] * length)
    poly = [
        a,
        p1,
        (p1[0] + nrm[0] * thickness, p1[1] + nrm[1] * thickness),
        (a[0] + nrm[0] * thickness, a[1] + nrm[1] * thickness),
    ]
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


def window(name, face, t_centre, z_sill, mats, lit=False, wall_d=0.0):
    """A recessed opening with a proud sill and trim — the same module on the
    street elevation and on the Taber Place rear, which is what the nomination
    describes (six windows each, three bays, one per bay per storey).

    `wall_d` is the outer face of whatever cladding this elevation carries; the
    glass has to poke a little past it or it is buried inside the cladding slab
    and the elevation renders as six sills and no windows."""
    t0, t1 = t_centre - WIN_W / 2.0, t_centre + WIN_W / 2.0
    prism(
        f"{name}_fill",
        face.rect(t0, t1, -WIN_RECESS, wall_d + 0.02),
        z_sill,
        z_sill + WIN_H,
        mats["Toy_glass"],
    )
    prism(
        f"{name}_sill",
        face.rect(t0 - 0.10, t1 + 0.10, wall_d, wall_d + 0.10),
        z_sill - 0.12,
        z_sill,
        mats["Toy_trim"],
    )
    if lit:
        prism(
            f"{name}_glow",
            face.rect(t0 + 0.05, t1 - 0.05, wall_d + 0.02, wall_d + 0.06),
            z_sill + 0.06,
            z_sill + WIN_H - 0.06,
            mats["Toy_glassl_Glow"],
        )


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    mats = {name: make_material(name) for name in PALETTE_HEX}

    # ------------------------------------------------------------ main volume
    # Three storeys of painted stucco on the surveyed lot. The north-east party
    # wall is never seen (102 South Park is 1.9 m taller and abuts it), so
    # everything below is applied to the other three faces and the roof.
    prism("body", FOOTPRINT, 0.0, Z_DECK, mats["Toy_cream"], mat_top=mats["Toy_stone"])

    # ------------------------------------------------- rear (Taber Place) face
    # Asbestos shingle over the original wood channel rustic siding: a plainer,
    # darker face than the street front, carried by value alone.
    prism(
        "rear_cladding",
        REAR.rect(0.0, REAR.length, 0.0, REAR_CLAD),
        0.0,
        Z_DECK,
        mats["Toy_roofd"],
    )

    # ------------------------------------- south-west flank above the neighbour
    # 108-110 South Park's roof sits at 7.76 m against this building's 11.02 m,
    # so the top ~3.2 m of this party wall is exposed. The nomination records it
    # as horizontal wood boards. This strip is one of only two things that stop
    # the building reading as a plain bar from the app's camera.
    prism(
        "flank_boarding",
        FLANK_SW.rect(0.0, FLANK_SW.length, 0.0, 0.05),
        Z_FLANK,
        Z_DECK,
        mats["Toy_sand"],
    )
    # Three shallow shadow grooves are what now says "horizontal boards, not
    # stucco" — with the field in Toy_sand rather than Toy_rust the strip needs
    # some texture to be distinguishable from the body at all.
    for k in range(3):
        z = Z_FLANK + (Z_DECK - Z_FLANK) * (k + 1) / 4.0
        prism(
            f"flank_groove_{k}",
            FLANK_SW.rect(0.20, FLANK_SW.length - 0.20, 0.05, 0.065),
            z - 0.025,
            z + 0.025,
            mats["Toy_steel"],
        )

    # -------------------------------------------------- ground-floor band
    # A darker stucco band under the sign course, proud of the upper storeys.
    # It wraps the street front and returns a little way down both flanks so it
    # does not stop dead at the party lines.
    for name, (t0, t1) in (
        ("shop_pier_sw", (-0.05, VEST_T0 - 0.06)),
        ("shop_pier_mid", (VEST_T1 + 0.06, SHOPFRONT_T0)),
        ("shop_pier_ne", (SHOPFRONT_T1, FRONT.length + 0.05)),
    ):
        prism(name, FRONT.rect(t0, t1, 0.0, SHOP_PROUD), 0.0, Z_SHOP, mats["Toy_steel"])
    # The plywood bulkhead under the shopfront glass, and the wall above it up to
    # the sign band.
    prism(
        "shop_bulkhead",
        FRONT.rect(SHOPFRONT_T0, SHOPFRONT_T1, 0.0, SHOP_PROUD),
        0.0,
        SHOPFRONT_Z0,
        mats["Toy_steel"],
    )
    prism(
        "shop_lintel",
        FRONT.rect(SHOPFRONT_T0, SHOPFRONT_T1, 0.0, SHOP_PROUD),
        SHOPFRONT_Z1,
        Z_SHOP,
        mats["Toy_steel"],
    )
    # ...and the head of the vestibule opening, which is 2.85 m against the
    # band's 3.30 m.
    prism(
        "vestibule_lintel",
        FRONT.rect(VEST_T0 - 0.06, VEST_T1 + 0.06, 0.0, SHOP_PROUD),
        VEST_H + 0.14,
        Z_SHOP,
        mats["Toy_steel"],
    )

    # ------------------------------------------------------------- sign band
    # "GRAN ORIENTE FILIPINO" in applied metal letters, kept through the
    # 2020-21 rehabilitation when everything else on the facade was removed.
    # The glyphs are sub-pixel at city scale: a light inset strip inside a dark
    # band is what carries them.
    prism(
        "sign_band",
        FRONT.rect(-0.05, FRONT.length + 0.05, 0.0, SIGN_PROUD),
        Z_SIGN0,
        Z_SIGN1,
        mats["Toy_ink"],
    )
    prism(
        "sign_letters",
        FRONT.rect(0.55, 5.75, SIGN_PROUD, SIGN_PROUD + 0.03),
        Z_SIGN0 + 0.19,
        Z_SIGN0 + 0.42,
        mats["Toy_trim"],
    )

    # --------------------------------------------------------------- vestibule
    # Recessed entry at the SOUTH-WEST end of the frontage, with the shopfront
    # to the north-east of it. Getting this handedness backwards mirrors the
    # building; the nomination is explicit ("a vestibule at the west end ...
    # three wood sash storefront windows ... are located to the east").
    prism(
        "vestibule_recess",
        FRONT.rect(VEST_T0 - 0.06, VEST_T1 + 0.06, -VEST_D, 0.01),
        0.0,
        VEST_H + 0.14,
        mats["Toy_ink"],
    )
    prism(
        "vestibule_door",
        FRONT.rect(VEST_T0 + 0.30, VEST_T1 - 0.30, -VEST_D, -VEST_D + 0.10),
        0.0,
        2.15,
        mats["Toy_steel"],
    )
    # Supporting night accent: a soffit light just inside the head of the
    # opening. The first build put the glow shell on the BACK wall of the
    # 1.1 m recess, where the reveals hid it completely from every angle the
    # app's camera can reach and the accent rendered as nothing at all — the
    # same failure 165 South Park logged with its gate. A band under the lintel
    # is both visible from a three-quarter aerial and true to how these entries
    # are actually lit.
    prism(
        "vestibule_glow",
        FRONT.rect(VEST_T0 + 0.10, VEST_T1 - 0.10, -0.32, -0.14),
        VEST_H - 0.20,
        VEST_H - 0.06,
        mats["Toy_trim_Glow"],
    )

    # -------------------------------------------------------------- shopfront
    # Three wood-sash storefront windows over a solid bulkhead, simplified to
    # one recessed glazed band split by two mullions.
    prism(
        "shopfront_glass",
        FRONT.rect(SHOPFRONT_T0, SHOPFRONT_T1, -0.12, 0.02),
        SHOPFRONT_Z0,
        SHOPFRONT_Z1,
        mats["Toy_glass"],
    )
    for k in range(2):
        mt = SHOPFRONT_T0 + (SHOPFRONT_T1 - SHOPFRONT_T0) * (k + 1) / 3.0
        prism(
            f"shopfront_mullion_{k}",
            FRONT.rect(mt - 0.06, mt + 0.06, -0.12, 0.035),
            SHOPFRONT_Z0,
            SHOPFRONT_Z1,
            mats["Toy_trim"],
        )
    prism(
        "shopfront_head",
        FRONT.rect(SHOPFRONT_T0 - 0.08, SHOPFRONT_T1 + 0.08, SHOP_PROUD, SHOP_PROUD + 0.07),
        SHOPFRONT_Z1,
        SHOPFRONT_Z1 + 0.14,
        mats["Toy_trim"],
    )

    # ---------------------------------------------------------- street windows
    # Six openings in a regular three-bay grid — the facade, now that the
    # painted order is gone. Lit unevenly at night: two on the second storey,
    # two on the third.
    lit_map = {(2, 0): True, (2, 2): True, (3, 0): True, (3, 1): True}
    for i, t in enumerate(BAY_T):
        window(f"win_s2_{i}", FRONT, t, Z_SILL2, mats, lit=lit_map.get((2, i), False))
        window(f"win_s3_{i}", FRONT, t, Z_SILL3, mats, lit=lit_map.get((3, i), False))

    # ------------------------------------------------------------ rear windows
    # Six more on the same module, plus the central inset service entrance to
    # the rear kitchen. The rear is seen from above and obliquely only, so it
    # gets the geometry and none of the trim refinement.
    for i, t in enumerate(BAY_T):
        window(f"win_r2_{i}", REAR, t, Z_SILL2, mats, wall_d=REAR_CLAD)
        window(f"win_r3_{i}", REAR, t, Z_SILL3, mats, wall_d=REAR_CLAD)
    rc = REAR.length / 2.0
    prism(
        "rear_service_door",
        REAR.rect(rc - REAR_DOOR_W / 2.0, rc + REAR_DOOR_W / 2.0, -0.18, REAR_CLAD + 0.02),
        0.0,
        REAR_DOOR_H,
        mats["Toy_ink"],
    )

    # ------------------------------------------------------------ fire escape
    # Serving the two north-east bays at the second and third floors. Flat
    # platforms and two posts: a modelled truss would spend a fifth of the
    # triangle budget on something 6 px tall in the app.
    for k, z in enumerate(FE_Z):
        prism(
            f"fire_escape_{k}",
            REAR.rect(FE_T0, FE_T1, REAR_CLAD, 0.90),
            z,
            z + 0.13,
            mats["Toy_ink"],
        )
    for k, t in enumerate((FE_T0 + 0.10, FE_T1 - 0.10)):
        prism(
            f"fire_escape_post_{k}",
            REAR.rect(t - 0.06, t + 0.06, 0.76, 0.88),
            FE_Z[0],
            FE_Z[1] + 1.05,
            mats["Toy_ink"],
        )

    # ---------------------------------------------------------------- parapet
    # A low lip around the whole roof in the body colour. The roof is the
    # surface the app's camera actually sees, and without it the deck reads as a
    # bare cut face rather than a designed top.
    rim("parapet", FOOTPRINT, PARAPET_W, Z_DECK, Z_DECK + PARAPET_H, mats["Toy_cream"])

    # ---------------------------------------------------------------- cornice
    # The only lift in the silhouette, and the geometry that sets the 11.58 m
    # crest. It must land on it exactly.
    prism(
        "cornice",
        FRONT.rect(-0.06, FRONT.length + 0.06, 0.0, CORNICE_PROUD),
        Z_DECK,
        Z_CREST,
        mats["Toy_trim"],
    )
    edge_return("cornice_die_sw", STREET_SW, REAR_SW, 0.35, CORNICE_PROUD,
                Z_DECK, Z_CREST, mats["Toy_trim"])
    edge_return("cornice_die_ne", STREET_NE, REAR_NE, 0.35, CORNICE_PROUD,
                Z_DECK, Z_CREST, mats["Toy_trim"])
    # The nomination's "simple cornice adorned with painted dentils": one
    # proud course under the cornice is all the dentils get at this scale.
    prism(
        "dentil_course",
        FRONT.rect(-0.02, FRONT.length + 0.02, 0.0, 0.11),
        DENTIL_Z0,
        DENTIL_Z1,
        mats["Toy_trim"],
    )

    # ------------------------------------------------------------------- roof
    # Read from Bing/Maxar aerial imagery masked to this footprint (see
    # REFERENCE.md): a photovoltaic array over the north-east half of the rear
    # two thirds, the run of raised skylights along the south-west edge that the
    # nomination records (three large rectangular ones, installed 1927), and a
    # cluster of mechanical plant at the street end.
    for k, (s0, s1) in enumerate(((7.0, 13.2), (13.8, 20.0), (20.6, 26.8))):
        prism(
            f"pv_{k}",
            long_rect(s0, s1, 3.60, 6.60),
            Z_DECK + 0.16,
            Z_DECK + 0.30,
            mats["Toy_ink"],
        )
        for j in (1, 2):
            sc = s0 + (s1 - s0) * j / 3.0
            prism(
                f"pv_{k}_rail_{j}",
                long_rect(sc - 0.04, sc + 0.04, 3.60, 6.60),
                Z_DECK + 0.30,
                Z_DECK + 0.31,
                mats["Toy_steel"],
            )
    for k, sc in enumerate((11.0, 15.5, 20.0)):
        prism(
            f"skylight_{k}",
            long_rect(sc - 1.05, sc + 1.05, 0.95, 2.05),
            Z_DECK,
            Z_DECK + 0.32,
            mats["Toy_trim"],
            mat_top=mats["Toy_glass"],
        )
    # Plant height is capped at 0.50 m so the cornice crest stays the tallest
    # geometry and the loader's targetHeightM / measuredHeight lands on 1.0.
    # Nothing on this roof is documented above the cornice: the LiDAR maximum
    # that would suggest otherwise is the taller neighbour bleeding across the
    # party wall (see REPORT.md), so capping is the conservative reading, not a
    # convenience.
    prism("roof_mech", long_rect(2.20, 3.90, 2.60, 4.40), Z_DECK, Z_DECK + 0.50,
          mats["Toy_steel"])
    prism("roof_mech_small", long_rect(4.30, 5.05, 4.75, 5.50), Z_DECK, Z_DECK + 0.32,
          mats["Toy_steel"])

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.10/2. Window fills, sills, glow shells, mullions and grooves are small
    # and numerous — a token softening or none at all is what keeps this under
    # cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        n = obj.name
        if n.endswith(("_fill", "_glow")) or "_rail_" in n or "_mullion_" in n or "_groove_" in n:
            continue
        if n.endswith("_sill") or n.startswith(("dentil", "sign_letters", "fire_escape")):
            bevel(obj, width=0.03, segments=1)
        else:
            bevel(obj)

    recentre()
    return scene


# Metres east / north from DESIGN_ANCHOR to the model's XY bbox centre, filled
# in by recentre(). The manifest anchor is DESIGN_ANCHOR moved by this vector,
# so the origin sits at the bbox centre (contract rule 2) while the building
# still lands on its real footprint.
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
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "106-south-park.blend")
    glb = os.path.join(out, "106-south-park.glb")
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
