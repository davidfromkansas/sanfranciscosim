"""Deterministic Blender build of the SF-SIM miniature Pier 15 (Exploratorium).

    blender -b --python build_pier_15.py -- [--out DIR]

Writes pier-15.blend and pier-15.glb next to this file (or into --out). Geometry
is authored directly in world space in metres, Z up, +X east, +Y north, so the
model drops into the city at its real-world heading — the loader applies no
rotation.

Origin = the OSM pier polygon's area centroid (anchor lon -122.3974662,
lat 37.8016046), which is over open water. `placeGeneric` seats generic
landmarks at max(0, sampleElevation(x, z)), so **Z = 0 here is the waterline**,
not the promenade. Everything is quoted above that datum: pile heads 2.45 m,
deck 3.05 m, shed eave 8.5 m, monitor ridge 13.9 m, bulkhead parapet 11.0 m,
and the gable crest cap at exactly 16.4 m, which is the bounding-box top.

Design (see REFERENCE.md for the sources behind every number):

* the measured OSM deck footprint (way 1390720125) at its real 54.9 deg
  heading, with the south apron promenade, the east apron, the bay-end north
  plaza, and the water-courtyard notch on the northwest flank kept OPEN — the
  daylighted water between Piers 15 and 17 is a 2013 design feature;
* a pile field and a deck soffit, because this thing stands in the bay and the
  courtyard makes THIS pier's underside more visible than most;
* the 1931 transit shed (823 ft) wrapped in its 1.3 MW photovoltaic roof:
  three dark panel bands, pale walkway seams, cross-platforms, and the glazed
  monitor riding OFF-AXIS over the original 1931 central aisle (the pier was
  widened north in 1955; the asymmetry is real and visible from above);
* the identity feature: the 1931 classical bulkhead pavilion — tapering piers,
  a 9 m arch with a glazed fanlight, the giant white Exploratorium "O" ring
  proud of the glazing, "PIER 15" in proud letters on an arc, a gabled parapet
  with a stepped crest cap. The "O" is enlarged past scale because it is the
  museum's whole graphic identity and the one place exaggeration is spent;
* the 2013 Bay Observatory Gallery: a glazed two-storey pavilion at the bay
  end with a PV roof and square skylight, and the open Observatory Terrace
  between it and the shed's original narrow east bays;
* night state: the monitor's glazing strips are the hero (the real museum
  reads at night as one warm lit line riding a dark roof), the arch fanlight
  glows amber behind the "O", the observatory's upper band is lit, and the
  apron light standards are amber points. The PV panels never glow, and the
  "O" and "PIER 15" do not glow — they are daylight graphics.

The real flagpole tops out ~6 m above the crest. It is NOT modelled: a mast at
true height would become the bounding-box top and shrink the whole 245 m pier
by ~27% under targetHeightM normalisation (plan 2.15). Deliberate omission.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

AXIS_DEG = 54.9
AX = (math.sin(math.radians(AXIS_DEG)), math.cos(math.radians(AXIS_DEG)))
LT = (math.cos(math.radians(AXIS_DEG)), -math.sin(math.radians(AXIS_DEG)))

# OSM way 1390720125 (man_made=pier) projected with the app's tangent
# projection, recentred on its area centroid, expressed in the pier frame
# (s seaward along 54.9 deg, t across toward the southeast) and simplified:
# sub-2 m survey doglegs and the 9 m floating-dock cove are merged (plan 2.3).
DECK_ST = [
    (116.5, -52.6),   # bay-end north corner
    (59.7, -46.5),    # north apron taper
    (26.4, -41.4),    # courtyard notch, NE shoulder
    (26.4, -29.0),
    (-55.4, -28.6),   # courtyard edge (open water to the NW)
    (-70.4, -28.7),
    (-126.3, -45.7),  # west corner at the seawall
    (-126.4, 46.1),   # south corner at the seawall
    (-96.5, 46.2),    # forecourt
    (-96.6, 35.4),
    (58.9, 35.4),     # south apron promenade edge
    (58.8, 42.3),
    (116.8, 42.0),    # bay-end south corner
]

# Superstructure bounds in the pier frame, measured from OSM way 25478444
# reprojected the same way (plan 2.3).
BULK_S0, BULK_S1 = -139.0, -124.0     # bulkhead building
BULK_T0, BULK_T1 = -16.4, 37.9
# The shed runs near-full-width all the way to s 106.6 (rectified Aug-2026
# aerial + the OSM way's own m->n edge at t -25.5); only the last ~5 m narrow.
SHEDW_S0, SHEDW_S1 = -124.0, 106.6    # full-width shed (incl. 1955 north aisle)
SHEDW_T0, SHEDW_T1 = -24.5, 30.1
SHEDN_S0, SHEDN_S1 = 106.4, 111.5     # narrow east stub at the end face
SHEDN_T0, SHEDN_T1 = -7.2, 30.1
# Bay Observatory Gallery = OSM w738027034, ON THE NORTH APRON abutting the
# shed's NW wall line and overlooking the courtyard mouth (build review 3: the
# plan's original placement inside the shed way was wrong; the aerial's
# PV-roof-plus-skylight block is this footprint).
OBS_S0, OBS_S1 = 83.5, 108.6
OBS_T0, OBS_T1 = -45.4, -25.5

MON_T0, MON_T1 = 5.0, 13.0            # monitor over the 1931 central aisle
MON_TC = 9.0
MON_S0, MON_S1 = -118.0, 104.0

PAV_TC = 10.75                        # pavilion centred on the bulkhead
PAV_W = 15.0
ARCH_SPAN = 9.0

Z_PILE_TOP = 2.45
Z_DECK = 3.05
Z_SHED_EAVE = 8.50
Z_ROOF_HI = 9.60      # roof plane where it meets the monitor
Z_MON_SIDE = 12.80
Z_MON_RIDGE = 13.90
Z_BULK_EAVE = 10.40
Z_PARAPET = 11.00
Z_GABLE_APEX = 15.90
Z_CREST = 16.40       # crest cap on the gable = the bbox top (measured, 2.16)
Z_ARCH_SPRING = 5.50
Z_ARCH_CROWN = 10.00
Z_OBS_TOP = 12.40

CURB_W = 0.50
RAIL_H = 1.10

PALETTE_HEX = {
    "Toy_cream": "f2ede3",
    "Toy_stone": "d9d2c2",
    # Deck walking surface. Toy_conc is not in the shipped palette, so the
    # plan's fallback applies: one step darker than Toy_stone so slab, deck and
    # roof seams read as separate planes. Off-palette is a WARN, not a FAIL.
    "Toy_conc": "c6bfb2",
    "Toy_trim": "f3efe6",
    "Toy_glass": "2a4d73",
    "Toy_glassl": "6f95b8",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_ink": "3a3530",
    "Toy_glass_Glow": "6f95b8",
    "Toy_glassl_Glow": "7ea8c8",
    "Toy_amber_Glow": "e8b563",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def pw(s, t):
    """Pier frame (along-axis, across-axis) -> world (x, y)."""
    return (AX[0] * s + LT[0] * t, AX[1] * s + LT[1] * t)


def ensure_ccw(poly):
    area = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        area += x1 * y2 - x2 * y1
    return poly if area > 0 else poly[::-1]


DECK = ensure_ccw([pw(s, t) for s, t in DECK_ST])


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


def point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


def arch_cut_profile(w, z0, z_spring, z_crown, seg=10):
    a = w / 2.0
    rise = z_crown - z_spring
    pts = [(-a, z0), (a, z0), (a, z_spring)]
    for k in range(1, seg):
        th = math.pi * k / seg
        pts.append((a * math.cos(th), z_spring + rise * math.sin(th)))
    pts.append((-a, z_spring))
    return pts


def arch_ring_profile(w, z0, z_spring, z_crown, band, seg=10):
    a = w / 2.0
    rise = z_crown - z_spring
    outer = []
    for k in range(seg + 1):
        th = math.pi * k / seg
        outer.append(((a + band) * math.cos(th), z_spring + (rise + band) * math.sin(th)))
    inner = []
    for k in range(seg + 1):
        th = math.pi * (seg - k) / seg
        inner.append((a * math.cos(th), z_spring + rise * math.sin(th)))
    return [(a + band, z0)] + outer + [(-a - band, z0), (-a, z0)] + inner + [(a, z0)]


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


def bevel(obj, width=0.10, segments=2):
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


def sbox(name, s0, s1, t0, t1, z0, z1, mat):
    corners = [pw(s0, t0), pw(s1, t0), pw(s1, t1), pw(s0, t1)]
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, [mat])


def slope_slab(name, s0, s1, t0, z_t0, t1, z_t1, thick, mat):
    """A slab whose top plane runs from (t0, z_t0) to (t1, z_t1), constant in s."""
    corners = [(s0, t0), (s1, t0), (s1, t1), (s0, t1)]
    ztop = [z_t0, z_t0, z_t1, z_t1]
    verts = [(pw(s, t)[0], pw(s, t)[1], z - thick) for (s, t), z in zip(corners, ztop)]
    verts += [(pw(s, t)[0], pw(s, t)[1], z) for (s, t), z in zip(corners, ztop)]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, [mat])


def ngon_post(name, s, t, z0, z1, r, mat, seg=6):
    ring = [
        pw(s + r * math.cos(2 * math.pi * k / seg), t + r * math.sin(2 * math.pi * k / seg))
        for k in range(seg)
    ]
    return prism(name, ring, z0, z1, mat)


def front_panel(name, profile, t_centre, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in a plane of constant s, extruded
    between s = d0 and s = d1. u runs across the pier (+t). Used for everything
    on the bulkhead frontage (front = more negative s)."""
    verts = []
    for d in (d0, d1):
        for du, z in profile:
            x, y = pw(d, t_centre + du)
            verts.append((x, y, z))
    npts = len(profile)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def side_panel(name, profile, t0, t1, mat):
    """Closed prism of a (u, z) profile lying in a plane of constant t, extruded
    between t = t0 and t = t1. u runs along the pier (+s). Used for panels on
    the shed's long walls."""
    verts = []
    for t in (t0, t1):
        for du, z in profile:
            x, y = pw(du, t)
            verts.append((x, y, z))
    npts = len(profile)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def srect_profile(s0, s1, z0, z1):
    return [(s0, z0), (s1, z0), (s1, z1), (s0, z1)]


def arch_band_panel(name, t_c, w, z_spring, z_crown, band, d0, d1, mat, seg=12):
    """An arch-following band built from explicit quads (no n-gon caps — a
    concave ring profile's cap can ear-clip into a filled face)."""
    a = w / 2.0
    rise = z_crown - z_spring
    outer, inner = [], []
    for k in range(seg + 1):
        th = math.pi * k / seg
        outer.append((a + band) * math.cos(th))
        inner.append(a * math.cos(th))
    verts = []
    for d in (d0, d1):
        for k in range(seg + 1):
            th = math.pi * k / seg
            x, y = pw(d, t_c + (a + band) * math.cos(th))
            verts.append((x, y, z_spring + (rise + band) * math.sin(th)))
        for k in range(seg + 1):
            th = math.pi * k / seg
            x, y = pw(d, t_c + a * math.cos(th))
            verts.append((x, y, z_spring + rise * math.sin(th)))
    n = seg + 1
    faces = []
    for d0i in (0, 1):
        base = d0i * 2 * n
        for k in range(seg):
            q = (base + k, base + k + 1, base + n + k + 1, base + n + k)
            faces.append(q if d0i == 0 else q[::-1])
    for k in range(seg):  # outer and inner walls between depths
        faces.append((k, k + 1, 2 * n + k + 1, 2 * n + k))
        faces.append((n + k + 1, n + k, 3 * n + k, 3 * n + k + 1))
    for k_a, k_b in ((0, n), (seg, n + seg)):  # end caps at the springing
        faces.append((k_a, k_b, 2 * n + k_b, 2 * n + k_a))
    return new_mesh(name, verts, faces, [mat])


def annulus_panel(name, t_c, z_c, r_out, r_in, d0, d1, mat, seg=24):
    """A flat ring (the Exploratorium "O") in the frontage plane."""
    verts = []
    for d in (d0, d1):
        for r in (r_out, r_in):
            for k in range(seg):
                th = 2 * math.pi * k / seg
                x, y = pw(d, t_c + r * math.cos(th))
                verts.append((x, y, z_c + r * math.sin(th)))
    faces = []

    def idx(di, ri, k):
        return di * 2 * seg + ri * seg + (k % seg)

    for k in range(seg):
        faces.append((idx(0, 0, k), idx(0, 0, k + 1), idx(0, 1, k + 1), idx(0, 1, k)))
        faces.append((idx(1, 1, k), idx(1, 1, k + 1), idx(1, 0, k + 1), idx(1, 0, k)))
        faces.append((idx(0, 0, k + 1), idx(0, 0, k), idx(1, 0, k), idx(1, 0, k + 1)))
        faces.append((idx(0, 1, k), idx(0, 1, k + 1), idx(1, 1, k + 1), idx(1, 1, k)))
    return new_mesh(name, verts, faces, [mat])


def ring_band(name, poly, z0, z1, off_in, off_out, mat):
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


def rail_chain(tag, pts_st, mat, half=0.06, base=None):
    """Solid railing ribbon along a chain of pier-frame points."""
    base = Z_DECK if base is None else base
    made = []
    for i in range(len(pts_st) - 1):
        (s0, t0), (s1, t1) = pts_st[i], pts_st[i + 1]
        dx, dy = s1 - s0, t1 - t0
        length = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / length * half, dx / length * half
        quad = [
            pw(s0 + nx, t0 + ny),
            pw(s1 + nx, t1 + ny),
            pw(s1 - nx, t1 - ny),
            pw(s0 - nx, t0 - ny),
        ]
        made.append(prism(f"{tag}{i}", ensure_ccw(quad), base + 0.55, base + RAIL_H, mat))
    return made


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
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------- lettering

BAR = 0.155
GLYPHS = {
    "P": [(0, BAR, 0, 1), (0, 0.62, 1 - BAR, 1), (0, 0.62, 0.5 - BAR / 2, 0.5 + BAR / 2),
          (0.62 - BAR, 0.62, 0.5 - BAR / 2, 1)],
    "I": [(0.16, 0.32, 0, 1)],
    "E": [(0, BAR, 0, 1), (0, 0.62, 1 - BAR, 1), (0, 0.56, 0.5 - BAR / 2, 0.5 + BAR / 2),
          (0, 0.62, 0, BAR)],
    "R": [(0, BAR, 0, 1), (0, 0.62, 1 - BAR, 1), (0, 0.62, 0.5 - BAR / 2, 0.5 + BAR / 2),
          (0.62 - BAR, 0.62, 0.5 - BAR / 2, 1), (0.40, 0.62, 0, 0.5 - BAR / 2)],
    "1": [(0.23, 0.39, 0, 1), (0.08, 0.23, 0.72, 0.87)],
    "5": [(0, 0.62, 1 - BAR, 1), (0, BAR, 0.5, 1), (0, 0.62, 0.5 - BAR / 2, 0.5 + BAR / 2),
          (0.62 - BAR, 0.62, BAR, 0.5), (0, 0.62, 0, BAR)],
}
ADVANCE = {"P": 0.72, "I": 0.46, "E": 0.76, "R": 0.76, "1": 0.56, "5": 0.76, " ": 0.28}


def inscription(text, t_centre, z_base, cap_h, d0, d1, mat, arc_r=0.0, tag="letter"):
    """Proud blocky lettering centred on t_centre. With arc_r > 0 the baseline
    follows a circle of radius arc_r whose top is at z_base (the "PIER 15" arc
    above the arch)."""
    width = sum(ADVANCE[c] for c in text) * cap_h
    u = -width / 2.0
    n = 0
    for ch in text:
        adv = ADVANCE[ch] * cap_h
        if ch == " ":
            u += adv
            continue
        u_mid = u + adv / 2.0
        dz = 0.0
        if arc_r > 0.0:
            dz = (math.sqrt(max(0.0, arc_r * arc_r - u_mid * u_mid)) - arc_r)
        for x0, x1, y0, y1 in GLYPHS[ch]:
            prof = [
                (u + x0 * cap_h, z_base + dz + y0 * cap_h),
                (u + x1 * cap_h, z_base + dz + y0 * cap_h),
                (u + x1 * cap_h, z_base + dz + y1 * cap_h),
                (u + x0 * cap_h, z_base + dz + y1 * cap_h),
            ]
            front_panel(f"{tag}{n}", prof, t_centre, d0, d1, mat)
            n += 1
        u += adv
    return n


# --------------------------------------------------------------------- parts


def build():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for item in list(block):
            block.remove(item)
    scene = bpy.context.scene

    cream = material("Toy_cream")
    stone = material("Toy_stone")
    conc = material("Toy_conc")
    trim = material("Toy_trim")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    ink = material("Toy_ink")
    g_glass = material("Toy_glass_Glow")
    g_glassl = material("Toy_glassl_Glow")
    g_amber = material("Toy_amber_Glow")

    # ------------------------------------------------------------ substructure
    # Pile field: only under the edge band and a centre spine — a full 1931 grid
    # is ~1,100 piles. Hard-capped so a footprint edit cannot blow the budget.
    inner = offset_polygon(DECK, -1.2)
    core = offset_polygon(DECK, -11.0)
    piles = 0
    step = 8.0
    s = -128.0
    while s <= 118.0 and piles < 150:
        t = -52.0
        while t <= 46.0 and piles < 150:
            x, y = pw(s, t)
            if point_in_poly(x, y, inner) and (
                not point_in_poly(x, y, core) or abs(t - 3.0) < step / 2.0
            ):
                sbox(f"pile{piles}", s - 0.45, s + 0.45, t - 0.45, t + 0.45, 0.0, Z_PILE_TOP, stone)
                piles += 1
            t += step
        s += step

    # Deck slab (the soffit band the piles carry) and the walking surface.
    prism("deck_slab", DECK, Z_PILE_TOP, Z_DECK, stone)
    prism("deck_surface", offset_polygon(DECK, -0.4), Z_DECK, Z_DECK + 0.05, conc)

    # Fender curb: chunky dark ring round the whole deck.
    ring_band("curb", DECK, Z_DECK, Z_DECK + 0.45, -CURB_W, 0.0, ink)

    # Railing ribbons: south apron, bay end, north plaza, courtyard notch.
    # The seawall frontage (the museum's entry plaza) stays open.
    rail_chain("rail_s", [(-90.0, 34.6), (58.4, 34.6), (58.4, 41.5), (115.9, 41.2)], steel)
    rail_chain("rail_e", [(115.9, 41.2), (115.7, -51.8)], steel)
    rail_chain("rail_n", [(115.7, -51.8), (59.7, -45.7), (27.2, -40.7), (27.2, -29.8)], steel)
    rail_chain("rail_c", [(27.2, -29.8), (-55.4, -29.4), (-70.4, -29.5)], steel)

    # ------------------------------------------------------------- deck fitout
    # Light standards along the public aprons.
    lamps = []
    n = 0
    s = -88.0
    while s <= 52.0:
        lamps.append((s, 33.2))
        s += 24.0
    # North-apron lamps hug the deck edge walkway NW of the observatory.
    lamps += [(68.0, -45.6), (90.0, -47.9), (112.0, -50.3)]
    lamps += [(113.5, 20.0), (113.5, -10.0), (113.5, -32.0)]
    for i, (ls, lt) in enumerate(lamps):
        ngon_post(f"lamp{i}", ls, lt, Z_DECK, Z_DECK + 5.50, 0.22, ink, seg=4)
        sbox(f"lamphead{i}", ls - 0.58, ls + 0.58, lt - 0.32, lt + 0.32,
             Z_DECK + 5.56, Z_DECK + 5.95, steel)

    # Bollards down the south apron and around the head.
    n = 0
    s = -92.0
    while s <= 110.0:
        ngon_post(f"bollard{n}", s, 34.9, Z_DECK + 0.05, Z_DECK + 0.50, 0.22, ink)
        n += 1
        s += 12.0

    # The group-entry pavilion on the forecourt's northwest flare (the old
    # Terminal Office site): a low charcoal box with a pale sign band — the
    # dark "expl O ratorium" gateway seen from the valley gate.
    sbox("entry", -123.0, -114.0, -40.0, -30.0, Z_DECK, Z_DECK + 4.25, ink)
    sbox("entry_sign", -123.15, -122.95, -38.5, -31.5, Z_DECK + 3.1, Z_DECK + 3.9, trim)
    sbox("entry_glow", -123.3, -123.16, -37.0, -33.0, Z_DECK + 1.0, Z_DECK + 2.6, g_amber)

    # ------------------------------------------------------------------- shed
    # Two overlapping solids: the full-width 1955 shed and the original narrow
    # east bays (they interpenetrate slightly rather than sharing a face).
    sbox("shed_w", SHEDW_S0, SHEDW_S1, SHEDW_T0, SHEDW_T1, Z_DECK, Z_SHED_EAVE, stone)
    sbox("shed_n", SHEDN_S0, SHEDN_S1, SHEDN_T0, SHEDN_T1, Z_DECK, Z_SHED_EAVE, stone)

    # Roof planes rising to the monitor. Wide section NW plane, narrow section
    # NW plane, and the SE plane running the full length.
    slope_slab("roof_nw_w", SHEDW_S0, SHEDW_S1, SHEDW_T0, Z_SHED_EAVE, MON_T0, Z_ROOF_HI,
               0.30, conc)
    slope_slab("roof_nw_n", SHEDN_S0, SHEDN_S1, SHEDN_T0, Z_SHED_EAVE, MON_T0, Z_ROOF_HI,
               0.30, conc)
    slope_slab("roof_se", SHEDW_S0, SHEDN_S1, MON_T1, Z_ROOF_HI, SHEDW_T1, Z_SHED_EAVE,
               0.30, conc)

    # The PV array: dark panel bands 0.15 m proud of the roof planes, pale
    # seams between, reading as the aerial does (plan 2.9). Split into strips
    # along s so the cross-platforms show as breaks.
    def pv_run(tag, plane, t0, t1, s0, s1):
        # plane: (t_eave, z_eave, t_hi, z_hi)
        te, ze, th, zh = plane
        def zat(t):
            return ze + (zh - ze) * (t - te) / (th - te)
        stations = [s0, -87.0, -84.0, -32.0, -29.0, 23.0, 26.0, 78.0, 81.0, s1]
        k = 0
        for i in range(0, len(stations) - 1, 2):
            a, b = stations[i], stations[i + 1]
            a = max(a, s0)
            b = min(b, s1)
            if b - a < 4.0:
                continue
            slope_slab(f"pv_{tag}{k}", a, b, t0, zat(t0) + 0.15, t1, zat(t1) + 0.15,
                       0.14, glass)
            k += 1

    plane_nw = (SHEDW_T0, Z_SHED_EAVE, MON_T0, Z_ROOF_HI)
    plane_se = (MON_T1, Z_ROOF_HI, SHEDW_T1, Z_SHED_EAVE)
    pv_run("a", plane_nw, -23.2, -10.0, SHEDW_S0 + 1.5, SHEDW_S1 - 1.5)
    pv_run("b", plane_nw, -8.2, 4.2, SHEDW_S0 + 1.5, SHEDW_S1 - 1.5)
    pv_run("c", plane_se, 13.8, 21.0, SHEDW_S0 + 1.5, SHEDN_S1 - 4.0)
    pv_run("d", plane_se, 22.0, 29.2, SHEDW_S0 + 1.5, SHEDN_S1 - 4.0)

    # The monitor: a long glazed bar over the 1931 central aisle, off today's
    # centreline by design. Frame, glazing strips, gabled ridge cap.
    sbox("monitor", MON_S0, MON_S1, MON_T0, MON_T1, Z_ROOF_HI - 0.2, Z_MON_SIDE, steel)
    for tag, tt0, tt1 in (("nw", MON_T0 - 0.10, MON_T0 + 0.02),
                          ("se", MON_T1 - 0.02, MON_T1 + 0.10)):
        side_panel(f"monitor_glass_{tag}", srect_profile(MON_S0 + 1.0, MON_S1 - 1.0,
                                                         Z_ROOF_HI + 0.5, Z_MON_SIDE - 0.4),
                   tt0, tt1, glassl)
    # Gabled cap: ridge at t = MON_TC.
    cap = [
        (MON_T0 - 0.15, Z_MON_SIDE), (MON_T1 + 0.15, Z_MON_SIDE),
        (MON_TC, Z_MON_RIDGE),
    ]
    verts = []
    for s_ in (MON_S0, MON_S1):
        for t_, z_ in cap:
            x, y = pw(s_, t_)
            verts.append((x, y, z_))
    new_mesh("monitor_cap", verts,
             [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)], [steel])
    # Glazed strips on both cap slopes so the monitor reads as a lightband from
    # the aerial camera, which is where it carries the roof's identity.
    for tag, ta, tb in (("nw", MON_T0 + 0.6, MON_TC - 0.5), ("se", MON_TC + 0.5, MON_T1 - 0.6)):
        za = Z_MON_SIDE + (Z_MON_RIDGE - Z_MON_SIDE) * (ta - MON_T0 + 0.15) / (MON_TC - MON_T0 + 0.15)
        zb = Z_MON_SIDE + (Z_MON_RIDGE - Z_MON_SIDE) * (MON_T1 + 0.15 - tb) / (MON_T1 + 0.15 - MON_TC)
        if tag == "nw":
            slope_slab(f"monitor_capglass_{tag}", MON_S0 + 2.0, MON_S1 - 2.0,
                       ta, za + 0.10, tb, Z_MON_RIDGE + 0.02, 0.09, glassl)
        else:
            slope_slab(f"monitor_capglass_{tag}", MON_S0 + 2.0, MON_S1 - 2.0,
                       ta, Z_MON_RIDGE + 0.02, tb, zb + 0.10, 0.09, glassl)

    # Clerestory band and door bays on the shed's long walls.
    side_panel("clere_se_frame", srect_profile(SHEDW_S0 + 3.0, SHEDN_S1 - 3.0, 6.9, 8.2),
               SHEDW_T1 - 0.02, SHEDW_T1 + 0.08, ink)
    side_panel("clere_se_glass", srect_profile(SHEDW_S0 + 3.5, SHEDN_S1 - 3.5, 7.1, 8.05),
               SHEDW_T1 + 0.08, SHEDW_T1 + 0.16, glass)
    side_panel("clere_nww_frame", srect_profile(SHEDW_S0 + 3.0, SHEDW_S1 - 3.0, 6.9, 8.2),
               SHEDW_T0 - 0.08, SHEDW_T0 + 0.02, ink)
    side_panel("clere_nww_glass", srect_profile(SHEDW_S0 + 3.5, SHEDW_S1 - 3.5, 7.1, 8.05),
               SHEDW_T0 - 0.16, SHEDW_T0 - 0.08, glass)
    # (The 5 m narrow stub carries no clerestory of its own.)

    for k, sc in enumerate((-100.0, -62.0, -24.0, 14.0)):
        # South apron door bays with canopy slabs.
        side_panel(f"door_se{k}", srect_profile(sc - 2.4, sc + 2.4, Z_DECK + 0.05, 5.8),
                   SHEDW_T1 - 0.02, SHEDW_T1 + 0.10, ink)
        sbox(f"canopy_se{k}", sc - 3.0, sc + 3.0, SHEDW_T1 + 0.02, SHEDW_T1 + 1.55,
             6.00, 6.24, steel)
        # Courtyard-side bays under the old loading-dock canopy.
        side_panel(f"door_nw{k}", srect_profile(sc - 2.4, sc + 2.4, Z_DECK + 0.05, 5.8),
                   SHEDW_T0 - 0.10, SHEDW_T0 + 0.02, ink)
        sbox(f"canopy_nw{k}", sc - 3.0, sc + 3.0, SHEDW_T0 - 1.55, SHEDW_T0 - 0.02,
             6.00, 6.24, steel)

    # East end: the shed's faintly Art Deco outer wall — a central gabled plane
    # and four shallow pier strips, one plane of relief each (plan 2.6).
    front_gable = [(-6.0, Z_SHED_EAVE - 0.4), (6.0, Z_SHED_EAVE - 0.4),
                   (0.9, Z_SHED_EAVE + 2.1), (-0.9, Z_SHED_EAVE + 2.1)]
    ec = (SHEDN_T0 + SHEDN_T1) / 2.0
    front_panel("end_gable", front_gable, ec, SHEDN_S1, SHEDN_S1 + 0.25, cream)
    for k, toff in enumerate((-14.0, -7.0, 7.0, 14.0)):
        front_panel(f"end_pier{k}", rect_profile(1.1, Z_DECK + 0.2, Z_SHED_EAVE + 0.3),
                    ec + toff, SHEDN_S1, SHEDN_S1 + 0.18, stone)

    # --------------------------------------------------- observatory + terrace
    sbox("obs", OBS_S0, OBS_S1, OBS_T0, OBS_T1, Z_DECK, Z_OBS_TOP - 0.5, steel)
    obs_poly = [pw(OBS_S0, OBS_T0), pw(OBS_S1, OBS_T0), pw(OBS_S1, OBS_T1), pw(OBS_S0, OBS_T1)]
    ring_band("obs_parapet", obs_poly, Z_OBS_TOP - 0.5, Z_OBS_TOP, -0.30, 0.02, steel)
    # Broad glazing bands both storeys on the water-facing sides.
    for tag, prof_t0, prof_t1 in (("nw", OBS_T0 - 0.10, OBS_T0 + 0.02),):
        for i, (z0, z1) in enumerate(((4.0, 6.3), (8.4, 11.3))):
            side_panel(f"obs_glass_{tag}{i}", srect_profile(OBS_S0 + 0.8, OBS_S1 - 0.8, z0, z1),
                       prof_t0, prof_t1, glass)
    for i, (z0, z1) in enumerate(((4.0, 6.3), (8.4, 11.3))):
        front_panel(f"obs_glass_e{i}",
                    rect_profile(OBS_T1 - OBS_T0 - 1.6, z0, z1),
                    (OBS_T0 + OBS_T1) / 2.0, OBS_S1, OBS_S1 + 0.10, glass)
        front_panel(f"obs_glass_w{i}",
                    rect_profile(OBS_T1 - OBS_T0 - 1.6, z0, z1),
                    (OBS_T0 + OBS_T1) / 2.0, OBS_S0 - 0.10, OBS_S0, glass)
    # Roof: PV quads and the pale square skylight.
    sbox("obs_pv_a", OBS_S0 + 1.0, OBS_S0 + 8.5, OBS_T0 + 1.0, OBS_T1 - 1.0,
         Z_OBS_TOP - 0.48, Z_OBS_TOP - 0.34, glass)
    sbox("obs_pv_b", OBS_S1 - 8.5, OBS_S1 - 1.0, OBS_T0 + 1.0, OBS_T1 - 1.0,
         Z_OBS_TOP - 0.48, Z_OBS_TOP - 0.34, glass)
    sbox("obs_skylight", OBS_S0 + 9.4, OBS_S1 - 9.4, (OBS_T0 + OBS_T1) / 2 - 2.4,
         (OBS_T0 + OBS_T1) / 2 + 2.4, Z_OBS_TOP - 0.40, Z_OBS_TOP - 0.05, glassl)
    # Night: the upper band lit on the courtyard side.
    side_panel("obs_glow", srect_profile(OBS_S0 + 1.2, OBS_S1 - 1.2, 8.7, 11.0),
               OBS_T0 - 0.17, OBS_T0 - 0.11, g_glass)

    # The "Observatory Terrace" of the 2013 project is an upper-level deck ON
    # the observatory/shed junction, not a freestanding platform — at toy scale
    # it reads as the observatory's parapet roofline and is not modelled
    # separately (build review 3).

    # ---------------------------------------------------------------- bulkhead
    sbox("bulkhead", BULK_S0, BULK_S1 + 0.4, BULK_T0, BULK_T1, Z_DECK, Z_BULK_EAVE, cream)
    bulk_poly = [pw(BULK_S0, BULK_T0), pw(BULK_S1 + 0.4, BULK_T0),
                 pw(BULK_S1 + 0.4, BULK_T1), pw(BULK_S0, BULK_T1)]
    sbox("bulkhead_roof", BULK_S0 + 0.4, BULK_S1, BULK_T0 + 0.4, BULK_T1 - 0.4,
         Z_BULK_EAVE - 0.02, Z_BULK_EAVE + 0.10, roofd)
    ring_band("bulk_cornice", bulk_poly, Z_BULK_EAVE, Z_BULK_EAVE + 0.35, -0.05, 0.35, stone)
    ring_band("bulk_parapet", bulk_poly, Z_BULK_EAVE + 0.35, Z_PARAPET - 0.15, -0.05, 0.05, cream)
    ring_band("bulk_parapet_cap", bulk_poly, Z_PARAPET - 0.15, Z_PARAPET, -0.14, 0.14, stone)
    # A few PV quads on the bulkhead roof (visible in the 2026 aerial).
    sbox("bulk_pv", BULK_S0 + 2.0, BULK_S1 - 2.0, BULK_T0 + 3.0, PAV_TC - 8.5,
         Z_BULK_EAVE + 0.10, Z_BULK_EAVE + 0.24, glass)
    sbox("bulk_pv2", BULK_S0 + 2.0, BULK_S1 - 2.0, PAV_TC + 8.5, BULK_T1 - 3.0,
         Z_BULK_EAVE + 0.10, Z_BULK_EAVE + 0.24, glass)

    # Wing windows: two bays each side, tall 25-light sash below, 9-light above.
    lit = 0
    for i, tc in enumerate((-11.5, -3.5, 23.4, 32.4)):
        w = 5.6
        front_panel(f"wing_rev_g{i}", rect_profile(w + 0.5, 3.9, 7.15), tc,
                    BULK_S0 - 0.10, BULK_S0, ink)
        front_panel(f"wing_glass_g{i}", rect_profile(w, 4.1, 6.95), tc,
                    BULK_S0 - 0.16, BULK_S0 - 0.06, glass)
        front_panel(f"wing_rev_u{i}", rect_profile(w + 0.5, 7.95, 10.05), tc,
                    BULK_S0 - 0.10, BULK_S0, ink)
        front_panel(f"wing_glass_u{i}", rect_profile(w, 8.15, 9.85), tc,
                    BULK_S0 - 0.16, BULK_S0 - 0.06, glass)
        if i in (1, 2):
            lit += 1
            front_panel(f"wing_glow{i}", rect_profile(w - 0.4, 8.35, 9.65), tc,
                        BULK_S0 - 0.23, BULK_S0 - 0.17, g_glass)
    # End-elevation windows deliberately dropped: the bulkhead ends are one bay
    # wide and read as noise at city scale; the budget goes to the pavilion.

    # ------------------------------------------------------------ portal pavilion
    P = BULK_S0 - 0.30  # pavilion front plane, proud of the bulkhead
    front_panel("pavilion", rect_profile(PAV_W, Z_DECK, Z_PARAPET), PAV_TC, P, BULK_S1 - 8.0,
                cream)
    # Tapering flank piers: wider at the base, read as battered masses.
    for sgn in (-1.0, 1.0):
        base_c = PAV_TC + sgn * (PAV_W / 2.0 - 1.1)
        prof = [(-1.55, Z_DECK), (1.55, Z_DECK), (1.05, Z_PARAPET + 0.4), (-1.05, Z_PARAPET + 0.4)]
        front_panel(f"pier_{'nw' if sgn < 0 else 'se'}", prof, base_c, P - 0.35, BULK_S0 + 2.0,
                    cream)
    # The gabled parapet wall: a solid trapezoid rising to the apex, carrying
    # the lettering; stone rakes along both edges; the crest cap on top.
    gable = [(-PAV_W / 2.0 - 0.45, Z_PARAPET), (PAV_W / 2.0 + 0.45, Z_PARAPET),
             (0.5, Z_GABLE_APEX), (-0.5, Z_GABLE_APEX)]
    front_panel("gable", gable, PAV_TC, P - 0.10, BULK_S0 + 2.5, cream)
    for sgn, tag in ((-1.0, "l"), (1.0, "r")):
        a = PAV_W / 2.0 + 0.45
        rake = [(sgn * a, Z_PARAPET - 0.05), (sgn * (a - 0.55), Z_PARAPET - 0.05),
                (sgn * 0.25, Z_GABLE_APEX + 0.22), (sgn * 0.8, Z_GABLE_APEX + 0.22)]
        if sgn > 0:
            rake = rake[::-1]
        front_panel(f"gable_rake_{tag}", rake, PAV_TC, P - 0.22, P + 0.6, stone)
    front_panel("gable_base_mould", rect_profile(PAV_W + 1.4, Z_PARAPET - 0.30, Z_PARAPET),
                PAV_TC, P - 0.20, P + 0.6, stone)
    # Crest cap: the measured 16.4 m top of the composition.
    sbox("crest", BULK_S0 - 0.55, BULK_S0 + 2.1, PAV_TC - 1.05, PAV_TC + 1.05,
         Z_GABLE_APEX - 0.15, Z_CREST - 0.14, cream)
    sbox("crest_cap", BULK_S0 - 0.70, BULK_S0 + 2.25, PAV_TC - 1.20, PAV_TC + 1.20,
         Z_CREST - 0.14, Z_CREST, stone)
    # No flagpole: see module docstring (the 22.6 m mast is a scale trap).

    # The arch: reveal, glazed fanlight + door band, voussoirs, "O", glow.
    front_panel("arch_reveal", arch_cut_profile(ARCH_SPAN, Z_DECK, Z_ARCH_SPRING, Z_ARCH_CROWN),
                PAV_TC, P - 0.02, BULK_S1 - 6.0, ink)
    front_panel("arch_fan",
                arch_cut_profile(ARCH_SPAN - 0.6, Z_DECK + 0.6, Z_ARCH_SPRING,
                                 Z_ARCH_CROWN - 0.40),
                PAV_TC, P - 0.09, P - 0.03, glass)
    front_panel("arch_transom", rect_profile(ARCH_SPAN - 1.3, Z_ARCH_SPRING - 0.10,
                                             Z_ARCH_SPRING + 0.10),
                PAV_TC, P - 0.13, P - 0.07, steel)
    front_panel("arch_doors", rect_profile(ARCH_SPAN - 2.6, Z_DECK + 0.1, 3.2),
                PAV_TC, P - 0.12, P - 0.04, ink)
    front_panel("arch_voussoir",
                arch_ring_profile(ARCH_SPAN, Z_DECK, Z_ARCH_SPRING, Z_ARCH_CROWN, 0.70),
                PAV_TC, P - 0.25, P, stone)
    # Night: a lit arch OUTLINE just inside the voussoirs — a filled fanlight
    # glow washed the whole glazing warm at the app's 12% day alpha (review 2).
    # Night: a lit arch OUTLINE just inside the voussoirs, not a filled panel —
    # a filled shape at the app's 12% day alpha washes the whole fanlight warm.
    arch_band_panel("arch_glow", PAV_TC, ARCH_SPAN - 1.5, Z_ARCH_SPRING,
                    Z_ARCH_CROWN - 0.85, 0.50, P - 0.17, P - 0.11, g_amber)
    # The Exploratorium "O": a proud white ring floating on the fanlight. Kept
    # low enough that its whole interior shows glazing, not wall (review 1).
    annulus_panel("O_ring", PAV_TC, 6.90, 2.55, 2.10, P - 0.45, P - 0.20, trim)

    # "PIER 15" on an arc above the arch, proud dark letters (mid-1930s signs
    # were dark metal on the cream stucco — ink, not stone).
    letters = inscription("PIER 15", PAV_TC, 11.55, 1.10, P - 0.16, P + 0.3, ink,
                          arc_r=9.5)

    # ------------------------------------------------------------------- night
    for tag, tt0, tt1 in (("nw", MON_T0 - 0.24, MON_T0 - 0.16),
                          ("se", MON_T1 + 0.16, MON_T1 + 0.24)):
        side_panel(f"monitor_glow_{tag}",
                   srect_profile(MON_S0 + 2.0, MON_S1 - 2.0, Z_ROOF_HI + 0.6, Z_MON_SIDE - 0.5),
                   tt0, tt1, g_glassl)
    for i, (ls, lt) in enumerate(lamps):
        sbox(f"lampglow{i}", ls - 0.86, ls + 0.86, lt - 0.50, lt + 0.50,
             Z_DECK + 5.42, Z_DECK + 5.56, g_amber)

    # ------------------------------------------------------------------ bevels
    HEAVY = ("bulkhead", "pavilion", "gable", "crest", "crest_cap", "arch_voussoir",
             "pier_nw", "pier_se", "obs", "entry")
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if name.startswith(("pile", "letter", "lampglow", "wing_glow", "pv_",
                            "monitor_glow", "obs_glow", "entry_glow", "arch_glow")):
            continue
        if "glass" in name or "glow" in name.lower():
            continue
        if name in HEAVY:
            bevel(obj, width=0.10, segments=2)
        elif name.startswith(("deck_", "curb", "rail")):
            bevel(obj, width=0.06, segments=1)
        else:
            bevel(obj, width=0.05, segments=1)

    print(f"[build] piles={piles} lamps={len(lamps)} letters={letters} lit_wing_bays={lit}")
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
    print("[build] anchor lon/lat: -122.3974662 37.8016046 (OSM pier polygon area centroid)")
    print("[build] pier axis 54.9 deg true; frontage faces ~235 deg (SW)")
    print("[build] Z=0 is the WATERLINE: piles 0-2.45, deck 3.05, crest 16.4")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "pier-15.blend")
    glb = os.path.join(out, "pier-15.glb")
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
