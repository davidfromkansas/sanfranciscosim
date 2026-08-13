"""Bill Graham Civic Auditorium - deterministic miniature build for SF-SIM.

Run:  blender -b --python build_bill_graham_civic_auditorium.py [-- --out DIR]

Authored world-true: the long axis bears 80.69 deg cw from true north
(OSM way/25759141), the granite arcade facing NORTH onto Grove Street and
Civic Center Plaza. The build frame is (u, v): u+ runs ENE along Grove, v+ is
north; W() rotates into world axes (+X east, +Y north). The contract's "front
faces -Y" rule cannot hold for a north-facing building - real-world
orientation wins (AGENTS rule 5), recorded in REPORT.md.

Massing from the measured footprint and photographic elevations (REFERENCE.md):
* 127.95 x 78.64 m oriented bbox; the great hall fills it to a 23.0 m roof
  deck (2010 LiDAR median 22.99 m);
* a 20 m deep granite front range on Grove carrying THREE giant round-arched
  windows (11 m wide, 17 m pitch) between paired pilasters, over a rusticated
  base and a continuous marquee canopy, under a frieze of wreath medallions,
  a projecting cornice at 22.9-24.3 m and a 25.8 m parapet;
* two 24 m end pavilions (Larkin west, Polk east) rising past the parapet to
  29.8 m, each crowned by an oval cartouche;
* the identity form, invisible from the street and dominant from this app's
  camera: a DARK OCTAGONAL DOME 58.6 m flat-to-flat (measured off z19 imagery,
  rotated to the building axis), centred 7 m south of the building centre,
  rising to the 37.0 m target height (OSM height=37 m; LiDAR hgt_max 36.98 m);
* glow set per the app's dusk system: Toy_mustard_Glow panes behind the three
  arches (the real building floodlights them in colour) plus one
  Toy_white_Glow band along the marquee soffit. Flagpoles are deliberately
  omitted - they rise above the dome and would break the height contract.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ------------------------------------------------------------------ site data

HEADING = 80.69                          # long-axis bearing, deg cw from N
THETA = math.radians(90.0 - HEADING)     # math angle of u+ from +X (CCW)
CT, ST = math.cos(THETA), math.sin(THETA)

LAT0 = 37.77
KX = 111320.0 * math.cos(math.radians(LAT0))
KY = 110540.0

# Oriented-bbox centre of the footprint (WGS84) == build-frame origin.
BLON, BLAT = -122.4173272, 37.7780592

WH = 63.98                               # half length along u (127.95 m)
DH = 39.32                               # half depth along v (78.64 m)

# ------------------------------------------------------------------- massing

BASE_TOP = 5.0                           # rusticated granite base
HALL_TOP = 23.0                          # great-hall walls / roof deck
FRONT_V0 = 19.3                          # front range starts here
ARC_SILL, ARC_SPRING, ARC_CREST = 7.6, 14.8, 18.3
ARCH_W = 11.0
ARCH_U = [-17.0, 0.0, 17.0]
PIER_U = [-25.5, -8.5, 8.5, 25.5]
MARQ_Z0, MARQ_Z1 = 4.6, 5.4
MARQ_PROJ = 4.5
FRIEZE_Z0, FRIEZE_Z1 = 20.0, 22.9
COR_Z0, COR_Z1 = 22.9, 24.3
PARAPET_TOP = 25.8
PAV_U0, PAV_TOP = 40.0, 29.8             # end pavilions
PAV_V0 = 15.3

DOME_Z0 = 23.0
DOME_TOP = 37.0                          # OSM height / LiDAR hgt_max
DOME_R = 58.6 / (2.0 * math.cos(math.radians(22.5)))   # 31.71 m circumradius
DOME_V = -7.0                            # octagon centre, south of the middle

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_sand": "ece4d4",
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


ARCH_SEG = 12


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
    """The lit-window pattern shared with the Opera House: a dark reveal, an
    opaque Toy_glass pane, and a smaller Toy_mustard_Glow pane 6 cm proud so a
    dark frame surrounds the lit area at night."""
    span = top - sill
    arch_slab(f"{name}_rev", base_uv, ang, w + 1.5, sill - 0.4, top + 0.75,
              proud - 0.10, 0.9, material("Toy_ink"))
    arch_slab(name, base_uv, ang, w, sill, top, proud, 0.55,
              material("Toy_glass"))
    arch_slab(f"{name}_lit", base_uv, ang, w * 0.80, sill + span * 0.04,
              top - span * 0.07, proud + 0.06, 0.55,
              material("Toy_mustard_Glow"))


DISC_SEG = 12


def disc(name, base_uv, ang, rt, rz, cz, proud, depth, mat):
    """An elliptical plaque on a wall plane (wreath medallions, cartouches)."""
    pts = [(rt * math.cos(2 * math.pi * i / DISC_SEG),
            cz + rz * math.sin(2 * math.pi * i / DISC_SEG))
           for i in range(DISC_SEG)]
    n = (math.cos(ang), math.sin(ang))
    base = (base_uv[0] + n[0] * proud, base_uv[1] + n[1] * proud)
    return extrude_outline(name, pts, base, ang, depth + proud, mat)


# --- the octagonal dome ------------------------------------------------------

OCTA_A = [math.radians(22.5 + 45 * k) for k in range(8)]
OCTA_FLAT = math.cos(math.radians(22.5))


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
    sand = material("Toy_sand")
    white = material("Toy_white")
    glass = material("Toy_glass")
    ink = material("Toy_ink")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")

    E, N, S, R = 0.0, math.pi / 2, -math.pi / 2, math.pi

    # ---- the great hall: the whole footprint up to the roof deck ----
    bevel(box("hall", 0, 0, BASE_TOP, HALL_TOP, 2 * WH, 2 * DH, sand))
    bevel(box("hall_base", 0, 0, 0.0, BASE_TOP, 2 * WH + 0.8, 2 * DH + 0.8,
              stone))
    for i, z in enumerate((1.7, 3.3)):
        bevel(box(f"hall_course{i}", 0, 0, z, z + 0.35, 2 * WH + 1.05,
                  2 * DH + 1.05, stone), width=0.05, segments=1)
    bevel(box("hall_cornice", 0, 0, HALL_TOP - 1.0, HALL_TOP, 2 * WH + 1.0,
              2 * DH + 1.0, white), width=0.09, segments=1)
    # the deck reads BRIGHT in imagery - a white membrane roof, so the dark
    # octagon is the only dark shape up here
    box("deck", 0, 0, HALL_TOP - 0.05, HALL_TOP + 0.12,
        2 * WH - 2.4, 2 * DH - 2.4, trim)

    # ---- the Grove Street front range ----
    fv = (FRONT_V0 + DH) / 2
    fd = DH - FRONT_V0
    bevel(box("front_range", 0, fv, BASE_TOP, FRIEZE_Z0, 2 * WH, fd, trim))
    bevel(box("front_base", 0, fv, 0.0, BASE_TOP, 2 * WH + 0.85, fd, stone))
    bevel(box("frieze", 0, fv, FRIEZE_Z0, FRIEZE_Z1, 2 * WH + 0.35, fd, white),
          width=0.08, segments=1)
    bevel(box("cornice", 0, fv, COR_Z0, COR_Z1, 2 * WH + 2.2, fd + 1.1, white))
    bevel(box("parapet", 0, DH - 1.4, COR_Z1, PARAPET_TOP - 0.18, 2 * PAV_U0,
              2.8, trim), width=0.09, segments=1)
    bevel(box("parapet_cap", 0, DH - 1.4, PARAPET_TOP - 0.4, PARAPET_TOP,
              2 * PAV_U0 + 0.5, 3.2, white), width=0.06, segments=1)

    # ---- the three giant arches, their piers and the marquee ----
    for k, uu in enumerate(ARCH_U):
        lit_arch(f"arch{k}", (uu, DH), N, ARCH_W, ARC_SILL, ARC_CREST, 0.15)
    for k, uu in enumerate(PIER_U):
        # paired engaged columns on a pedestal, with a projecting cap block
        bevel(box(f"ped{k}", uu, DH + 0.55, BASE_TOP, ARC_SILL - 0.4, 5.8, 1.5,
                  white), width=0.07, segments=1)
        for s in (-1, 1):
            seg = 10
            verts = []
            for z in (ARC_SILL - 0.4, FRIEZE_Z0 - 1.5):
                for i in range(seg):
                    a = 2 * math.pi * i / seg
                    verts.append((uu + s * 1.45 + 0.78 * math.cos(a),
                                  DH + 0.55 + 0.78 * math.sin(a), z))
            faces = [(i, seg + i, seg + (i + 1) % seg, (i + 1) % seg)
                     for i in range(seg)]
            faces.append(tuple(range(seg)))
            faces.append(tuple(range(2 * seg - 1, seg - 1, -1)))
            new_mesh(f"col{k}_{'e' if s > 0 else 'w'}", verts, faces, [white])
        bevel(box(f"colcap{k}", uu, DH + 0.55, FRIEZE_Z0 - 1.5, FRIEZE_Z0,
                  5.8, 1.9, white), width=0.07, segments=1)
        # wreath medallion in the frieze over each pier
        disc(f"wreath{k}", (uu, DH), N, 1.35, 1.15,
             (FRIEZE_Z0 + FRIEZE_Z1) / 2, 0.22, 0.30, white)
    # link bays: pilaster pairs and punched windows between arcade and pavilion
    for s_ in (1, -1):
        tag = "e" if s_ > 0 else "w"
        for i, du in enumerate((30.0, 36.5)):
            bevel(box(f"link_pil_{tag}{i}", s_ * du, DH + 0.32, BASE_TOP,
                      FRIEZE_Z0, 1.5, 0.64, white), width=0.06, segments=1)
        for r, z0 in ((0, 7.8), (1, 13.6)):
            box(f"link_win_{tag}{r}", s_ * 33.2, DH + 0.26, z0, z0 + 3.4,
                2.4, 0.45, glass)
        disc(f"link_wreath_{tag}", (s_ * 33.2, DH), N, 1.35, 1.15,
             (FRIEZE_Z0 + FRIEZE_Z1) / 2, 0.22, 0.30, white)

    # entrance wall and doors behind the marquee
    # one clean dark recessed ground storey the full length of the arcade,
    # with the door band on it - the real thing reads as a single shadowed
    # slot under the marquee, not as a row of separate openings
    box("ent_recess", 0, DH - 0.55, 0.0, MARQ_Z0 - 0.2, 2 * PAV_U0 - 1.6,
        1.5, ink)
    for k in range(9):
        box(f"door{k}", -24.0 + k * 6.0, DH - 0.05, 0.35, 3.9, 4.2, 0.6,
            glass)
    # the marquee canopy: a strong horizontal slab with a dark fascia and the
    # bulb band the real building lights at night
    bevel(box("marquee", 0, DH + MARQ_PROJ / 2 - 0.4, MARQ_Z0, MARQ_Z1,
              2 * PAV_U0 - 1.0, MARQ_PROJ + 0.8, white), width=0.1,
          segments=2)
    box("marquee_fascia", 0, DH + MARQ_PROJ - 0.05, MARQ_Z0 - 0.85, MARQ_Z1,
        2 * PAV_U0 - 1.0, 0.55, ink)
    box("marquee_glow", 0, DH + MARQ_PROJ - 0.26, MARQ_Z0 - 0.62,
        MARQ_Z0 - 0.16, 2 * PAV_U0 - 3.2, 0.36, material("Toy_white_Glow"))

    # ---- the two end pavilions ----
    for s in (1, -1):
        tag = "e" if s > 0 else "w"
        cu = s * (PAV_U0 + WH) / 2
        su = WH - PAV_U0
        cv = (PAV_V0 + DH) / 2
        sv = DH - PAV_V0
        bevel(box(f"pav_{tag}", cu, cv, BASE_TOP, COR_Z0, su, sv, trim))
        bevel(box(f"pav_base_{tag}", cu, cv, 0.0, BASE_TOP, su + 0.85,
                  sv + 0.85, stone))
        bevel(box(f"pav_cornice_{tag}", cu, cv, COR_Z0, COR_Z1, su + 2.2,
                  sv + 2.2, white))
        bevel(box(f"pav_attic_{tag}", cu, cv, COR_Z1, PAV_TOP - 0.25,
                  su - 1.6, sv - 1.6, trim), width=0.1, segments=2)
        bevel(box(f"pav_attic_cap_{tag}", cu, cv, PAV_TOP - 0.55, PAV_TOP,
                  su - 0.9, sv - 0.9, white), width=0.07, segments=1)
        # the oval cartouche on the attic, front and outer flank
        disc(f"cartouche_{tag}", (cu, DH), N, 2.9, 2.2,
             (COR_Z1 + PAV_TOP) / 2, 0.30, 0.40, white)
        disc(f"cartouche_side_{tag}", (s * WH, cv), E if s > 0 else R,
             2.9, 2.2, (COR_Z1 + PAV_TOP) / 2, 0.30, 0.40, white)
        # pedestal blocks where the real parapet carries sculpture groups
        for i, du in enumerate((-0.5, 0.5)):
            bevel(box(f"pav_ped_{tag}{i}", cu + du * (su - 3.0), DH - 1.4,
                      PAV_TOP - 0.5, PAV_TOP + 1.5, 2.6, 2.6, white),
                  width=0.08, segments=1)
        # pavilion fenestration: three rows, the middle one pedimented
        for r, z0 in ((0, 7.4), (1, 12.4), (2, 17.4)):
            for k in range(3):
                uu = cu + (k - 1) * 7.0
                box(f"pav_win_{tag}{r}_{k}", uu, DH + 0.26, z0, z0 + 3.0,
                    2.2, 0.45, glass)
                if r == 1:
                    bevel(box(f"pav_ped_head_{tag}{k}", uu, DH + 0.5,
                              z0 + 3.0, z0 + 3.6, 3.2, 0.7, white),
                          width=0.06, segments=1)
            for k in range(4):
                vv = cv + (k - 1.5) * 7.6
                box(f"pav_swin_{tag}{r}_{k}", s * (WH + 0.26), vv, z0,
                    z0 + 3.0, 0.45, 2.2, glass)
        # ground-floor arched openings under the pavilion
        for k in range(3):
            uu = cu + (k - 1) * 7.0
            box(f"pav_gdoor_{tag}{k}", uu, DH + 0.26, 0.4, 3.8, 2.6, 0.5, ink)
        for k in range(3):
            vv = cv + (k - 1) * 7.6
            box(f"pav_sdoor_{tag}{k}", s * (WH + 0.26), vv, 0.4, 3.8,
                0.5, 2.6, ink)

    # ---- the flanks and the rear of the great hall ----
    for s in (1, -1):
        tag = "e" if s > 0 else "w"
        for r, z0 in ((0, 8.0), (1, 14.0)):
            for k in range(6):
                vv = -33.0 + k * 6.6
                box(f"hall_swin_{tag}{r}_{k}", s * (WH + 0.24), vv, z0,
                    z0 + 2.6, 0.42, 1.8, glass)
        bevel(box(f"hall_pil_{tag}", s * (WH + 0.30), DOME_V - 4.0, BASE_TOP,
                  HALL_TOP - 1.0, 0.6, 44.0, sand), width=0.06, segments=1)
    for r, z0 in ((0, 8.0), (1, 14.0)):
        for k in range(9):
            uu = -48.0 + k * 12.0
            box(f"hall_rwin{r}_{k}", uu, -DH - 0.24, z0, z0 + 2.6,
                1.8, 0.42, glass)
    box("stage_door", -18.0, -DH - 0.24, 0.0, 6.5, 9.0, 0.5, ink)
    box("rear_dock", 20.0, -DH - 0.24, 0.0, 5.2, 11.0, 0.5, ink)

    # ---- THE DOME: the identity form, only legible from above ----
    bevel(octa_frustum("dome_ring", 0, DOME_V, DOME_R + 0.7, DOME_R + 0.7,
                       DOME_Z0 - 0.9, DOME_Z0 + 0.6, white),
          width=0.1, segments=1)
    octa_frustum("dome_a", 0, DOME_V, DOME_R, 27.5, DOME_Z0 + 0.4, 27.5, roofd)
    octa_frustum("dome_b", 0, DOME_V, 27.5, 20.0, 27.5, 31.5, roofd)
    octa_frustum("dome_c", 0, DOME_V, 20.0, 11.0, 31.5, 34.6, roofd)
    octa_frustum("dome_d", 0, DOME_V, 11.0, 4.6, 34.6, 36.3, roofd)
    bevel(octa_frustum("lantern", 0, DOME_V, 4.6, 4.6, 36.25, 36.75, steel),
          width=0.06, segments=1)
    octa_frustum("lantern_cap", 0, DOME_V, 4.9, 1.9, 36.75, DOME_TOP, roofd)

    # ---- roof plant, on the bright deck the imagery shows ----
    # two tidy clusters on the wide deck outside the octagon's corners (s.10:
    # organised clusters, never scattered props), one per end
    for s_ in (1, -1):
        tag = "e" if s_ > 0 else "w"
        for i, (du, dv, su, sv, hh) in enumerate((
                (46.0, -6.0, 10.0, 8.0, 2.9),
                (46.0, -17.0, 8.0, 6.0, 2.2),
                (56.0, -10.5, 5.0, 9.0, 1.8))):
            bevel(box(f"plant_{tag}{i}", s_ * du, dv, HALL_TOP,
                      HALL_TOP + hh, su, sv, steel), width=0.1, segments=1)
        bevel(box(f"stair_ph_{tag}", s_ * 36.0, 12.0, HALL_TOP,
                  HALL_TOP + 3.6, 6.0, 5.0, trim), width=0.1, segments=1)
    # pavilion roof decks, so the two tallest surfaces are not blank (s.10)
    for s_ in (1, -1):
        tag = "e" if s_ > 0 else "w"
        cu = s_ * (PAV_U0 + WH) / 2
        cv = (PAV_V0 + DH) / 2
        box(f"pav_deck_{tag}", cu, cv, COR_Z1, COR_Z1 + 0.15,
            WH - PAV_U0 - 1.2, DH - PAV_V0 - 1.2, stone)
        for i, dv in enumerate((-6.5, 6.5)):
            bevel(box(f"pav_plant_{tag}{i}", cu + 7.5, cv + dv, COR_Z1,
                      COR_Z1 + 1.8, 4.0, 3.4, steel), width=0.08,
                  segments=1)


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

    blend = os.path.join(out, "bill-graham-civic-auditorium.blend")
    glb = os.path.join(out, "bill-graham-civic-auditorium.glb")
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
