"""Deterministic Blender build of the SF-SIM miniature 35 South Park (Accel).

    blender -b --python build_35_south_park.py -- [--out DIR]

Writes 35-south-park.blend and 35-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = the oriented-bounding-box centre of OSM
way 112759864 (anchor lon -122.3933378, lat 37.7815714), min Z = 0, penthouse
crest exactly 13.40 m.

Design (see REFERENCE.md for the sources behind every number, and REPORT.md for
the corrections this build made to the plan):

* the surveyed footprint: a 22.72 x 35.80 m rectangle at bearing 45.5/225.5 deg
  with a 7.96 x 2.44 m notch bitten out of the rear (south-east) south-west
  corner. One public face — the 22.72 m north-west arcade onto South Park — one
  blind party wall with 41-43 South Park on the south-west, a 7.3 m side gap to
  27 South Park on the north-east, and a service rear;
* a 1920 industrial building wearing the grandest street elevation on the oval:
  five giant round-arched bays in smooth pale ashlar, a plain roundel on each
  interior pier, a rope-enriched architrave, a lettered frieze (the raised
  letters have been stripped and are deliberately not modelled), a projecting
  cornice and a tall blank parapet;
* a ground-up renovation completed in 2023 added the two things no neighbour
  has and that the app's downward camera reads first: a continuous clipped
  hedge the full length of the front parapet, and a set-back penthouse on the
  south-west half of the roof;
* night state: the five lit arches are the hero — the building's double-height
  interior with its ring chandeliers is what the park sees after dark — with
  the four pier sconces as the supporting accent. The penthouse, the roof
  lights and the three blind elevations stay dark. Glow surfaces are thin
  shells proud of the opaque glazing (the app renders _Glow in a separate layer
  that is ~12% alpha by day — never author a primary surface as glow).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way 112759864, projected with the app's tangent projection and recentred
# on the minimum-area oriented bounding-box centre (anchor lon -122.3933378,
# lat 37.7815714). Counter-clockwise. The two collinear vertex splits in the
# OSM ring (one on each flank) are dropped; the rear notch is real and kept.
#
#   F0 = west corner   (front x party wall)
#   F1 = south corner  (party wall x the set-back rear)
#   F2, F3 = the notch
#   F4 = east corner   (rear x north-east flank)
#   F5 = north corner  (north-east flank x front)
FOOTPRINT = [
    (-20.653, 4.786),    # F0  west
    (2.701, -18.947),    # F1  south
    (8.421, -13.409),    # F2  notch, outer
    (10.067, -15.078),   # F3  notch, inner  (reflex)
    (20.653, -4.797),    # F4  east
    (-4.338, 20.605),    # F5  north
]

# Edge index -> elevation. Outward normals verified against the survey (plan 2.3).
EDGE_PARTY = 0    # 33.30 m, faces SW 225.5 deg — blind party wall with 41-43
EDGE_REAR_B = 1   # 7.96 m,  faces SE 135.9 deg — rear wall behind the notch
EDGE_NOTCH = 2    # 2.34 m,  faces SW 225.4 deg — the notch return
EDGE_REAR_A = 3   # 14.76 m, faces SE 135.8 deg — main rear wall
EDGE_FLANK = 4    # 35.63 m, faces NE  45.5 deg — onto the 7.3 m gap to 27
EDGE_FRONT = 5    # 22.72 m, faces NW 315.9 deg — THE ARCADE

BAYS = 5
W_OPEN = 2.80        # clear width of an arched opening
ARCHIVOLT = 0.32     # width of the moulded band around it

# Vertical scheme. Photogrammetric from the Jan 2025 Street View captures
# (plan 2.4); the penthouse crest is the estimated number and the one the
# loader divides by, so it is a single named constant (plan 2.15 risk 1).
Z_WATER = 1.00            # water table / plinth top
Z_OPEN_0 = 1.10           # bottom of the arched openings
Z_SPRING = 5.20           # arch springing line -> crown at 6.60
Z_PORTAL = 4.30           # top of the dark portal in the two end bays
Z_SCONCE_0, Z_SCONCE_1 = 4.20, 5.20
Z_ROUND_C = 7.10          # roundel centre on the interior piers
R_ROUND_OUT, R_ROUND_IN = 0.62, 0.46
Z_ROPE_0, Z_ROPE_1 = 7.78, 7.98      # rope-enriched architrave (measured 7.9 m)
Z_FRIEZE_1 = 8.85         # top of the (blank) frieze
Z_CORN_1 = 9.30           # top of the projecting cornice
Z_DECK = 10.00            # roof deck
Z_PAR_TOP = 10.28         # parapet upstand
Z_COPING = 10.40          # coping top — the parapet line the park sees
Z_HEDGE = 11.30           # clipped hedge crest
Z_CREST = 13.40           # penthouse cap top = bbox top = targetHeightM

# Roof furniture on the building's own (u, v) grid: +u north-east along the
# frontage, +v south-east into the block. Front wall at v = -17.81,
# rear at v = +17.85, flanks at u = +-11.36.
HEDGE_V, HEDGE_SV = -16.90, 1.10
PENT_U, PENT_V, PENT_SU, PENT_SV = -4.40, -5.60, 11.00, 7.50

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",       # walls, piers, frieze, parapet, water table
    "Toy_trim": "f3efe6",        # archivolts, architrave, cornice, coping, roundel rings
    "Toy_glass": "2a4d73",       # the five arched windows
    "Toy_glassl": "6f95b8",      # roof lights
    "Toy_roofd": "45454a",       # roof deck, penthouse, the two end portals
    "Toy_verdigris": "9fb8a8",   # the roof hedge
    "Toy_ink": "3a3530",         # reveals, mullions, planter kerb, sconces
    "Toy_steel": "9aa0a6",       # the light roof membrane
    "Toy_glass_Glow": "6f95b8",  # the lit arcade — hero night state
    "Toy_gold_Glow": "caa64a",   # the four pier sconces
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
    """Miter offset of the CCW footprint; positive d moves outward. The one
    reflex vertex (the inner notch corner) is mild enough for a plain miter at
    the +-0.2 m offsets used here."""
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


def arch_profile(w, z0, z_spring, segments=10):
    """A round-arched opening as a convex (du, z) profile: two jambs and a
    semicircular head of radius w/2 centred on the springing line."""
    r = w / 2.0
    pts = [(-r, z0), (r, z0), (r, z_spring)]
    for k in range(1, segments):
        a = math.pi * k / segments
        pts.append((r * math.cos(a), z_spring + r * math.sin(a)))
    pts.append((-r, z_spring))
    return pts


def arch_path(r, z0, z_spring, segments=10):
    """Centreline of an archivolt: up the left jamb, round the head, down the
    right jamb. Open path, used by sweep_band."""
    pts = [(-r, z0)]
    for k in range(segments + 1):
        a = math.pi - math.pi * k / segments
        pts.append((r * math.cos(a), z_spring + r * math.sin(a)))
    pts.append((r, z0))
    return pts


def disc_profile(radius, cz, segments=14):
    return [
        (radius * math.cos(2 * math.pi * i / segments),
         cz + radius * math.sin(2 * math.pi * i / segments))
        for i in range(segments)
    ]


# ------------------------------------------------- building-local (u, v) frame
# u runs along the arcade, positive north-east (toward Second Street); v runs
# from the arcade into the block, positive south-east. Both measured from the
# oriented bounding-box centre, which is the anchor and the origin.

_T_FRONT = poly_edge(EDGE_FRONT)[2]
_N_FRONT = poly_edge(EDGE_FRONT)[3]
_U_AXIS = (-_T_FRONT[0], -_T_FRONT[1])   # +u north-east
_V_AXIS = (-_N_FRONT[0], -_N_FRONT[1])   # +v south-east, into the block


def uv(u, v):
    """Building-local (u north-east, v south-east) -> world (x, y)."""
    return (_U_AXIS[0] * u + _V_AXIS[0] * v, _U_AXIS[1] * u + _V_AXIS[1] * v)


def bay_layout():
    """(pier centres, bay centres, pitch) along EDGE_FRONT, measured from that
    edge's origin — which is the NORTH corner, so u increases south-west.
    Bay 0 is therefore the north-east end and bay 4 the south-west end."""
    length = poly_edge(EDGE_FRONT)[1]
    pitch = length / BAYS
    bays = [(k + 0.5) * pitch for k in range(BAYS)]
    piers = [k * pitch for k in range(1, BAYS)]
    return piers, bays, pitch


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


def sweep_band(name, edge, u_centre, path, half_w, d0, d1, mat):
    """Sweep a rectangular section along an OPEN (u, z) centreline lying in the
    plane of wall `edge`. All quads — this is how the archivolts are built,
    because a U-shaped ngon cap triangulates badly on export."""
    a, _length, t, n = poly_edge(edge)
    stations = []
    for i, (du, z) in enumerate(path):
        if i == 0:
            tx, tz = path[1][0] - du, path[1][1] - z
        elif i == len(path) - 1:
            tx, tz = du - path[-2][0], z - path[-2][1]
        else:
            tx, tz = path[i + 1][0] - path[i - 1][0], path[i + 1][1] - path[i - 1][1]
        m = math.hypot(tx, tz) or 1.0
        nx, nz = tz / m, -tx / m
        stations.append(
            ((du - nx * half_w, z - nz * half_w), (du + nx * half_w, z + nz * half_w))
        )

    def world(du, z, d):
        return (
            a[0] + t[0] * (u_centre + du) + n[0] * d,
            a[1] + t[1] * (u_centre + du) + n[1] * d,
            z,
        )

    verts, faces = [], []
    for inner, outer in stations:
        verts.append(world(inner[0], inner[1], d0))
        verts.append(world(outer[0], outer[1], d0))
        verts.append(world(outer[0], outer[1], d1))
        verts.append(world(inner[0], inner[1], d1))
    ns = len(stations)
    for i in range(ns - 1):
        a0, b0 = i * 4, (i + 1) * 4
        for k in range(4):
            k2 = (k + 1) % 4
            faces.append((a0 + k, a0 + k2, b0 + k2, b0 + k))
    faces.append((0, 1, 2, 3))
    last = (ns - 1) * 4
    faces.append((last + 3, last + 2, last + 1, last))
    return new_mesh(name, verts, faces, [mat])


def uv_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the building's own grid rather than the world axes."""
    corners = []
    for lu, lv in ((-su / 2, -sv / 2), (su / 2, -sv / 2), (su / 2, sv / 2), (-su / 2, sv / 2)):
        corners.append(uv(u + lu, v + lv))
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


def uv_cyl(name, u, v, z0, z1, radius, mat, segments=10):
    poly = []
    for i in range(segments):
        a = 2 * math.pi * i / segments
        poly.append(uv(u + radius * math.cos(a), v + radius * math.sin(a)))
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


def arched_bay(tag, u, lit, portal):
    """One of the five giant bays: a moulded archivolt standing proud of the
    ashlar, a dark reveal, glazing set inside it, a coarse mullion grid, and —
    where the bay is lit — a thin glow shell proud of the glazing."""
    trim = material("Toy_trim")
    ink = material("Toy_ink")
    glass = material("Toy_glass")
    roofd = material("Toy_roofd")
    glow = material("Toy_glass_Glow")

    r_mid = W_OPEN / 2 + ARCHIVOLT / 2
    sweep_band(
        f"archivolt_{tag}",
        EDGE_FRONT,
        u,
        arch_path(r_mid, Z_OPEN_0 - 0.10, Z_SPRING),
        ARCHIVOLT / 2,
        0.0,
        0.15,
        trim,
    )
    face_panel(
        f"reveal_{tag}",
        EDGE_FRONT,
        u,
        arch_profile(W_OPEN, Z_OPEN_0, Z_SPRING),
        0.0,
        0.06,
        ink,
    )
    face_panel(
        f"glass_{tag}",
        EDGE_FRONT,
        u,
        arch_profile(W_OPEN - 0.28, Z_OPEN_0 + 0.14, Z_SPRING),
        0.06,
        0.12,
        glass,
    )

    # Coarse mullion grid: three verticals and three transoms, plus a three-ray
    # fan in the head. The real sash is far finer and aliases to mush at the
    # app's camera (plan 2.6).
    half = (W_OPEN - 0.28) / 2
    for k in (-1, 0, 1):
        # Stop each vertical on the arch curve, not on the crown height, or the
        # outer two poke through the archivolt as dark ticks.
        du = k * half / 2
        z_top = Z_SPRING + math.sqrt(max(0.0, half * half - du * du)) - 0.06
        face_panel(
            f"mull_{tag}_v{k}",
            EDGE_FRONT,
            u + du,
            rect_profile(0.09, Z_OPEN_0 + 0.14, z_top),
            0.16,
            0.20,
            ink,
        )
    span = Z_SPRING - (Z_OPEN_0 + 0.14)
    for k in (1, 2, 3):
        z = Z_OPEN_0 + 0.14 + span * k / 4.0
        face_panel(
            f"mull_{tag}_h{k}",
            EDGE_FRONT,
            u,
            rect_profile(W_OPEN - 0.28, z - 0.045, z + 0.045),
            0.16,
            0.20,
            ink,
        )

    if portal:
        # The two end bays: a dark full-height opening under the arched glazing —
        # the service opening at the north-east end, the entrance at the
        # south-west end.
        face_panel(
            f"portal_{tag}",
            EDGE_FRONT,
            u,
            rect_profile(W_OPEN - 0.10, Z_OPEN_0, Z_PORTAL),
            0.06,
            0.22,
            roofd,
        )

    if lit:
        z0 = (Z_PORTAL + 0.30) if portal else (Z_OPEN_0 + 0.45)
        face_panel(
            f"glow_{tag}",
            EDGE_FRONT,
            u,
            arch_profile(W_OPEN - 0.90, z0, Z_SPRING),
            0.12,
            0.18,
            glow,
        )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    stone = material("Toy_stone")
    trim = material("Toy_trim")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    verd = material("Toy_verdigris")
    ink = material("Toy_ink")
    steel = material("Toy_steel")
    gold_glow = material("Toy_gold_Glow")

    # --- body: one ashlar volume to the roof deck ---------------------------
    prism("body", FOOTPRINT, 0.0, Z_DECK, stone)

    # --- water table --------------------------------------------------------
    ring_band("water_table", FOOTPRINT, 0.0, Z_WATER, -0.02, 0.12, stone)

    # --- the entablature, carried right round -------------------------------
    # Full rings rather than a front-only return: they cost almost nothing, and
    # they are what makes the blind party wall and the rear read as part of the
    # same building from the app's downward camera (the device 2 South Park
    # uses one block away).
    ring_band("architrave", FOOTPRINT, Z_ROPE_0, Z_ROPE_1, -0.02, 0.14, trim)
    ring_band("frieze", FOOTPRINT, Z_ROPE_1, Z_FRIEZE_1, -0.02, 0.04, stone)
    ring_band("cornice", FOOTPRINT, Z_FRIEZE_1, Z_CORN_1, -0.02, 0.28, trim)

    # --- parapet and coping -------------------------------------------------
    ring_band("parapet", FOOTPRINT, Z_CORN_1, Z_PAR_TOP, -0.02, 0.10, stone)
    ring_band("coping", FOOTPRINT, Z_PAR_TOP, Z_COPING, -0.05, 0.16, trim)

    # --- the arcade ---------------------------------------------------------
    # Bay 0 is the north-east end (the service opening), bay 4 the south-west
    # end (the entrance). Bays 1-3 are fully glazed and are the three that read
    # as lit at night; the end bays glow only above their portals.
    piers, bays, _pitch = bay_layout()
    for k, u in enumerate(bays):
        arched_bay(f"b{k}", u, lit=True, portal=k in (0, 4))

    # --- roundels and sconces on the four interior piers --------------------
    for k, u in enumerate(piers):
        face_panel(
            f"roundel_ring_{k}", EDGE_FRONT, u,
            disc_profile(R_ROUND_OUT, Z_ROUND_C), 0.0, 0.10, trim,
        )
        face_panel(
            f"roundel_disc_{k}", EDGE_FRONT, u,
            disc_profile(R_ROUND_IN, Z_ROUND_C), 0.10, 0.17, stone,
        )
        face_panel(
            f"sconce_{k}", EDGE_FRONT, u,
            rect_profile(0.30, Z_SCONCE_0, Z_SCONCE_1), 0.10, 0.40, ink,
        )
        face_panel(
            f"sconce_glow_{k}", EDGE_FRONT, u,
            rect_profile(0.20, Z_SCONCE_0 + 0.12, Z_SCONCE_1 - 0.12), 0.41, 0.47,
            gold_glow,
        )

    # --- roof ---------------------------------------------------------------
    # The membrane is a light grey, not the usual dark deck: this roof was
    # re-covered in the 2020-23 works and reads conspicuously brighter than every
    # neighbouring roof in the aerial (REFERENCE.md). Its top sits 0.06 m proud
    # of the body so the two never share a plane.
    prism("roof_slab", offset_polygon(FOOTPRINT, -0.18), Z_DECK - 0.20, Z_DECK + 0.06, steel)

    # The hedge: one clipped volume, not individual plants (style bible s.12),
    # running the whole 22.72 m front just inside the parapet, with a short
    # return down each flank. This is the roof's identity.
    uv_box("hedge_kerb", 0.0, HEDGE_V, Z_DECK, Z_DECK + 0.36, 21.6, HEDGE_SV + 0.18, ink)
    uv_box("hedge", 0.0, HEDGE_V, Z_DECK + 0.36, Z_HEDGE, 21.4, HEDGE_SV, verd)
    for side in (-1, 1):
        uv_box(
            f"hedge_return_{'sw' if side < 0 else 'ne'}",
            side * 10.30, HEDGE_V + 2.60, Z_DECK + 0.36, Z_HEDGE - 0.10,
            HEDGE_SV, 4.20, verd,
        )

    # Penthouse: the crest, set back 8 m from the front parapet and sitting on
    # the south-west half of the roof (plan 2.4, from the nadir aerial).
    uv_box("penthouse", PENT_U, PENT_V, Z_DECK, Z_CREST - 0.22, PENT_SU, PENT_SV, roofd)
    uv_box(
        "penthouse_upstand", PENT_U, PENT_V, Z_DECK, Z_DECK + 0.18,
        PENT_SU + 0.30, PENT_SV + 0.30, trim,
    )
    uv_box(
        "penthouse_cap", PENT_U, PENT_V, Z_CREST - 0.22, Z_CREST,
        PENT_SU + 0.28, PENT_SV + 0.28, roofd,
    )
    # the band of four roof lights on its north-west face
    for k in range(4):
        uv_box(
            f"pent_light_{k}",
            PENT_U - 3.75 + k * 2.5, PENT_V - PENT_SV / 2,
            Z_DECK + 1.60, Z_DECK + 2.80, 1.50, 0.18, glassl,
        )

    # Roof lights loose on the north-east half of the deck.
    for k, (u, v) in enumerate(((4.2, -2.0), (7.6, -2.0), (4.2, 3.2), (7.6, 3.2))):
        uv_box(f"roof_light_{k}", u, v, Z_DECK, Z_DECK + 0.42, 1.60, 1.20, glassl)

    # Mechanical group and hatch, grouped at the rear where the camera reads
    # the roof last (plan 2.9).
    uv_box("mech_a", 2.4, 11.8, Z_DECK, Z_DECK + 0.90, 1.80, 1.40, roofd)
    uv_box("mech_b", 5.6, 12.6, Z_DECK, Z_DECK + 0.70, 1.20, 1.00, roofd)
    uv_box("roof_hatch", -6.4, 8.0, Z_DECK, Z_DECK + 0.60, 1.20, 1.00, roofd)
    uv_cyl("vent", 8.8, 8.2, Z_DECK, Z_DECK + 0.65, 0.42, roofd)

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.12/2. The 60-odd arcade panels are small and numerous — frames get a
    # token 1-segment softening and the fills, mullions and glow shells none.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if name.startswith(("glass_", "glow_", "mull_", "sconce_glow_", "pent_light_")):
            continue
        if name.startswith(("architrave", "cornice", "coping", "frieze")):
            bevel(obj, width=0.03, segments=1)
        elif name.startswith(("archivolt_", "reveal_", "roundel_", "sconce_", "portal_")):
            bevel(obj, width=0.04, segments=1)
        elif name in ("parapet", "water_table", "roof_slab"):
            bevel(obj, width=0.06, segments=1)
        elif name.startswith(("mech_", "roof_light_", "roof_hatch", "vent", "hedge")):
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
    print("[build] anchor lon/lat: -122.3933378 37.7815714 (OSM way 112759864 OBB centre)")
    print("[build] arcade front heading: 315.9 deg true (NW); party wall 225.5 deg (SW)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "35-south-park.blend")
    glb = os.path.join(out, "35-south-park.glb")
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
