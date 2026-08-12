"""War Memorial Opera House - deterministic miniature build for SF-SIM.

Run:  blender -b --python build_war_memorial_opera_house.py [-- --out DIR]

Authored world-true: the auditorium axis bears 81.11 deg cw from true north
(OSM way/32865161), front colonnade facing east onto Van Ness Avenue. The
build frame is (u, v): u+ toward the Van Ness front along the axis, v+ the
north flank; W() rotates into world axes (+X east, +Y north).

Massing from the verified footprint (see REFERENCE.md):
* front pavilion 48.6 m wide (7-bay paired-column loggia over 7 rusticated
  arches), full-width wings behind it, 56 m auditorium block, 48 m rear
  service block on Franklin, ~40 x 20 m fly tower rising to the 44 m summit;
* one unbroken entablature + cornice line at ~24.5 m around the main mass
  (anchored to the Veterans Building twin, OSM height=28 parapet);
* dark steep hipped roofscape (front hip with court skylights, auditorium
  attic hip, fly-tower cap) - the primary aerial cue;
* glow set per the app's dusk system: Toy_mustard_Glow lit panes behind every
  arch (lit-lancet pattern, arches stay opaque Toy_glass by day) plus one thin
  Toy_white_Glow soffit strip under the colonnade entablature (floodlight cue).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ------------------------------------------------------------------ site data

HEADING = 81.11                          # long-axis bearing, deg cw from N
THETA = math.radians(90.0 - HEADING)     # math angle of u+ from +X (CCW)
CT, ST = math.cos(THETA), math.sin(THETA)

LAT0 = 37.77
KX = 111320.0 * math.cos(math.radians(LAT0))
KY = 110540.0

# Oriented-bbox centre of the footprint (WGS84), at build frame (-D/2, 0).
OBB_LON, OBB_LAT = -122.4209349, 37.7785711
DEPTH = 103.97                           # E-W, Van Ness front to Franklin rear
# lon/lat of the build-frame origin (u=0, v=0  =  front face on the axis)
_ox, _oy = (-DEPTH / 2) * CT, (-DEPTH / 2) * ST
BLON = OBB_LON - _ox / KX
BLAT = OBB_LAT - _oy / KY

# ------------------------------------------------------------------- massing

W_FRONT = 48.6      # front pavilion width (v +-24.3)
W_WING = 73.30      # wings, the full frontage (v +-36.65)
W_AUD = 56.1        # auditorium block (v +-28.05)
W_REAR = 48.2       # rear service block (v +-24.1)

U_FRONT0, U_FRONT1 = 0.0, -8.8
U_WING1 = -24.5
U_AUD1 = -83.0
U_REAR1 = -DEPTH

BASE_TOP = 9.5      # rusticated basement course
COL_Z0, COL_Z1 = 10.7, 20.3              # colonnade shafts
ENT_Z0, ENT_Z1 = 21.0, 23.0              # architrave + frieze
COR_Z0, COR_Z1 = 23.0, 24.5              # projecting cornice
ATTIC_TOP = 27.0                         # front attic parapet (twin tag 28)
HIP_F0, HIP_F1 = 25.6, 31.0              # front hip roof
AT_Z0, AT_Z1 = 24.5, 30.0                # auditorium attic block walls
HIP_A1 = 33.5                            # attic hip ridge
FLY_U0, FLY_U1 = -72.0, -92.0
FLY_W = 40.0
FLY_TOP = 40.5                           # fly-tower walls; hip peaks at 44
FLY_PEAK = 44.0                          # OSM height - the building summit
REAR_TOP = 20.0

BAYS = 7
BAY_P = 36.0 / BAYS                      # colonnade bay pitch (5.143)

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",
    "Toy_sand": "ece4d4",
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_ink": "3a3530",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_white_Glow": "f7f4ec",
    "Toy_mustard_Glow": "d9a441",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


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
        # Flagged for the app's night pass; emission ships OFF.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    return mat


# -------------------------------------------------------------- mesh plumbing


def W(u, v, z):
    """Local (u, v, z) -> world (x, y, z)."""
    return (u * CT - v * ST, u * ST + v * CT, z)


def new_mesh(name, verts_local, faces, materials, face_mats=None):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(W(*v)) for v in verts_local], [], faces)
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


def box(name, cu, cv, z0, z1, su, sv, mat):
    hx, hy = su / 2, sv / 2
    verts = [(cu - hx, cv - hy, z0), (cu + hx, cv - hy, z0),
             (cu + hx, cv + hy, z0), (cu - hx, cv + hy, z0),
             (cu - hx, cv - hy, z1), (cu + hx, cv - hy, z1),
             (cu + hx, cv + hy, z1), (cu - hx, cv + hy, z1)]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7),
             (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, [mat])


def extrude_outline(name, outline_tz, base_uv, ang, depth, mat):
    """A closed slab: outline in (tangent, z) on the plane through base_uv
    with outward normal at local angle `ang`; extends `depth` behind."""
    n = (math.cos(ang), math.sin(ang))
    t = (-math.sin(ang), math.cos(ang))
    verts = []
    for d in (0.0, -depth):
        for tt, zz in outline_tz:
            verts.append((base_uv[0] + t[0] * tt + n[0] * d,
                          base_uv[1] + t[1] * tt + n[1] * d, zz))
    k = len(outline_tz)
    faces = [tuple(range(k)), tuple(range(2 * k - 1, k - 1, -1))]
    for i in range(k):
        j = (i + 1) % k
        faces.append((i, j, k + j, k + i))
    return new_mesh(name, verts, faces, [mat])


ARCH_SEG = 10


def arch_outline(w, sill, top):
    """Round-headed opening: rectangle + semicircular head (radius w/2)."""
    h = w / 2
    spring = top - h
    pts = [(-h, sill), (h, sill), (h, spring)]
    for i in range(1, ARCH_SEG):
        a = math.pi * i / ARCH_SEG
        pts.append((h * math.cos(a), spring + h * math.sin(a)))
    pts.append((-h, spring))
    return pts


def arch_slab(name, base_uv, ang, w, sill, top, proud, depth, mat):
    n = (math.cos(ang), math.sin(ang))
    base = (base_uv[0] + n[0] * proud, base_uv[1] + n[1] * proud)
    return extrude_outline(name, arch_outline(w, sill, top), base, ang,
                           depth + proud, mat)


def lit_arch(name, base_uv, ang, w, sill, top, proud, glass=True):
    """The lit-window pattern: an opaque Toy_glass arch pane (the window by
    day) with a smaller Toy_mustard_Glow pane 5 cm in front, inset all round
    so a dark reveal frames it; both back edges buried in the wall."""
    if glass:
        arch_slab(name, base_uv, ang, w, sill, top, proud, 0.30,
                  material("Toy_glass"))
    span = top - sill
    arch_slab(f"{name}_lit", base_uv, ang, w * 0.74, sill + span * 0.06,
              top - span * 0.10, proud + 0.05, 0.30,
              material("Toy_mustard_Glow"))


def hip_roof(name, u0, u1, v0, v1, z0, z1, ridge_axis, ridge_half, mat):
    """Hipped roof over rect (u0..u1, v0..v1); ridge along `ridge_axis`
    ('u' or 'v') centred, half-length ridge_half, at z1."""
    cu, cv = (u0 + u1) / 2, (v0 + v1) / 2
    if ridge_axis == "u":
        # ridge verts: 4 = (cu - rh), 5 = (cu + rh)
        verts = [(u0, v0, z0), (u1, v0, z0), (u1, v1, z0), (u0, v1, z0),
                 (cu - ridge_half, cv, z1), (cu + ridge_half, cv, z1)]
        faces = [(3, 2, 1, 0),
                 (0, 1, 5, 4),   # v0 slope
                 (2, 3, 4, 5),   # v1 slope
                 (3, 0, 4),      # u0 hip
                 (1, 2, 5)]      # u1 hip
    else:
        verts = [(u0, v0, z0), (u1, v0, z0), (u1, v1, z0), (u0, v1, z0),
                 (cu, cv - ridge_half, z1), (cu, cv + ridge_half, z1)]
        faces = [(3, 2, 1, 0),
                 (0, 1, 4),      # v0 hip
                 (1, 2, 5, 4),   # u1 slope
                 (2, 3, 5),      # v1 hip
                 (3, 0, 4, 5)]   # u0 slope
    return new_mesh(name, verts, faces, [mat])


def sloped_panel(name, hip, side, uc, size_u, size_t, mat):
    """A thin glass panel lying on a front-hip slope (skylights facing the
    memorial court and Grove St). `hip` = (v_base, z_base, v_ridge, z_ridge);
    side +1 north slope, -1 south slope; uc = centre along u."""
    v_b, z_b, v_r, z_r = hip
    run, rise = abs(v_b - v_r), z_r - z_b
    L = math.hypot(run, rise)
    dv, dz = -side * run / L, rise / L          # downslope unit (toward base)
    nv, nz = side * rise / L, run / L           # outward slope normal
    mid_v = side * (abs(v_b) + abs(v_r)) / 2
    mid_z = (z_b + z_r) / 2
    hu, ht = size_u / 2, size_t / 2
    verts = []
    for lift in (0.02, 0.18):
        for du, dt in ((-hu, -ht), (hu, -ht), (hu, ht), (-hu, ht)):
            verts.append((uc + du,
                          mid_v + dv * dt + nv * lift,
                          mid_z + dz * dt + nz * lift))
    faces = [(3, 2, 1, 0), (4, 5, 6, 7),
             (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, [mat])


# ------------------------------------------------------------------ the build


def build():
    stone = material("Toy_stone")
    sand = material("Toy_sand")
    trim = material("Toy_trim")
    glass = material("Toy_glass")
    ink = material("Toy_ink")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")

    E, N, S, R = 0.0, math.pi / 2, -math.pi / 2, math.pi  # face angles

    # ---- basement course (rusticated, proud 0.3 all round) ----
    for nm, u0, u1, w in (("base_front", U_FRONT0, U_FRONT1, W_FRONT),
                          ("base_wing", U_FRONT1, U_WING1, W_WING),
                          ("base_aud", U_WING1, U_AUD1, W_AUD),
                          ("base_rear", U_AUD1, U_REAR1, W_REAR)):
        bevel(box(nm, (u0 + u1) / 2, 0, 0, BASE_TOP,
                  abs(u1 - u0) + 0.6, w + 0.6, stone))
    # two rusticated course lines across the front base
    for i, z in enumerate((3.4, 6.2)):
        bevel(box(f"base_course{i}", 0.36, 0, z, z + 0.5, 0.12, W_FRONT - 2.0,
                  stone), width=0.04, segments=1)

    # ---- front steps (three, full colonnade width) ----
    for i, (du, z1) in enumerate(((3.4, 0.45), (2.3, 0.9), (1.2, 1.35))):
        bevel(box(f"steps{i}", 0.3 + du / 2, 0, 0, z1, du, 46.0, stone),
              width=0.08)

    # ---- upper front block ----
    # corner pavilions, full height at the front plane
    for s in (1, -1):
        bevel(box(f"pavilion_{'n' if s > 0 else 's'}", U_FRONT1 / 2, s * 21.15,
                  BASE_TOP, ATTIC_TOP, abs(U_FRONT1), 6.3, stone))
        # blind arched niche on the front face
        arch_slab(f"niche_{'n' if s > 0 else 's'}", (0.31, s * 20.9), E,
                  2.8, 11.5, 17.9, 0.08, 0.3, ink)
        # ground-floor end door
        box(f"pav_door_{'n' if s > 0 else 's'}", 0.2, s * 20.9, 1.35, 4.95,
            0.4, 2.6, ink)
        # pavilion flank lit arch
        lit_arch(f"pav_flank_{'n' if s > 0 else 's'}", (-4.4, s * 24.3),
                 N if s > 0 else S, 2.6, 11.0, 17.8, 0.06)

    # loggia back wall (recessed 2.6 m) and its floor slab
    bevel(box("loggia_wall", (-2.6 + U_FRONT1) / 2, 0, BASE_TOP, ENT_Z0,
              abs(U_FRONT1) - 2.6, 36.0, sand))
    box("loggia_floor", -1.3, 0, BASE_TOP, COL_Z0 - 0.9, 2.6, 36.0, stone)

    # 7 ground arches + 7 loggia arches on the axis grid
    for k in range(BAYS):
        vk = (k - 3) * BAY_P
        arch_slab(f"garch_rev{k}", (0.31, vk), E, 3.6, 1.35, 7.2, 0.04, 0.5, ink)
        lit_arch(f"garch{k}", (0.31, vk), E, 3.0, 1.35, 6.9, 0.10)
        lit_arch(f"larch{k}", (-2.6, vk), E, 3.4, COL_Z0, 17.9, 0.08)

    # colonnade: 8 pedestals, 16 shafts, 8 cap blocks; bay balustrades
    for k in range(BAYS + 1):
        vk = -18.0 + k * BAY_P
        bevel(box(f"pedestal{k}", -1.05, vk, BASE_TOP, COL_Z0, 1.7, 3.8, trim),
              width=0.06, segments=1)
        for s in (1, -1):
            seg = 12
            verts = []
            for z in (COL_Z0, COL_Z1):
                for i in range(seg):
                    a = 2 * math.pi * i / seg
                    verts.append((-1.05 + 0.62 * math.cos(a),
                                  vk + s * 1.0 + 0.62 * math.sin(a), z))
            faces = [(i, seg + i, seg + (i + 1) % seg, (i + 1) % seg)
                     for i in range(seg)]
            faces.append(tuple(range(seg)))
            faces.append(tuple(range(2 * seg - 1, seg - 1, -1)))
            new_mesh(f"col{k}_{'n' if s > 0 else 's'}", verts, faces, [trim])
        bevel(box(f"colcap{k}", -1.05, vk, COL_Z1, ENT_Z0, 1.8, 3.8, trim),
              width=0.06, segments=1)
    for k in range(BAYS):
        vk = (k - 3) * BAY_P
        bevel(box(f"balustrade{k}", -0.7, vk, BASE_TOP, 10.6, 0.5,
                  BAY_P - 3.6, trim), width=0.05, segments=1)

    # floodlight cue: one thin warm-white strip under the entablature soffit
    box("soffit_glow", -0.55, 0, ENT_Z0 - 0.28, ENT_Z0 - 0.05, 0.12, 35.0,
        material("Toy_white_Glow"))

    # entablature, cornice, attic across the front block
    bevel(box("entablature", -0.85, 0, ENT_Z0, COR_Z0, 2.3, W_FRONT, trim))
    bevel(box("cornice_front", -0.65, 0, COR_Z0, COR_Z1, 2.8, W_FRONT + 1.0,
              trim))
    bevel(box("attic_front", -0.6, 0, COR_Z1, ATTIC_TOP, 1.2, W_FRONT, sand))
    for k in range(BAYS):
        vk = (k - 3) * BAY_P
        box(f"attic_panel{k}", 0.03, vk, 25.1, 26.5, 0.1, 3.4, stone)

    # ---- wings (full frontage) ----
    for s in (1, -1):
        tag = "n" if s > 0 else "s"
        bevel(box(f"wing_{tag}", (U_FRONT1 + U_WING1) / 2, s * 30.475,
                  BASE_TOP, COR_Z0, abs(U_WING1 - U_FRONT1), 12.35, sand))
        # wing front faces (facing Van Ness), two lit arches each
        for i, vv in enumerate((27.9, 33.4)):
            lit_arch(f"wing_farch_{tag}{i}", (U_FRONT1 + 0.31, s * vv), E,
                     2.8, 11.0, 17.8, 0.06)
        # wing outer flanks, two lit arches each
        for i, uu in enumerate((-13.0, -20.0)):
            lit_arch(f"wing_sarch_{tag}{i}", (uu, s * 36.65),
                     N if s > 0 else S, 2.6, 11.0, 17.8, 0.06)
        # cornice returns around the wing, and the parapet the roof sits on
        bevel(box(f"wing_cornice_{tag}", (U_FRONT1 + U_WING1) / 2, s * 30.475,
                  COR_Z0, COR_Z1, abs(U_WING1 - U_FRONT1) + 1.0, 13.35, trim))
        bevel(box(f"wing_parapet_{tag}", (U_FRONT1 + U_WING1) / 2, s * 30.475,
                  COR_Z1, 25.8, abs(U_WING1 - U_FRONT1), 12.35, sand),
              width=0.06, segments=1)
        # curved reentrant quadrant against the auditorium flank
        seg = 16
        verts = []
        for z in (BASE_TOP, 25.8):
            for i in range(seg):
                a = 2 * math.pi * i / seg
                verts.append((-25.7 + 3.0 * math.cos(a),
                              s * 29.9 + 3.0 * math.sin(a), z))
        faces = [(i, seg + i, seg + (i + 1) % seg, (i + 1) % seg)
                 for i in range(seg)]
        faces.append(tuple(range(seg)))
        faces.append(tuple(range(2 * seg - 1, seg - 1, -1)))
        new_mesh(f"quadrant_{tag}", verts, faces, [sand])

    # ---- auditorium block ----
    bevel(box("aud_block", (U_WING1 + U_AUD1) / 2, 0, BASE_TOP, COR_Z0,
              abs(U_AUD1 - U_WING1), W_AUD, sand))
    bevel(box("aud_frieze", (U_WING1 + U_AUD1) / 2, 0, ENT_Z0, 22.2,
              abs(U_AUD1 - U_WING1) - 0.5, W_AUD + 0.4, trim),
          width=0.06, segments=1)
    bevel(box("aud_cornice", (U_WING1 + U_AUD1) / 2, 0, COR_Z0, COR_Z1,
              abs(U_AUD1 - U_WING1), W_AUD + 1.1, trim))
    for s in (1, -1):
        tag = "n" if s > 0 else "s"
        for k in range(8):
            uu = -30.5 - k * 6.7
            lit_arch(f"aud_arch_{tag}{k}", (uu, s * W_AUD / 2),
                     N if s > 0 else S, 2.7, 11.0, 17.7, 0.06)
    # Grove St entrance marquee (south flank)
    bevel(box("marquee", -54.0, -W_AUD / 2 - 1.1, 8.3, 8.65, 50.0, 2.6, ink),
          width=0.05, segments=1)
    # roof deck over the auditorium zone
    box("aud_deck", (U_WING1 + U_AUD1) / 2 - 0.25, 0, 23.6, 24.1,
        abs(U_AUD1 - U_WING1) - 1.0, W_AUD - 1.5, roofd)

    # ---- front hip roof with court skylights ----
    # deck bridging the attic parapet to the roof base over the loggia zone
    box("front_attic_deck", (U_FRONT1 - 0.6) / 2, 0, COR_Z1, 25.7,
        abs(U_FRONT1) + 0.6, 48.0, sand)
    hip_roof("roof_front", -24.0, -1.0, -35.8, 35.8, HIP_F0, HIP_F1,
             "v", 14.0, roofd)
    hip = (35.8, HIP_F0, 14.0, HIP_F1)
    for s, tag in ((1, "n"), (-1, "s")):
        for i, uc in enumerate((-9.5, -15.5)):
            sloped_panel(f"skylight_{tag}{i}", hip, s, uc, 4.8, 3.4, glass)

    # ---- auditorium attic + hip ----
    bevel(box("attic_block", -55.0, 0, AT_Z0, AT_Z1, 34.0, 52.0, sand))
    bevel(box("attic_cornice", -55.0, 0, 29.2, AT_Z1, 34.6, 52.8, trim),
          width=0.06, segments=1)
    for s in (1, -1):
        box(f"attic_band_{'n' if s > 0 else 's'}", -55.0, s * 26.0,
            26.3, 27.8, 27.0, 0.36, glass)
    hip_roof("roof_attic", -71.5, -38.5, -25.8, 25.8, AT_Z1, HIP_A1,
             "u", 11.0, roofd)

    # ---- fly tower (the 44 m summit) ----
    bevel(box("flytower", (FLY_U0 + FLY_U1) / 2, 0, 18.0, FLY_TOP,
              abs(FLY_U1 - FLY_U0), FLY_W, sand))
    bevel(box("fly_band", (FLY_U0 + FLY_U1) / 2, 0, 39.0, FLY_TOP,
              abs(FLY_U1 - FLY_U0) + 0.5, FLY_W + 0.5, trim),
          width=0.06, segments=1)
    hip_roof("roof_fly", FLY_U1 + 0.3, FLY_U0 - 0.3, -FLY_W / 2 + 0.3,
             FLY_W / 2 - 0.3, FLY_TOP, FLY_PEAK, "v", 8.0, roofd)
    for s in (1, -1):
        for i, uu in enumerate((-76.5, -82.0, -87.5)):
            box(f"fly_win_{'n' if s > 0 else 's'}{i}", uu,
                s * (FLY_W / 2 - 0.05), 33.5, 36.0, 1.5, 0.36, glass)

    # ---- rear service block (Franklin St) ----
    bevel(box("rear_block", (U_AUD1 + U_REAR1) / 2, 0, BASE_TOP, REAR_TOP,
              abs(U_REAR1 - U_AUD1), W_REAR, sand))
    bevel(box("rear_parapet", (U_AUD1 + U_REAR1) / 2, 0, REAR_TOP, 20.9,
              abs(U_REAR1 - U_AUD1) + 0.4, W_REAR + 0.4, trim),
          width=0.05, segments=1)
    box("rear_deck", (U_AUD1 + U_REAR1) / 2, 0, 19.4, 19.8,
        abs(U_REAR1 - U_AUD1) - 1.6, W_REAR - 1.6, roofd)
    # stage door + window grid on the rear face
    box("stage_door", U_REAR1 + 0.05, 0, 1.35, 7.35, 0.4, 5.0, ink)
    for r, z0 in ((0, 11.5), (1, 15.5)):
        for k in range(6):
            vv = (k - 2.5) * 7.0
            box(f"rear_win{r}_{k}", U_REAR1 + 0.05, vv, z0, z0 + 2.4,
                0.36, 1.6, glass)
    for s in (1, -1):
        for r, z0 in ((0, 11.5), (1, 15.5)):
            for k in range(4):
                uu = -87.5 - k * 4.6
                box(f"rear_swin_{'n' if s > 0 else 's'}{r}_{k}", uu,
                    s * (W_REAR / 2 - 0.05), z0, z0 + 2.4, 1.6, 0.36, glass)
    # tidy roof plant on the rear deck
    for i, (uu, vv, w, d, h) in enumerate(
            ((-88.0, -8.0, 6.0, 4.0, 2.2), (-97.0, 6.0, 5.0, 4.5, 1.8))):
        bevel(box(f"plant{i}", uu, vv, 19.8, 19.8 + h, w, d, steel),
              width=0.08, segments=1)
    bevel(box("stair_ph", -85.5, 14.0, 19.8, 22.4, 3.6, 3.0, sand),
          width=0.08, segments=1)


# --------------------------------------------------------- recenter + export


def recenter_and_report():
    dg = bpy.context.evaluated_depsgraph_get()
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    mn = Vector((1e12, 1e12, 1e12))
    mx = Vector((-1e12, -1e12, -1e12))
    tris = 0
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
    center = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, mn.z))
    for o in objs:
        for v in o.data.vertices:
            v.co.x -= center.x
            v.co.y -= center.y
            v.co.z -= center.z
    anchor_lon = BLON + center.x / KX
    anchor_lat = BLAT + center.y / KY
    dims = [round(mx[i] - mn[i], 3) for i in range(3)]
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] dims={dims}")
    print(f"[build] recentered by {[round(v, 3) for v in center]}")
    print(f"[build] ANCHOR lon/lat = {anchor_lon:.7f}, {anchor_lat:.7f}")
    print(f"[build] heading: axis {HEADING} deg cw from N (authored world-true)")
    return tris, dims, (anchor_lon, anchor_lat)


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)

    build()
    recenter_and_report()

    blend = os.path.join(out, "war-memorial-opera-house.blend")
    glb = os.path.join(out, "war-memorial-opera-house.glb")
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
