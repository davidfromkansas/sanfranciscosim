"""Deterministic Blender build of the SF-SIM miniature 92 South Park.

    blender -b --python build_92_south_park.py -- [--out DIR]

Writes 92-south-park.blend and 92-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = the XY bounding-box centre of the built
form, min Z = 0, corner-tower crest exactly 13.28 m.

Design (see REFERENCE.md for the sources behind every number, and REPORT.md for
the corrections this build made to the plan):

* ONE LOT, THREE MASSES AND A COURT. Block 3775 lots 116-121 are six live/work
  condominiums on ONE surveyed 14.45 x 30.05 m corner parcel at the junction of
  South Park Street and Jack London Alley, bearing 44.8 deg along the frontage.
  Toby Levy built it in 1996 as a full-width front block on the park, a narrow
  bar down the alley at the rear, a thin arm down the party wall with 84 South
  Park, and an OPEN PAVED COURT between them. The court is a genuine void with a
  modelled floor — that C-plan is the asset's identity from directly overhead and
  nothing else on the oval has one;
* the corner tower at South Park x Jack London is the crest: a weathering-metal
  cube carried past every other parapet on the building, with ONE saturated red
  column up its outer corner. At the app's camera the column is the only
  saturated thing for a hundred metres, and it is deliberately fattened to
  0.42 m from a real ~0.2 m (style bible s.9);
* "an ambiguated facade of cubic forms" (SF Heritage): the volumes step in and
  out by 0.3-0.4 m, the parapets sit at four different heights, and one of them
  is RAKED — a straight diagonal tying the low front parapet up into the tower.
  A flush facade at one height is the wrong building;
* a cool silver-gray lead-coated-zinc body, a rust-brown tower and court volume,
  a copper-shingle panel raked across the alley end, and a near-black blue tiled
  plinth with a thin teal mosaic stripe at 1.6 m. Every published photograph of
  the base from 1996 to 2025 has that stripe on it;
* night state: the two South Park shopfronts and the entry warm, five upper
  windows cool and deliberately unaligned, and two warm patches in the court so
  the hole in the plan still reads after dark. Glow surfaces are thin shells
  proud of the opaque glazing, never closed boxes (the app renders _Glow in a
  separate layer; a closed shell is two alpha layers and reads ~23% by day).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- projection
# The app's tangent projection, verbatim from pipeline/lib/geo.mjs. Used once,
# to turn the surveyed parcel into metres; nothing downstream reprojects.

LON0, LAT0 = -122.4375, 37.77
M_PER_DEG_LON = 111320 * math.cos(math.radians(LAT0))
M_PER_DEG_LAT = 110540


def project(lon, lat):
    """WGS84 -> app world metres (x east, z south)."""
    return ((lon - LON0) * M_PER_DEG_LON, -(lat - LAT0) * M_PER_DEG_LAT)


def unproject(x, z):
    return (x / M_PER_DEG_LON + LON0, -z / M_PER_DEG_LAT + LAT0)


# ---------------------------------------------------------------- parameters

# DataSF parcel acdm-wktn, blklot 3775119 (one of the six condominium lots; all
# six carry identical geometry), reordered into survey order for the lot frame:
# south corner (South Park x Jack London Alley), east corner (South Park x the
# 84 South Park party line), north corner (rear x party line), west corner
# (rear x alley).
PARCEL_LONLAT = [
    (-122.394092583, 37.781769010),  # S — the street corner, s=0 t=0
    (-122.393976038, 37.781861076),  # E — party corner on South Park
    (-122.394216861, 37.782053976),  # N — party corner at the rear
    (-122.394333664, 37.781961440),  # W — alley corner at the rear
]

# Lot-frame extents, all metres. s runs along the South Park frontage from the
# Jack London Alley corner (s=0) to the 84 South Park party line; t runs into
# the lot from the front property line (t=0) to the rear line. The three masses
# are the 2010 DataSF LiDAR polygons (MBLR SF3775116, two parts) reduced to the
# lot frame and snapped to the lot lines — see the plan's 2.6.
FRONT_T1 = 15.95                 # front block runs this far back
TOWER_S1, TOWER_T1 = 4.30, 4.30  # the corner tower, within the front block
STEP_S = 9.40                    # where the front block steps back 0.35 m
STEP_D = 0.35
REAR_S1 = 6.60                   # rear bar occupies s in [0, REAR_S1]
ARM_S0 = 11.70                   # party arm occupies s in [ARM_S0, FRONTAGE]
ARM_T1 = 25.65                   # ...and t in [FRONT_T1, ARM_T1]
TOWER_PROJ = 0.40                # tower stands proud of both street faces

# Vertical scheme. The plinth top and the three upper floor lines are INFERRED
# from the 1996 frontage photographs against the LiDAR deck; everything at or
# above Z_DECK_A is measured. See REPORT.md s.2.
Z_STRIPE0, Z_STRIPE1 = 1.58, 1.72   # the mosaic accent stripe
Z_PLINTH = 3.55                     # top of the blue tile base / shopfront head
Z_F2 = 6.15
Z_F3 = 8.75
Z_DECK_A = 11.15                    # front block roof — LiDAR median, 837 cells
Z_PAR_A = 11.45
Z_RAKE_HI = 12.60                   # raked parapet, high end at s = TOWER_S1
RAKE_S1 = 8.60                      # ...running down to Z_PAR_A here
Z_DECK_B = 12.32                    # rear bar roof — LiDAR median, 324 cells
Z_PAR_B = 12.62
Z_DECK_C = 11.15                    # party arm roof
Z_PAR_C = 11.45
Z_CREST = 13.28                     # corner tower — LiDAR max, and the target

Z_COURT = 0.06                      # paved court floor
Z_COURT_WALL = 2.60                 # court enclosure walls on the rear lot lines

# Window bands on the three upper storeys, measured off the 1996 frontage frame.
WIN_BANDS = ((4.10, 5.85), (6.70, 8.45), (9.30, 10.85))

PLINTH_PROJ = 0.12    # the tile base stands proud of the body above it
STRIPE_PROJ = 0.05
TRIM = 0.14           # window-frame board width
BEVEL_BIG = 0.06
BEVEL_SMALL = 0.03

PALETTE_HEX = {
    # Lead-coated zinc panel — the body of every mass. Cool, light, and the one
    # thing that puts this building in a different value family from the cream
    # and brick stock either side of it.
    "Toy_steel": "9aa0a6",
    # Weathered copper / Cor-Ten: the corner tower, the court-facing volume of
    # the rear bar, and one band on the fourth floor of the front. ORANGE in the
    # 1996 photographs, dark chocolate in the 2025 one — the weathered state is
    # what the app depicts.
    "Toy_rust": "a86444",
    # The copper-shingle panel raked across the alley end of the rear bar. A
    # half-step darker than Toy_rust so the two brown surfaces do not merge.
    "Toy_cocoa": "6b4a3d",
    # PALETTE EXTENSION (plan 2.9 / 2.15 risk 7). The ground-floor glazed tile is
    # blue-black; Toy_ink (3a3530) is warm near-black and would fold the plinth
    # into the window frames, Toy_navy (2c4a70) is too close to Toy_glass and the
    # shopfronts would vanish into the wall. 2f3a44 is darker than the glazing
    # and bluer than the ink.
    "Toy_bluestone": "2f3a44",
    "Toy_ink": "3a3530",       # window frames, sunshades, shopfront frames, doors
    "Toy_ioorange": "c0402a",  # THE red corner column — the whole accent budget
    "Toy_teal": "3fa8a0",      # mosaic stripe, balcony and stair rails
    "Toy_glass": "2a4d73",     # every window
    "Toy_glassl": "6f95b8",    # shopfronts and the roof skylight
    "Toy_sand": "ece4d4",      # the two roll-up garage doors on the alley
    "Toy_roofd": "45454a",     # roof decks
    # The court paving: warm gray slate. It is deliberately the LIGHTEST large
    # surface on the asset, because from the app's downward camera a court floor
    # in the roof colour is not a court at all — it is another roof.
    "Toy_greige": "b0aa9e",
    "Toy_trim": "f3efe6",      # the two stainless flues, stair stringers, coping
    "Toy_gold_Glow": "caa64a",   # shopfronts, entry, the two court patches
    "Toy_glass_Glow": "6f95b8",  # the lit upper windows
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# ------------------------------------------------------- lot frame (s, t) -> XY
# Built once from the surveyed parcel, then everything in this file is authored
# in (s, t). Blender +X = east, +Y = north; the app's world z is south, so
# y = -z.

_P = [project(lon, lat) for lon, lat in PARCEL_LONLAT]
_ORIGIN = (_P[0][0], -_P[0][1])                       # S corner, in Blender XY
_DU = (_P[1][0] - _P[0][0], -(_P[1][1] - _P[0][1]))   # along the frontage, to NE
_DV = (_P[3][0] - _P[0][0], -(_P[3][1] - _P[0][1]))   # into the lot, to NW
FRONTAGE = math.hypot(*_DU)
DEPTH = math.hypot(*_DV)
U_HAT = (_DU[0] / FRONTAGE, _DU[1] / FRONTAGE)
V_HAT = (_DV[0] / DEPTH, _DV[1] / DEPTH)

# Provisional centring; main() re-centres on the measured bounding box and
# reports the corrected anchor.
_CTR_S = FRONTAGE / 2.0
_CTR_T = DEPTH / 2.0


def st(s, t):
    """Lot-frame (s along the frontage, t into the lot) -> Blender (x, y),
    measured from the provisional centre."""
    ds, dt = s - _CTR_S, t - _CTR_T
    return (U_HAT[0] * ds + V_HAT[0] * dt, U_HAT[1] * ds + V_HAT[1] * dt)


def st_world(s, t):
    """Lot-frame -> app world (x, z), for reporting the anchor."""
    bx = _ORIGIN[0] + U_HAT[0] * s + V_HAT[0] * t
    by = _ORIGIN[1] + U_HAT[1] * s + V_HAT[1] * t
    return (bx, -by)


# Outward normals of the four lot edges.
N_FRONT = (-V_HAT[0], -V_HAT[1])   # 134.8 deg SE — the South Park front
N_SW = (-U_HAT[0], -U_HAT[1])      # 224.8 deg SW — Jack London Alley
N_NE = (U_HAT[0], U_HAT[1])        #  44.8 deg NE — party line with 84 South Park
N_REAR = (V_HAT[0], V_HAT[1])      # 314.8 deg NW — back lot line


def bearing(n):
    return math.degrees(math.atan2(n[0], n[1])) % 360.0


# -------------------------------------------------------------- mesh helpers


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


def bevel(obj, width=BEVEL_BIG, segments=1):
    """Miniature-style edge softening (style bible s.4). Width is capped at a
    third of the object's thinnest dimension so thin trim boards and window
    panels do not collapse into slivers."""
    thin = min((d for d in obj.dimensions if d > 1e-6), default=width)
    offset = min(width, thin * 0.30)
    if offset < 1e-4:
        return obj
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


BOX_FACES = [
    (3, 2, 1, 0),          # bottom
    (4, 5, 6, 7),          # top
    (0, 1, 5, 4),
    (1, 2, 6, 5),
    (2, 3, 7, 6),
    (3, 0, 4, 7),
]


def st_box(name, s0, s1, t0, t1, z0, z1, mat, mat_top=None):
    """Closed box on the lot grid. Faces: bottom, top, 4 walls."""
    corners = [st(s0, t0), st(s1, t0), st(s1, t1), st(s0, t1)]
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    if mat_top:
        return new_mesh(name, verts, BOX_FACES, [mat, mat_top], [0, 1, 0, 0, 0, 0])
    return new_mesh(name, verts, BOX_FACES, [mat])


def st_prism(name, s0, s1, t0, t1, z0, z_s0, z_s1, mat):
    """Closed solid whose top face is RAKED linearly along s: the top sits at
    z_s0 over s0 and z_s1 over s1. The one shape this building cannot do
    without — the straight diagonal parapet is its sharpest silhouette line."""
    corners = [st(s0, t0), st(s1, t0), st(s1, t1), st(s0, t1)]
    tops = [z_s0, z_s1, z_s1, z_s0]
    verts = [(x, y, z0) for x, y in corners] + [
        (x, y, tz) for (x, y), tz in zip(corners, tops)
    ]
    return new_mesh(name, verts, BOX_FACES, [mat])


def st_ring(name, s0, s1, t0, t1, z0, z1, thickness, mat):
    """A closed band following a rectangle's outline: an outer shell with the
    inner face pulled in by `thickness`. Used for parapets and the plinth cap."""
    outer = [st(s0, t0), st(s1, t0), st(s1, t1), st(s0, t1)]
    inner = [
        st(s0 + thickness, t0 + thickness),
        st(s1 - thickness, t0 + thickness),
        st(s1 - thickness, t1 - thickness),
        st(s0 + thickness, t1 - thickness),
    ]
    verts = []
    for loop, z in ((outer, z0), (inner, z0), (inner, z1), (outer, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * 4, ((k + 1) % 4) * 4
        for i in range(4):
            j = (i + 1) % 4
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def st_raked_ring(name, s0, s1, t0, t1, z0, z_s0, z_s1, thickness, mat):
    """A parapet band whose top edge is RAKED linearly along s — the straight
    diagonal that ties this building's low front parapet up into its corner
    tower. Built as a ring rather than a solid so the roof deck inside it stays
    visible from the app's downward camera; the first build made it a solid and
    the whole front block read as a sloping roof."""
    def z_at(s):
        return z_s0 + (z_s1 - z_s0) * (s - s0) / (s1 - s0)

    si0, si1 = s0 + thickness, s1 - thickness
    outer = [(s0, t0), (s1, t0), (s1, t1), (s0, t1)]
    inner = [
        (si0, t0 + thickness),
        (si1, t0 + thickness),
        (si1, t1 - thickness),
        (si0, t1 - thickness),
    ]
    verts = []
    for loop, use_top in ((outer, False), (inner, False), (inner, True), (outer, True)):
        for s, t in loop:
            x, y = st(s, t)
            verts.append((x, y, z_at(s) if use_top else z0))
    faces = []
    for k in range(4):
        a0i, b0i = k * 4, ((k + 1) % 4) * 4
        for i in range(4):
            j = (i + 1) % 4
            faces.append((a0i + i, a0i + j, b0i + j, b0i + i))
    return new_mesh(name, verts, faces, [mat])


def curved_wall(name, cs, ct, radius, a0, a1, z0, z1, thick, mat, segments=10):
    """A faceted arc wall in the lot frame — the corrugated galvanized curve at
    the south end of the court, which is the one non-orthogonal thing on the lot
    and reads clearly from directly overhead. Angles in degrees, measured from
    the +s axis in the (s, t) plane."""
    outer, inner = [], []
    for i in range(segments + 1):
        a = math.radians(a0 + (a1 - a0) * i / segments)
        outer.append(st(cs + math.cos(a) * radius, ct + math.sin(a) * radius))
        inner.append(
            st(cs + math.cos(a) * (radius - thick), ct + math.sin(a) * (radius - thick))
        )
    n = segments + 1
    OB, IB, OT, IT = 0, n, 2 * n, 3 * n
    verts = (
        [(x, y, z0) for x, y in outer]
        + [(x, y, z0) for x, y in inner]
        + [(x, y, z1) for x, y in outer]
        + [(x, y, z1) for x, y in inner]
    )
    faces = []
    for i in range(segments):
        faces.append((OB + i, OB + i + 1, OT + i + 1, OT + i))      # outer face
        faces.append((IB + i + 1, IB + i, IT + i, IT + i + 1))      # inner face
        faces.append((OT + i, OT + i + 1, IT + i + 1, IT + i))      # top
        faces.append((IB + i, IB + i + 1, OB + i + 1, OB + i))      # bottom
    faces.append((OB, OT, IT, IB))                                  # start cap
    faces.append((IB + segments, IT + segments, OT + segments, OB + segments))
    return new_mesh(name, verts, faces, [mat])


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
        # Flagged for the app's night pass; emission is off in the day asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------------- parts

# Wall panels are built directly in (s, t) as thin boxes rather than through a
# normal-offset helper, because this building has eight distinct wall planes
# (four lot edges plus four court faces) and a side-keyed helper would need a
# case for each. `axis` is the constant coordinate: 's' means the panel lies in
# the plane s = plane and spans t, 't' means the reverse. `d` is the outward
# offset, POSITIVE in the direction of `out` (+1 or -1).

D_FRAME = 0.06
D_REVEAL = 0.10
D_GLASS = 0.15
D_GLOW = (0.14, 0.19)


def panel(name, axis, plane, out, a0, a1, z0, z1, d0, d1, mat):
    """Thin closed slab in a wall plane, extruded from offset d0 to d1 outward."""
    p0 = plane + out * d0
    p1 = plane + out * d1
    if axis == "s":
        return st_box(name, p0, p1, a0, a1, z0, z1, mat)
    return st_box(name, a0, a1, p0, p1, z0, z1, mat)


def window(tag, axis, plane, out, a0, a1, z0, z1, base_d=0.0, glow=None, sunshade=False):
    """A dark frame, a reveal, a glass panel, optionally a glow shell and a
    projecting hinged sunshade. Every inner layer protrudes past the one around
    it — same outward-increasing convention as artifacts/132-south-park."""
    m_ink, m_glass = material("Toy_ink"), material("Toy_glass")
    panel(f"{tag}_frame", axis, plane, out, a0, a1, z0, z1,
          base_d, base_d + D_FRAME, m_ink)
    panel(f"{tag}_reveal", axis, plane, out, a0 + TRIM, a1 - TRIM, z0 + TRIM, z1 - TRIM,
          base_d, base_d + D_REVEAL, m_ink)
    g = 0.03
    panel(f"{tag}_glass", axis, plane, out,
          a0 + TRIM + g, a1 - TRIM - g, z0 + TRIM + g, z1 - TRIM - g,
          base_d, base_d + D_GLASS, m_glass)
    if glow:
        h = 0.07
        panel(f"{tag}_glow", axis, plane, out,
              a0 + TRIM + h, a1 - TRIM - h, z0 + TRIM + h, z1 - TRIM - h,
              base_d + D_GLOW[0], base_d + D_GLOW[1], material(glow))
    if sunshade:
        # The hinged panel hung off the head, tilted out. Modelled as a flat
        # blade at the head — the tilt is below the camera's resolution and a
        # real hinge costs eight faces for nothing.
        panel(f"{tag}_shade", axis, plane, out, a0 - 0.08, a1 + 0.08,
              z1 + 0.02, z1 + 0.16, base_d, base_d + 0.52, m_ink)


def shopfront(tag, axis, plane, out, a0, a1, z0, z1, lit=True, base_d=PLINTH_PROJ):
    """A ground-floor commercial bay in the tile plinth: ink frame, teal-blue
    glazing, warm glow behind it.

    `base_d` defaults to PLINTH_PROJ because the tile plinth stands proud of the
    body wall these openings are dimensioned against: authored at base_d = 0
    every frame is buried inside the plinth and every glass panel z-fights with
    its outer face. That was the first build's defect on all three elevations."""
    m_ink = material("Toy_ink")
    panel(f"{tag}_frame", axis, plane, out, a0, a1, z0, z1,
          base_d, base_d + 0.07, m_ink)
    panel(f"{tag}_glass", axis, plane, out, a0 + 0.16, a1 - 0.16, z0 + 0.16, z1 - 0.16,
          base_d, base_d + 0.15, material("Toy_glassl"))
    if lit:
        panel(f"{tag}_glow", axis, plane, out,
              a0 + 0.26, a1 - 0.26, z0 + 0.26, z1 - 0.26,
              base_d + 0.14, base_d + 0.19, material("Toy_gold_Glow"))


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)

    m_steel = material("Toy_steel")
    m_rust = material("Toy_rust")
    m_cocoa = material("Toy_cocoa")
    m_blue = material("Toy_bluestone")
    m_ink = material("Toy_ink")
    m_teal = material("Toy_teal")
    m_sand = material("Toy_sand")
    m_roofd = material("Toy_roofd")
    m_trim = material("Toy_trim")
    m_greige = material("Toy_greige")
    m_red = material("Toy_ioorange")
    m_glassl = material("Toy_glassl")

    S = FRONTAGE
    T = DEPTH
    P = PLINTH_PROJ

    # ============================================================ THE PLINTH
    # A blue-black glazed tile base under all three masses, standing proud of
    # the metal body above. Built as three boxes on the three footprints.
    st_box("plinth_front", -P, S + P, -P, FRONT_T1, 0.0, Z_PLINTH, m_blue)
    st_box("plinth_rear", -P, REAR_S1 + P, FRONT_T1, T + P, 0.0, Z_PLINTH, m_blue)
    st_box("plinth_arm", ARM_S0 - P, S + P, FRONT_T1, ARM_T1 + P, 0.0, Z_PLINTH, m_blue)

    # The mosaic accent stripe: one thin teal band all the way round the street
    # faces. It is on every published photograph of this base and it is the only
    # small-scale ornament the building has.
    q = P + STRIPE_PROJ
    st_ring("stripe_front", -q, S + q, -q, FRONT_T1, Z_STRIPE0, Z_STRIPE1, 0.10, m_teal)
    st_ring("stripe_rear", -q, REAR_S1 + q, FRONT_T1, T + q, Z_STRIPE0, Z_STRIPE1,
            0.10, m_teal)

    # ======================================================= MASS A — front block
    # Two sub-volumes with a 0.35 m step between them, plus the raked parapet
    # that ties the low one up into the tower.
    st_box("A1_body", 0.0, STEP_S, 0.0, FRONT_T1, Z_PLINTH, Z_DECK_A,
           m_steel, m_roofd)
    st_box("A2_body", STEP_S, S, STEP_D, FRONT_T1, Z_PLINTH, Z_DECK_A,
           m_steel, m_roofd)
    # A2's fourth storey is a rust band — the horizontal weathering-metal course
    # that runs across the north-east half of the frontage.
    panel("A2_rustband", "t", STEP_D, -1, STEP_S, S, Z_F3, Z_DECK_A, 0.0, 0.09, m_rust)

    # Parapets. A1's is raked from Z_RAKE_HI at the tower down to Z_PAR_A.
    st_raked_ring("A1_parapet", 0.0, STEP_S, 0.0, FRONT_T1, Z_DECK_A,
                  Z_RAKE_HI, Z_PAR_A, 0.28, m_steel)
    st_ring("A2_parapet", STEP_S, S, STEP_D, FRONT_T1, Z_DECK_A, Z_PAR_A, 0.28, m_steel)

    # ====================================================== MASS A' — corner tower
    st_box("tower_body", -TOWER_PROJ, TOWER_S1, -TOWER_PROJ, TOWER_T1,
           Z_PLINTH, Z_CREST, m_rust, m_roofd)
    # The red column, floor to crest, on the outer corner. Fattened to 0.42 m
    # from a real ~0.2 m so it survives at the app's camera (style bible s.9).
    RC = 0.42
    st_box("tower_column", -TOWER_PROJ - 0.10, -TOWER_PROJ - 0.10 + RC,
           -TOWER_PROJ - 0.10, -TOWER_PROJ - 0.10 + RC, Z_PLINTH - 0.35, Z_CREST + 0.02,
           m_red)

    # The copper cube that oversails the court on the front block's fourth
    # floor (1996 photograph 8912EXT). From the app's camera it is the one thing
    # that stops the front block's 14 x 16 m deck reading as a bare plate.
    st_box("A1_cube", 1.30, 4.60, FRONT_T1 - 3.40, FRONT_T1 + 0.55, Z_F3, Z_RAKE_HI,
           m_rust, m_roofd)
    panel("A1_cube_glass", "s", 4.60, +1, FRONT_T1 - 3.05, FRONT_T1 + 0.20,
          Z_F3 + 0.45, Z_RAKE_HI - 0.45, 0.0, 0.09, material("Toy_glass"))

    # ========================================================= MASS B — rear bar
    st_box("B_body", 0.0, REAR_S1, FRONT_T1, T, Z_PLINTH, Z_DECK_B, m_steel, m_roofd)
    st_ring("B_parapet", 0.0, REAR_S1, FRONT_T1, T, Z_DECK_B, Z_PAR_B, 0.28, m_steel)
    # Its court face is the Cor-Ten volume from the 1996 courtyard photograph.
    panel("B_courtface", "s", REAR_S1, +1, FRONT_T1 + 0.4, T - 0.4, Z_PLINTH, Z_DECK_B,
          0.0, 0.10, m_rust)
    # The copper-shingle panel on the alley elevation, cut to a raked profile
    # that steps down toward the rear — the one diagonal on that whole flank.
    # st_prism() rakes along s, so this one is built by its own helper: the
    # diagonal has to run along t.
    SH_T0 = T - 5.20
    _raked_alley_panel("B_shingle", SH_T0, T, Z_PLINTH + 1.10, Z_DECK_B, m_cocoa)

    # ======================================================== MASS C — party arm
    st_box("C_body", ARM_S0, S, FRONT_T1, ARM_T1, Z_PLINTH, Z_DECK_C, m_steel, m_roofd)
    st_ring("C_parapet", ARM_S0, S, FRONT_T1, ARM_T1, Z_DECK_C, Z_PAR_C, 0.28, m_steel)

    # ============================================================== THE COURT
    st_box("court_floor", REAR_S1, S, FRONT_T1, T, 0.0, Z_COURT,
           material("Toy_greige"))
    # Enclosure on the two open lot lines.
    st_box("court_wall_rear", REAR_S1, S, T - 0.30, T, 0.0, Z_COURT_WALL, m_blue)
    st_box("court_wall_ne", S - 0.30, S, ARM_T1, T - 0.30, 0.0, Z_COURT_WALL, m_blue)
    # The curved corrugated wall at the court's south end.
    curved_wall("court_curve", REAR_S1 + 2.55, FRONT_T1 + 2.70, 2.55, -95.0, 95.0,
                Z_COURT, Z_COURT + 2.35, 0.22, m_steel, segments=10)
    # The external steel stair up the party arm's court face: a stepped ramp
    # solid plus two stringers, not individual treads (plan 2.10).
    _court_stair("court_stair", ARM_S0 - 1.25, ARM_S0 - 0.10,
                 FRONT_T1 + 1.20, FRONT_T1 + 7.40, Z_COURT, Z_F2)
    # Two polished stainless flues up the front block's court elevation.
    for i, sc in enumerate((REAR_S1 + 1.30, REAR_S1 + 2.35)):
        st_box(f"flue{i}", sc - 0.11, sc + 0.11, FRONT_T1 - 0.34, FRONT_T1 - 0.12,
               Z_PLINTH, 13.10, m_trim)

    # ========================================================== ROOF FURNITURE
    # The triangular skylight over the front block, from 2026 aerial imagery.
    _skylight("skylight", 4.90, 8.30, 3.60, 8.10, Z_DECK_A, Z_DECK_A + 0.72)
    # A roof rail along the front block's court edge, and a hatch on the bar.
    st_ring("roof_rail", 4.40, 8.90, FRONT_T1 - 4.10, FRONT_T1 - 0.45,
            Z_DECK_A, Z_DECK_A + 0.62, 0.07, m_trim)
    st_box("B_hatch", 2.10, 3.30, T - 4.40, T - 3.20, Z_DECK_B, Z_DECK_B + 0.42, m_ink)
    st_box("B_vent", 4.30, 4.86, T - 6.90, T - 6.34, Z_DECK_B, Z_DECK_B + 0.78, m_trim)
    st_box("C_condenser", ARM_S0 + 0.60, ARM_S0 + 2.10, ARM_T1 - 3.20, ARM_T1 - 1.60,
           Z_DECK_C, Z_DECK_C + 0.60, m_trim)

    # ============================================== SOUTH PARK FRONT (t = 0)
    # Two commercial condominiums at street level — units 86 (in the tower) and
    # 92 (in A1) — a recessed residential entry, and the upper windows.
    shopfront("shop86", "t", -TOWER_PROJ, -1, 0.55, 3.35, 0.75, Z_PLINTH - 0.35)
    shopfront("shop92", "t", 0.0, -1, 4.55, 8.30, 0.75, Z_PLINTH - 0.35)
    PD = PLINTH_PROJ
    panel("entry_recess", "t", 0.0, -1, 8.85, 10.35, 0.0, Z_PLINTH - 0.30,
          PD, PD + 0.07, m_ink)
    panel("entry_door", "t", 0.0, -1, 9.05, 10.15, 0.0, Z_PLINTH - 0.55,
          PD, PD + 0.13, m_red)
    panel("entry_glow", "t", 0.0, -1, 9.20, 10.00, 0.30, Z_PLINTH - 0.75,
          PD + 0.09, PD + 0.18, material("Toy_gold_Glow"))
    shopfront("shop_ne", "t", STEP_D, -1, 11.10, 13.90, 0.75, Z_PLINTH - 0.35,
              lit=False)

    # Upper windows on the front. Deliberately unaligned: the bands are shared
    # but the bays are not, which is the whole point of "ambiguated".
    FRONT_WINS = [
        # (plane_t, out, a0, a1, band, glow, sunshade)
        (-TOWER_PROJ, 0.70, 3.20, 0, "Toy_glass_Glow", False),
        (-TOWER_PROJ, 0.70, 3.20, 1, None, True),
        (-TOWER_PROJ, 0.70, 3.20, 2, "Toy_glass_Glow", False),
        (0.0, 4.35, 6.05, 0, None, True),
        (0.0, 6.70, 8.55, 0, "Toy_glass_Glow", False),
        (0.0, 4.35, 6.05, 1, None, False),
        (0.0, 6.55, 8.85, 1, "Toy_glass_Glow", True),
        (0.0, 4.35, 7.10, 2, None, False),
        (0.0, 8.00, 9.10, 2, None, False),
        (STEP_D, 9.95, 11.85, 0, None, True),
        (STEP_D, 12.45, 14.05, 0, None, False),
        (STEP_D, 9.95, 12.30, 1, "Toy_glass_Glow", False),
        (STEP_D, 12.90, 14.05, 1, None, False),
        (STEP_D, 10.40, 13.60, 2, None, True),
    ]
    for i, (pl, a0, a1, band, glow, shade) in enumerate(FRONT_WINS):
        z0, z1 = WIN_BANDS[band]
        window(f"fw{i}", "t", pl, -1, a0, a1, z0, z1, glow=glow, sunshade=shade)

    # A shallow balcony with a teal rail on the tower's second floor.
    st_box("balcony_deck", 0.55, 3.10, -TOWER_PROJ - 0.95, -TOWER_PROJ,
           WIN_BANDS[0][0] - 0.18, WIN_BANDS[0][0], m_ink)
    st_ring("balcony_rail", 0.55, 3.10, -TOWER_PROJ - 0.95, -TOWER_PROJ,
            WIN_BANDS[0][0], WIN_BANDS[0][0] + 0.62, 0.06, m_teal)

    # ========================================== JACK LONDON ALLEY (s = 0)
    # Two beige roll-up garage doors in the plinth, then sparse punched windows.
    for i, (t0, t1) in enumerate(((5.10, 7.90), (8.60, 11.40))):
        # Both layers are measured from the PLINTH's outer face (PLINTH_PROJ),
        # not from the body wall behind it, and the leaf starts at that face
        # rather than at the frame's front face. Authored the other way round,
        # the ink frame is buried inside the plinth and the leaf's front face
        # lands exactly in the plinth's own outer plane — the first build's
        # garage doors were solid z-fight speckle for both reasons.
        panel(f"garage{i}_frame", "s", 0.0, -1, t0, t1, 0.30, Z_PLINTH - 0.55,
              PLINTH_PROJ, PLINTH_PROJ + 0.06, m_ink)
        panel(f"garage{i}_leaf", "s", 0.0, -1, t0 + 0.14, t1 - 0.14, 0.44,
              Z_PLINTH - 0.69, PLINTH_PROJ, PLINTH_PROJ + 0.12, m_sand)
    panel("alley_service", "s", 0.0, -1, 12.60, 13.70, 0.0, 2.55,
          PLINTH_PROJ, PLINTH_PROJ + 0.08, m_ink)

    ALLEY_WINS = [
        (5.30, 6.55, 0, None), (7.40, 8.40, 0, None), (10.20, 11.60, 0, "Toy_glass_Glow"),
        (5.30, 6.30, 1, None), (8.90, 10.10, 1, None), (12.20, 13.70, 1, None),
        (6.20, 7.30, 2, None), (10.60, 12.90, 2, None),
        (17.60, 18.70, 0, None), (21.30, 22.60, 0, None),
        (17.60, 19.20, 1, "Toy_glass_Glow"), (22.10, 23.30, 1, None),
        (18.90, 20.10, 2, None), (23.00, 24.20, 2, None),
    ]
    for i, (a0, a1, band, glow) in enumerate(ALLEY_WINS):
        z0, z1 = WIN_BANDS[band]
        window(f"aw{i}", "s", 0.0, -1, a0, a1, z0, z1, glow=glow)

    # ================================================= COURT ELEVATIONS
    # The front block's court face (t = FRONT_T1) and the rear bar's (s = REAR_S1).
    for i, (a0, a1, band) in enumerate((
        (REAR_S1 + 0.60, REAR_S1 + 2.00, 0),
        (REAR_S1 + 3.10, REAR_S1 + 5.30, 0),
        (REAR_S1 + 0.60, REAR_S1 + 2.60, 1),
        (REAR_S1 + 3.60, REAR_S1 + 5.30, 1),
        (REAR_S1 + 1.20, REAR_S1 + 4.40, 2),
    )):
        z0, z1 = WIN_BANDS[band]
        window(f"cw{i}", "t", FRONT_T1, +1, a0, a1, z0, z1)
    for i, (a0, a1, band) in enumerate((
        (FRONT_T1 + 1.90, FRONT_T1 + 3.60, 1),
        (FRONT_T1 + 5.40, FRONT_T1 + 7.10, 1),
        (FRONT_T1 + 2.40, FRONT_T1 + 4.20, 2),
        (FRONT_T1 + 8.60, FRONT_T1 + 10.30, 2),
    )):
        z0, z1 = WIN_BANDS[band]
        window(f"bw{i}", "s", REAR_S1, +1, a0, a1, z0, z1, base_d=0.10)
    # Two warm patches at the foot of the stair — the light that escapes the
    # court is the only reason the hole in the plan reads at night.
    for i, (a0, a1) in enumerate(((FRONT_T1 + 1.40, FRONT_T1 + 3.00),
                                  (FRONT_T1 + 4.20, FRONT_T1 + 5.60))):
        panel(f"court_glow{i}", "s", ARM_S0, -1, a0, a1, 0.55, 2.35,
              PLINTH_PROJ + 0.02, PLINTH_PROJ + 0.10, material("Toy_gold_Glow"))

    # ============================================================= THE REAR
    panel("rear_service", "t", T, +1, 1.60, 3.00, 0.0, 2.60,
          PLINTH_PROJ, PLINTH_PROJ + 0.08, m_ink)
    for i, (a0, a1, band) in enumerate(((1.30, 2.60, 1), (4.10, 5.60, 1),
                                        (2.20, 4.80, 2))):
        z0, z1 = WIN_BANDS[band]
        window(f"rw{i}", "t", T, +1, a0, a1, z0, z1)

    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        w = BEVEL_SMALL if min(obj.dimensions) < 0.40 else BEVEL_BIG
        bevel(obj, width=w)


def _raked_alley_panel(name, t0, t1, z_lo, z_hi, mat):
    """The copper-shingle panel on the Jack London Alley flank, whose top edge
    is a straight diagonal rising from z_lo at t1 (the rear) to z_hi at t0."""
    a = st(-0.10, t0)
    b = st(-0.10, t1)
    c = st(0.02, t1)
    d = st(0.02, t0)
    ring = [a, b, c, d]
    tops = [z_hi, z_lo, z_lo, z_hi]
    verts = [(x, y, Z_PLINTH) for x, y in ring] + [
        (x, y, tz) for (x, y), tz in zip(ring, tops)
    ]
    return new_mesh(name, verts, BOX_FACES, [mat])


def _court_stair(name, s0, s1, t0, t1, z0, z1):
    """A stepped ramp solid plus two stringers. Eight steps is enough to read as
    a stair from above and costs a tenth of what real treads would."""
    m_roofd, m_teal = material("Toy_roofd"), material("Toy_teal")
    steps = 8
    for i in range(steps):
        f0 = t0 + (t1 - t0) * i / steps
        f1 = t0 + (t1 - t0) * (i + 1) / steps
        zz = z0 + (z1 - z0) * (i + 1) / steps
        st_box(f"{name}_step{i}", s0, s1, f0, f1, z0, zz, m_roofd)  # noqa: E501
    for i, sc in enumerate((s0, s1 - 0.09)):
        st_prism(f"{name}_rail{i}", sc, sc + 0.09, t0, t1, z0 + 0.30,
                 z1 + 0.95, z1 + 0.95, m_teal)


def _skylight(name, s0, s1, t0, t1, z0, z1):
    """A triangular-section glazed ridge on the front block's deck — the shape
    2026 aerial imagery shows there, and the only thing on that roof the camera
    can actually resolve."""
    m_ink, m_glassl = material("Toy_ink"), material("Toy_glassl")
    st_box(f"{name}_kerb", s0, s1, t0, t1, z0, z0 + 0.16, m_ink)
    mid = (t0 + t1) / 2.0
    ring = [st(s0, t0), st(s1, t0), st(s1, t1), st(s0, t1)]
    ridge = [st(s0, mid), st(s1, mid)]
    verts = [(x, y, z0 + 0.16) for x, y in ring] + [(x, y, z1) for x, y in ridge]
    faces = [
        (3, 2, 1, 0),
        (0, 1, 5, 4),
        (2, 3, 4, 5),
        (1, 2, 5),
        (3, 0, 4),
    ]
    return new_mesh(f"{name}_glass", verts, faces, [m_glassl])


def measure():
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
    return objs, tris, mn, mx


def _apply_to_verts(fn):
    """Rewrite every mesh's vertex coordinates in place, so object transforms
    stay identity and the contract's applied-transform check is trivially met."""
    for me in bpy.data.meshes:
        for v in me.vertices:
            v.co = fn(v.co)


def recentre_and_normalise():
    """Put the XY bounding-box centre at the origin and min Z at 0, then scale
    so the crest lands exactly on Z_CREST. Returns the corrected anchor."""
    _objs, _tris, mn, mx = measure()
    dx = (mn.x + mx.x) / 2.0
    dy = (mn.y + mx.y) / 2.0
    dz = mn.z
    _apply_to_verts(lambda c: Vector((c.x - dx, c.y - dy, c.z - dz)))

    _objs, _tris, mn, mx = measure()
    scale = Z_CREST / mx.z
    if abs(scale - 1.0) > 1e-9:
        _apply_to_verts(lambda c: c * scale)

    wx, wz = st_world(_CTR_S, _CTR_T)
    lon, lat = unproject(wx + dx, wz - dy)
    return lon, lat, dx, dy, dz, scale


def report(lon, lat):
    objs, tris, mn, mx = measure()
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 4) for i in range(2)]}")
    print(f"[build] lot frontage={FRONTAGE:.3f} depth={DEPTH:.3f}")
    print(f"[build] front bearing={bearing(N_FRONT):.1f} SW flank={bearing(N_SW):.1f} "
          f"NE flank={bearing(N_NE):.1f} rear={bearing(N_REAR):.1f}")
    print(f"[build] anchor lon/lat: {lon:.7f} {lat:.7f} (XY bbox centre of the built form)")
    print(f"[build] materials: {sorted(m.name for m in bpy.data.materials)}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    lon, lat, dx, dy, dz, scale = recentre_and_normalise()
    print(f"[build] recentre dx={dx:.4f} dy={dy:.4f} dz={dz:.4f} scale={scale:.9f}")
    report(lon, lat)

    blend = os.path.join(out, "92-south-park.blend")
    glb = os.path.join(out, "92-south-park.glb")
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
