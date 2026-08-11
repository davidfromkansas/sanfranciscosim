"""Deterministic Blender build of the SF-SIM miniature Fairmont San Francisco.

    blender -b --python build_fairmont_san_francisco.py -- [--out DIR]

Writes fairmont-san-francisco.blend and fairmont-san-francisco.glb next to
this file (or into --out). Geometry is authored in world space in metres, Z up,
+X east, +Y north, origin at the composition's base centre, min Z = 0, so the
export needs no transforms applied after the fact.

Design (see REFERENCE.md for the sources behind every number):

* the 1907 Beaux-Arts block at its mapped footprint (65 x 84 m of the
  117.9 x 84.1 m complex), a punched grid of recessed dark windows over a
  grooved rusticated base, one string course, a chunky projecting cornice with
  rhythmic cresting, stepped parapet blocks, and the roof-garden courtyard the
  aerial camera looks straight into;
* the west (Mason Street) hero front: slightly projecting corner pavilions, a
  centre pavilion with a giant eight-column colonnade, and the porte-cochere
  carrying the arc of international flags — the one-second identity cue;
* the 1961/62 tower east of the block (downhill), a pale slab with recessed
  vertical glass strips, thin spandrel ledges, a glassy Crown Room band, and
  the picket-crown parapet, topping out at the published 99.06 m;
* the ballroom podium between them with a simple planted roof terrace;
* the whole composition yawed +9.05 degrees CCW to the measured Nob Hill grid
  so it drops into the city at its true heading (entrance normal ~261 true).

_Glow is limited to two zones: the porte-cochere fascia (entrance uplight) and
the tower's crown fascia ring (the lit crown) — grand hotels read as lit at
night, but restraint keeps it a miniature.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters
# Grid frame: u runs along California (east-ish), v along Mason (north-ish).
# The OSM complex centroid is the grid origin; YAW maps grid onto true world.

YAW = math.radians(9.05)  # measured Nob Hill grid rotation, CCW from cardinal

# Historic block (mapped footprint, grid frame)
BLK_U0, BLK_U1 = -45.2, 20.0
BLK_V0, BLK_V1 = -48.8, 35.3
CRT_U0, CRT_U1 = -22.4, -0.2  # roof-garden courtyard hole (mapped)
CRT_V0, CRT_V1 = -26.7, 11.7

H_BASE = 8.0       # rusticated base top
H_BODY = 29.6      # wall top / roof deck
H_CORN = 31.2      # cornice top
H_CREST = 32.4     # cresting top
H_PARAPET = 33.4   # corner parapet blocks top

ROWS_Z = [9.4 + i * 3.35 for i in range(6)]  # window row sills
WIN_H = 2.85
WIN_W = 2.2
DEPTH = 0.35       # window recess
PANEL_GAP = 0.45   # panel face to core face

# Porte-cochere (mapped 21.3 x 6.9 m projection on Mason)
PC_U0, PC_U1 = -52.0, BLK_U0
PC_V0, PC_V1 = -16.2, 5.1
PC_H = 8.0

# Podium + tower (east, downhill)
POD_U0, POD_U1 = BLK_U1, 42.0
POD_V0, POD_V1 = BLK_V0, BLK_V1
POD_H = 12.0
TWR_U0, TWR_U1 = 42.0, 65.9
TWR_V0, TWR_V1 = -30.0, 8.0
TWR_ROOF = 96.6    # crown deck
TWR_TOP = 99.06    # published architectural height — governs the manifest
CROWN_GLASS0, CROWN_GLASS1 = 90.0, 95.5

# Project palette from .agents/skills/sf-asset-check (hex, sRGB).
PALETTE_HEX = {
    "Toy_cream": "f2ede3",
    "Toy_sand": "ece4d4",
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_stone": "d9d2c2",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_mint": "8fd0a8",
    "Toy_sky": "6db3d9",
    "Toy_red": "c4453c",
    "Toy_teal": "3fa8a0",
    "Toy_mustard": "d9a441",
    "Toy_ink": "3a3530",
    "Toy_white_Glow": "f7f4ec",
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
        # Flagged for the app's night pass; emission stays off in daylight.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    mat.blend_method = "OPAQUE"
    return mat


# -------------------------------------------------------------- mesh helpers


def new_mesh(name, verts, faces, materials_, face_mats=None, recalc=True):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    for m in materials_:
        mesh.materials.append(m)
    if face_mats:
        for poly, mi in zip(mesh.polygons, face_mats):
            poly.material_index = mi
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    if recalc:
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()
    mesh.shade_flat()
    return obj


def orient_outward(obj, axis=None):
    """Force a mesh's faces to face outward.

    Open shells (the facade panels, the capless cornice/parapet rings) cannot
    be fixed by recalc_face_normals, which only guarantees consistency, not
    direction. Score the area-weighted normals against a reference — an
    explicit outward axis for flat panels, or the horizontal radial direction
    from the mesh's own centroid for rings and tubes — and reverse every face
    when the mesh came out inside-out. Deterministic, so the build stays
    reproducible.
    """
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.normal_update()
    score = 0.0
    if axis is not None:
        a = Vector(axis).normalized()
        for f in bm.faces:
            score += f.calc_area() * f.normal.dot(a)
    else:
        cen = Vector()
        for v in bm.verts:
            cen += v.co
        cen /= max(1, len(bm.verts))
        for f in bm.faces:
            r = f.calc_center_median() - cen
            n = f.normal.copy()
            r.z = 0.0
            n.z = 0.0
            if r.length > 1e-6 and n.length > 1e-6:
                score += f.calc_area() * r.normalized().dot(n.normalized())
    if score < 0:
        bmesh.ops.reverse_faces(bm, faces=list(bm.faces))
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    return obj


def bevel(obj, width=0.12, segments=2):
    """Miniature-style edge softening on the chunky solids (style bible §4)."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(
        bm,
        geom=list(bm.verts) + list(bm.edges),
        offset=width,
        segments=segments,
        profile=0.5,
        affect="EDGES",
        clamp_overlap=True,
    )
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def box(name, u0, v0, u1, v1, z0, z1, mat):
    verts = [
        (u0, v0, z0), (u1, v0, z0), (u1, v1, z0), (u0, v1, z0),
        (u0, v0, z1), (u1, v0, z1), (u1, v1, z1), (u0, v1, z1),
    ]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, [mat])


def stick(name, p0, p1, thick, mat):
    """A thin square prism between two points — flagpoles, pergola members."""
    p0, p1 = Vector(p0), Vector(p1)
    axis = (p1 - p0).normalized()
    side = axis.cross(Vector((0, 0, 1)))
    if side.length < 1e-4:
        side = Vector((1, 0, 0))
    side.normalize()
    up = axis.cross(side).normalized()
    h = thick / 2
    ring = [side * h + up * h, side * h - up * h, -side * h - up * h, -side * h + up * h]
    verts = [p0 + r for r in ring] + [p1 + r for r in ring]
    faces = [(0, 1, 2, 3), (7, 6, 5, 4)]
    faces += [(i, (i + 1) % 4, 4 + (i + 1) % 4, 4 + i) for i in range(4)]
    return new_mesh(name, verts, faces, [mat])


def rect_loop(u0, v0, u1, v1, off=0.0):
    return [
        (u0 - off, v0 - off), (u1 + off, v0 - off),
        (u1 + off, v1 + off), (u0 - off, v1 + off),
    ]


def wind(verts, idx, want):
    """Return idx (or its reverse) so the polygon normal agrees with `want`."""
    a, b, c = (Vector(verts[i]) for i in idx[:3])
    return idx if (b - a).cross(c - b).dot(Vector(want)) >= 0 else tuple(reversed(idx))


def loft(name, rings, materials_, row_mats=None, cap_top=False, cap_bottom=False):
    """Loft equal-length closed plan loops (list of (z, points)) into a tube.

    Every face is wound against an explicitly derived outward direction rather
    than left to recalc_face_normals, which only guarantees consistency and
    cannot orient an open shell. The rings are read as a profile traversal that
    keeps solid material on one side: a rising strip is an outer wall and faces
    radially out, a falling strip is an inner wall and faces radially in, a
    horizontal strip is the top of the solid below when the plan steps inward
    and the underside of the solid above when it steps outward. That is what
    makes cornices, parapets, string courses and the rusticated grooves come
    out right.
    """
    n = len(rings[0][1])
    verts = []
    for z, loop in rings:
        verts.extend([(x, y, z) for x, y in loop])
    axis = Vector(
        (
            sum(p[0] for _, loop in rings for p in loop) / (n * len(rings)),
            sum(p[1] for _, loop in rings for p in loop) / (n * len(rings)),
            0.0,
        )
    )

    def mean_radius(loop):
        return sum(math.dist(p, (axis.x, axis.y)) for p in loop) / len(loop)

    faces, face_mats = [], []
    for r in range(len(rings) - 1):
        (z0, loop0), (z1, loop1) = rings[r], rings[r + 1]
        horizontal = abs(z1 - z0) < 1e-6
        step_in = mean_radius(loop1) < mean_radius(loop0)
        for i in range(n):
            j = (i + 1) % n
            quad = (r * n + i, r * n + j, (r + 1) * n + j, (r + 1) * n + i)
            if horizontal:
                want = (0.0, 0.0, 1.0 if step_in else -1.0)
            else:
                cx = (loop0[i][0] + loop0[j][0] + loop1[i][0] + loop1[j][0]) / 4
                cy = (loop0[i][1] + loop0[j][1] + loop1[i][1] + loop1[j][1]) / 4
                side = 1.0 if z1 > z0 else -1.0  # rising = outer, falling = inner
                want = ((cx - axis.x) * side, (cy - axis.y) * side, 0.0)
                if abs(want[0]) < 1e-9 and abs(want[1]) < 1e-9:
                    want = (0.0, 0.0, 1.0)
            faces.append(wind(verts, quad, want))
            face_mats.append(row_mats[r] if row_mats else 0)
    if cap_bottom:
        faces.append(wind(verts, tuple(range(n)), (0, 0, -1)))
        face_mats.append(0)
    if cap_top:
        off = (len(rings) - 1) * n
        faces.append(wind(verts, tuple(range(off, off + n)), (0, 0, 1)))
        face_mats.append(0)
    return new_mesh(name, verts, faces, materials_, face_mats, recalc=False)


def grooved_prism(name, u0, v0, u1, v1, z0, z1, grooves, mat, cap_top=True):
    """Extruded rectangle with recessed horizontal bands: the rusticated base."""
    rings = [(z0, rect_loop(u0, v0, u1, v1))]
    for gz in grooves:
        rings.append((gz, rect_loop(u0, v0, u1, v1)))
        rings.append((gz, rect_loop(u0, v0, u1, v1, -0.3)))
        rings.append((gz + 0.45, rect_loop(u0, v0, u1, v1, -0.3)))
        rings.append((gz + 0.45, rect_loop(u0, v0, u1, v1)))
    rings.append((z1, rect_loop(u0, v0, u1, v1)))
    return loft(name, rings, [mat], cap_top=cap_top, cap_bottom=True)


def ring_prism(name, outer, inner, z0, z1, wall_mat, top_mat=None, inner_mat=None):
    """A rectangular tube: outer walls, inner (courtyard) walls, flat top ring."""
    o = rect_loop(*outer)
    i = rect_loop(*inner)
    verts = [(x, y, z0) for x, y in o] + [(x, y, z1) for x, y in o]
    verts += [(x, y, z0) for x, y in i] + [(x, y, z1) for x, y in i]
    faces, mats = [], []
    for k in range(4):
        j = (k + 1) % 4
        faces.append((k, j, 4 + j, 4 + k))          # outer wall (CCW loop -> out)
        mats.append(0)
    for k in range(4):
        j = (k + 1) % 4
        faces.append((8 + j, 8 + k, 12 + k, 12 + j))  # inner wall faces courtyard
        mats.append(2 if inner_mat else 0)
    for k in range(4):
        j = (k + 1) % 4
        faces.append((4 + k, 4 + j, 12 + j, 12 + k))  # top ring
        mats.append(1 if top_mat else 0)
    faces.append((3, 2, 1, 0))
    mats.append(0)
    mlist = [wall_mat]
    if top_mat:
        mlist.append(top_mat)
    if inner_mat:
        mlist.append(inner_mat)
    return orient_outward(new_mesh(name, verts, faces, mlist, mats, recalc=False))


def punched_wall(name, origin, normal, length, z0, z1, cells, wall_mat, glass_mat,
                 depth=DEPTH, glass_override=None, back=PANEL_GAP):
    """A wall panel with recessed rectangular openings.

    origin: 3D point at s=0, z=0 on the panel face. normal: outward unit
    (grid-frame axis-aligned). s runs along normal x ez so that explicit
    winding gives outward faces without recalc. cells: (s0, s1, za, zb).
    glass_override: optional material per cell index.
    """
    n = Vector(normal)
    s_dir = n.cross(Vector((0, 0, 1))) * -1.0  # ez x s = n
    O = Vector(origin)

    def P(s, z, d=0.0):
        p = O + s_dir * s + Vector((0, 0, z)) - n * d
        return (p.x, p.y, p.z)

    verts, faces, mats = [], [], []

    def quad(a, b, c, d_, mi, want):
        base = len(verts)
        verts.extend([a, b, c, d_])
        faces.append(wind(verts, (base, base + 1, base + 2, base + 3), want))
        mats.append(mi)

    z_cuts = sorted({z0, z1} | {c[2] for c in cells} | {c[3] for c in cells})
    for za, zb in zip(z_cuts, z_cuts[1:]):
        row = sorted([c for c in cells if c[2] <= za and c[3] >= zb], key=lambda c: c[0])
        s = 0.0
        for c in row:
            if c[0] > s:
                quad(P(s, za), P(s, zb), P(c[0], zb), P(c[0], za), 0, n)
            s = c[1]
        if s < length:
            quad(P(s, za), P(s, zb), P(length, zb), P(length, za), 0, n)

    up = Vector((0, 0, 1))
    for idx, (s0, s1, za, zb) in enumerate(cells):
        gm = 1 if glass_override is None or glass_override[idx] is None else glass_override[idx]
        # reveals face into the opening, so the recess reads from outside
        quad(P(s0, za), P(s0, zb), P(s0, zb, depth), P(s0, za, depth), 0, s_dir)
        quad(P(s1, za, depth), P(s1, zb, depth), P(s1, zb), P(s1, za), 0, -s_dir)
        quad(P(s0, zb), P(s1, zb), P(s1, zb, depth), P(s0, zb, depth), 0, -up)
        quad(P(s0, za, depth), P(s1, za, depth), P(s1, za), P(s0, za), 0, up)
        quad(P(s0, za, depth), P(s0, zb, depth), P(s1, zb, depth), P(s1, za, depth), gm, n)

    # Close the panel's perimeter back to the core wall it stands in front of.
    # Without these returns the panels leave an open notch at every building
    # corner, through which a grazing view sees the panels' unlit back faces.
    if back:
        quad(P(0, z0), P(0, z1), P(0, z1, back), P(0, z0, back), 0, -s_dir)
        quad(P(length, z0, back), P(length, z1, back), P(length, z1),
             P(length, z0), 0, s_dir)
        quad(P(0, z1), P(length, z1), P(length, z1, back), P(0, z1, back), 0, up)
        quad(P(0, z0, back), P(length, z0, back), P(length, z0), P(0, z0), 0, -up)

    mlist = [wall_mat, glass_mat]
    extra = sorted({m for m in mats if m >= 2})
    return new_mesh(name, verts, faces, mlist, mats, recalc=False), extra


def glow_panes(name, origin, normal, cells, mat, depth=DEPTH, out=0.03):
    """Free-standing emissive panes sitting just in front of a wall plane.

    The app splits a landmark GLB into a lit body buffer and one unlit glow
    buffer keyed purely off the `_Glow` material suffix, then ramps the glow
    buffer's opacity from 0.12 (day) to 1.0 (night). A glow face is therefore
    ~88% transparent in daylight, so it must be a thin veneer with solid body
    geometry directly behind it — never the only skin at that spot. These panes
    hover `out` metres in front of the recessed window glass, which satisfies
    that: by day they barely tint the pane, by night they are the lit room.
    """
    n = Vector(normal)
    s_dir = n.cross(Vector((0, 0, 1))) * -1.0
    O = Vector(origin)

    def P(s, z):
        p = O + s_dir * s + Vector((0, 0, z)) - n * (depth - out)
        return (p.x, p.y, p.z)

    verts, faces = [], []
    for s0, s1, za, zb in cells:
        base = len(verts)
        verts.extend([P(s0, za), P(s0, zb), P(s1, zb), P(s1, za)])
        faces.append(wind(verts, (base, base + 1, base + 2, base + 3), n))
    if not faces:
        return None
    return new_mesh(name, verts, faces, [mat], recalc=False)


def lit_cells(cells, seed_text, share=3, modulus=8):
    """Deterministic subset of window cells: the rooms whose lights are on.

    Deterministic so the build stays reproducible — no randomness anywhere in
    this script — but scattered enough to read as an occupied hotel rather than
    a switchboard.
    """
    seed = sum((i + 1) * ord(c) for i, c in enumerate(seed_text))
    return [c for i, c in enumerate(cells) if (i * 7919 + seed * 131) % modulus < share]


def bays(length, margin, pitch=4.35, w=WIN_W):
    """Evenly spread window centres: as many bays as fit at ~pitch spacing."""
    span = length - 2 * margin
    count = max(1, round(span / pitch))
    return [(margin + span * (i + 0.5) / count - w / 2,
             margin + span * (i + 0.5) / count + w / 2) for i in range(count)]


def window_cells(length, margin, rows=None, pitch=4.35):
    rows = ROWS_Z if rows is None else rows
    return [(s0, s1, z, z + WIN_H) for (s0, s1) in bays(length, margin, pitch)
            for z in rows]


# --------------------------------------------------------------------- build


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    cream = material("Toy_cream")
    sand = material("Toy_sand")
    trim = material("Toy_trim")
    glass = material("Toy_glass")
    stone = material("Toy_stone")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    mint = material("Toy_mint")
    sky = material("Toy_sky")
    red = material("Toy_red")
    teal = material("Toy_teal")
    mustard = material("Toy_mustard")
    ink = material("Toy_ink")
    glow = material("Toy_white_Glow")
    gold_glow = material("Toy_gold_Glow")
    flag_mats = [red, teal, mustard, sky, mint]

    # === 1907 block =========================================================
    # Rusticated base: proud of the panel plane, deep horizontal grooves.
    grooved_prism("blk_base", BLK_U0 - 0.15, BLK_V0 - 0.15, BLK_U1 + 0.15,
                  BLK_V1 + 0.15, 0.0, H_BASE, [2.2, 4.4, 6.6], stone)

    # Body core: ring around the courtyard; cream walls, dark roof deck.
    ring_prism("blk_core",
               (BLK_U0 + PANEL_GAP, BLK_V0 + PANEL_GAP, BLK_U1 - PANEL_GAP, BLK_V1 - PANEL_GAP),
               (CRT_U0, CRT_V0, CRT_U1, CRT_V1),
               H_BASE, H_BODY, cream, top_mat=roofd, inner_mat=cream)

    # Punched facade panels (grid frame, outward normals).
    west_len = BLK_V1 - BLK_V0
    pav_w = 14.0
    # corner pavilions 3 bays, wings 4 bays, centre pavilion 5 bays
    # (s measured from the north end going south)
    segs = [
        (0.0, pav_w, 3),                                  # north corner pavilion
        (pav_w, BLK_V1 - PC_V1, 4),                       # north wing
        (BLK_V1 - PC_V1, BLK_V1 - PC_V0, 5),              # centre pavilion
        (BLK_V1 - PC_V0, west_len - pav_w, 4),            # south wing
        (west_len - pav_w, west_len, 3),                  # south corner pavilion
    ]
    wcells = []
    for a, b, count in segs:
        span = b - a
        for i in range(count):
            c = a + span * (i + 0.5) / count
            for z in ROWS_Z:
                wcells.append((c - WIN_W / 2, c + WIN_W / 2, z, z + WIN_H))
    punched_wall("blk_wall_w", (BLK_U0, BLK_V1, 0), (-1, 0, 0), west_len,
                 H_BASE, H_BODY, wcells, cream, glass)

    scells = window_cells(BLK_U1 - BLK_U0, 2.6)
    ncells = window_cells(BLK_U1 - BLK_U0, 2.6)
    ecells = window_cells(BLK_V1 - BLK_V0, 2.6, rows=ROWS_Z[1:])
    punched_wall("blk_wall_s", (BLK_U0, BLK_V0, 0), (0, -1, 0), BLK_U1 - BLK_U0,
                 H_BASE, H_BODY, scells, cream, glass)
    punched_wall("blk_wall_n", (BLK_U1, BLK_V1, 0), (0, 1, 0), BLK_U1 - BLK_U0,
                 H_BASE, H_BODY, ncells, cream, glass)
    punched_wall("blk_wall_e", (BLK_U1, BLK_V0, 0), (1, 0, 0), BLK_V1 - BLK_V0,
                 POD_H + 0.7, H_BODY, ecells, cream, glass)

    # --- night: lit rooms on the block ------------------------------------
    # The west wall's pavilion stretches are buried behind the projecting
    # pavilions, so only the exposed wings get panes there.
    covered = [(0.0, pav_w), (BLK_V1 - PC_V1 - 2.6, BLK_V1 - PC_V0 + 2.6),
               (west_len - pav_w, west_len)]
    exposed = [c for c in wcells
               if not any(a - 0.1 <= c[0] and c[1] <= b + 0.1 for a, b in covered)]
    glow_panes("glow_win_w", (BLK_U0, BLK_V1, 0), (-1, 0, 0),
               lit_cells(exposed, "west"), gold_glow)
    glow_panes("glow_win_s", (BLK_U0, BLK_V0, 0), (0, -1, 0),
               lit_cells(scells, "south"), gold_glow)
    glow_panes("glow_win_n", (BLK_U1, BLK_V1, 0), (0, 1, 0),
               lit_cells(ncells, "north"), gold_glow)
    glow_panes("glow_win_e", (BLK_U1, BLK_V0, 0), (1, 0, 0),
               lit_cells(ecells, "east"), gold_glow)

    # String course and cornice ring with cresting (chunky, rhythmic).
    loft("blk_string",
         [(12.9, rect_loop(BLK_U0, BLK_V0, BLK_U1, BLK_V1, 0.05)),
          (12.9, rect_loop(BLK_U0, BLK_V0, BLK_U1, BLK_V1, 0.5)),
          (13.35, rect_loop(BLK_U0, BLK_V0, BLK_U1, BLK_V1, 0.5)),
          (13.35, rect_loop(BLK_U0, BLK_V0, BLK_U1, BLK_V1, 0.05))],
         [trim], cap_top=False, cap_bottom=False)
    # The profile closes with an inner face dropping back to the roof deck, so
    # the parapet is solid when the app camera looks down into the block.
    loft("blk_cornice",
         [(H_BODY - 0.4, rect_loop(BLK_U0, BLK_V0, BLK_U1, BLK_V1, 0.1)),
          (H_BODY, rect_loop(BLK_U0, BLK_V0, BLK_U1, BLK_V1, 1.3)),
          (H_CORN, rect_loop(BLK_U0, BLK_V0, BLK_U1, BLK_V1, 1.3)),
          (H_CORN, rect_loop(BLK_U0, BLK_V0, BLK_U1, BLK_V1, -0.6)),
          (H_BODY - 0.4, rect_loop(BLK_U0, BLK_V0, BLK_U1, BLK_V1, -0.6))],
         [trim], cap_top=False, cap_bottom=False)
    # Night: the lit cornice line — the real hotel's brightest element after
    # the entrance. It rides the cornice's own outer face rather than tucking
    # under the overhang, where the app's downward camera would never see it.
    # Thin veneer with solid cornice behind, so daylight barely registers it.
    loft("glow_cornice_line",
         [(H_BODY + 0.25, rect_loop(BLK_U0, BLK_V0, BLK_U1, BLK_V1, 1.37)),
          (H_CORN - 0.25, rect_loop(BLK_U0, BLK_V0, BLK_U1, BLK_V1, 1.37))],
         [glow], cap_top=False, cap_bottom=False)

    # Cresting blocks along the cornice edge — the roofline fringe.
    ring = rect_loop(BLK_U0, BLK_V0, BLK_U1, BLK_V1, 0.9)
    per, segs2 = [], []
    for i in range(4):
        a, b = Vector(ring[i]), Vector(ring[(i + 1) % 4])
        L = (b - a).length
        count = int(L // 2.7)
        for k in range(count):
            t = (k + 0.5) / count
            p = a.lerp(b, t)
            per.append((p.x, p.y))
    for i, (cx, cy) in enumerate(per):
        if abs(cx - BLK_U0 - (BLK_U1 - BLK_U0) / 2) > (BLK_U1 - BLK_U0) / 2 - 4.5 and \
           abs(cy - BLK_V0 - (BLK_V1 - BLK_V0) / 2) > (BLK_V1 - BLK_V0) / 2 - 4.5:
            continue  # corners host the parapet blocks
        box(f"crest_{i}", cx - 0.36, cy - 0.36, cx + 0.36, cy + 0.36,
            H_CORN, H_CREST, trim)

    # Corner parapet blocks + rooftop flagpoles (US / California cues).
    corners = [(BLK_U0, BLK_V0), (BLK_U0, BLK_V1), (BLK_U1, BLK_V0), (BLK_U1, BLK_V1)]
    for i, (cu, cv) in enumerate(corners):
        du = 1 if cu == BLK_U0 else -1
        dv = 1 if cv == BLK_V0 else -1
        bevel(box(f"parapet_{i}", min(cu, cu + du * 5.4), min(cv, cv + dv * 5.4),
                  max(cu, cu + du * 5.4), max(cv, cv + dv * 5.4),
                  H_CORN, H_PARAPET, trim))
    for i, (cu, cv, mat) in enumerate(((BLK_U0 + 2.7, BLK_V1 - 2.7, red),
                                       (BLK_U0 + 2.7, BLK_V0 + 2.7, teal))):
        stick(f"roof_pole_{i}", (cu, cv, H_PARAPET), (cu, cv, H_PARAPET + 8.5), 0.22, steel)
        box(f"roof_flag_{i}", cu + 0.11, cv - 0.06, cu + 1.81, cv + 0.06,
            H_PARAPET + 7.2, H_PARAPET + 8.3, mat)

    # Roof penthouses — the block's top is very exposed to the app camera.
    for name, (pu0, pv0, pu1, pv1, ph) in {
        "penthouse_a": (3.0, 14.0, 17.0, 24.0, 4.6),
        "penthouse_b": (4.0, -42.0, 15.0, -34.0, 3.4),
        "penthouse_c": (-38.0, 22.0, -31.0, 27.5, 2.6),
    }.items():
        bevel(box(name, pu0, pv0, pu1, pv1, H_BODY, H_BODY + ph, cream))
        box(f"{name}_cap", pu0 - 0.35, pv0 - 0.35, pu1 + 0.35, pv1 + 0.35,
            H_BODY + ph, H_BODY + ph + 0.45, roofd)

    # Rooftop clusters (style bible §10: the roof is a second facade).
    for i, (mu, mv, mw, md, mh) in enumerate((
        (-40.0, -30.0, 5.0, 4.0, 1.7),
        (-33.5, -30.0, 4.0, 4.0, 1.2),
        (-40.0, -24.0, 5.0, 3.2, 1.0),
        (10.0, -12.0, 4.6, 4.6, 1.5),
        (10.0, -5.5, 4.6, 3.4, 1.1),
    )):
        bevel(box(f"roof_mech_{i}", mu, mv, mu + mw, mv + md,
                  H_BODY, H_BODY + mh, steel), width=0.2)
    for i, (gu, gv) in enumerate(((-38.0, 8.0), (-38.0, 14.0), (8.0, 26.0), (14.0, 26.0))):
        bevel(box(f"roof_planter_{i}", gu, gv, gu + 4.2, gv + 3.4,
                  H_BODY, H_BODY + 1.2, mint), width=0.25)

    # Roof-garden courtyard: the terrace sits one storey below the roof deck so
    # the app's downward camera reads a garden, not a 20 m shaft.
    H_GARDEN = H_BODY - 3.2
    box("crt_floor", CRT_U0, CRT_V0, CRT_U1, CRT_V1, H_GARDEN - 0.4, H_GARDEN, mint)
    cx, cy = (CRT_U0 + CRT_U1) / 2, (CRT_V0 + CRT_V1) / 2
    ring_r = 4.6
    seg = 14
    pool = [(cx + ring_r * math.cos(2 * math.pi * i / seg),
             cy + ring_r * math.sin(2 * math.pi * i / seg)) for i in range(seg)]
    pool_in = [(cx + (ring_r - 0.5) * math.cos(2 * math.pi * i / seg),
                cy + (ring_r - 0.5) * math.sin(2 * math.pi * i / seg)) for i in range(seg)]
    loft("crt_pool_rim",
         [(H_GARDEN, pool), (H_GARDEN + 0.55, pool),
          (H_GARDEN + 0.55, pool_in), (H_GARDEN + 0.35, pool_in)],
         [trim], cap_top=False, cap_bottom=False)
    water = pool_in
    new_mesh("crt_pool_water", [(x, y, H_GARDEN + 0.4) for x, y in water],
             [tuple(range(seg))], [sky])
    for i, (hu, hv, hw, hh) in enumerate(((CRT_U0 + 3.2, CRT_V0 + 5.0, 4.4, 2.6),
                                          (CRT_U1 - 7.6, CRT_V1 - 7.4, 4.4, 2.6),
                                          (CRT_U0 + 3.2, CRT_V1 - 9.0, 3.2, 3.6),
                                          (CRT_U1 - 7.6, CRT_V0 + 4.0, 3.2, 3.0))):
        bevel(box(f"crt_hedge_{i}", hu, hv, hu + hw, hv + hh,
                  H_GARDEN, H_GARDEN + 1.1, mint), width=0.3)
    # terrace parapet so the garden reads as a designed outdoor room
    loft("crt_parapet",
         [(H_BODY - 0.6, rect_loop(CRT_U0, CRT_V0, CRT_U1, CRT_V1, 0.35)),
          (H_BODY, rect_loop(CRT_U0, CRT_V0, CRT_U1, CRT_V1, 0.35)),
          (H_BODY, rect_loop(CRT_U0, CRT_V0, CRT_U1, CRT_V1, -0.15))],
         [trim], cap_top=False, cap_bottom=False)

    # West front: projecting centre and corner pavilions give the Beaux-Arts
    # relief; the giant colonnade (floors 4-7) stands against the centre one.
    for name, (pv0, pv1, out) in {
        "pav_centre": (PC_V0 - 2.6, PC_V1 + 2.6, 1.5),
        "pav_corner_n": (BLK_V1 - pav_w, BLK_V1, 0.9),
        "pav_corner_s": (BLK_V0, BLK_V0 + pav_w, 0.9),
    }.items():
        bevel(box(name, BLK_U0 - out + PANEL_GAP, pv0, BLK_U0 + 0.6, pv1,
                  H_BASE, H_BODY, cream))
        box(f"{name}_cornice", BLK_U0 - out - 0.75, pv0 - 0.75, BLK_U0 + 0.6,
            pv1 + 0.75, H_BODY - 0.35, H_CORN, trim)
        # keep the window rhythm alive on the projecting faces
        cells_p = [(s0, s1, z, z + WIN_H)
                   for (s0, s1) in bays(pv1 - pv0, 2.6, 4.6)
                   for z in ROWS_Z]
        punched_wall(f"{name}_face", (BLK_U0 - out, pv1, 0), (-1, 0, 0), pv1 - pv0,
                     H_BASE, H_BODY, cells_p, cream, glass)
        glow_panes(f"glow_win_{name}", (BLK_U0 - out, pv1, 0), (-1, 0, 0),
                   lit_cells(cells_p, name), gold_glow)
    grooved_prism("pav_centre_base", BLK_U0 - 1.5, PC_V0 - 2.6, BLK_U0,
                  PC_V1 + 2.6, 0.0, H_BASE, [2.2, 4.4, 6.6], stone)
    # Semantically enlarged so the order still reads from the city camera (§9).
    ncol = 6
    col_u = BLK_U0 - 2.4
    for i in range(ncol):
        v = PC_V0 + (PC_V1 - PC_V0) * (i + 0.5) / ncol
        col = [(col_u + 1.05 * math.cos(2 * math.pi * k / 10),
                v + 1.05 * math.sin(2 * math.pi * k / 10)) for k in range(10)]
        loft(f"col_{i}", [(13.4, col), (26.4, col)], [trim], cap_top=True, cap_bottom=True)
        box(f"col_cap_{i}", col_u - 1.35, v - 1.35, col_u + 1.35, v + 1.35, 26.4, 27.5, trim)
        box(f"col_base_{i}", col_u - 1.3, v - 1.3, col_u + 1.3, v + 1.3, 12.4, 13.4, trim)
    loft("colonnade_entab",
         [(27.5, rect_loop(col_u - 1.5, PC_V0 - 0.6, BLK_U0 + 0.2, PC_V1 + 0.6)),
          (29.0, rect_loop(col_u - 1.5, PC_V0 - 0.6, BLK_U0 + 0.2, PC_V1 + 0.6))],
         [trim], cap_top=True, cap_bottom=True)
    # Night: the colonnade recess is uplit from its plinth and downlit from the
    # entablature — the pair of bands that makes a classical order read at dusk.
    for tag, (gz0, gz1) in {"plinth": (12.6, 13.5), "entab": (26.7, 27.4)}.items():
        box(f"glow_colonnade_{tag}", BLK_U0 - 1.66, PC_V0 - 0.4,
            BLK_U0 - 1.54, PC_V1 + 0.4, gz0, gz1, glow)

    # Porte-cochere: stone pavilion, deep ink entries, glow fascia, flag arc.
    grooved_prism("pc_body", PC_U0, PC_V0, PC_U1 + 0.3, PC_V1, 0.0, PC_H,
                  [2.2, 4.4], stone)
    pc_len = PC_V1 - PC_V0
    pc_cells = [(2.0, 6.6, 0.8, 6.4), (8.2, 13.1, 0.8, 6.9), (14.7, 19.3, 0.8, 6.4)]
    punched_wall("pc_face", (PC_U0, PC_V1, 0), (-1, 0, 0), pc_len, 0.0, PC_H,
                 pc_cells, stone, ink, depth=1.3)
    box("pc_fascia", PC_U0 - 0.12, PC_V0 + 0.6, PC_U0 + 0.05, PC_V1 - 0.6,
        6.9, 7.75, glow)
    # Night: warm light spilling out of the lobby doors under the porte-cochere.
    glow_panes("glow_pc_doors", (PC_U0, PC_V1, 0), (-1, 0, 0), pc_cells,
               gold_glow, depth=1.3, out=0.06)
    # balustrade
    loft("pc_balustrade",
         [(PC_H, rect_loop(PC_U0, PC_V0, PC_U1 + 0.3, PC_V1, 0.12)),
          (PC_H + 0.32, rect_loop(PC_U0, PC_V0, PC_U1 + 0.3, PC_V1, 0.12))],
         [trim], cap_top=True, cap_bottom=True)
    nb = 12
    for i in range(nb):
        v = PC_V0 + 0.9 + (pc_len - 1.8) * i / (nb - 1)
        box(f"pc_post_{i}", PC_U0 - 0.02, v - 0.14, PC_U0 + 0.26, v + 0.14,
            PC_H + 0.32, PC_H + 1.05, trim)
    # the arc of international flags — the one-second identity cue
    nflags = 15
    for i in range(nflags):
        t = i / (nflags - 1)
        v = PC_V0 + 1.2 + (pc_len - 2.4) * t
        bulge = math.sin(t * math.pi) * 0.5
        b0 = (PC_U0 + 0.15 - bulge, v, PC_H + 0.9)
        tip = (b0[0] - 2.1, v, b0[2] + 2.6)
        stick(f"flag_pole_{i}", b0, tip, 0.13, steel)
        box(f"flag_{i}", tip[0] - 0.2, v - 0.07, tip[0] + 1.25, v + 0.07,
            tip[2] - 1.15, tip[2] - 0.08, flag_mats[i % 5])

    # === podium + roof terrace =============================================
    grooved_prism("pod_body", POD_U0, POD_V0, POD_U1 + 0.15, POD_V1, 0.0, POD_H,
                  [2.2, 4.4, 6.6], stone)
    punched_wall("pod_arcade_s", (POD_U0 + 0.15, POD_V0 - 0.001, 0), (0, -1, 0),
                 POD_U1 - POD_U0, 0.0, POD_H,
                 [(s0, s1, 2.0, 9.2) for (s0, s1) in bays(POD_U1 - POD_U0, 2.4, 5.2, 3.4)],
                 stone, glass, depth=0.8)
    # Ends sink 0.4 m into the podium: overlapping beats coincident, which
    # would let a grazing ray slip through the seam onto a back face.
    loft("pod_rail",
         [(POD_H - 0.4, rect_loop(POD_U0, POD_V0, POD_U1, POD_V1, 0.05)),
          (POD_H + 0.75, rect_loop(POD_U0, POD_V0, POD_U1, POD_V1, 0.05)),
          (POD_H + 0.75, rect_loop(POD_U0, POD_V0, POD_U1, POD_V1, -0.45)),
          (POD_H - 0.4, rect_loop(POD_U0, POD_V0, POD_U1, POD_V1, -0.45))],
         [trim], cap_top=False, cap_bottom=False)
    for i, (pu, pv) in enumerate(((POD_U0 + 4.5, POD_V0 + 5.0), (POD_U0 + 4.5, POD_V1 - 9.0),
                                  (POD_U1 - 8.5, POD_V1 - 9.0), (POD_U1 - 8.5, POD_V0 + 5.0))):
        bevel(box(f"pod_planter_{i}", pu, pv, pu + 4.0, pv + 4.0, POD_H, POD_H + 1.5, mint),
              width=0.25)

    # === 1961/62 tower ======================================================
    grooved_prism("twr_base", TWR_U0 - 0.15, TWR_V0 - 0.15, TWR_U1 + 0.15,
                  TWR_V1 + 0.15, 0.0, POD_H, [2.2, 4.4, 6.6], stone)
    core = bevel(box("twr_core", TWR_U0 + PANEL_GAP, TWR_V0 + PANEL_GAP,
                     TWR_U1 - PANEL_GAP, TWR_V1 - PANEL_GAP, POD_H, TWR_ROOF, sand),
                 width=0.15)
    twr_len = TWR_V1 - TWR_V0
    strip_cells = []
    nstrip = 7
    for i in range(nstrip):
        c = 2.6 + (twr_len - 5.2) * (i + 0.5) / nstrip
        strip_cells.append((c - 1.05, c + 1.05, 13.0, 88.6))
    punched_wall("twr_wall_w", (TWR_U0, TWR_V1, 0), (-1, 0, 0), twr_len,
                 POD_H + 0.6, 89.4, strip_cells, sand, glass)
    punched_wall("twr_wall_e", (TWR_U1, TWR_V0, 0), (1, 0, 0), twr_len,
                 POD_H + 0.6, 89.4, strip_cells, sand, glass)

    # Night: individual lit rooms inside the tower's vertical glass strips —
    # one cell per strip per storey, a deterministic scatter of about a third.
    room_cells = [(s0 + 0.15, s1 - 0.15, 14.9 + f * 3.3, 14.9 + f * 3.3 + 2.1)
                  for (s0, s1, _, _) in strip_cells for f in range(22)]
    glow_panes("glow_rooms_w", (TWR_U0, TWR_V1, 0), (-1, 0, 0),
               lit_cells(room_cells, "tower-west"), gold_glow)
    glow_panes("glow_rooms_e", (TWR_U1, TWR_V0, 0), (1, 0, 0),
               lit_cells(room_cells, "tower-east"), gold_glow)
    # Floor lines grouped one band per ~2 storeys, so the rhythm survives the
    # city camera instead of aliasing into mush (style bible §26).
    for f in range(12):
        z = 15.4 + f * 6.6
        box(f"twr_ledge_w_{f}", TWR_U0 - 0.22, TWR_V0 + 1.6, TWR_U0 + 0.1,
            TWR_V1 - 1.6, z, z + 0.7, sand)
        box(f"twr_ledge_e_{f}", TWR_U1 - 0.1, TWR_V0 + 1.6, TWR_U1 + 0.22,
            TWR_V1 - 1.6, z, z + 0.7, sand)
    # narrow window column on the blank ends + the little round balcony (N)
    twr_wid = TWR_U1 - TWR_U0
    punched_wall("twr_wall_n", (TWR_U1, TWR_V1, 0), (0, 1, 0), twr_wid,
                 POD_H + 0.6, 89.4, [(twr_wid / 2 - 1.0, twr_wid / 2 + 1.0, 13.0, 88.6)],
                 sand, glass)
    punched_wall("twr_wall_s", (TWR_U0, TWR_V0, 0), (0, -1, 0), twr_wid,
                 POD_H + 0.6, 89.4, [(twr_wid / 2 - 1.0, twr_wid / 2 + 1.0, 13.0, 88.6)],
                 sand, glass)
    bal_c = ((TWR_U0 + TWR_U1) / 2, TWR_V1)
    bal = [(bal_c[0] + 2.1 * math.cos(math.pi * i / 7), bal_c[1] + 2.1 * math.sin(math.pi * i / 7))
           for i in range(8)]
    loft("twr_balcony", [(83.0, bal), (84.1, bal)], [trim], cap_top=True, cap_bottom=True)

    # Crown Room band + glow fascia + picket crown parapet.
    loft("twr_crown_glass",
         [(CROWN_GLASS0, rect_loop(TWR_U0, TWR_V0, TWR_U1, TWR_V1, -0.35)),
          (CROWN_GLASS1, rect_loop(TWR_U0, TWR_V0, TWR_U1, TWR_V1, -0.35))],
         [glass], cap_top=False, cap_bottom=False)
    # Night: the Crown Room band. Kept as a thin veneer just outside the glass
    # so the daytime band still reads as dark glazing, not washed-out gold.
    loft("glow_crown_room",
         [(CROWN_GLASS0 + 0.5, rect_loop(TWR_U0, TWR_V0, TWR_U1, TWR_V1, -0.28)),
          (CROWN_GLASS1 - 0.5, rect_loop(TWR_U0, TWR_V0, TWR_U1, TWR_V1, -0.28))],
         [gold_glow], cap_top=False, cap_bottom=False)
    loft("twr_crown_fascia",
         [(CROWN_GLASS1, rect_loop(TWR_U0, TWR_V0, TWR_U1, TWR_V1, 0.4)),
          (TWR_ROOF, rect_loop(TWR_U0, TWR_V0, TWR_U1, TWR_V1, 0.4)),
          (TWR_ROOF, rect_loop(TWR_U0, TWR_V0, TWR_U1, TWR_V1, -0.2))],
         [glow], cap_top=False, cap_bottom=False)
    # tower roof deck: dark, so the crown ring and mechanical blocks read
    new_mesh("twr_roof_deck",
             [(x, y, TWR_ROOF + 0.03) for x, y in
              rect_loop(TWR_U0, TWR_V0, TWR_U1, TWR_V1, -0.2)],
             [(0, 1, 2, 3)], [roofd])
    ring2 = rect_loop(TWR_U0, TWR_V0, TWR_U1, TWR_V1, 0.35)
    idx = 0
    for i in range(4):
        a, b = Vector(ring2[i]), Vector(ring2[(i + 1) % 4])
        L = (b - a).length
        count = int(L // 2.3)
        for k in range(count):
            p = a.lerp(b, (k + 0.5) / count)
            box(f"picket_{idx}", p.x - 0.24, p.y - 0.24, p.x + 0.24, p.y + 0.24,
                TWR_ROOF, TWR_TOP, trim)
            idx += 1
    for i, (cu, cv) in enumerate(rect_loop(TWR_U0, TWR_V0, TWR_U1, TWR_V1, 0.35)):
        box(f"picket_c_{i}", cu - 0.38, cv - 0.38, cu + 0.38, cv + 0.38,
            TWR_ROOF, TWR_TOP, trim)
    bevel(box("twr_mech_a", TWR_U0 + 4.0, TWR_V0 + 6.0, TWR_U0 + 11.0, TWR_V0 + 12.0,
              TWR_ROOF, TWR_ROOF + 1.6, steel))
    bevel(box("twr_mech_b", TWR_U1 - 10.0, TWR_V1 - 13.0, TWR_U1 - 4.0, TWR_V1 - 7.0,
              TWR_ROOF, TWR_ROOF + 1.3, steel))

    return scene


# ------------------------------------------------- orient, centre and report


def finalize():
    """Yaw to the measured grid, centre the bbox, keep min Z at 0."""
    c, s = math.cos(YAW), math.sin(YAW)
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    for o in meshes:
        for v in o.data.vertices:
            x, y = v.co.x, v.co.y
            v.co.x, v.co.y = c * x - s * y, s * x + c * y
        o.data.update()
        for v in o.data.vertices:
            for i in range(3):
                mn[i] = min(mn[i], v.co[i])
                mx[i] = max(mx[i], v.co[i])
    centre = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, 0.0))
    for o in meshes:
        for v in o.data.vertices:
            v.co -= centre
        o.data.update()

    # anchor of the recentred origin, for REPORT.md
    lat0 = 37.7924935
    lon0 = -122.4101606
    lon = lon0 + centre.x / (111320.0 * math.cos(math.radians(lat0)))
    lat = lat0 + centre.y / 110540.0
    print(f"[build] recentre shift x={centre.x:.3f} y={centre.y:.3f}")
    print(f"[build] manifest anchor lon={lon:.7f} lat={lat:.7f}")

    dg = bpy.context.evaluated_depsgraph_get()
    tris = 0
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for o in meshes:
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    print(f"[build] objects={len(meshes)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 4) for i in range(3)]}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    finalize()

    blend = os.path.join(out, "fairmont-san-francisco.blend")
    glb = os.path.join(out, "fairmont-san-francisco.glb")
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
