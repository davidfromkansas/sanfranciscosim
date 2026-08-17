"""Deterministic Blender build of the SF-SIM miniature 126 South Park.

    blender -b --python build_126_south_park.py -- [--out DIR]

Writes 126-south-park.blend and 126-south-park.glb next to this file (or into
--out). Geometry is authored directly in world space in metres, Z up, +X east,
+Y north, so the model drops into the city at its real-world heading — the
loader applies no rotation. Origin = footprint area centroid (anchor
lon -122.3945863, lat 37.7816006), min Z = 0, front eave crest exactly 7.6 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured OSM footprint (way/124884348): a 6.90 m frontage on South Park
  running back 29.79 m, 45 deg off the world axes like the whole SoMa grid.
  Party walls down BOTH long flanks, 0.6 m from 112 South Park to the north-east
  and from 130/134 to the south-west;
* the identity feature, and the reason this asset exists: the WAIST. Two light
  wells cut in from opposite sides — 1.65 m deep from the north-east, 1.28 m
  from the south-west — overlap for 1.99 m about ten metres back from the street
  and squeeze the plan to 4.01 m. A third, shallower well (0.84 m) bites the
  south-west flank again near the rear. All three are true full-height voids;
  they come free with the polygon and must never be filled. They are what the
  leasing copy means by "3 sides of window line, plus an atrium garden", and
  they are the silhouette the app's downward camera reads first;
* a two-storey wood-frame box: Toy_steel gray siding on all elevations, the
  palette's nearest true neutral to the measured #8e9791 of the real paint.
  Toy_verdigris is closer in hue but saturated enough that a whole building of
  it reads as an accent, which the style bible s.7 reserves for identity — and
  here the identity is the plan shape, not the colour;
* the front's one piece of ornament: a projecting shed EAVE on exposed rafter
  tails, sloping down and out from the 7.6 m crest at the wall to 7.10 m at the
  fascia. It sets the bounding-box top;
* the party walls carry NO openings. Only the front, the rear and the three
  well faces can, which is exactly why the wells exist;
* night state: the wells are the hero glow — thin shells at the head of each
  slot, so from the app's aerial camera the building reads as a long dark plank
  with a bright notch burning across its middle: the night statement of the same
  cue that carries the day. Plus the two skylights and two lit front windows.
  Glow surfaces are thin shells proud of the opaque surfaces (the app renders
  _Glow in a separate layer that is ~12% alpha by day — never author a primary
  surface as glow);
* the roof is deliberately sparse: two skylights, a hatch, a vent cowl, all
  below the 7.6 m crest, and NO mechanical plant. The LiDAR (sigma 0.64 m over
  715 cells, mode and median both 7.32 m) is what a clean roof measures, and
  nothing in the evidence supports plant. See the plan's 2.7 step 10.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way/124884348 projected with the app's tangent projection and recentred on
# the polygon's area centroid. CCW, +X east, +Y north.
FOOTPRINT = [
    (-6.579, 1.521),     # 0
    (-5.980, 2.107),     # 1
    (-3.261, -0.602),    # 2
    (-3.851, -1.187),    # 3
    (-1.352, -3.675),    # 4
    (-0.419, -2.757),    # 5
    (2.045, -5.222),     # 6
    (1.165, -6.095),     # 7
    (8.143, -13.059),    # 8  front / south-west corner
    (13.053, -8.207),    # 9  front / north-east corner
    (6.348, -1.508),     # 10
    (5.169, -2.669),     # 11
    (3.488, -0.999),     # 12
    (4.667, 0.172),      # 13
    (-8.004, 12.807),    # 14 rear / north-east corner
    (-12.976, 7.899),    # 15 rear / south-west corner
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_FRONT = 8      # 6.90 m, faces SE 135.3 deg — South Park. u=0 at the SW end.
EDGE_REAR = 14      # 6.99 m, faces NW 315.4 deg — the mid-block yard
EDGE_PARTY_NE_F = 9    # 9.48 m,  NE 45.0 — party wall with 112, front run
EDGE_PARTY_NE_R = 13   # 17.89 m, NE 44.9 — party wall with 112, rear run
EDGE_PARTY_SW_F = 7    # 9.86 m,  SW 224.9 — party wall with 130/134, front run
EDGE_PARTY_SW_M = 3    # 3.53 m,  SW 224.9 — party wall with 130/134, middle run
EDGE_PARTY_SW_R = 15   # 9.03 m,  SW 224.9 — party wall with 130/134, rear run

# The three light wells: (back edge, front cheek, rear cheek, depth).
WELL_NE = (11, 10, 12, 1.66)    # back 2.37 m long, cut 1.65 m in from the NE
WELL_SW1 = (5, 6, 4, 1.28)      # back 3.49 m long, cut ~1.28 m in from the SW
WELL_SW2 = (1, 2, 0, 0.84)      # back 3.84 m long, cut 0.84 m in from the SW
WELLS = (WELL_NE, WELL_SW1, WELL_SW2)

Z_DECK = 7.32        # flat roof deck — DataSF LiDAR mode AND median, sigma 0.64 m
Z_UPSTAND = 7.52     # low roof upstand ring
Z_CREST = 7.60       # front eave crest at the wall = the bbox top (inferred, +0.28)
Z_EAVE_FASCIA = 7.10 # eave outer edge — the hood sheds down and out to the street
Z_BELT = 3.60        # belt course between the storeys
Z_GROUND_HEAD = 3.00 # ground-floor window head
Z_WIN0, Z_WIN1 = 4.50, 6.30   # upper-floor window band
Z_FRIEZE = 6.70      # frieze band under the eave

EAVE_OUT = 1.00      # eave projection over the sidewalk
SKIN = 0.0           # no applied front skin: one siding material everywhere
LINING = 0.10        # light-well lining proud of the structural face

PALETTE_HEX = {
    # Toy_steel for the siding: the palette's nearest true neutral to the
    # measured #8e9791 of the real paint. See the module docstring.
    "Toy_steel": "9aa0a6",
    "Toy_stone": "d9d2c2",
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_roofd": "45454a",
    "Toy_ink": "3a3530",
    "Toy_glass_Glow": "6f95b8",
    "Toy_glassl_Glow": "6f95b8",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def poly_edge(i):
    """Edge i of FOOTPRINT: (origin, length, tangent unit, outward normal)."""
    a = FOOTPRINT[i]
    b = FOOTPRINT[(i + 1) % len(FOOTPRINT)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def offset_polygon(poly, d):
    """Miter offset of the CCW footprint; positive d moves outward.

    Solved as the intersection of the two offset edge lines at each vertex, so
    it stays correct at the six reflex corners the three light wells introduce —
    a naive normal-averaging offset folds the upstand ring inside out there.
    """
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


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


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


def bevel(obj, width=0.12, segments=2):
    """Miniature-style edge softening on the chunky solids (style bible s.4).

    Width is capped at a third of the object's thinnest dimension: the applied
    window panels here are 60-160 mm thick and a flat 0.12 m bevel on those
    relies entirely on clamp_overlap, which collapses opposing profiles into
    zero-area slivers. The remove_doubles/dissolve_degenerate pass sweeps up
    whatever clamping still pinches shut.
    """
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


def prism(name, poly, z0, z1, mat, mat_caps=None):
    """Closed extrusion of a CCW polygon (walls + both caps).

    The caps are concave 16-gons here; Blender tessellates them correctly on
    export, which the validator re-checks by signed volume on the re-import.
    """
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


def ring_band(name, poly, z0, z1, off_in, off_out, mat):
    """Closed band following a footprint: 4 loops, quads between."""
    lo_in = offset_polygon(poly, off_in)
    lo_out = offset_polygon(poly, off_out)
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


def face_panel(name, edge, u_centre, profile, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in the plane of wall `edge`,
    extruded outward from offset d0 to d1 along that wall's normal."""
    a, _length, t, n = poly_edge(edge)
    verts = []
    for d in (d0, d1):
        for du, z in profile:
            px = a[0] + t[0] * (u_centre + du) + n[0] * d
            py = a[1] + t[1] * (u_centre + du) + n[1] * d
            verts.append((px, py, z))
    npts = len(profile)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


BOX_FACES = [
    (3, 2, 1, 0),
    (4, 5, 6, 7),
    (0, 1, 5, 4),
    (1, 2, 6, 5),
    (2, 3, 7, 6),
    (3, 0, 4, 7),
]


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0):
    """Box with local +x along yaw and local +y 90 deg ccw of it."""
    c, s = math.cos(yaw), math.sin(yaw)
    corners = []
    for lx, ly in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)):
        corners.append((cx + lx * c - ly * s, cy + lx * s + ly * c))
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    return new_mesh(name, verts, BOX_FACES, [mat])


def wedge(name, edge, u0, u1, d_in, d_out, z_in_lo, z_in_hi, z_out_lo, z_out_hi, mat):
    """Sloped slab in the frame of wall `edge`: a box whose inner and outer ends
    sit at different heights. Used for the eave hood and its rafter tails, which
    slope down and out toward the street."""
    a, _length, t, n = poly_edge(edge)

    def pt(u, d, z):
        return (a[0] + t[0] * u + n[0] * d, a[1] + t[1] * u + n[1] * d, z)

    verts = [
        pt(u0, d_in, z_in_lo),
        pt(u0, d_out, z_out_lo),
        pt(u1, d_out, z_out_lo),
        pt(u1, d_in, z_in_lo),
        pt(u0, d_in, z_in_hi),
        pt(u0, d_out, z_out_hi),
        pt(u1, d_out, z_out_hi),
        pt(u1, d_in, z_in_hi),
    ]
    return new_mesh(name, verts, BOX_FACES, [mat])


def cylinder(name, cx, cy, z0, z1, radius, mat, seg=10):
    """Low-segment cylinder (style bible s.4: 8-14 segments)."""
    ring = [
        (cx + radius * math.cos(2 * math.pi * k / seg), cy + radius * math.sin(2 * math.pi * k / seg))
        for k in range(seg)
    ]
    return prism(name, ring, z0, z1, mat)


# Building-local frame: u runs along the north-east party wall from the FRONT
# corner (vertex 9) back towards the rear, v runs into the block away from that
# wall. Every roof position below is expressed in it, so the roof composition is
# described relative to the building rather than to the world axes.
_PA, _PL, _PT, _PN = poly_edge(EDGE_PARTY_NE_F)


def uv_to_world(u, v):
    return (_PA[0] + _PT[0] * u - _PN[0] * v, _PA[1] + _PT[1] * u - _PN[1] * v)


def roof_box(name, u, v, z0, z1, su, sv, mat):
    cx, cy = uv_to_world(u, v)
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=math.atan2(_PT[1], _PT[0]))


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
        # Flagged for the app's night pass; emission is off in the day asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------------- parts


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None, base=0.0):
    """Frame panel + a smaller fill that protrudes further, so the frame reads
    as a border ring around a recessed opening. No booleans, all closed solids.

    `base` lifts the whole assembly outward, which is how the openings inside
    the light wells sit proud of their Toy_stone linings rather than sunk behind
    them."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), base, base + 0.06, frame_mat)
    inset = 0.16
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        base,
        base + 0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = 0.28
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            base + 0.10,
            base + 0.17,
            glow_mat,
        )


def light_well(tag, spec, stone, trim, glass, gglow):
    """Line a well's three faces in Toy_stone, glaze it, and band its head in
    glow. The lining is the point: a light well only reads as a void from above
    if its inner faces are brighter than the deck and the outer walls, and this
    building's whole identity is those voids."""
    back, cheek_a, cheek_b, _depth = spec
    _a, back_len, _t, _n = poly_edge(back)

    face_panel(
        f"{tag}_lining", back, back_len / 2.0, rect_profile(back_len - 0.02, 0.0, Z_DECK),
        0.0, LINING, stone,
    )
    for side, edge in (("a", cheek_a), ("b", cheek_b)):
        _ca, clen, _ct, _cn = poly_edge(edge)
        face_panel(
            f"{tag}_cheek_{side}", edge, clen / 2.0, rect_profile(clen - 0.02, 0.0, Z_DECK),
            0.0, LINING, stone,
        )

    # Glazing on the well back: as many columns as the back will take, two
    # storeys high. This is the "3 sides of window line" the leasing copy sells.
    cols = max(1, int(back_len // 1.6))
    for k in range(cols):
        u = back_len * (k + 0.5) / cols
        rect_opening(f"{tag}_g{k}", back, u, 0.9, 1.10, 2.50, trim, glass, base=LINING)
        rect_opening(f"{tag}_u{k}", back, u, 0.9, 4.60, 5.90, trim, glass, base=LINING)

    # Night: a thin glow band around the head of the slot, proud of the lining.
    # The app's camera looks DOWN at 30-50 deg, so what reads at night is the
    # top of the well, not the windows 5 m below it.
    for edge in (back, cheek_a, cheek_b):
        _ea, elen, _et, _en = poly_edge(edge)
        face_panel(
            f"{tag}_glow_{edge}", edge, elen / 2.0,
            rect_profile(elen - 0.10, 6.35, 7.05),
            LINING + 0.02, LINING + 0.09, gglow,
        )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    siding = material("Toy_steel")
    stone = material("Toy_stone")
    trim = material("Toy_trim")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    ink = material("Toy_ink")
    gglow = material("Toy_glass_Glow")
    sglow = material("Toy_glassl_Glow")

    # --- body: the sliver, its top cap IS the pale cool roof deck ------------
    # All three light wells come free with the polygon. Do not fill them.
    #
    # The deck is Toy_stone, not the dark Toy_roofd this set usually reaches for.
    # That is evidence, not taste: the 2023-08-28 re-roofing permit covers the
    # whole ~2,100 sq ft roof, which puts it over Title 24 Part 6 s.141.0(b)2Bi's
    # "more than 50 percent or 2,000 square feet, whichever is less" trigger, and
    # that section requires a low-slope nonresidential re-roof to hit an aged
    # solar reflectance of 0.63 in EVERY California climate zone. A 0.63-SR
    # membrane is a pale roof. (135 South Park one block away is dark because an
    # aerial was actually read for it; here the aerial is unusable and the code
    # is the better source.)
    prism("body", FOOTPRINT, 0.0, Z_DECK, siding, mat_caps=stone)

    # --- low upstand ring around the deck -----------------------------------
    ring_band("upstand", FOOTPRINT, Z_DECK, Z_UPSTAND, -0.25, 0.02, siding)

    # --- the three light wells: this asset's whole identity ------------------
    # Lined DARK against the pale deck. The first aerial review had this the
    # other way round — pale linings in a dark deck — and the wells read as
    # raised bright blocks rather than as holes, which inverted the one cue the
    # asset exists to carry. From above, a void is a dark slot. (Logged in
    # REPORT.md as revision 2.)
    for tag, spec in (("wne", WELL_NE), ("wsw1", WELL_SW1), ("wsw2", WELL_SW2)):
        light_well(tag, spec, roofd, trim, glass, gglow)

    # --- South Park front (SE), 6.90 m. u=0 at the south-west end -----------
    # Ground floor: gated entrance bay on the SW third, two tall windows on the
    # NE two thirds. Straight off the Sept 2025 photograph — this is the one
    # elevation in this dossier that is observed rather than inferred.
    # Frame outermost-but-shallowest, dark gate panel proud of it — the same
    # layering rect_opening uses. Built the other way round first and the trim
    # frame simply covered the gate, which rendered the entrance as a blank white
    # slab (revision 2).
    face_panel("fr_gate_frame", EDGE_FRONT, 1.35, rect_profile(2.40, 0.0, 2.90), 0.0, SKIN + 0.06, trim)
    face_panel("fr_gate_reveal", EDGE_FRONT, 1.35, rect_profile(2.22, 0.0, 2.75), 0.0, SKIN + 0.10, ink)
    face_panel("fr_gate_panel", EDGE_FRONT, 1.35, rect_profile(2.06, 0.0, 2.62), 0.0, SKIN + 0.14, roofd)
    for k, u in enumerate((3.75, 5.60)):
        rect_opening(f"fr_gw{k}", EDGE_FRONT, u, 1.55, 1.00, Z_GROUND_HEAD, trim, glass,
                     gglow if k == 0 else None)

    # Belt course, then three shallow siding bands implying the board rhythm,
    # then the frieze under the eave. Front only — the party walls are blank.
    face_panel("fr_belt", EDGE_FRONT, 3.45, rect_profile(6.80, Z_BELT, Z_BELT + 0.25), 0.0, SKIN + 0.18, trim)
    for k, z in enumerate((4.05, 5.05, 6.05)):
        face_panel(f"fr_band{k}", EDGE_FRONT, 3.45, rect_profile(6.80, z, z + 0.06), 0.0, SKIN + 0.04, siding)
    face_panel("fr_frieze", EDGE_FRONT, 3.45, rect_profile(6.80, Z_FRIEZE, Z_FRIEZE + 0.35), 0.0, SKIN + 0.10, trim)

    # Upper floor: the two-part window group set toward the north-east, in one
    # shared surround, plus the narrow opening at the south-west edge.
    face_panel("fr_upsurround", EDGE_FRONT, 4.65, rect_profile(3.40, Z_WIN0 - 0.18, Z_WIN1 + 0.18),
               0.0, SKIN + 0.08, trim)
    for k, u in enumerate((3.80, 5.50)):
        rect_opening(f"fr_up{k}", EDGE_FRONT, u, 1.30, Z_WIN0, Z_WIN1, trim, glass,
                     gglow if k == 1 else None, base=SKIN + 0.05)
    rect_opening("fr_upsw", EDGE_FRONT, 1.10, 0.70, Z_WIN0 + 0.20, Z_WIN1, trim, glass)

    # --- the front eave: the building's one ornament, and the bbox top -------
    # A shed hood sloping down and out from Z_CREST at the wall to the fascia,
    # on five exposed rafter tails. Kept flush with the 6.90 m frontage: an
    # overhang would poke into 112 and 130/134, whose walls are 0.6 m away.
    # Top face in the siding gray, not the deck colour: the photograph shows the
    # hood painted with the rest of the front, and a dark slab there fought the
    # pale cool roof behind it for attention (revision 2).
    wedge("eave", EDGE_FRONT, 0.05, 6.85, -0.10, EAVE_OUT,
          7.20, Z_CREST, Z_EAVE_FASCIA - 0.22, Z_EAVE_FASCIA, siding)
    wedge("eave_fascia", EDGE_FRONT, 0.05, 6.85, EAVE_OUT - 0.02, EAVE_OUT + 0.09,
          Z_EAVE_FASCIA - 0.24, Z_EAVE_FASCIA + 0.01, Z_EAVE_FASCIA - 0.24, Z_EAVE_FASCIA + 0.01, trim)
    for k in range(5):
        u = 0.55 + k * 1.45
        wedge(f"eave_rafter{k}", EDGE_FRONT, u - 0.06, u + 0.06, 0.10, EAVE_OUT - 0.04,
              7.02, 7.20, Z_EAVE_FASCIA - 0.38, Z_EAVE_FASCIA - 0.20, ink)

    # --- rear (NW), 6.99 m onto the mid-block yard: service elevation --------
    # Inferred — no photograph of this side was located. Kept plain on purpose.
    rect_opening("re_door", EDGE_REAR, 1.80, 1.10, 0.0, 2.30, trim, roofd)
    for k, u in enumerate((3.60, 5.30)):
        rect_opening(f"re_up{k}", EDGE_REAR, u, 0.90, 4.70, 5.80, trim, glass)

    # --- PARTY WALLS: deliberately blank -------------------------------------
    # 27.37 m against 112 South Park to the north-east and 22.42 m against
    # 130/134 to the south-west, both at a 0.6 m gap. A party wall cannot carry
    # openings; that is the whole reason the light wells exist. Do not add
    # windows to edges 7, 3, 15, 9 or 13.

    # --- roof: sparse by design (see the plan's 2.7 step 10) -----------------
    # u measured back from the front corner along the NE party wall, v across.
    for k, (u, v) in enumerate(((17.0, 3.4), (24.0, 3.4))):
        roof_box(f"skylight{k}_kerb", u, v, Z_DECK, Z_DECK + 0.08, 1.72, 1.32, trim)
        roof_box(f"skylight{k}_glaze", u, v, Z_DECK + 0.08, Z_DECK + 0.22, 1.60, 1.20, glassl)
        # One flat shell just proud of the glazing cap, not a pair of side bars:
        # the bars lit the skylight's flanks and read at night as two white
        # dashes rather than as a lit rooflight (revision 2).
        roof_box(f"skylight{k}_glow", u, v, Z_DECK + 0.22, Z_DECK + 0.25, 1.48, 1.08, sglow)
    roof_box("roof_hatch", 21.0, 4.6, Z_DECK, Z_DECK + 0.20, 1.00, 0.90, roofd)
    cx, cy = uv_to_world(6.5, 2.2)   # forward half, so the deck reads balanced
    cylinder("vent_cowl", cx, cy, Z_DECK, Z_DECK + 0.22, 0.30, ink)

    # Bevel budget: the chunky masses carry the miniature read and get the full
    # 0.12/2. The many small applied panels get a token 1-segment softening on
    # their frames and none at all on fills and glow shells, which is what keeps
    # this under the 7,000-triangle cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if "_glow" in obj.name or obj.name.endswith(("_fill", "_band0", "_band1", "_band2")):
            continue
        if obj.name.endswith(("_frame", "_panel", "_reveal", "_lining")) or "_cheek_" in obj.name:
            bevel(obj, width=0.05, segments=1)
        else:
            bevel(obj, width=0.12, segments=2)

    normalize()
    return scene


def normalize():
    """Land min Z on 0 and the bbox top on Z_CREST exactly (pipeline stage 2:
    "normalize the bbox top to the verified height exactly", so the loader's
    targetHeightM / measuredHeight scale is 1.0).

    A pass is needed rather than just authoring the eave at Z_CREST because this
    building's highest point is an EDGE, not a face: the hood's crest is the
    crease where its sloping top meets the wall, and the 0.12 m bevel that gives
    every other solid its miniature softness rounds that crease off by ~42 mm.
    Flat-topped landmarks (135 South Park's roof monitor, say) do not hit this —
    a bevel leaves the interior of a flat top face untouched.

    The correction is applied as a Z-only scale about z=0, so the measured
    footprint in XY is left bit-exact and only vertical dimensions move, by
    ~0.6% — 4 cm on the building's height, under 2 cm on any storey. Doing it
    here rather than by hand-tuning the eave upward keeps the script correct if
    the massing is ever revised.
    """
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    lo = min(v.co.z for o in objs for v in o.data.vertices)
    for o in objs:
        for v in o.data.vertices:
            v.co.z -= lo
    hi = max(v.co.z for o in objs for v in o.data.vertices)
    k = Z_CREST / hi
    for o in objs:
        for v in o.data.vertices:
            v.co.z *= k
        o.data.update()
    print(f"[build] normalize: min_z {lo:+.4f} -> 0, crest {hi:.4f} -> {Z_CREST} (z x {k:.6f})")


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
    print("[build] anchor lon/lat: -122.3945863 37.7816006 (footprint area centroid)")
    print("[build] South Park front heading: 135.3 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "126-south-park.blend")
    glb = os.path.join(out, "126-south-park.glb")
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
