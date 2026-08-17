"""Deterministic Blender build of the SF-SIM miniature 140 South Park Street.

    blender -b --python build_140_south_park.py -- [--out DIR]

Writes 140-south-park.blend and 140-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading - the
loader applies no rotation. Origin = footprint OBB centre (anchor
lon -122.3947379, lat 37.7814643), min Z = 0, cornice crest exactly 10.68 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3775064), a 6.84 x 29.81 m bar at
  45 deg off the world axes, built as ONE mass. The survey shows a single
  near-rectangular prism; there is no wing, no step and no rear block, and
  inventing one would be a lie about the type;
* a 4.4 : 1 stick. This aspect ratio IS the silhouette from the app's downward
  camera - a long dark bar in a row of broad pale blocks - and the whole reason
  the building is worth an asset. Nothing here may fatten it;
* the identity, carried hard: the bracketed Italianate cornice on the 6.84 m
  South Park front, the only ornament on the building and also its crest. Nine
  modillion brackets in Toy_ink under a projecting Toy_olive crown, enlarged to
  1.78 m of assembly against ~1.2 m on the photograph so the bracket row
  survives at thumbnail size (style bible s.9, logged in REPORT.md);
* horizontal lap siding, read as six shallow shadow lines per elevation rather
  than as modelled boards. The 2009 DPR form singles this building out as the
  district's only WOOD FRAME industrial building, so the siding is the material
  argument and it has to be visible;
* NO parapet. A 2018 permit correction records "no existing parapet" in as many
  words, so the flanks and rear get a 0.15 m fascia at the deck and nothing
  more. The cornice alone rises above the roof;
* a dark desaturated gray-green body (Toy_olive). 150 next door is white over
  black, 155 is white, 135 is dark brick: this is a value and hue slot no
  neighbour on the north-west rim holds, and it is what the building is;
* the party wall on the south-west flank is BLANK - 150 South Park is hard
  against it at a 0.00 m gap - while the north-east flank is a real elevation
  onto a ~6 m side passage and gets its siding, two high service windows and a
  downpipe;
* night state: the ground-floor shopfront and its transom band are the hero glow
  - warm gold, the one lit thing at the dark west tip of the oval - plus the
  three upper windows cool and lower in area. Nothing on the flanks, rear or
  roof. Glow surfaces are thin shells proud of the opaque glazing (the app
  renders _Glow in a separate layer that is ~12% alpha by day - never author a
  primary surface as glow);
* a roof the 2010 LiDAR proves was bare: dark deck, a low condenser pair from
  the 2019 VRF permit, a hatch and a vent, all kept under the cornice crest.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# The lot's own frame, from the minimum-area oriented bounding box of the DataSF
# footprint SF3775064: +u runs across the lot to the NORTH-EAST (toward the side
# passage and 136 South Park), +v runs along it to the NORTH-WEST (toward the
# rear and the Bryant Street block, i.e. AWAY from South Park Street).
ROT_DEG = 45.0

# Footprint in (u, v) metres, recentred on the OBB centre = the anchor. CCW and
# convex; these four points are the DataSF ring with its two collinear vertices
# on the party-wall side dropped (they lie on the v0-v3 line to within 5 mm).
# Shoelace area of the result is 200.77 m2 against DataSF's 200.8 m2.
FOOT_UV = [
    (-3.325, 14.900),   # rear, south-west  (DataSF vertex 5)
    (-3.419, -14.905),  # front, south-west (DataSF vertex 4)
    (3.422, -14.904),   # front, north-east (DataSF vertex 3)
    (3.327, 14.812),    # rear, north-east  (DataSF vertex 0)
]

# Edge index -> elevation. Outward normals verified against the survey.
E_SW = 0      # 29.81 m party wall, faces SW - 150 South Park, 0.00 m gap. BLANK
E_FRONT = 1   # 6.84 m, faces SE 135.0 deg - South Park Street. The hero
E_NE = 2      # 29.72 m, faces NE - the side passage. A real elevation
E_REAR = 3    # 6.65 m, faces NW - the Bryant Street block, ~6 m away

Z_DOOR_TOP = 3.35     # shopfront door / display head
Z_TRAN_A, Z_TRAN_B = 3.50, 4.20   # transom band
Z_SHOP_TOP = 4.35     # storefront head / second-floor line
Z_BELT_A, Z_BELT_B = 4.35, 5.20   # panelled belt band between the floors
Z_WIN_A, Z_WIN_B = 5.60, 8.55     # the three upper windows
Z_FRIEZE_A = 8.90     # cornice assembly starts
Z_BRACK_A, Z_BRACK_B = 9.25, 9.72  # the modillion bracket row
Z_CROWN_B = 10.14     # projecting crown moulding top
Z_CREST = 10.68       # cornice cap crest -> the bbox top, must land exactly
Z_DECK = 9.85         # roof deck (LiDAR modal height cell, 989 cm)
Z_FASCIA = 10.00      # thin roof-edge trim on the two flanks and the rear

SKIN = 0.10           # applied panels stand proud of the wall by this much
FRONT_W = 6.840       # measured length of E_FRONT
NE_W = 29.723         # measured length of E_NE
REAR_W = 6.653        # measured length of E_REAR

PALETTE_HEX = {
    # Deliberate palette extension, documented as a WARN in REPORT.md exactly as
    # 155 South Park's Toy_peach and 380 Brannan's Toy_slate were. The building
    # is a dark desaturated gray-green; Toy_slate (6f7883) is a blue-gray and
    # too light, Toy_pine (3f6b4f) is a saturated green and far too strong for a
    # whole wall. Neither is this building.
    "Toy_olive": "5f655c",
    "Toy_ink": "3a3530",
    "Toy_oak": "c08e50",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_red": "c4453c",
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

_C = math.cos(math.radians(ROT_DEG))
_S = math.sin(math.radians(ROT_DEG))


def to_world(u, v):
    """Lot frame -> world (east, north) metres, both centred on the anchor."""
    return (u * _C - v * _S, u * _S + v * _C)


FOOT = [to_world(u, v) for u, v in FOOT_UV]

# --------------------------------------------------------------- 2D helpers


def poly_edge(poly, i):
    """Edge i of poly: (origin, length, tangent unit, outward normal)."""
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def offset_polygon(poly, d):
    """Miter offset of a convex CCW footprint; positive d moves outward."""
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
    """Miniature-style edge softening (style bible s.4). The width is capped at
    a third of the object's thinnest dimension: the applied panels here are
    60-440 mm thick and a flat 0.12 m bevel on those collapses opposing profiles
    into zero-area slivers even with clamp_overlap. The remove_doubles /
    dissolve_degenerate pass sweeps up whatever clamping still pinches shut."""
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


def face_panel(name, poly, edge, u_centre, profile, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in the plane of wall `edge`,
    extruded outward from offset d0 to d1 along that wall's normal."""
    a, _length, t, n = poly_edge(poly, edge)
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


def lot_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the lot's own grid: centre at (u, v), sides su across the lot and
    sv along it, rotated with the building."""
    cx, cy = to_world(u, v)
    yaw = math.atan2(_S, _C)
    c, s = math.cos(yaw), math.sin(yaw)
    corners = []
    for lx, ly in ((-su / 2, -sv / 2), (su / 2, -sv / 2), (su / 2, sv / 2), (-su / 2, sv / 2)):
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


def rect_opening(tag, poly, edge, u, w, z0, z1, frame_mat, fill_mat, base=0.0, glow_mat=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads
    as a border ring around a recessed opening. No booleans, all closed solids."""
    face_panel(f"{tag}_frame", poly, edge, u, rect_profile(w, z0, z1), 0.0, base + 0.06, frame_mat)
    inset = 0.16
    face_panel(
        f"{tag}_fill",
        poly,
        edge,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        0.0,
        base + 0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.28
        face_panel(
            f"{tag}_glow",
            poly,
            edge,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            base + 0.10,
            base + 0.17,
            glow_mat,
        )


def siding(tag, poly, edge, z_from, z_to, count, mat, width=None, base=0.0):
    """Horizontal lap-siding shadow lines. Modelling boards on a 29.7 m flank
    would cost thousands of triangles for a detail that is sub-pixel at the
    app's camera; six proud strips per elevation carry the same read at 12
    triangles each. This is the material argument of the whole asset - the 2009
    DPR form singles this building out as the district's only WOOD FRAME
    industrial building - so it may be cheap but it may not be dropped."""
    length = poly_edge(poly, edge)[1]
    w = length if width is None else width
    for i in range(count):
        z = z_from + (z_to - z_from) * (i + 0.5) / count
        face_panel(
            f"{tag}_lap{i}",
            poly,
            edge,
            length / 2.0,
            rect_profile(w, z, z + 0.09),
            base,
            base + 0.06,
            mat,
        )


def upper_window(tag, u, w, ink, glass, glow_mat=None):
    """One of the three tall multi-pane lights on the South Park front: an ink
    frame, a Toy_glass fill, and a 2 x 3 grid of thin ink mullions. The grid is
    what says 'industrial sash' rather than 'picture window' - three real rows
    of openings would cost five times as much and read identically."""
    z0, z1 = Z_WIN_A, Z_WIN_B
    face_panel(f"{tag}_frame", FOOT, E_FRONT, u, rect_profile(w, z0, z1), 0.0, SKIN + 0.08, ink)
    face_panel(
        f"{tag}_fill",
        FOOT,
        E_FRONT,
        u,
        rect_profile(w - 0.30, z0 + 0.15, z1 - 0.15),
        0.0,
        SKIN + 0.15,
        glass,
    )
    # two horizontal transom bars (three rows of panes)
    for i in (1, 2):
        z = z0 + (z1 - z0) * i / 3.0
        face_panel(
            f"{tag}_bar{i}",
            FOOT,
            E_FRONT,
            u,
            rect_profile(w - 0.30, z - 0.05, z + 0.05),
            0.0,
            SKIN + 0.19,
            ink,
        )
    # vertical mullions: two on the wide centre light, one on the narrow ones
    cols = 3 if w > 1.7 else 2
    for i in range(1, cols):
        du = (w - 0.30) * (i / cols - 0.5)
        face_panel(
            f"{tag}_mul{i}",
            FOOT,
            E_FRONT,
            u + du,
            rect_profile(0.09, z0 + 0.15, z1 - 0.15),
            0.0,
            SKIN + 0.19,
            ink,
        )
    if glow_mat is not None:
        face_panel(
            f"{tag}_glow",
            FOOT,
            E_FRONT,
            u,
            rect_profile(w - 0.52, z0 + 0.32, z1 - 0.32),
            SKIN + 0.12,
            SKIN + 0.18,
            glow_mat,
        )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    olive = material("Toy_olive")
    ink = material("Toy_ink")
    oak = material("Toy_oak")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    red = material("Toy_red")
    gglow = material("Toy_gold_Glow")
    wglow = material("Toy_glass_Glow")

    # --- the one mass --------------------------------------------------------
    prism("body", FOOT, 0.0, Z_DECK, olive, mat_caps=roofd)

    # --- roof edge: a fascia, NOT a parapet ----------------------------------
    # The 2018 permit correction records "no existing parapet" in as many words,
    # so this is 0.15 m of trim standing on the wall line and nothing more. The
    # cornice on E_FRONT is the only thing that rises above the deck.
    ring_band("fascia", FOOT, Z_DECK, Z_FASCIA, -0.16, 0.05, olive)

    # =========================== SOUTH PARK FRONT ============================
    # u runs from the south-west corner (hard against 150 South Park) to the
    # north-east corner (the side passage), matching the Jan 2025 photograph
    # read left to right from the street.

    # lap siding on the upper wall only; the shopfront below is flush timber
    siding("fr", FOOT, E_FRONT, Z_BELT_B + 0.15, Z_FRIEZE_A - 0.20, 6, olive)

    # --- ground floor: the near-black shopfront ------------------------------
    face_panel(
        "shopfront", FOOT, E_FRONT, FRONT_W / 2.0, rect_profile(FRONT_W, 0.0, Z_SHOP_TOP), 0.0, SKIN, ink
    )
    rect_opening(
        "display", FOOT, E_FRONT, 1.75, 2.55, 1.05, Z_DOOR_TOP, ink, glass, base=SKIN, glow_mat=gglow
    )
    # The wood double door: the single warm, saturated thing on the building.
    face_panel(
        "entry_frame", FOOT, E_FRONT, 4.15, rect_profile(1.60, 0.0, Z_DOOR_TOP), 0.0, SKIN + 0.06, ink
    )
    face_panel(
        "entry_leaves", FOOT, E_FRONT, 4.15, rect_profile(1.36, 0.0, Z_DOOR_TOP - 0.10), 0.0, SKIN + 0.13, oak
    )
    face_panel(
        "entry_mullion", FOOT, E_FRONT, 4.15, rect_profile(0.09, 0.0, Z_DOOR_TOP - 0.10), 0.0, SKIN + 0.17, ink
    )
    face_panel(
        "entry_light", FOOT, E_FRONT, 4.15, rect_profile(1.06, 1.35, Z_DOOR_TOP - 0.30), 0.0, SKIN + 0.17, glass
    )
    face_panel(
        "entry_glow", FOOT, E_FRONT, 4.15, rect_profile(0.82, 1.55, Z_DOOR_TOP - 0.48), SKIN + 0.14, SKIN + 0.20, gglow
    )
    rect_opening("service", FOOT, E_FRONT, 5.72, 0.90, 0.0, 3.20, ink, roofd, base=SKIN)
    # Transom band across the full frontage, over everything below it.
    # Toy_glass, not Toy_glassl: the first aerial put a bright blue bar across
    # the whole frontage and it read as a light fixture, not as glazing. The
    # transom in the photograph is the same dark glass as everything else in the
    # shopfront; the four mullions are what give it its rhythm.
    face_panel(
        "transom", FOOT, E_FRONT, FRONT_W / 2.0, rect_profile(FRONT_W - 0.36, Z_TRAN_A, Z_TRAN_B),
        0.0, SKIN + 0.08, glass,
    )
    for i in range(1, 4):
        face_panel(
            f"transom_mul{i}", FOOT, E_FRONT, 0.18 + (FRONT_W - 0.36) * i / 4.0,
            rect_profile(0.09, Z_TRAN_A, Z_TRAN_B), 0.0, SKIN + 0.12, ink,
        )
    face_panel(
        "transom_glow", FOOT, E_FRONT, FRONT_W / 2.0, rect_profile(FRONT_W - 0.86, Z_TRAN_A + 0.14, Z_TRAN_B - 0.14),
        SKIN + 0.05, SKIN + 0.12, gglow,
    )
    # Fire department connection: the only saturated accent that is not the door.
    face_panel("fdc", FOOT, E_FRONT, 0.42, rect_profile(0.26, 1.05, 1.42), 0.0, SKIN + 0.22, red)

    # --- panelled belt band between the floors -------------------------------
    face_panel(
        "belt", FOOT, E_FRONT, FRONT_W / 2.0, rect_profile(FRONT_W, Z_BELT_A, Z_BELT_B), 0.0, SKIN + 0.10, olive
    )
    face_panel(
        "belt_reveal", FOOT, E_FRONT, FRONT_W / 2.0, rect_profile(FRONT_W, Z_BELT_A, Z_BELT_A + 0.10),
        SKIN + 0.06, SKIN + 0.13, ink,
    )

    # --- the three tall upper lights -----------------------------------------
    upper_window("w_sw", 1.375, 1.55, ink, glass, glow_mat=wglow)
    upper_window("w_c", 3.425, 1.95, ink, glass, glow_mat=wglow)
    # No glow on the north-east light: at night a two-storey office with every
    # window lit reads as a render, not as a building. The gold shopfront is the
    # hero and it should not be competing with three cool lights above it.
    upper_window("w_ne", 5.475, 1.55, ink, glass)

    # --- the bracketed cornice: the one piece of ornament, and the crest ------
    face_panel(
        "frieze", FOOT, E_FRONT, FRONT_W / 2.0, rect_profile(FRONT_W, Z_FRIEZE_A, Z_BRACK_A), 0.0, SKIN + 0.14, olive
    )
    for i in range(9):
        u = FRONT_W * (i + 0.5) / 9.0
        face_panel(
            f"bracket{i}", FOOT, E_FRONT, u, rect_profile(0.24, Z_BRACK_A, Z_BRACK_B), 0.0, SKIN + 0.34, ink
        )
    face_panel(
        "crown", FOOT, E_FRONT, FRONT_W / 2.0, rect_profile(FRONT_W, Z_BRACK_B, Z_CROWN_B), 0.0, SKIN + 0.44, olive
    )
    # The cap band. This sets the bounding-box top and must land exactly on
    # Z_CREST = 10.68 m, the DataSF LiDAR maximum.
    face_panel(
        "cornice_cap", FOOT, E_FRONT, FRONT_W / 2.0, rect_profile(FRONT_W, Z_CROWN_B, Z_CREST), 0.0, SKIN + 0.30, olive
    )

    # ======================= NORTH-EAST SIDE PASSAGE =========================
    # A real elevation: ~6 m of open passage runs the full 29.7 m depth of the
    # lot, so the app's camera reads this wall end to end.
    siding("ne", FOOT, E_NE, 1.10, Z_DECK - 0.45, 6, olive)
    for i, u in enumerate((8.0, 20.0)):
        rect_opening(f"ne_win{i}", FOOT, E_NE, u, 0.95, 6.40, 7.60, ink, glass)
    face_panel("ne_downpipe", FOOT, E_NE, 3.00, rect_profile(0.18, 0.0, Z_DECK), 0.0, 0.11, steel)

    # ============================ NORTH-WEST REAR ============================
    # Not observed by any source consulted; reconstructed as a blunt service
    # face on the strength of the type (REFERENCE.md s.4, plan s.2.15).
    siding("rr", FOOT, E_REAR, 1.10, Z_DECK - 0.45, 6, olive)
    rect_opening("rear_door", FOOT, E_REAR, 1.60, 1.05, 0.0, 2.40, ink, roofd)
    rect_opening("rear_win", FOOT, E_REAR, 4.20, 1.00, 5.90, 7.30, ink, glass)

    # ========================= SOUTH-WEST PARTY WALL =========================
    # Deliberately empty. 150 South Park's own facade runs hard against this
    # wall at a 0.00 m gap; nothing on it is visible from anywhere, and every
    # triangle spent here would be a triangle taken off the cornice.

    # ================================= ROOF ==================================
    # The 2010 LiDAR is nearly uniform across all 200 m2 (modal 9.89 m, median
    # 9.88 m), which proves the roof was BARE when it was flown. The only things
    # that go on it are the ones a permit accounts for.
    # Spread along the 29.8 m rather than bunched: the first top view put every
    # object in one 6 m band and left the front 12 m of deck dead.
    lot_box("cond_plinth", 0.00, 0.90, Z_DECK, Z_DECK + 0.10, 2.10, 3.30, roofd)
    lot_box("cond_a", 0.00, 0.00, Z_DECK + 0.08, Z_DECK + 0.62, 1.45, 0.85, steel)  # 2019 VRF
    lot_box("cond_b", 0.00, 1.80, Z_DECK + 0.08, Z_DECK + 0.62, 1.45, 0.85, steel)
    lot_box("roof_hatch", -1.00, 11.00, Z_DECK, Z_DECK + 0.35, 1.20, 0.90, roofd)
    lot_box("roof_vent", 1.55, -11.00, Z_DECK, Z_DECK + 0.72, 0.34, 0.34, steel)
    # Two flush skylights over the rear half. INFERRED FROM THE TYPE, not
    # measured: a 29.8 x 6.8 m loft with window walls only at its two short ends
    # has no daylight at all in its middle 20 m, and every South Park building of
    # this depth solves that from above. Their 0.18 m kerbs sit inside the 2010
    # LiDAR's noise (deck std 1.11 m over 0.5 m cells) so the survey neither
    # confirms nor rules them out - logged as an inference in REFERENCE.md s.4.
    for tag, v in (("a", -6.00), ("b", 6.00)):
        lot_box(f"skylight_{tag}_kerb", 0.15, v, Z_DECK, Z_DECK + 0.18, 2.30, 1.70, roofd)
        lot_box(f"skylight_{tag}", 0.15, v, Z_DECK + 0.14, Z_DECK + 0.34, 2.00, 1.42, glassl)

    # Bevel budget: the one chunky mass carries the miniature read, so it gets
    # the full 0.12/2. Applied panels are small and numerous - frames get a
    # token 1-segment softening and the fills, glow shells, mullions and siding
    # lines none at all, which is what keeps this well under the 7,000 cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if (
            name.endswith(("_fill", "_glow", "_light", "_leaves"))
            or "_lap" in name
            or "_mul" in name
            or "_bar" in name
            or name.startswith("bracket")
        ):
            continue
        if name.endswith(("_frame", "_mullion", "_reveal")) or name in {"fdc", "ne_downpipe"}:
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
    print("[build] anchor lon/lat: -122.3947379 37.7814643 (DataSF footprint OBB centre)")
    print("[build] South Park front heading: 135.0 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "140-south-park.blend")
    glb = os.path.join(out, "140-south-park.glb")
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
