"""Deterministic Blender build of the SF-SIM miniature Powell Street cable car.

    blender -b --python build_cable_car.py -- [--out DIR]

Writes cable-car.blend and cable-car-powell.glb next to this file (or into
--out).

AXES.  Authored in Blender metres, Z up, with the GRIPMAN'S END TOWARD +Y and
min Z = 0 at the street.  The glTF exporter's Y-up conversion maps Blender
(x, y, z) -> glTF (x, z, -y), so Blender +Y lands on glTF -Z: the exported car
matches `vehicles_manifest.json`'s "FRONT = -Z", up = +Y, wheels on the street
at min y = 0.  Verified against the shipped `commuter-bus.glb`, whose
windshield re-imports at Blender +Y (see REFERENCE.md s.7).  There are no rails
in this scene, so min y = 0 is the road surface exactly as it is for a bus.

SHAPE.  A Powell car is NOT open at both ends in the same way.  Front to rear
(REFERENCE.md s.4): a low front dash carrying the headlamp and route board; a
3.1 m open grip section where the gripman stands and passengers sit on
outward-facing benches; a 3.8 m enclosed cabin with arched-top windows; a 1.2 m
open rear platform for the conductor; a taller rear dash carrying the
destination boards.  Both ends are therefore see-through, but only the front is
a full open section.  A monitor (clerestory) deck runs the length of the roof
and carries the "POWELL & MASON Sts." letterboards - photo-confirmed, s.9.

OPENNESS IS THE SILHOUETTE, so every void is real geometry: the open section
has no side walls above the 1.30 m seat line, the roof there is carried on slim
posts, and the rear platform is open on both flanks.  Every individual object is
nevertheless a CLOSED solid (the signed-volume gate) - poles are capped
cylinders, benches are boxes, figures are stacks of boxes.

The component functions (trucks, poles, benches, band vocabulary, figures) are
written to be reused by a future double-ended California car, which shares all
of them (cable-car.md s.2.16).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- dimensions

L = 8.40            # overall length over the dash panels (27 ft 6 in)
W_OVERALL = 2.40    # width over the running boards (8 ft)
H_MONITOR = 3.18    # top of the monitor deck (10 ft 5 in)

Y_F = L / 2         # +4.20, the front (gripman) end
Y_R = -L / 2        # -4.20, the rear end

HB = 0.94           # body half-width
HR = 1.20           # running-board half-width (= W_OVERALL / 2)
HROOF = 1.18        # roof half-width
POLE_X = 1.15       # grab poles stand at the outer edge of the running board

# Longitudinal stations, front to rear.
DASH_F0, DASH_F1 = 4.02, 4.14       # front dash panel
OPEN_F0, OPEN_F1 = 0.95, 4.02       # open grip section
CAB_0, CAB_1 = -2.85, 0.95          # enclosed cabin
PLAT_0, PLAT_1 = -4.02, -2.85       # rear platform
DASH_R1, DASH_R0 = -4.02, -4.14     # rear dash panel

# Vertical stations.
Z_RAIL = 0.0
WHEEL_R = 0.28
Z_BOARD = 0.54      # top of the running boards
Z_FLOOR = 0.86      # passenger floor
Z_ROCKER = 1.10     # top of the sky-blue rocker band
Z_BELT = 1.18       # top of the cream reveal under the maroon panel
Z_PANEL = 1.66      # top of the maroon body panel
Z_SILL = 1.72       # window sill
Z_HEAD = 2.42       # window head
Z_CREAM = 2.56      # top of the cream band above the windows
Z_EAVE = 2.72       # top of the maroon roof fascia = underside of the roof
Z_ROOF = 2.86       # top of the main roof slab
Z_MON = H_MONITOR   # top of the monitor deck

Z_SEAT = 1.28       # bench seat pan top
Z_OPENSIDE = 1.30   # top of the open section's low side panel

GAUGE = 1.067       # 3 ft 6 in narrow gauge - the wheels sit visibly narrow
AXLE_F, AXLE_R = 1.80, -1.40        # rigid four-wheel truck, wheelbase 3.20 m

POST_Y = (1.10, 2.05, 3.00, 3.95)   # open-section roof posts
PLAT_POST_Y = (-2.90, -3.95)        # rear-platform roof posts
POLE_Y = POST_Y + PLAT_POST_Y       # a grab pole outboard of every post

# ------------------------------------------------------------------- palette
#
# Contract palette from .agents/skills/sf-asset-check/SKILL.md, with three
# deliberate off-palette entries recorded as WARNs in REPORT.md:
#
#   Toy_maroon  the livery IS the identity, and Toy_brick #c96f4a is a warm
#               terracotta that reads as a brick building, not as a cable car.
#   Toy_oak     the varnished-wood posts, benches and window frames are half of
#               why the car reads as a 19th-century wooden vehicle.
#   Toy_p_tan   figure heads; the palette has no skin tone at all.
#
# Toy_p_* is the new saturated figure palette this asset introduces (no earlier
# artifact ships baked people); it is deliberately drawn from the contract
# accents so the riders sit inside the existing colour world.

PALETTE_HEX = {
    "Toy_maroon": "7b2230",         # OFF-PALETTE - the Powell livery
    "Toy_oak": "c08e50",            # OFF-PALETTE - varnished wood
    "Toy_cream": "f2ede3",
    "Toy_sand": "ece4d4",
    "Toy_white": "f7f4ec",
    "Toy_sky": "6db3d9",
    "Toy_ink": "3a3530",
    "Toy_glass": "2a4d73",
    "Toy_gold": "caa64a",
    "Toy_mustard": "d9a441",        # opaque destination-board stock
    "Toy_steel": "9aa0a6",
    "Toy_roofd": "45454a",          # wheels, so the running gear reads against Toy_ink
    "Toy_p_navy": "2c4a70",         # crew uniforms
    "Toy_p_coral": "e8735a",
    "Toy_p_teal": "3fa8a0",
    "Toy_p_mustard": "d9a441",
    "Toy_p_cream": "f2ede3",
    "Toy_p_tan": "d8a878",          # OFF-PALETTE - heads and hands
    "Toy_mustard_Glow": "d9a441",
    "Toy_white_Glow": "f7f4ec",
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
        # Flagged for the app's night layer; emission ships OFF per contract.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    return mat


# -------------------------------------------------------------- mesh plumbing


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


def box(name, x0, x1, y0, y1, z0, z1, mat):
    """Axis-aligned closed cuboid. The workhorse: every band, panel, bench,
    post and figure limb is one of these, which keeps every object a closed
    solid with a positive signed volume.

    The extents are sorted here rather than at every call site: a mirrored part
    written as `sx * a, sx * a + sx * b` arrives with x1 < x0 on the left side,
    which silently inverts the winding and hands the signed-volume gate a
    negative solid."""
    (x0, x1), (y0, y1), (z0, z1) = sorted((x0, x1)), sorted((y0, y1)), sorted((z0, z1))
    verts = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
    ]
    faces = [
        (3, 2, 1, 0), (4, 5, 6, 7),
        (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


def prism(name, profile, axis, a, b, mat):
    """Extrude a 2D polygon along one axis into a closed solid.

    `profile` is a CCW list of 2-tuples in the plane orthogonal to `axis`
    ('x', 'y' or 'z'); `a`/`b` are the extrusion limits. Used for the
    chamfered-top ("arched") window panes and the crowned roof section, where a
    box would lose the shape that carries the Victorian read."""
    n = len(profile)
    if axis == "y":
        lo = [(p[0], a, p[1]) for p in profile]
        hi = [(p[0], b, p[1]) for p in profile]
    elif axis == "x":
        lo = [(a, p[0], p[1]) for p in profile]
        hi = [(b, p[0], p[1]) for p in profile]
    else:
        lo = [(p[0], p[1], a) for p in profile]
        hi = [(p[0], p[1], b) for p in profile]
    verts = lo + hi
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, j + n, i + n))
    return new_mesh(name, verts, faces, [mat])


def cyl(name, cx, cy, z0, z1, r, mat, seg=8, axis="z", phase=0.0):
    """Capped cylinder - a closed solid, which is what the grab poles must be.
    Segment counts are set for the vehicle camera band (15-120 m) at the app's
    1.6x render scale; the shrink pass is told NOT to retessellate these."""
    ring = [
        (r * math.cos(phase + 2 * math.pi * i / seg), r * math.sin(phase + 2 * math.pi * i / seg))
        for i in range(seg)
    ]
    if axis == "z":
        profile = [(cx + a, cy + b) for a, b in ring]
        return prism(name, profile, "z", z0, z1, mat)
    if axis == "y":
        profile = [(cx + a, z0 + b) for a, b in ring]
        return prism(name, profile, "y", z1, r * 0 + z1, mat)  # unused branch
    raise ValueError(axis)


def disc_y(name, cx, cz, y0, y1, r, mat, seg=10, phase=0.0):
    """Capped cylinder with its axis along Y - wheels and the headlamp bezel.

    `phase` exists so a wheel can put a VERTEX on the road rather than a chord:
    with min y = 0 defined as the contact patch, a chord leaves the car floating
    a centimetre and a half above the street."""
    profile = [
        (cx + r * math.cos(phase + 2 * math.pi * i / seg),
         cz + r * math.sin(phase + 2 * math.pi * i / seg))
        for i in range(seg)
    ]
    return prism(name, profile, "y", y0, y1, mat)


def disc_x(name, cy, cz, x0, x1, r, mat, seg=12, phase=0.0):
    """Capped cylinder with its axis along X - a wheel, which turns about a
    LATERAL axis. (Authored first with the fore-aft axis, which renders a disc
    lying flat against the car side; the front elevation caught it.)"""
    profile = [
        (cy + r * math.cos(phase + 2 * math.pi * i / seg),
         cz + r * math.sin(phase + 2 * math.pi * i / seg))
        for i in range(seg)
    ]
    return prism(name, profile, "x", x0, x1, mat)


def ring_prism(name, ox, oy, ix, iy, z0, z1, mat):
    """Closed rectangular ring (outer half-extents ox/oy, inner ix/iy) - the
    gold roof-edge moulding and the pinstripe outlines, at 32 tris apiece."""
    o = [(-ox, -oy), (ox, -oy), (ox, oy), (-ox, oy)]
    i = [(-ix, -iy), (ix, -iy), (ix, iy), (-ix, iy)]
    verts = [(p[0], p[1], z0) for p in o] + [(p[0], p[1], z0) for p in i]
    verts += [(p[0], p[1], z1) for p in o] + [(p[0], p[1], z1) for p in i]
    faces = []
    for k in range(4):
        m = (k + 1) % 4
        faces.append((k, m, m + 4, k + 4))              # bottom annulus
        faces.append((k + 8, m + 8, m + 12, k + 12)[::-1])  # top annulus
        faces.append((k, k + 8, m + 8, m))              # outer wall
        faces.append((k + 4, m + 4, m + 12, k + 12))    # inner wall
    return new_mesh(name, verts, faces, [mat])


def bevel(obj, width=0.018, segments=1):
    """Miniature edge softening (style bible s.4). Applied only to the masses
    that carry the silhouette - a 1-segment bevel is ~4x the triangles of the
    box it softens, so on a 6,000-tri vehicle it has to be spent, not sprayed."""
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
    # A clamped bevel on a crowned prism leaves sub-millimetre slivers at the
    # corners where the chamfer meets the eave - 0.03 mm2 triangles whose
    # normals come back non-unit. Dissolve them here rather than shipping four
    # degenerate faces and a validator warning.
    bmesh.ops.dissolve_degenerate(bm, dist=2e-4, edges=bm.edges)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def glow_plate(name, x0, x1, y0, y1, z0, z1, mat, out_axis, out_sign, proud=0.035, bury=0.02):
    """A night-glow shell: a thin closed slab standing `proud` off an opaque
    surface with its back edge BURIED `bury` inside that surface.

    The loader draws _Glow materials in a separate unlit layer at
    opacity = 0.12 + 0.95 * uNight, so a glow surface is 88% transparent by
    day. Burying the back face means the daytime see-through never reveals the
    shell's own edges (transit README, "No vehicle has a _Glow material today")."""
    lo, hi = {"x": (x0, x1), "y": (y0, y1), "z": (z0, z1)}[out_axis]
    if out_sign > 0:
        lo, hi = hi - bury, hi + proud
    else:
        lo, hi = lo - proud, lo + bury
    if out_axis == "x":
        return box(name, lo, hi, y0, y1, z0, z1, mat)
    if out_axis == "y":
        return box(name, x0, x1, lo, hi, z0, z1, mat)
    return box(name, x0, x1, y0, y1, lo, hi, mat)


# ------------------------------------------------------- component functions
#
# Everything below is written per family so the deferred double-ended
# California car (cable-car.md s.2.16) can reuse it wholesale: it differs only
# in length, in having a grip section at both ends, and in having no enclosed
# rear platform.


def running_gear():
    """Rigid four-wheel truck, narrow gauge, plus the grip shank reaching down
    toward a street that has no slot in it (transit README: no rails, no cable
    slot anywhere in this set)."""
    ink = material("Toy_ink")
    hw = GAUGE / 2
    for tag, ay in (("f", AXLE_F), ("r", AXLE_R)):
        for side, sx in (("l", -1), ("r", 1)):
            disc_x(f"wheel_{tag}{side}", ay, WHEEL_R, sx * (hw - 0.06), sx * (hw + 0.06),
                   WHEEL_R, material("Toy_roofd"), seg=12, phase=-math.pi / 2)
        box(f"axle_{tag}", -hw, hw, ay - 0.045, ay + 0.045, 0.24, 0.32, ink)
    for side, sx in (("l", -1), ("r", 1)):
        box(f"truckframe_{side}", sx * 0.60, sx * 0.66, AXLE_R - 0.30, AXLE_F + 0.30,
            0.30, 0.52, ink)
    # Underframe sill and floor: the visible dark band under the body.
    box("underframe", -0.90, 0.90, DASH_R1 + 0.02, DASH_F0 - 0.02, 0.60, 0.78, ink)
    box("floor", -HB, HB, DASH_R1, DASH_F0, 0.78, Z_FLOOR, material("Toy_oak"))
    # Grip shank - the mechanical story, reaching for a cable that is not here.
    box("grip_shank", -0.07, 0.07, 3.30, 3.52, 0.08, 0.60, ink)
    box("grip_shoe", -0.11, 0.11, 3.26, 3.56, 0.08, 0.16, ink)
    # Fenders under each dash.
    box("bumper_f", -0.86, 0.86, DASH_F0 - 0.04, DASH_F1 + 0.06, 0.46, 0.60, ink)
    box("bumper_r", -0.86, 0.86, DASH_R0 - 0.06, DASH_R1 + 0.04, 0.46, 0.60, ink)


def running_boards():
    """The exposed boards riders stand on, at 0.54 m above the street - one of
    the two strongest recognition cues once figures are standing on them."""
    ink = material("Toy_ink")
    sky = material("Toy_sky")
    for side, sx in (("l", -1), ("r", 1)):
        lo, hi = sorted((sx * HB, sx * HR))
        box(f"runboard_{side}", lo, hi, -4.00, 4.00, 0.46, Z_BOARD, ink)
        # The pale "TWO STANDEES ONLY" strip on the board's outer face; at city
        # distance this reads as the lettering it stands in for (style s.26).
        lo2, hi2 = sorted((sx * (HR - 0.012), sx * HR))
        box(f"runboard_strip_{side}", lo2, hi2, -3.90, 3.90, 0.485, 0.525, sky)


def body_bands(y0, y1, z_top, tag, with_rocker_letters=True, sides_only=False):
    """The Victorian horizontal band vocabulary, as a stack of closed boxes.

    Bottom to top: sky-blue rocker carrying the SAN FRANCISCO MUNICIPAL RAILWAY
    lettering, a cream reveal, then the maroon panel. Each band is its own
    solid and each steps in or out a few millimetres, so the shadow lines that
    say "panelled wood" cost nothing but the bands themselves."""
    sky = material("Toy_sky")
    cream = material("Toy_cream")
    maroon = material("Toy_maroon")
    ink = material("Toy_ink")
    # An open section's low panel is TWO SIDE WALLS. Built full width it is a
    # solid slab through the middle of the car: it buries the bench seats
    # (which then read as missing, and which the shrink pass rightly deleted),
    # and it quietly fills the lower half of the void that is this vehicle's
    # whole identity.
    spans = (
        [(-HB, -HB + 0.07), (HB - 0.07, HB)] if sides_only else [(-HB, HB)]
    )
    for i, (a, b) in enumerate(spans):
        sfx = f"{tag}" if not sides_only else f"{tag}{'lr'[i]}"
        box(f"rocker_{sfx}", a, b, y0, y1, Z_FLOOR, Z_ROCKER, sky)
        inset = 0.01 if not sides_only else 0.0
        box(f"reveal_{sfx}", a + inset, b - inset, y0, y1, Z_ROCKER, Z_BELT, cream)
        if z_top > Z_BELT:
            box(f"panel_{sfx}", a, b, y0, y1, Z_BELT, z_top, maroon)
    if with_rocker_letters:
        for side, sx in (("l", -1), ("r", 1)):
            lo, hi = sorted((sx * HB, sx * (HB + 0.014)))
            box(f"rockertext_{tag}_{side}", lo, hi, y0 + 0.20, y1 - 0.20,
                0.92, 1.02, ink)


def pinstripe(tag, y0, y1, z0, z1):
    """Gold rectangular outline on a maroon panel - the single cheapest thing
    that separates a Victorian car body from a shipping crate."""
    gold = material("Toy_gold")
    t = 0.022
    for side, sx in (("l", -1), ("r", 1)):
        lo, hi = sorted((sx * (HB + 0.002), sx * (HB + 0.016)))
        box(f"pin_{tag}_{side}_b", lo, hi, y0, y1, z0, z0 + t, gold)
        box(f"pin_{tag}_{side}_t", lo, hi, y0, y1, z1 - t, z1, gold)
        box(f"pin_{tag}_{side}_0", lo, hi, y0, y0 + t, z0, z1, gold)
        box(f"pin_{tag}_{side}_1", lo, hi, y1 - t, y1, z0, z1, gold)


def arched_window(name, sx, y0, y1, mat, chamfer=0.14, x_lo=None, x_hi=None,
                  inset=0.0):
    """A window bay with a chamfered top - the miniature translation of the
    Powell car's arched sash (cable-car.md s.2.6, "window arches become a
    simple chamfered top")."""
    z0, z1 = Z_SILL + 0.03 + inset, Z_HEAD - 0.03 - inset
    y0, y1 = y0 + inset, y1 - inset
    profile = [
        (y0, z0), (y1, z0), (y1, z1 - chamfer),
        (y1 - chamfer, z1), (y0 + chamfer, z1), (y0, z1 - chamfer),
    ]
    a = sx * (HB - 0.05) if x_lo is None else x_lo
    b = sx * (HB - 0.005) if x_hi is None else x_hi
    lo, hi = sorted((a, b))
    return prism(name, profile, "x", lo, hi, mat)


def enclosed_cabin():
    """Body sides, arched windows, roof fascia and the two end walls, each end
    wall pierced by a full-height doorway so you can see straight through the
    car end to end."""
    oak = material("Toy_oak")
    glass = material("Toy_glass")
    cream = material("Toy_cream")
    maroon = material("Toy_maroon")

    body_bands(CAB_0, CAB_1, Z_PANEL, "cab")
    pinstripe("cab", CAB_0 + 0.22, CAB_1 - 0.22, Z_BELT + 0.07, Z_PANEL - 0.07)

    # Window band: oak sill, four bays per side between five oak pillars, oak
    # head beam, then the cream band and the maroon fascia.
    box("sill", -HB - 0.015, HB + 0.015, CAB_0, CAB_1, Z_PANEL, Z_SILL, oak)
    bays = 4
    span = (CAB_1 - CAB_0 - 0.22) / bays
    pillars = [CAB_0 + 0.11 + span * k for k in range(bays + 1)]
    for side, sx in (("l", -1), ("r", 1)):
        lo, hi = sorted((sx * (HB - 0.05), sx * HB))
        for k, py in enumerate(pillars):
            w = 0.10 if 0 < k < bays else 0.13
            box(f"pillar_{side}_{k}", lo, hi, py - w / 2, py + w / 2, Z_SILL, Z_HEAD, oak)
        for k in range(bays):
            arched_window(f"win_{side}_{k}", sx,
                          pillars[k] + 0.06, pillars[k + 1] - 0.06, glass)
            # A lit pane shell 3.5 cm proud of the opaque glass. The plan's
            # glow table lists three surfaces; without this fourth the enclosed
            # half of the car goes black at night while the open half glows,
            # which is the opposite of the "warm light seen THROUGH the car"
            # the plan asks the night state to deliver.
            arched_window(f"winglow_{side}_{k}", sx,
                          pillars[k] + 0.06, pillars[k + 1] - 0.06,
                          material("Toy_mustard_Glow"), inset=0.055,
                          x_lo=sx * (HB - 0.015), x_hi=sx * (HB + 0.035))
        box(f"corner_{side}_0", lo, hi, CAB_0, CAB_0 + 0.11, Z_SILL, Z_HEAD, oak)
        box(f"corner_{side}_1", lo, hi, CAB_1 - 0.11, CAB_1, Z_SILL, Z_HEAD, oak)
    box("head_beam", -HB, HB, CAB_0, CAB_1, Z_HEAD, Z_CREAM, cream)
    box("fascia_cab", -HB - 0.02, HB + 0.02, CAB_0, CAB_1, Z_CREAM, Z_EAVE, maroon)

    # End walls with a doorway: two pillars plus a header, so the opening is a
    # real void rather than a dark rectangle.
    for tag, wy in (("f", CAB_1), ("r", CAB_0)):
        y0, y1 = (wy - 0.10, wy) if tag == "f" else (wy, wy + 0.10)
        for side, sx in (("l", -1), ("r", 1)):
            lo, hi = sorted((sx * 0.62, sx * HB))
            box(f"endpost_{tag}_{side}", lo, hi, y0, y1, Z_FLOOR, Z_HEAD, maroon)
        box(f"endhead_{tag}", -0.62, 0.62, y0, y1, Z_HEAD - 0.22, Z_CREAM, cream)

    # Longitudinal bench seats inside, visible through the glass and the ends.
    for side, sx in (("l", -1), ("r", 1)):
        lo, hi = sorted((sx * 0.50, sx * 0.90))
        box(f"cabbench_{side}", lo, hi, CAB_0 + 0.14, CAB_1 - 0.14, 1.16, Z_SEAT, oak)


def open_section():
    """The 3.1 m open grip section: low side panels, slim roof posts with
    decorative brackets, and back-to-back outward-facing benches.

    No side walls above 1.30 m. This void, and the gaps between the posts, are
    the whole identity of the vehicle - protected at every simplification step."""
    oak = material("Toy_oak")
    body_bands(OPEN_F0, OPEN_F1, Z_OPENSIDE, "open", sides_only=True)

    for side, sx in (("l", -1), ("r", 1)):
        lo, hi = sorted((sx * (HB - 0.09), sx * HB))
        for k, py in enumerate(POST_Y):
            box(f"post_{side}_{k}", lo, hi, py - 0.045, py + 0.045, Z_OPENSIDE, Z_EAVE, oak)
            # Curved spandrel brackets at the post heads, squared into the toy
            # vocabulary: two stepped blocks read as a bracket at 120 m.
            box(f"bracket_{side}_{k}_a", lo, hi, py - 0.20, py + 0.20, Z_EAVE - 0.09, Z_EAVE, oak)
            box(f"bracket_{side}_{k}_b", lo, hi, py - 0.13, py + 0.13, Z_EAVE - 0.15,
                Z_EAVE - 0.09, oak)

    # Outward-facing benches: one longitudinal back down the centreline with a
    # seat pan on each side (Wikipedia: "outward-facing seats flanking the
    # gripman"). Three closed boxes, and the shape reads instantly from above.
    box("bench_back", -0.11, 0.11, 1.05, 3.05, Z_SEAT, 1.86, oak)
    for side, sx in (("l", -1), ("r", 1)):
        lo, hi = sorted((sx * 0.11, sx * 0.92))
        box(f"bench_pan_{side}", lo, hi, 1.05, 3.05, 1.18, Z_SEAT, oak)


def rear_platform():
    """The conductor's open platform: low side panels, two posts per side, and
    the accordion gate reduced to a single dark slatted panel."""
    oak = material("Toy_oak")
    ink = material("Toy_ink")
    body_bands(PLAT_0, PLAT_1, Z_OPENSIDE, "plat", sides_only=True)
    for side, sx in (("l", -1), ("r", 1)):
        lo, hi = sorted((sx * (HB - 0.09), sx * HB))
        for k, py in enumerate(PLAT_POST_Y):
            box(f"platpost_{side}_{k}", lo, hi, py - 0.045, py + 0.045,
                Z_OPENSIDE, Z_EAVE, oak)
            box(f"platbracket_{side}_{k}", lo, hi, py - 0.16, py + 0.16,
                Z_EAVE - 0.09, Z_EAVE, oak)
        # Folding gate at the cabin end of the platform.
        box(f"gate_{side}", lo, hi, PLAT_1 - 0.06, PLAT_1 + 0.02, Z_OPENSIDE, 1.92, ink)


def roof():
    """Crowned main roof, gold edge moulding, and the monitor (clerestory) deck
    that carries the destination letterboards.

    The camera looks down at 42 degrees, so this small surface is fully visible
    and must not be a blank slab (style bible s.10)."""
    sand = material("Toy_sand")
    oak = material("Toy_oak")
    gold = material("Toy_gold")

    # A maroon fascia band carrying a gently crowned cream cap, with the gold
    # moulding on the joint. The roof is a fully visible surface at 42 degrees
    # and a single cream slab would be the blank rooftop the style bible bans.
    box("roof_fascia", -HROOF, HROOF, -L / 2, L / 2, Z_EAVE, Z_EAVE + 0.08,
        material("Toy_maroon"))
    section = [
        (-HROOF, Z_EAVE + 0.08), (HROOF, Z_EAVE + 0.08), (HROOF, Z_ROOF - 0.05),
        (HROOF - 0.16, Z_ROOF), (-HROOF + 0.16, Z_ROOF), (-HROOF, Z_ROOF - 0.05),
    ]
    prism("roof_slab", section, "y", -L / 2, L / 2, sand)
    ring_prism("roof_moulding", HROOF + 0.025, L / 2, HROOF - 0.06, L / 2 - 0.09,
               Z_EAVE + 0.055, Z_EAVE + 0.115, gold)

    # Monitor deck: a raised centre section with its own roof, arched at the
    # ends. Photo-confirmed present (REFERENCE.md s.9) - it is the roof's only
    # real feature, and it is what carries the line identification.
    box("monitor_wall", -0.60, 0.60, -3.72, 3.72, Z_ROOF - 0.03, Z_MON - 0.14, oak)
    for tag, sy in (("f", 1), ("r", -1)):
        cap = [
            (-0.60, Z_ROOF - 0.03), (0.60, Z_ROOF - 0.03), (0.60, Z_MON - 0.20),
            (0.44, Z_MON - 0.14), (-0.44, Z_MON - 0.14), (-0.60, Z_MON - 0.20),
        ]
        prism(f"monitor_end_{tag}", cap, "y", sy * 3.72, sy * 3.94, material("Toy_cream"))
    mon = [
        (-0.66, Z_MON - 0.14), (0.66, Z_MON - 0.14), (0.66, Z_MON - 0.05),
        (0.53, Z_MON), (-0.53, Z_MON), (-0.66, Z_MON - 0.05),
    ]
    prism("monitor_deck", mon, "y", -3.98, 3.98, sand)
    # Roof furniture, photo-verified on car 23: the gong on the front roof and
    # the hinged monitor vent panels. Small, but they are the difference
    # between a designed rooftop and the blank slab s.10 forbids.
    for k in range(4):
        box(f"monitor_vent_{k}", -0.36, 0.36, 1.90 - k * 1.55, 2.32 - k * 1.55,
            Z_MON - 0.045, Z_MON - 0.012, material("Toy_maroon"))
    # The gong sits on the main roof beside the monitor, as photographed - and
    # below Z_MON, so the published 10 ft 5 in stays the model's height.
    disc_x("roof_bell", 3.50, Z_ROOF + 0.10, 0.74, 0.96, 0.10, gold, seg=10)
    # Clerestory lights along the monitor wall over the ENCLOSED half - the
    # roof's only real feature, and what stops it reading as a blank slab from
    # the 42-degree camera. The open half of the monitor carries the
    # letterboard instead, exactly as the photographs show.
    for side, sx in (("l", -1), ("r", 1)):
        lo, hi = sorted((sx * 0.60, sx * 0.622))
        for k in range(5):
            cy = -3.30 + k * 0.86
            box(f"clerestory_{side}_{k}", lo, hi, cy - 0.27, cy + 0.27,
                Z_ROOF + 0.04, Z_MON - 0.19, material("Toy_glass"))


def destination_boards():
    """Line identification: the two side letterboards on the monitor deck and
    the route boards on both dashes. Each is an opaque plate with a
    Toy_mustard_Glow shell 3.5 cm proud and its back edge buried."""
    ink = material("Toy_ink")
    cream = material("Toy_cream")
    board = material("Toy_mustard")
    glow = material("Toy_mustard_Glow")

    # Side letterboards ("POWELL & MASON Sts.") on the monitor flanks, over the
    # open section, exactly where the photographs put them.
    for side, sx in (("l", -1), ("r", 1)):
        lo, hi = sorted((sx * 0.60, sx * 0.65))
        box(f"letterboard_{side}", lo, hi, 0.20, 3.70, Z_ROOF + 0.02, Z_MON - 0.17, board)
        glow_plate(f"letterboard_glow_{side}", lo, hi, 0.25, 3.65,
                   Z_ROOF + 0.05, Z_MON - 0.20, glow, "x", 1 if sx > 0 else -1)
        # An ink bar standing in for "POWELL & MASON Sts." - at 120 m the
        # lettering is a dark line on a light board, so that is what is built
        # (style bible s.26, deliberate compression).
        # Outboard of the glow shell (which stands 3.5 cm proud), not inside it:
        # buried, the lettering reads through 12%-opaque glow by day and is
        # invisible at night, and the shrink pass deletes it as interior.
        box(f"letterboard_text_{side}", sx * 0.700, sx * 0.712, 0.45, 3.45,
            Z_ROOF + 0.09, Z_MON - 0.24, ink)

    # Front dash route board.
    box("routeboard_f", -0.78, -0.16, DASH_F1, DASH_F1 + 0.016, 0.82, 1.16, board)
    glow_plate("routeboard_f_glow", -0.74, -0.20, DASH_F1, DASH_F1 + 0.016, 0.86, 1.12,
               glow, "y", 1)

    # Rear dash destination board - the tall one, with the number panel.
    box("routeboard_r", -0.40, 0.40, DASH_R0 - 0.016, DASH_R0, 0.80, 1.24, board)
    glow_plate("routeboard_r_glow", -0.35, 0.35, DASH_R0 - 0.016, DASH_R0, 0.84, 1.20,
               glow, "y", -1)
    box("numberplate_r", 0.46, 0.78, DASH_R0 - 0.016, DASH_R0, 0.86, 1.18,
        material("Toy_gold"))


def dashes_and_lamp():
    """Front and rear dash panels (banded white/maroon), the single forward
    headlamp with its Toy_white_Glow lens, and the rear tail lamps."""
    white = material("Toy_white")
    maroon = material("Toy_maroon")
    gold = material("Toy_gold")

    for tag, y0, y1, ztop in (("f", DASH_F0, DASH_F1, 1.30), ("r", DASH_R0, DASH_R1, 1.42)):
        lo, hi = sorted((y0, y1))
        box(f"dash_{tag}_lo", -HB, HB, lo, hi, 0.58, 0.72, maroon)
        box(f"dash_{tag}_mid", -HB - 0.01, HB + 0.01, lo, hi, 0.72, ztop - 0.12, white)
        box(f"dash_{tag}_hi", -HB, HB, lo, hi, ztop - 0.12, ztop, maroon)

    # Headlamp: gold bezel on the front dash with a glow lens standing proud.
    # The lamp is set so its glow lens lands exactly on y = L/2: the published
    # 8.40 m is over the dashes, and a headlamp that overhangs it would make
    # the manifest dims disagree with the source everyone will check.
    disc_y("lamp_bezel", 0.38, 1.02, DASH_F1 - 0.08, DASH_F1 + 0.02, 0.115, gold, seg=10)
    disc_y("lamp_glass", 0.38, 1.02, DASH_F1 - 0.02, DASH_F1 + 0.025, 0.085,
           material("Toy_white"), seg=10)
    disc_y("lamp_lens", 0.38, 1.02, DASH_F1 - 0.005, DASH_F1 + 0.06, 0.075,
           material("Toy_white_Glow"), seg=10)
    # Roof-corner tail lamps at the rear, the small red-lamp cue in the photos.
    for sx in (-1, 1):
        box(f"taillamp_{'r' if sx > 0 else 'l'}", sx * 0.74, sx * 0.74 + sx * 0.10,
            DASH_R0 + 0.02, DASH_R0 + 0.10, Z_EAVE - 0.16, Z_EAVE - 0.04, gold)


def levers():
    """The gripman's controls: the tall grip lever, the wheel-brake lever and
    the red slot-brake lever, on a low housing. With no slot in the street the
    grip reads as a lever and a housing, which is exactly what it looks like
    from the app camera anyway."""
    ink = material("Toy_ink")
    steel = material("Toy_steel")
    box("lever_housing", -0.30, 0.30, 3.28, 3.66, Z_FLOOR, 1.02, ink)

    def lever(name, x, y_bot, y_top, z_top, mat, w=0.038):
        """A raked lever as a closed slab between two stations."""
        verts = [
            (x - w, y_bot - w, 1.00), (x + w, y_bot - w, 1.00),
            (x + w, y_bot + w, 1.00), (x - w, y_bot + w, 1.00),
            (x - w, y_top - w, z_top), (x + w, y_top - w, z_top),
            (x + w, y_top + w, z_top), (x - w, y_top + w, z_top),
        ]
        faces = [
            (3, 2, 1, 0), (4, 5, 6, 7),
            (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
        ]
        return new_mesh(name, verts, faces, [mat])

    lever("grip_lever", 0.00, 3.44, 3.16, 1.82, steel, 0.045)
    lever("brake_lever", 0.26, 3.50, 3.30, 1.60, steel)
    lever("slot_lever", -0.26, 3.50, 3.34, 1.52, material("Toy_maroon"))
    # The conductor's rear brake lever.
    lever("cond_lever", 0.28, -3.46, -3.30, 1.50, steel)


def grab_poles():
    """Vertical brass grab poles outboard of the body, running board to roof.

    Thickened well past scale (r = 45 mm against a real ~20 mm) on purpose:
    they are what make the open sections read as OPEN rather than as holes, and
    they are what the standing riders are visibly holding."""
    gold = material("Toy_gold")
    pole_mat = material("Toy_ink")
    for side, sx in (("l", -1), ("r", 1)):
        for k, py in enumerate(POLE_Y):
            cyl(f"pole_{side}_{k}", sx * POLE_X, py, 0.50, Z_EAVE + 0.02, 0.045,
                pole_mat, seg=8)
    # Waist-high handrails along the open section, between the posts.
    for side, sx in (("l", -1), ("r", 1)):
        lo, hi = sorted((sx * (POLE_X - 0.016), sx * (POLE_X + 0.016)))
        box(f"handrail_{side}", lo, hi, POST_Y[0], POST_Y[-1], 1.86, 1.94, gold)


def interior_glow():
    """The lit cabin ceiling - the highest-value glow surface in the transit
    set, because on an open car you see the warm light THROUGH the vehicle
    rather than reflected off it. Opaque ceiling slab first, glow shell 4 cm
    proud below it with its top buried inside the slab."""
    box("ceiling", -0.88, 0.88, -3.90, 3.90, 2.62, Z_EAVE, material("Toy_cream"))
    glow_plate("ceiling_glow", -0.80, 0.80, -3.80, 3.80, 2.62, Z_EAVE,
               material("Toy_mustard_Glow"), "z", -1, proud=0.04, bury=0.025)


# ------------------------------------------------------------------- figures
#
# The exception to the usual "no people in the GLB" rule, and the reason it is
# an exception: a cable car without riders on the running boards is a small
# wooden shed. Chunky toy silhouettes - no faces, no fingers - at ~60 tris for
# a standing figure and ~48 for a seated one.


def standing_figure(name, x, y, z0, coat, trousers, reach=None, height=1.60):
    """Closed-box toy figure. `reach` is the x of a pole to put an arm on."""
    tan = material("Toy_p_tan")
    legs_h = z0 + height * 0.50
    torso_h = z0 + height * 0.85
    head_h = z0 + height
    box(f"{name}_legs", x - 0.125, x + 0.125, y - 0.10, y + 0.10, z0, legs_h, trousers)
    box(f"{name}_torso", x - 0.155, x + 0.155, y - 0.12, y + 0.12, legs_h, torso_h, coat)
    box(f"{name}_head", x - 0.095, x + 0.095, y - 0.085, y + 0.085, torso_h, head_h, tan)
    for tag, sx in (("l", -1), ("r", 1)):
        ax = x + sx * 0.205
        if reach is not None and (reach - x) * sx > 0:
            # The outboard arm rises to the grab pole - the pose that reads as
            # "hanging on" from 120 m. Kept at least 0.11 m long so a rider
            # standing almost against the pole still shows an arm.
            box(f"{name}_arm_{tag}", x + sx * 0.06, reach + sx * 0.05,
                y - 0.055, y + 0.055, torso_h - 0.14, torso_h + 0.12, coat)
        else:
            box(f"{name}_arm_{tag}", ax - 0.045, ax + 0.045, y - 0.055, y + 0.055,
                legs_h + 0.04, torso_h - 0.02, coat)


def seated_figure(name, x, y, facing, coat, trousers):
    """A rider on an outward-facing bench: thighs out, shins down, torso up.
    `facing` is +1 for the right flank, -1 for the left."""
    tan = material("Toy_p_tan")
    knee = x + facing * 0.42
    box(f"{name}_thigh", *sorted((x, knee)), y - 0.11, y + 0.11, Z_SEAT, Z_SEAT + 0.13,
        trousers)
    box(f"{name}_shin", *sorted((knee - facing * 0.13, knee)), y - 0.10, y + 0.10,
        Z_FLOOR + 0.02, Z_SEAT, trousers)
    box(f"{name}_torso", *sorted((x, x + facing * 0.22)), y - 0.13, y + 0.13,
        Z_SEAT + 0.13, Z_SEAT + 0.62, coat)
    box(f"{name}_head", *sorted((x + facing * 0.03, x + facing * 0.21)),
        y - 0.09, y + 0.09, Z_SEAT + 0.62, Z_SEAT + 0.82, tan)


def crew_and_riders():
    """Gripman standing at the levers, conductor on the rear platform, three
    riders standing on the running boards holding poles, three seated on the
    open benches. Eight baked figures, ~600 triangles."""
    navy = material("Toy_p_navy")
    ink = material("Toy_ink")
    coral = material("Toy_p_coral")
    teal = material("Toy_p_teal")
    mustard = material("Toy_p_mustard")
    cream = material("Toy_p_cream")

    # Gripman - STANDING at the grip lever, facing forward, hands on the lever.
    standing_figure("gripman", -0.18, 3.52, Z_FLOOR, navy, ink, reach=0.02, height=1.66)
    # Conductor at the rear.
    standing_figure("conductor", -0.20, -3.42, Z_FLOOR, navy, ink, reach=0.30, height=1.64)

    # Standees on the running boards, each beside a grab pole. Held at x = 1.02
    # so a leaning torso still ends inside the 2.40 m width over the boards.
    standing_figure("rider_sr0", 1.055, 2.10, Z_BOARD, coral, navy, reach=POLE_X)
    standing_figure("rider_sr1", 1.055, 3.05, Z_BOARD, mustard, ink, reach=POLE_X,
                    height=1.54)
    standing_figure("rider_sl0", -1.055, 2.16, Z_BOARD, teal, navy, reach=-POLE_X)

    # Seated on the outward-facing benches.
    seated_figure("rider_br0", 0.30, 1.45, 1, cream, navy)
    seated_figure("rider_br1", 0.30, 2.60, 1, coral, ink)
    seated_figure("rider_bl0", -0.30, 1.95, -1, mustard, navy)


# ----------------------------------------------------------------- assembly


def build():
    # Start from a genuinely empty scene: Blender's startup file ships a Cube,
    # a Camera and a Light, and the Cube would export as leaked geometry.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    running_gear()
    running_boards()
    enclosed_cabin()
    open_section()
    rear_platform()
    roof()
    dashes_and_lamp()
    destination_boards()
    levers()
    grab_poles()
    interior_glow()
    crew_and_riders()

    # Bevel only the masses that carry the silhouette - a 1-segment bevel costs
    # roughly 4x the box it softens, and on a vehicle at 120 m nothing smaller
    # than the roof or a dash panel repays it.
    for name in ("roof_slab", "roof_fascia", "monitor_deck", "monitor_wall",
                 "dash_f_mid", "dash_r_mid", "dash_f_lo", "dash_r_lo",
                 "panel_cab", "rocker_cab", "underframe", "bench_back",
                 "bench_pan_l", "bench_pan_r", "sill", "head_beam", "fascia_cab"):
        obj = bpy.data.objects.get(name)
        if obj:
            bevel(obj, width=0.016, segments=1)
    return scene


def recenter_and_report():
    """Centre in the X/Y footprint (X/Z once exported) and drop the wheel
    contact patch onto z = 0 - the street surface, exactly like a bus."""
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
    dims = [round(mx[i] - mn[i], 3) for i in range(3)]
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] blender dims (x,y,z)={dims}")
    print(f"[build] gltf dims (x,y,z)={[dims[0], dims[2], dims[1]]}")
    print(f"[build] recentered by {[round(v, 4) for v in center]}")
    print("[build] front = Blender +Y  ->  glTF -Z (gripman's end)")
    return tris, dims


def export(out):
    blend = os.path.join(out, "cable-car.blend")
    # The AUTHORED export. make.sh then runs the shrink and the meshopt intake
    # over it and writes the shipped cable-car-powell.glb; the authored file is
    # what validate_cable_car.py checks per object, because the shrink's
    # join-by-material step dissolves the per-object structure on purpose.
    glb = os.path.join(out, "cable-car-powell.authored.glb")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    # Leak-proof: a temp scene holding only the export objects, exported with
    # use_active_scene so no other scene's selection can ride along.
    export_scene = bpy.data.scenes.new("EXPORT_TMP")
    src = bpy.context.window.scene
    for o in list(src.objects):
        export_scene.collection.objects.link(o)
    bpy.context.window.scene = export_scene
    bpy.ops.export_scene.gltf(
        filepath=glb,
        export_format="GLB",
        export_apply=True,
        export_yup=True,
        use_active_scene=True,
        use_selection=False,
        export_cameras=False,
        export_lights=False,
        export_animations=False,
        export_skins=False,
        export_morph=False,
        export_materials="EXPORT",
        export_image_format="NONE",
    )
    bpy.context.window.scene = src
    print(f"[build] wrote {blend}")
    print(f"[build] wrote {glb}")


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)
    build()
    recenter_and_report()
    export(out)


if __name__ == "__main__":
    main()
