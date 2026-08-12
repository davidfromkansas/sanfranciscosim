"""Deterministic Blender build of the SF-SIM miniature 380 Brannan Street.

    blender -b --python build_380_brannan.py -- [--out DIR]

Writes 380-brannan.blend and 380-brannan.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint OBB centre (anchor lon -122.3940217,
lat 37.7806308), min Z = 0, stair-penthouse crest exactly 12.6 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3775022), a 20.17 x 23.9 m
  near-rectangle with two survey chamfers, sitting at 45.6 deg off the world
  axes like the whole SoMa grid;
* a two-storey unreinforced-brick box: raw Toy_rust masonry on the Varney Place
  rear and both flanks, a painted slate skin on the Brannan Street front only —
  the building's real two-material story;
* the identity feature: a continuous coral band under the parapet cap on the
  Brannan front, returning onto both flanks so it reads from three-quarter
  angles. It does NOT glow — it is a daylight feature, not signage;
* segmental-arched ground-floor openings (the wide freight arch, barred
  windows, the canopied entrance) and tall steel-sash upper windows simplified
  to 6 clean bays per long elevation;
* night state: a restrained scatter of lit upper windows on the front plus the
  entrance canopy underside. Glow surfaces are thin shells proud of the opaque
  glazing (the app renders _Glow in a separate layer that is ~12% alpha by day —
  never author a primary surface as glow);
* a designed roof for the app's downward camera: a parapet ring under a stone
  coping, a five-skylight field, a three-unit mechanical row, a hatch, two vent
  stubs, and the stair penthouse that sets the 12.6 m crest.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF building footprint SF3775022 projected with the app's tangent
# projection and recentred on the OBB centre. CCW. Vertices 0->1 and 2->3 are
# sub-200 mm survey chamfers, kept so the model stays honest to the survey.
FOOTPRINT = [
    (15.615, -1.519),
    (15.493, -1.396),
    (-1.191, 15.507),
    (-1.270, 15.586),
    (-15.394, 1.621),
    (1.213, -15.642),
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_FRONT = 5   # 20.17 m, faces SE 135.6 deg — Brannan Street
EDGE_REAR = 3    # 19.86 m, faces NW 315.3 deg — Varney Place
EDGE_NE = 1      # 23.75 m, faces NE  45.4 deg
EDGE_SW = 4      # 23.95 m, faces SW 226.1 deg

Z_DECK = 11.0        # roof deck / top of the masonry body (LiDAR median 11.02)
Z_PARAPET = 11.9     # parapet crest (inferred: deck + 0.9 m)
Z_CREST = 12.6       # stair-penthouse top = LiDAR max 12.64 -> the bbox top
Z_GROUND_TOP = 4.6   # ground-floor ceiling / string course
Z_BAND0, Z_BAND1 = 10.1, 11.2   # coral band, crosses the body/parapet junction
Z_WIN0, Z_WIN1 = 5.4, 8.4       # upper-floor window band

SKIN = 0.10          # painted front skin, proud of the brick
PARAPET_T = 0.35     # parapet wall thickness

PALETTE_HEX = {
    # Toy_rust, not the palette's Toy_brick, for the masonry: c96f4a sits in the
    # same hue family as the coral band and the first render proved the two
    # merge, which destroys the one accent this building has. a86444 is browner
    # and lets the band read as the only saturated element (style bible s.7).
    "Toy_rust": "a86444",
    "Toy_slate": "6f7883",   # deliberate palette extension — see REPORT.md
    "Toy_stone": "d9d2c2",
    "Toy_coral": "e8735a",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
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


def arch_profile(w, z0, z_spring, rise, seg=4):
    """Closed (u, z) profile: rectangle with a segmental-arched head."""
    a = w / 2.0
    pts = [(-a, z0), (a, z0), (a, z_spring)]
    if rise > 1e-4:
        radius = (a * a + rise * rise) / (2.0 * rise)
        cz = z_spring + rise - radius
        th0 = math.atan2(z_spring - cz, a)
        th1 = math.pi - th0
        for k in range(1, seg):
            th = th0 + (th1 - th0) * k / seg
            pts.append((radius * math.cos(th), cz + radius * math.sin(th)))
    pts.append((-a, z_spring))
    return pts


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
    """Miniature-style edge softening on the chunky solids (style bible s.4).

    The width is capped at a third of the object's thinnest dimension. Many of
    the applied panels here are only 90-220 mm thick, and a flat 0.12 m bevel on
    those relies entirely on clamp_overlap, which collapses opposing profiles
    into zero-area slivers — 132 degenerate triangles and 65 undefined loop
    normals in the first validation run. The remove_doubles/dissolve_degenerate
    pass afterwards sweeps up whatever clamping still pinches shut.
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


def roof_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the roof, aligned to the building's own grid rather than to the
    world axes: u runs along the Brannan edge from its SW end, v runs INTO the
    block (against the outward normal)."""
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


def arched_opening(tag, edge, u, w, z0, z_spring, rise, frame_mat, fill_mat, glow_mat=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads
    as a border ring around a recessed opening. No booleans, all closed solids."""
    face_panel(
        f"{tag}_frame", edge, u, arch_profile(w, z0, z_spring, rise), 0.0, SKIN + 0.06, frame_mat
    )
    inset = 0.20
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        arch_profile(w - 2 * inset, z0 + inset, z_spring, max(rise - 0.08, 0.0)),
        0.0,
        SKIN + 0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.34
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            arch_profile(w - 2 * g, z0 + g, z_spring - 0.12, max(rise - 0.16, 0.0)),
            SKIN + 0.10,
            SKIN + 0.17,
            glow_mat,
        )


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None):
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, SKIN + 0.06, frame_mat)
    inset = 0.18
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        0.0,
        SKIN + 0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.32
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            SKIN + 0.10,
            SKIN + 0.17,
            glow_mat,
        )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    brick = material("Toy_rust")  # masonry walls, parapet, corbel
    slate = material("Toy_slate")
    stone = material("Toy_stone")
    coral = material("Toy_coral")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    ink = material("Toy_ink")
    gglow = material("Toy_glass_Glow")
    tglow = material("Toy_trim_Glow")

    # --- masonry body: brick shell, its top cap IS the roof deck -----------
    prism("body", FOOTPRINT, 0.0, Z_DECK, brick, mat_caps=roofd)

    # --- parapet ring + stone coping ---------------------------------------
    # The coping is what a real brick parapet is finished with, and it is also
    # what stops the whole ring reading as one saturated band from the app's
    # downward camera.
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET - 0.18, -PARAPET_T, 0.0, brick)
    ring_band("coping", FOOTPRINT, Z_PARAPET - 0.18, Z_PARAPET, -PARAPET_T - 0.07, 0.07, stone)

    # --- painted slate skin on the Brannan front only ----------------------
    a_f, len_f, _t_f, _n_f = poly_edge(EDGE_FRONT)
    face_panel(
        "front_skin", EDGE_FRONT, len_f / 2.0, rect_profile(len_f, 0.0, Z_PARAPET), 0.0, SKIN, slate
    )

    # --- the coral band: the whole identity of the building -----------------
    face_panel(
        "coral_band",
        EDGE_FRONT,
        len_f / 2.0,
        rect_profile(len_f, Z_BAND0, Z_BAND1),
        0.0,
        SKIN + 0.09,
        coral,
    )
    # short returns onto both flanks so the band reads from three-quarter views
    for tag, edge, u in (("ne", EDGE_NE, 0.55), ("sw", EDGE_SW, poly_edge(EDGE_SW)[1] - 0.55)):
        face_panel(
            f"coral_return_{tag}",
            edge,
            u,
            rect_profile(1.1, Z_BAND0, Z_BAND1),
            0.0,
            0.09,
            coral,
        )
    # stone cap above the band, front only
    face_panel(
        "front_cap",
        EDGE_FRONT,
        len_f / 2.0,
        rect_profile(len_f, Z_BAND1, Z_PARAPET),
        0.0,
        SKIN + 0.05,
        stone,
    )

    # --- corbelled brick cornice on rear and flanks -------------------------
    for tag, edge in (("rear", EDGE_REAR), ("ne", EDGE_NE), ("sw", EDGE_SW)):
        L = poly_edge(edge)[1]
        # Same rust as the wall: rendered in the lighter Toy_brick this band read
        # as a second coral stripe wrapping the flanks, which stole the front's
        # one identity cue. It relies on its 0.22 m projection and bevel instead.
        face_panel(
            f"corbel_{tag}", edge, L / 2.0, rect_profile(L - 0.4, Z_DECK - 0.55, Z_DECK),
            0.0, 0.22, brick,
        )

    # --- Brannan front, ground floor ---------------------------------------
    # wide arched freight door toward the SW end, then barred arched windows
    # flanking the canopied entrance.
    arched_opening("freight", EDGE_FRONT, 3.2, 4.2, 0.0, 3.3, 0.6, stone, roofd)
    for i, u in enumerate((7.2, 9.6, 14.3, 16.7)):
        arched_opening(f"gwin{i}", EDGE_FRONT, u, 1.6, 0.9, 3.2, 0.5, stone, glass)
    arched_opening("entrance", EDGE_FRONT, 11.9, 1.9, 0.0, 3.0, 0.35, stone, ink)
    # A modest canopy, not the bright shelf the first render produced.
    face_panel(
        "canopy", EDGE_FRONT, 11.9, rect_profile(2.4, 3.30, 3.55), 0.0, SKIN + 0.72, stone
    )
    face_panel(
        "canopy_glow", EDGE_FRONT, 11.9, rect_profile(2.0, 3.31, 3.38), SKIN + 0.22, SKIN + 0.66, tglow
    )

    # string course at the floor line, front only
    face_panel(
        "string", EDGE_FRONT, len_f / 2.0, rect_profile(len_f, Z_GROUND_TOP, Z_GROUND_TOP + 0.2),
        0.0, SKIN + 0.12, stone,
    )

    # --- Brannan front, upper floor: 6 bays, a few lit at night -------------
    LIT = {1, 2, 4}
    for i in range(6):
        u = 2.35 + i * 3.09
        rect_opening(
            f"fwin{i}", EDGE_FRONT, u, 1.85, Z_WIN0, Z_WIN1, ink, glass,
            gglow if i in LIT else None,
        )

    # --- Varney Place rear: raw brick, segmental heads both floors ----------
    len_r = poly_edge(EDGE_REAR)[1]
    arched_opening("rolldoor", EDGE_REAR, 3.0, 3.4, 0.0, 3.2, 0.55, brick, roofd)
    for i, u in enumerate((7.4, 10.5, 13.6, 16.7)):
        arched_opening(f"rgwin{i}", EDGE_REAR, u, 1.5, 1.0, 3.2, 0.5, brick, glass)
    for i in range(6):
        u = 2.1 + i * 3.13
        arched_opening(f"rwin{i}", EDGE_REAR, u, 1.5, Z_WIN0, Z_WIN1 - 0.45, 0.45, brick, glass)

    # --- flanks: sparse arched windows, no invented grid --------------------
    for tag, edge in (("ne", EDGE_NE), ("sw", EDGE_SW)):
        L = poly_edge(edge)[1]
        for i in range(4):
            u = 4.0 + i * 5.2
            if u > L - 3.0:
                continue
            arched_opening(f"{tag}win{i}", edge, u, 1.4, Z_WIN0, Z_WIN1 - 0.6, 0.4, brick, glass)
            arched_opening(f"{tag}gwin{i}", edge, u, 1.4, 1.1, 3.2, 0.45, brick, glass)

    # --- fire escape on the Brannan front -----------------------------------
    # A chunky balcony, not a wireframe: the first render's thin bars read as
    # noise over the window behind them (style bible s.4, s.21).
    # Sat at 5.00-5.75 it crossed the bottom of the window behind it and read as
    # a dark smudge; hung at the sill it reads as what it is.
    fe_u = 2.35 + 3 * 3.09
    face_panel("fe_deck", EDGE_FRONT, fe_u, rect_profile(2.8, 5.35, 5.53), SKIN, SKIN + 1.05, ink)
    face_panel(
        "fe_rail", EDGE_FRONT, fe_u, rect_profile(2.8, 5.53, 6.15), SKIN + 0.88, SKIN + 1.05, ink
    )

    # --- roof: the surface the app's camera sees most ------------------------
    # u runs along the Brannan edge from its SW end, v goes back into the block.
    # Three clusters spread across the whole deck — a skylight field over the
    # second floor, a mechanical row along the NE flank, and the penthouse group
    # at the back — so the roof never reads as an empty tray (style bible s.10).
    for i, (u, v) in enumerate(((5.0, 6.6), (8.6, 6.6), (12.2, 6.6), (6.8, 11.2), (10.4, 11.2))):
        roof_box(f"skylight_kerb{i}", u, v, Z_DECK, Z_DECK + 0.22, 2.8, 2.0, stone)
        roof_box(f"skylight{i}", u, v, Z_DECK + 0.18, Z_DECK + 0.45, 2.5, 1.7, glassl)
    roof_box("hvac_a", 16.0, 7.4, Z_DECK, Z_DECK + 1.0, 2.2, 1.6, steel)
    roof_box("hvac_b", 16.2, 10.4, Z_DECK, Z_DECK + 0.8, 1.6, 1.2, steel)
    roof_box("hvac_c", 14.4, 13.2, Z_DECK, Z_DECK + 0.9, 1.4, 1.4, steel)
    roof_box("duct", 15.4, 8.9, Z_DECK + 0.25, Z_DECK + 0.55, 0.7, 1.9, steel)
    roof_box("penthouse", 5.2, 19.4, Z_DECK, Z_CREST, 3.6, 2.8, roofd)
    roof_box("roof_hatch", 10.6, 17.2, Z_DECK, Z_DECK + 0.5, 1.5, 1.2, roofd)
    roof_box("vent_a", 13.6, 19.8, Z_DECK, Z_DECK + 1.1, 0.6, 0.6, steel)
    roof_box("vent_b", 15.6, 18.0, Z_DECK, Z_DECK + 0.9, 0.5, 0.5, steel)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. Applied window panels are small and numerous — their frames
    # get a token 1-segment softening and the fills/glow shells none at all,
    # which is what keeps this under the 9,000-triangle cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")):
            continue
        if obj.name.endswith("_frame"):
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
    print("[build] anchor lon/lat: -122.3940217 37.7806308 (footprint OBB centre)")
    print("[build] Brannan front heading: 135.6 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "380-brannan.blend")
    glb = os.path.join(out, "380-brannan.glb")
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
