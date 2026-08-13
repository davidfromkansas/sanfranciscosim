"""Deterministic Blender build of the SF-SIM miniature 543 Presidio Blvd.

    blender -b --python build_543_presidio_blvd.py -- [--out DIR]

Writes 543-presidio-blvd.blend and 543-presidio-blvd.glb next to this file (or
into --out). Geometry is authored in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = XY bounding-box centre, min Z = 0, chimney
crest exactly 9.55 m.

Design (see REFERENCE.md for the sources behind every number):

* a World War I-era officers' family residence on the west side of Presidio
  Boulevard, one of a row of near-identical Mission Revival houses that step
  down the hillside from Lombard Gate;
* the recognition rests on the ROOF: a near-square 13.72 x 12.79 m plan under a
  low red clay-tile hip whose ridge is only 0.93 m long, so the roof reads as
  four large triangles meeting almost at a point. From the app's aerial camera
  that red shape IS the building;
* deep eaves with a heavy fascia — the eave shadow is what makes a tile roof
  read at 20 px, and it is exaggerated here for exactly that reason;
* a projecting one-storey entry porch on the street front under its own small
  hip, and one masonry chimney, which is the only vertical incident and sets
  the 9.55 m crest;
* the rear NNE corner is notched 2.70 x 3.45 m. The walls follow the notch; the
  roof spans the full rectangle over it (see BUILD CORRECTION below);
* night state: five warm-lit windows spread across three elevations plus a lit
  porch soffit. This is a house at 9pm, not an office block. Glow surfaces are
  thin shells proud of the opaque glazing — the app renders _Glow in a separate
  layer that is ~12% alpha by day, so a primary surface must never be authored
  as glow.

BUILD CORRECTION vs docs/asset-plans/543-presidio-blvd.md §2.7:
The plan specified two hips — a main hip over the notched block with its ridge
along v, plus a lower subordinate hip over the front wing. Carried at a matched
pitch the wing hip's ridge lands at 7.58 m, entirely swallowed by the main hip
and reading as a lump rather than a wing. The built asset instead carries ONE
hip over the full 13.72 x 12.79 m envelope with the ridge along u (parallel to
the street front, which is the longer axis at the eave line: 14.82 m against
13.89 m). That is what the aerial imagery shows, it is what a hipped roof over
rectangular framing actually does when a rear corner is recessed as a porch, and
it keeps the roof one legible red shape — recognition cue #1. The notch still
reads: on the rear elevation as a wall setback, and in the footprint the asset
occupies. REPORT beats plan.

Authoring frame: geometry is laid out in a local (u, v) frame aligned with the
house — u along the front wall, positive toward the SSW (bearing 190.7 deg
true); v across, positive toward Presidio Boulevard (bearing 100.7 deg) — and
mapped to world x/y by to_world(). The house sits ~11 deg off the world axes, so
the axis-aligned XY bounding box is slightly larger than the building. That is
expected, not a scale error.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# Heading of the front wall's long axis, measured from OSM way 288361199 pulled
# from the Overpass API and reprojected with the repo's local tangent
# projection, then reduced to a minimum-area oriented bounding box. The six
# polygon edges agree to within 0.15 deg on the two headings.
HEADING_LONG = 190.7    # +u, toward the SSW neighbour at 541 Presidio Blvd
HEADING_CROSS = 100.7   # +v, toward Presidio Boulevard (the street front)

_UL = math.radians(HEADING_LONG)
U_DIR = (math.sin(_UL), math.cos(_UL))
V_DIR = (-U_DIR[1], U_DIR[0])   # +90 deg in world XY -> bearing 100.7, the street

# Local extents, metres, relative to the footprint OBB centre. Measured.
U_MIN, U_MAX = -6.86, 6.86      # 13.72 m of street frontage
V_MIN, V_MAX = -6.39, 6.40      # 12.79 m deep
U_WING = -4.16                  # walls step back NNE of this line at the rear
V_NOTCH = -2.94                 # ...behind this line

Z_PLINTH = 0.90         # exposed raised basement; also hides the terrain seam
Z_EAVE = 7.00           # inferred: plinth + 3.10 m + 3.00 m storeys
Z_RIDGE = 9.15          # inferred: 4.25:12 hip over the 13.89 m cross span
Z_CREST = 9.55          # chimney crest = the bbox top. MEASURED: DataSF
                        # ynuv-fyni building 201006.0038392, hgt_maxcm = 955.
                        # A hip running 7.00 -> 9.15 has a median surface height
                        # of ~8.15 m over this footprint, and DataSF's measured
                        # hgt_median_m is 8.21 — which is the check that makes
                        # the inferred eave/ridge split defensible.

EAVE_OVERHANG = 0.62    # exaggerated: the eave shadow is the tile-roof cue
FASCIA_D = 0.42         # deep enough that the eave reads as a shadow line
PLINTH_GROW = 0.12      # the base is proud of the wall, so it reads as a base

CAP_W, CAP_H = 0.34, 0.17   # ridge and hip cap section

WIN_W, WIN_H = 1.10, 1.65
WIN_RECESS = 0.15
Z_SILL_LO, Z_SILL_HI = 2.10, 4.90

# Porch, third pass. At 4.6 m wide x 2.0 m deep on 0.4 m sticks it read as a
# carport, and at 3.90 m the canopy floated halfway up a 7 m wall. A Presidio
# officers' entry is a SMALL, SOLID thing: shallow projection, chunky square
# piers, a deep entablature sitting just above the door head, and a real hip on
# top. Those are the numbers below.
PORCH_HALF_W = 1.80     # 3.6 m wide entry porch on the front centre line
PORCH_PROJ = 1.50
Z_PORCH_CANOPY = 3.30   # door head is at 3.15 — the canopy sits right on it
PORCH_CANOPY_T = 0.45   # deep enough to read as an entablature, not a shelf
Z_PORCH_RIDGE = 4.55
PORCH_POST = 0.46       # square piers

CHIMNEY_U, CHIMNEY_V = -2.60, -2.00
CHIMNEY_SEC_U, CHIMNEY_SEC_V = 1.00, 0.82
Z_CHIMNEY_BASE = 7.90

PALETTE_HEX = {
    "Toy_white": "f7f4ec",   # smooth stucco
    "Toy_stone": "d9d2c2",   # exposed raised basement, porch slab
    "Toy_red": "c4453c",     # clay tile
    "Toy_trim": "f3efe6",    # eave fascia, sills, porch posts and canopy
    "Toy_glass": "2a4d73",
    "Toy_brick": "c96f4a",   # chimney — deliberately NOT Toy_red, so the stack
                             # reads as a separate object from above
    "Toy_ink": "3a3530",     # door recess
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
    """Local house frame -> world (x east, y north). Right-handed, so a CCW
    polygon in (u, v) stays CCW in (x, y) and outward normals stay outward."""
    return (
        u * U_DIR[0] + v * V_DIR[0],
        u * U_DIR[1] + v * V_DIR[1],
    )


def rect_uv(u0, u1, v0, v1):
    """CCW rectangle in the local frame."""
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]


def footprint_uv(grow=0.0):
    """The measured six-vertex footprint, CCW, optionally grown outward.

    A full 13.72 x 12.79 m rectangle with a 2.70 x 3.45 m bite out of the rear
    NNE corner (OSM way 288361199, six edges, two headings). The bite is 6% of
    the footprint and it is what distinguishes this house from its neighbours
    in plan, so it is modelled rather than squared off."""
    g = grow
    return [
        (U_WING - g, V_MIN - g),
        (U_MAX + g, V_MIN - g),
        (U_MAX + g, V_MAX + g),
        (U_MIN - g, V_MAX + g),
        (U_MIN - g, V_NOTCH - g),
        (U_WING - g, V_NOTCH - g),
    ]


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
    """Miniature-style edge softening (style bible §4). The offset is capped at
    a third of the object's thinnest dimension: several panels here are only
    120-380 mm thick and a flat 0.12 m bevel on those collapses opposing
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


def bar_3d(name, a, b, width, height, mat, extend=0.0):
    """Closed box running between two local-frame points a=(u,v,z), b=(u,v,z),
    with a `width` x `height` cross-section, `height` measured perpendicular to
    the run and `width` horizontally across it.

    This is how the ridge and hip caps are modelled. They are the detail that
    turns a red pyramid into a clay-TILE hip roof from the app's aerial camera:
    the caps are the same Toy_red as the field, so the line comes from the
    normal break, exactly the way it does on a real tile roof — no extra colour,
    no extra material, ~100 triangles for the single strongest roof cue."""
    A = Vector(to_world(a[0], a[1]) + (a[2],))
    B = Vector(to_world(b[0], b[1]) + (b[2],))
    d = (B - A)
    if d.length < 1e-6:
        raise ValueError(f"{name}: zero-length bar")
    d.normalize()
    A -= d * extend
    B += d * extend
    s = d.cross(Vector((0.0, 0.0, 1.0)))
    if s.length < 1e-6:
        s = Vector((1.0, 0.0, 0.0))
    s.normalize()
    n = s.cross(d)
    n.normalize()
    hw, hh = width / 2.0, height / 2.0
    verts = []
    for P in (A, B):
        for sw, sh in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            verts.append(tuple(P + s * (sw * hw) + n * (sh * hh)))
    faces = [
        (0, 1, 2, 3)[::-1],       # start cap
        (4, 5, 6, 7),             # end cap
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (3, 7, 4, 0),
    ]
    return new_mesh(name, verts, faces, [mat])


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


# Each wall face is described as (axis, wall coordinate, outward sign). "u"
# means the face is perpendicular to u (an end elevation); "v" means it faces
# along v (the street front or the rear).
FACES = {
    "front": ("v", V_MAX, +1),   # ESE, onto Presidio Boulevard
    "rear": ("v", V_MIN, -1),    # WNW
    "ssw": ("u", U_MAX, +1),     # toward 541
    "nne": ("u", U_MIN, -1),     # the notched side, toward 545
}


def window(name, face, along, z_sill, mats, lit=False):
    """One recessed window. `along` is the centre position on the free axis."""
    axis, wall, side = FACES[face]
    out = wall + side * 0.02
    inn = wall - side * WIN_RECESS
    lo, hi = (inn, out) if side > 0 else (out, inn)
    a0, a1 = along - WIN_W / 2.0, along + WIN_W / 2.0

    def box(u_lo, u_hi, v_lo, v_hi, z0, z1, mat, suffix):
        prism_uv(f"win_{name}_{suffix}", rect_uv(u_lo, u_hi, v_lo, v_hi), z0, z1, mat)

    if axis == "v":
        box(a0, a1, lo, hi, z_sill, z_sill + WIN_H, mats["Toy_glass"], "fill")
        sl, sh = (wall, wall + side * 0.12) if side > 0 else (wall + side * 0.12, wall)
        box(a0 - 0.12, a1 + 0.12, sl, sh, z_sill - 0.13, z_sill, mats["Toy_trim"], "sill")
        if lit:
            gl, gh = (out, out + side * 0.04) if side > 0 else (out + side * 0.04, out)
            box(a0 + 0.05, a1 - 0.05, gl, gh, z_sill + 0.05,
                z_sill + WIN_H - 0.05, mats["Toy_glass_Glow"], "glow")
    else:
        box(lo, hi, a0, a1, z_sill, z_sill + WIN_H, mats["Toy_glass"], "fill")
        sl, sh = (wall, wall + side * 0.12) if side > 0 else (wall + side * 0.12, wall)
        box(sl, sh, a0 - 0.12, a1 + 0.12, z_sill - 0.13, z_sill, mats["Toy_trim"], "sill")
        if lit:
            gl, gh = (out, out + side * 0.04) if side > 0 else (out + side * 0.04, out)
            box(gl, gh, a0 + 0.05, a1 - 0.05, z_sill + 0.05,
                z_sill + WIN_H - 0.05, mats["Toy_glass_Glow"], "glow")


# 12 windows. Deliberately quiet and symmetrical; the lit set is four, spread
# across three elevations because the app's camera orbits the city and a night
# state confined to one facade is invisible from half the orbit.
#   (name, face, along, z_sill, lit)
WINDOWS = [
    ("front_up_n", "front", -4.30, Z_SILL_HI, True),
    ("front_up_c", "front", 0.00, Z_SILL_HI, False),
    ("front_up_s", "front", 4.30, Z_SILL_HI, False),
    ("front_lo_n", "front", -4.30, Z_SILL_LO, False),
    ("front_lo_s", "front", 4.30, Z_SILL_LO, True),
    ("ssw_up_r", "ssw", -3.60, Z_SILL_HI, False),
    ("ssw_up_c", "ssw", 0.00, Z_SILL_HI, True),
    ("ssw_up_f", "ssw", 3.60, Z_SILL_HI, False),
    ("ssw_lo_r", "ssw", -3.60, Z_SILL_LO, False),
    ("ssw_lo_c", "ssw", 0.00, Z_SILL_LO, False),
    ("ssw_lo_f", "ssw", 3.60, Z_SILL_LO, True),
    ("nne_up_r", "nne", 1.20, Z_SILL_HI, True),
    ("nne_up_f", "nne", 4.60, Z_SILL_HI, False),
    ("nne_lo_r", "nne", 1.20, Z_SILL_LO, False),
    ("nne_lo_f", "nne", 4.60, Z_SILL_LO, False),
    ("rear_up_c", "rear", 0.00, Z_SILL_HI, False),
    ("rear_lo_c", "rear", 0.00, Z_SILL_LO, False),
    ("rear_up_s", "rear", 4.50, Z_SILL_HI, False),
    ("rear_lo_s", "rear", 4.50, Z_SILL_LO, False),
]


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    mats = {name: make_material(name) for name in PALETTE_HEX}

    g = PLINTH_GROW

    # -------------------------------------------------- raised basement band
    # Follows the notched footprint, proud of the wall by 0.12 m so it reads as
    # a base rather than as the bottom of the stucco.
    prism_uv("basement", footprint_uv(g), 0.0, Z_PLINTH, mats["Toy_stone"])

    # ------------------------------------------------------------ the walls
    # ONE closed solid on the notched hexagonal footprint. Built as two
    # rectangles in the first pass, which left a bevel groove running down the
    # centre of the street elevation where their coplanar front faces met — a
    # crack, from the camera that matters. A single n-gon prism has no seam and
    # is still one closed shell for the signed-volume normals test.
    prism_uv("walls", footprint_uv(0.0), Z_PLINTH, Z_EAVE, mats["Toy_white"])

    # ---------------------------------------------------------- eave fascia
    # A heavy band grown EAVE_OVERHANG outward from the full rectangle. This
    # is the single most important detail on the building at city scale: it is
    # what turns a red pyramid into a tile roof.
    band_uv(
        "eave_fascia",
        U_MIN,
        U_MAX,
        V_MIN,
        V_MAX,
        Z_EAVE - FASCIA_D,
        Z_EAVE,
        EAVE_OVERHANG,
        mats["Toy_trim"],
    )

    # ------------------------------------------------------------- the hip
    # One hip over the full 13.72 x 12.79 m envelope. At the eave line the u
    # span (14.82 m) exceeds the v span (13.89 m), so the ridge runs along u —
    # parallel to the street front — and is only 0.93 m long. Near-pyramidal,
    # which is what the aerial shows.
    ru0, ru1 = U_MIN - EAVE_OVERHANG, U_MAX + EAVE_OVERHANG
    rv0, rv1 = V_MIN - EAVE_OVERHANG, V_MAX + EAVE_OVERHANG
    hip_roof(
        "roof_hip",
        ru0,
        ru1,
        rv0,
        rv1,
        Z_EAVE,
        Z_RIDGE,
        mats["Toy_red"],
        ridge_along_u=True,
    )

    # ------------------------------------------------------- ridge/hip caps
    # The first pass rendered a large blank red pyramid: correct geometry,
    # no identity. These five raised caps are what a clay-tile hip roof
    # actually has and what makes it read as one from 300 m up. Same Toy_red
    # as the field — the line comes from the normal break, not from colour.
    inset = (rv1 - rv0) / 2.0
    vc = (rv0 + rv1) / 2.0
    r0 = (ru0 + inset, vc, Z_RIDGE)
    r1 = (ru1 - inset, vc, Z_RIDGE)
    bar_3d("roof_ridge_cap", r0, r1, CAP_W, CAP_H, mats["Toy_red"], extend=CAP_W / 2)
    for label, corner, ridge_end in (
        ("nne_rear", (ru0, rv0, Z_EAVE), r0),
        ("nne_front", (ru0, rv1, Z_EAVE), r0),
        ("ssw_rear", (ru1, rv0, Z_EAVE), r1),
        ("ssw_front", (ru1, rv1, Z_EAVE), r1),
    ):
        bar_3d(
            f"roof_hip_cap_{label}",
            corner,
            ridge_end,
            CAP_W,
            CAP_H,
            mats["Toy_red"],
            extend=CAP_W / 2,
        )

    # --------------------------------------------------------- the chimney
    # Sets the crest. Placed on the NNE half where the hip has already risen to
    # ~8.5 m, so the stack projects a natural ~1.0 m rather than standing off
    # the eave like a mast.
    hu, hv = CHIMNEY_SEC_U / 2.0, CHIMNEY_SEC_V / 2.0
    prism_uv(
        "chimney",
        rect_uv(CHIMNEY_U - hu, CHIMNEY_U + hu, CHIMNEY_V - hv, CHIMNEY_V + hv),
        Z_CHIMNEY_BASE,
        Z_CREST - 0.22,
        mats["Toy_brick"],
    )
    # Corbelled cap. A bare stack read as an orange peg in the first pass; the
    # flared cap is what makes it read as a chimney at thumbnail size.
    prism_uv(
        "chimney_cap",
        rect_uv(
            CHIMNEY_U - hu - 0.11,
            CHIMNEY_U + hu + 0.11,
            CHIMNEY_V - hv - 0.11,
            CHIMNEY_V + hv + 0.11,
        ),
        Z_CREST - 0.22,
        Z_CREST,
        mats["Toy_brick"],
    )

    # ------------------------------------------------------- the entry porch
    pu0, pu1 = -PORCH_HALF_W, PORCH_HALF_W
    pv0, pv1 = V_MAX, V_MAX + PORCH_PROJ
    prism_uv(
        "porch_slab",
        rect_uv(pu0 - 0.20, pu1 + 0.20, pv0, pv1 + 0.20),
        0.0,
        Z_PLINTH,
        mats["Toy_stone"],
    )
    prism_uv(
        "porch_step",
        rect_uv(pu0 + 0.18, pu1 - 0.18, pv1 + 0.20, pv1 + 0.68),
        0.0,
        Z_PLINTH / 2.0,
        mats["Toy_stone"],
    )
    for sign in (-1, 1):
        cu = sign * (PORCH_HALF_W - PORCH_POST / 2 - 0.06)
        prism_uv(
            f"porch_post_{'s' if sign > 0 else 'n'}",
            rect_uv(cu - PORCH_POST / 2, cu + PORCH_POST / 2,
                    pv1 - PORCH_POST - 0.06, pv1 - 0.06),
            Z_PLINTH,
            Z_PORCH_CANOPY,
            mats["Toy_trim"],
        )
    prism_uv(
        "porch_canopy",
        rect_uv(pu0 - 0.15, pu1 + 0.15, pv0 - 0.12, pv1 + 0.15),
        Z_PORCH_CANOPY,
        Z_PORCH_CANOPY + PORCH_CANOPY_T,
        mats["Toy_trim"],
    )
    phu0, phu1 = pu0 - 0.15, pu1 + 0.15
    phv0, phv1 = pv0 - 0.12, pv1 + 0.15
    hip_roof(
        "porch_hip",
        phu0,
        phu1,
        phv0,
        phv1,
        Z_PORCH_CANOPY + PORCH_CANOPY_T,
        Z_PORCH_RIDGE,
        mats["Toy_red"],
        ridge_along_u=True,
    )
    # The porch hip read as a flat red slab from directly above without its own
    # cap. Same treatment as the main roof, at a quarter of the section.
    p_inset = (phv1 - phv0) / 2.0
    p_vc = (phv0 + phv1) / 2.0
    bar_3d(
        "porch_ridge_cap",
        (phu0 + p_inset, p_vc, Z_PORCH_RIDGE),
        (phu1 - p_inset, p_vc, Z_PORCH_RIDGE),
        CAP_W * 0.75,
        CAP_H * 0.75,
        mats["Toy_red"],
        extend=CAP_W * 0.4,
    )
    # Door: a recess, not a panel — at this scale a dark hole reads as an
    # entrance and a modelled door does not.
    prism_uv(
        "door_recess",
        rect_uv(-0.62, 0.62, V_MAX - 0.16, V_MAX + 0.02),
        Z_PLINTH,
        Z_PLINTH + 2.25,
        mats["Toy_ink"],
    )
    # Porch soffit: the one architectural glow surface. A thin shell under the
    # canopy, never the canopy itself.
    prism_uv(
        "porch_soffit_glow",
        rect_uv(pu0 + 0.30, pu1 - 0.30, pv0 + 0.20, pv1 - 0.05),
        Z_PORCH_CANOPY - 0.05,
        Z_PORCH_CANOPY,
        mats["Toy_trim_Glow"],
    )

    # ----------------------------------------------------------- the windows
    for name, face, along, z_sill, lit in WINDOWS:
        window(name, face, along, z_sill, mats, lit=lit)

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.12/2. Window fills, sills, posts and glow shells are small and numerous
    # — a token softening or none at all is what keeps this well under the cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")):
            continue
        if obj.name.endswith("_sill") or obj.name.startswith(
            ("porch_post", "door_", "roof_ridge_cap", "roof_hip_cap", "porch_ridge_cap")
        ):
            bevel(obj, width=0.05, segments=1)
        else:
            bevel(obj, width=0.12, segments=2)

    recentre()
    return scene


# Metres east / north from the footprint OBB centre to the model's XY bbox
# centre, filled in by recentre(). The manifest anchor is the OBB centre moved
# by this vector, so the origin sits at the bbox centre (contract rule 2) while
# the house still lands on its real footprint.
ANCHOR_SHIFT = [0.0, 0.0]


def recentre():
    """Move the model so its XY bounding-box centre is the origin.

    The house is not symmetric about its footprint centre — the entry porch
    projects 2.1 m past the street wall while the rear has only the eave — so
    authoring on the true footprint leaves the bbox centre ~0.8 m off toward
    the boulevard. Shift the geometry and carry the same shift into the anchor,
    which keeps the house on its real footprint (AGENTS rule 5)."""
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
    lon0, lat0 = -122.4515779, 37.7973711
    lon_scale = 111320.0 * math.cos(math.radians(37.77))
    lon = lon0 + ANCHOR_SHIFT[0] / lon_scale
    lat = lat0 + ANCHOR_SHIFT[1] / 110540.0
    print(f"[build] footprint OBB centre lon/lat: {lon0} {lat0}")
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    print(f"[build] front elevation heading: {HEADING_CROSS} deg true (Presidio Blvd)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "543-presidio-blvd.blend")
    glb = os.path.join(out, "543-presidio-blvd.glb")
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
