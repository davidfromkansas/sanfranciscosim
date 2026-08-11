"""Deterministic Blender build of the SF-SIM miniature California Academy of Sciences.

    blender -b --python build_cal_academy.py -- [--out DIR]

Writes cal-academy.blend and cal-academy.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, origin at the base centre, min Z = 0, so the export needs no
transforms applied after the fact.

Design (see REFERENCE.md for the sources behind every number):

* a very low, very wide museum block: 161.3 x 102.5 m footprint on the
  Music Concourse grid (long axis bearing 48.3 deg true, i.e. yawed
  +41.7 deg CCW from +X), front facade facing NW toward the concourse;
* the hero is the undulating living roof: a smooth displaced green field
  carrying the seven hills of San Francisco - two dominant 27 m-class domes
  (planetarium WSW, rainforest ENE) flanking the round central piazza, and
  five smaller mounds placed with the photographed asymmetry. Roof plane at
  10 m, perimeter eave at 11.3 m, hill peaks at 19.3 m (Fondazione RP);
* 26 white porthole skylights ring the dome slopes like craters, semantically
  enlarged to stay readable from the app camera;
* the thin floating eave: an 8.5 m overhanging plate with a white fascia and
  the dark photovoltaic fringe inset on top, wrapping the whole perimeter;
* continuous dark glass walls with a chunky white mullion rhythm beneath the
  eave, plus a modest recessed entrance portal on the NW front;
* the 27 m piazza "Bolla": a white spider-web rimmed concave canopy dish
  (Toy_white_Glow - the piazza is the night identity) with an open oculus
  over a glowing courtyard disc.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

FOOT_X = 161.3  # long axis, metres (OSM oriented bbox)
FOOT_Y = 102.5  # short axis
YAW = math.radians(41.7)  # +X (long axis) -> bearing 48.3 true; +Y local = NW front

H_PLINTH = 1.2
H_WALL_TOP = 10.0  # roof plane (RPBW: lifted 10 m)
H_EAVE = 11.3  # top of the perimeter canopy plate (Fondazione RP)
H_PEAK = 19.3  # tallest hill crest (Fondazione RP)

OVERHANG = 8.5  # eave projection beyond the footprint
FASCIA_W = 1.2  # white rim on the eave top
WALK_W = 2.65  # pale maintenance strip between PV band and the green
WALL_INSET = 0.5  # glass line sits just inside the footprint edge
MULLION_PITCH = 6.7

FIELD_Z = H_EAVE + 0.02  # green field base sits on the eave plate
GRID_NX = 116  # roof heightfield resolution (the triangle budget hero)
GRID_NY = 74

PIAZZA_R_DRUM = 13.8  # outer white drum around the piazza
PIAZZA_R_DISH = 13.0  # spider-web dish rim (27 m diameter Bolla)
PIAZZA_R_OCULUS = 4.2
SKY_R = 1.8  # porthole skylights, semantically enlarged

# Seven hills: (cx, cy, radius, height-above-field). The two 27 m-class domes
# peak at H_PEAK; the five mounds follow the photographed asymmetry. Profiles
# are full spherical-cap-like bulges ("steeply sloped domes"), not gaussians.
# The whole field is normalised after sampling so the crest lands at exactly
# H_PEAK (see _FIELD_SCALE below).
HILLS = [
    (-24.0, 2.0, 17.5, H_PEAK - FIELD_Z),        # Morrison Planetarium (WSW)
    (24.0, -1.0, 17.5, H_PEAK - FIELD_Z - 0.4),  # Osher Rainforest (ENE)
    (-58.0, -22.0, 12.5, 3.4),                   # WSW rear mound
    (-52.0, 26.0, 10.5, 2.7),                    # WSW front mound
    (55.0, 20.0, 11.5, 3.1),                     # ENE front mound
    (58.0, -18.0, 9.5, 2.5),                     # ENE rear mound
    (8.0, -34.0, 10.5, 2.3),                     # rear-centre mound
]

# Broad, low swells that keep the whole field rolling between the hills, the
# way the real 87%-planted roof undulates everywhere.
SWELLS = [
    (-45.0, 8.0, 24.0, 1.2),
    (45.0, 12.0, 21.0, 1.0),
    (-8.0, 28.0, 25.0, 1.1),
    (20.0, -28.0, 23.0, 0.9),
]

# Porthole skylights: rings of eight on each dome, the rest scattered on the
# mounds. Count is a design decision (no published figure - REFERENCE.md).
def skylight_positions():
    pts = []
    # ring phase 22.5 deg keeps every porthole clear of the piazza drum
    for cx, cy, ring_r, a0 in ((-24.0, 2.0, 11.0, 22.5), (24.0, -1.0, 11.0, 22.5)):
        for i in range(8):
            a = math.radians(a0 + i * 45.0)
            pts.append((cx + ring_r * math.cos(a), cy + ring_r * math.sin(a)))
    pts.append((30.5, 5.5))  # ninth porthole on the rainforest upper slope
    pts += [
        (-62.0, -24.5), (-53.5, -17.0),   # WSW rear mound
        (-55.5, 29.5), (-48.0, 23.5),     # WSW front mound
        (51.0, 16.5), (59.5, 23.5),       # ENE front mound
        (61.5, -15.0), (55.0, -21.5),     # ENE rear mound
        (8.0, -37.5),                     # rear-centre mound
    ]
    return pts  # 8 + 8 + 1 + 9 = 26


# Project palette from .agents/skills/sf-asset-check (hex, sRGB), authored as
# linear values, which is what the shipped kit GLBs hold.
PALETTE_HEX = {
    "Toy_mint": "8fd0a8",
    "Toy_verdigris": "9fb8a8",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_white": "f7f4ec",
    "Toy_stone": "d9d2c2",
    "Toy_ink": "3a3530",
    "Toy_trim": "f3efe6",
    "Toy_white_Glow": "f7f4ec",
    "Toy_gold_Glow": "caa64a",
    "Toy_trim_Glow": "f3efe6",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# -------------------------------------------------------------- mesh helpers


def rot2(p, ang=None):
    a = YAW if ang is None else ang
    c, s = math.cos(a), math.sin(a)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def new_mesh(name, verts, faces, materials, face_mats=None, smooth=False, yawed=True):
    """Create an object from local-frame verts; yaw them onto the true heading."""
    if yawed:
        verts = [(*rot2((v[0], v[1])), v[2]) for v in verts]
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
    if smooth:
        mesh.polygons.foreach_set("use_smooth", [True] * len(mesh.polygons))
    else:
        mesh.shade_flat()
    return obj


def bevel(obj, width=0.15, segments=2):
    """Miniature-style edge softening on the chunky solids (style bible s.4)."""
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


def box(name, cx, cy, z0, z1, sx, sy, mat, local_yaw=0.0, face_mats=None, mats=None):
    hx, hy = sx / 2, sy / 2
    corners = [rot2(c, local_yaw) for c in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy))]
    verts = [(cx + x, cy + y, z0) for x, y in corners]
    verts += [(cx + x, cy + y, z1) for x, y in corners]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, mats or [mat], face_mats)


def rect_ring(name, z, ox, oy, ix, iy, mat, thick=0.0):
    """A flat rectangular annulus (4 quads); optionally a thin raised slab."""
    if thick <= 0.0:
        verts = [
            (-ox, iy, z), (ox, iy, z), (ox, oy, z), (-ox, oy, z),
            (-ox, -oy, z), (ox, -oy, z), (ox, -iy, z), (-ox, -iy, z),
            (ix, -iy, z), (ox, -iy, z), (ox, iy, z), (ix, iy, z),
            (-ox, -iy, z), (-ix, -iy, z), (-ix, iy, z), (-ox, iy, z),
        ]
        faces = [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15)]
        return new_mesh(name, verts, faces, [mat])
    # raised band built from four slim boxes (E/W kept between N/S to avoid
    # coplanar overlap)
    zc0, zc1 = z, z + thick
    objs = [
        box(f"{name}_n", 0, (oy + iy) / 2, zc0, zc1, 2 * ox, oy - iy, mat),
        box(f"{name}_s", 0, -(oy + iy) / 2, zc0, zc1, 2 * ox, oy - iy, mat),
        box(f"{name}_e", (ox + ix) / 2, 0, zc0, zc1, ox - ix, 2 * iy, mat),
        box(f"{name}_w", -(ox + ix) / 2, 0, zc0, zc1, ox - ix, 2 * iy, mat),
    ]
    return objs


def cylinder(name, cx, cy, z0, z1, radius, side_mat, cap_mat=None, seg=12,
             cap_top=True, cap_bottom=False, smooth=False):
    mats = [side_mat] + ([cap_mat] if cap_mat and cap_mat != side_mat else [])
    cap_idx = len(mats) - 1
    verts = []
    for z in (z0, z1):
        for i in range(seg):
            a = 2 * math.pi * i / seg
            verts.append((cx + radius * math.cos(a), cy + radius * math.sin(a), z))
    faces = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]
    face_mats = [0] * seg
    if cap_bottom:
        faces.append(tuple(range(seg - 1, -1, -1)))
        face_mats.append(cap_idx if cap_mat else 0)
    if cap_top:
        faces.append(tuple(range(seg, 2 * seg)))
        face_mats.append(cap_idx if cap_mat else 0)
    return new_mesh(name, verts, faces, mats, face_mats, smooth=smooth)


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
        # Flagged for the app's night pass; emission is off in the daylight asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    mat.blend_method = "OPAQUE"
    return mat


# ------------------------------------------------------------ roof heightfield


def smoothstep(e0, e1, x):
    t = min(max((x - e0) / (e1 - e0), 0.0), 1.0)
    return t * t * (3.0 - 2.0 * t)


def field_half_dims():
    # green field stops WALK_W inside the wall line
    hx = FOOT_X / 2 - WALL_INSET - WALK_W
    hy = FOOT_Y / 2 - WALL_INSET - WALK_W
    return hx, hy


def roof_height(x, y):
    """Height of the living roof above FIELD_Z at local (x, y)."""
    hx, hy = field_half_dims()
    h = 0.0
    for cx, cy, r, amp in HILLS:
        d = math.hypot(x - cx, y - cy)
        if d < r:
            # full-bellied spherical-cap profile: steep flanks, round crown
            h += amp * (1.0 - (d / r) ** 2) ** 0.72
    for cx, cy, r, amp in SWELLS:
        d = math.hypot(x - cx, y - cy)
        if d < r:
            h += amp * (0.5 + 0.5 * math.cos(math.pi * d / r))
    # keep the field flat around the piazza drum
    dp = math.hypot(x, y)
    h *= smoothstep(PIAZZA_R_DRUM + 1.0, PIAZZA_R_DRUM + 9.0, dp)
    # fade to the flat perimeter band
    edge = min(hx - abs(x), hy - abs(y))
    h *= smoothstep(0.0, 7.0, edge)
    return h


_FIELD_SCALE = None


def field_scale():
    """Uniform height factor putting the sampled crest at exactly H_PEAK."""
    global _FIELD_SCALE
    if _FIELD_SCALE is None:
        hx, hy = field_half_dims()
        raw_max = max(
            roof_height(-hx + 2 * hx * i / GRID_NX, -hy + 2 * hy * j / GRID_NY)
            for j in range(GRID_NY + 1)
            for i in range(GRID_NX + 1)
        )
        _FIELD_SCALE = (H_PEAK - FIELD_Z) / raw_max
    return _FIELD_SCALE


def roof_z(x, y):
    return FIELD_Z + roof_height(x, y) * field_scale()


def build_roof_field(mint):
    hx, hy = field_half_dims()
    nx, ny = GRID_NX, GRID_NY
    verts = []
    for j in range(ny + 1):
        for i in range(nx + 1):
            x = -hx + 2 * hx * i / nx
            y = -hy + 2 * hy * j / ny
            verts.append((x, y, roof_z(x, y)))
    faces = []
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i
            faces.append((a, a + 1, a + nx + 2, a + nx + 1))
    obj = new_mesh("living_roof", verts, faces, [mint], smooth=True)
    return obj


# --------------------------------------------------------------------- build


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    mint = material("Toy_mint")
    verdi = material("Toy_verdigris")
    glass = material("Toy_glass")
    white = material("Toy_white")
    stone = material("Toy_stone")
    ink = material("Toy_ink")
    trim = material("Toy_trim")
    glow = material("Toy_white_Glow")
    gold_glow = material("Toy_gold_Glow")
    trim_glow = material("Toy_trim_Glow")

    fx, fy = FOOT_X / 2, FOOT_Y / 2
    px, py = fx + OVERHANG, fy + OVERHANG  # eave plate half-dims
    wx, wy = fx - WALL_INSET, fy - WALL_INSET  # glass line

    # --- plinth ------------------------------------------------------------
    bevel(box("plinth", 0, 0, 0.0, H_PLINTH, FOOT_X, FOOT_Y, stone), width=0.2)

    # --- glass perimeter walls with chunky white mullions ------------------
    # (tops/bottoms tucked 4 cm into the plate and plinth so no face is
    # exactly coplanar with another solid's face)
    box("glass_walls", 0, 0, H_PLINTH - 0.1, H_WALL_TOP - 0.04, 2 * wx, 2 * wy, glass)
    for sx in (-1, 1):  # mullions along the long (front/back) facades
        n = int((2 * wx) // MULLION_PITCH)
        for i in range(n + 1):
            x = -wx + (2 * wx - n * MULLION_PITCH) / 2 + i * MULLION_PITCH
            box(f"mull_y{sx}_{i}", x, sx * wy, H_PLINTH - 0.1, H_WALL_TOP - 0.04,
                0.45, 1.15, white)
    for sy in (-1, 1):  # mullions along the short ends
        n = int((2 * wy) // MULLION_PITCH)
        for i in range(n + 1):
            y = -wy + (2 * wy - n * MULLION_PITCH) / 2 + i * MULLION_PITCH
            box(f"mull_x{sy}_{i}", sy * wx, y, H_PLINTH - 0.1, H_WALL_TOP - 0.04,
                1.15, 0.45, white)
    for cx_, cy_ in ((-wx, -wy), (wx, -wy), (wx, wy), (-wx, wy)):  # corner piers
        bevel(box(f"pier_{cx_ > 0}_{cy_ > 0}", cx_, cy_, H_PLINTH - 0.1,
                  H_WALL_TOP - 0.04, 2.4, 2.4, trim), width=0.2)

    # --- entrance portal + steps on the NW front (+Y local) ----------------
    for k, (w, d, h) in enumerate(((19.0, 1.3, 0.42), (17.0, 2.5, 0.82),
                                   (15.0, 3.7, H_PLINTH))):
        box(f"step_{k}", 0, fy + d / 2, 0.0, h, w, d, stone)
    for sx in (-1, 1):
        bevel(box(f"portal_fin_{sx}", sx * 7.2, wy + 0.9, H_PLINTH - 0.1, 9.6,
                  1.7, 2.3, trim), width=0.2)
    bevel(box("portal_lintel", 0, wy + 0.9, 8.4, 9.6, 16.1, 2.3, trim), width=0.2)
    # lit lobby doors: cream by day, the warm entrance at night
    box("portal_doors", 0, wy + 0.12, 1.3, 8.3, 11.6, 0.4, trim_glow)

    # night state - the lit interior seen through the top of the glass walls:
    # a continuous warm ribbon under the eave, broken visually by the mullions
    rect_ring("glow_ribbon", 9.0, wx + 0.16, wy + 0.16, wx - 0.14, wy - 0.14,
              gold_glow, thick=0.72)

    # --- the floating eave plate -------------------------------------------
    # fascia + sides Toy_trim, soffit Toy_verdigris (deep eave underside)
    plate = box("eave_plate", 0, 0, H_WALL_TOP, H_EAVE, 2 * px, 2 * py, trim,
                face_mats=[1, 0, 0, 0, 0, 0], mats=[trim, verdi])
    bevel(plate, width=0.12)
    # photovoltaic fringe inset on the eave top (fascia rim stays trim): an
    # outer light-glass ring and an inner dark PV ring, so the deep overhang
    # reads luminous rather than as one heavy dark frame
    glassl = material("Toy_glassl")
    mid_x = wx + (px - FASCIA_W - wx) * 0.5
    mid_y = wy + (py - FASCIA_W - wy) * 0.5
    rect_ring("canopy_glass", H_EAVE, px - FASCIA_W, py - FASCIA_W, mid_x, mid_y,
              glassl, thick=0.08)
    rect_ring("pv_band", H_EAVE, mid_x, mid_y, wx, wy, ink, thick=0.1)
    # pale maintenance walkway between the PV band and the green
    hx, hy = field_half_dims()
    rect_ring("roof_walk", H_EAVE, wx, wy, hx, hy, stone, thick=0.06)

    # --- the living roof ----------------------------------------------------
    # (its border sits at FIELD_Z, tucked behind the raised walkway band)
    build_roof_field(mint)

    # --- porthole skylights, tilted flush to the roof slope ----------------
    eps = 0.5
    for k, (sx, sy_) in enumerate(skylight_positions()):
        zs = roof_z(sx, sy_)
        dzdx = (roof_z(sx + eps, sy_) - roof_z(sx - eps, sy_)) / (2 * eps)
        dzdy = (roof_z(sx, sy_ + eps) - roof_z(sx, sy_ - eps)) / (2 * eps)
        n = Vector((-dzdx, -dzdy, 1.0)).normalized()
        up = Vector((0.0, 0.0, 1.0))
        t1 = Vector((1.0, 0.0, 0.0)) if abs(n.dot(up)) > 0.999 else up.cross(n).normalized()
        t2 = n.cross(t1)
        c = Vector((sx, sy_, zs))
        seg12 = 12
        verts, faces, fmats = [], [], []
        for h in (-1.0, 0.7):
            for i in range(seg12):
                a = 2 * math.pi * i / seg12
                p = c + n * h + (t1 * math.cos(a) + t2 * math.sin(a)) * SKY_R
                verts.append(tuple(p))
        for i in range(seg12):
            j = (i + 1) % seg12
            faces.append((i, j, seg12 + j, seg12 + i))
            fmats.append(0)
        faces.append(tuple(range(seg12 - 1, -1, -1)))
        fmats.append(0)
        faces.append(tuple(range(seg12, 2 * seg12)))
        fmats.append(1)
        # glowing rims: by day identical to Toy_white, at night the portholes
        # become rings of light on the dark hills
        new_mesh(f"skylight_{k}", verts, faces, [glow, glass], fmats)

    # --- the piazza "Bolla" -------------------------------------------------
    # white drum rim around the 27 m opening
    seg = 40
    r0, r1 = PIAZZA_R_DISH, PIAZZA_R_DRUM
    verts, faces = [], []
    for r in (r1, r0):
        for zz in (FIELD_Z, 12.35):
            for i in range(seg):
                a = 2 * math.pi * i / seg
                verts.append((r * math.cos(a), r * math.sin(a), zz))
    for i in range(seg):
        j = (i + 1) % seg
        faces.append((i, j, seg + j, seg + i))              # outer wall
        faces.append((seg + i, seg + j, 3 * seg + j, 3 * seg + i))  # top ring
        faces.append((3 * seg + i, 3 * seg + j, 2 * seg + j, 2 * seg + i))  # inner
        faces.append((2 * seg + i, 2 * seg + j, j, i))      # bottom ring
    new_mesh("piazza_drum", verts, faces, [white], smooth=False)

    # concave spider-web canopy dish (the night-glow surface)
    rings = 5
    verts, faces = [], []
    def dish_z(r):
        # concave bowl; the low point stays just above the eave plate top
        t = (r - PIAZZA_R_OCULUS) / (PIAZZA_R_DISH - PIAZZA_R_OCULUS)
        return 11.34 + (12.25 - 11.34) * t * t
    for ri in range(rings + 1):
        r = PIAZZA_R_OCULUS + (PIAZZA_R_DISH - PIAZZA_R_OCULUS) * ri / rings
        if ri == rings:
            r = PIAZZA_R_DISH + 0.45  # tuck the rim under the drum's top plate
        for i in range(seg):
            a = 2 * math.pi * i / seg
            verts.append((r * math.cos(a), r * math.sin(a), dish_z(min(r, PIAZZA_R_DISH))))
    for ri in range(rings):
        for i in range(seg):
            j = (i + 1) % seg
            a = ri * seg
            faces.append((a + i, a + j, a + seg + j, a + seg + i))
    new_mesh("piazza_dish", verts, faces, [glow], smooth=True)

    # spider-web ribs: closed thin solids (rings + 12 radials), never
    # single-sided strips - grazing rays must always meet an outward face
    for rname, rr in (("oculus_ring", PIAZZA_R_OCULUS), ("mid_ring", 8.2)):
        verts, faces = [], []
        z0, z1 = dish_z(rr) - 0.08, dish_z(rr) + 0.30
        for radius in (rr + 0.12, rr - 0.12):
            for zz in (z0, z1):
                for i in range(seg):
                    a = 2 * math.pi * i / seg
                    verts.append((radius * math.cos(a), radius * math.sin(a), zz))
        for i in range(seg):
            j = (i + 1) % seg
            faces.append((i, j, seg + j, seg + i))                      # outer
            faces.append((3 * seg + i, 3 * seg + j, 2 * seg + j, 2 * seg + i))  # inner
            faces.append((seg + i, seg + j, 3 * seg + j, 3 * seg + i))  # top
            faces.append((2 * seg + i, 2 * seg + j, j, i))              # bottom
        new_mesh(rname, verts, faces, [white], smooth=True)
    n_seg = 5
    for i in range(12):
        a = 2 * math.pi * i / 12
        ca, sa = math.cos(a), math.sin(a)
        half_w = 0.26
        ox, oy = -sa * half_w, ca * half_w
        verts, faces = [], []
        for kk in range(n_seg + 1):
            r = PIAZZA_R_OCULUS + (PIAZZA_R_DISH - PIAZZA_R_OCULUS) * kk / n_seg
            z = dish_z(r)
            verts.append((r * ca - ox, r * sa - oy, z + 0.26))
            verts.append((r * ca + ox, r * sa + oy, z + 0.26))
            verts.append((r * ca - ox, r * sa - oy, z + 0.04))
            verts.append((r * ca + ox, r * sa + oy, z + 0.04))
        for kk in range(n_seg):
            a0 = 4 * kk
            faces.append((a0, a0 + 1, a0 + 5, a0 + 4))          # top
            faces.append((a0 + 3, a0 + 2, a0 + 6, a0 + 7))      # bottom
            faces.append((a0 + 1, a0 + 3, a0 + 7, a0 + 5))      # side
            faces.append((a0 + 2, a0, a0 + 4, a0 + 6))          # side
        faces.append((1, 0, 2, 3))                              # inner end cap
        a0 = 4 * n_seg
        faces.append((a0, a0 + 1, a0 + 3, a0 + 2))              # outer end cap
        new_mesh(f"web_rib_{i}", verts, faces, [white], smooth=True)

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
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "cal-academy.blend")
    glb = os.path.join(out, "cal-academy.glb")
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
