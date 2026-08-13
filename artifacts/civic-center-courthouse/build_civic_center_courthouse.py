"""San Francisco Civic Center Courthouse - deterministic miniature build for SF-SIM.

Run:  blender -b --python build_civic_center_courthouse.py [-- --out DIR]

Authored world-true: the long axis bears 81.22 deg cw from true north
(OSM way/108389188), the ceremonial front facing SOUTH onto McAllister Street.
The build frame is (u, v): u+ runs ENE along McAllister, v+ is north; W()
rotates into world axes (+X east, +Y north).

Massing from the measured footprint and the architect's own McAllister Street
elevation (see REFERENCE.md):
* 83.46 x 36.98 m oriented bbox with a 6.1 m chamfer on the SE (McAllister x
  Polk) corner - the chamfer is carried explicitly by the OSM polygon;
* two-storey rusticated granite base to 7.6 m, then a giant order of five
  round-arched windows on McAllister and two on Polk, an attic band of small
  square windows, a projecting cornice at 20.7-21.7 m and a parapet at 25.0 m
  (OSM height=25; 2010 LiDAR median 24.67 m);
* the north (Golden Gate Ave) and west elevations drop the arcade for four
  flat ribbon bands - the building's two-faced parti;
* the SE corner carries the identity: recessed glazed entrance, a projecting
  glazed bay, then an octagonal drum of round oculi under a shallow dome whose
  crest is the 29.6 m target height (2010 LiDAR hgt_max);
* glow set per the app's dusk system: Toy_mustard_Glow panes behind every arch
  and inside all eight oculi (the lantern is the hero), plus one thin
  Toy_white_Glow soffit strip over the corner entrance.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ------------------------------------------------------------------ site data

HEADING = 81.22                          # long-axis bearing, deg cw from N
THETA = math.radians(90.0 - HEADING)     # math angle of u+ from +X (CCW)
CT, ST = math.cos(THETA), math.sin(THETA)

LAT0 = 37.77
KX = 111320.0 * math.cos(math.radians(LAT0))
KY = 110540.0

# Oriented-bbox centre of the footprint (WGS84) == build-frame origin.
BLON, BLAT = -122.4192590, 37.7804897

WH = 41.73                               # half length along u (83.46 m)
DH = 18.49                               # half depth along v (36.98 m)
CHAM = 4.31                              # chamfer cut on each face at the SE

# ------------------------------------------------------------------- massing

BASE_TOP = 7.6       # rusticated two-storey base
STR_Z0, STR_Z1 = 7.6, 8.0                # string course
WALL_TOP = 19.2      # main granite wall
ARC_SILL, ARC_SPRING, ARC_CREST = 8.6, 15.2, 17.9
ATT_Z0, ATT_Z1 = 19.3, 20.7              # attic band of small square windows
COR_Z0, COR_Z1 = 20.7, 21.7              # projecting cornice
PARAPET_TOP = 25.0                       # OSM height / LiDAR median
DECK_Z0, DECK_Z1 = 24.0, 24.2            # roof deck

# The corner attic deliberately clears the 25.0 m parapet so the drum starts
# in open air - buried behind the parapet the lantern stopped reading at all.
CORNER_ATT_TOP = 25.6                    # corner attic block over the cornice
DRUM_Z0, DRUM_Z1 = 25.6, 27.8            # octagonal drum with the oculi
DOME_TOP = 29.6                          # LiDAR hgt_max - the building summit
# The drum measures ~10.6 m across on z19 imagery; exaggerated ~15 % (style
# bible s.9) so the lantern still reads from the app's aerial camera.
DRUM_R = 5.8

# corner-lantern centre, on the 45 deg diagonal in from the SE corner
LU, LV = WH - 7.4, -DH + 7.4

ARCH_W = 6.0
ARCH_PITCH = 9.5
S_ARCH_U = [-8.75 + (k - 2) * ARCH_PITCH for k in range(5)]   # McAllister
E_ARCH_V = [-2.0, 8.0]                                        # Polk

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_white": "f7f4ec",
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


# --- the chamfered footprint, and prisms built on offsets of it ---------------

FOOT = [
    (-WH, -DH),          # SW
    (WH - CHAM, -DH),    # start of the SE chamfer, on McAllister
    (WH, -DH + CHAM),    # end of the SE chamfer, on Polk
    (WH, DH),            # NE
    (-WH, DH),           # NW
]


def offset_poly(poly, d):
    """Offset a convex CCW polygon outward by d (negative = inward)."""
    n = len(poly)
    lines = []
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        ex, ey = x1 - x0, y1 - y0
        L = math.hypot(ex, ey)
        nx, ny = ey / L, -ex / L          # outward normal for CCW winding
        lines.append((x0 + nx * d, y0 + ny * d, ex, ey))
    out = []
    for i in range(n):
        px, py, ex, ey = lines[i - 1]
        qx, qy, fx, fy = lines[i]
        det = ex * (-fy) - ey * (-fx)
        t = ((qx - px) * (-fy) - (qy - py) * (-fx)) / det
        out.append((px + ex * t, py + ey * t))
    return out


def prism(name, poly, z0, z1, mat):
    k = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces = [tuple(range(k - 1, -1, -1)), tuple(range(k, 2 * k))]
    for i in range(k):
        j = (i + 1) % k
        faces.append((i, j, k + j, k + i))
    return new_mesh(name, verts, faces, [mat])


# --- openings ---------------------------------------------------------------


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


def lit_arch(name, base_uv, ang, w, sill, top, proud):
    """The lit-window pattern (shared with the Opera House): a dark reveal, an
    opaque Toy_glass pane, and a smaller Toy_mustard_Glow pane 5 cm proud of
    it so a dark frame surrounds the lit area at night."""
    span = top - sill
    arch_slab(f"{name}_rev", base_uv, ang, w + 0.7, sill - 0.25, top + 0.35,
              proud - 0.06, 0.55, material("Toy_ink"))
    arch_slab(name, base_uv, ang, w, sill, top, proud, 0.35,
              material("Toy_glass"))
    arch_slab(f"{name}_lit", base_uv, ang, w * 0.76, sill + span * 0.05,
              top - span * 0.09, proud + 0.05, 0.35,
              material("Toy_mustard_Glow"))


DISC_SEG = 12


def disc(name, base_uv, ang, r, cz, proud, depth, mat):
    """A circular pane on a wall plane (the drum's oculi)."""
    pts = [(r * math.cos(2 * math.pi * i / DISC_SEG),
            cz + r * math.sin(2 * math.pi * i / DISC_SEG))
           for i in range(DISC_SEG)]
    n = (math.cos(ang), math.sin(ang))
    base = (base_uv[0] + n[0] * proud, base_uv[1] + n[1] * proud)
    return extrude_outline(name, pts, base, ang, depth + proud, mat)


# --- the octagonal lantern ---------------------------------------------------

OCTA_A = [math.radians(22.5 + 45 * k) for k in range(8)]   # flats face k*45 deg
OCTA_FLAT = math.cos(math.radians(22.5))                   # flat/circum ratio


def octa_frustum(name, cu, cv, r0, r1, z0, z1, mat):
    verts = []
    for r, z in ((r0, z0), (r1, z1)):
        for a in OCTA_A:
            verts.append((cu + r * math.cos(a), cv + r * math.sin(a), z))
    faces = [tuple(range(7, -1, -1)), tuple(range(8, 16))]
    for i in range(8):
        j = (i + 1) % 8
        faces.append((i, j, 8 + j, 8 + i))
    return new_mesh(name, verts, faces, [mat])


# ------------------------------------------------------------------ the build


def build():
    stone = material("Toy_stone")
    trim = material("Toy_trim")
    white = material("Toy_white")
    glass = material("Toy_glass")
    ink = material("Toy_ink")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")

    E, N, S = 0.0, math.pi / 2, -math.pi / 2       # face outward angles
    SE = math.radians(-45.0)

    # ---- the block, layer by layer ----
    bevel(prism("base", offset_poly(FOOT, 0.35), 0.0, BASE_TOP, stone))
    for i, z in enumerate((2.6, 5.1)):
        bevel(prism(f"base_course{i}", offset_poly(FOOT, 0.48), z, z + 0.35,
                    stone), width=0.05, segments=1)
    bevel(prism("string", offset_poly(FOOT, 0.55), STR_Z0, STR_Z1, white),
          width=0.07, segments=1)
    bevel(prism("wall", FOOT, STR_Z1, WALL_TOP, trim))
    bevel(prism("attic", offset_poly(FOOT, 0.06), ATT_Z0, ATT_Z1, trim),
          width=0.07, segments=1)
    bevel(prism("cornice", offset_poly(FOOT, 0.9), COR_Z0, COR_Z1, white))
    bevel(prism("parapet", offset_poly(FOOT, -0.15), COR_Z1,
                PARAPET_TOP - 0.18, trim), width=0.08, segments=1)
    bevel(prism("parapet_cap", offset_poly(FOOT, 0.05), PARAPET_TOP - 0.45,
                PARAPET_TOP, white), width=0.06, segments=1)
    prism("deck", offset_poly(FOOT, -0.7), DECK_Z0, DECK_Z1, stone)

    # ---- base storeys: punched square windows, south and east ----
    for k in range(10):
        uu = -36.5 + k * 7.6
        if uu > WH - CHAM - 3.4:
            continue
        for r, z0 in ((0, 1.8), (1, 4.8)):
            box(f"base_swin{r}_{k}", uu, -DH - 0.34, z0, z0 + 1.6,
                3.0, 0.42, glass)
    for k in range(4):
        vv = -9.5 + k * 7.2
        for r, z0 in ((0, 1.8), (1, 4.8)):
            box(f"base_ewin{r}_{k}", WH + 0.34, vv, z0, z0 + 1.6,
                0.42, 3.0, glass)

    # ---- the giant arcade: five on McAllister, two on Polk ----
    for k, uu in enumerate(S_ARCH_U):
        lit_arch(f"s_arch{k}", (uu, -DH), S, ARCH_W, ARC_SILL, ARC_CREST, 0.12)
        # the narrow slot window that splits each pier
        if k:
            box(f"s_slot{k}", (uu + S_ARCH_U[k - 1]) / 2, -DH - 0.3,
                ARC_SILL + 0.6, ARC_CREST - 1.4, 0.9, 0.4, glass)
    for k in range(4):
        uu = 17.5 + k * 4.4
        box(f"s_tall{k}", uu, -DH - 0.3, ARC_SILL + 0.4, ARC_CREST - 1.2,
            1.5, 0.4, glass)
    for k, vv in enumerate(E_ARCH_V):
        lit_arch(f"e_arch{k}", (WH, vv), E, ARCH_W, ARC_SILL, ARC_CREST, 0.12)

    # ---- attic band: small square windows over the classical frontage ----
    for k in range(11):
        uu = -36.0 + k * 6.2
        box(f"att_swin{k}", uu, -DH - 0.28, ATT_Z0 + 0.22, ATT_Z1 - 0.22,
            2.3, 0.36, glass)
    for k in range(4):
        vv = -2.0 + k * 5.4
        box(f"att_ewin{k}", WH + 0.28, vv, ATT_Z0 + 0.22, ATT_Z1 - 0.22,
            0.36, 2.3, glass)

    # ---- the contemporary faces: four flat ribbon bands, north and west ----
    for r, z0 in enumerate((8.8, 11.6, 14.4, 17.2)):
        box(f"n_band{r}", -1.0, DH + 0.26, z0, z0 + 1.9, 76.0, 0.42, glass)
        box(f"n_sill{r}", -1.0, DH + 0.42, z0 - 0.35, z0, 76.6, 0.5, trim)
        box(f"w_band{r}", -WH - 0.26, 0.0, z0, z0 + 1.9, 0.42, 31.0, glass)
        box(f"w_sill{r}", -WH - 0.42, 0.0, z0 - 0.35, z0, 0.5, 31.6, trim)
    for k in range(9):
        box(f"n_mull{k}", -37.0 + k * 9.0, DH + 0.3, 8.4, WALL_TOP - 0.2,
            0.55, 0.5, trim)
    # service door and loading bay on Golden Gate Ave
    box("n_door", -12.0, DH + 0.28, 0.0, 4.4, 5.6, 0.42, ink)
    box("n_dock", 14.0, DH + 0.28, 0.0, 4.0, 7.0, 0.42, ink)

    # ---- the SE corner: entrance, glazed bay, drum, dome ----
    cham_uv = (WH - CHAM / 2, -DH + CHAM / 2)
    # ground: recessed dark entrance with a glazed door band
    extrude_outline("ent_rec", [(-4.7, 0.0), (4.7, 0.0), (4.7, 7.0),
                                (-4.7, 7.0)], cham_uv, SE, 0.55, ink)
    extrude_outline("ent_glass", [(-3.9, 0.5), (3.9, 0.5), (3.9, 5.6),
                                  (-3.9, 5.6)], cham_uv, SE, 0.28, glass)
    # entrance canopy + its night light strip
    extrude_outline("ent_canopy", [(-5.4, 6.5), (5.4, 6.5), (5.4, 6.95),
                                   (-5.4, 6.95)],
                    (cham_uv[0] + 1.5 * math.cos(SE),
                     cham_uv[1] + 1.5 * math.sin(SE)), SE, 2.1, white)
    extrude_outline("ent_soffit_glow", [(-4.9, 6.28), (4.9, 6.28),
                                        (4.9, 6.48), (-4.9, 6.48)],
                    (cham_uv[0] + 1.3 * math.cos(SE),
                     cham_uv[1] + 1.3 * math.sin(SE)), SE, 1.6,
                    material("Toy_white_Glow"))
    # the projecting glazed bay over the entrance
    extrude_outline("bay_frame", [(-4.3, ARC_SILL - 0.5), (4.3, ARC_SILL - 0.5),
                                  (4.3, ARC_CREST + 0.6),
                                  (-4.3, ARC_CREST + 0.6)],
                    cham_uv, SE, 0.9, trim)
    bay_base = (cham_uv[0] + 1.0 * math.cos(SE), cham_uv[1] + 1.0 * math.sin(SE))
    for i in range(3):
        z0 = ARC_SILL + i * 3.15
        extrude_outline(f"bay_glass{i}", [(-3.4, z0), (3.4, z0),
                                          (3.4, z0 + 2.65), (-3.4, z0 + 2.65)],
                        bay_base, SE, 0.5, glass)
    for i, tt in enumerate((-1.15, 1.15)):
        extrude_outline(f"bay_mull{i}", [(tt - 0.22, ARC_SILL),
                                         (tt + 0.22, ARC_SILL),
                                         (tt + 0.22, ARC_CREST),
                                         (tt - 0.22, ARC_CREST)],
                        (bay_base[0] + 0.18 * math.cos(SE),
                         bay_base[1] + 0.18 * math.sin(SE)), SE, 0.6, trim)

    # corner attic block above the cornice, chamfered like the plan
    catt = [(LU - 7.4, LV - 7.4), (LU + 3.1, LV - 7.4), (LU + 7.4, LV - 3.1),
            (LU + 7.4, LV + 7.4), (LU - 7.4, LV + 7.4)]
    bevel(prism("corner_body", catt, COR_Z0, COR_Z1 + 0.0, trim),
          width=0.09, segments=1)
    bevel(prism("corner_attic", catt, COR_Z1, CORNER_ATT_TOP - 0.16, trim))
    bevel(prism("corner_att_cap", offset_poly(catt, 0.35),
                CORNER_ATT_TOP - 0.4, CORNER_ATT_TOP, white),
          width=0.06, segments=1)

    # the octagonal drum and its eight oculi
    bevel(octa_frustum("drum", LU, LV, DRUM_R, DRUM_R, DRUM_Z0, DRUM_Z1, trim),
          width=0.09, segments=2)
    ocz = (DRUM_Z0 + DRUM_Z1) / 2 + 0.15
    for k, a in enumerate(range(0, 360, 45)):
        ang = math.radians(a)
        f = DRUM_R * OCTA_FLAT
        base = (LU + f * math.cos(ang), LV + f * math.sin(ang))
        disc(f"oculus{k}", base, ang, 0.86, ocz, 0.10, 0.45, ink)
        disc(f"oculus{k}_g", base, ang, 0.66, ocz, 0.16, 0.45,
             material("Toy_mustard_Glow"))
    # the shallow dome
    bevel(octa_frustum("dome_lip", LU, LV, DRUM_R + 0.5, DRUM_R + 0.5,
                       DRUM_Z1, DRUM_Z1 + 0.4, white), width=0.07, segments=1)
    octa_frustum("dome_a", LU, LV, DRUM_R + 0.35, 4.0, DRUM_Z1 + 0.4, 28.8,
                 white)
    octa_frustum("dome_b", LU, LV, 4.0, 1.15, 28.8, DOME_TOP - 0.25, white)
    octa_frustum("dome_finial", LU, LV, 1.15, 0.4, DOME_TOP - 0.25,
                 DOME_TOP, white)

    # ---- roofscape: parapet, louvered penthouse, plant, stair ----
    bevel(box("penthouse", -11.0, 2.0, DECK_Z1, 27.55, 27.0, 8.0, trim))
    box("ph_deck", -11.0, 2.0, 27.55, 27.75, 26.0, 7.0, roofd)
    for s in (1, -1):
        for i in range(3):
            box(f"ph_louv_{'n' if s > 0 else 's'}{i}", -11.0,
                s * (2.0 + 4.05), DECK_Z1 + 0.9 + i * 1.0,
                DECK_Z1 + 1.5 + i * 1.0, 25.0, 0.22, steel)
    bevel(box("hvac_a", -27.5, -7.0, DECK_Z1, 26.2, 7.0, 5.5, steel),
          width=0.1, segments=1)
    bevel(box("hvac_b", 12.5, -6.5, DECK_Z1, 26.0, 6.0, 5.0, steel),
          width=0.1, segments=1)
    bevel(box("stair_ph", 6.0, 11.5, DECK_Z1, 26.8, 4.6, 4.0, trim),
          width=0.1, segments=1)
    for i in range(3):
        bevel(box(f"vent{i}", -34.0 + i * 3.8, 10.0, DECK_Z1, 25.2,
                  2.2, 2.2, steel), width=0.08, segments=1)
    # a run of court-lit skylights over the sixth-floor corridor, and a low
    # duct spine linking the plant - the roof is a facade here (style s.10)
    for i in range(5):
        box(f"skylight{i}", 20.0 + i * 4.0, 6.0, DECK_Z1, DECK_Z1 + 0.5,
            3.0, 5.0, glass)
    box("duct_spine", 1.0, -6.5, DECK_Z1, DECK_Z1 + 0.9, 22.0, 1.4, steel)
    box("duct_run", -27.0, 1.5, DECK_Z1, DECK_Z1 + 0.9, 1.4, 12.0, steel)


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

    blend = os.path.join(out, "civic-center-courthouse.blend")
    glb = os.path.join(out, "civic-center-courthouse.glb")
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
