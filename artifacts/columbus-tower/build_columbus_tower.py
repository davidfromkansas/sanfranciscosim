"""Deterministic Blender build of the SF-SIM miniature Columbus Tower
(Sentinel Building).

    blender -b --python build_columbus_tower.py -- [--out DIR]

Writes columbus-tower.blend and columbus-tower.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = footprint bbox centre (anchor
lon −122.4050266, lat 37.7965554), min Z = 0, finial tip exactly 29.0 m.

Design (see REFERENCE.md for the sources behind every number):

* the true OSM wedge polygon (way/288485994), including its 14-node rounded
  apex arc (fit circle r 2.482 m), extruded as the white glazed-brick body;
* verdigris bay stacks on the Kearny (4) and Columbus (3) flanks, each floor
  with the building's signature segmental eyebrow hood; the flat Jackson back
  gets a plain window grid;
* the apex turret sequence above the main cornice: windowed drum, copper
  dome, lantern cupola, gold finial ball and spire — the identity silhouette;
* a recessed cafe storefront with verdigris pilasters and the red Zoetrope
  awning band wrapping Columbus, the apex and Kearny;
* night state per the night photo: warm _Glow shells at the cafe front and a
  scatter of lit windows, plus the red light at the cupola. Glow surfaces are
  thin shells proud of opaque glazing (the app renders _Glow in a separate
  layer that is ~12% alpha by day — never author a primary surface as glow);
* a designed roof for the app's downward camera: deck, stair penthouse,
  HVAC pair, skylight, vent.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/288485994 projected with the app's tangent projection and recentred
# on the footprint bbox centre. CW order. Vertices 3..16 are the apex arc.
FOOTPRINT = [
    (8.659, -6.03),
    (-5.491, -8.362),
    (-6.195, -8.473),
    (-8.351, 4.129),
    (-8.65, 4.361),
    (-9.09, 5.068),
    (-9.266, 5.886),
    (-9.169, 6.715),
    (-8.791, 7.456),
    (-8.192, 8.042),
    (-7.436, 8.384),
    (-6.6, 8.473),
    (-5.817, 8.285),
    (-5.121, 7.865),
    (-4.611, 7.235),
    (-4.329, 6.483),
    (-4.312, 6.185),
    (9.266, -5.378),
]
ARC_C = (-6.778, 6.005)  # best-fit circle of the apex arc (residuals < 4 cm)
ARC_R = 2.482
# The flatiron nose wraps ~226 deg: from 4.2 deg (ccw from +X) up through
# north to 230 deg. The outward bisector sits at 120 deg = 330 deg true.
ARC_A0 = math.radians(4.2)
ARC_A1 = math.radians(230.0)

H_TIP = 29.0  # finial tip = OSM height (total-height interpretation)
H_STORE = 4.05  # cafe storefront band
FLOOR_H = 3.0  # six upper floors
H_WALL = 22.0  # top of the white wall / base of the main cornice
H_CORN0, H_CORN1 = 21.9, 22.75  # main cornice band
H_DECK = 22.28  # roof deck surface
H_DRUM0, H_DRUM1 = 21.9, 24.4  # turret drum (continues the round bay)
H_DOME0 = 24.85  # dome springing, above the drum cornice
H_DOME1 = 26.9  # dome closes
FLOORS = [4.0 + FLOOR_H * f for f in range(6)]  # floor lines of the six levels

BAY_W, BAY_D, BAY_EMBED = 2.7, 0.85, 0.15
STORE_INSET = 0.45

# Palette from .agents/skills/sf-asset-check (hex, sRGB); materials hold the
# linear equivalents, matching the shipped kit GLBs.
PALETTE_HEX = {
    "Toy_white": "f7f4ec",
    "Toy_verdigris": "9fb8a8",
    "Toy_glass": "2a4d73",
    "Toy_ink": "3a3530",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_red": "c4453c",
    "Toy_gold": "caa64a",
    "Toy_gold_Glow": "caa64a",
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

# --------------------------------------------------------------- 2D helpers


def poly_edge(i, j):
    """Edge i->j of FOOTPRINT: (a, b, length, tangent unit, outward normal)."""
    a, b = FOOTPRINT[i], FOOTPRINT[j]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (-t[1], t[0])  # CW polygon -> this points outward
    return a, b, length, t, n


EDGE_JACKSON = (0, 1)
EDGE_COLUMBUS = (2, 3)
EDGE_KEARNY = (16, 17)


def edge_point(edge, tpar):
    a, b, length, t, n = poly_edge(*edge)
    return (a[0] + (b[0] - a[0]) * tpar, a[1] + (b[1] - a[1]) * tpar), t, n, length


def offset_polygon(poly, d):
    """Miter offset of the convex CW footprint; positive d moves outward."""
    npts = len(poly)
    normals = []
    for i in range(npts):
        a, b = poly[i], poly[(i + 1) % npts]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        normals.append((-dy / length, dx / length))
    out = []
    for i in range(npts):
        n1 = normals[i - 1]
        n2 = normals[i]
        v = poly[i]
        det = n1[0] * n2[1] - n1[1] * n2[0]
        if abs(det) < 1e-6:
            out.append((v[0] + n2[0] * d, v[1] + n2[1] * d))
            continue
        c1 = v[0] * n1[0] + v[1] * n1[1] + d
        c2 = v[0] * n2[0] + v[1] * n2[1] + d
        out.append(
            (
                (c1 * n2[1] - c2 * n1[1]) / det,
                (c2 * n1[0] - c1 * n2[0]) / det,
            )
        )
    return out


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


def prism(name, poly, z0, z1, mat, mat_caps=None):
    """Closed extrusion of a convex-ish polygon (walls + both caps)."""
    npts = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces = []
    face_mats = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
        face_mats.append(0)
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    face_mats += [1 if mat_caps else 0] * 2
    mats = [mat, mat_caps] if mat_caps else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def ring_band(name, z0, z1, off_in, off_out, mat):
    """Closed cornice band following the footprint: 4 loops, quads between."""
    lo_in = offset_polygon(FOOTPRINT, off_in)
    lo_out = offset_polygon(FOOTPRINT, off_out)
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


def swept_profile(name, origin, sweep_dir, sweep_len, prof_dir, profile, mat):
    """Closed prism: 2D profile (d, z) in the plane spanned by prof_dir and Z,
    swept horizontally along sweep_dir. Profile must be convex, CCW."""
    verts = []
    for end in (0.0, sweep_len):
        for d, z in profile:
            verts.append(
                (
                    origin[0] + sweep_dir[0] * end + prof_dir[0] * d,
                    origin[1] + sweep_dir[1] * end + prof_dir[1] * d,
                    z,
                )
            )
    npts = len(profile)
    faces = [tuple(range(npts - 1, -1, -1)), tuple(range(npts, 2 * npts))]
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    return new_mesh(name, verts, faces, [mat])


def arc_prism(name, r_in, r_out, a0, a1, z0, z1, mat, seg=10, centre=ARC_C):
    """Closed curved slab around the apex arc centre."""
    inner = []
    outer = []
    for i in range(seg + 1):
        a = a0 + (a1 - a0) * i / seg
        inner.append((centre[0] + r_in * math.cos(a), centre[1] + r_in * math.sin(a)))
        outer.append((centre[0] + r_out * math.cos(a), centre[1] + r_out * math.sin(a)))
    verts = []
    for loop, z in ((inner, z0), (outer, z0), (outer, z1), (inner, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    npts = seg + 1
    faces = []
    for k in range(4):
        a_, b_ = k * npts, ((k + 1) % 4) * npts
        for i in range(seg):
            faces.append((a_ + i, a_ + i + 1, b_ + i + 1, b_ + i))
    faces.append((0, npts, 2 * npts, 3 * npts))  # end caps close the slab
    faces.append((npts - 1, 2 * npts - 1, 3 * npts - 1, 4 * npts - 1))
    return new_mesh(name, verts, faces, [mat])


def lathe(name, rows, mat, seg=14, cap_top=True, cap_bottom=True, centre=ARC_C):
    """Surface of revolution around the turret axis. rows = [(z, radius)]."""
    verts = []
    for z, r in rows:
        for i in range(seg):
            a = 2 * math.pi * i / seg
            verts.append((centre[0] + r * math.cos(a), centre[1] + r * math.sin(a), z))
    faces = []
    for r in range(len(rows) - 1):
        for i in range(seg):
            j = (i + 1) % seg
            faces.append((r * seg + i, r * seg + j, (r + 1) * seg + j, (r + 1) * seg + i))
    if cap_bottom:
        faces.append(tuple(range(seg - 1, -1, -1)))
    if cap_top:
        off = (len(rows) - 1) * seg
        faces.append(tuple(range(off, off + seg)))
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


# --------------------------------------------------------------------- build


def eyebrow_profile(width, base_h=0.14, sag=0.5):
    """Segmental-arched hood outline (CCW, convex) in the (d, z) plane."""
    half = width / 2
    pts = [(-half, 0.0), (half, 0.0), (half, base_h)]
    for i in range(1, 8):
        a = math.pi * i / 8
        pts.append((half * math.cos(a), base_h + sag * math.sin(a)))
    pts.append((-half, base_h))
    return pts


def bay_stack(tag, edge, tpar, glass, verd, glow):
    """One verdigris bay stack with its six windows, sills and eyebrow hoods.

    Every window carries a glow shell: the building lights up whole at night.
    """
    (px, py), t, n, _ = edge_point(edge, tpar)
    yaw = math.atan2(t[1], t[0])
    face_d = BAY_D - BAY_EMBED  # how far the bay face stands off the wall

    frame = box(
        f"bay_{tag}",
        px + n[0] * (BAY_D / 2 - BAY_EMBED),
        py + n[1] * (BAY_D / 2 - BAY_EMBED),
        4.0,
        H_WALL - 0.05,
        BAY_W,
        BAY_D,
        verd,
        yaw=yaw,
    )
    bevel(frame, width=0.18, segments=2)

    for f, fz in enumerate(FLOORS):
        win_h0, win_h1 = fz + 0.5, fz + 2.3
        box(
            f"bay_{tag}_glass_{f}",
            px + n[0] * (face_d + 0.05),
            py + n[1] * (face_d + 0.05),
            win_h0,
            win_h1,
            BAY_W - 0.55,
            0.1,
            glass,
            yaw=yaw,
        )
        box(
            f"bay_{tag}_sill_{f}",
            px + n[0] * (face_d + 0.07),
            py + n[1] * (face_d + 0.07),
            win_h0 - 0.28,
            win_h0,
            BAY_W - 0.35,
            0.16,
            verd,
            yaw=yaw,
        )
        swept_profile(
            f"bay_{tag}_hood_{f}",
            (px - n[0] * 0.05 + 0, py - n[1] * 0.05),
            n,
            face_d + 0.22,
            t,
            [(d, win_h1 + z) for d, z in eyebrow_profile(BAY_W - 0.2)],
            verd,
        )
        # The shell covers ~55% of the glazed area, not all of it: at night it
        # reads as a fully lit window inside its dark frame, while by day
        # (12% alpha) it tints far less of the facade.
        box(
            f"bay_{tag}_lit_{f}",
            px + n[0] * (face_d + 0.125),
            py + n[1] * (face_d + 0.125),
            win_h0 + 0.25,
            win_h1 - 0.25,
            BAY_W - 1.05,
            0.04,
            glow,
            yaw=yaw,
        )


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    white = material("Toy_white")
    verd = material("Toy_verdigris")
    glass = material("Toy_glass")
    ink = material("Toy_ink")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    red = material("Toy_red")
    gold = material("Toy_gold")
    gglow = material("Toy_gold_Glow")  # warm: cafe frontage and lantern
    wglow = material("Toy_white_Glow")  # cool: lit office windows
    rglow = material("Toy_red_Glow")

    # --- body, storefront, cornices ----------------------------------------
    prism("body", FOOTPRINT, 3.9, H_WALL, white)
    prism("storefront", offset_polygon(FOOTPRINT, -STORE_INSET), 0.0, H_STORE, ink)
    # Kickplate: without it the recessed shopfront reads as a black ring at
    # the base from the aerial camera (style bible s.19 — no crushed blacks).
    ring_band("kickplate", 0.0, 0.62, -STORE_INSET - 0.02, -STORE_INSET + 0.16, verd)
    ring_band("belt_course", 3.8, 4.3, -0.25, 0.3, verd)
    ring_band("main_cornice", H_CORN0, H_CORN1, -0.25, 0.55, verd)
    prism("roof_deck", offset_polygon(FOOTPRINT, -0.35), H_WALL - 0.05, H_DECK, roofd)

    # --- flank bay stacks with the eyebrow-hood rhythm ---------------------
    # Deterministic scatter of lit windows follows the night photo: a warm
    # handful, not a full grid.
    # Bay counts follow the photographs: three stacks on the long Kearny
    # flank, two on the shorter Columbus flank, with broad white glazed-brick
    # strips between them — the green-on-white contrast is recognition cue 2.
    for i, tpar in enumerate((0.19, 0.45, 0.71)):
        bay_stack(f"k{i}", EDGE_KEARNY, tpar, glass, verd, wglow)
    for i, tpar in enumerate((0.34, 0.64)):
        bay_stack(f"c{i}", EDGE_COLUMBUS, tpar, glass, verd, wglow)

    # --- the plain Jackson back: window grid on the white wall -------------
    for i, tpar in enumerate((0.14, 0.32, 0.5, 0.68, 0.86)):
        (px, py), t, n, _ = edge_point(EDGE_JACKSON, tpar)
        yaw = math.atan2(t[1], t[0])
        for f, fz in enumerate(FLOORS):
            box(
                f"jack_{i}_frame_{f}",
                px + n[0] * 0.03,
                py + n[1] * 0.03,
                fz + 0.35,
                fz + 2.6,
                1.55,
                0.12,
                verd,
                yaw=yaw,
            )
            box(
                f"jack_{i}_glass_{f}",
                px + n[0] * 0.08,
                py + n[1] * 0.08,
                fz + 0.55,
                fz + 2.4,
                1.3,
                0.08,
                glass,
                yaw=yaw,
            )
            box(
                f"jack_{i}_lit_{f}",
                px + n[0] * 0.125,
                py + n[1] * 0.125,
                fz + 0.75,
                fz + 2.2,
                0.95,
                0.04,
                wglow,
                yaw=yaw,
            )

    # --- apex round bay: fully verdigris-clad nose (the photos show the
    # whole rounded bay in copper green on the white body) ------------------
    arc_prism("apex_cladding", ARC_R + 0.01, ARC_R + 0.15, math.radians(18),
              math.radians(216), 3.9, H_CORN0, verd, seg=16)
    for f, fz in enumerate(FLOORS):
        arc_prism(
            f"apex_glass_{f}",
            ARC_R + 0.15,
            ARC_R + 0.23,
            math.radians(26),
            math.radians(208),
            fz + 0.5,
            fz + 2.3,
            glass,
            seg=14,
        )
        arc_prism(
            f"apex_ring_{f}",
            ARC_R + 0.15,
            ARC_R + 0.31,
            math.radians(20),
            math.radians(214),
            fz + 2.4,
            fz + 2.78,
            verd,
            seg=14,
        )
        arc_prism(
            f"apex_lit_{f}",
            ARC_R + 0.235,
            ARC_R + 0.265,
            math.radians(38),
            math.radians(196),
            fz + 0.78,
            fz + 2.02,
            wglow,
            seg=12,
        )
    for adeg in (24.0, 86.0, 148.0, 210.0):
        a = math.radians(adeg)
        box(
            f"apex_pilaster_{int(adeg)}",
            ARC_C[0] + (ARC_R + 0.24) * math.cos(a),
            ARC_C[1] + (ARC_R + 0.24) * math.sin(a),
            4.0,
            H_CORN0,
            0.34,
            0.36,
            verd,
            yaw=a + math.pi / 2,
        )

    # --- the turret: drum, dome, lantern, gold finial ----------------------
    lathe("drum", [(H_DRUM0, 2.62), (H_DRUM1, 2.62)], verd)
    for k, adeg in enumerate((30, 75, 120, 165, 210)):
        a0, a1 = math.radians(adeg - 13), math.radians(adeg + 13)
        arc_prism(f"drum_win_{k}", 2.62, 2.7, a0, a1, 22.9, 24.1, glass, seg=4)
        arc_prism(f"drum_lit_{k}", 2.705, 2.725, a0 + 0.04, a1 - 0.04, 23.0, 24.0, wglow, seg=4)
    lathe("drum_cornice", [(H_DRUM1, 2.5), (24.55, 2.95), (H_DOME0, 2.95), (H_DOME0, 2.5)], verd)
    dome_rows = []
    for i in range(7):
        tt = i / 6 * 0.96
        dome_rows.append((H_DOME0 + (H_DOME1 - H_DOME0) * tt, 2.55 * math.cos(tt * math.pi / 2) ** 0.85))
    lathe("dome", dome_rows, verd)
    lathe("lantern", [(26.6, 0.82), (27.75, 0.82)], verd)
    lathe("lantern_glow", [(26.95, 0.86), (27.55, 0.86)], gglow)
    lathe("lantern_cap", [(27.75, 0.98), (28.0, 0.52), (28.18, 0.16)], verd)
    lathe(
        "finial_ball",
        [(28.32 - 0.33 * math.cos(math.pi * p / 6), 0.33 * math.sin(math.pi * p / 6)) for p in range(1, 6)],
        gold,
        seg=10,
    )
    lathe("spire", [(28.35, 0.045), (H_TIP, 0.012)], verd, seg=8)
    lathe("beacon", [(28.55, 0.1), (28.72, 0.1)], rglow, seg=8)

    # --- cafe storefront: pilasters, glass, glow, red awnings --------------
    for edge, spans in ((EDGE_KEARNY, (0.03, 0.97)), (EDGE_COLUMBUS, (0.03, 0.97))):
        a_pt, t, n, length = edge_point(edge, spans[0])
        run = length * (spans[1] - spans[0])
        inset_origin = (a_pt[0] - n[0] * STORE_INSET, a_pt[1] - n[1] * STORE_INSET)
        swept_profile(
            f"store_glass_{edge[0]}",
            inset_origin,
            t,
            run,
            n,
            [(0.0, 0.65), (0.08, 0.65), (0.08, 3.35), (0.0, 3.35)],
            glass,
        )
        swept_profile(
            f"store_glow_{edge[0]}",
            inset_origin,
            t,
            run,
            n,
            [(0.09, 0.78), (0.12, 0.78), (0.12, 3.18), (0.09, 3.18)],
            gglow,
        )
        swept_profile(
            f"awning_{edge[0]}",
            a_pt,
            t,
            run,
            n,
            [(0.0, 3.34), (0.95, 2.92), (0.95, 3.1), (0.0, 3.7)],
            red,
        )

    # Jackson is the back: a service base, not cafe glazing. Ink wall with a
    # loading door and two small high windows.
    a_pt, t_j2, n_j2, length_j = edge_point(EDGE_JACKSON, 0.0)
    yaw_j2 = math.atan2(t_j2[1], t_j2[0])
    for k, (tpar, w) in enumerate(((0.3, 2.6), (0.72, 1.5))):
        px = a_pt[0] + t_j2[0] * length_j * tpar
        py = a_pt[1] + t_j2[1] * length_j * tpar
        box(f"jack_door_{k}", px - n_j2[0] * (STORE_INSET - 0.06),
            py - n_j2[1] * (STORE_INSET - 0.06), 0.0, 2.9 if k == 0 else 2.4,
            w, 0.1, verd, yaw=yaw_j2)
        box(f"jack_door_glass_{k}", px - n_j2[0] * (STORE_INSET - 0.12),
            py - n_j2[1] * (STORE_INSET - 0.12), 0.35, 2.6 if k == 0 else 2.15,
            w - 0.35, 0.06, glass, yaw=yaw_j2)
        box(f"jack_door_lit_{k}", px - n_j2[0] * (STORE_INSET - 0.165),
            py - n_j2[1] * (STORE_INSET - 0.165), 0.45, 2.5 if k == 0 else 2.05,
            w - 0.55, 0.04, gglow, yaw=yaw_j2)
    arc_prism("store_glass_apex", ARC_R - STORE_INSET + 0.02, ARC_R - STORE_INSET + 0.1,
              math.radians(12), math.radians(222), 0.65, 3.35, glass, seg=14)
    arc_prism("store_glow_apex", ARC_R - STORE_INSET + 0.11, ARC_R - STORE_INSET + 0.14,
              math.radians(20), math.radians(214), 0.78, 3.18, gglow, seg=14)
    for k in range(3):
        a0 = math.radians(0 + 78.0 * k)
        a1 = math.radians(0 + 78.0 * (k + 1))
        p0 = (ARC_C[0] + (ARC_R + 0.05) * math.cos(a0), ARC_C[1] + (ARC_R + 0.05) * math.sin(a0))
        p1 = (ARC_C[0] + (ARC_R + 0.05) * math.cos(a1), ARC_C[1] + (ARC_R + 0.05) * math.sin(a1))
        d = (p1[0] - p0[0], p1[1] - p0[1])
        run = math.hypot(*d)
        t = (d[0] / run, d[1] / run)
        mid_a = (a0 + a1) / 2
        n = (math.cos(mid_a), math.sin(mid_a))
        swept_profile(
            f"awning_apex_{k}",
            p0,
            t,
            run,
            n,
            [(-0.3, 3.3), (0.75, 2.92), (0.75, 3.1), (-0.3, 3.66)],
            red,
        )

    # Pilasters at every bay centreline and at the street corners.
    pilaster_spots = (
        [(EDGE_KEARNY, tp) for tp in (0.02, 0.32, 0.58, 0.84, 0.98)]
        + [(EDGE_COLUMBUS, tp) for tp in (0.03, 0.2, 0.52, 0.86, 0.97)]
        + [(EDGE_JACKSON, tp) for tp in (0.02, 0.52, 0.98)]
    )
    for k, (edge, tpar) in enumerate(pilaster_spots):
        (px, py), t, n, _ = edge_point(edge, tpar)
        yaw = math.atan2(t[1], t[0])
        box(
            f"store_pilaster_{k}",
            px - n[0] * 0.03,
            py - n[1] * 0.03,
            0.0,
            4.3,
            0.55,
            0.5,
            verd,
            yaw=yaw,
        )

    # --- the roof, designed for the downward camera ------------------------
    _, t_j, n_j, _ = edge_point(EDGE_JACKSON, 0.5)
    yaw_j = math.atan2(t_j[1], t_j[0])
    bevel(box("penthouse", 2.2, -4.5, H_DECK, H_DECK + 2.1, 3.4, 2.5, white, yaw=yaw_j), width=0.12)
    box("penthouse_cap", 2.2, -4.5, H_DECK + 2.1, H_DECK + 2.34, 3.7, 2.8, verd, yaw=yaw_j)
    bevel(box("hvac_a", -2.5, -3.1, H_DECK, H_DECK + 0.95, 1.8, 1.3, steel, yaw=yaw_j), width=0.1)
    bevel(box("hvac_b", -0.6, -3.4, H_DECK, H_DECK + 0.75, 1.35, 1.1, steel, yaw=yaw_j), width=0.08)
    bevel(box("hvac_c", 5.6, -4.9, H_DECK, H_DECK + 0.62, 1.15, 0.95, steel, yaw=yaw_j), width=0.08)
    bevel(box("plant_deck", -2.9, -1.0, H_DECK, H_DECK + 0.22, 3.2, 2.0, roofd, yaw=yaw_j), width=0.06)
    bevel(box("skylight_curb", 0.7, -0.5, H_DECK, H_DECK + 0.34, 2.2, 1.5, verd, yaw=yaw_j), width=0.06)
    box("skylight", 0.7, -0.5, H_DECK + 0.32, H_DECK + 0.56, 1.85, 1.2, glass, yaw=yaw_j)
    bevel(box("tank_stand", -4.2, 1.6, H_DECK, H_DECK + 0.9, 1.5, 1.5, steel, yaw=yaw_j), width=0.07)
    lathe("water_tank", [(H_DECK + 0.9, 0.86), (H_DECK + 2.5, 0.86), (H_DECK + 2.8, 0.5)],
          steel, seg=10, centre=(-4.2, 1.6))
    lathe("roof_vent", [(H_DECK, 0.2), (H_DECK + 1.2, 0.2)], steel, seg=8, centre=(3.9, -1.9))
    lathe("roof_flue", [(H_DECK, 0.16), (H_DECK + 0.85, 0.16)], verd, seg=8, centre=(4.9, -2.7))
    # A short parapet return keeps the deck from reading as an open tray.
    ring_band("parapet", H_DECK, H_DECK + 0.42, -0.42, -0.2, verd)

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
    print("[build] anchor lon/lat: -122.4050266 37.7965554 (footprint bbox centre)")
    print("[build] apex heading: 330.4 deg true (NNW into the Columbus/Kearny fork)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "columbus-tower.blend")
    glb = os.path.join(out, "columbus-tower.glb")
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
