"""Deterministic Blender build of the SF-SIM miniature 41-43 South Park.

    blender -b --python build_41_south_park.py -- [--out DIR]

Writes 41-south-park.blend and 41-south-park.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, cornice crest exactly
10.60 m.

Design (see REFERENCE.md and docs/asset-plans/41-south-park.md for the sources
behind every number):

* a 1911 Edwardian two-flat on the NORTH-EAST rim of the South Park oval,
  7.297 m of frontage against 24.0 m of depth, gutted and rebuilt behind its
  retained facade in 2012-13;
* the recognition rests on the ASYMMETRIC PAIR OF BAYS. The south-west bay (the
  garage side) is TWO storeys; the north-east bay (the entry side) is ONE, at
  the top only, because the two-storey arched entry recess occupies the level
  below it. Two matching full-height bays would be the wrong house;
* the north-east top-storey bay is OXBLOOD; every other surface is charcoal.
  That accent is the single strongest cue and the only saturated colour for
  fifty metres along this rim;
* the arched entry must read as a HOLE. It is built as a real 0.80 m notch in
  the ground-storey footprint with a stepped-free arch spandrel across its
  mouth, not as a painted arch on a flat wall;
* the roof is flat and PALE, at 9.83 m, with the cornice lifting to 10.60 m at
  the street end only, and carrying a timber terrace with a round spa — the one
  incident the app's downward-looking camera actually sees;
* night state: the four top-storey bay windows lit (hero), the spa glowing on
  the roof, and a warm spill in the entry recess. Glow surfaces are single thin
  panels proud of an opaque parent — a CLOSED glow shell is two alpha layers and
  reads ~23% by day instead of ~12%, tinting the facade it sits on.

Authoring frame: the lot is a true parallelogram, so one local frame describes
it. `t` runs along the frontage from the SOUTH-WEST party wall (t = 0, the
45-49 South Park side, where the garage is) to the NORTH-EAST one
(t = 7.297, the 35 South Park side, where the stoop and the oxblood bay are);
`d` runs outward toward the park (bearing 315.08 deg); `u` runs into the lot
(bearing 135.08 deg, u = -d). The building sits 135 deg off the world axes, so
the axis-aligned XY bounding box is ~23 x 23 m even though the building is
7.3 x 25.2 m. That is expected, not a scale error.

No booleans anywhere: openings are built either as real notches in the plan
polygon or as the layered-relief stack that artifacts/132-south-park and
artifacts/181-south-park established (surround -> reveal -> glass, each inner
layer protruding further so the value gradient reads as depth).
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

# Area centroid of the design footprint = the MANIFEST anchor before recentring.
# Derived in docs/asset-plans/41-south-park.md 2.3 from the surveyed DataSF
# parcel 3775040 truncated at the LiDAR footprint's rear extent (24.0 m).
DESIGN_ANCHOR = (-122.3934770, 37.7815017)

# Design footprint, metres east/north from DESIGN_ANCHOR. The surveyed lot is a
# parallelogram: 7.297 m frontage on the oval's curve, 135.08 deg into the
# block, truncated at 24.0 m of built depth (2.3).
FRONT_SW = (-11.064, 5.926)
FRONT_NE = (-5.884, 11.066)
REAR_NE = (11.064, -5.926)
REAR_SW = (5.884, -11.066)
FOOTPRINT = [FRONT_SW, FRONT_NE, REAR_NE, REAR_SW]

FRONTAGE = 7.297
DEPTH = 24.0

# ---- vertical stack (all measured or derived in the plan's 2.4) ------------
Z_GARAGE_HEAD = 2.05    # measured off the Compass photograph
Z_BAY_SW0 = 2.30        # south-west bay springs
Z_BELT = 5.60           # storey line, 2nd -> 3rd
Z_BAY_NE0 = 5.60        # oxblood bay's underside
Z_BAY_TOP = 9.10        # both bays' cornices tuck under the main one here
Z_DECK = 9.83           # flat roof deck — MEASURED (DataSF LiDAR height median
                        # over 672 cells at 50 cm, sd 1.08 m; for a flat roof
                        # the median is the deck)
Z_PARAPET = 10.10
Z_CREST = 10.60         # front cornice crest — the bbox top, and the manifest
                        # targetHeightM, so the loader's scale is exactly 1.0.
                        # ESTIMATED, photogrammetric: 417 px of a 288 px =
                        # 7.297 m facade scale on the Compass listing photo,
                        # cross-checked against the garage door (3.30 x 2.00 m).
                        # The LiDAR maximum is 11.88 m, is unexplained and
                        # predates the 2012-13 rebuild; see REPORT.md.

# ---- frontage layout, t from the SOUTH-WEST party wall ---------------------
BAY_PROJ = 0.95         # bays project over the property line, as SF bays do —
                        # this is what most of the raster footprints' streetward
                        # overshoot actually is (plan 2.3)
BAY_CANT = 0.65         # plan inset of each canted return

BAY_SW_T = (0.20, 3.15)
BAY_NE_T = (4.15, 7.10)

GARAGE_T = (0.25, 3.35)
ARCH_T = (4.20, 6.80)
ARCH_DEPTH = 0.80       # the entry recess is a REAL notch in the plan
ARCH_SPRING = 3.85
ARCH_CROWN = ARCH_SPRING + (ARCH_T[1] - ARCH_T[0]) / 2.0   # 5.15 m
ARCH_PLATE = 0.25       # the spandrel's thickness at the mouth of the notch
# The body is built as two closed solids because the ground storey carries the
# entry notch. The split is put ON the storey line rather than on the arch
# crown: at the crown (5.15 m) the seam rendered as a second horizontal line
# 0.45 m under the bay's belt course, and on a blank party flank two parallel
# lines that close together read as a modelling error. See REPORT.md.
Z_SPLIT = Z_BELT

STOOP_T = (4.60, 6.40)
STOOP_RISERS = 5
STOOP_RISE = 0.29
STOOP_TREAD = 0.24
Z_LANDING = STOOP_RISERS * STOOP_RISE   # 1.45 m

# ---- cornice ---------------------------------------------------------------
# Three stacked bands following the front profile INCLUDING the bay projections,
# so the crown returns over each bay exactly as the photograph shows.
CORN_Z = (9.10, 9.45, 9.71, Z_CREST)
CORN_PROUD = (0.30, 0.38, 0.45)

# ---- roof furniture --------------------------------------------------------
# The terrace sits in the FRONT half of the roof: three sources describe it as
# "overlooking South Park", and the nadir imagery reads it 12-16 m back with a
# 2-3 m registration error on this block. Mid-roof (the first build) satisfied
# the imagery and contradicted the text, and left 12 m of blank membrane at the
# street end where the camera looks first.
TERRACE_T = (1.55, 5.75)
TERRACE_U = (9.6, 13.4)
TERRACE_GUARD = 0.45    # 0.60 put the guard's top at 10.63 and stole the
                        # bounding-box maximum from the cornice crest, which is
                        # the one number the loader's scale depends on
Z_TERRACE = Z_DECK + 0.20
SPA_R = 1.00
SPA_RIM = 0.16
SPA_SEG = 14
Z_SPA = Z_TERRACE + 0.44
SPA_CENTRE = (4.55, 11.5)
# "Huge rollaway skylights" (One Kindesign). The first build's 1.2 x 0.9 curbs
# read as two blue chips on an otherwise empty 24 m slab.
SKYLIGHT_T = (2.45, 4.45)
SKYLIGHT_U = (5.0, 18.6)
SKYLIGHT_D = 1.40
# Roof access. INFERRED, and inferred from function rather than from a source:
# a roof terrace has to be reachable, and a hatch or low stair bulkhead is the
# only thing on this roof that could also explain the unexplained 11.88 m LiDAR
# maximum. Kept well under Z_CREST — see REPORT.md.
HATCH_T = (2.20, 3.70)
HATCH_U = (15.0, 16.3)
Z_HATCH = Z_DECK + 0.55

BEVEL_W, BEVEL_SEG = 0.10, 2

# Every interface where one solid stacks on another is overlapped by this much
# rather than butted. Butted solids leave a coincident face pair, and a ray that
# grazes one picks the wrong side: the first build's visibility residual was
# 0.162% (51 of 31,500 rays) with every per-object signed volume still positive.
# Burying each interface removes the ambiguity instead of arguing with it.
LAP = 0.03

# Layered-relief depths (132-south-park's device): d offsets run along the
# host face's OUTWARD normal, so each inner layer must protrude past the one
# around it to be seen at all.
D_SURROUND = 0.05
D_REVEAL = 0.08
D_GLASS = 0.12
D_GLOW = (0.11, 0.15)
TRIM = 0.13

PALETTE_HEX = {
    "Toy_roofd": "45454a",   # the whole charcoal body — walls, SW bay, cornice,
                             # parapet, arch spandrel. The darkest neutral in the
                             # palette and the building's identity.
    "Toy_red": "6e3947",     # THE OXBLOOD BAY, and nothing else. OFF-PALETTE and
                             # deliberate: the real colour is a deep plum around
                             # #6e3947 and no palette entry is close (Toy_rust
                             # a86444 is far too orange, Toy_red c4453c far too
                             # bright). The style bible's SF exception — painted
                             # residential rows keep their tinted facades —
                             # sanctions it, and this accent IS recognition cue
                             # #2. A WARN, not a FAIL. The material keeps a
                             # palette NAME so the contract check and the
                             # loader's merge path are unaffected; the same
                             # device 165-south-park used for its siding.
    "Toy_steel": "9aa0a6",   # sashes, trim, bay aprons, the dentil course, the
                             # spa shell. Every moulding on this building is pale
                             # on purpose: a 10 m volume in 45454a with no value
                             # breaks reads as a hole in the city, not a house.
    "Toy_glass": "2a4d73",
    "Toy_ink": "3a3530",     # garage leaf, entry recess lining, stoop, skylights
    "Toy_stone": "d9d2c2",   # the flat pale roof membrane — the value contrast
                             # against the charcoal walls is the single most
                             # useful thing about this asset from above
    "Toy_rust": "a86444",    # the roof terrace decking
    "Toy_glassl": "6f95b8",  # the spa water
    "Toy_glass_Glow": "6f95b8",   # the four lit top-storey bay windows — HERO
    "Toy_glassl_Glow": "6f95b8",  # the lit spa
    "Toy_gold_Glow": "caa64a",    # warm spill in the entry recess
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


# ----------------------------------------------------------------- transforms


def _unit(dx, dy):
    n = math.hypot(dx, dy)
    return (dx / n, dy / n)


def _centroid(poly):
    cx = cy = 0.0
    s = 0.0
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        cr = x0 * y1 - x1 * y0
        s += cr
        cx += (x0 + x1) * cr
        cy += (y0 + y1) * cr
    return (cx / (3 * s), cy / (3 * s), abs(s) / 2.0)


CX, CY, FOOT_AREA = _centroid(FOOTPRINT)

# Front frame: t runs along the frontage south-west -> north-east, d runs
# outward (away from the lot, toward the park). The outward sense is resolved
# against the footprint centroid rather than assumed from the winding order.
_FT = _unit(FRONT_NE[0] - FRONT_SW[0], FRONT_NE[1] - FRONT_SW[1])
_FN = (-_FT[1], _FT[0])
if (FRONT_SW[0] + _FN[0] - CX) ** 2 + (FRONT_SW[1] + _FN[1] - CY) ** 2 < (
    FRONT_SW[0] - CX
) ** 2 + (FRONT_SW[1] - CY) ** 2:
    _FN = (-_FN[0], -_FN[1])

FRONT_LEN = math.hypot(FRONT_NE[0] - FRONT_SW[0], FRONT_NE[1] - FRONT_SW[1])
FRONT_HEADING = (math.degrees(math.atan2(_FN[0], _FN[1])) + 360.0) % 360.0


def front_xy(t, d):
    """Front frame (t along the frontage, d outward) -> world (x east, y north)."""
    return (
        FRONT_SW[0] + _FT[0] * t + _FN[0] * d,
        FRONT_SW[1] + _FT[1] * t + _FN[1] * d,
    )


def plan_xy(t, u):
    """Roof-plan frame (t along the frontage, u into the lot) -> world XY."""
    return front_xy(t, -u)


def front_rect(t0, t1, d0, d1):
    """Rectangle in the front frame, expressed in world XY."""
    return [front_xy(t0, d0), front_xy(t1, d0), front_xy(t1, d1), front_xy(t0, d1)]


def plan_rect(t0, t1, u0, u1):
    return [plan_xy(t0, u0), plan_xy(t1, u0), plan_xy(t1, u1), plan_xy(t0, u1)]


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
    a third of the object's thinnest dimension: trim layers and glow shells are
    only 30-120 mm thick and a full bevel on those collapses opposing profiles
    into zero-area slivers even with clamp_overlap."""
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


def wall_prism(name, pts_tz, d0, d1, mat):
    """Extrude a polygon authored in the front frame's vertical (t, z) plane
    along d. This is how the arch spandrel is built: a rectangle with an
    arch-shaped bite out of its bottom edge is a simple polygon, so it needs no
    boolean."""
    n = len(pts_tz)
    verts = [front_xy(t, d0) + (z,) for t, z in pts_tz]
    verts += [front_xy(t, d1) + (z,) for t, z in pts_tz]
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    return new_mesh(name, verts, faces, [mat])


def inset_polygon(poly, dist, centre=None):
    """Offset every edge of a simple polygon inward by `dist` and re-intersect
    adjacent edges. Used for the roof parapet's inner ring.

    `centre` resolves which side is "inward". It defaults to the FOOTPRINT
    centroid, which is right for the parapet and wrong for anything that is not
    concentric with the building: the spa ring sits 5 m off that centroid, and
    with the default the near half of the ring inset outward, producing a
    self-intersecting annulus that accounted for every remaining flipped ray in
    the visibility test."""
    cx, cy = (CX, CY) if centre is None else centre
    n = len(poly)
    lines = []
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        d = _unit(b[0] - a[0], b[1] - a[1])
        nrm = (-d[1], d[0])
        if (a[0] + nrm[0] - cx) ** 2 + (a[1] + nrm[1] - cy) ** 2 > (a[0] - cx) ** 2 + (
            a[1] - cy
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


def rim(name, poly, inset, z0, z1, mat, centre=None):
    """Closed band solid between `poly` and its inward offset — a parapet."""
    inner = inset_polygon(poly, inset, centre=centre)
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


def circle(cx, cy, r, segments=SPA_SEG):
    return [
        (cx + r * math.cos(2 * math.pi * i / segments), cy + r * math.sin(2 * math.pi * i / segments))
        for i in range(segments)
    ]


def cylinder(name, cx, cy, r, z0, z1, mat, segments=SPA_SEG, mat_top=None):
    return prism(name, circle(cx, cy, r, segments), z0, z1, mat, mat_top=mat_top)


# ------------------------------------------------------------- facet helpers


def facet_frame(a, b):
    """Unit tangent and OUTWARD normal of a wall facet running a -> b in world
    XY. Outward is resolved against the footprint centroid, never assumed."""
    tv = _unit(b[0] - a[0], b[1] - a[1])
    nv = (-tv[1], tv[0])
    mx, my = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
    if (mx + nv[0] - CX) ** 2 + (my + nv[1] - CY) ** 2 < (mx - CX) ** 2 + (my - CY) ** 2:
        nv = (-nv[0], -nv[1])
    return tv, nv, math.hypot(b[0] - a[0], b[1] - a[1])


def facet_rect(a, b, s0, s1, d0, d1):
    """Rectangle on the facet a->b, between arc-lengths s0..s1 measured from a,
    spanning outward depths d0..d1."""
    tv, nv, _ = facet_frame(a, b)
    p0 = (a[0] + tv[0] * s0, a[1] + tv[1] * s0)
    p1 = (a[0] + tv[0] * s1, a[1] + tv[1] * s1)
    return [
        (p0[0] + nv[0] * d0, p0[1] + nv[1] * d0),
        (p1[0] + nv[0] * d0, p1[1] + nv[1] * d0),
        (p1[0] + nv[0] * d1, p1[1] + nv[1] * d1),
        (p0[0] + nv[0] * d1, p0[1] + nv[1] * d1),
    ]


def facet_window(tag, a, b, s0, s1, z0, z1, mats, lit=False):
    """Layered relief on an arbitrary wall facet: a pale surround, a dark reveal
    ring inside it, glass inside that, and an optional glow panel proud of the
    glass. Three closed solids and no booleans — the device from
    artifacts/132-south-park."""
    prism(f"{tag}_surround", facet_rect(a, b, s0, s1, -LAP, D_SURROUND), z0, z1, mats["Toy_steel"])
    prism(
        f"{tag}_reveal",
        facet_rect(a, b, s0 + TRIM, s1 - TRIM, -LAP, D_REVEAL),
        z0 + TRIM,
        z1 - TRIM,
        mats["Toy_ink"],
    )
    g = 0.03
    prism(
        f"{tag}_glass",
        facet_rect(a, b, s0 + TRIM + g, s1 - TRIM - g, -LAP, D_GLASS),
        z0 + TRIM + g,
        z1 - TRIM - g,
        mats["Toy_glass"],
    )
    if lit:
        h = 0.07
        prism(
            f"{tag}_glow",
            facet_rect(a, b, s0 + TRIM + h, s1 - TRIM - h, D_GLOW[0], D_GLOW[1]),
            z0 + TRIM + h,
            z1 - TRIM - h,
            mats["Toy_glass_Glow"],
        )


# ------------------------------------------------------------------ bay plans


def bay_plan(t0, t1, proj=BAY_PROJ, cant=BAY_CANT, grow=0.0):
    """Canted (five-facet) bay in plan: wall - return - front - return - wall.
    `grow` fattens it for the apron band underneath."""
    p = proj + grow
    return [
        front_xy(t0 - grow, 0.0),
        front_xy(t0 - grow + cant, p),
        front_xy(t1 + grow - cant, p),
        front_xy(t1 + grow, 0.0),
    ]


def bay_facets(t0, t1, proj=BAY_PROJ, cant=BAY_CANT):
    """The three visible facets of a bay, as (a, b) world-XY pairs:
    south-west return, front, north-east return."""
    p0 = front_xy(t0, 0.0)
    p1 = front_xy(t0 + cant, proj)
    p2 = front_xy(t1 - cant, proj)
    p3 = front_xy(t1, 0.0)
    return [(p0, p1), (p1, p2), (p2, p3)]


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


def ground_footprint():
    """The footprint of the ground storey: the surveyed lot with a real 0.80 m
    notch cut out of the frontage for the arched entry recess. Cutting the notch
    in the PLAN rather than booleaning it out of a solid is what lets the entry
    read as a hole from every angle in the app."""
    return [
        FRONT_SW,
        front_xy(ARCH_T[0], 0.0),
        front_xy(ARCH_T[0], -ARCH_DEPTH),
        front_xy(ARCH_T[1], -ARCH_DEPTH),
        front_xy(ARCH_T[1], 0.0),
        FRONT_NE,
        REAR_NE,
        REAR_SW,
    ]


def cornice_band(name, z0, z1, proud, mat):
    """One band of the front cornice. Its outer edge follows the front profile
    INCLUDING both bay projections, so the crown returns over each bay exactly
    as the photograph shows; its inner edge is the flat wall line, which is
    buried inside the body."""
    prof = [
        (0.0, 0.0),
        (BAY_SW_T[0], 0.0),
        (BAY_SW_T[0] + BAY_CANT, BAY_PROJ),
        (BAY_SW_T[1] - BAY_CANT, BAY_PROJ),
        (BAY_SW_T[1], 0.0),
        (BAY_NE_T[0], 0.0),
        (BAY_NE_T[0] + BAY_CANT, BAY_PROJ),
        (BAY_NE_T[1] - BAY_CANT, BAY_PROJ),
        (BAY_NE_T[1], 0.0),
        (FRONTAGE, 0.0),
    ]
    poly = [front_xy(t, d + proud) for t, d in prof]
    poly += [front_xy(FRONTAGE, -0.10), front_xy(0.0, -0.10)]
    return prism(name, poly, z0, z1, mat)


def arch_spandrel(mats):
    """The arch head across the mouth of the entry notch: a rectangle with a
    semicircular bite out of its bottom edge, extruded through the outer
    ARCH_PLATE of the notch. One simple polygon, one object, no boolean."""
    t0, t1 = ARCH_T
    r = (t1 - t0) / 2.0
    tc = (t0 + t1) / 2.0
    top = Z_SPLIT                # closes the notch up to the body split
    pts = [(t0, ARCH_SPRING), (t0, top), (t1, top), (t1, ARCH_SPRING)]
    # Interior arc points only: including ang = 0 and ang = pi would repeat the
    # rectangle's two springing corners, and a polygon with duplicated
    # consecutive vertices exports degenerate slivers.
    steps = 12
    for i in range(1, steps):
        ang = math.pi * i / steps            # t1 side -> crown -> t0 side
        pts.append((tc + r * math.cos(ang), ARCH_SPRING + r * math.sin(ang)))
    wall_prism("arch_spandrel", pts, -ARCH_DEPTH + 0.02, 0.0 + ARCH_PLATE - 0.25, mats["Toy_roofd"])


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    mats = {name: make_material(name) for name in PALETTE_HEX}

    # ------------------------------------------------------------ main volume
    # Two closed solids: the ground storey carries the entry notch, everything
    # above the arch crown is the full lot section.
    prism("body_lower", ground_footprint(), 0.0, Z_SPLIT, mats["Toy_roofd"])
    prism("body_upper", FOOTPRINT, Z_SPLIT - LAP, Z_DECK, mats["Toy_roofd"], mat_top=mats["Toy_stone"])

    # ---------------------------------------------------------- entry recess
    # Ink lining on the notch's three interior faces, proud of the charcoal so
    # the recess reads as a hole and not as a shadow, plus the landing slab the
    # stoop climbs to.
    prism(
        "recess_back",
        front_rect(ARCH_T[0], ARCH_T[1], -ARCH_DEPTH - LAP, -ARCH_DEPTH + 0.05),
        0.0,
        Z_SPLIT,
        mats["Toy_ink"],
    )
    for k, t in enumerate(ARCH_T):
        s = 0.05 if k == 0 else -0.05
        prism(
            f"recess_jamb{k}",
            front_rect(t - s * (LAP / 0.05), t + s, -ARCH_DEPTH, LAP),
            0.0,
            Z_SPLIT,
            mats["Toy_ink"],
        )
    prism(
        "recess_floor",
        front_rect(ARCH_T[0], ARCH_T[1], -ARCH_DEPTH, 0.02),
        Z_LANDING - 0.10,
        Z_LANDING,
        mats["Toy_ink"],
    )
    arch_spandrel(mats)

    # Entry door at the back of the recess, and the warm night spill that tells
    # the eye the arch is a passage rather than a panel.
    prism(
        "entry_door",
        front_rect(4.95, 6.05, -ARCH_DEPTH + 0.02, -ARCH_DEPTH + 0.12),
        Z_LANDING,
        Z_LANDING + 2.40,
        mats["Toy_ink"],
    )
    prism(
        "entry_glow",
        front_rect(5.10, 5.90, -ARCH_DEPTH + 0.12, -ARCH_DEPTH + 0.16),
        Z_LANDING + 1.60,
        Z_LANDING + 2.30,
        mats["Toy_gold_Glow"],
    )

    # ------------------------------------------------------------------ stoop
    # Five risers climbing from the sidewalk into the recess. Solid cheeks, no
    # balusters — at 300-500 m a handrail is sub-pixel and costs 400 triangles.
    for i in range(STOOP_RISERS):
        d_out = (STOOP_RISERS - i) * STOOP_TREAD
        prism(
            f"stoop_step{i}",
            front_rect(STOOP_T[0], STOOP_T[1], d_out - STOOP_TREAD - LAP, d_out),
            0.0,
            (i + 1) * STOOP_RISE,
            mats["Toy_ink"],
        )

    # ------------------------------------------------------------ garage door
    # Layered relief: pale surround, ink leaf, three shallow charcoal grooves.
    fa, fb = front_xy(0.0, 0.0), front_xy(FRONTAGE, 0.0)
    prism(
        "garage_surround",
        facet_rect(fa, fb, GARAGE_T[0] - 0.10, GARAGE_T[1] + 0.10, -LAP, D_SURROUND),
        0.0,
        Z_GARAGE_HEAD + 0.12,
        mats["Toy_steel"],
    )
    prism(
        "garage_leaf",
        facet_rect(fa, fb, GARAGE_T[0], GARAGE_T[1], -LAP, D_REVEAL),
        0.0,
        Z_GARAGE_HEAD,
        mats["Toy_ink"],
    )
    for i in range(3):
        z = 0.45 + i * 0.50
        prism(
            f"garage_groove{i}",
            facet_rect(fa, fb, GARAGE_T[0] + 0.08, GARAGE_T[1] - 0.08, D_REVEAL - LAP, D_REVEAL + 0.03),
            z,
            z + 0.07,
            mats["Toy_roofd"],
        )

    # ------------------------------------------------------------- the bays
    # THE recognition cue, and they are NOT a matched pair.
    prism("bay_sw", bay_plan(*BAY_SW_T), Z_BAY_SW0, Z_BAY_TOP, mats["Toy_roofd"])
    prism("bay_ne", bay_plan(*BAY_NE_T), Z_BAY_NE0, Z_BAY_TOP, mats["Toy_red"])

    # Pale aprons under each bay: the underside is what you see from the park,
    # and a charcoal bay hanging off a charcoal wall has no edge at all.
    prism("bay_sw_apron", bay_plan(*BAY_SW_T, grow=0.06), Z_BAY_SW0 - 0.24, Z_BAY_SW0 + LAP,
          mats["Toy_steel"])
    prism("bay_ne_apron", bay_plan(*BAY_NE_T, grow=0.06), Z_BAY_NE0 - 0.24, Z_BAY_NE0 + LAP,
          mats["Toy_steel"])
    # Belt course at the storey line, on the south-west bay only — it is the only
    # bay that crosses that line.
    prism("bay_sw_belt", bay_plan(*BAY_SW_T, grow=0.05), Z_BELT - 0.10, Z_BELT + 0.10,
          mats["Toy_steel"])

    # ----------------------------------------------------------- bay windows
    # Three openings per bay storey: the wide front facet plus one on each
    # canted return. Returns are only 1.15 m of arc, so their openings are
    # narrower and their trim is thinner.
    for tag, t01, storeys in (
        ("swb_lo", BAY_SW_T, ((2.75, 5.10, False),)),
        ("swb_hi", BAY_SW_T, ((6.15, 8.60, True),)),
        ("neb_hi", BAY_NE_T, ((6.15, 8.60, True),)),
    ):
        for (za, zb, lit) in storeys:
            for fi, (a, b) in enumerate(bay_facets(*t01)):
                _, _, ln = facet_frame(a, b)
                margin = 0.22 if fi == 1 else 0.26
                if ln - 2 * margin < 0.45:
                    continue
                facet_window(
                    f"{tag}_f{fi}", a, b, margin, ln - margin, za, zb, mats,
                    lit=lit and fi == 1,
                )

    # One lit sash on each bay's north-east return as well, so the night state
    # reads as four windows rather than two — the composition the plan asks for.
    for tag, t01 in (("swb_hi", BAY_SW_T), ("neb_hi", BAY_NE_T)):
        a, b = bay_facets(*t01)[2]
        _, _, ln = facet_frame(a, b)
        h = 0.26 + TRIM + 0.07
        prism(
            f"{tag}_f2_glow",
            facet_rect(a, b, h, ln - h, D_GLOW[0], D_GLOW[1]),
            6.15 + TRIM + 0.07,
            8.60 - TRIM - 0.07,
            mats["Toy_glass_Glow"],
        )

    # ----------------------------------------------------------- the cornice
    # Bed, dentil course, crown. The dentil course is a continuous PALE band
    # rather than modelled dentils: at 300-500 m a pale line under a dark crown
    # is exactly the dentil read, and 24 modelled blocks would cost 1,200
    # triangles for nothing.
    cornice_band("cornice_bed", CORN_Z[0], CORN_Z[1] + LAP, CORN_PROUD[0], mats["Toy_roofd"])
    cornice_band("cornice_dentil", CORN_Z[1], CORN_Z[2] + LAP, CORN_PROUD[1], mats["Toy_steel"])
    cornice_band("cornice_crown", CORN_Z[2], CORN_Z[3], CORN_PROUD[2], mats["Toy_roofd"])

    # -------------------------------------------------------------- the roof
    # Parapet on the other three sides only: the street end is capped by the
    # cornice, which is 0.50 m taller. Nothing up here may out-top Z_CREST.
    rim("parapet", FOOTPRINT, 0.25, Z_DECK - LAP, Z_PARAPET, mats["Toy_roofd"])

    prism("terrace", plan_rect(*TERRACE_T, *TERRACE_U), Z_DECK - LAP, Z_TERRACE, mats["Toy_rust"])
    # A low slatted guard on the terrace's street edge and its two flanks. It is
    # what makes the deck read as an occupied place rather than a coloured
    # rectangle, and it is the only thing on the roof with a vertical face.
    g = 0.10
    for tag, rect in (
        ("front", plan_rect(TERRACE_T[0], TERRACE_T[1], TERRACE_U[0], TERRACE_U[0] + g)),
        ("sw", plan_rect(TERRACE_T[0], TERRACE_T[0] + g, TERRACE_U[0], TERRACE_U[1])),
        ("ne", plan_rect(TERRACE_T[1] - g, TERRACE_T[1], TERRACE_U[0], TERRACE_U[1])),
    ):
        prism(f"terrace_guard_{tag}", rect, Z_TERRACE - LAP, Z_TERRACE + TERRACE_GUARD,
              mats["Toy_rust"])

    # The spa. Its shell is an ANNULUS, not a solid cylinder: built solid (the
    # first pass) its top cap covered the water and the whole thing rendered as
    # a grey pancake from the app's own camera angle.
    scx, scy = plan_xy(*SPA_CENTRE)
    rim("spa_shell", circle(scx, scy, SPA_R), SPA_RIM, Z_TERRACE - LAP, Z_SPA,
        mats["Toy_steel"], centre=(scx, scy))
    # The water sits 40 mm under the rim, not 70: deeper than that and the shell
    # shadows it into the same grey the solid-cylinder version rendered.
    cylinder("spa_water", scx, scy, SPA_R - SPA_RIM + 0.02, Z_SPA - 0.30, Z_SPA - 0.04,
             mats["Toy_glassl"])
    cylinder("spa_glow", scx, scy, SPA_R - SPA_RIM - 0.05, Z_SPA - 0.04, Z_SPA - 0.015,
             mats["Toy_glassl_Glow"])

    for i, u in enumerate(SKYLIGHT_U):
        prism(
            f"skylight{i}",
            plan_rect(SKYLIGHT_T[0], SKYLIGHT_T[1], u, u + SKYLIGHT_D),
            Z_DECK - LAP,
            Z_DECK + 0.28,
            mats["Toy_ink"],
            mat_top=mats["Toy_glassl"],
        )

    prism("roof_hatch", plan_rect(*HATCH_T, *HATCH_U), Z_DECK - LAP, Z_HATCH, mats["Toy_roofd"],
          mat_top=mats["Toy_steel"])

    # ------------------------------------------------------------ rear (SE)
    # The 2012-13 rebuild put a "soaring glass wall" onto the private yard here.
    # Its size and storey are INFERRED — no photograph of this elevation was
    # located — but it faces a walled yard and is seen only from directly above,
    # so the cost of being wrong is low. Recorded in REPORT.md.
    ra, rb = REAR_NE, REAR_SW
    _, _, rlen = facet_frame(ra, rb)
    prism("rear_surround", facet_rect(ra, rb, 1.55, 5.75, -LAP, D_SURROUND), 0.30, 3.60,
          mats["Toy_steel"])
    prism("rear_glass", facet_rect(ra, rb, 1.55 + TRIM, 5.75 - TRIM, -LAP, D_GLASS), 0.30 + TRIM,
          3.60 - TRIM, mats["Toy_glass"])
    prism("rear_door", facet_rect(ra, rb, 0.45, 1.35, -LAP, D_REVEAL), 0.0, 2.10, mats["Toy_ink"])

    # ------------------------------------------------------------------ bevel
    # The chunky masses carry the miniature read and get the full 0.10/2. Trim
    # layers, grooves and glow shells are thin and numerous — a token softening
    # or none at all is what keeps this under cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_glow", "_glass")) or "_groove" in obj.name:
            continue
        if obj.name.endswith(("_surround", "_reveal", "_apron", "_belt", "_jamb0", "_jamb1")) or "_guard_" in obj.name:
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
    """Move the model so its XY bounding-box centre is the origin, and its
    lowest geometry sits on z = 0."""
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
    print(f"[build] design footprint area: {FOOT_AREA:.2f} m2")
    print(f"[build] frontage: {FRONT_LEN:.3f} m   depth: {DEPTH:.2f} m")
    print(f"[build] design (area-centroid) anchor: {DESIGN_ANCHOR}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] street elevation faces: {FRONT_HEADING:.2f} deg true")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "41-south-park.blend")
    glb = os.path.join(out, "41-south-park.glb")
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
