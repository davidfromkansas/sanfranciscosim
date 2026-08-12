"""Deterministic Blender build of the SF-SIM miniature 1008 General Kennedy Avenue.

    blender -b --python build_1008_general_kennedy.py -- [--out DIR]

Writes 1008-general-kennedy.blend and 1008-general-kennedy.glb next to this file
(or into --out). Geometry is authored in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = footprint OBB centre (anchor
lon -122.4514885, lat 37.8007968), min Z = 0, chimney crest exactly 11.9 m.

Design (see REFERENCE.md for the sources behind every number):

* a 1930s concrete Mission Revival hospital ward in the Presidio's Letterman
  complex, rehabilitated 1994-96 as part of the Thoreau Center for
  Sustainability. One wing of a three-wing row (1007 / 1008 / 1009);
* the recognition rests on PROPORTION: a 55.1 x 12.0 m envelope whose main bar
  is only 9.38 m wide. Everything else is secondary. Do not fatten it;
* an unbroken red barrel-tile HIPPED roof with deep eaves and terracotta
  chimneys, which are the only vertical incident and set the 11.9 m crest;
* a wider hipped head block at the east end facing General Kennedy
  Avenue, carrying the exterior steel stair to an upper-floor landing;
* an open single-storey arcade stub at the west end where the ward meets the
  connecting corridor of the ward row;
* night state: a restrained scatter of lit windows (this is an office building
  that empties in the evening, not a working hospital) plus the doorway soffit.
  Glow surfaces are thin shells proud of the opaque glazing — the app renders
  _Glow in a separate layer that is ~12% alpha by day, so a primary surface must
  never be authored as glow.

Authoring frame: geometry is laid out in a local (u, v) frame aligned with the
ward — u along the long axis, positive toward the east head (bearing 116.85 deg
true); v across, positive toward the northeast flank (bearing 26.85 deg) — and
mapped to world x/y by to_world(). The building sits ~27 deg off the world axes,
so the axis-aligned XY bounding box is ~54.6 x 35.6 m even though the building
is 55.1 x 12.0 m. That is expected, not a scale error.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# Heading of the ward's long axis, measured from the footprint polygon cut out
# of DataSF LiDAR building 201006.0000207 and cross-checked against OSM way
# 288374440 (the two agree to within 0.03 m on the body width).
HEADING_LONG = 116.85   # +u, east head, faces General Kennedy Avenue
HEADING_CROSS = 26.85   # +v, northeast flank, faces the 1007 courtyard

_UL = math.radians(HEADING_LONG)
U_DIR = (math.sin(_UL), math.cos(_UL))
V_DIR = (-U_DIR[1], U_DIR[0])

# Local extents, metres, relative to the envelope's OBB centre.
# u: -27.57 (arcade end) .. +27.57 (head end)   -> 55.14 m, measured
# v:  -6.01 .. +6.01 at the head                -> 12.02 m, measured
U_WEST, U_EAST = -27.57, 27.57
U_ARCADE = -22.67       # arcade stub / ward bar junction
U_HEAD = 17.28          # ward bar / head block junction

# The bar is measurably off-centre within the envelope by ~60 mm. Keep it:
# it is what the two independent surveys say.
V_BAR0, V_BAR1 = -4.75, 4.63    # 9.38 m, measured
V_HEAD0, V_HEAD1 = -6.01, 6.01  # 12.02 m, measured

Z_PLINTH = 1.0          # raised base — also hides the terrain seam
Z_EAVE = 7.8            # inferred: plinth + two 3.4 m storeys. Bar and head
                        # share an eave line; the head reads taller because it
                        # is wider, so its cross-hip rises higher at the same
                        # pitch — which is what the aerial imagery shows.
Z_RIDGE = 10.9          # Overture height for the parent polygon
Z_RIDGE_HEAD = 11.17    # same roof pitch carried over the wider head span
Z_CREST = 11.9          # chimney crest — the bbox top, inferred as ridge + 1.0

EAVE_OVERHANG = 0.6     # deep eaves are what make a tile roof read at 20 px
FASCIA_D = 0.40         # deep enough that the eave reads as a shadow line

Z_SILL_LO, Z_SILL_HI = 2.0, 5.2
WIN_W, WIN_H = 1.2, 1.8
WIN_RECESS = 0.15
BAYS = 11

Z_ARCADE_SLAB = 3.40
ARCADE_SLAB_T = 0.35
ARCADE_POST = 0.35

CHIMNEY_SEC = 0.75
CHIMNEYS = 5            # counted off the aerial along this ward's ridge

PALETTE_HEX = {
    "Toy_white": "f7f4ec",   # smooth stucco — the ward is concrete, not wood
    "Toy_stone": "d9d2c2",   # plinth band
    "Toy_red": "c4453c",     # barrel tile
    "Toy_trim": "f3efe6",    # eave fascia, sills, arcade slab
    "Toy_glass": "2a4d73",
    "Toy_brick": "c96f4a",   # terracotta chimneys — deliberately NOT Toy_red,
                             # so the stacks read as separate objects from above
    "Toy_steel": "9aa0a6",   # the exterior steel stair — Toy_ink read as a
                             # black smear across the head elevation
    "Toy_ink": "3a3530",     # doorway recess
    "Toy_glass_Glow": "6f95b8",
    "Toy_trim_Glow": "f3efe6",
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
    """Local ward frame -> world (x east, y north). Right-handed, so a CCW
    polygon in (u, v) stays CCW in (x, y) and outward normals stay outward."""
    return (
        u * U_DIR[0] + v * V_DIR[0],
        u * U_DIR[1] + v * V_DIR[1],
    )


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
    a third of the object's thinnest dimension: several panels here are only
    120-350 mm thick and a flat 0.12 m bevel on those collapses opposing
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


def prism_uv(name, poly_uv, z0, z1, mat, mat_top=None):
    """Closed extrusion of a CCW local-frame polygon (walls + both caps)."""
    poly = [to_world(u, v) for u, v in poly_uv]
    n = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces, face_mats = [], []
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
        face_mats.append(0)
    faces.append(tuple(range(n - 1, -1, -1)))
    face_mats.append(0)
    faces.append(tuple(range(n, 2 * n)))
    face_mats.append(1 if mat_top else 0)
    mats = [mat, mat_top] if mat_top else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def hip_roof(name, u0, u1, v0, v1, z_eave, z_ridge, mat, ridge_along_u=True):
    """Closed hipped roof solid over the eave rectangle (u0..u1, v0..v1).

    The ridge is centred on the short axis and shortened at both ends by half
    the short span, which is what puts the hips at 45 deg in plan — the geometry
    a real hipped roof has, modelled as real geometry rather than faked with a
    bevelled plane (style bible: the app's camera looks down; the roof IS a
    facade). The base cap keeps the solid closed so the signed-volume normals
    test is meaningful."""
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
    return new_mesh(name, verts, faces, [mat], [0] * len(faces))


def band_uv(name, u0, u1, v0, v1, z0, z1, thickness, mat):
    """Closed rectangular band (a picture frame in plan) around the rectangle,
    growing outward by `thickness`. Used for the eave fascia."""
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


def window_bay(idx, side, u_centre, z_sill, mats, lit=False, v_wall=None):
    """One recessed window on a long elevation. `side` is -1 (southwest flank)
    or +1 (northeast flank). `v_wall` overrides the bar's wall line, which is
    what puts windows on the head block's wider flanks."""
    if v_wall is None:
        v_wall = V_BAR1 if side > 0 else V_BAR0
    v_out = v_wall + side * 0.02
    v_in = v_wall - side * WIN_RECESS
    u0, u1 = u_centre - WIN_W / 2.0, u_centre + WIN_W / 2.0
    lo, hi = (v_in, v_out) if side > 0 else (v_out, v_in)
    prism_uv(
        f"win_{side_name(side)}_{idx}_fill",
        rect_uv(u0, u1, lo, hi),
        z_sill,
        z_sill + WIN_H,
        mats["Toy_glass"],
    )
    # sill, 0.12 m proud of the wall
    sl, sh = (v_wall, v_wall + side * 0.12) if side > 0 else (v_wall + side * 0.12, v_wall)
    prism_uv(
        f"win_{side_name(side)}_{idx}_sill",
        rect_uv(u0 - 0.12, u1 + 0.12, sl, sh),
        z_sill - 0.14,
        z_sill,
        mats["Toy_trim"],
    )
    if lit:
        gl, gh = (
            (v_out, v_out + side * 0.04) if side > 0 else (v_out + side * 0.04, v_out)
        )
        prism_uv(
            f"win_{side_name(side)}_{idx}_glow",
            rect_uv(u0 + 0.05, u1 - 0.05, gl, gh),
            z_sill + 0.05,
            z_sill + WIN_H - 0.05,
            mats["Toy_glass_Glow"],
        )


def side_name(side):
    return "ne" if side > 0 else "sw"


def head_window(idx, u_centre, v_centre, z_sill, mats, lit=False):
    """A window on the east head elevation (the u = U_EAST face)."""
    u_out = U_EAST + 0.02
    u_in = U_EAST - WIN_RECESS
    v0, v1 = v_centre - WIN_W / 2.0, v_centre + WIN_W / 2.0
    prism_uv(
        f"win_head_{idx}_fill",
        rect_uv(u_in, u_out, v0, v1),
        z_sill,
        z_sill + WIN_H,
        mats["Toy_glass"],
    )
    prism_uv(
        f"win_head_{idx}_sill",
        rect_uv(U_EAST, U_EAST + 0.12, v0 - 0.12, v1 + 0.12),
        z_sill - 0.14,
        z_sill,
        mats["Toy_trim"],
    )
    if lit:
        prism_uv(
            f"win_head_{idx}_glow",
            rect_uv(u_out, u_out + 0.04, v0 + 0.05, v1 - 0.05),
            z_sill + 0.05,
            z_sill + WIN_H - 0.05,
            mats["Toy_glass_Glow"],
        )


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    mats = {name: make_material(name) for name in PALETTE_HEX}

    # ---------------------------------------------------------------- plinth
    # One continuous raised base under bar + arcade, and a wider one under the
    # head block, in a value darker than the stucco so it reads as a base.
    prism_uv(
        "plinth_bar",
        rect_uv(U_WEST - 0.15, U_HEAD, V_BAR0 - 0.15, V_BAR1 + 0.15),
        0.0,
        Z_PLINTH,
        mats["Toy_stone"],
    )
    prism_uv(
        "plinth_head",
        rect_uv(U_HEAD, U_EAST + 0.15, V_HEAD0 - 0.15, V_HEAD1 + 0.15),
        0.0,
        Z_PLINTH,
        mats["Toy_stone"],
    )

    # ------------------------------------------------------------- the bar
    # 39.95 x 9.38 m, two storeys of white stucco. This volume is the building.
    prism_uv(
        "ward_bar",
        rect_uv(U_ARCADE, U_HEAD, V_BAR0, V_BAR1),
        Z_PLINTH,
        Z_EAVE,
        mats["Toy_white"],
    )

    # --------------------------------------------------------- head block
    prism_uv(
        "head_block",
        rect_uv(U_HEAD, U_EAST, V_HEAD0, V_HEAD1),
        Z_PLINTH,
        Z_EAVE,
        mats["Toy_white"],
    )

    # ------------------------------------------------------------- windows
    # 11 bays per long elevation over the bar's 39.95 m, two tiers. The lit set
    # is deliberately sparse and confined to the northeast flank plus the head:
    # a fully lit 40 m bar would read as a working hospital, which it has not
    # been since 1994.
    span0, span1 = U_ARCADE + 1.9, U_HEAD - 1.9
    step = (span1 - span0) / (BAYS - 1)
    # Both flanks carry a few lit windows, weighted to the southwest — a night
    # state confined to one elevation is invisible from half the orbit, and the
    # app's camera circles the city. Nine lit windows out of 44 is the density
    # of an office building at 8pm, which is what this is.
    lit = {
        (-1, "lo"): {3, 7},
        (-1, "hi"): {0, 4, 8},
        (+1, "lo"): {2},
        (+1, "hi"): {5, 9},
    }
    for i in range(BAYS):
        uc = span0 + i * step
        for side in (+1, -1):
            window_bay(i, side, uc, Z_SILL_LO, mats, lit=(i in lit[(side, "lo")]))
            window_bay(
                i + 100, side, uc, Z_SILL_HI, mats, lit=(i in lit[(side, "hi")])
            )

    # The head block's own flanks. Without these the last 10 m of both long
    # elevations is a blank white wall, which the real building does not have.
    for j, uc in enumerate((20.4, 24.7)):
        for side in (+1, -1):
            vw = V_HEAD1 if side > 0 else V_HEAD0
            window_bay(200 + j, side, uc, Z_SILL_LO, mats, v_wall=vw)
            window_bay(
                220 + j, side, uc, Z_SILL_HI, mats,
                lit=(side < 0 and j == 1), v_wall=vw,
            )

    # East head elevation: four windows, asymmetric, plus the doorway.
    head_window(0, U_EAST, -3.9, Z_SILL_LO, mats)
    head_window(1, U_EAST, 3.4, Z_SILL_LO, mats, lit=True)
    head_window(2, U_EAST, -3.9, Z_SILL_HI, mats, lit=True)
    head_window(3, U_EAST, 1.5, Z_SILL_HI, mats)

    prism_uv(
        "head_door",
        rect_uv(U_EAST - 0.35, U_EAST + 0.02, -1.3, 0.0),
        Z_PLINTH,
        Z_PLINTH + 2.3,
        mats["Toy_ink"],
    )

    # ------------------------------------------------ east stair and landing
    # The exterior steel stair that climbs the head elevation to an upper-floor
    # landing. Simplified to a ramped slab, a landing block and two rail bars.
    stair = prism_uv(
        "east_stair",
        rect_uv(U_EAST + 0.02, U_EAST + 1.30, -6.0, -0.6),
        Z_PLINTH,
        Z_PLINTH + 0.25,
        mats["Toy_steel"],
    )
    stair.rotation_euler = (0.0, 0.0, 0.0)
    # Rake the slab by moving its far end up: done as a vertex edit so the
    # object keeps an identity transform (the contract requires applied
    # transforms and this avoids a later apply step).
    ramp_top = Z_PLINTH + 3.35
    for vtx in stair.data.vertices:
        local_u = vtx.co.x * U_DIR[0] + vtx.co.y * U_DIR[1]
        local_v = -vtx.co.x * U_DIR[1] + vtx.co.y * U_DIR[0]
        t = (local_v + 6.0) / 5.4
        del local_u
        if vtx.co.z > Z_PLINTH + 0.1:
            vtx.co.z = Z_PLINTH + 0.25 + t * (ramp_top - Z_PLINTH - 0.25)
        else:
            vtx.co.z = Z_PLINTH + t * (ramp_top - Z_PLINTH - 0.25)

    prism_uv(
        "east_landing",
        rect_uv(U_EAST + 0.02, U_EAST + 1.55, -0.6, 1.6),
        ramp_top,
        ramp_top + 0.25,
        mats["Toy_steel"],
    )
    for k, (v0, v1) in enumerate(((-6.0, 1.6), (-6.0, 1.6))):
        prism_uv(
            f"east_rail_{k}",
            rect_uv(U_EAST + (0.10 if k == 0 else 1.35), U_EAST + (0.22 if k == 0 else 1.47), v0, v1),
            ramp_top + 0.25,
            ramp_top + 1.15,
            mats["Toy_steel"],
        )
    prism_uv(
        "head_soffit_glow",
        rect_uv(U_EAST + 0.20, U_EAST + 1.35, -0.35, 1.35),
        ramp_top - 0.06,
        ramp_top - 0.02,
        mats["Toy_trim_Glow"],
    )

    # ----------------------------------------------------------- arcade stub
    # Where the ward meets the connecting corridor of the row. Open, single
    # storey, flat slab on four posts. Rarely seen at ground level; the app's
    # aerial camera reads it as the join to the (procedural) neighbours.
    prism_uv(
        "arcade_slab",
        rect_uv(U_WEST, U_ARCADE + 0.2, V_BAR0 - 0.2, V_BAR1 + 0.2),
        Z_ARCADE_SLAB,
        Z_ARCADE_SLAB + ARCADE_SLAB_T,
        mats["Toy_trim"],
    )
    for k, (uu, vv) in enumerate(
        (
            (U_WEST + 0.45, V_BAR0 + 0.45),
            (U_WEST + 0.45, V_BAR1 - 0.45),
            (U_ARCADE - 0.55, V_BAR0 + 0.45),
            (U_ARCADE - 0.55, V_BAR1 - 0.45),
        )
    ):
        h = ARCADE_POST / 2.0
        prism_uv(
            f"arcade_post_{k}",
            rect_uv(uu - h, uu + h, vv - h, vv + h),
            Z_PLINTH,
            Z_ARCADE_SLAB,
            mats["Toy_white"],
        )

    # -------------------------------------------------------------- roofs
    # Bar: hipped, ridge along the long axis. Head: its own hip, ridge across.
    # The main hip runs the WHOLE 55 m, so the ridge is continuous end to end —
    # the aerial's single unbroken ridge line. The head block's extra width
    # carries a cross-hip at the same pitch, which therefore rises higher and
    # splays wider, exactly the flare visible at every ward's east end. The two
    # solids interpenetrate on purpose: that intersection IS the cross-hip.
    o = EAVE_OVERHANG
    bar_e = (U_ARCADE - o, U_EAST + o, V_BAR0 - o, V_BAR1 + o)
    hip_roof("roof_bar", *bar_e, Z_EAVE, Z_RIDGE, mats["Toy_red"], ridge_along_u=True)
    band_uv(
        "fascia_bar",
        bar_e[0], bar_e[1], bar_e[2], bar_e[3],
        Z_EAVE - FASCIA_D, Z_EAVE,
        0.10,
        mats["Toy_trim"],
    )

    head_e = (U_HEAD - o, U_EAST + o, V_HEAD0 - o, V_HEAD1 + o)
    hip_roof("roof_head", *head_e, Z_EAVE, Z_RIDGE_HEAD, mats["Toy_red"], ridge_along_u=False)
    band_uv(
        "fascia_head",
        head_e[0], head_e[1], head_e[2], head_e[3],
        Z_EAVE - FASCIA_D, Z_EAVE,
        0.10,
        mats["Toy_trim"],
    )

    # ------------------------------------------------------------ chimneys
    # Three on the bar ridge at 20 / 50 / 80 percent of its length, one on the
    # head block. Exaggerated in section so they survive at thumbnail size, but
    # NOT in height: the crest must land on 11.9 exactly (loader scale = 1.0).
    ridge_inset = (bar_e[3] - bar_e[2]) / 2.0
    r0 = bar_e[0] + ridge_inset
    r1 = U_HEAD - ridge_inset
    v_ridge = (V_BAR0 + V_BAR1) / 2.0
    h = CHIMNEY_SEC / 2.0
    for k in range(CHIMNEYS):
        uc = r0 + (r1 - r0) * (k + 0.5) / CHIMNEYS
        prism_uv(
            f"chimney_{k}",
            rect_uv(uc - h, uc + h, v_ridge - h, v_ridge + h),
            Z_RIDGE - 1.2,
            Z_CREST,
            mats["Toy_brick"],
        )
    prism_uv(
        "chimney_head",
        rect_uv(U_EAST - 3.6 - h, U_EAST - 3.6 + h, 3.2 - h, 3.2 + h),
        Z_RIDGE_HEAD - 1.2,
        Z_CREST,
        mats["Toy_brick"],
    )

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.12/2. Window fills, sills and glow shells are small and numerous — a
    # token softening or none at all is what keeps this under the cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")):
            continue
        if obj.name.endswith("_sill") or obj.name.startswith(("east_rail", "arcade_post")):
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

    The building is not symmetric about its footprint centre — the head block's
    roof overhangs 0.6 m past the east wall while the arcade's flat slab stops
    dead at the west end — so authoring on the true footprint leaves the bbox
    centre ~1 m off. Shift the geometry and carry the same shift into the
    anchor, which keeps the building on its real footprint (AGENTS rule 5)."""
    mn = Vector((1e9, 1e9)); mx = Vector((-1e9, -1e9))
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    for o in meshes:
        for v in o.data.vertices:
            for i in range(2):
                mn[i] = min(mn[i], v.co[i]); mx[i] = max(mx[i], v.co[i])
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
    lon0, lat0 = -122.4514885, 37.8007968
    lat_scale = 111320.0 * math.cos(math.radians(37.77))
    lon = lon0 + ANCHOR_SHIFT[0] / lat_scale
    lat = lat0 + ANCHOR_SHIFT[1] / 110540.0
    print(f"[build] footprint OBB centre lon/lat: {lon0} {lat0}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] long axis heading: {HEADING_LONG} deg true (east head)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "1008-general-kennedy.blend")
    glb = os.path.join(out, "1008-general-kennedy.glb")
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
