"""Deterministic Blender build of the SF-SIM miniature Pier 17.

    blender -b --python build_pier_17.py -- [--out DIR]

Writes pier-17.blend and pier-17.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = model AABB centre (the script recentres
after building and prints the resulting WGS84 anchor), min Z = 0 (WATER
level — bridge/island convention), flagpole tip exactly 21.3 m.

Design (see REFERENCE.md for the sources behind every number):

* the asset carries its own PIER DECK: the app bakes no pier decks and
  `placeGeneric()` clamps its terrain sample to water level over open water,
  so a 2.0 m concrete slab on the real OSM deck ring (way 1390720126,
  simplified to its 5 true corners) is the ground this landmark stands on.
  Light concrete top, dark pile/fender sides to the water;
* the shed on the real OSM building ring (way 25489458): main volume
  232 x 43 m, plus the measured bay-end step — the NW two-thirds extends
  ~5.6 m further into the bay than the SE third (the plan's first draft had
  this notch on the wrong side; REPORT.md records the correction);
* a low gable roof, eaves 11.0 m and ridge 14.0 m above water (LiDAR roof
  majority 10.46 m + 2.0 m deck; ridge from the 1st-return median), white
  membrane with a weathered gray overlay on the front ~70 m (satellite
  value split) and a raised ridge-skylight strip — the night-glow hero;
* the cream bulkhead front: a full-width shallow gable parapet to 16.9 m
  (LiDAR facade max 14.87 m above deck), one big central door bay — olive
  roll-up flanked by weathered diagonal-plank timber barn doors — the
  "PIER 17" diamond-ended sign plate, and the apex flagpole to 21.3 m
  (LiDAR 1st-return peak 19.26 m above deck) with a small pennant;
* the fog horn (Pier 17 keeps the waterfront's last original one) high on
  the bay-end gable, pointing out to sea;
* long sides as rhythm: pilaster bays, glazed Valley-side openings from the
  Exploratorium-era renovation (3 lit at night), a high window strip, three
  service doors on the quieter Pier 19 side;
* glow discipline: every _Glow face is a thin plate proud of an opaque
  surface, never a closed shell, day colour = its non-glow neighbour.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# App tangent projection constants (pipeline/lib/geo.mjs).
LON0, LAT0 = -122.4375, 37.77
M_PER_DEG_LON = 111320.0 * math.cos(math.radians(LAT0))
M_PER_DEG_LAT = 110540.0

# Shed frame: s along the pier toward the bay (bearing 54.9 deg true),
# w toward the southeast (Valley / Pier 15 side). Origin = OSM shed centroid
# (app x 3467.93, z -3558.31 = lon -122.3980898, lat 37.8021902).
S_UNIT = (0.81805, 0.57511)   # Blender (X, Y) of +s
W_UNIT = (0.57511, -0.81805)  # Blender (X, Y) of +w  (the map is a REFLECTION)
SHED_CENTROID_APP = (3467.93, -3558.31)


def sw(s, w):
    """Shed frame -> Blender world XY. Reflection: enforce CCW after mapping."""
    return (
        s * S_UNIT[0] + w * W_UNIT[0],
        s * S_UNIT[1] + w * W_UNIT[1],
    )


def ring_ccw(pts):
    """Ensure a Blender-XY polygon is CCW (positive signed area)."""
    area = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        area += x1 * y2 - x2 * y1
    return list(pts) if area > 0 else list(reversed(pts))


# OSM deck ring (way 1390720126) simplified to its true corners, shed frame.
DECK_SW = [
    (-118.40, 25.19),   # front corner, SE side
    (124.10, 25.17),    # bay corner, SE side
    (123.91, -27.99),   # bay corner, NW side
    (-96.18, -28.36),   # NW side, where the front flare begins
    (-119.28, -35.70),  # front corner, NW flare
]

# OSM shed ring (way 25489458), shed frame. Main volume + bay-end step.
SHED_MAIN_SW = [
    (-118.08, -21.42),  # front NW corner
    (-117.77, 21.66),   # front SE corner
    (114.09, 21.65),    # bay SE corner (the SE third stops here)
    (114.05, -21.43),   # on the NW wall line
]
SHED_EXT_SW = [
    (114.05, -21.43),
    (114.01, 8.18),
    (119.75, 8.18),     # measured step: NW two-thirds runs 5.6 m further
    (119.53, -21.44),
]

W_RIDGE = 0.115         # ridge offset in w (mid of the two eave lines)

Z_DECK = 2.0            # deck top above water (NAVD88 2.78 m, toy 2.0)
Z_EAVE = 11.0           # shed eaves (LiDAR roof majority 10.46 + deck)
Z_RIDGE = 14.0          # ridge (1st-return median 11.51 + deck, rounded)
Z_EXT = 12.2            # bay-end step block, flat roof
Z_PARAPET_BASE = 11.2   # front parapet shoulder
Z_PARAPET_CORNER = 11.9
Z_APEX = 16.9           # facade gable apex (LiDAR max 14.87 above deck)
Z_POLE_TOP = 21.3       # flagpole tip = targetHeightM (1st-return peak 19.26)

DOOR_Z1 = 8.9           # door leaves top
FRAME_Z1 = 10.0         # door-bay frame header top

PALETTE_HEX = {
    "Toy_trim": "f3efe6",       # cream stucco walls, parapet, sign plate
    "Toy_white": "f7f4ec",      # roof membrane (white; separates from walls)
    "Toy_stone": "d9d2c2",      # deck top (concrete apron)
    "Toy_steel": "9aa0a6",      # weathered roof, roll-up, pole, horn, RTUs
    "Toy_rust": "a86444",       # timber barn doors
    "Toy_ink": "3a3530",        # deck sides, door reveal, horn mouth
    "Toy_glass": "2a4d73",      # side glazing, strip windows, skylight glass
    "Toy_ioorange": "c0402a",   # pennant only
    "Toy_trim_Glow": "f3efe6",  # sign face, transom strip
    "Toy_glass_Glow": "6f95b8", # ridge skylight, 3 lit Valley bays
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def poly_edge(poly, i):
    """Edge i of a CCW Blender-XY polygon: (origin, length, tangent, outward)."""
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def find_edge(poly, direction, tol=0.9):
    """Index of the edge whose outward normal best matches `direction`."""
    best, best_dot = None, -2.0
    for i in range(len(poly)):
        _, _, _, n = poly_edge(poly, i)
        d = n[0] * direction[0] + n[1] * direction[1]
        if d > best_dot:
            best, best_dot = i, d
    assert best_dot > tol, f"no edge faces {direction} (best {best_dot:.2f})"
    return best


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


def face_panel(name, poly, edge, u_centre, profile, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in the plane of wall `edge` of
    `poly`, extruded outward from offset d0 to d1 along that wall's normal."""
    a, _length, t, n = poly_edge(poly, edge)
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


def box_sw(name, s, w, z0, z1, ss, sw_, mat, mat_caps=None):
    """Axis-aligned box in the SHED frame (ss along s, sw_ along w)."""
    corners_sw = [
        (s - ss / 2, w - sw_ / 2),
        (s + ss / 2, w - sw_ / 2),
        (s + ss / 2, w + sw_ / 2),
        (s - ss / 2, w + sw_ / 2),
    ]
    ring = ring_ccw([sw(a, b) for a, b in corners_sw])
    return prism(name, ring, z0, z1, mat, mat_caps)


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


def gable_profile(w_left, w_right, z_eave, z_ridge, w_ridge, z_bottom):
    """CCW (w, z) pentagon profile of the gable roof cross-section."""
    return [
        (w_left, z_bottom),
        (w_right, z_bottom),
        (w_right, z_eave),
        (w_ridge, z_ridge),
        (w_left, z_eave),
    ]


def gable_solid(name, s0, s1, w_left, w_right, mat):
    """The roof: a pentagon profile swept from s0 to s1 in the shed frame."""
    prof = gable_profile(w_left, w_right, Z_EAVE, Z_RIDGE, W_RIDGE, Z_EAVE - 0.35)
    verts = []
    for s in (s0, s1):
        for w, z in prof:
            x, y = sw(s, w)
            verts.append((x, y, z))
    npts = len(prof)
    faces = [
        (i, (i + 1) % npts, npts + (i + 1) % npts, npts + i) for i in range(npts)
    ]
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def roof_overlay(name, s0, s1, w_edge, mat, lift=0.05):
    """A thin plate lying ON one roof slope between s0 and s1 (weathered
    membrane section). w_edge < 0 for the NW slope, > 0 for the SE slope."""
    def zat(w):
        t = (w_edge - w) / (w_edge - W_RIDGE)
        return Z_EAVE + (Z_RIDGE - Z_EAVE) * t

    w_hi = W_RIDGE + (0.35 if w_edge > 0 else -0.35)
    quads = [(s0, w_edge), (s1, w_edge), (s1, w_hi), (s0, w_hi)]
    # slope normal (in the w-z plane)
    dw = abs(w_edge - W_RIDGE)
    dz = Z_RIDGE - Z_EAVE
    ln = math.hypot(dw, dz)
    nw = (dz / ln) * (1 if w_edge > 0 else -1)
    nz = dw / ln
    verts = []
    for d in (0.0, lift):
        for s, w in quads:
            x, y = sw(s, w + nw * d)
            verts.append((x, y, zat(w) + nz * d))
    faces = [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
             (3, 2, 1, 0), (4, 5, 6, 7)]
    return new_mesh(name, verts, faces, [mat])


def cylinder_panel(name, poly, edge, u, zc, r, d0, d1, mat, segments=8):
    prof = [
        (r * math.cos(2 * math.pi * i / segments),
         zc + r * math.sin(2 * math.pi * i / segments))
        for i in range(segments)
    ]
    return face_panel(name, poly, edge, u, prof, d0, d1, mat)


def diag_batten(name, poly, edge, u, w_span, z0, z1, thick, d0, d1, mat, flip=False):
    """A diagonal batten strip on a barn door: a parallelogram (u,z) profile."""
    h = thick / 2
    if not flip:
        prof = [(-w_span / 2, z0 - h + 0), (-w_span / 2, z0 + h),
                (w_span / 2, z1 + h), (w_span / 2, z1 - h)]
    else:
        prof = [(w_span / 2, z0 - h), (w_span / 2, z0 + h),
                (-w_span / 2, z1 + h), (-w_span / 2, z1 - h)]
    return face_panel(name, poly, edge, u, prof, d0, d1, mat)


# --------------------------------------------------------------------- build


def build():
    mats = {k: material(k) for k in PALETTE_HEX}
    trim = mats["Toy_trim"]
    white = mats["Toy_white"]
    stone = mats["Toy_stone"]
    steel = mats["Toy_steel"]
    rust = mats["Toy_rust"]
    ink = mats["Toy_ink"]
    glass = mats["Toy_glass"]
    orange = mats["Toy_ioorange"]
    tglow = mats["Toy_trim_Glow"]
    gglow = mats["Toy_glass_Glow"]

    # ---- deck: the pier itself -------------------------------------------
    deck_ring = ring_ccw([sw(s, w) for s, w in DECK_SW])
    bevel(prism("deck", deck_ring, 0.0, Z_DECK, ink, mat_caps=stone), 0.15)

    # ---- shed volumes -----------------------------------------------------
    main_ring = ring_ccw([sw(s, w) for s, w in SHED_MAIN_SW])
    bevel(prism("shed_main", main_ring, Z_DECK, Z_EAVE, trim), 0.10)
    ext_ring = ring_ccw([sw(s, w) for s, w in SHED_EXT_SW])
    bevel(prism("shed_ext", ext_ring, Z_DECK, Z_EXT, trim, mat_caps=white), 0.10)

    # ---- roof -------------------------------------------------------------
    bevel(gable_solid("roof", -117.9, 114.07, -21.43, 21.66, white), 0.10)
    # weathered membrane on the front ~70 m of both slopes (satellite split)
    roof_overlay("roof_weathered_nw", -117.5, -48.0, -21.35, steel)
    roof_overlay("roof_weathered_se", -117.5, -48.0, 21.58, steel)

    # ridge skylight: steel curb straddling the ridge + glow plate on top
    curb_ring = ring_ccw([sw(s, w) for s, w in [
        (-80.0, W_RIDGE - 0.8), (60.0, W_RIDGE - 0.8),
        (60.0, W_RIDGE + 0.8), (-80.0, W_RIDGE + 0.8)]])
    prism("skylight_curb", curb_ring, Z_RIDGE - 0.25, Z_RIDGE + 0.30, steel)
    # opaque dark glass so the strip reads by day; glow plate proud on top
    glass_ring = ring_ccw([sw(s, w) for s, w in [
        (-79.6, W_RIDGE - 0.66), (59.6, W_RIDGE - 0.66),
        (59.6, W_RIDGE + 0.66), (-79.6, W_RIDGE + 0.66)]])
    prism("skylight_glass", glass_ring, Z_RIDGE + 0.30, Z_RIDGE + 0.38, glass)
    glow_ring = ring_ccw([sw(s, w) for s, w in [
        (-79.0, W_RIDGE - 0.55), (59.0, W_RIDGE - 0.55),
        (59.0, W_RIDGE + 0.55), (-79.0, W_RIDGE + 0.55)]])
    prism("skylight_glow", glow_ring, Z_RIDGE + 0.38, Z_RIDGE + 0.44, gglow)

    # RTU cluster on the bay-end step's flat roof
    for i, (s, w) in enumerate([(115.8, -14.5), (117.9, -9.0), (115.9, -3.6)]):
        bevel(box_sw(f"rtu_{i}", s, w, Z_EXT, Z_EXT + 0.9, 2.6, 1.8, steel), 0.08)

    # ---- bulkhead front ----------------------------------------------------
    # Edge lookup: front normal ~ -s in Blender = (-S_UNIT).
    front = find_edge(main_ring, (-S_UNIT[0], -S_UNIT[1]))
    a, flen, t, n = poly_edge(main_ring, front)
    uc = flen / 2.0

    # parapet: full-width shallow gable, a closed slab proud of the wall
    parapet_prof = [
        (-flen / 2, Z_PARAPET_BASE - 1.2), (flen / 2, Z_PARAPET_BASE - 1.2),
        (flen / 2, Z_PARAPET_CORNER), (0.0, Z_APEX), (-flen / 2, Z_PARAPET_CORNER),
    ]
    bevel(face_panel("parapet", main_ring, front, uc, parapet_prof,
                     -0.20, 0.30, trim), 0.10)

    # door bay: header + jambs (proud frame), dark reveal, three door leaves
    face_panel("door_header", main_ring, front, uc,
               rect_profile(29.6, DOOR_Z1 + 0.1, FRAME_Z1), 0.0, 0.38, trim)
    for side in (-1, 1):
        face_panel(f"door_jamb_{side}", main_ring, front, uc + side * 14.4,
                   rect_profile(0.9, Z_DECK, FRAME_Z1), 0.0, 0.38, trim)
    face_panel("door_reveal", main_ring, front, uc,
               rect_profile(28.0, Z_DECK, DOOR_Z1 + 0.15), 0.0, 0.04, ink)
    face_panel("rollup", main_ring, front, uc,
               rect_profile(12.0, Z_DECK, DOOR_Z1 - 0.4), 0.0, 0.12, steel)
    for side in (-1, 1):
        u_door = uc + side * 10.2
        face_panel(f"barn_{side}", main_ring, front, u_door,
                   rect_profile(7.8, Z_DECK, DOOR_Z1 - 0.2), 0.0, 0.15, rust)
        for k, u_off in enumerate((-2.4, 0.0, 2.4)):
            diag_batten(f"batten_{side}_{k}", main_ring, front, u_door + u_off,
                        2.2, Z_DECK + 0.7, DOOR_Z1 - 1.1, 0.28, 0.15, 0.22,
                        rust, flip=(side > 0))

    # transom glow strip over the roll-up (proud of the reveal and doors)
    face_panel("transom_glow", main_ring, front, uc,
               rect_profile(11.4, DOOR_Z1 - 0.25, DOOR_Z1 + 0.05), 0.16, 0.22, tglow)

    # sign: ink diamond-ended backing + glow face
    sign_z = 13.1
    sign_prof = [(-3.9, sign_z), (-3.2, sign_z + 0.75), (3.2, sign_z + 0.75),
                 (3.9, sign_z), (3.2, sign_z - 0.75), (-3.2, sign_z - 0.75)]
    face_panel("sign_back", main_ring, front, uc, sign_prof, 0.30, 0.40, trim)
    sign_face = [(-3.55, sign_z), (-2.95, sign_z + 0.62), (2.95, sign_z + 0.62),
                 (3.55, sign_z), (2.95, sign_z - 0.62), (-2.95, sign_z - 0.62)]
    face_panel("sign_glow", main_ring, front, uc, sign_face, 0.40, 0.46, tglow)

    # window band + receiving door at the SE end of the front (photo, right)
    face_panel("front_winband", main_ring, front, uc + 16.9,
               rect_profile(4.6, 4.2, 6.2), 0.0, 0.08, glass)
    face_panel("front_recvdoor", main_ring, front, uc + 13.6,
               rect_profile(1.6, Z_DECK, 4.4), 0.0, 0.08, steel)

    # flagpole + pennant at the apex (hexagonal, tip = bbox top 21.3)
    apex_x = a[0] + t[0] * uc - n[0] * 0.05
    apex_y = a[1] + t[1] * uc - n[1] * 0.05
    pole_prof = [(apex_x + 0.14 * math.cos(k * math.pi / 3),
                  apex_y + 0.14 * math.sin(k * math.pi / 3)) for k in range(6)]
    prism("flagpole", ring_ccw(pole_prof), Z_APEX - 0.5, Z_POLE_TOP, steel)
    # pennant: thin triangle streaming toward the SE (+w), 2.0 m
    pw = [sw(0, 0), sw(0, 0)]  # placeholder to keep linters calm
    base_s = -117.9
    p0 = sw(base_s, 0.25)
    p1 = sw(base_s, 2.25)
    pen_verts = [
        (apex_x + 0.10, apex_y, 20.35), (apex_x + 0.10, apex_y, 21.05),
        (apex_x + (p1[0] - p0[0]), apex_y + (p1[1] - p0[1]), 20.70),
        (apex_x - 0.10, apex_y, 20.35), (apex_x - 0.10, apex_y, 21.05),
    ]
    new_mesh("pennant", pen_verts,
             [(0, 1, 2), (4, 3, 2), (0, 2, 3), (1, 4, 2), (0, 3, 4, 1)], [orange])

    # ---- long sides ---------------------------------------------------------
    se_edge = find_edge(main_ring, (W_UNIT[0], W_UNIT[1]))
    nw_edge = find_edge(main_ring, (-W_UNIT[0], -W_UNIT[1]))
    _, se_len, _, _ = poly_edge(main_ring, se_edge)
    _, nw_len, _, _ = poly_edge(main_ring, nw_edge)

    # pilasters every ~14.5 m, both sides
    for edge, length, tag in ((se_edge, se_len, "se"), (nw_edge, nw_len, "nw")):
        nbay = 16
        for i in range(1, nbay):
            u = length * i / nbay
            face_panel(f"pilaster_{tag}_{i}", main_ring, edge, u,
                       rect_profile(0.6, Z_DECK, Z_EAVE - 0.35), 0.0, 0.14, trim)

    # Valley (SE) side: 7 glazed bays, 3 lit; high strip windows
    # NOTE: on the SE edge, u runs from the BAY corner toward the FRONT corner
    # (CCW winding), so u = se_len/2 is still the shed's midpoint.
    for i in range(7):
        u = se_len / 2 + (i - 3) * 14.5
        face_panel(f"bay_glass_{i}", main_ring, se_edge, u,
                   rect_profile(6.0, 2.6, 7.1), 0.0, 0.08, glass)
        if i in (1, 3, 5):
            face_panel(f"bay_glow_{i}", main_ring, se_edge, u,
                       rect_profile(5.4, 2.9, 5.6), 0.10, 0.16, gglow)
    # one strip window per pilaster bay so the two rhythms never collide
    for i in range(10):
        u = se_len / 2 + (i - 4.5) * 14.5
        face_panel(f"strip_win_{i}", main_ring, se_edge, u,
                   rect_profile(10.0, 8.7, 9.9), 0.0, 0.06, glass)

    # NW side: 3 service doors
    for i, du in enumerate((-60.0, 0.0, 60.0)):
        face_panel(f"nw_door_{i}", main_ring, nw_edge, nw_len / 2 + du,
                   rect_profile(4.0, Z_DECK, 6.6), 0.0, 0.08, steel)

    # ---- bay end: gable face + fog horn ------------------------------------
    bay_edge = find_edge(main_ring, (S_UNIT[0], S_UNIT[1]))
    _, bay_len, _, _ = poly_edge(main_ring, bay_edge)
    # end door on the gable face above the step block's roof line
    face_panel("bay_door", main_ring, bay_edge, bay_len / 2 - 8.0,
               rect_profile(8.0, Z_DECK, 7.6), 0.0, 0.10, steel)
    # fog horn: barrel + throat + flared mouth, pointing out to the bay
    horn_u = bay_len / 2 - 14.0  # on the SE third of the gable face
    cylinder_panel("horn_barrel", main_ring, bay_edge, horn_u, 12.4, 0.42,
                   0.0, 1.0, steel)
    cylinder_panel("horn_throat", main_ring, bay_edge, horn_u, 12.4, 0.24,
                   1.0, 1.7, steel)
    horn_mouth = [(0.62 * math.cos(2 * math.pi * i / 8),
                   12.4 + 0.62 * math.sin(2 * math.pi * i / 8)) for i in range(8)]
    face_panel("horn_mouth", main_ring, bay_edge, horn_u, horn_mouth,
               1.7, 2.15, ink)


# ------------------------------------------------------------------- recentre


def recentre_and_report():
    """Shift everything so the world AABB centre lands on X=Y=0, then report
    the resulting WGS84 anchor and headline numbers."""
    dg = bpy.context.evaluated_depsgraph_get()
    mn = Vector((1e12, 1e12, 1e12))
    mx = Vector((-1e12, -1e12, -1e12))
    tris = 0
    for o in bpy.data.objects:
        if o.type != "MESH":
            continue
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for v in me.vertices:
            wv = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], wv[i])
                mx[i] = max(mx[i], wv[i])
        ev.to_mesh_clear()
    cx, cy = (mn.x + mx.x) / 2, (mn.y + mx.y) / 2
    for o in bpy.data.objects:
        if o.type == "MESH":
            o.data.transform(
                __import__("mathutils").Matrix.Translation((-cx, -cy, 0.0))
            )
    # anchor = shed centroid + world offset (Blender +Y north = app -z)
    app_x = SHED_CENTROID_APP[0] + cx
    app_z = SHED_CENTROID_APP[1] - cy
    lon = LON0 + app_x / M_PER_DEG_LON
    lat = LAT0 - app_z / M_PER_DEG_LAT
    print(f"[build] tris={tris}")
    print(f"[build] AABB after recentre: "
          f"x {mn.x - cx:.2f}..{mx.x - cx:.2f}  y {mn.y - cy:.2f}..{mx.y - cy:.2f}"
          f"  z {mn.z:.2f}..{mx.z:.2f}")
    print(f"[build] anchor app=({app_x:.2f}, {app_z:.2f})  "
          f"lonlat=({lon:.7f}, {lat:.7f})")
    return tris


# ----------------------------------------------------------------------- main


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    out = argv[argv.index("--out") + 1] if "--out" in argv else here
    os.makedirs(out, exist_ok=True)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.data.scenes.new("Pier17")
    bpy.context.window.scene = scene

    build()
    recentre_and_report()

    blend = os.path.join(out, "pier-17.blend")
    glb = os.path.join(out, "pier-17.glb")
    for o in bpy.data.objects:
        o.select_set(False)
    for o in bpy.data.objects:
        if o.type == "MESH":
            o.select_set(True)
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    bpy.ops.export_scene.gltf(
        filepath=glb,
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_format="GLB",
    )
    print(f"[build] wrote {blend}")
    print(f"[build] wrote {glb}")


if __name__ == "__main__":
    main()
