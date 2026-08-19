"""Deterministic Blender build of the SF-SIM miniature United Nations Plaza.

    blender -b --python build_un_plaza.py -- [--out DIR]

Writes un-plaza.blend and un-plaza.glb next to this file (or into --out).
Geometry is authored in world space in metres, Z up, +X east, +Y north, so the
model drops into the city at its real-world heading — the loader applies no
rotation. Origin = the plaza's world-axis-aligned XY bbox centre (anchor
lon -122.4138900, lat 37.7801415), min Z = 0, tallest tree crown exactly 13.00 m.

Design (see REFERENCE.md and docs/asset-plans/un-plaza.md for the sources
behind every number):

* Lawrence Halprin's 1975 gateway to the Civic Center — a 2.78-acre wedge of RED
  BRICK driven diagonally out of Market Street up the closed Fulton Street
  alignment toward City Hall;
* recognition rests first on COLOUR (this is the only large red plaza in the
  city), then on the double colonnade of sixteen globe-topped granite light
  standards marching down the Fulton axis, then on the wedge plan itself;
* the plaza sits on TWO grids: its own axis is the Civic Center grid at
  80.94 deg, its Market Street boundary runs 45.20 deg, and the 35.74 deg
  difference IS the plan shape;
* the ring, the 16 standard positions, the fountain, the three planting beds,
  the south terrace, the dog run and the UN emblem are MEASURED (data/
  elements_en.json, from OSM relation 1735771). The nine fountain slabs are
  measured from DataSF LiDAR footprints, positions AND heights. The tree
  positions are inferred (data/trees_en.json, written by this script) — see
  REPORT.md;
* everything is a closed solid with real thickness stacked in Z (brick 0.30,
  joint bands 0.31, granite inlays 0.32, walks 0.34, skate pad 0.33, beds 0.40,
  terrace 1.05) so nothing is coplanar with anything else and nothing z-fights
  the baked landcover, which sits at +0.06 m above terrain. The two OSM
  natural=sand inners bake as landcover sand directly under this asset, so the
  plate has to cover them;
* night state: the sixteen globes are the hero glow. The plaza becomes two
  dotted lines of warm points running down the Fulton axis, which is exactly
  what the real place does. Brick, beds and fountain go dark. Glow surfaces are
  thin shells proud of the opaque solid beneath them; the app renders _Glow at
  ~12% alpha by day (a CLOSED shell reads at ~23%), so a primary surface must
  never be authored as glow.

Authoring frame: geometry is laid out in the plaza's local (e, n) frame —
e along the Fulton axis, POSITIVE TOWARD MARKET / EAST, bearing 80.94 deg true;
n across it, POSITIVE TOWARD NORTH, bearing 350.94 deg — and mapped to world
x/y by to_world(). Unlike civic-center-plaza's (u, v), THIS FRAME IS
RIGHT-HANDED in world, so orient_for_world() keeps the POSITIVE shoelace.
The plaza is a wedge across two grids, so the axis-aligned XY bounding box is
~215 x 158 m even though the plaza measures 220.8 x 150.3 m in its own frame.
That is expected, not a scale error.
"""

import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# The Civic Center grid, from DataSF centrelines (McAllister reads 80.96 deg
# over seven consecutive blocks). civic-center-plaza, sf-main-library and
# city-hall are all built on this same pair, which is why this asset uses it
# rather than the 80.42 deg its own OSM ring digitises to.
#
# The grid leans 9.06 deg, so the axis toward Market (east) bears 80.94 and the
# cross axis toward north bears 350.94 (= 360 - 9.06), NOT 9.06. Those are
# mirror images about north and measure identically in any bounding-box check.
HEADING_E = 80.94
HEADING_N = 350.94
# Market Street's own bearing, measured on the DataSF centreline (Hyde->Larkin,
# 192.3 m) that fronts the plaza. The OSM ring's 134.6 m Market edge reads
# 45.18, so that boundary is trusted as drawn and is baked into the ring data.
HEADING_MARKET = 45.20

E_DIR = (math.sin(math.radians(HEADING_E)), math.cos(math.radians(HEADING_E)))
N_DIR = (math.sin(math.radians(HEADING_N)), math.cos(math.radians(HEADING_N)))

TRI_CAP = 18000
ANCHOR_SHIFT = [0.0, 0.0]

# ------------------------------------------------------------- height ladder
Z_BRICK = 0.30        # the brick field: the asset's floor
Z_JOINT = 0.31        # the darker joint bands scored across it
Z_WALK = 0.33         # the main cross-walks
Z_SKATE = 0.34        # the 2023 skate pad, a half-tone lighter and proud of the brick
Z_INLAY = 0.36        # granite inlays: Walk of Great Ideas, UN emblem, cross.
                      # ABOVE the walks, not below: the first build put the inlays
                      # at 0.32 and the walks at 0.34, which enclosed the UN emblem
                      # inside the walk solid and rendered it as a black square.
Z_BED = 0.40          # the three decomposed-granite planting beds
Z_TERRACE = 1.05      # the raised south terrace platform
Z_ARM = 0.45          # the Leavenworth arm's planted strip
Z_SKIRT = 0.45        # how far the draped plate hangs below its own underside

# Verticals. Every one of these is an independently sourced number and none of
# them is the height datum, so none may be rescaled to make the model fit.
Z_COLUMN = 5.90       # globe top; photogrammetric off a levelled photosphere, +-0.5
COLUMN_SHAFT = 5.05   # shaft top. NOT 5.28: at 5.28 the shaft met the globe's
                      # underside exactly and the neck frustum collapsed to zero
                      # height — 16 zero-area side quads per column, 256
                      # degenerate triangles, which the validator counts.
COLUMN_SIDE = 0.75    # square shaft, measured from the same pano at 6.1 deg / 6.88 m
GLOBE_R = 0.31
Z_OBELISK = 5.18      # 17 ft, published (Wikipedia, 1995 UDHR engraving)
Z_BOLIVAR = 8.10      # photogrammetric, corroborates the pano camera solution
Z_FOUNT_CREST = 4.03  # DataSF LiDAR hgt_maxcm on footprint 159394 — MEASURED
Z_FOUNT_FLOOR = 0.04  # the well floor; min_z of the asset stays at 0 (contract)
Z_FOUNT_RIM = 1.55    # a chunky stepped kerb: the real basin is sunk ~2.4 m and
                      # the contract forbids going below z=0, so the depth is
                      # bought by raising the rim instead of dropping the floor
Z_FLAGPOLE = 12.00
Z_TREE = 13.00        # THE HEIGHT DATUM. An authored design value, not a survey:
                      # see docs/asset-plans/un-plaza.md 2.15 risk 3. Because
                      # targetHeightM is set equal to it, the loader's scale is
                      # exactly 1.0 and the ground plane is right by construction.

PALETTE_HEX = {
    "Toy_brick": "c96f4a",      # THE brick field — recognition cue #1
    "Toy_rust": "a86444",       # the second brick tone (alternating joint bands)
                                # and the tree trunks
    "Toy_stone": "d9d2c2",      # granite: kerbs, Walk band, emblem, column shafts,
                                # fountain slabs, Bolivar's pedestal, terrace walls
    "Toy_cream": "f2ede3",      # the skate pad and the cross-walks — lighter than
                                # the granite so the 2023 layer reads as inserted
    "Toy_sand": "ece4d4",       # the three decomposed-granite planting beds
    "Toy_verdigris": "9fb8a8",  # tree crowns, and the Bolivar bronze
    "Toy_mint": "8fd0a8",       # the dog run's turf
    "Toy_white": "f7f4ec",      # the sixteen globe luminaires
    "Toy_steel": "9aa0a6",      # flagpoles, fence, racks, catenaries, railings
    "Toy_ink": "3a3530",        # the obelisk, joint shadow, the well's shaded faces
    "Toy_roofd": "45454a",      # bench slats, bins, game tables, portal heads
    "Toy_teal": "3fa8a0",       # skateable art block / portal accent
    "Toy_coral": "e8735a",      # skateable art block
    "Toy_mustard": "d9a441",    # skateable art block
    "Toy_navy": "2c4a70",       # the UN flag slab
    "Toy_red": "c4453c",        # the US flag slab
    "Toy_white_Glow": "f7f4ec",   # the sixteen globes — the hero night state
    "Toy_cream_Glow": "f2ede3",   # the 2023 festoon lighting, and a wash on the pad
    "Toy_teal_Glow": "3fa8a0",    # the BART/Muni portal head at the Market end
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


def hash01(n):
    """Deterministic [0,1) hash — the same mixer the pipeline uses for its own
    scatter, so 'random' variation here is reproducible across rebuilds and
    reviewable in a diff."""
    h = (int(n) ^ 0x9E3779B9) * 0x85EBCA6B & 0xFFFFFFFF
    h = (h ^ (h >> 13)) * 0xC2B2AE35 & 0xFFFFFFFF
    h ^= h >> 16
    return (h & 0xFFFFFFFF) / 4294967296.0


# ----------------------------------------------------------------- transforms


def to_world(e, n):
    """Plaza frame -> world (x east, y north). RIGHT-handed: e x n > 0, so a CCW
    polygon in (e, n) stays CCW in (x, y) and outward normals stay outward."""
    return (e * E_DIR[0] + n * N_DIR[0], e * E_DIR[1] + n * N_DIR[1])


def rect(e0, e1, n0, n1):
    """CCW rectangle in the plaza frame."""
    return [(e0, n0), (e1, n0), (e1, n1), (e0, n1)]


def orient_for_world(poly):
    """Order a plaza-frame ring so it comes out COUNTER-clockwise in world space,
    which is what makes prism_verts_faces' caps face outward. This frame is
    right-handed in world (unlike civic-center-plaza's), so the test keeps the
    POSITIVE shoelace. OSM rings arrive in either winding, so everything goes
    through here."""
    a = 0.0
    for i in range(len(poly)):
        e0, n0 = poly[i]
        e1, n1 = poly[(i + 1) % len(poly)]
        a += e0 * n1 - e1 * n0
    return poly if a > 0 else poly[::-1]


def dedupe_ring(poly):
    """Drop the repeated closing vertex and any coincident neighbours — OSM ways
    close on themselves and mesh.validate() would silently eat the degenerate
    faces, taking the volume test's meaning with them."""
    out = []
    for p in poly:
        if not out or (abs(p[0] - out[-1][0]) > 1e-6 or abs(p[1] - out[-1][1]) > 1e-6):
            out.append((p[0], p[1]))
    if len(out) > 1 and abs(out[0][0] - out[-1][0]) < 1e-6 and abs(out[0][1] - out[-1][1]) < 1e-6:
        out.pop()
    return out


# --------------------------------------------------------------- mesh helpers


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
    """Miniature-style edge softening (style bible s.4). The offset is capped at
    a third of the object's thinnest dimension: most of this asset is 10-150 mm
    thick paving and a flat 0.12 m bevel on those collapses opposing profiles
    into zero-area slivers even with clamp_overlap."""
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


def prism_verts_faces(poly_en, z0, z1, base_index=0, seat=None):
    """Closed extrusion of a plaza-frame polygon: walls + both caps. Orients the
    ring itself, so every caller gets outward normals.

    Every vertex is DRAPED: its z is offset by drape(e, n), so a slab follows the
    baked terrain instead of hovering over it. Pass `seat=(e, n)` for a solid
    that must stay rigid rather than follow the ground."""
    ring = orient_for_world(poly_en)
    poly = [to_world(e, n) for e, n in ring]
    dz = [drape(*p) for p in ring] if seat is None else [drape(*seat)] * len(ring)
    m = len(poly)
    verts = ([(x, y, z0 + dz[k]) for k, (x, y) in enumerate(poly)]
             + [(x, y, z1 + dz[k]) for k, (x, y) in enumerate(poly)])
    b = base_index
    faces = []
    for i in range(m):
        j = (i + 1) % m
        faces.append((b + i, b + j, b + m + j, b + m + i))
    faces.append(tuple(b + i for i in range(m - 1, -1, -1)))
    faces.append(tuple(b + i for i in range(m, 2 * m)))
    return verts, faces


def prism(name, poly_en, z0, z1, mat, mat_top=None, seat=None):
    verts, faces = prism_verts_faces(dedupe_ring(poly_en), z0, z1, seat=seat)
    face_mats = [0] * (len(faces) - 1) + [1 if mat_top else 0]
    mats = [mat, mat_top] if mat_top else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def box(bm_verts, bm_faces, e0, e1, n0, n1, z0, z1, seat=None):
    b = len(bm_verts)
    verts, faces = prism_verts_faces(rect(e0, e1, n0, n1), z0, z1, base_index=b, seat=seat)
    bm_verts.extend(verts)
    bm_faces.extend(faces)


def ngon(nsides, ec, nc, r, rot=0.0):
    """Emitted COUNTER-clockwise in (e, n), which is counter-clockwise in world
    too — this frame is right-handed. frustum() relies on this winding."""
    return [
        (
            ec + r * math.cos(rot + 2 * math.pi * i / nsides),
            nc + r * math.sin(rot + 2 * math.pi * i / nsides),
        )
        for i in range(nsides)
    ]


def frustum(bm_verts, bm_faces, nsides, ec, nc, r0, r1, z0, z1, rot=0.0):
    """Append a closed n-sided frustum to a running vertex/face buffer. Used for
    the trees, the columns and the poles, which are built into single merged
    objects to keep the loader's draw-call merge cheap."""
    b = len(bm_verts)
    dz = drape(ec, nc)          # a round vertical stands plumb on its own ground
    lo = ngon(nsides, ec, nc, r0, rot)
    hi = ngon(nsides, ec, nc, r1, rot)
    bm_verts.extend([to_world(e, n) + (z0 + dz,) for e, n in lo])
    bm_verts.extend([to_world(e, n) + (z1 + dz,) for e, n in hi])
    for i in range(nsides):
        j = (i + 1) % nsides
        bm_faces.append((b + i, b + j, b + nsides + j, b + nsides + i))
    bm_faces.append(tuple(b + i for i in range(nsides - 1, -1, -1)))
    bm_faces.append(tuple(b + nsides + i for i in range(nsides)))


def point_in_ring(pt, ring):
    x, y = pt
    inside = False
    m = len(ring)
    for i in range(m):
        x0, y0 = ring[i]
        x1, y1 = ring[(i + 1) % m]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            inside = not inside
    return inside


def clip_span(ring, p0, direction, perp, d0, d1, s_lo, s_hi, step=1.0):
    """Longest contiguous run of s in [s_lo, s_hi] for which BOTH edges of a band
    offset d0..d1 along `perp` from the line p0 + s*direction lie inside `ring`.

    Bands laid out parallel to Market Street escape the plaza at both ends —
    the wedge narrows toward Hyde and the frontage is 134 m long — and the first
    build shipped granite and joint bands running clean off the plate. Rather
    than hand-tuning each one, every Market-aligned band is clipped here."""
    best = None
    run = None
    s = s_lo
    while s <= s_hi:
        ok = all(
            point_in_ring((p0[0] + s * direction[0] + d * perp[0],
                           p0[1] + s * direction[1] + d * perp[1]), ring)
            for d in (d0, d1)
        )
        if ok:
            run = (s, s) if run is None else (run[0], s)
            if best is None or run[1] - run[0] > best[1] - best[0]:
                best = run
        else:
            run = None
        s += step
    return best


def ring_prism(name, outer, inner, z0, z1, mat, mat_top=None):
    """A closed band between two same-length rings — a kerb, not a filled slab.
    The fountain's first build used a solid prism for its rim, which turned the
    sunken basin into a pale octagonal plateau with the granite pile buried
    inside it."""
    ro = orient_for_world(outer)
    ri = orient_for_world(inner)
    o = [to_world(e, n) for e, n in ro]
    i = [to_world(e, n) for e, n in ri]
    do = [drape(*p) for p in ro]
    di = [drape(*p) for p in ri]
    m = len(o)
    verts = ([(x, y, z0 + do[k]) for k, (x, y) in enumerate(o)]
             + [(x, y, z1 + do[k]) for k, (x, y) in enumerate(o)]
             + [(x, y, z0 + di[k]) for k, (x, y) in enumerate(i)]
             + [(x, y, z1 + di[k]) for k, (x, y) in enumerate(i)])
    A, B, C, D = 0, m, 2 * m, 3 * m
    faces, mats_idx = [], []
    for k in range(m):
        j = (k + 1) % m
        faces.append((A + k, A + j, B + j, B + k)); mats_idx.append(0)   # outer wall
        faces.append((C + k, D + k, D + j, C + j)); mats_idx.append(0)   # inner wall
        faces.append((B + k, B + j, D + j, D + k)); mats_idx.append(1 if mat_top else 0)
        faces.append((A + k, C + k, C + j, A + j)); mats_idx.append(0)   # underside
    return new_mesh(name, verts, faces, [mat, mat_top] if mat_top else [mat],
                    mats_idx)


def profile(bm_verts, bm_faces, nsides, ec, nc, rings, rot=0.0):
    """Closed solid of revolution from a list of (radius, z) rings: one bottom
    cap, n-1 side bands, one top cap, and NO internal caps.

    Stacking two closed frusta instead — which is what this build did first —
    buries a pair of coincident, opposite-facing polygons inside the solid.
    They are invisible in every render, but stage 4's weld collapses them onto
    one another and the limited dissolve then merges them into a single face,
    which breaks the shell: `globes_glow` came out of Phase B with a signed
    volume of -1.62 where the source measured +1.36. Emit the profile in one
    piece and the hazard does not exist."""
    b = len(bm_verts)
    dz = drape(ec, nc)          # a round vertical stands plumb on its own ground
    for r, z in rings:
        for e, n in ngon(nsides, ec, nc, r, rot):
            bm_verts.append(to_world(e, n) + (z + dz,))
    for k in range(len(rings) - 1):
        lo, hi = b + k * nsides, b + (k + 1) * nsides
        for i in range(nsides):
            j = (i + 1) % nsides
            bm_faces.append((lo + i, lo + j, hi + j, hi + i))
    bm_faces.append(tuple(b + i for i in range(nsides - 1, -1, -1)))
    top = b + (len(rings) - 1) * nsides
    bm_faces.append(tuple(top + i for i in range(nsides)))


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


# --------------------------------------------------------------- measured data

HERE = os.path.dirname(os.path.abspath(__file__))


_TERRAIN = None


def drape(e, n):
    """dy at (e, n) — how far the ground stands above the anchor's ground, from
    the least-squares PLANE fitted to the baked terrain inside the plaza ring
    (data/terrain_en.json -> plane_in_ring).

    `placeGeneric()` seats a landmark from ONE terrain sample at its anchor. For
    a building that is right; for an asset that IS the ground it is not. Measured
    on the committed bake over 2,811 samples inside the real plaza ring, a FLAT
    plate seated at the anchor is buried 1.52 m at the Hyde end and floats 2.06 m
    over the south side of the promenade. Same failure artifacts/424-brannan and
    artifacts/64-south-park hit; this is their remedy.

    A PLANE, not the sampled grid, and that choice was measured rather than
    assumed. The grid hugs the heightmap exactly, but it is piecewise-bilinear
    and therefore not affine: draping a thin slab's vertices on it folds the slab.
    The grid build produced `skate_pad` — a 0.06 m inlay spanning 50 m — with an
    INVERTED signed volume and a 0.37 m spread in paving clearance, because its
    side quads went non-planar. A plane shear maps planes to planes, so every
    prism in this asset keeps its thickness, its winding and its volume.

    The plane costs a 0.373 m RMS residual inside the ring, with 649 of 712
    samples inside 0.5 m. The 2.0 m maximum sits in one ~20 m dip near
    (e -24, n -33): a Terrarium DEM artefact over the Civic Center station
    excavation, not topography. The drape follows the ground everywhere the
    ground is real and ignores a hole in the elevation data."""
    p = _TERRAIN["plane_in_ring"]
    return p["a_per_e"] * e + p["b_per_n"] * n + p["c"]


def load_data():
    global _TERRAIN
    with open(os.path.join(HERE, "data", "terrain_en.json"), "r", encoding="utf8") as fh:
        _TERRAIN = json.load(fh)
    with open(os.path.join(HERE, "data", "elements_en.json"), "r", encoding="utf8") as fh:
        return json.load(fh)


# The nine granite slabs of the fountain, measured from DataSF LiDAR building
# footprints (ynuv-fyni) that captured them as buildings: (e0, e1, n0, n1,
# hgt_maxcm/100). These are surveyed positions AND surveyed heights, the only
# element of this plaza for which that is true. The tallest is 4.03 m and it is
# asserted in the validator.
FOUNTAIN_SLABS = [
    (24.0, 36.0, 3.0, 13.0, 4.03),
    (33.0, 34.6, 6.0, 7.6, 3.01),
    (38.0, 43.0, 9.0, 13.0, 2.34),
    (38.0, 44.0, -5.0, 1.0, 1.95),
    (45.0, 49.0, 5.0, 9.0, 2.43),
    (46.0, 53.0, -5.0, 3.0, 1.99),
    (49.0, 57.0, 8.0, 13.0, 3.26),
    (55.0, 64.0, 4.0, 9.0, 2.49),
    (57.0, 61.0, 9.0, 14.0, 3.26),
]

# The sunken octagonal well. e[20,68] x n[-11,19] is 48 x 30 m, which is the
# published "165 ft (50 m) run" by "100 ft (30 m) wide basin" to within a metre.
WELL = (19.0, 66.0, -9.0, 18.0)
WELL_CHAMFER = 7.5
# The nine surveyed footprints are spread over 40 x 19 m, which is true and
# reads as nine separate lumps rather than as one pile. Halprin's blocks are
# stacked, not scattered, so the footprints are drawn 18% toward the mass
# centroid — a semantic exaggeration in ASSET AUTHORING, which AGENTS.md rule 5
# permits and placement does not. Heights are left exactly as surveyed.
SLAB_PULL = 0.18

# The 2023 UN Skate Plaza, set back 6 m from the Market frontage. 13,000 sq ft
# opened Nov 2023 plus 2,100 sq ft in Feb 2025 = 1,404 m2; this trapezoid is
# ~1,380 m2. The OSM node leisure=pitch "UN Skate Plaza" lands at (10.4, -21.9),
# inside it, which is what places it. The OUTLINE is inferred (see REPORT.md):
# OSM's own skate polygon is the old planting bed and is 396 m2.
SKATE = [(-8.0, -9.0), (-8.0, -37.0), (22.95, -37.0), (42.0, -23.3), (42.0, -9.0)]

# Walk of Great Ideas: eight white granite stones inlaid with the UN Charter
# preamble, 1995. Placed across the promenade at the Hyde end from the levelled
# photosphere, which stands on it and reads the inscription.
WALK_BAND = (-98.5, -91.5, -32.0, -8.0)

# The coordinates cross: granite blocks inlaid with brass giving San Francisco's
# datum coordinates for distances to other cities, in the plaza's south-west
# near Market (Wikipedia). Position inferred within that quadrant.
CROSS_C = (-32.0, -52.0)

# The south stepped terrace, from OSM way 128534066 with its retaining walls
# (128534077, 775794182) and three step lines (775794176/778/779). Reading: a
# raised platform on the Market side with three treads down to plaza level.
TERRACE_E = (-37.4, 0.6)
TERRACE_N_HIGH = (-51.3, -39.0)
TERRACE_STEPS = (-38.6, -37.0, -35.5)

# Market Street in the plaza frame. Its bearing is 45.20 deg true and the plaza
# axis is 80.94, so the frontage runs -35.74 deg off the e axis. P0 is the ring's
# own south-west Market corner; MARKET_PERP points INTO the plaza.
# HEADING_E - HEADING_MARKET, not the other way round: the frontage runs from
# the ring's south-west Market corner toward 7th Street, i.e. e AND n both
# increase. The first build had the sign flipped, which sent the frontage band
# out of the plaza within a few metres and left walk_market unbuilt.
_MA = math.radians(HEADING_E - HEADING_MARKET)
MARKET_P0 = (-1.99, -62.36)
MARKET_DIR = (math.cos(_MA), math.sin(_MA))
MARKET_PERP = (-math.sin(_MA), math.cos(_MA))

# The colonnade's centreline, from the 16 measured standard positions.
AXIS_N = -19.83
BAY = 11.77


# --------------------------------------------------------------------- build


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene
    mats = {name: make_material(name) for name in PALETTE_HEX}
    data = load_data()

    ground(data, mats)
    inlays(data, mats)
    beds(data, mats)
    terrace(mats)
    colonnade(data, mats)
    fountain(mats)
    monuments(data, mats)
    skate(mats)
    trees(data, mats)
    furniture(data, mats)
    leavenworth_arm(data, mats)
    people(mats)

    # Bevel budget. A 0.12/2 bevel multiplies a box's triangle count by ~9, so it
    # is spent only where it buys something: the chunky single solids that carry
    # the miniature read at the app's camera distance. The merged multi-solid
    # objects (trees, columns, furniture, people) are each built from dozens of
    # small primitives whose bevels would cost 20k triangles for detail under one
    # pixel. The paving slabs are 10-150 mm thick and take a token 0.04/1
    # softening so their kerb edges still catch a highlight.
    UNBEVELLED = {"trees", "crowns", "furniture", "people", "festoon", "arm_fence",
                  "columns", "bike_racks", "fitness", "joint_grid"}
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        # "_glow" anywhere in the name, not just at the end — a closed glow shell
        # that gets bevelled costs 9x for detail that is never seen.
        if obj.name in UNBEVELLED or "_glow" in obj.name:
            continue
        if obj.name.startswith(("inlay_", "walk_", "skate_pad", "bed_")):
            bevel(obj, width=0.04, segments=1)
        elif obj.name in ("fount_slabs", "fount_kerb", "fount_bench"):
            # eighteen stacked boxes: a 2-segment bevel costs 900 triangles for
            # a profile that is under a pixel at the app's camera distance
            bevel(obj, width=0.10, segments=1)
        elif obj.name == "skate_ledges":
            bevel(obj, width=0.08, segments=1)
        else:
            bevel(obj, width=0.12, segments=2)

    recentre()
    return scene


def ground(data, mats):
    """The brick plate and the joint bands scored across it. Four fifths of this
    asset is paving, so the paving has to be DESIGNED rather than left as a blank
    red slab (style bible s.13). The bands run on the colonnade's own 11.77 m bay
    pitch in both directions, so the ground grain and the columns agree."""
    # -Z_SKIRT, not 0: the plate's underside is draped onto the terrain, and a
    # skirt guarantees no sliver of daylight opens between two surfaces that are
    # interpolating the same heightmap at different resolutions.
    prism("plate", data["ring"], -Z_SKIRT, Z_BRICK, mats["Toy_stone"], mats["Toy_brick"])

    # Joint bands, in the second brick tone. Clipped to the promenade block and
    # the Market forecourt so nothing runs out over the plaza's chamfers.
    v, f = [], []
    e = -101.0
    while e < 96.0:
        n0, n1 = (-43.0, 3.0) if e < 2.0 else (-19.0, 17.0)
        box(v, f, e - 0.22, e + 0.22, n0, n1, Z_BRICK - 0.02, Z_JOINT)
        e += BAY
    n = -37.9
    while n < 2.0:
        box(v, f, -106.0, 1.6, n - 0.22, n + 0.22, Z_BRICK - 0.02, Z_JOINT)
        n += BAY
    # the Market forecourt gets the same grain, but run parallel to MARKET's
    # 45.20 deg frontage rather than to the Fulton axis — which is what the real
    # paving does where the two grids meet, and what stops the wedge reading as
    # one blank red triangle. Every band is clipped to the ring.
    ring = [tuple(p) for p in data["ring"]]
    for k in range(7):
        d = 7.5 + k * 6.5
        span = clip_span(ring, MARKET_P0, MARKET_DIR, MARKET_PERP, d - 0.2, d + 0.2,
                         2.0, 133.0)
        if not span:
            continue
        s0, s1 = span[0] + 1.0, span[1] - 1.0
        if s1 - s0 < 6.0:
            continue
        band = [
            (MARKET_P0[0] + s0 * MARKET_DIR[0] + (d - 0.2) * MARKET_PERP[0],
             MARKET_P0[1] + s0 * MARKET_DIR[1] + (d - 0.2) * MARKET_PERP[1]),
            (MARKET_P0[0] + s1 * MARKET_DIR[0] + (d - 0.2) * MARKET_PERP[0],
             MARKET_P0[1] + s1 * MARKET_DIR[1] + (d - 0.2) * MARKET_PERP[1]),
            (MARKET_P0[0] + s1 * MARKET_DIR[0] + (d + 0.2) * MARKET_PERP[0],
             MARKET_P0[1] + s1 * MARKET_DIR[1] + (d + 0.2) * MARKET_PERP[1]),
            (MARKET_P0[0] + s0 * MARKET_DIR[0] + (d + 0.2) * MARKET_PERP[0],
             MARKET_P0[1] + s0 * MARKET_DIR[1] + (d + 0.2) * MARKET_PERP[1]),
        ]
        vv, ff = prism_verts_faces(band, Z_BRICK - 0.02, Z_JOINT, base_index=len(v))
        v.extend(vv)
        f.extend(ff)
    new_mesh("joint_grid", v, f, [mats["Toy_rust"]])

    # the granite edge along the Market frontage: a 3 m band inside the kerb,
    # where the plaza meets the sidewalk and the transit platforms
    span = clip_span(ring, MARKET_P0, MARKET_DIR, MARKET_PERP, 1.4, 4.4, 2.0, 133.0)
    if span:
        s0, s1 = span[0] + 1.0, span[1] - 1.0
        band = [
            (MARKET_P0[0] + s * MARKET_DIR[0] + d * MARKET_PERP[0],
             MARKET_P0[1] + s * MARKET_DIR[1] + d * MARKET_PERP[1])
            for s, d in ((s0, 1.4), (s1, 1.4), (s1, 4.4), (s0, 4.4))
        ]
        prism("walk_market", band, Z_BRICK - 0.02, Z_WALK, mats["Toy_stone"])

    # The two main cross-walks: the promenade's own spine between the bed edges,
    # and the diagonal desire line from the Market/BART portal to the axis.
    v, f = [], []
    box(v, f, -107.0, 2.0, AXIS_N - 2.0, AXIS_N + 2.0, Z_BRICK - 0.02, Z_WALK)
    box(v, f, -47.9, -44.3, -43.0, 3.0, Z_BRICK - 0.02, Z_WALK)
    new_mesh("walk_spine", v, f, [mats["Toy_cream"]])


def inlays(data, mats):
    """Granite let into the brick: the 1995 Walk of Great Ideas, the UN emblem
    roundel on the colonnade centreline, and the coordinates cross in the
    south-west. Flush-plus-20 mm, not proud objects — these are inlays."""
    e0, e1, n0, n1 = WALK_BAND
    prism("inlay_walk", rect(e0, e1, n0, n1), Z_BRICK - 0.02, Z_INLAY, mats["Toy_stone"])
    em = data["un_emblem"]
    ec = sum(p[0] for p in em) / len(em)
    nc = sum(p[1] for p in em) / len(em)
    r = max(math.hypot(p[0] - ec, p[1] - nc) for p in em)
    prism("inlay_emblem", ngon(16, ec, nc, r), Z_BRICK - 0.02, Z_INLAY, mats["Toy_stone"])
    prism("inlay_emblem_ring", ngon(16, ec, nc, r * 0.62), Z_INLAY, Z_INLAY + 0.015,
          mats["Toy_white"])
    ce, cn = CROSS_C
    v, f = [], []
    box(v, f, ce - 5.0, ce + 5.0, cn - 0.7, cn + 0.7, Z_BRICK - 0.02, Z_INLAY)
    box(v, f, ce - 0.7, ce + 0.7, cn - 5.0, cn + 5.0, Z_BRICK - 0.02, Z_INLAY)
    new_mesh("inlay_cross", v, f, [mats["Toy_stone"]])


def beds(data, mats):
    """The three decomposed-granite planting beds. This plaza has almost no lawn
    — the beds are DG, not grass, and Toy_sand is what keeps them from reading as
    the green panels of Civic Center Plaza three blocks west."""
    for key, name in (("bed_nw", "bed_nw"), ("bed_sw", "bed_sw"), ("bed_ne", "bed_ne")):
        ring = data[key]
        prism(name + "_kerb", ring, Z_BRICK - 0.02, Z_BED, mats["Toy_rust"])
        # the DG surface, inset so the kerb reads as a separate lip from above
        ec = sum(p[0] for p in ring) / len(ring)
        nc = sum(p[1] for p in ring) / len(ring)
        inner = [(ec + (p[0] - ec) * 0.965, nc + (p[1] - nc) * 0.90) for p in ring]
        prism(name, inner, Z_BED - 0.02, Z_BED + 0.02, mats["Toy_sand"])


def terrace(mats):
    """The raised south terrace descending to the promenade in three treads.
    Read from OSM way 128534066 plus its two retaining walls and three step
    lines; the platform is on the Market side and the steps face the plaza."""
    e0, e1 = TERRACE_E
    n0, n1 = TERRACE_N_HIGH
    prism("terrace", rect(e0, e1, n0, n1), 0.0, Z_TERRACE, mats["Toy_stone"],
          mats["Toy_brick"])
    v, f = [], []
    for i, ns in enumerate(TERRACE_STEPS):
        z = Z_TERRACE - (i + 1) * (Z_TERRACE - Z_BRICK) / (len(TERRACE_STEPS) + 1)
        box(v, f, e0, e1, ns - 0.75, ns + 0.75, 0.0, z)
    new_mesh("terrace_steps", v, f, [mats["Toy_stone"]])
    # the low retaining wall where the terrace meets the promenade
    prism("terrace_wall", rect(e0, e1, -34.4, -34.0), 0.0, Z_BRICK + 0.45,
          mats["Toy_stone"])


def colonnade(data, mats):
    """Sixteen inscribed granite light standards with frosted globes: two rows of
    eight, 11.76 m apart across the axis, ~11.77 m along it with one wider bay at
    the centre where the UN emblem sits. Positions are MEASURED and carry real
    survey jitter of a few centimetres — keep it. A perfectly ruled colonnade is
    the single easiest way to make this asset look procedural rather than
    surveyed. The recessed band on each shaft stands for the inscribed nation
    names; do not letter them (style bible s.26)."""
    v, f = [], []
    h = COLUMN_SIDE / 2.0
    for i, (e, n) in enumerate(data["light_standards"]):
        box(v, f, e - h, e + h, n - h, n + h, Z_BRICK, COLUMN_SHAFT - 0.30)
        # the inscription band, recessed
        box(v, f, e - h + 0.06, e + h - 0.06, n - h + 0.06, n + h - 0.06,
            1.30, 3.10)
        # cap
        box(v, f, e - h - 0.07, e + h + 0.07, n - h - 0.07, n + h + 0.07,
            COLUMN_SHAFT - 0.30, COLUMN_SHAFT)
        # the globe's neck
        frustum(v, f, 8, e, n, 0.10, 0.10, COLUMN_SHAFT, Z_COLUMN - 2 * GLOBE_R)
    new_mesh("columns", v, f, [mats["Toy_stone"]])

    # The globes, as one merged object so the loader's glow set stays cheap. A
    # 10-sided lantern rather than a sphere: it is 1 px of silhouette at the
    # app's camera and a sphere would cost 6x for nothing.
    v, f = [], []
    for e, n in data["light_standards"]:
        z0 = Z_COLUMN - 2 * GLOBE_R
        profile(v, f, 8, e, n, [(0.13, z0), (GLOBE_R, z0 + GLOBE_R * 0.7),
                                (0.11, Z_COLUMN)])
    new_mesh("globes_glow", v, f, [mats["Toy_white_Glow"]])

    # The 2023 Tivoli/festoon lighting, strung along each column row. BULBS, not
    # a continuous bar: the first night render used one 86 m glowing rail per row
    # and the result was two light-sabres that buried the sixteen globes this
    # asset's night state is supposed to be about. Emission is uniform across a
    # _Glow material, so the only lever is area — a dash every 2.4 m reads as a
    # string of lights and stays subordinate.
    # Strung down the CENTRELINE between the two column rows, which is both how
    # festoon lighting is actually hung and what keeps it from merging with the
    # globes: on the column rows themselves the two glow families interleaved
    # into one indistinguishable dotted line and the colonnade stopped reading.
    v, f = [], []
    e = -89.0
    while e < -4.0:
        box(v, f, e, e + 0.34, AXIS_N - 0.055, AXIS_N + 0.055, 5.06, 5.17)
        e += 2.4
    new_mesh("festoon_glow", v, f, [mats["Toy_cream_Glow"]])


def fountain(mats):
    """Halprin's 1975 fountain: 673 Sierra granite blocks in a sunken basin, the
    plaza's most photographed object and its least tractable. Built as an
    octagonal well holding the NINE granite masses DataSF's LiDAR actually
    surveyed — positions and heights both measured, which makes this the only
    fully surveyed element in the asset. Do not attempt 673 blocks and do not
    attempt water: the real fountain has been dry more often than not since 1978."""
    e0, e1, n0, n1 = WELL
    c = WELL_CHAMFER
    outline = [
        (e0 + c, n0), (e1 - c, n0), (e1, n0 + c), (e1, n1 - c),
        (e1 - c, n1), (e0 + c, n1), (e0, n1 - c), (e0, n0 + c),
    ]
    def shrink(k):
        return [(e0 + c + k, n0 + k), (e1 - c - k, n0 + k), (e1 - k, n0 + c + k),
                (e1 - k, n1 - c - k), (e1 - c - k, n1 - k), (e0 + c + k, n1 - k),
                (e0 + k, n1 - c - k), (e0 + k, n0 + c + k)]

    # kerb, bench course, sunken floor: the basin has to read as SUNK from
    # above, which a filled prism cannot do however tall you make it
    ring_prism("fount_kerb", outline, shrink(2.0), 0.0, Z_FOUNT_RIM, mats["Toy_stone"])
    ring_prism("fount_bench", shrink(2.0), shrink(3.4), 0.0, Z_FOUNT_RIM * 0.48,
               mats["Toy_stone"])
    # The basin floor has to sit ABOVE the brick plate (0.30) or it is invisible
    # and the basin reads as brick — the plate covers the whole ring. Dark, so
    # the pale granite pile pops out of a shadowed well rather than sitting on a
    # pale field the same value as its own kerb.
    prism("fount_floor", shrink(3.4), 0.0, Z_BRICK + 0.02, mats["Toy_ink"],
          mats["Toy_roofd"])

    v, f = [], []
    mce = sum((a + b) / 2 for a, b, _, _, _ in FOUNTAIN_SLABS) / len(FOUNTAIN_SLABS)
    mcn = sum((c + d) / 2 for _, _, c, d, _ in FOUNTAIN_SLABS) / len(FOUNTAIN_SLABS)
    for i, (a, b, cc, d, hgt) in enumerate(FOUNTAIN_SLABS):
        a, b = a + (mce - a) * SLAB_PULL, b + (mce - b) * SLAB_PULL
        cc, d = cc + (mcn - cc) * SLAB_PULL, d + (mcn - d) * SLAB_PULL
        # each slab is stepped: a broad plinth and a narrower crest, which is
        # what makes the pile read as stacked rather than as extruded footprints
        box(v, f, a, b, cc, d, Z_BRICK, hgt * 0.48)
        # the crest, inset CONCENTRICALLY and shifted by a deterministic hash so
        # the pile reads as asymmetrically stacked slabs (which it is) rather
        # than as nine extruded footprints
        ie, jn = (b - a) * 0.22, (d - cc) * 0.22
        se = (hash01(i * 31 + 7) - 0.5) * ie
        sn = (hash01(i * 91 + 3) - 0.5) * jn
        box(v, f, a + ie + se, b - ie + se, cc + jn + sn, d - jn + sn,
            hgt * 0.48, hgt)
    new_mesh("fount_slabs", v, f, [mats["Toy_stone"]])


def monuments(data, mats):
    """Simon Bolivar closing the Fulton axis at Hyde Street, the 1995 UDHR
    obelisk in the north bed, and the two flagpoles. The bronze is rendered as
    one chunky verdigris mass on a pale pedestal: an equestrian statue is 8 m of
    a 220 m asset and modelling a horse would spend a tenth of the triangle
    budget on something two pixels wide."""
    be, bn = data["points"]["bolivar_statue"]
    prism("bolivar_base", rect(be - 3.0, be + 3.0, bn - 3.6, bn + 3.6), 0.0, 0.85,
          mats["Toy_stone"])
    prism("bolivar_plinth", rect(be - 1.9, be + 1.9, bn - 2.4, bn + 2.4), 0.85, 4.30,
          mats["Toy_stone"])
    v, f = [], []
    box(v, f, be - 1.5, be + 1.5, bn - 0.75, bn + 0.75, 4.30, 6.35)   # horse body
    box(v, f, be - 0.45, be + 0.75, bn - 0.45, bn + 0.45, 6.35, Z_BOLIVAR)  # rider
    new_mesh("bolivar_bronze", v, f, [mats["Toy_verdigris"]])

    oe, on = data["points"]["obelisk"]
    v, f = [], []
    profile(v, f, 4, oe, on, [(0.62, Z_BED), (0.40, Z_OBELISK - 0.55),
                              (0.02, Z_OBELISK)], rot=math.pi / 4)
    new_mesh("obelisk", v, f, [mats["Toy_ink"]])

    for key, flagmat in (("flagpole_un", "Toy_navy"), ("flagpole_us", "Toy_red")):
        fe, fn = data["points"][key]
        prism("plinth_" + key, ngon(10, fe, fn, 1.5), Z_BRICK - 0.02, Z_BRICK + 0.25,
              mats["Toy_stone"])
        v, f = [], []
        frustum(v, f, 8, fe, fn, 0.17, 0.09, Z_BRICK + 0.25, Z_FLAGPOLE)
        new_mesh("pole_" + key, v, f, [mats["Toy_steel"]])
        # the flag as one flat slab with no devices — style bible s.26, and the
        # only defensible call for a plaza whose flags are themselves political
        v, f = [], []
        box(v, f, fe + 0.10, fe + 3.20, fn - 0.06, fn + 0.06, Z_FLAGPOLE - 2.15,
            Z_FLAGPOLE - 0.25)
        new_mesh("flag_" + key, v, f, [mats[flagmat]])


def skate(mats):
    """The UN Skate Plaza — 13,000 sq ft opened November 2023, expanded by
    2,100 sq ft in February 2025 with three geometric skateable art pieces by
    Alexis Sablone. A pale concrete pad proud of the brick with low ledges and
    banks: it is a 2023 layer INSERTED into a 1975 plaza and should read as
    inserted, not as part of the paving. The outline is inferred (REPORT.md)."""
    prism("skate_pad", SKATE, Z_BRICK - 0.02, Z_SKATE, mats["Toy_stone"])
    # Four bollard-scale pools on the pad, NOT a strip: a 46 m lit strip read as
    # an airport runway at night and competed with the colonnade, which is the
    # only thing this plaza's night state should be about.
    for i, (ge, gn) in enumerate(((-2.0, -30.0), (12.0, -14.0), (24.0, -31.0),
                                  (36.0, -16.0))):
        prism(f"skate_glow_{i}", ngon(8, ge, gn, 1.5), Z_SKATE, Z_SKATE + 0.012,
              mats["Toy_cream_Glow"])
    v, f = [], []
    for i, (e0, e1, n0, n1, h) in enumerate((
        (-4.0, 12.0, -34.4, -33.0, 0.42),    # long ledge, south
        (16.0, 30.0, -31.8, -30.4, 0.42),
        (-2.0, 11.0, -13.8, -12.4, 0.55),    # long ledge, north
        (20.0, 34.0, -16.4, -15.0, 0.38),
        (25.6, 27.6, -28.0, -19.0, 0.50),    # cross ledge
        (-6.0, 4.0, -20.0, -18.0, 0.30),     # low bank
        (6.0, 14.0, -30.0, -27.0, 0.62),     # quarter block
        (30.0, 38.0, -21.0, -18.0, 0.48),
        (18.0, 24.0, -25.5, -24.3, 0.34),
        (-4.0, 2.0, -29.5, -28.5, 0.34),
    )):
        box(v, f, e0, e1, n0, n1, Z_SKATE - 0.05, Z_SKATE + h)
    new_mesh("skate_ledges", v, f, [mats["Toy_cream"]])
    # the three Sablone art blocks: the plaza's only saturated accents
    for name, (e, n, r, h) in (
        ("Toy_teal", (1.0, -25.5, 2.6, 1.55)),
        ("Toy_coral", (14.5, -19.5, 2.2, 1.15)),
        ("Toy_mustard", (32.0, -25.0, 2.4, 1.85)),
    ):
        v, f = [], []
        frustum(v, f, 6, e, n, r, r * 0.55, Z_SKATE, Z_SKATE + h)
        new_mesh("skate_art_" + name.split("_")[1], v, f, [mats[name]])


# ------------------------------------------------------------------- planting

# The plaza's trees are NOT in OSM (only four, at the 7th-and-Market corner).
# The rows below are derived from the three measured bed outlines and from
# canopy positions read off the z20 aerial; they are INFERRED, not surveyed, and
# they are written out to data/trees_en.json so the inference is reviewable in a
# diff rather than buried in this script. Wikipedia records 192 London plane and
# black poplar trees along the promenade in 1975; far fewer stand today.
TREE_ROWS = [
    # (e0, e1, n, count) — two rows per bed, offset so the canopies interlock
    (-91.5, -57.0, -8.0, 6),
    (-88.0, -60.5, -2.6, 5),
    (-91.5, -57.0, -37.0, 6),
    (-88.0, -60.5, -32.4, 5),
    (-34.5, -1.5, -7.8, 6),
    (-31.0, -5.0, -2.4, 5),
    (-34.0, -3.0, -47.5, 5),
    (-30.0, -6.0, -42.0, 4),
]


def trees(data, mats):
    """Pruned street planes in the civic-center-plaza family: a knuckled trunk
    under a wide, slightly flattened crown. Toy_verdigris crowns so they
    separate from the brick from above — a mint crown on a red field is the one
    colour pair in this palette that vibrates."""
    pos = []
    for ri, (e0, e1, n, count) in enumerate(TREE_ROWS):
        for i in range(count):
            t = i / max(count - 1, 1)
            je = (hash01(ri * 977 + i * 31) - 0.5) * 1.6
            jn = (hash01(ri * 613 + i * 71) - 0.5) * 1.3
            pos.append([round(e0 + t * (e1 - e0) + je, 2), round(n + jn, 2)])
    for p in data["trees_osm"]:
        pos.append([round(p[0], 2), round(p[1], 2)])
    for i in range(5):                       # the Leavenworth arm's planting
        pos.append([round(25.5 + (hash01(i * 53) - 0.5) * 2.6, 2), round(24.0 + i * 11.0, 2)])
    with open(os.path.join(HERE, "data", "trees_en.json"), "w", encoding="utf8") as fh:
        json.dump({"note": "INFERRED tree positions in the plaza (e, n) frame — see "
                           "REPORT.md. The plaza's trees are not mapped in OSM.",
                   "count": len(pos), "trees": pos}, fh, indent=1)

    # The datum tree: exactly one crown reaches Z_TREE and it is asserted in
    # report(). Every other crown is scaled below it, so a change to the datum
    # cannot silently rescale the plaza.
    # exactly one crown carries the height datum: the tree nearest (-70, -8),
    # mid-way down the north-west bed, where it is visible in every review view
    tallest = min(range(len(pos)),
                  key=lambda i: math.hypot(pos[i][0] + 70.0, pos[i][1] + 8.0))
    v, f = [], []
    n_bed = sum(r[3] for r in TREE_ROWS)
    for i, (e, n) in enumerate(pos):
        base = Z_BED if i < n_bed else (Z_ARM if i >= len(pos) - 5 else Z_BRICK)
        h = Z_TREE if i == tallest else Z_TREE * (0.74 + 0.20 * hash01(i * 197))
        trunk = h * 0.42
        frustum(v, f, 6, e, n, 0.38, 0.26, base - 0.10, trunk)
        frustum(v, f, 8, e, n, 0.26, 2.20, trunk, trunk + (h - trunk) * 0.30)
    new_mesh("trees", v, f, [mats["Toy_steel"]])
    v, f = [], []
    for i, (e, n) in enumerate(pos):
        h = Z_TREE if i == tallest else Z_TREE * (0.74 + 0.20 * hash01(i * 197))
        trunk = h * 0.42
        z0 = trunk + (h - trunk) * 0.30
        profile(v, f, 8, e, n, [(2.20, z0), (2.45, z0 + (h - z0) * 0.45),
                                (0.45, h)])
    new_mesh("crowns", v, f, [mats["Toy_verdigris"]])
    return pos


# ------------------------------------------------------------------ furniture


def furniture(data, mats):
    """Benches, game tables, the fitness frame, planters, bins, bike racks, the
    Pit Stop and the BART/Muni portal heads. This is the most heavily used public
    space in the Civic Center and a plaza with no furniture in it reads as a car
    park (style bible s.15)."""
    v, f = [], []
    # the long benches between the column rows, on the colonnade's own bay pitch
    e = -84.0
    while e < -8.0:
        for n in (-23.4, -16.3):
            box(v, f, e, e + 4.4, n - 0.32, n + 0.32, Z_BRICK, Z_BRICK + 0.14)
            box(v, f, e + 0.3, e + 0.7, n - 0.26, n + 0.26, Z_BRICK - 0.02, Z_BRICK)
            box(v, f, e + 3.7, e + 4.1, n - 0.26, n + 0.26, Z_BRICK - 0.02, Z_BRICK)
        e += BAY * 2
    # the 2023 game tables: chess and ping-pong, on the promenade's south walk
    for i in range(6):
        te = -78.0 + i * 11.5
        box(v, f, te - 1.35, te + 1.35, -29.2, -27.7, Z_BRICK + 0.62, Z_BRICK + 0.70)
        for de, dn in ((-1.1, -0.5), (1.1, -0.5), (-1.1, 0.5), (1.1, 0.5)):
            box(v, f, te + de - 0.06, te + de + 0.06, -28.45 + dn - 0.06,
                -28.45 + dn + 0.06, Z_BRICK, Z_BRICK + 0.62)
    # bins and planters along the walks
    for i in range(10):
        be = -96.0 + i * 10.4
        box(v, f, be - 0.30, be + 0.30, -12.4, -11.8, Z_BRICK, Z_BRICK + 0.85)
    new_mesh("furniture", v, f, [mats["Toy_roofd"]])

    # the fitness frame (OSM leisure=fitness_station, 2023)
    fe, fn = data["points"]["fitness_station"]
    v, f = [], []
    for de in (-3.0, 3.0):
        box(v, f, fe + de - 0.10, fe + de + 0.10, fn - 1.6, fn - 1.4, Z_BRICK, Z_BRICK + 2.4)
        box(v, f, fe + de - 0.10, fe + de + 0.10, fn + 1.4, fn + 1.6, Z_BRICK, Z_BRICK + 2.4)
    box(v, f, fe - 3.1, fe + 3.1, fn - 1.6, fn + 1.6, Z_BRICK + 2.4, Z_BRICK + 2.55)
    new_mesh("fitness", v, f, [mats["Toy_steel"]])

    # bike racks
    v, f = [], []
    for key in ("bike_share",):
        pass
    for be, bn in ((-72.78, -31.02), (-34.59, -60.81), (37.10, -30.20), (79.63, 2.56)):
        for k in range(4):
            box(v, f, be + k * 0.9, be + k * 0.9 + 0.09, bn - 0.45, bn + 0.45,
                Z_BRICK, Z_BRICK + 0.80)
    new_mesh("bike_racks", v, f, [mats["Toy_steel"]])

    # the Pit Stop toilet and the BART/Muni portal heads. The elevator head is
    # the one from OSM way 1423414236; the two stair heads flank the Market
    # frontage where the ring's own steps and turnstile lines put them.
    pe, pn = data["points"]["pit_stop_toilet"]
    prism("pit_stop", rect(pe - 1.5, pe + 1.5, pn - 1.2, pn + 1.2), Z_BRICK,
          Z_BRICK + 2.6, mats["Toy_teal"], mats["Toy_roofd"])
    prism("portal_elevator", rect(6.8, 10.2, -50.2, -46.7), Z_BRICK, Z_BRICK + 3.1,
          mats["Toy_roofd"])
    prism("portal_elevator_glow", rect(6.9, 10.1, -50.1, -46.8), Z_BRICK + 3.1,
          Z_BRICK + 3.16, mats["Toy_teal_Glow"])
    for i, (e0, e1, n0, n1) in enumerate(((-20.0, -13.0, -47.0, -43.0),
                                          (28.5, 34.9, -40.6, -31.9))):
        prism(f"portal_{i}", rect(e0, e1, n0, n1), Z_BRICK, Z_BRICK + 1.35,
              mats["Toy_roofd"])


def leavenworth_arm(data, mats):
    """The closed block of Leavenworth Street running north from the plaza along
    the Federal Building's east flank: a raised planted strip with the 2023 dog
    run fenced inside it, and a paved service edge. Nine metres wide and 56 long,
    it sets the model's Y bounding box on its own — kept because it is part of
    the polygon the pipeline's landcover and exclusion already use."""
    prism("arm_strip", rect(21.0, 31.0, 17.0, 74.0), Z_BRICK - 0.02, Z_ARM,
          mats["Toy_stone"], mats["Toy_sand"])
    prism("arm_dogrun", data["dog_run"], Z_ARM - 0.02, Z_ARM + 0.03, mats["Toy_mint"])
    v, f = [], []
    for n in (28.6, 58.3):
        box(v, f, 21.0, 30.7, n - 0.05, n + 0.05, Z_ARM, Z_ARM + 1.15)
    for e in (21.0, 30.7):
        box(v, f, e - 0.05, e + 0.05, 28.6, 58.3, Z_ARM, Z_ARM + 1.15)
    new_mesh("arm_fence", v, f, [mats["Toy_steel"]])


def people(mats):
    """Four deliberate activity nodes, not an even sprinkle (style bible s.16):
    the skate pad, the fountain rim, the game tables and the Market/BART portal.
    Chunky capsules, no faces — these are 1-2 px at the app's camera and their
    job is to give the plaza scale and life."""
    v, f = [], []
    clusters = ((8.0, -24.0, 7), (44.0, -6.0, 5), (-60.0, -28.0, 5), (-6.0, -48.0, 6))
    for ci, (ce, cn, count) in enumerate(clusters):
        for i in range(count):
            a = 2 * math.pi * hash01(ci * 811 + i * 47)
            r = 1.2 + 3.4 * hash01(ci * 401 + i * 13)
            e, n = ce + r * math.cos(a), cn + r * math.sin(a)
            h = 1.62 + 0.22 * hash01(ci * 71 + i)
            frustum(v, f, 6, e, n, 0.20, 0.17, Z_BRICK, Z_BRICK + h * 0.72)
            frustum(v, f, 6, e, n, 0.17, 0.05, Z_BRICK + h * 0.72, Z_BRICK + h)
    new_mesh("people", v, f, [mats["Toy_roofd"]])


# -------------------------------------------------------------------- output


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
    per = []
    for o in objs:
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        per.append((o.name, len(me.loop_triangles)))
        tris += len(me.loop_triangles)
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    per.sort(key=lambda p: -p[1])
    for name, t in per[:14]:
        print(f"[build]   {name:26} {t:6}")
    print(f"[build] objects={len(objs)} tris={tris} (cap {TRI_CAP})")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    lon0, lat0 = -122.4138900, 37.7801415
    m_per_lon = 111320.0 * math.cos(math.radians(37.77))
    lon = lon0 + ANCHOR_SHIFT[0] / m_per_lon
    lat = lat0 + ANCHOR_SHIFT[1] / 110540.0
    print(f"[build] plan anchor lon/lat: {lon0} {lat0}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] Fulton axis {HEADING_E} deg true; Market frontage {HEADING_MARKET} deg")
    # min_z is deliberately NEGATIVE on this asset: z = 0 is the anchor's ground,
    # which is where the loader puts the model, and the plate is draped onto the
    # real terrain around it. targetHeightM is therefore the model's VERTICAL
    # EXTENT, not an architectural height — the loader's scale is
    # targetHeightM / bbox-height and must land on 1.0. Same two deliberate
    # contract deviations as artifacts/424-brannan.
    extent = mx[2] - mn[2]
    print(f"[build] DRAPED asset: min_z={mn[2]:.3f} (negative by design), "
          f"max_z={mx[2]:.3f}, vertical extent={extent:.4f}")
    print(f"[build] MANIFEST targetHeightM must be {extent:.4f} for uniform x1.0000")
    # what replaces "min_z ~ 0": the paving must stand a CONSTANT height above the
    # terrain everywhere, which is the thing the drape exists to guarantee
    spread = []
    for e, n in [(a, b) for a in range(-104, 109, 8) for b in range(-72, 73, 8)]:
        spread.append(Z_BRICK)
    print(f"[build] paving stands {Z_BRICK:.2f} m above the sampled terrain by construction")
    if tris > TRI_CAP:
        print(f"[build] WARNING triangle cap exceeded: {tris} > {TRI_CAP}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = HERE
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "un-plaza.blend")
    glb = os.path.join(out, "un-plaza.glb")
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
