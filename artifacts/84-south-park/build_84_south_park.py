"""Deterministic Blender build of the SF-SIM miniature 84 South Park.

    blender -b --python build_84_south_park.py -- [--out DIR]

Writes 84-south-park.blend and 84-south-park.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, pergola crest exactly
13.20 m.

Design (see REFERENCE.md for the sources behind every number):

* a 1907 sliver on the north-west rim of the South Park oval, occupying the whole
  of a 22.94 ft x 98.66 ft lot — 6.99 m of frontage against 30.07 m of depth, a
  4.3:1 proportion and the thinnest building in this set;
* it is THREE storeys, not the two the 2025 assessor roll still records. A
  1992-12-04 permit ($361,782, "vertical addition") took it 2 -> 3 and every
  permit since is filed at 3. The same campaign re-fronted it;
* the recognition rests on COLOUR and on the ROOF, because nothing else survives
  the app's camera. Both party walls are blind — 76-82 South Park on the
  north-east is 1.6 m taller and 86-96 on the south-west is only 0.2 m shorter —
  so the only things ever seen are the street front, the rear, and the top;
* the street front is TWO UNEQUAL BAYS: a wide south-west bay carrying a
  ground-floor living green wall under a pale projecting second-floor box, and a
  narrow north-east bay that is one tall recessed slot containing the rust-red
  entrance door and two terrace rails;
* the building steps DOWN at the back: the rear 7.2 m is a two-storey wing capped
  at 8.10 m with a pale planted roof terrace and a glazed bay at the very end.
  DataSF LiDAR sees this as an 8.18 m minimum against an 11.36 m median on the
  main footprint, plus a separate 16 m2 footprint at a 7.99 m median;
* the roof is the whole silhouette: a parapet at 11.50 m, a run of four skylights
  down the middle, three more along the north-east edge nearer the street, a
  planted roof garden with a small tree and a stair bulkhead at the street end,
  and — standing 2.0 m proud of the parapet and setting the bounding-box top — an
  open slatted PERGOLA. See REPORT.md for why the pergola is read as real and
  what it costs if it is not;
* night state: two windows lit, unevenly — this is one family's house on a quiet
  oval, and a fully lit front would read as an office — plus a warm spill in the
  entrance slot. Glow surfaces are thin shells proud of the opaque glazing: the
  app renders _Glow in a separate layer that reads ~12% alpha per surface by day,
  so a primary surface must never be authored as glow and a shell must never be
  closed around one.

Authoring frame: the footprint is a clean rectangle at 45 deg to the world axes,
so everything is placed through two local frames built from it — a FRONT frame
(t along the 6.99 m street frontage, d outward at 135.18 deg) and a LONG frame
(s from the street edge toward the rear, u across from the south-west party
wall). Because the building sits at 45 deg, the axis-aligned XY bounding box is
~26.2 x 26.2 m even though the building is 6.99 x 30.07 m. That is expected, not
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

# Area centroid of the DataSF parcel 3775055 — a clean surveyed rectangle, and
# the tie-breaker between the OSM trace and the LiDAR footprint, which disagree
# by 2.7 m along the long axis. See the plan's 2.3.
DESIGN_ANCHOR = (-122.3940683, 37.7819798)

# Lot, from the DataSF parcel polygon: 22.94 ft x 98.66 ft, fully occupied.
# The assessor roll's lot_area (2,242.5 sq ft) corroborates it to ~1%.
FRONTAGE = 6.99
DEPTH = 30.07
AXIS_BEARING = 315.18     # street -> rear (north-west)
FRONT_BEARING = 135.18    # the street elevation faces south-east, onto the oval

Z_DECK = 11.20            # main roof deck — MEASURED (DataSF LiDAR height median
                          # 11.36 m over 746 cells; majority 11.49 m). OSM
                          # height=11 agrees with the deck, not the crest.
Z_PARAPET = 11.50         # parapet crest. If the pergola is ever disproved this
                          # becomes the bounding-box top and targetHeightM.
Z_PERGOLA = 13.20         # pergola crest = the DataSF LiDAR maximum (13.24 m),
                          # read as the trellis over the roof deck. THE BBOX TOP
                          # and the manifest targetHeightM, so the loader's scale
                          # is exactly 1.0. See REPORT.md risk 1.

S_REAR_WING = 22.90       # the main volume runs s 0 -> 22.90; behind it the
Z_REAR_DECK = 8.10        # two-storey rear wing is capped at 8.10 m with a
Z_REAR_PARAPET = 8.35     # planted terrace, matching the LiDAR 8.18 m minimum.

# Storey lines, inferred from the three-storey conversion and the 11.20 m deck.
Z_FLOOR2 = 3.90
Z_FLOOR3 = 7.55

BEVEL_W = 0.10
BEVEL_SEG = 2

ANCHOR_SHIFT = [0.0, 0.0]


PALETTE_HEX = {
    "Toy_slate": "7b9298",      # the whole body. OFF-PALETTE and deliberate:
                                # the nearest palette entry, Toy_verdigris
                                # (#9fb8a8), was built first and the aerial
                                # review killed it — it read as pale sage and
                                # lost the one cue that makes this building
                                # worth modelling, which is being the only
                                # tinted facade in a row of cream and taupe.
                                # #6d8188 was the next attempt — the mid-dark
                                # slate blue-green the January 2025 Street View
                                # shows — and it was right in the Blender rig and
                                # too dark IN THE APP, which is the only judge
                                # that counts: the app's flatter lighting crushed
                                # it toward near-black on a facade that is in
                                # shade for most of the afternoon. Shipped one
                                # step lighter at #7b9298, measured against the
                                # cream procedural neighbours in a local build.
                                # The style bible's SF exception covers painted
                                # residential facades and sf-asset-check scores
                                # an off-palette colour as a WARN, not a FAIL.
                                # See REPORT.md correction 1.
    "Toy_trim": "f3efe6",       # parapet, the projecting second-floor box,
                                # window surrounds, skylight kerbs, green-wall
                                # frame
    "Toy_stone": "d9d2c2",      # the roof deck membrane and the rear terrace
    "Toy_mint": "8fd0a8",       # the ground-floor living green wall, the roof
                                # and terrace planting, the tree canopy
    "Toy_ink": "3a3530",        # the pergola, the roof bulkhead, the terrace
                                # rails
    "Toy_red": "c4453c",        # the entrance door — the one saturated accent
    "Toy_rust": "a86444",       # the roof tree's trunk
    "Toy_roofd": "45454a",      # the entrance/terrace slot's back plane
    "Toy_steel": "9aa0a6",      # the rear elevation
    "Toy_glass": "2a4d73",      # all windows, skylight tops, the rear glazed bay
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


FRONT = Face(STREET_SW, STREET_NE)   # the street elevation, faces 135.18 deg
REAR = Face(REAR_NE, REAR_SW)        # the rear, faces 315.18 deg
FLANK_SW = Face(REAR_SW, STREET_SW)  # toward 86-96, faces 225.18 deg
FLANK_NE = Face(STREET_NE, REAR_NE)  # toward 76-82, faces 45.18 deg


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
    a third of the object's thinnest dimension: window fills, rails, pergola
    beams and glow shells are only 60-160 mm thick and a full bevel on those
    collapses opposing profiles into zero-area slivers even with clamp_overlap."""
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


def box_long(name, s0, s1, u0, u1, z0, z1, mat, mat_top=None):
    """A box in the LONG frame — the roof's whole vocabulary."""
    return prism(name, long_rect(s0, s1, u0, u1), z0, z1, mat, mat_top=mat_top)


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


def skylight(name, s0, s1, u0, u1, z_deck, mats, rise=0.26):
    """A raised skylight: a trim kerb with a glass cap. The four in the middle of
    the roof and the three along the north-east edge nearer the street are the
    same module at two sizes."""
    prism(f"{name}_kerb", long_rect(s0, s1, u0, u1), z_deck, z_deck + rise, mats["Toy_trim"])
    prism(
        f"{name}_glass",
        long_rect(s0 + 0.12, s1 - 0.12, u0 + 0.12, u1 - 0.12),
        z_deck + rise - 0.04,
        z_deck + rise + 0.05,
        mats["Toy_glass"],
    )


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mats = {name: make_material(name) for name in PALETTE_HEX}

    # ------------------------------------------------------------ main volume
    # Three storeys on the surveyed lot, front 22.90 m of it. Both party walls
    # are blind (76-82 is 1.6 m taller, 86-96 only 0.2 m shorter), so nothing is
    # applied to the two long faces at all.
    prism(
        "body",
        long_rect(0.0, S_REAR_WING, 0.0, FRONTAGE),
        0.0,
        Z_DECK,
        mats["Toy_slate"],
        mat_top=mats["Toy_stone"],
    )
    rim(
        "parapet",
        long_rect(0.0, S_REAR_WING, 0.0, FRONTAGE),
        0.22,
        Z_DECK,
        Z_PARAPET,
        mats["Toy_trim"],
    )

    # -------------------------------------------------------------- rear wing
    # The building steps down to two storeys for its back 7.17 m: a planted
    # roof terrace at 8.10 m, matching the LiDAR minimum of 8.18 m on this
    # footprint and the separate 16 m2 / 7.99 m footprint at the lot's end.
    prism(
        "rear_wing",
        long_rect(S_REAR_WING, DEPTH, 0.0, FRONTAGE),
        0.0,
        Z_REAR_DECK,
        mats["Toy_slate"],
        mat_top=mats["Toy_stone"],
    )
    rim(
        "rear_parapet",
        long_rect(S_REAR_WING, DEPTH, 0.0, FRONTAGE),
        0.20,
        Z_REAR_DECK,
        Z_REAR_PARAPET,
        mats["Toy_trim"],
    )
    # The glazed bay over the very back of the wing — the gridded cap the aerial
    # shows at the rear lot line.
    box_long(
        "rear_glazed_kerb", 27.30, 29.70, 0.75, FRONTAGE - 0.75,
        Z_REAR_DECK, Z_REAR_DECK + 0.22, mats["Toy_trim"],
    )
    box_long(
        "rear_glazed_cap", 27.42, 29.58, 0.87, FRONTAGE - 0.87,
        Z_REAR_DECK + 0.18, Z_REAR_DECK + 0.28, mats["Toy_glass"],
    )
    # Terrace planting along the south-west edge of the wing's deck.
    for i, s in enumerate((23.55, 25.75)):
        box_long(
            f"terrace_plant{i}", s, s + 1.15, 0.42, 1.55,
            Z_REAR_DECK, Z_REAR_DECK + 0.48, mats["Toy_mint"],
        )

    # --------------------------------------------------------- roof skylights
    # Four in a near-continuous run down the middle of the main roof (Bing z20,
    # 1.55 x 1.11 m each at 1.83 m centres), then three smaller ones along the
    # north-east edge nearer the street. The ASYMMETRY is the cue; the exact
    # counts are read off 0.118 m/px imagery — see REPORT.md.
    for i in range(4):
        s0 = 15.55 + i * 1.83
        skylight(f"sky_mid{i}", s0, s0 + 1.55, 2.52, 3.63, Z_DECK, mats)
    for i in range(3):
        s0 = 2.85 + i * 1.45
        skylight(f"sky_ne{i}", s0, s0 + 1.18, 5.05, 6.13, Z_DECK, mats, rise=0.24)

    # ----------------------------------------------------------- roof pergola
    # An open slatted frame over the street-end roof deck: four posts, two side
    # rails and six cross beams, crest at exactly Z_PERGOLA. THIS IS THE
    # BOUNDING-BOX TOP. It must stay open — the deck has to be visible between
    # the beams from directly above, or it reads as a solid array.
    P_S0, P_S1 = 7.20, 10.20
    P_U0, P_U1 = 0.85, 4.85
    POST = 0.16
    for i, (ps, pu) in enumerate(
        ((P_S0, P_U0), (P_S0, P_U1 - POST), (P_S1 - POST, P_U0), (P_S1 - POST, P_U1 - POST))
    ):
        box_long(
            f"pergola_post{i}", ps, ps + POST, pu, pu + POST,
            Z_DECK, Z_PERGOLA - 0.14, mats["Toy_ink"],
        )
    for i, u in enumerate((P_U0, P_U1 - POST)):
        box_long(
            f"pergola_rail{i}", P_S0, P_S1, u, u + POST,
            Z_PERGOLA - 0.30, Z_PERGOLA - 0.14, mats["Toy_ink"],
        )
    for i in range(5):
        s = P_S0 + 0.20 + i * ((P_S1 - P_S0 - 0.40 - 0.14) / 4.0)
        box_long(
            f"pergola_beam{i}", s, s + 0.14, P_U0 - 0.10, P_U1 + 0.10,
            Z_PERGOLA - 0.14, Z_PERGOLA, mats["Toy_ink"],
        )

    # -------------------------------------------------------- roof garden
    # Planting, a small tree and a stair bulkhead, all at the street end of the
    # deck, south-west of the north-east skylight run.
    box_long("roof_bulkhead", 3.50, 4.70, 1.05, 2.35, Z_DECK, Z_DECK + 1.55, mats["Toy_ink"])
    for i, (s0, u0) in enumerate(((1.15, 1.05), (1.15, 4.35))):
        box_long(
            f"roof_plant{i}", s0, s0 + 1.35, u0, u0 + 0.85,
            Z_DECK, Z_DECK + 0.52, mats["Toy_mint"],
        )
    box_long("tree_trunk", 2.52, 2.78, 3.82, 4.08, Z_DECK, Z_DECK + 1.02, mats["Toy_rust"])
    box_long("tree_canopy", 1.90, 3.40, 3.15, 4.75, Z_DECK + 0.88, Z_DECK + 1.85, mats["Toy_mint"])

    # ------------------------------------------- street front, south-west bay
    # The wide bay: a recessed ground-floor opening holding the living green
    # wall and one window, a pale projecting box at second-floor level, and a
    # single wide third-floor window.
    prism(
        "gf_recess",
        FRONT.rect(0.40, 4.05, -0.14, 0.02),
        0.28,
        3.30,
        mats["Toy_roofd"],
    )
    prism(
        "greenwall",
        FRONT.rect(0.58, 2.92, -0.11, 0.03),
        0.95,
        3.12,
        mats["Toy_mint"],
    )
    for nm, t0, t1 in (("gw_jamb_sw", 0.44, 0.58), ("gw_jamb_ne", 2.92, 3.06)):
        prism(nm, FRONT.rect(t0, t1, -0.12, 0.08), 0.86, 3.22, mats["Toy_trim"])
    prism("gw_head", FRONT.rect(0.44, 3.06, -0.12, 0.08), 3.12, 3.22, mats["Toy_trim"])
    prism("gw_sill", FRONT.rect(0.44, 3.06, -0.12, 0.10), 0.86, 0.95, mats["Toy_trim"])
    prism("gf_window", FRONT.rect(3.18, 3.96, -0.11, 0.03), 1.05, 3.08, mats["Toy_glass"])

    # The projecting box. 0.35 m proud, spanning the wide bay, with one recessed
    # window in its face — the brightest object on the elevation.
    prism(
        "bay_box",
        FRONT.rect(0.30, 4.10, 0.0, 0.45),
        Z_FLOOR2 + 0.40,
        Z_FLOOR3 - 0.20,
        mats["Toy_trim"],
    )
    prism(
        "bay_window",
        FRONT.rect(0.85, 3.55, 0.30, 0.48),
        Z_FLOOR2 + 0.85,
        Z_FLOOR3 - 0.75,
        mats["Toy_glass"],
    )
    prism(
        "bay_window_glow",
        FRONT.rect(0.91, 3.49, 0.48, 0.52),
        Z_FLOOR2 + 0.91,
        Z_FLOOR3 - 0.81,
        mats["Toy_glassl_Glow"],
    )

    # Third floor: one wide recessed window with a proud surround.
    prism("f3_window", FRONT.rect(0.55, 4.00, -0.14, 0.02), 8.30, 10.20, mats["Toy_glass"])
    prism("f3_sill", FRONT.rect(0.43, 4.12, 0.0, 0.10), 8.18, 8.30, mats["Toy_trim"])
    prism("f3_head", FRONT.rect(0.43, 4.12, 0.0, 0.09), 10.20, 10.30, mats["Toy_trim"])
    prism(
        "f3_window_glow",
        FRONT.rect(0.62, 3.93, 0.02, 0.06),
        8.38,
        10.12,
        mats["Toy_glassl_Glow"],
    )

    # ------------------------------------------- street front, north-east bay
    # One tall recessed slot running from the pavement to just under the
    # parapet: the entrance below, two terrace rails above. From the app's
    # camera this dark vertical slot beside a pale projecting box is the whole
    # composition of the front.
    # There is no boolean subtraction here: the "recess" is a dark inset field
    # whose outer face sits just behind the wall, and everything that should
    # read inside it stands PROUD of that field. Authored the other way round
    # (door and rails deeper than the field) the first build buried both and the
    # bay rendered as a flat dark stripe — see REPORT.md correction 2.
    prism("slot", FRONT.rect(4.45, 6.62, -0.30, 0.03), 0.0, 10.60, mats["Toy_roofd"])
    prism("door", FRONT.rect(4.86, 6.16, 0.03, 0.17), 0.0, 2.34, mats["Toy_red"])
    prism("door_head", FRONT.rect(4.76, 6.26, 0.03, 0.22), 2.34, 2.48, mats["Toy_trim"])
    prism(
        "slot_glow",
        FRONT.rect(4.62, 6.45, 0.22, 0.26),
        2.54,
        2.80,
        mats["Toy_trim_Glow"],
    )
    for i, z in enumerate((Z_FLOOR2 + 0.30, Z_FLOOR3 + 0.35)):
        prism(f"terrace_rail{i}", FRONT.rect(4.50, 6.57, 0.06, 0.20), z, z + 0.95, mats["Toy_ink"])

    # ---------------------------------------------------------- rear elevation
    # Seen in the app only from above and obliquely. One value change and six
    # windows on the two-storey wing's back wall.
    prism("rear_face", REAR.rect(0.30, FRONTAGE - 0.30, -0.02, 0.06), 0.20, Z_REAR_DECK - 0.30,
          mats["Toy_steel"])
    for i in range(3):
        t = 1.05 + i * 2.10
        for z in (1.55, 4.85):
            prism(
                f"rear_win{i}_{int(z)}",
                REAR.rect(t, t + 1.05, -0.10, 0.09),
                z,
                z + 1.45,
                mats["Toy_glass"],
            )

    for obj in [o for o in bpy.data.objects if o.type == "MESH"]:
        bevel(obj)


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
    print(f"[build] design (parcel-centroid) anchor: {DESIGN_ANCHOR}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] street elevation faces: {FRONT.heading:.2f} deg true")
    print(f"[build] rear faces: {REAR.heading:.2f}; SW flank {FLANK_SW.heading:.2f}; "
          f"NE flank {FLANK_NE.heading:.2f}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    recentre()
    report()

    blend = os.path.join(out, "84-south-park.blend")
    glb = os.path.join(out, "84-south-park.glb")
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
