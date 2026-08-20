"""Deterministic Blender build of the SF-SIM miniature Pier 3 (Hornblower Landing).

    blender -b --python build_pier_3.py -- [--out DIR]

Writes pier-3.blend and pier-3.glb next to this file (or into --out). Geometry is
authored directly in world space in metres, Z up, +X east, +Y north, so the model
drops into the city at its real-world heading — the loader applies no rotation.

Origin = the OSM pier polygon's area centroid (anchor lon -122.3947017,
lat 37.7982322), which is over open water. `placeGeneric` seats generic landmarks
at max(0, sampleElevation(x, z)), so **Z = 0 here is the waterline**, not the
promenade. Everything is quoted above that datum: pile heads 2.4 m, deck 3.0 m,
bulkhead cornice 13.2 m, parapet 14.0 m, and the attic crest over the arch
pediment at exactly 18.5 m, which is the bounding-box top.

Design (see REFERENCE.md for the sources behind every number):

* the measured OSM footprint (way 281428977, `man_made=pier`) — 212.8 x 53.5 m,
  long axis bearing 53.92 deg, flaring from ~40 m across at the head to 53.5 m at
  the Embarcadero. There is no `building` polygon for Pier 3 anywhere; the pier
  structure IS the footprint;
* a pile field and a deck soffit, because this thing stands in the bay and the
  app's camera reaches water level. A deck slab floating on nothing would be seen;
* the identity feature: the 1918 Beaux-Arts bulkhead portal — a projecting
  pedimented pavilion, one deep semicircular arch, and "PIER . 3" spelled out
  above it in proud blocky letters. The lettering is enlarged well past scale
  because incised text is invisible from the app's camera, and it is the only
  text on the asset;
* the 2006 rehabilitation's office block behind the bulkhead with its two big
  glazed roof monitors and its rank of rooftop plant — the surface the aerial
  camera actually lands on;
* the working deck: fendered edge, railing ribbon, bollards, light standards,
  two service sheds and 125-ish painted parking bays. It is a car park on a
  working pier and modelling it as anything grander would be a lie;
* night state: the arch soffit is the hero (a lit gateway reads at a distance
  when nothing else on a 3 m deck does), one roof monitor lit from within, and
  the deck light standards as amber points that draw the pier's LINE into the
  bay. The "PIER . 3" letters do NOT glow — a 1918 inscription is not signage.
  Glow surfaces are thin closed shells proud of the opaque surface (the app
  renders _Glow in a separate layer — never author a primary surface as glow).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# OSM way 281428977 projected with the app's tangent projection and recentred on
# the polygon's area centroid. CCW (outward normal = (t.y, -t.x)). Sub-2 m
# chamfers at the pier head are merged into single corners; the two ~13 m jogs on
# the northwest flank are real and kept.
FOOTPRINT = [
    (73.400, 78.000),    # 0 A  pier head, north corner
    (8.769, 32.101),     # 1 I
    (-0.726, 25.148),    # 2 H
    (-74.818, -27.988),  # 3 G
    (-86.328, -34.422),  # 4 F
    (-98.691, -38.003),  # 5 E  frontage, north end
    (-69.996, -83.291),  # 6 D  frontage, south end
    (-67.083, -75.299),  # 7 C
    (97.200, 46.400),    # 8 B  pier head, east corner
]

EDGE_FRONT = 5   # 53.6 m, faces SW — The Embarcadero, the bulkhead and the portal
EDGE_SE = 7      # 204.5 m, faces SE 143.5 deg — the slip toward Pier 1 1/2
EDGE_HEAD = 8    # 39.6 m, faces NE 53.0 deg — the seaward end

# The pier frame. s runs seaward along the axis, t runs to the southeast across
# it, both measured from the anchor. Everything above deck level is built on this
# frame rather than on the footprint edges: the Embarcadero is square to the pier
# axis (bulkhead line 324.0 deg) while OSM's frontage edge is traced 3.6 deg off
# it, and a bulkhead built on the traced edge comes out visibly skew.
AXIS_DEG = 53.92
AX = (math.sin(math.radians(AXIS_DEG)), math.cos(math.radians(AXIS_DEG)))
LT = (math.cos(math.radians(AXIS_DEG)), -math.sin(math.radians(AXIS_DEG)))

Z_PILE_TOP = 2.40     # deck soffit
Z_DECK = 3.00         # deck walking surface (= promenade, DataSF gnd_median 3.07)
Z_BULK_EAVE = 12.60   # top of the bulkhead wall
Z_CORNICE = 13.20     # top of the projecting cornice band
Z_PARAPET = 14.00     # bulkhead parapet crest (inferred)
Z_PED_APEX = 16.80    # portal pediment apex (inferred)
Z_CREST = 18.50       # attic block over the pediment = the bbox top (measured, 2.16)
Z_ARCH_SPRING = 8.00
Z_ARCH_CROWN = 12.50  # measured: 9.5 m above the promenade
Z_OFFICE = 12.40      # office block roof deck
Z_MONITOR = 13.30     # roof monitor ridge
Z_GROUND_TOP = 7.40   # bulkhead ground-storey ceiling line

# Bulkhead: 11 m deep, matching Pier 5's measured bulkhead (OSM way 91913148,
# 65.9 x 10.8 m). Narrower than the real frontage because the asset has to stay
# inside its own footprint — see REPORT.md.
BULK_S0, BULK_S1 = -101.0, -90.0
BULK_T0, BULK_T1 = -22.5, 21.0

OFFICE_S0, OFFICE_S1 = -88.0, -30.0
OFFICE_T0, OFFICE_T1 = -19.0, 18.0

PAVILION_T = -1.0     # portal centreline across the frontage
PAVILION_W = 11.0
PAVILION_PROUD = 0.80
ARCH_SPAN = 9.00

DECK_INSET = 0.40     # deck surface inset from the slab edge
CURB_W = 0.50
RAIL_H = 1.10

PALETTE_HEX = {
    "Toy_cream": "f2ede3",
    "Toy_sand": "ece4d4",
    "Toy_stone": "d9d2c2",
    # Deck walking surface. Toy_conc is not in the shipped palette, so the plan's
    # fallback applies: the deck takes Toy_stone's neighbour one step darker so
    # the slab, the deck and the parapet cap still read as three planes from
    # above. Off-palette is a WARN, not a FAIL (contract rule 7).
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


def poly_edge(i, poly=None):
    """Edge i: (origin, length, tangent unit, outward normal). CCW polygon."""
    poly = poly or FOOTPRINT
    a = poly[i]
    b = poly[(i + 1) % len(poly)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    return a, length, t, (t[1], -t[0])


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
    """Closed (u, z) profile: a doorway with a true semicircular head."""
    a = w / 2.0
    rise = z_crown - z_spring
    pts = [(-a, z0), (a, z0), (a, z_spring)]
    for k in range(1, seg):
        th = math.pi * k / seg
        pts.append((a * math.cos(th), z_spring + rise * math.sin(th)))
    pts.append((-a, z_spring))
    return pts


def arch_ring_profile(w, z0, z_spring, z_crown, band, seg=10):
    """Closed (u, z) profile of the voussoir surround: the arch head swept out
    by `band`, returned down both jambs to z0. One closed loop, no hole."""
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


def sbox(name, s0, s1, t0, t1, z0, z1, mat):
    """Axis-aligned box in the PIER frame."""
    corners = [pw(s0, t0), pw(s1, t0), pw(s1, t1), pw(s0, t1)]
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return new_mesh(name, verts, faces, [mat])


def ngon_post(name, s, t, z0, z1, r, mat, seg=6):
    ring = [
        pw(s + r * math.cos(2 * math.pi * k / seg), t + r * math.sin(2 * math.pi * k / seg))
        for k in range(seg)
    ]
    return prism(name, ring, z0, z1, mat)


def front_panel(name, profile, t_centre, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in the bulkhead's FRONT plane
    (constant s), extruded seaward-to-shoreward between s offsets d0 and d1.
    u runs across the pier (+t), matching the elevation as drawn."""
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


def ring_band(name, poly, z0, z1, off_in, off_out, mat):
    """Closed band following a polygon: 4 loops, quads between."""
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

# "PIER . 3" as blocky stencil glyphs: a list of (x0, x1, y0, y1) rectangles per
# glyph in a unit em (x 0..0.62, y 0..1). Extruded proud of the tympanum. Serifs
# are dropped — the real inscription's are a fraction of a pixel from the app's
# camera and the block forms read cleanly at a distance (plan 2.6).
BAR = 0.155
GLYPHS = {
    "P": [(0, BAR, 0, 1), (0, 0.62, 1 - BAR, 1), (0, 0.62, 0.5 - BAR / 2, 0.5 + BAR / 2),
          (0.62 - BAR, 0.62, 0.5 - BAR / 2, 1)],
    "I": [(0.23, 0.39, 0, 1)],
    "E": [(0, BAR, 0, 1), (0, 0.62, 1 - BAR, 1), (0, 0.56, 0.5 - BAR / 2, 0.5 + BAR / 2),
          (0, 0.62, 0, BAR)],
    "R": [(0, BAR, 0, 1), (0, 0.62, 1 - BAR, 1), (0, 0.62, 0.5 - BAR / 2, 0.5 + BAR / 2),
          (0.62 - BAR, 0.62, 0.5 - BAR / 2, 1), (0.62 - BAR, 0.62, 0, 0.5 - BAR / 2)],
    ".": [(0.15, 0.32, 0, 0.17)],
    "3": [(0, 0.62, 1 - BAR, 1), (0.10, 0.62, 0.5 - BAR / 2, 0.5 + BAR / 2),
          (0, 0.62, 0, BAR), (0.62 - BAR, 0.62, 0.5, 1), (0.62 - BAR, 0.62, 0, 0.5)],
}
ADVANCE = {"P": 0.80, "I": 0.52, "E": 0.80, "R": 0.80, ".": 0.47, "3": 0.80}


def inscription(text, t_centre, z_base, cap_h, d0, d1, mat, tag="letter"):
    """Proud blocky lettering on the pavilion's tympanum, centred on t_centre."""
    width = sum(ADVANCE[c] for c in text) * cap_h
    u = -width / 2.0
    n = 0
    for ch in text:
        for x0, x1, y0, y1 in GLYPHS[ch]:
            prof = [
                (u + x0 * cap_h, z_base + y0 * cap_h),
                (u + x1 * cap_h, z_base + y0 * cap_h),
                (u + x1 * cap_h, z_base + y1 * cap_h),
                (u + x0 * cap_h, z_base + y1 * cap_h),
            ]
            front_panel(f"{tag}{n}", prof, t_centre, d0, d1, mat)
            n += 1
        u += ADVANCE[ch] * cap_h
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
    sand = material("Toy_sand")
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
    # Pile field. Only under the edge band and a centre spine: a full 1918 grid
    # would be ~400 piles, invisible from every camera that matters, and a third
    # of the triangle budget. Hard-capped so a footprint edit cannot blow it up.
    inner = offset_polygon(FOOTPRINT, -1.2)
    core = offset_polygon(FOOTPRINT, -11.0)
    piles = 0
    step = 7.5
    smin, smax, tmin, tmax = -110, 110, -30, 30
    s = math.ceil(smin / step) * step
    while s <= smax and piles < 150:
        t = math.ceil(tmin / step) * step
        while t <= tmax and piles < 150:
            x, y = pw(s, t)
            if point_in_poly(x, y, inner) and (
                not point_in_poly(x, y, core) or abs(t) < step / 2.0
            ):
                sbox(f"pile{piles}", s - 0.45, s + 0.45, t - 0.45, t + 0.45, 0.0, Z_PILE_TOP, stone)
                piles += 1
            t += step
        s += step

    # Deck slab (the soffit band the piles carry) and the walking surface.
    prism("deck_slab", FOOTPRINT, Z_PILE_TOP, Z_DECK, stone)
    prism("deck_surface", offset_polygon(FOOTPRINT, -DECK_INSET), Z_DECK, Z_DECK + 0.05, conc)

    # Fender curb: chunky dark ring round everything except the frontage.
    ring_band("curb", FOOTPRINT, Z_DECK, Z_DECK + 0.50, -CURB_W, 0.0, ink)

    # Railing ribbon, held in off the curb, on both flanks and the head only.
    rail = offset_polygon(FOOTPRINT, -(CURB_W + 0.30))
    ring_band("railing", rail, Z_DECK + 0.55, Z_DECK + RAIL_H, -0.12, 0.0, steel)

    # ------------------------------------------------------------- deck fitout
    # Painted bays: two double-loaded rows over the outer deck. Stripes, not
    # boxes — 125 modelled stalls would cost more than the bulkhead.
    n = 0
    for t0, t1 in ((-17.0, -6.0), (5.0, 16.0)):
        s = -22.0
        while s <= 92.0:
            sbox(f"bay{n}", s - 0.09, s + 0.09, t0, t1, Z_DECK + 0.05, Z_DECK + 0.07, trim)
            n += 1
            s += 5.4
    sbox("bay_aisle_n", -22.0, 92.0, -6.2, -6.0, Z_DECK + 0.05, Z_DECK + 0.07, trim)
    sbox("bay_aisle_s", -22.0, 92.0, 4.8, 5.0, Z_DECK + 0.05, Z_DECK + 0.07, trim)

    # Bollards and light standards down both flanks.
    n = 0
    s = -80.0
    while s <= 96.0:
        for t in (-18.6, 18.2):
            ngon_post(f"bollard{n}", s, t, Z_DECK + 0.05, Z_DECK + 0.50, 0.22, ink)
            n += 1
        s += 12.0
    lamps = []
    n = 0
    s = -74.0
    while s <= 94.0:
        for t in (-19.4, 19.0):
            ngon_post(f"lamp{n}", s, t, Z_DECK, Z_DECK + 5.50, 0.22, ink, seg=4)
            sbox(f"lamphead{n}", s - 0.58, s + 0.58, t - 0.32, t + 0.32,
                 Z_DECK + 5.56, Z_DECK + 5.95, steel)
            lamps.append((s, t))
            n += 1
        s += 24.0

    # Two service sheds on the outer deck (the "single-storey addition" family).
    # Steel bodies came back near-black from the aerial against a pale deck; they
    # take the office's sand with a steel roof instead.
    sbox("shed_a", 26.0, 34.0, 9.0, 13.0, Z_DECK + 0.05, Z_DECK + 3.20, sand)
    sbox("shed_a_roof", 25.7, 34.3, 8.7, 13.3, Z_DECK + 3.20, Z_DECK + 3.35, steel)
    sbox("shed_b", 58.0, 66.0, -13.0, -9.0, Z_DECK + 0.05, Z_DECK + 3.20, sand)
    sbox("shed_b_roof", 57.7, 66.3, -13.3, -8.7, Z_DECK + 3.20, Z_DECK + 3.35, steel)

    # Belt-railway remnant. The National Register nomination records the rails
    # still in the north breezeway, and two hairlines running the length of a
    # 190 m deck are the cheapest thing on this asset that makes it read as a
    # 1918 freight pier rather than a car park with a nice front door.
    for k, t in enumerate((-15.6, -14.2)):
        sbox(f"rail{k}", -24.0, 96.0, t - 0.10, t + 0.10,
             Z_DECK + 0.05, Z_DECK + 0.16, steel)

    # Fixed passenger boarding structures at the excursion berths: a platform
    # over the deck edge and a light canopy. The vessels are not in the GLB; the
    # gangway platforms are, because they are built and they do not sail away.
    for k, (s_c, t_edge, sgn) in enumerate(((-4.0, -19.0, -1.0), (34.0, -19.0, -1.0),
                                            (14.0, 18.6, 1.0))):
        sbox(f"gang{k}_deck", s_c - 5.0, s_c + 5.0, t_edge, t_edge + sgn * 4.6,
             Z_DECK + 0.05, Z_DECK + 0.45, conc)
        sbox(f"gang{k}_rail_a", s_c - 5.0, s_c - 4.85, t_edge, t_edge + sgn * 4.6,
             Z_DECK + 0.45, Z_DECK + 1.45, steel)
        sbox(f"gang{k}_rail_b", s_c + 4.85, s_c + 5.0, t_edge, t_edge + sgn * 4.6,
             Z_DECK + 0.45, Z_DECK + 1.45, steel)
        sbox(f"gang{k}_canopy", s_c - 3.6, s_c + 3.6, t_edge - sgn * 0.6, t_edge + sgn * 3.0,
             Z_DECK + 3.10, Z_DECK + 3.34, steel)
        for j, u in enumerate((s_c - 3.2, s_c + 3.2)):
            ngon_post(f"gang{k}_post{j}", u, t_edge + sgn * 1.2,
                      Z_DECK + 0.45, Z_DECK + 3.10, 0.15, steel, seg=4)

    # ------------------------------------------------------------- office block
    sbox("office", OFFICE_S0, OFFICE_S1, OFFICE_T0, OFFICE_T1, Z_DECK, Z_OFFICE, sand)
    office_poly = [pw(OFFICE_S0, OFFICE_T0), pw(OFFICE_S1, OFFICE_T0),
                   pw(OFFICE_S1, OFFICE_T1), pw(OFFICE_S0, OFFICE_T1)]
    sbox("office_roof", OFFICE_S0 + 0.7, OFFICE_S1 - 0.7, OFFICE_T0 + 0.7, OFFICE_T1 - 0.7,
         Z_OFFICE - 0.02, Z_OFFICE + 0.08, steel)
    ring_band("office_parapet", office_poly, Z_OFFICE, Z_OFFICE + 0.75, -0.35, 0.05, sand)
    # Two window bands per flank, recessed behind the wall plane.
    for tag, t0, t1 in (("nw", OFFICE_T0 - 0.02, OFFICE_T0 + 0.22),
                        ("se", OFFICE_T1 - 0.22, OFFICE_T1 + 0.02)):
        for i, z in enumerate((5.20, 8.80)):
            sbox(f"office_glass_{tag}{i}", OFFICE_S0 + 2.5, OFFICE_S1 - 2.5, t0, t1,
                 z, z + 2.40, glass)
    for i, z in enumerate((5.20, 8.80)):
        sbox(f"office_glass_ne{i}", OFFICE_S1 - 0.22, OFFICE_S1 + 0.02,
             OFFICE_T0 + 2.5, OFFICE_T1 - 2.5, z, z + 2.40, glass)

    # The two glazed roof monitors — the identity from directly overhead.
    monitors = ((-80.0, -46.0, -14.0, -5.0), (-80.0, -46.0, 2.0, 11.0))
    for i, (s0, s1, t0, t1) in enumerate(monitors):
        sbox(f"monitor{i}_frame", s0, s1, t0, t1, Z_OFFICE + 0.05, Z_MONITOR - 0.18, steel)
        sbox(f"monitor{i}_glass", s0 + 0.35, s1 - 0.35, t0 + 0.35, t1 - 0.35,
             Z_MONITOR - 0.22, Z_MONITOR, glassl)

    # Nine rooftop units (replaced 2021) plus one screened plant enclosure.
    n = 0
    for row, t0 in enumerate((-17.4, 13.2)):
        for k in range(5 if row == 0 else 4):
            s0 = -78.0 + k * 4.2
            sbox(f"rtu{n}", s0, s0 + 2.6, t0, t0 + 2.0,
                 Z_OFFICE + 0.08, Z_OFFICE + 1.50, roofd)
            n += 1
    sbox("plant_screen", -44.0, -36.0, -6.0, 0.5, Z_OFFICE + 0.08, Z_OFFICE + 2.30, roofd)

    # ---------------------------------------------------------------- bulkhead
    prism(
        "bulkhead",
        [pw(BULK_S0, BULK_T0), pw(BULK_S1, BULK_T0), pw(BULK_S1, BULK_T1), pw(BULK_S0, BULK_T1)],
        Z_DECK,
        Z_BULK_EAVE,
        cream,
    )
    bulk_poly = [pw(BULK_S0, BULK_T0), pw(BULK_S1, BULK_T0), pw(BULK_S1, BULK_T1),
                 pw(BULK_S0, BULK_T1)]
    sbox("bulkhead_roof", BULK_S0 + 0.4, BULK_S1 - 0.4, BULK_T0 + 0.4, BULK_T1 - 0.4,
         Z_BULK_EAVE - 0.02, Z_BULK_EAVE + 0.10, steel)
    ring_band("cornice", bulk_poly, Z_BULK_EAVE, Z_CORNICE, -0.05, 0.45, stone)
    ring_band("parapet", bulk_poly, Z_CORNICE, Z_PARAPET - 0.22, -0.05, 0.05, cream)
    ring_band("parapet_cap", bulk_poly, Z_PARAPET - 0.22, Z_PARAPET, -0.16, 0.16, stone)

    # Rustication: three proud bands across the ground storey, front face only.
    for i, z in enumerate((4.20, 5.30, 6.40)):
        front_panel(f"rustic{i}", rect_profile(BULK_T1 - BULK_T0 - 0.2, z, z + 0.16),
                    (BULK_T0 + BULK_T1) / 2.0, BULK_S0 - 0.10, BULK_S0, stone)

    # Pilaster rhythm on the frontage, skipping the pavilion.
    pil_t = []
    span = BULK_T1 - BULK_T0
    bays = 11
    for k in range(bays + 1):
        pil_t.append(BULK_T0 + span * k / bays)
    for i, t in enumerate(pil_t):
        if abs(t - PAVILION_T) < PAVILION_W / 2.0 + 0.4:
            continue
        front_panel(f"pilaster{i}", rect_profile(1.10, Z_DECK, Z_BULK_EAVE), t,
                    BULK_S0 - 0.22, BULK_S0, cream)

    # Upper-storey windows and ground-floor shopfront openings between pilasters.
    lit_bays = set()
    for i in range(bays):
        t = (pil_t[i] + pil_t[i + 1]) / 2.0
        if abs(t - PAVILION_T) < PAVILION_W / 2.0 + 1.0:
            continue
        w = (pil_t[i + 1] - pil_t[i]) - 1.9
        front_panel(f"win_reveal{i}", rect_profile(w + 0.4, Z_GROUND_TOP + 0.9, Z_BULK_EAVE - 1.1),
                    t, BULK_S0 - 0.10, BULK_S0, ink)
        front_panel(f"win_glass{i}", rect_profile(w, Z_GROUND_TOP + 1.1, Z_BULK_EAVE - 1.3),
                    t, BULK_S0 - 0.20, BULK_S0 - 0.06, glass)
        front_panel(f"shop_reveal{i}", rect_profile(w + 0.6, Z_DECK + 0.1, Z_GROUND_TOP - 1.0),
                    t, BULK_S0 - 0.12, BULK_S0, ink)
        front_panel(f"shop_glass{i}", rect_profile(w + 0.2, Z_DECK + 0.3, Z_GROUND_TOP - 1.2),
                    t, BULK_S0 - 0.22, BULK_S0 - 0.08, glass)
        if i % 4 != 1:
            lit_bays.add(i)
            front_panel(f"win_glow{i}", rect_profile(w - 0.3, Z_GROUND_TOP + 1.3,
                                                     Z_BULK_EAVE - 1.5),
                        t, BULK_S0 - 0.27, BULK_S0 - 0.19, g_glass)
        # Awnings over the shopfronts.
        front_panel(f"awning{i}", rect_profile(w + 0.8, Z_GROUND_TOP - 0.95, Z_GROUND_TOP - 0.75),
                    t, BULK_S0 - 1.30, BULK_S0, steel)

    # Bulkhead end walls (they face the slips and the aerial camera reads them).
    for tag, t_edge, sign in (("nw", BULK_T0, -1.0), ("se", BULK_T1, 1.0)):
        for k, s_c in enumerate((BULK_S0 + 3.2, BULK_S0 + 7.6)):
            sbox(f"bulkend_{tag}{k}", s_c - 1.5, s_c + 1.5,
                 t_edge + sign * 0.02, t_edge + sign * 0.26,
                 Z_GROUND_TOP + 1.1, Z_BULK_EAVE - 1.3, glass)

    # ------------------------------------------------------------ portal pavilion
    pav_s0 = BULK_S0 - PAVILION_PROUD
    front_panel("pavilion", rect_profile(PAVILION_W, Z_DECK, Z_PARAPET), PAVILION_T,
                pav_s0, BULK_S1, cream)
    # Triangular pediment above the parapet line.
    ped = [(-PAVILION_W / 2.0 - 0.3, Z_PARAPET), (PAVILION_W / 2.0 + 0.3, Z_PARAPET),
           (0.0, Z_PED_APEX)]
    front_panel("pediment", ped, PAVILION_T, pav_s0, BULK_S0 + 3.0, cream)
    # Raking cornice. Review 1 built this as a solid triangle 0.4 m proud of the
    # pediment, which is a wall in front of the tympanum: it swallowed the whole
    # "PIER . 3" inscription. It is a frame, so it is modelled as one — a bed
    # mould and two rakes, with the tympanum left open behind them.
    pa = PAVILION_W / 2.0 + 0.55
    front_panel("pediment_bed", rect_profile(2 * pa + 0.9, Z_PARAPET - 0.42, Z_PARAPET + 0.02),
                PAVILION_T, pav_s0 - 0.42, pav_s0, stone)
    for sgn, tag in ((-1.0, "l"), (1.0, "r")):
        rake = [
            (sgn * pa, Z_PARAPET),
            (sgn * (pa - 0.62), Z_PARAPET),
            (0.0, Z_PED_APEX - 0.52),
            (0.0, Z_PED_APEX + 0.30),
        ]
        if sgn > 0:
            rake = rake[::-1]
        front_panel(f"pediment_rake_{tag}", rake, PAVILION_T, pav_s0 - 0.34, pav_s0, stone)
    # Attic block over the pediment — this sets the 18.5 m bounding-box top.
    sbox("attic", BULK_S0 - 0.55, BULK_S0 + 2.00, PAVILION_T - 2.85, PAVILION_T + 2.85,
         Z_PED_APEX - 1.30, Z_CREST - 0.20, cream)
    sbox("attic_cap", BULK_S0 - 0.75, BULK_S0 + 2.20, PAVILION_T - 3.05, PAVILION_T + 3.05,
         Z_CREST - 0.20, Z_CREST, stone)
    # The real pavilion carries a flagpole roughly 4 m above this cap. It is NOT
    # modelled. targetHeightM is the architectural top, and a mast at true height
    # would take the bounding box to ~22.5 m: either the whole 213 m pier gets
    # scaled down 18% to make 18.5 fit, or a 160 mm spike becomes the number the
    # entire asset is normalised against. Both are worse than leaving it off.
    # Documented in REPORT.md as a deliberate omission (plan 2.15).

    # The arch: reveal, glazed screen, voussoir surround, glow soffit.
    front_panel("arch_reveal", arch_cut_profile(ARCH_SPAN, Z_DECK, Z_ARCH_SPRING, Z_ARCH_CROWN),
                PAVILION_T, pav_s0 - 0.02, BULK_S0 + 1.20, ink)
    front_panel("arch_screen",
                arch_cut_profile(ARCH_SPAN - 1.7, Z_DECK + 0.9, Z_ARCH_SPRING,
                                 Z_ARCH_CROWN - 0.95),
                PAVILION_T, pav_s0 - 0.09, pav_s0 - 0.03, glass)
    sbox("arch_mullion_v", pav_s0 - 0.13, pav_s0 - 0.07, PAVILION_T - 0.09, PAVILION_T + 0.09,
         Z_DECK + 0.9, Z_ARCH_CROWN - 1.1, steel)
    front_panel("arch_mullion_h", rect_profile(ARCH_SPAN - 1.9, Z_ARCH_SPRING - 0.09,
                                               Z_ARCH_SPRING + 0.09),
                PAVILION_T, pav_s0 - 0.13, pav_s0 - 0.07, steel)
    front_panel("arch_voussoir",
                arch_ring_profile(ARCH_SPAN, Z_DECK, Z_ARCH_SPRING, Z_ARCH_CROWN, 0.80),
                PAVILION_T, pav_s0 - 0.25, pav_s0, stone)
    # Hero glow: a thin shell inside the arch soffit, proud of the screen.
    front_panel("arch_glow",
                arch_cut_profile(ARCH_SPAN - 2.2, Z_ARCH_SPRING - 0.25, Z_ARCH_SPRING,
                                 Z_ARCH_CROWN - 0.85),
                PAVILION_T, pav_s0 - 0.17, pav_s0 - 0.11, g_amber)

    # "PIER . 3" on the tympanum. 1.15 m caps — well over the real ~0.7 m, which
    # is the one place the semantic exaggeration is spent (plan 2.6).
    letters = inscription("PIER.3", PAVILION_T, Z_PARAPET + 0.38, 1.05,
                          pav_s0 - 0.17, pav_s0, stone)

    # ------------------------------------------------------------------- night
    # One roof monitor lit from within.
    sbox("monitor_glow", -79.0, -47.0, 3.0, 10.0, Z_MONITOR - 0.06, Z_MONITOR + 0.06, g_glassl)
    # Deck light standards as amber points — this is what draws the pier's line
    # into the bay at night, and on a 3 m deck it is the only thing that will.
    for i, (s, t) in enumerate(lamps):
        sbox(f"lampglow{i}", s - 0.86, s + 0.86, t - 0.50, t + 0.50,
             Z_DECK + 5.42, Z_DECK + 5.56, g_amber)

    # ------------------------------------------------------------------ bevels
    # The chunky masses carry the miniature read and get the full 0.10/2. The
    # deck slab, curb and railing are 500 m of ring geometry: a 2-segment bevel
    # on those alone costs more than the bulkhead, so they get one segment. The
    # piles, bay stripes, glow shells and glass panels get none — sub-pixel
    # edges, and 118 beveled piles would be a third of the budget.
    HEAVY = ("bulkhead", "pavilion", "office", "attic", "attic_cap", "pediment",
             "arch_voussoir")
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if name.startswith(("pile", "bay", "letter", "lampglow", "win_glow")):
            continue
        if "glow" in name or "glass" in name:
            continue
        if name in HEAVY:
            bevel(obj, width=0.10, segments=2)
        elif name.startswith(("deck_", "curb", "railing")):
            bevel(obj, width=0.06, segments=1)
        else:
            bevel(obj, width=0.05, segments=1)

    print(f"[build] piles={piles} lamps={len(lamps)} letters={letters} lit_bays={sorted(lit_bays)}")
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
    print("[build] anchor lon/lat: -122.3947017 37.7982322 (OSM pier polygon area centroid)")
    print("[build] pier axis 53.92 deg true; frontage faces 233.92 deg (SW)")
    print("[build] Z=0 is the WATERLINE: piles 0-2.4, deck 3.0, crest 18.5")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "pier-3.blend")
    glb = os.path.join(out, "pier-3.glb")
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
