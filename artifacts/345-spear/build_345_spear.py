"""Deterministic Blender build of the SF-SIM miniature 345 Spear Street (Hills Plaza).

    blender -b --python build_345_spear.py -- [--out DIR]

Writes 345-spear.blend and 345-spear.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint OBB centre (anchor lon -122.3900655,
lat 37.7900324), min Z = 0, tower crest exactly 68.50 m.

Design (see REFERENCE.md for the sources behind every number):

* the OSM footprint (relation 12734194) simplified from 40 vertices to the 22
  that carry form: the Spear entry recess, the plaza notch at the 2 Harrison
  corner, the Folsom service recess, and the FOUR-STEP TERRACE STAIRCASE on the
  Embarcadero/plaza corner are all real plan geometry and all read from the air;
* the recognition cue is the 18-storey white residential tower ROTATED 45 deg
  OFF THE STREET GRID — aligned true N-S to face the bay square-on, a diamond
  against SoMa's diagonal roofs (measured off the nadir ortho, corroborated by
  Street View from the Embarcadero where its face reads dead flat). Floors 8-18
  are the 67 "One Hills Plaza" condos (Buehler Engineering; DataSF lists exactly
  67 condo lots at 75 Folsom in block 3744);
* heights: tower crest 68.50 m = DataSF LiDAR hgt_max, accepted because the
  12.4 m std reflects real stepped massing and 7 office floors + 11 residential
  + crown lands at 63-66 m + mechanicals; podium wings 24.2 m (LiDAR mode) with
  street frontages to 29.4 m (LiDAR median 28.4); the terracotta hip pavilion
  on Spear is ESTIMATED at 35.8 m crest;
* the courtyard hole in the OSM multipolygon is real - a sunken court SW of the
  tower - and the level-8 roof garden on the Folsom/Embarcadero quadrant is the
  top-surface hero (the camera looks down; roofs are facades);
* the ground-floor arcade of round-headed arches on the Embarcadero and plaza
  faces answers the 1926 Hills Brothers arches next door (2 Harrison is a
  SEPARATE landmark in a parallel session - nothing of it is modelled here);
* night state: the arcade arches are the hero glow (Toy_white_Glow), supported
  by a thin gold crown band on the tower and a scatter of lit tower windows.
  Glow surfaces are thin shells proud of the opaque surface behind them.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters
#
# Building frame: a = bearing 315 deg (toward Folsom, "NW"), b = bearing 45 deg
# (toward the Embarcadero, "NE"). World: x = east, y = north.
# a,b -> world:  x = (b - a) * S45,  y = (a + b) * S45.

S45 = math.sqrt(0.5)


def ab_to_world(a, b):
    return ((b - a) * S45, (a + b) * S45)


# Simplified outer ring, CCW in the (a, b) frame (verified CCW in world after
# conversion - the frame is a pure rotation, not a reflection).
# Walk: W corner -> Spear frontage (entry recess) -> plaza notch -> SE plaza
# side -> four-step Embarcadero staircase -> Embarcadero edge -> Folsom edge
# (service recess) -> close.
FOOTPRINT_AB = [
    (48.7, -41.7),   # W corner (Spear x Folsom)
    (19.7, -41.9),   # Spear frontage
    (19.7, -37.0),   # entry recess, north jamb
    (3.4, -37.2),    # entry recess, rear
    (3.4, -41.6),    # entry recess, south jamb
    (-35.0, -41.7),  # Spear frontage, south end
    (-35.0, -27.7),  # plaza notch (open corner shared with 2 Harrison)
    (-48.6, -27.7),  # SE (plaza) side
    (-48.6, 9.8),    # staircase step 0 (SE corner of the terraces)
    (-39.5, 9.9),    # step 1
    (-39.5, 19.1),
    (-30.3, 19.1),   # step 2
    (-30.3, 28.1),
    (-21.3, 28.1),   # step 3
    (-21.3, 37.4),
    (-12.3, 37.4),   # step 4
    (-12.3, 41.9),   # Embarcadero edge, SE end
    (48.6, 42.0),    # N corner (Folsom x Embarcadero)
    (48.7, 4.2),     # Folsom edge
    (44.3, 4.2),     # service recess
    (44.3, -13.2),
    (48.7, -13.2),   # back out to the Folsom plane
]

# The OSM inner ring (the sunken court SW of the tower), grid-aligned.
COURT_AB = [(-19.8, -8.2), (15.2, -8.2), (15.2, 6.1), (-19.8, 6.1)]

# Heights (see REFERENCE.md 3.x)
Z_PODIUM = 24.2      # LiDAR mode - the wing roofs and the garden deck
Z_FRONT = 29.4       # street-frontage bars (LiDAR median 28.4 + parapet)
Z_PAV_BODY = 31.0    # pavilion attic body
Z_PAV_EAVE = 31.8    # eaves slab top
Z_PAV_CREST = 35.8   # hip roof apex (ESTIMATED)
Z_TWR_BODY = 57.8    # tower main shaft roof
Z_TWR_SET = 64.3     # setback top floors (17-18)
Z_TWR_PAR = 65.0     # setback parapet
Z_CREST = 68.5       # mechanical penthouse = bbox top = LiDAR hgt_max
Z_ARC0, Z_ARC1 = 0.0, 6.2   # arcade storey
ARCH_H = 5.4                 # arch opening crest
ARCH_W = 3.6
Z_STORE0, Z_STORE1 = 0.6, 4.6  # Spear/Folsom storefront band

FLOOR_H = 3.55       # podium floor rhythm (0..24.2 in ~6 lifts above arcade)
PIER_PITCH = 8.6
PIER_W = 1.15
PIER_PROJ = 0.18

# Tower plan: axis-aligned in WORLD (the 45 deg rotation cue), centred just NE
# of the court.
TWR_C = (13.0, 11.0)      # world x, y
TWR_W, TWR_D = 23.0, 34.0  # E-W, N-S
SET_W, SET_D = 19.0, 29.0
MECH_W, MECH_D = 9.0, 13.0

PALETTE_HEX = {
    "Toy_sand": "ece4d4",    # buff brick podium
    "Toy_stone": "d9d2c2",   # base, arcade piers, decks
    "Toy_trim": "f3efe6",    # precast bands, parapets
    "Toy_white": "f7f4ec",   # tower precast
    "Toy_glass": "2a4d73",   # windows
    "Toy_glassl": "6f95b8",  # skylight monitor
    "Toy_navy": "2c4a70",    # storefront band
    "Toy_brick": "c96f4a",   # pavilion terracotta hip
    "Toy_roofd": "45454a",   # mech, court floor accents
    "Toy_steel": "9aa0a6",   # plant
    "Toy_mint": "8fd0a8",    # planting
    "Toy_ink": "3a3530",     # tree trunks, entry recess shadow
    "Toy_white_Glow": "f7f4ec",  # arcade at night (hero)
    "Toy_gold_Glow": "caa64a",   # crown band + entry sign
    "Toy_glass_Glow": "6f95b8",  # lit tower windows (scatter)
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

FOOTPRINT = [ab_to_world(a, b) for a, b in FOOTPRINT_AB]
COURT = [ab_to_world(a, b) for a, b in COURT_AB]


def signed_area(poly):
    s = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return s / 2.0


if signed_area(FOOTPRINT) < 0:
    FOOTPRINT.reverse()
if signed_area(COURT) < 0:
    COURT.reverse()

# --------------------------------------------------------------- 2D helpers


def edge_frame(poly, i):
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])
    return a, length, t, n


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


def arch_profile(w, z0, z1, segs=10):
    """Rectangle with a semicircular head; z1 is the crest of the arch."""
    r = w / 2.0
    spring = z1 - r
    pts = [(-r, z0), (r, z0), (r, spring)]
    for k in range(1, segs):
        th = math.pi * k / segs
        pts.append((r * math.cos(th), spring + r * math.sin(th)))
    pts.append((-r, spring))
    return pts


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


def bevel(obj, width=0.10, segments=2):
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


def prism(name, poly, z0, z1, mat, mat_caps=None):
    npts = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces, face_mats = [], []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
        face_mats.append(0)
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    face_mats += [1 if mat_caps else 0] * 2
    mats = [mat, mat_caps] if mat_caps else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def wall_panel(name, frame, u_centre, profile, d0, d1, mat):
    a, t, n = frame
    verts = []
    for d in (d0, d1):
        for du, z in profile:
            px = a[0] + t[0] * (u_centre + du) + n[0] * d
            py = a[1] + t[1] * (u_centre + du) + n[1] * d
            verts.append((px, py, z))
    npts = len(profile)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0):
    c, s = math.cos(yaw), math.sin(yaw)
    corners = []
    for lx, ly in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)):
        corners.append((cx + lx * c - ly * s, cy + lx * s + ly * c))
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


YAW_GRID = math.atan2(*reversed(ab_to_world(1.0, 0.0)))  # bearing of +a in world


def grid_box(name, a, b, z0, z1, sa, sb, mat):
    """Box aligned to the BUILDING grid, placed by (a, b) centre."""
    cx, cy = ab_to_world(a, b)
    # +a axis in world:
    ax, ay = ab_to_world(1.0, 0.0)
    yaw = math.atan2(ay, ax)
    return box(name, cx, cy, z0, z1, sa, sb, mat, yaw=yaw)


def pyramid(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0, apex_frac=0.0):
    """Hip roof: rectangular base to a ridge point (or short ridge)."""
    c, s = math.cos(yaw), math.sin(yaw)

    def w(lx, ly, z):
        return (cx + lx * c - ly * s, cy + lx * s + ly * c, z)

    hx, hy = sx / 2.0, sy / 2.0
    ridge = apex_frac * hx
    verts = [
        w(-hx, -hy, z0),
        w(hx, -hy, z0),
        w(hx, hy, z0),
        w(-hx, hy, z0),
        w(-ridge, 0.0, z1),
        w(ridge, 0.0, z1),
    ]
    faces = [
        (3, 2, 1, 0),
        (0, 1, 5, 4),
        (2, 3, 4, 5),
        (1, 2, 5),
        (3, 0, 4),
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
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------------- parts


def frontage_edges():
    """Indices of the FOOTPRINT edges that face a street, with a role tag."""
    tags = {}
    n = len(FOOTPRINT_AB)
    for i in range(n):
        (a1, b1), (a2, b2) = FOOTPRINT_AB[i], FOOTPRINT_AB[(i + 1) % n]
        length = math.hypot(a2 - a1, b2 - b1)
        if length < 3.0:
            continue
        if abs(b1 + 41.7) < 1.0 and abs(b2 + 41.7) < 1.0:
            tags[i] = "spear"
        elif abs(b1 - 42.0) < 0.6 and abs(b2 - 42.0) < 0.6:
            tags[i] = "embarcadero"
        elif abs(a1 - 48.7) < 0.5 and abs(a2 - 48.7) < 0.5 and length > 20:
            tags[i] = "folsom"
        elif abs(a1 + 48.6) < 0.5 and abs(a2 + 48.6) < 0.5:
            tags[i] = "plaza"
        elif abs(b1 - b2) < 0.3 and 8.0 < length < 12.0 and b1 > 5:
            tags[i] = "step"  # staircase wing-end faces (face NE)
    return tags


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    sand = material("Toy_sand")
    stone = material("Toy_stone")
    trim = material("Toy_trim")
    white = material("Toy_white")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    navy = material("Toy_navy")
    brick = material("Toy_brick")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    mint = material("Toy_mint")
    ink = material("Toy_ink")
    white_glow = material("Toy_white_Glow")
    gold_glow = material("Toy_gold_Glow")
    glass_glow = material("Toy_glass_Glow")

    # --- podium shell -------------------------------------------------------
    # One prism for the whole footprint; the court is a separate recessed
    # floor plate (no boolean) whose walls are the court prism's sides.
    prism("body", FOOTPRINT, 0.0, Z_PODIUM, sand, mat_caps=stone)
    # The sunken court, drawn as a DARK panel on the deck (the 501-second light
    # court lesson: from directly overhead a real recess throws no shadow, so a
    # 10 cm dark panel reads exactly like a court and costs no boolean).
    prism("court_panel", COURT, Z_PODIUM + 0.03, Z_PODIUM + 0.11, roofd)
    court_edge = [ab_to_world(a, b) for a, b in
                  [(-20.6, -9.0), (16.0, -9.0), (16.0, 6.9), (-20.6, 6.9)]]
    if signed_area(court_edge) < 0:
        court_edge.reverse()
    prism("court_border", court_edge, Z_PODIUM + 0.02, Z_PODIUM + 0.09, trim)
    # Planting ribbon + paving spine inside the court
    grid_box("court_green", -2.3, -4.6, Z_PODIUM + 0.11, Z_PODIUM + 0.42, 28.0, 3.0, mint)
    grid_box("court_paving", -2.3, 1.8, Z_PODIUM + 0.11, Z_PODIUM + 0.24, 24.0, 3.2, stone)

    # --- street-frontage upper bars (podium -> 29.4) -------------------------
    # L-bar: Spear strip + Folsom strip, with the entry recess carried up.
    upper_ab = [
        (48.7, -41.7),
        (19.7, -41.9),
        (19.7, -37.0),
        (3.4, -37.2),
        (3.4, -41.6),
        (-35.0, -41.7),
        (-35.0, -28.2),
        (35.2, -28.0),
        (35.2, 8.0),
        (48.7, 8.0),
    ]
    upper = [ab_to_world(a, b) for a, b in upper_ab]
    if signed_area(upper) < 0:
        upper.reverse()
    prism("upper_bar", upper, Z_PODIUM, Z_FRONT, sand, mat_caps=stone)
    # SE plaza wing keeps a slightly lower attic (27.0)
    se_ab = [(-35.6, -27.7), (-48.6, -27.7), (-48.6, 9.8), (-39.5, 9.9), (-39.4, -8.0), (-35.6, -8.0)]
    se = [ab_to_world(a, b) for a, b in se_ab]
    if signed_area(se) < 0:
        se.reverse()
    prism("se_wing", se, Z_PODIUM, 27.0, sand, mat_caps=stone)

    # --- parapets on the podium roof edges (only where no bar stands) --------
    tags = frontage_edges()
    for i, tag in tags.items():
        if tag in ("embarcadero", "step", "plaza"):
            a0, length, t, n = edge_frame(FOOTPRINT, i)
            wall_panel(
                f"parapet_{i}",
                (a0, t, n),
                length / 2.0,
                rect_profile(length, Z_PODIUM, Z_PODIUM + 1.1),
                -0.35,
                0.05,
                trim,
            )

    # --- facade rhythm: piers + floor bands on street faces ------------------
    for i, tag in tags.items():
        a0, length, t, n = edge_frame(FOOTPRINT, i)
        frame = (a0, t, n)
        top = Z_FRONT if tag in ("spear", "folsom") else Z_PODIUM
        # storefront/arcade storey treatment
        if tag in ("spear", "folsom"):
            wall_panel(
                f"store_{i}", frame, length / 2.0,
                rect_profile(max(length - 3.0, 2.0), Z_STORE0, Z_STORE1),
                0.02, 0.14, navy,
            )
        # piers
        n_piers = max(int(length / PIER_PITCH), 1)
        pitch = length / n_piers
        for k in range(n_piers + 1):
            u = min(max(k * pitch, PIER_W / 2), length - PIER_W / 2)
            wall_panel(
                f"pier_{i}_{k}", frame, u,
                rect_profile(PIER_W, Z_ARC1 if tag in ("embarcadero", "plaza", "step") else Z_STORE1, top - 0.9),
                0.0, PIER_PROJ, sand,
            )
        # floor bands: recessed glass strip per floor
        z = Z_ARC1 + 1.0
        while z + 1.7 < top - 0.9:
            wall_panel(
                f"band_{i}_{int(z*10)}", frame, length / 2.0,
                rect_profile(length - 1.2, z, z + 1.7),
                0.03, 0.10, glass,
            )
            z += FLOOR_H
        # cornice
        wall_panel(
            f"cornice_{i}", frame, length / 2.0,
            rect_profile(length, top - 0.9, top - 0.3),
            0.0, 0.55, trim,
        )

    # --- the arcade: round arches on the Embarcadero, plaza and step faces ---
    for i, tag in tags.items():
        if tag not in ("embarcadero", "plaza", "step"):
            continue
        a0, length, t, n = edge_frame(FOOTPRINT, i)
        frame = (a0, t, n)
        n_arch = max(int(length / 7.4), 1)
        pitch = length / n_arch
        for k in range(n_arch):
            u = (k + 0.5) * pitch
            wall_panel(
                f"arch_frame_{i}_{k}", frame, u,
                arch_profile(ARCH_W + 0.9, 0.0, ARCH_H + 0.45), 0.0, 0.22, stone,
            )
            wall_panel(
                f"arch_fill_{i}_{k}", frame, u,
                arch_profile(ARCH_W, 0.0, ARCH_H), 0.0, 0.30, glass,
            )
            wall_panel(
                f"arch_glow_{i}_{k}", frame, u,
                arch_profile(ARCH_W - 0.5, 0.0, ARCH_H - 0.3), 0.26, 0.34, white_glow,
            )

    # --- Spear entry: recessed jamb walls carry ink shadow + gold sign -------
    # (the recess itself is real plan geometry, edges 1-4 of FOOTPRINT)
    rec_i = 2  # edge from (19.7,-37.0) to (3.4,-37.2): the recess rear wall
    a0, length, t, n = edge_frame(FOOTPRINT, rec_i)
    frame = (a0, t, n)
    wall_panel("entry_dark", frame, length / 2.0, rect_profile(length - 1.0, 0.0, 5.6), 0.02, 0.10, ink)
    wall_panel(
        "entry_sign_glow", frame, length / 2.0, rect_profile(7.0, 4.6, 5.3), 0.10, 0.18, gold_glow
    )
    wall_panel("entry_canopy", frame, length / 2.0, rect_profile(length - 0.6, 5.6, 6.1), 0.0, 3.2, stone)

    # --- the terracotta hip pavilion on Spear ---------------------------------
    grid_box("pav_body", 35.2, -29.7, Z_PODIUM, Z_PAV_BODY, 24.0, 23.9, sand)
    grid_box("pav_eave", 35.2, -29.7, Z_PAV_BODY, Z_PAV_BODY + 0.35, 26.4, 26.3, trim)
    cx, cy = ab_to_world(35.2, -29.7)
    ax, ay = ab_to_world(1.0, 0.0)
    pyramid(
        "pav_hip", cx, cy, Z_PAV_BODY + 0.35, Z_PAV_CREST, 26.4, 26.3, brick,
        yaw=math.atan2(ay, ax), apex_frac=0.06,
    )
    grid_box("pav_finial", 35.2, -29.7, Z_PAV_CREST - 0.1, Z_PAV_CREST + 0.0, 0.9, 0.9, trim)

    # --- the tower: world-axis-aligned (the 45 deg cue) -----------------------
    tx, ty = TWR_C
    # glazing core + white corner piers + spandrel rings
    box("twr_core", tx, ty, Z_PODIUM - 2.0, Z_TWR_BODY, TWR_W - 0.6, TWR_D - 0.6, glass)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(
                f"twr_pier_{sx}_{sy}",
                tx + sx * (TWR_W / 2 - 1.4),
                ty + sy * (TWR_D / 2 - 1.4),
                0.0, Z_TWR_BODY + 0.4, 2.8, 2.8, white,
            )
    z = Z_PODIUM + 1.15
    k = 0
    while z < Z_TWR_BODY - 1.2:
        box(f"twr_band_{k}", tx, ty, z, z + 1.15, TWR_W, TWR_D, white)
        z += 3.2
        k += 1
    # base of the tower below podium reads as podium mass from outside
    box("twr_base", tx, ty, 0.0, Z_PODIUM + 0.1, TWR_W, TWR_D, sand)
    # lit-window scatter (night support): thin proud plates on two faces
    # each plate sits centred in a GLASS strip between spandrel bands (bands
    # start at 25.35 + 3.2k, 1.15 tall; strips span [26.5+3.2k, 28.55+3.2k]) —
    # a plate overlapping a band z-range gets provably buried inside the band
    # solid and stage 4's interior-face pass would gut it (learned here).
    for j, (fy, wz) in enumerate(
        ((1, 33.4), (1, 43.0), (-1, 36.6), (-1, 49.4), (1, 52.6), (-1, 27.0))
    ):
        box(
            f"twr_lit_{j}",
            tx + (j % 3 - 1) * 5.5,
            ty + fy * (TWR_D / 2 - 0.22),
            wz, wz + 1.05, 3.6, 0.12, glass_glow,
        )
    # crown: setback floors, parapet, gold band, mechanical penthouse
    box("twr_set", tx, ty, Z_TWR_BODY, Z_TWR_SET, SET_W, SET_D, white)
    box("twr_par", tx, ty, Z_TWR_SET, Z_TWR_PAR, SET_W + 0.7, SET_D + 0.7, trim)
    box("twr_gold", tx, ty, Z_TWR_SET - 0.65, Z_TWR_SET - 0.20, SET_W + 0.10, SET_D + 0.10, gold_glow)
    box("twr_mech", tx, ty, Z_TWR_PAR, Z_CREST, MECH_W, MECH_D, roofd)
    box("twr_roof", tx, ty, Z_TWR_BODY - 0.05, Z_TWR_BODY + 0.25, TWR_W + 0.3, TWR_D + 0.3, stone)

    # --- level-8 roof garden on the Folsom/Embarcadero quadrant ---------------
    # deck sits on the podium cap; garden is the top-surface hero
    grid_box("garden_deck", 33.0, 20.0, Z_PODIUM, Z_PODIUM + 0.22, 29.0, 40.0, stone)
    grid_box("garden_lawn1", 39.0, 12.0, Z_PODIUM + 0.22, Z_PODIUM + 0.55, 12.0, 16.0, mint)
    grid_box("garden_lawn2", 27.0, 30.0, Z_PODIUM + 0.22, Z_PODIUM + 0.55, 10.0, 12.0, mint)
    # circular feature (the fountain visible in the ortho)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=14, radius=3.4, depth=0.7,
        location=(*ab_to_world(36.0, 24.0), Z_PODIUM + 0.35),
    )
    fount = bpy.context.object
    fount.name = "garden_fountain"
    fount.data.materials.append(trim)
    fount.data.shade_flat()
    # chunky trees: ink trunk + mint crown
    for j, (ta, tb) in enumerate(
        ((22.0, 14.0), (42.5, 15.0), (30.5, 35.5), (42.0, 29.5), (21.5, 25.0))
    ):
        wx, wy = ab_to_world(ta, tb)
        grid_box(f"tree_trunk_{j}", ta, tb, Z_PODIUM + 0.2, Z_PODIUM + 1.6, 0.5, 0.5, ink)
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=10, ring_count=7, radius=1.9, location=(wx, wy, Z_PODIUM + 2.9)
        )
        crown = bpy.context.object
        crown.name = f"tree_crown_{j}"
        crown.data.materials.append(mint)
        crown.data.shade_flat()

    # --- wing roofscape --------------------------------------------------------
    # S wing skylight monitor (the Google atrium)
    grid_box("skylight_base", -16.0, -31.0, Z_PODIUM, Z_PODIUM + 0.9, 21.0, 12.0, stone)
    grid_box("skylight_glass", -16.0, -31.0, Z_PODIUM + 0.9, Z_PODIUM + 1.7, 19.0, 10.0, glassl)
    # mech blocks, grouped
    for j, (ma, mb, sa, sb, h) in enumerate(
        (
            (-27.0, 12.0, 5.0, 3.4, 1.9),
            (-33.0, 4.0, 3.6, 2.8, 1.5),
            (5.0, -20.0, 4.2, 3.0, 1.6),
            (-43.0, -14.0, 3.2, 2.6, 1.4),
        )
    ):
        grid_box(f"mech_{j}", ma, mb, Z_PODIUM + 0.0, Z_PODIUM + h, sa, sb, steel)
    # upper-bar roof: tidy vents
    for j, (ma, mb) in enumerate(((10.0, -34.0), (-8.0, -34.5), (42.0, -2.0), (28.0, -34.2))):
        grid_box(f"vent_{j}", ma, mb, Z_FRONT, Z_FRONT + 0.7, 1.4, 1.4, roofd)
    # terrace planters on the staircase steps, inboard of each step's parapet
    for j, (ma, mb) in enumerate(((-44.0, 6.2), (-35.0, 15.2), (-26.0, 24.2), (-16.8, 33.4))):
        grid_box(f"terrace_planter_{j}", ma, mb, Z_PODIUM + 0.0, Z_PODIUM + 0.75, 6.0, 1.4, mint)

    # --- bevels ---------------------------------------------------------------
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        nm = obj.name
        if nm.startswith(("arch_fill", "arch_glow", "twr_lit", "twr_gold", "entry_sign", "band_")):
            continue
        if nm.startswith(("pier_", "arch_frame", "vent_", "tree_", "terrace_", "court_green")):
            bevel(obj, width=0.05, segments=1)
        else:
            bevel(obj, width=0.11, segments=2)

    return scene


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


ANCHOR_LON, ANCHOR_LAT = -122.3900655, 37.7900324


def recenter():
    """The manifest anchor is the model's bbox centre (placeGeneric puts the GLB
    origin at the anchor), but this footprint is authored around its OBB centre,
    which for a diagonal, asymmetric plan is NOT the AABB centre. Shift the
    whole model so bbox centre xy = 0 and derive the manifest anchor lon/lat."""
    from mathutils import Matrix

    objs, _tris, mn, mx = measure()
    cx = (mn.x + mx.x) / 2.0
    cy = (mn.y + mx.y) / 2.0
    shift = Matrix.Translation((-cx, -cy, 0.0))
    for o in objs:
        # bake the full transform into the mesh so every object ships applied
        o.data.transform(shift @ o.matrix_world)
        o.matrix_world = Matrix.Identity(4)
    bpy.context.view_layer.update()
    lon = ANCHOR_LON + cx / (111320.0 * math.cos(math.radians(37.77)))
    lat = ANCHOR_LAT + cy / 110540.0
    print(f"[build] recentred by ({-cx:.3f}, {-cy:.3f}) m")
    print(f"[build] MANIFEST anchor (bbox centre): {lon:.7f} {lat:.7f}")
    print(f"[build] registry/exclusion anchor (OBB centre): {ANCHOR_LON} {ANCHOR_LAT}")
    return lon, lat


def report():
    objs, tris, mn, mx = measure()
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    print("[build] Spear frontage faces SW (225 deg); Embarcadero faces NE (45 deg)")
    print("[build] tower is WORLD-axis-aligned (45 deg off the street grid) by design")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    recenter()
    report()

    blend = os.path.join(out, "345-spear.blend")
    glb = os.path.join(out, "345-spear.glb")
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
