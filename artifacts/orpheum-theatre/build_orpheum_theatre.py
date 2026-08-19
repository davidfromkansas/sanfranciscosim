"""Orpheum Theatre (1192 Market Street) - deterministic miniature build for SF-SIM.

Run:  blender -b --python build_orpheum_theatre.py [-- --out DIR]

Authored world-true. The site is a trapezoid, not a rectangle: Market Street
bears 45.9 deg cw from true north and Hyde Street 171.5 deg, so the two street
frontages are 54 deg apart. The build frame is Market-aligned - u+ runs NE along
Market at 45.9 deg, v+ runs NW at 315.9 deg - and W() rotates into world axes
(+X east, +Y north). The model is re-centred on its world AABB at the end,
because the loader puts the GLB origin at the manifest anchor and the anchor is
the AABB centre (the polygon centroid is 6.0 m away; see the plan's 2.3).

Massing from the measured OSM footprint (way/35115840), 2010 city LiDAR
(DataSF SF0351022) and photogrammetry off the Market elevation:
* street wings in cream terra-cotta over a round-arched ground arcade, under a
  projecting red mission-tile pent roof and a low parapet - 24.3 m on the
  Hyde/chamfer/SW-Market block, stepping down to 17.5 m on the NE wing;
* the entrance bay between them, proud of the wall, crested, carrying the
  marquee and the vertical ORPHEUM blade sign (crown 26.0 m);
* a low-pitch hipped auditorium roof filling the centre and north;
* the 1998 stage house, flat-roofed, at the NE corner - 27.2 m, the LiDAR
  hgt_max and the model's bbox top, so targetHeightM / measured lands on 1.0;
* glow set: hero is the blade sign's bulb letters and crown lamps
  (Toy_white_Glow), supported by the marquee chase line and its warm soffit
  (Toy_mustard_Glow). Nothing else lights - a theatre's offices are dark at
  curtain and the Main Library is across the street.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ------------------------------------------------------------------ site data

HEADING = 45.9                           # Market frontage bearing, deg cw from N
THETA = math.radians(90.0 - HEADING)     # math angle of u+ from +X (CCW)
CT, ST = math.cos(THETA), math.sin(THETA)

LAT0 = 37.77
KX = 111320.0 * math.cos(math.radians(LAT0))
KY = 110540.0

# Market-frame bbox centre of the OSM footprint (WGS84) == build-frame origin.
BLON, BLAT = -122.4147272, 37.7793624

# Footprint in (u, v), metres from the frame origin, CCW. The site is the exact
# OSM polygon with the sub-metre jogs on the north-west smoothed out. M1 and M2
# are inserted mid-edge on Market to split corner block / entrance bay / NE wing
# and HM is inserted on Hyde where the tall block ends; none of the three are
# real corners.
#
# The 7.4 x 6.1 m step-out on the north-east party wall is genuinely CONCAVE and
# an inward offset of a polygon containing it self-intersects. It also carries
# the site's northernmost point, so clipping it would shorten the building by
# 5 m, and straightening the flank to reach it would trespass 6.3 m onto 1170
# Market (rule 5). It is therefore split off as its own solid: CORE is the
# convex remainder, NE_ANNEX restores the step, CORE + NE_ANNEX is the real
# outline exactly.
A  = (-28.05, -28.63)   # Market, SW end (top of the chamfer)
M1 = (  2.00, -28.63)   # corner block / entrance bay
M2 = ( 11.00, -28.63)   # entrance bay / NE wing
B  = ( 31.58, -28.63)   # Market, NE end
C  = ( 31.45,  13.21)   # NE flank meets the north edge (on the real diagonal)
FP = ( 10.59,  28.33)   # north (Grove) edge, east end
G  = ( -3.08,  28.63)   # NW corner
HM = (-24.28,  -0.97)   # Hyde, where the tall block stops (25 m up from H)
H  = (-38.84, -21.30)   # Hyde, south end (bottom of the chamfer)
CORE = [A, M1, M2, B, C, FP, G, HM, H]
NE_ANNEX = [(31.45, 1.90), (38.80, 1.80), (38.84, 7.85), (31.45, 13.21)]

# The 24.3 m block wraps the SW half of Market, the chamfer and the south half
# of Hyde. It is NOT a constant-depth band: 13 m of offices behind Market, only
# 5 m behind Hyde, because the auditorium comes almost up to the Hyde wall (the
# satellite roof plan shows the hip roof reaching the west parapet).
# Depth is uniform on purpose. An earlier version used 13 m behind Market and
# 6 m behind the chamfer; the two offset lines meet at 34 deg, so the miter at
# their shared corner landed 12 m OUTSIDE the building and the whole band
# inverted. Mixed insets are only safe across near-right-angle corners.
TALL_SPAN = (7, 8, 0, 1)          # CORE indices HM -> H -> A -> M1
LOW_SPAN = (1, 2, 3, 4, 5, 6, 7)  # M1 -> M2 -> B -> C -> FP -> G -> HM
TALL_INSET = 7.0                  # 10 m collapses the 13 m chamfer's inner edge

# ------------------------------------------------------------------- massing

ARCADE_TOP = 7.20          # ground arcade / first floor line

# lower mass: the whole block, NE-wing heights
LOW_WALL_TOP = 15.50
LOW_BAND_Z = (14.40, 15.50)      # ornament band under the eave
LOW_TILE_Z = (15.50, 16.50)      # projecting mission-tile pent roof
LOW_PARAPET = 17.50
LOW_WIN = ((8.00, 10.80), (11.60, 14.40))
DECK = 16.50                     # roof deck the plant stands on

# the tall street block over Market SW / chamfer / Hyde south
TALL_WALL_TOP = 21.40
TALL_BAND_Z = (20.00, 21.40)
TALL_TILE_Z = (21.40, 22.40)
TALL_PARAPET = 24.30             # photogrammetric; LiDAR median over site 21.47
TALL_WIN = ((8.20, 11.60), (12.40, 15.80), (16.60, 20.00))
TALL_DECK = 22.40

BAY_U = (2.00, 11.00)      # entrance bay along Market
BAY_PROUD = 0.60
BAY_TOP = 22.60
BAY_CREST = 24.80

MARQ_U, MARQ_W = 6.50, 12.40
MARQ_Z = (4.10, 7.20)
MARQ_PROJ = 4.20

PANEL_U = 2.60                   # the poster panel hangs WEST of the blade
PANEL_Z = (7.40, 12.60)
PANEL_W, PANEL_PROUD = 5.00, 1.40

SIGN_U, SIGN_T = 6.50, 1.50      # centre along Market, thickness across it
SIGN_PROJ = 4.20                 # how far it stands off the bay face
SIGN_Z = (8.50, 25.20)
SIGN_CROWN = 26.00

AUD_U = (-14.0, 12.0)            # auditorium block, in the frame
AUD_V = (-18.0, 12.0)
AUD_EAVE, AUD_RIDGE = 19.00, 22.00
AUD_HIP = 4.0                    # hip inset at each end of the ridge

STAGE_U = (12.0, 27.0)
STAGE_V = (0.0, 14.0)
STAGE_TOP = 27.20                # LiDAR hgt_max - the summit and the bbox top

PALETTE_HEX = {
    "Toy_cream": "f2ede3",
    "Toy_sand": "ece4d4",
    "Toy_trim": "f3efe6",
    "Toy_brick": "c96f4a",
    "Toy_glass": "2a4d73",
    "Toy_ink": "3a3530",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_stone": "d9d2c2",
    "Toy_white_Glow": "f7f4ec",
    "Toy_mustard_Glow": "d9a441",
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
        # Flagged for the app's night pass; emission ships OFF.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    return mat


# -------------------------------------------------------------- mesh plumbing


def W(u, v, z):
    """Local (u, v, z) -> world (x, y, z)."""
    return (u * CT - v * ST, u * ST + v * CT, z)


def new_mesh(name, verts_local, faces, materials, face_mats=None):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(W(*v)) for v in verts_local], [], faces)
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


def box(name, cu, cv, z0, z1, su, sv, mat):
    hx, hy = su / 2, sv / 2
    verts = [(cu - hx, cv - hy, z0), (cu + hx, cv - hy, z0),
             (cu + hx, cv + hy, z0), (cu - hx, cv + hy, z0),
             (cu - hx, cv - hy, z1), (cu + hx, cv - hy, z1),
             (cu + hx, cv + hy, z1), (cu - hx, cv + hy, z1)]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7),
             (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, [mat])


def offset_poly(poly, d):
    """Offset a convex CCW polygon outward by d (negative = inward). `d` may be
    a per-edge sequence, which is how the tall block gets 13 m of depth behind
    Market and only 5 m behind Hyde."""
    n = len(poly)
    ds = d if hasattr(d, "__len__") else [d] * n
    lines = []
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        ex, ey = x1 - x0, y1 - y0
        L = math.hypot(ex, ey)
        nx, ny = ey / L, -ex / L          # outward normal for CCW winding
        lines.append((x0 + nx * ds[i], y0 + ny * ds[i], ex, ey))
    out = []
    for i in range(n):
        px, py, ex, ey = lines[i - 1]
        qx, qy, fx, fy = lines[i]
        det = ex * (-fy) - ey * (-fx)
        if abs(det) < 1e-9:
            # Collinear neighbours (M1/M2 are inserted mid-edge, not corners):
            # the miter is the plain offset of the shared vertex.
            out.append((qx, qy))
            continue
        t = ((qx - px) * (-fy) - (qy - py) * (-fx)) / det
        out.append((px + ex * t, py + ey * t))
    return out


def prism(name, poly, z0, z1, mat):
    k = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces = [tuple(range(k - 1, -1, -1)), tuple(range(k, 2 * k))]
    for i in range(k):
        j = (i + 1) % k
        faces.append((i, j, k + j, k + i))
    return new_mesh(name, verts, faces, [mat])


def ring_prism(name, outer, inner, z0, z1, mat):
    """Closed annular solid between two same-length CCW loops (parapets, tile
    eaves). Built as a ring, not a slab: a solid prism here would roof the whole
    block over and bury the deck it is supposed to surround."""
    k = len(outer)
    verts = ([(x, y, z0) for x, y in outer] + [(x, y, z0) for x, y in inner]
             + [(x, y, z1) for x, y in outer] + [(x, y, z1) for x, y in inner])
    O0, I0, O1, I1 = 0, k, 2 * k, 3 * k
    faces = []
    for i in range(k):
        j = (i + 1) % k
        faces.append((O0 + i, O0 + j, O1 + j, O1 + i))     # outer wall
        faces.append((I0 + j, I0 + i, I1 + i, I1 + j))     # inner wall
        faces.append((O0 + j, O0 + i, I0 + i, I0 + j))     # underside
        faces.append((O1 + i, O1 + j, I1 + j, I1 + i))     # top
    return new_mesh(name, verts, faces, [mat])


def band_prism(name, arc_out, arc_in, z0, z1, mat):
    """Same idea for an OPEN arc: out one way, back the other, capped."""
    return prism(name, list(arc_out) + list(reversed(arc_in)), z0, z1, mat)


def wing_poly(span, insets):
    """Closed polygon tracing CORE[span] outward and an inward offset back."""
    inner = offset_poly(CORE, [-d for d in insets])
    return [CORE[i] for i in span] + [inner[i] for i in reversed(span)]


# --- facade openings ---------------------------------------------------------


def face_frame(p, q):
    """Outward normal angle and length of the CCW footprint edge p -> q."""
    ex, ey = q[0] - p[0], q[1] - p[1]
    L = math.hypot(ex, ey)
    return math.atan2(-ex / L, ey / L), L


def extrude_outline(name, outline_tz, base_uv, ang, depth, mat):
    """A closed slab: outline in (tangent, z) on the plane through base_uv with
    outward normal at local angle `ang`; extends `depth` behind."""
    n = (math.cos(ang), math.sin(ang))
    t = (-math.sin(ang), math.cos(ang))
    verts = []
    for d in (0.0, -depth):
        for tt, zz in outline_tz:
            verts.append((base_uv[0] + t[0] * tt + n[0] * d,
                          base_uv[1] + t[1] * tt + n[1] * d, zz))
    k = len(outline_tz)
    faces = [tuple(range(k)), tuple(range(2 * k - 1, k - 1, -1))]
    for i in range(k):
        j = (i + 1) % k
        faces.append((i, j, k + j, k + i))
    return new_mesh(name, verts, faces, [mat])


ARCH_SEG = 8

# Applied, never cut. There are no booleans in this pipeline: an opening built
# as a recessed prism is simply buried inside the wall solid and disappears, and
# a surround that stands PROUDER than the thing it surrounds turns every window
# into a flat dark rectangle. So every opening is a stack of slabs standing off
# the wall face, and the depths only ever increase outward:
#   pier 0.12  <  ink reveal 0.08 ... glass 0.18
PROUD_PIER = 0.12
PROUD_REVEAL = 0.08
PROUD_SILL = 0.14
PROUD_GLASS = 0.18
PROUD_ARCH = 0.10


def arch_outline(w, sill, top):
    h = w / 2
    spring = top - h
    pts = [(-h, sill), (h, sill), (h, spring)]
    for i in range(1, ARCH_SEG):
        a = math.pi * i / ARCH_SEG
        pts.append((h * math.cos(a), spring + h * math.sin(a)))
    pts.append((-h, spring))
    return pts


def rect_outline(w, z0, z1):
    h = w / 2
    return [(-h, z0), (h, z0), (h, z1), (-h, z1)]


def on_face(name, p, q, t, outline, proud, depth, mat):
    """Place an outline slab at tangent offset `t` along the edge p -> q, its
    front face `proud` metres out from the wall."""
    ang, _ = face_frame(p, q)
    n = (math.cos(ang), math.sin(ang))
    tv = (-math.sin(ang), math.cos(ang))
    base = (p[0] + tv[0] * t + n[0] * proud, p[1] + tv[1] * t + n[1] * proud)
    return extrude_outline(name, outline, base, ang, depth + proud, mat)


def bays(p, q, pitch, margin=2.4):
    """Evenly spaced bay centres, as tangent offsets along the edge p -> q."""
    _, L = face_frame(p, q)
    usable = L - 2 * margin
    n = max(1, int(round(usable / pitch)))
    step = usable / n
    return [margin + step * (i + 0.5) for i in range(n)], step


def arcade(tag, p, q, pitch=6.0):
    ink = material("Toy_ink")
    ts, _ = bays(p, q, pitch)
    for i, t in enumerate(ts):
        on_face(f"{tag}_arch{i}", p, q, t, arch_outline(4.20, 0.35, 6.30),
                PROUD_ARCH, 0.55, ink)


def window_rows(tag, p, q, rows, pitch=6.0):
    """Bay rhythm: a proud pier between bays, a sill course under each row, and
    an ink-framed glass pane per bay. The Plateresque crust is NOT modelled -
    this is the rhythm it reads as from the app camera (plan 2.6)."""
    cream, sand = material("Toy_cream"), material("Toy_sand")
    ink, glass = material("Toy_ink"), material("Toy_glass")
    ts, step = bays(p, q, pitch)
    _, L = face_frame(p, q)
    z_lo = rows[0][0] - 0.9
    z_hi = rows[-1][1] + 0.5
    edges = [t - step / 2 for t in ts] + [ts[-1] + step / 2]
    for i, t in enumerate(e for e in edges if 0.7 < e < L - 0.7):
        on_face(f"{tag}_pier{i}", p, q, t, rect_outline(1.15, z_lo, z_hi),
                PROUD_PIER, 0.35, cream)
    for r, (z0, z1) in enumerate(rows):
        for i, t in enumerate(ts):
            on_face(f"{tag}_r{r}rev{i}", p, q, t,
                    rect_outline(4.20, z0 - 0.20, z1 + 0.20), PROUD_REVEAL,
                    0.30, ink)
            on_face(f"{tag}_r{r}win{i}", p, q, t, rect_outline(3.70, z0, z1),
                    PROUD_GLASS, 0.30, glass)
        _, L = face_frame(p, q)
        on_face(f"{tag}_r{r}sill", p, q, L / 2,
                rect_outline(L - 1.2, z0 - 0.70, z0 - 0.25), PROUD_SILL, 0.30,
                sand)


# ------------------------------------------------------------------ the build


def build():
    cream = material("Toy_cream")
    sand = material("Toy_sand")
    trim = material("Toy_trim")
    brick = material("Toy_brick")
    ink = material("Toy_ink")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    stone = material("Toy_stone")
    wglow = material("Toy_white_Glow")
    mglow = material("Toy_mustard_Glow")

    def arc(d):
        return [offset_poly(CORE, d)[i] for i in TALL_SPAN]

    # ---- podium: the whole block up to the first floor line ----
    bevel(prism("podium", CORE, 0.0, ARCADE_TOP, cream))
    bevel(prism("plinth", offset_poly(CORE, 0.30), 0.0, 0.90, stone),
          width=0.08, segments=1)
    bevel(prism("arcade_cornice", offset_poly(CORE, 0.45),
                ARCADE_TOP - 0.55, ARCADE_TOP, sand), width=0.08, segments=1)

    # ---- lower mass over the whole block; its eave and parapet run only
    # ---- where the block IS low, or the tall front would carry two cornices
    low_arc = lambda d: [offset_poly(CORE, d)[i] for i in LOW_SPAN]
    bevel(prism("low_wall", CORE, ARCADE_TOP, LOW_WALL_TOP, cream))
    bevel(band_prism("low_band", low_arc(0.30), low_arc(-0.60), *LOW_BAND_Z,
                     sand), width=0.09, segments=1)
    bevel(band_prism("low_tile", low_arc(1.20), low_arc(-1.60), *LOW_TILE_Z,
                     brick))
    bevel(band_prism("low_parapet", low_arc(-0.10), low_arc(-1.60),
                     LOW_TILE_Z[1], LOW_PARAPET - 0.30, trim),
          width=0.08, segments=1)
    bevel(band_prism("low_cap", low_arc(0.18), low_arc(-1.70),
                     LOW_PARAPET - 0.30, LOW_PARAPET, trim),
          width=0.07, segments=1)
    prism("low_deck", offset_poly(CORE, -1.60), LOW_WALL_TOP - 0.2, DECK, roofd)

    # ---- the tall street block on the SW half ----
    inner_arc = [offset_poly(CORE, -TALL_INSET)[i] for i in TALL_SPAN]
    bevel(band_prism("tall_wall", arc(0.0), inner_arc, ARCADE_TOP,
                     TALL_WALL_TOP, cream))
    bevel(band_prism("tall_band", arc(0.30), arc(-0.60), *TALL_BAND_Z, sand),
          width=0.09, segments=1)
    bevel(band_prism("tall_tile", arc(1.20), arc(-1.60), *TALL_TILE_Z, brick))
    bevel(band_prism("tall_parapet", arc(-0.10), arc(-1.60), TALL_TILE_Z[1],
                     TALL_PARAPET - 0.30, trim), width=0.08, segments=1)
    bevel(band_prism("tall_cap", arc(0.18), arc(-1.70), TALL_PARAPET - 0.30,
                     TALL_PARAPET, trim), width=0.07, segments=1)
    band_prism("tall_deck", arc(-1.60), inner_arc, TALL_WALL_TOP - 0.2,
               TALL_DECK, roofd)

    # the north-east step-out, restored as its own solid at the NE wing heights
    bevel(prism("annex", NE_ANNEX, 0.0, LOW_WALL_TOP, cream))
    bevel(ring_prism("annex_tile", offset_poly(NE_ANNEX, 1.20),
                     offset_poly(NE_ANNEX, -1.60), *LOW_TILE_Z, brick))
    bevel(ring_prism("annex_parapet", offset_poly(NE_ANNEX, -0.10),
                     offset_poly(NE_ANNEX, -1.60), LOW_TILE_Z[1], LOW_PARAPET,
                     trim), width=0.08, segments=1)
    prism("annex_deck", offset_poly(NE_ANNEX, -1.60), LOW_WALL_TOP - 0.2,
          LOW_PARAPET - 0.25, roofd)

    # ---- facades: arcade everywhere the street sees, bays above ----
    tall_faces = [("mkt_sw", A, M1), ("cham", H, A), ("hyde_s", HM, H)]
    low_faces = [("mkt_ne", M2, B), ("hyde_n", G, HM), ("grove", FP, G),
                 ("nw", C, FP)]
    for tag, p, q in tall_faces + low_faces:
        arcade(tag, p, q)
    for tag, p, q in tall_faces:
        window_rows(tag, p, q, TALL_WIN)
    for tag, p, q in low_faces:
        window_rows(tag, p, q, LOW_WIN)

    # oval recesses in the tall parapet, over Hyde and SW Market
    for tag, p, q in [("mkt_sw", A, M1), ("hyde_s", HM, H)]:
        for i, t in enumerate(bays(p, q, 6.0)[0]):
            on_face(f"{tag}_oc{i}", p, q, t,
                    rect_outline(1.90, TALL_PARAPET - 1.50, TALL_PARAPET - 0.80),
                    0.08, 0.24, ink)

    # ---- entrance bay: proud, crested, and the thing the sign hangs on ----
    bu = (BAY_U[0] + BAY_U[1]) / 2
    bw = BAY_U[1] - BAY_U[0]
    face_v = -28.63
    bevel(box("bay", bu, face_v - BAY_PROUD / 2 + 3.0, 0.0, BAY_TOP,
              bw, 6.0 + BAY_PROUD, cream))
    bevel(box("bay_crest", bu, face_v + 1.4, BAY_TOP, BAY_CREST,
              bw - 1.6, 2.8 + BAY_PROUD, sand))
    for tag, du in (("w", BAY_U[0] + 0.9), ("e", BAY_U[1] - 0.9)):
        bevel(box(f"bay_finial_{tag}", du, face_v + 0.4, BAY_TOP,
                  BAY_CREST + 0.6, 1.3, 1.3, sand), width=0.09, segments=1)
    box("bay_door", bu, face_v - BAY_PROUD - 0.10, 0.0, 4.60, bw - 2.4, 1.2, ink)

    # ---- marquee ----
    mv = face_v - BAY_PROUD - MARQ_PROJ / 2
    bevel(box("marquee", MARQ_U, mv, MARQ_Z[0] + 0.30, MARQ_Z[1] - 0.25,
              MARQ_W, MARQ_PROJ, ink), width=0.1, segments=1)
    bevel(box("marquee_cap", MARQ_U, mv, MARQ_Z[1] - 0.25, MARQ_Z[1],
              MARQ_W + 0.5, MARQ_PROJ + 0.5, trim), width=0.08, segments=1)
    box("marquee_soffit", MARQ_U, mv, MARQ_Z[0], MARQ_Z[0] + 0.30,
        MARQ_W - 0.8, MARQ_PROJ - 0.8, mglow)
    for i in range(3):
        u0 = MARQ_U + (i - 1) * (MARQ_W / 3)
        box(f"marquee_chase{i}", u0, mv, MARQ_Z[0] + 0.30, MARQ_Z[0] + 0.55,
            MARQ_W / 3 - 0.3, MARQ_PROJ + 0.14, wglow)
    bevel(box("panel", PANEL_U, face_v - BAY_PROUD - PANEL_PROUD / 2, *PANEL_Z,
              PANEL_W + 0.6, PANEL_PROUD, ink), width=0.09, segments=1)
    box("panel_face", PANEL_U, face_v - BAY_PROUD - PANEL_PROUD - 0.02,
        PANEL_Z[0] + 0.45, PANEL_Z[1] - 0.45, PANEL_W - 0.5, 0.12, trim)

    # ---- the blade sign: the whole point of the asset ----
    sv = face_v - BAY_PROUD - SIGN_PROJ / 2
    bevel(box("sign", SIGN_U, sv, SIGN_Z[0], SIGN_Z[1], SIGN_T, SIGN_PROJ, ink),
          width=0.08, segments=1)
    # Beads run down the blade's two long EDGES, not its faces. An earlier
    # version put full-height trim strips beside the letters and the sign read
    # near-white by day - the exact opposite of a dark green blade with bulbs.
    for tag, dv in (("out", -SIGN_PROJ / 2 - 0.09), ("in", SIGN_PROJ / 2 + 0.09)):
        bevel(box(f"sign_bead_{tag}", SIGN_U, sv + dv, SIGN_Z[0], SIGN_Z[1],
                  SIGN_T + 0.26, 0.18, sand), width=0.05, segments=1)
    bevel(box("sign_crown", SIGN_U, sv, SIGN_Z[1], SIGN_CROWN - 0.35,
              SIGN_T + 0.70, SIGN_PROJ + 0.70, sand), width=0.09, segments=1)
    bevel(box("sign_finial", SIGN_U, sv, SIGN_CROWN - 0.35, SIGN_CROWN,
              SIGN_T + 0.30, SIGN_PROJ * 0.55, sand), width=0.07, segments=1)
    # ORPHEUM reading downward, as raised pucks on both broad faces (never a
    # closed glow shell - see the plan's 2.8)
    n_letters = 7
    top_z, bot_z = SIGN_Z[1] - 1.5, SIGN_Z[0] + 1.5
    step = (top_z - bot_z) / (n_letters - 1)
    for i in range(n_letters):
        z = top_z - i * step
        for side, du in (("w", -SIGN_T / 2 - 0.11), ("e", SIGN_T / 2 + 0.11)):
            box(f"sign_L{i}{side}", SIGN_U + du, sv, z - 0.85, z + 0.85,
                0.22, 2.10, wglow)
    for i, du in enumerate((-0.55, 0.55)):
        box(f"crown_lamp{i}", SIGN_U + du, sv - SIGN_PROJ / 2 - 0.20,
            SIGN_CROWN - 1.30, SIGN_CROWN - 0.55, 0.45, 0.30, wglow)

    # ---- auditorium and stage house ----
    au = (AUD_U[0] + AUD_U[1]) / 2
    av = (AUD_V[0] + AUD_V[1]) / 2
    bevel(box("aud_wall", au, av, DECK - 0.5, AUD_EAVE - 0.05,
              AUD_U[1] - AUD_U[0] - 0.5, AUD_V[1] - AUD_V[0] - 0.5, cream))
    e0u, e1u = AUD_U
    e0v, e1v = AUD_V
    hip = [(e0u, e0v, AUD_EAVE), (e1u, e0v, AUD_EAVE),
           (e1u, e1v, AUD_EAVE), (e0u, e1v, AUD_EAVE),
           (e0u + AUD_HIP, av, AUD_RIDGE), (e1u - AUD_HIP, av, AUD_RIDGE)]
    hip_faces = [(3, 2, 1, 0), (0, 1, 5, 4), (1, 2, 5), (2, 3, 4, 5), (3, 0, 4)]
    # Steel, not roofd: the satellite reads the auditorium hip as a light
    # silver plane against the dark flat decks, and that value break is what
    # makes the roof legible from the app's altitude.
    bevel(new_mesh("aud_roof", hip, hip_faces, [steel]), width=0.1, segments=1)
    for i, du in enumerate((-6.0, 3.0)):
        bevel(box(f"aud_monitor{i}", au + du, av, AUD_RIDGE - 1.4,
                  AUD_RIDGE + 0.9, 4.0, 3.0, trim), width=0.09, segments=1)

    # back of house filling the narrow north end, where the trapezoid is too
    # tight for the auditorium rectangle
    bevel(box("boh", 3.0, 17.0, DECK - 0.5, 19.00, 18.0, 10.0, cream))
    bevel(box("boh_cap", 3.0, 17.0, 19.00, 19.35, 18.4, 10.4, roofd),
          width=0.09, segments=1)

    su_ = (STAGE_U[0] + STAGE_U[1]) / 2
    sv_ = (STAGE_V[0] + STAGE_V[1]) / 2
    ssu, ssv = STAGE_U[1] - STAGE_U[0], STAGE_V[1] - STAGE_V[0]
    bevel(box("stage_house", su_, sv_, 0.0, STAGE_TOP - 0.45, ssu, ssv, sand))
    bevel(box("stage_cap", su_, sv_, STAGE_TOP - 0.45, STAGE_TOP,
              ssu + 0.4, ssv + 0.4, trim), width=0.09, segments=1)
    bevel(box("stage_rig", su_ + 3.0, sv_ + 2.0, STAGE_TOP - 2.20,
              STAGE_TOP - 0.45, 5.0, 4.0, steel), width=0.09, segments=1)

    # ---- roof plant, on the low deck along Market north-east of the entrance
    for i in range(4):
        bevel(box(f"cond{i}", 4.0 + i * 6.0, -22.5, DECK + 0.2, DECK + 2.0,
                  4.6, 4.4, steel), width=0.09, segments=1)
    for i in range(2):
        bevel(box(f"cond_n{i}", 20.0 + i * 6.5, -12.0, DECK + 0.2, DECK + 1.7,
                  5.0, 5.6, steel), width=0.09, segments=1)
    bevel(box("plant_ph", 24.0, -21.0, DECK + 0.2, DECK + 3.2, 7.0, 5.2, trim),
          width=0.09, segments=1)
    bevel(box("stair_ph", -4.5, -21.5, DECK + 0.2, DECK + 3.4, 4.8, 4.4, trim),
          width=0.09, segments=1)
    box("duct", 13.0, -17.0, DECK + 0.2, DECK + 1.0, 22.0, 1.3, steel)
    # the Hyde-side valley, between the tall block and the auditorium
    for i in range(3):
        bevel(box(f"vent{i}", -18.0, -12.0 + i * 7.0, DECK + 0.2, DECK + 1.5,
                  3.2, 3.0, steel), width=0.08, segments=1)
    bevel(box("tank", -18.5, 8.0, DECK + 0.2, DECK + 2.4, 4.0, 4.0, trim),
          width=0.09, segments=1)


# --------------------------------------------------------- recenter + export


def recenter_and_report():
    dg = bpy.context.evaluated_depsgraph_get()
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    mn = Vector((1e12, 1e12, 1e12))
    mx = Vector((-1e12, -1e12, -1e12))
    tris = 0
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
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, mn.z))
    for o in objs:
        for v in o.data.vertices:
            v.co.x -= center.x
            v.co.y -= center.y
            v.co.z -= center.z
    anchor_lon = BLON + center.x / KX
    anchor_lat = BLAT + center.y / KY
    dims = [round(mx[i] - mn[i], 3) for i in range(3)]
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] dims={dims}")
    print(f"[build] recentered by {[round(v, 3) for v in center]}")
    print(f"[build] ANCHOR lon/lat = {anchor_lon:.7f}, {anchor_lat:.7f}")
    print(f"[build] heading: Market frontage {HEADING} deg cw from N (world-true)")
    return tris, dims, (anchor_lon, anchor_lat)


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)

    build()
    recenter_and_report()

    blend = os.path.join(out, "orpheum-theatre.blend")
    glb = os.path.join(out, "orpheum-theatre.glb")
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
