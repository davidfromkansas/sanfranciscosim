"""Deterministic Blender build of the SF-SIM miniature 108-110 South Park.

    blender -b --python build_108_south_park.py -- [--out DIR]

Writes 108-south-park.blend and 108-south-park.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, cornice crest exactly
8.45 m.

Design (see REFERENCE.md for the sources behind every number):

* a 1914 two-storey wood-frame shop-and-flats building on the NORTH rim of South
  Park, built in the neighbourhood's pre-war Japanese quarter (the Gran Oriente
  National Register nomination names this address as the Omiya Shoten souvenir
  shop and Biwako Baths) and for the last forty years the South Park Cafe;
* 6.433 m of frontage against 29.750 m of depth, attached on BOTH flanks at a
  0.00 m party wall — 104-106 (11 m) north-east, 112 (6 m) south-west. Only the
  front, the rear on Taber Place, the roof and ~1.8 m of upper south-west wall
  above 112 are ever seen;
* the recognition is COLOUR before anything else: the whole building, front and
  back, is painted dark forest green, and on a rim of greige and pale grey it is
  the one dark object. The value is lifted one step from the real paint, which
  photographs near-black and would read as a hole in the row;
* the second cue is the gold sign fascia across the full frontage — the only
  saturated colour on the building, and this asset's equivalent of 165 South
  Park's blue gate. No lettering: the contract is flat colour and the letters are
  sub-pixel from the app's camera;
* the shopfront rhythm underneath it is green bulkhead / plate glass / two black
  awnings / a pale leaded-transom band, with the entry recessed at the
  south-west end;
* the roof is a LIGHT membrane, flat, with a line of four skylights and one low
  mechanical block.
  NOTHING on it rises above the cornice crest, so the loader's
  targetHeightM / measuredHeight scale lands at exactly 1.0;
* night state: the transom band is the hero glow (a warm strip the width of the
  shopfront), supported by one lit display bay and two lit upper windows. Glow
  surfaces are thin shells proud of the opaque glazing — the app renders _Glow in
  a separate layer that is ~12% alpha by day, so a primary surface must never be
  authored as glow.

Authoring frame: the lot is an exact parallelogram, so its area centroid and its
OBB centre coincide and recentre() moves nothing. Facade features use per-edge
frames (t along the edge, d outward, z up) built from that edge's two corners.
The building sits ~135 deg off the world axes, so the axis-aligned XY bounding
box is ~26 x 26 m even though the building is 6.4 x 29.8 m. That is expected,
not a scale error.
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
# Derived in docs/asset-plans/108-south-park.md 2.3 from OSM way/124884358.
DESIGN_ANCHOR = (-122.3944841, 37.7816792)

# Design footprint, metres east/north from DESIGN_ANCHOR. Four corners: the OSM
# polygon, which is the only one of the three available footprints consistent
# with the assessor's 21 x 100 ft lot (DataSF's LiDAR ring is buffered to
# 218.8 m2 over 14 vertices; see the plan's 2.15).
FOOTPRINT = [
    (-12.812, 8.252),    # A  rear south-west corner (Taber Place end)
    (-8.236, 12.773),    # B  rear north-east corner
    (12.812, -8.252),    # C  front north-east corner (against 104-106)
    (8.236, -12.773),    # D  front south-west corner (against 112)
]

REAR_A, REAR_B = FOOTPRINT[0], FOOTPRINT[1]
FRONT_C, FRONT_D = FOOTPRINT[2], FOOTPRINT[3]

# ---- vertical scheme -------------------------------------------------------
Z_BULK = 0.50           # shopfront bulkhead
Z_DISPLAY = 2.60        # head of the plate glass
Z_AWN0, Z_AWN1 = 2.62, 2.72
Z_TRAN0, Z_TRAN1 = 2.80, 3.40    # leaded transom band
Z_SIGN0, Z_SIGN1 = 3.50, 4.20    # gold fascia
Z_BELT = 4.36           # belt course between the storeys
Z_SILL_UP = 5.05
WIN_H_UP = 2.15
Z_MOD0 = 7.62           # modillion course under the cornice
Z_DECK = 7.80           # flat roof deck — MEASURED (DataSF LiDAR height median
                        # over 853 cells; OSM tags this way height=8)
Z_PARAPET = 8.02
Z_CREST = 8.45          # front cornice crest — the bbox top, and the manifest
                        # targetHeightM, so the loader's scale is exactly 1.0.
                        # Inferred: deck + ~0.65 m of boxed cornice. The LiDAR
                        # maximum of 11.88 m is party-wall bleed from the 11 m
                        # Gran Oriente next door; see REPORT.md and plan 2.15.

BASE_PROUD = 0.06
CORNICE_PROUD = 0.22
MOD_PROUD = 0.16
BELT_PROUD = 0.05
PILASTER_PROUD = 0.07
SIGN_PROUD = 0.10
TRANSOM_PROUD = 0.04
AWNING_PROUD = 0.80
PARAPET_W = 0.16

# ---- shopfront layout, metres along the frontage from the SOUTH-WEST corner --
ENTRY_T = (0.16, 1.21)
BAY_T = ((1.39, 3.72), (3.92, 6.27))
TRANSOM_T = (0.12, 6.31)
ENTRY_H = 2.45
GLASS_RECESS = 0.12

# ---- upper storey ----------------------------------------------------------
PILASTER_W = 0.34
WIN_W_UP = 1.05
WIN_T_UP = (1.515, 3.215, 4.915)
LIT_UP = (0, 2)          # which upper windows are lit at night

# ---- rear (Taber Place), metres along the rear edge from the NORTH-EAST corner
REAR_DOOR_W, REAR_DOOR_H = 3.60, 3.40
REAR_WIN_W, REAR_WIN_H = 0.85, 1.80
REAR_WIN_T = (2.71, 3.72)
Z_REAR_SILL = 5.10

# ---- roof ------------------------------------------------------------------
SKY_S = (0.23, 0.38, 0.53, 0.68)   # fraction of the depth, front -> rear
SKY_ALONG, SKY_ACROSS, SKY_H = 1.80, 1.25, 0.30
HATCH_S = 0.10
HATCH_SIDE, HATCH_H = 1.15, 0.45
MECH_S = 0.86
MECH_ALONG, MECH_ACROSS, MECH_H = 2.10, 1.70, 0.50
VENT_S = (0.79, 0.93)
VENT_SIDE, VENT_H, VENT_OFF = 0.26, 0.58, 1.45

BEVEL_W, BEVEL_SEG = 0.10, 2

PALETTE_HEX = {
    "Toy_verdigris": "587a66",  # the body, all four elevations, the parapet and
                                # the bulkhead. OFF-PALETTE and deliberate: the
                                # palette entry is #9fb8a8, too pale to stand
                                # for a building painted this dark. The style
                                # bible's SF exception — painted facades ARE
                                # saturated identity here — sanctions it, and
                                # 165 South Park set the precedent of keeping
                                # the palette NAME while overriding the hex so
                                # the contract check and the loader's merge path
                                # are unaffected. A WARN, not a FAIL.
                                #
                                # THE VALUE IS TWO STEPS UP FROM THE REAL PAINT
                                # AND THAT IS NOT NEGOTIABLE. First authored at
                                # #35493e, one step up, which looked correct in
                                # the Blender studio rig and rendered as a
                                # LITERAL BLACK SLAB in the app: the diorama
                                # lighting has low ambient, and at a linear
                                # luminance of 0.06 the green is gone, the
                                # cornice is gone and only the gold band and the
                                # skylights survive. Measured in a local build
                                # at 1 PM, 70 m out: the front wall came back
                                # rgb(5,5,6) against rgb(118,117,111) on the
                                # neighbour. #587a66 is ~3x the luminance and
                                # still leaves this the darkest building on the
                                # rim, which is the cue. Do not "correct" it
                                # back toward the photograph.
    "Toy_mint": "7f9d8b",       # cornice, modillions, belt course, window
                                # casings and sills. Also off-palette (#8fd0a8
                                # is a bright mint) and for the same reason: the
                                # real trim is green too, and a cream cornice
                                # would be a lie that happens to be in the
                                # palette. One step lighter than the body is
                                # what makes the crown and the belt read as
                                # articulation rather than as flat wall.
    "Toy_gold": "caa64a",       # THE SIGN FASCIA, and nothing else. Using it
                                # anywhere else would destroy the building's one
                                # saturated cue.
    "Toy_trim": "f3efe6",       # leaded transom band, skylight frames
    "Toy_ink": "3a3530",        # awnings, entry recess, rear door frame
    "Toy_glass": "2a4d73",
    "Toy_stone": "d9d2c2",      # the flat roof plane — a LIGHT membrane, which
                                # is what the 2026 satellite imagery actually
                                # shows on this row and what the neighbours read
                                # as in the app. First authored as Toy_roofd
                                # (#45454a) on the assumption that a flat SoMa
                                # roof is dark; in the local build that roof
                                # rendered black, swallowed the skylight line
                                # and made the whole asset a silhouette. Being
                                # wrong about the reference and wrong about the
                                # rendering happened to be the same mistake.
    "Toy_steel": "9aa0a6",      # roof mechanical block, skylight frames, roof
                                # hatch, rear louver — mid grey now reads
                                # against the light deck, where cream did not
    "Toy_trim_Glow": "f3efe6",  # the transom band at night — the hero glow
    "Toy_glass_Glow": "6f95b8",
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


def edge_frame(p_left, p_right):
    """Build a (t along the edge, d outward) frame from the two corners of one
    elevation, ordered as a viewer standing outside sees them left to right.
    The outward sense is resolved against the footprint centroid rather than
    assumed from the winding order."""
    t_hat = _unit(p_right[0] - p_left[0], p_right[1] - p_left[1])
    n_hat = (-t_hat[1], t_hat[0])
    mx = (p_left[0] + p_right[0]) / 2.0
    my = (p_left[1] + p_right[1]) / 2.0
    if (mx + n_hat[0] - CX) ** 2 + (my + n_hat[1] - CY) ** 2 < (mx - CX) ** 2 + (
        my - CY
    ) ** 2:
        n_hat = (-n_hat[0], -n_hat[1])
    length = math.hypot(p_right[0] - p_left[0], p_right[1] - p_left[1])
    heading = (math.degrees(math.atan2(n_hat[0], n_hat[1])) + 360.0) % 360.0

    def xy(t, d):
        return (
            p_left[0] + t_hat[0] * t + n_hat[0] * d,
            p_left[1] + t_hat[1] * t + n_hat[1] * d,
        )

    def rect(t0, t1, d0, d1):
        return [xy(t0, d0), xy(t1, d0), xy(t1, d1), xy(t0, d1)]

    return {"xy": xy, "rect": rect, "len": length, "heading": heading,
            "t": t_hat, "n": n_hat}


# The shopfront: a viewer on the park sees the south-west corner (D) on the left.
FRONT = edge_frame(FRONT_D, FRONT_C)
# Taber Place: a viewer in the alley sees the north-east corner (B) on the left.
REAR = edge_frame(REAR_B, REAR_A)

# Roof spine, front midpoint -> rear midpoint.
_FRONT_MID = ((FRONT_C[0] + FRONT_D[0]) / 2.0, (FRONT_C[1] + FRONT_D[1]) / 2.0)
_REAR_MID = ((REAR_A[0] + REAR_B[0]) / 2.0, (REAR_A[1] + REAR_B[1]) / 2.0)
_SPINE_LEN = math.hypot(_REAR_MID[0] - _FRONT_MID[0], _REAR_MID[1] - _FRONT_MID[1])
_SPINE = _unit(_REAR_MID[0] - _FRONT_MID[0], _REAR_MID[1] - _FRONT_MID[1])
_ACROSS = (-_SPINE[1], _SPINE[0])


def spine_rect(s, along, across):
    """Roof-plan rectangle centred at fraction `s` of the depth (0 = front)."""
    cx = _FRONT_MID[0] + _SPINE[0] * _SPINE_LEN * s
    cy = _FRONT_MID[1] + _SPINE[1] * _SPINE_LEN * s
    a, b = along / 2.0, across / 2.0
    return [
        (cx - _SPINE[0] * a - _ACROSS[0] * b, cy - _SPINE[1] * a - _ACROSS[1] * b),
        (cx + _SPINE[0] * a - _ACROSS[0] * b, cy + _SPINE[1] * a - _ACROSS[1] * b),
        (cx + _SPINE[0] * a + _ACROSS[0] * b, cy + _SPINE[1] * a + _ACROSS[1] * b),
        (cx - _SPINE[0] * a + _ACROSS[0] * b, cy - _SPINE[1] * a + _ACROSS[1] * b),
    ]


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
    adjacent edges. Used for the roof parapet's inner ring and for the proud
    perimeter bands (negative dist)."""
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
    """Closed band solid between `poly` and its inward offset — a parapet, or
    with a negative inset a proud belt course."""
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
    die the cornice a little way around the front corners so it does not stop
    dead at the party walls."""
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


def opening(name, frame, t0, t1, z0, z1, mats, sill=True, lit=False,
            recess=GLASS_RECESS):
    """A recessed glazed opening with a proud casing, on any elevation."""
    prism(
        f"{name}_fill",
        frame["rect"](t0, t1, -recess, 0.02),
        z0,
        z1,
        mats["Toy_glass"],
    )
    if sill:
        prism(
            f"{name}_sill",
            frame["rect"](t0 - 0.10, t1 + 0.10, 0.0, 0.11),
            z0 - 0.12,
            z0,
            mats["Toy_mint"],
        )
    if lit:
        prism(
            f"{name}_glow",
            frame["rect"](t0 + 0.06, t1 - 0.06, 0.02, 0.06),
            z0 + 0.06,
            z1 - 0.06,
            mats["Toy_glass_Glow"],
        )


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    mats = {name: make_material(name) for name in PALETTE_HEX}

    # ------------------------------------------------------------ main volume
    # Two storeys of painted clapboard on the surveyed lot. This prism IS the
    # building: both party flanks are blind, so everything else here is applied
    # to the two 6.4 m ends and the roof.
    prism("body", FOOTPRINT, 0.0, Z_DECK, mats["Toy_verdigris"],
          mat_top=mats["Toy_stone"])

    # ---------------------------------------------------------------- parapet
    # A low lip around the whole roof in the body colour. The roof is the
    # surface the app's camera actually sees, and without this it reads as a
    # bare cut face; with it the sliver has a designed edge that catches the sun
    # and throws a line of shade across the deck.
    rim("parapet", FOOTPRINT, PARAPET_W, Z_DECK, Z_PARAPET, mats["Toy_verdigris"])

    # ---------------------------------------------------------------- cornice
    # The only thing above the deck, and the only lift in the whole silhouette.
    # It sets the 8.45 m crest and must land on it exactly.
    prism(
        "cornice",
        FRONT["rect"](0.0, FRONT["len"], 0.0, CORNICE_PROUD),
        Z_DECK,
        Z_CREST,
        mats["Toy_mint"],
    )
    # Short returns only — a cornice die at each front corner. Longer than
    # ~0.3 m and they read as lumps sitting on the parapet rather than as the
    # end of the cornice.
    edge_return("cornice_return_ne", FRONT_C, REAR_B, 0.30, CORNICE_PROUD,
                Z_DECK, Z_CREST, mats["Toy_mint"])
    edge_return("cornice_return_sw", FRONT_D, REAR_A, 0.30, CORNICE_PROUD,
                Z_DECK, Z_CREST, mats["Toy_mint"])

    # ------------------------------------------------------------- modillions
    # Seven blocks under the cornice. Individually they are sub-pixel from the
    # app's camera; as a course they give the crown a serrated shadow line,
    # which is the one thing that distinguishes an Edwardian cornice from a
    # parapet at any distance.
    for k in range(7):
        mt = FRONT["len"] * (k + 0.5) / 7.0
        prism(
            f"modillion_{k}",
            FRONT["rect"](mt - 0.08, mt + 0.08, 0.0, MOD_PROUD),
            Z_MOD0,
            Z_DECK,
            mats["Toy_mint"],
        )

    # ------------------------------------------------------------ belt course
    # Runs the WHOLE perimeter, not just the two ends. 112 next door is only 6 m
    # tall, so the top ~1.8 m of the 29.8 m south-west flank is genuinely
    # visible in the city, and without this line that wall reads as a slab
    # rather than as the upper storey of a two-storey building.
    rim("belt", FOOTPRINT, -BELT_PROUD, Z_BELT - 0.06, Z_BELT, mats["Toy_mint"])

    # ================================================== front (South Park, SE)

    # Bulkhead under the glazing, proud so it casts its own line.
    prism(
        "bulkhead",
        FRONT["rect"](0.0, FRONT["len"], 0.0, BASE_PROUD),
        0.0,
        Z_BULK,
        mats["Toy_verdigris"],
    )

    # Recessed entry at the south-west end.
    #
    # THE RULE FOR EVERY DOORWAY IN THIS FILE: prism() makes a SOLID, so an ink
    # "recess" whose outer face reaches the wall plane is a filled black panel,
    # and any leaf authored *inside* it is invisible. Both this door and the
    # rear carriage door were built that way first and both rendered as flat
    # black rectangles. The working arrangement is 165 South Park's: the ink
    # block sits behind and slightly oversize so it shows only as a shadow
    # border, and the leaf sits PROUD of the wall in front of it.
    prism(
        "entry_reveal",
        FRONT["rect"](ENTRY_T[0] - 0.14, ENTRY_T[1] + 0.14, -0.30, 0.01),
        0.0,
        ENTRY_H + 0.14,
        mats["Toy_ink"],
    )
    prism(
        "entry_leaf",
        FRONT["rect"](ENTRY_T[0], ENTRY_T[1], 0.0, 0.05),
        0.0,
        ENTRY_H,
        mats["Toy_ink"],
    )
    # A light casing round the leaf. Without it the door is a dark rectangle on
    # a dark wall and disappears; with it the entry is a drawn object, which is
    # what a viewer needs in order to find the way in. The pale transom band
    # already runs across the top of this bay, so no separate fanlight.
    for jt0, jt1 in ((ENTRY_T[0] - 0.14, ENTRY_T[0]),
                     (ENTRY_T[1], ENTRY_T[1] + 0.14)):
        prism(
            f"entry_jamb_{jt0:.2f}",
            FRONT["rect"](jt0, jt1, 0.0, 0.09),
            0.0,
            ENTRY_H + 0.14,
            mats["Toy_mint"],
        )
    prism(
        "entry_head",
        FRONT["rect"](ENTRY_T[0] - 0.14, ENTRY_T[1] + 0.14, 0.0, 0.09),
        ENTRY_H,
        ENTRY_H + 0.14,
        mats["Toy_mint"],
    )

    # Two plate-glass display bays. The south-west bay is the one lit at night.
    for i, (t0, t1) in enumerate(BAY_T):
        opening(f"display_{i}", FRONT, t0, t1, Z_BULK, Z_DISPLAY, mats,
                sill=False, lit=(i == 0))
        # Flat black awning over each bay — not fabric, a clean slab. These are
        # the ground floor's whole contribution to the silhouette.
        prism(
            f"awning_{i}",
            FRONT["rect"](t0 - 0.06, t1 + 0.06, 0.0, AWNING_PROUD),
            Z_AWN0,
            Z_AWN1,
            mats["Toy_ink"],
        )

    # The leaded transom band, collapsed from two oval-motif panels to one pale
    # stripe running the full frontage. Light band under gold band over black
    # awnings is the rhythm that survives to thumbnail size; the ovals do not.
    prism(
        "transom",
        FRONT["rect"](TRANSOM_T[0], TRANSOM_T[1], 0.0, TRANSOM_PROUD),
        Z_TRAN0,
        Z_TRAN1,
        mats["Toy_trim"],
    )
    # Hero night glow: a warm shell proud of the transom band.
    prism(
        "transom_glow",
        FRONT["rect"](TRANSOM_T[0] + 0.06, TRANSOM_T[1] - 0.06,
                      TRANSOM_PROUD, TRANSOM_PROUD + 0.04),
        Z_TRAN0 + 0.06,
        Z_TRAN1 - 0.06,
        mats["Toy_trim_Glow"],
    )

    # The gold sign fascia — the building's one saturated cue, full frontage.
    prism(
        "sign",
        FRONT["rect"](0.0, FRONT["len"], 0.0, SIGN_PROUD),
        Z_SIGN0,
        Z_SIGN1,
        mats["Toy_gold"],
    )

    # Upper storey: three tall windows in a field between two flat pilasters.
    prism(
        "pilaster_sw",
        FRONT["rect"](0.0, PILASTER_W, 0.0, PILASTER_PROUD),
        Z_BELT,
        Z_MOD0,
        mats["Toy_verdigris"],
    )
    prism(
        "pilaster_ne",
        FRONT["rect"](FRONT["len"] - PILASTER_W, FRONT["len"], 0.0, PILASTER_PROUD),
        Z_BELT,
        Z_MOD0,
        mats["Toy_verdigris"],
    )
    for i, t in enumerate(WIN_T_UP):
        opening(
            f"upper_{i}",
            FRONT,
            t - WIN_W_UP / 2.0,
            t + WIN_W_UP / 2.0,
            Z_SILL_UP,
            Z_SILL_UP + WIN_H_UP,
            mats,
            lit=(i in LIT_UP),
        )

    # ================================================ rear (Taber Place, NW)
    # The alley is 6 m wide and the app's camera looks over it, so this
    # elevation gets exactly two events plus a vent: the multi-pane carriage
    # door that fills most of the ground floor, and the paired sash window
    # above it.
    rd0 = (REAR["len"] - REAR_DOOR_W) / 2.0
    rd1 = rd0 + REAR_DOOR_W
    # Same arrangement as the front entry (see the rule there): oversize ink
    # block behind, green leaf proud in front of it, glazing proud of the leaf.
    # The result is a thin shadow border around a green frame carrying one big
    # pane, which is what the real multi-light carriage door reads as.
    prism(
        "rear_door_reveal",
        REAR["rect"](rd0 - 0.10, rd1 + 0.10, -0.22, 0.01),
        0.0,
        REAR_DOOR_H + 0.10,
        mats["Toy_ink"],
    )
    prism(
        "rear_door_leaf",
        REAR["rect"](rd0, rd1, 0.0, 0.05),
        0.0,
        REAR_DOOR_H,
        mats["Toy_verdigris"],
    )
    prism(
        "rear_door_glass",
        REAR["rect"](rd0 + 0.17, rd1 - 0.17, 0.05, 0.08),
        1.30,
        REAR_DOOR_H - 0.17,
        mats["Toy_glass"],
    )
    prism(
        "rear_louver",
        REAR["rect"](REAR["len"] / 2.0 - 0.36, REAR["len"] / 2.0 + 0.36, 0.0, 0.07),
        REAR_DOOR_H + 0.24,
        REAR_DOOR_H + 0.58,
        mats["Toy_steel"],
    )
    for i, t in enumerate(REAR_WIN_T):
        opening(
            f"rear_win_{i}",
            REAR,
            t - REAR_WIN_W / 2.0,
            t + REAR_WIN_W / 2.0,
            Z_REAR_SILL,
            Z_REAR_SILL + REAR_WIN_H,
            mats,
        )

    # =========================================================== roof surface
    # Four skylights in a line down the spine — the graphic repetition the style
    # bible asks of a roof this plain (s.10) — with a pale stair hatch near the
    # street end, one low mechanical block in the rear third and two vent
    # stacks flanking it. The first build put four small skylights in the middle
    # third only and left 8 m of blank deck at the street end, which is exactly
    # the end the app's camera looks at. Everything here is sized up from
    # reality (s.9) and NOTHING reaches the 8.45 m crest.
    for i, sf in enumerate(SKY_S):
        prism(
            f"skylight_{i}",
            spine_rect(sf, SKY_ALONG, SKY_ACROSS),
            Z_DECK,
            Z_DECK + SKY_H,
            mats["Toy_steel"],
            mat_top=mats["Toy_glass"],
        )
    prism(
        "roof_hatch",
        spine_rect(HATCH_S, HATCH_SIDE, HATCH_SIDE),
        Z_DECK,
        Z_DECK + HATCH_H,
        mats["Toy_steel"],
    )
    prism(
        "mech",
        spine_rect(MECH_S, MECH_ALONG, MECH_ACROSS),
        Z_DECK,
        Z_DECK + MECH_H,
        mats["Toy_steel"],
    )
    for i, sf in enumerate(VENT_S):
        poly = spine_rect(sf, VENT_SIDE, VENT_SIDE)
        off = (_ACROSS[0] * VENT_OFF * (1 if i % 2 == 0 else -1),
               _ACROSS[1] * VENT_OFF * (1 if i % 2 == 0 else -1))
        prism(
            f"vent_{i}",
            [(x + off[0], y + off[1]) for x, y in poly],
            Z_DECK,
            Z_DECK + VENT_H,
            mats["Toy_steel"],
        )

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.10/2. Window fills, sills, modillions and glow shells are small and
    # numerous — a token softening or none at all is what keeps this under cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")) or obj.name.startswith("modillion"):
            continue
        if obj.name.endswith("_sill") or obj.name.startswith(("belt", "transom",
                                                              "sign")):
            bevel(obj, width=0.03, segments=1)
        else:
            bevel(obj)

    recentre()
    return scene


# Metres east / north from DESIGN_ANCHOR to the model's XY bbox centre, filled
# in by recentre(). The lot is a parallelogram so the two coincide to within the
# proud facade bands, and this shift is a few centimetres rather than the metre
# 165 South Park's bent wedge needed — but it is still carried into the anchor
# so the building lands on its real footprint (AGENTS rule 5).
ANCHOR_SHIFT = [0.0, 0.0]


def recentre():
    """Move the model so its XY bounding-box centre is the origin."""
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
    print(f"[build] frontage: {FRONT['len']:.3f} m   depth: {_SPINE_LEN:.3f} m")
    print(f"[build] design (area-centroid) anchor: {DESIGN_ANCHOR}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 4) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] front elevation faces: {FRONT['heading']:.2f} deg true")
    print(f"[build] rear elevation faces: {REAR['heading']:.2f} deg true")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "108-south-park.blend")
    glb = os.path.join(out, "108-south-park.glb")
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
