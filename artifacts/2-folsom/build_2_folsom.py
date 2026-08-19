"""Deterministic Blender build of the SF-SIM miniature 2 Folsom Street.

    blender -b --python build_2_folsom.py -- [--out DIR]

Writes 2-folsom.blend and 2-folsom.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint OBB centre (anchor lon -122.390975,
lat 37.790787), min Z = 0, limestone crown exactly 88.00 m.

Design (see REFERENCE.md for the sources behind every number):

* Robert A.M. Stern Architects with Gensler, 2001; Gap Inc.'s owner-occupied
  global headquarters, addressed both 2 Folsom Street and 250 Embarcadero.
  Fifteen storeys — RAMSA's "six story base with a fifteen story superstructure"
  is fifteen IN TOTAL, confirmed by Gap Inc.'s own 2022 press release and by
  CB Engineers, and by the arithmetic: the measured 32.28 m base roof is seven
  levels at 4.6 m, exactly what a 10'8" ceiling over an underfloor air plenum
  produces, and the measured 72.11 m deck is 8.6 more of them;
* the recognition cue is a THREE-MASS STACK stepping up toward the harbour.
  Every other SoMa landmark in this set is one box with a parapet. Here it is
  a whole-block base at 32.3 m, a red-brick superstructure set 16 m back from
  the block centre toward Spear Street, and a limestone tower standing at the
  superstructure's NORTHEAST corner and stepping twice to a crown at 88.0 m.
  Flatten that into one extrusion and the building is gone;
* the second cue is the two-material split: red brick body, tawny limestone
  tower / piers / frames / cornices. It is what tells the masses apart from a
  kilometre up;
* the third is the roof, because the camera looks down and this is 6,341 m2 of
  designed terrace at 32.3 m: the seven-storey atrium's gridded glass skylight
  in the northeast quadrant, two Olin lawn parterres, hedge parterres in ranks,
  and a wide paved ring inside the limestone parapet;
* all three roof planes are MEASURED, from one DataSF LiDAR row over 25,463
  cells at 50 cm: median 32.28 m (base terrace), majority/mode 72.11 m (the
  superstructure deck — a large dead-flat plane gives a sharp mode), maximum
  87.95 m (the crown). OSM independently tags height=91. The area split
  (70.6% / 23.1% / 6.3%) was solved from the same row's mean 44.98 and sigma
  20.01 and then checked twice: against the near-nadir satellite after
  correcting a measured 1.98 px/m building lean, and against two OSM
  building:part rings at the crown. Three methods, none tuned to the others;
* the footprint's own geometry carries two of the architect's moves and both
  are modelled: the MID-BLOCK FOLSOM ENTRANCE is a real 13.6 x 3.0 m recess in
  the ring, and the Embarcadero face has a 15.15 m CENTRAL PROJECTING PAVILION
  flanked by symmetric steps — RAMSA's porticoes, "at its boldest facing the
  harbor". The two Spear-side corners step in 4.7 m; the two Embarcadero-side
  corners are square;
* the facade is built as piers + continuous spandrel bands + glass fills rather
  than as 235 individually framed openings. That is both cheaper (about a third
  of the triangles) and more faithful: RAMSA describes "large, simple,
  structural frames";
* both roof membranes are Toy_sand from the start. Settled empirically on
  524-second and confirmed on 501-second: Toy_roofd measured rgb(9,9,12) on a
  lit deck in the live scene. The two decks here total 8,200 m2, the largest
  roof area in the bespoke set;
* night state: the ATRIUM SKYLIGHT is the hero glow — one softly lit rectangle
  on a dark roof plane, which is exactly what this building looks like from the
  Bay Bridge — supported by a scatter of lit windows, the crown pavilion's
  glazing, and the 2022 ground-floor retail sign band. The limestone tower does
  NOT glow. Glow surfaces are thin shells proud of the opaque surface behind
  them (the app renders _Glow in a separate layer that is ~12% alpha per face,
  so a closed shell reads at ~23% by day and would tint the whole facade).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# The footprint's own frame: +u = northeast (The Embarcadero), +v = southeast
# (Folsom Street). The block is rotated -44.81 deg from the world axes.
ANG = math.radians(-44.81)
_C, _S = math.cos(ANG), math.sin(ANG)


def P(u, v):
    """Building (u, v) -> Blender world (x east, y north), metres.

    The footprint was reduced in the app's local frame, whose second axis is
    z = -north; Blender's is +north. The map is therefore a REFLECTION, not a
    rotation (determinant -1), and getting that wrong rotates the whole
    building 90 deg — the Embarcadero elevation ends up facing Folsom Street.
    The sign flip also means FOOTPRINT_UV is listed clockwise in (u, v) so that
    it arrives counter-clockwise in Blender, which is what makes
    edge_frame()'s n = (t_y, -t_x) an OUTWARD normal."""
    return (_C * u - _S * v, -(_S * u + _C * v))


# DataSF LiDAR footprint 201006.0000175 (mblr SF3741035), projected with the
# app's tangent projection, recentred on the OBB centre and reduced from 28
# vertices to 24. OSM way 93817368 independently gives 84.49 x 77.32 m against
# this 84.31 x 77.14 m — a 0.2% agreement, so there is no conflict to
# adjudicate. Listed CLOCKWISE in (u, v): the (u, v) -> (x, y) map has
# determinant -1, so this comes out counter-clockwise in Blender.
FOOTPRINT_UV = [
    (8.53, -38.57),     # 0
    (8.53, -35.32),     # 1   northwest service recess, near side
    (-4.67, -35.32),    # 2   northwest recess back wall
    (-4.67, -38.54),    # 3
    (-37.37, -38.54),   # 4   northwest face
    (-37.37, -34.23),   # 5   west corner step
    (-42.10, -34.23),   # 6
    (-42.10, 34.33),    # 7   Spear Street face (68.56 m, the long one)
    (-37.85, 34.33),    # 8   south corner step
    (-37.85, 38.57),    # 9
    (-4.37, 38.57),     # 10  Folsom Street face
    (-4.37, 35.55),     # 11  MID-BLOCK FOLSOM ENTRANCE recess
    (9.22, 35.55),      # 12  Folsom entrance recess back wall
    (9.22, 38.56),      # 13
    (41.90, 38.56),     # 14  Folsom Street face
    (41.90, 13.84),     # 15  Embarcadero face, north flank
    (40.60, 13.84),     # 16
    (40.60, 7.85),      # 17
    (42.15, 7.85),      # 18
    (42.15, -7.30),     # 19  EMBARCADERO CENTRAL PAVILION (15.15 m, projecting)
    (40.60, -7.30),     # 20
    (40.60, -13.70),    # 21
    (41.90, -13.70),    # 22
    (41.90, -38.57),    # 23  Embarcadero face, south flank
]
FOOTPRINT = [P(u, v) for u, v in FOOTPRINT_UV]

# Edge index -> (bay count). Only the long wall planes are articulated; the
# 1.3-1.6 m returns between them are left plain. Outward normals are derived
# from the polygon winding, not asserted.
BAYS = {
    1: 2,    # northwest service recess back wall, 13.20 m
    3: 4,    # northwest face, 32.70 m
    6: 8,    # Spear Street (southwest), 68.56 m — the long elevation
    9: 4,    # Folsom Street (southeast), 33.48 m
    11: 2,   # Folsom entrance recess back wall, 13.59 m
    13: 4,   # Folsom Street (southeast), 32.68 m
    14: 3,   # Embarcadero (northeast), 24.72 m
    16: 1,   # Embarcadero north step, 5.99 m
    18: 2,   # EMBARCADERO CENTRAL PAVILION, 15.15 m
    20: 1,   # Embarcadero south step, 6.40 m
    22: 3,   # Embarcadero (northeast), 24.87 m
    23: 4,   # northwest face, 33.37 m — the second long NW plane
}
EDGE_EMB_PAVILION = 18   # the harbour entrance
EDGE_FOLSOM_RECESS = 11  # the mid-block entrance

# ------------------------------------------------------------------- heights
# Three MEASURED planes; everything between them is derived from the 4.6 m
# floor-to-floor those three planes imply.
Z_GROUND_TOP = 6.40      # limestone ground storey (now the 2022 retail floor)
FLOOR_H = 4.60
BASE_FLOORS = 5          # ground + 5 = the six-storey base
Z_BASE_CORNICE0 = 29.60
Z_BASE_CORNICE1 = 30.60
Z_TERRACE = 31.40        # the 7th-floor plaza deck
Z_BASE_PARAPET = 32.30   # MEASURED — DataSF hgt_median 32.28

SUP_FLOORS = 8
Z_SUP_CORNICE0 = 70.40
Z_SUP_CORNICE1 = 71.20
Z_SUP_DECK = 71.40
Z_SUP_PARAPET = 72.10    # MEASURED — DataSF hgt_majority 72.11

Z_TOWER_1 = 78.00        # first tower setback   (estimated)
Z_TOWER_2 = 84.00        # second tower setback  (estimated)
Z_CROWN_PARAPET = 86.60
Z_CREST = 88.00          # MEASURED — DataSF hgt_max 87.95; OSM height=91

# ------------------------------------------------------------------- massing
# Solved so the plan areas reproduce the LiDAR area split: the brick deck at
# 72.11 m wants ~1,467 m2 (34 x 44 = 1,496) and everything above it ~402 m2
# (20 x 20 = 400).
SUP_U0, SUP_U1 = -38.0, -4.0      # brick superstructure, 34 m along u
SUP_V0, SUP_V1 = -22.0, 22.0      # 44 m along v
TOWER_CU, TOWER_CV = -4.0, 2.0    # limestone tower centre
TOWER_W = 20.0
TOWER_W1 = 17.0                   # above the first setback
TOWER_W2 = 13.0                   # crown pavilion

# roof composition on the base terrace (all clear of the superstructure)
SKYLIGHT = (22.0, 6.0, 26.0, 22.0)    # cu, cv, w, d — the seven-storey atrium
LAWN_A = (22.0, -22.0, 15.0, 12.0)
LAWN_B = (20.0, 27.0, 14.0, 11.0)

SKIN = 0.10
PIER_W = 1.15
PIER_PROJ = 0.18
BAND_H = 0.28            # spandrel band height at each floor line
BAND_PROJ = 0.12
BASE_CORNICE_PROJ = 1.10
SUP_CORNICE_PROJ = 0.90
PARAPET_T = 0.50
WIN_H = 2.55
WIN_SILL = 1.05

PALETTE_HEX = {
    # the two lower masses: RAMSA's red brick over a limestone ground storey
    "Toy_brick": "c96f4a",
    # the tower, every pier, frame, cornice and parapet: tawny French limestone
    "Toy_stone": "d9d2c2",
    # copings and the two tower setback ledges — a half-tone lighter than stone
    # so the three mass transitions read from directly overhead
    "Toy_trim": "f3efe6",
    # both roof membranes. Pale from the start — see the docstring.
    "Toy_sand": "ece4d4",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_mint": "8fd0a8",
    "Toy_steel": "9aa0a6",
    "Toy_roofd": "45454a",
    "Toy_ink": "3a3530",
    "Toy_glassl_Glow": "6f95b8",
    "Toy_glass_Glow": "6f95b8",
    "Toy_gold_Glow": "caa64a",
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


def poly_edge(i):
    return edge_frame(FOOTPRINT, i)


def edge_wall(i):
    a, _length, t, n = poly_edge(i)
    return (a, t, n)


def offset_polygon(poly, d):
    """Miter offset; positive d moves outward. The line-intersection form is
    correct at the reflex vertices of the two entrance recesses too, as long as
    d stays well under the 3 m recess depth — it does (max 1.10 m)."""
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


def bay_centres(edge, count):
    _a, length, _t, _n = poly_edge(edge)
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


def bevel(obj, width=0.12, segments=2):
    """Width is capped at a third of the object's thinnest dimension: the
    applied panels are 60-200 mm thick and a full-width bevel on those relies
    entirely on clamp_overlap, which collapses opposing profiles into slivers."""
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
    """Closed extrusion of a CCW polygon (walls + both n-gon caps)."""
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
    from offset d0 to d1 along that wall's normal."""
    a, t, n = frame
    verts = []
    for d in (d0, d1):
        for du, z in profile:
            verts.append(
                (
                    a[0] + t[0] * (u_centre + du) + n[0] * d,
                    a[1] + t[1] * (u_centre + du) + n[1] * d,
                    z,
                )
            )
    npts = len(profile)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def face_panel(name, edge, u_centre, profile, d0, d1, mat):
    return wall_panel(name, edge_wall(edge), u_centre, profile, d0, d1, mat)


def uv_box(name, cu, cv, z0, z1, su, sv, mat):
    """Box aligned to the building's own (u, v) grid."""
    corners = [
        P(cu - su / 2, cv - sv / 2),
        P(cu + su / 2, cv - sv / 2),
        P(cu + su / 2, cv + sv / 2),
        P(cu - su / 2, cv + sv / 2),
    ]
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


def uv_rect(cu, cv, su, sv):
    """CCW-in-Blender rectangle on the building grid, for prism()/ring_band()."""
    return [
        P(cu - su / 2, cv - sv / 2),
        P(cu - su / 2, cv + sv / 2),
        P(cu + su / 2, cv + sv / 2),
        P(cu + su / 2, cv - sv / 2),
    ]


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


def articulate(edge, n_bays, z_start, floors, floor_h, pier_mat, glass_mat,
               glow_mat, band_mat, tag, lit_seed):
    """Piers + continuous spandrel bands + glass fills on one wall plane.

    This is the cheap form and the faithful one: RAMSA's facades are "large,
    simple, structural frames", so the frame is continuous and only the glass
    is per-bay. 235 individually framed openings would have cost about three
    times the triangles for a worse read."""
    _a, length, _t, _n = poly_edge(edge)
    frame = edge_wall(edge)
    pitch = length / n_bays
    z_end = z_start + floors * floor_h
    for i in range(n_bays + 1):
        wall_panel(
            f"{tag}pier{edge}_{i}",
            frame,
            min(max(i * pitch, PIER_W / 2.0), length - PIER_W / 2.0),
            rect_profile(PIER_W, z_start, z_end),
            0.0,
            PIER_PROJ,
            pier_mat,
        )
    # First aerial review: at (pitch - PIER_W - 0.30) the openings were 5.8 m
    # wide in a 7.5 m bay and the building rendered as limestone with red
    # slivers. The brick field is half the identity, so the window takes
    # barely half the bay and the brick keeps the rest.
    open_w = pitch * 0.46
    for k in range(floors):
        z0 = z_start + k * floor_h
        face_panel(
            f"{tag}band{edge}_{k}",
            edge,
            length / 2.0,
            rect_profile(length, z0, z0 + BAND_H),
            0.0,
            BAND_PROJ,
            band_mat,
        )
        for i, u in enumerate(bay_centres(edge, n_bays)):
            w0 = z0 + WIN_SILL
            wall_panel(
                f"{tag}win{edge}_{i}_{k}",
                frame,
                u,
                rect_profile(open_w, w0, w0 + WIN_H),
                0.0,
                SKIN,
                glass_mat,
            )
            if glow_mat is not None and (i * 7 + k * 3 + edge + lit_seed) % 11 < 2:
                g = 0.30
                wall_panel(
                    f"{tag}lit{edge}_{i}_{k}",
                    frame,
                    u,
                    rect_profile(open_w - 2 * g, w0 + g, w0 + WIN_H - g),
                    SKIN + 0.01,
                    SKIN + 0.08,
                    glow_mat,
                )


def uv_articulate(tag, cu, cv, su, sv, z_start, floors, floor_h,
                  pier_mat, glass_mat, glow_mat, band_mat, body_poly):
    """Same treatment on the four faces of a (u, v)-aligned box."""
    for e in range(4):
        a = body_poly[e]
        b = body_poly[(e + 1) % 4]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy)
        t = (dx / length, dy / length)
        n = (t[1], -t[0])
        frame = (a, t, n)
        n_bays = max(3, int(round(length / 7.5)))
        pitch = length / n_bays
        z_end = z_start + floors * floor_h
        for i in range(n_bays + 1):
            wall_panel(
                f"{tag}pier{e}_{i}",
                frame,
                min(max(i * pitch, PIER_W / 2.0), length - PIER_W / 2.0),
                rect_profile(PIER_W, z_start, z_end),
                0.0,
                PIER_PROJ,
                pier_mat,
            )
        open_w = pitch * 0.46
        for k in range(floors):
            z0 = z_start + k * floor_h
            wall_panel(
                f"{tag}band{e}_{k}",
                frame,
                length / 2.0,
                rect_profile(length, z0, z0 + BAND_H),
                0.0,
                BAND_PROJ,
                band_mat,
            )
            for i in range(n_bays):
                u = (i + 0.5) * pitch
                w0 = z0 + WIN_SILL
                wall_panel(
                    f"{tag}win{e}_{i}_{k}",
                    frame,
                    u,
                    rect_profile(open_w, w0, w0 + WIN_H),
                    0.0,
                    SKIN,
                    glass_mat,
                )
                if glow_mat is not None and (i * 5 + k * 3 + e) % 9 < 2:
                    g = 0.30
                    wall_panel(
                        f"{tag}lit{e}_{i}_{k}",
                        frame,
                        u,
                        rect_profile(open_w - 2 * g, w0 + g, w0 + WIN_H - g),
                        SKIN + 0.01,
                        SKIN + 0.08,
                        glow_mat,
                    )


def portico(tag, edge, u_centre, width, top, stone, ink, gold_glow):
    """RAMSA's "porticoes of columns and lintels": a recessed dark opening,
    four stone columns standing proud of it, a projecting lintel, and the
    2022 retail sign band on the lintel fascia (the ground-floor glow)."""
    frame = edge_wall(edge)
    wall_panel(f"{tag}_recess", frame, u_centre, rect_profile(width, 0.0, top), 0.0,
               SKIN + 0.02, ink)
    n_col = 4
    span = width - 1.6
    for i in range(n_col):
        du = -span / 2.0 + span * i / (n_col - 1)
        wall_panel(f"{tag}_col{i}", frame, u_centre + du, rect_profile(1.05, 0.0, top - 0.9),
                   0.0, SKIN + 1.15, stone)
    wall_panel(f"{tag}_lintel", frame, u_centre, rect_profile(width + 1.2, top - 0.9, top + 0.5),
               0.0, SKIN + 1.45, stone)
    wall_panel(f"{tag}_sign_glow", frame, u_centre,
               rect_profile(width - 0.6, top - 0.70, top + 0.25),
               SKIN + 1.43, SKIN + 1.52, gold_glow)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    brick = material("Toy_brick")
    stone = material("Toy_stone")
    trim = material("Toy_trim")
    sand = material("Toy_sand")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    mint = material("Toy_mint")
    steel = material("Toy_steel")
    roofd = material("Toy_roofd")
    ink = material("Toy_ink")
    skylight_glow = material("Toy_glassl_Glow")
    glass_glow = material("Toy_glass_Glow")
    gold_glow = material("Toy_gold_Glow")

    # ================================================================= 1. base
    # The whole-block six-storey base. The cap sits below the terrace deck,
    # which is laid on top as slabs, so the roof composition reads as objects
    # on a plane rather than as decals on the body cap.
    prism("base_body", FOOTPRINT, 0.0, Z_TERRACE - 0.30, brick, mat_caps=sand)

    # limestone ground storey (the 2022 retail floor) — a proud band, not a
    # separate prism, so the brick body stays one closed solid
    ring_band("base_course", FOOTPRINT, 0.0, Z_GROUND_TOP, -0.02, 0.16, stone)

    for edge, n_bays in BAYS.items():
        articulate(edge, n_bays, Z_GROUND_TOP, BASE_FLOORS, FLOOR_H,
                   stone, glass, glass_glow, stone, "b", lit_seed=0)

    # the two entrances, both into the seven-storey atrium
    portico("emb_entry", EDGE_EMB_PAVILION, 7.6, 11.4, 9.6, stone, ink, gold_glow)
    portico("fol_entry", EDGE_FOLSOM_RECESS, 6.8, 11.0, 9.6, stone, ink, gold_glow)

    # base cornice, parapet and coping — the first of the three transitions
    ring_band("base_cornice", FOOTPRINT, Z_BASE_CORNICE0, Z_BASE_CORNICE1,
              -0.02, BASE_CORNICE_PROJ, stone)
    ring_band("base_parapet", FOOTPRINT, Z_BASE_CORNICE1, Z_BASE_PARAPET - 0.18,
              -PARAPET_T, 0.10, stone)
    ring_band("base_coping", FOOTPRINT, Z_BASE_PARAPET - 0.18, Z_BASE_PARAPET,
              -PARAPET_T - 0.06, 0.16, trim)

    # ============================================================== 2. terrace
    # 6,341 m2 of designed surface at 32.3 m, and the reason this asset cannot
    # be judged from the street.
    prism("terrace_deck", offset_polygon(FOOTPRINT, -PARAPET_T),
          Z_TERRACE - 0.30, Z_TERRACE, sand)

    # the seven-storey atrium's skylight: the strongest positive on the roof
    # plane, and the night hero
    sku, skv, skw, skd = SKYLIGHT
    uv_box("skylight_kerb", sku, skv, Z_TERRACE, Z_TERRACE + 0.45,
           skw + 1.0, skd + 1.0, stone)
    uv_box("skylight_glass", sku, skv, Z_TERRACE + 0.35, Z_TERRACE + 1.35, skw, skd, glassl)
    # a coarse 6 x 5 rib grid: the real glazing is ~11 x 8 cells and is
    # sub-pixel at city scale
    for i in range(1, 6):
        uv_box(f"skylight_ribu{i}", sku - skw / 2 + skw * i / 6.0, skv,
               Z_TERRACE + 1.30, Z_TERRACE + 1.50, 0.35, skd, stone)
    for j in range(1, 5):
        uv_box(f"skylight_ribv{j}", sku, skv - skd / 2 + skd * j / 5.0,
               Z_TERRACE + 1.30, Z_TERRACE + 1.50, skw, 0.35, stone)
    uv_box("skylight_glow", sku, skv, Z_TERRACE + 1.36, Z_TERRACE + 1.44,
           skw - 0.8, skd - 0.8, skylight_glow)

    # the two Olin lawn parterres, each with a water strip
    for tag, (lu, lv, lw, ld) in (("lawn_a", LAWN_A), ("lawn_b", LAWN_B)):
        uv_box(f"{tag}_kerb", lu, lv, Z_TERRACE, Z_TERRACE + 0.30, lw + 0.8, ld + 0.8, stone)
        uv_box(f"{tag}", lu, lv, Z_TERRACE + 0.20, Z_TERRACE + 0.45, lw, ld, mint)
        uv_box(f"{tag}_water", lu, lv, Z_TERRACE + 0.40, Z_TERRACE + 0.50,
               lw * 0.55, ld * 0.30, glassl)

    # hedge parterres in ranks, on the Folsom and northwest terraces
    for r in range(6):
        uv_box(f"hedge_se{r}", -32.0 + r * 5.2, 30.0, Z_TERRACE, Z_TERRACE + 0.95,
               1.10, 13.0, mint)
        uv_box(f"hedge_nw{r}", -32.0 + r * 5.2, -30.0, Z_TERRACE, Z_TERRACE + 0.95,
               1.10, 13.0, mint)
    # a single rank in the narrow Spear-side band
    for r in range(4):
        uv_box(f"hedge_sw{r}", -40.0, -16.5 + r * 11.0, Z_TERRACE, Z_TERRACE + 0.95,
               2.60, 8.0, mint)

    # ======================================================= 3. superstructure
    # The red-brick "cubical background mass", set 16 m back from the block
    # centre toward Spear Street so it does not shadow the waterfront park.
    sup_cu = (SUP_U0 + SUP_U1) / 2.0
    sup_cv = (SUP_V0 + SUP_V1) / 2.0
    sup_w = SUP_U1 - SUP_U0
    sup_d = SUP_V1 - SUP_V0
    sup_poly = uv_rect(sup_cu, sup_cv, sup_w, sup_d)
    prism("sup_body", sup_poly, Z_TERRACE - 0.30, Z_SUP_DECK - 0.20, brick, mat_caps=sand)
    uv_articulate("s", sup_cu, sup_cv, sup_w, sup_d, Z_BASE_PARAPET + 0.60,
                  SUP_FLOORS, FLOOR_H, stone, glass, glass_glow, stone, sup_poly)
    ring_band("sup_cornice", sup_poly, Z_SUP_CORNICE0, Z_SUP_CORNICE1,
              -0.02, SUP_CORNICE_PROJ, stone)
    ring_band("sup_parapet", sup_poly, Z_SUP_CORNICE1, Z_SUP_PARAPET - 0.16,
              -0.45, 0.08, stone)
    ring_band("sup_coping", sup_poly, Z_SUP_PARAPET - 0.16, Z_SUP_PARAPET,
              -0.51, 0.14, trim)
    prism("sup_deck", offset_polygon(sup_poly, -0.45), Z_SUP_DECK - 0.20, Z_SUP_DECK, sand)

    # ============================================================== 4. tower
    # The "slender foreground tower": limestone, at the superstructure's
    # NORTHEAST corner, standing 2 m proud of it toward the harbour. It is the
    # only mass that goes above 72.11 m, and its plan area (400 m2) is what the
    # LiDAR decomposition says sits up there (402 m2).
    tow_poly = uv_rect(TOWER_CU, TOWER_CV, TOWER_W, TOWER_W)
    prism("tower_body", tow_poly, Z_TERRACE - 0.30, Z_TOWER_1 - 0.60, stone, mat_caps=sand)
    uv_articulate("t", TOWER_CU, TOWER_CV, TOWER_W, TOWER_W, Z_BASE_PARAPET + 0.60,
                  9, FLOOR_H, stone, glass, glass_glow, trim, tow_poly)
    ring_band("tower_ledge1", tow_poly, Z_TOWER_1 - 0.60, Z_TOWER_1, -0.10, 0.55, trim)

    tow1 = uv_rect(TOWER_CU, TOWER_CV, TOWER_W1, TOWER_W1)
    prism("tower_step1", tow1, Z_TOWER_1 - 0.60, Z_TOWER_2 - 0.60, stone, mat_caps=sand)
    for e in range(4):
        a, b = tow1[e], tow1[(e + 1) % 4]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy)
        t = (dx / length, dy / length)
        frame = (a, t, (t[1], -t[0]))
        for k in range(2):
            z0 = Z_TOWER_1 + 0.6 + k * FLOOR_H
            wall_panel(f"tw1band{e}_{k}", frame, length / 2.0,
                       rect_profile(length, z0, z0 + BAND_H), 0.0, BAND_PROJ, trim)
            for i in range(3):
                u = (i + 0.5) * length / 3.0
                wall_panel(f"tw1win{e}_{i}_{k}", frame, u,
                           rect_profile(length / 3.0 - 1.7, z0 + WIN_SILL,
                                        z0 + WIN_SILL + WIN_H), 0.0, SKIN, glass)
    ring_band("tower_ledge2", tow1, Z_TOWER_2 - 0.60, Z_TOWER_2, -0.10, 0.55, trim)

    # crown pavilion: the portico motif carried to the top, and the one place
    # the tower is allowed to glow at night
    tow2 = uv_rect(TOWER_CU, TOWER_CV, TOWER_W2, TOWER_W2)
    prism("crown_body", tow2, Z_TOWER_2 - 0.60, Z_CROWN_PARAPET - 0.50, stone, mat_caps=sand)
    for e in range(4):
        a, b = tow2[e], tow2[(e + 1) % 4]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy)
        t = (dx / length, dy / length)
        frame = (a, t, (t[1], -t[0]))
        wall_panel(f"crownwin{e}", frame, length / 2.0,
                   rect_profile(length - 3.2, Z_TOWER_2 + 0.9, Z_CROWN_PARAPET - 1.4),
                   0.0, SKIN, glassl)
        wall_panel(f"crownglow{e}", frame, length / 2.0,
                   rect_profile(length - 3.9, Z_TOWER_2 + 1.2, Z_CROWN_PARAPET - 1.7),
                   SKIN + 0.01, SKIN + 0.08, skylight_glow)
        wall_panel(f"crownlintel{e}", frame, length / 2.0,
                   rect_profile(length, Z_CROWN_PARAPET - 1.4, Z_CROWN_PARAPET - 0.5),
                   0.0, 0.32, trim)
    ring_band("crown_parapet", tow2, Z_CROWN_PARAPET - 0.50, Z_CROWN_PARAPET,
              -0.40, 0.22, trim)

    # crenellation: eight chunky blocks, tops landing exactly on the crest.
    # This sets the bounding-box top and therefore the loader's scale.
    h = TOWER_W2 / 2.0 - 1.5
    cren = [(-h, -h), (h, -h), (h, h), (-h, h), (0.0, -h), (0.0, h), (-h, 0.0), (h, 0.0)]
    for i, (du, dv) in enumerate(cren):
        uv_box(f"crenel{i}", TOWER_CU + du, TOWER_CV + dv,
               Z_CROWN_PARAPET - 0.35, Z_CREST, 3.00, 3.00, trim)

    # =========================================================== 5. roof plant
    # On the brick deck only, grouped away from the tower so the step-up stays
    # legible from above. Nothing may out-top the crown.
    uv_box("mech_pen", -22.0, -14.0, Z_SUP_DECK, Z_SUP_DECK + 2.20, 12.0, 8.0, steel)
    for i, du in enumerate((-3.0, 3.0)):
        uv_box(f"fan{i}", -22.0 + du, -14.0, Z_SUP_DECK + 2.00, Z_SUP_DECK + 2.80,
               4.20, 4.20, roofd)
    uv_box("stair_ph", -31.0, 10.0, Z_SUP_DECK, Z_SUP_DECK + 3.00, 7.0, 5.0, steel)
    uv_box("vent0", -14.0, -18.0, Z_SUP_DECK, Z_SUP_DECK + 1.10, 2.60, 2.60, roofd)
    uv_box("vent1", -33.0, -6.0, Z_SUP_DECK, Z_SUP_DECK + 1.10, 2.60, 2.60, roofd)
    uv_box("screen", -30.0, 17.0, Z_SUP_DECK, Z_SUP_DECK + 1.60, 10.0, 3.0, steel)

    # Bevel budget: the three masses, the cornices, the parapets and the
    # crenellation carry the miniature read and get the full 0.12/2. The
    # applied piers, bands and roof furniture get a token softening; the glass
    # fills and the glow shells get none.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        n = obj.name
        if "win" in n or "lit" in n or "glow" in n.lower() or "band" in n:
            # Spandrel bands are 0.12 m proud and 0.55 m tall: a bevel on them
            # is sub-pixel at city scale and cost 3,900 triangles of the 24,000
            # cap, which the three mass transitions need more.
            continue
        if n.startswith(("hedge", "vent", "skylight_rib")) or "pier" in n:
            bevel(obj, width=0.05, segments=1)
        elif "cornice" in n or "parapet" in n or "coping" in n or "ledge" in n or n == "base_course":
            # 24-vertex rings: a 2-segment bevel on these alone was 7,900
            # triangles. One segment keeps the lit top edge that makes the
            # cornice read from directly above and costs a third as much.
            bevel(obj, width=0.06, segments=1)
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
    print("[build] anchor lon/lat: -122.390975 37.790787 (footprint OBB centre)")
    print("[build] Embarcadero elevation heading: 45.2 deg true (NE)")
    print("[build] Folsom Street elevation heading: 135.2 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "2-folsom.blend")
    glb = os.path.join(out, "2-folsom.glb")
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
