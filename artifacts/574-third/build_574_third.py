"""Deterministic Blender build of the SF-SIM miniature 574 Third Street.

    blender -b --python build_574_third.py -- [--out DIR]

Writes 574-third.blend and 574-third.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint AABB centre (anchor lon -122.3950551,
lat 37.7801937), min Z = 0, billboard crest exactly 15.4 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3776008) simplified from 21 to 7
  vertices (1,909.7 m2 against the survey's 1,906.1), a through-block mass 33.95 m
  wide on Third Street and 45 m deep to the Ritch Street alley, with the big
  8.6 m step back from the northwest party line kept because it is a real court,
  not a survey wobble. Every simplified edge keeps its true SoMa-grid bearing
  (44.8 / 132.9 / 224.9 / 314.9 deg);
* three storeys of one strict window rhythm — 9 bays on Third, 8 on Ritch — which
  is this building's whole architecture. It has almost no ornament and the
  miniature must not invent any;
* painted front, bare brick everywhere else: a chocolate Toy_cocoa skin on the
  Third Street elevation only, stopping 4.5 m short of the northwest end so the
  bare buff brick reads there as it does in the street photography;
* the rooftop billboard at the northwest end, facing southeast down Third — the
  crest, and a blank panel: no advertising artwork;
* night state: a scatter of lit flats across both long elevations (this is 104
  units), the two entrance recesses, and an uplit strip under the billboard
  face. The billboard panel itself is NOT a glow surface;
* a designed roof: parapet ring, the two deep light wells that the nadir imagery
  shows, a skylight/vent field grouped along the strips between them, and one
  stair bulkhead.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF building footprint SF3776008, projected with the app's tangent
# projection, recentred on the AABB centre and simplified to 7 vertices. CCW.
FOOTPRINT = [
    (7.510, 29.965),     # 0  N corner   (Third St / 560 Third party line)
    (-10.350, 12.655),   # 1  inner corner of the northwest court
    (-16.700, 18.515),   # 2  outer corner of the northwest court
    (-33.160, 1.975),    # 3  W corner   (Ritch St / 560 Third side)
    (-1.150, -29.965),   # 4  S corner   (Ritch St / 400 Brannan side)
    (2.810, -24.915),    # 5  SE return
    (31.580, 6.025),     # 6  E corner   (Third St / 400 Brannan party line)
]

# Edge i runs FOOTPRINT[i] -> FOOTPRINT[i+1]. Outward normals verified against
# the survey.
EDGE_NW_COURT = 0    # 24.87 m, faces NW 315.9 — party line at the Third St end
EDGE_COURT_END = 1   #  8.64 m, faces NE  42.7 — the court's back wall
EDGE_NW_DEEP = 2     # 23.33 m, faces NW 314.9 — party line at the Ritch end
EDGE_RITCH = 3       # 45.22 m, faces SW 224.9 — Ritch Street rear
EDGE_SE_RETURN = 4   #  6.42 m, faces SE 128.1
EDGE_SE = 5          # 42.25 m, faces SE 132.9 — party flank toward 400 Brannan
EDGE_THIRD = 6       # 33.95 m, faces NE  44.8 — Third Street front

Z_DECK = 11.05       # roof deck (DataSF LiDAR median, mode 11.03, sigma 1.18)
Z_PARAPET = 11.9     # parapet crest (inferred: deck + 0.85 m)
Z_BILL0 = 11.85      # billboard panel underside (3.55 m panel over the parapet)
Z_CREST = 15.4       # billboard top -> the bbox top, = targetHeightM
Z_BASE = 0.55        # dark base band
Z_SHOP0, Z_SHOP1 = 0.85, 3.70    # shopfront glazing on Third
Z_COURSE = 4.15                  # floor-line course
FLOOR2 = (5.05, 7.15)            # second-floor window band
FLOOR3 = (8.50, 10.60)           # third-floor window band

SKIN = 0.12          # painted front skin, proud of the brick
PARAPET_T = 0.35
WELL_DEPTH = 0.95    # light wells, recessed below the deck

PALETTE_HEX = {
    # Deliberate palette extension: the real paint is a dark chocolate brown and
    # Toy_rust (a86444) turns the building back into a brick box, which is
    # precisely the distinction the painted front exists to make. Off-palette is
    # a WARN, not a FAIL (sf-asset-check s.7).
    "Toy_cocoa": "6b4a3d",
    "Toy_stone": "d9d2c2",
    "Toy_ink": "3a3530",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_trim": "f3efe6",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
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
    a = FOOTPRINT[i]
    b = FOOTPRINT[(i + 1) % len(FOOTPRINT)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def offset_polygon(poly, d):
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


def roof_point(u, v):
    """World XY of a point on the roof grid: u along the Third Street edge from
    its southeast end, v INTO the block."""
    origin, _l, t, n = poly_edge(EDGE_THIRD)
    return (origin[0] + t[0] * u - n[0] * v, origin[1] + t[1] * u - n[1] * v)


def roof_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the roof, aligned to the building's own grid: u runs along the
    Third Street edge from its southeast end, v runs INTO the block."""
    origin, _l, t, n = poly_edge(EDGE_THIRD)
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
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------------- parts


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None,
                 inset=0.16, base=0.0):
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, base + 0.06, frame_mat)
    face_panel(
        f"{tag}_fill", edge, u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset), 0.0, base + 0.13, fill_mat,
    )
    if glow_mat is not None:
        g = inset + 0.13
        face_panel(
            f"{tag}_glow", edge, u,
            rect_profile(w - 2 * g, z0 + g, z1 - g), base + 0.10, base + 0.17, glow_mat,
        )


def arched_opening(tag, edge, u, w, z0, z_spring, rise, frame_mat, fill_mat,
                   glow_mat=None, base=0.0):
    face_panel(
        f"{tag}_frame", edge, u, arch_profile(w, z0, z_spring, rise), 0.0, base + 0.06, frame_mat
    )
    inset = 0.18
    face_panel(
        f"{tag}_fill", edge, u,
        arch_profile(w - 2 * inset, z0 + inset, z_spring, max(rise - 0.07, 0.0)),
        0.0, base + 0.13, fill_mat,
    )
    if glow_mat is not None:
        g = 0.32
        face_panel(
            f"{tag}_glow", edge, u,
            arch_profile(w - 2 * g, z0 + g, z_spring - 0.12, max(rise - 0.15, 0.0)),
            base + 0.10, base + 0.17, glow_mat,
        )


def fire_escape(tag, edge, u, mats):
    """A chunky balcony per upper floor, not a wireframe: thin bars read as
    noise over the window behind them at city scale (style bible s.4, s.21)."""
    ink = mats["ink"]
    for k, (z0, _z1) in enumerate((FLOOR2, FLOOR3)):
        face_panel(f"{tag}_deck{k}", edge, u, rect_profile(2.9, z0 - 0.18, z0), 0.0, 1.05, ink)
        face_panel(f"{tag}_rail{k}", edge, u, rect_profile(2.9, z0, z0 + 0.62), 0.88, 1.05, ink)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    cocoa = material("Toy_cocoa")
    stone = material("Toy_stone")
    ink = material("Toy_ink")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    trim = material("Toy_trim")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    gglow = material("Toy_glass_Glow")
    tglow = material("Toy_trim_Glow")
    mats = {"ink": ink}

    # --- body: buff brick shell, its top cap IS the roof deck --------------
    prism("body", FOOTPRINT, 0.0, Z_DECK, stone, mat_caps=roofd)

    # --- parapet ring + coping ---------------------------------------------
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET - 0.16, -PARAPET_T, 0.0, stone)
    ring_band("coping", FOOTPRINT, Z_PARAPET - 0.16, Z_PARAPET, -PARAPET_T - 0.07, 0.07, stone)

    # --- painted Third Street skin, stopping short of the northwest end -----
    len_t = poly_edge(EDGE_THIRD)[1]
    paint_len = len_t - 4.5
    face_panel(
        "front_skin", EDGE_THIRD, paint_len / 2.0,
        rect_profile(paint_len, 0.0, Z_PARAPET), 0.0, SKIN, cocoa,
    )
    face_panel(
        "front_base", EDGE_THIRD, len_t / 2.0,
        rect_profile(len_t, 0.0, Z_BASE), 0.0, SKIN + 0.08, ink,
    )
    face_panel(
        "front_course", EDGE_THIRD, len_t / 2.0,
        rect_profile(len_t, Z_COURSE, Z_COURSE + 0.2), 0.0, SKIN + 0.10, stone,
    )

    # --- Third Street ground floor: shopfronts + two residential entrances --
    LIT_SHOPS = {0, 2, 4}
    for i, (u, w) in enumerate(((3.4, 4.2), (8.3, 4.2), (16.6, 4.2), (21.5, 4.2), (26.4, 4.2))):
        rect_opening(f"third_shop{i}", EDGE_THIRD, u, w, Z_SHOP0, Z_SHOP1, ink, glass,
                     tglow if i in LIT_SHOPS else None, inset=0.24, base=SKIN)
    for i, u in enumerate((12.6, 30.6)):
        rect_opening(f"third_door{i}", EDGE_THIRD, u, 1.6, 0.0, 3.2, ink, ink,
                     tglow, inset=0.18, base=SKIN)

    # --- Third Street upper floors: 9 bays, the building's whole architecture
    LIT3 = {(0, 1), (0, 4), (0, 5), (0, 8), (1, 0), (1, 2), (1, 3), (1, 6)}
    bays_t = 9
    for f, (z0, z1) in enumerate((FLOOR2, FLOOR3)):
        for i in range(bays_t):
            u = len_t / (2.0 * bays_t) + i * (len_t / bays_t)
            rect_opening(
                f"third_w{f}{i}", EDGE_THIRD, u, 1.35, z0, z1, trim, glass,
                gglow if (f, i) in LIT3 else None, inset=0.14,
                base=SKIN if u < paint_len else 0.0,
            )
    fire_escape("third_fe0", EDGE_THIRD, 11.3, mats)
    fire_escape("third_fe1", EDGE_THIRD, 26.4, mats)

    # --- Ritch Street rear: bare brick, segmental heads ---------------------
    len_r = poly_edge(EDGE_RITCH)[1]
    arched_opening("ritch_service", EDGE_RITCH, 6.0, 3.6, 0.0, 3.3, 0.55, stone, roofd)
    for i, u in enumerate((11.6, 15.4, 30.0, 33.8)):
        arched_opening(f"ritch_g{i}", EDGE_RITCH, u, 1.5, 0.9, 3.1, 0.45, stone, glass)
    arched_opening("ritch_door", EDGE_RITCH, 22.6, 1.6, 0.0, 3.0, 0.35, stone, ink)
    LITR = {(0, 2), (0, 5), (1, 0), (1, 3), (1, 4), (1, 7)}
    bays_r = 8
    for f, (z0, z1) in enumerate((FLOOR2, FLOOR3)):
        for i in range(bays_r):
            u = len_r / (2.0 * bays_r) + i * (len_r / bays_r)
            arched_opening(
                f"ritch_w{f}{i}", EDGE_RITCH, u, 1.35, z0, z1 - 0.45, 0.42, stone, glass,
                gglow if (f, i) in LITR else None,
            )
    fire_escape("ritch_fe0", EDGE_RITCH, 14.1, mats)
    fire_escape("ritch_fe1", EDGE_RITCH, 36.5, mats)

    # --- southeast party flank: sparse, block-interior half only ------------
    # No view of this wall was found; a quiet brick plane with a few openings is
    # the honest choice (see the plan's 2.15).
    for i, u in enumerate((22.0, 27.5, 33.0, 38.5)):
        for f, (z0, z1) in enumerate((FLOOR2, FLOOR3)):
            rect_opening(f"se_w{f}{i}", EDGE_SE, u, 1.2, z0 + 0.15, z1 - 0.15, stone, glass,
                         inset=0.13)

    # --- northwest court walls ----------------------------------------------
    for i, u in enumerate((5.5, 11.5, 17.5)):
        for f, (z0, z1) in enumerate((FLOOR2, FLOOR3)):
            rect_opening(f"nw_w{f}{i}", EDGE_NW_DEEP, u, 1.2, z0 + 0.15, z1 - 0.15, stone,
                         glass, inset=0.13)
    for f, (z0, z1) in enumerate((FLOOR2, FLOOR3)):
        rect_opening(f"court_w{f}", EDGE_COURT_END, 4.3, 1.2, z0 + 0.15, z1 - 0.15, stone,
                     glass, inset=0.13)

    # --- roof ----------------------------------------------------------------
    # Two light wells run back from Third Street, exactly as the nadir imagery
    # shows; they are recessed slots rather than plan notches, which reads the
    # same from the app's camera and keeps the party walls simple.
    # The kerb is a thin stone lip AROUND each well; the well itself is an ink
    # box whose top sits 60 mm proud of the deck, which is what makes it read as
    # a dark slot from above rather than as a light slab.
    for i, u in enumerate((12.6, 21.4)):
        roof_box(f"well_kerb{i}", u, 19.0, Z_DECK, Z_DECK + 0.14, 4.3, 26.4, stone)
        roof_box(f"well{i}", u, 19.0, Z_DECK - WELL_DEPTH, Z_DECK + 0.20, 3.5, 25.6, ink)

    for i, (u, v) in enumerate(((6.0, 7.0), (6.0, 17.5), (6.0, 28.0), (17.0, 34.0),
                                (27.5, 26.0), (27.5, 36.0))):
        roof_box(f"skylight_kerb{i}", u, v, Z_DECK, Z_DECK + 0.2, 2.4, 1.8, stone)
        roof_box(f"skylight{i}", u, v, Z_DECK + 0.16, Z_DECK + 0.42, 2.1, 1.5, glassl)
    roof_box("mech_plinth", 27.6, 15.0, Z_DECK, Z_DECK + 0.18, 6.2, 4.8, roofd)
    roof_box("mech_a", 26.2, 14.1, Z_DECK, Z_DECK + 1.0, 1.9, 1.4, steel)
    roof_box("mech_b", 29.0, 15.9, Z_DECK, Z_DECK + 0.75, 1.4, 1.1, steel)
    roof_box("vent_a", 16.9, 8.0, Z_DECK, Z_DECK + 0.9, 0.6, 0.6, steel)
    roof_box("vent_b", 9.5, 38.0, Z_DECK, Z_DECK + 0.8, 0.5, 0.5, steel)
    roof_box("bulkhead", 6.0, 39.5, Z_DECK, Z_DECK + 1.35, 3.2, 2.6, roofd)
    roof_box("bulkhead_b", 24.0, 39.0, Z_DECK, Z_DECK + 1.1, 2.6, 2.2, roofd)

    # --- rooftop billboard at the northwest end, facing southeast -----------
    # Blank panel in a frame on two legs. No artwork: the asset ships in a
    # published city and advertising imagery is not ours to reproduce.
    # Canted about 22 deg off the street line, the way a hoarding is turned to
    # face oncoming traffic — and the reason it reads as a panel rather than as
    # a hairline from the app's usual approach down Third Street.
    bill_yaw = math.radians(205.0)
    bx, by = roof_point(30.6, 8.6)
    ax, ay = math.cos(bill_yaw), math.sin(bill_yaw)
    for k, off in enumerate((-3.4, 3.4)):
        box(f"bill_leg{k}", bx + ax * off, by + ay * off, Z_DECK, Z_BILL0 + 0.4,
            1.0, 0.38, steel, yaw=bill_yaw)
    box("bill_frame", bx, by, Z_BILL0 - 0.20, Z_CREST, 9.9, 0.44, trim, yaw=bill_yaw)
    box("bill_face", bx, by, Z_BILL0, Z_CREST - 0.20, 9.5, 0.52, ink, yaw=bill_yaw)
    box("bill_light", bx + math.sin(bill_yaw) * 0.16, by - math.cos(bill_yaw) * 0.16,
        Z_BILL0 - 0.02, Z_BILL0 + 0.24, 9.0, 0.16, tglow, yaw=bill_yaw)

    # Bevel budget: chunky masses get the full 0.12/2; window frames a token
    # 1-segment softening; fills and glow shells none.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")) or obj.name == "bill_light":
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
    print("[build] anchor lon/lat: -122.3950551 37.7801937 (footprint AABB centre)")
    print("[build] Third front heading 44.8 deg; Ritch rear heading 224.9 deg")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "574-third.blend")
    glb = os.path.join(out, "574-third.glb")
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
