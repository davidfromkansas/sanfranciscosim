"""Deterministic Blender build of the SF-SIM miniature 49 Zoe Street.

    blender -b --python build_49_zoe.py -- [--out DIR]

Writes 49-zoe.blend and 49-zoe.glb next to this file (or into --out). Geometry
is authored directly in world space in metres, Z up, +X east, +Y north, so the
model drops into the city at its real-world heading — the loader applies no
rotation. Origin = footprint centroid (anchor lon -122.3960338, lat 37.7800764),
min Z = 0, roof-penthouse crest exactly 17.00 m.

Design (see REFERENCE.md and docs/asset-plans/49-zoe.md for the sources):

* the measured DataSF LiDAR footprint (mblr SF3776128) regularised to a clean
  rectangle 28.24 x 19.78 m on the 45 deg SoMa grid — every one of the survey's
  eleven vertices lies within 0.09 m of it, so the extra points are digitising
  noise, not corners;
* a 16-unit ARTIST LIVE/WORK building of 1996-97, re-clad in 2011-13. What you
  see is the 2013 rainscreen, not the 1997 exterior: an irregular VERTICAL
  STRIPE facade in five near-neutral tones, running full height from the base
  shelf to the parapet, with the windows punched through it. Nothing else in
  the scene has this, and it is the whole identity of the asset;
* the DOUBLE-HEIGHT LOFT RHYTHM: two tiers, not four floors. Each tier is one
  unit — a floor-to-ceiling window with a horizontal-slat juliet rail, a narrow
  spandrel, then the mezzanine window above. Four bays wide. The assessor roll
  proves the arrangement: eight units per tier, their areas repeating exactly
  (694, 775, 860, 937, 832, 987, 900, 693 sq ft) on lots 128-135 and again on
  136-143 — four fronting Zoe, four to the rear;
* a SPLIT-FACE CMU GARAGE BASE, 2.95 m, set 0.35 m back on the Zoe elevation so
  the panel wall above hangs over it in its own shadow line, carrying five grey
  roll-up doors and a recessed pedestrian entry under the galvanised steel
  awning of permit 9704456 (March 1997);
* exactly ONE street-visible elevation. The NW face is a party wall with 33-35
  Zoe (10.8-11.9 m, so our top ~2.5 m shows); the NE face looks into a 2.4 m
  light gap; the SE face stands open over a surface parking lot and carries the
  fire escape of permit 9621922. Detail is spent on Zoe and on the roof;
* a DESIGNED ROOF, which is half the asset on a building the aerial camera
  passes over constantly: a pale grey membrane inside a white coping ring, a
  central spine of three staggered glazed monitors lighting the internal
  circulation, a skylight scatter denser on the Zoe half, the stair/elevator
  penthouse that sets the 17.00 m crest at the SE end, and the common roof deck
  the sale listings document at the NW end;
* night state: the MONITOR SPINE lit end to end as the hero — the circulation of
  a 16-unit building is on all night and three glowing ridges down a dark roof
  is an image no other asset in this district gives the aerial camera — plus a
  deliberately uneven scatter of six lit loft windows and a warm strip under the
  entry awning. Glow surfaces are thin shells proud of the opaque geometry (the
  app renders _Glow in a separate layer that is ~12% alpha per layer by day —
  never author a primary surface as glow).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF footprint SF3776128, projected with the app's tangent projection,
# recentred on the footprint centroid and regularised to a rectangle.
# CCW, so outward normal = (t.y, -t.x).
FOOTPRINT = [
    (-16.9551, 3.1183),    # north corner  — Zoe frontage at the party wall
    (2.8638, -16.9999),    # south corner  — Zoe frontage at the parking lot
    (16.9551, -3.1183),    # east corner   — rear at the parking lot
    (-2.8638, 16.9999),    # west corner   — rear at the party wall
]

EDGE_ZOE = 0   # 28.24 m, faces SW 225.4 deg — Zoe Street, the only street face
EDGE_SE = 1    # 19.78 m, faces SE 135.4 deg — open over the parking lot
EDGE_NE = 2    # 28.24 m, faces NE  45.4 deg — 2.4 m light gap, near-blind
EDGE_NW = 3    # 19.78 m, faces NW 315.4 deg — party wall with 33-35 Zoe

LEN_ZOE = 28.241
LEN_SE = 19.780

Z_BASE = 2.95        # top of the CMU base / underside of the oversailing wall
Z_DECK = 13.60       # roof deck
Z_PARAPET = 14.40    # parapet crest (LiDAR median 14.42)
Z_CREST = 17.00      # penthouse top = LiDAR max 16.99 -> the bbox top

BASE_RECESS = 0.35   # the CMU base steps back this far on Zoe only
PARAPET_T = 0.30

# Loft tiers, measured off a metric rectification of Street View pano
# c2ZLvpFONJnFRVJgvl9OMw (rms 0.35 m). Each tier is ONE double-height unit.
TIERS = (
    # (main glazing, juliet rail, spandrel, mezzanine glazing)
    ((3.10, 5.55), (3.35, 4.30), (5.55, 5.90), (5.90, 7.80)),
    ((8.40, 10.70), (8.55, 9.50), (10.70, 11.00), (11.00, 12.50)),
)

BAY_N = 4
BAY_PITCH = LEN_ZOE / BAY_N          # 7.060 m
BAY_U = [BAY_PITCH * (i + 0.5) for i in range(BAY_N)]
WIN_W = 3.20

SKIN = 0.10

# Five roll-up doors and one pedestrian entry, read off the rectified elevation.
# u runs along the Zoe base from the party-wall corner.
DOORS = [(1.90, 5.10), (9.30, 12.50), (12.95, 16.15), (19.40, 22.60), (23.05, 26.25)]
ENTRY_U0, ENTRY_U1 = 26.70, 28.20

# The stripe cladding: irregular full-height panel bands. Widths are relative
# and normalised to the frontage, so the rhythm is fixed but the sum is exact.
# No two adjacent bands share a tone and no group of four repeats.
STRIPE_W = [1.30, 0.70, 1.85, 1.00, 1.55, 0.60, 2.05, 1.15, 0.85, 1.90, 1.35, 0.65,
            1.75, 1.05, 1.60, 1.20, 0.80, 1.95, 1.10, 0.70, 1.50, 0.95, 1.65]
STRIPE_TONE = [3, 5, 0, 2, 4, 3, 5, 2, 1, 4, 0, 3, 5, 2, 4, 0, 3, 5, 2, 4, 3, 0, 5]
STRIPE_TONES = ["Toy_white", "Toy_trim", "Toy_sand", "Toy_stone",
                "Toy_verdigris", "Toy_steel"]
STRIPE_PROUD = 0.18
STRIPE_FLUSH = 0.02

PALETTE_HEX = {
    "Toy_white": "f7f4ec",      # lightest stripe, coping, frames, kerbs, penthouse
    "Toy_trim": "f3efe6",       # second-lightest stripe (used once — see the plan)
    "Toy_sand": "ece4d4",       # warm pale stripe + the three non-street walls
    "Toy_stone": "d9d2c2",      # split-face CMU base, roof-deck paving, reveals
    "Toy_verdigris": "9fb8a8",  # the one stripe tone with any hue in it
    "Toy_steel": "9aa0a6",      # blue-grey stripe, roof membrane, doors, rails
    "Toy_glass": "2a4d73",      # loft glazing and the punched side windows
    "Toy_glassl": "6f95b8",     # monitor glazing and skylight domes
    "Toy_ink": "3a3530",        # fire escape, doors, reveals, louvres, hatch
    # Glow colours ARE the lit appearance — the app draws _Glow unlit at the
    # material's own base colour, so a night window that glows in its own dark
    # navy reads as a hole.
    "Toy_glass_Glow": "6f95b8",
    "Toy_glassl_Glow": "8fb4d8",
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


def poly_edge(i, poly=None):
    """Edge i of `poly`: (origin, length, tangent unit, outward normal)."""
    poly = FOOTPRINT if poly is None else poly
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def offset_polygon_per_edge(poly, ds):
    """Miter offset with a separate distance per edge (positive = outward)."""
    npts = len(poly)
    normals = [poly_edge(i, poly)[3] for i in range(npts)]
    out = []
    for i in range(npts):
        n1, n2 = normals[i - 1], normals[i]
        d1, d2 = ds[i - 1], ds[i]
        v = poly[i]
        det = n1[0] * n2[1] - n1[1] * n2[0]
        if abs(det) < 1e-6:
            out.append((v[0] + n2[0] * d2, v[1] + n2[1] * d2))
            continue
        c1 = v[0] * n1[0] + v[1] * n1[1] + d1
        c2 = v[0] * n2[0] + v[1] * n2[1] + d2
        out.append(((c1 * n2[1] - c2 * n1[1]) / det, (c2 * n1[0] - c1 * n2[0]) / det))
    return out


def offset_polygon(poly, d):
    return offset_polygon_per_edge(poly, [d] * len(poly))


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


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


def bevel(obj, width=0.12, segments=2):
    """Miniature-style edge softening (style bible s.4).

    Width is capped at a third of the object's thinnest dimension: the applied
    panels here are 60-130 mm thick and a flat 0.12 m bevel on those relies
    entirely on clamp_overlap, which collapses opposing profiles into zero-area
    slivers whose averaged vertex normal is zero — which fails the contract
    validator once gltfpack re-emits the stored normals.
    """
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
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-3)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-3, edges=list(bm.edges))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def prism(name, poly, z0, z1, mat, mat_caps=None):
    """Closed extrusion of a CCW polygon (walls + both caps)."""
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


def ring_band(name, poly, z0, z1, off_in, off_out, mat):
    """Closed band following a footprint: 4 loops, quads between."""
    lo_in = offset_polygon(poly, off_in)
    lo_out = offset_polygon(poly, off_out)
    npts = len(lo_in)
    verts = []
    for loop, z in ((lo_in, z0), (lo_out, z0), (lo_out, z1), (lo_in, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * npts, ((k + 1) % 4) * npts
        for i in range(npts):
            j = (i + 1) % npts
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def face_panel(name, edge, u_centre, profile, d0, d1, mat, poly=None):
    """Closed prism of a (u, z) profile lying in the plane of wall `edge`,
    extruded outward from offset d0 to d1 along that wall's normal."""
    a, _length, t, n = poly_edge(edge, poly)
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


def roof_uv(u, v):
    """Roof-grid coordinates: u runs along the Zoe edge from its NORTH-WEST
    corner (so u=0 is the party wall, u=28.24 the parking lot), v runs INTO the
    block against the Zoe outward normal."""
    origin, _l, t, n = poly_edge(EDGE_ZOE)
    return (origin[0] + t[0] * u - n[0] * v, origin[1] + t[1] * u - n[1] * v)


def roof_yaw():
    _o, _l, t, _n = poly_edge(EDGE_ZOE)
    return math.atan2(t[1], t[0])


def roof_box(name, u, v, z0, z1, su, sv, mat):
    cx, cy = roof_uv(u, v)
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=roof_yaw())


def roof_cylinder(name, u, v, z0, z1, radius, mat, segments=10):
    cx, cy = roof_uv(u, v)
    ring = [
        (cx + radius * math.cos(2 * math.pi * k / segments),
         cy + radius * math.sin(2 * math.pi * k / segments))
        for k in range(segments)
    ]
    return prism(name, ring, z0, z1, mat)


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


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None, poly=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads
    as a border ring around the opening. No booleans, all closed solids."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, SKIN + 0.09,
               frame_mat, poly)
    inset = 0.16
    face_panel(f"{tag}_fill", edge, u,
               rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
               0.0, SKIN + 0.15, fill_mat, poly)
    if glow_mat is not None:
        g = 0.30
        face_panel(f"{tag}_glow", edge, u,
                   rect_profile(w - 2 * g, z0 + g, z1 - g),
                   SKIN + 0.12, SKIN + 0.19, glow_mat, poly)


def juliet_rail(tag, edge, u, w, z0, z1, mat):
    """A horizontal-slat guard in front of a floor-to-ceiling window. Real ones
    project ~0.15 m; these project 0.30 because the rails are what make the
    two-tier loft rhythm legible from the app's downward camera (plan 2.6)."""
    for k, z in enumerate((z0 + (z1 - z0) * 0.45, z1)):
        face_panel(f"{tag}_slat{k}", edge, u,
                   rect_profile(w, z - 0.05, z + 0.05),
                   SKIN + 0.18, SKIN + 0.34, mat)
    for k, du in enumerate((-w / 2.0 + 0.07, w / 2.0 - 0.07)):
        face_panel(f"{tag}_post{k}", edge, u + du,
                   rect_profile(0.14, z0, z1), SKIN + 0.18, SKIN + 0.34, mat)


# Which loft windows are lit at night: six of sixteen, deliberately uneven —
# never a whole bay, never a whole row. (tier, part, bay) -> glow material key.
LIT = {
    (0, "main", 1): "Toy_glass_Glow",
    (0, "mezz", 3): "Toy_glass_Glow",
    (0, "mezz", 0): "Toy_gold_Glow",
    (1, "main", 0): "Toy_glass_Glow",
    (1, "mezz", 2): "Toy_glass_Glow",
    (1, "main", 3): "Toy_gold_Glow",
}


def stripes(materials):
    """The identity surface: irregular vertical panel bands running the full
    height of the Zoe elevation, alternating proud/flush so the aerial sun
    rakes them and they still read when the tones wash out under the app's
    flatter lighting."""
    total = sum(STRIPE_W)
    scale = LEN_ZOE / total
    u = 0.0
    for i, wrel in enumerate(STRIPE_W):
        w = wrel * scale
        depth = STRIPE_PROUD if i % 2 == 0 else STRIPE_FLUSH
        face_panel(
            f"stripe{i:02d}", EDGE_ZOE, u + w / 2.0,
            rect_profile(w, Z_BASE, Z_PARAPET), 0.0, depth,
            materials[STRIPE_TONES[STRIPE_TONE[i]]],
        )
        u += w


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials, bpy.data.curves):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    M = {k: material(k) for k in PALETTE_HEX}
    sand, stone, white, steel = M["Toy_sand"], M["Toy_stone"], M["Toy_white"], M["Toy_steel"]
    glass, glassl, ink = M["Toy_glass"], M["Toy_glassl"], M["Toy_ink"]

    # The CMU base steps back 0.35 m on Zoe only; the other three walls stay on
    # the survey line all the way down.
    base_ds = [0.0] * 4
    base_ds[EDGE_ZOE] = -BASE_RECESS
    BASE = offset_polygon_per_edge(FOOTPRINT, base_ds)

    # --- masses -------------------------------------------------------------
    # The body's bottom cap IS the soffit over the recess — the shadow line that
    # separates the pale striped wall from the rusticated plinth.
    prism("base", BASE, 0.0, Z_BASE, stone)
    prism("body", FOOTPRINT, Z_BASE, Z_DECK, sand, mat_caps=steel)

    # --- parapet ring + white coping ---------------------------------------
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET - 0.12, -PARAPET_T, 0.0, sand)
    ring_band("coping", FOOTPRINT, Z_PARAPET - 0.12, Z_PARAPET, -PARAPET_T - 0.06, 0.06, white)

    # --- THE IDENTITY: the vertical stripe cladding on Zoe -------------------
    stripes(M)

    # --- the two loft tiers, four bays ---------------------------------------
    for tier, ((m0, m1), (r0, r1), (_s0, _s1), (z0, z1)) in enumerate(TIERS):
        for bay, u in enumerate(BAY_U):
            gk = LIT.get((tier, "main", bay))
            rect_opening(f"t{tier}b{bay}main", EDGE_ZOE, u, WIN_W, m0, m1,
                         white, glass, M[gk] if gk else None)
            juliet_rail(f"t{tier}b{bay}rail", EDGE_ZOE, u, WIN_W - 0.20, r0, r1, steel)
            gk = LIT.get((tier, "mezz", bay))
            rect_opening(f"t{tier}b{bay}mezz", EDGE_ZOE, u, WIN_W, z0, z1,
                         white, glass, M[gk] if gk else None)

    # --- CMU base: five roll-up doors and the pedestrian entry ---------------
    face_panel("base_reveal", EDGE_ZOE, LEN_ZOE / 2.0,
               rect_profile(LEN_ZOE - 0.40, 1.46, 1.54), -0.05, 0.02, ink, BASE)
    for k, (u0, u1) in enumerate(DOORS):
        uc, w = (u0 + u1) / 2.0, u1 - u0
        face_panel(f"door{k}_jamb", EDGE_ZOE, uc, rect_profile(w + 0.18, 0.05, 2.50),
                   -0.20, 0.02, ink, BASE)
        face_panel(f"door{k}", EDGE_ZOE, uc, rect_profile(w, 0.15, 2.40),
                   -0.16, 0.08, steel, BASE)
        face_panel(f"door{k}_head", EDGE_ZOE, uc, rect_profile(w + 0.20, 2.40, 2.52),
                   -0.18, 0.10, ink, BASE)
        face_panel(f"door{k}_vent", EDGE_ZOE, uc, rect_profile(1.10, 0.30, 0.48),
                   0.04, 0.09, ink, BASE)

    U_ENTRY = (ENTRY_U0 + ENTRY_U1) / 2.0
    W_ENTRY = ENTRY_U1 - ENTRY_U0
    face_panel("entry_reveal", EDGE_ZOE, U_ENTRY, rect_profile(W_ENTRY, 0.0, Z_BASE),
               -0.45, 0.03, ink, BASE)
    face_panel("entry_door", EDGE_ZOE, U_ENTRY, rect_profile(W_ENTRY - 0.35, 0.0, 2.30),
               0.03, 0.12, ink, BASE)
    # permit 9704456, March 1997: "install galvanized steel awning over entry"
    face_panel("entry_awning", EDGE_ZOE, U_ENTRY, rect_profile(W_ENTRY + 0.55, 2.55, 2.67),
               -0.10, 0.90, steel, BASE)
    face_panel("entry_awning_lip", EDGE_ZOE, U_ENTRY,
               rect_profile(W_ENTRY + 0.55, 2.47, 2.55), 0.76, 0.90, ink, BASE)
    face_panel("entry_glow", EDGE_ZOE, U_ENTRY, rect_profile(W_ENTRY - 0.60, 2.05, 2.35),
               0.14, 0.21, M["Toy_gold_Glow"], BASE)

    # --- south-east elevation: open over the parking lot ---------------------
    # Two vertical stacks of small punched windows, and the fire escape of
    # permit 9621922 ("install fire escape at east elevation", 1996-97).
    for i, u in enumerate((5.20, 14.40)):
        for j, z in enumerate((4.10, 7.20, 11.30)):
            rect_opening(f"se{i}{j}", EDGE_SE, u, 0.95, z, z + 1.15, stone, glass)
    for k, z in enumerate((5.70, 11.00)):
        face_panel(f"fe_deck{k}", EDGE_SE, 9.90, rect_profile(2.60, z, z + 0.11),
                   0.0, 0.90, ink)
        for r, zr in enumerate((z + 0.55, z + 1.05)):
            face_panel(f"fe_rail{k}{r}", EDGE_SE, 9.90,
                       rect_profile(2.60, zr - 0.045, zr + 0.045), 0.80, 0.90, ink)
        for r, du in enumerate((-1.25, 1.25)):
            face_panel(f"fe_post{k}{r}", EDGE_SE, 9.90 + du,
                       rect_profile(0.10, z, z + 1.10), 0.80, 0.90, ink)
    for k, (z0, z1) in enumerate(((5.80, 11.00), (2.30, 5.70))):
        for r, du in enumerate((-0.34, 0.34)):
            face_panel(f"fe_rail{k}{r}_v", EDGE_SE, 9.90 + du,
                       rect_profile(0.11, z0, z1), 0.62, 0.74, ink)
        for m in range(6):
            z = z0 + (z1 - z0) * (m + 0.5) / 6.0
            face_panel(f"fe_rung{k}{m}", EDGE_SE, 9.90,
                       rect_profile(0.80, z - 0.045, z + 0.045), 0.62, 0.72, ink)

    # --- north-east elevation: near-blind onto a 2.4 m light gap -------------
    for i, u in enumerate((6.50, 14.10, 21.70)):
        rect_opening(f"ne{i}", EDGE_NE, u, 1.00, 9.30, 10.30, stone, glass)
    face_panel("ne_door", EDGE_NE, 25.60, rect_profile(1.20, 0.0, 2.40), 0.0, SKIN + 0.05, ink)

    # --- north-west party wall: blank, with the neighbour's roofline showing -
    face_panel("nw_reveal", EDGE_NW, LEN_SE / 2.0, rect_profile(LEN_SE - 0.30, 11.86, 11.94),
               -0.05, 0.02, stone)

    # --- roof: half the asset ------------------------------------------------
    # The monitor spine — three staggered glazed ridges lighting the internal
    # circulation, running down the middle and splitting the membrane into a
    # Zoe half and a rear half.
    MONITORS = ((7.00, 8.00), (14.00, 9.60), (21.00, 11.20))
    for k, (u, v) in enumerate(MONITORS):
        roof_box(f"mon{k}_kerb", u, v, Z_DECK, Z_DECK + 0.28, 7.00, 1.90, white)
        roof_box(f"mon{k}_glass", u, v, Z_DECK + 0.28, Z_DECK + 1.05, 6.80, 1.70, glassl)
        for m in range(4):
            roof_box(f"mon{k}_mull{m}", u - 2.55 + m * 1.70, v,
                     Z_DECK + 0.26, Z_DECK + 1.09, 0.12, 1.86, white)
        roof_box(f"mon{k}_glow", u, v, Z_DECK + 1.05, Z_DECK + 1.11, 6.20, 1.30,
                 M["Toy_glassl_Glow"])

    # Skylight scatter — denser on the Zoe half, and the rear quarter nearest
    # the party wall is deliberately left empty.
    SKYLIGHTS = ((12.00, 3.40), (18.00, 3.00), (24.50, 3.60),
                 (6.00, 10.60), (10.50, 13.50), (14.50, 16.50))
    for k, (u, v) in enumerate(SKYLIGHTS):
        roof_box(f"sky{k}_kerb", u, v, Z_DECK, Z_DECK + 0.22, 1.60, 1.60, white)
        roof_box(f"sky{k}", u, v, Z_DECK + 0.18, Z_DECK + 0.47, 1.34, 1.34, glassl)

    # The stair/elevator penthouse that sets the crest, at the parking-lot end.
    roof_box("penthouse", 23.50, 15.50, Z_DECK, Z_CREST - 0.38, 8.00, 6.00, white)
    roof_box("penthouse_cap", 23.50, 15.50, Z_CREST - 0.38, Z_CREST - 0.22, 8.30, 6.30, white)
    # The round vent on the penthouse roof is the tallest thing on the building
    # and therefore the LiDAR maximum: it sets the 17.00 m crest exactly.
    roof_cylinder("penthouse_vent", 21.80, 14.10, Z_CREST - 0.22, Z_CREST, 0.75, steel)
    roof_box("penthouse_door", 23.50, 12.62, Z_DECK, Z_DECK + 2.10, 1.20, 0.10, ink)

    # The common roof deck (documented by the sale listings; see plan 2.15).
    roof_box("deck_pave", 5.00, 3.80, Z_DECK, Z_DECK + 0.14, 7.00, 4.40, stone)
    roof_box("deck_wall_se", 8.58, 3.80, Z_DECK, Z_DECK + 1.10, 0.16, 4.40, white)
    roof_box("deck_wall_ne", 5.00, 6.08, Z_DECK, Z_DECK + 1.10, 7.16, 0.16, white)
    roof_box("deck_hatch", 2.30, 3.80, Z_DECK + 0.14, Z_DECK + 0.62, 0.85, 1.60, steel)

    for k, (u, v) in enumerate(((11.00, 6.00), (11.90, 6.30), (15.50, 7.50),
                                (16.40, 7.80), (19.50, 8.80), (20.40, 9.10))):
        roof_cylinder(f"vent{k}", u, v, Z_DECK, Z_DECK + 0.50, 0.20, steel)

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.12/2. The stripes, applied window panels, rails and hairline strips read
    # as lines rather than solids — a bevel on those costs ~96 triangles apiece
    # and buys nothing at city scale.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if name.endswith(("_fill", "_glow", "_glass")) or "_slat" in name or "_mull" in name:
            continue
        if name.startswith(("stripe", "fe_", "reveal", "base_reveal", "nw_reveal",
                            "entry_glow", "door", "sky")):
            continue
        if name.endswith("_frame") or name.endswith("_span") or name.startswith(("mon", "vent")):
            bevel(obj, width=0.05, segments=1)
        else:
            bevel(obj, width=0.12, segments=2)

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
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    print("[build] anchor lon/lat: -122.3960338 37.7800764 (footprint centroid)")
    print("[build] Zoe elevation heading: 225.4 deg true (SW)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "49-zoe.blend")
    glb = os.path.join(out, "49-zoe.glb")
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
