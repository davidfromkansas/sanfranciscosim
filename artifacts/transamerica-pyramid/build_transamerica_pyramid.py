"""Deterministic Blender build of the SF-SIM miniature Transamerica Pyramid.

    blender -b --python build_transamerica_pyramid.py -- [--out DIR]

Writes transamerica-pyramid.blend and transamerica-pyramid.glb next to this
file (or into --out). Geometry is authored directly in world space in metres,
Z up, +X east, +Y north, origin at the base centre, min Z = 0, so nothing has
to be transformed after the fact.

Design (see REFERENCE.md for the source behind every number):

* ONE straight-sided four-sided pyramid from grade to the 260 m tip. The
  photogrammetric trace in REFERENCE.md s.3 shows the spire continues the
  pyramid's silhouette rather than sitting on a blunt frustum, so the half
  width is simply 26.65 * (1 - z/260) everywhere;
* a 54.3 m square plan yawed -9.1 degrees onto the Financial District grid,
  measured from the OSM footprint;
* the facade's grain is vertical: thirteen recessed window channels per face,
  each terminating where the taper eats it, leaving the real building's wide
  blank corner bands and its triangular field of windows;
* the two triangular buttress wings on the east and west faces, flush at the
  29th floor (z 120) and projecting ~6.8 m by their flat caps at z 186;
* the chevron truss colonnade at the ground: raked chunky legs lying in the
  plane of the sloping facade over a recessed glass lobby;
* a crown designed for the app's downward camera - louvre band, parapet, metal
  hip roof, plant and the window-washing rig - and the metal spire whose glazed
  "crown jewel" and red aviation light are the only _Glow surfaces.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

H_TIP = 260.0  # architectural height, tip of the spire
H_CROWN = 195.0  # top of the occupied pyramid / parapet level
H_MECH = 190.6  # dark mechanical louvre band starts here
H_LEGS = 14.0  # apexes of the ground chevron truss
H_BAND = 18.5  # bottom of the office facade
H_LOBBY = 11.5  # recessed lobby box behind the legs

A_BASE = 26.65  # half width across the flats where the shell meets grade
A_FOOT = 27.15  # measured OSM half width: the splayed truss feet reach this
YAW = math.radians(-9.1)  # faces bear 80.9 / 170.9 / 260.9 / 351.0 deg

CHAMFER = 0.7  # corner chamfer of the shell, per side
CORNER_BAND = 2.4  # blank precast band before the first window channel
WIN_COLS = 15  # window channels per face (abstracting ~22 real columns)
WIN_PITCH = 2.9
WIN_WIDE = 1.8
WIN_DEEP = 0.45

WING_Z0 = 120.0  # 29th floor
WING_Z1 = 186.0  # just below the 49th
WING_HALF = 5.0  # half width of a wing across the face

LEG_BAYS = 5  # chevron apexes per face
LEG_W = 2.3  # face width of a truss member
LEG_D = 1.7  # how far it stands proud of the shell line

# The spire's silhouette is twice as steep as the pyramid's: measured on the
# 2023 elevation its half width at the crown is 51% of the shell's (REFERENCE
# s.3), and both lines still converge on the 260 m tip.
SPIRE_A0 = 3.5
JEWEL_Z = 250.5  # glazed room near the tip

# Project palette from .agents/skills/sf-asset-check (hex, sRGB). Materials are
# authored with the linear equivalents, which is what the shipped kit GLBs hold.
PALETTE_HEX = {
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_steel": "9aa0a6",
    "Toy_stone": "d9d2c2",
    "Toy_roofd": "45454a",
    "Toy_white_Glow": "f7f4ec",
    "Toy_red_Glow": "c4453c",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- plan shapes


def rot2(p, ang):
    c, s = math.cos(ang), math.sin(ang)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def half_width(z):
    """Distance from the axis to a face, at height z. One straight taper."""
    return A_BASE * (1.0 - z / H_TIP)


# Faces in build order, indexed by their outward direction before the yaw is
# applied: 0 = east (+X, Montgomery), 1 = north, 2 = west, 3 = south.
FACE_ANGLE = [0.0, math.pi / 2, math.pi, -math.pi / 2]
FACE_NAME = ["east", "north", "west", "south"]


def face_point(face, u, z, out=0.0):
    """Point on face `face`, u metres along it from its centre, at height z."""
    a = half_width(z) + out
    p = rot2((a, u), FACE_ANGLE[face])
    return rot2(p, YAW)


def face_normal(face):
    return rot2(rot2((1.0, 0.0), FACE_ANGLE[face]), YAW)


def face_tangent(face):
    return rot2(rot2((0.0, 1.0), FACE_ANGLE[face]), YAW)


def outline(z, out=0.0):
    """Chamfered square plan at height z, yawed onto the street grid."""
    a = half_width(z) + out
    c = min(CHAMFER, a * 0.4)
    pts = []
    for q in range(4):
        pts.append(rot2((a, -(a - c)), FACE_ANGLE[q]))
        pts.append(rot2((a, a - c), FACE_ANGLE[q]))
    return [rot2(p, YAW) for p in pts]


# -------------------------------------------------------------- mesh helpers


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


def new_mesh(name, verts, faces, materials, face_mats=None, recalc=True):
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
    if recalc:
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()
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


def loft(name, rings, materials, row_mats=None, cap_top=False, cap_bottom=False):
    """Loft equal-length closed plan loops (list of (z, points)) into a tube."""
    n = len(rings[0][1])
    verts = []
    for z, loop in rings:
        verts.extend([(x, y, z) for x, y in loop])
    faces, face_mats = [], []
    for r in range(len(rings) - 1):
        for i in range(n):
            j = (i + 1) % n
            faces.append((r * n + i, r * n + j, (r + 1) * n + j, (r + 1) * n + i))
            face_mats.append(row_mats[r] if row_mats else 0)
    if cap_bottom:
        faces.append(tuple(range(n - 1, -1, -1)))
        face_mats.append(0)
    if cap_top:
        off = (len(rings) - 1) * n
        faces.append(tuple(range(off, off + n)))
        face_mats.append(0)
    return new_mesh(name, verts, faces, materials, face_mats)


def ring_band(name, z0, z1, inner_off, outer_off, mat):
    """A closed band standing proud of the shell: outer wall plus lip faces."""
    lo_in = outline(z0, inner_off)
    lo_out = outline(z0, outer_off)
    hi_out = outline(z1, outer_off)
    hi_in = outline(z1, inner_off)
    n = len(lo_in)
    verts = []
    for loop, z in ((lo_in, z0), (lo_out, z0), (hi_out, z1), (hi_in, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * n, ((k + 1) % 4) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=YAW):
    hx, hy = sx / 2, sy / 2
    corners = [rot2(c, yaw) for c in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy))]
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
    return new_mesh(name, verts, faces, [mat])


def quad_prism(name, quad, thick, nrm, mat):
    """Extrude a planar quad (4 world points) by `thick` along `nrm` (2D)."""
    d = (nrm[0] * thick, nrm[1] * thick, 0.0)
    verts = [tuple(p) for p in quad] + [
        (p[0] + d[0], p[1] + d[1], p[2]) for p in quad
    ]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


# ---------------------------------------------------------------- the facade


def window_columns(face):
    """(u, z_top) for every window channel on a face, outermost cut by taper."""
    cols = []
    for i in range(WIN_COLS):
        u = (i - (WIN_COLS - 1) / 2.0) * WIN_PITCH
        # the channel dies where the blank corner band would swallow it
        need = abs(u) + WIN_WIDE / 2.0 + CORNER_BAND
        z_top = H_TIP * (1.0 - need / A_BASE)
        cols.append((u, min(z_top, H_MECH)))
    return cols


def build_facade(face, trim, glass):
    """One pyramid face: recessed vertical window channels between flat piers.

    The face is cut into horizontal bands at every channel-termination height;
    inside a band the set of live channels is constant, so each band is a
    simple strip of quads (pier / jamb / recessed glass / jamb / pier ...).
    """
    cols = window_columns(face)
    if face in (0, 2):  # the wings cover the middle of the east and west faces
        cols = [(u, min(zt, WING_Z0)) if abs(u) < WING_HALF + 0.6 else (u, zt)
                for u, zt in cols]
    levels = sorted({H_BAND} | {zt for _, zt in cols} | {H_MECH})
    levels = [z for z in levels if H_BAND <= z <= H_MECH]

    verts, faces, fmats = [], [], []

    def V(u, z, out):
        p = face_point(face, u, z, out)
        verts.append((p[0], p[1], z))
        return len(verts) - 1

    for b in range(len(levels) - 1):
        z0, z1 = levels[b], levels[b + 1]
        if z1 - z0 < 0.05:
            continue
        live = [(u, zt) for u, zt in cols if zt >= z1 - 1e-6]
        # u breakpoints across the band, in face-local metres
        edges = []
        for u, _ in live:
            edges.append((u - WIN_WIDE / 2, u + WIN_WIDE / 2))
        marks = [-1e9]
        for a, b2 in edges:
            marks += [a, b2]
        spans = []
        prev = None
        for a, b2 in edges:
            spans.append(("pier", prev, a))
            spans.append(("win", a, b2))
            prev = b2
        spans.append(("pier", prev, None))

        def clamp_u(u, z):
            lim = half_width(z) - CHAMFER
            return max(-lim, min(lim, u))

        for kind, ua, ub in spans:
            if kind == "pier":
                ua_ = ua if ua is not None else -1e9
                ub_ = ub if ub is not None else 1e9
                a0 = clamp_u(ua_, z0)
                b0 = clamp_u(ub_, z0)
                a1 = clamp_u(ua_, z1)
                b1 = clamp_u(ub_, z1)
                if b0 - a0 < 0.02 and b1 - a1 < 0.02:
                    continue
                i0, i1 = V(a0, z0, 0.0), V(b0, z0, 0.0)
                i2, i3 = V(b1, z1, 0.0), V(a1, z1, 0.0)
                faces.append((i0, i1, i2, i3))
                fmats.append(0)
            else:
                out = -WIN_DEEP
                # recessed glass
                g0, g1 = V(ua, z0, out), V(ub, z0, out)
                g2, g3 = V(ub, z1, out), V(ua, z1, out)
                faces.append((g0, g1, g2, g3))
                fmats.append(1)
                # jambs
                s0, s1 = V(ua, z0, 0.0), V(ua, z1, 0.0)
                faces.append((s0, s1, g3, g0))
                fmats.append(0)
                t0, t1 = V(ub, z0, 0.0), V(ub, z1, 0.0)
                faces.append((g1, g2, t1, t0))
                fmats.append(0)
                # head: close the channel where it terminates at z1
                if not any(abs(u - (ua + ub) / 2) < 1e-6 and zt > z1 + 1e-6
                           for u, zt in cols):
                    faces.append((g3, g2, t1, s1))
                    fmats.append(0)
        # sill at the very bottom of the facade
        if b == 0:
            for kind, ua, ub in spans:
                if kind != "win":
                    continue
                out = -WIN_DEEP
                a0, b0 = V(ua, z0, 0.0), V(ub, z0, 0.0)
                a1, b1 = V(ua, z0, out), V(ub, z0, out)
                faces.append((a0, b0, b1, a1))
                fmats.append(0)

    return new_mesh(
        f"facade_{FACE_NAME[face]}", verts, faces, [trim, glass], fmats, recalc=False
    )


def build_chamfers(trim):
    """The four blank chamfered corner strips, grade to the mechanical band."""
    for q in range(4):
        z0, z1 = 0.0, H_CROWN
        quad = []
        for z in (z0, z1):
            a = half_width(z)
            c = min(CHAMFER, a * 0.4)
            p0 = rot2(rot2((a, a - c), FACE_ANGLE[q]), YAW)
            p1 = rot2(rot2((a - c, a), FACE_ANGLE[q]), YAW)
            quad.append((p0, p1))
        verts = [
            (quad[0][0][0], quad[0][0][1], z0),
            (quad[0][1][0], quad[0][1][1], z0),
            (quad[1][1][0], quad[1][1][1], z1),
            (quad[1][0][0], quad[1][0][1], z1),
        ]
        new_mesh(f"corner_{q}", verts, [(0, 1, 2, 3)], [trim], recalc=False)


# ------------------------------------------------------------------- massing


def build_wings(trim, roofd):
    """Triangular buttresses: vertical outer face, flush at z0, flat cap."""
    for face in (0, 2):
        nrm = face_normal(face)
        tan = face_tangent(face)
        a0 = half_width(WING_Z0)  # outer plane distance from the axis
        name = FACE_NAME[face]
        verts = []
        for s in (-WING_HALF, WING_HALF):
            for z, r in ((WING_Z0, a0), (WING_Z1, a0)):
                # outer face is vertical: constant distance a0
                verts.append((nrm[0] * r + tan[0] * s, nrm[1] * r + tan[1] * s, z))
            for z in (WING_Z1, WING_Z0):
                r = half_width(z) - 1.2  # inner edge buried in the shell
                verts.append((nrm[0] * r + tan[0] * s, nrm[1] * r + tan[1] * s, z))
        # verts: 0..3 = side -, 4..7 = side + (outer lo, outer hi, inner hi, inner lo)
        faces = [
            (0, 1, 2, 3),
            (7, 6, 5, 4),
            (0, 4, 5, 1),  # bottom (buried)
            (1, 5, 6, 2),  # top cap
            (0, 3, 7, 4),
            (3, 2, 6, 7),
        ]
        obj = new_mesh(f"wing_{name}", verts, faces, [trim])
        bevel(obj, width=0.35, segments=2)
        # flat cap detail so the wing tops read from the aerial camera
        ang = math.atan2(nrm[1], nrm[0])
        cx, cy = nrm[0] * (a0 - 3.0), nrm[1] * (a0 - 3.0)
        bevel(
            box(f"wing_{name}_parapet", cx, cy, WING_Z1, WING_Z1 + 0.8, 5.6, 10.0,
                trim, yaw=ang),
            width=0.2,
        )
        bevel(
            box(f"wing_{name}_hatch", cx, cy, WING_Z1 + 0.4, WING_Z1 + 1.1, 2.4, 3.4,
                roofd, yaw=ang),
            width=0.15,
        )


def build_crown(trim, steel, roofd):
    ring_band("mech_band", H_MECH, H_CROWN - 1.6, -0.3, 0.1, roofd)
    ring_band("parapet", H_CROWN - 1.6, H_CROWN, -0.2, 0.55, trim)
    # metal hip roof rising from the parapet to the spire collar
    a = half_width(H_CROWN) - 0.2
    top = H_CROWN + 3.0
    verts = []
    for p in outline(H_CROWN - 0.3, -0.2):
        verts.append((p[0], p[1], H_CROWN - 0.3))
    n = len(verts)
    for p in outline(H_CROWN - 0.3, -0.2):
        k = SPIRE_A0 / a
        verts.append((p[0] * k, p[1] * k, top))
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    new_mesh("crown_roof", verts, faces, [steel], recalc=False)
    # the window-washing rig parked on the crown: the one piece of roof
    # furniture the downward camera can actually see past the hip roof
    cx, cy = rot2((0.0, -(half_width(H_CROWN) - 1.4)), YAW)
    bevel(box("bmu", cx, cy, H_CROWN - 0.2, H_CROWN + 1.5, 5.0, 1.5, steel), width=0.15)


def build_spire(steel, glow, red_glow):
    """The spire continues the pyramid's line, stepped in from the parapet."""

    def a_spire(z):
        return SPIRE_A0 * (H_TIP - z) / (H_TIP - H_CROWN)

    zs = [H_CROWN, JEWEL_Z - 6.0, JEWEL_Z, H_TIP - 3.2]
    rings = []
    for z in zs:
        a = max(a_spire(z), 0.12)
        pts = [rot2((a, a), YAW), rot2((-a, a), YAW), rot2((-a, -a), YAW),
               rot2((a, -a), YAW)]
        rings.append((z, pts))
    loft("spire", rings, [steel, glow], row_mats=[0, 1, 0], cap_bottom=True)
    # the 32-pane glazed room reads as one lit collar; the tip carries the
    # permanent red aviation light
    tip_a = max(a_spire(H_TIP - 3.2), 0.12)
    verts = [
        (*rot2((tip_a, tip_a), YAW), H_TIP - 3.2),
        (*rot2((-tip_a, tip_a), YAW), H_TIP - 3.2),
        (*rot2((-tip_a, -tip_a), YAW), H_TIP - 3.2),
        (*rot2((tip_a, -tip_a), YAW), H_TIP - 3.2),
        (0.0, 0.0, H_TIP),
    ]
    new_mesh(
        "spire_tip",
        verts,
        [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)],
        [red_glow],
    )


def build_ground(trim, glass, stone, roofd):
    """Chevron truss colonnade in the plane of the sloping facade."""
    for face in range(4):
        nrm = face_normal(face)
        tan = face_tangent(face)
        ang = math.atan2(nrm[1], nrm[0])
        w_foot = half_width(0.0) - CHAMFER
        w_apex = half_width(H_LEGS) - CHAMFER
        feet = [(-w_foot + 2 * w_foot * i / LEG_BAYS, 0.0) for i in range(LEG_BAYS + 1)]
        apex = [
            (-w_apex + 2 * w_apex * (i + 0.5) / LEG_BAYS, H_LEGS)
            for i in range(LEG_BAYS)
        ]
        members = []
        for i in range(LEG_BAYS):
            members.append((feet[i], apex[i]))
            members.append((apex[i], feet[i + 1]))
        for k, ((u0, z0), (u1, z1)) in enumerate(members):
            # lay the member out in face-local (u, z), which maps affinely to
            # the sloping face plane, then extrude it inward
            du, dz = u1 - u0, z1 - z0
            L = math.hypot(du, dz)
            du, dz = du / L, dz / L
            px, pz = -dz * LEG_W / 2, du * LEG_W / 2
            ext = LEG_W * 0.55  # overlap so the joints close
            a_u, a_z = u0 - du * ext, z0 - dz * ext
            b_u, b_z = u1 + du * ext, z1 + dz * ext
            corners = [
                (a_u - px, a_z - pz),
                (b_u - px, b_z - pz),
                (b_u + px, b_z + pz),
                (a_u + px, a_z + pz),
            ]
            quad = []
            for u, z in corners:
                z = max(0.0, z)
                lim = half_width(z) - CHAMFER
                u = max(-lim, min(lim, u))
                p = face_point(face, u, z, 0.0)
                quad.append(Vector((p[0], p[1], z)))
            obj = quad_prism(f"leg_{FACE_NAME[face]}_{k}", quad, -LEG_D, nrm, trim)
            bevel(obj, width=0.18, segments=2)
    ring_band("base_band", H_LEGS - 0.4, H_BAND, -0.2, 0.35, trim)
    ring_band("base_slit", H_LEGS + 0.9, H_LEGS + 2.6, -0.55, -0.15, glass)
    # recessed lobby box + its roof slab, glimpsed through the chevrons
    lob = 0.62
    rings = [
        (0.0, [(x * lob, y * lob) for x, y in outline(0.0)]),
        (H_LOBBY, [(x * lob, y * lob) for x, y in outline(0.0)]),
    ]
    loft("lobby_glass", rings, [glass], cap_bottom=True)
    pts = [(x * lob * 1.04, y * lob * 1.04) for x, y in outline(0.0)]
    new_mesh(
        "lobby_roof",
        [(x, y, H_LOBBY) for x, y in pts],
        [tuple(range(len(pts)))],
        [stone],
    )
    new_mesh(
        "lobby_sill",
        [(x, y, 0.35) for x, y in [(x * lob * 1.08, y * lob * 1.08) for x, y in outline(0.0)]],
        [tuple(range(len(pts)))],
        [stone],
    )
    # main entrance on the Montgomery Street (east) face: the identity cue
    nrm = face_normal(0)
    tan = face_tangent(0)
    ang = math.atan2(nrm[1], nrm[0])
    r = half_width(0.0) * lob
    bevel(
        box("entrance_doors", nrm[0] * (r + 0.4), nrm[1] * (r + 0.4), 0.0, 6.2,
            1.0, 12.0, glass, yaw=ang),
        width=0.2,
    )
    bevel(
        box("entrance_canopy", nrm[0] * (r + 2.6), nrm[1] * (r + 2.6), 6.2, 7.4,
            6.0, 15.0, stone, yaw=ang),
        width=0.28,
    )
    for s in (-6.6, 6.6):
        bevel(
            box("entrance_pier", nrm[0] * (r + 5.0) + tan[0] * s,
                nrm[1] * (r + 5.0) + tan[1] * s, 0.0, 6.2, 1.6, 1.6, stone, yaw=ang),
            width=0.18,
        )
    # soffit under the tower, so the colonnade reads as covered from below
    pts = [(x, y) for x, y in outline(H_LEGS)]
    new_mesh(
        "soffit",
        [(x, y, H_LEGS) for x, y in pts],
        [tuple(range(len(pts) - 1, -1, -1))],
        [roofd],
    )


# --------------------------------------------------------------------- build


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    trim = material("Toy_trim")
    glass = material("Toy_glass")
    steel = material("Toy_steel")
    stone = material("Toy_stone")
    roofd = material("Toy_roofd")
    glow = material("Toy_white_Glow")
    red_glow = material("Toy_red_Glow")

    for face in range(4):
        build_facade(face, trim, glass)
    build_chamfers(trim)
    build_wings(trim, roofd)
    build_crown(trim, steel, roofd)
    build_spire(steel, glow, red_glow)
    build_ground(trim, glass, stone, roofd)
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

    blend = os.path.join(out, "transamerica-pyramid.blend")
    glb = os.path.join(out, "transamerica-pyramid.glb")
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
