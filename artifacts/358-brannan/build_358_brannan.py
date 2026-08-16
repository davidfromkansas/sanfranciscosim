"""Deterministic Blender build of the SF-SIM miniature 358 Brannan Street.

    blender -b --python build_358_brannan.py -- [--out DIR]

Writes 358-brannan.blend and 358-brannan.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint OBB centre (anchor lon -122.3936350,
lat 37.7809258), min Z = 0, bay cornice cap exactly 9.6 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3775017) reduced to its
  minimum-area rectangle — 6.93 m of Brannan frontage running 25.20 m clean
  through the block to Varney Place, at 45.3 deg off the world axes. The raw
  LiDAR polygon has 18 vertices but 95.3% rectangular fill and matches the
  Assessor's 1,760 sq ft lot to 1.8%: it is a rectangle plus scan noise;
* the recognition cue is the PROPORTION. A 6.93 m frontage between a 20 m and a
  25 m one is the whole building. Everything else is subordinate to keeping that
  slot narrow;
* a two-level roof: the rear (Varney) two-thirds at 7.70 m — the LiDAR median,
  measured — stepping up to a front block at 8.40 m inside a 9.00 m parapet;
* the identity feature: a canted bay window over the Brannan freight door, its
  cornice cap lifted proud of the parapet to set the 9.6 m crest. That lift is
  the one place semantic exaggeration is spent;
* two fronts, not a front and a back: Varney Place carries a full-width slate
  timber storefront under a brown wood-sided upper storey, because this is a
  through-lot and the batting cage's actual entrance is on the alley;
* night state: the tenant's sign band is the hero glow (a lit sign is what a
  batting cage open until 20:00 has, and it is the only warm light on this
  stretch), supported by two lit bay windows. Varney does not glow — it is a
  back alley. Glow surfaces are thin shells proud of the opaque surface behind
  them (the app renders _Glow in a separate layer that is ~12% alpha by day —
  never author a primary surface as glow);
* blind party-wall flanks. Both neighbours' walls touch this building; inventing
  a window grid there would be a lie the aerial camera can see.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF building footprint SF3775017 projected with the app's tangent
# projection, reduced to its minimum-area OBB and recentred on the OBB centre.
# CCW in (x=east, y=north).
FOOTPRINT = [
    (-6.406, 11.391),
    (-11.328, 6.517),
    (6.406, -11.391),
    (11.328, -6.517),
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_REAR = 0    # 6.93 m, faces NW 315.3 deg — Varney Place
EDGE_SW = 1      # 25.20 m, faces SW 225.3 deg — party wall to 350 Brannan
EDGE_FRONT = 2   # 6.93 m, faces SE 135.3 deg — Brannan Street
EDGE_NE = 3      # 25.20 m, faces NE  45.3 deg — party wall to 362-366 Brannan

FRONT_BLOCK_DEPTH = 8.5   # how far the taller Brannan block reaches back

Z_REAR_DECK = 7.70        # rear roof deck (DataSF LiDAR hgt_median 7.74)
Z_FRONT_DECK = 8.40       # front roof deck (inferred from LiDAR mean 8.52)
Z_PARAPET = 9.00          # front parapet crest (photogrammetric, estimated)
Z_CREST = 9.60            # bay cornice cap = the bbox top

Z_DOOR_TOP = 3.40         # Brannan roll-up head
Z_LINTEL = 3.65
Z_SIGN0, Z_SIGN1 = 3.85, 4.62   # the tenant's sign board
Z_BAY0, Z_BAY1 = 4.70, 8.90     # the canted bay
Z_STORE_TOP = 4.00        # Varney storefront head
Z_HEADER = 4.25           # Varney steel header band

SKIN = 0.10               # painted front skin, proud of the shell
BAY_PROJ = 0.65           # bay projection beyond the skin
PARAPET_T = 0.30

PALETTE_HEX = {
    # Toy_brick, not the browner Toy_rust: this front has to ADVANCE against two
    # pale warehouses, which is the opposite of 380 Brannan's problem two lots
    # away — there Toy_brick had to be abandoned because it merged with the
    # coral band. Recorded in REPORT.md so the block reads as two related but
    # distinct buildings.
    "Toy_brick": "c96f4a",
    "Toy_stone": "d9d2c2",
    "Toy_slate": "6f7883",   # palette extension, precedent artifacts/380-brannan
    "Toy_rust": "a86444",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_roofd": "45454a",
    # Toy_steel doubles as the light roof membrane: real SoMa roofs on this block
    # are a pale gray sheet, and a dark deck made the building read as a black
    # slot from the app's downward camera (first aerial review).
    "Toy_steel": "9aa0a6",
    "Toy_ink": "3a3530",
    "Toy_gold_Glow": "caa64a",
    "Toy_glass_Glow": "6f95b8",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def edge_frame(poly, i):
    """Edge i of a CCW polygon: (origin, length, tangent unit, outward normal)."""
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def poly_edge(i):
    return edge_frame(FOOTPRINT, i)


def offset_polygon(poly, d):
    """Miter offset of the convex CCW footprint; positive d moves outward."""
    npts = len(poly)
    normals = []
    for i in range(npts):
        a, b = poly[i], poly[(i + 1) % npts]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        normals.append((dy / length, -dx / length))
    out = []
    for i in range(npts):
        n1, n2 = normals[i - 1], normals[i]
        v = poly[i]
        det = n1[0] * n2[1] - n1[1] * n2[0]
        if abs(det) < 1e-6:
            out.append((v[0] + n2[0] * d, v[1] + n2[1] * d))
            continue
        c1 = v[0] * n1[0] + v[1] * n1[1] + d
        c2 = v[0] * n2[0] + v[1] * n2[1] + d
        out.append(((c1 * n2[1] - c2 * n1[1]) / det, (c2 * n1[0] - c1 * n2[0]) / det))
    return out


def front_block_polygon():
    """The taller Brannan block: the first FRONT_BLOCK_DEPTH metres of the lot,
    measured back from the Brannan edge. Returned CCW, front edge first."""
    a, length, t, n = poly_edge(EDGE_FRONT)
    b = (a[0] + t[0] * length, a[1] + t[1] * length)
    inward = (-n[0] * FRONT_BLOCK_DEPTH, -n[1] * FRONT_BLOCK_DEPTH)
    return [
        a,
        b,
        (b[0] + inward[0], b[1] + inward[1]),
        (a[0] + inward[0], a[1] + inward[1]),
    ]


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


def bevel(obj, width=0.10, segments=2):
    """Miniature-style edge softening (style bible s.4). Width is capped at a
    third of the object's thinnest dimension: the applied panels here are only
    60-200 mm thick, and a flat bevel on those relies entirely on clamp_overlap,
    which collapses opposing profiles into zero-area slivers."""
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


def wall_panel(name, frame, u_centre, profile, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in a wall plane, extruded outward
    from offset d0 to d1 along that wall's normal. `frame` is (origin, t, n)."""
    a, t, n = frame
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


def edge_wall(edge):
    a, _length, t, n = poly_edge(edge)
    return (a, t, n)


def face_panel(name, edge, u_centre, profile, d0, d1, mat):
    return wall_panel(name, edge_wall(edge), u_centre, profile, d0, d1, mat)


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


def roof_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the roof, aligned to the building's own grid: u runs along the
    Brannan edge from its SW end, v runs INTO the block from that edge."""
    origin, _l, t, n = poly_edge(EDGE_FRONT)
    cx = origin[0] + t[0] * u - n[0] * v
    cy = origin[1] + t[1] * u - n[1] * v
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=math.atan2(t[1], t[0]))


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


def rect_opening(tag, frame, u, w, z0, z1, frame_mat, fill_mat, base_d, glow_mat=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads
    as a border ring around a recessed opening. No booleans, all closed solids."""
    wall_panel(f"{tag}_frame", frame, u, rect_profile(w, z0, z1), 0.0, base_d + 0.06, frame_mat)
    inset = 0.16
    wall_panel(
        f"{tag}_fill",
        frame,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        0.0,
        base_d + 0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.30
        wall_panel(
            f"{tag}_glow",
            frame,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            base_d + 0.10,
            base_d + 0.17,
            glow_mat,
        )


def bay_polygon():
    """Plan polygon of the canted bay, CCW in world XY. Three-sided: a flat face
    on the outside and two angled cheeks returning to the Brannan wall."""
    a, length, t, n = poly_edge(EDGE_FRONT)
    uc = length / 2.0
    half_wall, half_face = 2.15, 1.62
    d_wall, d_face = SKIN, SKIN + BAY_PROJ

    def p(u, d):
        return (a[0] + t[0] * u + n[0] * d, a[1] + t[1] * u + n[1] * d)

    return [
        p(uc - half_wall, d_wall),
        p(uc - half_face, d_face),
        p(uc + half_face, d_face),
        p(uc + half_wall, d_wall),
    ], (half_wall, half_face, d_wall, d_face)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    brick = material("Toy_brick")
    stone = material("Toy_stone")
    slate = material("Toy_slate")
    rust = material("Toy_rust")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    ink = material("Toy_ink")
    gold_glow = material("Toy_gold_Glow")
    glass_glow = material("Toy_glass_Glow")

    front_poly = front_block_polygon()
    _a_f, len_f, _t_f, _n_f = poly_edge(EDGE_FRONT)
    _a_r, len_r, _t_r, _n_r = poly_edge(EDGE_REAR)

    # --- shell: pale party-wall body, its top cap IS the rear roof deck -----
    prism("body", FOOTPRINT, 0.0, Z_REAR_DECK, stone, mat_caps=steel)

    # --- the taller Brannan block ------------------------------------------
    prism("front_block", front_poly, 0.0, Z_FRONT_DECK, stone, mat_caps=steel)
    ring_band("front_parapet", front_poly, Z_FRONT_DECK, Z_PARAPET - 0.14, -PARAPET_T, 0.0, stone)
    ring_band(
        "front_coping", front_poly, Z_PARAPET - 0.14, Z_PARAPET, -PARAPET_T - 0.06, 0.06, stone
    )

    # --- Brannan Street: the terracotta skin, the only saturated surface -----
    front = edge_wall(EDGE_FRONT)
    face_panel(
        "front_skin", EDGE_FRONT, len_f / 2.0, rect_profile(len_f, 0.0, Z_PARAPET), 0.0, SKIN, brick
    )

    # ground floor: a wide roll-up freight door and a narrow pedestrian door
    rect_opening("rollup", front, 2.55, 4.00, 0.0, Z_DOOR_TOP, stone, roofd, SKIN)
    rect_opening("pdoor", front, 5.85, 1.10, 0.0, 2.50, stone, ink, SKIN)
    face_panel(
        "front_lintel",
        EDGE_FRONT,
        len_f / 2.0,
        rect_profile(len_f, Z_DOOR_TOP, Z_LINTEL),
        0.0,
        SKIN + 0.12,
        stone,
    )

    # the sign band, and the lit strip inside it: the night hero
    face_panel(
        "sign_band",
        EDGE_FRONT,
        len_f / 2.0,
        rect_profile(len_f - 0.5, Z_SIGN0, Z_SIGN1),
        0.0,
        SKIN + 0.18,
        ink,
    )
    face_panel(
        "sign_glow",
        EDGE_FRONT,
        len_f / 2.0,
        rect_profile(len_f - 0.9, Z_SIGN0 + 0.12, Z_SIGN1 - 0.22),
        SKIN + 0.14,
        SKIN + 0.24,
        gold_glow,
    )

    # --- the canted bay: the identity cue ------------------------------------
    bpoly, (half_wall, half_face, d_wall, d_face) = bay_polygon()
    prism("bay", bpoly, Z_BAY0, Z_BAY1, brick)
    # a chunky sill slab under it, and the cornice cap that sets the crest
    # A shallow sill: at 0.10 m of overhang it shaded the whole sign band out of
    # the app's downward camera, leaving the hero night glow visible only as two
    # slivers at the ends (first night review).
    prism("bay_sill", offset_polygon(bpoly, 0.04), Z_BAY0 - 0.18, Z_BAY0, stone)
    prism("bay_cap", offset_polygon(bpoly, 0.14), Z_BAY1, Z_CREST, stone)

    # bay glazing: two windows on the flat face, one on each cheek
    face_frame = (bpoly[1], _t_f, _n_f)
    face_len = 2 * half_face
    for i, du in enumerate((-0.85, 0.85)):
        rect_opening(
            f"baywin{i}",
            face_frame,
            face_len / 2.0 + du,
            1.30,
            5.30,
            8.20,
            stone,
            glass,
            0.0,
            glass_glow if i == 0 else None,
        )
    for tag, i0, i1, lit in (("sw", 0, 1, False), ("ne", 2, 3, True)):
        a0, a1 = bpoly[i0], bpoly[i1]
        dx, dy = a1[0] - a0[0], a1[1] - a0[1]
        cl = math.hypot(dx, dy)
        ct = (dx / cl, dy / cl)
        cn = (ct[1], -ct[0])
        rect_opening(
            f"baycheek_{tag}",
            (a0, ct, cn),
            cl / 2.0,
            0.62,
            5.30,
            8.20,
            stone,
            glass,
            0.0,
            glass_glow if lit else None,
        )

    # --- Varney Place: the second front --------------------------------------
    rear = edge_wall(EDGE_REAR)
    face_panel(
        "varney_skin",
        EDGE_REAR,
        len_r / 2.0,
        rect_profile(len_r, 0.0, Z_STORE_TOP),
        0.0,
        SKIN,
        slate,
    )
    rect_opening("v_rollup", rear, 2.15, 3.10, 0.0, 3.55, slate, glass, SKIN)
    rect_opening("v_pdoor", rear, 4.35, 1.00, 0.0, 2.45, slate, ink, SKIN)
    rect_opening("v_glaze0", rear, 5.75, 1.35, 1.05, 3.55, slate, glass, SKIN)
    face_panel(
        "varney_header",
        EDGE_REAR,
        len_r / 2.0,
        rect_profile(len_r, Z_STORE_TOP, Z_HEADER),
        0.0,
        SKIN + 0.16,
        steel,
    )
    # brown horizontal wood siding above, with one shadow reveal at its base
    face_panel(
        "varney_siding",
        EDGE_REAR,
        len_r / 2.0,
        rect_profile(len_r, Z_HEADER, Z_REAR_DECK),
        0.0,
        SKIN + 0.05,
        rust,
    )
    face_panel(
        "varney_reveal",
        EDGE_REAR,
        len_r / 2.0,
        rect_profile(len_r - 0.3, Z_HEADER + 0.30, Z_HEADER + 0.42),
        0.0,
        SKIN + 0.11,
        rust,
    )

    # --- roof: two levels, and the rear one is a used deck --------------------
    # u runs along the Brannan edge from its SW end (0 .. 6.93); v runs back
    # into the block from that edge (0 .. 25.20). The front block is v < 8.5.
    for i, (u, v) in enumerate(((2.30, 11.6), (2.30, 14.6))):
        roof_box(f"skylight_kerb{i}", u, v, Z_REAR_DECK, Z_REAR_DECK + 0.18, 2.10, 1.50, stone)
        roof_box(f"skylight{i}", u, v, Z_REAR_DECK + 0.14, Z_REAR_DECK + 0.38, 1.85, 1.28, glassl)
    roof_box("hvac", 5.20, 13.1, Z_REAR_DECK, Z_REAR_DECK + 0.90, 1.60, 1.20, roofd)
    roof_box("roof_hatch", 4.90, 17.6, Z_REAR_DECK, Z_REAR_DECK + 0.50, 1.20, 1.00, roofd)
    # the front block gets its own bulkhead so its deck is not a blank tray
    roof_box("front_bulkhead", 5.05, 5.10, Z_FRONT_DECK, Z_FRONT_DECK + 0.75, 1.55, 1.90, roofd)
    roof_box("front_vent", 1.85, 6.30, Z_FRONT_DECK, Z_FRONT_DECK + 0.55, 0.85, 0.85, roofd)
    roof_box("vent", 5.35, 15.0, Z_REAR_DECK, Z_REAR_DECK + 0.85, 0.45, 0.45, roofd)

    # the listing's "roof deck/patio": warm decking inside a railing at the
    # Varney end. It is what stops 166 m2 of membrane reading as a dead tray,
    # and it is the only environmental story a building this size can carry.
    RAIL_V = 24.85
    RAIL_BACK = 21.6
    roof_box(
        "roof_deck", len_f / 2.0, (RAIL_V + RAIL_BACK) / 2.0,
        Z_REAR_DECK, Z_REAR_DECK + 0.14, len_f - 0.7, RAIL_V - RAIL_BACK, rust,
    )
    for i in range(2):
        roof_box(
            f"deck_seat{i}", 1.85 + i * 3.2, 23.2, Z_REAR_DECK + 0.14,
            Z_REAR_DECK + 0.55, 1.30, 0.55, stone,
        )
    roof_box(
        "rail_end", len_f / 2.0, RAIL_V, Z_REAR_DECK + 0.86, Z_REAR_DECK + 0.98,
        len_f - 0.7, 0.10, ink,
    )
    for tag, u in (("sw", 0.42), ("ne", len_f - 0.42)):
        roof_box(
            f"rail_{tag}", u, (RAIL_V + RAIL_BACK) / 2.0, Z_REAR_DECK + 0.86, Z_REAR_DECK + 0.98,
            0.10, RAIL_V - RAIL_BACK, ink,
        )
        roof_box(f"railpost_{tag}0", u, RAIL_V, Z_REAR_DECK, Z_REAR_DECK + 0.98, 0.12, 0.12, ink)
        roof_box(
            f"railpost_{tag}1", u, RAIL_BACK, Z_REAR_DECK, Z_REAR_DECK + 0.98, 0.12, 0.12, ink
        )
    roof_box(
        "railpost_mid", len_f / 2.0, RAIL_V, Z_REAR_DECK, Z_REAR_DECK + 0.98, 0.12, 0.12, ink
    )

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.10/2. Applied panels are small and numerous — their frames get a
    # token 1-segment softening and the fills/glow shells none at all.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")):
            continue
        if obj.name.endswith("_frame") or obj.name.startswith(("rail", "varney_reveal")):
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
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    print("[build] anchor lon/lat: -122.3936350 37.7809258 (footprint OBB centre)")
    print("[build] Brannan front heading: 135.3 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "358-brannan.blend")
    glb = os.path.join(out, "358-brannan.glb")
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
