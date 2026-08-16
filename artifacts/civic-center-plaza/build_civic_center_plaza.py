"""Deterministic Blender build of the SF-SIM miniature Civic Center Plaza.

    blender -b --python build_civic_center_plaza.py -- [--out DIR]

Writes civic-center-plaza.blend and civic-center-plaza.glb next to this file
(or into --out). Geometry is authored in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = plaza OBB centre (anchor lon -122.4176170,
lat 37.7794913), min Z = 0, US flagpole finial exactly 30.48 m.

Design (see REFERENCE.md for the sources behind every number):

* the 5.06-acre formal plaza east of City Hall, Douglas Baylis's 1956-58
  Modernist re-cut of John Galen Howard's 1911 Beaux-Arts plaza, sitting on the
  roof of a three-storey 1960 parking garage and Brooks Hall;
* the recognition rests on GROUND PATTERN and REPEATED RHYTHM, not massing:
  two dense bosques of pollarded London planes flanking a central east-west
  court on the Fulton axis, four crisp lawn panels, and two rows of nine
  historic flagpoles reading as a colonnade of masts;
* 190 tree positions, 35 flagpole positions and every polygon in this file are
  MEASURED from OSM (data/plaza_uv.json) and reprojected into the plaza frame.
  The row jitter is real survey jitter — do not straighten it, it is what keeps
  the bosques from reading as procedural;
* everything is a closed solid with real thickness stacked in Z (deck 0.30,
  joints 0.32, gravel 0.34, walks 0.36, playgrounds 0.42, lawns 0.45) so that
  nothing is coplanar with anything else and nothing z-fights the baked
  landcover, which sits at +0.06 m above terrain;
* night state: the walk grid is the hero glow — at night the plaza reads as a
  lit orthogonal grid drawn on a dark field, which is what the real place does.
  Lawns and bosques go dark. Glow surfaces are thin shells proud of the opaque
  slab beneath them; the app renders _Glow at ~12% alpha by day, so a primary
  surface must never be authored as glow.

Authoring frame: geometry is laid out in the plaza's local (u, v) frame —
u along the long axis, POSITIVE TOWARD THE SOUTH (Grove Street), bearing
170.94 deg true; v across, POSITIVE TOWARD THE WEST (City Hall), bearing
260.94 deg — and mapped to world x/y by to_world(). The plaza sits 9.06 deg off
the world axes, so the axis-aligned XY bounding box is ~146.6 x 192.4 m even
though the plaza is 177.9 x 121.5 m. That is expected, not a scale error.
"""

import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# Heading of the plaza's long axis, from the minimum-area oriented bounding box
# over OSM way 284764947. The Civic Center street grid runs the same 9.06 deg,
# which is why every lawn and walk in the measured data shares it.
#
# The grid leans 9.06 deg EAST of north, so the axis toward Grove Street (south)
# bears 170.94 deg (= 180 - 9.06), not 189.06 (= 180 + 9.06). Those two are
# mirror images about north and both "look like 9.06 deg off the axes" in any
# bounding-box check, which is why the first build shipped the wrong one: the
# plaza came out rotated 18.12 deg from the block it sits on, visibly crooked
# against City Hall while every measurement in the report still read 9.06 deg.
# The AABB cannot catch this; only a SIGNED angle can. Ground truth: 109 of the
# 166 baked DataSF footprints over 200 m2 in cells 19_13 + 19_14 sit at +9 deg
# in this convention and none at -9, and the neighbouring landmark GLBs (City
# Hall 9.62, Main Library 9.06, Bill Graham 9.31, 234 Van Ness 10.27) agree.
HEADING_LONG = 170.94   # +u, toward Grove Street (south)
HEADING_CROSS = 260.94  # +v, toward City Hall (west)

_UL = math.radians(HEADING_LONG)
U_DIR = (math.sin(_UL), math.cos(_UL))
# +v points WEST, toward City Hall, which is how data/plaza_uv.json defines it.
# That makes (u, v) a LEFT-handed frame in world (x east, y north) — the first
# build used (-U_DIR[1], U_DIR[0]) here to keep the map right-handed, which
# silently MIRRORED the whole plaza east-west: the playgrounds came out on the
# City Hall side instead of the Larkin side. Caught in the first top render.
# The mirror is fixed here; the winding it was compensating for is fixed in
# orient_for_world() and ngon_uv().
V_DIR = (U_DIR[1], -U_DIR[0])

# Z stack. Every level is a distinct closed solid; the gaps are deliberate and
# are what keeps the model free of coplanar surfaces.
Z_DECK = 0.30       # plaza deck top — the plaza is a raised deck, not grade
Z_JOINT = 0.32      # scored paving joints
Z_GRAVEL = 0.34     # the fine-gravel central court
Z_WALK = 0.36       # concrete walks, proud of the field paving
Z_PLAY = 0.42       # playground pads
Z_LAWN = 0.45       # lawn panels, kerbed

Z_FLAG_HISTORIC = 15.24   # 50 ft, OSM tag on all 18 Pavilion of American Flags poles
Z_FLAG_PRIDE = 9.00       # untagged; inferred from photography as ~30 ft
Z_FLAG_US = 30.48         # 100 ft — THE HEIGHT DATUM. See REFERENCE.md / plan 2.15.
                          # targetHeightM scales the whole 178 m plaza off this
                          # one pole, so it is asserted in the validator.

# Pollarded London plane. OSM tags all 190 trees height=4.5, which is a bulk
# default, not a survey (plan 2.15 risk 2). Pollarded planes of this age in this
# plaza read at 10-12 m; 11.0 m is the modelled crest.
# The trunk must reach INTO the crown. Authored first with the trunk stopping
# at 3.55 m and the crown starting at 7.55 m, which put a 4 m gap of bare pole
# under every tree and made the bosques read as crowns floating over stumps in
# the north elevation. A pollard is a stout trunk that ends in the crown, not a
# lollipop stick.
TREE_TRUNK_R = 0.38
TREE_TRUNK_TOP = 5.40
TREE_CROWN_LO = 4.90
TREE_CROWN_HI = 11.00
# Wider than deep, and wider than the 3.2 m row spacing on purpose: the crowns
# interpenetrate into one continuous canopy slab, which is what a bosque is and
# what makes the two green masses read at the app's camera distance.
TREE_CROWN_R_LO = 3.30
TREE_CROWN_R_HI = 2.55
TREE_JITTER = 0.06        # +/- 6% scale, hashed off the tree index, never random

TRI_CAP = 18000

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",      # deck plate, field paving, kerb
    "Toy_cream": "f2ede3",      # walks — a half-tone lighter, so the grid reads
    "Toy_sand": "ece4d4",       # the gravel court
    "Toy_mint": "8fd0a8",       # lawn panels
    "Toy_verdigris": "9fb8a8",  # tree crowns — greyer than the lawns on purpose,
                                # so the bosques separate from the grass from above
    "Toy_steel": "9aa0a6",      # flagpoles, railings, lamp poles, and the
                                # tree trunks: London plane bark is pale mottled
                                # grey-cream, and 190 orange-brown trunks were
                                # competing with the playground accents
    "Toy_gold": "caa64a",       # pole finials
    "Toy_red": "c4453c",        # flags
    "Toy_navy": "2c4a70",       # flags
    "Toy_white": "f7f4ec",      # flags
    "Toy_coral": "e8735a",      # playground N accent
    "Toy_teal": "3fa8a0",       # playground S accent
    "Toy_trim": "f3efe6",       # kiosk walls
    "Toy_roofd": "45454a",      # kiosk roofs, bench slats
    "Toy_ink": "3a3530",        # scored joints, contact-shadow edges
    "Toy_cream_Glow": "f2ede3",  # the lit walk grid — the hero night state
    "Toy_gold_Glow": "caa64a",   # the floodlit US flagpole (OSM lit=yes)
    "Toy_coral_Glow": "e8735a",  # playground N
    "Toy_teal_Glow": "3fa8a0",   # playground S
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
    scatter (pipeline/lib/geo.mjs), so 'random' variation here is reproducible
    across rebuilds and reviewable in a diff."""
    h = (n ^ 0x9E3779B9) * 0x85EBCA6B & 0xFFFFFFFF
    h = (h ^ (h >> 13)) * 0xC2B2AE35 & 0xFFFFFFFF
    h ^= h >> 16
    return (h & 0xFFFFFFFF) / 4294967296.0


# ----------------------------------------------------------------- transforms


def to_world(u, v):
    """Plaza frame -> world (x east, y north). Right-handed, so a CCW polygon in
    (u, v) stays CCW in (x, y) and outward normals stay outward."""
    return (u * U_DIR[0] + v * V_DIR[0], u * U_DIR[1] + v * V_DIR[1])


def rect_uv(u0, u1, v0, v1):
    """CCW rectangle in the plaza frame."""
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]


def orient_for_world(poly):
    """Order a plaza-frame ring so that it comes out COUNTER-clockwise in world
    space, which is what makes prism_verts_faces' caps face outward.

    The (u, v) frame is left-handed in world (see V_DIR), so a ring that is CCW
    in (u, v) is CW in world. The test is therefore inverted: keep the ring whose
    (u, v) shoelace is NEGATIVE. OSM rings arrive in either winding, so every
    polygon goes through here."""
    a = 0.0
    for i in range(len(poly)):
        u0, v0 = poly[i]
        u1, v1 = poly[(i + 1) % len(poly)]
        a += u0 * v1 - u1 * v0
    return poly if a < 0 else poly[::-1]


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
    a third of the object's thinnest dimension: most of this asset is 20-150 mm
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


def prism_verts_faces(poly_uv, z0, z1, base_index=0):
    """Closed extrusion of a plaza-frame polygon: walls + both caps. Orients the
    ring itself, so every caller (including box() and the fence rails, which do
    not go through prism_uv) gets outward normals."""
    poly = [to_world(u, v) for u, v in orient_for_world(poly_uv)]
    n = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    b = base_index
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((b + i, b + j, b + n + j, b + n + i))
    faces.append(tuple(b + i for i in range(n - 1, -1, -1)))
    faces.append(tuple(b + i for i in range(n, 2 * n)))
    return verts, faces


def prism_uv(name, poly_uv, z0, z1, mat, mat_top=None):
    verts, faces = prism_verts_faces(dedupe_ring(poly_uv), z0, z1)
    face_mats = [0] * (len(faces) - 1) + [1 if mat_top else 0]
    mats = [mat, mat_top] if mat_top else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def ribbon_uv(name, a, b, width, z0, z1, mat):
    """A straight paving band from (u,v) a to b. Every walk in the measured data
    is straight to within a metre over its whole length, so one box per walk is
    both accurate and 4x cheaper than segment-by-segment."""
    du, dv = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(du, dv)
    if ln < 1e-6:
        return None
    nu, nv = -dv / ln * width / 2.0, du / ln * width / 2.0
    poly = [
        (a[0] + nu, a[1] + nv),
        (b[0] + nu, b[1] + nv),
        (b[0] - nu, b[1] - nv),
        (a[0] - nu, a[1] - nv),
    ]
    return prism_uv(name, poly, z0, z1, mat)


def ngon_uv(nsides, uc, vc, r, rot=0.0):
    """Emitted CLOCKWISE in (u, v), which is counter-clockwise in world — see
    orient_for_world(). frustum() relies on this for its cap winding."""
    return [
        (
            uc + r * math.cos(rot - 2 * math.pi * i / nsides),
            vc + r * math.sin(rot - 2 * math.pi * i / nsides),
        )
        for i in range(nsides)
    ]


def frustum(bm_verts, bm_faces, nsides, uc, vc, r0, r1, z0, z1, rot=0.0):
    """Append a closed n-sided frustum to a running vertex/face buffer. Used for
    the 190 trees and the 35 flagpoles, which are built into single merged
    objects to keep the loader's draw-call merge cheap."""
    b = len(bm_verts)
    lo = ngon_uv(nsides, uc, vc, r0, rot)
    hi = ngon_uv(nsides, uc, vc, r1, rot)
    bm_verts.extend([to_world(u, v) + (z0,) for u, v in lo])
    bm_verts.extend([to_world(u, v) + (z1,) for u, v in hi])
    for i in range(nsides):
        j = (i + 1) % nsides
        bm_faces.append((b + i, b + j, b + nsides + j, b + nsides + i))
    bm_faces.append(tuple(b + i for i in range(nsides - 1, -1, -1)))
    bm_faces.append(tuple(b + nsides + i for i in range(nsides)))


def box(bm_verts, bm_faces, u0, u1, v0, v1, z0, z1):
    b = len(bm_verts)
    poly = rect_uv(u0, u1, v0, v1)
    verts, faces = prism_verts_faces(poly, z0, z1, base_index=b)
    bm_verts.extend(verts)
    bm_faces.extend(faces)


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


# ------------------------------------------------------------------ measured data


def load_data():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "data", "plaza_uv.json"), "r", encoding="utf8") as fh:
        return json.load(fh)


# Walk widths, metres. Keyed by the OSM way id in data/plaza_uv.json["walks"].
# The four long east-west allee walks are the plaza's primary circulation and
# are the widest; the short cross links between lawn panels are minor.
WALK_WIDTH = {
    "32865611": 4.5, "32865635": 4.5, "32865664": 4.5, "32865680": 4.5,   # allees
    "128534075": 5.5, "776062395": 5.5, "776062396": 5.5, "776062397": 5.5,  # perimeter
    "33790683": 4.0, "33790686": 4.0, "33790699": 4.0, "33790703": 4.0,   # cross links
    "941346737": 3.0, "941346738": 3.0, "941346739": 3.0, "941346740": 3.0,
    "941346741": 3.0, "941346742": 3.0, "941346743": 3.0, "941346744": 3.0,
    "941346745": 3.0, "941346746": 3.0,
}

# The perimeter-walk rectangle. The scored joint grid and the lamp posts live
# inside it so nothing runs out over the plaza's chamfered corners.
INNER_U0, INNER_U1 = -78.0, 83.8
INNER_V0, INNER_V1 = -48.9, 55.1


# --------------------------------------------------------------------- build


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene
    mats = {name: make_material(name) for name in PALETTE_HEX}
    data = load_data()

    ground(data, mats)
    trees(data, mats)
    flagpoles(data, mats)
    playgrounds(data, mats)
    kiosks(data, mats)
    furniture(mats)
    people(mats)

    # Bevel budget. A 0.12/2 bevel multiplies a box's triangle count by ~9, so
    # it is spent only where it buys something: the chunky single solids that
    # carry the miniature read at the app's camera distance. The merged
    # multi-solid objects (190 trees, 35 poles, 28 lamp parts, 20 figures, the
    # fences and benches) are each built from dozens of small primitives whose
    # bevels would cost 20k triangles for detail under one pixel; their tapered
    # profiles already read as soft. The paving slabs are 20-150 mm thick and
    # take a token 0.05/1 softening so their kerb edges still catch a highlight.
    UNBEVELLED = {"trees", "flagpoles", "lamps", "benches", "planters", "people"}
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        # "_glow" anywhere in the name, not just at the end: the playground
        # shells are called play_glow_playground_n/s, so an endswith() test let
        # them through and a 4-box lit frame came back as 432 triangles instead
        # of 48. Glow shells are thin coplanar-ish slabs and must never be
        # bevelled.
        if obj.name in UNBEVELLED or "_glow" in obj.name:
            continue
        if obj.name.startswith(("play_fence", "play_kit")):
            continue
        if obj.name.startswith(("walk_", "joint_", "lawn_", "gravel", "play_pad")):
            bevel(obj, width=0.05, segments=1)
        else:
            bevel(obj, width=0.12, segments=2)

    recentre()
    return scene


def ground(data, mats):
    """The deck plate, the scored joint grid, the walks, the gravel court and
    the six lawn panels. Two thirds of this asset is paving, so the paving has
    to be designed rather than left as a blank slab (style bible s.13)."""
    prism_uv("deck", data["ring"], 0.0, Z_DECK, mats["Toy_stone"])

    # Scored joints on a 14 m grid, 0.25 m wide, 20 mm proud so they read as a
    # dark line from the air and disappear under everything stacked above them.
    step = 14.0
    n = 0
    u = INNER_U0 + step
    while u < INNER_U1 - 1.0:
        ribbon_uv(f"joint_u{n}", (u, INNER_V0), (u, INNER_V1), 0.25, Z_DECK, Z_JOINT, mats["Toy_ink"])
        u += step
        n += 1
    v = INNER_V0 + step
    while v < INNER_V1 - 1.0:
        ribbon_uv(f"joint_v{n}", (INNER_U0, v), (INNER_U1, v), 0.25, Z_DECK, Z_JOINT, mats["Toy_ink"])
        v += step
        n += 1

    for wid, pts in data["walks"].items():
        a, b = pts[0], pts[-1]
        w = WALK_WIDTH.get(wid, 3.0)
        ribbon_uv(f"walk_{wid}", a, b, w, Z_DECK, Z_WALK, mats["Toy_cream"])
        # Night: the walk grid is the hero glow. A thin shell inset from the
        # walk edge, proud of its opaque parent — never the parent itself.
        ribbon_uv(f"walk_{wid}_glow", a, b, w - 1.2, Z_WALK, Z_WALK + 0.02, mats["Toy_cream_Glow"])

    # The gravel court is one of the six shapes the top view has to resolve
    # (plan 2.9), but Toy_sand (ece4d4), Toy_cream (f2ede3) and Toy_stone
    # (d9d2c2) are all within ~6% of each other, so on the first aerial the
    # court melted into the surrounding paving. A dark kerb reads at any
    # distance and costs 48 triangles, which is the cheaper fix than pushing a
    # paving tone off-palette.
    court = orient_for_world(dedupe_ring(data["areas"]["gravel_court"]))
    cus = [p[0] for p in court]
    cvs = [p[1] for p in court]
    prism_uv("gravel_kerb",
             rect_uv(min(cus) - 0.45, max(cus) + 0.45, min(cvs) - 0.45, max(cvs) + 0.45),
             Z_DECK, Z_GRAVEL + 0.04, mats["Toy_ink"])
    prism_uv("gravel_court", data["areas"]["gravel_court"], Z_DECK, Z_GRAVEL + 0.06,
             mats["Toy_sand"])

    for key in (
        "lawn_nw", "lawn_n_centre", "lawn_ne_strip",
        "lawn_sw", "lawn_s_centre", "lawn_s_strip",
    ):
        prism_uv(key, data["areas"][key], Z_DECK, Z_LAWN, mats["Toy_mint"])


def trees(data, mats):
    """190 pollarded London planes at their measured positions, merged into one
    object. Pollarded planes are not lollipops: a stubby knuckled trunk under a
    wide, flat, tapered drum that reads as a continuous green slab from the air.
    Trunk and crown are separate material slots on one mesh."""
    verts, faces_trunk, faces_crown = [], [], []
    for idx, t in enumerate(data["trees"]):
        s = 1.0 + (hash01(idx) * 2.0 - 1.0) * TREE_JITTER
        rot = hash01(idx + 7919) * math.pi / 4.0
        u, v = t["u"], t["v"]

        before = len(faces_trunk) + len(faces_crown)
        buf = []
        frustum(verts, buf, 6, u, v, TREE_TRUNK_R * s, TREE_TRUNK_R * 0.84 * s,
                Z_DECK, TREE_TRUNK_TOP * s, rot)
        faces_trunk.extend(buf)
        buf = []
        frustum(verts, buf, 8, u, v, TREE_CROWN_R_LO * s, TREE_CROWN_R_HI * s,
                TREE_CROWN_LO * s, TREE_CROWN_HI * s, rot)
        faces_crown.extend(buf)
        assert len(faces_trunk) + len(faces_crown) > before

    faces = faces_trunk + faces_crown
    face_mats = [0] * len(faces_trunk) + [1] * len(faces_crown)
    new_mesh("trees", verts, faces, [mats["Toy_steel"], mats["Toy_verdigris"]], face_mats)


def flagpoles(data, mats):
    """The 18 Pavilion of American Flags poles (15.24 m, two rows of nine), the
    16 Pride poles at the McAllister and Grove entrances, and the 100 ft US
    flagpole that is this model's height datum. Flags are opaque three-colour
    slabs with no devices — the contract forbids transparency, and the real
    flags are a live political question this asset has no business answering
    (plan 2.15 risk 7)."""
    verts = []
    f_pole, f_gold, f_red, f_navy, f_white = [], [], [], [], []
    flag_bins = {"Toy_red": f_red, "Toy_navy": f_navy, "Toy_white": f_white}

    for idx, p in enumerate(data["flagpoles"]):
        u, v = p["u"], p["v"]
        if p["kind"] == "tall":
            top, r0, r1, base, fw, fh = Z_FLAG_US, 0.34, 0.20, 1.30, 4.4, 2.6
        elif p["kind"] == "historic":
            top, r0, r1, base, fw, fh = Z_FLAG_HISTORIC, 0.22, 0.14, 0.90, 2.6, 1.5
        else:
            top, r0, r1, base, fw, fh = Z_FLAG_PRIDE, 0.16, 0.11, 0.60, 1.8, 1.1

        buf = []
        box(verts, buf, u - base / 2, u + base / 2, v - base / 2, v + base / 2,
            Z_DECK, Z_DECK + 0.35)
        frustum(verts, buf, 6, u, v, r0, r1, Z_DECK + 0.35, top - 0.45)
        f_pole.extend(buf)

        buf = []
        frustum(verts, buf, 6, u, v, r1 * 1.5, r1 * 0.4, top - 0.45, top)
        f_gold.extend(buf)

        # The flag hangs on the +v (west) side of every pole, angled the same
        # way throughout: one breeze over the whole plaza reads as designed,
        # thirty-five independent breezes read as noise.
        buf = []
        box(verts, buf, u - fh / 2, u + fh / 2, v + r1, v + r1 + fw,
            top - 1.0 - fh, top - 1.0)
        colour = ("Toy_red", "Toy_navy", "Toy_white")[idx % 3]
        flag_bins[colour].extend(buf)

    faces = f_pole + f_gold + f_red + f_navy + f_white
    face_mats = (
        [0] * len(f_pole) + [1] * len(f_gold)
        + [2] * len(f_red) + [3] * len(f_navy) + [4] * len(f_white)
    )
    new_mesh(
        "flagpoles", verts, faces,
        [mats["Toy_steel"], mats["Toy_gold"], mats["Toy_red"], mats["Toy_navy"], mats["Toy_white"]],
        face_mats,
    )

    # The US pole is floodlit (OSM lit=yes on node 7797674733) — a glow band at
    # the top only, so the tallest thing on site still registers at night.
    us = next(p for p in data["flagpoles"] if p["kind"] == "tall")
    gv, gf = [], []
    frustum(gv, gf, 6, us["u"], us["v"], 0.26, 0.26, Z_FLAG_US - 3.2, Z_FLAG_US - 0.5)
    new_mesh("us_pole_glow", gv, gf, [mats["Toy_gold_Glow"]])


def playgrounds(data, mats):
    """The two Helen Diller Civic Center Playgrounds (Andrea Cochran, 2018) on
    the Larkin side. These carry the only saturated non-green colour in the
    composition, which makes them the plaza's storytelling anchor and the thing
    that stops the top view reading as a cemetery."""
    for key, accent, glow, sign in (
        ("playground_n", "Toy_coral", "Toy_coral_Glow", +1),
        ("playground_s", "Toy_teal", "Toy_teal_Glow", -1),
    ):
        ring = orient_for_world(dedupe_ring(data["areas"][key]))
        prism_uv(f"play_pad_{key}", ring, Z_DECK, Z_PLAY, mats[accent])

        us = [p[0] for p in ring]
        vs = [p[1] for p in ring]
        u0, u1, v0, v1 = min(us), max(us), min(vs), max(vs)
        uc, vc = (u0 + u1) / 2.0, (v0 + v1) / 2.0

        # Railing: a chamfered rail bar on posts. Pickets are invisible at the
        # app's camera distance and would cost more than the whole bosque.
        verts, faces = [], []
        for a, b in (((u0, v0), (u1, v0)), ((u1, v0), (u1, v1)),
                     ((u1, v1), (u0, v1)), ((u0, v1), (u0, v0))):
            du, dv = b[0] - a[0], b[1] - a[1]
            ln = math.hypot(du, dv)
            nu, nv = -dv / ln * 0.06, du / ln * 0.06
            poly = [(a[0] + nu, a[1] + nv), (b[0] + nu, b[1] + nv),
                    (b[0] - nu, b[1] - nv), (a[0] - nu, a[1] - nv)]
            v2, f2 = prism_verts_faces(poly, Z_PLAY + 0.75, Z_PLAY + 0.90, len(verts))
            verts.extend(v2)
            faces.extend(f2)
            for k in range(1, int(ln / 4.5) + 1):
                t = k / (int(ln / 4.5) + 1)
                pu, pv = a[0] + du * t, a[1] + dv * t
                box(verts, faces, pu - 0.09, pu + 0.09, pv - 0.09, pv + 0.09,
                    Z_PLAY, Z_PLAY + 0.90)
        new_mesh(f"play_fence_{key}", verts, faces, [mats["Toy_steel"]])

        # One oversized signature structure plus two small ones (style bible
        # s.9 semantic scale) — a rope-climber cone and two play blocks.
        sv, sf = [], []
        frustum(sv, sf, 8, uc, vc + sign * 3.0, 3.6, 0.35, Z_PLAY, Z_PLAY + 6.4)
        box(sv, sf, uc - 9.5, uc - 5.0, vc - 3.2, vc + 1.4, Z_PLAY, Z_PLAY + 2.1)
        box(sv, sf, uc + 5.5, uc + 10.5, vc - 2.0, vc + 2.6, Z_PLAY, Z_PLAY + 1.4)
        new_mesh(f"play_kit_{key}", sv, sf, [mats["Toy_white"]])

        # A lit PERIMETER, not a lit pad. Authored first as a full-pad shell,
        # which at night turned each 36 x 22 m playground into a light box
        # brighter than the walk grid that is supposed to be the hero glow
        # (style bible: hero glow + supporting accents). A frame is also the
        # more plausible reading — playgrounds are lit around their edges.
        gv, gf = [], []
        gi, go = 1.1, 2.0
        box(gv, gf, u0 + gi, u1 - gi, v0 + gi, v0 + go, Z_PLAY, Z_PLAY + 0.02)
        box(gv, gf, u0 + gi, u1 - gi, v1 - go, v1 - gi, Z_PLAY, Z_PLAY + 0.02)
        box(gv, gf, u0 + gi, u0 + go, v0 + go, v1 - go, Z_PLAY, Z_PLAY + 0.02)
        box(gv, gf, u1 - go, u1 - gi, v0 + go, v1 - go, Z_PLAY, Z_PLAY + 0.02)
        new_mesh(f"play_glow_{key}", gv, gf, [mats[glow]])


def kiosks(data, mats):
    """The garage kiosk at the McAllister end, the ramp mouth beside it, and the
    two small kiosks at the Grove/Larkin corner. These four objects are the only
    evidence above ground that the north block is the roof of a three-storey
    1960 garage; Brooks Hall and the garage itself are underground and are not
    modelled."""
    prism_uv("kiosk_garage", data["areas"]["garage_kiosk"], Z_DECK, Z_DECK + 3.20,
             mats["Toy_trim"])
    ring = orient_for_world(dedupe_ring(data["areas"]["garage_kiosk"]))
    us = [p[0] for p in ring]
    vs = [p[1] for p in ring]
    prism_uv("kiosk_garage_roof",
             rect_uv(min(us) - 0.6, max(us) + 0.6, min(vs) - 0.6, max(vs) + 0.6),
             Z_DECK + 3.20, Z_DECK + 3.55, mats["Toy_roofd"])

    # Ramp mouth: a sunken rectangle with a low retaining wall on three sides,
    # at the notch in the measured plaza ring around u = -80.
    prism_uv("ramp_mouth", rect_uv(-79.0, -70.5, -9.5, -1.0), 0.0, Z_DECK - 0.22,
             mats["Toy_ink"])
    for poly, nm in (
        (rect_uv(-79.6, -79.0, -10.1, -0.4), "w"),
        (rect_uv(-70.5, -69.9, -10.1, -0.4), "e"),
        (rect_uv(-79.6, -69.9, -10.1, -9.5), "s"),
    ):
        prism_uv(f"ramp_wall_{nm}", poly, Z_DECK - 0.22, Z_DECK + 0.85, mats["Toy_stone"])

    prism_uv("kiosk_cafe", rect_uv(70.4, 76.8, -33.0, -26.6), Z_DECK, Z_DECK + 3.00,
             mats["Toy_trim"], mat_top=mats["Toy_roofd"])
    prism_uv("kiosk_pitstop", rect_uv(84.4, 87.4, -41.0, -37.8), Z_DECK, Z_DECK + 2.60,
             mats["Toy_roofd"])


def furniture(mats):
    """Lamp poles on the walk grid, benches lining the central court, and
    planters at the City Hall end. Budget-capped: if the triangle count runs
    hot this is the first section to shrink, in the order people, planters,
    benches, lamps."""
    verts, faces = [], []
    for u in (-20.9, 10.9):
        for v in (-40.0, -19.4, 0.6, 21.1, 45.0):
            frustum(verts, faces, 6, u, v, 0.13, 0.10, Z_WALK, Z_WALK + 4.6)
            box(verts, faces, u - 0.32, u + 0.32, v - 0.32, v + 0.32,
                Z_WALK + 4.6, Z_WALK + 4.95)
    for u in (-78.0, 83.8):
        for v in (-24.0, 30.0):
            frustum(verts, faces, 6, u, v, 0.13, 0.10, Z_WALK, Z_WALK + 4.6)
            box(verts, faces, u - 0.32, u + 0.32, v - 0.32, v + 0.32,
                Z_WALK + 4.6, Z_WALK + 4.95)
    new_mesh("lamps", verts, faces, [mats["Toy_steel"]])

    bv, bf = [], []
    for v in (-30.0, -21.0, -12.0, 12.0, 21.0, 30.0):
        for u in (-8.6, 9.8):
            box(bv, bf, u - 0.28, u + 0.28, v - 0.85, v + 0.85, Z_GRAVEL, Z_GRAVEL + 0.42)
            box(bv, bf, u - 0.46, u + 0.46, v - 0.95, v + 0.95,
                Z_GRAVEL + 0.42, Z_GRAVEL + 0.56)
    new_mesh("benches", bv, bf, [mats["Toy_roofd"]])

    pv, pf = [], []
    for u in (-52.0, -34.0, 40.0, 58.0):
        box(pv, pf, u - 1.5, u + 1.5, 56.4, 59.4, Z_DECK, Z_DECK + 0.95)
    new_mesh("planters", pv, pf, [mats["Toy_stone"]])


def people(mats):
    """Four deliberate activity nodes — the two playgrounds, the central court
    and the City Hall end (style bible s.15/s.16). A plaza with nobody in it
    reads as a car park; an even sprinkle reads as wallpaper."""
    nodes = [
        (-42.0, -32.0), (46.0, -32.0), (0.6, 4.0), (0.6, 48.0),
    ]
    verts, faces = [], []
    n = 0
    for uc, vc in nodes:
        for k in range(5):
            du = (hash01(n * 31 + 5) * 2.0 - 1.0) * 3.4
            dv = (hash01(n * 31 + 11) * 2.0 - 1.0) * 3.4
            z0 = Z_WALK
            # Semantic scale (style bible s.9/s.15): at 0.48 m across these
            # were sub-pixel from the app's camera and the plaza read empty.
            box(verts, faces, uc + du - 0.36, uc + du + 0.36,
                vc + dv - 0.30, vc + dv + 0.30, z0, z0 + 1.62)
            box(verts, faces, uc + du - 0.26, uc + du + 0.26,
                vc + dv - 0.26, vc + dv + 0.26, z0 + 1.62, z0 + 2.08)
            n += 1
    new_mesh("people", verts, faces, [mats["Toy_navy"]])


# Metres east / north from the plaza OBB centre to the model's XY bbox centre,
# filled in by recentre(). The manifest anchor is the OBB centre moved by this
# vector, so the origin sits at the bbox centre (contract rule 2) while the
# plaza still lands on its real polygon (AGENTS rule 5).
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
    for name, t in per[:12]:
        print(f"[build]   {name:26} {t:6}")
    print(f"[build] objects={len(objs)} tris={tris} (cap {TRI_CAP})")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    lon0, lat0 = -122.4176170, 37.7794913
    m_per_lon = 111320.0 * math.cos(math.radians(37.77))
    lon = lon0 + ANCHOR_SHIFT[0] / m_per_lon
    lat = lat0 + ANCHOR_SHIFT[1] / 110540.0
    print(f"[build] plaza OBB centre lon/lat: {lon0} {lat0}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] long axis heading: {HEADING_LONG} deg true (toward Grove St)")
    assert abs(mx[2] - Z_FLAG_US) < 0.01, f"height datum drifted: max_z={mx[2]}"
    if tris > TRI_CAP:
        print(f"[build] WARNING triangle cap exceeded: {tris} > {TRI_CAP}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "civic-center-plaza.blend")
    glb = os.path.join(out, "civic-center-plaza.glb")
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
