"""Deterministic Blender build of the SF-SIM miniature 132 South Park.

    blender -b --python build_132_south_park.py -- [--out DIR]

Writes 132-south-park.blend and 132-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = the XY bounding-box centre of the built
form, min Z = 0, cornice crest exactly 12.07 m.

Design (see REFERENCE.md for the sources behind every number, and REPORT.md for
the corrections this build made to the plan):

* ONE LOT, TWO BUILDINGS. Block 3775 lot 062 is a surveyed 6.689 x 29.974 m SoMa
  slot on the north-west arc of the South Park oval, at bearing 135.1 deg. It
  carries a 1913 three-storey flats block on the street (10.30 m deep), an OPEN
  COURTYARD 8.70 m long, and a two-storey rear cottage on the back lot line
  (10.98 m deep). The courtyard is a genuine void — no floor plate, nothing
  bridging — because that front/void/rear rhythm is the asset's plan-view
  identity and the only reading available from directly overhead;
* the front block is the only painted twin-bay wood front on this arc: pale lap
  siding, TWO full-height projecting square bays with a blank recessed stair
  strip between them, and butter-yellow trim outlining every edge — corner
  boards, window surrounds, floor belt courses, facade frame and cornice band.
  The trim is the identity and it is exaggerated to 0.22 m so it reads as a
  drawn outline from the app's aerial camera (style bible s.24);
* an oxblood ground-floor base reading as a plinth rather than a storey, with a
  black segmental-arched carriage gate on the south-west half — the passage
  through to the courtyard — and one square sash window on the north-east half;
* a gray shingled hipped false-mansard hood tucked under the cornice, spanning
  between the two bay tops. Modelled as one hipped solid: shingle texture is
  exactly the detail the camera cannot resolve;
* both flanks are party walls over much lower neighbours (126 South Park is
  7.3 m, 136 is 3.2 m), so several metres of each stands exposed. No source
  shows them; they are authored as blank painted siding with a belt-course
  return, which is what a 1913 party wall over a lower neighbour is;
* night state: five of the twelve bay windows lit, scattered across floors and
  across both bays, plus one window on the cottage's courtyard face so the void
  between the two volumes stays legible after dark. Glow surfaces are thin
  shells proud of the opaque glazing (the app renders _Glow in a separate layer
  that is ~12% alpha by day — never author a primary surface as glow).
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

# DataSF parcel acdm-wktn, blklot 3775062 (130-134 South Park), in survey order:
# NE-front, SW-front, SW-rear, NE-rear.
PARCEL_LONLAT = [
    (-122.394473947, 37.781467745),  # NE front — party corner with 126
    (-122.394527901, 37.781425122),  # SW front — party corner with 136
    (-122.394768358, 37.781617054),  # SW rear
    (-122.394714481, 37.781659739),  # NE rear
]

# Lot-frame extents, all metres. s runs along the frontage from the NE party
# line (s=0) to the SW party line; t runs into the lot from the front property
# line (t=0) to the rear line. The two footprints are the 2010 DataSF LiDAR
# polygons (MBLR SF3775062, two parts) corrected for a uniform 1.1 m
# registration offset and snapped to the lot lines — see the plan's 2.3.
FRONT_T0, FRONT_T1 = 0.00, 10.30    # front flats block
REAR_T0, REAR_T1 = 19.00, 29.974    # rear cottage
BAY_PROJ = 0.85                     # bay projection past the front wall (0.55 real, exaggerated)

# Front block levels, metres above the datum (the front block's own ground).
# Every one of these is scaled off the 2021 drone frame against the LiDAR crest:
# at 76.2 px/m the base cap reads 2.06 m, the belt courses 4.9 and 8.0, the hood
# 10.48-11.47 and the cornice band 11.47-12.07. See REPORT.md s.2.
Z_BASE = 2.10        # top of the oxblood plinth
Z_F1 = 4.95
Z_F2 = 8.05
Z_CORN0 = 11.47      # cornice band springs here — it hangs BELOW the deck
Z_DECK = 11.77       # roof membrane — LiDAR median 11.77, sigma 0.36
Z_CREST = 12.07      # cornice crest — LiDAR max, and the target height
Z_HOOD0, Z_HOOD1 = 10.45, 11.50     # shingled hipped hood

# Window bands, all three floors, measured off the same frame.
WIN_BANDS = ((2.45, 4.51), (5.31, 7.16), (8.36, 10.28))

# Rear cottage. The plan's 0.60 m buried skirt is NOT built — see REPORT.md s.3:
# it cannot coexist with the min Z ~ 0 contract, and the 0.48 m ground difference
# it guarded against is a seam between two LiDAR source tiles, not topography.
Z_R_F1 = 3.94
Z_R_DECK = 8.40
Z_R_CREST = 8.75

TRIM = 0.16          # window-surround board width — near the real 0.15, because
                     # widening THIS eats the glass the facade is mostly made of
TRIM_CB = 0.18       # corner boards and belt courses, where the exaggeration goes
TRIM_REL = 0.05      # trim relief off the wall face
BEVEL_BIG = 0.06
BEVEL_SMALL = 0.03

PALETTE_HEX = {
    "Toy_cream": "f2ede3",    # front block lap siding
    "Toy_mustard": "d9a441",  # ALL trim — the identity, and the whole accent budget
    "Toy_red": "c4453c",      # oxblood ground-floor base
    "Toy_glass": "2a4d73",    # every window
    "Toy_roofd": "45454a",    # shingled hood, carriage gate leaf
    "Toy_steel": "9aa0a6",    # roof membranes, vent stacks, skylight frame
    "Toy_ink": "3a3530",      # opening recesses, arch soffit
    "Toy_sand": "ece4d4",     # rear cottage walls
    "Toy_rust": "a86444",     # courtyard deck and stair
    # Warm lamplight, not a brighter pane of glass: the night proposition for
    # this asset is "someone is home" on an arc of dark commercial roofs.
    # Toy_gold_Glow is the established warm-window glow across the shipped set.
    "Toy_gold_Glow": "caa64a",
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
_ORIGIN = (_P[0][0], -_P[0][1])                       # NE front corner, in Blender XY
_DU = (_P[1][0] - _P[0][0], -(_P[1][1] - _P[0][1]))   # along the frontage
_DV = (_P[3][0] - _P[0][0], -(_P[3][1] - _P[0][1]))   # into the lot
FRONTAGE = math.hypot(*_DU)
DEPTH = math.hypot(*_DV)
U_HAT = (_DU[0] / FRONTAGE, _DU[1] / FRONTAGE)
V_HAT = (_DV[0] / DEPTH, _DV[1] / DEPTH)

# Provisional centring; main() re-centres on the measured bounding box and
# reports the corrected anchor.
_CTR_S = FRONTAGE / 2.0
_CTR_T = (-BAY_PROJ + DEPTH) / 2.0


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


# The bay faces and the outward normals of the four lot edges.
N_FRONT = (-V_HAT[0], -V_HAT[1])   # 135.1 deg SE — the South Park front
N_NE = (-U_HAT[0], -U_HAT[1])      # 45.2 deg  — party line with 126
N_SW = (U_HAT[0], U_HAT[1])        # 225.2 deg — party line with 136
N_REAR = (V_HAT[0], V_HAT[1])      # 315.1 deg — back lot line


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


def st_box(name, s0, s1, t0, t1, z0, z1, mat, mat_top=None):
    """Closed box on the lot grid. Faces: 4 walls, bottom, top."""
    corners = [st(s0, t0), st(s1, t0), st(s1, t1), st(s0, t1)]
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [
        (3, 2, 1, 0),          # bottom
        (4, 5, 6, 7),          # top
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    if mat_top:
        return new_mesh(name, verts, faces, [mat, mat_top], [0, 1, 0, 0, 0, 0])
    return new_mesh(name, verts, faces, [mat])


def st_ring(name, s0, s1, t0, t1, z0, z1, thickness, mat):
    """A closed band following a rectangle's outline: an outer box shell with the
    inner face pulled in by `thickness`. Four quad loops, no caps needed
    because the band is a closed solid ring."""
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


def hipped_hood(name, s0, s1, t0, t1, z0, z1, hip, mat, hip_t=0.0):
    """A hipped solid: rectangular base at z0, shrunk top at z1, hipped by `hip`
    at both ends of s and pulled back by `hip_t` along t. Used for the
    false-mansard hood, whose real form is a shingled apron with angled ends.

    `hip_t` defaults to 0 on purpose: a hood that slopes back in t disappears
    behind the bays it is supposed to cross, which is how the first build read
    as a dark box floating over the recessed centre and nothing else."""
    base = [st(s0, t0), st(s1, t0), st(s1, t1), st(s0, t1)]
    top = [
        st(s0 + hip, t0 + hip_t),
        st(s1 - hip, t0 + hip_t),
        st(s1 - hip, t1),
        st(s0 + hip, t1),
    ]
    verts = [(x, y, z0) for x, y in base] + [(x, y, z1) for x, y in top]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


def wall_panel(name, side, along0, along1, z0, z1, d0, d1, mat):
    """Closed slab lying in the plane of one wall, extruded from offset d0 to d1
    along that wall's outward normal.

    `side` selects the wall and what `along` means:
      'front' / 'rear' -> along is s, the wall plane is t = FRONT_T0 / REAR_T1
      'ne' / 'sw'      -> along is t, the wall plane is s = 0 / FRONTAGE
    """
    if side == "front":
        pts = [(along0, FRONT_T0), (along1, FRONT_T0)]
        n = N_FRONT
    elif side == "rear":
        pts = [(along0, REAR_T1), (along1, REAR_T1)]
        n = N_REAR
    elif side == "ne":
        pts = [(0.0, along0), (0.0, along1)]
        n = N_NE
    elif side == "sw":
        pts = [(FRONTAGE, along0), (FRONTAGE, along1)]
        n = N_SW
    else:
        raise ValueError(side)

    base = [st(*p) for p in pts]
    quad = []
    for d in (d0, d1):
        for (bx, by) in base:
            quad.append((bx + n[0] * d, by + n[1] * d))
    # quad = [a@d0, b@d0, a@d1, b@d1]
    a0, b0, a1, b1 = quad
    ring = [a0, b0, b1, a1]
    verts = [(x, y, z0) for x, y in ring] + [(x, y, z1) for x, y in ring]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
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


# wall_panel()'s d offsets run along the wall's OUTWARD normal, so every layer
# of an opening is built with INCREASING d and each inner layer must protrude
# past the one around it to be seen. Same device as artifacts/181-south-park.
D_SURROUND = 0.06
D_REVEAL = 0.09
D_GLASS = 0.13
D_GLOW = (0.12, 0.17)


def window(tag, side, a0, a1, z0, z1, base_d, glow=False, trim=TRIM):
    """A trim surround, a dark reveal ring inside it, and a glass panel inside
    that. Three closed solids, no booleans. `base_d` is the wall-face offset the
    surround sits on — the bay faces stand BAY_PROJ proud of the front wall.
    `trim` is narrowed on the bay returns, which are only 0.85 m deep."""
    m_trim, m_ink, m_glass = material("Toy_mustard"), material("Toy_ink"), material("Toy_glass")
    wall_panel(f"{tag}_surround", side, a0, a1, z0, z1, base_d, base_d + D_SURROUND, m_trim)
    wall_panel(
        f"{tag}_reveal", side, a0 + trim, a1 - trim, z0 + trim, z1 - trim,
        base_d, base_d + D_REVEAL, m_ink,
    )
    g = 0.03
    wall_panel(
        f"{tag}_glass", side, a0 + trim + g, a1 - trim - g, z0 + trim + g, z1 - trim - g,
        base_d, base_d + D_GLASS, m_glass,
    )
    if glow:
        h = 0.06
        wall_panel(
            f"{tag}_glow", side, a0 + trim + h, a1 - trim - h, z0 + trim + h, z1 - trim - h,
            base_d + D_GLOW[0], base_d + D_GLOW[1], material("Toy_gold_Glow"),
        )


def belt(tag, side, a0, a1, z, base_d):
    """A yellow belt course at a floor line."""
    wall_panel(
        f"{tag}", side, a0, a1, z - TRIM_CB / 2, z + TRIM_CB / 2,
        base_d, base_d + TRIM_REL, material("Toy_mustard"),
    )


def bay_window(tag, s0, s1, z0, z1, base_d, lit):
    """The bay's window group: one wide surround, one dark reveal, glass split by
    a central mullion. The reference frame shows the bay fronts as almost all
    glass — two small punched openings read as a warehouse, not as flats."""
    m_trim, m_ink, m_glass = material("Toy_mustard"), material("Toy_ink"), material("Toy_glass")
    wall_panel(f"{tag}_surround", "front", s0, s1, z0, z1, base_d, base_d + D_SURROUND, m_trim)
    a0, a1 = s0 + TRIM, s1 - TRIM
    b0, b1 = z0 + TRIM, z1 - TRIM
    wall_panel(f"{tag}_reveal", "front", a0, a1, b0, b1, base_d, base_d + D_REVEAL, m_ink)
    mid = (a0 + a1) / 2.0
    g = 0.03
    for li, (g0, g1) in enumerate(((a0 + g, mid - 0.09), (mid + 0.09, a1 - g))):
        wall_panel(f"{tag}_glass{li}", "front", g0, g1, b0 + g, b1 - g,
                   base_d, base_d + D_GLASS, m_glass)
        if lit:
            h = 0.06
            wall_panel(f"{tag}_glow{li}", "front", g0 + h, g1 - h, b0 + g + h, b1 - g - h,
                       base_d + D_GLOW[0], base_d + D_GLOW[1], material("Toy_gold_Glow"))
    wall_panel(f"{tag}_mullion", "front", mid - 0.07, mid + 0.07, b0, b1,
               base_d, base_d + D_GLASS + 0.02, m_trim)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    m_cream = material("Toy_cream")
    m_mustard = material("Toy_mustard")
    m_red = material("Toy_red")
    m_roofd = material("Toy_roofd")
    m_steel = material("Toy_steel")
    m_ink = material("Toy_ink")
    m_sand = material("Toy_sand")
    m_rust = material("Toy_rust")

    S = FRONTAGE
    # bay layout across the frontage: bay | centre stair strip | bay
    BAY_W = 2.80
    CTR0, CTR1 = BAY_W, S - BAY_W

    # ============================================================ FRONT BLOCK

    st_box("front_base", 0, S, FRONT_T0, FRONT_T1, 0.0, Z_BASE, m_red)
    st_box("front_body", 0, S, FRONT_T0, FRONT_T1, Z_BASE, Z_DECK, m_cream, mat_top=m_steel)
    # Cornice: a closed ring around all four walls, hanging from Z_CORN0 so the
    # band reads 0.60 m deep as the reference frame shows. Its front leg follows
    # the BAY face line, not the wall line — in the photo the band runs straight
    # across above both bays and the recessed centre alike.
    st_ring("front_cornice", -0.12, S + 0.12, -BAY_PROJ - 0.12, FRONT_T1 + 0.12,
            Z_CORN0, Z_CREST, 0.34, m_mustard)
    # base cap: a mustard band on top of the oxblood plinth
    for side, a0, a1, d in (("front", 0.0, S, 0.0),
                            ("ne", FRONT_T0, FRONT_T1, 0.0),
                            ("sw", FRONT_T0, FRONT_T1, 0.0)):
        belt(f"basecap_{side}", side, a0, a1, Z_BASE, d)

    # --- the two bays -------------------------------------------------------
    for tag, s0, s1 in (("bayNE", 0.0, BAY_W), ("baySW", CTR1, S)):
        st_box(f"{tag}", s0, s1, -BAY_PROJ, FRONT_T0 + 0.05, Z_BASE, Z_DECK,
               m_cream, mat_top=m_steel)
        # corner boards: a vertical trim strip on each outer edge of the bay face
        for k, edge in enumerate((s0, s1)):
            e0, e1 = (edge, edge + TRIM_CB) if k == 0 else (edge - TRIM_CB, edge)
            wall_panel(f"{tag}_cb{k}", "front", e0, e1, Z_BASE, Z_CORN0,
                       BAY_PROJ, BAY_PROJ + TRIM_REL, m_mustard)
        # and one down each bay return, so the bay reads as an outlined box
        side = "ne" if tag == "bayNE" else "sw"
        wall_panel(f"{tag}_cbret", side, -BAY_PROJ, -BAY_PROJ + TRIM_CB, Z_BASE, Z_CORN0,
                   0.0, TRIM_REL + 0.01, m_mustard)

    # belt courses at each floor line, across the recessed centre and both bays
    for zi, z in enumerate((Z_F1, Z_F2)):
        belt(f"belt_front{zi}", "front", 0.0, S, z, 0.0)
        belt(f"belt_bayNE{zi}", "front", 0.0, BAY_W, z, BAY_PROJ)
        belt(f"belt_baySW{zi}", "front", CTR1, S, z, BAY_PROJ)

    # --- bay windows: one wide two-light group per bay face per floor -------
    # Night: five of the twelve lights lit, scattered. Never a full grid.
    LIT = {("bayNE", 1), ("baySW", 0), ("baySW", 2)}
    GROUP_W = 2.28
    for tag, b0 in (("bayNE", 0.0), ("baySW", CTR1)):
        inset = (BAY_W - GROUP_W) / 2.0
        for fi, (za, zb) in enumerate(WIN_BANDS):
            bay_window(f"{tag}_w{fi}", b0 + inset, b0 + BAY_W - inset, za, zb,
                       BAY_PROJ, lit=(tag, fi) in LIT)
    # --- the shingled hipped hood ------------------------------------------
    # Spans the full facade width in the reference frame, sitting ON the bay
    # face plane (not the wall plane, or it reads as a dark box floating over
    # the recessed centre), hipped at both ends, tucked under the cornice.
    hipped_hood("hood", 0.10, S - 0.10, -BAY_PROJ - 0.12, FRONT_T0 + 0.05,
                Z_HOOD0, Z_CORN0, 0.55, m_roofd)

    # --- the oxblood base: carriage gate (NE half), sash window (SW half) ---
    # The 2021 frame is unambiguous: the arched gate sits against the party wall
    # shared with 126 South Park, i.e. the s = 0 end, and the sash window is on
    # the s = 6.7 end. Read the photo with north-east on the RIGHT.
    G0, G1 = 0.15, 2.75
    wall_panel("gate_recess", "front", G0, G1, 0.0, 1.55, 0.0, 0.03, m_ink)
    wall_panel("gate_leaf", "front", G0 + 0.11, G1 - 0.11, 0.0, 1.46, 0.0, 0.07, m_roofd)
    # arch head: stepped courses approximating a segmental arch, no booleans
    ARCH_STEPS = 5
    for i in range(ARCH_STEPS):
        f = (i + 1) / (ARCH_STEPS + 1)
        inset = (G1 - G0) / 2.0 * (1.0 - math.cos(f * math.pi / 2.0)) * 0.62
        z0 = 1.55 + i * 0.09
        z1 = z0 + 0.09
        wall_panel(f"arch_r{i}", "front", G0 + inset, G1 - inset, z0, z1, 0.0, 0.03, m_ink)
        wall_panel(f"arch_l{i}", "front", G0 + inset + 0.11, G1 - inset - 0.11, z0, z1,
                   0.0, 0.07, m_roofd)
    for k, (t0, t1) in enumerate(((G0 - TRIM, G0), (G1, G1 + TRIM))):
        wall_panel(f"gate_trim{k}", "front", t0, t1, 0.0, 2.00, 0.0, TRIM_REL, m_mustard)

    W0, W1 = 3.75, 5.45
    window("gwin", "front", W0, W1, 0.72, 1.82, 0.0)

    # --- flanks: blank party walls, belts returning only round the corner ---
    # 126 South Park is 7.3 m and 136 is 3.2 m, so several metres of each flank
    # stands exposed. No source shows either. A short trim return is honest; a
    # full-depth belt course would be invented articulation.
    for side in ("ne", "sw"):
        for zi, z in enumerate((Z_F1, Z_F2)):
            belt(f"belt_{side}{zi}", side, FRONT_T0, FRONT_T0 + 0.80, z, 0.0)

    # --- roof furniture -----------------------------------------------------
    # Both stay UNDER the cornice crest: the crest is the target height, so
    # nothing may out-top it, and a 0.30 m parapet ring hiding small roof
    # furniture is what the reference photo shows from street level anyway.
    st_box("skylight", 2.55, 3.65, 6.60, 7.50, Z_DECK, Z_DECK + 0.20, m_steel)
    for i, s in enumerate((1.35, 5.20)):
        st_box(f"stack{i}", s - 0.14, s + 0.14, 8.30, 8.58, Z_DECK, Z_CREST - 0.02, m_steel)

    # ============================================================ REAR COTTAGE

    st_box("rear_body", 0, S, REAR_T0, REAR_T1, 0.0, Z_R_DECK, m_sand, mat_top=m_steel)
    st_ring("rear_parapet", -0.06, S + 0.06, REAR_T0 - 0.06, REAR_T1 + 0.06,
            Z_R_DECK, Z_R_CREST, 0.26, m_sand)

    # Three punched openings per floor on the courtyard (south-east) face; the
    # rear and both flanks stay blank — no source shows them.
    for fi, (za, zb) in enumerate(((0.95, 2.95), (4.60, 6.90))):
        for wi, s0 in enumerate((0.65, 2.80, 4.95)):
            _cottage_window(f"cot_w{fi}{wi}", s0, s0 + 1.05, za, zb,
                            glow=(fi == 1 and wi == 1))

    # courtyard deck and external stair against the cottage's courtyard face
    st_box("court_deck", 1.05, 3.65, REAR_T0 - 1.60, REAR_T0, 0.0, 0.42, m_rust)
    for i in range(5):
        st_box(f"court_step{i}", 0.20, 1.05, REAR_T0 - 1.60 + i * 0.32,
               REAR_T0 - 1.28 + i * 0.32, 0.0, 0.10 + i * 0.09, m_rust)

    # ------------------------------------------------------------ bevel pass
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_glass", "_glow")):
            continue
        if obj.name.endswith(("_surround", "_reveal", "_leaf")) or obj.name.startswith(
            ("belt_", "arch_", "gate_trim")
        ):
            bevel(obj, width=BEVEL_SMALL, segments=1)
        else:
            bevel(obj, width=BEVEL_BIG, segments=1)

    return scene


def _cottage_window(tag, s0, s1, z0, z1, glow=False):
    """A window on the rear cottage's courtyard face — the plane t = REAR_T0,
    whose outward normal is the front bearing 135.1 deg."""
    m_ink, m_glass, m_sand = material("Toy_ink"), material("Toy_glass"), material("Toy_sand")
    n = N_FRONT

    def slab(name, a0, a1, za, zb, d0, d1, mat):
        base = [st(a0, REAR_T0), st(a1, REAR_T0)]
        ring = []
        for d in (d0, d1):
            ring.append((base[0][0] + n[0] * d, base[0][1] + n[1] * d))
            ring.append((base[1][0] + n[0] * d, base[1][1] + n[1] * d))
        ring = [ring[0], ring[1], ring[3], ring[2]]
        verts = [(x, y, za) for x, y in ring] + [(x, y, zb) for x, y in ring]
        faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        return new_mesh(name, verts, faces, [mat])

    # Same outward-increasing convention as window(): each inner layer must
    # protrude past the one around it or it is buried in the wall.
    slab(f"{tag}_surround", s0 - 0.12, s1 + 0.12, z0 - 0.12, z1 + 0.12, 0.0, 0.05, m_sand)
    slab(f"{tag}_reveal", s0, s1, z0, z1, 0.0, 0.08, m_ink)
    slab(f"{tag}_glass", s0 + 0.03, s1 - 0.03, z0 + 0.03, z1 - 0.03, 0.0, 0.11, m_glass)
    if glow:
        slab(f"{tag}_glow", s0 + 0.09, s1 - 0.09, z0 + 0.09, z1 - 0.09,
             0.10, 0.14, material("Toy_gold_Glow"))


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

    # The provisional lot-frame centre, moved by the same XY correction.
    # Blender y = -world z, so a +dy move in Blender is a -dy move in world z.
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
    print(f"[build] front bearing={bearing(N_FRONT):.1f} NE flank={bearing(N_NE):.1f} "
          f"SW flank={bearing(N_SW):.1f} rear={bearing(N_REAR):.1f}")
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

    blend = os.path.join(out, "132-south-park.blend")
    glb = os.path.join(out, "132-south-park.glb")
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
