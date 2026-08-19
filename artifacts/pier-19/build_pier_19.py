"""Deterministic Blender build of the SF-SIM miniature Pier 19.

    blender -b --python build_pier_19.py -- [--out DIR]

Writes pier-19.blend and pier-19.glb next to this file (or into --out). Geometry
is authored in world space in metres, Z up, +X east, +Y north, so the model drops
into the city at its real-world heading - the loader applies no rotation.

ORIGIN: same convention as pier-1, which broke the usual "min Z = 0" rule on
purpose and shipped. Local Z = 0 is the TOP OF THE PIER DECK; the deck fascia and
pile stubs run down to -2.2 m. placeGeneric() seats the GLB's origin on one
terrain sample at the anchor, and the app's DEM carries these Embarcadero piers
as low ridges (~2.4 m at Pier 1), so a model that sat on z = 0 would float above
its own deck. `targetHeightM` is therefore the model's total VERTICAL EXTENT
(-2.2 .. +15.0 = 17.2), not a height above water.

Design (see REFERENCE.md and docs/asset-plans/pier-19.md for sources):

* a 1936-38 finger pier, near-identical twin of Pier 9: a classical stucco
  BULKHEAD BUILDING on the Embarcadero (broad pavilion, monumental round arch
  with a steel roll-up door, PIER 19 over the arch, GABLED PARAPET whose crest is
  the top of the asset), and a 195 m TRANSIT SHED with scored precast-concrete
  walls and a CONTINUOUS ROOF MONITOR running its full length;
* between the bulkhead building and the 1936 shed front, the pier's own strip of
  the 1961 Pier 19-23 connector reads as a lower FLAT-ROOFED EXTENSION of the
  shed (the connector itself, spanning the slip to Pier 23, is out of scope);
* the rear (bay-end) elevation is faintly Art Deco: six profiled pilasters
  rising to peaks just above the roofline around a gabled central bay (NRHP);
* Pier 19 is a working storage pier: no railing ring, no parking field - fender
  piles, mooring bitts, a few lamp standards on the south apron. The north apron
  (Pier 23 slip side) is closed/deteriorated in reality and stays bare;
* the pier's long axis bears 054.89 deg, the facade faces 234.89 deg; the
  axis-aligned XY bbox is ~241 x 190 m even though the pier is 262 x 47 m;
* the flagpole that gives DataSF its 19.5-20.4 m max is NOT modelled: a hairline
  pole as the bbox top would rescale every wall (plan 2.15 risk 1). The bbox top
  is the gable crest cap: 15.0 m above deck, 17.0 m above water;
* night state: the monitor clerestory is the hero, lit in a scattered pattern -
  a storage pier at night is a dark mass with a few working bays - plus a warm
  lunette over the arch entry. Glow surfaces are single open faces standing
  proud of opaque glazing, never closed shells.
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

# The design frame's origin: (along 0, perp 0) - the pier centreline where it
# meets the Embarcadero street frontage. Derived in the plan's 2.3 from the
# deck-rectangle centre -122.3988051, 37.8030166 minus half the deck length.
DESIGN_ANCHOR = (-122.4000240, 37.8023351)

AXIS_BEARING = 54.89          # measured from the merged OSM ring's shed edge

# --- plan geometry, in (along a, perp p) metres. a=0 street frontage, +a into
# the bay; p=0 pier centreline, +p south-east (the Pier 17 / working side).
A_FRONT = 0.0
A_BULK_BACK = 12.0            # bulkhead building depth
A_EXT_END = 57.6              # 1961 flat extension ends / 1936 shed front
A_SHED_END = 252.5            # shed rear (bay-end) wall
A_DECK_END = 262.13           # head apron edge (60 ft wharf + 800 ft pier)

P_DECK = 23.32                # deck half-width (153 ft / 2)
P_WING = 26.5                 # bulkhead building half-frontage (53 m total)
P_SHED = 17.15                # shed half-width (34.3 m)

# --- heights above the deck (deck top = local z 0; water at -2.0)
Z_PILE_BOT = -2.2
Z_DECK_BOT = -0.55
Z_PLINTH = 0.7
Z_EXT = 9.0                   # flat 1961 extension roof
Z_EAVE = 9.8                  # shed side-wall eave
Z_RIDGE = 11.0                # roof planes rise to the monitor base
Z_MON = 12.8                  # monitor top (14.8 above water)
MON_HALF = 3.0
CLERE_Z = (11.35, 12.35)      # monitor clerestory band
Z_WING = 9.5                  # bulkhead wing parapet (11.5 above water)
Z_WING_COPE = 9.85
Z_PAV = 10.4                  # pavilion block top (just above the arch crown)
Z_ATTIC = 12.4                # attic screen top / gable base
Z_CREST = 15.0                # gable crest cap - the bbox top (17.0 above water)

# --- the pavilion & arch
PAV_W = 18.0
PAV_PROUD = 0.9
ARCH_W = 11.0
ARCH_SPRING = 4.5             # crown at 4.5 + 5.5 = 10.0 (12.0 above water)
ARCH_SEGS = 10
VOUSSOIR = 0.55

# --- rhythms
WING_PIL_W, WING_PIL_PROUD = 0.9, 0.14
WING_WIN_Z = (2.2, 7.8)
SHED_BAY = 9.745              # 20 bays over the 1936 shed
SHED_PIL_W, SHED_PIL_PROUD = 0.75, 0.09
DOOR_W, DOOR_H = 5.0, 4.6
SHED_WIN_Z = (6.2, 8.6)
RECESS = 0.14
EMBED = 0.03                  # applied bands sink into their face - no two
                              # solids share a coincident plane

BEVEL_W, BEVEL_SEG = 0.10, 2

LAMP_H = 4.0

# Which monitor clerestory bays are lit at night, by index. Scattered on
# purpose: a storage pier is mostly dark, with a few working bays.
LIT_PATTERN = (1, 2, 5, 8, 9, 13, 16, 17)

PALETTE_HEX = {
    "Toy_cream": "f2ede3",     # bulkhead stucco, shed pilasters
    "Toy_white": "f7f4ec",     # pavilion face, voussoirs, copings, gable
    "Toy_stone": "d9d2c2",     # shed walls, roof, deck top, plinths
    "Toy_ink": "3a3530",       # deck fascia, piles, fenders, bitts, lettering
    "Toy_navy": "2c4a70",      # window frames, arch band, pedestrian doors
    "Toy_glass": "2a4d73",     # graphical glazing
    "Toy_steel": "9aa0a6",     # roll-up doors, plated windows, roof vents
    "Toy_glassl": "6f95b8",    # clerestory glazing band, transoms, lamp globes
    # Night. A _Glow material's BASE colour is what the app draws at night (the
    # glow layer is unlit), so these are authored as the colour to be SEEN.
    "Toy_glassl_Glow": "f4dcb0",   # the arch lunette
    "Toy_glass_Glow": "cbd8e0",    # the lit monitor clerestory bays, cooler
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


def loft(name, section_pz, a0, a1, mat, mat_top=None):
    """Closed solid: a (p, z) cross-section polygon extruded from a0 to a1.
    Used for the shed's roof wedge and the pavilion gable, whose sections are
    not rectangles. Winding settled by recalc (closed manifold)."""
    n = len(section_pz)
    verts = []
    for a_at in (a0, a1):
        for p, z in section_pz:
            x, y = W(a_at, p)
            verts.append((x, y, z))
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    return new_mesh(name, verts, faces, [mat])


def glow_quad(name, a0, a1, p0, p1, z0, z1, mat, out_dir):
    """One OPEN, single-layer, outward-facing quad (see pier-1: night glow is
    never a closed shell - the app draws _Glow in a separate translucent layer,
    and a box reads at twice the intended day alpha). `out_dir` is the outward
    direction in the pier frame as (da, dp); winding is CHECKED against it."""
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
    """Miniature-style edge softening, capped at a third of the thinnest
    dimension so thin bands do not collapse into slivers."""
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


def arch_profile(w, spring, segs=ARCH_SEGS):
    """(p, z) points of a round-headed opening of width `w` centred on p=0."""
    r = w / 2.0
    pts = [(-r, 0.0), (-r, spring)]
    for i in range(1, segs):
        ang = math.pi * i / segs
        pts.append((-r * math.cos(ang), spring + r * math.sin(ang)))
    pts += [(r, spring), (r, 0.0)]
    return pts


def arch_face(name, w, spring, a_at, mat, z0=0.0):
    """A flat vertical slab filling a round-headed opening, in the plane
    a = a_at, facing -a (the street)."""
    prof = arch_profile(w, spring)
    verts, faces = [], []
    for p, z in prof:
        x, y = W(a_at, p)
        verts.append((x, y, z0 + z))
    x, y = W(a_at, 0.0)
    verts.append((x, y, z0))
    c = len(verts) - 1
    for i in range(len(prof) - 1):
        faces.append((c, i, i + 1))
    return new_mesh(name, verts, faces, [mat])


def window_pair(name, a0, a1, p_wall, p_recess, out, z0, z1, mats,
                glass="Toy_glass"):
    """A recessed opening: one dark graphical glazing panel with a single light
    transom bar. Both boxes poke 0.02-0.05 m PROUD of the wall plane (a purely
    coplanar or recessed box z-fights or vanishes into the solid)."""
    p_out = p_wall + out * 0.02
    box(f"{name}_gl", a0, a1, min(p_out, p_recess), max(p_out, p_recess),
        z0, z1, mats[glass])
    p_tr = p_wall + out * 0.05
    zt = z0 + (z1 - z0) * 0.42
    box(f"{name}_tr", a0, a1, min(p_tr, p_recess), max(p_tr, p_recess),
        zt, zt + 0.16, mats["Toy_glassl"])


# LETTERS: PIER 19, built from rectangles in the pavilion's (p, z) plane.
# Extruded, not painted - recognition cue #1 must survive the aerial camera.
def letter_boxes(ch, w, h):
    s = w * 0.22
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
    if ch == "9":
        # blocky 9: full-height right stroke, upper loop (left stroke upper
        # half, top bar, middle bar)
        return [(w - s, 0, s, h), (0, h / 2, s, h / 2), (0, h - s, w, s),
                (0, h / 2 - s / 2, w, s)]
    return []


def lettering(name, text, p_c, z0, h, a_at, mat, gap=0.30):
    lw = h * 0.62
    widths = [lw * (0.45 if c == " " else 1.0) for c in text]
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

    # 1. the pier: deck slab, fascia and pile stubs. Without these the
    #    buildings float - the app's terrain under the outer pier is water.
    deck_pts = [(A_FRONT, -P_DECK), (A_DECK_END, -P_DECK),
                (A_DECK_END, P_DECK), (A_FRONT, P_DECK)]
    prism("deck", poly(deck_pts), Z_DECK_BOT, 0.0, mats["Toy_ink"],
          mats["Toy_stone"])

    # pile stubs: a perimeter row on the three water sides, plus internal rows
    # under the head where the DEM has certainly fallen to open water
    n_pile = 0
    per = poly([(A_FRONT + 2.0, -P_DECK), (A_DECK_END, -P_DECK),
                (A_DECK_END, P_DECK), (A_FRONT + 2.0, P_DECK)])
    for i in range(len(per) - 1):
        ax_, ay_ = per[i]
        bx_, by_ = per[i + 1]
        seg = math.hypot(bx_ - ax_, by_ - ay_)
        k = max(1, int(seg / 9.0))
        for j in range(k):
            t = (j + 0.5) / k
            x = ax_ + (bx_ - ax_) * t
            y = ay_ + (by_ - ay_) * t
            cx, cy = W(*_pull_in(x, y))
            verts = [(cx - 0.45, cy - 0.45), (cx + 0.45, cy - 0.45),
                     (cx + 0.45, cy + 0.45), (cx - 0.45, cy + 0.45)]
            prism(f"pile_{n_pile}", verts, Z_PILE_BOT, Z_DECK_BOT + 0.05,
                  mats["Toy_ink"])
            n_pile += 1
    for row_p in (-8.0, 8.0):
        for a in range(205, 260, 9):
            cx, cy = W(a, row_p)
            verts = [(cx - 0.45, cy - 0.45), (cx + 0.45, cy - 0.45),
                     (cx + 0.45, cy + 0.45), (cx - 0.45, cy + 0.45)]
            prism(f"pile_i{n_pile}", verts, Z_PILE_BOT, Z_DECK_BOT + 0.05,
                  mats["Toy_ink"])
            n_pile += 1

    # fender piles: the working edge's rhythm, proud of the deck fascia
    n_f = 0
    for a in range(6, int(A_DECK_END) - 2, 7):
        for sgn in (-1, 1):
            pc = sgn * (P_DECK + 0.22)
            box(f"fender_{n_f}", a - 0.22, a + 0.22, pc - 0.22, pc + 0.22,
                -1.8, 0.4, mats["Toy_ink"])
            n_f += 1
    for p in range(-20, 21, 7):
        box(f"fender_h{n_f}", A_DECK_END - 0.1, A_DECK_END + 0.34,
            p - 0.22, p + 0.22, -1.8, 0.4, mats["Toy_ink"])
        n_f += 1

    # 2. bulkhead building: wings, pavilion, arch, gable. The frontage is 53 m
    #    (wings run 3.2 m past the deck edges over the bulkhead wharf).
    for tag, p0, p1 in (("n", -P_WING, -PAV_W / 2), ("s", PAV_W / 2, P_WING)):
        box(f"bulkhead_{tag}", A_FRONT, A_BULK_BACK, p0, p1, 0.0, Z_WING,
            mats["Toy_cream"], mats["Toy_stone"])
        box(f"bulkhead_{tag}_cope", A_FRONT - 0.12, A_BULK_BACK, p0, p1,
            Z_WING - EMBED, Z_WING_COPE, mats["Toy_white"])
        box(f"bulkhead_{tag}_plinth", A_FRONT - 0.10, A_BULK_BACK, p0, p1,
            0.0, Z_PLINTH, mats["Toy_stone"])

    # wing bays: pilaster strips + tall steel-sash windows (the real wings are
    # a stucco wall with big industrial sashes, one storey with a mezzanine)
    for wi, (p0, p1) in enumerate(((-P_WING, -PAV_W / 2), (PAV_W / 2, P_WING))):
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
            # one tall sash trio per bay, framed navy, transom barred
            box(f"wwin_{wi}_{b}_fr", A_FRONT - 0.04, A_FRONT + RECESS,
                pc - bw / 2 - 0.12, pc + bw / 2 + 0.12,
                WING_WIN_Z[0] - 0.12, WING_WIN_Z[1] + 0.12, mats["Toy_navy"])
            box(f"wwin_{wi}_{b}_gl", A_FRONT - 0.06, A_FRONT + RECESS,
                pc - bw / 2, pc + bw / 2,
                WING_WIN_Z[0], WING_WIN_Z[1], mats["Toy_glass"])
            box(f"wwin_{wi}_{b}_tr", A_FRONT - 0.08, A_FRONT + RECESS,
                pc - bw / 2, pc + bw / 2,
                WING_WIN_Z[0] + (WING_WIN_Z[1] - WING_WIN_Z[0]) * 0.55,
                WING_WIN_Z[0] + (WING_WIN_Z[1] - WING_WIN_Z[0]) * 0.55 + 0.16,
                mats["Toy_glassl"])

    # 3. the pavilion. Block to just above the arch crown; above that a 2.5 m
    #    deep SCREEN carries the attic band, the lettering and the gable, so the
    #    parapet reads as a frontispiece, not a gabled hall (pier-1's lesson).
    pv0, pv1 = -PAV_W / 2, PAV_W / 2
    A_PAV = A_FRONT - PAV_PROUD
    A_SCREEN = A_PAV + 2.5
    box("pavilion", A_PAV, A_BULK_BACK, pv0, pv1, 0.0, Z_PAV,
        mats["Toy_white"], mats["Toy_stone"])
    box("pav_screen", A_PAV, A_SCREEN, pv0, pv1, Z_PAV - EMBED, Z_ATTIC,
        mats["Toy_white"])
    # monumental piers flanking the arch: broad banded strips, the facade's
    # strongest vertical elements after the arch itself
    for tag, p in (("n", pv0 + 1.4), ("s", pv1 - 1.4)):
        box(f"mpier_{tag}", A_PAV - 0.22, A_PAV + EMBED, p - 1.4, p + 1.4,
            0.0, Z_PAV + 0.35, mats["Toy_white"])
        for bz in range(5):
            box(f"mpier_{tag}_band{bz}", A_PAV - 0.30, A_PAV - 0.18,
                p - 1.4, p + 1.4, 1.1 + bz * 1.75, 1.1 + bz * 1.75 + 0.55,
                mats["Toy_cream"])
    # attic cornice under the gable
    box("attic_cornice", A_PAV - 0.34, A_SCREEN, pv0 - 0.30, pv1 + 0.30,
        Z_ATTIC - 0.42, Z_ATTIC, mats["Toy_white"])

    # the GABLED PARAPET: raked screen with a small crest cap at the apex -
    # the cap is the model's bbox top at exactly Z_CREST
    gab = [(pv0 + 0.4, Z_ATTIC - EMBED), (-2.0, Z_CREST - 0.28),
           (2.0, Z_CREST - 0.28), (pv1 - 0.4, Z_ATTIC - EMBED)]
    verts, faces = [], []
    for a_at in (A_PAV - 0.20, A_SCREEN):
        for p, z in gab:
            x, y = W(a_at, p)
            verts.append((x, y, z))
    n = len(gab)
    for i in range(n - 1):
        faces.append((i, i + 1, n + i + 1, n + i))
    faces.append((n - 1, 0, n, 2 * n - 1))
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    new_mesh("gable", verts, faces, [mats["Toy_white"]])
    box("gable_cap", A_PAV - 0.26, A_SCREEN + 0.06, -2.2, 2.2,
        Z_CREST - 0.30, Z_CREST, mats["Toy_white"])

    # PIER 19 on the attic band, navy on white (raised metal letters in
    # reality; a value difference is what survives the aerial camera)
    lettering("pier19", "PIER 19", 0.0, Z_PAV + 0.55, 1.30,
              A_PAV - 0.24, mats["Toy_navy"], gap=0.42)

    # the great arch: dark fill panel proud of the pavilion face, ringed by a
    # proud archivolt whose shadow reads as the reveal; steel roll-up door in
    # the lower half, warm glow lunette above it at night
    arch_face("arch_fill", ARCH_W, ARCH_SPRING, A_PAV - 0.06, mats["Toy_glass"])
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
    m = len(prof)
    k = 2 * m
    for i in range(m - 1):
        faces.append((i, i + 1, m + i + 1, m + i))
        faces.append((k + i, k + m + i, k + m + i + 1, k + i + 1))
        faces.append((i, k + i, k + i + 1, i + 1))
        faces.append((m + i, m + i + 1, k + m + i + 1, k + m + i))
    faces.append((0, m, k + m, k))
    faces.append((m - 1, k + m - 1, k + 2 * m - 1, 2 * m - 1))
    new_mesh("voussoirs", verts, faces, [mats["Toy_white"]])
    # roll-up door: horizontal-slatted read = one steel panel + two seam bars
    box("arch_door", A_PAV - 0.14, A_PAV - 0.02, -4.6, 4.6, 0.0, DOOR_H,
        mats["Toy_steel"])
    for i, zb in enumerate((1.5, 3.0)):
        box(f"arch_door_seam{i}", A_PAV - 0.16, A_PAV - 0.13, -4.6, 4.6,
            zb, zb + 0.10, mats["Toy_ink"])
    box("arch_band", A_PAV - 0.15, A_PAV - 0.04, -4.9, 4.9,
        DOOR_H, DOOR_H + 0.45, mats["Toy_navy"])
    glow_quad("arch_glow", A_PAV - 0.20, A_PAV - 0.20, -4.6, 4.6,
              DOOR_H + 0.55, ARCH_SPRING + ARCH_W / 2 - 0.55,
              mats["Toy_glassl_Glow"], (-1, 0))
    # pedestrian doors flanking the arch, and the cast-iron wheel guards
    for tag, pc in (("n", -6.6), ("s", 6.6)):
        box(f"ped_door_{tag}", A_PAV - 0.10, A_PAV + EMBED, pc - 0.8, pc + 0.8,
            0.0, 2.5, mats["Toy_navy"])
    for tag, pc in (("n", -ARCH_W / 2 - 0.35), ("s", ARCH_W / 2 + 0.35)):
        cyl(f"wheelguard_{tag}", A_PAV - 0.35, pc, 0.0, 0.75, 0.24, 8,
            mats["Toy_ink"])

    # 4. the 1961 flat extension: the pier's own strip of the connector era -
    #    lower, plain, flat-roofed, between the bulkhead building and the shed
    box("extension", A_BULK_BACK - 0.4, A_EXT_END + 0.4, -P_SHED, P_SHED,
        0.0, Z_EXT, mats["Toy_cream"], mats["Toy_stone"])
    # its bay rhythm continues the shed's, quieter: pilasters only
    nb_ext = int((A_EXT_END - A_BULK_BACK) / SHED_BAY) + 1
    for b in range(nb_ext):
        a_c = A_BULK_BACK + SHED_BAY * (b + 0.5)
        if a_c > A_EXT_END:
            break
        for side in (-1, 1):
            p_w = side * P_SHED
            box(f"epil_{b}_{side > 0}", a_c - SHED_BAY / 2 - SHED_PIL_W / 2,
                a_c - SHED_BAY / 2 + SHED_PIL_W / 2,
                min(p_w, p_w + side * SHED_PIL_PROUD),
                max(p_w, p_w + side * SHED_PIL_PROUD),
                Z_PLINTH - EMBED, Z_EXT - 0.25, mats["Toy_cream"])
    # two working roll-ups on the south flank of the extension
    for i, a_c in enumerate((22.0, 42.0)):
        box(f"edoor_{i}", a_c - DOOR_W / 2, a_c + DOOR_W / 2,
            P_SHED - 0.02, P_SHED + 0.05, 0.0, DOOR_H, mats["Toy_steel"])

    # 5. the 1936 transit shed: walls, roof wedge, continuous monitor
    box("shed", A_EXT_END, A_SHED_END, -P_SHED, P_SHED, 0.0, Z_EAVE,
        mats["Toy_cream"], mats["Toy_stone"])
    prism("shed_plinth",
          poly([(A_EXT_END + 0.1, -P_SHED - 0.10), (A_SHED_END - 0.1, -P_SHED - 0.10),
                (A_SHED_END - 0.1, P_SHED + 0.10), (A_EXT_END + 0.1, P_SHED + 0.10)]),
          0.0, Z_PLINTH, mats["Toy_stone"])
    # roof wedge: two low-pitch planes rising from the eaves to the monitor base
    roof = [(-P_SHED - 0.35, Z_EAVE - 0.45), (-P_SHED - 0.35, Z_EAVE),
            (-MON_HALF - 0.2, Z_RIDGE), (MON_HALF + 0.2, Z_RIDGE),
            (P_SHED + 0.35, Z_EAVE), (P_SHED + 0.35, Z_EAVE - 0.45)]
    loft("shed_roof", roof, A_EXT_END - 0.25, A_SHED_END + 0.25,
         mats["Toy_stone"])
    # the monitor: full length of the shed, clerestory band down both sides
    box("monitor", A_EXT_END + 2.5, A_SHED_END - 2.5, -MON_HALF, MON_HALF,
        Z_RIDGE - EMBED, Z_MON, mats["Toy_stone"], mats["Toy_stone"])
    for side in (-1, 1):
        p_w = side * MON_HALF
        box(f"mon_glass_{side > 0}", A_EXT_END + 4.0, A_SHED_END - 4.0,
            min(p_w - side * 0.12, p_w + side * 0.03),
            max(p_w - side * 0.12, p_w + side * 0.03),
            CLERE_Z[0], CLERE_Z[1], mats["Toy_glassl"])

    # shed wall bays: pilasters, roll-up doors on alternating bays, high strip
    # windows (south-flank windows read as steel plates - they are plated over
    # in reality; the north flank keeps glass)
    nbays = int(round((A_SHED_END - A_EXT_END) / SHED_BAY))
    lit = set(LIT_PATTERN)
    for b in range(nbays):
        a_c = A_EXT_END + SHED_BAY * (b + 0.5)
        a0, a1 = a_c - SHED_BAY / 2, a_c + SHED_BAY / 2
        for side in (-1, 1):
            p_w = side * P_SHED
            tag = "n" if side < 0 else "s"
            box(f"spil_{b}_{tag}", a0 - SHED_PIL_W / 2, a0 + SHED_PIL_W / 2,
                min(p_w, p_w + side * SHED_PIL_PROUD),
                max(p_w, p_w + side * SHED_PIL_PROUD),
                Z_PLINTH - EMBED, Z_EAVE - 0.25, mats["Toy_cream"])
            # roll-up door on even bays
            if b % 2 == 0:
                box(f"sdoor_{b}_{tag}", a_c - DOOR_W / 2, a_c + DOOR_W / 2,
                    min(p_w - side * 0.02, p_w + side * 0.05),
                    max(p_w - side * 0.02, p_w + side * 0.05),
                    0.0, DOOR_H, mats["Toy_steel"])
            # high strip window
            pr = p_w - side * RECESS
            glass = "Toy_glass" if side < 0 or b % 3 == 0 else "Toy_steel"
            window_pair(f"swin_{b}_{tag}", a0 + 1.6, a1 - 1.6, p_w, pr, side,
                        SHED_WIN_Z[0], SHED_WIN_Z[1], mats, glass=glass)
        # lit monitor clerestory bays (the night hero), open quads proud of
        # the continuous glassl band on both monitor flanks
        if b in lit:
            for side in (-1, 1):
                p_g = side * (MON_HALF + 0.07)
                glow_quad(f"mon_glow_{b}_{side > 0}", a0 + 1.2, a1 - 1.2,
                          p_g, p_g, CLERE_Z[0] + 0.05, CLERE_Z[1] - 0.05,
                          mats["Toy_glass_Glow"], (0, side))

    # 6. rear (bay-end) elevation: six profiled pilasters rising to peaks just
    #    above the roofline, gabled central bay, one roll-up
    for i in range(6):
        pc = -P_SHED + (i + 0.5) * (2 * P_SHED / 6)
        box(f"rpil_{i}", A_SHED_END - EMBED, A_SHED_END + 0.14,
            pc - 0.45, pc + 0.45, Z_PLINTH - EMBED, Z_EAVE + 0.55,
            mats["Toy_cream"])
        box(f"rpil_cap_{i}", A_SHED_END - EMBED, A_SHED_END + 0.20,
            pc - 0.55, pc + 0.55, Z_EAVE + 0.55, Z_EAVE + 0.80,
            mats["Toy_white"])
    # gabled centre: a raked parapet echoing the roof wedge behind it
    rear_gab = [(-6.0, Z_EAVE - EMBED), (0.0, Z_RIDGE + 0.75),
                (6.0, Z_EAVE - EMBED)]
    verts, faces = [], []
    for a_at in (A_SHED_END - 0.10, A_SHED_END + 0.24):
        for p, z in rear_gab:
            x, y = W(a_at, p)
            verts.append((x, y, z))
    faces = [(0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5), (2, 1, 0), (3, 4, 5)]
    new_mesh("rear_gable", verts, faces, [mats["Toy_cream"]])
    box("rear_door", A_SHED_END - 0.02, A_SHED_END + 0.05, -3.0, 3.0,
        0.0, 5.0, mats["Toy_steel"])
    for kwin, pc in ((0, -11.5), (1, 11.5)):
        box(f"rear_win_{kwin}", A_SHED_END - 0.02, A_SHED_END + 0.04,
            pc - 2.2, pc + 2.2, SHED_WIN_Z[0], SHED_WIN_Z[1],
            mats["Toy_glass"])

    # 7. deck furniture: mooring bitts on the head apron and south apron,
    #    lamp standards along the working south apron only
    n_b = 0
    for p in (-14.0, 0.0, 14.0):
        cyl(f"bitt_h{n_b}", A_DECK_END - 4.0, p, 0.0, 0.85, 0.30, 6,
            mats["Toy_ink"])
        n_b += 1
    for a in range(70, 250, 36):
        cyl(f"bitt_s{n_b}", a, P_DECK - 2.0, 0.0, 0.75, 0.26, 6,
            mats["Toy_ink"])
        n_b += 1
    for i in range(6):
        a = 30.0 + i * 42.0
        p = P_DECK - 1.6
        cyl(f"lamp_{i}", a, p, 0.0, LAMP_H, 0.14, 6, mats["Toy_ink"])
        sphere(f"lampglobe_{i}", a, p, LAMP_H + 0.42, 0.42, mats["Toy_glassl"])

    # 8. bevels: chunky masses only - glazing, frames, glow faces, letters,
    #    piles, fenders and furniture are thin and numerous
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        nm = obj.name
        if nm.startswith(("pile", "fender", "pier19_", "bitt", "lamp",
                          "swin", "wwin", "mon_glass", "sdoor", "edoor",
                          "rear_door", "rear_win", "arch_", "voussoirs",
                          "ped_door", "wheelguard", "spil", "epil", "rpil",
                          "mpier_", "attic_cornice", "gable_cap")):
            continue
        if "_glow" in nm.lower():
            continue
        bevel(obj)

    recentre()
    return scene


def _pull_in(x, y):
    """Pull a world point 1.5% toward the deck centroid (piles sit just inside
    the fascia). Returns pier-frame coords for W() round-trip symmetry."""
    cx, cy = W((A_FRONT + A_DECK_END) / 2.0, 0.0)
    px, py = cx + (x - cx) * 0.985, cy + (y - cy) * 0.985
    # invert W(): a = dot(P, U), p = dot(P, V) (U, V are orthonormal)
    a = px * U[0] + py * U[1]
    p = px * V[0] + py * V[1]
    return a, p


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

    blend = os.path.join(out, "pier-19.blend")
    glb = os.path.join(out, "pier-19.glb")
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
