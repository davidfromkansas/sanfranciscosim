"""Deterministic Blender build of the SF-SIM miniature Letterman Digital Arts Center.

    blender -b --python build_letterman_digital_arts_center.py -- [--out DIR]

Writes letterman-digital-arts-center.blend and .glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
origin at the composition's base centre, min Z = 0, so the export needs no
transforms applied after the fact.

Design (see REFERENCE.md for the sources behind every number):

* the four Lucasfilm campus buildings (A north, B southwest with the main ILM
  entrance, C south-centre, D southeast) extruded from their true OSM
  footprints (simplified ~2 m) at their true relative positions and headings —
  the loader applies no rotation, so the ~25-degree campus grid is authored in;
* the shared Presidio facade family: stone plinth, brick body with two stucco
  string courses, punched dark window grids, an arcade-scale ground row, and a
  clipped-hip terracotta roof with tidy vent clusters — four buildings, one
  toy-box family;
* the Halprin landscape as one diorama base: green meadow slab, the
  boulder-lined lagoon east of Building A, the rocky stream winding down the
  meadow into it, two stone overlook plazas, and grouped tree groves framing
  the architecture;
* the Yoda Fountain on Building B's forecourt, semantically exaggerated
  (style bible §9) into the campus's one saturated storytelling object.

_Glow is limited to two zones: Building B's entrance canopy fascia and door
(the hero), and one arcade window row per park-facing facade (the supporting
accents) — a campus at night is warm pools of light, not a lit tower.

Height normalization: the tallest roof ridge tops out at exactly 22.0 m (the
verified-estimated architectural height), and nothing — trees, fountain,
vents — exceeds it, so the loader's targetHeightM / measuredHeight = 1.0.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

# ---------------------------------------------------------------- parameters

# Local frame: metres from the campus anchor (-122.449439, 37.799731), +X east,
# +Y north, projected with the repo's fixed cos(37.77 deg) convention.
ANCHOR_LON = -122.449439
ANCHOR_LAT = 37.799731
LAT0 = 37.77  # repo projection latitude — keep identical to pipeline/app

GROUND_TOP = 1.0     # diorama meadow surface
Z_PLINTH = 2.2       # stone base top
Z_TRIM1 = (7.0, 7.45)   # stucco string course between brick base and cream body
Z_WALL = 16.6        # brick top
Z_DECK = 17.2        # terracotta eave band top
Z_HIP = 20.0         # hip deck (top of the sloped band off the eave)
Z_RIDGE = 21.0       # ridge beams; rooftop vents reach exactly 22.0 (targetHeightM)
HIP_INSET = 4.6      # eave -> hip deck

# Window rows: (z0, z1, pane width, pitch) — arcade row + two upper rows.
ROW_ARCADE = (2.4, 5.4, 2.6, 5.6)
ROWS_UPPER = [(8.0, 10.4, 1.9, 3.8), (12.6, 15.0, 1.9, 3.8)]
WIN_MARGIN = 3.0     # facade end margin
WIN_MIN_EDGE = 11.0  # facades shorter than this stay solid
WIN_OFF = 0.10       # pane float off the wall plane

# OSM footprints, simplified (RDP eps 2.0 m), CCW, local metres.
FOOTPRINTS = {
    "A": [(-52.8, 120.6), (-49.2, 115.7), (-57.5, 119.6), (-65.6, 102.7), (-57.1, 98.8), (-62.2, 88.0), (-73.3, 87.0), (-81.4, 69.5), (-72.7, 65.6), (-85.3, 38.4), (-96.5, 37.5), (-100.5, 28.9), (-95.7, 15.5), (-34.5, -8.3), (-25.7, 10.8), (-38.4, 16.7), (-10.7, 64.1), (-23.6, 70.1), (-9.4, 100.5), (-0.2, 97.6), (7.7, 114.5), (0.4, 122.5), (-43.6, 139.8)],
    "B": [(-109.2, -0.6), (-111.8, -5.9), (-115.9, -4.0), (-124.1, -21.6), (-113.6, -22.0), (-127.8, -52.2), (-136.9, -49.5), (-147.2, -70.8), (-120.2, -79.0), (-126.8, -93.1), (-133.2, -92.5), (-142.2, -113.2), (-105.1, -130.4), (-93.8, -111.1), (-109.2, -101.8), (-102.5, -87.2), (-60.6, -106.7), (-51.6, -87.6), (-68.8, -79.6), (-54.8, -49.4), (-45.7, -53.6), (-36.7, -34.3), (-45.7, -30.1), (-43.8, -26.1), (-76.5, -11.0), (-78.2, -14.9), (-83.8, -12.3)],
    "C": [(-9.9, -46.8), (-19.0, -65.9), (-5.9, -72.0), (-20.2, -102.4), (-29.0, -98.3), (-38.0, -117.4), (-3.3, -137.3), (-1.7, -133.7), (45.6, -139.4), (43.9, -118.4), (30.6, -118.5), (32.6, -85.2), (48.2, -84.0), (45.5, -63.1), (33.3, -64.0), (33.7, -60.1), (-3.1, -45.5)],
    "D": [(129.2, -44.8), (106.9, -47.6), (107.3, -51.3), (70.4, -60.0), (82.1, -113.5), (63.7, -115.9), (66.3, -136.9), (122.5, -134.1), (122.1, -129.9), (145.7, -125.7), (143.4, -107.1), (129.0, -107.7), (124.8, -74.6), (143.4, -72.1), (145.9, -56.4), (141.5, -57.0), (140.7, -51.1), (130.3, -51.9)],
}

# OSM lagoon (way/32651841), simplified, CCW, local metres.
LAGOON = [(58.7, 90.2), (54.9, 86.7), (57.1, 79.1), (63.0, 71.5), (62.3, 65.8), (57.9, 59.7), (59.5, 57.4), (66.2, 58.7), (86.9, 47.1), (89.4, 47.6), (100.0, 61.9), (98.9, 64.4), (86.1, 66.5), (81.6, 74.9), (72.0, 76.3), (63.6, 88.6)]

YODA = (-90.0, -106.0)          # forecourt fountain (OSM node nudged off B's wall)
CAMPUS_HEART = (0.0, -10.0)     # the central meadow the arcades face

# The meandering walk from B's forecourt across the meadow to the lagoon
# plaza and on toward the Presidio Promenade (TCLF).
WALK = [(-74.0, -104.0), (-52.0, -88.0), (-30.0, -66.0), (-14.0, -44.0), (2.0, -26.0), (18.0, -6.0), (30.0, 16.0), (40.0, 40.0), (52.0, 56.0), (70.0, 66.0), (96.0, 70.0), (120.0, 62.0)]

# The stream winds down the meadow into the lagoon's west edge (TCLF).
STREAM = [(-14.0, -34.0), (0.0, -22.0), (6.0, -6.0), (16.0, 8.0), (28.0, 22.0), (38.0, 38.0), (50.0, 52.0), (60.0, 66.0), (66.0, 72.0)]

# Grouped groves + singles framing the architecture (style bible §12).
TREES = [
    (30.0, 98.0, 5.8), (40.0, 87.0, 4.9), (21.0, 86.0, 5.2),          # lagoon-north grove
    (52.0, 20.0, 6.0), (62.0, 30.0, 5.1), (45.0, 32.0, 4.7), (58.0, 10.0, 5.4),  # meadow grove
    (-16.0, -28.0, 5.6), (-6.0, -38.0, 4.9),                          # heart pair
    (103.0, -32.0, 5.4), (119.0, -42.0, 4.7),                         # D forecourt pair
    (-152.0, 8.0, 5.2), (-142.0, 17.0, 4.7),                          # B west pair
    (108.0, 52.0, 5.0), (30.0, 58.0, 4.6), (-125.0, 22.0, 5.3), (140.0, -30.0, 4.8),
    (124.0, 12.0, 5.7), (134.0, 24.0, 4.9), (113.0, 24.0, 5.2),           # east meadow grove
    (86.0, 106.0, 5.1), (66.0, 112.0, 4.7),                               # lagoon-far pair
]

PLAZAS = [  # stone overlooks (TCLF: "two stone plazas with overlooks")
    (42.0, 40.0, 62.0, 60.0),
    (6.0, 56.0, 26.0, 76.0),
]

PALETTE_HEX = {
    "Toy_brick": "c96f4a",
    "Toy_cream": "f2ede3",
    "Toy_rust": "a86444",
    "Toy_trim": "f3efe6",
    "Toy_stone": "d9d2c2",
    "Toy_glass": "2a4d73",
    "Toy_roofd": "45454a",
    "Toy_mint": "8fd0a8",
    "Toy_verdigris": "9fb8a8",
    "Toy_sky": "6db3d9",
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
        # Flagged for the app's night pass; emission stays off in daylight.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    mat.blend_method = "OPAQUE"
    return mat


# -------------------------------------------------------------- mesh helpers


def link(obj):
    bpy.context.collection.objects.link(obj)
    return obj


def new_mesh(name, verts, faces, materials_, face_mats=None, recalc=True):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    for m in materials_:
        mesh.materials.append(m)
    if face_mats:
        for poly, mi in zip(mesh.polygons, face_mats):
            poly.material_index = mi
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    link(obj)
    if recalc:
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()
    mesh.shade_flat()
    return obj


def bevel_sharp(obj, width=0.12, segments=2, angle=math.radians(24)):
    """Miniature-style edge softening (style bible §4), silhouette edges only —
    beveling the coplanar material-band seams would triple the budget for
    invisible facets."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    edges = []
    for e in bm.edges:
        if len(e.link_faces) == 2 and e.calc_face_angle(None) is not None:
            if e.calc_face_angle() > angle:
                edges.append(e)
        elif len(e.link_faces) == 1:
            edges.append(e)
    bmesh.ops.bevel(
        bm,
        geom=edges,
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


def box(name, u0, v0, u1, v1, z0, z1, mat, yaw=0.0, pivot=None):
    verts = [
        (u0, v0, z0), (u1, v0, z0), (u1, v1, z0), (u0, v1, z0),
        (u0, v0, z1), (u1, v0, z1), (u1, v1, z1), (u0, v1, z1),
    ]
    if yaw:
        px, py = pivot if pivot else ((u0 + u1) / 2, (v0 + v1) / 2)
        c, s = math.cos(yaw), math.sin(yaw)
        verts = [
            (px + c * (x - px) - s * (y - py), py + s * (x - px) + c * (y - py), z)
            for x, y, z in verts
        ]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, [mat])


def cylinder(name, cx, cy, r, z0, z1, mat, segs=16):
    verts = []
    for z in (z0, z1):
        for i in range(segs):
            a = 2 * math.pi * i / segs
            verts.append((cx + r * math.cos(a), cy + r * math.sin(a), z))
    faces = [tuple(range(segs - 1, -1, -1)), tuple(range(segs, 2 * segs))]
    faces += [(i, (i + 1) % segs, segs + (i + 1) % segs, segs + i) for i in range(segs)]
    return new_mesh(name, verts, faces, [mat])


def blob(name, cx, cy, cz, r, mat, sx=1.0, sy=1.0, sz=1.0, seed=0):
    """A deterministic low-seg icosphere — tree crowns and lagoon boulders."""
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r)
    for i, v in enumerate(bm.verts):
        k = math.sin(seed * 12.9898 + i * 78.233) * 0.5  # deterministic jitter
        v.co *= 1.0 + 0.10 * k
        v.co.x *= sx
        v.co.y *= sy
        v.co.z *= sz
        v.co += Vector((cx, cy, cz))
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat)
    mesh.shade_flat()
    return link(bpy.data.objects.new(name, mesh))


def ribbon_faces(verts, count):
    """Quads along a two-rail ribbon, each wound so its normal points up."""
    faces = []
    for i in range(count - 1):
        a = 2 * i
        idx = (a, a + 1, a + 3, a + 2)
        p = [Vector(verts[j]) for j in idx[:3]]
        if (p[1] - p[0]).cross(p[2] - p[1]).z < 0:
            idx = tuple(reversed(idx))
        faces.append(idx)
    return faces


def poly_prism(name, poly, z0, z1, side_mat, top_mat=None, bottom_mat=None):
    """Extrude a CCW footprint into a capped solid with per-face materials."""
    top_mat = top_mat or side_mat
    bottom_mat = bottom_mat or side_mat
    n = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    mats = [bottom_mat, top_mat]
    face_mats = [0, 1]
    uniq = []
    for m in (bottom_mat, top_mat, side_mat):
        if m not in uniq:
            uniq.append(m)
    faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    fm = [uniq.index(bottom_mat), uniq.index(top_mat)] + [uniq.index(side_mat)] * n
    return new_mesh(name, verts, faces, uniq, face_mats=fm, recalc=False)


# ------------------------------------------------------------- the buildings


def clean_poly(poly, min_area=40.0, min_verts=8):
    """Visvalingam pass: drop the vertex spanning the smallest triangle until
    every remaining vertex matters. Kills the OSM micro-notches and spikes that
    self-intersect under RDP and break the hip inset (the black-face bug)."""
    pts = [Vector((x, y, 0.0)) for x, y in poly]
    while len(pts) > min_verts:
        best_i, best_a = -1, 1e18
        n = len(pts)
        for i in range(n):
            a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
            area = ((b - a).cross(c - b)).length / 2
            if area < best_a:
                best_i, best_a = i, area
        if best_a >= min_area:
            break
        pts.pop(best_i)
    return [(p.x, p.y) for p in pts]


def wall_band_mat(z):
    """0 stone plinth / 1 brick base / 2 trim course / 3 rust / 4 cream body."""
    if z <= Z_PLINTH:
        return 0
    if Z_TRIM1[0] <= z <= Z_TRIM1[1]:
        return 2
    if z >= Z_WALL:
        return 3
    if z > Z_TRIM1[1]:
        return 4
    return 1


def building(name, poly):
    """One campus building: stacked banded walls + clipped-hip terracotta roof."""
    mats = (
        material("Toy_stone"), material("Toy_brick"),
        material("Toy_trim"), material("Toy_rust"), material("Toy_cream"),
    )
    levels = [Z_PLINTH, Z_TRIM1[0], Z_TRIM1[1], Z_WALL, Z_DECK]
    poly = clean_poly(poly)

    bm = bmesh.new()
    vs = [bm.verts.new((x, y, GROUND_TOP)) for x, y in poly]
    f = bm.faces.new(vs)
    bm.normal_update()
    if f.normal.z < 0:
        f.normal_flip()
    top = f
    for z in levels:
        res = bmesh.ops.extrude_face_region(bm, geom=[top])
        new_faces = [g for g in res["geom"] if isinstance(g, bmesh.types.BMFace)]
        for face in new_faces:
            for v in face.verts:
                v.co.z = z
        top = new_faces[0]

    # Clipped hip: ONE inset off the eave, lifted to the hip deck. A second
    # inset pass was tried and self-intersects wherever a wing is narrower than
    # twice the offset (the straight skeleton collapses), which exports as
    # inverted black roof faces. The ridge line comes from a separate beam
    # solid instead — deterministic and impossible to degenerate.
    bmesh.ops.inset_region(
        bm, faces=[top], thickness=HIP_INSET, use_even_offset=True, depth=0.0
    )
    for v in top.verts:
        v.co.z = Z_HIP
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    for m in mats:
        mesh.materials.append(m)
    for p in mesh.polygons:
        z = sum(mesh.vertices[i].co.z for i in p.vertices) / len(p.vertices)
        if abs(p.normal.z) > 0.35:      # caps, hip slopes, plateau, bottom
            p.material_index = 3 if z > Z_WALL - 0.1 else 0
        else:                            # vertical wall band by height
            p.material_index = wall_band_mat(z)
    mesh.shade_flat()
    obj = link(bpy.data.objects.new(name, mesh))
    return bevel_sharp(obj, 0.12)


def edge_frames(poly):
    """(p0, p1, length, outward-normal) per CCW footprint edge."""
    out = []
    n = len(poly)
    for i in range(n):
        p0, p1 = Vector(poly[i]).to_3d(), Vector(poly[(i + 1) % n]).to_3d()
        d = p1 - p0
        length = d.length
        if length < 1e-6:
            continue
        d /= length
        out.append((p0, p1, length, Vector((d.y, -d.x, 0.0))))
    return out


def pane_row(verts, faces, fmats, p0, d, nrm, z0, z1, w, pitch, length,
             row_key, glow_sink=None):
    count = int((length - 2 * WIN_MARGIN + (pitch - w)) // pitch)
    if count < 1:
        return
    total = count * pitch - (pitch - w)
    s0 = (length - total) / 2
    for k in range(count):
        for off, sink in ((WIN_OFF, None), (WIN_OFF + 0.03, glow_sink)):
            if sink is not None and not lit(row_key, k):
                continue
            a = p0 + d * (s0 + k * pitch) + nrm * off
            b = a + d * w
            tgt = verts if sink is None else sink[0]
            tfc = faces if sink is None else sink[1]
            tfm = fmats if sink is None else None
            i = len(tgt)
            tgt += [
                (a.x, a.y, z0), (b.x, b.y, z0), (b.x, b.y, z1), (a.x, a.y, z1),
            ]
            # wind so the face normal agrees with the outward wall normal
            va, vb, vc = Vector(tgt[i]), Vector(tgt[i + 1]), Vector(tgt[i + 2])
            idx = (i, i + 1, i + 2, i + 3)
            if (vb - va).cross(vc - vb).dot(nrm) < 0:
                idx = tuple(reversed(idx))
            tfc.append(idx)
            if tfm is not None:
                tfm.append(0)


def lit(row_key, k):
    """Deterministic 'lights on in this room' choice — ~3/8 of the panes,
    scattered so the campus reads as occupied, never as a switchboard."""
    return (k * 7919 + row_key * 131) % 8 < 3


def windows(name, poly):
    """One building's panes in one glass mesh + one gold `_Glow` veneer mesh.

    The app draws a glow face at 0.12 opacity by day and 1.0 at night, so the
    lit-room veneers hover 3 cm in front of their always-present glass panes
    (the fairmont pattern): by day they barely tint the glass, by night they
    are the lit rooms."""
    glass, glow = material("Toy_glass"), material("Toy_gold_Glow")
    verts, faces, fmats = [], [], []
    gverts, gfaces = [], []
    sink = (gverts, gfaces)
    row_key = 0
    for ei, (p0, p1, length, nrm) in enumerate(edge_frames(poly)):
        if length < WIN_MIN_EDGE:
            continue
        d = (p1 - p0).normalized()
        az0, az1, aw, apitch = ROW_ARCADE
        for z0, z1, w, pitch in [(az0, az1, aw, apitch)] + ROWS_UPPER:
            row_key += 1
            pane_row(verts, faces, fmats, p0, d, nrm, z0, z1, w, pitch, length,
                     row_key, glow_sink=sink)
    new_mesh(name, verts, faces, [glass], face_mats=fmats, recalc=False)
    if gfaces:
        new_mesh(f"{name}_lit", gverts, gfaces, [glow], recalc=False)


def nearest_edge(poly, target):
    """Index of the footprint edge whose midpoint is closest to target."""
    t = Vector(target).to_3d()
    best, best_d = 0, 1e18
    for i, (p0, p1, length, _n) in enumerate(edge_frames(poly)):
        if length < WIN_MIN_EDGE:
            continue
        d = ((p0 + p1) / 2 - t).length
        if d < best_d:
            best, best_d = i, d
    return best


def longest_edge_angle(poly):
    frames = edge_frames(poly)
    p0, p1, _l, _n = max(frames, key=lambda f: f[2])
    d = p1 - p0
    return math.atan2(d.y, d.x)


def roof_clutter(name, poly, k):
    """Roof as a designed second facade (style bible §10): dormer rows marching
    along the long eaves, plus two tidy mechanical clusters on the ridge."""
    roofd, trim = material("Toy_roofd"), material("Toy_trim")
    cream, glass = material("Toy_cream"), material("Toy_glass")
    poly = clean_poly(poly)
    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)
    ang = longest_edge_angle(poly)
    c, s = math.cos(ang), math.sin(ang)

    # dormers: evenly along every eave long enough to carry a row
    d_i = 0
    for p0, p1, length, nrm in edge_frames(poly):
        if length < 26.0:
            continue
        d = (p1 - p0).normalized()
        count = max(2, int((length - 12.0) // 13.0))
        span = length - 12.0
        for j in range(count):
            t = 6.0 + span * (j + 0.5) / count
            base = p0 + d * t - nrm * (HIP_INSET * 0.55)
            zt = Z_DECK + (Z_HIP - Z_DECK) * 0.55
            w, dp = 2.6, 2.4
            a = base - d * (w / 2)
            corners = [a, a + d * w, a + d * w + nrm * dp, a + nrm * dp]
            verts = ([(p.x, p.y, zt) for p in corners]
                     + [(p.x, p.y, zt + 2.3) for p in corners])
            faces = [(3, 2, 1, 0), (4, 5, 6, 7),
                     (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
            bevel_sharp(new_mesh(f"{name}_dormer{d_i}", verts, faces, [cream]), 0.07)
            # dark pane on the dormer's outward face
            f0 = a + d * 0.5 + nrm * (dp + 0.02)
            f1 = f0 + d * (w - 1.0)
            gv = [(f0.x, f0.y, zt + 0.5), (f1.x, f1.y, zt + 0.5),
                  (f1.x, f1.y, zt + 1.9), (f0.x, f0.y, zt + 1.9)]
            v = [Vector(q) for q in gv]
            idx = (0, 1, 2, 3)
            if (v[1] - v[0]).cross(v[2] - v[1]).dot(nrm) < 0:
                idx = tuple(reversed(idx))
            new_mesh(f"{name}_dormerpane{d_i}", gv, [idx], [glass], recalc=False)
            d_i += 1

    # ridge beam: the line that turns the hip deck into a roof rather than a
    # plateau. Length from the footprint's own extent along its long axis.
    ext = [(x - cx) * c + (y - cy) * s for x, y in poly]
    half = (max(ext) - min(ext)) / 2 * 0.62
    mid = (max(ext) + min(ext)) / 2
    bevel_sharp(box(f"{name}_ridge", mid - half, -1.5, mid + half, 1.5,
                    Z_HIP, Z_RIDGE, material("Toy_rust"), yaw=ang,
                    pivot=(0.0, 0.0)), 0.1)
    ridge = bpy.data.objects[f"{name}_ridge"]
    ridge.data.transform(Matrix.Translation(Vector((cx, cy, 0.0))))

    spots = [(cx + 9 * c, cy + 9 * s), (cx - 11 * c, cy - 11 * s)]
    for j, (px, py) in enumerate(spots):
        # tallest vent tops out at exactly 22.0 — the model's bbox top
        bevel_sharp(box(f"{name}_vent{j}a", px - 2.2, py - 1.6, px + 2.2, py + 1.6,
                        Z_RIDGE, Z_RIDGE + 1.0 - 0.15 * j, roofd, yaw=ang), 0.08)
        bevel_sharp(box(f"{name}_vent{j}b", px + 2.8, py - 1.1, px + 5.0, py + 1.1,
                        Z_RIDGE, Z_RIDGE + 0.75, trim, yaw=ang, pivot=(px, py)), 0.08)


# ------------------------------------------------------------- the landscape


def convex_hull(points):
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def ground():
    """One diorama base: the campus hull + margin, meadow top, stone sides."""
    pts = []
    for poly in FOOTPRINTS.values():
        pts += poly
    pts += LAGOON
    pts += [(YODA[0] + dx, YODA[1] + dy) for dx in (-18, 18) for dy in (-18, 18)]
    pts += [(p[0], p[1]) for p in STREAM]
    hull = convex_hull([(round(x, 2), round(y, 2)) for x, y in pts])
    cx = sum(p[0] for p in hull) / len(hull)
    cy = sum(p[1] for p in hull) / len(hull)
    grown = []
    for x, y in hull:
        v = Vector((x - cx, y - cy))
        v = v.normalized() * 10.0
        grown.append((x + v.x, y + v.y))
    obj = poly_prism("ground", grown, 0.0, GROUND_TOP,
                     material("Toy_stone"), top_mat=material("Toy_mint"),
                     bottom_mat=material("Toy_stone"))
    return bevel_sharp(obj, 0.25, angle=math.radians(40))


def lagoon():
    sky, stone = material("Toy_sky"), material("Toy_stone")
    poly_prism("lagoon_water", LAGOON, GROUND_TOP - 0.4, GROUND_TOP + 0.06,
               stone, top_mat=sky, bottom_mat=stone)
    # boulder rim (TCLF: "boulder-lined lagoon") — clustered, not a necklace:
    # three deterministic clusters of 2-3 sunk stones instead of an even ring
    frames = edge_frames(LAGOON)
    total = sum(f[2] for f in frames)
    placed = 0
    for frac, count in ((0.08, 3), (0.45, 2), (0.74, 3)):
        target = total * frac
        run = 0.0
        for p0, p1, length, nrm in frames:
            if run + length < target:
                run += length
                continue
            d = (p1 - p0).normalized()
            base = p0 + d * (target - run)
            for k in range(count):
                pos = base + d * (k * 2.6) + nrm * (0.5 + 0.5 * (k % 2))
                r = 1.3 + 0.8 * abs(math.sin((placed + 1) * 2.399))
                blob(f"boulder_{placed}", pos.x, pos.y, GROUND_TOP + r * 0.18, r,
                     stone, sz=0.62, seed=placed)
                placed += 1
            break


def stream():
    """One confident ribbon of water winding down the meadow (TCLF)."""
    sky = material("Toy_sky")
    half = 1.9
    pts = [Vector((x, y, GROUND_TOP + 0.05)) for x, y in STREAM]
    verts, faces = [], []
    for i, p in enumerate(pts):
        d = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)])
        d.z = 0
        d.normalize()
        n = Vector((d.y, -d.x, 0))
        w = half * (1.0 + 0.35 * math.sin(i * 1.7))  # gentle width variation
        verts += [p + n * w, p - n * w]
    faces = ribbon_faces(verts, len(pts))
    return new_mesh("stream", [tuple(v) for v in verts], faces, [sky], recalc=False)


def walk():
    """The meandering walk across the meadow (TCLF) — the graphic line that
    keeps the big green from reading as an empty slab (style bible §13)."""
    stone = material("Toy_stone")
    pts = [Vector((x, y, GROUND_TOP + 0.04)) for x, y in WALK]
    verts, faces = [], []
    for i, p in enumerate(pts):
        d = pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]
        d.z = 0
        d.normalize()
        n = Vector((d.y, -d.x, 0)) * 1.5
        verts += [p + n, p - n]
    faces = ribbon_faces(verts, len(pts))
    return new_mesh("walk", [tuple(v) for v in verts], faces, [stone], recalc=False)


def plazas():
    stone = material("Toy_stone")
    for i, (x0, y0, x1, y1) in enumerate(PLAZAS):
        bevel_sharp(box(f"plaza_{i}", x0, y0, x1, y1,
                        GROUND_TOP, GROUND_TOP + 0.22, stone), 0.05)
    cylinder("forecourt", YODA[0], YODA[1], 16.0,
             GROUND_TOP, GROUND_TOP + 0.16, stone, segs=24)


def yoda_fountain():
    """The campus's one saturated storytelling object, exaggerated ~3x."""
    stone, sky = material("Toy_stone"), material("Toy_sky")
    verd = material("Toy_verdigris")
    x, y = YODA
    bevel_sharp(cylinder("yoda_pool", x, y, 5.2, GROUND_TOP, GROUND_TOP + 1.1,
                         stone, segs=18), 0.08)
    cylinder("yoda_water", x, y, 4.5, GROUND_TOP + 0.6, GROUND_TOP + 0.95, sky, segs=18)
    bevel_sharp(box("yoda_plinth", x - 1.2, y - 1.2, x + 1.2, y + 1.2,
                    GROUND_TOP + 0.95, GROUND_TOP + 3.0, stone), 0.1)
    # the figure: robe cone, head, two ears — abstract but unmistakable
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=10,
                          radius1=1.55, radius2=0.6, depth=2.6)
    for v in bm.verts:
        v.co += Vector((x, y, GROUND_TOP + 3.0 + 1.3))
    mesh = bpy.data.meshes.new("yoda_robe")
    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(verd)
    mesh.shade_flat()
    link(bpy.data.objects.new("yoda_robe", mesh))
    hz = GROUND_TOP + 6.5
    blob("yoda_head", x, y, hz, 0.95, verd, sz=0.9, seed=41)
    for k, side in enumerate((-1, 1)):
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=6,
                              radius1=0.34, radius2=0.04, depth=1.5)
        rot = Matrix.Rotation(math.radians(78 * side), 4, "Y")
        for v in bm.verts:
            v.co = rot @ v.co + Vector((x + side * 1.1, y, hz + 0.3))
        mesh = bpy.data.meshes.new(f"yoda_ear_{k}")
        bm.to_mesh(mesh)
        bm.free()
        mesh.materials.append(verd)
        mesh.shade_flat()
        link(bpy.data.objects.new(f"yoda_ear_{k}", mesh))


def trees():
    ink, mint = material("Toy_roofd"), material("Toy_mint")
    verd = material("Toy_verdigris")
    for i, (x, y, r) in enumerate(TREES):
        cylinder(f"trunk_{i}", x, y, 0.55, GROUND_TOP, GROUND_TOP + 3.2, ink, segs=8)
        crown = verd if i % 5 == 4 else mint  # mostly vivid green, a few sages
        blob(f"crown_{i}", x, y, GROUND_TOP + 3.2 + r * 0.62, r, crown,
             sz=0.85, seed=i)


def entrance(poly):
    """Building B's ILM entrance: canopy + glow fascia + glow door, facing the
    Yoda forecourt."""
    trim, glow = material("Toy_trim"), material("Toy_white_Glow")
    frames = edge_frames(poly)
    ei = nearest_edge(poly, YODA)
    p0, p1, length, nrm = frames[ei]
    d = (p1 - p0).normalized()
    t = Vector(YODA).to_3d() - p0
    s = max(6.0, min(length - 6.0, t.dot(d)))  # entrance abreast of the fountain
    c = p0 + d * s
    w, depth = 5.5, 2.6
    a = c - d * w / 2
    quads = []
    # canopy slab
    v0 = a + nrm * 0.0
    corners = [v0, v0 + d * w, v0 + d * w + nrm * depth, v0 + nrm * depth]
    verts = [(p.x, p.y, 5.6) for p in corners] + [(p.x, p.y, 6.1) for p in corners]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7),
             (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    bevel_sharp(new_mesh("b_canopy", verts, faces, [trim]), 0.06)
    # glow fascia strip on the canopy's outer face
    f0 = a + nrm * (depth - 0.05)
    fverts = [
        (f0.x, f0.y, 5.62), ((f0 + d * w).x, (f0 + d * w).y, 5.62),
        ((f0 + d * w).x, (f0 + d * w).y, 6.08), (f0.x, f0.y, 6.08),
    ]
    fv = [Vector(v) for v in fverts]
    idx = (0, 1, 2, 3)
    if (fv[1] - fv[0]).cross(fv[2] - fv[1]).dot(nrm) < 0:
        idx = tuple(reversed(idx))
    new_mesh("b_glow_fascia", fverts, [idx], [glow], recalc=False)
    # glow door pane under the canopy
    g0 = a + d * (w / 2 - 1.8) + nrm * WIN_OFF
    g1 = g0 + d * 3.6
    dverts = [(g0.x, g0.y, GROUND_TOP + 0.4), (g1.x, g1.y, GROUND_TOP + 0.4),
              (g1.x, g1.y, 5.0), (g0.x, g0.y, 5.0)]
    dv = [Vector(v) for v in dverts]
    idx = (0, 1, 2, 3)
    if (dv[1] - dv[0]).cross(dv[2] - dv[1]).dot(nrm) < 0:
        idx = tuple(reversed(idx))
    new_mesh("b_glow_door", dverts, [idx], [glow], recalc=False)


# ------------------------------------------------------------------ assembly


def build():
    ground()
    for name, poly in FOOTPRINTS.items():
        building(f"bldg_{name}", poly)
        windows(f"win_{name}", poly)
        roof_clutter(f"roof_{name}", poly, name)
    entrance(FOOTPRINTS["B"])
    lagoon()
    stream()
    walk()
    plazas()
    yoda_fountain()
    trees()


def finalize():
    """Centre the bbox in XY, keep min Z at 0, report the corrected anchor."""
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    for o in meshes:
        for v in o.data.vertices:
            for i in range(3):
                mn[i] = min(mn[i], v.co[i])
                mx[i] = max(mx[i], v.co[i])
    centre = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, mn.z))
    for o in meshes:
        for v in o.data.vertices:
            v.co -= centre
        o.data.update()

    lon = ANCHOR_LON + centre.x / (111320.0 * math.cos(math.radians(LAT0)))
    lat = ANCHOR_LAT + centre.y / 110540.0
    print(f"[build] recentre shift x={centre.x:.3f} y={centre.y:.3f} z={centre.z:.3f}")
    print(f"[build] manifest anchor lon={lon:.7f} lat={lat:.7f}")

    dg = bpy.context.evaluated_depsgraph_get()
    tris = 0
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for o in meshes:
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    print(f"[build] objects={len(meshes)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 4) for i in range(3)]}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    build()
    finalize()

    blend = os.path.join(out, "letterman-digital-arts-center.blend")
    glb = os.path.join(out, "letterman-digital-arts-center.glb")
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
