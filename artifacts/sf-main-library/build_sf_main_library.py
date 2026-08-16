"""Deterministic Blender build of the SF-SIM miniature San Francisco Main Public Library.

    blender -b --python build_sf_main_library.py -- [--out DIR]

Writes sf-main-library.blend and sf-main-library.glb next to this file (or into
--out). Geometry is authored in metres, Z up, +X east, +Y true north, origin at
the footprint bbox centre, min Z = 0, crest normalised to 28.98 m.

Design (see REFERENCE.md for the sources behind every number):

* the plan IS a rectangle. OSM way/24446086, reprojected into the Civic Center
  street grid, is 106.42 x 56.88 m with every corner within 0.25 m of square,
  so no outline machinery is needed. Grid frame: E runs 0 (Larkin/west) ->
  106.42 (Hyde/east), S runs 0 (Fulton/north) -> 56.88 (Grove/south);
* James Ingo Freed's two grammars on one block, which is the whole point of the
  building and the only thing that keeps it from reading as a clone of the
  Asian Art Museum 90 m north. West (Larkin) and north (Fulton) get a proud
  cornice, a pilaster order, and a cresting of studs along the parapet. South
  (Grove) and east (Hyde) get a flush parapet, a dark spandrel band and
  scattered punched windows;
* the Larkin hero front: a centre pavilion pushed 0.8 m proud and raised 1.8 m
  above the flanking parapets, six chunky pilasters, the incised frieze band
  over three bronze doors, an attic of small squares;
* the tall square granite corner pier at Grove & Hyde, the modern face's anchor
  and the only place the silhouette breaks on that side;
* a designed roof, because 6,000 m2 of it faces the camera: pale north strip
  with plant, dark deck, and the four glazed events read off the nadir aerial -
  the circular atrium oculus at (E 54.5, S 36), the 45-degree rotated glazed
  pyramid west of it, and the two big pitched skylight sheds over the eastern
  half whose ridge IS the 28.98 m crest;
* flat Toy_* materials only. Two glow surfaces: the roof glazing lit from the
  atrium below (oculus cone + both sheds) and the three entrance doors. The
  roof glazing is `Toy_glassl_Glow`, not a white: at diorama scale a white cone
  on a white drum reads as a blank disc, and pale blue glass reads as a
  skylight by day and as the lit atrium by night, which is what it is.

The OSM/Overture height=46 tag is NOT used: it is the NAVD88 roof elevation
(153.78 ft), the same trap the Asian Art Museum carries on the identical
number. Heights come from the DataSF LiDAR record: crest 28.98 m
(hgt_maxcm 2898), main roof plane 24.02 m (hgt_mediancm 2402).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

# ---------------------------------------------------------------- parameters

E_LEN = 106.42
S_LEN = 56.88
GRID_ROT = math.radians(9.06)  # long-axis bearing 80.94 deg = 9.06 deg N of E

Z_PLINTH = 2.40     # banded granite base
Z_BODY = 22.60      # top of the wall plane
Z_PAR_C = 24.60     # classical parapet top (N, W) - LiDAR roof plane 24.02
Z_PAR_M = 24.20     # modern parapet top (S, E), deliberately 0.4 m lower
Z_CREST_N = 25.10   # top of the cresting studs on the classical parapets
Z_PAV_PAR = 26.40   # Larkin centre pavilion parapet
Z_PAV_CREST = 26.90
Z_PIER = 27.00      # Grove/Hyde corner pier
Z_DECK = 23.00      # roof deck
Z_NSTRIP = 23.60    # the pale raised strip along the Fulton edge
Z_CREST = 28.98     # DataSF hgt_maxcm - the skylight shed ridge

PROUD_C = 0.70      # classical cornice projection
ORDER_Z0, ORDER_Z1 = 6.00, 20.00
BAND_Z0, BAND_Z1 = 11.40, 12.60   # modern spandrel band

# Larkin centre pavilion, in S
PAV_S0, PAV_S1 = 13.40, 43.40
PAV_OUT = 0.80
COLS = 6

FULTON_BAYS = 14

# Grove/Hyde corner pier
PIER_E0, PIER_S0 = 89.40, 39.90

# Roof events (grid frame)
OCULUS = (54.50, 36.00, 11.00)          # E, S, radius
OCULUS_Z1, OCULUS_APEX = 25.40, 28.10
PYRAMID = (33.00, 35.50, 18.00, 45.0)   # E, S, side, rotation deg
PYRAMID_APEX = 28.20
# Two sheds sharing a valley, as on the nadir aerial. Sized and placed by the
# layout solver in REPORT.md: inside the deck, clear of the oculus and clear of
# the corner pier, which rises to 27 m and would otherwise swallow a ridge.
SHEDS = [                                # E, S, length, width, rot deg, ridge z
    (77.00, 30.00, 22.0, 12.0, 38.0, 28.98),
    (74.00, 43.00, 17.0, 9.0, 34.0, 28.10),
]
MECH = (93.00, 20.00, 10.0, 8.0)         # E0, S0, w, d
Z_MECH = 26.20
SLOT = (12.50, 22.00, 3.0, 28.0)         # E0, S0, w, d
TERRACE = (18.00, 49.50, 16.0, 5.5)

BEVEL_W = 0.12
BEVEL_SEG = 2

PALETTE_HEX = {
    "Toy_cream": "f2ede3",
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_roofd": "45454a",
    "Toy_sand": "ece4d4",
    "Toy_mint": "8fd0a8",
    "Toy_steel": "9aa0a6",
    "Toy_glassl_Glow": "6f95b8",
    "Toy_gold_Glow": "caa64a",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


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
        # Flagged for the app's night pass; emission is off in the daylight asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    return mat


# -------------------------------------------------------------- mesh helpers

OBJECTS = []


def grid_to_local(e, s):
    """Grid frame (E east-along-street, S south-across) -> model XY, unrotated."""
    return (e - E_LEN * 0.5, -(s - S_LEN * 0.5))


def new_mesh(name, verts, faces, matname, bevel_w=0.0):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    mesh.materials.append(material(matname))
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if bevel_w > 0.0:
        bmesh.ops.bevel(
            bm,
            geom=list(bm.verts) + list(bm.edges),
            offset=bevel_w,
            segments=BEVEL_SEG,
            profile=0.5,
            affect="EDGES",
            clamp_overlap=True,
        )
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.shade_flat()
    OBJECTS.append(obj)
    return obj


def prism(name, poly, z0, z1, matname, bevel_w=0.0):
    """Extrude a CCW polygon of (x, y) local points from z0 to z1."""
    n = len(poly)
    verts = [(p[0], p[1], z0) for p in poly] + [(p[0], p[1], z1) for p in poly]
    faces = [list(range(n - 1, -1, -1)), list(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, j, j + n, i + n])
    return new_mesh(name, verts, faces, matname, bevel_w)


def box(name, e0, e1, s0, s1, z0, z1, matname, bevel_w=0.0):
    """Axis-aligned box given in grid-frame E/S bounds."""
    a = grid_to_local(e0, s0)
    b = grid_to_local(e1, s1)
    x0, x1 = min(a[0], b[0]), max(a[0], b[0])
    y0, y1 = min(a[1], b[1]), max(a[1], b[1])
    poly = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return prism(name, poly, z0, z1, matname, bevel_w)


def rot_rect(e_c, s_c, length, width, deg):
    """A rectangle rotated about its centre inside the grid frame."""
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    out = []
    for de, ds in ((-length / 2, -width / 2), (length / 2, -width / 2),
                   (length / 2, width / 2), (-length / 2, width / 2)):
        out.append(grid_to_local(e_c + de * ca - ds * sa, s_c + de * sa + ds * ca))
    return out


def cylinder(name, e_c, s_c, r, z0, z1, matname, segs=16, bevel_w=0.0):
    poly = [grid_to_local(e_c + r * math.cos(2 * math.pi * i / segs),
                          s_c + r * math.sin(2 * math.pi * i / segs))
            for i in range(segs)]
    return prism(name, poly, z0, z1, matname, bevel_w)


def cone(name, e_c, s_c, r, z0, z1, matname, segs=16):
    """A closed cone: a ring at z0 rising to a single apex at z1."""
    poly = [grid_to_local(e_c + r * math.cos(2 * math.pi * i / segs),
                          s_c + r * math.sin(2 * math.pi * i / segs))
            for i in range(segs)]
    verts = [(p[0], p[1], z0) for p in poly]
    cx = sum(p[0] for p in poly) / segs
    cy = sum(p[1] for p in poly) / segs
    verts.append((cx, cy, z1))
    faces = [list(range(segs - 1, -1, -1))]
    for i in range(segs):
        faces.append([i, (i + 1) % segs, segs])
    return new_mesh(name, verts, faces, matname, 0.0)


def pyramid_solid(name, poly, z0, z1, matname):
    """A closed pyramid over a convex polygon."""
    n = len(poly)
    verts = [(p[0], p[1], z0) for p in poly]
    verts.append((sum(p[0] for p in poly) / n, sum(p[1] for p in poly) / n, z1))
    faces = [list(range(n - 1, -1, -1))]
    for i in range(n):
        faces.append([i, (i + 1) % n, n])
    return new_mesh(name, verts, faces, matname, 0.0)


def gable(name, e_c, s_c, length, width, deg, z0, z1, matname):
    """A closed gable roof: a rotated rectangle at z0 rising to a ridge at z1.

    The ridge runs along the rectangle's LENGTH, so the two long slopes are
    what the camera sees.
    """
    q = rot_rect(e_c, s_c, length, width, deg)
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    r0 = grid_to_local(e_c - length / 2 * ca, s_c - length / 2 * sa)
    r1 = grid_to_local(e_c + length / 2 * ca, s_c + length / 2 * sa)
    verts = [(p[0], p[1], z0) for p in q] + [(r0[0], r0[1], z1), (r1[0], r1[1], z1)]
    faces = [
        [3, 2, 1, 0],
        [0, 1, 5, 4],
        [1, 2, 5],
        [2, 3, 4, 5],
        [3, 0, 4],
    ]
    return new_mesh(name, verts, faces, matname, 0.0)


# ------------------------------------------------------------------- massing


def build_envelope():
    """One granite block; the two grammars live in the parapets and the faces."""
    box("plinth", 0, E_LEN, 0, S_LEN, 0.0, Z_PLINTH, "Toy_stone")
    for k, z in enumerate((0.62, 1.24, 1.86)):
        box(f"plinth_band{k}", -0.16, E_LEN + 0.16, -0.16, S_LEN + 0.16,
            z, z + 0.26, "Toy_stone", bevel_w=0.05)
    box("body", 0, E_LEN, 0, S_LEN, Z_PLINTH, Z_BODY, "Toy_cream")

    # Parapets, as four walls rather than one ring: the classical pair (north,
    # west) projects, the modern pair (south, east) is flush and lower. That
    # difference is the asset's single most important read.
    # Four walls that TILE rather than overlap: coincident top faces between two
    # solids z-fight, and a coplanar pair renders as a black patch in Cycles.
    # The classical pair owns both west corners; the modern pair stops short.
    box("par_north", -PROUD_C, E_LEN + PROUD_C, -PROUD_C, 1.60,
        Z_BODY, Z_PAR_C, "Toy_trim", bevel_w=0.08)
    box("par_west", -PROUD_C, 1.60, 1.60, S_LEN + PROUD_C,
        Z_BODY, Z_PAR_C, "Toy_trim", bevel_w=0.08)
    box("par_south", 1.60, E_LEN, S_LEN - 1.45, S_LEN,
        Z_BODY, Z_PAR_M, "Toy_trim", bevel_w=0.08)
    box("par_east", E_LEN - 1.45, E_LEN, 1.60, S_LEN - 1.45,
        Z_BODY, Z_PAR_M, "Toy_trim", bevel_w=0.08)

    # Cresting: a run of small studs along the two classical parapets only.
    pitch = 2.2
    n_e = int((E_LEN - 2.0) / pitch)
    for i in range(n_e):
        e = 1.0 + pitch * (i + 0.5)
        box(f"crest_n{i}", e - 0.22, e + 0.22, 0.30, 0.74,
            Z_PAR_C, Z_CREST_N, "Toy_trim")
    n_s = int((S_LEN - 6.0) / pitch)
    for i in range(n_s):
        s = 3.0 + pitch * (i + 0.5)
        box(f"crest_w{i}", 0.30, 0.74, s - 0.22, s + 0.22,
            Z_PAR_C, Z_CREST_N, "Toy_trim")


def build_west_front():
    """Larkin Street: the raised centre pavilion, the order, the frieze, the doors."""
    box("pav_body", -PAV_OUT, 0.4, PAV_S0, PAV_S1, Z_PLINTH, Z_BODY, "Toy_cream")
    box("pav_plinth", -PAV_OUT, 0.4, PAV_S0, PAV_S1, 0.0, Z_PLINTH, "Toy_stone")
    box("pav_parapet", -PAV_OUT - PROUD_C, 1.6, PAV_S0 - 0.9, PAV_S1 + 0.9,
        Z_BODY, Z_PAV_PAR, "Toy_trim", bevel_w=0.08)
    pitch = 2.2
    n = int((PAV_S1 - PAV_S0) / pitch)
    for i in range(n):
        s = PAV_S0 + 0.5 + pitch * (i + 0.5)
        box(f"crest_pav{i}", -PAV_OUT - 0.35, -PAV_OUT + 0.09, s - 0.22, s + 0.22,
            Z_PAV_PAR, Z_PAV_CREST, "Toy_trim")

    # Six chunky pilasters with glazing between - the giant order, compressed.
    span0, span1 = PAV_S0 + 2.6, PAV_S1 - 2.6
    step = (span1 - span0) / COLS
    for i in range(COLS):
        s_c = span0 + step * (i + 0.5)
        box(f"west_pil{i}", -PAV_OUT - 0.90, -PAV_OUT + 0.05, s_c - 1.10, s_c + 1.10,
            ORDER_Z0, ORDER_Z1, "Toy_trim", bevel_w=0.08)
    for i in range(COLS + 1):
        s0 = span0 + step * i - step * 0.5 + 1.10
        s1 = s0 + step - 2.20
        if s0 < PAV_S0 + 0.8 or s1 > PAV_S1 - 0.8:
            continue
        box(f"west_glass{i}", -PAV_OUT - 0.10, -PAV_OUT + 0.30, s0, s1,
            ORDER_Z0 + 0.9, ORDER_Z1 - 0.9, "Toy_glass")
    # Stylobate and abacus tie the six into one order.
    box("west_stylobate", -PAV_OUT - 1.00, 0.0, PAV_S0 - 0.4, PAV_S1 + 0.4,
        ORDER_Z0 - 0.85, ORDER_Z0, "Toy_trim", bevel_w=0.08)
    box("west_abacus", -PAV_OUT - 1.00, 0.0, PAV_S0 - 0.4, PAV_S1 + 0.4,
        ORDER_Z1, ORDER_Z1 + 0.85, "Toy_trim", bevel_w=0.08)
    # The incised SAN FRANCISCO PUBLIC LIBRARY frieze: one proud course, not letters.
    box("west_frieze", -PAV_OUT - 0.55, -PAV_OUT + 0.05, PAV_S0 + 0.6, PAV_S1 - 0.6,
        4.05, 5.15, "Toy_trim", bevel_w=0.06)
    # Attic of small squares above the order.
    for i in range(9):
        s_c = PAV_S0 + 2.4 + (PAV_S1 - PAV_S0 - 4.8) * i / 8.0
        box(f"west_attic{i}", -PAV_OUT - 0.08, -PAV_OUT + 0.32, s_c - 0.85, s_c + 0.85,
            21.00, 22.10, "Toy_glass")
    # Three sets of bronze doors, semantically enlarged so they read from the air.
    for i in range(3):
        s_c = (PAV_S0 + PAV_S1) * 0.5 + (i - 1) * 5.6
        box(f"west_door{i}", -PAV_OUT - 0.10, -PAV_OUT + 0.55, s_c - 2.10, s_c + 2.10,
            0.30, 3.85, "Toy_gold_Glow")
    # The flanking bays north and south of the pavilion are not blank granite:
    # they carry the same tall windows in a quieter rhythm.
    for i, s_c in enumerate((4.4, 8.2, 48.6, 52.4)):
        box(f"west_flankwin{i}", -0.12, 0.28, s_c - 1.35, s_c + 1.35,
            ORDER_Z0 + 0.9, ORDER_Z1 - 0.9, "Toy_glass")
        box(f"west_flankbase{i}", -0.12, 0.28, s_c - 1.10, s_c + 1.10,
            3.10, 5.10, "Toy_glass")
    # Three treads instead of the real flight.
    for i in range(3):
        half = 13.0 - i * 1.1
        box(f"west_step{i}", -4.30 + i * 1.15, 0.0,
            (PAV_S0 + PAV_S1) * 0.5 - half, (PAV_S0 + PAV_S1) * 0.5 + half,
            0.0, 0.35 + i * 0.30, "Toy_stone", bevel_w=0.10)


def build_north_front():
    """Fulton Street: the second Civic Center face - same order, longer, quieter."""
    lo, hi = 4.0, E_LEN - 4.0
    step = (hi - lo) / FULTON_BAYS
    for i in range(FULTON_BAYS + 1):
        e = lo + step * i
        box(f"north_pil{i}", e - 0.70, e + 0.70, -0.50, 0.05,
            ORDER_Z0, ORDER_Z1, "Toy_trim", bevel_w=0.06)
    for i in range(FULTON_BAYS):
        e_c = lo + step * (i + 0.5)
        box(f"north_glass{i}", e_c - 2.05, e_c + 2.05, -0.12, 0.28,
            ORDER_Z0 + 0.9, ORDER_Z1 - 0.9, "Toy_glass")
        box(f"north_basewin{i}", e_c - 1.50, e_c + 1.50, -0.12, 0.28,
            3.10, 5.10, "Toy_glass")
        box(f"north_attic{i}", e_c - 0.85, e_c + 0.85, -0.12, 0.28,
            21.00, 22.10, "Toy_glass")
    box("north_stylobate", lo - 1.2, hi + 1.2, -0.60, 0.0,
        ORDER_Z0 - 0.75, ORDER_Z0, "Toy_trim", bevel_w=0.08)
    box("north_abacus", lo - 1.2, hi + 1.2, -0.60, 0.0,
        ORDER_Z1, ORDER_Z1 + 0.75, "Toy_trim", bevel_w=0.08)


# The scattered punched openings on the two Market Street faces. Deliberately
# irregular: (position along the face, sill z, width, height). Read off the
# Grove Street elevation photograph, not from drawings - see 2.16 of the plan.
GROVE_WINDOWS = [
    (6.0, 15.4, 2.0, 3.2), (10.5, 6.6, 2.0, 3.2), (14.0, 15.4, 2.0, 2.0),
    (18.5, 19.2, 2.0, 2.0), (23.0, 6.6, 2.0, 3.2), (27.0, 15.4, 2.0, 3.2),
    (31.5, 19.2, 2.0, 2.0), (36.5, 6.6, 2.0, 2.0), (41.0, 15.4, 2.0, 3.2),
    (46.0, 19.2, 2.0, 2.0), (50.0, 6.6, 2.0, 3.2), (55.0, 15.4, 2.0, 2.0),
    (59.5, 19.2, 2.0, 3.2), (64.0, 6.6, 2.0, 2.0), (68.5, 15.4, 2.0, 3.2),
    (73.0, 19.2, 2.0, 2.0), (78.0, 6.6, 2.0, 3.2), (83.0, 15.4, 2.0, 2.0),
]
HYDE_WINDOWS = [
    (5.5, 15.4, 2.0, 3.2), (10.5, 6.6, 2.0, 2.0), (15.0, 19.2, 2.0, 2.0),
    (20.0, 15.4, 2.0, 3.2), (25.5, 6.6, 2.0, 3.2), (30.0, 19.2, 2.0, 2.0),
    (35.0, 15.4, 2.0, 2.0),
]


def build_modern_faces():
    """Grove and Hyde: flat granite, one dark spandrel band, scattered punches."""
    box("grove_band", 0.0, E_LEN, S_LEN - 0.05, S_LEN + 0.40,
        BAND_Z0, BAND_Z1, "Toy_roofd", bevel_w=0.06)
    box("hyde_band", E_LEN - 0.05, E_LEN + 0.40, 0.0, S_LEN,
        BAND_Z0, BAND_Z1, "Toy_roofd", bevel_w=0.06)
    for i, (e, z, w, h) in enumerate(GROVE_WINDOWS):
        box(f"grove_win{i}", e - w / 2, e + w / 2, S_LEN - 0.12, S_LEN + 0.28,
            z, z + h, "Toy_glass")
    for i, (s, z, w, h) in enumerate(HYDE_WINDOWS):
        box(f"hyde_win{i}", E_LEN - 0.12, E_LEN + 0.28, s - w / 2, s + w / 2,
            z, z + h, "Toy_glass")
    # The tall square granite corner pier at Grove & Hyde.
    box("corner_pier", PIER_E0, E_LEN, PIER_S0, S_LEN, 0.0, Z_PIER - 1.05, "Toy_cream")
    for k, z in enumerate((BAND_Z0, 18.60)):
        box(f"pier_band{k}", PIER_E0 - 0.30, E_LEN + 0.30, PIER_S0 - 0.30, S_LEN + 0.30,
            z, z + 1.20, "Toy_roofd", bevel_w=0.06)
    box("pier_cap", PIER_E0 - 0.35, E_LEN + 0.35, PIER_S0 - 0.35, S_LEN + 0.35,
        Z_PIER - 1.15, Z_PIER, "Toy_trim", bevel_w=0.08)
    for i, (e, s, z) in enumerate([(93.0, None, 8.0), (99.0, None, 14.5),
                                   (None, 44.0, 8.0), (None, 50.0, 14.5)]):
        if e is not None:
            box(f"pier_win{i}", e - 1.1, e + 1.1, S_LEN - 0.12, S_LEN + 0.28,
                z, z + 3.0, "Toy_glass")
        else:
            box(f"pier_win{i}", E_LEN - 0.12, E_LEN + 0.28, s - 1.1, s + 1.1,
                z, z + 3.0, "Toy_glass")


def build_roof():
    """The asset's largest surface: pale north strip, dark deck, four glazed events."""
    box("deck", 1.6, E_LEN - 1.45, 1.6, S_LEN - 1.45, 20.0, Z_DECK, "Toy_roofd")
    box("north_strip", 1.6, E_LEN - 1.45, 1.6, 19.0, Z_DECK, Z_NSTRIP,
        "Toy_stone", bevel_w=0.08)
    for i, (e, w, d) in enumerate([(20.0, 3.2, 2.4), (27.0, 2.4, 2.0), (34.0, 3.6, 2.8),
                                   (44.0, 5.0, 3.4), (52.0, 4.2, 3.0), (68.0, 3.0, 2.2),
                                   (77.0, 4.6, 3.2)]):
        box(f"roof_unit{i}", e, e + w, 9.5, 9.5 + d, Z_NSTRIP, Z_NSTRIP + 1.5,
            "Toy_steel", bevel_w=0.08)

    # The long linear skylight slot near the Larkin edge.
    e0, s0, w, d = SLOT
    box("slot_curb", e0 - 0.4, e0 + w + 0.4, s0 - 0.4, s0 + d + 0.4,
        Z_DECK, Z_DECK + 0.55, "Toy_trim", bevel_w=0.06)
    box("slot_glass", e0, e0 + w, s0, s0 + d, Z_DECK + 0.4, Z_DECK + 0.95, "Toy_glass")

    # The circular atrium oculus - recognition cue #1 from the air.
    oe, os_, orad = OCULUS
    cylinder("oculus_drum", oe, os_, orad, Z_DECK - 0.4, OCULUS_Z1, "Toy_trim",
             segs=16, bevel_w=0.08)
    cone("oculus_cone", oe, os_, orad - 0.55, OCULUS_Z1, OCULUS_APEX,
         "Toy_glassl_Glow", segs=16)

    # The glazed pyramid, on the 45-degree grid Freed rotated it onto.
    pe, ps, side, prot = PYRAMID
    q = rot_rect(pe, ps, side, side, prot)
    qc = rot_rect(pe, ps, side + 0.9, side + 0.9, prot)
    prism("pyramid_curb", qc, Z_DECK, Z_DECK + 0.6, "Toy_trim", bevel_w=0.06)
    pyramid_solid("pyramid_glass", q, Z_DECK + 0.5, PYRAMID_APEX, "Toy_glass")

    # The two pitched skylight sheds over the eastern half. The first ridge is
    # the 28.98 m crest.
    for i, (e_c, s_c, ln, wd, rot, zr) in enumerate(SHEDS):
        prism(f"shed_curb{i}", rot_rect(e_c, s_c, ln + 0.9, wd + 0.9, rot),
              Z_DECK, Z_DECK + 0.8, "Toy_trim", bevel_w=0.06)
        gable(f"shed_glass{i}", e_c, s_c, ln, wd, rot, Z_DECK + 0.7, zr, "Toy_glassl_Glow")

    # Mechanical enclosure with three pucks, by the Grove/Hyde corner.
    me, ms, mw, md = MECH
    box("mech", me, me + mw, ms, ms + md, Z_DECK, Z_MECH, "Toy_stone", bevel_w=0.10)
    for i in range(3):
        cylinder(f"mech_puck{i}", me + 2.2 + i * 4.1, ms + md * 0.5, 1.6,
                 Z_MECH, Z_MECH + 1.1, "Toy_roofd", segs=10, bevel_w=0.08)

    for i, (e, s_, w, d, h) in enumerate(
        [(62.0, 47.0, 5.0, 4.2, 2.0), (69.0, 50.0, 3.6, 3.2, 1.5)]
    ):
        box(f"deck_plant{i}", e, e + w, s_, s_ + d, Z_DECK, Z_DECK + h,
            "Toy_steel", bevel_w=0.08)

    # The roof garden PCF&P list in the programme, at the quiet south-west corner.
    te, ts, tw, td = TERRACE
    box("terrace", te, te + tw, ts, ts + td, Z_DECK, Z_DECK + 0.45, "Toy_sand",
        bevel_w=0.06)
    box("terrace_rail", te - 0.35, te + tw + 0.35, ts - 0.35, ts,
        Z_DECK + 0.45, Z_DECK + 1.35, "Toy_trim", bevel_w=0.06)
    for i, (e, w) in enumerate([(te + 1.0, 5.5), (te + 9.0, 5.5)]):
        box(f"terrace_planter{i}", e, e + w, ts + 1.2, ts + 4.0,
            Z_DECK + 0.45, Z_DECK + 1.35, "Toy_mint", bevel_w=0.08)


# --------------------------------------------------------------- assembly


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    OBJECTS.clear()
    build_envelope()
    build_west_front()
    build_north_front()
    build_modern_faces()
    build_roof()

    # Rotate the whole assembly onto the Civic Center grid, then recentre XY
    # and seat it on z = 0. Transforms are applied to the mesh data, so the
    # export needs none.
    rot = Matrix.Rotation(GRID_ROT, 4, "Z")
    for o in OBJECTS:
        o.data.transform(rot)

    mn, mx = bounds()
    shift = Vector((-(mn.x + mx.x) * 0.5, -(mn.y + mx.y) * 0.5, -mn.z))
    for o in OBJECTS:
        o.data.transform(Matrix.Translation(shift))

    # Normalise the crest to exactly Z_CREST so the loader's
    # targetHeightM / measuredHeight scale lands at 1.0.
    mn, mx = bounds()
    if abs(mx.z - Z_CREST) > 1e-6:
        k = Z_CREST / mx.z
        for o in OBJECTS:
            o.data.transform(Matrix.Diagonal((1.0, 1.0, k, 1.0)))


def bounds():
    dg = bpy.context.evaluated_depsgraph_get()
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        me = o.evaluated_get(dg).to_mesh()
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
        o.evaluated_get(dg).to_mesh_clear()
    return mn, mx


def signed_volume(obj, dg):
    me = obj.evaluated_get(dg).to_mesh()
    me.calc_loop_triangles()
    total = 0.0
    mw = obj.matrix_world
    for t in me.loop_triangles:
        a, b, c = (mw @ me.vertices[i].co for i in t.vertices)
        total += a.dot(b.cross(c)) / 6.0
    obj.evaluated_get(dg).to_mesh_clear()
    return total


def report():
    dg = bpy.context.evaluated_depsgraph_get()
    tris = 0
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    inverted = []
    for o in objs:
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        o.evaluated_get(dg).to_mesh_clear()
        if signed_volume(o, dg) <= 0:
            inverted.append(o.name)
    mn, mx = bounds()
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] materials={sorted(m.name for m in bpy.data.materials)}")
    print(f"[build] inverted_solids={inverted}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "sf-main-library.blend")
    glb = os.path.join(out, "sf-main-library.glb")
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
