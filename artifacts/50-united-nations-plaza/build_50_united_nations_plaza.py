"""Deterministic Blender build of the SF-SIM miniature 50 United Nations Plaza.

    blender -b --python build_50_united_nations_plaza.py -- [--out DIR]

Writes 50-united-nations-plaza.blend and .glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
origin at the base centre, min Z = 0, so the export needs no transforms applied
after the fact.

Design (see REFERENCE.md for the measured geometry behind every number):

* the plan is a RING, not a block: a 112.53 x 66.93 m oriented footprint on the
  Civic Center grid (long axis bearing 80.92 deg true = local +X yawed +9.08 deg
  CCW) wrapped around an open 72.2 x 27.1 m courtyard, offset 2.05 m east and
  1.65 m south of the building centre so the north wing is the deep one;
* the ring is assembled from four abutting bars (south / north / west / east)
  that tile it exactly, which is what makes the courtyard a real void and keeps
  every piece a closed convex solid for the normals test;
* the two SOUTH corners are CONCAVE scoops - 8-segment arcs of R 10.4 m bowing
  into the building, each carrying an arched entrance. The north corners are
  square. That asymmetry is the plan-level recognition cue;
* the vertical composition is the same on all four sides: rusticated Toy_stone
  base to 11.0 m with one reveal course, belt course, a two-storey order to
  22.1 m, a 0.90 m projecting cornice at 23.2 m (which is what the DataSF LiDAR
  outline actually traces - see REFERENCE.md), a set-back attic behind a
  balustrade, a top cornice at 29.0 m and a hipped metal roof cresting at 33.0;
* the SOUTH front carries 18 free-standing Doric columns standing 0.85 m proud
  of the wall under that cornice, with a balustrade band between them; the
  west, east and north fronts get proud pilaster strips on the same rhythm;
* the NORTH CENTRAL wing (|x| < 31 m) stops four storeys up: parapet at 24.7 m
  and a flat roof carrying the 2013 green roof, two photovoltaic banks, gravel
  margins and mechanical plant. Its two end pavilions stay full height. This
  step is the building's second-strongest read from the air;
* night per the dossier: six Toy_gold_Glow arched entrances (three on the south
  centre, one on each concave corner, one on the north centre) and a continuous
  Toy_glass_Glow attic window band that traces the cornice line all the way
  round. No facade floodlighting - none is documented.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

YAW = math.radians(9.08)  # local +X (long axis) -> bearing 80.92 true

HALF_U = 56.265  # half-length of the oriented footprint (112.53 m)
HALF_V = 33.465  # half-width (66.93 m)

# Courtyard, measured off the OSM inner ring in the building's own frame.
CY_X0, CY_X1 = -34.20, 38.00
CY_Y0, CY_Y1 = -15.40, 11.70
CY_CHAMFER = 3.2  # the courtyard's two SOUTH corners are cut

PAV_X = 31.0  # north end pavilions run from |x| = PAV_X out to HALF_U

# Concave south corners: the arc runs from (-HALF_U, -HALF_V + SCOOP) round to
# (-HALF_U + SCOOP, -HALF_V), bowing SAG metres into the building.
SCOOP = 6.90
SAG = 1.20
SCOOP_SEGS = 8

# Vertical stack (metres above grade)
Z_PLINTH = 0.90
REVEALS = ((3.05, 3.35), (5.60, 5.95), (8.20, 8.50))  # rustication courses
Z_BASE = 11.00  # top of the two-storey rusticated base
Z_BELT = 11.70  # top of the belt course
Z_ORDER = 20.60  # top of the two-storey order (column capitals)
Z_FRIEZE = 22.10
Z_CORNICE = 23.20  # top of the main projecting cornice
Z_BALUS = 24.60  # top of the attic balustrade
Z_ATTIC = 27.60  # top of the attic storey wall
Z_PARAPET = 29.00  # top cornice / coping - the "97 ft" parapet
Z_CREST = 33.00  # flat top of the hipped metal roof
Z_NORTH_PARAPET = 24.70  # the four-storey north wing
Z_NORTH_DECK = 23.40

# Plan offsets from the wall plane, positive = outward
O_PLINTH = 0.30
O_BASE = 0.25
O_REVEAL = 0.05
O_BELT = 0.45
O_BODY = 0.00
O_CORNICE = 0.90
O_BALUS = 0.60
O_ATTIC = -1.30
O_TOPCORN = -0.70
O_EAVE = -0.70  # roof eave sits on the top cornice face

ROOF_RUN = (Z_CREST - Z_PARAPET) / math.tan(math.radians(35.0))  # 5.71 m

COL_N = 18  # south colonnade
COL_R = 0.80
COL_SEGS = 10
COL_PROUD = 0.85  # column face stands this far outside the wall plane

BAY = 5.29  # facade bay module, set by the colonnade rhythm

PALETTE_HEX = {
    "Toy_cream": "f2ede3",
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_sand": "ece4d4",
    "Toy_glass": "2a4d73",
    "Toy_steel": "9aa0a6",
    "Toy_navy": "2c4a70",
    "Toy_mint": "8fd0a8",
    "Toy_white": "f7f4ec",
    "Toy_white_Glow": "f7f4ec",
    "Toy_gold_Glow": "caa64a",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# -------------------------------------------------------------- mesh helpers


def rot2(p, ang=None):
    a = YAW if ang is None else ang
    c, s = math.cos(a), math.sin(a)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def new_mesh(name, verts, faces, materials, face_mats=None, smooth=False,
             recalc=True):
    verts = [(*rot2((v[0], v[1])), v[2]) for v in verts]
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
    if smooth:
        mesh.polygons.foreach_set("use_smooth", [True] * len(mesh.polygons))
    else:
        mesh.shade_flat()
    return obj


def bevel(obj, width=0.12, segments=2):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(
        bm,
        geom=list(bm.verts) + list(bm.edges),
        offset=width,
        segments=segments,
        profile=0.5,
        affect="EDGES",
        clamp_overlap=True,
    )
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def prism(name, pts, z0, z1, side_mat, top_mat=None, bottom_mat=None):
    """Extrusion of a CCW polygon, closed, with optional cap materials."""
    mats = [side_mat]

    def midx(m):
        if m is None or m == side_mat:
            return 0
        if m not in mats:
            mats.append(m)
        return mats.index(m)

    ti, bi = midx(top_mat), midx(bottom_mat)
    n = len(pts)
    verts = [(x, y, z0) for x, y in pts] + [(x, y, z1) for x, y in pts]
    faces, fm = [], []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
        fm.append(0)
    faces.append(tuple(range(n - 1, -1, -1)))
    fm.append(bi)
    faces.append(tuple(range(n, 2 * n)))
    fm.append(ti)
    return new_mesh(name, verts, faces, mats, fm)


def frustum(name, pts_lo, pts_hi, z0, z1, side_mat, top_mat=None):
    """Closed solid lofting one polygon to another of the same vertex count."""
    assert len(pts_lo) == len(pts_hi)
    mats = [side_mat]
    ti = 0
    if top_mat is not None and top_mat != side_mat:
        mats.append(top_mat)
        ti = 1
    n = len(pts_lo)
    verts = [(x, y, z0) for x, y in pts_lo] + [(x, y, z1) for x, y in pts_hi]
    faces, fm = [], []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
        fm.append(0)
    faces.append(tuple(range(n - 1, -1, -1)))
    fm.append(0)
    faces.append(tuple(range(n, 2 * n)))
    fm.append(ti)
    return new_mesh(name, verts, faces, mats, fm)


def box(name, cx, cy, z0, z1, sx, sy, mat, local_yaw=0.0, face_mats=None,
        mats=None):
    hx, hy = sx / 2, sy / 2
    corners = [rot2(c, local_yaw)
               for c in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy))]
    verts = [(cx + x, cy + y, z0) for x, y in corners]
    verts += [(cx + x, cy + y, z1) for x, y in corners]
    faces = [
        (3, 2, 1, 0),   # 0 bottom
        (4, 5, 6, 7),   # 1 top
        (0, 1, 5, 4),   # 2 -Y face
        (1, 2, 6, 5),   # 3 +X face
        (2, 3, 7, 6),   # 4 +Y face
        (3, 0, 4, 7),   # 5 -X face
    ]
    return new_mesh(name, verts, faces, mats or [mat], face_mats)


def cylinder(name, cx, cy, z0, z1, r, mat, segs=COL_SEGS):
    verts = []
    for k in range(segs):
        a = 2 * math.pi * k / segs
        verts.append((cx + r * math.cos(a), cy + r * math.sin(a), z0))
    for k in range(segs):
        a = 2 * math.pi * k / segs
        verts.append((cx + r * math.cos(a), cy + r * math.sin(a), z1))
    faces = [(i, (i + 1) % segs, segs + (i + 1) % segs, segs + i)
             for i in range(segs)]
    faces.append(tuple(range(segs - 1, -1, -1)))
    faces.append(tuple(range(segs, 2 * segs)))
    return new_mesh(name, verts, faces, [mat])


def arch_prism(name, cx, cy, z0, w, h_rect, r, depth, mat, local_yaw=0.0):
    """A rounded-top prism: rectangle plus a semicircular head, extruded."""
    hw = w / 2
    profile = [(-hw, 0.0), (hw, 0.0), (hw, h_rect)]
    for k in range(1, 8):
        a = math.pi * k / 8
        profile.append((hw * math.cos(a), h_rect + r * math.sin(a)))
    profile.append((-hw, h_rect))
    verts, faces = [], []
    n = len(profile)
    for sgn in (-1, 1):
        for px, pz in profile:
            ox, oy = rot2((px, sgn * depth / 2), local_yaw)
            verts.append((cx + ox, cy + oy, z0 + pz))
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    return new_mesh(name, verts, faces, [mat])


def arched_opening(name, cx, cy, nx, ny, z0, w, h_rect, r, glass, glow):
    """An arched entrance: an opaque dark arch standing proud of the wall with
    a thin gold arch plate on its outer face (see glow_pane for why).

    The yaw is DERIVED from the outward normal rather than passed in: in
    arch_prism the extrusion axis is (-sin yaw, cos yaw), so the two concave
    corner entrances need 135 deg, not the 45 deg their faces sit at, and
    getting it wrong turns the arch into a blade edge-on to the street.
    """
    d = 0.22
    yaw = math.atan2(-nx, ny)
    arch_prism(name, cx + nx * (0.05 + d / 2), cy + ny * (0.05 + d / 2), z0,
               w, h_rect, r, d, glass, local_yaw=yaw)
    off = 0.05 + d + GLOW_T / 2
    arch_prism(f"{name}_g", cx + nx * off, cy + ny * off, z0 + 0.22,
               w - 0.44, h_rect - 0.22, r - 0.22, GLOW_T, glow, local_yaw=yaw)


GLOW_T = 0.04  # thickness of a glow plate


def glow_pane(name, cx, cy, z0, z1, sx, sy, out_dir, glow, glass, axis="y"):
    """An OPAQUE dark pane with a thin glow plate standing on its outer face.

    The obvious construction - one solid whose outward FACE carries the glow
    material - does not survive the loader's day state: glow faces are drawn at
    12% opacity, and what shows through is not the solid's far cap (verified in
    Cycles) but the wall behind it, so the window reads pale by day. Putting the
    glow on its own plate in FRONT of an opaque pane makes the day read the
    pane's own dark colour, with no dependence on what lies behind.
    """
    box(name, cx, cy, z0, z1, sx, sy, glass)
    if axis == "y":
        box(f"{name}_g", cx, cy + out_dir * (sy + GLOW_T) / 2, z0 + 0.12,
            z1 - 0.12, sx - 0.24, GLOW_T, glow)
    else:
        box(f"{name}_g", cx + out_dir * (sx + GLOW_T) / 2, cy, z0 + 0.12,
            z1 - 0.12, GLOW_T, sy - 0.24, glow)


def material(name):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    rgb = PALETTE[name]
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    bsdf.inputs["Metallic"].default_value = 0.0
    if name.endswith("_Glow"):
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    mat.blend_method = "OPAQUE"
    return mat


# ------------------------------------------------------------ plan outlines
#
# The ring is tiled by four bars that share edges and never overlap:
#   south  y in [-HALF_V, CY_Y0]   full width, both south corners scooped
#   north  y in [CY_Y1,  HALF_V]   full width, square corners
#   west   x in [-HALF_U, CY_X0]   y in [CY_Y0, CY_Y1], inner-south chamfer
#   east   x in [CY_X1,  HALF_U]   y in [CY_Y0, CY_Y1], inner-south chamfer
#
# `d` offsets every EXTERIOR edge outward; shared interior edges never move,
# so the bars stay watertight against each other at any offset.

SCOOP_C = SAG and ((SCOOP * math.sqrt(2.0)) ** 2 / 4 + SAG ** 2) / (2 * SAG)
SCOOP_R = SCOOP_C  # arc radius, centre outside the building


def _scoop(sx, d):
    """8-segment concave arc at the south corner on side sx (-1 west, +1 east).

    Returned in order of increasing y for sx=+1 / decreasing for sx=-1 so the
    caller can splice it into a CCW outline.
    """
    ax, ay = sx * (HALF_U + d), -HALF_V + SCOOP
    bx, by = sx * (HALF_U - SCOOP), -(HALF_V + d)
    mx, my = (sx * HALF_U + sx * (HALF_U - SCOOP)) / 2, (-HALF_V + SCOOP - HALF_V) / 2
    nx, ny = sx / math.sqrt(2.0), -1 / math.sqrt(2.0)  # outward corner normal
    ccx, ccy = mx + nx * (SCOOP_R - SAG), my + ny * (SCOOP_R - SAG)
    r = SCOOP_R - d  # offsetting the concave surface outward shrinks the radius
    a0 = math.atan2(ay - ccy, ax - ccx)
    a1 = math.atan2(by - ccy, bx - ccx)
    if sx > 0:
        if a1 < a0:
            a1 += 2 * math.pi
    else:
        if a1 > a0:
            a1 -= 2 * math.pi
    pts = []
    for k in range(SCOOP_SEGS + 1):
        a = a0 + (a1 - a0) * k / SCOOP_SEGS
        pts.append((ccx + r * math.cos(a), ccy + r * math.sin(a)))
    return pts


def outline(bar, d=0.0):
    """CCW plan polygon of one bar, exterior edges offset outward by d."""
    if bar == "south":
        # CCW: down the west edge, round the SW scoop, east along the south
        # wall, round the SE scoop, up the east edge, back along the north.
        pts = [(-(HALF_U + d), CY_Y0)]
        pts += _scoop(-1, d)                # SW scoop: west wall -> south wall
        pts += _scoop(+1, d)[::-1]          # SE scoop: south wall -> east wall
        pts += [(HALF_U + d, CY_Y0)]
        return pts
    if bar == "north":
        return [(-(HALF_U + d), CY_Y1), (HALF_U + d, CY_Y1),
                (HALF_U + d, HALF_V + d), (-(HALF_U + d), HALF_V + d)]
    if bar == "west":
        c = CY_CHAMFER
        return [(-(HALF_U + d), CY_Y0), (CY_X0 - c, CY_Y0), (CY_X0, CY_Y0 + c),
                (CY_X0, CY_Y1), (-(HALF_U + d), CY_Y1)]
    if bar == "east":
        c = CY_CHAMFER
        return [(CY_X1, CY_Y0 + c), (CY_X1 + c, CY_Y0), (HALF_U + d, CY_Y0),
                (HALF_U + d, CY_Y1), (CY_X1, CY_Y1)]
    raise ValueError(bar)


def pav_outline(sx, d=0.0):
    """One north end pavilion (sx = -1 west, +1 east), CCW."""
    x_in = sx * PAV_X
    x_out = sx * (HALF_U + d)
    xs = sorted((x_in, x_out))
    return [(xs[0], CY_Y1), (xs[1], CY_Y1),
            (xs[1], HALF_V + d), (xs[0], HALF_V + d)]


def rect(x0, x1, y0, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def inset_rect(x0, x1, y0, y1, d):
    return rect(x0 + d, x1 - d, y0 + d, y1 - d)


# --------------------------------------------------------------------- build

BARS = ("south", "north", "west", "east")
UPPER = ("south", "west", "east")  # bars that carry the attic and metal roof


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    cream = material("Toy_cream")
    stone = material("Toy_stone")
    trim = material("Toy_trim")
    sand = material("Toy_sand")
    glass = material("Toy_glass")
    steel = material("Toy_steel")
    navy = material("Toy_navy")
    mint = material("Toy_mint")
    white = material("Toy_white")
    gglow = material("Toy_gold_Glow")
    wglow = material("Toy_white_Glow")

    # ---- the ring: base, belt, order, cornice on all four bars -------------
    for b in BARS:
        bevel(prism(f"plinth_{b}", outline(b, O_PLINTH), 0.0, Z_PLINTH,
                    stone, bottom_mat=stone), width=0.10)
        z = Z_PLINTH
        for ri, (r0, r1) in enumerate(REVEALS):
            prism(f"base_{b}_{ri}", outline(b, O_BASE), z, r0, stone)
            prism(f"base_rev_{b}_{ri}", outline(b, O_REVEAL), r0, r1, stone)
            z = r1
        prism(f"base_{b}_top", outline(b, O_BASE), z, Z_BASE, stone)
        bevel(prism(f"belt_{b}", outline(b, O_BELT), Z_BASE, Z_BELT, trim),
              width=0.10)
        prism(f"body_{b}", outline(b, O_BODY), Z_BELT, Z_FRIEZE, cream)
        bevel(prism(f"cornice_{b}", outline(b, O_CORNICE), Z_FRIEZE, Z_CORNICE,
                    trim, top_mat=trim), width=0.10)

    # ---- attic, balustrade, top cornice: everything except the north centre
    uppers = [(b, outline(b, 0.0)) for b in UPPER]
    upper_specs = [(b, lambda d, b=b: outline(b, d)) for b in UPPER]
    upper_specs += [(f"pav_{'w' if s < 0 else 'e'}",
                     lambda d, s=s: pav_outline(s, d)) for s in (-1, 1)]
    for name, fn in upper_specs:
        prism(f"attic_{name}", fn(O_ATTIC), Z_CORNICE, Z_ATTIC, cream)
        bevel(prism(f"balus_{name}", fn(O_BALUS), Z_CORNICE, Z_BALUS, trim,
                    top_mat=trim), width=0.10)
        bevel(prism(f"topcorn_{name}", fn(O_TOPCORN), Z_ATTIC, Z_PARAPET, trim,
                    top_mat=trim), width=0.10)

    # ---- the C-shaped hipped metal roof ------------------------------------
    # Five overlapping hip bars of equal pitch and equal eave height: where two
    # meet at a right angle their 35 deg planes intersect exactly on the 45 deg
    # diagonal, which IS the correct hip line, so the union needs no boolean.
    # Where two bars overlap their flat tops would be COPLANAR and z-fight to
    # black, so each bar crests a few centimetres below the one it hides under:
    # south wins at the south corners, west/east win over the pavilion bars.
    roof_bars = [
        ("roof_s", -HALF_U, HALF_U, -HALF_V, CY_Y0, 0.00),
        ("roof_w", -HALF_U, CY_X0, -HALF_V, HALF_V, 0.07),
        ("roof_e", CY_X1, HALF_U, -HALF_V, HALF_V, 0.07),
        ("roof_nw", -HALF_U, -PAV_X, CY_Y1, HALF_V, 0.14),
        ("roof_ne", PAV_X, HALF_U, CY_Y1, HALF_V, 0.14),
    ]
    for name, x0, x1, y0, y1, drop in roof_bars:
        z_top = Z_CREST - drop
        run = (z_top - Z_PARAPET) / math.tan(math.radians(35.0))
        lo = inset_rect(x0, x1, y0, y1, -O_EAVE)
        hi = inset_rect(x0, x1, y0, y1, -O_EAVE + run)
        bevel(frustum(name, lo, hi, Z_PARAPET, z_top, steel, top_mat=steel),
              width=0.10)

    # arched dormers: small bumps on the long outer slopes
    for k in range(6):
        dx = -42.0 + k * 16.8
        box(f"dormer_s_{k}", dx, -HALF_V + 4.2, Z_PARAPET + 1.1,
            Z_PARAPET + 2.6, 2.6, 2.2, steel)
        box(f"dormer_n_{k}", dx * 0.55, HALF_V - 4.2, Z_PARAPET + 1.1,
            Z_PARAPET + 2.6, 2.6, 2.2, steel) if abs(dx * 0.55) > PAV_X else None
    for k in range(4):
        dy = -22.0 + k * 14.7
        box(f"dormer_w_{k}", -HALF_U + 4.2, dy, Z_PARAPET + 1.1,
            Z_PARAPET + 2.6, 2.2, 2.6, steel)
        box(f"dormer_e_{k}", HALF_U - 4.2, dy, Z_PARAPET + 1.1,
            Z_PARAPET + 2.6, 2.2, 2.6, steel)

    # ---- the four-storey north centre: parapet, green roof, PV -------------
    nc = rect(-PAV_X, PAV_X, CY_Y1, HALF_V)
    prism("deck_nc", nc, Z_CORNICE - 0.2, Z_NORTH_DECK, stone, top_mat=stone)
    box("parapet_nc_n", 0.0, HALF_V - 0.35, Z_CORNICE, Z_NORTH_PARAPET,
        2 * PAV_X, 0.7, trim)
    box("parapet_nc_s", 0.0, CY_Y1 + 0.35, Z_CORNICE, Z_NORTH_PARAPET,
        2 * PAV_X, 0.7, trim)
    box("green_nc", 0.0, (CY_Y1 + HALF_V) / 2 - 0.4, Z_NORTH_DECK,
        Z_NORTH_DECK + 0.30, 2 * PAV_X - 6.0, HALF_V - CY_Y1 - 7.0, mint)
    for k, (px0, px1) in enumerate(((-21.0, 1.5), (4.0, 22.0))):
        box(f"pv_{k}", (px0 + px1) / 2, 23.4, Z_NORTH_DECK + 0.30,
            Z_NORTH_DECK + 0.85, px1 - px0, 6.4, navy)
    for k, mx in enumerate((-26.0, -9.0, 26.0)):
        bevel(box(f"mech_nc_{k}", mx, 15.6, Z_NORTH_DECK, Z_NORTH_DECK + 1.8,
                  4.2, 2.6, white), width=0.08)

    # ---- the courtyard ------------------------------------------------------
    court = [(CY_X0, CY_Y0 + CY_CHAMFER), (CY_X0 + CY_CHAMFER, CY_Y0),
             (CY_X1 - CY_CHAMFER, CY_Y0), (CY_X1, CY_Y0 + CY_CHAMFER),
             (CY_X1, CY_Y1), (CY_X0, CY_Y1)]
    prism("court_floor", court, 0.0, 1.0, stone, top_mat=stone)
    # light glazed-brick liners on the four courtyard walls
    cw = 0.18
    box("court_liner_s", (CY_X0 + CY_X1) / 2, CY_Y0 + cw / 2, 1.0, Z_CORNICE,
        CY_X1 - CY_X0 - 2 * CY_CHAMFER, cw, sand)
    box("court_liner_n", (CY_X0 + CY_X1) / 2, CY_Y1 - cw / 2, 1.0, Z_CORNICE,
        CY_X1 - CY_X0, cw, sand)
    box("court_liner_w", CY_X0 + cw / 2, (CY_Y0 + CY_Y1) / 2 + CY_CHAMFER / 2,
        1.0, Z_CORNICE, cw, CY_Y1 - CY_Y0 - CY_CHAMFER, sand)
    box("court_liner_e", CY_X1 - cw / 2, (CY_Y0 + CY_Y1) / 2 + CY_CHAMFER / 2,
        1.0, Z_CORNICE, cw, CY_Y1 - CY_Y0 - CY_CHAMFER, sand)
    # courtyard glazing: VERTICAL slots on the courtyard's own bay rhythm.
    # Horizontal storey bands turned the light well into a striped billboard
    # from the app's three-quarter camera; vertical slots read as windows.
    for k in range(14):
        cx = CY_X0 + 5.0 + (CY_X1 - CY_X0 - 10.0) * k / 13.0
        box(f"court_slot_s_{k}", cx, CY_Y0 + cw - 0.04, 3.4, 20.0, 1.00, 0.24,
            glass)
        box(f"court_slot_n_{k}", cx, CY_Y1 - cw + 0.04, 3.4, 20.0, 1.00, 0.24,
            glass)
    for k in range(4):
        cy = CY_Y0 + 6.0 + (CY_Y1 - CY_Y0 - 12.0) * k / 3.0
        box(f"court_slot_w_{k}", CY_X0 + cw - 0.04, cy, 3.4, 20.0, 0.24, 1.00,
            glass)
        box(f"court_slot_e_{k}", CY_X1 - cw + 0.04, cy, 3.4, 20.0, 0.24, 1.00,
            glass)
    box("court_walk", (CY_X0 + CY_X1) / 2, (CY_Y0 + CY_Y1) / 2, 1.0, 1.06,
        CY_X1 - CY_X0 - 6.0, 5.0, sand)
    # 1.07, not 1.06: two coplanar paving slabs z-fight to a black patch.
    box("court_walk_x", 0.0, (CY_Y0 + CY_Y1) / 2, 1.0, 1.07, 5.0,
        CY_Y1 - CY_Y0 - 2.0, sand)
    for k, yy in enumerate((CY_Y0 + 4.0, CY_Y1 - 4.0)):
        box(f"court_bed_{k}", (CY_X0 + CY_X1) / 2, yy, 1.0, 1.35,
            CY_X1 - CY_X0 - 10.0, 3.6, mint)
    for k in range(8):
        tx = CY_X0 + 8.0 + (CY_X1 - CY_X0 - 16.0) * (k % 4) / 3.0
        ty = CY_Y0 + 4.0 if k < 4 else CY_Y1 - 4.0
        cylinder(f"court_tree_{k}", tx, ty, 1.35, 6.2, 2.2, mint, segs=8)
    bevel(box("court_bulkhead", CY_X1 - 3.4, 1.0, 1.0, 27.0, 6.0, 5.0, stone),
          width=0.10)

    # ---- the south colonnade ------------------------------------------------
    span = 2 * (HALF_U - SCOOP) - 4.0
    for k in range(COL_N):
        cx = -span / 2 + span * k / (COL_N - 1)
        cylinder(f"column_{k}", cx, -HALF_V - COL_PROUD + COL_R, Z_BELT,
                 Z_ORDER, COL_R, trim)
    # capitals and the balustrade band between the columns
    box("colon_balus", 0.0, -HALF_V - 0.55, Z_BELT, Z_BELT + 1.20,
        span + 2 * COL_R + 1.0, 1.10, trim)
    box("colon_abacus", 0.0, -HALF_V - 0.55, Z_ORDER - 0.45, Z_ORDER,
        span + 2 * COL_R + 1.0, 1.10, trim)

    # ---- pilaster strips on the other three fronts -------------------------
    def pilasters(prefix, axis, plane, lo, hi, n, skip=()):
        for k in range(n):
            t = (k + 0.5) / n
            p = lo + (hi - lo) * t
            if k in skip:
                continue
            if axis == "y":
                box(f"{prefix}_{k}", p, plane, Z_BELT, Z_FRIEZE, 1.30, 0.50,
                    trim)
            else:
                box(f"{prefix}_{k}", plane, p, Z_BELT, Z_FRIEZE, 0.50, 1.30,
                    trim)

    pilasters("pil_n", "y", HALF_V + 0.20, -HALF_U + 3.0, HALF_U - 3.0, 20)
    pilasters("pil_w", "x", -HALF_U - 0.20, -HALF_V + SCOOP + 1.0,
              HALF_V - 3.0, 11)
    pilasters("pil_e", "x", HALF_U + 0.20, -HALF_V + SCOOP + 1.0,
              HALF_V - 3.0, 11)
    for prefix, plane, lo, hi, axis in (
        ("balband_n", HALF_V + 0.28, -HALF_U, HALF_U, "y"),
        ("balband_w", -HALF_U - 0.28, -HALF_V + SCOOP, HALF_V, "x"),
        ("balband_e", HALF_U + 0.28, -HALF_V + SCOOP, HALF_V, "x"),
    ):
        if axis == "y":
            box(prefix, 0.0, plane, Z_BELT, Z_BELT + 1.20, hi - lo - 6.0, 0.56,
                trim)
        else:
            box(prefix, plane, (lo + hi) / 2, Z_BELT, Z_BELT + 1.20, 0.56,
                hi - lo - 6.0, trim)

    # ---- windows ------------------------------------------------------------
    # Five storeys of recessed panes on a single bay module. The attic band is
    # the night's supporting accent, so it uses the glow material.
    # A pane's outer face has to clear the wall it sits in, and the base stands
    # 0.25 m PROUD of the body, so each storey carries its own plane offset.
    # Getting this wrong buries the whole row - there are no booleans here.
    WD = 0.34  # pane depth
    ROWS = [(2.40, 5.00, O_BASE), (6.60, 9.90, O_BASE),
            (12.80, 16.20, O_BODY), (17.00, 20.20, O_BODY)]
    ATTIC_ROW = (24.30, 26.60, O_ATTIC)

    PROUD = 0.07  # 0.01 m of clearance was too tight: the pane only showed
    # where a rustication course happened to recess the wall behind it.

    def pane_plane(half, out_dir, off):
        """Centre plane putting the pane's outer face PROUD of its wall."""
        return out_dir * (half + off + PROUD - WD / 2)

    def wall_windows(prefix, axis, half, out_dir, positions, rows,
                     attic_positions=None):
        for k, p in enumerate(positions):
            for r, (z0, z1, off) in enumerate(rows):
                plane = pane_plane(half, out_dir, off)
                if axis == "y":
                    box(f"{prefix}_{k}_{r}", p, plane, z0, z1, 2.70, WD, glass)
                else:
                    box(f"{prefix}_{k}_{r}", plane, p, z0, z1, WD, 2.70, glass)
        if attic_positions is None:
            return
        z0, z1, off = ATTIC_ROW
        plane = pane_plane(half, out_dir, off)
        for k, p in enumerate(attic_positions):
            if axis == "y":
                glow_pane(f"{prefix}_a_{k}", p, plane, z0, z1, 2.70, WD,
                          out_dir, wglow, glass)
            else:
                glow_pane(f"{prefix}_a_{k}", plane, p, z0, z1, WD, 2.70,
                          out_dir, wglow, glass, axis="x")

    def spread(lo, hi, n):
        return [lo + (hi - lo) * (k + 0.5) / n for k in range(n)]

    s_pos = spread(-span / 2 - 1.4, span / 2 + 1.4, 18)
    s_low = [p for i, p in enumerate(s_pos) if i not in (8, 9)]
    wall_windows("win_s_low", "y", HALF_V, -1, s_low, ROWS[:2])
    wall_windows("win_s_up", "y", HALF_V, -1, s_pos, ROWS[2:],
                 attic_positions=s_pos)

    n_pos = spread(-HALF_U + 4.0, HALF_U - 4.0, 20)
    n_low = [p for i, p in enumerate(n_pos) if i != 10]
    wall_windows("win_n_low", "y", HALF_V, +1, n_low, ROWS[:2])
    wall_windows("win_n_up", "y", HALF_V, +1, n_pos, ROWS[2:],
                 attic_positions=[p for p in n_pos if abs(p) > PAV_X])

    # The west and east walls STOP at the concave corners, so their rhythm has
    # to start north of the scoop or the end bay floats in thin air.
    for side, sgn in (("w", -1), ("e", +1)):
        pos = spread(-HALF_V + SCOOP + 2.0, HALF_V - 4.0, 11)
        wall_windows(f"win_{side}", "x", HALF_U, sgn, pos, ROWS,
                     attic_positions=pos)

    # ---- the six arched entrances ------------------------------------------
    # Placed on the face of the rusticated base, which stands O_BASE proud of
    # the wall plane. Recessing them instead would bury them: there are no
    # booleans here, so anything behind that face never renders.
    for k, ex in enumerate((-5.6, 0.0, 5.6)):
        arched_opening(f"arch_s_{k}", ex, -(HALF_V + O_BASE), 0.0, -1.0, 1.20,
                       3.60, 5.60, 1.80, glass, gglow)
    arched_opening("arch_n", 0.0, HALF_V + O_BASE, 0.0, 1.0, 1.20, 3.60, 5.60,
                   1.80, glass, gglow)
    for sx in (-1, 1):
        arc = _scoop(sx, O_BASE)
        mid = arc[len(arc) // 2]
        nx, ny = sx / math.sqrt(2.0), -1 / math.sqrt(2.0)  # outward at 45 deg
        arched_opening(f"arch_c_{'w' if sx < 0 else 'e'}", mid[0], mid[1], nx,
                       ny, 1.20, 3.20, 5.20, 1.60, glass, gglow)


def recenter():
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        for v in o.data.vertices:
            for i in range(3):
                mn[i] = min(mn[i], v.co[i])
                mx[i] = max(mx[i], v.co[i])
    cx, cy = (mn.x + mx.x) / 2, (mn.y + mx.y) / 2
    dz = -mn.z
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        for v in o.data.vertices:
            v.co.x -= cx
            v.co.y -= cy
            v.co.z += dz
    lon = FOOT_LON + cx / (111320.0 * math.cos(math.radians(FOOT_LAT)))
    lat = FOOT_LAT + cy / 110540.0
    print(f"[build] recentered by ({-cx:.3f}, {-cy:.3f}, {dz:.3f}) m")
    print(f"[build] manifest anchor for the recentered origin: "
          f"[{lon:.7f}, {lat:.7f}]")


FOOT_LON = -122.4144797
FOOT_LAT = 37.7804306
TARGET_H = Z_CREST


def normalise_height():
    """Scale Z so the bbox top lands exactly on the verified crest."""
    mn = 1e9
    mx = -1e9
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        for v in o.data.vertices:
            mn = min(mn, v.co.z)
            mx = max(mx, v.co.z)
    h = mx - mn
    k = TARGET_H / h
    if abs(k - 1.0) < 1e-9:
        return
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        for v in o.data.vertices:
            v.co.z = (v.co.z - mn) * k
    print(f"[build] height {h:.4f} -> {TARGET_H:.4f} (x{k:.6f})")


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
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} "
          f"max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    recenter()
    normalise_height()
    report()

    blend = os.path.join(out, "50-united-nations-plaza.blend")
    glb = os.path.join(out, "50-united-nations-plaza.glb")
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
