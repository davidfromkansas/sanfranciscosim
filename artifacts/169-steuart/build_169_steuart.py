"""Deterministic Blender build of the SF-SIM miniature Army & Navy YMCA Building
(169 Steuart Street / 166 The Embarcadero, San Francisco).

    blender -b --python build_169_steuart.py -- [--out DIR]

Writes 169-steuart.blend and 169-steuart.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = parcel centroid (anchor lon -122.3919821, lat 37.7926993),
min Z = 0, tile-roof apex exactly 46.64 m.

Design (see REFERENCE.md for the sources behind every number):

* the footprint is the SURVEYED DataSF parcel 3715028/3715029 — one polygon, one
  mapblklot, one building. OSM traces it as three ways (32862485 / 193054138 /
  193054131) summing to the same outline; they are not three buildings. A
  1,766.9 m2 pentagon: a 45.1 deg rotated square 42.35 x 41.84 m with a 5.84 m
  chamfer at the east corner;
* the recognition cue is a ROOF. Every neighbour on these two blocks is a
  flat-topped street wall; this one carries a steeply pitched red clay TILE HIP
  standing 18 m above their parapets. Apex 46.64 m (DataSF LiDAR hgt_max), eave
  35.00 m (SKYDB's published "35 m / 10 floors" — the tower's wall top, not the
  building). Both numbers are right about different things;
* under the roof, the ARCADED TOWER STOREY the 1976 survey names: a band of
  small round-headed openings around the tower, modelled as a notched reveal
  band rather than as arches, because at city scale that is what an arcade is;
* two eight-storey wings at 28.14 m (the LiDAR modal plane; 8 storeys x 3.5 m)
  around a light court, over a podium that covers the WHOLE block-through
  parcel. The survey: "covers the width of the block from the Embarcadero to
  Steuart Street on the 1st 2 floors ... divided into 2 wings, each 8 stories";
* the Embarcadero front is the hallmark: a two-storey rusticated cast-stone base
  to a PHOTOGRAMMETRIC 9.60 m (solved off pano FWxuTLcC1ZB4mrrB42U-3w, which
  self-calibrates against the surveyed parcel to 5 cm), a corbelled bracket
  frieze, five brick storeys, a taller arched top storey with a balcony, and a
  decorative crest parapet at 30.90 m — also photogrammetric;
* the Steuart front, which is the address, is a THREE-STOREY STREET WALL ONLY at
  ~14 m, split cream stucco (161-165, Harbor Court) / dark brick (169, the
  Embarcadero YMCA). The tall mass sits 12.7 m behind it. Running the eight
  storeys out to Steuart Street is the single most likely way to get this
  building wrong;
* the flagpole is NOT modelled. DataSF peak_1st_m is 50.35 m and there is a real
  pole on the apex, but a 50.35 m bounding box would rescale the whole building
  by 7% through the loader's targetHeightM/measuredHeight. The apex is the crest;
* roof membrane is Toy_sand and roof plant is Toy_steel from the start.
  Toy_roofd (45454a) measured rgb(9,9,12) on a lit roof deck in the live scene;
* night state: the hero is the ARCADE BAND under the tile roof — a lit loggia
  ring visible from every direction, and the same feature that identifies the
  building by day. Supported by the Embarcadero entry arch, a scatter of lit
  hotel windows, and the "EMBARCADERO YMCA" fascia on Steuart. Glow surfaces are
  thin shells proud of the opaque surface behind them.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF parcel acdm-wktn blklot 3715028/3715029 projected with the app's
# tangent projection and recentred on the polygon centroid (which agrees with
# the minimum-area OBB centre to 0.01 m). CCW in (x=east, y=north).
FOOTPRINT = [
    (0.15, 29.76),      # A  north corner  — Embarcadero x Hotel Griffon line
    (-29.69, -0.17),    # E  west corner   — Steuart x Hotel Griffon line
    (-0.15, -29.76),    # D  south corner  — Steuart x 177 Steuart line
    (25.56, -3.97),     # C  chamfer end
    (29.69, 0.16),      # B  east corner
]

EDGE_GRIFFON = 0      # 42.27 m, faces NW 314.9 deg — party edge + open yard
EDGE_STEUART = 1      # 41.81 m, faces SW 225.1 deg — Steuart Street, the address
EDGE_SE = 2           # 36.42 m, faces SE 134.9 deg — party edge to 177 Steuart
EDGE_CHAMFER = 3      # 5.84 m,  faces SE 135.0 deg
EDGE_EMBARCADERO = 4  # 41.81 m, faces NE  45.1 deg — the hallmark entry front

# Heights above ground (ground = 3.62 m NAVD88; the model's z=0 is that ground).
Z_STONE_TOP = 9.60      # top of the two-storey cast-stone base (photogrammetric)
Z_FRIEZE1 = 10.45       # top of the corbelled bracket frieze
FLOOR_H = 2.82          # brick shaft floor-to-floor
SHAFT_FLOORS = 5
Z_ARCH0 = Z_FRIEZE1 + SHAFT_FLOORS * FLOOR_H     # 24.55 — arched top storey floor
Z_WING = 28.14          # eight-storey wing roof (LiDAR hgt_majority)
Z_CREST = 30.90         # Embarcadero crest parapet (photogrammetric)
Z_PODIUM = 14.00        # podium roof / Steuart street wall (estimated)
Z_TOWER_EAVE = 35.00    # tower wall top (SKYDB 35 m / 10 floors)
Z_ARCADE0 = 31.55       # springing of the arcade band
Z_APEX = 46.64          # tile-roof apex — the target height and the bbox top

# Ground and second-storey openings in the cast-stone base.
Z_G0, Z_G1 = 1.05, 5.15
Z_S0, Z_S1 = 6.35, 8.95
SHAFT_WIN_H = 1.95
SHAFT_WIN_SILL = 0.55
ARCH_WIN_H = 3.05       # the tall arched openings of the 8th storey

SKIN = 0.10
PIER_W = 0.95
PIER_PROJ = 0.16
BASE_PROJ = 0.16        # the rusticated base stands proud of the brick above it
FRIEZE_PROJ = 0.70      # the corbel band is the strongest horizontal after the roof
CORNICE_PROJ = 0.85
PARAPET_T = 0.40

BAYS_EMBARCADERO = 11
BAYS_STEUART = 9

# Depth of the eight-storey mass measured from the Embarcadero face along the
# parcel's 42.27 m NE->SW axis. The remaining 12.67 m is the Steuart street wall.
# 29.60 x 41.81 - the court = 65% of the footprint, which is what reproduces the
# LiDAR distribution's mean (24.90 m) and sd (7.40 m). See the plan's 2.1.
WING_DEPTH = 29.60
COURT = (12.0, 8.0)     # w along the frontage, d into the block
COURT_V = 24.2          # court centre depth: clear of the tower (which ends at v=19)

TOWER = (18.0, 16.0)    # w along the frontage, d into the block
TOWER_U_FRAC = 0.5      # centred on the Embarcadero frontage
TOWER_V = 11.0          # centre depth from the Embarcadero face
ROOF_RIDGE = 2.4        # ridge length of the hip (a near-pyramid)
EAVE_OVER = 0.85        # tile-roof eave overhang

PALETTE_HEX = {
    # The identity colours: warm red-brown brick over pale cast stone, under a
    # saturated terracotta tile roof.
    "Toy_brick": "c96f4a",
    "Toy_rust": "a86444",
    "Toy_stone": "d9d2c2",
    "Toy_cream": "f2ede3",
    "Toy_red": "c4453c",
    "Toy_sand": "ece4d4",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_gold": "caa64a",
    "Toy_steel": "9aa0a6",
    "Toy_ink": "3a3530",
    # A _Glow material's BASE colour IS its night appearance: the app's night
    # layer is an unlit overlay drawn at the baked colour.
    "Toy_glass_Glow": "6f95b8",
    "Toy_gold_Glow": "caa64a",
    "Toy_white_Glow": "f7f4ec",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def edge_frame(poly, i):
    """Edge i of a CCW polygon: (origin, length, tangent unit, outward normal)."""
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def poly_edge(i, poly=None):
    return edge_frame(poly if poly is not None else FOOTPRINT, i)


def offset_polygon(poly, d):
    """Miter offset of the convex CCW footprint; positive d moves outward."""
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


def clip_halfplane(poly, n, c):
    """Sutherland-Hodgman clip of a CCW polygon to {p : dot(p,n) <= c}."""
    out = []
    npts = len(poly)
    for i in range(npts):
        a, b = poly[i], poly[(i + 1) % npts]
        da = a[0] * n[0] + a[1] * n[1] - c
        db = b[0] * n[0] + b[1] * n[1] - c
        if da <= 0:
            out.append(a)
        if (da > 0) != (db > 0):
            t = da / (da - db)
            out.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
    return out


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


def arch_profile(w, z0, z1, seg=5):
    """Round-headed opening: rectangle to the springing, then a semicircle. The
    springing sits at z1 - w/2 so the head is a true half-round."""
    a = w / 2.0
    spring = z1 - a
    pts = [(-a, z0), (a, z0), (a, spring)]
    for k in range(1, seg):
        th = math.pi * k / seg
        pts.append((a * math.cos(th), spring + a * math.sin(th)))
    pts.append((-a, spring))
    return pts


def bay_centres(edge, count, poly=None):
    _a, length, _t, _n = poly_edge(edge, poly)
    pitch = length / count
    return [(i + 0.5) * pitch for i in range(count)]


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


def bevel(obj, width=0.10, segments=2):
    """Miniature-style edge softening (style bible s.4), capped at a third of the
    object's thinnest dimension so thin applied panels do not collapse."""
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


def prism(name, poly, z0, z1, mat, mat_caps=None):
    """Closed extrusion of a CCW polygon (walls + both caps)."""
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


def ring_band(name, poly, z0, z1, off_in, off_out, mat):
    """Closed band following a footprint: 4 loops, quads between."""
    lo_in = offset_polygon(poly, off_in)
    lo_out = offset_polygon(poly, off_out)
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


def wall_panel(name, frame, u_centre, profile, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in a wall plane, extruded outward
    from offset d0 to d1 along that wall's normal. `frame` is (origin, t, n)."""
    a, t, n = frame
    verts = []
    for d in (d0, d1):
        for du, z in profile:
            px = a[0] + t[0] * (u_centre + du) + n[0] * d
            py = a[1] + t[1] * (u_centre + du) + n[1] * d
            verts.append((px, py, z))
    npts = len(profile)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def edge_wall(edge, poly=None):
    a, _length, t, n = poly_edge(edge, poly)
    return (a, t, n)


def face_panel(name, edge, u_centre, profile, d0, d1, mat, poly=None):
    return wall_panel(name, edge_wall(edge, poly), u_centre, profile, d0, d1, mat)


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0):
    c, s = math.cos(yaw), math.sin(yaw)
    corners = []
    for lx, ly in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)):
        corners.append((cx + lx * c - ly * s, cy + lx * s + ly * c))
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


# The building's own roof grid: u runs along the EMBARCADERO edge from its east
# corner B (0 .. 41.81), v runs INTO the block away from that edge (0 .. 42.27).
def uv_to_world(u, v):
    origin, _l, t, n = poly_edge(EDGE_EMBARCADERO)
    return (origin[0] + t[0] * u - n[0] * v, origin[1] + t[1] * u - n[1] * v)


def roof_box(name, u, v, z0, z1, su, sv, mat):
    _o, _l, t, _n = poly_edge(EDGE_EMBARCADERO)
    cx, cy = uv_to_world(u, v)
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=math.atan2(t[1], t[0]))


def hip_roof(name, u, v, z0, z1, su, sv, ridge, mat):
    """Hipped roof over a rectangle on the building's own grid: two trapezoids
    along u, two triangles at the ends, plus the eave cap. ridge == 0 gives a
    pyramid."""
    _o, _l, t, _n = poly_edge(EDGE_EMBARCADERO)
    yaw = math.atan2(t[1], t[0])
    c, s = math.cos(yaw), math.sin(yaw)
    cx, cy = uv_to_world(u, v)

    def w(lx, ly, z):
        return (cx + lx * c - ly * s, cy + lx * s + ly * c, z)

    a, b, r = su / 2.0, sv / 2.0, ridge / 2.0
    verts = [
        w(-a, -b, z0), w(a, -b, z0), w(a, b, z0), w(-a, b, z0),
        w(-r, 0.0, z1), w(r, 0.0, z1),
    ]
    faces = [
        (0, 1, 5, 4),   # slope facing -v
        (2, 3, 4, 5),   # slope facing +v
        (1, 2, 5),      # hip end at +u
        (3, 0, 4),      # hip end at -u
        (3, 2, 1, 0),   # eave cap
    ]
    return new_mesh(name, verts, faces, [mat])


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
        # Flagged for the app's night pass; emission is off in the day asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------------- parts


def opening(tag, frame, u, profile_fn, w, z0, z1, frame_mat, fill_mat, base_d, glow_mat=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads as
    a border ring around a recessed opening. No booleans, all closed solids."""
    wall_panel(f"{tag}_frame", frame, u, profile_fn(w, z0, z1), 0.0, base_d + 0.06, frame_mat)
    inset = 0.16
    wall_panel(
        f"{tag}_fill", frame, u,
        profile_fn(w - 2 * inset, z0 + inset, z1 - inset), 0.0, base_d + 0.13, fill_mat,
    )
    if glow_mat is not None:
        g = 0.30
        wall_panel(
            f"{tag}_glow", frame, u,
            profile_fn(w - 2 * g, z0 + g, z1 - g), base_d + 0.10, base_d + 0.17, glow_mat,
        )


def cornice(tag, edges, z0, z1, proj, mat, poly=None):
    """A projecting horizontal band on selected faces only."""
    for e in edges:
        _a, length, _t, _n = poly_edge(e, poly)
        face_panel(f"{tag}_{e}", e, length / 2.0, rect_profile(length, z0, z1), 0.0, proj, mat, poly)


def shaft_floor_z(k):
    return Z_FRIEZE1 + k * FLOOR_H


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    brick = material("Toy_brick")
    rust = material("Toy_rust")
    stone = material("Toy_stone")
    cream = material("Toy_cream")
    tile = material("Toy_red")
    sand = material("Toy_sand")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    gold = material("Toy_gold")
    steel = material("Toy_steel")
    ink = material("Toy_ink")
    glass_glow = material("Toy_glass_Glow")
    gold_glow = material("Toy_gold_Glow")
    white_glow = material("Toy_white_Glow")

    # The eight-storey mass: the footprint clipped to WING_DEPTH from the
    # Embarcadero face. n_in points INTO the block (away from that face).
    _o_e, len_emb, t_emb, n_emb = poly_edge(EDGE_EMBARCADERO)
    n_in = (-n_emb[0], -n_emb[1])
    c_face = _o_e[0] * n_in[0] + _o_e[1] * n_in[1]
    WING_POLY = clip_halfplane(FOOTPRINT, n_in, c_face + WING_DEPTH)

    emb = edge_wall(EDGE_EMBARCADERO)
    steuart = edge_wall(EDGE_STEUART)
    _a_s, len_ste, _t_s, _n_s = poly_edge(EDGE_STEUART)

    # --- masses ------------------------------------------------------------
    prism("podium", FOOTPRINT, 0.0, Z_PODIUM - 0.30, brick, mat_caps=sand)
    prism("wings", WING_POLY, 0.0, Z_WING - 0.30, brick, mat_caps=sand)

    # roof decks laid on top, so the court can be a recess with no boolean
    ring_band("podium_deck", FOOTPRINT, Z_PODIUM - 0.30, Z_PODIUM - 0.05, -0.45, 0.0, sand)
    roof_box("podium_fill", len_emb / 2.0, (WING_DEPTH + 42.27) / 2.0,
             Z_PODIUM - 0.30, Z_PODIUM - 0.05, len_emb, 42.27 - WING_DEPTH, sand)

    # --- the cast-stone base and its corbel frieze -------------------------
    ring_band("stone_base", FOOTPRINT, 0.0, Z_STONE_TOP, 0.0, BASE_PROJ, stone)
    cornice("frieze", (EDGE_EMBARCADERO, EDGE_CHAMFER), Z_STONE_TOP, Z_FRIEZE1,
            FRIEZE_PROJ, stone)
    # the corbels themselves: a rank of small blocks under that band, the
    # strongest ornament on the building and cheap as boxes on the wall plane
    for i in range(24):
        u = (i + 0.5) * len_emb / 24.0
        wall_panel(f"corbel_{i}", emb, u, rect_profile(0.62, Z_STONE_TOP - 0.62, Z_STONE_TOP),
                   BASE_PROJ, FRIEZE_PROJ - 0.06, stone)

    # --- the Embarcadero elevation -----------------------------------------
    pitch = len_emb / BAYS_EMBARCADERO
    for i in range(BAYS_EMBARCADERO + 1):
        wall_panel(
            f"emb_pier{i}", emb,
            min(max(i * pitch, PIER_W / 2.0), len_emb - PIER_W / 2.0),
            rect_profile(PIER_W, Z_FRIEZE1, Z_ARCH0), 0.0, PIER_PROJ, brick,
        )
    open_w = pitch - PIER_W - 0.40
    for i, u in enumerate(bay_centres(EDGE_EMBARCADERO, BAYS_EMBARCADERO)):
        # two-storey cast-stone base: a tall shopfront-scale opening, then a
        # small round-headed window above it
        opening(f"emb_g{i}", emb, u, rect_profile, open_w, Z_G0, Z_G1, stone, ink, BASE_PROJ)
        opening(f"emb_s{i}", emb, u, arch_profile, open_w * 0.55, Z_S0, Z_S1,
                stone, glass, BASE_PROJ)
        # brick shaft
        for k in range(SHAFT_FLOORS):
            z0 = shaft_floor_z(k) + SHAFT_WIN_SILL
            lit = (i * 5 + k * 3) % 9 < 2
            opening(f"emb_w{i}_{k}", emb, u, rect_profile, open_w * 0.62, z0, z0 + SHAFT_WIN_H,
                    stone, glass, 0.0, glass_glow if lit else None)
        # the ornamented eighth storey: tall arched openings
        opening(f"emb_a{i}", emb, u, arch_profile, open_w * 0.80, Z_ARCH0 + 0.55,
                Z_ARCH0 + 0.55 + ARCH_WIN_H, stone, glass, 0.0,
                glass_glow if i % 4 == 1 else None)

    # the balustraded balcony across the centre of the arched storey
    wall_panel("emb_balcony", emb, len_emb / 2.0,
               rect_profile(len_emb * 0.46, Z_ARCH0, Z_ARCH0 + 0.55), 0.0, 0.85, stone)
    # the main entry: a round-headed portal with terracotta shields
    u_entry = len_emb * 0.50
    wall_panel("entry_arch", emb, u_entry, arch_profile(4.60, 0.0, 6.10), 0.0,
               BASE_PROJ + 0.05, stone)
    wall_panel("entry_recess", emb, u_entry, arch_profile(3.60, 0.10, 5.60), 0.0,
               BASE_PROJ + 0.14, ink)
    wall_panel("entry_glow", emb, u_entry, arch_profile(3.10, 0.35, 5.20),
               BASE_PROJ + 0.11, BASE_PROJ + 0.19, gold_glow)
    for du in (-3.55, 3.55):
        wall_panel(f"shield{du:+.0f}", emb, u_entry + du,
                   rect_profile(1.35, 5.10, 6.45), BASE_PROJ, BASE_PROJ + 0.22, gold)

    # cornice and the crest parapet
    cornice("emb_cornice", (EDGE_EMBARCADERO, EDGE_CHAMFER), Z_WING - 1.05, Z_WING - 0.30,
            CORNICE_PROJ, stone, WING_POLY)
    ring_band("wing_parapet", WING_POLY, Z_WING - 0.30, Z_WING, -PARAPET_T, 0.06, stone)
    # three raised crowns: one over each end bay and one over the centre
    for frac, w in ((0.09, 6.4), (0.50, 9.0), (0.91, 6.4)):
        wall_panel(f"crest{frac:.2f}", emb, len_emb * frac,
                   rect_profile(w, Z_WING - 0.20, Z_CREST), -PARAPET_T, 0.10, stone)
        wall_panel(f"crest_panel{frac:.2f}", emb, len_emb * frac,
                   rect_profile(w - 1.6, Z_WING + 0.25, Z_CREST - 0.45), 0.06, 0.20, brick)

    # --- the flanks -------------------------------------------------------
    # First aerial review: both wing flanks came back as 28 m of unbroken brick,
    # which reads as an unfinished model rather than as a party wall. The real
    # flanks ARE fenestrated — the northwest one faces an open yard and the
    # southeast one a light well — so they get the shaft rhythm without any of
    # the Embarcadero's ornament. This is the cheapest 3,000 triangles in the
    # asset and it is what stops the building looking like a solid block from
    # three of the app's four approach angles.
    for ei in range(len(WING_POLY)):
        _fa, flen, ft, fn = poly_edge(ei, WING_POLY)
        bearing = math.degrees(math.atan2(fn[0], fn[1])) % 360
        if flen < 9.0 or not (100.0 < bearing < 170.0 or 280.0 < bearing < 350.0):
            continue
        fframe = edge_wall(ei, WING_POLY)
        nb = max(3, int(round(flen / 3.55)))
        fw = flen / nb * 0.46
        for i, u in enumerate(bay_centres(ei, nb, WING_POLY)):
            for k in range(SHAFT_FLOORS + 1):
                z0 = shaft_floor_z(k) + SHAFT_WIN_SILL
                if z0 + SHAFT_WIN_H > Z_WING - 1.4:
                    continue
                lit = (i * 3 + k * 5 + ei) % 11 < 2
                opening(f"fl{ei}_{i}_{k}", fframe, u, rect_profile, fw, z0, z0 + SHAFT_WIN_H,
                        stone, glass, 0.0, glass_glow if lit else None)

    # --- the Steuart Street street wall (three storeys, two materials) ------
    # NW half = 161-165 Harbor Court, cream stucco; SE half = 169 Embarcadero
    # YMCA, dark brick. The tall mass is 12.7 m behind this wall.
    half = len_ste / 2.0
    face_panel("ste_stucco", EDGE_STEUART, half / 2.0, rect_profile(half, 0.0, Z_PODIUM),
               0.0, 0.22, cream)
    face_panel("ste_brick", EDGE_STEUART, half + half / 2.0,
               rect_profile(half, 0.0, Z_PODIUM - 0.35), 0.0, 0.22, rust)
    face_panel("ste_coping", EDGE_STEUART, len_ste / 2.0,
               rect_profile(len_ste, Z_PODIUM - 0.35, Z_PODIUM), -0.05, 0.34, stone)
    ste_pitch = len_ste / BAYS_STEUART
    for i, u in enumerate(bay_centres(EDGE_STEUART, BAYS_STEUART)):
        harbor = u < half
        wallmat = cream if harbor else rust
        # ground floor: a dark frontage band
        opening(f"ste_g{i}", steuart, u, rect_profile, ste_pitch - 1.15, 0.35, 4.10,
                wallmat, ink, 0.22)
        if harbor:
            # tall round-headed second-storey openings with a bay window in them
            opening(f"ste_a{i}", steuart, u, arch_profile, ste_pitch - 1.35, 5.05, 9.15,
                    stone, glass, 0.22, glass_glow if i % 3 == 0 else None)
            opening(f"ste_t{i}", steuart, u, arch_profile, (ste_pitch - 1.35) * 0.42,
                    10.20, 12.60, stone, glass, 0.22)
        else:
            # deep square reveals with projecting three-sided bay windows
            for z0, z1 in ((5.15, 8.35), (9.10, 12.30)):
                wall_panel(f"ste_r{i}_{z0:.0f}", steuart, u,
                           rect_profile(ste_pitch - 1.30, z0, z1), 0.22, 0.34, ink)
                opening(f"ste_b{i}_{z0:.0f}", steuart, u, rect_profile,
                        (ste_pitch - 1.30) * 0.72, z0 + 0.35, z1 - 0.35,
                        stone, glass, 0.34, glass_glow if (i + int(z0)) % 3 == 0 else None)
    # the two entrances and the YMCA fascia (the third night accent)
    wall_panel("hc_canopy", steuart, half * 0.62, rect_profile(5.20, 4.10, 4.62),
               0.20, 1.75, stone)
    wall_panel("ymca_fascia", steuart, half + half * 0.42, rect_profile(6.80, 3.35, 4.35),
               0.22, 0.40, ink)
    wall_panel("ymca_fascia_glow", steuart, half + half * 0.42,
               rect_profile(5.60, 3.55, 4.15), 0.38, 0.46, white_glow)
    wall_panel("ymca_blade", steuart, half + half * 0.72, rect_profile(1.15, 5.20, 9.60),
               0.22, 0.62, ink)
    wall_panel("ymca_blade_glow", steuart, half + half * 0.72,
               rect_profile(0.80, 5.45, 9.35), 0.60, 0.68, white_glow)

    # --- the tower and its tile roof ---------------------------------------
    tw, td = TOWER
    tu, tv = len_emb * TOWER_U_FRAC, TOWER_V
    roof_box("tower", tu, tv, Z_WING - 0.60, Z_TOWER_EAVE - 0.55, tw, td, brick)
    # the ninth storey inside the tower body: one rank of windows so the band
    # between the wing roof and the arcade is not blank brick
    for side, (du, dv, su, sv, along_u) in enumerate((
        (0.0, -td / 2.0, tw, 0.0, True),
        (0.0, td / 2.0, tw, 0.0, True),
        (-tw / 2.0, 0.0, 0.0, td, False),
        (tw / 2.0, 0.0, 0.0, td, False),
    )):
        span = su if along_u else sv
        for k in range(5):
            off = (k + 0.5) * span / 5.0 - span / 2.0
            ou, ov = (off, 0.0) if along_u else (0.0, off)
            wu, wv = (1.15, 0.30) if along_u else (0.30, 1.15)
            roof_box(f"twr{side}_{k}", tu + du + ou, tv + dv + ov,
                     Z_WING + 0.75, Z_ARCADE0 - 0.65, wu, wv, glass)

    # the arcaded storey: a recessed band with regular square-cut reveals. At
    # city scale a notched band IS an arcade; modelled arches cost 10x.
    roof_box("tower_arcband", tu, tv, Z_ARCADE0, Z_TOWER_EAVE - 0.55, tw + 0.14, td + 0.14, stone)
    for side, (du, dv, su, sv) in enumerate((
        (0.0, -td / 2.0 - 0.10, tw, 0.30),
        (0.0, td / 2.0 + 0.10, tw, 0.30),
        (-tw / 2.0 - 0.10, 0.0, 0.30, td),
        (tw / 2.0 + 0.10, 0.0, 0.30, td),
    )):
        span = su if su > sv else sv
        n_arc = 9 if span > 12 else 8
        for k in range(n_arc):
            off = (k + 0.5) * span / n_arc - span / 2.0
            ou, ov = (off, 0.0) if su > sv else (0.0, off)
            aw = span / n_arc * 0.52
            aku, akv = (aw, 0.42) if su > sv else (0.42, aw)
            roof_box(f"arc{side}_{k}", tu + du + ou, tv + dv + ov,
                     Z_ARCADE0 + 0.55, Z_TOWER_EAVE - 1.05, aku, akv, ink)
            # The glow shell must be PROUD of the opaque reveal behind it: the
            # first night render put it inside the ink box and the night hero
            # simply did not light. It keeps the reveal's across-wall axis 0.14 m
            # thicker so it pokes out on the visible side, and is inset in plane.
            gku, gkv = (aku * 0.66, 0.56) if su > sv else (0.56, akv * 0.66)
            roof_box(f"arcg{side}_{k}", tu + du + ou, tv + dv + ov,
                     Z_ARCADE0 + 0.75, Z_TOWER_EAVE - 1.25, gku, gkv, gold_glow)
    roof_box("tower_eave", tu, tv, Z_TOWER_EAVE - 0.55, Z_TOWER_EAVE,
             tw + 2 * EAVE_OVER, td + 2 * EAVE_OVER, stone)
    hip_roof("tile_roof", tu, tv, Z_TOWER_EAVE, Z_APEX,
             tw + 2 * EAVE_OVER, td + 2 * EAVE_OVER, ROOF_RIDGE, tile)
    # a finial on the ridge, kept below the apex so it cannot set the bbox
    roof_box("finial", tu, tv, Z_APEX - 1.35, Z_APEX - 0.25, 0.70, 0.70, gold)

    # --- roofs: court, plant, bulkheads ------------------------------------
    cw, cd = COURT
    roof_box("court", len_emb / 2.0, COURT_V, Z_WING - 0.32, Z_WING - 0.22, cw, cd, ink)
    for i, (u, v, sw, sd, h) in enumerate((
        (7.5, 24.5, 4.6, 3.4, 2.10),
        (34.0, 25.5, 3.8, 2.8, 1.60),
        (12.0, 5.5, 3.0, 2.4, 1.25),
        (30.5, 5.0, 3.0, 2.4, 1.25),
    )):
        roof_box(f"plant{i}", u, v, Z_WING - 0.30, Z_WING - 0.30 + h, sw, sd, steel)
    roof_box("bulkhead", 20.9, 27.0, Z_WING - 0.30, Z_WING + 2.35, 6.2, 4.0, brick)
    for i, (u, v) in enumerate(((6.0, 34.5), (14.5, 37.5), (26.0, 33.5), (34.5, 36.5),
                                (20.0, 39.0), (10.0, 31.5))):
        roof_box(f"pvent{i}", u, v, Z_PODIUM - 0.05, Z_PODIUM + 0.85, 1.35, 1.35, steel)
    roof_box("pstair", 30.0, 38.5, Z_PODIUM - 0.05, Z_PODIUM + 2.30, 5.0, 3.6, rust)
    roof_box("ppanel", 17.0, 34.0, Z_PODIUM - 0.05, Z_PODIUM + 0.30, 9.0, 5.0, ink)

    # Bevel budget: the chunky masses, the base, the cornices and the tile roof
    # carry the miniature read and take the full 0.10/2. Applied panels are small
    # and numerous — their frames get a token softening, fills and glow none.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")) or obj.name.startswith(("arcg", "arc", "twr")):
            continue
        if obj.name.endswith("_frame") or obj.name.startswith(("emb_pier", "corbel")):
            bevel(obj, width=0.04, segments=1)
        else:
            bevel(obj, width=0.10, segments=2)

    # The bevel rounds the hip apex down by ~50 mm, which would leave the
    # bounding box short of the target height and make the loader's
    # targetHeightM/measuredHeight scale 1.001 instead of 1.0. Correct it on the
    # roof object alone, about its eave, so the export tops out at exactly Z_APEX.
    roof = bpy.data.objects.get("tile_roof")
    if roof is not None:
        top = max((roof.matrix_world @ v.co).z for v in roof.data.vertices)
        k = (Z_APEX - Z_TOWER_EAVE) / (top - Z_TOWER_EAVE)
        for v in roof.data.vertices:
            v.co.z = Z_TOWER_EAVE + (v.co.z - Z_TOWER_EAVE) * k

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
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    print("[build] anchor lon/lat: -122.3919821 37.7926993 (parcel centroid)")
    print("[build] Embarcadero front heading: 45.1 deg true (NE)")
    print("[build] Steuart Street elevation heading: 225.1 deg true (SW)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "169-steuart.blend")
    glb = os.path.join(out, "169-steuart.glb")
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
