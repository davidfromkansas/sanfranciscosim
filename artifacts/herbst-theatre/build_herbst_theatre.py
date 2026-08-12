"""Herbst Theatre / War Memorial Veterans Building - deterministic miniature
build for SF-SIM.

Run:  blender -b --python build_herbst_theatre.py [-- --out DIR]

The northern half of the War Memorial pair (401 Van Ness Avenue). Officially
"substantially identical" to the Opera House twin south of the memorial court
(SF Landmark #84), so EVERY z constant below is lifted unchanged from
`artifacts/war-memorial-opera-house/build_war_memorial_opera_house.py`: the two
buildings must share a base course, a cornice line and a roof colour when the
app's camera sees them together. What differs is the plan (a smaller, shallower
footprint) and the silhouette (no fly tower - this is the calm one).

Authored world-true: the long axis bears 81.11 deg cw from true north
(OSM way/32865757), front colonnade facing east onto Van Ness Avenue. The build
frame is (u, v): u+ toward the Van Ness front along the axis, v+ the north
flank; W() rotates into world axes (+X east, +Y north).

Massing measured from the 37-node OSM footprint (see REFERENCE.md 2.4):
* front pavilion 45.5 m wide (7-bay paired-column loggia over 7 rusticated
  arches) with stepped shoulders, full-width 67.38 m wings behind it,
  51.4 m main block, 41.15 m rear block on Franklin;
* one unbroken entablature + cornice line at 24.5 m around the whole mass
  (the twin's line exactly; this building's own OSM height=28 is its parapet);
* dark metal hipped roofs with skylights - the primary aerial cue, and the
  whole aerial read for a building with no tower;
* glow set per the app's dusk system: Toy_mustard_Glow lit panes behind every
  arch (lit-lancet pattern, arches stay opaque Toy_glass by day) plus one thin
  Toy_white_Glow soffit strip under the colonnade entablature (floodlight cue).

MIRROR NOTE: this building is NORTH of the memorial court, so its SOUTH flank
is the formal court-facing one - the opposite hand to the Opera House.
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
OBB_LON, OBB_LAT = -122.4210354, 37.7795452
DEPTH = 83.06                            # E-W, Van Ness front to Franklin rear
# lon/lat of the build-frame origin (u=0, v=0  =  front face on the axis)
_ox, _oy = (-DEPTH / 2) * CT, (-DEPTH / 2) * ST
BLON = OBB_LON - _ox / KX
BLAT = OBB_LAT - _oy / KY

# ------------------------------------------------------------------- massing
# widths measured off the footprint width profile (REFERENCE.md 2.4)

W_FRONT = 45.50     # front pavilion / colonnade block (v +-22.75)
W_SHLDR = 52.20     # stepped shoulders behind it     (v +-26.10)
W_WING = 67.38      # wings, the full frontage        (v +-33.69)
W_MAIN = 51.40      # main block                      (v +-25.70)
W_REAR = 41.15      # rear block on Franklin St       (v +-20.58)

U_FRONT0, U_FRONT1 = 0.0, -3.10
U_SHLDR1 = -7.40
U_WING1 = -20.50
U_MAIN1 = -78.50
U_REAR1 = -DEPTH

# Height ladder - identical to the Opera House twin, deliberately.
BASE_TOP = 9.5      # rusticated granite basement course
COL_Z0, COL_Z1 = 10.7, 20.3              # colonnade shafts
ENT_Z0, ENT_Z1 = 21.0, 23.0              # architrave + frieze
COR_Z0, COR_Z1 = 23.0, 24.5              # projecting cornice
ATTIC_TOP = 27.0                         # front attic parapet (OSM height 28)
PARAPET = 25.80                          # wing / main-block parapet
HIP_F0, HIP_F1 = 25.6, 31.0              # front hip roof - THE SUMMIT
HIP_M0, HIP_M1 = 25.6, 29.4              # main-block hip roof (flat deck top)
REAR_TOP = 24.5                          # rear block shares the cornice line

CORNER_W = 5.80                          # front corner pavilions
LOGGIA = W_FRONT - 2 * CORNER_W          # 33.90 m of colonnade
BAYS = 7
BAY_P = LOGGIA / BAYS                    # 4.8429 m bay pitch

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


def hip_deck(name, u0, u1, v0, v1, z0, z1, inset_u, inset_v, mat):
    """A TRUNCATED hipped roof: eaves rectangle at z0, flat top deck inset on
    all four sides at z1. This is what the Veterans Building actually has - a
    metal hipped perimeter around a large flat deck (SGH) - and unlike a ridged
    hip it lets every slope share one pitch and gives the roofscape, which with
    no fly tower carries the whole aerial read, a surface to design on."""
    verts = [(u0, v0, z0), (u1, v0, z0), (u1, v1, z0), (u0, v1, z0),
             (u0 + inset_u, v0 + inset_v, z1), (u1 - inset_u, v0 + inset_v, z1),
             (u1 - inset_u, v1 - inset_v, z1), (u0 + inset_u, v1 - inset_v, z1)]
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

    # ---- rusticated granite basement course (proud 0.3 all round) ----
    for nm, u0, u1, w in (("base_front", U_FRONT0, U_FRONT1, W_FRONT),
                          ("base_shldr", U_FRONT1, U_SHLDR1, W_SHLDR),
                          ("base_wing", U_SHLDR1, U_WING1, W_WING),
                          ("base_main", U_WING1, U_MAIN1, W_MAIN),
                          ("base_rear", U_MAIN1, U_REAR1, W_REAR)):
        bevel(box(nm, (u0 + u1) / 2, 0, 0, BASE_TOP,
                  abs(u1 - u0) + 0.6, w + 0.6, stone))
    # two rusticated course lines across the front base
    for i, z in enumerate((3.4, 6.2)):
        bevel(box(f"base_course{i}", 0.36, 0, z, z + 0.5, 0.12, W_FRONT - 2.0,
                  stone), width=0.04, segments=1)

    # ---- front steps (three, colonnade width) ----
    for i, (du, z1) in enumerate(((3.4, 0.45), (2.3, 0.9), (1.2, 1.35))):
        bevel(box(f"steps{i}", 0.3 + du / 2, 0, 0, z1, du, 43.0, stone),
              width=0.08)

    # ---- upper front block ----
    # corner pavilions, full height at the front plane
    cpv = (W_FRONT - CORNER_W) / 2                      # +-19.85
    for s in (1, -1):
        tag = "n" if s > 0 else "s"
        bevel(box(f"pavilion_{tag}", U_FRONT1 / 2, s * cpv,
                  BASE_TOP, ATTIC_TOP, abs(U_FRONT1), CORNER_W, stone))
        # blind arched niche on the front face
        arch_slab(f"niche_{tag}", (0.31, s * cpv), E,
                  2.6, 11.5, 17.9, 0.08, 0.3, ink)
        # ground-floor end door
        box(f"pav_door_{tag}", 0.2, s * cpv, 1.35, 4.95, 0.4, 2.4, ink)
    # The solid core behind the loggia: the front block is a real 52.2 m wide
    # mass from the loggia back wall to the wings, not a screen wall. (The
    # first build left a void here that only the roof hid.)
    bevel(box("front_core", (-2.9 + U_SHLDR1) / 2, 0, BASE_TOP, COR_Z0,
              abs(U_SHLDR1) - 2.9, W_SHLDR, sand))
    # stepped shoulders flanking the corner pavilions - sand, not stone, so the
    # stone pavilions still read as distinct blocks rather than one slab corner
    for s in (1, -1):
        tag = "n" if s > 0 else "s"
        wsh = (W_SHLDR - W_FRONT) / 2                   # 3.35 m each side
        bevel(box(f"shoulder_{tag}", (U_FRONT1 + U_SHLDR1) / 2,
                  s * (W_FRONT / 2 + wsh / 2), ENT_Z0, ATTIC_TOP,
                  abs(U_SHLDR1 - U_FRONT1), wsh, sand),
              width=0.06, segments=1)
        # shoulder flank lit arch
        lit_arch(f"shldr_arch_{tag}", (-5.2, s * (W_SHLDR / 2)),
                 N if s > 0 else S, 2.5, 11.0, 17.6, 0.06)

    # loggia floor slab (the loggia is the 2.9 m recess in front of the core)
    box("loggia_floor", -1.45, 0, BASE_TOP, COL_Z0 - 0.9, 2.9, LOGGIA, stone)

    # 7 ground arches + 7 loggia arches on one bay grid
    for k in range(BAYS):
        vk = (k - (BAYS - 1) / 2) * BAY_P
        arch_slab(f"garch_rev{k}", (0.31, vk), E, 3.4, 1.35, 7.2, 0.04, 0.5, ink)
        lit_arch(f"garch{k}", (0.31, vk), E, 2.9, 1.35, 6.9, 0.10)
        lit_arch(f"larch{k}", (-2.9, vk), E, 3.1, COL_Z0, 17.9, 0.08)

    # colonnade: 8 pedestals, 16 shafts in 8 PAIRS, 8 cap blocks; balustrades
    for k in range(BAYS + 1):
        vk = -LOGGIA / 2 + k * BAY_P
        bevel(box(f"pedestal{k}", -1.05, vk, BASE_TOP, COL_Z0, 1.7, 3.5, trim),
              width=0.06, segments=1)
        for s in (1, -1):
            seg = 12
            verts = []
            for z in (COL_Z0, COL_Z1):
                for i in range(seg):
                    a = 2 * math.pi * i / seg
                    verts.append((-1.05 + 0.64 * math.cos(a),
                                  vk + s * 1.02 + 0.64 * math.sin(a), z))
            faces = [(i, seg + i, seg + (i + 1) % seg, (i + 1) % seg)
                     for i in range(seg)]
            faces.append(tuple(range(seg)))
            faces.append(tuple(range(2 * seg - 1, seg - 1, -1)))
            new_mesh(f"col{k}_{'n' if s > 0 else 's'}", verts, faces, [trim])
        bevel(box(f"colcap{k}", -1.05, vk, COL_Z1, ENT_Z0, 1.8, 3.5, trim),
              width=0.06, segments=1)
    for k in range(BAYS):
        vk = (k - (BAYS - 1) / 2) * BAY_P
        bevel(box(f"balustrade{k}", -0.7, vk, BASE_TOP, 10.6, 0.5,
                  BAY_P - 3.3, trim), width=0.05, segments=1)

    # floodlight cue: one thin warm-white strip under the entablature soffit
    box("soffit_glow", -0.55, 0, ENT_Z0 - 0.28, ENT_Z0 - 0.05, 0.12,
        LOGGIA - 1.0, material("Toy_white_Glow"))

    # entablature, cornice, attic across the front block
    bevel(box("entablature", -1.35, 0, ENT_Z0, COR_Z0, 3.3, W_FRONT, trim))
    bevel(box("cornice_front", -0.65, 0, COR_Z0, COR_Z1, 2.8, W_FRONT + 1.0,
              trim))
    bevel(box("attic_front", -1.7, 0, COR_Z1, ATTIC_TOP, 3.4, W_FRONT, sand))
    for k in range(BAYS):
        vk = (k - (BAYS - 1) / 2) * BAY_P
        box(f"attic_panel{k}", 0.03, vk, 25.1, 26.5, 0.1, 3.2, stone)
    # cornice + attic return around the shoulders
    bevel(box("cornice_shldr", (U_FRONT1 + U_SHLDR1) / 2, 0, COR_Z0, COR_Z1,
              abs(U_SHLDR1 - U_FRONT1), W_SHLDR + 1.0, trim))
    bevel(box("attic_shldr", -5.4, 0, COR_Z1, ATTIC_TOP, 4.0, W_SHLDR, sand),
          width=0.06, segments=1)

    # ---- wings (full frontage) ----
    wing_cv = (W_WING - (W_WING - W_SHLDR) / 2) / 2      # centre of each wing arm
    wing_w = (W_WING - W_SHLDR) / 2                      # 7.59 m outboard of shoulder
    for s in (1, -1):
        tag = "n" if s > 0 else "s"
        cv = s * (W_SHLDR / 2 + wing_w / 2)
        bevel(box(f"wing_{tag}", (U_SHLDR1 + U_WING1) / 2, cv,
                  BASE_TOP, COR_Z0, abs(U_WING1 - U_SHLDR1), wing_w, sand))
        # wing front face (facing Van Ness), two lit arches
        for i, vv in enumerate((28.2, 32.4)):
            lit_arch(f"wing_farch_{tag}{i}", (U_SHLDR1 + 0.31, s * vv), E,
                     2.5, 11.0, 17.6, 0.06)
        # wing outer flank, two lit arches
        for i, uu in enumerate((-11.0, -17.0)):
            lit_arch(f"wing_sarch_{tag}{i}", (uu, s * (W_WING / 2)),
                     N if s > 0 else S, 2.5, 11.0, 17.6, 0.06)
        # cornice return around the wing, and the parapet the roof sits on
        bevel(box(f"wing_cornice_{tag}", (U_SHLDR1 + U_WING1) / 2, cv,
                  COR_Z0, COR_Z1, abs(U_WING1 - U_SHLDR1) + 0.6, wing_w + 1.0,
                  trim))
        bevel(box(f"wing_parapet_{tag}", (U_SHLDR1 + U_WING1) / 2, cv,
                  COR_Z1, PARAPET, abs(U_WING1 - U_SHLDR1), wing_w, sand),
              width=0.06, segments=1)
        # curved reentrant quadrant against the main-block flank
        seg = 16
        verts = []
        for z in (BASE_TOP, PARAPET):
            for i in range(seg):
                a = 2 * math.pi * i / seg
                verts.append((U_WING1 - 1.2 + 3.0 * math.cos(a),
                              s * (W_MAIN / 2 + 1.9) + 3.0 * math.sin(a), z))
        faces = [(i, seg + i, seg + (i + 1) % seg, (i + 1) % seg)
                 for i in range(seg)]
        faces.append(tuple(range(seg)))
        faces.append(tuple(range(2 * seg - 1, seg - 1, -1)))
        new_mesh(f"quadrant_{tag}", verts, faces, [sand])

    # ---- main block (the long office / Herbst Theatre volume) ----
    bevel(box("main_block", (U_WING1 + U_MAIN1) / 2, 0, BASE_TOP, COR_Z0,
              abs(U_MAIN1 - U_WING1), W_MAIN, sand))
    bevel(box("main_frieze", (U_WING1 + U_MAIN1) / 2, 0, ENT_Z0, 22.2,
              abs(U_MAIN1 - U_WING1) - 0.5, W_MAIN + 0.4, trim),
          width=0.06, segments=1)
    bevel(box("main_cornice", (U_WING1 + U_MAIN1) / 2, 0, COR_Z0, COR_Z1,
              abs(U_MAIN1 - U_WING1), W_MAIN + 1.1, trim))
    bevel(box("main_parapet", (U_WING1 + U_MAIN1) / 2, 0, COR_Z1, PARAPET,
              abs(U_MAIN1 - U_WING1) - 0.6, W_MAIN - 0.6, sand),
          width=0.06, segments=1)
    for s in (1, -1):
        tag = "n" if s > 0 else "s"
        for k in range(8):
            uu = -25.5 - k * 6.6
            lit_arch(f"main_arch_{tag}{k}", (uu, s * W_MAIN / 2),
                     N if s > 0 else S, 2.6, 11.0, 17.6, 0.06)
    # McAllister St service canopy (north flank - the working side)
    bevel(box("canopy", -47.0, W_MAIN / 2 + 1.0, 8.3, 8.65, 22.0, 2.4, ink),
          width=0.05, segments=1)
    for k in range(3):
        box(f"service_door{k}", -40.0 - k * 7.0, W_MAIN / 2 - 0.05,
            1.35, 5.35, 2.2, 0.4, ink)

    # ---- rear block (Franklin St) ----
    bevel(box("rear_block", (U_MAIN1 + U_REAR1) / 2, 0, BASE_TOP, COR_Z0,
              abs(U_REAR1 - U_MAIN1), W_REAR, sand))
    bevel(box("rear_cornice", (U_MAIN1 + U_REAR1) / 2, 0, COR_Z0, REAR_TOP,
              abs(U_REAR1 - U_MAIN1), W_REAR + 1.1, trim))
    bevel(box("rear_parapet", (U_MAIN1 + U_REAR1) / 2, 0, REAR_TOP, PARAPET,
              abs(U_REAR1 - U_MAIN1) - 0.6, W_REAR - 0.6, sand),
          width=0.05, segments=1)
    # entrance + window grid on the Franklin face
    box("rear_door", U_REAR1 + 0.05, 0, 1.35, 6.35, 0.4, 4.2, ink)
    for r, z0 in ((0, 11.0), (1, 15.0), (2, 19.0)):
        for k in range(5):
            vv = (k - 2) * 7.4
            box(f"rear_win{r}_{k}", U_REAR1 + 0.05, vv, z0, z0 + 2.4,
                0.36, 1.6, glass)
    # rear-block flank windows, so the Franklin end is not a blank wall
    for s in (1, -1):
        for r, z0 in ((0, 11.0), (1, 15.0), (2, 19.0)):
            for k in range(2):
                box(f"rear_swin_{'n' if s > 0 else 's'}{r}_{k}",
                    -79.8 - k * 2.3, s * (W_REAR / 2 - 0.05), z0, z0 + 2.4,
                    1.5, 0.36, glass)

    # ---- roofscape: dark metal hipped roofs with skylights (SGH) ----
    # With no fly tower this IS the whole aerial read, so it is composed:
    # a tall hip over the front block (the 31 m summit), a lower hip over the
    # long main block, flat wing decks between them, all at one 40 deg pitch.
    # Every roof sits ONLY over footprint that exists - the first build let the
    # front hip hang over the void beside the narrower pavilion.
    # Insets chosen so the top collapses to a narrow ridge deck (2.1 x 38.4 m):
    # a near-ridged hip at ~36-38 deg, and HIP_F1 is then the exported max-z
    # exactly, so the loader's targetHeightM/measuredHeight lands at 1.0000.
    # No skylights here - they serve the main block's interiors, not the
    # entrance pavilion, and anything proud of this deck would break max-z.
    hip_deck("roof_front", U_WING1, -3.4, -W_SHLDR / 2, W_SHLDR / 2,
             HIP_F0 - 0.05, HIP_F1, 7.5, 6.9, roofd)

    # low wing roofs outboard of the front hip. These were flat decks buried
    # inside the parapet in the first build - invisible dead geometry that made
    # the wings read as pale sand terraces from above. Now they are real dark
    # metal roofs at the bottom of the hierarchy: wings 26.9 < main 29.4 <
    # front 31.0.
    for s in (1, -1):
        hip_deck(f"roof_wing_{'n' if s > 0 else 's'}",
                 U_WING1 + 0.4, U_SHLDR1 - 0.4,
                 s * (W_SHLDR / 2 + 0.3) if s > 0 else -(W_WING / 2 - 0.3),
                 s * (W_WING / 2 - 0.3) if s > 0 else -(W_SHLDR / 2 + 0.3),
                 25.55, 26.90, 1.5, 1.5, roofd)

    hip_deck("roof_main", U_MAIN1, U_WING1, -W_MAIN / 2 + 0.25,
             W_MAIN / 2 - 0.25, HIP_M0 - 0.05, HIP_M1, 4.6, 4.6, roofd)
    # court-facing skylights (south, the formal flank) plus a north pair
    for s, tag, n in ((-1, "s", 4), (1, "n", 2)):
        for i in range(n):
            box(f"skylight_m{tag}{i}", -30.0 - i * 11.0, s * 13.0,
                HIP_M1 - 0.02, HIP_M1 + 0.14, 6.0, 5.2, glass)
    # designed roof plant on the main deck, all kept below the 31 m summit
    for i, (uu, vv, w, d, ztop) in enumerate(
            ((-39.0, -4.0, 5.0, 4.0, 30.7), (-50.0, 6.0, 4.2, 3.6, 30.4))):
        bevel(box(f"plant{i}", uu, vv, HIP_M1, ztop, w, d, steel),
              width=0.08, segments=1)
    bevel(box("stair_ph", -62.0, -3.0, HIP_M1, 30.9, 3.4, 2.8, sand),
          width=0.08, segments=1)

    # rear flat deck behind its parapet
    box("rear_deck", (U_MAIN1 + U_REAR1) / 2, 0, PARAPET - 0.6, PARAPET - 0.2,
        abs(U_REAR1 - U_MAIN1) - 1.8, W_REAR - 1.8, roofd)


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

    blend = os.path.join(out, "herbst-theatre.blend")
    glb = os.path.join(out, "herbst-theatre.glb")
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
