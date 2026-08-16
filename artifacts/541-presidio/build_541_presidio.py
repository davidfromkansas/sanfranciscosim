"""Deterministic Blender build of the SF-SIM miniature 541 Presidio Boulevard.

    blender -b --python build_541_presidio.py -- [--out DIR]

Writes 541-presidio.blend and 541-presidio.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, chimney crest exactly
10.0 m.

Design (see REFERENCE.md for the sources behind every number):

* a World War I-era (1915-1918) officer's family quarters in the Presidio's East
  Housing area, one of twelve near-identical houses (Bldgs. 540-551) strung along
  the curve of Presidio Boulevard as it climbs a forested hill;
* the recognition rests on the ROOF: a red barrel-tile hip with deep overhanging
  eaves is ~90% of the building at the app's viewing distance. Cream stucco walls
  exist to make that roof read;
* a one-storey porch across the middle of the street (east-southeast) elevation,
  with its own subordinate hip — the silhouette cue that stops this reading as a
  plain hipped box from the air;
* two stucco chimneys through the main ridge: the only vertical incident, and
  what sets the 10.0 m crest;
* a shallow 4.61 x 0.86 m bay on the rear elevation, full height, flush into the
  main roof slope;
* night state: three or four lit windows on the front elevation only, plus the
  porch soffit. This is a single-family house on a quiet Presidio street; a fully
  lit twelve-window box would read as an institution. Glow surfaces are thin
  shells proud of the opaque glazing — the app renders _Glow in a separate layer
  that is ~12% alpha by day, so a primary surface must never be authored as glow.

Authoring frame: geometry is laid out in a local (u, v) frame aligned with the
house — u along the long axis, positive toward 540 (bearing 210.68 deg true); v
across, positive toward Presidio Boulevard (bearing 120.68 deg), which is the
front. Mapped to world x/y by to_world(). The building sits ~31 deg off the world
axes, so the axis-aligned XY bounding box is ~21.6 x 24.3 m even though the
building is 19.77 x 11.65 m plus a 1.75 m porch. That is expected, not a scale
error.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# Heading of the house's long axis, measured from OSM way 288361187 reprojected
# with the project's tangent projection and reduced to a min-area oriented
# bounding box. +u points along the row toward 540; +v points at the boulevard.
HEADING_LONG = 210.68   # +u, toward 540 (south-southwest)
HEADING_CROSS = 120.68  # +v, the front elevation, faces Presidio Boulevard

_UL = math.radians(HEADING_LONG)
U_DIR = (math.sin(_UL), math.cos(_UL))
V_DIR = (-U_DIR[1], U_DIR[0])

# Local extents, metres, relative to the main block's centre.
# u: -9.885 .. +9.885   -> 19.77 m, measured
# v: -5.825 .. +5.825   -> 11.65 m, measured
U_S, U_N = -9.885, 9.885
V_REAR, V_FRONT = -5.825, 5.825

# Front porch: 9.68 m long, 1.75 m deep, measured off the ring. It is very
# slightly off-centre (centre at u = -0.145); keep it — that is what the survey
# says, and a house is not a symmetrical object.
PORCH_U0, PORCH_U1 = -4.985, 4.695
PORCH_V1 = 7.595

# Rear bay: 4.61 m long, 0.86 m deep, measured. A stair or chimney breast.
BAY_U0, BAY_U1 = -2.515, 2.095
BAY_V0 = -6.675

Z_PLINTH = 0.9          # raised base — also hides the terrain seam
Z_EAVE = 7.2            # inferred: plinth + two ~3.15 m storeys. Solved against
                        # the LiDAR crest/median pair; see the plan's 2.3.
Z_RIDGE = 9.6           # inferred: same solve, pitch lands at ~20 deg
Z_CREST = 10.0          # chimney crest — the bbox top, and the manifest
                        # targetHeightM, so the loader's scale is exactly 1.0.
                        # LiDAR maximum is 10.04 m; 10.0 is the shipped target.

Z_PORCH_EAVE = 3.40
Z_PORCH_RIDGE = 4.35    # deliberately steeper than the main roof (~30 deg vs
                        # ~20 deg): over a 2.3 m span the main pitch renders as a
                        # flat awning from above, and the porch hip has to stay
                        # legible at thumbnail size. Raised from 4.05 after the
                        # first aerial review render — see REPORT.md.

EAVE_OVERHANG = 0.70    # deep eaves are what make a tile roof read at 20 px
PORCH_OVERHANG = 0.50
FASCIA_D = 0.22         # deep enough that the eave reads as a shadow line

Z_SILL_LO, Z_SILL_HI = 1.70, 4.60
WIN_W, WIN_H = 1.10, 1.90
WIN_RECESS = 0.12
BAYS_LONG = 5           # per long elevation, per tier
BAYS_END = 3            # per short end, per tier

DOOR_W, DOOR_H = 1.00, 2.20

CHIMNEY_U = 1.00        # exaggerated in section so they survive at thumbnail
CHIMNEY_V = 0.80        # size, but NOT in height — the crest must land on 10.0

# Chimneys pierce the SLOPES rather than sitting on the ridge. On the ridge a
# stack capped at the 10.0 m crest shows only 0.4 m of stucco and renders as a
# tiny block (first aerial review); 2.6 m off-centre the roof surface is at
# 8.64 m, so the same stack reads as a 1.36 m chimney while still topping out at
# exactly 10.0. Piercing the slope is also the commoner real configuration.
# Diagonally opposed so both read from any orbit azimuth.
CHIMNEY_SITES = ((-3.60, 2.60), (3.60, -2.60))
Z_CHIMNEY_BASE = 8.20

PALETTE_HEX = {
    "Toy_white": "f7f4ec",   # smooth stucco walls
    "Toy_stone": "d9d2c2",   # plinth band, and the chimney stacks: these are
                             # stuccoed to match the walls, not exposed brick,
                             # so Toy_brick would be wrong here even though
                             # 1008-general-kennedy uses it. Toy_stone keeps
                             # them a half-value darker than the wall so they
                             # still read as separate objects from directly
                             # above, which is the only view that matters.
    "Toy_red": "c4453c",     # barrel tile — main hip and porch hip
    "Toy_trim": "f3efe6",    # eave fascia, window sills, porch soffit
    "Toy_glass": "2a4d73",
    "Toy_ink": "3a3530",     # entrance doorway recess
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

# The measured OSM ring in the local (u, v) frame — used for the plinth, so the
# base carries the real plan shape (main block + porch + rear bay) rather than a
# simplified rectangle.
FOOTPRINT_UV = [
    (U_S, V_REAR),
    (BAY_U0, V_REAR),
    (BAY_U0, BAY_V0),
    (BAY_U1, BAY_V0),
    (BAY_U1, V_REAR),
    (U_N, V_REAR),
    (U_N, V_FRONT),
    (PORCH_U1, V_FRONT),
    (PORCH_U1, PORCH_V1),
    (PORCH_U0, PORCH_V1),
    (PORCH_U0, V_FRONT),
    (U_S, V_FRONT),
]


# ----------------------------------------------------------------- transforms


def to_world(u, v):
    """Local house frame -> world (x east, y north). Right-handed, so a CCW
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
    a third of the object's thinnest dimension: window fills, sills and glow
    shells are only 40-120 mm thick and a flat 0.12 m bevel on those collapses
    opposing profiles into zero-area slivers even with clamp_overlap."""
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


def window_v(name, u_centre, v_wall, side, z_sill, mats, lit=False):
    """A recessed window on an elevation whose wall runs along u (i.e. the front
    or rear faces). `side` is +1 for a wall facing +v, -1 for -v."""
    v_out = v_wall + side * 0.02
    v_in = v_wall - side * WIN_RECESS
    u0, u1 = u_centre - WIN_W / 2.0, u_centre + WIN_W / 2.0
    lo, hi = (v_in, v_out) if side > 0 else (v_out, v_in)
    prism_uv(f"{name}_fill", rect_uv(u0, u1, lo, hi), z_sill, z_sill + WIN_H,
             mats["Toy_glass"])
    sl, sh = ((v_wall, v_wall + side * 0.10) if side > 0
              else (v_wall + side * 0.10, v_wall))
    prism_uv(f"{name}_sill", rect_uv(u0 - 0.10, u1 + 0.10, sl, sh),
             z_sill - 0.12, z_sill, mats["Toy_trim"])
    if lit:
        gl, gh = ((v_out, v_out + side * 0.04) if side > 0
                  else (v_out + side * 0.04, v_out))
        prism_uv(f"{name}_glow", rect_uv(u0 + 0.05, u1 - 0.05, gl, gh),
                 z_sill + 0.05, z_sill + WIN_H - 0.05, mats["Toy_glass_Glow"])


def window_u(name, v_centre, u_wall, side, z_sill, mats, lit=False):
    """A recessed window on a short end (a wall running along v)."""
    u_out = u_wall + side * 0.02
    u_in = u_wall - side * WIN_RECESS
    v0, v1 = v_centre - WIN_W / 2.0, v_centre + WIN_W / 2.0
    lo, hi = (u_in, u_out) if side > 0 else (u_out, u_in)
    prism_uv(f"{name}_fill", rect_uv(lo, hi, v0, v1), z_sill, z_sill + WIN_H,
             mats["Toy_glass"])
    sl, sh = ((u_wall, u_wall + side * 0.10) if side > 0
              else (u_wall + side * 0.10, u_wall))
    prism_uv(f"{name}_sill", rect_uv(sl, sh, v0 - 0.10, v1 + 0.10),
             z_sill - 0.12, z_sill, mats["Toy_trim"])
    if lit:
        gl, gh = ((u_out, u_out + side * 0.04) if side > 0
                  else (u_out + side * 0.04, u_out))
        prism_uv(f"{name}_glow", rect_uv(gl, gh, v0 + 0.05, v1 - 0.05),
                 z_sill + 0.05, z_sill + WIN_H - 0.05, mats["Toy_glass_Glow"])


def spread(a, b, n, margin):
    """n evenly spaced centres across [a, b], inset by `margin` at both ends."""
    a, b = a + margin, b - margin
    if n == 1:
        return [(a + b) / 2.0]
    step = (b - a) / (n - 1)
    return [a + i * step for i in range(n)]


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    mats = {name: make_material(name) for name in PALETTE_HEX}

    # ---------------------------------------------------------------- plinth
    # The measured footprint ring, extruded, in a value darker than the stucco
    # so it reads as a base — and so the terrain seam has somewhere to hide.
    prism_uv("plinth", FOOTPRINT_UV, 0.0, Z_PLINTH, mats["Toy_stone"])

    # ------------------------------------------------------------ main block
    # 19.77 x 11.65 m, two storeys of cream stucco. This volume is the house.
    prism_uv("house_block", rect_uv(U_S, U_N, V_REAR, V_FRONT),
             Z_PLINTH, Z_EAVE, mats["Toy_white"])

    # Rear bay, full height, flush into the main roof slope.
    prism_uv("rear_bay", rect_uv(BAY_U0, BAY_U1, BAY_V0, V_REAR),
             Z_PLINTH, Z_EAVE, mats["Toy_white"])

    # ------------------------------------------------------------ front porch
    # One storey, solid volume with its own hip. Reading the measured 9.68 x
    # 1.75 m projection as a porch is the plan's single biggest inference
    # (2.15 #1); the massing is identical whether it is open or enclosed.
    prism_uv("porch", rect_uv(PORCH_U0, PORCH_U1, V_FRONT, PORCH_V1),
             Z_PLINTH, Z_PORCH_EAVE, mats["Toy_white"])

    # --------------------------------------------------------------- windows
    # 5 bays per long elevation per tier, 3 per short end per tier. These are
    # designed rhythms that respect the elevation lengths, not counts off a
    # photograph (2.15 #4).
    #
    # Front, upper tier: all five bays sit on the main wall, clear above the
    # porch roof. Front, lower tier: the porch occupies the middle of the
    # elevation, so only the two outer bays land on the main wall and the
    # middle of the ground floor is served by the porch's own face.
    front_u = spread(U_S, U_N, BAYS_LONG, 1.85)
    for i, uc in enumerate(front_u):
        lit = i in (1, 3)          # two lit upper windows
        window_v(f"win_front_hi_{i}", uc, V_FRONT, +1, Z_SILL_HI, mats, lit=lit)
    for i, uc in enumerate(front_u):
        if PORCH_U0 - 0.6 < uc < PORCH_U1 + 0.6:
            continue
        window_v(f"win_front_lo_{i}", uc, V_FRONT, +1, Z_SILL_LO, mats)

    # Porch face: the entrance, flanked by one window either side. One of them
    # is lit — the hall light behind the front door.
    porch_c = (PORCH_U0 + PORCH_U1) / 2.0
    prism_uv("front_door",
             rect_uv(porch_c - DOOR_W / 2.0, porch_c + DOOR_W / 2.0,
                     PORCH_V1 - 0.30, PORCH_V1 + 0.02),
             Z_PLINTH, Z_PLINTH + DOOR_H, mats["Toy_ink"])
    for i, uc in enumerate((porch_c - 3.05, porch_c + 3.05)):
        window_v(f"win_porch_{i}", uc, PORCH_V1, +1, Z_SILL_LO, mats,
                 lit=(i == 0))

    # Porch soffit: the supporting night accent, a thin shell under the eave.
    prism_uv("porch_soffit_glow",
             rect_uv(PORCH_U0 + 0.35, PORCH_U1 - 0.35,
                     V_FRONT + 0.35, PORCH_V1 + 0.30),
             Z_PORCH_EAVE - 0.06, Z_PORCH_EAVE - 0.02, mats["Toy_trim_Glow"])

    # Rear elevation: the 4.61 m bay interrupts the middle, so four bays land on
    # the main wall (two either side) and one per tier sits on the bay's face.
    rear_u = spread(U_S, U_N, BAYS_LONG, 1.85)
    for i, uc in enumerate(rear_u):
        if BAY_U0 - 0.5 < uc < BAY_U1 + 0.5:
            continue
        window_v(f"win_rear_hi_{i}", uc, V_REAR, -1, Z_SILL_HI, mats)
        window_v(f"win_rear_lo_{i}", uc, V_REAR, -1, Z_SILL_LO, mats)
    bay_c = (BAY_U0 + BAY_U1) / 2.0
    window_v("win_bay_hi", bay_c, BAY_V0, -1, Z_SILL_HI, mats)
    window_v("win_bay_lo", bay_c, BAY_V0, -1, Z_SILL_LO, mats)

    # Short ends, toward 542 (+u is toward 540, so U_N faces 542).
    for side, u_wall, tag in ((+1, U_N, "n"), (-1, U_S, "s")):
        for i, vc in enumerate(spread(V_REAR, V_FRONT, BAYS_END, 1.85)):
            window_u(f"win_end{tag}_hi_{i}", vc, u_wall, side, Z_SILL_HI, mats)
            window_u(f"win_end{tag}_lo_{i}", vc, u_wall, side, Z_SILL_LO, mats)

    # ----------------------------------------------------------------- roofs
    # Main: hipped, ridge along the long axis, deep eaves all round. Porch: its
    # own lower hip, springing off the front wall. The two solids interpenetrate
    # on purpose — that intersection is how the porch roof dies into the wall.
    o = EAVE_OVERHANG
    main_e = (U_S - o, U_N + o, V_REAR - o, V_FRONT + o)
    hip_roof("roof_main", *main_e, Z_EAVE, Z_RIDGE, mats["Toy_red"],
             ridge_along_u=True)
    band_uv("fascia_main", main_e[0], main_e[1], main_e[2], main_e[3],
            Z_EAVE - FASCIA_D, Z_EAVE, 0.10, mats["Toy_trim"])

    p = PORCH_OVERHANG
    porch_e = (PORCH_U0 - p, PORCH_U1 + p, V_FRONT, PORCH_V1 + p)
    hip_roof("roof_porch", *porch_e, Z_PORCH_EAVE, Z_PORCH_RIDGE,
             mats["Toy_red"], ridge_along_u=True)
    band_uv("fascia_porch", porch_e[0], porch_e[1], porch_e[2], porch_e[3],
            Z_PORCH_EAVE - 0.18, Z_PORCH_EAVE, 0.09, mats["Toy_trim"])

    # -------------------------------------------------------------- chimneys
    # Two stucco stacks piercing the main roof slopes. Count and position are
    # inferred (2.15 #2): two stacks is what a 10.04 m LiDAR maximum over a
    # 9.6 m ridge implies, but one central stack or three fit the data equally
    # well. They carry the crest, so their tops must land on 10.0 exactly.
    hu, hv = CHIMNEY_U / 2.0, CHIMNEY_V / 2.0
    for k, (uc, vc) in enumerate(CHIMNEY_SITES):
        prism_uv(f"chimney_{k}", rect_uv(uc - hu, uc + hu, vc - hv, vc + hv),
                 Z_CHIMNEY_BASE, Z_CREST, mats["Toy_stone"])

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.12/2. Window fills, sills and glow shells are small and numerous — a
    # token softening or none at all is what keeps this under the cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")):
            continue
        if obj.name.endswith("_sill"):
            bevel(obj, width=0.04, segments=1)
        else:
            bevel(obj, width=0.12, segments=2)

    recentre()
    return scene


# Metres east / north from the main-block centre to the model's XY bbox centre,
# filled in by recentre(). The manifest anchor is the main-block centre moved by
# this vector, so the origin sits at the bbox centre (contract rule 2) while the
# building still lands on its real footprint.
ANCHOR_SHIFT = [0.0, 0.0]


def recentre():
    """Move the model so its XY bounding-box centre is the origin.

    The house is not symmetric about its main-block centre — the porch pushes
    1.75 m past the front wall and its roof another 0.5 m beyond that, while the
    rear only has a 0.86 m bay — so authoring on the true footprint leaves the
    bbox centre ~0.7 m off toward the boulevard. Shift the geometry and carry the
    same shift into the anchor, which keeps the building on its real footprint
    (AGENTS rule 5)."""
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
    lon0, lat0 = -122.4518601, 37.7969312
    lon_scale = 111320.0 * math.cos(math.radians(37.77))
    lon = lon0 + ANCHOR_SHIFT[0] / lon_scale
    lat = lat0 + ANCHOR_SHIFT[1] / 110540.0
    print(f"[build] main-block centre lon/lat: {lon0} {lat0}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] long axis heading: {HEADING_LONG} deg true (+u toward 540)")
    print(f"[build] front elevation faces: {HEADING_CROSS} deg true")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "541-presidio.blend")
    glb = os.path.join(out, "541-presidio.glb")
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
