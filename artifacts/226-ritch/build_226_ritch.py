"""Deterministic Blender build of the SF-SIM miniature 226 Ritch Street.

    blender -b --python build_226_ritch.py -- [--out DIR]

Writes 226-ritch.blend and 226-ritch.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = DataSF footprint SF3776120 oriented-bounding-box centre
(anchor lon -122.3960899, lat 37.7804376), min Z = 0, crest exactly 18.10 m.

Design (see REFERENCE.md for the sources behind every number, and REPORT.md for
the corrections this build made to the plan):

* the measured footprint: a 12.13 x 22.80 m rectangle on the SOUTH-WEST side of
  Ritch Street at bearing 45.6/225.6 deg, front facing NE onto the alley. Narrow
  and deep — a slot building between two party walls;
* three live/work loft storeys of ~4.5 m floor-to-floor (the listings' "15-foot
  ceilings") over a ground-floor garage, wood frame, 1994-96. Parapet 16.0 m,
  which is why a three-storey building is as tall as a five-storey one;
* the front is split lengthwise: big white multi-lite loft windows on the SE
  half, recessed railed loggias on the NW half with a galvanised fire escape
  zig-zagging across them to the roof;
* sage-green stucco body, sand-tiled ground band, one saturated red roll-up
  garage door. The green is the recognition cue on an alley of grey concrete;
* the exposed flanks and rear are pale vinyl siding (1998 permits), a service
  treatment, not the stucco;
* roof: membrane, a tiled deck with a railing over the front half, a row of
  skylight domes down the spine, one mechanical box, and the stair bulkhead
  that carries the crest to 18.10 m (DataSF LiDAR hgt_max 18.14 m);
* night state: the six SE-half loft windows are the hero glow, plus the entry.
  The loggias stay dark. Glow surfaces are thin shells proud of the opaque
  glazing (the app renders _Glow in a separate layer — never author a primary
  surface as glow).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF SF3776120 oriented bounding box, 12.13 m frontage x 22.80 m depth,
# frontage bearing 135.6 deg, recentred on the OBB centre (the anchor).
# CCW in (east, north), 4 corners.
_HF = 12.13 / 2.0          # half frontage
_HD = 22.80 / 2.0          # half depth
_BF = math.radians(135.6)  # frontage bearing, NW -> SE
_F = (math.sin(_BF), math.cos(_BF))            # along the frontage, toward SE
_D = (math.sin(_BF + math.pi / 2), math.cos(_BF + math.pi / 2))  # toward the rear (SW)


def _corner(sf, sd):
    return (sf * _HF * _F[0] + sd * _HD * _D[0], sf * _HF * _F[1] + sd * _HD * _D[1])


# NW-front, NW-rear, SE-rear, SE-front  -> counter-clockwise
FOOTPRINT = [_corner(-1, -1), _corner(-1, 1), _corner(1, 1), _corner(1, -1)]

# Edge index -> elevation. Outward normals verified against the survey bearings.
# Edge 0: 22.80 m, faces NW 315.6 deg — party wall to 218 Ritch (siding)
# Edge 1: 12.13 m, faces SW 225.6 deg — rear, into the block interior (siding)
# Edge 2: 22.80 m, faces SE 135.6 deg — flank toward 230 Ritch (stucco)
# Edge 3: 12.13 m, faces NE  45.6 deg — RITCH STREET FRONT (the designed face)
EDGE_NW = 0
EDGE_REAR = 1
EDGE_SE = 2
EDGE_FRONT = 3

Z_BASE_TOP = 2.35     # top of the sand-tiled ground band (measured)
Z_L1 = 2.60           # first loft floor level
Z_ROOF = 15.60        # roof membrane
Z_PARAPET = 16.00     # street parapet crest (OSM height=16, LiDAR median 15.90)
Z_CREST = 18.10       # stair bulkhead crest = bbox top (LiDAR hgt_max 18.14)

# Loft window bands, three levels at ~4.5 m floor-to-floor.
BANDS = ((3.20, 6.40), (7.70, 10.90), (12.20, 14.40))
BAND_TOP_SHRINK = 0.0  # third band already shortened above

# Fire-escape landing levels on the NW half of the front.
FE_LEVELS = (4.20, 8.70, 13.20)

PALETTE_HEX = {
    "Toy_sage": "8a9d76",        # body stucco — the recognition cue
    "Toy_ash": "c8c4bc",         # vinyl siding, flanks and rear (1998 permits)
    "Toy_warm": "cbbb96",        # sand-tiled ground band
    "Toy_ioorange": "c0402a",    # the red roll-up garage door
    "Toy_white": "f7f4ec",       # window frames and mullions
    "Toy_glass": "2a4d73",       # glazing
    "Toy_ink": "3a3530",         # loggia rails, roof railing, door reveals
    "Toy_steel": "9aa0a6",       # fire escape, mechanical, skylight kerbs
    "Toy_trim": "f3efe6",        # parapet cap, bulkhead
    "Toy_roofd": "45454a",       # roof membrane
    "Toy_terra": "a9634a",       # roof-deck tile
    "Toy_bark": "6d6154",        # stained timber service door
    "Toy_glass_Glow": "6f95b8",  # lit loft windows at night
    "Toy_white_Glow": "f7f4ec",  # entry spill at the base
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def poly_edge(i):
    """Edge i of FOOTPRINT: (origin, length, tangent unit, outward normal)."""
    a = FOOTPRINT[i]
    b = FOOTPRINT[(i + 1) % len(FOOTPRINT)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


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


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


# ------------------------------------------------- building-local (u, v) frame
# u runs along the FRONT edge, 0 at its SE end, +12.13 at its NW end.
# u_c = u - 6.065 is the same axis centred on the building.
# v runs from the front (-11.40) to the rear (+11.40).

_A_FRONT, L_FRONT, T_FRONT, N_FRONT = poly_edge(EDGE_FRONT)
L_FLANK = poly_edge(EDGE_NW)[1]
V_AXIS = (-N_FRONT[0], -N_FRONT[1])  # inward = toward the rear


def uv(u_c, v):
    """(u_c along the frontage, + toward NW; v across, + toward the rear) -> world."""
    return (T_FRONT[0] * u_c + V_AXIS[0] * v, T_FRONT[1] * u_c + V_AXIS[1] * v)


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


def bevel(obj, width=0.12, segments=2):
    """Miniature-style edge softening on the chunky solids (style bible s.4)."""
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


def prism(name, poly, z0, z1, mat, mat_caps=None, wall_mats=None):
    """Closed extrusion of a CCW polygon (walls + both caps).

    `wall_mats` optionally gives one material per polygon edge, which is how the
    stucco street front and the vinyl-sided flanks live on one solid.
    """
    npts = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces, face_mats = [], []
    mats = [mat]
    if wall_mats:
        for m in wall_mats:
            if m not in mats:
                mats.append(m)
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
        face_mats.append(mats.index(wall_mats[i]) if wall_mats else 0)
    cap = mat_caps if mat_caps else mat
    if cap not in mats:
        mats.append(cap)
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    face_mats += [mats.index(cap)] * 2
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


def face_panel(name, edge, u_centre, profile, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in the plane of wall `edge`,
    extruded outward from offset d0 to d1 along that wall's normal."""
    a, _length, t, n = poly_edge(edge)
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


def uv_box(name, u_c, v, z0, z1, su, sv, mat, mat_caps=None):
    """Box on the building's own grid rather than the world axes."""
    corners = [uv(u_c + lu, v + lv) for lu, lv in
               ((-su / 2, -sv / 2), (-su / 2, sv / 2), (su / 2, sv / 2), (su / 2, -sv / 2))]
    if (corners[1][0] - corners[0][0]) * (corners[2][1] - corners[1][1]) - \
       (corners[1][1] - corners[0][1]) * (corners[2][0] - corners[1][0]) < 0:
        corners.reverse()
    return prism(name, corners, z0, z1, mat, mat_caps)


def uv_ngon(name, u_c, v, z0, z1, r, sides, mat):
    poly = []
    for i in range(sides):
        a = 2 * math.pi * i / sides
        poly.append(uv(u_c + r * math.cos(a), v + r * math.sin(a)))
    return prism(name, poly, z0, z1, mat)


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
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------------- parts


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None, mullions=0,
                 transom=True):
    """Frame panel + a smaller fill that protrudes further, so the frame reads as
    a border ring around a recessed opening. No booleans, all closed solids.

    `mullions` adds N chunky vertical bars across the fill — the multi-lite loft
    windows are a texture at this scale, so they are spent as bars, not panes.
    """
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, 0.07, frame_mat)
    inset = 0.16
    face_panel(
        f"{tag}_fill", edge, u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset), 0.0, 0.13, fill_mat,
    )
    if glow_mat is not None:
        g = 0.30
        face_panel(
            f"{tag}_glow", edge, u,
            rect_profile(w - 2 * g, z0 + g, z1 - g), 0.10, 0.17, glow_mat,
        )
    for m in range(mullions):
        du = (m + 1) * (w - 2 * inset) / (mullions + 1) - (w - 2 * inset) / 2
        face_panel(
            f"{tag}_mull{m}", edge, u + du,
            rect_profile(0.13, z0 + inset, z1 - inset), 0.11, 0.19, frame_mat,
        )
    # one horizontal transom, the other half of the multi-lite read
    if transom:
        zc = (z0 + z1) / 2.0
        face_panel(
            f"{tag}_transom", edge, u,
            rect_profile(w - 2 * inset, zc - 0.07, zc + 0.07), 0.11, 0.19, frame_mat,
        )


def loggia(tag, edge, u, w, z0, z1, frame_mat, rail_mat):
    """A loggia: a light frame ring around a dark panel that reads as the shaded
    interior, plus a solid rail panel across its mouth. There are no booleans in
    this framework, so depth is a value trick, not geometry — which is also the
    right answer at this detail tier."""
    face_panel(f"{tag}_reveal", edge, u, rect_profile(w, z0, z1), 0.0, 0.07, frame_mat)
    face_panel(f"{tag}_back", edge, u,
               rect_profile(w - 0.28, z0 + 0.14, z1 - 0.14), 0.0, 0.12,
               material("Toy_glass"))
    face_panel(f"{tag}_rail", edge, u,
               rect_profile(w + 0.10, z0, z0 + 1.00), 0.10, 0.24, rail_mat)


def fire_escape(edge, steel):
    """Three landings and the flights between them, on the NW half of the front.

    Solid stringers, one ramped slab per flight, solid rail panels — no
    balusters. This is the element that eats a triangle budget if it is modelled
    honestly, and it reads from the street as a zig-zag of pale steel.
    """
    u_lo, u_hi = 6.70, 9.20           # over the garage door, clear of the loggias
    for i, z in enumerate(FE_LEVELS):
        # landing slab + its rail
        face_panel(f"fe_land{i}", edge, (u_lo + u_hi) / 2,
                   rect_profile(u_hi - u_lo, z - 0.12, z), 0.10, 1.15, steel)
        face_panel(f"fe_rail{i}", edge, (u_lo + u_hi) / 2,
                   rect_profile(u_hi - u_lo, z, z + 0.95), 1.05, 1.15, steel)
        # flight up to the next level (or to the parapet from the top landing)
        z_next = FE_LEVELS[i + 1] if i + 1 < len(FE_LEVELS) else Z_PARAPET
        # a ramped slab: a quad prism in the wall plane, sloping across u
        a, _l, t, n = poly_edge(edge)
        run_lo, run_hi = (u_lo + 0.25, u_hi - 0.25)
        if i % 2:                       # alternate the run so it reads as a zig-zag
            run_lo, run_hi = run_hi, run_lo
        prof = [(run_lo, z), (run_hi, z_next - 0.34), (run_hi, z_next), (run_lo, z + 0.34)]
        verts = []
        for d in (0.42, 0.86):
            for du, zz in prof:
                verts.append((a[0] + t[0] * du + n[0] * d, a[1] + t[1] * du + n[1] * d, zz))
        faces = [(0, 1, 2, 3)[::-1], (4, 5, 6, 7),
                 (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        new_mesh(f"fe_flight{i}", verts, faces, [steel])


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    sage = material("Toy_sage")
    ash = material("Toy_ash")
    warm = material("Toy_warm")
    red = material("Toy_ioorange")
    white = material("Toy_white")
    glass = material("Toy_glass")
    ink = material("Toy_ink")
    steel = material("Toy_steel")
    trim = material("Toy_trim")
    roofd = material("Toy_roofd")
    terra = material("Toy_terra")
    bark = material("Toy_bark")
    gglow = material("Toy_glass_Glow")
    wglow = material("Toy_white_Glow")

    # --- body -----------------------------------------------------------------
    # Two stacked volumes: the sand-tiled ground band and the stucco/siding body.
    # Per-edge materials put stucco on the two faces that are seen from the alley
    # (front, SE flank) and pale vinyl siding on the two that the 1998 permits
    # re-clad (NW party wall, rear).
    wall_mats = [None] * 4
    wall_mats[EDGE_NW] = ash
    wall_mats[EDGE_REAR] = ash
    wall_mats[EDGE_SE] = sage
    wall_mats[EDGE_FRONT] = sage
    base_mats = [warm if e in (EDGE_FRONT, EDGE_SE) else ash for e in range(4)]

    prism("body_base", FOOTPRINT, 0.0, Z_BASE_TOP, warm, mat_caps=warm, wall_mats=base_mats)
    prism("body_upper", FOOTPRINT, Z_BASE_TOP, Z_ROOF, sage, mat_caps=roofd, wall_mats=wall_mats)

    # thin shadow reveal where the tiled base meets the stucco
    ring_band("base_cap", FOOTPRINT, Z_BASE_TOP - 0.10, Z_BASE_TOP + 0.04, -0.02, 0.09, trim)

    # --- parapet --------------------------------------------------------------
    ring_band("parapet", FOOTPRINT, Z_ROOF, Z_PARAPET, -0.02, 0.13, trim)

    # --- RITCH STREET FRONT (NE) ---------------------------------------------
    # u = 0 at the SE end of the frontage, 12.13 at the NW end.
    # Ground band, NW -> SE: service door, residential entry, garage door,
    # then plain tiled wall.
    rect_opening("garage", EDGE_FRONT, 7.90, 2.83, 0.0, 2.25, trim, red, transom=False)
    rect_opening("entry", EDGE_FRONT, 10.90, 1.90, 0.0, 2.60, white, glass, wglow)

    # SE half: the loft windows — two per level, white frames with chunky
    # mullions standing in for the multi-lite grids.
    LOFT_U = (1.75, 4.65)
    LIT = {(0, 0), (0, 1), (1, 1), (2, 0)}
    for fi, (za, zb) in enumerate(BANDS):
        for i, u in enumerate(LOFT_U):
            w, z0, z1 = 2.60, za, zb
            if fi == 2:                      # the top level's windows are smaller
                w, z0, z1 = 1.70, za, za + 2.00
            rect_opening(
                f"loft{fi}_{i}", EDGE_FRONT, u, w, z0, z1, white, glass,
                gglow if (fi, i) in LIT else None, mullions=2 if fi < 2 else 1,
            )

    # NW half: the recessed loggias, one per level, with their rails.
    for fi, (za, zb) in enumerate(BANDS):
        z1 = zb if fi < 2 else za + 2.00
        loggia(f"log{fi}", EDGE_FRONT, 10.55, 2.30, za, z1, trim, ink)

    # the fire escape crossing them
    fire_escape(EDGE_FRONT, steel)

    # --- SE flank: stucco, a few small openings toward the light gap ----------
    for fi, (za, zb) in enumerate(BANDS):
        for i, u in enumerate((4.5, 11.0, 17.5)):
            rect_opening(f"se{fi}_{i}", EDGE_SE, u, 1.10, za + 0.5, za + 2.1, white, glass)

    # --- NW party wall and rear: service faces, minimal openings -------------
    for i, u in enumerate((6.0, 15.0)):
        for fi, (za, _zb) in enumerate(BANDS):
            rect_opening(f"nw{fi}_{i}", EDGE_NW, u, 0.80, za + 0.7, za + 1.9, white, glass)
    rect_opening("reardoor", EDGE_REAR, 3.20, 1.10, 0.0, 2.20, ink, bark, transom=False)
    for fi, (za, _zb) in enumerate(BANDS):
        for i, u in enumerate((3.2, 6.1, 9.0)):
            rect_opening(f"rr{fi}_{i}", EDGE_REAR, u, 1.20, za + 0.5, za + 2.2, white, glass)

    # --- roof ----------------------------------------------------------------
    # membrane is the cap of body_upper; everything else sits on it.
    # Roof deck over the front half of the NW side, with its railing.
    DECK_U, DECK_V, DECK_SU, DECK_SV = 2.00, -6.60, 5.00, 5.60
    uv_box("roof_deck", DECK_U, DECK_V, Z_ROOF, Z_ROOF + 0.14, DECK_SU, DECK_SV, terra)
    deck_poly = [uv(DECK_U + lu, DECK_V + lv) for lu, lv in
                 ((-DECK_SU / 2, -DECK_SV / 2), (-DECK_SU / 2, DECK_SV / 2),
                  (DECK_SU / 2, DECK_SV / 2), (DECK_SU / 2, -DECK_SV / 2))]
    ring_band("deck_rail", deck_poly, Z_ROOF + 0.14, Z_ROOF + 0.90, -0.05, 0.05, ink)

    # Skylight domes down the spine — a deliberate rhythm, not scattered vents.
    for i, v in enumerate((-6.0, -3.0, 0.0, 3.0, 6.0)):
        uv_ngon(f"skylight{i}", -2.30, v, Z_ROOF, Z_ROOF + 0.16, 0.58, 8, steel)
        uv_ngon(f"skydome{i}", -2.30, v, Z_ROOF + 0.16, Z_ROOF + 0.52, 0.46, 8, trim)

    # The stair bulkhead that carries the crest, set back behind the deck.
    uv_box("bulkhead", 2.60, 0.60, Z_ROOF, Z_CREST, 3.40, 3.80, trim, mat_caps=roofd)
    uv_box("bulk_door", 2.60, 0.60 - 3.80 / 2 - 0.03, Z_ROOF, Z_ROOF + 1.95, 0.95, 0.10, steel)

    # One mechanical box on the rear third.
    uv_box("mech", -3.10, 7.60, Z_ROOF, Z_ROOF + 0.85, 2.00, 1.50, steel)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. The window panels are small and numerous — their frames get a
    # token 1-segment softening and the fills, glow shells and mullions none.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow", "_back")) or "_mull" in obj.name:
            continue
        if obj.name.endswith(("_frame", "_transom", "_reveal", "_rail")):
            bevel(obj, width=0.05, segments=1)
        elif obj.name.startswith(("fe_", "skylight", "skydome", "deck_rail", "bulk_door")):
            bevel(obj, width=0.04, segments=1)
        else:
            bevel(obj, width=0.12, segments=2)

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
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    print("[build] anchor lon/lat: -122.3960899 37.7804376 (DataSF SF3776120 OBB centre)")
    print("[build] Ritch Street front heading: 45.6 deg true (NE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "226-ritch.blend")
    glb = os.path.join(out, "226-ritch.glb")
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
