"""Deterministic Blender build of the SF-SIM miniature "The Towers at Rincon"
(88 Howard Street — the residential half of Rincon Center).

    blender -b --python build_towers_at_rincon.py -- [--out DIR]

Writes towers-at-rincon.blend and towers-at-rincon.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, mast tip exactly 89.00 m.

Design (see REFERENCE.md for the sources behind every number):

* Rincon Center phase two, Scott Johnson of Pereira Associates, 1988–89. A
  six-storey curvilinear office podium fills a whole Transbay diamond block, and
  twin 22-storey apartment towers (160 flats each) rise diagonally out of it —
  one over the south-west lobe, one over the east lobe;
* the block is a diamond whose corners point roughly N, E, S, W. Howard Street
  is the SOUTH-EAST face (the address and the residential entrance), Steuart
  Street the NORTH-EAST, Spear Street the SOUTH-WEST, and the NORTH-WEST side is
  the party line with the 1940 Rincon Annex post office (a separate footprint,
  NOT in this asset);
* the footprint is a C, not a diamond: a wedge-shaped open GARDEN COURTYARD is
  cut into the north-west side, ~45 m deep, narrowing to the south-east. The
  plan dossier put this terrace on the podium ROOF; satellite imagery at z21
  shows it is at grade — a circular paved plaza with curved stepped planting
  terraces, exactly the "central garden courtyard" the LA Times described in
  October 1988. Corrected here; see REPORT.md 1;
* each tower is an elongated lozenge ~50 x 26 m whose OUTER long face is a big
  bow (radius ~30 m) stacked full of white balcony slabs, and whose courtyard
  side is a W of two projecting wings. West tower bows south, east tower bows
  east;
* the crown is the identity. Heavy rolled bullnose cornices cap the tower
  shoulders at 75.70 m; a central bay rises 2.5 storeys above with its own
  rolled cornice at 83.70 m; a shallow ARCHED (segmental barrel) penthouse caps
  that at 87.20 m — the DataSF LiDAR crest — and a slim mast reaches 89.00 m,
  the CTBUH architectural / to-tip height;
* heights are measured, not assumed. DataSF footprint 201006.0000265 is strongly
  bimodal (mean 38.29, median 24.95, mode 24.21, sigma 25.93, max 87.13). Solving
  f*H+(1-f)*L = mean and f(1-f)(H-L)^2 = sigma^2 at H = 87.0 gives L = 24.49 m
  and f = 0.221: a six-storey podium at 24.5 m and a tower crest at 87 m fall
  straight out of the raw statistics and agree with CTBUH's 89 m to tip;
* night state: the arched crown windows are the hero (warm gold), an uneven
  scatter of apartment ribbons is the supporting accent (cool), plus the
  entrance canopy. Glow surfaces are single-layer open strips standing proud of
  the opaque glazing, never closed shells — the app draws _Glow in a separate
  translucent layer and a closed box reads at twice the intended day alpha.

Authoring frame: the block sits at ~45 deg to the world axes, so the axis-aligned
XY bounding box is ~112 x 113 m even though the block's sides are 73-89 m. That
is expected, not a scale error.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# The project's tangent projection (AGENTS.md), used only to convert the final
# recentring shift back into a lon/lat anchor.
LON0P, LAT0P = -122.4375, 37.77
LON_M = 111320.0 * math.cos(math.radians(LAT0P))
LAT_M = 110540.0

# AABB centre of the DataSF footprint 201006.0000265 — the plan's design anchor,
# before recentring.
DESIGN_ANCHOR = (-122.3924873, 37.7919896)

# --------------------------------------------------------------------- levels

Z_SHOP = 5.00          # top of the tall glazed ground storey / arcade head
Z_PODIUM = 24.50       # podium roof — MEASURED (LiDAR bimodal low mode 24.49 m)
PODIUM_BANDS = 5       # five office storeys between Z_SHOP and Z_PODIUM
Z_PARAPET = 25.40      # podium parapet crest

FLOOR_H = 3.20         # residential floor
TOWER_FLOORS = 16
Z_SHOULDER = Z_PODIUM + FLOOR_H * TOWER_FLOORS      # 75.70 — shoulder cornice
Z_BAY = 83.70          # central bay cornice (2.5 more storeys)
Z_ARCH = 87.20         # arched penthouse apex — MEASURED (LiDAR hgt_max 87.13)
Z_TIP = 89.00          # mast tip — CTBUH architectural / to tip, and the bbox top

CORNICE_H = 1.55       # depth of the rolled bullnose band
CORNICE_OUT = 1.15     # how far it projects
PARAPET_OUT = 0.35

GLASS_INSET = 0.35     # podium glazing ribbons recessed this far
SPANDREL_H = 2.50      # podium: solid band height (glazing gets the rest)
T_SPANDREL = 2.10      # tower: solid band height
BALC_T = 0.32          # balcony slab thickness
BALC_OUT = 1.55        # balcony slab projection
BALC_SPAN = 0.50       # fraction of the bow the balconies run across (the
                       # real slabs stop well short of the rounded ends)

ARCADE_INSET = 1.10    # ground storey set back behind the piers
PIER = 1.15            # square arcade pier
PIER_PITCH = 9.5

EMBED = 0.04           # how far every applied band is sunk INTO the surface it
                       # sits on. Nothing here is allowed to have a face exactly
                       # coincident with another solid's face: coincident faces
                       # make a ray's first-hit direction ambiguous and the
                       # contract's normals ray test counts that as a flipped
                       # face. Overlapping solids are the supported model — the
                       # authoritative normals test is per-object signed volume.

BEVEL_W, BEVEL_SEG = 0.12, 2

# Which tower floors are lit at night, as (west, east) sets. Deliberately uneven
# and different per tower: 320 flats, not an office floor.
LIT_W = {1, 2, 5, 6, 9, 12, 13, 15}
LIT_E = {0, 3, 4, 7, 8, 11, 14}

PALETTE_HEX = {
    "Toy_sand": "ece4d4",       # the precast spandrels of podium and towers —
                                # the dominant surface. Sunlit reference
                                # photography reads this as a pale warm grey;
                                # the backlit rooftop panorama reads it much
                                # darker, which is shadow and dark glass
                                # reflecting sky, not the material.
    "Toy_stone": "d9d2c2",      # arcade piers, courtyard plaza, planter walls
    "Toy_trim": "f3efe6",       # balcony slabs, rolled cornices, arch caps,
                                # parapets, pergola bars
    "Toy_glass": "2a4d73",      # every window ribbon and the arched window
    "Toy_glassl": "6f95b8",     # entrance pyramid canopy, courtyard atrium glass
    "Toy_ink": "3a3530",        # the dark ground-storey shopfront band, and the
                                # podium roof's solar arrays — the graphic dark
                                # note the roofscape needs from the air
    "Toy_roofd": "45454a",      # mechanical masses and the shopfront reveal ONLY.
                                # NOT the roof decks: on a flat deck under the
                                # app's own lighting 45454a resolves to about
                                # rgb(9,9,12) and the roof reads as a hole in the
                                # model. The decks are Toy_steel.
    "Toy_steel": "9aa0a6",      # every roof deck, and the two masts
    "Toy_navy": "2c4a70",       # the courtyard atrium's dark frame
    "Toy_mint": "8fd0a8",       # courtyard planting — the one saturated accent
    "Toy_glassl_Glow": "6f95b8",   # lit apartment ribbons. NOT Toy_glass_Glow:
                                # the app draws _Glow unlit at
                                # 0.12 + 0.95*uNight, so at night the surface
                                # shows its RAW base colour, and 2a4d73 is the
                                # navy of UNLIT glass — a lit window painted the
                                # colour of a dark one.
    "Toy_gold_Glow": "caa64a",  # the hero: the arched crown window band and the
                                # entrance canopy. Warm, and distinct from the
                                # cool flats above it.
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# ------------------------------------------------------------------ footprint

# The DataSF footprint 201006.0000265, Douglas-Peucker simplified per face at
# 1.5 m (97 -> 29 vertices), in metres east/north of DESIGN_ANCHOR. Order is
# clockwise from the EAST corner: Howard (SE) -> south corner -> Spear (SW) ->
# west corner -> the COURTYARD wedge -> north corner -> Steuart (NE).
FOOTPRINT_RAW = [
    (56.14, 1.75),      # east corner
    (43.55, -11.02), (39.50, -7.20), (29.05, -18.55), (27.99, -20.92),
    (31.77, -25.94), (25.93, -31.62), (18.32, -28.29), (6.74, -39.36),
    (10.81, -43.52),
    (-1.80, -56.30),    # south corner
    (-47.41, -10.58), (-49.91, -13.01),
    (-56.14, -6.64),    # west corner
    (-37.22, 12.78),    # courtyard mouth, south jamb
    (-31.66, 6.79), (-20.89, 5.13), (-15.91, -1.05), (-9.25, -2.12),
    (-2.71, -8.84),     # courtyard apex (south-east end)
    (8.64, 0.98),
    (1.69, 8.46), (-0.01, 17.62), (-5.45, 20.43), (-6.35, 30.88),
    (-12.57, 37.15),    # courtyard mouth, north jamb
    (7.02, 56.30),      # north corner
    (13.43, 49.85), (10.97, 47.45),
]

# Indices into FOOTPRINT_RAW that bound the open courtyard wedge, so the
# courtyard's inner walls can be treated differently from the street elevations.
COURT_FROM, COURT_TO = 14, 25

# Which run of the outline gets the street arcade (piers + set-back shopfront):
# the three street faces, i.e. everything except the courtyard walls.
STREET_SPAN = [(25, 29), (0, 14)]   # north corner -> east -> south -> west corner


def cut_corners(poly, ratio=0.28, min_turn=18.0, max_cut=3.0):
    """Selective corner cutting. The real building is curvilinear — every corner
    of the planimetric trace is a chamfer or a bow in the concrete — but a blind
    Chaikin pass doubles the vertex count of a ring that is extruded ten times,
    so only corners that actually TURN are cut, and the cut is capped so a long
    street face is not shortened."""
    n = len(poly)
    out = []
    for i in range(n):
        p = poly[i]
        a = poly[(i - 1) % n]
        b = poly[(i + 1) % n]
        va = (a[0] - p[0], a[1] - p[1])
        vb = (b[0] - p[0], b[1] - p[1])
        la = math.hypot(*va) or 1e-9
        lb = math.hypot(*vb) or 1e-9
        cosv = max(-1.0, min(1.0, (va[0] * vb[0] + va[1] * vb[1]) / (la * lb)))
        turn = 180.0 - math.degrees(math.acos(cosv))
        if turn < min_turn:
            out.append(p)
            continue
        ka = min(ratio, max_cut / la)
        kb = min(ratio, max_cut / lb)
        out.append((p[0] + va[0] * ka, p[1] + va[1] * ka))
        out.append((p[0] + vb[0] * kb, p[1] + vb[1] * kb))
    return out


def bow(a, b, sagitta, segs):
    """Circular arc from a to b bulging `sagitta` metres to the LEFT of a->b."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    c = math.hypot(dx, dy)
    if c < 1e-6 or abs(sagitta) < 1e-6:
        return [a, b]
    r = (c * c / 4.0 + sagitta * sagitta) / (2.0 * abs(sagitta))
    mx, my = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
    ux, uy = dx / c, dy / c
    nx, ny = -uy, ux                      # left of a->b
    s = math.copysign(1.0, sagitta)
    h = math.sqrt(max(r * r - c * c / 4.0, 0.0))
    cx, cy = mx - nx * h * s, my - ny * h * s
    a0 = math.atan2(a[1] - cy, a[0] - cx)
    a1 = math.atan2(b[1] - cy, b[0] - cx)
    d = a1 - a0
    while d > math.pi:
        d -= 2 * math.pi
    while d < -math.pi:
        d += 2 * math.pi
    return [(cx + r * math.cos(a0 + d * i / segs), cy + r * math.sin(a0 + d * i / segs))
            for i in range(segs + 1)]


def _winding(poly):
    s2 = 0.0
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        s2 += a[0] * b[1] - b[0] * a[1]
    return 1.0 if s2 > 0.0 else -1.0


def inset_polygon(poly, dist):
    """Offset a simple polygon inward by `dist` (positive = shrink). Segment
    offset + line intersection, with a miter clamp so the shallow re-entrant
    corners of the courtyard cannot fire a spike across the plan."""
    n = len(poly)
    w = _winding(poly)
    lines = []
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy)
        if m < 1e-9:
            lines.append(None)
            continue
        nx, ny = (dy / m, -dx / m)
        if w > 0:
            nx, ny = -nx, -ny            # inward for a CCW ring
        lines.append(((a[0] + nx * dist, a[1] + ny * dist), (dx / m, dy / m)))
    out = []
    for i in range(n):
        p = lines[i - 1]
        q = lines[i]
        if p is None or q is None:
            out.append(poly[i])
            continue
        den = p[1][0] * q[1][1] - p[1][1] * q[1][0]
        if abs(den) < 1e-6:
            out.append(p[0])
            continue
        ex, ey = q[0][0] - p[0][0], q[0][1] - p[0][1]
        t = (ex * q[1][1] - ey * q[1][0]) / den
        cand = (p[0][0] + p[1][0] * t, p[0][1] + p[1][1] * t)
        if math.hypot(cand[0] - poly[i][0], cand[1] - poly[i][1]) > dist * 3.0 + 0.5:
            cand = ((p[0][0] + q[0][0]) / 2.0, (p[0][1] + q[0][1]) / 2.0)
        out.append(cand)
    return out


def build_outline():
    """The podium outline: the simplified DataSF ring, corner-cut so the street
    elevations read as the curvilinear concrete they are."""
    return cut_corners(FOOTPRINT_RAW)


OUTLINE = build_outline()


def _nearest(poly, p):
    return min(range(len(poly)),
               key=lambda i: (poly[i][0] - p[0]) ** 2 + (poly[i][1] - p[1]) ** 2)


def sub_run(poly, a_raw, b_raw):
    """The stretch of `poly` between the vertices nearest FOOTPRINT_RAW[a_raw]
    and FOOTPRINT_RAW[b_raw], walking forward. Corner cutting changes the vertex
    count, so runs are addressed by geometry, never by index arithmetic."""
    a = _nearest(poly, FOOTPRINT_RAW[a_raw % len(FOOTPRINT_RAW)])
    b = _nearest(poly, FOOTPRINT_RAW[b_raw % len(FOOTPRINT_RAW)])
    n = len(poly)
    out = [poly[a]]
    i = a
    while i != b:
        i = (i + 1) % n
        out.append(poly[i])
    return out


def street_run(poly):
    """North corner -> east -> south -> west corner: the three street faces."""
    return sub_run(poly, 26, 14)

# --------------------------------------------------------------------- towers

# OSM building:part ways 944891683 (west) and 944891684 (east), in the same
# anchor-relative metres. The mapper's ten vertices are the correct GROUND plan
# (satellite roof outlines are displaced ~9.5 m by a ~6 deg off-nadir lean over
# an 87 m building); the photographs are the correct SHAPE, so the outer long
# face of each is rebuilt as the true bow it is.
WEST_INNER = [(-32.37, -28.03), (-19.96, -15.72), (-13.65, -21.80),
              (-1.72, -21.47), (5.41, -15.55), (19.39, -28.75)]
WEST_BOW = ((19.39, -28.75), (-32.37, -28.03), 13.10)     # a->b, sagitta left

EAST_INNER = [(29.69, -18.53), (16.84, -6.67), (20.81, -2.63),
              (20.98, 11.11), (16.01, 17.02), (27.76, 29.67)]
EAST_BOW = ((27.76, 29.67), (29.69, -18.53), 13.20)

BOW_SEGS = 10


def tower_plan(inner, bowspec):
    """Courtyard-side wings (as mapped) + the outer face rebuilt as its true
    bow. The arc is already smooth, so no corner-cutting pass — every extra
    vertex here is paid for 32 times over in the banded shaft."""
    a, b, s = bowspec
    arc = bow(a, b, s, BOW_SEGS)
    return list(inner[1:-1]) + arc


WEST_PLAN = tower_plan(WEST_INNER, WEST_BOW)
EAST_PLAN = tower_plan(EAST_INNER, EAST_BOW)

# Long axis of each lozenge (unit vector) and its centre — used to carve the
# central bay and to place the arched cap, the mech penthouses and the mast.
def _axis(plan):
    cx = sum(p[0] for p in plan) / len(plan)
    cy = sum(p[1] for p in plan) / len(plan)
    # principal direction by second moment
    sxx = syy = sxy = 0.0
    for x, y in plan:
        dx, dy = x - cx, y - cy
        sxx += dx * dx
        syy += dy * dy
        sxy += dx * dy
    th = 0.5 * math.atan2(2 * sxy, sxx - syy)
    return (cx, cy), (math.cos(th), math.sin(th))


WEST_C, WEST_U = _axis(WEST_PLAN)
EAST_C, EAST_U = _axis(EAST_PLAN)

BAY_HALF = 10.0        # half-length of the taller central bay along the axis
ARCH_HALF = 7.0        # half-length of the arched penthouse
ARCH_W = 9.4           # its width across the axis
Z_PENT = 85.40         # top of the penthouse wall the arch springs from.
                       # Tall enough for the crown's window band to be a
                       # BAND: at 85.00 the band was 0.20 m deep and the
                       # night render showed the hero glow as a hairline.
ARCH_SEGS = 12


def clip_band(poly, c, u, half):
    """Sutherland-Hodgman clip of `poly` to the slab |(p-c).u| <= half."""
    def clip(pts, sign):
        out = []
        n = len(pts)
        for i in range(n):
            a, b = pts[i], pts[(i + 1) % n]
            da = sign * ((a[0] - c[0]) * u[0] + (a[1] - c[1]) * u[1]) - half
            db = sign * ((b[0] - c[0]) * u[0] + (b[1] - c[1]) * u[1]) - half
            if da <= 0:
                out.append(a)
            if (da > 0) != (db > 0):
                t = da / (da - db)
                out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
        return out
    return clip(clip(poly, 1.0), -1.0)


# ---------------------------------------------------------------- mesh helpers


def new_mesh(name, verts, faces, materials, face_mats=None, recalc=True):
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
    if recalc:
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()
    mesh.shade_flat()
    return obj


def prism(name, poly_xy, z0, z1, mat, mat_top=None):
    """Closed extrusion of a world-XY polygon (walls + both caps)."""
    n = len(poly_xy)
    verts = [(x, y, z0) for x, y in poly_xy] + [(x, y, z1) for x, y in poly_xy]
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


def rim(name, poly, inset, z0, z1, mat):
    """A closed BAND between `poly` and its inward offset — a parapet, not a
    solid. Extruding the inset polygon instead fills the whole roof and buries
    everything designed to sit on it."""
    inner = inset_polygon(poly, inset)
    n = len(poly)
    verts = ([(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly] +
             [(x, y, z0) for x, y in inner] + [(x, y, z1) for x, y in inner])
    O, I = 0, 2 * n
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((O + i, O + j, O + n + j, O + n + i))            # outside
        faces.append((I + j, I + i, I + n + i, I + n + j))            # inside
        faces.append((O + n + i, O + n + j, I + n + j, I + n + i))    # coping
        faces.append((O + j, O + i, I + i, I + j))                    # underside
    return new_mesh(name, verts, faces, [mat], recalc=True)


def box(name, cx, cy, sx, sy, z0, z1, mat, rot=0.0):
    c, s = math.cos(rot), math.sin(rot)
    poly = []
    for dx, dy in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)):
        poly.append((cx + dx * c - dy * s, cy + dx * s + dy * c))
    return prism(name, poly, z0, z1, mat)


def disc(name, cx, cy, r, z0, z1, segs, mat):
    poly = [(cx + r * math.cos(2 * math.pi * i / segs), cy + r * math.sin(2 * math.pi * i / segs))
            for i in range(segs)]
    return prism(name, poly, z0, z1, mat)


def _polyline_side(pts):
    """Handedness of an open polyline relative to the plan centre, so a glow
    strip's single face can be pointed outward for the whole run at once."""
    sx = sum(p[0] for p in pts) / len(pts)
    sy = sum(p[1] for p in pts) / len(pts)
    a, b = pts[0], pts[-1]
    return math.copysign(1.0, (b[0] - a[0]) * (sy - a[1]) - (b[1] - a[1]) * (sx - a[0]))


def glow_strip(name, pts, z0, z1, mat, proud, closed=False, ref=None):
    """An OPEN, single-layer strip of outward-facing quads along a polyline.

    Night glow must never be a closed shell: the app draws _Glow in a separate
    layer that is translucent by day, so a closed box shows front AND back and
    reads at roughly twice the intended day alpha — enough to tint a facade.

    `ref` is a point the strip must face AWAY from — pass the tower centre. The
    handedness a polyline can work out from its own centroid is meaningless once
    the polyline is short: a two-point run puts its centroid ON the line, the
    cross product is zero, and the sign comes out arbitrary. That is what flipped
    one run of the east tower's bow inward at stage 2; see REPORT.md 3."""
    seq = list(pts) + [pts[0]] if closed else list(pts)
    side = _polyline_side(seq)
    verts, faces = [], []
    for i in range(len(seq) - 1):
        a, b = seq[i], seq[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy)
        if m < 1e-6:
            continue
        nx, ny = dy / m, -dx / m
        if ref is not None:
            mx2, my2 = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
            flip = (mx2 + nx - ref[0]) ** 2 + (my2 + ny - ref[1]) ** 2 < \
                   (mx2 - ref[0]) ** 2 + (my2 - ref[1]) ** 2
        else:
            flip = side > 0.0
        if flip:
            a, b = b, a
            nx, ny = -nx, -ny
        a2 = (a[0] + nx * proud, a[1] + ny * proud)
        b2 = (b[0] + nx * proud, b[1] + ny * proud)
        k = len(verts)
        verts += [(a2[0], a2[1], z0), (b2[0], b2[1], z0),
                  (b2[0], b2[1], z1), (a2[0], a2[1], z1)]
        faces.append((k, k + 1, k + 2, k + 3))
    if not faces:
        return None
    return new_mesh(name, verts, faces, [mat], recalc=False)


def glow_quad(name, a, b, z0, z1, outward, mat, proud=0.10):
    """One outward-facing quad from a to b, pushed `proud` along `outward`.

    glow_strip() infers handedness from the polyline's own centroid, which is
    meaningless for a two-point run - the centroid lies ON the line and the sign
    comes out arbitrary. Where the outward direction is known from the frame that
    built the geometry, state it."""
    ox, oy = outward
    m = math.hypot(ox, oy) or 1.0
    ox, oy = ox / m, oy / m
    a2 = (a[0] + ox * proud, a[1] + oy * proud)
    b2 = (b[0] + ox * proud, b[1] + oy * proud)
    # A quad wound a2,b2,b2',a2' has normal along (dy, -dx); flip the pair if that
    # points the wrong way.
    dx, dy = b2[0] - a2[0], b2[1] - a2[1]
    if dy * ox - dx * oy < 0.0:
        a2, b2 = b2, a2
    verts = [(a2[0], a2[1], z0), (b2[0], b2[1], z0),
             (b2[0], b2[1], z1), (a2[0], a2[1], z1)]
    return new_mesh(name, verts, [(0, 1, 2, 3)], [mat], recalc=False)


def bevel(obj, width=BEVEL_W, segments=BEVEL_SEG):
    """Miniature-style edge softening (style bible s.4). The offset is capped at
    a third of the object's thinnest dimension: slabs, ribbons and parapets are
    only 0.1-0.4 m thick and a full bevel collapses opposing profiles into
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


def make_material(name):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    rgb = PALETTE[name]
    bsdf.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = 0.25
    if name.endswith("_Glow"):
        bsdf.inputs["Emission Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
        bsdf.inputs["Emission Strength"].default_value = 3.0
    mat.diffuse_color = (rgb[0], rgb[1], rgb[2], 1.0)
    mat.roughness = 0.85
    return mat


# --------------------------------------------------------------------- pieces


def podium(mats):
    outer = OUTLINE
    shop = inset_polygon(outer, ARCADE_INSET)

    # Ground storey: a dark recessed shopfront band behind a pier arcade.
    prism("podium_shop", shop, 0.0, Z_SHOP, mats["Toy_ink"])
    prism("podium_shop_head", outer, Z_SHOP - 0.55, Z_SHOP, mats["Toy_sand"])

    # Arcade piers, only along the three street faces (never in the courtyard).
    run = street_run(outer)
    acc = 0.0
    k = 0
    for i in range(len(run) - 1):
        a, b = run[i], run[i + 1]
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        t = PIER_PITCH - acc
        while t < seg:
            px = a[0] + (b[0] - a[0]) * t / seg
            py = a[1] + (b[1] - a[1]) * t / seg
            rot = math.atan2(b[1] - a[1], b[0] - a[0])
            box(f"pier_{k}", px, py, PIER, PIER, 0.0, Z_SHOP, mats["Toy_stone"], rot)
            k += 1
            t += PIER_PITCH
        acc = (acc + seg) % PIER_PITCH

    # Five banded office storeys.
    band = (Z_PODIUM - Z_SHOP) / PODIUM_BANDS
    glassp = inset_polygon(outer, GLASS_INSET)
    for i in range(PODIUM_BANDS):
        z0 = Z_SHOP + band * i
        prism(f"podium_band_{i}", outer, z0, z0 + SPANDREL_H, mats["Toy_sand"])
        prism(f"podium_glass_{i}", glassp, z0 + SPANDREL_H - EMBED, z0 + band + EMBED,
              mats["Toy_glass"])

    # Roof deck and parapet. The camera looks down: this is a facade.
    #
    # The deck sits ABOVE Z_PODIUM, not below it. The topmost glazing ribbon runs
    # to Z_PODIUM + EMBED (the embed exists so each ribbon sinks into the band
    # above it), and the top band has no band above it — so a deck ending at
    # Z_PODIUM left the ribbon's navy cap as the topmost surface and the whole
    # podium roof rendered dark blue from the app's own camera. Caught in the
    # stage-2 aerial; see REPORT.md 3d.
    prism("podium_deck", inset_polygon(outer, PARAPET_OUT), Z_PODIUM - 0.30,
          Z_PODIUM + 0.14, mats["Toy_steel"])
    rim("podium_parapet", outer, PARAPET_OUT, Z_PODIUM - 0.40, Z_PARAPET, mats["Toy_trim"])
    roofscape(mats)


# Podium roof furniture, in metres east/north of DESIGN_ANCHOR. Each is checked
# against the outline and against both tower plans before it is built, so a
# later change to the footprint cannot leave a mechanical block hanging in air.
ROOF_PROPS = [
    ("mech_w", (-34.0, -6.0), (11.0, 7.0), 2.80, "Toy_stone", 45.0),
    ("mech_n", (8.0, 41.0), (8.5, 6.5), 2.60, "Toy_stone", -45.0),
    ("mech_e", (44.0, -3.0), (5.0, 4.0), 2.40, "Toy_stone", -45.0),
    ("stair_c", (-4.0, -17.0), (5.0, 5.0), 3.20, "Toy_sand", 45.0),
    ("solar_n", (8.0, 32.0), (15.0, 8.0), 0.55, "Toy_ink", -45.0),
    ("solar_w", (-31.0, -8.0), (13.0, 6.0), 0.55, "Toy_ink", 45.0),
    ("sky_w", (-40.0, -6.0), (8.0, 3.0), 0.80, "Toy_glassl", -45.0),
    ("sky_s", (0.0, -45.0), (8.0, 2.8), 0.80, "Toy_glassl", 45.0),
    ("mech_sw", (-31.0, -19.0), (4.5, 3.6), 2.20, "Toy_stone", 45.0),
]


def _inside(poly, p):
    c = False
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if (a[1] > p[1]) != (b[1] > p[1]):
            if p[0] < (b[0] - a[0]) * (p[1] - a[1]) / (b[1] - a[1]) + a[0]:
                c = not c
    return c


def roofscape(mats):
    keep = inset_polygon(OUTLINE, 2.2)
    for name, (cx, cy), (sx, sy), h, mat, rot in ROOF_PROPS:
        c, sn = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        corners = [(cx + dx * c - dy * sn, cy + dx * sn + dy * c)
                   for dx, dy in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2),
                                  (sx / 2, sy / 2), (-sx / 2, sy / 2))]
        if not all(_inside(keep, p) for p in corners):
            print(f"[build] ! roof prop {name} overhangs the podium outline - skipped")
            continue
        if any(_inside(WEST_PLAN, p) or _inside(EAST_PLAN, p) for p in corners):
            print(f"[build] ! roof prop {name} collides with a tower - skipped")
            continue
        box(f"roof_{name}", cx, cy, sx, sy, Z_PODIUM + 0.06, Z_PODIUM + h,
            mats[mat], math.radians(rot))


def entrance(mats):
    """Howard Street entrance: a glass pyramid canopy under a monumental
    semicircular arched window recessed into the precast."""
    # Position: a third of the way along the Howard face from the east corner.
    a, b = (43.55, -11.02), (29.05, -18.55)
    ex, ey = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
    nx, ny = 0.707, -0.707                       # outward from the SE face

    # Pyramid canopy: 10 m square base, 6.4 m apex, on the sidewalk.
    hw = 5.6
    cx, cy = ex + nx * 1.1, ey + ny * 1.1
    ux, uy = -ny, nx
    base = [(cx + ux * hw + nx * hw, cy + uy * hw + ny * hw),
            (cx - ux * hw + nx * hw, cy - uy * hw + ny * hw),
            (cx - ux * hw - nx * hw, cy - uy * hw - ny * hw),
            (cx + ux * hw - nx * hw, cy + uy * hw - ny * hw)]
    verts = [(x, y, 4.10) for x, y in base] + [(cx, cy, 9.20)]
    faces = [(0, 1, 2, 3), (1, 0, 4), (2, 1, 4), (3, 2, 4), (0, 3, 4)]
    new_mesh("entrance_canopy", verts, faces, [mats["Toy_glassl"]])
    box("entrance_pier_a", cx + ux * hw, cy + uy * hw, 1.0, 1.0, 0.0, 4.10,
        mats["Toy_stone"], math.atan2(uy, ux))
    box("entrance_pier_b", cx - ux * hw, cy - uy * hw, 1.0, 1.0, 0.0, 4.10,
        mats["Toy_stone"], math.atan2(uy, ux))

    # A warm band under the canopy: at night the front door of a 320-flat tower
    # should be the one thing lit at street level.
    glow_quad("entrance_glow", (ex + ux * 4.6, ey + uy * 4.6),
              (ex - ux * 4.6, ey - uy * 4.6), 3.30, 4.60, (nx, ny),
              mats["Toy_gold_Glow"], 0.18)

    # The arched window: a half-round-headed recess 12 m wide, springing at
    # 13.5 m, crown at 21.5 m. Built as a glazed plate standing slightly proud of
    # the recess reveal, so nothing is coincident.
    w = 6.0
    z0, zs, zc = 8.0, 15.5, 21.5
    ring = []
    for i in range(9):
        th = math.pi * i / 8.0
        ring.append((-w * math.cos(th), zs + (zc - zs) * math.sin(th)))
    prof = [(-w, z0)] + ring + [(w, z0)]
    verts, faces = [], []
    for d, off in ((0.0, 0), (0.55, len(prof))):
        for t, z in prof:
            verts.append((ex + ux * t + nx * (d - EMBED), ey + uy * t + ny * (d - EMBED), z))
    m = len(prof)
    for i in range(m - 1):
        faces.append((i, i + 1, off + i + 1, off + i))
    faces.append((m - 1, 0, off, off + m - 1))
    faces.append(tuple(range(m - 1, -1, -1)))
    faces.append(tuple(range(off, off + m)))
    new_mesh("entrance_arch", verts, faces, [mats["Toy_glass"]])


def courtyard(mats):
    """The open garden court cut into the north-west side: a circular paved
    plaza, curved stepped planting terraces, a pergola bar and a glazed canopy
    over the narrow south-east end."""
    inner = sub_run(OUTLINE, COURT_FROM, COURT_TO)
    cx = sum(p[0] for p in inner) / len(inner)
    cy = sum(p[1] for p in inner) / len(inner)

    # The court FLOOR. Without it the courtyard reads from the app's overhead
    # camera as a hole punched through the block rather than as a garden.
    prism("court_floor", inner, 0.0, 0.22, mats["Toy_stone"])

    disc("court_plaza", cx - 3.0, cy + 3.0, 7.5, 0.0, 0.40, 14, mats["Toy_stone"])
    disc("court_plaza_eye", cx - 3.0, cy + 3.0, 2.8, 0.40, 0.70, 10, mats["Toy_trim"])
    disc("court_plaza_ring", cx - 3.0, cy + 3.0, 9.2, 0.0, 0.22, 14, mats["Toy_trim"])
    # Explicit planting, placed off the court centroid. The curved terrace
    # ribbons below follow the real stepped beds along the north-east wall, but
    # they are thin; these are what actually carries the one saturated accent
    # from the app's overhead camera.
    disc("court_lawn", -4.0, 2.0, 4.5, 0.0, 0.35, 12, mats["Toy_mint"])
    disc("court_bed_n", -18.0, 22.0, 4.0, 0.0, 0.90, 10, mats["Toy_mint"])
    disc("court_bed_s", 5.0, 0.0, 3.2, 0.0, 0.80, 10, mats["Toy_mint"])
    box("court_planter_w", -24.0, 14.0, 7.0, 3.2, 0.0, 1.10, mats["Toy_stone"],
        math.radians(45.0))
    box("court_planter_w_bed", -24.0, 14.0, 5.8, 2.1, 1.00, 1.75, mats["Toy_mint"],
        math.radians(45.0))

    # Two curved stepped planting terraces following the court's north-east wall.
    wall = sub_run(OUTLINE, COURT_FROM + 6, COURT_TO)[::2]
    for j, (dist, h) in enumerate(((4.0, 1.40), (8.2, 2.70))):
        seg = sub_run(inset_polygon(OUTLINE, dist), COURT_FROM + 6, COURT_TO)[::2]
        ribbon = seg + wall[::-1]
        prism(f"court_terrace_{j}", ribbon, 0.0, h, mats["Toy_stone"])
        prism(f"court_planting_{j}", inset_polygon(ribbon, 0.55), h - 0.10, h + 0.90,
              mats["Toy_mint"])

    # Pergola bar along the court's south-west wall.
    sw = sub_run(OUTLINE, COURT_FROM, COURT_FROM + 6)[::2]
    if len(sw) >= 2:
        seg = sub_run(inset_polygon(OUTLINE, 2.8), COURT_FROM, COURT_FROM + 6)[::2]
        ribbon = seg + sw[::-1]
        prism("court_pergola_deck", ribbon, 0.0, 0.45, mats["Toy_stone"])
        prism("court_pergola_top", inset_polygon(ribbon, 0.35), 3.40, 3.80, mats["Toy_trim"])

    # Glazed canopy over the narrow south-east end of the court.
    apex = sub_run(OUTLINE, COURT_FROM + 4, COURT_FROM + 7)
    ax = sum(p[0] for p in apex) / len(apex)
    ay = sum(p[1] for p in apex) / len(apex)
    box("court_atrium", ax + 3.0, ay - 2.0, 12.0, 8.0, 8.60, 9.60,
        mats["Toy_glassl"], math.radians(-45.0))
    box("court_atrium_frame", ax + 3.0, ay - 2.0, 12.9, 8.9, 8.20, 8.75,
        mats["Toy_trim"], math.radians(-45.0))


def tower(tag, plan, centre, axis, lit, mats):
    """One residential lozenge: banded shaft, balcony slabs on the bow, rolled
    shoulder cornice, taller central bay with its own cornice, arched penthouse
    and mast."""
    ang = math.atan2(axis[1], axis[0])

    # Shaft: 16 banded storeys.
    glassp = inset_polygon(plan, 0.30)
    for i in range(TOWER_FLOORS):
        z0 = Z_PODIUM + FLOOR_H * i
        prism(f"{tag}_band_{i}", plan, z0, z0 + T_SPANDREL, mats["Toy_sand"])
        gm = mats["Toy_glass"]
        prism(f"{tag}_glass_{i}", glassp, z0 + T_SPANDREL - EMBED, z0 + FLOOR_H + EMBED, gm)

    # Balcony slabs. Only on the middle BALC_SPAN of the bow: the real slabs stop
    # well short of the rounded ends, and a slab that runs the whole arc turns
    # into a spike at each end once it is offset outward.
    m = len(plan)
    arc0 = len(WEST_INNER) - 2 if tag == "west" else len(EAST_INNER) - 2
    arc = plan[arc0:]
    lo = int(round(len(arc) * (1.0 - BALC_SPAN) / 2.0))
    balc_arc = arc[lo:len(arc) - lo]
    cxv = sum(p[0] for p in plan) / m
    cyv = sum(p[1] for p in plan) / m
    for i in range(TOWER_FLOORS):
        z0 = Z_PODIUM + FLOOR_H * i + T_SPANDREL - 0.10
        outer = []
        for j in range(len(balc_arc) - 1):
            a, b = balc_arc[j], balc_arc[j + 1]
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1.0
            nx, ny = dy / L, -dx / L
            if (a[0] + nx - cxv) ** 2 + (a[1] + ny - cyv) ** 2 < (a[0] - cxv) ** 2 + (a[1] - cyv) ** 2:
                nx, ny = -nx, -ny
            outer.append((a[0] + nx * BALC_OUT, a[1] + ny * BALC_OUT))
            if j == len(balc_arc) - 2:
                outer.append((b[0] + nx * BALC_OUT, b[1] + ny * BALC_OUT))
        ribbon = outer + [balc_arc[j] for j in range(len(balc_arc) - 1, -1, -1)]
        prism(f"{tag}_balc_{i}", ribbon, z0, z0 + BALC_T, mats["Toy_trim"])

    # Vertical piers flanking the central bay. Without them the shaft is 16
    # horizontal bands and 16 balcony slabs and nothing to stop the eye; the
    # reference photographs show a strong pair of piers running the full height.
    pier_at = []
    for s_ in (-1.0, 1.0):
        along = ((centre[0] + axis[0] * s_ * BAY_HALF, centre[1] + axis[1] * s_ * BAY_HALF))
        # walk the bow for the point nearest that station
        best = min(arc, key=lambda q: (q[0] - along[0]) ** 2 + (q[1] - along[1]) ** 2)
        dx, dy = best[0] - cxv, best[1] - cyv
        L = math.hypot(dx, dy) or 1.0
        px2, py2 = best[0] + dx / L * 0.35, best[1] + dy / L * 0.35
        box(f"{tag}_pier_{int(s_)}", px2, py2, 3.20, 2.40, Z_PODIUM,
            Z_SHOULDER - CORNICE_H + 0.15, mats["Toy_sand"],
            math.atan2(dy, dx))
        pier_at.append((px2, py2))

    # Shoulder: the heavy rolled bullnose cornice — two stacked steps, because a
    # single fascia band reads as a ledge and this profile is the tower's
    # signature. Then the deck and its parapet.
    prism(f"{tag}_cornice", inset_polygon(plan, -CORNICE_OUT),
          Z_SHOULDER - CORNICE_H, Z_SHOULDER - 0.45, mats["Toy_trim"])
    prism(f"{tag}_cornice_cap", inset_polygon(plan, -(CORNICE_OUT - 0.45)),
          Z_SHOULDER - 0.55, Z_SHOULDER, mats["Toy_trim"])
    prism(f"{tag}_shoulder_deck", inset_polygon(plan, 0.45), Z_SHOULDER - 0.30,
          Z_SHOULDER + 0.16, mats["Toy_steel"])
    rim(f"{tag}_shoulder_parapet", plan, 0.45, Z_SHOULDER - 0.10, Z_SHOULDER + 0.85,
        mats["Toy_trim"])

    # Mechanical penthouses on the two shoulder decks, inside the parapet.
    for s_ in (-1, 1):
        px = centre[0] + axis[0] * s_ * 15.0
        py = centre[1] + axis[1] * s_ * 15.0
        box(f"{tag}_mech_{s_}", px, py, 7.5, 5.0, Z_SHOULDER - 0.10, Z_SHOULDER + 2.30,
            mats["Toy_stone"], ang)

    # Central bay: the middle slab of the lozenge, 2.5 storeys taller, pushed a
    # little proud of the bow so it reads as a separate volume from below.
    bayp = inset_polygon(clip_band(plan, centre, axis, BAY_HALF), -0.45)
    bglass = inset_polygon(bayp, 0.30)
    for i in range(2):
        z0 = Z_SHOULDER + 3.20 * i
        prism(f"{tag}_bay_band_{i}", bayp, z0, z0 + T_SPANDREL, mats["Toy_sand"])
        prism(f"{tag}_bay_glass_{i}", bglass, z0 + T_SPANDREL - EMBED, z0 + 3.20 + EMBED,
              mats["Toy_glass"])
    prism(f"{tag}_bay_top", bayp, Z_SHOULDER + 6.40, Z_BAY - CORNICE_H, mats["Toy_sand"])
    prism(f"{tag}_bay_cornice", inset_polygon(bayp, -0.95), Z_BAY - CORNICE_H,
          Z_BAY - 0.40, mats["Toy_trim"])
    prism(f"{tag}_bay_cornice_cap", inset_polygon(bayp, -0.50), Z_BAY - 0.50, Z_BAY,
          mats["Toy_trim"])
    prism(f"{tag}_bay_deck", inset_polygon(bayp, 0.50), Z_BAY - 0.30, Z_BAY + 0.16,
          mats["Toy_steel"])
    rim(f"{tag}_bay_parapet", bayp, 0.50, Z_BAY - 0.10, Z_BAY + 0.70, mats["Toy_trim"])

    # Arched penthouse: a walled storey with a window band, capped by a shallow
    # segmental barrel whose apex is the LiDAR crest.
    ux, uy = axis
    vx, vy = -uy, ux

    def pen(t, s_):
        return (centre[0] + ux * s_ * ARCH_HALF + vx * t,
                centre[1] + uy * s_ * ARCH_HALF + vy * t)

    wall = [pen(-ARCH_W / 2.0, -1.0), pen(ARCH_W / 2.0, -1.0),
            pen(ARCH_W / 2.0, 1.0), pen(-ARCH_W / 2.0, 1.0)]
    prism(f"{tag}_penthouse", wall, Z_BAY - 0.20, Z_PENT, mats["Toy_sand"])
    prism(f"{tag}_penthouse_glass", inset_polygon(wall, 0.28), Z_BAY + 0.35,
          Z_PENT - 0.35, mats["Toy_glass"])

    prof = []
    for i in range(ARCH_SEGS + 1):
        t = -1.0 + 2.0 * i / ARCH_SEGS
        prof.append((t * (ARCH_W / 2.0 + 0.35),
                     Z_PENT - 0.30 + (Z_ARCH - Z_PENT + 0.30) * math.sqrt(max(0.0, 1.0 - t * t))))
    verts, faces = [], []
    for s_ in (-1.0, 1.0):
        for t, z in prof:
            verts.append((centre[0] + ux * s_ * (ARCH_HALF + 0.30) + vx * t,
                          centre[1] + uy * s_ * (ARCH_HALF + 0.30) + vy * t, z))
    k = len(prof)
    for i in range(k - 1):
        faces.append((i, i + 1, k + i + 1, k + i))
    faces.append((k - 1, 0, k, k + k - 1))          # underside
    faces.append(tuple(range(k - 1, -1, -1)))
    faces.append(tuple(range(k, 2 * k)))
    new_mesh(f"{tag}_arch", verts, faces, [mats["Toy_trim"]])

    # The crown's window band: the hero glow. It sits under the barrel's
    # springing, so it runs ALONG the tower axis on the two curved sides, not
    # across the gable ends.
    for s_ in (-1.0, 1.0):
        a = (centre[0] + ux * (-ARCH_HALF + 0.9) + vx * s_ * ARCH_W / 2.0,
             centre[1] + uy * (-ARCH_HALF + 0.9) + vy * s_ * ARCH_W / 2.0)
        b = (centre[0] + ux * (ARCH_HALF - 0.9) + vx * s_ * ARCH_W / 2.0,
             centre[1] + uy * (ARCH_HALF - 0.9) + vy * s_ * ARCH_W / 2.0)
        glow_quad(f"{tag}_glow_crown_{int(s_)}", a, b, Z_BAY + 0.45, Z_PENT - 0.35,
                  (vx * s_, vy * s_), mats["Toy_gold_Glow"], 0.12)

    # Mast.
    r0, r1 = 0.42, 0.15
    segs = 8
    verts, faces = [], []
    for r, z in ((r0, Z_ARCH - 0.9), (r1, Z_TIP)):
        for i in range(segs):
            th = 2 * math.pi * i / segs
            verts.append((centre[0] + r * math.cos(th), centre[1] + r * math.sin(th), z))
    for i in range(segs):
        j = (i + 1) % segs
        faces.append((i, j, segs + j, segs + i))
    faces.append(tuple(range(segs - 1, -1, -1)))
    faces.append(tuple(range(segs, 2 * segs)))
    new_mesh(f"{tag}_mast", verts, faces, [mats["Toy_steel"]])

    # Lit apartment ribbons: open strips on the bow at the chosen floors. The
    # runs BREAK at the two piers - a glow face standing 0.36 m proud of the bow
    # behind a pier that projects 1.55 m is a lit window nobody can see, and the
    # validator's open-strip test says so.
    runs = []
    cur = []
    # arc[0] and arc[-1] are the bow's ends, where it turns into the courtyard
    # wings; a glow quad on those segments faces into the corner rather than at
    # the wall it is meant to sit on.
    for q in arc[1:-1]:
        if any(math.hypot(q[0] - px3, q[1] - py3) < 2.9 for px3, py3 in pier_at):
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
        else:
            cur.append(q)
    if len(cur) >= 2:
        runs.append(cur)
    for i in sorted(lit):
        z0 = Z_PODIUM + FLOOR_H * i + T_SPANDREL
        for r, run in enumerate(runs):
            glow_strip(f"{tag}_glow_lit_{i}_{r}", run, z0 + 0.12,
                       z0 + FLOOR_H - T_SPANDREL - 0.12, mats["Toy_glassl_Glow"],
                       0.36, ref=(cxv, cyv))


# ----------------------------------------------------------------------- build


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    mats = {name: make_material(name) for name in PALETTE}

    podium(mats)
    entrance(mats)
    courtyard(mats)
    tower("west", WEST_PLAN, WEST_C, WEST_U, LIT_W, mats)
    tower("east", EAST_PLAN, EAST_C, EAST_U, LIT_E, mats)

    # Bevel budget: the chunky masses carry the miniature read. Ribbons, slabs,
    # glow strips and the many-sided podium bands are either too thin to bevel or
    # too numerous to afford it.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        n = obj.name
        if "_glass" in n or "_glow" in n or "_balc_" in n:
            continue
        if "_cornice_cap" in n:
            continue
        if n.startswith(("podium_band", "podium_glass", "west_band", "east_band",
                         "west_glass", "east_glass", "court_planting",
                         "podium_shop", "podium_deck", "west_shoulder_deck",
                         "east_shoulder_deck", "west_bay_deck", "east_bay_deck",
                         "west_penthouse_glass", "east_penthouse_glass")):
            continue
        if "_parapet" in n:
            continue
        if n.startswith(("pier_", "court_terrace", "court_planting",
                         "court_pergola", "court_plaza_ring", "court_floor",
                         "court_bed", "court_lawn", "court_planter")):
            continue
        if n.startswith(("west_mast", "east_mast", "roof_sky", "roof_solar")):
            bevel(obj, width=0.05, segments=1)
        else:
            bevel(obj, width=BEVEL_W, segments=BEVEL_SEG)

    recentre()
    return scene


ANCHOR_SHIFT = [0.0, 0.0]


def recentre():
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
    per = {}
    for o in objs:
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        t = len(me.loop_triangles)
        tris += t
        key = o.name.rstrip("0123456789_-")
        per[key] = per.get(key, 0) + t
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
        o.evaluated_get(dg).to_mesh_clear()
    print(f"[build] objects={len(objs)} tris={tris}")
    for k in sorted(per, key=lambda k: -per[k])[:14]:
        print(f"[build]   {k:26s} {per[k]:6d}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    lon = DESIGN_ANCHOR[0] + ANCHOR_SHIFT[0] / LON_M
    lat = DESIGN_ANCHOR[1] + ANCHOR_SHIFT[1] / LAT_M
    print(f"[build] anchor shift (m E, m N): {[round(v, 3) for v in ANCHOR_SHIFT]}")
    print(f"[build] MANIFEST anchor lon/lat: {lon:.7f} {lat:.7f}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "towers-at-rincon.blend")
    glb = os.path.join(out, "towers-at-rincon.glb")
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
