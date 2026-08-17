"""Deterministic Blender build of the SF-SIM miniature 54-58 South Park.

    blender -b --python build_58_south_park.py -- [--out DIR]

Writes 58-south-park.blend and 58-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = parcel-centroid anchor
(lon -122.3938881, lat 37.7821223), min Z = 0, roof-office crest exactly 16.9 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured ASSESSOR PARCEL polygon for lots 3775/219, /220 and /221 — the
  three condominium lots that share one building — a 9.73 x 30.10 m
  parallelogram at 45.2 deg off the world axes, with only 9.7 m of frontage on
  the South Park oval and 30 m of depth behind it. Both flanks are literal
  party walls: the neighbouring parcels share these edges vertex-for-vertex, so
  the front and the rear are the only elevations that exist;
* four storeys (SF permit 200501052622, "to erect 4 story, 2 family dwelling
  w/retail commercial", 2005) to a 13.6 m parapet, not the "1907 three-story"
  building every commercial listing for this address still describes — that is
  CoStar data for the two-storey office demolished on this lot in 2005;
* the identity feature: the TWO-TONE STACK. Three storeys of pale plaster
  carrying a dark charcoal metal-panel top storey, the cap built 0.15 m proud of
  the plaster so the split throws its own shadow line instead of relying on
  colour alone. It is the one thing that reads from the app's aerial camera at
  thumbnail size;
* the second cue: the tall dark-steel glazed bay at the WEST end of the front —
  58's own commercial entrance, running unbroken through all three plaster
  storeys. It is the only vertical element on an otherwise horizontally banded
  facade, and it is the hero night glow;
* the three-address ground floor, west to east: 58's glazed shopfront, 56's
  plaster bay with its dark slatted vehicle gate, 54's glass residential entry;
* the rear 4.5 m of the lot drops to a single storey. The 2010 city LiDAR over
  this footprint has a minimum of 3.97 m against a majority of 13.59 m, and 2026
  satellite imagery puts the roof's rear parapet about 3 m in from the rear lot
  line — so the low element is at the BACK, not a mid-depth lightwell;
* a designed roof, because this is a full-floor roof deck and not a membrane:
  pavers, a light coping ring, a guardrail on the park edge, a planter row along
  the south-west parapet, a skylight, a furniture cluster grouped at the park
  end, and the roof office ("private office" in 54's listing copy; SF permit
  2013 gave the "roof storage area" a window) that carries the 16.9 m crest;
* night state: the tall glazed bay lit full height, two middle-storey lights,
  one light in the dark cap's window band and the roof office's window. Glow
  surfaces are thin shells proud of the opaque glazing — the app renders _Glow
  in a separate layer that is a low alpha by day, so a primary surface must
  never be authored as glow.

Everything here is a union of CLOSED SOLIDS. There are no booleans, so an
opening cannot be cut out of a wall: openings are made by standing panels PROUD
of the wall, and recesses by building the surrounding skin proud of them.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# Assessor parcel polygon for block 3775 lots 219/220/221 (DataSF Parcels),
# projected with the app's tangent projection and recentred on the parcel
# centroid, wound CCW. A clean parallelogram: the four edges close to within
# 10 mm and the area is 292.8 m2 against the listing's 3,168 sq ft lot (0.5%).
#
# OSM way 124884349 traces the same building 3% smaller and shifted ~2.3 m
# north-west; the parcel is the survey and wins. Recorded in REPORT.md.
FOOTPRINT = [
    (7.154, -14.101),    # front (SE) corner, west side
    (14.059, -7.248),    # front (SE) corner, east side
    (-7.160, 14.107),    # rear (NW) corner, east side
    (-14.055, 7.244),    # rear (NW) corner, west side
]

# Edge index -> elevation. Outward normals verified against the parcel survey.
EDGE_FRONT = 0   # 9.729 m, faces SE 135.2 deg — SOUTH PARK, the hero elevation
EDGE_NE = 1      # 30.105 m, faces NE 45.2 deg — party wall with 44-46 South Park
EDGE_REAR = 2    # 9.728 m, faces NW 315.1 deg — the block interior, Taber Place
EDGE_SW = 3      # 30.088 m, faces SW 225.2 deg — party wall with 70 South Park

# Depths measured from the front (SE) face, INTO the block.
D_BODY = 25.60       # the four-storey block ends here
D_LOT = 30.10        # rear lot line

# Storey lines. Four storeys to the parapet: the 2005 permit's storey count,
# the 2010 LiDAR majority of 13.59 m and OSM's height=14 all agree on ~13.6 m,
# and the ground floor is the tall one because it is commercial.
Z_L1 = 4.00          # ground-floor ceiling line (58, the office)
Z_L2 = 7.20
Z_L3 = 10.20         # the dark charcoal cap starts here
Z_DECK = 13.20       # roof deck / top of the body
Z_PARAPET = 13.60    # main parapet crest — the architectural height
Z_RAIL = 14.30       # guardrail top on the park edge of the deck
Z_CREST = 16.90      # roof office top = the bbox top, = targetHeightM

Z_REAR = 4.00        # the single-storey rear element
Z_REAR_CAP = 4.32

CAP_PROUD = 0.15     # how far the dark top storey stands out of the plaster
PARAPET_T = 0.30

# Front bay centres, u measured along the front edge from its WEST corner.
# Widths 3.0 / 3.7 / 3.0 sum to the measured 9.73 m frontage; the individual
# splits are read off the January 2025 pano scaled against a 2.13 m door and
# are INFERRED to about +/- 0.4 m (REFERENCE.md).
U_58 = 1.50          # the tall glazed commercial bay
U_56 = 4.85          # plaster bay with the vehicle gate
U_54 = 8.20          # residential entry

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",      # the pale plaster body — a light WARM GRAY
    "Toy_sand": "ece4d4",       # the roof deck paving
    "Toy_roofd": "45454a",      # the dark charcoal cap, parapet and roof office
    "Toy_ink": "3a3530",        # frames, the vehicle gate, the balcony rails
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",     # the roof skylight and the shopfront glazing
    "Toy_steel": "9aa0a6",      # coping and guardrail
    "Toy_verdigris": "9fb8a8",  # the roof planters
    "Toy_trim": "f3efe6",       # the roof furniture cluster — lightest value
    "Toy_glass_Glow": "6f95b8",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def poly_edge(i, poly=None):
    """Edge i of a CCW polygon: (origin, length, tangent unit, outward normal)."""
    poly = FOOTPRINT if poly is None else poly
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def uv_point(u, v):
    """(u along the front from its west corner, v into the block) -> world."""
    a, _l, t, n = poly_edge(EDGE_FRONT)
    return (a[0] + t[0] * u - n[0] * v, a[1] + t[1] * u - n[1] * v)


def band_poly(v0, v1):
    """CCW quad of the footprint between two depths measured from the front."""
    length = poly_edge(EDGE_FRONT)[1]
    return [uv_point(0.0, v0), uv_point(length, v0), uv_point(length, v1), uv_point(0.0, v1)]


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
    """Miniature-style edge softening (style bible s.4). The width is capped at
    a third of the object's thinnest dimension: the applied panels here are
    60-200 mm thick and a flat 0.12 m bevel on those collapses opposing profiles
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
    extruded along that wall's outward normal from offset d0 to d1. Negative
    offsets move the panel INTO the building, which is how the tall glazed bay's
    reveal and the four-storey block's rear wall are reached."""
    a, _length, t, n = poly_edge(edge)
    verts = []
    for d in (d0, d1):
        for du, z in profile:
            verts.append(
                (a[0] + t[0] * (u_centre + du) + n[0] * d,
                 a[1] + t[1] * (u_centre + du) + n[1] * d,
                 z)
            )
    npts = len(profile)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0):
    """Box with local +x along yaw and local +y 90 deg ccw of it."""
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
    """Box on the roof, aligned to the building's own grid rather than to the
    world axes: u runs along the South Park front from its WEST end, v runs
    INTO the block."""
    t = poly_edge(EDGE_FRONT)[2]
    cx, cy = uv_point(u, v)
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


def opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, base=0.0,
            frame_d=0.07, fill_d=0.13, inset=0.11):
    """A punched opening. Everything is a union of closed solids and there are
    no booleans, so an opening cannot be cut into the wall: it is a dark border
    ring standing proud with the glass standing proud again inside it, and the
    eye reads the ring as a reveal."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), base, base + frame_d, frame_mat)
    face_panel(
        f"{tag}_fill", edge, u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        base, base + fill_d, fill_mat,
    )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    plaster = material("Toy_stone")
    deck = material("Toy_sand")
    roofd = material("Toy_roofd")
    ink = material("Toy_ink")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    steel = material("Toy_steel")
    verdigris = material("Toy_verdigris")
    trim = material("Toy_trim")
    gglow = material("Toy_glass_Glow")

    front_len = poly_edge(EDGE_FRONT)[1]
    body = band_poly(0.0, D_BODY)
    rear = band_poly(D_BODY, D_LOT)

    # --- the two-tone stack -------------------------------------------------
    # Three storeys of pale plaster carrying a dark charcoal cap. The split is
    # the building's whole identity, so the cap is also built CAP_PROUD out of
    # the plaster on the front: colour alone flattens out at diorama scale, and
    # a real shadow line under the cap does not.
    prism("body_plaster", body, 0.0, Z_L3, plaster)
    prism("body_cap", body, Z_L3, Z_DECK, roofd, mat_caps=deck)
    face_panel(
        "cap_proud", EDGE_FRONT, front_len / 2.0,
        rect_profile(front_len, Z_L3, Z_DECK), 0.0, CAP_PROUD, roofd,
    )

    # --- the single-storey rear -------------------------------------------
    # The 2010 LiDAR minimum over this footprint is 3.97 m against a majority of
    # 13.59 m, and 2026 satellite imagery puts the roof's rear parapet about 3 m
    # in from the rear lot line. So the low sixth of the lot is at the BACK.
    prism("rear_low", rear, 0.0, Z_REAR, plaster, mat_caps=deck)
    ring_band("rear_low_cap", rear, Z_REAR, Z_REAR_CAP, -0.24, 0.03, steel)

    # --- parapet ring + light coping ---------------------------------------
    # The coping is deliberately the light element: 2026 imagery shows this roof
    # as a pale deck inside a white parapet line, and against the dark cap below
    # it that light ring is what makes the roof read from the app's camera.
    ring_band("parapet", body, Z_DECK, Z_PARAPET - 0.14, -PARAPET_T, CAP_PROUD, roofd)
    ring_band("coping", body, Z_PARAPET - 0.14, Z_PARAPET, -PARAPET_T - 0.05, CAP_PROUD + 0.05, steel)

    # --- South Park front ---------------------------------------------------
    # u = 0 at the WEST corner of the front, which is 58's end.

    # 58: the tall glazed commercial bay, unbroken through all three plaster
    # storeys. The one vertical element on a horizontally banded facade, and the
    # reason this building is not a plain box (style bible s.22).
    face_panel(
        "bay58_frame", EDGE_FRONT, U_58,
        rect_profile(2.72, 0.18, 9.90), 0.0, 0.16, ink,
    )
    face_panel(
        "bay58_glass", EDGE_FRONT, U_58,
        rect_profile(2.30, 0.40, 9.62), 0.0, 0.22, glassl,
    )
    # transoms: three chunky bars, not a mullion grid — the grid is sub-pixel
    for i, z in enumerate((2.55, 5.30, 7.85)):
        face_panel(
            f"bay58_transom{i}", EDGE_FRONT, U_58,
            rect_profile(2.30, z - 0.09, z + 0.09), 0.0, 0.28, ink,
        )
    face_panel(
        "bay58_door", EDGE_FRONT, U_58,
        rect_profile(1.55, 0.18, 2.30), 0.0, 0.30, ink,
    )
    face_panel(
        "bay58_door_glass", EDGE_FRONT, U_58,
        rect_profile(1.30, 0.34, 2.14), 0.0, 0.36, glass,
    )

    # 56: plaster bay with the dark slatted vehicle gate (the one secured
    # parking space in 58's listing) and a narrow pedestrian door beside it.
    face_panel(
        "gate56", EDGE_FRONT, U_56 - 0.30,
        rect_profile(2.70, 0.12, 2.85), 0.0, 0.10, ink,
    )
    for i, z in enumerate((0.95, 1.60, 2.25)):
        face_panel(
            f"gate56_slat{i}", EDGE_FRONT, U_56 - 0.30,
            rect_profile(2.42, z - 0.07, z + 0.07), 0.0, 0.16, roofd,
        )
    opening("door56", EDGE_FRONT, U_56 + 1.62, 1.02, 0.12, 2.40, ink, glass)

    # 54: the residential entry.
    opening("door54", EDGE_FRONT, U_54, 1.42, 0.12, 2.46, ink, glass)

    # Middle storeys: a regular grid of punched openings over 56 and 54, with
    # the black horizontal-bar balcony railings in front of them. The real rails
    # are five or six thin bars; at diorama scale that is aliasing, so each
    # becomes one chunky bar (style bible s.26).
    for si, z0 in ((2, Z_L1 + 0.55), (3, Z_L2 + 0.55)):
        for bi, u in enumerate((U_56, U_54)):
            opening(f"win{si}_{bi}", EDGE_FRONT, u, 2.42, z0, z0 + 2.05, ink, glass)
    face_panel(
        "rail_l2", EDGE_FRONT, (U_56 + U_54) / 2.0 - 0.10,
        rect_profile(6.70, Z_L1 + 0.52, Z_L1 + 1.22), 0.13, 0.29, ink,
    )
    for bi, u in enumerate((U_56, U_54)):
        face_panel(
            f"rail_l3_{bi}", EDGE_FRONT, u,
            rect_profile(2.70, Z_L2 + 0.52, Z_L2 + 1.14), 0.13, 0.27, ink,
        )

    # The dark cap's window band: one horizontal run of tall lights, which is
    # what the May 2009 photograph shows sitting in the middle of the dark box.
    face_panel(
        "cap_band_frame", EDGE_FRONT, 5.55,
        rect_profile(6.80, Z_L3 + 0.62, Z_L3 + 2.42), CAP_PROUD, CAP_PROUD + 0.07, ink,
    )
    face_panel(
        "cap_band_glass", EDGE_FRONT, 5.55,
        rect_profile(6.52, Z_L3 + 0.78, Z_L3 + 2.26), CAP_PROUD, CAP_PROUD + 0.13, glass,
    )
    for i, u in enumerate((3.35, 5.55, 7.75)):
        face_panel(
            f"cap_band_mullion{i}", EDGE_FRONT, u,
            rect_profile(0.15, Z_L3 + 0.62, Z_L3 + 2.42), CAP_PROUD, CAP_PROUD + 0.19, ink,
        )

    # --- the flanks: party walls, deliberately blank ------------------------
    # 44-46 South Park (north-east) and 70 South Park (south-west) share these
    # edges with this parcel vertex-for-vertex. Nothing on them is visible in
    # the real world or in the app, and the style bible's "design every surface"
    # is about the roof, which this asset does spend its budget on.

    # --- rear elevation of the four-storey block ----------------------------
    # It stands at D_LOT - D_BODY back from the rear lot line, so the panels are
    # placed on EDGE_REAR at a negative offset. Entirely INFERRED: no imagery of
    # the block interior was found (REFERENCE.md).
    d_rear = -(D_LOT - D_BODY)
    rear_len = poly_edge(EDGE_REAR)[1]
    for si, z0 in enumerate((1.20, Z_L1 + 0.70, Z_L2 + 0.70, Z_L3 + 0.70)):
        mat_f = ink
        for bi, u in enumerate((rear_len / 2.0 - 2.30, rear_len / 2.0 + 2.30)):
            opening(
                f"rwin{si}_{bi}", EDGE_REAR, u, 2.05, z0, z0 + 1.85, mat_f, glass,
                base=d_rear,
            )
    face_panel(
        "rear_door", EDGE_REAR, rear_len / 2.0,
        rect_profile(1.30, 0.0, 2.30), d_rear, d_rear + 0.09, ink,
    )

    # --- the roof: a full-floor deck, not a membrane ------------------------
    # Layout read off 2026 satellite imagery (Vexcel, z21) plus 54's listing
    # copy: the roof office toward the rear, a skylight mid-depth, a planter row
    # along the south-west parapet, and the furniture grouped at the park end.
    # Grouping is the point — an evenly sprinkled roof reads as noise from the
    # aerial camera (style bible s.10).
    roof_box("roof_office", 4.90, 23.30, Z_DECK, Z_CREST - 0.16, 3.80, 3.50, roofd)
    roof_box("roof_office_coping", 4.90, 23.30, Z_CREST - 0.16, Z_CREST, 4.02, 3.72, steel)
    roof_box("roof_office_win", 4.90, 21.45, Z_DECK + 1.05, Z_DECK + 2.30, 1.90, 0.16, glass)
    roof_box("roof_stair", 7.35, 20.10, Z_DECK, Z_DECK + 1.05, 2.10, 2.30, roofd)

    roof_box("skylight_kerb", 5.40, 17.20, Z_DECK, Z_DECK + 0.22, 3.10, 2.10, steel)
    roof_box("skylight", 5.40, 17.20, Z_DECK + 0.18, Z_DECK + 0.46, 2.70, 1.70, glassl)

    roof_box("hvac_a", 2.35, 20.80, Z_DECK, Z_DECK + 0.85, 1.50, 1.20, steel)
    roof_box("hvac_b", 7.60, 24.10, Z_DECK, Z_DECK + 0.65, 1.30, 1.10, steel)

    for i, v in enumerate((8.6, 12.2, 15.8)):
        roof_box(f"planter{i}", 1.15, v, Z_DECK, Z_DECK + 0.62, 1.30, 2.60, verdigris)

    # The single-storey rear roof is small but the app's camera looks straight
    # down at it, and the style bible does not allow a blank prominent roof.
    roof_box("rear_light_kerb", 3.10, 27.60, Z_REAR, Z_REAR + 0.18, 2.20, 1.60, steel)
    roof_box("rear_light", 3.10, 27.60, Z_REAR + 0.14, Z_REAR + 0.38, 1.85, 1.25, glassl)
    roof_box("rear_condenser", 7.20, 27.20, Z_REAR, Z_REAR + 0.70, 1.30, 1.10, steel)
    roof_box("rear_planter", 7.30, 29.05, Z_REAR, Z_REAR + 0.50, 1.60, 0.90, verdigris)

    roof_box("deck_bench", 5.60, 8.60, Z_DECK, Z_DECK + 0.58, 3.00, 1.05, trim)
    roof_box("deck_table", 5.40, 5.20, Z_DECK, Z_DECK + 0.66, 1.45, 1.45, trim)
    for i, (u, v) in enumerate(((3.15, 5.20), (7.65, 5.20), (7.90, 11.10))):
        roof_box(f"deck_seat{i}", u, v, Z_DECK, Z_DECK + 0.52, 0.85, 0.85, trim)

    # Guardrail on the park edge of the deck only; the parapet does the job on
    # the other three sides.
    face_panel(
        "deck_rail", EDGE_FRONT, front_len / 2.0,
        rect_profile(front_len - 0.30, Z_PARAPET, Z_RAIL), CAP_PROUD - 0.14, CAP_PROUD - 0.04, steel,
    )

    # --- night state --------------------------------------------------------
    # Hero: the tall glazed bay, lit its full height — nine metres of warm light
    # on a 9.7 m facade is this building's whole night identity. Supporting: two
    # middle-storey lights, one light in the cap band, the roof office window.
    face_panel(
        "bay58_glow", EDGE_FRONT, U_58,
        rect_profile(1.94, 0.72, 9.30), 0.22, 0.28, gglow,
    )
    for i, (u, z0) in enumerate(((U_56, Z_L1 + 0.55), (U_54, Z_L2 + 0.55))):
        face_panel(
            f"win_glow{i}", EDGE_FRONT, u,
            rect_profile(2.02, z0 + 0.30, z0 + 1.75), 0.13, 0.19, gglow,
        )
    face_panel(
        "cap_band_glow", EDGE_FRONT, 6.65,
        rect_profile(1.90, Z_L3 + 0.92, Z_L3 + 2.12), CAP_PROUD + 0.13, CAP_PROUD + 0.19, gglow,
    )
    roof_box("office_glow", 4.90, 21.36, Z_DECK + 1.20, Z_DECK + 2.15, 1.60, 0.08, gglow)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. Applied panels are small and numerous — frames get a token
    # 1-segment softening and the fills/glow shells none at all, which is what
    # keeps this under the 10,000-triangle cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow", "_glass")) or "_mullion" in obj.name \
                or "_slat" in obj.name or "_transom" in obj.name:
            continue
        if obj.name.endswith(("_frame", "_win", "_rail", "_door")) or obj.name.startswith("rail_"):
            bevel(obj, width=0.05, segments=1)
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
    print("[build] anchor lon/lat: -122.3938881 37.7821223 (assessor parcel centroid)")
    print("[build] South Park front heading: 135.2 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "58-south-park.blend")
    glb = os.path.join(out, "58-south-park.glb")
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
