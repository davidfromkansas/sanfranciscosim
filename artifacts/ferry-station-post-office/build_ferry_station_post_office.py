"""Deterministic Blender build of the SF-SIM miniature Ferry Station Post Office
Building (the Agriculture Building), 101 The Embarcadero, San Francisco.

    blender -b --python build_ferry_station_post_office.py -- [--out DIR]

Writes ferry-station-post-office.blend and .glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = footprint AABB centre (anchor
lon -122.3921505, lat 37.7941368), min Z = 0, clay-tile hip ridge exactly
12.65 m.

Design (see REFERENCE.md for the source behind every number):

* A. A. Pyle, 1915, for the State Board of Harbor Commissioners: a two-storey
  riveted-steel Mediterranean palazzo on a timber-pile wharf, red pressed brick
  in Flemish bond over a granite base, trompe-l'oeil terracotta trim, copper
  cornice, low-pitched clay-tile hip roof;
* the identity is the WIDE TILED HIP ROOF over the Embarcadero front — a 16.6 m
  band across the whole 50.74 m frontage, hipped at both ends, ridge at 12.65 m,
  which is the only thing of its kind on the Embarcadero;
* second identity is the THREE-PAVILION FRONT: rusticated terracotta corner
  quoins, terracotta end-pavilion entrances, wide full-height terracotta piers
  setting those pavilions off, a terracotta central pavilion with the phoenix
  shield and the out-thrust flagstaff, and red brick in the two fields between;
* the facade is banded — a high first floor of tall windows, a deep terracotta
  string course, a squat second floor of near-square windows with diamond brick
  panels between them, and the dark copper cornice;
* the roof is the asset: tiled hip in front, a flat two-storey deck behind it, a
  big flat one-storey work-room deck with three roof monitors behind that, a dark
  light-well slot, and the 1918/19 tiled SE wing running out over the ferry slips;
* night state: the entrance transom is the hero (warm gold), with a sparse,
  irregular scatter of first-floor windows on the Embarcadero front only. Glow
  surfaces are thin plates proud of opaque glazing — the app renders _Glow in a
  separate layer at ~12% alpha by day (more where a closed shell stacks two
  layers), so a primary surface must never be authored as glow, and a _Glow
  material's BASE colour is what it looks like at night.

Everything is laid out in the building's own (s, w) frame: s runs along the
Embarcadero frontage from the west corner, w runs inward from the frontage. The
footprint is a 50.74 x 39.00 m rectangle in that frame plus a 10.89 x 8.20 m
bump-out on the bay side at the SE end (the 1919 dolphin extension), which is
why authoring in (s, w) and converting once is simpler than fighting the 54 deg
heading.

Walls are SOLID prisms with no cut openings; every opening is drawn proud of the
wall and reads as a recess because the piers and quoins stand out in front of it
(style bible s.5). No booleans anywhere.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# Anchor = footprint AABB centre, lon -122.3921505 lat 37.7941368.
# V1 (the west corner, s = 0 w = 0) in metres relative to that anchor, and the
# frontage tangent/outward normal, all measured from OSM way/104599975 projected
# with the app's tangent projection (LON0 -122.4375, LAT0 37.77).
V1 = (-34.10, 9.15)
T = (0.5883944, -0.8085741)     # +s, along the frontage, bearing 144.0 deg
N = (-0.8085741, -0.5883944)    # outward from the frontage, bearing 234.0 deg

S_FRONT = 50.74     # Embarcadero frontage
W_MAIN = 39.00      # depth of the main rectangle
S_BUMP = 39.85      # bump-out starts here in s
W_BUMP = 47.20      # bump-out reaches this depth

# footprint ring in (s, w), CCW
RING = [(0.0, 0.0), (S_FRONT, 0.0), (S_FRONT, W_BUMP), (S_BUMP, W_BUMP),
        (S_BUMP, W_MAIN), (0.0, W_MAIN)]

W_TILE = 16.60      # depth of the tiled front band
W_TWO = 25.90       # depth of the two-storey block (NRHP: 85 ft second floor)
S_SLOT0, S_SLOT1 = 36.50, 40.00   # the light-well slot
S_WING = 40.00      # SE wing starts here in s
S_MID = (9.00, 36.50)   # the two-storey block is only this deep over this run;
                        # beyond it the work-room deck runs from the tile straight
                        # back to the bay, which is where the roof monitors sit

Z_BASE = 1.00       # granite plinth top
Z_W1 = (1.90, 5.30)   # first-floor window band
Z_STR = (5.70, 6.70)  # terracotta string course
Z_W2 = (7.40, 9.50)   # second-floor window band
Z_CORN = (10.20, 10.80)   # copper cornice band; its top is the tile eave
Z_RIDGE = 12.65     # clay-tile hip ridge = the export's bounding-box top
Z_MID = 9.80        # flat deck behind the tile, inside the cornice
Z_LOWBODY = 5.40    # top of the one-storey body (= the light-well floor)
Z_LOW = 6.60        # one-storey work-room roof deck
Z_LOWPAR = 7.30     # its brick parapet
Z_LOWCAP = 7.45     # its terracotta coping
Z_SEW = 9.40        # SE wing wall top
Z_SEWC = 9.90       # SE wing cornice top = its tile eave
Z_SEWR = 11.05      # SE wing tile ridge

W_RIDGE = 8.30      # the front tile ridge sits at this depth; hips run 8.30 m
S_WRIDGE = (S_WING + S_FRONT) / 2.0   # SE wing ridge, running along w
EAVE_OVER = 0.42    # tile overhang; the copper cornice projects further (0.72)

BEVEL_W = 0.12
BEVEL_SEG = 2

PALETTE_HEX = {
    "Toy_brick": "c96f4a",
    "Toy_rust": "a86444",
    "Toy_sand": "ece4d4",
    "Toy_stone": "d9d2c2",
    "Toy_steel": "9aa0a6",
    "Toy_ink": "3a3530",
    "Toy_roofd": "45454a",
    "Toy_glass": "2a4d73",
    "Toy_gold": "caa64a",
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


# --------------------------------------------------------------- 2D helpers


def sw(s, w):
    """Building frame -> world XY, metres, relative to the anchor."""
    return (V1[0] + T[0] * s - N[0] * w, V1[1] + T[1] * s - N[1] * w)


# ---- the four exposed faces, each as (fixed coordinate, along-axis, sign) ----
# `face_pt(face, a, d)` returns (s, w) for a point `a` along the face and `d`
# outward from it (negative = buried in the wall).
FACES = {
    "front": ("w", 0.0, "s", -1.0),      # w = 0, a runs in s, outward = -w
    "nw": ("s", 0.0, "w", -1.0),         # s = 0, a runs in w, outward = -s
    "se": ("s", S_FRONT, "w", +1.0),     # s = S_FRONT, outward = +s
    "rear": ("w", W_MAIN, "s", +1.0),    # w = W_MAIN, outward = +w
    "bumpend": ("w", W_BUMP, "s", +1.0),
    "bumpside": ("s", S_BUMP, "w", -1.0),
}


def face_pt(face, a, d):
    fixed_axis, fixed_val, along_axis, sign = FACES[face]
    out = sign * d
    if fixed_axis == "w":
        return (a, fixed_val + out)
    return (fixed_val + out, a)


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


def bevel(obj, width=BEVEL_W, segments=BEVEL_SEG):
    """Miniature-style edge softening (style bible s.4). Width is clamped to 40%
    of the thinnest dimension; without that, bevelling a thin plate at full width
    collapses faces into zero-area triangles and flips signed volume."""
    thin = min(obj.dimensions)
    width = min(width, thin * 0.4)
    if width < 1e-4:
        return obj
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
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = obj.data
    bm.to_mesh(me)
    bm.free()
    me.shade_flat()
    return obj


def ensure_outward(obj):
    """Positive signed volume — the validator's authoritative normals test for a
    union of closed solids."""
    me = obj.data
    me.calc_loop_triangles()
    vol = 0.0
    for tri in me.loop_triangles:
        a, b, c = (obj.matrix_world @ me.vertices[i].co for i in tri.vertices)
        vol += a.dot(b.cross(c)) / 6.0
    if vol <= 0.0:
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
        bm.to_mesh(me)
        bm.free()
        me.shade_flat()
    return obj


def prism(name, poly_sw, z0, z1, mat, mat_caps=None):
    """Closed extrusion of an (s, w) polygon."""
    poly = [sw(s, w) for s, w in poly_sw]
    n = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces, face_mats = [], []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
        face_mats.append(0)
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    face_mats += [1 if mat_caps else 0] * 2
    mats = [mat, mat_caps] if mat_caps else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def box(name, s0, s1, w0, w1, z0, z1, mat):
    """Closed box on an (s, w) rectangle."""
    return prism(name, [(s0, w0), (s1, w0), (s1, w1), (s0, w1)], z0, z1, mat)


def face_box(name, face, a0, a1, z0, z1, d_in, d_out, mat):
    """Box hung on one face: `a` along the face, `d` outward from it."""
    pts = [face_pt(face, a0, d_in), face_pt(face, a1, d_in),
           face_pt(face, a1, d_out), face_pt(face, a0, d_out)]
    return prism(name, pts, z0, z1, mat)


def band(name, poly_sw, z0, z1, off_in, off_out, mat):
    """Closed band following an (s, w) polygon, offset outward by off_in/off_out."""
    def offset(d):
        n = len(poly_sw)
        normals = []
        for i in range(n):
            a, b = poly_sw[i], poly_sw[(i + 1) % n]
            ds, dw = b[0] - a[0], b[1] - a[1]
            ln = math.hypot(ds, dw) or 1.0
            normals.append((dw / ln, -ds / ln))
        out = []
        for i in range(n):
            n1, n2 = normals[i - 1], normals[i]
            v = poly_sw[i]
            det = n1[0] * n2[1] - n1[1] * n2[0]
            if abs(det) < 1e-6:
                out.append((v[0] + n2[0] * d, v[1] + n2[1] * d))
                continue
            c1 = v[0] * n1[0] + v[1] * n1[1] + d
            c2 = v[0] * n2[0] + v[1] * n2[1] + d
            out.append(((c1 * n2[1] - c2 * n1[1]) / det, (c2 * n1[0] - c1 * n2[0]) / det))
        return out

    lo_in = [sw(*p) for p in offset(off_in)]
    lo_out = [sw(*p) for p in offset(off_out)]
    n = len(lo_in)
    verts = []
    for loop, z in ((lo_in, z0), (lo_out, z0), (lo_out, z1), (lo_in, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * n, ((k + 1) % 4) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def hip_roof(name, s0, s1, w0, w1, z_eave, z_ridge, ridge_along, ridge_at,
             mat, fascia=0.30):
    """A closed low-pitch hip-roof solid over an (s, w) rectangle.

    `ridge_along` is 's' (ridge runs in s, slopes face -w/+w) or 'w'. `ridge_at`
    is the ridge's position on the other axis. The hip run is taken as the
    distance from the ridge to the nearer eave, which is what a constant-pitch
    hip gives, and is how the nadir imagery reads both of this building's roofs.
    """
    if ridge_along == "s":
        run = min(ridge_at - w0, w1 - ridge_at)
        r0 = (s0 + run, ridge_at)
        r1 = (s1 - run, ridge_at)
    else:
        run = min(ridge_at - s0, s1 - ridge_at)
        r0 = (ridge_at, w0 + run)
        r1 = (ridge_at, w1 - run)
    e = [(s0, w0), (s1, w0), (s1, w1), (s0, w1)]
    pe = [sw(*p) for p in e]
    pr = [sw(*p) for p in (r0, r1)]
    verts = [(x, y, z_eave - fascia) for x, y in pe]        # 0..3 lower eave
    verts += [(x, y, z_eave) for x, y in pe]                # 4..7 eave
    verts += [(x, y, z_ridge) for x, y in pr]               # 8, 9 ridge
    faces = [(3, 2, 1, 0)]                                  # underside
    for i in range(4):                                      # fascia
        j = (i + 1) % 4
        faces.append((i, j, 4 + j, 4 + i))
    if ridge_along == "s":
        faces += [(4, 5, 9, 8), (6, 7, 8, 9), (5, 6, 9), (7, 4, 8)]
    else:
        faces += [(5, 6, 9, 8), (7, 4, 8, 9), (6, 7, 9), (4, 5, 8)]
    return new_mesh(name, verts, faces, [mat])


# --------------------------------------------------------------- the facade

# The Embarcadero front, in metres from the west corner. Measured off a metric
# rectification of Street View pano PJ2Y60ERa8pqvq0e-Pwxlw and then made exactly
# symmetric about the frontage centre (25.37 m), which the building is.
QUOIN = 2.10          # rusticated terracotta corner strip
END0, END1 = 2.10, 6.80       # NW end-pavilion terracotta surround
PIER0, PIER1 = 6.80, 9.00     # wide full-height terracotta pier
FIELD_A = (9.00, 21.57)
CENTRE = (21.57, 29.17)
FIELD_B = (29.17, 41.74)
DOOR_W = 2.10
CENTRE_DOOR_W = 2.20


def mirror(s):
    return S_FRONT - s


def field_bays(f0, f1, n=3):
    return [f0 + (f1 - f0) * (k + 0.5) / n for k in range(n)]


BAYS = field_bays(*FIELD_A) + field_bays(*FIELD_B)
DIAMONDS = []
for f0, f1 in (FIELD_A, FIELD_B):
    c = field_bays(f0, f1)
    DIAMONDS += [(c[0] + c[1]) / 2.0, (c[1] + c[2]) / 2.0]

# Sparse, irregular, first floor only, Embarcadero front only.
LIT_BAYS = {0, 2, 3, 5}


def materials():
    mats = {}
    for name, rgb in PALETTE.items():
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        bsdf = m.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.85
        bsdf.inputs["Metallic"].default_value = 0.0
        if name.endswith("_Glow"):
            bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 0.0
        mats[name] = m
    return mats


def window_pair(tag, face, centre, wid1, wid2, mats, lit=False):
    """One bay: a tall first-floor opening and a squat second-floor one, both
    drawn proud of the wall and reading as recesses against the piers."""
    glass, sand, ink = mats["Toy_glass"], mats["Toy_sand"], mats["Toy_ink"]
    a0, a1 = centre - wid1 / 2.0, centre + wid1 / 2.0
    face_box(f"{tag}_r1", face, a0 - 0.22, a1 + 0.22, Z_W1[0] - 0.22, Z_W1[1] + 0.22,
             -0.04, 0.05, mats["Toy_brick"])
    face_box(f"{tag}_g1", face, a0, a1, *Z_W1, 0.02, 0.11, glass)
    face_box(f"{tag}_s1", face, a0 - 0.16, a1 + 0.16, Z_W1[0] - 0.30, Z_W1[0] - 0.06,
             0.02, 0.20, sand)
    face_box(f"{tag}_l1", face, a0 - 0.10, a1 + 0.10, Z_W1[1] + 0.04, Z_W1[1] + 0.22,
             0.02, 0.16, sand)
    b0, b1 = centre - wid2 / 2.0, centre + wid2 / 2.0
    face_box(f"{tag}_g2", face, b0, b1, *Z_W2, 0.02, 0.11, glass)
    face_box(f"{tag}_s2", face, b0 - 0.14, b1 + 0.14, Z_W2[0] - 0.26, Z_W2[0] - 0.06,
             0.02, 0.18, sand)
    if lit:
        face_box(f"{tag}_lit", face, a0 + 0.28, a1 - 0.28, Z_W1[0] + 0.30,
                 Z_W1[1] - 0.30, 0.12, 0.15, mats["Toy_glassl_Glow"])
    return ink


def diamond(face, tag, a, z, half, d_in, d_out, mat):
    """A lozenge plate on a facade — the one ornament the miniature keeps."""
    pts = [face_pt(face, a - half, d_in), face_pt(face, a, d_in),
           face_pt(face, a + half, d_in), face_pt(face, a, d_in)]
    verts = []
    quad = [(a - half, z), (a, z + half), (a + half, z), (a, z - half)]
    for d in (d_in, d_out):
        for aa, zz in quad:
            x, y = sw(*face_pt(face, aa, d))
            verts.append((x, y, zz))
    faces = [(3, 2, 1, 0), (4, 5, 6, 7)]
    for i in range(4):
        j = (i + 1) % 4
        faces.append((i, j, 4 + j, 4 + i))
    return new_mesh(tag, verts, faces, [mat])


def rusticated(tag, face, a0, a1, z0, z1, mats, courses=7, d=0.22):
    """A terracotta pier or quoin with its ashlar courses cut as thin proud
    strips — the trompe-l'oeil 'stone' that is really painted brick."""
    bevel(face_box(f"{tag}_body", face, a0, a1, z0, z1, -0.05, d, mats["Toy_sand"]),
          width=0.08)
    step = (z1 - z0) / courses
    for k in range(1, courses):
        face_box(f"{tag}_c{k}", face, a0 + 0.04, a1 - 0.04, z0 + k * step - 0.07,
                 z0 + k * step + 0.07, d - 0.10, d - 0.01, mats["Toy_stone"])


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    mats = materials()
    brick, rust, sand = mats["Toy_brick"], mats["Toy_rust"], mats["Toy_sand"]
    stone, steel, ink = mats["Toy_stone"], mats["Toy_steel"], mats["Toy_ink"]
    glass, roofd, gold = mats["Toy_glass"], mats["Toy_roofd"], mats["Toy_gold"]

    # ---- 1. the one-storey work-room block, over the whole wharf footprint --- #
    bevel(prism("low_body", RING, 0.0, Z_LOWBODY, brick, mat_caps=steel), width=0.14)
    bevel(box("low_deckA", 0.0, S_SLOT0, 0.0, W_MAIN, Z_LOWBODY, Z_LOW, brick,),
          width=0.10)
    bevel(prism("low_deckB", [(S_SLOT1, 0.0), (S_FRONT, 0.0), (S_FRONT, W_BUMP),
                              (S_BUMP, W_BUMP), (S_BUMP, W_MAIN), (S_SLOT1, W_MAIN)],
                Z_LOWBODY, Z_LOW, brick), width=0.10)
    for tag, obj in (("A", None),):
        pass
    # deck surfaces (the loader bakes material colour to vertex colour, so the
    # deck reads as its own material only if it is its own geometry)
    box("low_surfA", 0.30, S_SLOT0 - 0.30, 0.30, W_MAIN - 0.30, Z_LOW, Z_LOW + 0.05, steel)
    box("low_surfB", S_SLOT1 + 0.30, S_FRONT - 0.30, 0.30, W_BUMP - 0.30,
        Z_LOW, Z_LOW + 0.05, steel)
    # parapet + terracotta coping (the NRHP's 'artificial stone band' crowning
    # the original rear)
    bevel(band("low_par", RING, Z_LOW, Z_LOWPAR, -0.50, 0.06, brick), width=0.07)
    bevel(band("low_cap", RING, Z_LOWPAR, Z_LOWCAP, -0.60, 0.16, sand), width=0.05)
    # slot edges
    for k, s in ((0, S_SLOT0), (1, S_SLOT1)):
        d = -0.45 if k == 0 else 0.0
        bevel(box(f"slot_up{k}", s + d, s + d + 0.45, W_TILE, 41.0, Z_LOW, Z_LOW + 0.62,
                  brick), width=0.06)
        box(f"slot_cap{k}", s + d - 0.06, s + d + 0.51, W_TILE, 41.0,
            Z_LOW + 0.62, Z_LOW + 0.74, sand)
    box("slot_floor", S_SLOT0, S_SLOT1, W_TILE, 41.0, Z_LOWBODY, Z_LOWBODY + 0.06, glass)

    # ---- 2. the two-storey block behind the frontage ------------------------ #
    bevel(box("two_body", 0.0, S_FRONT, 0.0, W_TILE, 0.0, Z_CORN[0], brick), width=0.14)
    # the two-storey block behind the tile: a real deck at 9.80 inside its own
    # parapet, which is what the nadir imagery shows — not a solid top at 10.20
    mid_rect = [(S_MID[0], W_TILE), (S_MID[1], W_TILE), (S_MID[1], W_TWO),
                (S_MID[0], W_TWO)]
    bevel(prism("mid_body", mid_rect, 0.0, Z_MID, brick, mat_caps=stone), width=0.14)
    bevel(band("mid_par", mid_rect, Z_MID, Z_CORN[0] - 0.16, -0.42, 0.04, brick),
          width=0.07)
    bevel(band("mid_cap", mid_rect, Z_CORN[0] - 0.16, Z_CORN[0], -0.50, 0.12, sand),
          width=0.05)
    two_poly = [(0.0, 0.0), (S_FRONT, 0.0), (S_FRONT, W_TILE), (S_MID[1], W_TILE),
                (S_MID[1], W_TWO), (S_MID[0], W_TWO), (S_MID[0], W_TILE), (0.0, W_TILE)]
    bevel(band("two_corn", two_poly, Z_CORN[0], Z_CORN[1], -0.34, 0.72, ink), width=0.07)

    # granite plinth all the way round the two-storey block and the work room
    bevel(band("plinth", RING, 0.0, Z_BASE, -0.02, 0.20, steel), width=0.07)

    # ---- 3. the clay-tile hip roofs ----------------------------------------- #
    bevel(hip_roof("tile_front", -EAVE_OVER, S_FRONT + EAVE_OVER, -EAVE_OVER,
                   W_TILE + EAVE_OVER, Z_CORN[1], Z_RIDGE, "s", W_RIDGE, rust,
                   fascia=0.16), width=0.10)
    bevel(box("sew_body", S_WING, S_FRONT, W_TILE, W_BUMP, 0.0, Z_SEW, brick), width=0.13)
    bevel(band("sew_corn", [(S_WING, W_TILE), (S_FRONT, W_TILE), (S_FRONT, W_BUMP),
                            (S_WING, W_BUMP)], Z_SEW, Z_SEWC, -0.30, 0.62, ink),
          width=0.06)
    bevel(hip_roof("tile_sew", S_WING - EAVE_OVER, S_FRONT + EAVE_OVER, W_TILE,
                   W_BUMP + EAVE_OVER, Z_SEWC, Z_SEWR, "w", S_WRIDGE, rust,
                   fascia=0.16), width=0.09)

    # ---- 4. the Embarcadero elevation --------------------------------------- #
    for tag, a0, a1 in (("qL", 0.0, QUOIN), ("qR", mirror(QUOIN), S_FRONT)):
        rusticated(tag, "front", a0, a1, Z_BASE, Z_CORN[0], mats, courses=8, d=0.26)
    for tag, a0, a1 in (("eL", END0, END1), ("eR", mirror(END1), mirror(END0))):
        rusticated(tag, "front", a0, a1, Z_BASE, Z_CORN[0], mats, courses=8, d=0.20)
        c = (a0 + a1) / 2.0
        face_box(f"{tag}_rec", "front", c - DOOR_W / 2 - 0.26, c + DOOR_W / 2 + 0.26,
                 0.0, 4.16, 0.14, 0.22, stone)
        face_box(f"{tag}_door", "front", c - DOOR_W / 2, c + DOOR_W / 2, 0.0, 2.90,
                 0.22, 0.28, roofd)
        face_box(f"{tag}_tran", "front", c - DOOR_W / 2 + 0.12, c + DOOR_W / 2 - 0.12,
                 2.96, 3.96, 0.22, 0.28, glass)
        bevel(face_box(f"{tag}_lint", "front", c - DOOR_W / 2 - 0.52,
                       c + DOOR_W / 2 + 0.52, 4.22, 4.62, 0.14, 0.58, sand), width=0.06)
    for tag, a0, a1 in (("pL", PIER0, PIER1), ("pR", mirror(PIER1), mirror(PIER0))):
        rusticated(tag, "front", a0, a1, Z_BASE, Z_CORN[0], mats, courses=9, d=0.30)

    # brick fields: the two window bands, the string course, the diamond panels
    for bi, c in enumerate(BAYS):
        window_pair(f"f{bi}", "front", c, 2.30, 1.90, mats, lit=bi in LIT_BAYS)
    for di, c in enumerate(DIAMONDS):
        # a shallow ornamental brick panel with a terracotta lozenge in it — the
        # miniature's stand-in for the real elaborate patterned brickwork
        face_box(f"dia{di}p", "front", c - 0.92, c + 0.92, 7.30, 9.14, -0.03, 0.05, rust)
        diamond("front", f"dia{di}", c, 8.22, 0.52, 0.05, 0.13, sand)
    for tag, f0, f1 in (("A", FIELD_A[0], FIELD_A[1]), ("B", FIELD_B[0], FIELD_B[1])):
        bevel(face_box(f"str{tag}", "front", f0, f1, Z_STR[0], Z_STR[1], -0.04, 0.20,
                       sand), width=0.06)

    # the central pavilion: terracotta field, entrance, phoenix shield, flagstaff,
    # and the two carved shield panels on the second floor
    c0, c1 = CENTRE
    cm = (c0 + c1) / 2.0
    rusticated("cen", "front", c0, c1, Z_BASE, Z_CORN[0], mats, courses=9, d=0.24)
    face_box("cen_door", "front", cm - CENTRE_DOOR_W / 2, cm + CENTRE_DOOR_W / 2,
             0.0, 3.60, 0.22, 0.32, ink)
    face_box("cen_tran", "front", cm - CENTRE_DOOR_W / 2 + 0.10,
             cm + CENTRE_DOOR_W / 2 - 0.10, 3.66, 4.90, 0.22, 0.30, glass)
    # the hero: the grilled transom over the doors, and a low sill of light at
    # the doorway itself. Flat plates proud of the opaque glazing, never a shell.
    face_box("cen_tran_glow", "front", cm - 1.35, cm + 1.35, 3.70, 4.86, 0.31, 0.35,
             mats["Toy_gold_Glow"])
    face_box("cen_door_glow", "front", cm - 0.86, cm + 0.86, 0.55, 2.65, 0.33, 0.37,
             mats["Toy_gold_Glow"])
    bevel(face_box("cen_lint", "front", cm - 1.85, cm + 1.85, 4.96, 5.44, 0.20, 0.74,
                   sand), width=0.06)
    # the cast phoenix-and-shield over the doors, simplified to a chunky plaque
    bevel(face_box("cen_wing", "front", cm - 1.55, cm + 1.55, 5.94, 6.44, 0.24, 0.50,
                   sand), width=0.06)
    bevel(face_box("cen_shield", "front", cm - 0.55, cm + 0.55, 5.70, 6.80, 0.24, 0.62,
                   gold), width=0.07)
    # the flagstaff, angled down and out so the tile ridge stays the bbox top
    for k in range(7):
        t = k / 6.0
        face_box(f"flag{k}", "front", cm - 0.08 + 1.15 * t, cm + 0.08 + 1.15 * t,
                 7.10 - 0.52 * t, 7.26 - 0.52 * t, 0.42 + 2.35 * t, 0.58 + 2.35 * t, ink)
    face_box("flagcloth", "front", cm + 0.55, cm + 1.45, 6.30, 6.98, 1.65, 2.45, stone)
    for si, c in ((0, 23.00), (1, mirror(23.00))):
        bevel(face_box(f"shp{si}", "front", c - 1.20, c + 1.20, 7.45, 9.40, 0.24, 0.42,
                       stone), width=0.06)
        diamond("front", f"shpd{si}", c, 8.42, 0.72, 0.42, 0.52, gold)

    # ---- 5. the two flanks --------------------------------------------------- #
    for face, depth, quo in (("nw", W_TWO, True), ("se", W_BUMP, True)):
        rusticated(f"{face}q", face, 0.0, QUOIN, Z_BASE, Z_CORN[0], mats, courses=8,
                   d=0.24)
    # NW flank: the finished design returns for the two-storey depth, then drops
    for k, c in enumerate((5.0, 9.6, 14.2, 18.8, 23.4)):
        window_pair(f"nw{k}", "nw", c, 2.10, 1.75, mats)
    bevel(face_box("nw_str", "nw", QUOIN, W_TWO, Z_STR[0], Z_STR[1], -0.04, 0.18, sand),
          width=0.06)
    for k, c in enumerate((28.5, 32.2, 35.9)):
        face_box(f"nwl{k}", "nw", c - 1.05, c + 1.05, 2.20, 5.30, 0.02, 0.10, glass)
    face_box("nw_door", "nw", 30.6, 32.4, 0.0, 3.10, 0.02, 0.12, ink)
    # SE flank: front block, then the 1918 wing all the way to the bump-out
    for k, c in enumerate((5.0, 9.6, 14.2)):
        window_pair(f"se{k}", "se", c, 2.10, 1.75, mats)
    bevel(face_box("se_str", "se", QUOIN, W_TILE, Z_STR[0], Z_STR[1], -0.04, 0.18, sand),
          width=0.06)
    for k, c in enumerate((20.4, 25.0, 29.6, 34.2, 38.8, 43.4)):
        face_box(f"sew_g1{k}", "se", c - 1.10, c + 1.10, 2.10, 5.20, 0.02, 0.10, glass)
        face_box(f"sew_s1{k}", "se", c - 1.24, c + 1.24, 1.84, 2.04, 0.02, 0.18, sand)
        face_box(f"sew_g2{k}", "se", c - 0.95, c + 0.95, 6.90, 8.60, 0.02, 0.10, glass)
    bevel(face_box("sew_str", "se", W_TILE, W_BUMP, 5.90, 6.60, -0.04, 0.18, sand),
          width=0.06)

    # ---- 6. the bay (NE) side: work room rear, plain --------------------------- #
    for k, c in enumerate((4.0, 10.5, 17.0, 23.5, 30.0, 36.0)):
        face_box(f"rear_g{k}", "rear", c - 1.35, c + 1.35, 1.90, 4.40, 0.02, 0.10, glass)
    for k, c in enumerate((7.2, 20.0, 33.0)):
        bevel(face_box(f"rear_roll{k}", "rear", c - 1.55, c + 1.55, 0.0, 3.60, 0.02,
                       0.13, steel), width=0.05)
    for k, c in enumerate((42.5, 46.5)):
        face_box(f"bs_g{k}", "bumpside", c - 1.20, c + 1.20, 2.10, 5.20, 0.02, 0.10,
                 glass)
    for k, c in enumerate((42.0, 46.2)):
        face_box(f"be_g{k}", "bumpend", c - 1.20, c + 1.20, 2.10, 5.20, 0.02, 0.10,
                 glass)
    face_box("be_roll", "bumpend", 44.0, 47.0, 0.0, 3.40, 0.02, 0.12, steel)

    # ---- 7. the roofscape ------------------------------------------------------ #
    # three light-topped roof monitors on the darker NW quarter of the work room
    for k, w0 in enumerate((19.4, 25.2, 31.0)):
        bevel(box(f"mon{k}", 1.4, 7.9, w0, w0 + 2.40, Z_LOW + 0.05, Z_LOW + 1.28,
                  brick), width=0.10)
        bevel(box(f"mon{k}g", 1.7, 7.6, w0 - 0.06, w0 + 2.46, Z_LOW + 0.42,
                  Z_LOW + 1.02, glass), width=0.05, segments=1)
        bevel(box(f"mon{k}c", 1.2, 8.1, w0 - 0.22, w0 + 2.62, Z_LOW + 1.28,
                  Z_LOW + 1.52, stone), width=0.07)
    # mechanical scatter on the big work-room deck, none on the tile
    for k, (s0, w0, ss, ww, h) in enumerate((
            (12.0, 27.4, 1.10, 1.10, 0.95), (17.5, 29.6, 0.90, 0.90, 0.80),
            (23.0, 27.2, 1.20, 1.20, 1.05), (28.5, 30.2, 0.90, 0.90, 0.80),
            (14.5, 34.6, 1.05, 1.05, 0.90), (25.0, 35.2, 1.15, 1.15, 1.00),
            (32.0, 33.0, 0.95, 0.95, 0.85))):
        bevel(box(f"vent{k}", s0, s0 + ss, w0, w0 + ww, Z_LOW + 0.05, Z_LOW + 0.05 + h,
                  roofd), width=0.07)
    for k, (s0, s1, w0) in enumerate(((11.0, 33.0, 32.0), (13.0, 30.0, 37.0))):
        bevel(box(f"duct{k}", s0, s1, w0, w0 + 0.85, Z_LOW + 0.05, Z_LOW + 0.62, roofd),
              width=0.06)
    bevel(box("plant", 18.5, 26.5, 30.8, 33.2, Z_LOW + 0.05, Z_LOW + 1.45, steel),
          width=0.10)
    bevel(box("hatch", 33.0, 34.8, 28.0, 29.6, Z_LOW + 0.05, Z_LOW + 0.66, roofd),
          width=0.06)
    # the two vents the mid deck actually carries, and a stair bulkhead
    bevel(box("mid_bulk", 20.0, 24.0, W_TILE + 1.6, W_TILE + 4.2, Z_MID, Z_MID + 1.55,
              brick), width=0.10)
    bevel(box("mid_bulkc", 19.8, 24.2, W_TILE + 1.4, W_TILE + 4.4, Z_MID + 1.55,
              Z_MID + 1.74, stone), width=0.06)
    for k, (s0, w0) in enumerate(((12.0, W_TILE + 3.0), (31.5, W_TILE + 5.2))):
        bevel(box(f"midvent{k}", s0, s0 + 1.0, w0, w0 + 1.0, Z_MID, Z_MID + 0.78, roofd),
              width=0.06)
    return scene


def finish():
    for obj in [o for o in bpy.data.objects if o.type == "MESH"]:
        ensure_outward(obj)
    normalize_height(Z_RIDGE)


def normalize_height(target):
    """Land the export's bounding-box top exactly on the architectural height so
    the loader's targetHeightM / measuredHeight scale is 1.0. Bevelling the tile
    ridge shaves ~12 mm off it, so the model is scaled about z = 0 to put it
    back; min Z stays 0 and the correction is ~0.1%."""
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    top = max((o.matrix_world @ Vector(c))[2] for o in objs for c in o.bound_box)
    k = target / top
    for o in objs:
        me = o.data
        for v in me.vertices:
            v.co.z *= k
    print(f"[build] height normalization: top {top:.4f} -> {target} (x{k:.6f})")


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
    print("[build] anchor lon/lat: -122.3921505 37.7941368 (footprint AABB centre)")
    print("[build] Embarcadero front normal 234.0 deg true; NW 324.3; SE 144.3; rear 54.0")
    print(f"[build] eave {Z_CORN[1]}; ridge {Z_RIDGE}; mid deck {Z_MID}; low deck {Z_LOW}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    finish()
    report()

    blend = os.path.join(out, "ferry-station-post-office.blend")
    glb = os.path.join(out, "ferry-station-post-office.glb")
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
