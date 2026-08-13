"""Deterministic Blender build of the SF-SIM miniature 165-167 South Park.

    blender -b --python build_165_south_park.py -- [--out DIR]

Writes 165-south-park.blend and 165-south-park.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, cornice crest exactly
9.0 m.

Design (see REFERENCE.md for the sources behind every number):

* a 1908 two-storey, three-unit wooden flats building on the south rim of South
  Park, the oval that is San Francisco's oldest planned residential square;
* the recognition rests on the PROPORTION: 6.2 m of frontage against 24 m of
  depth. From the app's aerial camera the building is a pale sliver that narrows
  and bends as it runs back from the oval, and nothing else about it is
  distinctive at that distance;
* the one close-range cue is the vivid blue steel gate at the east edge of the
  frontage, closing a full-height passage to the flats. It is the only saturated
  colour on the block and the single feature separating this building from 171
  next door, which wears identical siding;
* the facade is FLAT — no projecting bay window, which is unusual for a San
  Francisco flats building and is a positive fact about this one. A dark
  stone-tile base band (2014) grounds the pale lap siding;
* the roof is flat, with the cornice lifting to 9.0 m at the street end only;
* night state: two lit windows on the upper storey plus a thin warm spill in the
  gate recess, which is what tells the eye at night that the gate is a passage
  and not a painted panel. Glow surfaces are thin shells proud of the opaque
  glazing — the app renders _Glow in a separate layer that is ~12% alpha by day,
  so a primary surface must never be authored as glow.

Authoring frame: the plan polygon is authored directly in world metres relative
to the manifest anchor, because the lot BENDS (front block ~157 deg, rear block
135.3 deg) and no single local axis describes it. Facade features use a front
frame (t along the frontage, d outward, z up) built from the two front corners.
The building sits ~145 deg off the world axes, so the axis-aligned XY bounding
box is ~18.9 x 21.7 m even though the building is 6.2 x 24.0 m. That is
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

# Area centroid of the design footprint = the MANIFEST anchor before recentring.
# Derived in docs/asset-plans/165-south-park.md 2.3 from the surveyed DataSF
# parcel 3775028 truncated at the LiDAR footprint's rear extent (24.0 m).
DESIGN_ANCHOR = (-122.3943860, 37.7808670)

# Design footprint, metres east/north from DESIGN_ANCHOR. Six corners: the
# surveyed lot, with the eleven-segment street arc collapsed to its chord (the
# arc's bulge is 0.14 m — below the bevel radius, so modelling it would be
# false precision).
FOOTPRINT = [
    (10.319, -8.677),   # rear-east corner
    (3.748, -2.089),    # east party line, bend
    (-2.481, 10.025),   # front-east corner (the gate end)
    (-8.587, 8.919),    # front-west corner
    (-6.149, 1.807),    # west party line, bend
    (7.293, -11.671),   # rear-west corner
]

FRONT_WEST = FOOTPRINT[3]
FRONT_EAST = FOOTPRINT[2]

Z_BASE = 0.90           # dark stone-tile band, installed 2014
Z_FLOOR_LINE = 4.30     # shadow groove between the storeys
Z_DECK = 8.55           # flat roof deck — MEASURED (DataSF LiDAR height median
                        # over 433 cells, sd 0.65 m; for a flat roof the median
                        # is the deck)
Z_CREST = 9.00          # front cornice crest — the bbox top, and the manifest
                        # targetHeightM, so the loader's scale is exactly 1.0.
                        # Inferred: deck + ~0.45 m cornice. The LiDAR maximum is
                        # 9.90 m and is unexplained; see REPORT.md and the
                        # plan's 2.15.

BASE_PROUD = 0.06
CORNICE_PROUD = 0.15
CORNICE_D = Z_CREST - Z_DECK

WIN_W, WIN_H = 1.00, 1.70
WIN_RECESS = 0.12
Z_SILL_LO, Z_SILL_HI = 1.50, 5.10
# Two bays per storey on the 4.9 m of frontage west of the gate.
WIN_T = (1.35, 3.35)

GATE_W, GATE_H = 1.30, 2.60
GATE_PROUD = 0.07       # the leaf sits ON the siding plane, not inside the
                        # passage. Recessed 0.10 m (the first build) it fell
                        # into its own shadow and rendered as a black doorway —
                        # the one saturated cue on the building disappeared.
                        # See REPORT.md.
GATE_RECESS = 0.55      # the passage behind it reads as a hole, not a panel
GATE_T1 = 6.05          # east end of the gate, measured from the west corner

PARAPET_H = 0.17        # low lip around the whole roof, in the siding colour.
                        # Without it the flat roof reads as a bare cut face from
                        # the app's camera, which is the view that matters.
PARAPET_W = 0.16

DOOR_W, DOOR_H = 1.00, 2.10

BEVEL_W, BEVEL_SEG = 0.10, 2

PALETTE_HEX = {
    "Toy_steel": "a9b5bd",   # the lap siding, all four elevations. OFF-PALETTE
                             # and deliberate: the nearest palette entry is
                             # Toy_steel #9aa0a6, which rendered dead and
                             # noticeably darker than the real building in the
                             # first aerial review. #a9b5bd is the building's
                             # actual desaturated blue-gray, and the style
                             # bible's SF exception — painted residential rows
                             # keep their tinted facades — sanctions it. A WARN,
                             # not a FAIL; recorded in REPORT.md. The material
                             # keeps the Toy_steel NAME so the contract check
                             # and the loader's merge path are unaffected.
    "Toy_ink": "3a3530",     # stone base band, gate recess, rear door
    "Toy_trim": "f3efe6",    # cornice, window trim and sills
    "Toy_glass": "2a4d73",
    "Toy_sky": "6db3d9",     # THE GATE, and nothing else. Using it anywhere
                             # else would destroy the building's only cue.
    "Toy_roofd": "45454a",   # the flat roof plane
    "Toy_glass_Glow": "6f95b8",
    "Toy_trim_Glow": "f3efe6",   # the passage lamp over the gate
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

# Front frame: t runs along the frontage west -> east, d runs outward (away from
# the lot). The outward sense is resolved against the footprint centroid rather
# than assumed from the winding order.
_FT = _unit(FRONT_EAST[0] - FRONT_WEST[0], FRONT_EAST[1] - FRONT_WEST[1])
_FN = (-_FT[1], _FT[0])
if (FRONT_WEST[0] + _FN[0] - CX) ** 2 + (FRONT_WEST[1] + _FN[1] - CY) ** 2 < (
    FRONT_WEST[0] - CX
) ** 2 + (FRONT_WEST[1] - CY) ** 2:
    _FN = (-_FN[0], -_FN[1])

FRONT_LEN = math.hypot(FRONT_EAST[0] - FRONT_WEST[0], FRONT_EAST[1] - FRONT_WEST[1])
FRONT_HEADING = (math.degrees(math.atan2(_FN[0], _FN[1])) + 360.0) % 360.0


def front_xy(t, d):
    """Front frame (t along the frontage, d outward) -> world (x east, y north)."""
    return (
        FRONT_WEST[0] + _FT[0] * t + _FN[0] * d,
        FRONT_WEST[1] + _FT[1] * t + _FN[1] * d,
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
    a third of the object's thinnest dimension: window fills, sills and glow
    shells are only 40-120 mm thick and a flat bevel on those collapses opposing
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
    adjacent edges. Used for the roof parapet's inner ring."""
    n = len(poly)
    lines = []
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        d = _unit(b[0] - a[0], b[1] - a[1])
        nrm = (-d[1], d[0])
        # inward = toward the centroid
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
    """Closed band solid between `poly` and its inward offset — a parapet."""
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
        faces.append((O0 + i, O0 + j, O1 + j, O1 + i))   # outer wall
        faces.append((I0 + i, I0 + j, I1 + j, I1 + i))   # inner wall
        faces.append((O0 + i, O0 + j, I0 + j, I0 + i))   # bottom
        faces.append((O1 + i, O1 + j, I1 + j, I1 + i))   # top
    return new_mesh(name, verts, faces, [mat])


def edge_return(name, a, b, length, thickness, z0, z1, mat):
    """A short proud band running from corner `a` along the edge a->b, used to
    wrap the base course and the cornice a little way around the front corners
    so they do not stop dead at the party walls."""
    d = _unit(b[0] - a[0], b[1] - a[1])
    nrm = (-d[1], d[0])
    if (a[0] + nrm[0] - CX) ** 2 + (a[1] + nrm[1] - CY) ** 2 < (a[0] - CX) ** 2 + (
        a[1] - CY
    ) ** 2:
        nrm = (-nrm[0], -nrm[1])
    p0 = a
    p1 = (a[0] + d[0] * length, a[1] + d[1] * length)
    poly = [
        p0,
        p1,
        (p1[0] + nrm[0] * thickness, p1[1] + nrm[1] * thickness),
        (p0[0] + nrm[0] * thickness, p0[1] + nrm[1] * thickness),
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


def window(name, t_centre, z_sill, mats, lit=False):
    """A recessed opening on the street elevation, with a proud sill and trim."""
    t0, t1 = t_centre - WIN_W / 2.0, t_centre + WIN_W / 2.0
    prism(
        f"{name}_fill",
        front_rect(t0, t1, -WIN_RECESS, 0.02),
        z_sill,
        z_sill + WIN_H,
        mats["Toy_glass"],
    )
    prism(
        f"{name}_sill",
        front_rect(t0 - 0.10, t1 + 0.10, 0.0, 0.10),
        z_sill - 0.12,
        z_sill,
        mats["Toy_trim"],
    )
    if lit:
        prism(
            f"{name}_glow",
            front_rect(t0 + 0.05, t1 - 0.05, 0.02, 0.06),
            z_sill + 0.05,
            z_sill + WIN_H - 0.05,
            mats["Toy_glass_Glow"],
        )


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    mats = {name: make_material(name) for name in PALETTE_HEX}

    # ------------------------------------------------------------ main volume
    # The surveyed lot, two storeys of lap siding. This prism IS the building:
    # the party flanks are blind and the rear is barely seen, so everything else
    # here is applied to the street elevation.
    prism("body", FOOTPRINT, 0.0, Z_DECK, mats["Toy_steel"], mat_top=mats["Toy_roofd"])

    # -------------------------------------------------------------- base band
    # Dark stone tile, 2014, proud of the siding plane so it casts its own line.
    # It runs the WHOLE perimeter rather than the street elevation alone: the
    # real tile is a facade treatment, but every building has a base course, and
    # a 0.6 m return that stops dead at the corner reads as a black box stuck to
    # the wall (first aerial review). Wrapping it also gives the terrain seam
    # somewhere to hide.
    rim(
        "base_band",
        FOOTPRINT,
        -BASE_PROUD,   # negative inset = proud of the wall
        0.0,
        Z_BASE,
        mats["Toy_ink"],
    )

    # ---------------------------------------------------------------- parapet
    # A low lip around the whole roof in the siding colour. The roof is the
    # surface the app's camera actually sees, and without this it reads as a
    # bare cut face; with it the sliver has a designed edge that catches the
    # sun and throws a line of shade across the deck.
    rim("parapet", FOOTPRINT, PARAPET_W, Z_DECK, Z_DECK + PARAPET_H,
        mats["Toy_steel"])

    # ---------------------------------------------------------------- cornice
    # The only thing above the deck, and the only lift in the whole silhouette.
    # It sets the 9.0 m crest and must land on it exactly.
    prism(
        "cornice",
        front_rect(-0.04, FRONT_LEN + 0.04, 0.0, CORNICE_PROUD),
        Z_DECK,
        Z_CREST,
        mats["Toy_trim"],
    )
    # Short returns only — a cornice die at each front corner. Longer than
    # ~0.3 m and they read as lumps sitting on the parapet rather than as the
    # end of the cornice.
    edge_return("cornice_return_e", FRONT_EAST, FOOTPRINT[1], 0.30, CORNICE_PROUD,
                Z_DECK, Z_CREST, mats["Toy_trim"])
    edge_return("cornice_return_w", FRONT_WEST, FOOTPRINT[4], 0.30, CORNICE_PROUD,
                Z_DECK, Z_CREST, mats["Toy_trim"])

    # ------------------------------------------------------------- floor line
    # A shallow proud band is all the horizontality the lap siding gets:
    # modelling boards would spend the whole triangle budget on a 20 px facade.
    # It runs the WHOLE perimeter, not just the street elevation. The party
    # flanks are blind and 24 m long, and 159 next door is only 5.5 m tall, so
    # the upper half of the east flank is genuinely visible in the city — without
    # this line that wall reads as a slab rather than as two storeys.
    rim(
        "floor_line",
        FOOTPRINT,
        -0.04,   # negative inset = the band stands 0.04 m PROUD of the wall
        Z_FLOOR_LINE - 0.05,
        Z_FLOOR_LINE,
        mats["Toy_trim"],
    )

    # ---------------------------------------------------------------- windows
    # Two bays per storey on the 4.9 m of frontage west of the gate. The count
    # is a designed rhythm for a 6.2 m elevation, not a reading off a photograph
    # (the single Street View pano is partly behind a street tree) — see the
    # plan's 2.15.
    for i, t in enumerate(WIN_T):
        window(f"win_lo_{i}", t, Z_SILL_LO, mats)
        window(f"win_hi_{i}", t, Z_SILL_HI, mats, lit=True)

    # ------------------------------------------------------------------- gate
    # The building's one identity cue. Modelled as a solid slab with shallow
    # vertical grooving rather than real pickets: the gaps are sub-pixel at city
    # scale and would only add triangles and alias. Slightly wider than the real
    # 1.1 m so it survives at thumbnail size.
    t0, t1 = GATE_T1 - GATE_W, GATE_T1
    prism(
        "gate_recess",
        front_rect(t0 - 0.06, t1 + 0.06, -GATE_RECESS, 0.01),
        0.0,
        GATE_H + 0.12,
        mats["Toy_ink"],
    )
    prism(
        "gate",
        front_rect(t0, t1, 0.0, GATE_PROUD),
        0.0,
        GATE_H,
        mats["Toy_sky"],
    )
    for k in range(4):
        gt = t0 + GATE_W * (k + 0.5) / 4.0
        prism(
            f"gate_bar_{k}",
            front_rect(gt - 0.05, gt + 0.05, GATE_PROUD, GATE_PROUD + 0.04),
            0.12,
            GATE_H - 0.12,
            mats["Toy_sky"],
        )
    # Supporting night accent: the passage lamp above the gate. The first build
    # put a glow shell on the back wall of the recess, which the opaque gate leaf
    # in front of it hid completely — the accent rendered as nothing at all. A
    # lamp over the gate is both visible and true: Street View shows a fixture
    # there. See REPORT.md.
    gc = (t0 + t1) / 2.0
    prism(
        "gate_lamp_glow",
        front_rect(gc - 0.16, gc + 0.16, 0.02, 0.08),
        GATE_H + 0.26,
        GATE_H + 0.46,
        mats["Toy_trim_Glow"],
    )

    # -------------------------------------------------------------- rear door
    # The rear elevation faces a light well and is seen only from directly
    # above. One recessed door, and nothing else.
    ra, rb = FOOTPRINT[0], FOOTPRINT[5]
    rd = _unit(rb[0] - ra[0], rb[1] - ra[1])
    rlen = math.hypot(rb[0] - ra[0], rb[1] - ra[1])
    rn = (-rd[1], rd[0])
    if (ra[0] + rn[0] - CX) ** 2 + (ra[1] + rn[1] - CY) ** 2 < (ra[0] - CX) ** 2 + (
        ra[1] - CY
    ) ** 2:
        rn = (-rn[0], -rn[1])
    c0 = rlen / 2.0 - DOOR_W / 2.0
    door = []
    for s, dd in ((c0, 0.02), (c0 + DOOR_W, 0.02), (c0 + DOOR_W, -0.14), (c0, -0.14)):
        door.append((ra[0] + rd[0] * s + rn[0] * dd, ra[1] + rd[1] * s + rn[1] * dd))
    prism("rear_door", door, 0.0, DOOR_H, mats["Toy_ink"])

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.10/2. Window fills, sills, gate bars and glow shells are small and
    # numerous — a token softening or none at all is what keeps this under cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")) or "_bar_" in obj.name:
            continue
        if obj.name.endswith("_sill") or obj.name.startswith("floor_line"):
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

    The lot is a bent wedge, so its bbox centre is ~1.2 m from its area
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

    blend = os.path.join(out, "165-south-park.blend")
    glb = os.path.join(out, "165-south-park.glb")
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
