"""Deterministic Blender build of the SF-SIM miniature Earl Warren Building.

    blender -b --python build_earl_warren_building.py -- [--out DIR]

Writes earl-warren-building.blend and earl-warren-building.glb next to this file
(or into --out). Geometry is authored in metres, Z up, +X east, +Y true north,
origin at the footprint bbox centre, min Z = 0, crest normalised to 27.00 m.

Design (see REFERENCE.md for the sources behind every number):

* the plan is NOT the rectangle the asset plan assumed. OSM way/260137839,
  reprojected into the Civic Center street grid, is a COMB: a continuous
  115.48 m bar along McAllister (south) about 21 m deep, three wings running
  north off it, and two 25 x 9.5 m light courts notched between them, plus
  recessed corners at both north ends. The 16-vertex OUTLINE below is the
  measured polygon, snapped to the grid;
* the south (McAllister) front is the hero and is unbroken end to end:
  rusticated granite base, three carved entrance portals breaking up through
  the string course, then the giant arcade of 19 round-arched bays that is
  recognition cue #1, then a heavy modillion cornice, a light attic and a
  parapet cap at the 27.00 m crest;
* a designed roof, because the camera looks down: dark sloping mansard band
  along McAllister, pale parapet ring, mid-grey deck over the wings, the two
  light courts glazed turquoise (they are what makes this building findable
  from altitude), and the central courtroom lantern with its twin laylights;
* flat Toy_* materials only. Two glow surfaces: the three entrance arch
  soffits with their lantern pucks, and the courtroom laylights.

The LiDAR hgt_max of 46.39 m is NOT used: it is the 54 m Hiram W. Johnson slab
bleeding across a shared party wall. Heights are the parapet crest 27.00 m
(Wikipedia 87 ft, OSM height=27) and the roof plane 25.10 m (DataSF
hgt_median_m 25.11).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

# ---------------------------------------------------------------- parameters

# Grid frame: E runs 0 (Polk/west) -> 115.48 (Larkin/east);
#             S runs 0 (Golden Gate/north) -> 31.52 (McAllister/south).
E_LEN = 115.48
S_LEN = 31.52
GRID_ROT = math.radians(8.67)  # long-axis bearing 81.33 deg = 8.67 deg N of E

# The measured OSM polygon in the grid frame, snapped. Jogs under 0.15 m are
# absorbed; area error against the surveyed polygon is under 1%.
OUTLINE = [
    (0.00, 14.71),
    (5.07, 14.71),
    (5.07, 0.70),
    (19.86, 0.70),
    (19.86, 9.90),
    (44.64, 9.90),
    (44.64, 0.40),
    (70.95, 0.40),
    (70.95, 10.15),
    (96.73, 10.15),
    (96.73, 0.05),
    (110.60, 0.05),
    (110.60, 14.85),
    (115.48, 14.85),
    (115.48, 31.52),
    (0.00, 31.52),
]

Z_PLINTH = 1.00    # granite water table
Z_BASE = 7.20      # rusticated granite base storey
Z_STR = 8.00       # string course above it
Z_SEC = 10.40      # low second storey of square windows
Z_SILL = 11.00     # arcade sill / balustrade band
Z_BODY = 20.00     # top of the giant arcade order
Z_CORN = 22.60     # top of the entablature - the cornice line
Z_ATTIC = 25.40    # top of the attic storey
Z_DECK = 25.10     # roof plane (DataSF hgt_median_m 25.11)
Z_CREST = 27.00    # parapet cap - Wikipedia 87 ft, OSM height=27

PROUD_PLINTH = 0.35
PROUD_STR = 0.50
PROUD_SILL = 0.45
PROUD_CORN = 1.00
INSET_ATTIC = 0.50
INSET_PARAPET = 1.20
INSET_DECK = 2.30

# The two light courts, as measured (E0, E1, S0, S1). Open to the north,
# glazed over well below the roof plane - the turquoise panels in the aerial.
COURT_A = (19.86, 44.64, 0.00, 9.90)
COURT_B = (70.95, 96.73, 0.00, 10.15)
Z_COURT_GLASS = 17.50

# The central courtroom lantern, on the middle wing between the two courts.
LANTERN = (49.5, 66.0, 1.40, 9.00)
Z_LANTERN = 26.60
LAYLIGHTS = ((52.4, 57.4), (58.4, 63.4))  # E spans of the twin laylights

# Mansard band along McAllister: high at its north edge, low at the parapet.
MANSARD_S0 = 18.70
MANSARD_S1 = S_LEN - INSET_DECK
Z_MANSARD_HI = 26.60

ARCADE = 19        # south (McAllister) arched bays
ARC_E0, ARC_E1 = 4.60, 110.90
END_BAYS = 3       # east and west short ends
ENTRY_BAYS = (7, 8, 9)  # arcade bays the three portals sit under

BEVEL_W = 0.12
BEVEL_SEG = 2

PALETTE_HEX = {
    "Toy_cream": "f2ede3",
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_teal": "3fa8a0",
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


def arch_profile(c, half_w, z0, z_spring, z_top, segs=7):
    """2D outline (u, z) of an arch-headed opening centred on u = c."""
    pts = [(c - half_w, z0), (c + half_w, z0), (c + half_w, z_spring)]
    for i in range(1, segs):
        a = math.pi * i / segs
        pts.append((c + half_w * math.cos(a), z_spring + (z_top - z_spring) * math.sin(a)))
    pts.append((c - half_w, z_spring))
    return pts


def arch_panel_ew(name, e_c, half_w, s_face, out, z0, z_spring, z_top, matname, segs=7):
    """Arch-headed panel on a north/south facade (opening runs along E)."""
    pts = arch_profile(e_c, half_w, z0, z_spring, z_top, segs)
    verts = []
    n = len(pts)
    for depth in (0.0, out):
        for e, z in pts:
            x, y = grid_to_local(e, s_face + depth)
            verts.append((x, y, z))
    faces = [list(range(n - 1, -1, -1)), list(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, j, j + n, i + n])
    return new_mesh(name, verts, faces, matname, 0.0)


def arch_panel_ns(name, s_c, half_w, e_face, out, z0, z_spring, z_top, matname, segs=7):
    """Arch-headed panel on an east/west facade (opening runs along S)."""
    pts = arch_profile(s_c, half_w, z0, z_spring, z_top, segs)
    verts = []
    n = len(pts)
    for depth in (0.0, out):
        for s, z in pts:
            x, y = grid_to_local(e_face + depth, s)
            verts.append((x, y, z))
    faces = [list(range(n - 1, -1, -1)), list(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, j, j + n, i + n])
    return new_mesh(name, verts, faces, matname, 0.0)


def cylinder_dir(name, p0, p1, r, matname, segs=10):
    """A capped cylinder between two local 3D points - used for the flagpoles."""
    a = Vector(p0)
    b = Vector(p1)
    axis = (b - a).normalized()
    up = Vector((0.0, 0.0, 1.0))
    if abs(axis.dot(up)) > 0.95:
        up = Vector((1.0, 0.0, 0.0))
    u = axis.cross(up).normalized()
    v = axis.cross(u).normalized()
    verts = []
    for p in (a, b):
        for i in range(segs):
            t = 2 * math.pi * i / segs
            q = p + u * (r * math.cos(t)) + v * (r * math.sin(t))
            verts.append((q.x, q.y, q.z))
    faces = [list(range(segs - 1, -1, -1)), list(range(segs, 2 * segs))]
    for i in range(segs):
        j = (i + 1) % segs
        faces.append([i, j, j + segs, i + segs])
    return new_mesh(name, verts, faces, matname, 0.0)


def polygon_area(poly):
    a = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        a += x0 * y1 - x1 * y0
    return a * 0.5


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


def outline_ring(name, d_out, d_in, z0, z1, matname, bevel_w=BEVEL_W):
    """A closed rectilinear ring - the cornice, the attic and the parapet cap."""
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


# ------------------------------------------------------------------- massing


def build_envelope():
    """One continuous Beaux-Arts envelope, never interrupted along its length."""
    outline_prism("plinth", PROUD_PLINTH, 0.0, Z_PLINTH, "Toy_stone")
    outline_prism("base", 0.0, Z_PLINTH, Z_BASE, "Toy_stone")
    for k, z in enumerate((2.10, 3.65, 5.20)):
        outline_prism(f"rustic{k}", 0.16, z, z + 0.26, "Toy_stone", bevel_w=0.05)
    outline_prism("stringcourse", PROUD_STR, Z_BASE, Z_STR, "Toy_trim")
    outline_prism("second", 0.0, Z_STR, Z_SEC, "Toy_cream")
    outline_prism("sillband", PROUD_SILL, Z_SEC, Z_SILL, "Toy_trim")
    outline_prism("body", 0.0, Z_SILL, Z_BODY, "Toy_cream")
    # Cornice, attic and parapet are RINGS: the roof they enclose is the
    # asset's largest surface and must not be buried under a solid slab.
    outline_ring("entablature", PROUD_CORN, -1.60, Z_BODY, Z_CORN, "Toy_trim")
    outline_ring("attic", -INSET_ATTIC, -2.10, Z_CORN, Z_ATTIC, "Toy_cream")
    outline_ring("parapet", -INSET_PARAPET, -2.55, Z_ATTIC, Z_CREST, "Toy_trim")


def deck_slabs():
    """The roof plane, one slab per plan region, inset from the walls.

    The regions are disjoint in E, so the slabs cannot overlap. An earlier
    version overlapped the south bar at both recessed corners, and the
    resulting coplanar top faces z-fought into black patches.
    """
    d = INSET_DECK
    s_south = S_LEN - d
    return [
        (0.00 + d, 5.07, 14.71 + d, s_south),
        (5.07, 19.86, 0.70 + d, s_south),
        (19.86, 44.64, 9.90 + d, s_south),
        (44.64, 70.95, 0.40 + d, s_south),
        (70.95, 96.73, 10.15 + d, s_south),
        (96.73, 110.60, 0.05 + d, s_south),
        (110.60, E_LEN - d, 14.85 + d, s_south),
    ]


def build_roof():
    for i, (e0, e1, s0, s1) in enumerate(deck_slabs()):
        box(f"deck{i}", e0, e1, s0, s1, Z_BODY, Z_DECK, "Toy_steel")

    # Mansard band along McAllister: a slab that is high at its inner (north)
    # edge and falls to the parapet, so the aerial reads a broad dark slope.
    a = grid_to_local(INSET_DECK, MANSARD_S0)
    b = grid_to_local(E_LEN - INSET_DECK, MANSARD_S1)
    x0, x1 = min(a[0], b[0]), max(a[0], b[0])
    y_hi, y_lo = a[1], b[1]  # y_hi = north edge (higher), y_lo = south edge
    verts = [
        (x0, y_lo, Z_DECK - 0.25), (x1, y_lo, Z_DECK - 0.25),
        (x1, y_hi, Z_DECK - 0.25), (x0, y_hi, Z_DECK - 0.25),
        (x0, y_lo, Z_DECK + 0.10), (x1, y_lo, Z_DECK + 0.10),
        (x1, y_hi, Z_MANSARD_HI), (x0, y_hi, Z_MANSARD_HI),
    ]
    faces = [
        [3, 2, 1, 0], [4, 5, 6, 7],
        [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7],
    ]
    new_mesh("mansard", verts, faces, "Toy_roofd", BEVEL_W)
    for i in range(6):
        e_c = 11.0 + i * 18.8
        box(f"dormer{i}", e_c - 1.9, e_c + 1.9, MANSARD_S1 - 4.6, MANSARD_S1 - 2.2,
            Z_DECK + 0.2, Z_DECK + 1.9, "Toy_trim", bevel_w=0.07)

    # The two light courts, glazed over: the only saturated colour on the asset
    # and what makes the building findable from the app's altitude.
    for tag, (e0, e1, s0, s1) in (("a", COURT_A), ("b", COURT_B)):
        box(f"court_{tag}_glass", e0 + 0.9, e1 - 0.9, s0, s1 - 0.9,
            Z_COURT_GLASS, Z_COURT_GLASS + 0.35, "Toy_teal")
        box(f"court_{tag}_curb", e0, e1, s1 - 1.5, s1 - 0.5,
            Z_COURT_GLASS, Z_COURT_GLASS + 0.9, "Toy_trim", bevel_w=0.07)

    # The central courtroom lantern with its twin ornamental laylights.
    le0, le1, ls0, ls1 = LANTERN
    box("lantern", le0, le1, ls0, ls1, Z_DECK - 0.4, Z_LANTERN, "Toy_cream", bevel_w=BEVEL_W)
    box("lantern_cornice", le0 - 0.5, le1 + 0.5, ls0 - 0.5, ls1 + 0.5,
        Z_LANTERN - 0.75, Z_LANTERN - 0.18, "Toy_trim", bevel_w=0.08)
    for i, (a0, a1) in enumerate(LAYLIGHTS):
        box(f"laylight_curb{i}", a0 - 0.45, a1 + 0.45, ls0 + 0.85, ls1 - 0.85,
            Z_LANTERN - 0.3, Z_LANTERN + 0.22, "Toy_trim", bevel_w=0.08)
        box(f"laylight{i}", a0, a1, ls0 + 1.3, ls1 - 1.3, Z_LANTERN + 0.14,
            Z_CREST, "Toy_white_Glow", bevel_w=0.09)

    # Plant and stair penthouses on the wings (style bible s.10 - the camera
    # looks down on this and a blank deck reads as unfinished).
    for i, (e, s, w, d, h) in enumerate(
        [(8.0, 3.6, 7.0, 4.4, 2.4), (13.0, 9.2, 4.4, 3.2, 1.6),
         (50.0, 10.4, 5.0, 3.4, 1.7), (63.0, 10.4, 5.0, 3.4, 1.7),
         (99.0, 3.0, 8.0, 4.4, 2.4), (104.5, 9.0, 4.4, 3.2, 1.6)]
    ):
        box(f"mech{i}", e, e + w, s, s + d, Z_DECK - 0.25, Z_DECK + h, "Toy_roofd", bevel_w=0.08)


def build_south_front():
    """McAllister Street: the hero elevation. The arcade is never interrupted."""
    pitch = (ARC_E1 - ARC_E0) / ARCADE
    s_face = S_LEN

    # The giant arcade: 19 arch-headed glass recesses between flat pilasters.
    for i in range(ARCADE):
        e_c = ARC_E0 + pitch * (i + 0.5)
        arch_panel_ew(f"s_arch{i}", e_c, 2.00, s_face + 0.08, -0.85,
                      11.60, 16.75, 18.75, "Toy_glass")
        # a keystone, so the arcade reads as masonry rather than as slots
        box(f"s_key{i}", e_c - 0.42, e_c + 0.42, s_face - 0.05, s_face + 0.30,
            18.70, 19.45, "Toy_trim", bevel_w=0.05)
    for i in range(ARCADE + 1):
        e_c = ARC_E0 + pitch * i
        box(f"s_pier{i}", e_c - 0.70, e_c + 0.70, s_face, s_face + 0.32,
            Z_SILL, Z_BODY, "Toy_cream", bevel_w=0.06)
    # A continuous impost course at the springing ties 19 bays into one arcade.
    box("s_impost", ARC_E0 - 2.2, ARC_E1 + 2.2, s_face, s_face + 0.52,
        16.50, 17.05, "Toy_trim", bevel_w=0.07)
    # Small square spandrel windows over each pier.
    for i in range(1, ARCADE):
        e_c = ARC_E0 + pitch * i
        box(f"s_spandrel{i}", e_c - 0.55, e_c + 0.55, s_face - 0.08, s_face + 0.22,
            17.60, 18.70, "Toy_glass")
    # Second-storey and base windows.
    for i in range(ARCADE):
        e_c = ARC_E0 + pitch * (i + 0.5)
        box(f"s_secwin{i}", e_c - 1.55, e_c + 1.55, s_face - 0.10, s_face + 0.40,
            8.40, 10.00, "Toy_glass")
        if i in ENTRY_BAYS:
            continue
        box(f"s_basewin{i}", e_c - 1.20, e_c + 1.20, s_face - 0.10, s_face + 0.40,
            3.10, 6.10, "Toy_glass")

    # The three carved entrance portals, semantically enlarged and breaking up
    # through the string course exactly as they do on the real facade.
    for k, i in enumerate(ENTRY_BAYS):
        e_c = ARC_E0 + pitch * (i + 0.5)
        arch_panel_ew(f"s_portal_frame{k}", e_c, 3.00, s_face + 0.50, -0.50,
                      0.60, 6.60, 10.85, "Toy_trim")
        arch_panel_ew(f"s_portal_reveal{k}", e_c, 2.55, s_face + 0.64, -0.14,
                      0.85, 6.95, 10.20, "Toy_glass")
        arch_panel_ew(f"s_portal{k}", e_c, 2.15, s_face + 0.72, -0.08,
                      0.90, 7.10, 9.90, "Toy_gold_Glow")
        for sgn in (-1, 1):
            box(f"s_lamp{k}{sgn}", e_c + sgn * 3.55 - 0.30, e_c + sgn * 3.55 + 0.30,
                s_face + 0.10, s_face + 0.85, 5.20, 6.40, "Toy_gold_Glow", bevel_w=0.06)

    # One chunky three-tread step block in front of the entrance group.
    e_mid = ARC_E0 + pitch * (ENTRY_BAYS[1] + 0.5)
    for i in range(3):
        half = 13.5 - i * 1.1
        box(f"s_step{i}", e_mid - half, e_mid + half,
            s_face, s_face + 3.4 - i * 1.05, 0.0, 0.30 + i * 0.30,
            "Toy_stone", bevel_w=0.10)



def build_ends():
    """Polk (west) and Larkin (east): the short 16.7 m returns."""
    for tag, e_face, out in (("w", 0.0, 1.0), ("e", E_LEN, -1.0)):
        s0, s1 = (14.71, S_LEN) if tag == "w" else (14.85, S_LEN)
        pitch = (s1 - s0 - 2.6) / END_BAYS
        for i in range(END_BAYS):
            s_c = s0 + 1.3 + pitch * (i + 0.5)
            arch_panel_ns(f"{tag}_arch{i}", s_c, 2.00, e_face - out * 0.08, out * 0.85,
                          11.60, 16.75, 18.75, "Toy_glass")
            box(f"{tag}_secwin{i}", min(e_face, e_face - out * 0.40),
                max(e_face, e_face - out * 0.40), s_c - 1.55, s_c + 1.55,
                8.40, 10.00, "Toy_glass")
            box(f"{tag}_basewin{i}", min(e_face, e_face - out * 0.40),
                max(e_face, e_face - out * 0.40), s_c - 1.20, s_c + 1.20,
                3.10, 6.10, "Toy_glass")
        box(f"{tag}_impost", min(e_face, e_face - out * 0.52),
            max(e_face, e_face - out * 0.52), s0 + 0.6, s1 - 0.6,
            16.50, 17.05, "Toy_trim", bevel_w=0.07)


def build_north():
    """Golden Gate side: plain rectangular rhythms, no arches, plus the courts."""
    # (e0, e1, s_face, outward sign) for every north-facing wall segment
    segs = [
        (5.07, 19.86, 0.70, -1.0),
        (44.64, 70.95, 0.40, -1.0),
        (96.73, 110.60, 0.05, -1.0),
        (0.00, 5.07, 14.71, -1.0),
        (110.60, 115.48, 14.85, -1.0),
        (19.86, 44.64, 9.90, -1.0),   # court A back wall
        (70.95, 96.73, 10.15, -1.0),  # court B back wall
    ]
    for k, (e0, e1, s_face, out) in enumerate(segs):
        span = e1 - e0
        n = max(1, int(round(span / 5.6)))
        pitch = span / n
        for i in range(n):
            e_c = e0 + pitch * (i + 0.5)
            box(f"n{k}_win{i}", e_c - 1.60, e_c + 1.60, s_face - 0.42, s_face + 0.10,
                11.90, 18.60, "Toy_glass")
            box(f"n{k}_secwin{i}", e_c - 1.35, e_c + 1.35, s_face - 0.42, s_face + 0.10,
                8.40, 10.00, "Toy_glass")
            box(f"n{k}_basewin{i}", e_c - 1.10, e_c + 1.10, s_face - 0.42, s_face + 0.10,
                3.10, 6.10, "Toy_glass")

    # The court flanks (walls facing into each light court along E).
    for (e0, e1, _s0, s1) in (COURT_A, COURT_B):
        for e_face, out in ((e0, -1.0), (e1, 1.0)):
            for i in range(2):
                s_c = 3.2 + i * 4.0
                box(f"court_win_{int(e_face)}_{i}",
                    min(e_face, e_face + out * 0.40), max(e_face, e_face + out * 0.40),
                    s_c - 1.30, s_c + 1.30, 11.90, 16.60, "Toy_glass")


def build_attic_windows():
    """Small square attic lights, at the arcade pitch, all the way round."""
    pitch = (ARC_E1 - ARC_E0) / ARCADE
    for i in range(ARCADE):
        e_c = ARC_E0 + pitch * (i + 0.5)
        box(f"a_swin{i}", e_c - 0.95, e_c + 0.95,
            S_LEN - INSET_ATTIC - 0.10, S_LEN - INSET_ATTIC + 0.35,
            23.20, 24.60, "Toy_glass")
    for k, (e0, e1, s_face) in enumerate(
        [(5.07, 19.86, 0.70), (44.64, 70.95, 0.40), (96.73, 110.60, 0.05)]
    ):
        span = e1 - e0
        n = max(1, int(round(span / 5.6)))
        p = span / n
        for i in range(n):
            e_c = e0 + p * (i + 0.5)
            box(f"a_nwin{k}_{i}", e_c - 0.95, e_c + 0.95,
                s_face + INSET_ATTIC - 0.35, s_face + INSET_ATTIC + 0.10,
                23.20, 24.60, "Toy_glass")


# --------------------------------------------------------------- assembly


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    OBJECTS.clear()
    build_envelope()
    build_roof()
    build_south_front()
    build_ends()
    build_north()
    build_attic_windows()

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

    blend = os.path.join(out, "earl-warren-building.blend")
    glb = os.path.join(out, "earl-warren-building.glb")
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
