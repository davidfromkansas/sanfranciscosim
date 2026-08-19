"""Deterministic Blender build of the SF-SIM miniature 44-46 South Park.

    blender -b --python build_46_south_park.py -- [--out DIR]

Writes 46-south-park.blend and 46-south-park.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, parapet crest exactly
16.15 m.

Design (see REFERENCE.md for the sources behind every number):

* a 2008 four-level wood-frame mixed-use infill house on the north-west rim of
  the South Park oval — a commercial unit at 46 under three residential levels
  reached from a purple door at 44 — occupying the whole of a 9.47 m x 29.43 m
  lot, both long sides party walls, one public face;
* the recognition is ONE MOVE: a white-painted, finely gridded glazed wall
  filling almost the whole 9.47 m frontage from the pavement to a charcoal
  parapet, set into and standing proud of a mid-grey stucco surround. It is the
  only glass front on this stretch of the rim, between a pale stuccoed neighbour
  (54-58, south-west, roof 13.50 m) and a black board-clad one (22-24,
  north-east, roof 12.39 m) — this building's deck is 13.90 m, so it stands
  above both;
* the grid is deliberately COARSE. The real wall is roughly five panes by
  twelve; at the app's 30-50 deg aerial camera that count is invisible and the
  whiteness and regularity is everything, so it is modelled as three structural
  bays by four floor bands of raised trim on ONE recessed glass plane. See the
  plan's 2.6 and 2.11 — a faithful pane grid is 4k triangles that do not read;
* the ground floor is glazed to the pavement with two things broken out of it:
  a white-framed double-door service bay at the south-west end and a shallow
  AUBERGINE entry recess with a small awning at the north-east end, tucked
  against the stucco pier. That purple is the building's only colour and it is
  the fifth recognition cue;
* the roof deck is at 13.90 m (LiDAR majority over 1,146 cells) and the street
  face continues 2.25 m above it as a solid parapet/terrace screen to the 16.15 m
  LiDAR maximum — corroborated independently at 15.9 +/- 0.5 m by photogrammetry
  off the Jan 2025 Street View panorama. Both immediate neighbours carry the same
  bimodal LiDAR signature, so a tall street parapet over a terrace is the
  typology here, not an outlier. See REPORT.md and the plan's 2.15;
* the rear quarter of the plan steps down to ~8.0 m: the two-level mixture that
  reproduces the measured mean (12.50 m) and standard deviation (2.47 m) against
  a 13.90 m deck is 23.7% of the footprint at 8.0 m. The fraction is measured;
  the position (at the north-west end) is read off the nadir aerial;
* the roof is NOT empty: the 4.96 kW 2012 photovoltaic array covers the
  north-west half of the main deck, a large skylight sits immediately south-east
  of it, and the mechanical plant is grouped hard against the north-east parapet
  so the south-east third stays clean;
* night state: the commercial ground floor lit across the full frontage — an
  office behind a wall of glass, and the brightest thing on this rim after dark —
  plus four scattered lit panes upstairs, never a full row. Glow surfaces are
  thin shells proud of the opaque glazing: the app renders _Glow in a separate
  layer that is ~12% alpha by day, and a closed shell reads at about twice that,
  so a primary surface must never be authored as glow.

Authoring frame: the footprint is a clean rectangle at 45 deg to the world axes,
so everything is placed through two local frames built from it — a FRONT frame
(t along the 9.47 m street frontage from the south-west party wall, d outward at
135.2 deg) and a LONG frame (s from the street edge toward the block interior, u
across from the south-west party wall). Because the building sits at 45 deg, the
axis-aligned XY bounding box is ~27.5 x 27.6 m even though the building is
9.47 x 29.43 m. That is expected, not a scale error.
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

# Area centroid of the DataSF LiDAR footprint SF3775217 — the middle of the
# three surveys (1.22 m from the OSM centroid, 1.37 m from the parcel centroid)
# and the centroid of the ring the bake actually deletes, which is what opens
# the exclusion window. See the plan's 2.3 and 2.13.
DESIGN_ANCHOR = (-122.3938249, 37.7821869)

# Lot: OSM way/124884347 measures 29.43 x 9.47 m (278.7 m2); the surveyed parcel
# 3775217 measures 30.10 x 9.74 m (293.0 m2) on the same bearing; the DataSF
# LiDAR footprint is 284.3 m2. The OSM dimensions are taken — they are the
# middle reading and the one the bake's own gap-fill ring uses.
FRONTAGE = 9.47
DEPTH = 29.43
AXIS_BEARING = 315.2      # street -> rear (north-west, into the block interior)
FRONT_BEARING = 135.2     # the street elevation faces south-east, onto the oval

Z_DECK = 13.90            # main flat roof deck — MEASURED (DataSF LiDAR height
                          # majority over 1,146 cells; median 13.52). OSM
                          # height=14 agrees.
Z_CREST = 16.15           # front parapet / terrace screen crest — MEASURED
                          # (DataSF LiDAR maximum), corroborated at 15.9 +/- 0.5
                          # by panorama photogrammetry. The bbox top and the
                          # manifest targetHeightM, so the loader's scale is
                          # exactly 1.0.
Z_REAR = 8.00             # the low rear block — DERIVED from the LiDAR height
                          # distribution (see the module docstring).
S_REAR = 22.43            # where the main mass steps down (29.43 - 7.00)

Z_GF = 4.35               # head of the ground floor / first heavy floor mullion
Z_FL2, Z_FL3 = 7.50, 10.70   # the two upper floor mullions
Z_FROST = 11.90           # bottom of the obscure-glass band
Z_WALLTOP = 13.00         # top rail of the window wall

# Front-face layout, t metres from the south-west party wall along the 9.47 m
# frontage. Read off the Jan 2025 panorama after rectification: the projection
# is exactly linear along the facade once the view is centred on its normal, so
# these are measurements, not eyeballed proportions. See REPORT.md.
T_DOOR0, T_DOOR1 = 0.15, 1.95      # the white-framed double-door service bay
T_WALL0, T_WALL1 = 1.10, 7.35      # the glazed wall above the ground floor
T_GLASS0 = 2.15                    # ground-floor glazing starts clear of the doors
T_PIER0, T_PIER1 = 7.62, 8.10      # the stucco pier
T_ENTRY0, T_ENTRY1 = 8.10, 9.35    # the aubergine residential entry (44)

# The glazed wall is a shallow BAY: the white frame and the grid stand proud of
# the stucco plane and the glass sits just behind them. The glass is authored a
# few centimetres PROUD of the stucco rather than sunk into it — the body is a
# solid prism with no opening cut in it (that is what keeps every object a
# closed shell for the signed-volume normal test), so a glass plane authored
# behind the wall face is simply invisible. First build did exactly that and
# rendered a blank grey slab; see REPORT.md.
GLASS_D0, GLASS_D1 = -0.10, 0.05   # the glass plane, just proud of the stucco
GRID_D1 = 0.15            # outer face of the bay/floor mullions
WALL_PROUD = 0.24         # outer face of the frame around the whole opening
PIER_PROUD = 0.10
MULLION_W = 0.18          # vertical bay mullions
MULLION_H = 0.22          # horizontal floor mullions
SCREEN_T = 0.35           # thickness of the front parapet / terrace screen
SCREEN_RETURN = 1.40      # how far it wraps down each party wall
PARAPET_H = 0.45          # upstand on the other three roof edges
PLINTH_H = 0.15

DOOR_Z1 = 3.35
ENTRY_D, ENTRY_Z1 = 0.40, 3.45
AWNING_Z = 3.20

BEVEL_W, BEVEL_SEG = 0.12, 2

PALETTE_HEX = {
    "Toy_steel": "9aa0a6",   # the stucco body, both party walls, the rear block,
                             # the parapet and screen, the pier, the mechanical
                             # plant and the PV rails. The real stucco is a shade
                             # darker than this; 9aa0a6 is chosen deliberately
                             # over Toy_roofd because the building's whole trick
                             # is a WHITE grid against a DARKER surround, and at
                             # 45454a the surround becomes a black hole at the
                             # app's camera and the grid stops reading. See
                             # REPORT.md.
    "Toy_trim": "f3efe6",    # the window-wall frame, the bay and floor mullions,
                             # the obscure-glass band, the door-bay frame and the
                             # skylight kerb — the white that carries the asset
    "Toy_glass": "2a4d73",   # the glazed wall, the ground floor, the skylight
    "Toy_roofd": "45454a",   # the front screen band above the window wall, the
                             # stucco pier beside it and the vent recesses. The
                             # real stucco is one colour all over, but at the
                             # app's camera a single mid grey turns the whole
                             # asset into a grey box and the white grid — the
                             # entire recognition — stops reading. Darkening the
                             # two elements that FRAME the grid, and only those,
                             # buys the contrast back for 2.25 m of band and a
                             # 0.48 m pier. Deliberately NOT applied to the body
                             # or the party walls: a dark palette that looks
                             # right in this rig renders near-black in the app.
    "Toy_stone": "d9d2c2",   # the roof membrane
    "Toy_navy": "2c4a70",    # the photovoltaic panels
    "Toy_ink": "3a3530",     # base plinth, double-door panel, stucco vents
    "Toy_plum": "6b4270",    # DELIBERATELY OFF-PALETTE. The residential entry
                             # recess and its awning. The building has exactly
                             # one colour and this is it; no palette entry is
                             # anywhere near purple, and dropping it to Toy_ink
                             # loses a recognition cue. sf-asset-check scores an
                             # off-palette colour as a WARN, not a failure — this
                             # one is knowing and is logged in REPORT.md.
    "Toy_trim_Glow": "f3efe6",
    "Toy_glassl_Glow": "6f95b8",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


# ------------------------------------------------------------------ geometry


def _brg(deg):
    """Compass bearing -> unit vector in world XY (+X east, +Y north)."""
    r = math.radians(deg)
    return (math.sin(r), math.cos(r))


AXIS = _brg(AXIS_BEARING)          # street edge -> rear edge
PERP = _brg(AXIS_BEARING + 90.0)   # south-west party wall -> north-east one

_HC = (-AXIS[0] * DEPTH / 2.0, -AXIS[1] * DEPTH / 2.0)   # street-edge midpoint
STREET_SW = (_HC[0] - PERP[0] * FRONTAGE / 2.0, _HC[1] - PERP[1] * FRONTAGE / 2.0)
STREET_NE = (_HC[0] + PERP[0] * FRONTAGE / 2.0, _HC[1] + PERP[1] * FRONTAGE / 2.0)
REAR_NE = (STREET_NE[0] + AXIS[0] * DEPTH, STREET_NE[1] + AXIS[1] * DEPTH)
REAR_SW = (STREET_SW[0] + AXIS[0] * DEPTH, STREET_SW[1] + AXIS[1] * DEPTH)

FOOTPRINT = [STREET_SW, STREET_NE, REAR_NE, REAR_SW]

CX = sum(p[0] for p in FOOTPRINT) / 4.0
CY = sum(p[1] for p in FOOTPRINT) / 4.0


def long_xy(s, u):
    """LONG frame: s metres from the street edge toward the block interior,
    u metres across from the south-west party wall."""
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


FRONT = Face(STREET_SW, STREET_NE)   # the street elevation, faces 135.2 deg
REAR = Face(REAR_NE, REAR_SW)        # block interior, faces 315.2 deg
FLANK_SW = Face(REAR_SW, STREET_SW)  # toward 54-58, faces 225.2 deg
FLANK_NE = Face(STREET_NE, REAR_NE)  # toward 22-24, faces 45.2 deg


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
    a third of the object's thinnest dimension: mullions, glow shells and the PV
    scoring are only 40-180 mm thick and a full bevel on those collapses
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


def cylinder(name, cx, cy, r, z0, z1, mat, seg=10):
    poly = [
        (cx + r * math.cos(2 * math.pi * i / seg), cy + r * math.sin(2 * math.pi * i / seg))
        for i in range(seg)
    ]
    return prism(name, poly, z0, z1, mat)


def face_slab(name, face, t0, t1, d0, d1, z0, z1, mat):
    return prism(name, face.rect(t0, t1, d0, d1), z0, z1, mat)


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


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    mats = {name: make_material(name) for name in PALETTE}

    # -- massing ------------------------------------------------------------
    # The main four-level mass, then the rear block that steps down to 8 m. They
    # are separate solids on purpose: the union is what the loader merges, and
    # per-object signed volume is the authoritative normal test.
    prism("body_main", long_rect(0.0, S_REAR, 0.0, FRONTAGE), 0.0, Z_DECK,
          mats["Toy_steel"], mat_top=mats["Toy_stone"])
    prism("body_rear", long_rect(S_REAR, DEPTH, 0.0, FRONTAGE), 0.0, Z_REAR,
          mats["Toy_steel"], mat_top=mats["Toy_stone"])
    # The rear block gets its own thin upstand so the step reads as a parapet
    # edge rather than a saw cut.
    prism("rear_upstand", long_rect(DEPTH - 0.30, DEPTH, 0.0, FRONTAGE),
          Z_REAR, Z_REAR + 0.35, mats["Toy_steel"])

    # -- the front parapet / terrace screen ---------------------------------
    # The 2.25 m between the deck and the crest. Modelled as a screen wall on
    # the street face with short returns down both party walls, which is the
    # reading argued in the plan's 2.15 — and the returns are what stop it
    # reading as a billboard propped on the roof.
    face_slab("front_screen", FRONT, 0.0, FRONTAGE, -SCREEN_T + 0.06, 0.06,
              Z_DECK, Z_CREST, mats["Toy_roofd"])
    face_slab("screen_return_sw", FLANK_SW, FLANK_SW.length - SCREEN_RETURN,
              FLANK_SW.length, -SCREEN_T + 0.04, 0.04, Z_DECK, Z_CREST,
              mats["Toy_roofd"])
    face_slab("screen_return_ne", FLANK_NE, 0.0, SCREEN_RETURN,
              -SCREEN_T + 0.04, 0.04, Z_DECK, Z_CREST, mats["Toy_roofd"])

    # Three small recessed vents in the screen — the one incident on an
    # otherwise blank 2.25 m band. Kept as shallow ink recesses, not openings.
    for i, tc in enumerate((3.10, 4.70, 6.30)):
        face_slab(f"screen_vent_{i}", FRONT, tc - 0.34, tc + 0.34, -0.04, 0.08,
                  Z_CREST - 1.35, Z_CREST - 0.85, mats["Toy_ink"])

    # -- the stucco pier and the window-wall reveal --------------------------
    face_slab("front_pier", FRONT, T_PIER0, T_PIER1, 0.0, PIER_PROUD,
              0.0, Z_DECK, mats["Toy_roofd"])

    # The glazed wall itself: ONE recessed plane, upper and ground portions, and
    # the grid is raised trim on top of it (plan 2.6). Two planes rather than
    # one because the ground-floor glazing stops clear of the door bay.
    face_slab("glass_upper", FRONT, T_WALL0, T_WALL1, GLASS_D0, GLASS_D1,
              Z_GF, Z_WALLTOP, mats["Toy_glass"])
    face_slab("glass_ground", FRONT, T_GLASS0, T_WALL1, GLASS_D0, GLASS_D1,
              PLINTH_H, Z_GF, mats["Toy_glass"])

    # The white frame around the opening, standing proud of the stucco plane —
    # the wall is a shallow bay, not a flush curtain wall, and the stucco
    # returns down its north-east side are visible from the street.
    fw = 0.22
    for nm, t0, t1 in (("frame_sw", T_WALL0 - fw, T_WALL0),
                       ("frame_ne", T_WALL1, T_WALL1 + fw)):
        face_slab(nm, FRONT, t0, t1, GLASS_D0, WALL_PROUD,
                  PLINTH_H, Z_WALLTOP + fw, mats["Toy_trim"])
    face_slab("frame_head", FRONT, T_WALL0 - fw, T_WALL1 + fw, GLASS_D0, WALL_PROUD,
              Z_WALLTOP, Z_WALLTOP + fw, mats["Toy_trim"])
    # The ground-floor return of the frame, closing the opening beside the doors.
    face_slab("frame_ground_sw", FRONT, T_GLASS0 - fw, T_GLASS0, GLASS_D0, WALL_PROUD,
              PLINTH_H, Z_GF, mats["Toy_trim"])

    # -- the grid: three bays x four floor bands -----------------------------
    span = T_WALL1 - T_WALL0
    centre_bay = 2.55
    side_bay = (span - centre_bay - 2 * MULLION_W) / 2.0
    m1 = T_WALL0 + side_bay
    m2 = m1 + MULLION_W + centre_bay
    for i, t0 in enumerate((m1, m2)):
        face_slab(f"mullion_v_{i}", FRONT, t0, t0 + MULLION_W, GLASS_D0, GRID_D1,
                  PLINTH_H, Z_WALLTOP, mats["Toy_trim"])
    for i, z in enumerate((Z_GF, Z_FL2, Z_FL3)):
        face_slab(f"mullion_h_{i}", FRONT, T_WALL0, T_WALL1, GLASS_D0, GRID_D1,
                  z - MULLION_H / 2.0, z + MULLION_H / 2.0, mats["Toy_trim"])
    # The obscure-glass band that caps the wall: flat opaque trim, sitting in the
    # glass plane, not another sheet of Toy_glass.
    face_slab("frost_band", FRONT, T_WALL0, T_WALL1, GLASS_D0, GLASS_D1 + 0.02,
              Z_FROST, Z_WALLTOP, mats["Toy_trim"])

    # -- ground floor: the two things broken out of the glazing --------------
    # Three bars, not one slab: a solid frame at full depth simply buries the
    # panel behind it (that is what the first build did).
    for nm, t0, t1, z0, z1 in (
        ("door_jamb_sw", T_DOOR0 - 0.14, T_DOOR0, PLINTH_H, DOOR_Z1 + 0.14),
        ("door_jamb_ne", T_DOOR1, T_DOOR1 + 0.14, PLINTH_H, DOOR_Z1 + 0.14),
        ("door_head", T_DOOR0 - 0.14, T_DOOR1 + 0.14, DOOR_Z1, DOOR_Z1 + 0.14),
    ):
        face_slab(nm, FRONT, t0, t1, -0.10, 0.17, z0, z1, mats["Toy_trim"])
    face_slab("door_panel", FRONT, T_DOOR0, T_DOOR1, -0.10, 0.09,
              PLINTH_H, DOOR_Z1, mats["Toy_glass"])
    face_slab("door_mullion", FRONT, (T_DOOR0 + T_DOOR1) / 2.0 - 0.05,
              (T_DOOR0 + T_DOOR1) / 2.0 + 0.05, -0.10, 0.14,
              PLINTH_H, DOOR_Z1, mats["Toy_trim"])

    # The entry reads as a shallow COLOUR PANEL rather than a deep hole: a real
    # 0.4 m recess falls into its own shadow at the app's camera and the one
    # colour on the building disappears. The awning does the depth instead.
    face_slab("entry_recess", FRONT, T_ENTRY0, T_ENTRY1, -0.12, 0.02,
              PLINTH_H, ENTRY_Z1, mats["Toy_plum"])
    # The door leaf itself, so the purple reads as a surround and not a slab.
    # It is WHITE in the photograph — an ink leaf turns the one colour on the
    # building into a black slot with a purple edge.
    face_slab("entry_door", FRONT, T_ENTRY0 + 0.26, T_ENTRY1 - 0.26, -0.12, 0.06,
              PLINTH_H, ENTRY_Z1 - 0.30, mats["Toy_trim"])
    face_slab("entry_reveal_sw", FRONT, T_ENTRY0 - 0.13, T_ENTRY0, -0.12, 0.12,
              PLINTH_H, ENTRY_Z1 + 0.13, mats["Toy_plum"])
    face_slab("entry_reveal_ne", FRONT, T_ENTRY1, T_ENTRY1 + 0.13, -0.12, 0.12,
              PLINTH_H, ENTRY_Z1 + 0.13, mats["Toy_plum"])
    face_slab("entry_head", FRONT, T_ENTRY0 - 0.13, T_ENTRY1 + 0.13, -0.12, 0.12,
              ENTRY_Z1, ENTRY_Z1 + 0.13, mats["Toy_plum"])
    face_slab("entry_awning", FRONT, T_ENTRY0 - 0.22, T_ENTRY1 + 0.20, 0.12, 0.66,
              AWNING_Z, AWNING_Z + 0.14, mats["Toy_plum"])

    face_slab("plinth", FRONT, 0.0, FRONTAGE, -0.02, 0.08, 0.0, PLINTH_H,
              mats["Toy_ink"])

    # -- roof ---------------------------------------------------------------
    # Upstands on the three edges the screen does not cover. The screen already
    # runs 2 m down each flank, so these start clear of it.
    prism("parapet_sw", long_rect(SCREEN_RETURN, S_REAR, 0.0, 0.28),
          Z_DECK, Z_DECK + PARAPET_H, mats["Toy_steel"])
    prism("parapet_ne", long_rect(SCREEN_RETURN, S_REAR, FRONTAGE - 0.28, FRONTAGE),
          Z_DECK, Z_DECK + PARAPET_H, mats["Toy_steel"])
    prism("parapet_rear", long_rect(S_REAR - 0.28, S_REAR, 0.0, FRONTAGE),
          Z_DECK, Z_DECK + PARAPET_H, mats["Toy_steel"])

    # The 2012 photovoltaic array: one slab on low rails, scored into a 4 x 5
    # grid rather than modelled as twenty panels (plan 2.6). It covers the
    # north-west half of the main deck with its long axis along the building's.
    pv_s0, pv_s1 = 12.10, 20.10
    pv_u0, pv_u1 = 1.85, 7.45
    prism("pv_rail_sw", long_rect(pv_s0, pv_s1, pv_u0, pv_u0 + 0.16),
          Z_DECK + 0.02, Z_DECK + 0.28, mats["Toy_steel"])
    prism("pv_rail_ne", long_rect(pv_s0, pv_s1, pv_u1 - 0.16, pv_u1),
          Z_DECK + 0.02, Z_DECK + 0.28, mats["Toy_steel"])
    prism("pv_panels", long_rect(pv_s0, pv_s1, pv_u0, pv_u1),
          Z_DECK + 0.28, Z_DECK + 0.40, mats["Toy_navy"])
    for i in range(1, 5):
        s = pv_s0 + (pv_s1 - pv_s0) * i / 5.0
        prism(f"pv_score_s_{i}", long_rect(s - 0.04, s + 0.04, pv_u0, pv_u1),
              Z_DECK + 0.40, Z_DECK + 0.44, mats["Toy_steel"])
    for i in range(1, 4):
        u = pv_u0 + (pv_u1 - pv_u0) * i / 4.0
        prism(f"pv_score_u_{i}", long_rect(pv_s0, pv_s1, u - 0.04, u + 0.04),
              Z_DECK + 0.40, Z_DECK + 0.44, mats["Toy_steel"])

    # The big skylight immediately south-east of the array, over the stair.
    sk_s0, sk_s1, sk_u0, sk_u1 = 6.80, 11.00, 2.60, 6.80
    prism("skylight_kerb", long_rect(sk_s0, sk_s1, sk_u0, sk_u1),
          Z_DECK + 0.02, Z_DECK + 0.34, mats["Toy_trim"])
    prism("skylight_glass", long_rect(sk_s0 + 0.20, sk_s1 - 0.20, sk_u0 + 0.20, sk_u1 - 0.20),
          Z_DECK + 0.34, Z_DECK + 0.46, mats["Toy_glass"])

    # -- rear fenestration ---------------------------------------------------
    # INFERRED, and flagged as such in REFERENCE.md and REPORT.md: nothing sees
    # this face. But both long sides are party walls, so the rear elevation is
    # the ONLY daylight these four flats have and the step down to the rear
    # block exists precisely to give the middle of the plan a window — a wholly
    # blind rear is the one reading the building's own plan rules out. Kept
    # plain and regular: an unobserved block-interior face is not the place to
    # invent character.
    for i, u in enumerate((2.20, 5.95)):
        for j, z in enumerate((1.30, 4.80)):
            prism(f"rear_win_{i}{j}",
                  long_rect(DEPTH - 0.14, DEPTH + 0.04, u, u + 2.05),
                  z, z + 1.70, mats["Toy_glass"])
    for i, u in enumerate((1.70, 4.20, 6.70)):
        for j, z in enumerate((8.70, 11.30)):
            prism(f"step_win_{i}{j}",
                  long_rect(S_REAR - 0.14, S_REAR + 0.04, u, u + 1.75),
                  z, z + 1.60, mats["Toy_glass"])

    # The rear block's own roof: a hatch and two vents, so the quarter of the
    # plan nearest the block interior is not a blank lid from the app's camera
    # (style bible: the camera looks down, roofs are facades).
    prism("rear_hatch", long_rect(24.60, 26.30, 2.10, 4.00),
          Z_REAR + 0.02, Z_REAR + 0.32, mats["Toy_trim"])
    for i, (s_, u_) in enumerate(((25.20, 6.60), (26.60, 7.30))):
        cx, cy = long_xy(s_, u_)
        cylinder(f"rear_vent_{i}", cx, cy, 0.30, Z_REAR + 0.02, Z_REAR + 0.48,
                 mats["Toy_steel"])

    # Mechanical, grouped hard against the north-east parapet so the south-east
    # third of the deck stays clean (plan 2.9).
    prism("roof_mech", long_rect(3.10, 4.90, 7.10, 8.30),
          Z_DECK + 0.02, Z_DECK + 0.82, mats["Toy_steel"])
    for i, (s, u) in enumerate(((5.60, 7.60), (6.70, 7.60), (5.60, 8.65))):
        cx, cy = long_xy(s, u)
        cylinder(f"roof_fan_{i}", cx, cy, 0.40, Z_DECK + 0.02, Z_DECK + 0.62,
                 mats["Toy_steel"])

    # -- night state ---------------------------------------------------------
    # Hero: the commercial ground floor, lit across the full glazed width. Thin
    # shells standing proud of the opaque glazing, never a closed box around it.
    # A BAND across the shopfront rather than the whole 4.2 m storey. A shell
    # that tall is still only ~23% alpha by day, but over that much area it
    # lifts the ground floor from navy glass to flat pale grey and the base of
    # the building stops reading as glazing at all. 2.7 m of it is still the
    # brightest thing on the rim at night.
    face_slab("gf_glow", FRONT, T_GLASS0 + 0.10, T_WALL1 - 0.10,
              GLASS_D1, GLASS_D1 + 0.06,
              1.00, 3.70, mats["Toy_trim_Glow"])
    # Supporting: four lit panes upstairs, unevenly placed across the three bays
    # and the three residential levels. An even grid reads institutional; this
    # is four flats.
    lit = (
        (T_WALL0 + 0.35, T_WALL0 + side_bay - 0.35, Z_GF + 0.45, Z_FL2 - 0.45),
        (m1 + MULLION_W + 0.45, m2 - 1.35, Z_FL2 + 0.45, Z_FL3 - 0.45),
        (m2 + MULLION_W + 0.35, T_WALL1 - 0.35, Z_FL2 + 0.45, Z_FL3 - 0.45),
        (m2 + MULLION_W + 0.35, T_WALL1 - 0.35, Z_FL3 + 0.45, Z_FROST - 0.30),
    )
    for i, (t0, t1, z0, z1) in enumerate(lit):
        face_slab(f"win_glow_{i}", FRONT, t0, t1,
                  GLASS_D1, GLASS_D1 + 0.06, z0, z1,
                  mats["Toy_glassl_Glow"])

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.12/2. The grid, the glow shells, the PV scoring and the thin reveals are
    # small and numerous — a token softening or none at all is what keeps this
    # under a 6,000 triangle cap, and none of it reads at the app's camera.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        n = obj.name
        if n.endswith("_glow") or n.startswith(("pv_score", "mullion_", "screen_vent")):
            continue
        if n.startswith(("frame_", "door_", "entry_", "frost_", "plinth",
                         "parapet_", "pv_rail", "glass_", "rear_upstand",
                         "rear_win_", "step_win_")):
            bevel(obj, width=0.035, segments=1)
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
    print(f"[build] rear faces: {REAR.heading:.2f}; SW flank: {FLANK_SW.heading:.2f}; "
          f"NE flank: {FLANK_NE.heading:.2f}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "46-south-park.blend")
    glb = os.path.join(out, "46-south-park.glb")
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
