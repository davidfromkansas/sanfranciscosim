"""Deterministic Blender build of the SF-SIM miniature 424 Brannan parking lot.

    blender -b --python build_424_brannan.py -- [--out DIR]

Writes 424-brannan.blend and 424-brannan.glb next to this file (or into --out).
Geometry is authored in world space in metres, Z up, +X east, +Y north, so the
model drops into the city at its real-world heading — the loader applies no
rotation. Origin = the parcel's axis-aligned bounding-box centre (anchor
lon -122.3954857, lat 37.7798744).

WHAT THIS ASSET IS. 424 Brannan Street is not a building and never has been: it
is a 2,026 m2 Z-shaped through-block surface parking lot (Tower Valet Parking,
60 permitted stalls) that reaches Brannan through a 15.8 m neck, runs 68.4 m of
fence along Ritch, and opens a gate on Zoe. DataSF returns zero building
footprints on parcel 3776455; the assessor carries it as class V, vacant, with
$0 of improvements. The subject is the void: a pale ordered rectangle punched
through a block of otherwise continuous roofs.

Design (see REFERENCE.md for the sources behind every number):

* recognition rests on GROUND PATTERN, OUTLINE and ONE SIGN, not on massing.
  The plan view is the hero image for this asset, not the aerial;
* the parcel ring, the anchor and the positions of the booth, the trailer and
  the two green masses are MEASURED (data/site_uv.json, from the DataSF parcel
  layer and z21 nadir imagery). The row layout is a reconstruction that totals
  exactly the 60 permitted stalls; the departures are named in REPORT.md;
* everything is a closed solid with real thickness stacked in Z, and every
  superstructure's bottom cap is buried INSIDE the plate rather than laid on
  it, so nothing is coplanar with anything else and nothing z-fights the baked
  landcover (which sits +0.06 m above terrain);
* night state: the PUBLIC PARKING sign is the hero glow — a lit box sign is what
  this lot actually shows after dark. The booth window and three lamp heads are
  the only supporting accents; the plate, the striping and the cars go dark.

THE ASSET IS DRAPED. app/src/assets.js seats a landmark by ONE terrain sample,
at the anchor, which is right for a building and wrong for an asset that IS the
ground: this lot falls 1.469 m across its bounding box, so a flat plate would be
0.78 m under the terrain at the Zoe end and 0.69 m above it at Brannan — perfect
in every Blender render and broken in the app. So every z here is
`authored height + TERRAIN(u, v)`, and z = 0 means THE ANCHOR'S GROUND rather
than the bottom of the model. Two consequences the rest of the pipeline has to
know about, both asserted by validate_424_brannan.py:
  * min_z is negative (about -1.1 m), not 0;
  * targetHeightM is the model's VERTICAL EXTENT, not an architectural height,
    because the loader's scale is targetHeightM / bbox height and must be 1.0.
Unlike South Park, this site falls in two directions at once (2.18% toward
bearing 250), so dy is a 2-D grid, not a 1-D profile.

Authoring frame: (u, v), u along Brannan POSITIVE TOWARD THE NORTH-EAST (bearing
45.2 deg), v across it POSITIVE TOWARD BRANNAN (bearing 135.2 deg). The frame is
LEFT-handed in world exactly as South Park's and civic-center-plaza's are, so
every ring goes through orient_for_world() before extrusion — a build that skips
it exports inside-out caps that pass every dimension check and fail the normals
test.
"""

import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

HEADING_U = 45.2    # +u, north-east along Brannan
HEADING_V = 135.2   # +v, south-east toward Brannan

_RU = math.radians(HEADING_U)
_RV = math.radians(HEADING_V)
U_DIR = (math.sin(_RU), math.cos(_RU))
V_DIR = (math.sin(_RV), math.cos(_RV))

# Z stack, all relative to the local draped ground. Nothing is coplanar with
# anything else, and every superstructure starts BELOW the plate top.
Z_PLATE_BOT = -0.30
Z_PLATE_TOP = 0.12    # the paved surface; +0.06 m of the clearance is the
                      # margin against the baked landcover
Z_BURY = 0.05         # where things standing on the plate start
Z_KERB = 0.30
Z_PATCH = 0.13
Z_STRIPE = 0.145
Z_STOP = 0.26

KERB_W = 0.30
STRIPE_W = 0.18
STOP_L, STOP_W = 1.70, 0.16

FENCE_POST = 0.09
FENCE_H = 2.30
FENCE_PITCH = 3.00
MESH_LO, MESH_HI, MESH_T = 0.18, 1.05, 0.04
MID_LO, MID_HI, MID_T = 1.35, 1.42, 0.06
RAIL_LO, RAIL_HI, RAIL_T = 2.05, 2.15, 0.08
BARB_LO, BARB_HI, BARB_T = 2.22, 2.27, 0.04

SIGN_UV = (17.00, 43.00)
SIGN_POST = 0.22
SIGN_TOP = 6.80        # *** the model's crest: this sets targetHeightM ***
SIGN_BOARD_W = 2.60
SIGN_BOARD_T = 0.18
SIGN_BOARD_LO, SIGN_BOARD_HI = 4.90, 6.50

BOOTH_L, BOOTH_W, BOOTH_H, BOOTH_RIDGE = 3.00, 2.40, 2.40, 2.72
TRAILER_L, TRAILER_W = 6.00, 2.50

LAMP_UV = ((17.40, 28.00), (17.40, -18.00), (-26.90, -21.00))
LAMP_H = 5.20

BAY_W, BAY_D = 2.65, 5.20      # 8'8" x 17'
PARALLEL_W, PARALLEL_L = 2.40, 6.00

TRI_CAP = 18000

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",       # the paved plate — the asset's dominant surface
    "Toy_trim": "f3efe6",        # kerb
    "Toy_sand": "ece4d4",        # the one concrete patch
    "Toy_mustard": "d9a441",     # stall striping
    "Toy_ink": "3a3530",         # plate skirt, wheel stops, barbed strand, booth
                                 # roof, lamp heads, trailer chassis, dark cars.
                                 # NOT Toy_roofd: it renders rgb(9,9,12) under
                                 # the app's lighting (156 South Park, Aug 2026)
    "Toy_steel": "9aa0a6",       # fence posts, rails, gates, sign post, lamp
                                 # poles, grey cars
    "Toy_red": "c4453c",         # the PUBLIC PARKING field
    "Toy_white": "f7f4ec",       # sign wordmark band, box trailer, white cars
    "Toy_cream": "f2ede3",       # booth walls
    "Toy_glass": "2a4d73",       # booth window, car greenhouses
    "Toy_navy": "2c4a70",
    "Toy_teal": "3fa8a0",
    "Toy_coral": "e8735a",
    "Toy_sky": "6db3d9",
    "Toy_verdigris": "9fb8a8",   # foliage — the same crown colour as South Park
                                 # and civic-center-plaza's bosques: one toy box
    "Toy_rust": "a86444",        # trunks
    "Toy_red_Glow": "c4453c",    # HERO: the sign field at night
    "Toy_white_Glow": "f7f4ec",  # the sign's wordmark band
    "Toy_trim_Glow": "f3efe6",   # the booth window
    "Toy_gold_Glow": "caa64a",   # the three lamp heads
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


def hash01(n):
    """Deterministic [0,1) hash — the same mixer pipeline/lib/geo.mjs uses, so
    'random' variation is reproducible across rebuilds and shows in a diff."""
    h = (n ^ 0x9E3779B9) * 0x85EBCA6B & 0xFFFFFFFF
    h = (h ^ (h >> 13)) * 0xC2B2AE35 & 0xFFFFFFFF
    h ^= h >> 16
    return (h & 0xFFFFFFFF) / 4294967296.0


# ----------------------------------------------------------------- transforms


def to_world(u, v):
    return (u * U_DIR[0] + v * V_DIR[0], u * U_DIR[1] + v * V_DIR[1])


class Terrain:
    """Bilinear lookup over the dy grid written by sample_terrain.mjs — the same
    surface app/src/terrain.js evaluates, so the plate hugs the runtime's ground
    rather than a plane fitted through it."""

    def __init__(self, data):
        self.u0 = data["u_min"]
        self.v0 = data["v_min"]
        self.step = data["step"]
        self.nu = data["nu"]
        self.nv = data["nv"]
        self.grid = data["grid"]
        self.fall = data["fall_m"]
        self.residual = data["plane"]["max_residual_m"]

    def __call__(self, u, v):
        fu = (u - self.u0) / self.step
        fv = (v - self.v0) / self.step
        i = min(self.nu - 2, max(0, int(math.floor(fu))))
        j = min(self.nv - 2, max(0, int(math.floor(fv))))
        tu = min(1.0, max(0.0, fu - i))
        tv = min(1.0, max(0.0, fv - j))
        a = self.grid[j][i]
        b = self.grid[j][i + 1]
        c = self.grid[j + 1][i]
        d = self.grid[j + 1][i + 1]
        return (a + (b - a) * tu) + ((c + (d - c) * tu) - (a + (b - a) * tu)) * tv


TERRAIN = None  # set in main()


# ------------------------------------------------------------- ring utilities


def orient_for_world(poly):
    """Order a site-frame ring so it comes out COUNTER-clockwise in world space,
    which is what makes prism_verts_faces' caps face outward. The (u, v) frame is
    left-handed in world (+u bears 45.2, +v bears 135.2, so their cross product
    points DOWN), so a ring that is CCW in (u, v) is CW in world: keep the ring
    whose (u, v) shoelace is NEGATIVE."""
    a = 0.0
    for i in range(len(poly)):
        u0, v0 = poly[i]
        u1, v1 = poly[(i + 1) % len(poly)]
        a += u0 * v1 - u1 * v0
    return list(poly) if a < 0 else list(reversed(poly))


def dedupe_ring(poly):
    out = []
    for p in poly:
        if not out or math.dist(p, out[-1]) > 1e-6:
            out.append(p)
    while len(out) > 1 and math.dist(out[0], out[-1]) < 1e-6:
        out.pop()
    return out


def point_in_ring(poly, p):
    u, v = p
    inside = False
    n = len(poly)
    for i in range(n):
        u1, v1 = poly[i]
        u2, v2 = poly[(i + 1) % n]
        if (v1 > v) != (v2 > v) and u < (u2 - u1) * (v - v1) / (v2 - v1) + u1:
            inside = not inside
    return inside


def u_span_at(poly, v):
    """The lot is v-simple: every v-slice is ONE u-interval (checked in
    REFERENCE.md s.3). Return it, or None outside the site."""
    hits = []
    n = len(poly)
    for i in range(n):
        u1, v1 = poly[i]
        u2, v2 = poly[(i + 1) % n]
        if (v1 > v) != (v2 > v):
            hits.append(u1 + (u2 - u1) * (v - v1) / (v2 - v1))
    if len(hits) < 2:
        return None
    return min(hits), max(hits)


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


def bevel(obj, width=0.12, segments=2, thin=None):
    """Miniature-style edge softening (style bible s.4). The offset is capped at
    a third of the object's thinnest dimension, because most of this asset is
    120-260 mm paving furniture and a flat 0.12 m bevel collapses opposing
    profiles into zero-area slivers even with clamp_overlap."""
    if thin is None:
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


def prism_verts_faces(poly_uv, z0, z1, base_index=0):
    """Closed extrusion of a site-frame polygon: walls + both caps, with every
    vertex draped on the terrain so a prism laid across the slope follows it."""
    ring_uv = orient_for_world(poly_uv)
    poly = [to_world(u, v) for u, v in ring_uv]
    dys = [TERRAIN(u, v) for u, v in ring_uv]
    n = len(poly)
    verts = ([(x, y, z0 + d) for (x, y), d in zip(poly, dys)]
             + [(x, y, z1 + d) for (x, y), d in zip(poly, dys)])
    b = base_index
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((b + i, b + j, b + n + j, b + n + i))
    faces.append(tuple(b + i for i in range(n - 1, -1, -1)))
    faces.append(tuple(b + i for i in range(n, 2 * n)))
    return verts, faces


def add_prism(vb, fb, poly_uv, z0, z1):
    v, f = prism_verts_faces(dedupe_ring(poly_uv), z0, z1, base_index=len(vb))
    vb.extend(v)
    fb.extend(f)


def box_uv(vb, fb, u0, u1, v0, v1, z0, z1):
    add_prism(vb, fb, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], z0, z1)


def oriented_box(vb, fb, uc, vc, du, dv, length, width, z0, z1):
    """A box centred at (uc, vc) whose long axis is the unit vector (du, dv)."""
    nu, nv = -dv, du
    hl, hw = length / 2.0, width / 2.0
    poly = [
        (uc - du * hl - nu * hw, vc - dv * hl - nv * hw),
        (uc + du * hl - nu * hw, vc + dv * hl - nv * hw),
        (uc + du * hl + nu * hw, vc + dv * hl + nv * hw),
        (uc - du * hl + nu * hw, vc - dv * hl + nv * hw),
    ]
    add_prism(vb, fb, poly, z0, z1)


def ngon_uv(nsides, uc, vc, r, rot=0.0):
    """Emitted CLOCKWISE in (u, v), i.e. counter-clockwise in world."""
    return [
        (uc + r * math.cos(rot - 2 * math.pi * i / nsides),
         vc + r * math.sin(rot - 2 * math.pi * i / nsides))
        for i in range(nsides)
    ]


def frustum(vb, fb, nsides, uc, vc, r0, r1, z0, z1, rot=0.0):
    b = len(vb)
    d = TERRAIN(uc, vc)
    lo = ngon_uv(nsides, uc, vc, r0, rot)
    hi = ngon_uv(nsides, uc, vc, r1, rot)
    vb.extend([to_world(u, v) + (z0 + d,) for u, v in lo])
    vb.extend([to_world(u, v) + (z1 + d,) for u, v in hi])
    for i in range(nsides):
        j = (i + 1) % nsides
        fb.append((b + i, b + j, b + nsides + j, b + nsides + i))
    fb.append(tuple(b + i for i in range(nsides - 1, -1, -1)))
    fb.append(tuple(b + nsides + i for i in range(nsides)))


def cone_ring(vb, fb, nsides, uc, vc, radii, zs, rot=0.0):
    """A stack of ngon rings closed top and bottom — the tree crowns."""
    b = len(vb)
    d = TERRAIN(uc, vc)
    for r, z in zip(radii, zs):
        vb.extend([to_world(u, v) + (z + d,) for u, v in ngon_uv(nsides, uc, vc, r, rot)])
    for k in range(len(radii) - 1):
        o0 = b + k * nsides
        o1 = b + (k + 1) * nsides
        for i in range(nsides):
            j = (i + 1) % nsides
            fb.append((o0 + i, o0 + j, o1 + j, o1 + i))
    fb.append(tuple(b + i for i in range(nsides - 1, -1, -1)))
    top = b + (len(radii) - 1) * nsides
    fb.append(tuple(top + i for i in range(nsides)))


def make_materials():
    mats = {}
    for name, rgb in PALETTE.items():
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        bsdf = m.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.85
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = 0.0
        if "Specular IOR Level" in bsdf.inputs:
            bsdf.inputs["Specular IOR Level"].default_value = 0.3
        m.diffuse_color = (*rgb, 1.0)
        m.roughness = 0.85
        mats[name] = m
    return mats


# ------------------------------------------------------------------ the layout
#
# 60 stalls, which is exactly the number on SFPD commercial-parking-lot permit
# 500106 and in the Colliers offering. The ROW STRUCTURE and the aisle are read
# off z21 nadir imagery; the per-row bay allocation is a reconstruction chosen
# to total 60 against the measured parcel. REPORT.md names every departure.
#
# Each row: an anchor line the cars nose into, a depth direction, a bay pitch
# along the row, and the bay count. `head` is the unit (du, dv) a parked car
# points in.

ROWS = {
    # against the 68.4 m Ritch fence; the lot's densest row
    "R": dict(kind="perp", head=(1.0, 0.0), far_u=18.10,
              along="v", start=-23.00, count=25, skip=(4, 5)),
    # facing R across the 6.4 m spine aisle
    "M": dict(kind="perp", head=(-1.0, 0.0), far_u=1.30,
              along="v", start=-6.70, count=11, skip=()),
    # backing onto the party line V7->V8
    "C1": dict(kind="perp", head=(0.0, 1.0), far_v=-8.70,
               along="u", start=-27.00, count=8, skip=()),
    # backing onto the party line V9->V10
    # backing onto the party line V9->V10. SIX bays, not seven: the seventh
    # would stand in the volunteer thicket that fills the notch corner.
    "C2": dict(kind="perp", head=(0.0, -1.0), far_v=-34.05,
               along="u", start=-27.00, count=6, skip=()),
    # against the Zoe fence, north of the gate
    "Z": dict(kind="perp", head=(-1.0, 0.0), far_u=-28.35,
              along="v", start=-25.90, count=7, skip=()),
    # the Brannan neck is only 15.8 m wide: one perpendicular row plus the aisle
    # leaves a 4 m strip, so the leftover is parallel stalls, as such strips are
    # in life. These four are what bring the total to 60.
    "A": dict(kind="parallel", u0=2.60, u1=5.00,
              along="v", start=16.50, pitch=6.00, count=5, skip=()),
}

# (row, bay index, body kind, material). 18 cars, not 60: the lot is never full
# and a solid model of it reads as noise from the aerial (style bible s.26).
CARS = [
    ("R", 0, "car", "Toy_white"),
    ("R", 1, "car", "Toy_ink"),
    ("R", 3, "pickup", "Toy_steel"),
    ("R", 7, "car", "Toy_navy"),
    ("R", 8, "car", "Toy_stone"),
    ("R", 12, "car", "Toy_red"),
    ("R", 16, "van", "Toy_white"),
    ("R", 20, "car", "Toy_teal"),
    ("M", 1, "car", "Toy_ink"),
    ("M", 4, "car", "Toy_steel"),
    ("M", 8, "car", "Toy_coral"),
    ("C1", 0, "car", "Toy_white"),
    ("C1", 2, "pickup", "Toy_ink"),
    ("C1", 5, "car", "Toy_sky"),
    ("C2", 1, "car", "Toy_steel"),
    ("C2", 4, "car", "Toy_navy"),
    ("Z", 2, "car", "Toy_stone"),
    ("A", 1, "car", "Toy_white"),
]

BODIES = {
    #        length  width  body z0   body z1  cabin len  cabin w  cabin z1
    "car": (4.30, 1.85, 0.24, 1.00, 2.10, 1.55, 1.38),
    "pickup": (5.40, 1.95, 0.26, 1.08, 1.80, 1.62, 1.60),
    "van": (5.20, 2.00, 0.24, 1.00, 3.20, 1.72, 1.98),
}

# Gate openings, as (edge index in the ring, span along that edge).
BRANNAN_GATE = (6.00, 12.50)     # in u, on the v = +44.48 frontage
ZOE_GATE = (-34.19, -27.20)      # in v, on the u = -28.5 frontage


def bay_centre(row, k):
    """Centre of bay k in (u, v), plus the bay's two extents."""
    r = ROWS[row]
    pitch = r.get("pitch", BAY_W)
    t = r["start"] + k * pitch
    if r["kind"] == "parallel":
        return ((r["u0"] + r["u1"]) / 2.0, t)
    if r["along"] == "v":
        far = r["far_u"]
        u = far + r["head"][0] * (-BAY_D / 2.0)
        return (u, t)
    far = r["far_v"]
    v = far + r["head"][1] * (-BAY_D / 2.0)
    return (t, v)


def row_bays(row):
    r = ROWS[row]
    return [k for k in range(r["count"]) if k not in r["skip"]]


def stripe_lines(row):
    """Bay-boundary lines, dropping any that would sit inside a skipped run."""
    r = ROWS[row]
    pitch = r.get("pitch", BAY_W)
    half = pitch / 2.0
    out = []
    for i in range(r["count"] + 1):
        t = r["start"] - half + i * pitch
        left, right = i - 1, i
        if left in r["skip"] and right in r["skip"]:
            continue
        out.append(t)
    return out


# -------------------------------------------------------------------- builder


def build_plate(site, ring):
    """The paved slab, draped. Sliced into v-bands at the ring's own breakpoints
    (every edge of this parcel is axis-aligned in (u, v), so the u-span is
    piecewise constant) and then into <=8 m cells across, so the top face follows
    the sampled terrain rather than a plane through four corners."""
    vb, fb = [], []
    breaks = sorted({round(p[1], 4) for p in ring})
    edges = []
    for a, b in zip(breaks, breaks[1:]):
        n = max(1, int(math.ceil((b - a) / 3.5)))
        for i in range(n):
            edges.append((a + (b - a) * i / n, a + (b - a) * (i + 1) / n))
    cells = 0
    for v0, v1 in edges:
        if v1 - v0 < 1e-6:
            continue
        s0 = u_span_at(ring, v0 + 1e-4)
        s1 = u_span_at(ring, v1 - 1e-4)
        if not s0 or not s1:
            continue
        width = max(s0[1] - s0[0], s1[1] - s1[0])
        n = max(1, int(math.ceil(width / 8.0)))
        for i in range(n):
            t0, t1 = i / n, (i + 1) / n
            a0 = s0[0] + (s0[1] - s0[0]) * t0
            a1 = s0[0] + (s0[1] - s0[0]) * t1
            b0 = s1[0] + (s1[1] - s1[0]) * t0
            b1 = s1[0] + (s1[1] - s1[0]) * t1
            add_prism(vb, fb, [(a0, v0), (a1, v0), (b1, v1), (b0, v1)],
                      Z_PLATE_BOT, Z_PLATE_TOP)
            cells += 1
    return vb, fb, cells


def edge_runs(p, q, gaps):
    """Split the segment p->q around the gate openings in `gaps`, each given as
    a (t0, t1) span in whichever of u/v varies along the edge."""
    du, dv = q[0] - p[0], q[1] - p[1]
    axis = 0 if abs(du) > abs(dv) else 1
    a, b = p[axis], q[axis]
    lo, hi = min(a, b), max(a, b)
    cuts = [(lo, hi)]
    for g0, g1 in gaps:
        nxt = []
        for c0, c1 in cuts:
            if g1 <= c0 or g0 >= c1:
                nxt.append((c0, c1))
                continue
            if g0 > c0:
                nxt.append((c0, g0))
            if g1 < c1:
                nxt.append((g1, c1))
        cuts = nxt
    out = []
    for c0, c1 in cuts:
        if c1 - c0 < 0.2:
            continue
        def at(t):
            f = (t - a) / (b - a) if abs(b - a) > 1e-9 else 0.0
            return (p[0] + du * f, p[1] + dv * f)
        out.append((at(c0), at(c1)))
    return out


def build(site, mats):
    ring = [tuple(p) for p in site["ring_uv"]]
    objs = []
    counts = {}

    # 1 ---------------------------------------------------------- the plate
    vb, fb, cells = build_plate(site, ring)
    plate = new_mesh("plate", vb, fb, [mats["Toy_stone"], mats["Toy_ink"]],
                     # skirt walls read as the ink shadow line under the slab;
                     # every 6th face of each prism is its top cap
                     [0 if (i % 6) == 5 else (1 if (i % 6) < 4 else 0)
                      for i in range(len(fb))])
    objs.append(plate)
    counts["plate cells"] = cells

    # 2 ------------------------------------------- kerb on the three frontages
    # Ritch V2->V3, Brannan V3->V4, Zoe V8->V9. The party boundaries have the
    # neighbours' walls instead and get no kerb.
    vb, fb = [], []
    for i, gaps in ((2, []), (3, [BRANNAN_GATE]), (8, [ZOE_GATE])):
        p, q = ring[i], ring[(i + 1) % len(ring)]
        # inward normal: toward the ring's centroid side
        du, dv = q[0] - p[0], q[1] - p[1]
        L = math.hypot(du, dv)
        nu, nv = -dv / L, du / L
        mid = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        if not point_in_ring(ring, (mid[0] + nu * 0.5, mid[1] + nv * 0.5)):
            nu, nv = -nu, -nv
        for a, b in edge_runs(p, q, gaps):
            poly = [a, b,
                    (b[0] + nu * KERB_W, b[1] + nv * KERB_W),
                    (a[0] + nu * KERB_W, a[1] + nv * KERB_W)]
            add_prism(vb, fb, poly, Z_PLATE_TOP - 0.06, Z_KERB)
    objs.append(bevel(new_mesh("kerb", vb, fb, [mats["Toy_trim"]]), width=0.05,
                      segments=1, thin=KERB_W))

    # 3 ----------------------------------------------------- the concrete patch
    # One panel of newer, lighter slab in the eastern belly — the only piece of
    # surface texture this asset is allowed (style bible s.6).
    vb, fb = [], []
    box_uv(vb, fb, 4.0, 13.0, -7.0, -1.0, 0.06, Z_PATCH)
    # Toy_sand, not Toy_trim: against a Toy_stone plate the trim white read as a
    # hole punched in the slab rather than as newer concrete.
    objs.append(new_mesh("patch", vb, fb, [mats["Toy_sand"]]))

    # 4 ------------------------------------------------------------- striping
    vb, fb = [], []
    nlines = 0
    for name, r in ROWS.items():
        half = STRIPE_W / 2.0
        if r["kind"] == "parallel":
            for t in stripe_lines(name):
                box_uv(vb, fb, r["u0"], r["u1"], t - half, t + half, Z_BURY, Z_STRIPE)
                nlines += 1
            continue
        if r["along"] == "v":
            far = r["far_u"]
            near = far - r["head"][0] * BAY_D
            u0, u1 = min(far, near), max(far, near)
            for t in stripe_lines(name):
                box_uv(vb, fb, u0, u1, t - half, t + half, Z_BURY, Z_STRIPE)
                nlines += 1
        else:
            far = r["far_v"]
            near = far - r["head"][1] * BAY_D
            v0, v1 = min(far, near), max(far, near)
            for t in stripe_lines(name):
                box_uv(vb, fb, t - half, t + half, v0, v1, Z_BURY, Z_STRIPE)
                nlines += 1
    # Direction arrows: the spine aisle runs from the Brannan gate toward the
    # belly, the cross-aisle from the belly out at Zoe. Without them the middle
    # of this lot is 700 m2 of blank slab, which style bible s.13 forbids.
    # in at Brannan, up the spine aisle, round the belly, out at Zoe — with a
    # return lane against the south-west party wall, which is what the 6.6 m the
    # spine's bay module leaves over is actually for.
    for au, av, du, dv in ((9.70, 33.0, 0.0, -1.0), (9.70, 6.0, 0.0, -1.0),
                           (9.70, -18.0, 0.0, -1.0), (-6.0, -21.4, -1.0, 0.0),
                           (-18.0, -21.4, -1.0, 0.0), (-2.10, -1.0, 0.0, 1.0),
                           (-2.10, 14.0, 0.0, 1.0)):
        oriented_box(vb, fb, au + du * 0.30, av + dv * 0.30, du, dv,
                     2.60, 0.30, Z_BURY, Z_STRIPE)
        for sgn in (1, -1):
            ang = math.radians(38.0 * sgn)
            bu = du * math.cos(ang) - dv * math.sin(ang)
            bv = du * math.sin(ang) + dv * math.cos(ang)
            oriented_box(vb, fb, au + du * 1.30 - bu * 0.45, av + dv * 1.30 - bv * 0.45,
                         bu, bv, 1.10, 0.28, Z_BURY, Z_STRIPE)
    objs.append(new_mesh("striping", vb, fb, [mats["Toy_mustard"]]))
    counts["stripe lines"] = nlines

    # 5 ---------------------------------------------------------- wheel stops
    vb, fb = [], []
    nstops = 0
    for name in ("R", "C1", "C2", "Z"):
        r = ROWS[name]
        hu, hv = r["head"]
        for k in row_bays(name):
            uc, vc = bay_centre(name, k)
            if r["along"] == "v":
                su = r["far_u"] - hu * 0.85
                oriented_box(vb, fb, su, vc, 0.0, 1.0, STOP_L, STOP_W, Z_BURY, Z_STOP)
            else:
                sv = r["far_v"] - hv * 0.85
                oriented_box(vb, fb, uc, sv, 1.0, 0.0, STOP_L, STOP_W, Z_BURY, Z_STOP)
            nstops += 1
    objs.append(new_mesh("wheel_stops", vb, fb, [mats["Toy_ink"]]))
    counts["wheel stops"] = nstops

    # 6 ------------------------------------------------------------- the fence
    # Posts + top rail + a 1.05 m mesh band + a barbed strand. The band stops at
    # 1.25 m deliberately: a full-height opaque panel walls the lot in, and a
    # chain-link fence has to read as a LINE from the app's aerial camera, not as
    # a surface. Contract forbids alpha and textures, so this is the honest
    # translation (style bible s.4, s.13).
    gaps_for = {3: [BRANNAN_GATE], 8: [ZOE_GATE]}
    posts_v, posts_f = [], []
    band_v, band_f = [], []
    rail_v, rail_f = [], []
    barb_v, barb_f = [], []
    nposts = 0
    for i in range(len(ring)):
        p, q = ring[i], ring[(i + 1) % len(ring)]
        du, dv = q[0] - p[0], q[1] - p[1]
        L = math.hypot(du, dv)
        if L < 0.5:
            continue
        ux, vx = du / L, dv / L
        for a, b in edge_runs(p, q, gaps_for.get(i, [])):
            RL = math.hypot(b[0] - a[0], b[1] - a[1])
            mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            oriented_box(band_v, band_f, mid[0], mid[1], ux, vx, RL, MESH_T, MESH_LO, MESH_HI)
            oriented_box(rail_v, rail_f, mid[0], mid[1], ux, vx, RL, RAIL_T, RAIL_LO, RAIL_HI)
            oriented_box(rail_v, rail_f, mid[0], mid[1], ux, vx, RL, MID_T, MID_LO, MID_HI)
            oriented_box(barb_v, barb_f, mid[0], mid[1], ux, vx, RL, BARB_T, BARB_LO, BARB_HI)
            n = max(1, int(round(RL / FENCE_PITCH)))
            for s in range(n + 1):
                f = s / n
                pu = a[0] + (b[0] - a[0]) * f
                pv = a[1] + (b[1] - a[1]) * f
                box_uv(posts_v, posts_f, pu - FENCE_POST / 2, pu + FENCE_POST / 2,
                       pv - FENCE_POST / 2, pv + FENCE_POST / 2, Z_BURY, FENCE_H)
                nposts += 1
    # No bevel on the posts: 93 boxes x 27 triangles of chamfer on a 90 mm
    # section is 2,500 triangles and ~5,000 flat-shaded vertices spent on an
    # edge that is sub-pixel at every distance the app renders this from. That
    # is a fifth of the whole asset's file size for nothing (see optimize/).
    objs.append(new_mesh("fence_posts", posts_v, posts_f, [mats["Toy_steel"]]))
    objs.append(new_mesh("fence_mesh", band_v, band_f, [mats["Toy_steel"]]))
    objs.append(new_mesh("fence_rail", rail_v, rail_f, [mats["Toy_steel"]]))
    objs.append(new_mesh("fence_barb", barb_v, barb_f, [mats["Toy_ink"]]))
    counts["fence posts"] = nposts

    # 7 --------------------------------------------------------------- gates
    vb, fb = [], []
    # Brannan: a rolling leaf parked open, stacked against the fence beside the
    # opening — which is how this gate stands in every photograph of the lot.
    oriented_box(vb, fb, (12.60 + 18.00) / 2, 43.85, 1.0, 0.0, 5.40, 0.10, 0.25, 2.05)
    # Zoe: one swing leaf standing 30 deg into the lot from its hinge.
    ang = math.radians(30.0)
    du, dv = math.sin(ang), -math.cos(ang)
    hinge = (-28.45, -27.30)
    oriented_box(vb, fb, hinge[0] + du * 1.80, hinge[1] + dv * 1.80, du, dv,
                 3.60, 0.10, 0.25, 2.05)
    objs.append(new_mesh("gates", vb, fb, [mats["Toy_steel"]]))

    # 8 ------------------------------------------- the PUBLIC PARKING pole sign
    # The lot's identity, and the one place semantic exaggeration is spent
    # (style bible s.8). Enlarged ~25% over the real board so it survives at
    # thumbnail size, and pulled ~2 m inside the fence because the real pole
    # stands in the public right of way, which this asset does not own.
    su, sv = SIGN_UV
    vb, fb = [], []
    box_uv(vb, fb, su - SIGN_POST / 2, su + SIGN_POST / 2,
           sv - SIGN_POST / 2, sv + SIGN_POST / 2, Z_BURY, SIGN_TOP)
    objs.append(bevel(new_mesh("sign_post", vb, fb, [mats["Toy_steel"]]),
                      width=0.04, segments=1, thin=SIGN_POST))

    hb = SIGN_BOARD_W / 2
    bt = SIGN_BOARD_T / 2
    vb, fb = [], []
    box_uv(vb, fb, su - hb, su + hb, sv - bt, sv + bt, SIGN_BOARD_LO, SIGN_BOARD_HI - 0.34)
    objs.append(bevel(new_mesh("sign_field", vb, fb, [mats["Toy_red"]]),
                      width=0.06, segments=2, thin=SIGN_BOARD_T))
    vb, fb = [], []
    box_uv(vb, fb, su - hb, su + hb, sv - bt, sv + bt, SIGN_BOARD_HI - 0.34, SIGN_BOARD_HI)
    objs.append(bevel(new_mesh("sign_band", vb, fb, [mats["Toy_white"]]),
                      width=0.06, segments=2, thin=SIGN_BOARD_T))
    vb, fb = [], []
    box_uv(vb, fb, su - hb, su + hb, sv - bt, sv + bt, SIGN_BOARD_HI, SIGN_BOARD_HI + 0.30)
    objs.append(bevel(new_mesh("sign_header", vb, fb, [mats["Toy_ink"]]),
                      width=0.05, segments=1, thin=SIGN_BOARD_T))

    # Glow shells: thin plates 20 mm PROUD of the board's Brannan face only.
    # Not closed boxes around the whole board — the app draws _Glow in a separate
    # unlit layer at opacity 0.12 + 0.95*uNight, and a closed shell is two alpha
    # layers, i.e. ~23% by day, which would tint the board in daylight.
    vb, fb = [], []
    box_uv(vb, fb, su - hb + 0.05, su + hb - 0.05, sv + bt, sv + bt + 0.02,
           SIGN_BOARD_LO + 0.08, SIGN_BOARD_HI - 0.40)
    objs.append(new_mesh("sign_field_glow", vb, fb, [mats["Toy_red_Glow"]]))
    vb, fb = [], []
    box_uv(vb, fb, su - hb + 0.05, su + hb - 0.05, sv + bt, sv + bt + 0.02,
           SIGN_BOARD_HI - 0.30, SIGN_BOARD_HI - 0.04)
    objs.append(new_mesh("sign_band_glow", vb, fb, [mats["Toy_white_Glow"]]))

    # 9 ------------------------------------------------- the attendant's booth
    bu, bv = site["features"]["booth"]
    vb, fb = [], []
    box_uv(vb, fb, bu - BOOTH_W / 2, bu + BOOTH_W / 2, bv - BOOTH_L / 2, bv + BOOTH_L / 2,
           Z_BURY, BOOTH_H)
    objs.append(bevel(new_mesh("booth", vb, fb, [mats["Toy_cream"]]), width=0.10, segments=2))
    vb, fb = [], []
    box_uv(vb, fb, bu - BOOTH_W / 2 - 0.25, bu + BOOTH_W / 2 + 0.25,
           bv - BOOTH_L / 2 - 0.25, bv + BOOTH_L / 2 + 0.25, BOOTH_H, BOOTH_RIDGE)
    objs.append(bevel(new_mesh("booth_roof", vb, fb, [mats["Toy_ink"]]), width=0.08, segments=2))
    vb, fb = [], []
    box_uv(vb, fb, bu - BOOTH_W / 2 - 0.03, bu - BOOTH_W / 2 + 0.03,
           bv - 1.10, bv + 1.10, 1.10, 1.95)
    objs.append(new_mesh("booth_window", vb, fb, [mats["Toy_glass"]]))
    vb, fb = [], []
    box_uv(vb, fb, bu - BOOTH_W / 2 - 0.06, bu - BOOTH_W / 2 - 0.04,
           bv - 1.02, bv + 1.02, 1.16, 1.89)
    objs.append(new_mesh("booth_window_glow", vb, fb, [mats["Toy_trim_Glow"]]))

    # 10 ------------------------------------------------------- the box trailer
    tu, tv = site["features"]["trailer"]
    vb, fb = [], []
    box_uv(vb, fb, tu - TRAILER_W / 2, tu + TRAILER_W / 2,
           tv - TRAILER_L / 2, tv + TRAILER_L / 2, 0.20, 0.60)
    objs.append(bevel(new_mesh("trailer_chassis", vb, fb, [mats["Toy_ink"]]),
                      width=0.06, segments=1, thin=0.40))
    vb, fb = [], []
    box_uv(vb, fb, tu - TRAILER_W / 2, tu + TRAILER_W / 2,
           tv - TRAILER_L / 2, tv + TRAILER_L / 2 - 0.4, 0.60, 3.00)
    objs.append(bevel(new_mesh("trailer_box", vb, fb, [mats["Toy_white"]]),
                      width=0.10, segments=2))

    # 11 ----------------------------------------------------------- lot lights
    pole_v, pole_f = [], []
    head_v, head_f = [], []
    glow_v, glow_f = [], []
    for lu, lv in LAMP_UV:
        box_uv(pole_v, pole_f, lu - 0.07, lu + 0.07, lv - 0.07, lv + 0.07, Z_BURY, LAMP_H)
        box_uv(head_v, head_f, lu - 0.25, lu + 0.65, lv - 0.25, lv + 0.25,
               LAMP_H - 0.22, LAMP_H)
        box_uv(glow_v, glow_f, lu - 0.20, lu + 0.60, lv - 0.20, lv + 0.20,
               LAMP_H - 0.25, LAMP_H - 0.23)
    objs.append(bevel(new_mesh("lamp_poles", pole_v, pole_f, [mats["Toy_steel"]]),
                      width=0.03, segments=1, thin=0.14))
    objs.append(bevel(new_mesh("lamp_heads", head_v, head_f, [mats["Toy_ink"]]),
                      width=0.05, segments=1, thin=0.22))
    objs.append(new_mesh("lamp_glow", glow_v, glow_f, [mats["Toy_gold_Glow"]]))

    # 12 ---------------------------------------------------------- parked cars
    by_mat = {}
    cabin_v, cabin_f = [], []
    for idx, (row, k, kind, colour) in enumerate(CARS):
        r = ROWS[row]
        L, W, z0, z1, cl, cw, cz = BODIES[kind]
        uc, vc = bay_centre(row, k)
        if r["kind"] == "parallel":
            du, dv = 0.0, 1.0
            cu, cv = uc, vc
        else:
            du, dv = r["head"]
            if r["along"] == "v":
                cu = r["far_u"] - du * (0.55 + L / 2.0)
                cv = vc
            else:
                cu = uc
                cv = r["far_v"] - dv * (0.55 + L / 2.0)
        # +/- 4% of length of nose-in slop and up to 3 deg of yaw, hashed off the
        # car index so it is reproducible and shows up in a diff, never random.
        jitter = (hash01(idx * 7 + 1) - 0.5) * 0.30
        cu += du * jitter
        cv += dv * jitter
        yaw = math.radians((hash01(idx * 13 + 5) - 0.5) * 6.0)
        cy, sy = math.cos(yaw), math.sin(yaw)
        dux, dvx = du * cy - dv * sy, du * sy + dv * cy
        vb, fb = by_mat.setdefault(colour, ([], []))
        oriented_box(vb, fb, cu, cv, dux, dvx, L, W, z0, z1)
        oriented_box(cabin_v, cabin_f, cu - dux * L * 0.06, cv - dvx * L * 0.06,
                     dux, dvx, cl, cw, z1, cz)
    for colour, (vb, fb) in sorted(by_mat.items()):
        objs.append(bevel(new_mesh(f"cars_{colour[4:].lower()}", vb, fb, [mats[colour]]),
                          width=0.11, segments=2, thin=1.6))
    objs.append(bevel(new_mesh("car_cabins", cabin_v, cabin_f, [mats["Toy_glass"]]),
                      width=0.08, segments=1, thin=1.4))
    counts["cars"] = len(CARS)

    # 13 ------------------------------------------------------------- greenery
    # The thicket measured at (u -2.0, v -30.8) straddles the parcel line into
    # the private lot next door, so it is pulled wholly inside the boundary;
    # REPORT.md records the move. The Brannan-corner shrub is inside as measured.
    crown_v, crown_f = [], []
    trunk_v, trunk_f = [], []
    thicket = [(-10.60, -31.40, 2.40, 3.90), (-8.30, -29.60, 1.90, 3.10),
               (-11.90, -28.90, 1.65, 2.60)]
    for i, (cu, cv, r, h) in enumerate(thicket):
        frustum(trunk_v, trunk_f, 6, cu, cv, 0.22, 0.16, Z_BURY, h * 0.38)
        cone_ring(crown_v, crown_f, 10, cu, cv,
                  [r * 0.58, r * 0.95, r, r * 0.82, r * 0.40],
                  [h * 0.32, h * 0.48, h * 0.64, h * 0.84, h])
    su_, sv_ = 4.60, 42.40
    frustum(trunk_v, trunk_f, 6, su_, sv_, 0.24, 0.17, Z_BURY, 1.30)
    cone_ring(crown_v, crown_f, 10, su_, sv_,
              [1.05, 1.70, 1.85, 1.50, 0.70], [1.18, 1.85, 2.50, 3.20, 3.70])
    objs.append(new_mesh("crowns", crown_v, crown_f, [mats["Toy_verdigris"]]))
    objs.append(new_mesh("trunks", trunk_v, trunk_f, [mats["Toy_rust"]]))

    return objs, counts


# ---------------------------------------------------------------------- shell


def clear_scene():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = here
    if "--out" in argv:
        out_dir = os.path.abspath(argv[argv.index("--out") + 1])
    os.makedirs(out_dir, exist_ok=True)

    site = json.load(open(os.path.join(here, "data", "site_uv.json")))
    global TERRAIN
    TERRAIN = Terrain(json.load(open(os.path.join(here, "data", "terrain_uv.json"))))

    clear_scene()
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0

    mats = make_materials()
    objs, counts = build(site, mats)

    # NO normalization. Both of the usual moves are wrong for a draped asset:
    #   * re-centring x/y on the model's own bounding box would slide the lot
    #     across the city, because the sign and the crowns overhang asymmetrically.
    #     The authored origin is already the parcel's bbox centre, which is what
    #     the manifest anchor means.
    #   * shifting z so min_z = 0 would break the drape. assets.js puts the GLB's
    #     z = 0 plane at the anchor's terrain elevation, and this model's z = 0 IS
    #     the anchor's ground: TERRAIN(0, 0) = 0 by construction. Lifting until
    #     the lowest point reached zero would float the Brannan end 1.1 m — the
    #     failure the drape exists to fix, reintroduced from the other side.
    bpy.context.view_layer.update()
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    tris = 0
    dg = bpy.context.evaluated_depsgraph_get()
    mn = [1e9] * 3
    mx = [-1e9] * 3
    per_obj = []
    for o in objs:
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        t = len(me.loop_triangles)
        tris += t
        per_obj.append((o.name, t))
        for vert in me.vertices:
            w = o.matrix_world @ vert.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
        ev.to_mesh_clear()

    extent = mx[2] - mn[2]
    stalls = sum(len(row_bays(r)) for r in ROWS)
    print("objects         %d" % len(objs))
    for name, t in sorted(per_obj, key=lambda p: -p[1]):
        print("   %-22s %6d" % (name, t))
    for k, v in counts.items():
        print("%-15s %d" % (k, v))
    print("stalls          %d  (permit says 60)" % stalls)
    print("triangles       %d / %d" % (tris, TRI_CAP))
    print("dims            %.4f x %.4f x %.4f" % tuple(mx[i] - mn[i] for i in range(3)))
    print("min z           %.6f  (the Zoe end, below the anchor's ground)" % mn[2])
    print("max z           %.6f  (the PUBLIC PARKING sign)" % mx[2])
    print("terrain fall    %.4f   plane residual %.4f" % (TERRAIN.fall, TERRAIN.residual))
    print("centre xy       %.6f %.6f" % ((mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2))
    print("VERTICAL EXTENT %.4f  <- this is targetHeightM, so the loader scale is 1.0"
          % extent)
    if tris > TRI_CAP:
        print("!! OVER TRIANGLE CAP")
    if stalls != 60:
        print("!! STALL COUNT IS NOT 60")

    blend = os.path.join(out_dir, "424-brannan.blend")
    glb = os.path.join(out_dir, "424-brannan.glb")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    for o in bpy.data.objects:
        o.select_set(o in objs)
    bpy.ops.export_scene.gltf(
        filepath=glb, export_format="GLB", use_selection=True, export_apply=True,
        export_cameras=False, export_lights=False, export_yup=True,
    )
    print("wrote", blend)
    print("wrote", glb)


if __name__ == "__main__":
    main()
