"""Deterministic Blender build of the SF-SIM miniature 160 South Park.

    blender -b --python build_160_south_park.py -- [--out DIR]

Writes 160-south-park.blend and 160-south-park.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, tile-eave ridge exactly
9.40 m.

Design (see REFERENCE.md for the sources behind every number):

* a 1924 two-storey commercial-front building on the NORTH-WEST rim of South
  Park, the oval that is San Francisco's oldest planned residential square;
* the recognition rests on TWO things and nothing else. Close up it is the
  round-arched, multi-pane window centred on the upper storey under a moulded
  archivolt — the only arch on this side of the oval. From the air it is the
  projecting pent roof of RED BARREL TILE across the street end, the one warm
  colour on an otherwise entirely monochrome building and the only thing on
  this roof that any neighbour does not also have;
* everything else is flat dark slate charcoal: walls, pilasters, window
  surrounds, the lintel band, the shopfront frame. The building's interest is
  relief, not colour. The single other accent is the warm-wood street door;
* the plan is a bent strip: 6.17 m of frontage against ~26.5 m of built depth,
  running back at 282 deg for 12.8 m and then at 315.1 deg, because South Park's
  lots are radial at the oval and orthogonal at the rear;
* the roof is flat at 8.81 m (the DataSF LiDAR height MODE — the median is a
  roof-and-yard blend, see the plan's 2.3), with the tile ridge at 9.40 m;
* night state: the arched window is the hero glow and the storefront window the
  supporting accent. The two flanking upper windows stay dark — this is a
  six-room building on a quiet oval, and a fully lit facade would read as an
  office block. Glow surfaces are thin shells proud of the opaque glazing: the
  app renders _Glow in a separate layer that is ~12% alpha by day, so a primary
  surface must never be authored as glow.

Authoring frame: the plan polygon is authored directly in world metres relative
to the design anchor, because the lot BENDS and no single local axis describes
it. Facade features use a front frame (t along the frontage from its SOUTH end,
d outward, z up) built from the two front corners. The building sits ~108 deg
off the world axes, so the axis-aligned XY bounding box is ~25 x 18 m even
though the building is 6.2 x 26.5 m. That is expected, not a scale error.
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

# Area centroid of the design footprint = the DESIGN anchor. Derived in
# docs/asset-plans/160-south-park.md 2.3 from the surveyed DataSF parcel
# 3775067 truncated to the built depth that reproduces SF Planning's 3,674 sq ft
# over two storeys (166.4 m2 per floor).
DESIGN_ANCHOR = (-122.3948669, 37.7812686)

# Design footprint, metres east/north from DESIGN_ANCHOR. Six corners: the
# surveyed lot, with the eleven-segment street arc collapsed to its chord (the
# arc's bulge is 0.14 m — below the bevel radius, so modelling it would be
# false precision).
FOOTPRINT = [
    (12.873, -1.497),    # front-north corner (party wall with 156)
    (10.952, -7.365),    # front-south corner (party wall with 164)
    (-1.523, -5.075),    # south party line, bend
    (-12.409, 5.841),    # rear-south corner
    (-8.103, 10.134),    # rear-north corner
    (0.397, 1.611),      # north party line, bend
]

FRONT_SOUTH = FOOTPRINT[1]
FRONT_NORTH = FOOTPRINT[0]

# ---- vertical scheme (metres above grade) ---------------------------------
Z_BULK = 0.35           # dark base bulkhead under the shopfront
Z_SHOP_SILL = 0.55
Z_SHOP_HEAD = 3.05
Z_SHOP_TOP = 3.55   # solid spandrel between the glass head and the lintel
Z_DOOR_HEAD = 2.40
Z_LINTEL0, Z_LINTEL1 = 3.90, 4.25   # proud lintel band with its two tie-plates
Z_PANEL0, Z_PANEL1 = 4.35, 8.45     # recessed upper panel field
Z_SILL = 5.05                       # all three upper windows share a sill line
Z_WIN_HEAD = 7.25                   # the two flanking rectangular windows
Z_SPRING = 7.35                     # the arch springs a little above them
Z_CORNICE0 = 8.55                   # plain moulded band under the tile
Z_DECK = 8.81           # flat roof — MEASURED (DataSF LiDAR height MODE,
                        # hgt_majoritycm 881 over 882 cells). The median, 7.79 m,
                        # is a roof-and-yard blend because the LiDAR polygon is
                        # the whole lot; see the plan's 2.3.
Z_RIDGE = 9.40          # tile-eave ridge against the wall — the bbox top, and
                        # the manifest targetHeightM, so the loader's scale is
                        # exactly 1.0. MEASURED (LiDAR hgt_maxcm 941).
Z_EAVE_OUT = 9.05       # outer edge of the tile: the pent slopes DOWN to the
                        # street, which is what makes it read from the air.

PARAPET_H = 0.15        # low lip around the rest of the roof, wall colour
PARAPET_W = 0.16

# ---- frontage layout, t measured from the SOUTH end of the 6.17 m chord ----
FRONT_PAD = 0.02        # tiny overhang so proud bands do not stop dead

# ground storey
SHOP_T0, SHOP_T1 = 0.50, 3.85
DOOR_T0, DOOR_T1 = 4.13, 5.31
SHOP_BACK = -0.24

# upper storey
PILASTER = 0.55
WIN_S_T0, WIN_S_T1 = 0.55, 1.70     # south rectangular window
ARCH_T0, ARCH_T1 = 2.12, 4.07       # the arch — 1.95 m wide, near-centred
WIN_N_T0, WIN_N_T1 = 4.49, 5.55     # north rectangular window
# Facade depth convention. There are no booleans in this build: the body is a
# solid to d = 0, so an "opening" is a slab that reaches slightly PROUD of the
# wall and is made to read as recessed by a surround that stands further proud
# still. The first build put the fills at d = -0.14..-0.07 and every window on
# the building vanished inside the wall.
WIN_BACK = -0.16        # back of a glazing slab
D_GLASS = 0.015         # glazing face, just proud of the wall
D_MUNTIN0 = 0.02        # muntin bars sit on the glass
D_MUNTIN1 = 0.07
D_SURROUND = 0.10       # pilasters, shopfront frame, door
D_WINTRIM = 0.07        # the two flanking windows wear a plain flat surround
                        # and nothing more, exactly as the real ones do
ARCH_SEG = 12                       # semicircle segments — 12 is plenty at
                                    # 1 m radius and keeps the cap under budget
ARCHIVOLT_W = 0.16                  # band width, ~2x the real relief (2.6)
ARCHIVOLT_PROUD = 0.14
MUNTIN = 0.05                       # square bars, proud of the glass

LINTEL_PROUD = 0.12
CORNICE_PROUD = 0.15
STRING_PROUD = 0.05     # plain string course carried round the blind flanks
EAVE_PROJ = 0.46        # tile projection beyond the facade plane
EAVE_THICK = 0.11       # a 0.16 slab under a 0.10 bevel rendered as an orange
                        # sausage in the first review; the tile has to read as a
                        # BAND, not as a bolster
EAVE_WALL = 0.10        # upstand the tiles die into

STACK_W = 0.72          # roof stack near the north party wall (see REPORT.md)
STACK_TOP = 9.30        # deliberately BELOW the ridge: 9.40 is the measured
                        # LiDAR maximum and the stack must not steal it

REAR_DOOR_W, REAR_DOOR_H = 1.00, 2.10
REAR_WIN_W, REAR_WIN_H = 0.90, 1.50

BEVEL_W, BEVEL_SEG = 0.10, 2

PALETTE_HEX = {
    "Toy_roofd": "45454a",   # THE BUILDING. Walls, pilasters, lintel band,
                             # archivolt, cornice, stack — one flat slate for
                             # everything. The real paint is a cool blue
                             # charcoal ~#4a505a; #45454a is the nearest palette
                             # entry and is on-palette, which is the tiebreak.
    "Toy_ink": "3a3530",     # roof plane, base bulkhead, tie-plates, rear door.
                             # One clear step darker than the walls so the plan
                             # outline reads from directly overhead.
    "Toy_brick": "c96f4a",   # THE TILE EAVE, and nothing else. It is the only
                             # saturated colour on the building and the whole
                             # reason the roof reads from the app's camera.
    "Toy_glass": "2a4d73",
    "Toy_steel": "9aa0a6",   # the muntin bars only. Toy_trim (#f3efe6) was the
                             # first choice and blew the windows out to near-
                             # white at city distance, which made the darkest
                             # building on the block read as the lightest. The
                             # real muntins are the same slate as the wall, so
                             # any lift is already an exaggeration; #9aa0a6 is
                             # the smallest one that still reads as a GRID.
    "Toy_rust": "a86444",    # THE STREET DOOR, and nothing else
    # Two glow materials, not one, so the hierarchy the plan asks for survives
    # into the app: its night layer is an unlit overlay drawn at each material's
    # own baked colour, so a single glow colour would light the hero and the
    # accent identically.
    "Toy_glassl_Glow": "6f95b8",   # the arched window — the HERO
    "Toy_glass_Glow": "2a4d73",    # the storefront — the supporting accent
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

# Front frame: t runs along the frontage SOUTH -> NORTH, d runs outward (away
# from the lot). The outward sense is resolved against the footprint centroid
# rather than assumed from the winding order.
_FT = _unit(FRONT_NORTH[0] - FRONT_SOUTH[0], FRONT_NORTH[1] - FRONT_SOUTH[1])
_FN = (-_FT[1], _FT[0])
if (FRONT_SOUTH[0] + _FN[0] - CX) ** 2 + (FRONT_SOUTH[1] + _FN[1] - CY) ** 2 < (
    FRONT_SOUTH[0] - CX
) ** 2 + (FRONT_SOUTH[1] - CY) ** 2:
    _FN = (-_FN[0], -_FN[1])

FRONT_LEN = math.hypot(
    FRONT_NORTH[0] - FRONT_SOUTH[0], FRONT_NORTH[1] - FRONT_SOUTH[1]
)
FRONT_HEADING = (math.degrees(math.atan2(_FN[0], _FN[1])) + 360.0) % 360.0


def front_xy(t, d):
    """Front frame (t along the frontage, d outward) -> world (x east, y north)."""
    return (
        FRONT_SOUTH[0] + _FT[0] * t + _FN[0] * d,
        FRONT_SOUTH[1] + _FT[1] * t + _FN[1] * d,
    )


def front_rect(t0, t1, d0, d1):
    """CCW-in-(t, d) rectangle expressed in world XY."""
    return [front_xy(t0, d0), front_xy(t1, d0), front_xy(t1, d1), front_xy(t0, d1)]


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
    a third of the object's thinnest dimension: window fills, muntins and glow
    shells are only 40-160 mm thick and a flat bevel on those collapses opposing
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


def profile(name, pts_tz, d0, d1, mat):
    """Closed extrusion of a (t, z) profile in the FACADE plane, along the
    outward normal from d0 to d1. This is what makes the arch buildable: prism()
    can only extrude vertically, and the arch is a shape in the wall."""
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


def arch_outline(t0, t1, z_bottom, z_spring, seg=ARCH_SEG, grow=0.0):
    """(t, z) outline of a round-headed opening, optionally grown outward by
    `grow` (used for the archivolt's outer edge)."""
    tc = (t0 + t1) / 2.0
    r = (t1 - t0) / 2.0 + grow
    pts = [(tc - r, z_bottom), (tc + r, z_bottom), (tc + r, z_spring)]
    for k in range(1, seg):
        a = math.pi * k / seg
        pts.append((tc + r * math.cos(a), z_spring + r * math.sin(a)))
    pts.append((tc - r, z_spring))
    return pts


def inset_polygon(poly, dist):
    """Offset every edge of a simple polygon inward by `dist` and re-intersect
    adjacent edges. Used for the roof parapet's inner ring."""
    n = len(poly)
    lines = []
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        d = _unit(b[0] - a[0], b[1] - a[1])
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
    """Closed band solid between `poly` and its inward offset — a parapet or a
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


def rear_frame():
    """(origin, along, outward) frame for the rear wall, resolved against the
    footprint centroid so the outward sense is not assumed."""
    a, b = FOOTPRINT[3], FOOTPRINT[4]
    d = _unit(b[0] - a[0], b[1] - a[1])
    n = (-d[1], d[0])
    if (a[0] + n[0] - CX) ** 2 + (a[1] + n[1] - CY) ** 2 < (a[0] - CX) ** 2 + (
        a[1] - CY
    ) ** 2:
        n = (-n[0], -n[1])
    return a, d, n, math.hypot(b[0] - a[0], b[1] - a[1])


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


def rect_window(name, t0, t1, z0, z1, mats, muntins=(1, 1)):
    """A recessed rectangular opening with a cross of proud muntin bars."""
    prism(
        f"{name}_fill",
        front_rect(t0, t1, WIN_BACK, D_GLASS),
        z0,
        z1,
        mats["Toy_glass"],
    )
    # Plain flat surround, proud of the wall: the real windows have exactly this
    # and nothing more, and it is what makes them read as openings.
    rim_pts = (
        (t0 - 0.10, t0, z0 - 0.10, z1 + 0.10),
        (t1, t1 + 0.10, z0 - 0.10, z1 + 0.10),
        (t0, t1, z1, z1 + 0.10),
        (t0, t1, z0 - 0.10, z0),
    )
    for i, (a0, a1, b0, b1) in enumerate(rim_pts):
        prism(f"{name}_trim{i}", front_rect(a0, a1, 0.0, D_WINTRIM), b0, b1,
              mats["Toy_roofd"])
    nv, nh = muntins
    for k in range(1, nv + 1):
        tc = t0 + (t1 - t0) * k / (nv + 1)
        profile(
            f"{name}_mv{k}",
            [
                (tc - MUNTIN / 2, z0),
                (tc + MUNTIN / 2, z0),
                (tc + MUNTIN / 2, z1),
                (tc - MUNTIN / 2, z1),
            ],
            D_MUNTIN0,
            D_MUNTIN1,
            mats["Toy_steel"],
        )
    for k in range(1, nh + 1):
        zc = z0 + (z1 - z0) * k / (nh + 1)
        profile(
            f"{name}_mh{k}",
            [
                (t0, zc - MUNTIN / 2),
                (t1, zc - MUNTIN / 2),
                (t1, zc + MUNTIN / 2),
                (t0, zc + MUNTIN / 2),
            ],
            D_MUNTIN0,
            D_MUNTIN1,
            mats["Toy_steel"],
        )


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    mats = {name: make_material(name) for name in PALETTE_HEX}

    # ------------------------------------------------------------ main volume
    # The surveyed lot truncated to the built depth. The party flanks are blind
    # and the rear is barely seen, so everything else here is applied to the
    # street elevation.
    prism("body", FOOTPRINT, 0.0, Z_DECK, mats["Toy_roofd"], mat_top=mats["Toy_ink"])

    # ---------------------------------------------------------------- parapet
    # A low lip around the roof in the wall colour. The roof is the surface the
    # app's camera actually sees, and without this it reads as a bare cut face.
    rim("parapet", FOOTPRINT, PARAPET_W, Z_DECK, Z_DECK + PARAPET_H, mats["Toy_roofd"])

    # ----------------------------------------------------------- base bulkhead
    # Runs the WHOLE perimeter rather than the street elevation alone: every
    # building has a base course, and a return that stops dead at a party wall
    # reads as a box stuck to the wall. It also gives the terrain seam somewhere
    # to hide.
    rim("base_bulkhead", FOOTPRINT, -0.05, 0.0, Z_BULK, mats["Toy_ink"])

    # ------------------------------------------------------------- pilasters
    # The real upper wall is a panel field recessed between two flat pilasters.
    # With no booleans available the same reading comes from standing the
    # PILASTERS proud instead of sinking the field, which also keeps the corners
    # crisp against the party walls.
    for name, t0, t1 in (
        ("pilaster_s", -FRONT_PAD, PILASTER),
        ("pilaster_n", FRONT_LEN - 0.62, FRONT_LEN + FRONT_PAD),
    ):
        prism(name, front_rect(t0, t1, 0.0, D_SURROUND), Z_PANEL0, Z_DECK,
              mats["Toy_roofd"])

    # --------------------------------------------------------- ground storey
    # One wide recessed shopfront window and one flush warm-wood door. The door
    # is the only warm value at street level and must not be recessed into its
    # own shadow — it sits ON the wall plane with a shallow reveal.
    prism(
        "shop_fill",
        front_rect(SHOP_T0, SHOP_T1, SHOP_BACK, D_GLASS),
        Z_SHOP_SILL,
        Z_SHOP_HEAD,
        mats["Toy_glass"],
    )
    # Shopfront frame: slim proud jambs and a head, which is what makes the
    # glass read as set into an opening rather than stuck onto the wall.
    for name, t0, t1 in (
        ("shop_jamb_s", SHOP_T0 - 0.10, SHOP_T0),
        ("shop_jamb_n", SHOP_T1, SHOP_T1 + 0.10),
    ):
        prism(name, front_rect(t0, t1, 0.0, D_SURROUND), Z_SHOP_SILL - 0.10,
              Z_SHOP_TOP, mats["Toy_roofd"])
    prism(
        "shop_head",
        front_rect(SHOP_T0 - 0.10, SHOP_T1 + 0.10, 0.0, D_SURROUND),
        Z_SHOP_HEAD,
        Z_SHOP_TOP,
        mats["Toy_roofd"],
    )
    for k in range(1, 3):
        tc = SHOP_T0 + (SHOP_T1 - SHOP_T0) * k / 3.0
        profile(
            f"shop_mv{k}",
            [
                (tc - MUNTIN / 2, Z_SHOP_SILL),
                (tc + MUNTIN / 2, Z_SHOP_SILL),
                (tc + MUNTIN / 2, Z_SHOP_HEAD),
                (tc - MUNTIN / 2, Z_SHOP_HEAD),
            ],
            D_MUNTIN0,
            D_MUNTIN1,
            mats["Toy_roofd"],
        )
    # Supporting night accent: the shopfront, at a lower value than the arch.
    prism(
        "shop_glow",
        front_rect(SHOP_T0 + 0.08, SHOP_T1 - 0.08, D_GLASS, D_GLASS + 0.04),
        Z_SHOP_SILL + 0.10,
        Z_SHOP_HEAD - 0.10,
        mats["Toy_glass_Glow"],
    )
    prism(
        "door_reveal",
        front_rect(DOOR_T0 - 0.09, DOOR_T1 + 0.09, -0.10, 0.02),
        0.0,
        Z_SHOP_TOP,
        mats["Toy_ink"],
    )
    prism(
        "door",
        front_rect(DOOR_T0, DOOR_T1, -0.06, D_SURROUND),
        0.0,
        Z_DOOR_HEAD,
        mats["Toy_rust"],
    )

    # ------------------------------------------------------------ lintel band
    # Proud band across the whole frontage with its two square tie-plates. It is
    # the one piece of the ground storey that survives at thumbnail size.
    prism(
        "lintel",
        front_rect(-FRONT_PAD, FRONT_LEN + FRONT_PAD, 0.0, LINTEL_PROUD),
        Z_LINTEL0,
        Z_LINTEL1,
        mats["Toy_roofd"],
    )
    for k in (1, 2):
        tc = FRONT_LEN * k / 3.0
        prism(
            f"tieplate_{k}",
            front_rect(tc - 0.11, tc + 0.11, LINTEL_PROUD, LINTEL_PROUD + 0.05),
            Z_LINTEL0 + 0.06,
            Z_LINTEL1 - 0.06,
            mats["Toy_ink"],
        )

    # ----------------------------------------------------------- string course
    # Carried round the whole perimeter at the lintel line. The party flanks are
    # blind and 26 m long, and 164 next door is low, so without this the south
    # wall reads as a slab rather than as two storeys.
    rim(
        "string_course",
        FOOTPRINT,
        -STRING_PROUD,
        Z_LINTEL1 + 0.02,
        Z_LINTEL1 + 0.10,
        mats["Toy_roofd"],
    )

    # --------------------------------------------------- upper storey windows
    rect_window("win_s", WIN_S_T0, WIN_S_T1, Z_SILL, Z_WIN_HEAD, mats, muntins=(1, 2))
    rect_window("win_n", WIN_N_T0, WIN_N_T1, Z_SILL, Z_WIN_HEAD, mats, muntins=(1, 2))

    # ------------------------------------------------------- THE ARCHED WINDOW
    # The building. A true semicircular head, a moulded archivolt exaggerated to
    # roughly twice its real relief so it survives the aerial camera, and a
    # coarse grid of proud muntins — three verticals, two horizontals below the
    # springing and three radial bars in the head. The real glazing is a 6 x 6
    # grid; at 40 px that is grey mush, and the grid has to read as a GRID.
    arch_in = arch_outline(ARCH_T0, ARCH_T1, Z_SILL, Z_SPRING)
    profile("arch_fill", arch_in, WIN_BACK, D_GLASS, mats["Toy_glass"])
    profile(
        "arch_glow",
        arch_outline(ARCH_T0 + 0.07, ARCH_T1 - 0.07, Z_SILL + 0.08, Z_SPRING),
        D_GLASS,
        D_GLASS + 0.04,
        mats["Toy_glassl_Glow"],
    )

    tc = (ARCH_T0 + ARCH_T1) / 2.0
    r_in = (ARCH_T1 - ARCH_T0) / 2.0
    r_out = r_in + ARCHIVOLT_W
    # Archivolt: a horseshoe profile, walked as ONE simple loop — up the outer
    # left jamb, over the outer arc, down the outer right jamb, step in, up the
    # inner right jamb, back round the inner arc, down the inner left jamb.
    # Splicing arch_outline() slices instead produced a self-intersecting
    # polygon that tessellated into a black diagonal slab across the facade.
    def semi(radius, lo_to_hi):
        pts = []
        rng = range(0, ARCH_SEG + 1)
        for k in (rng if lo_to_hi else reversed(rng)):
            a = math.pi * k / ARCH_SEG
            pts.append((tc + radius * math.cos(a), Z_SPRING + radius * math.sin(a)))
        return pts

    # cos(0) = +1, so semi(r, True) runs RIGHT -> LEFT and semi(r, False) runs
    # LEFT -> RIGHT. The loop goes up the outer left jamb, over, down the outer
    # right jamb, in, up the inner right jamb, back over, down the inner left.
    horseshoe = [(tc - r_out, Z_SILL)]
    horseshoe += semi(r_out, False)
    horseshoe += [(tc + r_out, Z_SILL), (tc + r_in, Z_SILL)]
    horseshoe += semi(r_in, True)
    horseshoe += [(tc - r_in, Z_SILL)]
    profile("archivolt", horseshoe, 0.0, ARCHIVOLT_PROUD, mats["Toy_roofd"])

    # Vertical muntins run from the sill straight up into the lunette, clipped
    # by the arc. The first build put a three-bar RADIAL fan in the head; it
    # rendered as a peace sign and read as a wheel, not as glazing. The real
    # window continues its grid into the head, and so does this one.
    for k in range(1, 4):
        mt = ARCH_T0 + (ARCH_T1 - ARCH_T0) * k / 4.0
        top = Z_SPRING + math.sqrt(max(r_in**2 - (mt - tc) ** 2, 0.0)) - 0.02
        profile(
            f"arch_mv{k}",
            [
                (mt - MUNTIN / 2, Z_SILL),
                (mt + MUNTIN / 2, Z_SILL),
                (mt + MUNTIN / 2, top),
                (mt - MUNTIN / 2, top),
            ],
            D_MUNTIN0,
            D_MUNTIN1,
            mats["Toy_steel"],
        )
    # Horizontals below the springing, plus the impost line across the base of
    # the lunette — the one bar that says "arch" rather than "curved top".
    for k in range(1, 4):
        mz = Z_SILL + (Z_SPRING - Z_SILL) * k / 3.0
        profile(
            f"arch_mh{k}",
            [
                (ARCH_T0, mz - MUNTIN / 2),
                (ARCH_T1, mz - MUNTIN / 2),
                (ARCH_T1, mz + MUNTIN / 2),
                (ARCH_T0, mz + MUNTIN / 2),
            ],
            D_MUNTIN0,
            D_MUNTIN1,
            mats["Toy_steel"],
        )

    # ---------------------------------------------------------------- cornice
    prism(
        "cornice",
        front_rect(-FRONT_PAD, FRONT_LEN + FRONT_PAD, 0.0, CORNICE_PROUD),
        Z_CORNICE0,
        Z_DECK,
        mats["Toy_roofd"],
    )

    # ------------------------------------------------------- THE TILE EAVE
    # A shallow pent of red barrel tile across the whole street end, ridged
    # against the wall at 9.40 and sloping DOWN to 9.05 at its outer edge. This
    # is the only warm colour and the only non-flat plane on the roof, and from
    # the app's camera it is the entire recognition. The upstand it dies into is
    # wall-coloured so the tile reads as a band, not as a lump.
    prism(
        "eave_upstand",
        front_rect(-FRONT_PAD, FRONT_LEN + FRONT_PAD, 0.0, EAVE_WALL),
        Z_DECK,
        Z_RIDGE,
        mats["Toy_roofd"],
    )
    t0, t1 = -0.08, FRONT_LEN + 0.08
    d_in, d_out = EAVE_WALL - 0.02, EAVE_PROJ
    top = [
        (front_xy(t0, d_in) + (Z_RIDGE,)),
        (front_xy(t1, d_in) + (Z_RIDGE,)),
        (front_xy(t1, d_out) + (Z_EAVE_OUT,)),
        (front_xy(t0, d_out) + (Z_EAVE_OUT,)),
    ]
    bot = [(x, y, z - EAVE_THICK) for x, y, z in top]
    verts = top + bot
    faces = [
        (0, 1, 2, 3),
        (7, 6, 5, 4),
        (0, 3, 7, 4),
        (1, 5, 6, 2),
        (0, 4, 5, 1),
        (3, 2, 6, 7),
    ]
    new_mesh("eave_tile", verts, faces, [mats["Toy_brick"]])

    # ------------------------------------------------------------- roof stack
    # One square stucco stack near the north party wall, at the street end. It
    # is INFERRED from the January 2025 panoramas and is capped below the ridge:
    # 9.40 m is the measured LiDAR maximum and the model's top must be the tile.
    st = FRONT_LEN - 1.05
    prism(
        "stack",
        front_rect(st - STACK_W / 2, st + STACK_W / 2, -1.55, -1.55 + STACK_W),
        Z_DECK - 0.10,
        STACK_TOP,
        mats["Toy_roofd"],
    )

    # -------------------------------------------------------- rear elevation
    # Faces the rear yard and is seen only from directly above. One door and two
    # plain windows, and nothing else.
    ra, rd, rn, rlen = rear_frame()

    def rear_poly(s0, s1, d0, d1):
        return [
            (ra[0] + rd[0] * s + rn[0] * d, ra[1] + rd[1] * s + rn[1] * d)
            for s, d in ((s0, d0), (s1, d0), (s1, d1), (s0, d1))
        ]

    c0 = rlen / 2.0 - REAR_DOOR_W / 2.0
    prism(
        "rear_door",
        rear_poly(c0, c0 + REAR_DOOR_W, 0.02, -0.14),
        0.0,
        REAR_DOOR_H,
        mats["Toy_ink"],
    )
    for k, s in ((0, 1.05), (1, rlen - 1.05 - REAR_WIN_W)):
        prism(
            f"rear_win_{k}",
            rear_poly(s, s + REAR_WIN_W, 0.01, -0.12),
            Z_SILL,
            Z_SILL + REAR_WIN_H,
            mats["Toy_glass"],
        )

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.10/2. Muntins, fills, fans and glow shells are small and numerous — a
    # token softening or none at all is what keeps this under cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        n = obj.name
        if (
            n.endswith(("_fill", "_glow"))
            or "_mv" in n
            or "_mh" in n
            or "_fan" in n
        ):
            continue
        if n.startswith(("string_course", "tieplate", "cornice", "eave_tile")) or "_trim" in n:
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
    """Move the model so its XY bounding-box centre is the origin.

    The lot is a bent strip, so its bbox centre is ~1.4 m from its area
    centroid. Shift the geometry and carry the same shift into the anchor, which
    keeps the building on its real footprint (AGENTS rule 5)."""
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
    print(f"[build] frontage: {FRONT_LEN:.3f} m")
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

    blend = os.path.join(out, "160-south-park.blend")
    glb = os.path.join(out, "160-south-park.glb")
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
