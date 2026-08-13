"""Deterministic Blender build of the SF-SIM miniature 181 South Park.

    blender -b --python build_181_south_park.py -- [--out DIR]

Writes 181-south-park.blend and 181-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = footprint OBB centre (anchor
lon -122.3945113, lat 37.7807582), min Z = 0, roof ridge exactly 16.5 m.

Design (see REFERENCE.md for the sources behind every number, and REPORT.md for
the corrections this build made to the plan):

* the measured footprint: a plain 43.21 x 13.84 m rectangle running the full
  depth of the block at bearing 135.2 deg, from the South Park frontage (NW end)
  back to the Varney Place alley (SE end). Three times as deep as it is wide —
  the proportion IS the building;
* four storeys of 2002 live/work loft over a ground-floor commercial base and a
  garage, wood frame, the tallest thing on its side of the oval by ~5 m;
* a straight-pitched gable roof, eave 11.82 m, ridge 16.5 m, hipped down at the
  NW end, with the last 6.5 m at the Varney end a flat mechanical roof. The
  gable — not a barrel — is forced by the LiDAR height distribution; see
  REPORT.md s.2. The top-floor lofts live inside it, which is what the unit
  listings' "arched hardwood high ceilings" describes;
* the exposed SW flank carries the building's window rhythm (10 bays, two
  floors); the NE flank is a party wall against 171 South Park and is authored
  as blind recessed bays, honest to what is really there;
* night state: a restrained scatter of lit windows on the SW flank plus two of
  its roof glazing panels and the storefront at the park end. The alley end and
  the party wall stay dark. Glow surfaces are thin shells proud of the opaque
  glazing (the app renders _Glow in a separate layer that is ~12% alpha by day —
  never author a primary surface as glow).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/124889463 reduced to its four real corners (six of its eight nodes are
# collinear), projected with the app's tangent projection and recentred on the
# OBB centre. CCW, signed area 597.96 m2.
FOOTPRINT = [
    (-10.443, 20.082),
    (-20.255, 10.322),
    (10.438, -20.088),
    (20.250, -10.327),
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_FRONT = 0   # 13.84 m, faces NW 315.2 deg — South Park
EDGE_SW = 1      # 43.21 m, faces SW 224.7 deg — exposed flank (Shell forecourt)
EDGE_REAR = 2    # 13.84 m, faces SE 135.2 deg — Varney Place, garage
EDGE_NE = 3      # 43.21 m, faces NE  44.7 deg — party wall with 171 South Park

Z_EAVE = 11.82       # derived from the LiDAR height distribution (REPORT.md s.2)
Z_RIDGE = 16.5       # LiDAR max 16.54 -> the bbox top
Z_GROUND_TOP = 4.0   # commercial ground floor ceiling / floor band
Z_FASCIA = 11.50     # eave fascia band springs here
Z_FLAT = 12.72       # parapet crest over the Varney-end mechanical roof
Z_W1A, Z_W1B = 4.60, 7.55    # first loft floor window band
Z_W2A, Z_W2B = 8.35, 11.30   # second loft floor window band

HIP_RUN = 6.92       # 45 deg hip at the NW end = half the building width
RIDGE_HALF = 0.15    # half-width of the flat ridge cap; see gable_roof()
FLAT_RUN = 6.50      # flat mechanical roof at the Varney end
OVERHANG = 0.22      # roof overhang past the wall face
SKIN = 0.0           # walls are one plane; openings measure from the wall face

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",   # body walls
    "Toy_trim": "f3efe6",    # floor band, eave fascia, entry surround
    "Toy_steel": "9aa0a6",   # standing-seam metal roof (observed), frames, HVAC
    "Toy_glass": "2a4d73",   # windows and storefront glazing
    "Toy_glassl": "6f95b8",  # roof glazing / monitors — up-facing glass
    "Toy_roofd": "45454a",   # flat mechanical roof, garage door
    "Toy_ink": "3a3530",     # door recesses, reveals
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
# u runs along the long axis from the NW end toward Varney (bearing 135.2 deg),
# v runs across it toward the NE flank. Both measured from the footprint centre.

_A_REAR, _L_LONG, _T_LONG, _N_LONG = poly_edge(EDGE_SW)
U_AXIS = _T_LONG                     # SW edge runs NW -> SE, bearing 135.2 deg
V_AXIS = (-_N_LONG[0], -_N_LONG[1])  # SW outward normal points SW, so -n points NE
HALF_L = _L_LONG / 2.0
HALF_W = poly_edge(EDGE_FRONT)[1] / 2.0
ROOF_W = HALF_W + OVERHANG           # the roof plane springs from the overhang line
SLOPE_SPAN = ROOF_W - RIDGE_HALF     # horizontal run of one slope, ridge cap to eave


def uv(u, v):
    """Building-local (u along the long axis, v across) -> world (x, y)."""
    return (U_AXIS[0] * u + V_AXIS[0] * v, U_AXIS[1] * u + V_AXIS[1] * v)


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

    Width is capped at a third of the object's thinnest dimension: the applied
    window panels here are only 60-200 mm thick, and a flat 0.12 m bevel on those
    collapses opposing profiles into zero-area slivers.
    """
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


def slope_slab(name, u0, u1, v0, v1, side, t0, t1, mat):
    """Thin slab lying in the plane of one gable slope, offset t0..t1 along the
    slope's outward normal. `side` is +1 for the NE slope, -1 for the SW slope.
    v is measured as distance from the ridge toward the eave (0..HALF_W)."""
    rise = Z_RIDGE - Z_EAVE
    # slope normal in the (v, z) section, pointing away from the roof interior
    ln = math.hypot(rise, SLOPE_SPAN)
    nv, nz = (rise / ln) * side, SLOPE_SPAN / ln

    def pt(u, vdist, t):
        z = Z_RIDGE - rise * (vdist / SLOPE_SPAN) + nz * t
        x, y = uv(u, side * (RIDGE_HALF + vdist) + nv * t)
        return (x, y, z)

    quad = ((u0, v0), (u1, v0), (u1, v1), (u0, v1))
    verts = [pt(u, v, t0) for u, v in quad] + [pt(u, v, t1) for u, v in quad]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


def gable_roof(name, u_start, u_end, hip_run, mat):
    """Closed gable solid: two slopes to a ridge, hipped down at the u_start end,
    a plain gable wall at the u_end end, sitting on the eave plane.

    The ridge is a 0.30 m flat cap rather than a knife edge. That is what a real
    standing-seam gable is finished with, and it is also what makes the height
    normalization hold: a bevelled knife-edge apex loses ~36 mm of height, which
    put the first build's bbox top at 16.464 m and would have handed the loader a
    scale of 1.002 instead of 1.0. A flat cap keeps its face at exactly Z_RIDGE
    however hard the edges are rounded.
    """
    w = ROOF_W
    k = RIDGE_HALF
    a = uv(u_start, -w)
    b = uv(u_end, -w)
    c = uv(u_end, w)
    d = uv(u_start, w)
    u_r = u_start + hip_run
    r0m, r0p = uv(u_r, -k), uv(u_r, k)
    r1m, r1p = uv(u_end, -k), uv(u_end, k)
    verts = [
        (a[0], a[1], Z_EAVE),      # 0
        (b[0], b[1], Z_EAVE),      # 1
        (c[0], c[1], Z_EAVE),      # 2
        (d[0], d[1], Z_EAVE),      # 3
        (r0m[0], r0m[1], Z_RIDGE),  # 4
        (r1m[0], r1m[1], Z_RIDGE),  # 5
        (r1p[0], r1p[1], Z_RIDGE),  # 6
        (r0p[0], r0p[1], Z_RIDGE),  # 7
    ]
    faces = [
        (0, 1, 5, 4),      # SW slope
        (2, 3, 7, 6),      # NE slope
        (4, 5, 6, 7),      # ridge cap
        (3, 0, 4, 7),      # NW hip
        (1, 2, 6, 5),      # SE gable end
        (0, 3, 2, 1),      # underside
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


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None):
    """Frame panel + a smaller fill that protrudes further, so the frame reads as
    a border ring around a recessed opening. No booleans, all closed solids."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, 0.07, frame_mat)
    inset = 0.16
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        0.0,
        0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.30
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            0.10,
            0.17,
            glow_mat,
        )


def blind_bay(tag, edge, u, w, z0, z1, mat):
    """A recessed panel with no glazing. The NE flank is a party wall against
    171 South Park: it has no windows in reality, but the app's aerial camera
    sees it plainly, so it gets articulation rather than a blank slab or an
    invented window grid (style bible s.10)."""
    face_panel(f"{tag}_recess", edge, u, rect_profile(w, z0, z1), -0.09, 0.02, mat)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    stone = material("Toy_stone")
    trim = material("Toy_trim")
    steel = material("Toy_steel")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    ink = material("Toy_ink")
    gglow = material("Toy_glass_Glow")
    tglow = material("Toy_trim_Glow")

    len_end = poly_edge(EDGE_FRONT)[1]    # 13.84 m, both ends
    len_flank = poly_edge(EDGE_SW)[1]     # 43.21 m, both flanks

    # --- body: one plain volume up to the eave -----------------------------
    prism("body", FOOTPRINT, 0.0, Z_EAVE, stone)

    # --- floor band separating the commercial base from the lofts -----------
    ring_band("floor_band", FOOTPRINT, Z_GROUND_TOP, Z_GROUND_TOP + 0.18, -0.02, 0.10, trim)

    # --- eave fascia --------------------------------------------------------
    ring_band("eave_fascia", FOOTPRINT, Z_FASCIA, Z_EAVE, -0.02, 0.14, trim)

    # --- South Park (NW) end: the address elevation -------------------------
    # Ground: the 8,631 sq ft commercial condo's storefront, plus the recessed
    # residential entry that serves the five lofts.
    rect_opening("store", EDGE_FRONT, 4.7, 6.0, 0.55, 3.45, ink, glass, gglow)
    rect_opening("entry", EDGE_FRONT, 9.6, 1.5, 0.0, 2.75, trim, ink)
    face_panel(
        "entry_canopy", EDGE_FRONT, 9.6, rect_profile(2.3, 2.80, 3.02), 0.0, 0.80, trim
    )
    face_panel(
        "entry_canopy_glow", EDGE_FRONT, 9.6, rect_profile(1.9, 2.81, 2.87), 0.24, 0.74, tglow
    )
    # Upper: two bays per floor on a face only 13.84 m wide — the proportion
    # that makes this end read as tall and thin rather than as a normal facade.
    for fi, (za, zb) in enumerate(((Z_W1A, Z_W1B), (Z_W2A, Z_W2B))):
        for i, u in enumerate((4.15, 9.69)):
            rect_opening(
                f"nw{fi}_{i}", EDGE_FRONT, u, 3.4, za, zb, steel, glass,
                gglow if (fi, i) == (1, 0) else None,
            )

    # --- Varney Place (SE) end: the service end -----------------------------
    rect_opening("garage", EDGE_REAR, 4.2, 3.6, 0.0, 3.3, ink, roofd)
    rect_opening("backdoor", EDGE_REAR, 7.3, 1.0, 0.0, 2.5, ink, roofd)
    for fi, (za, zb) in enumerate(((Z_W1A, Z_W1B), (Z_W2A, Z_W2B))):
        for i, u in enumerate((4.15, 9.69)):
            rect_opening(f"se{fi}_{i}", EDGE_REAR, u, 2.6, za, zb, steel, glass)

    # --- exposed SW flank: the building's window rhythm ---------------------
    # 10 bays at 4.32 m centres. This is the largest surface the app's aerial
    # camera presents and the only long elevation with a real neighbour gap.
    BAYS = 10
    LIT = {(0, 2), (0, 6), (1, 1), (1, 4), (1, 5), (1, 8)}
    for fi, (za, zb) in enumerate(((Z_W1A, Z_W1B), (Z_W2A, Z_W2B))):
        for i in range(BAYS):
            u = len_flank / (2.0 * BAYS) + i * (len_flank / BAYS)
            rect_opening(
                f"sw{fi}_{i}", EDGE_SW, u, 2.5, za, zb, steel, glass,
                gglow if (fi, i) in LIT else None,
            )
    # three service openings in the commercial base, not a full ground rhythm
    for i, u in enumerate((7.0, 21.6, 36.2)):
        rect_opening(f"swg{i}", EDGE_SW, u, 2.0, 0.8, 3.2, steel, glass)

    # --- NE flank: party wall against 171 South Park ------------------------
    for i in range(BAYS):
        u = len_flank / (2.0 * BAYS) + i * (len_flank / BAYS)
        blind_bay(f"ne{i}", EDGE_NE, u, 2.5, Z_W1A, Z_W2B, stone)

    # --- roof ---------------------------------------------------------------
    # Gable, not barrel: the LiDAR height distribution (median 14.18 m against a
    # 16.54 m maximum) only closes on a straight slope. See REPORT.md s.2.
    u_gable_start = -HALF_L - OVERHANG
    u_gable_end = HALF_L - FLAT_RUN
    gable_roof("roof", u_gable_start, u_gable_end, HIP_RUN, steel)

    # roof glazing: what lights lofts that sit inside a roof. Flush panels on
    # both slopes, lined up with the wall bays below.
    for i, u in enumerate((-14.0, -7.0, 0.0, 7.0)):
        slope_slab(f"rooflight_sw{i}", u - 1.6, u + 1.6, 1.9, 4.6, -1, 0.0, 0.10, glassl)
        slope_slab(f"rooflight_ne{i}", u - 1.6, u + 1.6, 1.9, 4.6, +1, 0.0, 0.10, glassl)
    for i, u in enumerate((-7.0, 0.0)):
        slope_slab(f"rooflight_glow{i}", u - 1.4, u + 1.4, 2.1, 4.4, -1, 0.08, 0.15, gglow)

    # two monitors straddling the ridge, the only things allowed to break it
    for i, u in enumerate((-10.5, 3.5)):
        uv_box(f"monitor{i}", u, 0.0, Z_RIDGE - 0.55, Z_RIDGE - 0.05, 2.4, 1.5, glassl)

    # --- Varney-end mechanical roof -----------------------------------------
    # The LiDAR mean sits a metre below its median, so a sixth of the footprint
    # is well under the main roof; the aerial shows a lower flat section at this
    # end. It is also the only honest place to put the plant.
    flat_c = HALF_L - FLAT_RUN / 2.0
    uv_box("flat_deck", flat_c, 0.0, Z_EAVE - 0.05, Z_EAVE + 0.05, FLAT_RUN, 2 * HALF_W, roofd)
    ring_band(
        "flat_parapet",
        [uv(HALF_L - FLAT_RUN, -HALF_W), uv(HALF_L, -HALF_W), uv(HALF_L, HALF_W),
         uv(HALF_L - FLAT_RUN, HALF_W)],
        Z_EAVE, Z_FLAT, -0.28, 0.02, trim,
    )
    uv_box("hvac_a", HALF_L - 2.0, -2.6, Z_EAVE, Z_EAVE + 0.9, 2.2, 1.6, steel)
    uv_box("hvac_b", HALF_L - 4.4, 1.4, Z_EAVE, Z_EAVE + 0.7, 1.6, 1.2, steel)
    uv_box("vent_a", HALF_L - 1.8, 2.9, Z_EAVE, Z_EAVE + 1.0, 0.5, 0.5, steel)
    uv_box("vent_b", HALF_L - 4.9, -3.4, Z_EAVE, Z_EAVE + 0.8, 0.45, 0.45, steel)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. The 50-odd applied window panels are small and numerous —
    # their frames get a token 1-segment softening and the fills, glow shells and
    # roof glazing none at all, which is what keeps this under 9,000 triangles.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")) or obj.name.startswith("rooflight"):
            continue
        if obj.name.endswith(("_frame", "_recess")):
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
    print("[build] anchor lon/lat: -122.3945113 37.7807582 (footprint OBB centre)")
    print("[build] South Park front heading: 315.2 deg true (NW)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "181-south-park.blend")
    glb = os.path.join(out, "181-south-park.glb")
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
