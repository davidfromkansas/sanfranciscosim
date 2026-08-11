"""Deterministic Blender build of the SF-SIM miniature Mission Dolores.

    blender -b --python build_mission_dolores.py -- [--out DIR]

Writes mission-dolores.blend and mission-dolores.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops onto its anchor at its true heading with no loader rotation.
Both facades face EAST onto Dolores Street (REFERENCE.md §3 — the plan doc's
"north" was wrong); the two long axes splay 4 deg / 8 deg exactly as mapped.
Origin = combined bounding-box base centre, min Z = 0 at sidewalk grade.

Design (see REFERENCE.md for the source behind every number):

* the 1918 basilica: T-plan nave running west from a 24.6 m east facade,
  14 m eaves, tile gable, flat white aisle roofs, octagonal tiled crossing
  dome near the west end, apse half-dome, and two ASYMMETRICAL towers -
  south cupola to ~28 m, north wedding-cake tower normalised to 41.0 m at
  the cross tip (measured, not published: estimated true);
* the 1791 adobe chapel tight alongside to the south (1.4-2 m gap at the
  street): 12.2 x 37 m, 6.8 m eaves, deep dark-soffit tile roof, four-column
  facade with balcony, four pilasters, three arched bell openings, ridge cross;
* every piece is a closed solid (no open shells) so the deterministic
  visibility-ray normals test in the validator can pass;
* night state: EVERY window lights. White uplight strips wash the basilica
  facade; warm gold shells sit inside the belfry arches, the great central
  window, the nave clerestory and aisle windows, the transept and dome-drum
  windows, the parish-wing windows, the tower slits, the aisle roof
  skylights, and the adobe's three bells and flank openings. Each shell
  stands ~5 cm proud of an OPAQUE day surface and is inset on its other
  edges, because the app draws _Glow as a separate unlit layer at
  0.12 + 0.95 * uNight opacity - authoring a window itself as _Glow would
  make it 88 % transparent in daylight.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

# ---------------------------------------------------------------- parameters

# Site frame = basilica-footprint-centroid frame of the project projection,
# +X east, +Y north (REFERENCE.md §3). Recentred to the combined bbox at the
# end; the printed anchor is the WGS84 of the final origin.
LON0, LAT0 = -122.4375, 37.77
CENTROID_X, CENTROID_Z = 926.74, 622.61  # basilica centroid, project coords

BAS_ORIGIN = (30.3, 2.85)   # facade centre at grade, site frame
BAS_YAW = math.radians(4.0)  # facade normal bearing ~086 deg
ADO_ORIGIN = (36.35, -16.89)  # chapel facade centre at grade
ADO_YAW = math.radians(8.0)   # chapel bearing ~082 deg

# Basilica (local frame: origin facade centre, +x east out the front door)
FACADE_W = 24.6      # east face across, m
FACADE_D = 8.0       # depth of the facade/narthex block
CORNICE = 19.0       # shared main cornice, both tower shafts
FLOOR = 2.2          # main floor above sidewalk (top of the grand stair)
TOWER_A = 7.0        # tower shaft, square
TOWER_CY = FACADE_W / 2 - TOWER_A / 2  # 8.8 - tower centres +/-y
NAVE_HW = 6.5        # nave half width
NAVE_EAVE = 14.0     # OSM height tag
NAVE_RIDGE = 18.2
AISLE_HW = FACADE_W / 2  # aisles flush with the facade block
AISLE_H = 11.2
NAVE_X0, NAVE_X1 = -38.0, -FACADE_D
TRAN_X0, TRAN_X1 = -50.6, -38.0
TRAN_Y0, TRAN_Y1 = -15.0, 12.3
APSE_R = 5.9
APSE_X = -58.6 + APSE_R  # flat side buried into the transept block
DOME_C = (-44.3, 0.0)    # crossing dome centre
H_TOTAL = 41.0           # north tower cross tip - normalised target height

# Adobe chapel (local frame: origin facade centre, +x east)
ADO_HW = 6.1
ADO_LEN = 37.0
ADO_EAVE = 6.8
ADO_RIDGE = 10.3

# Project palette from .agents/skills/sf-asset-check (hex, sRGB).
PALETTE_HEX = {
    "Toy_cream": "f2ede3",
    "Toy_trim": "f3efe6",
    "Toy_ioorange": "c0402a",
    "Toy_brick": "c96f4a",
    "Toy_stone": "d9d2c2",
    "Toy_glass": "2a4d73",
    "Toy_ink": "3a3530",
    "Toy_verdigris": "9fb8a8",
    "Toy_gold": "caa64a",
    "Toy_rust": "a86444",
    "Toy_roofd": "45454a",
    "Toy_white_Glow": "f7f4ec",
    "Toy_gold_Glow": "caa64a",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# A module-level frame: every primitive transforms its local (x, y) through
# this before creating vertices, which is how each building carries its own
# true-world yaw and position.
FRAME = ((0.0, 0.0), 0.0)


def set_frame(origin, yaw):
    global FRAME
    FRAME = (origin, yaw)


def tf(x, y):
    (ox, oy), yaw = FRAME
    c, s = math.cos(yaw), math.sin(yaw)
    return (ox + x * c - y * s, oy + x * s + y * c)


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
        # Flagged for the app's night pass; emission off in the daylight asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    try:
        mat.blend_method = "OPAQUE"
    except AttributeError:
        pass
    return mat


def new_mesh(name, verts, faces, mat):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    mesh.materials.append(material(mat))
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
    """Miniature-style edge softening on the chunky solids (style bible s4)."""
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


def box(name, cx, cy, z0, z1, sx, sy, mat):
    hx, hy = sx / 2, sy / 2
    cs = [(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]
    verts = [(*tf(cx + x, cy + y), z0) for x, y in cs]
    verts += [(*tf(cx + x, cy + y), z1) for x, y in cs]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, mat)


def prism(name, profile, v0, v1, mat, axis="x"):
    """Closed solid: 2D profile (u, z) extruded from v0 to v1 along `axis`.

    axis='x': profile u maps to local y, extrusion along local x.
    axis='y': profile u maps to local x, extrusion along local y.
    Profile must be a simple CCW polygon; caps are n-gons.
    """
    if v1 < v0:  # keep the extrusion right-handed so normals stay outward
        v0, v1 = v1, v0
    n = len(profile)
    verts = []
    for v in (v0, v1):
        for u, z in profile:
            x, y = (v, u) if axis == "x" else (u, v)
            verts.append((*tf(x, y), z))
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    return new_mesh(name, verts, faces, mat)


def arch_profile(cu, w, z0, z1, seg=8):
    """Rectangle with a semicircular top: CCW (u, z) profile for prism()."""
    r = w / 2
    spring = max(z0, z1 - r)
    pts = [(cu + r, z0)]
    pts += [
        (cu + r * math.cos(a), spring + r * math.sin(a))
        for a in [math.pi * i / seg for i in range(seg + 1)]
    ]
    pts.append((cu - r, z0))
    return list(reversed(pts))  # CCW in (u, z)


def arch(name, cu, w, z0, z1, v0, v1, mat, axis="x", seg=8):
    return prism(name, arch_profile(cu, w, z0, z1, seg), v0, v1, mat, axis)


def lit_arch(name, cu, w, z0, z1, v_in, v_out, axis="x", seg=8, glass="Toy_glass"):
    """An arched window that is lit from inside at night.

    The day surface stays an opaque glazing solid; the night light is a thin
    `_Glow` shell standing 5 cm proud of it, narrower and shorter so its own
    edges are buried inside the reveal. The app draws every `_Glow` surface as
    a separate unlit layer at 0.12 + 0.95 * uNight opacity, so authoring the
    glazing itself as `_Glow` would make it 88 % transparent in daylight -
    hence the shell.
    """
    arch(name, cu, w, z0, z1, v_in, v_out, glass, axis=axis, seg=seg)
    s = 1.0 if v_out >= v_in else -1.0
    arch(
        name + "_lit",
        cu,
        w - 0.26,
        z0 + 0.13,
        z1 - 0.11,
        v_out - s * 0.18,
        v_out + s * 0.05,
        "Toy_gold_Glow",
        axis=axis,
        seg=seg,
    )


def lit_box(name, cx, cy, z0, z1, sx, sy, mat, face, proud=0.05):
    """A rectangular opening that lights up at night.

    `face` names the outward direction of the opening ('x+', 'x-', 'y+', 'y-'
    or 'z+' for a roof skylight). Same shell rule as lit_arch: the day surface
    stays opaque and the `_Glow` shell stands `proud` metres beyond it, inset
    on its other four sides so no shell edge is ever exposed.
    """
    box(name, cx, cy, z0, z1, sx, sy, mat)
    t = 0.16  # shell thickness
    if face in ("x+", "x-"):
        s = 1.0 if face == "x+" else -1.0
        gx = cx + s * (sx / 2 + proud - t / 2)
        box(name + "_lit", gx, cy, z0 + 0.08, z1 - 0.08, t, sy - 0.16, "Toy_gold_Glow")
    elif face in ("y+", "y-"):
        s = 1.0 if face == "y+" else -1.0
        gy = cy + s * (sy / 2 + proud - t / 2)
        box(name + "_lit", cx, gy, z0 + 0.08, z1 - 0.08, sx - 0.16, t, "Toy_gold_Glow")
    else:  # 'z+' - a roof skylight seen from the app's downward camera
        box(name + "_lit", cx, cy, z1 + proud - t / 2, z1 + proud + t / 2,
            sx - 0.16, sy - 0.16, "Toy_gold_Glow")


def gable_roof(name, x0, x1, cy, hw, ov, z_eave, z_ridge, t, mat, axis="x"):
    """Tile gable roof slab: thick inverted-V closed prism, ridge along axis."""
    p = [
        (cy - hw - ov, z_eave),
        (cy, z_ridge),
        (cy + hw + ov, z_eave),
        (cy + hw + ov, z_eave + t),
        (cy, z_ridge + t),
        (cy - hw - ov, z_eave + t),
    ]
    return prism(name, p, x0, x1, mat, axis)


def gable_wall(name, x0, x1, cy, hw, z0, z_eave, z_ridge, mat, axis="x"):
    """Wall volume with a gabled top, closed."""
    p = [
        (cy - hw, z0),
        (cy + hw, z0),
        (cy + hw, z_eave),
        (cy, z_ridge),
        (cy - hw, z_eave),
    ]
    return prism(name, p, x0, x1, mat, axis)


def ngon_drum(name, cx, cy, z0, z1, r, mat, seg=8, r_top=None, rot=0.0):
    """Closed prism/frustum on a regular n-gon plan."""
    r_top = r if r_top is None else r_top
    verts = []
    for z, rr in ((z0, r), (z1, r_top)):
        for i in range(seg):
            a = rot + 2 * math.pi * i / seg
            verts.append((*tf(cx + rr * math.cos(a), cy + rr * math.sin(a)), z))
    faces = [tuple(range(seg - 1, -1, -1)), tuple(range(seg, 2 * seg))]
    for i in range(seg):
        j = (i + 1) % seg
        faces.append((i, j, seg + j, seg + i))
    return new_mesh(name, verts, faces, mat)


def dome(name, cx, cy, z0, r, h, mat, seg=16, rings=6, rot=0.0):
    """Closed dome: lofted shrinking rings + apex fan + bottom cap."""
    verts = []
    for k in range(rings):
        phi = (math.pi / 2) * k / rings
        rr = r * math.cos(phi)
        z = z0 + h * math.sin(phi)
        for i in range(seg):
            a = rot + 2 * math.pi * i / seg
            verts.append((*tf(cx + rr * math.cos(a), cy + rr * math.sin(a)), z))
    verts.append((*tf(cx, cy), z0 + h))
    apex = len(verts) - 1
    faces = [tuple(range(seg - 1, -1, -1))]  # bottom cap
    for k in range(rings - 1):
        for i in range(seg):
            j = (i + 1) % seg
            faces.append((k * seg + i, k * seg + j, (k + 1) * seg + j, (k + 1) * seg + i))
    top = (rings - 1) * seg
    for i in range(seg):
        faces.append((top + i, top + (i + 1) % seg, apex))
    return new_mesh(name, verts, faces, mat)


def half_drum(name, cx, cy, z0, z1, r, mat, seg=10):
    """Half cylinder (flat chord on the +x side), closed - the apse."""
    pts = [
        (cx + r * math.cos(a), cy + r * math.sin(a))
        for a in [math.pi / 2 + math.pi * i / seg for i in range(seg + 1)]
    ]
    verts = [(*tf(x, y), z0) for x, y in pts] + [(*tf(x, y), z1) for x, y in pts]
    n = seg + 1
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(seg):
        faces.append((i, i + 1, n + i + 1, n + i))
    faces.append((seg, 0, n, n + seg))  # chord wall
    return new_mesh(name, verts, faces, mat)


def half_dome(name, cx, cy, z0, r, h, mat, seg=10, rings=5):
    """Quarter-sphere shell over the apse, closed with chord + bottom faces."""
    verts = []
    for k in range(rings):
        phi = (math.pi / 2) * k / rings
        rr = r * math.cos(phi)
        z = z0 + h * math.sin(phi)
        for i in range(seg + 1):
            a = math.pi / 2 + math.pi * i / seg
            verts.append((*tf(cx + rr * math.cos(a), cy + rr * math.sin(a)), z))
    verts.append((*tf(cx, cy), z0 + h))
    apex = len(verts) - 1
    n = seg + 1
    faces = [tuple(range(n - 1, -1, -1))]  # bottom
    for k in range(rings - 1):
        for i in range(seg):
            faces.append((k * n + i, k * n + i + 1, (k + 1) * n + i + 1, (k + 1) * n + i))
    top = (rings - 1) * n
    for i in range(seg):
        faces.append((top + i, top + i + 1, apex))
    chord = [k * n for k in range(rings)] + [apex] + [k * n + seg for k in range(rings - 1, -1, -1)]
    faces.append(tuple(chord))
    return new_mesh(name, verts, faces, mat)


def cylinder(name, cx, cy, z0, z1, r, mat, seg=10):
    return ngon_drum(name, cx, cy, z0, z1, r, mat, seg=seg)


def cross(name, cx, cy, z0, h, arm, mat, t=0.14):
    box(name + "_v", cx, cy, z0, z0 + h, t, t, mat)
    box(name + "_h", cx, cy, z0 + h * 0.68, z0 + h * 0.68 + t, t, arm, mat)


# ------------------------------------------------------------- the basilica


def build_basilica():
    set_frame(BAS_ORIGIN, BAS_YAW)
    cream, trim, ink = "Toy_cream", "Toy_trim", "Toy_ink"

    # facade / narthex block between the towers, with parapet + cornice band
    bevel(box("MD_facade_block", -FACADE_D / 2, 0, 0, CORNICE - 0.8, FACADE_D, FACADE_W, cream))
    box("MD_facade_cornice", -FACADE_D / 2, 0, CORNICE - 0.8, CORNICE, FACADE_D + 0.5, FACADE_W + 0.5, trim)

    # central bay, slightly proud, carrying all the Churrigueresque ornament.
    # BAY_F is the bay's front plane; every layer of ornament is stacked
    # forward of it, with each recess material standing a few centimetres
    # PROUDER than its own surround so the opening still reads from outside.
    BAY_F = 0.55
    bevel(box("MD_central_bay", -0.7, 0, 0, CORNICE, 2.5, 10.6, cream))

    # stepped espadana cresting above the cornice
    bevel(box("MD_crest_1", -0.7, 0, CORNICE, 20.4, 2.5, 10.6, trim))
    bevel(box("MD_crest_2", -0.8, 0, 20.4, 22.2, 2.3, 7.0, trim))
    bevel(box("MD_crest_3", -0.9, 0, 22.2, 24.0, 2.1, 3.6, trim))
    arch("MD_crest_niche", 0, 1.4, 22.5, 23.7, -0.3, BAY_F + 0.02, ink, axis="x")
    cylinder("MD_crest_finial", -0.9, 0, 24.0, 24.6, 0.28, "Toy_gold", seg=8)
    for y in (-5.3, 5.3):
        cylinder("MD_crest_pin", -0.7, y, CORNICE + 1.1, CORNICE + 2.8, 0.26, trim, seg=8)
    for y in (-3.5, 3.5):
        cylinder("MD_crest_pin2", -0.8, y, 20.4, 22.8, 0.24, trim, seg=8)

    # grand central portal: layered trim surround, deeper ink opening
    arch("MD_portal_trim", 0, 6.4, FLOOR, 10.2, -1.0, BAY_F + 0.60, trim, axis="x")
    arch("MD_portal_ink", 0, 4.6, FLOOR, 9.2, -0.5, BAY_F + 0.66, ink, axis="x")

    # central stained-glass window, surround, spiral columns, shell niches
    arch("MD_window_trim", 0, 5.8, 10.5, 17.9, -0.9, BAY_F + 0.40, trim, axis="x")
    arch("MD_window_glass", 0, 4.2, 11.0, 17.3, -0.5, BAY_F + 0.46, "Toy_glass", axis="x")
    arch("MD_window_glow", 0, 3.9, 11.2, 17.1, -0.5, BAY_F + 0.50, "Toy_gold_Glow", axis="x")
    for y in (-3.55, 3.55):
        cylinder("MD_col_a", BAY_F + 0.50, y, 10.5, 17.4, 0.38, trim, seg=10)
        box("MD_col_cap", BAY_F + 0.50, y, 17.4, 17.9, 1.1, 1.1, trim)
    for y in (-4.6, 4.6):
        arch(f"MD_niche_trim_{y:+.0f}", y, 2.0, 12.4, 15.4, -0.3, BAY_F + 0.34, trim, axis="x")
        arch(f"MD_niche_ink_{y:+.0f}", y, 1.3, 12.7, 14.9, 0.0, BAY_F + 0.40, ink, axis="x")
    # ornament panel field between portal and window sill
    box("MD_panel", -0.35, 0, 9.4, 10.5, 2.1, 8.6, trim)

    towers = []
    for sy, tall in ((-1, False), (1, True)):
        cy = sy * TOWER_CY
        tag = "n" if sy > 0 else "s"
        shaft = box(f"MD_tower_{tag}", -TOWER_A / 2, cy, 0, CORNICE - 0.8, TOWER_A, TOWER_A, cream)
        bevel(shaft)
        box(f"MD_tcorn_{tag}", -TOWER_A / 2, cy, CORNICE - 0.8, CORNICE + 0.1, TOWER_A + 0.7, TOWER_A + 0.7, trim)
        # paired slit windows on the street face of the shaft
        for dy in (-1.1, 1.1):
            lit_box(f"MD_slit_{tag}", 0.04, cy + dy, 12.0, 14.2, 0.24, 0.5, ink, "x+")
        # side portals at the tower bases
        arch(f"MD_sportal_trim_{tag}", cy, 3.6, FLOOR, 7.6, -0.8, 0.60, trim, axis="x")
        arch(f"MD_sportal_ink_{tag}", cy, 2.4, FLOOR, 6.8, -0.4, 0.66, ink, axis="x")
        box(f"MD_sportal_ped_{tag}", 0.42, cy, 7.6, 8.5, 0.66, 3.0, trim)
        towers.append((sy, cy, tall))

    # ---- south tower top: one open cupola stage + verdigris dome (~28 m)
    _, cy, _ = towers[0][0], towers[0][1], towers[0][2]
    stage = box("MD_s_cupola", -TOWER_A / 2, cy, CORNICE + 0.1, 23.7, 4.9, 4.9, cream)
    bevel(stage)
    for a in ("x", "y"):
        arch(f"MD_s_arch_{a}", cy if a == "x" else -TOWER_A / 2, 1.8, 19.9, 23.0,
             (-TOWER_A / 2 - 2.6) if a == "x" else (cy - 2.6),
             (-TOWER_A / 2 + 2.6) if a == "x" else (cy + 2.6), "Toy_ink", axis=a)
    arch("MD_s_glow_x", cy, 1.5, 20.2, 22.7, -TOWER_A / 2 - 2.64, -TOWER_A / 2 + 2.64, "Toy_gold_Glow", axis="x")
    for cxx, cyy in ((-TOWER_A / 2 - 2.2, cy - 2.2), (-TOWER_A / 2 - 2.2, cy + 2.2),
                     (-TOWER_A / 2 + 2.2, cy - 2.2), (-TOWER_A / 2 + 2.2, cy + 2.2)):
        cylinder("MD_s_urn", cxx, cyy, 23.7, 24.9, 0.30, trim, seg=8)
    box("MD_s_cap", -TOWER_A / 2, cy, 23.7, 24.2, 5.5, 5.5, trim)
    dome("MD_s_dome", -TOWER_A / 2, cy, 24.2, 2.45, 2.9, "Toy_verdigris")
    cylinder("MD_s_ball", -TOWER_A / 2, cy, 27.1, 27.75, 0.32, "Toy_gold", seg=8)
    cross("MD_s_cross", -TOWER_A / 2, cy, 27.75, 0.95, 0.55, "Toy_gold")

    # ---- north tower top: three diminishing stages + dome + cross (41 m)
    _, cy, _ = towers[1][0], towers[1][1], towers[1][2]
    cx = -TOWER_A / 2
    s1 = box("MD_n_stage1", cx, cy, CORNICE + 0.1, 26.2, 5.9, 5.9, cream)
    bevel(s1)
    for c in ((cx - 2.7, cy - 2.7), (cx - 2.7, cy + 2.7), (cx + 2.7, cy - 2.7), (cx + 2.7, cy + 2.7)):
        box("MD_n_pil1", c[0], c[1], CORNICE + 0.1, 26.0, 0.55, 0.55, trim)
    for a in ("x", "y"):
        arch(f"MD_n_arch1_{a}", cy if a == "x" else cx, 2.2, 20.2, 25.2,
             (cx - 3.1) if a == "x" else (cy - 3.1),
             (cx + 3.1) if a == "x" else (cy + 3.1), "Toy_ink", axis=a)
    arch("MD_n_glow1", cy, 1.9, 20.5, 24.9, cx - 3.16, cx + 3.16, "Toy_gold_Glow", axis="x")
    box("MD_n_balc1", cx + 2.95, cy, 20.2, 20.55, 0.9, 3.0, trim)
    box("MD_n_corn1", cx, cy, 26.2, 26.8, 6.6, 6.6, trim)
    s2 = box("MD_n_stage2", cx, cy, 26.8, 31.6, 4.7, 4.7, cream)
    bevel(s2)
    for a in ("x", "y"):
        arch(f"MD_n_arch2_{a}", cy if a == "x" else cx, 1.7, 27.6, 30.9,
             (cx - 2.5) if a == "x" else (cy - 2.5),
             (cx + 2.5) if a == "x" else (cy + 2.5), "Toy_ink", axis=a)
    arch("MD_n_glow2", cy, 1.45, 27.8, 30.6, cx - 2.56, cx + 2.56, "Toy_gold_Glow", axis="x")
    box("MD_n_corn2", cx, cy, 31.6, 32.1, 5.4, 5.4, trim)
    ngon_drum("MD_n_lantern", cx, cy, 32.1, 35.2, 1.75, cream, seg=8, rot=math.pi / 8)
    for a in ("x", "y"):
        arch(f"MD_n_arch3_{a}", cy if a == "x" else cx, 0.9, 32.7, 34.7,
             (cx - 1.9) if a == "x" else (cy - 1.9),
             (cx + 1.9) if a == "x" else (cy + 1.9), "Toy_ink", axis=a)
    ngon_drum("MD_n_corn3", cx, cy, 35.2, 35.6, 2.1, trim, seg=8, rot=math.pi / 8)
    dome("MD_n_dome", cx, cy, 35.6, 1.95, 2.9, "Toy_verdigris")
    cylinder("MD_n_ball", cx, cy, 38.5, 39.1, 0.3, "Toy_gold", seg=8)
    cross("MD_n_cross", cx, cy, 39.1, H_TOTAL - 39.1, 1.1, "Toy_gold")

    # ---- nave, aisles, clerestory
    gable_wall("MD_nave", NAVE_X0, NAVE_X1, 0, NAVE_HW, 0, NAVE_EAVE, NAVE_RIDGE, cream)
    gable_roof("MD_nave_roof", NAVE_X0 - 0.4, NAVE_X1 + 0.2, 0, NAVE_HW, 0.5,
               NAVE_EAVE, NAVE_RIDGE, 0.45, "Toy_ioorange")
    box("MD_nave_ridge", (NAVE_X0 + NAVE_X1) / 2, 0, NAVE_RIDGE + 0.35, NAVE_RIDGE + 0.7,
        NAVE_X1 - NAVE_X0 + 0.4, 0.55, "Toy_brick")
    for sy in (-1, 1):
        aisle = box(f"MD_aisle_{ 'n' if sy>0 else 's'}", (NAVE_X0 + NAVE_X1) / 2, sy * (NAVE_HW + (AISLE_HW - NAVE_HW) / 2),
                    0, AISLE_H - 0.3, NAVE_X1 - NAVE_X0, AISLE_HW - NAVE_HW, cream)
        bevel(aisle)
        # parapet + white deck (the flat roofs read white from above)
        box(f"MD_aisle_par_{sy}", (NAVE_X0 + NAVE_X1) / 2, sy * (NAVE_HW + (AISLE_HW - NAVE_HW) / 2),
            AISLE_H - 0.3, AISLE_H + 0.25, NAVE_X1 - NAVE_X0 + 0.3, AISLE_HW - NAVE_HW + 0.3, trim)
        # roof furniture: two low skylight strips per deck (style bible s10)
        for i in (0, 1):
            lit_box(f"MD_aisle_sky_{sy}_{i}", NAVE_X0 + 8 + i * 12, sy * (NAVE_HW + (AISLE_HW - NAVE_HW) / 2),
                    AISLE_H + 0.25, AISLE_H + 0.65, 4.5, 1.6, "Toy_glass", "z+")
        for i in range(5):
            wx = NAVE_X1 - 3.4 - i * 5.6
            # clerestory sits clear of the aisle parapet (11.45) so the whole
            # arch reads instead of being cut by the roof line
            lit_arch(f"MD_cler_{sy}_{i}", wx, 1.9, 11.75, 13.7, sy * (NAVE_HW - 0.3), sy * (NAVE_HW + 0.06), axis="y")
            lit_arch(f"MD_aisw_{sy}_{i}", wx, 1.6, 4.6, 8.4, sy * (AISLE_HW - 0.3), sy * (AISLE_HW + 0.05), axis="y")

    # ---- transept (cross gable), crossing dome, apse, south chapel wing
    gable_wall("MD_transept", TRAN_Y0, TRAN_Y1, (TRAN_X0 + TRAN_X1) / 2, (TRAN_X1 - TRAN_X0) / 2,
               0, NAVE_EAVE, NAVE_RIDGE, cream, axis="y")
    gable_roof("MD_transept_roof", TRAN_Y0 - 0.4, TRAN_Y1 + 0.4, (TRAN_X0 + TRAN_X1) / 2,
               (TRAN_X1 - TRAN_X0) / 2, 0.5, NAVE_EAVE, NAVE_RIDGE, 0.45, "Toy_ioorange", axis="y")
    box("MD_transept_ridge", (TRAN_X0 + TRAN_X1) / 2, (TRAN_Y0 + TRAN_Y1) / 2, NAVE_RIDGE + 0.35,
        NAVE_RIDGE + 0.7, 0.55, TRAN_Y1 - TRAN_Y0 + 0.8, "Toy_brick")
    for sy, yy in ((-1, TRAN_Y0), (1, TRAN_Y1)):
        lit_arch(f"MD_tran_win_{sy}", (TRAN_X0 + TRAN_X1) / 2, 2.4, 8.8, 13.0,
                 yy - sy * 0.3, yy + sy * 0.06, axis="y")

    drum = ngon_drum("MD_dome_drum", DOME_C[0], DOME_C[1], 15.5, 19.4, 5.8, cream, seg=8, rot=math.pi / 8)
    bevel(drum, width=0.1)
    # faceted octagonal tiled dome: lofted rings to a lantern platform
    for k, (z0, r0, z1, r1) in enumerate(
        (
            (19.4, 6.1, 21.6, 5.3),
            (21.6, 5.3, 23.6, 3.6),
            (23.6, 3.6, 25.0, 1.55),
        )
    ):
        ngon_drum(f"MD_dome_t{k}", DOME_C[0], DOME_C[1], z0, z1, r0, "Toy_ioorange", seg=8, r_top=r1, rot=math.pi / 8)
    ngon_drum("MD_dome_lantern", DOME_C[0], DOME_C[1], 25.0, 27.0, 1.15, cream, seg=8, rot=math.pi / 8)
    ngon_drum("MD_dome_cap", DOME_C[0], DOME_C[1], 27.0, 28.2, 1.35, "Toy_ioorange", seg=8, r_top=0.2, rot=math.pi / 8)
    cross("MD_dome_cross", DOME_C[0], DOME_C[1], 28.2, 1.4, 0.7, "Toy_gold")
    for i in range(4):  # small arched drum windows on the cardinal faces
        a = math.pi / 2 * i
        wx = DOME_C[0] + 5.5 * math.cos(a)
        wy = DOME_C[1] + 5.5 * math.sin(a)
        if abs(math.cos(a)) > 0.5:  # face normal along local x: extrude in x
            lit_arch(f"MD_drum_win_{i}", wy, 1.4, 16.6, 18.6, wx - 0.55, wx + 0.55, axis="x")
        else:  # face normal along local y: extrude in y
            lit_arch(f"MD_drum_win_{i}", wx, 1.4, 16.6, 18.6, wy - 0.55, wy + 0.55, axis="y")

    half_drum("MD_apse", APSE_X, 0, 0, 11.5, APSE_R, cream)
    half_dome("MD_apse_dome", APSE_X, 0, 11.5, APSE_R + 0.3, 3.7, "Toy_ioorange")

    wing = box("MD_wing_s", -46.0, -17.2, 0, 9.2, 12.0, 8.6, cream)
    bevel(wing)
    box("MD_wing_par", -46.0, -17.2, 9.2, 9.7, 12.3, 8.9, trim)
    for i in (0, 1):
        lit_arch(f"MD_wing_win_{i}", -49.0 + i * 6.0, 1.5, 3.6, 6.6, -21.2, -21.8, axis="y")

    # the facade block roof is seen from the app's downward camera: give it a
    # designed surface rather than a blank plane (style bible s10)
    for i, dy in enumerate((-4.6, 4.6)):
        box(f"MD_narthex_vent_{i}", -4.4, dy, CORNICE, CORNICE + 0.9, 2.6, 2.2, trim)
        box(f"MD_narthex_cap_{i}", -4.4, dy, CORNICE + 0.9, CORNICE + 1.1, 3.0, 2.6, "Toy_roofd")
    box("MD_narthex_deck", -4.6, 0, CORNICE - 0.05, CORNICE + 0.12, 6.4, 12.0, "Toy_stone")

    # ---- grand stair with scroll cheeks + facade uplight glow strips
    # Six treads marching east off the landing; each is a slab from grade to
    # its own tread height, so the stack is solid with no hidden shells.
    N_STEP = 6
    TREAD = 1.05
    for i in range(N_STEP):
        z1 = FLOOR * (N_STEP - i) / N_STEP
        depth = TREAD * (i + 1) + 0.6
        box(f"MD_step_{i}", depth / 2, 0, 0, z1, depth, FACADE_W, "Toy_stone")
    for sy in (-1, 1):
        p = [(0.0, 0.0), (N_STEP * TREAD + 0.6, 0.0), (N_STEP * TREAD + 0.6, 0.85), (0.0, FLOOR + 1.1)]
        prism(f"MD_cheek_{sy}", p, sy * (FACADE_W / 2 - 0.05), sy * (FACADE_W / 2 + 0.85), cream, axis="y")
        dome(f"MD_cheek_ball_{sy}", N_STEP * TREAD + 0.2, sy * (FACADE_W / 2 + 0.4), 0.85, 0.52, 0.52,
             "Toy_stone", seg=10, rings=4)
    for cy, w in ((0, 9.6), (-TOWER_CY, 6.0), (TOWER_CY, 6.0)):
        box(f"MD_uplight_{cy:+.0f}", 0.02 if cy == 0 else 0.02, cy, 2.5, 2.85, 0.5, w, "Toy_white_Glow")


# ------------------------------------------------------------ adobe chapel


def build_adobe():
    set_frame(ADO_ORIGIN, ADO_YAW)
    cream, trim, ink = "Toy_cream", "Toy_trim", "Toy_ink"

    body = gable_wall("AD_body", -ADO_LEN, 0, 0, ADO_HW, 0, ADO_EAVE, ADO_RIDGE, cream)
    bevel(body, width=0.1)
    # dark soffit prism just under the tile roof: the deep-eave shadow
    gable_roof("AD_soffit", -ADO_LEN - 0.55, 1.0, 0, ADO_HW, 0.72, ADO_EAVE - 0.14, ADO_RIDGE - 0.14, 0.12, ink)
    gable_roof("AD_roof", -ADO_LEN - 0.6, 1.1, 0, ADO_HW, 0.85, ADO_EAVE, ADO_RIDGE, 0.4, "Toy_ioorange")
    box("AD_ridge", -ADO_LEN / 2 + 0.25, 0, ADO_RIDGE + 0.3, ADO_RIDGE + 0.62, ADO_LEN + 1.7, 0.5, "Toy_brick")

    # battered corner buttresses on the street front
    for sy in (-1, 1):
        vs = []
        for z, s in ((0.0, 1.0), (4.4, 0.62)):
            for dx, dy in ((-0.75, -0.75), (0.75, -0.75), (0.75, 0.75), (-0.75, 0.75)):
                vs.append((*tf(0.35 + dx * s, sy * 5.45 + dy * s), z))
        faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        new_mesh(f"AD_buttress_{sy}", vs, faces, cream)

    # four facade columns in two pairs, on plinths, carrying the balcony
    for y in (-4.35, -2.85, 2.85, 4.35):
        box(f"AD_plinth_{y:+.2f}", 0.65, y, 0, 0.95, 1.05, 1.05, cream)
        cylinder(f"AD_col_{y:+.2f}", 0.65, y, 0.95, 4.35, 0.30, cream, seg=10)
    box("AD_entab", 0.62, 0, 4.35, 4.85, 1.15, 10.4, cream)
    box("AD_balcony", 0.65, 0, 4.85, 5.05, 1.5, 10.9, ink)
    box("AD_rail_top", 1.28, 0, 5.8, 5.98, 0.12, 10.6, ink)
    box("AD_rail_bot", 1.28, 0, 5.12, 5.24, 0.12, 10.6, ink)
    for i in range(9):
        y = -4.8 + i * 1.2
        box(f"AD_post_{i}", 1.28, y, 5.05, 5.8, 0.09, 0.09, ink)
    for sy in (-1, 1):
        box(f"AD_rail_side_{sy}", 0.64, sy * 5.3, 5.5, 5.66, 1.3, 0.12, ink)

    # Roman-arch doorway with molded surround + brick steps
    arch("AD_door_trim", 0, 3.1, 0.5, 4.05, -0.6, 0.22, trim, axis="x")
    arch("AD_door_ink", 0, 2.3, 0.6, 3.7, -0.7, 0.10, ink, axis="x")
    box("AD_door_ped", 0.08, 0, 4.05, 4.35, 0.22, 2.5, trim)
    for i in range(3):
        box(f"AD_bstep_{i}", 0.5 + (i + 1) * 0.42, 0, 0, 0.55 - i * 0.18, 0.85, 3.5, "Toy_brick")

    # belfry level: four pilasters, three arched bell openings, three bells
    for y in (-4.05, -1.35, 1.35, 4.05):
        box(f"AD_pil_{y:+.2f}", 0.18, y, 5.98, 8.45, 0.4, 0.5, cream)
        box(f"AD_pilcap_{y:+.2f}", 0.2, y, 8.45, 8.72, 0.44, 0.62, trim)
    for k, y in enumerate((-2.7, 0.0, 2.7)):
        arch(f"AD_bell_arch_{k}", y, 1.5, 6.15, 8.35, -0.5, 0.12, ink, axis="x")
        arch(f"AD_bell_glow_{k}", y, 1.3, 6.3, 8.15, -0.45, 0.20, "Toy_gold_Glow", axis="x")
        box(f"AD_bell_bar_{k}", 0.05, y, 7.6, 7.75, 0.5, 1.3, ink)
        d = dome(f"AD_bell_{k}", 0.05, y, 6.9, 0.34, 0.62, "Toy_rust", seg=10, rings=4)
        d.name = f"AD_bell_{k}"
    # stepped rake moldings flanking the belfry (the zigzag corbels)
    for sy in (-1, 1):
        for j in range(3):
            yy = sy * (4.9 - j * 0.0)
            box(f"AD_rake_{sy}_{j}", 0.12, sy * (5.0 - j * 1.05), 6.5 + j * 0.85, 6.9 + j * 0.85, 0.35, 0.85, trim)

    # chunky ridge cross on the street gable
    box("AD_cross_v", 0.3, 0, ADO_RIDGE + 0.55, ADO_RIDGE + 2.4, 0.18, 0.18, ink)
    box("AD_cross_h", 0.3, 0, ADO_RIDGE + 1.75, ADO_RIDGE + 1.93, 0.18, 1.1, ink)

    # sparse tiny flank windows
    for k, x in enumerate((-8.0, -18.0, -28.0)):
        lit_box(f"AD_swin_{k}", x, -ADO_HW + 0.06 - 0.3, 3.9, 5.1, 1.0, 0.7, ink, "y-")
    lit_box("AD_nwin", -20.0, ADO_HW - 0.06 + 0.3 - 0.6, 3.9, 5.1, 1.0, 0.7, ink, "y+")


# --------------------------------------------------------- recentre + report


def recentre():
    """Shift everything so the combined bbox base centre is the origin."""
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for o in objs:
        for v in o.data.vertices:
            for i in range(3):
                mn[i] = min(mn[i], v.co[i])
                mx[i] = max(mx[i], v.co[i])
    cx, cy = (mn.x + mx.x) / 2, (mn.y + mx.y) / 2
    shift = Matrix.Translation((-cx, -cy, 0))
    for o in objs:
        o.data.transform(shift)
    # the anchor is the WGS84 point now under the origin
    ax = CENTROID_X + cx
    az = CENTROID_Z - cy
    lon = LON0 + ax / (111320 * math.cos(math.radians(LAT0)))
    lat = LAT0 - az / 110540
    print(f"[build] recentred by ({-cx:.3f}, {-cy:.3f})")
    print(f"[build] manifest anchor: [{lon:.7f}, {lat:.7f}]")
    return lon, lat


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

    bpy.ops.wm.read_factory_settings(use_empty=True)
    build_basilica()
    build_adobe()
    recentre()
    report()

    blend = os.path.join(out, "mission-dolores.blend")
    glb = os.path.join(out, "mission-dolores.glb")
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
