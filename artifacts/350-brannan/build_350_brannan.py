"""Deterministic Blender build of the SF-SIM miniature 350 Brannan Street.

    blender -b --python build_350_brannan.py -- [--out DIR]

Writes 350-brannan.blend and 350-brannan.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint centroid (anchor lon -122.3935234,
lat 37.7810229), min Z = 0, roof-penthouse crest exactly 13.85 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3775016), a 21.60 x 24.22 m
  near-rectangle with two survey jogs, sitting at ~45.3 deg off the world axes
  like the whole SoMa grid, covering its entire lot;
* a three-storey WHITE PAINTED CONCRETE box (assessor construction class C) —
  deliberately not the brick of its neighbour 380 Brannan, which is the single
  easiest mistake to make on this block;
* the identity feature: TWO round-arched portals bookending the Brannan Street
  ground floor, with pale cast-stone surrounds, framing a colonnade of five
  pier-separated storefront bays;
* three finished elevations (Brannan SE, Jack London Alley NE, Varney Place NW)
  and one blind southwest party wall — the real asymmetry of a full-lot corner
  building, and why the leasing copy sells "window lines on 3 sides";
* two upper floors of large steel-sash industrial windows, the top floor taller
  than the middle one, which is what makes them read as industrial sash;
* the black zig-zag fire escape on the Jack London Alley elevation;
* night state: the two arched portals lit as entrances plus a restrained scatter
  of lit upper windows. Glow surfaces are thin shells proud of the opaque
  glazing (the app renders _Glow in a separate layer that is ~12% alpha by day —
  never author a primary surface as glow);
* a designed roof for the app's downward camera: a LIGHT membrane deck (the real
  roof is a bright reflective membrane — separation comes from the lighter cap
  and the darker clutter, not from faking a dark deck), the big raised penthouse
  that sets the 13.85 m crest, a skylight row, a mechanical pair and a hatch.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF building footprint SF3775016 projected with the app's tangent
# projection and recentred on the footprint centroid. CCW. Edges 3 and 5 are
# 0.42 m and 1.02 m survey jogs, kept so the model stays honest to the survey.
FOOTPRINT = [
    (1.094, -15.780),
    (16.574, -0.721),
    (-0.716, 16.241),
    (-16.502, 0.922),
    (-16.205, 0.630),
    (1.048, -16.797),
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_FRONT = 0   # 21.60 m, faces SE 135.8 deg — Brannan Street
EDGE_NE = 1      # 24.22 m, faces NE  44.5 deg — Jack London Alley
EDGE_NW = 2      # 22.00 m, faces NW 315.9 deg — Varney Place
EDGE_SW = 4      # 24.52 m, faces SW 225.3 deg — party wall, blind

Z_DECK = 12.02       # roof deck / top of the body (LiDAR median 12.02)
Z_PARAPET = 12.90    # parapet crest (inferred: deck + 0.88 m)
Z_CREST = 13.85      # roof penthouse top = LiDAR max 13.85 -> the bbox top
Z_G_TOP = 4.40       # ground-floor ceiling / string course
Z_W2A, Z_W2B = 4.90, 7.90    # middle-floor window band
Z_W3A, Z_W3B = 8.20, 11.40   # top-floor window band (taller = industrial sash)

SKIN = 0.10          # applied-panel standoff from the wall plane
PARAPET_T = 0.35     # parapet wall thickness

PALETTE_HEX = {
    # The painted body. Toy_cream is the palette's warm off-white; the real
    # paint reads warm white in sun and cool light grey in shade.
    "Toy_cream": "f2ede3",
    "Toy_trim": "f3efe6",    # arch surrounds, string course, parapet cap
    "Toy_stone": "d9d2c2",   # roof membrane — light, as the real one is
    "Toy_glass": "2a4d73",   # steel-sash upper windows
    "Toy_glassl": "6f95b8",  # ground-floor storefronts, skylights
    "Toy_roofd": "45454a",   # service doors
    "Toy_steel": "9aa0a6",   # mechanical blocks
    "Toy_ink": "3a3530",     # fire escape, arch reveals, window frames
    # Glow colours are the LIT appearance, not the day colour: a night window
    # that glows in its own dark navy reads as a hole. Same lesson as 380.
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


def arch_profile(w, z0, z_spring, rise, seg=6):
    """Closed (u, z) profile: rectangle with a round-arched head.

    These arches are the building's identity, so they carry 6 segments where the
    segmental heads on 380 Brannan needed 4 — a shallow segmental arc survives
    coarse faceting, a near-semicircular one does not.
    """
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

    The width is capped at a third of the object's thinnest dimension: the
    applied panels here are only 90-230 mm thick, and a flat 0.12 m bevel on
    those relies entirely on clamp_overlap, which collapses opposing profiles
    into zero-area slivers. The remove_doubles/dissolve_degenerate pass
    afterwards sweeps up whatever clamping still pinches shut.
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
        f"{tag}_frame", edge, u, arch_profile(w, z0, z_spring, rise), 0.0, SKIN + 0.08, frame_mat
    )
    inset = 0.30
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        arch_profile(w - 2 * inset, z0 + inset, z_spring, max(rise - 0.10, 0.0)),
        0.0,
        SKIN + 0.20,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.52
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            arch_profile(w - 2 * g, z0 + g, z_spring - 0.16, max(rise - 0.22, 0.0)),
            SKIN + 0.17,
            SKIN + 0.24,
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


# Upper-floor bay centres per elevation, and which of them are lit at night.
# Five bays per finished elevation is the dossier's regularisation of the real
# window rhythm (plan 2.6); the party wall gets none.
UPPER_BAYS = {
    EDGE_FRONT: [2.60, 6.70, 10.80, 14.90, 19.00],
    EDGE_NE: [3.00, 7.55, 12.10, 16.65, 21.20],
    EDGE_NW: [2.70, 6.85, 11.00, 15.15, 19.30],
}
# Restrained: six lit windows across two floors and two elevations.
LIT_MID = {EDGE_FRONT: {1, 3}, EDGE_NE: {2}, EDGE_NW: set()}
LIT_TOP = {EDGE_FRONT: {0}, EDGE_NE: {1, 4}, EDGE_NW: set()}


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    cream = material("Toy_cream")
    trim = material("Toy_trim")
    stone = material("Toy_stone")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    ink = material("Toy_ink")
    gglow = material("Toy_glass_Glow")
    tglow = material("Toy_trim_Glow")

    # --- painted concrete body; its top cap IS the roof membrane ------------
    prism("body", FOOTPRINT, 0.0, Z_DECK, cream, mat_caps=stone)

    # --- parapet ring + light coping ---------------------------------------
    # The real membrane is bright, so the ring is read from the CAP being
    # lighter than the deck and the clutter being darker — not from a faked
    # dark deck (plan 2.9).
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET - 0.16, -PARAPET_T, 0.0, cream)
    ring_band("coping", FOOTPRINT, Z_PARAPET - 0.16, Z_PARAPET, -PARAPET_T - 0.07, 0.07, trim)

    len_f = poly_edge(EDGE_FRONT)[1]
    len_ne = poly_edge(EDGE_NE)[1]
    len_nw = poly_edge(EDGE_NW)[1]

    # --- THE IDENTITY: two round-arched portals on Brannan ------------------
    # One at each end of the ground floor, cast-stone surround, lit at night.
    # Widened from the survey rhythm on purpose: the arches are the one place
    # this asset spends semantic exaggeration (plan 2.6), and at the app's
    # camera a true-width arch is four pixels of nothing.
    for tag, u in (("portal_sw", 2.40), ("portal_ne", 19.20)):
        arched_opening(tag, EDGE_FRONT, u, 3.20, 0.0, 3.00, 1.25, stone, ink, tglow)

    # --- Brannan ground floor: five pier-framed storefront bays --------------
    for i in range(5):
        u = 5.36 + i * 2.72
        rect_opening(f"sfront{i}", EDGE_FRONT, u, 2.10, 0.90, 3.60, ink, glassl)

    # --- Jack London Alley + Varney Place ground floors ---------------------
    # Five plain bays each, plus one service door apiece. The alley door is the
    # accessible entry the 2008 permits designated (plan 2.4).
    for i in range(5):
        u = 3.40 + i * 4.35
        if i == 0:
            rect_opening(f"nedoor{i}", EDGE_NE, u, 2.40, 0.0, 3.30, ink, roofd)
        else:
            rect_opening(f"negrd{i}", EDGE_NE, u, 2.40, 0.90, 3.60, ink, glassl)
    for i in range(5):
        u = 3.20 + i * 3.95
        if i == 4:
            rect_opening(f"nwdoor{i}", EDGE_NW, u, 2.40, 0.0, 3.30, ink, roofd)
        else:
            rect_opening(f"nwgrd{i}", EDGE_NW, u, 2.40, 0.90, 3.60, ink, glassl)

    # --- string course at the ground-floor ceiling, finished sides only ------
    for tag, edge, L in (("f", EDGE_FRONT, len_f), ("ne", EDGE_NE, len_ne), ("nw", EDGE_NW, len_nw)):
        face_panel(
            f"string_{tag}", edge, L / 2.0, rect_profile(L - 0.3, Z_G_TOP, Z_G_TOP + 0.18),
            0.0, SKIN + 0.12, trim,
        )

    # --- two upper floors of steel-sash industrial windows ------------------
    # The top floor is 3.2 m where the middle is 3.0 m. That difference is what
    # makes the sash read as industrial rather than as office ribbon glazing.
    for edge, bays in UPPER_BAYS.items():
        tag = {EDGE_FRONT: "f", EDGE_NE: "ne", EDGE_NW: "nw"}[edge]
        for i, u in enumerate(bays):
            rect_opening(
                f"{tag}mid{i}", edge, u, 2.60, Z_W2A, Z_W2B, ink, glass,
                gglow if i in LIT_MID[edge] else None,
            )
            rect_opening(
                f"{tag}top{i}", edge, u, 2.60, Z_W3A, Z_W3B, ink, glass,
                gglow if i in LIT_TOP[edge] else None,
            )

    # --- raised attic panels over the Brannan bays --------------------------
    # The parapet is plain except for small stepped panels on the street front;
    # they keep the crest line from reading as a single extruded stripe.
    for u in UPPER_BAYS[EDGE_FRONT]:
        face_panel(
            f"attic{u:.0f}", EDGE_FRONT, u, rect_profile(2.60, Z_PARAPET - 0.30, Z_PARAPET + 0.34),
            -0.05, 0.13, cream,
        )

    # --- fire escape on the Jack London Alley elevation ---------------------
    # Chunky slabs, not a wireframe: thin bars read as noise at city scale
    # (style bible s.4, s.21). Two landings and one diagonal stair between them.
    fe_u = 12.10
    for z in (Z_W2A + 0.30, Z_W3A + 0.30):
        face_panel(f"fe_deck{z:.0f}", EDGE_NE, fe_u, rect_profile(3.20, z, z + 0.18), SKIN, SKIN + 1.05, ink)
        face_panel(f"fe_rail{z:.0f}", EDGE_NE, fe_u, rect_profile(3.20, z + 0.18, z + 0.80), SKIN + 0.88, SKIN + 1.05, ink)
    # the run between the landings, as one raked slab
    face_panel("fe_stair", EDGE_NE, fe_u + 1.10, rect_profile(0.95, Z_W2A + 0.48, Z_W3A + 0.30), SKIN + 0.45, SKIN + 0.62, ink)

    # --- roof: the surface the app's camera sees most ------------------------
    # u runs along the Brannan edge from its SW end, v goes back into the block
    # (the block is ~24.3 m deep). The penthouse is the piece that matters — it
    # is what the LiDAR maximum measures and what sets the model's height.
    roof_box("penthouse", 10.80, 13.50, Z_DECK, Z_CREST, 9.00, 6.00, cream)
    for i, u in enumerate((5.00, 8.20, 11.40, 14.60)):
        roof_box(f"skylight_kerb{i}", u, 6.40, Z_DECK, Z_DECK + 0.20, 2.60, 1.80, trim)
        roof_box(f"skylight{i}", u, 6.40, Z_DECK + 0.16, Z_DECK + 0.42, 2.30, 1.50, glassl)
    roof_box("hvac_a", 18.60, 10.20, Z_DECK, Z_DECK + 1.00, 2.20, 1.60, steel)
    roof_box("hvac_b", 18.90, 14.00, Z_DECK, Z_DECK + 0.80, 1.60, 1.20, steel)
    roof_box("duct", 17.20, 12.10, Z_DECK + 0.25, Z_DECK + 0.55, 0.70, 1.90, steel)
    roof_box("roof_hatch", 5.40, 18.60, Z_DECK, Z_DECK + 0.50, 1.50, 1.20, roofd)
    roof_box("vent_a", 8.60, 19.60, Z_DECK, Z_DECK + 1.10, 0.60, 0.60, steel)
    roof_box("vent_b", 15.40, 19.20, Z_DECK, Z_DECK + 0.90, 0.50, 0.50, steel)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. Applied window panels are small and numerous — their frames
    # get a token 1-segment softening and the fills/glow shells none at all,
    # which is what keeps this under the 10,000-triangle cap.
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
    print("[build] anchor lon/lat: -122.3935234 37.7810229 (footprint centroid)")
    print("[build] Brannan front heading: 135.8 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "350-brannan.blend")
    glb = os.path.join(out, "350-brannan.glb")
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
