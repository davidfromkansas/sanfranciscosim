"""Deterministic Blender build of the SF-SIM miniature 521 Third Street.

    blender -b --python build_521_third.py -- [--out DIR]

Writes 521-third.blend and 521-third.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = parcel oriented-bbox centre (anchor lon -122.3952384,
lat 37.7811509), min Z = 0, parapet crest exactly 11.40 m.

Design (see REFERENCE.md for the sources behind every number):

* the SURVEYED PARCEL rhombus (DataSF `acdm-wktn` blklot 3775072), not the LiDAR
  footprint: the LiDAR ring overhangs the 3rd Street property line by ~0.5 m
  (that is the cornice, seen from above) and stops ~1.1 m short at the rear, and
  it carries a 5.2 m jog across the 3rd/Taber corner that is the awning and the
  projecting blade sign, not a chamfer. The parcel's 23.13 m depth matches the
  assessor's 76.0 ft lot depth to 3 cm and the building covers 94 % of the lot;

* a 1914 three-storey unreinforced-masonry apartment-over-store block holding the
  EAST corner of 3rd Street and Taber Place. Two designed elevations — the 14.64 m
  3rd Street front and the 23.10 m Taber Place flank — a blind SE party wall and
  an inferred rear;

* the identity features are HORIZONTAL: a cream cornice over a dentil course and
  a corbelled brick band at the top, and a cream Greek-key belt band at the
  storefront head, both turning the 3rd/Taber corner. That pair of bright lines
  on a dark red box is the whole graphic read at city scale. The corner itself is
  a SHARP 90 deg arris — the curve visible in every equirectangular panorama is
  projection distortion (plan 2.15 risk 1);

* it is the LOW, ornamented one — 11.40 m against 501 Third's 13.72 m across
  Taber Place and 549 Third's 13.03 m on the party wall. Getting it lower and
  fussier than what flanks it is most of the job;

* the one saturated note is Neill's ORANGE awning at the corner, balanced by the
  black SouthBeach fascia and its steel roll-up shutter on the other half;

* night state: the two shopfronts and the projecting blade sign carry the whole
  composition, plus four of the ten upper-floor windows. The Taber flank stays
  dark. Glow shells are thin and proud of the opaque glazing — the app renders
  _Glow in a separate layer that is ~12 % alpha by day, and a CLOSED glow shell
  is two such layers (~23 %) and would tint the facade;

* a genuinely designed roof: a white membrane deck inside a parapet ring, the
  roof-edge hoist davit frame and ladder that the LiDAR maximum of 13.53 m is
  actually measuring, a stair hatch and four vents. The davits are modelled
  co-terminal with the parapet crest rather than proud of it, so the parapet
  stays the 11.40 m datum the manifest quotes (REPORT.md records the call).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF surveyed parcel 3775072, projected with the app's tangent projection and
# recentred on the parcel oriented-bbox centre. CCW.
FOOTPRINT = [
    (-3.032, -13.320),   # S — 3rd Street / SE party wall
    (13.368, 2.960),     # E — SE party wall / rear
    (2.998, 13.350),     # N — rear / Taber Place
    (-13.372, -2.950),   # W — 3rd Street / Taber Place, the hero corner
]

# Edge index -> elevation. Outward normals verified against the survey.
EDGE_PARTY = 0   # 23.11 m, faces SE 135.2 deg — blind party wall (549 Third)
EDGE_REAR = 1    # 14.68 m, faces NE  45.1 deg — rear, block interior
EDGE_TABER = 2   # 23.10 m, faces NW 315.1 deg — Taber Place flank
EDGE_THIRD = 3   # 14.64 m, faces SW 225.1 deg — 3rd Street front

L_THIRD = 14.64
L_TABER = 23.10

Z_DECK = 10.90       # roof deck (LiDAR mode 10.87, median 10.95)
Z_CREST = 11.40      # parapet crest -> the bbox top and the loader's scale
PARAPET_T = 0.30     # parapet wall thickness

Z_CORBEL0, Z_CORBEL1 = 9.75, 10.00   # corbelled dogtooth brick band
Z_DENT0, Z_DENT1 = 10.00, 10.25      # dentil course
Z_CORN0, Z_CORN1 = 10.25, 11.00      # the cream cornice fascia
Z_PLIP0, Z_PLIP1 = 11.00, 11.40      # brick parapet face above the cornice

Z_BAND0, Z_BAND1 = 3.55, 3.95        # cream Greek-key belt band (storefront head)
Z_STORE = 3.50                       # top of the shopfront field
Z_W2_0, Z_W2_1 = 4.55, 6.10          # 2nd-floor punched windows
Z_W3_0, Z_W3_1 = 7.65, 9.20          # 3rd-floor punched windows
Z_FLOOR2, Z_FLOOR3 = 4.35, 7.45      # fire-escape balcony levels

D_CORBEL = 0.10
D_DENT = 0.24
D_CORN = 0.50
D_PLIP = 0.06
D_BAND = 0.18
TABER_RETURN = 6.2   # how far the cornice group runs into Taber before stopping

# 3rd Street bay centres, u measured from the Taber (west) corner.
# Bay 1 window, bay 2 the FIRE-ESCAPE DOOR, bays 3-5 windows. The rhythm is
# deliberately uneven: bays 1-2 are the widest gap on the real facade.
THIRD_BAYS = (1.55, 4.80, 7.50, 10.55, 13.10)
BAY_FIRE = 1         # index of the fire-escape door bay
WIN_W = 1.20

PALETTE_HEX = {
    "Toy_oxblood": "7a4034",       # brick body — the dark red-brown of 1914 stock.
                                   # Toy_rust and Toy_brick both render salmon at
                                   # the app's exposure and lost the value contrast
                                   # against the cream bands (REPORT.md iteration 1)
    "Toy_rust": "a86444",          # spare warm brick note
    "Toy_cocoa": "6b4a3d",         # recessed basketweave panels — a recessed panel
                                   # reads DARKER than its wall; Toy_rust made them
                                   # look like blocked-up windows (REPORT.md it. 2)
    "Toy_cream": "f2ede3",         # cornice, dentils, Greek-key band, window trim
    "Toy_greige": "b0aa9e",        # roof membrane + the meander's shadow ticks
    "Toy_p_tan": "d8a878",         # Taber Place stucco base. Toy_peach (e8cdc9)
                                   # was tried first and is so close to Toy_cream
                                   # that the Greek-key band vanished into it
                                   # (REPORT.md iteration 2)
    "Toy_cobalt": "2f5fb0",        # mural
    "Toy_mint": "8fd0a8",          # mural
    "Toy_glass": "2a4d73",
    "Toy_ink": "3a3530",           # sashes, fire escapes, black fascia, entry
    "Toy_orange": "d4622a",        # Neill's awning + blade sign
    "Toy_mustard": "d9a441",       # the 527 apartments entry awning
    "Toy_steel": "9aa0a6",         # roll-up shutter, davits, ladder, vents
    "Toy_orange_Glow": "d4622a",
    "Toy_glass_Glow": "6f95b8",
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
    """Miter offset of the convex CCW footprint; positive d moves outward."""
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


def point_inset_ok(px, py, inset):
    """True when (px,py) is at least `inset` inside every footprint edge."""
    for i in range(len(FOOTPRINT)):
        a, _l, _t, n = poly_edge(i)
        if (px - a[0]) * n[0] + (py - a[1]) * n[1] > -inset:
            return False
    return True


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
    """Miniature-style edge softening (style bible s.4). Width is capped at a
    third of the object's thinnest dimension: the applied bands here are only
    40-400 mm thick and a flat 0.12 m bevel collapses opposing profiles into
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


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0):
    """Box with local +x along yaw and local +y 90 deg ccw of it."""
    c, s = math.cos(yaw), math.sin(yaw)
    corners = []
    for lx, ly in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)):
        corners.append((cx + lx * c - ly * s, cy + lx * s + ly * c))
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


def wall_box(name, edge, u, z0, z1, w, depth, mat, d0=0.0):
    """Small box hung on a wall, sized in (along-wall, outward) metres."""
    a, _l, t, n = poly_edge(edge)
    cx = a[0] + t[0] * u + n[0] * (d0 + depth / 2.0)
    cy = a[1] + t[1] * u + n[1] * (d0 + depth / 2.0)
    return box(name, cx, cy, z0, z1, w, depth, mat, yaw=math.atan2(t[1], t[0]))


def wall_wedge(name, edge, u, w, d_out, z_wall, z_edge, mat):
    """A sloped awning: a closed six-face wedge hung on `edge`, springing from
    the wall at z_wall and falling to z_edge at d_out, with a vertical valance
    face of 0.30 m under its outer lip. Modelled as one solid so the union stays
    watertight for the normals test."""
    a, _l, t, n = poly_edge(edge)

    def p(du, d, z):
        return (a[0] + t[0] * (u + du) + n[0] * d, a[1] + t[1] * (u + du) + n[1] * d, z)

    h = w / 2.0
    v = [
        p(-h, 0.02, z_wall),          # 0 wall top, left
        p(h, 0.02, z_wall),           # 1 wall top, right
        p(h, d_out, z_edge),          # 2 outer lip top, right
        p(-h, d_out, z_edge),         # 3 outer lip top, left
        p(-h, 0.02, z_edge - 0.30),   # 4 wall bottom, left
        p(h, 0.02, z_edge - 0.30),    # 5 wall bottom, right
        p(h, d_out, z_edge - 0.30),   # 6 valance bottom, right
        p(-h, d_out, z_edge - 0.30),  # 7 valance bottom, left
    ]
    faces = [
        (0, 1, 2, 3),  # sloped top
        (7, 6, 5, 4),  # underside
        (3, 2, 6, 7),  # valance (the lettered face)
        (1, 0, 4, 5),  # against the wall
        (0, 3, 7, 4),  # left end
        (2, 1, 5, 6),  # right end
    ]
    return new_mesh(name, v, faces, [mat])


def disc(name, edge, u, z, r, d0, d1, mat, sides=10):
    """Flat polygonal disc lying in a wall plane — the SouthBeach roundel."""
    prof = [
        (r * math.cos(2 * math.pi * k / sides), z + r * math.sin(2 * math.pi * k / sides))
        for k in range(sides)
    ]
    return face_panel(name, edge, u, prof, d0, d1, mat)


def blob(name, edge, u, z, rx, rz, d0, d1, mat, sides=9, seed=0):
    """Irregular flat blob in a wall plane — one shape of the Taber mural. The
    mural is ephemeral (plan 2.15 risk 4), so these are abstract forms, not a
    portrait of the 2025 piece."""
    prof = []
    for k in range(sides):
        a = 2 * math.pi * k / sides
        j = 0.78 + 0.30 * ((math.sin(seed * 7.7 + k * 2.3) + 1) / 2)
        prof.append((rx * j * math.cos(a), z + rz * j * math.sin(a)))
    return face_panel(name, edge, u, prof, d0, d1, mat)


def roof_uv(u, v):
    """Roof coordinates: u runs along the 3rd Street edge from the Taber (west)
    corner, v runs INTO the block (against that edge's outward normal)."""
    origin, _l, t, n = poly_edge(EDGE_THIRD)
    return (origin[0] + t[0] * u - n[0] * v, origin[1] + t[1] * u - n[1] * v)


def roof_box(name, u, v, z0, z1, su, sv, mat):
    cx, cy = roof_uv(u, v)
    _o, _l, t, _n = poly_edge(EDGE_THIRD)
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=math.atan2(t[1], t[0]))


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


def punched_window(tag, edge, u, w, z0, z1, cream, glass, ink, glow=None):
    """A punched opening: a cream surround, dark glazing PROUD of that surround,
    and a single sash bar. The glazing must not be recessed behind the wall
    plane — a recessed fill is invisible from every camera the app uses and the
    window reads as a solid pale block (learned on 592 Third)."""
    face_panel(f"{tag}_trim", edge, u, rect_profile(w + 0.26, z0 - 0.14, z1 + 0.14), 0.0, 0.06, cream)
    face_panel(f"{tag}_glass", edge, u, rect_profile(w, z0, z1), 0.04, 0.09, glass)
    face_panel(
        f"{tag}_sash", edge, u, rect_profile(w + 0.02, (z0 + z1) / 2 - 0.05, (z0 + z1) / 2 + 0.05),
        0.06, 0.11, ink,
    )
    if glow is not None:
        face_panel(
            f"{tag}_glow", edge, u, rect_profile(w - 0.22, z0 + 0.12, z1 - 0.12), 0.085, 0.115, glow
        )


def fire_door(tag, edge, u, w, z0, z1, cream, ink):
    """The fire-escape door: same surround as a window, but a solid dark leaf
    running to the floor. Bay 2 of the 3rd Street front on both upper storeys."""
    face_panel(f"{tag}_trim", edge, u, rect_profile(w + 0.26, z0 - 0.10, z1 + 0.14), 0.0, 0.06, cream)
    face_panel(f"{tag}_leaf", edge, u, rect_profile(w, z0, z1), 0.04, 0.09, ink)


def balcony(tag, edge, u, z, w, depth, ink):
    """One fire-escape landing: deck, top rail, and four uprights. Deliberately
    thin — the fire escape is a recognition cue but it must not out-detail the
    cornice it hangs below."""
    wall_box(f"{tag}_deck", edge, u, z, z + 0.11, w, depth, ink, d0=0.04)
    wall_box(f"{tag}_rail", edge, u, z + 0.92, z + 1.00, w, 0.06, ink, d0=depth)
    for k, du in enumerate((-w / 2 + 0.06, 0.0, w / 2 - 0.06)):
        wall_box(f"{tag}_post{k}", edge, u + du, z + 0.05, z + 1.00, 0.07, 0.07, ink, d0=depth - 0.07)


def stair(tag, edge, u, z_low, z_high, run, ink):
    """The diagonal flight between two landings: one stringer plus five treads.
    A real zig-zag would cost more than the cornice."""
    a, _l, t, n = poly_edge(edge)
    steps = 4
    for k in range(steps):
        f = (k + 0.5) / steps
        z = z_low + (z_high - z_low) * f
        du = -run / 2 + run * f
        wall_box(f"{tag}_tread{k}", edge, u + du, z, z + 0.06, run / steps + 0.04, 0.62, ink, d0=0.08)
    # stringer: a thin leaning slab approximated by three short segments
    for k in range(2):
        f = (k + 0.5) / 2
        z = z_low + (z_high - z_low) * f
        du = -run / 2 + run * f
        wall_box(f"{tag}_str{k}", edge, u + du, z - 0.26, z + 0.62, run / 2 + 0.05, 0.07, ink, d0=0.68)


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    oxblood = material("Toy_oxblood")
    rust = material("Toy_rust")
    cocoa = material("Toy_cocoa")
    cream = material("Toy_cream")
    greige = material("Toy_greige")
    tan = material("Toy_p_tan")
    cobalt = material("Toy_cobalt")
    mint = material("Toy_mint")
    glass = material("Toy_glass")
    ink = material("Toy_ink")
    orange = material("Toy_orange")
    mustard = material("Toy_mustard")
    steel = material("Toy_steel")
    oglow = material("Toy_orange_Glow")
    gglow = material("Toy_glass_Glow")

    # --- brick body: its top cap IS the roof membrane -----------------------
    prism("body", FOOTPRINT, 0.0, Z_DECK, oxblood, mat_caps=greige)

    # --- parapet ring: sets the 11.40 m crest and the loader's scale ---------
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_CREST, -PARAPET_T, 0.0, oxblood)

    # --- the cornice group ---------------------------------------------------
    # Corbel + dentils + cream fascia + a brick lip above it, run the full 3rd
    # Street front and RETURN 6.2 m into Taber Place before stopping — which is
    # what the alley elevation actually does. The two runs are mitred by overlap
    # at the west corner so the group reads as continuous around it.
    for edge, length, run in ((EDGE_THIRD, L_THIRD, L_THIRD), (EDGE_TABER, L_TABER, TABER_RETURN)):
        # u is measured from FOOTPRINT[edge]; on Taber that is the REAR corner,
        # so the return has to sit at the far end of the edge.
        u0 = length - run / 2.0 if edge == EDGE_TABER else length / 2.0
        tag = "third" if edge == EDGE_THIRD else "taber"
        face_panel(
            f"corbel_{tag}", edge, u0, rect_profile(run, Z_CORBEL0, Z_CORBEL1), 0.0, D_CORBEL, oxblood
        )
        face_panel(
            f"cornice_{tag}", edge, u0, rect_profile(run, Z_CORN0, Z_CORN1), 0.0, D_CORN, cream
        )
        face_panel(
            f"plip_{tag}", edge, u0, rect_profile(run, Z_PLIP0, Z_PLIP1), 0.0, D_PLIP, oxblood
        )
        # Dentils: one toothed strip. Individual teeth, but only on the 0.25 m
        # band, and only where the cornice runs.
        pitch = 0.46
        n_teeth = int(run / pitch)
        start = u0 - run / 2.0 + (run - n_teeth * pitch) / 2.0 + pitch / 2.0
        face_panel(
            f"dentband_{tag}", edge, u0, rect_profile(run, Z_DENT0, Z_DENT1), 0.0, 0.10, cream
        )
        for k in range(n_teeth):
            face_panel(
                f"dent_{tag}{k}", edge, start + k * pitch,
                rect_profile(0.24, Z_DENT0 + 0.03, Z_DENT1 - 0.03), 0.08, D_DENT, greige,
            )

    # --- the Greek-key belt band --------------------------------------------
    # Full 3rd Street front and the FULL Taber flank — unlike the cornice, this
    # band runs the whole alley elevation, and it is what ties the two designed
    # faces into one building. The meander itself is a row of greige shadow
    # ticks, and only on the hero elevation.
    for edge, length in ((EDGE_THIRD, L_THIRD), (EDGE_TABER, L_TABER)):
        tag = "third" if edge == EDGE_THIRD else "taber"
        face_panel(
            f"band_{tag}", edge, length / 2.0, rect_profile(length, Z_BAND0, Z_BAND1), 0.0, D_BAND, cream
        )
    pitch = 0.56
    n_tick = int(L_THIRD / pitch)
    start = (L_THIRD - n_tick * pitch) / 2.0 + pitch / 2.0
    for k in range(n_tick):
        face_panel(
            f"key{k}", EDGE_THIRD, start + k * pitch,
            rect_profile(0.20, Z_BAND0 + 0.09, Z_BAND1 - 0.09), D_BAND - 0.05, D_BAND - 0.01, greige,
        )

    # --- recessed basketweave brick panels ----------------------------------
    # Square panels on the two end piers at the 2nd/3rd floor spandrel, and a
    # horizontal panel over each 3rd-floor opening under the corbel band. Flush,
    # not recessed: an embedded panel in an opaque wall is invisible.
    for k, u in enumerate((THIRD_BAYS[0], THIRD_BAYS[-1])):
        face_panel(
            f"weave_sp{k}", EDGE_THIRD, u, rect_profile(1.15, 6.72, 7.18), -0.06, 0.02, cocoa
        )
    for k, u in enumerate(THIRD_BAYS):
        face_panel(
            f"weave_hi{k}", EDGE_THIRD, u, rect_profile(1.40, 9.34, 9.66), -0.06, 0.02, cocoa
        )
    # Two more on the Taber flank near the corner, where the alley elevation is
    # still being designed rather than merely built.
    for k, u in enumerate((L_TABER - 2.2, L_TABER - 5.4)):
        face_panel(
            f"weave_tb{k}", EDGE_TABER, u, rect_profile(1.05, 6.75, 7.20), -0.06, 0.02, cocoa
        )

    # --- 3rd Street upper storeys: five bays, bay 2 the fire-escape door -----
    lit2 = {0, 3}    # which 2nd-floor windows are lit at night
    lit3 = {2, 4}
    for i, u in enumerate(THIRD_BAYS):
        if i == BAY_FIRE:
            fire_door(f"fd2_{i}", EDGE_THIRD, u, WIN_W, Z_FLOOR2 - 0.20, Z_W2_1, cream, ink)
            fire_door(f"fd3_{i}", EDGE_THIRD, u, WIN_W, Z_FLOOR3 - 0.20, Z_W3_1, cream, ink)
            continue
        punched_window(
            f"w2_{i}", EDGE_THIRD, u, WIN_W, Z_W2_0, Z_W2_1, cream, glass, ink,
            glow=gglow if i in lit2 else None,
        )
        punched_window(
            f"w3_{i}", EDGE_THIRD, u, WIN_W, Z_W3_0, Z_W3_1, cream, glass, ink,
            glow=gglow if i in lit3 else None,
        )

    # --- the fire escape on bay 2 -------------------------------------------
    u_fe = THIRD_BAYS[BAY_FIRE]
    balcony("fe2", EDGE_THIRD, u_fe, Z_FLOOR2, 2.60, 1.05, ink)
    balcony("fe3", EDGE_THIRD, u_fe, Z_FLOOR3, 2.60, 1.05, ink)
    stair("fes", EDGE_THIRD, u_fe + 1.05, Z_FLOOR2 + 1.05, Z_FLOOR3, 1.90, ink)

    # --- 3rd Street shopfront ------------------------------------------------
    # Left (Taber end, low u): Neill's, an ORANGE awning over glazing.
    # Centre: the recessed residential entry to 521A.
    # Right: SouthBeach, a BLACK fascia over a steel roll-up shutter.
    # Far right: the small mustard 527 apartments entry awning.
    face_panel(
        "storefield", EDGE_THIRD, L_THIRD / 2.0, rect_profile(L_THIRD, 0.0, Z_STORE), 0.0, 0.05, ink
    )
    # Neill's: 0.35 .. 6.05 m from the corner
    face_panel("nl_bulk", EDGE_THIRD, 3.20, rect_profile(5.60, 0.0, 0.55), 0.05, 0.11, oxblood)
    face_panel("nl_glass", EDGE_THIRD, 3.20, rect_profile(5.20, 0.62, 3.10), 0.02, 0.08, glass)
    face_panel("nl_glow", EDGE_THIRD, 3.20, rect_profile(4.70, 0.85, 2.85), 0.075, 0.105, gglow)
    for k, u in enumerate((1.05, 3.20, 5.35)):
        face_panel(f"nl_mull{k}", EDGE_THIRD, u, rect_profile(0.14, 0.55, 3.15), 0.06, 0.12, ink)
    wall_wedge("nl_awning", EDGE_THIRD, 3.20, 5.90, 1.15, 3.48, 3.02, orange)
    face_panel("nl_awnglow", EDGE_THIRD, 3.20, rect_profile(5.50, 2.80, 3.00), 1.16, 1.19, oglow)
    # The projecting blade sign, near the Taber corner at second-floor level.
    wall_box("blade_arm", EDGE_THIRD, 1.05, 4.92, 5.02, 0.10, 0.85, ink, d0=0.06)
    wall_box("blade_body", EDGE_THIRD, 1.05, 4.30, 5.55, 0.16, 1.05, ink, d0=0.60)
    face_panel("blade_face", EDGE_THIRD, 1.05, rect_profile(0.98, 4.45, 5.40), 0.90, 0.94, orange)
    face_panel("blade_glow", EDGE_THIRD, 1.05, rect_profile(0.84, 4.55, 5.30), 0.94, 0.965, oglow)
    # 521A residential entry: a lit surround with a glazed door. A true recess is
    # a black hole inside a black field at this scale.
    face_panel("entry_trim", EDGE_THIRD, 6.70, rect_profile(1.35, 0.0, 3.05), 0.05, 0.10, cream)
    face_panel("entry_door", EDGE_THIRD, 6.70, rect_profile(0.95, 0.05, 2.75), 0.08, 0.13, glass)
    # SouthBeach: black fascia + steel roll-up shutter, 7.45 .. 12.95 m
    face_panel("sb_shutter", EDGE_THIRD, 10.20, rect_profile(5.20, 0.05, 3.05), 0.05, 0.11, steel)
    face_panel("sb_fascia", EDGE_THIRD, 10.20, rect_profile(5.50, 3.02, 3.52), 0.05, 0.20, ink)
    disc("sb_roundel", EDGE_THIRD, 8.35, 3.27, 0.30, 0.20, 0.245, cream)
    face_panel("sb_glow", EDGE_THIRD, 11.00, rect_profile(3.00, 3.12, 3.42), 0.205, 0.23, gglow)
    # The tag on the shutter. Every photograph of this shopfront since 2023 has
    # one; a bare steel roll-up on 3rd Street would be the invented version.
    blob("sb_tag", EDGE_THIRD, 10.10, 1.55, 1.45, 0.62, 0.105, 0.125, ink, seed=6)
    # 527 apartments entry at the party-wall end
    face_panel("ap_trim", EDGE_THIRD, 13.75, rect_profile(1.15, 0.0, 2.90), 0.05, 0.10, cream)
    face_panel("ap_door", EDGE_THIRD, 13.75, rect_profile(0.80, 0.05, 2.60), 0.08, 0.13, ink)
    wall_wedge("ap_awning", EDGE_THIRD, 13.75, 1.45, 0.70, 3.35, 3.05, mustard)

    # --- Taber Place flank ---------------------------------------------------
    # Ground storey is painted STUCCO, not brick, carrying a mural; above the
    # belt band the wall is plain brick with small, irregular openings and vent
    # slots — visibly secondary to the 3rd Street front.
    face_panel(
        "tb_stucco", EDGE_TABER, L_TABER / 2.0, rect_profile(L_TABER, 0.0, Z_BAND0), 0.0, 0.05, tan
    )
    mural = (
        (L_TABER - 3.4, 2.35, 1.55, 1.05, cobalt, 1),
        (L_TABER - 6.6, 1.60, 1.30, 0.95, mint, 2),
        (L_TABER - 9.4, 2.20, 1.15, 1.15, cobalt, 3),
        (L_TABER - 12.2, 1.45, 1.45, 0.80, ink, 4),
        (L_TABER - 15.6, 2.05, 1.05, 0.90, mint, 5),
    )
    for k, (u, z, rx, rz, mat, seed) in enumerate(mural):
        blob(f"mural{k}", EDGE_TABER, u, z, rx, rz, 0.05, 0.075, mat, seed=seed)
    # Upper openings: three windows per floor near the corner, vent slots behind.
    for k, u in enumerate((L_TABER - 1.9, L_TABER - 5.6, L_TABER - 9.6)):
        punched_window(f"tw2_{k}", EDGE_TABER, u, 0.95, 4.75, 5.95, cream, glass, ink,
                       glow=gglow if k == 0 else None)
        punched_window(f"tw3_{k}", EDGE_TABER, u, 0.95, 7.85, 9.05, cream, glass, ink)
    for k, u in enumerate((L_TABER - 12.3, L_TABER - 15.1, L_TABER - 17.9, L_TABER - 20.6)):
        face_panel(f"tv2_{k}", EDGE_TABER, u, rect_profile(0.62, 5.05, 5.60), -0.02, 0.05, ink)
        face_panel(f"tv3_{k}", EDGE_TABER, u, rect_profile(0.62, 8.15, 8.70), -0.02, 0.05, ink)
    # Downpipes. On a SoMa alley elevation these are the most reliable vertical
    # incident there is, and they are what stops 23 m of plain brick reading as
    # an unfinished face.
    for k, u in enumerate((L_TABER - 7.6, L_TABER - 18.9)):
        wall_box(f"tdp{k}", EDGE_TABER, u, 0.30, Z_CORBEL0 + 0.10, 0.18, 0.18, ink, d0=0.02)
        wall_box(f"tdp{k}_shoe", EDGE_TABER, u, 0.0, 0.42, 0.26, 0.26, ink, d0=0.02)
    # The rear fire escape, near the far end of the alley elevation.
    balcony("tfe2", EDGE_TABER, 3.60, Z_FLOOR2, 1.90, 0.85, ink)
    balcony("tfe3", EDGE_TABER, 3.60, Z_FLOOR3, 1.90, 0.85, ink)
    stair("tfes", EDGE_TABER, 3.60 + 0.95, Z_FLOOR2 + 1.05, Z_FLOOR3, 1.60, ink)

    # --- rear (NE) -----------------------------------------------------------
    # No public vantage reaches it (plan 2.4); modelled conservatively as plain
    # brick with four small utility openings, matching the far end of Taber.
    for k, u in enumerate((3.0, 6.1, 9.2, 12.0)):
        face_panel(f"rv2_{k}", EDGE_REAR, u, rect_profile(0.70, 4.90, 5.85), -0.02, 0.05, ink)
        face_panel(f"rv3_{k}", EDGE_REAR, u, rect_profile(0.70, 8.00, 8.95), -0.02, 0.05, ink)
    wall_box("rdp0", EDGE_REAR, 7.60, 0.30, Z_CORBEL0 + 0.10, 0.18, 0.18, ink, d0=0.02)

    # --- south-east party wall: blank ----------------------------------------
    # It abuts 549 Third, which stands 1.6 m taller. 549 is missing from the
    # committed bake, so this wall WILL be seen in the app until that gap is
    # fixed — it is left as honest blank brick rather than given invented
    # openings.

    # --- roof ----------------------------------------------------------------
    # On a 339 m2 plan only 11 m up, this asset is more roof than facade. The
    # first pass put four 0.55 m vents on it and read as an empty tray from the
    # app's camera (REPORT.md iteration 1); this is the second pass.
    #
    # HARD CONSTRAINT: the 11.40 m parapet crest is the manifest datum, so every
    # roof object has to live inside the 0.50 m between the deck and the crest.
    # That is the same call 592 Third made, and it is why the roof reads through
    # PLAN AREA and VALUE rather than through height: big pale blocks with dark
    # caps, long ducts, and a dark coping ring drawing the outline.
    ring_band("coping", FOOTPRINT, Z_CREST - 0.14, Z_CREST, -PARAPET_T - 0.05, 0.03, ink)

    # The hoist DAVIT FRAME on the 3rd Street parapet is what the 13.53 m LiDAR
    # maximum is measuring. Modelled co-terminal with the crest, not proud of it.
    for k, du in enumerate((-0.45, 0.45)):
        roof_box(f"davit_leg{k}", 5.10 + du, 1.30, Z_DECK, Z_CREST, 0.12, 0.12, steel)
        roof_box(f"davit_arm{k}", 5.10 + du, 0.85, Z_CREST - 0.14, Z_CREST, 0.12, 1.05, steel)
    roof_box("davit_bar", 5.10, 1.30, Z_CREST - 0.16, Z_CREST - 0.04, 1.14, 0.12, steel)
    roof_box("roof_ladder", 2.60, 1.30, Z_DECK, Z_CREST - 0.06, 0.70, 0.12, steel)

    # Stair head: the roof access of a 1914 walk-up. Wide in plan, low in
    # section, with a dark cap so it separates from the pale membrane.
    roof_box("bulk", 4.70, 5.60, Z_DECK, Z_DECK + 0.36, 2.45, 1.85, greige)
    roof_box("bulk_cap", 4.70, 5.60, Z_DECK + 0.33, Z_DECK + 0.45, 2.67, 2.07, ink)

    # Two mechanical cabinets, their duct run, and the saddles under it.
    for k, (u, v) in enumerate(((9.40, 4.10), (10.60, 12.30))):
        roof_box(f"mech{k}", u, v, Z_DECK, Z_DECK + 0.34, 1.70, 1.30, ink)
        roof_box(f"mech{k}_cap", u, v, Z_DECK + 0.31, Z_DECK + 0.43, 1.86, 1.46, steel)
    for k, (u, v, su, sv) in enumerate(
        ((9.40, 7.30, 0.50, 5.20), (7.40, 12.30, 4.60, 0.50), (5.10, 15.70, 0.50, 4.80))
    ):
        roof_box(f"duct{k}", u, v, Z_DECK + 0.14, Z_DECK + 0.46, su, sv, greige)

    # Two roof lights over the stair well and the rear light court.
    for k, (u, v) in enumerate(((8.10, 18.10), (11.00, 19.90))):
        roof_box(f"skyk{k}", u, v, Z_DECK, Z_DECK + 0.20, 1.60, 1.40, greige)
        roof_box(f"sky{k}_glass", u, v, Z_DECK + 0.17, Z_DECK + 0.30, 1.32, 1.12, glass)

    # Vents, flues and the two roof drains — small, but they are the scatter
    # that stops the tray reading as a moulded lid.
    for k, (u, v) in enumerate(
        ((2.90, 8.60), (2.75, 13.40), (12.30, 8.90), (12.10, 16.40), (6.80, 20.60))
    ):
        roof_box(f"vent{k}", u, v, Z_DECK, Z_DECK + 0.44, 0.66, 0.66, steel)
    for k, (u, v) in enumerate(((4.10, 10.90), (11.60, 20.40), (2.40, 18.90), (7.20, 8.30))):
        roof_box(f"flue{k}", u, v, Z_DECK, Z_CREST - 0.02, 0.24, 0.24, ink)
    for k, (u, v) in enumerate(((1.70, 5.60), (12.80, 21.20))):
        roof_box(f"drain{k}", u, v, Z_DECK - 0.04, Z_DECK + 0.09, 0.58, 0.58, ink)

    # Bevel budget: the chunky masses carry the miniature read, so they get the
    # full 0.12/2. Applied panels are thin — trims and bands get a token
    # 1-segment softening and the fills, ticks and glow shells none at all.
    # A beveled 12-tri panel costs ~60 tris. The 44 dentil teeth and 26 meander
    # ticks are 3 mm-scale repeats read at city distance: beveling them spent a
    # quarter of the whole budget on edges no camera resolves, so they are left
    # hard-edged. Everything that carries a silhouette still gets softened.
    skip = ("_glass", "_glow", "_sash", "_door", "_leaf", "_mull", "_face", "_roundel")
    skip_pre = ("dent_", "key", "mural", "tv2_", "tv3_", "rv2_", "rv3_", "tdp", "rdp",
                "vent", "flue", "drain", "duct", "davit", "sky")
    light = ("_trim", "_bulk", "band_", "corbel", "cornice", "plip_", "dentband_", "weave",
             "storefield", "tb_stucco", "sb_", "ap_", "nl_bulk")
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if name.endswith(skip) or "_glow" in name or name.startswith(skip_pre):
            continue
        if name.startswith(light) or name.endswith(("_trim", "_bulk")):
            bevel(obj, width=0.05, segments=1)
        else:
            bevel(obj, width=0.10, segments=2)

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
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    print("[build] anchor lon/lat: -122.3952384 37.7811509 (parcel OBB centre)")
    print("[build] 3rd Street front heading: 225.1 deg true (SW)")
    print("[build] Taber Place flank heading: 315.1 deg true (NW)")
    for u, v in ((5.10, 1.30), (2.60, 1.30), (4.70, 5.60), (9.40, 4.10), (10.60, 12.30),
                 (9.40, 7.30), (7.40, 12.30), (5.10, 15.70), (8.10, 18.10), (11.00, 19.90),
                 (2.90, 8.60), (2.75, 13.40), (12.30, 8.90), (12.10, 16.40), (6.80, 20.60),
                 (4.10, 10.90), (11.60, 20.40), (2.40, 18.90), (7.20, 8.30),
                 (1.70, 5.60), (12.80, 21.20)):
        px, py = roof_uv(u, v)
        if not point_inset_ok(px, py, 0.9):
            print(f"[build] WARN roof object at u={u} v={v} is within 0.9 m of a parapet")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "521-third.blend")
    glb = os.path.join(out, "521-third.glb")
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
