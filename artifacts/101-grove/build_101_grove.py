"""Deterministic Blender build of the SF-SIM miniature 101 Grove Street.

    blender -b --python build_101_grove.py -- [--out DIR]

Writes 101-grove.blend and 101-grove.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint AABB centre (anchor lon -122.4186747,
lat 37.7781359), min Z = 0, balustrade top rail exactly 21.4 m.

Design (see REFERENCE.md for the sources behind every number):

* the true OSM polygon (way/35176281, block 811 lot 001) extruded as a four
  storey Beaux-Arts granite block on the Civic Center grid — Grove Street north,
  Polk Street east, Dr. Tom Waddell Place south, a stepped light-court wall west
  against the Bill Graham Civic Auditorium;
* the identity is the chamfered NORTH-EAST corner bay: a monumental round-arched
  entrance with a gold oculus in its tympanum, two lantern sconces, a
  gold-rosetted balconette over it, and a pedimented window above that;
* the second strongest thing is the horizontal: a rusticated base of three
  courses, a string course, then three smooth ashlar storeys under a bold
  projecting cornice and a continuous open balustrade at a dead-level 21.4 m —
  the Civic Center's mandated cornice line, which is what makes the district
  read as a district;
* the roof IS a facade here (style bible s.10) and the honest fact about it is a
  brilliant white cool-roof membrane inside a trim frame, with a low penthouse
  over the corner bay, an interior light court south of centre, and a tight
  mechanical cluster on the west third. Nothing on the roof breaks the
  balustrade line, which is both true and what keeps the height normalisation
  honest;
* night state: the entrance is the hero — the two lanterns, the oculus and the
  door transom read as one warm gold pool at the chamfer. Supporting: an
  irregular scatter of lit windows on Grove and Polk (a 24-hour public health
  building). Nothing on the roof glows. Glow surfaces are thin shells proud of
  opaque glazing — the app renders _Glow in a separate layer at ~12% alpha by
  day, so a primary surface must never be authored as glow.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/35176281 projected with the app's tangent projection (LON0 -122.4375,
# LAT0 37.77) and recentred on the footprint AABB centre. CCW, (x east, y north).
FOOTPRINT = [
    (-34.17, 13.32),    # P0  north-west corner (Grove / west party line)
    (-31.87, 0.21),     # P1  light-court step
    (-28.53, -0.31),    # P2
    (-26.81, -11.20),   # P3  light-court step
    (-30.10, -11.62),   # P4
    (-28.25, -22.72),   # P5  south-west corner
    (34.17, -12.99),    # P6  south-east corner (Polk / Waddell)
    (28.99, 18.29),     # P7  chamfer, south end
    (22.52, 22.72),     # P8  chamfer, north end
]
E_W1 = (0, 1)       # west wall, north segment, 13.31 m
E_STEP1 = (1, 2)    # light-court step, 3.38 m
E_W2 = (2, 3)       # west wall, middle segment (the court), 11.02 m
E_STEP2 = (3, 4)    # light-court step, 3.31 m
E_W3 = (4, 5)       # west wall, south segment, 11.25 m
E_SOUTH = (5, 6)    # Dr. Tom Waddell Place, 63.17 m, outward normal 170.6 deg
E_POLK = (6, 7)     # Polk Street, 31.71 m, outward normal 80.6 deg
E_CHAMFER = (7, 8)  # the corner entrance bay, 7.84 m, outward normal 34.4 deg
E_GROVE = (8, 0)    # Grove Street, 57.46 m, outward normal 350.6 deg

# --- the vertical order. Cornice/roof plane 20.3 m is measured twice (2010 city
# LiDAR median 19.77 / majority 20.29, and OSM height=20 independently); the
# balustrade above it is read off the 2008 reference photograph.
H_WATER = 0.50      # granite water table
H_BASE = 5.40       # top of the rusticated ground-floor base
H_STRING0 = 5.40    # string course
H_STRING1 = 5.75
H_BODY = 19.35      # top of the ashlar body = underside of the cornice
H_FRIEZE0 = 18.60   # plain frieze band under the cornice
H_CORN0 = 19.35     # cornice
H_CORN1 = 20.30     # cornice top = the eave line (measured)
H_BAL0 = 20.30      # balustrade bottom rail
H_BAL1 = 20.60
H_BAL2 = 21.05      # balusters run 20.60 -> 21.05
H_CREST = 21.40     # balustrade top rail = the architectural height
H_ROOF = 19.60      # white membrane, sitting inside the cornice frame
H_PENT = 20.85      # corner penthouse top, deliberately below the crest

# Rustication: four proud courses separated by three deeply recessed joints. The
# joints have to be a real 0.18 m step, not a hairline — at the app's camera a
# shallow groove disappears and the base stops reading as rusticated at all.
BASE_COURSES = [(H_WATER, 1.72), (1.90, 3.02), (3.20, 4.32), (4.50, H_BASE)]
BASE_JOINTS = [(1.72, 1.90), (3.02, 3.20), (4.32, 4.50)]

# Window bands, sill to head.
FLOORS = [(1.70, 4.30), (6.60, 9.60), (11.10, 13.90), (15.60, 17.70)]

BEVEL_W = 0.10
BEVEL_SEG = 2

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",
    "Toy_sand": "ece4d4",
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_ink": "3a3530",
    "Toy_navy": "2c4a70",
    "Toy_gold": "caa64a",
    "Toy_white": "f7f4ec",
    "Toy_steel": "9aa0a6",
    "Toy_roofd": "45454a",
    "Toy_gold_Glow": "caa64a",
    "Toy_glassl_Glow": "6f95b8",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def poly_edge(edge):
    """(a, b, length, tangent unit, outward normal) for a CCW footprint edge."""
    a, b = FOOTPRINT[edge[0]], FOOTPRINT[edge[1]]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> this points outward
    return a, b, length, t, n


def edge_len(edge):
    return poly_edge(edge)[2]


def offset_polygon(poly, d):
    """Miter offset of the footprint; positive d moves outward. The light-court
    steps are reflex, but every offset used here is under 1 m against a 3.3 m
    notch, so the miter cannot self-intersect."""
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


# The building's own axes: U runs east along the 80.6 deg Civic Center grid (the
# long axis), W runs north across it. Roof objects are laid out in this frame so
# the composition follows the building rather than true north.
def _axes():
    _, _, _, t_grove, n_grove = poly_edge(E_GROVE)
    return (-t_grove[0], -t_grove[1]), n_grove


U, W = _axes()


def uw(u, w):
    return (U[0] * u + W[0] * w, U[1] * u + W[1] * w)


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


def bevel(obj, width=BEVEL_W, segments=BEVEL_SEG):
    """Miniature-style edge softening on the chunky solids (style bible s.4)."""
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


def prism(name, poly, z0, z1, mat, mat_caps=None):
    """Closed extrusion of a plan polygon (walls + both caps)."""
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


def ring_band(name, z0, z1, off_in, off_out, mat):
    """Closed band following the footprint: 4 loops, quads between."""
    lo_in = offset_polygon(FOOTPRINT, off_in)
    lo_out = offset_polygon(FOOTPRINT, off_out)
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


def quad_box(name, corners, z0, z1, mat):
    """Closed box from four CCW plan corners."""
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


def wall_box(name, edge, s0, s1, z0, z1, d_in, d_out, mat):
    """Box hung on a facade: s along the edge from its first vertex, d measured
    along the outward normal (negative = recessed into the wall)."""
    a, _, _, t, n = poly_edge(edge)

    def p(s, d):
        return (a[0] + t[0] * s + n[0] * d, a[1] + t[1] * s + n[1] * d)

    return quad_box(name, [p(s0, d_in), p(s1, d_in), p(s1, d_out), p(s0, d_out)], z0, z1, mat)


def facade_poly(name, edge, pts_sz, d0, d1, mat):
    """Extrude an arbitrary (s, z) outline drawn on a facade plane outward from
    depth d0 to d1. Used for the entrance archivolt, the oculus and the
    pediments — shapes a box cannot make."""
    a, _, _, t, n = poly_edge(edge)

    def p(s, d):
        return (a[0] + t[0] * s + n[0] * d, a[1] + t[1] * s + n[1] * d)

    npts = len(pts_sz)
    verts = [(*p(s, d0), z) for s, z in pts_sz] + [(*p(s, d1), z) for s, z in pts_sz]
    faces = [(i, (i + 1) % npts, npts + (i + 1) % npts, npts + i) for i in range(npts)]
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def facade_strip(name, edge, pts_in, pts_out, d0, d1, mat):
    """A band on a facade plane between two open polylines, built as a chain of
    convex segment solids. A band like an archivolt must NOT go through
    facade_poly as one concave outline: Blender fans an n-gon from its first
    vertex, and the fan of a C-shape fills its own hole — which silently drew a
    blank slab over the entrance arch, the door and the oculus."""
    objs = []
    for i in range(len(pts_in) - 1):
        objs.append(facade_poly(
            f"{name}_{i}", edge,
            [pts_in[i], pts_in[i + 1], pts_out[i + 1], pts_out[i]], d0, d1, mat))
    return objs


def uw_box(name, u, w, z0, z1, su, sw, mat):
    """Box centred at (u, w) in the building frame, su along U, sw along W."""
    corners = []
    for du, dw in ((-su / 2, -sw / 2), (su / 2, -sw / 2), (su / 2, sw / 2), (-su / 2, sw / 2)):
        corners.append(uw(u + du, w + dw))
    return quad_box(name, corners, z0, z1, mat)


# ------------------------------------------------------------------ facades

# Bay counts per elevation. Grove and Polk carry the enriched second floor; the
# service elevations get the same grid without ornament (dossier 2.4).
BAYS = [
    (E_GROVE, 12, 2.30, True, "grove"),
    (E_POLK, 6, 2.30, True, "polk"),
    (E_SOUTH, 13, 2.10, False, "south"),
    (E_W1, 3, 1.80, False, "westa"),
    (E_W2, 2, 1.80, False, "westb"),
    (E_W3, 2, 1.80, False, "westc"),
]


def window(tag, edge, s_c, width, z0, z1, mats, base=False, mull=False, lit=False):
    """One opening: an ink reveal plate with a glass slab proud of it. The walls
    are solid prisms with no cut openings, so anything at negative depth is
    buried inside the shell and invisible (style bible s.5 — windows are
    graphical elements before they are literal openings). In the rusticated base
    everything is pushed further out so the rustication joints pass BEHIND the
    glass instead of running across it."""
    d_rev = 0.24 if base else 0.04
    dg0, dg1 = (0.23, 0.34) if base else (0.03, 0.11)
    s0, s1 = s_c - width / 2, s_c + width / 2
    wall_box(f"{tag}_reveal", edge, s0, s1, z0, z1, 0.0, d_rev, mats["Toy_ink"])
    wall_box(f"{tag}_glass", edge, s0 + 0.12, s1 - 0.12, z0 + 0.10, z1 - 0.10,
             dg0, dg1, mats["Toy_glass"])
    if mull:
        wall_box(f"{tag}_mv", edge, s_c - 0.05, s_c + 0.05, z0 + 0.10, z1 - 0.10,
                 dg1 - 0.02, dg1 + 0.04, mats["Toy_ink"])
        zm = (z0 + z1) / 2
        wall_box(f"{tag}_mh", edge, s0 + 0.12, s1 - 0.12, zm - 0.05, zm + 0.05,
                 dg1 - 0.02, dg1 + 0.04, mats["Toy_ink"])
    if lit:
        # inset and lifted clear of the pane: coincident faces z-fight, and at
        # 12% day alpha that reads as a triangulated smear
        wall_box(f"{tag}_glow", edge, s0 + 0.20, s1 - 0.20, z0 + 0.18, z1 - 0.18,
                 dg1 + 0.025, dg1 + 0.065, mats["Toy_glassl_Glow"])


def enrich_bay(tag, edge, s_c, width, mats):
    """Second-floor enrichment on the public elevations: a projecting balconette
    with a dark ground and oversized gold rosettes under the sill, and a low
    triangular pediment over the head. The real balconette carries nine rosettes;
    three is what reads from the app's camera (style bible s.26)."""
    s0, s1 = s_c - width / 2 - 0.25, s_c + width / 2 + 0.25
    bevel(wall_box(f"{tag}_balc", edge, s0, s1, 6.10, 6.60, 0.0, 0.30,
                   mats["Toy_navy"]), width=0.05)
    for k, f in enumerate((0.25, 0.5, 0.75)):
        s = s0 + (s1 - s0) * f
        # unbevelled on purpose: a 0.22 m block cannot carry a bevel wide enough
        # to catch light without clamping into degenerate faces
        wall_box(f"{tag}_ros{k}", edge, s - 0.11, s + 0.11, 6.24, 6.46,
                 0.28, 0.38, mats["Toy_gold"])
    peak = s_c
    facade_poly(f"{tag}_ped", edge,
                [(s0 - 0.10, 9.60), (s1 + 0.10, 9.60), (peak, 10.15)],
                0.0, 0.26, mats["Toy_trim"])


def corner_bay(mats):
    """The chamfered north-east corner bay — the whole identity of the building.

    Bottom to top: a round-arched entrance recess ringed by a trim archivolt,
    a gold oculus in the tympanum, a gold door, two lantern sconces on ink
    brackets, then the balconette, then a fully pedimented aedicule around the
    second-floor window."""
    length = edge_len(E_CHAMFER)
    mid = length / 2
    ink, trim, gold = mats["Toy_ink"], mats["Toy_trim"], mats["Toy_gold"]

    # Everything here is built PROUD of the wall in a strict depth order, and
    # the whole group clears 0.22 m — the rusticated base courses stand 0.20 m
    # out, so anything shallower is buried behind them and the arch fills with
    # course lines instead of shadow. The wall itself is a solid prism with no
    # cut opening, so a plate authored at depth 0 is coplanar with it and
    # z-fights into a shimmering mess. Both cost a review round.
    r_in, r_out = 2.35, 2.95
    springing = 2.35
    seg = 10
    inner = [(mid - r_in, 0.0), (mid - r_in, springing)]
    inner += [(mid - r_in * math.cos(math.pi * i / seg),
               springing + r_in * math.sin(math.pi * i / seg)) for i in range(1, seg)]
    inner += [(mid + r_in, springing), (mid + r_in, 0.0)]

    # archivolt: the band between the two arcs, one convex solid per segment
    outer = [(mid - r_out, 0.0), (mid - r_out, springing)]
    outer += [(mid - r_out * math.cos(math.pi * i / seg),
               springing + r_out * math.sin(math.pi * i / seg)) for i in range(1, seg)]
    outer += [(mid + r_out, springing), (mid + r_out, 0.0)]
    facade_strip("corner_archivolt", E_CHAMFER, inner, outer, 0.22, 0.50, trim)

    # the dark arched field inside it, standing clear of the wall
    facade_poly("corner_recess", E_CHAMFER, inner, 0.23, 0.31, ink)

    # tympanum ornament reduced to one strong disc: the oculus (style bible s.26)
    disc = [(mid + 0.60 * math.cos(2 * math.pi * i / 14),
             4.05 + 0.60 * math.sin(2 * math.pi * i / 14)) for i in range(14)]
    facade_poly("corner_oculus", E_CHAMFER, disc, 0.32, 0.52, gold)
    facade_poly("corner_oculus_glow", E_CHAMFER,
                [(mid + 0.48 * math.cos(2 * math.pi * i / 14),
                  4.05 + 0.48 * math.sin(2 * math.pi * i / 14)) for i in range(14)],
                0.525, 0.565, mats["Toy_gold_Glow"])

    # door and its lit transom
    bevel(wall_box("corner_door", E_CHAMFER, mid - 1.15, mid + 1.15, 0.0, 2.50,
                   0.32, 0.52, gold), width=0.05)
    wall_box("corner_transom", E_CHAMFER, mid - 1.32, mid + 1.32, 2.56, 3.06,
             0.32, 0.46, ink)
    wall_box("corner_transom_glow", E_CHAMFER, mid - 1.24, mid + 1.24, 2.64, 2.98,
             0.465, 0.505, mats["Toy_gold_Glow"])

    # lantern sconces, ~1.7x true size so they survive the camera (style bible s.9)
    for k, off in ((0, -3.05), (1, 3.05)):
        s = mid + off
        wall_box(f"corner_bracket{k}", E_CHAMFER, s - 0.10, s + 0.10, 2.30, 3.30,
                 0.0, 0.54, ink)
        bevel(wall_box(f"corner_lantern{k}", E_CHAMFER, s - 0.26, s + 0.26,
                       2.32, 3.16, 0.50, 1.02, gold), width=0.05)
        wall_box(f"corner_lantern{k}_glow", E_CHAMFER, s - 0.19, s + 0.19,
                 2.42, 3.06, 1.03, 1.07, mats["Toy_gold_Glow"])

    # second-floor aedicule: pilaster strips either side of the enriched window
    for k, off in ((0, -2.05), (1, 2.05)):
        s = mid + off
        bevel(wall_box(f"corner_pil{k}", E_CHAMFER, s - 0.30, s + 0.30, 5.75, 9.70,
                       0.0, 0.24, trim), width=0.05)


# --------------------------------------------------------------- the build


def materials():
    mats = {}
    for name, rgb in PALETTE.items():
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        bsdf = m.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.85
        bsdf.inputs["Metallic"].default_value = 0.0
        if name.endswith("_Glow"):
            bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 0.0
        mats[name] = m
    return mats


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    mats = materials()

    stone = mats["Toy_stone"]
    sand = mats["Toy_sand"]
    trim = mats["Toy_trim"]
    ink = mats["Toy_ink"]
    white = mats["Toy_white"]
    steel = mats["Toy_steel"]
    roofd = mats["Toy_roofd"]
    glassl = mats["Toy_glassl"]

    # ---- 1. ashlar body -------------------------------------------------- #
    bevel(prism("body", FOOTPRINT, 0.0, H_BODY, stone), width=0.12)

    # ---- 2. rusticated base: three proud courses, two recessed joints ----- #
    bevel(ring_band("water_table", 0.0, H_WATER, -0.20, 0.22, trim), width=0.06)
    for i, (z0, z1) in enumerate(BASE_COURSES):
        bevel(ring_band(f"rustic_{i}", z0, z1, -0.20, 0.20, sand), width=0.05)
    for i, (z0, z1) in enumerate(BASE_JOINTS):
        ring_band(f"rustic_joint_{i}", z0, z1, -0.20, 0.02, sand)

    # ---- 3. string course, frieze, cornice -------------------------------- #
    bevel(ring_band("string_course", H_STRING0, H_STRING1, -0.20, 0.18, trim),
          width=0.06)
    ring_band("frieze", H_FRIEZE0, H_CORN0, -0.20, 0.06, trim)
    bevel(ring_band("cornice", H_CORN0, H_CORN1, -0.20, 0.95, trim), width=0.08)

    # ---- 4. balustrade ---------------------------------------------------- #
    # One continuous line at the crest. Grove, the chamfer and Polk carry open
    # balusters; the service elevations get a solid infill panel instead, which
    # is both how the building reads and half the triangles.
    bevel(ring_band("bal_rail_lo", H_BAL0, H_BAL1, -0.20, 0.55, trim), width=0.06)
    bevel(ring_band("bal_rail_hi", H_BAL2, H_CREST, -0.20, 0.55, trim), width=0.06)
    for edge, tag in ((E_GROVE, "grove"), (E_CHAMFER, "chamfer"), (E_POLK, "polk")):
        length = edge_len(edge)
        count = max(2, int(round(length / 1.15)))
        pitch = length / count
        for i in range(count):
            s = (i + 0.5) * pitch
            # unbevelled: a 0.16 m baluster clamps to degenerate faces
            wall_box(f"bal_{tag}_{i}", edge, s - 0.08, s + 0.08, H_BAL1, H_BAL2,
                     0.10, 0.36, trim)
    for edge, tag in ((E_SOUTH, "south"), (E_W1, "w1"), (E_STEP1, "s1"),
                      (E_W2, "w2"), (E_STEP2, "s2"), (E_W3, "w3")):
        length = edge_len(edge)
        wall_box(f"parapet_{tag}", edge, -0.12, length + 0.12, H_BAL1, H_BAL2,
                 0.10, 0.36, trim)

    # ---- 5. window grid --------------------------------------------------- #
    for edge, count, width, public, tag in BAYS:
        length = edge_len(edge)
        pitch = length / count
        for i in range(count):
            s_c = (i + 0.5) * pitch
            for f, (z0, z1) in enumerate(FLOORS):
                # deterministic scatter, never a full grid (style bible s.19)
                lit = public and ((i * 7 + f * 3) % 5 == 0)
                window(f"{tag}_{i}_{f}", edge, s_c, width, z0, z1, mats,
                       base=(f == 0), mull=(public and f == 1), lit=lit)
            if public:
                enrich_bay(f"{tag}_{i}", edge, s_c, width, mats)

    # ---- 6. the corner bay ------------------------------------------------ #
    length = edge_len(E_CHAMFER)
    mid = length / 2
    for f, (z0, z1) in enumerate(FLOORS[1:], start=1):
        window(f"chamfer_{f}", E_CHAMFER, mid, 2.90, z0, z1, mats,
               mull=(f == 1), lit=(f == 2))
    # the corner's balconette and pediment span the full aedicule, not just the
    # window — this is the grand bay, and it has to read as grander
    enrich_bay("chamfer", E_CHAMFER, mid, 4.20, mats)
    corner_bay(mats)

    # ---- 7. the roof: a brilliant white membrane in a trim frame ---------- #
    bevel(prism("roof", offset_polygon(FOOTPRINT, -0.05), H_BODY, H_ROOF, white),
          width=0.05)

    # Light court, south of centre. Kept in the mid greys rather than the near
    # blacks: a Toy_roofd field this large reads as a hole punched in the roof
    # from the app's camera, which is not what is there.
    bevel(uw_box("court_kerb", -2.0, -9.0, H_ROOF, H_ROOF + 0.16, 19.0, 10.0, steel),
          width=0.05)
    uw_box("court_pad", -2.0, -9.0, H_ROOF + 0.10, H_ROOF + 0.18, 17.4, 8.4, roofd)
    for i, u in enumerate((-8.0, -2.0, 4.0)):
        bevel(uw_box(f"court_plant_{i}", u, -9.0, H_ROOF + 0.14, H_ROOF + 0.92,
                     4.4, 2.6, steel), width=0.07)

    # Corner penthouse, following the chamfer plan and stopping below the crest.
    # Toy_stone, not Toy_trim: trim on the white membrane is the same value and
    # the whole object vanishes from above.
    bevel(wall_box("penthouse", E_CHAMFER, -1.0, length + 1.0, H_ROOF, H_PENT,
                   -9.2, -0.6, stone), width=0.08)
    bevel(wall_box("penthouse_curb", E_CHAMFER, 1.4, length - 1.4, H_PENT,
                   H_PENT + 0.30, -6.8, -2.4, roofd), width=0.05)
    wall_box("penthouse_sky", E_CHAMFER, 1.7, length - 1.7, H_PENT + 0.24,
             H_PENT + 0.40, -6.5, -2.7, glassl)

    # Mechanical cluster on the west third: tight clusters, never a scatter
    # (style bible s.10) — and the roof still needs enough on it to stop being a
    # blank plane at the one camera angle that sees the most of it.
    bevel(uw_box("mech_curb", -22.0, 2.0, H_ROOF, H_ROOF + 0.18, 12.5, 4.6, roofd),
          width=0.05)
    for i, u in enumerate((-26.0, -22.0, -18.0)):
        bevel(uw_box(f"mech_{i}", u, 2.0, H_ROOF + 0.14, H_ROOF + 1.25, 2.6, 3.2,
                     roofd), width=0.08)
    for i, w in enumerate((8.4, 11.4)):
        bevel(uw_box(f"duct_{i}", -19.0, w, H_ROOF + 0.06, H_ROOF + 0.60, 12.0, 0.9,
                     steel), width=0.05)
    bevel(uw_box("riser", -12.4, 11.4, H_ROOF + 0.06, H_ROOF + 1.40, 1.2, 1.2, steel),
          width=0.06)
    for i, (u, w) in enumerate(((-14.5, 2.0), (-14.5, 11.4), (10.0, -9.0))):
        bevel(uw_box(f"hatch_{i}", u, w, H_ROOF, H_ROOF + 0.50, 2.2, 1.7, steel),
              width=0.06)
    # A short maintenance walk tying the plant cluster to the light court. Kept
    # short on purpose: a full-length ribbon reads as a slash across the roof.
    uw_box("walk_a", -10.5, 2.0, H_ROOF, H_ROOF + 0.06, 13.0, 1.4, steel)
    uw_box("walk_b", -4.5, -4.0, H_ROOF, H_ROOF + 0.06, 1.4, 11.0, steel)

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
        o.evaluated_get(dg).to_mesh_clear()
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print("[build] anchor lon/lat: -122.4186747 37.7781359 (footprint AABB centre)")
    print("[build] long axis 80.6 deg true; Grove front normal 350.6 deg; "
          "corner bay normal 34.4 deg true")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "101-grove.blend")
    glb = os.path.join(out, "101-grove.glb")
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
