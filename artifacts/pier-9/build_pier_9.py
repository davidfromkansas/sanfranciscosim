"""Deterministic Blender build of the SF-SIM miniature Pier 9.

    blender -b --python build_pier_9.py -- [--out DIR]

Writes pier-9.blend and pier-9.glb next to this file (or into --out). Geometry
is authored in world space in metres, Z up, +X east, +Y north, so the model
drops into the city at its real-world heading - the loader applies no rotation.

ORIGIN: deck-top rule (the pier-1 precedent). Local Z = 0 is the TOP OF THE
PIER DECK; the deck fascia and pile stubs run down to -2.6 m. placeGeneric()
seats the GLB's origin on one terrain sample at the anchor, and the app's DEM
carries this pier as a ~2.5 m ridge, so a model sitting on z = 0 would float
2.6 m above its own deck. `targetHeightM` is the model's total VERTICAL EXTENT
(-2.6 .. +15.0 = 17.6 m), not a height above water. See the plan's 2.3.

Design (see REFERENCE.md for the sources behind every number):

* a 1936-38 reinforced-concrete finger pier, twin of Pier 19: a classical
  stucco BULKHEAD BUILDING (broad central pavilion, monumental arch, gabled
  parapet, PIER 9 in raised letters, attic crest 15.0 m) across the full 49 m
  width, then a 240 m steel-framed TRANSIT SHED with scored precast concrete
  walls, eaves 7.3 m, under a DARK built-up roof that rises to a continuous
  glazed MONITOR (top 10.3 m) on the shed's centreline;
* the shed is OFFSET SOUTH in the deck: ~10 m of working apron on the north
  flank (with a broken run of freight containers), ~4 m on the south. The
  asymmetry is measured (DataSF ring in the pier frame) and is kept;
* the bay end is faintly Art Deco - six profiled pilasters rising to peaks and
  a gabled centre - and carries the BAR PILOTS station: an annex widening the
  last bays of the north side, a lookout volume over the roof, two short masts
  (all kept below the +15.0 bulkhead crest, which must set the bbox top);
* the roof is honestly NEAR-BLACK (Toy_roofd): the real six-ply built-up
  roofing reads charcoal in every aerial. Pale grey plant boxes cluster on the
  south plane (the Autodesk-era mechanical crowd), the north plane is cleaner;
* night: the arch screen is the hero, a partial scattered run of the monitor
  and the Bar Pilots lookout support it, amber apron lamps draw the pier's
  line into the bay. The PIER 9 letters do NOT glow (raised metal, not a
  sign). Glow surfaces are open faces proud of the opaque geometry, never
  closed shells - except the lamp globes, which ARE the light source.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

LON0P, LAT0P = -122.4375, 37.77
LON_M = 111320.0 * math.cos(math.radians(LAT0P))
LAT_M = 110540.0

# The design frame's origin: the measured OBB centre of the building ring -
# (along 0, perp 0) - which is also the manifest anchor.
DESIGN_ANCHOR = (-122.3967912, 37.8006745)

AXIS_BEARING = 54.59          # min-area OBB over OSM way 25478417

# --- plan geometry, in (along a, perp p) metres. See plan 2.3.
A_FRONT = -127.5              # Embarcadero building line
A_BULK_BACK = -116.5          # back of the bulkhead / start of the shed head
A_HEAD_END = -91.0            # shed head -> north-wall loft
A_LOFT_END = -78.0            # end of the north-wall loft -> main shed
A_SHED_END = 123.5            # bay-end wall of the shed
A_DECK_END = 126.8            # north-east edge of the deck

P_BULK_NW = -23.8             # bulkhead north-west end
P_BULK_SE = 25.3              # bulkhead south-east end
P_HEAD_NW = -20.3             # shed-head north wall
P_MAIN_NW = -14.9             # main shed north wall
P_MAIN_SE = 19.9              # main shed south wall
P_HEAD_SE0 = 23.9             # shed-head south wall at the bulkhead...
A_TAPER_SE = -104.0           # ...tapering to P_MAIN_SE by here

P_DECK_NW = -25.0
P_DECK_SE = 23.5

# --- heights above the deck
Z_PILE_BOT = -2.6             # the model's min Z
Z_DECK_BOT = -1.2
Z_PLINTH = 0.8
Z_BELT = 3.8
Z_EAVE = 7.3                  # shed wall top
Z_ROOF_HI = 8.6               # roof planes rise to this at the monitor edges
Z_MON_GL0, Z_MON_GL1 = 8.9, 10.0   # monitor clerestory band
Z_MON_TOP = 10.3              # monitor cap
Z_WING = 8.5                  # bulkhead wing parapet
Z_WING_COPE = 8.8
Z_CORNICE = 10.0              # pavilion cornice / gable springing
Z_APEX = 13.7                 # gable apex
Z_CREST = 15.0                # attic block top - the bbox top

# --- the frontispiece
PAV_P = 1.5                   # pavilion centre (the drive axis through the shed)
PAV_W = 19.0
PAV_PROUD = 0.6
PIER_W = 3.0                  # the monumental banded piers flanking the arch
ARCH_W = 11.3                 # real ~9.8 m, enlarged per style bible s.8/s.9
ARCH_SPRING = 3.4
ARCH_SEGS = 10
VOUSSOIR = 0.8                # width of the archivolt ring

# --- shed rhythm
SHED_BAY = 7.5
SHED_PIL_W, SHED_PIL_PROUD = 0.6, 0.08
SHED_WIN_Z = (4.2, 6.6)
RECESS = 0.14
# roll-up door bays (every 4th), plus the two 1970 enlarged doors on the south
DOOR_Z = (0.2, 3.5)
# centres of the enlarged 1970 south doors - placed BETWEEN the regular door
# bays (b % 4 == 1 lands at ...-15.25, 14.75, 44.75...) so no door-on-door
BIG_DOORS_A = (-26.5, 28.5)

# --- monitor
MON_HALF = 4.5
MON_A0, MON_A1 = -95.0, 121.5
SHED_MC = (P_MAIN_NW + P_MAIN_SE) / 2.0      # +2.5, the shed's own centreline
# lit stretches of the monitor at night (scattered, ~1/3 of the length)
MON_LIT = ((-60.0, -25.0), (5.0, 45.0), (80.0, 105.0))

RAIL_Z = 1.1
RAIL_PITCH = 4.5
BOLLARD_PITCH = 13.0
LAMP_H = 5.5
LAMP_PITCH = 24.0

BEVEL_W, BEVEL_SEG = 0.10, 2
EMBED = 0.03

# Which shed windows are lit at night, by bay index. Scattered on purpose.
LIT_BAYS = (2, 3, 7, 12, 18, 24, 29)

PALETTE_HEX = {
    "Toy_cream": "f2ede3",     # bulkhead walls, wings, pavilion body
    "Toy_white": "f7f4ec",     # pavilion trim, archivolt, copings, attic
    "Toy_stone": "d9d2c2",     # shed walls, pilasters, plinths, end pilasters
    "Toy_steel": "9aa0a6",     # deck/apron asphalt-grey, doors, plant, railing
    "Toy_ink": "3a3530",       # fascia, piles, fenders, bollards, lamps, letters
    "Toy_roofd": "45454a",     # the near-black roof planes and monitor cap
    "Toy_navy": "2c4a70",      # container accent
    "Toy_rust": "a86444",      # container accent
    "Toy_glass": "2a4d73",     # glazing - graphical, opaque, recessed
    "Toy_glassl": "6f95b8",    # monitor glazing, lookout band, transoms
    # Night. A _Glow material's BASE colour is what the app draws at night (the
    # glow layer is unlit), so these are authored as the colour to be SEEN.
    "Toy_glassl_Glow": "f4dcb0",   # the arch screen - warm, the hero
    "Toy_glass_Glow": "cbd8e0",    # monitor stretches, lookout, lit windows
    "Toy_amber_Glow": "e8b563",    # apron lamp globes (off-palette WARN, noted)
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

_R = math.radians(AXIS_BEARING)
U = (math.sin(_R), math.cos(_R))          # along, to the north-east
V = (math.cos(_R), -math.sin(_R))         # perp, to the south-east


def W(a, p):
    """Pier-frame (along, perp) -> world XY metres."""
    return (a * U[0] + p * V[0], a * U[1] + p * V[1])


def poly(pts):
    return [W(a, p) for a, p in pts]


# --------------------------------------------------------------- mesh helpers


def new_mesh(name, verts, faces, materials, face_mats=None, recalc=True):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    for m in materials:
        mesh.materials.append(m)
    if face_mats:
        for pol, mi in zip(mesh.polygons, face_mats):
            pol.material_index = mi
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


def offset_polygon(poly_xy, d):
    """Offset a simple polygon by `d` (positive = outward for a CCW ring)."""
    n = len(poly_xy)
    s2 = 0.0
    for i in range(n):
        a, b = poly_xy[i], poly_xy[(i + 1) % n]
        s2 += a[0] * b[1] - b[0] * a[1]
    sgn = 1.0 if s2 > 0.0 else -1.0
    lines = []
    for i in range(n):
        a, b = poly_xy[i], poly_xy[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy) or 1.0
        nx, ny = dy / m * sgn, -dx / m * sgn
        lines.append((a[0] + nx * d, a[1] + ny * d, dx / m, dy / m))
    out = []
    for i in range(n):
        px, py, ux, uy = lines[i - 1]
        qx, qy, vx, vy = lines[i]
        den = ux * vy - uy * vx
        if abs(den) < 1e-9:
            out.append((qx, qy))
            continue
        t = ((qx - px) * vy - (qy - py) * vx) / den
        out.append((px + ux * t, py + uy * t))
    return out


def rim(name, poly_xy, thickness, z0, z1, mat):
    """A closed ring band (parapet coping) - never a slab over the roof."""
    outer = poly_xy
    inner = offset_polygon(poly_xy, -thickness)
    n = len(outer)
    verts = ([(x, y, z0) for x, y in outer] + [(x, y, z1) for x, y in outer] +
             [(x, y, z0) for x, y in inner] + [(x, y, z1) for x, y in inner])
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
        faces.append((2 * n + j, 2 * n + i, 3 * n + i, 3 * n + j))
        faces.append((n + i, n + j, 3 * n + j, 3 * n + i))
        faces.append((j, i, 2 * n + i, 2 * n + j))
    return new_mesh(name, verts, faces, [mat], recalc=True)


def prism(name, poly_xy, z0, z1, mat, mat_top=None):
    """Closed extrusion of a world-XY polygon (walls + both caps)."""
    n = len(poly_xy)
    verts = [(x, y, z0) for x, y in poly_xy] + [(x, y, z1) for x, y in poly_xy]
    faces, face_mats = [], []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
        face_mats.append(0)
    faces.append(tuple(range(n - 1, -1, -1)))
    face_mats.append(0)
    faces.append(tuple(range(n, 2 * n)))
    face_mats.append(1 if mat_top else 0)
    mats = [mat, mat_top] if mat_top else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def box(name, a0, a1, p0, p1, z0, z1, mat, mat_top=None):
    return prism(name, poly([(a0, p0), (a1, p0), (a1, p1), (a0, p1)]), z0, z1,
                 mat, mat_top)


def slope_slab(name, a0, a1, p0, z0, p1, z1, thick, mat):
    """A sloped roof-plane slab: the top surface runs from (p0, z0) to (p1, z1)
    across the full a0..a1, with a vertical thickness `thick` below it. Built
    as one closed 8-vert solid so the signed-volume test applies."""
    corners = [(a0, p0, z0), (a1, p0, z0), (a1, p1, z1), (a0, p1, z1)]
    verts = []
    for a, p, z in corners:
        x, y = W(a, p)
        verts.append((x, y, z))
    for a, p, z in corners:
        x, y = W(a, p)
        verts.append((x, y, z - thick))
    faces = [(0, 1, 2, 3), (7, 6, 5, 4),
             (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return new_mesh(name, verts, faces, [mat])


def glow_quad(name, a0, a1, p0, p1, z0, z1, mat, out_dir):
    """One OPEN, single-layer, outward-facing quad; winding checked against the
    actual outward direction `(da, dp)` and flipped if it disagrees."""
    c = [W(a0, p0), W(a1, p1)]
    verts = [(c[0][0], c[0][1], z0), (c[1][0], c[1][1], z0),
             (c[1][0], c[1][1], z1), (c[0][0], c[0][1], z1)]
    ex = (verts[1][0] - verts[0][0], verts[1][1] - verts[0][1], 0.0)
    ey = (0.0, 0.0, z1 - z0)
    nrm = (ex[1] * ey[2] - ex[2] * ey[1],
           ex[2] * ey[0] - ex[0] * ey[2],
           ex[0] * ey[1] - ex[1] * ey[0])
    ox = out_dir[0] * U[0] + out_dir[1] * V[0]
    oy = out_dir[0] * U[1] + out_dir[1] * V[1]
    faces = [(0, 1, 2, 3)] if (nrm[0] * ox + nrm[1] * oy) > 0 else [(3, 2, 1, 0)]
    return new_mesh(name, verts, faces, [mat], recalc=False)


def cyl(name, a, p, z0, z1, r, segs, mat):
    ring = [(a + r * math.cos(2 * math.pi * i / segs),
             p + r * math.sin(2 * math.pi * i / segs)) for i in range(segs)]
    return prism(name, poly(ring), z0, z1, mat)


def sphere(name, a, p, z, r, mat, rings=4, segs=8):
    cx, cy = W(a, p)
    verts, faces = [(cx, cy, z + r)], []
    for i in range(1, rings):
        th = math.pi * i / rings
        for j in range(segs):
            ph = 2 * math.pi * j / segs
            verts.append((cx + r * math.sin(th) * math.cos(ph),
                          cy + r * math.sin(th) * math.sin(ph),
                          z + r * math.cos(th)))
    verts.append((cx, cy, z - r))
    bot = len(verts) - 1
    for j in range(segs):
        faces.append((0, 1 + (j + 1) % segs, 1 + j))
    for i in range(rings - 2):
        a0 = 1 + i * segs
        b0 = a0 + segs
        for j in range(segs):
            faces.append((a0 + j, a0 + (j + 1) % segs, b0 + (j + 1) % segs, b0 + j))
    a0 = 1 + (rings - 2) * segs
    for j in range(segs):
        faces.append((bot, a0 + j, a0 + (j + 1) % segs))
    return new_mesh(name, verts, faces, [mat])


def bevel(obj, width=BEVEL_W, segments=BEVEL_SEG):
    thin = min((d for d in obj.dimensions if d > 1e-6), default=width)
    offset = min(width, thin * 0.30)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(bm, geom=list(bm.verts) + list(bm.edges), offset=offset,
                    segments=segments, profile=0.5, affect="EDGES",
                    clamp_overlap=True)
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-4)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-4, edges=list(bm.edges))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def make_material(name):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = PALETTE[name] + (1.0,)
    bsdf.inputs["Roughness"].default_value = 0.85
    if "Metallic" in bsdf.inputs:
        bsdf.inputs["Metallic"].default_value = 0.0
    if name.endswith("_Glow") and "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = PALETTE[name] + (1.0,)
        bsdf.inputs["Emission Strength"].default_value = 1.0
    return mat


# ------------------------------------------------------------------- shapes


def shed_nw(a):
    """North wall of the shed at along `a` (the loft)."""
    if a <= A_HEAD_END:
        return P_HEAD_NW
    if a >= A_LOFT_END:
        return P_MAIN_NW
    t = (a - A_HEAD_END) / (A_LOFT_END - A_HEAD_END)
    return P_HEAD_NW + (P_MAIN_NW - P_HEAD_NW) * t


def shed_se(a):
    """South wall of the shed at along `a` (the head taper)."""
    if a >= A_TAPER_SE:
        return P_MAIN_SE
    t = (a - A_BULK_BACK) / (A_TAPER_SE - A_BULK_BACK)
    return P_HEAD_SE0 + (P_MAIN_SE - P_HEAD_SE0) * t


def shed_outline():
    return [(A_BULK_BACK, P_HEAD_NW), (A_HEAD_END, P_HEAD_NW),
            (A_LOFT_END, P_MAIN_NW), (A_SHED_END, P_MAIN_NW),
            (A_SHED_END, P_MAIN_SE), (A_TAPER_SE, P_MAIN_SE),
            (A_BULK_BACK, P_HEAD_SE0)]


def deck_outline():
    """Deck: constant NW edge; SE edge carries the bulkhead-wharf bump at the
    shore end and converges to the pier's own width."""
    return poly([(A_FRONT, P_DECK_NW), (A_DECK_END, P_DECK_NW),
                 (A_DECK_END, P_DECK_SE), (A_TAPER_SE, P_DECK_SE),
                 (A_BULK_BACK + 4.0, P_BULK_SE + 0.2),
                 (A_FRONT, P_BULK_SE + 0.2)])


def deck_perimeter():
    """The deck edge the railing follows - everything except the frontage."""
    return poly([(A_FRONT, P_DECK_NW), (A_DECK_END, P_DECK_NW),
                 (A_DECK_END, P_DECK_SE), (A_TAPER_SE, P_DECK_SE),
                 (A_BULK_BACK + 4.0, P_BULK_SE + 0.2),
                 (A_FRONT, P_BULK_SE + 0.2)])


def roof_z(p):
    """Top surface of the shallow-gable roof at perp `p` (main shed only)."""
    if p <= SHED_MC - MON_HALF:
        t = (p - P_MAIN_NW) / ((SHED_MC - MON_HALF) - P_MAIN_NW)
        return Z_EAVE - 0.05 + (Z_ROOF_HI - Z_EAVE + 0.05) * max(0.0, min(1.0, t))
    if p >= SHED_MC + MON_HALF:
        t = (P_MAIN_SE - p) / (P_MAIN_SE - (SHED_MC + MON_HALF))
        return Z_EAVE - 0.05 + (Z_ROOF_HI - Z_EAVE + 0.05) * max(0.0, min(1.0, t))
    return Z_ROOF_HI


def arch_profile(w, spring, segs=ARCH_SEGS):
    r = w / 2.0
    pts = [(PAV_P - r, 0.0), (PAV_P - r, spring)]
    for i in range(1, segs):
        ang = math.pi * i / segs
        pts.append((PAV_P - r * math.cos(ang), spring + r * math.sin(ang)))
    pts += [(PAV_P + r, spring), (PAV_P + r, 0.0)]
    return pts


def arch_face(name, w, spring, a_at, mat, z0=0.0):
    prof = arch_profile(w, spring)
    verts, faces = [], []
    for p, z in prof:
        x, y = W(a_at, p)
        verts.append((x, y, z0 + z))
    x, y = W(a_at, PAV_P)
    verts.append((x, y, z0))
    c = len(verts) - 1
    for i in range(len(prof) - 1):
        faces.append((c, i, i + 1))
    return new_mesh(name, verts, faces, [mat])


def window_pair(name, a0, a1, p_wall, p_recess, out, z0, z1, mats):
    """A recessed opening: dark glazing panel + one light transom, both poking
    0.02-0.05 m PROUD of the wall plane (coincident faces z-fight and fail the
    normals ray test; fully recessed boxes vanish inside the wall solid)."""
    p_out = p_wall + out * 0.02
    box(f"{name}_gl", a0, a1, min(p_out, p_recess), max(p_out, p_recess),
        z0, z1, mats["Toy_glass"])
    p_tr = p_wall + out * 0.05
    zt = z0 + (z1 - z0) * 0.45
    box(f"{name}_tr", a0, a1, min(p_tr, p_recess), max(p_tr, p_recess),
        zt, zt + 0.14, mats["Toy_glassl"])


# LETTERS: PIER 9, rectangles in the gable's (p, z) plane, extruded.
def letter_boxes(ch, w, h):
    s = w * 0.24
    if ch == "P":
        return [(0, 0, s, h), (0, h - s, w, s), (0, h / 2 - s / 2, w, s),
                (w - s, h / 2 - s / 2, s, h / 2 + s / 2)]
    if ch == "I":
        return [(w / 2 - s / 2, 0, s, h)]
    if ch == "E":
        return [(0, 0, s, h), (0, h - s, w, s), (0, h / 2 - s / 2, w * 0.8, s),
                (0, 0, w, s)]
    if ch == "R":
        return [(0, 0, s, h), (0, h - s, w, s), (0, h / 2 - s / 2, w, s),
                (w - s, h / 2 - s / 2, s, h / 2 + s / 2),
                (w * 0.55, 0, s, h / 2)]
    if ch == "9":
        return [(0, h / 2 - s / 2, s, h / 2 + s / 2),      # upper-left stroke
                (0, h - s, w, s),                          # top bar
                (0, h / 2 - s / 2, w, s),                  # mid bar
                (w - s, 0, s, h)]                          # right stroke, full
    return []


def lettering(name, text, p_c, z0, h, a_at, mat, gap=0.34):
    lw = h * 0.66
    widths = [lw for _ in text]
    total = sum(widths) + gap * (len(text) - 1)
    p = p_c - total / 2.0
    n = 0
    for ch, wdt in zip(text, widths):
        for dp, dz, bw, bh in letter_boxes(ch, wdt, h):
            box(f"{name}_{n}", a_at - 0.16, a_at + EMBED, p + dp, p + dp + bw,
                z0 + dz, z0 + dz + bh, mat)
            n += 1
        p += wdt + gap
    return n


# --------------------------------------------------------------------- build


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    mats = {k: make_material(k) for k in PALETTE}

    # 1. the pier: deck slab, fascia, pile stubs. The deck's walking surface is
    #    asphalt-grey (Toy_steel), the fascia and piles dark.
    deck = deck_outline()
    prism("deck", deck, Z_DECK_BOT, 0.0, mats["Toy_ink"], mats["Toy_steel"])

    per = deck_perimeter()
    n_pile = 0
    for i in range(len(per) - 1):
        seg = math.dist(per[i], per[i + 1])
        k = max(1, int(seg / 9.0))
        for j in range(k):
            t = (j + 0.5) / k
            x = per[i][0] + (per[i + 1][0] - per[i][0]) * t
            y = per[i][1] + (per[i + 1][1] - per[i][1]) * t
            cx0, cy0 = deck_centroid()
            cx, cy = (x - cx0) * 0.985 + cx0, (y - cy0) * 0.985 + cy0
            prism(f"pile_{n_pile}",
                  [(cx - 0.45, cy - 0.45), (cx + 0.45, cy - 0.45),
                   (cx + 0.45, cy + 0.45), (cx - 0.45, cy + 0.45)],
                  Z_PILE_BOT, Z_DECK_BOT + 0.05, mats["Toy_ink"])
            n_pile += 1
    # two internal rows under the outer end, where the DEM is open water
    for row_p in (-8.0, 12.0):
        for a in range(78, 125, 9):
            cx, cy = W(a, row_p)
            prism(f"pile_i{n_pile}",
                  [(cx - 0.45, cy - 0.45), (cx + 0.45, cy - 0.45),
                   (cx + 0.45, cy + 0.45), (cx - 0.45, cy + 0.45)],
                  Z_PILE_BOT, Z_DECK_BOT + 0.05, mats["Toy_ink"])
            n_pile += 1

    # rail-spur score lines in the aprons: thin dark strips, barely proud
    for tag, p_r in (("n1", -19.6), ("n2", -18.2), ("s1", 21.2), ("s2", 22.4)):
        box(f"railspur_{tag}", -110.0, 118.0, p_r - 0.14, p_r + 0.14,
            0.005, 0.035, mats["Toy_ink"])

    # 2. the bulkhead building: full-width slab, wings, cope, plinth.
    box("bulkhead", A_FRONT, A_BULK_BACK, P_BULK_NW, P_BULK_SE, 0.0, Z_WING,
        mats["Toy_cream"], mats["Toy_roofd"])
    pv0, pv1 = PAV_P - PAV_W / 2.0, PAV_P + PAV_W / 2.0
    for tag, p0, p1 in (("nw", P_BULK_NW, pv0), ("se", pv1, P_BULK_SE)):
        box(f"bulk_cope_{tag}", A_FRONT - 0.12, A_BULK_BACK, p0, p1,
            Z_WING - EMBED, Z_WING_COPE, mats["Toy_white"])
    box("bulk_plinth", A_FRONT - 0.10, A_BULK_BACK, P_BULK_NW, P_BULK_SE,
        0.0, Z_PLINTH + 0.4, mats["Toy_stone"])

    # 3. wing fenestration: big steel-sash windows in moulded surrounds, doors.
    #    North wing 3 windows + door, south wing 3 windows + door.
    wing_windows = [(-20.8, "n0"), (-16.6, "n1"), (-12.4, "n2"),
                    (13.6, "s0"), (17.8, "s1"), (22.0, "s2")]
    for pc, tag in wing_windows:
        box(f"wfr_{tag}", A_FRONT - 0.12, A_FRONT + EMBED,
            pc - 1.55, pc + 1.55, 1.15, 5.85, mats["Toy_white"])
        box(f"wwin_{tag}_gl", A_FRONT - 0.14, A_FRONT + RECESS,
            pc - 1.3, pc + 1.3, 1.5, 5.5, mats["Toy_glass"])
        box(f"wwin_{tag}_tr", A_FRONT - 0.17, A_FRONT + RECESS,
            pc - 1.3, pc + 1.3, 3.35, 3.55, mats["Toy_glassl"])
    for pc, tag in ((-9.9, "dn"), (24.4, "ds")):
        box(f"wdoor_{tag}", A_FRONT - 0.10, A_FRONT + RECESS,
            pc - 0.9, pc + 0.9, 0.0, 3.2, mats["Toy_steel"])
    # two lit wing windows at night
    for pc, tag in ((-16.6, "wn"), (17.8, "ws")):
        glow_quad(f"wwin_{tag}_glow", A_FRONT - 0.20, A_FRONT - 0.20,
                  pc - 1.2, pc + 1.2, 1.7, 5.3, mats["Toy_glass_Glow"], (-1, 0))

    # 4. the frontispiece. Everything above the wing parapet is a SCREEN 2.6 m
    #    deep, not a full-depth block (the pier-1 lesson).
    A_PAV = A_FRONT - PAV_PROUD
    A_SCREEN = A_PAV + 2.6
    box("pavilion", A_PAV, A_BULK_BACK, pv0, pv1, 0.0, Z_WING,
        mats["Toy_cream"], mats["Toy_roofd"])
    box("pav_screen", A_PAV, A_SCREEN, pv0, pv1, Z_WING - EMBED, Z_CORNICE,
        mats["Toy_cream"])
    # the monumental banded piers flanking the arch
    for tag, p_c in (("nw", pv0 + PIER_W / 2), ("se", pv1 - PIER_W / 2)):
        box(f"bpier_{tag}", A_PAV - 0.28, A_PAV + EMBED,
            p_c - PIER_W / 2, p_c + PIER_W / 2, 0.0, Z_CORNICE,
            mats["Toy_white"])
        for bi, zb in enumerate((1.6, 3.4, 5.2, 7.0)):
            box(f"bpier_{tag}_band_{bi}", A_PAV - 0.34, A_PAV - 0.20,
                p_c - PIER_W / 2 - 0.04, p_c + PIER_W / 2 + 0.04,
                zb, zb + 0.35, mats["Toy_cream"])
    # cornice band across the pavilion at the gable springing
    box("pav_cornice", A_PAV - 0.32, A_SCREEN, pv0 - 0.25, pv1 + 0.25,
        Z_CORNICE - 0.35, Z_CORNICE, mats["Toy_white"])

    # gable with a flattened apex, on the 2.6 m screen; small shoulder pylons
    ped = [(pv0 + 0.4, Z_CORNICE - EMBED), (PAV_P - 1.8, Z_APEX),
           (PAV_P + 1.8, Z_APEX), (pv1 - 0.4, Z_CORNICE - EMBED)]
    verts, faces = [], []
    for a_at in (A_PAV - 0.18, A_SCREEN):
        for p, z in ped:
            x, y = W(a_at, p)
            verts.append((x, y, z))
    n = len(ped)
    for i in range(n - 1):
        faces.append((i, i + 1, n + i + 1, n + i))
    faces.append((n - 1, 0, n, 2 * n - 1))
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    new_mesh("gable", verts, faces, [mats["Toy_cream"]])
    # raking cornice: one smooth sloped slab along each gable edge (stepped
    # boxes rendered as a crenellated staircase in the first aerial)
    for sgn, tag in ((-1, "nw"), (1, "se")):
        p_lo = pv0 + 0.4 if sgn < 0 else pv1 - 0.4
        p_hi = PAV_P - 1.8 if sgn < 0 else PAV_P + 1.8
        corners = [(p_lo, Z_CORNICE - 0.15), (p_hi, Z_APEX - 0.15),
                   (p_hi, Z_APEX + 0.22), (p_lo, Z_CORNICE + 0.22)]
        verts = []
        for a_at in (A_PAV - 0.30, A_PAV - 0.02):
            for p, z in corners:
                x, y = W(a_at, p)
                verts.append((x, y, z))
        faces = [(0, 1, 2, 3), (7, 6, 5, 4),
                 (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
        new_mesh(f"rake_{tag}", verts, faces, [mats["Toy_white"]])
    for tag, p_c in (("nw", pv0 + 0.9), ("se", pv1 - 0.9)):
        box(f"pylon_{tag}", A_PAV - 0.30, A_SCREEN, p_c - 0.85, p_c + 0.85,
            Z_WING - EMBED, 11.2, mats["Toy_white"])
    # attic block at the apex - THE bbox top at +15.0
    box("attic", A_PAV - 0.22, A_SCREEN, PAV_P - 1.6, PAV_P + 1.6,
        Z_APEX - EMBED, Z_CREST - 0.18, mats["Toy_cream"])
    box("attic_cope", A_PAV - 0.30, A_SCREEN, PAV_P - 1.75, PAV_P + 1.75,
        Z_CREST - 0.18, Z_CREST, mats["Toy_white"])

    # PIER 9 on the gable face, extruded. Dark metal letters on stucco.
    lettering("pier9", "PIER9", PAV_P, 10.55, 1.15, A_PAV - 0.18,
              mats["Toy_ink"], gap=0.40)

    # the great arch: dark screen + proud archivolt ring + keystone
    arch_face("arch_glass", ARCH_W, ARCH_SPRING, A_PAV - 0.06, mats["Toy_glass"])
    prof = arch_profile(ARCH_W, ARCH_SPRING)
    prof_o = arch_profile(ARCH_W + 2 * VOUSSOIR, ARCH_SPRING - VOUSSOIR * 0.5)
    verts, faces = [], []
    a0, a1 = A_PAV - 0.30, A_PAV + 0.10
    for a_at in (a0, a1):
        for p, z in prof:
            x, y = W(a_at, p)
            verts.append((x, y, z))
        for p, z in prof_o:
            x, y = W(a_at, p)
            verts.append((x, y, z))
    m = len(prof)
    k = 2 * m
    for i in range(m - 1):
        faces.append((i, i + 1, m + i + 1, m + i))
        faces.append((k + i, k + m + i, k + m + i + 1, k + i + 1))
        faces.append((i, k + i, k + i + 1, i + 1))
        faces.append((m + i, m + i + 1, k + m + i + 1, k + m + i))
    faces.append((0, m, k + m, k))
    faces.append((m - 1, k + m - 1, k + 2 * m - 1, 2 * m - 1))
    new_mesh("archivolt", verts, faces, [mats["Toy_white"]])
    box("keystone", A_PAV - 0.40, A_PAV + 0.10, PAV_P - 0.55, PAV_P + 0.55,
        ARCH_SPRING + ARCH_W / 2 - 0.15, ARCH_SPRING + ARCH_W / 2 + 1.05,
        mats["Toy_white"])
    # steel screen: doors, roll-up band, mullion cross
    box("arch_doors", A_PAV - 0.16, A_PAV - 0.02, PAV_P - 3.4, PAV_P + 3.4,
        0.0, 3.2, mats["Toy_steel"])
    box("arch_shutter", A_PAV - 0.14, A_PAV - 0.02, PAV_P - 4.0, PAV_P + 4.0,
        3.2, 5.1, mats["Toy_steel"])
    box("arch_mull_v", A_PAV - 0.13, A_PAV - 0.05, PAV_P - 0.10, PAV_P + 0.10,
        5.1, ARCH_SPRING + ARCH_W / 2 - 0.4, mats["Toy_glassl"])
    box("arch_mull_h", A_PAV - 0.13, A_PAV - 0.05, PAV_P - 4.0,
        PAV_P + 4.0, 6.7, 6.9, mats["Toy_glassl"])
    glow_quad("arch_glow", A_PAV - 0.20, A_PAV - 0.20,
              PAV_P - ARCH_W / 2 + 0.35, PAV_P + ARCH_W / 2 - 0.35,
              0.3, ARCH_SPRING + ARCH_W / 2 - 0.5, mats["Toy_glassl_Glow"],
              (-1, 0))

    # 5. the shed: one lofted solid (head, loft, main run), grey precast walls.
    sh = shed_outline()
    prism("shed", poly(sh), 0.0, Z_EAVE, mats["Toy_stone"], mats["Toy_roofd"])
    prism("shed_plinth", offset_polygon(poly(sh), 0.10), 0.0, Z_PLINTH,
          mats["Toy_stone"])

    # shed bays, both flanks: pilaster, high window band, belt, doors.
    door_count = 0
    nbays = int((A_SHED_END - A_BULK_BACK) / SHED_BAY)
    for b in range(nbays):
        a_c = A_BULK_BACK + SHED_BAY * (b + 0.5)
        a0, a1 = a_c - SHED_BAY / 2, a_c + SHED_BAY / 2
        for side in (0, 1):
            p_w = shed_nw(a_c) if side == 0 else shed_se(a_c)
            out = -1 if side == 0 else 1
            pi = p_w + out * SHED_PIL_PROUD
            box(f"spil_{b}_{side}", a0 - SHED_PIL_W / 2, a0 + SHED_PIL_W / 2,
                min(p_w, pi), max(p_w, pi), Z_PLINTH - EMBED, Z_EAVE - 0.15,
                mats["Toy_stone"])
            pr = p_w - out * RECESS
            window_pair(f"swin_{b}_{side}", a0 + 1.4, a1 - 1.4, p_w, pr, out,
                        SHED_WIN_Z[0], SHED_WIN_Z[1], mats)
            if side == 1 and b in LIT_BAYS:
                glow_quad(f"swin_{b}_glow", a0 + 1.4, a1 - 1.4,
                          p_w + out * 0.07, p_w + out * 0.07,
                          SHED_WIN_Z[0], SHED_WIN_Z[1],
                          mats["Toy_glass_Glow"], (0, out))
            box(f"sbelt_{b}_{side}", a0, a1,
                min(p_w, p_w + out * 0.10), max(p_w, p_w + out * 0.10),
                Z_BELT, Z_BELT + 0.20, mats["Toy_stone"])
            # roll-up doors every 4th bay (skip the head taper bays)
            if b % 4 == 1 and a_c > A_LOFT_END:
                box(f"sdoor_{door_count}", a_c - 2.2, a_c + 2.2,
                    min(p_w + out * 0.02, pr + out * 0.04),
                    max(p_w + out * 0.02, pr + out * 0.04),
                    DOOR_Z[0], DOOR_Z[1], mats["Toy_steel"])
                door_count += 1
    # the two 1970 enlarged doors on the south flank
    for i, a_c in enumerate(BIG_DOORS_A):
        p_w = shed_se(a_c)
        box(f"sbigdoor_{i}", a_c - 3.2, a_c + 3.2, p_w + 0.03, p_w + 0.16,
            0.2, 4.15, mats["Toy_steel"])

    # 6. the roof: head flat roof, two dark sloped planes, the monitor.
    head_roof = [(A_BULK_BACK + 0.15, P_HEAD_NW + 0.2),
                 (A_HEAD_END, P_HEAD_NW + 0.2),
                 (A_LOFT_END, P_MAIN_NW + 0.2),
                 (A_LOFT_END, P_MAIN_SE - 0.2),
                 (A_TAPER_SE, P_MAIN_SE - 0.2),
                 (A_BULK_BACK + 0.15, P_HEAD_SE0 - 0.2)]
    prism("roof_head", poly(head_roof), Z_EAVE - 0.12, Z_EAVE + 0.02,
          mats["Toy_roofd"])
    slope_slab("roof_n", -95.0, A_SHED_END, P_MAIN_NW + 0.1,
               Z_EAVE - 0.05, SHED_MC - MON_HALF + 0.3, Z_ROOF_HI, 0.15,
               mats["Toy_roofd"])
    slope_slab("roof_s", -95.0, A_SHED_END, SHED_MC + MON_HALF - 0.3,
               Z_ROOF_HI, P_MAIN_SE - 0.1, Z_EAVE - 0.05, 0.15,
               mats["Toy_roofd"])
    # the monitor: steel body, glazing band both sides, dark cap
    box("monitor", MON_A0, MON_A1, SHED_MC - MON_HALF, SHED_MC + MON_HALF,
        Z_ROOF_HI - 0.35, Z_MON_TOP - 0.12, mats["Toy_steel"])
    for sgn, tag in ((-1, "nw"), (1, "se")):
        p_gl = SHED_MC + sgn * MON_HALF
        box(f"mon_glass_{tag}", MON_A0 + 2.0, MON_A1 - 2.0,
            min(p_gl, p_gl + sgn * 0.06), max(p_gl, p_gl + sgn * 0.06),
            Z_MON_GL0, Z_MON_GL1, mats["Toy_glassl"])
        for gi, (ga0, ga1) in enumerate(MON_LIT):
            glow_quad(f"mon_glow_{tag}_{gi}", ga0, ga1,
                      p_gl + sgn * 0.10, p_gl + sgn * 0.10,
                      Z_MON_GL0 + 0.1, Z_MON_GL1 - 0.1,
                      mats["Toy_glass_Glow"], (0, sgn))
    box("mon_cap", MON_A0 - 0.15, MON_A1 + 0.15, SHED_MC - MON_HALF - 0.15,
        SHED_MC + MON_HALF + 0.15, Z_MON_TOP - 0.12, Z_MON_TOP,
        mats["Toy_roofd"])

    # roof plant: a pale grey crowd on the south plane, a few on the north
    south_plant = ((-45, 13.0, 2.6, 1.3), (-37, 15.5, 1.8, 1.0),
                   (-24, 11.5, 2.2, 1.2), (-10, 14.0, 3.0, 1.4),
                   (3, 16.5, 1.6, 0.9), (16, 12.0, 2.4, 1.1),
                   (31, 15.0, 2.0, 1.3), (46, 11.0, 2.8, 1.0),
                   (61, 13.5, 1.8, 1.2), (74, 15.5, 2.2, 0.9))
    north_plant = ((-55, -9.0, 2.4, 1.1), (20, -8.0, 2.0, 1.0),
                   (90, -10.0, 2.6, 1.2))
    for i, (a, p, w_, h_) in enumerate(south_plant + north_plant):
        z0 = roof_z(p) - 0.10
        box(f"plant_{i}", a - w_ / 2, a + w_ / 2, p - w_ / 3, p + w_ / 3,
            z0, z0 + h_, mats["Toy_steel"])
    for i, (a, p) in enumerate(((-60, 10.0), (-15, -6.5), (38, 13.5),
                                (68, -7.5), (100, 12.0))):
        z0 = roof_z(p) - 0.10
        cyl(f"roof_vent_{i}", a, p, z0, z0 + 0.8, 0.5, 8, mats["Toy_steel"])

    # 7. the bay end: six profiled pilasters, gabled centre, doors, Bar Pilots.
    for k in range(6):
        p_c = P_MAIN_NW + (P_MAIN_SE - P_MAIN_NW) * (k + 0.5) / 6.0
        box(f"endpil_{k}", A_SHED_END - EMBED, A_SHED_END + 0.35,
            p_c - 0.45, p_c + 0.45, 0.0, Z_EAVE + 0.5, mats["Toy_stone"])
    # gabled centre pavilion of the end elevation: a closed pentagonal prism.
    # Verts per slice: 0,1,2 = gable top edge (left shoulder, apex, right
    # shoulder), 3,4 = base corners sunk below the eave.
    egp = [(SHED_MC - 4.0, Z_EAVE + 0.4 - EMBED), (SHED_MC, Z_EAVE + 1.7),
           (SHED_MC + 4.0, Z_EAVE + 0.4 - EMBED)]
    verts = []
    for a_at in (A_SHED_END - EMBED, A_SHED_END + 0.30):
        for p, z in egp:
            x, y = W(a_at, p)
            verts.append((x, y, z))
        x, y = W(a_at, SHED_MC - 4.0)
        verts.append((x, y, Z_EAVE - 0.8))
        x, y = W(a_at, SHED_MC + 4.0)
        verts.append((x, y, Z_EAVE - 0.8))
    faces = [(3, 0, 1, 2, 4), (9, 7, 6, 5, 8),
             (0, 5, 6, 1), (1, 6, 7, 2), (3, 8, 5, 0), (2, 7, 9, 4),
             (4, 9, 8, 3)]
    new_mesh("end_gable", verts, faces, [mats["Toy_stone"]])
    cyl("end_pole", A_SHED_END + 0.1, SHED_MC, Z_EAVE + 1.5, 11.0, 0.09, 6,
        mats["Toy_ink"])
    for i, p_c in enumerate((-8.0, 8.0)):
        box(f"end_door_{i}", A_SHED_END - RECESS, A_SHED_END + 0.02,
            p_c - 2.8, p_c + 2.8, 0.2, 4.0, mats["Toy_steel"])

    # Bar Pilots: annex on the north side, lookout over the roof, two masts.
    box("bp_annex", 118.5, A_DECK_END - 0.5, P_MAIN_NW - 5.0, P_MAIN_NW + 0.2,
        0.0, 6.5, mats["Toy_stone"], mats["Toy_roofd"])
    box("bp_lookout", 119.5, 124.5, -13.5, -8.5, Z_EAVE - 0.4, 11.1,
        mats["Toy_white"])
    box("bp_lookout_band", 119.4, 124.6, -13.6, -8.4, 10.0, 10.9,
        mats["Toy_glassl"])
    box("bp_lookout_cap", 119.3, 124.7, -13.7, -8.3, 11.1, 11.35,
        mats["Toy_roofd"])
    glow_quad("bp_glow_ne", 124.62, 124.62, -13.4, -8.6, 10.1, 10.8,
              mats["Toy_glass_Glow"], (1, 0))
    glow_quad("bp_glow_nw", 119.5, 124.5, -13.62, -13.62, 10.1, 10.8,
              mats["Toy_glass_Glow"], (0, -1))
    for i, (a, p, h) in enumerate(((125.4, -17.5, 13.8), (124.2, -15.9, 12.6))):
        cyl(f"bp_mast_{i}", a, p, 0.0, h, 0.09, 6, mats["Toy_ink"])

    # 8. containers on the north apron: a broken run, 2-3 colours.
    containers = ((-58, "Toy_rust"), (-50, "Toy_navy"), (-18, "Toy_steel"),
                  (8, "Toy_navy"), (16, "Toy_rust"), (48, "Toy_steel"))
    for i, (a, mkey) in enumerate(containers):
        box(f"container_{i}", a - 3.05, a + 3.05, -21.2, -18.8, 0.0, 2.6,
            mats[mkey])

    # 9. apron furniture: railing ring, bollards, mooring bitts, lamps.
    per = deck_perimeter()
    npost = 0
    for i in range(len(per) - 1):
        ax, ay = per[i]
        bx, by = per[i + 1]
        seg = math.hypot(bx - ax, by - ay)
        k = max(1, int(seg / RAIL_PITCH))
        nx, ny = (bx - ax) / seg, (by - ay) / seg
        ix, iy = -ny * 0.55, nx * 0.55
        s = _side_sign(per)
        ix, iy = ix * s, iy * s
        verts = [(ax + ix - ny * 0.05, ay + iy + nx * 0.05),
                 (bx + ix - ny * 0.05, by + iy + nx * 0.05),
                 (bx + ix + ny * 0.05, by + iy - nx * 0.05),
                 (ax + ix + ny * 0.05, ay + iy - nx * 0.05)]
        prism(f"rail_{i}", verts, RAIL_Z - 0.09, RAIL_Z, mats["Toy_steel"])
        for j in range(k):
            t = (j + 0.5) / k
            px, py = ax + (bx - ax) * t + ix, ay + (by - ay) * t + iy
            prism(f"railpost_{npost}",
                  [(px - 0.05, py - 0.05), (px + 0.05, py - 0.05),
                   (px + 0.05, py + 0.05), (px - 0.05, py + 0.05)],
                  0.0, RAIL_Z, mats["Toy_steel"])
            npost += 1
    nbol = 0
    for a in range(-110, 122, int(BOLLARD_PITCH)):
        for p in (P_DECK_NW + 0.9, P_DECK_SE - 0.9):
            cyl(f"bollard_{nbol}", a, p, 0.0, 0.72, 0.26, 6, mats["Toy_ink"])
            nbol += 1
    for i, p in enumerate((-18.0, -6.0, 6.0, 18.0)):
        cyl(f"bitt_{i}", 125.6, p, 0.0, 0.9, 0.32, 6, mats["Toy_ink"])
    nlamp = 0
    for a in range(-100, 122, int(LAMP_PITCH)):
        p = P_DECK_SE - 1.3
        cyl(f"lamp_{nlamp}", a, p, 0.0, LAMP_H, 0.12, 6, mats["Toy_ink"])
        sphere(f"lampglobe_{nlamp}", a, p, LAMP_H + 0.38, 0.38,
               mats["Toy_amber_Glow"])
        nlamp += 1
    for p in (-16.0, 10.0):
        cyl(f"lamp_{nlamp}", 124.8, p, 0.0, LAMP_H, 0.12, 6, mats["Toy_ink"])
        sphere(f"lampglobe_{nlamp}", 124.8, p, LAMP_H + 0.38, 0.38,
               mats["Toy_amber_Glow"])
        nlamp += 1

    # 10. bevels: chunky masses only.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        n = obj.name
        if n.startswith(("rail", "pile", "pier9_", "bollard", "bitt", "lamp",
                         "swin", "wwin", "wfr", "wdoor", "sdoor", "sbigdoor",
                         "sbelt", "spil", "endpil", "end_", "arch_",
                         "archivolt", "keystone", "mon_glass", "plant_",
                         "roof_vent", "railspur", "bpier", "rake_", "pylon",
                         "bp_mast", "bp_lookout_band", "bp_glow")):
            continue
        if "_glow" in n or "glow_" in n:
            continue
        bevel(obj)

    recentre()
    return scene


_DECK_C = [None]


def deck_centroid():
    if _DECK_C[0] is None:
        d = deck_outline()
        _DECK_C[0] = (sum(p[0] for p in d) / len(d), sum(p[1] for p in d) / len(d))
    return _DECK_C[0]


def _side_sign(per):
    cx, cy = deck_centroid()
    ax, ay = per[0]
    bx, by = per[1]
    seg = math.hypot(bx - ax, by - ay)
    nx, ny = (bx - ax) / seg, (by - ay) / seg
    if (ax - ny - cx) ** 2 + (ay + nx - cy) ** 2 < (ax - cx) ** 2 + (ay - cy) ** 2:
        return 1.0
    return -1.0


ANCHOR_SHIFT = [0.0, 0.0]


def recentre():
    mn = Vector((1e9, 1e9))
    mx = Vector((-1e9, -1e9))
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    for o in meshes:
        for v in o.data.vertices:
            for i in range(2):
                mn[i] = min(mn[i], v.co[i])
                mx[i] = max(mx[i], v.co[i])
    cx, cy = (mn[0] + mx[0]) / 2.0, (mn[1] + mx[1]) / 2.0
    ANCHOR_SHIFT[0], ANCHOR_SHIFT[1] = cx, cy
    for o in meshes:
        for v in o.data.vertices:
            v.co.x -= cx
            v.co.y -= cy


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
        o.evaluated_get(dg).to_mesh_clear()
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] vertical extent (targetHeightM) = {mx[2] - mn[2]:.3f}")
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    lon = DESIGN_ANCHOR[0] + ANCHOR_SHIFT[0] / LON_M
    lat = DESIGN_ANCHOR[1] + ANCHOR_SHIFT[1] / LAT_M
    print(f"[build] design anchor (along 0, perp 0): {DESIGN_ANCHOR}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] axis bearing {AXIS_BEARING:.2f} deg; facade faces "
          f"{(AXIS_BEARING + 180.0) % 360.0:.2f} deg")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "pier-9.blend")
    glb = os.path.join(out, "pier-9.glb")
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
