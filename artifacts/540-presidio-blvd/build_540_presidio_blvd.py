"""Deterministic Blender build of the SF-SIM miniature 540 Presidio Boulevard.

    blender -b --python build_540_presidio_blvd.py -- [--out DIR]

Writes 540-presidio-blvd.blend and 540-presidio-blvd.glb next to this file (or
into --out). Geometry is authored in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = XY bbox centre (the manifest anchor is the
footprint OBB centre shifted by the same vector, printed by report()), min Z = 0,
chimney cap exactly 11.5 m so the loader's scale lands on 1.000.

Design (see REFERENCE.md for the sources behind every number):

* a 1912 Colonial Revival officers' quarters in the Presidio of San Francisco,
  built for 4th Cavalry officers' families and now a two-unit residence. One of
  a short row of four near-identical houses (540 / 541 / 542 / 543) on a wooded
  rise above Presidio Boulevard;
* the recognition is almost entirely ROOF: a low-pitched hipped tile roof, red
  against cream, with an exaggerated 0.9 m overhang so the eave shadow line
  survives at city distance, and two terracotta chimneys breaking the ridge.
  From the app's downward camera that is the building;
* the one projecting mass is the full-width covered porch on the EAST front —
  mapped in OSM as a 9.8 x 1.74 m bump-out — with five square columns on a
  solid rail, the arched entry behind it, and steps down to the walk that
  descends to the boulevard;
* a small service bay on the west (rear) elevation, also mapped in OSM;
* night state: four lit windows split across two elevations plus a warm lantern
  under the porch soffit. Glow surfaces are thin panes proud of the opaque
  glazing — the app renders _Glow in a separate layer that is ~12% alpha by day,
  so a primary surface must never be authored as glow.

Authoring frame: geometry is laid out in a local (u, v) frame aligned with the
house — u across the plan, positive toward the porch/east front; v along the
plan, positive toward the north end — and mapped to world x/y by to_world().
The plan sits +6.49 deg CCW off the world axes, so the axis-aligned XY bounding
box is wider than the building. That is expected, not a scale error.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# Plan yaw, measured as the minimum-area oriented bounding box over OSM
# way/288360343 reprojected into the project's local tangent frame. +6.49 deg
# CCW: local +u bears 83.51 deg true (the porch front), local +v bears 353.51.
YAW = math.radians(6.49)

# Local extents, metres, relative to the footprint OBB centre. Every number
# below is read straight off the de-yawed OSM polygon.
U_W, U_E = -5.94, 5.50          # main block across the plan: 11.44 m
V_S, V_N = -9.86, 9.86          # main block along the plan: 19.72 m
U_PORCH = 7.24                  # porch face: 1.74 m proud of the east wall
V_PORCH_S, V_PORCH_N = -4.80, 5.00   # porch length: 9.80 m
U_BAY = -7.24                   # service bay face: 1.31 m proud of the west wall
V_BAY_S, V_BAY_N = -1.77, 2.19  # service bay length: 3.96 m

Z_PLINTH = 1.10   # raised basement/plinth to the first floor
Z_FLOOR2 = 4.80   # second floor line (10' 6" ground-floor ceiling plus structure)
Z_EAVE = 8.00     # OSM height=8 on all four houses of the row, read as the EAVE.
                  # It reconciles exactly with 1.10 + 3.70 + 3.20; see REFERENCE.
Z_RIDGE = 10.50   # 4.5:12 over the 6.47 m half-span from eave edge to ridge
Z_CREST = 11.50   # chimney caps — the bbox top, and the manifest targetHeightM

EAVE_OVERHANG = 0.75  # exaggerated (real is ~0.6): the eave shadow is the cue
FASCIA_D = 0.35       # deep enough that the roof edge reads as a drawn line

Z_PORCH_EAVE = 3.60
PORCH_OVERHANG = 0.5
PORCH_COLS = 5
COL_SEC = 0.30
Z_RAIL = 2.05

Z_BAY_EAVE = 5.20
BAY_OVERHANG = 0.40

CHIMNEY_SEC = 0.90
V_CHIMNEY = 3.20      # both chimneys sit on the ridge run (|v| <= 4.14)

WIN_W, WIN_H = 1.10, 1.90
WIN_RECESS = 0.12
Z_SILL_LO, Z_SILL_HI = 2.20, 5.30

STEPS = 4
STEP_W = 2.60

PALETTE_HEX = {
    "Toy_cream": "f2ede3",     # cream stucco — the row's documented finish
    "Toy_stone": "d9d2c2",     # plinth, entry steps
    "Toy_red": "c4453c",       # tile roof, matching artifacts/1008-general-kennedy
    "Toy_trim": "f3efe6",      # eave fascia, storey band, columns, rail, sills
    "Toy_glass": "2a4d73",
    "Toy_brick": "c96f4a",     # terracotta chimneys — deliberately NOT Toy_red,
                               # so the stacks read as separate objects from above
    "Toy_ink": "3a3530",       # the front door
    "Toy_mint": "8fd0a8",      # two clipped hedges, the only landscaping
    "Toy_glass_Glow": "6f95b8",  # lit panes: LIGHTER than the glass behind them
    "Toy_gold_Glow": "caa64a",   # the porch lantern
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


# ----------------------------------------------------------------- transforms


def to_world(u, v):
    """Local house frame -> world (x east, y north). A pure CCW rotation, so a
    CCW polygon in (u, v) stays CCW in (x, y) and outward normals stay outward."""
    c, s = math.cos(YAW), math.sin(YAW)
    return (u * c - v * s, u * s + v * c)


def rect_uv(u0, u1, v0, v1):
    """CCW rectangle in the local frame."""
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]


# --------------------------------------------------------------- mesh helpers


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
    """Miniature-style edge softening (style bible s.4). The offset is capped at
    a third of the object's thinnest dimension: the rail, the fascia and the
    columns are thin, and a flat 0.12 m bevel on those collapses opposing
    profiles into zero-area slivers even with clamp_overlap."""
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


def prism_uv(name, poly_uv, z0, z1, mat):
    """Closed extrusion of a CCW local-frame polygon (walls + both caps)."""
    poly = [to_world(u, v) for u, v in poly_uv]
    n = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    return new_mesh(name, verts, faces, [mat])


def hip_roof(name, u0, u1, v0, v1, z_eave, z_ridge, mat, ridge_along_u=True):
    """Closed hipped roof solid over the eave rectangle (u0..u1, v0..v1).

    The ridge is centred on the short axis and shortened at both ends by half
    the short span, which is what puts the hips at 45 deg in plan — the geometry
    a real hipped roof has, modelled as real geometry rather than faked with a
    bevelled plane (the app's camera looks down; the roof IS a facade). The base
    cap keeps the solid closed so the signed-volume normals test is meaningful."""
    span_u, span_v = u1 - u0, v1 - v0
    if ridge_along_u:
        inset = span_v / 2.0
        rc = (v0 + v1) / 2.0
        r0, r1 = (u0 + inset, rc), (u1 - inset, rc)
    else:
        inset = span_u / 2.0
        rc = (u0 + u1) / 2.0
        r0, r1 = (rc, v0 + inset), (rc, v1 - inset)

    corners = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
    verts = [to_world(u, v) + (z_eave,) for u, v in corners]
    verts += [to_world(*r0) + (z_ridge,), to_world(*r1) + (z_ridge,)]
    A, B, C, D, R0, R1 = range(6)

    if ridge_along_u:
        faces = [(A, B, R1, R0), (C, D, R0, R1), (B, C, R1), (D, A, R0)]
    else:
        faces = [(B, C, R1, R0), (D, A, R0, R1), (A, B, R0), (C, D, R1)]
    faces.append((D, C, B, A))  # base cap
    return new_mesh(name, verts, faces, [mat])


def band_uv(name, u0, u1, v0, v1, z0, z1, thickness, mat):
    """Closed rectangular band (a picture frame in plan) around the rectangle,
    growing outward by `thickness`. Used for the eave fascia and storey band."""
    t = thickness
    inner = rect_uv(u0, u1, v0, v1)
    outer = rect_uv(u0 - t, u1 + t, v0 - t, v1 + t)
    loops = [(inner, z0), (outer, z0), (outer, z1), (inner, z1)]
    verts = []
    for loop, z in loops:
        verts.extend([to_world(u, v) + (z,) for u, v in loop])
    n = 4
    faces = []
    for k in range(4):
        a0, b0 = k * n, ((k + 1) % 4) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])



def cap_bar(name, p0, p1, width, thick, mat):
    """A thin box swept along the 3D segment p0 -> p1, centred on it.

    Used for the ridge and hip tiles. Half the section sits above the roof
    plane and half below, so the bar reads as a raised capping course without
    leaving a gap under it — which is exactly how ridge and hip tiles sit on a
    real tile roof, and what stops a hipped roof reading as one flat plate from
    the app's downward camera (style bible s.10)."""
    a = Vector(p0)
    b = Vector(p1)
    d = (b - a).normalized()
    side = d.cross(Vector((0.0, 0.0, 1.0)))
    side = side.normalized() if side.length > 1e-6 else Vector((1.0, 0.0, 0.0))
    up = side.cross(d).normalized()
    hw, ht = width / 2.0, thick / 2.0
    verts = []
    for base in (a, b):
        for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            verts.append(tuple(base + side * (sx * hw) + up * (sz * ht)))
    faces = [(i, (i + 1) % 4, 4 + (i + 1) % 4, 4 + i) for i in range(4)]
    faces.append((3, 2, 1, 0))
    faces.append((4, 5, 6, 7))
    return new_mesh(name, verts, faces, [mat])


# --------------------------------------------------------------------- build


def make_material(name):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = PALETTE[name] + (1.0,)
    bsdf.inputs["Roughness"].default_value = 0.85
    if "Metallic" in bsdf.inputs:
        bsdf.inputs["Metallic"].default_value = 0.0
    if name.endswith("_Glow") and "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = PALETTE[name] + (1.0,)
        bsdf.inputs["Emission Strength"].default_value = 1.0
    return mat


def window(name, axis, wall, side, centre, z_sill, mats, lit=False):
    """One recessed window with a proud sill, and optionally a lit pane.

    `axis` is "u" for a window in a u-normal wall (the east front / west rear)
    or "v" for one in a v-normal wall (the north / south ends). `wall` is that
    wall's coordinate, `side` is +1 if the wall faces the positive direction,
    `centre` is the position along the wall."""
    out = wall + side * 0.02
    inn = wall - side * WIN_RECESS
    lo, hi = (inn, out) if side > 0 else (out, inn)
    a0, a1 = centre - WIN_W / 2.0, centre + WIN_W / 2.0
    sill_lo, sill_hi = (wall, wall + side * 0.10) if side > 0 else (wall + side * 0.10, wall)
    glow_lo, glow_hi = (out, out + side * 0.04) if side > 0 else (out + side * 0.04, out)

    def r(lowv, highv, b0, b1):
        return rect_uv(lowv, highv, b0, b1) if axis == "u" else rect_uv(b0, b1, lowv, highv)

    prism_uv(f"{name}_fill", r(lo, hi, a0, a1), z_sill, z_sill + WIN_H, mats["Toy_glass"])
    prism_uv(
        f"{name}_sill",
        r(sill_lo, sill_hi, a0 - 0.10, a1 + 0.10),
        z_sill - 0.12,
        z_sill,
        mats["Toy_trim"],
    )
    if lit:
        prism_uv(
            f"{name}_glow",
            r(glow_lo, glow_hi, a0 + 0.05, a1 - 0.05),
            z_sill + 0.05,
            z_sill + WIN_H - 0.05,
            mats["Toy_glass_Glow"],
        )


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"
    mats = {name: make_material(name) for name in PALETTE_HEX}

    # ---------------------------------------------------------------- plinth
    # The raised basement the house stands on, in a value darker than the stucco
    # so it reads as a base at any distance. It follows each mass's own
    # footprint: one continuous slab under all three would read as a terrace,
    # which this house does not have.
    prism_uv(
        "plinth_body",
        rect_uv(U_W - 0.15, U_E + 0.15, V_S - 0.15, V_N + 0.15),
        0.0,
        Z_PLINTH,
        mats["Toy_stone"],
    )
    prism_uv(
        "plinth_bay",
        rect_uv(U_BAY - 0.12, U_W, V_BAY_S - 0.12, V_BAY_N + 0.12),
        0.0,
        Z_PLINTH,
        mats["Toy_stone"],
    )

    # ------------------------------------------------------------ main block
    # 11.44 x 19.72 m, two storeys of cream stucco. This volume is the building.
    prism_uv("body", rect_uv(U_W, U_E, V_S, V_N), Z_PLINTH, Z_EAVE, mats["Toy_cream"])

    # The floor line, as a thin band proud of the wall: it splits a 6.9 m blank
    # wall into two readable storeys without a single extra window.
    band_uv("storey_band", U_W, U_E, V_S, V_N, Z_FLOOR2 - 0.09, Z_FLOOR2 + 0.09, 0.06,
            mats["Toy_trim"])

    # ----------------------------------------------------------- service bay
    prism_uv(
        "service_bay",
        rect_uv(U_BAY, U_W + 0.10, V_BAY_S, V_BAY_N),
        Z_PLINTH,
        Z_BAY_EAVE,
        mats["Toy_cream"],
    )
    bay_e = (U_BAY - BAY_OVERHANG, U_W + 0.10, V_BAY_S - BAY_OVERHANG, V_BAY_N + BAY_OVERHANG)
    hip_roof("roof_bay", *bay_e, Z_BAY_EAVE, Z_BAY_EAVE + 0.62, mats["Toy_red"],
             ridge_along_u=False)

    # ------------------------------------------------------------ the porch
    # Full width of the east front, five square columns on a solid rail, its own
    # shallow hipped roof tucking under the main eave. This is the one mass that
    # says "officers' quarters" rather than "house".
    prism_uv(
        "porch_deck",
        rect_uv(U_E, U_PORCH, V_PORCH_S, V_PORCH_N),
        0.0,
        Z_PLINTH,
        mats["Toy_stone"],
    )
    u_col = U_PORCH - COL_SEC / 2.0 - 0.12
    span0, span1 = V_PORCH_S + 0.55, V_PORCH_N - 0.55
    h = COL_SEC / 2.0
    for k in range(PORCH_COLS):
        vc = span0 + (span1 - span0) * k / (PORCH_COLS - 1)
        prism_uv(
            f"porch_col_{k}",
            rect_uv(u_col - h, u_col + h, vc - h, vc + h),
            Z_PLINTH,
            Z_PORCH_EAVE,
            mats["Toy_trim"],
        )
    # Solid rail between the columns, broken by the entry gap in the middle.
    v_gap = (V_PORCH_S + V_PORCH_N) / 2.0
    for k, (v0, v1) in enumerate(
        ((V_PORCH_S, v_gap - STEP_W / 2.0 - 0.2), (v_gap + STEP_W / 2.0 + 0.2, V_PORCH_N))
    ):
        prism_uv(
            f"porch_rail_{k}",
            rect_uv(u_col - 0.10, u_col + 0.10, v0, v1),
            Z_PLINTH,
            Z_RAIL,
            mats["Toy_trim"],
        )
    porch_e = (
        U_E - 0.20,
        U_PORCH + PORCH_OVERHANG,
        V_PORCH_S - PORCH_OVERHANG,
        V_PORCH_N + PORCH_OVERHANG,
    )
    hip_roof("roof_porch", *porch_e, Z_PORCH_EAVE, Z_PORCH_EAVE + 0.45, mats["Toy_red"],
             ridge_along_u=False)
    band_uv("fascia_porch", porch_e[0], porch_e[1], porch_e[2], porch_e[3],
            Z_PORCH_EAVE - 0.22, Z_PORCH_EAVE, 0.08, mats["Toy_trim"])
    # The porch roof gets its ridge tile too, so it reads as the same tile roof
    # as the main hip rather than as a painted awning.
    p_inset = (porch_e[1] - porch_e[0]) / 2.0
    u_pr = (porch_e[0] + porch_e[1]) / 2.0
    cap_bar(
        "tile_ridge_porch",
        to_world(u_pr, porch_e[2] + p_inset) + (Z_PORCH_EAVE + 0.45,),
        to_world(u_pr, porch_e[3] - p_inset) + (Z_PORCH_EAVE + 0.45,),
        0.26,
        0.14,
        mats["Toy_brick"],
    )

    # The entry: a dark door in the east wall, behind the porch, and the warm
    # lantern above it. The lantern is the hero glow and it hangs UNDER the
    # porch roof solid, so it always has body geometry directly behind it.
    prism_uv(
        "front_door",
        rect_uv(U_E - 0.14, U_E + 0.02, v_gap - 0.70, v_gap + 0.70),
        Z_PLINTH,
        Z_PLINTH + 2.40,
        mats["Toy_ink"],
    )
    prism_uv(
        "glow_lantern",
        rect_uv(U_E + 0.55, U_E + 0.95, v_gap - 0.22, v_gap + 0.22),
        Z_PORCH_EAVE - 0.36,
        Z_PORCH_EAVE - 0.24,
        mats["Toy_gold_Glow"],
    )

    # ------------------------------------------------------------ entry steps
    for k in range(STEPS):
        rise = Z_PLINTH / STEPS
        prism_uv(
            f"step_{k}",
            rect_uv(
                U_PORCH + (STEPS - 1 - k) * 0.34,
                U_PORCH + 1.40,
                v_gap - STEP_W / 2.0,
                v_gap + STEP_W / 2.0,
            ),
            0.0,
            (k + 1) * rise,
            mats["Toy_stone"],
        )

    # -------------------------------------------------------------- windows
    # Sixteen windows, symmetric on the ends, weighted to the front. Four are
    # lit, split between the east front and the north end so the night state is
    # not invisible from half the camera's orbit.
    for k, vc in enumerate((-6.6, -2.2, 2.2, 6.6)):
        window(f"win_e_hi_{k}", "u", U_E, +1, vc, Z_SILL_HI, mats, lit=(k in (1, 2)))
    for k, vc in enumerate((-6.6, 6.6)):
        window(f"win_e_lo_{k}", "u", U_E, +1, vc, Z_SILL_LO, mats)
    for k, vc in enumerate((-5.6, 0.0, 5.6)):
        window(f"win_w_hi_{k}", "u", U_W, -1, vc, Z_SILL_HI, mats)
    for k, vc in enumerate((-5.6, 5.6)):
        window(f"win_w_lo_{k}", "u", U_W, -1, vc, Z_SILL_LO, mats)
    for k, uc in enumerate((-3.0, 2.6)):
        window(f"win_n_hi_{k}", "v", V_N, +1, uc, Z_SILL_HI, mats, lit=(k == 0))
        window(f"win_n_lo_{k}", "v", V_N, +1, uc, Z_SILL_LO, mats, lit=(k == 1))
        window(f"win_s_hi_{k}", "v", V_S, -1, uc, Z_SILL_HI, mats)
        window(f"win_s_lo_{k}", "v", V_S, -1, uc, Z_SILL_LO, mats)

    # ---------------------------------------------------------- the main roof
    # Hipped, ridge along the long axis, 0.9 m overhang all round. At the app's
    # camera distance this red plane and its shadow line ARE the building.
    o = EAVE_OVERHANG
    roof_e = (U_W - o, U_E + o, V_S - o, V_N + o)
    hip_roof("roof_main", *roof_e, Z_EAVE, Z_RIDGE, mats["Toy_red"], ridge_along_u=False)
    band_uv("fascia_main", roof_e[0], roof_e[1], roof_e[2], roof_e[3],
            Z_EAVE - FASCIA_D, Z_EAVE, 0.10, mats["Toy_trim"])

    # Ridge and hip tiles, in the chimneys' terracotta. Five thin bars, ~250
    # triangles, and they are what turn a blank red plate into a tile roof from
    # above — the single highest-value detail on this building, because the
    # top view is the view the app's camera actually gets.
    inset = (roof_e[1] - roof_e[0]) / 2.0
    u_ridge = (roof_e[0] + roof_e[1]) / 2.0
    ridge_ends = ((u_ridge, roof_e[2] + inset), (u_ridge, roof_e[3] - inset))
    p_ridge = [to_world(*e) + (Z_RIDGE,) for e in ridge_ends]
    cap_bar("tile_ridge", p_ridge[0], p_ridge[1], 0.34, 0.18, mats["Toy_brick"])
    corners = (
        (roof_e[0], roof_e[2]), (roof_e[1], roof_e[2]),
        (roof_e[1], roof_e[3]), (roof_e[0], roof_e[3]),
    )
    for k, corner in enumerate(corners):
        end = p_ridge[0] if corner[1] < 0 else p_ridge[1]
        cap_bar(f"tile_hip_{k}", end, to_world(*corner) + (Z_EAVE,), 0.30, 0.16,
                mats["Toy_brick"])

    # ------------------------------------------------------------- chimneys
    # Two, on the ridge, exaggerated in section so they survive at thumbnail
    # size but NOT in height: the cap must land on 11.50 exactly (scale = 1.0).
    u_ridge = (roof_e[0] + roof_e[1]) / 2.0
    c = CHIMNEY_SEC / 2.0
    for k, vc in enumerate((-V_CHIMNEY, V_CHIMNEY)):
        prism_uv(
            f"chimney_{k}",
            rect_uv(u_ridge - c, u_ridge + c, vc - c, vc + c),
            Z_RIDGE - 1.60,
            Z_CREST,
            mats["Toy_brick"],
        )

    # --------------------------------------------------------------- hedges
    # The only landscaping, and the only scale cue: two clipped blocks flanking
    # the steps. Style bible s.15/s.16 on a 24-triangle budget.
    for k, vc in enumerate((v_gap - 2.30, v_gap + 2.30)):
        prism_uv(
            f"hedge_{k}",
            rect_uv(U_PORCH + 0.30, U_PORCH + 1.10, vc - 0.60, vc + 0.60),
            0.0,
            0.90,
            mats["Toy_mint"],
        )

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.12/2. Window fills, sills and glow panes are small and numerous — a
    # token softening or none at all is what keeps this well under the cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")) or obj.name == "glow_lantern":
            continue
        if obj.name.endswith("_sill") or obj.name.startswith(
            ("porch_col", "porch_rail", "storey_band", "fascia", "tile_")
        ):
            bevel(obj, width=0.05, segments=1)
        else:
            bevel(obj, width=0.12, segments=2)

    recentre()
    return scene


# Metres east / north from the footprint OBB centre to the model's XY bbox
# centre, filled in by recentre(). The manifest anchor is the OBB centre moved
# by this vector, so the origin sits at the bbox centre (contract rule 2) while
# the building still lands on its real footprint.
ANCHOR_SHIFT = [0.0, 0.0]


def recentre():
    """Move the model so its XY bounding-box centre is the origin.

    The house is not symmetric about its footprint centre — the porch, its roof
    overhang, the steps and the hedges all push east while only the service bay
    pushes west — so authoring on the true footprint leaves the bbox centre
    about a metre off. Shift the geometry and carry the same shift into the
    anchor, which keeps the building on its real footprint (AGENTS rule 5)."""
    mn = Vector((1e9, 1e9))
    mx = Vector((-1e9, -1e9))
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    for o in meshes:
        for v in o.data.vertices:
            for i in range(2):
                mn[i] = min(mn[i], v.co[i])
                mx[i] = max(mx[i], v.co[i])
    cx, cy = (mn[0] + mx[0]) / 2.0, (mn[1] + mx[1]) / 2.0
    ANCHOR_SHIFT[0], ANCHOR_SHIFT[1] = cx, cy
    for o in meshes:
        for v in o.data.vertices:
            v.co.x -= cx
            v.co.y -= cy


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
    lon0, lat0 = -122.4519267, 37.7966669
    lon_scale = 111320.0 * math.cos(math.radians(37.77))
    lon = lon0 + ANCHOR_SHIFT[0] / lon_scale
    lat = lat0 + ANCHOR_SHIFT[1] / 110540.0
    print(f"[build] footprint OBB centre lon/lat: {lon0} {lat0}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] plan yaw: +{math.degrees(YAW):.2f} deg CCW (porch front bears 83.51 deg true)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "540-presidio-blvd.blend")
    glb = os.path.join(out, "540-presidio-blvd.glb")
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
