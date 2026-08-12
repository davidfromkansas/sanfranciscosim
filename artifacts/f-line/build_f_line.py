"""Deterministic Blender build of the SF-SIM miniature F-line PCC streetcar.

    blender -b --python build_f_line.py -- [--out DIR]

Writes f-line.blend and f-line-pcc.authored.glb next to this file (or into
--out).

THE CAR.  Muni 1050 class: ex-Philadelphia Transportation Company PCCs built
1947-48 by St. Louis Car Company, 13 operational, the largest single class on
the F line and SINGLE-ENDED (REFERENCE.md s.3).  48 ft 5 in x 8 ft 4 in x
10 ft 3 in = 14.76 x 2.54 x 3.12 m over the anti-climbers, rail to roof.

AXES.  Authored in Blender metres, Z up, with the CAB END TOWARD +Y and min Z = 0
at the wheel contact patch.  The glTF exporter's Y-up conversion maps Blender
(x, y, z) -> glTF (x, z, -y), so Blender +Y lands on glTF -Z: the exported car
matches `vehicles_manifest.json`'s "FRONT = -Z", up = +Y, wheels on the ground
at min y = 0.  Verified against the shipped `commuter-bus.glb`.

THE LIVERY SPLIT is the whole point of this asset (historic-streetcar.md s.2.6).
`Toy_body` is authored near-neutral #d8d3c8 and carries EVERY surface that
changes between the cities-series liveries; windows, roof, trucks, pole,
bumpers and headlight are ordinary fixed `Toy_*` so a per-instance multiply
cannot wash them out.  One geometry, five liveries, one draw call.

THE SHELL is one lofted solid.  A PCC's identity is the compound nose, and a
box with a chamfer is a tram, not a PCC, so the body is built by lofting
rounded-rectangle rings down the car: full section through the straight run,
then four rings tucking in and RAKING FORWARD at the bottom over the leading
1.4 m, and four blanker rings at the tail.  Every ring carries the window
NOTCH in its outline, so the glazing recess wraps the nose for free and the
front cap's notch triangles become the wrapped windscreen.  Face materials are
assigned by face-centre height against the ring's own stations, which is why
the outline puts vertices exactly on those stations.

The component functions (trucks, trolley pole, glazing pattern, glow shells)
are written to be reused by the deferred 1928 Milan Peter Witt car
(historic-streetcar.md s.2.17), which shares all of them but not the body.
"""

import contextlib
import io
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- dimensions
#
# Muni 1050 class, ex-PTC: 48'5" x 8'4" x 10'3" (REFERENCE.md s.2.1).

L = 14.76           # overall length over the anti-climbers
W = 2.54            # width over the body sides
H = 3.124           # rail to the top of the roof crown

HW = W / 2          # 1.27, body half-width
Y_F = L / 2         # +7.38, the cab end -> glTF -Z
Y_R = -L / 2        # -7.38

# The lofted shell stops short of the anti-climbers, which then reach the
# published length exactly.  The nose ring is held further back than the tail
# because the rake below pushes its LOW vertices forward by another 0.145 m;
# authored at the tail's -7.26 the fascia overhung the anti-climber and the car
# measured 14.87 m instead of 14.76 m.
Y_NOSE = 7.16
Y_TAIL = -7.26

# Vertical stations, measured from the top of rail (= min z = 0).
Z_SKIRT = 0.38      # bottom of the skirted body side.  A PCC's flanks come
                    # down over the trucks, so from any elevation the wheels
                    # only peek below this line - which is correct, and is why
                    # the underframe below it has to be a real dark bar or the
                    # car reads as floating.
Z_SILL = 1.74       # window sill = bottom of the glazing notch
Z_HEAD = 2.40       # window head = top of the glazing notch
Z_EAVE = 2.744      # where the roof crown's arc starts; below it is the
                    # letterboard band, above it is roof
Z_ROOF = H

NOTCH = 0.055       # how far the glazing band is recessed into the flank
NOTCH_CHAM = 0.05   # the recess is CHAMFERED in, not stepped square.  Partly
                    # because an angled reveal reads as a window frame, but
                    # mostly because a square step puts two ring vertices at
                    # the same height, and the end caps are tiled as horizontal
                    # rungs between the left and right halves of the outline -
                    # equal heights collapse a rung into a zero-area quad.

R_BOT = 0.16        # rocker chamfer radius
R_TOP = H - Z_EAVE  # 0.38, the roof crown radius

WHEEL_R = 0.33      # 26 in wheels
GAUGE = 1.435       # standard gauge - visibly wider than the cable car's 1.067
TRUCK_Y = 3.30      # truck centres, 21 ft apart
AXLE_DY = 0.95      # PCC truck wheelbase 75 in

POLE_BASE_Y = -2.40  # the trolley pole stands a third of the way back

# ------------------------------------------------------------------- palette
#
# Contract palette from .agents/skills/sf-asset-check/SKILL.md.  One entry is
# this asset's sanctioned exception and one is an off-palette WARN:
#
#   Toy_body   THE TINTED SURFACE.  Authored at the kit's near-neutral #d8d3c8
#              so a per-instance multiply lands on the palette entry rather
#              than a muddied version of it (app/src/kitfleet.js BODY_BASE).
#              Allowed on this asset only, on the livery panels only.
#   Toy_red_Glow  #c4453c is the contract's `red`; used as a glow it is a new
#              name, not a new colour.

PALETTE_HEX = {
    "Toy_body": "d8d3c8",           # TINTABLE - the livery panels
    "Toy_cream": "f2ede3",          # fixed letterboard band above the windows
    "Toy_ink": "3a3530",            # underframe, trucks, reveals, doors, pole base
    "Toy_glass": "2a4d73",          # side windows, windscreen, rear window
    # The roof is SILVER, not dark.  Both because it is right - Baltimore's
    # 1063 wears a "Pearl gray roof" and Dallas's 1009 a "silver roof"
    # (REFERENCE.md s.4) - and because the app's camera is 42 degrees down: a
    # charcoal lid on a 14.76 m object swallowed the whole aerial silhouette in
    # the first review render and the livery could not be read at all.
    "Toy_steel": "9aa0a6",          # roof, anti-climbers, headlight bezel, pole
    "Toy_roofd": "45454a",          # ventilators, drip rails, wheels
    "Toy_white_Glow": "f7f4ec",     # the single central headlight
    "Toy_mustard_Glow": "d9a441",   # destination sign, lit interior ceiling
    "Toy_red_Glow": "c4453c",       # tail lights
}

# The reveal material used inside the glazing notch, by longitudinal station.
# The windscreen wraps the nose, so the notch there is glass rather than a
# dark reveal; the same is true of the rear window on this single-ended car.
GLASS_WRAP_FRONT = 6.20
GLASS_WRAP_REAR = -6.55


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
    # Winding is never hand-managed: every part is a closed manifold, so the
    # normals are recomputed outward here and the signed-volume gate in
    # validate_f_line.py proves it stuck.
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.shade_flat()
    return obj


def box(name, x0, x1, y0, y1, z0, z1, mat):
    """Axis-aligned closed cuboid - the workhorse for every panel, bumper,
    plinth and vent.  Extents are sorted here rather than at the call sites: a
    mirrored part written as `sx * a, sx * b` arrives with x1 < x0 on the left
    side, which inverts the winding."""
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
    """Extrude a 2D polygon along one axis into a closed solid."""
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


def disc_y(name, cx, cz, y0, y1, r, mat, seg=10, phase=0.0):
    """Capped cylinder with its axis along Y - the headlight bezel and lens."""
    profile = [
        (cx + r * math.cos(phase + 2 * math.pi * i / seg),
         cz + r * math.sin(phase + 2 * math.pi * i / seg))
        for i in range(seg)
    ]
    return prism(name, profile, "y", y0, y1, mat)


def disc_x(name, cy, cz, x0, x1, r, mat, seg=10, phase=0.0):
    """Capped cylinder with its axis along X - a wheel turns about a LATERAL
    axis.  `phase` puts a VERTEX at the bottom of the circle rather than a
    chord: with min z = 0 defined as the contact patch, a chord leaves the car
    floating a centimetre above the ground."""
    profile = [
        (cy + r * math.cos(phase + 2 * math.pi * i / seg),
         cz + r * math.sin(phase + 2 * math.pi * i / seg))
        for i in range(seg)
    ]
    return prism(name, profile, "x", x0, x1, mat)


def bevel(obj, width=0.016, segments=1):
    """Miniature edge softening (style bible s.4).  Spent only on the chunky
    boxes that read as separate objects - the shell is not beveled because its
    lofted arcs already are the chamfer."""
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
    day.  Burying the back face means the daytime see-through never reveals the
    shell's own edges (transit README, "No vehicle has a _Glow material today").
    """
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


# ------------------------------------------------- the lofted body shell
#
# One ring outline, one loft, one solid.  Everything that makes the car a PCC
# rather than a box lives in the ring table below.

ARC_K = 4           # samples per rounded corner; 4 x 4 corners + 8 notch = 24


def outline(hw, z0, z1, notch=True):
    """CCW rounded-rectangle ring in the X-Z plane, with the glazing notch cut
    into both flanks.

    Vertices land EXACTLY on Z_SILL, Z_HEAD and the crown-arc start, because
    face materials are assigned by face-centre height and a quad that straddles
    a station would be painted the wrong colour."""
    rb = min(R_BOT, (z1 - z0) * 0.5 - 0.02, hw - 0.02)
    rt = min(R_TOP, (z1 - z0) * 0.5 - 0.02, hw - 0.02)

    def arc(cx, cz, r, a0, a1):
        return [
            (cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / (ARC_K - 1))),
             cz + r * math.sin(math.radians(a0 + (a1 - a0) * i / (ARC_K - 1))))
            for i in range(ARC_K)
        ]

    pts = []
    pts += arc(hw - rb, z0 + rb, rb, -90, 0)                 # bottom-right
    if notch:
        pts += [(hw, Z_SILL), (hw - NOTCH, Z_SILL + NOTCH_CHAM),
                (hw - NOTCH, Z_HEAD - NOTCH_CHAM), (hw, Z_HEAD)]
    pts += arc(hw - rt, z1 - rt, rt, 0, 90)                  # top-right
    pts += arc(-(hw - rt), z1 - rt, rt, 90, 180)             # top-left
    if notch:
        pts += [(-hw, Z_HEAD), (-(hw - NOTCH), Z_HEAD - NOTCH_CHAM),
                (-(hw - NOTCH), Z_SILL + NOTCH_CHAM), (-hw, Z_SILL)]
    pts += arc(-(hw - rb), z0 + rb, rb, 180, 270)            # bottom-left
    return pts


# y, half-width, bottom, top, rake.  `rake` pushes low vertices FORWARD
# (+y at the nose, handled by sign) about z = 2.0, which is what turns four
# tucking rings into a nose that leans out over the anti-climber instead of a
# cone.  s.2.7: "4-5 chamfered planes, not a lofted surface" - this is five
# rings and it costs 428 triangles.
RAKE_PIVOT = 2.0

RINGS = [
    # tail, blanker than the nose - a single-ended PCC's rear is a rounded lid
    (Y_TAIL,      1.00, 0.62, 2.94, 0.00),
    (-7.02,       1.19, 0.50, 3.05, 0.00),
    (-6.58,       1.26, 0.44, 3.11, 0.00),
    (-6.05,        HW,  Z_SKIRT, Z_ROOF, 0.00),
    # the straight run
    (5.86,         HW,  Z_SKIRT, Z_ROOF, 0.00),
    # the nose
    (6.40,        1.26, 0.44, 3.10, 0.030),
    (6.80,        1.21, 0.50, 3.04, 0.060),
    (7.02,        1.11, 0.60, 2.98, 0.090),
    (Y_NOSE,      0.94, 0.74, 2.90, 0.115),
]


def shell():
    """The lofted body: rings -> quad strips -> fan-triangulated end caps, with
    per-face materials by height and station."""
    mats = [material(n) for n in
            ("Toy_body", "Toy_cream", "Toy_steel", "Toy_ink", "Toy_glass")]
    MI = {"body": 0, "cream": 1, "roof": 2, "ink": 3, "glass": 4}

    verts = []
    rings = []
    for y, hw, z0, z1, rake in RINGS:
        pts = outline(hw, z0, z1)
        base = len(verts)
        for x, z in pts:
            verts.append((x, y + rake * (RAKE_PIVOT - z), z))
        rings.append(list(range(base, base + len(pts))))

    n = len(rings[0])
    faces = []
    for a, b in zip(rings, rings[1:]):
        for i in range(n):
            j = (i + 1) % n
            faces.append((a[i], a[j], b[j], b[i]))

    # End caps tiled as HORIZONTAL RUNGS between the right and left halves of
    # the outline, not as a fan from the ring centroid.
    #
    # The fan was the first attempt and it is wrong for a reason worth keeping:
    # face materials are assigned by face-centre height, and a fan's triangles
    # all radiate from one point at mid-height, so the front elevation came out
    # with the windscreen as a blue bowtie converging on the nose centre
    # instead of a band across it.  Rungs make every cap face a horizontal
    # strip, so the same height test paints a real wrapped windscreen, a real
    # letterboard and a real fascia.
    #
    # The outline is built symmetric and z-monotone up each side, so index i on
    # the right chain pairs with its mirror on the left and the 11 rungs tile
    # the cap exactly - the ring's own 23-0 and 11-12 edges close the bottom
    # and the top.
    half = n // 2
    for ring in (rings[0], rings[-1]):
        # left[k] is right[k]'s MIRROR: index n-1-k, not n-k.  Off by one, the
        # first rung degenerates onto itself and the topmost outline vertex is
        # never used - the closure gate in validate_f_line.py caught it as
        # body_shell being the file's only open shell.
        right = [ring[k] for k in range(half)]
        left = [ring[n - 1 - k] for k in range(half)]
        for k in range(half - 1):
            faces.append((right[k], right[k + 1], left[k + 1], left[k]))

    def material_for(centre):
        z, y = centre.z, centre.y
        if Z_SILL - 1e-4 <= z <= Z_HEAD + 1e-4:
            wrap = y > GLASS_WRAP_FRONT or y < GLASS_WRAP_REAR
            return MI["glass"] if wrap else MI["ink"]
        if z > Z_EAVE:
            return MI["roof"]
        if z > Z_HEAD:
            return MI["cream"]
        return MI["body"]

    face_mats = []
    for f in faces:
        c = Vector((0, 0, 0))
        for vi in f:
            c += Vector(verts[vi])
        c /= len(f)
        face_mats.append(material_for(c))

    return new_mesh("body_shell", verts, faces, mats, face_mats)


def nose_surface_y(z):
    """Where the nose's outer skin sits at height `z` on the centreline, so the
    headlight, sign and anti-climber can be planted ON it rather than floating
    in front of it or sinking inside it."""
    y, hw, z0, z1, rake = RINGS[-1]
    return y + rake * (RAKE_PIVOT - z) - 0.02 if z0 <= z <= z1 else y


# ------------------------------------------------------- component functions
#
# Everything below is written per component so the deferred Milan Peter Witt
# car (historic-streetcar.md s.2.17) can reuse the running gear, the trolley
# pole and the glazing vocabulary wholesale; only `shell()` is PCC-specific.


def running_gear():
    """Underframe shadow, two trucks, eight wheels at standard gauge.

    The truck frames are held INBOARD of the wheels (x +/-0.60 against the
    wheels' +/-0.7175) so the wheels stay visible below the skirt; a frame wide
    enough to swallow them turns the running gear into one dark slab."""
    ink = material("Toy_ink")
    dark = material("Toy_roofd")

    # The underframe is held INBOARD of the wheels.  Authored at the body's
    # own half-width it read as a full-length dark slab that hid all eight
    # wheels behind it in every elevation - the running gear disappeared.
    bevel(box("underframe", -0.60, 0.60, -7.02, 7.02, 0.20, 0.42, ink), 0.012)

    for s, tag in ((1, "f"), (-1, "r")):
        cy = s * TRUCK_Y
        bevel(box(f"truck_{tag}", -0.58, 0.58, cy - 1.35, cy + 1.35, 0.16, 0.52, ink), 0.012)
        for a, atag in ((1, "a"), (-1, "b")):
            ay = cy + a * AXLE_DY
            for sx, xtag in ((1, "l"), (-1, "r")):
                x = sx * GAUGE / 2
                # phase -90 deg puts a vertex on the ground, so min z is a
                # contact patch and not a chord an inch in the air.
                disc_x(f"wheel_{tag}{atag}{xtag}", ay, WHEEL_R,
                       x - 0.05, x + 0.05, WHEEL_R, dark, seg=10,
                       phase=math.radians(-90))


def anticlimbers():
    """The metal bumpers, front and rear.  They - not the shell - set the
    published 14.76 m length."""
    steel = material("Toy_steel")
    for s, tag in ((1, "f"), (-1, "r")):
        y_out = s * Y_F
        y_in = s * (Y_F - 0.20)
        bevel(box(f"anticlimber_{tag}", -0.82, 0.82, y_in, y_out, 0.54, 0.80, steel), 0.014)


def glazing():
    """Side windows and doors.

    Rhythm, not the real irregular pattern (s.2.7).  The post-war PCC pattern
    is front door / seven windows / side door / four windows (REFERENCE.md
    s.2.1); this is its cadence at ten panes a side, which is what survives at
    the app's camera.  The DOOR side is +X: front is +Y, up is +Z, so
    forward x up = +X is the car's right, the kerb side in the United States.
    """
    glass = material("Toy_glass")
    ink = material("Toy_ink")

    # Panes sit inside the notch: 0.017 proud of the recess floor, so still
    # 0.038 shy of the flank.  A pane flush with the flank loses the reveal
    # that makes the window band read as a band.
    gx0, gx1 = HW - NOTCH, HW - NOTCH + 0.017
    # The pane head stops CLEAR of the lit interior strip above it (2.28 m).
    # Authored overlapping, the two solids interpenetrate: harmless to look at,
    # but the shrink pass's buried-face step read the strip as an occluder and
    # opened every pane.  Separating them is the modelling fix; refusing to
    # treat a _Glow shell as an occluder at all is the guard, in
    # optimize_f_line.py.
    z0, z1 = Z_SILL + 0.06, 2.26

    def pane(name, sx, y0, y1):
        box(name, sx * gx0, sx * gx1, y0, y1, z0, z1, glass)

    # Left flank (-X): the blind side of a single-ended car is one even run.
    left = [(-5.95 + i * 1.15, -5.95 + i * 1.15 + 0.95) for i in range(10)]
    for i, (a, b) in enumerate(left):
        pane(f"win_l{i}", -1, a, b)

    # Right flank (+X): front door, six windows, centre door, four windows.
    right = [(4.30 - i * 0.98, 4.30 - i * 0.98 - 0.78) for i in range(6)]
    right += [(-3.10 - i * 0.78, -3.10 - i * 0.78 - 0.60) for i in range(4)]
    for i, (a, b) in enumerate(right):
        pane(f"win_r{i}", 1, min(a, b), max(a, b))

    # Doors stand 0.012 proud of the flank and therefore FILL the glazing
    # recess where they cross it, which is exactly how a real plug door reads.
    for tag, (a, b) in (("front", (4.55, 5.75)), ("centre", (-2.90, -1.70))):
        bevel(box(f"door_{tag}", HW - NOTCH, HW + 0.012, a, b, 0.50, Z_HEAD, ink), 0.010)
        box(f"door_{tag}_glass", HW + 0.002, HW + 0.014, a + 0.12, b - 0.12,
            1.24, Z_HEAD - 0.08, glass)


def windscreen_post():
    """The centre pillar between the two windscreen panes.  The shell paints
    the whole notch band across the nose as glass, which without a post reads
    as one continuous letterbox; a PCC's windscreen is two panes."""
    ink = material("Toy_ink")
    z0, z1 = Z_SILL + 0.02, Z_HEAD - 0.02
    y = nose_surface_y((z0 + z1) / 2)
    box("windscreen_post", -0.055, 0.055, y - 0.09, y + 0.035, z0, z1, ink)


def headlight():
    """The single central lamp, low in the fascia - recognition cue 4 and the
    one thing that most says PCC from head on."""
    steel = material("Toy_steel")
    glow = material("Toy_white_Glow")
    z = 1.06
    y = nose_surface_y(z)
    disc_y("headlight_bezel", 0.0, z, y - 0.06, y + 0.09, 0.18, steel, seg=10)
    # The lens is a proud shell with its back buried in the bezel (glow_plate's
    # rule, applied to a disc).
    disc_y("headlight_lens", 0.0, z, y + 0.07, y + 0.12, 0.125, glow, seg=10)


def taillights():
    """Rear identification.  Small, but at night they are the only thing that
    tells you which end of a heritage car you are behind."""
    ink = material("Toy_ink")
    glow = material("Toy_red_Glow")
    y_face = RINGS[0][0] + 0.02
    for sx, tag in ((1, "l"), (-1, "r")):
        x = sx * 0.52
        box(f"taillight_bezel_{tag}", x - 0.13, x + 0.13, y_face - 0.10, y_face + 0.04,
            1.02, 1.28, ink)
        glow_plate(f"taillight_lens_{tag}", x - 0.09, x + 0.09,
                   y_face - 0.10, y_face + 0.04, 1.06, 1.24, glow,
                   out_axis="y", out_sign=-1, proud=0.035, bury=0.02)


def destination_sign():
    """Route board above the windscreen: opaque backing, a mustard glow shell
    3.5 cm proud, and an extruded route letter standing on the glow.  The F is
    the cheapest possible "this is the heritage line" cue - 36 triangles."""
    ink = material("Toy_ink")
    glow = material("Toy_mustard_Glow")
    z0, z1 = 2.44, 2.72
    y = nose_surface_y((z0 + z1) / 2)
    bevel(box("sign_back", -0.66, 0.66, y - 0.10, y + 0.03, z0, z1, ink), 0.010)
    face = y + 0.03
    glow_plate("sign_face", -0.60, 0.60, face - 0.05, face, z0 + 0.03, z1 - 0.03,
               glow, out_axis="y", out_sign=1, proud=0.035, bury=0.02)
    # An extruded "F" in three boxes, standing on the lit board.
    f0, f1 = face + 0.035, face + 0.06
    box("sign_letter_stem", -0.05, 0.02, f0, f1, z0 + 0.05, z1 - 0.05, ink)
    box("sign_letter_top", -0.05, 0.14, f0, f1, z1 - 0.10, z1 - 0.05, ink)
    box("sign_letter_mid", -0.05, 0.10, f0, f1, 2.565, 2.605, ink)


def roof_vents():
    """A line of ventilator boxes along the crown, plus the drip rails.

    The app's camera is 42 degrees down (s.2.10): the roof is the single
    largest surface on a 14.76 m object and style bible s.10 forbids leaving it
    blank.  The dark vents against the silver crown give it rhythm, and the
    drip rails draw the line where roof stops and livery starts - without them
    the silver crown and the cream letterboard ran into one another and the car
    lost 0.3 m of apparent height from above."""
    dark = material("Toy_roofd")
    for i in range(7):
        y = -3.9 + i * 1.3
        # The pole plinth stands on the crown at y = -2.40; a vent authored
        # under it came out of the top elevation as a doubled box growing out
        # of the pole base.
        if abs(y - POLE_BASE_Y) < 0.55:
            continue
        bevel(box(f"roof_vent_{i}", -0.26, 0.26, y - 0.17, y + 0.17,
                  Z_ROOF - 0.04, Z_ROOF + 0.055, dark), 0.010)
    for sx, tag in ((1, "r"), (-1, "l")):
        box(f"drip_rail_{tag}", sx * (HW - 0.015), sx * (HW + 0.012),
            -6.30, 6.20, Z_EAVE - 0.035, Z_EAVE + 0.02, dark)


def trolley_pole():
    """Base, tapered pole and shoe.

    DEVIATION FROM THE PLAN, recorded in REPORT.md.  s.2.8 specifies 5.5 m at
    30 degrees; that puts the tip 6.0 m above the rail and 0.8 m BEYOND the
    tail, and at the app's 1.6x render scale it becomes a 9.6 m mast reaching
    for an overhead wire the scene does not contain (transit README, the
    no-rails-no-wires decision).  Authored instead at 4.5 m and 20 degrees from
    a base one third back from the cab: the pole trails visibly ALONG the roof,
    stays inside the car's own length, and reads as period hardware rather than
    as a connection the viewer tries to trace.

    The shank is thickened well past scale (75 mm base radius against a real
    car's ~30 mm) because a scale-accurate pole is sub-pixel at the app camera.
    """
    ink = material("Toy_ink")
    steel = material("Toy_steel")

    base_y, base_z = POLE_BASE_Y, Z_ROOF + 0.02
    bevel(box("pole_plinth", -0.26, 0.26, base_y - 0.30, base_y + 0.30,
              base_z, base_z + 0.13, ink), 0.010)

    ang = math.radians(20.0)
    length = 4.50
    p0 = Vector((0.0, base_y - 0.10, base_z + 0.15))
    p1 = p0 + Vector((0.0, -length * math.cos(ang), length * math.sin(ang)))

    # A tapered hexagonal shank, built as an explicit closed solid so its
    # signed volume is meaningful; a Blender cone primitive would arrive with a
    # transform the export has to apply.
    axis = (p1 - p0).normalized()
    side = Vector((1.0, 0.0, 0.0))
    up = axis.cross(side).normalized()
    seg = 6
    verts, faces = [], []
    for ring_i, (p, r) in enumerate(((p0, 0.075), (p1, 0.045))):
        for i in range(seg):
            a = 2 * math.pi * i / seg
            verts.append(tuple(p + side * (r * math.cos(a)) + up * (r * math.sin(a))))
        _ = ring_i
    for i in range(seg):
        j = (i + 1) % seg
        faces.append((i, j, j + seg, i + seg))
    faces.append(tuple(range(seg - 1, -1, -1)))
    faces.append(tuple(range(seg, 2 * seg)))
    new_mesh("pole_shank", verts, faces, [steel])

    shoe = p1 + axis * 0.06
    box("pole_shoe", -0.11, 0.11, shoe.y - 0.09, shoe.y + 0.09,
        shoe.z - 0.05, shoe.z + 0.05, ink)


def interior_glow():
    """The warm lit ceiling strip behind the window band.

    Kept warmer than the modern fleet's (the plan's brief): these are
    incandescent-era cars and the warmth is half of why a lit PCC at dusk on
    the Embarcadero looks like 1948.  Authored as a 3.5 cm proud shell inside
    the glazing recess, so by day - when the loader draws it at alpha 0.12 -
    it is hidden in shadow rather than floating on the flank."""
    glow = material("Toy_mustard_Glow")
    z0, z1 = 2.28, Z_HEAD - 0.02
    # The blind flank is one unbroken run; the door flank is broken AT THE
    # DOORS.  Authored as two continuous lines the strip read at night as a
    # neon tube down each side rather than as light spilling out of a lit
    # saloon - the breaks are what turn it back into windows.
    runs = {
        -1: [(-6.00, 5.80)],
        1: [(4.30, 5.80), (-1.60, 4.40), (-6.00, -3.00)],
    }
    for sx, tag in ((1, "r"), (-1, "l")):
        for i, (a, b) in enumerate(runs[sx]):
            glow_plate(f"interior_strip_{tag}{i}", sx * (HW - NOTCH), sx * (HW - NOTCH),
                       a, b, z0, z1, glow,
                       out_axis="x", out_sign=sx, proud=0.035, bury=0.015)


# ----------------------------------------------------------------- assembly


def build():
    # Blender's startup file ships a Cube, a Camera and a Light; the Cube would
    # export as leaked geometry.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    shell()
    running_gear()
    anticlimbers()
    glazing()
    windscreen_post()
    headlight()
    taillights()
    destination_sign()
    roof_vents()
    trolley_pole()
    interior_glow()
    return scene


def recenter_and_report():
    """Centre in the X/Y footprint (X/Z once exported) and drop the wheel
    contact patch onto z = 0."""
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
    print("[build] front = Blender +Y  ->  glTF -Z (the cab end)")
    return tris, dims


def export(out):
    blend = os.path.join(out, "f-line.blend")
    # The AUTHORED export.  make.sh runs the shrink and the meshopt intake over
    # it and writes the shipped f-line-pcc.glb; the authored file is what
    # validate_f_line.py gates per object, because the shrink's
    # join-by-material step dissolves the per-object structure on purpose.
    glb = os.path.join(out, "f-line-pcc.authored.glb")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    # Leak-proof: a temp scene holding only the export objects, exported with
    # use_active_scene so no other scene's selection can ride along.
    export_scene = bpy.data.scenes.new("EXPORT_TMP")
    src = bpy.context.window.scene
    for o in list(src.objects):
        export_scene.collection.objects.link(o)
    bpy.context.window.scene = export_scene
    with contextlib.redirect_stdout(io.StringIO()):
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
