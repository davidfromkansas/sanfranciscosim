"""Deterministic Blender build of the SF-SIM miniature 21-29 South Park.

    blender -b --python build_21_south_park.py -- [--out DIR]

Writes 21-south-park.blend and 21-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = the footprint's WORLD-AXIS-ALIGNED bbox
centre (anchor lon -122.3931063, lat 37.7817676), min Z = 0, roof bulkhead crest
exactly 11.73 m.

Design (see REFERENCE.md for the sources behind every number, and REPORT.md for
the corrections this build made to the plan):

* the measured DataSF footprint SF3775042, 1115 m2, whose STREET WALL BENDS:
  19.69 m facing NW 315.7 deg, then a reflex corner, then 12.07 m facing WNW
  286.7 deg, because the lot fronts the curve of the South Park oval where the
  oval closes at its Second Street end. Nothing else in the manifest has a bent
  street front and it is the whole recognition of this building;
* a 1919 two-storey unreinforced brick warehouse, painted bright off-white, in
  office use since the 1990s (Redpoint Ventures took the ground floor in 2016);
* the front is two registers: wide three-part loft bays below (glass, ribbed
  cast-iron spandrel, four-pane transom) with a teal freight door in the
  re-entrant corner and a timber office entrance beside it; a continuous rank of
  segmental-arched windows above that turns the bend without interruption;
* party walls on the other three sides, so they are blank: only the NW front is
  exposed;
* the roof deck sits at 9.50 m with a corbelled cornice crest at 10.20 m; the
  stair/lift bulkhead at 11.73 m (LiDAR maximum) is the bbox top. The park-facing
  third of the roof is deliberately EMPTY and the equipment is massed behind it;
* night state: the ground-floor loft bays are the hero glow, with a sparse
  scatter of lit second-floor windows. Glow surfaces are thin shells proud of the
  opaque glazing (the app renders _Glow in a separate layer at low alpha by day —
  never author a primary surface as glow, and keep the shells small because a
  closed shell presents two alpha layers, not one).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF LiDAR building footprint SF3775042, projected with the app's tangent
# projection (lon0 -122.4375, lat0 37.77) and recentred on the world-AABB centre.
# Listed clockwise in (+X east, +Y north), so it is reversed once below to give a
# CCW ring (outward normal = (t.y, -t.x)).
FOOTPRINT_CW = [
    (-23.281, -1.470),   # W corner  — south end of the main front plane
    (-9.193, 12.281),    # the BEND (reflex) — main front meets angled front
    (-5.717, 23.844),    # N corner — angled front meets the jog
    (-6.192, 24.330),    # jog
    (-5.919, 25.546),    # jog — start of the NE party wall
    (18.693, 1.913),     # E corner (party wall dog-legs)
    (23.286, -2.796),    # E corner — start of the rear party wall
    (-0.261, -25.556),   # S corner — start of the SW party wall
]
FOOTPRINT = list(reversed(FOOTPRINT_CW))

# Indices into FOOTPRINT (the REVERSED list). Verified by outward normal in
# report(): 136.0 / 45.7 / 43.8 / 282.6 / 225.7 / 286.7 / 315.7 / 226.3 deg.
EDGE_REAR = 0        # 32.75 m, faces SE 136.0 — party wall, Brannan Street row
EDGE_NE_SHORT = 1    # 6.58 m, faces NE 45.7 — party wall
EDGE_NE = 2          # 34.12 m, faces NE 43.8 — party wall, 17-19 South Park
EDGE_JOG_A = 3       # 1.25 m, faces WNW 282.6
EDGE_JOG_B = 4       # 0.68 m, faces SW 225.7
EDGE_FRONT_ANG = 5   # 12.07 m, faces WNW 286.7 — angled front; u=0 at the N corner
EDGE_FRONT = 6       # 19.69 m, faces NW 315.7 — main front; u=0 at the BEND
EDGE_SW = 7          # 33.32 m, faces SW 226.3 — party wall, 35 South Park

Z_DECK = 9.50         # roof deck — DataSF LiDAR, median 9.60 / mean 9.52, sigma 0.45
Z_CORNICE_MID = 9.86
Z_CREST_CORNICE = 10.20   # corbelled cornice crest (estimated, plan 2.15)
Z_PARAPET = 9.90          # braced UMB parapet on the three party sides
Z_COPING = 10.00
Z_BULKHEAD = 11.73        # stair/lift bulkhead — LiDAR maximum, THE BBOX TOP

Z_FLOOR2 = 4.65           # ground floor is a 4.65 m loft storey

# Ground-floor loft bay: glass / ribbed spandrel / four-pane transom.
BAY_W = 3.55
BAY_Z0, BAY_Z1 = 0.75, 4.20
GLASS_Z0, GLASS_Z1 = 0.91, 2.95
SPAN_Z0, SPAN_Z1 = 3.03, 3.35
TRAN_Z0, TRAN_Z1 = 3.43, 4.04

# Segmental-arched second-floor window.
ARCH_W = 2.10
ARCH_SILL = 5.45
ARCH_SPRING = 8.05
ARCH_RISE = 0.50
ARCH_SEGS = 7         # enough to read as a shallow curve at diorama scale

# Bay centres, in each front edge's own u (see the edge table above).
BAYS_MAIN = (3.17, 7.62, 12.07, 16.52)          # 4 loft bays, 4.45 m centres
ARCH_MAIN = (2.745, 6.295, 9.845, 13.395, 16.945)   # 5 arches, 3.55 m centres
ARCH_ANG = (2.735, 6.035, 9.335)                # 3 arches, 3.30 m centres
U_ENTRANCE = 1.55     # timber office entrance, far (N) end of the angled plane
U_ANG_BAY = 5.10      # the angled plane's one loft bay
U_FREIGHT = 9.60      # freight doors, in the re-entrant corner

PALETTE_HEX = {
    "Toy_white": "f7f4ec",     # the painted brick body, parapet
    "Toy_stone": "d9d2c2",     # cornice, coping, beltcourse, roof deck, sills, ribs
    "Toy_sash": "2f4f49",      # THE near-black teal industrial joinery (off-palette,
                               # deliberate — see REPORT.md)
    "Toy_glass": "2a4d73",     # glazing
    "Toy_rust": "a86444",      # the timber office entrance — the one saturated accent
    "Toy_steel": "9aa0a6",     # roof membrane deck, downpipe, conduit
    "Toy_roofd": "45454a",     # roof bulkhead, condensers, duct, vents
    "Toy_mustard_Glow": "d9a441",  # the lit loft bays — hero glow
    "Toy_glassl_Glow": "6f95b8",   # a scatter of lit second-floor windows
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
    """Edge i of the footprint: (origin, length, tangent unit, outward normal)."""
    poly = FOOTPRINT if poly is None else poly
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def signed_area(poly):
    s = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return s / 2.0


def point_in_poly(pt, poly):
    x, y = pt
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xin = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xin:
                inside = not inside
    return inside


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


def seg_arch_profile(w, z_sill, z_spring, rise, segs=ARCH_SEGS):
    """(u, z) profile of a SEGMENTAL-arched opening: a rectangle to the springing
    line, then a shallow circular segment of the given rise over it. Unlike a
    semicircular arch the crown lands at z_spring + rise, not z_spring + w/2 —
    this building's brick arches are shallow and that is what has to read."""
    half = w / 2.0
    radius = rise / 2.0 + (w * w) / (8.0 * rise)
    cz = z_spring + rise - radius
    theta = math.asin(min(1.0, half / radius))
    pts = [(-half, z_sill), (half, z_sill), (half, z_spring)]
    for i in range(1, segs):
        a = theta - 2.0 * theta * i / segs
        pts.append((radius * math.sin(a), cz + radius * math.cos(a)))
    pts.append((-half, z_spring))
    return pts


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
    """Miniature-style edge softening on the chunky solids (style bible s.4).
    Width is capped at a third of the object's thinnest dimension so the thin
    applied panels do not collapse into slivers."""
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


def prism(name, poly, z0, z1, mat):
    """Closed extrusion of a CCW polygon (walls + both caps)."""
    npts = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def offset_polygon(poly, d):
    """Miter offset of a CCW polygon; positive d moves outward. The reflex corner
    at the bend is handled by the same intersection formula."""
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


def edge_box(name, edge, u_centre, su, z0, z1, d0, d1, mat):
    """Axis box on a wall's own (u, normal) frame — cornice, beltcourse, returns."""
    return face_panel(name, edge, u_centre, rect_profile(su, z0, z1), d0, d1, mat)


def uv_box(name, edge, u_centre, v_centre, su, sv, z0, z1, mat):
    """Box on the building's own grid: u along `edge`, v outward from it (so roof
    furniture uses negative v, measured inward from the front wall)."""
    a, _length, t, n = poly_edge(edge)
    corners = []
    for du, dv in ((-su / 2, -sv / 2), (su / 2, -sv / 2), (su / 2, sv / 2), (-su / 2, sv / 2)):
        u = u_centre + du
        v = v_centre + dv
        corners.append((a[0] + t[0] * u + n[0] * v, a[1] + t[1] * u + n[1] * v))
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


def uv_to_xy(edge, u, v):
    a, _length, t, n = poly_edge(edge)
    return (a[0] + t[0] * u + n[0] * v, a[1] + t[1] * u + n[1] * v)


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


def loft_bay(tag, edge, u, sash, stone, glass, glow_mat=None, w=BAY_W):
    """The ground-floor warehouse bay, in its three real registers: a big
    multi-pane window, a cast-iron spandrel panel above it, and a four-pane
    transom above that. The spandrel's ribs are drawn in the PALE stone rather
    than in the sash colour — the real relief is same-colour and would vanish at
    diorama scale, and the imagery reads as light bars on dark (plan 2.6)."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, BAY_Z0, BAY_Z1), 0.0, 0.09, sash)
    inner = w - 0.36
    face_panel(f"{tag}_glass", edge, u,
               rect_profile(inner, GLASS_Z0, GLASS_Z1), 0.0, 0.15, glass)
    face_panel(f"{tag}_spandrel", edge, u,
               rect_profile(inner, SPAN_Z0, SPAN_Z1), 0.0, 0.15, sash)
    face_panel(f"{tag}_rib", edge, u,
               rect_profile(inner - 0.44, SPAN_Z0 + 0.10, SPAN_Z0 + 0.22), 0.13, 0.20, stone)
    face_panel(f"{tag}_transom", edge, u,
               rect_profile(inner, TRAN_Z0, TRAN_Z1), 0.0, 0.15, glass)
    for k, du in ((0, -inner / 4.0), (1, 0.0), (2, inner / 4.0)):
        face_panel(f"{tag}_mull{k}", edge, u + du,
                   rect_profile(0.10, TRAN_Z0, TRAN_Z1), 0.0, 0.18, sash)
    if glow_mat is not None:
        # A WIDE warm band rather than a small panel: it reads as a lit interior
        # from 400 m, and keeping it short in Z keeps the daytime alpha tint (a
        # closed shell is two blended layers, not one) off most of the glazing.
        face_panel(f"{tag}_glow", edge, u,
                   rect_profile(inner - 0.56, GLASS_Z0 + 0.72, GLASS_Z1 - 0.68),
                   0.13, 0.20, glow_mat)


def arch_window(tag, edge, u, sash, stone, glass, glow_mat=None):
    """The signature second-floor opening: a shallow segmental brick arch with no
    architrave — the arch itself is the surround — over a recessed teal reveal
    and a pale projecting sill."""
    inset = 0.18
    face_panel(f"{tag}_reveal", edge, u,
               seg_arch_profile(ARCH_W, ARCH_SILL, ARCH_SPRING, ARCH_RISE),
               0.0, 0.09, sash)
    face_panel(f"{tag}_fill", edge, u,
               seg_arch_profile(ARCH_W - 2 * inset, ARCH_SILL + inset, ARCH_SPRING,
                                ARCH_RISE * 0.80),
               0.0, 0.15, glass)
    face_panel(f"{tag}_sill", edge, u,
               rect_profile(ARCH_W + 0.28, ARCH_SILL - 0.18, ARCH_SILL), 0.0, 0.19, stone)
    if glow_mat is not None:
        g = 0.44
        face_panel(f"{tag}_glow", edge, u,
                   seg_arch_profile(ARCH_W - 2 * g, ARCH_SILL + g, ARCH_SPRING,
                                    ARCH_RISE * 0.66),
                   0.13, 0.20, glow_mat)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    white = material("Toy_white")
    stone = material("Toy_stone")
    sash = material("Toy_sash")
    glass = material("Toy_glass")
    rust = material("Toy_rust")
    steel = material("Toy_steel")
    roofd = material("Toy_roofd")
    bay_glow = material("Toy_mustard_Glow")
    win_glow = material("Toy_glassl_Glow")

    len_main = poly_edge(EDGE_FRONT)[1]     # 19.69 m
    len_ang = poly_edge(EDGE_FRONT_ANG)[1]  # 12.07 m

    # --- body: one volume on the measured footprint, up to the roof deck ------
    prism("body", FOOTPRINT, 0.0, Z_DECK, white)

    # --- roof deck ------------------------------------------------------------
    prism("roof_deck", offset_polygon(FOOTPRINT, -0.34), Z_DECK - 0.02, Z_DECK + 0.05,
          steel)

    # --- beltcourse at the second-floor line, front planes only ---------------
    for tag, edge, ln in (("main", EDGE_FRONT, len_main), ("ang", EDGE_FRONT_ANG, len_ang)):
        edge_box(f"belt_{tag}", edge, ln / 2.0, ln + 0.30, Z_FLOOR2 - 0.13, Z_FLOOR2 + 0.11,
                 -0.02, 0.14, stone)

    # --- main front plane (NW, 315.7 deg): four loft bays, five arches --------
    LIT_MAIN_BAYS = {0, 1, 3}
    for i, u in enumerate(BAYS_MAIN):
        loft_bay(f"bayM{i}", EDGE_FRONT, u, sash, stone, glass,
                 bay_glow if i in LIT_MAIN_BAYS else None)
    LIT_MAIN_ARCH = {1, 4}
    for i, u in enumerate(ARCH_MAIN):
        arch_window(f"arcM{i}", EDGE_FRONT, u, sash, stone, glass,
                    win_glow if i in LIT_MAIN_ARCH else None)

    # --- angled front plane (WNW, 286.7 deg) ----------------------------------
    # From the far (north) end toward the bend: office entrance, one loft bay,
    # then the freight doors sitting in the re-entrant corner itself.
    loft_bay("bayA0", EDGE_FRONT_ANG, U_ANG_BAY, sash, stone, glass, bay_glow)

    # Freight doors: a flush pair with the same spandrel and transom carried over
    # them, so the bay rhythm survives across the loading opening.
    face_panel("freight_frame", EDGE_FRONT_ANG, U_FREIGHT,
               rect_profile(2.45, 0.0, BAY_Z1), 0.0, 0.09, sash)
    face_panel("freight_leaf_l", EDGE_FRONT_ANG, U_FREIGHT - 0.585,
               rect_profile(1.05, 0.06, 3.35), 0.0, 0.15, sash)
    face_panel("freight_leaf_r", EDGE_FRONT_ANG, U_FREIGHT + 0.585,
               rect_profile(1.05, 0.06, 3.35), 0.0, 0.15, sash)
    face_panel("freight_transom", EDGE_FRONT_ANG, U_FREIGHT,
               rect_profile(2.13, 3.48, 4.04), 0.0, 0.15, glass)
    face_panel("freight_mull", EDGE_FRONT_ANG, U_FREIGHT,
               rect_profile(0.10, 3.48, 4.04), 0.0, 0.18, sash)

    # Office entrance: the one saturated element on 33.7 m of white wall, drawn
    # deliberately wider and deeper than reality (plan 2.6).
    face_panel("entry_frame", EDGE_FRONT_ANG, U_ENTRANCE,
               rect_profile(2.10, 0.0, 3.75), 0.0, 0.10, stone)
    face_panel("entry_door", EDGE_FRONT_ANG, U_ENTRANCE,
               rect_profile(1.70, 0.0, 2.95), 0.0, 0.17, rust)
    face_panel("entry_transom", EDGE_FRONT_ANG, U_ENTRANCE,
               rect_profile(1.70, 3.06, 3.55), 0.0, 0.15, glass)
    face_panel("entry_glow", EDGE_FRONT_ANG, U_ENTRANCE,
               rect_profile(1.24, 3.14, 3.47), 0.12, 0.19, bay_glow)

    LIT_ANG_ARCH = {0}
    for i, u in enumerate(ARCH_ANG):
        arch_window(f"arcA{i}", EDGE_FRONT_ANG, u, sash, stone, glass,
                    win_glow if i in LIT_ANG_ARCH else None)

    # --- party walls: blank ---------------------------------------------------
    # NE (17-19 South Park), SE (the Brannan row) and SW (35 South Park) are all
    # shared planes. No openings, by observation, not by omission.

    # --- corbelled cornice: the two front planes, plus short returns -----------
    # Two steps; the upper step's flat top lands exactly on Z_CREST_CORNICE. The
    # two runs cross inside the mass at the re-entrant bend, which is correct for
    # a union of solids.
    for tag, edge, ln in (("main", EDGE_FRONT, len_main), ("ang", EDGE_FRONT_ANG, len_ang)):
        edge_box(f"cornice_lo_{tag}", edge, ln / 2.0, ln + 0.70,
                 Z_DECK, Z_CORNICE_MID, -0.24, 0.30, stone)
        edge_box(f"cornice_hi_{tag}", edge, ln / 2.0, ln + 1.16,
                 Z_CORNICE_MID, Z_CREST_CORNICE, -0.24, 0.52, stone)
    for tag, edge, u0 in (("ne", EDGE_NE, poly_edge(EDGE_NE)[1] - 0.55),
                          ("sw", EDGE_SW, 0.55)):
        edge_box(f"cornice_ret_{tag}_lo", edge, u0, 1.10, Z_DECK, Z_CORNICE_MID,
                 -0.24, 0.30, stone)
        edge_box(f"cornice_ret_{tag}_hi", edge, u0, 1.10, Z_CORNICE_MID, Z_CREST_CORNICE,
                 -0.24, 0.52, stone)

    # --- braced UMB parapet on every side, with a darker coping ---------------
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET, -0.32, 0.02, white)
    ring_band("parapet_coping", FOOTPRINT, Z_PARAPET, Z_COPING, -0.36, 0.05, stone)

    # --- roof: an empty park-side apron, then the equipment field -------------
    # Placed on the main front's own (u, v) frame, v measured INWARD (negative).
    # The apron runs to v = -13; nothing is allowed in front of that line.
    # The box stops BELOW the cap. An earlier build ran both to Z_BULKHEAD, which
    # left two coplanar top faces and z-fought into a mottled patch on the roof at
    # the app's own aerial camera — caught in the stage-5 local QA, not in the rig.
    uv_box("bulkhead", EDGE_FRONT, -6.80, -15.40, 5.60, 4.00,
           Z_DECK, Z_BULKHEAD - 0.14, roofd)
    uv_box("bulkhead_cap", EDGE_FRONT, -6.80, -15.40, 5.92, 4.32,
           Z_BULKHEAD - 0.22, Z_BULKHEAD, stone)

    for c, (uc, vc) in enumerate(((-9.50, -21.50), (-3.50, -18.00), (2.50, -16.50),
                                 (8.00, -21.00), (13.50, -17.50), (13.00, -27.50),
                                 (-8.00, -28.50))):
        for i in range(4):
            uv_box(f"cond{c}_{i}", EDGE_FRONT, uc + (i % 2) * 2.30, vc - (i // 2) * 1.70,
                   2.05, 1.45, Z_DECK + 0.03, Z_DECK + 0.98, roofd)
    uv_box("duct", EDGE_FRONT, 6.10, -23.00, 0.70, 13.00,
           Z_DECK + 0.03, Z_DECK + 0.63, roofd)
    uv_box("vent_a", EDGE_FRONT, 5.00, -14.00, 0.80, 0.80, Z_DECK, Z_DECK + 0.90, roofd)
    uv_box("vent_b", EDGE_FRONT, 17.20, -15.00, 0.80, 0.80, Z_DECK, Z_DECK + 0.80, roofd)
    uv_box("vent_c", EDGE_FRONT, -1.50, -25.50, 0.85, 0.85, Z_DECK, Z_DECK + 0.95, roofd)

    # --- services on the front wall ------------------------------------------
    face_panel("downpipe", EDGE_FRONT, 19.20, rect_profile(0.16, 0.20, Z_DECK),
               0.0, 0.16, steel)
    face_panel("conduit", EDGE_FRONT_ANG, 11.55, rect_profile(0.12, 3.20, Z_DECK - 0.6),
               0.0, 0.12, steel)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. The applied panels are small and numerous — their frames and
    # reveals get a token 1-segment softening and the fills, glass, ribs, sills,
    # mullions and glow shells none at all, which is what keeps this under 9,000.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if name.endswith(("_glass", "_fill", "_glow", "_sill", "_transom")) or (
            "_rib" in name or "_mull" in name
        ):
            continue
        if name.endswith(("_frame", "_reveal", "_spandrel")) or name.startswith(
            ("freight_leaf", "entry_")
        ):
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
    print(f"[build] footprint signed area={signed_area(FOOTPRINT):.1f} m2 (CCW if > 0)")
    for tag, e in (("rear", EDGE_REAR), ("NE-short", EDGE_NE_SHORT), ("NE", EDGE_NE),
                   ("jogA", EDGE_JOG_A), ("jogB", EDGE_JOG_B),
                   ("front-angled", EDGE_FRONT_ANG), ("front-main", EDGE_FRONT),
                   ("SW", EDGE_SW)):
        _a, ln, _t, n = poly_edge(e)
        print(f"[build] edge {tag}: len={ln:.2f} outward normal="
              f"{math.degrees(math.atan2(n[0], n[1])) % 360:.1f} deg")
    # Roof furniture must sit inside the footprint: report any that does not.
    stray = []
    for o in objs:
        if not (o.name.startswith(("bulkhead", "duct", "vent", "plant")) or o.name.startswith("cond") and "uit" not in o.name):
            continue
        c = sum((o.matrix_world @ v.co for v in o.data.vertices), Vector()) / len(
            o.data.vertices
        )
        if not point_in_poly((c.x, c.y), offset_polygon(FOOTPRINT, -0.9)):
            stray.append(o.name)
    print(f"[build] roof furniture outside footprint: {stray or 'none'}")
    print("[build] anchor lon/lat: -122.3931063 37.7817676 (footprint world-AABB centre)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "21-south-park.blend")
    glb = os.path.join(out, "21-south-park.glb")
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
