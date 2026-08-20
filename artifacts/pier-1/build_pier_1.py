"""Deterministic Blender build of the SF-SIM miniature Pier 1.

    blender -b --python build_pier_1.py -- [--out DIR]

Writes pier-1.blend and pier-1.glb next to this file (or into --out). Geometry is
authored in world space in metres, Z up, +X east, +Y north, so the model drops
into the city at its real-world heading - the loader applies no rotation.

ORIGIN: this asset breaks the usual "min Z = 0" rule on purpose. Local Z = 0 is
the TOP OF THE PIER DECK; the deck fascia and pile stubs run down to -2.6 m.
placeGeneric() seats the GLB's origin on one terrain sample at the anchor, and
the app's DEM already carries this pier as a ~2.4 m ridge, so a model that sat on
z = 0 would float 2.6 m above the deck it is standing on. See the plan's 2.3.
`targetHeightM` is therefore the model's total VERTICAL EXTENT (-2.6 .. +12.8),
not a height above water.

Design (see REFERENCE.md for the sources behind every number):

* a 1918/1931 finger pier: a shallow Neo-classical BULKHEAD BUILDING on the
  Embarcadero building line, and a 213 m transit SHED running north-east into the
  Bay behind it, all on a concrete deck on piles;
* the recognition rests on three things: the arched FRONTISPIECE (one round arch
  with PIER . 1 over it), the LENGTH AND TAPER of the shed (41 m wide at the head,
  36 m in the body, 26.5 m for the outer 100 m), and the flat white roof striped
  with two dark SOLAR ARRAYS either side of a raised monitor spine;
* the pier's long axis bears 053.77 deg and the Embarcadero facade faces
  233.77 deg, so the axis-aligned XY bbox is ~185 x 190 m even though the pier is
  234 x 52 m. That is expected, not a scale error;
* Pier 1 is a two-colour building: warm off-white painted stucco and concrete,
  slate blue-grey steel. There is no third colour and adding one would make it a
  different building;
* night state: the great arch is the hero, the Embarcadero shopfront band
  supports it, and roughly half the shed's clerestory bays are lit in a scattered
  pattern - an office building at night is not uniformly on, and a fully-lit 213 m
  clerestory would out-shout the arch. Glow surfaces are single open faces
  standing proud of the opaque glazing, never closed shells: the app draws _Glow
  in a separate translucent layer and a closed shell is two layers deep.
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

# The design frame's origin: (along 0, perp 0) of the plan's pier frame - the
# shed's north-west corner on the bulkhead's inner line.
DESIGN_ANCHOR = (-122.3950194, 37.7970976)

AXIS_BEARING = 53.77          # measured from the OSM ring's north-west edge

# --- plan geometry, in (along a, perp p) metres. See plan 2.3.
A_FRONT = -24.2               # Embarcadero building line
A_BULK_BACK = -11.5           # back of the bulkhead slab / start of the shed
A_HEAD_END = 19.0             # shed head -> shed body
A_TAPER0 = 97.0               # start of the taper
A_TAPER1 = 149.0              # end of the taper
A_SHED_END = 202.0            # north-east end wall
A_DECK_END = 209.0            # north-east edge of the deck

P_BULK_NW = -14.2             # bulkhead north-west face
P_BULK_SE = 50.6              # bulkhead south-east face
P_HEAD_SE = 41.0              # shed head south-east wall
P_BODY_SE = 36.2              # shed body south-east wall
P_OUTER_SE = 26.5             # outer run south-east wall

# --- deck, one apron ring round the whole pier
P_DECK_NW = -11.0
DECK_NW = [(A_BULK_BACK, P_BULK_NW), (A_HEAD_END, P_DECK_NW),
           (A_SHED_END, P_DECK_NW), (A_DECK_END, P_DECK_NW + 6.0)]
# The south-east edge runs as one converging line rather than stepping out to
# meet the bulkhead's own 50.6 m face: the first build closed it on the bulkhead
# and the aerial showed a wart of deck sticking out beside the frontispiece.
DECK_SE = [(A_DECK_END, P_OUTER_SE + 5.0), (A_SHED_END, P_OUTER_SE + 7.0),
           (A_TAPER1, P_OUTER_SE + 7.0), (A_TAPER0, P_BODY_SE + 7.0),
           (A_HEAD_END, P_HEAD_SE + 6.0), (A_BULK_BACK, P_BULK_SE + 2.6)]

# --- heights above the deck
Z_DECK_BOT = -1.2             # underside of the deck slab / top of the piles
Z_PILE_BOT = -2.6             # bottom of the pile stubs = the model's min Z
Z_PLINTH = 0.8
Z_BELT = 2.2
Z_WING = 8.4                  # bulkhead wing parapet
Z_WING_COPE = 8.75
Z_SHED = 9.7                  # shed parapet (DataSF LiDAR median 9.66 m)
Z_SHED_COPE = 10.0
Z_MONITOR = 12.0              # roof monitor spine crest (9.7 + 2.3 rise)
Z_CORNICE0, Z_CORNICE1 = 9.6, 10.3   # pavilion entablature
Z_CREST = 12.8                # pavilion apex - the bbox top

# --- the frontispiece
PAV_P = 19.0                  # centred on the shed's head axis
PAV_W = 24.0
PAV_PROUD = 0.9
QUOIN_W = 1.7
ARCH_W = 10.4                 # real ~9.6 m, enlarged per style bible s.8/s.9
ARCH_SPRING = 4.4
ARCH_SEGS = 10
ARCH_RECESS = 0.55
VOUSSOIR = 0.55               # depth of the proud archivolt ring

PORTAL_P0, PORTAL_P1 = -1.2, 3.6      # the Belt Railroad pass-through
PORTAL_Z = 4.6

# --- wing and shed rhythms
WING_PIL_W, WING_PIL_PROUD = 0.9, 0.14
WING_WIN_Z = (5.2, 7.6)
WING_GF_Z = (1.0, 4.1)
SHED_BAY = 7.5
SHED_PIL_W, SHED_PIL_PROUD = 0.75, 0.09
SHED_WIN_Z = (2.6, 6.0)
SHED_CLERE_Z = (8.2, 9.2)
RECESS = 0.14

# --- roof
# Roof, re-measured off the georeferenced ortho at 0.08 m/px (three stations,
# along 38-46, 64-72 and 120-128). The cross-section is: 12.7 m of flat white
# roof, a 0.6 m hard shadow line, then a RAISED SPINE 9.5 m wide whose top
# carries a 1.9 m walkway strip and a 7.0 m solar array, then 12 m of flat white
# roof again. The shadow gives the spine's height as ~2.3 m at the capture's
# ~76 deg solar elevation, which is also what closes the 3.1 m gap between
# DataSF's LiDAR median (9.66 m) and its max (12.73 m). The first build had this
# inverted - a 9 m spine with two 8.4 m solar fields on the LOW roof either side -
# and the aerial read as a hangar ridge instead of a striped flat roof.
MON_HALF = 4.75
MON_RISE = 2.3
MON_A0, MON_A1 = -6.0, 198.0
SOLAR_HALF = 3.5           # on top of the spine
SOLAR_T = 0.14
OUTER_SOLAR_A0 = 145.0     # past here the arrays spill onto the flat roof too

RAIL_Z = 1.1
RAIL_PITCH = 4.5
BOLLARD_PITCH = 13.0
LAMP_H = 4.0

BEVEL_W, BEVEL_SEG = 0.10, 2
EMBED = 0.03                  # applied bands are sunk into the face they sit on,
                              # so no two solids share a coincident plane

# Which shed bays are lit at night, by index modulo. Scattered on purpose.
LIT_PATTERN = (0, 1, 3, 4, 8, 9, 11, 14, 15, 17, 20, 21, 24, 25)

PALETTE_HEX = {
    "Toy_cream": "f2ede3",     # bulkhead and shed walls, pilasters, coping
    "Toy_white": "f7f4ec",     # pavilion face, voussoirs, cornice, lettering
    "Toy_stone": "d9d2c2",     # plinth, belt course, deck slab, apron, roof
    "Toy_ink": "3a3530",       # deck fascia, pile stubs, portal reveal
    "Toy_navy": "2c4a70",      # window frames, doors, railing, solar arrays
    "Toy_glass": "2a4d73",     # all glazing - graphical, opaque, recessed
    "Toy_steel": "9aa0a6",     # roof vents and hatches
    "Toy_glassl": "6f95b8",    # the monitor's glazing band
    # Night. A _Glow material's BASE colour is what the app draws at night (the
    # glow layer is unlit), so these are authored as the colour to be SEEN, not
    # as a dark colour that a Blender emission boost would flatter.
    "Toy_glassl_Glow": "f4dcb0",   # the arch lunette and the shopfront band
    "Toy_glass_Glow": "cbd8e0",    # the lit shed clerestory bays, cooler
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
    """Offset a simple polygon by `d` (positive = outward for a CCW ring), by
    intersecting the offset lines of consecutive edges. Used for plinths and
    parapet rims, which have to stand proud of a face rather than sit exactly on
    it - coincident faces make a ray's first hit ambiguous and the contract's
    normals test counts the ambiguity as a flipped face."""
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
    """A closed ring band: the parapet coping, which must NOT be a slab over the
    whole roof - the first build made it one and buried the roof deck."""
    outer = poly_xy
    inner = offset_polygon(poly_xy, -thickness)
    n = len(outer)
    verts = ([(x, y, z0) for x, y in outer] + [(x, y, z1) for x, y in outer] +
             [(x, y, z0) for x, y in inner] + [(x, y, z1) for x, y in inner])
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))                              # outside
        faces.append((2 * n + j, 2 * n + i, 3 * n + i, 3 * n + j))      # inside
        faces.append((n + i, n + j, 3 * n + j, 3 * n + i))              # top
        faces.append((j, i, 2 * n + i, 2 * n + j))                      # bottom
    # recalc=True: the band is a closed manifold shell, so bmesh can settle the
    # winding. Hand-wound, it came out inside-out on the concave taper corner and
    # failed the validator's signed-volume test.
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


def glow_quad(name, a0, a1, p0, p1, z0, z1, mat, out_dir):
    """One OPEN, single-layer, outward-facing quad. Night glow is never a closed
    shell: the app draws _Glow in a separate translucent layer, so a box shows
    its front AND back face and reads at roughly twice the intended day alpha.

    `out_dir` is the actual outward direction in the pier frame as `(da, dp)` —
    e.g. `(-1, 0)` for the Embarcadero facade, `(0, -1)` for the shed's
    north-west flank. The winding is then CHECKED against it and flipped if it
    disagrees, rather than being derived by hand from a sign flag: the flag
    version got the facade quads backwards and the mistake was invisible in the
    renders, because nothing here culls back faces."""
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
    # Winding is set explicitly, never recalculated: an open strip has no inside
    # for recalc_face_normals to reason about.
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
    """Miniature-style edge softening (style bible s.4). The offset is capped at
    a third of the object's thinnest dimension: thin bands collapse into
    zero-area slivers under a full bevel even with clamp_overlap."""
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


def shed_se(a):
    """South-east wall of the shed at along `a` - this is the taper."""
    if a <= A_HEAD_END:
        return P_HEAD_SE
    if a <= A_TAPER0:
        return P_BODY_SE
    if a >= A_TAPER1:
        return P_OUTER_SE
    t = (a - A_TAPER0) / (A_TAPER1 - A_TAPER0)
    return P_BODY_SE + (P_OUTER_SE - P_BODY_SE) * t


def shed_centre(a):
    return shed_se(a) / 2.0


def deck_outline():
    return poly([(A_FRONT, P_BULK_NW)] + DECK_NW + DECK_SE +
                [(A_FRONT, P_BULK_SE + 2.6)])


def deck_perimeter():
    """The deck edge the railing follows: everything except the Embarcadero
    frontage, which is a building line, not a quay edge."""
    return poly(DECK_NW + DECK_SE)


def arch_profile(w, spring, segs=ARCH_SEGS):
    """(p, z) points of a round-headed opening of width `w` centred on PAV_P,
    from the springing line up over the crown and back down."""
    r = w / 2.0
    pts = [(PAV_P - r, 0.0), (PAV_P - r, spring)]
    for i in range(1, segs):
        ang = math.pi * i / segs
        pts.append((PAV_P - r * math.cos(ang), spring + r * math.sin(ang)))
    pts += [(PAV_P + r, spring), (PAV_P + r, 0.0)]
    return pts


def arch_face(name, w, spring, a_at, mat, z0=0.0):
    """A flat vertical slab filling a round-headed opening, in the plane a=a_at."""
    prof = arch_profile(w, spring)
    verts, faces = [], []
    for p, z in prof:
        x, y = W(a_at, p)
        verts.append((x, y, z0 + z))
    # fan-triangulate the (closed) profile through its base midpoint
    x, y = W(a_at, PAV_P)
    verts.append((x, y, z0))
    c = len(verts) - 1
    for i in range(len(prof) - 1):
        faces.append((c, i, i + 1))
    return new_mesh(name, verts, faces, [mat])


def window_pair(name, a0, a1, p_wall, p_recess, out, z0, z1, mats):
    """A recessed opening: one dark graphical glazing panel with a single light
    steel transom across it (style bible s.5 - windows are graphical elements
    before they are literal openings).

    Both boxes poke 0.02-0.05 m PROUD of the wall plane rather than stopping on
    it. A box whose outer face is coplanar with the wall z-fights, and the
    contract's normals ray test counts a coincident first hit as a flipped face.
    The wall is a solid, so a purely recessed box would also be invisible."""
    # `out` is the OUTWARD direction, so proud is p_wall + out * d and the recess
    # is p_wall - out * RECESS. Getting that sign backwards put every shed window
    # inside the wall solid: the flanks rendered blank except on the bays whose
    # night-glow quads (which had the sign right) showed through.
    p_out = p_wall + out * 0.02
    box(f"{name}_gl", a0, a1, min(p_out, p_recess), max(p_out, p_recess),
        z0, z1, mats["Toy_glass"])
    p_tr = p_wall + out * 0.05
    zt = z0 + (z1 - z0) * 0.42
    box(f"{name}_tr", a0, a1, min(p_tr, p_recess), max(p_tr, p_recess),
        zt, zt + 0.16, mats["Toy_glassl"])


# LETTERS: PIER . 1, built from rectangles in the pavilion's (p, z) plane.
# Extruded, not painted - it is recognition cue #1 and has to survive the aerial
# camera (style bible s.8).
def letter_boxes(ch, w, h):
    """Unit-placed boxes for one character, in (dp, dz) from its lower left."""
    s = w * 0.22                      # stroke
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
    if ch == "1":
        return [(w / 2 - s / 2, 0, s, h), (w / 2 - s * 1.3, h - s * 1.6, s * 1.1, s)]
    if ch == ".":
        return [(w / 2 - s / 2, 0, s, s)]
    return []


def lettering(name, text, p_c, z0, h, a_at, mat, gap=0.30):
    lw = h * 0.62
    widths = [lw * (0.35 if c == "." else 1.0) for c in text]
    total = sum(widths) + gap * (len(text) - 1)
    p = p_c - total / 2.0
    n = 0
    for ch, wdt in zip(text, widths):
        for dp, dz, bw, bh in letter_boxes(ch, wdt, h):
            box(f"{name}_{n}", a_at - 0.22, a_at + EMBED, p + dp, p + dp + bw,
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

    # 1. the pier: deck slab, fascia and pile stubs. Without these the buildings
    #    float - the app's terrain under a pier is water, not ground.
    deck = deck_outline()
    prism("deck", deck, Z_DECK_BOT, 0.0, mats["Toy_ink"], mats["Toy_stone"])

    per = deck_perimeter()
    total = 0.0
    for i in range(len(per) - 1):
        total += math.dist(per[i], per[i + 1])
    # pile stubs: the perimeter row plus two internal rows under the outer end,
    # which is the only stretch where the DEM has fallen to open water
    n_pile = 0
    walked = 0.0
    for i in range(len(per) - 1):
        seg = math.dist(per[i], per[i + 1])
        k = max(1, int(seg / 9.0))
        for j in range(k):
            t = (j + 0.5) / k
            x = per[i][0] + (per[i + 1][0] - per[i][0]) * t
            y = per[i][1] + (per[i + 1][1] - per[i][1]) * t
            cx, cy = (x - deck_centroid()[0]) * 0.985 + deck_centroid()[0], \
                     (y - deck_centroid()[1]) * 0.985 + deck_centroid()[1]
            verts = [(cx - 0.45, cy - 0.45), (cx + 0.45, cy - 0.45),
                     (cx + 0.45, cy + 0.45), (cx - 0.45, cy + 0.45)]
            prism(f"pile_{n_pile}", verts, Z_PILE_BOT, Z_DECK_BOT + 0.05,
                  mats["Toy_ink"])
            n_pile += 1
        walked += seg
    for row_p in (4.0, 20.0):
        for a in range(150, 205, 9):
            cx, cy = W(a, row_p)
            verts = [(cx - 0.45, cy - 0.45), (cx + 0.45, cy - 0.45),
                     (cx + 0.45, cy + 0.45), (cx - 0.45, cy + 0.45)]
            prism(f"pile_i{n_pile}", verts, Z_PILE_BOT, Z_DECK_BOT + 0.05,
                  mats["Toy_ink"])
            n_pile += 1

    # 2. the bulkhead slab, split either side of the Belt Railroad portal so the
    #    pass-through is a real hole in the massing, not a painted-on recess.
    for tag, p0, p1 in (("nw", P_BULK_NW, PORTAL_P0), ("se", PORTAL_P1, P_BULK_SE)):
        box(f"bulkhead_{tag}", A_FRONT, A_BULK_BACK, p0, p1, 0.0, Z_WING,
            mats["Toy_cream"], mats["Toy_stone"])
        box(f"bulkhead_{tag}_cope", A_FRONT - 0.12, A_BULK_BACK, p0, p1,
            Z_WING - EMBED, Z_WING_COPE, mats["Toy_white"])
        box(f"bulkhead_{tag}_plinth", A_FRONT - 0.10, A_BULK_BACK, p0, p1,
            0.0, Z_PLINTH, mats["Toy_stone"])
    box("portal_lintel", A_FRONT, A_BULK_BACK, PORTAL_P0, PORTAL_P1,
        PORTAL_Z, Z_WING, mats["Toy_cream"], mats["Toy_stone"])
    box("portal_lintel_cope", A_FRONT - 0.12, A_BULK_BACK, PORTAL_P0, PORTAL_P1,
        Z_WING - EMBED, Z_WING_COPE, mats["Toy_white"])
    box("portal_head", A_FRONT - 0.14, A_FRONT + 0.5, PORTAL_P0 - 0.35,
        PORTAL_P1 + 0.35, PORTAL_Z - 0.45, PORTAL_Z + 0.25, mats["Toy_white"])

    # 3. wing bays: flat pilaster strips, an upper band of narrow steel-sash
    #    windows per bay, shopfronts and doors below.
    wings = ((P_BULK_NW, PAV_P - PAV_W / 2.0), (PAV_P + PAV_W / 2.0, P_BULK_SE))
    for wi, (p0, p1) in enumerate(wings):
        span = p1 - p0
        nbay = max(2, int(round(span / 5.4)))
        for b in range(nbay + 1):
            p = p0 + span * b / nbay
            box(f"wpil_{wi}_{b}", A_FRONT - WING_PIL_PROUD, A_FRONT + EMBED,
                p - WING_PIL_W / 2, p + WING_PIL_W / 2, 0.0, Z_WING_COPE,
                mats["Toy_cream"])
        for b in range(nbay):
            pc = p0 + span * (b + 0.5) / nbay
            bw = span / nbay - WING_PIL_W - 0.5
            if bw < 1.2:
                continue
            # upper band: three narrow lights
            for k in range(3):
                cw = bw / 3.0
                cpc = pc - bw / 2 + cw * (k + 0.5)
                box(f"wwin_{wi}_{b}_{k}_gl", A_FRONT - 0.02, A_FRONT + RECESS,
                    cpc - cw * 0.30, cpc + cw * 0.30,
                    WING_WIN_Z[0], WING_WIN_Z[1], mats["Toy_glass"])
                box(f"wwin_{wi}_{b}_{k}_tr", A_FRONT - 0.05, A_FRONT + RECESS,
                    cpc - cw * 0.30, cpc + cw * 0.30,
                    WING_WIN_Z[0] + 1.05, WING_WIN_Z[1] - 1.15,
                    mats["Toy_glassl"])
            # ground floor: a glazed shopfront bay
            box(f"wgf_{wi}_{b}_gl", A_FRONT - 0.03, A_FRONT + 0.16,
                pc - bw / 2, pc + bw / 2, WING_GF_Z[0], WING_GF_Z[1],
                mats["Toy_glass"])
            box(f"wgf_{wi}_{b}_tr", A_FRONT - 0.06, A_FRONT + 0.16,
                pc - bw / 2, pc + bw / 2, WING_GF_Z[1] - 0.85,
                WING_GF_Z[1] - 0.70, mats["Toy_glassl"])
            glow_quad(f"wgf_{wi}_{b}_glow", A_FRONT - 0.10, A_FRONT - 0.10,
                      pc - bw / 2, pc + bw / 2, WING_GF_Z[0], WING_GF_Z[1],
                      mats["Toy_glassl_Glow"], (-1, 0))

    # 4. the frontispiece: pavilion, quoins, entablature, pediment, arch.
    #
    # Everything above the wing parapet is a SCREEN 2.7 m deep, not a 13.6 m deep
    # block. The real pavilion is a frontispiece on a shallow bulkhead building;
    # the first build extruded the pediment the full depth of the bulkhead and it
    # read as a gabled hall with the shed growing out of its back.
    pv0, pv1 = PAV_P - PAV_W / 2.0, PAV_P + PAV_W / 2.0
    A_PAV = A_FRONT - PAV_PROUD          # the pavilion's own face plane
    A_SCREEN = A_PAV + 2.7               # back of the raised screen
    box("pavilion", A_PAV, A_BULK_BACK, pv0, pv1, 0.0, Z_WING,
        mats["Toy_white"], mats["Toy_stone"])
    box("pav_screen", A_PAV, A_SCREEN, pv0, pv1, Z_WING - EMBED, Z_CORNICE0,
        mats["Toy_white"])
    for tag, p in (("nw", pv0 + QUOIN_W / 2), ("se", pv1 - QUOIN_W / 2)):
        box(f"quoin_{tag}", A_PAV - 0.18, A_PAV + EMBED,
            p - QUOIN_W / 2, p + QUOIN_W / 2, 0.0, Z_CORNICE1, mats["Toy_white"])
    box("entab", A_PAV - 0.36, A_SCREEN, pv0 - 0.32, pv1 + 0.32,
        Z_CORNICE0 - EMBED, Z_CORNICE1, mats["Toy_white"])
    box("entab_step", A_PAV - 0.20, A_SCREEN, pv0 - 0.16, pv1 + 0.16,
        Z_CORNICE0 - 0.38, Z_CORNICE0, mats["Toy_white"])

    # low raked pediment with a flattened apex, on the same 2.7 m screen
    ped = [(pv0 + 0.5, Z_CORNICE1 - EMBED), (PAV_P - 4.2, Z_CREST),
           (PAV_P + 4.2, Z_CREST), (pv1 - 0.5, Z_CORNICE1 - EMBED)]
    verts, faces = [], []
    for a_at in (A_PAV - 0.22, A_SCREEN):
        for p, z in ped:
            x, y = W(a_at, p)
            verts.append((x, y, z))
    n = len(ped)
    for i in range(n - 1):
        faces.append((i, i + 1, n + i + 1, n + i))
    faces.append((n - 1, 0, n, 2 * n - 1))
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    new_mesh("pediment", verts, faces, [mats["Toy_white"]])

    # PIER . 1 in the tympanum. Slate blue on white: the incised stone letters of
    # the real frieze are a value difference the app's camera cannot resolve, and
    # identity has to survive at thumbnail size (style bible s.8).
    lettering("pier1", "PIER.1", PAV_P, Z_CORNICE1 + 0.62, 1.45,
              A_PAV - 0.24, mats["Toy_navy"], gap=0.46)

    # The great arch. A recess cut into a solid is not available without booleans,
    # so the opening is a dark panel standing 0.06 m PROUD of the pavilion face,
    # ringed by an archivolt standing 0.25 m proud of that. From the app's camera
    # the ring's own shadow reads as the reveal.
    arch_face("arch_glass", ARCH_W, ARCH_SPRING, A_PAV - 0.06, mats["Toy_glass"])
    prof = arch_profile(ARCH_W, ARCH_SPRING)
    prof_o = arch_profile(ARCH_W + 2 * VOUSSOIR, ARCH_SPRING - VOUSSOIR * 0.6)
    verts, faces = [], []
    a0, a1 = A_PAV - 0.30, A_PAV + 0.10
    for a_at in (a0, a1):
        for p, z in prof:
            x, y = W(a_at, p)
            verts.append((x, y, z))
        for p, z in prof_o:
            x, y = W(a_at, p)
            verts.append((x, y, z))
    # Vertex blocks: [0, m) inner arc at a0 · [m, 2m) outer arc at a0 ·
    # [2m, 3m) inner arc at a1 · [3m, 4m) outer arc at a1.
    m = len(prof)
    k = 2 * m
    for i in range(m - 1):
        faces.append((i, i + 1, m + i + 1, m + i))                       # front
        faces.append((k + i, k + m + i, k + m + i + 1, k + i + 1))       # back
        faces.append((i, k + i, k + i + 1, i + 1))                       # soffit
        faces.append((m + i, m + i + 1, k + m + i + 1, k + m + i))       # extrados
    # Cap both springing ends, or the archivolt is an open tube with no signed
    # volume for the validator's authoritative normals test to work on.
    faces.append((0, m, k + m, k))
    faces.append((m - 1, k + m - 1, k + 2 * m - 1, 2 * m - 1))
    new_mesh("voussoirs", verts, faces, [mats["Toy_white"]])
    box("arch_band", A_PAV - 0.14, A_PAV - 0.04, PAV_P - ARCH_W / 2 + 0.5,
        PAV_P + ARCH_W / 2 - 0.5, 3.55, 4.15, mats["Toy_navy"])
    box("arch_doors", A_PAV - 0.16, A_PAV - 0.02, PAV_P - 3.2, PAV_P + 3.2,
        0.0, 3.3, mats["Toy_navy"])
    box("arch_mull", A_PAV - 0.13, A_PAV - 0.05, PAV_P - 0.10, PAV_P + 0.10,
        4.15, ARCH_SPRING + ARCH_W / 2 - 0.4, mats["Toy_glassl"])
    glow_quad("arch_glow", A_PAV - 0.20, A_PAV - 0.20,
              PAV_P - ARCH_W / 2 + 0.35, PAV_P + ARCH_W / 2 - 0.35,
              0.3, ARCH_SPRING + ARCH_W / 2 - 0.5, mats["Toy_glassl_Glow"],
              (-1, 0))

    # 5. the shed: one lofted solid so the taper is a real chamfer, not a step.
    shed_poly = [(A_BULK_BACK, 0.0), (A_SHED_END, 0.0),
                 (A_SHED_END, P_OUTER_SE), (A_TAPER1, P_OUTER_SE),
                 (A_TAPER0, P_BODY_SE), (A_HEAD_END, P_BODY_SE),
                 (A_HEAD_END, P_HEAD_SE), (A_BULK_BACK, P_HEAD_SE)]
    prism("shed", poly(shed_poly), 0.0, Z_SHED, mats["Toy_cream"],
          mats["Toy_stone"])
    rim("shed_cope", poly(shed_poly), 0.55, Z_SHED - EMBED, Z_SHED_COPE,
        mats["Toy_cream"])
    prism("shed_plinth", offset_polygon(poly(shed_poly), 0.10), 0.0, Z_PLINTH,
          mats["Toy_stone"])

    # shed bays, both flanks and the north-east end
    nb = 0
    lit = set(LIT_PATTERN)
    nbays = int((A_SHED_END - A_BULK_BACK) / SHED_BAY)
    for b in range(nbays):
        a_c = A_BULK_BACK + SHED_BAY * (b + 0.5)
        a0, a1 = a_c - SHED_BAY / 2, a_c + SHED_BAY / 2
        for side in (0, 1):
            p_w = 0.0 if side == 0 else shed_se(a_c)
            out = -1 if side == 0 else 1
            pi = p_w + out * SHED_PIL_PROUD
            # pilaster on the bay's leading edge
            box(f"spil_{b}_{side}", a0 - SHED_PIL_W / 2, a0 + SHED_PIL_W / 2,
                min(p_w, pi), max(p_w, pi), Z_PLINTH - EMBED, Z_SHED_COPE,
                mats["Toy_cream"])
            box(f"scorb_{b}_{side}", a0 - SHED_PIL_W / 2 - 0.12,
                a0 + SHED_PIL_W / 2 + 0.12,
                min(p_w, p_w + out * (SHED_PIL_PROUD + 0.12)),
                max(p_w, p_w + out * (SHED_PIL_PROUD + 0.12)),
                Z_SHED - 0.75, Z_SHED - 0.35, mats["Toy_cream"])
            # Main window group: a recessed steel reveal with the dark glazing
            # sitting inside it, so the opening reads as a framed sash rather
            # than as one flat navy panel. The first build made the "frame" a
            # solid slab standing proud of the glass, which hid the glass
            # entirely and turned the flank into a picket fence.
            pr = p_w - out * RECESS
            # 4.5 m of glass in a 7.5 m bay, not 6.0: at 6 m the openings ran
            # into one another and the flank read as a continuous glazed ribbon
            # instead of the pier-shed rhythm of solid piers between windows.
            window_pair(f"swin_{b}_{side}", a0 + 1.5, a1 - 1.5, p_w, pr, out,
                        SHED_WIN_Z[0], SHED_WIN_Z[1], mats)
            # clerestory band
            window_pair(f"scl_{b}_{side}", a0 + 1.5, a1 - 1.5, p_w, pr, out,
                        SHED_CLERE_Z[0], SHED_CLERE_Z[1], mats)
            if b in lit:
                glow_quad(f"scl_{b}_{side}_glow", a0 + 1.5, a1 - 1.5,
                          p_w + out * 0.07, p_w + out * 0.07,
                          SHED_CLERE_Z[0], SHED_CLERE_Z[1],
                          mats["Toy_glass_Glow"], (0, out))
            nb += 1
        # belt course, run per bay so it follows the taper
        for side in (0, 1):
            p_w = 0.0 if side == 0 else shed_se(a_c)
            out = -1 if side == 0 else 1
            box(f"sbelt_{b}_{side}", a0, a1,
                min(p_w, p_w + out * 0.10), max(p_w, p_w + out * 0.10),
                Z_BELT, Z_BELT + 0.22, mats["Toy_stone"])
    # north-east end wall gets the same rhythm, three bays across
    for k in range(3):
        pc = P_OUTER_SE * (k + 0.5) / 3.0
        bw = P_OUTER_SE / 3.0
        box(f"send_win_{k}", A_SHED_END - RECESS, A_SHED_END + 0.02,
            pc - bw * 0.32, pc + bw * 0.32, SHED_WIN_Z[0], SHED_WIN_Z[1],
            mats["Toy_glass"])
        box(f"send_cl_{k}", A_SHED_END - RECESS, A_SHED_END + 0.02,
            pc - bw * 0.32, pc + bw * 0.32, SHED_CLERE_Z[0], SHED_CLERE_Z[1],
            mats["Toy_glass"])
        box(f"send_pil_{k}", A_SHED_END, A_SHED_END + SHED_PIL_PROUD,
            pc - bw / 2 - SHED_PIL_W / 2, pc - bw / 2 + SHED_PIL_W / 2,
            Z_PLINTH - EMBED, Z_SHED_COPE, mats["Toy_cream"])

    # 6. the roof: monitor spine, two solar fields, vents and hatches.
    mon = []
    for a in (MON_A0, A_HEAD_END, A_TAPER0, A_TAPER1, MON_A1):
        mon.append((a, shed_centre(a) - MON_HALF))
    for a in (MON_A1, A_TAPER1, A_TAPER0, A_HEAD_END, MON_A0):
        mon.append((a, shed_centre(a) + MON_HALF))
    prism("monitor", poly(mon), Z_SHED - EMBED, Z_MONITOR, mats["Toy_stone"])
    # the spine's south-east clerestory band
    gl = []
    for a in (MON_A0 + 3, A_HEAD_END, A_TAPER0, A_TAPER1, MON_A1 - 3):
        gl.append((a, shed_centre(a) + MON_HALF - 0.10))
    for a in (MON_A1 - 3, A_TAPER1, A_TAPER0, A_HEAD_END, MON_A0 + 3):
        gl.append((a, shed_centre(a) + MON_HALF + EMBED))
    prism("mon_glass", poly(gl), Z_MONITOR - 1.55, Z_MONITOR - 0.35,
          mats["Toy_glassl"])
    # the array that rides on top of the spine, the length of the shed
    sol = []
    for a in (MON_A0 + 3, A_HEAD_END, A_TAPER0, A_TAPER1, MON_A1 - 3):
        sol.append((a, shed_centre(a) - SOLAR_HALF))
    for a in (MON_A1 - 3, A_TAPER1, A_TAPER0, A_HEAD_END, MON_A0 + 3):
        sol.append((a, shed_centre(a) + SOLAR_HALF))
    prism("solar_spine", poly(sol), Z_MONITOR - EMBED, Z_MONITOR + SOLAR_T,
          mats["Toy_navy"])
    # past OUTER_SOLAR_A0 the arrays spill onto the flat roof either side too
    for side, sgn in (("nw", -1), ("se", 1)):
        pts = []
        for a in (OUTER_SOLAR_A0, MON_A1 - 3):
            pts.append((a, shed_centre(a) + sgn * (MON_HALF + 1.0)))
        for a in (MON_A1 - 3, OUTER_SOLAR_A0):
            pts.append((a, shed_centre(a) + sgn * (MON_HALF + 6.5)))
        prism(f"solar_outer_{side}", poly(pts), Z_SHED - EMBED,
              Z_SHED + SOLAR_T + 0.18, mats["Toy_navy"])
    for i, (a, dp) in enumerate(((6, -7.0), (44, 8.5), (78, -8.0), (112, 7.0),
                                 (158, -6.5), (186, 6.0))):
        cyl(f"roof_vent_{i}", a, shed_centre(a) + dp, Z_SHED - EMBED,
            Z_SHED + 0.85, 0.6, 10, mats["Toy_steel"])
    for i, (a, dp) in enumerate(((16, 9.0), (62, -9.5), (128, 8.0), (172, -7.5))):
        box(f"roof_hatch_{i}", a - 0.9, a + 0.9,
            shed_centre(a) + dp - 0.7, shed_centre(a) + dp + 0.7,
            Z_SHED - EMBED, Z_SHED + 0.45, mats["Toy_steel"])

    # 7. apron furniture: the railing ring, bollards, and the globe lamp
    #    standards that line the south-east promenade.
    per = deck_perimeter()
    npost = 0
    for i in range(len(per) - 1):
        ax, ay = per[i]
        bx, by = per[i + 1]
        seg = math.hypot(bx - ax, by - ay)
        k = max(1, int(seg / RAIL_PITCH))
        nx, ny = (bx - ax) / seg, (by - ay) / seg
        ix, iy = -ny * 0.55, nx * 0.55          # pull the rail in off the edge
        s = _side_sign(per)
        ix, iy = ix * s, iy * s
        verts = [(ax + ix - ny * 0.05, ay + iy + nx * 0.05),
                 (bx + ix - ny * 0.05, by + iy + nx * 0.05),
                 (bx + ix + ny * 0.05, by + iy - nx * 0.05),
                 (ax + ix + ny * 0.05, ay + iy - nx * 0.05)]
        prism(f"rail_{i}", verts, RAIL_Z - 0.09, RAIL_Z, mats["Toy_navy"])
        for j in range(k):
            t = (j + 0.5) / k
            px, py = ax + (bx - ax) * t + ix, ay + (by - ay) * t + iy
            prism(f"railpost_{npost}",
                  [(px - 0.05, py - 0.05), (px + 0.05, py - 0.05),
                   (px + 0.05, py + 0.05), (px - 0.05, py + 0.05)],
                  0.0, RAIL_Z, mats["Toy_navy"])
            npost += 1
    nbol = 0
    for a in range(0, int(A_SHED_END), int(BOLLARD_PITCH)):
        for p in (P_DECK_NW + 3.0, shed_se(a) + 3.4):
            if p > shed_se(a) + 8.0:
                continue
            cyl(f"bollard_{nbol}", a, p, 0.0, 0.72, 0.26, 6, mats["Toy_ink"])
            nbol += 1
    for i in range(8):
        a = 4.0 + i * 24.0
        p = shed_se(a) + 4.6
        cyl(f"lamp_{i}", a, p, 0.0, LAMP_H, 0.14, 6, mats["Toy_ink"])
        sphere(f"lampglobe_{i}", a, p, LAMP_H + 0.42, 0.42, mats["Toy_glassl"])

    # 8. bevels. The chunky masses carry the miniature read and get the full
    #    0.10/2. Glazing, frames, glow faces, railing and letters are thin and
    #    numerous - a bevel there buys nothing at the app's camera and costs
    #    thousands of triangles.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        n = obj.name
        if n.startswith(("rail", "pile", "letter", "pier1_", "bollard", "lamp",
                         "swin", "scl", "wwin", "wgf", "send_", "sbelt",
                         "arch_", "voussoirs", "mon_glass", "solar_",
                         "roof_hatch", "roof_vent", "scorb", "spil",
                         "shed_cope")):
            continue
        if "_glow" in n or "_fr" in n:
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
    """+1 if the inward normal of a perimeter run is (-ny, nx), else -1."""
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

    blend = os.path.join(out, "pier-1.blend")
    glb = os.path.join(out, "pier-1.glb")
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
