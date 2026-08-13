"""Deterministic Blender build of the SF-SIM miniature 171 South Park Street.

    blender -b --python build_171_south_park.py -- [--out DIR]

Writes 171-south-park.blend and 171-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = footprint AREA CENTROID (anchor
lon -122.3945219, lat 37.7809000), min Z = 0, crowning cornice exactly 12.6 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured footprint — a WEDGE, 131.2 m2, broad on South Park's oval and
  tapering over ~20.6 m to a 5.44 m tail. This shape is the asset: it is what
  the app's downward camera sees first, and nothing else in the district has it;
* a three-facet park front (outward bearings 1.1 / 348.2 / 321.3 deg) bowing
  along the oval. The facet creases are real and the cornice steps with them;
* the FLAT-FRONT Edwardian flats variant — every opening flush, no angled bays.
  All the relief is ornament, in three horizontal bands: a garland frieze at
  each upper floor line (abstracted to a plain proud band) and the crowning
  bracketed cornice with its raised centre section, which is the tallest thing
  on the building and what the 12.62 m LiDAR maximum measures;
* three storeys of ~3.8 m, entry at grade — a pedimented porch hood on
  pilasters over sage-green doors, at the WEST end of the front;
* light blue-gray painted clapboard (Toy_slate, a deliberate palette extension
  — see REPORT.md), cooler and paler than every neighbour on the oval;
* night state: a restrained scatter of lit upper windows plus the entry lamp.
  Glow surfaces are thin shells proud of the opaque glazing (the app renders
  _Glow in a separate layer that is ~12% alpha by day — never author a primary
  surface as glow). The friezes and cornice do NOT glow: they are daylight
  identity, and lighting them would misread as signage;
* a designed roof for the app's downward camera: a four-skylight row across the
  wide front third, a pair further back, a mechanical box and a hatch, plus the
  rear deck hung off the tail.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way 124889458 (agrees with DataSF SF3775137 within 0.8% on area),
# projected with the app's tangent projection and recentred on the footprint's
# AREA CENTROID. CCW. The v1..v3 run is the light-well notch on the southwest
# party wall — real survey geometry, kept.
FOOTPRINT = [
    (-9.513, 4.415),
    (-3.371, -1.664),
    (-2.007, -1.498),
    (0.343, -3.742),
    (-0.476, -4.527),
    (5.024, -9.988),
    (8.940, -6.208),
    (7.215, -4.174),
    (4.329, -0.879),
    (3.036, 0.591),
    (0.968, 7.400),
    (-2.922, 7.477),
    (-6.670, 6.693),
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_FRONT_E = 10   # 3.89 m, faces N     1.1 deg — park front, east facet
EDGE_FRONT_C = 11   # 3.83 m, faces NNW 348.2 deg — park front, centre facet
EDGE_FRONT_W = 12   # 3.64 m, faces NW  321.3 deg — park front, west facet (entry)
EDGE_RET_E = 9      # 7.12 m, faces ENE  73.1 deg — northeast return
EDGE_RET_W = 0      # 8.64 m, faces SW  224.7 deg — southwest party wall
EDGE_NE = 7         # 4.38 m, faces NE   48.8 deg — northeast party wall
EDGE_TAIL = 5       # 5.44 m, faces SE  136.0 deg — tail (rear)

Z_FLOOR = (0.0, 3.80, 7.60)     # three storeys, generously tall (11.41 / 3)
Z_DECK = 11.41                  # roof deck — DataSF LiDAR hgt_median_m
Z_CORN0, Z_CORN1 = 11.41, 11.96  # main cornice band
Z_CREST = 12.60                 # crown centre section = LiDAR max -> bbox top
FRIEZE_H = 0.35                 # garland frieze, abstracted to a plain band
CORNICE_D = 0.40                # cornice projection
FRIEZE_D = 0.10                 # frieze projection

PALETTE_HEX = {
    # Deliberate palette extension. The real facade is a light blue-gray:
    # Toy_steel (9aa0a6) is the nearest palette entry but reads neutral and
    # kills the blue that makes this building the coolest thing on the oval;
    # Toy_glassl (6f95b8) is far too saturated. AGENTS rule on painted
    # residential rows applies. Off-palette is a WARN, not a FAIL.
    "Toy_slate": "a7b3bc",
    "Toy_trim": "f3efe6",
    "Toy_stone": "d9d2c2",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    # The roof was re-done in March 2026 and reads noticeably PALER than every
    # neighbour on the oval in current imagery (REFERENCE.md s.5). Toy_roofd is
    # the palette's dark deck colour and is kept for the kerbs and the hatch,
    # which need to read as objects ON a pale deck; the deck itself is Toy_sand.
    "Toy_roofd": "45454a",
    "Toy_sand": "ece4d4",
    "Toy_steel": "9aa0a6",
    "Toy_verdigris": "9fb8a8",
    "Toy_ink": "3a3530",
    "Toy_glass_Glow": "6f95b8",
    "Toy_trim_Glow": "f3efe6",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def poly_edge(i):
    """Edge i of FOOTPRINT: (origin, length, tangent unit, outward normal)."""
    a = FOOTPRINT[i]
    b = FOOTPRINT[(i + 1) % len(FOOTPRINT)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def rect_profile(w, z0, z1):
    return [(-w / 2, z0), (w / 2, z0), (w / 2, z1), (-w / 2, z1)]


def gable_profile(w, z0, z1):
    """Pediment: a rectangle capped by a triangle — the entry porch hood."""
    return [(-w / 2, z0), (w / 2, z0), (w / 2, z0 + 0.16), (0.0, z1), (-w / 2, z0 + 0.16)]


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
    """Miniature-style edge softening on the chunky solids (style bible s.4).

    Width is capped at a third of the object's thinnest dimension: the applied
    trim panels here are only 70-400 mm thick, and a flat 0.10 m bevel on those
    relies entirely on clamp_overlap, which collapses opposing profiles into
    zero-area slivers. The remove_doubles/dissolve_degenerate pass sweeps up
    whatever clamping still pinches shut.
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
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-4)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-4, edges=list(bm.edges))
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


def face_panel(name, edge, u_centre, profile, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in the plane of wall `edge`,
    extruded outward from offset d0 to d1 along that wall's normal."""
    a, _length, t, n = poly_edge(edge)
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
    """Box with local +x along yaw and local +y 90 deg ccw of it."""
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
        # Flagged for the app's night pass; emission is off in the day asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------------- parts

# The roof grid: a centreline from the middle of the park front to the middle
# of the tail. Roof furniture is placed along it so everything sits inside the
# wedge and lines up with the building rather than with the world axes.
ROOF_A = (-4.63, 6.69)
ROOF_B = (6.98, -8.10)
_rd = (ROOF_B[0] - ROOF_A[0], ROOF_B[1] - ROOF_A[1])
ROOF_L = math.hypot(*_rd)
ROOF_U = (_rd[0] / ROOF_L, _rd[1] / ROOF_L)
ROOF_P = (-ROOF_U[1], ROOF_U[0])
ROOF_YAW = math.atan2(ROOF_U[1], ROOF_U[0])


def roof_box(name, t, off, z0, z1, su, sv, mat):
    """Box on the roof at fraction `t` down the centreline, `off` metres to its
    left. su runs across the building, sv down the centreline."""
    cx = ROOF_A[0] + ROOF_U[0] * t * ROOF_L + ROOF_P[0] * off
    cy = ROOF_A[1] + ROOF_U[1] * t * ROOF_L + ROOF_P[1] * off
    return box(name, cx, cy, z0, z1, sv, su, mat, yaw=ROOF_YAW)


def window(tag, edge, u, w, z0, z1, trim, glass, stone, glow=None):
    """A flush window: proud trim frame, glazing set behind it, a stone sill,
    and — at night — a thin glow shell proud of the opaque glazing."""
    # The glazing sits PROUD of the trim surround, not behind it: a frame panel
    # spanning the full opening occludes anything drawn inside its own depth
    # range, which is what turned every window into a blank cream slab in the
    # first render pass. Trim to 0.07, glass to 0.13, glow shell to 0.19.
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, 0.07, trim)
    face_panel(
        f"{tag}_fill", edge, u, rect_profile(w - 0.26, z0 + 0.13, z1 - 0.13), 0.0, 0.13, glass
    )
    face_panel(f"{tag}_sill", edge, u, rect_profile(w + 0.22, z0 - 0.15, z0), 0.0, 0.20, stone)
    if glow is not None:
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            rect_profile(w - 0.64, z0 + 0.32, z1 - 0.32),
            0.13,
            0.19,
            glow,
        )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    slate = material("Toy_slate")
    trim = material("Toy_trim")
    stone = material("Toy_stone")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    sand = material("Toy_sand")
    steel = material("Toy_steel")
    sage = material("Toy_verdigris")
    ink = material("Toy_ink")
    glow_w = material("Toy_glass_Glow")
    glow_t = material("Toy_trim_Glow")

    # --- body ---------------------------------------------------------------
    # One clean wedge from grade to the roof deck. Every footprint vertex is
    # kept, notch included: the plan shape is the whole point of this asset.
    prism("body", FOOTPRINT, 0.0, Z_DECK, slate, mat_caps=sand)

    # --- park front: the three facets ---------------------------------------
    FRONT = (EDGE_FRONT_E, EDGE_FRONT_C, EDGE_FRONT_W)
    # One paired window per facet per upper floor, plus the ground floor. The
    # front is only 11.36 m wide across three facets, so one generous pair per
    # facet is the honest rhythm; the entry takes the west facet's ground slot.
    for edge in FRONT:
        _a, length, _t, _n = poly_edge(edge)
        u = length / 2
        w = min(2.05, length - 1.4)
        for level, (z0, z1) in enumerate(((1.15, 3.15), (4.85, 6.85), (8.65, 10.65))):
            if edge == EDGE_FRONT_W and level == 0:
                continue  # the entry sits here
            # Night: a restrained scatter, not a lit-up office front.
            lit = glow_w if (edge, level) in ((EDGE_FRONT_C, 1), (EDGE_FRONT_E, 2)) else None
            window(f"win_f{edge}_{level}", edge, u, w, z0, z1, trim, glass, stone, lit)

    # --- entry: pedimented porch hood at the west end ------------------------
    _a, w_len, _t, _n = poly_edge(EDGE_FRONT_W)
    eu = w_len / 2
    face_panel("entry_step", EDGE_FRONT_W, eu, rect_profile(2.10, 0.0, 0.28), 0.0, 0.55, stone)
    face_panel("entry_recess", EDGE_FRONT_W, eu, rect_profile(1.72, 0.28, 3.00), 0.0, 0.07, ink)
    face_panel("entry_door", EDGE_FRONT_W, eu, rect_profile(1.28, 0.28, 2.78), 0.0, 0.13, sage)
    for side in (-1, 1):
        face_panel(
            f"entry_pilaster{side}",
            EDGE_FRONT_W,
            eu + side * 1.03,
            rect_profile(0.30, 0.0, 3.06),
            0.0,
            0.26,
            trim,
        )
    face_panel(
        "entry_hood", EDGE_FRONT_W, eu, gable_profile(2.26, 3.06, 3.82), 0.0, 0.46, trim
    )
    # The one supporting night accent: a lamp under the hood.
    face_panel("entry_lamp", EDGE_FRONT_W, eu, rect_profile(0.44, 2.86, 3.02), 0.16, 0.26, glow_t)

    # --- the three horizontal ornament bands --------------------------------
    # The real building carries carved garland-and-paterae friezes at each upper
    # floor line. At city scale a garland is a stripe, so a stripe is what
    # ships (style bible s.22: simplify the facade into broad rhythms).
    RETURNS = ((EDGE_RET_E, "end"), (EDGE_RET_W, "start"))
    for band, z0 in enumerate((Z_FLOOR[1], Z_FLOOR[2])):
        for edge in FRONT:
            _a, length, _t, _n = poly_edge(edge)
            face_panel(
                f"frieze{band}_{edge}",
                edge,
                length / 2,
                rect_profile(length, z0, z0 + FRIEZE_H),
                0.0,
                FRIEZE_D,
                trim,
            )
        for edge, side in RETURNS:
            _a, length, _t, _n = poly_edge(edge)
            u = length - 0.42 if side == "end" else 0.42
            face_panel(
                f"frieze{band}_ret{edge}",
                edge,
                u,
                rect_profile(0.84, z0, z0 + FRIEZE_H),
                0.0,
                FRIEZE_D,
                trim,
            )

    # --- crowning cornice: steps at every facet crease -----------------------
    for edge in FRONT:
        _a, length, _t, _n = poly_edge(edge)
        face_panel(
            f"cornice_{edge}",
            edge,
            length / 2,
            rect_profile(length, Z_CORN0, Z_CORN1),
            0.0,
            CORNICE_D,
            trim,
        )
        # Brackets: one row of identical chunky blocks, front facets only.
        count = max(2, int(length / 1.05))
        for k in range(count):
            u = length * (k + 0.5) / count
            face_panel(
                f"bracket_{edge}_{k}",
                edge,
                u,
                rect_profile(0.26, 11.02, Z_CORN0),
                0.0,
                CORNICE_D - 0.09,
                trim,
            )
    for edge, side in RETURNS:
        _a, length, _t, _n = poly_edge(edge)
        u = length - 0.42 if side == "end" else 0.42
        face_panel(
            f"cornice_ret{edge}",
            edge,
            u,
            rect_profile(0.84, Z_CORN0, Z_CORN1),
            0.0,
            CORNICE_D,
            trim,
        )
    # The raised centre section over the middle facet. This is the tallest
    # geometry in the export and must land on Z_CREST exactly.
    _a, c_len, _t, _n = poly_edge(EDGE_FRONT_C)
    face_panel(
        "crown", EDGE_FRONT_C, c_len / 2, rect_profile(c_len - 0.34, Z_CORN1, Z_CREST), 0.0, 0.30, trim
    )

    # --- flanks and tail -----------------------------------------------------
    # Both long flanks are party walls. The northeast one stands ~3 m above
    # 165-167's roof deck, and the app's camera sees that band — so it gets a
    # sparse scatter up there and nothing below. The southwest flank is buried
    # by the taller 181 and gets nothing invented.
    _a, ne_len, _t, _n = poly_edge(EDGE_NE)
    window("win_ne0", EDGE_NE, ne_len * 0.32, 1.25, 8.85, 10.45, trim, glass, stone)
    window("win_ne1", EDGE_NE, ne_len * 0.72, 1.25, 8.85, 10.45, trim, glass, stone)
    _a, re_len, _t, _n = poly_edge(EDGE_RET_E)
    window("win_re0", EDGE_RET_E, re_len * 0.30, 1.25, 8.85, 10.45, trim, glass, stone)

    _a, tail_len, _t, _n = poly_edge(EDGE_TAIL)
    for level, (z0, z1) in enumerate(((4.85, 6.85), (8.65, 10.65))):
        for k, frac in enumerate((0.30, 0.70)):
            lit = glow_w if (level, k) == (1, 0) else None
            window(
                f"win_t{level}_{k}", EDGE_TAIL, tail_len * frac, 1.35, z0, z1, trim, glass, stone, lit
            )
    # Rear deck (SF permit 200509062106, 2005) hung off the tail.
    face_panel("deck_slab", EDGE_TAIL, tail_len / 2, rect_profile(3.50, 7.42, 7.60), 0.0, 1.85, ink)
    face_panel("deck_rail", EDGE_TAIL, tail_len / 2, rect_profile(3.50, 7.60, 8.52), 1.67, 1.85, ink)
    for side in (-1, 1):
        face_panel(
            f"deck_post{side}",
            EDGE_TAIL,
            tail_len / 2 + side * 1.66,
            rect_profile(0.18, 7.60, 8.60),
            0.0,
            1.85,
            ink,
        )

    # --- roof: the surface the app's camera sees most ------------------------
    # A four-skylight row across the wide front third, a pair further back, one
    # mechanical box and a hatch pushed toward the tail — which leaves the broad
    # front third clean so the taper reads (style bible s.10).
    for i, off in enumerate((-3.2, -1.1, 1.0, 3.1)):
        roof_box(f"skylight_kerb{i}", 0.24, off, Z_DECK, Z_DECK + 0.16, 1.30, 0.95, roofd)
        roof_box(f"skylight{i}", 0.24, off, Z_DECK + 0.13, Z_DECK + 0.34, 1.10, 0.78, glassl)
    for i, off in enumerate((-1.3, 0.9)):
        roof_box(f"skylight_kerb{4 + i}", 0.44, off, Z_DECK, Z_DECK + 0.16, 1.30, 0.95, roofd)
        roof_box(f"skylight{4 + i}", 0.44, off, Z_DECK + 0.13, Z_DECK + 0.34, 1.10, 0.78, glassl)
    roof_box("mech", 0.63, 0.0, Z_DECK, Z_DECK + 0.80, 1.60, 1.20, steel)
    roof_box("roof_hatch", 0.53, 1.2, Z_DECK, Z_DECK + 0.42, 1.10, 0.90, roofd)
    roof_box("vent", 0.72, -1.1, Z_DECK, Z_DECK + 0.62, 0.42, 0.42, steel)

    # Bevel budget: the body and the ornament bands carry the miniature read, so
    # they get the full 0.10/2. The applied window panels are small and numerous
    # — frames get a token 1-segment softening and the fills/glow/sills none at
    # all, which is what keeps this under the 8,000-triangle cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow", "_sill")):
            continue
        if obj.name.endswith("_frame") or obj.name.startswith("bracket"):
            bevel(obj, width=0.04, segments=1)
        else:
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
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] xy bbox centre={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    print("[build] anchor lon/lat: -122.3945219 37.7809000 (footprint area centroid)")
    print("[build] park front heading: 343.5 deg true (NNW), three facets")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "171-south-park.blend")
    glb = os.path.join(out, "171-south-park.glb")
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
