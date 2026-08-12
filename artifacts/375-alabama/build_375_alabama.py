"""Deterministic Blender build of the SF-SIM miniature 375 Alabama Street.

    blender -b --python build_375_alabama.py -- [--out DIR]

Writes 375-alabama.blend and 375-alabama.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint OBB centre (anchor lon -122.4118477,
lat 37.7645633), min Z = 0, stair-tower crest exactly 22.5 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3966002), a 61.02 x 54.62 m block
  filling the corner of 17th and Alabama, rotated 4.32 deg CCW off the world
  axes like the rest of the Mission grid;
* the Ames Harris Neville Co. daylight-factory grammar: a cream reinforced
  concrete shell, expressed piers proud of the wall, and continuous recessed
  steel-sash glazing bands running behind them — the piers carry the rhythm, so
  the glazing is banded rather than cut bay by bay (cheap, and truer to a
  concrete frame than a grid of punched holes);
* the identity feature: cast cog-wheel medallions in the parapet frieze, one
  over every pier of the two street elevations. They do NOT glow — they are a
  daylight feature, not signage;
* the stepped Art Deco stair tower over the arched Alabama Street entrance, the
  only thing that breaks the skyline, setting the 22.5 m crest;
* a real sawtooth monitor roof across the southern half and a clean dark
  membrane across the north — this is the surface the app's camera actually
  sees;
* night state: the tower crown fins as the hero, two of the five monitors lit
  from within, a restrained scatter of lit window segments and the entrance.
  Glow surfaces are thin shells proud of the opaque glazing (the app renders
  _Glow in a separate layer that is ~12% alpha by day — never author a primary
  surface as glow).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF building footprint SF3966002 projected with the app's tangent
# projection and recentred on the OBB centre, reduced to its four corners. CCW.
# The survey's two sub-620 mm jogs on the east and west walls are pilaster
# returns; they are absorbed into the expressed pier rhythm rather than modelled
# as footprint steps (documented deviation from plan 2.3 — see REPORT.md).
FOOTPRINT = [
    (-28.407, -29.541),  # SW — 17th & Alabama
    (32.429, -24.754),   # SE — 17th & Florida
    (28.359, 29.537),    # NE
    (-32.354, 24.938),   # NW
]

EDGE_SOUTH = 0   # 61.02 m, faces S 175.7 deg — 17th Street
EDGE_EAST = 1    # 54.44 m, faces E  85.7 deg — Florida Street
EDGE_NORTH = 2   # 60.89 m, faces N 355.7 deg — rear yard
EDGE_WEST = 3    # 54.62 m, faces W 265.7 deg — Alabama Street, the address

Z_DECK = 15.90       # roof deck (DataSF LiDAR hgt_median_m, = OSM height 16)
Z_PARAPET = 17.60    # main parapet crest (inferred)
Z_PIERCAP = 18.40    # stepped cap over each pier (inferred)
Z_CORNERCAP = 18.90  # taller chamfered corner-bay cap (inferred)
Z_RIDGE = 19.20      # sawtooth monitor ridge (LiDAR hgt_majoritycm 1921)
Z_CREST = 22.50      # stair-tower crown = the bbox top (inferred, 2.15)

Z_GROUND_TOP = 4.90  # ground-floor ceiling line
FLOOR = (Z_DECK - Z_GROUND_TOP) / 3.0   # 3.667 m upper-floor height

PIER_W = 1.50
PIER_D = 0.25        # piers proud of the wall
GLASS_D = 0.18       # glazing bands sit behind the piers
REVEAL_D = 0.10

BAYS = {EDGE_WEST: 10, EDGE_EAST: 10, EDGE_SOUTH: 11, EDGE_NORTH: 11}

# Tower: measured along the west wall from the SOUTHWEST corner.
TOWER_FROM_SW = 13.0
TOWER_W = 6.40       # along the wall (N-S)
TOWER_DEPTH = 5.60   # into the block
TOWER_PROUD = 1.10   # projection past the west wall
TOWER_FIN_W = 1.15   # the full-height cream fins that give the shaft its lift

PALETTE_HEX = {
    "Toy_cream": "f2ede3",
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    # Deliberate palette extension: the tower's centre panel is a dusty
    # mauve-taupe. The nearest palette entry, Toy_rust (a86444), rendered as an
    # orange billboard that stole the whole elevation — see REPORT.md for the
    # comparison. Off-palette is a WARN, not a FAIL (contract rule 7).
    "Toy_mauve": "a2887f",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_ink": "3a3530",
    "Toy_glass_Glow": "6f95b8",
    "Toy_glassl_Glow": "9fc3dd",
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


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


def arch_profile(w, z0, z_spring, rise, seg=5):
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


def cog_profile(zc, r_out, r_in, teeth=12):
    """Closed (u, z) profile of a gear wheel — the AHN medallion silhouette.

    The monogram inside the real casting is dropped: it is sub-pixel at city
    scale and the cog reads on its own (plan 2.6).
    """
    pts = []
    for k in range(teeth * 2):
        ang = math.pi * k / teeth
        r = r_out if k % 2 == 0 else r_in
        pts.append((r * math.cos(ang), zc + r * math.sin(ang)))
    return pts


def disc_profile(zc, r, seg=12):
    return [
        (r * math.cos(2 * math.pi * k / seg), zc + r * math.sin(2 * math.pi * k / seg))
        for k in range(seg)
    ]


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

    Width is capped at a third of the object's thinnest dimension: many applied
    panels here are only 80-250 mm thick, and a flat 0.12 m bevel on those
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


def wall_box(name, edge, u, z0, z1, span, depth, d_out, mat):
    """Box hung on wall `edge`: `span` along the wall centred on u, its outer
    face `d_out` proud of the wall plane, running `depth` back into the block."""
    a, _l, t, n = poly_edge(edge)
    mid = d_out - depth / 2.0
    cx = a[0] + t[0] * u + n[0] * mid
    cy = a[1] + t[1] * u + n[1] * mid
    return box(name, cx, cy, z0, z1, span, depth, mat, yaw=math.atan2(t[1], t[0]))


def roof_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the roof, aligned to the building's own grid: u runs east along
    the 17th Street edge from the SW corner, v runs north into the block."""
    origin, _l, t, n = poly_edge(EDGE_SOUTH)
    cx = origin[0] + t[0] * u - n[0] * v
    cy = origin[1] + t[1] * u - n[1] * v
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=math.atan2(t[1], t[0]))


def roof_prism(name, profile_vz, u0, u1, mat):
    """Closed prism whose cross-section is a closed (v, z) profile in the
    building's own north/up plane, extruded along u (east, along 17th Street)."""
    origin, _l, t, n = poly_edge(EDGE_SOUTH)
    verts = []
    for u in (u0, u1):
        for v, z in profile_vz:
            verts.append((origin[0] + t[0] * u - n[0] * v, origin[1] + t[1] * u - n[1] * v, z))
    npts = len(profile_vz)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
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


def pier_positions(edge):
    """Pier centres along `edge`, one at each bay boundary including corners."""
    length = poly_edge(edge)[1]
    n = BAYS[edge]
    return [length * i / n for i in range(n + 1)], length


def glazing_band(tag, edge, z0, z1, mats, lit=()):
    """Continuous recessed steel-sash band running the whole elevation behind
    the piers: a dark reveal, the glass proud of it, and optional glow shells.

    `lit` is a list of (u_centre, width) segments that light at night.
    """
    ink, glass, glow = mats
    length = poly_edge(edge)[1]
    inner = length - 2.0
    face_panel(f"{tag}_reveal", edge, length / 2.0, rect_profile(inner, z0, z1), 0.0, REVEAL_D, ink)
    face_panel(
        f"{tag}_glass",
        edge,
        length / 2.0,
        rect_profile(inner - 0.5, z0 + 0.22, z1 - 0.22),
        0.0,
        GLASS_D,
        glass,
    )
    for i, (u, w) in enumerate(lit):
        face_panel(
            f"{tag}_glow{i}",
            edge,
            u,
            rect_profile(w, z0 + 0.42, z1 - 0.42),
            GLASS_D - 0.03,
            GLASS_D + 0.05,
            glow,
        )


def rollup_door(tag, edge, u, w, height, steel, ink):
    face_panel(f"{tag}_frame", edge, u, rect_profile(w + 0.5, 0.0, height + 0.3), 0.0, 0.30, ink)
    face_panel(f"{tag}_leaf", edge, u, rect_profile(w, 0.0, height), 0.0, 0.38, steel)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    cream = material("Toy_cream")
    stone = material("Toy_stone")
    trim = material("Toy_trim")
    mauve = material("Toy_mauve")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    ink = material("Toy_ink")
    gglow = material("Toy_glass_Glow")
    lglow = material("Toy_glassl_Glow")
    tglow = material("Toy_trim_Glow")

    # --- concrete body: its top cap IS the flat north roof deck -------------
    prism("body", FOOTPRINT, 0.0, Z_DECK, cream, mat_caps=roofd)

    # --- glazing bands: ground floor plus three upper floors ----------------
    # A concrete frame shows continuous glazing between its piers, so the bands
    # run the full elevation and the piers (added next) cut them into bays.
    bands = [
        (1.70, 4.35),
        (Z_GROUND_TOP + 0.60, Z_GROUND_TOP + FLOOR - 0.50),
        (Z_GROUND_TOP + FLOOR + 0.60, Z_GROUND_TOP + 2 * FLOOR - 0.50),
        (Z_GROUND_TOP + 2 * FLOOR + 0.60, Z_DECK - 0.50),
    ]
    # Restrained night scatter: a handful of segments on the two street
    # elevations only, never a fully lit floor (style bible s.11).
    lit_west = {2: [(11.0, 4.6), (33.5, 4.6)], 3: [(22.0, 4.6)]}
    lit_south = {1: [(28.0, 5.0)], 2: [(11.0, 5.0), (50.0, 5.0)], 3: [(39.0, 5.0)]}
    for edge, tag in ((EDGE_WEST, "w"), (EDGE_SOUTH, "s"), (EDGE_EAST, "e"), (EDGE_NORTH, "n")):
        for bi, (z0, z1) in enumerate(bands):
            if edge == EDGE_NORTH and bi == 0:
                continue  # blank service wall at ground level on the rear
            lit = ()
            if edge == EDGE_WEST:
                lit = lit_west.get(bi, ())
            elif edge == EDGE_SOUTH:
                lit = lit_south.get(bi, ())
            glazing_band(f"{tag}b{bi}", edge, z0, z1, (ink, glass, gglow), lit)

    # --- expressed piers: the bay rhythm ------------------------------------
    for edge, tag in ((EDGE_WEST, "w"), (EDGE_SOUTH, "s"), (EDGE_EAST, "e"), (EDGE_NORTH, "n")):
        us, _length = pier_positions(edge)
        for i, u in enumerate(us):
            face_panel(
                f"pier_{tag}{i}", edge, u, rect_profile(PIER_W, 0.0, Z_PARAPET), 0.0, PIER_D, cream
            )

    # --- parapet ring, stone coping, stepped pier caps ----------------------
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET - 0.20, -0.45, PIER_D, cream)
    ring_band("coping", FOOTPRINT, Z_PARAPET - 0.20, Z_PARAPET, -0.52, PIER_D + 0.07, stone)
    for edge, tag in ((EDGE_WEST, "w"), (EDGE_SOUTH, "s"), (EDGE_EAST, "e"), (EDGE_NORTH, "n")):
        us, length = pier_positions(edge)
        for i, u in enumerate(us):
            corner = i == 0 or i == len(us) - 1
            top = Z_CORNERCAP if corner else Z_PIERCAP
            span = 2.5 if corner else PIER_W + 0.4
            wall_box(
                f"cap_{tag}{i}", edge, u, Z_PARAPET, top, span, 1.05, PIER_D + 0.07, stone
            )

    # --- the cog medallions: the whole identity of the building -------------
    # Enlarged from the real ~1.2 m casting to 1.7 m so the cog silhouette
    # survives at the app's camera distance — the one place semantic
    # exaggeration is spent (plan 2.6).
    for edge, tag in ((EDGE_WEST, "w"), (EDGE_SOUTH, "s")):
        us, _length = pier_positions(edge)
        for i, u in enumerate(us):
            face_panel(
                f"medal_{tag}{i}", edge, u, cog_profile(16.70, 0.85, 0.68), PIER_D, PIER_D + 0.15,
                stone,
            )
            face_panel(
                f"hub_{tag}{i}", edge, u, disc_profile(16.70, 0.34, 8), PIER_D + 0.10, PIER_D + 0.22,
                cream,
            )

    # --- Alabama Street ground floor: the arched entrance under the tower ---
    len_w = poly_edge(EDGE_WEST)[1]
    u_tower = len_w - TOWER_FROM_SW           # u runs NW -> SW along the west wall
    face_panel(
        "entrance_frame", EDGE_WEST, u_tower, arch_profile(3.0, 0.0, 3.60, 0.65),
        0.0, TOWER_PROUD + 0.10, stone,
    )
    face_panel(
        "entrance_fill", EDGE_WEST, u_tower, arch_profile(2.3, 0.30, 3.55, 0.55),
        0.0, TOWER_PROUD + 0.18, ink,
    )
    face_panel(
        "entrance_glow", EDGE_WEST, u_tower, rect_profile(1.7, 0.60, 2.90),
        TOWER_PROUD + 0.14, TOWER_PROUD + 0.22, tglow,
    )
    # the "375" plaque on the pier north of the arch
    face_panel(
        "plaque375", EDGE_WEST, u_tower - 4.9, rect_profile(1.0, 3.20, 4.00), PIER_D, PIER_D + 0.10,
        trim,
    )
    rollup_door("door_w", EDGE_WEST, u_tower + 6.0, 4.4, 4.20, steel, ink)
    rollup_door("door_w2", EDGE_WEST, 9.0, 4.4, 4.20, steel, ink)

    # --- 17th Street and Florida Street loading -----------------------------
    rollup_door("door_s1", EDGE_SOUTH, 14.0, 4.4, 4.20, steel, ink)
    rollup_door("door_s2", EDGE_SOUTH, 39.5, 4.4, 4.20, steel, ink)
    rollup_door("door_e", EDGE_EAST, 12.0, 4.4, 4.20, steel, ink)
    rollup_door("door_n", EDGE_NORTH, 30.0, 4.0, 3.90, steel, ink)

    # --- the stair tower: the only break in the skyline ---------------------
    face_panel(
        "tower_base", EDGE_WEST, u_tower, rect_profile(TOWER_W, 0.0, Z_DECK), 0.0, TOWER_PROUD,
        cream,
    )
    wall_box(
        "tower_body", EDGE_WEST, u_tower, Z_DECK, 21.00, TOWER_W, TOWER_DEPTH, TOWER_PROUD, cream
    )
    # The shaft's dark centre panel starts above the ground floor, so the
    # entrance surround stays cream the way the 2007 photograph shows it.
    face_panel(
        "tower_panel", EDGE_WEST, u_tower, rect_profile(3.6, Z_GROUND_TOP, 21.80),
        TOWER_PROUD, TOWER_PROUD + 0.18, mauve,
    )
    # Full-height fins: in the photograph these run the whole shaft, and without
    # them the tower reads as a box parked on the parapet rather than a tower.
    fin_off = (TOWER_W - TOWER_FIN_W) / 2.0
    for tag, du in (("n", -fin_off), ("s", fin_off)):
        face_panel(
            f"tower_fin_{tag}", EDGE_WEST, u_tower + du, rect_profile(TOWER_FIN_W, 0.0, Z_CREST),
            TOWER_PROUD, TOWER_PROUD + 0.45, trim,
        )
        face_panel(
            f"tower_finglow_{tag}", EDGE_WEST, u_tower + du,
            rect_profile(TOWER_FIN_W - 0.20, 18.20, Z_CREST - 0.15),
            TOWER_PROUD + 0.41, TOWER_PROUD + 0.53, tglow,
        )
    # the notched crown: the centre steps back and up between the fins
    wall_box("tower_notch", EDGE_WEST, u_tower, 21.00, 21.80, 3.9, TOWER_DEPTH - 1.2,
             TOWER_PROUD, cream)

    # --- roof: the surface the app's camera sees most ------------------------
    # u runs east along 17th Street from the SW corner, v north into the block.
    # South ~60% is the sawtooth monitor field; north stays a clean dark
    # membrane (the body's top cap) so the two halves read as different planes.
    MONITORS = (8.0, 13.5, 19.0, 24.5, 30.0)
    LIT_MONITORS = {1, 3}
    for i, v_r in enumerate(MONITORS):
        # A trapezoid with a flat 0.8 m ridge cap, not a triangle: the single
        # ridge vertex bevelled into a barrel and the whole field read as fat
        # white tubes from the aerial. The flat cap also gives the near-vertical
        # north face enough area to read as glass.
        body = [
            (v_r - 2.60, Z_DECK),
            (v_r + 1.40, Z_DECK),
            (v_r + 0.55, Z_RIDGE),
            (v_r - 0.25, Z_RIDGE),
        ]
        roof_prism(f"monitor{i}", body, 5.0, 56.0, stone)
        # glazed north face: the ridge-to-eave segment offset along its normal
        dv, dz = 0.85, Z_DECK - Z_RIDGE
        ln = math.hypot(dv, dz)
        ov, oz = -dz / ln * 0.09, dv / ln * 0.09
        pane = [
            (v_r + 0.55, Z_RIDGE),
            (v_r + 1.40, Z_DECK),
            (v_r + 1.40 + ov, Z_DECK + oz),
            (v_r + 0.55 + ov, Z_RIDGE + oz),
        ]
        roof_prism(f"monitor_glass{i}", pane, 5.4, 55.6, glassl)
        if i in LIT_MONITORS:
            # A short lit stretch near the ridge, not the whole 50 m pane: lit
            # end to end at full height the two monitors read as fluorescent
            # light bars and flattened the tower's hero glow (style bible s.11).
            f = 0.34   # fraction of the glazed face that lights
            gv = v_r + 0.55 + (0.85 * f)
            gz = Z_RIDGE + (Z_DECK - Z_RIDGE) * f
            pane_g = [
                (v_r + 0.55 + ov * 0.9, Z_RIDGE + oz * 0.9),
                (gv + ov * 0.9, gz + oz * 0.9),
                (gv + ov * 1.8, gz + oz * 1.8),
                (v_r + 0.55 + ov * 1.8, Z_RIDGE + oz * 1.8),
            ]
            roof_prism(f"monitor_glow{i}", pane_g, 15.0, 34.0, lglow)

    # rooftop wireless facility (permitted 2000 onward) + vents, on the clean
    # north membrane where the sawteeth leave room
    roof_box("equip_room", 44.0, 42.0, Z_DECK, Z_DECK + 2.20, 4.2, 3.2, steel)
    roof_box("equip_low", 39.0, 39.6, Z_DECK, Z_DECK + 1.10, 2.4, 2.0, steel)
    roof_box("mast", 46.6, 44.4, Z_DECK, Z_DECK + 3.50, 0.45, 0.45, steel)
    for i, (u, v) in enumerate(((41.6, 44.6), (46.2, 40.2))):
        roof_box(f"dish{i}", u, v, Z_DECK + 1.60, Z_DECK + 2.80, 1.20, 0.30, steel)
    for i, (u, v) in enumerate(((6.5, 40.0), (14.0, 44.5), (22.0, 38.5), (30.0, 45.5))):
        roof_box(f"vent{i}", u, v, Z_DECK, Z_DECK + 1.40, 0.85, 0.85, ink)
    roof_box("stairhatch", 52.0, 36.0, Z_DECK, Z_DECK + 0.90, 2.2, 1.8, roofd)
    # the west half of the membrane read as an empty tray from the aerial
    roof_box("plantroom", 12.0, 34.5, Z_DECK, Z_DECK + 1.80, 3.6, 2.6, steel)
    roof_box("tankstand", 24.5, 43.0, Z_DECK, Z_DECK + 1.30, 2.0, 2.0, roofd)

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.12/2. Piers, caps and roof props are numerous — a token 1-segment
    # softening keeps the silhouette without spending the cap. The medallions
    # get none: 23 beveled 24-gon cogs cost 6,500 triangles, over a third of the
    # whole asset, to soften an edge that is a fraction of a pixel from the
    # app's camera. Panel fills and glow shells get none either.
    HEAVY = ("body", "parapet", "coping", "tower_body", "tower_base", "tower_notch")
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if "glow" in name or "glass" in name or name.endswith("_fill"):
            continue
        if name.startswith(("medal_", "hub_")):
            continue
        if name in HEAVY:
            bevel(obj, width=0.12, segments=2)
        elif name.startswith("monitor"):
            # 0.12/2 turned the sawtooth ridges into fat white tubes from the
            # aerial; a monitor ridge is a sharp line and has to stay one.
            bevel(obj, width=0.05, segments=1)
        else:
            bevel(obj, width=0.05, segments=1)

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
    print("[build] anchor lon/lat: -122.4118477 37.7645633 (footprint OBB centre)")
    print("[build] 17th Street front heading: 175.7 deg true (S); Alabama front 265.7 deg (W)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "375-alabama.blend")
    glb = os.path.join(out, "375-alabama.glb")
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
