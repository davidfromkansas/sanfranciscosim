"""Deterministic Blender build of the SF-SIM miniature Oracle Park.

    blender -b --python build_oracle_park.py -- [--out DIR]

Real-world metres. Blender +X east, +Y true north, +Z up.

Everything is authored in one field-centric frame whose origin is home plate:
local +u runs home plate -> centre field, local +v runs toward left field.
That axis is bearing 85.5 degrees clockwise from true north, measured on Esri
World Imagery from the home-plate circle to the pitcher's mound and confirmed
by the left-field foul pole (bearing 40.7 deg, 104 m / 342 ft against the
published 339 ft).  Because the bowl, the field graphic, the outer shell, the
gates and the scoreboard are all evaluated in that single frame, they cannot
drift out of alignment with each other.

The outer wall follows the real OSM footprint (relation 7325085 / way 4786909)
resampled into the field frame, so the plan silhouette is the surveyed one and
every deck is lofted between the field boundary and that footprint.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

FIELD_BEARING = math.radians(85.5)
TOTAL_H = 45.0
RIGHT_FIELD_WALL_H = 7.32

# Outfield fence radius from home plate, (degrees from the centre-field axis,
# metres).  Positive angles run toward left field.  Anchored on the published
# marks: 339 ft LF pole, 364 ft LCF, 399 ft CF, 421 ft right-centre, 309 ft RF.
FENCE = [
    (-45.0, 94.2), (-40.0, 97.0), (-34.0, 103.0), (-28.0, 111.3),
    (-22.0, 121.9), (-15.0, 128.3), (-8.0, 125.6), (0.0, 121.6),
    (10.0, 119.5), (20.0, 114.3), (30.0, 110.9), (38.0, 108.2), (45.0, 103.3),
]

# OSM footprint (way 4786909) expressed in the field frame, metres.
FOOTPRINT = [
    (8.6, -95.0), (1.1, -88.3), (-35.4, -56.3), (-48.2, -44.6), (-58.3, -32.5),
    (-62.7, -21.8), (-63.2, -9.0), (-74.7, 5.9), (-83.5, -2.3), (-92.8, 7.6),
    (-83.8, 15.5), (-39.5, 54.3), (-13.3, 76.7), (3.5, 91.1), (51.5, 132.2),
    (54.2, 134.5), (66.8, 145.4), (75.2, 135.7), (100.2, 108.4), (92.9, 102.6),
    (87.8, 98.2), (96.7, 88.0), (149.9, 26.7), (149.8, -35.2), (26.4, -87.5),
]

PALETTE_HEX = {
    "Toy_brick": "c96f4a",
    "Toy_verdigris": "9fb8a8",
    "Toy_trim": "f3efe6",
    "Toy_mint": "8fd0a8",
    "Toy_rust": "a86444",
    "Toy_steel": "9aa0a6",
    "Toy_ink": "3a3530",
    "Toy_roofd": "45454a",
    "Toy_glass": "2a4d73",
    "Toy_white_Glow": "f7f4ec",
    "Toy_gold": "caa64a",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {name: srgb_to_linear(value) for name, value in PALETTE_HEX.items()}


def world(u, v, z):
    """Field frame -> world.  +u home plate to centre field, +v to left field."""
    east = math.sin(FIELD_BEARING) * u - math.cos(FIELD_BEARING) * v
    north = math.cos(FIELD_BEARING) * u + math.sin(FIELD_BEARING) * v
    return (east, north, z)


def wrap(deg):
    return (deg + 180.0) % 360.0 - 180.0


def fence_radius(deg):
    """Outfield fence distance from home plate at an angle off the CF axis."""
    d = max(-45.0, min(45.0, wrap(deg)))
    for (a0, r0), (a1, r1) in zip(FENCE, FENCE[1:]):
        if a0 <= d <= a1:
            t = (d - a0) / (a1 - a0)
            return r0 + (r1 - r0) * t
    return FENCE[-1][1]


def field_radius(deg):
    """Inner boundary of the stands: the playing surface edge, all round.

    Inside the foul poles this is the fence plus the warning strip.  Outside
    them the stands run parallel to the foul lines at a fixed 15 m stand-off,
    which is what produces the real wedge-shaped foul ground and the tight
    backstop behind home plate.
    """
    d = wrap(deg)
    if abs(d) <= 45.0:
        return fence_radius(d) + 2.2
    best = fence_radius(45.0 if d > 0 else -45.0) + 2.2
    for sign in (1.0, -1.0):
        c = math.cos(math.radians(d - sign * 135.0))
        if c > 0.02:
            best = min(best, 15.0 / c)
    return best


def footprint_radius(deg):
    """Distance from home plate to the surveyed outer wall along a bearing."""
    a = math.radians(deg)
    dx, dy = math.cos(a), math.sin(a)
    best = None
    n = len(FOOTPRINT)
    for i in range(n):
        x0, y0 = FOOTPRINT[i]
        x1, y1 = FOOTPRINT[(i + 1) % n]
        ex, ey = x1 - x0, y1 - y0
        den = dx * ey - dy * ex
        if abs(den) < 1e-9:
            continue
        t = (x0 * ey - ex * y0) / den          # along the ray
        s = (dy * x0 - dx * y0) / den          # along the edge
        if t > 0 and -1e-9 <= s <= 1 + 1e-9:
            best = t if best is None else min(best, t)
    return best if best else 120.0


DECK_MAX = 50.0  # how far the stands may reach behind the field boundary


_OUTER_LUT = None


def outer_radius(deg):
    """Outer face of the building: an offset of the bowl, clipped by the site.

    The surveyed polygon has service notches and a spike at the left-field
    corner that read as damage at miniature scale, so the profile is sampled
    every degree and box-filtered.  The result keeps the surveyed proportions
    and the two long straight street edges while giving the confident chunky
    silhouette the style bible asks for.
    """
    global _OUTER_LUT
    if _OUTER_LUT is None:
        raw = [min(footprint_radius(float(d)), field_radius(float(d)) + DECK_MAX)
               for d in range(360)]
        w = 7
        _OUTER_LUT = [sum(raw[(i + k) % 360] for k in range(-w, w + 1)) / (2 * w + 1)
                      for i in range(360)]
    d = wrap(deg) % 360.0
    i = int(math.floor(d))
    f = d - i
    smooth = _OUTER_LUT[i % 360] * (1 - f) + _OUTER_LUT[(i + 1) % 360] * f
    return max(smooth, field_radius(deg) + 9.0)


def radii(deg, d_in, d_out):
    """Two radii a fixed distance behind the field boundary, clipped to the site.

    Constant depths keep every deck the same width all the way round, which is
    what makes the bowl read as one continuous terraced mass rather than a set
    of unrelated slabs.
    """
    base = field_radius(deg)
    lim = outer_radius(deg)
    ri = min(base + d_in, lim - 0.6)
    ro = min(base + d_out, lim)
    return ri, max(ro, ri + 0.6)


def polar(deg, r, z):
    a = math.radians(deg)
    return world(r * math.cos(a), r * math.sin(a), z)


def material(name):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    rgb = PALETTE[name]
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    bsdf.inputs["Metallic"].default_value = 0.0
    if name.endswith("_Glow"):
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    return mat


def new_mesh(name, verts, faces, mats, bevel=0.0, recalc=True):
    me = bpy.data.meshes.new(name)
    me.from_pydata([Vector(v) for v in verts], [], faces)
    for mat in mats:
        me.materials.append(mat)
    me.validate()
    obj = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    if recalc:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if bevel:
        bmesh.ops.bevel(bm, geom=list(bm.verts) + list(bm.edges), offset=bevel,
                        segments=2, profile=0.5, affect="EDGES", clamp_overlap=True)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free(); me.shade_flat()
    return obj


def loft(name, sections, mat, bevel=0.0):
    """Sweep a closed cross-section (list of world points) along the sections."""
    n = len(sections[0])
    verts = [p for sec in sections for p in sec]
    faces = []
    for i in range(len(sections) - 1):
        a, b = i * n, (i + 1) * n
        for j in range(n):
            k = (j + 1) % n
            faces.append((a + j, a + k, b + k, b + j))
    faces.append(tuple(range(n - 1, -1, -1)))
    tail = (len(sections) - 1) * n
    faces.append(tuple(range(tail, tail + n)))
    return new_mesh(name, verts, faces, [mat], bevel=bevel)


def band(name, deg0, deg1, d_in, d_out, z_base, z_front, z_back, mat,
         step=6.0, bevel=0.0, z_base_back=None):
    """A deck lofted between two constant depths behind the field boundary.

    ``z_base_back`` raises the outer underside, which turns the solid deck into
    a thin sloping strip -- used for the aisles so they hug the seating rake
    instead of standing up out of it.
    """
    zb = z_base if z_base_back is None else z_base_back
    steps = max(2, int(round(abs(deg1 - deg0) / step)))
    sections = []
    for i in range(steps + 1):
        deg = deg0 + (deg1 - deg0) * i / steps
        ri, ro = radii(deg, d_in, d_out)
        sections.append([
            polar(deg, ri, z_base), polar(deg, ri, z_front),
            polar(deg, ro, z_back), polar(deg, ro, zb),
        ])
    return loft(name, sections, mat, bevel=bevel)


def wall(name, deg0, deg1, depth, thickness, z0, z1, mat, step=6.0, bevel=0.0,
         z0_fn=None, z1_fn=None):
    """A vertical wall a constant depth behind the field boundary.

    ``depth`` of ``None`` puts the wall on the outer face of the building.
    ``z0_fn`` / ``z1_fn`` let the wall's top or bottom follow the roofline.
    """
    steps = max(2, int(round(abs(deg1 - deg0) / step)))
    sections = []
    for i in range(steps + 1):
        deg = deg0 + (deg1 - deg0) * i / steps
        r = outer_radius(deg) if depth is None else radii(deg, depth, depth)[0]
        a = z0 if z0_fn is None else z0_fn(deg)
        b = z1 if z1_fn is None else z1_fn(deg)
        sections.append([
            polar(deg, r - thickness / 2, a), polar(deg, r - thickness / 2, b),
            polar(deg, r + thickness / 2, b), polar(deg, r + thickness / 2, a),
        ])
    return loft(name, sections, mat, bevel=bevel)


def shell_top(deg):
    """Height of the brick facade: tall around the grandstand, low outfield.

    Oracle Park only carries its full-height brick street wall around the
    King Street / Second Street sides; behind the outfield the building drops
    to a two-storey arcade, and that step is a big part of the silhouette.
    """
    d = wrap(deg) % 360.0
    if 56.0 <= d <= 304.0:
        return 24.0
    if d < 46.0 or d > 314.0:
        return 18.5
    t = (d - 46.0) / 10.0 if d < 56.0 else (314.0 - d) / 10.0
    return 18.5 + 5.5 * t


def fence_wall(name, deg0, deg1, thickness, z0, z1, mat, step=5.0, bevel=0.0):
    steps = max(2, int(round(abs(deg1 - deg0) / step)))
    sections = []
    for i in range(steps + 1):
        deg = deg0 + (deg1 - deg0) * i / steps
        r = fence_radius(deg)
        sections.append([
            polar(deg, r - thickness / 2, z0), polar(deg, r - thickness / 2, z1),
            polar(deg, r + thickness / 2, z1), polar(deg, r + thickness / 2, z0),
        ])
    return loft(name, sections, mat, bevel=bevel)


def prism_polygon(name, points, z0, z1, mat, bevel=0.0):
    """A closed solid between two copies of a polygon.

    Caps are centroid fans, which stay well-formed on large polygons where a
    single n-gon can yield degenerate corner normals.
    """
    n = len(points)
    cu = sum(u for u, _ in points) / n
    cv = sum(v for _, v in points) / n
    verts = ([world(u, v, z0) for u, v in points] +
             [world(u, v, z1) for u, v in points] +
             [world(cu, cv, z0), world(cu, cv, z1)])
    c0, c1 = 2 * n, 2 * n + 1
    faces = [((i + 1) % n, i, c0) for i in range(n)]
    faces += [(n + i, n + (i + 1) % n, c1) for i in range(n)]
    faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return new_mesh(name, verts, faces, [mat], bevel=bevel)


def local_box(name, cu, cv, z0, z1, su, sv, mat, angle=0.0, bevel=0.12):
    hu, hv = su / 2, sv / 2
    c, s = math.cos(angle), math.sin(angle)

    def p(x, y, z):
        return world(cu + x * c - y * s, cv + x * s + y * c, z)

    q = [(-hu, -hv), (hu, -hv), (hu, hv), (-hu, hv)]
    verts = [p(x, y, z0) for x, y in q] + [p(x, y, z1) for x, y in q]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, [mat], bevel=bevel)


def polar_box(name, deg, r, z0, z1, radial, tangential, mat, bevel=0.1):
    a = math.radians(deg)
    return local_box(name, r * math.cos(a), r * math.sin(a), z0, z1,
                     radial, tangential, mat, angle=a, bevel=bevel)


def arch_relief(name, deg, r, z0, width, height, mat, depth=0.5, segments=7):
    """A recessed arched opening, extruded so it is solid, not a floating plane."""
    a = math.radians(deg)
    rad = width / 2
    spring = height - rad
    prof = [(-rad, 0.0), (rad, 0.0), (rad, spring)]
    for i in range(1, segments + 1):
        t = i * math.pi / segments
        prof.append((rad * math.cos(t), spring + rad * math.sin(t)))
    tu, tv = -math.sin(a), math.cos(a)
    ru, rv = math.cos(a), math.sin(a)
    sections = []
    for off in (-depth / 2, depth / 2):
        cu = r * ru + ru * off
        cv = r * rv + rv * off
        sections.append([world(cu + tu * x, cv + tv * x, z0 + z) for x, z in prof])
    return loft(name, sections, mat)


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    brick = material("Toy_brick"); green = material("Toy_verdigris")
    trim = material("Toy_trim"); grass = material("Toy_mint")
    dirt = material("Toy_rust"); steel = material("Toy_steel")
    ink = material("Toy_ink"); roof = material("Toy_roofd")
    glass = material("Toy_glass"); glow = material("Toy_white_Glow")
    gold = material("Toy_gold")

    # ---- Playing surface -------------------------------------------------
    # The floor is the stands' own inner boundary, so the field can never sit
    # proud of the bowl or leave a gap against it.
    floor = [(field_radius(d) * math.cos(math.radians(d)),
              field_radius(d) * math.sin(math.radians(d))) for d in range(0, 360, 5)]
    # The warning track is the full floor slab; the grass is a slightly taller,
    # slightly smaller slab on top, so the dirt strip shows around the edge and
    # both meshes stay closed solids.
    prism_polygon("warning_track", floor, 0.0, 0.40, dirt)
    track = [(0.965 * u, 0.965 * v) for u, v in floor]
    prism_polygon("field_grass", track, 0.0, 0.44, grass)

    # Diamond: 27.43 m base paths, 18.44 m mound, laid out on the same axis.
    base_d = 27.43
    corners = [(0.0, 0.0)]
    for deg in (-45.0, 0.0, 45.0):
        rad = base_d if deg else base_d * math.sqrt(2)
        a = math.radians(deg)
        corners.append((rad * math.cos(a), rad * math.sin(a)))
    # Skinned infield: a 28.9 m arc struck from the mound, closed on the two
    # foul lines, which is the shape a real groundcrew cuts.
    arc_r = 28.9
    hit = 38.8  # where the foul line meets that arc, from home plate
    infield = [(-2.0, 0.0), (hit * math.cos(math.radians(-45.0)),
                             hit * math.sin(math.radians(-45.0)))]
    for i in range(13):
        t = math.radians(-71.9 + 143.8 * i / 12)
        infield.append((18.44 + arc_r * math.cos(t), arc_r * math.sin(t)))
    infield.append((hit * math.cos(math.radians(45.0)),
                    hit * math.sin(math.radians(45.0))))
    prism_polygon("infield_dirt", infield, 0.40, 0.52, dirt)
    grass_sq = []
    for deg in (-45.0, 0.0, 45.0, 180.0):
        a = math.radians(deg)
        r = {(-45.0): base_d - 4.0, 0.0: base_d * math.sqrt(2) - 5.0,
             45.0: base_d - 4.0, 180.0: 5.0}[deg]
        grass_sq.append((r * math.cos(a), r * math.sin(a)))
    prism_polygon("infield_grass", grass_sq, 0.51, 0.58, grass)
    for i, (a, b) in enumerate(zip(corners, corners[1:] + corners[:1])):
        du, dv = b[0] - a[0], b[1] - a[1]
        length = math.hypot(du, dv)
        local_box(f"baseline_{i}", (a[0] + b[0]) / 2, (a[1] + b[1]) / 2,
                  0.56, 0.70, length, 0.5, trim, math.atan2(dv, du), 0.03)
    for i, (u, v) in enumerate(corners):
        local_box(f"base_{i}", u, v, 0.70, 0.86, 1.7, 1.7, trim, math.pi / 4, 0.04)
    local_box("pitcher_mound", 18.44, 0.0, 0.52, 0.78, 6.4, 6.4, dirt, math.pi / 4, 0.10)
    local_box("pitcher_rubber", 18.44, 0.0, 0.78, 0.88, 2.2, 0.5, trim, 0.0, 0.02)

    # ---- Outfield walls --------------------------------------------------
    # Right field is the 24 ft brick cove wall; the rest is the low green fence.
    fence_wall("outfield_fence", -18.0, 45.0, 1.1, 0.0, 2.6, green, 4.0)
    fence_wall("right_field_wall", -45.0, -17.0, 1.5, 0.0, RIGHT_FIELD_WALL_H, brick, 3.5)
    fence_wall("right_field_wall_cap", -45.0, -17.0, 1.9, RIGHT_FIELD_WALL_H,
               RIGHT_FIELD_WALL_H + 0.45, green, 3.5)
    local_box("left_foul_pole", fence_radius(45.0) * math.cos(math.radians(45.0)),
              fence_radius(45.0) * math.sin(math.radians(45.0)), 2.0, 27.0,
              0.7, 0.7, gold, 0.0, 0.02)
    local_box("right_foul_pole", fence_radius(-45.0) * math.cos(math.radians(-45.0)),
              fence_radius(-45.0) * math.sin(math.radians(-45.0)),
              RIGHT_FIELD_WALL_H, 27.0, 0.7, 0.7, gold, 0.0, 0.02)

    # ---- The grandstand bowl (three decks, foul pole to foul pole) --------
    # Every deck is a constant-depth terrace measured back from the field
    # boundary, so the three tiers step up as one continuous mass and the
    # outer wall is simply the last step.  All three wrap the full seating
    # arc, which is what stops the corners opening into holes from above.
    band("lower_deck", 46.0, 314.0, 0.0, 20.0, 0.0, 3.2, 12.6, ink, 5.0)
    band("club_deck", 48.0, 312.0, 18.5, 31.0, 12.4, 16.4, 23.2, ink, 5.0)
    band("upper_deck", 50.0, 310.0, 29.5, 45.0, 23.0, 27.0, 35.4, ink, 5.0)
    # Pale concourse fascias on the front of the two upper tiers: from inside
    # and from above they are what makes the bowl read as three stacked rings
    # rather than one dark rake.
    wall("club_fascia", 48.0, 312.0, 18.5, 2.6, 8.0, 16.6, trim, 5.0)
    wall("upper_fascia", 50.0, 310.0, 29.5, 2.6, 18.6, 27.2, trim, 5.0)
    # The canopy caps the back rows and closes the plan from above.
    band("deck_canopy", 50.0, 310.0, 40.0, DECK_MAX + 6.0, 35.4, 37.6, 38.4, steel, 5.0)
    # Solid corner concourses fill the two ends of the arc.
    for tag, d0, d1 in (("left", 42.0, 50.0), ("right", 310.0, 318.0)):
        band(f"corner_block_{tag}", d0, d1, 16.0, DECK_MAX + 4.0, 0.0, 21.0, 21.0,
             green, 4.0)

    # Radial aisle strokes, lofted along the rake so they lie on the seating.
    for i, deg in enumerate(range(52, 309, 12)):
        w = math.degrees(1.5 / max(field_radius(deg), 20.0))
        band(f"aisle_lower_{i}", deg - w, deg + w, 1.5, 19.0,
             3.3, 3.6, 12.9, trim, 2 * w, z_base_back=12.4)
        band(f"aisle_upper_{i}", deg - w, deg + w, 31.0, 44.0,
             27.1, 27.4, 35.7, trim, 2 * w, z_base_back=35.2)

    # ---- Outer brick shell on the surveyed footprint ---------------------
    wall("outer_brick_shell", -18.0, 320.0, None, 4.0, 0.0, 0.0, brick, 4.0,
         z1_fn=shell_top)
    wall("outer_green_frame", 50.0, 310.0, None, 3.4, 0.0, 35.0, green, 5.0,
         z0_fn=shell_top)
    wall("outer_cornice", 50.0, 310.0, None, 5.2, 35.0, 37.0, trim, 5.0)
    wall("outfield_cornice", -18.0, 52.0, None, 5.2, 0.0, 0.0, trim, 4.0,
         z0_fn=shell_top, z1_fn=lambda d: shell_top(d) + 1.7)
    wall("cove_cornice", 308.0, 320.0, None, 5.2, 0.0, 0.0, trim, 4.0,
         z0_fn=shell_top, z1_fn=lambda d: shell_top(d) + 1.7)
    # A cream string course splits the brick into base and piano nobile.
    wall("shell_string_course", -18.0, 320.0, None, 4.8, 14.2, 15.4, trim, 4.0)
    # Facade openings sit proud of the 4 m wall face (outer face is r + 2).
    for i, deg in enumerate(range(-16, 319, 7)):
        r = outer_radius(deg)
        top = shell_top(deg)
        polar_box(f"shell_pier_{i}", deg, r, 0.0, top + 1.4, 5.4, 3.0, brick, 0.0)
        if abs(wrap(deg + 3.5 - 180.0)) > 12.0:
            arch_relief(f"shell_arch_{i}", deg + 3.5, r + 2.0, 2.4, 9.0, 11.4,
                        glass, 0.7, 7)
        if top > 22.0:
            polar_box(f"shell_window_{i}", deg + 3.5, r + 2.1, 16.6, 22.4, 0.6, 7.6,
                      glass, 0.0)
            polar_box(f"shell_upper_win_{i}", deg + 3.5, r + 1.9, 26.5, 33.0, 0.6,
                      7.6, glass, 0.0)

    # ---- Willie Mays Plaza gate, cut into the brick shell ----------------
    # The gate shares the shell radius, so the towers are the shell wall made
    # thicker and taller rather than free-standing objects in front of it.
    gate_deg = 180.0
    gate_r = outer_radius(gate_deg)
    for sgn, tag in ((1, "left"), (-1, "right")):
        polar_box(f"gate_tower_{tag}", gate_deg + sgn * 6.4, gate_r + 0.5,
                  0.0, 32.0, 10.0, 11.0, brick, 0.18)
    polar_box("gate_lintel", gate_deg, gate_r + 0.5, 18.5, 27.0, 10.0, 20.0, brick, 0.16)
    arch_relief("gate_portal", gate_deg, gate_r + 3.4, 0.0, 12.0, 17.0, ink, 5.0, 9)
    polar_box("gate_sign", gate_deg, gate_r + 5.8, 19.6, 24.6, 0.7, 15.0, ink, 0.04)
    polar_box("gate_clock", gate_deg, gate_r + 5.9, 27.4, 30.6, 0.6, 3.2, glow, 0.03)
    polar_box("gate_canopy", gate_deg, gate_r + 7.5, 12.0, 13.4, 7.0, 24.0, roof, 0.12)

    # ---- Waterfront Portwalk arcade on the cove side ---------------------
    # The one deliberately open side: a single low brick arcade, its arches
    # cut into the wall, with the public walkway as its roof.
    band("portwalk_block", -44.0, -18.0, 0.0, 17.0, 0.0, 11.6, 12.0, brick, 4.0)
    band("portwalk_walk", -44.0, -18.0, 1.0, 17.6, 11.9, 12.6, 12.6, trim, 4.0)
    wall("portwalk_parapet", -44.0, -18.0, 17.0, 1.6, 12.6, 14.4, green, 4.0)
    for i, deg in enumerate(range(-42, -18, 5)):
        arch_relief(f"portwalk_arch_{i}", deg, radii(deg, 17.0, 17.0)[0],
                    0.0, 5.0, 8.2, ink, 3.0, 7)

    # ---- Left / centre field bleachers, batter's eye and scoreboard ------
    band("bleachers", 4.0, 47.0, 0.0, 22.0, 0.0, 4.0, 14.0, ink, 4.0)
    band("bleacher_concourse", 4.0, 47.0, 20.0, DECK_MAX + 4.0, 0.0, 17.0, 17.0,
         green, 4.0)
    band("batters_eye", -18.0, 6.0, 0.0, 11.0, 0.0, 9.5, 11.0, green, 4.0)

    # The scoreboard stands on the centre-field concourse block: a solid brick
    # pedestal rising out of that roof carries the frame, so the board is
    # visibly supported from every side.
    sb_deg = 26.0
    sb_r = radii(sb_deg, 30.0, 30.0)[0]
    polar_box("scoreboard_pedestal", sb_deg, sb_r, 0.0, 20.0, 11.0, 40.0, brick, 0.2)
    polar_box("scoreboard_frame", sb_deg, sb_r, 19.0, 35.0, 5.0, 42.0, ink, 0.2)
    polar_box("scoreboard_face", sb_deg, sb_r - 2.8, 20.6, 33.4, 0.4, 38.0, glow, 0.03)
    polar_box("scoreboard_header", sb_deg, sb_r - 2.0, 35.0, 37.4, 2.2, 42.0, brick, 0.1)
    for i in range(5):
        polar_box(f"scoreboard_strut_{i}", sb_deg - 14.0 + i * 7.0, sb_r + 2.4,
                  18.0, 35.0, 1.6, 1.6, green, 0.05)

    # ---- Roof-mounted light standards ------------------------------------
    # Five standards, per the owner material, spread along the grandstand roof.
    for i, deg in enumerate((66.0, 123.0, 180.0, 237.0, 294.0)):
        r = radii(deg, 44.0, 44.0)[0]
        for j, off in enumerate((-5.0, 5.0)):
            polar_box(f"light_{i}_mast_{j}", deg + math.degrees(off / max(r, 1.0)), r,
                      36.0, 41.0, 1.2, 1.2, green, 0.0)
        polar_box(f"light_{i}_truss", deg, r, 40.2, 41.6, 2.0, 15.0, green, 0.0)
        polar_box(f"light_{i}_array", deg, r - 0.6, 41.6, TOTAL_H, 2.6, 16.0,
                  roof, 0.1)
        polar_box(f"light_{i}_lamps", deg, r - 2.0, 42.1, 44.5, 0.3, 14.5, glow, 0.02)

    # ---- Recentre to base centre, keeping the true-world heading ---------
    dg = bpy.context.evaluated_depsgraph_get()
    mn = Vector((1e9, 1e9, 1e9)); mx = Vector((-1e9, -1e9, -1e9))
    for obj in [o for o in bpy.data.objects if o.type == "MESH"]:
        me = obj.evaluated_get(dg).to_mesh()
        for vert in me.vertices:
            p = obj.matrix_world @ vert.co
            for k in range(3):
                mn[k] = min(mn[k], p[k]); mx[k] = max(mx[k], p[k])
        obj.evaluated_get(dg).to_mesh_clear()
    offset = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, mn.z))
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            for vert in obj.data.vertices:
                vert.co -= offset
    return scene


def report():
    dg = bpy.context.evaluated_depsgraph_get()
    mn = Vector((1e9, 1e9, 1e9)); mx = Vector((-1e9, -1e9, -1e9)); tris = 0
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    for obj in objs:
        me = obj.evaluated_get(dg).to_mesh(); me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for vert in me.vertices:
            p = obj.matrix_world @ vert.co
            for k in range(3):
                mn[k] = min(mn[k], p[k]); mx[k] = max(mx[k], p[k])
        obj.evaluated_get(dg).to_mesh_clear()
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)
    build(); report()
    blend = os.path.join(out, "oracle-park.blend")
    glb = os.path.join(out, "oracle-park.glb")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    bpy.ops.export_scene.gltf(filepath=glb, export_format="GLB", export_apply=True,
                              export_yup=True, use_selection=False, export_cameras=False,
                              export_lights=False, export_animations=False,
                              export_skins=False, export_morph=False,
                              export_materials="EXPORT", export_image_format="NONE")
    print(f"[build] wrote {blend}"); print(f"[build] wrote {glb}")


if __name__ == "__main__":
    main()
