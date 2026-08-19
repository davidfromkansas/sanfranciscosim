"""Deterministic Blender build of the SF-SIM miniature 326 Brannan Street.

    blender -b --python build_326_brannan.py -- [--out DIR]

Writes 326-brannan.blend and 326-brannan.glb next to this file (or into --out).

Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = DataSF parcel centroid (anchor lon -122.3928965,
lat 37.7815080), min Z = 0, shed parapet crest exactly 5.90 m.

326 Brannan is a SITE, not a building (see docs/asset-plans/326-brannan.md):
a 7.98 x 24.32 m infill slot whose front two thirds is the JAX Vineyards
outdoor "Wine Court" and whose rear ninth-of-a-metre-shy-of-ten metres is a
1959 one-storey commercial shed. Everything is authored in a lot-local (u, v)
frame — u runs along the Brannan frontage from the SW party line to the NE one,
v runs INTO the lot from the Brannan property line — and transformed to world
at the end. That frame comes straight off the surveyed parcel corners, so every
constant below is a measurement rather than a guess.

Survey (DataSF parcel 3775/012 + LiDAR footprints mblr SF3775012), in (u, v):

* lot          u [-3.99, +4.00]   v [0, 24.32]
* court        u [-3.86, +3.69]   v [1.00, 14.61]   LiDAR mode 0.14 m  (open)
* shed         u [-3.88, +3.00]   v [14.05, 23.66]  LiDAR median 5.66 m
* the shed is narrower than the lot on its NE flank, leaving a ~1.0 m side
  passage, and stops 0.66 m short of the rear property line. Both are in the
  survey and both are kept.

Design:

* the street elevation is not a building — it is a 2.80 m charcoal
  vertical-board gate and fence carrying five off-white wine-bottle
  silhouettes and one red JAX disc, the only saturated element on the asset;
* the court behind it is the composition: pale slab, raised terracotta
  planters down both sides, a fire table inside a built-in bench ring, loose
  tables, a dark canopy plate on four posts, vine mass on both party walls
  (densest on the SW, where the real ivy blankets 334 Brannan), and a
  multi-stem olive whose crown at 5.80 m sits deliberately 0.10 m UNDER the
  shed parapet so the parapet owns the bounding box;
* the shed is near-black painted CMU with a 12-pane glazed roll-up door on its
  court elevation and a designed flat roof (two mechanical boxes, a hatch);
* night state: catenary string lights are the hero, supported by the fire
  table burner, the roll-up door and the JAX disc. Four glow groups, every one
  a thin shell proud of an opaque surface — the app renders _Glow in a separate
  layer and a closed glow shell reads as stacked alpha in daylight.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- lot frame

# Surveyed parcel corners, app-local metres, recentred on the anchor and
# converted to Blender axes (+X east, +Y north). A and B are the Brannan
# frontage; the ring A -> D -> C -> B is CCW.
CORNER_A = (11.400, -5.811)   # east corner, on Brannan
CORNER_B = (5.740, -11.441)   # south corner, on Brannan
CORNER_C = (-11.410, 5.799)   # west corner, at the rear
CORNER_D = (-5.740, 11.429)   # north corner, at the rear

_FRONT_LEN = math.hypot(CORNER_A[0] - CORNER_B[0], CORNER_A[1] - CORNER_B[1])
E_U = ((CORNER_A[0] - CORNER_B[0]) / _FRONT_LEN, (CORNER_A[1] - CORNER_B[1]) / _FRONT_LEN)
E_V = (-E_U[1], E_U[0])
ORIGIN_UV = ((CORNER_A[0] + CORNER_B[0]) / 2.0, (CORNER_A[1] + CORNER_B[1]) / 2.0)
if ORIGIN_UV[0] * E_V[0] + ORIGIN_UV[1] * E_V[1] > 0:  # make +v point into the lot
    E_V = (-E_V[0], -E_V[1])

U_SW, U_NE = -3.99, 4.00       # party lines
V_FRONT, V_REAR = 0.0, 24.32   # Brannan property line -> rear property line

# ------------------------------------------------------------------ heights

Z_SLAB = 0.10          # court apron top
Z_GATE = 2.80          # gate / fence boards
Z_GATE_CAP = 2.92      # cap rail
Z_WALL = 2.70          # court side walls — a liner; the neighbours do the enclosing
Z_CANOPY0 = 3.44       # pergola beam soffit
Z_CANOPY1 = 3.72       # pergola slat top
Z_DECK = 5.66          # shed roof deck (LiDAR median over 252 cells)
Z_CREST = 5.90         # shed parapet crest = the bounding-box top
Z_OLIVE = 5.80         # olive crown crest, 0.10 m under the parapet by design

# The shed's surveyed quad in (u, v). Slightly skewed; kept as surveyed.
SHED = [(3.00, 14.05), (-3.86, 14.61), (-3.88, 23.66), (2.49, 23.65)]

PALETTE_HEX = {
    "Toy_charcoal": "34312e",   # gate boards, shed CMU — warm near-black
    "Toy_ink": "1f1d1c",        # frames, posts, furniture
    "Toy_cream": "e9e2d3",      # bottle silhouettes
    "Toy_coral": "d24f39",      # the JAX disc: the ONE saturated accent
    "Toy_stone": "cbc3b2",      # court slab
    "Toy_plaster": "c2b8a5",    # court side walls — a liner, not a facade
    "Toy_terra": "a9634a",      # raised planters
    "Toy_olive": "7f8d6b",      # olive foliage — silver-green, NOT mint
    "Toy_vine": "4e6b3d",       # wall vines and ground planting
    "Toy_bark": "6d6154",       # trunks and stems
    "Toy_glass": "3d5f85",      # roll-up door panes, day — graphical, not black
    "Toy_canopy": "6f736e",     # pergola panel — smoky, must never out-shout
                                # the gate, which is the one loud element
    "Toy_roofd": "6a6a66",      # shed roof membrane — light enough that the
                                # parapet ring and the roof kit both read
    "Toy_steel": "8f959b",      # mechanical boxes, hatch
    "Toy_glass_Glow": "f0d9a8",
    "Toy_bulb_Glow": "ffe6b0",
    "Toy_fire_Glow": "ff8a3d",
    "Toy_coral_Glow": "ef7a63",
}

NO_BEVEL = set()  # populated as tiny objects are created


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


# ---------------------------------------------------------------- transforms


def w(u, v):
    """Lot-local (u, v) -> world (x, y)."""
    return (
        ORIGIN_UV[0] + E_U[0] * u + E_V[0] * v,
        ORIGIN_UV[1] + E_U[1] * u + E_V[1] * v,
    )


def material(name):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    rgb = PALETTE[name]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = 0.2
    if name.endswith("_Glow") and "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 1.0
    mat.diffuse_color = (*rgb, 1.0)
    return mat


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


def prism_uv(name, poly_uv, z0, z1, mat, mat_caps=None):
    """Closed extrusion of a CCW (u, v) polygon into world space."""
    pts = [w(u, v) for u, v in poly_uv]
    if signed_area(pts) < 0:
        pts.reverse()
    n = len(pts)
    verts = [(x, y, z0) for x, y in pts] + [(x, y, z1) for x, y in pts]
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


def signed_area(pts):
    n = len(pts)
    return 0.5 * sum(
        pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n)
    )


def ubox(name, u0, u1, v0, v1, z0, z1, mat):
    """Closed box axis-aligned in the lot frame."""
    return prism_uv(name, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], z0, z1, mat)


def offset_polygon(poly, d):
    """Miter offset of a CCW polygon; positive d moves outward."""
    n = len(poly)
    normals = []
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        normals.append((dy / length, -dx / length))
    out = []
    for i in range(n):
        n1, n2 = normals[i - 1], normals[i]
        p = poly[i]
        det = n1[0] * n2[1] - n1[1] * n2[0]
        if abs(det) < 1e-6:
            out.append((p[0] + n2[0] * d, p[1] + n2[1] * d))
            continue
        c1 = p[0] * n1[0] + p[1] * n1[1] + d
        c2 = p[0] * n2[0] + p[1] * n2[1] + d
        out.append(((c1 * n2[1] - c2 * n1[1]) / det, (c2 * n1[0] - c1 * n2[0]) / det))
    return out


def ring_band_uv(name, poly_uv, z0, z1, off_in, off_out, mat):
    """Closed parapet-style band following a (u, v) footprint."""
    if signed_area(poly_uv) < 0:
        poly_uv = list(reversed(poly_uv))
    lo_in = offset_polygon(poly_uv, off_in)
    lo_out = offset_polygon(poly_uv, off_out)
    n = len(lo_in)
    verts = []
    for loop, z in ((lo_in, z0), (lo_out, z0), (lo_out, z1), (lo_in, z1)):
        verts.extend([(*w(u, v), z) for u, v in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * n, ((k + 1) % 4) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def line_panel(name, p0, p1, s0, s1, d0, d1, z0, z1, mat):
    """Closed box lying along the (u, v) line p0->p1.

    s is the parameter along the line (metres from p0), d is the offset along
    the line's left normal. Used for the shed's skewed court elevation, where a
    lot-frame box would poke through the wall at one end.
    """
    du, dv = p1[0] - p0[0], p1[1] - p0[1]
    length = math.hypot(du, dv)
    t = (du / length, dv / length)
    nrm = (-t[1], t[0])
    quad = []
    for s, d in ((s0, d0), (s1, d0), (s1, d1), (s0, d1)):
        quad.append((p0[0] + t[0] * s + nrm[0] * d, p0[1] + t[1] * s + nrm[1] * d))
    return prism_uv(name, quad, z0, z1, mat)


def blob(name, cu, cv, cz, ru, rv, rz, mat, subdiv=1):
    """Low-poly rounded mass — foliage, planting, vine clumps.

    The lot-frame ellipsoid transform is baked straight into the vertices so
    the exported object carries an identity transform (contract: applied
    transforms, no negative scales).
    """
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    cx, cy = w(cu, cv)
    for vert in bm.verts:
        lu, lv, lz = vert.co.x * ru, vert.co.y * rv, vert.co.z * rz
        vert.co = Vector(
            (
                cx + E_U[0] * lu + E_V[0] * lv,
                cy + E_U[1] * lu + E_V[1] * lv,
                cz + lz,
            )
        )
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.append(mat)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    mesh.shade_flat()
    NO_BEVEL.add(obj.name)
    return obj


def bevel(obj, width=0.10, segments=2):
    """Miniature edge softening (style bible s.4), clamped for thin panels."""
    thin = min((d for d in obj.dimensions if d > 1e-6), default=width)
    offset = min(width, thin * 0.30)
    if offset < 1e-3:
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


# ------------------------------------------------------------------- pieces


def build_slab():
    M = material("Toy_stone")
    # Main court apron, plus the surveyed side passage down the shed's NE flank.
    ubox("CourtSlab", -3.84, 3.84, 0.35, 14.35, 0.0, Z_SLAB, M)
    ubox("SidePassage", 2.55, 3.84, 14.35, 23.60, 0.0, Z_SLAB, M)
    # Threshold band at the shed door, a shade lower so the plan reads in two parts.
    ubox("Threshold", -3.10, 2.40, 13.55, 14.35, 0.0, Z_SLAB - 0.02, material("Toy_plaster"))


def build_gate():
    charcoal = material("Toy_charcoal")
    ink = material("Toy_ink")
    cream = material("Toy_cream")
    coral = material("Toy_coral")

    ubox("GateWall", U_SW, U_NE, 0.15, 0.37, 0.0, Z_GATE, charcoal)
    ubox("GateCap", U_SW - 0.04, U_NE + 0.04, 0.11, 0.41, Z_GATE, Z_GATE_CAP, ink)

    # Solid double-leaf gate at the SW end, set slightly proud with a reveal.
    ubox("GateLeaf", -3.93, -1.55, 0.10, 0.16, 0.12, Z_GATE - 0.06, ink)
    ubox("GatePull", -1.78, -1.72, 0.05, 0.11, 1.00, 1.80, material("Toy_steel"))
    NO_BEVEL.add("GatePull")

    # Five wine-bottle silhouettes on the fence panels: body + shoulder + neck.
    for i, uc in enumerate((-1.05, -0.10, 0.85, 1.80, 3.05)):
        base = 0.55 + (0.12 if i % 2 else 0.0)
        ubox(f"Bottle{i}_body", uc - 0.24, uc + 0.24, 0.11, 0.15, base, base + 0.86, cream)
        ubox(f"Bottle{i}_shoulder", uc - 0.16, uc + 0.16, 0.11, 0.15, base + 0.86, base + 1.06, cream)
        ubox(f"Bottle{i}_neck", uc - 0.08, uc + 0.08, 0.11, 0.15, base + 1.06, base + 1.62, cream)
        for part in ("body", "shoulder", "neck"):
            NO_BEVEL.add(f"Bottle{i}_{part}")

    # The JAX disc — a 16-gon, the single saturated element on the asset.
    disc = [
        (2.05 + 0.42 * math.cos(k * math.pi / 8), 0.0)
        for k in range(16)
    ]
    ring = []
    for k in range(16):
        a = k * math.pi / 8
        ring.append((2.05 + 0.42 * math.cos(a), 0.42 * math.sin(a)))
    verts, faces = [], []
    for d, zoff in ((0.15, 0.0), (0.11, 0.0)):
        for uu, zz in ring:
            x, y = w(uu, d)
            verts.append((x, y, 1.90 + zz))
    for i in range(16):
        j = (i + 1) % 16
        faces.append((i, j, 16 + j, 16 + i))
    faces.append(tuple(range(15, -1, -1)))
    faces.append(tuple(range(16, 32)))
    disc_obj = new_mesh("GateDisc", verts, faces, [coral])
    NO_BEVEL.add(disc_obj.name)

    # Night: a thin glow shell proud of the opaque disc face. Never a closed shell.
    gverts, gfaces = [], []
    for d in (0.105, 0.088):
        for uu, zz in ring:
            x, y = w(uu * 1.0, d)
            gverts.append((x, y, 1.90 + zz * 0.94))
    for i in range(16):
        j = (i + 1) % 16
        gfaces.append((i, j, 16 + j, 16 + i))
    gfaces.append(tuple(range(15, -1, -1)))
    gfaces.append(tuple(range(16, 32)))
    g = new_mesh("GateDisc_Glow", gverts, gfaces, [material("Toy_coral_Glow")])
    NO_BEVEL.add(g.name)


def build_court_walls():
    plaster = material("Toy_plaster")
    ubox("WallNE", 3.72, 3.96, 0.37, 14.35, 0.0, Z_WALL, plaster)
    ubox("WallSW", -3.96, -3.72, 0.37, 14.35, 0.0, Z_WALL, plaster)
    ubox("WallRear", -3.60, 3.60, 23.94, 24.14, 0.0, 2.20, plaster)


def build_vines():
    vine = material("Toy_vine")
    # Densest on the SW wall — the real ivy blankets 334 Brannan's party wall.
    # Crests deliberately sit ABOVE Z_WALL: on the real site the ivy tops the
    # party wall, and it is the only way green reads from outside the court.
    sw = [(1.5, 2.55, 1.15, 0.80), (3.9, 2.80, 1.30, 0.95), (6.4, 2.50, 1.10, 0.78),
          (8.8, 2.90, 1.35, 0.98), (11.2, 2.65, 1.20, 0.86), (13.4, 2.45, 1.00, 0.72)]
    for i, (v, z, rv, rz) in enumerate(sw):
        blob(f"VineSW{i}", -3.55, v, z, 0.30, rv, rz, vine)
    ne = [(2.6, 2.50, 1.05, 0.72), (5.9, 2.70, 1.20, 0.88), (9.6, 2.45, 1.00, 0.68),
          (12.9, 2.60, 1.10, 0.78)]
    for i, (v, z, rv, rz) in enumerate(ne):
        blob(f"VineNE{i}", 3.55, v, z, 0.28, rv, rz, vine)
    # Two vine columns on the gate's inner face.
    # Overtopping the gate: from Brannan the only thing above the fence is foliage.
    blob("VineGateA", -3.05, 0.66, 2.05, 0.55, 0.30, 1.25, vine)
    blob("VineGateB", 2.55, 0.66, 1.95, 0.50, 0.28, 1.10, vine)


def build_planters():
    terra = material("Toy_terra")
    vine = material("Toy_vine")
    spec = [
        (-3.05, 1.70, 1.15, 0.52),
        (-3.05, 6.10, 1.55, 0.46),
        (-3.05, 11.40, 1.05, 0.50),
        (3.00, 3.60, 1.35, 0.44),
        (3.00, 8.90, 1.20, 0.54),
        (3.00, 12.70, 0.95, 0.42),
    ]
    for i, (u, v, half, h) in enumerate(spec):
        ubox(f"Planter{i}", u - 0.55, u + 0.55, v - half, v + half, 0.05, Z_SLAB + h, terra)
        blob(f"Planting{i}", u, v, Z_SLAB + h + 0.12, 0.42, half * 0.78, 0.26, vine)


def build_olive():
    """Multi-stem olive in a raised planter, crown crest at Z_OLIVE."""
    bark = material("Toy_bark")
    terra = material("Toy_terra")
    olive = material("Toy_olive")
    CU, CV = 2.00, 9.55
    ubox("OlivePlanter", CU - 1.05, CU + 1.05, CV - 1.05, CV + 1.05, 0.05, Z_SLAB + 0.45, terra)
    stems = [(0.0, 0.0, 0.20, 2.30), (-0.34, 0.22, 0.15, 1.95), (0.30, -0.26, 0.14, 1.80)]
    for i, (du, dv, r, top) in enumerate(stems):
        ubox(
            f"OliveStem{i}",
            CU + du - r, CU + du + r, CV + dv - r, CV + dv + r,
            Z_SLAB + 0.30, Z_SLAB + 0.45 + top, bark,
        )
    # Crown: three overlapping masses, the tallest topping out at Z_OLIVE.
    # Three separated masses rather than one dome: an olive is an open,
    # irregular crown, and a single smooth blob reads as broccoli from the
    # app's downward camera (first render, see REPORT.md).
    crown = [
        (0.00, 0.15, 1.55, 1.30, 4.86, 0.94),
        (-1.30, -0.70, 1.20, 1.05, 4.10, 0.78),
        (1.05, -0.95, 1.05, 0.95, 4.35, 0.66),
        (-0.55, 1.35, 1.00, 0.85, 4.20, 0.62),
    ]
    for i, (du, dv, ru, rv, cz, rz) in enumerate(crown):
        rz = (Z_OLIVE - cz) if i == 0 else rz
        blob(f"OliveCrown{i}", CU + du, CV + dv, cz, ru, rv, rz, olive, subdiv=2)


def build_canopy():
    """Slatted pergola with a translucent panel over its NE half.

    The real structure is a panelled metal canopy. Modelled solid it becomes a
    black rectangle over a third of the court in the app's downward view — the
    one view this asset exists for — so it is built as an open slat frame with
    the panel kept to the half that shelters the tables. The departure is
    recorded in REPORT.md.
    """
    ink = material("Toy_ink")
    glazing = material("Toy_canopy")
    V0, V1 = 3.05, 7.25
    V_SPLIT = 4.75
    for i, u in enumerate((-3.05, 3.05)):
        ubox(f"PergolaBeam{i}", u - 0.09, u + 0.09, V0, V1, Z_CANOPY0, Z_CANOPY1, ink)
        NO_BEVEL.add(f"PergolaBeam{i}")
    # The panel goes UNDER the slats and stops on a cross beam, so the split
    # reads as a designed edge rather than a modelling accident. Its tone sits
    # close to the court slab: bright metal here out-shouted the gate, which is
    # the only element allowed to be loud (second render, see REPORT.md).
    ubox("PergolaSplitBeam", -3.05, 3.05, V_SPLIT - 0.07, V_SPLIT + 0.07,
         Z_CANOPY0, Z_CANOPY1, ink)
    NO_BEVEL.add("PergolaSplitBeam")
    ubox("PergolaPanel", -2.98, 2.98, V0 + 0.09, V_SPLIT - 0.07,
         Z_CANOPY1 - 0.13, Z_CANOPY1 - 0.09, glazing)
    NO_BEVEL.add("PergolaPanel")
    n = 5
    for k in range(n + 1):
        v = V0 + (V1 - V0) * k / n
        ubox(f"PergolaSlat{k}", -3.14, 3.14, v - 0.045, v + 0.045,
             Z_CANOPY1 - 0.08, Z_CANOPY1 + 0.02, ink)
        NO_BEVEL.add(f"PergolaSlat{k}")
    for i, (u, v) in enumerate(((-3.05, V0 + 0.20), (3.05, V0 + 0.20),
                                (-3.05, V1 - 0.20), (3.05, V1 - 0.20))):
        ubox(f"CanopyPost{i}", u - 0.08, u + 0.08, v - 0.08, v + 0.08, Z_SLAB, Z_CANOPY0, ink)
        NO_BEVEL.add(f"CanopyPost{i}")


def build_fire_and_furniture():
    ink = material("Toy_ink")
    charcoal = material("Toy_charcoal")
    # Fire table inside an L of built-in bench.
    ubox("FireTable", -0.75, 0.75, 5.05, 5.95, Z_SLAB, Z_SLAB + 0.42, charcoal)
    ubox("FireBurner", -0.52, 0.52, 5.25, 5.75, Z_SLAB + 0.42, Z_SLAB + 0.45, ink)
    NO_BEVEL.add("FireBurner")
    ubox("FireGlow", -0.46, 0.46, 5.30, 5.70, Z_SLAB + 0.45, Z_SLAB + 0.49, material("Toy_fire_Glow"))
    NO_BEVEL.add("FireGlow")
    ubox("BenchA", -3.05, -1.35, 4.35, 4.95, Z_SLAB, Z_SLAB + 0.44, charcoal)
    ubox("BenchB", -3.05, -2.45, 4.95, 6.75, Z_SLAB, Z_SLAB + 0.44, charcoal)
    ubox("BenchC", 1.30, 2.95, 6.05, 6.65, Z_SLAB, Z_SLAB + 0.44, charcoal)
    # Loose tables, deliberately off-grid.
    tables = [(-1.75, 2.05), (1.90, 2.55), (-1.15, 12.35), (1.55, 13.10)]
    for i, (u, v) in enumerate(tables):
        ubox(f"Table{i}", u - 0.42, u + 0.42, v - 0.42, v + 0.42, Z_SLAB + 0.62, Z_SLAB + 0.68, charcoal)
        ubox(f"TableLeg{i}", u - 0.07, u + 0.07, v - 0.07, v + 0.07, Z_SLAB, Z_SLAB + 0.62, ink)
        NO_BEVEL.add(f"TableLeg{i}")
        for k, (du, dv) in enumerate(((-0.70, 0.05), (0.70, -0.05))):
            ubox(f"Chair{i}_{k}", u + du - 0.18, u + du + 0.18, v + dv - 0.18, v + dv + 0.18,
                 Z_SLAB, Z_SLAB + 0.42, ink)
            NO_BEVEL.add(f"Chair{i}_{k}")


def build_string_lights():
    """Two catenaries between the court walls; opaque cord, separate beads."""
    ink = material("Toy_ink")
    bulb = material("Toy_bulb_Glow")
    for c, v_at in enumerate((2.10, 11.60)):
        segs = 6
        sag_top, sag_mid = 3.05, 2.62
        pts = []
        for k in range(segs + 1):
            t = k / segs
            u = U_SW + 0.15 + (U_NE - U_SW - 0.30) * t
            z = sag_top - (sag_top - sag_mid) * (1.0 - (2.0 * t - 1.0) ** 2)
            pts.append((u, z))
        verts, faces = [], []
        r = 0.025
        for k, (u, z) in enumerate(pts):
            x, y = w(u, v_at)
            dx, dy = E_V[0] * r, E_V[1] * r
            verts += [
                (x - dx, y - dy, z - r), (x + dx, y + dy, z - r),
                (x + dx, y + dy, z + r), (x - dx, y - dy, z + r),
            ]
        for k in range(segs):
            a, b = 4 * k, 4 * (k + 1)
            for i in range(4):
                j = (i + 1) % 4
                faces.append((a + i, a + j, b + j, b + i))
        faces.append((3, 2, 1, 0))
        faces.append((4 * segs, 4 * segs + 1, 4 * segs + 2, 4 * segs + 3))
        cord = new_mesh(f"Cord{c}", verts, faces, [ink])
        NO_BEVEL.add(cord.name)
        # Each bead is an OPAQUE bulb with a thin glow shell proud of it. A bead
        # authored entirely in a _Glow material would be a primary surface in
        # the app's separate unlit layer and read as ~23% alpha in daylight —
        # i.e. see-through bulbs by day (see AGENTS/style notes on _Glow).
        for k in range(12):
            t = (k + 0.5) / 12
            u = U_SW + 0.15 + (U_NE - U_SW - 0.30) * t
            z = sag_top - (sag_top - sag_mid) * (1.0 - (2.0 * t - 1.0) ** 2)
            b = ubox(f"Bulb{c}_{k}", u - 0.050, u + 0.050, v_at - 0.050, v_at + 0.050,
                     z - 0.112, z - 0.028, material("Toy_cream"))
            NO_BEVEL.add(b.name)
            g = ubox(f"Bulb{c}_{k}_Glow", u - 0.062, u + 0.062, v_at - 0.062, v_at + 0.062,
                     z - 0.124, z - 0.016, bulb)
            NO_BEVEL.add(g.name)


def build_shed():
    charcoal = material("Toy_charcoal")
    ink = material("Toy_ink")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")

    prism_uv("ShedBody", SHED, 0.0, Z_DECK, charcoal, mat_caps=roofd)
    ring_band_uv("ShedParapet", SHED, Z_DECK, Z_CREST, -0.30, 0.0, charcoal)

    # Court elevation: a 12-pane glazed roll-up door, recessed into the wall.
    p0, p1 = SHED[0], SHED[1]          # (3.00, 14.05) -> (-3.86, 14.61)
    span = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    s_mid = span * 0.46
    half = 2.10
    # DEPTH ORDER MATTERS HERE and got it wrong twice. +d moves out of the wall
    # into the court, so the stack from back to front must be:
    #   reveal (dark backing, recessed)  <  panes  <  pane glow shells
    # and the surround must be a FRAME of four bars, not a slab over the
    # opening — a slab at any depth either hides the panes or is hidden by them.
    Z0 = Z_SLAB + 0.10
    Z1 = Z_SLAB + 3.58
    s_lo, s_hi = s_mid - half, s_mid + half
    line_panel("DoorReveal", p0, p1, s_lo - 0.04, s_hi + 0.04,
               -0.14, 0.02, Z0 - 0.04, Z1 + 0.04, ink)
    for tag, sa, sb, za, zb in (
        ("Head", s_lo - 0.16, s_hi + 0.16, Z1, Z1 + 0.16),
        ("Sill", s_lo - 0.16, s_hi + 0.16, Z0 - 0.14, Z0),
        ("JambA", s_lo - 0.16, s_lo, Z0, Z1),
        ("JambB", s_hi, s_hi + 0.16, Z0, Z1),
    ):
        line_panel(f"DoorFrame{tag}", p0, p1, sa, sb, 0.02, 0.20, za, zb,
                   material("Toy_steel"))
        NO_BEVEL.add(f"DoorFrame{tag}")
    cols, rows = 4, 3
    pw = (2 * half) / cols
    ph = (Z1 - Z0) / rows
    for r in range(rows):
        for c in range(cols):
            s0 = s_lo + c * pw + 0.05
            s1 = s_lo + (c + 1) * pw - 0.05
            z0 = Z0 + r * ph + 0.05
            z1 = Z0 + (r + 1) * ph - 0.05
            line_panel(f"Pane{r}{c}", p0, p1, s0, s1, 0.02, 0.14, z0, z1,
                       material("Toy_glass"))
            NO_BEVEL.add(f"Pane{r}{c}")
            line_panel(f"Pane{r}{c}_Glow", p0, p1, s0 + 0.03, s1 - 0.03,
                       0.14, 0.17, z0 + 0.03, z1 - 0.03, material("Toy_glass_Glow"))
            NO_BEVEL.add(f"Pane{r}{c}_Glow")

    # Designed roof — the camera looks down and this is the one built roof here.
    # Nothing on the roof is allowed above Z_CREST: the parapet owns the
    # bounding box, and this roof has never been photographed — inventing a
    # mechanical unit tall enough to become the crest would rescale the whole
    # asset off an unobserved feature (see the plan's 2.15).
    # One grouped kit, all of it in the same light steel, on a light membrane.
    # Earlier passes tried a dark housekeeping pad and dark hatches: on a 6.9 m
    # roof seen from directly above, any dark rectangle reads as a HOLE rather
    # than as equipment (third render, see REPORT.md).
    ubox("RoofCurb", -2.85, -0.35, 16.05, 18.95, Z_DECK, Z_DECK + 0.08, roofd)
    ubox("RoofMechA", -2.55, -1.40, 16.40, 17.90, Z_DECK + 0.08, Z_CREST - 0.02, steel)
    ubox("RoofMechB", -1.15, -0.60, 16.55, 17.60, Z_DECK + 0.08, Z_CREST - 0.34, steel)
    # Z_DECK + 0.08 == Z_CREST - 0.16 exactly, so an earlier pass gave this box
    # zero height and eight degenerate triangles. Keep the two ends apart.
    ubox("RoofDuct", -2.30, -0.60, 18.10, 18.55, Z_DECK + 0.08, Z_CREST - 0.06, steel)
    NO_BEVEL.add("RoofDuct")
    ubox("RoofHatch", 0.95, 1.90, 20.45, 21.40, Z_DECK, Z_DECK + 0.18, steel)
    ubox("RoofVent", -2.90, -2.55, 22.10, 22.45, Z_DECK, Z_CREST - 0.05, steel)
    NO_BEVEL.add("RoofVent")


# --------------------------------------------------------------------- build


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    build_slab()
    build_gate()
    build_court_walls()
    build_planters()
    build_vines()
    build_olive()
    build_canopy()
    build_fire_and_furniture()
    build_string_lights()
    build_shed()

    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name in NO_BEVEL:
            continue
        bevel(obj, width=0.10, segments=2)
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
            p = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], p[i])
                mx[i] = max(mx[i], p[i])
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    print("[build] anchor lon/lat: -122.3928965 37.7815080 (DataSF parcel centroid)")
    print("[build] Brannan frontage heading: 135.15 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "326-brannan.blend")
    glb = os.path.join(out, "326-brannan.glb")
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
