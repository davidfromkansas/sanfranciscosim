"""Deterministic Blender build of the SF-SIM miniature Palace of Fine Arts.

    blender -b --python build_palace_of_fine_arts.py -- [--out DIR]

Writes palace-of-fine-arts.blend and palace-of-fine-arts.glb next to this file
(or into --out). Geometry is authored in world space in metres, Z up, +X east,
+Y true north, origin at the rotunda centroid (= the manifest anchor), min Z 0,
so the export needs no transforms applied after the fact.

Design (see REFERENCE.md for the sources behind every number):

* an open octagonal rotunda on eight piers whose measured azimuths are
  30 deg + 45k CCW from east, so one arch axis points at the lagoon in the
  east; paired freestanding Corinthian columns on tall pedestals flank each
  pier;
* a tall attic ring above the arches carrying the relief-panel band (the
  night-lit frieze -> the panels are the rotunda's _Glow surfaces), urn
  finials at the corners, and the muted red-orange dome to the published
  49.4 m apex - smooth cap, no finial, small glowing crown ring;
* two curved colonnade arms whose centerlines are traced point-for-point
  from the surveyed OSM roof outlines - the arms are NOT mirror images: both
  end in L-hooks that turn east then away, with detached terminal gate boxes
  at the surveyed positions;
* double rows of columns under a continuous entablature, punctuated by
  4-column clusters carrying vine boxes with blocky weeping-maiden
  silhouettes at the corners, looking inward;
* a low stone terrace that grounds the whole crescent;
* BY OWNER DIRECTIVE (2026-08-10, superseding the original task scope): the
  surrounding grounds are included - the lagoon water traced from the surveyed
  OSM multipolygon (relation 7471537, outer ring + the large island; the 3 m
  islet is dropped as sub-toy-scale), a stone shore rim, a manicured lawn
  plate, grouped toy trees (conical and round species), shrub masses behind
  the colonnade, and three swans on the water as the storytelling props;
* the NIGHT STATE mirrors the real warm-gold floodlighting: Toy_gold_Glow on
  the attic frieze panels, the cornice ring at the dome springing, the main
  entablature underside, the uplit floor pool inside the open rotunda, the
  colonnade underside bands and the gate undersides; Toy_white_Glow only on
  the apex crown ring. Emission ships at 0 - the app's night pass raises it;
  render_palace_of_fine_arts.py --night previews the look.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector, geometry

# ---------------------------------------------------------------- parameters

H_APEX = 49.4  # published architectural height, dome apex (Wikidata P2048)

# terrace
TER_H = 1.25  # rotunda terrace height
TER_R = 39.0  # rotunda terrace radius
ARM_TER_H = 1.1  # arm terrace strip height (lower: avoids coplanar z-fight)
ARM_TER_W = 9.5  # arm terrace strip width

# rotunda ring
A_PIER = 30.0  # measured pier azimuth offset, degrees CCW from +X (east)
R_PIER = 24.0  # pier center radius
PIER_W = 6.0  # pier width (tangential)
PIER_D = 4.2  # pier depth (radial)
H_PIER = 26.5  # pier / arch-wall top
R_WALL = 24.6  # arch spandrel wall apothem (perpendicular distance)
WALL_T = 1.4  # arch wall thickness
ARCH_HW = 5.4  # arch opening half-width
ARCH_SPRING = 14.5  # arch springing height
H_ENT0, H_ENT1 = 26.5, 29.6  # main entablature ring
R_COL = 29.6  # paired-column radius (center of shafts)
COL_TAN = 4.3  # tangential offset of each column of a pair
COL_R = 1.05  # rotunda column shaft radius
PED = 2.7  # pedestal width
H_PED = 5.0  # pedestal top
H_CAP0 = 23.4  # capital bottom (shaft top)
ATTIC_R_OUT = 22.8  # attic ring apothem (outer)
ATTIC_T = 2.6  # attic ring thickness
H_ATT0, H_ATT1 = 29.6, 37.6  # attic band
H_COR1 = 38.9  # attic cornice top
DOME_R = 21.6  # dome base radius: springs from just inside the attic cornice
DOME_Z0 = 38.2  # dome base height

# colonnade arms
COL2_R = 0.85  # arm column shaft radius
ARM_ROW = 2.2  # half distance between the two column rows
ARM_BAY = 6.55  # column spacing along the arc
H_AB = 1.1  # arm column base bottom (terrace top)
H_APED = 2.5  # arm column base top
H_ASH = 12.7  # arm shaft top
H_AENT0 = 14.1  # arm capital top / entablature bottom
H_AENT1 = 17.3  # entablature top
H_ACOR1 = 17.9  # cornice top
ENT_W = 5.5  # entablature band width (OSM roof band)
BOX_EVERY = 3  # a maiden box every N bays
BOX_L, BOX_W, BOX_H = 7.6, 7.0, 3.5  # boxes atop the entablature

# Surveyed arm centerlines, traced from OSM ways 288371310 (north) and
# 288371306 (south), decimated to ~8 m steps, local metres (+X east +Y north).
# Order: from the L-hook far end toward the rotunda shoulder.
ARM_N = [
    (17.5, 110.5), (12.0, 106.5), (14.4, 98.7), (16.8, 91.3), (16.4, 83.6),
    (12.5, 79.8), (4.7, 79.8), (-2.6, 79.0), (-9.1, 73.8), (-14.5, 68.0),
    (-19.1, 62.7), (-23.3, 55.6), (-25.8, 47.9), (-29.4, 41.8), (-31.9, 33.8),
    (-33.4, 26.1), (-36.0, 20.1),
]
ARM_S = [
    (47.8, -104.4), (47.3, -97.5), (44.8, -90.2), (43.2, -81.9), (43.1, -74.3),
    (35.7, -71.9), (31.1, -76.9), (24.2, -74.3), (16.8, -74.1), (9.1, -70.8),
    (3.6, -66.3), (-3.3, -61.7), (-9.2, -55.8), (-14.2, -50.1), (-19.2, -43.3),
    (-23.3, -36.5), (-27.6, -30.5),
]
# Detached terminal gate boxes (OSM ways 288371313 / 288371314).
GATE_N = (-3.1, 105.2)
GATE_S = (30.0, -101.6)
GATE_W = 8.8  # gate footprint
H_GATE_ENT0, H_GATE_ENT1 = 14.1, 17.6
H_GATE_TOP = 21.3  # OSM height 21

# Lagoon rings traced from OSM relation 7471537 (RDP-decimated, local metres).
LAGOON = [
    (43.7, 109.7), (35.7, 130.5), (39.0, 134.4), (59.6, 134.3), (80.3, 120.6),
    (94.0, 95.9), (90.0, 74.7), (103.4, 53.8), (108.3, 12.3), (106.6, 8.0), (97.8, 4.7),
    (96.6, -1.3), (101.4, -12.8), (117.7, -32.8), (111.0, -47.1), (117.1, -62.9),
    (109.9, -71.3), (106.4, -83.1), (95.3, -90.8), (102.6, -98.8), (100.7, -104.0),
    (90.1, -102.7), (78.1, -105.7), (56.6, -90.5), (45.8, -61.8), (39.3, -59.1),
    (17.4, -64.1), (4.1, -56.3), (-6.9, -45.0), (-7.1, -40.1), (0.2, -35.1),
    (20.8, -36.4), (35.2, -30.4), (40.6, -21.0), (47.4, 6.3), (33.0, 29.4), (20.4, 40.7),
    (10.2, 41.7), (-10.9, 32.6), (-18.0, 35.8), (-19.5, 44.6), (-3.9, 67.6),
    (19.7, 70.7), (31.8, 78.0), (24.2, 90.6), (23.5, 102.8), (29.9, 107.0), (34.1, 94.5),
    (39.4, 96.0), (43.2, 99.0),
]
ISLAND = [
    (53.6, 109.9), (58.7, 90.0), (66.7, 71.7), (79.4, 72.9), (82.1, 81.0), (77.9, 90.8),
    (75.6, 105.8), (69.5, 120.5), (56.9, 123.1),
]

WATER_Z0, WATER_Z1 = 0.10, 0.42
LAWN_Z = 0.28
RIM_W, RIM_Z = 1.5, 0.55
LAWN_MARGIN = 9.0

# Grouped toy trees: (kind, x, y, crown-top height). Composed from the aerial
# photograph: dense screen west of both arms, groves at the hooks and gates,
# specimens on the east shore and the island. All well below the 49.4 m apex.
TREES = [
    ("cone", -44, 26, 15), ("round", -42, 40, 11), ("cone", -38, 53, 16),
    ("round", -31, 65, 10), ("round", -22, 76, 12), ("cone", -12, 86, 17),
    ("round", 2, 95, 10), ("cone", 7, 116, 16), ("round", 22, 116, 9),
    ("cone", -37, -34, 16), ("round", -33, -45, 11), ("cone", -26, -57, 15),
    ("round", -17, -66, 10), ("round", -6, -76, 12),
    ("cone", 14, -84, 17), ("round", 28, -88, 10), ("cone", 38, -112, 15),
    ("round", 52, -108, 10),
    ("round", 108, 62, 10), ("round", 112, 20, 11), ("round", 121, -48, 10),
    ("round", 68, 96, 9), ("round", 63, 112, 8), ("cone", 74, 82, 11),
    ("cone", -41, 5, 14), ("round", -36, -12, 10),
]
# Shrub masses: (x, y, length, width, yaw degrees)
SHRUBS = [
    (-39, 33, 8, 2.6, 60), (-28, 61, 7, 2.4, 40), (-15, 80, 6, 2.2, 25),
    (-31, -40, 8, 2.6, -55), (-20, -60, 7, 2.4, -40), (-1, -71, 6, 2.2, -15),
    (-30, -5, 7, 2.4, 90), (72, 108, 6, 2.4, -20),
]
SWANS = [(58, 10, -35), (63, 6, 20), (56, 2, 70)]  # x, y, heading degrees

# Project palette from .agents/skills/sf-asset-check (hex, sRGB). Toy_pine and
# Toy_leaf are off-palette vegetation greens (contract WARN, style bible s.12:
# vegetation may be vivid); everything else is the standard palette.
PALETTE_HEX = {
    "Toy_sand": "ece4d4",
    "Toy_trim": "f3efe6",
    "Toy_stone": "d9d2c2",
    "Toy_ioorange": "c0402a",
    "Toy_white_Glow": "f7f4ec",
    "Toy_gold_Glow": "caa64a",
    "Toy_glass": "2a4d73",
    "Toy_mint": "8fd0a8",
    "Toy_white": "f7f4ec",
    "Toy_ink": "3a3530",
    "Toy_pine": "3f6b4f",
    "Toy_leaf": "6fa361",
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
        # Flagged for the app's night pass; emission off in the daylight asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# -------------------------------------------------------------- mesh helpers


def new_mesh(name, verts, faces, mats, face_mats=None):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    for m in mats:
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


def bevel(obj, width=0.12, segments=2):
    """Miniature-style edge softening on the chunky solids (style bible s.4)."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(
        bm,
        geom=list(bm.verts) + list(bm.edges),
        offset=width,
        segments=segments,
        profile=0.5,
        affect="EDGES",
        clamp_overlap=True,
    )
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def rot2(p, ang):
    c, s = math.cos(ang), math.sin(ang)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0):
    hx, hy = sx / 2, sy / 2
    corners = [rot2(c, yaw) for c in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy))]
    verts = [(cx + x, cy + y, z0) for x, y in corners]
    verts += [(cx + x, cy + y, z1) for x, y in corners]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


def frustum(name, cx, cy, z0, z1, s0, s1, mat, yaw=0.0):
    """Tapered box: square s0 at z0 to square s1 at z1 (maiden silhouettes)."""
    verts = []
    for z, s in ((z0, s0), (z1, s1)):
        h = s / 2
        for c in ((-h, -h), (h, -h), (h, h), (-h, h)):
            x, y = rot2(c, yaw)
            verts.append((cx + x, cy + y, z))
    faces = [(3, 2, 1, 0), (4, 5, 6, 7)]
    for i in range(4):
        j = (i + 1) % 4
        faces.append((i, j, 4 + j, 4 + i))
    return new_mesh(name, verts, faces, [mat])


def cylinder(name, cx, cy, z0, z1, radius, mat, seg=10, r1=None, caps=True):
    r1 = radius if r1 is None else r1
    verts = []
    for z, r in ((z0, radius), (z1, r1)):
        for i in range(seg):
            a = 2 * math.pi * i / seg
            verts.append((cx + r * math.cos(a), cy + r * math.sin(a), z))
    faces = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]
    if caps:
        faces.append(tuple(range(seg - 1, -1, -1)))
        faces.append(tuple(range(seg, 2 * seg)))
    return new_mesh(name, verts, faces, [mat])


def ngon_ring(name, n, apothem_out, thickness, z0, z1, mat, phase=0.0):
    """Closed prismatic ring of n flat faces (attic / entablature rings)."""
    r_out = apothem_out / math.cos(math.pi / n)
    r_in = (apothem_out - thickness) / math.cos(math.pi / n)
    pts_out = []
    pts_in = []
    for i in range(n):
        a = phase + 2 * math.pi * (i + 0.5) / n
        pts_out.append((r_out * math.cos(a), r_out * math.sin(a)))
        pts_in.append((r_in * math.cos(a), r_in * math.sin(a)))
    verts = []
    for loop, z in ((pts_out, z0), (pts_out, z1), (pts_in, z0), (pts_in, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))  # outer wall
        faces.append((3 * n + j, 3 * n + i, 2 * n + i, 2 * n + j))  # inner wall
        faces.append((n + i, n + j, 3 * n + j, 3 * n + i))  # top
        faces.append((2 * n + j, 2 * n + i, i, j))  # bottom
    return new_mesh(name, verts, faces, [mat])


def dome_cap(name, base_r, z0, z1, mat, seg=20, rings=9):
    """Spherical cap, flat-shaded segments read as toy panelling."""
    h = z1 - z0
    R = (base_r * base_r + h * h) / (2 * h)
    zc = z1 - R
    phi0 = math.asin((z0 - zc) / R)  # polar angle at the base ring
    verts = []
    ring_rows = []
    for k in range(rings):
        phi = phi0 + (math.pi / 2 - phi0) * k / rings  # equal-angle rows
        z = zc + R * math.sin(phi)
        r = R * math.cos(phi)
        row = []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            row.append(len(verts))
            verts.append((r * math.cos(a), r * math.sin(a), z))
        ring_rows.append(row)
    apex = len(verts)
    verts.append((0.0, 0.0, z1))
    faces = []
    for k in range(rings - 1):
        a, b = ring_rows[k], ring_rows[k + 1]
        for i in range(seg):
            j = (i + 1) % seg
            faces.append((a[i], a[j], b[j], b[i]))
    top = ring_rows[-1]
    for i in range(seg):
        j = (i + 1) % seg
        faces.append((top[i], top[j], apex))
    return new_mesh(name, verts, faces, [mat])


def arch_wall(name, face_az, mat):
    """One octagon face: spandrel wall with a full arched opening.

    Built in local (u = tangential, z = up) coordinates, extruded radially,
    then placed at apothem R_WALL along azimuth face_az.
    """
    half_gap = R_PIER * math.sin(math.radians(22.5))  # to adjacent pier centers
    u0 = half_gap + PIER_W * 0.45  # tuck the wall ends into the piers
    arc = []
    n_arc = 8
    for i in range(n_arc + 1):
        a = math.pi * i / n_arc  # 180..0 across the opening
        arc.append((ARCH_HW * math.cos(math.pi - a), ARCH_SPRING + ARCH_HW * math.sin(math.pi - a)))
    # closed profile with the door-shaped notch (CCW)
    profile = [(-u0, TER_H), (-u0, H_PIER), (u0, H_PIER), (u0, TER_H), (ARCH_HW, TER_H), (ARCH_HW, ARCH_SPRING)]
    profile += [(u, z) for u, z in reversed(arc[1:-1])]
    profile += [(-ARCH_HW, ARCH_SPRING), (-ARCH_HW, TER_H)]
    tris = geometry.tessellate_polygon([[Vector((u, z, 0)) for u, z in profile]])
    m = len(profile)
    verts = []
    ca, sa = math.cos(face_az), math.sin(face_az)
    for w in (R_WALL - WALL_T, R_WALL):
        for u, z in profile:
            x = ca * w - sa * u
            y = sa * w + ca * u
            verts.append((x, y, z))
    faces = []
    for t in tris:
        faces.append(tuple(reversed(t)))  # inner skin
        faces.append(tuple(m + i for i in t))  # outer skin
    for i in range(m):
        j = (i + 1) % m
        faces.append((i, j, m + j, m + i))  # boundary (arch reveal, edges)
    return new_mesh(name, verts, faces, [mat])


# ---------------------------------------------------------------- path tools


def resample(path, step):
    """Even arc-length resample; returns points and unit tangents."""
    L = [0.0]
    for a, b in zip(path, path[1:]):
        L.append(L[-1] + math.dist(a, b))
    total = L[-1]
    n = max(2, round(total / step))
    pts = []
    k = 0
    for m in range(n + 1):
        t = total * m / n
        while k < len(L) - 2 and L[k + 1] < t:
            k += 1
        f = (t - L[k]) / (L[k + 1] - L[k]) if L[k + 1] > L[k] else 0.0
        pts.append(
            (
                path[k][0] + (path[k + 1][0] - path[k][0]) * f,
                path[k][1] + (path[k + 1][1] - path[k][1]) * f,
            )
        )
    tans = []
    for i, p in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        d = (b[0] - a[0], b[1] - a[1])
        m2 = math.hypot(*d) or 1.0
        tans.append((d[0] / m2, d[1] / m2))
    return pts, tans


def path_band(name, path, z0, z1, width, mat, step=5.5, closed=False):
    """Rectangular band lofted along a 2D path (entablature, terrace strips).

    closed=True lofts around a ring (shore rims) - the seam is a doubled
    point, so no end caps are emitted.
    """
    if closed:
        path = list(path) + [path[0]]
    pts, tans = resample(path, step)
    h = width / 2
    left = []
    right = []
    for (x, y), (tx, ty) in zip(pts, tans):
        nx, ny = -ty, tx
        left.append((x + nx * h, y + ny * h))
        right.append((x - nx * h, y - ny * h))
    n = len(pts)
    verts = []
    for z in (z0, z1):
        verts += [(x, y, z) for x, y in left]
        verts += [(x, y, z) for x, y in right]
    faces = []
    L0, R0, L1, R1 = 0, n, 2 * n, 3 * n
    for i in range(n - 1):
        faces.append((L1 + i, L1 + i + 1, R1 + i + 1, R1 + i))  # top
        faces.append((R0 + i, R0 + i + 1, L0 + i + 1, L0 + i))  # bottom
        faces.append((L0 + i, L0 + i + 1, L1 + i + 1, L1 + i))  # left wall
        faces.append((R1 + i, R1 + i + 1, R0 + i + 1, R0 + i))  # right wall
    if not closed:
        faces.append((L0, R0, R1, L1))  # start cap
        faces.append((R0 + n - 1, L0 + n - 1, L1 + n - 1, R1 + n - 1))  # end cap
    return new_mesh(name, verts, faces, [mat])


def prism(name, rings, z0, z1, mat):
    """Extruded polygon with optional holes: rings = [outer, hole, ...]."""
    tris = geometry.tessellate_polygon([[Vector((x, y, 0)) for x, y in r] for r in rings])
    flat = [p for r in rings for p in r]
    m = len(flat)
    verts = [(x, y, z0) for x, y in flat] + [(x, y, z1) for x, y in flat]
    faces = []
    for t in tris:
        faces.append(tuple(reversed(t)))  # bottom
        faces.append(tuple(m + i for i in t))  # top
    off = 0
    for r in rings:
        n = len(r)
        for i in range(n):
            j = (i + 1) % n
            faces.append((off + i, off + j, m + off + j, m + off + i))
        off += n
    return new_mesh(name, verts, faces, [mat])


def convex_hull(points):
    pts = sorted(set(points))
    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and (
                (out[-1][0] - out[-2][0]) * (p[1] - out[-2][1])
                - (out[-1][1] - out[-2][1]) * (p[0] - out[-2][0])
            ) <= 0:
                out.pop()
            out.append(p)
        return out
    lower = half(pts)
    upper = half(reversed(pts))
    return lower[:-1] + upper[:-1]


# --------------------------------------------------------------------- build


def tree(name, kind, cx, cy, top, mats):
    ink, pine, leaf = mats
    trunk_top = top * 0.28
    cylinder(f"{name}_t", cx, cy, LAWN_Z, trunk_top, 0.4, ink, seg=6)
    if kind == "cone":
        r = top * 0.20
        cylinder(f"{name}_c0", cx, cy, trunk_top, top * 0.72, r, pine, seg=8, r1=r * 0.55)
        cylinder(f"{name}_c1", cx, cy, top * 0.72, top, r * 0.62, pine, seg=8, r1=0.12)
    else:
        r = top * 0.30
        z0, z1 = trunk_top, top
        mid = (z0 + z1) / 2
        cylinder(f"{name}_c0", cx, cy, z0, mid, r * 0.72, leaf, seg=8, r1=r)
        cylinder(f"{name}_c1", cx, cy, mid, z1, r, leaf, seg=8, r1=r * 0.45)


def swan(name, cx, cy, heading, mats):
    white, mustard = mats
    yaw = math.radians(heading)
    bevel(box(f"{name}_body", cx, cy, WATER_Z1, WATER_Z1 + 0.75, 1.7, 0.95, white, yaw), 0.3, 2)
    nx, ny = rot2((0.75, 0.0), yaw)
    box(f"{name}_neck", cx + nx, cy + ny, WATER_Z1 + 0.55, WATER_Z1 + 1.55, 0.24, 0.24, white, yaw)
    box(f"{name}_head", cx + nx, cy + ny, WATER_Z1 + 1.55, WATER_Z1 + 1.85, 0.42, 0.3, white, yaw)


def build_grounds(mats_main, mats_green):
    sand, trim, stone, orange, glow, gold = mats_main
    glass, mint, white, ink, pine, leaf = mats_green

    # lawn: smooth blob = offset convex hull of the whole composition
    anchor_pts = list(LAGOON) + ARM_N + ARM_S + [GATE_N, GATE_S]
    for k in range(12):
        a = 2 * math.pi * k / 12
        anchor_pts.append((TER_R * math.cos(a), TER_R * math.sin(a)))
    hull = convex_hull(anchor_pts)
    cx = sum(p[0] for p in hull) / len(hull)
    cy = sum(p[1] for p in hull) / len(hull)
    lawn = []
    n = len(hull)
    for i in range(n):  # midpoint-smoothed, margin-offset hull
        for f in (0.0, 0.5):
            j = (i + 1) % n
            px = hull[i][0] + (hull[j][0] - hull[i][0]) * f
            py = hull[i][1] + (hull[j][1] - hull[i][1]) * f
            d = math.hypot(px - cx, py - cy) or 1.0
            s = (d + LAWN_MARGIN) / d
            lawn.append((cx + (px - cx) * s, cy + (py - cy) * s))
    prism("lawn", [lawn], 0.0, LAWN_Z, mint)

    # lagoon: surveyed water polygon with the island as a hole, stone rims
    prism("lagoon", [LAGOON, ISLAND], WATER_Z0, WATER_Z1, glass)
    path_band("shore_rim", LAGOON, 0.0, RIM_Z, RIM_W, stone, step=4.0, closed=True)
    path_band("island_rim", ISLAND, 0.0, RIM_Z, 1.2, stone, step=4.0, closed=True)
    prism("island_mound", [ISLAND], 0.0, 0.6, mint)

    for i, (kind, x, y, top) in enumerate(TREES):
        tree(f"tree{i}", kind, x, y, top, (ink, pine, leaf))
    for i, (x, y, ln, w, deg) in enumerate(SHRUBS):
        bevel(box(f"shrub{i}", x, y, LAWN_Z, LAWN_Z + 1.5, ln, w, leaf, math.radians(deg)), 0.35, 2)
    for i, (x, y, hd) in enumerate(SWANS):
        swan(f"swan{i}", x, y, hd, (white, trim))


def maiden(name, cx, cy, z, yaw, mat):
    """Blocky weeping-maiden silhouette: tapered body + head knob."""
    frustum(name + "_b", cx, cy, z, z + 2.0, 1.15, 0.7, mat, yaw)
    frustum(name + "_h", cx, cy, z + 2.0, z + 2.55, 0.62, 0.4, mat, yaw)


def maiden_box(name, cx, cy, z0, yaw, size_l, size_w, h, mats):
    """Entablature vine box with maidens at the corners, looking in."""
    sand, trim = mats
    bevel(box(name, cx, cy, z0, z0 + h, size_l, size_w, sand, yaw), 0.14)
    box(name + "_lip", cx, cy, z0 + h, z0 + h + 0.35, size_l + 0.5, size_w + 0.5, trim, yaw)
    dl, dw = size_l / 2 - 0.8, size_w / 2 - 0.8
    for sx, sy in ((-dl, -dw), (dl, -dw), (dl, dw), (-dl, dw)):
        ox, oy = rot2((sx, sy), yaw)
        maiden(name + f"_m{sx:.0f}{sy:.0f}", cx + ox, cy + oy, z0 + h + 0.35, yaw, trim)


def build_rotunda(mats):
    sand, trim, stone, orange, glow, gold = mats

    # terrace: chamfered 24-gon plinth
    cylinder("terrace", 0, 0, 0.0, TER_H - 0.35, TER_R, stone, seg=24)
    cylinder("terrace_lip", 0, 0, TER_H - 0.35, TER_H, TER_R - 0.45, stone, seg=24)

    for k in range(8):
        az = math.radians(A_PIER + 45 * k)
        ca, sa = math.cos(az), math.sin(az)
        px, py = R_PIER * ca, R_PIER * sa
        # pier
        bevel(box(f"pier_{k}", px, py, TER_H, H_PIER, PIER_D, PIER_W, sand, yaw=az), 0.15)
        # paired freestanding columns on tall pedestals, flanking the pier
        for s in (-1, 1):
            tx, ty = -sa * s, ca * s  # tangential direction
            cx = R_COL * ca + tx * COL_TAN
            cy = R_COL * sa + ty * COL_TAN
            bevel(box(f"ped_{k}{'ab'[s>0]}", cx, cy, TER_H, H_PED, PED, PED, sand, yaw=az), 0.14)
            cylinder(f"col_{k}{'ab'[s>0]}", cx, cy, H_PED, H_CAP0, COL_R, sand, seg=12)
            box(f"cap1_{k}{'ab'[s>0]}", cx, cy, H_CAP0, H_CAP0 + 0.7, 2.3, 2.3, trim, yaw=az)
            box(f"cap2_{k}{'ab'[s>0]}", cx, cy, H_CAP0 + 0.7, H_ENT0, 2.8, 2.8, trim, yaw=az)
        # projecting entablature block tying the pair back to the ring
        bevel(
            box(f"entblk_{k}", (R_COL - 1.2) * ca, (R_COL - 1.2) * sa, H_ENT0, H_ENT1, 4.6, 2 * COL_TAN + 3.0, sand, yaw=az),
            0.14,
        )
        # arch spandrel wall on the face between this pier and the next
        arch_wall(f"arch_{k}", az + math.radians(22.5), sand)

    # main entablature ring and attic
    ngon_ring("entab_ring", 8, R_WALL + 0.9, 2.6, H_ENT0, H_ENT1, trim, phase=math.radians(A_PIER))
    ngon_ring("attic", 8, ATTIC_R_OUT, ATTIC_T, H_ATT0, H_ATT1, sand, phase=math.radians(A_PIER))
    ngon_ring("attic_cornice", 8, ATTIC_R_OUT + 0.8, 1.6, H_ATT1, H_COR1, trim, phase=math.radians(A_PIER))

    # relief panels: the lit frieze band (warm gold floodlight at night)
    for k in range(8):
        az = math.radians(A_PIER + 45 * k + 22.5)
        w = ATTIC_R_OUT - 0.18
        px, py = w * math.cos(az), w * math.sin(az)
        box(f"panel_{k}", px, py, H_ATT0 + 1.5, H_ATT1 - 1.2, 0.8, 11.0, gold, yaw=az)

    # night-glow fixtures: entablature underside ring, uplit interior floor
    ngon_ring("entab_uplight", 8, R_WALL + 1.0, 1.2, H_ENT0 - 0.5, H_ENT0, gold, phase=math.radians(A_PIER))
    cylinder("floor_uplight", 0, 0, TER_H + 0.05, TER_H + 0.14, 16.5, gold, seg=16)

    # urn finials on the attic corners
    for k in range(8):
        az = math.radians(A_PIER + 45 * k)
        r = (ATTIC_R_OUT + 0.4) / math.cos(math.pi / 8)
        ux, uy = r * math.cos(az), r * math.sin(az)
        cylinder(f"urn_{k}", ux, uy, H_COR1, H_COR1 + 1.5, 0.75, trim, seg=8, r1=0.35)

    # dome: smooth muted red-orange cap to the published apex, crown ring
    cylinder("dome_drum", 0, 0, H_COR1 - 0.4, DOME_Z0, DOME_R + 0.5, sand, seg=20)
    cylinder("dome_base_glow", 0, 0, DOME_Z0 - 0.55, DOME_Z0 - 0.05, DOME_R + 0.68, gold, seg=20)
    dome_cap("dome", DOME_R, DOME_Z0, H_APEX - 0.35, orange, seg=20, rings=9)
    cylinder("crown_ring", 0, 0, H_APEX - 0.75, H_APEX, 2.6, glow, seg=10)


def build_arm(label, path, mats):
    sand, trim, stone, orange, glow, gold = mats
    # ground strip
    path_band(f"{label}_terrace", path, 0.0, ARM_TER_H, ARM_TER_W, stone)
    # entablature band with cornice and a night-glow underside strip
    path_band(f"{label}_entab", path, H_AENT0, H_AENT1, ENT_W, sand)
    path_band(f"{label}_cornice", path, H_AENT1, H_ACOR1, ENT_W + 0.9, trim)
    path_band(f"{label}_glowband", path, H_AENT0 - 0.45, H_AENT0, ENT_W + 0.25, gold)

    # double column rows + maiden boxes every BOX_EVERY bays
    pts, tans = resample(path, ARM_BAY)
    for i, ((x, y), (tx, ty)) in enumerate(zip(pts, tans)):
        nx, ny = -ty, tx
        yaw = math.atan2(ty, tx)
        for s in (-1, 1):
            cx, cy = x + nx * ARM_ROW * s, y + ny * ARM_ROW * s
            box(f"{label}_b{i}{'ab'[s>0]}", cx, cy, H_AB, H_APED, 1.9, 1.9, sand, yaw)
            cylinder(f"{label}_c{i}{'ab'[s>0]}", cx, cy, H_APED, H_ASH, COL2_R, sand, seg=10)
            box(f"{label}_k{i}{'ab'[s>0]}", cx, cy, H_ASH, H_AENT0, 1.75, 1.75, trim, yaw)
        if i % BOX_EVERY == 1 and 0 < i < len(pts) - 1:
            maiden_box(f"{label}_box{i}", x, y, H_ACOR1, yaw, BOX_L, BOX_W, BOX_H, (sand, trim))


def build_gate(label, cx, cy, mats):
    sand, trim, stone, orange, glow, gold = mats
    box(f"{label}_terr", cx, cy, 0.0, ARM_TER_H, GATE_W + 4.0, GATE_W + 4.0, stone)
    box(f"{label}_glow", cx, cy, H_GATE_ENT0 - 0.4, H_GATE_ENT0, GATE_W + 0.6, GATE_W + 0.6, gold)
    d = GATE_W / 2 - 1.1
    for sx, sy in ((-d, -d), (d, -d), (d, d), (-d, d)):
        box(f"{label}_b{sx:.0f}{sy:.0f}", cx + sx, cy + sy, ARM_TER_H, H_APED, 2.1, 2.1, sand)
        cylinder(f"{label}_c{sx:.0f}{sy:.0f}", cx + sx, cy + sy, H_APED, H_ASH, 0.95, sand, seg=10)
        box(f"{label}_k{sx:.0f}{sy:.0f}", cx + sx, cy + sy, H_ASH, H_GATE_ENT0, 1.9, 1.9, trim)
    bevel(box(f"{label}_ent", cx, cy, H_GATE_ENT0, H_GATE_ENT1, GATE_W + 1.2, GATE_W + 1.2, sand), 0.14)
    maiden_box(f"{label}_box", cx, cy, H_GATE_ENT1, 0.0, GATE_W - 0.6, GATE_W - 0.6, H_GATE_TOP - H_GATE_ENT1 - 0.35, (sand, trim))


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    mats = (
        material("Toy_sand"),
        material("Toy_trim"),
        material("Toy_stone"),
        material("Toy_ioorange"),
        material("Toy_white_Glow"),
        material("Toy_gold_Glow"),
    )
    mats_green = (
        material("Toy_glass"),
        material("Toy_mint"),
        material("Toy_white"),
        material("Toy_ink"),
        material("Toy_pine"),
        material("Toy_leaf"),
    )
    build_rotunda(mats)
    build_arm("armN", ARM_N, mats)
    build_arm("armS", ARM_S, mats)
    build_gate("gateN", *GATE_N, mats)
    build_gate("gateS", *GATE_S, mats)
    build_grounds(mats, mats_green)
    return scene


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
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "palace-of-fine-arts.blend")
    glb = os.path.join(out, "palace-of-fine-arts.glb")
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
