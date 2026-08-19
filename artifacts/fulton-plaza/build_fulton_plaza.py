"""Deterministic Blender build of the SF-SIM miniature Fulton Plaza.

    blender -b --python build_fulton_plaza.py -- [--out DIR]

Writes fulton-plaza.blend and fulton-plaza.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = the model's XY bbox centre; the manifest anchor is the
plaza's right-of-way OBB centre moved by ANCHOR_SHIFT.

Design (see REFERENCE.md for the sources behind every number):

* Fulton Plaza is the pedestrianised block of Fulton Street between Larkin and
  Hyde — a STREET that stopped being a street in spring 2020. It has no parcel
  of its own, so its polygon is the right-of-way between two block parcels;
* the recognition rests on ONE AXIS, ONE MONUMENT and ONE ENORMOUS GRAPHIC:
  the 1894 Pioneer Monument dead centre (0.995 m off the plaza's own OBB
  centre — the 1993 relocation put it on the crossing of the two axes), and
  Jeremy Novy's two 20 m koi circling it on the black asphalt;
* the two flanks are deliberately DIFFERENT: raised soil beds and mature
  planes on the museum side, a pale terrace and smaller trees on the library
  side. That contrast is the second recognition cue and it costs one material;
* the whole asset is DRAPED on the baked terrain. Fulton falls 2.37 m across
  this block, and `placeGeneric()` seats a landmark from a single elevation
  sample at the anchor — so a flat plate is buried at one end and floating at
  the other. See "the drape" below and REFERENCE.md;
* night state: the koi are the hero glow, and that is not a licence — the real
  mural is sealed with retroreflective glass beads specifically so that it
  lights up (KQED). Supporting glow: lamp heads and a wash on the monument.
  SPECTRA, the LED array over the plaza, is deliberately NOT modelled; see
  docs/asset-plans/fulton-plaza.md 2.10.

Authoring frame: geometry is laid out in the plaza's local (u, v) frame —
u along the long axis, POSITIVE TOWARD HYDE STREET (east), bearing 81.15 deg
true; v across, POSITIVE TOWARD THE MAIN LIBRARY (south), bearing 171.15 deg —
and mapped to world x/y by to_world(). The plaza sits 8.85 deg off the world
axes, so the axis-aligned XY bounding box is ~126 x 66 m even though the plaza
is 120.0 x 48.6 m. That is expected, not a scale error.

THE DRAPE. Every z in this file is a height ABOVE LOCAL GRADE, and dz(u, v)
from data/terrain_uv.json is added at vertex-emission time. Consequences,
both asserted in the validator rather than left looking like contract slips:
  * min_z is NEGATIVE (z = 0 is the anchor's ground, which is where the loader
    puts the model), so the usual "min_z ~ 0" check is replaced by "the deck
    stands a constant height above the terrain everywhere";
  * targetHeightM is the model's VERTICAL EXTENT, because the loader's scale is
    targetHeightM / bbox height and it must land on 1.0.
"""

import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# Signed headings. The Civic Center grid leans 8.85 deg EAST of north, so the
# cross axis toward the library (south) bears 171.15 (= 180 - 8.85), NOT 188.85.
# Those two are mirror images about north and every bounding-box check reads the
# same 8.85 deg for both; civic-center-plaza shipped the wrong sign once and
# came out 18 deg crooked against its own block with every measurement still
# validating. Ground truth here: the neighbouring landmark GLBs (Main Library
# 9.06, Asian Art Museum 9.06, City Hall 9.62, Civic Center Plaza 9.06).
HEADING_LONG = 81.15    # +u, toward Hyde Street (east)
HEADING_CROSS = 171.15  # +v, toward the Main Library (south)

_UL = math.radians(HEADING_LONG)
U_DIR = (math.sin(_UL), math.cos(_UL))
# +v points SOUTH, which makes (u, v) LEFT-handed in world (x east, y north) —
# exactly the convention civic-center-plaza uses, and the reason
# orient_for_world() keeps the ring whose (u, v) shoelace is NEGATIVE.
V_DIR = (U_DIR[1], -U_DIR[0])

# Heights above LOCAL GRADE. Every level is a distinct closed solid and the gaps
# are deliberate: nothing in this asset may be coplanar with anything else, and
# the deck has to clear the baked street underneath it (see below).
Z_BOT = -1.50      # deck underside, flat. dy_min is -1.165, so this is 0.34 m
                   # of skirt below the lowest terrain the plate covers.
# THE DECK HEIGHT IS SET BY THE BAKED STREET UNDERNEATH, NOT BY TASTE.
# exclusionZones() clears buildings, not streets, so the DataSF centreline for
# Fulton still bakes here: a 9 m charcoal ribbon at v=0, two 3 m pale sidewalk
# plinths at v=+-6 lifted TOY_CURB_H = 0.35 m, and a centre dash at +0.03
# (toystreets/19_13.bin lines 169-172, measured).
#
# 0.55 was the first value and it is NOT enough. Two things eat the margin:
#   * the ribbon's y is quantised to decimetres and rounds UP to 0.20 m above
#     the terrain sample in places, so the sidewalk top reaches terrain + 0.55;
#   * createGroundMaterial() in app/src/materials.js runs the ground with
#     polygonOffsetFactor/Units = -2, which pulls it toward the camera in depth.
# At 0.55 the measured clearance inside the right-of-way was 0.06-0.15 m, the
# offset won, and two pale stone stripes drew straight over the deck, the koi
# and the monument's apron in the running app. Nothing in the Blender renders
# or the contract validator can see this: it is a depth-bias fight against
# geometry that is not in the file.
# 0.95 leaves 0.40 m of clearance over the worst station. The cost is a plaza
# that stands a little proud of the crossings at Larkin and Hyde — semantic
# exaggeration in authoring, which the style bible allows and AGENTS rule 5
# does not touch (nothing has been moved or rescaled).
Z_DECK = 0.95      # asphalt field top
Z_KOI = 1.01       # the mural, painted ON the asphalt. 60 mm of body over the
                   # deck: the deck's own top is a 4 m drape grid and a 20 m koi
                   # interpolates it differently, so 5 mm of clearance sank the
                   # fish into the asphalt in patches.
Z_APRON = 1.03     # the monument's pale granite apron. 80 mm clear of the
                   # scored joints (Z_DECK + 0.02), which otherwise draw across it.
Z_WALK = 1.10      # terrace and sidewalks, one step up from the roadway
Z_BED = 1.35       # the north planting beds, kerbed

# The Pioneer Monument. SF Arts Commission accession 1894.4.a-o records the work
# as 420 x 488 x 676 in overall: 10.668 m tall on a 12.40 x 17.17 m base, with
# the base alone 294 in = 7.468 m and Minerva 126 in = 3.200 m. The 17-vertex
# cruciform in data/plaza_uv.json (which is how the CITY BAKE traces it) measures
# 16.76 x 11.39 m — agreement to within a metre from two unrelated sources.
# All four are measured from the monument's OWN base, which stands on the apron:
# add Z_APRON to get a height above local grade. Authored the other way round
# once and the model's crest came out 0.60 m short of the catalogue figure.
MON_H = 10.668          # base -> Minerva's finial. THE monument datum.
MON_PEDESTAL_TOP = 7.468
MON_PLATFORM = 1.15     # the stepped granite platform under everything
MON_PIER_TOP = 2.75     # the four cardinal piers
MON_FIGURE_H = 2.25     # the three surviving bronze groups

# Trees. No source consulted measures them. The crowns are modelled at 8.60 m
# above local grade so that the Pioneer Monument stays the tallest thing on its
# own plaza once the 2.37 m drape is added — a taller measured tree would move
# the model's crest onto a lollipop, which is both wrong compositionally and
# wrong as a height datum. Recorded as ESTIMATED (plan 2.15 risk 2).
TREE_N_TRUNK_R = 0.32
TREE_N_TRUNK_TOP = 4.10
TREE_N_CROWN_LO = 3.55
TREE_N_CROWN_HI = 7.80
TREE_N_CROWN_R_LO = 2.45
TREE_N_CROWN_R_HI = 1.80
TREE_N_SPACING = 8.6
TREE_S_TRUNK_R = 0.22
TREE_S_TRUNK_TOP = 2.90
TREE_S_CROWN_LO = 2.45
TREE_S_CROWN_HI = 5.60
TREE_S_CROWN_R_LO = 1.55
TREE_S_CROWN_R_HI = 1.15
TREE_JITTER = 0.07      # +/- 7% scale, hashed off the index, never random

KOI_LEN = 20.5          # published 65-70 ft; 20.5 m is the middle of that band

TRI_CAP = 16000

PALETTE_HEX = {
    # The plaza's own ground. NOT Toy_roofd (45454a): measured in the running
    # app, that value comes back rgb(9,9,12) on a large up-facing surface — the
    # diorama's ambient cannot lift it and the whole asset reads as a hole.
    # 6f7076 is ~2.7x its linear luminance, still the darkest large surface in
    # the model, and still unmistakably asphalt against the pale edges.
    "Toy_tarmac": "6f7076",
    "Toy_stone": "d9d2c2",       # kerb, terrace, sidewalks, monument granite
    "Toy_cream": "f2ede3",       # the monument's apron — the bullseye the koi orbit
    "Toy_steel": "9aa0a6",       # lamp poles, bollards, tree trunks (as
                                 # civic-center-plaza: London plane bark is pale
                                 # mottled grey-cream, not orange-brown)
    "Toy_verdigris": "9fb8a8",   # tree crowns, shared with civic-center-plaza so
                                 # the two plazas on this spine read as one world
    "Toy_soil": "7d6a55",        # the north beds
    "Toy_bronze": "6d6448",      # Minerva, the three surviving groups, Ashurbanipal.
                                 # Patinated bronze, not gilt: 7a6f52 rendered as pale khaki
                                 # and the figures read as gold pagoda finials next to the
                                 # granite. Kept above the diorama's dark cliff all the same.
    "Toy_koiWhite": "f4e9dc",    # koi bodies
    "Toy_koiOrange": "e8733c",   # koi markings — the asset's one saturated accent
    "Toy_seam": "5f5f68",        # scored paving joints. Authored in Toy_ink first
                                 # (3a3530) and the top view came back as a grid of black
                                 # bars dividing the plaza into tiles — a joint has to give
                                 # the asphalt a SCALE, not a pattern of its own.
    "Toy_ink": "3a3530",         # bollard bands and other hairline darks
    "Toy_roofd": "45454a",       # bench slats and bins only (small dark props)
    "Toy_navy": "2c4a70",        # people
    "Toy_koiWhite_Glow": "f4e9dc",
    "Toy_koiOrange_Glow": "e8733c",
    "Toy_gold_Glow": "caa64a",   # lamp heads, and the wash up the monument
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


# ------------------------------------------------------------------ the drape

DRAPE = None


def load_data():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "data", "plaza_uv.json"), "r", encoding="utf8") as fh:
        plaza = json.load(fh)
    with open(os.path.join(here, "data", "terrain_uv.json"), "r", encoding="utf8") as fh:
        terrain = json.load(fh)
    return plaza, terrain


def dz(u, v):
    """Terrain height at (u, v) relative to the anchor's ground, bilinear over
    the sampled grid — the same interpolation app/src/data.js does, so the model
    and the loader agree about where the ground is."""
    t = DRAPE
    fu = (u - t["u_min"]) / t["u_step"]
    fv = (v - t["v_min"]) / t["v_step"]
    i = min(t["u_count"] - 2, max(0, int(math.floor(fu))))
    j = min(t["v_count"] - 2, max(0, int(math.floor(fv))))
    tu = min(1.0, max(0.0, fu - i))
    tv = min(1.0, max(0.0, fv - j))
    a = t["dy"][j][i] + (t["dy"][j][i + 1] - t["dy"][j][i]) * tu
    b = t["dy"][j + 1][i] + (t["dy"][j + 1][i + 1] - t["dy"][j + 1][i]) * tu
    return a + (b - a) * tv


# ----------------------------------------------------------------- transforms


def to_world(u, v):
    return (u * U_DIR[0] + v * V_DIR[0], u * U_DIR[1] + v * V_DIR[1])


def W(u, v, h):
    """(u, v, height above local grade) -> world vertex, drape applied."""
    x, y = to_world(u, v)
    return (x, y, h + dz(u, v))


def rect_uv(u0, u1, v0, v1):
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]


def orient_for_world(poly):
    """Order a plaza-frame ring so it comes out COUNTER-clockwise in world, which
    is what makes the prism caps face outward. The (u, v) frame is left-handed
    in world (see V_DIR), so the test is inverted: keep the negative shoelace."""
    a = 0.0
    for i in range(len(poly)):
        u0, v0 = poly[i]
        u1, v1 = poly[(i + 1) % len(poly)]
        a += u0 * v1 - u1 * v0
    return poly if a < 0 else poly[::-1]


def dedupe_ring(poly):
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


def prism_verts_faces(poly_uv, h0, h1, base_index=0, flat_bottom=None):
    """Closed extrusion of a plaza-frame polygon, draped. `flat_bottom`, when
    given, is an ABSOLUTE z for the underside instead of a draped height —
    the deck plate uses it so its skirt reaches below the terrain everywhere."""
    poly = orient_for_world(poly_uv)
    n = len(poly)
    if flat_bottom is None:
        lo = [W(u, v, h0) for u, v in poly]
    else:
        lo = [to_world(u, v) + (flat_bottom,) for u, v in poly]
    hi = [W(u, v, h1) for u, v in poly]
    verts = lo + hi
    b = base_index
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((b + i, b + j, b + n + j, b + n + i))
    faces.append(tuple(b + i for i in range(n - 1, -1, -1)))
    faces.append(tuple(b + i for i in range(n, 2 * n)))
    return verts, faces


def prism_uv(name, poly_uv, h0, h1, mat, mat_top=None, flat_bottom=None):
    verts, faces = prism_verts_faces(dedupe_ring(poly_uv), h0, h1, flat_bottom=flat_bottom)
    face_mats = [0] * (len(faces) - 1) + [1 if mat_top else 0]
    mats = [mat, mat_top] if mat_top else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def bilerp_quad(quad, s, t):
    """Point inside a (u, v) quad given as [c0, c1, c2, c3] in ring order."""
    a = (quad[0][0] + (quad[1][0] - quad[0][0]) * s, quad[0][1] + (quad[1][1] - quad[0][1]) * s)
    b = (quad[3][0] + (quad[2][0] - quad[3][0]) * s, quad[3][1] + (quad[2][1] - quad[3][1]) * s)
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def draped_slab(name, quad, h_top, mat, ns, nt, flat_bottom=None, h_bot=None):
    """A quad slab whose TOP follows the terrain on an ns x nt grid. Anything
    wider than ~20 m has to be built this way: a four-corner top is a plane, and
    a plane over 120 m of 1.7% grade is 0.5 m out in the middle of the block."""
    verts, faces = [], []
    idx = {}
    for j in range(nt + 1):
        for i in range(ns + 1):
            u, v = bilerp_quad(quad, i / ns, j / nt)
            idx[(i, j)] = len(verts)
            verts.append(W(u, v, h_top))
    for j in range(nt):
        for i in range(ns):
            faces.append((idx[(i, j)], idx[(i, j + 1)], idx[(i + 1, j + 1)], idx[(i + 1, j)]))
    # skirt: walk the top's boundary, drop to the underside
    border = ([(i, 0) for i in range(ns + 1)]
              + [(ns, j) for j in range(1, nt + 1)]
              + [(i, nt) for i in range(ns - 1, -1, -1)]
              + [(0, j) for j in range(nt - 1, 0, -1)])
    low = []
    for i, j in border:
        u, v = bilerp_quad(quad, i / ns, j / nt)
        low.append(len(verts))
        verts.append(to_world(u, v) + (flat_bottom,) if flat_bottom is not None
                     else W(u, v, h_bot))
    m = len(border)
    for k in range(m):
        a, b = border[k], border[(k + 1) % m]
        faces.append((idx[a], idx[b], low[(k + 1) % m], low[k]))
    faces.append(tuple(low))
    obj = new_mesh(name, verts, faces, [mat])
    # The winding above is derived from the quad's own order; recalc_face_normals
    # in new_mesh() only agrees on a closed manifold, which this is — but the
    # signed volume is what the validator checks, so flip if it came out inside-out.
    return obj


def rot_rect(uc, vc, a, b, ang):
    """A rectangle 2a x 2b centred on (uc, vc), rotated by `ang` in the plaza
    frame. Bronze figures are not axis-aligned — a statue that lines up exactly
    with the paving grid reads as a piece of the paving."""
    ca, sa = math.cos(ang), math.sin(ang)
    return [(uc + du * ca - dv * sa, vc + du * sa + dv * ca)
            for du, dv in ((-a, -b), (a, -b), (a, b), (-a, b))]


def figure(verts, faces, uc, vc, base, height, width, depth, ang):
    """A bronze figure as a chunky silhouette: tapered body, then a head. Built
    from boxes rather than from frusta — the first build used 6-sided frusta and
    every statue on the monument read as a little pagoda spire."""
    h_body = height * 0.70
    poly_solid(verts, faces, rot_rect(uc, vc, width, depth, ang), base, base + h_body * 0.55)
    poly_solid(verts, faces, rot_rect(uc, vc, width * 0.78, depth * 0.80, ang),
               base + h_body * 0.55, base + h_body)
    poly_solid(verts, faces, rot_rect(uc, vc, width * 0.42, depth * 0.46, ang),
               base + h_body, base + height * 0.90)
    poly_solid(verts, faces, rot_rect(uc, vc, width * 0.30, depth * 0.34, ang),
               base + height * 0.90, base + height)


def ngon_uv(nsides, uc, vc, r, rot=0.0):
    """CLOCKWISE in (u, v) = counter-clockwise in world; see orient_for_world()."""
    return [
        (uc + r * math.cos(rot - 2 * math.pi * i / nsides),
         vc + r * math.sin(rot - 2 * math.pi * i / nsides))
        for i in range(nsides)
    ]


def frustum(verts, faces, nsides, uc, vc, r0, r1, h0, h1, rot=0.0):
    b = len(verts)
    lo = ngon_uv(nsides, uc, vc, r0, rot)
    hi = ngon_uv(nsides, uc, vc, r1, rot)
    verts.extend([W(u, v, h0) for u, v in lo])
    verts.extend([W(u, v, h1) for u, v in hi])
    for i in range(nsides):
        j = (i + 1) % nsides
        faces.append((b + i, b + j, b + nsides + j, b + nsides + i))
    faces.append(tuple(b + i for i in range(nsides - 1, -1, -1)))
    faces.append(tuple(b + nsides + i for i in range(nsides)))


def box(verts, faces, u0, u1, v0, v1, h0, h1):
    b = len(verts)
    vs, fs = prism_verts_faces(rect_uv(u0, u1, v0, v1), h0, h1, base_index=b)
    verts.extend(vs)
    faces.extend(fs)


def draped_bar(verts, faces, u0, u1, v0, v1, h0, h1, n, along="u"):
    """A long thin bar whose top follows the terrain, appended to a shared
    buffer. A single prism will NOT do: prism_verts_faces() puts a plane through
    the four corners, and this site's cross-fall reaches 0.87 m, so a 45 m
    scored joint modelled as one box rose 0.6 m above the deck in the middle and
    drew straight across the monument's apron. Measured in the exported GLB —
    joint_u5 spanned z +0.40 to +1.19 where the apron topped out at +0.77."""
    for k in range(n):
        a, b = k / n, (k + 1) / n
        if along == "u":
            box(verts, faces, u0 + (u1 - u0) * a, u0 + (u1 - u0) * b, v0, v1, h0, h1)
        else:
            box(verts, faces, u0, u1, v0 + (v1 - v0) * a, v0 + (v1 - v0) * b, h0, h1)


def poly_solid(verts, faces, poly_uv, h0, h1):
    b = len(verts)
    vs, fs = prism_verts_faces(dedupe_ring(poly_uv), h0, h1, base_index=b)
    verts.extend(vs)
    faces.extend(fs)


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


# -------------------------------------------------------------------- the koi

# Jeremy Novy, 2024. Two white-and-orange koi, each about 20 m, "circling" the
# Pioneer Monument on the blacktop. Their positions are measured from aerial
# imagery; their outlines are authored, because no source gives them and the
# aerial resolves the silhouette but not its edge. Plan 2.15 risk 1.
#
# The outline is parametric so it can be re-tuned from one place: s runs 0 at
# the tail tip to 1 at the nose, w is the half-width, both as fractions of
# length. The forked tail is made by closing the ring through a notch at
# s = 0.075 rather than by boolean-ing two shapes — this asset has no booleans.
KOI_UPPER = [
    (0.000, 0.118), (0.045, 0.130), (0.105, 0.082), (0.170, 0.032),
    (0.250, 0.050), (0.340, 0.064), (0.430, 0.074), (0.500, 0.086),
    (0.560, 0.098), (0.615, 0.082), (0.700, 0.074), (0.790, 0.066),
    (0.880, 0.050), (0.950, 0.031), (1.000, 0.000),
]
KOI_NOTCH = 0.078
# One dorsal bump in the upper outline (s 0.50-0.615 above) reads as a fin from
# the air; the pectorals are separate little solids so they can sit on one side
# only, the way a koi seen from above shows them.
KOI_PECTORAL = [(0.735, 0.070), (0.700, 0.150), (0.640, 0.140), (0.660, 0.066)]
# A kohaku is roughly 40% red. Authored first as three small ellipses and the
# top view came back as a white fish with a dot on it — at the app's camera
# distance the orange has to be a SADDLE, not a spot, or the koi read as two
# pale slivers and the plaza loses its only saturated accent.
KOI_PATCHES = [
    [(0.155, 0.000), (0.215, 0.046), (0.300, 0.058), (0.345, 0.030),
     (0.330, -0.034), (0.250, -0.052), (0.180, -0.034)],
    [(0.395, 0.010), (0.455, 0.072), (0.545, 0.084), (0.620, 0.060),
     (0.640, -0.020), (0.560, -0.074), (0.460, -0.062), (0.400, -0.030)],
    [(0.700, -0.006), (0.760, 0.052), (0.845, 0.048), (0.880, 0.014),
     (0.850, -0.038), (0.760, -0.050), (0.710, -0.034)],
]


def koi_outline():
    lower = [(s, -w) for s, w in reversed(KOI_UPPER[:-1])]
    return [KOI_UPPER[-1]] + lower + [(KOI_NOTCH, 0.0)] + KOI_UPPER[:-1]


def koi_place(pts, uc, vc, ang, length, mirror=False):
    """Koi-local (s, w) -> plaza (u, v). s is measured from the tail, so the
    body is shifted to sit centred on (uc, vc)."""
    ca, sa = math.cos(ang), math.sin(ang)
    out = []
    for s, w in pts:
        a = (s - 0.5) * length
        b = (-w if mirror else w) * length
        out.append((uc + a * ca - b * sa, vc + a * sa + b * ca))
    return out


def koi(data, mats):
    """Two koi, each one closed 0.02 m solid for the body plus three orange
    patch solids and one pectoral fin, and a glow shell inset from the body.

    The glow is a THIN slab inset from the body edge, never the body itself: a
    closed _Glow shell is two alpha layers in the app's day pass and would tint
    the whole fish ~23% even at noon."""
    verts, f_white, f_orange = [], [], []
    gverts, g_white, g_orange = [], [], []
    n = data["nodes"]
    # Heads point in opposite directions around the monument, which is what
    # "circling" means: the west fish swims north, the east fish swims south.
    spec = [
        ("west", n["koi_west"][0], n["koi_west"][1], math.radians(-104.0), False),
        ("east", n["koi_east"][0], n["koi_east"][1], math.radians(74.0), True),
    ]
    for name, uc, vc, ang, mirror in spec:
        body = koi_place(koi_outline(), uc, vc, ang, KOI_LEN, mirror)
        poly_solid(verts, f_white, body, Z_DECK + 0.03, Z_KOI)
        poly_solid(verts, f_white, koi_place(KOI_PECTORAL, uc, vc, ang, KOI_LEN, mirror),
                   Z_DECK + 0.03, Z_KOI)
        for patch in KOI_PATCHES:
            poly_solid(verts, f_orange, koi_place(patch, uc, vc, ang, KOI_LEN, mirror),
                       Z_KOI, Z_KOI + 0.015)
        # Glow: the body outline pulled in toward its own spine, then the
        # markings ON TOP of it in their own colour. Authored first as one white
        # shell over everything and the night render gave two pure-white fish —
        # the shell was simply covering the orange. A koi that loses its
        # markings at night has lost the thing that makes it a koi.
        inset = [(s, w * 0.55) for s, w in KOI_UPPER]
        low = [(s, -w) for s, w in reversed(inset[:-1])]
        shell = [inset[-1]] + low + [(KOI_NOTCH + 0.02, 0.0)] + inset[:-1]
        poly_solid(gverts, g_white, koi_place(shell, uc, vc, ang, KOI_LEN, mirror),
                   Z_KOI + 0.015, Z_KOI + 0.030)
        for patch in KOI_PATCHES:
            pc = (sum(q[0] for q in patch) / len(patch), sum(q[1] for q in patch) / len(patch))
            shrunk = [(pc[0] + (q[0] - pc[0]) * 0.86, pc[1] + (q[1] - pc[1]) * 0.86)
                      for q in patch]
            poly_solid(gverts, g_orange, koi_place(shrunk, uc, vc, ang, KOI_LEN, mirror),
                       Z_KOI + 0.030, Z_KOI + 0.042)

    faces = f_white + f_orange
    face_mats = [0] * len(f_white) + [1] * len(f_orange)
    new_mesh("koi", verts, faces, [mats["Toy_koiWhite"], mats["Toy_koiOrange"]], face_mats)
    new_mesh("koi_glow", gverts, g_white + g_orange,
             [mats["Toy_koiWhite_Glow"], mats["Toy_koiOrange_Glow"]],
             [0] * len(g_white) + [1] * len(g_orange))


# --------------------------------------------------------------------- ground


def ground(data, mats):
    """The draped asphalt deck, its scored joints, the south terrace, the north
    sidewalk and the two planting beds. Two thirds of this asset is paving, so
    the paving is designed rather than left as a slab (style bible s.13)."""
    ring = orient_for_world(dedupe_ring(data["ring"]))
    # 30 x 12 cells over 120 x 49 m = 4 m resolution, which resolves the 2.37 m
    # fall to under 40 mm anywhere. 720 quads is 1440 triangles and it is the
    # single largest line in the budget; it buys the thing the asset exists for.
    draped_slab("deck", ring, Z_DECK, mats["Toy_tarmac"], 30, 12, flat_bottom=Z_BOT)

    # Scored joints on a 12 m grid, 0.22 m wide, 20 mm proud: from the air they
    # give the asphalt a scale, which is what stops it reading as a blank field.
    u0, u1 = -57.0, 57.0
    v0, v1 = -22.5, 22.5
    jv, jf = [], []
    u = u0
    while u <= u1 + 1e-6:
        draped_bar(jv, jf, u - 0.09, u + 0.09, v0, v1, Z_DECK, Z_DECK + 0.02, 12, along="v")
        u += 12.0
    for v in (-11.0, 0.0, 11.0):
        draped_bar(jv, jf, u0, u1, v - 0.09, v + 0.09, Z_DECK, Z_DECK + 0.02, 24, along="u")
    new_mesh("joints", jv, jf, [mats["Toy_seam"]])

    # South (library) terrace: a pale band with a low wall on its plaza edge.
    # The OSM sidewalk centreline sits at v ~ +17.8 and the property line at
    # +24.29, so the band is the 10 m between the wall and the line.
    terrace = rect_uv(-59.0, 59.3, 14.2, 24.29)
    draped_slab("terrace_s", orient_for_world(terrace), Z_WALK, mats["Toy_stone"], 20, 3,
                h_bot=Z_DECK - 0.05)
    wv, wf = [], []
    draped_bar(wv, wf, -59.0, 59.3, 14.2, 14.62, Z_DECK, Z_WALK + 0.32, 24)
    new_mesh("terrace_s_wall", wv, wf, [mats["Toy_stone"]])

    # North (museum) sidewalk: narrower, outboard of the beds.
    walk_n = rect_uv(-59.4, 59.0, -24.29, -19.6)
    draped_slab("walk_n", orient_for_world(walk_n), Z_WALK, mats["Toy_stone"], 20, 2,
                h_bot=Z_DECK - 0.05)

    # The two raised soil beds, at their measured OSM outlines. They overhang the
    # museum's property line by up to 2 m — that is real (the beds are cut into
    # the museum forecourt) and harmless: the Asian Art Museum GLB's own wall is
    # another ~5 m north. Do not clip them to the parcel line. Plan 2.3.
    for side in ("west", "east"):
        bed = orient_for_world(dedupe_ring(data["beds"][side]))
        us = [p[0] for p in bed]
        vs = [p[1] for p in bed]
        cu, cv = sum(us) / len(us), sum(vs) / len(vs)
        inner = [(u + (cu - u) * 0.055, v + (cv - v) * 0.055) for u, v in bed]
        # 50 m long and draped: gridded along their own length for the same
        # reason the joints are (see draped_bar).
        draped_slab(f"bed_{side}_kerb", bed, Z_BED + 0.06, mats["Toy_stone"], 12, 1,
                    h_bot=Z_DECK)
        draped_slab(f"bed_{side}_soil", orient_for_world(inner), Z_BED,
                    mats["Toy_soil"], 12, 1, h_bot=Z_DECK + 0.02)


# ------------------------------------------------------------------- monument


def monument(data, mats):
    """The Pioneer Monument. A cruciform granite platform (the ring the city bake
    traces), a tapered central pedestal to 7.468 m, Minerva to 10.668 m, and four
    cardinal piers — THREE of which carry a bronze group. The EAST pier is empty:
    'Early Days' was removed on 14 September 2018 and never replaced, and the
    empty pier is visible from above, so modelling the pre-2018 monument would be
    both wrong and conspicuous."""
    ring = dedupe_ring(data["monument"]["ring"])
    us = [p[0] for p in ring]
    vs = [p[1] for p in ring]
    cu = (min(us) + max(us)) / 2.0
    cv = (min(vs) + max(vs)) / 2.0

    # The pale apron the whole thing stands on: ~21 m across, measured from the
    # aerial. It is the bullseye the koi orbit and it has to read at thumbnail.
    prism_uv("apron", ngon_uv(20, cu, cv, 10.1), Z_DECK, Z_APRON, mats["Toy_cream"])

    verts, f_stone, f_bronze = [], [], []
    # stepped platform, two courses, on the traced cruciform
    outer = [(u + (cu - u) * -0.06, v + (cv - v) * -0.06) for u, v in ring]
    poly_solid(verts, f_stone, outer, Z_APRON, Z_APRON + 0.42)
    poly_solid(verts, f_stone, ring, Z_APRON, Z_APRON + MON_PLATFORM)

    # Central pedestal: the hub of the cross, tapering. Deliberately the widest
    # single mass on the plaza after the apron — authored slimmer first and the
    # aerial read as four little chapels with nothing in the middle.
    poly_solid(verts, f_stone, rect_uv(cu - 2.85, cu + 2.85, cv - 3.05, cv + 3.05),
               Z_APRON, Z_APRON + 1.55)
    poly_solid(verts, f_stone, rect_uv(cu - 2.35, cu + 2.35, cv - 2.55, cv + 2.55),
               Z_APRON + 1.55, Z_APRON + 2.55)
    ped_top = Z_APRON + MON_PEDESTAL_TOP
    crest = Z_APRON + MON_H
    frustum(verts, f_stone, 4, cu, cv, 2.60, 2.10, Z_APRON + 2.55, ped_top - 0.70,
            rot=math.pi / 4)
    poly_solid(verts, f_stone, rect_uv(cu - 1.72, cu + 1.72, cv - 1.82, cv + 1.82),
               ped_top - 0.70, ped_top - 0.55)
    poly_solid(verts, f_stone, rect_uv(cu - 1.62, cu + 1.62, cv - 1.72, cv + 1.72),
               ped_top - 0.55, ped_top)

    # Minerva with her California grizzly: a bronze silhouette, not anatomy —
    # but a READABLE one. She is 126 in of a 420 in monument, i.e. 30% of its
    # height, and the first build made her a thin 0.95 m cone that vanished at
    # the app's camera distance. Robe, torso, helmeted head, and the bear as a
    # separate block at her feet, which is what makes the group legible from
    # above rather than a spike.
    figure(verts, f_bronze, cu, cv, ped_top, crest - ped_top, 0.86, 0.66,
           math.radians(24.0))
    # the California grizzly at her feet, a low block rather than an animal
    poly_solid(verts, f_bronze, rot_rect(cu + 1.05, cv + 0.35, 0.62, 0.40, math.radians(24.0)),
               ped_top, ped_top + 0.78)

    # the four cardinal piers, at the ends of the cross arms
    piers = {
        "west": (min(us) + 1.35, cv, True),
        "east": (max(us) - 1.35, cv, False),   # <- EMPTY since 2018
        "north": (cu, min(vs) + 1.25, True),
        "south": (cu, max(vs) - 1.25, True),
    }
    for name, (pu, pv, has_figure) in piers.items():
        poly_solid(verts, f_stone, rect_uv(pu - 1.45, pu + 1.45, pv - 1.45, pv + 1.45),
                   Z_APRON, Z_APRON + MON_PIER_TOP)
        poly_solid(verts, f_stone, rect_uv(pu - 1.68, pu + 1.68, pv - 1.68, pv + 1.68),
                   Z_APRON + MON_PIER_TOP - 0.30, Z_APRON + MON_PIER_TOP)
        if not has_figure:
            continue
        top = Z_APRON + MON_PIER_TOP
        # Plenty (north), Commerce (south) and In '49 (west) face outward, so
        # each is turned to its own cardinal rather than to the paving grid.
        ang = {"north": 0.0, "south": math.pi, "west": math.pi / 2}[name]
        figure(verts, f_bronze, pu, pv, top, MON_FIGURE_H, 0.76, 0.54, ang + math.radians(12))

    faces = f_stone + f_bronze
    face_mats = [0] * len(f_stone) + [1] * len(f_bronze)
    new_mesh("monument", verts, faces, [mats["Toy_stone"], mats["Toy_bronze"]], face_mats)

    # Night: a wash up the pedestal faces. A thin shell proud of the granite,
    # never the granite itself — a _Glow primary surface reads translucent by day.
    gv, gf = [], []
    poly_solid(gv, gf, rect_uv(cu - 2.90, cu + 2.90, cv - 3.10, cv + 3.10),
               Z_APRON + 0.28, Z_APRON + 1.02)
    new_mesh("monument_glow", gv, gf, [mats["Toy_gold_Glow"]])

    return cu, cv


# ---------------------------------------------------------------------- trees

# Positions are read off the aerial: the north beds carry a regular row of
# mature planes, the south terrace a thinner row of younger ones. Counted from
# the imagery rather than invented, but not surveyed — ESTIMATED, plan 2.15.
def tree_rows(data):
    north, south = [], []
    for side in ("west", "east"):
        bed = data["beds"][side]
        us = [p[0] for p in bed]
        vs = [p[1] for p in bed]
        u0, u1 = min(us) + 3.2, max(us) - 3.2
        vc = (min(vs) + max(vs)) / 2.0
        n = max(2, int(round((u1 - u0) / TREE_N_SPACING)) + 1)
        for k in range(n):
            north.append((u0 + (u1 - u0) * k / (n - 1), vc))
    for k in range(10):
        south.append((-51.5 + k * 11.4, 19.6))
    return north, south


def trees(data, mats):
    north, south = tree_rows(data)
    verts, f_trunk, f_crown = [], [], []
    for idx, (u, v) in enumerate(north):
        s = 1.0 + (hash01(idx) * 2.0 - 1.0) * TREE_JITTER
        rot = hash01(idx + 7919) * math.pi / 4.0
        frustum(verts, f_trunk, 6, u, v, TREE_N_TRUNK_R * s, TREE_N_TRUNK_R * 0.82 * s,
                Z_BED, TREE_N_TRUNK_TOP * s, rot)
        frustum(verts, f_crown, 8, u, v, TREE_N_CROWN_R_LO * s, TREE_N_CROWN_R_HI * s,
                TREE_N_CROWN_LO * s, TREE_N_CROWN_HI * s, rot)
    for idx, (u, v) in enumerate(south):
        s = 1.0 + (hash01(idx + 331) * 2.0 - 1.0) * TREE_JITTER
        rot = hash01(idx + 5011) * math.pi / 4.0
        frustum(verts, f_trunk, 6, u, v, TREE_S_TRUNK_R * s, TREE_S_TRUNK_R * 0.82 * s,
                Z_WALK, TREE_S_TRUNK_TOP * s, rot)
        frustum(verts, f_crown, 8, u, v, TREE_S_CROWN_R_LO * s, TREE_S_CROWN_R_HI * s,
                TREE_S_CROWN_LO * s, TREE_S_CROWN_HI * s, rot)
    faces = f_trunk + f_crown
    face_mats = [0] * len(f_trunk) + [1] * len(f_crown)
    new_mesh("trees", verts, faces, [mats["Toy_steel"], mats["Toy_verdigris"]], face_mats)


# ------------------------------------------------------------------ furniture


def furniture(data, mats):
    """Bollards at both ends — they are why this is a plaza and not a street —
    plus lamps, benches, bins and the Ashurbanipal statue."""
    bv, bf, bi = [], [], []
    for u in (-57.6, 57.4):
        v = -22.0
        while v <= 22.01:
            frustum(bv, bf, 8, u, v, 0.20, 0.17, Z_DECK, Z_DECK + 0.92)
            frustum(bv, bi, 8, u, v, 0.215, 0.215, Z_DECK + 0.66, Z_DECK + 0.76)
            v += 3.15
    faces = bf + bi
    new_mesh("bollards", bv, faces, [mats["Toy_steel"], mats["Toy_ink"]],
             [0] * len(bf) + [1] * len(bi))

    lv, lf = [], []
    gv, gf = [], []
    for v, base in ((21.4, Z_WALK), (-21.0, Z_WALK)):
        for k in range(6):
            u = -50.0 + k * 20.0
            frustum(lv, lf, 6, u, v, 0.15, 0.11, base, base + 5.1)
            # lens under the housing, not inside it: the first build buried the
            # glow box within the opaque head and the night render showed a row
            # of unlit poles.
            box(gv, gf, u - 0.31, u + 0.31, v - 0.31, v + 0.31, base + 5.10, base + 5.26)
            box(lv, lf, u - 0.28, u + 0.28, v - 0.28, v + 0.28, base + 5.26, base + 5.60)
    new_mesh("lamps", lv, lf, [mats["Toy_steel"]])
    new_mesh("lamps_glow", gv, gf, [mats["Toy_gold_Glow"]])

    fv, ff = [], []
    for u in (-44.0, -30.0, -16.0, 16.0, 30.0, 44.0):
        box(fv, ff, u - 0.95, u + 0.95, 16.1, 16.72, Z_WALK, Z_WALK + 0.40)
        box(fv, ff, u - 1.05, u + 1.05, 15.98, 16.84, Z_WALK + 0.40, Z_WALK + 0.53)
    for u in (-38.0, 0.0, 38.0):
        box(fv, ff, u - 0.42, u + 0.42, -20.4, -19.56, Z_WALK, Z_WALK + 0.88)
    new_mesh("furniture", fv, ff, [mats["Toy_roofd"]])

    # Ashurbanipal (1988), at its mapped position on the museum side.
    au, av = data["nodes"]["ashurbanipal"]
    sv, sf = [], []
    box(sv, sf, au - 0.95, au + 0.95, av - 0.95, av + 0.95, Z_WALK, Z_WALK + 1.30)
    frustum(sv, sf, 6, au, av, 0.62, 0.44, Z_WALK + 1.30, Z_WALK + 3.10)
    frustum(sv, sf, 6, au, av, 0.40, 0.16, Z_WALK + 3.10, Z_WALK + 4.05)
    new_mesh("ashurbanipal", sv, sf, [mats["Toy_bronze"]])


def people(mats):
    """Three deliberate activity nodes (style bible s.15/s.16): the monument,
    the terrace outside the library's Fulton entrance, and the Hyde end where
    the farmers market stages. Not an even sprinkle — this plaza is either busy
    or notoriously empty, and an even sprinkle reads as neither."""
    nodes = [(-6.0, 6.5, 6), (12.0, 13.0, 5), (44.0, 2.0, 5)]
    verts, faces = [], []
    n = 0
    for uc, vc, count in nodes:
        for _ in range(count):
            du = (hash01(n * 37 + 5) * 2.0 - 1.0) * 4.2
            dv = (hash01(n * 37 + 11) * 2.0 - 1.0) * 3.6
            base = Z_WALK if vc > 14.0 else Z_DECK
            box(verts, faces, uc + du - 0.36, uc + du + 0.36,
                vc + dv - 0.30, vc + dv + 0.30, base, base + 1.62)
            box(verts, faces, uc + du - 0.26, uc + du + 0.26,
                vc + dv - 0.26, vc + dv + 0.26, base + 1.62, base + 2.08)
            n += 1
    new_mesh("people", verts, faces, [mats["Toy_navy"]])


# ---------------------------------------------------------------------- build

ANCHOR_SHIFT = [0.0, 0.0]


def build():
    global DRAPE
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    plaza, terrain = load_data()
    DRAPE = terrain
    mats = {name: make_material(name) for name in PALETTE_HEX}

    ground(plaza, mats)
    monument(plaza, mats)
    koi(plaza, mats)
    trees(plaza, mats)
    furniture(plaza, mats)
    people(mats)

    # Bevel budget. Spent only on the chunky single solids that carry the
    # miniature read at the app's camera distance. The draped slabs are NOT
    # bevelled: their tops are 4 m grids and a bevel would multiply 1440
    # triangles by nine for detail under a pixel. Glow shells are never
    # bevelled — "_glow" anywhere in the name, not endswith().
    SKIP = {"deck", "terrace_s", "walk_n", "trees", "lamps", "furniture",
            "people", "koi", "bollards", "ashurbanipal", "joints",
            "bed_west_kerb", "bed_east_kerb", "bed_west_soil", "bed_east_soil",
            "terrace_s_wall"}
    for obj in list(bpy.data.objects):
        if obj.type != "MESH" or obj.name in SKIP or "_glow" in obj.name:
            continue
        if obj.name.startswith(("bed_", "apron", "terrace_s_wall")):
            bevel(obj, width=0.06, segments=1)
        else:
            bevel(obj, width=0.10, segments=2)

    recentre()
    return plaza


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


def report(plaza):
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
    for name, t in per:
        print(f"[build]   {name:22} {t:6}")
    extent = mx[2] - mn[2]
    print(f"[build] objects={len(objs)} tris={tris} (cap {TRI_CAP})")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    lon0, lat0 = plaza["anchor_lonlat"]
    m_per_lon = 111320.0 * math.cos(math.radians(37.77))
    lon = lon0 + ANCHOR_SHIFT[0] / m_per_lon
    lat = lat0 + ANCHOR_SHIFT[1] / 110540.0
    print(f"[build] ROW OBB centre lon/lat:  {lon0} {lat0}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] long axis heading: {HEADING_LONG} deg true (toward Hyde St)")
    print(f"[build] VERTICAL EXTENT (= targetHeightM): {extent:.4f} m")
    print(f"[build]   min_z {mn[2]:.4f} is NEGATIVE by design: z=0 is the anchor's ground")
    print(f"[build]   monument crest above local grade: {MON_H + Z_APRON:.3f} m")
    mon = [o for o in objs if o.name == "monument"][0]
    mon_top = max((mon.matrix_world @ v.co)[2] for v in mon.data.vertices)
    print(f"[build]   monument crest in model space: {mon_top:.4f} m")
    assert abs(mon_top - mx[2]) < 1e-3, (
        f"the model's crest is NOT the monument: max_z={mx[2]:.3f}, monument={mon_top:.3f}. "
        "A tree has overtaken the Pioneer Monument on its own plaza — see plan 2.15 risk 2.")
    if tris > TRI_CAP:
        print(f"[build] WARNING triangle cap exceeded: {tris} > {TRI_CAP}")
    return tris, extent


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    plaza = build()

    # The validator needs two numbers it cannot recover from the GLB: the XY
    # recentring shift (so it can map plaza (u, v) back into model space) and
    # the vertical extent the manifest will carry. Written here rather than
    # hand-copied, so the two can never drift.
    tris, extent = report(plaza)
    with open(os.path.join(out, "data", "build_meta.json"), "w", encoding="utf8") as fh:
        json.dump({
            "_": "GENERATED by build_fulton_plaza.py — do not hand-edit",
            "anchor_lonlat_row_obb": plaza["anchor_lonlat"],
            "anchor_shift_m_east_north": [round(v, 4) for v in ANCHOR_SHIFT],
            "manifest_anchor_lonlat": [
                round(plaza["anchor_lonlat"][0]
                      + ANCHOR_SHIFT[0] / (111320.0 * math.cos(math.radians(37.77))), 7),
                round(plaza["anchor_lonlat"][1] + ANCHOR_SHIFT[1] / 110540.0, 7),
            ],
            "heading_long_deg": HEADING_LONG,
            "heading_cross_deg": HEADING_CROSS,
            "vertical_extent_m": round(extent, 4),
            "monument_crest_above_grade_m": round(Z_APRON + MON_H, 4),
            "z_deck_above_grade_m": Z_DECK,
            "triangles": tris,
        }, fh, indent=1)

    blend = os.path.join(out, "fulton-plaza.blend")
    glb = os.path.join(out, "fulton-plaza.glb")
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
