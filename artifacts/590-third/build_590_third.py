"""Deterministic Blender build of the SF-SIM miniature 590 Third Street.

    blender -b --python build_590_third.py -- [--out DIR]

Writes 590-third.blend and 590-third.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = parcel-polygon centroid (anchor lon -122.3946749,
lat 37.7800837), min Z = 0, raised corner parapet top exactly 9.50 m.

Design (see REFERENCE.md for the sources behind every number):

* the DataSF parcel parallelogram (block 3776 lot 114) extruded as a two-storey
  painted-stucco commercial block holding the WEST corner of 3rd and Brannan —
  a base, not a wall. The building fills its lot, so two of four faces are blind
  party walls;
* the identity is TWO-TONE: a continuous glossy near-black shopfront band
  wrapping the whole ground floor of both street faces, unbroken around the east
  corner, under a plain pale-grey block;
* the one silhouette event is the RAISED CORNER PARAPET, stepping up 1.10 m over
  the corner bay and running 8.0 m back along Brannan and 7.0 m along 3rd;
* the two street faces are deliberately different: Brannan (23.10 m) is a steady
  rhythm of seven tall punched windows with through-wall AC boxes, 3rd Street
  (21.28 m) is three big sparse squares plus the blue CAFE BUENOS AIRES panel
  that is literally the address;
* the roof is a warm BROWN built-up membrane (every roof around it is grey) with
  a genuine LIGHT WELL cut through the shell — a real 3.54 x 2.18 m opening,
  corroborated by the interior ring of the DataSF LiDAR footprint;
* night state is a BAND, not a scatter: the shopfront ribbon glows continuously
  around the corner, the signage panels read as lit fascia, and only two upper
  windows are on. 599 Third across the street is the scatter; between them the
  intersection reads "shops below, homes above". Glow surfaces are thin shells
  proud of opaque glazing — the app renders _Glow in a separate layer at ~12%
  alpha by day, so a primary surface must never be authored as glow. Glow COLOUR
  must be light: the app draws that layer unlit at the material's own baked
  colour, so a dark navy glow would make a lit window read darker than an unlit
  one.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF parcel 3776114 projected with the app's tangent projection
# (LON0 -122.4375, LAT0 37.77) and recentred on the parcel centroid.
# CCW, (x east, y north). A true parallelogram: 21.28 x 23.10 m, 491.5 m2.
FOOTPRINT = [
    (-15.709, -0.602),  # 0  W  west corner   (SW party wall / NW party wall)
    (-0.689, -15.669),  # 1  S  south corner  (SW party wall / Brannan)
    (15.714, 0.602),    # 2  E  EAST CORNER — 3rd & Brannan, the hero corner
    (0.684, 15.669),    # 3  N  north corner  (3rd / NW party wall)
]
E_SW = (0, 1)  # SW party wall, 21.28 m, outward normal 225.2 deg (toward 414 Brannan)
E_BRANNAN = (1, 2)  # SE front, 23.10 m, outward normal 135.1 deg true — the long face
E_THIRD = (2, 3)  # NE front, 21.28 m, outward normal 45.2 deg true — the address face
E_NW = (3, 0)  # NW party wall, 23.10 m, normal 315.1 deg (toward the brick warehouse)

L_BRANNAN = 23.10
L_THIRD = 21.28

H_WALL = 7.80  # top of the wall shell / underside of the parapet
H_ROOF = 7.90  # roof membrane surface (LiDAR median 7.77 m)
H_PAR = 8.26  # main parapet below its coping
H_PAR_CAP = 8.40  # main parapet coping top
H_COR = 9.36  # raised corner parapet below its coping
H_COR_CAP = 9.50  # raised corner coping top = the target height / bbox top

# Where the corner parapet steps back down, measured from the east corner.
COR_BRANNAN = 8.00  # along Brannan, i.e. s from 15.10 to 23.10
COR_THIRD = 7.00  # along 3rd, i.e. s from 0.00 to 7.00

# A tall commercial ground floor under one office storey.
Z_SHOP_SILL = 0.20
Z_SHOP_HEAD = 3.10
Z_FASCIA_TOP = 4.10

# Light well: the interior ring of DataSF LiDAR footprint SF3776114, expressed
# in the building frame. A genuine hole through the shell, not a painted panel.
WELL_U, WELL_W = -4.78, 2.02
WELL_SU, WELL_SW = 3.54, 2.18

BEVEL_W = 0.08
BEVEL_SEG = 2

PALETTE_HEX = {
    "Toy_stone": "d9d2c2",
    "Toy_ink": "3a3530",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_trim": "f3efe6",
    "Toy_rust": "a86444",
    "Toy_roofd": "45454a",
    "Toy_sky": "6db3d9",
    "Toy_mustard_Glow": "d9a441",
    "Toy_trim_Glow": "f3efe6",
    "Toy_sky_Glow": "6db3d9",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def poly_edge(edge):
    """(a, b, length, tangent unit, outward normal) for a CCW footprint edge."""
    a, b = FOOTPRINT[edge[0]], FOOTPRINT[edge[1]]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> this points outward
    return a, b, length, t, n


def offset_polygon(poly, d):
    """Miter offset of a CCW polygon; positive d moves outward."""
    npts = len(poly)
    normals = []
    for i in range(npts):
        a, b = poly[i], poly[(i + 1) % npts]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        normals.append((dy / length, -dx / length))
    out = []
    for i in range(npts):
        n1, n2 = normals[i - 1], normals[i]
        v = poly[i]
        det = n1[0] * n2[1] - n1[1] * n2[0]
        if abs(det) < 1e-6:
            out.append((v[0] + n2[0] * d, v[1] + n2[1] * d))
            continue
        c1 = v[0] * n1[0] + v[1] * n1[1] + d
        c2 = v[0] * n2[0] + v[1] * n2[1] + d
        out.append(((c1 * n2[1] - c2 * n1[1]) / det, (c2 * n1[0] - c1 * n2[0]) / det))
    return out


# The building's own axes: U runs along Brannan from the south corner toward the
# 3rd/Brannan corner, W runs along 3rd from that corner toward the north corner.
# Every roof object is laid out in this frame so the composition follows the
# building rather than true north. u spans +-11.58, w spans +-10.67.
def _axes():
    _, _, _, t_brannan, _ = poly_edge(E_BRANNAN)
    _, _, _, t_third, _ = poly_edge(E_THIRD)
    return t_brannan, t_third


U, W = _axes()


def uw(u, w):
    return (U[0] * u + W[0] * w, U[1] * u + W[1] * w)


def uw_rect(u, w, su, sw):
    """Four CCW plan corners of a rectangle in the building frame."""
    return [
        uw(u - su / 2, w - sw / 2),
        uw(u + su / 2, w - sw / 2),
        uw(u + su / 2, w + sw / 2),
        uw(u - su / 2, w + sw / 2),
    ]


def signed_area(poly):
    n = len(poly)
    return sum(
        poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1]
        for i in range(n)
    ) / 2.0


def _seg_cross(p1, p2, p3, p4):
    """True if open segments p1p2 and p3p4 properly intersect."""

    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    d1, d2 = orient(p3, p4, p1), orient(p3, p4, p2)
    d3, d4 = orient(p1, p2, p3), orient(p1, p2, p4)
    return ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0))


# -------------------------------------------------------------- mesh helpers


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


def bevel(obj, width=BEVEL_W, segments=BEVEL_SEG):
    """Miniature-style edge softening on the chunky solids (style bible s.4)."""
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
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def prism(name, poly, z0, z1, mat, mat_caps=None):
    """Closed extrusion of a CCW polygon (walls + both caps)."""
    npts = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces, face_mats = [], []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
        face_mats.append(0)
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    face_mats += [1 if mat_caps else 0] * 2
    mats = [mat, mat_caps] if mat_caps else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def prism_with_hole(name, outer, inner, z0, z1, mat, mat_inner=None):
    """Closed genus-1 extrusion: an outer CCW ring with an inner CCW ring cut
    through it. Both rings must have the same vertex count and matching corner
    order, which is true here (both are rectangles in the building frame). The
    caps are bridged corner to corner, so the result is a genuine hole in a
    closed manifold shell rather than a painted-on rectangle — which is what the
    light well actually is, and what keeps the signed-volume test meaningful."""
    npts = len(outer)
    assert len(inner) == npts
    # A bridged annulus is only simple if the corner-to-corner spokes never
    # cross. Cheap to assert, expensive to discover in a render.
    for i in range(npts):
        j = (i + 1) % npts
        assert not _seg_cross(outer[i], inner[i], outer[j], inner[j]), (
            f"{name}: annulus spokes {i} and {j} cross — the hole is too far "
            "off-centre for corner-to-corner bridging"
        )
    o0 = [(x, y, z0) for x, y in outer]
    o1 = [(x, y, z1) for x, y in outer]
    i0 = [(x, y, z0) for x, y in inner]
    i1 = [(x, y, z1) for x, y in inner]
    verts = o0 + o1 + i0 + i1
    O0, O1, I0, I1 = 0, npts, 2 * npts, 3 * npts
    faces, face_mats = [], []
    for i in range(npts):
        j = (i + 1) % npts
        # outer skin, outward
        faces.append((O0 + i, O0 + j, O1 + j, O1 + i))
        face_mats.append(0)
    for i in range(npts):
        j = (i + 1) % npts
        # shaft skin, normals point INTO the shaft = outward from the solid
        faces.append((I0 + j, I0 + i, I1 + i, I1 + j))
        face_mats.append(1 if mat_inner else 0)
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((O1 + i, O1 + j, I1 + j, I1 + i))  # top annulus
        face_mats.append(0)
        faces.append((O0 + j, O0 + i, I0 + i, I0 + j))  # bottom annulus
        face_mats.append(0)
    mats = [mat, mat_inner] if mat_inner else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def ring_band(name, z0, z1, off_in, off_out, mat, poly=None):
    """Closed band following a polygon: 4 loops, quads between."""
    base = poly if poly is not None else FOOTPRINT
    lo_in = offset_polygon(base, off_in)
    lo_out = offset_polygon(base, off_out)
    npts = len(lo_in)
    verts = []
    for loop, z in ((lo_in, z0), (lo_out, z0), (lo_out, z1), (lo_in, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * npts, ((k + 1) % 4) * npts
        for i in range(npts):
            j = (i + 1) % npts
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def quad_box(name, corners, z0, z1, mat):
    """Closed box from four CCW plan corners."""
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


def wall_box(name, edge, s0, s1, z0, z1, d_in, d_out, mat):
    """Box hung on a facade: s along the edge from its first vertex, d measured
    along the outward normal (negative = recessed into the wall). s may run past
    either end of the edge — that is how the shopfront band and the raised corner
    parapet wrap the corner without leaving a notch."""
    a, _, _, t, n = poly_edge(edge)

    def p(s, d):
        return (a[0] + t[0] * s + n[0] * d, a[1] + t[1] * s + n[1] * d)

    return quad_box(name, [p(s0, d_in), p(s1, d_in), p(s1, d_out), p(s0, d_out)], z0, z1, mat)


def uw_box(name, u, w, z0, z1, su, sw, mat):
    """Box centred at (u, w) in the building frame, su along U, sw along W."""
    return quad_box(name, uw_rect(u, w, su, sw), z0, z1, mat)


# ------------------------------------------------------------------- the build


def materials():
    mats = {}
    for name, rgb in PALETTE.items():
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        bsdf = m.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.85
        bsdf.inputs["Metallic"].default_value = 0.0
        if name.endswith("_Glow"):
            bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 0.0
        mats[name] = m
    return mats


def punched_window(tag, edge, s0, s1, z0, z1, mats, lit=False):
    """Upper-storey opening: a Toy_trim reveal with a Toy_glass pane set into it.
    Built PROUD of the wall — the shell is a solid prism with no cut openings, so
    anything at negative depth is buried inside it and invisible. The apparent
    recess comes from the reveal standing 0.10 m out in front of the pane (style
    bible s.5: windows are graphical elements before they are literal openings)."""
    wall_box(f"{tag}_reveal", edge, s0, s1, z0, z1, 0.0, 0.10, mats["Toy_trim"])
    wall_box(f"{tag}_glass", edge, s0 + 0.14, s1 - 0.14, z0 + 0.14, z1 - 0.14,
             0.06, 0.14, mats["Toy_glass"])
    if lit:
        # thin shell lifted clear of the pane: coincident faces z-fight, and at
        # 12% day alpha that reads as a triangulated smear.
        wall_box(f"{tag}_glow", edge, s0 + 0.20, s1 - 0.20, z0 + 0.20, z1 - 0.20,
                 0.145, 0.165, mats["Toy_mustard_Glow"])


def shopfront(tag, edge, s0, s1, mats, bays, awnings=()):
    """A run of the black band: recessed glazing under a proud Toy_ink fascia,
    with the continuous night glow that is this building's whole night state."""
    wall_box(f"{tag}_back", edge, s0, s1, 0.0, Z_FASCIA_TOP, 0.0, 0.04, mats["Toy_ink"])
    # The fascia stands proud of everything below it. This is the cue that has to
    # survive at city distance — from the app's downward camera an awning-depth
    # band would otherwise be hidden under the awnings themselves.
    bevel(wall_box(f"{tag}_fascia", edge, s0, s1, Z_SHOP_HEAD + 0.14, Z_FASCIA_TOP,
                   0.0, 0.20, mats["Toy_ink"]), width=0.04)
    wall_box(f"{tag}_glass", edge, s0 + 0.10, s1 - 0.10, Z_SHOP_SILL, Z_SHOP_HEAD,
             0.03, 0.11, mats["Toy_glass"])
    span = s1 - s0
    for k in range(1, bays):
        s = s0 + span * k / bays
        wall_box(f"{tag}_mull{k}", edge, s - 0.07, s + 0.07, Z_SHOP_SILL, Z_SHOP_HEAD,
                 0.10, 0.17, mats["Toy_ink"])
    # One glow panel per bay rather than one continuous strip. At night the bays
    # still read as a ribbon wrapping the corner; by DAY the app draws this layer
    # at ~12% alpha, and a single strip across both faces would veil the entire
    # ground floor pale — which is exactly the dark base this building is for.
    for k in range(bays):
        g0 = s0 + span * k / bays + 0.45
        g1 = s0 + span * (k + 1) / bays - 0.45
        wall_box(f"{tag}_glow{k}", edge, g0, g1, Z_SHOP_SILL + 0.55,
                 Z_SHOP_HEAD - 0.45, 0.115, 0.135, mats["Toy_trim_Glow"])
    for k, (a0, a1) in enumerate(awnings):
        bevel(wall_box(f"{tag}_awn{k}", edge, a0, a1, Z_SHOP_HEAD - 0.06, Z_SHOP_HEAD + 0.14,
                       0.10, 0.60, mats["Toy_ink"]), width=0.04)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    mats = materials()

    stone = mats["Toy_stone"]
    ink = mats["Toy_ink"]
    glass = mats["Toy_glass"]
    glassl = mats["Toy_glassl"]
    trim = mats["Toy_trim"]
    rust = mats["Toy_rust"]
    roofd = mats["Toy_roofd"]
    sky = mats["Toy_sky"]

    # ---- 1. body with the light well cut through it ----------------------- #
    well_outer = uw_rect(WELL_U, WELL_W, WELL_SU, WELL_SW)
    bevel(
        prism_with_hole("body", FOOTPRINT, well_outer, 0.0, H_WALL, stone, mat_inner=ink),
        width=0.12,
    )

    # ---- 2. roof field: a brown annulus around the well -------------------- #
    prism_with_hole(
        "roof_field",
        offset_polygon(FOOTPRINT, -0.30),
        uw_rect(WELL_U, WELL_W, WELL_SU + 0.20, WELL_SW + 0.20),
        H_WALL,
        H_ROOF,
        rust,
        mat_inner=ink,
    )

    # ---- 3. parapets ------------------------------------------------------- #
    bevel(ring_band("parapet", H_WALL, H_PAR, -0.30, 0.0, stone), width=0.05)
    bevel(ring_band("parapet_cap", H_PAR, H_PAR_CAP, -0.38, 0.08, ink), width=0.04)
    # the one silhouette event: the wall steps up over the corner bay. Each run
    # is carried 0.34 m past the corner along its own edge line so the two
    # solids overlap and close the outside corner without a notch.
    # The raised run is deliberately built PROUD of the main coping (d_out 0.10
    # against the coping's 0.08): flush with the wall, the coping band would run
    # across in front of it and read as a shadow gap slung under a floating slab.
    for tag, edge, s0, s1 in (
        ("cor_b", E_BRANNAN, L_BRANNAN - COR_BRANNAN, L_BRANNAN + 0.36),
        ("cor_t", E_THIRD, -0.36, COR_THIRD),
    ):
        bevel(wall_box(f"{tag}", edge, s0, s1, H_WALL, H_COR, -0.40, 0.10, stone), width=0.05)
        bevel(wall_box(f"{tag}_cap", edge, s0 - 0.04, s1 + 0.04, H_COR, H_COR_CAP,
                       -0.48, 0.18, ink), width=0.04)

    # ---- 4. the black band, wrapping the east corner ----------------------- #
    # Brannan: garage door at the SW end, then shopfronts up to and past the
    # corner; 3rd Street picks the band up on the other side of the same corner.
    shopfront("shop_b", E_BRANNAN, 4.10, L_BRANNAN + 0.34, mats, bays=4,
              awnings=((5.20, 11.40), (12.10, 18.30)))
    shopfront("shop_t", E_THIRD, -0.34, L_THIRD - 0.60, mats, bays=3,
              awnings=((1.10, 7.30), (8.00, 14.20)))
    # the roll-up garage door at the Brannan (south-west) end
    wall_box("garage_back", E_BRANNAN, 0.60, 3.90, 0.0, Z_FASCIA_TOP, 0.0, 0.04, ink)
    wall_box("garage_door", E_BRANNAN, 0.80, 3.70, 0.05, 3.05, 0.03, 0.13, roofd)
    for k, z in enumerate((1.05, 2.05)):
        wall_box(f"garage_rib{k}", E_BRANNAN, 0.80, 3.70, z - 0.04, z + 0.04,
                 0.12, 0.16, ink)
    # two recessed entries, one per street face
    for tag, edge, s in (("ent_b", E_BRANNAN, 15.60), ("ent_t", E_THIRD, 9.90)):
        wall_box(f"{tag}_door", edge, s, s + 1.30, 0.0, 2.60, 0.02, 0.09, glass)
        bevel(wall_box(f"{tag}_jamb0", edge, s - 0.16, s, 0.0, 2.80, 0.02, 0.18, ink),
              width=0.04)
        bevel(wall_box(f"{tag}_jamb1", edge, s + 1.30, s + 1.46, 0.0, 2.80, 0.02, 0.18, ink),
              width=0.04)

    # ---- 5. 3rd Street elevation (NE, 21.28 m) — the address face ---------- #
    # Three big sparse squares. s runs from the east corner toward the north
    # corner, so the CAFE BUENOS AIRES panel at the north-west end is at high s.
    for k, s0 in enumerate((3.60, 9.00, 14.40)):
        punched_window(f"t_win{k}", E_THIRD, s0, s0 + 2.00, 5.30, 6.90, mats,
                       lit=(k == 1))
    # the blue cafe panel set into the fascia — the one saturated element
    # applied ON the fascia, which itself stands 0.20 m proud — at 0.13 the panel
    # would be buried inside the band it is supposed to be screwed to.
    wall_box("cafe_panel", E_THIRD, 17.50, 19.40, Z_SHOP_HEAD + 0.26, Z_FASCIA_TOP - 0.08,
             0.18, 0.28, sky)
    wall_box("cafe_glow", E_THIRD, 17.60, 19.30, Z_SHOP_HEAD + 0.34, Z_FASCIA_TOP - 0.16,
             0.285, 0.305, mats["Toy_sky_Glow"])
    # the blank white blade sign near the north-west end
    bevel(wall_box("blade", E_THIRD, 19.90, 20.80, 4.90, 7.10, 0.05, 0.22, trim), width=0.05)

    # ---- 6. Brannan Street elevation (SE, 23.10 m) — the long face --------- #
    # Seven tall punched windows on a 2.95 m pitch, AC boxes under four of them.
    for k in range(7):
        s0 = 1.55 + k * 2.95
        punched_window(f"b_win{k}", E_BRANNAN, s0, s0 + 1.10, 5.00, 6.90, mats,
                       lit=(k == 3))
        if k in (1, 2, 4, 5):
            bevel(wall_box(f"b_ac{k}", E_BRANNAN, s0 + 0.25, s0 + 0.85, 4.45, 4.85,
                           0.05, 0.30, roofd), width=0.05)

    # ---- 7. the working roof ---------------------------------------------- #
    # Five skylights and three plant boxes, loosely scattered rather than
    # gridded — the reading is "a working roof", not a census. Nothing here
    # competes with 599 Third's genuinely inhabited roof across the street.
    for k, (u, w) in enumerate(((-8.2, -6.0), (-2.5, -6.6), (3.5, -3.8), (6.6, 3.2),
                                (0.5, 6.4), (-6.0, 4.6), (9.0, -6.4))):
        bevel(uw_box(f"sky_{k}_frame", u, w, H_ROOF, H_ROOF + 0.22, 1.35, 1.05, trim),
              width=0.05)
        uw_box(f"sky_{k}_pane", u, w, H_ROOF + 0.19, H_ROOF + 0.31, 1.05, 0.75, glassl)
    for k, (u, w) in enumerate(((-9.2, 5.4), (2.0, -8.2), (8.2, -1.2), (4.4, 7.4))):
        bevel(uw_box(f"plant_{k}", u, w, H_ROOF, H_ROOF + 0.52, 0.85, 0.65, roofd),
              width=0.06)
    # the roof hatch / stair head, the only raised box up here. Its coping is four
    # thin bars around the top edge, NOT a lid: a full-plan cap box reads from
    # directly above as a black hole punched in the roof (599 Third learned this).
    bevel(uw_box("stairhead", -7.2, -1.4, H_ROOF, H_ROOF + 1.00, 2.40, 1.80, stone),
          width=0.08)
    for k, (du, dw, su, sw) in enumerate(((0, -0.94, 2.56, 0.16), (0, 0.94, 2.56, 0.16),
                                          (-1.24, 0, 0.16, 1.72), (1.24, 0, 0.16, 1.72))):
        bevel(uw_box(f"stairhead_cope{k}", -7.2 + du, -1.4 + dw, H_ROOF + 0.88,
                     H_ROOF + 1.02, su, sw, ink), width=0.04)

    return scene


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
        o.evaluated_get(dg).to_mesh_clear()
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] footprint area={abs(signed_area(FOOTPRINT)):.1f} m2")
    print("[build] anchor lon/lat: -122.3946749 37.7800837 (parcel centroid)")
    print("[build] 3rd Street front normal 45.2 deg true; Brannan front 135.1 deg true")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "590-third.blend")
    glb = os.path.join(out, "590-third.glb")
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
