"""Deterministic Blender build of the SF-SIM miniature South Park.

    blender -b --python build_64_south_park.py -- [--out DIR]

Writes 64-south-park.blend and 64-south-park.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = the park's oriented-bounding-box centre (anchor
lon -122.3939704, lat 37.7815903), min Z = 0, tallest elm crest exactly 15.00 m.

Design (see REFERENCE.md for the sources behind every number):

* South Park, laid out 1852, the oldest public park in San Francisco, as
  completely re-cut by Fletcher Studio in 2017: a 159.5 x 23.5 m oval inside the
  block bounded by Second, Third, Brannan and Bryant;
* the recognition rests on OUTLINE, GROUND PATTERN and CANOPY, not on massing —
  a green lozenge at 45 degrees to a district of grey rectangles, with one
  bone-white ribbon drawn corner to corner through it;
* every polygon, path vertex, wall alignment, tree position, lamp and bench in
  this file is MEASURED from OSM (data/park_uv.json, produced by
  extract_park_uv.py) and reprojected into the park frame. The exceptions are
  named: the 14 derived trees (tagged "derived" in the data), the central plaza
  bulge (taken from the measured table cluster, see PLAZA_CENTRES), the lawn
  mounding and the play mound (estimated from photography), and the Shout's
  wave count. Nothing else is invented;
* everything is a closed solid with real thickness stacked in Z (plate 0.34,
  path 0.50, glow 0.52, kerb 0.46, bed 0.62, wall 0.79, mound 1.34) so that
  nothing is coplanar with anything else and nothing z-fights the baked
  landcover, which sits at +0.06 m above terrain;
* night state: the path is the hero glow — one continuous lit curve threading a
  dark canopy, which is what the 2017 lighting scheme does. The four lamp heads
  are the only supporting accents; lawns, beds and crowns go dark. Glow surfaces
  are thin shells proud of the opaque slab beneath them; the app renders _Glow
  at ~12% alpha by day, so a primary surface must never be authored as glow.

Authoring frame: geometry is laid out in the park's local (u, v) frame — u along
the long axis, POSITIVE TOWARD THE NORTH-EAST (Second Street), bearing 45.467
deg true; v across, POSITIVE TOWARD THE SOUTH-EAST (Brannan Street), bearing
135.467 deg — and mapped to world x/y by to_world(). The park sits 45.47 deg off
the world axes, so the axis-aligned XY bounding box is ~117.1 x 115.7 m even
though the park is 159.5 x 23.5 m. That is expected, not a scale error.

The (u, v) frame is LEFT-handed in world, exactly as civic-center-plaza's is, so
every ring goes through orient_for_world() before extrusion. See the comment
there — a build that skips it exports inside-out caps that pass every dimension
check and fail the normals test.
"""

import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

HEADING_LONG = 45.4669    # +u, toward Second Street (north-east)
HEADING_CROSS = 135.4669  # +v, toward Brannan Street (south-east)

_UL = math.radians(HEADING_LONG)
_UC = math.radians(HEADING_CROSS)
U_DIR = (math.sin(_UL), math.cos(_UL))
V_DIR = (math.sin(_UC), math.cos(_UC))

# Z stack. Every level is a distinct closed solid; the gaps are deliberate and
# are what keeps the model free of coplanar surfaces.
Z_PLATE = 0.34       # ground plate top — the park's earth body
Z_BASE = 0.26        # where everything standing ON the plate starts. NOT
                     # Z_PLATE: a superstructure whose bottom cap sits exactly
                     # on the plate's top face is coplanar with it, and the
                     # first build z-fought across the whole asset — the NE
                     # entry plaza rendered a solid black quadrilateral where
                     # a stub's bottom cap and the plate agreed to the last
                     # float. Burying the caps 80 mm inside the plate is the
                     # fix, and it is why this docstring insists nothing is
                     # coplanar with anything else.
Z_FIELD = 0.47       # the continuous concrete field the tablets are set into
Z_KERB = 0.50        # the historic rounded kerb, proud of the plate
Z_PATH = 0.50        # tablet tops — only 30 mm proud, so the joints read as a
                     # line and not as a shadow (see TABLET_JOINT)
Z_GLOW = 0.52        # the lit ribbon, a thin shell on the tablets
Z_BED = 0.66         # bio-retention beds, the tallest ground layer
Z_WALL = Z_PLATE + 0.45   # cast-in-place seat walls, 450 mm seat height
Z_MOUND = Z_PLATE + 1.00  # the play mound that hides the Shout's six posts

KERB_WIDTH = 0.70    # plan 2.15 risk 7 — profile is undocumented, and
                     # 0.45 m did not draw the oval from above
WALL_THICK = 0.35

# The path. Tablets are laid ACROSS the band in a procession, 2.6 m on centre
# with a 0.4 m joint — the real pavers are ~1.2 m and would be 2 px at the app's
# camera distance (style bible s.9). Width follows the design's thickening into
# plazas: base 3.2 m, rising to 7.6 m at each plaza centre with a Gaussian of
# sigma 7.5 m, which reproduces the measured 18.6 m length of the south-west
# picnic site.
# The tablets are set INTO a continuous field a half-tone darker than they are,
# and each one is cut from the band itself between two arc-length stations, so
# the joint is CONSTANT around every bend.
#
# Two earlier attempts are worth recording. Laid straight on the earth plate,
# the joints read from above as a black zebra. Cut as straight stadium chords
# perpendicular to a curving centreline, the joints fanned open on the outside
# of every bend — at the plaza widths a 0.18 m joint opened to 0.84 m — and the
# zebra came back as wedges. Neither is a colour problem; both are geometry.
TABLET_PITCH = 2.6
TABLET_JOINT = 0.30
TABLET_INSET = 0.18   # the field frames each tablet on its long edges too
PATH_W_BASE = 3.2
PATH_W_PLAZA = 7.6
PLAZA_SIGMA = 7.5
# Two plaza centres are measured (tourism=picnic_site ways 549848254, 549848256
# at u -64.9 and +68.6). The third, central plaza is NOT tagged in OSM; it is
# taken from the measured cluster of six amenity=table nodes spanning u -2.8 to
# +7.6, whose midpoint is +2.4. Derived, and stated.
PLAZA_CENTRES = (-64.9, 2.4, 68.6)

# Lawn mounding: "gently sloping meadows" and "a grassy hillock toward the
# centre" are documented in words and visible in photography, but no source
# gives grades. Estimated (plan 2.15 risk 4). Keyed by lawn OSM id so the two
# big lawns crown higher than the two small ones.
LAWN_CROWN = {549848274: 1.10, 549848275: 0.75, 549848276: 1.30, 549848277: 1.00}
LAWN_CROWN_DEFAULT = 0.90

# The Shout (Berliner Seilfabrik, custom). Manufacturer's envelope: a perfect
# circle in plan, two curved steel tubes running side by side, undulating from
# 0.6 m to 3.0 m, six posts all below grade. The WAVE COUNT is read from the
# installation photography, not from a spec (plan 2.15 risk 5).
SHOUT_LO = 0.60
SHOUT_HI = 3.00
SHOUT_WAVES = 3
SHOUT_GAUGE = 0.55   # centre-to-centre of the two tubes
SHOUT_TUBE_R = 0.225  # 0.45 m diameter, ~3x life size so the circle reads at all
SHOUT_SEGS = 48
SHOUT_NETS = 4

TREE_JITTER = 0.06   # +/- 6% crown scale, hashed off the tree index, never random

TRI_CAP = 12000

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",       # ground plate, kerb base, seat walls
    "Toy_cream": "f2ede3",       # path tablets, wall caps, kerb top
    "Toy_mint": "8fd0a8",        # the five lawns, including the play meadow
    "Toy_teal": "3fa8a0",        # the two picnic plaza aprons, and nothing
                                 # else. Tried as the bed colour (790 m2 of
                                 # saturated blue-green banding both long edges
                                 # read as a moat) and then as the crown colour
                                 # (turquoise pom-poms — style bible s.27's
                                 # "childishly toy-like"). It is a small
                                 # accent colour on this asset or it is nothing
    "Toy_verdigris": "9fb8a8",   # tree crowns AND the thirteen bio-retention
                                 # beds — greyer than the lawns on purpose, so
                                 # both separate from the grass from above.
                                 # Same crown colour as civic-center-plaza's
                                 # bosques: one toy box
    "Toy_steel": "9aa0a6",       # tree trunks (plane and elm bark is pale
                                 # mottled grey), lamp poles, furniture frames
    "Toy_sand": "ece4d4",        # play mound and surfacing
    "Toy_roofd": "45454a",       # the Shout's tubes — the manufacturer's
                                 # "modern, almost industrial colour choice"
    "Toy_ink": "3a3530",         # the climbing nets
    "Toy_rust": "a86444",        # bench slats and table tops — the design's
                                 # thermally modified wood
    "Toy_coral": "e8735a",       # the nest swing; the only warm accent, and all
                                 # of it inside the play circle
    "Toy_gold": "caa64a",        # lamp heads
    "Toy_cream_Glow": "f2ede3",  # the lit path — the hero night state
    "Toy_gold_Glow": "caa64a",   # the four lamp heads at night
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


def hash01(n):
    """Deterministic [0,1) hash — the same mixer the pipeline uses for its own
    scatter (pipeline/lib/geo.mjs), so 'random' variation here is reproducible
    across rebuilds and reviewable in a diff."""
    h = (n ^ 0x9E3779B9) * 0x85EBCA6B & 0xFFFFFFFF
    h = (h ^ (h >> 13)) * 0xC2B2AE35 & 0xFFFFFFFF
    h ^= h >> 16
    return (h & 0xFFFFFFFF) / 4294967296.0


# ----------------------------------------------------------------- transforms


def to_world(u, v):
    return (u * U_DIR[0] + v * V_DIR[0], u * U_DIR[1] + v * V_DIR[1])


def orient_for_world(poly):
    """Order a park-frame ring so that it comes out COUNTER-clockwise in world
    space, which is what makes prism_verts_faces' caps face outward.

    The (u, v) frame is left-handed in world (+u bears 45.47, +v bears 135.47,
    so their cross product points DOWN), so a ring that is CCW in (u, v) is CW
    in world and the test is inverted: keep the ring whose (u, v) shoelace is
    NEGATIVE. OSM rings arrive in either winding, so every polygon goes through
    here. civic-center-plaza shipped inside-out caps once for exactly this."""
    a = 0.0
    for i in range(len(poly)):
        u0, v0 = poly[i]
        u1, v1 = poly[(i + 1) % len(poly)]
        a += u0 * v1 - u1 * v0
    return poly if a < 0 else poly[::-1]


def dedupe_ring(poly):
    """Drop the repeated closing vertex and any coincident neighbours — OSM ways
    close on themselves and mesh.validate() would silently eat the degenerate
    faces, taking the volume test's meaning with them."""
    out = []
    for p in poly:
        if not out or (abs(p[0] - out[-1][0]) > 1e-6 or abs(p[1] - out[-1][1]) > 1e-6):
            out.append((p[0], p[1]))
    if len(out) > 1 and abs(out[0][0] - out[-1][0]) < 1e-6 and abs(out[0][1] - out[-1][1]) < 1e-6:
        out.pop()
    return out


def centroid(poly):
    a = cu = cv = 0.0
    n = len(poly)
    for i in range(n):
        u0, v0 = poly[i]
        u1, v1 = poly[(i + 1) % n]
        cr = u0 * v1 - u1 * v0
        a += cr
        cu += (u0 + u1) * cr
        cv += (v0 + v1) * cr
    if abs(a) < 1e-9:
        return (sum(p[0] for p in poly) / n, sum(p[1] for p in poly) / n)
    return (cu / (3 * a), cv / (3 * a))


def shrink(poly, factor):
    cu, cv = centroid(poly)
    return [(cu + (u - cu) * factor, cv + (v - cv) * factor) for u, v in poly]


def inset_ring(poly, d):
    """Move every vertex inward along its angle bisector by d. The park ring is
    a convex oval, which is the case this handles correctly; it is used for the
    kerb band only."""
    n = len(poly)
    out = []
    for i in range(n):
        pu, pv = poly[i - 1]
        cu, cv = poly[i]
        nu, nv = poly[(i + 1) % n]
        a = (cu - pu, cv - pv)
        b = (nu - cu, nv - cv)
        la = math.hypot(*a) or 1.0
        lb = math.hypot(*b) or 1.0
        # inward normal of each edge, for a ring wound CCW in (u, v)
        na = (a[1] / la, -a[0] / la)
        nb = (b[1] / lb, -b[0] / lb)
        mu, mv = na[0] + nb[0], na[1] + nb[1]
        lm = math.hypot(mu, mv)
        if lm < 1e-6:
            mu, mv, lm = na[0], na[1], 1.0
        scale = d / max(0.35, (1 + na[0] * nb[0] + na[1] * nb[1]) / 2) ** 0.5
        out.append((cu + mu / lm * scale, cv + mv / lm * scale))
    return out


def point_in_ring(poly, p):
    """Even-odd test in the (u, v) frame."""
    inside = False
    n = len(poly)
    for i in range(n):
        u0, v0 = poly[i]
        u1, v1 = poly[(i + 1) % n]
        if (v0 > p[1]) != (v1 > p[1]):
            x = u0 + (p[1] - v0) * (u1 - u0) / (v1 - v0)
            if p[0] < x:
                inside = not inside
    return inside


def ring_ccw_uv(poly):
    a = 0.0
    for i in range(len(poly)):
        u0, v0 = poly[i]
        u1, v1 = poly[(i + 1) % len(poly)]
        a += u0 * v1 - u1 * v0
    return poly if a > 0 else poly[::-1]


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
    a third of the object's thinnest dimension: most of this asset is 120-340 mm
    paving and a flat 0.12 m bevel on those collapses opposing profiles into
    zero-area slivers even with clamp_overlap."""
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


def prism_verts_faces(poly_uv, z0, z1, base_index=0):
    """Closed extrusion of a park-frame polygon: walls + both caps. Orients the
    ring itself, so every caller gets outward normals."""
    poly = [to_world(u, v) for u, v in orient_for_world(poly_uv)]
    n = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    b = base_index
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((b + i, b + j, b + n + j, b + n + i))
    faces.append(tuple(b + i for i in range(n - 1, -1, -1)))
    faces.append(tuple(b + i for i in range(n, 2 * n)))
    return verts, faces


def prism_uv(name, poly_uv, z0, z1, mat, mat_top=None):
    verts, faces = prism_verts_faces(dedupe_ring(poly_uv), z0, z1)
    face_mats = [0] * (len(faces) - 1) + [1 if mat_top else 0]
    mats = [mat, mat_top] if mat_top else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def add_prism(vb, fb, poly_uv, z0, z1):
    v, f = prism_verts_faces(dedupe_ring(poly_uv), z0, z1, base_index=len(vb))
    vb.extend(v)
    fb.extend(f)


def ngon_uv(nsides, uc, vc, r, rot=0.0):
    """Emitted CLOCKWISE in (u, v), which is counter-clockwise in world — see
    orient_for_world()."""
    return [
        (uc + r * math.cos(rot - 2 * math.pi * i / nsides),
         vc + r * math.sin(rot - 2 * math.pi * i / nsides))
        for i in range(nsides)
    ]


def frustum(vb, fb, nsides, uc, vc, r0, r1, z0, z1, rot=0.0):
    b = len(vb)
    lo = ngon_uv(nsides, uc, vc, r0, rot)
    hi = ngon_uv(nsides, uc, vc, r1, rot)
    vb.extend([to_world(u, v) + (z0,) for u, v in lo])
    vb.extend([to_world(u, v) + (z1,) for u, v in hi])
    for i in range(nsides):
        j = (i + 1) % nsides
        fb.append((b + i, b + j, b + nsides + j, b + nsides + i))
    fb.append(tuple(b + i for i in range(nsides - 1, -1, -1)))
    fb.append(tuple(b + nsides + i for i in range(nsides)))


def cone_ring(vb, fb, nsides, uc, vc, radii, zs, rot=0.0):
    """A stack of ngon rings closed top and bottom — the tree crowns."""
    b = len(vb)
    for r, z in zip(radii, zs):
        vb.extend([to_world(u, v) + (z,) for u, v in ngon_uv(nsides, uc, vc, r, rot)])
    for k in range(len(radii) - 1):
        o0 = b + k * nsides
        o1 = b + (k + 1) * nsides
        for i in range(nsides):
            j = (i + 1) % nsides
            fb.append((o0 + i, o0 + j, o1 + j, o1 + i))
    fb.append(tuple(b + i for i in range(nsides - 1, -1, -1)))
    top = b + (len(radii) - 1) * nsides
    fb.append(tuple(top + i for i in range(nsides)))


def box_uv(vb, fb, u0, u1, v0, v1, z0, z1):
    add_prism(vb, fb, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], z0, z1)


def oriented_box(vb, fb, uc, vc, du, dv, length, width, z0, z1):
    """A box centred at (uc, vc) whose long axis is the unit vector (du, dv)."""
    nu, nv = -dv, du
    hl, hw = length / 2.0, width / 2.0
    poly = [
        (uc - du * hl - nu * hw, vc - dv * hl - nv * hw),
        (uc + du * hl - nu * hw, vc + dv * hl - nv * hw),
        (uc + du * hl + nu * hw, vc + dv * hl + nv * hw),
        (uc - du * hl + nu * hw, vc - dv * hl + nv * hw),
    ]
    add_prism(vb, fb, poly, z0, z1)


def stadium(uc, vc, du, dv, length, width, cap_segs=2):
    """A rounded oblong ('tablet') centred at (uc, vc), long axis (du, dv). The
    real pavers have rounded ends; this is the cheapest outline that keeps them."""
    nu, nv = -dv, du
    hl = max(length / 2.0 - width / 2.0, 0.01)
    r = width / 2.0
    pts = []
    for sign in (1, -1):
        cu, cv = uc + du * hl * sign, vc + dv * hl * sign
        for k in range(cap_segs + 1):
            a = math.pi * k / cap_segs
            # sweep from +n to -n around the cap, in the +sign direction
            ru = math.cos(a) * nu + math.sin(a) * du * sign
            rv = math.cos(a) * nv + math.sin(a) * dv * sign
            pts.append((cu + ru * r, cv + rv * r))
    return dedupe_ring(pts)


# ------------------------------------------------------------------ materials


def make_materials():
    mats = {}
    for name, rgb in PALETTE.items():
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        bsdf = m.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.85
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = 0.0
        if "Specular IOR Level" in bsdf.inputs:
            bsdf.inputs["Specular IOR Level"].default_value = 0.3
        m.diffuse_color = (*rgb, 1.0)
        m.roughness = 0.85
        mats[name] = m
    return mats


# -------------------------------------------------------------- path geometry


def polyline_length(line):
    return sum(math.dist(line[i], line[i + 1]) for i in range(len(line) - 1))


def station(line, s):
    """The point and unit tangent at arc length s along a polyline."""
    acc = 0.0
    for i in range(len(line) - 1):
        (u0, v0), (u1, v1) = line[i], line[i + 1]
        seg = math.dist((u0, v0), (u1, v1))
        if seg < 1e-9:
            continue
        if s <= acc + seg or i == len(line) - 2:
            t = min(max(s - acc, 0.0), seg)
            du, dv = (u1 - u0) / seg, (v1 - v0) / seg
            return ((u0 + du * t, v0 + dv * t), (du, dv))
        acc += seg
    return (line[-1], (1.0, 0.0))


def station_smooth(line, s, h=1.3):
    """Point at arc length s, with a tangent taken over +/- h so it follows the
    band rather than the individual OSM segment. The unsmoothed tangent is what
    made the tablet quads bow-tie on the tight bends: two neighbouring stations
    on either side of a 90-degree OSM vertex produced offsets that crossed, and
    the folded quad exported one triangle facing down — a black wedge in the
    top view that no dimension check would ever catch."""
    p, _ = station(line, s)
    a, _ = station(line, max(s - h, 0.0))
    b, _ = station(line, s + h)
    du, dv = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(du, dv) or 1.0
    return p, (du / ln, dv / ln)


def resample(line, step):
    """Walk a polyline at fixed arc length. Returns (point, unit tangent, s)."""
    out = []
    s_target = step / 2.0
    s_acc = 0.0
    for i in range(len(line) - 1):
        (u0, v0), (u1, v1) = line[i], line[i + 1]
        seg = math.dist((u0, v0), (u1, v1))
        if seg < 1e-9:
            continue
        du, dv = (u1 - u0) / seg, (v1 - v0) / seg
        while s_target <= s_acc + seg:
            t = s_target - s_acc
            out.append(((u0 + du * t, v0 + dv * t), (du, dv), s_target))
            s_target += step
        s_acc += seg
    return out


def path_width(u):
    w = PATH_W_BASE
    for c in PLAZA_CENTRES:
        w = max(w, PATH_W_BASE + (PATH_W_PLAZA - PATH_W_BASE)
                * math.exp(-((u - c) ** 2) / (2 * PLAZA_SIGMA ** 2)))
    return w


def ribbon_boxes(vb, fb, line, half_width_fn, z0, z1, overlap=0.9, phase=0):
    """A band along a polyline, built as one overlapping box per segment.

    ribbon_poly() is the obvious way to do this and it is wrong for OSM
    polylines: on a corner tighter than the band is wide, the two offset edges
    cross and the closed ring becomes a bow tie whose top cap exports facing
    DOWN. That is what put small black polygons on the promenade and on the
    Third Street entry stubs in the first three builds — invisible to every
    dimension check, invisible to the signed-volume test (the fold is
    volume-neutral), and obvious only in the top render."""
    for i, (a, b) in enumerate(zip(line, line[1:])):
        ln = math.dist(a, b)
        if ln < 1e-6:
            continue
        du, dv = (b[0] - a[0]) / ln, (b[1] - a[1]) / ln
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        w = half_width_fn(mid[0]) * 2.0
        # Stagger the top face by a few millimetres per segment. Overlapping
        # boxes that share an exactly coplanar top surface shadow each other,
        # and Cycles renders that acne as hard-edged dark polygons — which is
        # what the joints of the promenade looked like once ribbon_poly was
        # replaced by boxes. Invisible at 4 mm, and it costs nothing.
        oriented_box(vb, fb, mid[0], mid[1], du, dv, ln + w * overlap, w,
                     z0, z1 + ((i + phase) % 3) * 0.004)


def ribbon_poly(line, half_width_fn):
    """Left edge forward, right edge back — a closed band around a polyline.
    Only safe where the polyline has no corner tighter than its own width; see
    ribbon_boxes()."""
    left, right = [], []
    n = len(line)
    for i, (u, v) in enumerate(line):
        if i == 0:
            du, dv = line[1][0] - u, line[1][1] - v
        elif i == n - 1:
            du, dv = u - line[-2][0], v - line[-2][1]
        else:
            du, dv = line[i + 1][0] - line[i - 1][0], line[i + 1][1] - line[i - 1][1]
        ln = math.hypot(du, dv) or 1.0
        nu, nv = -dv / ln, du / ln
        hw = half_width_fn(u)
        left.append((u + nu * hw, v + nv * hw))
        right.append((u - nu * hw, v - nv * hw))
    return left + right[::-1]


# ------------------------------------------------------------------- the park


def build(data, mats):
    objs = []
    ring = dedupe_ring([tuple(p) for p in data["ring"]])

    # 1. ground plate — the park's earth body. Its side wall IS the historic
    #    rounded kerb face, the one piece of 1854 fabric that survives.
    objs.append(bevel(prism_uv("ground_plate", ring, 0.0, Z_PLATE,
                               mats["Toy_stone"]), 0.14, segments=1))

    # 2. kerb band — a 0.45 m ring standing 0.12 m proud, a half-tone lighter
    #    than the plate. This is what draws the oval from directly above and it
    #    is the first recognition cue (plan 2.5, 2.15 risk 7).
    outer = ring_ccw_uv(ring)
    inner = inset_ring(outer, KERB_WIDTH)
    clip_ring = inset_ring(outer, 2.0)
    vb, fb = [], []
    n = len(outer)
    for i in range(n):
        j = (i + 1) % n
        add_prism(vb, fb, [outer[i], outer[j], inner[j], inner[i]], Z_BASE, Z_KERB)
    objs.append(new_mesh("kerb", vb, fb, [mats["Toy_cream"]]))

    # 3. bio-retention beds — thirteen measured polygons, the one saturated
    #    ground colour in the asset.
    vb, fb = [], []
    for bed in data["beds"]:
        add_prism(vb, fb, [tuple(p) for p in bed["poly"]], Z_BASE, Z_BED)
    objs.append(new_mesh("beds", vb, fb, [mats["Toy_verdigris"]]))

    # 4. lawns — five sloping meadows, crowned. Estimated grades (2.15 risk 4).
    vb, fb = [], []
    for lawn in data["lawns"]:
        poly = orient_for_world(dedupe_ring([tuple(p) for p in lawn["poly"]]))
        crown = LAWN_CROWN.get(lawn["id"], LAWN_CROWN_DEFAULT)
        rings = [(poly, Z_BASE),
                 (shrink(poly, 0.62), Z_PLATE + crown * 0.62),
                 (shrink(poly, 0.22), Z_PLATE + crown)]
        b = len(vb)
        for rp, z in rings:
            vb.extend([to_world(u, v) + (z,) for u, v in rp])
        m = len(poly)
        for k in range(len(rings) - 1):
            o0, o1 = b + k * m, b + (k + 1) * m
            for i in range(m):
                j = (i + 1) % m
                fb.append((o0 + i, o0 + j, o1 + j, o1 + i))
        fb.append(tuple(b + i for i in range(m - 1, -1, -1)))
        top = b + (len(rings) - 1) * m
        fb.append(tuple(top + i for i in range(m)))
    objs.append(new_mesh("lawns", vb, fb, [mats["Toy_mint"]]))

    # 5. the promenade — a procession of tablets laid ACROSS the band, plus the
    #    nine measured entry stubs. 188 m, corner to corner, three plazas.
    main = [tuple(p) for p in next(p for p in data["paths"] if p["main"])["line"]]
    fv, ff = [], []
    ribbon_boxes(fv, ff, main, lambda u: path_width(u) * 0.5, Z_BASE, Z_FIELD)
    vb, fb = [], []
    tablets = 0
    total = polyline_length(main)
    k = 0
    while (k + 1) * TABLET_PITCH < total:
        s0 = k * TABLET_PITCH + TABLET_JOINT / 2.0
        s1 = (k + 1) * TABLET_PITCH - TABLET_JOINT / 2.0
        ends = [station_smooth(main, s0), station_smooth(main, s1)]

        def tablet(scale):
            out = []
            for side in (1, -1):
                for (pu, pv), (du, dv) in (ends if side == 1 else ends[::-1]):
                    hw = max((path_width(pu) * 0.5 - TABLET_INSET) * scale, 0.35)
                    out.append((pu - dv * hw * side, pv + du * hw * side))
            return out

        # Narrow the tablet until it is actually a quad. Clamping against an
        # estimated turning radius was tried and was not enough: the smoothed
        # tangent understates the curvature at the sharp OSM vertices, so a few
        # tablets per build still came out bow-tied and exported a downward
        # face — a black wedge in the top view that every dimension check
        # passes. Measuring the polygon's own area catches all of them, because
        # a folded quad loses area by construction.
        scale = 1.0
        for _ in range(5):
            quad = tablet(scale)
            ideal = (s1 - s0) * (math.dist(quad[0], quad[3]) + math.dist(quad[1], quad[2])) / 2.0
            area = abs(sum(quad[i][0] * quad[(i + 1) % 4][1] - quad[(i + 1) % 4][0] * quad[i][1]
                           for i in range(4))) / 2.0
            if ideal < 1e-6 or area > 0.80 * ideal:
                break
            scale *= 0.62
        add_prism(vb, fb, quad, Z_FIELD, Z_PATH)
        tablets += 1
        k += 1
    for si, stub in enumerate(data["paths"]):
        # surface=asphalt stubs are the street crossings OUTSIDE the kerb (ways
        # 1171034234, 1171034240); the first build exported them and two white
        # wedges stuck out of the oval into the road.
        if stub["main"] or stub["surface"] == "asphalt":
            continue
        line = [tuple(p) for p in stub["line"]]
        if len(line) < 2:
            continue
        # Each stub gets its own phase, so two stubs meeting at the Third
        # Street entry do not present each other a coplanar top face; and a
        # short overlap, so a 4.6 m stub does not shoot 2.7 m past the kerb.
        # Clip to the kerb. Two of these stubs run out to the Third Street
        # entry where the oval is only a few metres across, and a 3 m band laid
        # along them shot a white wedge out past the boundary into the road.
        # Segments whose midpoint falls outside the ring inset by 2 m are the
        # part that belongs to the crossing, not to the park.
        line = [q for q in line if point_in_ring(clip_ring, q)]
        if len(line) < 2:
            continue
        ribbon_boxes(fv, ff, line, lambda u: 1.2, Z_BASE, Z_FIELD,
                     overlap=0.0, phase=si + 1)
    objs.append(new_mesh("path_field", fv, ff, [mats["Toy_stone"]]))
    objs.append(new_mesh("path_tablets", vb, fb, [mats["Toy_cream"]]))

    # 6. the lit ribbon — one continuous glow shell 20 mm proud of the tablets.
    #    A shell per tablet would be 2,000 triangles and would read at night as
    #    a dashed line; the design's night state is a single curve.
    gv, gf = [], []
    ribbon_boxes(gv, gf, main, lambda u: path_width(u) * 0.5 - 0.35, Z_PATH, Z_GLOW,
                 overlap=0.25)
    objs.append(new_mesh("path_glow", gv, gf, [mats["Toy_cream_Glow"]]))

    # 7. seat walls — six cast-in-place runs, 370 m, following the path and
    #    holding the lawns. Cap a half-tone lighter so the top line reads.
    # One box per segment, overlapping at the joints. ribbon_poly was used here
    # first and self-intersected at the tighter corners, exporting white
    # triangular sails that read from above as torn geometry.
    vb, fb = [], []
    for wall in data["walls"]:
        line = dedupe_ring([tuple(p) for p in wall["line"]])
        for i, (a, b) in enumerate(zip(line, line[1:])):
            ln = math.dist(a, b)
            if ln < 1e-6:
                continue
            du, dv = (b[0] - a[0]) / ln, (b[1] - a[1]) / ln
            oriented_box(vb, fb, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, du, dv,
                         ln + WALL_THICK * 0.9, WALL_THICK, Z_BASE,
                         Z_WALL + (i % 3) * 0.004)
    objs.append(new_mesh("seat_walls", vb, fb, [mats["Toy_stone"]]))

    # 8. play mound + surfacing. The mound follows the Shout's curvature and
    #    hides its six below-grade posts — the manufacturer's stated intent, and
    #    what makes the structure appear to float.
    pg = orient_for_world(dedupe_ring([tuple(p) for p in data["playground"]["poly"]]))
    su, sv = data["shout"]["centre"]
    vb, fb = [], []
    rings = [(pg, Z_BASE),
             ([(su + (u - su) * 0.66, sv + (v - sv) * 0.66) for u, v in pg], Z_MOUND - 0.25),
             ([(su + (u - su) * 0.30, sv + (v - sv) * 0.30) for u, v in pg], Z_MOUND)]
    b = 0
    for rp, z in rings:
        vb.extend([to_world(u, v) + (z,) for u, v in rp])
    m = len(pg)
    for k in range(len(rings) - 1):
        o0, o1 = k * m, (k + 1) * m
        for i in range(m):
            j = (i + 1) % m
            fb.append((o0 + i, o0 + j, o1 + j, o1 + i))
    fb.append(tuple(range(m - 1, -1, -1)))
    top = (len(rings) - 1) * m
    fb.append(tuple(top + i for i in range(m)))
    objs.append(new_mesh("play_mound", vb, fb, [mats["Toy_mint"]]))

    # The poured surfacing under the structure. The playground way is tagged
    # landcover=grass / surface=grass, so the mound above is the park's FIFTH
    # lawn (TCLF: "a series of five separate lawns"); only the fall zone under
    # the Shout is surfaced.
    vb, fb = [], []
    frustum(vb, fb, 14, su, sv, data["shout"]["radius_m"] + 0.95,
            data["shout"]["radius_m"] + 0.80, Z_MOUND - 0.06, Z_MOUND + 0.04)
    objs.append(new_mesh("play_surfacing", vb, fb, [mats["Toy_sand"]]))

    # 9. the Shout — two tubes swept side by side around the measured circle,
    #    undulating SHOUT_LO -> SHOUT_HI over SHOUT_WAVES full waves.
    r0 = data["shout"]["radius_m"]

    def shout_z(theta):
        return (Z_MOUND + SHOUT_LO
                + (SHOUT_HI - SHOUT_LO) * 0.5 * (1 - math.cos(SHOUT_WAVES * theta)))

    vb, fb = [], []
    for lane in (-1, 1):
        r = r0 + lane * SHOUT_GAUGE / 2.0
        base = len(vb)
        for k in range(SHOUT_SEGS):
            th = 2 * math.pi * k / SHOUT_SEGS
            cu, cv = su + r * math.cos(th), sv + r * math.sin(th)
            cz = shout_z(th)
            for q in range(6):
                a = 2 * math.pi * q / 6
                ru = math.cos(a) * SHOUT_TUBE_R * math.cos(th)
                rv = math.cos(a) * SHOUT_TUBE_R * math.sin(th)
                vb.append(to_world(cu + ru, cv + rv) + (cz + math.sin(a) * SHOUT_TUBE_R,))
        for k in range(SHOUT_SEGS):
            o0 = base + k * 6
            o1 = base + ((k + 1) % SHOUT_SEGS) * 6
            for q in range(6):
                p = (q + 1) % 6
                fb.append((o0 + q, o1 + q, o1 + p, o0 + p))
    shout = new_mesh("shout_tubes", vb, fb, [mats["Toy_roofd"]])
    objs.append(shout)

    # nets slung between the tubes at the low points, and the nest swing.
    vb, fb = [], []
    for k in range(SHOUT_NETS):
        th = 2 * math.pi * (k + 0.5) / SHOUT_NETS
        cu, cv = su + r0 * math.cos(th), sv + r0 * math.sin(th)
        z = shout_z(th)
        oriented_box(vb, fb, cu, cv, -math.sin(th), math.cos(th),
                     3.2, SHOUT_GAUGE * 0.8, z - 0.9, z - 0.08)
    objs.append(new_mesh("shout_nets", vb, fb, [mats["Toy_ink"]]))

    vb, fb = [], []
    th = math.pi * 0.5
    nu, nv = su + (r0 - 1.9) * math.cos(th), sv + (r0 - 1.9) * math.sin(th)
    frustum(vb, fb, 10, nu, nv, 1.05, 1.05, Z_MOUND + 0.95, Z_MOUND + 1.10)
    objs.append(new_mesh("nest_swing", vb, fb, [mats["Toy_coral"]]))

    # 10. trees — 20 measured + 14 derived, four silhouette families. The trunk
    #     must reach INTO the crown: civic-center-plaza's first build stopped the
    #     trunk 4 m short and every tree read as a crown floating over a stump.
    fam = data["families"]
    tv, tf = [], []
    cv_, cf = [], []
    for i, t in enumerate(data["trees"]):
        u, v = t["uv"]
        f = fam[t["family"]]
        crest = t["crest_m"]
        span = crest - f["crown_lo"]
        jit = 1.0 + (hash01(i * 7919) - 0.5) * 2 * TREE_JITTER
        rot = hash01(i * 104729) * math.pi / 4
        trunk_top = min(f["trunk_top"], f["crown_lo"] + span * 0.45)
        # Tree heights are ABSOLUTE above z=0, not stacked on the plate: the
        # crest IS the asset's height datum and max_z has to be exactly 15.00.
        frustum(tv, tf, 8, u, v, 0.34, 0.26, Z_BASE, trunk_top, rot)
        # Broad and rounded, with the widest ring low. Tapering the crest ring
        # to 0.42 of the upper radius made every tree a cone: 34 conifers in a
        # park of elms, planes and pollards.
        cone_ring(cv_, cf, 10, u, v,
                  [f["crown_r_lo"] * 0.66 * jit, f["crown_r_lo"] * jit,
                   f["crown_r_hi"] * 0.98 * jit, f["crown_r_hi"] * 0.50 * jit],
                  [f["crown_lo"],
                   f["crown_lo"] + span * 0.30,
                   f["crown_lo"] + span * 0.70,
                   crest], rot)
    objs.append(new_mesh("tree_trunks", tv, tf, [mats["Toy_steel"]]))
    objs.append(new_mesh("tree_crowns", cv_, cf, [mats["Toy_verdigris"]]))

    # 11. furniture. Slightly oversized for scale legibility (style bible s.14).
    #     Benches and table tops are the design's thermally modified wood.
    wood_v, wood_f = [], []
    steel_v, steel_f = [], []
    for i, (u, v) in enumerate([tuple(p) for p in data["benches"]]):
        a = hash01(i * 2654435761) * math.pi
        du, dv = math.cos(a), math.sin(a)
        oriented_box(wood_v, wood_f, u, v, du, dv, 2.1, 0.62, Z_PLATE + 0.36, Z_PLATE + 0.47)
        oriented_box(wood_v, wood_f, u - dv * 0.26, v + du * 0.26, du, dv,
                     2.1, 0.12, Z_PLATE + 0.47, Z_PLATE + 0.92)
        oriented_box(steel_v, steel_f, u, v, du, dv, 1.7, 0.10, Z_BASE, Z_PLATE + 0.36)
    for u, v in [tuple(p) for p in data["tables"]]:
        frustum(wood_v, wood_f, 6, u, v, 0.52, 0.52, Z_PLATE + 0.68, Z_PLATE + 0.76)
        frustum(steel_v, steel_f, 4, u, v, 0.09, 0.09, Z_BASE, Z_PLATE + 0.68)
    for u, v in [tuple(p) for p in data["picnic_tables"]]:
        oriented_box(wood_v, wood_f, u, v, 1, 0, 2.3, 0.85, Z_PLATE + 0.68, Z_PLATE + 0.76)
        for s in (-1, 1):
            oriented_box(wood_v, wood_f, u, v + s * 0.78, 1, 0, 2.3, 0.32,
                         Z_PLATE + 0.42, Z_PLATE + 0.48)
        oriented_box(steel_v, steel_f, u, v, 1, 0, 0.22, 1.5, Z_BASE, Z_PLATE + 0.68)
    for u, v in [tuple(p) for p in data["bike"]]:
        for s in (-0.5, 0.5):
            oriented_box(steel_v, steel_f, u + s, v, 0, 1, 0.10, 0.90, Z_BASE, Z_PLATE + 0.80)
        oriented_box(steel_v, steel_f, u, v + 0.45, 1, 0, 1.1, 0.10,
                     Z_PLATE + 0.72, Z_PLATE + 0.80)
    for u, v in [tuple(p) for p in data["waste"]]:
        frustum(steel_v, steel_f, 5, u, v, 0.34, 0.30, Z_BASE, Z_PLATE + 0.92)
    for u, v in [tuple(p) for p in data["water"]]:
        frustum(steel_v, steel_f, 5, u, v, 0.22, 0.18, Z_BASE, Z_PLATE + 0.95)
    objs.append(new_mesh("furniture_wood", wood_v, wood_f, [mats["Toy_rust"]]))
    objs.append(new_mesh("furniture_steel", steel_v, steel_f, [mats["Toy_steel"]]))

    # 12. the four measured lamp standards, with the night accents.
    pv, pf = [], []
    hv, hf = [], []
    gv, gf = [], []
    for u, v in [tuple(p) for p in data["lamps"]]:
        frustum(pv, pf, 6, u, v, 0.15, 0.10, Z_BASE, Z_PLATE + 5.16)
        frustum(hv, hf, 8, u, v, 0.42, 0.30, Z_PLATE + 5.16, Z_PLATE + 5.56)
        frustum(gv, gf, 8, u, v, 0.46, 0.34, Z_PLATE + 5.20, Z_PLATE + 5.52)
    objs.append(new_mesh("lamp_poles", pv, pf, [mats["Toy_steel"]]))
    objs.append(new_mesh("lamp_heads", hv, hf, [mats["Toy_gold"]]))
    objs.append(new_mesh("lamp_glow", gv, gf, [mats["Toy_gold_Glow"]]))

    return objs, tablets


# ---------------------------------------------------------------------- shell


def clear_scene():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = here
    if "--out" in argv:
        out_dir = os.path.abspath(argv[argv.index("--out") + 1])
    os.makedirs(out_dir, exist_ok=True)

    data = json.load(open(os.path.join(here, "data", "park_uv.json")))
    clear_scene()
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0

    mats = make_materials()
    objs, tablets = build(data, mats)

    # Normalize Z only. The authored origin is ALREADY the park's oriented
    # bounding-box centre — that is what the manifest anchor means — so the
    # model must not be re-centred on its own axis-aligned bounding box. The
    # first build did, and because the canopy overhangs the kerb asymmetrically
    # the whole park slid 0.92 m across the city: the Shout came out at
    # v = -0.39 where the survey puts it at -1.29. Rule 5 is not negotiable for
    # 0.92 m of convenience. min z goes to exactly 0; x/y are left alone, and
    # the ground plate's own centre is what the validator checks against the
    # 0.5 m tolerance.
    dg = bpy.context.evaluated_depsgraph_get()
    mn = [1e9] * 3
    mx = [-1e9] * 3
    for o in objs:
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        for vert in me.vertices:
            w = o.matrix_world @ vert.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
        ev.to_mesh_clear()
    shift = Vector((0.0, 0.0, -mn[2]))
    for o in objs:
        o.location += shift
    bpy.context.view_layer.update()
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    tris = 0
    dg = bpy.context.evaluated_depsgraph_get()
    mn = [1e9] * 3
    mx = [-1e9] * 3
    for o in objs:
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for vert in me.vertices:
            w = o.matrix_world @ vert.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
        ev.to_mesh_clear()

    datum = data["tallest_elm_m"]
    print("objects        %d" % len(objs))
    print("tablets        %d" % tablets)
    print("triangles      %d / %d" % (tris, TRI_CAP))
    print("dims           %.4f x %.4f x %.4f" % tuple(mx[i] - mn[i] for i in range(3)))
    print("min z          %.6f" % mn[2])
    print("centre xy      %.6f %.6f" % ((mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2))
    print("datum          %.4f (target %.2f, delta %.4f)" % (mx[2], datum, mx[2] - datum))
    if tris > TRI_CAP:
        print("!! OVER TRIANGLE CAP")
    if abs(mx[2] - datum) > 0.01:
        print("!! MAX Z IS NOT THE DATUM")

    blend = os.path.join(out_dir, "64-south-park.blend")
    glb = os.path.join(out_dir, "64-south-park.glb")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    for o in bpy.data.objects:
        o.select_set(o in objs)
    bpy.ops.export_scene.gltf(
        filepath=glb, export_format="GLB", use_selection=True, export_apply=True,
        export_cameras=False, export_lights=False, export_yup=True,
    )
    print("wrote", blend)
    print("wrote", glb)


if __name__ == "__main__":
    main()
