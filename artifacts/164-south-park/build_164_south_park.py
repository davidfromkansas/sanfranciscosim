"""Deterministic Blender build of the SF-SIM miniature 164 South Park.

    blender -b --python build_164_south_park.py -- [--out DIR]

Writes 164-south-park.blend and 164-south-park.glb next to this file (or into
--out). Geometry is authored in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = model XY bbox centre, min Z = 0, rear parapet crest
exactly 5.40 m.

Design (see REFERENCE.md for the sources behind every number):

* a 1907 single-storey brick warehouse at the west tip of the South Park oval,
  wearing a 2024-25 Stanley Saitowitz | Natoma Architects front: large-format
  red panels in stretcher bond, one black ribbon window that tracks the shift
  around the oval and drops to become a glazed entry recess, and a slender
  black canopy. The concrete doormat at that entry says Twitter and Instagram
  were both founded here, which is true;
* the recognition rests on TWO things. First, it is the only saturated red
  plane on the rim. Second, and stranger, the street screen (4.10 m) is
  LOWER than the building behind it (5.40 m) — every other building on this
  oval presents its tallest face to the park. From the app's aerial camera that
  reads as a red bar lying in front of a pale roof with a shadow between them;
* the ribbon is ONE band. It mitres around all five facets and it does not stop
  at the entry — it drops to the ground there. Breaking it into windows
  destroys the building;
* the roof is the third facade: flat pale membrane at 5.10 m inside a 5.40 m
  parapet, four glazed skylight monitors in two staggered rows, two mechanical
  boxes. The skylights are why the famously dark Twitter room had any daylight;
* night state: the ribbon and the entry glazing are one continuous lit band —
  the daytime idea seen at night — plus a single thin spill on the canopy
  soffit. Glow surfaces are single-sided shells 0.01 m proud of the opaque
  glazing, because the app draws _Glow in a separate layer at ~12% alpha per
  surface by day and a closed shell would tint the whole facade pink.

Authoring frame: the plan polygon is authored directly in world metres relative
to the surveyed parcel-union centroid, because the street elevation is five
facets turning through 49 deg and no single local axis describes it. The screen,
the ribbon and the canopy are swept along a MITRED chain built from that
polygon; "outward" always comes from the segment normals, never from the
building centroid, which folds at the 135.2 deg chamfer (see the plan's 2.7).
The building sits ~45 deg off the world axes, so the axis-aligned XY bounding
box is ~35.7 x 36.2 m even though the building is a 42 x 16 m wedge. That is
expected, not a scale error.
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

# Area centroid of the union of surveyed parcels 3775068 + 3775069 (both are
# addressed 164) = the MANIFEST anchor before recentring. Plan 2.3.
DESIGN_ANCHOR = (-122.3949238, 37.7812072)

# Design footprint, metres east/north from DESIGN_ANCHOR. Nine corners, from the
# DataSF parcel survey; IoU 0.895 against the DataSF LiDAR building footprint.
FOOTPRINT = [
    (-19.725,  12.057),   # v0 rear-west corner
    (  9.974, -17.722),   # v1 south corner, street end of the SW party line
    ( 15.275, -12.461),   # v2 south end of the frontage arc
    ( 15.061,  -9.380),   # v3
    ( 15.117,  -6.321),   # v4
    ( 15.395,  -3.595),   # v5
    ( 15.957,  -0.586),   # v6 north corner of the frontage
    (  3.482,   1.704),   # v7 north party corner with 160 South Park
    (-13.260,  18.491),   # v8 rear-north corner
]

# The exposed street elevation, as indices into FOOTPRINT, ordered NORTH to
# SOUTH — the direction the screen chain runs and the direction t increases.
STREET_IDX = [6, 5, 4, 3, 2, 1]

Z_DECK = 5.10           # flat roof membrane. INFERRED = crest - 0.30 m upstand.
Z_CREST = 5.40          # rear parapet crest — the bbox top, and the manifest
                        # targetHeightM, so the loader's scale is exactly 1.0.
                        # MEASURED: DataSF LiDAR height median over 1715 cells,
                        # sd 0.84 m. The 9.25 m maximum is rejected; see the
                        # plan's 2.15 for the four independent reasons.
PARAPET_W = 0.22

Z_SCREEN = 4.10         # red panel screen parapet. PHOTOGRAMMETRIC, two
                        # independent photographs, 4.01 m and 4.11 m.
SCREEN_D = 0.35         # how far the screen stands proud of the body wall. Real
                        # (rainscreen cavity + panel) and load-bearing for the
                        # design: it is what makes the 1.3 m step read as two
                        # objects with a shadow between them instead of one wall
                        # with a setback.

Z_SILL, Z_HEAD = 1.55, 2.95   # ribbon window. PHOTOGRAMMETRIC.
GLASS_D = 0.16          # ribbon glass, measured back from the body wall face
FRAME_D0, FRAME_D1 = 0.21, 0.33   # ribbon frame bars, ditto
FRAME_W = 0.07          # frame bar height/width
MULLION_W = 0.06
MULLION_PITCH = 1.60

COURSE = 0.47           # panel course. PHOTOGRAMMETRIC: 8.7 uniform courses
                        # between grade and the screen parapet.
GROOVE_PITCH = 2 * COURSE   # the miniature cuts EVERY SECOND real joint. At
                        # 0.47 m the reveals read as clapboard from the app's
                        # camera, which is the opposite of "large scale panels".
                        # Style bible 22: keep the rhythm, drop the count.
GROOVE_H = 0.035        # the joint reveal, exaggerated from ~8 mm so it
                        # survives the miniature
GROOVE_D = 0.035        # how deep the reveal is cut into the panel face

# Entry recess, as arc length from the north end of the frontage (v6 = t 0).
T_ENTRY0, T_ENTRY1 = 1.90, 5.50
ENTRY_NOTCH = 0.65      # how far the BODY is pulled back behind the screen, so
                        # the total recess depth is 0.35 + 0.65 = 1.00 m
Z_ENTRY_HEAD = 3.30     # entry glazing head; red lintel band runs above it
Z_TRANSOM = 2.35
DOOR_W = 1.90

CAN_SOFFIT = 2.98       # canopy blade. PHOTOGRAMMETRIC (2.87-3.09 m).
CAN_T = 0.14            # thickness, exaggerated from ~0.10 so it still throws
                        # a shadow at miniature scale
CAN_PROJ = 1.50         # projection beyond the screen face
CAN_OVER = 0.40         # how far it runs past the recess at each end
NUM_H = 0.35            # the 164 numerals on the canopy fascia
NUM_D = 0.03

SKY_L, SKY_W, SKY_H = 2.40, 1.40, 0.28   # skylight monitors (0.28, not 0.35,
                                         # so the parapet keeps the crest)
MECH = (1.20, 0.90, 0.26)

BEVEL_W, BEVEL_SEG = 0.020, 2   # below half the 0.035 joint reveal, or
                                # the bevel collapses the groove faces

PALETTE_HEX = {
    "Toy_red": "c4453c",      # THE SCREEN, and nothing else. On-palette by a
                              # happy accident: the sunlit panel samples
                              # #C44B38 in the architect's photographs, which is
                              # Toy_red to within two units per channel.
    "Toy_brick": "c96f4a",    # the retained warehouse: both party flanks, the
                              # rear, and the strip of body above the screen
    "Toy_ink": "3a3530",      # ribbon frame and mullions, entry frame and
                              # doors, the canopy and its outriggers
    "Toy_glass": "2a4d73",
    "Toy_steel": "9aa0a6",    # the roof membrane.
                              # NOT Toy_roofd: on a flat roof under the app's
                              # lighting that renders at about rgb(9,9,12), a
                              # black hole where a pale membrane should be.
    "Toy_trim": "f3efe6",     # parapet coping, the 164 numerals
    "Toy_glass_Glow": "6f95b8",   # the ribbon + entry band at night
    "Toy_trim_Glow": "f3efe6",    # one thin spill on the canopy soffit
}

Z = Vector((0.0, 0.0, 1.0))


# ------------------------------------------------------------------ helpers

def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def make_material(name):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    h = PALETTE_HEX[name]
    rgb = [srgb_to_linear(int(h[i:i + 2], 16) / 255.0) for i in (0, 2, 4)]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.62
    bsdf.inputs["Metallic"].default_value = 0.0
    if name.endswith("_Glow"):
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    return mat


MATS = {}


def mat(name):
    if name not in MATS:
        MATS[name] = make_material(name)
    return MATS[name]


def signed_area(poly):
    a = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        a += x1 * y2 - x2 * y1
    return a / 2.0


def seg_normals(pts, closed):
    """Outward unit normal per segment, from the WINDING, never from a centroid.

    For a CCW ring in a right-handed XY frame the outward normal of the segment
    p->q is (dy, -dx) normalised. The plan's 2.7 is explicit about this: this
    footprint has a 135.2 deg chamfer and 49 deg of arc, and a centroid-derived
    outward folds at both.
    """
    ns = []
    n = len(pts)
    last = n if closed else n - 1
    for i in range(last):
        px, py = pts[i]
        qx, qy = pts[(i + 1) % n]
        dx, dy = qx - px, qy - py
        L = math.hypot(dx, dy)
        ns.append(Vector((dy / L, -dx / L, 0.0)))
    return ns


def mitre_vectors(pts, closed):
    """Per-VERTEX offset vector m with m.n_prev == m.n_next == 1, so that
    P + d*m is the exact offset of the polyline by d."""
    ns = seg_normals(pts, closed)
    out = []
    n = len(pts)
    for i in range(n):
        if closed:
            a, b = ns[(i - 1) % n], ns[i]
        else:
            if i == 0:
                a = b = ns[0]
            elif i == n - 1:
                a = b = ns[-1]
            else:
                a, b = ns[i - 1], ns[i]
        c = a.dot(b)
        out.append((a + b) / (1.0 + c) if c > -0.999 else a.copy())
    return out


def offset_ring(poly, d):
    """Offset a closed ring outward by d (negative = inward), mitred."""
    ms = mitre_vectors(poly, True)
    return [(poly[i][0] + d * ms[i].x, poly[i][1] + d * ms[i].y)
            for i in range(len(poly))]


def new_mesh(name, verts, faces, material):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], faces)
    me.validate()
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(mat(material))
    return ob


def prism(name, poly, z0, z1, material):
    """Closed solid from a CCW ring extruded z0..z1, outward normals."""
    n = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, j, n + j, n + i])            # side, outward
    faces.append(list(range(n - 1, -1, -1)))          # bottom, -Z
    faces.append(list(range(n, 2 * n)))               # top, +Z
    return new_mesh(name, verts, faces, material)


def box(name, centre, size, material, rot_z=0.0):
    cx, cy, cz = centre
    sx, sy, sz = (s / 2.0 for s in size)
    c, s = math.cos(rot_z), math.sin(rot_z)
    corners = [(-sx, -sy), (sx, -sy), (sx, sy), (-sx, sy)]
    ring = [(cx + x * c - y * s, cy + x * s + y * c) for x, y in corners]
    return prism(name, ring, cz - sz, cz + sz, material)


def sweep(name, chain, profile, material, close_start=True, close_end=True,
          loop=False, nsign=1.0):
    """Sweep a closed 2D profile, given as (d, z) pairs CCW in the (outward,
    up) plane, along an open mitred chain of XY points.

    d is measured outward from the chain, z is world height. Returns one closed
    manifold solid with outward normals.

    nsign flips which side "outward" is. The street chain runs v6 -> v1, i.e.
    BACKWARDS along the CCW footprint ring, so its segment normals point into
    the building and every street sweep passes nsign=-1. Getting this wrong
    builds the whole screen inside the body, where it is invisible.
    """
    ms = [m * nsign for m in mitre_vectors(chain, loop)]
    ns = len(chain)
    np_ = len(profile)
    verts = []
    for j, (px, py) in enumerate(chain):
        m = ms[j]
        for (d, z) in profile:
            verts.append((px + d * m.x, py + d * m.y, z))
    faces = []
    for j in range(ns if loop else ns - 1):
        jn = (j + 1) % ns
        for i in range(np_):
            k = (i + 1) % np_
            a = j * np_ + i
            b = j * np_ + k
            c = jn * np_ + k
            e = jn * np_ + i
            faces.append([a, b, c, e])
    if loop:
        close_start = close_end = False
    if close_start:
        faces.append(list(range(np_ - 1, -1, -1)))
    if close_end:
        o = (ns - 1) * np_
        faces.append([o + i for i in range(np_)])
    ob = new_mesh(name, verts, faces, material)
    # The winding above assumes the profile runs CCW in (d, z); if the sweep
    # came out inside-out (concave mitre at a tight corner cannot do this, but
    # a reversed profile can), fix it once here rather than trusting the caller.
    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.normal_update()
    vol = bm.calc_volume(signed=True)
    if vol < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
        bm.to_mesh(me)
    bm.free()
    me.update()
    return ob


def grooved_profile(z0, z1, courses_from=0.0):
    """Panel face profile in (d, z): outer face at SCREEN_D with a joint reveal
    cut GROOVE_D deep every COURSE metres, back face at 0.

    Only the reveals that fall inside [z0, z1] are cut, so the ribbon opening
    does not leave half a groove hanging in the air.
    """
    up = [(SCREEN_D, z0)]
    k = 1
    while True:
        zc = courses_from + k * GROOVE_PITCH
        k += 1
        if zc - GROOVE_H / 2 <= z0 + 0.06:
            continue
        if zc + GROOVE_H / 2 >= z1 - 0.06:
            break
        up += [(SCREEN_D, zc - GROOVE_H / 2),
               (SCREEN_D - GROOVE_D, zc - GROOVE_H / 2),
               (SCREEN_D - GROOVE_D, zc + GROOVE_H / 2),
               (SCREEN_D, zc + GROOVE_H / 2)]
    up += [(SCREEN_D, z1), (0.0, z1), (0.0, z0)]
    return up


def resample(chain_pts, t_lo, t_hi):
    """Sub-chain of a polyline between two arc lengths, keeping every original
    vertex in between so facet corners survive."""
    segs = []
    acc = 0.0
    for i in range(len(chain_pts) - 1):
        a = Vector(chain_pts[i] + (0.0,))
        b = Vector(chain_pts[i + 1] + (0.0,))
        L = (b - a).length
        segs.append((acc, acc + L, chain_pts[i], chain_pts[i + 1], L))
        acc += L
    out = []

    def at(t):
        for s0, s1, a, b, L in segs:
            if t <= s1 + 1e-9:
                f = (t - s0) / L
                return (a[0] + f * (b[0] - a[0]), a[1] + f * (b[1] - a[1]))
        return chain_pts[-1]

    out.append(at(t_lo))
    for s0, s1, a, b, L in segs:
        if t_lo + 1e-6 < s1 < t_hi - 1e-6:
            out.append(b)
    out.append(at(t_hi))
    # Drop stations that coincide: a t bound landing on a facet corner makes a
    # zero-length segment, and every quad swept on it is a degenerate pair.
    ded = [out[0]]
    for p in out[1:]:
        if math.dist(p, ded[-1]) > 1e-4:
            ded.append(p)
    return ded if len(ded) > 1 else out[:2]


# -------------------------------------------------------------------- build

def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)

    poly = list(FOOTPRINT)
    if signed_area(poly) < 0:
        poly.reverse()
    # STREET_IDX was written against the original order; recover the street
    # chain by position rather than by index after a possible reverse.
    street_pts = [FOOTPRINT[i] for i in STREET_IDX]

    chain_len = sum(
        math.dist(street_pts[i], street_pts[i + 1])
        for i in range(len(street_pts) - 1)
    )

    # -- the body, with the entry notch cut into its street wall -------------
    ms_chain = mitre_vectors(street_pts, False)
    notch_chain = resample(street_pts, T_ENTRY0, T_ENTRY1)
    nm = mitre_vectors(notch_chain, False)
    # nm points INTO the building on the street-ordered chain (see sweep), so
    # pulling the wall back into the building ADDS the offset.
    notch_in = [(notch_chain[i][0] + ENTRY_NOTCH * nm[i].x,
                 notch_chain[i][1] + ENTRY_NOTCH * nm[i].y)
                for i in range(len(notch_chain))]

    # Splice the notch into the body ring. street_pts runs v6 -> v1, i.e.
    # BACKWARDS along the ring, so the notch is inserted reversed.
    body_ring = []
    for i, p in enumerate(poly):
        body_ring.append(p)
        if p == FOOTPRINT[1]:          # after v1, walking v1 -> v2 -> ... -> v6
            pass
    body_ring = []
    for p in poly:
        body_ring.append(p)
    # insert between v4 and v6 travelling v1->v6: that is after FOOTPRINT[4]
    ins_after = body_ring.index(FOOTPRINT[4])
    spliced = list(reversed(notch_chain[:1] + notch_in + notch_chain[-1:]))
    body_ring = body_ring[:ins_after + 1] + spliced + body_ring[ins_after + 1:]
    # v5 sits inside the notch span and is now superseded by the notch line
    if FOOTPRINT[5] in body_ring:
        body_ring.remove(FOOTPRINT[5])

    # The entry recess is cut into the wall, not into the roof: notch the body
    # only up to the entry head and carry the full ring above it, or the
    # parapet and the roof outline inherit a notch that does not exist.
    body = prism("body", body_ring, 0.0, Z_ENTRY_HEAD, "Toy_brick")
    body_up = prism("body_upper", poly, Z_ENTRY_HEAD - 0.002, Z_DECK, "Toy_brick")

    inner = offset_ring(poly, -PARAPET_W)
    deck = prism("roof_deck", inner, Z_DECK - 0.08, Z_DECK + 0.02, "Toy_steel")
    parapet_out = sweep(
        "parapet", poly,
        [(0.0, Z_DECK - 0.05), (0.0, Z_CREST - 0.05),
         (-PARAPET_W, Z_CREST - 0.05), (-PARAPET_W, Z_DECK - 0.05)],
        "Toy_brick", loop=True)
    coping = sweep(
        "coping", poly,
        [(0.012, Z_CREST - 0.05), (0.012, Z_CREST),
         (-PARAPET_W - 0.012, Z_CREST), (-PARAPET_W - 0.012, Z_CREST - 0.05)],
        "Toy_trim", loop=True)

    # -- the red screen ------------------------------------------------------
    E = 0.002   # 2 mm overlap so butting solids are never exactly coplanar
    pier = sweep("screen_pier", resample(street_pts, 0.0, T_ENTRY0 + E),
                 grooved_profile(0.0, Z_SCREEN), "Toy_red", nsign=-1.0)
    lintel = sweep("screen_lintel",
                   resample(street_pts, T_ENTRY0 - E, T_ENTRY1 + E),
                   grooved_profile(Z_ENTRY_HEAD, Z_SCREEN), "Toy_red", nsign=-1.0)
    low = sweep("screen_low", resample(street_pts, T_ENTRY1 - E, chain_len),
                grooved_profile(0.0, Z_SILL), "Toy_red", nsign=-1.0)
    high = sweep("screen_high", resample(street_pts, T_ENTRY1 - E, chain_len),
                 grooved_profile(Z_HEAD, Z_SCREEN), "Toy_red", nsign=-1.0)

    # reveals of the entry recess, faced in panel like the real one
    rev = []
    for t in (T_ENTRY0, T_ENTRY1):
        sub = resample(street_pts, max(0.0, t - 0.001), min(chain_len, t + 0.001))
        rev.append(sweep(f"entry_reveal_{t:.1f}",
                         [(sub[0][0], sub[0][1]), (sub[-1][0], sub[-1][1])],
                         [(SCREEN_D, 0.0), (SCREEN_D, Z_ENTRY_HEAD),
                          (-ENTRY_NOTCH, Z_ENTRY_HEAD), (-ENTRY_NOTCH, 0.0)],
                         "Toy_red", nsign=-1.0))
    soffit = sweep("entry_soffit", notch_chain,
                   [(SCREEN_D, Z_ENTRY_HEAD - 0.08), (SCREEN_D, Z_ENTRY_HEAD),
                    (-ENTRY_NOTCH, Z_ENTRY_HEAD), (-ENTRY_NOTCH, Z_ENTRY_HEAD - 0.08)],
                   "Toy_ink", nsign=-1.0)

    # -- the ribbon window ---------------------------------------------------
    rib = resample(street_pts, T_ENTRY1, chain_len)
    glass = sweep("ribbon_glass", rib,
                  [(GLASS_D, Z_SILL + FRAME_W), (GLASS_D + 0.04, Z_SILL + FRAME_W),
                   (GLASS_D + 0.04, Z_HEAD - FRAME_W), (GLASS_D, Z_HEAD - FRAME_W)],
                  "Toy_glass", nsign=-1.0)
    glow = sweep("ribbon_glow", rib,
                 [(GLASS_D + 0.04, Z_SILL + FRAME_W),
                  (GLASS_D + 0.05, Z_SILL + FRAME_W),
                  (GLASS_D + 0.05, Z_HEAD - FRAME_W),
                  (GLASS_D + 0.04, Z_HEAD - FRAME_W)],
                 "Toy_glass_Glow", nsign=-1.0)
    sill_bar = sweep("ribbon_sill", rib,
                     [(FRAME_D0, Z_SILL), (FRAME_D1, Z_SILL),
                      (FRAME_D1, Z_SILL + FRAME_W), (FRAME_D0, Z_SILL + FRAME_W)],
                     "Toy_ink", nsign=-1.0)
    head_bar = sweep("ribbon_head", rib,
                     [(FRAME_D0, Z_HEAD - FRAME_W), (FRAME_D1, Z_HEAD - FRAME_W),
                      (FRAME_D1, Z_HEAD), (FRAME_D0, Z_HEAD)],
                     "Toy_ink", nsign=-1.0)

    mullions = []
    t = T_ENTRY1
    k = 0
    while t < chain_len - 0.3:
        sub = resample(street_pts, t, min(chain_len, t + MULLION_W))
        mullions.append(sweep(
            f"mullion_{k}", [(sub[0][0], sub[0][1]), (sub[-1][0], sub[-1][1])],
            [(FRAME_D0, Z_SILL + FRAME_W), (FRAME_D1, Z_SILL + FRAME_W),
             (FRAME_D1, Z_HEAD - FRAME_W), (FRAME_D0, Z_HEAD - FRAME_W)],
            "Toy_ink", nsign=-1.0))
        k += 1
        t += MULLION_PITCH

    # -- the entry -----------------------------------------------------------
    eg = sweep("entry_glass", notch_chain,
               [(-ENTRY_NOTCH + 0.04, 0.0), (-ENTRY_NOTCH + 0.08, 0.0),
                (-ENTRY_NOTCH + 0.08, Z_ENTRY_HEAD - 0.06),
                (-ENTRY_NOTCH + 0.04, Z_ENTRY_HEAD - 0.06)],
               "Toy_glass", nsign=-1.0)
    eglow = sweep("entry_glow", notch_chain,
                  [(-ENTRY_NOTCH + 0.08, 0.02), (-ENTRY_NOTCH + 0.09, 0.02),
                   (-ENTRY_NOTCH + 0.09, Z_ENTRY_HEAD - 0.08),
                   (-ENTRY_NOTCH + 0.08, Z_ENTRY_HEAD - 0.08)],
                  "Toy_glass_Glow", nsign=-1.0)
    ehead = sweep("entry_head", notch_chain,
                  [(-ENTRY_NOTCH + 0.02, Z_ENTRY_HEAD - 0.08),
                   (-ENTRY_NOTCH + 0.15, Z_ENTRY_HEAD - 0.08),
                   (-ENTRY_NOTCH + 0.15, Z_ENTRY_HEAD),
                   (-ENTRY_NOTCH + 0.02, Z_ENTRY_HEAD)],
                  "Toy_ink", nsign=-1.0)
    etrans = sweep("entry_transom", notch_chain,
                   [(-ENTRY_NOTCH + 0.06, Z_TRANSOM),
                    (-ENTRY_NOTCH + 0.15, Z_TRANSOM),
                    (-ENTRY_NOTCH + 0.15, Z_TRANSOM + 0.07),
                    (-ENTRY_NOTCH + 0.06, Z_TRANSOM + 0.07)],
                   "Toy_ink", nsign=-1.0)

    tmid = (T_ENTRY0 + T_ENTRY1) / 2.0
    doors = []
    for sgn, tag in ((-1, "l"), (1, "r")):
        t0 = tmid + sgn * 0.03 if sgn > 0 else tmid - DOOR_W / 2
        t1 = tmid + DOOR_W / 2 if sgn > 0 else tmid - 0.03
        sub = resample(street_pts, t0, t1)
        doors.append(sweep(
            f"door_{tag}", [(sub[0][0], sub[0][1]), (sub[-1][0], sub[-1][1])],
            [(-ENTRY_NOTCH + 0.06, 0.0), (-ENTRY_NOTCH + 0.14, 0.0),
             (-ENTRY_NOTCH + 0.14, Z_TRANSOM), (-ENTRY_NOTCH + 0.06, Z_TRANSOM)],
            "Toy_ink", nsign=-1.0))

    # -- the canopy ----------------------------------------------------------
    can_chain = resample(street_pts, max(0.0, T_ENTRY0 - CAN_OVER),
                         min(chain_len, T_ENTRY1 + CAN_OVER))
    canopy = sweep("canopy", can_chain,
                   [(SCREEN_D - 0.02, CAN_SOFFIT), (SCREEN_D + CAN_PROJ, CAN_SOFFIT),
                    (SCREEN_D + CAN_PROJ, CAN_SOFFIT + CAN_T),
                    (SCREEN_D - 0.02, CAN_SOFFIT + CAN_T)],
                   "Toy_ink", nsign=-1.0)
    canglow = sweep("canopy_spill", can_chain,
                    [(SCREEN_D + 0.20, CAN_SOFFIT - 0.01),
                     (SCREEN_D + CAN_PROJ - 0.20, CAN_SOFFIT - 0.01),
                     (SCREEN_D + CAN_PROJ - 0.20, CAN_SOFFIT),
                     (SCREEN_D + 0.20, CAN_SOFFIT)],
                    "Toy_trim_Glow", nsign=-1.0)

    outriggers = []
    for i in range(4):
        t = T_ENTRY0 - CAN_OVER + 0.55 + i * ((T_ENTRY1 - T_ENTRY0 + 2 * CAN_OVER - 1.1) / 3.0)
        sub = resample(street_pts, t, t + 0.10)
        outriggers.append(sweep(
            f"outrigger_{i}", [(sub[0][0], sub[0][1]), (sub[-1][0], sub[-1][1])],
            [(SCREEN_D, CAN_SOFFIT + CAN_T), (SCREEN_D + 0.62, CAN_SOFFIT + CAN_T),
             (SCREEN_D + 0.62, CAN_SOFFIT + CAN_T + 0.05),
             (SCREEN_D, CAN_SOFFIT + CAN_T + 0.09)],
            "Toy_ink", nsign=-1.0))

    # the 164 numerals, block-built on the canopy fascia
    digits = {
        "1": [(0.28, 0.00, 0.10, 1.00)],
        "6": [(0.00, 0.00, 0.16, 1.00), (0.00, 0.84, 0.62, 0.16),
              (0.00, 0.42, 0.62, 0.16), (0.00, 0.00, 0.62, 0.16),
              (0.46, 0.00, 0.16, 0.58)],
        "4": [(0.00, 0.42, 0.16, 0.58), (0.00, 0.42, 0.62, 0.16),
              (0.46, 0.00, 0.16, 1.00)],
    }
    numerals = []
    dw = 0.62 * NUM_H
    # t increases SOUTHWARD along the frontage, and a viewer on the sidewalk
    # facing the building has north on the RIGHT, so reading order left-to-right
    # is DECREASING t. Lay the glyphs out backwards in t and mirror each block
    # within its cell, or the sign reads "b9l".
    fascia_t1 = tmid + 1.05
    for di, ch in enumerate("164"):
        for bi, (bx, bz, bw, bh) in enumerate(digits[ch]):
            t0 = fascia_t1 - di * (dw + 0.10) - (bx + bw) * NUM_H
            sub = resample(street_pts, t0, t0 + bw * NUM_H)
            z0 = CAN_SOFFIT + CAN_T + 0.06 + bz * NUM_H
            numerals.append(sweep(
                f"num_{di}_{bi}",
                [(sub[0][0], sub[0][1]), (sub[-1][0], sub[-1][1])],
                [(SCREEN_D + CAN_PROJ, z0), (SCREEN_D + CAN_PROJ + NUM_D, z0),
                 (SCREEN_D + CAN_PROJ + NUM_D, z0 + bh * NUM_H),
                 (SCREEN_D + CAN_PROJ, z0 + bh * NUM_H)],
                "Toy_trim", nsign=-1.0))

    # -- roof furniture ------------------------------------------------------
    # Positions are metres east/north from DESIGN_ANCHOR, taken along the SW
    # party line and offset inward, then checked point-in-polygon with a
    # clearance ≥ the monitor's half-diagonal. Two staggered rows, matching the
    # aerial. `ax` is the body's long axis so the monitors sit square to it.
    ax = math.radians(-45.1)
    SKY_AT = [(-6.723, 5.251), (-0.151, 2.626), (2.245, -3.458), (8.959, -5.942)]
    MECH_AT = [(-11.244, 9.217), (-7.920, 9.001)]
    roof = []
    for i, (cx, cy) in enumerate(SKY_AT):
        # pale curbs, dark glazing: that is how they read in the aerial, and a
        # Toy_steel curb on a Toy_steel deck disappears entirely.
        roof.append(box(f"skylight_{i}", (cx, cy, Z_DECK + SKY_H / 2),
                        (SKY_L, SKY_W, SKY_H), "Toy_trim", rot_z=ax))
        roof.append(box(f"skylight_glass_{i}", (cx, cy, Z_DECK + SKY_H - 0.02),
                        (SKY_L - 0.26, SKY_W - 0.26, 0.06), "Toy_glass", rot_z=ax))
    for i, (cx, cy) in enumerate(MECH_AT):
        roof.append(box(f"mech_{i}", (cx, cy, Z_DECK + MECH[2] / 2), MECH,
                        "Toy_ink", rot_z=ax))

    # -- bevel the massing, not the hairlines --------------------------------
    for ob in (body, body_up, parapet_out, pier, lintel, low, high, canopy):
        m = ob.modifiers.new("bevel", "BEVEL")
        m.width = BEVEL_W
        m.segments = BEVEL_SEG
        m.limit_method = "ANGLE"
        m.angle_limit = math.radians(35)
        m.harden_normals = False

    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    for ob in objs:
        ob.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.convert(target="MESH")

    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    for ob in objs:
        finalise(ob)
    return objs


def finalise(ob):
    """Weld coincident verts, dissolve degenerate faces, recalculate normals
    outward, and force flat shading.

    The weld threshold is deliberately tiny (0.1 mm). A generous weld smooths
    flat shading across a bevel and the app renders it as a soft blob; the
    style bible wants crisp facets.
    """
    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-5, edges=bm.edges)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    for f in bm.faces:
        f.smooth = False
    bm.to_mesh(me)
    bm.free()
    me.update()


def recentre(objs):
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    shift = Vector((-(mn.x + mx.x) / 2.0, -(mn.y + mx.y) / 2.0, -mn.z))
    for o in objs:
        o.location += shift
    bpy.ops.object.select_all(action="SELECT")
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return shift, mn, mx


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    out = argv[argv.index("--out") + 1] if "--out" in argv else here
    os.makedirs(out, exist_ok=True)

    objs = build()
    shift, mn, mx = recentre(objs)

    tris = sum(len(o.data.loop_triangles) for o in objs
               if (o.data.calc_loop_triangles() or True))
    dims = (mx.x - mn.x, mx.y - mn.y, mx.z - mn.z)

    # The manifest anchor is where the RECENTRED origin lands in the world.
    ax = -shift.x
    ay = -shift.y
    lon = DESIGN_ANCHOR[0] + ax / LON_M
    lat = DESIGN_ANCHOR[1] + ay / LAT_M

    print(f"[build] objects  {len(objs)}")
    print(f"[build] tris     {tris}")
    print(f"[build] dims     {dims[0]:.4f} x {dims[1]:.4f} x {dims[2]:.4f} m")
    print(f"[build] crest    {mx.z - mn.z:.4f} m (target {Z_CREST})")
    print(f"[build] anchor   {lon:.7f}, {lat:.7f}   (design {DESIGN_ANCHOR})")

    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, "164-south-park.blend"))
    bpy.ops.export_scene.gltf(
        filepath=os.path.join(out, "164-south-park.glb"),
        export_format="GLB",
        use_selection=False,
        export_apply=True,
        export_yup=True,
        export_materials="EXPORT",
        export_image_format="NONE",
        export_cameras=False,
        export_lights=False,
        export_animations=False,
        export_skins=False,
        export_morph=False,
    )
    print("[build] wrote 164-south-park.glb")


if __name__ == "__main__":
    main()
