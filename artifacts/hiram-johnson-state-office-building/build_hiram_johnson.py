"""Deterministic Blender build of the SF-SIM miniature Hiram W. Johnson State
Office Building (455 Golden Gate Avenue, SOM 1998).

    blender -b --python build_hiram_johnson.py -- [--out DIR]

Writes hiram-johnson-state-office-building.blend/.glb next to this file (or into
--out). Geometry is authored in metres, Z up, +X east, +Y true north, origin at
the footprint bbox centre, min Z = 0, crest normalised to 61.90 m.

Design (see REFERENCE.md for the sources behind every number):

* the plan is a 127.38 x 47.70 m slab whose LONG faces are flat and whose SHORT
  ends are sculpted. Each end is a five-part profile measured off OSM
  way/35176304 reprojected into the Civic Center grid: cut-back corner, convex
  granite pier, deeply recessed curved glass bay, convex granite pier, cut-back
  corner. Here the OSM step trace is rebuilt as smooth arcs, which is what the
  Street View frames show;
* the south front is FLAT. SOM's "sweeping curve of the tallest slab gestures
  out toward the plaza" is realised by the end drums and the north entrance bay.
  The OSM south edge is collinear to within 1 cm over 91 m and a rectilinear
  re-projection of the Civic Center Plaza panorama shows a dead-straight parapet;
* the facade is a granite lattice over glass: nine punched-grid storeys from
  9.8 m to 42.9 m, then three lighter, more continuously glazed storeys to the
  53.6 m roof plane - the change the plaza photograph shows;
* the Golden Gate Avenue entrance is the hero: a convex glass bay bulging 3.5 m
  out of the north wall under a curved canopy on granite piers;
* a designed roof, because the camera looks down: level parapet ring, pale deck,
  and the long set-back mechanical penthouse that carries the crest from the
  53.61 m LiDAR median roof plane to SOM's published 203 ft = 61.87 m;
* flat Toy_* materials only. Three glow surfaces, all at the entrance.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

# ---------------------------------------------------------------- parameters

# Grid frame: E runs 0 (Larkin/west) -> 127.38 (Polk/east);
#             S runs 0 (Golden Gate/north) -> 47.70 (the seismic joint/south).
E_LEN = 127.38
S_LEN = 47.70
GRID_ROT = math.radians(8.73)  # long-axis bearing 81.27 deg = 8.73 deg N of E

# Measured end profiles: (s0, s1, e_face) from the reprojected OSM polygon.
WEST_PROFILE = [
    (0.00, 7.31, 8.00),    # north corner, cut back
    (7.31, 17.11, 1.40),   # convex granite pier
    (17.11, 29.51, 8.00),  # the recessed curved glass bay
    (29.51, 40.31, 0.00),  # convex granite pier
    (40.31, 47.70, 7.20),  # south corner, cut back
]
EAST_PROFILE = [
    (0.00, 7.21, 119.63),
    (7.21, 17.21, 126.64),
    (17.21, 28.60, 120.10),
    (28.60, 37.80, 127.38),
    (37.80, 47.70, 121.25),
]
BLEND = 5.0       # metres over which one profile level eases into the next
PIER_BOW = 1.10   # convex sagitta added to the two pier bands
BAY_BOW = 0.50    # concave sagitta of the recessed glass bay
END_SAMPLES = 40  # samples along S per end profile (fixed, see outline)

Z_BASE = 6.00     # top of the two-storey granite base
Z_GRID0 = 9.80    # first punched-window band
Z_GRID1 = 42.90   # top of the punched grid / bottom of the glazed ribbon
Z_DECK = 53.60    # main roof plane (DataSF hgt_median_m 53.61, OSM height=54)
Z_ROOF = 53.75    # the deck surface itself, 0.15 m above the structural plane
Z_PARAPET = 55.00
Z_PENT = 59.90    # top of the mechanical penthouse (LiDAR hgt_max 60.04)
Z_CREST = 61.90   # architectural crest (SOM 203 ft = 61.87 m)

FLOOR = 3.83      # 53.60 m over 14 storeys
GRID_ROWS = 9     # punched-window storeys
RIBBON_ROWS = 3   # the lighter glazed storeys on top
BAND_H = 2.40     # glass band height in the punched grid
PIER_PITCH = 8.40 # granite pier spacing on the long faces
GRID_E0, GRID_E1 = 10.60, 116.80   # extent of the lattice on the long faces

PROUD_PIER = 0.42     # how far the applied granite piers stand off the glass
PROUD_SPAND = 0.34
PROUD_BASE = 0.30
INSET_RIBBON = 0.55
INSET_PARAPET = 1.00
INSET_DECK = 2.00

BAY_S = (17.11, 29.51)     # west end glass bay, in S
BAY_S_E = (17.21, 28.60)   # east end glass bay
Z_BAY0, Z_BAY1 = 13.40, 51.50

ENTRY_E = 63.70            # centre of the Golden Gate Avenue entrance
ENTRY_W = 30.00            # width of the convex glass bay
ENTRY_OUT = 4.20           # how far it bulges north
Z_ENTRY1 = 30.60

PENT = (34.0, 92.0, 16.5, 31.5)   # mechanical penthouse, (e0, e1, s0, s1)
SKYLIGHTS = ((11.0, 29.0), (98.0, 116.0))
SKY_S = (18.5, 29.5)

BEVEL_W = 0.12
BEVEL_SEG = 2
ARC_SEGS = 14

PALETTE_HEX = {
    "Toy_cream": "f2ede3",
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_teal": "3fa8a0",
    "Toy_roofd": "45454a",
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


def dedupe_ring(poly, tol=2e-3):
    """Drop duplicate and collinear points. A run of collinear vertices makes
    the n-gon cap triangulate into slivers whose shared vertex normal collapses
    to zero length, which the stage-2 contract validator counts as
    invalid_or_nonunit_loop_normal and fails the asset on."""
    pts = []
    for p in poly:
        if pts and abs(p[0] - pts[-1][0]) < tol and abs(p[1] - pts[-1][1]) < tol:
            continue
        pts.append(p)
    while len(pts) > 3 and abs(pts[0][0] - pts[-1][0]) < tol and abs(pts[0][1] - pts[-1][1]) < tol:
        pts.pop()
    out = []
    n = len(pts)
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        base = math.hypot(c[0] - a[0], c[1] - a[1])
        if base > 1e-9 and abs(cross) / base < tol:
            continue  # b sits on the segment a-c
        out.append(b)
    return out if len(out) >= 3 else pts


def prism(name, poly, z0, z1, matname, bevel_w=0.0):
    """Extrude a polygon of (x, y) local points from z0 to z1."""
    poly = dedupe_ring(poly)
    if polygon_area(poly) < 0:
        poly = list(reversed(poly))
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


def polygon_area(poly):
    a = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        a += x0 * y1 - x1 * y0
    return a * 0.5


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def profile_e(prof, s, sign):
    """Smoothed E(s) for one end. sign = +1 for the east end (E grows outward),
    -1 for the west end. Pier bands bow outward, the middle band bows inward."""
    # base level: nearest band, eased across BLEND at each boundary
    e = prof[0][2]
    for i, (s0, s1, ev) in enumerate(prof):
        if i == 0:
            e = ev
            continue
        prev = prof[i - 1][2]
        t = smoothstep((s - (s0 - BLEND * 0.5)) / BLEND)
        e = prev + (ev - prev) * t if s < s0 + BLEND * 0.5 else ev
        if s < s0 - BLEND * 0.5:
            e = prev
            break
    # bow: bands 1 and 3 are the granite piers, band 2 is the glass bay
    for idx, bow in ((1, PIER_BOW * sign), (3, PIER_BOW * sign), (2, -BAY_BOW * sign)):
        s0, s1, _ = prof[idx]
        if s0 <= s <= s1:
            u = (s - s0) / (s1 - s0)
            e += bow * math.sin(math.pi * u)
    return e


def end_points(prof, sign, s_lo=0.0, s_hi=S_LEN, n=None):
    """Sampled (e, s) points down one end, S ascending. The sample COUNT is
    fixed so that every offset of the outline has matching vertices - the
    parapet ring depends on that, and a variable count self-intersects."""
    if n is None:
        n = END_SAMPLES
    pts = []
    for i in range(n + 1):
        s = s_lo + (s_hi - s_lo) * i / n
        s_eval = min(max(s, 0.0), S_LEN)
        pts.append((profile_e(prof, s_eval, sign), s))
    return pts


def outline(d=0.0):
    """Closed plan outline in the grid frame, offset outward by d.

    S is parameterised over [-d, S_LEN + d] so the long faces move with the
    offset and the point count never changes; E is offset outward per end.
    """
    s_lo, s_hi = -d, S_LEN + d
    west = [(e - d, s) for e, s in end_points(WEST_PROFILE, -1.0, s_lo, s_hi)]
    east = [(e + d, s) for e, s in end_points(EAST_PROFILE, +1.0, s_lo, s_hi)]
    return west + list(reversed(east))


_OUTLINE_MASK = None


def outline_mask():
    """Indices of outline() worth keeping, computed once at d = 0 and reused for
    every offset so outer/inner rings stay index-aligned."""
    global _OUTLINE_MASK
    if _OUTLINE_MASK is None:
        pts = [grid_to_local(e, s) for e, s in outline(0.0)]
        n = len(pts)
        keep = []
        for i in range(n):
            a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
            cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            base = math.hypot(c[0] - a[0], c[1] - a[1])
            if base > 1e-9 and abs(cross) / base < 0.012:
                continue
            keep.append(i)
        _OUTLINE_MASK = keep
    return _OUTLINE_MASK


def outline_poly(d):
    pts = outline(d)
    return [grid_to_local(*pts[i]) for i in outline_mask()]


def outline_prism(name, d, z0, z1, matname, bevel_w=BEVEL_W):
    return prism(name, outline_poly(d), z0, z1, matname, bevel_w)


def outline_ring(name, d_out, d_in, z0, z1, matname, bevel_w=BEVEL_W):
    """A closed ring following the plan - used for the parapet."""
    outer = outline_poly(d_out)
    inner = outline_poly(d_in)
    if polygon_area(outer) < 0:
        outer.reverse()
        inner.reverse()
    n = len(outer)
    verts = ([(p[0], p[1], z0) for p in outer] + [(p[0], p[1], z1) for p in outer]
             + [(p[0], p[1], z0) for p in inner] + [(p[0], p[1], z1) for p in inner])
    O0, O1, I0, I1 = 0, n, 2 * n, 3 * n
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append([O0 + i, O0 + j, O1 + j, O1 + i])       # outer wall
        faces.append([I1 + i, I1 + j, I0 + j, I0 + i])       # inner wall
        faces.append([O1 + i, O1 + j, I1 + j, I1 + i])       # top
        faces.append([I0 + i, I0 + j, O0 + j, O0 + i])       # bottom
    return new_mesh(name, verts, faces, matname, bevel_w)


# ------------------------------------------------------------------ assembly


def build_envelope():
    outline_prism("base", PROUD_BASE, 0.0, Z_BASE, "Toy_stone")
    outline_prism("body", 0.0, Z_BASE, Z_GRID1, "Toy_cream")
    # the lighter glazed ribbon is a real set-back block, not a painted band
    outline_prism("ribbon", -INSET_RIBBON, Z_GRID1, Z_DECK, "Toy_cream")


def build_lattice():
    """Granite lattice over glass on the two long faces."""
    faces = (("n", 0.0, -1.0), ("s", S_LEN, +1.0))
    for tag, s_face, sgn in faces:
        # nine punched-grid storeys: a continuous glass band per storey, with
        # applied granite piers and spandrels standing proud of it.
        for r in range(GRID_ROWS):
            z0 = Z_GRID0 + r * FLOOR
            box(f"{tag}_gband{r}", GRID_E0, GRID_E1,
                s_face + sgn * -0.10, s_face + sgn * 0.16,
                z0, z0 + BAND_H, "Toy_glass")
            box(f"{tag}_spand{r}", GRID_E0 - 0.6, GRID_E1 + 0.6,
                s_face - sgn * 0.02, s_face + sgn * PROUD_SPAND,
                z0 + BAND_H, z0 + FLOOR, "Toy_cream", bevel_w=0.06)
        n_piers = int(round((GRID_E1 - GRID_E0) / PIER_PITCH))
        pitch = (GRID_E1 - GRID_E0) / n_piers
        for i in range(n_piers + 1):
            e_c = GRID_E0 + pitch * i
            box(f"{tag}_pier{i}", e_c - 1.15, e_c + 1.15,
                s_face - sgn * 0.02, s_face + sgn * PROUD_PIER,
                Z_BASE, Z_GRID1, "Toy_cream", bevel_w=0.07)
        # base course and the band that closes the grid at the top
        box(f"{tag}_sill", GRID_E0 - 1.2, GRID_E1 + 1.2,
            s_face - sgn * 0.02, s_face + sgn * (PROUD_PIER + 0.16),
            Z_GRID0 - 0.75, Z_GRID0, "Toy_trim", bevel_w=0.07)
        box(f"{tag}_grid_cap", GRID_E0 - 1.2, GRID_E1 + 1.2,
            s_face - sgn * 0.02, s_face + sgn * (PROUD_PIER + 0.16),
            Z_GRID1 - 0.85, Z_GRID1, "Toy_trim", bevel_w=0.07)

        # three lighter storeys above: continuous glazing, thin trim spandrels
        rib = (Z_DECK - Z_GRID1) / RIBBON_ROWS
        for r in range(RIBBON_ROWS):
            z0 = Z_GRID1 + r * rib
            box(f"{tag}_rband{r}", GRID_E0 - 0.4, GRID_E1 + 0.4,
                s_face - sgn * (INSET_RIBBON + 0.10),
                s_face - sgn * (INSET_RIBBON - 0.18),
                z0 + 0.55, z0 + rib - 0.30, "Toy_glass")
            box(f"{tag}_rspand{r}", GRID_E0 - 0.7, GRID_E1 + 0.7,
                s_face - sgn * (INSET_RIBBON + 0.02),
                s_face - sgn * (INSET_RIBBON - 0.34),
                z0 + rib - 0.30, z0 + rib + 0.55, "Toy_trim", bevel_w=0.06)


def build_ends():
    """The two drums: recessed curved glass bays between the granite piers,
    plus the full-height louvre slots that cut the stone."""
    for tag, prof, sign, bay in (("w", WEST_PROFILE, -1.0, BAY_S),
                                 ("e", EAST_PROFILE, +1.0, BAY_S_E)):
        s0, s1 = bay
        e_face = profile_e(prof, (s0 + s1) * 0.5, sign)
        # the glazed bay itself, sitting just proud of the recessed stone
        segs = ARC_SEGS
        pts = []
        for i in range(segs + 1):
            u = i / segs
            # profile_e already carries the bay's concave bow - adding it a
            # second time buries the glass inside the granite.
            pts.append((profile_e(prof, s0 + (s1 - s0) * u, sign) + 0.14 * sign,
                        s0 + (s1 - s0) * u))
        back = [(profile_e(prof, s, sign) - 0.55 * sign, s) for _, s in pts]
        ring = [grid_to_local(e, s) for e, s in pts] + \
               [grid_to_local(e, s) for e, s in reversed(back)]
        prism(f"{tag}_bay", ring, Z_BAY0, Z_BAY1, "Toy_teal", 0.0)
        # four horizontal mullion bands tie the bay into the storey lines
        for k in range(4):
            z = Z_BAY0 + (Z_BAY1 - Z_BAY0) * (k + 1) / 5.0
            mull = [grid_to_local(e + 0.16 * sign, s) for e, s in pts] + \
                   [grid_to_local(e, s) for e, s in reversed(back)]
            prism(f"{tag}_mull{k}", mull, z, z + 0.45, "Toy_trim", 0.0)
        # louvre slots in the piers
        for band, frac in ((1, 0.34), (1, 0.70), (3, 0.30), (3, 0.66)):
            bs0, bs1, _ = prof[band]
            s = bs0 + (bs1 - bs0) * frac
            e = profile_e(prof, s, sign)
            a = grid_to_local(e - 0.55 * sign, s - 0.55)
            b = grid_to_local(e + 0.08 * sign, s + 0.55)
            poly = [(a[0], a[1]), (b[0], a[1]), (b[0], b[1]), (a[0], b[1])]
            prism(f"{tag}_louvre{band}_{int(frac*100)}", poly, Z_BASE, Z_DECK - 1.6,
                  "Toy_roofd", 0.0)


def build_roof():
    # Toy_roofd renders near-black on a large flat deck under this rig; the
    # deck reads as a hole in the model. Toy_steel is the repo's roof-deck grey.
    # NOT coplanar with the ribbon block's top cap at Z_DECK: two coincident
    # faces there make Cycles shade the model's unlit interior, and the whole
    # roof renders pure black while Workbench shows it correctly.
    outline_prism("deck", -(INSET_RIBBON + 0.20), Z_DECK - 0.35, Z_ROOF,
                  "Toy_steel", bevel_w=0.0)
    # 0.06 m proud of the ribbon block: a coincident outer wall makes Cycles
    # shade the unlit interior and punches a black notch in the parapet.
    # bevel_w = 0: a 0.12 m bevel on a ring this long manufactures ~2,000
    # sub-5 mm faces where the profiles meet at the drum corners, and the Phase B
    # weld collapses two of them into zero-length vertex normals - which the
    # contract validator counts as invalid_or_nonunit_loop_normal on the SHIPPED
    # file only. The parapet's edge is crisp on purpose.
    outline_ring("parapet", -(INSET_RIBBON - 0.06), -INSET_RIBBON - INSET_PARAPET,
                 Z_DECK, Z_PARAPET, "Toy_trim", bevel_w=0.0)

    e0, e1, s0, s1 = PENT
    box("penthouse", e0, e1, s0, s1, Z_ROOF, Z_PENT, "Toy_cream", bevel_w=BEVEL_W)
    box("pent_louvre", e0 - 0.22, e1 + 0.22, s0 - 0.22, s1 + 0.22,
        Z_ROOF + 2.4, Z_ROOF + 5.0, "Toy_roofd", bevel_w=0.08)
    box("pent_cap", e0 - 0.45, e1 + 0.45, s0 - 0.45, s1 + 0.45,
        Z_PENT, Z_CREST, "Toy_trim", bevel_w=BEVEL_W)

    for i, (a, b) in enumerate(SKYLIGHTS):
        box(f"sky_curb{i}", a - 0.6, b + 0.6, SKY_S[0] - 0.6, SKY_S[1] + 0.6,
            Z_ROOF, Z_ROOF + 0.5, "Toy_trim", bevel_w=0.08)
        box(f"sky{i}", a, b, SKY_S[0], SKY_S[1],
            Z_ROOF + 0.5, Z_ROOF + 1.0, "Toy_teal", bevel_w=0.08)

    for i, e_c in enumerate((36.0, 60.0, 84.0)):
        box(f"mech{i}", e_c - 2.5, e_c + 2.5, 8.5, 12.5,
            Z_ROOF, Z_ROOF + 2.2, "Toy_roofd", bevel_w=0.09)
    box("stair_pent", 68.0, 78.0, 34.5, 39.5, Z_ROOF, Z_ROOF + 3.0,
        "Toy_roofd", bevel_w=0.10)


def build_entrance():
    """Golden Gate Avenue: the convex glass bay, the curved canopy, the lobby."""
    e0, e1 = ENTRY_E - ENTRY_W * 0.5, ENTRY_E + ENTRY_W * 0.5
    segs = ARC_SEGS
    front = []
    for i in range(segs + 1):
        u = i / segs
        e = e0 + (e1 - e0) * u
        front.append((e, -ENTRY_OUT * math.sin(math.pi * u)))
    back = [(e, 0.55) for e, _ in front]
    ring = [grid_to_local(e, s) for e, s in front] + \
           [grid_to_local(e, s) for e, s in reversed(back)]
    prism("entry_bay", ring, Z_BASE, Z_ENTRY1, "Toy_glassl_Glow", 0.0)

    # mullion bands and the eyebrow that caps the bay
    for k in range(3):
        z = Z_BASE + (Z_ENTRY1 - Z_BASE) * (k + 1) / 4.0
        band = [grid_to_local(e, s - 0.16) for e, s in front] + \
               [grid_to_local(e, s) for e, s in reversed(back)]
        prism(f"entry_mull{k}", band, z, z + 0.42, "Toy_trim", 0.0)
    eyeb = [grid_to_local(e, s - 1.10) for e, s in front] + \
           [grid_to_local(e, s) for e, s in reversed(back)]
    prism("entry_eyebrow", eyeb, Z_ENTRY1, Z_ENTRY1 + 1.10, "Toy_trim", 0.10)

    # the canopy: a curved slab on four granite piers
    cf, cb = [], []
    ce0, ce1 = ENTRY_E - 18.0, ENTRY_E + 18.0
    for i in range(segs + 1):
        u = i / segs
        e = ce0 + (ce1 - ce0) * u
        cf.append((e, -8.5 - 1.6 * math.sin(math.pi * u)))
        cb.append((e, 0.30))
    ring = [grid_to_local(e, s) for e, s in cf] + \
           [grid_to_local(e, s) for e, s in reversed(cb)]
    prism("canopy", ring, 11.40, 12.30, "Toy_trim", 0.09)
    soff = [grid_to_local(e, s + 0.35) for e, s in cf] + \
           [grid_to_local(e, s) for e, s in reversed(cb)]
    prism("canopy_soffit", soff, 11.05, 11.40, "Toy_gold_Glow", 0.0)
    for e_c in (ce0 + 3.0, ENTRY_E - 7.5, ENTRY_E + 7.5, ce1 - 3.0):
        box(f"canopy_pier{int(e_c)}", e_c - 1.25, e_c + 1.25, -8.0, -5.5,
            0.0, 11.40, "Toy_stone", bevel_w=0.10)

    # the two-storey lobby glazing, set back behind the canopy
    box("lobby", ENTRY_E - 13.0, ENTRY_E + 13.0, -0.20, 0.30,
        1.00, 10.60, "Toy_gold_Glow")
    # a granite reveal frames the bay so it reads as architecture, not a decal
    for e_c in (ENTRY_E - ENTRY_W * 0.5 - 1.3, ENTRY_E + ENTRY_W * 0.5 + 1.3):
        box(f"entry_jamb{int(e_c)}", e_c - 1.3, e_c + 1.3, -1.4, 1.2,
            0.0, Z_ENTRY1 + 1.1, "Toy_cream", bevel_w=0.10)
    # the Polk Street shopfront in the east base
    box("shopfront", 118.9, 125.9, 8.5, 8.9, 1.50, 4.50, "Toy_glass")


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    OBJECTS.clear()
    build_envelope()
    build_lattice()
    build_ends()
    build_roof()
    build_entrance()

    rot = Matrix.Rotation(GRID_ROT, 4, "Z")
    for o in OBJECTS:
        o.data.transform(rot)

    mn, mx = bounds()
    shift = Vector((-(mn.x + mx.x) * 0.5, -(mn.y + mx.y) * 0.5, -mn.z))
    for o in OBJECTS:
        o.data.transform(Matrix.Translation(shift))

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

    blend = os.path.join(out, "hiram-johnson-state-office-building.blend")
    glb = os.path.join(out, "hiram-johnson-state-office-building.glb")
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
