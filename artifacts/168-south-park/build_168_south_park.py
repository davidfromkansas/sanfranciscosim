"""Deterministic Blender build of the SF-SIM miniature 166-168 South Park.

    blender -b --python build_168_south_park.py -- [--out DIR]

Writes 168-south-park.blend and 168-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = the OSM ring's area centroid (anchor
lon -122.3949862, lat 37.7811327), min Z = 0, parapet crown exactly 10.44 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured OSM footprint (way 124884342) reprojected with the app's tangent
  projection and reduced to its four real corners — the fifth node is collinear.
  6.10 m of South Park frontage running 29.82 m back through the lot, at 45 deg
  off the world axes. OSM rather than the DataSF LiDAR outline because this ring
  shares nodes with BOTH neighbours' rings: it is the only outline that
  describes the party walls, and the LiDAR one is inflated 1.3 m across a 6.1 m
  width;
* the recognition cue is the PROPORTION. 6.10 m wide, 29.82 m deep, 10.44 m
  tall, wedged between a 15.93 m glass-and-metal loft (188 South Park, already a
  landmark asset) and a low site (164). Nothing on the rim is this narrow, and
  everything else here is subordinate to keeping the slot narrow;
* one designed elevation and three plain ones. Both flanks are party walls; the
  rear faces a 9.5 m yard nothing can see. Inventing openings there would be a
  lie the aerial camera can catch;
* the identity feature: the stepped brick parapet. Three panels over three bays,
  the centre one raised to the 10.44 m crest under a shallow gable with a
  projecting brick coping, the flanking two stepping down to 9.78 m and then to
  the 8.60 m parapet return that runs the rest of the way round. One inset
  stone lozenge per panel, as observed. That silhouette is the whole building
  from the street and from a low aerial;
* the second cue is VALUE: the real roof is a bright white membrane, measurably
  the lightest roof on the block in both Esri and Vexcel imagery. Toy_white is
  used nowhere else in the model so the roof stays the lightest plane in it;
* Toy_brick (c96f4a) not the browner Toy_rust, on the same argument recorded in
  artifacts/358-brannan: this front has to advance against a cool grey-and-glass
  wall on one side and a pale low site on the other;
* night state: two of the three second-floor windows lit — an office building
  after hours, not a hotel — supported by a low spill at the shopfront. Flanks,
  rear and roof stay dark; a party wall that glows would misread. Glow surfaces
  are thin shells proud of the opaque surface behind them (the app renders
  _Glow in a separate layer that is ~12% alpha by day — never author a primary
  surface as glow).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way 124884342 projected with the app's tangent projection and recentred on
# the ring's area centroid (3741.035, -1230.609). Blender X = x - cx,
# Y = cz - z (the app's +z is south). CCW in (x=east, y=north).
FOOTPRINT = [
    (8.415, -12.639),    # front, south-west corner
    (12.735, -8.339),    # front, north-east corner
    (-8.415, 12.631),    # rear, north-east corner
    (-12.735, 8.331),    # rear, south-west corner
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_FRONT = 0   # 6.10 m, faces SE 135 deg — South Park
EDGE_NE = 1      # 29.82 m, faces NE 45 deg — party wall to 164 South Park
EDGE_REAR = 2    # 6.10 m, faces NW 315 deg — rear yard, fire escape
EDGE_SW = 3      # 29.82 m, faces SW 225 deg — party wall to 188 South Park

Z_DECK = 7.98             # flat roof deck (DataSF LiDAR hgt_median 7.98, measured)
Z_PAR = 8.60              # parapet return on the flanks and rear (inferred)
Z_STEP = 9.78             # the two flanking front panels (photogrammetric, see REPORT 4)
Z_SHOULDER = 10.18        # where the centre panel's gable starts
Z_CREST = 10.44           # gable crown = the bbox top (LiDAR hgt_max, measured)

Z_SHOP0, Z_SHOP1 = 0.55, 3.35   # shopfront display glazing
Z_DOOR1 = 2.60                  # entrance door heads
Z_LINTEL0, Z_LINTEL1 = 3.90, 4.16  # stone lintel band over the shopfront
Z_WIN0, Z_WIN1 = 4.75, 7.15     # second-floor openings

SKIN = 0.10               # brick front skin, proud of the shell
PARAPET_T = 0.24          # parapet thickness, inward from the footprint edge
PIER_PROJ = 0.09          # pilaster projection beyond the skin

PALETTE_HEX = {
    # Toy_brick, not the browner Toy_rust, and for the reason recorded in
    # artifacts/358-brannan: this front is 6 m wide and has to advance against
    # 188 South Park's cool grey-and-glass wall on the party side. Rust merged
    # with the shadowed flank in the first aerial review of that building and
    # would do the same here.
    "Toy_brick": "c96f4a",
    "Toy_stone": "d9d2c2",
    "Toy_glass": "2a4d73",
    # Used ONLY for the roof slab. The white membrane is a measured observation
    # about this building and the lightest value in the model has to stay on it.
    "Toy_white": "f8f4ec",
    "Toy_steel": "9aa0a6",
    "Toy_ink": "3a3530",
    "Toy_glass_Glow": "6f95b8",
    "Toy_trim_Glow": "f3efe6",
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


def diamond_profile(half_w, half_h, zc):
    """A lozenge in the wall plane, as observed in each parapet panel."""
    return [(0.0, zc - half_h), (half_w, zc), (0.0, zc + half_h), (-half_w, zc)]


def gable_profile(w, z0, z_shoulder, z_crown, crown_w):
    """Parapet panel with a shallow gable and a FLAT crown. The crown must stay
    flat: a knife ridge would be rounded away by the bevel and the bbox top
    would land under Z_CREST, which is exactly the number the loader divides by."""
    a = w / 2.0
    c = crown_w / 2.0
    return [
        (-a, z0),
        (a, z0),
        (a, z_shoulder),
        (c, z_crown),
        (-c, z_crown),
        (-a, z_shoulder),
    ]


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


def bevel(obj, width=0.08, segments=2):
    """Miniature-style edge softening (style bible s.4). Width is capped at a
    third of the object's thinnest dimension: this building is 6 m wide and its
    applied panels are 60-200 mm thick, so an uncapped bevel collapses opposing
    profiles into zero-area slivers."""
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


def edge_wall(edge):
    a, _length, t, n = poly_edge(edge)
    return (a, t, n)


def face_panel(name, edge, u_centre, profile, d0, d1, mat):
    return wall_panel(name, edge_wall(edge), u_centre, profile, d0, d1, mat)


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


def roof_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the roof, aligned to the building's own grid: u runs along the
    South Park edge from its SW end, v runs INTO the lot from that edge."""
    origin, _l, t, n = poly_edge(EDGE_FRONT)
    cx = origin[0] + t[0] * u - n[0] * v
    cy = origin[1] + t[1] * u - n[1] * v
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=math.atan2(t[1], t[0]))


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


def rect_opening(tag, frame, u, w, z0, z1, frame_mat, fill_mat, base_d, glow_mat=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads
    as a border ring around the opening. No booleans, all closed solids."""
    wall_panel(f"{tag}_frame", frame, u, rect_profile(w, z0, z1), 0.0, base_d + 0.06, frame_mat)
    inset = 0.14
    wall_panel(
        f"{tag}_fill",
        frame,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        0.0,
        base_d + 0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.26
        wall_panel(
            f"{tag}_glow",
            frame,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            base_d + 0.10,
            base_d + 0.17,
            glow_mat,
        )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    brick = material("Toy_brick")
    stone = material("Toy_stone")
    glass = material("Toy_glass")
    white = material("Toy_white")
    steel = material("Toy_steel")
    ink = material("Toy_ink")
    glass_glow = material("Toy_glass_Glow")
    trim_glow = material("Toy_trim_Glow")

    _a_f, LF, _t_f, _n_f = poly_edge(EDGE_FRONT)
    _a_r, LR, _t_r, _n_r = poly_edge(EDGE_REAR)
    front = edge_wall(EDGE_FRONT)
    rear = edge_wall(EDGE_REAR)

    # --- shell -------------------------------------------------------------
    # The top cap IS the roof deck, and it is the only Toy_white surface in the
    # model. The bottom cap sits at z=0 under the terrain and is never seen.
    prism("body", FOOTPRINT, 0.0, Z_DECK, brick, mat_caps=white)

    # --- parapet return, all four sides -------------------------------------
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PAR - 0.08, -PARAPET_T, 0.0, brick)
    ring_band("parapet_coping", FOOTPRINT, Z_PAR - 0.08, Z_PAR, -PARAPET_T - 0.05, 0.05, steel)

    # --- South Park front: the brick skin, the only designed elevation ------
    face_panel("front_skin", EDGE_FRONT, LF / 2.0, rect_profile(LF, 0.0, Z_PAR), 0.0, SKIN, brick)

    # three bays between four pilasters, so the parapet's three panels have
    # something under them to stand on
    BAY_U = [LF / 6.0, LF / 2.0, 5.0 * LF / 6.0]
    PIER_W = 0.34
    PIER_U = [PIER_W / 2.0, LF / 3.0, 2.0 * LF / 3.0, LF - PIER_W / 2.0]
    for i, u in enumerate(PIER_U):
        face_panel(
            f"pier{i}",
            EDGE_FRONT,
            u,
            rect_profile(PIER_W, Z_LINTEL1 - 0.10, Z_PAR),
            0.0,
            SKIN + PIER_PROJ,
            brick,
        )

    # ground floor: one wide display window (the tenant's, with its vinyl
    # lettering) and two dark entrance doors, in a brick surround
    rect_opening("shop", front, 1.62, 2.50, Z_SHOP0, Z_SHOP1, ink, glass, SKIN)
    face_panel(
        "shop_bulkhead", EDGE_FRONT, 1.62, rect_profile(2.50, 0.0, Z_SHOP0), 0.0, SKIN + 0.06, ink
    )
    rect_opening("doorA", front, 3.72, 1.04, 0.0, Z_DOOR1, ink, glass, SKIN)
    rect_opening("doorB", front, 5.04, 1.04, 0.0, Z_DOOR1, ink, glass, SKIN)
    # a low spill across the shopfront: the night accent, not the hero
    face_panel(
        "shop_glow",
        EDGE_FRONT,
        1.62,
        rect_profile(2.00, Z_SHOP0 + 0.34, Z_SHOP0 + 0.82),
        SKIN + 0.10,
        SKIN + 0.17,
        trim_glow,
    )
    face_panel(
        "front_lintel",
        EDGE_FRONT,
        LF / 2.0,
        rect_profile(LF, Z_LINTEL0, Z_LINTEL1),
        0.0,
        SKIN + 0.11,
        stone,
    )

    # second floor: one tall recessed opening per bay. Two are lit at night —
    # an office building after hours, not a hotel.
    for i, u in enumerate(BAY_U):
        rect_opening(
            f"win{i}",
            front,
            u,
            1.28,
            Z_WIN0,
            Z_WIN1,
            stone,
            glass,
            SKIN,
            glass_glow if i in (0, 2) else None,
        )

    # --- the stepped parapet: the identity feature --------------------------
    # ONE continuous wall with a stepped top, not three panels: built as three
    # separate tabs the silhouette dipped back to the flank return between the
    # pilasters and the steps read as floating blocks (second aerial review).
    # The real profile is monotone — 8.60 flank return, 9.78 shoulders, 10.44
    # crown — and that monotone climb is the whole recognition cue. The two
    # shoulder heights come from a door-scaled tangent-ratio measurement of the
    # Jan 2025 Street View capture (REPORT 4), not from a guess.
    PAR_D = SKIN + PIER_PROJ
    a_u = PIER_U[1] - LF / 2.0   # left step, relative to the front's centre
    b_u = PIER_U[2] - LF / 2.0   # right step
    crown = 0.62 / 2.0
    stepped = [
        (-LF / 2.0, Z_PAR - 0.10),
        (LF / 2.0, Z_PAR - 0.10),
        (LF / 2.0, Z_STEP),
        (b_u, Z_STEP),
        (b_u, Z_SHOULDER),
        (crown, Z_CREST - 0.12),
        (-crown, Z_CREST - 0.12),
        (a_u, Z_SHOULDER),
        (a_u, Z_STEP),
        (-LF / 2.0, Z_STEP),
    ]
    wall_panel("parapet_front", front, LF / 2.0, stepped, -PARAPET_T, PAR_D, brick)

    # the grey metal coping the photograph shows, on the two shoulders only
    for tag, u0, u1 in (("l", 0.0, PIER_U[1]), ("r", PIER_U[2], LF)):
        wall_panel(
            f"coping_{tag}",
            front,
            (u0 + u1) / 2.0,
            rect_profile(u1 - u0, Z_STEP - 0.09, Z_STEP),
            -PARAPET_T - 0.05,
            PAR_D + 0.07,
            steel,
        )

    # the projecting brick coping over the gable; its crown IS the bbox top
    wall_panel(
        "parapet_crown",
        front,
        LF / 2.0,
        gable_profile(
            (b_u - a_u) + 0.14, Z_SHOULDER - 0.34, Z_SHOULDER, Z_CREST, 0.62 + 0.14
        ),
        -PARAPET_T - 0.06,
        PAR_D + 0.08,
        brick,
    )

    # one inset stone lozenge per panel, as observed
    wall_panel(
        "diamond_c", front, LF / 2.0, diamond_profile(0.34, 0.34, 9.42), PAR_D, PAR_D + 0.07, stone
    )
    for tag, u in (("l", PIER_U[1] / 2.0), ("r", (PIER_U[2] + LF) / 2.0)):
        wall_panel(
            f"diamond_{tag}",
            front,
            u,
            diamond_profile(0.30, 0.30, 9.14),
            PAR_D,
            PAR_D + 0.07,
            stone,
        )

    # --- rear: plain brick, one door, two openings, and the 1995 fire escape --
    rect_opening("rdoor", rear, 1.30, 1.05, 0.0, 2.35, brick, ink, 0.0)
    for i, u in enumerate((3.10, 4.70)):
        rect_opening(f"rwin{i}", rear, u, 0.86, 4.95, 6.55, brick, ink, 0.0)
    wall_panel(
        "fe_landing", rear, LF / 2.0, rect_profile(2.60, 4.62, 4.76), 0.02, 0.92, steel
    )
    wall_panel("fe_rail", rear, LF / 2.0, rect_profile(2.60, 5.58, 5.70), 0.80, 0.90, steel)
    for i, du in enumerate((-1.24, 1.24)):
        wall_panel(
            f"fe_post{i}",
            rear,
            LF / 2.0 + du,
            rect_profile(0.11, 4.76, 5.70),
            0.80,
            0.90,
            steel,
        )
    wall_panel(
        "fe_stair",
        rear,
        LF / 2.0 - 0.55,
        [(-0.62, 2.42), (0.62, 4.62), (0.62, 4.76), (-0.62, 2.56)],
        0.20,
        0.86,
        steel,
    )

    # --- roof: a flat white membrane and three small things on it ------------
    # u runs along the South Park edge from its SW end (0 .. 6.10); v runs back
    # into the lot from that edge (0 .. 29.82). Everything stays inside the
    # 0.30 m parapet return, off-centre and grouped, per 2.9 of the plan.
    # Two skylight runs: a 6 m wide, 30 m deep loft has no other daylight in
    # its middle, and the nadir imagery shows a loose line of small dark items
    # here. They are kept under 0.4 m because the LiDAR standard deviation over
    # this roof is 0.75 m — nothing tall stands on it.
    for i, v in enumerate((7.8, 20.4)):
        roof_box(f"skylight_kerb{i}", 3.05, v, Z_DECK, Z_DECK + 0.18, 2.30, 1.50, stone)
        roof_box(f"skylight{i}", 3.05, v, Z_DECK + 0.14, Z_DECK + 0.36, 2.02, 1.24, glass)
    # a low duct run down the north-east side, and the plant it serves
    roof_box("duct", 4.55, 15.0, Z_DECK, Z_DECK + 0.34, 0.62, 5.60, steel)
    roof_box("vent0", 1.62, 11.6, Z_DECK, Z_DECK + 0.56, 0.55, 0.55, steel)
    roof_box("vent1", 2.55, 12.4, Z_DECK, Z_DECK + 0.42, 0.45, 0.45, steel)
    roof_box("vent2", 1.75, 24.6, Z_DECK, Z_DECK + 0.48, 0.50, 0.50, steel)
    roof_box("roof_hatch", 2.20, 16.6, Z_DECK, Z_DECK + 0.40, 1.10, 0.90, steel)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.08/2 (0.08 not 0.10 — this facade is 6 m wide and a 30 m block's
    # bevel eats it). Applied panels are small and numerous: their frames get a
    # token 1-segment softening and the fills/glow shells none at all.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")) or obj.name.startswith("diamond"):
            continue
        if obj.name.endswith("_frame") or obj.name.startswith(("fe_", "pier")):
            bevel(obj, width=0.035, segments=1)
        else:
            bevel(obj, width=0.08, segments=2)

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
    print("[build] anchor lon/lat: -122.3949862 37.7811327 (OSM ring area centroid)")
    print("[build] South Park front heading: 135 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "168-south-park.blend")
    glb = os.path.join(out, "168-south-park.glb")
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
