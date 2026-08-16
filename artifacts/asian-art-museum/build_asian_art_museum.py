"""Deterministic Blender build of the SF-SIM miniature Asian Art Museum.

    blender -b --python build_asian_art_museum.py -- [--out DIR]

Writes asian-art-museum.blend and asian-art-museum.glb next to this file (or
into --out). Geometry is authored in metres, Z up, +X east, +Y true north,
origin at the footprint bbox centre, min Z = 0, crest normalised to 28.10 m.

Design (see REFERENCE.md for the sources behind every number):

* the plan is NOT a rectangle. OSM way/24588037, reprojected into the Civic
  Center street grid, is a 106.60 x 54.71 m envelope that steps BACK on the
  north-east (the north wall jogs 9.7 m then 4.2 m south past E=62.5) and on
  the south-east (the south wall jogs 12.9 m north past E=93.6). Four grid
  rectangles reproduce it to within 2% on area;
* one continuous Beaux-Arts envelope all the way round - rusticated granite
  base, giant order, entablature at 22.6 m, attic to 24.2 m. The unbroken
  cornice is recognition cue #1 and is never interrupted;
* the Larkin (west) hero front: ten chunky columns between two solid end
  pavilions, each pierced by a tall arched opening, over eight steps that
  become one three-tread plinth and three bronze doors;
* the Fulton (south) long arcade: fourteen arched openings, the longest
  rhythm on the building and the Civic Center axis elevation;
* a designed roof, because 4,900 m2 of it faces the camera: dark low-slope
  deck, two light courts with plant and plant-room clusters, the raised
  hipped monitor that IS the 28.10 m crest, and - over the eastern third -
  wHY's 2023 pale terracotta pavilion and the sculpture terrace;
* flat Toy_* materials only. Two glow surfaces: the colonnade uplight cove
  and the three entrance doors.

The OSM height=46 tag is NOT used: it is the NAVD88 roof elevation. Heights
come from the DataSF LiDAR record (crest 28.10 m, roof plane 23.22 m).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

# ---------------------------------------------------------------- parameters

# Footprint in the street-grid frame: E runs 0 (Larkin/west) -> 106.60
# (Hyde/east), S runs 0 (McAllister/north) -> 54.71 (Fulton/south).
E_LEN = 106.60
S_LEN = 54.71
GRID_ROT = math.radians(8.32)  # long axis bearing 81.68 deg = 8.32 deg N of E

# The four grid rectangles that reproduce the OSM polygon (E0, E1, S0, S1).
CELLS = [
    (0.0, 62.5, 0.0, 54.71),
    (62.5, 70.0, 11.5, 54.71),
    (70.0, 93.6, 15.75, 54.71),
    (93.6, 106.6, 15.75, 41.78),
]

# The same envelope as one rectilinear outline, CCW in (E, S). Jogs under 2 m
# in the surveyed polygon are absorbed; area error against OSM is under 2%.
OUTLINE = [
    (0.0, 0.0),
    (62.5, 0.0),
    (62.5, 11.5),
    (70.0, 11.5),
    (70.0, 15.75),
    (106.6, 15.75),
    (106.6, 41.78),
    (93.6, 41.78),
    (93.6, 54.71),
    (0.0, 54.71),
]

Z_BASE = 6.5       # rusticated granite base
Z_CAP = 7.0        # base cap course
Z_BODY = 19.5      # top of the giant order
Z_CORN = 22.6      # top of the entablature - the cornice line (LiDAR 23.22 deck)
Z_ATTIC = 24.2     # top of the attic parapet
Z_DECK = 23.2      # roof plane (DataSF hgt_median_m)
Z_CREST = 28.10    # DataSF hgt_maxcm - the raised central monitor

PROUD_CAP = 0.35
PROUD_CORN = 0.90
PROUD_ATTIC = 0.35
INSET = 1.2        # roof deck inset inside the attic

# Light courts (grid frame), shared S range, different widths - as surveyed
COURT_A = (7.0, 25.0, 11.0, 43.0)
COURT_B = (30.0, 42.0, 11.0, 43.0)
Z_COURT = 19.9  # court floor: the deck reads as a 3.3 m well, which is enough

MONITOR = (46.0, 60.0, 18.0, 36.0)
Z_MON_WALL = 25.6

# 2023 wHY work over the eastern third
TERRACE_E0 = 70.0
Z_TERRACE = 23.4
PAVILION = (73.0, 99.0, 18.0, 28.0)
Z_PAV = 26.0

COLS = 8           # west colonnade
PAV_END = 9.0      # solid end pavilion width on the Larkin front
ARCADE = 14        # south (Fulton) arched bays
NORTH_BAYS = 9
NE_BAYS = 4

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
    "Toy_coral": "e8735a",
    "Toy_steel": "9aa0a6",
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


def arch_panel(name, e_c, half_w, s_face, z0, z_spring, z_top, matname, out, segs=7):
    """A thin arch-topped panel standing proud of a south/north facade plane."""
    pts = [(e_c - half_w, z0), (e_c + half_w, z0), (e_c + half_w, z_spring)]
    r = half_w
    for i in range(1, segs):
        a = math.pi * i / segs
        pts.append((e_c + r * math.cos(a), z_spring + (z_top - z_spring) * math.sin(a)))
    pts.append((e_c - half_w, z_spring))
    verts = []
    faces = []
    n = len(pts)
    for depth in (0.0, out):
        for e, z in pts:
            x, y = grid_to_local(e, s_face + depth)
            verts.append((x, y, z))
    faces.append(list(range(n - 1, -1, -1)))
    faces.append(list(range(n, 2 * n)))
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, j, j + n, i + n])
    return new_mesh(name, verts, faces, matname, 0.0)


def cylinder(name, e_c, s_c, r, z0, z1, matname, segs=12, bevel_w=0.0):
    poly = []
    for i in range(segs):
        a = 2 * math.pi * i / segs
        poly.append(grid_to_local(e_c + r * math.cos(a), s_c + r * math.sin(a)))
    return prism(name, poly, z0, z1, matname, bevel_w)


def hip_roof(name, e0, e1, s0, s1, z0, z1, ridge_in, matname):
    """A four-sided hipped cap: rectangle at z0 rising to a short ridge at z1."""
    c = [grid_to_local(e0, s0), grid_to_local(e1, s0), grid_to_local(e1, s1), grid_to_local(e0, s1)]
    xs = [p[0] for p in c]
    ys = [p[1] for p in c]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    ym = (y0 + y1) * 0.5
    verts = [
        (x0, y0, z0),
        (x1, y0, z0),
        (x1, y1, z0),
        (x0, y1, z0),
        (x0 + ridge_in, ym, z1),
        (x1 - ridge_in, ym, z1),
    ]
    faces = [
        [3, 2, 1, 0],
        [0, 1, 5, 4],
        [1, 2, 5],
        [2, 3, 4, 5],
        [3, 0, 4],
    ]
    return new_mesh(name, verts, faces, matname, BEVEL_W)


# ------------------------------------------------------------------- massing


def offset_outline(d):
    """Mitred offset of the rectilinear OUTLINE by d (positive = outward)."""
    n = len(OUTLINE)
    area = 0.0
    for i in range(n):
        e0, s0 = OUTLINE[i]
        e1, s1 = OUTLINE[(i + 1) % n]
        area += e0 * s1 - e1 * s0
    sign = 1.0 if area > 0 else -1.0  # normalise to CCW in (E, S)
    out = []
    for i in range(n):
        pe, ps = OUTLINE[i - 1]
        ce, cs = OUTLINE[i]
        ne, ns = OUTLINE[(i + 1) % n]
        nx = 0.0
        ny = 0.0
        for (ae, a_s), (be, bs) in (((pe, ps), (ce, cs)), ((ce, cs), (ne, ns))):
            dx, dy = be - ae, bs - a_s
            ln = math.hypot(dx, dy)
            if ln < 1e-9:
                continue
            nx += sign * dy / ln  # outward normal of a CCW edge
            ny += sign * -dx / ln
        out.append((ce + d * nx, cs + d * ny))
    return out


def outline_prism(name, d, z0, z1, matname, bevel_w=BEVEL_W):
    poly = [grid_to_local(e, s) for e, s in offset_outline(d)]
    if polygon_area(poly) < 0:
        poly.reverse()
    return prism(name, poly, z0, z1, matname, bevel_w)


def polygon_area(poly):
    a = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        a += x0 * y1 - x1 * y0
    return a * 0.5


def outline_ring(name, d_out, d_in, z0, z1, matname, bevel_w=BEVEL_W):
    """A closed rectilinear ring - the cornice and attic parapet."""
    outer = [grid_to_local(e, s) for e, s in offset_outline(d_out)]
    inner = [grid_to_local(e, s) for e, s in offset_outline(d_in)]
    if polygon_area(outer) < 0:
        outer.reverse()
        inner.reverse()
    n = len(outer)
    verts = (
        [(p[0], p[1], z0) for p in outer]
        + [(p[0], p[1], z1) for p in outer]
        + [(p[0], p[1], z0) for p in inner]
        + [(p[0], p[1], z1) for p in inner]
    )
    O0, O1, I0, I1 = 0, n, 2 * n, 3 * n
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append([O0 + i, O0 + j, O1 + j, O1 + i])          # outer wall
        faces.append([I1 + i, I1 + j, I0 + j, I0 + i])          # inner wall
        faces.append([O1 + i, O1 + j, I1 + j, I1 + i])          # top
        faces.append([I0 + i, I0 + j, O0 + j, O0 + i])          # bottom
    return new_mesh(name, verts, faces, matname, bevel_w)


def build_envelope():
    # Rusticated granite base with three proud coursing ledges.
    outline_prism("base", 0.0, 0.0, Z_BASE, "Toy_stone")
    for k, z in enumerate((1.55, 3.10, 4.65)):
        outline_prism(f"rustic{k}", 0.18, z, z + 0.28, "Toy_stone", bevel_w=0.05)
    outline_prism("basecap", PROUD_CAP, Z_BASE, Z_CAP, "Toy_trim")
    outline_prism("body", 0.0, Z_CAP, Z_BODY, "Toy_cream")
    # Cornice and attic are RINGS: the roof they enclose is the asset's largest
    # surface and must not be buried under a solid slab.
    outline_ring("entab", PROUD_CORN, -1.6, Z_BODY, Z_CORN, "Toy_trim")
    outline_ring("attic", PROUD_ATTIC, -1.45, Z_CORN, Z_ATTIC, "Toy_trim")


def build_roof():
    """Dark low-slope deck in the west, pale terrace in the east, courts between."""
    ax0, ax1, ay0, ay1 = COURT_A
    bx0, bx1, by0, by1 = COURT_B
    n_edge, s_edge = INSET, 54.71 - INSET
    zt = Z_BODY  # the deck springs off the top of the body, inside the cornice

    # West block deck with the two court voids cut out.
    slabs = [
        (INSET, 61.3, n_edge, ay0),
        (INSET, 61.3, ay1, s_edge),
        (INSET, ax0, ay0, ay1),
        (ax1, bx0, ay0, ay1),
        (bx1, 61.3, ay0, ay1),
        (61.3, 68.8, 12.7, s_edge),
        (68.8, TERRACE_E0, 16.95, s_edge),
    ]
    for i, (e0, e1, s0, s1) in enumerate(slabs):
        box(f"deck_w{i}", e0, e1, s0, s1, zt, Z_DECK, "Toy_roofd")

    # Light courts: the deck reads as a well down to a pale floor, with a plant
    # cluster in one and planting in the other (style bible s.10).
    for tag, (e0, e1, s0, s1) in (("a", COURT_A), ("b", COURT_B)):
        box(f"court_{tag}_floor", e0, e1, s0, s1, zt, Z_COURT, "Toy_stone")
    for i, (e, s, w, d, h) in enumerate(
        [(9.5, 15.0, 5.5, 4.5, 2.4), (17.5, 21.5, 4.5, 3.6, 1.8), (11.0, 33.0, 6.5, 5.0, 2.0)]
    ):
        box(f"court_plant{i}", e, e + w, s, s + d, Z_COURT, Z_COURT + h, "Toy_steel", bevel_w=0.08)
    for i, (e, s) in enumerate([(32.0, 14.0), (32.0, 25.0), (32.0, 36.0)]):
        box(f"court_green{i}", e, e + 8.0, s, s + 5.5, Z_COURT, Z_COURT + 1.0, "Toy_mint", bevel_w=0.08)

    # The raised central monitor - this is the 28.10 m crest.
    me0, me1, ms0, ms1 = MONITOR
    box("monitor", me0, me1, ms0, ms1, Z_DECK - 0.5, Z_MON_WALL, "Toy_cream")
    box("monitor_cornice", me0 - 0.55, me1 + 0.55, ms0 - 0.55, ms1 + 0.55, Z_MON_WALL - 0.7, Z_MON_WALL, "Toy_trim", bevel_w=0.08)
    hip_roof("monitor_cap", me0 - 0.9, me1 + 0.9, ms0 - 0.9, ms1 + 0.9, Z_MON_WALL, Z_CREST, 3.6, "Toy_roofd")
    for i in range(3):
        s = ms0 + 2.6 + i * 4.6
        box(f"monitor_glassS{i}", me0 - 0.10, me0 + 0.5, s, s + 3.0, Z_DECK + 0.6, Z_MON_WALL - 1.4, "Toy_glass")
        box(f"monitor_glassN{i}", me1 - 0.5, me1 + 0.10, s, s + 3.0, Z_DECK + 0.6, Z_MON_WALL - 1.4, "Toy_glass")
    for i in range(3):
        e = me0 + 2.4 + i * 4.4
        box(f"monitor_glassW{i}", e, e + 2.8, ms0 - 0.10, ms0 + 0.5, Z_DECK + 0.6, Z_MON_WALL - 1.4, "Toy_glass")
        box(f"monitor_glassE{i}", e, e + 2.8, ms1 - 0.5, ms1 + 0.10, Z_DECK + 0.6, Z_MON_WALL - 1.4, "Toy_glass")

    # --- the 2023 wHY work: pale terracotta pavilion + sculpture terrace ----
    box("terrace_1", TERRACE_E0, 92.4, 16.95, s_edge, zt, Z_TERRACE, "Toy_sand")
    box("terrace_2", 92.4, E_LEN - INSET, 16.95, 41.78 - INSET, zt, Z_TERRACE, "Toy_sand")
    box("terrace_rail", TERRACE_E0 - 0.7, TERRACE_E0, 16.95, s_edge, Z_TERRACE, Z_TERRACE + 1.2, "Toy_trim", bevel_w=0.06)

    pe0, pe1, ps0, ps1 = PAVILION
    box("pavilion", pe0, pe1, ps0, ps1, Z_TERRACE, Z_PAV, "Toy_sand")
    for i in range(4):
        e_c = pe0 + 3.0 + (pe1 - pe0 - 6.0) * i / 3.0
        box(f"pavilion_win{i}", e_c - 2.2, e_c + 2.2, ps1 - 0.02, ps1 + 0.12, Z_PAV - 1.9, Z_PAV - 0.55, "Toy_glass")
    box("pavilion_skylight", pe1 - 9.0, pe1 - 1.0, ps0 + 1.0, ps1 - 1.0, Z_PAV - 0.05, Z_PAV + 0.12, "Toy_glass")

    for i, (e, s) in enumerate([(87.0, 34.0), (96.5, 30.5), (91.5, 40.0)]):
        cylinder(f"sculpture{i}", e, s, 1.7, Z_TERRACE, Z_TERRACE + 2.4, "Toy_coral", segs=10, bevel_w=0.10)
    box("terrace_planter0", 74.0, 86.0, 46.0, 50.0, Z_TERRACE, Z_TERRACE + 1.0, "Toy_mint", bevel_w=0.08)
    box("terrace_planter1", 90.0, 101.0, 30.0, 34.0, Z_TERRACE, Z_TERRACE + 1.0, "Toy_mint", bevel_w=0.08)

    # One tidy plant cluster on the otherwise blank stretch of dark deck east
    # of the monitor - the camera looks down on it (style bible s.10).
    for i, (e, s, w, d, h) in enumerate(
        [(62.5, 22.0, 5.5, 6.0, 2.3), (62.5, 30.0, 4.0, 4.5, 1.6), (63.5, 42.0, 6.0, 5.0, 1.9)]
    ):
        box(f"deck_plant{i}", e, e + w, s, s + d, Z_DECK, Z_DECK + h, "Toy_steel", bevel_w=0.08)


def build_west_front():
    """Larkin Street: the hero elevation - colonnade, end pavilions, steps."""
    span0, span1 = PAV_END, S_LEN - PAV_END
    pitch = (span1 - span0) / COLS

    # Glazed bays sit on the wall plane; the columns in front make them read
    # as deep recesses without a single boolean.
    # One continuous stylobate and one continuous abacus band, so the order
    # reads as a colonnade rather than a picket fence.
    box("west_stylobate", -2.55, 0.3, span0 - 1.4, span1 + 1.4, Z_CAP - 0.55, Z_CAP + 0.30, "Toy_trim", bevel_w=0.08)
    box("west_abacus", -2.55, 0.3, span0 - 1.4, span1 + 1.4, Z_BODY - 0.85, Z_BODY, "Toy_trim", bevel_w=0.08)
    for i in range(COLS):
        s_c = span0 + pitch * (i + 0.5)
        box(f"west_bay{i}", -0.08, 0.6, s_c - 1.75, s_c + 1.75, 8.2, 18.4, "Toy_glass")
        cylinder(f"west_col{i}", -1.25, s_c, 1.15, Z_CAP + 0.30, Z_BODY - 0.85, "Toy_trim", segs=12, bevel_w=0.10)

    # Solid end pavilions, each pierced by one tall arched opening.
    for i, s_c in enumerate((PAV_END * 0.5, S_LEN - PAV_END * 0.5)):
        pts = []
        half = 2.5
        z0, z_spring, z_top = 9.0, 14.6, 18.6
        segs = 7
        pts = [(s_c - half, z0), (s_c + half, z0), (s_c + half, z_spring)]
        for k in range(1, segs):
            a = math.pi * k / segs
            pts.append((s_c + half * math.cos(a), z_spring + (z_top - z_spring) * math.sin(a)))
        pts.append((s_c - half, z_spring))
        verts = []
        faces = []
        n = len(pts)
        for depth in (0.0, 0.55):
            for s, z in pts:
                x, y = grid_to_local(-0.08 + depth, s)
                verts.append((x, y, z))
        faces.append(list(range(n - 1, -1, -1)))
        faces.append(list(range(n, 2 * n)))
        for k in range(n):
            j = (k + 1) % n
            faces.append([k, j, j + n, k + n])
        new_mesh(f"west_arch{i}", verts, faces, "Toy_glass")

    # Eight steps, semantically compressed into one chunky three-tread plinth.
    for i in range(3):
        w = 13.2 - i * 1.0
        box(f"west_step{i}", -4.9 + i * 1.35, 0.0, S_LEN * 0.5 - w, S_LEN * 0.5 + w, 0.0, 0.9 + i * 0.75, "Toy_stone", bevel_w=0.12)
    # Three sets of bronze doors, set in the rusticated base where they belong
    # and enlarged so they still read from the app's aerial camera (s.9).
    for i in range(3):
        s_c = S_LEN * 0.5 + (i - 1) * 5.4
        box(f"west_door{i}", -0.12, 0.7, s_c - 2.3, s_c + 2.3, 2.4, 6.35, "Toy_gold_Glow")
    # The uplight cove that washes the colonnade at night (hero glow).
    box("west_cove", -1.85, -1.15, span0, span1, Z_CAP - 0.05, Z_CAP + 0.75, "Toy_white_Glow")
    # The incised frieze band reads as one proud course, not letterforms.
    box("west_frieze", -1.30, -0.55, span0 - 1.0, span1 + 1.0, Z_BODY + 0.5, Z_BODY + 1.9, "Toy_trim", bevel_w=0.06)


def build_south_arcade():
    """Fulton Street: the long arcade, the Civic Center axis elevation."""
    e_lo, e_hi = 3.4, 90.2
    pitch = (e_hi - e_lo) / ARCADE
    for i in range(ARCADE):
        e_c = e_lo + pitch * (i + 0.5)
        arch_panel(f"south_arch{i}", e_c, 2.55, 54.71 + 0.08, 7.6, 13.6, 18.5, "Toy_glass", -0.75)
    for i in range(ARCADE + 1):
        e_c = e_lo + pitch * i
        box(f"south_pier{i}", e_c - 0.85, e_c + 0.85, 54.71, 55.10, Z_CAP, Z_BODY, "Toy_cream", bevel_w=0.06)
    # A continuous impost course ties the fourteen bays into one arcade.
    box("south_impost", e_lo - 1.6, e_hi + 1.6, 54.71, 55.32, 13.30, 14.00, "Toy_trim", bevel_w=0.08)
    # The rusticated base is 6.5 m of blank granite otherwise - give it the
    # small square openings the real base carries.
    for i in range(ARCADE):
        e_c = e_lo + pitch * (i + 0.5)
        box(f"south_basewin{i}", e_c - 1.35, e_c + 1.35, 54.71 - 0.10, 54.71 + 0.45, 2.6, 5.3, "Toy_glass")


def build_north_and_east():
    """McAllister and Hyde: quieter rhythms, plus the 2003 glazed bay."""
    pitch = (60.0 - 3.0) / NORTH_BAYS
    for i in range(NORTH_BAYS):
        e_c = 3.0 + pitch * (i + 0.5)
        box(f"north_win{i}", e_c - 1.9, e_c + 1.9, -0.10, 0.5, 9.0, 17.6, "Toy_glass")
        box(f"north_basewin{i}", e_c - 1.35, e_c + 1.35, -0.45, 0.10, 2.6, 5.3, "Toy_glass")
        box(f"north_pier{i}", e_c - pitch * 0.5 - 0.9, e_c - pitch * 0.5 + 0.9, -0.30, 0.0, Z_CAP, Z_BODY, "Toy_cream", bevel_w=0.06)

    pitch2 = (103.0 - 73.0) / NE_BAYS
    for i in range(NE_BAYS):
        e_c = 73.0 + pitch2 * (i + 0.5)
        box(f"ne_win{i}", e_c - 1.9, e_c + 1.9, 15.75 - 0.10, 15.75 + 0.5, 9.0, 17.6, "Toy_glass")

    # Hyde Street: the Aulenti-era glazed bay projecting from the historic wall.
    box("east_bay", E_LEN - 0.1, E_LEN + 1.3, 22.0, 34.0, 8.0, 17.6, "Toy_glass")
    box("east_bay_frame", E_LEN - 0.05, E_LEN + 1.55, 21.4, 22.2, 7.6, 18.1, "Toy_steel", bevel_w=0.06)
    box("east_bay_frame2", E_LEN - 0.05, E_LEN + 1.55, 33.8, 34.6, 7.6, 18.1, "Toy_steel", bevel_w=0.06)
    for i, s_c in enumerate((18.6, 38.0)):
        box(f"east_win{i}", E_LEN - 0.1, E_LEN + 0.5, s_c - 1.4, s_c + 1.4, 9.0, 17.6, "Toy_glass")


# --------------------------------------------------------------- assembly


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    OBJECTS.clear()
    build_envelope()
    build_roof()
    build_west_front()
    build_south_arcade()
    build_north_and_east()

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

    blend = os.path.join(out, "asian-art-museum.blend")
    glb = os.path.join(out, "asian-art-museum.glb")
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
